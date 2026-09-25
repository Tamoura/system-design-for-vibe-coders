import { EVENT_NAMES, TRACKING_PLAN } from '@/core/tracking-plan';
import { activationFunnel, recentEvents } from '@/lib/analytics/funnel';
import { requireStaff } from '@/lib/staff';

export const dynamic = 'force-dynamic';

const pct = (n: number, of: number) => (of === 0 ? '—' : `${Math.round((n / of) * 100)}%`);

/**
 * Lesson 6.2 (🟡): Beacon's activation funnel, per ORGANIZATION and by plan,
 * from the server-side events in Postgres. With PostHog configured the same
 * funnel is a PostHog insight with a breakdown on the "organization" group's
 * plan; this page is what you have with Postgres alone.
 */
export default async function AnalyticsPage({ searchParams }: { searchParams: Promise<{ days?: string }> }) {
  await requireStaff();
  const days = Math.min(Math.max(Number((await searchParams).days) || 30, 1), 365);
  const since = new Date(Date.now() - days * 24 * 3600 * 1000);
  const [funnel, recent] = await Promise.all([activationFunnel({ since }), recentEvents(25)]);
  return (
    <section className="grid">
      <h1>Activation funnel</h1>
      <p className="muted" style={{ margin: 0 }}>
        Organizations created in the last {days} days (<a href="?days=7">7</a> · <a href="?days=30">30</a> · <a href="?days=90">90</a>).
        Activated = first check result within 24 hours of the org being created.
      </p>
      <div className="card">
        <table data-testid="funnel">
          <caption className="sr-only">Activation funnel by plan</caption>
          <thead>
            <tr>
              <th scope="col">Plan today</th><th scope="col">org_created</th><th scope="col">monitor_created</th>
              <th scope="col">first check</th><th scope="col">activated (≤ 24 h)</th><th scope="col">median time to activation</th>
            </tr>
          </thead>
          <tbody>
            {funnel.map((r) => (
              <tr key={r.plan} data-plan={r.plan} style={r.isTotal ? { fontWeight: 700 } : undefined}>
                <th scope="row">{r.plan}</th>
                <td>{r.orgs}</td>
                <td>{r.withMonitor} <span className="muted">({pct(r.withMonitor, r.orgs)})</span></td>
                <td>{r.withCheck} <span className="muted">({pct(r.withCheck, r.orgs)})</span></td>
                <td>{r.activated} <span className="muted">({pct(r.activated, r.orgs)})</span></td>
                <td>{r.medianMinutesToActivation === null ? '—' : `${r.medianMinutesToActivation} min`}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <h2>Latest events</h2>
      <div className="card">
        <table data-testid="recent-events">
          <thead><tr><th scope="col">When (UTC)</th><th scope="col">Event</th><th scope="col">Org</th><th scope="col">Plan</th><th scope="col">Properties</th></tr></thead>
          <tbody>
            {recent.map((e, i) => (
              <tr key={i}>
                <td>{e.occurredAt.toISOString().slice(0, 19).replace('T', ' ')}</td>
                <td><code>{e.event}</code></td>
                <td>{e.orgSlug}</td>
                <td>{e.orgPlan}</td>
                <td><code>{JSON.stringify(e.properties)}</code></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <h2>The tracking plan</h2>
      <div className="card">
        <table>
          <thead><tr><th scope="col">Event</th><th scope="col">Sent by</th><th scope="col">Question</th><th scope="col">Why</th></tr></thead>
          <tbody>
            {EVENT_NAMES.map((name) => (
              <tr key={name}>
                <td><code>{name}</code></td>
                <td>{TRACKING_PLAN[name].source}</td>
                <td>{TRACKING_PLAN[name].question}</td>
                <td>{TRACKING_PLAN[name].why}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
