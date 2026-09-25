'use server';

import { unsubscribeWithToken } from '@/lib/notifications/subscribers';

export type LinkState = { done?: boolean; ok?: boolean; message?: string };

/** The button on /unsubscribe: a POST, so opening the link alone changes nothing. */
export async function unsubscribeAction(token: string, _prev: LinkState): Promise<LinkState> {
  const result = await unsubscribeWithToken(token);
  return { done: true, ok: result.ok, message: result.message };
}
