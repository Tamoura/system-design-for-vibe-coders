import { beforeAll, describe, expect, it, vi } from 'vitest';

vi.mock('@/db', () => import('./helpers/test-db').then((m) => m.testDbModule()));
vi.mock('@/lib/session', () => ({ getCurrentUser: vi.fn(), requireUser: vi.fn() }));

import { and, eq, sql } from 'drizzle-orm';
import { db, schema } from '@/db';
import { withOrg } from '@/db/tenant';
import type { CheckOutcome } from '@/core/check';
import { stableUuid } from '@/core/ids';
import { checkSlots, phaseOffsetSec } from '@/core/schedule';
import { createMonitor, updateMonitor } from '@/lib/monitors';
import { enqueue } from '@/lib/queue';
import { runScheduledCheck, scheduleChecks, WINDOW_AHEAD_MS, WINDOW_BEHIND_MS } from '@/lib/scheduler';
import { queueStatus, redriveDeadLetters } from '@/lib/queue/status';
import { makeOrg } from './helpers/fixtures';
import { clearQueues, jobsIn, retriesAreDue, runQueuedJobs } from './helpers/queue';

/*
 * Lesson 5.1: the queue itself, and the check scheduler on top of it. pg-boss
 * runs on the in-memory Postgres, so these are its real SQL and semantics:
 * deterministic job ids, transactional enqueue, retries, dead letters.
 */
type Org = Awaited<ReturnType<typeof makeOrg>>;
const UP: CheckOutcome = { ok: true, statusCode: 200, latencyMs: 5, error: null };

