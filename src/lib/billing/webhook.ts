import Stripe from 'stripe';
import { eq, isNotNull, and } from 'drizzle-orm';
import { db, schema } from '@/db';
import { syncCustomerFromStripe } from './sync';
import { isFakeBilling } from './provider';

const { stripeEvents } = schema;

/**
 * Lesson 3.1 (🟡): the webhook handler's three jobs, in order.
 *
 *   1. Verify the signature, on the RAW body.
 *   2. Deduplicate by event id.
 *   3. Sync (re-fetch, upsert) and return 2xx fast.
 *
 * The route (src/app/api/stripe/webhook/route.ts) only reads the raw body and
 * the header and hands them here, so the tests can call this directly.
 */

/**
 * The signing secret of the webhook endpoint (`whsec_…`): from the Stripe
 * dashboard, or printed by `stripe listen`. With the fake provider a fixed
 * development secret is used unless one is set.
 */
export const FAKE_WEBHOOK_SECRET = 'whsec_beacon_fake_billing_do_not_use_in_production';

export function webhookSecret(): string | null {
  return process.env.STRIPE_WEBHOOK_SECRET || (isFakeBilling() ? FAKE_WEBHOOK_SECRET : null);
}

/**
 * Only these events mean "a customer's subscriptions may have changed".
 * Everything else is answered 200 and ignored (a 500 would make Stripe retry
 * for days and finally disable the endpoint). Subscribe the endpoint to these
 * only, in the dashboard or with `stripe listen --events …`.
 */
export const HANDLED_EVENTS = new Set([
  'checkout.session.completed',
  'customer.subscription.created',
  'customer.subscription.updated',
  'customer.subscription.deleted',
  'customer.subscription.paused',
  'customer.subscription.resumed',
  'invoice.paid',
  'invoice.payment_failed',
]);

export type WebhookResult = { status: number; body: string };

export async function handleStripeWebhook(rawBody: string, signature: string | null): Promise<WebhookResult> {
  const secret = webhookSecret();
  if (!secret) return { status: 500, body: 'STRIPE_WEBHOOK_SECRET is not set' }; // a 5xx: Stripe retries once it is fixed

  // 1. Verify. constructEvent recomputes the HMAC of the exact bytes Stripe
  //    sent, and refuses a timestamp older than 5 minutes, so a captured
  //    request cannot be replayed later. JSON.parse-then-stringify would
  //    change the bytes, which is why the route reads req.text(), never req.json().
  let event: Stripe.Event;
  try {
    event = Stripe.webhooks.constructEvent(rawBody, signature ?? '', secret);
  } catch {
    return { status: 400, body: 'invalid signature' };
  }

  // 2. Dedupe. The event id is the primary key of stripe_events, so a second
  //    delivery of the same event inserts nothing.
  const firstTime = await db.insert(stripeEvents).values({ id: event.id, type: event.type }).onConflictDoNothing().returning({ id: stripeEvents.id });
  if (firstTime.length === 0) {
    const [done] = await db
      .select({ id: stripeEvents.id })
      .from(stripeEvents)
      .where(and(eq(stripeEvents.id, event.id), isNotNull(stripeEvents.processedAt)));
    // Seen AND processed: nothing to do. Seen but never processed means our
    // first attempt failed half-way; handle this retry. (Two concurrent
    // copies may both sync, which is harmless: the sync is repeatable.)
    if (done) return { status: 200, body: 'duplicate' };
  }

  // 3. Sync. If it throws, the route answers 500 and Stripe retries later.
  const customerId = HANDLED_EVENTS.has(event.type) ? customerIdOf(event) : null;
  if (customerId) await syncCustomerFromStripe(customerId);
  await db.update(stripeEvents).set({ processedAt: new Date() }).where(eq(stripeEvents.id, event.id));
  return { status: 200, body: customerId ? 'ok' : 'ignored' };
}

/** The only thing we take from the payload: which customer changed. */
function customerIdOf(event: Stripe.Event): string | null {
  const obj = event.data.object as { customer?: string | { id: string } | null };
  if (!obj.customer) return null;
  return typeof obj.customer === 'string' ? obj.customer : obj.customer.id;
}

/**
 * Sign a payload the way Stripe does. Used by the fake provider to deliver
 * its events, and by the tests. (`generateTestHeaderString` is the SDK's own
 * helper for exactly this.)
 */
export function signWebhookPayload(payload: string, secret: string, timestamp?: number): string {
  return Stripe.webhooks.generateTestHeaderString({ payload, secret, timestamp });
}

/**
 * Fake billing only: deliver an event to our own webhook endpoint over HTTP,
 * signed, exactly as Stripe would, so the fake goes through verification,
 * dedupe and sync like the real thing.
 */
export async function deliverFakeWebhook(event: object): Promise<number> {
  const secret = webhookSecret();
  if (!secret || !isFakeBilling()) throw new Error('deliverFakeWebhook is only for BILLING_PROVIDER=fake');
  const payload = JSON.stringify(event);
  const url = `${(process.env.APP_URL ?? 'http://localhost:3000').replace(/\/$/, '')}/api/stripe/webhook`;
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'stripe-signature': signWebhookPayload(payload, secret) },
    body: payload,
  });
  return res.status;
}
