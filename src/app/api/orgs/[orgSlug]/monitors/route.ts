import { toMonitorDto } from '@/core/dto';
import { createMonitorInput } from '@/core/validation';
import { requirePermission } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { createMonitor, listMonitorRows } from '@/lib/monitors';

/*
 * JSON endpoints for monitors, authenticated by the same session cookie as the
 * UI. Lesson 1.3: each handler starts with requirePermission(), and the org it
 * returns (not anything in the body) scopes the query.
 * These are the dashboard's own endpoints. The PUBLIC API (lesson 5.2) is a
 * separate, versioned surface with API keys: src/app/api/v1.
 */

type Params = { params: Promise<{ orgSlug: string }> };

/** GET /api/orgs/:orgSlug/monitors */
export const GET = apiRoute(async (_req: Request, { params }: Params) => {
  const { orgSlug } = await params;
  const ctx = await requirePermission(orgSlug, 'monitor.read');
  const rows = await listMonitorRows(ctx);
  return Response.json({ data: rows.map(toMonitorDto) });
});

/** POST /api/orgs/:orgSlug/monitors  { name, url, intervalSeconds } */
export const POST = apiRoute(async (req: Request, { params }: Params) => {
  const { orgSlug } = await params;
  const ctx = await requirePermission(orgSlug, 'monitor.write');
  // Allow-list parse: unknown keys such as organizationId or createdBy are dropped.
  const input = createMonitorInput.parse(await req.json());
  const monitor = await createMonitor(ctx, input);
  return Response.json({ data: toMonitorDto(monitor) }, { status: 201 });
});
