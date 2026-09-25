import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { and, eq } from 'drizzle-orm';
import type { PGlite } from '@electric-sql/pglite';
import * as dbModule from '@/db';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { DAY_MS, RETENTION_RULES } from '@/core/retention';
import { createApiKey } from '@/lib/api-keys';
import { AccessError, InvalidRequestError } from '@/lib/errors';
import { createMonitor } from '@/lib/monitors';
import { findPublicStatusPage } from '@/lib/organizations';
import { scheduleChecks } from '@/lib/scheduler';
import { getStorage } from '@/lib/storage';
import { setResolverForTests } from '@/core/safe-fetch';
import { createEndpoint } from '@/lib/webhooks';
import {
  buildOrgExport, cancelOrgDeletion, countOrgRows, exportDownloadUrl, NOT_EXPORTED, purgeOrganization, requestOrgDeletion, requestOrgExport, tenantTables,
} from '@/lib/privacy/org-data';
import { accountDeletionPlan, deleteAccount, exportUserData, USER_DATA_COVERAGE } from '@/lib/privacy/user-data';
import { purgeExpiredData } from '@/lib/privacy/retention';
import { makeOrg, makeUser } from './helpers/fixtures';
import { jobsAreDue, jobsIn, runQueuedJobs } from './helpers/queue';
import { useTempLocalStorage } from './helpers/storage';

/*
 * Lesson 8.1 (GDPR): export completeness, account deletion with the
 * org-ownership edge cases, org export and deletion through the queue,
 * cross-tenant safety, and retention.
 */
const pg = () => (dbModule as unknown as { sql: PGlite }).sql;
const SOURCE = { actor: { type: 'user' as const, id: null }, ip: '203.0.113.1', via: 'app' as const };
type Org = Awaited<ReturnType<typeof makeOrg>>;
const owner = (org: Org) => ({ orgId: org.id, orgSlug: org.slug, userId: org.users.owner.id });

beforeAll(() => {
  useTempLocalStorage();
  setResolverForTests(async () => [{ address: '93.184.215.14', family: 4 }]);
});

describe('completeness: every column that points at a user, and every tenant table, has a decision', () => {
  it('USER_DATA_COVERAGE lists exactly the foreign keys to users(id)', async () => {
    const { rows } = await pg().query<{ col: string }>(`
      select tc.table_name || '.' || kcu.column_name as col
      from information_schema.table_constraints tc
      join information_schema.key_column_usage kcu on kcu.constraint_name = tc.constraint_name
      join information_schema.constraint_column_usage ccu on ccu.constraint_name = tc.constraint_name
      where tc.constraint_type = 'FOREIGN KEY' and ccu.table_name = 'users' and ccu.column_name = 'id'
      order by 1`);
    expect(rows.map((r) => r.col).sort()).toEqual(Object.keys(USER_DATA_COVERAGE).sort());
  });

  it('the org export covers every table with organization_id except the few listed with a reason', async () => {
    const { rows } = await pg().query<{ table_name: string }>(`
      select distinct c.table_name from information_schema.columns c join pg_class cl on cl.relname = c.table_name and cl.relkind = 'r'
      where c.table_schema = 'public' and c.column_name = 'organization_id' order by 1`);
    expect(tenantTables().map((t) => t.name)).toEqual(rows.map((r) => r.table_name));
    for (const name of Object.keys(NOT_EXPORTED)) expect(rows.map((r) => r.table_name)).toContain(name);
  });
});

