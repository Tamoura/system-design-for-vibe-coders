import { hasPlanAtLeast, isPaidPlanId, PLAN_IDS, PLANS } from '@/core/plans';
import { forPage, requirePermission } from '@/lib/access';
import { getBillingOverview } from '@/lib/billing';
import { AutoRefresh } from '@/app/_components/auto-refresh';
import { manageBillingAction, upgradeAction } from './actions';
import { UsageCard } from './usage-card';

export const dynamic = 'force-dynamic';

const ERRORS: Record<string, string> = {
  already_subscribed: 'This organization already has a subscription. Change plans in “Manage billing”.',
  billing_disabled: 'Billing is not configured on this server.',
  unknown_plan: 'That plan does not exist.',
};

const day = (d: Date) => d.toISOString().slice(0, 10);

/**
 * Lesson 3.1 (🟢): the billing page. Owners only ("billing.manage"): a
 * member or viewer who opens /<org>/billing gets the 403 page.
 */
export default async function BillingPage({
  params,
  searchParams,
}: {
  params: Promise<{ orgSlug: string }>;
  searchParams: Promise<{ checkout?: string; plan?: string; error?: string }>;
}) {
  const { orgSlug } = await params;
  const ctx = await forPage(requirePermission(orgSlug, 'billing.manage'), `/${orgSlug}/billing`);
  const query = await searchParams;
  const overview = await getBillingOverview(ctx);
  const { ent, subscription } = overview;

  // Lesson 3.1: the success redirect is only a message. The plan changes when
  // the signed webhook arrives; until then we say "confirming…" and refresh.
  const wanted = isPaidPlanId(query.plan) ? query.plan : null;
  const confirming = query.checkout === 'success' && wanted !== null && !hasPlanAtLeast(ent.plan, wanted);

  return (
    <section className="grid" style={{ maxWidth: 760 }}>
      <h1 style={{ margin: 0 }}>Billing</h1>
      <AutoRefresh active={confirming} />
      {confirming && (
        <div className="card" data-testid="confirming">
          <strong>Confirming your payment…</strong>
          <div className="muted">Your plan changes as soon as Stripe confirms the payment. This page updates by itself.</div>
        </div>
      )}
      {query.checkout === 'success' && !confirming && wanted && (
        <div className="card" data-testid="confirmed">Payment confirmed. You are on {PLANS[ent.plan].name}.</div>
      )}
      {query.checkout === 'cancelled' && <div className="card muted">Checkout cancelled. Nothing was charged.</div>}
      {query.error && <div className="card error">{ERRORS[query.error] ?? 'Something went wrong.'}</div>}
      {!overview.billingEnabled && (
        <div className="card muted">
          Billing is not configured on this server. Set <code>STRIPE_SECRET_KEY</code> (or <code>BILLING_PROVIDER=fake</code> for
          development) as described in docs/SOLUTIONS.md.
        </div>
      )}

      {subscription && (
        <div className="card grid">
          <div>
            Subscription: <strong>{subscription.status}</strong>
            {subscription.currentPeriodEnd &&
              (subscription.cancelAtPeriodEnd ? (
                <span className="error" data-testid="cancels-at"> · cancels on {day(subscription.currentPeriodEnd)}</span>
              ) : (
                <span className="muted"> · renews on {day(subscription.currentPeriodEnd)}</span>
              ))}
          </div>
          {/* Lesson 3.1 (🟡): past_due keeps the plan during Stripe's retries, with a warning. */}
          {subscription.status === 'past_due' && (
            <div className="error">Your last payment failed. Update your card in “Manage billing” to keep {PLANS[ent.plan].name}.</div>
          )}
        </div>
      )}

      <UsageCard overview={overview} />

      <div className="row" style={{ alignItems: 'stretch' }}>
        {PLAN_IDS.map((id) => (
          <div key={id} className="card grid" style={{ flex: 1, minWidth: 200 }} data-testid={`plan-${id}`}>
            <strong>{PLANS[id].name}</strong>
            <div>{PLANS[id].priceLabel}</div>
            <div className="muted">{PLANS[id].pitch}</div>
            {id === ent.plan ? (
              <span className="badge">Current plan</span>
            ) : isPaidPlanId(id) && !subscription && overview.billingEnabled ? (
              <form action={upgradeAction.bind(null, ctx.orgSlug, id)}>
                <button className="btn">Upgrade to {PLANS[id].name}</button>
              </form>
            ) : null}
          </div>
        ))}
      </div>

      {overview.billingEnabled && overview.hasCustomer && (
        <form action={manageBillingAction.bind(null, ctx.orgSlug)} className="card grid">
          <div className="muted">Update your card, download invoices, change plan or cancel, on Stripe’s secure page.</div>
          <div><button className="btn secondary">Manage billing</button></div>
        </form>
      )}
    </section>
  );
}
