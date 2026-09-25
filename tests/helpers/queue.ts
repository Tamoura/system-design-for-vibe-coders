import type { PGlite } from '@electric-sql/pglite';
import * as dbModule from '@/db';

/*
 * Lesson 5.1: helpers for tests that use the job queue. Import only from test
 * files that mock `@/db` with ./test-db.ts: pg-boss then runs on the same
 * in-memory Postgres, and runQueuedJobs() (src/lib/queue/run.ts) is "the
 * worker, once".
 */
export { runQueuedJobs } from '@/lib/queue/run';

const pg = () => (dbModule as unknown as { sql: PGlite }).sql;

/** As if the backoff had passed: every job waiting for a retry is due now. */
export async function retriesAreDue() {
  await pg().query(`update pgboss.job set start_after = now() - interval '1 second' where state = 'retry'`);
}

/** Every job of one queue, newest last: state, attempts, payload, output (the error of a failed job). */
export async function jobsIn(queue: string) {
  const { rows } = await pg().query<{ id: string; state: string; retry_count: number; retry_limit: number; start_after: Date; data: Record<string, unknown>; output: Record<string, unknown> | null; group_id: string | null }>(
    `select id, state, retry_count, retry_limit, start_after, data, output, group_id from pgboss.job where name = $1 order by created_on, id`,
    [queue],
  );
  return rows;
}

/** Empty every queue, so a test starts from nothing. */
export async function clearQueues() {
  await pg().query(`delete from pgboss.job`);
}

/** As if their start time had come: every created job of one queue is due now (lesson 6.2: the per-minute analytics batch). */
export async function jobsAreDue(queue: string) {
  await pg().query(`update pgboss.job set start_after = now() - interval '1 second' where name = $1 and state = 'created'`, [queue]);
}
