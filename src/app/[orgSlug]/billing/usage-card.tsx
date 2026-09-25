import { PLANS } from '@/core/plans';
import { formatCents } from '@/core/usage';
import type { BillingOverview } from '@/lib/billing';

const day = (d: Date) => d.toISOString().slice(0, 10);

/**
 * Lessons 3.2 and 3.3: where the org stands. Shown on the billing page and in
 * settings. "This period" is the subscription's billing period (lesson 3.3),
 * the calendar month only for orgs without one.
 */
export function UsageCard({ overview }: { overview: BillingOverview }) {
  const { ent, monitors, usage } = overview;
  const { sms } = usage;
  return (
    <div className="card grid" data-testid="usage">
      <div className="row">
        <strong>Plan and usage</strong>
        <span className="badge" data-testid="current-plan">{PLANS[ent.plan].name}</span>
      </div>
      <div>
        Monitors: <strong data-testid="monitor-usage">{monitors.total} of {ent.maxMonitors}</strong>
        {monitors.frozen > 0 && <span className="error"> · {monitors.frozen} paused by the plan limit</span>}
      </div>
      <div>
        SMS used this period: <strong data-testid="sms-usage">{sms.used} of {sms.included} included</strong>
        <span className="muted"> ({day(usage.period.start)} to {day(usage.period.end)})</span>
        {sms.overageUnits > 0 && (
          <div className="error">
            {sms.overageUnits} over the included amount: {formatCents(sms.overageCents)} will be added to the next invoice.
          </div>
        )}
      </div>
      <div className="muted">
        Checks at most every {ent.minIntervalSec} seconds · SSO {ent.sso ? '✓' : '✗'} · audit log {ent.auditLog ? `✓ (${ent.auditLogRetentionDays} days)` : '✗'} · API {ent.api ? '✓' : '✗'}
      </div>
    </div>
  );
}
