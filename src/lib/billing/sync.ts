import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg, type TenantTx } from '@/db/tenant';
import { isDowngrade, type PlanId } from '@/core/plans';
import type { AuditSource } from '@/core/audit';
import { notify } from '../notifications';
import { planDowngradedEvent } from '../notifications/events';
import { recomputePlanInTx } from './plan';
import { getBillingProvider } from './provider';

/** Lesson 7.3: plan changes that come from Stripe are recorded as the system's doing. */
export const STRIPE_SYNC_SOURCE: AuditSource = { actor: { type: 'system', id: 'stripe', name: 'Stripe billing' }, via: 'worker' };

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
 *
 * Lesson 7.1: Beacon support's "Extend trial" changes Stripe first, then calls
 * this with its own audit source and an `inTransaction` step (its audit
 * event), so the copy, the plan and the evidence commit together.
 */
export async function syncCustomerFromStripe(
  customerId: string,
  opts: { source?: AuditSource; inTransaction?: (tx: TenantTx, orgId: string) => Promise<void> } = {},
): Promise<SyncResult> {
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
        trialEnd: s.trialEnd,
      };
      await tx
        .insert(subscriptions)
        .values({ id: s.id, organizationId: org.id, ...values })
        .onConflictDoUpdate({ target: subscriptions.id, set: values });
    }

    const recomputed = await recomputePlanInTx(tx, org.id, opts.source ?? STRIPE_SYNC_SOURCE);
    await opts.inTransaction?.(tx, org.id);
    return recomputed;
  });

  // Lesson 3.2 (🟡): "email the owner", once per downgrade. Since 4.2 it is a
  // notification in the required "billing" category (in-app + email to
  // everyone who may manage billing), queued here and sent by the worker (5.1).
  if (isDowngrade(result.previousPlan, result.plan)) {
    await notify(planDowngradedEvent(org, { from: result.previousPlan, to: result.plan, frozen: result.frozen, at: new Date() }));
  }
  return { synced: true, orgId: org.id, ...result };
}
