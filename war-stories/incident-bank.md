# Incident Bank

Raw material for lessons. Every entry: symptoms → root cause → fix → principle.
Lessons cite these; new incidents land here first. Details are drawn from a real
production audio-streaming platform (web + iOS + Android + TV, global audience,
Cloudflare CDN, VPS origin, MongoDB/Redis/R2 object storage).

Status key: 🟢 used in a lesson · ⚪ unassigned

---

## Caching & CDN

### 🟢 CDN cache poisoning via RSC flight responses *(→ Lesson 3.2)*
- **Symptoms:** Some users saw pages render as raw `0:{...}` JSON; intermittent, self-healing, nothing in logs.
- **Root cause:** CDN ignores `Vary`; cached a React Server Component flight (JSON) response as the page HTML for that URL.
- **Fix v1 (failed silently):** Middleware stamped flight responses `no-store` — a framework upgrade stripped the detection headers before middleware ran; fix became inert.
- **Fix v2 (durable):** nginx guard keyed on response `Content-Type: text/x-component` → force `private, no-store`. Encoded into the deploy script with a "never trim" rule.
- **Principle:** Poisoning = response varies by something the effective cache key doesn't capture. Defend at the most stable layer you control; pair every guard with a tripwire.

### 🟢 Deploy "verified" through a 5-minute CDN HTML cache *(→ Lesson 4.3)*
- **Symptoms:** Deploy declared live; users (and the deployer) still saw the old site.
- **Root cause:** CDN caches HTML ~300s; checking the public URL verified the cache, not the origin.
- **Fix:** Post-deploy verification compares CSS/asset hash against origin directly before declaring success.
- **Principle:** Deploy verification must pierce every cache between you and the user.

### 🟢 Cache invalidation aimed at a key nobody reads *(→ Lesson 3.3)*
- **Symptoms:** Stale data survived mutations that "cleared the cache."
- **Root cause:** Reads populated one Redis key shape; invalidation deleted another (bare slug vs derived key).
- **Fix:** Centralized cache-key construction; mutation tests assert the read-path key is cleared.
- **Principle:** Invalidate through one shared function or you invalidate through zero.

### 🟢 Stale JS served after a "successful" deploy — twice *(→ Lesson 4.3)*
- **Symptoms:** Deploy reported success; users kept receiving old JavaScript.
- **Root cause:** The framework's persistent webpack build cache reused stale modules across builds.
- **Fix:** Deploy script deletes the build cache before every frontend build.
- **Principle:** A release pipeline must treat build caches as untrusted — they optimize speed, not correctness.

### ⚪ Admin-only analytics cacheable by shared caches
- **Symptoms:** Audit finding: auth-gated admin analytics responses carried `Cache-Control: public, s-maxage=600` on URLs with no auth component — poisonable to anonymous clients.
- **Fix:** Force `private`/`no-store` on any auth-gated handler.
- **Principle:** A response that varies by identity must never be publicly cacheable; the auth dimension must be in the key or caching must be off.

### ⚪ Redis with no memory cap = latent full outage
- **Symptoms:** Audit: Redis had no `maxmemory`/eviction policy (default `noeviction`). On OOM, every cache write fails silently and 100% of traffic falls through to the database.
- **Fix:** `maxmemory` + `allkeys-lru` — one line.
- **Principle:** "Cache down" must degrade to *slow*, not *down*. An unbounded cache is an outage on a timer.

### ⚪ Cache stampede on cold start
- **Symptoms:** Risk: on deploy or Redis restart, every concurrent request on a cold key recomputes the same expensive aggregation simultaneously.
- **Fix:** Single-flight lock so one request populates the key while the rest wait.
- **Principle:** Cache expiry is a synchronized load spike aimed at your weakest moment; coalesce misses.

