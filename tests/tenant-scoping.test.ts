import { readdirSync, readFileSync, statSync } from 'node:fs';
import path from 'node:path';
import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { sql } from 'drizzle-orm';
import { PGlite } from '@electric-sql/pglite';
import * as dbModule from '@/db';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { createMonitor } from '@/lib/monitors';
import { makeOrg } from './helpers/fixtures';

/*
 * Lesson 2.4: the tenant boundary is enforced by the system, not remembered.
 *   1. Row-level security: queries inside withOrg() see and write only the
 *      current org's rows, even when the WHERE organization_id is missing.
 *   2. A "lint rule" as a test: no code reaches a tenant table except
 *      through withOrg(), and no tenant table lacks a policy.
 */
const pg = (dbModule as unknown as { sql: PGlite }).sql;
const { monitors, incidents } = schema;

let acme: Awaited<ReturnType<typeof makeOrg>>;
let globex: Awaited<ReturnType<typeof makeOrg>>;
let acmeMonitorId: string;
let globexMonitorId: string;

beforeAll(async () => {
  acme = await makeOrg('Acme');
  globex = await makeOrg('Globex');
  // Identical names in both orgs: nothing may tell them apart except the org.
  acmeMonitorId = (await createMonitor({ orgId: acme.id, userId: acme.users.owner.id }, { name: 'api', url: 'https://acme.test', intervalSeconds: 60 })).id;
  globexMonitorId = (await createMonitor({ orgId: globex.id, userId: globex.users.owner.id }, { name: 'api', url: 'https://globex.test', intervalSeconds: 60 })).id;
  await db.insert(incidents).values([
    { organizationId: acme.id, monitorId: acmeMonitorId, cause: 'acme down' },
    { organizationId: globex.id, monitorId: globexMonitorId, cause: 'globex down' },
  ]);
});

/** The Postgres error behind a Drizzle error (Drizzle wraps it as `cause`). */
function pgMessage(err: unknown): string {
  const e = err as { message?: string; cause?: { message?: string } };
  return e.cause?.message ?? e.message ?? '';
}

describe('row-level security (defence in depth)', () => {
  it('a query with the WHERE organization_id deleted still returns only the current org’s rows', async () => {
    const rows = await withOrg(acme.id, (tx) => tx.select().from(monitors)); // no WHERE at all
    expect(rows.map((r) => r.id)).toEqual([acmeMonitorId]);
    const allIncidents = await withOrg(globex.id, (tx) => tx.select().from(incidents));
    expect(allIncidents.map((i) => i.cause)).toEqual(['globex down']);
  });

  it('inserting a monitor with another org’s id fails with an RLS violation', async () => {
    const attempt = withOrg(acme.id, (tx) =>
      tx.insert(monitors).values({ organizationId: globex.id, name: 'planted', url: 'https://evil.test' }),
    );
    await expect(attempt.catch((e) => Promise.reject(new Error(pgMessage(e))))).rejects.toThrow(/row-level security/);
  });

  it('updates and deletes cannot reach another org’s rows, even by id', async () => {
    const updated = await withOrg(acme.id, (tx) => tx.update(monitors).set({ name: 'hijacked' }).where(sql`id = ${globexMonitorId}`).returning());
    const deleted = await withOrg(acme.id, (tx) => tx.delete(monitors).where(sql`id = ${globexMonitorId}`).returning());
    expect(updated).toEqual([]);
    expect(deleted).toEqual([]);
    // Nor can a row be moved into another org.
    const moved = withOrg(acme.id, (tx) => tx.update(monitors).set({ organizationId: globex.id }).where(sql`id = ${acmeMonitorId}`));
    await expect(moved.catch((e) => Promise.reject(new Error(pgMessage(e))))).rejects.toThrow(/row-level security/);
  });

  it('fails closed: as the app role with no org set, a tenant table looks empty', async () => {
    const rows = await db.transaction(async (tx) => {
      await tx.execute(sql`select set_config('role', 'beacon_app', true)`);
      return tx.select().from(monitors);
    });
    expect(rows).toEqual([]);
  });

  it('the SECURITY DEFINER search functions (lesson 2.3) also return nothing without an org', async () => {
    const found = await db.transaction(async (tx) => {
      await tx.execute(sql`select set_config('role', 'beacon_app', true)`);
      const result = (await tx.execute(sql`select * from search_monitors('api', 10)`)) as unknown as { rows: unknown[] };
      return result.rows;
    });
    expect(found).toEqual([]);
    const inAcme = await withOrg(acme.id, async (tx) => ((await tx.execute(sql`select id from search_monitors('api', 10)`)) as unknown as { rows: { id: string }[] }).rows);
    expect(inAcme.map((r) => r.id)).toEqual([acmeMonitorId]);
  });

  it('leaves nothing behind on the connection (safe behind a transaction-mode pooler)', async () => {
    await withOrg(acme.id, (tx) => tx.select().from(monitors));
    // PGlite has exactly one connection, so this is "the next transaction on
    // the same server connection", like the next request through PgBouncer.
    const { rows } = await pg.query<{ org: string; role: string }>(`select current_setting('app.current_org', true) as org, current_user as role`);
    expect(rows[0].org).toBe('');
    expect(rows[0].role).not.toBe('beacon_app');
  });

  it('a rolled-back transaction does not leak its org either', async () => {
    await withOrg(acme.id, async () => {
      throw new Error('boom');
    }).catch(() => {});
    const { rows } = await pg.query<{ org: string }>(`select current_setting('app.current_org', true) as org`);
    expect(rows[0].org).toBe('');
  });
});

