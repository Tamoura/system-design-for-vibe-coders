import { createHash } from 'node:crypto';
import { eq } from 'drizzle-orm';
import { db, schema } from '@/db';
import type { RateLimitPolicy } from '@/core/rate-limit';
import { consumeRateLimit } from './rate-limit';
import { logger } from './observability/logger';

/*
 * Lesson 8.1 (threat model: "credential stuffing" against user accounts,
 * lesson 1.1's defences): sign-in attempts are throttled twice, with lesson
 * 5.2's token buckets in Postgres (every app instance shares them):
 *
 *   per ACCOUNT  10 attempts, then one every 90 seconds, until a successful
 *                sign-in resets it. That is the "lockout": a password guesser gets
 *                ~40 tries an hour instead of thousands, and the real user is
 *                never locked out for long (a hard lockout is a denial-of-service
 *                button anyone can press with your email address).
 *   per IP       30 attempts, then 3 a minute: one machine trying many accounts.
 *
 * The account bucket is keyed by a HASH of the email, whether or not an account
 * exists, and the refusal says the same thing either way: the throttle cannot
 * be used to find out who has an account (lesson 1.1, enumeration).
 * Better Auth's own per-IP limiter (in memory, per instance) stays on in production too.
 */
export const SIGN_IN_POLICIES = {
  account: { name: 'sign-in-account', capacity: 10, refillPerSec: 1 / 90 },
  ip: { name: 'sign-in-ip', capacity: 30, refillPerSec: 3 / 60 },
} satisfies Record<string, RateLimitPolicy>;

const accountKey = (email: string) => `signin:acct:${createHash('sha256').update(email.trim().toLowerCase()).digest('hex')}`;

export type SignInDecision = { allowed: true } | { allowed: false; retryAfterSec: number; reason: 'account' | 'ip' };

/** Called before every email/password sign-in (a Better Auth `before` hook in src/lib/auth.ts). */
export async function checkSignInAttempt(email: string, ip: string | null, now = new Date()): Promise<SignInDecision> {
  if (ip) {
    const byIp = await consumeRateLimit(`signin:ip:${ip}`, SIGN_IN_POLICIES.ip, now);
    if (!byIp.allowed) {
      logger.warn({ reason: 'ip' }, 'auth.sign_in_throttled');
      return { allowed: false, retryAfterSec: byIp.retryAfterSec, reason: 'ip' };
    }
  }
  const byAccount = await consumeRateLimit(accountKey(email), SIGN_IN_POLICIES.account, now);
  if (!byAccount.allowed) {
    // The IP goes to the log (a security signal to alert on), the email never does.
    logger.warn({ reason: 'account', account: accountKey(email).slice(-12) }, 'auth.sign_in_throttled');
    return { allowed: false, retryAfterSec: byAccount.retryAfterSec, reason: 'account' };
  }
  return { allowed: true };
}

/** A successful sign-in: the account's bucket starts full again. */
export async function clearSignInThrottle(email: string): Promise<void> {
  await db.delete(schema.rateLimitBuckets).where(eq(schema.rateLimitBuckets.key, accountKey(email)));
}

/** The message a refused sign-in shows. The same for every email, existing or not. */
export function throttledMessage(retryAfterSec: number): string {
  const wait = retryAfterSec >= 90 ? `${Math.ceil(retryAfterSec / 60)} minutes` : `${retryAfterSec} seconds`;
  return `Too many sign-in attempts. Try again in ${wait}, or reset your password.`;
}
