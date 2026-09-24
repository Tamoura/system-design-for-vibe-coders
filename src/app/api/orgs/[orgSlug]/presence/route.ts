import { z } from 'zod';
import { requirePermission } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { heartbeat, leave } from '@/lib/presence';

type Params = { params: Promise<{ orgSlug: string }> };
const topicInput = z.object({ topic: z.string().max(100) });

/** POST /api/orgs/:orgSlug/presence { topic } — lesson 4.3 (🟡): heartbeat; answers who is viewing. */
export const POST = apiRoute(async (req: Request, { params }: Params) => {
  const { orgSlug } = await params;
  const ctx = await requirePermission(orgSlug, 'monitor.read');
  const { topic } = topicInput.parse(await req.json());
  return Response.json({ data: await heartbeat(ctx, topic) });
});

/** DELETE /api/orgs/:orgSlug/presence?topic=… — the tab is closing (sent with fetch keepalive). */
export const DELETE = apiRoute(async (req: Request, { params }: Params) => {
  const { orgSlug } = await params;
  const ctx = await requirePermission(orgSlug, 'monitor.read');
  const { topic } = topicInput.parse({ topic: new URL(req.url).searchParams.get('topic') ?? '' });
  await leave(ctx, topic);
  return new Response(null, { status: 204 });
});
