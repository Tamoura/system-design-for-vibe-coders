import { forPage, requirePermission } from '@/lib/access';
import { getOrganization } from '@/lib/organizations';
import { listOrgExports, orgDeletionBlockers } from '@/lib/privacy/org-data';
import { withOrg } from '@/db/tenant';
import { OTHER_RETENTION, ORG_DELETION_GRACE_DAYS, RETENTION_RULES } from '@/core/retention';
import { AutoRefresh } from '@/app/_components/auto-refresh';
import { cancelDeletionAction, requestDeletionAction, requestExportAction } from './actions';

export const dynamic = 'force-dynamic';

/**
 * Lesson 8.1: Organization → Data & privacy, for owners. The org's GDPR
 * controls (it is the controller of this data; Beacon is its processor):
 * export everything, delete everything, and how long Beacon keeps what.
 */
export default async function DataSettingsPage({ params, searchParams }: { params: Promise<{ orgSlug: string }>; searchParams: Promise<Record<string, string | undefined>> }) {
  const { orgSlug } = await params;
  const query = await searchParams;
  const ctx = await forPage(requirePermission(orgSlug, 'org.export'), `/${orgSlug}/settings/data`);
  const org = await getOrganization(ctx);
  const exports = await listOrgExports(ctx);
  const blockers = await withOrg(ctx.orgId, (tx) => orgDeletionBlockers(tx, ctx.orgId));
  return (
    <section className="grid page-narrow">
      <h1>Data &amp; privacy</h1>
      <AutoRefresh active={exports.some((e) => e.status === 'pending')} />

      <div className="card grid" id="export">
        <strong>Export all data</strong>
        <p className="muted" style={{ margin: 0 }}>
          One JSON file with the organization, its members, monitors, check results, incidents, status-page subscribers, alert settings,
          webhooks (without secrets) and the audit log. It is built in the background; the link works for {RETENTION_RULES.orgExports.days} days.
        </p>
        <form action={requestExportAction.bind(null, ctx.orgSlug)}>
          <button className="btn secondary" data-testid="request-export">Export data</button>
        </form>
        {exports.length > 0 && (
          <table data-testid="exports">
            <tbody>
              {exports.map((e) => (
                <tr key={e.id}>
                  <td>{e.createdAt.toISOString().slice(0, 16).replace('T', ' ')}</td>
                  <td>{e.status === 'ready' ? `${Math.ceil((e.sizeBytes ?? 0) / 1024)} KB` : e.status === 'failed' ? <span className="error">failed: {e.error}</span> : 'being prepared…'}</td>
                  <td>{e.status === 'ready' && e.expiresAt > new Date() && <a href={`/api/orgs/${ctx.orgSlug}/exports/${e.id}`} data-testid="download-export">Download</a>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="card grid" id="delete">
        <strong>Delete this organization</strong>
        {org?.deletionScheduledFor ? (
          <>
            <p className="error" style={{ margin: 0 }} data-testid="deletion-scheduled">
              Scheduled for deletion on {org.deletionScheduledFor.toISOString().slice(0, 16).replace('T', ' ')} UTC. Checks have stopped and the status page is offline.
            </p>
            <form action={cancelDeletionAction.bind(null, ctx.orgSlug)}>
              <button className="btn secondary">Cancel the deletion</button>
            </form>
          </>
        ) : blockers.length ? (
          <ul className="error" style={{ margin: 0 }}>{blockers.map((b) => <li key={b}>{b}</li>)}</ul>
        ) : (
          <>
            <p className="muted" style={{ margin: 0 }}>
              Checks stop at once and the status page goes offline. After {ORG_DELETION_GRACE_DAYS} days every monitor, incident, file, member
              list and audit event is deleted for good. Until then you can cancel. Export first if you want a copy.
            </p>
            <form action={requestDeletionAction.bind(null, ctx.orgSlug)} className="row">
              <label htmlFor="confirmSlug" className="muted">Type <strong>{ctx.orgSlug}</strong> to confirm</label>
              <input id="confirmSlug" name="confirmSlug" autoComplete="off" required style={{ flex: 1 }} />
              <button className="btn danger">Delete organization</button>
            </form>
          </>
        )}
        {query.delete_error && <div className="error" role="alert">{query.delete_error}</div>}
      </div>

      <div className="card grid" id="retention">
        <strong>How long Beacon keeps your data</strong>
        <table>
          <tbody>
            {Object.values(RETENTION_RULES).map((r) => (
              <tr key={r.table}><td>{r.data}</td><td>{r.days} days</td><td className="muted">{r.why}</td></tr>
            ))}
            {OTHER_RETENTION.map((r) => (
              <tr key={r.data}><td>{r.data}</td><td colSpan={2} className="muted">{r.rule}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
