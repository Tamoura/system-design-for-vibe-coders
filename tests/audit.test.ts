import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn(), getSessionUser: vi.fn() }));
vi.mock('@/lib/email', () => ({ sendEmail: vi.fn(async () => ({ id: 'queued' })) }));

import { and, desc, eq, sql } from 'drizzle-orm';
import * as dbModule from '@/db';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { actorLabel, AUDIT_ACTIONS, csvField, diffFields, findSecrets, verifyChain } from '@/core/audit';
import { entitlementsFor } from '@/core/plans';
import { requireMembership } from '@/lib/access';
import { createApiKey, revokeApiKey } from '@/lib/api-keys';
import { listAuditEvents, recordAudit, toCustomerView } from '@/lib/audit';
import { countAuditEvents, purgeExpiredAuditEvents, recordPlatformAudit, verifyAuditChain } from '@/lib/admin/audit';
import { createInvitation, revokeInvitation, resendInvitation } from '@/lib/invitations';
import { createMonitor, deleteMonitor, updateMonitor } from '@/lib/monitors';
import { runWithContext } from '@/lib/observability/context';
import { setResolverForTests } from '@/core/safe-fetch';
import { createEndpoint, deleteEndpoint, setEndpointEnabled } from '@/lib/webhooks';
import { renameOrganization, setStatusPagePublic } from '@/lib/organizations';
import * as auditRoute from '@/app/api/orgs/[orgSlug]/audit-log/route';
import * as memberRoute from '@/app/api/orgs/[orgSlug]/members/[userId]/route';
import type { AuditEvent } from '@/db/schema';
import { makeOrg, signInAs } from './helpers/fixtures';
import type { PGlite } from '@electric-sql/pglite';

/*
 * Lesson 7.3: the audit log.
 *   🟢 the table and recordAudit() in the SAME transaction, for every sensitive action
 *   🟡 the customer's page and API: owners/admins only, filters, pagination, CSV, retention by plan
 *   (and the 🔴 essentials Beacon also has: append-only grants, a hash chain per org)
 */
const pg = () => (dbModule as unknown as { sql: PGlite }).sql;
const { auditEvents } = schema;

type Org = Awaited<ReturnType<typeof makeOrg>>;
let acme: Org;
let globex: Org;

/** As if the request came from a browser: the request id, IP and user agent the audit log should keep. */
const REQUEST = { requestId: 'req-audit-test', ip: '203.0.113.9', userAgent: 'Mozilla/5.0 (audit test)' };
const inRequest = <T>(fn: () => Promise<T>) => runWithContext({ ...REQUEST }, fn);
const ownerCtx = (org: Org) => inRequest(async () => {
  signInAs(org.users.owner);
  return requireMembership(org.slug);
});

async function eventsOf(orgId: string, action?: string): Promise<AuditEvent[]> {
  return db
    .select()
    .from(auditEvents)
    .where(action ? and(eq(auditEvents.organizationId, orgId), eq(auditEvents.action, action)) : eq(auditEvents.organizationId, orgId))
    .orderBy(desc(auditEvents.seq));
}

beforeAll(async () => {
  acme = await makeOrg('Audit Acme');
  globex = await makeOrg('Audit Globex');
});

