# Curriculum — System Design for Vibe Coders

Build-along spine: across the course you build **Muraja'a**, an audio-library app
(browse creators, stream audio, playlists, accounts) from a local prototype to a
zero-downtime, multi-client production system. Every module upgrades it with the
capability the module teaches — in the same order a real product forces you to
learn them.

Legend per lesson: 🔥 war story · 📐 principle · 🔨 build-along · 🤖 agent technique

---

## Module 0 — The Vibe Coder's Gap

Why fast code generation makes system design *more* important, not less.

- **0.1 "It works" is not a property of a system.**
  🔥 A polished feature that fell over the moment two things were true at once (deploy + cache).
  📐 Systems = components + the failure modes of the seams between them. AI writes components; seams are your job.
  🔨 Install the course toolchain; meet Muraja'a's product brief.
  🤖 Why "make it production ready" is the worst prompt in your vocabulary.

- **0.2 The map of everything that can hurt you.**
  📐 The eight seams: data, cache, deploy, auth, abuse, clients, observability, cost. Course roadmap as a threat model.
  🔨 Write Muraja'a's one-page "what could kill this" doc.

## Module 1 — Anatomy of a Real App

- **1.1 Draw the boxes before the agent writes the code.**
  📐 Client / API / DB / cache / object storage / CDN — what each is *for*, and what each one lies about.
  🔥 Tour of the real reference architecture: Next.js + Express + MongoDB + Redis + Cloudflare CDN + R2 object storage, serving audio worldwide.
  🔨 Scaffold Muraja'a (Next.js + API + DB) and draw its C4-style diagram — by hand, before generating code.
  🤖 Giving your agent an architecture document (CLAUDE.md as the load-bearing artifact).

- **1.2 The request's journey.**
  📐 Trace one GET from browser → CDN → proxy → app → cache → DB and back. Every hop is a place to be wrong.
  🔨 Add request tracing headers to Muraja'a; follow one request end-to-end in the logs.

## Module 2 — Data, Storage & Backups

- **2.1 The database is the easy part.**
  📐 Choosing boring storage; schema decisions you can't cheaply undo.
  🔥 A schema keyed on the wrong identity: recitations keyed by narration style, discovered only when a reciter had two styles — one got silently swallowed.
  🔨 Design Muraja'a's schema; deliberately find the identity mistake before it finds you.

- **2.2 Object storage and the two-owner trap.**
  🔥 Deleted files that resurrected themselves: storage was migrated from GCS to R2 with a replication bridge (Sippy) still on — every R2 delete was quietly restored from the old bucket.
  📐 Migrations aren't done until the old system can't act anymore. Dual-write/dual-read phases need explicit end dates.
  🔨 Add audio upload to Muraja'a via object storage; write the migration-phases table.

- **2.3 Backups: what, not just whether.**
  🔥 The nightly backup that grew 244 MB → 871 MB overnight — it was faithfully archiving webpack build caches from *both* blue-green build directories, while the thing that actually needed backing up (two Mongo databases + configs) was a fraction of the size.
  📐 Back up state, not artifacts. Code lives in git; builds are reproducible; data is not.
  🔨 Write Muraja'a's backup script + a restore drill. A backup you've never restored is a hope, not a backup.
  🤖 Asking the agent "what did this backup actually capture?" — verifying agent-written ops scripts.

## Module 3 — Caching: the Sharpest Knife in the Drawer

- **3.1 Why caching is where correctness goes to die.**
  📐 The only two hard things; cache keys, TTLs, invalidation. Layered caches multiply, not add, your confusion.
  🔨 Add Redis response caching to Muraja'a's hot endpoints; measure the speedup honestly.

- **3.2 The cache poisoning incident.** *(flagship lesson)*
  🔥 Users worldwide saw pages render as raw `0:{...}` JSON. Root cause: the CDN ignored the `Vary` header and cached a React Server Component *flight* response as if it were the HTML page. Framework updates silently stripped the headers the first fix depended on — the durable fix was a content-type guard at the proxy layer.
  📐 Shared caches + content negotiation = poisoning risk. Defend at the layer you control, not the layer you hope behaves.
  🔨 Put a CDN in front of Muraja'a; reproduce a poisoning in miniature; install the guard.

- **3.3 Invalidation in real life.**
  🔥 A cache key that was a bare slug when the code computed a prefixed one — mutations "invalidated" a key nobody read.
  📐 Invalidate through one function or you'll invalidate through zero. Cache-key discipline.
  🔨 Centralize Muraja'a's cache keys; write the test that proves mutation clears what reads populate.
  🤖 A drift-guard test template: making the agent keep two lists in sync forever.

## Module 4 — Deploys Without Downtime

