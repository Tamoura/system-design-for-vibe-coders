# A Practical Guide to Becoming an AI-Native Engineer — authoring guide

This is the contract every lesson follows. It is not published.

## What the course is

A free, bilingual (English/Arabic) course for **software engineers who can code** and want to work the way strong engineers now work: with AI coding agents as part of the daily loop, without giving up the engineering judgement that makes the work safe to ship. It goes from "what is an agent actually doing when it edits my repo" to "my team has an AI engineering playbook, my setup is hardened, my agents are automated and verified, and I know how to keep my own skills sharp". It is *practical*: every lab is a real task on one shared codebase, with an offline grader, so the learner leaves with working habits, not opinions.

Three promises to the learner:
1. **Habits, not hype.** The course teaches five habits (below) and the evidence for and against each. It says plainly what agents are good at, where they fail and when to take the wheel.
2. **Every lab is graded, offline, for free.** The learner works on **Najm Remit**, a small Python codebase, with their own agentic coding tool (the course uses **Claude Code** for examples; any tool works, or no tool). `python -m ailab grade …` runs hidden acceptance tests and checks on the result. No API key is needed by the kit.
3. **You stay accountable.** Whatever the agent writes, the engineer owns: they must be able to explain, verify and defend every line that ships. The course trains the verification and review skills that make that possible.

## The five habits (the spine; use these names exactly)

1. **Context first** — give the agent what it needs to know before you tell it what to do (project memory, conventions, the right files, the constraints).
2. **Specify before you delegate** — write down what "done" means (acceptance criteria, non-goals, constraints) and plan before code.
3. **Small verified steps** — work in short loops with checks after each (tests, diffs, commits); stop an agent early rather than late.
4. **Trust evidence, not fluency** — a confident, well-written answer is not evidence. Tests, reproduction, diffs, logs and sources are.
5. **Automate the loop, keep the skill** — turn repeated steps into commands, hooks and scripts; keep practising the fundamentals so you can still tell when the agent is wrong.

The learner-facing "AI-native loop" is **specify → delegate → verify → integrate**, with **context** feeding every step and **safety** wrapping all of it.

**Not** AI engineering: this course is about *how an engineer works with AI tools*. Building AI products (LLM applications, RAG, agents for customers) is the companion course *Building AI Applications & Agents*. Say this in lesson 0.1 and link it.

## Audience, tone and honesty

- **Audience:** software engineers and engineering students who can read and write basic Python and use git and a terminal; junior to mid-level; GCC bank, government and enterprise engineers; reading groups and teams. No prior experience with coding agents is assumed. Not for non-coders (see *System Design for Vibe Coders* for them).
- **Honest, not hype.** Never invent statistics, benchmark scores, prices, dates, quotes, URLs, version numbers or company policies. Studies and reports may be cited **only** from `/home/user/coursework/ai-evidence.md` (the verified evidence sheet), with the source's own caveats, and never with a number that is not marked VERIFIED there. Hedge anything that changes ("at the time of writing (2026)"). 'AI-native engineer' has no standard definition: say so, and say this is the course's working definition.
- **Tool-agnostic principles, Claude Code examples.** The habits survive tool changes. Use Claude Code for concrete commands and files, say "check the current documentation" for anything that moves, and mention that other tools (Cursor, GitHub Copilot agent mode, Codex CLI, Gemini CLI, Aider and others) have equivalents. No rankings, no benchmark claims, no tool bashing.
- **Reading-group edition.** Each module is about one week of part-time study: concept lesson, then a lab. Every lab lesson ends its 🏛️ section with the weekly **deliverable** (what to commit), a **group session** agenda and debrief questions.
- **Companion courses** (relative links; catalogue in `/home/user/coursework/LIBRARY.md`; link only to lessons listed there): *Building AI Applications & Agents* (aiapps: the agent loop, MCP, evals, guardrails; link rather than repeat), *Software Testing: Zero to Hero in the AI Era* (testing: 6.1 verifying AI-generated code, 6.2 tests as the spec for coding agents, 6.3 AI as testing assistant, 2.x unit testing), *Secure AI & Application Security* (secai: 6.3 securing AI-generated code, 8.x AI attacks, 9.2 agents/tools/MCP), *System Design for Vibe Coders* (vibe: the non-coder track, 9.5–9.8 Claude Code techniques), *Running AI Agents in Production* (agentic), *Cloud & DevOps* (cloud: CI/CD, secrets, SLOs), *From Graduate to Hired* (career: portfolio, skills), *AI Governance* (aigp) and *AI Product Management* (aipm: specs, evaluation).

