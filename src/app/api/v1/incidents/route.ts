import { incidentListParams } from '@/core/api-schemas';
import { fromPublicId } from '@/core/ids';
import { listIncidentsPage } from '@/lib/incidents';
import { page, problem, publicApi, toApiIncident } from '@/lib/public-api';

/** GET /api/v1/incidents?status=open&monitor_id=mon_…&limit=20&starting_after=inc_… */
export const GET = publicApi('incidents:read', async (req, api) => {
  const instance = '/api/v1/incidents';
  const query = incidentListParams.safeParse(Object.fromEntries(new URL(req.url).searchParams));
  if (!query.success) return problem('invalid-parameter', { detail: 'limit must be 1 to 100; status open or resolved.', instance });
  const { starting_after, monitor_id } = query.data;
  const startingAfter = starting_after === undefined ? undefined : fromPublicId('incident', starting_after);
  const monitorId = monitor_id === undefined ? undefined : fromPublicId('monitor', monitor_id);
  if (startingAfter === null || monitorId === null) return problem('invalid-parameter', { detail: 'starting_after must be an incident id (inc_…), monitor_id a monitor id (mon_…).', instance });
  const { rows, hasMore } = await listIncidentsPage(api, { limit: query.data.limit, startingAfter, status: query.data.status, monitorId });
  return Response.json(page(rows.map(toApiIncident), hasMore));
});
