import { requirePermission } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { searchEverything } from '@/lib/search';

/**
 * GET /api/orgs/:orgSlug/search?q=…
 *
 * Lesson 2.3 (🟡): one call for the cmd-K palette: pages, monitors and
 * incident updates. The org comes from the URL *and* the membership check,
 * never from a filter the browser sends, so the browser cannot widen it.
 * Server-Timing shows how long the search took (DevTools → Network → Timing).
 */
export const GET = apiRoute(async (req: Request, { params }: { params: Promise<{ orgSlug: string }> }) => {
  const { orgSlug } = await params;
  const ctx = await requirePermission(orgSlug, 'monitor.read');
  const q = new URL(req.url).searchParams.get('q') ?? '';
  const started = performance.now();
  const results = await searchEverything(ctx, q);
  const ms = (performance.now() - started).toFixed(1);
  return Response.json({ data: results }, { headers: { 'Server-Timing': `search;dur=${ms}`, 'Cache-Control': 'private, no-store' } });
});
