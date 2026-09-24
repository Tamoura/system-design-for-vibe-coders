import { and, asc, desc, eq, gte, inArray, isNotNull, isNull, lt, sum } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg, type TenantTx } from '@/db/tenant';
import { PLANS, statusGrantsAccess } from '@/core/plans';
import { billingPeriod, METERS, rateSms, reachedThresholds, usageKeys, type Meter, type Period } from '@/core/usage';
import { getBillingProvider } from './billing/provider';
import { listBillingContacts } from './billing/sync';
import { sendEmail } from './email';
import { appUrl } from './urls';
import { entitlementsInTx } from './entitlements';

const { organizations, subscriptions, usageEvents, usageAlerts } = schema;

/*
 * Lesson 3.3: usage-based billing and metering.
 *
 *   recordSmsSent()  ──►  usage_events (one row per SMS, idempotent)
 *                              │
 *          getUsageSummary() ◄─┤ sum per billing period → the billing page
 *        reportPendingUsage() ◄┘ → the provider's meter (Stripe Billing meters)
 *                                   → Stripe rates it and puts it on the invoice
 */

type Scope = { orgId: string };

/**
 * Record one billable event. Safe to call twice with the same key: the
 * second call inserts nothing and returns `{ recorded: false }`.
 */
export async function recordUsage(
  { orgId }: Scope,
  event: { idempotencyKey: string; meter: Meter; quantity: number; occurredAt: Date },
): Promise<{ recorded: boolean }> {
  const { recorded, alerts } = await withOrg(orgId, async (tx) => {
    const inserted = await tx
      .insert(usageEvents)
      .values({ organizationId: orgId, ...event })
      .onConflictDoNothing({ target: usageEvents.idempotencyKey })
      .returning({ id: usageEvents.id });
    if (inserted.length === 0) return { recorded: false, alerts: [] as Alert[] };
    return { recorded: true, alerts: await newAlerts(tx, orgId, event.meter) };
  });
  // Emails go out after the transaction (lesson 2.4: no network inside withOrg).
  for (const alert of alerts) await emailUsageAlert(orgId, alert);
  return { recorded };
}

/**
 * Lesson 3.3 (🟢): the function Module 4's SMS worker calls, AFTER the SMS
 * provider accepted the message: that is when the cost is certain. Recording
 * when we merely *decide* to send would bill for messages that failed.
 *
 *   await recordSmsSent({ orgId }, { messageSid: msg.sid, segments: Number(msg.numSegments), sentAt: msg.dateCreated })
 *
 * The key comes from the message SID, so a retried job records nothing new.
 * `sentAt` is the send time (event time); it decides the billing period,
 * however late this call happens.
 */
export async function recordSmsSent(scope: Scope, sms: { messageSid: string; segments: number; sentAt: Date }) {
  return recordUsage(scope, {
    idempotencyKey: usageKeys.sms(sms.messageSid),
    meter: METERS.sms,
    quantity: Math.max(1, Math.floor(sms.segments)),
    occurredAt: sms.sentAt,
  });
}

/** The subscription whose period we bill against: the latest one that grants access. */
async function currentSubscription(tx: TenantTx, orgId: string) {
  const subs = await tx
    .select()
    .from(subscriptions)
    .where(eq(subscriptions.organizationId, orgId))
    .orderBy(desc(subscriptions.currentPeriodEnd));
  return subs.find((s) => statusGrantsAccess(s.status)) ?? null;
}

/** Sum of one meter for one org between two instants, by event time. */
async function usageInPeriod(tx: TenantTx, orgId: string, meter: Meter, period: Period): Promise<number> {
  const [row] = await tx
    .select({ total: sum(usageEvents.quantity).mapWith(Number) })
    .from(usageEvents)
    .where(
      and(
        eq(usageEvents.organizationId, orgId),
        eq(usageEvents.meter, meter),
        gte(usageEvents.occurredAt, period.start),
        lt(usageEvents.occurredAt, period.end),
      ),
    );
  return row?.total ?? 0;
}

/**
 * Lesson 3.3 (🟢): "SMS used this period" for the billing and settings pages,
 * for the org's current BILLING period (from its subscription), rated with
 * the plan's included amount and overage price.
 */
export async function getUsageSummary({ orgId }: Scope, now: Date = new Date()) {
  return withOrg(orgId, async (tx) => {
    const ent = await entitlementsInTx(tx, orgId);
    const period = billingPeriod(await currentSubscription(tx, orgId), now);
    const used = await usageInPeriod(tx, orgId, METERS.sms, period);
    return { period, sms: rateSms(used, ent) };
  });
}

