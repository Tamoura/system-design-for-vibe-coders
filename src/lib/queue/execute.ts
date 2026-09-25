import type { JobWithMetadata } from 'pg-boss';
import { runWithContext } from '../observability/context';
import { captureError } from '../observability/errors';
import { logger } from '../observability/logger';
import { recordJob } from '../observability/metrics';
import { extractTraceContext, SpanKind, withSpan } from '../observability/telemetry';
import type { JobContext, JobMeta, QueueName } from './queues';

/*
 * Lesson 7.2: every job, in the worker and in runQueuedJobs(), runs through
 * here, so jobs are as observable as requests:
 *
 *   context   the request id of the request that enqueued it (from `_meta`),
 *             or `job:<id>` for cron jobs; the org from the payload. Every
 *             log line inside the handler carries them.
 *   trace     a CONSUMER span whose parent is the enqueue's span: one trace
 *             from "POST /api/…" to the job that did the work
 *   metrics   jobs_total{queue, outcome} and job_duration_seconds{queue}
 *   logs      job.completed / job.failed, with attempt numbers
 *   errors    the LAST failed attempt (the one that dead-letters) is captured
 *             for the error tracker; earlier ones are expected retries
 */
export async function executeJob<T>(
  queue: QueueName,
  job: Pick<JobWithMetadata, 'id' | 'data'>,
  ctx: JobContext,
  handler: (data: never, ctx: JobContext) => Promise<T>,
): Promise<T> {
  const data = (job.data ?? {}) as { orgId?: string; _meta?: JobMeta };
  const meta = data._meta;
  return runWithContext({ requestId: meta?.requestId ?? `job:${job.id}`, queue, jobId: job.id, ...(data.orgId && { orgId: data.orgId }) }, () =>
    withSpan(
      `job ${queue}`,
      { kind: SpanKind.CONSUMER, parent: extractTraceContext(meta), attributes: { 'messaging.system': 'pg-boss', 'messaging.destination.name': queue, 'messaging.message.id': job.id, 'beacon.attempt': ctx.attempt } },
      async () => {
        const started = performance.now();
        try {
          const output = await handler(job.data as never, ctx);
          const seconds = (performance.now() - started) / 1000;
          recordJob(queue, 'completed', seconds);
          logger.info({ ms: Math.round(seconds * 1000), attempt: ctx.attempt, result: summary(output) }, 'job.completed');
          return output;
        } catch (err) {
          const seconds = (performance.now() - started) / 1000;
          recordJob(queue, 'failed', seconds);
          const fields = { ms: Math.round(seconds * 1000), attempt: ctx.attempt, lastAttempt: ctx.lastAttempt, error: (err as Error).message };
          if (ctx.lastAttempt) captureError(err, { queue, jobId: job.id, attempt: ctx.attempt });
          else logger.warn(fields, 'job.failed'); // pg-boss records the error and schedules the retry
          throw err;
        }
      },
    ),
  );
}

/** A short, loggable version of a handler's result (never a whole payload). */
function summary(output: unknown): unknown {
  if (output === undefined || output === null) return undefined;
  if (typeof output === 'string') return output.slice(0, 200);
  const text = JSON.stringify(output);
  return text.length > 300 ? `${text.slice(0, 300)}…` : output;
}
