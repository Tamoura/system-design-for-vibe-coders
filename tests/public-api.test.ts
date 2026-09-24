import { readdirSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { bearerToken, canGrantScopes, generateApiKey, hashApiKey, looksLikeApiKey, type ApiScope } from '@/core/api-keys';
import { fromPublicId, toPublicId } from '@/core/ids';
import { buildOpenApiDocument } from '@/core/openapi';
import { perMinute, takeToken } from '@/core/rate-limit';
import { createApiKey, listApiKeys, revokeApiKey } from '@/lib/api-keys';
import { AccessError } from '@/lib/errors';
import { createMonitor } from '@/lib/monitors';
import * as monitorsRoute from '@/app/api/v1/monitors/route';
import * as monitorRoute from '@/app/api/v1/monitors/[id]/route';
import * as incidentsRoute from '@/app/api/v1/incidents/route';
import * as incidentRoute from '@/app/api/v1/incidents/[id]/route';
import * as openapiRoute from '@/app/api/v1/openapi.json/route';
import { makeOrg } from './helpers/fixtures';

/*
 * Lesson 5.2: the public API. Keys (hashed, scoped, revocable), plan gate,
 * RFC 9457 errors, cursor pagination, idempotency keys, rate limits, the
 * OpenAPI document, and cross-tenant safety: a key from org B never sees org A.
 */
type Org = Awaited<ReturnType<typeof makeOrg>>;
const owner = (org: Org) => ({ orgId: org.id, userId: org.users.owner.id, role: 'owner' as const });
const ALL: ApiScope[] = ['monitors:read', 'monitors:write', 'incidents:read'];

function call(handler: (req: Request, ctx: { params: Promise<never> }) => Promise<Response>, url: string, init: RequestInit & { key?: string; params?: object } = {}) {
  const headers = new Headers(init.headers);
  if (init.key) headers.set('authorization', `Bearer ${init.key}`);
  if (init.body) headers.set('content-type', 'application/json');
  return handler(new Request(`http://test${url}`, { ...init, headers }), { params: Promise.resolve((init.params ?? {}) as never) });
}
const json = (body: unknown) => JSON.stringify(body);

async function expectProblem(res: Response, status: number, type: string) {
  expect(res.status).toBe(status);
  expect(res.headers.get('content-type')).toBe('application/problem+json');
  const body = await res.json();
  expect(body).toMatchObject({ type: `https://beacon.app/problems/${type}`, title: expect.any(String), status });
  return body;
}

let acme: Org;
let globex: Org;
let acmeKey: string;
let globexKey: string;

beforeAll(async () => {
  acme = await makeOrg('ApiAcme'); // Business: includes the API
  globex = await makeOrg('ApiGlobex');
  acmeKey = (await createApiKey(owner(acme), { name: 'acme-all', scopes: ALL })).key;
  globexKey = (await createApiKey(owner(globex), { name: 'globex-all', scopes: ALL })).key;
});

describe('API keys (🟢)', () => {
  it('are prefixed, random, and only their SHA-256 hash is stored', async () => {
    const a = generateApiKey();
    expect(a.key).toMatch(/^bk_live_[A-Za-z0-9_-]{43}$/);
    expect(a.key).not.toBe(generateApiKey().key);
    expect(a.hash).toBe(hashApiKey(a.key));
    expect(looksLikeApiKey(a.key)).toBe(true);
    expect(looksLikeApiKey('sk_live_nope')).toBe(false);
    expect(bearerToken(`Bearer ${a.key}`)).toBe(a.key);
    expect(bearerToken(a.key)).toBeNull();

    const rows = await db.select().from(schema.apiKeys);
    const dump = JSON.stringify(rows);
    for (const key of [acmeKey, globexKey]) {
      expect(dump).not.toContain(key);
      expect(dump).toContain(hashApiKey(key));
    }
    const [listed] = (await listApiKeys({ orgId: acme.id })).filter((k) => k.name === 'acme-all');
    expect(listed).toMatchObject({ keyStart: acmeKey.slice(0, 12), keyLast4: acmeKey.slice(-4), scopes: ALL });
    expect(JSON.stringify(listed)).not.toContain(acmeKey);
  });

  it('only owners and admins can create keys, and never with more than their role (lesson 1.3)', async () => {
    expect(canGrantScopes('admin', ALL)).toBe(true);
    expect(canGrantScopes('member', ['monitors:read'])).toBe(false); // no integration.manage
    await expect(createApiKey({ orgId: acme.id, userId: acme.users.member.id, role: 'member' }, { name: 'x', scopes: ['monitors:read'] })).rejects.toBeInstanceOf(AccessError);
  });

  it('a revoked key gets 401 on the very next request; last used is recorded', async () => {
    const { id, key } = await createApiKey(owner(acme), { name: 'short-lived', scopes: ['monitors:read'] });
    expect((await call(monitorsRoute.GET, '/api/v1/monitors', { key })).status).toBe(200);
    const [used] = (await listApiKeys({ orgId: acme.id })).filter((k) => k.id === id);
    expect(used.lastUsedAt).toBeInstanceOf(Date);
    await revokeApiKey(owner(acme), id);
    await expectProblem(await call(monitorsRoute.GET, '/api/v1/monitors', { key }), 401, 'unauthenticated');
  });

  it('another org cannot revoke Acme’s key', async () => {
    const [k] = await listApiKeys({ orgId: acme.id });
    await expect(revokeApiKey(owner(globex), k.id)).rejects.toBeInstanceOf(AccessError);
  });
});

describe('authentication, plan and scopes', () => {
  it('no key, a malformed key and an unknown key are 401 problem details', async () => {
    const res = await call(monitorsRoute.GET, '/api/v1/monitors');
    const body = await expectProblem(res, 401, 'unauthenticated');
    expect(res.headers.get('www-authenticate')).toContain('Bearer');
    expect(body.instance).toBe('/api/v1/monitors');
    await expectProblem(await call(monitorsRoute.GET, '/api/v1/monitors', { key: 'nope' }), 401, 'unauthenticated');
    await expectProblem(await call(monitorsRoute.GET, '/api/v1/monitors', { key: generateApiKey().key }), 401, 'unauthenticated');
  });

  it('an org whose plan does not include the API gets 402 with the plan to upgrade to (lesson 3.2)', async () => {
    const free = await makeOrg('ApiFree', { plan: 'pro' });
    const { key } = await createApiKey(owner(free), { name: 'k', scopes: ALL });
    const body = await expectProblem(await call(monitorsRoute.GET, '/api/v1/monitors', { key }), 402, 'plan-upgrade-required');
    expect(body.upgrade_to).toBe('business');
  });

  it('a read-only key cannot write: 403 insufficient-scope', async () => {
    const { key } = await createApiKey(owner(acme), { name: 'read-only', scopes: ['monitors:read'] });
    const res = await call(monitorsRoute.POST, '/api/v1/monitors', { key, method: 'POST', body: json({ name: 'x', url: 'https://x.test' }) });
    const body = await expectProblem(res, 403, 'insufficient-scope');
    expect(body.required_scope).toBe('monitors:write');
    await expectProblem(await call(incidentsRoute.GET, '/api/v1/incidents', { key }), 403, 'insufficient-scope');
  });
});

describe('monitors', () => {
  it('POST creates a monitor in the key’s org (201), with prefixed ids and snake_case fields', async () => {
    const res = await call(monitorsRoute.POST, '/api/v1/monitors', {
      key: acmeKey,
      method: 'POST',
      body: json({ name: 'Checkout API', url: 'https://checkout.acme.test/health', interval_seconds: 60, organizationId: globex.id }),
    });
    expect(res.status).toBe(201);
    const monitor = await res.json();
    expect(monitor).toEqual({
      id: expect.stringMatching(/^mon_[0-9a-f]{32}$/),
      name: 'Checkout API',
      url: 'https://checkout.acme.test/health',
      interval_seconds: 60,
      paused: false,
      paused_reason: null,
      created_at: expect.any(String),
    });
    const [row] = await db.select().from(schema.monitors).where(eq(schema.monitors.id, fromPublicId('monitor', monitor.id)!));
    expect(row.organizationId).toBe(acme.id); // the key decides the org; the body cannot
    expect(res.headers.get('ratelimit-policy')).toBe('"api";q=120;w=60');
    expect(res.headers.get('x-ratelimit-remaining')).toMatch(/^\d+$/);
  });

  it('validation errors are 422 with one entry per field; bad JSON is 400; an internal URL is 400 blocked-url', async () => {
    const res = await call(monitorsRoute.POST, '/api/v1/monitors', { key: acmeKey, method: 'POST', body: json({ name: '', url: 'not a url', interval_seconds: 7 }) });
    const body = await expectProblem(res, 422, 'validation-failed');
    expect([...new Set(body.errors.map((e: { field: string }) => e.field))].sort()).toEqual(['interval_seconds', 'name', 'url']);
    await expectProblem(await call(monitorsRoute.POST, '/api/v1/monitors', { key: acmeKey, method: 'POST', body: '{"name":' }), 400, 'invalid-json');
    const blocked = await call(monitorsRoute.POST, '/api/v1/monitors', { key: acmeKey, method: 'POST', body: json({ name: 'meta', url: 'http://169.254.169.254/latest/meta-data/' }) });
    expect((await expectProblem(blocked, 400, 'blocked-url')).detail).toMatch(/link-local/);
  });

  it('PATCH and DELETE work by prefixed id; a malformed or unknown id is 404', async () => {
    const m = await createMonitor({ orgId: acme.id, userId: acme.users.owner.id }, { name: 'to-change', url: 'https://change.test', intervalSeconds: 300 });
    const id = toPublicId('monitor', m.id);
    const patched = await call(monitorRoute.PATCH, `/api/v1/monitors/${id}`, { key: acmeKey, method: 'PATCH', body: json({ paused: true }), params: { id } });
    expect(await patched.json()).toMatchObject({ id, paused: true, paused_reason: 'manual' });
    expect((await call(monitorRoute.DELETE, `/api/v1/monitors/${id}`, { key: acmeKey, method: 'DELETE', params: { id } })).status).toBe(204);
    await expectProblem(await call(monitorRoute.GET, `/api/v1/monitors/${id}`, { key: acmeKey, params: { id } }), 404, 'not-found');
    await expectProblem(await call(monitorRoute.GET, '/api/v1/monitors/123', { key: acmeKey, params: { id: '123' } }), 404, 'not-found');
    await expectProblem(await call(monitorRoute.GET, `/api/v1/monitors/${m.id}`, { key: acmeKey, params: { id: m.id } }), 404, 'not-found'); // a bare uuid is not an id here
  });
});

describe('cursor pagination (🟢)', () => {
  let org: Org;
  let key: string;

  beforeAll(async () => {
    org = await makeOrg('Pages');
    key = (await createApiKey(owner(org), { name: 'pages', scopes: ALL })).key;
    for (let i = 0; i < 7; i++) await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name: `m${i}`, url: `https://m${i}.test`, intervalSeconds: 300 });
  });

  it('walks every monitor exactly once, newest first, following next_cursor', async () => {
    const seen: string[] = [];
    let cursor: string | null = null;
    let pages = 0;
    do {
      const url: string = `/api/v1/monitors?limit=3${cursor ? `&starting_after=${cursor}` : ''}`;
      const body = await (await call(monitorsRoute.GET, url, { key })).json();
      seen.push(...body.data.map((m: { name: string }) => m.name));
      expect(body.has_more).toBe(body.next_cursor !== null);
      cursor = body.next_cursor;
      pages++;
    } while (cursor);
    expect(pages).toBe(3);
    expect(seen).toEqual(['m6', 'm5', 'm4', 'm3', 'm2', 'm1', 'm0']);
  });

  it('a monitor added between two pages does not shift the next page (unlike OFFSET)', async () => {
    const first = await (await call(monitorsRoute.GET, '/api/v1/monitors?limit=2', { key })).json();
    await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name: 'late', url: 'https://late.test', intervalSeconds: 300 });
    const second = await (await call(monitorsRoute.GET, `/api/v1/monitors?limit=2&starting_after=${first.next_cursor}`, { key })).json();
    expect(second.data.map((m: { name: string }) => m.name)).toEqual(['m4', 'm3']);
  });

  it('limit has a maximum (100); a bad limit or cursor is 400', async () => {
    await expectProblem(await call(monitorsRoute.GET, '/api/v1/monitors?limit=101', { key }), 400, 'invalid-parameter');
    await expectProblem(await call(monitorsRoute.GET, '/api/v1/monitors?limit=0', { key }), 400, 'invalid-parameter');
    await expectProblem(await call(monitorsRoute.GET, '/api/v1/monitors?starting_after=inc_00', { key }), 400, 'invalid-parameter');
    const [acmeMonitor] = await db.select().from(schema.monitors).where(eq(schema.monitors.organizationId, acme.id));
    // Another org's monitor is not a cursor here (and reveals nothing about it).
    await expectProblem(await call(monitorsRoute.GET, `/api/v1/monitors?starting_after=${toPublicId('monitor', acmeMonitor.id)}`, { key }), 400, 'invalid-parameter');
  });
});

