# Curriculum — System Design for Vibe Coders

Build-along spine: across the course you build **Relay**, a deliberately generic
product — accounts, creator profiles, media uploads, feeds, email, a mobile
client — from a local prototype to a zero-downtime, multi-client production
system. Every module upgrades it with the capability the module teaches, in the
same order a real product forces you to learn them. Every build-along step is
phrased so you can apply it to your own app instead; Relay is just the reference.

Legend per lesson: 🔥 war story · 📐 principle · 🎛️ direct your agent · ✅ verify it
(🔧 = optional "under the hood" material for readers who code; 🤖 lines describe
agent-direction techniques and fold into 🎛️ in the written lessons)

Audience policy: **non-coders first.** Every 🎛️ step is an instruction to give an
agent, never code to write; every ✅ step is evidence checkable without reading
code. Coders get optional 🔧 boxes. Terms are defined before use (see GLOSSARY.md).

Coverage policy: the curriculum is a **complete** practical system-design set —
incident-backed where we have scars, concept-complete everywhere else. Lessons
without a 🔥 line are concept lessons; as real incidents accumulate they get one.

Language policy: the course ships **bilingual** — every lesson is authored in
English (`lesson-N.md`) and Arabic (`lesson-N.ar.md`, RTL). Outline mirrors:
`OUTLINE.md` / `OUTLINE.ar.md`.

---

## Part 0 — Foundations (no prerequisites)

Five plain-language lessons for readers who have never coded. Diagram-first,
zero jargon without definition, each ends with something you can *see* working.

- **F.1 What happens when you open a website.**
  📐 The whole journey in plain words: your browser asks a directory (DNS) where the site lives, reaches a computer that never sleeps (a server), which sends back the page. Every later lesson zooms into one part of this picture.
  🎛️ Ask your agent to draw this journey for any website you use daily — then for the app you dream of building.
  ✅ You can explain to a friend, in one minute with a napkin sketch, what happens between typing an address and seeing a page.

- **F.2 What a server actually is (and what code is).**
  📐 A server is a computer that runs your product's instructions all day; code is those instructions written precisely enough for a machine; a database is the notebook it never loses. Your laptop vs "the cloud" — same thing, different room.
  🎛️ Have your agent show you a running program on your own machine, stop it, start it — feel the difference between "the code exists" and "the code is running."
  ✅ You can answer: where does my app live when my laptop is closed? What's the difference between the app being *written* and being *on*?

- **F.3 Versions, repos, and deploys — how software moves.**
  📐 A repo is the product's full history of saved drafts (git); a deploy is copying a chosen draft onto the always-on computer; a rollback is choosing yesterday's draft. Why "it's on my machine" and "it's live" are different places.
  🎛️ Direct your agent to create a repo for a tiny page, make two saved versions, and show you the history — then restore the older one.
  ✅ You can point at the history and say which version is live, and get back to the previous one without panic.

- **F.4 Meet your agent: how to direct a builder you can't watch.**
  📐 What an AI coding agent can and can't know; why context files (CLAUDE.md) are its memory; the three sentences every good instruction has (goal, constraint, evidence demanded); why "make it production ready" fails and "add a login page; don't touch the database; show me it working at the real URL" succeeds.
  🎛️ Write your first CLAUDE.md with the agent: what the product is, what it must never do, how you want evidence delivered.
  ✅ A fresh agent session, given only your CLAUDE.md, correctly answers three questions about your product without you repeating yourself.

