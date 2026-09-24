import { and, desc, eq, isNull, sql as dsql } from 'drizzle-orm';
import { db, schema } from '@/db';
import { uptimePercent } from '@/core/incidents';
import type { CreateMonitorInput } from '@/core/validation';

const { monitors, checkResults, incidents } = schema;

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

/**
 * Every monitor with its latest state. TODO(1.2): scope this to the caller's
 * organization — right now every visitor sees every monitor.
 */
export async function listMonitors(): Promise<MonitorView[]> {
  const rows = await db.select().from(monitors).orderBy(monitors.createdAt);
  return Promise.all(
    rows.map(async (m) => {
      const recent = await db
        .select()
        .from(checkResults)
        .where(and(eq(checkResults.monitorId, m.id), dsql`${checkResults.checkedAt} > now() - interval '24 hours'`))
        .orderBy(desc(checkResults.checkedAt));
      const [open] = await db
        .select()
        .from(incidents)
        .where(and(eq(incidents.monitorId, m.id), isNull(incidents.resolvedAt)))
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

export async function createMonitor(input: CreateMonitorInput) {
  // TODO(1.3): check the caller may create monitors. TODO(3.2): enforce the plan's monitor limit.
  // TODO(7.3): record "monitor.created" in the audit log.
  const [row] = await db.insert(monitors).values(input).returning();
  return row;
}
