import { readdirSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn(), isSessionValid: vi.fn(async () => true) }));

import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { createMonitor } from '@/lib/monitors';
import * as monitorsRoute from '@/app/api/orgs/[orgSlug]/monitors/route';
import * as monitorRoute from '@/app/api/orgs/[orgSlug]/monitors/[id]/route';
import * as membersRoute from '@/app/api/orgs/[orgSlug]/members/route';
import * as memberRoute from '@/app/api/orgs/[orgSlug]/members/[userId]/route';
import * as logoRoute from '@/app/api/orgs/[orgSlug]/logo/route';
import * as screenshotsRoute from '@/app/api/orgs/[orgSlug]/incidents/[incidentId]/screenshots/route';
import * as fileRoute from '@/app/api/orgs/[orgSlug]/files/[fileId]/route';
import * as completeRoute from '@/app/api/orgs/[orgSlug]/files/[fileId]/complete/route';
import * as searchRoute from '@/app/api/orgs/[orgSlug]/search/route';
import * as billingRoute from '@/app/api/orgs/[orgSlug]/billing/route';
import * as checkoutRoute from '@/app/api/orgs/[orgSlug]/billing/checkout/route';
import * as portalRoute from '@/app/api/orgs/[orgSlug]/billing/portal/route';
import * as notificationsRoute from '@/app/api/orgs/[orgSlug]/notifications/route';
import * as eventsRoute from '@/app/api/orgs/[orgSlug]/events/route';
import * as presenceRoute from '@/app/api/orgs/[orgSlug]/presence/route';
import * as settingsRoute from '@/app/api/orgs/[orgSlug]/settings/route';
import * as analyticsRoute from '@/app/api/orgs/[orgSlug]/analytics/route';
import * as auditLogRoute from '@/app/api/orgs/[orgSlug]/audit-log/route';
import { publish } from '@/lib/realtime';
import { makeOrg, signInAs } from './helpers/fixtures';

/*
 * Lesson 2.4 (🟢): "an automated test logs in as org B and gets 404 for every
 * org A resource", for every route. Globex's owner (the strongest role in
 * Globex) tries two ways in:
 *
 *   under Acme's slug       → 404: not a member, the org "does not exist"
 *   under Globex's own slug  → 404 for Acme's ids; lists contain no Acme data
 *
 * The last test reads src/app/api and fails when a route or a method has no
 * case here, so a new endpoint cannot ship without its cross-tenant test.
 */
let acme: Awaited<ReturnType<typeof makeOrg>>;
let globex: Awaited<ReturnType<typeof makeOrg>>;
const A: Record<string, string> = {}; // ids of Acme's resources

beforeAll(async () => {
  vi.stubEnv('BILLING_PROVIDER', 'fake'); // lesson 3.1: Stripe is replaced by the in-memory fake
  acme = await makeOrg('Acme');
  globex = await makeOrg('Globex');
  const m = await createMonitor({ orgId: acme.id, userId: acme.users.owner.id }, { name: 'acme-secret', url: 'https://acme.test', intervalSeconds: 60 });
  A.monitor = m.id;
  A.member = acme.users.viewer.id;
  const [incident] = await db.insert(schema.incidents).values({ organizationId: acme.id, monitorId: m.id, cause: 'acme-secret down' }).returning();
  A.incident = incident.id;
  const [file] = await db
    .insert(schema.files)
    .values({ organizationId: acme.id, kind: 'incident_screenshot', incidentId: incident.id, key: `orgs/${acme.id}/screenshots/${crypto.randomUUID()}`, originalName: 'acme-secret.png', declaredType: 'image/png', declaredSize: 10, status: 'ready' })
    .returning();
  A.file = file.id;
  // Lesson 3.1: Acme is a paying customer, with its own Stripe customer and subscription.
  await db.update(schema.organizations).set({ stripeCustomerId: 'cus_acme_secret' }).where(eq(schema.organizations.id, acme.id));
  await db.insert(schema.subscriptions).values({ id: 'sub_acme_secret', organizationId: acme.id, stripeCustomerId: 'cus_acme_secret', status: 'active', priceId: 'price_fake_business' });
  A.customer = 'cus_acme_secret';
  // Lesson 4.2: Acme's owner has a notification about Acme's incident.
  const [n] = await db
    .insert(schema.notifications)
    .values({ organizationId: acme.id, userId: acme.users.owner.id, category: 'incident.opened', dedupeKey: `acme-secret:${incident.id}`, title: 'acme-secret is down', body: 'acme-secret down', url: `/${acme.slug}/monitors/${m.id}` })
    .returning();
  A.notification = n.id;
  A.subscription = 'sub_acme_secret';
});