- **F.5 Your first live page — with proof.**
  📐 Putting the pieces together: repo → deploy → a real URL anyone on earth can open. The habit that defines this course: never accept "done" — accept *evidence*.
  🎛️ Direct your agent end-to-end: create a one-page site, put it live on a real URL (a managed host is fine), then change one word and ship the change.
  ✅ Open the URL on your *phone* (not the agent's screenshot), see the change, and check the old version still exists in history. That's your first verified deploy — and the standard for everything that follows.

## Module 0 — The Vibe Coder's Gap

Why fast code generation makes system design *more* important, not less.

- **0.1 "It works" is not a property of a system.**
  🔥 A polished feature that fell over the moment two things were true at once (deploy + cache).
  📐 Systems = components + the failure modes of the seams between them. AI writes components; seams are your job.
  🔨 Install the course toolchain; meet Relay's product brief.
  🤖 Why "make it production ready" is the worst prompt in your vocabulary.

- **0.2 The map of everything that can hurt you.**
  📐 The eight seams: data, cache, deploy, auth, abuse, clients, observability, cost. Course roadmap as a threat model.
  🔨 Write Relay's one-page "what could kill this" doc.

## Module 1 — Anatomy of a Real App

- **1.1 Draw the boxes before the agent writes the code.**
  📐 Client / API / DB / cache / object storage / CDN — what each is *for*, and what each one lies about.
  🔥 Tour of the real reference architecture: Next.js + Express + MongoDB + Redis + Cloudflare CDN + R2 object storage, serving a global audience.
  🔨 Scaffold Relay (Next.js + API + DB) and draw its C4-style diagram — by hand, before generating code.
  🤖 Giving your agent an architecture document (CLAUDE.md as the load-bearing artifact).

- **1.2 The request's journey.**
  📐 Trace one GET from browser → CDN → proxy → app → cache → DB and back. Every hop is a place to be wrong.
  🔨 Add request tracing headers to Relay; follow one request end-to-end in the logs.

## Module 2 — Data, Storage & Backups

- **2.1 The database is the easy part.**
  📐 Choosing boring storage; schema decisions you can't cheaply undo.
  🔥 A schema keyed on the wrong identity: catalog entries keyed by edition alone, discovered only when a creator published two variants of the same edition — one got silently swallowed.
  🔨 Design Relay's schema; deliberately find the identity mistake before it finds you.

- **2.2 Object storage and the two-owner trap.**
  🔥 Deleted files that resurrected themselves: storage was migrated from GCS to R2 with a replication bridge (Sippy) still on — every R2 delete was quietly restored from the old bucket.
  📐 Migrations aren't done until the old system can't act anymore. Dual-write/dual-read phases need explicit end dates.
  🔨 Add media upload to Relay via object storage; write the migration-phases table.

- **2.3 Backups: what, not just whether.**
  🔥 The nightly backup that grew 244 MB → 871 MB overnight — it was faithfully archiving webpack build caches from *both* blue-green build directories, while the thing that actually needed backing up (two Mongo databases + configs) was a fraction of the size.
  📐 Back up state, not artifacts. Code lives in git; builds are reproducible; data is not.
  🔨 Write Relay's backup script + a restore drill. A backup you've never restored is a hope, not a backup.
  🤖 Asking the agent "what did this backup actually capture?" — verifying agent-written ops scripts.

- **2.4 Retention, deletion, and the data you promised to erase.**
  🔥 Analytics TTLs deliberately removed → millions of rows/year growing forever on the same disk as the primary DB. And account deletion that removed one document while ~13 linked collections kept personal data the privacy policy promised to erase.
  📐 Retention is a reliability control, not just privacy. The golden rule for destructive retention migrations: backfill → verify → *then* expire. "Delete" is defined over the whole data graph.
  🔨 Add TTLs + a tested deletion cascade to Relay; write the retention table (what, how long, why).

- **2.5 Indexes, queries, and the working set.**
  🔥 One admin dashboard load ran eight unbounded whole-collection scans over the largest table — evicting the hot catalog data every DB actually serves from memory.
  📐 How indexes actually work (and what they cost); compound indexes; reading a query plan; N+1 queries; why an OLTP database has a "working set" and what evicts it. SQL vs document vs key-value — choosing boring, and when each fits.
  🔨 Add indexes to Relay's two hottest queries; read the query plans before and after; find and fix one N+1.
  🤖 Agents write queries that pass tests on 50 rows and die on 5 million — the standing prompt: "what does this query's plan look like at 10M rows, and which index serves it?"

## Module 3 — Caching: the Sharpest Knife in the Drawer

- **3.1 Why caching is where correctness goes to die.**
  📐 The only two hard things; cache keys, TTLs, invalidation. Layered caches multiply, not add, your confusion.
  🔨 Add Redis response caching to Relay's hot endpoints; measure the speedup honestly.

- **3.2 The cache poisoning incident.** *(flagship lesson)*
  🔥 Users worldwide saw pages render as raw `0:{...}` JSON. Root cause: the CDN ignored the `Vary` header and cached a React Server Component *flight* response as if it were the HTML page. Framework updates silently stripped the headers the first fix depended on — the durable fix was a content-type guard at the proxy layer.
  📐 Shared caches + content negotiation = poisoning risk. Defend at the layer you control, not the layer you hope behaves.
  🔨 Put a CDN in front of Relay; reproduce a poisoning in miniature; install the guard.

- **3.3 Invalidation in real life.**
  🔥 A cache key that was a bare slug when the code computed a prefixed one — mutations "invalidated" a key nobody read.
  📐 Invalidate through one function or you'll invalidate through zero. Cache-key discipline.
  🔨 Centralize Relay's cache keys; write the test that proves mutation clears what reads populate.
  🤖 A drift-guard test template: making the agent keep two lists in sync forever.

- **3.4 When the cache takes you down.**
  🔥 Three ways one Redis nearly (or actually) caused an outage: no memory cap (`noeviction` default → on OOM every cache write fails and 100% of traffic lands on the DB); no single-flight lock (cold cache after deploy = thundering herd of identical expensive queries); and a `FLUSHDB` cache-clear that also wiped live-presence state sharing the same DB — the live-presence counter dropped to zero instantly.
  📐 "Cache down" must degrade to *slow*, never *down*. Cap memory, coalesce misses, and never colocate disposable and non-disposable state — or only ever evict by key prefix.
  🔨 Cap Relay's Redis, add a single-flight lock, and split presence state from response cache.

## Module 4 — Deploys Without Downtime

- **4.1 Shipping is a system.**
  📐 What actually happens during a deploy; why "restart the server" was fine until it wasn't.
  🔨 Give Relay a real deploy script to a VPS (or container); break it on purpose.

- **4.2 Blue-green and the shared-directory 502s.**
  🔥 Zero-downtime blue-green deploys that still 502'd: both colors built into the same `.next` directory, so bringing up green corrupted the assets blue was actively serving. Fix: each color owns its own build directory, permanently.
  📐 "Two instances" isn't isolation unless *everything* is duplicated — builds, temp dirs, ports, state.
  🔨 Implement blue-green for Relay with per-color build dirs; deploy under load and watch zero requests drop.

- **4.3 The proxy lies: stale workers and trusting your own verification.**
  🔥 After a color flip, an nginx worker kept routing to the dead color — flapping 502s that no app log explained. And a separate trap: the CDN caches HTML for 5 minutes, so "I checked the site, deploy's live" verified the *old* deploy. Rule that emerged: compare asset hashes against origin before declaring victory.
  📐 Every layer between you and the user has its own lifecycle and its own cache. Deploy verification must pierce all of them.
  🔨 Write Relay's post-deploy verification script (origin check, asset-hash check, health endpoint).
  🤖 Turning a post-incident rule into an agent-enforced checklist so it survives you forgetting.

- **4.4 Rollback, staging, and release gates.**
  🔥 Content uploads that went live the moment an admin uploaded them — until a release gate made everything land hidden by default.
  📐 Staging environments, feature flags vs deploys, and default-hidden as a publishing model.
  🔨 Add a staging target + rollback command to Relay.

- **4.5 Verify the artifact, not the source.**
  🔥 TV apps submitted to two app stores with `localhost:3105` baked in as the API — a stray gitignored `.env.local` was inlined at build time, invisible in every diff; one store rejected it, the other nearly shipped it. Plus the deploy that served stale JS twice because the webpack build cache reused old modules.
  📐 Build-time config inlining + local overrides = silent corruption. Release checks must inspect the compiled output (grep the bundle), not the source tree.
  🔨 Add a postbuild verifier to Relay that fails loudly if the artifact contains localhost or lacks the production origin.
  🤖 Agents can't see gitignored files in diffs either — the verifier is the only reviewer that catches this class.

## Module 5 — Real Users, Real Abuse

- **5.1 Your first attacker is a script.**
  🔥 A registration/email-bomb abuser ("bob") and the layered response: CAPTCHA, rate limits, disposable-email rejection.
  📐 Abuse economics: raise the attacker's cost above the payoff. Defense in depth for the three free endpoints (signup, email, search).
  🔨 Add Turnstile + signup limits to Relay.

- **5.2 Rate limiting that survives a CDN.**
  🔥 Legit users got 429'd: behind Cloudflare, every request appeared to come from a handful of CDN IPs, so the whole world shared one rate-limit bucket. Fix: key on the CDN-provided client IP header, store counters in Redis (in-memory counters reset on every deploy and don't share across instances).
  📐 Identity at the edge: what "the client's IP" even means behind proxies. Distributed counters need shared storage.
  🔨 Add correct, Redis-backed rate limiting to Relay behind its CDN.

