"""Negative and alternative-solution tests for m12 (the team's AI engineering playbook).

The grader here is a *lint* of one Markdown file plus the usual repository hygiene, so the interesting tests
are of four kinds:

* the wrong playbooks people and agents really write (a generic draft of wishes and vanity metrics, rules with
  no check, metrics with no definition, a guard with no response, an invented baseline, a pointer to the module
  the old architecture page still lists) and the check that must catch each;
* the shortcuts: editing CONTRIBUTING.md or the facts file to make the playbook fit, editing the tests, leaving
  the skeleton's prompts in, committing badly or not at all, putting a key in the text;
* the right playbooks written differently (another structure, other words, other formats for the same things)
  that must all pass, because a grader has to accept any sound solution;
* the helpers (parsing, rule extraction, metric parsing), because a lint is only as good as its parser.

Text-level tests call ``checks_m12.playbook_checks`` on a started lab (so file pointers resolve); the
repository tests use the full grade.
"""
from __future__ import annotations

import re
import shutil
import time
from pathlib import Path

import pytest

from ailab import checks_m12 as m, framework, gitutil
from conftest import LEARNER, learner_commit, run_cli, start

HERE = Path(m.__file__).resolve().parent / "labs" / "m12_playbook"
REFERENCE = (HERE / "solution" / "playbook.md").read_text(encoding="utf-8")
SKELETON = (HERE / "templates" / "playbook.md").read_text(encoding="utf-8")

REQUIRED_TEXT_CHECKS = [n for n in m.ALL_NAMES if n not in m.ADVISORY and n in m._FILE_CHECKS]  # noqa: SLF001


# --------------------------------------------------------------------------------------------------------------
# a generic first draft (constructed for teaching, not recorded from a model) and an alternative good playbook
# --------------------------------------------------------------------------------------------------------------
GENERIC_DRAFT = """\
# Payments Platform: AI Engineering Playbook

## 1. Tools and Environments
We use best-in-class AI coding assistants such as GitHub Copilot, Cursor and ChatGPT to boost developer
productivity. Engineers should choose the tool that works best for them and use it responsibly in a secure
environment.

## 2. Data Rules
Engineers should be careful not to share sensitive data with AI tools. Follow company data protection policies
at all times and use good judgement.

## 3. Context and Memory
Maintain a CLAUDE.md file with up-to-date project context so that AI assistants generate relevant code. Update it
regularly and keep it comprehensive.

## 4. Spec and Review Norms
All AI-generated code should be reviewed carefully by a qualified engineer. Pull requests should be kept
reasonably small. Changes to `src/remit/risk.py` need extra attention. Reviews should be completed in a timely
manner.

## 5. Verification Standard
Ensure that all code is properly tested. Aim for high test coverage and run the test suite before merging.

## 6. Security Baseline
Follow security best practices. Never commit secrets. Keep dependencies up to date.

## 7. Automation
Automate repetitive tasks wherever feasible to improve efficiency.

## 8. Metrics Plan
Studies show AI assistants make developers up to 55% more productive. We will track:
- Lines of code written per developer
- Suggestion acceptance rate
- Percentage of code written by AI (target: 50%)
- Developer satisfaction

## 9. Incident Handling
If an AI-related incident occurs, follow the standard incident response process and learn from it.

## 10. Onboarding
New engineers will receive training on the effective use of AI tools.
"""

ALTERNATIVE = """\
# AI engineering playbook, Payments Platform

Version 1. Maintained by Tariq (engineering lead). We revisit it every quarter and after any AI-related incident.
It sits under the bank's six rules and under CONTRIBUTING.md and never loosens either.

## 1) Approved tools and where agents run

The approved-tools list is kept by Salem (platform engineering). At the moment it names Claude Code on the bank's
enterprise account and GitHub Copilot in the IDE; no personal or free account is ever used with bank code.
To get a tool added, an engineer sends Salem a request; Noura reviews its security and Sara its handling of data.

Agents work in a throw-away branch or a worktree on a managed laptop, or in CI with a read-only token.
Production hosts and production credentials are out of bounds for every agent, always.

* **T1.** MUST use only tools on the approved-tools list. Verified by: Salem's quarterly licence audit against the list.
* **T2.** MUST NOT hand an agent a production credential. Verified by: the CI secrets audit, run monthly by Salem.

## 2) Data

Data classes: Public, Internal, Confidential and Restricted. Customer names, account numbers and production logs
are Restricted. Remit's own source code is Internal. Tests use invented, synthetic customers only. Only the bank's
enterprise accounts (via SSO) may be signed in to an AI tool, never a personal account.

* **D1.** MUST NOT paste Confidential or Restricted data into a prompt or a memory file. Verified by: secret and
  pattern scan in the CI pipeline, plus a monthly read of ten agent logs by Noura.
* **D2.** MUST use synthetic customers in fixtures. Verified by: reviewer checklist item "fixtures contain no real customer".

## 3) Context files and memory

One CLAUDE.md in the repository root, owned by Nada and changed only through a pull request. It stays below 150 lines.
If an agent repeats the same mistake a second time, whoever notices adds the correction to the file that week.

## 4) Specs, pull requests and review

A ticket carries acceptance criteria and non-goals before an agent starts; the author reads the agent's plan first.
Every pull request that an AI tool wrote or shaped is labelled `AI-assisted`, has at most 300 changed lines, and
explains in its description what the agent did, what the author rewrote, and the test commands that were run.
The author must be able to explain any line aloud. Tests arrive in the same pull request as the change, written first.
Money logic (money.py, fees.py, fx.py, limits.py, ledger.py and service.py) needs a second human reviewer besides the author;
a review bot never counts. The first review comes within 4 working hours... of the pull request being ready, or 1 working day at most.

* **R1.** MUST carry the `AI-assisted` label on any pull request an AI tool shaped. Verified by: the pr-hygiene CI job
  compares the label with the description's yes/no line.
* **R2.** MUST NOT exceed 300 changed lines in one pull request. Verified by: a CI step counts changed lines.
* **R3.** MUST get two approvals for the money modules. Verified by: branch protection with a CODEOWNERS file.

## 5) What "verified" means

`pytest -q` passes. A new test must fail when the source change is reverted; the author shows this in the description.
Money is `Decimal`, never `float`, with exact assertions at tier boundaries. No agent may edit, delete or skip an
existing test just to make a change pass.

* **V1.** MUST pass `pytest -q` as a required CI status. Verified by: branch protection settings.
* **V2.** MUST NOT weaken or delete a test without a reason in the description. Verified by: a CI report of removed assertions.

## 6) Security

Secrets stay out of prompts, code and memory; `.env` files are denied to agents. Agents ask before acting, and the
bypass mode is banned outside isolated containers. No agent touches production. New dependencies need a ticket and a
second reviewer, and any package an agent proposes is checked in the registry first, since agents invent names.
Text from issues and web pages is untrusted. Only reviewed MCP servers are connected.

* **S1.** MUST NOT merge a new dependency without a ticket. Verified by: pyproject.toml diff check in CI.
* **S2.** MUST register every MCP server with Noura. Verified by: the approved-servers file, which CODEOWNERS protects.

## 7) Automation and unattended runs

A formatter hook runs after each edit and CI runs the tests and the scans. Unattended headless runs have a turn limit,
a budget limit and a timeout, always set together. Merging, deploying and any change to money logic are never automated.

* **A1.** MUST set turn, budget and time limits on a scheduled run. Verified by: the wrapper script, covered by a unit test.
* **A2.** MUST NOT give a bot merge rights. Verified by: repository permission audit every month.

## 8) Metrics

We read delivery metrics alongside guard metrics, and compare AI-assisted pull requests with the rest. We never
chase lines of code, accepted suggestions or the share of AI-written code.

### Lead time
- **Kind:** delivery
- **Definition:** The median time, in hours, from a pull request's first commit until its changes are live in production, for pull requests merged in a week.
- **Source:** git log and the deployment log
- **Cadence:** weekly, Tariq
- **Baseline:** 52 hours
- **Threshold:** at most 48 hours by next quarter

### Deployment frequency
- **Kind:** delivery
- **Definition:** The number of production deployments in each calendar week.
- **Source:** deployment log
- **Cadence:** weekly, Tariq
- **Baseline:** to be measured per week; 30 in 13 weeks
- **Threshold:** at least 2 per week

### Time to restore
- **Kind:** delivery
- **Definition:** The median time from the moment a production deployment is declared failed until service is back, per quarter.
- **Source:** incident tickets
- **Cadence:** monthly, Maha
- **Baseline:** 3 hours
- **Threshold:** at most 3 hours

### Change failure rate
- **Kind:** guard
- **Definition:** Production deployments that needed a rollback or a hotfix, divided by all production deployments, over a rolling four weeks.
- **Source:** deployment log and incident tickets
- **Cadence:** weekly, Tariq
- **Baseline:** 3 of 30 (10%)
- **Threshold:** More than 15%: we freeze autonomy upgrades and hold a retro on each failure.

## 9) When an AI-related incident happens

Contain: stop the agent, revoke the credentials it could reach, revert the change. Preserve the session transcript and
the agent log first. Page Maha or the on-call SRE within 1 hour. Hold a blameless postmortem in 5 working days, and finish it
with a change to a control (a hook, a rule, a permission, a memory line or a test).

* **I1.** MUST keep the transcript before cleanup. Verified by: the postmortem template has a transcript field Maha checks.

## 10) Onboarding and juniors

Week 1: set up the approved tools with Salem, read CONTRIBUTING.md and docs/TOUR.md, and pair with a mentor.
Juniors explain each AI-assisted change back to the mentor before it merges. Every sprint they take one ticket without an
AI tool. They read one module's code with a senior each month, and for 3 months a named senior reviews their pull requests.
"""


