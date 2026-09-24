import { cache } from 'react';
import { headers } from 'next/headers';
import { redirect } from 'next/navigation';
import { auth } from './auth';

export type CurrentUser = { id: string; email: string; name: string; emailVerified: boolean };

/**
 * Lesson 1.1: who is making this request? Better Auth looks the session cookie
 * up in the `sessions` table on every call, so a deleted (logged-out) session
 * is rejected immediately. `cache` makes it one lookup per request.
 */
export const getCurrentUser = cache(async (): Promise<CurrentUser | null> => {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) return null;
  const { id, email, name, emailVerified } = session.user;
  return { id, email, name, emailVerified };
});

/** For pages: signed-out visitors are sent to /login and brought back afterwards. */
export async function requireUser(returnTo = '/dashboard'): Promise<CurrentUser> {
  const user = await getCurrentUser();
  if (!user) redirect(`/login?next=${encodeURIComponent(returnTo)}`);
  return user;
}
