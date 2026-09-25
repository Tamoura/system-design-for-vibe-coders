import { and, desc, eq, isNotNull, lte } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { isDowngrade, PLANS, type PaidPlanId } from '@/core/plans';
import { MAX_TRIAL_EXTENSION_DAYS } from '@/core/staff';
import type { AuditSource } from '@/core/audit';
import { recordAudit, SYSTEM_SOURCE } from '../audit';
import { InvalidRequestError } from '../errors';
import { notify } from '../notifications';
import { planDowngradedEvent } from '../notifications/events';
import { recomputePlanInTx } from './plan';
import { getBillingProvider } from './provider';
import { syncCustomerFromStripe } from './sync';

const { organizations, subscriptions } = schema;

/*
 * Lesson 7.1 (🟡): the billing actions Beacon support can take. "Every write
 * goes through your service layer": these reuse the functions the product
 * uses (the provider, the Stripe sync, the plan recompute), never a raw
 * UPDATE, so Stripe, the plan snapshot, the monitors, the product events and
 * the downgrade email all stay consistent. Each one takes a reason and writes
 * an audit event with the staff member, the org, before and after.
 *
 * Who may call them is checked before (staffRoute): trial.extend (support,
 * billing), plan.comp (billing).
 */

/**
 * Extend a trial by `days` (1–14). Stripe first (the trial end lives there;
 * changing only our copy would bill on the old date), then the same sync the
 * webhook runs, with the audit event in its transaction.
 */
export async function extendTrial(orgId: string, days: number, reason: string, source: AuditSource, now = new Date()) {
  if (!Number.isInteger(days) || days < 1 || days > MAX_TRIAL_EXTENSION_DAYS) {
    throw new InvalidRequestError('invalid_days', `A trial can be extended by 1 to ${MAX_TRIAL_EXTENSION_DAYS} days at a time.`);
  }
  const provider = getBillingProvider();
  if (!provider) throw new InvalidRequestError('billing_disabled', 'Billing is not configured on this server.');
  const [trial] = await withOrg(orgId, (tx) =>
    tx
      .select()
      .from(subscriptions)
      .where(and(eq(subscriptions.organizationId, orgId), eq(subscriptions.status, 'trialing')))
      .orderBy(desc(subscriptions.currentPeriodEnd))
      .limit(1),
  );
  if (!trial?.trialEnd) throw new InvalidRequestError('no_trial', 'This organization has no subscription in a trial.');

  const before = trial.trialEnd;
  // Extend from the current end (or from now, if it is somehow already past).
  const after = new Date(Math.max(before.getTime(), now.getTime()) + days * 86_400_000);
  await provider.extendTrial(trial.id, after); // network: outside any transaction

  const result = await syncCustomerFromStripe(trial.stripeCustomerId, {
    source,
    inTransaction: async (tx) => {
      await recordAudit(tx, {
        orgId,
        action: 'billing.trial_extended',
        source,
        target: { type: 'subscription', id: trial.id },
        changes: { trial_end: { before: before.toISOString(), after: after.toISOString() } },
        metadata: { days },
        reason,
        at: now,
      });
    },
  });
  if (!result.synced) throw new InvalidRequestError('sync_failed', `The trial was extended in the billing provider, but the sync failed (${result.reason}).`);
  return { before, after };
}

/**
 * "Comp plan": give the org `plan` free of charge, for `months` or until
 * removed. The snapshot becomes the better of the comp and the subscriptions
 * (recomputePlanInTx), so a comp never downgrades a paying customer.
 */
export async function compPlan(orgId: string, input: { plan: PaidPlanId; months?: number }, reason: string, source: AuditSource, now = new Date()) {
  const until = input.months ? addMonths(now, input.months) : null;
  return withOrg(orgId, async (tx) => {
    const [before] = await tx
      .select({ compPlan: organizations.compPlan, compPlanUntil: organizations.compPlanUntil })
      .from(organizations)
      .where(eq(organizations.id, orgId))
      .for('update');
    await tx.update(organizations).set({ compPlan: input.plan, compPlanUntil: until }).where(eq(organizations.id, orgId));
    await recordAudit(tx, {
      orgId,
      action: 'billing.plan_comped',
      source,
      target: { type: 'organization', id: orgId },
      changes: {
        comp_plan: { before: before.compPlan, after: input.plan },
        comp_plan_until: { before: before.compPlanUntil?.toISOString() ?? null, after: until?.toISOString() ?? null },
      },
      metadata: { plan_name: PLANS[input.plan].name, months: input.months ?? null },
      reason,
      at: now,
    });
    return recomputePlanInTx(tx, orgId, source, now);
  });
}

/** Remove a comp (by staff, or because it expired). Emails billing people if the plan goes down. */
export async function removeComp(orgId: string, reason: string, source: AuditSource, now = new Date()) {
  const result = await withOrg(orgId, async (tx) => {
    const [before] = await tx
      .select({ compPlan: organizations.compPlan, compPlanUntil: organizations.compPlanUntil })
      .from(organizations)
      .where(eq(organizations.id, orgId))
      .for('update');
    if (!before.compPlan) return null;
    await tx.update(organizations).set({ compPlan: null, compPlanUntil: null }).where(eq(organizations.id, orgId));
    await recordAudit(tx, {
      orgId,
      action: 'billing.comp_removed',
      source,
      target: { type: 'organization', id: orgId },
      changes: { comp_plan: { before: before.compPlan, after: null }, comp_plan_until: { before: before.compPlanUntil?.toISOString() ?? null, after: null } },
      reason,
      at: now,
    });
    return recomputePlanInTx(tx, orgId, source, now);
  });
  if (result && isDowngrade(result.previousPlan, result.plan)) {
    const [org] = await db.select({ id: organizations.id, name: organizations.name, slug: organizations.slug }).from(organizations).where(eq(organizations.id, orgId));
    await notify(planDowngradedEvent(org, { from: result.previousPlan, to: result.plan, frozen: result.frozen, at: now }));
  }
  return result;
}

/** The worker's `billing.comps` job (hourly): end the comps whose date has passed. */
export async function expireComps(now = new Date()) {
  const due = await db
    .select({ id: organizations.id })
    .from(organizations)
    .where(and(isNotNull(organizations.compPlan), lte(organizations.compPlanUntil, now)));
  for (const org of due) await removeComp(org.id, 'The complimentary plan reached its end date.', SYSTEM_SOURCE, now);
  return { expired: due.length };
}

function addMonths(d: Date, n: number) {
  const r = new Date(d);
  r.setUTCMonth(r.getUTCMonth() + n);
  return r;
}
