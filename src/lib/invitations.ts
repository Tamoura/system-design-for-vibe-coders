import { and, count, desc, eq, gt, isNull } from 'drizzle-orm';
import { db, schema } from '@/db';
import {
  emailsMatch,
  hashToken,
  INVITE_TTL_MS,
  inviteState,
  MAX_INVITES_PER_ORG_PER_HOUR,
  newInviteToken,
  type InviteState,
} from '@/core/invitations';
import { canGrantRole } from '@/core/permissions';
import type { Role } from '@/core/roles';
import { withOrg } from '@/db/tenant';
import type { OrgContext } from './access';
import { trackInTx, track } from './analytics';
import { recordMilestoneInTx } from './onboarding';
import { sendEmail } from './email';
import { appUrl } from './urls';

const { invitations, memberships, organizations, users } = schema;

/** A refusal the person can act on; the message is shown in the UI as-is. */
export class InvitationError extends Error {}

/*
 * Lesson 1.2 (🟡): invitations. Every function that changes an invitation
 * takes the OrgContext from requirePermission(…, 'member.manage') and filters
 * on its orgId, like every other tenant query.
 */

export async function createInvitation(ctx: OrgContext, input: { email: string; role: Role }) {
  // Unverified users must not send email from our domain to arbitrary addresses.
  if (!ctx.emailVerified) throw new InvitationError('Confirm your own email address before inviting people.');
  if (!canGrantRole(ctx.role, input.role)) throw new InvitationError(`As ${ctx.role} you cannot invite someone as ${input.role}.`);

  const [alreadyMember] = await db
    .select({ userId: memberships.userId })
    .from(memberships)
    .innerJoin(users, eq(users.id, memberships.userId))
    .where(and(eq(memberships.organizationId, ctx.orgId), eq(users.email, input.email)))
    .limit(1);
  if (alreadyMember) throw new InvitationError(`${input.email} is already a member.`);

  const [open] = await db
    .select({ id: invitations.id })
    .from(invitations)
    .where(and(eq(invitations.organizationId, ctx.orgId), eq(invitations.email, input.email), isNull(invitations.acceptedAt), isNull(invitations.revokedAt)))
    .limit(1);
  if (open) throw new InvitationError(`${input.email} already has an invitation. Resend it instead.`);

  await assertUnderRateLimit(ctx.orgId);
  const token = newInviteToken();
  const [invitation] = await db
    .insert(invitations)
    .values({
      organizationId: ctx.orgId,
      email: input.email,
      role: input.role,
      tokenHash: hashToken(token),
      invitedBy: ctx.userId,
      expiresAt: new Date(Date.now() + INVITE_TTL_MS),
    })
    .returning();
  // Lessons 6.1/6.2: "invite a teammate" is an onboarding step and a product event (the role, never the email).
  await withOrg(ctx.orgId, async (tx) => {
    await recordMilestoneInTx(tx, ctx.orgId, 'teammate_invited', ctx.userId);
    await trackInTx(tx, ctx, 'teammate_invited', { role: invitation.role });
  });
  await sendInvitationEmail(ctx, invitation.id, invitation.email, invitation.role, token);
  return invitation;
}

/** Resend = a brand-new token and expiry. The old link stops working. */
export async function resendInvitation(ctx: OrgContext, invitationId: string) {
  const invitation = await findOrgInvitation(ctx, invitationId);
  const state = invitation && inviteState(invitation);
  if (!invitation || state === 'accepted' || state === 'revoked') throw new InvitationError('That invitation can no longer be resent.');
  await assertUnderRateLimit(ctx.orgId);
  const token = newInviteToken();
  await db
    .update(invitations)
    .set({ tokenHash: hashToken(token), expiresAt: new Date(Date.now() + INVITE_TTL_MS), sentAt: new Date() })
    .where(and(eq(invitations.organizationId, ctx.orgId), eq(invitations.id, invitationId)));
  await sendInvitationEmail(ctx, invitation.id, invitation.email, invitation.role, token);
}

export async function revokeInvitation(ctx: OrgContext, invitationId: string) {
  await db
    .update(invitations)
    .set({ revokedAt: new Date() })
    .where(and(eq(invitations.organizationId, ctx.orgId), eq(invitations.id, invitationId), isNull(invitations.acceptedAt)));
}

/** Invitations not yet accepted or revoked (pending or expired), newest first. */
export async function listOpenInvitations(ctx: { orgId: string }) {
  const rows = await db
    .select()
    .from(invitations)
    .where(and(eq(invitations.organizationId, ctx.orgId), isNull(invitations.acceptedAt), isNull(invitations.revokedAt)))
    .orderBy(desc(invitations.createdAt));
  return rows.map((r) => ({ id: r.id, email: r.email, role: r.role, expiresAt: r.expiresAt, state: inviteState(r) }));
}

