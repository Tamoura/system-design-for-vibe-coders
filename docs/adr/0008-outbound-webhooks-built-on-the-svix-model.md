# ADR 0008: Outbound webhooks, built on the Svix data model, behind an SSRF guard

- **Status:** Accepted
- **Decided in:** `module-5-solution` (lesson 5.3); secrets encrypted at rest in `module-8-solution` (lesson 8.1)
- **Recorded:** Module 9, from docs/SOLUTIONS.md "Lesson 5.3" and "Lesson 8.1"

## Context

Customers want `incident.opened`, `incident.acknowledged` and `incident.resolved` pushed to their own systems.
Their receivers are slow, down, or misconfigured; and a customer-supplied URL is an attacker-supplied URL: without a
guard, `http://169.254.169.254/` turns Beacon into a proxy into its own cloud account (the same risk as monitor URLs).

## Decision

- **The Svix data model, in Postgres:** an immutable event → one message per subscribed endpoint (its id is the
  `webhook-id`, the same on every retry) → attempts, the log (`src/db/schema.ts`, `src/lib/webhooks.ts`). All three
  are written in the incident's transaction, with one `webhook.deliver` job per message.
- **Standard Webhooks signatures** (`src/core/webhooks.ts`), verified in tests with the official `standardwebhooks`
  package. Secrets are shown once and stored envelope-encrypted (`src/lib/secrets/index.ts`).
- **Delivery:** `safeFetch()` resolves DNS, rejects private, loopback, link-local and CGNAT addresses (v4 and v6),
  pins the checked address for the connection, follows no redirects, 10 s timeout, reads at most 64 KB
  (`src/core/safe-fetch.ts`, `src/core/ssrf.ts`). 18 attempts over about a day and a half, grouped by endpoint so a
  slow receiver delays only itself; after 5 days of failures the endpoint is disabled and admins are emailed.
- **Operable by the customer:** a delivery log per endpoint, **Resend**, and **Replay failed since…**.

## Alternatives rejected

1. **Svix (managed).** The right buy for a funded team (a customer portal, replay and scale come with it). Beacon
   builds the same model to show its mechanics, and so the course repo runs without a vendor account.
2. **A plain POST from the check path.** No retries, no log, a slow receiver would delay checks, and no SSRF guard
   in the one place that most needs it.

## Consequences

- Machines get every change: webhook events are recorded even while a monitor is flapping; only people are spared.
- A webhook secret must be readable to sign, so it cannot be hashed like an API key; its compromise lets someone
  forge Beacon's signature to that one receiver. Rotation with two signatures at once is not built.
- The same guard protects monitor checks, so Beacon's egress policy lives in one file. There is no egress proxy
  (Smokescreen) in front of it yet; `OUTBOUND_ALLOWLIST` is a development escape hatch refused in production.
- **How to predict the next choice:** another outbound integration (PagerDuty, Teams) posts through `safeFetch()`,
  keeps an attempts log, and is retried by the queue.

## Revisit when

- Deliveries pass **100,000 a day**, or any org has **more than 50 endpoints** → Svix or Hookdeck.
- Customers ask for a **self-serve portal**, an event catalog, or per-endpoint transformations → Svix.
- A penetration test or SOC 2 control asks for **network-level egress control** → an egress proxy in front of the
  guard, not instead of it.
- A customer needs **secret rotation without downtime** → two active secrets per endpoint, both signing.
