import { and, desc, eq, isNull, sql as dsql } from 'drizzle-orm';
import { db, schema } from '@/db';
import { uptimeFromCounts } from '@/core/incidents';
import { canEditMonitor, type Actor } from '@/core/permissions';
import type { CreateMonitorInput, UpdateMonitorInput } from '@/core/validation';
import { AccessError } from './errors';

const { monitors, checkResults, incidents } = schema;

/*
 * Lesson 1.2: every function here takes the organization it works inside and
 * puts `organization_id = …` into every WHERE clause. There is deliberately no
 * way to ask for "monitor 123" without saying which org you are in, so a
 * monitor from another tenant simply does not exist for these queries.
 */
export type OrgScope = { orgId: string };

export type MonitorView = {
  id: string;
  name: string;
  url: string;
  intervalSeconds: number;
  paused: boolean;
  state: 'up' | 'down' | 'unknown';
  lastCheckedAt: Date | null;
  lastLatencyMs: number | null;
  uptime24h: number | null;
  openIncident: { id: string; openedAt: Date; cause: string } | null;
};

/** The monitor rows of one organization, without check data (for the API). */
export async function listMonitorRows({ orgId }: OrgScope) {
  return db.select().from(monitors).where(eq(monitors.organizationId, orgId)).orderBy(monitors.createdAt);
}

/**
 * Every monitor in one organization, with its latest state.
 *
 * Lesson 2.1 (🟡): ONE query, however many monitors the org has. The first
 * version ran one query for the list plus two per monitor (an N+1: 401 queries
 * for 200 monitors). Here each monitor row is joined to three small LATERAL
 * subqueries, which Postgres runs per monitor *inside the database*, each one
 * an index lookup:
 *
 *   latest check      → check_results_monitor_time_idx, first entry
 *   last 24h counts   → the same index, a range scan
 *   open incident     → incidents_open_idx (partial: open incidents only)
 *
 * `EXPLAIN ANALYZE` of this query shows index scans only; see docs/SOLUTIONS.md.
 */
export async function listMonitors({ orgId }: OrgScope): Promise<MonitorView[]> {
  const latest = db
    .select({ ok: checkResults.ok, checkedAt: checkResults.checkedAt, latencyMs: checkResults.latencyMs })
    .from(checkResults)
    .where(and(eq(checkResults.organizationId, orgId), eq(checkResults.monitorId, monitors.id)))
    .orderBy(desc(checkResults.checkedAt))
    .limit(1)
    .as('latest');
  const day = db
    .select({
      total: dsql<number>`count(*)::int`.as('total'),
      up: dsql<number>`(count(*) filter (where ${checkResults.ok}))::int`.as('up'),
    })
    .from(checkResults)
    .where(
      and(
        eq(checkResults.organizationId, orgId),
        eq(checkResults.monitorId, monitors.id),
        dsql`${checkResults.checkedAt} > now() - interval '24 hours'`,
      ),
    )
    .as('day');
  const open = db
    .select({ id: incidents.id, openedAt: incidents.openedAt, cause: incidents.cause })
    .from(incidents)
    .where(and(eq(incidents.organizationId, orgId), eq(incidents.monitorId, monitors.id), isNull(incidents.resolvedAt)))
    .orderBy(desc(incidents.openedAt))
    .limit(1)
    .as('open_incident');

  const rows = await db
    .select({
      monitor: monitors,
      latestOk: latest.ok,
      latestAt: latest.checkedAt,
      latestLatencyMs: latest.latencyMs,
      checks24h: day.total,
      up24h: day.up,
      openId: open.id,
      openedAt: open.openedAt,
      openCause: open.cause,
    })
    .from(monitors)
    .leftJoinLateral(latest, dsql`true`)
    .leftJoinLateral(day, dsql`true`)
    .leftJoinLateral(open, dsql`true`)
    .where(eq(monitors.organizationId, orgId))
    .orderBy(monitors.createdAt);

  return rows.map(({ monitor: m, ...r }) => ({
    id: m.id,
    name: m.name,
    url: m.url,
    intervalSeconds: m.intervalSeconds,
    paused: m.paused,
    state: r.latestOk === null ? 'unknown' : r.latestOk ? 'up' : 'down',
    lastCheckedAt: r.latestAt,
    lastLatencyMs: r.latestLatencyMs,
    uptime24h: uptimeFromCounts(r.up24h ?? 0, r.checks24h ?? 0),
    openIncident: r.openId && r.openedAt && r.openCause !== null ? { id: r.openId, openedAt: r.openedAt, cause: r.openCause } : null,
  }));
}

