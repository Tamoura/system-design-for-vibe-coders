import { randomUUID } from 'node:crypto';
import { eq, inArray, sql } from 'drizzle-orm';
import { db, schema } from '@/db';
import { renderEmail, TEMPLATES, type TemplateName, type TemplateProps } from '@/emails';
import { enqueueInTx } from '../queue';
import type { JobContext } from '../queue/queues';
import { getEmailTransport } from './transport';

const { emailOutbox, emailSuppressions } = schema;

/*
 * Lesson 4.1: transactional email.
 *
 *   sendEmail()  ──► email_outbox (a row) + an `email.send` job, in ONE transaction
 *                        │  the worker (lesson 5.1, npm run worker): sendQueuedEmail()
 *                        ▼
 *                  deliverEmail(): suppressed? ─► render template ─► transport (SMTP / Resend)
 *                        │ fails? the queue retries with backoff (8 attempts), then "failed"
 *                        ▼
 *                  provider ──webhook──► bounce / complaint ─► email_suppressions
 */

export type EmailRequest<N extends TemplateName> = {
  to: string;
  template: N;
  props: TemplateProps<N>;
  /**
   * Identifies the JOB: the same key twice queues one email. Give one when a
   * repeated call must not send twice (an invitation: its id and token);
   * leave it out for "send one more" (a verification email resent on request).
   */
  idempotencyKey?: string;
  /** One-click unsubscribe endpoint (RFC 8058) for optional or subscribed mail. */
  listUnsubscribe?: string;
};

/**
 * Lesson 4.1 (🟡): queue an email. Nothing is sent inside the caller's
 * request, so a slow or broken provider can never make sign-up or an
 * invitation fail; the email goes out a moment later, or after recovery.
 */
export async function sendEmail<N extends TemplateName>(request: EmailRequest<N>): Promise<{ queued: boolean }> {
  // Lesson 5.1 (🟡): the row and its job commit together. Before Module 5 a
  // worker was nudged "after the response"; a crash in between left the row
  // for cron to find. Now the job cannot be lost: it IS a row, in this transaction.
  // (email_outbox is not a tenant table: verification mail has no org.)
  return db.transaction(async (tx) => {
    const inserted = await tx
      .insert(emailOutbox)
      .values({
        idempotencyKey: request.idempotencyKey ?? `${request.template}:${randomUUID()}`,
        to: request.to.trim(),
        template: request.template,
        props: request.props,
        listUnsubscribe: request.listUnsubscribe ?? null,
      })
      .onConflictDoNothing({ target: emailOutbox.idempotencyKey })
      .returning({ id: emailOutbox.id });
    // The job's key is the row: queuing the same email twice adds one job.
    for (const row of inserted) await enqueueInTx(tx, 'email.send', { emailId: row.id }, { key: row.id });
    return { queued: inserted.length > 0 };
  });
}

/** Where mail comes from, per stream (lesson 4.1: separate transactional and subscriber mail). */
function fromAddress(stream: 'transactional' | 'status'): string {
  return stream === 'status'
    ? (process.env.EMAIL_FROM_STATUS ?? 'Beacon Status <status@updates.beacon.app>')
    : (process.env.EMAIL_FROM ?? 'Beacon <notifications@mail.beacon.app>');
}

export type EmailMessage<N extends TemplateName = TemplateName> = {
  to: string;
  template: N;
  props: TemplateProps<N>;
  idempotencyKey: string;
  listUnsubscribe?: string | null;
};

export type DeliveryResult = { status: 'sent'; providerMessageId: string } | { status: 'suppressed'; reason: string };

/**
 * Send one email now: the step both queues share (this outbox, and the
 * email channel of notifications in lesson 4.2). Checks the suppression list
 * first, renders HTML + plain text, adds the unsubscribe headers, and hands
 * the message to the transport. Throws if the provider did not accept it,
 * so the caller can retry.
 */