describe('a user exports their data', () => {
  it('has their profile, orgs, what they created and their audit trail; never a password hash, token or key', async () => {
    const org = await makeOrg('Portable');
    const me = org.users.admin;
    await db.insert(schema.accounts).values({ userId: me.id, providerId: 'credential', accountId: me.id, password: '$argon2id$v=19$SECRET-HASH', accessToken: 'gho_SECRET_TOKEN' });
    await db.insert(schema.sessions).values({ userId: me.id, token: 'SESSION-TOKEN-XYZ', expiresAt: new Date(Date.now() + DAY_MS), ipAddress: '198.51.100.4', userAgent: 'test' });
    await createMonitor({ orgId: org.id, userId: me.id }, { name: 'my-monitor', url: 'https://mine.test', intervalSeconds: 300 });
    const key = await createApiKey({ orgId: org.id, userId: me.id, role: 'admin' }, { name: 'ci', scopes: ['monitors:read'] });

    const data = await exportUserData(me.id);
    const text = JSON.stringify(data);
    expect(data!.profile).toMatchObject({ id: me.id, email: me.email });
    expect(data!.loginMethods).toEqual([expect.objectContaining({ provider: 'credential' })]);
    expect(data!.sessions).toEqual([expect.objectContaining({ ipAddress: '198.51.100.4' })]);
    const inOrg = data!.organizations.find((o) => o.organization.id === org.id)!;
    expect(inOrg.organization.role).toBe('admin');
    expect(inOrg.monitorsCreated.map((m) => m.name)).toEqual(['my-monitor']);
    expect(inOrg.apiKeysCreated).toHaveLength(1);
    expect(inOrg.auditEvents.map((e) => e.action)).toEqual(expect.arrayContaining(['monitor.created', 'api_key.created']));
    for (const secret of ['SECRET-HASH', 'gho_SECRET_TOKEN', 'SESSION-TOKEN-XYZ', key.key]) expect(text).not.toContain(secret);
    // Another org's data never appears, even with identical names.
    const other = await makeOrg('Portable-other');
    await createMonitor({ orgId: other.id, userId: other.users.owner.id }, { name: 'my-monitor', url: 'https://theirs.test', intervalSeconds: 300 });
    expect(JSON.stringify(await exportUserData(me.id))).not.toContain('theirs.test');
  });
});

describe('a user deletes their account', () => {
  it('a member leaves: the user and their sessions are gone, their monitors stay with the org, both logs say so', async () => {
    const org = await makeOrg('Leavers');
    const me = org.users.member;
    const monitor = await createMonitor({ orgId: org.id, userId: me.id }, { name: 'left-behind', url: 'https://left.test', intervalSeconds: 300 });
    await db.insert(schema.sessions).values({ userId: me.id, token: 'tok-leaver', expiresAt: new Date(Date.now() + DAY_MS) });

    await expect(deleteAccount(me, { confirmEmail: 'someone-else@example.com', source: SOURCE })).rejects.toBeInstanceOf(InvalidRequestError);
    await deleteAccount(me, { confirmEmail: me.email.toUpperCase(), source: SOURCE });

    expect(await db.select().from(schema.users).where(eq(schema.users.id, me.id))).toEqual([]);
    expect(await db.select().from(schema.sessions).where(eq(schema.sessions.userId, me.id))).toEqual([]);
    expect(await db.select().from(schema.memberships).where(eq(schema.memberships.userId, me.id))).toEqual([]);
    const [kept] = await withOrg(org.id, (tx) => tx.select().from(schema.monitors).where(eq(schema.monitors.id, monitor.id)));
    expect(kept.createdBy).toBeNull();
    const events = await db.select().from(schema.auditEvents).where(eq(schema.auditEvents.targetId, me.id));
    expect(events.map((e) => [e.action, e.organizationId])).toEqual(expect.arrayContaining([['member.account_deleted', org.id], ['account.deleted', null]]));
  });

  it('the only owner of an org with other members is refused until someone else is owner', async () => {
    const org = await makeOrg('Stuck');
    const plan = await accountDeletionPlan(org.users.owner.id);
    expect(plan.blockers.join()).toMatch(/only owner of Stuck/);
    await expect(deleteAccount(org.users.owner, { confirmEmail: org.users.owner.email, source: SOURCE })).rejects.toThrow(/only owner of Stuck/);
    // A second owner resolves it.
    await db.update(schema.memberships).set({ role: 'owner' }).where(and(eq(schema.memberships.organizationId, org.id), eq(schema.memberships.userId, org.users.admin.id)));
    expect((await accountDeletionPlan(org.users.owner.id)).blockers).toEqual([]);
  });

  it('Beacon staff are refused here', async () => {
    const staff = await makeUser('staffer');
    await db.insert(schema.staffUsers).values({ userId: staff.id, role: 'support' });
    expect((await accountDeletionPlan(staff.id)).blockers.join()).toMatch(/staff/);
  });

  it('the only member of an org: the org is scheduled for deletion with the account, and purged after the grace period', async () => {
    const solo = await makeUser('Solo');
    const { createOrganization } = await import('@/lib/organizations');
    const org = await createOrganization(solo.id, 'Solo Co');
    await createMonitor({ orgId: org.id, userId: solo.id }, { name: 'solo', url: 'https://solo.test', intervalSeconds: 300 });
    expect((await accountDeletionPlan(solo.id)).orgsToDelete.map((o) => o.name)).toContain('Solo Co');

    await deleteAccount(solo, { confirmEmail: solo.email, source: SOURCE });
    const [row] = await db.select().from(schema.organizations).where(eq(schema.organizations.id, org.id));
    expect(row.deletionScheduledFor!.getTime()).toBeGreaterThan(Date.now() + 6 * DAY_MS);
    expect((await jobsIn('org.delete')).some((j) => j.data.orgId === org.id)).toBe(true);

    await purgeOrganization(org.id, new Date(Date.now() + 8 * DAY_MS));
    expect(Object.values(await countOrgRows(org.id)).every((n) => n === 0)).toBe(true);
  });
});

