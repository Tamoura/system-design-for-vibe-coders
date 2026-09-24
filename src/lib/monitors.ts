import { and, desc, eq, isNull, sql as dsql } from 'drizzle-orm';
import { schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { uptimeFromCounts } from '@/core/incidents';
import { canEditMonitor, type Actor } from '@/core/permissions';
import { isUuid, type CreateMonitorInput, type UpdateMonitorInput } from '@/core/validation';
import { assertCanCreateMonitor, assertCanRunAnotherMonitor, assertIntervalAllowed, entitlementsInTx } from './entitlements';
import { BlockedUrlError, assertPublicUrl } from '@/core/safe-fetch';
import { AccessError, InvalidRequestError } from './errors';
import { enqueueNotify } from './notifications/incidents';
import { publishInTx } from './realtime';

const { monitors, checkResults, incidents } = schema;

/*
 * Lesson 1.2: every function here takes the organization it works inside and
 * puts `organization_id = …` into every WHERE clause. There is deliberately no
 * way to ask for "monitor 123" without saying which org you are in, so a
 * monitor from another tenant simply does not exist for these queries.
 *
 * Lesson 2.4: and every query runs inside withOrg(orgId), so Postgres
 * row-level security enforces the same filter a second time. Together they
 * are the lesson's `forOrg(orgId)`: the only way to reach tenant tables.
 */
export type OrgScope = { orgId: string };

export type MonitorView = {
  id: string;
  name: string;
  url: string;
  intervalSeconds: number;
  paused: boolean;
  pausedReason: 'manual' | 'plan_limit' | null;
  state: 'up' | 'down' | 'unknown';
  lastCheckedAt: Date | null;
  lastLatencyMs: number | null;
  uptime24h: number | null;
  openIncident: { id: string; openedAt: Date; cause: string } | null;
};

/** The monitor rows of one organization, without check data (for the API). */
export async function listMonitorRows({ orgId }: OrgScope) {
  return withOrg(orgId, (tx) => tx.select().from(monitors).where(eq(monitors.organizationId, orgId)).orderBy(monitors.createdAt));
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
 *   latest check      → check_results_org_monitor_time_idx, last entry
 *   last 24h counts   → the same index, a range scan (index-only)
 *   open incident     → incidents_open_idx (partial: open incidents only)
 *
 * `EXPLAIN ANALYZE` of this query shows index scans only; see docs/SOLUTIONS.md.
 * The query count stays constant too: tests/data-layer.test.ts counts them.
 */
export async function listMonitors({ orgId }: OrgScope): Promise<MonitorView[]> {
  return withOrg(orgId, async (tx) => {
    const latest = tx
      .select({ ok: checkResults.ok, checkedAt: checkResults.checkedAt, latencyMs: checkResults.latencyMs })
      .from(checkResults)
      .where(and(eq(checkResults.organizationId, orgId), eq(checkResults.monitorId, monitors.id)))
      .orderBy(desc(checkResults.checkedAt))
      .limit(1)
      .as('latest');
    const day = tx
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
    const open = tx
      .select({ id: incidents.id, openedAt: incidents.openedAt, cause: incidents.cause })
      .from(incidents)
      .where(and(eq(incidents.organizationId, orgId), eq(incidents.monitorId, monitors.id), isNull(incidents.resolvedAt)))
      .orderBy(desc(incidents.openedAt))
      .limit(1)
      .as('open_incident');

    const rows = await tx
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
      pausedReason: m.pausedReason,
      state: r.latestOk === null ? 'unknown' : r.latestOk ? 'up' : 'down',
      lastCheckedAt: r.latestAt,
      lastLatencyMs: r.latestLatencyMs,
      uptime24h: uptimeFromCounts(r.up24h ?? 0, r.checks24h ?? 0),
      openIncident: r.openId && r.openedAt && r.openCause !== null ? { id: r.openId, openedAt: r.openedAt, cause: r.openCause } : null,
    }));
  });
}

/**
 * One monitor, only if it belongs to this organization. Lesson 1.3: this is
 * the object-level check that stops IDOR — the org id is part of the query.
 */
export async function getMonitor({ orgId }: OrgScope, id: string) {
  if (!isUuid(id)) return null; // a malformed id cannot exist; don't let Postgres throw on it
  const [row] = await withOrg(orgId, (tx) =>
    tx
      .select()
      .from(monitors)
      .where(and(eq(monitors.organizationId, orgId), eq(monitors.id, id)))
      .limit(1),
  );
  return row ?? null;
}

/** The latest check results and incidents for one monitor, for its detail page. */
export async function getMonitorHistory({ orgId }: OrgScope, monitorId: string) {
  return withOrg(orgId, async (tx) => {
    const checks = await tx
      .select()
      .from(checkResults)
      .where(and(eq(checkResults.organizationId, orgId), eq(checkResults.monitorId, monitorId)))
      .orderBy(desc(checkResults.checkedAt))
      .limit(20);
    const recentIncidents = await tx
      .select()
      .from(incidents)
      .where(and(eq(incidents.organizationId, orgId), eq(incidents.monitorId, monitorId)))
      .orderBy(desc(incidents.openedAt))
      .limit(10);
    return { checks, incidents: recentIncidents };
  });
}