export async function deliverEmail(message: EmailMessage): Promise<DeliveryResult> {
  const suppression = await findSuppression(message.to);
  // A hard bounce stops everything. A complaint stops everything except the
  // essential account emails (you still get the password reset you asked for).
  if (suppression && (suppression.reason !== 'complaint' || !TEMPLATES[message.template].essential)) {
    return { status: 'suppressed', reason: suppression.reason };
  }
  const rendered = await renderEmail(message.template, message.props);
  const headers: Record<string, string> = {};
  if (message.listUnsubscribe) {
    // RFC 8058 one-click unsubscribe: Gmail and Yahoo show an "Unsubscribe"
    // button and POST "List-Unsubscribe=One-Click" to this URL.
    headers['List-Unsubscribe'] = `<${message.listUnsubscribe}>`;
    headers['List-Unsubscribe-Post'] = 'List-Unsubscribe=One-Click';
  }
  const transport = await getEmailTransport();
  const { messageId } = await transport.send({
    from: fromAddress(rendered.stream),
    to: message.to,
    subject: rendered.subject,
    html: rendered.html,
    text: rendered.text,
    headers,
    idempotencyKey: message.idempotencyKey,
  });
  return { status: 'sent', providerMessageId: messageId };
}

/**
 * Lesson 5.1: the `email.send` job. Idempotent: an email that is no longer
 * pending (sent, suppressed, failed, or gone) is left alone, so running the
 * job twice sends once. If two copies race (at-least-once delivery), the
 * provider drops the second: the idempotency key goes with the message.
 *
 * A failure throws, and the QUEUE retries it with backoff; the row only
 * records what happened, for people and for the members page.
 */
export async function sendQueuedEmail(emailId: string, job: Pick<JobContext, 'attempt' | 'lastAttempt'> = { attempt: 1, lastAttempt: false }) {
  const [row] = await db.select().from(emailOutbox).where(eq(emailOutbox.id, emailId));
  if (!row || row.status !== 'pending') return { status: row?.status ?? 'missing', skipped: true };
  try {
    const result = await deliverEmail({ ...row, template: row.template as TemplateName, props: row.props as TemplateProps<TemplateName> });
    if (result.status === 'sent') {
      await db
        .update(emailOutbox)
        .set({ status: 'sent', attempts: job.attempt, sentAt: new Date(), providerMessageId: result.providerMessageId, lastError: null })
        .where(eq(emailOutbox.id, row.id));
    } else {
      await db.update(emailOutbox).set({ status: 'suppressed', attempts: job.attempt, lastError: `suppressed: ${result.reason}` }).where(eq(emailOutbox.id, row.id));
    }
    return { status: result.status };
  } catch (err) {
    await db
      .update(emailOutbox)
      .set({ status: job.lastAttempt ? 'failed' : 'pending', attempts: job.attempt, lastError: (err as Error).message.slice(0, 500) })
      .where(eq(emailOutbox.id, row.id));
    throw err; // the queue retries, or dead-letters it after the last attempt
  }
}

/** Pending emails (for the worker's start-up check, see src/lib/queue/worker.ts). */
export async function listPendingEmailIds(): Promise<string[]> {
  const rows = await db.select({ id: emailOutbox.id }).from(emailOutbox).where(eq(emailOutbox.status, 'pending'));
  return rows.map((r) => r.id);
}

/*
 * Lesson 4.1 (🟡): the suppression list. Addresses are compared lower-cased.
 */
const normalize = (email: string) => email.trim().toLowerCase();

export async function findSuppression(email: string) {
  const [row] = await db.select().from(emailSuppressions).where(eq(emailSuppressions.email, normalize(email))).limit(1);
  return row ?? null;
}

/** Record a bounce or complaint. A hard bounce overrides a complaint (it is the stronger reason). */
export async function suppressEmail(email: string, reason: 'hard_bounce' | 'complaint' | 'manual', detail?: string) {
  await db
    .insert(emailSuppressions)
    .values({ email: normalize(email), reason, detail: detail?.slice(0, 500) ?? null })
    .onConflictDoUpdate({
      target: emailSuppressions.email,
      set: { reason, detail: detail?.slice(0, 500) ?? null },
      setWhere: reason === 'hard_bounce' ? sql`true` : sql`false`,
    });
}

/** For the members page: which of these addresses we cannot email, and why. */
export async function listSuppressions(emails: string[]): Promise<Map<string, 'hard_bounce' | 'complaint' | 'manual'>> {
  if (emails.length === 0) return new Map();
  const rows = await db.select().from(emailSuppressions).where(inArray(emailSuppressions.email, emails.map(normalize)));
  return new Map(rows.map((r) => [r.email, r.reason]));
}
