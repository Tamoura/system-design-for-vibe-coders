import { betterAuth } from 'better-auth';
import { drizzleAdapter } from 'better-auth/adapters/drizzle';
import { nextCookies } from 'better-auth/next-js';
import { db, schema } from '@/db';
import { hashPassword, verifyPassword } from './password';

/*
 * Lesson 1.1: authentication is a library's job. Better Auth owns the crypto
 * and the flows; Beacon owns the configuration and the edge cases.
 *
 *  - Passwords: argon2id hashes (./password.ts).
 *  - Sessions: server-side rows in `sessions`, referenced by an HttpOnly,
 *    SameSite=Lax cookie that is Secure whenever APP_URL is https. Signing out
 *    deletes the row, so a copied cookie stops working.
 */
export const auth = betterAuth({
  appName: 'Beacon',
  baseURL: process.env.APP_URL ?? 'http://localhost:3000',
  // Signs cookies and tokens. Better Auth refuses to start in production without it.
  secret: process.env.BETTER_AUTH_SECRET,
  database: drizzleAdapter(db, {
    provider: 'pg',
    schema: {
      user: schema.users,
      session: schema.sessions,
      account: schema.accounts,
      verification: schema.verifications,
    },
  }),
  emailAndPassword: {
    enabled: true,
    // NIST SP 800-63B: favour length over composition rules.
    minPasswordLength: 12,
    password: { hash: hashPassword, verify: verifyPassword },
  },
  session: {
    expiresIn: 60 * 60 * 24 * 30, // 30 days…
    updateAge: 60 * 60 * 24, //      …sliding forward once a day while in use.
  },
  advanced: {
    // Let Postgres generate uuid ids (gen_random_uuid()), like every other table.
    database: { generateId: 'uuid' },
    // HttpOnly and SameSite=Lax are Better Auth's defaults; spelled out so you
    // can see them. `Secure` (and the __Secure- name prefix) is added
    // automatically when APP_URL starts with https://.
    defaultCookieAttributes: { httpOnly: true, sameSite: 'lax' },
  },
  // Lets server actions that call auth.api.* set and clear the session cookie.
  plugins: [nextCookies()],
});

export type AuthSession = typeof auth.$Infer.Session;
