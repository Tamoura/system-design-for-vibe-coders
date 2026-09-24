import type { WorkOptions } from 'pg-boss';
import { db, schema } from '@/db';
import { listPendingEmailIds } from '../email';
import { listProcessingFileIds } from '../files';
import { listPendingDeliveryIds } from '../notifications/deliver';
import { enqueue, startWorkerBoss } from './index';
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
 *                   organization) may run at once across ALL workers. An org
 *                   with 20,000 monitors gets 5 check slots at a time; the
 *                   other 15 slots stay free for everyone else.
 */
export const WORKERS: Partial<Record<QueueName, WorkOptions>> = {
  'checks.schedule': { localConcurrency: 1, pollingIntervalSeconds: 2 },
  'check.run': { localConcurrency: 20, groupConcurrency: 5 },
  'incident.notify': { localConcurrency: 5 },
  'notification.deliver': { localConcurrency: 10, groupConcurrency: 5 },
  'email.send': { localConcurrency: 10 },
  'file.process': { localConcurrency: 2 },
  'usage.report': { localConcurrency: 1, pollingIntervalSeconds: 5 },
};

const log = (...args: unknown[]) => console.log(new Date().toISOString().slice(11, 19), ...args);

export async function startWorkers() {
  const boss = await startWorkerBoss();
  for (const { queue, cron } of SCHEDULES) await boss.schedule(queue, cron, {}, { tz: 'UTC' });

  for (const [queue, options] of Object.entries(WORKERS) as [QueueName, WorkOptions][]) {
    const handler = handlerFor(queue);
    if (!handler) continue;
    await boss.work(queue, { pollingIntervalSeconds: 1, ...options, includeMetadata: true }, async ([job]) => {
      const ctx = jobContext(job);
      const started = Date.now();
      try {
        const output = await handler(job.data as never, ctx);
        log(`✓ ${queue} ${Date.now() - started} ms`, summary(output));
        return asOutput(output);
      } catch (err) {
        log(`✗ ${queue} attempt ${ctx.attempt}${ctx.lastAttempt ? ' (last: dead-lettered)' : ', will retry'}: ${(err as Error).message}`);
        throw err; // pg-boss records the error and schedules the retry
      }
    });
  }
  await requeueOrphans();
  return boss;
}

function summary(output: unknown): string {
  if (typeof output === 'string') return output.trim();
  return output === undefined ? '' : JSON.stringify(output);
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
  if (n) log(`requeued ${n} job(s) for rows that had none`);
}