type Alert = { threshold: number; used: number; included: number };

/**
 * Lesson 3.3 (🟡): alerts at 80% and 100% of the included SMS, each at most
 * once per org per period. The insert into usage_alerts is the "have we sent
 * it?" check: its primary key lets only the first one through.
 */
async function newAlerts(tx: TenantTx, orgId: string, meter: Meter): Promise<Alert[]> {
  if (meter !== METERS.sms) return [];
  const ent = await entitlementsInTx(tx, orgId);
  const period = billingPeriod(await currentSubscription(tx, orgId));
  const used = await usageInPeriod(tx, orgId, meter, period);
  const alerts: Alert[] = [];
  for (const threshold of reachedThresholds(used, ent.smsCreditsPerMonth)) {
    const first = await tx
      .insert(usageAlerts)
      .values({ organizationId: orgId, meter, periodStart: period.start, threshold })
      .onConflictDoNothing()
      .returning({ threshold: usageAlerts.threshold });
    if (first.length) alerts.push({ threshold, used, included: ent.smsCreditsPerMonth });
  }
  return alerts;
}

async function emailUsageAlert(orgId: string, alert: Alert) {
  const [org] = await db
    .select({ name: organizations.name, slug: organizations.slug, plan: organizations.plan })
    .from(organizations)
    .where(eq(organizations.id, orgId));
  for (const person of await listBillingContacts(orgId)) {
    await sendEmail({
      to: person.email,
      template: 'usage-alert',
      props: { orgName: org.name, planName: PLANS[org.plan].name, url: appUrl(`/${org.slug}/billing`), ...alert },
    });
  }
}

/**
 * Lesson 3.3 (🟡): send recorded usage to the billing provider's meter.
 * Run by `npm run usage:report` (from cron, until lesson 5.1's job queue).
 *
 *  - Every event is sent with its idempotency key as the identifier, so a
 *    re-run, or a crash between "sent" and "marked reported", cannot bill
 *    twice: the provider drops the duplicate.
 *  - A failed send is retried a few times, then left unreported for the
 *    next run. Nothing is lost.
 *  - Only orgs with a Stripe customer are reported; one that never paid has
 *    nothing to be billed for.
 *
 * Pricing lives in Stripe: a metered Price with a graduated first tier that
 * is free (100 on Pro), then $0.05 per unit, so we report every unit and
 * Stripe works out the overage.
 */
export async function reportPendingUsage(opts: { batchSize?: number; attempts?: number; backoffMs?: number } = {}) {
  const { batchSize = 500, attempts = 3, backoffMs = 250 } = opts;
  const provider = getBillingProvider();
  if (!provider) return { reported: 0, failed: 0 };
  const orgs = await db
    .select({ id: organizations.id, customerId: organizations.stripeCustomerId })
    .from(organizations)
    .where(isNotNull(organizations.stripeCustomerId));

  let reported = 0;
  let failed = 0;
  for (const org of orgs) {
    const pending = await withOrg(org.id, (tx) =>
      tx
        .select()
        .from(usageEvents)
        .where(and(eq(usageEvents.organizationId, org.id), isNull(usageEvents.reportedAt)))
        .orderBy(asc(usageEvents.occurredAt))
        .limit(batchSize),
    );
    const done: string[] = [];
    for (const e of pending) {
      // Network, outside the transaction.
      const ok = await withRetries(attempts, backoffMs, () =>
        provider.reportUsage({ customerId: org.customerId!, meter: e.meter, value: e.quantity, identifier: e.idempotencyKey, timestamp: e.occurredAt }),
      );
      if (ok) done.push(e.id);
      else failed++;
    }
    if (done.length) {
      await withOrg(org.id, (tx) =>
        tx
          .update(usageEvents)
          .set({ reportedAt: new Date() })
          .where(and(eq(usageEvents.organizationId, org.id), inArray(usageEvents.id, done))),
      );
      reported += done.length;
    }
  }
  return { reported, failed };
}

async function withRetries(attempts: number, backoffMs: number, fn: () => Promise<void>): Promise<boolean> {
  for (let i = 0; i < attempts; i++) {
    try {
      await fn();
      return true;
    } catch (err) {
      if (i === attempts - 1) {
        console.error('usage report failed, will retry on the next run:', (err as Error).message);
        return false;
      }
      await new Promise((r) => setTimeout(r, backoffMs * 2 ** i)); // 250 ms, 500 ms, …
    }
  }
  return false;
}
