import { afterAll, beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { and, eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import type { CheckOutcome } from '@/core/check';
import { recordCheckResult } from '@/lib/checks';
import { deliverPendingEmails } from '@/lib/email';
import { memoryTransport } from '@/lib/email/memory';
import { createMonitor, resolveIncident } from '@/lib/monitors';
import {
  countUnread,
  deliverPendingNotifications,
  getPreferenceMatrix,
  listNotifications,
  markAllNotificationsRead,
  markNotificationsRead,
  notify,
  saveOrgNotificationSettings,
  savePreferences,
  setPreference,
} from '@/lib/notifications';
import { incidentOpenedEvent, planDowngradedEvent } from '@/lib/notifications/events';
import { fakeSlack, fakeSms } from '@/lib/notifications/providers';
import { subscribeToStatusPage } from '@/lib/notifications/subscribers';
import { getUsageSummary } from '@/lib/usage';
import { InvalidRequestError } from '@/lib/errors';
import * as notificationsRoute from '@/app/api/orgs/[orgSlug]/notifications/route';
import * as unsubscribeRoute from '@/app/api/unsubscribe/route';
import { makeOrg, signInAs } from './helpers/fixtures';

/*
 * Lesson 4.2: the notification pipeline end to end, on a real (in-memory)
 * Postgres: check results → incident → notifications → channel workers →
 * delivery log. SMS and Slack use the fake providers; email the memory driver.
 */
const { notifications, notificationDeliveries, statusPageSubscribers, incidents } = schema;
type Org = Awaited<ReturnType<typeof makeOrg>>;

const DOWN: CheckOutcome = { ok: false, statusCode: 503, latencyMs: 12, error: null };
const UP: CheckOutcome = { ok: true, statusCode: 200, latencyMs: 12, error: null };

beforeAll(() => {
  vi.stubEnv('SMS_PROVIDER', 'fake');
  vi.stubEnv('SLACK_PROVIDER', 'fake');
});
afterAll(() => vi.unstubAllEnvs());

async function newMonitor(org: Org, name: string) {
  return createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name, url: `https://${name}.test`, intervalSeconds: 300 });
}

/** Three failed checks in a row: the lesson's threshold for opening an incident. */
async function breakMonitor(org: Org, monitor: { id: string; name: string; url: string }, start = Date.now() - 60_000) {
  for (let i = 0; i < 3; i++) await recordCheckResult(org, monitor, DOWN, new Date(start + i * 1000));
}

async function notificationsOf(org: Org, userId?: string) {
  const rows = await withOrg(org.id, (tx) => tx.select().from(notifications).where(eq(notifications.organizationId, org.id)));
  return userId ? rows.filter((r) => r.userId === userId) : rows;
}

async function deliveriesOf(org: Org) {
  return withOrg(org.id, (tx) => tx.select().from(notificationDeliveries).where(eq(notificationDeliveries.organizationId, org.id)));
}

const me = (org: Org, role: keyof Org['users']) => ({ orgId: org.id, userId: org.users[role].id });

