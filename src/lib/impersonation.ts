import { createHash, randomBytes } from 'node:crypto';
import { and, eq, gt, isNull } from 'drizzle-orm';
import { alias } from 'drizzle-orm/pg-core';
import { db, schema } from '@/db';
import type { AuditSource } from '@/core/audit';
import { IMPERSONATION_TTL_MS, staffCan } from '@/core/staff';
import { recordAudit } from './audit';
import { AccessError, InvalidRequestError } from './errors';
import type { StaffMember } from './staff';

const { impersonationSessions, memberships, organizations, staffUsers, users } = schema;

/*
 * Lesson 7.1: impersonation, "see what the customer sees", done the safe way.
 *
 *   read-only      src/proxy.ts refuses every POST/PUT/PATCH/DELETE while the
 *                  cookie is present (server actions are POSTs too), and
 *                  requirePermission() refuses any non-read permission
 *   time-limited   30 minutes from the start, active or not; no "remember me"
 *   one org        the session is bound to the org it was started from:
 *                  the customer's other orgs stay 404
 *   bannered       every page of the app shows who is viewing and until when
 *   audited        impersonation.started / .ended in the CUSTOMER's audit log,
 *                  with actor = the staff member and on_behalf_of = the customer,
 *                  so it reads "Beacon support (on behalf of Ana)"
 *
 * The staff member keeps their own session; the impersonation is a second,
 * HttpOnly cookie holding a random token whose hash is stored here. It counts
 * only together with the session of the staff member who started it.
 */
export type ImpersonationInfo = {
  id: string;
  staffUserId: string;
  staffEmail: string;
  orgId: string;
  orgSlug: string;
  readOnly: boolean;
  expiresAt: Date;
};

// A second reference to `users`: the staff member's own account, next to the customer's.
const staffAccount = alias(users, 'staff_account');

const hash = (token: string) => createHash('sha256').update(token).digest('hex');

/** Start: checks, one row, one audit event, in one transaction. Returns the cookie's token. */
export async function startImpersonation(
  staff: StaffMember,
  input: { orgId: string; targetUserId: string; reason: string },
  source: AuditSource,
  now = new Date(),
): Promise<{ token: string; expiresAt: Date; orgSlug: string }> {
  if (!staffCan(staff.role, 'impersonate')) throw new AccessError('forbidden');
  if (input.targetUserId === staff.userId) throw new InvalidRequestError('self', 'You cannot impersonate yourself.');
  const [target] = await db
    .select({ userId: users.id, name: users.name, email: users.email, orgSlug: organizations.slug })
    .from(memberships)
    .innerJoin(users, eq(users.id, memberships.userId))
    .innerJoin(organizations, eq(organizations.id, memberships.organizationId))
    .where(and(eq(memberships.organizationId, input.orgId), eq(memberships.userId, input.targetUserId)));
  if (!target) throw new InvalidRequestError('not_a_member', 'That person is not a member of this organization.');

  const token = randomBytes(32).toString('base64url');
  const expiresAt = new Date(now.getTime() + IMPERSONATION_TTL_MS);
  // As the owner: beacon_app has no rights on impersonation_sessions (migration 0024).
  await db.transaction(async (tx) => {
    const [row] = await tx
      .insert(impersonationSessions)
      .values({ tokenHash: hash(token), staffUserId: staff.staffId, targetUserId: target.userId, organizationId: input.orgId, reason: input.reason, readOnly: true, expiresAt })
      .returning({ id: impersonationSessions.id });
    await recordAudit(tx, {
      orgId: input.orgId,
      action: 'support.impersonation_started',
      source: { ...source, onBehalfOf: { id: target.userId, name: target.name, email: target.email } },
      target: { type: 'user', id: target.userId, name: target.name },
      reason: input.reason,
      metadata: { impersonation_id: row.id, read_only: true, expires_at: expiresAt.toISOString() },
      at: now,
    });
  });
  return { token, expiresAt, orgSlug: target.orgSlug };
}

/**
 * On every request of a staff member who has the cookie: the customer to act
 * as, or null (wrong staff member, ended, expired, or no longer staff).
 */
export async function resolveImpersonation(sessionUserId: string, token: string, now = new Date()) {
  const [row] = await db
    .select({
      id: impersonationSessions.id,
      staffUserId: impersonationSessions.staffUserId,
      staffEmail: staffAccount.email,
      orgId: impersonationSessions.organizationId,
      orgSlug: organizations.slug,
      readOnly: impersonationSessions.readOnly,
      expiresAt: impersonationSessions.expiresAt,
      target: { id: users.id, email: users.email, name: users.name, emailVerified: users.emailVerified },
    })
    .from(impersonationSessions)
    .innerJoin(staffUsers, eq(staffUsers.id, impersonationSessions.staffUserId))
    .innerJoin(staffAccount, eq(staffAccount.id, staffUsers.userId))
    .innerJoin(users, eq(users.id, impersonationSessions.targetUserId))
    .innerJoin(organizations, eq(organizations.id, impersonationSessions.organizationId))
    .where(
      and(
        eq(impersonationSessions.tokenHash, hash(token)),
        eq(staffUsers.userId, sessionUserId), // only for the staff member who started it
        isNull(impersonationSessions.endedAt),
        gt(impersonationSessions.expiresAt, now),
      ),
    );
  if (!row) return null;
  const { target, ...info } = row;
  return { ...target, impersonation: info satisfies ImpersonationInfo };
}

/** Exit: marks the row ended and records it. Idempotent; returns the org's slug for the redirect. */
export async function endImpersonation(sessionUserId: string, token: string, source: AuditSource, now = new Date()): Promise<{ orgId: string } | null> {
  return db.transaction(async (tx) => {
    const [row] = await tx
      .select({ session: impersonationSessions, staffUserId: staffUsers.userId, targetName: users.name, targetEmail: users.email })
      .from(impersonationSessions)
      .innerJoin(staffUsers, eq(staffUsers.id, impersonationSessions.staffUserId))
      .innerJoin(users, eq(users.id, impersonationSessions.targetUserId))
      .where(eq(impersonationSessions.tokenHash, hash(token)))
      .for('update', { of: impersonationSessions });
    if (!row || row.staffUserId !== sessionUserId) return null;
    if (row.session.endedAt) return { orgId: row.session.organizationId };
    await tx.update(impersonationSessions).set({ endedAt: now }).where(eq(impersonationSessions.id, row.session.id));
    await recordAudit(tx, {
      orgId: row.session.organizationId,
      action: 'support.impersonation_ended',
      source: { ...source, onBehalfOf: { id: row.session.targetUserId, name: row.targetName, email: row.targetEmail } },
      target: { type: 'user', id: row.session.targetUserId, name: row.targetName },
      metadata: { impersonation_id: row.session.id, expired: row.session.expiresAt <= now },
      at: now,
    });
    return { orgId: row.session.organizationId };
  });
}
