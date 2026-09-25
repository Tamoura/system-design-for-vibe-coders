import Link from 'next/link';
import { listAuditForStaff } from '@/lib/admin/audit';
import { requireStaff } from '@/lib/staff';
import { isUuid } from '@/core/validation';

export const dynamic = 'force-dynamic';

const fmt = (d: Date) => d.toISOString().replace('T', ' ').slice(0, 19) + ' UTC';

/**
 * Lesson 7.3, Beacon's side: every audit event, with what customers do not
 * see (the staff member's email, the internal reason, IPs of staff). Filter
 * by org, by "staff actions only" ("which of your employees accessed our
 * data?"), or the platform's own events (staff roles, flags).
 */
export default async function StaffAuditPage({ searchParams }: { searchParams: Promise<{ org?: string; staff?: string; platform?: string; before?: string }> }) {
  await requireStaff('audit.read');
  const sp = await searchParams;
  const orgId = sp.platform ? null : sp.org && isUuid(sp.org) ? sp.org : undefined;
  const rows = await listAuditForStaff({ orgId, staffOnly: sp.staff === '1', before: sp.before ? Number(sp.before) : undefined, limit: 100 });
  return (
    <section className="grid">
      <h1>Audit log (all of Beacon)</h1>
      <p className="muted" style={{ margin: 0 }}>
        <Link href="/internal/audit">Everything</Link> · <Link href="/internal/audit?staff=1">Staff actions only</Link> · <Link href="/internal/audit?platform=1">Platform events</Link>
      </p>
      <div className="card">
        <table data-testid="staff-audit">
          <thead>
            <tr><th scope="col">When</th><th scope="col">Org</th><th scope="col">Action</th><th scope="col">Actor</th><th scope="col">Target</th><th scope="col">Changes</th><th scope="col">Reason</th><th scope="col">IP</th></tr>
          </thead>
          <tbody>
            {rows.map((e) => (
              <tr key={e.id} data-action={e.action}>
                <td>{fmt(e.occurredAt)}</td>
                <td>{e.orgSlug ? <Link href={`/internal/orgs/${e.organizationId}`}>{e.orgSlug}</Link> : <em>platform</em>}</td>
                <td><code>{e.action}</code></td>
                <td>{e.actorType}: {e.actorEmail ?? e.actorName ?? e.actorId}{e.onBehalfOfName ? ` (on behalf of ${e.onBehalfOfName})` : ''}</td>
                <td>{e.targetType} {e.targetName ?? e.targetId ?? ''}</td>
                <td><code style={{ fontSize: '.75rem' }}>{e.changes ? JSON.stringify(e.changes) : ''}</code></td>
                <td className="muted">{e.reason ?? ''}</td>
                <td className="muted">{e.ipAddress ?? ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {rows.length === 100 && (
          <p><Link href={`/internal/audit?${new URLSearchParams({ ...(sp.org && { org: sp.org }), ...(sp.staff && { staff: sp.staff }), ...(sp.platform && { platform: sp.platform }), before: String(rows[rows.length - 1].seq) })}`}>Older →</Link></p>
        )}
      </div>
    </section>
  );
}
