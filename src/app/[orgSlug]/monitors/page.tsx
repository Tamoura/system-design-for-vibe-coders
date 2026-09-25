import Link from 'next/link';
import { can } from '@/core/permissions';
import { forPage, requirePermission } from '@/lib/access';
import { listMonitors } from '@/lib/monitors';
import { getMonitorUsage } from '@/lib/entitlements';
import { PLANS } from '@/core/plans';
import { searchMonitors } from '@/lib/search';
import { getOnboarding } from '@/lib/onboarding';
import { LiveMonitorList } from './live-monitor-list';
import { AddMonitorDialog } from './add-monitor-dialog';
import { OnboardingChecklist } from './onboarding-checklist';

export const dynamic = 'force-dynamic';

export default async function MonitorsPage({
  params,
  searchParams,
}: {
  params: Promise<{ orgSlug: string }>;
  searchParams: Promise<{ q?: string; add?: string }>;
}) {
  const { orgSlug } = await params;
  // Lesson 1.2/1.3: signed in, a member of this org, and allowed to read monitors.
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.read'), `/${orgSlug}/monitors`);
  const query = await searchParams;
  const q = (query.q ?? '').trim();
  // Lesson 2.3 (🟢): with ?q=…, a fuzzy search of this org's monitors instead of the full list.
  const hits = q ? await searchMonitors(ctx, q) : null;
  const monitors = hits ? [] : await listMonitors(ctx);
  // Lesson 3.2: where the org stands against its plan, for the hints below.
  const usage = await getMonitorUsage(ctx);
  const billingHref = can(ctx.role, 'billing.manage') ? `/${ctx.orgSlug}/billing` : null;
  const onboarding = await getOnboarding(ctx); // lesson 6.1 (🟡)
  const empty = !hits && monitors.length === 0;
  const canAdd = can(ctx.role, 'monitor.write') && !usage.atLimit;
  const addDialog = (label: string, primary = true) => (
    <AddMonitorDialog orgSlug={ctx.orgSlug} minIntervalSec={usage.ent.minIntervalSec} billingHref={billingHref} label={label} primary={primary} openInitially={query.add === '1'} />
  );
  return (
    <section className="grid">
      <OnboardingChecklist orgSlug={ctx.orgSlug} role={ctx.role} state={onboarding} />
      <div className="row">
        <h1 style={{ margin: 0 }}>Monitors</h1>
        {/* Lesson 1.3: the UI hides what the role cannot do, using the same map the server enforces. */}
        <span className="muted" data-testid="monitor-count">
          {usage.total} of {usage.ent.maxMonitors} monitors on {PLANS[usage.ent.plan].name}
        </span>
        {can(ctx.role, 'monitor.write') &&
          (usage.atLimit ? (
            // Lesson 3.2: at the limit the button becomes an upgrade prompt.
            // (The API refuses a sixth monitor anyway, with a limit_exceeded error.)
            <span style={{ marginLeft: 'auto' }} data-testid="upgrade-prompt">
              {billingHref ? (
                <Link className="btn" href={billingHref}>Upgrade to add more monitors</Link>
              ) : (
                <span className="muted">Monitor limit reached. Ask an owner to upgrade.</span>
              )}
            </span>
          ) : (
            // Lesson 6.1 (🟢): the form opens in a dialog; /monitors/new still works as a page.
            !empty && <span style={{ marginLeft: 'auto' }}>{addDialog('Add monitor')}</span>
          ))}
      </div>
      {usage.frozen > 0 && (
        // Lesson 3.2 (🟡): the freeze policy, explained where people will see it.
        <div className="card error" data-testid="frozen-banner">
          {usage.frozen} monitor{usage.frozen === 1 ? ' is' : 's are'} paused because {PLANS[usage.ent.plan].name} runs{' '}
          {usage.ent.maxMonitors} at a time. Their history is kept.{' '}
          {can(ctx.role, 'monitor.write_any') && <Link href={`/${ctx.orgSlug}/monitors/plan-limit`}>Choose which monitors run</Link>}
          {billingHref && <> or <Link href={billingHref}>upgrade</Link></>}.
        </div>
      )}
      {!empty && (
        <form className="row" role="search" action={`/${ctx.orgSlug}/monitors`}>
          <input type="search" name="q" defaultValue={q} placeholder="Search monitors by name or URL (typos welcome)" aria-label="Search monitors" style={{ flex: 1 }} />
          <button className="btn secondary">Search</button>
          {q && <Link href={`/${ctx.orgSlug}/monitors`}>Clear</Link>}
        </form>
      )}
      {hits && (
        <div className="grid" data-testid="search-results">
          <div className="muted">
            {hits.length === 0 ? `No monitors match “${q}”.` : `${hits.length} monitor${hits.length === 1 ? '' : 's'} matching “${q}”, best first:`}
          </div>
          {hits.map((h) => (
            <div className="card row" key={h.id}>
              <div style={{ flex: 1, minWidth: 200 }}>
                <Link href={`/${ctx.orgSlug}/monitors/${h.id}`}><strong>{h.name}</strong></Link>
                <div className="muted">{h.url}</div>
              </div>
              <div className="muted" title="trigram word similarity, 0–1">{h.score.toFixed(2)}</div>
            </div>
          ))}
        </div>
      )}
      {empty && (
        // Lesson 6.1 (🟢): the empty dashboard is the first screen of onboarding. It says
        // what belongs here and offers ONE obvious action.
        <div className="card empty-state" data-testid="empty-state">
          <h2 className="h2">Add your first monitor</h2>
          <p className="muted">Paste the URL of your site or API health check. Beacon checks it on a schedule and tells you the moment it goes down.</p>
          {canAdd ? addDialog('Add your first monitor') : <p className="muted">Ask an owner, admin or member of this organization to add one.</p>}
        </div>
      )}
      {/* Lesson 4.3 (🟢): tiles update live over SSE instead of polling. */}
      <LiveMonitorList
        orgSlug={ctx.orgSlug}
        renderedAt={Date.now()}
        monitors={monitors.map((m) => ({
          id: m.id,
          name: m.name,
          url: m.url,
          intervalSeconds: m.intervalSeconds,
          pausedReason: m.pausedReason,
          state: m.state,
          lastCheckedAt: m.lastCheckedAt?.toISOString() ?? null,
          lastLatencyMs: m.lastLatencyMs,
          uptime24h: m.uptime24h,
          openIncident: m.openIncident ? { cause: m.openIncident.cause } : null,
        }))}
      />
    </section>
  );
}
