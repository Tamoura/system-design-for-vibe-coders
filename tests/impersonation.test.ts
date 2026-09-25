import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn(), getSessionUser: vi.fn() }));

import { NextRequest } from 'next/server';
import { and, desc, eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { IMPERSONATION_COOKIE, IMPERSONATION_TTL_MS } from '@/core/staff';
import { requireMembership, requirePermission } from '@/lib/access';
import { toCustomerView } from '@/lib/audit';
import { AccessError } from '@/lib/errors';
import { endImpersonation, resolveImpersonation, startImpersonation } from '@/lib/impersonation';
import { getSessionUser, type CurrentUser } from '@/lib/session';
import { findStaffMember, type StaffMember } from '@/lib/staff';
import { proxy } from '@/proxy';
import * as actionRoute from '@/app/api/internal/orgs/[orgId]/[action]/route';
import * as monitorsRoute from '@/app/api/orgs/[orgSlug]/monitors/route';
import { makeOrg, makeUser, signInAs } from './helpers/fixtures';

/*
 * Lesson 7.1: impersonation, done safely. Read-only, 30 minutes, one org,
 * a banner, and the customer's own audit log says "Beacon support (on behalf of Ana)".
 */
type Org = Awaited<ReturnType<typeof makeOrg>>;
let acme: Org;
let other: Org;
let supportUser: CurrentUser;
let support: StaffMember;
const SOURCE = { actor: { type: 'staff' as const, id: 'x', name: 'Sue', email: 'sue@beacon.test' }, ip: '10.0.0.1', via: 'admin' as const };

beforeAll(async () => {
  acme = await makeOrg('Imp Acme');
  other = await makeOrg('Imp Other');
  // Acme's owner is also in another org: an impersonation of Acme must not open that one.
  await db.insert(schema.memberships).values({ organizationId: other.id, userId: acme.users.owner.id, role: 'owner' });
  supportUser = await makeUser('support-sue');
  await db.insert(schema.staffUsers).values({ userId: supportUser.id, role: 'support' });
  support = (await findStaffMember(supportUser))!;
});

async function impersonateOwner() {
  const source = { ...SOURCE, actor: { ...SOURCE.actor, id: support.staffId } };
  const started = await startImpersonation(support, { orgId: acme.id, targetUserId: acme.users.owner.id, reason: 'TICKET-5: chart looks wrong' }, source);
  const as = await resolveImpersonation(supportUser.id, started.token);
  return { ...started, as: as! };
}

describe('starting: checks, a row, and an event in the customer’s log', () => {
  it('support starts a 30-minute, read-only session; the start is in Acme’s audit log as Beacon support on behalf of the owner', async () => {
    const { as, expiresAt, orgSlug } = await impersonateOwner();
    expect(orgSlug).toBe(acme.slug);
    expect(as).toMatchObject({ id: acme.users.owner.id, impersonation: { staffUserId: support.staffId, orgId: acme.id, readOnly: true } });
    expect(Math.round((expiresAt.getTime() - Date.now()) / 60_000)).toBe(IMPERSONATION_TTL_MS / 60_000);
    const [e] = await db.select().from(schema.auditEvents).where(and(eq(schema.auditEvents.organizationId, acme.id), eq(schema.auditEvents.action, 'support.impersonation_started'))).orderBy(desc(schema.auditEvents.seq)).limit(1);
    expect(e).toMatchObject({ actorType: 'staff', onBehalfOfId: acme.users.owner.id, reason: 'TICKET-5: chart looks wrong', targetId: acme.users.owner.id });
    expect(toCustomerView(e).actor).toBe(`Beacon support (on behalf of ${acme.users.owner.name})`);
  });

  it('a billing staff member may not impersonate (403, direct POST); nobody may impersonate a non-member', async () => {
    const biller = await makeUser('bill');
    await db.insert(schema.staffUsers).values({ userId: biller.id, role: 'billing' });
    vi.mocked(getSessionUser).mockResolvedValue(biller);
    const res = await actionRoute.POST(
      new Request(`http://test/x`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ userId: acme.users.owner.id, reason: 'just curious, really' }) }),
      { params: Promise.resolve({ orgId: acme.id, action: 'impersonate' }) },
    );
    expect(res.status).toBe(403);
    const stranger = await makeUser('stranger');
    await expect(startImpersonation(support, { orgId: acme.id, targetUserId: stranger.id, reason: 'not a member at all' }, SOURCE)).rejects.toThrow(/not a member/);
  });
});

