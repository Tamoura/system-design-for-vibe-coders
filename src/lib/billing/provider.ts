import { FakeBillingProvider } from './fake-provider';
import { StripeBillingProvider } from './stripe-provider';

/**
 * Lesson 3.1: everything Beacon asks of its payment provider, in one small
 * interface. Two implementations:
 *
 *   StripeBillingProvider  the real thing, through the official `stripe` SDK
 *   FakeBillingProvider    in memory, for tests and for running Beacon (and
 *                          the smoke test) without Stripe or the internet
 *
 * Beacon's own code (checkout, the webhook sync, usage reporting) only talks
 * to this interface, so the tests exercise the real code paths with the fake
 * standing in for Stripe's servers. What a provider returns is already in
 * Beacon's shape (`ProviderSubscription`), so no Stripe type leaks further in.
 *
 * Webhook signatures are NOT part of the interface: verifying them is local
 * crypto that needs no network, so both modes use the real
 * `Stripe.webhooks.constructEvent` (src/lib/billing/webhook.ts).
 */
export interface BillingProvider {
  readonly name: 'stripe' | 'fake';

  /** One Customer per organization. The idempotency key makes a retried call return the same customer. */
  createCustomer(input: { orgId: string; name: string; email: string }, idempotencyKey: string): Promise<{ id: string }>;

  /** Lesson 3.1 (🟢): a hosted Checkout page for one plan's Price. */
  createCheckoutSession(input: {
    customerId: string;
    priceId: string;
    /** Extra line items, e.g. the metered SMS price (lesson 3.3). */
    meteredPriceIds: string[];
    orgId: string;
    successUrl: string;
    cancelUrl: string;
    /** Lesson 7.1: a free trial before the first charge (BILLING_TRIAL_DAYS). 0 or absent: none. */
    trialDays?: number;
  }): Promise<{ url: string }>;

  /** Lesson 3.1 (🟢): the hosted Customer Portal (cards, invoices, cancel). */
  createPortalSession(input: { customerId: string; returnUrl: string }): Promise<{ url: string }>;

  /**
   * Lesson 3.1 (🟡): the CURRENT state of a customer's subscriptions, fetched
   * fresh. The webhook handler calls this instead of trusting the event
   * payload, so events arriving out of order cannot write stale state.
   */
  listSubscriptions(customerId: string): Promise<ProviderSubscription[]>;

  /**
   * Lesson 3.3 (🟡): send one usage event to the provider's meter. The
   * `identifier` is our idempotency key: the provider drops a second event
   * with the same identifier, so re-running the reporting job is harmless.
   */
  reportUsage(input: { customerId: string; meter: string; value: number; identifier: string; timestamp: Date }): Promise<void>;

  /**
   * Lesson 7.1 (🟡): Beacon support's "Extend trial". Moves the subscription's
   * trial end in the provider; the webhook sync (or the caller) then copies it.
   */
  extendTrial(subscriptionId: string, trialEnd: Date): Promise<void>;
}

export type ProviderSubscription = {
  id: string;
  customerId: string;
  status: string;
  /** The Price of the plan item (not the metered SMS item). */
  priceId: string | null;
  currentPeriodStart: Date | null;
  currentPeriodEnd: Date | null;
  cancelAtPeriodEnd: boolean;
  /** Set while the subscription is in "trialing". */
  trialEnd: Date | null;
};

/**
 * Which provider this process uses:
 *
 *   BILLING_PROVIDER=fake     the in-memory fake (never with real customers)
 *   STRIPE_SECRET_KEY=sk_…    Stripe (test keys locally, live keys in production)
 *   neither                   null: billing is off, the billing page says so
 */
export function getBillingProvider(): BillingProvider | null {
  if (process.env.BILLING_PROVIDER === 'fake') return fakeBilling();
  if (process.env.STRIPE_SECRET_KEY) {
    const g = globalThis as unknown as { beaconStripe?: StripeBillingProvider };
    g.beaconStripe ??= new StripeBillingProvider(process.env.STRIPE_SECRET_KEY);
    return g.beaconStripe;
  }
  return null;
}

/**
 * The fake's single instance. It lives on globalThis so that every route and
 * server action in the process (and every module instance Next.js creates)
 * sees the same fake "Stripe account".
 */
export function fakeBilling(): FakeBillingProvider {
  const g = globalThis as unknown as { beaconFakeBilling?: FakeBillingProvider };
  g.beaconFakeBilling ??= new FakeBillingProvider();
  return g.beaconFakeBilling;
}

export function isFakeBilling(): boolean {
  return process.env.BILLING_PROVIDER === 'fake';
}
