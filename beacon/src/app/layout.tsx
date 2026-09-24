import type { Metadata } from 'next';
import Link from 'next/link';
import './globals.css';

export const metadata: Metadata = {
  title: 'Beacon — uptime monitoring and status pages',
  description: 'The reference SaaS for the SaaS Building Blocks course.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="top">
          <div className="wrap">
            <Link href="/" className="brand">◉ Beacon</Link>
            <nav>
              <Link href="/dashboard">Dashboard</Link>
              <Link href="/status">Status page</Link>
              {/* TODO(1.1): sign in / sign out. TODO(1.2): organization switcher. */}
            </nav>
          </div>
        </header>
        <main className="wrap">{children}</main>
      </body>
    </html>
  );
}
