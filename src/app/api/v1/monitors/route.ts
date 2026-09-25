import { MonitorCreate, pageParams } from '@/core/api-schemas';
import { fromPublicId } from '@/core/ids';
import { createMonitor, listMonitorsPage } from '@/lib/monitors';
import { idempotent, page, problem, publicApi, toApiMonitor } from '@/lib/public-api';

/*
 * Lesson 5.2: the public API, version 1. Not the dashboard's JSON routes
 * (/api/orgs/…, cookie sessions): a separate, documented contract reached
 * with API keys. See src/lib/public-api.ts for what every request goes
 * through, and /docs/api for the reference (generated from the same schemas).
 */

/** GET /api/v1/monitors?limit=20&starting_after=mon_… : newest first, cursor-paginated (limit ≤ 100). */
export const GET = publicApi('monitors:read', async (req, api) => {
  const query = pageParams.safeParse(Object.fromEntries(new URL(req.url).searchParams));
  if (!query.success) return problem('invalid-parameter', { detail: 'limit must be 1 to 100; starting_after a monitor id.', instance: '/api/v1/monitors' });
  const startingAfter = query.data.starting_after === undefined ? undefined : fromPublicId('monitor', query.data.starting_after);
  if (startingAfter === null) return problem('invalid-parameter', { detail: 'starting_after is not a monitor id (mon_…).', instance: '/api/v1/monitors' });
  const { rows, hasMore } = await listMonitorsPage(api, { limit: query.data.limit, startingAfter });
  return Response.json(page(rows.map(toApiMonitor), hasMore));
});

/** POST /api/v1/monitors  { name, url, interval_seconds } — send an Idempotency-Key to make retries safe. */
export const POST = publicApi('monitors:write', async (req, api) => {
  const raw = await req.text();
  return idempotent(req, api.orgId, raw, async () => {
    const input = MonitorCreate.parse(JSON.parse(raw)); // ZodError → 422, SyntaxError → 400
    // The org comes from the key, the author from the key's creator: never from the body.
    const monitor = await createMonitor({ orgId: api.orgId, userId: api.createdBy }, { name: input.name, url: input.url, intervalSeconds: input.interval_seconds }, 'api');
    return Response.json(toApiMonitor(monitor), { status: 201 });
  });
});
