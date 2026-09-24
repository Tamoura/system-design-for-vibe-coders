import { createLinkToken, readLinkToken, type LinkToken } from '@/core/tokens';

/** Absolute links for emails, SMS and Slack: they are read outside the browser, so a path is not enough. */
export function appUrl(path: string): string {
  return `${(process.env.APP_URL ?? 'http://localhost:3000').replace(/\/$/, '')}${path}`;
}

/*
 * Lesson 4.2: signed links (src/core/tokens.ts) with the app's secret. The
 * same BETTER_AUTH_SECRET signs sessions; the HMAC key is prefixed, so a
 * token from one use cannot be replayed as the other.
 */
function secret(): string {
  const s = process.env.BETTER_AUTH_SECRET;
  if (!s && process.env.NODE_ENV === 'production') throw new Error('BETTER_AUTH_SECRET is required to sign links');
  return s ?? 'beacon-development-secret';
}

export const signLink = (payload: LinkToken) => createLinkToken(payload, secret());
export const readLink = (token: string) => readLinkToken(token, secret());

/** Lesson 4.2: the two unsubscribe links in an email: a page for people, and the RFC 8058 one-click endpoint for mail clients. */
export function unsubscribeLinks(payload: LinkToken): { page: string; oneClick: string } {
  const token = encodeURIComponent(signLink(payload));
  return { page: appUrl(`/unsubscribe?token=${token}`), oneClick: appUrl(`/api/unsubscribe?token=${token}`) };
}
