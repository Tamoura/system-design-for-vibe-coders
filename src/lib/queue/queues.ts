import type { Queue } from 'pg-boss';

/*
 * Lesson 5.1: every queue Beacon has, and how its jobs retry. Plain data, in
 * one place, the way src/core/plans.ts holds the plans: `npm run db:migrate`
 * creates these queues, the worker (scripts/worker.ts) works them, and
 * enqueue() refuses a name that is not here.
 *
 * Queues are split by URGENCY and FAILURE MODE, not by code module:
 *
 *   checks.schedule   every minute: decide which checks are due (cron, singleton)
 *   check.run         one uptime check: late is useless, so barely any retries
 *   workflow.run      run or resume a durable workflow (lesson 5.4): the
 *                     incident fan-out to people and channels, escalations
 *   notification.deliver / email.send
 *                     one message to one person on one channel: a provider can
 *                     be down for an hour, so 8 attempts with exponential backoff
 *   webhook.deliver   one signed POST to a customer's endpoint (lesson 5.3):
 *                     retried for about a day and a half, then dead-lettered
 *   file.process      a thumbnail (lesson 2.2)
 *   usage.report      send SMS usage to the billing meter (lesson 3.3), every 5 minutes
 *   analytics.forward send one org's product events to PostHog in a batch (lesson 6.2),
 *                     at most one job per org per minute
 *   billing.comps     hourly: end complimentary plans past their date (lesson 7.1)
 *   audit.retention   daily: delete audit events older than the plan keeps (lesson 7.3)
 *   audit.verify      daily: recompute every audit hash chain; a broken one logs
 *                     `audit.chain_broken` at error level, which pages (lesson 7.2)
 *   org.export        build one org's data export file (lesson 8.1, GDPR portability)
 *   org.delete        purge an org after its grace period (lesson 8.1, erasure): delayed
 *   retention.purge   daily: delete data past its retention (lesson 8.1, src/core/retention.ts)
 *   ai.summarize      write one incident's AI summary draft (lesson 8.2). The gateway already
 *                     retries and falls back between models; the job retries only a crash
 *
 * Retries (pg-boss): `retryLimit` retries AFTER the first attempt, so 7 means
 * 8 attempts. With `retryBackoff` the delay before retry n is about
 * retryDelay × 2^n, randomised between half and all of it (jitter, so 5,000
 * jobs that failed together do not all retry in the same second), and never
 * more than `retryDelayMax`. For retryDelay 30 s: ~30 s, 1 min, 2 min, 4 min,
 * 8 min, 16 min, 32 min: about an hour of outage is absorbed.
 *
 * Dead letters: a job whose last attempt fails is copied into DEAD_LETTER
 * with its payload, and the failed original keeps its error (`output`).
 * `npm run jobs` lists both; `npm run jobs -- redrive` puts them back.
 */
export const DEAD_LETTER = 'dead-letter';

/** 8 attempts, ~1 hour of backoff, then the dead-letter queue. The lesson's default for "talk to a provider". */
const PROVIDER_RETRIES = { retryLimit: 7, retryDelay: 30, retryBackoff: true, retryDelayMax: 30 * 60, deadLetter: DEAD_LETTER } as const;

