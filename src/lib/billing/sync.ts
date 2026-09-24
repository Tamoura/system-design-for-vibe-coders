import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { can } from '@/core/permissions';
import { entitlementsFor, isDowngrade, planFromSubscriptions, PLANS, type PlanId } from '@/core/plans';
import { sendEmail } from '../email';
import { appUrl } from '../urls';
import { reconcileMonitorsWithPlan } from '../entitlements';
import { getBillingProvider } from './provider';

const { organizations, subscriptions, memberships, users } = schema;

export type SyncResult =
  | { synced: false; reason: 'unknown_customer' | 'billing_disabled' }
  | { synced: true; orgId: string; previousPlan: PlanId; plan: PlanId; frozen: number; unfrozen: number; clamped: number };

/**
 * Lesson 3.1 (🟡): bring our copy of a customer's subscriptions up to date.
 *
 * The webhook event is only a signal ("something changed for customer X").
 * We never trust its payload: we fetch the CURRENT state from the provider and
 * upsert it. That makes the sync
 *
 *  - order-proof: an old event arriving late still writes today's state;
 *  - repeatable: running it twice writes the same rows;
 *  - self-healing: delete a subscriptions row, and the next event puts it back.
 *
 * Then lesson 3.2: recompute the org's plan snapshot from the subscriptions,
 * and fit the org's monitors to it (freeze on downgrade, unfreeze on upgrade).
 */
export async function syncCustomerFromStripe(customerId: string): Promise<SyncResult> {
  const provider = getBillingProvider();
  if (!provider) return { synced: false, reason: 'billing_disabled' };

  // Which org is this? organizations is not a tenant table (it is how we find the tenant).
  const [org] = await db
    .select({ id: organizations.id, name: organizations.name, slug: organizations.slug })
    .from(organizations)
    .where(eq(organizations.stripeCustomerId, customerId))
    .limit(1);
  // A customer we did not create (another app on the same Stripe account, or
  // a deleted org). Nothing to do, and not an error: Stripe must not retry it.
  if (!org) return { synced: false, reason: 'unknown_customer' };

  // Network first, outside any transaction (rule from lesson 2.4).
  const fresh = await provider.listSubscriptions(customerId);

  const result = await withOrg(org.id, async (tx) => {
    for (const s of fresh) {
      const values = {
        stripeCustomerId: s.customerId,
        status: s.status,
        priceId: s.priceId,
        currentPeriodStart: s.currentPeriodStart,
        currentPeriodEnd: s.currentPeriodEnd,
        cancelAtPeriodEnd: s.cancelAtPeriodEnd,
      };
      await tx
        .insert(subscriptions)
        .values({ id: s.id, organizationId: org.id, ...values })
        .onConflictDoUpdate({ target: subscriptions.id, set: values });
    }

    const all = await tx.select().from(subscriptions).where(eq(subscriptions.organizationId, org.id));
    const plan = planFromSubscriptions(all);

    // Lock the org row, then compare and set the plan snapshot. Two syncs for
    // the same org (two webhooks at once) queue here, so exactly one of them
    // sees "Pro → Free", and the owner gets exactly one email per downgrade.
    const [locked] = await tx
      .select({ plan: organizations.plan })
      .from(organizations)
      .where(eq(organizations.id, org.id))
      .for('update');
    const previousPlan = locked.plan;
    if (previousPlan !== plan) await tx.update(organizations).set({ plan }).where(eq(organizations.id, org.id));

    const changes = await reconcileMonitorsWithPlan(tx, org.id, entitlementsFor(plan));
    return { previousPlan, plan, ...changes };
  });

  // Email after the transaction has committed, never inside it.
  // TODO(5.1): enqueue it as a job; the webhook should only sync and return.
  if (isDowngrade(result.previousPlan, result.plan)) {
    await emailDowngrade(org, result.previousPlan, result.plan, result.frozen);
  }
  return { synced: true, orgId: org.id, ...result };
}

/** Lesson 3.2 (🟡): "email the owner", once per downgrade: everyone who may manage billing. */
async function emailDowngrade(org: { id: string; name: string; slug: string }, from: PlanId, to: PlanId, frozen: number) {
  const people = await listBillingContacts(org.id);
  const ent = entitlementsFor(to);
  for (const person of people) {
    await sendEmail({
      to: person.email,
      template: 'plan-downgraded',
      props: {
        orgName: org.name,
        fromPlan: PLANS[from].name,
        toPlan: PLANS[to].name,
        maxMonitors: ent.maxMonitors,
        minIntervalSec: ent.minIntervalSec,
        frozen,
        url: appUrl(`/${org.slug}/${frozen > 0 ? 'monitors/plan-limit' : 'billing'}`),
      },
    });
  }
}

/** Members whose role may manage billing (lesson 1.3's permission map decides, not a role name). */
export async function listBillingContacts(orgId: string) {
  const rows = await db
    .select({ email: users.email, role: memberships.role })
    .from(memberships)
    .innerJoin(users, eq(users.id, memberships.userId))
    .where(eq(memberships.organizationId, orgId));
  return rows.filter((r) => can(r.role, 'billing.manage'));
}
