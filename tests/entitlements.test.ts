import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { entitlementsFor } from '@/core/plans';
import { createMonitor, updateMonitor } from '@/lib/monitors';
import { chooseRunningMonitors, getEntitlements, getMonitorUsage, reconcileMonitorsWithPlan } from '@/lib/entitlements';
import { LimitExceededError } from '@/lib/errors';
import * as monitorsRoute from '@/app/api/orgs/[orgSlug]/monitors/route';
import * as monitorRoute from '@/app/api/orgs/[orgSlug]/monitors/[id]/route';
import { makeOrg, signInAs } from './helpers/fixtures';

/*
 * Lesson 3.2: entitlements are enforced on the server, at every write path:
 * create AND update, through the API and not only the form.
 */

const json = (method: string, body?: unknown) =>
  new Request('http://test', { method, headers: { 'content-type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body) });
const p = <T extends object>(params: T) => ({ params: Promise.resolve(params) });

async function monitorsOf(orgId: string) {
  return withOrg(orgId, (tx) => tx.select().from(schema.monitors).where(eq(schema.monitors.organizationId, orgId)).orderBy(schema.monitors.createdAt));
}

describe('monitor limit and interval minimum (🟢)', () => {
  let free: Awaited<ReturnType<typeof makeOrg>>;

  beforeAll(async () => {
    free = await makeOrg('Freebie', { plan: 'free' });
    for (let i = 1; i <= 5; i++) {
      await createMonitor({ orgId: free.id, userId: free.users.owner.id }, { name: `m${i}`, url: `https://m${i}.test`, intervalSeconds: 300 });
    }
  });

  it('getEntitlements(org) reads the org’s plan', async () => {
    expect(await getEntitlements({ orgId: free.id })).toEqual({ plan: 'free', ...entitlementsFor('free') });
  });

  it('a Free org gets a structured limit_exceeded error for its sixth monitor via the API', async () => {
    signInAs(free.users.owner);
    const res = await monitorsRoute.POST(json('POST', { name: 'sixth', url: 'https://six.test', intervalSeconds: 300 }), p({ orgSlug: free.slug }));
    expect(res.status).toBe(402);
    expect(await res.json()).toMatchObject({ error: 'limit_exceeded', limit: 'maxMonitors', allowed: 5, upgradeTo: 'pro' });
    expect(await monitorsOf(free.id)).toHaveLength(5);
  });

  it('refuses an interval below the plan minimum on create…', async () => {
    const other = await makeOrg('FreeTwo', { plan: 'free' });
    signInAs(other.users.member);
    const res = await monitorsRoute.POST(json('POST', { name: 'fast', url: 'https://fast.test', intervalSeconds: 60 }), p({ orgSlug: other.slug }));
    expect(res.status).toBe(402);
    expect(await res.json()).toMatchObject({ error: 'limit_exceeded', limit: 'minIntervalSec', allowed: 300, upgradeTo: 'pro' });
  });

  it('…and on update', async () => {
    const [m] = await monitorsOf(free.id);
    signInAs(free.users.owner);
    const res = await monitorRoute.PATCH(json('PATCH', { intervalSeconds: 30 }), p({ orgSlug: free.slug, id: m.id }));
    expect(res.status).toBe(402);
    expect(await res.json()).toMatchObject({ limit: 'minIntervalSec', upgradeTo: 'business' });
    // Changing something else still works.
    const ok = await monitorRoute.PATCH(json('PATCH', { name: 'renamed' }), p({ orgSlug: free.slug, id: m.id }));
    expect(ok.status).toBe(200);
  });

  it('pausing by hand records the reason, and un-pausing is allowed while there is room', async () => {
    const [m] = await monitorsOf(free.id);
    const ctx = { orgId: free.id, userId: free.users.owner.id, role: 'owner' as const };
    expect((await updateMonitor(ctx, m.id, { paused: true })).pausedReason).toBe('manual');
    expect((await updateMonitor(ctx, m.id, { paused: false })).pausedReason).toBeNull();
  });
});

describe('downgrade with the freeze policy (🟡)', () => {
  let org: Awaited<ReturnType<typeof makeOrg>>;
  let ids: string[];

  beforeAll(async () => {
    org = await makeOrg('Shrinks', { plan: 'pro' });
    for (let i = 1; i <= 12; i++) {
      await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name: `svc-${i}`, url: `https://svc${i}.test`, intervalSeconds: 60 });
    }
    ids = (await monitorsOf(org.id)).map((m) => m.id);
    // One monitor was already paused by a person.
    await updateMonitor({ orgId: org.id, userId: org.users.owner.id, role: 'owner' }, ids[11], { paused: true });
  });

  it('Pro → Free: the 5 oldest keep running, the rest pause with plan_limit, nothing is deleted, intervals clamp', async () => {
    await db.update(schema.organizations).set({ plan: 'free' }).where(eq(schema.organizations.id, org.id));
    const result = await withOrg(org.id, (tx) => reconcileMonitorsWithPlan(tx, org.id, entitlementsFor('free')));
    expect(result).toMatchObject({ frozen: 6, unfrozen: 0, clamped: 12 });

    const ms = await monitorsOf(org.id);
    expect(ms).toHaveLength(12);
    expect(ms.filter((m) => !m.paused).map((m) => m.name)).toEqual(['svc-1', 'svc-2', 'svc-3', 'svc-4', 'svc-5']);
    expect(ms.filter((m) => m.pausedReason === 'plan_limit')).toHaveLength(6);
    expect(ms.find((m) => m.name === 'svc-12')?.pausedReason).toBe('manual');
    expect(ms.every((m) => m.intervalSeconds === 300)).toBe(true);
    expect(await getMonitorUsage({ orgId: org.id })).toMatchObject({ total: 12, running: 5, frozen: 6, atLimit: true });
  });

  it('running it again changes nothing', async () => {
    const again = await withOrg(org.id, (tx) => reconcileMonitorsWithPlan(tx, org.id, entitlementsFor('free')));
    expect(again).toEqual({ frozen: 0, unfrozen: 0, clamped: 0 });
  });

  it('a frozen monitor cannot be switched back on while 5 are running', async () => {
    const frozen = (await monitorsOf(org.id)).find((m) => m.pausedReason === 'plan_limit')!;
    const attempt = updateMonitor({ orgId: org.id, userId: org.users.owner.id, role: 'owner' }, frozen.id, { paused: false });
    await expect(attempt).rejects.toBeInstanceOf(LimitExceededError);
  });

  it('the owner picks which monitors run', async () => {
    const pick = [ids[6], ids[7], ids[8]];
    await chooseRunningMonitors({ orgId: org.id }, pick);
    const ms = await monitorsOf(org.id);
    expect(ms.filter((m) => !m.paused).map((m) => m.id).sort()).toEqual([...pick].sort());
    expect(ms.find((m) => m.id === ids[11])?.pausedReason).toBe('manual'); // untouched
    await expect(chooseRunningMonitors({ orgId: org.id }, ids.slice(0, 6))).rejects.toBeInstanceOf(LimitExceededError);
  });

  it('another org’s monitor ids cannot be switched on from here', async () => {
    const other = await makeOrg('Neighbour', { plan: 'free' });
    const theirs = await createMonitor({ orgId: other.id, userId: other.users.owner.id }, { name: 'theirs', url: 'https://t.test', intervalSeconds: 300 });
    await updateMonitor({ orgId: other.id, userId: other.users.owner.id, role: 'owner' }, theirs.id, { paused: true });
    await chooseRunningMonitors({ orgId: org.id }, [ids[6], ids[7], ids[8], theirs.id]);
    expect((await monitorsOf(other.id))[0].pausedReason).toBe('manual');
    expect((await monitorsOf(org.id)).filter((m) => !m.paused)).toHaveLength(3);
  });

  it('upgrading again un-pauses the plan-paused monitors, not the manually paused one', async () => {
    await db.update(schema.organizations).set({ plan: 'pro' }).where(eq(schema.organizations.id, org.id));
    const result = await withOrg(org.id, (tx) => reconcileMonitorsWithPlan(tx, org.id, entitlementsFor('pro')));
    expect(result.unfrozen).toBe(8);
    const ms = await monitorsOf(org.id);
    expect(ms.filter((m) => !m.paused)).toHaveLength(11);
    expect(ms.find((m) => m.id === ids[11])?.pausedReason).toBe('manual');
  });
});
