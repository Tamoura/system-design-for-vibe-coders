import { randomBytes } from 'node:crypto';
import type { BillingProvider, ProviderSubscription } from './provider';

/**
 * An in-memory stand-in for Stripe, used when BILLING_PROVIDER=fake: by the
 * tests, by the headless-browser smoke test, and by anyone running Beacon
 * without a Stripe account or internet access. NEVER for real customers.
 *
 * It behaves like the parts of Stripe Beacon uses: customers (idempotent),
 * Checkout and Portal sessions whose URLs point at small pages in Beacon
 * (/fake-billing/…), subscriptions, and a meter that dedupes by identifier.
 * The pages call the `simulate…` methods below, which return the Stripe-shaped
 * event that Stripe would send; the caller then delivers it, SIGNED, to
 * /api/stripe/webhook (see deliverFakeWebhook in src/lib/billing/webhook.ts),
 * so the fake exercises the real verification and sync code.
 *
 * State lives in this process only, and is gone after a restart.
 */
export class FakeBillingProvider implements BillingProvider {
  readonly name = 'fake' as const;

  customers = new Map<string, { id: string; orgId: string; name: string; email: string }>();
  checkoutSessions = new Map<string, FakeCheckoutSession>();
  portalSessions = new Map<string, { id: string; customerId: string; returnUrl: string }>();
  subscriptions = new Map<string, ProviderSubscription>();
  meterEvents = new Map<string, { customerId: string; meter: string; value: number; timestamp: Date }>();
  /** How often each method was called, so tests can assert "no second call". */
  calls: Record<string, number> = {};
  /** Make the next N reportUsage calls fail, like a network blip. */
  failNextReports = 0;

  private idempotency = new Map<string, string>();

  reset() {
    this.customers.clear();
    this.checkoutSessions.clear();
    this.portalSessions.clear();
    this.subscriptions.clear();
    this.meterEvents.clear();
    this.idempotency.clear();
    this.calls = {};
    this.failNextReports = 0;
  }

  private count(method: string) {
    this.calls[method] = (this.calls[method] ?? 0) + 1;
  }

  async createCustomer(input: { orgId: string; name: string; email: string }, idempotencyKey: string) {
    this.count('createCustomer');
    const existing = this.idempotency.get(idempotencyKey);
    if (existing) return { id: existing }; // same key → same customer, like Stripe
    const id = fakeId('cus');
    this.customers.set(id, { id, ...input });
    this.idempotency.set(idempotencyKey, id);
    return { id };
  }

  async createCheckoutSession(input: {
    customerId: string;
    priceId: string;
    meteredPriceIds: string[];
    orgId: string;
    successUrl: string;
    cancelUrl: string;
    trialDays?: number;
  }) {
    this.count('createCheckoutSession');
    const id = fakeId('cs');
    this.checkoutSessions.set(id, { id, ...input, status: 'open' });
    return { url: `${appUrl()}/fake-billing/checkout/${id}` };
  }

  async createPortalSession(input: { customerId: string; returnUrl: string }) {
    this.count('createPortalSession');
    const id = fakeId('bps');
    this.portalSessions.set(id, { id, ...input });
    return { url: `${appUrl()}/fake-billing/portal/${id}` };
  }

  async listSubscriptions(customerId: string) {
    this.count('listSubscriptions');
    return [...this.subscriptions.values()].filter((s) => s.customerId === customerId).map((s) => ({ ...s }));
  }

  async reportUsage(input: { customerId: string; meter: string; value: number; identifier: string; timestamp: Date }) {
    this.count('reportUsage');
    if (this.failNextReports > 0) {
      this.failNextReports--;
      throw new Error('fake network error');
    }
    // Like Stripe's meter: a second event with the same identifier is ignored.
    if (!this.meterEvents.has(input.identifier)) {
      this.meterEvents.set(input.identifier, { customerId: input.customerId, meter: input.meter, value: input.value, timestamp: input.timestamp });
    }
  }

  /** Like Stripe's meter event summaries: the sum for one customer and meter in [start, end). */
  meterSummary(customerId: string, meter: string, start: Date, end: Date): number {
    let total = 0;
    for (const e of this.meterEvents.values()) {
      if (e.customerId === customerId && e.meter === meter && e.timestamp >= start && e.timestamp < end) total += e.value;
    }
    return total;
  }

