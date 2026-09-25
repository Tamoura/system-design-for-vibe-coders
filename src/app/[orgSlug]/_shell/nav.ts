import { can, type Permission } from '@/core/permissions';
import type { Role } from '@/core/roles';

/*
 * Lesson 6.1: the app shell's navigation, as data. The sidebar shows the
 * items the viewer's role may open (the same can() the pages enforce: hiding
 * a link is a courtesy, the page still answers 403), and the org switcher
 * uses it to keep you on the same section when you switch org.
 *
 * Settings come in kinds with different owners (lesson 6.1 🟡):
 *   organization  General (name), Members           /[org]/settings/general, /[org]/members
 *   billing       plan, payment, invoices           /[org]/billing
 *   alerts        Slack, policy, escalation         /[org]/settings/notifications
 *   developer     API keys, webhooks                /[org]/settings/api-keys, …/webhooks
 *   account       the USER's own settings, across orgs: /settings/account (not under an org)
 */
export type NavItem = { section: string; label: string; permission: Permission };
export type NavGroup = { label: string | null; items: NavItem[] };

export const NAV: NavGroup[] = [
  {
    label: null,
    items: [
      { section: 'monitors', label: 'Monitors', permission: 'monitor.read' },
      { section: 'incidents', label: 'Incidents', permission: 'monitor.read' },
      { section: 'status-page', label: 'Status page', permission: 'monitor.read' },
    ],
  },
  {
    label: 'Organization',
    items: [
      { section: 'settings/general', label: 'General', permission: 'member.read' },
      { section: 'members', label: 'Members', permission: 'member.read' },
      { section: 'billing', label: 'Billing', permission: 'billing.manage' },
      { section: 'settings/notifications', label: 'Alert channels', permission: 'notification.manage' },
      { section: 'settings/escalation', label: 'Escalation', permission: 'notification.manage' },
      // Lesson 7.3 (🟡): owners and admins. The page itself shows an upgrade prompt on Free.
      { section: 'settings/audit-log', label: 'Audit log', permission: 'audit.read' },
      // Lesson 8.2: the AI opt-in (the page shows an upgrade prompt on plans without it).
      { section: 'settings/ai', label: 'AI summaries', permission: 'org.manage' },
      // Lesson 8.1: export and deletion (GDPR), owners only.
      { section: 'settings/data', label: 'Data & privacy', permission: 'org.export' },
    ],
  },
  {
    label: 'Developer',
    items: [
      { section: 'settings/api-keys', label: 'API keys', permission: 'integration.manage' },
      { section: 'settings/webhooks', label: 'Webhooks', permission: 'integration.manage' },
    ],
  },
];

export function navFor(role: Role): NavGroup[] {
  return NAV.map((g) => ({ ...g, items: g.items.filter((i) => can(role, i.permission)) })).filter((g) => g.items.length > 0);
}

/**
 * Lesson 6.1 (🟢): where the org switcher sends you. The org is the first URL
 * segment, so switching org means changing that segment: /acme/incidents →
 * /globex/incidents. Deep links (a monitor's id) do not exist in the other
 * org, so only the section is kept, and only if your role there may open it.
 */
export function switchOrgHref(pathname: string, targetSlug: string, targetRole: Role): string {
  const rest = pathname.split('/').slice(2);
  const candidates = [rest.slice(0, 2).join('/'), rest[0] ?? ''];
  const item = NAV.flatMap((g) => g.items).find((i) => candidates.includes(i.section));
  const section = item && can(targetRole, item.permission) ? item.section : 'monitors';
  return `/${targetSlug}/${section}`;
}