/*
 * The tables that carry organization_id but are deliberately NOT under RLS:
 * they are read before the org is known (at login, from an invitation token).
 * Adding a table here is a design decision to explain in review.
 */
const NOT_UNDER_RLS = [
  'memberships',
  'invitations',
  // Lesson 5.2: the key is how an API request finds its org; looked up by hash before any org is known.
  'api_keys',
  // Lesson 6.3: per-org flag targeting is platform configuration written by Beacon staff, not tenant
  // data. Every process loads the whole rule set to evaluate flags in memory (local evaluation).
  'feature_flag_overrides',
  // Lesson 7.1: looked up on every request of a staff member, before any org is known; the app
  // role has no rights on it at all (migration 0024), only the owner (staff code) reads it.
  'impersonation_sessions',
];

describe('every tenant table is protected', () => {
  it('has row-level security enabled with a policy, unless it is on the short list above', async () => {
    const { rows } = await pg.query<{ table_name: string; rls: boolean; policies: number }>(`
      select c.table_name, cl.relrowsecurity as rls,
             (select count(*)::int from pg_policies p where p.tablename = c.table_name) as policies
      from information_schema.columns c
      join pg_class cl on cl.relname = c.table_name and cl.relkind = 'r'
      where c.table_schema = 'public' and c.column_name = 'organization_id'
      order by 1`);
    const unprotected = rows.filter((r) => !NOT_UNDER_RLS.includes(r.table_name) && (!r.rls || r.policies === 0));
    expect(unprotected.map((r) => r.table_name)).toEqual([]);
    expect(rows.length).toBeGreaterThan(NOT_UNDER_RLS.length); // the query really found tenant tables
  });
});

/*
 * Lesson 2.4 (🟢), "enforced by a lint rule": a test that reads the source.
 * Tenant tables are touched only through `tx` inside withOrg(); a direct
 * `db.select()…from(monitors)` anywhere in the app or the check runner fails
 * here. Admin scripts that connect as the database owner (seed, reset,
 * claim-org) are exempt: they are not reachable from a request.
 */
