import { createHash } from 'node:crypto';
import { effectiveIntervalSec, type Entitlements } from './plans';

/**
 * Lesson 3.2 (🟡): which monitors the check runner may check now.
 *
 * Workers enforce entitlements too, and from the same snapshot as the API: a
 * downgraded org must not keep 30-second checks because the runner cached the
 * old plan. So a monitor is due when it was never checked, or when its
 * interval, raised to the plan's minimum, has passed. Paused monitors (by
 * hand or by the plan limit) never run.
 *
 * Lesson 5.1: the scheduler (checkSlots below) keeps the same rule by
 * spacing a monitor's slots by effectiveIntervalSec(). isDue() is still what
 * `npm run checks:run` uses to catch up on monitors by hand.
 */
export function isDue(
  monitor: { paused: boolean; intervalSeconds: number; lastCheckedAt: Date | null },
  ent: Pick<Entitlements, 'minIntervalSec'>,
  now: Date = new Date(),
): boolean {
  if (monitor.paused) return false;
  if (!monitor.lastCheckedAt) return true;
  return now.getTime() - monitor.lastCheckedAt.getTime() >= effectiveIntervalSec(monitor.intervalSeconds, ent) * 1000;
}

/**
 * Lesson 5.1: WHEN a monitor is checked. Every monitor gets a stable phase
 * offset inside its interval, derived from its id: a 60-second monitor whose
 * phase is 17 is checked at :17 of every minute, forever, on every worker.
 *
 * Why (the lesson's "add jitter"): if every 1-minute monitor ran at :00, the
 * workers would get 16,000 checks in the first second of each minute and
 * nothing for the other 59, and customers' servers would see Beacon's checks
 * as synchronized spikes. Hashing spreads monitors evenly across the interval,
 * and because the phase never changes, the spacing between two checks of one
 * monitor is always exactly its interval.
 */
export function phaseOffsetSec(monitorId: string, intervalSec: number): number {
  const n = createHash('sha256').update(monitorId).digest().readUInt32BE(0);
  return n % intervalSec;
}

/**
 * The check times ("slots") of one monitor that fall in [from, to): every
 * t = k × interval + phase, in whole seconds since the epoch. The scheduler
 * asks for a window a little wider than its own period, so windows overlap;
 * the job id is derived from the slot (see src/lib/scheduler.ts), so a slot
 * enqueued twice is one job.
 */
export function checkSlots(monitorId: string, intervalSec: number, from: Date, to: Date): Date[] {
  const phase = phaseOffsetSec(monitorId, intervalSec);
  const start = Math.ceil(from.getTime() / 1000);
  const end = to.getTime() / 1000;
  const slots: Date[] = [];
  // First slot at or after `from`.
  let t = start - ((((start - phase) % intervalSec) + intervalSec) % intervalSec);
  if (t < start) t += intervalSec;
  for (; t < end; t += intervalSec) slots.push(new Date(t * 1000));
  return slots;
}
