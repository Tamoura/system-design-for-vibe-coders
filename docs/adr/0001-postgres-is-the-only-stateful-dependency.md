# ADR 0001: Postgres is the only stateful dependency

- **Status:** Accepted
- **Decided in:** Modules 1–8, one component at a time (first stated for the queue in lesson 5.1); recorded in Module 9
- **Applies to:** the queue, real-time, rate limits, feature flags, search, presence, product analytics, the AI cache

## Context

Beacon is run by a two-person team (and by every student who clones it). Each extra stateful system is one more
thing to provision, back up, secure, monitor and restore in a drill. The course repo also has to run its whole test
suite with no servers: the tests run the real migrations on PGlite, an in-memory Postgres (`tests/helpers/test-db.ts`).
And most of Beacon's reactions to a change must happen *if and only if* the change commits (an incident and its
notification job, a monitor and its audit event).

## Decision

Every piece of state lives in the one Postgres database, behind a small function that names what it does, so that
moving one concern to a dedicated system later is a driver change:

| Concern | In Postgres as | The function to swap |
|---|---|---|
| Jobs, cron, dead letters | pg-boss's `pgboss` schema ([ADR 0004](0004-job-queue-pg-boss.md)) | `enqueue()` / `enqueueInTx()` in `src/lib/queue/index.ts` |
| Real-time fan-out | `LISTEN/NOTIFY`, presence rows | `publishInTx()` / `subscribe()` in `src/lib/realtime.ts` |
| Rate limits, sign-in throttle | `rate_limit_buckets`, one row lock per decision | `consumeRateLimit()` in `src/lib/rate-limit.ts` |
| Feature flags | two tables behind an OpenFeature provider | `setProvider()` in `src/lib/flags/index.ts` |
| Search | `pg_trgm` and `tsvector` | `src/lib/search.ts` |
| Product analytics | `analytics_events`, forwarded to PostHog by a job | `src/lib/analytics/drivers.ts` |

Files are the exception: bytes go to an S3-compatible bucket, never into Postgres (lesson 2.2).

## Alternatives rejected

1. **Redis next to Postgres** (BullMQ, Redis pub/sub, Redis rate limiters: the lessons' usual defaults). A second
   system to run and persist, and a job enqueued in Redis cannot commit with the Postgres row it is about, so every
   producer would need an outbox table and a relay.
2. **A dedicated service per concern** (Meilisearch for search, Unleash for flags, ClickHouse for events). Each is
   better at its job at scale; at Beacon's size each is an operational cost with no user-visible gain, and none runs
   inside `npm test`.

## Consequences

- One backup and one restore drill cover everything (`docs/backup-and-restore.md`); one `withOrg()` covers tenancy.
- Transactional side effects everywhere: a rolled-back change leaves no job, no NOTIFY, no event.
- Postgres is also the single bottleneck and the single blast radius. Known limits, written where they bite:
  a notifying commit takes a global lock (`src/lib/realtime.ts`); `LISTEN` needs a session connection, not
  PgBouncer in transaction mode; a hot rate-limit row serializes its requests.
- **How to predict the next choice:** a new stateful concern goes into Postgres first, behind one function, unless
  one of the triggers below is already true for it.

## Revisit when

- Commits that `NOTIFY` exceed **500 per second** sustained, or the app needs more than **20 instances** each holding a
  `LISTEN` connection → Redis pub/sub or Centrifugo behind `publishInTx()` / `subscribe()`.
- `consumeRateLimit()` p95 exceeds **5 ms**, or public API traffic passes **200 requests per second** → Redis buckets.
- Monitor search on the busiest org exceeds **150 ms** p95 (lesson 2.3's target) → Typesense or Meilisearch with an outbox.
- Queue tables are among the **top 3 tables by write volume** while primary CPU stays above **60%** → see ADR 0004.
