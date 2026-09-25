import Link from 'next/link';

/**
 * The public status page belongs to the CUSTOMER (their customers read it),
 * so it has no Beacon app chrome: the org's logo and name, and a small
 * "Powered by Beacon" link. Custom domains (status.acme.com) are lesson 6.1's
 * 🔴 exercise; see docs/SOLUTIONS.md, Module 6.
 */
export default function StatusLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <main id="main" className="wrap">{children}</main>
      <footer className="wrap muted status-footer">
        Powered by <Link href="/">Beacon</Link>
      </footer>
    </>
  );
}
