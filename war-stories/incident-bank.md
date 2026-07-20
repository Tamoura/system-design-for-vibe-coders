# Incident Bank

Raw material for lessons. Every entry: symptoms → root cause → fix → principle.
Lessons cite these; new incidents land here first. Details are drawn from a real
production audio-streaming platform (web + iOS + Android + TV, global audience,
Cloudflare CDN, VPS origin, MongoDB/Redis/R2).

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

## Deployment & Infrastructure

### 🟢 Blue-green deploys that still 502'd *(→ Lesson 4.2)*
- **Symptoms:** 502s during "zero-downtime" deploys.
- **Root cause:** Both colors built into and served from the same `.next` build directory; bringing up the new color clobbered assets the live color was serving.
- **Fix:** Per-color build directories (`.next-blue` / `.next-green`), each color builds and serves its own. Proven with 0 dropped requests under live traffic.
- **Principle:** Two instances isn't isolation unless *everything* is duplicated — builds, dirs, ports, state.

### 🟢 nginx stale worker serving the dead color *(→ Lesson 4.3)*
- **Symptoms:** Flapping 502s after a blue-green flip; app logs clean.
- **Root cause:** An old nginx worker survived reload and kept routing to the decommissioned color's port.
- **Fix:** Full `systemctl restart nginx` after each color flip, encoded in the deploy script.
- **Principle:** Every intermediary has its own process lifecycle; "reloaded" and "restarted" are different guarantees.

### 🟢 Backup grew 244 MB → 871 MB overnight *(→ Lesson 2.3)*
- **Symptoms:** Nightly backup size tripled with no data growth.
- **Root cause:** tar excluded `.next` but the blue-green refactor created `.next-blue`/`.next-green` — each holding ~620 MB webpack caches that got archived nightly.
- **Fix:** Exclude patterns `.next-*` and `*/cache/webpack`; clarified backup scope = the two Mongo DBs + configs (code is redundant with GitHub).
- **Principle:** Back up state, not artifacts. Backup scripts rot when the directory layout evolves — audit contents, not just success exit codes.

### 🟢 Stale staging process running unnoticed for two months *(→ Lesson 7.2)*
- **Symptoms:** Discovered by accident: a staging server process from May still alive in July, serving old code.
- **Root cause:** Nothing audited what was actually running; deploys started new processes without guaranteeing old ones died.
- **Fix:** Process cleanup added; "what's running where" became a checkable runbook item.
- **Principle:** Audit the actual state of production, not your mental model of it.

### ⚪ Long-running VPS jobs killed by SSH hangups
- **Symptoms:** Multi-hour data imports died mid-run when the SSH session dropped.
- **Root cause:** Jobs tied to the interactive session; also sudo/nohup interaction subtleties.
- **Fix:** nohup + detached execution pattern for anything long-running on the VPS.
- **Principle:** Any job longer than minutes must not depend on your laptop's Wi-Fi.

## Data & Storage

### 🟢 Deleted files resurrecting from the old storage backend *(→ Lesson 2.2)*
- **Symptoms:** Files deleted from R2 object storage kept reappearing.
- **Root cause:** Migration GCS→R2 left Sippy (pull-through replication) enabled; every R2 miss re-fetched from GCS, restoring deletes.
- **Fix:** Delete from both backends; end the dual-source phase explicitly.
- **Principle:** A migration isn't done until the old system can no longer act. Dual-read/write phases need explicit end dates.

### 🟢 Schema keyed on the wrong identity *(→ Lesson 2.1)*
- **Symptoms:** A reciter with two recitation styles in the same narration — one style unrepresentable.
- **Root cause:** Recitations keyed by riwaya (narration) only; style existed in storage layout but not in the data model's identity.
- **Fix/mitigation:** Lived with one-style-per-riwaya constraint; workarounds at content layer.
- **Principle:** The keys you choose early are the constraints you live with longest. Model identity from the domain's edge cases, not its common case.

