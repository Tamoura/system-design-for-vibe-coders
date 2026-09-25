# ADR 0002: Authentication with Better Auth, sessions in Postgres

- **Status:** Accepted (SSO and SCIM deferred)
- **Decided in:** `module-1-solution` (lesson 1.1); sign-in throttling added in `module-8-solution` (lesson 8.1)
- **Recorded:** Module 9, from docs/SOLUTIONS.md "Lesson 1.1" and "Lesson 1.4"

## Context

Beacon needs email and password sign-up, verification, password reset, "Sign in with GitHub", and sign-out that
really signs out. The lesson's first rule is that authentication is a library's job: hand-written crypto and token
flows are where breaches come from. The user table must join with Beacon's own `memberships` and `organizations`
in SQL, and the course repo has to run offline with Postgres alone ([ADR 0001](0001-postgres-is-the-only-stateful-dependency.md)).

## Decision

[Better Auth](https://www.better-auth.com) with its Drizzle adapter, configured in one file (`src/lib/auth.ts`):
server-side sessions in the `sessions` table behind an `HttpOnly`, `SameSite=Lax` cookie (`Secure` on https), no
cookie cache (every request reads the row), argon2id hashes (`src/lib/password.ts`), reset tokens hashed with a one-hour
expiry, `revokeSessionsOnPasswordReset`, GitHub OAuth with PKCE and no implicit account linking. Server actions call
`auth.api.*`, so there is no client auth SDK. Lesson 8.1 added per-account and per-IP token buckets in a `before`
hook (`src/lib/sign-in-throttle.ts`). Beacon owns the configuration and the edge cases; the library owns the crypto.

## Alternatives rejected

1. **Stateless JWT sessions.** "Log out" and "a password reset signs you out everywhere" would need a deny-list, which
   is a session table again. With server-side sessions each is one `DELETE`, and account deletion cascades to them.
2. **A managed identity service (Clerk, Auth0).** The users would live outside Beacon's database, so every membership
   query would cross a network; the course repo could not run offline; and pricing per active user grows with the
   customers' teams, not with revenue.

## Consequences

- Removing access is immediate: deleting a `sessions` row (sign-out, support's "sign out everywhere", account
  deletion) ends the next request, and open real-time streams re-check within 30 s (`src/lib/realtime-stream.ts`).
- **Known gap, accepted:** Better Auth stores the session token itself, not a hash of it, and has no option to hash
  it. A leaked `sessions` table is usable until the sessions expire (30 days, sliding).
- **SSO and SCIM are not built** (lesson 1.4 needs an IdP and a SAML service running next to Beacon). The Business
  plan's `sso` entitlement exists in `src/core/plans.ts` with no feature behind it. Without SCIM, an employee who
  leaves a customer keeps their Beacon login until someone acts (see `docs/readiness-review.md`).
- Staff sign in through the same library and the same form; staff MFA and a separate hostname are documented, not built.

## Revisit when

- A customer contract **requires SAML SSO or SCIM**, or the first Business deal stalls on it → Better Auth's `sso`
  plugin, or Ory Polis self-hosted, with an `sso_connections` table per org (lesson 1.4). This is the most likely
  trigger of all ten ADRs.
- A SOC 2 auditor or a penetration test **flags the raw session tokens** and Better Auth still cannot hash them.
- More than **one engineer-week per quarter** goes into auth maintenance or upgrades → price a managed provider.
