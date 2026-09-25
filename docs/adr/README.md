# Architecture decision records

Lesson 9.1 (🟡). One page per consequential choice: the context, the decision, two alternatives we rejected, what
follows from it, and the concrete signal that should make us revisit it. The format is Michael Nygard's, with a
**Revisit when** section instead of a status that silently goes stale.

These were written in Module 9 from the reasoning recorded while each module was built (`docs/SOLUTIONS.md`), not
invented afterwards. Where the code changed during the review, the ADR says so. The picture they add up to is
[`docs/architecture.md`](../architecture.md); the seams they leave open are in
[`docs/readiness-review.md`](../readiness-review.md).

## Index

| ADR | Decision | Lessons | The trigger most likely to fire first |
|---|---|---|---|
| [0001](0001-postgres-is-the-only-stateful-dependency.md) | Postgres is the only stateful dependency | 2.1, 4.3, 5.1, 5.2, 6.3 | more than 500 notifying commits per second |
| [0002](0002-authentication-better-auth.md) | Better Auth, sessions in Postgres; SSO/SCIM deferred | 1.1, 1.4, 8.1 | a contract that requires SAML SSO or SCIM |
| [0003](0003-tenancy-shared-schema-and-rls.md) | One schema, `organization_id` everywhere, RLS per transaction | 1.2, 1.3, 2.4 | a contract that requires data residency |
| [0004](0004-job-queue-pg-boss.md) | pg-boss for jobs and the scheduler; a small workflow engine | 5.1, 5.4 | a fourth consumer of incident events |
| [0005](0005-billing-stripe-and-entitlements.md) | Stripe owns money; plan snapshot and entitlements in code | 3.1, 3.2, 3.3 | the first annual invoice or custom contract |
| [0006](0006-email-and-notifications.md) | One `sendEmail()` and one `notify()`, providers behind interfaces | 4.1, 4.2 | a status page with 10,000 subscribers |
| [0007](0007-public-api-and-api-keys.md) | A separate `/api/v1` with org-owned keys | 5.2 | a customer asking for service-account keys |
| [0008](0008-outbound-webhooks-built-on-the-svix-model.md) | Outbound webhooks on the Svix model, behind an SSRF guard | 5.3, 8.1 | 100,000 deliveries a day |
| [0009](0009-observability-and-audit.md) | pino + OpenTelemetry for operators; a hash-chained audit log for customers | 7.1, 7.2, 7.3 | a SIEM streaming request |
| [0010](0010-ai-gateway.md) | AI through a thin in-house gateway; drafts a person publishes | 8.2 | a second AI feature |

## Predicting the eleventh

The lesson's test for a set of ADRs: can a teammate predict the next one? These five rules run through all ten.

1. **Postgres first.** New state goes in the one database, behind one named function (0001).
2. **Tenant id first.** A new table gets `organization_id`, a policy and a cross-tenant test (0003).
3. **Library before service; service where the other side owns the truth** (money, mail delivery, phone networks,
   the model), and always behind an interface with a fake, so tests run offline (0002, 0005, 0006, 0010).
4. **Side effects are rows and jobs in the transaction of the change**, retried by the queue, logged in a row (0004).
5. **Every revisit trigger is a number or a signed contract**, never "if needed".

Worked example: **SSO and SCIM.** Rules 3 and 1 say a library or a self-hosted service rather than a SaaS
(Better Auth's `sso` plugin, or Ory Polis next to Beacon), connections in a Postgres table with `organization_id`
under RLS, and a SCIM deprovisioning handler that calls the *same* offboarding service function a person's removal
calls, audited in its transaction (rules 2 and 4). Revisit when more than 20 orgs have a connection or a customer
needs an IdP the library does not support → WorkOS.

## Template

Copy this into `NNNN-short-title.md`. Keep it to one page: if it needs more, it is two decisions.

```markdown
# ADR NNNN: <the decision, as a sentence>

- **Status:** Proposed | Accepted | Superseded by NNNN
- **Decided in:** <branch or pull request> (lesson x.y)
- **Recorded:** <date or module>

## Context

What forces this decision: the requirement, the constraint, the team's size and stage. No solution yet.

## Decision

What we do, concretely, with the files where it lives.

## Alternatives rejected

1. **<Alternative>.** Why not, in this context.
2. **<Alternative>.** Why not, in this context.

## Consequences

What becomes easy, what becomes hard, what we accept knowingly. Link the tests that hold the decision in place.
One line starting "How to predict the next choice:".

## Revisit when

- <a measurable signal: a number, a customer contract, an incident> → <what we would do instead>
```

## Keeping them true

`tests/architecture-docs.test.ts` fails when a file path cited in these records, in `docs/architecture.md` or in
`docs/readiness-review.md` no longer exists, so a move or a rename has to update the decision that names it.
