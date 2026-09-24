import { toMonitorDto } from '@/core/dto';
import { requirePermission } from '@/lib/access';
import { apiRoute, notFoundResponse } from '@/lib/api';
import { deleteMonitor, getMonitor } from '@/lib/monitors';

type Params = { params: Promise<{ orgSlug: string; id: string }> };

/** GET /api/orgs/:orgSlug/monitors/:id — another org's monitor id is a 404 (lesson 1.3, IDOR). */
export const GET = apiRoute(async (_req: Request, { params }: Params) => {
  const { orgSlug, id } = await params;
  const ctx = await requirePermission(orgSlug, 'monitor.read');
  const monitor = await getMonitor(ctx, id);
  return monitor ? Response.json({ data: toMonitorDto(monitor) }) : notFoundResponse();
});

/** DELETE /api/orgs/:orgSlug/monitors/:id — a viewer gets 403 before anything is looked up. */
export const DELETE = apiRoute(async (_req: Request, { params }: Params) => {
  const { orgSlug, id } = await params;
  const ctx = await requirePermission(orgSlug, 'monitor.write');
  return (await deleteMonitor(ctx, id)) ? new Response(null, { status: 204 }) : notFoundResponse();
});
