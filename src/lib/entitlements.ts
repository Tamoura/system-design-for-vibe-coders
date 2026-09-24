import { and, count, eq, inArray, lt, notInArray, sql as dsql } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg, type TenantTx } from '@/db/tenant';
import { cheapestPlanWhere, entitlementsFor, PLANS, planFreeze, type Entitlements, type PausedReason, type PlanId } from '@/core/plans';
import { intervalLabel, isUuid } from '@/core/validation';
import { LimitExceededError } from './errors';

const { organizations, monitors } = schema;

/*
 * Lesson 3.2: the entitlements layer.
 *
 *   organizations.plan (snapshot, written by the Stripe sync)
 *        │
 *        ▼
 *   getEntitlements(org) ──► assert…() in every write path (API, forms)
 *                        ──► UI hints (disabled intervals, "Upgrade to add more")
 *                        ──► the check runner (paused and interval rules)
 *
 * Enforcement is on the SERVER, at the point of action. The UI reads the same
 * entitlements only to be helpful; the API and anyone with dev tools skip it.
 */

export type OrgEntitlements = Entitlements & { plan: PlanId };

/** What this organization may do or have right now. */
export async function getEntitlements({ orgId }: { orgId: string }): Promise<OrgEntitlements> {
  const [org] = await db.select({ plan: organizations.plan }).from(organizations).where(eq(organizations.id, orgId)).limit(1);
  const plan = org?.plan ?? 'free';
  return { plan, ...entitlementsFor(plan) };
}

/** The same, inside a withOrg() transaction (so the check and the write see the same snapshot). */
export async function entitlementsInTx(tx: TenantTx, orgId: string): Promise<OrgEntitlements> {
  const [org] = await tx.select({ plan: organizations.plan }).from(organizations).where(eq(organizations.id, orgId)).limit(1);
  const plan = org?.plan ?? 'free';
  return { plan, ...entitlementsFor(plan) };
}

/** An interval shorter than the plan's minimum is refused. */
export function assertIntervalAllowed(ent: OrgEntitlements, intervalSeconds: number): void {
  if (intervalSeconds >= ent.minIntervalSec) return;
  const upgradeTo = cheapestPlanWhere((e) => e.minIntervalSec <= intervalSeconds);
  throw new LimitExceededError(
    'minIntervalSec',
    ent.minIntervalSec,
    `Your ${PLANS[ent.plan].name} plan checks at most every ${intervalLabel(ent.minIntervalSec)}.` +
      (upgradeTo ? ` Upgrade to ${PLANS[upgradeTo].name} for ${intervalLabel(intervalSeconds)} checks.` : ''),
    upgradeTo,
  );
}

/**
 * The org may have at most `maxMonitors` monitors: all of them, running or
 * paused. (After a downgrade an org can have more than that, frozen; it
 * then cannot add more until it is back under the limit.)
 *
 * Count-then-insert has a race: two requests at 4 of 5 can both pass. For a
 * cheap resource like a monitor the lesson accepts that small overshoot;
 * making it race-safe is 3.2's 🔴 exercise.
 */
export async function assertCanCreateMonitor(tx: TenantTx, orgId: string, ent: OrgEntitlements): Promise<void> {
  const [{ n }] = await tx.select({ n: count() }).from(monitors).where(eq(monitors.organizationId, orgId));
  if (n < ent.maxMonitors) return;
  throw monitorLimitError(ent);
}

/** Un-pausing a monitor needs a free running slot (at most `maxMonitors` run at once). */
export async function assertCanRunAnotherMonitor(tx: TenantTx, orgId: string, ent: OrgEntitlements): Promise<void> {
  const [{ n }] = await tx
    .select({ n: count() })
    .from(monitors)
    .where(and(eq(monitors.organizationId, orgId), eq(monitors.paused, false)));
  if (n < ent.maxMonitors) return;
  const upgradeTo = cheapestPlanWhere((e) => e.maxMonitors > ent.maxMonitors);
  throw new LimitExceededError(
    'runningMonitors',
    ent.maxMonitors,
    `Your ${PLANS[ent.plan].name} plan runs ${ent.maxMonitors} monitors at a time. Pause another one first` +
      (upgradeTo ? `, or upgrade to ${PLANS[upgradeTo].name}.` : '.'),
    upgradeTo,
  );
}

function monitorLimitError(ent: OrgEntitlements) {
  const upgradeTo = cheapestPlanWhere((e) => e.maxMonitors > ent.maxMonitors);
  return new LimitExceededError(
    'maxMonitors',
    ent.maxMonitors,
    `Your ${PLANS[ent.plan].name} plan includes ${ent.maxMonitors} monitors.` +
      (upgradeTo ? ` Upgrade to ${PLANS[upgradeTo].name} to add more.` : ''),
    upgradeTo,
  );
}

