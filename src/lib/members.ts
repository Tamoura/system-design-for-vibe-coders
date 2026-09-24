import { and, asc, eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { roleChangeRefusal, type Actor } from '@/core/permissions';
import type { Role } from '@/core/roles';
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
export async function changeMemberRole(ctx: { orgId: string } & Actor, targetUserId: string, newRole: Role): Promise<MemberRow> {
  const [target] = /^[0-9a-f-]{36}$/i.test(targetUserId)
    ? await db
        .select(memberColumns)
        .from(memberships)
        .innerJoin(users, eq(users.id, memberships.userId))
        .where(and(eq(memberships.organizationId, ctx.orgId), eq(memberships.userId, targetUserId)))
    : [];
  if (!target) throw new AccessError('not_found');
  if (roleChangeRefusal(ctx, target, newRole)) throw new AccessError('forbidden');
  // TODO(7.3): record "member.role_changed" in the audit log.
  await db
    .update(memberships)
    .set({ role: newRole })
    .where(and(eq(memberships.organizationId, ctx.orgId), eq(memberships.userId, targetUserId)));
  return { ...target, role: newRole };
}