NATURAL = """\
# Payments Platform: AI engineering playbook

Owner: Tariq. Status: draft for the clinic. Next review: after the first incident or in three months, whichever is sooner.

## 1. Tools and environments

We use two approved tools: Claude Code (bank enterprise account through SSO) and GitHub Copilot in the IDE. Salem owns the approved-tools list. If you want another tool, ask Salem; Noura checks security and Sara checks data. Until it is on the list, nobody uses it with Remit code.

Agents work on a feature branch on a managed laptop, or in CI. They never run against production and never get production credentials.

- MUST NOT use an unapproved tool or a personal account with Remit code. Check: Salem compares the licence report with the approved-tools list every quarter.
- MUST NOT give any agent a production credential. Check: the CI secrets audit lists every secret and its environment, and production ones are not visible to pull-request jobs.

## 2. Data rules

Data classes are Public, Internal, Confidential and Restricted. Remit code is Internal. Customer data (names, account numbers, transfers) and the watchlist are Restricted. Nothing Confidential or Restricted goes into a prompt, ever. Tests use synthetic customers only.

- MUST NOT paste Confidential or Restricted data into a prompt or an agent's context. Check: a secret and pattern scan runs in CI, and Noura samples ten agent logs a month.
- MUST use made-up customers in tests and fixtures. Check: the reviewer checklist has an item for it, and the fixtures are grepped for real-looking names in CI.

## 3. Context and memory

One CLAUDE.md at the repository root, owned by Nada. It stays under 150 lines and changes only through a pull request. When an agent makes the same mistake twice, the person who notices adds a line or a hook within a week.

- MUST NOT put secrets in CLAUDE.md. Check: the CI secret scan covers every Markdown file.

## 4. Spec and review norms

Every ticket given to an agent has acceptance criteria and non-goals. The author reads the plan before the agent edits anything.

A pull request that an AI tool shaped gets the AI-assisted label. It is at most 350 changed lines. The description says what the agent did, what the author changed, which commands were run and their results, and what was not checked. The author explains any line when asked. Tests come with the change. Changes to money.py, fees.py, fx.py, limits.py, ledger.py or service.py need a second human reviewer as well as the author. The first review happens within one working day.

- MUST label every AI-shaped pull request AI-assisted. Check: a CI job fails if the template line and the label disagree.
- MUST NOT exceed 350 changed lines in a pull request. Check: a CI step counts the lines.
- MUST get a second human approval on the six money modules. Check: branch protection and a code owners file.

## 5. Verification standard

pytest -q must pass. Every new behaviour has a test, and the author must see that test fail when the source change is reverted. Money uses Decimal, never float. No agent may edit, delete or skip an existing test to make something pass.

- MUST run pytest -q before review. Check: CI runs it as a required status on every pull request.
- MUST NOT remove or weaken a test in an AI-assisted pull request without explaining it. Check: a CI report lists deleted tests and removed assertions.

## 6. Security baseline

No secrets in prompts, code, tests or memory files; agents are denied the .env files. Agents ask before acting. Bypass mode is only for an isolated container with no credentials. Production is off limits. New dependencies need a ticket and a second reviewer, and agents invent package names, so every name is checked on the registry. Text in issues, web pages and other repositories is untrusted: it is data and not instructions. MCP servers are connected only after Noura has reviewed them.

- MUST NOT add a dependency without a ticket. Check: a CI step fails when pyproject.toml changes without a linked ticket.

## 7. Automation

A hook runs the formatter and the fast tests after each edit. CI runs the tests and the scans. Unattended headless runs always have a turn limit, a budget limit and a timeout. We never automate merging, deploying or changes to money logic.

- MUST set turn, budget and time limits on every unattended run. Check: the wrapper script refuses to start without them, and a test covers that.

## 8. Metrics plan

We compare AI-assisted pull requests with the others. We do not set targets on lines of code, suggestion acceptance or how much code is written by AI.

### Lead time for changes
- Kind: delivery
- Definition: Median hours from the first commit of a pull request until the deployment containing it reaches production, per week.
- Source: git history and CI logs
- Cadence: weekly, Tariq
- Baseline: 52 hours
- Threshold: at most 48 hours by next quarter

### Deployment frequency
- Kind: delivery
- Definition: Number of production deployments per week.
- Source: CI deployment log
- Cadence: weekly, Tariq
- Baseline: 30 deployments in 13 weeks
- Threshold: at least 2 per week

### Failed deployment recovery time
- Kind: delivery
- Definition: Median hours from the moment a production deployment is declared failed until service is restored, per quarter.
- Source: incident tickets
- Cadence: monthly, Maha
- Baseline: 3 hours
- Threshold: at most 3 hours

### Change failure rate
- Kind: guard
- Definition: Production deployments that needed a rollback or a hotfix divided by all production deployments, over a rolling four weeks.
- Source: CI log and incident tickets
- Cadence: weekly, Tariq
- Baseline: 3 of 30 deployments
- Threshold: Above 15%, we freeze autonomy upgrades and hold a retro on each failure.

## 9. Incident handling

If an AI tool or an AI-assisted change plays a part in an incident: stop the agent session, revoke any credential it could reach, and revert the change. Keep the session transcript and the agent log before anything is cleaned up. Page Maha or the on-call SRE within 1 hour. Hold a blameless postmortem within 5 working days. It ends with a change to one control: a rule, a hook, a permission, a memory line or a test.

- MUST keep the transcript before cleanup. Check: the postmortem template has a field for where the transcript is stored.

## 10. Onboarding

New joiners set up the approved tools with Salem, read CONTRIBUTING.md and docs/TOUR.md in week 1, and pair with a mentor. Juniors explain each AI-assisted change back to the mentor before it merges. In every sprint they take one ticket without an AI tool. Each month they read one module with a senior. For 3 months a named senior reviews their pull requests.
"""


# --------------------------------------------------------------------------------------------------------------
# fixtures and helpers
# --------------------------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def template(tmp_path_factory) -> Path:
    return start("m12", tmp_path_factory.mktemp("m12-template") / "work")


@pytest.fixture
def work(template, tmp_path) -> Path:
    """A private copy of the started lab (the .git folder and the lab-start tag come with it)."""
    target = tmp_path / "work"
    shutil.copytree(template, target)
    return target


def put(work: Path, text: str) -> None:
    (work / "playbook.md").write_text(text, encoding="utf-8")


def results(work: Path) -> dict[str, framework.Check]:
    return {c.name: c for c in m.playbook_checks(work)}


def failing(work: Path) -> set[str]:
    """Names of the text checks (required or advisory) that fail."""
    return {name for name, c in results(work).items() if not c.ok}


def failing_required(work: Path) -> set[str]:
    return {name for name, c in results(work).items() if not c.ok and c.required}


def swap(text: str, old: str, new: str) -> str:
    assert old in text, f"test bug: {old!r} is not in the text"
    return text.replace(old, new, 1)


def drop_between(text: str, start_marker: str, end_marker: str) -> str:
    """Remove the text from ``start_marker`` up to (not including) ``end_marker``."""
    a = text.index(start_marker)
    b = text.index(end_marker, a)
    return text[:a] + text[b:]


def metrics_of(text: str) -> str:
    return text[text.index("## 8. Metrics plan"):text.index("## 9. Incident handling")]


