import { notFound } from 'next/navigation';
import { getCurrentUser, type CurrentUser } from './session';

/*
 * Lesson 6.3: who may flip feature flags and read the activation funnel.
 * A deliberately small stand-in until Module 7 builds the real admin panel
 * (lesson 7.1: a separate `staff_users` table, staff roles, an audit log):
 * BEACON_STAFF_EMAILS, a comma-separated list, and a VERIFIED email.
 *
 * Anyone else gets a plain 404 on /internal/…, pages and actions alike, so
 * the area does not even admit it exists (like a foreign org, lesson 1.2).
 */
export function staffEmails(env: Record<string, string | undefined> = process.env): Set<string> {
  return new Set(
    (env.BEACON_STAFF_EMAILS ?? '')
      .split(',')
      .map((e) => e.trim().toLowerCase())
      .filter(Boolean),
  );
}

export function isStaff(user: Pick<CurrentUser, 'email' | 'emailVerified'> | null, env?: Record<string, string | undefined>): boolean {
  return Boolean(user?.emailVerified && staffEmails(env).has(user.email.toLowerCase()));
}

/** For /internal pages and their server actions: the staff member, or a 404. */
export async function requireStaff(): Promise<CurrentUser> {
  const user = await getCurrentUser();
  if (!user || !isStaff(user)) notFound();
  return user;
}
