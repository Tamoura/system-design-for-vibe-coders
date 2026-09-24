# Beacon

**Uptime monitoring and public status pages for teams. It is also the practice project for the
[SaaS Building Blocks](https://tamoura.github.io/system-design-for-vibe-coders/saas/) course.**

Beacon checks your URLs on a schedule, opens an incident when they fail, and keeps a public status page
up to date. That is the product, the part a customer pays for. It is also only about 15% of a real SaaS.
The other 85% is the machinery every SaaS shares: accounts, organizations, roles, billing, email, jobs,
an API, webhooks, an audit log, SSO. The course teaches those components one lesson at a time, and this
repo is where you build them.

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
cp .env.example .env.local
docker compose up -d          # Postgres on :5432, Mailpit on :8025
npm install
npm run db:migrate
npm run db:seed               # three sample monitors
npm run dev                   # http://localhost:3000
```

In a second terminal, run the checks. On `main` this is a one-shot script, and lesson 5.1 turns it into
a real scheduler:

```bash
npm run checks:run
```

Run it twice. One of the seed monitors always fails, and an incident opens after two failures in a row.

| Command | What it does |
|---|---|
| `npm test` | Unit tests (Vitest). No database needed. |
| `npm run typecheck` | TypeScript, strict mode. |
| `npm run db:generate` | Create a new migration after you edit `src/db/schema.ts`. |
| `npm run build` | Production build, the same one CI runs. |

## Where things live

```
src/
  core/         Beacon's own logic: run a check, decide incidents, validate input. No I/O, fully tested.
  db/           Drizzle schema and the Postgres client.
  lib/          Data access used by pages and scripts.
  app/          Next.js App Router pages: landing, dashboard, add-monitor form, status page.
scripts/        migrate, seed, run-checks.
drizzle/        SQL migrations (generated; commit them).
tests/          Vitest tests for src/core.
docs/           EXERCISES.md, and later the architecture docs (module 9).
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
| Zod | One validation schema shared by forms and, later, the public API | 5.2 |
| Vitest | Fast tests for the core logic | — |
| Docker Compose | Postgres and Mailpit locally with one command | 7.4 |

The course names the Django, Rails, Laravel and Go equivalents for every component. The ideas carry over,
so port Beacon to your own stack if that is what your team uses.

## License

MIT. Copy anything you like into your own projects.
