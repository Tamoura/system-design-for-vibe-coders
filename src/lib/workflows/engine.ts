import { and, asc, eq, inArray, sql } from 'drizzle-orm';
import { schema } from '@/db';
import { withOrg, type TenantTx } from '@/db/tenant';
import { enqueueInTx } from '../queue';
import type { JobContext } from '../queue/queues';

const { workflowRuns, workflowSteps, workflowSignals } = schema;

/*
 * Lesson 5.4: durable execution, small enough to read in one sitting.
 *
 * A workflow is an ordinary async function. Everything it does that touches
 * the world goes through `ctx`:
 *
 *   await ctx.step('notify-tier-0', () => page(tier))   run once; the RESULT is recorded
 *   await ctx.waitForSignal('wait-tier-0', [...], 5min) suspend until a signal or the deadline
 *
 * To run or resume, the engine calls the function FROM THE TOP (a
 * `workflow.run` job). Every step already in the history (workflow_steps)
 * returns its recorded result without running again; the first step that is
 * not there runs for real. So:
 *
 *   - a worker that dies after step 2 → the job is retried → steps 1 and 2 are
 *     replayed from the history (no second notification), step 3 runs;
 *   - a step that throws → the job is retried with backoff → only that step
 *     runs again (earlier ones are in the history);
 *   - a wait costs no worker: the job ends, and a delayed job (at the
 *     deadline) or a signal (enqueued at once) wakes the run.
 *
 * The rules this puts on workflow code (the lesson's "determinism"): no I/O,
 * clock or randomness outside steps; step names are stable (they are the
 * history's keys); steps are idempotent, because a crash between "done" and
 * "recorded" runs a step again.
 *
 * This is the lesson's model, built on the queue from 5.1 so you can see
 * every moving part. In production, prefer an engine that already solved
 * versioning, observability and scale: Temporal, Inngest, Trigger.dev,
 * Hatchet or DBOS (docs/SOLUTIONS.md, Module 5).
 */

export type Signal = { name: string; payload: unknown };

export type WorkflowContext = {
  runId: string;
  orgId: string;
  /** Run `fn` once, record its (JSON) result, and return the recorded result on every replay. */
  step<T>(name: string, fn: () => Promise<T>, input?: unknown): Promise<T>;
  /**
   * Wait until one of these signals arrives for this run, or `timeoutMs`
   * passes. Returns the signal, or null on timeout. The deadline is fixed
   * the first time the run gets here. A timeout of 0 only checks.
   */
  waitForSignal(name: string, signals: readonly string[], timeoutMs: number): Promise<Signal | null>;
};

const CLOCK_TOLERANCE_MS = 1000;

type WorkflowFn = (ctx: WorkflowContext, input: never) => Promise<unknown>;
const registry = new Map<string, WorkflowFn>();

export function defineWorkflow<I, O>(name: string, fn: (ctx: WorkflowContext, input: I) => Promise<O>) {
  registry.set(name, fn as WorkflowFn);
  return { name, fn };
}

/** Thrown inside a run to suspend it: caught by the engine, never by workflow code. */
class Suspend {
  constructor(
    readonly step: string,
    readonly until: Date,
  ) {}
}

/**
 * Start a run INSIDE the caller's transaction (it commits with the incident).
 * The key makes it idempotent: the same key twice is one run.
 */
export async function startWorkflowInTx(tx: TenantTx, orgId: string, workflow: string, key: string, input: object, subjectId?: string): Promise<string | null> {
  const [run] = await tx
    .insert(workflowRuns)
    .values({ organizationId: orgId, workflow, key, input, subjectId: subjectId ?? null })
    .onConflictDoNothing({ target: workflowRuns.key })
    .returning({ id: workflowRuns.id });
  if (!run) return null;
  await enqueueRun(tx, orgId, run.id, 'start');
  return run.id;
}

/**
 * One `workflow.run` job per wake-up. Its group is the RUN: the worker runs at
 * most one job of a run at a time, so a timer and a signal arriving together
 * cannot replay the same run in parallel.
 */
async function enqueueRun(tx: TenantTx, orgId: string, runId: string, reason: string, startAfter?: Date) {
  await enqueueInTx(tx, 'workflow.run', { orgId, runId }, { key: `${runId}:${reason}`, startAfter, group: runId });
}

/**
 * Deliver a signal to every active run with this subject (an incident): it is
 * stored (a run that reaches its wait later still sees it) and wakes them now.
 */
export async function signalRunsInTx(tx: TenantTx, orgId: string, subjectId: string, name: string, payload: unknown = null): Promise<number> {
  const runs = await tx
    .select({ id: workflowRuns.id })
    .from(workflowRuns)
    .where(and(eq(workflowRuns.organizationId, orgId), eq(workflowRuns.subjectId, subjectId), inArray(workflowRuns.status, ['running', 'waiting'])));
  for (const run of runs) {
    const [signal] = await tx.insert(workflowSignals).values({ organizationId: orgId, runId: run.id, name, payload }).returning({ id: workflowSignals.id });
    await enqueueRun(tx, orgId, run.id, `signal:${signal.id}`);
  }
  return runs.length;
}

