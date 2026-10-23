# Module 14 — Hero: capstone and practice exam

*The last week of the course has no new idea in it: it asks you to use all of them at once. Lesson 14.1 is the capstone. Hessa's ticket REMIT-414 opens a Bangladesh (BDT) corridor in Najm Remit, with a fee schedule, a rate, limits per transfer and customer wording of its own. You take that one change through the whole AI-native cycle (context, spec and plan, small verified steps, review, a security baseline, automation, documents and a retrospective) and leave the evidence in the repository, where Hessa, Tariq, Noura and Nada can check it. Lesson 14.2 is a 60-question practice exam across all fifteen modules, with a way to turn your misses into a study plan.*

> **Focus:** Workflow, Verify, Secure — all five habits in one change you can defend, then the whole course in 60 scenario questions.

---

# 14.1 — Capstone: take a change to Najm Remit through the full AI-native cycle
*Level: 🔴 Advanced* · *Prerequisites: Modules 0-13* · *Focus: Workflow, Verify, Secure*

## ⚡ In 60 seconds
- **One ticket, the whole cycle.** REMIT-414 opens a Bangladesh corridor: five small code edits, graded with the evidence around them.
- **Ten pieces of evidence** (memory, spec, plan, ADR, tests, review, settings and hook, docs, agent log, retrospective) must agree with the code and each other.
- **Judgement, not volume.** Some results land exactly on a rounding tie. Half-even or float rounding can be a cent wrong, and no summary says so.
- **Needs an agent: no, but recommended.** The grader sees the result, never the author; only the demo tests understanding.

## 🧭 Why it matters
Hessa's ticket has every number. Lujain finishes in an hour: one prompt, a corridor borrowing `STD-B`, tests written after the code, all green. Tariq asks four questions. Where is the spec? What fails if the maximum is 12,000.01? Who has read the `service.py` diff, a money file? What stops the agent opening `.env`? Lujain has no answer. The change may be fine; nobody can know.

The capstone trains the habit behind those questions: a change others can trust without your word. The 2025 DORA report (nearly 5,000 technology professionals, self-reported, associations not causes) frames AI as an amplifier of what a team already does; that specs, tests, small batches and review are what to amplify is the course's bet, not DORA's finding.

## 📐 How it works

### 🟢 The essentials
**The brief.** Eight milestones: context (modules 0-2), spec and plan (3), small steps (4, 5), review (5, 6), security (8), automation (9, 10), documents (11) and retrospective (12, 13). Each leaves something checkable that must refer to something real: files, ids `AC1`..., sample commands, the code, a commit. `lab-assets/README.md` lists what the grader reads in each document; read it before you write them.

**Providers before the consumer.** A corridor names its fee schedule, and an old test (`tests/test_corridors.py`) checks that the schedule exists. So the plan adds `STD-C` in `fees.py`, then the rate and margin in `fx.py`, then the corridor, then the wording (`notify.py`) and the template choice (`service.py`). No code commit turns an old test red. Fee and rate functions take a `Corridor`, so build one in your fee tests that points at `STD-C`; they can then pass before the real corridor exists.

**Work the money out by hand.** Remit rounds half up, in `Decimal`. A fee, a rate or a receive amount can land exactly on a tie, which half-even rounding, `round()` or a float resolves the other way. The base repo pins two:

```text
150.25 on QAR-INR:   150.25 x 2.00% + 2.00 = 5.005    half up 5.01      (half-even or float: 5.00)
55 QAR, test rate:   55 x 19.8990 = 1094.4450         half up 1094.45   (half-even: 1094.44)
```

A tie catches a wrong rounding only when the two rules disagree, which is when the digit before the 5 is even (5.005 gives 5.01 or 5.00; 5.015 gives 5.02 either way). `STD-C`, its rate and its receive amounts have such ties; find them before any test exists. This script scans one tier (some tiers have none), so keep it outside the repository:

