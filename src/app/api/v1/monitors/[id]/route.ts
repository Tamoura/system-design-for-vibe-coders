import { MonitorUpdate } from '@/core/api-schemas';
import { fromPublicId } from '@/core/ids';
import { deleteMonitor, getMonitor, updateMonitor } from '@/lib/monitors';
import { problem, publicApi, toApiMonitor } from '@/lib/public-api';

type Params = { id: string };

/** A malformed id, an unknown id and another org's id are all the same 404. */
const monitorId = (id: string) => fromPublicId('monitor', id);

/** GET /api/v1/monitors/:id */
export const GET = publicApi<Params>('monitors:read', async (req, api, { id }) => {
  const uuid = monitorId(id);
  const monitor = uuid ? await getMonitor(api, uuid) : null;
  return monitor ? Response.json(toApiMonitor(monitor)) : problem('not-found', { instance: new URL(req.url).pathname });
});

/** PATCH /api/v1/monitors/:id  { name?, url?, interval_seconds?, paused? } */
export const PATCH = publicApi<Params>('monitors:write', async (req, api, { id }) => {
  const uuid = monitorId(id);
  if (!uuid) return problem('not-found', { instance: new URL(req.url).pathname });
  const input = MonitorUpdate.parse(await req.json());
  const monitor = await updateMonitor({ orgId: api.orgId, ...api.actor, audit: api.audit }, uuid, {
    name: input.name,
    url: input.url,
    intervalSeconds: input.interval_seconds,
    paused: input.paused,
  });
  return Response.json(toApiMonitor(monitor));
});

/** DELETE /api/v1/monitors/:id */
export const DELETE = publicApi<Params>('monitors:write', async (req, api, { id }) => {
  const uuid = monitorId(id);
  if (!uuid) return problem('not-found', { instance: new URL(req.url).pathname });
  await deleteMonitor({ orgId: api.orgId, ...api.actor, audit: api.audit }, uuid);
  return new Response(null, { status: 204 });
});
