import type { Metadata } from 'next';
import Link from 'next/link';
import { getCurrentUser } from '@/lib/session';
import { signOutAction } from './(auth)/actions';
import './globals.css';

export const metadata: Metadata = {
  title: 'Beacon — uptime monitoring and status pages',
  description: 'The reference SaaS for the SaaS Building Blocks course.',
};

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const user = await getCurrentUser();
  return (
    <html lang="en">
      <body>
        <header className="top">
          <div className="wrap">
            <Link href="/" className="brand">◉ Beacon</Link>
            <nav>
              {user ? (
                <>
                  <Link href="/dashboard">Dashboard</Link>
                  <span className="muted">{user.email}</span>
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
        <main className="wrap">{children}</main>
      </body>
    </html>
  );
}
