# Deploying Beacon

Lesson 7.4. How Beacon gets from a pull request to production, in small, reversible steps.

## Four environments

| Environment | Database | Configuration | How it is created |
|---|---|---|---|
| Local | `docker compose up -d` (Postgres, Mailpit), seeded by `npm run db:seed` | `.env.local` (scripts read it too) | by hand |
| Preview (per PR) | a fresh, seeded throwaway Postgres (or a Neon branch), never production data | `APP_ENV=preview` | `.github/workflows/deploy.yml` → `preview` |
| Staging | its own database with synthetic or anonymised data | `APP_ENV=staging` | on every push to `main` |
| Production | the real one, with point-in-time recovery | `APP_ENV=production` | the SAME image as staging, promoted |

Everything that differs between them is an environment variable, checked when a process starts
(`src/lib/env.ts`; the list is `docs/configuration.md`, generated from the schema). A missing `DATABASE_URL` stops the
web app, the worker and the migrations with a message that names it. `APP_ENV=production` also refuses
development-only settings (`BILLING_PROVIDER=fake`, a non-empty `OUTBOUND_ALLOWLIST`, no `BETTER_AUTH_SECRET`, no
`ENCRYPTION_KEYS`: lesson 8.1, docs/security/secrets.md).

**Preview environments.** Each PR gets its own URL and its own database: run the PR's image with `migrate`, then
`seed` (`NODE_ENV=development` for that one container: the seed refuses production), then `web` and `worker`. Give it
`BILLING_PROVIDER=fake`, `EMAIL_DRIVER=console` and no customer data. Vercel, Render and Railway do this for you;
the workflow shows the steps for a platform that does not. Tear it down when the PR closes.

## One image, built once, promoted

`Dockerfile`: a multi-stage build. The final stage has production dependencies only (`npm ci --omit=dev`), the
Next.js build, the worker and CLIs bundled to plain JavaScript (`npm run build:scripts`, so `tsx` is not needed), the
SQL migrations, no `.env` file (`.dockerignore`), and runs as uid 1000, not root. One image, three commands:

```bash
docker build --build-arg GIT_SHA=$(git rev-parse HEAD) -t beacon:$(git rev-parse --short HEAD) .
docker run … beacon:abc1234                                   # web: next start (the default)
docker run … beacon:abc1234 node dist/scripts/worker.mjs      # the worker
docker run … beacon:abc1234 node dist/scripts/migrate.mjs     # the release step
```

`GIT_SHA` becomes `APP_RELEASE` (logs, traces and errors say which release) and `NEXT_PUBLIC_APP_RELEASE` (browser
errors). With the `sentry_auth_token` build secret, the build uploads the browser source maps to Sentry for that
release and then deletes them from the image.

CI (`.github/workflows/ci.yml`) lints, typechecks, tests, applies the migrations to a real Postgres, builds, lints the
Dockerfile with hadolint, builds the image tagged with the SHA (pushed to GHCR on `main`) and checks that it runs as
uid 1000 with no dev dependencies or `.env` files. The deploy workflow resolves that tag to its **digest** and deploys
the digest to staging and then production: what was tested is byte for byte what runs.

Verification in the course sandbox: there is no Docker daemon there, so the image was not built. The Dockerfile passes
hadolint, and its runtime stage was reproduced by hand: a directory with only `npm ci --omit=dev`, `.next`, `dist`,
`drizzle`, `package.json` and `next.config.ts` served `/api/health` and `/api/ready` with `next start`, ran the bundled
worker and migrations, and exited with the configuration error when `DATABASE_URL` was removed.

## The release step: migrations before code

`node dist/scripts/migrate.mjs` (`npm run db:migrate` locally) applies the SQL migrations and installs the job queue's
schema. It runs **once per deploy, before the new code starts**: the `migrate` one-shot service in
`docker-compose.prod.yml` (web and worker wait for it to complete successfully), a PaaS "release command", or the
`staging`/`production` jobs of the deploy workflow. Never on every web instance's boot: ten instances would race.

Because old and new code run side by side during a rolling deploy, every migration must keep the **currently running**
code working. Renames and type changes are three deploys: **expand, migrate, contract**. The lesson's example, renaming
`monitors.url` to `monitors.target` (planned here, not performed: the course keeps `url`):

| Deploy | Migration (runs first) | Code |
|---|---|---|
| 1. expand | `ALTER TABLE monitors ADD COLUMN target text;` (nullable, instant) | writes `url` AND `target`, reads `url` |
| 2. migrate | a job backfills in batches: `UPDATE monitors SET target = url WHERE id IN (SELECT id FROM monitors WHERE target IS NULL LIMIT 1000)`, repeated; then `ALTER TABLE monitors ALTER COLUMN target SET NOT NULL` | reads `target`, still writes both |
| 3. contract | `ALTER TABLE monitors DROP COLUMN url;` (no running code uses it) | uses `target` only |

Batching keeps each `UPDATE` short (no long lock on the table); `lock_timeout` in `scripts/migrate.ts` makes a
migration that would wait on a lock fail fast instead of freezing every query behind it. Migration 0024 of this module
is additive only (new tables, nullable columns, indexes), so it deploys in one step.

## Zero-downtime details

- **Readiness before traffic.** A new instance gets traffic only once `/api/ready` answers 200.
- **Draining.** `SIGTERM` → Next.js finishes in-flight requests; the worker stops claiming jobs and gives running ones
  20 seconds (`stopBoss`), anything unfinished is retried by another worker (queues deliver at least once, every
  handler is idempotent). The Dockerfile's `CMD` is exec form so the process receives the signal.
- **Rollback** = deploy the previous digest. Only additive migrations make that safe, which is the other reason for
  expand/contract.

## Where to run it

Beacon's shape (a web app, workers, one Postgres) fits a PaaS (Render, Railway, Fly.io) or a few VMs with Kamal or
Coolify; Kubernetes only when a concrete need forces it. The checkers are the part that may one day need several
regions (a check from Europe and one from Asia are different product features): they are stateless, pull jobs and
push results, so they can run anywhere near Postgres, labelled with `CHECK_REGION`.

See also: [self-hosting.md](self-hosting.md) (one machine, Docker Compose), [backup-and-restore.md](backup-and-restore.md)
(backups and the restore drill), [operations.md](operations.md) (health checks, SLO, alerts, runbooks).
