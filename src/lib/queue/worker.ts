import type { WorkOptions } from 'pg-boss';
import { db, schema } from '@/db';
import { listPendingEmailIds } from '../email';
import { listProcessingFileIds } from '../files';
import { listPendingDeliveryIds } from '../notifications/deliver';
import { logger } from '../observability/logger';
import { enqueue, startWorkerBoss } from './index';
import { executeJob } from './execute';
import { handlerFor } from './handlers';
import { SCHEDULES, type QueueName } from './queues';
import { asOutput, jobContext } from './run';

/*
 * Lesson 5.1: the worker process (`npm run worker`). Run one or several:
 * pg-boss claims each job with SKIP LOCKED, so two workers never run the same
 * job, and its cron takes a lock, so the schedule fires once per tick however
 * many workers there are ("never run cron in every web instance").
 *
 * localConcurrency  how many jobs of that queue this process runs at once
 * groupConcurrency  lesson 5.1 fairness: how many jobs of ONE group (one
 *                   organization, or one webhook endpoint) may run at once
 *                   across ALL workers. An org with 20,000 monitors gets 5
 *                   check slots at a time; the other 15 stay free for everyone else.
 */
export const WORKERS: Partial<Record<QueueName, WorkOptions>> = {
  'checks.schedule': { localConcurrency: 1, pollingIntervalSeconds: 2 },
  'check.run': { localConcurrency: 20, groupConcurrency: 5 },
  // Lesson 5.4: groups are RUNS: one job per run at a time, so a timer and a
  // signal arriving together never replay the same run in parallel.
  'workflow.run': { localConcurrency: 10, groupConcurrency: 1 },
  'notification.deliver': { localConcurrency: 10, groupConcurrency: 5 },
  'email.send': { localConcurrency: 10 },
  // Lesson 5.3: groups are ENDPOINTS here. A slow endpoint holds at most 2 of
  // the 10 slots (each for at most 10 s), so it cannot delay anyone else's.
  'webhook.deliver': { localConcurrency: 10, groupConcurrency: 2 },
  'file.process': { localConcurrency: 2 },
  'usage.report': { localConcurrency: 1, pollingIntervalSeconds: 5 },
  // Lesson 6.2: one forwarding job per org at a time, so two never send the same rows.
  'analytics.forward': { localConcurrency: 2, groupConcurrency: 1, pollingIntervalSeconds: 5 },
  // Module 7: housekeeping, once an hour or once a day.
  'billing.comps': { localConcurrency: 1, pollingIntervalSeconds: 30 },
  'audit.retention': { localConcurrency: 1, pollingIntervalSeconds: 30 },
  'audit.verify': { localConcurrency: 1, pollingIntervalSeconds: 30 },
};

export async function startWorkers() {
  const boss = await startWorkerBoss();
  for (const { queue, cron } of SCHEDULES) await boss.schedule(queue, cron, {}, { tz: 'UTC' });

  for (const [queue, options] of Object.entries(WORKERS) as [QueueName, WorkOptions][]) {
    const handler = handlerFor(queue);
    if (!handler) continue;
    // Lesson 7.2: executeJob() gives each job its request context, span, metrics and log lines.
    // A throw is a failed attempt: pg-boss records the error and schedules the retry.
    await boss.work(queue, { pollingIntervalSeconds: 1, ...options, includeMetadata: true }, async ([job]) =>
      asOutput(await executeJob(queue, job as Parameters<typeof executeJob>[1], jobContext(job), handler as (data: never, ctx: ReturnType<typeof jobContext>) => Promise<unknown>)),
    );
  }
  await requeueOrphans();
  return boss;
}

/**
 * Rows that need a job, and should already have one. Normally every one does
 * (they are enqueued in the same transaction), so this adds nothing: the job
 * ids come from the rows, and an existing id is not added twice. It matters
 * once, after upgrading from Module 4, whose pending rows had no jobs.
 */
export async function requeueOrphans() {
  let n = 0;
  for (const emailId of await listPendingEmailIds()) if (await enqueue('email.send', { emailId }, { key: emailId })) n++;
  const orgs = await db.select({ id: schema.organizations.id }).from(schema.organizations);
  for (const { id: orgId } of orgs) {
    for (const deliveryId of await listPendingDeliveryIds(orgId)) {
      if (await enqueue('notification.deliver', { orgId, deliveryId }, { key: deliveryId, group: orgId })) n++;
    }
    for (const fileId of await listProcessingFileIds({ orgId })) if (await enqueue('file.process', { orgId, fileId }, { key: fileId })) n++;
  }
  if (n) logger.info({ requeued: n }, 'worker.requeued_orphans');
}
