import { readdirSync, readFileSync, statSync } from 'node:fs';
import type { AddressInfo } from 'node:net';
import path from 'node:path';
import { afterAll, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));

import { eq } from 'drizzle-orm';
import { simpleParser, type ParsedMail } from 'mailparser';
import { SMTPServer } from 'smtp-server';
import { db, schema } from '@/db';
import { renderEmail, TEMPLATES, type TemplateName } from '@/emails';
import { MAX_ATTEMPTS, retryDelayMs } from '@/core/retry';
import { deliverEmail, deliverPendingEmails, findSuppression, listSuppressions, sendEmail, suppressEmail } from '@/lib/email';
import { memoryTransport } from '@/lib/email/memory';
import { createSmtpTransport } from '@/lib/email/smtp';
import { setEmailTransportForTests } from '@/lib/email/transport';
import { signWebhookForTests, verifyWebhookSignature } from '@/lib/email/webhook';
import { POST as webhook } from '@/app/api/email/webhook/route';

/*
 * Lesson 4.1: templates, the queue, suppression, the bounce webhook, and the
 * SMTP driver against a real (local) SMTP server.
 */
const { emailOutbox } = schema;
const SECRET = `whsec_${Buffer.from('beacon-test-webhook-secret').toString('base64')}`;

beforeEach(() => {
  memoryTransport.reset();
  setEmailTransportForTests(memoryTransport);
});

async function outboxRow(to: string) {
  const [row] = await db.select().from(emailOutbox).where(eq(emailOutbox.to, to));
  return row;
}

/** Make every pending row due now, as if the backoff had passed. */
async function timePasses() {
  await db.update(emailOutbox).set({ nextAttemptAt: new Date(Date.now() - 1000) }).where(eq(emailOutbox.status, 'pending'));
}

describe('templates (🟢)', () => {
  for (const name of Object.keys(TEMPLATES) as TemplateName[]) {
    it(`${name} renders a subject, HTML and a plain-text part that carries the link`, async () => {
      const sample = TEMPLATES[name].sample as { url: string };
      const email = await renderEmail(name, TEMPLATES[name].sample);
      expect(email.subject.length).toBeGreaterThan(5);
      expect(email.html).toMatch(/^<!DOCTYPE html/);
      expect(email.html).toContain(sample.url);
      expect(email.text).toContain(sample.url);
      expect(email.text).not.toMatch(/<[a-z]/i); // really plain text
    });
  }

  it('optional and subscribed mail shows an unsubscribe link; account and billing mail does not', async () => {
    expect((await renderEmail('incident-opened', TEMPLATES['incident-opened'].sample)).text).toContain('Unsubscribe');
    expect((await renderEmail('status-update', TEMPLATES['status-update'].sample)).text).toContain('Unsubscribe');
    expect((await renderEmail('reset-password', TEMPLATES['reset-password'].sample)).text).not.toContain('Unsubscribe');
    expect((await renderEmail('plan-downgraded', TEMPLATES['plan-downgraded'].sample)).text).not.toContain('Unsubscribe');
  });
});

