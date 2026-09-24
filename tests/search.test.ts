import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { db, schema } from '@/db';
import { matchPages, parseHighlight } from '@/core/search';
import { addIncidentUpdate } from '@/lib/incidents';
import { createMonitor } from '@/lib/monitors';
import { searchIncidentUpdates, searchMonitors } from '@/lib/search';
import * as searchRoute from '@/app/api/orgs/[orgSlug]/search/route';
import { makeOrg, signInAs } from './helpers/fixtures';

/*
 * Lesson 2.3: pg_trgm for monitors (🟢), full-text search for incident
 * updates and one call for the palette (🟡), always inside one org.
 * PGlite ships pg_trgm, so these run the real Postgres operators.
 */
let acme: Awaited<ReturnType<typeof makeOrg>>;
let globex: Awaited<ReturnType<typeof makeOrg>>;
const ids: Record<string, string> = {};

async function monitor(org: typeof acme, name: string, url: string) {
  return (await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name, url, intervalSeconds: 60 })).id;
}

async function incident(org: typeof acme, monitorId: string, updates: string[]) {
  const [row] = await db.insert(schema.incidents).values({ organizationId: org.id, monitorId, cause: 'down' }).returning();
  for (const body of updates) await addIncidentUpdate({ orgId: org.id, userId: org.users.owner.id }, row.id, body);
  return row.id;
}

beforeAll(async () => {
  acme = await makeOrg('Acme');
  globex = await makeOrg('Globex');
  ids.checkout = await monitor(acme, 'checkout-api', 'https://checkout.acme.test/health');
  ids.billing = await monitor(acme, 'billing-api', 'https://billing.acme.test/health');
  ids.homepage = await monitor(acme, 'Homepage', 'https://www.acme.test');
  ids.percent = await monitor(acme, '100% uptime club', 'https://club.acme.test');
  // Same name in another org: it must never show up for Acme, nor Acme's for Globex.
  ids.globexCheckout = await monitor(globex, 'checkout-api', 'https://checkout.globex.test/health');

  ids.prodIncident = await incident(acme, ids.checkout, ['The TLS certificate expired on the checkout load balancer.', 'Renewed it.']);
  ids.stagingIncident = await incident(acme, ids.billing, ['Staging only: the certificate expired on the staging proxy.']);
  ids.xssIncident = await incident(acme, ids.homepage, ['<script>alert("xss")</script> renew the certificate before it expires']);
  ids.globexIncident = await incident(globex, ids.globexCheckout, ['Globex: certificate expired on checkout too.']);
});

describe('🟢 monitor search with pg_trgm', () => {
  it('"chekout" finds "checkout-api" (a typo), and not billing-api', async () => {
    const hits = await searchMonitors({ orgId: acme.id }, 'chekout');
    expect(hits.map((h) => h.id)).toEqual([ids.checkout]);
  });

  it('ranks by similarity: the closer name comes first', async () => {
    const hits = await searchMonitors({ orgId: acme.id }, 'billing api');
    expect(hits[0].id).toBe(ids.billing);
    expect(hits[0].score).toBeGreaterThan(hits[hits.length - 1].score - 0.0001);
  });

  it('matches substrings of the name or the URL', async () => {
    expect((await searchMonitors({ orgId: acme.id }, 'api')).map((h) => h.id).sort()).toEqual([ids.checkout, ids.billing].sort());
    expect((await searchMonitors({ orgId: acme.id }, 'www')).map((h) => h.id)).toEqual([ids.homepage]);
  });

  it('treats % and _ literally', async () => {
    expect((await searchMonitors({ orgId: acme.id }, '100%')).map((h) => h.id)).toEqual([ids.percent]);
  });

  it('never returns another org’s monitor, even with an identical name', async () => {
    expect((await searchMonitors({ orgId: acme.id }, 'checkout-api')).map((h) => h.id)).toEqual([ids.checkout]);
    expect((await searchMonitors({ orgId: globex.id }, 'checkout-api')).map((h) => h.id)).toEqual([ids.globexCheckout]);
  });
});

