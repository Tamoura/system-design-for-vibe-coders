import { beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));
vi.mock('@/lib/email', () => ({ sendEmail: vi.fn() }));

import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { sendEmail } from '@/lib/email';
import { fakeBilling } from '@/lib/billing/provider';
import { getUsageSummary, recordSmsSent, reportPendingUsage } from '@/lib/usage';
import { makeOrg } from './helpers/fixtures';

/*
 * Lesson 3.3: usage events for SMS. Module 4's SMS worker will call
 * recordSmsSent() after the SMS provider accepts a message; these tests play
 * that worker.
 */

const fake = fakeBilling();
const { usageEvents, organizations, subscriptions } = schema;

beforeAll(() => vi.stubEnv('BILLING_PROVIDER', 'fake'));

/** A Pro org whose billing period runs from the 14th to the 14th, like the lesson's Acme. */
async function proOrg(name: string) {
  const org = await makeOrg(name, { plan: 'pro' });
  const customerId = `cus_${name}`;
  await db.update(organizations).set({ stripeCustomerId: customerId }).where(eq(organizations.id, org.id));
  const period = { currentPeriodStart: new Date('2026-05-14T00:00:00Z'), currentPeriodEnd: new Date('2099-06-14T00:00:00Z') };
  await withOrg(org.id, (tx) =>
    tx.insert(subscriptions).values({ id: `sub_${name}`, organizationId: org.id, stripeCustomerId: customerId, status: 'active', priceId: 'price_fake_pro', ...period }),
  );
  return { ...org, customerId, period };
}

async function eventsOf(orgId: string) {
  return withOrg(orgId, (tx) => tx.select().from(usageEvents).where(eq(usageEvents.organizationId, orgId)));
}

describe('recording usage (🟢)', () => {
  let org: Awaited<ReturnType<typeof proOrg>>;
  beforeAll(async () => {
    org = await proOrg('Texter');
  });

  it('running the SMS job twice for the same message creates one usage row', async () => {
    const sms = { messageSid: 'SM0001', segments: 2, sentAt: new Date('2026-05-20T10:00:00Z') };
    expect(await recordSmsSent({ orgId: org.id }, sms)).toEqual({ recorded: true });
    expect(await recordSmsSent({ orgId: org.id }, sms)).toEqual({ recorded: false });
    const rows = await eventsOf(org.id);
    expect(rows).toHaveLength(1);
    expect(rows[0]).toMatchObject({ idempotencyKey: 'sms:SM0001', meter: 'sms_segments', quantity: 2 });
  });

  it('stores occurred_at from the send time, not the time of insertion', async () => {
    const sentAt = new Date('2026-05-13T23:59:58Z'); // arrives "now", happened last period
    await recordSmsSent({ orgId: org.id }, { messageSid: 'SM-late', segments: 1, sentAt });
    const row = (await eventsOf(org.id)).find((e) => e.idempotencyKey === 'sms:SM-late')!;
    expect(row.occurredAt).toEqual(sentAt);
    expect(row.createdAt.getTime()).toBeGreaterThan(sentAt.getTime());
  });

  it('counts the current BILLING period (14th to 14th), not the calendar month', async () => {
    await recordSmsSent({ orgId: org.id }, { messageSid: 'SM-june', segments: 1, sentAt: new Date('2026-06-02T08:00:00Z') });
    const summary = await getUsageSummary({ orgId: org.id }, new Date('2026-06-03T00:00:00Z'));
    // 2 (May 20) + 1 (June 2) inside the period; the May 13 one is in the previous period.
    expect(summary.sms).toMatchObject({ used: 3, included: 100, overageUnits: 0 });
    expect(summary.period.start).toEqual(org.period.currentPeriodStart);
  });

  it('usage is tenant data: another org sees none of it, even by key', async () => {
    const other = await proOrg('Other');
    expect(await eventsOf(other.id)).toEqual([]);
    const all = await withOrg(other.id, (tx) => tx.select().from(usageEvents));
    expect(all).toEqual([]);
    // The same key from another org does not create a second row either (keys are global facts).
    expect(await recordSmsSent({ orgId: other.id }, { messageSid: 'SM0001', segments: 1, sentAt: new Date() })).toEqual({ recorded: false });
  });
});

