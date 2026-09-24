import http from 'node:http';
import type { AddressInfo } from 'node:net';
import { afterAll, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { and, eq } from 'drizzle-orm';
import { Webhook } from 'standardwebhooks';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import type { CheckOutcome } from '@/core/check';
import { setResolverForTests } from '@/core/safe-fetch';
import { DISABLE_AFTER_MS, generateWebhookSecret, signWebhook, webhookHeaders } from '@/core/webhooks';
import { recordCheckResult } from '@/lib/checks';
import { AccessError, InvalidRequestError } from '@/lib/errors';
import { createMonitor, resolveIncident } from '@/lib/monitors';
import { WORKERS } from '@/lib/queue/worker';
import { createEndpoint, deliverWebhook, getEndpointLog, replayFailedSince, resendMessage, setEndpointEnabled } from '@/lib/webhooks';
import { makeOrg } from './helpers/fixtures';
import { jobsIn, retriesAreDue, runQueuedJobs } from './helpers/queue';

/*
 * Lesson 5.3: outbound webhooks. A real HTTP receiver on 127.0.0.1 (let
 * through by the development allow-list), verified with the OFFICIAL
 * Standard Webhooks library, as a customer would.
 */
type Org = Awaited<ReturnType<typeof makeOrg>>;
type Received = { headers: http.IncomingHttpHeaders; body: string; path: string };
const DOWN: CheckOutcome = { ok: false, statusCode: 503, latencyMs: 5, error: null };
const UP: CheckOutcome = { ok: true, statusCode: 200, latencyMs: 5, error: null };

let server: http.Server;
let base = '';
let received: Received[] = [];
let respond: (path: string) => number = () => 200;

beforeAll(async () => {
  server = http.createServer((req, res) => {
    let body = '';
    req.on('data', (c) => (body += c));
    req.on('end', () => {
      received.push({ headers: req.headers, body, path: req.url ?? '' });
      const status = respond(req.url ?? '');
      if (status >= 300 && status < 400) res.writeHead(status, { location: 'http://169.254.169.254/' });
      else res.writeHead(status);
      res.end(status >= 400 ? 'receiver is sad' : 'ok');
    });
  });
  await new Promise<void>((r) => server.listen(0, '127.0.0.1', r));
  const port = (server.address() as AddressInfo).port;
  base = `http://127.0.0.1:${port}`;
  vi.stubEnv('OUTBOUND_ALLOWLIST', `127.0.0.1:${port}`); // development escape hatch, like a local receiver
  setResolverForTests(async (host) => {
    const table: Record<string, string> = { 'hooks.public.test': '93.184.215.14', 'hooks.intranet.test': '10.0.0.8' };
    if (!table[host]) throw Object.assign(new Error(`getaddrinfo ENOTFOUND ${host}`), { code: 'ENOTFOUND' });
    return [{ address: table[host], family: 4 }];
  });
});
afterAll(async () => {
  vi.unstubAllEnvs();
  setResolverForTests(null);
  await new Promise<void>((r) => server.close(() => r()));
});
beforeEach(() => {
  received = [];
  respond = () => 200;
});

const admin = (org: Org) => ({ orgId: org.id, userId: org.users.owner.id });
const scope = (org: Org) => ({ orgId: org.id });
async function openIncident(org: Org, name: string) {
  const m = await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name, url: `https://${name}.test`, intervalSeconds: 300 });
  for (let i = 0; i < 3; i++) await recordCheckResult(org, m, DOWN, new Date(Date.now() - 10_000 + i));
  const [incident] = await withOrg(org.id, (tx) => tx.select().from(schema.incidents).where(eq(schema.incidents.monitorId, m.id)));
  return { monitor: m, incident };
}
const deliver = () => runQueuedJobs({ queues: ['webhook.deliver'] });
async function messagesOf(org: Org) {
  return withOrg(org.id, (tx) => tx.select().from(schema.webhookMessages).where(eq(schema.webhookMessages.organizationId, org.id)));
}

