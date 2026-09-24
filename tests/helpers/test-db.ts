import { PGlite } from '@electric-sql/pglite';
import { pg_trgm } from '@electric-sql/pglite/contrib/pg_trgm';
import { drizzle } from 'drizzle-orm/pglite';
import { migrate } from 'drizzle-orm/pglite/migrator';
import { fromPglite, PgBoss } from 'pg-boss';
import * as schema from '@/db/schema';
import { installQueues, QUEUE_SCHEMA } from '@/lib/queue/install';

/**
 * A real Postgres, in memory, for tests that touch the database. PGlite is
 * Postgres compiled to WebAssembly, so `npm test` still needs no database
 * server, and the tests run the same SQL migrations as production.
 *
 * Use it by replacing the app's `@/db` module at the top of a test file:
 *
 *   vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
 */
export async function testDbModule() {
  // pg_trgm is one of PGlite's bundled contrib extensions (lesson 2.3's
  // fuzzy search); the migrations then CREATE EXTENSION it as on a server.
  const client = new PGlite({ extensions: { pg_trgm } });
  // Lesson 2.1: every SQL statement the app sends is recorded here, so a test
  // can count queries (see tests/data-layer.test.ts, the N+1 test).
  const queryLog: string[] = [];
  const db = drizzle(client, { schema, logger: { logQuery: (query) => queryLog.push(query) } });
  await migrate(db, { migrationsFolder: 'drizzle' });
  // Lesson 5.1: the job queue (pg-boss) runs on the same in-memory Postgres,
  // as `npm run db:migrate` installs it on a real one. The started instance
  // becomes the app's queue client (src/lib/queue getBoss()), so enqueue()
  // and runQueuedJobs() in tests use the real queue, SQL and all.
  const queueConnection = { db: fromPglite(client), backend: 'pglite' as const };
  await installQueues(queueConnection);
  // Started AFTER the queues exist, so it has them all in its cache: PGlite has
  // one connection, and a cache miss inside a transaction would wait forever.
  const boss = await new PgBoss({ ...queueConnection, schema: QUEUE_SCHEMA, supervise: false, schedule: false, migrate: false }).start();
  (globalThis as unknown as { beaconBoss?: Promise<unknown> }).beaconBoss = Promise.resolve(boss);
  queryLog.length = 0;
  return { db, schema, sql: client, queryLog, queueConnection };
}