describe('deterministic job ids', () => {
  it('the same key is the same UUID; a different key is a different one', () => {
    expect(stableUuid('check.run:m1@12:00')).toBe(stableUuid('check.run:m1@12:00'));
    expect(stableUuid('check.run:m1@12:00')).not.toBe(stableUuid('check.run:m1@12:01'));
    expect(stableUuid('x')).toMatch(/^[0-9a-f]{8}-[0-9a-f]{4}-8[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);
  });

  it('enqueuing the same key twice adds one job', async () => {
    await clearQueues();
    expect(await enqueue('email.send', { emailId: 'e-1' }, { key: 'e-1' })).toBeTruthy();
    expect(await enqueue('email.send', { emailId: 'e-1' }, { key: 'e-1' })).toBeNull();
    expect(await jobsIn('email.send')).toHaveLength(1);
  });

  it('refuses a queue that is not declared', async () => {
    await expect(enqueue('nope' as never, {} as never)).rejects.toThrow(/Unknown queue/);
  });
});

describe('the app role may add jobs, and nothing more (lesson 2.4 meets 5.1)', () => {
  it('inside withOrg() a job can be enqueued, but other jobs cannot be read, changed or deleted', async () => {
    const org = await makeOrg('Grants');
    await enqueue('email.send', { emailId: 'someone-elses' }, { key: 'someone-elses' });
    for (const statement of [sql`select data from pgboss.job`, sql`update pgboss.job set state = 'completed'`, sql`delete from pgboss.job`]) {
      const error = await withOrg(org.id, (tx) => tx.execute(statement)).catch((e: Error & { cause?: Error }) => e.cause?.message ?? e.message);
      expect(error).toMatch(/permission denied/);
    }
  });
});

describe('retries and the dead-letter queue', () => {
  it('a job that fails every attempt ends up in the dead-letter queue with its error; redrive puts it back', async () => {
    await clearQueues();
    // An email row that does not exist is "done" (idempotent no-op), so use a
    // queue whose handler really fails: a delivery of an org that does not exist
    // throws inside withOrg (not a uuid).
    await enqueue('notification.deliver', { orgId: 'not-a-uuid', deliveryId: 'x' }, { key: 'poison' });
    for (let attempt = 0; attempt < 8; attempt++) {
      await retriesAreDue();
      await runQueuedJobs({ queues: ['notification.deliver'] });
    }
    const [original] = await jobsIn('notification.deliver');
    expect(original).toMatchObject({ state: 'failed', retry_count: 7, output: { message: expect.stringContaining('uuid') } });
    const status = await queueStatus();
    expect(status.dead).toEqual([expect.objectContaining({ sourceQueue: 'notification.deliver', error: expect.stringContaining('uuid'), data: { orgId: 'not-a-uuid', deliveryId: 'x' } })]);
    expect(status.queues.find((q) => q.queue === 'notification.deliver')).toMatchObject({ failed: 1, waiting: 0 });

    expect(await redriveDeadLetters('notification.deliver')).toBe(1);
    expect((await jobsIn('notification.deliver')).filter((j) => j.state === 'created')).toHaveLength(1);
  });

  it('a job waiting for its retry is listed with its attempt, error and next attempt', async () => {
    await clearQueues();
    await enqueue('notification.deliver', { orgId: 'not-a-uuid', deliveryId: 'y' });
    await runQueuedJobs({ queues: ['notification.deliver'] });
    const { retrying } = await queueStatus();
    expect(retrying).toEqual([expect.objectContaining({ queue: 'notification.deliver', attempt: 1, of: 8, error: expect.stringContaining('uuid') })]);
    expect(retrying[0].nextAttemptAt.getTime()).toBeGreaterThan(Date.now());
  });
});

describe('the check schedule (pure)', () => {
  it('each monitor has a stable phase inside its interval, so its checks are exactly one interval apart', () => {
    const from = new Date('2026-01-01T00:00:00Z');
    const to = new Date('2026-01-01T00:05:00Z');
    const slots = checkSlots('monitor-a', 60, from, to);
    expect(slots).toHaveLength(5);
    const phase = phaseOffsetSec('monitor-a', 60);
    expect(slots.every((s) => s.getUTCSeconds() === phase)).toBe(true);
    expect(slots[1].getTime() - slots[0].getTime()).toBe(60_000);
    expect(checkSlots('monitor-a', 60, from, to)).toEqual(slots); // same answer on every scheduler
  });

  it('spreads 6,000 one-minute monitors evenly over the minute (no spike at :00)', () => {
    const perSecond = new Array(60).fill(0);
    for (let i = 0; i < 6000; i++) perSecond[phaseOffsetSec(`monitor-${i}`, 60)]++;
    expect(Math.max(...perSecond)).toBeLessThan(160); // about 100 a second, not 6,000 at once
    expect(Math.min(...perSecond)).toBeGreaterThan(50);
  });

  it('includes a slot exactly at the window start and excludes one at its end', () => {
    const phase = phaseOffsetSec('m', 30);
    const at = new Date(Date.UTC(2026, 0, 1, 0, 0, phase));
    expect(checkSlots('m', 30, at, new Date(at.getTime() + 30_000))).toEqual([at]);
  });
});

describe('scheduleChecks() and the check.run job', () => {
  let org: Org;
  let monitor: Awaited<ReturnType<typeof createMonitor>>;

  beforeAll(async () => {
    await clearQueues();
    org = await makeOrg('Sched');
    monitor = await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name: 'api', url: 'https://api.sched.test', intervalSeconds: 60 });
  });

  it('enqueues one check.run job per slot, at the slot, grouped by org; running it again adds nothing', async () => {
    const now = new Date();
    await scheduleChecks(now);
    const expected = checkSlots(monitor.id, 60, new Date(now.getTime() - WINDOW_BEHIND_MS), new Date(now.getTime() + WINDOW_AHEAD_MS));
    const jobs = (await jobsIn('check.run')).filter((j) => j.data.monitorId === monitor.id);
    expect(jobs.map((j) => j.data.scheduledAt).sort()).toEqual(expected.map((d) => d.toISOString()));
    expect(jobs.every((j) => j.group_id === org.id)).toBe(true);
    expect(jobs.map((j) => new Date(j.start_after).getTime()).sort()).toEqual(expected.map((d) => d.getTime()));

    await scheduleChecks(now); // a second scheduler, or the cron firing twice
    await scheduleChecks(new Date(now.getTime() + 60_000)); // the next minute: its window overlaps this one
    const after = (await jobsIn('check.run')).filter((j) => j.data.monitorId === monitor.id);
    const slots = after.map((j) => j.data.scheduledAt);
    expect(new Set(slots).size).toBe(slots.length); // no slot twice
  });

  it('never schedules a paused monitor, nor faster than the plan allows (lesson 3.2)', async () => {
    const free = await makeOrg('SchedFree', { plan: 'free' });
    const slow = await createMonitor({ orgId: free.id, userId: free.users.owner.id }, { name: 'slow', url: 'https://slow.test', intervalSeconds: 300 });
    const paused = await createMonitor({ orgId: org.id, userId: org.users.owner.id }, { name: 'paused', url: 'https://paused.test', intervalSeconds: 60 });
    await updateMonitor({ orgId: org.id, userId: org.users.owner.id, role: 'owner' }, paused.id, { paused: true });
    // Free's minimum is 300 s: even a monitor stored at 60 s is checked every 5 minutes.
    await db.update(schema.monitors).set({ intervalSeconds: 60 }).where(eq(schema.monitors.id, slow.id));
    const now = new Date();
    for (let minute = 0; minute < 10; minute++) await scheduleChecks(new Date(now.getTime() + minute * 60_000));
    const jobs = await jobsIn('check.run');
    expect(jobs.filter((j) => j.data.monitorId === paused.id)).toEqual([]);
    const slowSlots = jobs.filter((j) => j.data.monitorId === slow.id).map((j) => new Date(j.data.scheduledAt as string).getTime()).sort();
    for (let i = 1; i < slowSlots.length; i++) expect(slowSlots[i] - slowSlots[i - 1]).toBe(300_000);
  });

  it('a check job that runs twice stores one result (the slot is unique per monitor)', async () => {
    const scheduledAt = new Date(Date.now() - 1000).toISOString();
    const check = vi.fn(async () => UP);
    expect(await runScheduledCheck({ orgId: org.id, monitorId: monitor.id, scheduledAt }, check)).toMatch(/✓ api/);
    expect(await runScheduledCheck({ orgId: org.id, monitorId: monitor.id, scheduledAt }, check)).toMatch(/already checked/);
    const results = await withOrg(org.id, (tx) =>
      tx.select().from(schema.checkResults).where(and(eq(schema.checkResults.monitorId, monitor.id), eq(schema.checkResults.scheduledAt, new Date(scheduledAt)))),
    );
    expect(results).toHaveLength(1);
  });

  it('skips a monitor that was deleted or paused after its job was enqueued', async () => {
    const check = vi.fn(async () => UP);
    expect(await runScheduledCheck({ orgId: org.id, monitorId: '00000000-0000-4000-8000-000000000000', scheduledAt: new Date().toISOString() }, check)).toBe('skipped: monitor deleted');
    expect(check).not.toHaveBeenCalled();
  });
});