describe('Standard Webhooks signatures (🟢)', () => {
  it('the official library verifies what Beacon signs, and refuses a changed body, another secret, or an old timestamp', () => {
    const secret = generateWebhookSecret();
    expect(secret).toMatch(/^whsec_[A-Za-z0-9+/=]{32}$/);
    const body = JSON.stringify({ type: 'incident.opened', data: { x: 1 } });
    const headers = webhookHeaders(secret, 'msg_1', body);
    expect(headers['webhook-signature']).toMatch(/^v1,[A-Za-z0-9+/=]+$/);
    expect(new Webhook(secret).verify(body, headers)).toEqual(JSON.parse(body));
    expect(() => new Webhook(secret).verify(body.replace('1', '2'), headers)).toThrow();
    expect(() => new Webhook(generateWebhookSecret()).verify(body, headers)).toThrow();
    const old = webhookHeaders(secret, 'msg_1', body, new Date(Date.now() - 10 * 60_000));
    expect(() => new Webhook(secret).verify(body, old)).toThrow(/too old/i);
    // The library's own signer agrees byte for byte.
    const at = new Date('2026-01-01T00:00:00Z');
    expect(signWebhook(secret, 'msg_1', at.getTime() / 1000, body)).toBe(new Webhook(secret).sign('msg_1', at, body));
  });
});

describe('registering endpoints: the SSRF guard (🟡)', () => {
  let org: Org;
  beforeAll(async () => {
    org = await makeOrg('Hooks');
  });

  it.each([
    ['http://127.0.0.1/hook', /loopback/],
    ['http://169.254.169.254/latest/meta-data/', /link-local/],
    ['http://[::1]/hook', /loopback/],
    ['https://hooks.intranet.test/hook', /resolves to 10\.0\.0\.8, a private address/],
    ['https://hooks.public.test:6379/hook', /only ports 80 and 443/],
    ['https://nowhere.test/hook', /cannot resolve/],
  ])('%s is refused', async (url, message) => {
    const err = await createEndpoint(admin(org), { url, eventTypes: ['incident.opened'] }).catch((e) => e);
    expect(err).toBeInstanceOf(InvalidRequestError);
    expect(err.message).toMatch(message);
  });

  it('a public URL is accepted; the secret is returned once and never by the log', async () => {
    const { id, secret } = await createEndpoint(admin(org), { url: 'https://hooks.public.test/beacon', eventTypes: ['incident.opened'] });
    expect(secret).toMatch(/^whsec_/);
    const log = await getEndpointLog(scope(org), id);
    expect(JSON.stringify(log)).not.toContain(secret);
  });
});