- **4.1 Shipping is a system.**
  📐 What actually happens during a deploy; why "restart the server" was fine until it wasn't.
  🔨 Give Muraja'a a real deploy script to a VPS (or container); break it on purpose.

- **4.2 Blue-green and the shared-directory 502s.**
  🔥 Zero-downtime blue-green deploys that still 502'd: both colors built into the same `.next` directory, so bringing up green corrupted the assets blue was actively serving. Fix: each color owns its own build directory, permanently.
  📐 "Two instances" isn't isolation unless *everything* is duplicated — builds, temp dirs, ports, state.
  🔨 Implement blue-green for Muraja'a with per-color build dirs; deploy under load and watch zero requests drop.

- **4.3 The proxy lies: stale workers and trusting your own verification.**
  🔥 After a color flip, an nginx worker kept routing to the dead color — flapping 502s that no app log explained. And a separate trap: the CDN caches HTML for 5 minutes, so "I checked the site, deploy's live" verified the *old* deploy. Rule that emerged: compare asset hashes against origin before declaring victory.
  📐 Every layer between you and the user has its own lifecycle and its own cache. Deploy verification must pierce all of them.
  🔨 Write Muraja'a's post-deploy verification script (origin check, asset-hash check, health endpoint).
  🤖 Turning a post-incident rule into an agent-enforced checklist so it survives you forgetting.

- **4.4 Rollback, staging, and release gates.**
  🔥 Content uploads that went live the moment an admin uploaded them — until a release gate made everything land hidden by default.
  📐 Staging environments, feature flags vs deploys, and default-hidden as a publishing model.
  🔨 Add a staging target + rollback command to Muraja'a.

## Module 5 — Real Users, Real Abuse

- **5.1 Your first attacker is a script.**
  🔥 A registration/email-bomb abuser ("bob") and the layered response: CAPTCHA, rate limits, disposable-email rejection.
  📐 Abuse economics: raise the attacker's cost above the payoff. Defense in depth for the three free endpoints (signup, email, search).
  🔨 Add Turnstile + signup limits to Muraja'a.

- **5.2 Rate limiting that survives a CDN.**
  🔥 Legit users got 429'd: behind Cloudflare, every request appeared to come from a handful of CDN IPs, so the whole world shared one rate-limit bucket. Fix: key on the CDN-provided client IP header, store counters in Redis (in-memory counters reset on every deploy and don't share across instances).
  📐 Identity at the edge: what "the client's IP" even means behind proxies. Distributed counters need shared storage.
  🔨 Add correct, Redis-backed rate limiting to Muraja'a behind its CDN.

- **5.3 Auth that you can operate.**
  📐 JWT in httpOnly cookies, rotating refresh tokens (reuse detection burns the chain), 2FA, why localStorage tokens are a smell.
  🔥 The URL that betrayed you: user-facing links built from a CORS-origin env var that was `localhost` in prod — password-reset emails pointing nowhere. Env vars have *audiences*.
  🔨 Add sessions + refresh rotation to Muraja'a; write the env-var audience table.
  🤖 Security review prompts that actually catch things; making the agent enumerate env-var consumers.

## Module 6 — One Backend, Many Clients

- **6.1 The client fleet problem.**
  📐 Web deploys in minutes; mobile releases live for months. API versioning, tolerant readers, force-update gates as the last resort.
  🔥 A force-update gate wired to store versions: enable the store release *first*, then flip the minimum version — order matters or you brick users.
  🔨 Add a versioned API + a mobile-style "min supported version" gate to Muraja'a.

- **6.2 Over-the-air updates and the revert trap.**
  🔥 An OTA update published from a feature branch — the next OTA from main silently reverted it. And OTA env handling that stripped runtime config unless the environment was named explicitly.
  📐 Update channels are state machines. Every publish path needs a single source of truth (main).
  🔨 Simulate channel discipline with Muraja'a's staging/prod flag config.

- **6.3 Feature flags done once, not five times.**
  🔥 The same flag checked at compile time in one surface and runtime in another — nav showed a feature the route 404'd.
  📐 One runtime flag map, resolved in one place, consumed everywhere. Flags are config, not code.
  🔨 Add a runtime flag system to Muraja'a gating one route + its nav + its promo stripe together.

- **6.4 Deep links and the drift problem.**
  🔥 A hand-maintained list of "routes the app knows" rotted as routes were added — deep links fell back to web for pages the app had. Fix included a drift-guard test that fails the build when the list and the router disagree.
  📐 Any two sources of truth will diverge. Either derive one from the other or install a tripwire.
  🔨 Write a drift-guard test for Muraja'a's sitemap vs its route table.
  🤖 Drift-guards as the general antidote to agent-maintained parallel lists.

