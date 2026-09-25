import { cache } from 'react';
import { headers } from 'next/headers';
import { forbidden, notFound, redirect } from 'next/navigation';
import { can, isReadPermission, type Permission } from '@/core/permissions';
import type { Role } from '@/core/roles';
import type { AuditSource } from '@/core/audit';
import { AccessError } from './errors';
import type { ImpersonationInfo } from './impersonation';
import { annotateContext, clientIpFrom, getContext, requestIdFrom } from './observability/context';
import { findMembership } from './organizations';
import { getCurrentUser, type CurrentUser } from './session';

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
  /**
   * Lesson 7.3: who the audit log names for what this request changes, and
   * from where (IP, user agent, request id). Built once, here, so no service
   * function has to dig it out of the request. (Optional only so that tests
   * and scripts can build a context by hand: auditSourceOf() then falls back
   * to the user id.)
   */
  audit?: AuditSource;
  /** Lesson 7.1: set while Beacon staff view this org as this user. */
  impersonation?: ImpersonationInfo;
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
  // Lesson 7.1: an impersonation is bound to the org it was started from.
  if (user.impersonation && user.impersonation.orgId !== membership.id) throw new AccessError('not_found');
  // Lesson 7.2: from here on, every log line of this request names the org and the user.
  annotateContext({ orgId: membership.id, userId: user.id, impersonatorId: user.impersonation?.staffUserId });
  return {
    orgId: membership.id,
    orgSlug: membership.slug,
    orgName: membership.name,
    userId: user.id,
    userEmail: user.email,
    emailVerified: user.emailVerified,
    role: membership.role,
    audit: await auditSourceFor(user),
    ...(user.impersonation && { impersonation: user.impersonation }),
  };
});

/**
 * Lesson 7.3: the request's audit source. A person acting for themselves is
 * the actor; during impersonation the actor is the STAFF member and the
 * customer is `onBehalfOf` ("Beacon support, on behalf of Ana"), so an
 * impersonated action can never look like the customer did it.
 */
async function auditSourceFor(user: CurrentUser): Promise<AuditSource> {
  // API routes: observeRequest() already read the request. Pages and server actions: Next's headers().
  const ctx = getContext();
  const h = ctx ? null : await requestHeaders();
  const where = {
    ip: ctx ? (ctx.ip ?? null) : h ? clientIpFrom(h) : null,
    userAgent: ctx ? (ctx.userAgent ?? null) : (h?.get('user-agent') ?? null),
    requestId: ctx?.requestId ?? (h ? requestIdFrom(h.get('x-request-id')) : null),
    via: 'app' as const,
  };
  if (user.impersonation) {
    return {
      actor: { type: 'staff', id: user.impersonation.staffUserId, name: null, email: user.impersonation.staffEmail },
      onBehalfOf: { id: user.id, name: user.name, email: user.email },
      ...where,
    };
  }
  return { actor: { type: 'user', id: user.id, name: user.name, email: user.email }, ...where };
}

/** The request's headers, or null outside a request (a script, a test). */
async function requestHeaders(): Promise<Headers | null> {
  try {
    return await headers();
  } catch {
    return null;
  }
}

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
  // Lesson 7.1: read-only impersonation. src/proxy.ts already refuses every
  // mutating request while the cookie is present; this is the second lock,
  // for anything that checks a write permission.
  if (ctx.impersonation?.readOnly && !isReadPermission(permission)) throw new AccessError('forbidden');
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
