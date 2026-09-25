import Link from 'next/link';
import { AUDIT_CATEGORIES } from '@/core/audit';
import { can } from '@/core/permissions';
import { cheapestPlanWhere, PLANS } from '@/core/plans';
import { forPage, requirePermission } from '@/lib/access';
import { AUDIT_TARGET_TYPES, listAuditEvents, parseAuditQuery, toCustomerView, type CustomerAuditEvent } from '@/lib/audit';
import { getEntitlements } from '@/lib/entitlements';
import { listMembers } from '@/lib/members';

export const dynamic = 'force-dynamic';

const fmt = (d: Date) => d.toISOString().replace('T', ' ').slice(0, 19) + ' UTC';
const show = (v: unknown) => (v === null || v === undefined ? '—' : typeof v === 'string' ? v : JSON.stringify(v));

/**
 * Lesson 7.3 (🟡): the customer-facing audit log. Owners and admins only
 * ("audit.read": a member gets 403, here and from the API behind it), on a
 * plan with the audit log (Pro: 30 days, Business: a year; Free sees what it
 * would get). Filters combine (actor, category, target, dates) and pages go
 * backwards with a cursor; each row opens to its context and before/after
 * values; "Export CSV" downloads exactly the current filter.
 */
export default async function AuditLogPage({ params, searchParams }: { params: Promise<{ orgSlug: string }>; searchParams: Promise<Record<string, string | undefined>> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'audit.read'), `/${orgSlug}/settings/audit-log`);
  const ent = await getEntitlements(ctx);

  if (!ent.auditLog) {
    const upgradeTo = cheapestPlanWhere((e) => e.auditLog);
    return (
      <section className="grid" style={{ maxWidth: 760 }}>
        <h1 style={{ margin: 0 }}>Audit log</h1>
        <div className="card grid" data-testid="audit-upsell">
          <strong>Who did what, when, and from where.</strong>
          <p style={{ margin: 0 }}>
            Every change to members, monitors, API keys, webhooks, alerting and billing, with the person, their IP address and the before/after values,
            filterable and exportable as CSV. The audit log is part of the {upgradeTo ? PLANS[upgradeTo].name : 'higher'} plan ({PLANS.pro.entitlements.auditLogRetentionDays} days of history)
            and Business ({PLANS.business.entitlements.auditLogRetentionDays} days).
          </p>
          {can(ctx.role, 'billing.manage') && <div><Link className="btn" href={`/${ctx.orgSlug}/billing`}>Upgrade</Link></div>}
        </div>
      </section>
    );
  }

  const query = new URLSearchParams(Object.entries(await searchParams).filter((e): e is [string, string] => typeof e[1] === 'string' && e[1] !== ''));
  const { filters, before } = parseAuditQuery(query);
  const [page, members] = await Promise.all([listAuditEvents(ctx.orgId, filters, { retentionDays: ent.auditLogRetentionDays, before }), listMembers(ctx)]);
  const events = page.rows.map(toCustomerView);
  const filterQuery = new URLSearchParams(query);
  filterQuery.delete('before');
  const exportHref = `/api/orgs/${ctx.orgSlug}/audit-log?${new URLSearchParams([...filterQuery, ['format', 'csv']])}`;
  const olderHref = page.nextBefore ? `?${new URLSearchParams([...filterQuery, ['before', String(page.nextBefore)]])}` : null;

  return (
    <section className="grid">
      <div className="row">
        <h1 style={{ margin: 0 }}>Audit log</h1>
        <span className="badge">last {ent.auditLogRetentionDays} days on {PLANS[ent.plan].name}</span>
        <a className="btn secondary" href={exportHref} data-testid="audit-export" style={{ marginLeft: 'auto' }} download>Export CSV</a>
      </div>

      <form className="card row" data-testid="audit-filters" action={`/${ctx.orgSlug}/settings/audit-log`}>
        <label className="grid" style={{ gap: '.2rem' }}>
          <span className="muted">Actor</span>
          <select name="actor" defaultValue={filters.actor ?? ''}>
            <option value="">Anyone</option>
            {members.map((m) => <option key={m.userId} value={m.userId}>{m.name}</option>)}
            <option value="api_key">An API key</option>
            <option value="staff">Beacon support</option>
          </select>
        </label>
        <label className="grid" style={{ gap: '.2rem' }}>
          <span className="muted">Category</span>
          <select name="category" defaultValue={filters.category ?? ''}>
            <option value="">All</option>
            {AUDIT_CATEGORIES.filter((c) => c !== 'platform').map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
        </label>
        <label className="grid" style={{ gap: '.2rem' }}>
          <span className="muted">Target</span>
          <select name="target_type" defaultValue={filters.targetType ?? ''}>
            <option value="">Any</option>
            {AUDIT_TARGET_TYPES.map((t) => <option key={t} value={t}>{t.replace('_', ' ')}</option>)}
          </select>
        </label>
        {filters.targetId && <input type="hidden" name="target_id" value={filters.targetId} />}
        <label className="grid" style={{ gap: '.2rem' }}>
          <span className="muted">From</span>
          <input type="date" name="from" defaultValue={query.get('from') ?? ''} />
        </label>
        <label className="grid" style={{ gap: '.2rem' }}>
          <span className="muted">To</span>
          <input type="date" name="to" defaultValue={query.get('to') ?? ''} />
        </label>
        <button className="btn">Filter</button>
        <Link href={`/${ctx.orgSlug}/settings/audit-log`}>Clear</Link>
      </form>

      <div className="card">
        {events.length === 0 ? (
          <p className="muted" data-testid="audit-empty">No events match.</p>
        ) : (
          <table data-testid="audit-table">
            <thead>
              <tr><th scope="col">When</th><th scope="col">Actor</th><th scope="col">Action</th><th scope="col">Target</th><th scope="col">Details</th></tr>
            </thead>
            <tbody>
              {events.map((e) => <Row key={e.id} e={e} orgSlug={ctx.orgSlug} />)}
            </tbody>
          </table>
        )}
        {olderHref && <p><Link href={olderHref} data-testid="audit-older">Older events →</Link></p>}
      </div>
    </section>
  );
}