describe('Idempotency-Key on POST (🟡)', () => {
  const post = (key: string, idem: string, body: object) =>
    call(monitorsRoute.POST, '/api/v1/monitors', { key, method: 'POST', body: json(body), headers: { 'idempotency-key': idem } });

  it('the same POST twice with the same key creates one monitor and returns the same body twice', async () => {
    const body = { name: 'idem', url: 'https://idem.test', interval_seconds: 300 };
    const a = await post(acmeKey, 'retry-123', body);
    const b = await post(acmeKey, 'retry-123', body);
    expect(a.status).toBe(201);
    expect(b.status).toBe(201);
    expect(b.headers.get('idempotent-replayed')).toBe('true');
    expect(await b.json()).toEqual(await a.json());
    const rows = await db.select().from(schema.monitors).where(eq(schema.monitors.name, 'idem'));
    expect(rows).toHaveLength(1);
  });

  it('the same key with a different body is a 422; the same key in another org is independent', async () => {
    await expectProblem(await post(acmeKey, 'retry-123', { name: 'other', url: 'https://other.test' }), 422, 'idempotency-key-reused');
    expect((await post(globexKey, 'retry-123', { name: 'idem', url: 'https://idem.test', interval_seconds: 300 })).status).toBe(201);
  });

  it('while the first request is still running, a retry gets 409; after a failed request the key is free again', async () => {
    await db.insert(schema.apiIdempotencyKeys).values({ organizationId: acme.id, key: 'in-flight', requestMethod: 'POST', requestPath: '/api/v1/monitors', requestHash: 'x' });
    const res = await call(monitorsRoute.POST, '/api/v1/monitors', { key: acmeKey, method: 'POST', body: 'x', headers: { 'idempotency-key': 'in-flight' } });
    expect(res.status).toBe(422); // different body hash than the stored claim
    const same = { name: 'x', url: 'https://x.test' };
    const { createHash } = await import('node:crypto');
    const hash = createHash('sha256').update(`POST /api/v1/monitors\n${json(same)}`).digest('hex');
    await db.insert(schema.apiIdempotencyKeys).values({ organizationId: acme.id, key: 'in-flight-2', requestMethod: 'POST', requestPath: '/api/v1/monitors', requestHash: hash });
    await expectProblem(await post(acmeKey, 'in-flight-2', same), 409, 'idempotency-key-in-use');

    await expectProblem(await post(acmeKey, 'fails-first', { name: '' }), 422, 'validation-failed');
    // Only successful responses are kept: after the 422 the key was released,
    // so the client can fix the body and retry with the same key.
    expect(await db.select().from(schema.apiIdempotencyKeys).where(eq(schema.apiIdempotencyKeys.key, 'fails-first'))).toEqual([]);
    expect((await post(acmeKey, 'fails-first', { name: 'fixed', url: 'https://fixed.test' })).status).toBe(201);
    expect((await post(acmeKey, 'fails-first', { name: 'fixed', url: 'https://fixed.test' })).headers.get('idempotent-replayed')).toBe('true');
  });
});

