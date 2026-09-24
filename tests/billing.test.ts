import { beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));
vi.mock('@/lib/email', () => ({ sendEmail: vi.fn() }));

import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { sendEmail } from '@/lib/email';
import { createMonitor } from '@/lib/monitors';
import { getEntitlements } from '@/lib/entitlements';
import { fakeBilling } from '@/lib/billing/provider';
import { FAKE_WEBHOOK_SECRET, signWebhookPayload } from '@/lib/billing/webhook';
import { fakeEvent } from '@/lib/billing/fake-provider';
import * as webhookRoute from '@/app/api/stripe/webhook/route';
import * as billingRoute from '@/app/api/orgs/[orgSlug]/billing/route';
import * as checkoutRoute from '@/app/api/orgs/[orgSlug]/billing/checkout/route';
import * as portalRoute from '@/app/api/orgs/[orgSlug]/billing/portal/route';
import { makeOrg, makeUser, signInAs } from './helpers/fixtures';

/*
 * Lesson 3.1: Checkout, the Portal and the webhook, against the fake provider
 * (no network). Webhook requests are signed exactly as Stripe signs them, with
 * the SDK's own generateTestHeaderString.
 */

const fake = fakeBilling();
const { subscriptions, organizations, stripeEvents } = schema;

beforeAll(() => {
  vi.stubEnv('BILLING_PROVIDER', 'fake');
  vi.stubEnv('APP_URL', 'https://beacon.test');
});

