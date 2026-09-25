'use server';

import { after } from 'next/server';
import { redirect } from 'next/navigation';
import { fakeBilling } from '@/lib/billing/provider';
import { deliverFakeWebhook } from '@/lib/billing/webhook';
import { requireFakeCheckoutSession, requireFakePortalSession } from './access';

/** Stripe's test card that always succeeds. Any other number is declined, like 4000 0000 0000 0002. */
const TEST_CARD = '4242424242424242';

export type PayState = { error?: string };

/**
 * "Pay" on the fake Checkout page. Like Stripe: the subscription starts, the
 * browser goes back to Beacon's success URL, and the webhook arrives a moment
 * LATER, signed. Beacon must not grant anything before it does.
 */
export async function payAction(sessionId: string, _prev: PayState, formData: FormData): Promise<PayState> {
  const { session } = await requireFakeCheckoutSession(sessionId);
  if (String(formData.get('card') ?? '').replace(/\s/g, '') !== TEST_CARD) return { error: 'Your card was declined.' };
  const event = fakeBilling().simulateCheckoutCompleted(sessionId);
  after(async () => {
    await new Promise((r) => setTimeout(r, 1500)); // webhooks are asynchronous; show "confirming…" meanwhile
    await deliverFakeWebhook(event);
  });
  redirect(session.successUrl);
}

/** The fake Portal's buttons: what a customer can do to their subscription in Stripe's Portal. */
export async function changeSubscriptionAction(sessionId: string, subscriptionId: string, change: 'cancel_at_period_end' | 'resume' | 'cancel_now') {
  const { session } = await requireFakePortalSession(sessionId);
  const sub = fakeBilling().subscriptions.get(subscriptionId);
  if (!sub || sub.customerId !== session.customerId) redirect(`/fake-billing/portal/${sessionId}`);
  const event = fakeBilling().simulateSubscriptionChange(
    subscriptionId,
    change === 'cancel_now' ? { status: 'canceled', cancelAtPeriodEnd: false } : { cancelAtPeriodEnd: change === 'cancel_at_period_end' },
  );
  await deliverFakeWebhook(event); // the Portal's own changes arrive by webhook too
  redirect(`/fake-billing/portal/${sessionId}`);
}
