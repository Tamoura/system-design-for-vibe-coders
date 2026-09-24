import { requirePermission } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { openPortal } from '@/lib/billing';

type Params = { params: Promise<{ orgSlug: string }> };

/** POST /api/orgs/:orgSlug/billing/portal → { url } of the hosted Customer Portal (lesson 3.1, "billing.manage"). */
export const POST = apiRoute(async (_req: Request, { params }: Params) => {
  const { orgSlug } = await params;
  const ctx = await requirePermission(orgSlug, 'billing.manage');
  return Response.json({ data: await openPortal(ctx) });
});