```python
# ~/scratch/find_ties.py: a throwaway script, kept outside the repository
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal as D


def useful_tie(value, places=2):  # exactly halfway, and half up and half even disagree
    unit = D(1).scaleb(-places)
    return value / unit % 1 == D("0.5") and value.quantize(unit, ROUND_HALF_UP) != value.quantize(unit, ROUND_HALF_EVEN)


def fee(amount, percent, flat, minimum, cap):  # one tier; put the STD-C tier you test here
    return min(max(amount * D(percent) / 100 + D(flat), D(minimum)), D(cap))


amount = D("100")
while amount <= D("151"):  # amounts on a 0.25 grid
    if useful_tie(fee(amount, "2.00", "2.00", "5.00", "150.00")):  # STD-A, first tier
        print(amount, "->", fee(amount, "2.00", "2.00", "5.00", "150.00"))  # 150.25 -> 5.0050
    amount += D("0.25")
```

Try the rate (`useful_tie(mid * (1 - margin), 4)`) and the receive amount (send times rate) the same way. An agent may draft the tests; the expected values come from you.

### 🟡 Going deeper
**Delegate the draft, keep the decision.** The agent interviews you for the spec, drafts tests from your values and takes one plan step per prompt. A fresh-context reviewer (the **Second-model review** of lesson 5.1: a second session or `/code-review`) adds questions. Verify each: the best-practices page warns that reviewers usually report something even when the work is sound. The vague prompt is "Add a Bangladesh corridor to Remit". The specified one, for step 2, is a task contract (lesson 10.1; your AC ids will differ).

```text
Do step 2 of specs/REMIT-414-plan.md; read the plan, the spec and CLAUDE.md first.
Add the fee schedule STD-C to src/remit/fees.py and register it in SCHEDULES, from the spec's table.
May change: src/remit/fees.py. Must not change: any other file, any existing test.
Money is Decimal; ties round half up. If spec and ticket disagree, stop and ask.
Done when the fee tests (AC3, AC4) pass and nothing else moves.
Then commit: feat(fees): add the STD-C fee schedule for Bangladesh
```

**A right diff and the finding it still earned.** Say the agent's `service.py` change passes every test. Read the end of `send`: the template is chosen by name, notification comes last and `_notify` catches only `NotificationError`. A mistyped id raises `UnknownTemplate` after the ledger has posted and the transfer is stored. The review rates it minor and asks for one test: every template id the service can choose exists in `notify.TEMPLATES`, in both languages.

### 🔴 Expert view
**When the ticket's account of today's Remit and the code disagree,** the code wins and the ticket gets a question. **When the agent offers a neighbouring fix** (the stale `risk.py` and daily-limit text of the architecture page), decline it and log it as a follow-up with an owner. The same goes for a product question you notice, such as who can ever send the 12,000 maximum under the T1 and T2 daily limits: it belongs in your spec's open questions. **Do not delegate** the approved wording or the expected values.

**How much evidence is enough?** Match it to risk. A typo needs one commit and the test that was red; money logic gets all ten pieces and a second human on `fees.py`, `fx.py` and `service.py`. The capstone is maximal so that you feel each piece once.

**What the grader cannot tell.** A model could fill every template in ten minutes and pass: the checks verify shape, truth and references, never sincerity. So the demo has you break your own code live. Alone, or inside one agent session, you cannot start a second reviewer or hold the demo: say "self-review" in your notes and list your questions for the humans.

## 🧰 The toolkit
| Tool, practice or pattern | What it is and does | When to reach for it |
|---|---|---|
| **Capstone brief** | Eight milestones, ten artefacts and what each refers to | At the start; before every `ailab grade` |
| **Traceability ids** | `AC1`...: one id per criterion, in spec, plan and a test | Any change with a provable "done" |
| **Rubric** | Five dimensions, four levels each | To score yourself and each other |
| **Retrospective template** | Six sections citing minutes, commits, habits | After any ticket worth remembering |

## 🏛️ In practice at Najm Bank
*Needs an agent: no, but recommended: the capstone is about working with one. No-agent path: write every document and test yourself, in the same order.*

**The ticket.** This is `TASK.md` in your work directory, as Hessa wrote it.

