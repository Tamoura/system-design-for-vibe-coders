import Link from 'next/link';
import { getCurrentUser } from '@/lib/session';
import { signOutAction } from '@/app/(auth)/actions';

/**
 * The header of the pages outside an organization: sign-in, sign-up, account
 * settings, invitations, "new organization". It reads the session, so these
 * pages render per request (unlike the marketing site).
 */
export async function SiteHeader() {
  const user = await getCurrentUser();
  return (
    <header className="top">
      <div className="wrap">
        <Link href={user ? '/dashboard' : '/'} className="brand">◉ Beacon</Link>
        <nav aria-label="Account">
          {user ? (
            <>
              <Link href="/dashboard">Dashboard</Link>
              <Link href="/settings/account" className="muted">{user.email}</Link>
              {/* Lesson 1.1: a real logout is a POST that deletes the session server-side. */}
              <form action={signOutAction}>
                <button className="link-btn">Sign out</button>
              </form>
            </>
          ) : (
            <>
              <Link href="/login">Sign in</Link>
              <Link href="/signup">Sign up</Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}

/** Header + main, for the (auth) and (site) route groups. */
export function SiteFrame({ children }: { children: React.ReactNode }) {
  return (
    <>
      <SiteHeader />
      <main id="main" className="wrap">{children}</main>
    </>
  );
}
