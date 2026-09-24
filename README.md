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

In a second terminal, run the checks. On `main` this is a one-shot script, and lesson 5.1 turns it into
a real scheduler:

```bash
npm run checks:run -- --all
```

An incident opens after three failures in a row (lesson 4.2) and notifies the team: a notification behind the
🔔 and an email in Mailpit. The seed's "Always broken" monitor already has an open incident; click **Mark
resolved** on its page (that notifies too), run the checks again, and a new incident opens. Start the app with
`SMS_PROVIDER=fake` to see SMS alerts (set a phone number under 🔔 → Preferences) printed and metered.
Without `--all` it checks only the monitors that are due (their interval, never shorter than the plan's
minimum, has passed), which is what cron should run every minute.

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
| `npm run files:process` | Finish uploads whose background thumbnail job never ran. |
| `npm run usage:report` | Send recorded SMS usage to Stripe's meter (lesson 3.3). Safe to re-run. |
| `npm run messages:send` | Send queued emails and notifications that are due, including retries after a provider outage (lessons 4.1, 4.2). Run it from cron. |
| `npm run email:preview` | Render every email template (HTML and plain text) to `.email-preview/` (lesson 4.1). |
| `npm run storage:setup` | With `STORAGE_DRIVER=s3`: create the bucket, block public access, set CORS. |
| `npm run build` | Production build, the same one CI runs. |
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
  emails/       React Email templates, each with a plain-text part (lesson 4.1).
  app/          Next.js App Router: auth pages, /[orgSlug]/… org pages, /status/[slug], /api/….
scripts/        migrate, seed, reset, run-checks, process-files, send-messages, email-preview, storage-setup, claim-org.
drizzle/        SQL migrations (generated; commit them).
tests/          Vitest tests for src/core, and for src/lib and the API on an in-memory Postgres.
docs/           EXERCISES.md, SOLUTIONS.md (what each solution branch built and why), later the architecture docs (module 9).
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
| Zod | One validation schema shared by forms and, later, the public API | 5.2 |
| Vitest | Fast tests for the core logic | — |
| React Email + nodemailer (Resend in production) | Templates as components with a plain-text part; SMTP to Mailpit locally | 4.1 |
| Docker Compose | Postgres and Mailpit locally with one command | 7.4 |

The course names the Django, Rails, Laravel and Go equivalents for every component. The ideas carry over,
so port Beacon to your own stack if that is what your team uses.

## License

MIT. Copy anything you like into your own projects.
