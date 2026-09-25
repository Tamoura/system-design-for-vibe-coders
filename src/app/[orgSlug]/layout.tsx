import Link from 'next/link';
import { forPage, requireMembership } from '@/lib/access';
import { listOrganizationsForUser } from '@/lib/organizations';
import { countUnread } from '@/lib/notifications';
import { signOutAction } from '@/app/(auth)/actions';
import { CommandPalette } from './command-palette';
import { NotificationBell } from './notification-bell';
import { LiveStatus, RealtimeProvider } from './realtime';
import { navFor } from './_shell/nav';
import { OrgSwitcher } from './_shell/org-switcher';
import { SidebarNav } from './_shell/sidebar-nav';

export const metadata = { robots: { index: false } }; // lesson 6.1: the app is never indexed

/**
 * Lesson 6.1 (🟢): the APP SHELL, the frame around every page of an org.
 *
 *   ┌ sidebar ─────────┬ top bar: ⌘K search · 🔔 · live ────────────┐
 *   │ ◉ Beacon         │                                            │
 *   │ [Acme ▾] switcher│   the page                                  │
 *   │ Monitors …       │                                            │
 *   │ Organization …   │                                            │
 *   │ you · sign out   │                                            │
 *   └──────────────────┴────────────────────────────────────────────┘
 *
 * Lesson 1.2: everything under /[orgSlug] belongs to one organization, taken
 * from the URL and checked against the membership on every request. This
 * layout draws the frame; each page still runs its own access check, because
 * a layout is not re-run for every request and server actions never pass through it.
 */
export default async function OrgLayout({ children, params }: { children: React.ReactNode; params: Promise<{ orgSlug: string }> }) {
  const { orgSlug } = await params;
  const ctx = await forPage(requireMembership(orgSlug), `/${orgSlug}/monitors`);
  const orgs = await listOrganizationsForUser(ctx.userId);
  const unread = await countUnread(ctx); // lesson 4.2: the bell
  // Lesson 4.3: one live connection (SSE) for every page of this org, shared by the components below.
  return (
    <RealtimeProvider orgSlug={ctx.orgSlug}>
      <div className="shell">
        <aside className="sidebar">
          <Link href={`/${ctx.orgSlug}/monitors`} className="brand">◉ Beacon</Link>
          <OrgSwitcher current={{ slug: ctx.orgSlug, name: ctx.orgName, role: ctx.role }} orgs={orgs.map((o) => ({ slug: o.slug, name: o.name, role: o.role }))} />
          <SidebarNav orgSlug={ctx.orgSlug} groups={navFor(ctx.role)} />
          <div className="sidebar-user">
            <Link href="/settings/account" title="Your account settings">{ctx.userEmail}</Link>
            <Link href={`/${ctx.orgSlug}/notifications/preferences`} className="muted">My alert preferences</Link>
            {/* Lesson 1.1: a real logout is a POST that deletes the session server-side. */}
            <form action={signOutAction}>
              <button className="link-btn">Sign out</button>
            </form>
          </div>
        </aside>
        <div className="shell-main">
          <header className="topbar">
            {/* Lesson 2.3 (🟡): Ctrl+K / ⌘K search across monitors, incidents and pages. */}
            <CommandPalette orgSlug={ctx.orgSlug} />
            {/* Lesson 4.2 (🟢): the in-app inbox, with the unread count (live since 4.3). */}
            <NotificationBell orgSlug={ctx.orgSlug} unread={unread} />
            <LiveStatus />
          </header>
          <main id="main" className="shell-content">{children}</main>
        </div>
      </div>
    </RealtimeProvider>
  );
}