- **5.3 Auth that you can operate.**
  📐 JWT in httpOnly cookies, rotating refresh tokens (reuse detection burns the chain), 2FA, why localStorage tokens are a smell.
  🔥 The URL that betrayed you: user-facing links built from a CORS-origin env var that was `localhost` in prod — password-reset emails pointing nowhere. Env vars have *audiences*.
  🔨 Add sessions + refresh rotation to Relay; write the env-var audience table.
  🤖 Security review prompts that actually catch things; making the agent enumerate env-var consumers.

- **5.4 Input you didn't realize you were trusting.**
  🔥 Three audit finds on one app: a streaming proxy that followed redirects anywhere and would sign internal URLs (read-SSRF, with a secret that silently fell back to a hardcoded dev literal); an anonymous telemetry endpoint with no auth, limits, or length caps — free usage-count inflation and metric pollution; and the realization that the CDN-provided client-IP header is forgeable if anyone can reach the origin directly.
  📐 Adversarial-input inventory: URLs you fetch, headers you trust, metrics you rank by. A security primitive only helps if *every* code path uses it; secrets must fail closed, never fall back.
  🔨 Threat-model Relay's three anonymous endpoints; route all outbound fetches through one SSRF-guarded function.
  🤖 The standing prompt: "list every place this handler trusts something the client controls."