/**
 * One monitor, only if it belongs to this organization. Lesson 1.3: this is
 * the object-level check that stops IDOR — the org id is part of the query.
 */
export async function getMonitor({ orgId }: OrgScope, id: string) {
  if (!isUuid(id)) return null; // a malformed id cannot exist; don't let Postgres throw on it
  const [row] = await db
    .select()
    .from(monitors)
    .where(and(eq(monitors.organizationId, orgId), eq(monitors.id, id)))
    .limit(1);
  return row ?? null;
}

/** The latest check results and incidents for one monitor, for its detail page. */
export async function getMonitorHistory({ orgId }: OrgScope, monitorId: string) {
  const checks = await db
    .select()
    .from(checkResults)
    .where(and(eq(checkResults.organizationId, orgId), eq(checkResults.monitorId, monitorId)))
    .orderBy(desc(checkResults.checkedAt))
    .limit(20);
  const recentIncidents = await db
    .select()
    .from(incidents)
    .where(and(eq(incidents.organizationId, orgId), eq(incidents.monitorId, monitorId)))
    .orderBy(desc(incidents.openedAt))
    .limit(10);
  return { checks, incidents: recentIncidents };
}

/**
 * The org and the author come from the server-side context, never from the
 * request body: `input` has been parsed by an allow-list schema that has no
 * organizationId field (lesson 1.3, mass assignment).
 */
export async function createMonitor(ctx: OrgScope & { userId: string }, input: CreateMonitorInput) {
  // TODO(3.2): enforce the plan's monitor limit.
  // TODO(7.3): record "monitor.created" in the audit log.
  const [row] = await db
    .insert(monitors)
    .values({ ...input, organizationId: ctx.orgId, createdBy: ctx.userId })
    .returning();
  return row;
}

/**
 * Load a monitor the actor may change. Lesson 1.3: two checks, in this order —
 * object-level (is it in this org? else 404) then the ABAC rule (may this
 * actor edit *this* monitor? else 403).
 */
async function getEditableMonitor(ctx: OrgScope & Actor, id: string) {
  const monitor = await getMonitor(ctx, id);
  if (!monitor) throw new AccessError('not_found');
  if (!canEditMonitor(ctx, monitor)) throw new AccessError('forbidden');
  return monitor;
}

export async function updateMonitor(ctx: OrgScope & Actor, id: string, input: UpdateMonitorInput) {
  await getEditableMonitor(ctx, id);
  // TODO(7.3): record "monitor.updated" in the audit log.
  const [row] = await db
    .update(monitors)
    .set(input) // parsed by updateMonitorInput: only name, url, intervalSeconds, paused
    .where(and(eq(monitors.organizationId, ctx.orgId), eq(monitors.id, id)))
    .returning();
  return row;
}

export async function deleteMonitor(ctx: OrgScope & Actor, id: string): Promise<void> {
  await getEditableMonitor(ctx, id);
  // TODO(7.3): record "monitor.deleted" in the audit log.
  await db.delete(monitors).where(and(eq(monitors.organizationId, ctx.orgId), eq(monitors.id, id)));
}

/** Mark an open incident as resolved by hand (the checker also resolves it on the next success). */
export async function resolveIncident({ orgId }: OrgScope, incidentId: string): Promise<boolean> {
  if (!isUuid(incidentId)) return false;
  const updated = await db
    .update(incidents)
    .set({ resolvedAt: new Date() })
    .where(and(eq(incidents.organizationId, orgId), eq(incidents.id, incidentId), isNull(incidents.resolvedAt)))
    .returning({ id: incidents.id });
  return updated.length > 0;
}

export function isUuid(value: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value);
}
