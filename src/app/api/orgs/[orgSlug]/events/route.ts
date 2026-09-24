import { requirePermission } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { eventStream } from '@/lib/realtime-stream';
import { isSessionValid } from '@/lib/session';

// A stream that stays open: never cached, never prerendered, Node.js runtime (LISTEN needs a real connection).
export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';

type Params = { params: Promise<{ orgSlug: string }> };

/**
 * GET /api/orgs/:orgSlug/events — lesson 4.3 (🟢): live updates for the
 * dashboard and the bell, as Server-Sent Events. Authorized like every org
 * route (401 / 404 before any stream opens). The exercise says 403 for a
 * non-member; Beacon answers 404 everywhere (lesson 1.2) so an outsider
 * cannot even learn that the org exists.
 */
export const GET = apiRoute(async (req: Request, { params }: Params) => {
  const { orgSlug } = await params;
  const ctx = await requirePermission(orgSlug, 'monitor.read');
  return eventStream(req, ctx, { sessionStillValid: () => isSessionValid(req.headers, ctx.userId) });
});
