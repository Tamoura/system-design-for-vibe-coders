import { can } from '@/core/permissions';
import { UPLOAD_PERMISSION } from '@/core/files';
import { AccessError, requireMembership } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { completeUpload, getFile } from '@/lib/files';

type Params = { params: Promise<{ orgSlug: string; fileId: string }> };

/**
 * POST /api/orgs/:orgSlug/files/:fileId/complete
 *
 * Lesson 2.2: step 3, "I have uploaded it". Beacon checks the real size and
 * sniffs the real type; a mismatch deletes the object and answers
 * { status: "rejected" }. Screenshots answer "processing" and a background
 * job makes the thumbnail (enqueued by completeUpload, lesson 5.1).
 *
 * The permission depends on the kind of file, so this is the one route that
 * loads the object before checking the role: membership (401/404), the file
 * in this org (404), then the role for that kind (403).
 */
export const POST = apiRoute(async (_req: Request, { params }: Params) => {
  const { orgSlug, fileId } = await params;
  const ctx = await requireMembership(orgSlug);
  const file = await getFile(ctx, fileId);
  if (!file) throw new AccessError('not_found');
  if (!can(ctx.role, UPLOAD_PERMISSION[file.kind])) throw new AccessError('forbidden');

  const result = await completeUpload(ctx, file);
  return Response.json({ data: { fileId: file.id, status: result.status, reason: result.reason ?? null } });
});