const TENANT_TABLES = [
  'monitors', 'checkResults', 'incidents', 'incidentUpdates', 'files', 'subscriptions', 'usageEvents', 'usageAlerts',
  // Module 4
  'notifications', 'notificationPreferences', 'orgNotificationPolicies', 'notificationDeliveries', 'statusPageSubscribers', 'presence',
  // Module 5
  'apiIdempotencyKeys', 'webhookEndpoints', 'webhookEvents', 'webhookMessages', 'webhookAttempts',
  'workflowRuns', 'workflowSteps', 'workflowSignals', 'escalationPolicies',
  // Module 6
  'orgMilestones', 'analyticsEvents',
  // Module 7
  'auditEvents',
];
const SCANNED = ['src', 'scripts/run-checks.ts', 'scripts/report-usage.ts', 'scripts/worker.ts', 'scripts/jobs.ts'];
const EXEMPT = [
  'src/db/tenant.ts', 'src/db/schema.ts', 'src/db/index.ts',
  // Lesson 6.2: the internal activation funnel reads across every org by design (staff only, /internal).
  'src/lib/analytics/funnel.ts',
  // Lessons 7.1/7.3: the staff side of Beacon reads across orgs as the owner (never from a customer
  // request): the admin panel, the audit verifier and retention job.
  'src/lib/admin/audit.ts', 'src/lib/admin/customers.ts',
];

function sourceFiles(p: string): string[] {
  let stat;
  try {
    stat = statSync(p);
  } catch {
    return []; // a scanned script that does not exist yet
  }
  if (stat.isFile()) return /\.(ts|tsx)$/.test(p) ? [p] : [];
  return readdirSync(p).flatMap((f) => sourceFiles(path.join(p, f)));
}

describe('lint: tenant tables only through withOrg()', () => {
  const files = SCANNED.flatMap(sourceFiles).filter((f) => !EXEMPT.includes(f.split(path.sep).join('/')));

  it('scans the app', () => {
    expect(files.length).toBeGreaterThan(20);
  });

  it('no direct db query mentions a tenant table', () => {
    const offenders: string[] = [];
    for (const file of files) {
      const text = readFileSync(file, 'utf8');
      // Each `db.select(…)`, `db.insert(…)` … up to the end of its statement.
      for (const m of text.matchAll(/\bdb\s*\.\s*(select|selectDistinct|insert|update|delete|execute|query|\$count)\b[\s\S]*?;/g)) {
        const hit = TENANT_TABLES.find((t) => new RegExp(`\\b${t}\\b`).test(m[0]));
        if (hit) offenders.push(`${file}: db.${m[1]}(…) on ${hit}`);
      }
    }
    expect(offenders).toEqual([]);
  });

  it('db.transaction() is used only where the tables are not tenant tables', () => {
    // email/index.ts: the outbox row and its job (lesson 5.1); email_outbox is not a tenant table.
    // rate-limit.ts: one bucket row locked per request (lesson 5.2); rate_limit_buckets is not a tenant table.
    // Module 7: staff-side writes run as the owner in one transaction with their audit event (impersonation
    // sessions and platform events such as flag changes are not tenant rows; beacon_app may not touch them).
    // Module 8: the platform audit events of key rotation (secrets/maintenance.ts).
    const allowed = [
      'src/lib/organizations.ts', 'src/lib/invitations.ts', 'src/lib/email/index.ts', 'src/lib/rate-limit.ts',
      'src/lib/admin/audit.ts', 'src/lib/admin/support.ts', 'src/lib/admin/staff.ts', 'src/lib/impersonation.ts', 'src/lib/flags/store.ts',
      'src/lib/secrets/maintenance.ts',
    ];
    const users = files.filter((f) => /\bdb\s*\.\s*transaction\s*\(/.test(readFileSync(f, 'utf8'))).map((f) => f.split(path.sep).join('/'));
    expect(users.filter((f) => !allowed.includes(f))).toEqual([]);
  });
});