function Row({ e, orgSlug }: { e: CustomerAuditEvent; orgSlug: string }) {
  return (
    <tr data-action={e.action} data-testid="audit-row">
      <td style={{ whiteSpace: 'nowrap' }}>{fmt(e.occurredAt)}</td>
      <td data-testid="audit-actor">{e.actor}</td>
      <td><code>{e.action}</code><div className="muted">{e.description}</div></td>
      <td>
        {e.targetType ? (
          <>
            {e.targetType.replace('_', ' ')} {e.targetName && <strong>{e.targetName}</strong>}
            {e.targetId && (
              <div><Link className="muted" href={`/${orgSlug}/settings/audit-log?target_type=${e.targetType}&target_id=${encodeURIComponent(e.targetId)}`}>history of this {e.targetType.replace('_', ' ')}</Link></div>
            )}
          </>
        ) : '—'}
      </td>
      <td>
        <details>
          <summary>Details</summary>
          {e.changes && Object.keys(e.changes).length > 0 && (
            <table data-testid="audit-diff">
              <thead><tr><th scope="col">Field</th><th scope="col">Before</th><th scope="col">After</th></tr></thead>
              <tbody>
                {Object.entries(e.changes).map(([field, c]) => (
                  <tr key={field}><td><code>{field}</code></td><td>{show(c.before)}</td><td>{show(c.after)}</td></tr>
                ))}
              </tbody>
            </table>
          )}
          {e.metadata && <div className="muted">{Object.entries(e.metadata).map(([k, v]) => `${k}: ${show(v)}`).join(' · ')}</div>}
          <div className="muted">
            {e.via && <>via {e.via} · </>}IP {e.ipAddress ?? '—'} · {e.userAgent ?? 'no user agent'} · request {e.requestId ?? '—'}
          </div>
        </details>
      </td>
    </tr>
  );
}