describe('the queue (🟡)', () => {
  it('sendEmail only queues; the worker sends it, with HTML, text and the stream’s From', async () => {
    await sendEmail({ to: 'ada@example.test', template: 'verify-email', props: { name: 'Ada', url: 'https://beacon.test/v?t=1' } });
    expect(memoryTransport.messages).toHaveLength(0); // nothing sent inside the "request"
    expect((await outboxRow('ada@example.test')).status).toBe('pending');

    expect(await deliverPendingEmails()).toMatchObject({ sent: 1 });
    const [sent] = memoryTransport.to('ada@example.test');
    expect(sent.subject).toBe('Confirm your email for Beacon');
    expect(sent.from).toContain('mail.beacon.app');
    expect(sent.html).toContain('https://beacon.test/v?t=1');
    expect(sent.text).toContain('https://beacon.test/v?t=1');
    const row = await outboxRow('ada@example.test');
    expect(row.status).toBe('sent');
    expect(row.providerMessageId).toMatch(/^<.+@.+>$/);
  });

  it('status-page mail goes out from the separate status stream', async () => {
    await sendEmail({ to: 'sub@example.test', template: 'confirm-subscription', props: { orgName: 'Acme', url: 'https://beacon.test/c' } });
    await deliverPendingEmails();
    expect(memoryTransport.to('sub@example.test')[0].from).toContain('updates.beacon.app');
  });

  it('the same idempotency key queues one email, however often it is asked for', async () => {
    const request = { to: 'once@example.test', template: 'invitation' as const, props: TEMPLATES.invitation.sample, idempotencyKey: 'invitation:1:abc' };
    expect(await sendEmail(request)).toEqual({ queued: true });
    expect(await sendEmail(request)).toEqual({ queued: false });
    await deliverPendingEmails();
    await deliverPendingEmails();
    expect(memoryTransport.to('once@example.test')).toHaveLength(1);
    expect(memoryTransport.to('once@example.test')[0].idempotencyKey).toBe('invitation:1:abc'); // passed on to the provider
  });

  it('a provider outage delays the email without failing the request, and it goes out after recovery', async () => {
    memoryTransport.outage = true; // like a bad API key
    await expect(sendEmail({ to: 'outage@example.test', template: 'reset-password', props: { name: 'O', url: 'https://beacon.test/r' } })).resolves.toEqual({ queued: true });
    expect(await deliverPendingEmails()).toMatchObject({ sent: 0, retrying: 1 });
    let row = await outboxRow('outage@example.test');
    expect(row.status).toBe('pending');
    expect(row.lastError).toContain('unavailable');
    expect(row.nextAttemptAt.getTime()).toBeGreaterThan(Date.now() + 20_000); // backoff: not retried at once
    expect(await deliverPendingEmails()).toMatchObject({ retrying: 0 }); // not due yet

    memoryTransport.outage = false; // the provider is back
    await timePasses();
    expect(await deliverPendingEmails()).toMatchObject({ sent: 1 });
    row = await outboxRow('outage@example.test');
    expect(row.status).toBe('sent');
    expect(row.attempts).toBe(2);
  });

  it(`gives up after ${MAX_ATTEMPTS} attempts and marks the email failed`, async () => {
    memoryTransport.outage = true;
    await sendEmail({ to: 'never@example.test', template: 'verify-email', props: { name: 'N', url: 'https://beacon.test/v' } });
    for (let i = 0; i < MAX_ATTEMPTS; i++) {
      await timePasses();
      await deliverPendingEmails();
    }
    expect((await outboxRow('never@example.test')).status).toBe('failed');
  });

  it('backs off exponentially, capped at six hours', () => {
    expect(retryDelayMs(1)).toBe(30_000);
    expect(retryDelayMs(2)).toBe(120_000);
    expect(retryDelayMs(3)).toBe(480_000);
    expect(retryDelayMs(20)).toBe(6 * 3600_000);
  });

  it('a claimed row is not sent twice by two workers running at once', async () => {
    for (let i = 0; i < 5; i++) await sendEmail({ to: `race${i}@example.test`, template: 'verify-email', props: { name: 'R', url: 'https://beacon.test/v' } });
    await Promise.all([deliverPendingEmails(), deliverPendingEmails()]);
    expect(memoryTransport.messages.filter((m) => m.to.startsWith('race'))).toHaveLength(5);
  });
});

describe('suppression list (🟡)', () => {
  const hardBounce = (to: string) => ({ type: 'email.bounced', created_at: new Date().toISOString(), data: { email_id: 'e1', to: [to], bounce: { type: 'Permanent', subType: 'Suppressed', message: 'mailbox does not exist' } } });
  const post = (body: string, headers: Record<string, string>) => webhook(new Request('http://test/api/email/webhook', { method: 'POST', body, headers }));

  beforeAll(() => vi.stubEnv('EMAIL_WEBHOOK_SECRET', SECRET));
  afterAll(() => vi.unstubAllEnvs());

  it('a signed hard-bounce webhook adds a suppression row, and no further email is attempted to that address', async () => {
    const body = JSON.stringify(hardBounce('Bounced@Example.test'));
    const res = await post(body, signWebhookForTests(body, SECRET));
    expect(res.status).toBe(200);
    expect(await findSuppression('bounced@example.test')).toMatchObject({ reason: 'hard_bounce' });

    await sendEmail({ to: 'bounced@example.test', template: 'invitation', props: TEMPLATES.invitation.sample });
    await sendEmail({ to: 'bounced@example.test', template: 'reset-password', props: TEMPLATES['reset-password'].sample }); // not even essential mail
    expect(await deliverPendingEmails()).toMatchObject({ sent: 0, suppressed: 2 });
    expect(memoryTransport.to('bounced@example.test')).toHaveLength(0);
  });

  it('a complaint stops optional mail but not the password reset the person asks for', async () => {
    const body = JSON.stringify({ type: 'email.complained', data: { to: ['grumpy@example.test'] } });
    expect((await post(body, signWebhookForTests(body, SECRET))).status).toBe(200);
    expect(await deliverEmail({ to: 'grumpy@example.test', template: 'incident-opened', props: TEMPLATES['incident-opened'].sample, idempotencyKey: 'k1' })).toEqual({ status: 'suppressed', reason: 'complaint' });
    expect(await deliverEmail({ to: 'grumpy@example.test', template: 'reset-password', props: TEMPLATES['reset-password'].sample, idempotencyKey: 'k2' })).toMatchObject({ status: 'sent' });
  });

  it('a later hard bounce upgrades a complaint; a complaint never downgrades a hard bounce', async () => {
    await suppressEmail('both@example.test', 'complaint');
    await suppressEmail('both@example.test', 'hard_bounce');
    await suppressEmail('both@example.test', 'complaint');
    expect((await findSuppression('both@example.test'))?.reason).toBe('hard_bounce');
  });

  it('a soft bounce is the provider’s to retry: no suppression', async () => {
    const body = JSON.stringify({ type: 'email.bounced', data: { to: ['full@example.test'], bounce: { type: 'Transient', message: 'mailbox full' } } });
    const warn = vi.spyOn(console, 'warn').mockImplementation(() => {});
    expect((await post(body, signWebhookForTests(body, SECRET))).status).toBe(200);
    warn.mockRestore();
    expect(await findSuppression('full@example.test')).toBeNull();
  });

  it('forged, tampered, stale and unsigned webhooks are rejected with 400 and change nothing', async () => {
    const body = JSON.stringify(hardBounce('victim@example.test'));
    const signed = signWebhookForTests(body, SECRET);
    expect((await post(body.replace('victim', 'other'), signed)).status).toBe(400); // tampered body
    expect((await post(body, signWebhookForTests(body, `whsec_${Buffer.from('wrong').toString('base64')}`))).status).toBe(400); // wrong secret
    const stale = signWebhookForTests(body, SECRET, 'msg_old', Math.floor(Date.now() / 1000) - 3600);
    expect((await post(body, stale)).status).toBe(400); // a replay from an hour ago
    expect((await post(body, {})).status).toBe(400); // unsigned
    expect(await findSuppression('victim@example.test')).toBeNull();
  });

  it('accepts any of several signatures (secret rotation)', () => {
    const body = '{}';
    const good = signWebhookForTests(body, SECRET, 'msg_1', 1_700_000_000);
    const headers = { id: 'msg_1', timestamp: '1700000000', signature: `v1,bm90LWl0 ${good['svix-signature']}` };
    expect(verifyWebhookSignature(body, headers, SECRET, 1_700_000_000_000)).toBe(true);
  });

  it('lists suppressed addresses for the members page, case-insensitively', async () => {
    const found = await listSuppressions(['BOUNCED@example.test', 'nobody@example.test']);
    expect([...found]).toEqual([['bounced@example.test', 'hard_bounce']]);
  });

  it('answers 503 when no webhook secret is configured (never trusts an unsigned request)', async () => {
    vi.stubEnv('EMAIL_WEBHOOK_SECRET', '');
    expect((await post('{}', {})).status).toBe(503);
    vi.stubEnv('EMAIL_WEBHOOK_SECRET', SECRET);
  });
});

