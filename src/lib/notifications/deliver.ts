import { and, count, eq, gt, inArray, lte, sql } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { SMS_PER_HOUR, smsText } from '@/core/notifications';
import { MAX_ATTEMPTS, retryDelayMs } from '@/core/retry';
import type { TemplateName, TemplateProps } from '@/emails';
import { deliverEmail } from '../email';
import { recordSmsSent } from '../usage';
import type { DeliveryPayload } from './pipeline';
import { getSlackSender, getSmsProvider } from './providers';

const { organizations, notificationDeliveries, users } = schema;
type Delivery = typeof notificationDeliveries.$inferSelect & { payload: DeliveryPayload };
type Outcome = 'sent' | 'suppressed' | 'throttled' | 'skipped' | 'retrying' | 'failed';

/** How long a worker owns the deliveries it claimed; a crashed worker's rows are due again after this. */
const LEASE_MS = 5 * 60_000;
const HOUR_MS = 60 * 60 * 1000;

/**
 * Lesson 4.2 (🟡): the channel workers. Each pending delivery is a job for
 * its channel (email, SMS, Slack), claimed with FOR UPDATE SKIP LOCKED,
 * sent outside any transaction, and its outcome written back to the same
 * row, which is the delivery log.
 *
 * Runs after every notify() (after the response) and from
 * `npm run messages:send`. Per org, inside withOrg(), like every tenant job
 * (lesson 2.4). A few rounds per org, because a round can create new work:
 * a throttled SMS becomes a fallback email, an SMS can trigger a usage alert.
 */
export async function deliverPendingNotifications(opts: { orgId?: string; limit?: number } = {}) {
  const counts: Record<Outcome, number> = { sent: 0, suppressed: 0, throttled: 0, skipped: 0, retrying: 0, failed: 0 };
  const orgIds = opts.orgId ? [opts.orgId] : (await db.select({ id: organizations.id }).from(organizations)).map((o) => o.id);
  for (const orgId of orgIds) {
    for (let round = 0; round < 10; round++) {
      const claimed = await claimDue(orgId, opts.limit ?? 50);
      if (claimed.length === 0) break;
      for (const delivery of claimed) counts[await deliverOne(delivery)]++;
    }
  }
  return counts;
}

async function claimDue(orgId: string, limit: number): Promise<Delivery[]> {
  return withOrg(orgId, async (tx) => {
    const due = tx
      .select({ id: notificationDeliveries.id })
      .from(notificationDeliveries)
      .where(
        and(
          eq(notificationDeliveries.organizationId, orgId),
          eq(notificationDeliveries.status, 'pending'),
          lte(notificationDeliveries.nextAttemptAt, new Date()),
        ),
      )
      .orderBy(notificationDeliveries.createdAt)
      .limit(limit)
      .for('update', { skipLocked: true });
    const rows = await tx
      .update(notificationDeliveries)
      .set({ attempts: sql`${notificationDeliveries.attempts} + 1`, nextAttemptAt: new Date(Date.now() + LEASE_MS) })
      .where(and(eq(notificationDeliveries.organizationId, orgId), inArray(notificationDeliveries.id, due)))
      .returning();
    // RETURNING comes back in storage order, not the subquery's: restore "oldest first".
    return (rows as Delivery[]).sort((a, b) => a.createdAt.getTime() - b.createdAt.getTime());
  });
}

type Patch = Partial<Pick<Delivery, 'status' | 'providerMessageId' | 'error' | 'sentAt' | 'nextAttemptAt'>>;

async function record(d: Delivery, patch: Patch) {
  await withOrg(d.organizationId, (tx) =>
    tx
      .update(notificationDeliveries)
      .set(patch)
      .where(and(eq(notificationDeliveries.organizationId, d.organizationId), eq(notificationDeliveries.id, d.id))),
  );
}

async function deliverOne(d: Delivery): Promise<Outcome> {
  try {
    switch (d.channel) {
      case 'email':
        return await sendEmailDelivery(d);
      case 'sms':
        return await sendSmsDelivery(d);
      case 'slack':
        return await sendSlackDelivery(d);
      case 'in_app':
        await record(d, { status: 'sent', sentAt: new Date() }); // written as sent by notify(); nothing to do
        return 'sent';
    }
  } catch (err) {
    // The provider refused or is down: retry with backoff, then give up visibly.
    const giveUp = d.attempts >= MAX_ATTEMPTS;
    await record(d, {
      status: giveUp ? 'failed' : 'pending',
      nextAttemptAt: new Date(Date.now() + retryDelayMs(d.attempts)),
      error: (err as Error).message.slice(0, 500),
    });
    return giveUp ? 'failed' : 'retrying';
  }
}

