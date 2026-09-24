import { toMonitorDto } from '@/core/dto';
import { updateMonitorInput } from '@/core/validation';
import { requirePermission } from '@/lib/access';
import { apiRoute, notFoundResponse } from '@/lib/api';
import { deleteMonitor, getMonitor, updateMonitor } from '@/lib/monitors';

type Params = { params: Promise<{ orgSlug: string; id: string }> };

/** GET /api/orgs/:orgSlug/monitors/:id — another org's monitor id is a 404 (lesson 1.3, IDOR). */
export const GET = apiRoute(async (_req: Request, { params }: Params) => {
  const { orgSlug, id } = await params;
  const ctx = await requirePermission(orgSlug, 'monitor.read');
  const monitor = await getMonitor(ctx, id);
  return monitor ? Response.json({ data: toMonitorDto(monitor) }) : notFoundResponse();
});

/**
 * PATCH /api/orgs/:orgSlug/monitors/:id  { name?, url?, intervalSeconds?, paused? }
 * Function-level check here; the object-level and ABAC checks ("members edit
 * only their own monitors") happen in updateMonitor once the row is loaded.
 */
export const PATCH = apiRoute(async (req: Request, { params }: Params) => {
  const { orgSlug, id } = await params;
  const ctx = await requirePermission(orgSlug, 'monitor.write');
  const input = updateMonitorInput.parse(await req.json());
  return Response.json({ data: toMonitorDto(await updateMonitor(ctx, id, input)) });
});

/** DELETE /api/orgs/:orgSlug/monitors/:id — a viewer gets 403 before anything is looked up. */
export const DELETE = apiRoute(async (_req: Request, { params }: Params) => {
  const { orgSlug, id } = await params;
  const ctx = await requirePermission(orgSlug, 'monitor.write');
  await deleteMonitor(ctx, id);
  return new Response(null, { status: 204 });
});