describe('the in-app inbox (🟢)', () => {
  let acme: Org;
  let globex: Org;
  let monitor: Awaited<ReturnType<typeof newMonitor>>;

  beforeAll(async () => {
    acme = await makeOrg('Acme');
    globex = await makeOrg('Globex');
    monitor = await newMonitor(acme, 'checkout');
  });

  it('does not open an incident on two failures; the third opens it and notifies every eligible member once', async () => {
    await recordCheckResult(acme, monitor, DOWN);
    await recordCheckResult(acme, monitor, DOWN);
    expect(await notificationsOf(acme)).toHaveLength(0);
    await recordCheckResult(acme, monitor, DOWN);
    const rows = await notificationsOf(acme);
    expect(rows.map((r) => r.userId).sort()).toEqual(Object.values(acme.users).map((u) => u.id).sort()); // owner, admin, member, viewer
    expect(rows.every((r) => r.category === 'incident.opened' && r.title === 'checkout is down')).toBe(true);
  });

  it('calling notify() again for the same incident creates nothing (unique dedupe key)', async () => {
    const [incident] = await withOrg(acme.id, (tx) => tx.select().from(incidents).where(eq(incidents.monitorId, monitor.id)));
    const again = await notify(incidentOpenedEvent(acme, monitor, incident));
    expect(again.notified).toBe(0);
    expect(await notificationsOf(acme)).toHaveLength(4);
  });

  it('people outside the org get nothing, and another org cannot see these rows (RLS)', async () => {
    expect(await notificationsOf(globex)).toHaveLength(0);
    const leaked = await withOrg(globex.id, (tx) => tx.select().from(notifications)); // no WHERE at all
    expect(leaked).toHaveLength(0);
    expect(await countUnread({ orgId: acme.id, userId: globex.users.owner.id })).toBe(0);
  });

  it('only members whose role has the category’s permission are recipients (billing → billing.manage)', async () => {
    await notify(planDowngradedEvent(acme, { from: 'pro', to: 'free', frozen: 0, at: new Date() }));
    const billing = (await notificationsOf(acme)).filter((n) => n.category === 'billing');
    expect(billing.map((n) => n.userId)).toEqual([acme.users.owner.id]); // not the admin, member or viewer
  });

  it('the unread count goes down after "mark as read" and to zero after "mark all as read"', async () => {
    const member = me(acme, 'member');
    expect(await countUnread(member)).toBe(1);
    const [n] = await listNotifications(member);
    expect(await markNotificationsRead(member, [n.id])).toBe(1);
    expect(await countUnread(member)).toBe(0);
    const owner = me(acme, 'owner');
    expect(await countUnread(owner)).toBe(2); // the incident and the billing notice
    await markAllNotificationsRead(owner);
    expect(await countUnread(owner)).toBe(0);
  });

  it('nobody can mark someone else’s notification as read, in their org or from another', async () => {
    const viewer = me(acme, 'viewer');
    const [viewers] = await listNotifications(viewer);
    expect(await markNotificationsRead(me(acme, 'admin'), [viewers.id])).toBe(0);
    expect(await markNotificationsRead({ orgId: globex.id, userId: globex.users.owner.id }, [viewers.id])).toBe(0);
    expect(await countUnread(viewer)).toBe(1);
  });

  it('GET /api/orgs/:slug/notifications returns only the signed-in person’s inbox', async () => {
    signInAs(acme.users.viewer);
    const res = await notificationsRoute.GET(new Request('http://test'), { params: Promise.resolve({ orgSlug: acme.slug }) });
    const body = await res.json();
    expect(body.unread).toBe(1);
    expect(body.data).toHaveLength(1);
    expect(body.data[0].deliveries.map((d: { channel: string }) => d.channel)).toEqual(['in_app', 'email']);
  });
});