describe('🟢 recordAudit(): one event per sensitive action, with actor, action, target, org, IP, user agent and time', () => {
  it('member.role_changed through the API: before/after, the person, their IP and user agent', async () => {
    signInAs(acme.users.owner);
    const res = await memberRoute.PATCH(
      new Request('http://test/x', { method: 'PATCH', headers: { 'content-type': 'application/json', 'x-forwarded-for': '198.51.100.7', 'user-agent': 'curl/8', 'x-request-id': 'req-role-1' }, body: JSON.stringify({ role: 'member' }) }),
      { params: Promise.resolve({ orgSlug: acme.slug, userId: acme.users.viewer.id }) },
    );
    expect(res.status).toBe(200);
    const events = await eventsOf(acme.id, 'member.role_changed');
    expect(events).toHaveLength(1);
    expect(events[0]).toMatchObject({
      organizationId: acme.id,
      category: 'members',
      actorType: 'user',
      actorId: acme.users.owner.id,
      actorEmail: acme.users.owner.email,
      targetType: 'member',
      targetId: acme.users.viewer.id,
      ipAddress: '198.51.100.7',
      userAgent: 'curl/8',
      requestId: 'req-role-1',
      changes: { role: { before: 'viewer', after: 'member' } },
    });
    expect(Math.abs(events[0].occurredAt.getTime() - Date.now())).toBeLessThan(10_000);
    // Setting the same role again changes nothing, so it records nothing.
    signInAs(acme.users.owner);
    await memberRoute.PATCH(new Request('http://test/x', { method: 'PATCH', body: JSON.stringify({ role: 'member' }) }), { params: Promise.resolve({ orgSlug: acme.slug, userId: acme.users.viewer.id }) });
    expect(await eventsOf(acme.id, 'member.role_changed')).toHaveLength(1);
  });

  it('monitor created, paused, resumed, edited, deleted: exactly one event each', async () => {
    const ctx = await ownerCtx(acme);
    const m = await inRequest(() => createMonitor(ctx, { name: 'payments-api', url: 'https://pay.acme.test', intervalSeconds: 60 }));
    await inRequest(() => updateMonitor(ctx, m.id, { paused: true }));
    await inRequest(() => updateMonitor(ctx, m.id, { paused: false }));
    await inRequest(() => updateMonitor(ctx, m.id, { name: 'payments-api-v2', intervalSeconds: 300 }));
    await inRequest(() => deleteMonitor(ctx, m.id));
    const trail = (await eventsOf(acme.id)).filter((e) => e.targetId === m.id).reverse();
    expect(trail.map((e) => e.action)).toEqual(['monitor.created', 'monitor.paused', 'monitor.resumed', 'monitor.updated', 'monitor.deleted']);
    for (const e of trail) expect(e).toMatchObject({ actorId: acme.users.owner.id, ipAddress: REQUEST.ip, userAgent: REQUEST.userAgent, requestId: REQUEST.requestId });
    expect(trail[1].changes).toEqual({ paused: { before: false, after: true }, pausedReason: { before: null, after: 'manual' } });
    expect(trail[3].changes).toEqual({ name: { before: 'payments-api', after: 'payments-api-v2' }, intervalSeconds: { before: 60, after: 300 } });
    expect(trail[4].targetName).toBe('payments-api-v2'); // a snapshot: the monitor itself is gone
  });

  it('API key created and revoked: the log keeps the key’s PREFIX, never the key', async () => {
    const ctx = await ownerCtx(acme);
    const { id, key } = await inRequest(() => createApiKey(ctx, { name: 'terraform', scopes: ['monitors:read'] }));
    await inRequest(() => revokeApiKey(ctx, id));
    await inRequest(() => revokeApiKey(ctx, id)); // revoking twice records it once
    const [created] = await eventsOf(acme.id, 'api_key.created');
    const revoked = await eventsOf(acme.id, 'api_key.revoked');
    expect(created.metadata).toMatchObject({ key_prefix: key.slice(0, 12), scopes: ['monitors:read'] });
    expect(revoked).toHaveLength(1);
    const everything = JSON.stringify(await eventsOf(acme.id));
    expect(everything).not.toContain(key);
    expect(everything).not.toContain(key.slice(12)); // not even the secret part
  });

  it('invitations: invited, resent, revoked (the token never)', async () => {
    const ctx = await ownerCtx(acme);
    const invitation = await inRequest(() => createInvitation(ctx, { email: 'new-hire@acme.test', role: 'viewer' }));
    await inRequest(() => resendInvitation(ctx, invitation.id));
    await inRequest(() => revokeInvitation(ctx, invitation.id));
    const actions = (await eventsOf(acme.id)).filter((e) => e.targetId === invitation.id).map((e) => e.action).reverse();
    expect(actions).toEqual(['member.invited', 'member.invitation_resent', 'member.invitation_revoked']);
    expect(JSON.stringify(await eventsOf(acme.id))).not.toContain(invitation.tokenHash);
  });

  it('webhooks, org name and status page: the settings that change who is told what', async () => {
    const ctx = await ownerCtx(globex);
    setResolverForTests(async () => [{ address: '93.184.215.14', family: 4 }]); // no DNS in tests: a public address
    const { id, secret } = await inRequest(() => createEndpoint(ctx, { url: 'https://hooks.globex.test/beacon', eventTypes: ['incident.opened'] }));
    setResolverForTests(null);
    await inRequest(() => setEndpointEnabled(ctx, id, false));
    await inRequest(() => deleteEndpoint(ctx, id));
    await inRequest(() => renameOrganization(ctx, 'Audit Globex Renamed'));
    await inRequest(() => setStatusPagePublic(ctx, false));
    const actions = (await eventsOf(globex.id)).map((e) => e.action);
    expect(actions).toEqual(expect.arrayContaining(['webhook.created', 'webhook.disabled', 'webhook.deleted', 'org.renamed', 'status_page.unpublished']));
    expect(JSON.stringify(await eventsOf(globex.id))).not.toContain(secret);
  });

  it('a failure before COMMIT leaves neither the change nor the event', async () => {
    const [m] = await withOrg(acme.id, (tx) => tx.insert(schema.monitors).values({ organizationId: acme.id, name: 'rollback-me', url: 'https://r.test' }).returning());
    const before = await countAuditEvents(acme.id);
    await expect(
      withOrg(acme.id, async (tx) => {
        await tx.update(schema.monitors).set({ paused: true, pausedReason: 'manual' }).where(eq(schema.monitors.id, m.id));
        await recordAudit(tx, { orgId: acme.id, action: 'monitor.paused', source: { actor: { type: 'user', id: acme.users.owner.id } }, target: { type: 'monitor', id: m.id } });
        throw new Error('crash after the change, before commit');
      }),
    ).rejects.toThrow('crash');
    expect(await countAuditEvents(acme.id)).toBe(before);
    const [still] = await withOrg(acme.id, (tx) => tx.select().from(schema.monitors).where(eq(schema.monitors.id, m.id)));
    expect(still.paused).toBe(false);
  });

  it('refuses unknown actions and anything that looks like a secret (and the change rolls back with it)', async () => {
    await expect(withOrg(acme.id, (tx) => recordAudit(tx, { orgId: acme.id, action: 'monitor.hacked' as never, source: { actor: { type: 'system', id: 'x' } } }))).rejects.toThrow(/Unknown audit action/);
    await expect(
      withOrg(acme.id, (tx) => recordAudit(tx, { orgId: acme.id, action: 'api_key.created', source: { actor: { type: 'system', id: 'x' } }, metadata: { key: 'bk_live_AAAAAAAAAAAAAAAAAAAAAAAA' } })),
    ).rejects.toThrow(/secret/);
    expect(findSecrets({ changes: { password: { before: 'a', after: 'b' } } })).toEqual(['changes.password']);
    expect(findSecrets({ url: 'https://hooks.slack.com/services/T0/B0/xyz' })).toEqual(['url']);
    expect(findSecrets({ scopes: ['monitors:read'], key_prefix: 'bk_live_Ab3x' })).toEqual([]);
  });

  it('every action in the registry has a dotted name, a category and a description', () => {
    for (const [name, spec] of Object.entries(AUDIT_ACTIONS)) {
      expect(name).toMatch(/^[a-z_]+\.[a-z_]+$/);
      expect(spec.description.length).toBeGreaterThan(10);
    }
  });

  it('diffFields keeps only the fields that changed, never the rest of the row', () => {
    expect(diffFields({ name: 'a', url: 'u', secret: 's' }, { name: 'b', url: 'u', secret: 't' }, ['name', 'url'])).toEqual({ name: { before: 'a', after: 'b' } });
  });
});