describe('overage, alerts and reporting to the meter (🟡)', () => {
  let org: Awaited<ReturnType<typeof proOrg>>;
  let alertSubjects: string[];
  const sentAt = (i: number) => new Date(Date.UTC(2026, 4, 20, 0, i));

  beforeAll(async () => {
    org = await proOrg('Flappy');
    vi.mocked(sendEmail).mockClear();
    for (let i = 1; i <= 130; i++) await recordSmsSent({ orgId: org.id }, { messageSid: `SMf${i}`, segments: 1, sentAt: sentAt(i) });
    alertSubjects = vi.mocked(sendEmail).mock.calls.map(([m]) => `${m.template} ${(m.props as { threshold: number }).threshold}%`); // (mocks are cleared between tests)
  });

  beforeEach(() => {
    fake.failNextReports = 0;
  });

  it('130 SMS on Pro: 30 over the included 100, a $1.50 overage', async () => {
    const { sms } = await getUsageSummary({ orgId: org.id }, new Date('2026-05-21T00:00:00Z'));
    expect(sms).toEqual({ used: 130, included: 100, overageUnits: 30, overageCents: 150 });
  });

  it('sends each alert (80%, 100%) at most once per org per period', async () => {
    expect(alertSubjects).toEqual([expect.stringContaining('80%'), expect.stringContaining('100%')]);
    vi.mocked(sendEmail).mockClear();
    await recordSmsSent({ orgId: org.id }, { messageSid: 'SMf-extra', segments: 1, sentAt: sentAt(200) });
    expect(vi.mocked(sendEmail)).not.toHaveBeenCalled();
  });

  it('reports every event to the meter with its idempotency key; Beacon’s count and the meter’s match', async () => {
    fake.meterEvents.clear();
    const result = await reportPendingUsage({ backoffMs: 0 });
    expect(result.failed).toBe(0);
    expect(fake.meterEvents.has('sms:SMf1')).toBe(true);
    const { period } = await getUsageSummary({ orgId: org.id });
    const beacon = (await getUsageSummary({ orgId: org.id })).sms.used;
    expect(fake.meterSummary(org.customerId, 'sms_segments', period.start, period.end)).toBe(beacon);
    expect((await eventsOf(org.id)).every((e) => e.reportedAt !== null)).toBe(true);
  });

  it('replaying the reporting job changes nothing', async () => {
    const before = fake.meterSummary(org.customerId, 'sms_segments', new Date(0), new Date('2100-01-01'));
    // Pretend the job crashed after sending but before marking rows as reported.
    await withOrg(org.id, (tx) => tx.update(usageEvents).set({ reportedAt: null }).where(eq(usageEvents.organizationId, org.id)));
    await reportPendingUsage({ backoffMs: 0 });
    await reportPendingUsage({ backoffMs: 0 });
    expect(fake.meterSummary(org.customerId, 'sms_segments', new Date(0), new Date('2100-01-01'))).toBe(before);
  });

  it('retries a failing send, and leaves it for the next run when it keeps failing', async () => {
    await recordSmsSent({ orgId: org.id }, { messageSid: 'SM-retry', segments: 1, sentAt: sentAt(300) });
    fake.failNextReports = 2; // two blips, then success on the third attempt
    expect(await reportPendingUsage({ backoffMs: 0 })).toEqual({ reported: 1, failed: 0 });

    await recordSmsSent({ orgId: org.id }, { messageSid: 'SM-down', segments: 1, sentAt: sentAt(301) });
    fake.failNextReports = 3; // down for the whole run
    expect(await reportPendingUsage({ backoffMs: 0 })).toEqual({ reported: 0, failed: 1 });
    expect((await eventsOf(org.id)).find((e) => e.idempotencyKey === 'sms:SM-down')?.reportedAt).toBeNull();
    expect(await reportPendingUsage({ backoffMs: 0 })).toEqual({ reported: 1, failed: 0 });
  });
});
