import { cache } from 'react';
import { notFound, redirect } from 'next/navigation';
import type { Role } from '@/core/roles';
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

/** Why access was refused. Pages, server actions and API routes turn this into a redirect, a 404 page or a status code. */
export class AccessError extends Error {
  constructor(readonly reason: 'unauthenticated' | 'not_found' | 'forbidden') {
    super(reason);
  }
}

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
 * For pages and server actions: run an access check and turn a refusal into
 * what a browser expects — the login page, or a 404 page.
 */
export async function forPage<T>(check: Promise<T>, returnTo: string): Promise<T> {
  try {
    return await check;
  } catch (err) {
    if (!(err instanceof AccessError)) throw err;
    if (err.reason === 'unauthenticated') redirect(`/login?next=${encodeURIComponent(returnTo)}`);
    notFound();
  }
}
