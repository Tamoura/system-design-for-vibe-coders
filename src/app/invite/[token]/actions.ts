'use server';

import { redirect } from 'next/navigation';
import { acceptInvitation, InvitationError } from '@/lib/invitations';
import { requireUser } from '@/lib/session';

export type AcceptState = { error?: string };

/**
 * Accepting is a POST from a button, never a side effect of opening the link:
 * email scanners open links too, and would otherwise use up the invitation
 * (lesson 1.1, magic links).
 */
export async function acceptInvitationAction(token: string, _prev: AcceptState): Promise<AcceptState> {
  const user = await requireUser(`/invite/${token}`);
  let orgSlug: string;
  try {
    ({ orgSlug } = await acceptInvitation(token, user));
  } catch (err) {
    if (err instanceof InvitationError) return { error: err.message };
    throw err;
  }
  redirect(`/${orgSlug}/monitors`);
}