/** For the /invite/[token] page: what the link is for, looked up by the token's hash. */
export async function findInvitationByToken(token: string): Promise<{
  email: string;
  role: Role;
  orgName: string;
  state: InviteState;
} | null> {
  const [row] = await db
    .select({ invitation: invitations, orgName: organizations.name })
    .from(invitations)
    .innerJoin(organizations, eq(organizations.id, invitations.organizationId))
    .where(eq(invitations.tokenHash, hashToken(token)))
    .limit(1);
  if (!row) return null;
  return { email: row.invitation.email, role: row.invitation.role, orgName: row.orgName, state: inviteState(row.invitation) };
}

/**
 * Accept an invitation: a small transaction (lesson 1.2).
 *  1. Find it by the token's hash and check the email matches the signed-in user.
 *  2. Mark it accepted with a *conditional* UPDATE. If two tabs race, only one
 *     UPDATE matches the "not yet accepted" condition, so the link is single use.
 *  3. Create the membership. Already a member? Keep the existing role.
 */
export async function acceptInvitation(token: string, user: { id: string; email: string }): Promise<{ orgSlug: string }> {
  const accepted = await db.transaction(async (tx) => {
    const [invitation] = await tx.select().from(invitations).where(eq(invitations.tokenHash, hashToken(token))).limit(1);
    if (!invitation || inviteState(invitation) !== 'pending') {
      throw new InvitationError('This invitation is invalid, expired, revoked or already used.');
    }
    if (!emailsMatch(invitation.email, user.email)) {
      throw new InvitationError(`This invitation was sent to ${invitation.email}, but you are signed in as ${user.email}.`);
    }
    const claimed = await tx
      .update(invitations)
      .set({ acceptedAt: new Date(), acceptedBy: user.id })
      .where(and(eq(invitations.id, invitation.id), isNull(invitations.acceptedAt), isNull(invitations.revokedAt), gt(invitations.expiresAt, new Date())))
      .returning({ id: invitations.id });
    if (claimed.length === 0) throw new InvitationError('This invitation is invalid, expired, revoked or already used.');

    await tx
      .insert(memberships)
      .values({ organizationId: invitation.organizationId, userId: user.id, role: invitation.role })
      .onConflictDoNothing();
    // Clicking a link we emailed to this address proves the user controls it.
    await tx.update(users).set({ emailVerified: true }).where(eq(users.id, user.id));

    const [org] = await tx.select({ slug: organizations.slug }).from(organizations).where(eq(organizations.id, invitation.organizationId));
    return { orgSlug: org.slug, orgId: invitation.organizationId, role: invitation.role };
  });
  // Lesson 6.2: after the commit (this transaction is not a withOrg one).
  await track({ orgId: accepted.orgId, userId: user.id }, 'invitation_accepted', { role: accepted.role });
  return { orgSlug: accepted.orgSlug };
}

async function findOrgInvitation(ctx: { orgId: string }, invitationId: string) {
  if (!/^[0-9a-f-]{36}$/i.test(invitationId)) return null;
  const [row] = await db
    .select()
    .from(invitations)
    .where(and(eq(invitations.organizationId, ctx.orgId), eq(invitations.id, invitationId)))
    .limit(1);
  return row ?? null;
}

/** A per-org limit counted from the table itself: no Redis needed at this size (lesson 5.2 covers real rate limiters). */
async function assertUnderRateLimit(orgId: string) {
  const [{ sent }] = await db
    .select({ sent: count() })
    .from(invitations)
    .where(and(eq(invitations.organizationId, orgId), gt(invitations.sentAt, new Date(Date.now() - 60 * 60 * 1000))));
  if (sent >= MAX_INVITES_PER_ORG_PER_HOUR) {
    throw new InvitationError(`This organization has sent ${MAX_INVITES_PER_ORG_PER_HOUR} invitations in the last hour. Try again later.`);
  }
}

/**
 * Lesson 4.1: queued, never sent inside the request. The idempotency key is
 * the invitation plus its token: a retried request queues this email once,
 * while "Resend" (a new token) queues a new one.
 */
async function sendInvitationEmail(ctx: OrgContext, invitationId: string, email: string, role: Role, token: string) {
  await sendEmail({
    to: email,
    template: 'invitation',
    props: { inviterEmail: ctx.userEmail, orgName: ctx.orgName, role, url: appUrl(`/invite/${token}`) },
    idempotencyKey: `invitation:${invitationId}:${hashToken(token).slice(0, 16)}`,
  });
}
