import { afterAll, beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { eq } from 'drizzle-orm';
import { z } from 'zod';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import type { CheckOutcome } from '@/core/check';
import { EVENT_NAME_PATTERN, EVENT_NAMES, findPii, TRACKING_PLAN } from '@/core/tracking-plan';
import { createMemoryAnalyticsDriver, setAnalyticsDriverForTests, track, TrackingPlanError, validateEvent } from '@/lib/analytics';
import { createPostHogDriver } from '@/lib/analytics/drivers';
import { activationFunnel } from '@/lib/analytics/funnel';
import { createApiKey } from '@/lib/api-keys';
import { fakeBilling } from '@/lib/billing/provider';
import { signWebhookPayload, FAKE_WEBHOOK_SECRET } from '@/lib/billing/webhook';
import { recordCheckResult } from '@/lib/checks';
import { createInvitation } from '@/lib/invitations';
import { createMonitor } from '@/lib/monitors';
import { saveOrgNotificationSettings } from '@/lib/notifications';
import { createOrganization, setStatusPagePublic } from '@/lib/organizations';
import * as analyticsRoute from '@/app/api/orgs/[orgSlug]/analytics/route';
import * as checkoutRoute from '@/app/api/orgs/[orgSlug]/billing/checkout/route';
import * as webhookRoute from '@/app/api/stripe/webhook/route';
import { makeOrg, makeUser, signInAs } from './helpers/fixtures';
import { clearQueues, jobsAreDue, jobsIn, retriesAreDue, runQueuedJobs } from './helpers/queue';

/*
 * Lesson 6.2: the tracking plan and server-side product analytics, on a real
 * (in-memory) Postgres: every business event is recorded by the server, per
 * organization, with the plan, and without personal data.
 */
const { analyticsEvents } = schema;
type Org = Awaited<ReturnType<typeof makeOrg>>;
const DOWN: CheckOutcome = { ok: false, statusCode: 503, latencyMs: 12, error: null };
const UP: CheckOutcome = { ok: true, statusCode: 200, latencyMs: 40, error: null };

async function eventsOf(orgId: string) {
  return withOrg(orgId, (tx) => tx.select().from(analyticsEvents).where(eq(analyticsEvents.organizationId, orgId)).orderBy(analyticsEvents.occurredAt));
}
const names = (rows: { event: string }[]) => rows.map((r) => r.event);

beforeAll(() => {
  vi.stubEnv('BILLING_PROVIDER', 'fake');
  vi.stubEnv('APP_URL', 'https://beacon.test');
  vi.stubEnv('SLACK_PROVIDER', 'fake');
});
afterAll(() => {
  vi.unstubAllEnvs();
  setAnalyticsDriverForTests(undefined);
});

describe('the tracking plan (🟢)', () => {
  it('has 8–12 events, each named object_action in snake_case with a past-tense verb', () => {
    expect(EVENT_NAMES.length).toBeGreaterThanOrEqual(8);
    expect(EVENT_NAMES.length).toBeLessThanOrEqual(12);
    for (const name of EVENT_NAMES) expect(name).toMatch(EVENT_NAME_PATTERN);
    for (const bad of ['createMonitor', 'Monitor Created', 'new-monitor', 'monitor_create', 'monitor']) expect(bad).not.toMatch(EVENT_NAME_PATTERN);
  });

  it('every event says which question it answers and why', () => {
    for (const name of EVENT_NAMES) {
      expect(['activation', 'retention', 'revenue', 'engagement']).toContain(TRACKING_PLAN[name].question);
      expect(TRACKING_PLAN[name].why.length).toBeGreaterThan(20);
    }
    // The activation funnel of lesson 6.2's 🟡 exercise is in the plan.
    expect(EVENT_NAMES).toEqual(expect.arrayContaining(['org_created', 'monitor_created', 'monitor_check_completed', 'subscription_upgraded']));
  });

  it('properties can only be enums, numbers and booleans: no free text, so no email, name or URL', () => {
    for (const name of EVENT_NAMES) {
      const shape = TRACKING_PLAN[name].properties.shape as Record<string, z.ZodType>;
      for (const [key, field] of Object.entries(shape)) {
        expect(field instanceof z.ZodEnum || field instanceof z.ZodNumber || field instanceof z.ZodBoolean, `${name}.${key}`).toBe(true);
      }
    }
  });

  it('findPii() catches emails, URLs and personal-data keys, even if a schema is loosened by mistake', () => {
    expect(findPii({ interval_seconds: 60, via: 'app' })).toEqual([]);
    expect(findPii({ note: 'alice@example.com' })).toHaveLength(1);
    expect(findPii({ target: 'https://acme.test/health' })).toHaveLength(1);
    expect(findPii({ user_email: 'x' })).toHaveLength(1);
    expect(findPii({ monitor_url: 'x', name: 'y' })).toHaveLength(2);
  });

  it('validateEvent() refuses unknown events, unknown properties and wrong types at runtime', () => {
    expect(() => validateEvent('monitor_created', { interval_seconds: 60, is_first: true, via: 'app' })).not.toThrow();
    // A property the plan does not list (the monitor's URL, say) is refused, not silently stored.
    expect(() => validateEvent('monitor_created', { interval_seconds: 60, is_first: true, via: 'app', url: 'https://x.test' } as never)).toThrow(TrackingPlanError);
    expect(() => validateEvent('monitor_created', { interval_seconds: '60', is_first: true, via: 'app' } as never)).toThrow(TrackingPlanError);
    expect(() => validateEvent('Monitor Created' as never, {} as never)).toThrow(/not in the tracking plan/);
  });

  it('track() rejects names and properties outside the plan at COMPILE time (npm run typecheck)', () => {
    // These lines are type-checked, never run: each @ts-expect-error fails the typecheck if the call compiles.
    const neverCalled = () => {
      // @ts-expect-error: a typo in the event name is not in the plan
      void track({ orgId: 'x' }, 'monitor_creatd', { interval_seconds: 60, is_first: true, via: 'app' });
      // @ts-expect-error: `url` is not a property of monitor_created
      void track({ orgId: 'x' }, 'monitor_created', { interval_seconds: 60, is_first: true, via: 'app', url: 'https://x' });
      // @ts-expect-error: `via` must be 'app' or 'api'
      void track({ orgId: 'x' }, 'monitor_created', { interval_seconds: 60, is_first: true, via: 'browser' });
    };
    expect(typeof neverCalled).toBe('function');
  });
});

describe('server-side business events, per organization (🟡)', () => {
  let acme: Org;
  let monitor: { id: string; name: string; url: string };

  beforeAll(async () => {
    acme = await makeOrg('Acme Analytics');
    monitor = await createMonitor({ orgId: acme.id, userId: acme.users.member.id }, { name: 'Checkout API', url: 'https://checkout.acme-secret.test/health', intervalSeconds: 60 });
  });

  it('org_created, when an organization is created (from sign-up or "new organization")', async () => {
    const user = await makeUser('Founder');
    const personal = await createOrganization(user.id, "Founder's workspace", 'signup');
    const [e] = await eventsOf(personal.id);
    expect(e).toMatchObject({ event: 'org_created', userId: user.id, orgPlan: 'free', properties: { signup_source: 'signup' } });
    expect(names(await eventsOf(acme.id))[0]).toBe('org_created');
  });

  it('monitor_created after the insert, with is_first and where it came from', async () => {
    await createMonitor({ orgId: acme.id, userId: acme.users.owner.id }, { name: 'Second', url: 'https://second.acme-secret.test', intervalSeconds: 300 }, 'api');
    const created = (await eventsOf(acme.id)).filter((e) => e.event === 'monitor_created');
    expect(created.map((e) => e.properties)).toEqual([
      { interval_seconds: 60, is_first: true, via: 'app' },
      { interval_seconds: 300, is_first: false, via: 'api' },
    ]);
    expect(created[0].userId).toBe(acme.users.member.id); // who did it: an id, never the email
    expect(created.every((e) => e.orgPlan === 'business')).toBe(true); // the plan when it happened
  });

  it('a monitor create that fails records nothing (the event is in the same transaction)', async () => {
    const before = (await eventsOf(acme.id)).length;
    await expect(createMonitor({ orgId: acme.id, userId: acme.users.owner.id }, { name: 'x', url: 'https://x.test', intervalSeconds: 7 })).rejects.toThrow();
    expect((await eventsOf(acme.id)).length).toBe(before);
  });

  it('monitor_check_completed for the FIRST check of each monitor only; incident_opened when one opens', async () => {
    const t = Date.now() - 60_000;
    await recordCheckResult(acme, monitor, UP, new Date(t));
    await recordCheckResult(acme, monitor, DOWN, new Date(t + 1000));
    await recordCheckResult(acme, monitor, DOWN, new Date(t + 2000));
    await recordCheckResult(acme, monitor, DOWN, new Date(t + 3000));
    const rows = await eventsOf(acme.id);
    const completed = rows.filter((e) => e.event === 'monitor_check_completed');
    expect(completed.map((e) => e.properties)).toEqual([{ status: 'up', is_first_for_org: true }]);
    expect(completed[0].userId).toBeNull(); // Beacon did it, not a person
    expect(rows.filter((e) => e.event === 'incident_opened')).toHaveLength(1);
  });

  it('alert_channel_connected, teammate_invited, status_page_published and api_key_created', async () => {
    await saveOrgNotificationSettings({ orgId: acme.id, userId: acme.users.admin.id }, { allowed: new Set(), slackWebhookUrl: 'https://hooks.slack.com/services/T0/B0/acme-secret' });
    await saveOrgNotificationSettings({ orgId: acme.id, userId: acme.users.admin.id }, { allowed: new Set(), slackWebhookUrl: 'https://hooks.slack.com/services/T0/B0/acme-secret-2' }); // a change, not a new connection
    const ownerCtx = { orgId: acme.id, orgSlug: acme.slug, orgName: acme.name, userId: acme.users.owner.id, userEmail: acme.users.owner.email, emailVerified: true, role: 'owner' as const };
    vi.stubEnv('EMAIL_DRIVER', 'memory');
    await createInvitation(ownerCtx, { email: 'new.person@acme-secret.test', role: 'member' });
    await setStatusPagePublic(ownerCtx, false);
    await setStatusPagePublic(ownerCtx, true);
    await setStatusPagePublic(ownerCtx, true); // already public: no second event
    await createApiKey(ownerCtx, { name: 'CI at Acme', scopes: ['monitors:read', 'monitors:write'] });
    const rows = await eventsOf(acme.id);
    expect(rows.filter((e) => e.event === 'alert_channel_connected').map((e) => e.properties)).toEqual([{ channel: 'slack' }]);
    expect(rows.filter((e) => e.event === 'teammate_invited').map((e) => e.properties)).toEqual([{ role: 'member' }]);
    expect(rows.filter((e) => e.event === 'status_page_published')).toHaveLength(1);
    expect(rows.filter((e) => e.event === 'api_key_created').map((e) => e.properties)).toEqual([{ scope_count: 2 }]);
  });

  it('subscription_upgraded comes from the Stripe webhook sync, not from the "Upgrade" click', async () => {
    const payer = await makeOrg('Payer Analytics', { plan: 'free' });
    signInAs(payer.users.owner);
    const res = await checkoutRoute.POST(new Request('http://test', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ plan: 'pro' }) }), { params: Promise.resolve({ orgSlug: payer.slug }) });
    const { data } = await res.json();
    expect(names(await eventsOf(payer.id))).not.toContain('subscription_upgraded'); // clicking is not paying
    const event = await fakeBilling().simulateCheckoutCompleted(String(data.url).split('/').pop()!);
    const payload = JSON.stringify(event);
    await webhookRoute.POST(new Request('http://test/api/stripe/webhook', { method: 'POST', headers: { 'stripe-signature': signWebhookPayload(payload, FAKE_WEBHOOK_SECRET) }, body: payload }));
    const upgraded = (await eventsOf(payer.id)).filter((e) => e.event === 'subscription_upgraded');
    expect(upgraded.map((e) => [e.properties, e.orgPlan])).toEqual([[{ from_plan: 'free', to_plan: 'pro' }, 'pro']]);
  });

  it('no event anywhere contains an email, a name, a URL or any other personal data', async () => {
    const all = await db.select().from(analyticsEvents);
    expect(all.length).toBeGreaterThan(10);
    const text = JSON.stringify(all.map((e) => e.properties));
    for (const secret of ['@', '://', 'acme-secret', 'Checkout API', acme.users.owner.email, acme.users.owner.name, acme.name, 'CI at Acme']) {
      expect(text).not.toContain(secret);
    }
    for (const e of all) expect(findPii(e.properties as Record<string, unknown>)).toEqual([]);
  });

  it('every event carries its organization (group analytics), and another org sees none of them', async () => {
    const globex = await makeOrg('Globex Analytics');
    // Row-level security: inside withOrg(globex), even a query with no WHERE sees only Globex's events.
    const seen = await withOrg(globex.id, (tx) => tx.select().from(analyticsEvents));
    expect(seen.length).toBeGreaterThan(0);
    expect(seen.every((e) => e.organizationId === globex.id)).toBe(true);
    // And a row claiming another org is refused.
    const refused = await withOrg(globex.id, (tx) => tx.insert(analyticsEvents).values({ organizationId: acme.id, event: 'org_created', orgPlan: 'free' })).catch((e) => e);
    expect(String((refused as { cause?: Error }).cause?.message ?? refused)).toMatch(/row-level security/);
  });
});

