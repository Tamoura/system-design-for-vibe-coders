import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Beacon — uptime monitoring and status pages',
  description: 'Beacon checks your URLs, opens an incident when they fail, and keeps a public status page up to date.',
};

/**
 * Lesson 6.1: the root layout is only the document. Each part of Beacon has
 * its own frame, because they have opposite needs:
 *
 *   (marketing)/   the public site: landing and pricing. Static HTML, no
 *                  session read, cookieless web analytics. For visitors and search engines.
 *   (auth)/, (site)/  sign-in, sign-up, account settings, invitations: a simple header.
 *   [orgSlug]/     the APP SHELL: sidebar, org switcher, onboarding. Signed in,
 *                  the org in the URL, never indexed.
 *   status/        the customer's public status page: their brand, not Beacon's app.
 *   internal/      Beacon staff tools (flags, the activation funnel).
 *
 * In a bigger team the marketing site is its own app (next-forge's apps/web)
 * or a CMS, deployed separately; route groups give the same split in one app.
 */
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {/* Lesson 6.1 (a11y): the first Tab stop jumps over the navigation. */}
        <a href="#main" className="skip-link">Skip to content</a>
        {children}
      </body>
    </html>
  );
}
