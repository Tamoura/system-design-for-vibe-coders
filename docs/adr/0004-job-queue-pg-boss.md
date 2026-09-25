# ADR 0004: pg-boss for jobs and the scheduler; a small workflow engine on top

- **Status:** Accepted
- **Decided in:** `module-5-solution` (lessons 5.1 and 5.4)
- **Recorded:** Module 9, from docs/SOLUTIONS.md "Lesson 5.1" ("Why pg-boss") and "Lesson 5.4"

## Context

Beacon's core work happens when nobody is looking: checking every monitor on its schedule, and sending every email,
SMS, Slack message and webhook with retries. Until Module 5 these were `after()` callbacks and cron scripts that lost
work on a restart. The hard requirement: a notification job must exist **if and only if** the incident that caused
it committed. Escalation needs something that waits minutes for an acknowledgement without holding a worker.

## Decision

- **[pg-boss](https://github.com/timgit/pg-boss)** in its own `pgboss` schema. Queues as data with retries,
  exponential backoff with jitter and a dead-letter queue (`src/lib/queue/queues.ts`); `enqueueInTx()` inserts the
  job in the caller's transaction; `groupConcurrency` caps one org's jobs (5 checks per org at once,
  `src/lib/queue/worker.ts`); deterministic job ids make enqueueing idempotent.
- **The scheduler decides, the workers check:** one `checks.schedule` cron job per minute enqueues a `check.run` per
  monitor slot with a stable per-monitor phase (`src/lib/scheduler.ts`, `src/core/schedule.ts`).
- **Workflows:** a replay engine on the same queue, with runs, steps and stored signals in Postgres
  (`src/lib/workflows/engine.ts`); the incident fan-out and the escalation policy are workflows.

## Alternatives rejected

1. **Graphile Worker.** Also a Postgres queue with transactional enqueue, and faster at very high rates. pg-boss fit
   the exercises more directly: built-in dead-letter queues with redrive, per-tenant group concurrency in one option,
   a cron that takes a lock, and adapters for Drizzle (enqueue in our transaction) and PGlite (the real queue SQL
   runs in `npm test`).
2. **BullMQ on Redis, or Temporal / Inngest / Trigger.dev for workflows.** A second stateful system
   ([ADR 0001](0001-postgres-is-the-only-stateful-dependency.md)), and a Redis job cannot commit with a Postgres row,
   so every producer would need an outbox. The lesson's advice stands for production workflows: use an engine that
   already solved versioning and observability; Beacon's engine is short enough to read, which is its purpose here.

## Consequences

- The queue is the outbox: no relay, no "committed but never enqueued" window (tested).
- Handlers must be idempotent in three ways: deterministic ids, "only a pending row is sent", unique constraints on
  the effect. The row (email, delivery, webhook message) keeps the log; the queue owns retries.
- `beacon_app` may only insert jobs; the worker connects as the owner and scopes itself with `withOrg()` per job.
- The engine has no workflow versioning (rename a step and running workflows lose their place) and no dashboard
  beyond `npm run jobs` and the monitor page's run list.
- The core names each consumer of an incident (`src/lib/checks.ts`, `src/lib/monitors.ts`), not one event that
  consumers subscribe to (see "The event backbone" in `docs/architecture.md`).

## Revisit when

- `check.run` jobs pass **500 per second** sustained (about 30,000 one-minute monitors), or `pgboss.job` autovacuum
  falls behind → shard the scheduler (lesson 5.1 🔴) or move checks to a dedicated queue.
- A workflow must **change shape while runs are waiting**, or runs last **longer than a day** → Temporal or Inngest.
- A **fourth consumer** of incident events is added (after webhooks, notifications and escalation) → one
  `emitIncidentEventInTx(tx, event)` that owns the list, before writing the fourth call site.
- One org's checks are late while others are on time for **more than 5 minutes** → the per-org share cap (5.1 🔴).
