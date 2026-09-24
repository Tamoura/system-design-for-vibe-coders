'use server';

import { revalidatePath } from 'next/cache';
import { inviteInput } from '@/core/validation';
import { forPage, requirePermission } from '@/lib/access';
import { createInvitation, InvitationError, resendInvitation, revokeInvitation } from '@/lib/invitations';

export type InviteFormState = { error?: string; sent?: string };

/** Lesson 1.2 (🟡): invite someone by email and role. Needs "member.manage". */
export async function inviteAction(orgSlug: string, _prev: InviteFormState, formData: FormData): Promise<InviteFormState> {
  const ctx = await forPage(requirePermission(orgSlug, 'member.manage'), `/${orgSlug}/members`);
  const parsed = inviteInput.safeParse({ email: formData.get('email'), role: formData.get('role') });
  if (!parsed.success) return { error: parsed.error.issues[0]?.message };
  try {
    const invitation = await createInvitation(ctx, parsed.data);
    revalidatePath(`/${ctx.orgSlug}/members`);
    return { sent: `Invitation sent to ${invitation.email}.` };
  } catch (err) {
    if (err instanceof InvitationError) return { error: err.message };
    throw err;
  }
}

export async function resendInvitationAction(orgSlug: string, invitationId: string) {
  const ctx = await forPage(requirePermission(orgSlug, 'member.manage'), `/${orgSlug}/members`);
  await resendInvitation(ctx, invitationId).catch((err) => {
    if (!(err instanceof InvitationError)) throw err; // rate limited or no longer open: the list shows the truth
  });
  revalidatePath(`/${ctx.orgSlug}/members`);
}

export async function revokeInvitationAction(orgSlug: string, invitationId: string) {
  const ctx = await forPage(requirePermission(orgSlug, 'member.manage'), `/${orgSlug}/members`);
  await revokeInvitation(ctx, invitationId);
  revalidatePath(`/${ctx.orgSlug}/members`);
}
