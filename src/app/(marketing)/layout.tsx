import Link from 'next/link';
import Script from 'next/script';

/**
 * Lesson 6.1: the MARKETING SITE's frame. Public, static, for visitors and
 * search engines: no session is read here (the pages declare
 * `dynamic = 'error'`, so a cookies() call would fail the build instead of
 * silently making them per-request). "Sign in" and "Start free" are plain links;
 * the app decides who you are.
 *
 * Lesson 6.2 (🟢): cookieless web analytics on the marketing site ONLY.
 * Plausible (or Umami) counts visits without a cookie or any other storage on
 * the visitor's device (a daily-salted hash of IP + user agent, server side),
 * so no consent banner is needed here. Set NEXT_PUBLIC_PLAUSIBLE_DOMAIN to
 * turn it on (and NEXT_PUBLIC_PLAUSIBLE_SRC for a self-hosted Plausible).
 * The app itself never loads it: product analytics there is server-side (src/lib/analytics).
 */
const plausibleDomain = process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN;
const plausibleSrc = process.env.NEXT_PUBLIC_PLAUSIBLE_SRC || 'https://plausible.io/js/script.js';

export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {plausibleDomain && <Script defer data-domain={plausibleDomain} src={plausibleSrc} strategy="afterInteractive" />}
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
        © Beacon · <Link href="/pricing">Pricing</Link> · <Link href="/trust">Trust</Link> · <Link href="/docs/api">API reference</Link> · Uptime monitoring and status pages for teams.
      </footer>
    </>
  );
}