- **5.5 Email is production infrastructure.**
  🔥 Three email incidents on one platform: the SMTP provider silently rejecting mail because the From address wasn't an owned mailbox (and a module-load-timing bug meant the configured From was read too early); password-reset links built from a CORS env var pointing at localhost; and the "bob" attack burning sender reputation by bombing strangers with verification emails.
  📐 Transactional vs marketing mail; sender reputation as a shared, damageable resource; verification/reset flows as security surfaces; newsletters as background jobs (idempotent sends, atomic dedup).
  🔨 Add transactional email + a newsletter to Relay: owned From address, dedicated link base URL, per-email cooldowns, an idempotent send job.
  🤖 Making the agent enumerate every code path that sends mail — and what each one costs when abused.

- **5.6 The OWASP Top 10, mapped to a real app.**
  🔥 A full security audit of the reference platform scored it against OWASP — and the failures weren't exotic: SSRF in a proxy (A10), secrets falling back to defaults (A05), no server-side error tracking (A09), a credential-bearing CI runner executing untrusted PR code (A08, supply chain), tag-pinned third-party actions.
  📐 The OWASP Top 10 as a working checklist, not a certification: injection, broken access control, misconfiguration, vulnerable dependencies, SSRF — each mapped to where it actually appears in an agent-built codebase. Supply-chain hygiene: lockfiles, SHA-pinning, dependency audit gates.
  🔨 Run an OWASP-structured self-audit of Relay; fix the top three findings; add a dependency-audit gate to CI.
  🤖 The standing security prompt: "review this diff as an attacker: what can I reach, forge, inject, or exhaust?" — and why security review needs its own pass, separate from correctness review.

## Module 6 — One Backend, Many Clients

- **6.1 The client fleet problem.**
  📐 Web deploys in minutes; mobile releases live for months. API versioning, tolerant readers, force-update gates as the last resort.
  🔥 A force-update gate wired to store versions: enable the store release *first*, then flip the minimum version — order matters or you brick users.
  🔨 Add a versioned API + a mobile-style "min supported version" gate to Relay.

- **6.2 Over-the-air updates and the revert trap.**
  🔥 An OTA update published from a feature branch — the next OTA from main silently reverted it. And OTA env handling that stripped runtime config unless the environment was named explicitly.
  📐 Update channels are state machines. Every publish path needs a single source of truth (main).
  🔨 Simulate channel discipline with Relay's staging/prod flag config.

