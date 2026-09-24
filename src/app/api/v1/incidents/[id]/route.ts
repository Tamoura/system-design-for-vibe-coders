import { fromPublicId } from '@/core/ids';
import { getIncident } from '@/lib/incidents';
import { problem, publicApi, toApiIncident } from '@/lib/public-api';

/** GET /api/v1/incidents/:id */
export const GET = publicApi<{ id: string }>('incidents:read', async (req, api, { id }) => {
  const uuid = fromPublicId('incident', id);
  const incident = uuid ? await getIncident(api, uuid) : null;
  return incident ? Response.json(toApiIncident(incident)) : problem('not-found', { instance: new URL(req.url).pathname });
});
