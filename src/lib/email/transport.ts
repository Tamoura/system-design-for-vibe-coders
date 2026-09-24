import { createHash } from 'node:crypto';

/*
 * Lesson 4.1 (🟢): one interface in front of every way of sending mail.
 * sendEmail() (./index.ts) is the only caller, and the drivers below are the
 * only files that know about nodemailer or the provider's HTTP API. Nothing
 * else in Beacon imports them (tests/email.test.ts checks).
 *
 *   smtp     nodemailer over SMTP. In development: Mailpit on localhost:1025
 *            (docker compose), inbox at http://localhost:8025. Also works in
 *            production with a provider's SMTP endpoint (Postmark, SES).
 *   resend   Resend's HTTP API, the production default when RESEND_API_KEY is set.
 *   console  prints the plain-text part: for a laptop without Mailpit.
 *   memory   keeps messages in an array: for tests.
 */
export type OutgoingEmail = {
  from: string;
  to: string;
  subject: string;
  html: string;
  text: string;
  headers: Record<string, string>;
  /** Same job, same key: the provider drops the second send. */
  idempotencyKey: string;
};

export interface EmailTransport {
  readonly name: string;
  /** Resolves once the provider has ACCEPTED the message; throws if it did not. */
  send(email: OutgoingEmail): Promise<{ messageId: string }>;
}

/** A stable Message-ID for a job, so a message retried over SMTP can be recognised as the same one. */
export function messageIdFor(idempotencyKey: string, domain = 'beacon.local'): string {
  return `<${createHash('sha256').update(idempotencyKey).digest('hex').slice(0, 32)}@${domain}>`;
}

let override: EmailTransport | null = null;
let cached: EmailTransport | null = null;

export function setEmailTransportForTests(transport: EmailTransport | null) {
  override = transport;
}

export async function getEmailTransport(): Promise<EmailTransport> {
  if (override) return override;
  if (cached) return cached;
  const driver = process.env.EMAIL_DRIVER ?? (process.env.RESEND_API_KEY ? 'resend' : 'smtp');
  switch (driver) {
    case 'smtp':
      cached = (await import('./smtp')).createSmtpTransport(process.env.SMTP_URL ?? 'smtp://localhost:1025');
      break;
    case 'resend':
      cached = (await import('./resend')).createResendTransport(process.env.RESEND_API_KEY ?? '');
      break;
    case 'console':
      cached = consoleTransport;
      break;
    case 'memory':
      cached = (await import('./memory')).memoryTransport;
      break;
    default:
      throw new Error(`Unknown EMAIL_DRIVER "${driver}" (use smtp, resend, console or memory)`);
  }
  return cached;
}

/** The old console "mailer" from before 4.1, kept as a driver: EMAIL_DRIVER=console. */
const consoleTransport: EmailTransport = {
  name: 'console',
  async send(email) {
    console.log(`\n[email] to=${email.to} subject="${email.subject}"\n${email.text}\n[/email]\n`);
    return { messageId: messageIdFor(email.idempotencyKey) };
  },
};
