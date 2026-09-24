import { boolean, index, pgTable, text, timestamp, uuid } from 'drizzle-orm/pg-core';

/*
 * Lesson 1.1: the tables Better Auth needs. Their shape belongs to the library
 * (https://www.better-auth.com/docs/concepts/database#core-schema), so they
 * live apart from the tables Beacon owns in schema.ts.
 *
 * Watch the word "account": here it means *a way to log in* (a password, a
 * GitHub identity), not the customer. The customer is an organization (1.2).
 */

export const users = pgTable('users', {
  // Our own id, not a vendor's (lesson 1.1: lock-in is mostly about user ids).
  id: uuid('id').primaryKey().defaultRandom(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  emailVerified: boolean('email_verified').notNull().default(false),
  image: text('image'),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
});

/**
 * Server-side sessions. Logging out deletes the row, so a copied cookie stops
 * working immediately — the thing a JWT cannot do (lesson 1.1).
 */
export const sessions = pgTable(
  'sessions',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    userId: uuid('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
    token: text('token').notNull().unique(),
    expiresAt: timestamp('expires_at', { withTimezone: true }).notNull(),
    ipAddress: text('ip_address'),
    userAgent: text('user_agent'),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => [index('sessions_user_idx').on(t.userId)],
);

/**
 * Login methods. providerId "credential" holds the argon2id password hash;
 * providerId "github" holds the GitHub identity, keyed on GitHub's stable user
 * id (accountId), never on the email (lesson 1.1, social login).
 */
export const accounts = pgTable(
  'accounts',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    userId: uuid('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
    providerId: text('provider_id').notNull(),
    accountId: text('account_id').notNull(),
    password: text('password'),
    accessToken: text('access_token'),
    refreshToken: text('refresh_token'),
    idToken: text('id_token'),
    accessTokenExpiresAt: timestamp('access_token_expires_at', { withTimezone: true }),
    refreshTokenExpiresAt: timestamp('refresh_token_expires_at', { withTimezone: true }),
    scope: text('scope'),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => [index('accounts_user_idx').on(t.userId)],
);

/**
 * Short-lived tokens: password-reset links and OAuth state. Better Auth is
 * configured to store only a hash of the identifier (storeIdentifier: 'hashed').
 */
export const verifications = pgTable(
  'verifications',
  {
    id: uuid('id').primaryKey().defaultRandom(),
    identifier: text('identifier').notNull(),
    value: text('value').notNull(),
    expiresAt: timestamp('expires_at', { withTimezone: true }).notNull(),
    createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
    updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
  },
  (t) => [index('verifications_identifier_idx').on(t.identifier)],
);

export type User = typeof users.$inferSelect;
