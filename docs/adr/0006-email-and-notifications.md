# ADR 0006: One `sendEmail()` and one `notify()`, built; providers behind interfaces

- **Status:** Accepted
- **Decided in:** `module-4-solution` (lessons 4.1, 4.2); moved onto the queue in `module-5-solution`
- **Recorded:** Module 9, from docs/SOLUTIONS.md "Lesson 4.1" and "Lesson 4.2"

## Context

An uptime monitor that does not reach the on-call person is worthless. Beacon sends transactional email
(verification, reset, invitations), incident alerts on four channels (in-app, email, SMS, Slack), and status-page
updates to subscribers who are not users. People must control what reaches them, some categories must not be
switchable off, SMS costs money and is a plan entitlement, and every attempt must be visible to the customer.

## Decision

- **Email:** React Email templates with a plain-text part (`src/emails/index.tsx`). `sendEmail()` only writes an
  `email_outbox` row and an `email.send` job with an idempotency key; the worker sends through an `EmailTransport`:
  Resend's HTTP API in production, SMTP (nodemailer) to Mailpit locally, `console` and `memory` drivers
  (`src/lib/email/index.ts`, `src/lib/email/transport.ts`). A signed bounce/complaint webhook fills
  `email_suppressions`, checked before every send. Status-page mail uses a second sending stream.
- **Notifications:** one pipeline, `notify()` / `notifyInTx()` (`src/lib/notifications/pipeline.ts`): recipients by
  permission, dedupe per event and person, preferences resolved as required → org policy → person → default, one
  `notification_deliveries` row per channel which is both the job and the delivery log. Twilio and Slack are HTTP
  calls behind `SmsProvider` / `SlackSender` with fakes (`src/lib/notifications/providers.ts`).

## Alternatives rejected

1. **Calling the provider SDK where the email is needed.** A provider outage would fail the request, retries would
   be ad hoc, and switching providers would touch every call site. A test greps `src/` and `scripts/` for provider
   imports outside `src/lib/email/`.
2. **Notification infrastructure as a service (Knock, Courier, Novu).** It would own preferences and the delivery log,
   which Beacon needs inside the incident's transaction and next to entitlements (SMS only on paid plans, metered
   through Beacon's usage pipeline). Beacon's needs fit in one pipeline file.

## Consequences

- Nothing a request does waits for a provider; an outage delays mail, then it goes out (tested).
- Anti-flapping and the SMS throttle (5 per person per hour, then an email) live in the domain, next to the incident.
- Recipients are resolved when the event is delivered, from current memberships: a removed person gets nothing new.
- **How to predict the next choice:** a new channel (push, Teams, PagerDuty) is one more driver behind an interface
  and one more delivery `channel`, not a new pipeline.
- Not done: per-tenant sending domains, batched fan-out to very large subscriber lists, digests, quiet hours.

## Revisit when

- One status page has **more than 10,000 confirmed subscribers** → batched, throttled fan-out on its own stream (4.1 🔴).
- A customer asks to **send from their own domain** → per-tenant domains at the provider.
- Hard bounces exceed **2%** or complaints **0.1%** of a month's mail → review lists and the provider's reputation tools.
- Customers ask for **digests, quiet hours and on-call schedules** together → price Knock or Novu against building them.
