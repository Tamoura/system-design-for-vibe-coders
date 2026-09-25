import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { entitlementsFor, isDowngrade, planFromSubscriptions, planRank, type PlanId } from '@/core/plans';
import { trackInTx } from '../analytics';
import { notify } from '../notifications';
import { planDowngradedEvent } from '../notifications/events';
import { reconcileMonitorsWithPlan } from '../entitlements';
import { getBillingProvider } from './provider';

const { organizations, subscriptions } = schema;

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
    if (previousPlan !== plan) {
      await tx.update(organizations).set({ plan }).where(eq(organizations.id, org.id));
      // Lesson 6.2 (🟡): revenue events, server-side, after the webhook's sync
      // committed the new plan, never from the browser's "Upgrade" click. Once
      // per change, thanks to the row lock above.
      await trackInTx(tx, { orgId: org.id }, planRank(plan) > planRank(previousPlan) ? 'subscription_upgraded' : 'subscription_downgraded', {
        from_plan: previousPlan,
        to_plan: plan,
      });
    }

    const changes = await reconcileMonitorsWithPlan(tx, org.id, entitlementsFor(plan));
    return { previousPlan, plan, ...changes };
  });

  // Lesson 3.2 (🟡): "email the owner", once per downgrade. Since 4.2 it is a
  // notification in the required "billing" category (in-app + email to
  // everyone who may manage billing), queued here and sent by the worker (5.1).
  if (isDowngrade(result.previousPlan, result.plan)) {
    await notify(planDowngradedEvent(org, { from: result.previousPlan, to: result.plan, frozen: result.frozen, at: new Date() }));
  }
  return { synced: true, orgId: org.id, ...result };
}
