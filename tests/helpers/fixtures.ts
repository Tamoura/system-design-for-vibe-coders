import { vi } from 'vitest';
import { db, schema } from '@/db';
import type { Role } from '@/core/roles';
import { getCurrentUser, type CurrentUser } from '@/lib/session';
import { createOrganization } from '@/lib/organizations';

/*
 * Test fixtures. Import this file only from tests that mock `@/db` (see
 * test-db.ts) and `@/lib/session`:
 *
 *   vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));
 */

let n = 0;

export async function makeUser(label: string, opts: { emailVerified?: boolean } = {}): Promise<CurrentUser> {
  n++;
  const [u] = await db
    .insert(schema.users)
    .values({ name: label, email: `${label.toLowerCase()}-${n}@example.com`, emailVerified: opts.emailVerified ?? true })
    .returning();
  return { id: u.id, email: u.email, name: u.name, emailVerified: u.emailVerified };
}

/** An organization with its owner plus one user per other role. */
export async function makeOrg(name: string) {
  const owner = await makeUser(`${name}-owner`);
  const org = await createOrganization(owner.id, name);
  const users: Record<Role, CurrentUser> = { owner } as Record<Role, CurrentUser>;
  for (const role of ['admin', 'member', 'viewer'] as const) {
    users[role] = await makeUser(`${name}-${role}`);
    await db.insert(schema.memberships).values({ organizationId: org.id, userId: users[role].id, role });
  }
  return { ...org, users };
}

/** Make the next requests come from this user (or from nobody). */
export function signInAs(user: CurrentUser | null) {
  vi.mocked(getCurrentUser).mockResolvedValue(user);
}