describe('client events: consent first, only UI events (🟡)', () => {
  let acme: Org;
  beforeAll(async () => {
    acme = await makeOrg('Consent Co');
  });
  const post = (orgSlug: string, body: unknown, consent?: string) =>
    analyticsRoute.POST(
      new Request('http://test/x', { method: 'POST', headers: { 'content-type': 'application/json', ...(consent && { cookie: `theme=dark; beacon_analytics_consent=${consent}` }) }, body: JSON.stringify(body) }),
      { params: Promise.resolve({ orgSlug }) },
    );
  const palette = { event: 'command_palette_opened', properties: { via: 'keyboard' } };
  const count = async () => (await eventsOf(acme.id)).filter((e) => e.event === 'command_palette_opened').length;

  it('stores nothing without consent, or after "no"', async () => {
    signInAs(acme.users.viewer);
    expect((await post(acme.slug, palette)).status).toBe(204);
    expect((await post(acme.slug, palette, 'denied')).status).toBe(204);
    expect(await count()).toBe(0);
  });

  it('records the event for the org in the URL after "yes"', async () => {
    signInAs(acme.users.viewer);
    expect((await post(acme.slug, palette, 'granted')).status).toBe(202);
    const [e] = (await eventsOf(acme.id)).filter((r) => r.event === 'command_palette_opened');
    expect(e).toMatchObject({ userId: acme.users.viewer.id, properties: { via: 'keyboard' } });
  });

  it('the browser cannot send a business event or extra properties', async () => {
    signInAs(acme.users.owner);
    expect((await post(acme.slug, { event: 'monitor_created', properties: { interval_seconds: 60, is_first: true, via: 'app' } }, 'granted')).status).toBe(400);
    expect((await post(acme.slug, { event: 'subscription_upgraded', properties: { from_plan: 'free', to_plan: 'business' } }, 'granted')).status).toBe(400);
    expect((await post(acme.slug, { event: 'command_palette_opened', properties: { via: 'keyboard', email: 'a@b.c' } }, 'granted')).status).toBe(400);
    expect(await count()).toBe(1);
  });

  it('a non-member gets 404, whatever the consent', async () => {
    const other = await makeUser('Stranger');
    signInAs(other);
    expect((await post(acme.slug, palette, 'granted')).status).toBe(404);
  });
});

