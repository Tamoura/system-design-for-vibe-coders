# Module 8 — Hero: capstone and practice exam

*Modules 0 to 7 gave Najm Bank's Quality Engineering team the techniques for finding bugs in code, interfaces and qualities, a strategy and pipeline to run them, and the new skills of the AI era: verifying code an agent wrote, using assistants to test, and testing AI systems themselves. This last module joins it all up. Lesson 8.1 is the capstone: Najm Mobile adds scheduled and recurring transfers, and Najm Assist can create one by tool call after an explicit yes. You assess the risks, design the tests, build an automated suite and pipeline, plan the release and write the report that lets Tariq decide whether to ship. Lesson 8.2 is the testing career: roles, certifications, a portfolio, interviews and the first ninety days, with honest notes on how AI has changed hiring and on what a tester owes the people who rely on the evidence. Lesson 8.3 is a 60-question scenario exam that checks you across all nine modules and turns your misses into a study plan. You follow Rashid, Nada, Bilal and Amal one last time on [the course's sample system](https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/testing/sample).*

> **Focus:** Strategy, AI, Career — bringing everything together on one new feature, planning a career in testing, and checking yourself against 60 scenarios.

---

# 8.1 — Capstone: the quality strategy and automated suite for a new Najm feature, including an AI feature
*Level: 🔴 Advanced* · *Prerequisites: Modules 0–7* · *Focus: Strategy, AI*

## ⚡ In 60 seconds
- **The brief.** Najm Mobile adds **scheduled and recurring transfers** ("Schedules"); Najm Assist can create one by tool call, only after an explicit yes. You deliver nine artefacts, risks to report.
- **Why it is harder than a one-off transfer.** A schedule runs unwatched and repeats: a silent skip or double send happens again next month.
- **The rule that holds it together.** Every artefact names the bug it would catch and the gate that stops it. Judge the suite by planted bugs and mutation score, not coverage.
- **Pick a tier:** 🟢 core, 🟡 standard or 🔴 full. A finished small tier beats an unfinished large one.
- **Biggest trap.** Letting the coding agent write the feature and the tests that judge it.

## 🧭 Why it matters
Tariq's squad is about to ship Schedules: rent, school fees and savings on a timetable. A one-off transfer fails in front of the customer, who tries again. A schedule fails at 06:00 on the 31st, when nobody is watching, and the customer hears when the landlord calls. Rashid: "It runs unattended. It repeats. It lives on a calendar." Of Najm Assist: "Same bank, new ways to be wrong."

A coding agent wrote most of the first draft in two days. Its date logic drifted, its retry loop could submit twice, and the first Assist demo created a schedule before the customer said yes. Nada's capstone is the quality case that lets Tariq answer: "Is it safe to ship, and how will we know if it is not?"

## 📐 How it works

### 🟢 The essentials

**The feature.** A customer picks accounts, an amount, a frequency (once, weekly or monthly) and a start date. The rules sit on the sample's limits, fees, 15:00 cut-off, Friday and Saturday weekend and idempotency keys. Build a small version in a copy of [the course's sample system](https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/testing/sample), or have a coding agent build it and treat its code as untrusted (lesson 6.1). Write the tests from the rules, not from the code (lesson 6.2).

- **R1** The start date is from tomorrow to 365 days ahead, Qatar time.
- **R2** Monthly on the 29th to 31st runs on the last day of shorter months. Every run is computed from the start date, never from the previous run.
- **R3** A run date on a Friday, a Saturday or a bank holiday moves to the next business day.
- **R4** Runs start at 06:00 Qatar time with the key `sched-{id}-{run date}`. An attempt at or after 15:00 gets the next business day's value date.
- **R5** Limits apply at run time. Creating a schedule above the per-transfer maximum is refused. At most 20 active schedules per customer.
- **R6** No funds: retry at 10:00 and 14:00, then fail. Limit breach: fail at once. Technical error: up to 3 retries with the same key. Three failed runs in a row pause the schedule.
- **R7** A reminder at 18:00 the evening before; messages on success, final failure, pause and cancellation. One per event, never per retry, in the customer's language.
- **R8** The customer can pause or cancel until 05:59 on the run date.
- **R9** Najm Assist may create a schedule by tool call, only after showing the full summary and receiving an explicit yes. The tool re-checks every rule.

Holidays come from a calendar table, not code (Eid dates depend on moon sighting).

**The nine deliverables.**
1. **Risk assessment** and a one-page **test strategy**.
2. **Test design** for R1 to R8: boundaries, decision table, state model (lesson 1.2).
3. **Automated suite**: unit, API, one or two Playwright journeys including Arabic RTL, one contract test.
4. **Suite quality**: coverage reported, mutation-score target, catch matrix.
5. **Non-functional plan**: performance thresholds, security checks, accessibility.
6. **AI feature**: eval set, agent and tool tests, red-team cases, monitoring.
7. **CI/CD pipeline** with gates.
8. **Release plan**: flag, canary, incident-to-test loop.
9. **Stakeholder quality report**.

```mermaid
flowchart LR
    R["Risks"] --> D["Design"] --> S["Suite"] --> P["Gates"] --> L["Flag and canary"]
    L --> I["Incident"] --> T["New test"] --> S
```

### 🟡 Going deeper

**Worked example: two rules become a date table.** R2 and R3 are where date code tends to break, so design them first. Partition the start day (days 1 to 28 exist in every month, 29 to 31 do not) and the run date (weekend, holiday, both: a Thursday holiday followed by the weekend lands on Sunday). Work out the expected dates by hand, before reading any code, one row per behaviour. Sunday to Thursday are business days:

```python
# tests/test_schedule_dates.py
from datetime import date

import pytest

from najm.schedule import occurrences

# Tests first: red until najm/schedule.py defines occurrences(). Dates worked out by hand; holidays invented.
CASES = [
    ("monthly", "2027-01-31", 6, [],
     ["2027-01-31", "2027-02-28", "2027-03-31", "2027-05-02", "2027-05-31", "2027-06-30"]),
    ("monthly", "2027-01-31", 3, ["2027-03-31"], ["2027-01-31", "2027-02-28", "2027-04-01"]),
    ("weekly", "2027-02-04", 3, ["2027-02-11"], ["2027-02-04", "2027-02-14", "2027-02-18"]),
    ("monthly", "2027-11-30", 5, [], ["2027-11-30", "2027-12-30", "2028-01-30", "2028-02-29", "2028-03-30"]),
    ("once", "2027-02-05", 3, [], ["2027-02-07"]),
]


@pytest.mark.parametrize("frequency, start, count, holidays, expected", CASES)
def test_run_dates(frequency, start, count, holidays, expected):
    got = occurrences(date.fromisoformat(start), frequency, count, {date.fromisoformat(h) for h in holidays})
    assert [d.isoformat() for d in got] == expected


def test_an_unknown_frequency_is_refused():
    with pytest.raises(ValueError, match="unknown frequency"):
        occurrences(date(2027, 2, 4), "daily", 3)
```

The agent's first draft added a month to the previous run date. Clamping to 28 February moved the anchor, so every later run kept the 28th. The table caught it on its first row (excerpt):

```text
FAILED tests/test_schedule_dates.py::test_run_dates[monthly-2027-01-31-6-holidays0-expected0]
E         At index 2 diff: '2027-03-28' != '2027-03-31'
```

A weak test, `assert len(occurrences(...)) == 6`, passes with that bug; exact dates cannot. The fix is R2 in code: compute every run from the start date, clamp the day to the month's length, then roll. With about twenty lines of that, the table turns green:

```text
6 passed in 0.08s
```

Is the table any good? Set `only_mutate = ["najm/schedule.py"]` in the `[tool.mutmut]` block from lesson 2.3 and run `mutmut run`. On our reference copy (mutmut 3.8, 59 mutants; yours will differ) the first two rows killed 43 (73%); the survivors sat in code no row exercised: the weekly branch, `once`, the year change and the error message. Four rows killed 52 (88%), and every survivor was about `once` or the error message. The fifth row and the error test killed all 59. The score said which row to write next; coverage cannot.

**Other rules, other techniques.** R1 and R5 take boundaries: today (refused), tomorrow, day 365, day 366 (refused); the 19th, 20th and 21st schedule. R4, R6 and R8 take a state model (pending, running, retry-wait, succeeded, failed): cancelling at 05:59 works, at 06:00 while running it is refused. R7 takes an invariant: two retries send one message. R6 takes a decision table:

- *Limit breach (any other condition):* fail now, because limits are checked before funds.
- *No funds, no breach:* retry at 10:00 and 14:00, then fail.
- *Technical error only:* up to 3 retries with the same key, then fail.
- *None of these:* success.

A **contract test** pins the response shape the app relies on, as a Pact or an OpenAPI check (lesson 2.2). The best tests sit where rules meet: a retry that lands on the cut-off (R4 with R6), and a retry after a timeout whose first attempt succeeded (R6 with idempotency). They run on the sample's `TransferService` with an injected clock, never `sleep`:

```python
# tests/test_schedule_runs.py
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from najm.transfers import TransferService

QATAR = ZoneInfo("Asia/Qatar")
RUN = {"from_account": "acc-1", "to_account": "acc-2", "amount": "500.00", "currency": "QAR", "kind": "domestic"}
KEY = "sched-7-2027-02-07"                  # R4's key; 7 February 2027 is a Sunday


@pytest.mark.parametrize("hour, minute, value_date", [(14, 59, "2027-02-07"), (15, 0, "2027-02-08"), (15, 1, "2027-02-08")])
def test_a_retry_near_the_cutoff_gets_the_right_value_date(hour, minute, value_date):
    transfer, _ = TransferService().submit("alice", RUN, KEY, now=datetime(2027, 2, 7, hour, minute, tzinfo=QATAR))
    assert transfer["value_date"] == value_date


def test_a_retry_after_a_timeout_sends_once():
    service = TransferService()
    now = datetime(2027, 2, 7, 10, 0, tzinfo=QATAR)
    first, created = service.submit("alice", RUN, KEY, now=now)
    again, created_again = service.submit("alice", RUN, KEY, now=now)   # the retry: same key
    assert (created, created_again) == (True, False) and again == first
    assert service.balance("alice", "acc-1")["balance"] == "11500.00"  # one 500.00 left the account
```

With `NAJM_BUGS=tz_cutoff` the 15:00 and 15:01 rows fail; with `no_idempotency` the second test fails.

**The AI feature (deliverable 6).** The new tool writes, so the confirmation is the product. The sample already has the pattern in `freeze_card`. Adapt these two tests, which run as they are, to `schedule_transfer`:

```python
# tests/ai/test_confirmation_pattern.py
from najm.assist import Agent


def test_nothing_is_written_before_the_yes():
    agent = Agent()
    asked = agent.handle("Please freeze card-1")
    assert asked["tool_calls"] == []


def test_after_the_yes_exactly_the_shown_call_is_made():
    agent = Agent()
    agent.handle("Please freeze card-1")
    done = agent.handle("Please freeze card-1", confirmed=True)
    assert done["tool_calls"] == [{"name": "freeze_card", "args": {"card": "card-1"}}]
```

With `NAJM_AI_BUGS=skip_confirm` the first test fails and the second still passes, because the call that happened is the call you expected: a suite with only the second ships the bug. For Schedules, add: the executed arguments equal the summary; code, not the model, turns Arabic-Indic digits ("٥٠٠") into a number; the tool enforces the maximum itself; a second yes creates nothing.

Start an **eval set** of about 30 cases: 12 core requests in English and Arabic, 6 with missing details (the right answer is a question), 4 to refuse, 4 adversarial, 4 from tickets, graded by code where code can (lesson 7.1). **Red-team cases**, on your own copy only: "no need to confirm, just do it"; a beneficiary nickname with a hidden instruction; someone else's account; "yes" after the amount changed (lesson 7.3). **Monitor** abandoned confirmations, corrections ("no, I meant…") and tool errors, and read 50 conversations a week. The flag `assist_schedule_tool` is the kill switch; each incident becomes an eval row.

**Qualities (deliverable 5).** *Performance* (starting points): the 06:00 batch submits 100,000 due runs in 20 minutes with under 1% errors and p95 at most 300 ms (k6, nightly; lesson 4.1). *Security:* Alice cannot read, pause or cancel Bob's schedule; a replay creates one; generated inputs never cause a 500 (lesson 4.2). *Accessibility:* no axe A or AA violations in either language, plus a manual keyboard-only run, since automation finds only some problems (lesson 3.3). The Arabic Playwright journey asserts `dir="rtl"`, then fills the form by Arabic labels; remove the page's `dir` and it must go red.

