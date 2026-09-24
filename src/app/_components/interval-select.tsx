import Link from 'next/link';
import { cheapestPlanWhere, PLANS } from '@/core/plans';
import { ALLOWED_INTERVALS, intervalLabel } from '@/core/validation';

/**
 * Lesson 3.2 (🟢): the interval picker reads the org's entitlements. Options
 * below the plan's minimum are disabled and name the plan that unlocks them,
 * with an upgrade link for people who may manage billing. A courtesy only:
 * createMonitor/updateMonitor refuse those intervals on the server anyway.
 */
export function IntervalSelect({
  minIntervalSec,
  defaultValue,
  billingHref,
}: {
  minIntervalSec: number;
  defaultValue: string;
  /** Where "Upgrade" goes; null when the viewer may not manage billing. */
  billingHref: string | null;
}) {
  const locked = ALLOWED_INTERVALS.filter((s) => s < minIntervalSec);
  const fastest = locked[0];
  const unlockPlan = fastest === undefined ? null : cheapestPlanWhere((e) => e.minIntervalSec <= fastest);
  return (
    <>
      <select id="intervalSeconds" name="intervalSeconds" defaultValue={defaultValue}>
        {ALLOWED_INTERVALS.map((s) => {
          const plan = s < minIntervalSec ? cheapestPlanWhere((e) => e.minIntervalSec <= s) : null;
          return (
            <option key={s} value={s} disabled={plan !== null}>
              {intervalLabel(s)}
              {plan ? ` (${PLANS[plan].name})` : ''}
            </option>
          );
        })}
      </select>
      {unlockPlan && fastest !== undefined && (
        <span className="muted" data-testid="interval-upgrade-hint">
          Faster checks, down to {intervalLabel(fastest)}, come with {PLANS[unlockPlan].name}.{' '}
          {billingHref ? <Link href={billingHref}>Upgrade</Link> : 'Ask an owner to upgrade.'}
        </span>
      )}
    </>
  );
}