describe('channels, preferences and the delivery log (🟡)', () => {
  let acme: Org;

  beforeAll(async () => {
    acme = await makeOrg('Channels');
    memoryTransport.reset();
  });

  it('emails members through the channel worker, with a per-category unsubscribe link and one-click headers', async () => {
    const m = await newMonitor(acme, 'api');
    await breakMonitor(acme, m);
    expect(memoryTransport.messages).toHaveLength(0); // nothing is sent inside the check runner's transaction
    const counts = await deliverPendingNotifications({ orgId: acme.id });
    expect(counts.sent).toBe(4);
    const mail = memoryTransport.to(acme.users.member.email)[0];
    expect(mail.subject).toBe('[Channels] api is down');
    expect(mail.text).toContain('/unsubscribe?token=');
    expect(mail.headers['List-Unsubscribe']).toMatch(/^<http.+\/api\/unsubscribe\?token=.+>$/);
    expect(mail.headers['List-Unsubscribe-Post']).toBe('List-Unsubscribe=One-Click');
  });

  it('records every delivery with channel, status and provider message id', async () => {
    const rows = (await deliveriesOf(acme)).filter((d) => d.userId === acme.users.member.id);
    expect(rows.map((d) => [d.channel, d.status])).toEqual([
      ['in_app', 'sent'],
      ['email', 'sent'],
    ]);
    expect(rows.every((d) => d.providerMessageId && d.sentAt)).toBe(true);
  });

  it('a user who disabled email for "incident resolved" gets no resolved email, but still the in-app one', async () => {
    memoryTransport.reset();
    const member = me(acme, 'member');
    await savePreferences(member, { checked: new Set(['incident.opened:email']), phoneNumber: '' }); // resolved:email unticked
    const m = await newMonitor(acme, 'search');
    await breakMonitor(acme, m);
    await recordCheckResult(acme, m, UP); // resolves
    await deliverPendingNotifications({ orgId: acme.id });

    const resolved = (await notificationsOf(acme, member.userId)).filter((n) => n.category === 'incident.resolved');
    expect(resolved).toHaveLength(1); // in-app
    expect(memoryTransport.to(acme.users.member.email).map((e) => e.subject)).toEqual(['[Channels] search is down']);
    expect(memoryTransport.to(acme.users.owner.email).map((e) => e.subject)).toContain('[Channels] search is back up');
  });

  it('required categories stay on: the form and the unsubscribe path cannot turn billing email off', async () => {
    memoryTransport.reset();
    const admin = me(acme, 'owner');
    await savePreferences(admin, { checked: new Set(), phoneNumber: '' }); // nothing ticked at all
    expect(await setPreference(admin, 'billing', 'email', false)).toBe(false);
    const matrix = await getPreferenceMatrix(admin);
    const billing = matrix.rows.find((r) => r.category === 'billing')!;
    expect(billing.cells.email).toEqual({ enabled: true, locked: expect.stringMatching(/Required/) });
    await notify(planDowngradedEvent(acme, { from: 'pro', to: 'free', frozen: 1, at: new Date() }));
    await deliverPendingNotifications({ orgId: acme.id });
    expect(memoryTransport.to(acme.users.owner.email).map((e) => e.subject)).toEqual(['Channels is now on the Free plan']);
  });

  it('rejects a phone number that is not E.164', async () => {
    await expect(savePreferences(me(acme, 'member'), { checked: new Set(), phoneNumber: '555-1234' })).rejects.toBeInstanceOf(InvalidRequestError);
  });
});

