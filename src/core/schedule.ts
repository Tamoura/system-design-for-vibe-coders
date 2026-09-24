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
 * TODO(5.1): a real scheduler replaces "run the script from cron"; it keeps
 * this rule.
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