describe('delivery (🟢)', () => {
  let org: Org;
  let secret: string;
  let endpointId: string;

  beforeAll(async () => {
    org = await makeOrg('Deliveries');
    ({ id: endpointId, secret } = await createEndpoint(admin(org), { url: `${base}/beacon`, eventTypes: ['incident.opened', 'incident.resolved'] }));
    await createEndpoint(admin(org), { url: `${base}/only-resolved`, eventTypes: ['incident.resolved'] });
  });

  it('an incident enqueues one signed delivery per subscribed endpoint, in the incident’s transaction', async () => {
    const { incident, monitor } = await openIncident(org, 'hooked');
    expect(received).toHaveLength(0); // nothing is sent by the checker
    const jobs = (await jobsIn('webhook.deliver')).filter((j) => j.data.orgId === org.id);
    expect(jobs).toHaveLength(1); // /only-resolved is not subscribed to incident.opened
    expect(jobs[0].group_id).toBe(endpointId); // fairness per endpoint

    await deliver();
    expect(received).toHaveLength(1);
    const [hit] = received;
    expect(hit.path).toBe('/beacon');
    const verified = new Webhook(secret).verify(hit.body, hit.headers as Record<string, string>) as { type: string; data: { incident: { id: string; status: string }; monitor: { name: string } } };
    expect(verified.type).toBe('incident.opened');
    expect(verified.data.incident).toMatchObject({ id: `inc_${incident.id.replaceAll('-', '')}`, status: 'open' });
    expect(verified.data.monitor.name).toBe(monitor.name);
    expect(hit.headers['webhook-id']).toMatch(/^msg_[0-9a-f]{32}$/);

    const [message] = await messagesOf(org);
    expect(message).toMatchObject({ status: 'delivered', attempts: 1 });
    const log = await getEndpointLog(scope(org), endpointId);
    expect(log!.messages[0].attempts).toEqual([expect.objectContaining({ statusCode: 200, trigger: 'automatic', error: null, responseBody: 'ok' })]);
  });

  it('resolving by hand is an event too, for every endpoint subscribed to it', async () => {
    const { incident } = await openIncident(org, 'manual-resolve');
    await deliver();
    received = [];
    await resolveIncident({ orgId: org.id }, incident.id);
    await deliver();
    expect(received.map((r) => r.path).sort()).toEqual(['/beacon', '/only-resolved']);
    expect(received.every((r) => JSON.parse(r.body).type === 'incident.resolved')).toBe(true);
  });

  it('a slow endpoint cannot hold up others: each endpoint is its own group, with a 10 s timeout per attempt', () => {
    expect(WORKERS['webhook.deliver']).toMatchObject({ groupConcurrency: 2 });
  });
});

