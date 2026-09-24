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
