import { toMemberDto } from '@/core/dto';
import { changeRoleInput } from '@/core/validation';
import { requirePermission } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { changeMemberRole } from '@/lib/members';

/**
 * PATCH /api/orgs/:orgSlug/members/:userId  { role }
 * 403 for your own role, for anyone above you, and for granting a role above yours.
 */
export const PATCH = apiRoute(async (req: Request, { params }: { params: Promise<{ orgSlug: string; userId: string }> }) => {
  const { orgSlug, userId } = await params;
  const ctx = await requirePermission(orgSlug, 'member.manage');
  const { role } = changeRoleInput.parse(await req.json());
  return Response.json({ data: toMemberDto(await changeMemberRole(ctx, userId, role)) });
});
