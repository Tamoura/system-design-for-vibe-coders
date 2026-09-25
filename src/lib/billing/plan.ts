import { eq } from 'drizzle-orm';
import { schema } from '@/db';
import type { TenantTx } from '@/db/tenant';
import { entitlementsFor, planFromSubscriptions, planRank, type PlanId } from '@/core/plans';
import type { AuditSource } from '@/core/audit';
import { trackInTx } from '../analytics';
import { recordAudit } from '../audit';
import { reconcileMonitorsWithPlan } from '../entitlements';

const { organizations, subscriptions } = schema;

/**
 * Lesson 3.2 + 7.1: THE function that decides an org's plan snapshot, used by
 * both front doors:
 *
 *   the Stripe webhook sync (src/lib/billing/sync.ts)       after a subscription changed
 *   Beacon support (src/lib/billing/support.ts)             "Comp plan", "Extend trial"
 *   the worker's billing.comps job                          a comp that reached its end date
 *
 * plan = the better of what the subscriptions grant and an unexpired comp.
 * On a change, in the caller's transaction: the snapshot, the product event
 * (6.2), the audit event (7.3), and the monitors fitted to the new limits
 * (freeze on downgrade, unfreeze on upgrade). Because the scheduler and every
 * limit check read the snapshot from Postgres, the new limit applies on the
 * next check and the next request: no restart, no cache to clear.
 */
export async function recomputePlanInTx(tx: TenantTx, orgId: string, source: AuditSource, now = new Date()) {
  const all = await tx.select().from(subscriptions).where(eq(subscriptions.organizationId, orgId));
  // Lock the org row, then compare and set the plan snapshot. Two syncs for
  // the same org (two webhooks at once) queue here, so exactly one of them
  // sees "Pro → Free", and the owner gets exactly one email per downgrade.
  const [org] = await tx
    .select({ plan: organizations.plan, compPlan: organizations.compPlan, compPlanUntil: organizations.compPlanUntil })
    .from(organizations)
    .where(eq(organizations.id, orgId))
    .for('update');
  const fromSubscriptions = planFromSubscriptions(all);
  const comp = activeComp(org, now);
  const plan: PlanId = comp && planRank(comp) > planRank(fromSubscriptions) ? comp : fromSubscriptions;
  const previousPlan = org.plan;

  if (previousPlan !== plan) {
    await tx.update(organizations).set({ plan }).where(eq(organizations.id, orgId));
    // Lesson 6.2 (🟡): revenue events, server-side, after the change committed.
    await trackInTx(tx, { orgId }, planRank(plan) > planRank(previousPlan) ? 'subscription_upgraded' : 'subscription_downgraded', {
      from_plan: previousPlan,
      to_plan: plan,
    });
    // Lesson 7.3: billing changes are security-relevant ("who gave Acme free Business?").
    await recordAudit(tx, {
      orgId,
      action: 'billing.plan_changed',
      source,
      target: { type: 'organization', id: orgId },
      changes: { plan: { before: previousPlan, after: plan } },
      metadata: { from_subscriptions: fromSubscriptions, comp: comp ?? null },
      at: now,
    });
  }

  const changes = await reconcileMonitorsWithPlan(tx, orgId, entitlementsFor(plan));
  return { previousPlan, plan, ...changes };
}

/** A comp counts until its end date (none = until removed). */
export function activeComp(org: { compPlan: PlanId | null; compPlanUntil: Date | null }, now = new Date()): PlanId | null {
  if (!org.compPlan) return null;
  if (org.compPlanUntil && org.compPlanUntil <= now) return null;
  return org.compPlan;
}
