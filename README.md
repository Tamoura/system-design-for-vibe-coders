# Beacon

**Uptime monitoring and public status pages for teams. It is also the practice project for the
[SaaS Building Blocks](https://tamoura.github.io/system-design-for-vibe-coders/saas/) course.**

Beacon checks your URLs on a schedule, opens an incident when they fail, and keeps a public status page
up to date. That is the product, the part a customer pays for. It is also only about 15% of a real SaaS.
The other 85% is the machinery every SaaS shares: accounts, organizations, roles, billing, email, jobs,
an API, webhooks, an audit log, SSO. The course teaches those components one lesson at a time, and this
repo is where you build them.

## Get the code

Beacon lives inside the course repository,
[Tamoura/system-design-for-vibe-coders](https://github.com/Tamoura/system-design-for-vibe-coders), as a set of
branches whose root *is* the Beacon project. Clone just the starter as a standalone repo:

```bash
git clone -b beacon/starter --single-branch https://github.com/Tamoura/system-design-for-vibe-coders.git beacon
cd beacon
```

Fetch a solution when you want it:

```bash
git fetch origin beacon/module-2-solution:module-2-solution
git diff main module-2-solution
```

In the table below, `main` means your local `main`, which is `beacon/starter`, and `module-N-solution` is the
remote branch `beacon/module-N-solution`. A copy of the starter is also in the course repo's
[`beacon/`](https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/beacon) folder, for browsing.

## How this repo works

| Branch | What it contains |
|---|---|
| `main` | **The starter.** The core product works: monitors, checks, incidents, dashboard, status page. Every generic SaaS component is missing and marked with a `TODO(lesson)` comment. Start here. |
| `module-1-solution` | Identity & access: authentication, organizations and invitations, roles and permissions |
| `module-2-solution` | Data: migrations and tenant scoping, logo uploads, search, row-level security |
| `module-3-solution` | Money: Stripe checkout and webhooks, plans and limits, SMS usage metering |
| `module-4-solution` | Communication: transactional email, incident notifications with preferences, live dashboard |
| `module-5-solution` | Background work: the check scheduler and workers, public API with keys, outbound webhooks |
| `module-6-solution` | Product: onboarding and settings, analytics events, feature flags |
| `module-7-solution` | Operations: admin panel, structured logging, audit log, Docker and deploy |
| `module-8-solution` | Trust: security headers and secrets hygiene, AI incident summaries |
| `module-9-solution` | Capstone: architecture diagram and decision records |

Each solution branch builds on the one before it, so `module-5-solution` also contains modules 1–4.
The solutions cover the 🟢 Beginner and 🟡 Intermediate exercises. The 🔴 Advanced exercises are stretch
goals with no solution, on purpose.

**Try each exercise before you look at the solution.** When you do look, read the diff for that module
only:

```bash
git diff module-2-solution module-3-solution
```

All exercises, copied from the course with their "done when" criteria, are in
[docs/EXERCISES.md](docs/EXERCISES.md).

## Run it

You need Node 22+ and Docker.

```bash
cp .env.example .env.local    # then set BETTER_AUTH_SECRET (openssl rand -base64 32)
docker compose up -d          # Postgres on :5432, Mailpit on :8025
npm install
npm run db:migrate
npm run db:seed               # "demo" org: an owner, a member, five monitors, a day of checks
npm run dev                   # http://localhost:3000
```

`npm run db:reset` does the last three database steps in one go on a local database (it drops everything
first). Sign in as `demo@beacon.test` (owner) or `member@beacon.test` (member), password
`beacon-demo-password`, or sign up. Uploaded files go to `.storage/` unless you configure an S3-compatible
bucket (`STORAGE_DRIVER=s3` in `.env.example`). Every email Beacon sends (verification, password reset,
invitations, incident alerts) lands in Mailpit at <http://localhost:8025>. No Docker? Start the app with
`EMAIL_DRIVER=console` and emails are printed in the terminal instead.
"Sign in with GitHub" appears when `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` are set.

In a second terminal, start the worker. It checks every monitor on its schedule (each monitor at its own
second of its interval, lesson 5.1), sends the queued emails, SMS, Slack messages and webhooks, and runs the
escalation workflows:

```bash
npm run worker
```

An incident opens after three failures in a row (lesson 4.2) and notifies the team: a notification behind the
🔔 and an email in Mailpit. The seed's "Always broken" monitor already has an open incident; click **Mark
resolved** on its page (that notifies too), wait for its next check, and a new incident opens. Its URL is on
`localhost`, so its check fails with "Blocked: … loopback address": the SSRF guard (lesson 5.3) refuses
internal addresses, and `OUTBOUND_ALLOWLIST` in `.env.example` lets `localhost:3000` through for "Beacon
itself" in development. Start the app with `SMS_PROVIDER=fake` to see SMS alerts (set a phone number under
🔔 → Preferences) printed and metered. `npm run checks:run -- --all` checks every monitor now instead of
waiting, and `npm run jobs` shows the queues: what is waiting, what is being retried and why, and the
dead letters.

Module 5 adds what other software uses to reach Beacon: **Settings → API keys** for the public API
(`/api/v1`, reference at <http://localhost:3000/docs/api>; the API is part of the Business plan, so put the
demo org on it with `update organizations set plan = 'business' where slug = 'demo'`), **Settings →
Webhooks** for signed incident events, and **Settings → Escalation policy**. See
[docs/SOLUTIONS.md](docs/SOLUTIONS.md#module-5--background-work--integrations).

Module 6 adds the parts customers see first. `/` and `/pricing` are the **marketing site** (static, the pricing
cards drawn from the plans config); the app has a **sidebar shell** with an org switcher, settings split into
organization, billing, alerts and developer sections (your own account is at `/settings/account`), and a
**Getting started** checklist for new organizations. Product events (`monitor_created`, …) are recorded
server-side in `analytics_events`, and feature flags are evaluated per organization (**/internal/flags**,
**/internal/analytics**, or `npm run flags`). See [docs/SOLUTIONS.md](docs/SOLUTIONS.md#module-6--product--growth).

Module 7 is what running Beacon needs. **Staff** are a separate table with staff roles: sign in as
`staff@beacon.test` (superadmin), `support@beacon.test` or `billing@beacon.test` (same password) and open
**/internal**, the admin panel: find a customer by part of an email, see plan and usage, extend a trial, comp a
plan, resend an invitation, and view an account **read-only for 30 minutes** (a red banner, and an entry in the
customer's own audit log). Every sensitive change is written to the **audit log** in its own transaction
(**Organization → Audit log** on Pro and Business, with filters and CSV export). Logs are **JSON lines** with a
request id and the org on every line (`npm run dev | npx pino-pretty` to read them), `/api/health` and `/api/ready`
answer probes, and OpenTelemetry traces and metrics go to a collector when `OTEL_EXPORTER_OTLP_ENDPOINT` is set
(`docker-compose.observability.yml`). The **Dockerfile** builds one image for the web app, the worker and the
migrations; `docker-compose.prod.yml` runs Beacon in production shape, or self-hosted. `npm run staff` makes your own
account staff. See [docs/SOLUTIONS.md](docs/SOLUTIONS.md#module-7--operating-the-saas), and
[deployment](docs/deployment.md), [operations](docs/operations.md), [self-hosting](docs/self-hosting.md),
[backups](docs/backup-and-restore.md), [configuration](docs/configuration.md).

Module 8 is trust. Every response carries **security headers** and a **Content-Security-Policy** with a fresh nonce
(`curl -I localhost:3000/status/demo`); `/.well-known/security.txt` and a **/trust** page list how to report a
vulnerability and every subprocessor. Webhook signing secrets and Slack URLs are **encrypted at rest** (envelope
encryption, `ENCRYPTION_KEYS`, `npm run secrets` to rotate); sign-in is throttled per account and per IP. Each user can
**download their data** and **delete their account** (Account settings); owners can **export** or **delete** the whole
organization (Settings → Data & privacy), and a nightly job enforces the retention table. On Business, **AI incident
summaries** (Settings → AI summaries, off by default) draft a status-page update when an incident resolves, for a person
to edit and publish; without `ANTHROPIC_API_KEY` a built-in fake provider writes them. `npm run ai:eval` runs the eval.
`npm run hooks:install` once per clone runs gitleaks before every commit. See
[docs/SOLUTIONS.md](docs/SOLUTIONS.md#module-8--trust--the-frontier) and [docs/security/](docs/security/threat-model.md).

Billing (Module 3) is off until you configure it. To try upgrades without a Stripe account, start the app
with `BILLING_PROVIDER=fake npm run dev`: "Upgrade" then opens a stand-in Checkout page inside Beacon and
a signed webhook follows. For real Stripe test mode (test keys, `stripe listen`), see
[docs/SOLUTIONS.md](docs/SOLUTIONS.md#module-3--money).

| Command | What it does |
|---|---|
| `npm test` | Tests (Vitest). No database server needed: database tests run the migrations on an in-memory Postgres (PGlite). |
| `npm run typecheck` | TypeScript, strict mode. |
| `npm run db:generate` | Create a new migration after you edit `src/db/schema.ts`. |
| `npm run db:reset` | Drop, migrate and seed a local database. Refuses anything but localhost. |
| `npm run db:seed:large` | Org `big` with 500 monitors × 1,000 checks, for measuring queries (`-- --monitors=50000 --checks=0` for search). |
| `npm run worker` | The background worker (lesson 5.1): the check scheduler, checks, emails, SMS, Slack, webhooks, thumbnails, usage reporting, workflows. Run one or more next to the app. |
| `npm run jobs` | The queues at a glance: waiting, oldest job, retries with their errors, dead letters. `-- redrive` puts dead letters back; `-- run` runs due jobs once without a worker. |
| `npm run checks:run` | Enqueue checks for monitors that are due now (`-- --all`: every running monitor). The worker also does this by itself. |
| `npm run usage:report` | Send recorded SMS usage to Stripe's meter (lesson 3.3). The worker does it every 5 minutes; safe to re-run. |
| `npm run openapi` | Regenerate `docs/openapi.json` from the API's Zod schemas (lesson 5.2). CI runs `npm run openapi:check`. |
| `npm run email:preview` | Render every email template (HTML and plain text) to `.email-preview/` (lesson 4.1). |
| `npm run storage:setup` | With `STORAGE_DRIVER=s3`: create the bucket, block public access, set CORS. |
| `npm run build` | Production build, the same one CI runs. |
| `npm run flags` | Feature flags (lesson 6.3): list them, `-- rollout <flag> 10`, `-- override <flag> <org> on`, `-- off <flag>` (the kill switch). |
| `npm run staff` | Beacon staff (lesson 7.1): list, `-- add <email> <support\|billing\|engineer\|superadmin> "<reason>"`, `-- remove <email> "<reason>"`. |
| `npm run audit -- verify` | Recompute every audit log hash chain (lesson 7.3); `-- purge` applies the retention now. The worker does both nightly. |
| `npm run env:docs` | Regenerate `docs/configuration.md` from the configuration schema (lesson 7.4). CI runs `npm run env:docs:check`. |
| `npm run build:scripts` | Bundle the worker, migrations and CLIs to `dist/scripts/*.mjs` for the production image (lesson 7.4). |
| `sh scripts/backup.sh` / `sh scripts/restore.sh` | A Postgres backup, and a restore into a scratch database for the drill (lesson 7.4). |
| `npm run secrets` | Encryption at rest (lesson 8.1): which key wraps each stored secret; `-- rotate` re-wraps them with the newest key in `ENCRYPTION_KEYS`; `-- generate-key`. |
| `npm run ai:eval` | The AI incident summary eval (lesson 8.2): 15 fixture incidents, five with prompt injections. The fake provider unless `ANTHROPIC_API_KEY` is set. |
| `npm run hooks:install` | Use `.githooks/` in this clone: gitleaks scans every commit for secrets (lesson 8.1). |
| `npm run org:claim -- <slug> <email>` | Make a user the owner of an org, e.g. the `default` org that migration 0003 creates for monitors from before Module 1. |

## Where things live

```
src/
  core/         Pure logic: run a check, decide incidents, validate input, roles and permissions. Fully tested.
  db/           Drizzle schema, the Postgres client, and withOrg() (row-level security, lesson 2.4).
  lib/          Data access used by pages and scripts. Every tenant query takes the organization.
  lib/storage/  Object storage behind one interface: S3-compatible or local files (lesson 2.2).
  lib/email/    sendEmail(): the queue, SMTP/Resend drivers, bounces and suppression (lesson 4.1).
  lib/notifications/  notify(): recipients, preferences, channels, delivery log (lesson 4.2).
  lib/queue/    The job queue (pg-boss): queues, enqueue(), handlers, the worker (lesson 5.1).
  lib/workflows/  A small durable-workflow engine and the escalation policy (lesson 5.4).
  lib/analytics/  track(): the tracking plan's events, server-side, forwarded to PostHog; the funnel (lesson 6.2).
  lib/flags/    isEnabled(): feature flags through OpenFeature, evaluated locally per org (lesson 6.3).
  lib/observability/  pino logs with the request context, OpenTelemetry traces and metrics, error tracking (lesson 7.2).
  lib/admin/    The admin panel's service side: customer search, support actions, staff roles, audit verifier (7.1, 7.3).
  lib/audit.ts  recordAudit(): the audit log, written in the transaction of the change (lesson 7.3).
  lib/secrets/  Envelope encryption of stored secrets behind a KMS interface; key rotation (lesson 8.1).
  lib/privacy/  GDPR: a person's export and account deletion, an org's export and deletion jobs, retention (lesson 8.1).
  lib/ai/       The AI gateway (providers: Claude via the Anthropic SDK, a fake), incident summaries (lesson 8.2).
  proxy.ts      Request ids, the read-only rule for staff impersonation, security headers and the CSP (7.1, 7.2, 8.1).
  emails/       React Email templates, each with a plain-text part (lesson 4.1).
  app/          Next.js App Router: (marketing)/ landing and pricing, (auth)/ and (site)/ sign-in and account
                pages, /[orgSlug]/… the app shell and org pages, /status/[slug], /internal/… (staff), /api/… (the
                dashboard's JSON), /api/v1/… (the public API, lesson 5.2), /docs/api.
scripts/        migrate, seed, reset, worker, jobs, run-checks, report-usage, openapi, email-preview, storage-setup, claim-org, flags,
                staff, audit, env-docs, build-scripts, secrets, ai-eval, backup.sh, restore.sh.
evals/          The AI summary eval's fixture incidents (lesson 8.2).
.githooks/      The pre-commit hook (gitleaks, lesson 8.1). `.gitleaks.toml`, `trivy.yaml`: the scanners' configuration.
ops/            The observability stack's configuration: OTel Collector, Prometheus alert rules (the SLO), Grafana (lesson 7.2).
drizzle/        SQL migrations (generated; commit them).
tests/          Vitest tests for src/core, and for src/lib and the API on an in-memory Postgres.
docs/           EXERCISES.md, SOLUTIONS.md (what each solution branch built and why), openapi.json and
                configuration.md (generated), operations, deployment, self-hosting and backup guides (module 7),
                security/ (threat model, secrets, privacy and retention: module 8), later the architecture docs (module 9).
```

To find where a lesson plugs in, search for its TODO:

```bash
grep -rn "TODO(1.2)" src scripts
```

## The stack, and why

| Choice | Why | Lesson |
|---|---|---|
| Next.js (App Router) + TypeScript | One language across UI, server and scripts, and the most common SaaS starter stack | 6.1 |
| PostgreSQL + Drizzle ORM | Postgres is the default SaaS database; Drizzle keeps SQL visible and migrations in the repo | 2.1 |
| Stripe (hosted Checkout, Customer Portal, Billing meters) | Card data never touches Beacon; a signed webhook keeps a copy of each subscription | 3.1 |
| Zod | One validation schema shared by forms (in the browser too) and the server, and the source of the OpenAPI document | 5.2, 6.1 |
| OpenFeature (with Beacon's own Postgres provider) | Vendor-neutral flag calls; swap in Unleash, Flagsmith or flagd without touching call sites | 6.3 |
| Vitest | Fast tests for the core logic | — |
| React Email + nodemailer (Resend in production) | Templates as components with a plain-text part; SMTP to Mailpit locally | 4.1 |
| pg-boss (a job queue in Postgres) | Jobs commit in the same transaction as the data; retries, cron, dead letters, per-tenant concurrency; no Redis to run | 5.1 |
| pino + OpenTelemetry (+ Sentry, optional) | JSON logs with request and tenant context; vendor-neutral traces and metrics; errors tagged with the release | 7.2 |
| Claude through the official Anthropic SDK, behind a small in-house gateway | One place for keys, fallbacks, caching, per-org limits and metering; the SDK's structured output with the same zod schemas | 8.2 |
| gitleaks, trivy, Dependabot | Secrets never land; known-vulnerable dependencies and images fail CI | 8.1 |
| Docker (one multi-stage image) and Compose | The same image in every environment; Postgres and Mailpit locally with one command | 7.4 |

The course names the Django, Rails, Laravel and Go equivalents for every component. The ideas carry over,
so port Beacon to your own stack if that is what your team uses.

## License

MIT. Copy anything you like into your own projects.