def commit(work: Path, message: str = "docs(playbook): write the playbook") -> None:
    learner_commit(work, message)


# --------------------------------------------------------------------------------------------------------------
# the reference, the starter, and the facts the grader reads
# --------------------------------------------------------------------------------------------------------------
def test_the_reference_passes_every_text_check(work):
    put(work, REFERENCE)
    assert failing(work) == set()


def test_the_alternative_playbook_passes_every_required_check(work):
    """Another structure, other words and other formats for the same content: a sound solution must pass."""
    put(work, ALTERNATIVE)
    assert failing_required(work) == set(), {n: c.detail for n, c in results(work).items() if not c.ok and c.required}


def test_a_playbook_written_blind_from_the_ticket_passes(work):
    """Written from the ticket, the facts and CONTRIBUTING.md before the grader was finished, in plain sentences."""
    put(work, NATURAL)
    assert failing_required(work) == set(), {n: c.detail for n, c in results(work).items() if not c.ok and c.required}


def test_the_starter_skeleton_fails_with_useful_details(work):
    put(work, SKELETON)
    found = results(work)
    assert failing_required(work)
    for name, check in found.items():
        if not check.ok:
            assert check.detail and check.hint, f"{name}: a failing check needs a detail and a hint"
    # nothing passes just because there is nothing to check
    for name in (m.N_RULE_CHECK, m.N_RULE_VAGUE, m.N_MET_DEFINED, m.N_MET_BASELINE, m.N_MET_VANITY, m.N_SECTIONS):
        assert not found[name].ok, name


def test_no_hint_or_detail_quotes_the_reference(template):
    """The grader names what is missing; it must never hand over the reference text."""
    work = template
    texts = [c.detail + " " + c.hint for c in m.all_checks(work)]
    def grams_of(text: str) -> set[str]:
        words = re.findall(r"[a-z0-9']+", text.lower())
        return {" ".join(words[i:i + 7]) for i in range(len(words) - 6)}

    # what the learner is given anyway (the skeleton, the ticket, the facts) is not a leak
    given = SKELETON + (HERE / "task.md").read_text(encoding="utf-8") + (HERE / "assets" / "team-context.md").read_text(encoding="utf-8") \
        + framework.BASE_REPO.joinpath("CONTRIBUTING.md").read_text(encoding="utf-8")
    grams = grams_of(REFERENCE) - grams_of(given)
    for text in texts:
        said = re.findall(r"[a-z0-9']+", text.lower())
        for i in range(len(said) - 6):
            assert " ".join(said[i:i + 7]) not in grams, f"a hint repeats the reference: {text!r}"


def test_the_facts_the_grader_uses_are_the_kits_own(template):
    assert m.money_modules() == ("money.py", "fees.py", "fx.py", "limits.py", "ledger.py", "service.py")
    assert m.fact_numbers() == {"13", "30", "2", "52", "3", "10", "4", "9", "60", "0", "1"}
    # every figure a metric may quote is in the facts file, and every figure of the table belongs to some metric
    quotable = set().union(*(numbers for _, numbers in m.BASELINES)) | {m.QUARTER_WEEKS}
    assert quotable == m.fact_numbers()
    # and the lab asset says the same things the lab's task promises
    assets = (template / "lab-assets" / "team-context.md").read_text(encoding="utf-8")
    assert "Last quarter in numbers" in assets and "AI-assisted" in assets


# --------------------------------------------------------------------------------------------------------------
# the wrong playbooks
# --------------------------------------------------------------------------------------------------------------
def test_a_generic_ai_draft_fails_where_it_should(work):
    put(work, GENERIC_DRAFT)
    bad = failing_required(work)
    for expected in (m.N_SECTIONS, m.N_LENGTH, m.N_RULE_COUNT, m.N_RULE_COVER, m.N_TOOLS, m.N_DATA, m.N_REV_LABEL,
                     m.N_REV_SIZE, m.N_REV_MONEY, m.N_REV_SPEED, m.N_VERIFY, m.N_INCIDENT, m.N_ONBOARDING,
                     m.N_MET_BLOCKS, m.N_MET_DELIVERY, m.N_MET_GUARD, m.N_MET_VANITY, m.N_PROD, m.N_PATHS, m.N_CLAIMS):
        assert expected in bad, expected


def test_vanity_metrics_are_caught_and_do_not_count_as_delivery(work):
    vanity = """\
## 8. Metrics plan
We track developer output.

### Lines of code per developer
- Kind: delivery
- Definition: The number of lines of code each developer commits per week, counted from the git history.
- Source: git log
- Cadence: weekly, Tariq
- Baseline: to be measured
- Threshold: at least 500 lines a week

### Suggestion acceptance rate
- Kind: delivery
- Definition: Suggestions accepted divided by suggestions shown, per developer, per week, taken from the IDE telemetry.
- Source: IDE telemetry
- Cadence: weekly, Tariq
- Baseline: to be measured
- Threshold: at least 30%

### Percentage of code written by AI
- Kind: guard
- Definition: Lines written by AI divided by all lines merged, per month, from the commit trailers.
- Source: git log
- Cadence: monthly, Tariq
- Baseline: to be measured
- Threshold: Above 80% we review the code, so we reach the target of 70% AI-written code.

"""
    put(work, swap(REFERENCE, metrics_of(REFERENCE), vanity))
    bad = failing_required(work)
    assert m.N_MET_VANITY in bad and m.N_MET_DELIVERY in bad


def test_an_adoption_target_is_caught(work):
    block = """\
### AI adoption
- Kind: delivery
- Definition: The share of merged pull requests carrying the AI-assisted label, per month, from the GitHub label history.
- Source: GitHub
- Cadence: monthly, Tariq
- Baseline: 60%
- Threshold: at least 80% of merged pull requests

"""
    put(work, swap(REFERENCE, "### Deployment frequency", block + "### Deployment frequency"))
    assert m.N_MET_VANITY in failing_required(work)


def test_reporting_the_adoption_share_without_a_target_is_fine(work):
    block = """\
### AI-assisted share
- Kind: delivery
- Definition: The share of merged pull requests carrying the AI-assisted label, per month, from the GitHub label history.
- Source: GitHub
- Cadence: monthly, Tariq
- Baseline: 60%
- Threshold: no target; we report it and never aim for a number
"""
    put(work, swap(REFERENCE, "### Deployment frequency", block + "\n### Deployment frequency"))
    assert m.N_MET_VANITY not in failing_required(work)


def test_a_guard_on_the_quality_of_ai_assisted_changes_is_not_adoption(work):
    block = """\
### Rework on AI-assisted pull requests
- Kind: guard
- Definition: Count of pull requests labelled AI-assisted that needed a follow-up fix within 14 days, divided by all AI-assisted pull requests merged in the quarter.
- Source: GitHub and the ticket board
- Cadence: monthly, Nada
- Baseline: to be measured
- Threshold: Above 20% in a quarter, Nada reviews the tests of those changes and we add what is missing.
"""
    put(work, swap(REFERENCE, "### Review turnaround", block + "\n### Review turnaround"))
    assert failing(work) == set()


def test_metric_names_without_definitions_fail(work):
    text = REFERENCE
    for definition in re.findall(r"- Definition: .*?(?=\n- Source)", metrics_of(REFERENCE), flags=re.S):
        text = text.replace(definition, "- Definition: How well we deliver.")
    put(work, text)
    found = results(work)
    assert not found[m.N_MET_DEFINED].ok
    assert "feeling or a question" in found[m.N_MET_DEFINED].detail


def test_a_one_line_definition_is_fine_when_it_is_precise(work):
    """Written blind from the ticket: 'Number of production deployments per week.' is six words and measurable."""
    put(work, swap(REFERENCE, "Number of deployments to production per week, counted from the CI deployment log.",
                   "Number of production deployments per week."))
    assert m.N_MET_DEFINED not in failing(work)