describe('an owner exports the organization (through the queue)', () => {
  it('builds one JSON file with every tenant table and no secrets; only this org’s owner can download it', async () => {
    const org = await makeOrg('Exporter');
    const other = await makeOrg('Exporter-other');
    await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name: 'exported', url: 'https://exported.test', intervalSeconds: 300 });
    const { secret } = await createEndpoint({ orgId: org.id, userId: org.users.owner.id }, { url: 'https://hooks.public.test/x', eventTypes: ['incident.opened'] });
    const key = await createApiKey({ orgId: org.id, userId: org.users.owner.id, role: 'owner' }, { name: 'exp', scopes: ['monitors:read'] });

    const { id } = await requestOrgExport(owner(org));
    expect(await requestOrgExport(owner(org))).toEqual({ id }); // a second click while pending: the same export
    await runQueuedJobs({ queues: ['org.export'] });
    const [row] = await withOrg(org.id, (tx) => tx.select().from(schema.orgExports).where(eq(schema.orgExports.id, id)));
    expect(row).toMatchObject({ status: 'ready', storageKey: `orgs/${org.id}/exports/${id}.json` });

    const text = new TextDecoder().decode(await getStorage().get(row.storageKey!));
    const doc = JSON.parse(text);
    expect(doc.format).toBe('beacon-organization-export');
    expect(doc.members.map((m: { email: string }) => m.email)).toContain(org.users.owner.email);
    expect(Object.keys(doc.tables).sort()).toEqual(tenantTables().map((t) => t.name).filter((n) => !NOT_EXPORTED[n]).sort());
    expect(doc.tables.monitors.map((m: { name: string }) => m.name)).toEqual(['exported']);
    expect(doc.tables.audit_events.length).toBeGreaterThan(0);
    for (const s of [secret, key.key, 'enc:v1:', 'key_hash', 'keyHash']) expect(text).not.toContain(s);
    expect(text).not.toContain(other.id);

    expect(await exportDownloadUrl(owner(org), id)).toMatch(/\/api\/storage\//);
    // Another org's owner, with this export's id: not found (lesson 1.3, BOLA).
    await expect(exportDownloadUrl(owner(other), id)).rejects.toBeInstanceOf(AccessError);
    const downloads = await db.select().from(schema.auditEvents).where(eq(schema.auditEvents.action, 'org.export_downloaded'));
    expect(downloads.map((d) => d.organizationId)).toEqual([org.id]);
  });

  it('buildOrgExport never reads another org’s rows', async () => {
    const a = await makeOrg('Iso-A');
    const b = await makeOrg('Iso-B');
    await createMonitor({ orgId: b.id, userId: b.users.owner.id }, { name: 'b-only', url: 'https://b.test', intervalSeconds: 300 });
    const doc = await buildOrgExport(a.id);
    expect(JSON.stringify(doc)).not.toContain('b-only');
    expect(JSON.stringify(doc)).not.toContain(b.id);
  });
});

