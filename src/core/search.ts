import { can, type Permission } from './permissions';
import type { Role } from './roles';

/*
 * Lesson 2.3: the pure parts of search. The SQL lives in src/lib/search.ts.
 */

export type SearchResultType = 'monitor' | 'incident' | 'page';

/** A piece of a highlighted snippet. `hit` pieces are the matched words. */
export type SnippetPart = { text: string; hit: boolean };

export type SearchResult = {
  type: SearchResultType;
  id: string;
  title: string;
  subtitle: string;
  snippet: SnippetPart[] | null;
  href: string;
};

/*
 * ts_headline marks matches with StartSel/StopSel. search_incident_updates()
 * (drizzle/0009_search.sql) asks for two characters that never appear in
 * normal text, and we split on them, instead of asking for "<b>…</b>" and
 * rendering HTML: the snippet is user text (an incident update), and
 * inserting it as HTML would be stored XSS.
 */
export const HIGHLIGHT_START = '⟦';
export const HIGHLIGHT_STOP = '⟧';

export function parseHighlight(snippet: string): SnippetPart[] {
  const parts: SnippetPart[] = [];
  for (const chunk of snippet.split(HIGHLIGHT_START)) {
    const stop = chunk.indexOf(HIGHLIGHT_STOP);
    if (stop === -1) {
      if (chunk) parts.push({ text: chunk, hit: false });
      continue;
    }
    if (stop > 0) parts.push({ text: chunk.slice(0, stop), hit: true });
    const rest = chunk.slice(stop + HIGHLIGHT_STOP.length);
    if (rest) parts.push({ text: rest, hit: false });
  }
  return parts;
}

/*
 * The "settings pages" of the cmd-K palette: places to go, not rows in the
 * database. Each carries the permission the page itself checks, so the
 * palette never offers a page that would answer 403.
 */
type Page = { title: string; keywords: string; path: (org: string) => string; permission?: Permission };

export const PAGES: Page[] = [
  { title: 'Monitors', keywords: 'dashboard checks uptime getting started onboarding', path: (o) => `/${o}/monitors`, permission: 'monitor.read' },
  { title: 'Add a monitor', keywords: 'new create url check', path: (o) => `/${o}/monitors/new`, permission: 'monitor.write' },
  // Lesson 6.1: the app shell's sections and the settings split (organization, billing, developer).
  { title: 'Incidents', keywords: 'outages open resolved', path: (o) => `/${o}/incidents`, permission: 'monitor.read' },
  { title: 'Status page', keywords: 'status page public publish logo', path: (o) => `/${o}/status-page`, permission: 'page.publish' },
  { title: 'Members', keywords: 'team people users roles invite', path: (o) => `/${o}/members`, permission: 'member.read' },
  { title: 'Settings', keywords: 'organization general name rename', path: (o) => `/${o}/settings/general`, permission: 'org.manage' },
  { title: 'Alert channels', keywords: 'settings notifications slack policy escalation', path: (o) => `/${o}/settings/notifications`, permission: 'notification.manage' },
  { title: 'Billing', keywords: 'settings plan upgrade invoices payment', path: (o) => `/${o}/billing`, permission: 'billing.manage' },
  { title: 'API keys', keywords: 'settings developer api integration', path: (o) => `/${o}/settings/api-keys`, permission: 'integration.manage' },
  { title: 'Webhooks', keywords: 'settings developer integration events', path: (o) => `/${o}/settings/webhooks`, permission: 'integration.manage' },
  { title: 'Public status page', keywords: 'status page public', path: (o) => `/status/${o}` },
  { title: 'Your account', keywords: 'profile password github sign out', path: () => '/settings/account' },
  { title: 'New organization', keywords: 'create workspace team', path: () => '/orgs/new' },
];

/**
 * Pages whose title or keywords contain every word of the query as a word
 * prefix ("mem" finds Members, "status pub" finds the public status page).
 * An empty query lists them all: the palette's "navigation" section.
 */
export function matchPages(query: string, role: Role, orgSlug: string, limit = 5): SearchResult[] {
  const words = query.toLowerCase().split(/\s+/).filter(Boolean);
  return PAGES.filter((page) => !page.permission || can(role, page.permission))
    .filter((page) => {
      const haystack = `${page.title} ${page.keywords}`.toLowerCase().split(/\s+/);
      return words.every((w) => haystack.some((h) => h.startsWith(w)));
    })
    .slice(0, limit)
    .map((page) => ({ type: 'page', id: page.path(orgSlug), title: page.title, subtitle: page.path(orgSlug), snippet: null, href: page.path(orgSlug) }));
}