@pytest.mark.parametrize("name, definition, expected", [
    ("Lead time for changes", "Time from commit to production, as the median, per week for merged pull requests.", True),
    ("Lead time for changes", "The mean number of days a change takes to get live in production, weekly.", False),   # no start/end
    ("Lead time for changes", "Median hours since the first commit until the change is in production, per week.", True),
    ("Lead time", "how fast we ship", False),
    ("Speed", "Deployment speed.", False),
    ("Lead time for changes", "From the first commit until production, for the pull requests merged in the week.", False),  # no statistic
    ("Change failure rate", "Deployments needing a hotfix or rollback divided by all deployments in four weeks.", True),
    ("Change failure rate", "How often a deployment goes wrong, as a percentage, looked at by the team each month.", False),
    ("Deployment frequency", "Number of deployments to production per week, counted from the CI deployment log.", True),
    ("Deployment frequency", "How often the team deploys to production, which we watch carefully every week.", False),
    ("AI-related incidents", "Count of incidents with an AI-assisted change as a contributing cause, per quarter.", True),
    ("Developer productivity", "How productive the developers feel when they use the tools every single day.", False),
])
def test_what_makes_a_definition_measurable(name, definition, expected):
    metric = m.Metric(name, 0, {"Definition": definition})
    assert (m.definition_problems(metric) == []) is expected, (name, m.definition_problems(metric))


@pytest.mark.parametrize("threshold", [
    "Above 20% in a quarter, Nada reviews the tests of those changes.",
    "More than 3 failures in four weeks: autonomy stops rising.",
    "Over 16 hours in a week, we are pausing new agent work.",
    "At least 1 in a quarter, the incident process runs in full and the on-call SRE reviews the agent's permissions.",
    "Above 15%: alert Tariq and hold a retro.",
])
def test_a_response_may_be_inflected(threshold):
    assert m.threshold_problems(threshold) == []


@pytest.mark.parametrize("threshold, ok", [
    ("Above 15% over any four weeks, we stop raising agent autonomy and review every failed change.", True),
    ("More than 2 incidents in a quarter: pause new agent work and open a retro.", True),
    ("Keep it low.", False),
    ("Above 15% over any four weeks.", False),          # a number, a comparison, but no response
    ("We stop and review when it looks bad.", False),   # a response, but no number
    ("15% is the limit and we stop at 15%", False),     # no comparison words ... see below
])
def test_what_makes_a_guard_threshold(threshold, ok):
    problems = m.threshold_problems(threshold)
    if threshold.startswith("15% is the limit"):
        # a number and an action, but nothing says what is crossed: the grader asks for a comparison
        assert problems and "comparison" in problems[0]
    else:
        assert (problems == []) is ok, problems


def test_a_guard_without_a_response_fails(work):
    text = swap(REFERENCE, "Above 15% over any four weeks, we stop raising agent autonomy and review every failed change at the\n  next clinic.",
                "Above 15% over any four weeks.")
    put(work, text)
    found = results(work)
    assert not found[m.N_MET_GUARD].ok and "response" in found[m.N_MET_GUARD].detail


def test_two_delivery_metrics_are_not_enough(work):
    put(work, drop_between(REFERENCE, "### Failed deployment recovery time", "### Change failure rate"))
    assert m.N_MET_DELIVERY in failing_required(work)


def test_three_blocks_of_the_same_metric_are_one_family(work):
    text = REFERENCE
    text = swap(text, "### Deployment frequency", "### Lead time per team")
    text = swap(text, "### Failed deployment recovery time", "### Lead time for hotfixes")
    put(work, text)
    assert m.N_MET_DELIVERY in failing_required(work)


def test_a_guard_metric_is_required(work):
    text = REFERENCE
    for guard in ("Change failure rate", "Rework rate", "Review turnaround", "AI-related incidents"):
        text = swap(text, f"### {guard}\n- Kind: guard", f"### {guard}\n- Kind: delivery")
    put(work, text)
    assert m.N_MET_GUARD in failing_required(work)


def test_an_invented_baseline_is_caught(work):
    put(work, swap(REFERENCE, "- Baseline: 52 hours (median, last quarter).", "- Baseline: 7 hours (median, last quarter)."))
    found = results(work)
    assert not found[m.N_MET_BASELINE].ok and "7" in found[m.N_MET_BASELINE].detail


def test_a_real_figure_on_the_wrong_metric_is_caught(work):
    """4 and 52 are both in the facts file, but 4 is the rework count and 52 is the lead time."""
    put(work, swap(REFERENCE, "- Baseline: 52 hours (median, last quarter).", "- Baseline: 4 hours (median, last quarter)."))
    assert m.N_MET_BASELINE in failing_required(work)
    put(work, swap(REFERENCE, "- Baseline: 30 deployments in 13 weeks (about 2 a week).", "- Baseline: 52 hours."))
    assert m.N_MET_BASELINE in failing_required(work)


def test_a_custom_metric_has_no_baseline_figure_to_quote(work):
    block = """\
### Time for a new joiner to merge a first pull request
- Kind: guard
- Definition: Median working days from a new joiner's first day until their first pull request is merged, per quarter.
- Source: GitHub and the HR start dates
- Cadence: quarterly, Tariq
- Baseline: 9 days
- Threshold: Over 15 days in a quarter we review the onboarding plan with the buddies and shorten the first ticket.
"""
    put(work, swap(REFERENCE, "### Review turnaround", block + "\n### Review turnaround"))
    found = results(work)
    assert not found[m.N_MET_BASELINE].ok       # the 9 hours belong to the review-turnaround metric, not to this one
    put(work, swap(REFERENCE, "### Review turnaround", block.replace("- Baseline: 9 days", "- Baseline: to be measured") + "\n### Review turnaround"))
    assert m.N_MET_BASELINE not in failing(work)


def test_to_be_measured_is_an_honest_baseline(work):
    put(work, swap(REFERENCE, "- Baseline: 52 hours (median, last quarter).", "- Baseline: To be measured in the first month."))
    assert m.N_MET_BASELINE not in failing(work)


def test_editing_the_facts_file_does_not_move_the_goalposts(work):
    facts = work / "lab-assets" / "team-context.md"
    facts.write_text(facts.read_text(encoding="utf-8") + "\n| Median lead time, all teams | 4 hours |\n", encoding="utf-8")
    put(work, swap(REFERENCE, "- Baseline: 52 hours (median, last quarter).", "- Baseline: 4 hours (median, last quarter)."))
    assert m.N_MET_BASELINE in failing_required(work)


def test_a_metric_block_with_a_missing_field_fails(work):
    put(work, swap(REFERENCE, "- Cadence: monthly, reviewed by Nada.\n", ""))
    found = results(work)
    assert not found[m.N_MET_BLOCKS].ok and "Cadence" in found[m.N_MET_BLOCKS].detail


def test_kind_must_be_delivery_or_guard(work):
    put(work, swap(REFERENCE, "### Rework rate\n- Kind: guard", "### Rework rate\n- Kind: quality"))
    assert m.N_MET_BLOCKS in failing_required(work)


def test_rules_without_a_check_clause_fail(work):
    text = re.sub(r" Check: .*?(?=\n- MUST|\n\n|\n##)", "", REFERENCE, flags=re.S)
    put(work, text)
    assert m.N_RULE_CHECK in failing_required(work)


def test_a_check_that_names_no_mechanism_fails(work):
    put(work, swap(REFERENCE, "Check: the secret scan covers\n  memory files, and the pull-request template asks whether the memory changed.",
                   "Check: everyone knows."))
    found = results(work)
    assert not found[m.N_RULE_CHECK].ok and "no mechanism" in found[m.N_RULE_CHECK].detail


@pytest.mark.parametrize("word", ["responsibly", "carefully", "where appropriate", "if possible", "try to", "reasonable", "best effort", "properly"])
def test_weasel_words_in_a_rule_fail(work, word):
    put(work, swap(REFERENCE, "MUST NOT use `float` for money.", f"MUST NOT use `float` for money, {word}."))
    assert m.N_RULE_VAGUE in failing_required(work)


def test_weasel_words_outside_a_rule_are_not_this_checks_business(work):
    put(work, swap(REFERENCE, "Done means verified, not \"it compiles\".", "Done means verified, not \"it compiles\"; use good judgement."))
    assert m.N_RULE_VAGUE not in failing(work)


def test_fewer_than_twelve_rules_fail(work):
    text = REFERENCE
    for rule in re.findall(r"^- MUST (?:NOT )?[^\n]*(?:\n  [^\n]*)*", text, flags=re.M)[:10]:
        text = text.replace(rule, "")
    put(work, text)
    assert m.N_RULE_COUNT in failing_required(work)


def test_rules_must_cover_the_areas(work):
    text = drop_between(REFERENCE, "- MUST preserve the session transcript", "## 10. Onboarding")
    put(work, text)
    found = results(work)
    assert not found[m.N_RULE_COVER].ok and "incident handling" in found[m.N_RULE_COVER].detail


