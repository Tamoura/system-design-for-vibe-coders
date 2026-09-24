import { toBillingDto } from '@/core/dto';
import { requirePermission } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { getBillingOverview } from '@/lib/billing';

type Params = { params: Promise<{ orgSlug: string }> };

/**
 * GET /api/orgs/:orgSlug/billing — the plan, its limits and this period's
 * usage (lessons 3.1–3.3). Owners and admins ("billing.read").
 */
export const GET = apiRoute(async (_req: Request, { params }: Params) => {
  const { orgSlug } = await params;
  const ctx = await requirePermission(orgSlug, 'billing.read');
  return Response.json({ data: toBillingDto(await getBillingOverview(ctx)) });
});
