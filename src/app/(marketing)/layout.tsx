import Link from 'next/link';

/**
 * Lesson 6.1: the MARKETING SITE's frame. Public, static, for visitors and
 * search engines: no session is read here (the pages declare
 * `dynamic = 'error'`, so a cookies() call would fail the build instead of
 * silently making them per-request). "Sign in" and "Start free" are plain links;
 * the app decides who you are.
 */

export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <header className="top">
        <div className="wrap">
          <Link href="/" className="brand">◉ Beacon</Link>
          <nav aria-label="Site">
            <Link href="/pricing">Pricing</Link>
            <Link href="/status/demo">Example status page</Link>
            <Link href="/login">Sign in</Link>
            <Link href="/signup" className="btn">Start free</Link>
          </nav>
        </div>
      </header>
      <main id="main" className="wrap">{children}</main>
      <footer className="wrap muted marketing-footer">
        © Beacon · <Link href="/pricing">Pricing</Link> · <Link href="/docs/api">API reference</Link> · Uptime monitoring and status pages for teams.
      </footer>
    </>
  );
}
