import { UPLOAD_PERMISSION } from '@/core/files';
import { uploadRequestInput } from '@/core/validation';
import { requirePermission } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { requestUpload } from '@/lib/files';

/**
 * POST /api/orgs/:orgSlug/logo  { name, type, size }
 *
 * Lesson 2.2 (🟢): step 1 of a logo upload. Owners and admins only
 * ("page.publish"). A 10 MB file or an .exe is refused here, before any URL
 * is signed. Answers with a 5-minute presigned PUT URL; then the browser
 * uploads straight to storage and calls /files/:fileId/complete.
 */
export const POST = apiRoute(async (req: Request, { params }: { params: Promise<{ orgSlug: string }> }) => {
  const { orgSlug } = await params;
  const ctx = await requirePermission(orgSlug, UPLOAD_PERMISSION.logo);
  const file = uploadRequestInput.parse(await req.json());
  return Response.json({ data: await requestUpload(ctx, 'logo', file) }, { status: 201 });
});
