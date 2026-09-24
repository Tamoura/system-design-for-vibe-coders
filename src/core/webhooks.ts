import { createHmac, randomBytes } from 'node:crypto';

/*
 * Lesson 5.3 (🟢): outbound webhooks, the pure parts. Beacon signs every
 * delivery the Standard Webhooks way (standardwebhooks.com), so a customer
 * verifies it with the official library for their language in one line:
 *
 *   new Webhook(secret).verify(body, headers)   // throws if forged, altered or too old
 *
 * Each request carries three headers:
 *
 *   webhook-id         msg_…  the message id: the SAME on every retry, so the
 *                      receiver can drop duplicates (delivery is at-least-once)
 *   webhook-timestamp  Unix seconds: the receiver refuses old ones (replays)
 *   webhook-signature  "v1," + base64(HMAC-SHA256(secret, `${id}.${timestamp}.${body}`))
 */

/** The public catalogue of event types. Endpoints subscribe to some of them. */
export const WEBHOOK_EVENT_TYPES = {
  'incident.opened': 'A monitor failed 3 checks in a row and an incident opened.',
  'incident.acknowledged': 'Someone acknowledged the incident, which stops its escalation.',
  'incident.resolved': 'The incident was resolved (checks pass again, or someone marked it resolved).',
} as const;

export type WebhookEventType = keyof typeof WEBHOOK_EVENT_TYPES;
export const WEBHOOK_EVENT_TYPE_IDS = Object.keys(WEBHOOK_EVENT_TYPES) as [WebhookEventType, ...WebhookEventType[]];

/** A signing secret: "whsec_" + base64 of 24 random bytes (the Standard Webhooks format). Shown once. */
export function generateWebhookSecret(): string {
  return `whsec_${randomBytes(24).toString('base64')}`;
}

/** The signature for one delivery. The key is the secret's bytes (base64 after "whsec_"). */
export function signWebhook(secret: string, msgId: string, timestampSec: number, body: string): string {
  const key = Buffer.from(secret.replace(/^whsec_/, ''), 'base64');
  const mac = createHmac('sha256', key).update(`${msgId}.${timestampSec}.${body}`).digest('base64');
  return `v1,${mac}`;
}

/** Everything a delivery sends besides the body. */
export function webhookHeaders(secret: string, msgId: string, body: string, now = new Date()): Record<string, string> {
  const timestamp = Math.floor(now.getTime() / 1000);
  return {
    'content-type': 'application/json',
    'user-agent': 'Beacon-Webhooks/1.0',
    'webhook-id': msgId,
    'webhook-timestamp': String(timestamp),
    'webhook-signature': signWebhook(secret, msgId, timestamp, body),
  };
}

/**
 * Lesson 5.3 (🟡): when to give up on an endpoint. If every delivery has
 * failed for this long, the endpoint is disabled and the org's admins are
 * emailed; re-enabling is one click, and "replay failed" catches up.
 */
export const DISABLE_AFTER_MS = 5 * 24 * 3600_000;

export function shouldDisable(failingSince: Date | null, now: Date): boolean {
  return failingSince !== null && now.getTime() - failingSince.getTime() >= DISABLE_AFTER_MS;
}

/** A response body in the delivery log is cut short: enough to debug, not a copy of their server's page. */
export function snippet(text: string, max = 500): string {
  return text.length > max ? `${text.slice(0, max)}…` : text;
}
