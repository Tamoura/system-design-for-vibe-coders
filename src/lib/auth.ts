import { betterAuth } from 'better-auth';
import { drizzleAdapter } from 'better-auth/adapters/drizzle';
import { nextCookies } from 'better-auth/next-js';
import { db, schema } from '@/db';
import { hashPassword, verifyPassword } from './password';
import { sendEmail } from './email';
import { createPersonalOrganization } from './organizations';

/** "Sign in with GitHub" is switched on by setting both env vars (see .env.example). */
export const githubEnabled = Boolean(process.env.GITHUB_CLIENT_ID && process.env.GITHUB_CLIENT_SECRET);

/*
 * Lesson 1.1: authentication is a library's job. Better Auth owns the crypto
 * and the flows; Beacon owns the configuration and the edge cases.
 *
 *  - Passwords: argon2id hashes (./password.ts).
 *  - Sessions: server-side rows in `sessions`, referenced by an HttpOnly,
 *    SameSite=Lax cookie that is Secure whenever APP_URL is https. Signing out
 *    deletes the row, so a copied cookie stops working.
 *  - Reset links: hashed in the database, valid for one hour, single use, and
 *    a completed reset signs out every session of that user.
 *  - GitHub: authorization code flow with PKCE and a checked `state`, keyed on
 *    GitHub's user id. It never merges into an existing account on its own.
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
    // Lesson 1.1 (🟡): password reset. Better Auth answers "reset my password"
    // with the same body whether or not the email exists.
    resetPasswordTokenExpiresIn: 60 * 60, // one hour
    revokeSessionsOnPasswordReset: true, // "someone else may be in my account"
    sendResetPassword: async ({ user, url }) => {
      await sendEmail({
        to: user.email,
        subject: 'Reset your Beacon password',
        text: `Someone asked to reset your Beacon password. If it was you, open this link within an hour:\n${url}\nIf it wasn't, ignore this email.`,
      });
    },
  },
  // Lesson 1.1: prove the user controls the address before trusting it for
  // anything important (sending invitations, lesson 1.2).
  emailVerification: {
    sendOnSignUp: true,
    autoSignInAfterVerification: true,
    sendVerificationEmail: async ({ user, url }) => {
      await sendEmail({ to: user.email, subject: 'Confirm your email for Beacon', text: `Confirm your email address:\n${url}` });
    },
  },
  // Store only a hash of reset tokens and other one-time identifiers, so a
  // leaked database copy cannot be used to reset anyone's password.
  verification: { storeIdentifier: 'hashed' },
  socialProviders: githubEnabled
    ? { github: { clientId: process.env.GITHUB_CLIENT_ID!, clientSecret: process.env.GITHUB_CLIENT_SECRET! } }
    : {},
  account: {
    accountLinking: {
      enabled: true,
      // Lesson 1.1: never merge a GitHub identity into an existing account just
      // because the emails match. The user must sign in with their existing
      // method first and click "Link GitHub" on /account; Better Auth then also
      // requires GitHub to report that email as verified.
      disableImplicitLinking: true,
    },
  },
  databaseHooks: {
    user: {
      create: {
        // Lesson 1.2: every new user lands in a working product — their own
        // personal organization, with them as owner.
        after: async (user) => {
          await createPersonalOrganization(user);
        },
      },
    },
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
