# ADR 0003: One shared schema, `organization_id` everywhere, row-level security per transaction

- **Status:** Accepted
- **Decided in:** `module-1-solution` (lessons 1.2, 1.3) and `module-2-solution` (lesson 2.4)
- **Recorded:** Module 9, from docs/SOLUTIONS.md "Lesson 1.2", "Lesson 1.3" and "Lesson 2.4"

## Context

Every customer is an organization, with members in roles (owner, admin, member, viewer). A cross-tenant leak is the
one bug a B2B SaaS does not survive. Beacon has thousands of small tenants, not a few huge ones, and one team to
run migrations and backups.

## Decision

- **Pool model:** one database, one schema; `organization_id` on every tenant table, including tables that could
  reach it through a join (`check_results`, `incidents`).
- **Two layers.** Every function in `src/lib` takes the org and writes `WHERE organization_id = …`; and runs inside
  `withOrg(orgId)` (`src/db/tenant.ts`), which switches to the `beacon_app` role and sets `app.current_org` for that
  transaction only, so Postgres policies (`drizzle/0007_row_level_security.sql`) filter and check every row.
- **Authorization in code:** one permission map and `can()` (`src/core/permissions.ts`), `requirePermission()` before
  any work (`src/lib/access.ts`), 404 (not 403) for outsiders, one ABAC rule (members edit only their own monitors).
- **The org never comes from the body:** from the URL plus a membership, from an API key, or from a job payload.

## Alternatives rejected

1. **Schema or database per tenant.** Stronger isolation, but every migration runs N times, connection pools
   multiply, and cross-org staff queries become N queries. It suits a few large tenants, not thousands of small ones.
2. **Application filtering only (no RLS).** One missing `WHERE` is a leak, and nothing notices. RLS makes Postgres
   add the filter anyway and refuses a row written with another org's id.

## Consequences

- Proven by tests that fail on the next mistake: every tenant table has a policy, no tenant query outside `withOrg()`
  (`tests/tenant-scoping.test.ts`), every route called as another org (`tests/cross-tenant-routes.test.ts`).
- `memberships`, `invitations` and `api_keys` are not under RLS: they are how a request finds its org.
- Index-using search under RLS needs `SECURITY DEFINER` functions that filter by `current_org_id()` themselves
  (`drizzle/0009_search.sql`).
- The app connects as the table owner and switches role per transaction; code that skips `withOrg()` sees every row
  (the lint test is the guard). Hardening: connect as a login role that is only a member of `beacon_app`.
- Tenants share one database's CPU and locks. Fairness is per job group (5 checks per org at once) and per-org API
  and AI rate limits, not physical isolation.
- **How to predict the next choice:** a new table gets `organization_id`, a policy in its migration, and a
  cross-tenant test case, or a line in `NOT_UNDER_RLS` with a reason.

## Revisit when

- A signed contract **requires data residency** (EU-only storage) or a dedicated database → add cells: one Beacon
  deployment per region, orgs pinned to a cell (lesson 2.4 🔴).
- One org holds **more than 20% of `check_results` rows** or of worker time → move it to its own cell.
- The first **SOC 2 audit**, or any finding of a query outside `withOrg()` → do the non-owner login role hardening.
- Customers ask to **share one monitor across orgs** or for per-resource roles → OpenFGA or SpiceDB (lesson 1.3 🔴).