describe('rate limiting (token bucket)', () => {
  it('allows a burst up to the capacity, then refills at the steady rate', () => {
    const policy = perMinute('api', 60); // 60 now, then 1 per second
    const t0 = new Date('2026-01-01T00:00:00Z');
    let bucket = null;
    for (let i = 0; i < 60; i++) {
      const d = takeToken(bucket, policy, t0);
      expect(d.allowed).toBe(true);
      bucket = d.bucket;
    }
    const denied = takeToken(bucket, policy, t0);
    expect(denied).toMatchObject({ allowed: false, remaining: 0, retryAfterSec: 1 });
    expect(takeToken(denied.bucket, policy, new Date(t0.getTime() + 1000)).allowed).toBe(true);
    expect(takeToken(denied.bucket, policy, new Date(t0.getTime() + 3600_000)).remaining).toBe(59); // never above capacity
  });

  it('an empty bucket gives 429 with Retry-After and the quota headers; other orgs are not affected', async () => {
    await call(monitorsRoute.GET, '/api/v1/monitors', { key: acmeKey }); // make sure Acme's bucket exists
    await db.update(schema.rateLimitBuckets).set({ tokens: 0, updatedAt: new Date() }).where(eq(schema.rateLimitBuckets.key, `org:${acme.id}`));
    const res = await call(monitorsRoute.GET, '/api/v1/monitors', { key: acmeKey });
    await expectProblem(res, 429, 'rate-limited');
    expect(Number(res.headers.get('retry-after'))).toBeGreaterThanOrEqual(1);
    expect(res.headers.get('ratelimit')).toMatch(/^"api";r=0;t=\d+$/);
    expect(res.headers.get('x-ratelimit-limit')).toBe('120');
    expect((await call(monitorsRoute.GET, '/api/v1/monitors', { key: globexKey })).status).toBe(200);
    await db.update(schema.rateLimitBuckets).set({ tokens: 120 }).where(eq(schema.rateLimitBuckets.key, `org:${acme.id}`));
  });

  it('really runs out after the plan’s requests per minute (Business: 120)', async () => {
    const org = await makeOrg('Burst');
    const { key } = await createApiKey(owner(org), { name: 'b', scopes: ['monitors:read'] });
    // The bucket refills while the loop runs (2 tokens a second), so count until the first 429.
    const started = Date.now();
    let ok = 0;
    let limited: Response | null = null;
    while (!limited && ok < 400) {
      const res = await call(monitorsRoute.GET, '/api/v1/monitors?limit=1', { key, headers: { 'x-forwarded-for': `10.9.${ok % 250}.1` } });
      if (res.status === 429) limited = res;
      else ok++;
    }
    expect(limited?.status).toBe(429);
    expect(ok).toBeGreaterThanOrEqual(120);
    expect(ok).toBeLessThanOrEqual(120 + Math.ceil(((Date.now() - started) / 1000) * 2) + 1);
  });
});

