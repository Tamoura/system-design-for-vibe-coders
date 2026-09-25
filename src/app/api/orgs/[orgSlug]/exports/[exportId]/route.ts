import { apiRoute } from '@/lib/api';
import { requirePermission } from '@/lib/access';
import { exportDownloadUrl } from '@/lib/privacy/org-data';

/**
 * GET /api/orgs/:org/exports/:id — lesson 8.1: download an organization
 * export. Owners only ("org.export"), this org's exports only (404 for any
 * other), and the answer is a redirect to a signed URL that dies in 5 minutes.
 */
export const GET = apiRoute(async (_req: Request, { params }: { params: Promise<{ orgSlug: string; exportId: string }> }) => {
  const { orgSlug, exportId } = await params;
  const ctx = await requirePermission(orgSlug, 'org.export');
  const url = await exportDownloadUrl(ctx, exportId);
  return new Response(null, { status: 303, headers: { location: url, 'cache-control': 'no-store' } });
});