### ⚪ FLUSHDB wiped live-presence state along with the cache
- **Symptoms:** Real-time "listening now" counter dropped instantly to zero.
- **Root cause:** Response cache and semi-durable presence state (heartbeat ZSETs) shared one Redis DB; a blunt `FLUSHDB` cache-clear destroyed both.
- **Fix:** Never flush; evict by narrow key prefix (`SCAN` + `UNLINK`). Presence self-healed via heartbeats in ~60s.
- **Principle:** Colocating disposable and non-disposable state in one store turns cache maintenance into data loss. Segregate, or only ever evict by prefix.

### ⚪ CDN bot protection blocked the team's own automation
- **Symptoms:** Screenshot automation rendered pages with blank images (`naturalWidth=0`).
- **Root cause:** The media domain's WAF blocks headless-browser fingerprints — including the team's own tooling.
- **Fix:** Intercept media requests in the automation and fetch bytes out-of-band server-side.
- **Principle:** Your abuse defenses can't tell your robots from attackers'; plan an out-of-band path for your own automation.

## Deployment & Infrastructure

### 🟢 Blue-green deploys that still 502'd *(→ Lesson 4.2)*
- **Symptoms:** 502s during "zero-downtime" deploys.
- **Root cause:** Both colors built into and served from the same `.next` build directory; bringing up the new color clobbered assets the live color was serving.
- **Fix:** Per-color build directories (`.next-blue` / `.next-green`). Proven with 0 dropped requests under live traffic.
- **Principle:** Two instances isn't isolation unless *everything* is duplicated — builds, dirs, ports, state.

### 🟢 The 502 that created blue-green in the first place *(→ Lesson 4.1)*
- **Symptoms:** During an in-place `pm2 restart`, an upload client hit 502 on its confirm call *after* the storage PUTs succeeded — files orphaned in storage.
- **Root cause:** Single-process restart = a ~10s window where the proxy routes to a dead upstream.
- **Fix:** Blue-green: start + health-check the new color on another port, flip traffic, then stop the old.
- **Principle:** In-place restarts have an unavoidable downtime window. Also: any storage-then-confirm boundary needs idempotent reconciliation, because the failure will land exactly between the two.

### 🟢 nginx stale worker serving the dead color *(→ Lesson 4.3)*
- **Symptoms:** Flapping 502s from the edge after a flip while direct-to-origin curl returned 200; app logs clean.
- **Root cause:** A stale nginx worker, kept alive by upstream keepalive connections, outlived the graceful reload and kept routing to the drained color.
- **Fix:** Full nginx restart after each flip; durable fix is bounding worker lifetime (`worker_shutdown_timeout`).
- **Principle:** Graceful reload doesn't drain long-lived keepalive connections; "reloaded" and "restarted" are different guarantees.

### ⚪ Hardcoded proxy_pass took the whole site down after a flip
- **Symptoms:** Full-site 502 for ~3 minutes after a blue-green flip.
- **Root cause:** The proxy config hardcoded `localhost:3000` instead of the named upstream block; the flip moved the app to another port.
- **Fix:** Deploy script asserts the config points at the upstream block and aborts otherwise.
- **Principle:** Indirection you rely on at deploy time must be enforced by an automated precondition, not convention.

### ⚪ Sibling subdomains kept pointing at the dead color
- **Symptoms:** After a flip, the admin uploader on a secondary subdomain broke with generic network errors.
- **Root cause:** Secondary nginx configs (`upload.`, `direct.`) proxied to a hardcoded port and weren't updated by the flip — only the main site block was.
- **Fix:** Bootstrap script patches all sibling configs to route through the same shared upstream (idempotent).
- **Principle:** Every consumer must go through one source of routing truth; parallel hardcoded copies drift and one gets missed at cutover.

### ⚪ `location /api` swallowed `/api-next/*`
- **Symptoms:** Next.js route handlers under `/api-next/` were misrouted to the Express API.
- **Root cause:** nginx prefix match without a trailing slash also captures sibling paths.
- **Fix:** `location /api/` (trailing slash).
- **Principle:** Prefix routing silently over-matches; be explicit about boundaries.