describe('cross-tenant: a key from org B never reaches org A', () => {
  const A: Record<string, string> = {};

  beforeAll(async () => {
    const m = await createMonitor({ orgId: acme.id, userId: acme.users.owner.id }, { name: 'acme-secret', url: 'https://acme-secret.test', intervalSeconds: 60 });
    A.monitor = toPublicId('monitor', m.id);
    const [incident] = await db.insert(schema.incidents).values({ organizationId: acme.id, monitorId: m.id, cause: 'acme-secret down' }).returning();
    A.incident = toPublicId('incident', incident.id);
  });

  const CASES: Record<string, { kind: 'item' | 'list'; call: () => Promise<Response> }> = {
    'GET monitors': { kind: 'list', call: () => call(monitorsRoute.GET, '/api/v1/monitors?limit=100', { key: globexKey }) },
    'POST monitors': { kind: 'list', call: () => call(monitorsRoute.POST, '/api/v1/monitors', { key: globexKey, method: 'POST', body: json({ name: 'g', url: 'https://g.test', organizationId: acme.id }) }) },
    'GET monitors/[id]': { kind: 'item', call: () => call(monitorRoute.GET, '/x', { key: globexKey, params: { id: A.monitor } }) },
    'PATCH monitors/[id]': { kind: 'item', call: () => call(monitorRoute.PATCH, '/x', { key: globexKey, method: 'PATCH', body: json({ name: 'pwned' }), params: { id: A.monitor } }) },
    'DELETE monitors/[id]': { kind: 'item', call: () => call(monitorRoute.DELETE, '/x', { key: globexKey, method: 'DELETE', params: { id: A.monitor } }) },
    'GET incidents': { kind: 'list', call: () => call(incidentsRoute.GET, `/api/v1/incidents?limit=100&monitor_id=${A.monitor}`, { key: globexKey }) },
    'GET incidents/[id]': { kind: 'item', call: () => call(incidentRoute.GET, '/x', { key: globexKey, params: { id: A.incident } }) },
    'GET openapi.json': { kind: 'list', call: async () => openapiRoute.GET() },
  };

  for (const [name, c] of Object.entries(CASES)) {
    it(`${name} → ${c.kind === 'item' ? '404' : 'no Acme data'}`, async () => {
      const res = await c.call();
      if (c.kind === 'item') await expectProblem(res, 404, 'not-found');
      else {
        expect(res.status).toBeLessThan(300);
        const text = await res.text();
        for (const secret of [...Object.values(A), 'acme-secret', acme.id]) expect(text).not.toContain(secret);
      }
    });
  }

  it('Acme’s monitor is untouched', async () => {
    const [m] = await db.select().from(schema.monitors).where(eq(schema.monitors.id, fromPublicId('monitor', A.monitor)!));
    expect(m.name).toBe('acme-secret');
  });

  it('covers every method of every /api/v1 route', () => {
    const root = path.join('src', 'app', 'api', 'v1');
    const found: string[] = [];
    const walk = (dir: string) => {
      for (const entry of readdirSync(dir, { withFileTypes: true })) {
        const full = path.join(dir, entry.name);
        if (entry.isDirectory()) walk(full);
        else if (entry.name === 'route.ts') {
          const route = path.relative(root, dir).split(path.sep).join('/');
          for (const [, method] of readFileSync(full, 'utf8').matchAll(/export (?:const|function) (GET|POST|PUT|PATCH|DELETE)\b/g)) found.push(`${method} ${route}`);
        }
      }
    };
    walk(root);
    expect(found.filter((k) => !(k in CASES))).toEqual([]);
  });
});

