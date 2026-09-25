import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import type { CheckOutcome } from '@/core/check';
import { activatedAt, CHECKLIST, MILESTONES, onboardingState } from '@/core/onboarding';
import { createMonitorInput, organizationNameInput } from '@/core/validation';
import { recordCheckResult } from '@/lib/checks';
import { createInvitation } from '@/lib/invitations';
import { createMonitor } from '@/lib/monitors';
import { saveOrgNotificationSettings } from '@/lib/notifications';
import { getOnboarding } from '@/lib/onboarding';
import { createOrganization, getOrganization, setStatusPagePublic } from '@/lib/organizations';
import { createEndpoint } from '@/lib/webhooks';
import * as settingsRoute from '@/app/api/orgs/[orgSlug]/settings/route';
import * as monitorsRoute from '@/app/api/orgs/[orgSlug]/monitors/route';
import { navFor, switchOrgHref } from '@/app/[orgSlug]/_shell/nav';
import { makeOrg, makeUser, signInAs } from './helpers/fixtures';

/*
 * Lesson 6.1: onboarding milestones stored on the org, the settings split
 * with server-side permission checks, the shared form schema and the shell's
 * navigation rules.
 */
const UP: CheckOutcome = { ok: true, statusCode: 200, latencyMs: 30, error: null };
type Org = Awaited<ReturnType<typeof makeOrg>>;
const H = 3600 * 1000;

const ctxOf = (org: Org, role: keyof Org['users']) => ({
  orgId: org.id,
  orgSlug: org.slug,
  orgName: org.name,
  userId: org.users[role].id,
  userEmail: org.users[role].email,
  emailVerified: true,
  role,
});

beforeAll(() => {
  vi.stubEnv('EMAIL_DRIVER', 'memory');
  vi.stubEnv('SLACK_PROVIDER', 'fake');
});

describe('onboarding state and activation (pure)', () => {
  it('lists the checklist in order and completes when every milestone is reached', () => {
    expect(CHECKLIST.map((s) => s.milestone)).toEqual([...MILESTONES]);
    const created = new Date('2026-09-01T00:00:00Z');
    const empty = onboardingState(created, new Map());
    expect(empty).toMatchObject({ done: 0, total: 5, complete: false, activatedAt: null });
    const all = onboardingState(created, new Map(MILESTONES.map((m) => [m, created])));
    expect(all).toMatchObject({ done: 5, complete: true });
  });

  it('activation = first check result within 24 hours of the org being created', () => {
    const created = new Date('2026-09-01T00:00:00Z');
    expect(activatedAt(created, new Date(created.getTime() + 23 * H))).toEqual(new Date(created.getTime() + 23 * H));
    expect(activatedAt(created, new Date(created.getTime() + 25 * H))).toBeNull();
    expect(activatedAt(created, null)).toBeNull();
  });
});

describe('a new org walks through onboarding (🟡)', () => {
  let org: Org;
  let monitor: { id: string; name: string; url: string };

  beforeAll(async () => {
    const owner = await makeUser('Newbie');
    const created = await createOrganization(owner.id, 'Newbie Inc');
    // The org as a fresh sign-up has it: Free and nothing published. (makeOrg would publish its status page.)
    const admin = await makeUser('Newbie-admin');
    await db.insert(schema.memberships).values({ organizationId: created.id, userId: admin.id, role: 'admin' });
    org = { ...created, name: 'Newbie Inc', users: { owner, admin, member: admin, viewer: admin } };
  });

  it('starts empty, with the status page NOT published', async () => {
    expect(await getOnboarding({ orgId: org.id })).toMatchObject({ done: 0, complete: false });
    expect((await getOrganization({ orgId: org.id }))?.statusPagePublic).toBe(false);
  });

  it('first monitor → first check → alert channel → teammate → status page, each stored with its time', async () => {
    monitor = await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name: 'Site', url: 'https://newbie.test', intervalSeconds: 300 });
    expect((await getOnboarding({ orgId: org.id })).done).toBe(1);

    const checkedAt = new Date(Date.now() + 1000);
    await recordCheckResult({ id: org.id, name: org.name, slug: org.slug }, monitor, UP, checkedAt);
    const afterCheck = await getOnboarding({ orgId: org.id });
    expect(afterCheck.steps.find((s) => s.milestone === 'first_check')?.reachedAt).toEqual(checkedAt);
    expect(afterCheck.activatedAt).toEqual(checkedAt); // within 24 h of creation: activated

    await createEndpoint({ orgId: org.id, userId: org.users.admin.id }, { url: 'https://93.184.215.14/hooks', eventTypes: ['incident.opened'] });
    await createInvitation(ctxOf(org, 'owner'), { email: 'teammate@example.com', role: 'member' });
    expect((await getOnboarding({ orgId: org.id })).complete).toBe(false);
    await setStatusPagePublic(ctxOf(org, 'admin'), true);

    const done = await getOnboarding({ orgId: org.id });
    expect(done.complete).toBe(true);
    expect(done.steps.every((s) => s.reachedAt instanceof Date)).toBe(true);
    // Who got there is recorded too (null for what Beacon did by itself).
    const rows = await withOrg(org.id, (tx) => tx.select().from(schema.orgMilestones).where(eq(schema.orgMilestones.organizationId, org.id)));
    expect(Object.fromEntries(rows.map((r) => [r.milestone, r.userId]))).toEqual({
      monitor_created: org.users.owner.id,
      first_check: null,
      alert_channel_connected: org.users.admin.id,
      teammate_invited: org.users.owner.id,
      status_page_published: org.users.admin.id,
    });
  });

  it('a milestone keeps the time it was FIRST reached', async () => {
    const before = (await getOnboarding({ orgId: org.id })).steps.find((s) => s.milestone === 'monitor_created')!.reachedAt;
    await createMonitor({ orgId: org.id, userId: org.users.admin.id }, { name: 'Second', url: 'https://two.newbie.test', intervalSeconds: 300 });
    await setStatusPagePublic(ctxOf(org, 'admin'), false);
    await setStatusPagePublic(ctxOf(org, 'admin'), true);
    const after = await getOnboarding({ orgId: org.id });
    expect(after.steps.find((s) => s.milestone === 'monitor_created')!.reachedAt).toEqual(before);
  });

  it('a second admin who joins after onboarding is done never sees the checklist', async () => {
    const late = await makeUser('Late-admin');
    await db.insert(schema.memberships).values({ organizationId: org.id, userId: late.id, role: 'admin' });
    // The state is the org's, not the person's: nothing about "late" is read at all.
    expect((await getOnboarding({ orgId: org.id })).complete).toBe(true);
  });

  it('connecting Slack counts as an alert channel too', async () => {
    const other = await createOrganization((await makeUser('Slacker')).id, 'Slack First');
    await saveOrgNotificationSettings({ orgId: other.id, userId: null }, { allowed: new Set(), slackWebhookUrl: 'https://hooks.slack.com/services/T0/B0/x' });
    const state = await getOnboarding({ orgId: other.id });
    expect(state.steps.find((s) => s.milestone === 'alert_channel_connected')?.reachedAt).toBeInstanceOf(Date);
    expect(state.done).toBe(1);
  });

  it('another org cannot read these milestones (row-level security)', async () => {
    const globex = await makeOrg('Globex Onboarding');
    const seen = await withOrg(globex.id, (tx) => tx.select().from(schema.orgMilestones));
    expect(seen.every((m) => m.organizationId === globex.id)).toBe(true);
    expect((await getOnboarding({ orgId: globex.id })).done).toBe(0);
  });
});