  /* ------------------------------------------------------------------
   * Simulations: what happens on Stripe's side when a person pays or
   * changes their subscription. Each returns the event Stripe would send.
   * ------------------------------------------------------------------ */

  /** The customer paid on the Checkout page: a subscription starts. */
  simulateCheckoutCompleted(sessionId: string, now: Date = new Date()): FakeStripeEvent {
    const session = this.checkoutSessions.get(sessionId);
    if (!session || session.status !== 'open') throw new Error('No open checkout session with that id');
    session.status = 'complete';
    // Lesson 7.1: with a trial, Stripe starts the subscription in "trialing" and bills at trial_end.
    const trialEnd = session.trialDays ? new Date(now.getTime() + session.trialDays * 86_400_000) : null;
    const sub: ProviderSubscription = {
      id: fakeId('sub'),
      customerId: session.customerId,
      status: trialEnd ? 'trialing' : 'active',
      priceId: session.priceId,
      currentPeriodStart: now,
      currentPeriodEnd: trialEnd ?? addMonths(now, 1),
      cancelAtPeriodEnd: false,
      trialEnd,
    };
    this.subscriptions.set(sub.id, sub);
    return fakeEvent('checkout.session.completed', {
      id: session.id,
      object: 'checkout.session',
      customer: session.customerId,
      client_reference_id: session.orgId,
      subscription: sub.id,
    });
  }

  /** Like `stripe.subscriptions.update(id, { trial_end })`: a trialing subscription's trial moves; the period ends with it. */
  async extendTrial(subscriptionId: string, trialEnd: Date) {
    this.count('extendTrial');
    const sub = this.subscriptions.get(subscriptionId);
    if (!sub) throw new Error('No such subscription: ' + subscriptionId);
    if (sub.status !== 'trialing') throw new Error('This subscription is not in a trial');
    sub.trialEnd = trialEnd;
    sub.currentPeriodEnd = trialEnd;
  }

  /** Change a subscription the way the Portal (or Stripe's dunning) would. */
  simulateSubscriptionChange(subscriptionId: string, change: Partial<Omit<ProviderSubscription, 'id' | 'customerId'>>): FakeStripeEvent {
    const sub = this.subscriptions.get(subscriptionId);
    if (!sub) throw new Error('No subscription with that id');
    Object.assign(sub, change);
    const type = sub.status === 'canceled' ? 'customer.subscription.deleted' : 'customer.subscription.updated';
    return fakeEvent(type, { id: sub.id, object: 'subscription', customer: sub.customerId, status: sub.status });
  }

  /** Test helper: a subscription that already exists (e.g. created before a test starts). */
  seedSubscription(sub: Omit<ProviderSubscription, 'id' | 'trialEnd'> & { id?: string; trialEnd?: Date | null }): ProviderSubscription {
    const full = { ...sub, trialEnd: sub.trialEnd ?? null, id: sub.id ?? fakeId('sub') };
    this.subscriptions.set(full.id, full);
    return full;
  }
}

export type FakeCheckoutSession = {
  id: string;
  customerId: string;
  priceId: string;
  meteredPriceIds: string[];
  orgId: string;
  successUrl: string;
  cancelUrl: string;
  trialDays?: number;
  status: 'open' | 'complete';
};

/** The parts of a Stripe event Beacon reads. */
export type FakeStripeEvent = {
  id: string;
  object: 'event';
  type: string;
  created: number;
  livemode: false;
  data: { object: Record<string, unknown> };
};

export function fakeEvent(type: string, object: Record<string, unknown>): FakeStripeEvent {
  return { id: fakeId('evt'), object: 'event', type, created: Math.floor(Date.now() / 1000), livemode: false, data: { object } };
}

function fakeId(prefix: string) {
  return `${prefix}_fake_${randomBytes(9).toString('base64url')}`;
}

function addMonths(d: Date, n: number) {
  const r = new Date(d);
  r.setUTCMonth(r.getUTCMonth() + n);
  return r;
}

function appUrl() {
  return (process.env.APP_URL ?? 'http://localhost:3000').replace(/\/$/, '');
}