describe('forwarding to PostHog: batched, retried, grouped by org (🟡)', () => {
  it('the PostHog driver sends the org as a group with its plan, user ids as distinct ids, and row ids for dedupe', async () => {
    const calls: { url: string; body: { api_key: string; batch: Record<string, unknown>[] } }[] = [];
    const driver = createPostHogDriver({
      apiKey: 'phc_test',
      host: 'https://eu.i.posthog.com/',
      fetchImpl: (async (url: string, init: RequestInit) => {
        calls.push({ url, body: JSON.parse(String(init.body)) });
        return new Response('{}', { status: 200 });
      }) as typeof fetch,
    });
    const at = new Date('2026-09-01T10:00:00Z');
    await driver.send({
      orgId: 'org-1',
      plan: 'pro',
      events: [
        { id: 'e1', event: 'monitor_created', userId: 'u1', properties: { interval_seconds: 60, is_first: true, via: 'app' }, orgPlan: 'pro', occurredAt: at },
        { id: 'e2', event: 'monitor_check_completed', userId: null, properties: { status: 'up', is_first_for_org: true }, orgPlan: 'pro', occurredAt: at },
      ],
    });
    expect(calls[0].url).toBe('https://eu.i.posthog.com/batch/');
    const [group, created, checked] = calls[0].body.batch;
    expect(group).toMatchObject({ event: '$groupidentify', properties: { $group_type: 'organization', $group_key: 'org-1', $group_set: { plan: 'pro' } } });
    expect(created).toMatchObject({ event: 'monitor_created', uuid: 'e1', distinct_id: 'u1', properties: { $groups: { organization: 'org-1' }, org_plan: 'pro', interval_seconds: 60 } });
    expect(checked).toMatchObject({ distinct_id: 'org_org-1', properties: { $process_person_profile: false } });
  });

  it('events become one job per org per minute; an outage is retried and nothing is lost', async () => {
    const driver = createMemoryAnalyticsDriver();
    setAnalyticsDriverForTests(driver);
    await clearQueues();
    const org = await makeOrg('Forwarded');
    await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name: 'a', url: 'https://a.test', intervalSeconds: 60 });
    await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name: 'b', url: 'https://b.test', intervalSeconds: 60 });
    const jobs = (await jobsIn('analytics.forward')).filter((j) => j.data.orgId === org.id);
    expect(jobs.length).toBeGreaterThanOrEqual(1);
    expect(jobs.length).toBeLessThanOrEqual(2); // one per minute; two if the test crossed a minute boundary

    driver.fail = true;
    await jobsAreDue('analytics.forward');
    await runQueuedJobs({ queues: ['analytics.forward'] });
    expect((await eventsOf(org.id)).every((e) => e.forwardedAt === null)).toBe(true);
    expect((await jobsIn('analytics.forward')).some((j) => j.state === 'retry')).toBe(true);

    driver.fail = false;
    await retriesAreDue();
    await runQueuedJobs({ queues: ['analytics.forward'] });
    const rows = await eventsOf(org.id);
    expect(rows.every((e) => e.forwardedAt !== null)).toBe(true);
    const sent = driver.batches.filter((b) => b.orgId === org.id).flatMap((b) => b.events.map((e) => e.event));
    expect(sent).toEqual(['org_created', 'monitor_created', 'monitor_created']);
    setAnalyticsDriverForTests(null);
  });
});

