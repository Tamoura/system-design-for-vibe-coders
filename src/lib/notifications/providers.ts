import { createHash } from 'node:crypto';
import { smsSegments } from '@/core/notifications';

/*
 * Lesson 4.2: "rent the channels, own the decisions". Each external channel
 * is a small interface; the pipeline (./index.ts, ./deliver.ts) never talks
 * to Twilio or Slack directly, so adding a provider or failing over to a
 * second one touches only this file.
 *
 *   SMS    twilio (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM)
 *          fake   (SMS_PROVIDER=fake: development, tests, the smoke test)
 *   Slack  webhook (the org's incoming-webhook URL)
 *          fake    (SLACK_PROVIDER=fake: nothing leaves the machine)
 *
 * The real drivers were typechecked but not run against Twilio or Slack here
 * (no internet in the course's build environment).
 */

export type SmsReceipt = { sid: string; segments: number; sentAt: Date };

export interface SmsProvider {
  readonly name: string;
  /** Resolves once the provider ACCEPTED the message (the moment it becomes billable, lesson 3.3). */
  send(message: { to: string; body: string; idempotencyKey: string }): Promise<SmsReceipt>;
}

export interface SlackSender {
  readonly name: string;
  post(webhookUrl: string, message: { text: string }): Promise<{ id: string }>;
}

/** In-memory SMS "provider". The message SID is derived from the job's key, so a retried job gets the same SID. */
class FakeSms implements SmsProvider {
  readonly name = 'fake';
  readonly sent: { to: string; body: string; sid: string }[] = [];
  outage = false;
  async send({ to, body, idempotencyKey }: { to: string; body: string; idempotencyKey: string }) {
    if (this.outage) throw new Error('SMS provider unavailable (simulated outage)');
    const sid = `SMfake${createHash('sha256').update(idempotencyKey).digest('hex').slice(0, 26)}`;
    this.sent.push({ to, body, sid });
    if (process.env.NODE_ENV !== 'test') console.log(`[sms] to=${to} sid=${sid} ${body}`);
    return { sid, segments: smsSegments(body), sentAt: new Date() };
  }
}

class FakeSlack implements SlackSender {
  readonly name = 'fake';
  readonly posts: { webhookUrl: string; text: string }[] = [];
  async post(webhookUrl: string, { text }: { text: string }) {
    this.posts.push({ webhookUrl, text });
    if (process.env.NODE_ENV !== 'test') console.log(`[slack] ${text.replace(/\n/g, ' / ')}`);
    return { id: `slack_fake_${this.posts.length}` };
  }
}

export const fakeSms = new FakeSms();
export const fakeSlack = new FakeSlack();

/** Twilio's Messages API: one form-encoded POST. */
function twilioSms(accountSid: string, authToken: string, from: string): SmsProvider {
  return {
    name: 'twilio',
    async send({ to, body }) {
      const res = await fetch(`https://api.twilio.com/2010-04-01/Accounts/${accountSid}/Messages.json`, {
        method: 'POST',
        headers: { authorization: `Basic ${Buffer.from(`${accountSid}:${authToken}`).toString('base64')}` },
        body: new URLSearchParams({ To: to, From: from, Body: body }),
      });
      if (!res.ok) throw new Error(`Twilio answered ${res.status}: ${(await res.text()).slice(0, 200)}`);
      const msg = (await res.json()) as { sid: string; num_segments: string; date_created: string };
      return { sid: msg.sid, segments: Number(msg.num_segments) || smsSegments(body), sentAt: new Date(msg.date_created) };
    },
  };
}

/** Slack incoming webhooks answer "ok" and no message id. */
const slackWebhook: SlackSender = {
  name: 'webhook',
  async post(webhookUrl, message) {
    const res = await fetch(webhookUrl, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(message) });
    if (!res.ok) throw new Error(`Slack answered ${res.status}: ${(await res.text()).slice(0, 200)}`);
    return { id: `slack:${res.headers.get('x-slack-req-id') ?? 'webhook'}` };
  },
};

/** null when no SMS provider is configured: SMS deliveries are then "skipped", visibly, in the delivery log. */
export function getSmsProvider(): SmsProvider | null {
  if (process.env.SMS_PROVIDER === 'fake') return fakeSms;
  const { TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM } = process.env;
  if (TWILIO_ACCOUNT_SID && TWILIO_AUTH_TOKEN && TWILIO_FROM) return twilioSms(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM);
  return null;
}

export function getSlackSender(): SlackSender {
  return process.env.SLACK_PROVIDER === 'fake' ? fakeSlack : slackWebhook;
}

/**
 * Only Slack's own webhook host. The URL is typed in by an admin and Beacon's
 * server POSTs to it, so accepting any URL would let someone make Beacon call
 * internal addresses (server-side request forgery).
 */
export function isSlackWebhookUrl(value: string): boolean {
  try {
    const u = new URL(value);
    return u.protocol === 'https:' && u.hostname === 'hooks.slack.com' && u.pathname.startsWith('/services/');
  } catch {
    return false;
  }
}
