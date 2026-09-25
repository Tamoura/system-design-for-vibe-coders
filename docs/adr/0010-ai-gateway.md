# ADR 0010: AI through a thin in-house gateway; drafts that a person publishes

- **Status:** Accepted
- **Decided in:** `module-8-solution` (lesson 8.2)
- **Recorded:** Module 9, from docs/SOLUTIONS.md "Lesson 8.2"

## Context

The first AI feature is an incident summary: when an incident resolves, draft a status-page update. It brings back
every old problem in a new place: untrusted input (incident notes can carry prompt injections), a cost per tenant,
tenant isolation (a cache or a context must never mix orgs), provider outages, and the question of who is
responsible for text on a customer's public page.

## Decision

- **A thin gateway in Beacon** (`src/lib/ai/gateway.ts`): an ordered provider chain (primary model, then a fallback
  model), timeouts, a per-org rate limit sized by plan, a per-org response cache keyed by the input's hash,
  validation of the structured output with Zod plus domain checks (`summaryProblems()` in
  `src/core/incident-summary.ts`), and metering of every call in `llm_usage` (Beacon's cost) and of successful
  calls as `ai_tokens` usage events (the customer's bill).
- **Claude through the official Anthropic SDK** (`src/lib/ai/anthropic.ts`); model ids from configuration
  (`AI_MODEL`, `AI_FALLBACK_MODEL`); a fake provider when there is no key (`src/lib/ai/providers.ts`).
- **A job, not a stream:** `ai.summarize` runs when the incident resolves; the result is a **draft**. Only a person
  with `page.publish` puts it on the status page (`src/lib/ai/incident-summary.ts`). Off by default per org, and a
  Business entitlement.
- **An eval in CI** (`scripts/ai-eval.ts`, `evals/incident-summary.fixtures.ts`), including injections and a
  control run that must fail.

## Alternatives rejected

1. **The Vercel AI SDK as the abstraction.** The gateway already is the provider abstraction; one SDK is less to learn,
   and the lesson's point is the gateway, not the library.
2. **A separate gateway service (LiteLLM, Portkey) from day one.** One more service in the path for one feature and one
   provider. `ANTHROPIC_BASE_URL` can point the SDK at such a proxy without code changes.

## Consequences

- Blast radius of a prompt injection: the model has no tools and no network, its answer is checked against the facts
  (an ongoing incident is never "resolved"; no links or contact details), and a person publishes. The worst case is a
  misleading draft that someone must still choose to publish.
- The model sees minimised context: the monitor's host, not its URL; counts of alerts, never recipients.
- Incident data goes to a subprocessor, which is why the feature is opt-in and listed on `/trust` (`src/core/trust.ts`).
- **How to predict the next choice:** a second AI feature calls `generateStructured()` with its own Zod schema, its own
  feature name for metering, and its own eval file; it does not import the SDK.

## Revisit when

- A **second AI feature** ships, or a **second provider** is needed in production → LiteLLM or Portkey as the proxy.
- Any org's AI cost passes **$50 a month**, or AI cost passes **5% of revenue** → per-org monthly token budgets checked
  before each call (lesson 8.2 🔴).
- Users must **watch text appear** (an interactive assistant, not a background draft) → streaming through the gateway.