describe('retries, the delivery log, replay and disabling (🟡)', () => {
  let org: Org;
  let endpointId: string;

  beforeAll(async () => {
    org = await makeOrg('Flaky');
    ({ id: endpointId } = await createEndpoint(admin(org), { url: `${base}/flaky`, eventTypes: ['incident.opened', 'incident.resolved'] }));
  });

  it('an endpoint returning 500 is retried with growing delays, and every attempt is stored', async () => {
    respond = () => 500;
    await openIncident(org, 'down-receiver');
    const delays: number[] = [];
    for (let i = 0; i < 4; i++) {
      await retriesAreDue();
      await deliver();
      const [job] = (await jobsIn('webhook.deliver')).filter((j) => j.data.orgId === org.id);
      delays.push(new Date(job.start_after).getTime() - Date.now());
    }
    expect(received).toHaveLength(4);
    for (let i = 1; i < delays.length; i++) expect(delays[i]).toBeGreaterThan(delays[i - 1]);
    // The same webhook-id on every retry, so the receiver can drop duplicates.
    expect(new Set(received.map((r) => r.headers['webhook-id'])).size).toBe(1);
    const log = await getEndpointLog(scope(org), endpointId);
    expect(log!.messages[0].status).toBe('pending');
    expect(log!.messages[0].attempts.map((a) => [a.statusCode, a.error, a.responseBody])).toEqual(Array(4).fill([500, 'HTTP 500', 'receiver is sad']));
    expect(log!.endpoint.failingSince).toBeInstanceOf(Date);

    respond = () => 204; // they fixed their server
    await retriesAreDue();
    await deliver();
    const fixed = await getEndpointLog(scope(org), endpointId);
    expect(fixed!.messages[0].status).toBe('delivered');
    expect(fixed!.endpoint.failingSince).toBeNull();
  });

  it('a redirect is a failure, never followed (and never to the metadata service)', async () => {
    respond = (path) => (path === '/flaky' ? 302 : 200);
    await openIncident(org, 'redirecting');
    await deliver();
    expect(received).toHaveLength(1); // the 302 itself; nothing reached 169.254.169.254
    const log = await getEndpointLog(scope(org), endpointId);
    expect(log!.messages[0].attempts.at(-1)).toMatchObject({ statusCode: 302, error: 'HTTP 302' });
  });

  it('"Resend" delivers a message again; "Replay failed since" re-queues the failed ones', async () => {
    const log = await getEndpointLog(scope(org), endpointId);
    const failedOne = log!.messages[0]; // the redirecting one, still pending: give up on it for the test
    await withOrg(org.id, (tx) => tx.update(schema.webhookMessages).set({ status: 'failed' }).where(eq(schema.webhookMessages.id, failedOne.id)));
    const delivered = log!.messages.find((m) => m.status === 'delivered')!;
    respond = () => 200;

    await resendMessage(scope(org), endpointId, delivered.id);
    await deliver();
    expect(received.filter((r) => r.headers['webhook-id'] === delivered.webhookId)).toHaveLength(1);

    const since = new Date(Date.now() - 24 * 3600_000);
    expect(await replayFailedSince(scope(org), endpointId, since)).toBe(1);
    await deliver();
    const after = await getEndpointLog(scope(org), endpointId);
    expect(after!.messages.every((m) => m.status === 'delivered')).toBe(true);
    expect(after!.messages.find((m) => m.id === failedOne.id)!.attempts.at(-1)).toMatchObject({ trigger: 'manual', statusCode: 200 });
    expect(await replayFailedSince(scope(org), endpointId, since)).toBe(0); // nothing left to replay
  });

  it('failing continuously for 5 days disables the endpoint and emails the owners and admins', async () => {
    respond = () => 503;
    await openIncident(org, 'five-days');
    const [pending] = (await messagesOf(org)).filter((m) => m.status === 'pending');
    await withOrg(org.id, (tx) =>
      tx.update(schema.webhookEndpoints).set({ failingSince: new Date(Date.now() - DISABLE_AFTER_MS - 60_000) }).where(eq(schema.webhookEndpoints.id, endpointId)),
    );
    expect(await deliverWebhook({ orgId: org.id, messageId: pending.id })).toEqual({ status: 'disabled' });
    const log = await getEndpointLog(scope(org), endpointId);
    expect(log!.endpoint).toMatchObject({ enabled: false, disabledReason: expect.stringContaining('HTTP 503') });
    const mails = await db.select().from(schema.emailOutbox).where(eq(schema.emailOutbox.template, 'webhook-disabled'));
    expect(mails.map((m) => m.to).sort()).toEqual([org.users.admin.email, org.users.owner.email].sort()); // not the member or viewer

    // Disabled: new incidents create no messages for it, until someone enables it again.
    received = [];
    await openIncident(org, 'while-disabled');
    await deliver();
    expect(received).toHaveLength(0);
    await setEndpointEnabled(scope(org), endpointId, true);
    expect((await getEndpointLog(scope(org), endpointId))!.endpoint).toMatchObject({ enabled: true, failingSince: null });
  });
});

describe('cross-tenant', () => {
  it('org B cannot read org A’s delivery log, resend its messages, replay or toggle its endpoint; RLS hides the rows', async () => {
    const a = await makeOrg('HookA');
    const b = await makeOrg('HookB');
    const { id } = await createEndpoint(admin(a), { url: `${base}/a`, eventTypes: ['incident.opened'] });
    await openIncident(a, 'a-secret');
    await deliver();
    const [message] = await messagesOf(a);
    expect(await getEndpointLog(scope(b), id)).toBeNull();
    await expect(resendMessage(scope(b), id, message.id)).rejects.toBeInstanceOf(AccessError);
    expect(await replayFailedSince(scope(b), id, new Date(0))).toBe(0);
    await expect(setEndpointEnabled(scope(b), id, false)).rejects.toBeInstanceOf(AccessError);
    for (const table of [schema.webhookEndpoints, schema.webhookEvents, schema.webhookMessages, schema.webhookAttempts]) {
      expect(await withOrg(b.id, (tx) => tx.select().from(table))).toEqual([]);
    }
    const [endpoint] = await withOrg(a.id, (tx) => tx.select().from(schema.webhookEndpoints).where(and(eq(schema.webhookEndpoints.id, id))));
    expect(endpoint.enabled).toBe(true);
  });
});