const json = (method: string, body?: unknown) =>
  new Request('http://test', { method, headers: { 'content-type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body) });
const p = <T extends object>(params: T) => ({ params: Promise.resolve(params) });

/** POST an event to the webhook route the way Stripe does: raw JSON body + Stripe-Signature. */
function postWebhook(event: object, opts: { secret?: string; timestamp?: number; tamper?: (body: string) => string; signature?: string | null } = {}) {
  const payload = JSON.stringify(event);
  const signature = opts.signature !== undefined ? opts.signature : signWebhookPayload(payload, opts.secret ?? FAKE_WEBHOOK_SECRET, opts.timestamp);
  const body = opts.tamper ? opts.tamper(payload) : payload;
  const headers: Record<string, string> = { 'content-type': 'application/json' };
  if (signature !== null) headers['stripe-signature'] = signature;
  return webhookRoute.POST(new Request('http://test/api/stripe/webhook', { method: 'POST', headers, body }));
}

async function subsOf(orgId: string) {
  return withOrg(orgId, (tx) => tx.select().from(subscriptions).where(eq(subscriptions.organizationId, orgId)));
}

async function planOf(orgId: string) {
  return (await getEntitlements({ orgId })).plan;
}

/** Owner of a Free org goes through Checkout and "pays"; returns the event Stripe would send. */
async function checkoutAndPay(org: Awaited<ReturnType<typeof makeOrg>>, plan: 'pro' | 'business' = 'pro') {
  signInAs(org.users.owner);
  const res = await checkoutRoute.POST(json('POST', { plan }), p({ orgSlug: org.slug }));
  expect(res.status).toBe(200);
  const { data } = await res.json();
  const sessionId = String(data.url).split('/').pop()!;
  return fake.simulateCheckoutCompleted(sessionId);
}

describe('Checkout and the Portal (🟢)', () => {
  let org: Awaited<ReturnType<typeof makeOrg>>;
  beforeAll(async () => {
    org = await makeOrg('Payer', { plan: 'free' });
  });

  it('Upgrade creates the Stripe customer ON THE ORG, once, and a Checkout Session carrying the org id', async () => {
    signInAs(org.users.owner);
    const res = await checkoutRoute.POST(json('POST', { plan: 'pro' }), p({ orgSlug: org.slug }));
    expect(res.status).toBe(200);
    const { data } = await res.json();
    expect(data.url).toMatch(/^https:\/\/beacon\.test\/fake-billing\/checkout\/cs_fake_/);

    const [row] = await db.select().from(organizations).where(eq(organizations.id, org.id));
    expect(row.stripeCustomerId).toMatch(/^cus_fake_/);
    const session = fake.checkoutSessions.get(String(data.url).split('/').pop()!)!;
    expect(session).toMatchObject({ customerId: row.stripeCustomerId, orgId: org.id, priceId: 'price_fake_pro' });
    expect(session.successUrl).toBe(`https://beacon.test/${org.slug}/billing?checkout=success&plan=pro`);

    // A second click reuses the org's customer.
    await checkoutRoute.POST(json('POST', { plan: 'business' }), p({ orgSlug: org.slug }));
    expect([...fake.customers.values()].filter((c) => c.orgId === org.id)).toHaveLength(1);
  });

  it('returning from Checkout changes nothing: only the webhook does', async () => {
    expect(await planOf(org.id)).toBe('free');
    expect(await subsOf(org.id)).toEqual([]);
  });

  it('Manage billing opens a Portal session for the org’s customer', async () => {
    signInAs(org.users.owner);
    const res = await portalRoute.POST(json('POST'), p({ orgSlug: org.slug }));
    const { data } = await res.json();
    const session = fake.portalSessions.get(String(data.url).split('/').pop()!)!;
    const [row] = await db.select().from(organizations).where(eq(organizations.id, org.id));
    expect(session).toMatchObject({ customerId: row.stripeCustomerId, returnUrl: `https://beacon.test/${org.slug}/billing` });
  });

  it('refuses a second Checkout once the org has a subscription (plan changes go through the Portal)', async () => {
    const paid = await makeOrg('AlreadyPaid', { plan: 'free' });
    await postWebhook(await checkoutAndPay(paid));
    signInAs(paid.users.owner);
    const res = await checkoutRoute.POST(json('POST', { plan: 'business' }), p({ orgSlug: paid.slug }));
    expect(res.status).toBe(400);
    expect(await res.json()).toMatchObject({ error: 'already_subscribed' });
  });

  it('an unknown plan in the body is a 400, not a Checkout', async () => {
    signInAs(org.users.owner);
    const res = await checkoutRoute.POST(json('POST', { plan: 'enterprise' }), p({ orgSlug: org.slug }));
    expect(res.status).toBe(400);
  });
});

describe('only billing roles may use billing endpoints (🟢, the 1.3 permission map)', () => {
  let org: Awaited<ReturnType<typeof makeOrg>>;
  let outsider: Awaited<ReturnType<typeof makeUser>>;
  beforeAll(async () => {
    org = await makeOrg('Roles', { plan: 'free' });
    outsider = await makeUser('Outsider');
  });

  //                        owner admin member viewer outsider anonymous
  const MATRIX: Record<string, number[]> = {
    'GET billing': [200, 200, 403, 403, 404, 401],
    'POST billing/checkout': [200, 403, 403, 403, 404, 401],
    'POST billing/portal': [200, 403, 403, 403, 404, 401],
  };
  const CALLS: Record<string, (slug: string) => Promise<Response>> = {
    'GET billing': (slug) => billingRoute.GET(json('GET'), p({ orgSlug: slug })),
    'POST billing/checkout': (slug) => checkoutRoute.POST(json('POST', { plan: 'pro' }), p({ orgSlug: slug })),
    'POST billing/portal': (slug) => portalRoute.POST(json('POST'), p({ orgSlug: slug })),
  };
  const ACTORS = ['owner', 'admin', 'member', 'viewer', 'outsider', 'anonymous'] as const;

  for (const [name, statuses] of Object.entries(MATRIX)) {
    ACTORS.forEach((actor, i) => {
      it(`${name} as ${actor} → ${statuses[i]}`, async () => {
        signInAs(actor === 'anonymous' ? null : actor === 'outsider' ? outsider : org.users[actor]);
        expect((await CALLS[name](org.slug)).status).toBe(statuses[i]);
      });
    });
  }

  it('GET billing returns the DTO only: no Stripe ids, no org id', async () => {
    signInAs(org.users.admin);
    const body = await (await billingRoute.GET(json('GET'), p({ orgSlug: org.slug }))).text();
    expect(body).not.toMatch(/cus_|sub_|price_|organization/i);
    expect(body).not.toContain(org.id);
    expect(JSON.parse(body).data).toMatchObject({ plan: 'free', monitors: { max: 5 }, sms: { included: 0 } });
  });
});

describe('the webhook (🟡)', () => {
  let org: Awaited<ReturnType<typeof makeOrg>>;
  let customerId: string;

  beforeAll(async () => {
    org = await makeOrg('Hooked', { plan: 'free' });
    const paid = await checkoutAndPay(org);
    customerId = String(paid.data.object.customer);
    expect((await postWebhook(paid)).status).toBe(200);
  });

  beforeEach(() => vi.mocked(sendEmail).mockClear());

  it('a valid, signed checkout.session.completed moves the org to Pro and stores the subscription', async () => {
    expect(await planOf(org.id)).toBe('pro');
    const [sub] = await subsOf(org.id);
    expect(sub).toMatchObject({ stripeCustomerId: customerId, status: 'active', priceId: 'price_fake_pro', cancelAtPeriodEnd: false });
    expect(sub.currentPeriodEnd).toBeInstanceOf(Date);
  });

  it('a tampered body gets 400 and changes nothing', async () => {
    const event = fakeEvent('customer.subscription.updated', { customer: customerId });
    const res = await postWebhook(event, { tamper: (body) => body.replace('customer.subscription.updated', 'customer.subscription.deleted') });
    expect(res.status).toBe(400);
    expect(await db.select().from(stripeEvents).where(eq(stripeEvents.id, event.id))).toEqual([]);
  });

  it('a forged event (signed with the wrong secret, or not signed) gets 400', async () => {
    const event = fakeEvent('customer.subscription.deleted', { customer: customerId });
    expect((await postWebhook(event, { secret: 'whsec_attacker' })).status).toBe(400);
    expect((await postWebhook(event, { signature: null })).status).toBe(400);
    expect((await postWebhook(event, { signature: 't=1,v1=deadbeef' })).status).toBe(400);
    expect(await planOf(org.id)).toBe('pro');
  });

  it('a captured request replayed later (timestamp older than 5 minutes) gets 400', async () => {
    const event = fakeEvent('customer.subscription.updated', { customer: customerId });
    const tenMinutesAgo = Math.floor(Date.now() / 1000) - 600;
    expect((await postWebhook(event, { timestamp: tenMinutesAgo })).status).toBe(400);
  });

  it('the same event delivered twice changes nothing the second time', async () => {
    const sub = [...fake.subscriptions.values()].find((s) => s.customerId === customerId)!;
    const event = fake.simulateSubscriptionChange(sub.id, { cancelAtPeriodEnd: true });
    expect((await postWebhook(event)).status).toBe(200);
    const listed = fake.calls.listSubscriptions;

    const again = await postWebhook(event);
    expect(again.status).toBe(200);
    expect(await again.text()).toBe('duplicate');
    expect(fake.calls.listSubscriptions).toBe(listed); // not even a Stripe call
  });

  it('cancelling in the Portal sets cancel_at_period_end, and the plan stays until the period ends', async () => {
    const [sub] = await subsOf(org.id);
    expect(sub.cancelAtPeriodEnd).toBe(true);
    expect(await planOf(org.id)).toBe('pro');
  });

  it('deleting our subscriptions row and replaying any (new) event restores it from Stripe', async () => {
    await withOrg(org.id, (tx) => tx.delete(subscriptions).where(eq(subscriptions.organizationId, org.id)));
    const res = await postWebhook(fakeEvent('invoice.paid', { object: 'invoice', customer: customerId }));
    expect(res.status).toBe(200);
    const [sub] = await subsOf(org.id);
    expect(sub).toMatchObject({ status: 'active', cancelAtPeriodEnd: true, priceId: 'price_fake_pro' });
  });

  it('the payload is never trusted: an event claiming "deleted" re-fetches the real (active) state', async () => {
    const lie = fakeEvent('customer.subscription.deleted', { customer: customerId, status: 'canceled' });
    expect((await postWebhook(lie)).status).toBe(200);
    expect(await planOf(org.id)).toBe('pro');
  });

  it('events we do not handle, and customers we do not know, get 200 (so Stripe does not retry for days)', async () => {
    expect((await postWebhook(fakeEvent('charge.succeeded', { customer: customerId }))).status).toBe(200);
    expect((await postWebhook(fakeEvent('customer.subscription.updated', { customer: 'cus_someone_else' }))).status).toBe(200);
  });

  it('a failed sync answers 500 and the retry is processed, not skipped as a duplicate', async () => {
    const event = fakeEvent('customer.subscription.updated', { customer: customerId });
    const spy = vi.spyOn(fake, 'listSubscriptions').mockRejectedValueOnce(new Error('Stripe is down'));
    await expect(postWebhook(event)).rejects.toThrow('Stripe is down'); // Next.js turns this into a 500
    const retry = await postWebhook(event);
    expect(await retry.text()).toBe('ok');
    spy.mockRestore();
  });
});

describe('downgrades from the webhook path (3.1 → 3.2 🟡)', () => {
  it('Pro → Free with 12 monitors: 5 run, 7 paused, nothing deleted, exactly one email; upgrading again restores them', async () => {
    const org = await makeOrg('Downgrader', { plan: 'free' });
    const paid = await checkoutAndPay(org);
    await postWebhook(paid);
    expect(await planOf(org.id)).toBe('pro');
    for (let i = 1; i <= 12; i++) {
      await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name: `svc-${i}`, url: `https://svc${i}.test`, intervalSeconds: 60 });
    }
    vi.mocked(sendEmail).mockClear();

    // The subscription ends (cancelled now, or the last dunning retry failed).
    const sub = [...fake.subscriptions.values()].find((s) => s.customerId === paid.data.object.customer)!;
    const deleted = fake.simulateSubscriptionChange(sub.id, { status: 'canceled' });
    await postWebhook(deleted);
    await postWebhook(deleted); // Stripe retried it
    await postWebhook(fakeEvent('invoice.payment_failed', { customer: sub.customerId })); // another event about the same change

    expect(await planOf(org.id)).toBe('free');
    const ms = await withOrg(org.id, (tx) => tx.select().from(schema.monitors).where(eq(schema.monitors.organizationId, org.id)));
    expect(ms).toHaveLength(12);
    expect(ms.filter((m) => !m.paused)).toHaveLength(5);
    expect(ms.filter((m) => m.pausedReason === 'plan_limit')).toHaveLength(7);
    expect(ms.every((m) => m.intervalSeconds >= 300)).toBe(true);
    expect(vi.mocked(sendEmail)).toHaveBeenCalledTimes(1); // one owner, one downgrade
    expect(vi.mocked(sendEmail).mock.calls[0][0]).toMatchObject({ to: org.users.owner.email, template: 'plan-downgraded', props: expect.objectContaining({ toPlan: 'Free' }) });

    // Resubscribe: a new Checkout, a new subscription, and the frozen monitors run again.
    await postWebhook(await checkoutAndPay(org));
    expect(await planOf(org.id)).toBe('pro');
    const after = await withOrg(org.id, (tx) => tx.select().from(schema.monitors).where(eq(schema.monitors.organizationId, org.id)));
    expect(after.filter((m) => !m.paused)).toHaveLength(12);
  });
});

describe('subscriptions are tenant data (lesson 2.4)', () => {
  it('row-level security hides another org’s subscription rows', async () => {
    const a = await makeOrg('SubA', { plan: 'free' });
    const b = await makeOrg('SubB', { plan: 'free' });
    await postWebhook(await checkoutAndPay(a));
    expect(await subsOf(a.id)).toHaveLength(1);
    const seenFromB = await withOrg(b.id, (tx) => tx.select().from(subscriptions));
    expect(seenFromB).toEqual([]);
  });
});
