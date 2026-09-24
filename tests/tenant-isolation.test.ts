import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { makeOrg, signInAs } from './helpers/fixtures';
import { createMonitor, deleteMonitor, getMonitor, listMonitors } from '@/lib/monitors';
import { AccessError, requireMembership, requirePermission } from '@/lib/access';
import * as monitorRoute from '@/app/api/orgs/[orgSlug]/monitors/[id]/route';

/*
 * Lesson 1.2 / 1.3: two customers, Acme and Globex. Nothing Globex does may
 * reach Acme's monitor, even when Globex knows its id (IDOR).
 */
let acme: Awaited<ReturnType<typeof makeOrg>>;
let globex: Awaited<ReturnType<typeof makeOrg>>;
let acmeMonitorId: string;

beforeAll(async () => {
  acme = await makeOrg('Acme');
  globex = await makeOrg('Globex');
  const m = await createMonitor({ orgId: acme.id, userId: acme.users.owner.id }, { name: 'Acme API', url: 'https://acme.test', intervalSeconds: 60 });
  acmeMonitorId = m.id;
});

const params = (orgSlug: string, id: string) => ({ params: Promise.resolve({ orgSlug, id }) });

describe('data access is scoped to the organization', () => {
  it('lists only the org’s own monitors', async () => {
    expect((await listMonitors({ orgId: acme.id })).map((m) => m.id)).toEqual([acmeMonitorId]);
    expect(await listMonitors({ orgId: globex.id })).toEqual([]);
  });

  it('cannot fetch another org’s monitor by id', async () => {
    expect(await getMonitor({ orgId: globex.id }, acmeMonitorId)).toBeNull();
    expect(await getMonitor({ orgId: acme.id }, acmeMonitorId)).not.toBeNull();
  });

  it('cannot delete another org’s monitor by id', async () => {
    expect(await deleteMonitor({ orgId: globex.id }, acmeMonitorId)).toBe(false);
    expect(await getMonitor({ orgId: acme.id }, acmeMonitorId)).not.toBeNull();
  });
});

describe('membership checks', () => {
  it('treats a non-member like a missing org (404, not 403)', async () => {
    signInAs(globex.users.owner);
    await expect(requireMembership(acme.slug)).rejects.toEqual(new AccessError('not_found'));
  });

  it('refuses a member whose role lacks the permission', async () => {
    signInAs(acme.users.viewer);
    await expect(requirePermission(acme.slug, 'monitor.write')).rejects.toEqual(new AccessError('forbidden'));
  });

  it('refuses anonymous requests', async () => {
    signInAs(null);
    await expect(requireMembership(acme.slug)).rejects.toEqual(new AccessError('unauthenticated'));
  });
});

describe('IDOR through the API', () => {
  it('Globex owner asking for Acme’s monitor under Globex’s own slug gets 404', async () => {
    signInAs(globex.users.owner);
    const res = await monitorRoute.GET(new Request('http://test'), params(globex.slug, acmeMonitorId));
    expect(res.status).toBe(404);
  });

  it('Globex owner asking under Acme’s slug gets 404 too', async () => {
    signInAs(globex.users.owner);
    const res = await monitorRoute.GET(new Request('http://test'), params(acme.slug, acmeMonitorId));
    expect(res.status).toBe(404);
    const del = await monitorRoute.DELETE(new Request('http://test', { method: 'DELETE' }), params(acme.slug, acmeMonitorId));
    expect(del.status).toBe(404);
  });

  it('an Acme viewer can read it but gets 403 on DELETE', async () => {
    signInAs(acme.users.viewer);
    expect((await monitorRoute.GET(new Request('http://test'), params(acme.slug, acmeMonitorId))).status).toBe(200);
    const del = await monitorRoute.DELETE(new Request('http://test', { method: 'DELETE' }), params(acme.slug, acmeMonitorId));
    expect(del.status).toBe(403);
    expect(await getMonitor({ orgId: acme.id }, acmeMonitorId)).not.toBeNull();
  });
});
