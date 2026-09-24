import type { JobWithMetadata } from 'pg-boss';
import { getBoss } from './index';
import { handlerFor, HANDLERS } from './handlers';
import type { JobContext, QueueName } from './queues';

/** Lesson 5.1: attempt numbers, from pg-boss's retry count (0 on the first try). */
export function jobContext(job: Pick<JobWithMetadata, 'id' | 'retryCount' | 'retryLimit'>): JobContext {
  return { jobId: job.id, attempt: job.retryCount + 1, lastAttempt: job.retryCount >= job.retryLimit };
}

/** pg-boss stores a job's result as JSON; wrap plain values. */
export function asOutput(value: unknown): object | null {
  if (value === undefined || value === null) return null;
  return typeof value === 'object' ? (value as object) : { result: value };
}

/**
 * Run every job that is due now, in this process, until the queues are empty:
 * the worker's loop, without the waiting. The tests use it on their in-memory
 * Postgres ("run the worker once"), and `npm run jobs -- run` uses it by hand.
 *
 * It is the same queue: claimed with SKIP LOCKED, completed or failed through
 * pg-boss, so a failure is retried later with backoff (not in this call) and
 * dead-lettered after the last attempt, exactly as in the worker.
 */
export async function runQueuedJobs(opts: { queues?: QueueName[]; maxRounds?: number } = {}) {
  const boss = await getBoss();
  const queues = opts.queues ?? (Object.keys(HANDLERS) as QueueName[]);
  const counts = { completed: 0, failed: 0 };
  for (let round = 0; round < (opts.maxRounds ?? 25); round++) {
    let ran = 0;
    for (const queue of queues) {
      const handler = handlerFor(queue);
      if (!handler) continue;
      const jobs = await boss.fetch<never>(queue, { batchSize: 50, includeMetadata: true });
      for (const job of jobs) {
        ran++;
        try {
          const output = await handler(job.data, jobContext(job));
          await boss.complete(queue, job.id, asOutput(output));
          counts.completed++;
        } catch (err) {
          await boss.fail(queue, job.id, { message: (err as Error).message });
          counts.failed++;
        }
      }
    }
    if (ran === 0) break; // a handler can enqueue more work (a delivery, a fallback email): go round again
  }
  return counts;
}