describe('SMS: metered, throttled, with email fallback (🟡)', () => {
  let acme: Org;

  beforeAll(async () => {
    acme = await makeOrg('Pager');
    for (const role of ['member', 'admin'] as const) {
      await savePreferences(me(acme, role), { checked: new Set(['incident.opened:sms']), phoneNumber: role === 'member' ? '+15550000001' : '+15550000002' });
    }
  });

  it('sends the SMS through the provider and records it as usage (lesson 3.3)', async () => {
    const m = await newMonitor(acme, 'payments');
    await breakMonitor(acme, m);
    await deliverPendingNotifications({ orgId: acme.id });
    const sms = fakeSms.sent.find((s) => s.to === '+15550000001')!;
    expect(sms.body).toMatch(/^Beacon: payments is down http/);
    const [delivery] = (await deliveriesOf(acme)).filter((d) => d.channel === 'sms' && d.recipient === '+15550000001');
    expect(delivery).toMatchObject({ status: 'sent', providerMessageId: sms.sid });
    const usage = await withOrg(acme.id, (tx) => tx.select().from(schema.usageEvents).where(eq(schema.usageEvents.organizationId, acme.id)));
    expect(usage.map((u) => u.idempotencyKey)).toContain(`sms:${sms.sid}`);
    expect((await getUsageSummary({ orgId: acme.id })).sms.used).toBe(2); // member and admin
  });

  it('the org policy can switch SMS off for everyone', async () => {
    await saveOrgNotificationSettings({ orgId: acme.id }, { allowed: new Set(['incident.opened:email', 'incident.resolved:email', 'incident.resolved:sms']) });
    const before = fakeSms.sent.length;
    await breakMonitor(acme, await newMonitor(acme, 'policy'));
    await deliverPendingNotifications({ orgId: acme.id });
    expect(fakeSms.sent.length).toBe(before);
    await saveOrgNotificationSettings({ orgId: acme.id }, { allowed: new Set(['incident.opened:email', 'incident.opened:sms', 'incident.resolved:email', 'incident.resolved:sms']) });
  });

  it('the sixth SMS within an hour is replaced by an email saying how many were held back', async () => {
    memoryTransport.reset();
    const phone = '+15550000002'; // the admin: 1 SMS so far this hour
    for (let i = 0; i < 5; i++) await breakMonitor(acme, await newMonitor(acme, `svc${i}`));
    await deliverPendingNotifications({ orgId: acme.id });
    expect(fakeSms.sent.filter((s) => s.to === phone)).toHaveLength(5);
    const admin = (await deliveriesOf(acme)).filter((d) => d.userId === acme.users.admin.id && d.channel === 'sms');
    expect(admin.filter((d) => d.status === 'sent')).toHaveLength(5);
    expect(admin.filter((d) => d.status === 'throttled')).toHaveLength(1);
    const fallback = memoryTransport.to(acme.users.admin.email).find((e) => e.subject.includes('SMS limit reached'))!;
    expect(fallback.subject).toBe('svc4 is down (SMS limit reached)');
    expect(fallback.text).toContain('1 SMS alert has been held back');
  });

  it('a provider outage leaves the SMS pending with its error, and it goes out on a later run', async () => {
    fakeSms.outage = true;
    await savePreferences(me(acme, 'viewer'), { checked: new Set(['incident.opened:sms']), phoneNumber: '+15550000003' });
    await breakMonitor(acme, await newMonitor(acme, 'flaky-sms'));
    const m = (await deliveriesOf(acme)).find((d) => d.recipient === '+15550000003' && d.status === 'pending');
    expect(m).toBeTruthy();
    await deliverPendingNotifications({ orgId: acme.id });
    const [pending] = (await deliveriesOf(acme)).filter((d) => d.id === m!.id);
    expect(pending).toMatchObject({ status: 'pending', error: expect.stringContaining('unavailable') });
    fakeSms.outage = false;
    await withOrg(acme.id, (tx) => tx.update(notificationDeliveries).set({ nextAttemptAt: new Date(0) }).where(eq(notificationDeliveries.id, m!.id)));
    await deliverPendingNotifications({ orgId: acme.id });
    const [sent] = (await deliveriesOf(acme)).filter((d) => d.id === m!.id);
    expect(sent.status).toBe('sent');
  });
});

describe('SMS is an entitlement (lesson 3.2)', () => {
  it('a Free org (no SMS included, nothing to bill) sends no SMS, and the preferences page says why', async () => {
    const free = await makeOrg('Frugal', { plan: 'free' });
    await savePreferences(me(free, 'owner'), { checked: new Set(['incident.opened:email', 'incident.opened:sms']), phoneNumber: '+15550000099' });
    const matrix = await getPreferenceMatrix(me(free, 'owner'));
    expect(matrix.rows[0].cells.sms).toEqual({ enabled: false, locked: expect.stringMatching(/plan that includes SMS/) });
    await breakMonitor(free, await newMonitor(free, 'cheap'));
    await deliverPendingNotifications({ orgId: free.id });
    expect((await deliveriesOf(free)).filter((d) => d.channel === 'sms')).toEqual([]);
    expect(fakeSms.sent.filter((s) => s.to === '+15550000099')).toEqual([]);
  });

  it('saving the form keeps the SMS choice of a cell the form showed as locked', async () => {
    const free = await makeOrg('Keeper', { plan: 'free' });
    const owner = me(free, 'owner');
    await savePreferences(owner, { checked: new Set(['incident.opened:sms']), phoneNumber: '+15550000098' }); // chosen on an earlier plan
    await savePreferences(owner, { checked: new Set(), editable: new Set(['incident.opened:email']), phoneNumber: '+15550000098' });
    await db.update(schema.organizations).set({ plan: 'pro' }).where(eq(schema.organizations.id, free.id));
    expect((await getPreferenceMatrix(owner)).rows[0].cells.sms.enabled).toBe(true);
  });
});