### ⚪ Env var reused across audiences: broken email links
- **Symptoms:** User-facing links in emails pointed to localhost in production.
- **Root cause:** Links built from `CLIENT_URL`, whose real job was CORS origin configuration; its value was correct for CORS, wrong for links.
- **Fix:** Separate `PUBLIC_SITE_URL` for user-facing URLs; rule: never build links from infra-purpose vars.
- **Principle:** Every env var has an audience. One var serving two audiences will eventually be wrong for one.

## Security, Abuse & Auth

### 🟢 Everyone shared one rate-limit bucket behind the CDN *(→ Lesson 5.2)*
- **Symptoms:** Legitimate users receiving 429s at modest traffic.
- **Root cause:** Limiter keyed on socket IP; behind Cloudflare all traffic arrives from CDN IPs. Also: in-memory counters reset per deploy and didn't share across instances.
- **Fix:** Key on `CF-Connecting-IP`; move counters to Redis; fail-open on store errors.
- **Principle:** Behind any proxy, "client IP" is an application-layer claim you must configure deliberately. Distributed limits need shared state.

### 🟢 Registration / email-bomb abuse *(→ Lesson 5.1)*
- **Symptoms:** Scripted signups triggering email floods to victim addresses.
- **Root cause:** Free unauthenticated endpoints (signup + email send) with no cost to the attacker.
- **Fix:** Turnstile CAPTCHA + per-IP limiter layered on signup.
- **Principle:** Every unauthenticated endpoint that triggers cost (email, SMS, storage) will be found by a script. Raise attacker cost above payoff.

### ⚪ Rotating refresh tokens with reuse detection
- **Design:** 180-day sliding refresh tokens; reuse of a rotated token burns the whole chain.
- **Principle:** Assume token theft; design the protocol so theft is detectable and bounded.

## Multi-Client (Web / Mobile / TV)

### 🟢 OTA update silently reverted *(→ Lesson 6.2)*
- **Symptoms:** A shipped mobile fix vanished days later.
- **Root cause:** OTA published from a feature branch; next OTA from main didn't contain it.
- **Fix:** Rule: never OTA a feature branch — merge to main first; main is the only publish source.
- **Principle:** Every publish channel needs exactly one source of truth.

### ⚪ OTA stripped runtime env config
- **Symptoms:** OTA'd app lost environment-dependent behavior.
- **Root cause:** `eas update` without `--environment production` stripped `EXPO_PUBLIC` build-env vars.
- **Fix:** Always pass the environment flag; documented in runbook.
- **Principle:** Update tooling has its own config model; verify what the artifact actually contains.

### 🟢 Feature flag checked two different ways *(→ Lesson 6.3)*
- **Symptoms:** Nav showed a feature whose route 404'd (or vice versa) depending on surface.
- **Root cause:** One surface read the flag at compile time, another at runtime — two sources of truth.
- **Fix:** Single runtime flag map (`useFeatureFlag()` / `resolveAllFeatureFlags()`); banned compile-time checks.
- **Principle:** A flag is config with one resolver. Every additional way to read it is a future inconsistency.

### 🟢 Deep-link route list rotted *(→ Lesson 6.4)*
- **Symptoms:** App deep links fell back to the website for screens the app actually had; one path looped back into the app.
- **Root cause:** Hand-maintained `KNOWN_ROUTES` list diverged from the real router as routes were added; group-qualified paths broke the fallback check.
- **Fix:** Fixed the checks + added a drift-guard test that fails when the list and router disagree.
- **Principle:** Two sources of truth always diverge — derive one from the other, or install a tripwire test.

### 🟢 Force-update gate ordering *(→ Lesson 6.1)*
- **Design/near-miss:** Gate fires when app version < configured minimum. Enabling the minimum before the store release is live bricks every user.
- **Principle:** Kill-switches need an ordering contract with the thing they depend on. Write the runbook before you need it.

### ⚪ Push notifications "shipped" but never wired
- **Symptoms:** Android push silently didn't work; code looked complete.
- **Root cause:** FCM was never actually configured — the PR was inert without Firebase setup + native rebuild.
- **Fix:** Explicit dependency checklist (Firebase project, EAS key, new native build) before calling it done.
- **Principle:** "Code merged" ≠ "capability exists." Verify from the user's side.

