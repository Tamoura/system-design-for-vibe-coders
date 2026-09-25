import { and, asc, count, eq, ne } from 'drizzle-orm';
import { db, schema } from '@/db';
import type { AuditSource } from '@/core/audit';
import type { StaffRole } from '@/core/staff';
import { recordAudit } from '../audit';
import { InvalidRequestError } from '../errors';

const { staffUsers, users } = schema;

/*
 * Lesson 7.1: granting and removing staff roles. The most powerful write in
 * Beacon, so: superadmins only (staffRoute('staff.manage')) or a shell on a
 * server (`npm run staff`), always with a reason, always a platform audit
 * event, never your own role, and never the last superadmin.
 */

export async function grantStaffRole(input: { email: string; role: StaffRole; reason: string }, source: AuditSource, grantedBy: string | null = null) {
  const [user] = await db.select({ id: users.id, email: users.email, emailVerified: users.emailVerified }).from(users).where(eq(users.email, input.email.toLowerCase()));
  if (!user) throw new InvalidRequestError('no_user', `No Beacon account for ${input.email}. They sign up first (in production: through the company identity provider).`);
  if (!user.emailVerified) throw new InvalidRequestError('unverified', `${input.email} has not verified their email address yet.`);
  return db.transaction(async (tx) => {
    const [before] = await tx.select().from(staffUsers).where(eq(staffUsers.userId, user.id)).for('update');
    if (before && grantedBy && before.id === grantedBy) throw new InvalidRequestError('self', 'You cannot change your own staff role.');
    if (before?.role === 'superadmin' && input.role !== 'superadmin') await assertAnotherSuperadmin(tx, before.id);
    const [row] = await tx
      .insert(staffUsers)
      .values({ userId: user.id, role: input.role, createdBy: grantedBy })
      .onConflictDoUpdate({ target: staffUsers.userId, set: { role: input.role } })
      .returning();
    await recordAudit(tx, {
      orgId: null,
      action: 'staff.granted',
      source,
      target: { type: 'staff', id: row.id, name: user.email },
      changes: { role: { before: before?.role ?? null, after: input.role } },
      reason: input.reason,
    });
    return row;
  });
}

export async function revokeStaff(staffId: string, reason: string, source: AuditSource, revokedBy: string | null = null) {
  if (revokedBy && staffId === revokedBy) throw new InvalidRequestError('self', 'You cannot remove yourself.');
  return db.transaction(async (tx) => {
    const [row] = await tx
      .select({ id: staffUsers.id, role: staffUsers.role, email: users.email })
      .from(staffUsers)
      .innerJoin(users, eq(users.id, staffUsers.userId))
      .where(eq(staffUsers.id, staffId))
      .for('update', { of: staffUsers });
    if (!row) throw new InvalidRequestError('not_staff', 'No such staff member.');
    if (row.role === 'superadmin') await assertAnotherSuperadmin(tx, row.id);
    await tx.delete(staffUsers).where(eq(staffUsers.id, staffId));
    await recordAudit(tx, { orgId: null, action: 'staff.revoked', source, target: { type: 'staff', id: row.id, name: row.email }, changes: { role: { before: row.role, after: null } }, reason });
  });
}

type Tx = Parameters<Parameters<typeof db.transaction>[0]>[0];

async function assertAnotherSuperadmin(tx: Tx, exceptId: string) {
  const [{ n }] = await tx.select({ n: count() }).from(staffUsers).where(and(eq(staffUsers.role, 'superadmin'), ne(staffUsers.id, exceptId)));
  if (n === 0) throw new InvalidRequestError('last_superadmin', 'Beacon must keep at least one superadmin.');
}

/** Every staff member and role: /internal/staff and `npm run staff`. */
export async function listStaff() {
  return db
    .select({ staffId: staffUsers.id, email: users.email, name: users.name, role: staffUsers.role, since: staffUsers.createdAt })
    .from(staffUsers)
    .innerJoin(users, eq(users.id, staffUsers.userId))
    .orderBy(asc(staffUsers.createdAt));
}
