import { PGlite } from '@electric-sql/pglite';
import { drizzle } from 'drizzle-orm/pglite';
import { migrate } from 'drizzle-orm/pglite/migrator';
import * as schema from '@/db/schema';

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
  const client = new PGlite();
  // Lesson 2.1: every SQL statement the app sends is recorded here, so a test
  // can count queries (see tests/data-layer.test.ts, the N+1 test).
  const queryLog: string[] = [];
  const db = drizzle(client, { schema, logger: { logQuery: (query) => queryLog.push(query) } });
  await migrate(db, { migrationsFolder: 'drizzle' });
  queryLog.length = 0;
  return { db, schema, sql: client, queryLog };
}
