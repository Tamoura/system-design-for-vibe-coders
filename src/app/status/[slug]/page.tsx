import { notFound } from 'next/navigation';
import { listMonitors } from '@/lib/monitors';
import { findPublicStatusPage } from '@/lib/organizations';
import { overallStatus } from '@/core/incidents';
import { SubscribeForm } from './subscribe-form';
import { listPublishedSummaries } from '@/lib/ai/incident-summary';

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
 * Serving it on the customer's own domain (status.acme.com: CNAME, TXT
 * verification, host-based routing, on-demand TLS) is lesson 6.1's 🔴
 * exercise, not built; docs/SOLUTIONS.md (Module 6) describes the design.
 * Lesson 4.2 (🟡): visitors subscribe to incident updates (double opt-in).
 */
export default async function StatusPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const org = await findPublicStatusPage(slug);
  if (!org) notFound();
  const monitors = (await listMonitors({ orgId: org.id })).filter((m) => !m.paused);
  const status = overallStatus(monitors.map((m) => m.state));
  // Lesson 8.2: incident updates a PERSON published (an AI draft is never shown here until then).
  const updates = await listPublishedSummaries(org.id);
  return (
    <section className="grid">
      <div className="row">
        {/* Lesson 2.2: the logo is served through /status/[slug]/logo, a redirect to a short-lived signed URL. */}
        {org.logoFileId && (
          <img src={`/status/${slug}/logo`} alt={`${org.name} logo`} className="logo" data-testid="status-logo" />
        )}
        <h1 style={{ margin: 0 }}>{org.name} status</h1>
      </div>
      <div className={`banner ${status}`}>{HEADLINE[status]}</div>
      {monitors.map((m) => (
        <div key={m.id} className="card row">
          {/* Lesson 6.1 (a11y): a word next to the dot, never colour alone. */}
          <span className={`dot ${m.state}`} aria-hidden="true" />
          <strong style={{ flex: 1 }}>{m.name}</strong>
          <span className={`state-label ${m.state}`}>{m.state === 'up' ? 'Operational' : m.state === 'down' ? 'Down' : 'No data'}</span>
          <span className="muted">{m.uptime24h === null ? '—' : `${m.uptime24h}% uptime (24h)`}</span>
        </div>
      ))}
      {updates.length > 0 && (
        <section className="grid" aria-labelledby="past-incidents" data-testid="incident-updates">
          <h2 id="past-incidents" style={{ margin: 0, fontSize: '1.1rem' }}>Recent incidents</h2>
          {updates.map((u) => (
            <article key={`${u.publishedAt?.toISOString()}-${u.headline}`} className="card grid" style={{ gap: '.3rem' }}>
              {/* Text, never HTML: React escapes it (lesson 8.1: output encoding + the CSP). */}
              <strong>{u.headline}</strong>
              <p style={{ margin: 0 }}>{u.body}</p>
              <span className="muted">
                {u.openedAt.toISOString().slice(0, 16).replace('T', ' ')} UTC{u.resolvedAt ? ` – ${u.resolvedAt.toISOString().slice(11, 16)} UTC` : ' · ongoing'}
              </span>
            </article>
          ))}
        </section>
      )}
      <div className="card">
        <SubscribeForm slug={slug} />
      </div>
    </section>
  );
}