```text
# REMIT-414: open the Bangladesh (BDT) corridor, and show your working

**From:** Hessa, Product Owner, Najm Remit
**Priority:** High. Marketing has announced Bangladesh for the end of the quarter.

Treasury has agreed these numbers. Everything here is fictional, like the rest of Remit.

### The corridor

| | |
|---|---|
| Code | `QAR-BDT` (send QAR, receive BDT) |
| Per transfer | QAR 100.00 to QAR 12,000.00, both inclusive |
| Delivery | `bank_deposit` (the default) and `wallet`; no `cash_pickup` |
| Mid-market rate | 1 QAR = 33.46 BDT |
| Margin | 0.0175, taken off the mid rate like every corridor |
| Fees | a schedule of its own, `STD-C`, below |

`STD-C` works like the others: the whole amount picks the tier, the upper bound is included, the minimum and the cap apply, and the express surcharge comes after the cap.

| Amount up to (QAR) | Percent | Flat (QAR) |
|---:|---:|---:|
| 1,000.00 | 2.20% | 3.50 |
| 5,000.00 | 1.60% | 12.00 |
| no limit | 1.10% | 45.00 |

Minimum fee QAR 7.00, cap QAR 130.00, express surcharge QAR 18.00. The KYC tiers' daily and monthly limits do not change and apply here too: by "limits" above I mean only the minimum and maximum per transfer.

### What the customer reads

A new template, `transfer_sent_bdt`, goes out for `QAR-BDT` transfers; every other corridor keeps `transfer_sent`. Customer Care approved this wording, so do not rephrase it. Values: `name`, `transfer_id`, `recipient`, `receive_amount`, `send_amount`, `fee`, `rate` (the customer rate).

    en: Hi {name}, your transfer {transfer_id} to Bangladesh was sent. {recipient} received {receive_amount} at a rate of 1 QAR = {rate} BDT. You paid {send_amount} plus a fee of {fee}. Please keep this message as your receipt.
    ar: مرحباً {name}، تم إرسال تحويلك {transfer_id} إلى بنغلاديش. تم استلام مبلغ {receive_amount} من قبل {recipient} بسعر صرف ١ ريال قطري مقابل {rate} تاكا. المبلغ المرسل: {send_amount}، والرسوم: {fee}. يرجى الاحتفاظ بهذه الرسالة كإيصال لك.

### How I want it delivered

The change, and the evidence around it. `lab-assets/hessa-notes.md` has my meeting notes, `lab-assets/templates/` a starting point for each document and `lab-assets/README.md` what the grader reads in each one. Use an agent as much as you like; you answer for every line.

- the change in `src/remit/` (`corridors.py`, `fees.py`, `fx.py`, `notify.py`, `service.py`), added to the tables that are already there, and new `tests/test_*.py` files; each acceptance criterion of your spec is named in a test (`AC1`, `AC2`...)
- `CLAUDE.md` (or `AGENTS.md`), updated for corridor work: start from your lesson 2.2 file or `templates/memory.md`
- `specs/REMIT-414.md`, then `specs/REMIT-414-plan.md`: one row per step, the last column that step's commit header
- `docs/adr/0001-<short-title>.md`: one decision
- `docs/review-REMIT-414.md`: your own diff, `AI-assisted: yes` or `no`, the money files needing a second human
- `.claude/settings.json` and `.claude/hooks/guard.py`
- `docs/corridors.md` (new) and the lines of `docs/ARCHITECTURE.md` this change makes untrue
- `docs/agent-log.md`, then `docs/retrospective.md`

`CONTRIBUTING.md` applies; its list of scopes is only examples, so `claude` or `specs` is fine. One kind of change per commit: code with its tests (`src/`, `tests/`), or documents (`docs/`, `specs/`), or agent configuration (`CLAUDE.md`, `.claude/`). At least eight commits. Do not edit an existing test, add a dependency or touch files the change does not need; keep scratch scripts outside the repository. In every document a path in backticks must exist (unless its line says it does not), and a line or table cell that starts with `TODO` counts as unfinished. Where this ticket is silent, decide, write the decision in your spec and say who confirms it.

Done when every required check of `python -m ailab grade m14 --dir <this directory>` passes (run it from the `ailab` folder of the course repository, on the branch with your commits). It checks the result and how the documents refer to each other, not whether your thinking was good.
```