/**
 * Lesson 3.2 (🟡): make an org's monitors fit its (new) plan. Called by the
 * Stripe sync on every change, so it runs for voluntary downgrades, for
 * involuntary ones (a failed payment ends the subscription) and for upgrades.
 * Idempotent: running it twice changes nothing the second time.
 *
 *   intervals below the plan's minimum  → raised to the minimum
 *   more running monitors than allowed  → the newest are frozen ('plan_limit')
 *   room again and some frozen          → the oldest frozen run again
 *
 * Nothing is deleted. Monitors paused by hand are never touched.
 */
export async function reconcileMonitorsWithPlan(tx: TenantTx, orgId: string, ent: Entitlements) {
  const clamped = await tx
    .update(monitors)
    .set({ intervalSeconds: ent.minIntervalSec })
    .where(and(eq(monitors.organizationId, orgId), lt(monitors.intervalSeconds, ent.minIntervalSec)))
    .returning({ id: monitors.id });

  const rows = await tx
    .select({ id: monitors.id, createdAt: monitors.createdAt, pausedReason: monitors.pausedReason })
    .from(monitors)
    .where(and(eq(monitors.organizationId, orgId), dsql`${monitors.pausedReason} is distinct from 'manual'`));
  const { freeze, unfreeze } = planFreeze(rows, ent.maxMonitors);
  if (freeze.length) {
    await tx
      .update(monitors)
      .set({ paused: true, pausedReason: 'plan_limit' })
      .where(and(eq(monitors.organizationId, orgId), inArray(monitors.id, freeze)));
  }
  if (unfreeze.length) {
    await tx
      .update(monitors)
      .set({ paused: false, pausedReason: null })
      .where(and(eq(monitors.organizationId, orgId), inArray(monitors.id, unfreeze), eq(monitors.pausedReason, 'plan_limit')));
  }
  return { clamped: clamped.length, frozen: freeze.length, unfrozen: unfreeze.length };
}

/** For the UI: where the org stands against its monitor limit. */
export async function getMonitorUsage({ orgId }: { orgId: string }) {
  return withOrg(orgId, async (tx) => {
    const ent = await entitlementsInTx(tx, orgId);
    const rows = await tx
      .select({ reason: monitors.pausedReason, n: count() })
      .from(monitors)
      .where(eq(monitors.organizationId, orgId))
      .groupBy(monitors.pausedReason);
    const by = (r: PausedReason | null) => rows.find((x) => x.reason === r)?.n ?? 0;
    const total = rows.reduce((sum, r) => sum + r.n, 0);
    return {
      ent,
      total,
      running: by(null),
      frozen: by('plan_limit'),
      atLimit: total >= ent.maxMonitors,
    };
  });
}

/**
 * Lesson 3.2 (🟡): after a downgrade, the owner picks which monitors run.
 * `keepIds` (at most maxMonitors) run; every other monitor that is not
 * paused by hand is frozen. Ids from another org match nothing (RLS and the
 * WHERE both say so), so they cannot be switched on from here.
 */
export async function chooseRunningMonitors({ orgId }: { orgId: string }, keepIds: string[]) {
  return withOrg(orgId, async (tx) => {
    const ent = await entitlementsInTx(tx, orgId);
    const unique = [...new Set(keepIds)].filter(isUuid);
    if (unique.length > ent.maxMonitors) throw monitorLimitErrorForChoice(ent);
    const notManual = and(eq(monitors.organizationId, orgId), dsql`${monitors.pausedReason} is distinct from 'manual'`);
    await tx
      .update(monitors)
      .set({ paused: true, pausedReason: 'plan_limit' })
      .where(unique.length ? and(notManual, notInArray(monitors.id, unique)) : notManual);
    if (unique.length) {
      await tx
        .update(monitors)
        .set({ paused: false, pausedReason: null })
        .where(and(notManual, inArray(monitors.id, unique)));
    }
  });
}

function monitorLimitErrorForChoice(ent: OrgEntitlements) {
  return new LimitExceededError(
    'runningMonitors',
    ent.maxMonitors,
    `Your ${PLANS[ent.plan].name} plan runs ${ent.maxMonitors} monitors at a time. Pick at most ${ent.maxMonitors}.`,
    cheapestPlanWhere((e) => e.maxMonitors > ent.maxMonitors),
  );
}

/** The monitors a downgrade froze, and the ones running, for the "choose" page. */
export async function listPlanLimitedMonitors({ orgId }: { orgId: string }) {
  return withOrg(orgId, (tx) =>
    tx
      .select({ id: monitors.id, name: monitors.name, url: monitors.url, pausedReason: monitors.pausedReason, createdAt: monitors.createdAt })
      .from(monitors)
      .where(and(eq(monitors.organizationId, orgId), dsql`${monitors.pausedReason} is distinct from 'manual'`))
      .orderBy(monitors.createdAt),
  );
}