describe('Slack (🟡)', () => {
  it('posts once per event to the org’s channel, and only accepts Slack webhook URLs', async () => {
    const acme = await makeOrg('Slacky');
    await expect(saveOrgNotificationSettings({ orgId: acme.id }, { allowed: new Set(), slackWebhookUrl: 'http://169.254.169.254/latest' })).rejects.toBeInstanceOf(InvalidRequestError);
    const all = ['incident.opened', 'incident.resolved', 'monitor.flapping'].flatMap((c) => ['email', 'sms', 'slack'].map((ch) => `${c}:${ch}`));
    await saveOrgNotificationSettings({ orgId: acme.id }, { allowed: new Set(all), slackWebhookUrl: 'https://hooks.slack.com/services/T0/B0/secret' });
    await breakMonitor(acme, await newMonitor(acme, 'web'));
    await deliverPendingNotifications({ orgId: acme.id });
    const posts = fakeSlack.posts.filter((p) => p.webhookUrl.endsWith('/secret'));
    expect(posts).toHaveLength(1); // one per event, not one per member
    expect(posts[0].text).toMatch(/^\*web is down\*/);
  });
});

describe('anti-flapping (🟡)', () => {
  it('a monitor alternating up/down every 30 s for an hour opens no incident at all (3 failures needed)', async () => {
    const org = await makeOrg('Alternating');
    const m = await newMonitor(org, 'wobbly');
    const start = Date.now() - 3 * 3600_000;
    for (let i = 0; i < 120; i++) await recordCheckResult(org, m, i % 2 ? UP : DOWN, new Date(start + i * 30_000));
    expect(await notificationsOf(org)).toHaveLength(0);
  });

  it('a monitor that keeps opening and resolving incidents sends one "flapping" notification and holds back the rest', async () => {
    memoryTransport.reset();
    const org = await makeOrg('Flappy');
    const m = await newMonitor(org, 'flappy');
    const start = Date.now() - 3 * 3600_000;
    // Down for 1.5 minutes, up for 30 s, for an hour: an incident opens and resolves every 2 minutes (60 changes).
    let t = start;
    for (let cycle = 0; cycle < 30; cycle++) {
      for (const outcome of [DOWN, DOWN, DOWN, UP]) {
        await recordCheckResult(org, m, outcome, new Date(t));
        t += 30_000;
      }
    }
    const [{ n: opened }] = await withOrg(org.id, (tx) => tx.select({ n: db.$count(incidents, eq(incidents.monitorId, m.id)) }).from(schema.monitors).limit(1));
    expect(opened).toBe(30);
    await deliverPendingNotifications({ orgId: org.id });

    const mine = await notificationsOf(org, org.users.member.id);
    // opened, resolved, opened, resolved, then "flapping": 5, instead of 60.
    expect(mine.map((n) => n.category)).toEqual(['incident.opened', 'incident.resolved', 'incident.opened', 'incident.resolved', 'monitor.flapping']);
    expect(memoryTransport.to(org.users.member.email)).toHaveLength(5); // per channel: a handful
    expect(memoryTransport.to(org.users.member.email).at(-1)!.subject).toBe('[Flappy] flappy is flapping');

    // Quiet for over an hour, then a real outage: notified normally again.
    t += 61 * 60_000;
    await recordCheckResult(org, m, UP, new Date(t)); // settles
    const [{ flappingSince }] = await withOrg(org.id, (tx) => tx.select({ flappingSince: schema.monitors.flappingSince }).from(schema.monitors).where(eq(schema.monitors.id, m.id)));
    expect(flappingSince).toBeNull();
    await breakMonitor(org, m, t + 30_000);
    const after = await notificationsOf(org, org.users.member.id);
    expect(after.at(-1)?.category).toBe('incident.opened');
  });
});

describe('manual resolve notifies too', () => {
  it('"Mark resolved" in the UI sends the resolved notification', async () => {
    const org = await makeOrg('Manual');
    const m = await newMonitor(org, 'manual');
    await breakMonitor(org, m);
    const [incident] = await withOrg(org.id, (tx) => tx.select().from(incidents).where(eq(incidents.monitorId, m.id)));
    expect(await resolveIncident({ orgId: org.id, orgSlug: org.slug, orgName: 'Manual' }, incident.id)).toBe(true);
    expect((await notificationsOf(org, org.users.viewer.id)).map((n) => n.category)).toEqual(['incident.opened', 'incident.resolved']);
  });
});