- **6.3 Feature flags done once, not five times.**
  🔥 The same flag checked at compile time in one surface and runtime in another — nav showed a feature the route 404'd.
  📐 One runtime flag map, resolved in one place, consumed everywhere. Flags are config, not code.
  🔨 Add a runtime flag system to Relay gating one route + its nav + its promo stripe together.

- **6.4 Deep links and the drift problem.**
  🔥 A hand-maintained list of "routes the app knows" rotted as routes were added — deep links fell back to web for pages the app had. Fix included a drift-guard test that fails the build when the list and the router disagree.
  📐 Any two sources of truth will diverge. Either derive one from the other or install a tripwire.
  🔨 Write a drift-guard test for Relay's sitemap vs its route table.
  🤖 Drift-guards as the general antidote to agent-maintained parallel lists.

- **6.5 Sign in with Google & Apple, on every client.**
  🔥 Three OAuth incidents from one product: Apple sign-in failing with "invalid password" because the server verified tokens against the *web* client ID while native iOS tokens carry the bundle ID (and the client swallowed the real error); Google sign-in returning to a permanently blank app because a deep-link interceptor mangled the single-slash redirect URL; and the Google button that silently didn't exist because build-time client IDs were missing from the shipped build.
  📐 One provider, many audiences: web/iOS/Android each get their own client ID and token audience — the backend must accept all valid ones. Auth redirects must pass through your URL handling untouched. Surface real error bodies or every config mismatch looks like a wrong password.
  🔨 Wire Google + Apple sign-in into Relay's web and mobile clients against one backend; write the audience table (platform → client ID → token aud).
  🤖 The review question: "which token audiences does this endpoint accept, and which client produces each?"

- **6.6 API design that survives its clients.**
  🔥 A 502 landed exactly between "files stored" and "upload confirmed" — orphaning files because the confirm wasn't idempotent. And a client that swallowed server error bodies, turning a one-line config fix into a blind debugging session.
  📐 Pagination (cursor vs offset), idempotency keys, partial failure across a two-step boundary, error contracts (machine-readable codes + human messages), consistent envelopes. Rate-limit headers as part of the contract.
  🔨 Give Relay's API cursor pagination, an idempotent upload-confirm, and a single error envelope every client parses.
  🤖 Have the agent generate the API contract table first (endpoint → auth → idempotency → error codes) and implement against it.

## Module 7 — Observability: You Can't Fix What You Can't See

- **7.1 The dashboard that lies and the metric that doesn't.**
  🔥 "Returning users" counted logins; the honest metric was distinct days of real use. Same data, different question.
  📐 Choose metrics that measure the user's reality, not the system's convenience.
  🔨 Add basic analytics events + one honest retention metric to Relay.

- **7.2 Errors, logs, and the noise floor.**
  🔥 A crash dashboard dominated by three noisy non-actionable errors, hiding real ones. A staging process discovered still running — two months stale — quietly serving old code.
  📐 Alert on symptoms users feel; triage by actionability; audit what's actually running.
  🔨 Wire Sentry (or equivalent) into Relay; write the "what's running where" runbook page.

- **7.3 Search is telemetry.**
  🔥 Zero-result searches revealed both a normalization bug and what users actually wanted.
  📐 Instrument the failure paths of discovery features — they're free user research.
  🔨 Log Relay's zero-result searches; fix the top normalization miss.

- **7.4 Background jobs: the code nobody watches.**
  🔥 Scheduled push jobs that could run twice (no claim lock), left no audit record, and never checked delivery receipts — duplicates and silent failures both undetectable. Same pattern found in the newsletter sender and render queue (no lease → jobs stuck forever).
  📐 Every background job needs three things: an idempotency lock (SET NX EX), an audit trail, and reconciliation of what was actually delivered. Fire-and-forget means forget.
  🔨 Give Relay a scheduled job done right: claim key, audit row, receipt check, stale-job sweep.