/** Email: the same send step as the outbox (suppression list, template, List-Unsubscribe), keyed by this delivery. */
async function sendEmailDelivery(d: Delivery): Promise<Outcome> {
  const email = d.payload.email;
  if (!email) {
    await record(d, { status: 'skipped', error: 'no email content' });
    return 'skipped';
  }
  const result = await deliverEmail({
    to: d.recipient,
    template: email.template,
    props: email.props as TemplateProps<TemplateName>,
    idempotencyKey: `delivery:${d.id}`,
    listUnsubscribe: d.payload.listUnsubscribe,
  });
  if (result.status === 'suppressed') {
    await record(d, { status: 'suppressed', error: `address suppressed: ${result.reason}` });
    return 'suppressed';
  }
  await record(d, { status: 'sent', providerMessageId: result.providerMessageId, sentAt: new Date(), error: null });
  return 'sent';
}

/**
 * SMS, with the lesson's throttle: at most SMS_PER_HOUR per person per hour
 * (in this org). The next one is not sent: it is marked "throttled" and an
 * email goes out instead, saying how many SMS were held back.
 * Once the provider accepts a message, it is metered (lesson 3.3).
 */
async function sendSmsDelivery(d: Delivery): Promise<Outcome> {
  const provider = getSmsProvider();
  if (!provider) {
    await record(d, { status: 'skipped', error: 'no SMS provider configured' });
    return 'skipped';
  }
  const hourAgo = new Date(Date.now() - HOUR_MS);
  const sentLastHour = await countSms(d, 'sent', hourAgo);
  if (sentLastHour >= SMS_PER_HOUR) {
    await holdBackSms(d, hourAgo);
    return 'throttled';
  }

  const receipt = await provider.send({ to: d.recipient, body: smsText(d.payload.title, d.payload.url), idempotencyKey: `delivery:${d.id}` });
  await record(d, { status: 'sent', providerMessageId: receipt.sid, sentAt: receipt.sentAt, error: null });
  // Lesson 3.3: the cost is certain now. The SID is the idempotency key, so a retried job is not billed twice.
  await recordSmsSent({ orgId: d.organizationId }, { messageSid: receipt.sid, segments: receipt.segments, sentAt: receipt.sentAt });
  return 'sent';
}

async function countSms(d: Delivery, status: 'sent' | 'throttled', since: Date): Promise<number> {
  const column = status === 'sent' ? notificationDeliveries.sentAt : notificationDeliveries.createdAt;
  const [row] = await withOrg(d.organizationId, (tx) =>
    tx
      .select({ n: count() })
      .from(notificationDeliveries)
      .where(
        and(
          eq(notificationDeliveries.organizationId, d.organizationId),
          eq(notificationDeliveries.userId, d.userId!),
          eq(notificationDeliveries.channel, 'sms'),
          eq(notificationDeliveries.status, status),
          gt(column, since),
        ),
      ),
  );
  return row.n;
}

/** The throttled SMS becomes an email (its own delivery, so it is logged and retried like any other). */
async function holdBackSms(d: Delivery, hourAgo: Date) {
  await record(d, { status: 'throttled', error: `more than ${SMS_PER_HOUR} SMS in an hour; sent by email instead` });
  const heldBack = await countSms(d, 'throttled', hourAgo);
  await withOrg(d.organizationId, async (tx) => {
    const [user] = await tx.select({ email: users.email }).from(users).where(eq(users.id, d.userId!));
    if (!user) return;
    await tx
      .insert(notificationDeliveries)
      .values({
        organizationId: d.organizationId,
        notificationId: d.notificationId,
        userId: d.userId,
        channel: 'email',
        dedupeKey: `${d.dedupeKey}:sms-fallback`,
        recipient: user.email,
        payload: {
          ...d.payload,
          email: {
            template: 'sms-held-back',
            props: { orgName: d.payload.orgName, heldBack, limit: SMS_PER_HOUR, title: d.payload.title, url: d.payload.url },
          },
          listUnsubscribe: null,
        } satisfies DeliveryPayload,
      })
      .onConflictDoNothing({ target: notificationDeliveries.dedupeKey });
  });
}

/** Slack: the org's incoming webhook, looked up at send time (it may have changed or been removed). */
async function sendSlackDelivery(d: Delivery): Promise<Outcome> {
  const [org] = await db.select({ url: organizations.slackWebhookUrl }).from(organizations).where(eq(organizations.id, d.organizationId));
  if (!org?.url) {
    await record(d, { status: 'skipped', error: 'no Slack webhook configured' });
    return 'skipped';
  }
  const { title, body, url } = d.payload;
  const { id } = await getSlackSender().post(org.url, { text: `*${title}*\n${body}\n<${url}|Open in Beacon>` });
  await record(d, { status: 'sent', providerMessageId: id, sentAt: new Date(), error: null });
  return 'sent';
}