export const QUEUES = {
  [DEAD_LETTER]: {
    // Nobody works this queue: it is a parking lot a human looks at. Keep a month.
    retentionSeconds: 30 * 24 * 3600,
  },
  'checks.schedule': {
    // Lesson 5.1: "use your queue's scheduler, which takes a lock". pg-boss's cron
    // creates one job per minute however many workers run; `singleton` lets only
    // one run at a time.
    policy: 'singleton',
    retryLimit: 1,
    expireInSeconds: 120,
    deleteAfterSeconds: 3600,
  },
  'check.run': {
    // A check that runs 10 minutes late is not worth running: the next slot is
    // already queued. One quick retry for a crashed worker, no dead letter.
    retryLimit: 1,
    retryDelay: 5,
    expireInSeconds: 60,
    // Completed checks stay an hour: long enough that the scheduler, which
    // re-enqueues overlapping windows, finds the job id taken (see scheduler.ts).
    deleteAfterSeconds: 3600,
  },
  // Lesson 5.4: each job replays one workflow run until it finishes or waits.
  'workflow.run': { ...PROVIDER_RETRIES, expireInSeconds: 300 },
  'notification.deliver': { ...PROVIDER_RETRIES, expireInSeconds: 120 },
  'email.send': { ...PROVIDER_RETRIES, expireInSeconds: 120 },
  // Lesson 5.3: "a customer's endpoint being down during their deploy should not
  // lose events". 18 attempts, 5 s doubling to a 6-hour cap: about 30-40 hours.
  // A request times out after 10 s (src/lib/webhooks.ts), so the job's own
  // expiry can stay short.
  'webhook.deliver': { retryLimit: 17, retryDelay: 5, retryBackoff: true, retryDelayMax: 6 * 3600, deadLetter: DEAD_LETTER, expireInSeconds: 60 },
  'file.process': { retryLimit: 3, retryDelay: 10, retryBackoff: true, deadLetter: DEAD_LETTER, expireInSeconds: 300 },
  'usage.report': { policy: 'singleton', retryLimit: 2, retryDelay: 60, expireInSeconds: 600, deleteAfterSeconds: 24 * 3600 },
  // Lesson 6.2: an analytics outage delays events, it never loses them (the rows stay unforwarded).
  'analytics.forward': { ...PROVIDER_RETRIES, expireInSeconds: 120 },
  // Module 7: housekeeping. Singletons: one run at a time, a failed run retries a few times.
  'billing.comps': { policy: 'singleton', retryLimit: 3, retryDelay: 60, expireInSeconds: 600, deleteAfterSeconds: 7 * 24 * 3600 },
  'audit.retention': { policy: 'singleton', retryLimit: 3, retryDelay: 300, expireInSeconds: 1800, deleteAfterSeconds: 30 * 24 * 3600 },
  'audit.verify': { policy: 'singleton', retryLimit: 1, retryDelay: 300, expireInSeconds: 3600, deleteAfterSeconds: 30 * 24 * 3600 },
  // Module 8. An export or a deletion that fails every attempt lands in the dead letters,
  // where someone must look: a customer is waiting for their data, or for it to be gone.
  'org.export': { retryLimit: 3, retryDelay: 60, retryBackoff: true, deadLetter: DEAD_LETTER, expireInSeconds: 900 },
  'org.delete': { retryLimit: 5, retryDelay: 300, retryBackoff: true, deadLetter: DEAD_LETTER, expireInSeconds: 1800, deleteAfterSeconds: 90 * 24 * 3600 },
  'retention.purge': { policy: 'singleton', retryLimit: 3, retryDelay: 300, expireInSeconds: 3600, deleteAfterSeconds: 30 * 24 * 3600 },
  'ai.summarize': { retryLimit: 2, retryDelay: 30, retryBackoff: true, deadLetter: DEAD_LETTER, expireInSeconds: 300 },
} as const satisfies Record<string, Omit<Queue, 'name'>>;

export type QueueName = keyof typeof QUEUES;

/**
 * What each job carries. Lesson 5.1: IDs, not objects. The worker re-reads
 * the rows, so a job retried an hour later acts on today's data, and every
 * payload names its organization (lesson 2.4: the job runs inside withOrg).
 */
export type JobData = {
  [DEAD_LETTER]: Record<string, unknown>;
  'checks.schedule': Record<string, never>;
  'check.run': { orgId: string; monitorId: string; scheduledAt: string };
  'workflow.run': { orgId: string; runId: string };
  'notification.deliver': { orgId: string; deliveryId: string };
  'email.send': { emailId: string };
  'webhook.deliver': { orgId: string; messageId: string; manual?: boolean };
  'file.process': { orgId: string; fileId: string };
  'usage.report': Record<string, never>;
  'analytics.forward': { orgId: string };
  'billing.comps': Record<string, never>;
  'audit.retention': Record<string, never>;
  'audit.verify': Record<string, never>;
  'org.export': { orgId: string; exportId: string };
  'org.delete': { orgId: string };
  'retention.purge': Record<string, never>;
  'ai.summarize': { orgId: string; incidentId: string };
};

/**
 * Lesson 7.2: added to a job's data by enqueue() when it is enqueued inside a
 * request or a trace: the request id (so the worker's log lines carry it) and
 * the W3C trace context (so the job's span joins the request's trace).
 */
export type JobMeta = { requestId?: string; traceparent?: string; tracestate?: string };

/** Recurring jobs (lesson 5.1 "Scheduled tasks"): pg-boss cron, UTC. One job per tick across all workers. */
export const SCHEDULES: { queue: QueueName; cron: string }[] = [
  { queue: 'checks.schedule', cron: '* * * * *' },
  { queue: 'usage.report', cron: '*/5 * * * *' },
  { queue: 'billing.comps', cron: '7 * * * *' },
  { queue: 'audit.retention', cron: '17 3 * * *' },
  { queue: 'audit.verify', cron: '37 3 * * *' },
  { queue: 'retention.purge', cron: '47 3 * * *' },
];

export function isQueueName(name: string): name is QueueName {
  return Object.hasOwn(QUEUES, name);
}

/** What a handler knows about the job it is running. */
export type JobContext = {
  jobId: string;
  /** 1 on the first try. */
  attempt: number;
  /** No retry follows if this attempt throws (the job goes to the dead-letter queue, if it has one). */
  lastAttempt: boolean;
};
