import Link from 'next/link';
import { can } from '@/core/permissions';
import { cheapestPlanWhere, PLANS } from '@/core/plans';
import { forPage, requirePermission } from '@/lib/access';
import { getMonitorUsage } from '@/lib/entitlements';
import { NewMonitorForm } from './new-monitor-form';

export default async function NewMonitorPage({ params }: { params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.write'), `/${orgSlug}/monitors/new`);
  // Lesson 3.2: the form reads the same entitlements the server enforces.
  const usage = await getMonitorUsage(ctx);
  const billingHref = can(ctx.role, 'billing.manage') ? `/${ctx.orgSlug}/billing` : null;
  if (usage.atLimit) {
    const next = cheapestPlanWhere((e) => e.maxMonitors > usage.ent.maxMonitors);
    return (
      <section className="card grid" style={{ maxWidth: 520 }} data-testid="monitor-limit">
        <h1 style={{ margin: 0 }}>Upgrade to add more monitors</h1>
        <p style={{ margin: 0 }}>
          Your {PLANS[usage.ent.plan].name} plan includes {usage.ent.maxMonitors} monitors, and this organization has {usage.total}.
          {next && ` ${PLANS[next].name} includes ${PLANS[next].entitlements.maxMonitors}.`}
        </p>
        {billingHref ? (
          <div><Link className="btn" href={billingHref}>See plans</Link></div>
        ) : (
          <p className="muted" style={{ margin: 0 }}>Ask an owner of this organization to upgrade.</p>
        )}
      </section>
    );
  }
  return <NewMonitorForm orgSlug={ctx.orgSlug} minIntervalSec={usage.ent.minIntervalSec} billingHref={billingHref} />;
}
