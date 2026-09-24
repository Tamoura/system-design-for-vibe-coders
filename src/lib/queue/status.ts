import { getBoss } from './index';
import { QUEUE_SCHEMA } from './install';
import { DEAD_LETTER, QUEUES } from './queues';

/*
 * Lesson 5.1 "Monitoring": the four numbers to watch per queue, plus what is
 * retrying and what is dead. `npm run jobs` prints this; an admin page
 * (lesson 7.1) would show the same. Alert on the AGE of the oldest waiting
 * job, not on the count: 10,000 jobs that are 2 seconds old are fine.
 *
 * It reads pg-boss's tables directly, as the database owner. Never from a
 * request: job payloads of every org are in there.
 */
export type QueueRow = { queue: string; waiting: number; deferred: number; active: number; failed: number; oldestWaitingSec: number | null };
export type RetryingJob = { queue: string; id: string; attempt: number; of: number; nextAttemptAt: Date; error: string | null; data: unknown };
export type DeadJob = { id: string; sourceQueue: string | null; sourceId: string | null; deadAt: Date; error: string | null; data: unknown };

export async function queueStatus(): Promise<{ queues: QueueRow[]; retrying: RetryingJob[]; dead: DeadJob[] }> {
  const db = (await getBoss()).getDb();
  const { rows: counts } = await db.executeSql(`
    select name,
      count(*) filter (where state in ('created', 'retry') and start_after <= now())::int as waiting,
      count(*) filter (where state in ('created', 'retry') and start_after > now())::int as deferred,
      count(*) filter (where state = 'active')::int as active,
      count(*) filter (where state = 'failed')::int as failed,
      extract(epoch from now() - min(start_after) filter (where state in ('created', 'retry') and start_after <= now()))::int as oldest
    from ${QUEUE_SCHEMA}.job group by name`);
  const byName = new Map(counts.map((r: { name: string }) => [r.name, r]));
  const queues = Object.keys(QUEUES)
    .filter((q) => q !== DEAD_LETTER)
    .map((queue) => {
      const r = byName.get(queue) as { waiting: number; deferred: number; active: number; failed: number; oldest: number | null } | undefined;
      return { queue, waiting: r?.waiting ?? 0, deferred: r?.deferred ?? 0, active: r?.active ?? 0, failed: r?.failed ?? 0, oldestWaitingSec: r?.oldest ?? null };
    });

  const { rows: retrying } = await db.executeSql(`
    select name, id, retry_count, retry_limit, start_after, output->>'message' as error, data
    from ${QUEUE_SCHEMA}.job where state = 'retry' order by start_after limit 50`);
  // A dead-lettered job keeps its payload; its error is on the original, failed job.
  const { rows: dead } = await db.executeSql(`
    select d.id, d.source_name, d.source_id, d.created_on, d.data, f.output->>'message' as error
    from ${QUEUE_SCHEMA}.job d
    left join ${QUEUE_SCHEMA}.job f on f.id = d.source_id and f.name = d.source_name
    where d.name = $1 and d.state in ('created', 'retry')
    order by d.created_on desc limit 50`, [DEAD_LETTER]);

  return {
    queues,
    retrying: retrying.map((r: Record<string, unknown>) => ({
      queue: r.name as string,
      id: r.id as string,
      attempt: (r.retry_count as number) + 1,
      of: (r.retry_limit as number) + 1,
      nextAttemptAt: new Date(r.start_after as string),
      error: r.error as string | null,
      data: r.data,
    })),
    dead: dead.map((r: Record<string, unknown>) => ({
      id: r.id as string,
      sourceQueue: r.source_name as string | null,
      sourceId: r.source_id as string | null,
      deadAt: new Date(r.created_on as string),
      error: r.error as string | null,
      data: r.data,
    })),
  };
}

/** Put dead-lettered jobs back on their original queue (after fixing the cause). */
export async function redriveDeadLetters(sourceQueue?: string): Promise<number> {
  const boss = await getBoss();
  return boss.redrive(DEAD_LETTER, sourceQueue ? { sourceName: sourceQueue } : {});
}
