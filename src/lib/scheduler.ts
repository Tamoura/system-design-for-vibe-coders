import { and, eq, max } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { runCheck, type CheckOutcome } from '@/core/check';
import { effectiveIntervalSec, entitlementsFor } from '@/core/plans';
import { checkSlots, isDue } from '@/core/schedule';
import { recordCheckResult } from './checks';
import { enqueueInTx, type JobData } from './queue';

const { organizations, monitors, checkResults } = schema;

/*
 * Lesson 5.1: the check scheduler, which replaces "run a script from cron".
 *
 *   pg-boss cron, every minute ─► ONE `checks.schedule` job (whatever the number of workers)
 *        scheduleChecks(): for every running monitor, the slots in the next
 *        ~90 seconds (src/core/schedule.ts: a stable phase per monitor = jitter)
 *        ─► one `check.run` job per slot, startAfter = the slot, id = hash(monitor, slot)
 *   workers ─► runScheduledCheck(): HTTP check (outside any transaction) ─► recordCheckResult()
 *
 * The scheduler only decides WHAT is due; the workers do the checking (the
 * lesson's "separate the executor from the scheduler"). Each part scales on
 * its own: more workers check faster, the scheduler stays one small job.
 *
 * Why the window overlaps (from 30 s ago to 90 s ahead, every 60 s): pg-boss's
 * cron can fire a few seconds late, and a gap between two windows would skip
 * a check. The overlap costs nothing because the job id comes from the slot:
 * a slot enqueued by two runs is one job. A worker outage longer than the
 * window skips the missed slots instead of running a backlog of stale checks.
 */
export const WINDOW_BEHIND_MS = 30_000;
export const WINDOW_AHEAD_MS = 90_000;

/** The `checks.schedule` job. Returns how many new check jobs it added. */
export async function scheduleChecks(now = new Date()): Promise<{ monitors: number; enqueued: number }> {
  const from = new Date(now.getTime() - WINDOW_BEHIND_MS);
  const to = new Date(now.getTime() + WINDOW_AHEAD_MS);
  const orgs = await db.select({ id: organizations.id, plan: organizations.plan }).from(organizations);
  let count = 0;
  let enqueued = 0;
  for (const org of orgs) {
    // Lesson 3.2: the plan's minimum interval, from the same snapshot the API enforces.
    const ent = entitlementsFor(org.plan);
    // Lesson 2.4: a job that visits every org works inside withOrg(org.id), like a request.
    await withOrg(org.id, async (tx) => {
      const running = await tx
        .select({ id: monitors.id, intervalSeconds: monitors.intervalSeconds })
        .from(monitors)
        .where(and(eq(monitors.organizationId, org.id), eq(monitors.paused, false)));
      count += running.length;
      for (const m of running) {
        for (const slot of checkSlots(m.id, effectiveIntervalSec(m.intervalSeconds, ent), from, to)) {
          const id = await enqueueInTx(tx, 'check.run', { orgId: org.id, monitorId: m.id, scheduledAt: slot.toISOString() }, {
            key: `${m.id}@${slot.toISOString()}`, // the monitor + slot dedupe key
            startAfter: slot,
            group: org.id, // lesson 5.1 fairness: at most N of one org's checks run at once
          });
          if (id) enqueued++;
        }
      }
    });
  }
  return { monitors: count, enqueued };
}

/**
 * The `check.run` job. Idempotent in two ways (lesson 5.1, "record what you
 * did"): a paused or deleted monitor is skipped, and the result is stored
 * with its slot (`scheduled_at`, unique per monitor), so a job that runs
 * twice records one result and opens at most one incident.
 */
export async function runScheduledCheck(job: JobData['check.run'], check: (url: string) => Promise<CheckOutcome> = (url) => runCheck(url)): Promise<string> {
  const [org] = await db.select({ id: organizations.id, name: organizations.name, slug: organizations.slug }).from(organizations).where(eq(organizations.id, job.orgId));
  if (!org) return 'skipped: organization deleted';
  const [monitor] = await withOrg(org.id, (tx) =>
    tx
      .select()
      .from(monitors)
      .where(and(eq(monitors.organizationId, org.id), eq(monitors.id, job.monitorId))),
  );
  if (!monitor) return 'skipped: monitor deleted';
  if (monitor.paused) return 'skipped: monitor paused';
  const outcome = await check(monitor.url); // network: outside any transaction
  return recordCheckResult(org, monitor, outcome, new Date(), { scheduledAt: new Date(job.scheduledAt) });
}

/**
 * `npm run checks:run`: check monitors NOW instead of waiting for their slot
 * (for trying things out). Only monitors that are due by the old rule
 * (never checked, or their interval has passed), or every running one with
 * `all`. It only enqueues: the worker runs them.
 */
export async function enqueueChecksNow(opts: { all?: boolean; now?: Date } = {}): Promise<{ enqueued: number }> {
  const now = opts.now ?? new Date();
  const orgs = await db.select({ id: organizations.id, plan: organizations.plan }).from(organizations);
  let enqueued = 0;
  for (const org of orgs) {
    const ent = entitlementsFor(org.plan);
    await withOrg(org.id, async (tx) => {
      const running = await tx.select().from(monitors).where(and(eq(monitors.organizationId, org.id), eq(monitors.paused, false)));
      const last = await tx
        .select({ monitorId: checkResults.monitorId, at: max(checkResults.checkedAt) })
        .from(checkResults)
        .where(eq(checkResults.organizationId, org.id))
        .groupBy(checkResults.monitorId);
      const lastAt = new Map(last.map((r) => [r.monitorId, r.at]));
      for (const m of running) {
        if (!opts.all && !isDue({ ...m, lastCheckedAt: lastAt.get(m.id) ?? null }, ent, now)) continue;
        const slot = now.toISOString();
        if (await enqueueInTx(tx, 'check.run', { orgId: org.id, monitorId: m.id, scheduledAt: slot }, { key: `${m.id}@${slot}`, group: org.id })) enqueued++;
      }
    });
  }
  return { enqueued };
}
