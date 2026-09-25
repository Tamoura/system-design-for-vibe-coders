import { organizationNameInput } from '@/core/validation';
import { requirePermission } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { renameOrganization } from '@/lib/organizations';

type Params = { params: Promise<{ orgSlug: string }> };

/**
 * PATCH /api/orgs/:orgSlug/settings  { name }
 *
 * Lesson 6.1 (🟡): the org-rename endpoint. "org.manage" is checked HERE, on
 * the server: a Member calling it directly with curl gets 403, not just a
 * hidden button. The org comes from the URL + membership, never from the body.
 */
export const PATCH = apiRoute(async (req: Request, { params }: Params) => {
  const { orgSlug } = await params;
  const ctx = await requirePermission(orgSlug, 'org.manage');
  const { name } = organizationNameInput.parse(await req.json());
  await renameOrganization(ctx, name);
  return Response.json({ data: { slug: ctx.orgSlug, name } });
});
