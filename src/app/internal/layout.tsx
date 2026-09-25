import Link from 'next/link';
import { requireStaff } from '@/lib/staff';

export const metadata = { robots: { index: false } };

/** Lesson 6.3: Beacon's own tools, for staff only (src/lib/staff.ts). Module 7 turns this into the admin panel. */
export default async function InternalLayout({ children }: { children: React.ReactNode }) {
  const staff = await requireStaff();
  return (
    <>
      <div className="internal-banner">Beacon staff area · {staff.email} · changes here affect every customer</div>
      <header className="top">
        <div className="wrap">
          <Link href="/internal/flags" className="brand">◉ Beacon internal</Link>
          <nav aria-label="Internal">
            <Link href="/internal/flags">Feature flags</Link>
            <Link href="/internal/analytics">Activation funnel</Link>
            <Link href="/dashboard">Back to the app</Link>
          </nav>
        </div>
      </header>
      <main id="main" className="wrap">{children}</main>
    </>
  );
}
