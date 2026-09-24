import { listMonitors } from '@/lib/monitors';
import { overallStatus } from '@/core/incidents';

export const dynamic = 'force-dynamic';

const HEADLINE = {
  operational: 'All systems operational',
  partial_outage: 'Partial outage',
  major_outage: 'Major outage',
  unknown: 'No data yet',
} as const;

/**
 * The public status page. TODO(1.2): one page per organization, at
 * /status/[slug]. TODO(6.1): serve it on the customer's own domain.
 * TODO(4.2): let visitors subscribe to incident updates.
 */
export default async function StatusPage() {
  const monitors = (await listMonitors()).filter((m) => !m.paused);
  const status = overallStatus(monitors.map((m) => m.state));
  return (
    <section className="grid">
      <div className={`banner ${status}`}>{HEADLINE[status]}</div>
      {monitors.map((m) => (
        <div key={m.id} className="card row">
          <span className={`dot ${m.state}`} />
          <strong style={{ flex: 1 }}>{m.name}</strong>
          <span className="muted">{m.uptime24h === null ? '—' : `${m.uptime24h}% uptime (24h)`}</span>
        </div>
      ))}
    </section>
  );
}
