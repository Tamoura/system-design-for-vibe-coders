import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn(), getSessionUser: vi.fn() }));
vi.mock('@/lib/email', () => ({ sendEmail: vi.fn(async () => ({ id: 'queued' })) }));

import { and, desc, eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { STAFF_PERMISSIONS, STAFF_ROLES, staffCan, type StaffPermission, type StaffRole } from '@/core/staff';
import { getCustomerOverview, searchCustomers } from '@/lib/admin/customers';
import { grantStaffRole, revokeStaff } from '@/lib/admin/staff';
import { cliAuditSource } from '@/lib/audit';
import { fakeBilling } from '@/lib/billing/provider';
import { syncCustomerFromStripe } from '@/lib/billing/sync';
import { expireComps } from '@/lib/billing/support';
import { getEntitlements } from '@/lib/entitlements';
import { createInvitation } from '@/lib/invitations';
import { requireMembership } from '@/lib/access';
import { createMonitor } from '@/lib/monitors';
import { scheduleChecks } from '@/lib/scheduler';
import { checkSlots } from '@/core/schedule';
import { getSessionUser, type CurrentUser } from '@/lib/session';
import { findStaffMember, requireStaff } from '@/lib/staff';
import * as actionRoute from '@/app/api/internal/orgs/[orgId]/[action]/route';
import * as staffRoute from '@/app/api/internal/staff/route';
import { makeOrg, makeUser, signInAs } from './helpers/fixtures';
import { clearQueues, jobsIn } from './helpers/queue';

/*
 * Lesson 7.1: Beacon's staff and the admin panel.
 *   🟢 a separate staff table; customers of ANY role get 404; search by partial email; usage from the entitlement code
 *   🟡 "Extend trial" (support, ≤ 14 days) and "Comp plan" (billing) through the billing service, with a reason and an audit event
 */
type Org = Awaited<ReturnType<typeof makeOrg>>;
const staffUser: Partial<Record<StaffRole, CurrentUser>> = {};
let acme: Org;

async function makeStaff(role: StaffRole) {
  const user = await makeUser(`staff-${role}`);
  await db.insert(schema.staffUsers).values({ userId: user.id, role });
  staffUser[role] = user;
  return user;
}

/** The real person at the keyboard (staff pages use getSessionUser, never the impersonated user). */
const actAs = (user: CurrentUser | null) => vi.mocked(getSessionUser).mockResolvedValue(user);

const post = (orgId: string, action: string, body: Record<string, unknown>, headers: Record<string, string> = {}) =>
  actionRoute.POST(new Request(`http://test/api/internal/orgs/${orgId}/${action}`, { method: 'POST', headers: { 'content-type': 'application/json', ...headers }, body: JSON.stringify(body) }), {
    params: Promise.resolve({ orgId, action }),
  });

const lastAudit = async (orgId: string, action: string) =>
  (await db.select().from(schema.auditEvents).where(and(eq(schema.auditEvents.organizationId, orgId), eq(schema.auditEvents.action, action))).orderBy(desc(schema.auditEvents.seq)).limit(1))[0];

beforeAll(async () => {
  acme = await makeOrg('Staff Acme', { plan: 'free' });
  for (const role of STAFF_ROLES) await makeStaff(role);
});

describe('staff roles (the lesson’s table)', () => {
  const EXPECTED: Record<StaffPermission, StaffRole[]> = {
    'customers.read': ['support', 'billing', 'engineer', 'superadmin'],
    'trial.extend': ['support', 'billing', 'superadmin'],
    'email.resend': ['support', 'superadmin'],
    'sessions.revoke': ['support', 'superadmin'],
    impersonate: ['support', 'engineer', 'superadmin'],
    'plan.comp': ['billing', 'superadmin'],
    'flags.manage': ['engineer', 'superadmin'],
    'audit.read': ['engineer', 'superadmin'],
    'analytics.read': ['support', 'billing', 'engineer', 'superadmin'],
    'staff.manage': ['superadmin'],
  };
  for (const [permission, roles] of Object.entries(EXPECTED) as [StaffPermission, StaffRole[]][]) {
    it(`${permission}: ${roles.join(', ')}`, () => expect(STAFF_ROLES.filter((r) => staffCan(r, permission))).toEqual(roles));
  }
  it('every permission any role has is in the table above', () => {
    expect(new Set(Object.values(STAFF_PERMISSIONS).flat())).toEqual(new Set(Object.keys(EXPECTED)));
  });
});

describe('🟢 who is staff: a separate table, not a customer role', () => {
  it('an org owner, admin, member or viewer is not staff: 404 on pages and on every staff route', async () => {
    for (const role of ['owner', 'admin', 'member', 'viewer'] as const) {
      actAs(acme.users[role]);
      await expect(requireStaff()).rejects.toMatchObject({ digest: expect.stringMatching(/;404$/) });
      expect((await post(acme.id, 'comp-plan', { plan: 'pro', reason: 'let me in please' })).status).toBe(404);
      expect((await post(acme.id, 'impersonate', { userId: acme.users.owner.id, reason: 'let me in please' })).status).toBe(404);
    }
    actAs(null);
    expect((await post(acme.id, 'extend-trial', { days: 3, reason: 'anonymous attempt' })).status).toBe(404);
  });

  it('an unverified account with a staff row is not staff either', async () => {
    const sneaky = await makeUser('sneaky', { emailVerified: false });
    await db.insert(schema.staffUsers).values({ userId: sneaky.id, role: 'superadmin' });
    expect(await findStaffMember(sneaky)).toBeNull();
    await db.delete(schema.staffUsers).where(eq(schema.staffUsers.userId, sneaky.id));
  });

  it('staff with a role lacking the permission get 403 on the page (forbidden) and the route', async () => {
    actAs(staffUser.support!);
    await expect(requireStaff('plan.comp')).rejects.toThrow(/forbidden\(\)/); // Next's forbidden(): the 403 page
    expect(await requireStaff('trial.extend')).toMatchObject({ role: 'support' });
  });

  it('a cross-site POST (another Origin) is refused even for staff', async () => {
    actAs(staffUser.billing!);
    const res = await post(acme.id, 'comp-plan', { plan: 'pro', reason: 'from an evil page' }, { origin: 'https://evil.example', host: 'test' });
    expect(res.status).toBe(403);
  });
});

describe('🟢 find a customer and see their state', () => {
  it('finds an org from a partial member email, a name, a slug or a Stripe customer id, in well under a second', async () => {
    const globex = await makeOrg('Globex Industries');
    await db.update(schema.organizations).set({ stripeCustomerId: 'cus_globex123' }).where(eq(schema.organizations.id, globex.id));
    for (let i = 0; i < 200; i++) await db.insert(schema.users).values({ name: `Filler ${i}`, email: `filler-${i}@elsewhere.test` });
    const started = performance.now();
    const byEmail = await searchCustomers(globex.users.viewer.email.slice(0, 12)); // "globex indus…" part of the email
    expect(performance.now() - started).toBeLessThan(1000);
    expect(byEmail.map((h) => h.id)).toContain(globex.id);
    expect((await searchCustomers('industries')).map((h) => h.id)).toContain(globex.id);
    expect((await searchCustomers('cus_globex123')).map((h) => [h.id, h.matched])).toEqual([[globex.id, 'Stripe customer']]);
    expect(await searchCustomers('%')).toEqual([]); // wildcards are escaped, one character is not a search
  });

  it('the org page shows usage against the limit from the product’s own entitlement code, members and the last 10 incidents', async () => {
    const m = await createMonitor({ orgId: acme.id, userId: acme.users.owner.id }, { name: 'acme-web', url: 'https://acme.test', intervalSeconds: 300 });
    for (let i = 0; i < 12; i++) {
      await withOrg(acme.id, (tx) => tx.insert(schema.incidents).values({ organizationId: acme.id, monitorId: m.id, cause: `HTTP 50${i % 10}`, openedAt: new Date(Date.now() - i * 60_000) }));
    }
    const o = (await getCustomerOverview(acme.id))!;
    expect(o.ent).toEqual(await getEntitlements({ orgId: acme.id })); // one source of truth
    expect(o.usage).toMatchObject({ total: 1, ent: { maxMonitors: 5, plan: 'free' } });
    expect(o.members.map((x) => x.role).sort()).toEqual(['admin', 'member', 'owner', 'viewer']);
    expect(o.recentIncidents).toHaveLength(10);
    expect(o.recentIncidents[0].cause).toBe('HTTP 500');
  });
});

describe('🟡 "Comp plan" (billing role): the plan changes everywhere at once, with a reason and an audit event', () => {
  it('support cannot (403, direct POST); billing can; the limits and the scheduler follow without a restart', async () => {
    actAs(staffUser.support!);
    expect((await post(acme.id, 'comp-plan', { plan: 'pro', reason: 'TICKET-9: nonprofit' })).status).toBe(403);

    // Six monitors on Free: one is frozen by the plan (lesson 3.2).
    for (let i = 0; i < 5; i++) await createMonitor({ orgId: acme.id, userId: acme.users.owner.id }, { name: `m${i}`, url: `https://m${i}.test`, intervalSeconds: 300 }).catch(() => null);
    await withOrg(acme.id, (tx) => tx.insert(schema.monitors).values({ organizationId: acme.id, name: 'frozen', url: 'https://frozen.test', paused: true, pausedReason: 'plan_limit' }));

    actAs(staffUser.billing!);
    const res = await post(acme.id, 'comp-plan', { plan: 'pro', months: 12, reason: 'TICKET-9: nonprofit, 12 months free' });
    expect(res.status).toBe(200);
    expect((await getEntitlements({ orgId: acme.id })).maxMonitors).toBe(50);
    const [frozen] = await withOrg(acme.id, (tx) => tx.select().from(schema.monitors).where(and(eq(schema.monitors.organizationId, acme.id), eq(schema.monitors.name, 'frozen'))));
    expect(frozen.paused).toBe(false); // the monitor the plan froze runs again…
    // …and the next scheduler run (it reads the plan snapshot from Postgres, no cache) checks it at its next slot.
    await clearQueues();
    const [slot] = checkSlots(frozen.id, frozen.intervalSeconds, new Date(), new Date(Date.now() + frozen.intervalSeconds * 1000));
    await scheduleChecks(slot);
    expect((await jobsIn('check.run')).map((j) => j.data.monitorId)).toContain(frozen.id);

    const comped = await lastAudit(acme.id, 'billing.plan_comped');
    expect(comped).toMatchObject({ actorType: 'staff', actorId: expect.any(String), actorEmail: staffUser.billing!.email, reason: 'TICKET-9: nonprofit, 12 months free', organizationId: acme.id });
    expect(comped.changes).toMatchObject({ comp_plan: { before: null, after: 'pro' } });
    const changed = await lastAudit(acme.id, 'billing.plan_changed');
    expect(changed.changes).toEqual({ plan: { before: 'free', after: 'pro' } });
  });

  it('refuses without a reason (400), and the comp ends by itself at its date', async () => {
    actAs(staffUser.billing!);
    const res = await post(acme.id, 'comp-plan', { plan: 'business' });
    expect(res.status).toBe(400);
    expect((await res.json()).message).toMatch(/reason/i);

    await expireComps(new Date(Date.now() + 400 * 86_400_000)); // a year and a bit later
    expect((await getEntitlements({ orgId: acme.id })).plan).toBe('free');
    expect(await lastAudit(acme.id, 'billing.comp_removed')).toMatchObject({ actorType: 'system', reason: expect.stringMatching(/end date/) });
  });
});

describe('🟡 "Extend trial" (support, at most 14 days): Stripe first, then our copy, in the same code path as the webhook', () => {
  let org: Org;
  let subId: string;

  beforeAll(async () => {
    vi.stubEnv('BILLING_PROVIDER', 'fake');
    org = await makeOrg('Trial Co', { plan: 'free' });
    const fake = fakeBilling();
    const { id: customerId } = await fake.createCustomer({ orgId: org.id, name: 'Trial Co', email: 'x@trial.test' }, `customer:${org.id}`);
    await db.update(schema.organizations).set({ stripeCustomerId: customerId }).where(eq(schema.organizations.id, org.id));
    const trialEnd = new Date(Date.now() + 2 * 86_400_000);
    subId = fake.seedSubscription({ customerId, status: 'trialing', priceId: 'price_fake_pro', currentPeriodStart: new Date(), currentPeriodEnd: trialEnd, cancelAtPeriodEnd: false, trialEnd }).id;
    await syncCustomerFromStripe(customerId);
  });

  it('extends Postgres AND the billing provider, and records staff, org, reason, before and after', async () => {
    const [before] = await withOrg(org.id, (tx) => tx.select().from(schema.subscriptions).where(eq(schema.subscriptions.id, subId)));
    actAs(staffUser.support!);
    const res = await post(org.id, 'extend-trial', { days: 3, reason: 'TICKET-1234: owner on a plane during an outage' }, { 'x-forwarded-for': '192.0.2.44' });
    expect(res.status).toBe(200);
    const [after] = await withOrg(org.id, (tx) => tx.select().from(schema.subscriptions).where(eq(schema.subscriptions.id, subId)));
    expect(after.trialEnd!.getTime() - before.trialEnd!.getTime()).toBe(3 * 86_400_000);
    expect(fakeBilling().subscriptions.get(subId)!.trialEnd!.getTime()).toBe(after.trialEnd!.getTime()); // "Stripe" agrees
    expect(await lastAudit(org.id, 'billing.trial_extended')).toMatchObject({
      actorType: 'staff',
      actorEmail: staffUser.support!.email,
      ipAddress: '192.0.2.44',
      reason: 'TICKET-1234: owner on a plane during an outage',
      changes: { trial_end: { before: before.trialEnd!.toISOString(), after: after.trialEnd!.toISOString() } },
    });
    expect((await getEntitlements({ orgId: org.id })).plan).toBe('pro'); // trialing grants the plan (lesson 3.1)
  });

  it('refuses more than 14 days, and an org with no trial', async () => {
    actAs(staffUser.support!);
    expect((await post(org.id, 'extend-trial', { days: 15, reason: 'a very long favour' })).status).toBe(400);
    expect((await post(acme.id, 'extend-trial', { days: 2, reason: 'no trial here, though' })).status).toBe(400);
  });
});

describe('support actions on people, and staff management', () => {
  it('resend an invitation: same code path as the customer’s button, audited as support with the reason', async () => {
    signInAs(acme.users.owner);
    const inv = await createInvitation(await requireMembership(acme.slug), { email: 'lost-in-spam@acme.test', role: 'member' });
    actAs(staffUser.support!);
    const res = await post(acme.id, 'resend-invitation', { invitationId: inv.id, reason: 'TICKET-77: invite went to spam' });
    expect(res.status).toBe(200);
    expect(await lastAudit(acme.id, 'support.invitation_resent')).toMatchObject({ targetId: inv.id, reason: 'TICKET-77: invite went to spam' });
  });

  it('sign a member out everywhere', async () => {
    await db.insert(schema.sessions).values({ userId: acme.users.member.id, token: 'tok-1', expiresAt: new Date(Date.now() + 3600_000) });
    actAs(staffUser.support!);
    expect((await post(acme.id, 'revoke-sessions', { userId: acme.users.member.id, reason: 'TICKET-78: lost laptop' })).status).toBe(200);
    expect(await db.select().from(schema.sessions).where(eq(schema.sessions.userId, acme.users.member.id))).toEqual([]);
    expect(await lastAudit(acme.id, 'support.sessions_revoked')).toMatchObject({ metadata: { sessions: 1 } });
    // Someone outside the org cannot be targeted from this org's page.
    const outsider = await makeUser('outsider');
    expect((await post(acme.id, 'revoke-sessions', { userId: outsider.id, reason: 'not a member of acme' })).status).toBe(400);
  });

  it('only superadmins grant roles; never your own; never the last superadmin', async () => {
    const hire = await makeUser('new-hire');
    actAs(staffUser.engineer!);
    const req = (body: object) => staffRoute.POST(new Request('http://test/api/internal/staff', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) }), { params: Promise.resolve({}) });
    expect((await req({ email: hire.email, role: 'support', reason: 'joined support' })).status).toBe(403);
    actAs(staffUser.superadmin!);
    expect((await req({ email: hire.email, role: 'support', reason: 'joined support, HR-1' })).status).toBe(200);
    expect(await findStaffMember(hire)).toMatchObject({ role: 'support' });
    const [granted] = await db.select().from(schema.auditEvents).where(eq(schema.auditEvents.action, 'staff.granted')).orderBy(desc(schema.auditEvents.seq)).limit(1);
    expect(granted).toMatchObject({ organizationId: null, reason: 'joined support, HR-1', changes: { role: { before: null, after: 'support' } } });

    const me = (await findStaffMember(staffUser.superadmin!))!;
    await expect(grantStaffRole({ email: staffUser.superadmin!.email, role: 'support', reason: 'demote myself' }, cliAuditSource('test'), me.staffId)).rejects.toThrow(/your own/);
    await expect(revokeStaff(me.staffId, 'leaving', cliAuditSource('test'))).rejects.toThrow(/at least one superadmin/);
  });
});