## Module 7 — Observability: You Can't Fix What You Can't See

- **7.1 The dashboard that lies and the metric that doesn't.**
  🔥 "Returning users" counted logins; the honest metric was distinct listening days. Same data, different question.
  📐 Choose metrics that measure the user's reality, not the system's convenience.
  🔨 Add basic analytics events + one honest retention metric to Muraja'a.

- **7.2 Errors, logs, and the noise floor.**
  🔥 A crash dashboard dominated by three noisy non-actionable errors, hiding real ones. A staging process discovered still running — two months stale — quietly serving old code.
  📐 Alert on symptoms users feel; triage by actionability; audit what's actually running.
  🔨 Wire Sentry (or equivalent) into Muraja'a; write the "what's running where" runbook page.

- **7.3 Search is telemetry.**
  🔥 Zero-result searches revealed both a normalization bug and what users actually wanted.
  📐 Instrument the failure paths of discovery features — they're free user research.
  🔨 Log Muraja'a's zero-result searches; fix the top normalization miss.

## Module 8 — Safety Nets for AI-Generated Code

- **8.1 The 600-file near-miss.**
  🔥 One branch created from the wrong base + one `git add .` deleted 600+ files. The response wasn't "be careful" — it was hooks: staged-file count limits, deletion-size tripwires, base-branch verification.
  📐 At agent speed, process rules must be mechanical. Anything enforced by memory will fail.
  🔨 Install pre-commit and pre-push guards in Muraja'a's repo.
  🤖 Git hygiene rules that belong in every CLAUDE.md.

- **8.2 Tests as the spec the agent can't ignore.**
  📐 TDD with an agent: red-green-refactor as a prompting pattern, not a ritual. Which tests earn their keep (drift-guards, contract tests, E2E smoke) vs vanity coverage.
  🔥 A ~3,200-test suite kept green across hundreds of agent PRs — and the cold-compile E2E false-failures that had to be engineered away before anyone trusted it.
  🔨 Build Muraja'a's three-layer test pyramid; make CI block merges.

- **8.3 CI preflight and the boy-who-cried-wolf check.**
  🔥 A preflight check that always failed (wrong package manager assumption) trained everyone to ignore it — the most dangerous state a check can be in.
  📐 A check that can be ignored will be. Fix it or delete it; never let it lie.
  🔨 Add a preflight script to Muraja'a; prove every check can actually fail *and* actually pass.

## Module 9 — Directing an AI Team

- **9.1 You are the architect now.**
  📐 The division of labor: agents write components; you own seams, invariants, and taste. Specs before code (spec → plan → tasks); acceptance criteria as the contract.
  🔨 Run one Muraja'a feature through a full spec-driven cycle.

- **9.2 Context engineering.**
  📐 Why agents degrade with bloated context; progressive disclosure; what belongs in CLAUDE.md vs a spec vs a memory file. Writing docs *for an agent audience*.
  🔨 Write Muraja'a's CLAUDE.md properly; measure the difference on a real task.

- **9.3 Every repeated review comment is a missing guardrail.**
  📐 The review-to-guardrail pipeline: flag it twice → automate it (lint rule, test template, hook) → stop reviewing for it. The review surface should shrink over time.
  🔨 Convert your three most-repeated review nits into automated checks.

- **9.4 Verification before completion.**
  🔥 The deploy "verified" through a CDN cache; the push notifications "shipped" that were never wired to the sender; the flag that was "on" in a config nobody read.
  📐 "Done" requires evidence from the layer the user touches. Screenshots of localhost are not evidence.
  🔨 Write Muraja'a's definition-of-done checklist; make the agent produce evidence, not assurances.

## Module 10 — Capstone: You Get Paged

Six incident simulations. Each gives you symptoms only (user reports, status codes,
graphs); you diagnose, propose the fix, then compare against what actually happened
in production. Drawn from the incident bank:

1. Pages render as raw JSON for some users, some of the time.
2. Flapping 502s that stop when you restart something you "shouldn't have to."
3. Nightly backup size triples with no data growth.
4. Legit users hit 429s the day after a traffic spike.
5. A deleted file keeps coming back.
6. Your mobile fix disappears a week after you shipped it.

Passing bar: correct layer identified, plausible root cause, a fix that survives
the follow-up question "and how do you know it worked?"

---

## Format notes

- Each lesson ≈ 1,500–2,500 words + diagrams (Mermaid) + a build-along commit.
- Modules ship as directories: `modules/NN-slug/lesson-N.md`.
- Incident bank (`war-stories/incident-bank.md`) is the raw source of truth;
  lessons cite it. New incidents land there first.
