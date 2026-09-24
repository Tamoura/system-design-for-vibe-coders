import { sql } from 'drizzle-orm';
import { selectRows, withOrg } from '@/db/tenant';
import { matchPages, parseHighlight, type SearchResult, type SnippetPart } from '@/core/search';
import type { Role } from '@/core/roles';
import type { OrgScope } from './monitors';

/*
 * Lesson 2.3: search inside Postgres, two rungs of the ladder.
 *
 *   monitors          pg_trgm on name and url: short strings, typos welcome
 *                     ("chekout" finds "checkout-api"), ranked by similarity
 *   incident updates  full-text search on a generated tsvector column: prose,
 *                     stemming ("expires" matches "expired"), web-style queries
 *                     ('"certificate expired" -staging'), ranking and
 *                     highlighted snippets
 *
 * The one rule: a search is a query on tenant data like any other. Both run
 * inside withOrg(), and the org comes from the server-side context, never
 * from anything the browser sends.
 *
 * The SQL itself lives in two functions, search_monitors() and
 * search_incident_updates(), in drizzle/0009_search.sql. Why not a Drizzle
 * query like everywhere else? Row-level security (lesson 2.4) stops Postgres
 * from using the trigram and full-text indexes for ordinary queries; those
 * functions are how the indexes and RLS work together. The migration explains
 * the details, and tests/search.test.ts proves they stay inside one org.
 */

export type MonitorHit = { id: string; name: string; url: string; score: number };

/** Monitors whose name or URL contains the query, or nearly does. Best matches first. */
export async function searchMonitors({ orgId }: OrgScope, query: string, limit = 20): Promise<MonitorHit[]> {
  const q = query.trim().slice(0, 100);
  if (!q) return [];
  const rows = await withOrg(orgId, (tx) =>
    selectRows<{ id: string; name: string; url: string; score: number }>(tx, sql`select * from search_monitors(${q}, ${limit})`),
  );
  return rows.map((r) => ({ ...r, score: Number(r.score) }));
}

export type IncidentHit = {
  updateId: string;
  incidentId: string;
  monitorId: string;
  monitorName: string;
  openedAt: Date;
  resolvedAt: Date | null;
  rank: number;
  snippet: SnippetPart[];
};

type IncidentRow = {
  update_id: string;
  incident_id: string;
  monitor_id: string;
  monitor_name: string;
  opened_at: Date | string;
  resolved_at: Date | string | null;
  rank: number;
  headline: string;
};

/**
 * Incident updates matching a web-search-style query: words are ANDed,
 * "quoted phrases" must appear together, -word excludes, "or" alternates.
 * websearch_to_tsquery never fails on odd input, so raw user text is fine.
 */
export async function searchIncidentUpdates({ orgId }: OrgScope, query: string, limit = 10): Promise<IncidentHit[]> {
  const q = query.trim().slice(0, 200);
  if (!q) return [];
  const rows = await withOrg(orgId, (tx) => selectRows<IncidentRow>(tx, sql`select * from search_incident_updates(${q}, ${limit})`));
  return rows.map((r) => ({
    updateId: r.update_id,
    incidentId: r.incident_id,
    monitorId: r.monitor_id,
    monitorName: r.monitor_name,
    openedAt: new Date(r.opened_at),
    resolvedAt: r.resolved_at === null ? null : new Date(r.resolved_at),
    rank: Number(r.rank),
    snippet: parseHighlight(r.headline),
  }));
}

/**
 * Lesson 2.3 (🟡): the cmd-K palette's single call — pages, monitors and
 * incidents together. The two database searches run in parallel.
 */
export async function searchEverything(ctx: OrgScope & { orgSlug: string; role: Role }, query: string): Promise<SearchResult[]> {
  const pages = matchPages(query, ctx.role, ctx.orgSlug);
  if (!query.trim()) return pages;
  const [monitorHits, incidentHits] = await Promise.all([searchMonitors(ctx, query, 8), searchIncidentUpdates(ctx, query, 8)]);
  const day = (d: Date) => d.toISOString().slice(0, 10);
  return [
    ...pages,
    ...monitorHits.map((m): SearchResult => ({
      type: 'monitor',
      id: m.id,
      title: m.name,
      subtitle: m.url,
      snippet: null,
      href: `/${ctx.orgSlug}/monitors/${m.id}`,
    })),
    ...incidentHits.map((i): SearchResult => ({
      type: 'incident',
      id: i.updateId,
      title: `${i.monitorName} incident, ${day(i.openedAt)}`,
      subtitle: i.resolvedAt ? 'resolved' : 'open',
      snippet: i.snippet,
      href: `/${ctx.orgSlug}/monitors/${i.monitorId}#incident-${i.incidentId}`,
    })),
  ];
}
