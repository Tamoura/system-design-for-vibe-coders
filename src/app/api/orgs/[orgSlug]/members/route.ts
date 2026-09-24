import { toMemberDto } from '@/core/dto';
import { requirePermission } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { listMembers } from '@/lib/members';

/** GET /api/orgs/:orgSlug/members — names, emails and roles only (MemberDto). */
export const GET = apiRoute(async (_req: Request, { params }: { params: Promise<{ orgSlug: string }> }) => {
  const { orgSlug } = await params;
  const ctx = await requirePermission(orgSlug, 'member.read');
  return Response.json({ data: (await listMembers(ctx)).map(toMemberDto) });
});
