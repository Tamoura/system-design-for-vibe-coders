import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));

import { APIError } from 'better-auth/api';
import { auth } from '@/lib/auth';
import { checkSignInAttempt, SIGN_IN_POLICIES } from '@/lib/sign-in-throttle';

/*
 * Lesson 8.1: sign-in throttling per account and per IP, through Better Auth
 * itself (the `before`/`after` hooks in src/lib/auth.ts), on the test database.
 */
const PASSWORD = 'correct-horse-battery-staple';
let n = 0;

async function signIn(email: string, password: string, ip = '203.0.113.7') {
  try {
    await auth.api.signInEmail({ body: { email, password }, headers: new Headers({ 'x-forwarded-for': ip }) });
    return 'ok';
  } catch (err) {
    if (err instanceof APIError) return { status: err.statusCode, message: err.message };
    throw err;
  }
}

async function newAccount() {
  n++;
  const email = `throttle-${n}@example.com`;
  await auth.api.signUpEmail({ body: { name: `T${n}`, email, password: PASSWORD } });
  return email;
}

beforeAll(async () => {
  vi.stubEnv('EMAIL_DRIVER', 'memory');
});

describe('per-account throttle ("lockout")', () => {
  it('after 10 wrong passwords even the right one is refused with 429, and the message is the same as for an unknown email', async () => {
    const email = await newAccount();
    for (let i = 0; i < SIGN_IN_POLICIES.account.capacity; i++) {
      expect(await signIn(email, 'wrong-password-123', `198.51.100.${i}`)).toMatchObject({ status: 401 });
    }
    const locked = await signIn(email, PASSWORD, '198.51.100.99');
    expect(locked).toMatchObject({ status: 429, message: expect.stringMatching(/Too many sign-in attempts\. Try again in \d+ (seconds|minutes)/) });

    const unknown = 'nobody-here@example.com';
    for (let i = 0; i < SIGN_IN_POLICIES.account.capacity; i++) await signIn(unknown, 'x-password-1234', `192.0.2.${i}`);
    const unknownLocked = (await signIn(unknown, 'x-password-1234', '192.0.2.99')) as { message: string };
    expect(unknownLocked.message.replace(/\d+/g, 'N')).toBe((locked as { message: string }).message.replace(/\d+/g, 'N'));
  });

  it('a successful sign-in resets the account bucket', async () => {
    const email = await newAccount();
    for (let i = 0; i < SIGN_IN_POLICIES.account.capacity - 1; i++) await signIn(email, 'wrong-password-123', `198.51.100.${i}`);
    expect(await signIn(email, PASSWORD, '198.51.100.50')).toBe('ok');
    for (let i = 0; i < SIGN_IN_POLICIES.account.capacity - 1; i++) {
      expect(await signIn(email, 'wrong-password-123', `198.51.100.${60 + i}`)).toMatchObject({ status: 401 });
    }
  });

  it('refills over time: one attempt every 90 seconds once empty', async () => {
    const t0 = new Date('2026-01-01T00:00:00Z');
    for (let i = 0; i < 10; i++) await checkSignInAttempt('clock@example.com', null, t0);
    expect(await checkSignInAttempt('clock@example.com', null, t0)).toMatchObject({ allowed: false, reason: 'account' });
    expect(await checkSignInAttempt('clock@example.com', null, new Date(t0.getTime() + 91_000))).toEqual({ allowed: true });
  });
});

describe('per-IP throttle', () => {
  it('one address trying many accounts is refused after 30 attempts', async () => {
    const ip = '203.0.113.200';
    const results = [];
    for (let i = 0; i < SIGN_IN_POLICIES.ip.capacity + 1; i++) results.push(await signIn(`spray-${i}@example.com`, 'Password12345', ip));
    expect(results.slice(0, SIGN_IN_POLICIES.ip.capacity).every((r) => typeof r === 'object' && r.status === 401)).toBe(true);
    expect(results.at(-1)).toMatchObject({ status: 429 });
  });
});