describe('append-only, enforced by Postgres', () => {
  it('the app role may insert and read, but not UPDATE or DELETE an event', async () => {
    const tryAs = (statement: string) =>
      withOrg(acme.id, (tx) => tx.execute(sql.raw(statement))).then(
        () => 'allowed',
        (e) => String((e as { cause?: { message?: string } }).cause?.message ?? (e as Error).message),
      );
    expect(await tryAs(`update audit_events set action = 'x'`)).toMatch(/permission denied/);
    expect(await tryAs(`delete from audit_events`)).toMatch(/permission denied/);
  });
});

describe('tamper evidence: a hash chain per organization', () => {
  it('an intact chain verifies; editing a row as a superuser is detected; so is deleting one', async () => {
    const org = await makeOrg('Chain Co');
    for (let i = 0; i < 5; i++) {
      await withOrg(org.id, (tx) => recordAudit(tx, { orgId: org.id, action: 'org.renamed', source: { actor: { type: 'user', id: org.users.owner.id } }, changes: { name: { before: `v${i}`, after: `v${i + 1}` } } }));
    }
    expect(await verifyAuditChain(org.id)).toMatchObject({ ok: true, checked: 5 });

    const rows = await eventsOf(org.id); // newest first
    // The database owner (or anyone with psql) quietly rewrites history…
    await pg().query(`update audit_events set actor_email = 'someone-else@evil.test' where id = $1`, [rows[2].id]);
    const edited = await verifyAuditChain(org.id);
    expect(edited.ok).toBe(false);
    expect(edited.problems).toEqual([{ id: rows[2].id, problem: 'hash_mismatch' }]);

    await pg().query(`delete from audit_events where id = $1`, [rows[2].id]);
    const deleted = await verifyAuditChain(org.id);
    expect(deleted.problems).toContainEqual({ id: rows[1].id, problem: 'broken_link' });
  });

  it('chains are per org: another org’s events never link into this one', async () => {
    expect((await verifyAuditChain(acme.id)).ok).toBe(true);
    expect((await verifyAuditChain(globex.id)).ok).toBe(true);
    const [first] = await db.select().from(auditEvents).where(eq(auditEvents.organizationId, globex.id)).orderBy(auditEvents.seq).limit(1);
    expect(first.prevHash).toBe('0'.repeat(64));
  });

  it('verifyChain works on the rows alone (the worker runs it every night)', () => {
    expect(verifyChain([])).toEqual({ ok: true, checked: 0, problems: [] });
  });
});

