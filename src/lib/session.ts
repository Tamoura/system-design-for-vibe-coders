import { cache } from 'react';
import { cookies, headers } from 'next/headers';
import { redirect } from 'next/navigation';
import { IMPERSONATION_COOKIE } from '@/core/staff';
import { auth } from './auth';
import { resolveImpersonation, type ImpersonationInfo } from './impersonation';

export type CurrentUser = {
  id: string;
  email: string;
  name: string;
  emailVerified: boolean;
  /** Lesson 7.1: set when Beacon staff are viewing the app AS this user (read-only, 30 minutes). */
  impersonation?: ImpersonationInfo;
};

/**
 * Lesson 1.1: who is signed in? Better Auth looks the session cookie up in
 * the `sessions` table on every call, so a deleted (logged-out) session is
 * rejected immediately. `cache` makes it one lookup per request.
 *
 * Lesson 7.1: this is always the REAL person at the keyboard. The staff area
 * (src/lib/staff.ts) uses it, so a staff member who is impersonating a
 * customer is still themselves in /internal.
 */
export const getSessionUser = cache(async (): Promise<CurrentUser | null> => {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) return null;
  const { id, email, name, emailVerified } = session.user;
  return { id, email, name, emailVerified };
});

/**
 * Who the APP should treat as the user: the signed-in person, or, while a
 * staff member impersonates (lesson 7.1), the customer they are viewing, with
 * `impersonation` set. The impersonation cookie only counts for the staff
 * member who started it, until it ends or expires (30 minutes, active or not).
 * Every page and route of the customer app goes through here, so they all see
 * the customer's orgs and roles, and the banner and the read-only rule apply.
 */
export const getCurrentUser = cache(async (): Promise<CurrentUser | null> => {
  const me = await getSessionUser();
  if (!me) return null;
  const token = (await cookies()).get(IMPERSONATION_COOKIE)?.value;
  if (!token) return me;
  const impersonated = await resolveImpersonation(me.id, token);
  return impersonated ?? me;
});

/** For pages: signed-out visitors are sent to /login and brought back afterwards. */
export async function requireUser(returnTo = '/dashboard'): Promise<CurrentUser> {
  const user = await getCurrentUser();
  if (!user) redirect(`/login?next=${encodeURIComponent(returnTo)}`);
  return user;
}

/**
 * Lesson 4.3: is the session behind these request headers still the one for
 * `userId`? A live stream is opened once and lives for hours, so it asks
 * again from time to time: signing out (or a password reset, which revokes
 * every session) then also ends the user's open streams. (Lesson 7.1: while
 * staff impersonate, `userId` is the customer and the session is the staff
 * member's, so the stream ends too; the banner's 30 minutes are short anyway.)
 */
export async function isSessionValid(requestHeaders: Headers, userId: string): Promise<boolean> {
  const session = await auth.api.getSession({ headers: requestHeaders });
  return session?.user.id === userId;
}
