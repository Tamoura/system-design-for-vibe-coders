import Stripe from 'stripe';
import { planForPrice } from '@/core/plans';
import type { BillingProvider, ProviderSubscription } from './provider';

/**
 * Lesson 3.1: the real provider, through the official Stripe SDK. Hosted
 * Checkout and the hosted Customer Portal, so card numbers never touch
 * Beacon's servers and PCI scope stays minimal.
 *
 * Every method is a network call: never call one inside withOrg() (a
 * transaction would hold its database connection while waiting on Stripe).
 */
export class StripeBillingProvider implements BillingProvider {
  readonly name = 'stripe' as const;
  private readonly stripe: Stripe;

  constructor(secretKey: string) {
    this.stripe = new Stripe(secretKey);
  }

  async createCustomer(input: { orgId: string; name: string; email: string }, idempotencyKey: string) {
    // Lesson 3.1 (🟡), idempotency goes both ways: if this request times out
    // and we retry with the same key, Stripe returns the first customer
    // instead of creating a second one. The key comes from our intent
    // ("a customer for org X"), never from a random UUID.
    const customer = await this.stripe.customers.create(
      { name: input.name, email: input.email, metadata: { orgId: input.orgId } },
      { idempotencyKey },
    );
    return { id: customer.id };
  }

  async createCheckoutSession(input: {
    customerId: string;
    priceId: string;
    meteredPriceIds: string[];
    orgId: string;
    successUrl: string;
    cancelUrl: string;
  }) {
    if (input.priceId.startsWith('price_fake_')) {
      throw new Error('Set STRIPE_PRICE_PRO and STRIPE_PRICE_BUSINESS to your Stripe Price ids (see .env.example).');
    }
    const session = await this.stripe.checkout.sessions.create({
      mode: 'subscription',
      customer: input.customerId,
      // The org id travels with the session, so the Stripe dashboard (and a
      // webhook, if we ever need it) can tell which workspace paid.
      client_reference_id: input.orgId,
      metadata: { orgId: input.orgId },
      subscription_data: { metadata: { orgId: input.orgId } },
      line_items: [
        { price: input.priceId, quantity: 1 },
        // Metered prices take no quantity: Stripe sums the meter (lesson 3.3).
        ...input.meteredPriceIds.map((price) => ({ price })),
      ],
      success_url: input.successUrl,
      cancel_url: input.cancelUrl,
    });
    if (!session.url) throw new Error('Stripe returned a Checkout Session without a URL');
    return { url: session.url };
  }

  async createPortalSession(input: { customerId: string; returnUrl: string }) {
    const session = await this.stripe.billingPortal.sessions.create({ customer: input.customerId, return_url: input.returnUrl });
    return { url: session.url };
  }

  async listSubscriptions(customerId: string): Promise<ProviderSubscription[]> {
    const result: ProviderSubscription[] = [];
    // status 'all' includes canceled ones, so a cancellation is synced too.
    for await (const sub of this.stripe.subscriptions.list({ customer: customerId, status: 'all', limit: 100 })) {
      result.push(toProviderSubscription(sub));
    }
    return result;
  }

  async reportUsage(input: { customerId: string; meter: string; value: number; identifier: string; timestamp: Date }) {
    // Lesson 3.3 (🟡): Stripe Billing meters. `identifier` is our idempotency
    // key; Stripe ignores a second event with the same identifier (for at
    // least 24 hours), so the reporting job can retry safely.
    await this.stripe.billing.meterEvents.create({
      event_name: input.meter,
      identifier: input.identifier,
      timestamp: Math.floor(input.timestamp.getTime() / 1000),
      payload: { stripe_customer_id: input.customerId, value: String(input.value) },
    });
  }
}

/**
 * Stripe's subscription → Beacon's shape. A Pro subscription has two items
 * (the Pro price, and the metered SMS price); the plan item is the one whose
 * price maps to a plan. Since Stripe's 2025 API versions the billing period
 * lives on the subscription items, not on the subscription.
 */
function toProviderSubscription(sub: Stripe.Subscription): ProviderSubscription {
  const items = sub.items.data;
  const planItem = items.find((i) => planForPrice(i.price.id) !== 'free') ?? items[0];
  return {
    id: sub.id,
    customerId: typeof sub.customer === 'string' ? sub.customer : sub.customer.id,
    status: sub.status,
    priceId: planItem?.price.id ?? null,
    currentPeriodStart: planItem ? new Date(planItem.current_period_start * 1000) : null,
    currentPeriodEnd: planItem ? new Date(planItem.current_period_end * 1000) : null,
    cancelAtPeriodEnd: sub.cancel_at_period_end,
  };
}
