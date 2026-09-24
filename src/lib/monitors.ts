import { and, desc, eq, isNull, sql as dsql } from 'drizzle-orm';
import { db, schema } from '@/db';
import { uptimePercent } from '@/core/incidents';
import type { CreateMonitorInput } from '@/core/validation';

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

/** Every monitor in one organization, with its latest state. */
export async function listMonitors({ orgId }: OrgScope): Promise<MonitorView[]> {
  const rows = await db.select().from(monitors).where(eq(monitors.organizationId, orgId)).orderBy(monitors.createdAt);
  return Promise.all(
    rows.map(async (m) => {
      const recent = await db
        .select()
        .from(checkResults)
        .where(
          and(
            eq(checkResults.organizationId, orgId),
            eq(checkResults.monitorId, m.id),
            dsql`${checkResults.checkedAt} > now() - interval '24 hours'`,
          ),
        )
        .orderBy(desc(checkResults.checkedAt));
      const [open] = await db
        .select()
        .from(incidents)
        .where(and(eq(incidents.organizationId, orgId), eq(incidents.monitorId, m.id), isNull(incidents.resolvedAt)))
        .limit(1);
      const latest = recent[0];
      return {
        id: m.id,
        name: m.name,
        url: m.url,
        intervalSeconds: m.intervalSeconds,
        paused: m.paused,
        state: latest ? (latest.ok ? 'up' : 'down') : 'unknown',
        lastCheckedAt: latest?.checkedAt ?? null,
        lastLatencyMs: latest?.latencyMs ?? null,
        uptime24h: uptimePercent(recent),
        openIncident: open ? { id: open.id, openedAt: open.openedAt, cause: open.cause } : null,
      } satisfies MonitorView;
    }),
  );
  // Lesson 2.1: this is an N+1 query (two queries per monitor). Fine for ten
  // monitors; the 🟡 exercise asks you to replace it with one query.
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

export function isUuid(value: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value);
}
