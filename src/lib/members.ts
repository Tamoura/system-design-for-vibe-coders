import { and, asc, eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { roleChangeRefusal, type Actor } from '@/core/permissions';
import type { Role } from '@/core/roles';
import type { AuditSource } from '@/core/audit';
import { withOrg } from '@/db/tenant';
import { auditSourceOf, recordAudit } from './audit';
import { AccessError } from './errors';

const { memberships, users } = schema;

const memberColumns = { userId: users.id, name: users.name, email: users.email, role: memberships.role, joinedAt: memberships.createdAt };

/** Everyone in one organization, with their role. */
export async function listMembers({ orgId }: { orgId: string }) {
  return db
    .select(memberColumns)
    .from(memberships)
    .innerJoin(users, eq(users.id, memberships.userId))
    .where(eq(memberships.organizationId, orgId))
    .orderBy(asc(memberships.createdAt));
}

export type MemberRow = Awaited<ReturnType<typeof listMembers>>[number];

/**
 * Lesson 1.3 (🟡): change someone's role inside this org. The target is
 * looked up *in this org* (404 otherwise); the rules live in
 * roleChangeRefusal(). Because nobody may change their own role, the acting
 * owner always stays an owner, so an org can never lose its last owner here.
 */
export async function changeMemberRole(ctx: { orgId: string; audit?: AuditSource } & Actor, targetUserId: string, newRole: Role): Promise<MemberRow> {
  const [target] = /^[0-9a-f-]{36}$/i.test(targetUserId)
    ? await db
        .select(memberColumns)
        .from(memberships)
        .innerJoin(users, eq(users.id, memberships.userId))
        .where(and(eq(memberships.organizationId, ctx.orgId), eq(memberships.userId, targetUserId)))
    : [];
  if (!target) throw new AccessError('not_found');
  if (roleChangeRefusal(ctx, target, newRole)) throw new AccessError('forbidden');
  if (target.role === newRole) return target; // nothing changed, nothing to record
  // Lesson 7.3: the change and its audit event commit together, or neither does.
  await withOrg(ctx.orgId, async (tx) => {
    await tx
      .update(memberships)
      .set({ role: newRole })
      .where(and(eq(memberships.organizationId, ctx.orgId), eq(memberships.userId, targetUserId)));
    await recordAudit(tx, {
      orgId: ctx.orgId,
      action: 'member.role_changed',
      source: auditSourceOf(ctx),
      target: { type: 'member', id: target.userId, name: target.email },
      changes: { role: { before: target.role, after: newRole } },
    });
  });
  return { ...target, role: newRole };
}
