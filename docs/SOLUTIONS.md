# Solutions

What each `module-N-solution` branch builds, which files to read, and the decisions behind them. Read the
lesson first, try the exercise, then read the diff for one module next to its section here:

```bash
git diff main module-1-solution            # Module 1
git diff module-1-solution module-2-solution   # Module 2, and so on
```

Each module appends its own section below. The solutions cover the 🟢 Beginner and 🟡 Intermediate
exercises; the 🔴 Advanced ones are stretch goals.

---

## Module 1 — Identity & Access

Beacon on `main` has no login and one global list of monitors. After Module 1 every request answers the
module's three questions in order: **who are you** (1.1), **which organization are you in** (1.2), and
**may you do this** (1.3).

```
request ─► session cookie ─► user ─► /[orgSlug] ─► membership ─► role ─► can(role, permission)
                (1.1)                    (1.2: 404 if not a member)       (1.3: 403 if not allowed)
                                                         │
                                                         └─► orgId goes into every WHERE clause
```

### Try it by hand

```bash
cp .env.example .env.local        # set BETTER_AUTH_SECRET: openssl rand -base64 32
npm install && npm run db:migrate && npm run db:seed
npm run dev
```

1. Sign up at <http://localhost:3000/signup>. You land in *Your-name's workspace*, a personal
   organization. The terminal prints a `[email]` block with a verification link. Open it.
2. Create a second organization at `/orgs/new` and add a monitor.
3. Go to **Members**, invite a second email address as `viewer`. Copy the `/invite/…` link from the
   terminal and open it in a private window. Create the account (the email is pre-filled) and accept.
4. As the viewer: no **Add monitor** button, `/<org>/monitors/new` shows a 403 page, and the API refuses too:

   ```bash
   # copy the better-auth.session_token cookie from the viewer's browser
   curl -i -X DELETE -b 'better-auth.session_token=…' http://localhost:3000/api/orgs/<org>/monitors/<id>
   # HTTP/1.1 403  {"error":"forbidden"}
   ```

5. Sign up a third user and open the first org's monitor URL: 404, both under the first org's slug and
   under their own.
6. Sign out, then replay the old cookie with `curl`: 401 from the API, a redirect to `/login` from pages.

Existing database from `main`? `npm run db:migrate` moves your old monitors into an organization with
slug `default`; run `npm run org:claim -- default you@example.com` after signing up to become its owner.

### Lesson 1.1 — Authentication

