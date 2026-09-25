import { and, desc, eq, isNull } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { priceForPlan, statusGrantsAccess, type PaidPlanId } from '@/core/plans';
import { InvalidRequestError } from '../errors';
import { getEntitlements, getMonitorUsage } from '../entitlements';
import { getUsageSummary } from '../usage';
import { getBillingProvider } from './provider';

const { organizations, subscriptions } = schema;

/*
 * Lesson 3.1 (🟢): Upgrade and Manage billing.
 *
 * Callers have already checked "billing.manage" (requirePermission); the org
 * comes from that check, never from the request body. Both functions only
 * send the person to a page Stripe hosts. Neither changes the plan: that
 * happens when the signed webhook arrives (src/lib/billing/webhook.ts).
 */

type BillingCtx = { orgId: string; orgSlug: string; orgName: string; userEmail: string };

function appUrl() {
  return (process.env.APP_URL ?? 'http://localhost:3000').replace(/\/$/, '');
}

function requireProvider() {
  const provider = getBillingProvider();
  if (!provider) throw new InvalidRequestError('billing_disabled', 'Billing is not configured on this server (see docs/SOLUTIONS.md, Module 3).');
  return provider;
}

/**
 * The org's Stripe customer, created on first use. The Customer belongs to
 * the organization (lesson 3.1): its id is stored on the org row.
 */
async function ensureCustomer(ctx: BillingCtx): Promise<string> {
  const [org] = await db.select({ customerId: organizations.stripeCustomerId }).from(organizations).where(eq(organizations.id, ctx.orgId));
  if (org?.customerId) return org.customerId;
  const provider = requireProvider();
  // Two clicks at once both get here; the idempotency key makes Stripe return
  // the same customer to both, and the conditional update stores it once.
  const customer = await provider.createCustomer({ orgId: ctx.orgId, name: ctx.orgName, email: ctx.userEmail }, `customer:${ctx.orgId}`);
  await db
    .update(organizations)
    .set({ stripeCustomerId: customer.id })
    .where(and(eq(organizations.id, ctx.orgId), isNull(organizations.stripeCustomerId)));
  const [after] = await db.select({ customerId: organizations.stripeCustomerId }).from(organizations).where(eq(organizations.id, ctx.orgId));
  return after.customerId!;
}

/** "Upgrade to Pro": a Checkout Session for the plan's Price. Returns the URL to send the browser to. */
export async function startCheckout(ctx: BillingCtx, plan: PaidPlanId): Promise<{ url: string }> {
  const provider = requireProvider();
  // One paid subscription per org. Changing plans (Pro → Business) happens in
  // the Portal, which prorates; a second Checkout would bill twice.
  const current = await getCurrentSubscription(ctx);
  if (current) {
    throw new InvalidRequestError('already_subscribed', 'This organization already has a subscription. Change plans in "Manage billing".');
  }
  const customerId = await ensureCustomer(ctx);
  const smsPrice = process.env[`STRIPE_PRICE_${plan.toUpperCase()}_SMS`];
  const base = `${appUrl()}/${ctx.orgSlug}/billing`;
  return provider.createCheckoutSession({
    customerId,
    priceId: priceForPlan(plan),
    meteredPriceIds: smsPrice ? [smsPrice] : [],
    orgId: ctx.orgId,
    // The success page only says "confirming…" (lesson 3.1): visiting this
    // URL by hand grants nothing.
    successUrl: `${base}?checkout=success&plan=${plan}`,
    cancelUrl: `${base}?checkout=cancelled`,
    // Lesson 7.1: an optional free trial (the thing support extends). 0 = none.
    trialDays: Number(process.env.BILLING_TRIAL_DAYS ?? 0) || undefined,
  });
}

/** "Manage billing": the hosted Customer Portal (card, invoices, cancel, change plan). */
export async function openPortal(ctx: BillingCtx): Promise<{ url: string }> {
  const provider = requireProvider();
  const customerId = await ensureCustomer(ctx);
  return provider.createPortalSession({ customerId, returnUrl: `${appUrl()}/${ctx.orgSlug}/billing` });
}

/** The subscription that currently grants the org its plan, if any. */
export async function getCurrentSubscription({ orgId }: { orgId: string }) {
  const rows = await withOrg(orgId, (tx) =>
    tx.select().from(subscriptions).where(eq(subscriptions.organizationId, orgId)).orderBy(desc(subscriptions.currentPeriodEnd)),
  );
  return rows.find((s) => statusGrantsAccess(s.status)) ?? null;
}

/** Everything the billing page and GET /api/orgs/:org/billing show. */
export async function getBillingOverview(ctx: { orgId: string }) {
  const [ent, monitors, usage, subscription, org] = await Promise.all([
    getEntitlements(ctx),
    getMonitorUsage(ctx),
    getUsageSummary(ctx),
    getCurrentSubscription(ctx),
    db.select({ customerId: organizations.stripeCustomerId }).from(organizations).where(eq(organizations.id, ctx.orgId)),
  ]);
  return {
    billingEnabled: getBillingProvider() !== null,
    hasCustomer: Boolean(org[0]?.customerId),
    ent,
    monitors,
    usage,
    subscription,
  };
}

export type BillingOverview = Awaited<ReturnType<typeof getBillingOverview>>;
