import { z } from 'zod';
import { PAID_PLANS } from '@/core/plans';
import { requirePermission } from '@/lib/access';
import { apiRoute } from '@/lib/api';
import { startCheckout } from '@/lib/billing';

type Params = { params: Promise<{ orgSlug: string }> };

const checkoutInput = z.object({ plan: z.enum(PAID_PLANS) });

/**
 * POST /api/orgs/:orgSlug/billing/checkout  { plan: "pro" | "business" }
 * → { url } of a hosted Checkout page. Lesson 3.1: only "billing.manage"
 * (owners). The org is the one in the URL that the caller belongs to; an
 * `orgId` in the body is dropped by the schema.
 */
export const POST = apiRoute(async (req: Request, { params }: Params) => {
  const { orgSlug } = await params;
  const ctx = await requirePermission(orgSlug, 'billing.manage');
  const { plan } = checkoutInput.parse(await req.json());
  return Response.json({ data: await startCheckout(ctx, plan) });
});