### ⚪ Onboarding flag dead-chain on fresh installs
- **Symptoms:** New installs missed starter content and startup autoplay entirely.
- **Root cause:** A chain of features all gated behind an onboarding-seen flag that was never set on the fresh-install path.
- **Principle:** Feature chains inherit the weakest gate; test the *fresh install* path, not just upgrades.

## Testing, CI & Git Safety

### 🟢 The 600-file deletion *(→ Lesson 8.1)*
- **Symptoms:** A commit deleted 600+ files.
- **Root cause:** Branch created from the wrong base + broad `git add .` staged the divergence.
- **Fix:** Mandatory rules + pre-commit hook: verify base branch, never `git add .`, block commits >30 files or >5000 deletions, verify after commit.
- **Principle:** At agent speed, safety rules must be mechanical (hooks), not behavioral (memory).

### 🟢 Preflight check that always failed *(→ Lesson 8.3)*
- **Symptoms:** CI preflight's lockfile check failed on every push; everyone learned to ignore it.
- **Root cause:** Check assumed pnpm; repo is npm-only.
- **Principle:** A check that's known to false-alarm trains people to push through failures — worse than no check.

### 🟢 E2E false-failures from dev-server cold compiles *(→ Lesson 8.2)*
- **Symptoms:** Playwright suite flaked locally on first-visit timeouts.
- **Root cause:** Next dev server cold-compiles routes on first hit; test timeout measured compilation, not the app.
- **Fix:** Global setup pre-warms routes before the suite runs.
- **Principle:** Flaky tests get ignored; spend the effort to make the suite trustworthy or it protects nothing.

### ⚪ Local typecheck drift vs worktree
- **Symptoms:** `tsc` errors locally that CI didn't have (and vice versa).
- **Root cause:** Typechecking outside the worktree/deps actually being built.
- **Fix:** Run typecheck inside the worktree with its own node_modules.
- **Principle:** Verification must run in the environment that ships.

## Observability & Product Telemetry

### 🟢 "Returning users" measured logins, not returns *(→ Lesson 7.1)*
- **Symptoms:** Retention numbers didn't match observed reality.
- **Root cause:** Metric counted login events; listening happens without logins.
- **Fix:** Redefined returning = 2+ distinct listening days.
- **Principle:** Metrics must measure the user's reality, not the system's convenient events.

### 🟢 Zero-result searches as free user research *(→ Lesson 7.3)*
- **Symptoms:** Users searched and got nothing; nobody knew.
- **Root cause:** No instrumentation on the failure path; Arabic text normalization gaps made valid queries miss.
- **Fix:** Logged zero-result queries; shipped fuzzy + holistic normalization across all surfaces; dashboard tracks the miss rate.
- **Principle:** Instrument discovery-feature failures — they're both bugs and roadmap.

### 🟢 Crash dashboard noise floor *(→ Lesson 7.2)*
- **Symptoms:** Error tracker dominated by three noisy, non-actionable mobile errors.
- **Principle:** Triage by actionability; an alert channel with known noise stops being read.

## Process & AI-Team Direction

### 🟢 Verification before completion *(→ Lesson 9.4)*
- **Pattern:** Repeated theme across incidents: "done" declared from the wrong layer (CDN-cached page, unwired push, unflipped flag).
- **Rule that emerged:** No task is done without evidence from the layer the user touches.

### 🟢 Review-to-guardrail pipeline *(→ Lesson 9.3)*
- **Pattern:** Same review feedback recurring across agent PRs.
- **Rule:** Flagged twice → automate it (lint rule, drift-guard test, hook) → stop reviewing for it. Review surface should shrink over time.

### ⚪ Post-incident rules must live in agent-readable memory
- **Pattern:** Fixes and gotchas solved in one chat session were re-broken later when context was gone.
- **Rule:** Every hard-won rule lands in CLAUDE.md / project memory files, phrased for a future agent with zero context.