def test_lower_case_must_is_not_a_rule(work):
    put(work, re.sub(r"^- MUST", "- Must", REFERENCE, flags=re.M))
    found = results(work)
    assert not found[m.N_RULE_COUNT].ok and "found 0" in found[m.N_RULE_COUNT].detail


def test_a_missing_section_fails(work):
    put(work, drop_between(REFERENCE, "## 9. Incident handling", "## 10. Onboarding"))
    bad = failing_required(work)
    assert m.N_SECTIONS in bad and m.N_INCIDENT in bad and m.N_RULE_COVER in bad


def test_a_thin_section_fails(work):
    put(work, drop_between(REFERENCE, "## 7. Automation", "## 8. Metrics plan") .replace("## 8. Metrics plan", "## 7. Automation\nWe automate things.\n\n## 8. Metrics plan"))
    found = results(work)
    assert not found[m.N_SECTIONS].ok and "automation" in found[m.N_SECTIONS].detail


def test_template_text_left_in_fails(work):
    put(work, swap(REFERENCE, "Owner: Tariq, engineering lead.", "Owner: <<a named person>>."))
    assert m.N_PLACEHOLDERS in failing_required(work)


@pytest.mark.parametrize("word", ["TODO", "TBD", "FIXME"])
def test_unfinished_markers_fail(work, word):
    put(work, REFERENCE + f"\n{word}: write the rest\n")
    assert m.N_PLACEHOLDERS in failing_required(work)


def test_a_far_too_long_playbook_fails(work):
    put(work, REFERENCE + "\n" + ("This sentence pads the playbook out with words nobody needs to read. " * 70 + "\n\n") * 6)
    assert m.N_LENGTH in failing_required(work)


# ---- review norms -----------------------------------------------------------------------------------------------
def test_the_label_must_be_named(work):
    put(work, REFERENCE.replace("`AI-assisted`", "`ai`").replace("AI-assisted", "AI"))
    assert m.N_REV_LABEL in failing_required(work)


@pytest.mark.parametrize("limit, ok", [("400 lines", True), ("800 lines", True), ("5,000 lines", False), ("2000 lines", False)])
def test_the_diff_limit_must_be_small(work, limit, ok):
    put(work, REFERENCE.replace("400 lines", limit).replace("400 changed lines", limit.replace("lines", "changed lines")))
    assert (m.N_REV_SIZE in failing_required(work)) is (not ok)


def test_a_diff_limit_in_words_is_not_a_limit(work):
    text = swap(REFERENCE, "at most\n400 lines (additions plus deletions, generated files excluded)", "a small number of lines")
    put(work, text.replace("more than 400 changed lines", "more than a small number of lines"))
    assert m.N_REV_SIZE in failing_required(work)


def test_every_money_module_must_be_named(work):
    put(work, swap(REFERENCE, ", `ledger.py`", ""))
    found = results(work)
    assert not found[m.N_REV_MONEY].ok and "ledger.py" in found[m.N_REV_MONEY].detail


def test_naming_the_modules_without_a_second_human_fails(work):
    text = re.sub(r"second human (reviewer|approval)", r"review", REFERENCE).replace("in addition to the author", "").replace("two approvals", "an approval")
    put(work, text)
    assert m.N_REV_MONEY in failing_required(work)


def test_the_author_must_explain(work):
    text = REFERENCE.replace("The author can explain every line; a reviewer who asks and gets no answer sends it back.", "")
    text = text.replace("explain", "describe")
    put(work, text)
    assert m.N_REV_AUTHOR in failing_required(work)


def test_a_response_time_is_required(work):
    text = swap(REFERENCE, "A pull request gets its first human review within one working day.", "")
    text = text.replace("one working day", "a good while")
    put(work, text)
    assert m.N_REV_SPEED in failing_required(work)


def test_the_advisory_review_checks_do_not_fail_the_lab(work):
    text = REFERENCE.replace("acceptance criteria", "details").replace("non-goals", "notes")
    put(work, text)
    found = results(work)
    assert not found[m.N_REV_SPEC].ok and not found[m.N_REV_SPEC].required


# ---- the other sections -------------------------------------------------------------------------------------------
def test_tools_need_a_list_an_owner_and_a_process(work):
    put(work, drop_between(REFERENCE, "Only tools on Salem's approved-tools list", "## 2. Data rules"))
    assert m.N_TOOLS in failing_required(work)


def test_data_rules_need_the_classes(work):
    put(work, REFERENCE.replace("Confidential", "Sensitive").replace("Restricted", "Secret"))
    assert m.N_DATA in failing_required(work)


def test_data_rules_need_the_test_data_and_the_accounts(work):
    text = drop_between(REFERENCE, "Test data is synthetic", "Session transcripts are stored")
    text = drop_between(text, "- MUST use synthetic customers", "## 3. Context and memory")
    put(work, text)
    found = results(work)
    assert not found[m.N_DATA].ok and "synthetic test data" in found[m.N_DATA].detail


def test_memory_needs_an_owner_a_file_and_a_trigger(work):
    put(work, drop_between(REFERENCE, "The repository has one `CLAUDE.md`", "- MUST NOT put secrets or customer data in `CLAUDE.md`"))
    assert m.N_CONTEXT in failing_required(work)


def test_verification_must_protect_the_tests(work):
    text = REFERENCE.replace("MUST NOT edit, delete or skip an existing test to make a change pass.", "MUST keep the suite green.")
    put(work, text)
    assert m.N_VERIFY in failing_required(work)


def test_verification_must_name_decimal(work):
    put(work, REFERENCE.replace("Decimal", "exact numbers"))
    assert m.N_VERIFY in failing_required(work)


def test_security_needs_five_of_six_topics(work):
    put(work, drop_between(REFERENCE, "Standard library only: a new dependency", "## 7. Automation"))
    assert m.N_SECURITY in failing_required(work)


def test_automation_needs_a_never_list_and_limits(work):
    text = drop_between(REFERENCE, "We never automate merging to `main`", "Every unattended or scheduled run has a cap")
    text = drop_between(text, "- MUST NOT let an automated job merge or deploy.", "## 8. Metrics plan")
    put(work, text)
    assert m.N_AUTOMATION in failing_required(work)


def test_incident_handling_needs_five_of_six_topics(work):
    text = drop_between(REFERENCE, "1. Contain, within minutes", "- MUST preserve the session transcript")
    put(work, text)
    assert m.N_INCIDENT in failing_required(work)


def test_onboarding_needs_juniors_covered(work):
    put(work, drop_between(REFERENCE, "First-year engineers work under three extra habits", "- MUST explain every AI-assisted"))
    assert m.N_ONBOARDING in failing_required(work)


# ---- honesty -------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("sentence", [
    "Use `--dangerously-skip-permissions` on your laptop to move faster.",
    "Bypass mode is fine for everyday work.",
    "It is fine to use float for money in quick prototypes.",
    "The AI-assisted label is optional for small changes.",
    "The second reviewer is optional when the change is small.",
    "Authors may approve their own pull request when the reviewer is away.",
    "An AI review can replace the second human reviewer on small diffs.",
    "Agents may use production data to reproduce bugs.",
])
def test_contradicting_the_bank_or_contributing_fails(work, sentence):
    put(work, swap(REFERENCE, "## 2. Data rules\n", f"## 2. Data rules\n\n{sentence}\n"))
    assert m.N_CONTRADICT in failing_required(work), sentence


@pytest.mark.parametrize("sentence", [
    "Bypass mode is never used outside an isolated container with no credentials.",
    "We never use float for money.",
    "Nobody approves their own pull request.",
    "The label is not optional.",
])
def test_the_same_topics_stated_safely_pass(work, sentence):
    put(work, swap(REFERENCE, "## 2. Data rules\n", f"## 2. Data rules\n\n{sentence}\n"))
    assert m.N_CONTRADICT not in failing(work), sentence


def test_a_playbook_that_never_mentions_production_fails(work):
    text = REFERENCE.replace("production", "the live system")
    put(work, text)
    assert m.N_PROD in failing_required(work)


def test_the_module_the_old_architecture_page_lists_does_not_exist(work):
    put(work, swap(REFERENCE, "## 3. Context and memory\n", "## 3. Context and memory\n\nLimits and screening live in `src/remit/risk.py`, which agents must not rewrite.\n"))
    found = results(work)
    assert not found[m.N_PATHS].ok and "risk.py" in found[m.N_PATHS].detail


def test_a_proposed_new_file_is_not_a_missing_file(work):
    put(work, swap(REFERENCE, "## 3. Context and memory\n", "## 3. Context and memory\n\nWe will add a new file `tests/test_policy.py` for this.\n"))
    assert m.N_PATHS not in failing(work)