**Start.**

```bash
cd ~/system-design-for-vibe-coders/ainative/ailab    # virtual environment of lesson 0.2 active
python -m ailab start m14 --dir ~/ainative/m14
cd ~/ainative/m14
export PYTHONPATH=src    # so python -m remit works
pytest -q                # 99 passed
```

`python -m ailab solve m14 --dir ~/ainative/m14` applies the reference solution. It is a peek: try first.

**Your move.** (1) Read `lab-assets/hessa-notes.md` (context, not orders) and `lab-assets/README.md`. Write `CLAUDE.md` (or `AGENTS.md`) from your lesson 2.2 file or `lab-assets/templates/memory.md`, and let an agent interview you in plan mode for the spec; commit spec and plan before any code prompt. (2) Install the baseline hardening, or bring your lesson 8.2 files, and read every line you keep. Run these in `~/ainative/m14`:

```bash
mkdir -p .claude/hooks
cp lab-assets/harden/settings.json .claude/settings.json
cp lab-assets/harden/guard.py .claude/hooks/guard.py
python3 .claude/hooks/guard.py < lab-assets/hook-samples/block-rm-rf.json; echo $?    # Blocked: ... then 2
```

Exit code 2 with a reason on standard error blocks a command; any other non-zero code is a non-blocking error, so a guard must block what it cannot read. (3) Tests first, then one step per commit. CONTRIBUTING.md wants a green suite at every commit, so one commit of red tests alone is a deliberate exception here; committing each step's tests with its code is fine too. Its scope list is only examples: `chore(claude)` and `docs(specs)` pass. (4) Review your own diff, then ask a fresh session for a second opinion; if you cannot start one, write "self-review" in the notes and put your questions for the humans under Second reviewer. (5) Write the ADR, the corridors page and the architecture fix from the code. (6) Log, then write the retrospective last, from `lab-assets/templates/retrospective.md`: it quotes a commit hash, so after any rebase or amend copy one again. *No agent:* the same order; budget a week of part-time study.

**What the grader checks.** *The change:* five groups of hidden acceptance tests (corridor, fees, rate, wording, and the send path with limits, ledger and command line); no old test weakened; only the expected files touched; your new tests failing without your change and noticing at least four of six deliberate defects, each one agreed number broken in the repository's own tables (a test that asserts nothing, or computes its expected value with the code, notices none). *The evidence:* each document keeps its template's headings and has no `TODO` placeholder; a path in backticks exists unless its line says it does not; documents are checked against the code and each other (spec ids proved by a plan step and named in a test, at least three correct worked results in the spec, a commit header in the plan's last column, `docs/corridors.md` equal to the code, the retrospective quoting the log's total and a commit); the hook runs on 18 sample inputs. *Hygiene and security:* Conventional Commits, one kind of change per commit, no secrets, no float or clock shortcuts, no new dependency. *Advisory:* tests before or with the code, a history that follows the plan, small commits, a hook that sees through `bash -lc`, ask rules for the money files.

**Grade.**

```bash
cd ~/system-design-for-vibe-coders/ainative/ailab      # with the virtual environment active
python -m ailab grade m14 --dir ~/ainative/m14
```

On the starter state the real output includes these lines (others omitted):

```text
[PASS] Your tests pass: 99 passed
[FAIL] Corridor: code, minimum, maximum and delivery: 16 hidden checks failed: test_the_corridor_exists_and_corridors_are_listed_in_code_order, test_the_corridor_has_a_fee_schedule_of_its_own_called_std_c (+6 more)
       hint: Compare the corridor with the table in the ticket. Is each limit inclusive, and does one cent outside it fail?
[FAIL] Spec: sections, agreed numbers and acceptance criteria: specs/REMIT-414.md does not exist
[FAIL] Guard hook blocks the dangerous and allows the harmless: .claude/hooks/guard.py does not exist

Lab m14: 7/29 required checks passed: NOT YET
```