describe('status-page subscribers: double opt-in and one-click unsubscribe (🟡)', () => {
  let org: Org;
  const unsubscribe = (url: string) => unsubscribeRoute.POST(new Request(url, { method: 'POST', body: 'List-Unsubscribe=One-Click' }));
  const tokenFrom = (url: string) => new URL(url).searchParams.get('token')!;

  beforeAll(async () => {
    org = await makeOrg('Public');
    memoryTransport.reset();
  });

  it('subscribing sends one confirmation email and subscribes nobody yet', async () => {
    expect(await subscribeToStatusPage(org.slug, 'Reader@Example.test')).toBe('check_inbox');
    expect(await subscribeToStatusPage(org.slug, 'reader@example.test')).toBe('check_inbox'); // a second click within 10 minutes
    await deliverPendingEmails();
    const mails = memoryTransport.to('reader@example.test');
    expect(mails).toHaveLength(1);
    expect(mails[0].from).toContain('updates.beacon.app'); // the status stream
    await breakMonitor(org, await newMonitor(org, 'before-confirming'));
    await deliverPendingNotifications({ orgId: org.id });
    expect(memoryTransport.to('reader@example.test')).toHaveLength(1); // still only the confirmation
  });

  it('confirming from the link subscribes; incident emails then carry the unsubscribe headers', async () => {
    const { confirmSubscription } = await import('@/lib/notifications/subscribers');
    const link = memoryTransport.to('reader@example.test')[0].text.match(/https?:\S+\/confirm\?token=\S+/)![0];
    expect(await confirmSubscription(`${tokenFrom(link)}x`)).toMatchObject({ ok: false }); // tampered
    expect(await confirmSubscription(tokenFrom(link))).toMatchObject({ ok: true });
    memoryTransport.reset();
    await breakMonitor(org, await newMonitor(org, 'after-confirming'));
    await deliverPendingNotifications({ orgId: org.id });
    const [update] = memoryTransport.to('reader@example.test');
    expect(update.subject).toBe('[Public status] after-confirming: investigating');
    expect(update.headers['List-Unsubscribe-Post']).toBe('List-Unsubscribe=One-Click');
  });

  it('the one-click POST removes the subscriber without a login; a forged token does nothing', async () => {
    const [update] = memoryTransport.to('reader@example.test');
    const oneClick = update.headers['List-Unsubscribe'].slice(1, -1);
    expect((await unsubscribe(`${oneClick}tampered`)).status).toBe(400);
    expect((await unsubscribe(oneClick)).status).toBe(200);
    const rows = await withOrg(org.id, (tx) => tx.select().from(statusPageSubscribers).where(eq(statusPageSubscribers.organizationId, org.id)));
    expect(rows).toHaveLength(0);
    expect((await unsubscribe(oneClick)).status).toBe(200); // idempotent
  });

  it('a member’s per-category unsubscribe link turns off that email only; in-app continues', async () => {
    const mail = memoryTransport.to(org.users.member.email).find((e) => e.subject.includes('after-confirming is down'))!;
    expect((await unsubscribe(mail.headers['List-Unsubscribe'].slice(1, -1))).status).toBe(200);
    memoryTransport.reset();
    await breakMonitor(org, await newMonitor(org, 'after-unsubscribing'));
    await deliverPendingNotifications({ orgId: org.id });
    expect(memoryTransport.to(org.users.member.email)).toHaveLength(0);
    expect(memoryTransport.to(org.users.owner.email)).toHaveLength(1);
    const latest = await withOrg(org.id, (tx) =>
      tx.select().from(notifications).where(and(eq(notifications.organizationId, org.id), eq(notifications.userId, org.users.member.id), eq(notifications.title, 'after-unsubscribing is down'))),
    );
    expect(latest).toHaveLength(1);
  });

  it('an unpublished status page cannot be subscribed to', async () => {
    await db.update(schema.organizations).set({ statusPagePublic: false }).where(eq(schema.organizations.id, org.id));
    expect(await subscribeToStatusPage(org.slug, 'late@example.test')).toBe('not_found');
  });
});
