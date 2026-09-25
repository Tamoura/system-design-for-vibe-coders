import Link from 'next/link';
import { staffCan } from '@/core/staff';
import { requireStaff } from '@/lib/staff';

export const metadata = { robots: { index: false } };

/**
 * Lesson 7.1: the admin panel, Beacon's back office. Staff only
 * (src/lib/staff.ts): everyone else gets a 404 here, customers of every role
 * included. The links shown depend on the staff ROLE; the pages and routes
 * check the same permissions again (a hidden link is not a security control).
 *
 * In production this is its own hostname (admin.beacon.internal) behind an
 * identity-aware proxy and the company IdP with MFA (docs/SOLUTIONS.md).
 */
export default async function InternalLayout({ children }: { children: React.ReactNode }) {
  const staff = await requireStaff();
  return (
    <>
      <div className="internal-banner" data-testid="staff-banner">
        Beacon staff area · {staff.email} ({staff.role}) · every write here needs a reason and is audited
      </div>
      <header className="top">
        <div className="wrap">
          <Link href="/internal" className="brand">◉ Beacon admin</Link>
          <nav aria-label="Internal">
            <Link href="/internal">Customers</Link>
            {staffCan(staff.role, 'audit.read') && <Link href="/internal/audit">Audit log</Link>}
            {staffCan(staff.role, 'staff.manage') && <Link href="/internal/staff">Staff</Link>}
            {staffCan(staff.role, 'flags.manage') && <Link href="/internal/flags">Feature flags</Link>}
            <Link href="/internal/analytics">Activation funnel</Link>
            <Link href="/dashboard">Back to the app</Link>
          </nav>
        </div>
      </header>
      <main id="main" className="wrap">{children}</main>
    </>
  );
}
