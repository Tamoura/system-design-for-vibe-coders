import Link from 'next/link';
import { forPage, requirePermission } from '@/lib/access';
import { listRecentIncidents } from '@/lib/incidents';
import { LocalTime } from '@/app/_components/local-time';

export const dynamic = 'force-dynamic';

/** Lesson 6.1: the Incidents section: every monitor's incidents in one list, open ones first. */
export default async function IncidentsPage({ params }: { params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.read'), `/${orgSlug}/incidents`);
  const rows = await listRecentIncidents(ctx);
  return (
    <section className="grid">
      <h1>Incidents</h1>
      {rows.length === 0 ? (
        // Lesson 6.1: an empty state says what will appear here and why that is good news.
        <div className="card empty-state">
          <h2 className="h2">No incidents</h2>
          <p className="muted">When a monitor fails three checks in a row, Beacon opens an incident here and alerts your team.</p>
          <Link href={`/${ctx.orgSlug}/monitors`}>Go to your monitors →</Link>
        </div>
      ) : (
        <div className="card">
          <table>
            <caption className="sr-only">Incidents, open first</caption>
            <thead>
              <tr><th scope="col">Status</th><th scope="col">Monitor</th><th scope="col">Cause</th><th scope="col">Opened</th></tr>
            </thead>
            <tbody>
              {rows.map((i) => (
                <tr key={i.id}>
                  <td>
                    {i.resolvedAt ? <span className="badge">Resolved</span> : <span className="badge status-down">Open{i.acknowledgedAt ? ', acknowledged' : ''}</span>}
                  </td>
                  <td><Link href={`/${ctx.orgSlug}/monitors/${i.monitorId}#incident-${i.id}`}>{i.monitorName}</Link></td>
                  <td>{i.cause}</td>
                  <td><LocalTime iso={i.openedAt.toISOString()} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
