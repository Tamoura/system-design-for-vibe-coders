import { drizzle } from 'drizzle-orm/postgres-js';
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
