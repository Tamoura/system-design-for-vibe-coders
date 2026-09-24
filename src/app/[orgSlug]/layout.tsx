import Link from 'next/link';
import { can } from '@/core/permissions';
import { forPage, requireMembership } from '@/lib/access';
import { listOrganizationsForUser } from '@/lib/organizations';
import { CommandPalette } from './command-palette';

/**
 * Lesson 1.2: everything under /[orgSlug] belongs to one organization. This
 * layout draws the org's navigation; each page still runs its own access
 * check, because a layout is not re-run for every request and server actions
 * never pass through it.
 */
export default async function OrgLayout({ children, params }: { children: React.ReactNode; params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requireMembership(orgSlug), `/${orgSlug}/monitors`);
  const orgs = await listOrganizationsForUser(ctx.userId);
  return (
    <div className="grid" style={{ gap: '1.4rem' }}>
      <nav className="org-nav row">
        {/* Lesson 1.2 (🟡): the org switcher lists every org the user belongs to. */}
        <details className="switcher">
          <summary><strong>{ctx.orgName}</strong></summary>
          <div className="card switcher-menu">
            {orgs.map((o) => (
              <Link key={o.id} href={`/${o.slug}/monitors`}>
                {o.name} <span className="muted">· {o.role}</span>
              </Link>
            ))}
            <Link href="/orgs/new">+ New organization</Link>
          </div>
        </details>
        <span className="badge">{ctx.role}</span>
        <Link href={`/${ctx.orgSlug}/monitors`}>Monitors</Link>
        <Link href={`/${ctx.orgSlug}/members`}>Members</Link>
        <Link href={`/status/${ctx.orgSlug}`}>Status page</Link>
        {can(ctx.role, 'page.publish') && <Link href={`/${ctx.orgSlug}/settings`}>Settings</Link>}
        {/* Lesson 3.1: only roles that may manage billing see it (the page checks again). */}
        {can(ctx.role, 'billing.manage') && <Link href={`/${ctx.orgSlug}/billing`}>Billing</Link>}
        {/* Lesson 2.3 (🟡): Ctrl+K / ⌘K search across monitors, incidents and pages. */}
        <CommandPalette orgSlug={ctx.orgSlug} />
      </nav>
      {children}
    </div>
  );
}
