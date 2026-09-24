import Link from 'next/link';
import { can } from '@/core/permissions';
import { forPage, requirePermission } from '@/lib/access';
import { listMonitors } from '@/lib/monitors';
import { searchMonitors } from '@/lib/search';

export const dynamic = 'force-dynamic';

function ago(d: Date | null) {
  if (!d) return 'never';
  const s = Math.round((Date.now() - d.getTime()) / 1000);
  if (s < 60) return `${s}s ago`;
  if (s < 3600) return `${Math.round(s / 60)}m ago`;
  return `${Math.round(s / 3600)}h ago`;
}

export default async function MonitorsPage({
  params,
  searchParams,
}: {
  params: Promise<{ orgSlug: string }>;
  searchParams: Promise<{ q?: string }>;
}) {
  const { orgSlug } = await params;
  // Lesson 1.2/1.3: signed in, a member of this org, and allowed to read monitors.
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.read'), `/${orgSlug}/monitors`);
  const q = ((await searchParams).q ?? '').trim();
  // Lesson 2.3 (🟢): with ?q=…, a fuzzy search of this org's monitors instead of the full list.
  const hits = q ? await searchMonitors(ctx, q) : null;
  const monitors = hits ? [] : await listMonitors(ctx);
  return (
    <section className="grid">
      <div className="row">
        <h1 style={{ margin: 0 }}>Monitors</h1>
        {/* Lesson 1.3: the UI hides what the role cannot do, using the same map the server enforces. */}
        {can(ctx.role, 'monitor.write') && (
          <Link className="btn" href={`/${ctx.orgSlug}/monitors/new`} style={{ marginLeft: 'auto' }}>Add monitor</Link>
        )}
      </div>
      <form className="row" role="search" action={`/${ctx.orgSlug}/monitors`}>
        <input type="search" name="q" defaultValue={q} placeholder="Search monitors by name or URL (typos welcome)" aria-label="Search monitors" style={{ flex: 1 }} />
        <button className="btn secondary">Search</button>
        {q && <Link href={`/${ctx.orgSlug}/monitors`}>Clear</Link>}
      </form>
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
      {!hits && monitors.length === 0 && (
        // TODO(6.1): a real empty state is the first step of onboarding.
        <div className="card muted">No monitors yet. Add one, then run <code>npm run checks:run</code>.</div>
      )}
      {monitors.map((m) => (
        <div className="card row" key={m.id}>
          <span className={`dot ${m.state}`} title={m.state} />
          <div style={{ flex: 1, minWidth: 200 }}>
            <Link href={`/${ctx.orgSlug}/monitors/${m.id}`}><strong>{m.name}</strong></Link>
            <div className="muted">{m.url}</div>
          </div>
          <div className="muted">every {m.intervalSeconds}s</div>
          <div className="muted">{m.uptime24h === null ? '—' : `${m.uptime24h}%`} 24h</div>
          <div className="muted">
            {m.lastLatencyMs === null ? '' : `${m.lastLatencyMs} ms · `}checked {ago(m.lastCheckedAt)}
          </div>
          {m.openIncident && <div className="error">Incident open: {m.openIncident.cause}</div>}
        </div>
      ))}
    </section>
  );
}