Pointing Bangladesh at `STD-B` instead of `STD-C` runs and looks plausible, yet fails your own tests, three groups of hidden tests (corridor, fees, send path) and the corridors page (`QAR-BDT: wrong or missing fee schedule`).

When every required check passes, the last line reads `Lab m14: 29/29 required checks passed: PASSED`.

**The rubric.** Score each dimension 1 to 4. The grader can award the evidence rows up to 3; you and your group score the rest at the demo.
- *Context and spec:* 1 spec after the code; 2 criteria vague; 3 numbered, testable; 4 non-goals held.
- *Small steps:* 1 one big commit; 2 mixed kinds; 3 one kind, tests first; 4 history matches plan.
- *Verify and review:* 1 green suite only; 2 tests pin numbers; 3 tests fail without the change; 4 a stranger's review answered.
- *Security baseline:* 1 defaults; 2 deny rules; 3 hook blocks and allows; 4 hook limits written down.
- *Documents:* 1 from memory; 2 match today; 3 cross-refer, checked; 4 drift check automated.

**Weekly deliverable (Module 14).** In a notes folder of your own, commit `week-14/` with `m14-grade.txt` (the final grade output), `baseline-after.md` (the lesson 0.1 self-check again, if you did one), `demo-notes.md` and `portfolio.md`. The kit does not check these.

