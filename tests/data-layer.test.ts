import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import * as dbModule from '@/db';
import { db, schema } from '@/db';
import { makeOrg } from './helpers/fixtures';
import { createMonitor, listMonitors, updateMonitor } from '@/lib/monitors';

/*
 * Lesson 2.1: the data layer. The dashboard query must not grow with the
 * number of monitors (no N+1), and tables Beacon owns keep their timestamps.
 */
const queryLog = (dbModule as unknown as { queryLog: string[] }).queryLog;

let org: Awaited<ReturnType<typeof makeOrg>>;
const owner = () => ({ orgId: org.id, userId: org.users.owner.id, role: 'owner' as const });

async function addMonitorWithChecks(name: string, oks: boolean[]) {
  const m = await createMonitor(owner(), { name, url: `https://${name}.test`, intervalSeconds: 60 });
  const now = Date.now();
  await db.insert(schema.checkResults).values(
    oks.map((ok, i) => ({ organizationId: org.id, monitorId: m.id, ok, statusCode: ok ? 200 : 500, latencyMs: 100 + i, checkedAt: new Date(now - i * 60_000) })),
  );
  return m;
}

/** How many SQL statements `fn` sends. */
async function countQueries(fn: () => Promise<unknown>) {
  queryLog.length = 0;
  await fn();
  return queryLog.length;
}

beforeAll(async () => {
  org = await makeOrg('Data');
});

describe('listMonitors (the dashboard query)', () => {
  it('returns the latest state, 24h uptime and the open incident of each monitor', async () => {
    const up = await addMonitorWithChecks('up', [true, true, false, true]); // newest first
    const down = await addMonitorWithChecks('down', [false, false, true, true]);
    await db.insert(schema.incidents).values({ organizationId: org.id, monitorId: down.id, cause: 'HTTP 500' });
    const old = new Date(Date.now() - 48 * 3600_000); // outside the 24h window: must not count
    await db.insert(schema.checkResults).values({ organizationId: org.id, monitorId: up.id, ok: false, checkedAt: old });

    const views = await listMonitors({ orgId: org.id });
    const byName = Object.fromEntries(views.map((v) => [v.name, v]));
    expect(byName.up).toMatchObject({ state: 'up', uptime24h: 75, lastLatencyMs: 100, openIncident: null });
    expect(byName.up.lastCheckedAt).toBeInstanceOf(Date);
    expect(byName.down).toMatchObject({ state: 'down', uptime24h: 50, openIncident: { cause: 'HTTP 500' } });
  });

  it('shows a monitor with no checks as unknown', async () => {
    await createMonitor(owner(), { name: 'fresh', url: 'https://fresh.test', intervalSeconds: 60 });
    const fresh = (await listMonitors({ orgId: org.id })).find((v) => v.name === 'fresh');
    expect(fresh).toMatchObject({ state: 'unknown', uptime24h: null, lastCheckedAt: null, openIncident: null });
  });

  it('sends the same number of queries for 3 monitors as for 23 (no N+1)', async () => {
    const small = await countQueries(() => listMonitors({ orgId: org.id }));
    for (let i = 0; i < 20; i++) await addMonitorWithChecks(`bulk-${i}`, [true, false]);
    const large = await countQueries(() => listMonitors({ orgId: org.id }));
    expect(large).toBe(small);
  });
});

describe('timestamps', () => {
  it('bumps updated_at on update and leaves created_at alone', async () => {
    const m = await createMonitor(owner(), { name: 'ts', url: 'https://ts.test', intervalSeconds: 60 });
    await new Promise((r) => setTimeout(r, 20));
    const updated = await updateMonitor(owner(), m.id, { name: 'ts2' });
    expect(updated.createdAt).toEqual(m.createdAt);
    expect(updated.updatedAt.getTime()).toBeGreaterThan(m.updatedAt.getTime());
  });
});
