import { sql } from 'drizzle-orm';
import { db } from '@/db';
import { QUEUE_SCHEMA } from './queue/install';

/*
 * Lesson 7.4: what "ready" means for Beacon. Each check has a deadline: a
 * readiness probe that hangs is worse than one that says no.
 */
export type Readiness = { status: 'ready' | 'not_ready'; checks: Record<string, { ok: boolean; ms: number; error?: string }> };

const TIMEOUT_MS = 2000;

async function timed(fn: () => Promise<unknown>) {
  const started = performance.now();
  try {
    await Promise.race([fn(), new Promise((_, reject) => setTimeout(() => reject(new Error(`timed out after ${TIMEOUT_MS} ms`)), TIMEOUT_MS))]);
    return { ok: true, ms: Math.round(performance.now() - started) };
  } catch (err) {
    return { ok: false, ms: Math.round(performance.now() - started), error: (err as Error).message };
  }
}

export async function checkReadiness(): Promise<Readiness> {
  const [database, queue] = await Promise.all([
    // The database answers.
    timed(() => db.execute(sql`select 1`)),
    // The queue's tables exist (npm run db:migrate installed them) and can be read.
    timed(() => db.execute(sql.raw(`select count(*) from ${QUEUE_SCHEMA}.queue`))),
  ]);
  const checks = { database, queue };
  return { status: Object.values(checks).every((c) => c.ok) ? 'ready' : 'not_ready', checks };
}