- **7.5 Product analytics in practice: GA, Cloudflare, and owning your events.**
  🔥 Echoes from the bank: "returning users" measured logins (7.1); offline usage invisible (sampling bias); analytics tables growing without retention (2.4); a heartbeat endpoint anyone could inflate (5.4). Every one is an *analytics* failure before it's anything else.
  📐 The three tiers and what each answers: Cloudflare Web Analytics (edge truth: requests, cache ratio, bots — no JS, no consent baggage), Google Analytics 4 (behavioral funnels — events model, consent mode, sampling caveats), and first-party events in your own DB (the only tier you can join against your domain data). When to use which; why edge numbers and GA numbers never match; privacy and consent as design constraints, not banners.
  🔨 Instrument Relay with all three tiers; define one funnel (visit → signup → first action) and reconcile the three tiers' counts for it — the differences are the lesson.
  🤖 Agents love adding events; nobody deletes them. The standing rule: every event has an owner question ("what decision does this inform?") or it doesn't ship.

## Module 8 — Safety Nets for AI-Generated Code

- **8.1 The 600-file near-miss.**
  🔥 One branch created from the wrong base + one `git add .` deleted 600+ files. The response wasn't "be careful" — it was hooks: staged-file count limits, deletion-size tripwires, base-branch verification.
  📐 At agent speed, process rules must be mechanical. Anything enforced by memory will fail.
  🔨 Install pre-commit and pre-push guards in Relay's repo.
  🤖 Git hygiene rules that belong in every CLAUDE.md.

- **8.2 Tests as the spec the agent can't ignore.**
  📐 TDD with an agent: red-green-refactor as a prompting pattern, not a ritual. Which tests earn their keep (drift-guards, contract tests, E2E smoke) vs vanity coverage.
  🔥 A ~3,200-test suite kept green across hundreds of agent PRs — and the cold-compile E2E false-failures that had to be engineered away before anyone trusted it.
  🔨 Build Relay's three-layer test pyramid; make CI block merges.

- **8.3 CI preflight and the boy-who-cried-wolf check.**
  🔥 A preflight check that always failed (wrong package manager assumption) trained everyone to ignore it — the most dangerous state a check can be in.
  📐 A check that can be ignored will be. Fix it or delete it; never let it lie.
  🔨 Add a preflight script to Relay; prove every check can actually fail *and* actually pass.

## Module 9 — Directing an AI Team

- **9.1 You are the architect now.**
  📐 The division of labor: agents write components; you own seams, invariants, and taste. Specs before code (spec → plan → tasks); acceptance criteria as the contract.
  🔨 Run one Relay feature through a full spec-driven cycle.

- **9.2 Context engineering.**
  📐 Why agents degrade with bloated context; progressive disclosure; what belongs in CLAUDE.md vs a spec vs a memory file. Writing docs *for an agent audience*.
  🔨 Write Relay's CLAUDE.md properly; measure the difference on a real task.

- **9.3 Every repeated review comment is a missing guardrail.**
  📐 The review-to-guardrail pipeline: flag it twice → automate it (lint rule, test template, hook) → stop reviewing for it. The review surface should shrink over time.
  🔨 Convert your three most-repeated review nits into automated checks.

- **9.4 Verification before completion.**
  🔥 The deploy "verified" through a CDN cache; the push notifications "shipped" that were never wired to the sender; the flag that was "on" in a config nobody read.
  📐 "Done" requires evidence from the layer the user touches. Screenshots of localhost are not evidence.
  🔨 Write Relay's definition-of-done checklist; make the agent produce evidence, not assurances.

- **9.5 Claude Code power techniques.**
  📐 The toolbox that separates casual use from directing a fleet: CLAUDE.md hierarchy (global vs project) and persistent memory files; hooks that enforce rules mechanically (the pre-commit guards from 8.1 are hooks); custom slash commands and skills for repeatable workflows; subagents and git worktrees for parallel isolated work; headless runs for CI and cron; permission settings that reduce prompts without reducing safety.
  🔥 Real artifacts from the reference project: a deploy skill, a staging-deploy skill, an audit skill, spec-kit commands — each one a workflow that used to live in someone's head.
  🔨 Build your first three: a project CLAUDE.md that passes the "new agent cold-start" test, one hook that enforces a rule you keep repeating, one skill for your most common workflow.
  🤖 Meta-rule: whenever you correct the agent twice for the same thing, the correction belongs in CLAUDE.md, a hook, or a skill — never in the chat.

