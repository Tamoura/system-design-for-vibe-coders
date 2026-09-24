import { sql } from 'drizzle-orm';
import { fromDrizzle, PgBoss, type ConstructorOptions, type SendOptions } from 'pg-boss';
import { queueConnection } from '@/db';
import type { TenantTx } from '@/db/tenant';
import { stableUuid } from '@/core/ids';
import { QUEUE_SCHEMA } from './install';
import { QUEUES, type JobData, type QueueName } from './queues';

/*
 * Lesson 5.1: Beacon's job queue.
 *
 * The broker is pg-boss: jobs are rows in Postgres (schema `pgboss`), claimed
 * by workers with `SELECT … FOR UPDATE SKIP LOCKED`. Why a Postgres queue and
 * not Redis (BullMQ): Beacon already has Postgres and nothing else, and a job
 * enqueued inside a transaction commits or rolls back WITH the data it is
 * about. No outbox table, no relay process (docs/SOLUTIONS.md, Module 5).
 *
 *   producer (request, checker, another job)
 *      enqueueInTx(tx, 'incident.notify', { orgId, incidentId })   ← same transaction as the incident
 *      enqueue('email.send', { emailId })                          ← its own statement
 *            │
 *            ▼
 *   pgboss.job ──► worker (npm run worker, src/lib/queue/worker.ts) ──► handler (./handlers.ts)
 *                    throws? retry with backoff ─► last attempt fails ─► dead-letter queue
 */

const g = globalThis as unknown as { beaconBoss?: Promise<PgBoss> };

function start(options: Partial<ConstructorOptions>): Promise<PgBoss> {
  const boss = new PgBoss({ ...queueConnection, schema: QUEUE_SCHEMA, ...options });
  boss.on('error', (err) => console.error('[queue]', err));
  return boss.start();
}

/**
 * The queue client for this process. The web app and scripts only ADD jobs:
 * no maintenance, no cron, no schema migration (`npm run db:migrate` did it).
 * The worker process starts a full instance instead (startWorkerBoss).
 */
export function getBoss(): Promise<PgBoss> {
  g.beaconBoss ??= start({ supervise: false, schedule: false, migrate: false });
  return g.beaconBoss;
}

/** The worker's instance: also runs maintenance (expiring stuck jobs, retention) and the cron schedules. */
export function startWorkerBoss(): Promise<PgBoss> {
  g.beaconBoss = start({});
  return g.beaconBoss;
}

export async function stopBoss(): Promise<void> {
  const boss = await g.beaconBoss;
  g.beaconBoss = undefined;
  await boss?.stop({ graceful: true, timeout: 20_000 });
}

export type EnqueueOptions = {
  /**
   * What makes this job unique: "the check of monitor X at 12:00:30". The job
   * id is derived from it (src/core/ids.ts), so enqueuing the same key twice
   * adds one job. Leave it out for "always a new job".
   */
  key?: string;
  /** Run no earlier than this. */
  startAfter?: Date;
  /**
   * Lesson 5.1 (fairness): the job's group, usually its organization. The
   * worker caps how many jobs of one group run at once (groupConcurrency), so
   * one org with 20,000 monitors cannot occupy every worker.
   */
  group?: string;
};

function sendOptions(queue: QueueName, opts: EnqueueOptions): SendOptions {
  return {
    ...(opts.key && { id: stableUuid(`${queue}:${opts.key}`) }),
    ...(opts.startAfter && { startAfter: opts.startAfter }),
    ...(opts.group && { group: { id: opts.group } }),
  };
}

function assertQueue(queue: string): asserts queue is QueueName {
  if (!Object.hasOwn(QUEUES, queue)) throw new Error(`Unknown queue "${queue}"`);
}

/**
 * Add a job on its own. Returns the job id, or null when a job with the same
 * key already exists (nothing was added).
 */
export async function enqueue<Q extends QueueName>(queue: Q, data: JobData[Q], opts: EnqueueOptions = {}): Promise<string | null> {
  assertQueue(queue);
  const boss = await getBoss();
  return boss.send(queue, data, sendOptions(queue, opts));
}

/**
 * Lesson 5.1 (🟡): add a job INSIDE the caller's transaction (usually a
 * withOrg() callback). The job exists if and only if the transaction commits:
 *
 *   - the process dies after the incident committed → the job is committed too,
 *     and a worker will run it (no "incident nobody was told about");
 *   - the transaction rolls back → there is no job looking for a missing row.
 *
 * This is why the lesson calls Postgres-backed queues "an outbox you don't
 * have to build". It runs as beacon_app, which may only add jobs (./install.ts).
 */
export async function enqueueInTx<Q extends QueueName>(tx: TenantTx, queue: Q, data: JobData[Q], opts: EnqueueOptions = {}): Promise<string | null> {
  assertQueue(queue);
  const boss = await getBoss();
  return boss.send(queue, data, { ...sendOptions(queue, opts), db: fromDrizzle(tx, sql) });
}

export { QUEUES, type JobData, type QueueName } from './queues';