/**
 * The org and the author come from the server-side context, never from the
 * request body: `input` has been parsed by an allow-list schema that has no
 * organizationId field (lesson 1.3, mass assignment).
 */
export async function createMonitor(ctx: OrgScope & { userId: string | null }, input: CreateMonitorInput) {
  await assertMonitorUrl(input.url);
  // TODO(7.3): record "monitor.created" in the audit log.
  return withOrg(ctx.orgId, async (tx) => {
    // Lesson 3.2: entitlements are enforced here, on the server, at the point
    // of action. The form, the API and (later) the public API all end up in
    // this function, so none of them can skip the limits.
    const ent = await entitlementsInTx(tx, ctx.orgId);
    await assertCanCreateMonitor(tx, ctx.orgId, ent);
    assertIntervalAllowed(ent, input.intervalSeconds);
    const [row] = await tx
      .insert(monitors)
      .values({ ...input, organizationId: ctx.orgId, createdBy: ctx.userId })
      .returning();
    return row;
  });
}

/**
 * Lesson 5.3 (🟡): refuse a monitor URL that points inside our network
 * (loopback, private, link-local/cloud metadata, CGNAT, v4 and v6), checked
 * after DNS. A host that does not resolve right now is accepted: the check
 * will say so, and the guard runs again on every check (src/core/safe-fetch.ts).
 * DNS is network: this runs before the transaction, never inside it.
 */
async function assertMonitorUrl(url: string) {
  try {
    await assertPublicUrl(url, { allowUnresolved: true });
  } catch (err) {
    if (err instanceof BlockedUrlError) throw new InvalidRequestError('blocked_url', `Beacon cannot check this URL: ${err.message}.`);
    throw err;
  }
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
  const current = await getEditableMonitor(ctx, id);
  if (input.url !== undefined && input.url !== current.url) await assertMonitorUrl(input.url);
  // TODO(7.3): record "monitor.updated" in the audit log.
  return withOrg(ctx.orgId, async (tx) => {
    // Lesson 3.2: the limits apply to updates too, not only to creates.
    const ent = await entitlementsInTx(tx, ctx.orgId);
    if (input.intervalSeconds !== undefined) assertIntervalAllowed(ent, input.intervalSeconds);
    // Lesson 3.2 (🟡): pausing records why. Un-pausing (a monitor paused by
    // hand, or one a downgrade froze) needs a free running slot.
    const { paused, ...fields } = input; // parsed by updateMonitorInput: only name, url, intervalSeconds, paused
    const pause =
      paused === true && !current.paused
        ? { paused: true, pausedReason: 'manual' as const }
        : paused === false && current.paused
          ? { paused: false, pausedReason: null }
          : {};
    if (paused === false && current.paused) await assertCanRunAnotherMonitor(tx, ctx.orgId, ent);
    const [row] = await tx
      .update(monitors)
      .set({ ...fields, ...pause })
      .where(and(eq(monitors.organizationId, ctx.orgId), eq(monitors.id, id)))
      .returning();
    return row;
  });
}

export async function deleteMonitor(ctx: OrgScope & Actor, id: string): Promise<void> {
  await getEditableMonitor(ctx, id);
  // TODO(7.3): record "monitor.deleted" in the audit log.
  await withOrg(ctx.orgId, (tx) => tx.delete(monitors).where(and(eq(monitors.organizationId, ctx.orgId), eq(monitors.id, id))));
}

/**
 * Mark an open incident as resolved by hand (the checker also resolves it on
 * the next success). Lesson 4.2: resolving notifies; lesson 5.1: through an
 * `incident.notify` job enqueued in the same transaction.
 */
export async function resolveIncident(ctx: OrgScope, incidentId: string): Promise<boolean> {
  if (!isUuid(incidentId)) return false;
  return withOrg(ctx.orgId, async (tx) => {
    const [incident] = await tx
      .update(incidents)
      .set({ resolvedAt: new Date() })
      .where(and(eq(incidents.organizationId, ctx.orgId), eq(incidents.id, incidentId), isNull(incidents.resolvedAt)))
      .returning();
    if (!incident?.resolvedAt) return false;
    const [monitor] = await tx.select().from(monitors).where(and(eq(monitors.organizationId, ctx.orgId), eq(monitors.id, incident.monitorId)));
    await publishInTx(tx, ctx.orgId, { type: 'incident.changed', monitorId: monitor.id, incidentId: incident.id, state: 'resolved' });
    await enqueueNotify(tx, { orgId: ctx.orgId, event: 'incident.resolved', incidentId: incident.id });
    return true;
  });
}
