import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn(), isSessionValid: vi.fn(async () => true) }));

import { and, eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { reconnectDelayMs } from '@/core/retry';
import { recordCheckResult } from '@/lib/checks';
import { runQueuedJobs } from '@/lib/queue/run';
import { createMonitor } from '@/lib/monitors';
import { notify } from '@/lib/notifications';
import { incidentOpenedEvent } from '@/lib/notifications/events';
import { heartbeat, TTL_MS } from '@/lib/presence';
import { channelFor, publish, publishInTx, subscribe, type RealtimeEvent } from '@/lib/realtime';
import { isSessionValid } from '@/lib/session';
import * as eventsRoute from '@/app/api/orgs/[orgSlug]/events/route';
import * as presenceRoute from '@/app/api/orgs/[orgSlug]/presence/route';
import { makeOrg, signInAs } from './helpers/fixtures';

/*
 * Lesson 4.3: live updates over Postgres LISTEN/NOTIFY and SSE, and presence.
 * PGlite implements LISTEN/NOTIFY, so these tests run the real SQL.
 */
type Org = Awaited<ReturnType<typeof makeOrg>>;
let acme: Org;
let globex: Org;
let acmeMonitor: Awaited<ReturnType<typeof createMonitor>>;
let globexMonitor: Awaited<ReturnType<typeof createMonitor>>;

const DOWN = { ok: false, statusCode: 500, latencyMs: 9, error: null };
const p = <T extends object>(params: T) => ({ params: Promise.resolve(params) });
const tick = (ms = 30) => new Promise((r) => setTimeout(r, ms));

beforeAll(async () => {
  acme = await makeOrg('Acme');
  globex = await makeOrg('Globex');
  acmeMonitor = await createMonitor({ orgId: acme.id, userId: acme.users.owner.id }, { name: 'acme-api', url: 'https://acme.test', intervalSeconds: 60 });
  globexMonitor = await createMonitor({ orgId: globex.id, userId: globex.users.owner.id }, { name: 'globex-api', url: 'https://globex.test', intervalSeconds: 60 });
});
afterEach(() => vi.unstubAllEnvs());

/** Open the SSE route as the signed-in user and read it like a browser would. */
async function openStream(orgSlug: string) {
  const abort = new AbortController();
  const res = await eventsRoute.GET(new Request('http://test/api/events', { signal: abort.signal }), p({ orgSlug }));
  let text = '';
  let done = false;
  const reader = res.body?.getReader();
  const pump = (async () => {
    if (!reader) return;
    const decoder = new TextDecoder();
    for (;;) {
      const chunk = await reader.read().catch(() => ({ done: true, value: undefined }));
      if (chunk.done) break;
      text += decoder.decode(chunk.value);
    }
    done = true;
  })();
  return {
    res,
    text: () => text,
    done: () => done,
    /** Wait until the stream contains `needle` (or give up after `ms`). */
    async waitFor(needle: string, ms = 2000) {
      const until = Date.now() + ms;
      while (!text.includes(needle) && Date.now() < until && !done) await tick(10);
      return text.includes(needle);
    },
    async close() {
      abort.abort();
      await reader?.cancel().catch(() => {});
      await pump;
    },
  };
}

describe('LISTEN/NOTIFY fan-out', () => {
  it('an event published in a transaction arrives when it commits, and never if it rolls back', async () => {
    const got: RealtimeEvent[] = [];
    const stop = await subscribe(acme.id, (e) => got.push(e));
    await withOrg(acme.id, (tx) => publishInTx(tx, acme.id, { type: 'presence.changed', topic: 'committed' }));
    await withOrg(acme.id, async (tx) => {
      await publishInTx(tx, acme.id, { type: 'presence.changed', topic: 'rolled-back' });
      throw new Error('boom');
    }).catch(() => {});
    await tick();
    expect(got).toEqual([{ type: 'presence.changed', topic: 'committed' }]);
    await stop();
  });

  it('each org has its own channel: a listener on Globex hears nothing from Acme', async () => {
    const heard: RealtimeEvent[] = [];
    const stop = await subscribe(globex.id, (e) => heard.push(e));
    await publish(acme.id, { type: 'presence.changed', topic: 'acme-only' });
    await tick();
    expect(heard).toEqual([]);
    expect(channelFor(acme.id)).not.toBe(channelFor(globex.id));
    await stop();
  });

  it('many subscribers share one LISTEN, and the last one to leave stops it', async () => {
    const a: RealtimeEvent[] = [];
    const b: RealtimeEvent[] = [];
    const stopA = await subscribe(acme.id, (e) => a.push(e));
    const stopB = await subscribe(acme.id, (e) => b.push(e));
    await publish(acme.id, { type: 'presence.changed', topic: 'both' });
    await tick();
    await stopA();
    await publish(acme.id, { type: 'presence.changed', topic: 'only-b' });
    await tick();
    await stopB();
    await publish(acme.id, { type: 'presence.changed', topic: 'nobody' });
    await tick();
    expect(a.map((e) => (e as { topic: string }).topic)).toEqual(['both']);
    expect(b.map((e) => (e as { topic: string }).topic)).toEqual(['both', 'only-b']);
  });
});

describe('the SSE endpoint (🟢)', () => {
  it('401 without a session, 404 for someone outside the org (Beacon never confirms an org exists)', async () => {
    signInAs(null);
    expect((await eventsRoute.GET(new Request('http://test'), p({ orgSlug: acme.slug }))).status).toBe(401);
    signInAs(globex.users.owner);
    expect((await eventsRoute.GET(new Request('http://test'), p({ orgSlug: acme.slug }))).status).toBe(404);
  });

  it('streams a failing check to the org’s dashboards as it happens, and never to another org’s', async () => {
    signInAs(acme.users.viewer);
    const acmeStream = await openStream(acme.slug);
    expect(acmeStream.res.headers.get('content-type')).toContain('text/event-stream');
    expect(await acmeStream.waitFor('event: ready')).toBe(true);
    signInAs(globex.users.owner);
    const globexStream = await openStream(globex.slug);
    expect(await globexStream.waitFor('event: ready')).toBe(true);

    await recordCheckResult(acme, acmeMonitor, DOWN);
    expect(await acmeStream.waitFor(`"monitorId":"${acmeMonitor.id}"`)).toBe(true);
    expect(acmeStream.text()).toContain('event: monitor.status');
    expect(acmeStream.text()).toContain('"state":"down"');

    await recordCheckResult(globex, globexMonitor, DOWN);
    expect(await globexStream.waitFor(globexMonitor.id)).toBe(true);
    expect(globexStream.text()).not.toContain(acmeMonitor.id);
    expect(globexStream.text()).not.toContain(acme.id);
    expect(acmeStream.text()).not.toContain(globexMonitor.id);
    await acmeStream.close();
    await globexStream.close();
  });

  it('an incident opening is announced, and "new notification" only reaches its recipient', async () => {
    signInAs(acme.users.member);
    const member = await openStream(acme.slug);
    await member.waitFor('event: ready');
    await recordCheckResult(acme, acmeMonitor, DOWN);
    await recordCheckResult(acme, acmeMonitor, DOWN); // third failure in a row (one from the test above)
    await runQueuedJobs({ queues: ['workflow.run'] }); // lesson 5.1: the fan-out is a job
    expect(await member.waitFor('event: incident.changed')).toBe(true);
    expect(await member.waitFor('event: notification')).toBe(true);
    // Every member got a notification, but this stream announced exactly one: the member's own.
    expect(member.text().match(/event: notification\n/g)).toHaveLength(1);
    expect(member.text()).not.toContain(acme.users.owner.id);
    await member.close();
  });

  it('a notification for someone else is not even announced', async () => {
    signInAs(acme.users.viewer);
    const viewer = await openStream(acme.slug);
    await viewer.waitFor('event: ready');
    await withOrg(acme.id, (tx) => publishInTx(tx, acme.id, { type: 'notification.created', userId: acme.users.owner.id }));
    await tick(50);
    expect(viewer.text()).not.toContain('event: notification');
    await viewer.close();
  });

  it('closing the connection stops listening (no leaked LISTEN)', async () => {
    signInAs(acme.users.viewer);
    const s = await openStream(globex.slug).catch(() => null); // not a member: a 404, no stream at all
    expect(s?.res.status).toBe(404);
    signInAs(acme.users.admin);
    const stream = await openStream(acme.slug);
    await stream.waitFor('event: ready');
    await stream.close();
    expect(stream.done()).toBe(true);
  });
});

describe('re-authorization while connected (🟡)', () => {
  it('a member removed from the org gets "revoked" and the stream ends within the recheck interval', async () => {
    vi.stubEnv('REALTIME_RECHECK_MS', '50');
    const org = await makeOrg('Leaving');
    signInAs(org.users.member);
    const stream = await openStream(org.slug);
    await stream.waitFor('event: ready');
    await db.delete(schema.memberships).where(and(eq(schema.memberships.organizationId, org.id), eq(schema.memberships.userId, org.users.member.id)));
    expect(await stream.waitFor('event: revoked', 2000)).toBe(true);
    for (let i = 0; i < 50 && !stream.done(); i++) await tick(10);
    expect(stream.done()).toBe(true);
    // Events published after the removal never reach the old stream.
    await publish(org.id, { type: 'presence.changed', topic: 'after-removal' });
    await tick();
    expect(stream.text()).not.toContain('after-removal');
  });

  it('signing out (the session is gone) ends the stream too', async () => {
    vi.stubEnv('REALTIME_RECHECK_MS', '50');
    signInAs(acme.users.owner);
    const stream = await openStream(acme.slug);
    await stream.waitFor('event: ready');
    vi.mocked(isSessionValid).mockResolvedValue(false);
    expect(await stream.waitFor('event: revoked', 2000)).toBe(true);
    vi.mocked(isSessionValid).mockResolvedValue(true);
    await stream.close();
  });
});

describe('reconnecting with exponential backoff and full jitter (🟡)', () => {
  it('grows exponentially up to 30 s, with a random delay below that ceiling', () => {
    expect(reconnectDelayMs(0, () => 1)).toBe(1000);
    expect(reconnectDelayMs(3, () => 1)).toBe(8000);
    expect(reconnectDelayMs(10, () => 1)).toBe(30_000);
    expect(reconnectDelayMs(3, () => 0.5)).toBe(4000);
  });

  it('10,000 dashboards reconnecting after a restart spread over seconds instead of one spike', () => {
    const delays = Array.from({ length: 10_000 }, () => reconnectDelayMs(2)); // third attempt: up to 4 s
    const perSecond = [0, 1, 2, 3].map((s) => delays.filter((d) => d >= s * 1000 && d < (s + 1) * 1000).length);
    expect(Math.max(...perSecond)).toBeLessThan(3000); // about a quarter each, not 10,000 at once
    expect(Math.min(...perSecond)).toBeGreaterThan(2000);
  });
});

describe('presence (🟡)', () => {
  const topic = () => `monitor:${acmeMonitor.id}`;
  const post = (orgSlug: string, t: string) =>
    presenceRoute.POST(new Request('http://test', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ topic: t }) }), p({ orgSlug }));
  const del = (orgSlug: string, t: string) => presenceRoute.DELETE(new Request(`http://test?topic=${encodeURIComponent(t)}`, { method: 'DELETE' }), p({ orgSlug }));

  it('shows who is viewing, announces joins and leaves, and forgets tabs that stopped heartbeating', async () => {
    const events: RealtimeEvent[] = [];
    const stop = await subscribe(acme.id, (e) => events.push(e));
    signInAs(acme.users.owner);
    await post(acme.slug, topic());
    signInAs(acme.users.member);
    const res = await post(acme.slug, topic());
    const { data } = await res.json();
    expect(data.map((v: { userId: string }) => v.userId).sort()).toEqual([acme.users.owner.id, acme.users.member.id].sort());
    await post(acme.slug, topic()); // a heartbeat, not a join: no new event
    await tick();
    expect(events.filter((e) => e.type === 'presence.changed')).toHaveLength(2);

    expect((await del(acme.slug, topic())).status).toBe(204); // the member closes the tab
    await tick();
    expect(events.filter((e) => e.type === 'presence.changed')).toHaveLength(3);

    // The owner's tab crashed: no DELETE, just silence. After the TTL, it no longer counts.
    const later = new Date(Date.now() + TTL_MS + 1000);
    const viewers = await heartbeat({ orgId: acme.id, userId: acme.users.admin.id }, topic(), later);
    expect(viewers.map((v) => v.userId)).toEqual([acme.users.admin.id]);
    await stop();
  });

  it('another org’s monitor is a 404 under either slug, and malformed topics are refused', async () => {
    signInAs(globex.users.owner);
    expect((await post(acme.slug, topic())).status).toBe(404);
    expect((await post(globex.slug, topic())).status).toBe(404);
    expect((await del(globex.slug, topic())).status).toBe(404);
    expect((await post(globex.slug, 'org:everything')).status).toBe(404);
  });

  it('presence rows are tenant data (RLS): Globex sees none of Acme’s', async () => {
    const rows = await withOrg(globex.id, (tx) => tx.select().from(schema.presence));
    expect(rows).toEqual([]);
  });
});

describe('notify() publishes after commit', () => {
  it('no event for a notification that was already sent (dedupe)', async () => {
    const events: RealtimeEvent[] = [];
    const stop = await subscribe(acme.id, (e) => events.push(e));
    const [incident] = await withOrg(acme.id, (tx) => tx.select().from(schema.incidents).where(eq(schema.incidents.monitorId, acmeMonitor.id)));
    await notify(incidentOpenedEvent(acme, acmeMonitor, incident)); // already notified by the check runner
    await tick();
    expect(events).toEqual([]);
    await stop();
  });
});
