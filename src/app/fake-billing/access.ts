import { eq } from 'drizzle-orm';
import { notFound } from 'next/navigation';
import { db, schema } from '@/db';
import { forPage, requirePermission } from '@/lib/access';
import { fakeBilling, isFakeBilling } from '@/lib/billing/provider';

/*
 * The fake provider's stand-ins for Stripe's hosted pages (BILLING_PROVIDER=fake
 * only; 404 otherwise). They exist so Beacon, and the smoke test, can go
 * through "Upgrade → pay → webhook → Pro" without Stripe or the internet.
 *
 * They still check access like any page: only someone with "billing.manage"
 * in the org a session belongs to may use it.
 */

async function requireBillingManager(orgId: string, returnTo: string) {
  const [org] = await db.select({ slug: schema.organizations.slug }).from(schema.organizations).where(eq(schema.organizations.id, orgId));
  if (!org) notFound();
  return forPage(requirePermission(org.slug, 'billing.manage'), returnTo);
}

export async function requireFakeCheckoutSession(sessionId: string) {
  if (!isFakeBilling()) notFound();
  const session = fakeBilling().checkoutSessions.get(sessionId);
  if (!session) notFound();
  const ctx = await requireBillingManager(session.orgId, `/fake-billing/checkout/${sessionId}`);
  return { session, ctx };
}

export async function requireFakePortalSession(sessionId: string) {
  if (!isFakeBilling()) notFound();
  const session = fakeBilling().portalSessions.get(sessionId);
  if (!session) notFound();
  const [org] = await db
    .select({ id: schema.organizations.id })
    .from(schema.organizations)
    .where(eq(schema.organizations.stripeCustomerId, session.customerId));
  if (!org) notFound();
  const ctx = await requireBillingManager(org.id, `/fake-billing/portal/${sessionId}`);
  return { session, ctx };
}