describe('the activation funnel, per organization and by plan (🟡)', () => {
  it('org_created → monitor_created → first check within 24 h, broken down by plan', async () => {
    const since = new Date(Date.now() - 1);
    const fast = await makeOrg('Fast Activator'); // business
    const m = await createMonitor({ orgId: fast.id, userId: fast.users.owner.id }, { name: 'a', url: 'https://fast.test', intervalSeconds: 60 });
    await recordCheckResult(fast, m, UP, new Date());
    const slow = await makeOrg('Monitor Only', { plan: 'free' });
    await createMonitor({ orgId: slow.id, userId: slow.users.owner.id }, { name: 'b', url: 'https://slow.test', intervalSeconds: 300 });
    await makeOrg('Signed Up Only', { plan: 'free' });
    // An org whose first check came after 24 hours has not activated.
    const late = await makeOrg('Late', { plan: 'free' });
    const lm = await createMonitor({ orgId: late.id, userId: late.users.owner.id }, { name: 'c', url: 'https://late.test', intervalSeconds: 300 });
    await recordCheckResult(late, lm, UP, new Date(Date.now() + 25 * 3600 * 1000));

    const rows = await activationFunnel({ since, until: new Date(Date.now() + 1000) });
    const byPlan = Object.fromEntries(rows.map((r) => [r.isTotal ? 'all' : r.plan, r]));
    expect(byPlan.business).toMatchObject({ orgs: 1, withMonitor: 1, withCheck: 1, activated: 1 });
    expect(byPlan.free).toMatchObject({ orgs: 3, withMonitor: 2, withCheck: 1, activated: 0 });
    expect(byPlan.all).toMatchObject({ orgs: 4, activated: 1, isTotal: true });
    expect(byPlan.business.medianMinutesToActivation).toBe(0);
  });
});