- **9.6 Building your agent team: custom agents and skills.**
  🔥 The reference platform runs as an AI-first company: an Orchestrator routing work to specialist agents (backend, frontend, mobile, QA, security, code-reviewer...), spec-kit commands for spec → plan → tasks, checkpoints where the human decides. It shipped hundreds of PRs this way — and its failure modes shaped every rule in this module.
  📐 When one agent is enough vs when to specialize; agent definitions as job descriptions (scope, tools, escalation rules); skills as the team's standard operating procedures; quality gates between agents; the human as CEO, not reviewer-of-everything.
  🔨 Define two specialist agents for Relay (e.g. reviewer + QA) with explicit scopes, and one orchestration workflow that uses both with a gate between them.
  🤖 The escalation contract: agents never make product decisions — ambiguity goes up, not sideways. Write it into every agent definition.

- **9.7 Code audit and review at agent speed.**
  🔥 The reference project's periodic full audits (an agent sweeping the entire codebase against a structured checklist) produced the incident bank's best finds: the SSRF proxy, the analytics timebomb, the mocked-test blind spot, the CI supply-chain exposure — none of which any single PR review would have caught.
  📐 Three review layers with different jobs: per-PR review (catch defects before merge), adversarial multi-pass review (independent reviewers per dimension — correctness, security, performance — then verify each finding to kill false positives), and periodic whole-system audits (find what no diff shows: drift, dead code, contradicted docs, systemic risk). Audit reports as living documents with severity, owner, and status.
  🔨 Run all three on Relay: agent-review one PR, adversarially re-review it on the security dimension, then run a whole-repo audit against a 10-point checklist and file the findings.
  🤖 Review prompts that work: assign one dimension per pass; require a failure scenario for every finding ("what input makes this break?"); verify findings adversarially before acting.

## Module 10 — Scaling Beyond One Server

Concept-complete module: the classic scaling canon, taught through the lens of a
product that grew — with incidents cited where we have them.

- **10.1 Stateless services and load balancing.**
  📐 Why state in the process kills horizontal scaling (sessions, in-memory counters, local uploads); load balancer types (L4/L7); health checks; sticky sessions and why to avoid them.
  🔥 Echo from 5.2: in-memory rate-limit counters that reset per deploy and didn't share across instances — the same trap in miniature.
  🔨 Run two instances of Relay's API behind a load balancer; find and evict every piece of process state.

- **10.2 Queues and asynchronous work.**
  📐 When a request shouldn't do the work: queues, workers, at-least-once delivery (so consumers must be idempotent), backpressure, dead-letter queues, exactly-once as a lie.
  🔥 Echo from 7.4: the fire-and-forget jobs with no locks, no audit, no receipts — a queue-shaped problem solved without understanding queues.
  🔨 Move Relay's media processing and email sending onto a queue with a dead-letter lane and a stale-job sweep.

- **10.3 Scaling the database.**
  📐 The escalation ladder: indexes → caching → read replicas (and replication lag's lies) → vertical scaling → partitioning/sharding as the last resort. Backup/restore implications at each rung. Why most products never need rung five.
  🔨 Add a read replica to Relay; route analytics reads to it; demonstrate replication lag and handle it honestly.

- **10.4 Realtime: presence, websockets, and heartbeats.**
  🔥 The live-presence system from the incident bank: heartbeat ZSETs, the FLUSHDB wipe, the client-trusted counter inflation.
  📐 Polling vs SSE vs websockets; presence as soft state that self-heals; capping cardinality; why realtime data must never be your source of truth.
  🔨 Add a "who's online" presence feature to Relay that survives a cache flush and a malicious client.

- **10.5 Performance and capacity.**
  📐 Latency budgets end-to-end; percentiles (p50 lies, p99 pays the bills); load testing before launch days; Core Web Vitals as the frontend contract; back-of-envelope capacity math a vibe coder can actually do.
  🔥 Echo from 2.5: the dashboard COLLSCAN — a capacity problem invisible until the working set was evicted.
  🔨 Load-test Relay to its breaking point; write down the number; fix the first bottleneck; measure again.

## Module 11 — Reaching the World

- **11.1 Domains, DNS, and TLS.**
  📐 What actually happens before your server hears anything: DNS records and propagation lies, apex vs subdomains, TLS certificates and auto-renewal, why the CDN terminates TLS, CDN-only ingress (echo of the forgeable client-IP header from 5.4).
  🔨 Put Relay on a real domain with TLS, a www redirect, and origin locked to CDN-only ingress.

- **11.2 Internationalization and RTL.**
  🔥 Real bilingual-product scars: web URLs locale-prefixed while app routes weren't (deep links landed on Home); text-normalization gaps that made search miss valid queries in a non-Latin script; layouts that broke mirrored.
  📐 Locale routing strategies; translation files as a drift surface (drift-guard tests again); RTL as a first-class layout mode, not a patch; dates, numbers, and collation.
  🔨 Ship Relay in two locales — one RTL — with a locale-drift guard test.

- **11.3 SEO and AEO: being found by crawlers and cited by answer engines.**
  🔥 The 350MB monolithic sitemap, and the split version that froze the build when the API was down at build time.
  📐 SEO: what crawlers actually fetch; sitemaps at scale (chunked, dynamic); canonical URLs and hreflang; Open Graph cards; Core Web Vitals as a ranking input; don't couple build success to runtime data. AEO (answer-engine optimization): AI assistants and answer engines are becoming the front door — structured data (schema.org/JSON-LD) so machines can parse your meaning, content written to be *citable* (direct answers, stable anchors), llms.txt as an emerging convention, and monitoring AI crawlers in your logs (they don't behave like Googlebot).
  🔨 Give Relay chunked sitemaps, hreflang pairs, OG cards, and JSON-LD on its two main page types; then ask three AI assistants a question your product answers and see whether — and how — you're cited.

