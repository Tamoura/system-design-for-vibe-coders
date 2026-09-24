import { asc, eq } from 'drizzle-orm';
import { db, schema } from '@/db';

const { memberships, users } = schema;

/** Everyone in one organization, with their role. */
export async function listMembers({ orgId }: { orgId: string }) {
  return db
    .select({ userId: users.id, name: users.name, email: users.email, role: memberships.role, joinedAt: memberships.createdAt })
    .from(memberships)
    .innerJoin(users, eq(users.id, memberships.userId))
    .where(eq(memberships.organizationId, orgId))
    .orderBy(asc(memberships.createdAt));
}
