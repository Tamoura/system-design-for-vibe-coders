import { createHmac, timingSafeEqual } from 'node:crypto';

/*
 * Lesson 4.2 (🟡): links that work without logging in, such as "unsubscribe"
 * and "confirm my subscription". The token is the data itself plus an HMAC
 * signature:
 *
 *   base64url(JSON payload) + "." + base64url(HMAC-SHA256(secret, payload))
 *
 * Nobody can forge or alter one without the server's secret, and there is no
 * table to look it up in. What a token may do is small on purpose: turn off
 * one category of email for one person, or confirm/remove one subscriber.
 * Tokens that grant access (sessions, password resets) are random and stored
 * hashed instead (lesson 1.1).
 */
export type LinkToken =
  | { kind: 'unsubscribe-category'; orgId: string; userId: string; category: string }
  | { kind: 'subscriber-confirm'; orgId: string; subscriberId: string }
  | { kind: 'subscriber-unsubscribe'; orgId: string; subscriberId: string };

function sign(data: string, secret: string): string {
  return createHmac('sha256', `beacon-link:${secret}`).update(data).digest('base64url');
}

export function createLinkToken(payload: LinkToken, secret: string): string {
  const data = Buffer.from(JSON.stringify(payload)).toString('base64url');
  return `${data}.${sign(data, secret)}`;
}

/** The payload, or null if the token was altered, truncated or signed with another secret. */
export function readLinkToken(token: string, secret: string): LinkToken | null {
  const [data, signature, extra] = token.split('.');
  if (!data || !signature || extra !== undefined) return null;
  const expected = Buffer.from(sign(data, secret));
  const given = Buffer.from(signature);
  if (expected.length !== given.length || !timingSafeEqual(expected, given)) return null;
  try {
    const payload = JSON.parse(Buffer.from(data, 'base64url').toString('utf8'));
    return payload && typeof payload.kind === 'string' ? (payload as LinkToken) : null;
  } catch {
    return null;
  }
}
