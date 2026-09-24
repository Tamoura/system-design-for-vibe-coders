import { UPLOAD_PERMISSION } from '@/core/files';
import { uploadRequestInput } from '@/core/validation';
import { requirePermission } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { requestUpload } from '@/lib/files';

type Params = { params: Promise<{ orgSlug: string; incidentId: string }> };

/**
 * POST /api/orgs/:orgSlug/incidents/:incidentId/screenshots  { name, type, size }
 *
 * Lesson 2.2 (🟡): step 1 of an incident screenshot upload, for anyone who
 * may update incidents. The incident must belong to this org (404 otherwise).
 */
export const POST = apiRoute(async (req: Request, { params }: Params) => {
  const { orgSlug, incidentId } = await params;
  const ctx = await requirePermission(orgSlug, UPLOAD_PERMISSION.incident_screenshot);
  const file = uploadRequestInput.parse(await req.json());
  return Response.json({ data: await requestUpload(ctx, 'incident_screenshot', file, incidentId) }, { status: 201 });
});