### ⚪ Two deploy paths, one system — and they drifted
- **Symptoms:** Audit: the local deploy skill did blue-green while the CI workflow did stop-then-start with root SSH, unverified rollback tags (0 found in history), and no health gate. 15 releases in one day (hotfix bursts) showed the change-failure cost.
- **Principle:** Two deploy mechanisms for one system guarantees drift; a rollback that isn't verified to exist is not a rollback.

### ⚪ CI + deploy on the developer's personal Mac
- **Symptoms:** All blocking CI and auto-deploy on a self-hosted macOS runner that only runs while the Mac is awake, holds SSH keys, and executes untrusted PR code; third-party actions tag-pinned, not SHA-pinned. Single runner also serialized the whole PR queue.
- **Principle:** A credential-bearing host running untrusted code is a supply-chain compromise waiting to happen; cost workarounds become availability SPOFs. CI capacity is part of lead time.

### 🟢 Backup grew 244 MB → 871 MB overnight *(→ Lesson 2.3)*
- **Symptoms:** Nightly backup size tripled with no data growth.
- **Root cause:** tar excluded `.next` but the blue-green refactor created `.next-blue`/`.next-green` — each holding ~620 MB webpack caches, archived nightly.
- **Fix:** Exclude `.next-*` and `*/cache/webpack`; clarified backup scope = the two Mongo DBs + configs (code is redundant with GitHub).
- **Principle:** Back up state, not artifacts. Backup scripts rot when the directory layout evolves — audit contents, not just exit codes.

### 🟢 Stale staging process running unnoticed for two months *(→ Lesson 7.2)*
- **Symptoms:** A staging process from May discovered still alive in July, serving old code.
- **Fix:** Process cleanup; "what's running where" became a checkable runbook item.
- **Principle:** Audit the actual state of production, not your mental model of it.

### ⚪ Stale runtime config override beat source config
- **Symptoms:** A feature 404'd on staging despite correct source configuration.
- **Root cause:** A forgotten flag-override document in the database outranked the declarative config.
- **Fix:** Cleared the override manually.
- **Principle:** Runtime overrides that outrank declarative config create invisible precedence bugs; make overrides observable and expirable.

### ⚪ Long-running VPS jobs killed by SSH hangups
- **Symptoms:** Multi-hour data imports died mid-run when the SSH session dropped.
- **Fix:** nohup + detached execution for anything long-running.
- **Principle:** Any job longer than minutes must not depend on your laptop's Wi-Fi.

## Data & Storage

### 🟢 Deleted files resurrecting from the old storage backend *(→ Lesson 2.2)*
- **Symptoms:** Files deleted from R2 object storage kept reappearing.
- **Root cause:** GCS→R2 migration left pull-through replication (Sippy) enabled; every R2 miss re-fetched from GCS, restoring deletes.
- **Fix:** Delete from both backends; end the dual-source phase explicitly.
- **Principle:** A migration isn't done until the old system can no longer act. Dual-read/write phases need explicit end dates.

### 🟢 Schema keyed on the wrong identity *(→ Lesson 2.1)*
- **Symptoms:** A reciter with two recitation styles in the same narration — one style unrepresentable.
- **Root cause:** Recitations keyed by narration only; style existed in storage layout but not in the data model's identity.
- **Principle:** The keys you choose early are the constraints you live with longest. Model identity from the domain's edge cases.

### ⚪ Analytics retention removed → unbounded growth timebomb
- **Symptoms:** Audit: every raw-event collection had its TTL deliberately removed; ~3.65M rows/year growing forever on the same VPS as the primary DB — headed for disk-full/OOM taking the whole site down together. A model comment still claimed "expire after 90 days."
- **Fix (prescribed):** Reinstate raw TTLs; serve long-range dashboards from daily rollups.
- **Principle:** Retention is a reliability control, not just a privacy one. Co-locating analytics with the primary DB couples their failure domains. Comments that contradict code are landmines.