@pytest.mark.parametrize("claim", [
    "Studies show that AI assistants make teams 55% more productive.",
    "Research proves developers are 10x faster with agents.",
    "According to a recent survey, most teams save two hours a day.",
    "The industry average is a 40% productivity gain.",
])
def test_unsourced_productivity_claims_fail(work, claim):
    put(work, swap(REFERENCE, "## 8. Metrics plan\n", f"## 8. Metrics plan\n\n{claim}\n"))
    assert m.N_CLAIMS in failing_required(work), claim


def test_a_sourced_claim_with_its_limits_is_allowed(work):
    put(work, swap(REFERENCE, "## 8. Metrics plan\n", "## 8. Metrics plan\n\nStudies show mixed results; the METR trial of 2025 found experienced developers slower.\n"))
    assert m.N_CLAIMS not in failing(work)


def test_copy_pasted_sections_are_noticed(work):
    block = "Agents run on a managed laptop, in a clean working tree on a feature branch, and never on a production host. " * 4
    text = REFERENCE.replace("## 7. Automation\n", f"## 7. Automation\n\n{block}\n").replace("## 6. Security baseline\n", f"## 6. Security baseline\n\n{block}\n")
    put(work, text)
    # the two sections now differ (each keeps its own text), so this must NOT be flagged ...
    assert m.N_DISTINCT not in failing(work)
    # ... but two identical bodies must
    doc = m.parse("## 1. Tools\n" + block + "\n\n## 2. Data rules\n" + block + "\n")
    sections = m.find_sections(doc)
    assert not m.distinct_check(sections).ok


# --------------------------------------------------------------------------------------------------------------
# a draft that follows the ticket but has the flaws an assistant's draft tends to have (constructed for teaching,
# not recorded from a model): lesson 12.2 shows the grade of this state
# --------------------------------------------------------------------------------------------------------------
ACCEPTANCE_BLOCK = """\
### Suggestion acceptance rate
- Kind: delivery
- Definition: Suggestions accepted divided by suggestions shown, per developer, per week, taken from the IDE telemetry.
- Source: IDE telemetry
- Cadence: weekly, Tariq
- Baseline: to be measured
- Threshold: Target: at least 30%

"""

TICKET_DRAFT_EDITS = [
    # a rule whose check names no mechanism
    ("Check: the secret scan runs in CI on every pull request, and Noura reads ten agent logs a month.", "Check: team lead review."),
    # a weasel word in a rule
    ("MUST NOT use `float` for money. Check:", "MUST NOT use `float` for money where possible. Check:"),
    # an unsourced claim
    ("## 8. Metrics plan\n\n", "## 8. Metrics plan\n\nStudies show that AI assistants make developers 55% more productive.\n\n"),
    # an invented baseline
    ("- Baseline: 52 hours (median, last quarter).", "- Baseline: 4 hours (median, last quarter)."),
    # a vanity metric instead of the rework guard
    (None, None),
    # a guard with no number and no response
    ("Over 16 hours in any week, we review the queue at the clinic and cap new agent work until it clears.", "Keep it low."),
    # the module the old architecture page still lists
    ("The repository has one `CLAUDE.md` at the root.", "Limits and screening are described in `src/remit/risk.py`. The repository has one `CLAUDE.md` at the root."),
    # no number in the diff limit
    ("It changes at most\n400 lines (additions plus deletions, generated files excluded) and contains one logical change.", "It is kept small and contains one logical change."),
    ("- MUST NOT merge a pull request of more than 400 changed lines. Check: a CI step counts changed lines and fails\n  above the limit; the author splits the work instead.",
     "- MUST NOT merge a pull request that is too big to review. Check: the pr-hygiene CI job warns on large diffs."),
    # one money module forgotten
    ("`fx.py`, `limits.py`, `ledger.py` or `service.py` need", "`fx.py`, `limits.py` or `service.py` need"),
]


def ticket_draft() -> str:
    text = REFERENCE
    for old, new in TICKET_DRAFT_EDITS:
        if old is None:
            a = text.index("### Rework rate")
            b = text.index("### Review turnaround")
            text = text[:a] + ACCEPTANCE_BLOCK + text[b:]
        else:
            text = swap(text, old, new)
    return text


EXPECTED_DRAFT_FAILURES = {
    m.N_RULE_CHECK, m.N_RULE_VAGUE, m.N_REV_SIZE, m.N_REV_MONEY, m.N_MET_GUARD, m.N_MET_BASELINE, m.N_MET_VANITY,
    m.N_PATHS, m.N_CLAIMS,
}


def test_the_ticket_following_draft_fails_exactly_where_the_lesson_says(work):
    put(work, ticket_draft())
    assert failing_required(work) == EXPECTED_DRAFT_FAILURES
    found = results(work)
    assert "team lead review" not in found[m.N_RULE_CHECK].hint  # hints never quote the learner either
    assert "risk.py" in found[m.N_PATHS].detail and "line" in found[m.N_CLAIMS].detail


# --------------------------------------------------------------------------------------------------------------
# the same content in other forms must pass
# --------------------------------------------------------------------------------------------------------------
def variants():
    yield "headings one level up", re.sub(r"^(#{2,3}) ", lambda hit: "#" * (len(hit.group(1)) - 1) + " ", REFERENCE, flags=re.M)
    yield "no numbers in the headings", re.sub(r"^## \d+\. ", "## ", REFERENCE, flags=re.M)
    yield "numbered rules", re.sub(r"^- MUST", "1. MUST", REFERENCE, flags=re.M)
    yield "rule ids in bold", re.sub(r"^- MUST", "- **R-1.** MUST", REFERENCE, flags=re.M)
    yield "verified by", REFERENCE.replace(" Check: ", " Verified by: ")
    yield "check in bold", REFERENCE.replace(" Check: ", " **Check:** ")
    yield "bold field names", re.sub(r"^- (Kind|Definition|Source|Cadence|Baseline|Threshold):", r"- **\1:**", REFERENCE, flags=re.M)
    yield "unwrapped paragraphs", re.sub(r"(?<=\S)\n(?=[A-Za-z`(])(?<!\n- )", " ", REFERENCE) if False else REFERENCE.replace(",\n", ", ").replace("\n  ", " ")
    yield "windows line endings", REFERENCE.replace("\n", "\r\n")
    yield "target spelled out", REFERENCE.replace("- Threshold: Target:", "- Target:")
    yield "tools and ampersands", REFERENCE.replace("## 1. Tools and environments", "## 1. Tools & environments").replace("## 3. Context and memory", "## 3. Context & memory")
    yield "heading with a trailing colon", REFERENCE.replace("## 5. Verification standard", "## 5. Verification standard:")


@pytest.mark.parametrize("label, text", list(variants()), ids=[label for label, _ in variants()])
def test_other_forms_of_the_same_playbook_pass(work, label, text):
    put(work, text)
    assert failing_required(work) == set(), (label, {n: c.detail for n, c in results(work).items() if not c.ok and c.required})


def test_a_check_on_its_own_sub_bullet_counts(work):
    text = re.sub(r"^(- MUST[^\n]*?) Check: ([^\n]*)", r"\1\n  - Check: \2", REFERENCE, flags=re.M)
    put(work, text)
    found = results(work)
    assert found[m.N_RULE_CHECK].ok, found[m.N_RULE_CHECK].detail


def test_rules_in_a_fence_do_not_count(work):
    fenced = "```markdown\n" + "\n".join(f"- MUST NOT do thing {i}. Check: the CI job {i}." for i in range(14)) + "\n```\n"
    put(work, SKELETON + "\n" + fenced)
    assert m.N_RULE_COUNT in failing_required(work)


# --------------------------------------------------------------------------------------------------------------
# hygiene shortcuts: scope, secrets, commits
# --------------------------------------------------------------------------------------------------------------
def test_the_reference_passes_the_whole_grade(template, tmp_path):
    work = tmp_path / "work"
    shutil.copytree(template, work)
    framework.solve_lab(framework.load_lab("m12"), work)
    assert framework.passed(framework.grade_lab(framework.load_lab("m12"), work))


def test_editing_contributing_to_fit_the_playbook_is_caught(work):
    put(work, REFERENCE)
    contributing = work / "CONTRIBUTING.md"
    contributing.write_text(contributing.read_text(encoding="utf-8").replace("Money logic needs a second reviewer.", "Money logic is reviewed by the author."), encoding="utf-8")
    commit(work)
    found = {c.name: c for c in m.repository_checks(work)}
    assert not found[m.N_SCOPE].ok and "CONTRIBUTING.md" in found[m.N_SCOPE].detail


