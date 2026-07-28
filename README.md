# System Design for Vibe Coders

**You can ship code faster than any generation of programmers before you. This course teaches you the things your AI won't warn you about until production is down.**

## What this is

A written course on practical system design for **AI-first builders** — people shipping real products with Claude Code, Cursor, and friends, **whether or not they have ever written code**. If you build by directing an agent, this course teaches the two skills that replace reading code: knowing what to *ask for*, and knowing how to *check it*.

Honest label: this is **production engineering for AI-assisted builders**. It is not a FAANG-interview prep course — no CAP theorem drills, no whiteboard estimation, no designing Twitter on a napkin. If you're preparing for interviews, this is the wrong course; if you're keeping a real product alive, it's the right one. Every lesson in this course is anchored to a **real production incident** from a real product: a real multi-client production platform (web, iOS, Android, and TV, serving a global audience) — built and operated largely *by* AI agents under human direction. The incidents span the whole surface a real product grows: caching and CDNs, data and backups, deploys, auth and OAuth, email and newsletters, feature flags, mobile releases, security and abuse, observability. The scars are real; the fixes shipped.

## How the course works

**You do not need to know how to code.** In this course you are the architect and
the safety inspector; your AI agent is the builder. Every hands-on step is written
as instructions *you give the agent* and evidence *you demand back* — never as code
you must write yourself. Readers who do code get optional **🔧 Under the Hood**
boxes with the manual commands and source.

Every lesson has the same four pillars:

1. **🔥 The War Story** — a real incident: the symptoms as they appeared, the wrong theories, the actual root cause, the fix that shipped.
2. **📐 The Principle** — the system-design concept the incident teaches, in plain language and diagrams, every term defined before it's used (backed by the [Glossary](./GLOSSARY.md)).
3. **🎛️ Direct Your Agent** — you apply the principle to **Relay**, a deliberately generic product (accounts, creator content, media uploads, feeds, email, a mobile client) built across the course from prototype to zero-downtime production — by telling your agent *what* to build: the exact prompts to give, the context that makes it build the right thing, and the guardrail to install so the rule outlives the chat. Apply every step to your own app instead if you have one.
4. **✅ Verify It** — the pillar that makes vibe coding safe: an evidence checklist proving the step actually worked, written so checking it requires **zero code reading** — things you can see, click, or make the agent demonstrate from the layer users touch.

## Who it's for

- You build (or want to build) real products by directing an AI agent — with or without a programming background.
- You've been bitten (or are about to be) by something that "worked" until real users arrived.
- You want to stop trusting and start verifying — without needing to read the code.

## Who it's not for

- Interview preppers — go do the Grokking course.
- People who want theory without operating anything.

**Completely new to this world?** Start at **Part 0 — Foundations**: five
plain-language lessons with no prerequisites at all (what a server is, what happens
when you open a website, what code/repos/deploys are, how to work with your agent,
and putting your first page live — with proof).

## Curriculum

See [OUTLINE.md](./OUTLINE.md) for the full module-by-module curriculum, and [war-stories/incident-bank.md](./war-stories/incident-bank.md) for the raw incident material the lessons are built from.

| # | Module | The wall you hit |
|---|--------|------------------|
| F | Part 0: Foundations | You don't code — and you don't need to. No prerequisites. |
| 0 | The Vibe Coder's Gap | "It works" and "it's a system" are different claims |
| 1 | Anatomy of a Real App | You can't reason about what you can't draw |
| 2 | Data, Storage & Backups | The database is not the only thing that can lose data |
| 3 | Caching: the Sharpest Knife in the Drawer | Every cache is a bug you haven't met yet |
| 4 | Deploys Without Downtime | Shipping is a system, not a command |
| 5 | Real Users, Real Abuse | Rate limits, auth, and the first attacker |
| 6 | One Backend, Many Clients | Web, mobile, TV — and the update problem |
| 7 | Observability | You can't fix what you can't see |
| 8 | Safety Nets for AI-Generated Code | Tests, guardrails, and git hygiene at agent speed |
| 9 | Directing an AI Team | Specs, context engineering, and review-to-guardrail |
| 10 | Scaling Beyond One Server | The classic scaling canon, through the lens of a product that grew |
| 11 | Reaching the World | DNS & TLS, i18n & RTL, SEO & sitemaps, cost engineering |
| 12 | Capstone: You Get Paged | Symptoms only. Diagnose it. |

The curriculum is a **complete** practical system-design set: incident-backed where
we have scars, concept-complete everywhere else (lessons without a war story are
marked as concept lessons and gain one as incidents accumulate).

## Languages

The course is **bilingual**: every document ships in English and Arabic (RTL).
English files are the source of truth during drafting; Arabic mirrors live beside
them (`README.ar.md`, `OUTLINE.ar.md`, `lesson-N.ar.md`).

## Reading it

The whole course builds into several self-contained editions. Read online at
**[tamoura.github.io/system-design-for-vibe-coders](https://tamoura.github.io/system-design-for-vibe-coders/)**,
or take it with you:

| Edition | File | What it's for |
|---|---|---|
| Bilingual page | [`index.html`](./index.html) | Everything, with a language toggle |
| English page | [`index.en.html`](./index.en.html) | Single language, half the weight |
| Arabic page | [`index.ar.html`](./index.ar.html) | Single language, RTL throughout |
| PDF | `course-en.pdf` · `course-ar.pdf` | Print and offline reading (~350pp) |
| EPUB | `course-en.epub` · `course-ar.epub` | E-readers and Kindle |

Every edition carries all 68 lessons with the diagrams pre-rendered — no server, no network,
no CDN. The HTML pages also have a clickable course map, the glossary appendix, and dark mode.
PDF and EPUB are published with each release rather than committed; build them locally with
`npm run dist`.

```
npm install     # once — marked, mermaid, puppeteer, archiver (build-time only)
npm run build   # regenerate the HTML pages from the markdown
npm run dist    # the above, plus PDF and EPUB per language into dist/
npm run check   # fail if the committed HTML is out of date (used by CI)
```

**The markdown under `modules/` is the source of truth.** Everything above is generated
output — never edit it by hand; edit the lesson and rebuild. The build fails loudly if a
module's English and Arabic lesson counts diverge, if any Mermaid diagram fails to render,
or if an EPUB document is not well-formed XHTML.

## Status

Early draft. Outline complete; lessons being written module by module.