const req = (method: string, body?: unknown) =>
  new Request('http://test/x', { method, headers: { 'content-type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body) });
const p = <T extends object>(params: T) => ({ params: Promise.resolve(params) });

type Case = {
  /**
   * 'item': must be 404 under both slugs. 'list': 404 under Acme's slug; 200 under Globex's, without Acme data.
   * 'stream' (lesson 4.3): like 'list', for a response that never ends: read it for a moment while Acme
   * publishes events, then hang up.
   */
  kind: 'item' | 'list' | 'stream';
  call: (orgSlug: string) => Promise<Response>;
};

// Keyed by "<METHOD> <route directory below src/app/api/orgs/[orgSlug]>".
const CASES: Record<string, Case> = {
  'GET monitors': { kind: 'list', call: (orgSlug) => monitorsRoute.GET(req('GET'), p({ orgSlug })) },
  'POST monitors': {
    kind: 'list', // creating is allowed in your own org; the body cannot choose Acme (see api-matrix.test.ts)
    call: (orgSlug) => monitorsRoute.POST(req('POST', { name: 'x', url: 'https://x.test', intervalSeconds: 60, organizationId: acme.id }), p({ orgSlug })),
  },
  'GET monitors/[id]': { kind: 'item', call: (orgSlug) => monitorRoute.GET(req('GET'), p({ orgSlug, id: A.monitor })) },
  'PATCH monitors/[id]': { kind: 'item', call: (orgSlug) => monitorRoute.PATCH(req('PATCH', { name: 'pwned' }), p({ orgSlug, id: A.monitor })) },
  'DELETE monitors/[id]': { kind: 'item', call: (orgSlug) => monitorRoute.DELETE(req('DELETE'), p({ orgSlug, id: A.monitor })) },
  'GET members': { kind: 'list', call: (orgSlug) => membersRoute.GET(req('GET'), p({ orgSlug })) },
  'PATCH members/[userId]': { kind: 'item', call: (orgSlug) => memberRoute.PATCH(req('PATCH', { role: 'admin' }), p({ orgSlug, userId: A.member })) },
  // Lesson 2.2
  'POST logo': { kind: 'list', call: (orgSlug) => logoRoute.POST(req('POST', { name: 'l.png', type: 'image/png', size: 10, organizationId: acme.id }), p({ orgSlug })) },
  'POST incidents/[incidentId]/screenshots': {
    kind: 'item',
    call: (orgSlug) => screenshotsRoute.POST(req('POST', { name: 's.png', type: 'image/png', size: 10 }), p({ orgSlug, incidentId: A.incident })),
  },
  'GET files/[fileId]': { kind: 'item', call: (orgSlug) => fileRoute.GET(req('GET'), p({ orgSlug, fileId: A.file })) },
  'POST files/[fileId]/complete': { kind: 'item', call: (orgSlug) => completeRoute.POST(req('POST'), p({ orgSlug, fileId: A.file })) },
  // Lesson 2.3: searching for Acme's words from Globex finds nothing of Acme's.
  'GET search': { kind: 'list', call: (orgSlug) => searchRoute.GET(new Request('http://test/x?q=acme-secret'), p({ orgSlug })) },
  // Lesson 3.1: billing. Under Globex's own slug these act on Globex's own
  // customer: never Acme's, whatever the body says.
  'GET billing': { kind: 'list', call: (orgSlug) => billingRoute.GET(req('GET'), p({ orgSlug })) },
  'POST billing/checkout': {
    kind: 'list',
    call: (orgSlug) => checkoutRoute.POST(req('POST', { plan: 'pro', orgId: acme.id, customer: A.customer }), p({ orgSlug })),
  },
  'POST billing/portal': { kind: 'list', call: (orgSlug) => portalRoute.POST(req('POST', { customer: A.customer }), p({ orgSlug })) },
  // Lesson 4.2: the inbox is per org and per person.
  'GET notifications': { kind: 'list', call: (orgSlug) => notificationsRoute.GET(req('GET'), p({ orgSlug })) },
  // Lesson 4.3: the live stream, and presence on Acme's monitor.
  'GET events': { kind: 'stream', call: (orgSlug) => eventsRoute.GET(req('GET'), p({ orgSlug })) },
  'POST presence': { kind: 'item', call: (orgSlug) => presenceRoute.POST(req('POST', { topic: `monitor:${A.monitor}` }), p({ orgSlug })) },
  // Lesson 6.1: renaming under Globex's slug renames Globex, never Acme.
  'PATCH settings': { kind: 'list', call: (orgSlug) => settingsRoute.PATCH(req('PATCH', { name: 'Renamed', orgId: acme.id }), p({ orgSlug })) },
  // Lesson 6.2: a client event is recorded for the org in the URL (with consent), never one named in the body.
  'POST analytics': {
    kind: 'list',
    call: (orgSlug) =>
      analyticsRoute.POST(
        new Request('http://test/x', {
          method: 'POST',
          headers: { 'content-type': 'application/json', cookie: 'beacon_analytics_consent=granted' },
          body: JSON.stringify({ event: 'command_palette_opened', properties: { via: 'button' }, orgId: acme.id }),
        }),
        p({ orgSlug }),
      ),
  },
  // Lesson 7.3: Acme's audit log (which names 'acme-secret', its monitor) is not in Globex's, JSON or CSV.
  'GET audit-log': { kind: 'list', call: (orgSlug) => auditLogRoute.GET(new Request('http://test/x?format=csv'), p({ orgSlug })) },
  'DELETE presence': {
    kind: 'item',
    call: (orgSlug) => presenceRoute.DELETE(new Request(`http://test/x?topic=monitor:${A.monitor}`, { method: 'DELETE' }), p({ orgSlug })),
  },
};

/** Read a stream for ~200 ms while `meanwhile` runs, then hang up. */
async function readForAWhile(res: Response, meanwhile: () => Promise<unknown>): Promise<string> {
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  let text = '';
  const until = Date.now() + 200;
  let published = false;
  while (Date.now() < until) {
    const chunk = await Promise.race([reader.read(), new Promise<null>((r) => setTimeout(() => r(null), 50))]);
    if (chunk && chunk.done) break;
    if (chunk?.value) text += decoder.decode(chunk.value);
    if (!published) {
      published = true;
      await meanwhile();
    }
  }
  await reader.cancel();
  return text;
}

describe('org B cannot reach org A through any route', () => {
  for (const [name, c] of Object.entries(CASES)) {
    it(`${name} under Acme's slug → 404`, async () => {
      signInAs(globex.users.owner);
      expect((await c.call(acme.slug)).status).toBe(404);
    });

    it(`${name} under Globex's slug → ${c.kind === 'item' ? '404' : 'no Acme data'}`, async () => {
      signInAs(globex.users.owner);
      const res = await c.call(globex.slug);
      if (c.kind === 'item') {
        expect(res.status).toBe(404);
      } else if (c.kind === 'stream') {
        expect(res.status).toBe(200);
        const body = await readForAWhile(res, () => publish(acme.id, { type: 'monitor.status', monitorId: A.monitor, state: 'down', checkedAt: new Date().toISOString(), latencyMs: 1 }));
        expect(body).toContain('event: ready'); // it really was streaming
        for (const secret of [...Object.values(A), 'acme-secret', acme.id]) expect(body).not.toContain(secret);
      } else {
        expect(res.status).toBeLessThan(300);
        const body = await res.text();
        for (const secret of [...Object.values(A), 'acme-secret', acme.id]) expect(body).not.toContain(secret);
      }
    });
  }

  it('Acme’s data is intact afterwards', async () => {
    const [m] = await db.select().from(schema.monitors).where(eq(schema.monitors.id, A.monitor));
    expect(m?.name).toBe('acme-secret');
  });
});

describe('every API route has a cross-tenant case', () => {
  it('covers each exported method of each route file', () => {
    const root = path.join('src', 'app', 'api', 'orgs', '[orgSlug]');
    const found: string[] = [];
    const walk = (dir: string) => {
      for (const entry of readdirSync(dir, { withFileTypes: true })) {
        const full = path.join(dir, entry.name);
        if (entry.isDirectory()) walk(full);
        else if (entry.name === 'route.ts') {
          const route = path.relative(root, dir).split(path.sep).join('/');
          for (const [, method] of readFileSync(full, 'utf8').matchAll(/export const (GET|POST|PUT|PATCH|DELETE)\b/g)) found.push(`${method} ${route}`);
        }
      }
    };
    walk(root);
    expect(found.length).toBeGreaterThan(0);
    expect(found.filter((k) => !(k in CASES))).toEqual([]);
  });
});