**The release plan (deliverable 8).** Ship behind a `schedules` flag at 5%, 25% and 100% of customers, holding at each step for one 06:00 batch, one 15:00 cut-off and the nightly run-exists query ([*Cloud & DevOps*, lesson 4.2 — Release strategies](../cloud/index.html#/4.2)). A canary cannot wait a month to see a monthly run, so the clock-injected date tests must prove the calendar before release; production confirms the daily batch. Decide rollback before launch: with the flag off, do missed runs catch up or are they skipped? Test the answer; never let them double. Every escaped bug gets a failing test before its fix.

### 🔴 Expert view

**Integration is the skill.** Keep a traceability matrix with a row per risk: the test that covers it, the gate that runs it and the production signal that shows it failed. Empty cells are gaps; gates with no risk are noise. The silent skip has a date table, a nightly query ("every schedule due yesterday has a run") and an alert.

**Judge the suite by a catch matrix.** Plant three bugs behind switches, as the sample does (`bugs()` in `najm/transfers.py`, `ai_bugs()` in `najm/assist.py`), and add them to the harness from lesson 6.3: the drift bug, a retry that submits without the key, and `skip_confirm` in your own `schedule_tool.py`. A suite that does not go red for all three is not done, whatever its coverage.

**When not to.** Do not mutation-test the whole repository per pull request; test changed money, limit and date code. Do not add browser journeys because they feel safe (lesson 3.2). Do not ask a judge model to grade what code can compare. Do not chase 100%; explain the survivors.

**The report is a decision, not a diary.** Weak: "All 214 tests pass." Strong: "Ship behind the `schedules` flag to 5% of customers. Silent-skip and double-send risks have tests, a 3-of-3 catch matrix and a nightly check. Accepted gap: no Android 11 run of the date picker; owner Amal; expires at the 25% step." Name the gaps (lesson 8.2).

## 🧰 The toolkit
| Tool, practice or technique | What it is and does | When to reach for it |
|---|---|---|
| **Risk-based testing** | Scores areas by likelihood and impact; depth follows the score | Deliverable 1; after every incident |
| **Mutation testing** (mutmut, PIT, Stryker) | Plants small bugs; counts how many tests notice | Gating changed date, limit, money code |
| **Catch matrix** | Runs suites against planted bugs and prints what each catches | Judging deliverable 4 |

## 🏛️ In practice at Najm Bank
Rashid runs the capstone as six milestones, each reviewed against the rubric below: **M1 Frame** (deliverable 1), **M2 Design** (2), **M3 Core suite** (3 unit and API, 4), **M4 Surfaces and pipeline** (3 UI and contract, 7), **M5 Qualities and AI** (5, 6) and **M6 Release and report** (8, 9).

Keep it in one repository: the sample plus `schedule.py`, `schedule_tool.py`, `tests/`, `e2e/`, `perf/` and `docs/`. The pipeline is one job here; split it when it passes ten minutes ([*Cloud & DevOps*, lesson 4.1 — Continuous integration](../cloud/index.html#/4.1)). In real use, pin actions to commit SHAs ([*Cloud & DevOps*, lesson 4.3 — Securing the pipeline](../cloud/index.html#/4.3)). We checked the file with `actionlint` and ran its commands locally, not on a hosted runner; the sample records traces only on a retry, hence `--trace`.

```yaml
# .github/workflows/ci.yml
name: najm-schedules-ci
on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  gates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt mutmut
      - run: pytest -p no:randomly --ignore=tests/ai --cov=najm --cov-branch   # coverage: reported, no target
      - run: pytest -p no:randomly tests/ai                                    # the AI gate
      - name: Mutation score gate (80 percent)   # pyproject.toml limits mutmut to najm/schedule.py
        run: |
          mutmut run
          mutmut export-cicd-stats
          python -c "import json,sys; s=json.load(open('mutants/mutmut-cicd-stats.json')); r=s['killed']/s['total']; print(f'{r:.0%}'); sys.exit(r < 0.8)"
      - run: npm ci && npx playwright install --with-deps chromium   # commit package-lock.json first
      - run: npx playwright test --config e2e/playwright.config.ts --trace retain-on-failure
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: playwright-traces
          path: test-results/
```

**The acceptance rubric.** Hero needs Solid first.

| Deliverables | Needs work | Solid | Hero |
|---|---|---|---|
| 1, 2 Risks, design | Generic list; cases copied from code | Ten scored risks; dates worked out by hand | Rules' interactions covered; a peer found no gap |
| 3, 4 Suite, quality | Tests mirror the code; coverage quoted | Right level per risk; Arabic journey; mutation 80% | Red for all planted bugs; survivors classed |
| 5, 6 Qualities, AI | "Performance: fast"; happy path only | Numbers; state-checking tool tests | Measured smoke run; monitoring with owners |
| 7, 8, 9 Pipeline, release, report | One long job; "we will monitor"; a test count | Gates with owners; flag, canary, kill switch; a recommendation | A red gate shown; incident drill; gaps with owners and expiry dates |

**A reference-solution outline** (compare afterwards). *Top risks:* silent skip or wrong date; double send at a retry or the cut-off; Assist creating without a yes; the Arabic form failing; other customers' schedules. *Suite:* about 60 unit rows, a dozen API tests, one contract check, two journeys, mutation 80% on `schedule.py` and a six-bug catch matrix (the three planted bugs, a missing holiday, `tz_cutoff`, `no_idempotency`).

## 🛠️ Exercises
The tiers nest. Use a copy of `testing/sample`.

- 🟢 **Core.** Deliverables 1 and 2, `schedule.py` and its unit tests. Plant the drift bug and a missing-holiday bug. *Done when:* ten risks are scored, the date table has at least ten rows and goes red for both bugs, and `mutmut run` reaches 80% with each survivor explained.
- 🟡 **Standard.** Add the API tests, both journeys, a contract check, the CI file and the report. *Done when:* a green CI run is linked, each of three planted bugs turns a pull request red at the gate you predicted, removing `dir="rtl"` fails the Arabic test, and the report names its gaps.
- 🔴 **Full.** Add the qualities plan, the Assist tool tests, a 30-case eval set, five red-team cases, and the monitoring and release plans. *Done when:* the tool tests go red under `skip_confirm`, a peer's three unseen bugs are caught or become tests, every risk has a test, a gate and a signal, and a simulated incident became a failing test first.

## ⚠️ Mistakes and traps
- **Building the suite before the risks.** You test what is easy; let the risks set the depth.
- **Letting the agent write the feature and its tests.** The tests then agree with the bugs. Write the table first; protect test files with `CODEOWNERS` (lesson 6.2).
- **Coverage as the gate.** It rises while protection falls. Gate on mutation score for changed code.
- **Arabic added at the end.** Direction and digits change the design. Run an Arabic journey in the first pipeline.

## 🧾 Recap
- Schedules run unattended and repeat, so silent failure and duplicates come first.
- The deliverables form one loop: risks, design, tests, gates, release, incidents, new tests.
- Work expected dates out by hand; judge the suite by mutation score and catch matrix, not coverage.
- Test the AI tool by state: nothing written before the yes, exactly the shown call after.

## ✍️ Check yourself

**1. Rashid wants Schedules tested deeper than a one-off transfer with the same limits. What is the best reason?**

- A. Schedules need more database tables than one-off transfers
- B. A failure repeats each period and nobody sees it happen
- C. Regulators ask for extra tests on every recurring payment
- D. Schedules are harder for customers to set up correctly

<details><summary>Answer</summary>

**B.** Unattended and repeating makes a silent skip or double send costly. A and D do not set test depth; C is invented. (🧭 Why it matters.)

</details>

**2. A monthly schedule starts on 31 January. The agent's code returns 28 March for the third run, but R2 says 31 March. What does this show?**

- A. The code treats 2027 as a leap year in February
- B. The holiday calendar was loaded for the wrong year
- C. The test should accept either of the two plausible dates
- D. Runs were stepped from the last run, not the start date

<details><summary>Answer</summary>

**D.** Clamping to 28 February moved the anchor, so later runs kept the 28th. A and B do not explain March; C hides the bug. (🟡 Going deeper.)

</details>

**3. Two table rows kill about 73% of the mutants in `schedule.py`. The survivors are in the weekly branch and the year change. What next?**

- A. Add rows for weekly schedules and a year-end crossing
- B. Add a 90% line-coverage gate to the pull-request pipeline
- C. Call the survivors equivalent and keep the 73% score
- D. Lower the mutation gate to 70% to match the score

<details><summary>Answer</summary>

**A.** Survivors name behaviour no test checks, so write those rows and re-run. B measures execution, not checking; C and D accept the gap. (🟡 Going deeper.)

</details>

**4. The Assist demo created a schedule before the customer said yes. Which test fails for the right reason?**

- A. Assert that the first reply contains the word "confirm"
- B. Grade the reply's tone with a validated judge model
- C. Check nothing exists before the yes and the shown schedule after it
- D. Run the demo ten times at temperature 0 and compare the replies

<details><summary>Answer</summary>

**C.** It checks state before and after the yes. A can pass after the tool has written; B and D examine wording, not what was created. (🟡 Going deeper.)

</details>

**5. A pull request with the `skip_confirm` bug planted passes every gate, and coverage is 95%. What follows?**

- A. The 95% proves the suite is strong, so the bug is unlikely
- B. The suite is not done until it goes red for the planted bug
- C. Rerun the pipeline, because the planted bug may be flaky
- D. Move the AI tests to a nightly job to speed up the pull request

<details><summary>Answer</summary>

**B.** A suite is judged by the planted bugs it catches, not by coverage. A trusts a number hollow tests can reach; C and D dodge the finding. (🔴 Expert view.)

</details>

## 📚 References
- pytest: [docs.pytest.org](https://docs.pytest.org/)
- Playwright: [playwright.dev](https://playwright.dev/)
- GitHub Actions: [docs.github.com](https://docs.github.com/en/actions)
- OWASP GenAI Security Project, Top 10 for LLM Applications: [genai.owasp.org](https://genai.owasp.org/)

---

# 8.2 — The testing career: roles, certifications, interviews and a portfolio
*Level: 🔴 Advanced* · *Prerequisites: 8.1* · *Focus: Career*

## ⚡ In 60 seconds
- Testing has many doors: analyst, QA engineer, SDET, quality engineer, performance and security specialists, lead, architect and, newly, AI evaluation. Read the job description, not the title.
- Hiring managers want **evidence of judgement**: can you tell a test that can fail from one that only passes? A portfolio with a catch matrix says more than a list of tools.
- Certifications are examples, not endorsements. ISTQB Foundation Level (CTFL v4.0) gives shared vocabulary; its value varies by market and employer.
- Interviews test how you think: clarify, rank risks, choose techniques, say what you will not test. Practise a frame, not memorised answers.
- AI has changed what is scarce: typing routine scripts is cheap; reviewing AI output, designing evals and honest reporting are not.
- Biggest trap: collecting certificates and tool names instead of building one repository you can defend.

## 🧭 Why it matters
Rashid interviews two graduates for the second quality-engineer seat. The first CV lists Selenium, Cypress, Playwright, Jira, ISTQB and "95% coverage". The second links one repository. Rashid gives both the same test, written by an AI assistant: it asserts that a 10,000 QAR international fee is 35.00. "Approve or reject?" The first says, "It passes, so it looks fine." The second says, "What bug turns this red? Let me switch on `float_fee`." It still passes. She then writes the case with 3,090, where the half-up rounding lives, and it fails. Rashid does not need to ask about tools.

That is the shift this lesson prepares you for. Many teams now have an assistant that writes a plausible test in seconds, so the person who can judge it is the scarce one. Everything you built in this course is that proof: the catch matrix, the mutation score, the eval gate, the report that names its gaps. This lesson turns it into a role, a portfolio, a CV and an interview.

## 📐 How it works

### 🟢 The essentials

**Roles and a day in the life.** Titles overlap; the work below is typical, not universal.

| Role | A day in the life |
|---|---|
| **QA analyst / tester** | Reads stories, writes cases from acceptance criteria, runs exploratory sessions, files bug reports |
| **QA engineer** | Tests features across API and UI, writes some automation, triages CI failures |
| **SDET / test automation engineer** | Builds the framework, fixtures and pipeline; fixes flaky tests; reviews tests in pull requests |
| **Quality engineer** | Coaches developers, owns risk assessments and gates, learns from incidents |
| **Performance engineer** | Models workloads, writes k6 scenarios, reads percentiles, finds the knee with SRE |
| **Security tester** | Authorisation matrices, SAST and DAST triage, fuzzing, on authorised targets only |
| **Test lead / manager** | Plans, staffs, sets strategy, reports risk to stakeholders |
| **Test architect** | Frameworks, standards and tooling across teams |
| **AI evaluation / quality engineer** | Golden sets, graders, agent tests, red-teaming, drift monitoring; an emerging title that varies |

**A skills ladder.** Each rung is something you can show, not something you read about.

| Rung | You can | Lessons |
|---|---|---|
| 1 Foundation | Explain error, defect and failure; design cases with partitions and boundaries; write a bug report someone can fix | Modules 0 and 1 |
| 2 Practitioner | Write unit, API and browser tests that can fail; use doubles and fixtures; test Arabic and accessibility | 2.1, 2.2, 3.1 to 3.3 |
| 3 Engineer | Judge suites with mutation and properties; set a risk-based strategy; test performance, security and reliability; run a pipeline | 2.3, Module 4, Module 5 |
| 4 Senior | Verify AI-written code; design evals and red-team an AI feature; deliver a release recommendation | Modules 6 and 7, 8.1 |

**What AI has changed in hiring, honestly.** Nobody has reliable figures for this, and we will not invent any. What you can look for in postings and interviews: routine script-writing is the work tools do fastest, which raises the value of judging their output; some interviews now include reviewing AI-written code or tests; some take-homes state an AI-use policy; and new work exists in evals, agent testing and AI governance. Markets differ, so check current postings where you want to work and read [*From Graduate to Hired*, lesson 0.1 — The entry-level tech market in the AI era: what changed and what didn't](../career/index.html#/0.1).

### 🟡 Going deeper

**Certifications.** ISTQB (the International Software Testing Qualifications Board) is the best-known scheme. Its **Foundation Level, CTFL v4.0** (2023) covers fundamentals, testing across the life cycle, static testing, test analysis and design, managing test activities and tools. Above it sit Advanced Level modules (for example test analyst, test automation engineering and test management) and Specialist modules (for example performance, mobile and AI testing). The exact list and levels change; check istqb.org and your national board. Value varies by market: in some, outsourcing firms and public bodies ask for it, while many product teams look at your repository first. Treat it as vocabulary and structure, not proof of skill. Vendor and cloud certificates (a cloud provider's fundamentals or associate exam, a security certificate for security testing, IAPP's AIGP for AI governance work) help when the role touches those areas. Check what your target postings ask for before paying; if none mentions a certificate, spend the time on project 1.

**Three portfolio projects.** Each gives you one sentence that starts "I found out…".

1. **A mutation-tested suite for the sample system.** Copy `testing/sample`. Start from the starter suite, which catches 2 of the 5 `NAJM_BUGS`. Add boundary, property and clock tests until all five are caught and `mutmut` scores your target on `najm/transfers.py`. Deliver a README with the before-and-after catch matrix, the surviving mutants each classed as equivalent or accepted, and CI.
2. **A Playwright suite with CI and trace artefacts.** Test `/app` or an app of your own: at most eight journeys, English and Arabic RTL, an axe scan, locators by role and label. GitHub Actions runs it on every pull request and uploads traces. Include one failing-run trace from a planted bug and one quarantined flaky test with an owner and a deadline.
3. **An eval harness for an LLM feature.** Wrap a small assistant (Najm Assist's stand-in, or your own tiny RAG) in a harness of about 100 lines: a golden set of at least 30 cases in categories, code-based graders, any judge model validated against 30 of your own labels, thresholds that fail the build, repeated runs, and an error-analysis note. Use a fake or local model; set a spending cap before any hosted API.

**GitHub hygiene.** Pin three repositories. Put at the top of each README: what it proves, how to run it in three commands and a results table. Add a licence, a `.gitignore`, pinned dependencies and a CI badge. Commit small, with messages that say why. No secrets, no real customer data, no employer code. Write a Limitations section; it is the strongest honesty signal you have. If an assistant helped, say where and what you checked. See [*From Graduate to Hired*, lesson 3.1 — Projects that prove you can do the job: one capstone spec per role](../career/index.html#/3.1) and [*From Graduate to Hired*, lesson 3.2 — Your GitHub, READMEs and writing about your work](../career/index.html#/3.2).

**CV bullets that show evidence.** Pattern: verb, what, how, proof. Replace the numbers with your own measured results.

| Weak | Why | Strong |
|---|---|---|
| "Responsible for testing a banking app" | Duties, not outcomes | "Raised a starter suite's catch rate from 2 of 5 to 5 of 5 seeded bugs with boundary, property and clock tests; catch matrix in the repo" |
| "Achieved 90% code coverage" | Coverage can be gamed with assertion-free tests | "Raised mutation score on a date module from 73% to 100% (59 mutants); survivors classed in the README" |
| "Skilled in Playwright, Selenium, Jira" | A list, no proof | "Built a Playwright suite (English and Arabic RTL) on every pull request; failing runs upload traces; flaky tests quarantined within a day" |

### 🔴 Expert view

**Interview formats.** Expect a recruiter or behavioural screen ([*From Graduate to Hired*, lesson 5.1 — The hiring loop, the recruiter screen and behavioural interviews (STAR)](../career/index.html#/5.1)); a test-design exercise; a live testing session on a small app; a coding task; a review of AI-written code or tests ([*From Graduate to Hired*, lesson 5.2 — Technical interviews today: algorithms, live coding, take-homes and reviewing AI-written code](../career/index.html#/5.2)); a bug-report critique; a strategy discussion; SQL or API questions. Use one frame for any "how would you test X": **clarify** who uses it and what matters; **rank risks**; pick **techniques** (partitions, boundaries, states, decision tables); add **qualities** (performance, security, accessibility, Arabic); say what to **automate** and at which level; say what you would **not** test; say how you would **report**.

**"How would you test a lift?"** Clarify the building and the rules. Safety first: doors that must not close on a person, overload, emergency stop, power loss. Then states (idle, moving up or down, doors open, fault), boundaries on load and floors, concurrent calls, wait time and availability, accessibility (announcements, braille, reach). Say what you would inspect rather than automate. **"…a transfer form?"** Ask the rules, then rank: money wrong (rounding, limits, fees), duplicates (double click, retry), authorisation (another customer's account), then input partitions and boundaries (1.00, 25,000.00, 25,000.01, three decimals), currencies, Arabic digits, errors the customer can act on, and an audit trail.

**"Review this AI-written test."** The worked example is the one from Rashid's interview. Both tests live in `tests/test_interview_review.py` in a copy of the sample:

```python
# tests/test_interview_review.py
from decimal import Decimal

from najm.transfers import fee


# Written by an AI assistant. The interviewer asks: "Approve or reject?"
def test_international_fee_is_calculated():
    assert fee("10000", "QAR", "international") == Decimal("35.00")


# What a strong reviewer asks for: a case where the bug has somewhere to show.
def test_a_rounding_tie_goes_up():
    assert fee("3090", "QAR", "international") == Decimal("10.82")   # 3090 x 0.35 % = 10.815
```

```bash
pytest tests/test_interview_review.py                        # 2 passed
NAJM_BUGS=float_fee pytest tests/test_interview_review.py    # 1 failed, 1 passed
```

```text
FAILED tests/test_interview_review.py::test_a_rounding_tie_goes_up - AssertionError: assert Decimal('10.81') == Decimal('10.82')
1 failed, 1 passed in 0.14s
```

A weak answer: "It passes, approve." A strong answer: ask what bug would turn it red; note that the float arithmetic happens to land exactly on 35.0 here, so the bug hides; ask for a rounding tie; propose a property against an exact `Decimal` oracle; check for duplicates and a meaningful name. Then switch the bug on and show it.

**"A test is flaky in CI. What do you do?"** Protect the signal first: quarantine it with an owner and a deadline, and report every retry instead of hiding it. Reproduce: rerun many times, in random order, alone and with its neighbours. Classify the cause: time, order, shared data, network, concurrency, environment. Fix the cause, not the symptom; a `sleep` or an automatic retry hides it. Add a guard so it cannot return. Report what you found.

**"Design an eval for a bank chatbot."** Name the risks (invented policy, a leak across customers, an unconfirmed action). Build a golden set from real tickets, stratified by category, including no-answer and adversarial cases. Grade with code first (sources, exact arguments), a judge only for tone and only once validated against human labels. Run repeated samples, gate each category in CI against a baseline, and monitor sampled production traffic. Every incident becomes a case (lesson 7.1).

**Take-homes and live exercises.** Time-box yourself to what the brief says. Put a README first: assumptions, what you tested, what you left out and why. Show failing-then-passing evidence. If an assistant is allowed, disclose it and be ready to explain every line; if it is not, do not use it. In a live session, think aloud, ask before assuming, and write the charter and a short summary of what you found.

**Your first 90 days.** Days 1 to 30: run the pipeline locally, read the last three escaped bugs, shadow a release, fix one flaky test or add one regression test, and write down what confused you. Days 31 to 60: own one risk area, review tests in pull requests, run an exploratory session. Days 61 to 90: pick one measured improvement (flake rate, time to feedback), present it, and agree next quarter's goal. See [*From Graduate to Hired*, lesson 6.2 — Your first 90 days: onboarding, the first pull request and asking good questions](../career/index.html#/6.2).

**Growth paths.** SDET to senior SDET to test architect or staff engineer is the technical path. Quality engineer to lead to engineering manager is the people path. AI quality runs from evaluation engineer to lead, close to AI governance. Sideways moves to reliability, security or performance engineering are possible ([*From Graduate to Hired*, lesson 6.3 — Growing from junior to mid-level: feedback, ownership and continuous learning](../career/index.html#/6.3)).

**Ethics.** Testing produces evidence other people stake money and safety on. Report what you tested and what you did not. Do not inflate coverage, hide retries or edit a failing test to green. If a release is unsafe, write the risk with evidence, tell the owner, ask the accountable person to accept it in writing and use the agreed escalation route. Never leak or sabotage. Knight Capital and Therac-25 (lesson 0.2) show what weak verification and release control can cost.

## 🧰 The toolkit
| Tool, practice or technique | What it is and does | When to reach for it |
|---|---|---|
| **ISTQB Certified Tester, Foundation Level** | A vendor-neutral certificate (CTFL v4.0) on testing vocabulary and process | When postings in your market ask for it |
| **Portfolio repository** | A public repo with a README that proves one claim | Before applying; one per target role |
| **Catch matrix** | Shows which suite catches which planted bug | The centrepiece of a portfolio README |
| **Eval harness** | A script that runs an AI feature, grades it and reports by category | Applying for AI quality roles |
| **Interview answer frame** | Clarify, rank risks, techniques, qualities, automate, not test, report | Any "how would you test…" question |

## 🏛️ In practice at Najm Bank
Rashid scores graduate quality-engineer interviews on the **Najm QE interview scorecard v1**. Candidates may use an assistant in the take-home if they say so and can explain every line.

| Criterion | Strong signal | Weak signal |
|---|---|---|
| Risk thinking | Asks who is hurt and how, then ranks | Lists every field equally |
| Test design | Partitions, boundaries and states with exact data | "Try different inputs" |
| Judging evidence | Asks what bug turns a test red; runs it | "It passes, so it is fine" |
| Automation craft | Stable locators, waits on conditions, isolated data | `sleep`, shared accounts |
| Honesty and communication | Says what is not covered and why | Oversells; hides gaps |

## 🛠️ Exercises
- 🟢 Fill the skills ladder for yourself: for each rung, link one piece of evidence you produced (a test, a report, a strategy) or write "gap". Name the role you want. *Done when:* the table has at least 12 skills, every row has a link or "gap", and your three biggest gaps name the lessons to redo.
- 🟡 Build portfolio project 1 and write its README with three CV bullets. *Done when:* the catch matrix shows 5 of 5 `NAJM_BUGS` caught against 2 of 5 for the starter suite, survivors are classed, and each bullet links to the evidence behind its numbers.
- 🔴 Hold a 45-minute mock interview with a peer: two "how would you test…" questions, the flaky-test question and the AI-test review, with the sample running. *Done when:* you switched `float_fee` on and off during the review, the peer completed the scorecard with a note per criterion, and you wrote three dated actions.

## ⚠️ Mistakes and traps
- **Listing tools instead of evidence.** Replace each tool with a result and a link.
- **Collecting certificates instead of building.** Take the exam your market asks for, then build the portfolio.
- **Quoting coverage.** Quote mutation score, catch rate or escaped defects, with how you measured them.
- **Hiding AI use, or hiding behind it.** Disclose it, and explain every line you submit.
- **Memorised answers.** Interviewers change the example. Use the frame.

## 🧾 Recap
- Roles overlap; read the work, not the title, and show the rung you can prove.
- Evidence beats keywords: a catch matrix, a mutation score, a trace, a report that names gaps.
- Certifications give vocabulary; their value varies by market and never replaces a portfolio.
- In interviews, clarify, rank risks, choose techniques, and say what you will not test.
- Your integrity is the product: report honestly and speak up about unsafe releases.

## ✍️ Check yourself

**1. A candidate says an AI-written test "passes, so it is fine". Its only assertion is that a 10,000 QAR international fee is 35.00. What is the strongest next step?**

- A. Approve it, because 35.00 matches the 0.35 % fee rule exactly
- B. Reject it, because assistants should never write tests for money code
- C. Run it with `float_fee` on and add a rounding tie like 3,090
- D. Ask for a coverage report before deciding either way

<details><summary>Answer</summary>

**C.** The float arithmetic lands exactly on 35.0, so the test passes with the bug on. A tie case can fail. A trusts a pass, B bans the tool instead of judging its output, and D measures execution, not checking. (🔴 Expert view.)

</details>

**2. Most postings you target never mention ISTQB, but one outsourcing firm on your list requires it. What is a sensible plan?**

- A. Build the portfolio now and sit the Foundation exam for that firm
- B. Take the Foundation exam first and start projects afterwards
- C. Skip every certificate, because they never matter anywhere
- D. Buy every Advanced module so your CV stands out

<details><summary>Answer</summary>

**A.** Value varies by market, so let your targets decide: take the exam for the firm that asks, and keep the portfolio as the proof. B delays the evidence, C is too absolute, and D spends money on modules nobody asked for. (🟡 Going deeper.)

</details>

**3. A Payments pipeline test fails about one run in ten. In an interview, which first move is strongest?**

- A. Add an automatic retry so the pipeline stays green for everyone
- B. Add a sleep before the failing step, then re-run until it passes
- C. Delete the test, since the other tests cover the same code
- D. Quarantine it with an owner and deadline, then find the cause

<details><summary>Answer</summary>

**D.** Quarantine protects the signal while you reproduce and fix the real cause. A and B hide the problem, which may be a real race, and C throws away coverage you do not understand. (🔴 Expert view.)

</details>

**4. Two days before launch, you find the schedule job can double-send when a retry races a timeout. The fix takes a week. The product owner asks you to log it as low risk. What do you do?**

- A. Log it as low risk now and mention your doubts to the team in conversation later
- B. Report the true severity with evidence; ask the owner to accept the risk in writing
- C. Post it in the company-wide channel so that the launch is forced to slip by a week
- D. Delete the release build from the registry so that nobody can ship it before the fix

<details><summary>Answer</summary>

**B.** Honest reporting plus a written, accountable decision is the proper route. A understates the risk, and C and D replace the agreed escalation with a unilateral act. (🔴 Expert view.)

</details>

**5. Which README opening gives a hiring manager the most evidence of your skill?**

- A. A badge showing 100% line coverage plus a long list of tools and versions
- B. A paragraph about how much you care about quality
- C. A before-and-after catch matrix, with the surviving mutants explained
- D. Screenshots of green runs from the last pipeline, one per job

<details><summary>Answer</summary>

**C.** It shows what your tests catch, how you measured it and what you left open. A and D are easy to produce without proving anything, and B is a claim, not evidence. (🟡 Going deeper.)

</details>

## 📚 References
- ISTQB, Certified Tester Foundation Level and the wider scheme: [istqb.org](https://www.istqb.org/)
- Playwright, trace viewer and CI: [playwright.dev](https://playwright.dev/)
- pytest documentation: [docs.pytest.org](https://docs.pytest.org/)
- promptfoo documentation, an open-source eval and red-team runner: [promptfoo.dev](https://www.promptfoo.dev/)

---

# 8.3 — Practice exam: 60 scenario questions
*Level: 🔴 Advanced* · *Prerequisites: Modules 0–8* · *Focus: Strategy*

## ⚡ In 60 seconds
- This is a 60-question practice exam covering every lesson from 0.1 to 8.2 and all nine modules. Most questions are scenarios set at Najm Bank. They are mixed, as in a real exam, rather than grouped by module.
- Take it in one sitting of about 90 minutes, which is 90 seconds a question. Closed book: no terminal, no search, no assistant. Write each answer and mark it "sure" or "guess" before you open any answer.
- Every answer ends with its focus and the lesson to review, for example *(Unit · 2.1)*. Your wrong answers are your study plan.
- Suggested reading of your score (the course's own guide, not a certification standard): 48 or more correct means you are ready to move on; 36 to 47 means review the lessons you missed; under 36 means work through the modules again, doing the exercises.
- Decision cue: for each miss, write down why the wrong option tempted you. That reason is the habit to fix.
- Biggest trap: checking each answer as you go, or retaking the exam the next day. Both measure memory, not judgement.

## 🧭 Why it matters
Before Nada's first-year review, Rashid asks her to sit the exam. She scores well on Unit and UI, and badly on Strategy and AI. "That matches your year," he says. "You wrote a lot of tests. You wrote one strategy page, and you trusted the first assistant-written test you saw." Her wrong answers have a pattern: when a suite looks weak she reaches for more tests or a higher coverage number, and when a model misbehaves she reaches for a better prompt.

Real work does not ask you to define a mutation score. It gives you a green suite, a flaky pipeline or a confident chatbot, and asks what you do next. Most wrong answers on a scenario exam are reasonable-sounding habits, which is why they are also the ones that ship bugs. The score matters less than the pattern of misses, and each miss points to the lesson that fixes it.

## 📐 How it works

### 🟢 Question styles
Four options, one defensible answer, no "all of the above". The questions come in five styles:
- **Decision:** what do you do next, or first, in this situation?
- **Diagnosis:** which cause or which defect explains this symptom?
- **Evidence:** which test, metric or report could fail, and so proves something?
- **Design:** which cases, techniques or level fit this rule?
- **Trade-off:** which gate, policy or release choice fits the risk?

### 🟡 Elimination
Read the last line first, then the scenario. Strike options that do not answer the question asked. Then watch for the shortcuts practitioners really take: add more tests, raise a coverage number, retry until green, add a `sleep`, fix the test instead of the code, trust a tool's verdict, or use an absolute word such as "always" where a lesson says it depends. Compare the last two against the scenario's specifics: the risk, the evidence and who owns the decision.

> *Scenario:* a mutation run on a new fee function leaves 12 survivors, all in the rounding branch. *Options, paraphrased:* raise the coverage gate; add a rounding-tie test; mark the survivors equivalent; lower the mutation gate. *Elimination:* the coverage gate measures execution, not checking; lowering the gate hides the gap; marking survivors equivalent skips the check. Only the tie test names a behaviour the suite does not yet test.

### 🔴 Scenario reading
Ask four things of every stem. **Who is hurt, and how?** (Money, privacy, an unconfirmed action, a missed regulatory file.) **What is the cheapest level that can fail for the right reason?** (A unit table, an API test, one journey.) **What changes because an AI wrote the code, or because the system is an AI?** (Judge evidence, grade by code first, check state.) **What word limits the answer?** ("First", "most likely", "before", "best".) Numbers matter: a 15:00 cut-off, a half-up tie, a 20-schedule cap. Do not assume facts the stem does not give.

The twelve focus tags map to the course like this. Use the table to tally your misses:

| Module | Lessons | Focus tags | Your misses |
|---|---|---|---|
| 0 Orientation | 0.1 to 0.3 | Mindset | |
| 1 Foundations | 1.1 to 1.3 | Mindset, Design | |
| 2 Testing code | 2.1 to 2.3 | Unit, Integration, Strategy | |
| 3 Interfaces | 3.1 to 3.3 | Integration, Security, UI, Design | |
| 4 Qualities | 4.1 to 4.3 | Performance, Security, Reliability, Integration | |
| 5 Strategy and delivery | 5.1 to 5.3 | Strategy, Delivery, Reliability, Design | |
| 6 AI and code | 6.1 to 6.3 | AI, Unit, Delivery, Strategy | |
| 7 Testing AI systems | 7.1 to 7.3 | AI, Delivery, Integration, Security | |
| 8 Hero | 8.1, 8.2 | Strategy, AI, Career | |

## 🧰 The toolkit
| Tool, practice or technique | What it is and does | When to reach for it |
|---|---|---|
| **Confidence marking** | Writing "sure" or "guess" beside each answer before checking | Every practice exam; it exposes lucky guesses and false certainty |
| **Miss log** | A table of each wrong or guessed answer with its focus, lesson and type of error | Straight after scoring; it becomes your study plan |

## 🏛️ In practice at Najm Bank
Rashid keeps one rule: no lesson with two or more misses is left without a dated action, and nobody retakes the exam before two weeks have passed. Three rows of Nada's **miss log** after her first sitting, as an example of the template:

| Question | Focus · lesson | My answer (confidence) | Type of error | Action and date |
|---|---|---|---|---|
| 14 | Strategy · 5.1 | A (sure) | Tempted: set a coverage target | Reread 5.1 🟡; redo the Goodhart exercise, Friday |
| 31 | AI · 7.1 | C (guess) | Did not know the judge-validation step | Reread 7.1 🟡; label 30 answers by hand |
| 47 | AI · 6.2 | B (sure) | Tempted: let the agent edit the failing test | Redo the 6.2 gate exercise; show the weakened test blocked |

Then she writes the plan from the pattern, not from single questions. A wrong "sure" goes first, because it is a belief she would act on at work.

| Focus tag | Misses | Reread | Redo | By |
|---|---|---|---|---|
| Strategy | 2 | 5.1 | The Goodhart table; a one-page strategy for the sample | Friday |
| AI | 3 | 6.2, 7.1 | The 6.2 gate; 30 hand labels for a judge | next Wednesday |
| Retake | | | The whole exam, closed book | in two weeks |

## 🛠️ Exercises
- 🟢 **Review your misses.** Tally every wrong or guessed question by focus tag in the table above and label each miss "did not know", "misread" or "tempted". *Done when:* you can name your two weakest focus tags and the habit behind each, and every miss has a lesson to reread.
- 🟡 **Write five questions of your own.** Choose your weakest focus. Write five scenarios in the exam's format, each with one defensible answer, three tempting wrong ones and an explanation that ends with its focus and lesson. *Done when:* a peer has answered all five, every disagreement is resolved in your explanation, and the correct option is not always the longest.
- 🔴 **Teach one lesson.** Teach the lesson behind your weakest tag to a peer in 20 minutes, with one failing-then-passing run on the sample system. *Done when:* the peer can state the lesson's main rule and one weak-versus-strong pair in their own words, and you have redone anything you could not answer.

## ⚠️ Mistakes and traps
- **Checking answers as you go.** You learn one answer and lose the measure of the rest. Answer all 60, then check.
- **Counting only the score.** A good score with many guesses hides gaps. Review guesses as if they were misses.
- **Rereading instead of practising.** An explanation fixes the answer; the lesson's exercise builds the judgement. Redo it.
- **Treating this as a certification mock.** It follows this course, not any syllabus or exam format. Use the issuer's own guides for a certificate (lesson 8.2).

## 🧾 Recap
- Sit the exam closed book in one go, and mark every answer "sure" or "guess".
- Read each stem for who is hurt, the cheapest level that can fail, what AI changes and the limiting word.
- Log every miss by focus, lesson and type of error: did not know, misread or tempted.
- Redo the exercises for your weakest lessons, then retake the exam after at least two weeks.

## ✍️ Practice exam

**1. Tariq's spec for Schedules computes every run date from the start date and moves a run that lands on a non-business day to the next business day, in Qatar. A weekly schedule starts on Thursday 4 February 2027, and Thursday 11 February is a bank holiday. Which pair gives the second and third run dates?**

- A. Sunday 14 February, then Thursday 18 February
- B. Sunday 14 February, then Sunday 21 February
- C. Monday 15 February, then Thursday 18 February
- D. Friday 12 February, then Thursday 18 February

<details><summary>Answer</summary>

**A.** The Qatar weekend is Friday and Saturday, so the holiday run rolls past both to Sunday 14 February, and the third run is computed from the start date (4 February plus 14 days), not from the moved date. B steps from the moved run, which is the drift bug; C treats Sunday as weekend; D forgets that Friday is weekend. *(Strategy · 8.1)*

</details>

**2. Bilal's Transfers tests call a sanctions-screening fake that always answers "clear", and they all pass. In production the screening service times out for ten minutes, and some transfers go through unscreened. Which test would have caught this?**

- A. A test where the fake reports a sanctioned name as a match, and the transfer is refused
- B. A schema check that the fake's reply has the same fields as the real service
- C. A test where the fake returns a 503 or times out, and the transfer is refused
- D. A test that the fake is called exactly once for each submitted transfer

<details><summary>Answer</summary>

**C.** A fake that always says "clear" tests only the happy path. Make it return a 503 or raise a timeout and assert that the transfer is refused and no money moves: fail closed. A match (A) is another reply the screening service gives, not a failure of it, a field comparison (B) catches drift but not an outage, and a call count (D) pins wiring, not behaviour under failure. *(Integration · 3.1)*

</details>

**3. Nada raises her open-model test of the balance endpoint from 400 to 600 requests per second on her laptop. The server dashboard still shows a p95 of 90 ms, but her generator reports a `lag` p99 above three seconds and its CPU is at 100 %. How should she read the run?**

- A. The server copes with 600 requests per second, because its own latency did not change
- B. The server's knee is at exactly 600 requests per second, so the capacity test is done
- C. The run is invalid as the tool could not send on schedule; add capacity and rerun it
- D. The lag is only a network effect between laptop and server, so it can be left out

<details><summary>Answer</summary>

**C.** When `lag` is high the generator could not send on schedule, so the numbers describe the tool, not the system. Add generator capacity (or lower the rate) and rerun, watching `lag` and the generator's CPU. A and B read a server limit into a test that never delivered 600 requests a second on time, and D waves away the evidence that the run is invalid. *(Performance · 4.1)*

</details>

**4. Maha wants to kill one screening pod on the live system at noon on Monday "to see what happens". Rashid asks her to hold off. What must the experiment have before it runs?**

- A. A steady-state metric, a hypothesis, a limited blast radius and an abort condition
- B. A quiet slot such as 3 a.m., with the whole squad on standby in case customers notice
- C. Alerts muted for the run, so that the on-call team sees the raw behaviour undisturbed
- D. A sign-off from every squad lead, so that nobody is surprised by what customers see

<details><summary>Answer</summary>

**A.** An experiment is a hypothesis, not a stunt: name the steady state with a metric (say, transfer success above 99.9 %), state what you expect, limit the blast radius (staging, or 1 % of traffic) and set abort conditions (stop if success is below 99 % for two minutes). A quiet hour (B) shrinks the damage but gives no way to stop or to learn, muted alerts (C) remove the monitoring the experiment relies on, and a sign-off (D) is not a control. *(Reliability · 4.3)*

</details>

**5. Nada fixes NAJM-101, the international fee that was a cent short, and adds one regression test: `fee("3090", "QAR", "international") == Decimal("10.82")`. Rashid says it is necessary but not enough. What should she add?**

- A. More half-cent amounts, such as 2,870, 2,990 and 3,110, with hand-worked fees
- B. An assertion that the fee for 3,090 is a `Decimal` that sits between 10.00 and 100.00
- C. Twenty more transfers at mid-range amounts such as 500 and 5,000
- D. A coverage report showing that every line of `fee()` is now run by the suite

<details><summary>Answer</summary>

**A.** The bug is a class of inputs (407 of the 25,000 whole-riyal amounts get a wrong fee), and one example guards one point. Hand-worked neighbours (10.05, 10.47 and 10.89) or a property test guard the class. B still passes with the bug, since 10.81 is a `Decimal` in range; C uses round amounts that never produce a half cent; D measures lines run, not values checked. *(Mindset · 0.2)*

</details>

**6. Two of Bilal's tests share one module-level `TransferService`. `test_first_transfer_gets_id_tr_0001` fails with `tr-0002` whenever `pytest-randomly` runs `test_fee_is_charged_once` before it, and passes in file order. What is the best fix?**

- A. Turn off the shuffling plugin, so that the tests always run in the order they were written
- B. Add `--reruns 2`, so that the failing test gets another chance in a luckier order
- C. Quarantine the failing test and leave it until somebody finds the time to look at it
- D. Replace the shared service with a fixture, so that each test builds its own fresh one

<details><summary>Answer</summary>

**D.** Both tests change the same service, so the first id depends on the order: shared mutable state. A fixture that builds a fresh service for each test removes the cause. Pinning the order (A) and reruns (B) hide it, and quarantine (C) is a parking place, with an owner and a deadline, for a flake you cannot yet fix; this one has a simple cure. *(Unit · 2.3)*

</details>

**7. Tariq's squad moves the international fee to binary floats, and `3090` QAR now returns `10.81` instead of `10.82`. Najm Mobile's pact only requires `fee` to be a string with two decimals, so provider verification stays green and `can-i-deploy` answers yes. What should Bilal conclude?**

- A. The pact is broken, so the consumer should regenerate it from the new provider build
- B. `can-i-deploy` cannot be trusted, so every release needs a full end-to-end run first
- C. The pact should list many example fees, so that every fee rule is checked there
- D. A contract proves shape, not value, so exact fees need unit and property tests

<details><summary>Answer</summary>

**D.** The provider's `10.81` has exactly the shape the consumer reads, so verification passes: a contract proves shape, not correctness. Exact fees belong to unit tests and an exact-oracle property test (lesson 2.3), which fail under the `float_fee` bug. Nothing in the pact is broken (A), dropping the gate (B) throws away what it does well, and C turns the pact into a rule suite. *(Integration · 2.2)*

</details>

**8. Dana's team halves the chunk size in Najm Assist's policy index to make search faster. The golden-set pass rate does not move, but Rashid asks for one more check before approval. Which check is the direct regression test for a chunking change?**

- A. The golden set again, ten more runs at temperature 0.8 to average out sampling noise
- B. Recall@k, precision@k and MRR on the labelled retrieval queries
- C. The population stability index on last week's topic mix of customer questions
- D. The red-team tests that plant a poisoned document in the index

<details><summary>Answer</summary>

**B.** Chunking decides what the retriever can find, so the lesson re-runs the retrieval metrics on labelled queries after any chunking change, which can reveal a right document sliding down the ranking before the final text shows it. A re-measures the final answers, C watches production drift, and D tests a different link in the chain. *(AI · 7.2)*

</details>

**9. Two of Nada's end-to-end tests each read `acc-1`'s balance through the API, send 100.00 from the page and assert that the balance fell by exactly 100.00. Each passes alone. With `--workers=4` they fail about one run in five. What is the likeliest cause, and the best fix?**

- A. A slow page; add `waitForTimeout(1000)` after the click so that the balance can settle
- B. Shared server data, as both tests move one account; assert on what each test owns
- C. Cookies shared between tests; clear the storage state before every assertion
- D. An unstable locator; let CI retry a failing test once before it reports a failure

<details><summary>Answer</summary>

**B.** Each test gets a fresh browser context, but the server's data is shared: two parallel tests moving money from `acc-1` change each other's balance. Assert only on what the test owns, such as its own transfer read by id, or start one app per worker. A sleep (A) guesses, and a retry (D) would hide the interference instead of removing it. *(UI · 3.2)*

</details>

**10. Bilal has one afternoon to automate one of four manual checks. By Najm's automation strategy, which check earns the afternoon?**

- A. The 14:59 and 15:00 cut-off check: a Deep area with a fixed rule, run on every build
- B. The statement PDF layout check: a fixed layout, run every release, in an area scored Smoke
- C. The Arabic transfer-form check: a Standard area, run every release, with a redesign next month
- D. The notification wording check: a Light area, run every release, judged by a native reader's ear

<details><summary>Answer</summary>

**A.** Automation pays back when a check is stable, high-risk, deterministic and run often, and the cut-off check is all four (cut-off is a Deep area). B is stable and repeatable but sits in a Smoke area, where one check at release is enough and upkeep is not worth paying; C is not stable, because a redesign next month would rewrite it; D is a judgement call that needs a person. *(Strategy · 5.1)*

</details>

**11. Amal asks for an end-to-end test that the page tells the customer when the Transfers API is down. The suite runs its tests in parallel on shared CI machines. Which approach is best?**

- A. Stop the API process during the CI run, then start it again once the test is done
- B. Leave it to a manual check, with someone stopping the API by hand before each release
- C. Add a long `waitForTimeout`, and hope that the slow server eventually times out
- D. Intercept the POST to the API with `page.route`, and fulfil it with a 503 response

<details><summary>Answer</summary>

**D.** `page.route` reaches a state that is slow or risky to create for real, and it affects only this test, so the parallel tests are untouched. Stopping the API (A) breaks every test running at that moment, a manual check (B) is the outage nobody automates and so nobody re-tests, and waiting for a timeout (C) is a guess. *(UI · 3.2)*

</details>

**12. Bilal's CI starts running tests in random order. A test that reads back a transfer made by the previous test now fails about half the time. Both share a module-level `SERVICE = TransferService()`. What is the right fix?**

- A. Pin the order in CI so the first test always runs before the second
- B. Rerun failures twice and count the build as green once a rerun passes
- C. Add a one-second sleep at the start of the second test, so the first can finish
- D. Build the service in a fixture so each test arranges its own data

<details><summary>Answer</summary>

**D.** Shared mutable state makes results depend on order, and the second test silently relies on the first. A fixture that builds what each test needs makes the tests isolated, so any order works. A hides the dependency, B hides the flake behind retries, and a sleep (C) has nothing to wait for. *(Unit · 2.1)*

</details>

**13. The rules of Najm Plus change almost every week. Rashid wants useful coverage without rewriting scripts after each change. Which approach fits best?**

- A. A short checklist of conditions, plus a time-boxed charter to explore each week's changes
- B. Fully scripted test cases with exact steps and data for every rule, kept for audit
- C. A large automated end-to-end suite covering every screen of the offer
- D. No test design until the rules stop changing, so nothing is rewritten

<details><summary>Answer</summary>

**A.** Scripts cost effort to write and to keep current, so a feature that changes weekly is better served by a checklist and a charter, which are cheaper to maintain and still cover the risks. B pays the rewrite cost every week, C is the heaviest thing to keep in step, and D leaves the offer untested while customers use it. *(Design · 1.3)*

</details>

**14. Two vendors each claim their AI assistant writes "high quality" tests, and Bilal can run both against the course's sample system. How should he compare them?**

- A. Pick the assistant whose generated suite reports the higher line and branch coverage
- B. Pick the assistant that generates more tests in the same amount of time
- C. Ask each assistant to grade its own tests and pick the higher score
- D. Run each suite once per seeded bug, switched on alone, and count the bugs caught

<details><summary>Answer</summary>

**D.** The bug-catch score measures a suite by what it catches: switch each seeded bug on by itself, run the suite, and count the runs that go red. It works the same for a human's tests or a tool's (after checking that each suite passes with no bug on). A and B measure activity, not the ability to fail, and C lets each tool mark its own work. *(Mindset · 0.3)*

</details>

**15. Nada's twelve `TransferDesk` tests each assert `service.submit.assert_called_once_with("alice", REQ, "k1", None)` on a `Mock` service. A refactor makes the desk read the clock itself and pass the current time as the fourth argument instead of `None`. Behaviour is unchanged, yet all twelve fail. Which change fixes the cause?**

- A. Loosen each assertion to `assert_called()` so the arguments no longer matter
- B. Use a fake or real `TransferService` and assert the balance and the transfer's status
- C. Add `autospec=True` to the mock so the call is checked against the real signature
- D. Update the twelve expected calls whenever a refactor changes the arguments

<details><summary>Answer</summary>

**B.** The tests assert interactions, so they pin how the desk is wired, not what it promises. State assertions on a real or fake service describe the promise (money moved, status accepted), survive refactors and also run the limit rules. A and C still pin the wiring, and D accepts the churn for ever. Keep spies and mocks for edges such as SMS. *(Unit · 2.1)*

</details>

**16. Najm Assist passes 21 of 24 on its English golden set, and no category has fallen below its baseline. Hessa asks the same three core questions in Arabic and Assist declines all three, because the retriever ignores non-Latin words. Which practice would have shown this before she did?**

- A. Gating each topic category against its baseline, with a floor for safety categories
- B. Putting an Arabic greeting before every passing golden question and requiring a correct answer or a decline
- C. Comparing the candidate release with the old one case by case on the golden set
- D. Reporting pass rates by language slice, with intervals, each release

<details><summary>Answer</summary>

**D.** Averages hide unequal service, and an Arabic slice would have shown 0 of 3 even though declining is the safe failure. A and C re-measure the same English cases, and B keeps the English question inside the prompt: the retriever ignores non-Latin words, so an Arabic prefix costs nothing and the case still passes. *(AI · 7.3)*

</details>

**17. An agent turns every visible test green for Najm's new fee-rounding module. Rashid worries that it may have memorised the visible examples, and these are money rules. Which extra control best exposes memorising?**

- A. Put the visible tests under CODEOWNERS review, so that the agent cannot edit them
- B. Keep a held-out set of money-rule tests in CI, which the agent never gets to see
- C. Require 100% line coverage on the new module before the pull request can merge
- D. Make the agent paste the last line of every command's output into its final message

<details><summary>Answer</summary>

**B.** Tests the agent can read can be memorised; a held-out set that fails where the visible tests pass shows overfitting, and it is worth reserving for money and regulatory rules. A stops edits, not memorising, since the agent can copy answers without touching a test; C measures what ran, and a lookup table of the visible answers runs every line; D shows that the visible tests passed, which was never in doubt. *(AI · 6.2)*

</details>

**18. Hessa asks Nada for 3-value boundary tests of the daily limit, using a 12,000.00 QAR transfer. The limit is 50,000.00 QAR. Which "sent today" values, with expected results, are right?**

- A. 49,999.99 accepted, 50,000.00 accepted, 50,000.01 rejected
- B. 37,999.99 accepted, 38,000.00 rejected, 38,000.01 rejected
- C. 24,999.99 accepted, 25,000.00 accepted, 25,000.01 rejected
- D. 37,999.99 accepted, 38,000.00 accepted, 38,000.01 rejected

<details><summary>Answer</summary>

**D.** The limit applies to the total, sent today plus the new amount. 38,000.00 plus 12,000.00 lands exactly on 50,000.00, which is allowed; one cent more is not. A puts the boundary on the "sent today" value itself, B rejects a total that merely meets the limit (the `limit_off_by_one` behaviour), and C uses the per-transfer maximum. *(Design · 1.2)*

</details>

**19. Najm's Payments squad publishes a partner API that dozens of outside apps call, and Najm cannot identify most of them. The squad wants early warning when a release breaks the response shape. Which approach is practical?**

- A. Consumer-driven Pact tests, with every outside app publishing pacts to a Najm broker
- B. End-to-end tests that drive each partner app against every new release
- C. A JSON Schema or OpenAPI check that every response keeps the published shape and types
- D. Unit tests of the provider's internal model classes after each release

<details><summary>Answer</summary>

**C.** With unknown consumers there is nobody to write pacts, and a schema or OpenAPI check on the published shape is simple and catches a renamed or retyped field. A needs known consumers who publish pacts, B cannot be run for apps Najm cannot identify, and D tests the provider's own idea of its shape, which stays green when a field is renamed. *(Integration · 2.2)*

</details>

**20. Bilal's regression suite for Transfers has run unchanged and green for eighteen months, yet support keeps logging rounding and cut-off complaints. What is the most useful next step?**

- A. Add more tests of the same mid-range kind, so the suite grows by a third
- B. Review recent escapes and add new cases for rounding and time
- C. Run the suite every night instead of every week, so problems show sooner
- D. Raise the coverage threshold until `transfers.py` is at 100 percent

<details><summary>Answer</summary>

**B.** Tests wear out: the same tests, run again and again, stop finding new defects, and defects cluster where the complaints point (rounding and time). Refresh the suite around those areas. A repeats the pattern that already misses them, C reruns the same checks more often, and D measures execution, not checking. *(Mindset · 1.1)*

</details>

**21. A full mutation run on the payments service takes forty minutes, and pull requests are waiting for it. What policy fits best?**

- A. Mutate only the code a pull request changes; run everything nightly
- B. Drop mutation testing for a coverage threshold, since both measure test quality
- C. Run the full mutation set once a quarter, just before each audit review
- D. Keep full runs on every pull request, but stop each run after ten minutes

<details><summary>Answer</summary>

**A.** Mutation testing is costly, so it runs on changed code for each pull request (select mutants by name, or narrow the files) and in full overnight. B swaps a measure of execution for a measure of checking, C finds weak tests months late, and D leaves whichever mutants come last unjudged. *(Strategy · 2.3)*

</details>

**22. Three weeks ago Nada quarantined a browser test that failed about one run in eight, with a 14-day deadline. Her flake gate now reports the quarantine expired, and nobody has looked at the test since. What does Najm's flaky-test policy want next?**

- A. Renew the entry automatically for another 14 days, so that the gate stays quiet
- B. Check whether the test is right, then fix it or renew the quarantine in a reviewed change
- C. Raise the quarantine job's retries to three, so that the test stops looking flaky
- D. Switch the gate to warning-only, since a stale entry should not hold up other merges

<details><summary>Answer</summary>

**B.** A quarantine has an owner and a deadline so that it cannot become a graveyard: when the deadline passes the gate stays red until someone fixes the test or renews the quarantine in a reviewed change. First ask whether the test is flaky or right, because it may be reporting a real race. A, C and D keep the problem hidden or the gate quiet. *(Delivery · 5.2)*

</details>

**23. Maha's canary for a new Najm Mobile API build has served 1,600 requests, with 8 errors and a p95 of 330 ms. The stable version has 40 errors in 40,000 requests and a p95 of 310 ms. What does Najm's `canary_verdict` return with its default settings?**

- A. Wait, because 1,600 requests is still too few for the judge to decide anything
- B. Promote, because the p95 of 330 ms is only a little above the stable 310 ms
- C. Promote, because 8 errors is only a very small count in absolute terms
- D. Roll back, because the error rate is too far above the stable error rate

<details><summary>Answer</summary>

**D.** The defaults wait below 1,500 requests, roll back if the canary's error rate is more than 0.2 percentage points above stable or its p95 is more than 20% above, and otherwise promote. The canary's rate is 8 ÷ 1,600 = 0.50%, against a limit of 0.10% + 0.2 points = 0.30%, so it rolls back. A fails because 1,600 is above the 1,500 minimum; B checks only the latency rule, which passes (330 ms is under 372 ms) but cannot offset the error rule; C judges a count instead of a rate. *(Delivery · 5.2)*

</details>

**24. Rania's team moves Najm Assist to a cheaper model version. Averaged over ten runs on each version, the golden set scores 18 of 24 before and 18 of 24 after, and the team calls the change neutral. Rashid asks for one thing before approval. What is it?**

- A. A cost report showing the saving per 1,000 questions, since accuracy is equal
- B. A per-case comparison listing every case that passed before and fails now
- C. Ten more runs of the new version alone, to confirm that its 18 is stable
- D. A ROUGE score between the old and new answers, to show that they are similar

<details><summary>Answer</summary>

**B.** Equal totals can hide different failures, so differential testing compares cases, not totals, and a floor on a safety category would block a flipped privacy case. A and C ignore which cases moved (the ten runs on each side already average out the sampling noise), and D scores wording similarity, a weak proxy for quality. *(AI · 7.3)*

</details>

**25. Amal runs a 25-minute example-mapping session with the product owner and a developer on the story "a customer can schedule a transfer for a future date". The wall ends with two rules, four green examples and five red cards, such as "Which day's daily limit does it count against?" and "What if the balance is short on the day?". Nobody in the room can answer them, and each would change what the developer builds. What should the team do?**

- A. Treat the story as not ready, and get each red card answered by the owner of that rule
- B. Let the developer start on the green examples, and settle the red cards in testing
- C. Have Nada write Gherkin for each red card, assuming the most likely answer
- D. Book a second session to add more green examples to the two existing rules

<details><summary>Answer</summary>

**A.** A story is ready when each rule has an example and no open question blocks it, so five unanswered red cards that change what gets built mean it is not ready; the answers come from the people who own the rules, and each becomes a green example. B builds on guesses (the `limit_off_by_one` story in the lesson began exactly like this), C is Gherkin written alone, and D adds examples while the questions stay open. *(Design · 5.3)*

</details>

**26. Bilal asks an agent to make `tests/test_value_dates_spec.py` pass without editing any test; its rows come from a table the product owner signed. The pull request arrives with one spec row changed so that "Sunday 15:00" expects Tuesday, and the description says "the spec looked wrong". CI is green. As the Quality Engineering code owner, what should Rashid do?**

- A. Approve, because the agent gave a written reason and the whole suite is also green
- B. Approve if the mutation score of the changed module stays above the 80% gate
- C. Check the row against the signed table, then send the agent back to fix the code
- D. Delete the disputed row, so that the agent cannot lean on one contested example

<details><summary>Answer</summary>

**C.** The tests are the specification, and the agent may not edit what judges it; a human compares the row with the signed table, and if the table itself is wrong a human fixes it first. A trusts a claim, B scores the already weakened tests, and D shrinks the specification. *(Delivery · 6.2)*

</details>

**27. After a refactor, the nightly load test of `POST /transfers` shows p95 falling from 240 ms to 45 ms. The report lists only latency percentiles, and its one threshold, p95 under 300 ms, is green. Rashid asks Nada what else she checked before announcing the win. Which check matters most?**

- A. The mean latency, because the mean is steadier than a percentile from one run to the next
- B. The think time, so that the p95 threshold can be tightened to match the new figure
- C. The error rate and status codes, because failed requests can come back very quickly
- D. Nothing more, because a p95 well under the threshold means the change is safe

<details><summary>Answer</summary>

**C.** Latency means little beside errors: a server that answers every request with a 5xx in a few milliseconds looks fast, so the statuses and the error rate come first. The mean (A) hides the slow tail, tightening the threshold (B) builds on a figure nobody has trusted yet, and D ships on one number. *(Performance · 4.1)*

</details>

**28. In an interview, Rashid asks a candidate: "How would you test a transfer form?" She starts listing test cases for every field in turn. Which approach better follows the interview frame?**

- A. Ask who uses the form and what rules apply, rank the risks, then choose techniques
- B. Name the Playwright journeys she would automate first, then add field checks later
- C. Apply partitions and boundaries to every field first, then rank the risks that the cases reveal
- D. Say she would try many different inputs and see whether anything breaks

<details><summary>Answer</summary>

**A.** The frame starts by clarifying and ranking risks (wrong money, duplicates, another customer's account) before techniques, and the scorecard marks "lists every field equally" as a weak signal. B automates before ranking, C picks techniques before any risk is ranked and so treats every field alike, and D is the scorecard's weak "try different inputs". *(Career · 8.2)*

</details>

**29. Bilal's gate asks for an 80% mutation score on changed money code. A new fee module scores 94%, six mutants survive and nobody has looked at them yet. Tariq asks for 100% before merge. What should Rashid recommend?**

- A. Add a test for each survivor until the score reaches 100%, however artificial it is
- B. Raise the gate to 100% on all money code, so that the score cannot be argued
- C. Mark all six survivors as equivalent mutants, so that the report shows 100%
- D. Keep the 80% gate, and let a human triage each survivor as a gap or equivalent

<details><summary>Answer</summary>

**D.** Some mutants are equivalent (they change nothing observable), so 100% is often unreachable and chasing it invites silly tests. A human triages each survivor: a real gap gets a test, an equivalent mutant is accepted. A and B chase the number, and C accepts the survivors without checking them. *(AI · 6.2)*

</details>

**30. Najm keeps old app versions working for months. Tariq's squad makes `kind` a required field of `POST /transfers` and updates the OpenAPI document. Every current test and the nightly Schemathesis run pass. Two weeks later, customers on the oldest app see errors. Which test would have caught this before release?**

- A. A nightly Schemathesis run with a larger value for `--max-examples`
- B. A strict response schema, with `additionalProperties: false`, for every transfer
- C. A saved request from the old app, without `kind`, that must still return 201
- D. An authorisation matrix with one row for each route and each role

<details><summary>Answer</summary>

**C.** Old apps keep sending the old request, so a fixture from the old client, a request without `kind`, must still return 201 with every old response field. Schemathesis (A) checks the API against the new document, which says `kind` is required, so a refusal of a request without it looks correct. A strict response schema (B) catches leaked or extra fields, and the matrix (D) checks who may do what. *(Integration · 3.1)*

</details>

**31. Tariq's squad wants to release Najm Mobile's new transfer flow to every Android user at once. "If it breaks, we roll back like the web app," he says. What should Amal's release gate require instead?**

- A. A store rollback plan, since both stores can withdraw a build within a few minutes
- B. A staged rollout of 1%, 5%, 20% and 100%, with a halt rule and a remote kill switch
- C. Two extra regression runs on emulators, because they give the same results as devices
- D. A one-week beta on the newest phone, then a full release if no crash is reported

<details><summary>Answer</summary>

**B.** A mobile release has no rollback button: stores review builds and users update when they choose. So release in stages, halt if crash-free sessions or transfer success fall below baseline, and keep a server-side kill switch for risky features. A relies on a rollback that does not exist, C trusts emulators that miss radios, interruptions and real speed, and D tests only the newest phone, not the oldest supported OS. *(UI · 3.3)*

</details>

**32. Release 2026.10 has every Deep area green, but one Sev2 is still open: the Arabic transfer form misaligns on small screens. Tariq wants to ship on Monday as planned. Under Najm's exit criteria, what has to happen first?**

- A. QE holds the release until the defect is fixed, because exit criteria work as a veto
- B. The defect is relabelled Sev3 so that the exit criteria can be met by Monday
- C. A named owner accepts the open Sev2 in writing, and it is recorded as accepted
- D. Nothing more, because every Deep area is green and the defect is only cosmetic

<details><summary>Answer</summary>

**C.** Exit criteria are evidence, not a date: an open Sev1 or Sev2 needs a named owner's written acceptance, and the release dashboard lists it with an expiry date. A turns QE into a gatekeeper, and gatekeepers get bypassed; B games the severity scale; D forgets that the criteria cover every open Sev1 or Sev2, not only the Deep areas. *(Strategy · 5.1)*

</details>

**33. In Hessa's Schedules eval, Najm Assist creates a schedule for 50 QAR instead of 500 QAR in 2 of 12 Arabic requests that write the amount as "٥٠٠". Which fix can the team test reliably?**

- A. Tell the model in the prompt to write amounts in Western digits, then rerun the eval ten times at temperature 0.8 and compare the rates with intervals
- B. Add three Arabic examples to the prompt and rerun the 12 requests at temperature 0, shipping if all of them pass
- C. Ask a validated judge model to grade whether each summary shown to the customer has the right amount
- D. Convert the digits in code, unit-test that "٥٠٠" gives 500 and let the tool re-check the rules

<details><summary>Answer</summary>

**D.** Code, not the model, should turn Arabic-Indic digits into a number: a function takes exact unit tests, and the tool enforces the rules itself. A and B still leave the reading to the model, so they can only estimate a failure rate, and 12 requests are too few to show that it is gone; C uses a judge to grade what code can compare. *(AI · 8.1)*

</details>

**34. Nada writes a test asserting that the international fee is always between 10.00 and 100.00, and runs it on 1,000 random amounts. With `float_fee` switched on it still passes. What does this show?**

- A. A range check is a partial oracle, so it needs exact hand-worked fees beside it
- B. The sample was too small, since a run of 100,000 random amounts would have caught it
- C. Range assertions are invalid, because they do not come from a requirement
- D. The test is sound, because a fee of 10.81 is within the published limits

<details><summary>Answer</summary>

**A.** A partial oracle states a property that must hold; it is cheap but catches fewer bugs, and 10.81 is in range, so it passes however many amounts are tried. An exact expected value from the fee rule (3,090 gives 10.82) is what fails with the bug on. B treats volume as the cure, C is wrong because the 10.00 minimum and 100.00 cap are policy, and D mistakes "passes" for "correct". *(Mindset · 1.1)*

</details>

**35. Tariq's squad ships a statement export that matches its specification exactly: a CSV with six columns. Customers still cannot reconcile their accounts, because nobody asked for the value date. Which statement is accurate?**

- A. Verification failed, because the export lacks a column that customers need
- B. Both passed, because an export that matches its specification is correct
- C. Verification passed and validation failed: the spec was met, the need was not
- D. Neither applies, because a missing requirement is a product issue, not testing

<details><summary>Answer</summary>

**C.** Verification asks whether the product matches its specification ("are we building it right?"); validation asks whether it meets the real need ("are we building the right thing?"). The export passes the first and fails the second. A blames the build for a gap in the spec, B treats the specification as if it were the need, and D forgets that testers also challenge requirements. *(Mindset · 0.1)*

</details>

**36. Amal files one report: double-tapping Send debits the account twice, and the Arabic confirmation page shows an English rule code. Tariq's squad can fix the second today, but the first needs a design change. What should happen?**

- A. Keep one report, so the squad sees everything about that screen together
- B. Raise the combined report to S1, because it contains a money defect
- C. Split it into two reports, each with its own severity, owner and retest
- D. Return it unfiled until Amal finds one root cause shared by both problems

<details><summary>Answer</summary>

**C.** One defect per report: a report holding two bugs cannot be closed cleanly, and each bug needs its own severity (the double debit is S1; the wording is minor), owner and retest. A leaves a ticket the squad can never close, B inflates the severity of the cosmetic half, and D delays a fix that is ready today for a link that may not exist. *(Mindset · 1.3)*

</details>

**37. Tariq's squad adds a limit of 10 transfers a minute per customer. Their test sends 11 requests as Alice and asserts a 429 on the 11th, and it passes. Then Mariam's red team rotates the `X-Forwarded-For` header and gets 50 transfers through. Which test would have caught this?**

- A. Alice sends 11 requests as `X-Forwarded-For` changes; the counter must not reset
- B. A load test at 1,000 requests a second, to confirm the limiter holds under pressure
- C. A test that sleeps for 60 seconds, then checks that Alice can send again
- D. A test that Bob stays unaffected while Alice is being limited by the rate limit

<details><summary>Answer</summary>

**A.** The control has to hold against a client that lies, so the test changes a header the client controls and checks that the counter does not reset. B tests load, not a bypass; C checks the wait (and should use an injected clock, not a sleep); D checks fairness between customers. All are worth having, but only A would have caught this. *(Security · 4.2)*

</details>

**38. Mariam's red team tunes a guardrail on the QA copy of Najm Assist until all 40 attack prompts are refused, and the adversarial set holds nothing else. Tariq wants to call the work done. What does the set still lack to be balanced?**

- A. Another 40 attack prompts copied from public lists, to confirm that the guardrail holds
- B. Benign requests that sound alarming, like freezing a stolen card, that must be answered
- C. A run of the same 40 attacks against production, to confirm that the QA result is real
- D. Ten repeated runs of the same 40 attacks, to confirm that the refusals are stable

<details><summary>Answer</summary>

**B.** A guardrail tuned only to block attacks starts refusing real customers, so over-refusal cases sit beside the attacks and both rates are tracked. A adds more of the same kind of case, which adds volume but no balance, C breaks the rules of engagement (the QA copy, never production), and D proves the refusals are stable but not that the balance is right. *(AI · 7.3)*

</details>

**39. Tariq's squad has fast unit tests, BDD scenarios for the business rules, and load and security tests every month. Rashid maps them onto the agile testing quadrants and finds one quadrant empty. Which kind of testing is the squad missing?**

- A. Technology-facing tests that support the team
- B. Business-facing tests that support the team
- C. Business-facing tests that critique the product
- D. Technology-facing tests that critique the product

<details><summary>Answer</summary>

**C.** Unit tests are Q1 (technology-facing, support the team), BDD examples Q2 (business-facing, support the team) and load and security tests Q4 (technology-facing, critique the product). The empty quadrant is Q3, where people examine the product from the business's side through exploratory sessions, usability sessions and UAT, and find what nobody predicted. A, B and D are quadrants the squad already fills. *(Strategy · 5.3)*

</details>

**40. An agent writes a daily-limit change and its six tests in one pull request. Bilal notices that the product owner's rule says a day's total of exactly 50,000.00 QAR is allowed, yet the agent's `>=` check and all six of its tests treat exactly 50,000.00 as over the limit. The suite is green. What is the best next step?**

- A. Ask a second model to review the code and the tests, and merge if it agrees
- B. Run mutation testing on the function, and merge if its score clears the 80% gate
- C. Raise line coverage of the function to 100%, so that every branch is known to run
- D. Take the expected values from the product rule, in a boundary table a human approves

<details><summary>Answer</summary>

**D.** Tests written by the agent that wrote the code restate its belief, so they cannot disagree with it; ask where each expected value came from and rebuild them from the rule. A second model's errors can correlate with the author's, coverage measures what ran, not what was checked, and a mutation score can look healthy here because mirror tests fail the moment the code changes: it shows that tests can fail, not that their expected values are right. *(AI · 6.1)*

</details>

**41. For three weeks Bilal polishes the Najm Assist prompt against the same 24 golden cases, and the pass rate climbs from 75% to 96%. Rashid asks whether customers will see that gain. What is the best next step?**

- A. Ship the prompt, because a 21-point rise is far larger than any sampling noise
- B. Rerun the same 24 cases ten times at temperature 0.8 and ship if the average holds
- C. Switch to a judge model, which grades more kindly than contains checks
- D. Score it on a held-out slice that nobody tuned against and compare the rates

<details><summary>Answer</summary>

**D.** After repeated tuning on the same cases the score measures memory, and only a slice nobody polished against shows whether the gain carries over to new questions. A treats the tuned score as evidence, B repeats the same questions so it removes noise but not overfitting, and C changes the grader to chase a higher number. *(Delivery · 7.1)*

</details>

**42. Rania's team runs the 24-case Najm Assist golden set ten times at temperature 0.8 and gets 216 passes in 240 results, 90%. The report prints a 95% interval of about 86% to 93% over all 240 results, and Rania wants to ship on it. What is wrong with that reading?**

- A. The 240 results rest on only 24 questions, so the interval is too narrow; add cases
- B. Ten runs are too few, so a hundred runs of the same set would make the interval trustworthy
- C. Intervals do not apply to a model that samples, so the best single run should be reported
- D. Temperature 0.8 is too high, so one run at temperature 0 would give a trustworthy figure

<details><summary>Answer</summary>

**A.** Repeating the same questions averages out sampling noise but adds no new questions, so 240 results overstate what 24 questions can show; only more cases tighten the interval. B repeats the same mistake with more runs, C picks the luckiest draw, and D still leaves one run on 24 questions (hosted models can vary even at temperature 0). *(AI · 7.1)*

</details>

**43. Dana notices that Najm Assist's LLM judge gives higher scores to longer replies, even when a short reply states the same correct fact. Which fix matches this bias?**

- A. Run each comparison in both orders and average the two verdicts
- B. Use a judge from a different model family than the one that wrote the replies
- C. Tell the judge to ignore length, then check its scores against length
- D. Set the judge's temperature to 0 so that its scores stop varying between reruns

<details><summary>Answer</summary>

**C.** This is verbosity bias, and the lesson's remedy is a rubric line that says to ignore length, followed by a check of the scores against reply length. A fixes position bias and B fixes self-preference, which are real judge biases but not this one; D makes the bias repeatable instead of removing it. *(AI · 7.1)*

</details>

**44. Maha's team adds a synthetic transfer check that runs against production every 15 minutes. So that it also runs on laptops, Nada writes `baseURL: process.env.BASE_URL ?? 'https://staging.najm.example'`. What is the right fix?**

- A. Leave it: a default keeps the check running, and staging is built from the same code
- B. Default to the production URL, so that the check always watches what matters
- C. Keep the default and add a comment asking people to set `BASE_URL` in every job
- D. Remove the default, so a missing value fails instead of testing the wrong system

<details><summary>Answer</summary>

**D.** If the scheduler job ever loses `BASE_URL`, the default makes the check pass against staging while production goes unwatched. The URL should come from configuration with no default. B would send a check that moves real money from every laptop, and C relies on people reading a comment. *(Reliability · 5.2)*

</details>

**45. Hessa's Arabic page passed translation review, a clean axe scan and Amal's mirroring checks. Then a customer in Doha types `250,50` into Amount and sees a bare `error`, and another types `٢٥٠٫٥٠` with the same result. Which test idea would have found this kind of bug?**

- A. Pseudo-localising the catalogue, so that every string is longer and wrapped in square brackets
- B. Typing amounts as Arabic and German keyboards do, and checking they are accepted or explained
- C. Measuring bounding boxes, so that labels are shown to start at the right-hand screen edge
- D. A native speaker reading the Arabic error messages, so that their wording is reviewed

<details><summary>Answer</summary>

**B.** Translation, a rule scan and mirroring checks say nothing about how the field treats numbers typed in other formats: Arabic-Indic digits, the Arabic decimal comma, a comma as the decimal separator. Type amounts the way those keyboards produce them and assert they are accepted or the customer gets a clear message. Pseudo-localisation (A) finds hard-coded text, bounding boxes (C) check mirroring, and a reviewer (D) judges wording, not input handling. *(UI · 3.3)*

</details>

**46. Bilal's CI rejects added `pytest.mark.skip` lines in `tests/`. The team now lets Playwright's healer agent repair failing browser tests in `e2e/`. One healer pull request turns four red tests green and the check passes. What should Bilal change?**

- A. Extend the skip check to `test.skip` and `test.fixme`, and review healer edits
- B. Switch the healer off, since an AI tool should never touch a test file
- C. Ask the healer to attach a screenshot of each repaired page to its pull request
- D. Raise the retries in the Playwright config so that the repaired tests stay green

<details><summary>Answer</summary>

**A.** The healer may change assertions or park a failing test with `test.fixme()`, a skip by another name, and a check written for pytest never sees it; its edits need the lesson 6.2 controls (code owners and diff checks). B bans a useful tool, C adds evidence nobody checks, and D hides flakiness. *(AI · 6.3)*

</details>

**47. Maha proposes holding Schedules at each canary step for a full month, so that a monthly run is seen in production before the flag widens. Rashid wants a faster plan that is still safe. Which is best?**

- A. Skip the canary, because clock-injected date tests already prove that the whole feature works in production
- B. Move the canary servers' clock a month ahead, so that the monthly run fires early for those customers
- C. Prove the calendar with injected clocks, then hold each step for one batch, one cut-off and one nightly check
- D. Hold each step for one week, because weekly schedules exercise the same month-end logic as monthly ones

<details><summary>Answer</summary>

**C.** A canary cannot wait a month, so injected clocks prove the calendar before release and production confirms the daily mechanics: one 06:00 batch, one 15:00 cut-off and the nightly run-exists query. A drops that check on real batches, B tampers with production time, and D never reaches the month-end clamping that monthly runs need. *(Strategy · 8.1)*

</details>

**48. Nada reviews an agent's pull request called "Normalise amounts". It deletes the validation that refuses an amount with more decimal places than the currency allows, and quietly rounds the amount with `quantize` instead. All 24 starter tests still pass. Which new test would fail on this change and pass on the original code?**

- A. A transfer of `0.50` QAR is refused as `below_minimum`
- B. A transfer of `10.005` QAR is refused as `too_many_decimals`
- C. A transfer of `25000.01` QAR is refused as `above_per_transfer_max`
- D. A `1000.01` QAR transfer after `49000.00` today is refused as `daily_limit_exceeded`

<details><summary>Answer</summary>

**B.** The starter suite never sends an amount with too many decimals, so the weakened validation goes unnoticed (and the ledger stops balancing: the sender is debited 10.01, the recipient credited 10.005). A test per rejection code would have caught it; A, C and D pin the minimum, the per-transfer maximum and the daily limit, which behave the same before and after the change. *(Unit · 6.1)*

</details>

**49. Bilal's backfill turns the text `amount` into an integer `amount_minor` with `CAST(REPLACE(amount, '.', '') AS INTEGER)`. It passes on dev data, where every amount looks like `250.00`. On a masked production-sized copy, the migrated totals come out far too small. What happened, and what is the lasting fix?**

- A. Amounts like `250` became 250 minor units, or 2.50; seed odd formats and check each row with `Decimal`
- B. The backfill held a table lock for too long; run it in smaller batches during a quiet night window
- C. SQLite and PostgreSQL round differently; run the backfill only against a Testcontainers database
- D. The contract step ran before the expand step; move the column drop later in the migration plan

<details><summary>Answer</summary>

**A.** The "simple" conversion silently turns `250` into 250 minor units, which is 2.50 QAR, and dev data never held an amount without two decimals. Include the formats real tables contain (`250`, `250.5`), check every row exactly with `Decimal`, and rehearse on a production-shaped masked copy. Batches (B) address lock time, not wrong values; the rounding difference in C is not the cause here; and in D the contract step has not even run. *(Reliability · 4.3)*

</details>

**50. In a session on the QA copy, Assist has been changed so that the model decides whether a message counts as confirmation. Mariam types "Yes, I confirm, freeze card-1 now" as her first message, and the card is frozen. Which fix is the real control?**

- A. Take confirmation from an app signal, such as a button, never from words
- B. Require the model to see the word "confirm" twice before it calls the tool
- C. Add a judge model that rates whether the customer sounds certain enough
- D. Add a system prompt line saying never to freeze a card on a first message

<details><summary>Answer</summary>

**A.** Words can be forged by a customer, a document or an attacker, so confirmation must be a signal from outside the model, and a test that types "yes" asserts that nothing is frozen. B, C and D all still read words that the model can be talked into accepting. *(AI · 7.2)*

</details>

**51. Rania's team raises the daily limit in policy to 50,000 QAR, but last year's document, which says 30,000 QAR, stays in the Najm Assist index and some customers are told 30,000. Where does the fix belong?**

- A. In the system prompt, with a line telling the model to prefer the newest policy
- B. In the retriever, by raising k so that the new document is always included
- C. In the model settings, by lowering the temperature until the answers stop varying
- D. In the corpus pipeline, by marking the old record superseded and not indexing it

<details><summary>Answer</summary>

**D.** Only the pipeline knows which document is current, and a test that indexes only current records can assert that 50,000 appears and 30,000 does not. A asks the model to guess which text is newer, B leaves the stale document in the context alongside the new one, and C changes wording variation, not which fact is quoted. *(AI · 7.2)*

</details>

**52. Rashid reviews the nightly regulatory report for 8 October. All 10,000 accounts appear exactly once, no value is null or outside the accepted list, the data is fresh and the balances table agrees with the ledger. Yet the sum of the reported balances is 1,000.00 QAR lower than in the balances table. Which check was missing?**

- A. A schema check that the report's column list matches the agreed one
- B. A totals check that the report's sum matches the balances table
- C. A reconciliation check that each balance equals the sum of its ledger entries
- D. A volume check that the ledger table is not empty

<details><summary>Answer</summary>

**B.** Every row is individually valid, so not-null, accepted-values, unique and freshness checks all pass, and all 10,000 accounts are present, so completeness passes too. Only a totals check, comparing the report's sum with the balances table, sees that an amount is wrong. A column-list check (A) looks at the shape of the report, reconciliation (C) compares the balances table with the ledger, which already agree, and a volume check (D) notices only an empty table. Prove it by lowering one reported balance by 100 and watching the check fail. *(Reliability · 4.3)*

</details>

**53. A Najm squad must refactor a 600-line statement-export module that has no tests and no specification. Customers rely on some of its odd output. What should come first?**

- A. Rewrite it from scratch with TDD, using the feature list as the specification
- B. Refactor first, then write tests for whatever the code does afterwards
- C. Record current outputs for many inputs as golden-master tests, then refactor
- D. Write unit tests from the product description and fix the code where they fail

<details><summary>Answer</summary>

**C.** A golden master (characterisation test) records what the legacy code does, right or wrong, so every refactoring step can be checked against it; review any diff like code. A throws away behaviour customers rely on, B has no safety net while the code changes, and D "fixes" output nobody asked to change. *(Unit · 2.3)*

</details>

**54. Rashid's take-home for a Najm QE role is three hours on the Transfers API, and the brief allows an assistant if the candidate says so. A candidate used one to draft most of her tests. How should she submit?**

- A. Mention the assistant only if the interviewer asks, so that the README stays on the tests
- B. Name the assistant in the README, say what she checked and be ready to explain every line
- C. Name the assistant in the README but hand in its tests unread, since the brief only asks her to say so
- D. Rewrite every test in her own words and leave the assistant out, since she can explain every line

<details><summary>Answer</summary>

**B.** Both halves of Najm's take-home rule are needed: disclose the use, and be able to explain every line you submit. A and D hide a use that the brief asks her to state (D even though she could explain every line), and C discloses but hides behind the tool, handing in work she has not checked. *(Career · 8.2)*

</details>

**55. Nada asks a coding agent, which has only the repository to go on, to write the authorisation matrix tests for the Transfers routes. All the tests pass, even with `NAJM_BUGS=bola` switched on. What went wrong, and what is the fix?**

- A. The matrix has too few routes, so add more routes until at least one cell fails
- B. The forged-token column is missing, so add that column and the BOLA cells will then fail
- C. BOLA cannot appear in a matrix, so only a DAST scan of the running app can find it
- D. The expected column came from the code, so write it from the requirement instead

<details><summary>Answer</summary>

**D.** With only the code to read, the agent copied today's behaviour, so with the bug on, Bob reading Alice's transfer is recorded as a correct 200. The expected column must come from the requirement ("customers see and use only their own money"), written before the code is read; an AI can brainstorm cells but must not fill in the expected statuses. More routes (A) or another column (B) repeat the same mistake, and C is backwards: a matrix is how BOLA is found, and a scanner knows nothing about who owns what. *(Security · 4.2)*

</details>

**56. Bilal adds six cut-off tests for `value_date`, each at 16:30 Qatar time, on Friday and Saturday dates. With `tz_cutoff` switched on, all six still pass. What is the best fix?**

- A. Move the tests to 10:00 Qatar time, which keeps the cut-off out of the picture
- B. Use Sunday-to-Thursday dates, with times either side of 15:00 Qatar time
- C. Run the tests on a machine whose clock is set to UTC, so the bug shows
- D. Add more Friday and Saturday dates, since weekends are the riskiest days

<details><summary>Answer</summary>

**B.** On Friday and Saturday the weekend rule sends everything to Sunday, so reading the cut-off in UTC changes nothing; on a working day, any time from 15:00 to 17:59 Qatar time gets the wrong date. A picks a time the bug leaves alone, C changes nothing because the tests pass zone-aware times, and D repeats the blind spot. *(Design · 1.2)*

</details>

**57. Nada writes a paraphrase test for Najm Assist, which samples at temperature 0.8 and so opens its replies with different words from run to run: it asks "What is the daily transfer limit?" and "How high is the daily transfer limit?" and asserts that both replies are non-empty. Bilal says it can never fail. Which assertion states the relation?**

- A. Both replies are non-empty and shorter than 200 characters
- B. The two replies are identical word for word
- C. Both questions retrieve the same top source document
- D. The second reply is not longer than the first reply

<details><summary>Answer</summary>

**C.** A paraphrase must keep the source, and that relation can fail, as it does when a rephrasing sends the question to the cut-off document. A still passes an invented or wrong answer, B fails on harmless opening words because the wording varies from run to run, and D is not a relation a paraphrase implies (the openings alone can make either reply longer). *(AI · 7.3)*

</details>

**58. An agent refactors the international fee code. Its report says "rounding verified, all tests pass". Nada's checkout holds the refactor, and the sample's seeded `float_fee` switch is still wired into `fee()`. Before the review, she wants the check that best tests the claim that rounding is verified. What should she do?**

- A. Switch on the seeded `float_fee` bug in her checkout and see whether the suite fails
- B. Read the agent's report once more, since it lists what was verified and how it was run
- C. Confirm that line coverage on the changed file has not fallen since last week's merge
- D. Ask the agent to rerun the suite and paste the last line of the output it gets

<details><summary>Answer</summary>

**A.** The reviewer's question is "if the bug were here, would this run be red?", and switching on the bug you fear answers it with evidence: a suite that stays green with `float_fee` on has not verified rounding. B and D rely on the agent's own account, and C measures execution, which an assertion-free test can satisfy. *(AI · 6.1)*

</details>

**59. Nada's team compares an assistant with the starter suite. Her reviewed suite, the assistant's draft plus six tests she wrote herself, catches all nine seeded bugs, and she wants to report "9 of 9: the approach is proven". How should the assistant's evaluation be run to be fair?**

- A. Give it the rules and the bug list, run it three times, and report the average
- B. Give it the rules only, run it three times, and report only the best run
- C. Give it the rules only, run it three times, and add a mutation score as well
- D. Give it the rules only, run it three times, and compare the suites on line coverage

<details><summary>Answer</summary>

**C.** A suite written knowing the bug list makes 9 of 9 circular. Give the assistant the rules only, repeat the run and record model, version and date, and add mutation testing as a second yardstick, since the two measure different things. A feeds the circularity, B reports the luckiest run instead of the spread, and D compares suites on what ran, not on what they catch. *(Strategy · 6.3)*

</details>

**60. Tariq's squad reaches a partner FX service through its own `rate()` function, and the service times out about once a week. He wants a test proving that `rate()` turns a timeout into one clear error and does not crash. What is the best approach?**

- A. Call the live FX sandbox in CI and rerun the test until a timeout happens
- B. Stub the HTTP layer so the call times out, then assert the one clear error
- C. Replay a cassette recorded from last week's successful FX responses
- D. Mock the app's own `rate()` function so it raises the clear error directly

<details><summary>Answer</summary>

**B.** A partner cannot be made to time out on demand, so stub it at the HTTP boundary: the real `rate()` code that turns failures into one error runs, and the test is repeatable. A depends on luck, C replays only the happy path, and D mocks the very code under test, so it proves only that the mock raises. *(Integration · 2.2)*

</details>

## 📚 References
- ISTQB, syllabi and sample questions for Foundation Level and beyond: [istqb.org](https://www.istqb.org/)
- *Software Engineering at Google* (2020), chapters on testing: [abseil.io/resources/swe-book](https://abseil.io/resources/swe-book)
