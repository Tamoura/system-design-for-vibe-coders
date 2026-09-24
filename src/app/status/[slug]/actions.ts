'use server';

import { z } from 'zod';
import { confirmSubscription, subscribeToStatusPage } from '@/lib/notifications/subscribers';
import type { LinkState } from '@/app/unsubscribe/actions';

export type SubscribeState = { message?: string; error?: string };

const subscribeInput = z.object({ email: z.string().trim().toLowerCase().email('Enter a valid email address').max(254) });

/** Lesson 4.2 (🟡): the public subscribe form. Always the same answer, whoever is or is not subscribed. */
export async function subscribeAction(slug: string, _prev: SubscribeState, formData: FormData): Promise<SubscribeState> {
  const parsed = subscribeInput.safeParse({ email: formData.get('email') });
  if (!parsed.success) return { error: parsed.error.issues[0].message };
  const result = await subscribeToStatusPage(slug, parsed.data.email);
  if (result === 'not_found') return { error: 'This status page is not published.' };
  return { message: `Almost done: we sent a confirmation link to ${parsed.data.email}. Open it to start getting updates.` };
}

export async function confirmSubscriptionAction(token: string, _prev: LinkState): Promise<LinkState> {
  const result = await confirmSubscription(token);
  return { done: true, ok: result.ok, message: result.message };
}