- **11.4 Cost engineering.**
  📐 The bills that surprise you: egress (why object-storage egress fees drove a real GCS→R2 migration), storage tiers, database growth (echo of the analytics timebomb), CDN as a cost shield, the cost of "free" background jobs. Reading your first cloud bill like an SRE.
  🔥 Echo from 2.3: the backup that tripled — cost bugs and correctness bugs are often the same bug.
  🔨 Build Relay's monthly cost model (storage, egress, compute) at 1×, 10×, 100× users; find the line item that scales worst.

- **11.5 Your edge platform in practice: Cloudflare end to end.**
  🔥 The reference platform's whole edge story in one place: the `Vary` header it ignores (3.2), the client-IP header it provides (5.2), the 5-minute HTML cache that fooled deploy verification (4.3), the WAF that blocked the team's own automation, Turnstile in the abuse defenses (5.1), R2 as primary storage with its egress economics (11.4).
  📐 One platform, many products — and each is a system-design decision: DNS + proxy mode (orange cloud), cache rules and what "respect origin headers" really means, WAF and bot management (and your own robots), Turnstile, R2, Workers as edge compute, and Cloudflare's analytics as the edge-truth tier from 7.5. The recurring rule: the edge is configuration you own on a platform you don't — version it, test through it, never assume defaults.
  🔨 Put Relay fully behind Cloudflare: proxy mode, one cache rule, WAF on, Turnstile on signup, CDN-only origin ingress — then re-run the lesson 3.2 poisoning attempt and the 5.2 rate-limit test through the real edge.
  🤖 Agents configure the edge blind (they can't see your dashboard). Export/document the edge config in the repo so the agent designs *with* it, not around it.

## Module 12 — Capstone: You Get Paged

Eight incident simulations. Each gives you symptoms only (user reports, status codes,
graphs); you diagnose, propose the fix, then compare against what actually happened
in production. Drawn from the incident bank:

1. Pages render as raw JSON for some users, some of the time.
2. Flapping 502s that stop when you restart something you "shouldn't have to."
3. Nightly backup size triples with no data growth.
4. Legit users hit 429s the day after a traffic spike.
5. A deleted file keeps coming back.
6. Your mobile fix disappears a week after you shipped it.
7. The app store rejects your build for content that plays fine on your machine.
8. Your live-presence counter drops to zero the moment someone "clears the cache."

Passing bar: correct layer identified, plausible root cause, a fix that survives
the follow-up question "and how do you know it worked?"

---

## Format notes

- Each lesson ≈ 1,500–2,500 words + diagrams (Mermaid) + a build-along commit.
- Modules ship as directories: `modules/NN-slug/lesson-N.md`.
- Incident bank (`war-stories/incident-bank.md`) is the raw source of truth;
  lessons cite it. New incidents land there first.
