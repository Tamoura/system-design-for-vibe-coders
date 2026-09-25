# ADR 0009: pino and OpenTelemetry for operators; a hash-chained audit log for customers

- **Status:** Accepted
- **Decided in:** `module-7-solution` (lessons 7.1, 7.2, 7.3); envelope encryption in `module-8-solution` (8.1)
- **Recorded:** Module 9, from docs/SOLUTIONS.md "Module 7" and "Lesson 8.1"

## Context

Two different audiences ask "what happened?". Operators need to explain any request or job: which org, how slow,
which error, which job it caused. Customers (and their auditors) need evidence of who changed what in their org,
including Beacon staff acting on their behalf. Logs are the wrong tool for the second: they are sampled, rotated,
lossy, and not written in the transaction of the change.

## Decision

- **Operators:** pino JSON logs with `requestId`, `orgId`, `userId`, `jobId` and trace ids added by a mixin from one
  AsyncLocalStorage context, secrets redacted at any depth (`src/lib/observability/logger.ts`,
  `src/lib/observability/context.ts`); OpenTelemetry traces and metrics over OTLP to any collector, the trace context
  carried in job payloads (`src/lib/observability/telemetry.ts`, `src/lib/queue/index.ts`); Sentry only when
  `SENTRY_DSN` is set. One SLO, "checks on time", with burn-rate alerts (`ops/prometheus/alerts.yml`,
  `docs/operations.md`). Metric labels never contain an org id.
- **Customers:** `recordAudit(tx, event)` in the transaction of every sensitive change (`src/lib/audit.ts`), a typed
  registry of actions and a refusal of anything that looks like a secret (`src/core/audit.ts`), append-only by grant,
  a hash chain per org verified nightly, retention by plan, CSV export. Staff act through the same service functions
  and are shown to the customer as "Beacon support".

## Alternatives rejected

1. **A vendor's agent and SDK throughout (Datadog, New Relic).** Call sites would be tied to one vendor; with
   OpenTelemetry the backend is a configuration choice (Grafana stack locally, Honeycomb or Grafana Cloud later).
2. **Audit from database triggers, change-data capture, or the logs.** Triggers and CDC see rows, not intent: no
   actor, IP, reason or "on behalf of"; logs are not transactional. The audit event commits with the change or not at all.

## Consequences

- One request id ties the browser's response header, every log line, the job it enqueued and the audit event.
- The audit log only covers what service functions record: a person **resolving an incident by hand** is on the
  incident's timeline but not in the audit log (finding A11 in `docs/readiness-review.md`).
- Retention deletes the oldest events; the verifier trusts the first remaining hash. Hashes are not anchored to
  write-once storage, so a database owner could rewrite the whole chain undetected.
- Secrets Beacon must read back use envelope encryption behind a `Kms` interface with only a local driver
  (`src/lib/secrets/kms.ts`); keys come from `ENCRYPTION_KEYS`.
- **How to predict the next choice:** a new sensitive action is an entry in `AUDIT_ACTIONS` and a `recordAudit()`
  call inside the service function's transaction, never in the route.

## Revisit when

- Log volume passes **20 GB a day** or observability spend passes **10% of hosting** → tail sampling, a cheaper backend.
- A customer asks for **audit streaming to their SIEM** → a stream consumer of `audit_events` (lesson 7.3 🔴).
- `audit_events` passes **50 million rows** → monthly partitions.
- The first **SOC 2 Type II** window starts → anchor the chain heads to object storage with a retention lock, staff
  SSO with MFA, and a cloud KMS driver.
