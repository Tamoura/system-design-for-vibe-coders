import { notFound } from 'next/navigation';
import { can, canEditMonitor } from '@/core/permissions';
import { forPage, requirePermission } from '@/lib/access';
import { getMonitor, getMonitorHistory } from '@/lib/monitors';
import { deleteMonitorAction, resolveIncidentAction } from './actions';
import { EditMonitorForm } from './edit-form';

export const dynamic = 'force-dynamic';

export default async function MonitorPage({ params }: { params: Promise<{ orgSlug: string; id: string }> }) {
  const { orgSlug, id } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.read'), `/${orgSlug}/monitors/${id}`);
  // Lesson 1.3: fetched by id *and* org. Another org's monitor id is a 404 here.
  const monitor = await getMonitor(ctx, id);
  if (!monitor) notFound();
  const history = await getMonitorHistory(ctx, monitor.id);
  // Lesson 1.3 (🟡): the same ABAC rule the server enforces decides what to show.
  const editable = canEditMonitor(ctx, monitor);
  return (
    <section className="grid">
      <h1 style={{ margin: 0 }}>{monitor.name}</h1>
      <div className="card grid">
        <div><span className="muted">URL</span> {monitor.url}</div>
        <div><span className="muted">Checked every</span> {monitor.intervalSeconds}s{monitor.paused ? ' (paused)' : ''}</div>
        {/* Lesson 1.3: hidden when the rules say no; the actions check again on the server. */}
        {editable && (
          <form action={deleteMonitorAction.bind(null, ctx.orgSlug, monitor.id)}>
            <button className="btn secondary">Delete monitor</button>
          </form>
        )}
      </div>
      {editable && (
        <EditMonitorForm
          orgSlug={ctx.orgSlug}
          monitor={{ id: monitor.id, name: monitor.name, url: monitor.url, intervalSeconds: monitor.intervalSeconds, paused: monitor.paused }}
        />
      )}
      <h2 style={{ margin: 0, fontSize: '1.1rem' }}>Incidents</h2>
      <div className="card">
        {history.incidents.length === 0 ? (
          <span className="muted">No incidents.</span>
        ) : (
          <table>
            <tbody>
              {history.incidents.map((i) => (
                <tr key={i.id}>
                  <td>{i.openedAt.toISOString().slice(0, 16).replace('T', ' ')}</td>
                  <td>{i.cause}</td>
                  <td>
                    {i.resolvedAt ? 'resolved' : <span className="error">open</span>}
                    {!i.resolvedAt && can(ctx.role, 'incident.write') && (
                      <form action={resolveIncidentAction.bind(null, ctx.orgSlug, monitor.id, i.id)} style={{ display: 'inline', marginLeft: '.6rem' }}>
                        <button className="link-btn">Mark resolved</button>
                      </form>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
      <h2 style={{ margin: 0, fontSize: '1.1rem' }}>Latest checks</h2>
      <div className="card">
        {history.checks.length === 0 ? (
          <span className="muted">Not checked yet. Run <code>npm run checks:run</code>.</span>
        ) : (
          <table>
            <tbody>
              {history.checks.map((c) => (
                <tr key={c.id}>
                  <td><span className={`dot ${c.ok ? 'up' : 'down'}`} style={{ display: 'inline-block' }} /></td>
                  <td>{c.checkedAt.toISOString().slice(0, 19).replace('T', ' ')}</td>
                  <td>{c.statusCode ?? c.error}</td>
                  <td>{c.latencyMs === null ? '' : `${c.latencyMs} ms`}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}