## The running scenario: Najm Remit (use these facts consistently)

**Najm Bank** is the fictional mid-sized Gulf bank (Qatar, the UAE and the EU) used across the library; say it is fictional in lesson 0.1. The learner joins the **Payments Platform** team as a new engineer on a 14-week "AI-native onboarding" (one module a week, then the capstone). The team owns **Najm Remit**, the service that lets the bank's expatriate customers in Qatar send money home: quotes, fees, exchange rates, limits, sanctions screening, ledger postings and customer notifications in English and Arabic. The lab repository is a *small* version of it. All numbers are **fictional** and labelled as such wherever they appear.

- **Cast:** **Tariq**, engineering lead of Payments Platform (the reader's mentor; runs the weekly "AI-native clinic"); **Lujain**, graduate engineer (enthusiastic with AI tools; over-trusts them; makes the mistakes the reader should avoid); **Hessa**, product owner of Najm Remit (writes the tickets); **Nada**, quality engineering lead (verification, test strategy); **Noura**, application and AI security; **Maha**, SRE lead (incidents, on-call); **Layla**, head of AI governance; **Hamad**, CISO; **Sara**, data protection officer; **Salem**, platform engineering (CI, shared tooling, the approved-tools list).
- **Najm's AI-engineering rules (fictional):** only approved tools, run in approved environments; no Confidential or Restricted data and no secrets in prompts or agent contexts; AI-written code is reviewed like any other and **the author remains accountable**; agents run with least privilege and never touch production; changes to money logic need a second human reviewer; every AI-assisted change is labelled in the pull request.
- **Systems (fictional):** the Remit service (the lab repo), the internal helper library **najmkit** (vendored in the repo; an agent cannot know it from training: a recurring teaching point), the CI pipeline run by Salem, the ticket board run by Hessa.
- **The repo's facts** (modules, function names, seeded quirks, what is tested and what is not) are in `ainative/ailab/KIT_NOTES.md`, written by the kit builder. Read it before you write; never contradict it.

## The lab kit: `ainative/ailab/`

GitHub: https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/ainative/ailab. Python 3.11+, standard library plus `pytest` only (and `pyyaml` if you add it to `requirements.txt`). **No network, no API key, no agent is needed to run, start, grade or test any lab.**

```
ainative/ailab/
  README.md  KIT_NOTES.md  requirements.txt  pytest.ini
  ailab/                      # the package (python -m ailab ...)
    cli.py  framework.py  checks.py  gitutil.py  runner.py
    base/remit/               # the frozen base repo: src/remit/, najmkit/, tests/, docs/, README.md
    labs/mNN_slug/            # one folder per lab: lab.py, task.md, assets/, solution/
    stubs/claude              # a stand-in for the `claude` CLI used by the headless lab's grader
  tests/                      # test_framework.py, test_base.py, test_labs_mNN.py (one per lab)
  check_blocks.py             # lesson code blocks that name a kit file must equal it
```

**Commands** (the learner uses these; lessons show them exactly):
- `python -m ailab list` — the labs, their lesson numbers and whether they need an agent.
- `python -m ailab doctor` — checks Python, git, pytest and a writable directory.
- `python -m ailab start m04 --dir ~/ainative/m04` — copies the base repo, `git init`s it, commits "Initial state", applies the lab's seed (a second commit, "Lab starting state", tagged `lab-start`), copies `assets/` into `lab-assets/`, writes `TASK.md` and prints the task.
- `python -m ailab grade m04 --dir ~/ainative/m04 [--json]` — runs the lab's checks, prints one line per check (PASS/FAIL, with a hint, never the hidden answer), exits non-zero unless every required check passes.
- `python -m ailab solve m04 --dir ~/ainative/m04` — applies the reference solution (used by the kit's own tests; the lessons tell learners it is a peek and to try first).

**Lab contract** (`ailab/labs/mNN_slug/lab.py` defines `LAB = Lab(...)` from `ailab/framework.py`): `id`, `title`, `lesson`, `needs_agent`, `seed(work)`, `grade(work) -> list[Check]`, `solve(work)`; `task.md` is the ticket/brief shown to the learner and quoted in the lesson. Rules:
1. **The starter state must fail the grader and the reference solution must pass it** (the generic test in `tests/` enforces this for every lab). Add **negative tests** for the typical wrong answers a learner or an agent will produce (for example: special-casing the test, rounding with floats, forgetting the Arabic message, touching unrelated files). A grader must accept *any* sound solution, so test behaviour through the public interfaces the task names, not through your own implementation.
2. Hidden tests live inside the kit (not in the learner's work directory) and are run against the learner's work directory in a subprocess with a timeout; never `exec` learner code in-process.
3. A check has a short `name`, `ok`, a `detail` the learner can act on and an optional `hint`. Mark checks `required` or advisory.
4. Seeds modify the base repo only through `seed()` (patches, new files, a branch); **never edit `ailab/base/remit/`** after the kit builder has finished (if a base change is needed, say so in your report).
5. Everything is deterministic and offline. No sleeping, no network, no clock dependence (inject time). A lab runs in under about 20 seconds.
6. Lab assets that are *illustrative* (for example agent transcripts) must say, in the file and in the lesson, that they are **constructed for teaching, not recorded from a real model**.
7. Every lab lesson says **"Needs an agent: yes/no"**; when yes it also gives the **no-agent path** (do the task by hand or with a chat assistant; the grader does not care how the work was produced).
8. **Lesson code blocks that show a kit file.** A Python, shell, YAML or TOML block that shows a kit file (a starter template the learner will edit, a hook skeleton) starts with a first-line comment naming the file's path relative to `ainative/ailab/` (for example `# ailab/labs/m08_harden/assets/guard_skeleton.py`) and must be byte-identical to that file; `check_blocks.py` enforces this. Formats without comments (JSON, Markdown) are introduced by a sentence naming the path and are not byte-checked, but must still be valid and match the file. **Never show reference solutions or hidden tests in a lesson.**
9. Tests for your lab: `ainative/ailab/tests/test_labs_mNN.py`; run `cd ainative/ailab && /home/user/coursework/venv/bin/pytest -q` (the same venv as the testing course: Python 3.11 with pytest). All kit tests must pass.
10. **Learner dry-run** (a later stage, by an independent agent): it will `start` your lab, follow only the lesson text and the task, do the work as a learner would, and run `grade`. Write the task and the lesson so that this works without insider knowledge; ambiguous tasks will be sent back.

## The lab plan (one lab per module; ids fixed)

| Lab | Lesson | What the learner does | What the grader checks (hidden) |
|---|---|---|---|
| m00 | 0.2 | `doctor`, then fix a one-word typo in an English notification with their agent (or by hand), run the tests, commit | doctor passes; tests pass; the diff is tiny; the commit message follows the convention in the repo's `CONTRIBUTING.md`; no unrelated files |
| m01 | 1.2 | Read three **constructed** agent sessions in `lab-assets/sessions/` and fill `diagnosis.json`: failure mode (from a fixed list), the turn where it went wrong, the cheapest prevention. Optional second part: run their own session and fill `session-notes.md` | JSON schema; failure modes and turns match the seeded ones (±1 turn); prevention is one of the allowed categories; notes file structure |
| m02 | 2.2 | Write the project memory file (`CLAUDE.md`, or `AGENTS.md`) for the repo; run the same small task with and without it and fill `ab-notes.md` | memory lint: size band, exact working commands (they are executed), conventions that match the repo (Decimal money, test layout), a short "never do" list, architecture pointers that resolve to real files, no secrets, no filler; notes structure |
| m03 | 3.2 | Turn three vague tickets into specs and plans (`specs/T1.md` … `T3.md`) | each spec has the required sections; acceptance criteria are checkable; files named exist; **each ticket hides ambiguities (rounding, tier boundary, currency, Arabic) and the spec must resolve them**; plan steps are small |
| m04 | 4.2 | Ship the "80% of daily limit" customer warning (English and Arabic) with spec, plan, small commits and tests | hidden acceptance tests; existing tests still pass; the learner's new tests would catch the feature being removed (mutation-style); diff size and files in scope; commit messages; no secrets |
| m05 | 5.2 | Review the branch `agent/loyalty-discount` (an agent's pull request seeded with flaws) and write `review.md`; then fix the branch | findings matched to the seeded flaw ids (hallucinated dependency, swallowed exception, float money, a test that asserts nothing, an over-mocked test, a hard-coded key, scope creep with a deleted test); fixed branch passes hidden tests and static checks |
| m06 | 6.2 | Onboard to the codebase with an agent (write `docs/onboarding.md`), then fix a production bug from `lab-assets/prod.log` (a limit applied at the wrong midnight) with a regression test and a root-cause note | hidden boundary tests; the regression test fails on the starter and passes on the fix; the note names the root cause; the patch is minimal |
| m07 | 7.2 | Add characterization tests to the untested `ledger` module (quirks included), refactor away its global state, then migrate `najmkit` from v1 to v2 | hidden characterization suite passes on the refactor (quirks preserved); the learner's tests kill a set of seeded mutants; no module-level mutable state; migration complete; old API gone |
| m08 | 8.2 | Harden the setup: permission rules, a guard hook script, a dependency check, and notes on an injected README | the hook is run against about twenty hook-input JSON documents (block the dangerous, allow the harmless, exit codes as the documentation says); the dependency check flags unknown packages; settings parse and contain the required denies; notes structure |
| m09 | 9.2 | Build a project toolkit: a review command or skill, a read-only reviewer subagent, a post-edit hook, and a headless triage script | file formats and frontmatter valid; hooks behave on sample inputs; the headless script is run against the kit's `claude` stub and must parse its JSON, handle errors and respect limits |
| m10 | 10.2 | Split a four-part change across branches or worktrees (agents or by hand), integrate, resolve a planted conflict | merged `main` passes hidden tests; at least three feature branches merged; the planted conflict resolved correctly; history is readable |
| m11 | 11.2 | Write an ADR with an AI critic, docs for `najmkit` generated and **verified against the code**, and a postmortem from an incident record | ADR format; every function/signature claimed in the docs exists; every fact in the postmortem timeline matches `incident.json`; no invented facts |
| m12 | 12.2 | Write the team's AI engineering playbook (`playbook.md`) | required sections; at least three delivery metrics plus a guard metric with definitions; policy rules testable; review norms concrete |
| m13 | 13.2 | Build a personal tool/model eval (`eval/tasks.jsonl`, at least eight tasks with checks) and a 90-day plan | JSON lines valid; each task has a runnable check; plan has measurable goals |
| m14 | 14.1 | Capstone: add a new corridor (a Bangladesh BDT corridor with its own fee tier and limits) through the full cycle | hidden acceptance tests; the artefacts exist and cross-refer (memory, spec, plan, ADR, tests, review notes, hardened settings, docs, agent log, retrospective); commit hygiene; security checks pass |

### Decisions on the kit's open questions (final; they override KIT_NOTES section 9 wherever they differ)

1. **Doc name collision (m06):** the learner writes `docs/onboarding.md`, never `docs/tour.md` (the base ships `docs/TOUR.md`; case-insensitive file systems would collide).
2. **m06 and the four boundary tests:** the seed that plants the UTC bug **deletes** the four `tests/test_limits.py` tests that would expose it (as if they had never been written), so the starter suite is green and the bug is a real mystery; the hidden tests restore the boundary checks. The grader and the lesson must say plainly that the learner should add their own regression test.
3. **m07 interface:** the post-refactor shape is `class Ledger` (instance state only) with `post_transfer`, `balance`, `accounts`, `journal`, and `RemitService(..., ledger=None)` defaulting to a fresh `Ledger()`; the base `tests/conftest.py` stops calling `ledger.reset()`. The lab must state this interface exactly in `task.md`, and the learner's characterization tests must be writable before the refactor and still runnable after it (design a small adapter or fixture the task tells them to use, and test the idea with a negative case where a refactor changes a quirk).
4. **m09 stub:** the m09 writer builds `ailab/ailab/stubs/claude`, a deterministic stand-in for the `claude` CLI's `-p` and `--output-format json` behaviour, shaped exactly as `/home/user/coursework/claude-code-facts.md` section 6 documents; lesson and README say it is a stand-in.
5. **m11:** the seed deletes `docs/najmkit.md` ("lost in a migration") so the learner regenerates it from the code; the grader checks every claim against the code with `checks.public_api`.
6. **m14 limits:** "limits" in the capstone ticket mean the corridor's per-transfer `min_send` and `max_send`; the KYC-tier daily and monthly limits apply unchanged. The ticket must state the BDT rate, margin, fee tier, min and max explicitly (hidden tests cannot guess them).
7. **m02:** any command the grader executes sets `PYTHONPATH=src` (or the lesson tells the learner to `pip install -e .`).
8. **Commit convention:** keep the kit's stricter rule exactly as CONTRIBUTING.md and `checks.conventional_commits` define it (`type(scope): subject`, fixed types, lower-case scope, header up to 72 characters, no trailing full stop); lessons must teach that exact rule.
9. **`TASK.md` and `lab-assets/` are committed** in the "Lab starting state" commit (keep). **`hidden/` is readable** by a learner who looks: say once, in lesson 0.2, that the grader is a practice partner, not a gate, and that peeking defeats the point.
10. **Paths:** the package folder is `ainative/ailab/ailab/`; lesson path comments written as `# ailab/labs/...` mean `ainative/ailab/ailab/labs/...` (relative to `ainative/ailab/`).

## Claude Code and agent-tool facts

Read `/home/user/coursework/claude-code-facts.md` (verified against the current official documentation by a research pass) before you write anything about Claude Code. It is the authority for file names, flags, hook events and exit codes, permission syntax, subagent and skill formats, headless mode and the GitHub integration. Where it says UNVERIFIED or "changing", hedge ("check the current Claude Code documentation"). Never invent a flag, event or path. The **method** is the lesson (specify, plan, small steps, verify, review, commit); the product is the example. Other tools are named neutrally.

## Evidence and engineering facts to get right

State only what you are confident is true; hedge anything that changes; never invent.
- **Evidence:** `/home/user/coursework/ai-evidence.md` lists the studies and reports you may cite (METR randomized trial, DORA reports, vendor studies, package-hallucination research, security studies, prompt-injection disclosures, OWASP guidance) with exact titles, years, headline findings, caveats and links, flagged VERIFIED or UNVERIFIED. Describe findings as the source states them, with its caveats ("one randomized trial of experienced open-source developers found…"); never turn a study into a universal rule; say that results depend on task, tool and experience. If something is UNVERIFIED, do not cite it.
- **How agents work (Module 1):** a model is a stateless function of its context; the context window is finite and fills with the conversation, file contents, tool output and instructions; an agent is a loop of model calls and tool calls; failures: hallucinated APIs and packages, stale knowledge, misreading requirements, fixing symptoms, sycophancy (agreeing with a wrong premise), context rot in long sessions, runaway loops, "passing" by weakening the test. Link the companion course for the loop internals.
- **Verification (Module 5):** tests as the specification; test-first with an agent; the ways AI code passes while wrong (asserts nothing, mocks the thing under test, special-cases the example, swallows exceptions, changes the test); reading diffs for scope and for the five risk classes (correctness, security, scope, maintainability, hidden coupling); property-based tests and mutation testing as judges (point to the testing course rather than re-teach).
- **Security (Module 8):** prompt injection (direct and through files, issues, web pages, MCP tool descriptions), the "lethal trifecta" (private data + untrusted content + a way to send data out — Simon Willison's framing, presented as one practitioner's idea), excessive agency, secrets, destructive commands, hallucinated package names ("slopsquatting"), supply-chain hygiene (lockfiles, allow-lists, hashes), licence and IP questions, data privacy, sandboxing and least privilege, branch protection, human review of money logic. Point to *Secure AI* rather than re-teach.
- **Legacy and change (Module 7):** characterization tests (Michael Feathers), seams, the strangler fig (Martin Fowler), small safe steps, expand-contract migrations, codemods; when an agent is good at mechanical change and when it is dangerous.
- **Teams (Module 12):** DORA's delivery metrics (lead time, deployment frequency, change failure rate, time to restore; use the official definitions), why lines-of-code and acceptance-rate are poor targets, guard metrics, review norms for AI-assisted pull requests, onboarding juniors with and without AI, policy basics, cost awareness. Hedge every claim about productivity.
- **Skills (Module 13):** deskilling risk (hedge: evidence is still early), deliberate practice, using AI as a tutor without outsourcing the thinking, evaluating tools and models with your own tasks rather than leaderboards, staying current without chasing every release.

## Focus (the lesson tag)

Every lesson is tagged with one or two focus areas, in English, in both languages, chosen only from: **Mindset · Context · Workflow · Verify · Secure · Automate · Team**. Header: `*Focus: Verify*` or `*Focus: Workflow, Verify*`. (The tag is called Focus, not Skill, so it is never confused with Claude Code's *skills* feature.)

## Module and lesson plan (numbers are fixed)

| Module | File | Lessons (suggested focus tag) |
|---|---|---|
| 0 Orientation: becoming AI-native | 00-orientation.md | 0.1 What an AI-native engineer is (and is not): the shift, five habits and the evidence (Mindset) · 0.2 Your setup: tools, safe configuration, the Najm Remit repo and the ailab kit (Workflow, Secure) · 0.3 The AI-native loop: specify, delegate, verify, integrate, and who stays accountable (Mindset, Workflow) |
| 1 How coding agents work | 01-agents.md | 1.1 The mental model: context, tools and the loop, and why agents are brilliant and why they fail (Mindset) · 1.2 Lab: read three agent sessions, name the failure, then run your own (Mindset, Verify) |
| 2 Context engineering | 02-context.md | 2.1 What the agent sees: the context budget, project memory, rules, references, compaction and subagents (Context) · 2.2 Lab: write the project memory for Najm Remit and measure what it changes (Context) |
| 3 Specifying the work | 03-specs.md | 3.1 Spec-driven development: from ticket to acceptance criteria, constraints, non-goals and a plan (Workflow) · 3.2 Lab: turn three vague tickets into specs an agent can build from (Workflow) |
| 4 The daily loop | 04-loop.md | 4.1 Explore, plan, implement, check, commit: small steps, checkpoints and when to take the wheel (Workflow) · 4.2 Lab: ship a small feature through the whole loop (Workflow) |
| 5 Verification | 05-verify.md | 5.1 Trust evidence, not fluency: tests as the spec, reading diffs and the ways AI code passes while being wrong (Verify) · 5.2 Lab: review a pull request an agent wrote (Verify) |
| 6 Debugging and understanding code | 06-debug.md | 6.1 Understanding unfamiliar code and debugging with an agent: reproduce first, hypotheses, root cause (Workflow) · 6.2 Lab: onboard to the codebase and fix a production bug from its logs (Workflow, Verify) |
| 7 Legacy, refactoring and migration | 07-legacy.md | 7.1 Changing code you do not understand: characterization tests, seams, incremental refactors and agent-sized migrations (Workflow, Verify) · 7.2 Lab: tame an untested module, refactor it, then migrate a dependency (Workflow, Verify) |
| 8 Safety and security | 08-security.md | 8.1 When an agent has your keyboard: injection, secrets, destructive commands, hallucinated packages, permissions and sandboxes (Secure) · 8.2 Lab: harden your setup with permissions, a guard hook and a dependency check (Secure, Automate) |
| 9 Automating your agent | 09-automate.md | 9.1 Commands, skills, subagents, hooks, MCP and headless mode: what to automate and what not to (Automate) · 9.2 Lab: build a project toolkit and a headless triage script (Automate) |
| 10 Parallel and multi-agent work | 10-parallel.md | 10.1 Working with several agents: worktrees, delegation, the review bottleneck and cost (Workflow, Automate) · 10.2 Lab: split a change across agents and integrate it (Workflow) |
| 11 AI across the lifecycle | 11-lifecycle.md | 11.1 Beyond writing code: requirements, design critique, docs, review, incidents and learning (Workflow) · 11.2 Lab: an ADR with a critic, docs checked against code and a postmortem that sticks to the facts (Workflow, Verify) |
| 12 AI-native teams | 12-teams.md | 12.1 Team practice: conventions, review norms, ownership, juniors, metrics and policy (Team) · 12.2 Workshop: write your team's AI engineering playbook (Team) |
| 13 Staying sharp | 13-sharp.md | 13.1 Skills that compound: fundamentals, taste, deliberate practice, evaluating tools and avoiding deskilling (Mindset) · 13.2 Workshop: your personal eval, learning plan and 90-day plan (Mindset, Team) |
| 14 Hero: capstone and practice exam | 14-capstone.md | 14.1 Capstone: take a change to Najm Remit through the full AI-native cycle (Workflow, Verify, Secure) · 14.2 Practice exam: 60 scenario questions (all seven focus tags) |

Levels: 🟢 Beginner for Modules 0–3, 🟡 Intermediate for Modules 4–9 and 11, 🔴 Advanced for Modules 10, 12, 13 and 14 (use judgement per lesson).
**Odd-numbered lessons (N.1) are concept lessons; N.2 lessons are labs or workshops.** (0.2 is a setup lab with lab m00; 0.3 is a concept lesson.) In every lab lesson the 🏛️ section carries, in this order: **The ticket** (the kit's `task.md` in a `text` block, as Hessa wrote it), **Start** (the `ailab start` command), **Your move** (what to do and how an agent helps; the no-agent path), **What the grader checks** (the categories, not the hidden answers), **Grade** (the command and a sample output block tagged `text`), the weekly **deliverable**, the **group session** agenda, **debrief questions** (what did the agent get wrong? what did your context or spec miss?) and an **agent log** template (a few lines: prompt, what it did, what you corrected, time spent) that builds the reflection habit. In every concept lesson the 🏛️ section produces a reusable artefact (a memory template, a spec template, a review checklist, a hook skeleton, a playbook outline…). Concept lessons' 📚 References also carry a short "Go deeper" list from the evidence sheet and the official documentation (no quotes).

## Code and file snippets (they will be checked)

- Python 3.11+ and the repo's own conventions. Show imports. Comment liberally where code is the lesson. Where a snippet is *meant* to be wrong, say so in a comment and show the output separately.
- Configuration shown to the learner (`CLAUDE.md`, `settings.json`, hook scripts, subagent and skill files, GitHub workflow YAML) must be **valid** (JSON and YAML are parsed by a verifier; hook scripts are run against sample input) and consistent with the Claude Code fact sheet.
- Shell commands: real, current flags only. Fenced blocks have a language tag (`python`, `bash`, `json`, `yaml`, `text`, `markdown`, `toml`). Output blocks are `text`.
- Never in lessons: real secrets, real customer data, instructions to attack systems you do not own, destructive commands presented as safe.

## File format (the build parses this — follow exactly)

```
# Module 3 — Specifying the work

*One-paragraph italic module intro: what the module covers and why, tied to Najm Remit.*

> **Focus:** Workflow — …(one line in the course's words)

---

# 3.1 — Spec-driven development: from ticket to acceptance criteria, constraints, non-goals and a plan
*Level: 🟢 Beginner* · *Prerequisites: 2.1* · *Focus: Workflow*

## ⚡ In 60 seconds
- 4–6 bullets: what it is, the rule that matters most, the decision cue, the biggest trap.

## 🧭 Why it matters
A Najm Remit scenario (or a well-documented public failure) that makes the topic unavoidable. 1–3 paragraphs.

## 📐 How it works
### 🟢 The essentials
### 🟡 Going deeper
### 🔴 Expert view
(Plain explanations first; define every term on first use; worked examples with real text the reader can copy; weak-versus-strong contrasts; trade-offs and "when NOT to do this"; short correct snippets in fenced blocks; tables; one mermaid diagram where it genuinely helps. Mermaid: flowchart or sequence only, `flowchart LR` or `TD`, short labels in double quotes, no parentheses inside labels.)

## 🧰 The toolkit
| Tool, practice or pattern | What it is and does | When to reach for it |
|---|---|---|
| **Spec template** | … | … |
(3–8 rows. The first cell MUST start with the name in bold, e.g. **Project memory**, **Plan mode**, **Characterization test**, **Guard hook**, **Worktree**, **ADR**; optionally followed by a short credit in parentheses. Keep bold names identical wherever the same item appears; they build the toolkit catalogue.)

## 🏛️ In practice at Najm Bank
The artefact this lesson produces and, in lab lessons, the sequence described under the plan table.

## 🛠️ Exercises
Three graded exercises: 🟢 …, 🟡 …, 🔴 …, each with a "*Done when:*" line. Say for each whether it needs an agent.

## ⚠️ Mistakes and traps
4–6 bullets: the trap, then what to do instead.

## 🧾 Recap
4–6 bullets.

## ✍️ Check yourself
Five multiple-choice questions (at least three scenario-based). Format:

**1. Question text?**

- A. …
- B. …
- C. …
- D. …

<details><summary>Answer</summary>

**B.** Why B is right, and why the tempting distractor is wrong. (Pointer to the section.)

</details>

## 📚 References
Official documentation and primary sources only (code.claude.com/docs, docs.anthropic.com, anthropic.com/engineering, github.com/anthropics, agents.md, modelcontextprotocol.io, owasp.org / genai.owasp.org, dora.dev, sre.google, martinfowler.com, git-scm.com, docs.python.org, docs.pytest.org, conventionalcommits.org, and the sources in the evidence sheet). Plain links; if unsure of a deep link, link the top-level page.
```

- Separate lessons with a `---` line.
- Lesson 14.2 (practice exam) follows the same outer format but its body is: ⚡ (how to take it), 🧭, 📐 (three ### subsections), 🧰, 🏛️, 🛠️, ⚠️, 🧾, then `## ✍️ Practice exam` followed by a blank line and the single line `@@EXAM@@` (a later step fills 60 questions numbered 1–60 in the same Q/A format, mixed across all fifteen modules, each answer ending with its focus tag and the lesson to review, e.g. *(Verify · 5.2)*), then 📚. Do not write the questions; do not add a ✍️ Check yourself section to 14.2. `en_check.py` is told 14.2 is the exam lesson.

## Quiz quality rules (every ✍️ block and the exam)

- Exactly one clearly correct option, defensible from the lesson; three distractors that are plausible mistakes practitioners really make. No "all/none of the above", no "Which is NOT".
- **The correct option must not be systematically the longest or the shortest.** Options of similar length and grammatical form; the correct one must not be the only hedged or qualified option. Across a lesson's five questions it may be the longest in at most two and the shortest in at most two (exam: each at most about a quarter).
- Spread the correct letters across A–D (no letter more than twice in a lesson's five; exam: roughly 15 each).
- Test judgement and application in scenarios, not trivia or wording recall.

## Style

- Plain, direct English; short sentences; define jargon on first use; no hype, no filler. Explain *why*, not just *what*. Teach with worked examples: show the weak ticket and the strong one, the vague prompt and the specified one, the risky diff and the reviewed one.
- Lengths: 2,000–3,500 words per lesson (14.2 excepted), code and tables included. Every lesson's five questions must be answerable from that lesson.
- Use the running cast and the Najm Remit canon consistently. Do not start any non-quiz line with `**N.` (bold number + dot).
- Cross-course references: the reader auto-links any bare "lesson N.M", "lessons N.M", "see N.M", "(N.M" to a lesson of THIS course, so another course's lesson number may only appear inside a markdown link's text, e.g. `[*Software Testing*, lesson 6.2 — Tests as the specification for coding agents](../testing/index.html#/6.2)`.
