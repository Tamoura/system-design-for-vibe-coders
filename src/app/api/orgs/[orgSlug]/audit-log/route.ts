import { requirePermission } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { AUDIT_EXPORT_MAX_ROWS, CSV_HEADER, listAuditEvents, parseAuditQuery, toCsvLine, toCustomerView } from '@/lib/audit';
import { assertAuditLogAccess } from '@/lib/audit-access';

type Params = { params: Promise<{ orgSlug: string }> };

/**
 * GET /api/orgs/:orgSlug/audit-log?actor=&category=&target_type=&target_id=&from=YYYY-MM-DD&to=YYYY-MM-DD&before=
 * GET …&format=csv   the same filters, as a CSV file (lesson 7.3 🟡: "export for the current filter")
 *
 * 404 not a member · 403 not an owner/admin ("audit.read") · 402 the plan has
 * no audit log. The org comes from the URL + membership, and every query runs
 * inside withOrg(): an org can only ever read its own events.
 */
export const GET = apiRoute(async (req: Request, { params }: Params) => {
  const { orgSlug } = await params;
  const ctx = await requirePermission(orgSlug, 'audit.read');
  const { retentionDays } = await assertAuditLogAccess(ctx);
  const url = new URL(req.url);
  const { filters, before } = parseAuditQuery(url.searchParams);

  if (url.searchParams.get('format') === 'csv') {
    const lines = [CSV_HEADER.join(',')];
    let cursor = before;
    while (lines.length <= AUDIT_EXPORT_MAX_ROWS) {
      const page = await listAuditEvents(ctx.orgId, filters, { retentionDays, before: cursor, limit: 1000 });
      for (const e of page.rows) lines.push(toCsvLine(toCustomerView(e)));
      if (page.nextBefore === null) break;
      cursor = page.nextBefore;
    }
    const file = `beacon-audit-${ctx.orgSlug}-${new Date().toISOString().slice(0, 10)}.csv`;
    return new Response(lines.slice(0, AUDIT_EXPORT_MAX_ROWS + 1).join('\r\n') + '\r\n', {
      headers: { 'content-type': 'text/csv; charset=utf-8', 'content-disposition': `attachment; filename="${file}"`, 'cache-control': 'no-store' },
    });
  }

  const page = await listAuditEvents(ctx.orgId, filters, { retentionDays, before });
  return Response.json({ data: page.rows.map(toCustomerView), next_before: page.nextBefore, retention_days: retentionDays });
});
