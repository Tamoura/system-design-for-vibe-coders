# System Design for Vibe Coders

**You can ship code faster than any generation of programmers before you. This course teaches you the things your AI won't warn you about until production is down.**

## What this is

A written course on practical system design for **AI-first builders** — people shipping real products with Claude Code, Cursor, and friends, who never formally studied distributed systems, and who hit the wall the day their prototype meets real users.

It is not a FAANG-interview prep course. There are no whiteboard exercises about designing Twitter. Every lesson in this course is anchored to a **real production incident** from a real product: a real multi-client production platform (web, iOS, Android, and TV, serving a global audience) — built and operated largely *by* AI agents under human direction. The incidents span the whole surface a real product grows: caching and CDNs, data and backups, deploys, auth and OAuth, email and newsletters, feature flags, mobile releases, security and abuse, observability. The scars are real; the fixes shipped.

## How the course works

Every lesson has the same four-part shape:

1. **🔥 The War Story** — a real incident: the symptoms as they appeared, the wrong theories, the actual root cause, the fix that shipped.
2. **📐 The Principle** — the system-design concept the incident teaches, explained from first principles for someone who has never read a distributed-systems textbook.
3. **🔨 The Build-Along** — you apply the principle to **Relay**, a deliberately generic product you build across the whole course — accounts, creator content, media uploads, feeds, email, a mobile client — from local prototype to zero-downtime production. Every step is written so you can apply it to *your own* app instead; Relay is just the reference. Each module leaves your app one production-grade capability stronger.
4. **🤖 Prompting Your Agent** — how to get your AI coding agent to do this *right*: the context to give it, the guardrail to install, and the review question that catches the failure mode before it ships. Because in vibe coding, *you* are the architect and the reviewer — the agent is the typist.

## Who it's for

- You've shipped something real with an AI coding agent and people actually use it.
- You can read code but you've never had to reason about caches, CDNs, deploys, or backups.
- You've been bitten (or are about to be) by something that "worked locally."

## Who it's not for

- Interview preppers — go do the Grokking course.
- People who want theory without operating anything.

## Curriculum

See [OUTLINE.md](./OUTLINE.md) for the full module-by-module curriculum, and [war-stories/incident-bank.md](./war-stories/incident-bank.md) for the raw incident material the lessons are built from.

| # | Module | The wall you hit |
|---|--------|------------------|
| 0 | The Vibe Coder's Gap | "It works" and "it's a system" are different claims |
| 1 | Anatomy of a Real App | You can't reason about what you can't draw |
| 2 | Data, Storage & Backups | The database is not the only thing that can lose data |
| 3 | Caching — the Sharpest Knife | Every cache is a bug you haven't met yet |
| 4 | Deploys Without Downtime | Shipping is a system, not a command |
| 5 | Real Users, Real Abuse | Rate limits, auth, and the first attacker |
| 6 | One Backend, Many Clients | Web, mobile, TV — and the update problem |
| 7 | Observability | You can't fix what you can't see |
| 8 | Safety Nets for AI-Generated Code | Tests, guardrails, and git hygiene at agent speed |
| 9 | Directing an AI Team | Specs, context engineering, and review-to-guardrail |
| 10 | Scaling Beyond One Server | Load balancing, queues, DB scaling, realtime, performance |
| 11 | Reaching the World | DNS & TLS, i18n & RTL, SEO & sitemaps, cost engineering |
| 12 | Capstone: Incident Response | You get paged. Diagnose it. |

The curriculum is a **complete** practical system-design set: incident-backed where
we have scars, concept-complete everywhere else (lessons without a war story are
marked as concept lessons and gain one as incidents accumulate).

## Languages

The course is **bilingual**: every document ships in English and Arabic (RTL).
English files are the source of truth during drafting; Arabic mirrors live beside
them (`README.ar.md`, `OUTLINE.ar.md`, `lesson-N.ar.md`).

## Status

Early draft. Outline complete; lessons being written module by module.