describe('SMTP driver against a local SMTP server (what Mailpit does in development)', () => {
  let server: SMTPServer;
  let port: number;
  const received: ParsedMail[] = [];

  beforeAll(async () => {
    server = new SMTPServer({
      authOptional: true,
      disabledCommands: ['STARTTLS'],
      logger: false,
      onData(stream, _session, callback) {
        simpleParser(stream).then((mail) => {
          received.push(mail);
          callback();
        }, callback);
      },
    });
    await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', resolve));
    port = (server.server.address() as AddressInfo).port;
  });
  afterAll(() => new Promise<void>((resolve) => server.close(() => resolve())));

  it('sends multipart/alternative (text + HTML) with the one-click unsubscribe headers and a stable Message-ID', async () => {
    setEmailTransportForTests(createSmtpTransport(`smtp://127.0.0.1:${port}`));
    const message = { to: 'smtp@example.test', template: 'status-update' as const, props: TEMPLATES['status-update'].sample, idempotencyKey: 'delivery:42', listUnsubscribe: 'https://beacon.test/api/unsubscribe?token=abc' };
    const result = await deliverEmail(message);
    expect(result.status).toBe('sent');
    const mail = received.at(-1)!;
    expect(mail.subject).toBe('[Acme status] Checkout: investigating');
    expect(mail.text).toContain('View status page');
    expect(mail.html).toContain('<html');
    const raw = (name: string) => mail.headerLines.find((h) => h.key === name)?.line;
    expect(raw('list-unsubscribe')).toBe('List-Unsubscribe: <https://beacon.test/api/unsubscribe?token=abc>');
    expect(raw('list-unsubscribe-post')).toBe('List-Unsubscribe-Post: List-Unsubscribe=One-Click');

    await deliverEmail(message); // a retry of the same job
    expect(received.at(-1)!.messageId).toBe(mail.messageId);
  });
});

describe('lint: only the email drivers know the provider (🟢)', () => {
  function files(dir: string): string[] {
    return readdirSync(dir).flatMap((f) => {
      const p = path.join(dir, f);
      return statSync(p).isDirectory() ? files(p) : /\.(ts|tsx)$/.test(p) ? [p] : [];
    });
  }

  it('nobody outside src/lib/email imports nodemailer or calls the Resend API', () => {
    const offenders = [...files('src'), ...files('scripts')].filter((f) => {
      if (f.split(path.sep).join('/').startsWith('src/lib/email/')) return false;
      const text = readFileSync(f, 'utf8');
      return /from ['"]nodemailer['"]|api\.resend\.com/.test(text);
    });
    expect(offenders).toEqual([]);
  });
});