describe('🟡 the customer-facing audit log (page API + CSV)', () => {
  const get = (org: Org, query = '') => auditRoute.GET(new Request(`http://test/api/orgs/${org.slug}/audit-log${query}`), { params: Promise.resolve({ orgSlug: org.slug }) });

  it('owners and admins read it; a member gets 403, a viewer 403, an outsider 404', async () => {
    for (const [role, status] of [['owner', 200], ['admin', 200], ['member', 403], ['viewer', 403]] as const) {
      signInAs(acme.users[role]);
      expect((await get(acme)).status).toBe(status);
    }
    signInAs(globex.users.owner);
    expect((await get(acme)).status).toBe(404);
  });

  it('a Free org gets 402 with the plan that has it (the entitlement from lesson 3.2)', async () => {
    const free = await makeOrg('Audit Free', { plan: 'free' });
    signInAs(free.users.owner);
    const res = await get(free);
    expect(res.status).toBe(402);
    expect(await res.json()).toMatchObject({ error: 'limit_exceeded', limit: 'auditLog', upgradeTo: 'pro' });
  });

  it('retention is the plan’s: Pro sees 30 days, Business a year', async () => {
    expect([entitlementsFor('free').auditLogRetentionDays, entitlementsFor('pro').auditLogRetentionDays, entitlementsFor('business').auditLogRetentionDays]).toEqual([0, 30, 365]);
    const org = await makeOrg('Retention Co', { plan: 'pro' });
    const at = (days: number) => new Date(Date.now() - days * 86_400_000);
    for (const days of [5, 45, 200]) {
      await withOrg(org.id, (tx) => recordAudit(tx, { orgId: org.id, action: 'org.renamed', source: { actor: { type: 'system', id: 't' } }, metadata: { days }, at: at(days) }));
    }
    const visible = async () => (await listAuditEvents(org.id, {}, { retentionDays: entitlementsFor((await db.select().from(schema.organizations).where(eq(schema.organizations.id, org.id)))[0].plan).auditLogRetentionDays })).rows.map((e) => (e.metadata as { days: number }).days);
    expect(await visible()).toEqual([5]);
    await db.update(schema.organizations).set({ plan: 'business' }).where(eq(schema.organizations.id, org.id));
    expect(await visible()).toEqual([200, 45, 5]); // newest WRITTEN first; these were back-dated in this order

    // The nightly job deletes what no plan window (and Beacon's 30-day floor) covers any more.
    await db.update(schema.organizations).set({ plan: 'pro' }).where(eq(schema.organizations.id, org.id));
    await recordPlatformAudit({ action: 'flag.changed', source: { actor: { type: 'system', id: 't' } }, at: at(400) });
    await purgeExpiredAuditEvents();
    const left = await db.select({ metadata: auditEvents.metadata }).from(auditEvents).where(eq(auditEvents.organizationId, org.id));
    expect(left.map((r) => (r.metadata as { days: number }).days)).toEqual([5]);
    expect(await countAuditEvents(null)).toBeGreaterThan(0); // platform events are kept two years
    expect((await verifyAuditChain(org.id)).ok).toBe(true); // deleting the oldest rows keeps the chain verifiable
  });

  it('filters combine (actor + category + dates) and pages go back with a cursor, without gaps or repeats', async () => {
    const org = await makeOrg('Filter Co');
    const owner = { actor: { type: 'user' as const, id: org.users.owner.id } };
    const admin = { actor: { type: 'user' as const, id: org.users.admin.id } };
    for (let i = 0; i < 130; i++) {
      await withOrg(org.id, (tx) =>
        recordAudit(tx, { orgId: org.id, action: i % 2 ? 'monitor.created' : 'member.role_changed', source: i % 3 ? owner : admin, target: { type: i % 2 ? 'monitor' : 'member', id: `t${i}` }, metadata: { i }, at: new Date(Date.now() - i * 60_000) }),
      );
    }
    const filters = { actor: org.users.owner.id, category: 'monitors' as const };
    // Newest first = last written first (seq): i = 129, 127, …
    const expected = Array.from({ length: 130 }, (_, i) => i).filter((i) => i % 2 && i % 3).reverse();
    const seen: number[] = [];
    let before: number | undefined;
    do {
      const page = await listAuditEvents(org.id, filters, { retentionDays: 365, limit: 10, before });
      seen.push(...page.rows.map((e) => (e.metadata as { i: number }).i));
      before = page.nextBefore ?? undefined;
    } while (before);
    expect(seen).toEqual(expected);
    // A date range: only the last hour.
    const recent = await listAuditEvents(org.id, { from: new Date(Date.now() - 3600_000) }, { retentionDays: 365, limit: 500 });
    expect(recent.rows.every((e) => e.occurredAt.getTime() >= Date.now() - 3600_000)).toBe(true);
    expect(recent.rows.length).toBeGreaterThan(55);
    expect(recent.rows.length).toBeLessThan(65);
  });

  it('the query string drives the same filters, and CSV exports exactly them', async () => {
    signInAs(acme.users.owner);
    const json = await (await get(acme, '?category=integrations')).json();
    expect(json.data.length).toBeGreaterThan(0);
    expect(json.data.every((e: { category: string }) => e.category === 'integrations')).toBe(true);
    const csv = await get(acme, '?category=monitors&format=csv');
    expect(csv.headers.get('content-type')).toContain('text/csv');
    expect(csv.headers.get('content-disposition')).toMatch(/attachment; filename="beacon-audit-/);
    const lines = (await csv.text()).trim().split('\r\n');
    expect(lines[0]).toBe('occurred_at,action,category,actor,actor_type,target_type,target_id,target_name,ip_address,user_agent,request_id,changes,metadata');
    expect(lines.length).toBeGreaterThan(5);
    expect(lines.slice(1).every((l) => l.includes('"monitors"'))).toBe(true);
    expect(csvField('=HYPERLINK("http://evil")')).toBe(`"'=HYPERLINK(""http://evil"")"`); // no formula injection in Excel
  });

  it('staff impersonation reads "Beacon support (on behalf of Ana)", and hides the staff member’s email and IP', async () => {
    await withOrg(acme.id, (tx) =>
      recordAudit(tx, {
        orgId: acme.id,
        action: 'support.impersonation_started',
        source: { actor: { type: 'staff', id: 'staff-1', name: 'Sue Support', email: 'sue@beacon.test' }, onBehalfOf: { id: acme.users.owner.id, name: 'Ana' }, ip: '10.1.2.3' },
        reason: 'TICKET-1: internal note',
      }),
    );
    const [e] = await eventsOf(acme.id, 'support.impersonation_started');
    const view = toCustomerView(e);
    expect(view.actor).toBe('Beacon support (on behalf of Ana)');
    expect(JSON.stringify(view)).not.toMatch(/sue@beacon\.test|10\.1\.2\.3|internal note/);
    expect(actorLabel({ actorType: 'user', actorName: 'Ana', actorEmail: 'ana@acme.test' })).toBe('Ana (ana@acme.test)');
    expect(actorLabel({ actorType: 'api_key', actorName: 'bk_live_Ab3x…', actorEmail: null })).toBe('API key bk_live_Ab3x…');
  });

  it('cross-tenant: org B never sees org A’s events, even with a guessed cursor or target id', async () => {
    signInAs(globex.users.owner);
    const [acmeEvent] = await eventsOf(acme.id);
    const res = await get(globex, `?target_id=${acmeEvent.targetId}&before=${acmeEvent.seq + 1}`);
    const body = await res.text();
    expect(body).not.toContain(acmeEvent.id);
    expect(body).not.toContain(acme.id);
    // And inside withOrg(globex), row-level security hides Acme's rows even without a WHERE.
    const all = await withOrg(globex.id, (tx) => tx.select({ org: auditEvents.organizationId }).from(auditEvents));
    expect(new Set(all.map((r) => r.org))).toEqual(new Set([globex.id]));
  });
});
