import { notFound } from 'next/navigation';
import { listMonitors } from '@/lib/monitors';
import { findPublicStatusPage } from '@/lib/organizations';
import { overallStatus } from '@/core/incidents';

export const dynamic = 'force-dynamic';

const HEADLINE = {
  operational: 'All systems operational',
  partial_outage: 'Partial outage',
  major_outage: 'Major outage',
  unknown: 'No data yet',
} as const;

/**
 * The public status page, one per organization (lesson 1.2). No login needed,
 * but it only ever shows the monitors of the org named in the URL.
 * TODO(6.1): serve it on the customer's own domain.
 * TODO(4.2): let visitors subscribe to incident updates.
 */
export default async function StatusPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const org = await findPublicStatusPage(slug);
  if (!org) notFound();
  const monitors = (await listMonitors({ orgId: org.id })).filter((m) => !m.paused);
  const status = overallStatus(monitors.map((m) => m.state));
  return (
    <section className="grid">
      <h1 style={{ margin: 0 }}>{org.name} status</h1>
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