describe('🟡 full-text search over incident updates', () => {
  it('"certificate expired" -staging behaves like a web search', async () => {
    const hits = await searchIncidentUpdates({ orgId: acme.id }, '"certificate expired" -staging');
    expect(hits.map((h) => h.incidentId)).toEqual([ids.prodIncident]);
    // Without the exclusion, staging's update matches too; "expires" stems like "expired".
    const all = await searchIncidentUpdates({ orgId: acme.id }, 'certificate expired');
    expect(new Set(all.map((h) => h.incidentId))).toEqual(new Set([ids.prodIncident, ids.stagingIncident, ids.xssIncident]));
    // A phrase must appear in that order, next to each other.
    expect((await searchIncidentUpdates({ orgId: acme.id }, '"expired certificate"')).length).toBe(0);
  });

  it('returns a highlighted snippet as parts, never as HTML', async () => {
    const [hit] = await searchIncidentUpdates({ orgId: acme.id }, '"certificate expired" -staging');
    expect(hit.snippet.filter((p) => p.hit).map((p) => p.text.toLowerCase())).toEqual(['certificate', 'expired']);
    // The update with a <script> in it comes back as data (strings), which
    // React renders as text. Nothing in the pipeline produces HTML.
    const [xss] = await searchIncidentUpdates({ orgId: acme.id }, 'renew before');
    expect(xss.snippet.every((p) => typeof p.text === 'string' && typeof p.hit === 'boolean')).toBe(true);
    expect(xss.snippet.find((p) => p.hit)?.text.toLowerCase()).toBe('renew');
  });

  it('only searches the current org', async () => {
    const acmeHits = await searchIncidentUpdates({ orgId: acme.id }, 'globex');
    expect(acmeHits).toEqual([]);
    const globexHits = await searchIncidentUpdates({ orgId: globex.id }, 'certificate');
    expect(globexHits.map((h) => h.incidentId)).toEqual([ids.globexIncident]);
  });

  it('survives odd input', async () => {
    for (const q of ['"', '-', 'or or', '&|!():*', '   ']) await expect(searchIncidentUpdates({ orgId: acme.id }, q)).resolves.toBeInstanceOf(Array);
  });
});

describe('🟡 the palette’s one call', () => {
  const get = (orgSlug: string, q: string) => searchRoute.GET(new Request(`http://test/x?q=${encodeURIComponent(q)}`), { params: Promise.resolve({ orgSlug }) });

  it('returns pages, monitors and incidents with their type, in one response', async () => {
    signInAs(acme.users.viewer);
    const res = await get(acme.slug, 'checkout');
    expect(res.status).toBe(200);
    expect(res.headers.get('server-timing')).toMatch(/^search;dur=/);
    const { data } = await res.json();
    expect(data.map((r: { type: string }) => r.type)).toEqual(expect.arrayContaining(['monitor', 'incident']));
    expect(data.find((r: { type: string }) => r.type === 'monitor').href).toBe(`/${acme.slug}/monitors/${ids.checkout}`);
    const pages = (await (await get(acme.slug, 'settings')).json()).data;
    expect(pages).toEqual([]); // viewers cannot open Settings, so it is not offered
  });

  it('with an empty query lists the pages this role may open', async () => {
    signInAs(acme.users.admin);
    const { data } = await (await get(acme.slug, '')).json();
    expect(data.map((r: { title: string }) => r.title)).toContain('Settings');
  });

  it('another org’s user gets 404 under Acme’s slug and only Globex data under their own', async () => {
    signInAs(globex.users.owner);
    expect((await get(acme.slug, 'checkout')).status).toBe(404);
    const body = await (await get(globex.slug, 'checkout')).text();
    for (const id of Object.values(ids).filter((id) => ![ids.globexCheckout, ids.globexIncident].includes(id))) expect(body).not.toContain(id);
    expect(body).toContain(ids.globexCheckout);
  });
});

describe('pure helpers', () => {
  it('parseHighlight splits ts_headline output into plain and matched parts', () => {
    expect(parseHighlight('The ⟦certificate⟧ ⟦expired⟧ today')).toEqual([
      { text: 'The ', hit: false },
      { text: 'certificate', hit: true },
      { text: ' ', hit: false },
      { text: 'expired', hit: true },
      { text: ' today', hit: false },
    ]);
    expect(parseHighlight('no match')).toEqual([{ text: 'no match', hit: false }]);
  });

  it('matchPages matches word prefixes and respects permissions', () => {
    expect(matchPages('mem', 'viewer', 'acme').map((p) => p.title)).toEqual(['Members']);
    expect(matchPages('status pub', 'viewer', 'acme').map((p) => p.href)).toEqual(['/status/acme']);
    expect(matchPages('logo', 'member', 'acme')).toEqual([]);
    expect(matchPages('logo', 'admin', 'acme').map((p) => p.href)).toEqual(['/acme/settings']);
  });
});
