import Link from 'next/link';
import { forPage, requireMembership } from '@/lib/access';
import { listMonitors } from '@/lib/monitors';

export const dynamic = 'force-dynamic';

function ago(d: Date | null) {
  if (!d) return 'never';
  const s = Math.round((Date.now() - d.getTime()) / 1000);
  if (s < 60) return `${s}s ago`;
  if (s < 3600) return `${Math.round(s / 60)}m ago`;
  return `${Math.round(s / 3600)}h ago`;
}

export default async function MonitorsPage({ params }: { params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  // Lesson 1.2: signed in *and* a member of this org, or no page at all.
  const ctx = await forPage(requireMembership(orgSlug), `/${orgSlug}/monitors`);
  const monitors = await listMonitors(ctx);
  return (
    <section className="grid">
      <div className="row">
        <h1 style={{ margin: 0 }}>Monitors</h1>
        <Link className="btn" href={`/${ctx.orgSlug}/monitors/new`} style={{ marginLeft: 'auto' }}>Add monitor</Link>
      </div>
      {monitors.length === 0 && (
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
