import Link from 'next/link';
import { forPage, requireMembership } from '@/lib/access';

/**
 * Lesson 1.2: everything under /[orgSlug] belongs to one organization. This
 * layout draws the org's navigation; each page still runs its own access
 * check, because a layout is not re-run for every request and server actions
 * never pass through it.
 */
export default async function OrgLayout({ children, params }: { children: React.ReactNode; params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requireMembership(orgSlug), `/${orgSlug}/monitors`);
  return (
    <div className="grid" style={{ gap: '1.4rem' }}>
      <nav className="org-nav row">
        <strong>{ctx.orgName}</strong>
        <span className="badge">{ctx.role}</span>
        <Link href={`/${ctx.orgSlug}/monitors`}>Monitors</Link>
        <Link href={`/status/${ctx.orgSlug}`}>Status page</Link>
      </nav>
      {children}
    </div>
  );
}