describe('while impersonating', () => {
  it('the token only works for the staff member who started it, and dies after 30 minutes even if active', async () => {
    const { token } = await impersonateOwner();
    const someoneElse = await makeUser('thief');
    expect(await resolveImpersonation(someoneElse.id, token)).toBeNull();
    expect(await resolveImpersonation(supportUser.id, token, new Date(Date.now() + 29 * 60_000))).not.toBeNull();
    expect(await resolveImpersonation(supportUser.id, token, new Date(Date.now() + 31 * 60_000))).toBeNull();
  });

  it('read permissions work; every write permission is refused (403), and other orgs of the customer are 404', async () => {
    const { as } = await impersonateOwner();
    signInAs(as);
    expect((await requireMembership(acme.slug)).impersonation?.readOnly).toBe(true);
    await expect(requirePermission(acme.slug, 'monitor.read')).resolves.toMatchObject({ orgId: acme.id });
    await expect(requirePermission(acme.slug, 'audit.read')).resolves.toMatchObject({ orgId: acme.id });
    for (const write of ['monitor.write', 'member.manage', 'integration.manage', 'billing.manage', 'org.manage'] as const) {
      await expect(requirePermission(acme.slug, write)).rejects.toEqual(new AccessError('forbidden'));
    }
    await expect(requireMembership(other.slug)).rejects.toEqual(new AccessError('not_found'));
  });

  it('an API write during impersonation is refused by the route too (the second lock), and nothing is created', async () => {
    const { as } = await impersonateOwner();
    signInAs(as);
    const res = await monitorsRoute.POST(
      new Request('http://test/x', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ name: 'by support', url: 'https://x.test', intervalSeconds: 300 }) }),
      { params: Promise.resolve({ orgSlug: acme.slug }) },
    );
    expect(res.status).toBe(403);
    expect((await monitorsRoute.GET(new Request('http://test/x'), { params: Promise.resolve({ orgSlug: acme.slug }) })).status).toBe(200);
  });

  it('exit ends it, in the customer’s log too; the token is dead afterwards', async () => {
    const { token } = await impersonateOwner();
    const ended = await endImpersonation(supportUser.id, token, SOURCE);
    expect(ended).toEqual({ orgId: acme.id });
    expect(await resolveImpersonation(supportUser.id, token)).toBeNull();
    const [e] = await db.select().from(schema.auditEvents).where(eq(schema.auditEvents.action, 'support.impersonation_ended')).orderBy(desc(schema.auditEvents.seq)).limit(1);
    expect(e).toMatchObject({ organizationId: acme.id, onBehalfOfId: acme.users.owner.id });
  });
});

describe('src/proxy.ts: the first lock, before any code runs', () => {
  const request = (method: string, path: string, cookie?: string, headers: Record<string, string> = {}) =>
    new NextRequest(`http://localhost${path}`, { method, headers: { ...(cookie && { cookie: `${IMPERSONATION_COOKIE}=${cookie}` }), ...headers } });

  it('refuses POST, PUT, PATCH and DELETE everywhere while the impersonation cookie is present (API routes and server actions alike)', async () => {
    for (const method of ['POST', 'PUT', 'PATCH', 'DELETE']) {
      for (const path of ['/api/orgs/acme/monitors', '/api/v1/monitors', '/acme/settings/general', '/api/auth/change-password']) {
        const res = proxy(request(method, path, 'tok'));
        expect(res.status, `${method} ${path}`).toBe(403);
        expect((await res.json()).message).toMatch(/Read-only impersonation/);
      }
    }
  });

  it('lets reads through, and the few POSTs that leave or act as staff', () => {
    expect(proxy(request('GET', '/acme/monitors', 'tok')).status).toBe(200);
    for (const path of ['/api/impersonation/exit', '/api/auth/sign-out', '/api/internal/orgs/x/extend-trial', '/internal/flags']) {
      expect(proxy(request('POST', path, 'tok')).status, path).toBe(200);
    }
    expect(proxy(request('POST', '/api/orgs/acme/monitors')).status).toBe(200); // no cookie: not the proxy's business
  });

  it('gives every request an id: reuses a sane incoming one, replaces garbage, and returns it', () => {
    const kept = proxy(request('GET', '/x', undefined, { 'x-request-id': 'lb-req-12345678' }));
    expect(kept.headers.get('x-request-id')).toBe('lb-req-12345678');
    expect(kept.headers.get('x-middleware-request-x-request-id')).toBe('lb-req-12345678'); // passed on to the app
    const replaced = proxy(request('GET', '/x', undefined, { 'x-request-id': '<script>' }));
    expect(replaced.headers.get('x-request-id')).toMatch(/^[0-9a-f-]{36}$/);
  });
});