def test_editing_the_tests_or_the_facts_is_caught(work):
    put(work, REFERENCE)
    (work / "lab-assets" / "team-context.md").write_text("changed\n", encoding="utf-8")
    (work / "tests" / "test_money.py").write_text("# gutted\n", encoding="utf-8")
    commit(work)
    found = {c.name: c for c in m.repository_checks(work)}
    assert not found[m.N_SCOPE].ok


def test_an_uncommitted_playbook_fails_the_commit_checks(work):
    put(work, REFERENCE)
    found = {c.name: c for c in m.repository_checks(work)}
    assert not found[m.N_COMMITS].ok and not found[m.N_CLEAN].ok


def test_a_commit_message_that_ignores_the_convention_fails(work):
    put(work, REFERENCE)
    commit(work, "Added the AI playbook.")
    found = {c.name: c for c in m.repository_checks(work)}
    assert not found[m.N_COMMITS].ok and found[m.N_SCOPE].ok


def test_several_good_commits_are_fine(work):
    put(work, SKELETON.replace("<<a named person>>", "Tariq"))
    commit(work, "docs(playbook): start the playbook")
    put(work, REFERENCE)
    commit(work, "docs(playbook): finish the playbook")
    found = {c.name: c for c in m.repository_checks(work)}
    assert all(c.ok for c in found.values()), {n: c.detail for n, c in found.items() if not c.ok}


def test_a_secret_in_the_playbook_is_caught(work):
    key = "AKIA" + "ABCDEFGHIJKLMNOP"  # built in pieces so this file holds no key-shaped literal
    put(work, REFERENCE + f"\nExample of what the scan finds: {key}\n")
    commit(work)
    found = {c.name: c for c in m.repository_checks(work)}
    assert not found[m.N_SECRETS].ok


def test_a_missing_file_waits_and_does_not_crash(work):
    (work / "playbook.md").unlink()
    found = results(work)
    assert not found[m.N_EXISTS].ok
    assert [c.name for c in m.playbook_checks(work)] == [n for n in m.ALL_NAMES if n in m._FILE_CHECKS]  # noqa: SLF001


def test_an_empty_or_binary_file_does_not_crash(work):
    put(work, "")
    assert failing_required(work)
    (work / "playbook.md").write_bytes(b"\xff\xfe\x00\x01 not utf-8 \xff")
    assert not results(work)[m.N_EXISTS].ok


def test_grading_a_huge_file_is_fast(work):
    put(work, (REFERENCE + "\n") * 40)
    began = time.monotonic()
    m.playbook_checks(work)
    assert time.monotonic() - began < 3


def test_the_check_names_are_unique_and_the_advisory_set_is_known(template):
    names = [c.name for c in m.all_checks(template)]
    assert len(names) == len(set(names)) == len(m.ALL_NAMES)
    assert {c.name for c in m.all_checks(template) if not c.required} == m.ADVISORY


# --------------------------------------------------------------------------------------------------------------
# the parser
# --------------------------------------------------------------------------------------------------------------
def test_soft_wrapped_lines_are_one_sentence():
    doc = m.parse("## Tools\nWe do not\nmeasure lines of code.\n\n- MUST A\n  more of A\n- MUST B\n")
    assert [text for _, text in doc.logical()] == ["## Tools", "We do not measure lines of code.", "- MUST A more of A", "- MUST B"]


def test_headings_inside_fences_are_ignored():
    doc = m.parse("## Real\n```text\n## Not a heading\n```\n## Also real\n")
    assert [h.title for h in doc.headings] == ["Real", "Also real"]


def test_the_section_level_is_the_one_that_matches_most():
    text = "# Title\n\n" + "\n".join(f"## {t}\nbody\n" for t in ["Tools", "Data", "Memory", "Review", "Verification"])
    sections = m.find_sections(m.parse(text))
    assert set(sections) == {"tools", "data", "context", "review", "verification"}


def test_a_metric_named_like_a_section_is_not_taken_for_one():
    text = (
        "## 4. Spec and review norms\nbody\n\n## 8. Metrics plan\n\n### Review turnaround\n- Kind: guard\n- Definition: x\n\n## 9. Incident handling\nbody\n"
    )
    sections = m.find_sections(m.parse(text))
    assert sections["review"].heading.title == "4. Spec and review norms"


@pytest.mark.parametrize("item, is_rule", [
    ("- MUST do a thing. Check: CI.", True),
    ("- MUST NOT do a thing. Check: CI.", True),
    ("- **R1.** MUST NOT do a thing. Check: CI.", True),
    ("- R-DATA-2: MUST do a thing. Check: CI.", True),
    ("1. MUST do a thing. Check: CI.", True),
    ("- **MUST NOT** do a thing. Check: CI.", True),
    ("- **D1 (data):** MUST NOT do a thing. Check: CI.", True),
    ("- Data rule 3 \u2014 MUST do a thing. Check: CI.", True),
    ("- Agents MUST NOT do a thing. Check: CI.", False),
    ("- Note: you MUST do a thing. Check: CI.", False),
    ("- must do a thing. Check: CI.", False),
    ("- You MUST do a thing. Check: CI.", False),
    ("MUST do a thing. Check: CI.", False),   # not a list item
])
def test_rule_shapes(item, is_rule):
    doc = m.parse("## 2. Data rules\n\n" + item + "\n")
    rules = m.extract_rules(doc, m.find_sections(doc))
    assert bool(rules) is is_rule
    if is_rule:
        assert rules[0].check == "CI." and rules[0].section == "data"


def test_the_family_of_a_metric_name():
    assert m.family("Lead time for changes") == "lead time"
    assert m.family("Deployment frequency") == "deployment frequency"
    assert m.family("Change failure rate") == "change failure rate"
    assert m.family("Failed deployment recovery time") == "recovery time"
    assert m.family("Time to restore service") == "recovery time"
    assert m.family("Rework rate") == "rework rate"
    assert m.family("Review turnaround") is None
    assert m.family("Lines of code") is None


def test_a_lab_asset_with_absolute_paths_or_hidden_mentions_is_not_in_the_task():
    task = (HERE / "task.md").read_text(encoding="utf-8")
    assert "/home/" not in task and "hidden/" not in task and "team-context.md" in task
    assert LEARNER[0]  # the shared identity used by the commits above
    assert gitutil.TAG_START == "lab-start"


# --------------------------------------------------------------------------------------------------------------
# the lesson and the grader must agree
# --------------------------------------------------------------------------------------------------------------
MODULE = Path(m.__file__).resolve().parents[2] / "modules" / "12-teams.md"


