import { createHmac, timingSafeEqual } from 'node:crypto';
import { suppressEmail } from './index';

/*
 * Lesson 4.1 (🟡): the provider tells us what happened to our mail. Resend
 * signs its webhooks the Svix way; verify exactly like Stripe's in 3.1:
 *
 *   1. the signature is an HMAC of "<id>.<timestamp>.<raw body>" with our
 *      secret, compared in constant time;
 *   2. the timestamp is at most 5 minutes old (a captured request cannot be
 *      replayed tomorrow);
 *   3. only then parse the JSON and act on it.
 */
const TOLERANCE_SECONDS = 5 * 60;

export type SignatureHeaders = { id: string | null; timestamp: string | null; signature: string | null };

function hmac(secret: string, id: string, timestamp: string, body: string): string {
  // Svix secrets look like "whsec_<base64 key>".
  const key = Buffer.from(secret.replace(/^whsec_/, ''), 'base64');
  return createHmac('sha256', key).update(`${id}.${timestamp}.${body}`).digest('base64');
}

export function verifyWebhookSignature(body: string, headers: SignatureHeaders, secret: string, now = Date.now()): boolean {
  const { id, timestamp, signature } = headers;
  if (!id || !timestamp || !signature || !secret) return false;
  const seconds = Number(timestamp);
  if (!Number.isFinite(seconds) || Math.abs(now / 1000 - seconds) > TOLERANCE_SECONDS) return false;
  const expected = Buffer.from(hmac(secret, id, timestamp, body));
  // The header can carry several signatures ("v1,abc v1,def") during a secret rotation.
  return signature.split(' ').some((part) => {
    const [version, value] = part.split(',');
    if (version !== 'v1' || !value) return false;
    const given = Buffer.from(value);
    return given.length === expected.length && timingSafeEqual(given, expected);
  });
}

/** For tests and local simulation: the headers the provider would send with `body`. */
export function signWebhookForTests(body: string, secret: string, id = `msg_${Date.now()}`, timestamp = Math.floor(Date.now() / 1000)) {
  const ts = String(timestamp);
  return { 'svix-id': id, 'svix-timestamp': ts, 'svix-signature': `v1,${hmac(secret, id, ts, body)}` };
}

type ProviderEvent = {
  type?: string;
  data?: { to?: string[] | string; bounce?: { type?: string; subType?: string; message?: string } };
};

/**
 * Act on one verified event. Hard bounce → suppress. Complaint → suppress.
 * Soft (transient) bounces are the provider's to retry; we only log them.
 * Everything else (delivered, opened…) is acknowledged and ignored.
 */
export async function handleEmailEvent(event: ProviderEvent): Promise<{ suppressed: string[] }> {
  const to = event.data?.to;
  const recipients = Array.isArray(to) ? to : to ? [to] : [];
  if (event.type === 'email.bounced') {
    const bounce = event.data?.bounce;
    if (bounce?.type !== 'Permanent') {
      console.warn(`[email] soft bounce for ${recipients.join(', ')}: ${bounce?.message ?? bounce?.type ?? 'unknown'}`);
      return { suppressed: [] };
    }
    for (const r of recipients) await suppressEmail(r, 'hard_bounce', [bounce.subType, bounce.message].filter(Boolean).join(': '));
    return { suppressed: recipients };
  }
  if (event.type === 'email.complained') {
    for (const r of recipients) await suppressEmail(r, 'complaint', 'marked as spam');
    return { suppressed: recipients };
  }
  return { suppressed: [] };
}