**As a portfolio piece,** write a one-page `README`: what changed, how you know it is right, where AI helped and where you overruled it; say it is fictional and leave out secrets. See [*From Graduate to Hired*, lesson 3.1 — Projects that prove you can do the job: one capstone spec per role](../career/index.html#/3.1) and [lesson 3.2 — Your GitHub, READMEs and writing about your work](../career/index.html#/3.2).

**Group session (90 minutes).** (1) Demo, in English and Arabic; Hessa asks if Customer Care would sign (15). (2) The trail: spec, plan, `git log --oneline`; Tariq asks where the plan changed (15). (3) Move the cap by one cent, live (the **Mutation check** of lesson 5.1); Nada asks which test fails (20). (4) Try to make the agent read `.env`, push or install; Noura asks what the guard cannot see (15). (5) Swap repositories and find the riskiest hunk in `git diff lab-start` (15). (6) Agree one change to the memory file (10).

**Debrief.** What did the agent get wrong, or nearly? What did your context or spec miss? Which document would you write first?

**Agent log template** (`lab-assets/templates/agent-log.md`; the retrospective quotes its `Total minutes:` line):

```markdown
# Agent log: REMIT-414

One row per session or task (at least three), including the ones where you did the work by hand ("no agent"). The last column is whole minutes; the total is their sum.

| # | Task | Prompt (short) | What it did | What I corrected | Artefact | Minutes |
|---|---|---|---|---|---|---|
| 1 | TODO | TODO | TODO | TODO | `specs/REMIT-414.md` | 0 |

Total minutes: 0
```

## 🛠️ Exercises
- 🟢 **Core: the change and its spec.** *No agent needed.* *Done when:* the five hidden groups, `Your tests pass` and the spec, plan and test-trace checks print PASS.
- 🟡 **Full cycle.** *Needs an agent: recommended.* All eight milestones. *Done when:* `grade` prints `PASSED` and the retrospective names the document that changed your mind.
- 🔴 **Hero: a stranger and the demo.** *Needs an agent: recommended.* *Done when:* the six advisory checks pass, you have held the session, and a peer has reviewed your branch with the **AI pull-request review checklist** and you answered every finding.

## ⚠️ Mistakes and traps
- **Writing the spec after the code.** It then describes what the agent did. **Specify before you delegate.**
- **Letting the agent work out the numbers.** A float can resolve a tie the wrong way, and no summary says so. **Trust evidence, not fluency.**
- **Keeping a hook or settings file you have not read.** The grader accepts a copy; you answer for it. **Automate the loop, keep the skill.**
- **Documents that agree because one was copied from another.** Copy from the code.
- **A green run taken for a review.** The demo asks what the checks cannot.

## 🧾 Recap
- One small change, ten pieces of evidence that refer to each other and the code.
- Order is a decision: spec, plan, tests, then providers before the consumer.
- The five habits in one change: **Context first** (memory file), **Specify before you delegate** (spec, plan), **Small verified steps** (tests first, a commit per step), **Trust evidence, not fluency** (hand-worked values, review, demo), **Automate the loop, keep the skill** (guard hook, log).
- Work the money out by hand, and match evidence to risk. The grader sees shape, truth and references; the demo tests understanding.

## ✍️ Check yourself

**1. Your plan adds the `QAR-BDT` corridor before the `STD-C` schedule, and an old test goes red. What does that tell you?**

- A. The old test is flaky, so rerun it
- B. Corridors must be added in alphabetical order
- C. The corridor names a schedule that does not exist yet
- D. The agent also edited an old test

<details><summary>Answer</summary>

**C.** An old test checks that every corridor names a real fee schedule: providers come first. (🟢 Providers before the consumer.)

</details>

**2. The agent's `STD-C` tests compute each expected fee by calling `quote_fee`, then assert that `quote_fee` returns it. All pass. What does that show?**

- A. The fees match the ticket, because test and code agree
- B. Nothing about the fees, because those tests cannot fail
- C. The schedule is well tested, because every tier is covered
- D. Only a style problem, because the tests are repetitive

<details><summary>Answer</summary>

**B.** A value computed by the code under test can only agree with it. Expected values come from you, worked by hand. (🟢 Work the money out by hand.)

</details>

**3. After writing the plan you rename `tests/test_bdt_corridor.py`, and the grader fails the plan check. What is the sound response?**

- A. Rename the file back, because a plan may never change
- B. Delete the file names from the plan, so the check passes
- C. Leave it, because a plan is only a draft
- D. Fix the plan's file name in a documents commit

<details><summary>Answer</summary>

**D.** Plans change, but one naming a missing file is false. Fix it in a documents commit, not a code commit. (🏛️ What the grader checks.)

</details>

**4. Your guard hook crashes with exit code 1 on input that is not JSON. With default hook settings, what happens to that command?**

- A. It runs, because exit code 1 does not block the call
- B. It is blocked, because the hook itself reported an error
- C. Claude Code asks you, because any hook error prompts
- D. It is retried until the hook exits with 0

<details><summary>Answer</summary>

**A.** By default only exit code 2 blocks; any other non-zero code is a non-blocking error, so a guard must block what it cannot read. (Newer versions add an opt-in `onFailure` setting: check the current documentation.) (🟢 Your move.)

</details>

**5. Lujain passes every required check, but at the demo cannot tell Nada why the cap bites at 10,000.00 and not at 7,000.00. What does this show?**

- A. The grader is broken, since a pass should mean understanding
- B. Nada's question was unfair, since the tests prove the cap
- C. The grader cannot see understanding; you answer for every line
- D. Lujain needed a longer explanation from the agent

<details><summary>Answer</summary>

**C.** Checks verify results, not minds. The raw fee is 122.00 at 7,000.00 but 155.00 at 10,000.00, against a cap of 130.00. (🔴 What the grader cannot tell.)

</details>

## 📚 References
- Claude Code documentation: memory https://code.claude.com/docs/en/memory; permissions https://code.claude.com/docs/en/permissions; hooks https://code.claude.com/docs/en/hooks; best practices https://code.claude.com/docs/en/best-practices
- DORA, "Announcing the 2025 DORA Report" (Google Cloud): https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report
- Michael Nygard's ADR format, as used by adr-tools: https://github.com/npryce/adr-tools; Conventional Commits: https://www.conventionalcommits.org; the lab kit: https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/ainative/ailab
- [*Software Testing*, lesson 6.2 — Tests as the specification for coding agents](../testing/index.html#/6.2); [*Secure AI & Application Security*, lesson 6.3 — Securing AI-generated code: what coding agents get wrong](../secai/index.html#/6.3)

---

# 14.2 — Practice exam: 60 scenario questions
*Level: 🔴 Advanced* · *Prerequisites: Modules 0-14* · *Focus: Mindset, Context, Workflow, Verify, Secure, Automate, Team*

## ⚡ In 60 seconds
- **Sixty scenario questions** from all fifteen modules (0 to 14), mixed and numbered 1 to 60. Most are short scenes on the Payments Platform team. Each has one best answer.
- **Take it in one sitting of about 90 minutes,** with no notes, no agent, and no opening of answers as you go. Write your letters down first, then mark.
- **Bands are the course's own guide, not a certification, and no exam board is involved.** 54 or more (90%): you can teach it. 48 to 53: the judgement this course aims for. 36 to 47: a solid base with gaps, so make a plan and retake in two weeks. Below 36: redo the labs behind your weakest tag.
- **Every answer ends with a tag and a lesson,** for example *(Verify · 5.2)*. Count your misses per tag: the highest count is where to study first.
- **Count a lucky guess as a miss.** You are measuring what you can rely on at work.

## 🧭 Why it matters
Lujain passes every lab. The grader tells her when she is done, and she is quick. On Monday Tariq stops her in the corridor: "Your agent says the tests pass, and the diff touches `limits.py`. What do you do first?" She knows the lessons, and still the answer does not come. At work there is no grader. There is a question, a tired afternoon and an option that sounds sensible. This exam is a safe place to get those wrong. It tests choosing, not remembering, and it shows you which habit to practise next.

## 📐 How it works

### 🟢 Question styles, and the seven tags
Five kinds of question come up again and again. *What do you do first?* asks for the next step in the loop. *What is the likeliest cause?* gives you a symptom, a diff or a session. *Which evidence would settle it?* asks for the check that could fail. *Which rule or setting applies?* tests a fact about permissions, hooks or memory. *What does the team agreement ask?* tests policy and review norms.

Each lesson carries a Focus tag, and each answer repeats it. Use this table to tally your misses.

| Focus tag | What it trains | Modules and lessons |
|---|---|---|
| Mindset | the shift, how agents work, staying sharp | 0.1, 0.3, 1.1, 1.2, 13.1, 13.2 |
| Context | context first | Module 2: 2.1, 2.2 |
| Workflow | specify, small steps, debugging, legacy, lifecycle | 0.2, 0.3, 3.1, 3.2, 4.1, 4.2, 6.1, 6.2, 7.1, 7.2, 10.1, 10.2, 11.1, 11.2, 14.1 |
| Verify | trust evidence, not fluency | 1.2, 5.1, 5.2, 6.2, 7.1, 7.2, 11.2, 14.1 |
| Secure | safety around the agent | 0.2, 8.1, 8.2, 14.1 |
| Automate | automate the loop, keep the skill | 8.2, 9.1, 9.2, 10.1 |
| Team | policy, review norms, metrics | 12.1, 12.2, 13.2 |

### 🟡 Elimination
Read the last sentence first: it says whether you want the first step, the best option or the likeliest cause. Cover the options and say what you would do. Then strike every option that breaks a habit. The wrong answers are patterns you have met:

| Pattern | Habit (or tag) it breaks | Sounds like |
|---|---|---|
| The fluent summary | Trust evidence, not fluency | "The agent says all tests pass, so merge" |
| The bigger prompt | Context first | "Paste the whole repository into the session" |
| The one-liner | Specify before you delegate | "Just add the feature, you know what I mean" |
| The silent fix | Small verified steps | "Let it fix the failing test as well" |
| The prayer | Secure | "Tell the agent not to read `.env`" (a prompt is not a control) |
| The hero | Automate the loop, keep the skill | "Let it do all of it, and stop reading diffs" |

If two options survive, prefer the one that is cheaper to check and to undo, and the one earlier in the loop.

### 🔴 Scenario reading
Underline the facts: who is accountable, what is at stake (money logic, customer data, a secret), what evidence already exists, what has been tried, and the question word. Take one scene that is not in the exam: *the agent reports "all tests pass" after editing `tests/test_fees.py` to match its new output; what do you do first?* The word is "first", and the evidence is a summary plus a changed test. Accepting it fails habit 4. Asking the agent to explain it gives you more fluency. Adding a rule to `CLAUDE.md` may be right later. What comes first is to run the original tests against the new code. Budget about ninety seconds a question: answer what you know, flag the rest, return, and mark each guess.

## 🧰 The toolkit
| Tool, practice or pattern | What it is and does | When to reach for it |
|---|---|---|
| **Miss log** | A row for every miss or guess: number, my answer, the correct one, tag, lesson, the trap, what I will re-read | Straight after marking |
| **Tag tally** | Misses counted per Focus tag; the highest tag leads the study plan | After the miss log |
| **Study plan** | One page: weakest two tags, two weeks of re-reading and teaching, a retake date | After the tag tally |

## 🏛️ In practice at Najm Bank
Tariq never asks a new engineer for the score. He asks for the miss log and the plan, on one page.

```markdown
# Exam result and study plan                      Date:

Score: __ / 60     Band:
Guesses that were right (count them as misses below): __
Misses by tag:  Mindset __ · Context __ · Workflow __ · Verify __ · Secure __ · Automate __ · Team __

| # | Mine | Correct | Tag · lesson | The trap I fell for | What I will do |
|---|---|---|---|---|---|

Weakest two tags:
Week 1: re-read the expert view of the lessons behind my weakest tag; redo that lab's debrief on a fresh copy.
Week 2: write five questions for it; teach one lesson to a colleague.
Retake on:               (not before two weeks; aim to beat my own tag score, not only the total)
```

Fill it in this order. Mark the exam and count guesses as misses. Write one row per miss, naming the trap from the table above. Tally by tag. Pick the two highest and read the lessons your rows point to; redo the lab behind the tag, not just the reading. Teaching a lesson is the strongest test of all, because a gap in your explanation shows within a minute.

## 🛠️ Exercises
- 🟢 **Review your misses.** *No agent.* *Done when:* your miss log has a row for every wrong or guessed answer, each with a tag, a lesson and the trap, and the tag tally is filled in.
- 🟡 **Write five questions of your own.** *An agent may critique them, not write them.* *Done when:* five scenarios at Najm Bank or your own workplace, in the course format: four options, one best, an answer that explains the best distractor and ends with a tag and a lesson. No answer is the longest option every time, and one colleague has tried them and found at least one distractor tempting.
- 🔴 **Teach one lesson.** *No agent for the preparation.* Pick the lesson behind your weakest tag and teach it for twenty minutes with a Najm Remit example and one live exercise. *Done when:* your colleague answers two of your questions correctly, and you have logged one question they asked that you could not answer.

## ⚠️ Mistakes and traps
- **Opening answers as you go.** It turns an exam into a reading exercise. Write all the letters first.
- **Counting lucky guesses as knowledge.** A guess is a miss in the log, even when it was right.
- **Choosing the most complete-sounding option.** Many questions ask what to do *first*, and the complete plan is often the wrong answer.
- **Answering for the team you know.** Use only the facts in the scene, not how your own workplace does it.

## 🧾 Recap
- The exam tests choosing under pressure: sixty scenes, one best answer each, about ninety minutes.
- The bands are a guide, not a certification; the miss log and the tag tally are the point.
- Strike options that break a habit; of the survivors, take the one cheaper to check and to undo.
- A plan from your misses is two weeks long and ends with you teaching a lesson.

## ✍️ Practice exam

@@EXAM@@

## 📚 References
- Claude Code documentation, behind many questions: memory https://code.claude.com/docs/en/memory; permissions https://code.claude.com/docs/en/permissions; hooks https://code.claude.com/docs/en/hooks; skills https://code.claude.com/docs/en/skills; subagents https://code.claude.com/docs/en/sub-agents; MCP https://code.claude.com/docs/en/mcp; headless mode https://code.claude.com/docs/en/headless; best practices https://code.claude.com/docs/en/best-practices
- Each answer names the lesson to review; the references of that lesson list the sources behind it.
- The lab kit: https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/ainative/ailab
