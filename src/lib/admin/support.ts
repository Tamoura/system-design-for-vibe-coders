import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import type { AuditSource } from '@/core/audit';
import { recordAudit } from '../audit';
import { auth } from '../auth';
import { InvalidRequestError } from '../errors';
import { findOrgMember } from './customers';

const { sessions } = schema;

/*
 * Lesson 7.1: the account-level support actions. Each one is scoped to a
 * member of the org whose page the staff member is on, takes a reason, and
 * is recorded in that org's audit log (the customer sees "Beacon support").
 * Billing actions live with the billing code (src/lib/billing/support.ts),
 * invitations with the invitation code: every write through the service layer.
 *
 * Beacon has no account lockout to "unlock" (Better Auth rate-limits sign-in
 * attempts by IP instead), so the two account actions are the ones support
 * actually needs: the verification email went to spam, and "someone else may
 * be in my account" (sign out everywhere).
 */

/** "The verification email went to spam": send a new link, through Better Auth. */
export async function resendVerificationEmail(orgId: string, userId: string, reason: string, source: AuditSource) {
  const member = await findOrgMember(orgId, userId);
  if (!member) throw new InvalidRequestError('not_a_member', 'That person is not a member of this organization.');
  if (member.emailVerified) throw new InvalidRequestError('already_verified', `${member.email} is already verified.`);
  await auth.api.sendVerificationEmail({ body: { email: member.email } }); // queues the email (lesson 4.1)
  await withOrg(orgId, (tx) =>
    recordAudit(tx, { orgId, action: 'support.verification_resent', source, target: { type: 'member', id: member.userId, name: member.email }, reason }),
  );
}

/** "Sign this user out everywhere": delete every session, in the transaction that records it. */
export async function revokeUserSessions(orgId: string, userId: string, reason: string, source: AuditSource) {
  const member = await findOrgMember(orgId, userId);
  if (!member) throw new InvalidRequestError('not_a_member', 'That person is not a member of this organization.');
  return db.transaction(async (tx) => {
    const revoked = await tx.delete(sessions).where(eq(sessions.userId, member.userId)).returning({ id: sessions.id });
    await recordAudit(tx, {
      orgId,
      action: 'support.sessions_revoked',
      source,
      target: { type: 'member', id: member.userId, name: member.email },
      metadata: { sessions: revoked.length },
      reason,
    });
    return { revoked: revoked.length };
  });
}
