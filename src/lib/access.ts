import { cache } from 'react';
import { forbidden, notFound, redirect } from 'next/navigation';
import { can, type Permission } from '@/core/permissions';
import type { Role } from '@/core/roles';
import { AccessError } from './errors';
import { findMembership } from './organizations';
import { getCurrentUser } from './session';

/**
 * Everything a request inside an organization needs: which org (by id, for
 * queries), who is asking, and their role there.
 */
export type OrgContext = {
  orgId: string;
  orgSlug: string;
  orgName: string;
  userId: string;
  userEmail: string;
  emailVerified: boolean;
  role: Role;
};

export { AccessError };

/**
 * Lesson 1.2: resolve the org from the URL *and* check the membership, on
 * every request. Not a member? The org "does not exist": 404, never 403, so
 * outsiders cannot even learn that the slug is taken.
 */
export const requireMembership = cache(async (orgSlug: string): Promise<OrgContext> => {
  const user = await getCurrentUser();
  if (!user) throw new AccessError('unauthenticated');
  const membership = await findMembership(orgSlug, user.id);
  if (!membership) throw new AccessError('not_found');
  return {
    orgId: membership.id,
    orgSlug: membership.slug,
    orgName: membership.name,
    userId: user.id,
    userEmail: user.email,
    emailVerified: user.emailVerified,
    role: membership.role,
  };
});

/**
 * Lesson 1.3: the check every page, server action and API route makes before
 * doing any work. It answers, in order:
 *   1. Who is this?                    no session  → 'unauthenticated' (401)
 *   2. Are they in this org?           no          → 'not_found' (404, hides the org)
 *   3. May their role do this action?  no          → 'forbidden' (403)
 * and returns the context whose orgId goes into every query that follows.
 * It checks a permission, never a role name.
 */
export async function requirePermission(orgSlug: string, permission: Permission): Promise<OrgContext> {
  const ctx = await requireMembership(orgSlug);
  if (!can(ctx.role, permission)) throw new AccessError('forbidden');
  return ctx;
}

/**
 * For pages and server actions: run an access check and turn a refusal into
 * what a browser expects — the login page, a 404 page or a 403 page.
 */
export async function forPage<T>(check: Promise<T>, returnTo: string): Promise<T> {
  try {
    return await check;
  } catch (err) {
    if (!(err instanceof AccessError)) throw err;
    if (err.reason === 'unauthenticated') redirect(`/login?next=${encodeURIComponent(returnTo)}`);
    if (err.reason === 'forbidden') forbidden(); // renders src/app/forbidden.tsx with status 403
    notFound();
  }
}
