import { drizzle } from 'drizzle-orm/postgres-js';
import type { ConstructorOptions } from 'pg-boss';
import postgres from 'postgres';
import * as schema from './schema';

const url = process.env.DATABASE_URL ?? 'postgres://beacon:beacon@localhost:5432/beacon';

// One pool per process. In dev, Next.js hot-reloads modules, so keep the
// client on globalThis to avoid opening a new pool on every edit (lesson 2.1).
const globalForDb = globalThis as unknown as { beaconSql?: ReturnType<typeof postgres> };
export const sql = globalForDb.beaconSql ?? postgres(url, { max: 10 });
if (process.env.NODE_ENV !== 'production') globalForDb.beaconSql = sql;

// Lesson 2.1: know the SQL your ORM sends. `DB_LOG=1 npm run dev` prints every
// query, which is how you spot an N+1 (one query per row of a list).
export const db = drizzle(sql, { schema, logger: process.env.DB_LOG === '1' });
export { schema };

/**
 * Lesson 5.1: how the job queue (pg-boss, src/lib/queue) reaches the same
 * database. It opens its own small pool with the `pg` driver. A job enqueued
 * inside a transaction does not use this pool: it goes through that
 * transaction (enqueueInTx), which is the point of a Postgres-backed queue.
 * The tests replace this with their in-memory Postgres (tests/helpers/test-db.ts).
 */
export const queueConnection: Pick<ConstructorOptions, 'connectionString' | 'max' | 'db' | 'backend'> = { connectionString: url, max: 4 };
