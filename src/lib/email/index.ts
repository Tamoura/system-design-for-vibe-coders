import { randomUUID } from 'node:crypto';
import { and, eq, inArray, lte, sql } from 'drizzle-orm';
import { db, schema } from '@/db';
import { renderEmail, TEMPLATES, type TemplateName, type TemplateProps } from '@/emails';
import { MAX_ATTEMPTS, retryDelayMs } from '@/core/retry';
import { runAfterResponse } from '../jobs';
import { getEmailTransport } from './transport';

const { emailOutbox, emailSuppressions } = schema;

/*
 * Lesson 4.1: transactional email.
 *
 *   sendEmail()  ──► email_outbox (a row; the request returns at once)
 *                        │  after the response, and from cron: deliverPendingEmails()
 *                        ▼
 *                  deliverEmail(): suppressed? ─► render template ─► transport (SMTP / Resend)
 *                        │ fails? retry with backoff (30 s, 2 min, 8 min …), MAX_ATTEMPTS, then "failed"
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
  const inserted = await db
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
  runAfterResponse(() => deliverPendingEmails());
  return { queued: inserted.length > 0 };
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

/** How long a worker "owns" the rows it claimed. A crashed worker's rows are due again after this. */
const LEASE_MS = 5 * 60_000;

/**
 * Lesson 4.1 (🟡): the email worker. Claims due rows (FOR UPDATE SKIP LOCKED,
 * so two workers never take the same row), sends each, and records the
 * outcome. Called after every sendEmail() and by `npm run messages:send`.
 */
export async function deliverPendingEmails(opts: { limit?: number } = {}) {
  const counts = { sent: 0, suppressed: 0, retrying: 0, failed: 0 };
  const due = db
    .select({ id: emailOutbox.id })
    .from(emailOutbox)
    .where(and(eq(emailOutbox.status, 'pending'), lte(emailOutbox.nextAttemptAt, new Date())))
    .orderBy(emailOutbox.createdAt)
    .limit(opts.limit ?? 50)
    .for('update', { skipLocked: true });
  const claimed = await db
    .update(emailOutbox)
    .set({ attempts: sql`${emailOutbox.attempts} + 1`, nextAttemptAt: new Date(Date.now() + LEASE_MS) })
    .where(inArray(emailOutbox.id, due))
    .returning();

  for (const row of claimed) {
    try {
      const result = await deliverEmail({ ...row, template: row.template as TemplateName, props: row.props as TemplateProps<TemplateName> });
      if (result.status === 'sent') {
        await db.update(emailOutbox).set({ status: 'sent', sentAt: new Date(), providerMessageId: result.providerMessageId, lastError: null }).where(eq(emailOutbox.id, row.id));
        counts.sent++;
      } else {
        await db.update(emailOutbox).set({ status: 'suppressed', lastError: `suppressed: ${result.reason}` }).where(eq(emailOutbox.id, row.id));
        counts.suppressed++;
      }
    } catch (err) {
      const giveUp = row.attempts >= MAX_ATTEMPTS;
      await db
        .update(emailOutbox)
        .set({
          status: giveUp ? 'failed' : 'pending',
          nextAttemptAt: new Date(Date.now() + retryDelayMs(row.attempts)),
          lastError: (err as Error).message.slice(0, 500),
        })
        .where(eq(emailOutbox.id, row.id));
      if (giveUp) counts.failed++;
      else counts.retrying++;
    }
  }
  return counts;
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
