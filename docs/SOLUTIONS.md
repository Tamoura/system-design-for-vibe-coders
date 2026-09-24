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