### ⚪ The golden rule for destructive retention migrations
- **Context:** Re-enabling raw-event TTLs without losing dashboard history.
- **Rule:** Never enable a TTL until every stat reading beyond the window is backed by an aggregate that has been backfilled *and verified against raw*. Sequence: backfill → verify → then expire.
- **Also found:** The rollup grouped on session *start* timestamp while age was measured on *last* timestamp — a midnight-spanning session could be purged before the aggregate captured it.
- **Principle:** Ordering turns an irreversible operation into a safe one. Retention and aggregation jobs must key on the same time semantics or boundaries silently lose data.

### ⚪ Concurrent uploads clobbered each other → forced sequential
- **Symptoms:** Admin bulk upload took 15–30 minutes for 114 files, one at a time, and felt hung.
- **Root cause:** Server did read-modify-write on one big document per file (`findOne` → push → `save`), so parallel requests dropped each other's files — sequential was the workaround, not the design.
- **Fix:** Direct-to-storage signed-URL uploads in parallel (independent keys, raceless) + one atomic confirm.
- **Principle:** Read-modify-write on a shared aggregate can't take concurrency. Make writes independent; collapse shared mutation into one atomic append. Route big payloads around the app server.

### ⚪ Account deletion didn't cascade
- **Symptoms:** Deleting a user removed one document; ~13 linked collections kept personal/behavioral data forever — while the privacy policy promised full erasure.
- **Fix:** A tested `deleteUserData()` cascade wired into both self-service and admin deletion.
- **Principle:** "Delete" must be defined over the full data graph. A policy that outruns the implementation is itself a liability.

### ⚪ Production DB cloned to laptops, unscrubbed
- **Symptoms:** Real emails, OAuth IDs, and push tokens copied to staging and dev machines.
- **Fix (prescribed):** Pseudonymize PII in the staging-refresh script.
- **Principle:** Every copy of production data inherits production's blast radius.

### ⚪ One dashboard load evicted the whole working set
- **Symptoms:** A single admin page ran eight unbounded whole-collection scans over the largest table, evicting the hot catalog data from memory.
- **Fix (prescribed):** Cache + date-bound the query; add compound indexes.
- **Principle:** One unbounded analytical query on a hot OLTP store is a cache-eviction bomb; bound and index heavy aggregations.

### ⚪ 350MB sitemap + build-time prerender froze on a dead API
- **Symptoms:** A monolithic 350MB sitemap; the split version froze the build when the API was unreachable at build time.
- **Fix:** Sitemap index + ~21 dynamically-served chunks; no build-time data dependency.
- **Principle:** Don't couple build success to runtime data availability; chunk large generated documents.

### 🟢 Env var reused across audiences: broken email links *(→ Lesson 5.3)*
- **Symptoms:** User-facing links in emails pointed to localhost in production.
- **Root cause:** Links built from `CLIENT_URL`, whose real job was CORS configuration.
- **Fix:** Separate `PUBLIC_SITE_URL`; rule: never build links from infra-purpose vars.
- **Principle:** Every env var has an audience; one var serving two will eventually be wrong for one.

## Security, Abuse & Auth

### 🟢 Everyone shared one rate-limit bucket behind the CDN *(→ Lesson 5.2)*
- **Symptoms:** Legitimate users receiving 429s at modest traffic.
- **Root cause:** Limiter keyed on socket IP; behind Cloudflare all traffic arrives from CDN IPs. Also: in-memory counters reset per deploy and didn't share across instances.
- **Fix:** Key on `CF-Connecting-IP`; counters in Redis; fail-open on store errors.
- **Corollary (audit):** That header is only trustworthy if clients can't reach the origin directly to forge it — enforce CDN-only ingress and strip inbound copies at the edge.
- **Principle:** Behind any proxy, "client IP" is a claim you must configure deliberately — and defend from forgery. Distributed limits need shared state.

