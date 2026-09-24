import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { sql } from 'drizzle-orm';
import { drizzle } from 'drizzle-orm/postgres-js';
import { fromDrizzle, PgBoss } from 'pg-boss';
import postgres from 'postgres';

/*
 * Lesson 5.1, against a REAL Postgres server. Runs only when DATABASE_URL is
 * set (CI provides one; locally: DATABASE_URL=postgres://… npm test). The
 * other queue tests run pg-boss on PGlite; this one covers what they cannot:
 * the app's own driver (postgres.js through Drizzle) enqueuing inside a
 * transaction, and a real polling worker with its timers.
 *
 * It uses a throwaway schema, so it never touches Beacon's own queues.
 */
const url = process.env.DATABASE_URL;

describe.skipIf(!url)('pg-boss on a real Postgres', () => {
  const schemaName = `pgboss_it_${process.pid}_${Date.now()}`;
  let boss: PgBoss;
  let client: ReturnType<typeof postgres>;
  let db: ReturnType<typeof drizzle>;

  beforeAll(async () => {
    boss = new PgBoss({ connectionString: url, schema: schemaName, max: 3, supervise: false, schedule: false });
    boss.on('error', () => {});
    await boss.start();
    await boss.createQueue('it-dead');
    await boss.createQueue('it-work', { retryLimit: 1, retryDelay: 1, deadLetter: 'it-dead' });
    client = postgres(url!, { max: 2, onnotice: () => {} });
    db = drizzle(client);
  });

  afterAll(async () => {
    await boss?.stop({ graceful: false });
    await client?.unsafe(`drop schema if exists "${schemaName}" cascade`);
    await client?.end();
  });

  it('a job enqueued in a transaction that rolls back does not exist; one that commits does', async () => {
    await db
      .transaction(async (tx) => {
        await boss.send('it-work', { n: 'rolled-back' }, { db: fromDrizzle(tx, sql) });
        throw new Error('crash before commit');
      })
      .catch(() => {});
    await db.transaction(async (tx) => {
      await boss.send('it-work', { n: 'committed' }, { db: fromDrizzle(tx, sql) });
    });
    const jobs = await boss.findJobs<{ n: string }>('it-work');
    expect(jobs.map((j) => j.data.n)).toEqual(['committed']);
    await boss.deleteAllJobs('it-work');
  });

  it('a worker retries a failing job until it works, and dead-letters one that never does', async () => {
    const seen: Record<string, number> = {};
    await boss.work<{ n: string }>('it-work', { pollingIntervalSeconds: 0.5 }, async ([job]) => {
      seen[job.data.n] = (seen[job.data.n] ?? 0) + 1;
      if (job.data.n === 'poison' || seen[job.data.n] === 1) throw new Error(`boom ${job.data.n}`);
    });
    const flaky = await boss.send('it-work', { n: 'flaky' });
    const poison = await boss.send('it-work', { n: 'poison' });
    const deadline = Date.now() + 20_000;
    let dead: unknown[] = [];
    while (Date.now() < deadline) {
      const [f] = await boss.findJobs('it-work', { id: flaky! });
      dead = await boss.findJobs('it-dead');
      if (f?.state === 'completed' && dead.length === 1) break;
      await new Promise((r) => setTimeout(r, 250));
    }
    expect(seen).toEqual({ flaky: 2, poison: 2 }); // 1 try + 1 retry each
    const [p] = await boss.findJobs('it-work', { id: poison! });
    expect(p.state).toBe('failed');
    expect(dead).toEqual([expect.objectContaining({ data: { n: 'poison' }, sourceName: 'it-work' })]);
    await boss.offWork('it-work');
  });
});
