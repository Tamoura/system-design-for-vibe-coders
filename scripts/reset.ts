/**
 * Lesson 2.1: `npm run db:reset` = this script, then `db:migrate`, then
 * `db:seed`. From a fresh clone, one command gives you a working, seeded
 * database.
 *
 * It drops every table, so it refuses to touch anything but a local database
 * (host localhost or 127.0.0.1) unless you pass --force, and it never runs
 * with NODE_ENV=production.
 */
import postgres from 'postgres';

const url = process.env.DATABASE_URL ?? 'postgres://beacon:beacon@localhost:5432/beacon';
const host = new URL(url).hostname;
const force = process.argv.includes('--force');

if (process.env.NODE_ENV === 'production' || (!['localhost', '127.0.0.1', '::1'].includes(host) && !force)) {
  console.error(`Refusing to reset the database on "${host}". It only resets local databases (use --force if you really mean it).`);
  process.exit(1);
}

const sql = postgres(url, { max: 1, onnotice: () => {} });
// Everything Beacon creates lives in the "public" schema, plus drizzle's
// record of which migrations ran in the "drizzle" schema.
await sql`DROP SCHEMA IF EXISTS drizzle CASCADE`;
await sql`DROP SCHEMA IF EXISTS public CASCADE`;
await sql`CREATE SCHEMA public`;
await sql.end();
console.log(`✓ dropped everything in ${new URL(url).pathname.slice(1)} on ${host}`);