/** The `workflow.run` job: replay the run from the top, as described above. */
export async function runWorkflow(orgId: string, runId: string, job: Pick<JobContext, 'lastAttempt'> = { lastAttempt: false }, now: () => Date = () => new Date()) {
  const loaded = await withOrg(orgId, async (tx) => {
    const [run] = await tx.select().from(workflowRuns).where(and(eq(workflowRuns.organizationId, orgId), eq(workflowRuns.id, runId)));
    if (!run) return null;
    const steps = await tx.select().from(workflowSteps).where(and(eq(workflowSteps.organizationId, orgId), eq(workflowSteps.runId, runId)));
    return { run, steps: new Map(steps.map((s) => [s.name, s])) };
  });
  if (!loaded || loaded.run.status === 'completed' || loaded.run.status === 'failed') return { status: loaded?.run.status ?? 'missing' };
  const { run, steps } = loaded;
  const fn = registry.get(run.workflow);
  if (!fn) throw new Error(`Unknown workflow "${run.workflow}"`);

  const saveStep = (name: string, values: Partial<typeof workflowSteps.$inferInsert>) =>
    withOrg(orgId, (tx) =>
      tx
        .insert(workflowSteps)
        .values({ organizationId: orgId, runId, name, status: 'running', ...values })
        .onConflictDoUpdate({ target: [workflowSteps.runId, workflowSteps.name], set: values }),
    );

  const ctx: WorkflowContext = {
    runId,
    orgId,
    async step(name, stepFn, input) {
      const recorded = steps.get(name);
      if (recorded?.status === 'completed') return recorded.output as never; // replay: no side effect
      const attempts = (recorded?.attempts ?? 0) + 1;
      await saveStep(name, { status: 'running', input: input ?? null, attempts, startedAt: now(), error: null });
      try {
        const output = await stepFn();
        await saveStep(name, { status: 'completed', output: (output ?? null) as object, finishedAt: now() });
        return output;
      } catch (err) {
        await saveStep(name, { status: 'failed', error: (err as Error).message.slice(0, 500), finishedAt: now() });
        throw err; // the job is retried; completed steps will be replayed, this one runs again
      }
    },
    async waitForSignal(name, names, timeoutMs) {
      const recorded = steps.get(name);
      if (recorded?.status === 'completed') return recorded.output as Signal | null;
      // The deadline is decided once and recorded: a replay tomorrow waits for the same moment.
      const wakeAt = recorded?.wakeAt ?? new Date(now().getTime() + timeoutMs);
      if (!recorded) await saveStep(name, { status: 'waiting', input: { signals: names, timeoutMs }, wakeAt, attempts: 1 });
      const [signal] = await withOrg(orgId, (tx) =>
        tx
          .select({ name: workflowSignals.name, payload: workflowSignals.payload })
          .from(workflowSignals)
          .where(and(eq(workflowSignals.organizationId, orgId), eq(workflowSignals.runId, runId), inArray(workflowSignals.name, [...names])))
          .orderBy(asc(workflowSignals.createdAt))
          .limit(1),
      );
      if (signal) {
        await saveStep(name, { status: 'completed', output: signal, finishedAt: now() });
        return signal;
      }
      // A second of tolerance: the wake-up job is due by the DATABASE's clock, this is ours.
      if (now().getTime() >= wakeAt.getTime() - CLOCK_TOLERANCE_MS) {
        await saveStep(name, { status: 'completed', output: null, finishedAt: now() });
        return null;
      }
      throw new Suspend(name, wakeAt);
    },
  };

  try {
    const output = await fn(ctx, run.input as never);
    await withOrg(orgId, (tx) =>
      tx
        .update(workflowRuns)
        .set({ status: 'completed', output: (output ?? null) as object, completedAt: now(), wakeAt: null, error: null })
        .where(and(eq(workflowRuns.organizationId, orgId), eq(workflowRuns.id, runId))),
    );
    return { status: 'completed', output };
  } catch (err) {
    if (err instanceof Suspend) {
      // Suspended: the job ends here and frees the worker. A delayed job wakes the run at the deadline.
      await withOrg(orgId, async (tx) => {
        await tx.update(workflowRuns).set({ status: 'waiting', wakeAt: err.until }).where(and(eq(workflowRuns.organizationId, orgId), eq(workflowRuns.id, runId)));
        await enqueueRun(tx, orgId, runId, `wake:${err.step}`, err.until);
      });
      return { status: 'waiting', step: err.step, until: err.until.toISOString() };
    }
    await withOrg(orgId, (tx) =>
      tx
        .update(workflowRuns)
        .set({ status: job.lastAttempt ? 'failed' : 'running', error: (err as Error).message.slice(0, 500) })
        .where(and(eq(workflowRuns.organizationId, orgId), eq(workflowRuns.id, runId))),
    );
    throw err;
  }
}

/** The runs about one subject (an incident), with their steps: the "dashboard" on the incident. */
export async function listRuns(orgId: string, subjectIds: string[]) {
  if (subjectIds.length === 0) return [];
  return withOrg(orgId, async (tx) => {
    const runs = await tx
      .select()
      .from(workflowRuns)
      .where(and(eq(workflowRuns.organizationId, orgId), inArray(workflowRuns.subjectId, subjectIds)))
      .orderBy(asc(workflowRuns.createdAt));
    const steps = runs.length
      ? await tx
          .select()
          .from(workflowSteps)
          .where(and(eq(workflowSteps.organizationId, orgId), inArray(workflowSteps.runId, runs.map((r) => r.id))))
          .orderBy(asc(workflowSteps.startedAt), asc(sql`${workflowSteps.createdAt}`))
      : [];
    return runs.map((r) => ({ ...r, steps: steps.filter((s) => s.runId === r.id) }));
  });
}