describe('settings: the org-rename endpoint checks the permission on the server (🟡)', () => {
  let acme: Org;
  beforeAll(async () => {
    acme = await makeOrg('Rename Me');
  });
  const patch = (orgSlug: string, body: unknown) =>
    settingsRoute.PATCH(new Request('http://test/x', { method: 'PATCH', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) }), { params: Promise.resolve({ orgSlug }) });

  it('a Member gets 403 from the endpoint itself, not just a hidden button', async () => {
    signInAs(acme.users.member);
    expect((await patch(acme.slug, { name: 'Pwned' })).status).toBe(403);
    signInAs(acme.users.viewer);
    expect((await patch(acme.slug, { name: 'Pwned' })).status).toBe(403);
    expect((await getOrganization({ orgId: acme.id }))?.name).toBe('Rename Me');
  });

  it('an admin renames it; the slug (and every URL) stays', async () => {
    signInAs(acme.users.admin);
    const res = await patch(acme.slug, { name: '  Acme Renamed ' });
    expect(res.status).toBe(200);
    expect(await getOrganization({ orgId: acme.id })).toMatchObject({ name: 'Acme Renamed', slug: acme.slug });
  });

  it('refuses a name the shared schema refuses, with the same message the form shows', async () => {
    signInAs(acme.users.owner);
    const res = await patch(acme.slug, { name: 'x' });
    expect(res.status).toBe(400);
    const expected = organizationNameInput.safeParse({ name: 'x' }).error!.flatten().fieldErrors.name;
    expect((await res.json()).issues.name).toEqual(expected);
  });
});

describe('add a monitor: one schema, in the browser and on the server (🟢)', () => {
  it('curl with an invalid URL gets the same message the form shows inline', async () => {
    const acme = await makeOrg('Schema Co');
    signInAs(acme.users.member);
    const bad = { name: 'Site', url: 'not a url', intervalSeconds: 300 };
    // What the browser computes before sending anything (new-monitor-form.tsx):
    const inline = createMonitorInput.safeParse(bad).error!.flatten().fieldErrors.url;
    expect(inline?.[0]).toBe('Enter a full URL, like https://example.com/health'); // the form shows the first message
    // What the server answers to the same payload:
    const res = await monitorsRoute.POST(new Request('http://test/x', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(bad) }), { params: Promise.resolve({ orgSlug: acme.slug }) });
    expect(res.status).toBe(400);
    expect((await res.json()).issues.url).toEqual(inline);
  });
});

describe('the app shell navigation (🟢)', () => {
  it('shows each role only what it may open', () => {
    const items = (role: Parameters<typeof navFor>[0]) => navFor(role).flatMap((g) => g.items.map((i) => i.section));
    expect(items('viewer')).toEqual(['monitors', 'incidents', 'status-page', 'settings/general', 'members']);
    expect(items('owner')).toEqual(expect.arrayContaining(['billing', 'settings/api-keys', 'settings/webhooks', 'settings/notifications']));
    expect(items('admin')).not.toContain('billing');
  });

  it('the org switcher changes the org segment of the URL and keeps the section', () => {
    expect(switchOrgHref('/acme/incidents', 'globex', 'viewer')).toBe('/globex/incidents');
    expect(switchOrgHref('/acme/settings/webhooks/0b6f', 'globex', 'admin')).toBe('/globex/settings/webhooks');
    // A deep link to Acme's monitor does not exist in Globex: the section only.
    expect(switchOrgHref('/acme/monitors/5c1d-uuid', 'globex', 'owner')).toBe('/globex/monitors');
    // A section your role in the other org cannot open: back to Monitors, not a 403 page.
    expect(switchOrgHref('/acme/settings/api-keys', 'globex', 'viewer')).toBe('/globex/monitors');
  });
});