@pytest.mark.skipif(not MODULE.is_file(), reason="the lesson file is written separately")
def test_the_lessons_examples_pass_the_graders_own_checks():
    text = MODULE.read_text(encoding="utf-8")
    # lesson 12.2: the four wish -> rule rows are rules with a mechanism and no weasel word
    rules = re.findall(r"^\| [^|]+ \| (MUST[^|]+) \|$", text, flags=re.M)
    assert len(rules) == 4
    doc = m.parse("## 2. Data rules\n\n" + "\n".join(f"- {rule}" for rule in rules) + "\n")
    parsed = m.extract_rules(doc, m.find_sections(doc))
    assert len(parsed) == 4
    for rule in parsed:
        assert rule.check and m.MECHANISM.search(rule.check) and not m.VAGUE.search(rule.text), rule.text
    # lesson 12.2: the filled metric block is a good guard block, and it is not a block of the reference playbook
    block = re.search(r"```markdown\n(### Pull request size\n.*?)```", text, flags=re.S).group(1)
    assert "### Pull request size" not in REFERENCE and block.strip() not in REFERENCE
    doc = m.parse("## 8. Metrics plan\n\n" + block)
    blocks = m.metric_blocks(doc, m.find_sections(doc)["metrics"])
    assert len(blocks) == 1 and blocks[0].kind == "guard" and m.family(blocks[0].name) is None
    assert m.definition_problems(blocks[0]) == [] and all(blocks[0].fields.get(f) for f in m.FIELDS)
    assert m.threshold_problems(blocks[0].fields["Threshold"]) == []
    assert not m.is_adoption(blocks[0]) and not m._VANITY.search(block)  # noqa: SLF001
    assert not re.findall(r"\d+", blocks[0].fields["Baseline"]) and "to be measured" in blocks[0].fields["Baseline"]
    assert m.baseline_figures(blocks[0].name) == {m.QUARTER_WEEKS}  # no figure of the facts file belongs to it
    # lesson 12.2: the weak definition really fails, and the guard sentence really passes
    assert m.definition_problems(m.Metric("Pull request size", 0, {"Definition": "how big our pull requests are"}))
    assert m.definition_problems(m.Metric("Lead time", 0, {"Definition": "how fast we ship"}))
    assert m.threshold_problems("Above 15% over any four weeks, we stop raising agent autonomy and review each failed change") == []
    # lesson 12.1: every row of the guard table has a number, a comparison and a response
    rows = re.findall(r"^\| (Change failure rate|Rework rate|Review turnaround|AI-related incidents) \| ([^|]+) \| ([^|]+) \|$", text, flags=re.M)
    assert len(rows) == 4
    for name, threshold, response in rows:
        assert m.threshold_problems(f"{threshold.strip()}: {response.strip()}") == [], name
        assert m.family(name) in (None, "change failure rate", "rework rate")
    # lesson 12.2 quiz: the rule the answer calls a rule is one, and the SHOULD one is not
    good = "- MUST get a second human approval on `fees.py`. Check: branch protection requires two approvals there"
    bad = "- SHOULD review AI-written code before it merges. Check: the culture of mutual respect on the team"
    for item, expected in ((good, 1), (bad, 0)):
        doc = m.parse("## 4. Spec and review norms\n\n" + item + "\n")
        assert len(m.extract_rules(doc, m.find_sections(doc))) == expected
    # lesson 12.2 quiz: the complete guard entry has a number, a comparison and a response; the weak ones do not
    assert m.threshold_problems("more than 20% of deployments in a quarter, and Nada reviews those tests") == []
    for weak in ("keep it low, and watch it closely at the clinic every single week",
                 "it should not rise from one quarter to the next, whatever else changes",
                 "reviewed weekly by the engineering lead for any change that ships late"):
        assert m.threshold_problems(weak), weak


def lesson_text_blocks(text: str) -> list[list[str]]:
    """The lines of every ``text`` fence of lesson 12.2 that starts with a grade line."""
    lesson = text[text.index("# 12.2 \u2014"):]
    blocks = re.findall(r"```text\n(.*?)```", lesson, flags=re.S)
    return [block.splitlines() for block in blocks if block.lstrip().startswith("[")]


def printed(work: Path) -> list[str]:
    """What ``ailab grade`` prints for the work directory, without the hint lines."""
    code, out, _ = run_cli("grade", "m12", "--dir", str(work))
    return [line for line in out.splitlines() if not line.startswith("       hint:")]


def matches_in_order(shown: list[str], real: list[str]) -> None:
    """Every shown line is a real line, in the real order; ``...`` stands for any lines left out."""
    position = 0
    for line in shown:
        if line in ("...", ""):
            continue
        assert line in real[position:], f"the lesson shows a line the grader does not print: {line!r}"
        position = real.index(line, position) + 1


@pytest.mark.skipif(not MODULE.is_file(), reason="the lesson file is written separately")
def test_the_lessons_sample_output_is_what_the_grader_really_prints(work):
    """Lesson 12.2 quotes the grade of the untouched starter and of a draft that follows the ticket."""
    starter, draft = lesson_text_blocks(MODULE.read_text(encoding="utf-8"))[:2]
    real_starter = printed(work)
    matches_in_order(starter, real_starter)
    assert starter[-1] == real_starter[-1]  # the verdict line
    put(work, ticket_draft())
    learner_commit(work, "docs(playbook): write the first draft")
    real_draft = printed(work)
    matches_in_order(draft, real_draft)
    assert draft[-1] == real_draft[-1] and "26/35" in draft[-1]
    # the failing lines the lesson cut with "..." are the three it names: a weasel word, a diff limit, a claim
    cut = [line for line in real_draft if line.startswith("[FAIL]") and line not in draft]
    names = sorted(n for n in m.ALL_NAMES if any(line.startswith(f"[FAIL] {n}") for line in cut))
    assert len(cut) == 3 and names == sorted([m.N_RULE_VAGUE, m.N_REV_SIZE, m.N_CLAIMS])


# --------------------------------------------------------------------------------------------------------------
# fairness: sound sentences in other words must pass (found by probing the grader with different vocabulary)
# --------------------------------------------------------------------------------------------------------------
def section_of(title: str, key: str, body: str) -> m.Section:
    doc = m.parse(f"## 1. {title}\n{body}\n")
    return m.find_sections(doc)[key]


@pytest.mark.parametrize("sentence", [
    "An agent must never modify an existing test to make a change pass.",
    "Agents may not change or loosen existing tests to get a green build.",
    "Nobody, human or agent, may alter, weaken or delete a test to pass.",
    "Never tamper with the tests so that they pass.",
    "No agent may touch the existing tests to make them pass.",
    "Do not game the suite by overwriting expected values.",
])
def test_other_ways_to_protect_the_tests_pass(sentence):
    section = section_of("Verification standard", "verification", f"Run `pytest -q`. Money is `Decimal`, never `float`. {sentence}")
    assert m.verification_checks(section)[0].ok, sentence


@pytest.mark.parametrize("sentence", [
    "MUST keep the suite green.",
    "New behaviour has a test that fails without the change.",  # a different rule: not "do not weaken the tests"
])
def test_a_sentence_that_does_not_protect_the_tests_still_fails(sentence):
    section = section_of("Verification standard", "verification", f"Run `pytest -q`. Money is `Decimal`, never `float`. {sentence}")
    assert not m.verification_checks(section)[0].ok, sentence


MONEY = "(`money.py`, `fees.py`, `fx.py`, `limits.py`, `ledger.py`, `service.py`)"


@pytest.mark.parametrize("sentence, ok", [
    (f"Money logic {MONEY} needs two approvals.", True),
    (f"Money logic {MONEY} must be approved by a different person from the author.", True),
    (f"Money logic {MONEY} must be approved by two people, one of them not the author.", True),
    (f"Money logic {MONEY} gets four-eyes review.", True),
    (f"Money logic {MONEY} needs a second reviewer who is human.", True),
    (f"Money logic {MONEY} is reviewed carefully by the team.", False),
    (f"Money logic {MONEY} must be reviewed by the author before the pull request is opened.", False),
])
def test_other_ways_to_say_a_second_human_reviews_money_logic(sentence, ok):
    body = ("A pull request that an AI tool shaped carries the label `AI-assisted`, has at most 300 changed lines, and its author "
            "explains what the agent did and the commands run. The first review comes within 4 hours. " + sentence)
    found = {c.name: c for c in m.review_checks(section_of("Spec and review norms", "review", body))}
    assert found[m.N_REV_MONEY].ok is ok, found[m.N_REV_MONEY].detail


@pytest.mark.parametrize("sentence", [
    "The author explains the change and lists which commands were run.",
    "The author explains the change and pastes the test results.",
    "The author explains the change, and the description shows what was run.",
])
def test_other_ways_to_ask_for_evidence_in_the_description_pass(sentence):
    body = ("A pull request that an AI tool shaped carries the label `AI-assisted` and has at most 300 changed lines. "
            f"{sentence} The first review comes within 4 hours. A second human reviews {MONEY}.")
    found = {c.name: c for c in m.review_checks(section_of("Spec and review norms", "review", body))}
    assert found[m.N_REV_AUTHOR].ok, found[m.N_REV_AUTHOR].detail


def test_the_missing_file_hint_says_a_new_file_is_fine(work):
    put(work, REFERENCE + "\nThe check is `check_diff_size.py`, run in CI.\n")
    assert "propose to create" in results(work)[m.N_PATHS].hint


@pytest.mark.skipif(not MODULE.is_file(), reason="the lesson file is written separately")
def test_the_measurable_versions_in_lesson_12_1_pass_the_graders_definition_check():
    """A reader who copies a 'measurable version' from the table into a metric block must not be failed for it."""
    text = MODULE.read_text(encoding="utf-8")
    rows = re.findall(r"^\| ((?:Change lead time|Deployment frequency|Failed deployment recovery time|Change fail rate[^|]*|Deployment rework rate)) \| [^|]+ \| ([^|]+) \|$", text, flags=re.M)
    assert len(rows) == 5
    for name, definition in rows:
        problems = m.definition_problems(m.Metric(name.split(" (")[0], 0, {"Definition": definition.strip()}))
        assert problems == [], (name, problems)
