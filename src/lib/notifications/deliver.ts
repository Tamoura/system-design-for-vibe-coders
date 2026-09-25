import { and, count, eq, gt } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import { SMS_PER_HOUR, smsText } from '@/core/notifications';
import type { TemplateName, TemplateProps } from '@/emails';
import { deliverEmail } from '../email';
import type { JobContext } from '../queue/queues';
import { isEnabled } from '../flags';
import { recordSmsSent } from '../usage';
import { enqueueDeliveries, type DeliveryPayload } from './pipeline';
import { getSlackSender, getSmsProvider } from './providers';
import { readSlackWebhookUrl } from './slack';

const { organizations, notificationDeliveries, users } = schema;
type Delivery = typeof notificationDeliveries.$inferSelect & { payload: DeliveryPayload };
type Outcome = 'sent' | 'suppressed' | 'throttled' | 'skipped';

const HOUR_MS = 60 * 60 * 1000;

/**
 * Lesson 4.2 (🟡) + 5.1: the channel worker, as the `notification.deliver`
 * job. One job per delivery row (enqueued by notifyInTx in the transaction
 * that wrote the row). The row stays the delivery log: channel, status,
 * provider message id, error, attempts.
 *
 * Idempotent (lesson 5.1): a delivery that is no longer "pending" was already
 * handled, so a job that runs twice (at-least-once delivery) or a job enqueued
 * twice sends once. The provider gets an idempotency key derived from the
 * delivery too, for the crash between "sent" and "marked sent".
 *
 * A provider failure THROWS: the queue retries with backoff (8 attempts, see
 * src/lib/queue/queues.ts) and dead-letters the job after the last one. On
 * the last attempt the row is marked "failed", so the log says so.
 *
 * Per org, inside withOrg(), like every tenant job (lesson 2.4). The network
 * call happens outside any transaction.
 */
export async function deliverNotification(
  orgId: string,
  deliveryId: string,
  job: Pick<JobContext, 'attempt' | 'lastAttempt'> = { attempt: 1, lastAttempt: false },
): Promise<Outcome | 'already-done'> {
  const [row] = await withOrg(orgId, (tx) =>
    tx
      .select()
      .from(notificationDeliveries)
      .where(and(eq(notificationDeliveries.organizationId, orgId), eq(notificationDeliveries.id, deliveryId))),
  );
  if (!row || row.status !== 'pending') return 'already-done'; // gone, or handled by an earlier run
  const d = row as Delivery;
  await record(d, { attempts: job.attempt });
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
    // The provider refused or is down. Record it, then let the queue retry.
    await record(d, { status: job.lastAttempt ? 'failed' : 'pending', error: (err as Error).message.slice(0, 500) });
    throw err;
  }
}

/** Pending deliveries of one org (for the worker's start-up check, src/lib/queue/worker.ts). */
export async function listPendingDeliveryIds(orgId: string): Promise<string[]> {
  const rows = await withOrg(orgId, (tx) =>
    tx
      .select({ id: notificationDeliveries.id })
      .from(notificationDeliveries)
      .where(and(eq(notificationDeliveries.organizationId, orgId), eq(notificationDeliveries.status, 'pending'))),
  );
  return rows.map((r) => r.id);
}

type Patch = Partial<Pick<Delivery, 'status' | 'providerMessageId' | 'error' | 'sentAt' | 'attempts'>>;

async function record(d: Delivery, patch: Patch) {
  await withOrg(d.organizationId, (tx) =>
    tx
      .update(notificationDeliveries)
      .set(patch)
      .where(and(eq(notificationDeliveries.organizationId, d.organizationId), eq(notificationDeliveries.id, d.id))),
  );
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
  // Lesson 6.3 (🟡): the ops kill switch. On-call flips `disable-sms-sending`
  // in /internal/flags (for everyone, or for one org) and every worker stops
  // sending SMS within one flag refresh interval, with no deploy. The delivery
  // is logged as skipped; the email, Slack and in-app messages of the same
  // alert are separate deliveries and still go out.
  if (await isEnabled('disable-sms-sending', { id: d.organizationId })) {
    await record(d, { status: 'skipped', error: 'SMS sending is switched off by an operator (flag disable-sms-sending)' });
    return 'skipped';
  }
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

  // The key names the event, the person and the channel (the delivery's
  // dedupe key): a retried job, or a re-run workflow step (lesson 5.4), never
  // pages twice.
  const receipt = await provider.send({ to: d.recipient, body: smsText(d.payload.title, d.payload.url), idempotencyKey: d.dedupeKey });
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
    const inserted = await tx
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
      .onConflictDoNothing({ target: notificationDeliveries.dedupeKey })
      .returning({ id: notificationDeliveries.id, status: notificationDeliveries.status });
    await enqueueDeliveries(tx, d.organizationId, inserted); // a job of its own, in the same transaction
  });
}

/** Slack: the org's incoming webhook, looked up at send time (it may have changed or been removed). */
async function sendSlackDelivery(d: Delivery): Promise<Outcome> {
  const slackUrl = await readSlackWebhookUrl(d.organizationId); // lesson 8.1: decrypted only to post
  if (!slackUrl) {
    await record(d, { status: 'skipped', error: 'no Slack webhook configured' });
    return 'skipped';
  }
  const { title, body, url } = d.payload;
  const { id } = await getSlackSender().post(slackUrl, { text: `*${title}*\n${body}\n<${url}|Open in Beacon>` });
  await record(d, { status: 'sent', providerMessageId: id, sentAt: new Date(), error: null });
  return 'sent';
}
