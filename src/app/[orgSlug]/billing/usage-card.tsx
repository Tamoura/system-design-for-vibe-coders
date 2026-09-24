import { PLANS } from '@/core/plans';
import type { BillingOverview } from '@/lib/billing';

/** Lesson 3.2: where the org stands. Shown on the billing page and in settings. */
export function UsageCard({ overview }: { overview: BillingOverview }) {
  const { ent, monitors } = overview;
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
      <div className="muted">
        Checks at most every {ent.minIntervalSec} seconds · SSO {ent.sso ? '✓' : '✗'} · audit log {ent.auditLog ? '✓' : '✗'} · API {ent.api ? '✓' : '✗'}
      </div>
    </div>
  );
}