describe('an owner deletes the organization (offboarding)', () => {
  it('is refused with a wrong confirmation or an active paid subscription', async () => {
    const org = await makeOrg('Paying');
    await expect(requestOrgDeletion(owner(org), 'nope')).rejects.toThrow(/Type the organization/);
    await db.insert(schema.subscriptions).values({ id: `sub_${org.id}`, organizationId: org.id, stripeCustomerId: 'cus_x', status: 'active', priceId: 'price_fake_pro' });
    await expect(requestOrgDeletion(owner(org), org.slug)).rejects.toThrow(/active paid subscription/);
  });

  it('stops checks and hides the status page at once, can be cancelled, and after the grace period leaves no row and no file', async () => {
    const org = await makeOrg('Goodbye');
    const neighbour = await makeOrg('Neighbour');
    await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name: 'bye', url: 'https://bye.test', intervalSeconds: 60 });
    await createMonitor({ orgId: neighbour.id, userId: neighbour.users.owner.id }, { name: 'stay', url: 'https://stay.test', intervalSeconds: 60 });
    const logoKey = `orgs/${org.id}/logos/${crypto.randomUUID()}`;
    await getStorage().put(logoKey, new Uint8Array([1, 2, 3]), 'image/png');
    await withOrg(org.id, (tx) => tx.insert(schema.files).values({ organizationId: org.id, kind: 'logo', key: logoKey, originalName: 'x.png', declaredType: 'image/png', declaredSize: 3, status: 'ready' }));
    expect(await findPublicStatusPage(org.slug)).not.toBeNull();

    const at = await requestOrgDeletion(owner(org), org.slug);
    expect(await findPublicStatusPage(org.slug)).toBeNull();
    await scheduleChecks();
    const checks = await jobsIn('check.run');
    expect(checks.some((j) => j.data.orgId === org.id)).toBe(false);
    expect(checks.some((j) => j.data.orgId === neighbour.id)).toBe(true);

    // Cancel, then ask again: the first job finds nothing to do.
    expect(await cancelOrgDeletion(owner(org))).toBe(true);
    expect(await purgeOrganization(org.id, new Date(at.getTime() + 1000))).toEqual({ skipped: 'deletion cancelled' });
    const again = await requestOrgDeletion(owner(org), org.slug);
    expect(await purgeOrganization(org.id)).toMatchObject({ skipped: expect.stringMatching(/^scheduled for/) });

    // The grace period is over: the delayed job runs.
    await pg().query(`update pgboss.job set start_after = now() - interval '1 second' where name = 'org.delete'`);
    vi.useFakeTimers({ now: again.getTime() + 60_000, toFake: ['Date'] });
    try {
      await jobsAreDue('org.delete');
      await runQueuedJobs({ queues: ['org.delete'] });
    } finally {
      vi.useRealTimers();
    }
    const left = await countOrgRows(org.id);
    expect(Object.entries(left).filter(([, n]) => n > 0)).toEqual([]);
    expect(Object.keys(left).length).toBeGreaterThan(20); // every tenant table was checked
    expect(await getStorage().head(logoKey)).toBeNull();
    expect((await countOrgRows(neighbour.id)).monitors).toBe(1);
    const [deleted] = await db.select().from(schema.auditEvents).where(and(eq(schema.auditEvents.action, 'org.deleted'), eq(schema.auditEvents.targetId, org.id)));
    expect(deleted).toMatchObject({ organizationId: null, targetName: 'Goodbye' });
  });
});

describe('retention (the nightly retention.purge job)', () => {
  it('deletes what is past its time and keeps the rest, pending emails included', async () => {
    const org = await makeOrg('Retained');
    const m = await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name: 'old', url: 'https://old.test', intervalSeconds: 300 });
    const old = new Date(Date.now() - (RETENTION_RULES.checkResults.days + 1) * DAY_MS);
    await withOrg(org.id, (tx) =>
      tx.insert(schema.checkResults).values([
        { organizationId: org.id, monitorId: m.id, ok: true, checkedAt: old },
        { organizationId: org.id, monitorId: m.id, ok: true, checkedAt: new Date() },
      ]),
    );
    const oldMail = new Date(Date.now() - (RETENTION_RULES.emailOutbox.days + 1) * DAY_MS);
    await db.insert(schema.emailOutbox).values([
      { idempotencyKey: 'ret-sent', to: 'a@example.com', template: 'verify-email', props: {}, status: 'sent', createdAt: oldMail },
      { idempotencyKey: 'ret-pending', to: 'b@example.com', template: 'verify-email', props: {}, status: 'pending', createdAt: oldMail },
    ]);
    const deleted = await purgeExpiredData();
    expect(deleted.check_results).toBeGreaterThanOrEqual(1);
    expect(deleted.email_outbox).toBeGreaterThanOrEqual(1);
    const left = await withOrg(org.id, (tx) => tx.select().from(schema.checkResults).where(eq(schema.checkResults.monitorId, m.id)));
    expect(left).toHaveLength(1);
    const keys = (await db.select().from(schema.emailOutbox)).map((e) => e.idempotencyKey);
    expect(keys).toContain('ret-pending');
    expect(keys).not.toContain('ret-sent');
    expect(await db.select().from(schema.auditEvents).where(eq(schema.auditEvents.action, 'retention.purged'))).not.toHaveLength(0);
  });
});