**What was built.** Email and password sign-up, sign-in and sign-out with [Better Auth](https://www.better-auth.com)
and its Drizzle adapter. Server-side sessions in Postgres behind an `HttpOnly`, `SameSite=Lax` cookie
(`Secure` automatically when `APP_URL` is https). Passwords hashed with argon2id. Email verification,
password reset, and an optional "Sign in with GitHub" with explicit account linking.

**Read in this order**

1. `src/db/auth-schema.ts`: the four tables Better Auth needs, and why "account" means a login method here.
2. `src/lib/password.ts`: argon2id with the OWASP baseline parameters.
3. `src/lib/auth.ts`: the whole configuration, one commented block per decision.
4. `src/lib/session.ts`: `getCurrentUser()` and `requireUser()`.
5. `src/app/(auth)/actions.ts`: sign-in, sign-up, sign-out, reset and GitHub as server actions.
6. `src/core/safe-redirect.ts`: why `?next=` must not accept `https://evil.example`.
7. `src/lib/email.ts`: the console "mailer" (`TODO(4.1)`).

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 Sign-up/login, protected pages, logout | argon2id hashes; no plaintext in a dump | `password.ts`; `select password from accounts` shows only `$argon2id$v=19$m=19456,t=2,p=1$…` |
| | `HttpOnly`, `Secure` in production, `SameSite=Lax` | `auth.ts` `advanced`; smoke test reads the cookie flags |
| | replaying the cookie after logout → redirect or 401 | logout deletes the `sessions` row; smoke test replays the cookie and gets 401 |
| 🟡 GitHub sign-in + password reset | OAuth code flow with PKCE, `state` validated | Better Auth's GitHub provider (it sends `code_challenge` and checks `state`) |
| | link GitHub only if verified *and* confirmed by signing in | `disableImplicitLinking: true`; linking only from `/account` while signed in, and Better Auth refuses an unverified GitHub email |
| | reset tokens hashed, expire within an hour, fail on second use | `verification.storeIdentifier: 'hashed'`, `resetPasswordTokenExpiresIn: 3600`; Better Auth consumes the token |
| | a completed reset signs out other sessions | `revokeSessionsOnPasswordReset: true` (the reset happens signed out, so that is *every* session) |
| | byte-identical reset responses | Better Auth returns one body for both; our form shows one message; smoke test compares bodies |

**Design decisions to notice**

- **A library, not hand-written crypto.** The lesson's rule. What is ours is the configuration and the
  edge cases, and those are all in one file.
- **argon2id instead of Better Auth's default scrypt.** scrypt is fine too, but the exercise names
  argon2id or bcrypt, and swapping the hash is a two-function change (`password.hash/verify`).
- **Server-side sessions, not JWTs.** Logout and "reset signs you out everywhere" are one `DELETE`.
- **Server actions call `auth.api.*`** (with the `nextCookies()` plugin) so forms work like the rest of
  Beacon, without a client auth SDK.
- **Email verification is not required to log in**, only to send invitations (lesson 1.2: unverified users
  must not send email from your domain). Accepting an invitation also verifies the email, because the
  link was emailed to that address.
- **Minimum password length 12, no composition rules** (NIST SP 800-63B).
- **Known gap: session tokens are stored as-is.** The lesson stores a SHA-256 of the session token.
  Better Auth keeps the token itself in `sessions.token` (the cookie holds that token plus an HMAC
  signature) and has no option to hash it. A leaked `sessions` table would therefore be usable until the
  sessions expire. We accepted this rather than fork the library; it is a good question to raise when
  choosing an auth library.
- **GitHub sign-in is wired but only switched on with `GITHUB_CLIENT_ID`/`GITHUB_CLIENT_SECRET`.** It was
  typechecked but not exercised end to end in CI or the smoke test, which have no GitHub OAuth app.

### Lesson 1.2 — Users, organizations and invitations

**What was built.** Hand-written `organizations`, `memberships` (one role per user per org) and
`invitations` tables. `organization_id` on monitors, check results and incidents. A personal organization
for every new user, more organizations at `/orgs/new`, the org slug in every URL, invitations with
resend and revoke, and an org switcher. The public status page is now per organization at `/status/[slug]`.

**Read in this order**

1. `src/db/schema.ts`: the data model. Note `organization_id` on *every* tenant table.
2. `drizzle/0002…0004`: expand (nullable column) → backfill (hand-written SQL) → contract (`NOT NULL`).
3. `src/core/roles.ts`, `src/core/slugs.ts`: the roles, and why an org cannot be called "login".
4. `src/lib/organizations.ts`: create an org and its owner in one transaction; `findMembership()`.
5. `src/lib/access.ts`: `requireMembership()` — the slug in the URL is a claim, the membership is the fact.
6. `src/lib/monitors.ts`: every function takes the org and filters on it.
7. `src/core/invitations.ts`, then `src/lib/invitations.ts`: token rules, then the flows.
8. `src/app/invite/[token]/page.tsx`: one link for new users, existing users and the wrong account.
9. `src/app/[orgSlug]/layout.tsx`: the org switcher.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 orgs + memberships, org ownership, personal org, slug in URL | every monitor has non-null `org_id`; every monitor query filters on it | migration 0004; `src/lib/monitors.ts`, `scripts/run-checks.ts` |
| | `/some-other-org/monitors` as a non-member → 404 | `requireMembership()` throws `not_found`; smoke test and `tests/tenant-isolation.test.ts` |
| | a migration moves existing monitors into an org | `drizzle/0003_backfill_organizations.sql` (see below) |
| 🟡 invitations, revoke, resend, org switcher | tokens hashed, expire in 7 days, single use | `src/core/invitations.ts`; conditional `UPDATE` in `acceptInvitation()`; `tests/invitations.test.ts` |
| | `sam@acme.com`'s invite cannot be accepted as `sam@gmail.com` | `emailsMatch()`; the invite page explains and offers to switch account |
| | a user with no account signs up from the link and lands in the org | invite page → `/signup?email=…&next=/invite/…` → accept → `/<org>/monitors` (smoke test) |
| | invites rate-limited per org | 20 per org per hour, counted from `invitations.sent_at` |

**Design decisions to notice**

- **`/[orgSlug]/monitors`, not `/dashboard`.** Org in the URL (the lesson's preferred design): shareable
  links, two orgs in two tabs. `/dashboard` now just redirects to your first org. Top-level slugs cannot
  shadow Beacon's own routes (`RESERVED_SLUGS`).
- **404, not 403, for non-members**, so outsiders cannot learn that a slug exists.
- **The tenant_id rule.** `check_results` and `incidents` carry `organization_id` even though the monitor
  already has it. Every read in `src/lib` and in the check runner filters on it.
- **The backfill.** On `main`, monitors belonged to nobody (there were no users), so "move each user's
  monitors into their personal org" becomes "move all existing monitors into one `default` org". It has
  no members; `npm run org:claim -- default <email>` adopts it. Users created before the migration
  (only possible on this branch) get a personal org in the same migration.
- **Personal org on sign-up** through Better Auth's `databaseHooks.user.create.after`, so it also happens
  for GitHub sign-ups.
- **Accepting is a POST from a button**, never a side effect of opening the link: email scanners open
  links too (lesson 1.1, magic links). The page also sets `<meta name="referrer" content="no-referrer">` so the token does not leak to other sites.
- **Single use under races.** `acceptInvitation()` marks the invitation accepted with
  `UPDATE … WHERE accepted_at IS NULL AND revoked_at IS NULL AND expires_at > now()`; only one of two
  concurrent requests can match.
- **At most one open invitation per email per org**, enforced by a partial unique index. Resend issues a
  new token and expiry, so the old link dies.
- **Rate limit from the table itself** (no Redis yet). Resends count too. Lesson 5.2 covers real limiters.
- **Sending invitations requires a verified email** and a role at or above the one being granted.

### Lesson 1.3 — Authorization

**What was built.** The owner/admin/member/viewer matrix as one permission map, `can()` and
`requirePermission()`, enforced in every page, server action and API route. JSON endpoints under
`/api/orgs/:orgSlug/…` with Zod-parsed bodies and DTO responses. One ABAC rule (members edit only their own
monitors), role-change rules, a real 403 page, and a test that calls every endpoint as every role.

**Read in this order**

1. `src/core/permissions.ts`: the matrix, `can()`, `canEditMonitor()`, `roleChangeRefusal()`, `canGrantRole()`.
2. `src/lib/access.ts`: `requirePermission()` → 401 / 404 / 403, and `forPage()` for pages and actions.
3. `src/lib/errors.ts` and `src/lib/api.ts`: one error type, mapped to status codes in one place.
4. `src/app/api/orgs/[orgSlug]/monitors/[id]/route.ts`: a short, complete endpoint.
5. `src/lib/monitors.ts` `getEditableMonitor()`: object-level check (404), then the ABAC rule (403).
6. `src/core/validation.ts` and `src/core/dto.ts`: allow-lists in, allow-lists out.
7. `src/app/[orgSlug]/members/page.tsx`: the UI offers only what the server would accept.
8. `tests/permissions.test.ts`, `tests/tenant-isolation.test.ts`, `tests/api-matrix.test.ts`.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 roles, `requirePermission()`, hide buttons | every mutating endpoint calls `requirePermission()` first | all server actions in `src/app/**/actions.ts` and all `src/app/api/orgs/**/route.ts` |
| | a viewer's `DELETE` → 403 | `tests/api-matrix.test.ts`; smoke test from the viewer's browser |
| | every monitor query includes the org; another org's id → 404 | `src/lib/monitors.ts`; IDOR tests through the API and the smoke test |
| 🟡 Zod + DTOs, role-change rules, one ABAC rule | `{"orgId": …}` or `{"role": "owner"}` in a body has no effect | Zod strips unknown keys; role ceiling enforced; mass-assignment tests |
| | no response has columns outside its DTO | `toMonitorDto`, `toMemberDto`; DTO key tests |
| | an admin cannot promote to owner; nobody changes their own role | `roleChangeRefusal()`; unit and API tests |
| | a test calls each endpoint as each role | `tests/api-matrix.test.ts`: 8 endpoints × 6 actors |

**Design decisions to notice**

- **Permissions, not role names.** Nothing outside `permissions.ts` compares a role to a string.
  Adding a role is a one-line change there, and `tests/permissions.test.ts` pins the matrix down.
- **Two permissions where the lesson has one row.** "Create and edit monitors" became `monitor.write`
  (create, and edit your own) and `monitor.write_any` (edit anyone's). The ABAC rule then stays a
  permission check instead of `role === 'admin'`. We also added `member.read` (all roles), so the members
  page and API call `requirePermission()` like everything else.
- **Function-level, then object-level.** `requirePermission()` answers "may this role do this at all?"
  before any lookup; `getMonitor(ctx, id)` answers "is this object in the org?" by putting the org in
  the query. Returning 404 for foreign objects and 403 for forbidden ones follows the lesson.
- **The org comes from the server, never from the body.** Actions receive the slug as a bound
  argument, re-check it, and pass the resulting `orgId` to the query.
- **Role hierarchy protects the last owner.** Nobody may change their own role, so whoever changes an
  owner's role is still an owner. (Leave, remove and ownership transfer are the 🔴 exercise.)
- **`forbidden()` needs `experimental.authInterrupts`** in `next.config.ts`. It gives the 403 page a real
  status code, which the smoke test checks.
- **API paths are `/api/orgs/:orgSlug/monitors/:id`**, not the exercise's `/api/monitors/:id`, because the
  org lives in the URL everywhere else. Lesson 5.2's public API will take the org from the API key.
- **Tests use a real Postgres in memory** (PGlite running the same migrations), so `npm test` still needs
  no database server, and the IDOR and matrix tests exercise real SQL.

### Lesson 1.4 — Enterprise SSO and SCIM: left as a stretch goal

Lesson 1.4 is an 🔴 Advanced lesson, and even its 🟢 Beginner exercise needs infrastructure this
solution cannot ship honestly: a local IdP (authentik or Keycloak) **and** a self-hosted SAML Jackson /
Ory Polis, both running in Docker, plus a working SAML round trip to verify ("a tampered or expired SAML
response is rejected"). Faking the IdP inside Beacon would teach the opposite of the lesson's first rule,
*never write SAML validation yourself*, and an untested config for services we could not run would be
worse than none.

What Module 1 already gives you for it: organizations to own an SSO connection, memberships with a
default role for JIT provisioning, and `emailVerified` to build domain logic on. If you do it, start with
Better Auth's `sso` plugin (OIDC and SAML) or run Ory Polis next to Beacon with `docker compose`, and map
a connection to an org with a small `sso_connections` table.

### Not done in Module 1 (🔴 exercises and neighbours)

Passkeys, TOTP, devices page, step-up auth and login rate limiting in Redis (1.1 🔴); leave, remove member,
ownership transfer, org deletion and row-level security (1.2 🔴); OpenFGA/SpiceDB sharing (1.3 🔴); all of
1.4. Real email is lesson 4.1, the audit log for role changes and deletions is `TODO(7.3)`.

### Verification for this branch

`npm test` (124 tests), `npm run typecheck`, `npm run db:migrate` on a fresh database and on a database
migrated and seeded on `main`, `npm run build`, and a headless-browser run against `next start` covering:
sign up → create org → add monitor → invite → invitee signs up from the link and accepts as viewer → the
viewer cannot create or delete a monitor (UI, page and API) → a user of another org gets 404 for the
monitor by id → identical reset responses → logout invalidates the cookie.

---

## Module 2 — Data

Module 1 decided *who* may see a row. Module 2 is about the rows themselves: keeping the dashboard fast
as they pile up (2.1), keeping files out of the database (2.2), finding things again (2.3), and making
the tenant boundary something Postgres enforces, not only something each query remembers (2.4).

```
request ─► requirePermission() ─► src/lib/* (orgId in every WHERE) ─► withOrg(orgId)
                                                                         │ BEGIN
                                                                         │ set_config('app.current_org', orgId, true)
                                                                         │ set_config('role', 'beacon_app', true)
                                                                         │ … queries: RLS policies filter and check every row …
                                                                         │ COMMIT  (both settings end here)
files:   browser ──signed PUT──► object storage (orgs/{orgId}/…)  ◄──signed GET── browser
                    ▲ Beacon signs after checking role, size, type; checks the bytes after upload
```

### Try it by hand

```bash
npm install
npm run db:reset             # drop everything, migrate, seed (local databases only)
npm run db:seed:large        # optional: org "big", 500 monitors × 1,000 checks
npm run dev
```

1. Sign in as `demo@beacon.test` / `beacon-demo-password` (owner) or `member@beacon.test` (member).
2. `DB_LOG=1 npm run dev` and open `/demo/monitors`: one SQL statement for the list, however many
   monitors. Open `/big/monitors` for the 500-monitor version.
3. **Settings → Status page logo**: upload a PNG. Open `/status/demo` in a private window and the logo
   is there. Now rename a text file to `logo.png` and upload it: *Rejected: That file is not the image
   it claims to be.* Try an `.exe`: refused before any URL is signed.
4. Open the "Always broken" monitor, add a screenshot to its incident: *processing…*, then a 400 px
   thumbnail. Copy the image link, sign in as another user in another org, open it: 404.
5. Type `chekout` in the search box on the monitors page. Press **Ctrl+K** (⌘K) and type
   `"certificate expired" -staging`: the checkout incident, highlighted, and not the staging one.
   Arrow keys and Enter open it.
6. Post an update on an incident, then find it with Ctrl+K.

Files go to `.storage/` by default. To use a real bucket (R2, S3, Garage, SeaweedFS), set
`STORAGE_DRIVER=s3` and the `S3_*` variables in `.env.local`, then `npm run storage:setup` once.

### Lesson 2.1 — The data layer

**What was built.** The dashboard query as one statement with three `LATERAL` subqueries instead of an
N+1; a covering index that turns it into index-only scans; `updated_at` on every table Beacon owns; an
idempotent seed with an owner and a member; `npm run db:reset`; a large seed for measuring; query
logging; and a `lock_timeout` for migrations.

**Read in this order**

1. `src/lib/monitors.ts` `listMonitors()`: the N+1 fix. Compare with `git show module-1-solution:src/lib/monitors.ts`.
2. `src/db/schema.ts`: the `check_results` index comment (column order, covering columns, the
   `DESC NULLS LAST` trap), `incidents_open_idx` (partial), and the `updatedAt()` helper.
3. `drizzle/0006_timestamps_and_indexes.sql`: why `ADD COLUMN … DEFAULT now()` is cheap, a backfill
   in the same migration, and why the index is not built `CONCURRENTLY` here.
4. `scripts/seed.ts`: idempotent by natural keys. `scripts/reset.ts`: refuses non-local databases.
5. `scripts/seed-large.ts`: rows generated inside Postgres with `generate_series`.
6. `tests/data-layer.test.ts`: counts SQL statements to prove the query count is constant.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 schema, first migration, idempotent seed (1 org, owner + member, 5 monitors, a day of checks) | fresh clone + one command → working, seeded database | `npm run db:reset` (reset → migrate → seed) |
| | every tenant table has `organization_id`, `created_at`, `updated_at` with FKs | migration 0006; `check_results` is the one deliberate exception (below) |
| | running the seed twice creates no duplicates | lookups by email / slug / monitor name; the second run prints "nothing to do" |
| 🟡 the dashboard query, fast, with 500 × 1,000 | constant number of queries | `listMonitors()`; `tests/data-layer.test.ts` (3 vs 23 monitors → same count) |
| | `EXPLAIN ANALYZE` shows no seq scan on `check_result` | plan below |
| | page loads in under 200 ms locally with the large seed | smoke test: `/big/monitors` median 162 ms (query ~90 ms, the rest is rendering 500 rows) |

`EXPLAIN ANALYZE` of the dashboard query for org "big" (500 monitors × 1,000 checks, Postgres 16):

```
Nested Loop Left Join (actual time=0.35..92.6 rows=500)
  -> Index Scan using monitors_org_idx on monitors m (rows=500)
  -> Limit (rows=1 loops=500)
       -> Index Only Scan Backward using check_results_org_monitor_time_idx on check_results
  -> Aggregate (loops=500)
       -> Index Only Scan using check_results_org_monitor_time_idx on check_results  (rows=1000 loops=500, Heap Fetches: 0)
  -> Index Scan using incidents_open_idx on incidents (loops=500)
Execution Time: 92.7 ms          (the starter's index: Bitmap Heap Scan + Sort, 1,036 ms)
```

**Design decisions to notice**

- **`LATERAL` instead of the lesson's `DISTINCT ON`.** The dashboard also needs 24-hour uptime and the
  open incident. `DISTINCT ON` gives only the latest check; three small lateral subqueries give all
  three in one statement, each an index lookup per monitor.
- **The index already existed and was still wrong.** The starter had `(monitor_id, checked_at DESC)`.
  Module 1's tenant rule adds `organization_id = …` to every check query, which that index cannot
  answer, and Drizzle writes `.desc()` as `DESC NULLS LAST`, which does not match `ORDER BY … DESC`
  (NULLS FIRST), so Postgres sorted. The replacement is `(organization_id, monitor_id, checked_at, ok,
  latency_ms)`: equality columns, then the range column, then the columns the query reads, so the
  table is never touched ("Heap Fetches: 0" once autovacuum has run; the large seed runs `VACUUM`).
  It also serves as the index on the `organization_id` foreign key.
- **`check_results` has no `updated_at`.** Rows are immutable facts, `checked_at` is their creation
  time, and it is the table that grows by millions of rows. A deliberate exception, written down in
  the schema.
- **`updated_at` via Drizzle's `$onUpdate`**, visible in the schema. A trigger would also catch
  hand-written SQL; the trade-off is noted in `schema.ts`.
- **Expand/contract, as house rules** (lesson 2.1, and 1.2's 0002→0004 did it for real):
  1. Additive first: new columns nullable or with a non-volatile default; new tables; new indexes.
  2. Backfill in the same migration when it is small (0006, 0009), in batches with a `lock_timeout`
     when it is not.
  3. Switch the code to the new shape in a deploy of its own.
  4. Contract (drop, `NOT NULL`, rename's second half) only after no running code uses the old shape.
  5. Never `CREATE INDEX` on a big table inside the migrator's transaction: build it `CONCURRENTLY` by
     hand first, then let the migration's `IF NOT EXISTS` do nothing.
  6. Roles, grants, policies, extensions and functions go in `drizzle-kit generate --custom` migrations
     (0007), or at the end of a generated one with a comment (0008, 0009). Never by hand in production.
- **`lock_timeout` 10 s** on the migration connection: a migration stuck behind a long query fails
  instead of queueing every request behind itself.
- **Ids stay plain UUIDs.** No exercise asks for prefixed ids, and changing every id is not a change to
  make without one. The lesson's `mon_…` prefix at the API boundary is a good stretch.

### Lesson 2.2 — File uploads and object storage

**What was built.** A `files` table, a `Storage` interface with an S3 driver (`@aws-sdk/client-s3`,
presigned URLs) and a local-filesystem driver, status page logos for owners and admins, incident
screenshots for members with a background thumbnail job, downloads through a membership-checked
redirect, and `npm run storage:setup` for a real bucket.

**Read in this order**

1. `src/core/files.ts`: the rules. Allowlists, sizes, magic-number sniffing, keys under `orgs/{orgId}/`.
2. `src/lib/storage/index.ts`, then `s3.ts` and `local.ts`: one interface, two drivers.
3. `src/lib/files.ts`: request → upload → complete, the thumbnail job, signed downloads.
4. `src/app/api/orgs/[orgSlug]/logo/route.ts`, `…/files/[fileId]/complete/route.ts`,
   `…/files/[fileId]/route.ts`, `src/app/status/[slug]/logo/route.ts`.
5. `src/app/_components/direct-upload.ts`: the three steps from the browser's side.
6. `src/app/api/storage/[...key]/route.ts`: the local driver's "bucket".
7. `tests/uploads.test.ts` and `tests/storage.test.ts` (the S3 driver against s3rver).

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 logo: `file` table, presigned PUT for `orgs/{orgId}/logos/{fileId}`, "complete" marks it ready | the bytes never pass through the app server | S3 driver: browser → bucket. (Local driver: see the first decision below.) |
| | only admins of the org can request a signed URL | `requirePermission(…, 'page.publish')`; member/viewer 403, other org 404 (tests, smoke) |
| | a 10 MB file or an `.exe` is rejected before a URL is issued | `checkUploadRequest()`: size, type allowlist, extension; no row is written (tests, smoke) |
| 🟡 incident screenshots, private; download endpoint → 5-minute presigned GET; sniff after upload; 400 px thumbnail in a job | another org's user gets 404 for the download, even with a valid id | `signedDownloadUrl()` looks the file up *in the org*; tests and smoke, both slugs |
| | a text file renamed to `.png` is rejected after upload and its object deleted | `completeUpload()` sniffs the first bytes; the object is deleted (tests, smoke) |
| | thumbnails are generated asynchronously, the UI shows "processing" | `after()` job in `src/lib/jobs.ts`, `npm run files:process` as a safety net; `AutoRefresh` on the monitor page |

**Design decisions to notice**

- **Two drivers, one interface.** No MinIO or Docker is needed to run or test Beacon. The local
  driver signs URLs with an HMAC and an expiry, and its route checks them like S3 checks a presigned
  URL (tampered, expired or wrong-type requests get 403). The honest difference: with the local driver
  the Next.js process plays the bucket, so bytes do pass through it. The S3 driver is the one to
  deploy; it runs in the tests against s3rver, a small S3-compatible server in Node.
- **Checked twice.** Before signing: the declared size, type and extension. After upload: `HEAD` for the
  real size (a presigned PUT does not limit size; a presigned POST policy could), then the first 12
  bytes against the PNG/JPEG/WebP magic numbers. The thumbnail job is a third check: an "image" that
  `sharp` cannot decode is rejected and deleted too.
- **No SVG.** An SVG can carry `<script>`. Allowing it would need a sanitiser; leaving it out is the
  lesson's default.
- **Private bucket, even for the public logo.** `/status/[slug]/logo` redirects to a 5-minute signed
  URL while the status page is published and answers 404 when it is not. A separate public bucket
  behind a CDN would be the next step for traffic.
- **User content on Beacon's domain.** The local route serves files with `X-Content-Type-Options:
  nosniff` and `Content-Security-Policy: sandbox`. In production, point downloads at a separate
  domain (the bucket's or a CDN's), as the lesson says.
- **Keys are ours:** `orgs/{orgId}/logos/{fileId}`, never the user's file name. Signing asserts the key
  is under the caller's org (`keyBelongsToOrg`), a cheap guard against id-swapping bugs.
- **No network inside transactions.** Rows are written in `withOrg()`, storage is called outside it.
- **Jobs before lesson 5.1.** `after()` runs the thumbnail after the response; a restart can lose it,
  so `npm run files:process` finishes anything left "processing". The job payload is
  `{ type, orgId, fileId }` (lesson 2.4).
- **Replacing a logo deletes the old one**, row and object, so the bucket does not collect orphans.

### Lesson 2.3 — Search

**What was built.** Trigram search over monitor names and URLs, an `incident_updates` table with a
generated `tsvector`, full-text search with web-style queries, ranking and highlighted snippets, a
search box on the monitors page, and a Ctrl+K palette that searches pages, monitors and incidents in
one call.

**Read in this order**

1. `src/db/schema.ts`: `monitors_*_trgm_idx`, `incidentUpdates` and its generated `search` column.
2. `drizzle/0009_search.sql`: the extension, the backfill, and at the end the two search functions
   and *why they are functions* (the RLS/LEAKPROOF comment).
3. `src/lib/search.ts`, then `src/core/search.ts` (snippets as parts, the pages list).
4. `src/app/api/orgs/[orgSlug]/search/route.ts` and `src/app/[orgSlug]/command-palette.tsx`.
5. `tests/search.test.ts`.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 pg_trgm monitor search, name and URL indexed, ranked, org-filtered | "chekout" finds "checkout-api" | `search_monitors()`; tests; smoke (search box) |
| | `EXPLAIN ANALYZE` shows the trigram index on 50,000 monitors | plan below |
| | a test proves a user never gets another org's monitors, even with identical names | `tests/search.test.ts`, `tests/cross-tenant-routes.test.ts`; smoke (a second org's search box and API) |
| 🟡 FTS over incident updates, `websearch_to_tsquery`, ranking, snippets; cmd-K over monitors, incidents, pages in one call | `"certificate expired" -staging` behaves like a web search | tests and smoke: the checkout incident, not the staging one |
| | results show a highlighted snippet and the object type | `ts_headline` → `<mark>`; a type badge per result |
| | keyboard-only, under 150 ms locally | Ctrl+K, ↑/↓, Enter, Esc; smoke measured the API at 6 ms (`Server-Timing`) |

`npm run db:seed:large -- --monitors=50000 --checks=0`, then `search_monitors('chekout', 20)` as the
app role (plan captured with `auto_explain.log_nested_statements`):

```
Limit (actual time=20.5 rows=20)
  -> Sort (top-N heapsort)
       -> Bitmap Heap Scan on monitors m (rows=1250)
            -> BitmapOr
                 -> Bitmap Index Scan on monitors_name_trgm_idx   Index Cond: (name %> $1)
                 -> Bitmap Index Scan on monitors_url_trgm_idx    Index Cond: (url %> $1)
                 -> Bitmap Index Scan on monitors_name_trgm_idx   Index Cond: (name ~~* …)
                 -> Bitmap Index Scan on monitors_url_trgm_idx    Index Cond: (url ~~* …)
Execution Time: ~21 ms           (the same query as a plain query under RLS: Seq Scan, ~500 ms)
```

**Design decisions to notice**

- **Where 2.3 meets 2.4.** Under row-level security, Postgres evaluates the policy before any condition
  whose operator is not `LEAKPROOF`, and cannot use such a condition to search an index. The trigram
  operators and `@@` are not leakproof, so as `beacon_app` both searches were sequential scans (~0.5 s
  on 50,000 monitors). They are therefore `SECURITY DEFINER` SQL functions: they run as the table owner
  (whom RLS does not restrict here), so the indexes work, and they apply the tenant filter themselves
  from `current_org_id()`, the org `withOrg()` set. They take no org argument, return nothing without
  `withOrg()`, have a fixed `search_path`, and only `beacon_app` may execute them. This is the one place
  the tenant filter lives in SQL rather than in both TypeScript and a policy, so the tests cover it
  directly. Supabase recommends the same pattern for the same problem.
- **`word_similarity` (the `<%` operator), threshold 0.4.** A short query against a longer name or URL
  is "is the query like *part of* this text?". pg_trgm's default 0.6 misses one-letter typos in short
  words ("chekout" scores 0.55); 0.4 still keeps unrelated names out (tested). `ILIKE '%…%'` covers
  exact substrings, with the user's `%` and `_` escaped.
- **Snippets are data, not HTML.** `ts_headline` marks matches with `⟦ ⟧`, the API returns
  `[{ text, hit }]`, and React renders `<mark>` elements. Asking Postgres for `<b>…</b>` and using
  `dangerouslySetInnerHTML` would be stored XSS through an incident update.
- **Incident updates are the searchable prose.** The check runner writes the first ("Opened
  automatically: …") and the last update; people post the rest from the monitor page. Migration 0009
  backfills one update per existing incident.
- **One call, filtered server-side.** The palette sends only `q`. Pages are offered only if the role may
  open them (a viewer is never shown Settings). Debounce 150 ms, and a newer keystroke aborts the older
  request so results never arrive out of order.
- **Drizzle for everything else, raw SQL here.** `selectRows()` in `src/db/tenant.ts` smooths over the
  two drivers' result shapes (postgres.js in the app, PGlite in tests). PGlite ships `pg_trgm`, so the
  tests run the real operators.

### Lesson 2.4 — Multi-tenancy deep dive (🟢 and 🟡)

2.4 is an 🔴 lesson, but its 🟢 and 🟡 exercises fit Beacon well: Module 1 already scoped every query,
and row-level security is exactly the "defence in depth" the lesson describes. Its 🔴 exercise (EU
cells, per-org job fairness) needs infrastructure this solution does not have.

**What was built.** `withOrg()`, the `beacon_app` role, `tenant_isolation` policies on every tenant
table, the check runner and file job running per org, a source "lint" test, and a cross-tenant test
that must cover every API route.

**Read in this order**

1. `src/db/tenant.ts`: `withOrg()` and why the settings are transaction-local.
2. `drizzle/0007_row_level_security.sql`: role, grants, `current_org_id()`, policies, and why no `FORCE`.
3. `scripts/run-checks.ts`: a job that sets the tenant too, and keeps HTTP outside the transaction.
4. `tests/tenant-scoping.test.ts`: RLS behaviour, "every tenant table has a policy", and the lint.
5. `tests/cross-tenant-routes.test.ts`: org B against every org A route, and the coverage check.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 audit, scoped helper, cross-tenant test for every route | no handler queries a tenant table except through the helper (lint rule or checklist) | lint test: no `db.select/insert/update/delete/execute` touching a tenant table in `src/` or the jobs; `db.transaction` only in two identity files |
| | logged in as org B → 404 for every org A resource | `tests/cross-tenant-routes.test.ts`: 12 route/method pairs × 2 slugs; fails if a new route has no case |
| | cache keys and job payloads include `org_id` | no caches yet; job payload `{ type, orgId, fileId }`; storage keys `orgs/{orgId}/…` |
| 🟡 RLS on monitor, incident, incident_update; non-owner role; `app.current_org` per transaction; jobs too | deleting `WHERE organization_id` still returns only the current org | test: `withOrg(acme, tx => tx.select().from(monitors))` |
| | inserting a monitor with another org's id fails with an RLS violation | test: "new row violates row-level security policy" (also for moving a row) |
| | works through PgBouncer in transaction mode | `set_config(…, true)` only; test: nothing is left on the connection after commit or rollback (PGlite's single connection = the next pooled transaction). Not run through a real PgBouncer. |

**Design decisions to notice**

- **Both layers stay.** Every function in `src/lib` still writes `organization_id = …` (Module 1), and
  runs inside `withOrg()`. Together they are the lesson's `forOrg(orgId)`: Module 1's functions already
  take the org as a required first argument, so the name did not change.
- **RLS on every table with `organization_id`**, not only the three the exercise names: monitors,
  check_results, incidents, incident_updates, files. The exceptions are `memberships` and
  `invitations`, read *before* the org is known (at login, from an invitation token). A test fails if a
  new tenant table has no policy.
- **The role switch happens inside the transaction** (`set_config('role', 'beacon_app', true)`), the
  way PostgREST/Supabase do it, rather than a separate login role for the app. It works with any
  connection string and with transaction pooling. The gap: code that skips `withOrg()` runs as the
  connection's user and is not filtered, which is what the lint test is for. Hardening for production:
  connect the app as a login role that owns nothing and is only a member of `beacon_app`, so a query
  outside `withOrg()` fails instead of seeing everything.
- **No `FORCE ROW LEVEL SECURITY`.** Tenant queries run as `beacon_app`, not as the owner, so policies
  apply to them without it. The owner (migrations, `db:seed`) keeps seeing every row, so a data
  migration cannot silently backfill nothing.
- **Fail closed.** `current_org_id()` is NULL when nothing is set, so as `beacon_app` without `withOrg()`
  every tenant table looks empty (tested), and so do the search functions.
- **Jobs set the tenant too.** The check runner and `files:process` list organizations (not a tenant
  table), then work inside `withOrg(org.id)` per org.
- **Rules for `withOrg()` callbacks:** only `tx` inside (the global `db` is another connection without
  the setting), and no network calls: a transaction holds its connection until it ends.

### Not done in Module 2 (🔴 exercises and neighbours)

The rename with zero downtime, PITR and a restore drill (2.1 🔴); retention for `check_results` and
time partitioning (no exercise asks yet; the covering index keeps the dashboard fast meanwhile);
prefixed ids; org offboarding for files, lifecycle rules and orphan reconciliation (2.2 🔴; deleting a
monitor or incident deletes its file rows but not yet its objects); malware scanning; Meilisearch or
Typesense with an outbox and tenant tokens (2.3 🔴); residency cells and per-org job fairness (2.4 🔴);
a real PgBouncer in CI; a dedicated app login role (above).

### Verification for this branch

`npm test` (205 tests, no database server: PGlite with `pg_trgm`, s3rver for the S3 driver),
`npm run typecheck`, `npm run db:migrate` on a fresh database and on a database migrated, seeded and
checked on `module-1-solution` (existing incidents get their first update), `npm run build`, and a
headless-browser run against `next start` (27 checks): `/big/monitors` with 500 × 1,000 in under
200 ms → owner uploads a logo → it shows on the public status page → the object is private without a
signature → a text file renamed to `.png` is rejected → an `.exe` and a declared 10 MB file are refused
→ an incident screenshot shows "processing" then a 400 px thumbnail → a member cannot upload a logo
but can download the screenshot → "chekout" finds checkout-api → Ctrl+K `"certificate expired"
-staging` finds the checkout incident with highlighted words, Enter opens it → a user of another org
finds nothing, gets 404 for the demo org's search, and 404 for the screenshot by id under both slugs.

---

## Module 3 — Money

Modules 1 and 2 decided who may see which rows. Module 3 decides what an organization has **paid for**:
Stripe owns the truth about money and a signed webhook keeps Beacon's copy in sync (3.1), one module turns
that copy into limits the server enforces everywhere (3.2), and every SMS becomes exactly one billable
usage event (3.3).

```
 Upgrade ─► startCheckout() ─► Stripe Checkout ─► success page: "confirming…" (grants nothing)
                                    │
                                    └─► POST /api/stripe/webhook  (signed)
                                          1. verify signature on the raw body   → 400 if not
                                          2. insert event id into stripe_events → "duplicate" if seen
                                          3. syncCustomerFromStripe(customer):
                                               re-fetch subscriptions from Stripe (never trust the payload)
                                               withOrg: upsert subscriptions → plan snapshot on the org
                                                        → freeze / unfreeze monitors (3.2)
                                               after commit: email owners once per downgrade

 every write ─► getEntitlements(org) ─► assertCanCreateMonitor / assertIntervalAllowed ─► 402 limit_exceeded
 check runner ─► same snapshot: paused monitors never run, interval ≥ plan minimum

 SMS worker (Module 4) ─► recordSmsSent() ─► usage_events (unique idempotency key, occurred_at = send time)
                              ├─► getUsageSummary(): sum per BILLING period → billing page, settings
                              ├─► usage_alerts: 80% / 100% email, once per period
                              └─► npm run usage:report ─► Stripe Billing meter (identifier = key) ─► invoice
```

Every Stripe call goes through a small `BillingProvider` interface with two implementations: the real
one (the official `stripe` SDK) and an in-memory fake. Tests, the smoke test and a laptop without a Stripe
account use the fake; the webhook signature check is the real SDK in both cases.

### Try it by hand (no Stripe account needed)

```bash
npm run db:reset                         # "demo" is on Free with 5 monitors: exactly its limit
BILLING_PROVIDER=fake npm run dev
```

1. Sign in as `demo@beacon.test`. The monitors page says *5 of 5 monitors on Free* and **Add monitor** has
   become **Upgrade to add more monitors**. The API refuses too:

   ```bash
   curl -i -b 'better-auth.session_token=…' -H 'content-type: application/json' \
     -d '{"name":"six","url":"https://six.test","intervalSeconds":300}' http://localhost:3000/api/orgs/demo/monitors
   # HTTP/1.1 402  {"error":"limit_exceeded","limit":"maxMonitors","allowed":5,"upgradeTo":"pro",…}
   ```

2. Open a monitor: the 30-second and 1-minute intervals are disabled and name the plan that unlocks them.
3. **Billing → Upgrade to Pro** opens a stand-in for Stripe Checkout. Pay with `4242 4242 4242 4242`
   (any other number is declined). You land on *Confirming your payment…*; about 1.5 s later the signed
   webhook arrives and the page switches to Pro by itself. The limit is now 50 and 1-minute checks unlock.
4. **Settings** shows the plan, *Monitors: 5 of 50* and *SMS used this period*.
5. **Manage billing** opens a stand-in for the Customer Portal. *Cancel at period end* shows "cancels on …"
   and keeps Pro; *Cancel now* ends the plan: add a sixth monitor first and watch it get paused with
   reason `plan_limit`, and one email ("Demo is now on the Free plan") in the terminal.
6. Sign in as `member@beacon.test`: no Billing link, `/demo/billing` is a 403 page, and
   `POST /api/orgs/demo/billing/checkout` answers 403.

The fake keeps its "Stripe account" in memory: restart the server and it is gone (the subscriptions table
keeps its copy). `BILLING_PROVIDER=fake` is for development only; never set it in production.

### Run it with real Stripe (test mode)

Nothing here needs code changes; the fake and the real provider implement the same interface.

1. In the Stripe dashboard (test mode) create a product **Beacon Pro** with a recurring price of $29/month
   and **Beacon Business** with $99/month. Put the price ids in `.env.local`:
   `STRIPE_PRICE_PRO=price_…`, `STRIPE_PRICE_BUSINESS=price_…`, and `STRIPE_SECRET_KEY=sk_test_…`.
2. Lesson 3.3 (optional): **Billing → Meters → Create meter**: event name `sms_segments`, aggregation
   *Sum*, customer mapping key `stripe_customer_id`, value key `value`. On each product add a *usage-based*
   price on that meter with **graduated** tiers: units 1–100 at $0 then $0.05 (Pro), 1–500 at $0 then
   $0.05 (Business). Put them in `STRIPE_PRICE_PRO_SMS` / `STRIPE_PRICE_BUSINESS_SMS`; Checkout adds them
   as a second line item.
3. **Settings → Billing → Customer portal**: allow cancelling (at period end), updating the payment
   method, invoice history, and switching between the two prices.
4. Forward webhooks to your laptop and copy the signing secret it prints into `STRIPE_WEBHOOK_SECRET`:

   ```bash
   stripe login
   stripe listen --forward-to localhost:3000/api/stripe/webhook \
     --events checkout.session.completed,customer.subscription.created,customer.subscription.updated,customer.subscription.deleted,invoice.paid,invoice.payment_failed
   npm run dev          # in another terminal, without BILLING_PROVIDER
   ```

5. Upgrade with `4242 4242 4242 4242`. `stripe listen` shows the events and the `200`s.
   `stripe events resend evt_…` answers `duplicate` and changes nothing. A request with a wrong signature
   gets `400`:
   `curl -i -X POST -H 'stripe-signature: t=1,v1=bad' -d '{}' localhost:3000/api/stripe/webhook`.
6. Cancel in the Portal: `select cancel_at_period_end from subscriptions` is `true` within a second or two.
   Delete that row, cause any new event for the subscription (for example, edit its metadata in the
   dashboard, which sends `customer.subscription.updated`), and the row is back.
7. Usage: once Module 4 sends SMS, `npm run usage:report` (from cron) sends the events to the meter. To
   see the $1.50 overage, attach a customer to a **test clock**, subscribe it to Pro, record 130 SMS,
   report, and advance the clock past the period end: the invoice has a 30 × $0.05 line.

This path was written against the `stripe` SDK's types and typechecks, but was **not run against Stripe's
servers** in this environment (no internet); the tests and the smoke test run the same code against the
fake provider.

### Lesson 3.1 — Subscriptions and payments

**What was built.** A `stripe_customer_id` on the organization, a `subscriptions` table (our copy) and a
`stripe_events` table (dedupe), hosted Checkout and Customer Portal behind **Upgrade** and **Manage billing**
(owners only), the webhook route, `syncCustomerFromStripe()`, a success page that only says
"confirming…", and a fake provider with stand-in Checkout and Portal pages.

**Read in this order**

1. `src/lib/billing/provider.ts`: the interface, and how the provider is chosen.
2. `src/lib/billing/index.ts`: `startCheckout()`, `openPortal()`, the customer on the org.
3. `src/app/api/stripe/webhook/route.ts`, then `src/lib/billing/webhook.ts`: verify → dedupe → sync.
4. `src/lib/billing/sync.ts`: re-fetch, upsert, plan snapshot, lock, one email.
5. `src/core/plans.ts` `statusGrantsAccess()`: what each Stripe status grants, in one place.
6. `src/lib/billing/stripe-provider.ts` and `fake-provider.ts`: the two implementations.
7. `src/app/[orgSlug]/billing/page.tsx` and `actions.ts`; `src/app/fake-billing/`.
8. `tests/billing.test.ts`.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 Checkout + Portal, org id on the session | an owner upgrades with 4242… and lands back on Beacon | smoke test (fake Checkout); `client_reference_id` and `metadata.orgId` in `stripe-provider.ts` |
| | the success page says "confirming…" and does not change the plan | `billing/page.tsx`; test "returning from Checkout changes nothing"; smoke test sees *Free* next to *Confirming…* |
| | "Manage billing" opens the Portal: update card, cancel | `openPortal()`; the fake Portal's cancel buttons; the real Portal after step 3 above |
| | non-owners don't see the billing buttons | `billing.manage` (owner) for the page, actions and endpoints; `billing.read` (owner, admin) for plan and usage; role matrix in `tests/billing.test.ts` |
| 🟡 raw-body verification, `stripe_events`, `syncCustomerFromStripe()` | the same event twice changes nothing the second time | primary key on `stripe_events.id`; test asserts no second Stripe call |
| | tampered body → 400, valid → 200 | `Stripe.webhooks.constructEvent` on `req.text()`; tests: tampered, wrong secret, unsigned, garbage signature, 10-minute-old timestamp (replay) |
| | Portal cancel → `cancel_at_period_end = true` within seconds | test and smoke test |
| | delete the row, replay an event → restored | test "deleting our subscriptions row…" (a new event; a resend of an already *processed* event is skipped by design) |

**Design decisions to notice**

- **The payload is never trusted.** The handler takes only the customer id from the event and re-fetches
  the subscriptions. A test sends a correctly signed `customer.subscription.deleted` while the real
  subscription is active: the org stays on Pro. Out-of-order events cannot write stale state.
- **Dedupe that survives a crash.** The event row is inserted first and `processed_at` is set after the
  sync. A repeated event is skipped only if it was processed; if the first attempt failed half-way, Stripe's
  retry is handled again (tested). Two concurrent copies may both sync, which is harmless.
- **Replay protection is the signature's timestamp.** `constructEvent` refuses signatures older than five
  minutes; within those minutes a replay is a duplicate id. Both are tested.
- **200 for events we do not handle** and for customers we do not know, so Stripe does not retry for days
  and disable the endpoint. An unhandled error is a 500 on purpose: Stripe retries it.
- **The customer belongs to the organization**, created on the first Upgrade with an idempotency key
  `customer:{orgId}` and stored with `WHERE stripe_customer_id IS NULL`, so two clicks make one customer.
- **One subscription per org.** A second Checkout is refused (`already_subscribed`); plan changes go
  through the Portal, which prorates.
- **Status → access in one function.** `trialing`, `active` and `past_due` keep the plan (the billing page
  shows a red "your last payment failed" line during `past_due`); everything else is Free.
- **Tenant data like the rest.** `subscriptions` is under row-level security; the webhook finds the org by
  customer id in `organizations` (not a tenant table) and then works inside `withOrg()`. `stripe_events`
  has no org. Stripe is called before the transaction, never inside it.
- **The fake is honest about its edges.** Its pages exist only with `BILLING_PROVIDER=fake`, still require
  `billing.manage` in the session's org, and deliver events over HTTP, signed, to the real webhook route.
- **Not done:** emails for `invoice.payment_failed` and `trial_will_end`, and moving the sync into a job
  queue (the lesson's "sync the row, enqueue the rest"; TODO(5.1)).

### Lesson 3.2 — Plans, limits and entitlements

**What was built.** `PLANS` (Free / Pro / Business) and the price-to-plan map in one module, a plan
snapshot column on the organization, `getEntitlements(org)`, `assertCanCreateMonitor()` and
`assertIntervalAllowed()` on create *and* update, a structured `402 limit_exceeded` error, disabled
intervals and upgrade prompts in the UI, and the freeze policy for downgrades with a page where the owner
picks which monitors run.

**Read in this order**

1. `src/core/plans.ts`: plans as data, statuses, the price map, `planFreeze()`.
2. `src/lib/entitlements.ts`: `getEntitlements()`, the asserts, `reconcileMonitorsWithPlan()`.
3. `src/lib/monitors.ts` `createMonitor()` / `updateMonitor()`: enforcement at the point of action.
4. `src/lib/errors.ts` `LimitExceededError`, `src/lib/api.ts`: the 402.
5. `drizzle/0010_plans.sql` and `0011_existing_orgs_on_free.sql`.
6. `src/app/_components/interval-select.tsx`, `src/app/[orgSlug]/monitors/page.tsx`, `…/monitors/plan-limit/`.
7. `src/core/schedule.ts` and `scripts/run-checks.ts`: the worker side.
8. `tests/plans.test.ts`, `tests/entitlements.test.ts`, the downgrade test in `tests/billing.test.ts`.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 `plans.ts`, `getEntitlements(org)`, `maxMonitors` and `minIntervalSec` on create and update | `grep -rn "plan ===" src/` returns nothing outside the plans module | a test greps `src/` for a plan compared to a string |
| | a Free org's sixth monitor via the API → structured `limit_exceeded` | `402 {"error":"limit_exceeded","limit":"maxMonitors","allowed":5,"upgradeTo":"pro"}`; test and smoke |
| | the form disables short intervals and shows an upgrade prompt | `IntervalSelect`; smoke checks the disabled options on Free and on Pro |
| 🟡 freeze on downgrade, clamp intervals, email the owner, owner picks | Pro → Free with 12 monitors: 5 active, 7 paused, nothing deleted | `reconcileMonitorsWithPlan()`; tests via the webhook path and directly |
| | upgrading un-pauses plan-paused monitors, not manually paused ones | `paused_reason` `manual` vs `plan_limit`; tests |
| | the scheduler never runs a paused monitor, nor faster than the current minimum | `isDue()` with `effectiveIntervalSec()` in `run-checks.ts`, reading the same snapshot; unit tests |
| | exactly one email per downgrade | the sync locks the org row (`SELECT … FOR UPDATE`) and compares the snapshot; test sends the cancel twice plus another event: one email |

**Design decisions to notice**

- **`src/core/plans.ts`, not `lib/plans.ts`.** It is pure, so it sits with the other pure modules; the
  server enforces it, the forms import it for hints, tests import it directly.
- **A snapshot on the org** (`organizations.plan`), written only by the sync and read by everything else:
  the API, the pages and the check runner enforce the same limits without calling Stripe. It is also where
  grandfathering and overrides will attach (3.2's 🔴 exercise).
- **Which monitors count.** `maxMonitors` limits how many monitors an org *has* (the lesson's count).
  After a downgrade an org can have more, frozen; at most `maxMonitors` of them *run*, and it cannot add
  any until it is back under the limit. Un-pausing needs a free running slot.
- **Freeze newest, keep oldest, never touch manual pauses.** Idempotent, so the sync runs it on every
  change: downgrade, upgrade, and the involuntary case (a failed payment ends the subscription).
  Intervals are raised to the new minimum and not lowered again on upgrade (the old value is gone).
- **402, not 403.** 403 already means "your role may not"; 402 *Payment Required* tells a client to show
  an upgrade prompt. The error carries `limit`, `allowed` and the cheapest plan that allows it.
- **Existing orgs start on Free.** Migration 0011 applies Free's limits to data from before Module 3
  (clamp, then freeze beyond the 5 oldest running). It hard-codes 5 and 300 on purpose: a migration is
  history and must not import application code that can change.
- **The runner is due-based now.** `npm run checks:run` checks only monitors whose effective interval has
  passed; `-- --all` checks every running monitor, for trying things out.
- **Count-then-insert can overshoot** by a monitor under concurrency. The lesson accepts that for cheap
  resources; the race-safe version is 3.2's 🔴 exercise.
- **Test fixtures default to Business** (`makeOrg(name, { plan })`), so tests that are not about limits
  are not limited by them.

### Lesson 3.3 — Usage-based billing and metering (🟢 and 🟡)

3.3 is an 🔴 lesson; its 🟢 and 🟡 exercises are done except the parts that need Stripe's servers
(below). The SMS worker itself is Module 4, so the entry point is a function it will call.

**What was built.** `usage_events` (unique `idempotency_key`, `occurred_at`), `recordSmsSent()` for the
SMS worker, a per-billing-period meter shown on the billing and settings pages and in the billing API,
80% / 100% alerts sent once per period, and `npm run usage:report`, which sends events to the provider's
meter with retries.

**Read in this order**

1. `src/core/usage.ts`: keys, billing period, rating, thresholds.
2. `src/db/schema.ts` `usageEvents`, `usageAlerts`; `drizzle/0013_usage.sql`.
3. `src/lib/usage.ts`: `recordSmsSent()` → `recordUsage()`, `getUsageSummary()`, `reportPendingUsage()`.
4. `src/app/[orgSlug]/billing/usage-card.tsx`; `scripts/report-usage.ts`.
5. `tests/usage.test.ts`.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 `usage_events`, one event per SMS keyed by the message SID, "SMS used this period" | running the SMS job twice creates one row | `sms:{sid}` + unique constraint + `ON CONFLICT DO NOTHING`; test and smoke (4 calls, 3 rows) |
| | the count is for the billing period, not the calendar month | period from the subscription (14th → 14th in the test); calendar month only without one |
| | `occurred_at` is the send time | test records an SMS "sent" before the period and inserted now |
| 🟡 report to a Stripe meter with the key as identifier, retries, 80%/100% alerts | replaying the reporting job changes nothing | test resets `reported_at` and reports twice: the fake meter (which dedupes like Stripe) is unchanged |
| | each alert at most once per org per period | `usage_alerts` primary key (org, meter, period, threshold); test |
| | Beacon's count and the meter summary match | test compares `getUsageSummary()` with the fake's `meterSummary()` |
| | a test-clock subscription with 130 SMS gets a $1.50 overage line | **not verified**: needs Stripe. `rateSms()` computes the same $1.50 and is tested; steps are in "Run it with real Stripe" |

**Design decisions to notice**

- **Record when the cost is certain.** `recordSmsSent()` is called after the SMS provider accepted the
  message; recording the decision to send would bill for failures.
- **Report every unit, let Stripe rate it.** The metered price's first tier is free (100 on Pro), so
  Beacon never computes "units beyond included" at report time, and a late event cannot shift the split.
  `rateSms()` does the same arithmetic only for the usage view.
- **A crash between "sent" and "marked reported" is safe**, because the meter drops a second event with
  the same identifier. Failed sends are retried three times with backoff, then left for the next run.
- **Global unique keys.** A key recorded for one org cannot be recorded again for another (tested); keys
  are provider message ids, which are globally unique.
- **Usage is tenant data**: `usage_events` and `usage_alerts` are under row-level security, and the
  reporting job works per org inside `withOrg()` with the network call outside it.
- **Late events.** Aggregation is by `occurred_at`, so a late event lands in its own period on Beacon's
  page; on Stripe's side the invoice's one-hour finalization window is the grace period. Stripe refuses
  meter events older than 35 days, which a daily job never reaches.

### Not done in Module 3 (🔴 exercises and neighbours)

Test clocks, trials, dunning with a grace-period banner and automatic downgrade, and nightly reconciliation
(3.1 🔴); overrides, add-ons and race-safe creation (3.2 🔴); the credit ledger, overage caps and
three-way reconciliation (3.3 🔴). Also: `invoice.payment_failed` / `trial_will_end` emails, a queue for
the webhook's follow-up work and for usage reporting (5.1), the feature gates `sso`, `auditLog` and `api`
are defined but their features arrive in 1.4, 7.3 and 5.2, and the real Stripe path was not exercised
against Stripe here.

### Verification for this branch

`npm test` (287 tests, no database server and no network: PGlite, and the fake billing provider with
webhooks signed by the SDK's `generateTestHeaderString`), `npm run typecheck`, `npm run db:migrate` on a
fresh database and on a database migrated and seeded on `module-2-solution` (plus an org with 8 monitors
at 60 s, one paused by hand: afterwards 5 run, 2 are frozen, the manual pause stays manual, all at
300 s), `npm run build`, and a headless-browser run against `next start` with `BILLING_PROVIDER=fake`
(30 checks): the Free demo org shows 5 of 5 and an upgrade prompt instead of **Add monitor** → the API
answers 402 `limit_exceeded` for a sixth monitor and for a 60-second interval → the edit form disables
30 s and 60 s → forged and unsigned webhooks get 400 → Upgrade → fake Checkout declines 4000…0002, accepts
4242… → back on Beacon, *Confirming your payment…* while still Free → the signed webhook arrives and the
page switches to Pro by itself → 5 of 50, a sixth monitor at 1 minute → three SMS recorded through
`recordSmsSent()` (a fourth, retried one is not) show as *3 of 100 included* in settings and in the billing
API → a member sees no Billing link, gets the 403 page and 403 from the checkout and portal endpoints →
the Portal's *Cancel at period end* shows "cancels on …" and keeps Pro → *Cancel now* moves the org to
Free, freezes the newest monitor, and one downgrade email is logged.

---

## Module 4 — Communication

Modules 1–3 decided who may do what and what they paid for. Module 4 is how Beacon **reaches people**:
email that arrives (4.1), alerts that reach the right person on the right channel without burying them
(4.2), and a dashboard that changes while you look at it (4.3).

```
 check runner ─► recordCheckResult()  ── one withOrg() transaction ──────────────────────────────┐
                   insert check result ─► NOTIFY monitor.status                                     │
                   3 failures in a row ─► incident ─► NOTIFY incident.changed                       │
                   flapping? (>4 changes/h) ─► one "flapping" notification instead                  │
                   notifyInTx(): members with the permission ─► dedupe ─► preferences ─► deliveries │
                                 (+ the org's Slack channel, + confirmed status-page subscribers)  │
                                                                                          COMMIT ───┘
      after commit ─► channel workers: email (suppression, List-Unsubscribe) · SMS (5/h, fallback,
                      recordSmsSent) · Slack ─► each delivery row records status + provider id
      and Postgres delivers the NOTIFYs ─► every app instance ─► SSE ─► open dashboards and bells

 sendEmail() ─► email_outbox ─► worker (after the response, and `npm run messages:send`) ─► SMTP / Resend
                                                          provider webhook ─► email_suppressions ◄┘
```

### Try it by hand

```bash
docker compose up -d                  # Mailpit: SMTP on :1025, inbox on http://localhost:8025
npm run db:reset
SMS_PROVIDER=fake SLACK_PROVIDER=fake npm run dev
```

1. Sign up at <http://localhost:3000/signup>. The verification email is in Mailpit (HTML and a plain-text
   part: open the *Text* tab). Click its link. `npm run email:preview` renders every template to
   `.email-preview/` without sending anything.
2. Sign in as `demo@beacon.test`. The 🔔 in the org navigation is the inbox; **● Live** next to it means the
   live connection is up. Open **🔔 → Preferences**: *Billing and plan* is locked on (required), in-app is
   always on, and SMS is locked because Demo is on Free, which includes no SMS. Put Demo on Pro to try
   SMS (`update organizations set plan = 'pro' where slug = 'demo'`, or upgrade with `BILLING_PROVIDER=fake`),
   then add a phone number such as `+15551234567` and tick *Incident opened → SMS*.
3. Sign in as `member@beacon.test` in a private window and untick every *Email* box.
4. Open `/status/demo` in a third window and subscribe with any address. Confirm from the email in Mailpit.
5. As the owner, keep **Monitors** open. Open *Always broken*, click **Mark resolved** (that notifies: a
   resolved email, a bell count, a status update to the subscriber). Run `npm run checks:run -- --all`
   in a terminal: the tiles change colour while you watch, the incident reopens (the monitor still fails),
   the bell goes up, the owner gets an email and an SMS (printed by the check run), the member gets only
   the in-app notification. **🔔** shows each notification's deliveries: *In-app: sent · Email: sent ·
   SMS: sent*. **Settings** shows *SMS used this period: 1*.
6. Open the same monitor as owner and as member: each sees "👀 … is also viewing this monitor".
7. Stop `npm run dev` for a few seconds: the dashboard says *reconnecting…*, then comes back by itself.
8. In Mailpit, every alert email has `List-Unsubscribe` and `List-Unsubscribe-Post` headers. Clicking the
   footer's *Unsubscribe* opens a page with a button; mail clients POST the header's URL directly.

Without Docker, `EMAIL_DRIVER=console` prints emails in the terminal instead.

### Lesson 4.1 — Transactional email that actually arrives

**What was built.** React Email templates for every email Beacon sends (verification, password reset,
invitation, incident opened/resolved, flapping, SMS held back, plan downgraded, usage alert, subscription
confirmation, status update), each with a plain-text part. One `sendEmail()` that only queues a row in
`email_outbox`; a worker that sends it after the response through an `EmailTransport` (SMTP via nodemailer
to Mailpit in development, Resend's HTTP API in production, `console` and `memory` drivers), with retries
and backoff. A signed bounce/complaint webhook that fills `email_suppressions`, checked before every send,
and a warning on the members page. The `TODO(4.1)` console mailer is gone.

**Read in this order**

1. `src/emails/layout.tsx`, then `src/emails/incidents.tsx`: templates as components.
2. `src/emails/index.tsx`: the registry (subject, sample props, stream, "essential") and `renderEmail()`.
3. `src/lib/email/index.ts`: `sendEmail()` → outbox, `deliverEmail()` (suppression → render → headers →
   transport), `deliverPendingEmails()` (claim with `SKIP LOCKED`, retry, give up).
4. `src/lib/email/transport.ts`, `smtp.ts`, `resend.ts`, `memory.ts`: one interface, four drivers.
5. `src/lib/email/webhook.ts` and `src/app/api/email/webhook/route.ts`: verify, then suppress.
6. `src/lib/jobs.ts` `runAfterResponse()`; `scripts/send-messages.ts`; `scripts/email-preview.ts`.
7. `src/lib/auth.ts`, `src/lib/invitations.ts`: the call sites, now one line each.
8. `tests/email.test.ts`.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 Mailpit + a production provider, React Email templates (verify, invitation, incident opened), one `sendEmail()` choosing SMTP in development and the provider in production | signing up shows the verify email in Mailpit | Mailpit is in `docker-compose.yml`; the smoke test used a local SMTP server in its place (no Docker in the build environment) and followed the link |
| | every template has a plain-text part and renders in a preview | `renderEmail()` renders both from one component; `npm run email:preview`; a test per template checks subject, HTML, text and link |
| | no code outside `sendEmail()` imports the provider SDK | only `src/lib/email/*` knows nodemailer or Resend; a test greps `src/` and `scripts/` |
| 🟡 SPF, DKIM, DMARC; a queued job with idempotency keys; signed bounce/complaint webhooks; `email_suppressions` checked before every send; a warning in the members UI | SPF, DKIM and DMARC pass and align | **not verified**: needs a real domain and a provider account. The records are below |
| | a simulated hard bounce adds a suppression row and no further email is attempted | test and smoke: a signed `email.bounced` (Permanent) → row → the next sends are `suppressed`, the transport is never called; the members page shows ⚠ |
| | a provider outage delays emails without failing requests, and they send after recovery | test: the memory driver in "outage" → `sendEmail()` still resolves, the row stays `pending` with the error and a backoff, then sends once the driver recovers. A bad Resend key throws the same way |

The DNS records for `mail.beacon.app` with Resend (Resend's domain page shows the real values):

```
send.mail.beacon.app             MX   10 feedback-smtp.us-east-1.amazonses.com   (bounces come back here)
send.mail.beacon.app             TXT  "v=spf1 include:amazonses.com ~all"     SPF for the Return-Path domain
resend._domainkey.mail.beacon.app TXT "p=MIGfMA0GCSqGSIb3…"                    DKIM public key, d=mail.beacon.app
_dmarc.beacon.app                TXT  "v=DMARC1; p=none; rua=mailto:dmarc-reports@beacon.app"
```

`From: notifications@mail.beacon.app` aligns (relaxed alignment, same organizational domain) with DKIM's
`d=mail.beacon.app` and SPF's `send.mail.beacon.app`. Status-page mail uses `status@updates.beacon.app`,
a second domain with its own records, so its reputation is separate.

**Design decisions to notice**

- **A table as the queue until 5.1.** `email_outbox` is the job: unique `idempotency_key`, `attempts`,
  `next_attempt_at`, `last_error`. Claiming pushes `next_attempt_at` five minutes ahead (a lease), so a
  crashed worker's rows come back by themselves, and `FOR UPDATE SKIP LOCKED` keeps two workers apart
  (tested). `after()` sends right after the response; `npm run messages:send` from cron catches retries
  and anything a restart lost.
- **The key is the job, not the email.** Asking twice for the same invitation (same invitation, same
  token) queues one email; *Resend* makes a new token and so a new email. The key also goes to the
  provider (Resend's `Idempotency-Key`; over SMTP a Message-ID derived from it), so a retry after a crash
  between "sent" and "marked sent" is dropped there.
- **Templates render at send time.** The row stores the template name and props (plain JSON), so a fixed
  typo reaches queued mail too.
- **Suppression is global, by address.** An address that does not exist does not exist for any org.
  A hard bounce stops everything; a complaint stops everything except "essential" mail (verification,
  password reset) the person asks for themselves. A later hard bounce upgrades a complaint, never the
  reverse. Soft bounces are the provider's to retry and are only logged.
- **Two streams.** Transactional mail from `EMAIL_FROM`, subscriber mail from `EMAIL_FROM_STATUS` on
  another subdomain (the lesson's stream separation).
- **Webhook verification like Stripe's (3.1).** The raw body, an HMAC over `id.timestamp.body` compared in
  constant time, at most five minutes old, several signatures accepted during a rotation. Written out
  (about 20 lines) instead of pulling in the `svix` package, so you can see it; `svix` does the same.
- **Resend was not exercised against its servers** (no internet here). The SMTP driver ran against a real
  SMTP server in the tests (`smtp-server`) and in the smoke test.

### Lesson 4.2 — Notifications: in-app, email, Slack, SMS, and preferences

**What was built.** `notifications` (the inbox), `notification_deliveries` (one row per channel: the job
*and* the delivery log), per-person `notification_preferences`, per-org `org_notification_policies`, and
`status_page_subscribers`, all under row-level security. One entry point, `notify()` / `notifyInTx()`,
called when an incident opens or resolves (automatically or by hand), when a monitor starts flapping, on a
downgrade and on a usage alert. Channel workers for email, SMS (fake provider or Twilio, metered with 3.3's
`recordSmsSent()`, 5 per person per hour with an email fallback) and Slack (incoming webhook, or fake).
Anti-flapping. A bell with an unread count, an inbox with *Mark as read* / *Mark all as read* and delivery
badges, a preferences matrix, the org policy and Slack in Settings, status-page subscription with double
opt-in, and signed one-click unsubscribe links.

**Read in this order**

1. `src/core/notifications.ts`: categories, `resolvePersonalChannels()` (the lesson's resolution order),
   flapping, SMS text and segments. Then `tests/notifications-core.test.ts`.
2. `src/lib/checks.ts` `recordCheckResult()`: check → incident → flapping → `notifyInTx()`, one transaction.
3. `src/lib/notifications/pipeline.ts`: recipients, dedupe, preferences, deliveries.
4. `src/lib/notifications/deliver.ts`: the channel workers, the SMS throttle and its fallback.
5. `src/lib/notifications/providers.ts`: `SmsProvider`, `SlackSender`, fakes, and the Slack URL allowlist.
6. `src/lib/notifications/events.ts`: every event Beacon sends, in one place.
7. `src/lib/notifications/index.ts`: inbox, preferences, org settings. `subscribers.ts`: double opt-in and
   unsubscribe. `src/core/tokens.ts`: signed links.
8. `src/app/[orgSlug]/notifications/`, `src/app/status/[slug]/`, `src/app/unsubscribe/`, `src/app/api/unsubscribe/`.
9. `tests/notifications.test.ts`.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 `notifications` table, `notify()` on open/resolve, bell with unread count, mark as read / all | opening an incident creates exactly one notification per eligible member, even if `notify()` is called twice | unique `dedupe_key` = `incident.opened:<incident>:<user>`; test calls `notify()` again: 0 new rows |
| | the unread count updates after marking as read | `revalidatePath` re-renders the layout's bell; tests; smoke (*Mark all as read* → 0) |
| | members without access to the monitor receive nothing | recipients are members whose role has the category's permission. In Beacon every role may read every monitor (1.3), so for incidents that is every member; tests show outsiders get nothing and that `billing` (needs `billing.manage`) reaches only the owner |
| 🟡 email, Slack and SMS behind a channel router with per-channel jobs; preferences matrix with required categories locked; anti-flapping; SMS throttle with email fallback | a monitor flapping for an hour produces at most a handful of notifications per channel | tests: strictly alternating up/down every 30 s opens nothing (3 failures needed); down 1.5 min / up 30 s for an hour (60 state changes) gives opened, resolved, opened, resolved, *flapping*: 5 per channel |
| | a user who disabled email for "incident resolved" gets no resolved emails but still in-app ones | test; smoke (the member got no email, has the in-app notification with only *In-app: sent*) |
| | the sixth SMS within an hour is replaced by an email saying how many were held back | test: 5 SMS sent, the 6th `throttled`, an `sms-held-back` email "1 SMS alert has been held back" |
| | every delivery attempt is recorded with channel, status and provider message ID | `notification_deliveries`; badges in the inbox; tests; smoke (*In-app / Email / SMS: sent*) |

**Design decisions to notice**

- **Notifications commit with the incident.** The check runner calls `notifyInTx()` inside the
  transaction that opens the incident: both exist or neither. Only rows are written there; sending happens
  after the commit, outside any transaction (2.4's rule).
- **The delivery row is the job.** Email, SMS and Slack each claim their pending rows (`SKIP LOCKED`, a
  lease, backoff, `MAX_ATTEMPTS`), and the same row keeps status, provider id, error and time: the log a
  customer can be shown. In-app is written as delivered, so the log is complete.
- **Resolution order** is the lesson's: required → org policy → the person → default. In-app is always on
  (it is the record). Required categories cannot be turned off by the form, a hand-made POST or an
  unsubscribe link (tested). Cells the form shows as locked keep the person's choice when saved.
- **SMS is an entitlement (3.2).** Free includes no SMS and has no subscription to bill overage to, so the
  pipeline switches SMS off below Pro and the preferences page says why. A sent SMS is metered with
  `recordSmsSent()` (message SID as key; the fake's SID is derived from the delivery, so a retry is not
  billed twice). Alert texts are ASCII, and the link drops its `#fragment`: the smoke test caught a
  typical alert costing two segments.
- **Flapping lives in the domain**, next to the incident decision: 3 failures to open (was 2), and more
  than 4 state changes within an hour marks the monitor (`flapping_since`), sends one *flapping*
  notification and holds back the rest until it has been quiet for an hour.
- **Slack is the org's channel**, one message per event, not per member. The webhook URL is a secret: never
  sent back to the browser, only `https://hooks.slack.com/services/…` accepted (anything else would let an
  admin make Beacon call internal addresses: SSRF). Posting to Slack with OAuth, threads and an
  *Acknowledge* button is 5.3 and 4.2 🔴.
- **Links that work without a login** are signed, not stored: an HMAC over the payload with the app
  secret (`src/core/tokens.ts`). They can only switch mail *off*, or confirm a subscription. A GET never
  changes anything (link scanners open every link): pages show a button; mail clients use the one-click
  POST (RFC 8058).
- **Status-page subscribers are not users.** Double opt-in, the same answer whether or not an address is
  subscribed, one confirmation per address per 10 minutes and 30 per page per hour, and mail from the
  status stream. Fan-out is plain rows here; batched, throttled fan-out for 10,000 subscribers is 4.1 🔴.
- **SMS throttle per person per org.** Deliveries are tenant rows under RLS, so "5 per hour" is counted
  within one org. Two workers racing could both send a sixth; acceptable at this size.

### Lesson 4.3 — Real-time (🟢 and 🟡)

4.3 is an 🔴 lesson; its 🟢 and 🟡 exercises fit Beacon well. Its 🔴 exercise (a Yjs/Hocuspocus
postmortem editor and optimistic locking) is left as a stretch goal.

**What was built.** Live updates over Server-Sent Events, fanned out through **Postgres
`LISTEN/NOTIFY`**: the check runner (another process) and the app publish per-org events inside their
transactions; every app instance listens once per org and forwards to its browsers. An authorized SSE
endpoint that re-checks access every 30 seconds. One connection per tab with exponential backoff and full
jitter, resync on every reconnect, monitor tiles updated in place, a live bell, a *Live* indicator, and
presence on the monitor page.

**Read in this order**

1. `src/lib/realtime.ts`: `publishInTx()`, `subscribe()`, why NOTIFY, and its limits.
2. `src/lib/checks.ts` and `src/lib/notifications/pipeline.ts`: where events are published.
3. `src/lib/realtime-stream.ts` and `src/app/api/orgs/[orgSlug]/events/route.ts`: the stream.
4. `src/app/[orgSlug]/realtime.tsx`: `RealtimeProvider`, backoff, resync. `src/core/retry.ts` `reconnectDelayMs()`.
5. `src/app/[orgSlug]/monitors/live-monitor-list.tsx`, `notification-bell.tsx`, `monitors/[id]/live.tsx`.
6. `src/lib/presence.ts` and `src/app/api/orgs/[orgSlug]/presence/route.ts`.
7. `tests/realtime.test.ts`, and the new cases in `tests/cross-tenant-routes.test.ts`.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 SSE instead of polling: the worker publishes `monitor.status` to the org's channel, an authorized endpoint forwards it, the tile updates in place, the list is refetched on reconnect | a monitor going down turns red on an open dashboard within about a second, without polling | smoke: `npm run checks:run` in another process → the tile turns red, same document (no reload) |
| | a non-member gets 403 from the SSE endpoint | **404**, like every org route in Beacon (lesson 1.2: outsiders cannot learn an org exists); anonymous 401. Tests and smoke |
| | restarting the server makes dashboards reconnect and resync | smoke: instance B killed → *reconnecting…*; the incident resolved meanwhile on A; B restarted → *Live* again and the tile shows the missed change |
| 🟡 two instances, presence with TTL heartbeats, backoff with jitter, removed members disconnected within a minute | an event published on instance A reaches clients connected to instance B | smoke: **Mark resolved** on :3100 updates a dashboard on :3101 (and the check runner is a third process) |
| | presence updates within a few seconds, stale entries expire | heartbeat every 10 s, 30 s TTL, join/leave events, `DELETE` with `keepalive` on `pagehide`; tests and smoke |
| | killing an instance spreads reconnects over several seconds | full jitter; a test draws 10,000 delays for one attempt and finds them spread evenly (not measured with real browsers) |
| | a removed member's open dashboard stops receiving events | the stream re-checks membership, role and session every `REALTIME_RECHECK_MS` (30 s): `event: revoked`, stream closed; tests (removal, sign-out) and smoke |

**Design decisions to notice**

- **`LISTEN/NOTIFY` instead of Redis**, because Beacon has no Redis yet and Postgres has two properties
  worth teaching: a `NOTIFY` inside a transaction is delivered **only if it commits** (tested), so a
  published event can never describe a rolled-back write; and it already reaches every process connected
  to the database, which is what "fan out across instances" needs.
- **Signals, not secrets.** Events carry ids and states. The tile updates its dot and latency; anything
  else (the incident's cause, the list after a reconnect) is refetched through the normal authorized page.
  `notification.created` carries a user id and is forwarded **only** to that user's streams; others are not
  even told it happened (tested).
- **Authorize the channel, and keep authorizing it.** The route runs `requirePermission()` before any
  stream exists; the stream listens only on its org's channel (`beacon_org_<id>`); and it asks again every
  30 s. A single membership row deleted in SQL ended the member's stream in the smoke test.
- **One connection per tab.** Browsers allow about six HTTP/1.1 connections per origin, so the dashboard,
  the bell and presence share one `EventSource` through React context. The client closes it on error and
  reconnects itself (EventSource's own retry has no jitter), and every `ready` after the first triggers a
  refetch: pub/sub does not replay what was missed.
- **Presence in a table, not Redis TTL keys**: `presence(org, topic, user, last_seen_at)` under RLS,
  "viewing" = seen in the last 30 s, rows older than 5 minutes deleted on the next heartbeat. Approximate
  on purpose, like the lesson says.

**How it scales, and when to switch**

- *Today:* each app instance holds **one** extra Postgres connection for all its `LISTEN`s (postgres.js
  multiplexes channels on it) and one `LISTEN` per org that has a viewer on that instance; browsers hold
  sockets on the Node process, not database connections. The 25-second ping keeps load balancers (idle
  timeouts are often 60 s) from closing quiet streams.
- *Limits of NOTIFY:* payloads under 8,000 bytes (ours are ~150); a transaction that notifies takes a
  global lock at commit, so thousands of notifying commits per second serialize; the `LISTEN` connection
  must be a direct (session) connection, not through PgBouncer in transaction mode; and delivery is
  fire-and-forget: a listener that is down misses events (hence resync). A very slow listener can fill the
  8 GB notification queue, after which `NOTIFY` fails.
- *Next step:* Redis pub/sub (the lesson's default) behind the same two functions: `publishInTx()` becomes
  "write an outbox row, publish after commit" (5.3), `subscribe()` a Redis subscriber on `org:<id>`.
  Redis Streams or Centrifugo add history, so a reconnecting client can catch up by event id instead of
  refetching. Re-authorizing each stream every 30 s is one membership query and one session lookup per
  stream; at tens of thousands of streams, push a "membership changed" event instead of polling.
- *Public status pages* stay server-rendered and uncached-per-request here. At 50,000 viewers they should
  be CDN-cached with a short TTL, not 50,000 streams (the lesson's advice); not built.

### Not done in Module 4 (🔴 exercises and neighbours)

Per-tenant sending domains, the 10,000-subscriber batched fan-out on its own stream (4.1 🔴); escalation
policies, acknowledgement from Slack or SMS, digests, and an incident timeline of deliveries (4.2 🔴; the
delivery log is there to build it on); the Yjs/Hocuspocus postmortem editor and optimistic locking for
monitor settings (4.3 🔴). Also: SPF/DKIM/DMARC not verified and Resend, Twilio and Slack not exercised
against their servers (no domain or internet here; all three are behind interfaces and ran through fakes or
a local SMTP server); push notifications and quiet hours; STOP keyword handling for SMS; soft-bounce counting;
emails and times in the recipient's timezone and locale; a real job queue for the outbox and deliveries
(5.1); presence and streams through Redis.

### Verification for this branch

`npm test` (386 tests, no database server and no network: PGlite, whose `LISTEN/NOTIFY` the realtime tests
use, a local SMTP server for the SMTP driver, fake SMS and Slack providers), `npm run typecheck`,
`npm run db:migrate` on a fresh database and on a database migrated, seeded and checked on
`module-3-solution` (then the checks opened an incident and notified: 4 in-app and 4 email deliveries),
`npm run build`, and a headless-browser run against two `next start` instances on one database, with a
local SMTP server standing in for Mailpit and the fake SMS and Slack providers (42 checks): sign-up →
multipart verification email over SMTP → its link verifies the address → the owner adds a phone number
and turns on SMS, the member turns off email → a status-page subscription is confirmed from its email →
owner and member see each other on the monitor page → **Mark resolved** on instance A updates a dashboard
on instance B and its bell → a check run in another process turns a tile red and shows the new incident
without a reload → the owner gets the alert email (with `List-Unsubscribe` and `List-Unsubscribe-Post`),
an SMS recorded as one usage event (*1 of 100 included*), and in-app; the member only in-app; the subscriber
a status email from the status stream → *Mark all as read* → another org's user got no events on an open
stream, no notifications, 404 from the demo org's event stream and inbox API → instance B is killed,
the dashboard reconnects by itself after the restart and shows what changed meanwhile → one-click
unsubscribe removes the subscriber → a forged bounce webhook is refused, a signed hard bounce suppresses
`member@beacon.test` and the members page warns about it → deleting the member's membership ends their
live stream within seconds.

---

## Module 5 — Background Work & Integrations

Modules 1–4 answered requests. Module 5 is the work that happens when nobody is looking: a **queue and a
worker** that check every monitor on schedule and send every message with retries (5.1), a **public API**
that other software calls with keys (5.2), **webhooks** that Beacon sends to other software, through a guard
that keeps customer URLs out of our network (5.3), and **durable workflows** for processes that wait, like an
escalation (5.4).

```
 pg-boss cron (1/min) ─► checks.schedule ─► check.run jobs, one per monitor slot (stable phase = jitter,
                                            id = hash(monitor, slot), grouped by org: ≤ 5 at once)
 worker ─► runCheck() through safeFetch (SSRF guard) ─► recordCheckResult() ── one withOrg() transaction ─┐
             result (unique per slot) ─► incident ─► incident-notify workflow run   ─► workflow.run job   │
                                                 ─► webhook event + messages      ─► webhook.deliver jobs │
                                                 ─► incident-escalation run (if the org has a policy)     │
                                                                                                 COMMIT ─┘
 workflow.run ─► load-incident ─► notify-channels (notifications + deliveries + notification.deliver jobs)
               ─► record-deliveries                     escalation: page tier ─► wait (no worker held)
                                                        ◄── "Acknowledge" / resolve: a signal wakes it
 notification.deliver / email.send / webhook.deliver ─► provider or customer URL; throw = retry with
                                                        backoff and jitter; last attempt = dead letter
 /api/v1 ─► IP bucket ─► API key (hash) ─► plan `api` ─► scope ─► org bucket ─► handler ─► problem+json
```

Everything enqueued above is an `INSERT` in the same transaction as the data it is about: that is the
reason for a Postgres queue.

### Try it by hand

```bash
docker compose up -d
npm run db:reset                      # migrations, then pg-boss's schema and Beacon's queues
psql "$DATABASE_URL" -c "update organizations set plan = 'business' where slug = 'demo'"   # the API is a Business feature
SMS_PROVIDER=fake npm run dev         # terminal 1
npm run worker                        # terminal 2: checks run by themselves from now on
npm run jobs                          # terminal 3, any time: the queues
```

1. Watch terminal 2: every minute `checks.schedule` enqueues the checks due in the next 90 seconds, and each
   `check.run` logs its result at its monitor's own second of the interval. Nobody runs a script.
2. Sign in as `demo@beacon.test`. **Settings → API keys**: create a key with all three scopes. It is shown once.
   ```bash
   KEY=bk_live_…
   curl -s localhost:3000/api/v1/monitors?limit=2 -H "Authorization: Bearer $KEY"          # a page + next_cursor
   curl -si localhost:3000/api/v1/monitors -H "Authorization: Bearer $KEY" -H 'Idempotency-Key: 1' \
        -H 'content-type: application/json' -d '{"name":"Local","url":"http://localhost:3000","interval_seconds":30}'
   # run it again: the same body, `Idempotent-Replayed: true`, still one monitor
   curl -si localhost:3000/api/v1/monitors -H "Authorization: Bearer $KEY" -H 'content-type: application/json' \
        -d '{"name":"x","url":"http://169.254.169.254/latest/meta-data/"}'   # 400 problem+json: blocked-url
   for i in $(seq 130); do curl -s -o /dev/null -w '%{http_code} ' localhost:3000/api/v1/monitors -H "Authorization: Bearer $KEY"; done   # …200 200 429
   ```
   <http://localhost:3000/docs/api> renders the reference (Scalar, from `/api/v1/openapi.json`). Revoke the key
   in Settings and the next `curl` is a 401.
3. **Settings → Webhooks**: add an endpoint. For a local receiver, allow it first: `OUTBOUND_ALLOWLIST=localhost:3000,127.0.0.1:4555`
   (restart both processes) and run a 10-line Node receiver on port 4555 that logs what it gets. `http://127.0.0.1/`,
   `http://169.254.169.254/` and `http://[::1]/` are refused. Copy the `whsec_` secret.
4. **Settings → Escalation policy**: tier 1 = the member, wait 2 minutes; tier 2 = you.
5. Break a monitor (a URL that answers 500). Three checks later: the incident, a signed `incident.opened` POST to
   your receiver, an email "Escalation tier 1" to `member@beacon.test` in Mailpit. Make the receiver answer 500:
   `npm run jobs` shows `webhook.deliver … attempt 2 of 18 failed, next at …`, and the endpoint's delivery log
   shows every attempt with its status and the start of the response. Fix it and click **Resend**, or
   **Replay failed** for everything since yesterday.
6. As the member, open the monitor and click **Acknowledge**: the escalation run ends within seconds
   (`acknowledged`), tier 2 is never paged, and the incident row's **Workflows** list shows both runs step by
   step. The incident timeline says who was told, who was paged and who acknowledged.
7. Stop the worker with Ctrl+C in the middle of an escalation's wait, start it again: the run continues where it
   was (the deadline is in its history; the wake-up is a delayed job).

### Lesson 5.1 — Background jobs, queues and scheduled tasks

**What was built.** [pg-boss](https://github.com/timgit/pg-boss) in its own `pgboss` schema, installed by
`npm run db:migrate`. Queues as data (`src/lib/queue/queues.ts`) with retries, exponential backoff with jitter
and a dead-letter queue. `enqueue()` and `enqueueInTx()` (the job commits with the rows it is about). A worker
process (`npm run worker`) with per-queue concurrency and a per-org cap. The check scheduler: a cron job every
minute that enqueues one `check.run` job per monitor slot. Every Module 3/4 background task moved onto the queue:
the email outbox, notification deliveries, thumbnails and usage reporting; `runAfterResponse()`,
`npm run messages:send` and `npm run files:process` are gone. `npm run jobs` is the dashboard.

**Why pg-boss (and not Graphile Worker).** Both are Postgres queues with transactional enqueue, the lesson's
default. pg-boss fits these exercises more directly: **dead-letter queues** with redrive are built in (Graphile
Worker keeps permanently failed jobs in its table, and you build the DLQ view yourself); **group concurrency**
gives per-tenant fairness in one option; **deterministic job ids** and singleton policies give dedupe; its
**cron** takes a lock; and it ships adapters for **Drizzle** (enqueue inside our transaction) and **PGlite**
(so `npm test` runs the real queue SQL with no database server). Graphile Worker is faster at very high rates
(LISTEN/NOTIFY, one SQL function per job) and its `add_job()` is a plain SQL call, which is lovely inside a
transaction; if you already use PostGraphile, pick it. Both beat Redis here: no second system to run, persist
and monitor, and no outbox to build.

**Read in this order**

1. `src/lib/queue/queues.ts`: every queue, its retry policy, what each job carries (ids, not objects).
2. `src/lib/queue/index.ts`: `getBoss()`, `enqueue()`, `enqueueInTx()`; `install.ts`: the schema, the queues
   and what `beacon_app` may do (insert jobs, nothing else).
3. `src/core/ids.ts` `stableUuid()` and `src/core/schedule.ts` `phaseOffsetSec()` / `checkSlots()`.
4. `src/lib/scheduler.ts`: `scheduleChecks()`, `runScheduledCheck()`; `src/lib/checks.ts`: the slot-unique result.
5. `src/lib/email/index.ts` `sendEmail()` / `sendQueuedEmail()`; `src/lib/notifications/deliver.ts`
   `deliverNotification()`; `pipeline.ts` `enqueueDeliveries()`.
6. `src/lib/queue/handlers.ts`, `worker.ts` (concurrency, groups, `requeueOrphans()`), `run.ts`; `scripts/worker.ts`,
   `scripts/jobs.ts`, `src/lib/queue/status.ts`.
7. `tests/queue.test.ts`, the queue cases in `tests/email.test.ts` and `tests/notifications.test.ts`, and
   `tests/queue.integration.test.ts` (a real Postgres, when `DATABASE_URL` is set: CI).

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 the checker writes the incident and enqueues a notify job; a separate worker sends; 8 attempts, exponential backoff, dead letter | the checker path makes no email, Slack or SMS call | `recordCheckResult()` only writes rows and jobs; test: three failures, then no mail, no SMS, no Slack post and no notification until the job runs |
| | a bad email provider causes retries visible in the queue dashboard, and the job succeeds after | tests (email outage → `retry` state with the error and a later `start_after` → recovers, `attempts = 2`); smoke: `npm run jobs` listed the failing webhook as "attempt n of 18 failed, next at …, HTTP 500" |
| | a job that fails every attempt ends in the DLQ with its error | tests: 8 attempts → the email row `failed`, the job `failed` with its error, a copy in `dead-letter`; `queueStatus()` lists it with the error; redrive puts it back |
| 🟡 `notification_deliveries` unique per (incident, recipient, channel); enqueue in the same transaction | running the same job twice sends each subscriber one email | the unique `dedupe_key` (Module 4) + "only a pending delivery is sent"; tests run the fan-out and a delivery job twice |
| | a crash between "incident committed" and "job enqueued" still notifies | there is no between: `enqueueInTx()` is an INSERT in the incident's transaction; test: a transaction that throws after enqueuing leaves no job, and one that commits leaves exactly one |
| | a test proves the handler is a no-op for an incident that no longer exists | test: monitor deleted after the incident → `{ skipped: 'incident deleted' }`, no notifications, no deliveries |

**Design decisions to notice**

- **The scheduler decides, the workers check.** Every minute one job (pg-boss cron takes the lock) looks 30 s
  back and 90 s ahead and enqueues each monitor's slots. Overlapping windows cost nothing, because a slot's job
  id is `hash(monitor, slot)`: enqueuing it twice adds one job. A worker outage skips missed slots instead of
  running a backlog of stale checks. The per-monitor phase (`hash(id) % interval`) spreads 6,000 one-minute
  monitors to about 100 per second (tested) instead of 6,000 at `:00`.
- **Idempotent handlers, in three ways.** Deterministic job ids (the same work is one job), "only a pending row"
  (email, delivery, webhook message, file), and unique constraints on the effect (check results per slot,
  deliveries per event/person/channel).
- **The queue owns retries; the row keeps the log.** Module 4's hand-made lease and `next_attempt_at` are gone
  (migration 0017). The row records attempts, the last error and the outcome; on the last attempt it is marked
  `failed`. A handler throws to ask for a retry. It commits its log first: a throw inside a transaction would roll
  the log back.
- **Fairness.** Jobs carry a group: the org for checks and deliveries, the endpoint for webhooks, the run for
  workflows. `groupConcurrency` caps how many of one group run at once across all workers (5 checks per org, 2
  deliveries per endpoint, 1 job per workflow run). That is a first step; the 🔴 5 % cap and sharded
  schedulers are not built.
- **Least privilege for jobs.** `beacon_app` (the role tenant queries run as) may insert jobs and read back their
  id: it cannot read other orgs' payloads or change jobs (tested). The worker connects as the owner.
- **Upgrading from Module 4.** Pending rows of Module 4 have no jobs. The worker's start-up check enqueues one
  per pending email, delivery and processing file, with the same deterministic ids, so it adds nothing when
  every row already has its job. Tried on a database migrated on `module-4-solution`: 8 queued emails were sent.
- **Tests run pg-boss on PGlite** (its adapter), and `runQueuedJobs()` is "the worker, once": same claim, same
  complete/fail, same backoff. One PGlite caveat: a single connection, so the queue client must already have
  every queue in its cache before a transaction enqueues (test-db starts it after installing the queues).

### Lesson 5.2 — The public API: API keys, versioning and rate limits

**What was built.** `/api/v1/monitors` (list, create, get, update, delete) and `/api/v1/incidents` (list, get),
separate from the dashboard's `/api/orgs/…` JSON: snake_case, prefixed ids (`mon_…`, `inc_…`), gated by the
plan's `api` entitlement. API keys managed in **Settings → API keys** by roles with the new
`integration.manage` permission. Cursor pagination, RFC 9457 problem details for every error,
`Idempotency-Key` on POST, token-bucket rate limits per IP and per org, the OpenAPI document generated from
the Zod schemas, served at `/api/v1/openapi.json`, rendered by Scalar at `/docs/api` and committed as
`docs/openapi.json`.

**Read in this order**

1. `src/core/api-keys.ts`: format, hash, scopes and which permission each needs.
2. `src/lib/api-keys.ts`: create (returns the key once), list, revoke, `verifyApiKey()`, last-used.
3. `src/lib/public-api.ts`: `publicApi()` (the order of checks), `problem()`, `idempotent()`, the response shapes.
4. `src/app/api/v1/…`: the handlers, each a few lines.
5. `src/core/rate-limit.ts` (the bucket arithmetic) and `src/lib/rate-limit.ts` (the row lock).
6. `src/core/api-schemas.ts`, `src/core/openapi.ts`, `src/core/problems.ts`, `scripts/openapi.ts`.
7. `src/lib/monitors.ts` `listMonitorsPage()`, `src/lib/incidents.ts` `listIncidentsPage()`.
8. `src/app/[orgSlug]/settings/api-keys/`; `tests/public-api.test.ts`.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 `GET`/`POST /v1/monitors` with org-owned keys, prefixed `bk_live_`, SHA-256 at rest, shown once, revocable | `api_keys` has no plaintext keys | `key_hash`, `key_start` (12 chars), `key_last4` only; test dumps the table; smoke: `sha256(key)` matches, the key's middle is nowhere |
| | a revoked key gets 401 within one request | no cache: every request looks the hash up; test and smoke |
| | org A's key never reads org B's monitors (a test) | `tests/public-api.test.ts`: org B's key against every `/api/v1` route (404 or no data), and a check that fails when a new route has no case; smoke: GET/PATCH 404, list without A's monitor |
| | cursor pagination with a maximum `limit` | `starting_after` / `has_more` / `next_cursor`, keyset on `(created_at, id)` compared inside Postgres; `limit` ≤ 100 (400 above); test walks 7 monitors in pages of 3 and adds one mid-walk without a shift |
| 🟡 schemas once, OpenAPI generated, Scalar at `/docs/api`, RFC 9457, `Idempotency-Key` | a CI step fails if the spec changes without being committed | `npm run openapi:check` in `.github/workflows/ci.yml`; a unit test compares too |
| | every 4xx/5xx is `application/problem+json` with `type`, `title`, `status` | `errorToProblem()`; tests for 400, 401, 402, 403, 404, 409, 422, 429 |
| | the same POST twice with the same key creates one monitor and returns the same body twice | key claimed with an INSERT, response stored as text and replayed byte for byte with `Idempotent-Replayed: true`; 409 while the first runs, 422 for a different body, released after an error; tests and smoke |

Also built, from 5.2's 🔴 exercise because the task asked for it: a token bucket per org **sized by plan**
(`apiRequestsPerMinute`: Business 120; a plan change is config only), a per-IP bucket before authentication,
and `RateLimit`/`RateLimit-Policy` (IETF draft) plus `X-RateLimit-*` on every response, `Retry-After` on 429.
Not built: a separate limit for an expensive endpoint and date-based versions (`Beacon-Version`).

**Design decisions to notice**

- **The key decides the org.** Nothing in the URL or body can name another org; `organizationId` in a POST body
  is ignored (tested). A key acts as an integration, not a person: `monitors:write` maps to
  `monitor.write_any`, so only owners and admins can grant it, and a key can never do more than the role that
  created it (`canGrantScopes`). Monitors it creates record the key's creator as author.
- **`api_keys` is not under row-level security**, like memberships: the key is how the request finds its org.
  The lint test's list of exceptions names it; everything else new is under RLS.
- **Additive changes only.** Lesson 5.4 added `acknowledged_at` to the Incident: a new field in v1, no rename.
  The generated schema drops `additionalProperties: false` from responses for that reason: clients must accept
  fields they do not know yet.
- **Rate limits in Postgres**, one row per bucket locked for the instant of the update, so all app instances
  share it. At high traffic this moves to Redis (the lesson's default) behind the same function.
- **Scalar from its CDN**, pinned. Installing it is 47 MB of dependencies for one page. Offline, `/docs/api` falls
  back to a link to the JSON.

### Lesson 5.3 — Outbound webhooks and third-party integrations (🟢 and 🟡)

**What was built.** Endpoints per org (URL, event types, a `whsec_` secret shown once) in **Settings →
Webhooks**. `incident.opened`, `incident.acknowledged` and `incident.resolved` become an event row, a message per
subscribed endpoint and a `webhook.deliver` job each, in the incident's transaction. Deliveries are signed per
Standard Webhooks, go through the SSRF guard with no redirects and a 10 s timeout, and are retried 18 times over
about a day and a half. A delivery log per endpoint (every message and attempt, **Resend**, **Replay failed
since…**, enable, disable, delete). An endpoint that failed every delivery for 5 days is disabled and the owners
and admins are emailed. The SSRF guard also covers every monitor check (the `TODO(5.3)` in `src/core/check.ts`)
and monitor URLs when they are saved.

**Read in this order**

1. `src/core/ssrf.ts` (which addresses) and `src/core/safe-fetch.ts` (resolve, check, pin, redirects).
2. `src/core/check.ts`, `src/lib/monitors.ts` `assertMonitorUrl()`.
3. `src/core/webhooks.ts`: event types, secret, signature, when to disable.
4. `src/lib/webhooks.ts`: `recordWebhookEvent()`, `deliverWebhook()`, `resendMessage()`, `replayFailedSince()`.
5. `src/db/schema.ts` `webhookEndpoints` … `webhookAttempts`; `drizzle/0019_webhooks.sql`.
6. `src/app/[orgSlug]/settings/webhooks/`; `src/emails/integrations.tsx`.
7. `tests/ssrf.test.ts`, `tests/webhooks.test.ts`.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 endpoints with event types and a `whsec_` secret shown once; one signed delivery job per matching endpoint, 10 s timeout, retries | a receiver using the official Standard Webhooks library verifies the signatures | tests and smoke verify with the `standardwebhooks` npm package; our signer and the library's agree byte for byte |
| | an endpoint returning 500 is retried with growing delays, and the attempts are stored | test: 4 attempts, each delay longer, same `webhook-id`, each attempt in the log with status and body; smoke: the receiver saw the retries |
| | a slow endpoint does not delay other endpoints | jobs grouped by endpoint (at most 2 slots of 10 each), 10 s timeout per attempt; the test checks the grouping and the config, not a stopwatch |
| 🟡 the delivery log with resend and replay; a guard that resolves DNS, rejects private/loopback/link-local/CGNAT (v4 and v6), pins the address, refuses redirects for webhooks | `127.0.0.1`, `169.254.169.254`, `[::1]` or a name resolving to `10.x` fail, for webhooks and monitors | tests for both (plus `0x7f000001`, `2130706433`, `::ffff:127.0.0.1`, IPv6 ULA, a redirect to the metadata service); smoke through the UI and the API |
| | a customer replays yesterday's failed messages from the UI | "Replay failed since" (default: 24 hours ago); test and smoke |
| | endpoints failing continuously for 5 days are disabled and admins emailed | `failing_since` on the endpoint, cleared by any success; test sets it 5 days back: disabled, `webhook-disabled` email to the owner and the admin only; new events skip it; re-enable is one click |

**Design decisions to notice**

- **The check is the lookup.** The HTTP agent's DNS lookup resolves, checks every address and hands the
  connection only those, so there is no second resolution for DNS rebinding to exploit. An IP in the URL skips
  the lookup and is checked before the request. Redirects are followed by hand (monitors, 5 hops, each checked)
  or not at all (webhooks). IPv4-mapped IPv6 is caught by Node's `BlockList`; NAT64, 6to4 and Teredo prefixes are
  refused outright. `OUTBOUND_ALLOWLIST` is the development escape hatch (a local receiver, Beacon monitoring
  itself). Production-grade is an egress proxy (Smokescreen) on top, not instead.
- **Monitors may point at hosts that do not resolve right now** (that is what monitors are for); webhook
  endpoints must resolve when they are saved.
- **The Svix data model:** event (immutable, what happened) → message (per endpoint; its id is `webhook-id`, the
  same on every retry) → attempts (the log). Fat payloads in the public API's shapes: one contract.
- **The secret must be readable to sign**, so unlike an API key it cannot be hashed. It is shown once and never
  sent back to the browser. `TODO(8.1)`: encrypt it at rest, like the Slack URL.
- **Machines get every change.** Webhook events are recorded even while a monitor is flapping; only people are
  spared the noise (lesson 4.2).
- **Slack stays Module 4's incoming webhook**; the OAuth app with an Acknowledge button is 5.3's 🔴 exercise.

### Lesson 5.4 — Workflow engines and durable execution (🟢 and 🟡)

5.4 is an 🔴 lesson; its 🟢 and 🟡 exercises are done, on a small engine built on the 5.1 queue instead of
Inngest, Trigger.dev or Temporal: the course repo must run with Postgres alone, and the engine is short enough
to read. The lesson's advice still stands: in production, use an engine (Temporal, Inngest, Trigger.dev,
Hatchet, DBOS) that already solved versioning, observability and scale.

**What was built.** `src/lib/workflows/engine.ts`: runs, steps (the recorded history) and signals in Postgres.
Each `workflow.run` job replays the workflow function from the top; a step already in the history returns its
recorded result, the first missing one runs; `waitForSignal()` records its deadline once, then suspends the run
(the job ends, a delayed job or a signal wakes it). The incident fan-out from 5.1 became the `incident-notify`
workflow with three steps. Escalation policies as data (**Settings → Escalation policy**) and one
`incident-escalation` workflow that interprets them. **Acknowledge** on incidents. Each incident's runs, step by
step, on the monitor page.

**Read in this order**

1. `src/lib/workflows/engine.ts`, the header comment first.
2. `src/lib/workflows/incident-notify.ts`, then `src/lib/workflows/escalation.ts` (read the workflow top to
   bottom: that is the policy); `src/core/escalation.ts`.
3. `src/lib/monitors.ts` `acknowledgeIncident()` and the `signalRunsInTx()` calls in `resolveIncident()` and
   `recordCheckResult()`.
4. `src/lib/notifications/pipeline.ts` `pageInTx()`.
5. `src/app/[orgSlug]/settings/escalation/`, `src/app/[orgSlug]/monitors/[id]/workflow-runs.tsx`.
6. `tests/workflows.test.ts`.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 the "incident opened" fan-out as a workflow: load incident, notify channels, record deliveries | the engine's dashboard shows each run with per-step inputs, outputs and timings | the incident row's **Workflows** list (from `workflow_steps`); test checks names, outputs, timings |
| | killing the worker after step 2 does not re-send notifications | test removes step 3 from the history and resumes: step 2 is replayed, no new deliveries, one email per person |
| | a failing step retries on its own without re-running earlier steps | test: a step that throws once; after the retry, steps 1 and 2 ran once, step 3 twice (`attempts = 2`) |
| 🟡 escalation policies as data plus one durable workflow; snapshot; wait for acknowledged or resolved | acknowledging in the dashboard stops the escalation within seconds | the signal is stored and a `workflow.run` job enqueued in the acknowledging transaction; test and smoke (the run ended right after the click; tier 2 was never paged, even past tier 1's deadline) |
| | resolving before any ack cancels the remaining tiers | `incident.resolved` signal from both resolve paths; test |
| | editing the policy mid-incident does not affect the running escalation, but the next | step `load-policy` records the snapshot; test edits between tiers |
| | SMS sends use an idempotency key derived from run and tier | the page's key is `escalation:<run>:tier-<n>`; the SMS delivery's dedupe key (the provider's idempotency key since this module) extends it; test re-runs the step: one SMS |

Acknowledging from Slack is not built (the Slack app is 5.3 🔴).

**Design decisions to notice**

- **Replay, not snapshots of memory.** The workflow is ordinary code; only `ctx.step()` and `ctx.waitForSignal()`
  touch the world. The rules that follow: no I/O, clock or randomness outside steps; step names are the history's
  keys (rename one and runs in flight lose their place: version by adding a new workflow name); steps must be
  idempotent (a crash between "done" and "recorded" runs one again).
- **A wait costs nothing.** The run's status is `waiting` with its `wake_at`; the only thing in the queue is a
  delayed job with a deterministic id. One job per run at a time (group = run), so a timer and a signal arriving
  together do not replay the same run in parallel. A second of clock tolerance covers the database and the worker
  disagreeing about "now".
- **Signals are stored**, so a run that reaches its wait after the acknowledgement still sees it; before every
  tier the workflow checks without waiting.
- **Pages ignore preferences, not permissions.** The policy chose the people and channels, so the new
  `incident.escalated` category is required; recipients must still be members who may see incidents, and SMS
  still needs a plan that includes it.
- **The fan-out became a workflow** instead of 5.1's plain `incident.notify` job: same transactional start, same
  retries, now with a history. Its third step writes "Alert sent: 4 in-app, 3 email" on the incident's timeline
  (4.2's 🔴 "timeline of deliveries", in one line).

### Not done in Module 5 (🔴 exercises and neighbours)

The sharded scheduler with `next_run_at`, two schedulers taking over each other's shards and a 5 % per-org cap
(5.1 🔴; a per-org cap of 5 concurrent checks is there); date-based versions with a transformer and a separate
limit for an expensive endpoint (5.2 🔴; plan-sized rate limits are there); the Slack OAuth app with an
Acknowledge button, encrypted tokens and uninstall handling (5.3 🔴); the custom-domain saga and workflow
versioning (5.4 🔴). Also: secret rotation with two signatures, webhook retention as a plan feature, a web
dashboard for the queue behind admin auth (7.1), queue alerts on the oldest job's age (7.2), an egress proxy,
OAuth apps for third parties, encryption of webhook secrets (8.1), and Scalar was not rendered in the smoke test
(no CDN access here; the page and the JSON were).

### Verification for this branch

`npm test` (498 tests and 2 more with `DATABASE_URL`, 500 in CI: no database server needed, pg-boss runs on
PGlite; `tests/queue.integration.test.ts` runs a real worker and the app's own driver against Postgres when
`DATABASE_URL` is set), `npm run typecheck`, `npm run openapi:check`, `npm run db:migrate` on a fresh database
(twice: idempotent) and on a database migrated, seeded and checked on `module-4-solution` with a broken SMTP
server (8 pending emails; after the migration the worker's start-up check queued and sent all 8),
`npm run build`, and a smoke test against `next start` plus `npm run worker` (41 checks), with a local SMTP
server for Mailpit and local receivers allowed through `OUTBOUND_ALLOWLIST`: checks run on schedule with no
trigger, one job per slot → the seed's `localhost` monitor fails with "Blocked: … loopback address" → an API key
created in Settings, shown once, hash-only in the database → `curl`: a page of 2 with a cursor and the next page,
RateLimit headers, 401 problem+json without a key, 201 and an identical replay for the same `Idempotency-Key`
(one monitor), 400 `blocked-url` for `127.0.0.1` and `169.254.169.254`, 422 per field, the OpenAPI document and
`/docs/api` → an org-B key gets 404 for org A's monitor (GET and PATCH) and a list without it → 429 with
`Retry-After` after the Business limit, org B unaffected → an escalation policy and two endpoints saved from the
UI; `127.0.0.1`, `169.254.169.254` and `[::1]` endpoints refused → the monitor breaks, the worker opens the
incident, the receiver verifies `incident.opened` with the official library → tier 1 paged by email, the run
waiting → **Acknowledge** as the member ends the run within seconds; `incident.acknowledged` delivered →
the failing receiver is retried with the same `webhook-id`, `npm run jobs` and the delivery log show the 500s →
**Resend** after recovery and **Replay failed** (yesterday's messages) deliver → past tier 1's deadline tier 2 is
never paged → `acknowledged_at` in the API → the incident's workflow runs on the monitor page → **Mark
resolved** delivers `incident.resolved`, signed; the timeline shows the fan-out, the page and the acknowledgement
→ a revoked key gets 401, last-used is recorded → a member gets 403 on the API keys page.

---

## Module 6 — Product & Growth

Modules 1–5 built what customers never see. Module 6 is what they see first and every day: a **marketing site**
separate from an **app shell** with onboarding and a settings split (6.1), **product analytics** that say whether
new orgs get value (6.2), and **feature flags** that change the product per organization without a deploy (6.3).
One number ties the three together: **activation**, "the org's first check result arrived within 24 hours".

```
 /  /pricing (static, no session read) ─► Sign up ─► createOrganization ─► org_created
                                                           │
 /[org]/monitors: empty state + Getting started ◄──────────┘   org_milestones (stored on the org, with times)
   "Add your first monitor" (dialog, one zod schema in the browser AND on the server)
        └─► createMonitor ── one withOrg() transaction: monitor + milestone + monitor_created event
 worker: checks.schedule ── isEnabled('new-scheduler', org) (OpenFeature, rules cached in memory)
        └─► first check ─► recordCheckResult: first_check milestone + monitor_check_completed  = ACTIVATED (≤ 24 h)
 Slack/webhook, invitation, status page published ─► milestones + events ─► checklist done, it disappears
 analytics_events (Postgres, RLS) ─► analytics.forward job, 1 per org per minute ─► PostHog (optional)
 /internal/analytics: org_created → monitor_created → first check ≤ 24 h, by plan   /internal/flags: rollout, targeting, kill switch
```

### Try it by hand

```bash
npm run db:reset
BEACON_STAFF_EMAILS=demo@beacon.test npm run dev    # terminal 1
FLAGS_REFRESH_SECONDS=3 npm run worker              # terminal 2
```

1. Open <http://localhost:3000/> and **/pricing** signed out: static pages, the plans come from `src/core/plans.ts`.
   DevTools → Application: no cookie. (Set `NEXT_PUBLIC_PLAUSIBLE_DOMAIN` before `npm run build` to load Plausible
   here, and only here.)
2. Sign up. You land on an empty Monitors page with one button, **Add your first monitor**, and a **Getting
   started** checklist at 0/5. Use only the keyboard: Tab (the first stop is "Skip to content"), Enter opens the
   dialog, Escape closes it. Type `not a url` and press Enter: the error appears inline and DevTools → Network
   shows no request. Then the same payload with curl (copy the session cookie):
   ```bash
   curl -s -X POST localhost:3000/api/orgs/<org>/monitors -b 'better-auth.session_token=…' \
        -H 'content-type: application/json' -d '{"name":"x","url":"not a url","intervalSeconds":300}'
   # {"error":"invalid_body","issues":{"url":["Enter a full URL, like https://example.com/health", …]}}
   ```
3. `npm run flags -- override new-scheduler <your-org> on`, then add a real monitor: its first check arrives within
   a minute instead of at its first slot. The checklist ticks "first check": the org is activated.
4. Connect Slack (**Organization → Alert channels**, any `https://hooks.slack.com/services/…` URL with
   `SLACK_PROVIDER=fake`), invite someone (**Members**), publish the **Status page**. The checklist disappears, for
   every member, including one who joins tomorrow.
5. `psql "$DATABASE_URL" -c "select event, properties, org_plan from analytics_events order by occurred_at"`:
   object_action names, ids and enums, no email or URL anywhere.
6. Sign in as `demo@beacon.test` and open **/internal/flags**: put `monitor-latency-chart` at 0% (nobody sees the
   chart on a monitor page), add an override for `demo` (only demo sees it), press the **kill switch** (nobody
   again). **/internal/analytics** shows the funnel by plan.
7. As `member@beacon.test`, `curl -X PATCH localhost:3000/api/orgs/demo/settings -d '{"name":"x"}' …`: 403.

Existing database? Migration 0021 records the milestones your orgs already reached (first monitor, first check,
Slack or a webhook, an invitation or a second member, a public status page), with their original times, so
nobody is walked through "add your first monitor" again. Existing status pages stay as they were; only new orgs
start unpublished.

### Lesson 6.1 — The app shell: marketing site, onboarding, dashboard and settings

**What was built.** Route groups split Beacon into frames with opposite needs: `(marketing)` (`/`, `/pricing`,
static, `dynamic = 'error'` so a session read fails the build), `(auth)` and `(site)` (sign-in, `/settings/account`,
invitations), `[orgSlug]` (the app shell) and `status/` (the customer's page, no Beacon chrome). The shell: a sidebar
(Monitors, Incidents, Status page; Organization: General, Members, Billing, Alert channels, Escalation; Developer: API
keys, Webhooks), an org switcher that swaps the org segment of the URL and keeps the section, the ⌘K palette and the
bell in a top bar. Settings split by owner: `/settings/account` (the user), `/[org]/settings/general` (rename, behind
the new `org.manage` permission, with `PATCH /api/orgs/:org/settings`), members, billing, alert channels, API keys
and webhooks. A new **Incidents** page and a **Status page** section (publish, logo). Onboarding: an empty state with
one action that opens a dialog, and a checklist driven by five milestones stored on the org.

**Read in this order**

1. `src/app/layout.tsx` (the map of frames), `src/app/(marketing)/layout.tsx`, `page.tsx`, `pricing/page.tsx`.
2. `src/app/[orgSlug]/layout.tsx`, then `_shell/nav.ts` (`navFor`, `switchOrgHref`), `org-switcher.tsx`, `sidebar-nav.tsx`.
3. `src/app/[orgSlug]/monitors/new/new-monitor-form.tsx` (`MonitorForm`: one schema, twice) and `add-monitor-dialog.tsx`.
4. `src/core/onboarding.ts`, `src/lib/onboarding.ts`, `drizzle/0021_onboarding_milestones.sql` (the backfill), and the
   `recordMilestoneInTx()` calls in `src/lib/monitors.ts`, `checks.ts`, `invitations.ts`, `webhooks.ts`,
   `notifications/index.ts`, `organizations.ts`.
5. `src/app/[orgSlug]/monitors/onboarding-checklist.tsx`, `page.tsx` (the empty state).
6. `src/app/[orgSlug]/settings/general/`, `src/app/api/orgs/[orgSlug]/settings/route.ts`, `src/core/permissions.ts` (`org.manage`).
7. `tests/onboarding.test.ts`.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 authenticated layout: sidebar (Monitors, Incidents, Status pages, Settings), org switcher changing `/[org]/…`, an empty state whose one button opens a form validated by a shared zod schema | switching org changes the URL and a reload keeps you in that org | `switchOrgHref()` (tested); the org is only ever the URL segment; smoke: `/newco-two/incidents` → `/nora-s-workspace/incidents`, reload, same org |
| | an invalid URL shows an inline error with no request, and curl gets the same message from the server | `MonitorForm` runs `createMonitorInput.safeParse()` on submit and cancels it; the route parses the same schema; test compares the two messages; smoke: 0 POSTs in the browser, then curl → 400 with the identical text |
| | the whole flow works keyboard-only (Tab, Enter, Escape closes the dialog) | a native `<dialog>` with `showModal()`, focus back on the trigger on close; smoke drives it with Tab/Enter/Escape only |
| 🟡 settings split: Account `/settings/account`, Organization `/[org]/settings/general` + `/members`, Billing, Developer | a Member gets 403 from the org-rename endpoint itself | `PATCH /api/orgs/:org/settings` and the server action check `org.manage`; tests (member and viewer 403, admin 200, invalid name 400) and smoke (curl as `member@beacon.test`) |
| 🟡 checklist from milestones stored on the org: first monitor, first alert channel, status page published | the checklist hides itself once done; a second admin who joins later never sees it | state read from `org_milestones`, never from the user; test adds an admin after completion; smoke: checklist and sidebar progress gone after step 5 |
| | milestone timestamps are stored ("time to activation") | `reached_at` (first time only, `ON CONFLICT DO NOTHING`) and `user_id`; the funnel's median time to activation reads them |

The checklist has five steps, not three: the exercise's three plus "first check result" (activation, 6.2) and "invite
a teammate", which the task asked for.

**Design decisions to notice**

- **One Next.js app, split by route groups**, not a monorepo: the course repo stays one project. The seams are where
  next-forge puts its apps: the marketing pages read no session (the build enforces it), the app is `noindex`, the
  status page has its own frame. Moving `(marketing)` to its own app or a CMS is moving a folder.
- **New orgs start with the status page unpublished** (the column's default changed; existing orgs kept theirs).
  Publishing is then a real decision, and a milestone. Test fixtures and the seed publish theirs explicitly.
- **Milestones are rows, written in the transaction of the thing they describe** (the monitor, the check result, the
  webhook endpoint), so they can never disagree with the data. The checklist, the sidebar badge and the funnel all
  read the same rows.
- **Accessibility basics**: a skip link, visible `:focus-visible` rings, labels on every field, `aria-invalid` plus
  focus on the first field in error, `aria-current` in the sidebar, errors with `role="alert"`, and **words next to
  every red/green dot** (the monitor tiles, the checks table, the status page; "never colour alone"). Found on the
  way: the ⌘K palette stole focus on every page load, so Tab skipped "Skip to content"; fixed.
- **No shadcn/ui or Tailwind.** The shell needed a dialog (native `<dialog>` gives the focus trap and Escape), a
  disclosure (`<details>`) and a table; adding a component toolchain for those would have been most of the diff.
  In a new product, start with shadcn/ui as the lesson says.
- Times on the Incidents page are formatted by `Intl` in the viewer's time zone (`LocalTime`).

### Lesson 6.2 — Analytics: product, web and the event pipeline

**What was built.** A tracking plan in code (`src/core/tracking-plan.ts`): 12 events, object_action names,
properties as zod schemas of enums, numbers and booleans only, a "why" and the question each answers. `track()` /
`trackInTx()` accept only those names and exactly those properties (compile time and runtime), refuse anything that
looks like personal data, and write `analytics_events` (org, internal user id, plan at the time) in the business
transaction. Eleven server-side events are wired where the thing happens: `org_created`, `monitor_created`, the first
`monitor_check_completed` per monitor, `alert_channel_connected`, `teammate_invited`, `invitation_accepted`,
`status_page_published`, `incident_opened`, `subscription_upgraded` / `_downgraded` (from the Stripe sync) and
`api_key_created`. One client event, `command_palette_opened`, goes through `POST /api/orgs/:org/analytics` only
after the user said yes to a consent banner. With `ANALYTICS_DRIVER=posthog` the worker forwards events to PostHog in
batches. `/internal/analytics` shows the activation funnel by plan. Plausible loads on the marketing site only, when
`NEXT_PUBLIC_PLAUSIBLE_DOMAIN` is set.

**Read in this order**

1. `src/core/tracking-plan.ts` (the plan, the name rule, `findPii()`).
2. `src/lib/analytics/index.ts` (`validateEvent`, `trackInTx`, `track`), then the calls: `grep -rn "trackInTx\|track(" src/lib`.
3. `src/lib/analytics/drivers.ts` (PostHog: `$groupidentify`, `$groups`, `uuid`), `forward.ts`, the `analytics.forward` queue.
4. `src/core/consent.ts`, `src/app/_components/analytics-consent.tsx`, `src/app/api/orgs/[orgSlug]/analytics/route.ts`.
5. `src/lib/analytics/funnel.ts`, `src/app/internal/analytics/page.tsx`; `src/app/(marketing)/layout.tsx` (Plausible).
6. `drizzle/0022_analytics_events.sql`; `tests/analytics.test.ts`.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 a tracking plan of 8–12 object_action events with properties and a why; cookieless web analytics on the marketing site only | every event maps to a question (activation, retention, upgrade) | `question` and `why` on every entry; tests check names, questions and whys; `/internal/analytics` prints the plan |
| | no property contains an email, name or monitored URL | schemas allow only enums, numbers and booleans (a test walks every schema); `findPii()` on every event; test runs every flow and scans all rows; smoke scanned the new org's events |
| | marketing visits are counted with no cookie set | the Plausible script is in `(marketing)/layout.tsx` only; smoke (against a local stand-in for Plausible): 2 page views, no cookie, no storage, and no script in the app |
| 🟡 PostHog: identify, `group("organization", orgId, { plan })`, `monitor_created` and `subscription_upgraded` server-side after the write/webhook; the activation funnel | the funnel breaks down by organization plan | every event carries its org and `org_plan`; PostHog batches start with `$groupidentify` (type organization, plan) and every event has `$groups`; `activationFunnel()` groups by plan (test with four orgs, smoke) |
| | blocking PostHog in the browser does not stop `monitor_created` | there is no PostHog in the browser: `monitor_created` is inserted in the monitor's transaction (a failed create records nothing, tested) and forwarded by the worker (an outage retries, tested) |
| | a typed `track` rejects event names outside the plan at compile time | `EventName` and `EventProperties<E>` derive from the plan; `tests/analytics.test.ts` has three `@ts-expect-error` calls that `npm run typecheck` verifies |

**Design decisions to notice**

- **Postgres first, PostHog second.** Events are business facts, so they commit with the business write (the 5.1
  lesson again: no dual write). Forwarding is a job per org per minute (deterministic id, one running per org), sends
  the row id as PostHog's `uuid` so a retry does not double-count, and a PostHog outage only delays it.
- **`identify` and `group`, server-side.** The distinct id is Beacon's user id from the start, so there is no
  anonymous browser id to merge: `identify` has nothing to do. The org is sent as a group with its plan on every batch
  and on every event, which is the lesson's "send the group on every event, not only at identify time". If you add
  the posthog-js SDK for UI events, call `identify(userId)` at login and `group('organization', orgId, { plan })` in
  the org layout, after consent.
- **Consent where it is needed.** Server-side events are about the org's use of the product, with ids only (privacy
  policy and DPA, lesson 8.1). The browser's optional UI event waits for a yes; the server checks the same cookie, so
  a client that ignores it gains nothing. "No thanks" is one click, and `/settings/account` changes it later.
- **Only the first check per monitor** becomes an event: every check would be millions of rows. Uptime history for
  customers is the 🔴 ClickHouse exercise.
- **Deleting a user keeps their events and forgets them** (`user_id` is set null), so GDPR erasure does not rewrite
  history.
- The funnel reads across orgs as the database owner; it is staff-only and exempt from the `withOrg()` lint for that
  reason. At scale it runs on a replica or in the warehouse.

### Lesson 6.3 — Feature flags and experiments

**What was built.** `feature_flags` (`key`, `enabled`, `rollout_percent`) and `feature_flag_overrides` (`key`,
`organization_id`, `enabled`). What each flag *is* lives in code (`src/core/flags.ts`: type, owner, expiry, safe
default, cleanup ticket); how it is set lives in the tables. Evaluation: master switch → per-org override → stable
hash of `key:orgId` into 0–99 against the rollout. The app calls OpenFeature
(`client.getBooleanValue(key, safeDefault, { targetingKey: orgId })`) through `isEnabled()`, with Beacon's own
provider doing local evaluation from a cached rule set. Three flags, each wired to real code: `new-scheduler`
(release: the scheduler checks a never-checked monitor at once), `disable-sms-sending` (ops kill switch, checked
before every SMS) and `monitor-latency-chart` (permission/beta: a response-time chart on the monitor page).
`/internal/flags` (staff: `BEACON_STAFF_EMAILS`) and `npm run flags` change them.

**Read in this order**

1. `src/core/flags.ts`: `FLAGS`, `rolloutBucket()`, `evaluateFlag()`.
2. `src/lib/flags/provider.ts` (the OpenFeature provider: refresh, last known rules, safe defaults), `index.ts`, `store.ts`.
3. The three call sites: `src/lib/scheduler.ts`, `src/lib/notifications/deliver.ts` `sendSmsDelivery()`,
   `src/app/[orgSlug]/monitors/[id]/page.tsx`.
4. `src/app/internal/flags/`, `scripts/flags.ts`, `src/lib/staff.ts`.
5. `drizzle/0023_feature_flags.sql`; `tests/flags.test.ts`.

**Exercises covered**

| Exercise | Done-when | Where |
|---|---|---|
| 🟢 `feature_flags` + `feature_flag_overrides`; `isEnabled(key, orgId)`: overrides, then hash `key:orgId` into 0–99 | the same org always gets the same answer (1,000 calls) | test; plus 10,000 random orgs at 30% land between 28% and 32%, and every bucket is used |
| | raising 10% → 30% keeps every org already on | test (2,000 orgs); a different flag picks a different slice (test) |
| | an override for your internal org turns it on regardless of percentage | test at 0%, and an override can also keep one org out of 100%; smoke: override for `demo` shows the chart there only |
| 🟡 OpenFeature with a self-hosted provider; `new-scheduler` keyed by org with local evaluation in the worker; `disable-sms-sending` flipped from a dashboard | stopping the flag service does not crash workers: last known rules or the safe default | provider tests: the loader fails after a load → same answers, reason `STALE`; never loaded → every flag's safe default; no targeting key → default, never a throw |
| | flipping the kill switch stops SMS within the refresh interval, no deploy | test: switched on → the SMS delivery is `skipped` with the reason, the fake provider sent nothing, the email went out; switched off → SMS again; the refresh interval is tested with an injected clock |
| | every flag has an owner and an expiry, and a ticket to remove `new-scheduler` | `FLAGS` entries (tested: owner, description, cleanup; expiry for every non-ops flag); each temporary flag's cleanup names a `TODO(flag:<key>)` that must exist at its call site (tested) |

Not Unleash or Flagsmith: the course repo runs with Postgres alone (no Docker in CI for a flag server), so the
"self-hosted service" is Beacon's own tables, behind the same OpenFeature API. Swapping in
`@openfeature/flagsmith-provider` or `@openfeature/flagd-provider` is one `setProvider()` call in
`src/lib/flags/index.ts`; the call sites and the tests of the pure rules stay.

**Design decisions to notice**

- **The master switch beats overrides.** The exercise checks overrides first; Beacon puts `enabled = false` above
  them so one click turns a misbehaving feature off everywhere, including for the beta customers (tested). A key with
  no row uses its safe default, so shipping code before creating the rule is safe.
- **Flags are not entitlements** (lesson 3.2). `src/core/flags.ts` and `src/lib/flags/` import nothing about plans,
  and the plans and entitlements modules import nothing about flags (a test reads the imports). A test forces every
  flag on for a Free org: still 5 monitors, 5-minute checks, no API, and a 30-second monitor is still refused.
- **Evaluate on the server, send results.** Pages and the worker call `isEnabled()`; the browser never sees a rule
  or a targeting list. The org is the rollout unit (teammates never see different products).
- **Local evaluation with a refresh.** Each process holds the rule set (two small queries) and reloads it when older
  than `FLAGS_REFRESH_SECONDS` (15 s). The staff action reloads its own process at once. The scheduler asks for every
  org every minute without a query per org.
- **`new-scheduler` is small but real**: a new monitor's first check within a minute instead of at its first phase
  slot (up to 15 minutes for a 900 s interval). It shortens time to activation, which is exactly what a release flag
  is for: turn it on for your own org, then 10%, watch, then everyone, then delete the flag. Found on the way: Drizzle
  prints an interpolated column without its table inside a `select`, which silently broke the correlated
  `not exists` subquery; the SQL is written out in full there now.
- **Staff access is a stopgap**: `BEACON_STAFF_EMAILS` and a verified email, 404 for everyone else (pages and
  actions). Module 7 builds the admin panel with a staff table, roles and the audit log (`TODO(7.3)` on every flag
  change).

**Flag cleanup.** `npm run flags` and `/internal/flags` mark a temporary flag past its expiry, and a rule left in the
database for a flag deleted from the code ("delete it, never reuse the name"). Removing `new-scheduler`, once at
100% for two weeks: delete its `FLAGS` entry, the `if` in `scheduleChecks()` (keep the new branch), then its row
from `/internal/flags`. Search `TODO(flag:` for every removal ticket.

### Not done in Module 6 (🔴 exercises and neighbours)

Custom domains for status pages (6.1 🔴): a `custom_domains` table, a TXT/CNAME verification job re-checked daily,
routing by `Host` in `middleware.ts` before any page logic, and Caddy's `on_demand_tls` whose `ask` endpoint answers
200 only for verified hostnames (never enable on-demand TLS without it), or Cloudflare for SaaS custom hostnames.
Customer-facing uptime analytics in ClickHouse with batched inserts and TTL by plan (6.2 🔴). The
`onboarding-checklist-v2` experiment with a sample-size plan, exposure events and an SRM check (6.3 🔴). Also: the
posthog-js SDK in the app (the only client event goes through Beacon's endpoint), a rate limit on the client-event
endpoint, flag change history and approvals (7.3), and a danger zone (transfer ownership, delete the org, 1.2 🔴).

### Verification for this branch

`npm test` (563 tests and 2 more with `DATABASE_URL`, 565 in CI; 65 new in `tests/analytics.test.ts`,
`tests/onboarding.test.ts` and `tests/flags.test.ts`, plus a cross-tenant case for each new route), `npm run typecheck`
(including the `@ts-expect-error` calls to `track()`), `npm run openapi:check`, `npm run db:migrate` on a fresh
database (twice: idempotent) and on a database migrated and seeded on `module-5-solution` (the demo org got its four
milestones back-filled with their original times, its status page stayed public, the column default became false),
`npm run build` (`/` and `/pricing` prerendered as static), and a smoke test against `next start` plus
`npm run worker` (50 checks), with a local stand-in for Plausible and a local monitor target: `/` and `/pricing`
without a session, no `Set-Cookie`, the three plans from the config → Plausible counted two page views with no
cookie or storage and is absent from the app → `/demo/monitors` signed out redirects to `/login`, `/account` →
`/settings/account` (308) → a new user signs up: empty state with one action, checklist 0/5, `org_created` →
keyboard only: first Tab is "Skip to content", Tab to the button, Enter opens the dialog with focus inside, Escape
closes it and focus returns → `not a url` + Enter: inline error, 0 POSTs; curl with the same payload: 400, identical
message → the monitor is added with Enter → `npm run flags -- override new-scheduler <org> on`: the worker checked
the new monitor 24 s after it was created → first check within 24 h: activated → the verification link from the
console email driver, Slack connected, a teammate invited, the status page published (404 → 200) → all five
milestones stored, checklist and sidebar badge gone → six product events with the plan's names, no email, name, URL
or secret in any property, internal user ids and the org's plan on each → the consent banner: ⌘K before "Allow"
sends nothing, after it `command_palette_opened` is recorded → every settings section reached with Tab from the
sidebar, Enter opens it (`aria-current`), each renders for the owner → rename with the keyboard, the slug stays → a
second org and the switcher: `/newco-two/incidents` → `/<first>/incidents`, reload stays, Escape closes the menu → a
Member: read-only General page and 403 from `PATCH /api/orgs/demo/settings` → the new user gets 404 on demo's pages,
rename and analytics endpoints → `/internal/flags` 404 for them; as staff: the three flags with owners and cleanup
tickets → `monitor-latency-chart` at 0%: no chart for demo or the new org → an override for demo: the chart only
there → the kill switch: gone for demo too → `/internal/analytics`: the free row counts the new orgs and one
activation; recent events show names and ids only. The SMS kill switch and the provider's failure modes are covered
by the tests, not the smoke test.
