import Link from 'next/link';
import { can } from '@/core/permissions';
import { PLANS } from '@/core/plans';
import { forPage, requirePermission } from '@/lib/access';
import { getEntitlements, listPlanLimitedMonitors } from '@/lib/entitlements';
import { chooseRunningAction } from './actions';

export const dynamic = 'force-dynamic';

/**
 * Lesson 3.2 (🟡): after a downgrade froze some monitors, choose which ones
 * run. Owners and admins ("monitor.write_any": it switches everyone's
 * monitors on and off). Monitors paused by hand are not listed; they stay off.
 */
export default async function PlanLimitPage({
  params,
  searchParams,
}: {
  params: Promise<{ orgSlug: string }>;
  searchParams: Promise<{ error?: string }>;
}) {
  const { orgSlug } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.write_any'), `/${orgSlug}/monitors/plan-limit`);
  const { error } = await searchParams;
  const [ent, monitors] = await Promise.all([getEntitlements(ctx), listPlanLimitedMonitors(ctx)]);
  return (
    <section className="grid" style={{ maxWidth: 640 }}>
      <h1 style={{ margin: 0 }}>Choose which monitors run</h1>
      <p className="muted" style={{ margin: 0 }}>
        {PLANS[ent.plan].name} runs up to {ent.maxMonitors} monitors at a time. The others stay paused, with all their history,
        until you pick them here or upgrade{can(ctx.role, 'billing.manage') && <> (<Link href={`/${ctx.orgSlug}/billing`}>see plans</Link>)</>}.
      </p>
      {error === 'too_many' && <div className="card error">Pick at most {ent.maxMonitors}.</div>}
      <form action={chooseRunningAction.bind(null, ctx.orgSlug)} className="card grid">
        {monitors.map((m) => (
          <label key={m.id} className="row">
            <input type="checkbox" name="keep" value={m.id} defaultChecked={m.pausedReason === null} />
            <span>
              <strong>{m.name}</strong> <span className="muted">{m.url}</span>
            </span>
          </label>
        ))}
        <div><button className="btn">Save</button></div>
      </form>
    </section>
  );
}
