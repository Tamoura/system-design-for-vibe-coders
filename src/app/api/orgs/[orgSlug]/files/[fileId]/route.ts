import { requirePermission } from '@/lib/access';
import { apiRoute, notFoundResponse } from '@/lib/api';
import { signedDownloadUrl } from '@/lib/files';

type Params = { params: Promise<{ orgSlug: string; fileId: string }> };

/**
 * GET /api/orgs/:orgSlug/files/:fileId[?variant=thumbnail]
 *
 * Lesson 2.2 (🟡): private files are downloaded through this endpoint only.
 * It checks membership, finds the file *in this org*, and redirects to a
 * presigned GET that expires in 5 minutes. Another org's member gets 404,
 * even with a valid file id.
 */
export const GET = apiRoute(async (req: Request, { params }: Params) => {
  const { orgSlug, fileId } = await params;
  const ctx = await requirePermission(orgSlug, 'monitor.read');
  const variant = new URL(req.url).searchParams.get('variant') === 'thumbnail' ? 'thumbnail' : 'original';
  const url = await signedDownloadUrl(ctx, fileId, variant);
  if (!url) return notFoundResponse();
  // The redirect may be cached briefly by this browser only; the URL it points to dies in 5 minutes.
  return new Response(null, { status: 302, headers: { Location: url, 'Cache-Control': 'private, max-age=60' } });
});
