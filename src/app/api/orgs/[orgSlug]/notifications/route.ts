import { requirePermission } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { countUnread, listNotifications } from '@/lib/notifications';

type Params = { params: Promise<{ orgSlug: string }> };

/**
 * GET /api/orgs/:orgSlug/notifications — lesson 4.2: the signed-in person's
 * inbox in this org, and the unread count the bell shows. Never anyone
 * else's: the query is scoped to the org and the user.
 */
export const GET = apiRoute(async (_req: Request, { params }: Params) => {
  const { orgSlug } = await params;
  const ctx = await requirePermission(orgSlug, 'monitor.read');
  const [items, unread] = await Promise.all([listNotifications(ctx, { limit: 20 }), countUnread(ctx)]);
  return Response.json({ unread, data: items });
});
