import { notFound } from 'next/navigation';
import { can, canEditMonitor } from '@/core/permissions';
import { forPage, requirePermission } from '@/lib/access';
import { getMonitor, getMonitorHistory } from '@/lib/monitors';
import { getEntitlements } from '@/lib/entitlements';
import { listIncidentScreenshots } from '@/lib/files';
import { listIncidentUpdates } from '@/lib/incidents';
import { AutoRefresh } from '@/app/_components/auto-refresh';
import { FileUploader } from '@/app/_components/file-uploader';
import { addIncidentUpdateAction, deleteMonitorAction, resolveIncidentAction } from './actions';
import { EditMonitorForm } from './edit-form';
import { LiveRefresh, Presence } from './live';

export const dynamic = 'force-dynamic';

export default async function MonitorPage({ params }: { params: Promise<{ orgSlug: string; id: string }> }) {
  const { orgSlug, id } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'monitor.read'), `/${orgSlug}/monitors/${id}`);
  // Lesson 1.3: fetched by id *and* org. Another org's monitor id is a 404 here.
  const monitor = await getMonitor(ctx, id);
  if (!monitor) notFound();
  const history = await getMonitorHistory(ctx, monitor.id);
  // Lesson 2.2 (🟡): incident screenshots, private to the org's members.
  const screenshots = await listIncidentScreenshots(ctx, history.incidents.map((i) => i.id));
  // Lesson 2.3 (🟡): the updates that full-text search indexes.
  const updates = await listIncidentUpdates(ctx, history.incidents.map((i) => i.id));
  const canWriteIncidents = can(ctx.role, 'incident.write');
  // Lesson 1.3 (🟡): the same ABAC rule the server enforces decides what to show.
  const editable = canEditMonitor(ctx, monitor);
  const ent = await getEntitlements(ctx); // lesson 3.2: for the interval picker's hints
  return (
    <section className="grid">
      <div className="row">
        <h1 style={{ margin: 0 }}>{monitor.name}</h1>
        {/* Lesson 4.3 (🟡): who else has this page open, and live updates for it. */}
        <Presence orgSlug={ctx.orgSlug} topic={`monitor:${monitor.id}`} me={ctx.userId} />
        <LiveRefresh monitorId={monitor.id} />
      </div>
      <div className="card grid">
        <div><span className="muted">URL</span> {monitor.url}</div>
        <div>
          <span className="muted">Checked every</span> {monitor.intervalSeconds}s
          {monitor.pausedReason === 'manual' && ' (paused)'}
          {/* Lesson 3.2 (🟡): frozen by a downgrade, not by a person. */}
          {monitor.pausedReason === 'plan_limit' && (
            <span className="error"> (paused: over the plan’s monitor limit, <a href={`/${ctx.orgSlug}/monitors/plan-limit`}>choose which run</a>)</span>
          )}
        </div>
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
          minIntervalSec={ent.minIntervalSec}
          billingHref={can(ctx.role, 'billing.manage') ? `/${ctx.orgSlug}/billing` : null}
        />
      )}
      <AutoRefresh active={screenshots.some((f) => f.status === 'processing')} />
      <h2 style={{ margin: 0, fontSize: '1.1rem' }}>Incidents</h2>
      <div className="card">
        {history.incidents.length === 0 ? (
          <span className="muted">No incidents.</span>
        ) : (
          <table>
            <tbody>
              {history.incidents.map((i) => (
                <tr key={i.id} id={`incident-${i.id}`}>
                  <td>{i.openedAt.toISOString().slice(0, 16).replace('T', ' ')}</td>
                  <td>
                    {i.cause}
                    <ul className="updates">
                      {updates
                        .filter((u) => u.incidentId === i.id)
                        .map((u) => (
                          <li key={u.id}>
                            <span className="muted">
                              {u.createdAt.toISOString().slice(11, 16)} {u.authorName ?? 'Beacon'}:
                            </span>{' '}
                            {u.body}
                          </li>
                        ))}
                    </ul>
                    {canWriteIncidents && (
                      <form action={addIncidentUpdateAction.bind(null, ctx.orgSlug, monitor.id, i.id)} className="row" style={{ gap: '.4rem' }}>
                        <input name="body" placeholder="Post an update…" required maxLength={5000} style={{ flex: 1 }} />
                        <button className="btn secondary">Post</button>
                      </form>
                    )}
                  </td>
                  <td>
                    {i.resolvedAt ? 'resolved' : <span className="error">open</span>}
                    {!i.resolvedAt && canWriteIncidents && (
                      <form action={resolveIncidentAction.bind(null, ctx.orgSlug, monitor.id, i.id)} style={{ display: 'inline', marginLeft: '.6rem' }}>
                        <button className="link-btn">Mark resolved</button>
                      </form>
                    )}
                  </td>
                  <td>
                    <div className="row" style={{ gap: '.4rem' }}>
                      {screenshots
                        .filter((f) => f.incidentId === i.id)
                        .map((f) =>
                          f.status === 'ready' ? (
                            <a key={f.id} href={`/api/orgs/${ctx.orgSlug}/files/${f.id}`} title={f.originalName}>
                              <img src={`/api/orgs/${ctx.orgSlug}/files/${f.id}?variant=thumbnail`} alt={f.originalName} className="thumb" />
                            </a>
                          ) : (
                            <span key={f.id} className={f.status === 'rejected' ? 'error' : 'badge'} title={f.rejectionReason ?? undefined}>
                              {f.status === 'rejected' ? `${f.originalName}: rejected` : `${f.originalName}: ${f.status}…`}
                            </span>
                          ),
                        )}
                    </div>
                    {canWriteIncidents && (
                      <FileUploader
                        requestUrl={`/api/orgs/${ctx.orgSlug}/incidents/${i.id}/screenshots`}
                        orgSlug={ctx.orgSlug}
                        label="Add screenshot:"
                      />
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