### 🟢 The "bob" registration email-bombing flood *(→ Lesson 5.1)*
- **Symptoms:** 45 accounts in 24h, all named "bob," registered with *other people's* real emails — each triggering a verification email to the victim (harassment + burned SMTP sender reputation).
- **Root cause:** Anonymous endpoints that send email, with a limiter loose enough to permit 120/day/IP.
- **Fix:** CAPTCHA on register/forgot; tighter per-IP limit; a global *email* budget that throttles the send, not the signup (so an attacker can't DoS legit registrations); per-email cooldown with constant generic responses. A global registration circuit-breaker was explicitly rejected — a fixed site-wide cap is itself a DoS vector.
- **Principle:** Rate-limit the expensive side effect, not the user action. Any anonymous endpoint that triggers outbound email is a weapon against third parties. Naive global caps become self-DoS.

### ⚪ The streaming proxy was a read-SSRF
- **Symptoms:** Audit: an unauthenticated audio-proxy endpoint followed redirects and signed URLs from the *redirected* upstream — an attacker-influenced source could get the server to sign internal URLs (cloud metadata service, local Redis).
- **Root cause:** Raw `fetch(..., {redirect:"follow"})` instead of the project's own SSRF-guarded fetch; the signing secret silently fell back to the JWT secret and finally to a hardcoded dev literal.
- **Fix (prescribed):** Every hop through the guarded fetch with manual redirects + private-IP checks; dedicated secret that fails closed if unset.
- **Principle:** A security primitive only helps if every code path uses it. Re-validate per redirect hop. Secrets must never silently fall back.

### ⚪ Anonymous telemetry endpoints fully client-trusted
- **Symptoms:** Audit: the "now playing" heartbeat had no auth, no rate limit, no schema, no length caps, keyed on a client-chosen session ID — anyone could inflate listen counts, pollute rankings, and flood the store.
- **Fix (prescribed):** Length-cap fields, per-IP limits, cap the presence set's cardinality, treat ranking inputs as adversarial. (Also learned: dedup blocks *replay*, not *forged-unique* inflation.)
- **Principle:** Data that drives product decisions is adversarial input. Anonymous + unlimited + unvalidated writes corrupt metrics and invite write-amplification DoS.

### ⚪ Privacy declarations contradicted the app's behavior
- **Symptoms:** The published policy and store data-safety forms declared "no data collection, no accounts" — while the app had accounts, push tokens, analytics, and a location library. Stores cross-check declarations against observed behavior.
- **Principle:** Compliance declarations are executable contracts. Drift between stated and actual practice is a live legal/store-rejection risk independent of any code bug.

### ⚪ Diagnostic capture stored secrets forever
- **Symptoms:** Audit stop-item: the error-report store kept raw URLs (which can contain live password-reset tokens) and free-form metadata, with no TTL.
- **Fix (prescribed):** Redact URLs on ingest, allowlist metadata, add retention.
- **Principle:** Diagnostics are a data-exfiltration surface; redact on ingest, expire on schedule.

### ⚪ Rotating refresh tokens with reuse detection
- **Design:** 180-day sliding refresh tokens; reuse of a rotated token burns the whole chain.
- **Principle:** Assume token theft; design so theft is detectable and bounded.

## Multi-Client (Web / Mobile / TV)

### 🟢 OTA update silently reverted *(→ Lesson 6.2)*
- **Symptoms:** A shipped mobile fix vanished days later.
- **Root cause:** OTA published from a feature branch; the next OTA from main didn't contain it.
- **Principle:** Every publish channel needs exactly one source of truth.

### ⚪ OTA/build config traps (collection)
- `eas update` without `--environment production` silently strips `EXPO_PUBLIC` runtime config.
- Untracked native prebuild dirs make OTA publishing fail with a misleading "bare workflow" error.
- Publishing from a worktree with symlinked node_modules breaks the bundler on local modules.
- Giant local caches (11GB index, 2.1GB prebuild) caused disk-full and upload failures until ignored.
- **Principle:** Update tooling has its own config model; verify what the artifact actually contains, not what the source says.

### ⚪ TV apps submitted to two stores pointing at localhost
- **Symptoms:** Samsung certification rejected ("unable to play content"); the LG submission carried the byte-identical broken bundle.
- **Root cause:** A stray gitignored `.env.local` (`VITE_API_BASE=http://localhost:3105`) was inlined at build time — invisible in any diff.
- **Fix:** A postbuild verifier that fails loudly if compiled output contains `localhost` or lacks the production origin.
- **Principle:** Build-time env inlining + gitignored local overrides = silent corruption. Verify release artifacts against their *compiled output*, not their source.

### 🟢 Feature flag checked two different ways *(→ Lesson 6.3)*
- **Symptoms:** Nav showed a feature whose route 404'd, depending on surface.
- **Root cause:** One surface read the flag at compile time, another at runtime — two sources of truth.
- **Fix:** Single runtime flag map with one resolver; banned compile-time checks.
- **Principle:** A flag is config with one resolver. Every additional way to read it is a future inconsistency.

### 🟢 Deep-link route list rotted *(→ Lesson 6.4)*
- **Symptoms:** App deep links fell back to the website for screens the app had; one path *looped*: web fallback → OS App Link → re-enters the app → not-found → fallback again, forever.
- **Root cause:** Hand-maintained known-routes list diverged from the real router; group-qualified paths broke the fallback check; no loop detection.
- **Fix:** Handle qualified paths + a drift-guard test that fails when list and router disagree + loop detection with a terminal failure state.
- **Principle:** Two sources of truth always diverge — derive one or install a tripwire. When your own links can re-open your own app, fallback logic needs loop detection.

### ⚪ Universal links opened the app on Home — and the tests were green
- **Symptoms:** Tapping a real website link opened the app on the Home screen, not the linked content. The deep-link E2E suite passed.
- **Root cause:** Web paths are locale-prefixed + plural; app routes are locale-less + singular; real HTTPS links were never translated. The tests only exercised the custom `app://` scheme — a proxy input that skipped the broken path entirely.
- **Fix:** A single translation hook that rewrites every inbound link (cold + warm start) through one shared resolver.
- **Principle:** Two clients sharing a URL space need an explicit translation layer at the boundary. Tests that use a proxy input instead of the real one produce false green.

### ⚪ OAuth deep-link interception bricked the app
- **Symptoms:** Google sign-in returned to a permanently blank app — surviving restarts.
- **Root cause:** The deep-link resolver's scheme test required `://`, but the OAuth library redirects with a *single-slash* scheme URL; the resolver mangled it into a junk route, and persisted navigation state made the wreckage permanent. Latent for months until the native scheme registration finally let redirects reach the app.
- **Fix:** Auth-redirect URLs pass through untouched; cold-start handler skips navigation for them.
- **Principle:** Catch-all URL interceptors will eventually mangle a shape they didn't anticipate; let auth flows own their URLs. Persisted state can turn a transient bug into a brick.

### ⚪ Apple sign-in: right token, wrong audience, misleading error
- **Symptoms:** "Continue with Apple" failed with "Invalid email or password."
- **Root cause:** Server verified tokens against the *web* client ID; native iOS tokens carry the app bundle ID as audience. The client swallowed the server's error body, so a one-line config mismatch presented as a generic login failure.
- **Fix:** Accept both audiences; parse and surface real server error messages app-wide.
- **Principle:** OAuth audiences differ per platform — multi-client backends must accept all valid ones. Swallowed error messages turn config fixes into blind debugging sessions.

### ⚪ The sign-in button that silently didn't exist
- **Symptoms:** No "Continue with Google" button on mobile at all.
- **Root cause:** The button renders only if a client ID is present — and the IDs are build-time-embedded env vars that the shipped build was made without. Not OTA-fixable.
- **Principle:** Build-time-embedded config produces features that silently no-op. Know exactly which fixes are OTA-able and which need a store rebuild.

### 🟢 Force-update gate ordering *(→ Lesson 6.1)*
- **Design/near-miss:** Gate fires when app version < configured minimum. Setting the minimum before the store release is live bricks every user.
- **Principle:** Kill-switches need an ordering contract with the thing they depend on. Write the runbook before you need it.

### ⚪ No API versioning against un-force-updatable clients
- **Symptoms:** Audit: no versioned API contract, while the mobile app in users' hands can't be force-updated. The hand-mirrored legacy and v1 route tables had already drifted (~20 mounts) — a security middleware added to one prefix and missed on the other is a live auth gap.
- **Principle:** Any client you can't force-update makes your API a permanent public contract. Never hand-mirror route tables.

### ⚪ Back button lost the instance
- **Symptoms:** From a detail page, following a related link then pressing Back landed on a generic list, not the page you came from.
- **Root cause:** Sibling routes in the same navigator don't grow a poppable stack; the origin tracking encoded screen *type*, not *instance* — identity lost.
- **Fix:** Explicit `backTo` return path carrying the exact instance; pure, unit-tested resolver.
- **Principle:** Model return targets explicitly; type-level tracking loses identity.

### ⚪ Offline listeners systematically invisible
- **Symptoms:** Users who download and listen offline (subway, rural, airplane) never appeared in analytics — biasing rankings toward online-heavy regions and against the most loyal users.
- **Fix:** Local queue of offline events, batch-synced idempotently on reconnect to an endpoint that deliberately does *not* feed real-time counters.
- **Principle:** Connectivity-gated telemetry has systematic sampling bias. Capture-and-reconcile fixes it — but sync must be idempotent under retries and must not inflate live signals.

### ⚪ Push notifications "shipped" but never wired
- **Symptoms:** Android push silently didn't work; the merged code looked complete.
- **Root cause:** FCM was never configured — the PR was inert without external setup + a native rebuild.
- **Principle:** "Code merged" ≠ "capability exists." Verify from the user's side.

### ⚪ Onboarding flag dead-chain on fresh installs
- **Symptoms:** New installs missed starter content and startup autoplay entirely.
- **Root cause:** Features chained behind an onboarding-seen flag that the fresh-install path never set.
- **Principle:** Feature chains inherit the weakest gate; test the fresh-install path, not just upgrades.

## Testing, CI & Git Safety

### 🟢 The 600-file deletion *(→ Lesson 8.1)*
- **Symptoms:** A commit deleted 600+ files.
- **Root cause:** Branch created from the wrong base + broad `git add .` staged the divergence.
- **Fix:** Mandatory mechanical rules: verify base branch, never `git add .`, pre-commit hook blocks >30 files or >5000 deletions, verify after commit.
- **Principle:** At agent speed, safety rules must be mechanical (hooks), not behavioral (memory).

### 🟢 ~1,990 green tests that couldn't catch a data bug *(→ Lesson 8.2)*
- **Symptoms:** Audit: a broken query, missing index, or bad migration would pass every test and only break in production.
- **Root cause:** Most server suites mock the database models — assertions became tautological (mock returns X, assert X). Validation, unique constraints, cascades all bypassed. The mocking also coupled tests to call *order*, so adding one query broke unrelated suites.
- **Fix (prescribed):** Convert the highest-risk suites to a real in-memory database engine; one integration test per migration.
- **Principle:** Mocking the layer under test proves nothing about it. Data-layer correctness needs a real engine.

### 🟢 The E2E suite that couldn't fail the build *(→ Lesson 8.3)*
- **Symptoms:** Audit: ~30 journey specs existed but ran only on manual trigger with `continue-on-error: true` — a broken login could ship unnoticed.
- **Principle:** A test suite that can't fail the build is theater. Coverage counts only if it gates releases.

### 🟢 Preflight check that always failed *(→ Lesson 8.3)*
- **Symptoms:** CI preflight's lockfile check failed on every push; everyone learned to ignore it.
- **Root cause:** Check assumed the wrong package manager.
- **Principle:** A check that's known to false-alarm trains people to push through failures — worse than no check.

### 🟢 E2E false-failures from dev-server cold compiles *(→ Lesson 8.2)*
- **Symptoms:** Playwright flaked on first-visit timeouts.
- **Root cause:** Dev server cold-compiles routes on first hit; the timeout measured compilation, not the app.
- **Fix:** Global setup pre-warms routes before the suite runs.
- **Principle:** Flaky tests get ignored; make the suite trustworthy or it protects nothing.

### ⚪ The France bug: fixed on web, still broken on mobile
- **Symptoms:** The same prayer-times bug fixed on one client persisted on the other.
- **Root cause:** Business logic copy-pasted into each client instead of the shared package; the copies drifted.
- **Principle:** Cross-client duplicated logic guarantees divergent bugs; shared behavior lives in one shared module.

### ⚪ Local typecheck drift vs worktree
- **Symptoms:** `tsc` errors locally that CI didn't have (and vice versa).
- **Fix:** Typecheck inside the worktree with its own dependencies.
- **Principle:** Verification must run in the environment that ships.

## Observability & Background Jobs

### 🟢 "Returning users" measured logins, not returns *(→ Lesson 7.1)*
- **Symptoms:** Retention numbers didn't match observed reality.
- **Root cause:** Metric counted login events; listening happens without logins.
- **Fix:** Redefined returning = 2+ distinct listening days.
- **Principle:** Metrics must measure the user's reality, not the system's convenient events.

### 🟢 Zero-result searches as free user research *(→ Lesson 7.3)*
- **Symptoms:** Users searched and got nothing; nobody knew.
- **Fix:** Logged zero-result queries; shipped fuzzy + normalization fixes across all surfaces; dashboard tracks miss rate.
- **Principle:** Instrument discovery-feature failures — they're both bugs and roadmap.

### 🟢 Sentry noise floor: the top "error" was a success message *(→ Lesson 7.2)*
- **Symptoms:** The single largest error group (~1,200 events) was a diagnostic reporting the *healthy* state at Error severity; second was an already-handled fallback. Real crashes hid underneath.
- **Fix:** Report only failure states; capture a root cause once per session, not per call site.
- **Principle:** Severity must map to actionability. Logging healthy states as errors destroys the signal a tracker exists to provide.

### 🟢 Blind in production *(→ Lesson 7.2)*
- **Symptoms:** Audit: no server or web error tracking, no metrics, no alerting — a 3am failure would be discovered via user complaints.
- **Principle:** Without alerting, MTTR is bounded by how long users take to complain. Observability is a prerequisite for operating, not a nice-to-have.

### ⚪ Fire-and-forget scheduled jobs: no lock, no audit, no receipts
- **Symptoms:** Audit: scheduled push jobs could run twice (no claim lock), left no audit record, and never polled delivery receipts — duplicates and silent failures undetectable. Same pattern in newsletter (non-atomic dedup) and render jobs (no lease → stuck forever).
- **Fix (prescribed):** Per-job idempotency claim (SET NX EX), an audit row, receipt polling, leases + stale-job sweeps.
- **Principle:** Every background job needs three things: an idempotency lock, an audit trail, and reconciliation of what actually got delivered.

## Process & AI-Team Direction

### 🟢 Verification before completion *(→ Lesson 9.4)*
- **Pattern:** "Done" repeatedly declared from the wrong layer: the CDN-cached page, the unwired push, the TV build with localhost baked in, the OTA'd fix that was still reproducible on the CEO's device.
- **Rule:** No task is done without evidence from the layer the user touches — for bugs, reproduce-then-confirm on the exact surface reported.

### 🟢 Review-to-guardrail pipeline *(→ Lesson 9.3)*
- **Pattern:** Same review feedback recurring across agent PRs.
- **Rule:** Flagged twice → automate it (lint rule, drift-guard test, hook) → stop reviewing for it. The review surface should shrink over time.

### ⚪ Post-incident rules must live in agent-readable memory
- **Pattern:** Fixes and gotchas solved in one session were re-broken later when context was gone.
- **Rule:** Every hard-won rule lands in CLAUDE.md / project memory, phrased for a future agent with zero context ("never trim the flight-guard block").

### ⚪ Docs that contradict each other misdirect agents
- **Pattern:** Two project instruction files gave opposite testing rules ("no mocks, real DB" vs "mock the models"); a model comment claimed a TTL the code didn't have.
- **Principle:** For AI-directed development, stale docs aren't just annoying — they're instructions someone *will* follow. Doc drift is a defect class.
