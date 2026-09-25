# Operating Beacon: signals, SLO, alerts and runbooks

Lesson 7.2. What Beacon emits, the one objective it is held to, what pages a human, and what that human
does next. The alert rules are `ops/prometheus/alerts.yml`; the dashboard is `ops/grafana/dashboards/beacon.json`.

## The five signals

| Signal | Where it comes from | Where it goes |
|---|---|---|
| Logs | pino, JSON lines on stdout (`src/lib/observability/logger.ts`). Every line carries `requestId`; lines of an org's request or job also `orgId` and `userId`; lines inside a span `traceId`/`spanId`. Passwords, keys, tokens, cookies and `authorization` are redacted. | stdout → your platform's log store (Loki, Better Stack, CloudWatch). `… \| npx pino-pretty` to read locally. |
| Metrics | OpenTelemetry (`src/lib/observability/metrics.ts`): `http_server_requests_total`, `http_server_duration_seconds` (RED for the API), `jobs_total`, `job_duration_seconds` (RED for the worker), `checks_executed_total` and `check_lag_seconds` (Beacon's own health). Labels are closed sets: never an org id. | OTLP → collector → Prometheus (`docker-compose.observability.yml`). |
| Traces | OpenTelemetry: a SERVER span per API request, a PRODUCER span per enqueue, a CONSUMER span per job with the enqueue as parent (the trace context rides in the job payload, `_meta`), a CLIENT span per check. Next.js adds its own spans for pages and server actions. | OTLP → collector → Tempo. |
| Errors | `captureError()` (`src/lib/observability/errors.ts`): unexpected errors in API routes, pages and server actions (`onRequestError`), and a job's LAST failed attempt. Tagged with release, request id, org id, user id. | Sentry or GlitchTip when `SENTRY_DSN` is set; the error log line otherwise. |
| Outside probe | Beacon monitors itself (the seed's "Beacon itself" monitor on `/api/health`), and one probe that is NOT Beacon checks it from another provider. | A second provider's uptime check (Uptime Kuma on another cloud, or a managed service) that alerts through a different channel than Beacon's own. |

`/api/health` is liveness (the process answers; no database). `/api/ready` is readiness (Postgres answers and the
job queue's schema exists) and answers 503 with the failing check otherwise. A load balancer routes on `/api/ready`;
an orchestrator restarts on `/api/health`.

Try the stack: `docker compose -f docker-compose.observability.yml up -d`, then start the app and the worker with
`OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318`. Grafana on <http://localhost:3001> has the "Beacon" dashboard
(check lag p50/p95/p99 per region, checks per second, RED for the API, jobs by outcome). Stop the worker and watch
check lag and "checks executed" react within a minute or two. Without Docker, `OTEL_EXPORTER=console` prints spans and
metrics to stdout. (The stack's configuration is written for current image versions but was not run in the course
sandbox, which has no Docker daemon.)

## The SLO

**"Checks on time": 99.9% of scheduled checks start within 15 seconds of their slot, measured over 30 days.**

- SLI: `check_lag_seconds` (the time from a check's scheduled slot to the moment the worker starts it), the share of
  observations with lag ≤ 15 s.
- Error budget: 0.1% of checks may be late, about 43 minutes' worth of every check being late per month.
- Why this SLI: a late check is a late alert, which is the thing a monitoring customer pays us not to do. Every HTTP
  endpoint can be green while the scheduler skips monitors or the workers fall behind; this number is not.

| Alert | Condition | Severity | Meaning |
|---|---|---|---|
| `CheckLagBudgetFastBurn` | bad ratio > 14.4 × 0.1% over 1 h AND over 5 min | page | 2% of the month's budget burned in an hour |
| `CheckLagBudgetSlowBurn` | bad ratio > 6 × 0.1% over 6 h AND over 30 min | page | 5% of the budget in 6 hours |
| `CheckLagBudgetTicket` | bad ratio > 0.1% over 3 d AND over 6 h | ticket | steady, slow erosion |
| `NoChecksExecuted` | no check at all for 10 minutes | page | the scheduler or every worker is down (nothing is late because nothing runs) |
| `ApiErrorRateHigh` | > 5% 5xx on a route for 10 minutes | page | customers see errors |
| `JobsDeadLettering` | > 20 failed jobs of a queue in 30 minutes | ticket | a provider or a customer endpoint keeps failing |
| `AuditChainBroken` | the nightly `audit.verify` job failed | page | an audit event was changed or deleted outside the app |

Rules for alerts, from the lesson: page only on symptoms a customer feels, with a runbook; delete or downgrade an alert
that fired without anyone needing to act, the same week. The rules were written for Prometheus 2.x but not loaded into
a Prometheus in the sandbox (no `promtool`): run `promtool check rules ops/prometheus/alerts.yml` before relying on them.

## Runbook: checks are late

*Fires as `CheckLagBudgetFastBurn`, `CheckLagBudgetSlowBurn` or `NoChecksExecuted`.*

1. **Is the worker running?** `npm run jobs` (or the dashboard's "Jobs by queue"). No `checks.schedule` completed in the
   last two minutes: every worker is down or cannot reach Postgres. Restart it; check its logs for `worker.started`.
2. **Is it running but behind?** `check.run` jobs piling up in `created` with `start_after` in the past: not enough
   workers. Scale out (`docker compose -f docker-compose.prod.yml up -d --scale worker=3`, or your platform's scale
   command). Check lag should fall within one interval.
3. **Is one org hogging it?** Lag high for everyone while one org has thousands of monitors: the per-org cap
   (`groupConcurrency` in `src/lib/queue/worker.ts`) is doing its job; add workers.
4. **Is Postgres slow?** `/api/ready` slow or 503, the database's CPU pegged: find the slow query
   (`pg_stat_statements`), not the worker.
5. **After a deploy?** Roll back to the previous image (the deploy workflow keeps the previous digest), then look.
6. Write down what happened (a blameless postmortem) and how much budget it cost.

## Runbook: API errors

*`ApiErrorRateHigh`.* Open the error tracker filtered by the route and the release: an error that started with the
current release → roll back. Otherwise search the logs for `"level":"error"` and the route, pick a `requestId`, and
follow it (the same id is on every line of the request and on the jobs it enqueued). `/api/ready` 503 → the database.

## Runbook: jobs failing

*`JobsDeadLettering`.* `npm run jobs` lists retries with their last error and the dead letters. A provider outage
(email, SMS, Slack) recovers by itself thanks to retries with backoff; after the provider is back,
`npm run jobs -- redrive` puts dead letters back. One customer's webhook endpoint failing is theirs to fix (Beacon
disables it after five days and emails their admins).

## Runbook: audit chain broken

*`AuditChainBroken`.* Somebody changed or deleted an audit row outside the app (the app role cannot), or a bug wrote a
row the verifier cannot reproduce. `npm run audit -- verify <org-slug>` names the first rows that fail. Treat it as a
security incident until proven otherwise: who had database access at that time (the database's own audit log,
pgaudit)? Do not "fix" the rows; the break is the evidence.
