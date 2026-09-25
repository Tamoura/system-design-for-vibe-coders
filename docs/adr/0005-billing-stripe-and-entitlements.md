# ADR 0005: Stripe owns money; a plan snapshot and entitlements in code decide access

- **Status:** Accepted
- **Decided in:** `module-3-solution` (lessons 3.1–3.3); staff trials and comps in `module-7-solution` (lesson 7.1)
- **Recorded:** Module 9, from docs/SOLUTIONS.md "Module 3" and "Lesson 7.1"

## Context

Beacon sells three plans (Free, Pro, Business) with limits (monitors, check interval, SMS credits, audit retention,
API, AI) and SMS overage. Card data must never touch Beacon. Every limit has to hold on every path: the form, the
dashboard JSON, the public API and the check scheduler.

## Decision

- **Stripe** for everything about money: hosted Checkout and Customer Portal, subscriptions, Billing Meters for SMS
  and AI tokens. Every call goes through a `BillingProvider` interface with the `stripe` SDK and an in-memory fake
  (`src/lib/billing/provider.ts`).
- **The webhook is a trigger, not a message:** verify the signature on the raw body, dedupe by event id
  (`stripe_events`), then re-fetch the customer's subscriptions from Stripe and upsert our copy
  (`src/lib/billing/webhook.ts`, `src/lib/billing/sync.ts`). The success page grants nothing.
- **Entitlements in code:** `PLANS` is the one module that knows plan names (`src/core/plans.ts`); a plan snapshot on
  the organization is written only by the sync (and staff comps, through the same `recomputePlanInTx()`), and read
  by everything else (`src/lib/entitlements.ts`). A limit is a `402 limit_exceeded` with the plan that unlocks it.
- **Usage** is recorded when the cost is certain, with the provider message id as idempotency key, and reported to
  the meter by a job (`src/lib/usage.ts`).

## Alternatives rejected

1. **Ask Stripe (or trust the webhook payload) at request time.** A network call on every write, and out-of-order
   events would write stale state. The snapshot lets the API, the pages and the scheduler enforce the same limits
   without calling Stripe; the re-fetch makes event order irrelevant.
2. **A merchant of record (Paddle, Lemon Squeezy) or a metering service (Lago, OpenMeter).** Worth it for sales tax
   in many countries or many usage dimensions; Beacon has two meters and the course follows the lesson's seed-stage
   default, Stripe Checkout plus the Portal.

## Consequences

- Downgrades are idempotent and humane: the newest monitors are frozen, never deleted; exactly one email.
- A test greps `src/` for a plan compared to a string; flags never grant entitlements (`tests/flags.test.ts`).
- Count-then-insert can overshoot a limit by one under concurrency (accepted for cheap resources).
- **Beacon prices per monitor, not per seat**, so removing a member changes no invoice (`docs/readiness-review.md`).
- Not done: payment-failed and trial-ending emails, dunning, nightly reconciliation, deleting the Stripe customer
  when an org is purged.

## Revisit when

- The first customer asks for **annual invoicing, a PO or a custom contract** → Stripe Invoicing and quotes, and
  per-org entitlement overrides in a table (lesson 3.2 🔴).
- Beacon must collect **sales tax or VAT in more than 3 jurisdictions** → Stripe Tax, or a merchant of record.
- A **third usage meter** is added, or usage events pass **1 million a month** → a metering service.
- `syncCustomerFromStripe()` fails **more than once a week** in production → move it onto the queue (TODO(5.1)).