describe('incidents', () => {
  it('lists open and resolved incidents with filters, and gets one by id', async () => {
    const org = await makeOrg('Incidents');
    const { key } = await createApiKey(owner(org), { name: 'i', scopes: ['incidents:read'] });
    const m = await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name: 'i', url: 'https://i.test', intervalSeconds: 300 });
    const [open] = await db.insert(schema.incidents).values({ organizationId: org.id, monitorId: m.id, cause: 'HTTP 503' }).returning();
    await db.insert(schema.incidents).values({ organizationId: org.id, monitorId: m.id, cause: 'old', resolvedAt: new Date() });
    const onlyOpen = await (await call(incidentsRoute.GET, '/api/v1/incidents?status=open', { key })).json();
    expect(onlyOpen.data).toEqual([expect.objectContaining({ id: toPublicId('incident', open.id), monitor_id: toPublicId('monitor', m.id), status: 'open', cause: 'HTTP 503', resolved_at: null })]);
    const all = await (await call(incidentsRoute.GET, '/api/v1/incidents', { key })).json();
    expect(all.data).toHaveLength(2);
    const one = await call(incidentRoute.GET, '/x', { key, params: { id: toPublicId('incident', open.id) } });
    expect((await one.json()).cause).toBe('HTTP 503');
  });
});

describe('OpenAPI (🟡)', () => {
  it('is generated from the same schemas, served at /api/v1/openapi.json, and the committed copy is up to date', async () => {
    const served = await (await openapiRoute.GET()).json();
    expect(served).toEqual(JSON.parse(JSON.stringify(buildOpenApiDocument())));
    expect(served.openapi).toBe('3.1.0');
    expect(Object.keys(served.paths)).toEqual(['/monitors', '/monitors/{id}', '/incidents', '/incidents/{id}']);
    const committed = readFileSync('docs/openapi.json', 'utf8');
    expect(committed).toBe(`${JSON.stringify(buildOpenApiDocument(), null, 2)}\n`); // run `npm run openapi` if this fails
  });
});
