# ADR 0007: A separate `/api/v1` with org-owned API keys, built in-house

- **Status:** Accepted (amended in Module 9: keys die with their creator's account)
- **Decided in:** `module-5-solution` (lesson 5.2)
- **Recorded:** Module 9, from docs/SOLUTIONS.md "Lesson 5.2" and the readiness review

## Context

Customers want to manage monitors from Terraform and scripts, and read incidents into their own tools. The
dashboard's JSON routes (`/api/orgs/:org/…`) are shaped for the UI and authenticated by a session cookie; a public
contract has to be stable, documented and safe to call from a CI job with a secret.

## Decision

- **A separate surface:** `/api/v1/monitors` and `/api/v1/incidents`, snake_case, prefixed ids (`mon_…`), cursor
  pagination, RFC 9457 problem details, `Idempotency-Key` on POST, OpenAPI generated from the same Zod schemas
  (`src/core/api-schemas.ts`, `src/core/openapi.ts`; CI fails if `docs/openapi.json` drifts). Business plan only.
- **Keys:** `bk_live_…`, SHA-256 at rest, shown once, revocable with no cache (the next request is a 401). The key
  decides the org; scopes map to permissions and cannot exceed the creator's role at creation
  (`src/core/api-keys.ts`, `src/lib/api-keys.ts`). The audit actor is the key, by prefix.
- **The order of checks** in one wrapper, `publicApi()` (`src/lib/public-api.ts`): per-IP bucket → key → plan →
  scope → per-org bucket sized by plan → handler.
- **Module 9:** deleting an account revokes the keys that person created, in the same transaction, audited
  (`src/lib/privacy/user-data.ts`, tested in `tests/privacy.test.ts`).

## Alternatives rejected

1. **Open the dashboard routes to API keys.** Their shape changes with the UI, and a cookie-authenticated route and
   a key-authenticated one need different CSRF, error and rate-limit rules. One contract per audience.
2. **A managed key and rate-limit service (Unkey, Zuplo) or Redis buckets.** Another service in the request path for
   two resources; token buckets in Postgres share state across app instances already
   ([ADR 0001](0001-postgres-is-the-only-stateful-dependency.md)).

## Consequences

- `api_keys` is not under RLS (a key is looked up before any org is known); the lint test names the exception.
- Additive changes only: new fields may appear, so generated response schemas allow unknown properties.
- **Open seam:** a key keeps its scopes when its creator is demoted (for example admin → viewer): the role bound is
  checked only at creation. Recorded as finding A4 in `docs/readiness-review.md`.
- **How to predict the next choice:** a new public resource is a Zod schema in `src/core/api-schemas.ts`, a
  `publicApi(scope, …)` handler, a scope, and a cross-tenant case in `tests/public-api.test.ts`.

## Revisit when

- Sustained API traffic passes **200 requests per second**, or bucket updates show lock waits → Redis limiter.
- The first **breaking change** is unavoidable → date-based versions (`Beacon-Version`) with transformers (5.2 🔴).
- A partner wants to act for **many customers' orgs** → OAuth apps instead of copied keys.
- A customer asks for **keys that outlive people** (service accounts) → an explicit service-account owner, instead of
  a person, and the demotion rule in finding A4.
