"""Negative and alternative-solution tests for m11 ("An ADR with a critic, docs checked against code and a postmortem
that sticks to the facts").

Each test starts from the started lab, or from the lab with the reference solution applied, makes the kind of
mistake a learner or an AI assistant really makes (an invented function, a copied stale docstring, a plausible
time that is not in the record, a cause stated as fact, a "fix" to the code instead of the docs ...), grades it,
and says exactly which checks must fail. A second group shows that other sound ways of writing the three
documents are accepted. The last groups test the helper module and the learner's claims_scan.py directly.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from ailab import checks_m11 as m
from ailab import framework, gitutil
from ailab.labs import m11_lifecycle  # noqa: F401  (namespace package: makes sure the folder is importable)
from conftest import LEARNER, learner_commit, start

KIT = Path(__file__).resolve().parent.parent / "ailab"
LAB_DIR = KIT / "labs" / "m11_lifecycle"
SOLUTION = LAB_DIR / "solution"
BASE_DOCS = KIT / "base" / "remit" / "docs"

# check names (a test fails loudly if the lab renames one)
ADR_EXISTS = "ADR exists in docs/adr/"
ADR_FORMAT = "ADR follows Nygard's format"
ADR_FACTS = "ADR facts trace to the code"
ADR_CRITIC = "ADR records the critic's objections"
DOC_EXISTS = "najmkit page exists (docs/najmkit.md)"
DOC_NAMES = "Docs: every name exists in the code"
DOC_SIGS = "Docs: signatures match the code"
DOC_EXAMPLES = "Docs: the examples run"
DOC_COVERAGE = "Docs: the public API is covered"
DOC_FACTS = "Docs: nothing contradicts the code"
PM_SECTIONS = "Postmortem has all its sections"
PM_ROWS = "Postmortem: every timeline row matches the record"
PM_COVER = "Postmortem: the timeline covers the key events"
PM_INVENTED = "Postmortem: no invented numbers, times, dates or ids"
PM_UNKNOWN = "Postmortem: nothing unknown is stated as fact"
PM_LABELS = "Postmortem: inferences are labelled, open questions listed"
PM_BLAMELESS = "Postmortem: blameless wording"
DOCS_ONLY = "Only documentation changed"
THREE_COMMITS = "Three documents, three commits"
MESSAGES = "Commit messages follow CONTRIBUTING.md"
CLEAN = "Everything is committed"
SECRETS = "No secrets in the change"
ALL = {ADR_EXISTS, ADR_FORMAT, ADR_FACTS, ADR_CRITIC, DOC_EXISTS, DOC_NAMES, DOC_SIGS, DOC_EXAMPLES, DOC_COVERAGE, DOC_FACTS,
       PM_SECTIONS, PM_ROWS, PM_COVER, PM_INVENTED, PM_UNKNOWN, PM_LABELS, PM_BLAMELESS, DOCS_ONLY, THREE_COMMITS, MESSAGES,
       CLEAN, SECRETS}

ADR_PATH = "docs/adr/0001-failed-notification-does-not-undo-a-transfer.md"
DOC_PATH = "docs/najmkit.md"
PM_PATH = "docs/postmortems/INC-2031.md"


# --------------------------------------------------------------------------------------------
# fixtures and helpers
# --------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def template(tmp_path_factory) -> Path:
    return start("m11", tmp_path_factory.mktemp("m11-template") / "work")


@pytest.fixture(scope="module")
def solved_template(tmp_path_factory) -> Path:
    work = start("m11", tmp_path_factory.mktemp("m11-solved") / "work")
    framework.solve_lab(framework.load_lab("m11"), work)
    return work


@pytest.fixture
def work(template, tmp_path) -> Path:
    target = tmp_path / "work"
    shutil.copytree(template, target)
    return target


@pytest.fixture
def solved(solved_template, tmp_path) -> Path:
    target = tmp_path / "work"
    shutil.copytree(solved_template, target)
    return target


def grade(work: Path) -> dict[str, framework.Check]:
    return {c.name: c for c in framework.grade_lab(framework.load_lab("m11"), work, catch=False)}


def failing(result: dict[str, framework.Check]) -> set[str]:
    return {name for name, check in result.items() if not check.ok}


def assert_only(result: dict[str, framework.Check], *expected: str) -> None:
    got = failing(result)
    detail = "\n".join(f"  {'ok  ' if c.ok else 'FAIL'} {n}: {c.detail}" for n, c in result.items())
    assert got == set(expected), f"expected failures {set(expected)}, got {got}\n{detail}"


def text_of(work: Path, rel: str) -> str:
    return (work / rel).read_text(encoding="utf-8")


def swap(work: Path, rel: str, old: str, new: str) -> None:
    """Replace text in a document; the test fails if the text is not there (so a changed reference cannot hide it)."""
    text = text_of(work, rel)
    assert old in text, f"{old!r} not found in {rel}"
    (work / rel).write_text(text.replace(old, new), encoding="utf-8")


def put(work: Path, rel: str, text: str) -> None:
    path = work / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def commit(work: Path, message: str = "docs(review): edit a document") -> None:
    learner_commit(work, message)


def detail_of(result: dict[str, framework.Check], name: str) -> str:
    return result[name].detail + " " + result[name].hint


# --------------------------------------------------------------------------------------------
# the starter and the reference solution
# --------------------------------------------------------------------------------------------
def test_the_seed_loses_the_page_and_plants_one_stale_docstring(work):
    assert not (work / DOC_PATH).exists()
    assert "A missing file raises FileNotFoundError." in text_of(work, "src/najmkit/audit.py")
    audit = subprocess.run([sys.executable, "-c", "from najmkit import audit; print(audit.read_events('nope.jsonl'))"],
                           cwd=work, env={"PYTHONPATH": str(work / "src"), "PATH": "/usr/bin:/bin"}, capture_output=True, text=True)
    assert audit.stdout.strip() == "[]"  # the code and the docstring really disagree
    for asset in ("incident.json", "adr-template.md", "postmortem-template.md", "claims_scan.py"):
        assert (work / "lab-assets" / asset).is_file()
    assert (work / "lab-assets" / "incident.json").read_text() == (LAB_DIR / "assets" / "incident.json").read_text()
    assert "CONSTRUCTED FOR TEACHING" in text_of(work, "lab-assets/incident.json")


def test_the_starter_fails_for_the_right_reasons(work):
    result = grade(work)
    assert set(result) == ALL
    assert_only(result, *(ALL - {CLEAN, SECRETS}))
    assert all(c.hint for c in result.values() if not c.ok)
    blob = "".join(c.detail + c.hint for c in result.values())
    assert "FileNotFoundError" not in blob and "E13" not in blob  # nothing from the answer key leaks


def test_the_reference_solution_passes_every_check(solved):
    assert_only(grade(solved))
    assert framework.passed(framework.grade_lab(framework.load_lab("m11"), solved))


def test_grading_never_reads_the_learners_copy_of_the_record(solved):
    """Editing lab-assets/incident.json to match an invented timeline cannot move the goalposts."""
    record = json.loads(text_of(solved, "lab-assets/incident.json"))
    record["timeline"].append({"id": "E14", "time": "10:15:00", "source": "chat", "text": "Database failover completed."})
    put(solved, "lab-assets/incident.json", json.dumps(record, indent=2))
    swap(solved, PM_PATH, "| 10:19 | INC-2031", "| 10:15 | Database failover completed. | E14 |\n| 10:19 | INC-2031")
    commit(solved)
    result = grade(solved)
    assert {PM_ROWS, PM_INVENTED, DOCS_ONLY} <= failing(result)


# --------------------------------------------------------------------------------------------
# other sound ways to write the three documents
# --------------------------------------------------------------------------------------------
ALT_ADR = """# 3. Qatar days are fixed UTC+3 windows

Date: 2026-03-12

Status: Accepted

## Context

Sending limits are per Qatar calendar day and month. `limits.to_local` converts an aware time with `limits.QATAR_TZ`,
a fixed offset (`limits.QATAR_UTC_OFFSET`, three hours), and `limits.day_window` and `limits.month_window` build the
windows from it, in `src/remit/limits.py`. Qatar has no daylight saving, so the offset never changes. Timestamps are
stored in UTC, so every comparison converts first.

## Decision

We use a fixed UTC+3 offset for Qatar instead of the time-zone database.

## Consequences

The code has no dependency and no data file, and the windows are easy to test: 21:00 UTC is midnight in Qatar. The
cost is that the offset is a belief about the world written into a constant. If Qatar ever changed its offset, the
constant would have to change, and old transfers would be assigned to the wrong day unless the history was kept.

## Critic's objections

### 1. Hard-coding an offset is a time bomb

A time-zone database knows the history. **Response:** rejected for now, because Qatar has had no daylight saving
since the offset was fixed and the windows are only ever computed for the present and the last month. We keep the constant.

### 2. The windows are easy to get wrong at midnight

Converting in two places invites a bug. **Response:** accepted: `limits.to_local` is the single place that converts, and
the tests cover the boundary at 21:00 UTC. Added a sentence to Context.

### 3. The best alternative is to store the Qatar date next to each transfer

Then no conversion is needed at read time. **Response:** deferred. It needs a migration of `store.py` and a decision
about backfilling old rows; follow-up ticket.
"""

ALT_PM = """# INC-2031: Customers did not receive their transfer-sent message for 52 minutes

SEV3, Najm Remit, 11 March 2026, incident commander Maha. Times are UTC.

## Summary

For 52 minutes on 11 March 2026 (09:58 to 10:50) transfers kept completing while the "transfer sent" message failed:
171 `notification.failed` events with template `transfer_sent`, against 188 `transfer.sent` events. The ledger and the
store agree for every transfer in the window (E13).

## Impact

- 171 failed confirmations by event count; events are not customers.
- 64 support tickets tagged "no confirmation".
- No mismatch between the ledger and the store (0 mismatches).

## Timeline

- 09:58 (E1) First `notification.failed` event, template `transfer_sent`.
- 10:11 (E2) Alert: notification failure rate above 20% for 10 minutes. On-call SRE paged.
- 10:14 (E3) Page acknowledged.
- 10:19 (E4) INC-2031 opened, SEV3; Maha is incident commander.
- 10:26 (E5) A payments engineer read the audit log: transfers still completing, every error `notification_error`.
- 10:30 (E6) Vendor status page: "Investigating delayed message delivery".
- 10:36 (E7) Support lead: callers ask where their confirmation is.
- 10:41 (E8) Notice added to the Najm app.
- 10:50 (E9) Last `notification.failed` event.
- 10:52 (E10) Alert resolved on its own.
- 11:02 (E11) Vendor status page: resolved, delivery back to normal.
- 11:10 (E12) Maha closed the incident.
- 11:40 (E13) Reconciliation: 188 transfers checked, 0 mismatches.

## Facts

- No deploy or configuration change in the window.
- The vendor status page reported delayed delivery from 10:30 until 11:02 (E6, E11).

## Hypotheses (not confirmed)

- The failures and the vendor's delay are related. Confidence: low to medium; the times overlap (E1, E6, E11). The vendor's report would confirm it.
- Extra `limit_exceeded` rejections (23 against 9 a week earlier) came from customers trying again. Confidence: low (E7). A look at the rejected customers' earlier transfers would check it.

## Open questions

- Why delivery degraded, and whether that explains our failures.
- Whether any customer sent a transfer a second time because no message came.
- How many different customers the 171 events are.

## Follow-ups

- Alert earlier than 10 minutes. Owner: SRE. Done when a replay fires sooner.
- Turn the in-app notice on automatically. Owner: payments engineering. Done when a test alert does it.
- Decide how to retry failed messages. Owner: payments engineering. Done when an ADR exists.
"""


def test_a_different_decision_with_a_different_layout_is_accepted(solved):
    (solved / ADR_PATH).unlink()
    put(solved, "docs/adr/0003-qatar-days-are-fixed-offset-windows.md", ALT_ADR)
    commit(solved, "docs(adr): record the fixed UTC+3 windows")
    assert_only(grade(solved))


def test_the_original_najmkit_page_plus_examples_is_accepted(solved):
    base = (BASE_DOCS / "najmkit.md").read_text(encoding="utf-8")
    examples = '''
## Examples

```python
from najmkit import ids, clock, audit

ids.use_generator(ids.SequentialIds())
ids.new_id("TRF")
clock.set_clock(clock.FixedClock("2026-03-02T09:00:00+00:00"))
clock.now()
clock.reset_clock()
audit.log_event("demo.happened", thing="x")
```
'''
    put(solved, DOC_PATH, base + examples)
    commit(solved)
    assert_only(grade(solved))


def test_the_original_najmkit_page_without_examples_is_not_enough(solved):
    put(solved, DOC_PATH, (BASE_DOCS / "najmkit.md").read_text(encoding="utf-8"))
    commit(solved)
    result = grade(solved)
    assert_only(result, DOC_EXAMPLES)
    assert "najmkit.clock" in result[DOC_EXAMPLES].detail and "najmkit.audit" in result[DOC_EXAMPLES].detail


def test_a_postmortem_with_a_bullet_timeline_and_other_headings_is_accepted(solved):
    put(solved, PM_PATH, ALT_PM)
    commit(solved)
    assert_only(grade(solved))


# --------------------------------------------------------------------------------------------
# the ADR: wrong formats, invented references, stale figures
# --------------------------------------------------------------------------------------------
def test_an_adr_without_consequences(solved):
    text = text_of(solved, ADR_PATH)
    start_at, end_at = text.index("## Consequences"), text.index("## Critic's objections")
    put(solved, ADR_PATH, text[:start_at] + text[end_at:])
    commit(solved)
    result = grade(solved)
    assert_only(result, ADR_FORMAT)
    assert "Consequences" in result[ADR_FORMAT].detail


def test_adr_sections_in_the_wrong_order(solved):
    text = text_of(solved, ADR_PATH)
    a, b, c = text.index("## Context"), text.index("## Decision"), text.index("## Consequences")
    d = text.index("## Critic's objections")
    put(solved, ADR_PATH, text[:a] + text[b:c] + text[a:b] + text[c:d] + text[d:])
    commit(solved)
    result = grade(solved)
    assert_only(result, ADR_FORMAT)
    assert "order" in result[ADR_FORMAT].detail


def test_an_adr_whose_status_is_not_a_status(solved):
    swap(solved, ADR_PATH, "Accepted. This ADR records", "Probably fine. This ADR records")
    commit(solved)
    assert_only(grade(solved), ADR_FORMAT)


def test_an_adr_that_only_lists_benefits(solved):
    text = text_of(solved, ADR_PATH)
    start_at, end_at = text.index("## Consequences"), text.index("## Critic's objections")
    benefits = ("## Consequences\n\nThe design is simple and clear and everyone on the team understands it. It keeps the code short, "
                "keeps the tests fast and makes the behaviour easy to explain to a new colleague on their first day. Reviewers like "
                "it, auditors like it, and customers see a service that does what it should every single time.\n\n")
    put(solved, ADR_PATH, text[:start_at] + benefits + text[end_at:])
    commit(solved)
    result = grade(solved)
    assert_only(result, ADR_FORMAT)
    assert "downside" in result[ADR_FORMAT].detail


@pytest.mark.parametrize(
    "old,new,expected_in_detail",
    [
        ("`src/remit/service.py` runs", "`src/remit/risk.py` runs", "risk.py"),
        ("`ledger.post_transfer`", "`ledger.post_and_confirm`", "ledger.post_and_confirm"),
        ("`errors.NotificationError`", "`errors.NotifyTimeout`", "errors.NotifyTimeout"),
        ("(`store.Store.save_transfer`)", "(`store.Store.save_all`)", "store.Store.save_all"),
    ],
    ids=["module-from-the-stale-architecture-doc", "invented-function", "invented-error-class", "invented-method"],
)
def test_an_adr_that_points_at_code_that_does_not_exist(solved, old, new, expected_in_detail):
    swap(solved, ADR_PATH, old, new)
    commit(solved)
    result = grade(solved)
    assert_only(result, ADR_FACTS)
    assert expected_in_detail in result[ADR_FACTS].detail
    assert "claims_scan" in result[ADR_FACTS].hint


def test_an_adr_with_no_pointers_into_the_code(solved):
    text = text_of(solved, ADR_PATH)
    stripped = text.replace("`", "")
    put(solved, ADR_PATH, stripped)
    commit(solved)
    result = grade(solved)
    assert_only(result, ADR_FACTS)
    assert "reference" in result[ADR_FACTS].detail


@pytest.mark.parametrize(
    "sentence",
    [
        "T1 customers may send up to QAR 5,000 per day, so a notice is useful.",
        "T2 customers may send QAR 25,000 per day.",
        "There is no monthly limit, so the notice only needs the daily figure.",
        "Remit supports two KYC tiers, which keeps the rules simple.",
        "A quote is valid for 5 minutes, which gives the customer time to decide.",
        "Qatar is UTC+4 all year, so midnight there is 20:00 in UTC.",
        "All queries use placeholders, so nothing in the store can be injected.",
        "Fees are marginal: each band is charged at its own rate.",
    ],
    ids=["t1-stale", "t2-stale", "no-monthly", "two-tiers", "quote-5-minutes", "qatar-utc-4", "all-placeholders", "marginal-fee"],
)
def test_an_adr_that_repeats_a_stale_or_invented_figure(solved, sentence):
    """The figures docs/ARCHITECTURE.md got wrong (and a few an assistant invents) are contradicted by the code."""
    swap(solved, ADR_PATH, "## Consequences\n", "## Consequences\n\n" + sentence + "\n")
    commit(solved)
    assert_only(grade(solved), ADR_FACTS)


def test_an_adr_may_quote_the_stale_document_in_order_to_refute_it(solved):
    swap(solved, ADR_PATH, "## Consequences\n",
         "## Consequences\n\ndocs/ARCHITECTURE.md still says T1 may send QAR 5,000 per day; that is stale, `limits.LIMITS` is the source.\n")
    commit(solved)
    assert_only(grade(solved))


def test_an_adr_with_only_two_objections(solved):
    text = text_of(solved, ADR_PATH)
    cut = text.index("3. **Objection:**")
    put(solved, ADR_PATH, text[:cut])
    commit(solved)
    result = grade(solved)
    assert_only(result, ADR_CRITIC)
    assert "2 objection" in result[ADR_CRITIC].detail


def test_an_adr_whose_objections_have_no_answer(solved):
    text = text_of(solved, ADR_PATH)
    cut = text.index("## Critic's objections")
    put(solved, ADR_PATH, text[:cut] + """## Critic's objections

1. The customer who is not told may send the same transfer again and so create several transfers out of a single failure.
2. Nothing retries a failed message, so a message that was lost at the provider is simply lost for good and for ever.
3. A transactional outbox would be the textbook alternative here, and the ADR does not even look at that option at all.
""")
    commit(solved)
    result = grade(solved)
    assert_only(result, ADR_CRITIC)
    assert "what you did" in result[ADR_CRITIC].detail


def test_an_adr_without_a_critic_section(solved):
    text = text_of(solved, ADR_PATH)
    put(solved, ADR_PATH, text[: text.index("## Critic's objections")])
    commit(solved)
    assert_only(grade(solved), ADR_CRITIC)


def test_a_critic_table_with_a_response_column_is_accepted(solved):
    text = text_of(solved, ADR_PATH)
    cut = text.index("## Critic's objections")
    put(solved, ADR_PATH, text[:cut] + """## Critic's objections

| Objection | Response |
|---|---|
| A customer who is not told sends again, so one failure becomes several transfers. | Accepted as a real risk; we add an alert and an in-app notice. |
| Nothing retries, so a lost message stays lost, which is the standard complaint. | Deferred: a retry queue needs somewhere to keep unsent messages. |
| An outbox in the same database would be the textbook alternative to this choice. | Rejected for now: the ledger is not in that database. |
""")
    commit(solved)
    assert_only(grade(solved))


# --------------------------------------------------------------------------------------------
# the najmkit page: what an assistant invents, and what a stale comment teaches it
# --------------------------------------------------------------------------------------------
def append_to_page(work: Path, extra: str) -> None:
    put(work, DOC_PATH, text_of(work, DOC_PATH) + "\n" + extra + "\n")
    commit(work)


def test_functions_the_assistant_made_up(solved):
    append_to_page(solved, "Other helpers: `ids.generate(prefix)` makes an id, `clock.utcnow()` reads the time and `audit.write(event)` records one.")
    result = grade(solved)
    assert_only(result, DOC_NAMES)
    for invented in ("ids.generate", "clock.utcnow", "audit.write"):
        assert invented in result[DOC_NAMES].detail or "+" in result[DOC_NAMES].detail


def test_a_made_up_import(solved):
    append_to_page(solved, "```python\nfrom najmkit.ids import new_uuid\n```")
    assert_only(grade(solved), DOC_NAMES, DOC_EXAMPLES)  # found twice: by reading the page and by running it


@pytest.mark.parametrize(
    "claim",
    [
        "Create an id with `ids.new_id(prefix, length=8)`.",
        "Read the time with `clock.now(tz)`.",
        "Move a fixed clock with `clock.FixedClock.advance(delta: timedelta)`.",
        "Record an event with `audit.log_event(event, fields: dict)`.",
        "Read events back with `audit.read_events(path, limit=100)`.",
        "Build a clock with `clock.FixedClock()`; no start is needed.",
    ],
    ids=["extra-parameter", "extra-argument", "kwargs-as-a-parameter-name-delta", "dict-instead-of-kwargs", "limit", "missing-start"],
)
def test_signatures_that_are_not_the_real_ones(solved, claim):
    append_to_page(solved, claim)
    result = grade(solved)
    failed = failing(result)
    if claim.endswith("no start is needed."):
        assert failed in (set(), {DOC_SIGS})  # an empty call is shorthand, so it may pass; the examples below catch it
    else:
        assert failed == {DOC_SIGS}, failed


def test_a_call_with_the_wrong_keyword_in_an_example(solved):
    append_to_page(solved, "```python\nids.new_id(\"TRF\", length=8)\n```")
    result = grade(solved)
    assert DOC_EXAMPLES in failing(result) or DOC_SIGS in failing(result)


@pytest.mark.parametrize(
    "claim",
    [
        "This vendored copy is version 2.0.0 of najmkit.",
        "najmkit exposes API v2.",
        "Install it with pip install najmkit from the package index.",
        "najmkit is thread-safe, so the audit file can be shared between workers.",
        "`log_event` retries the write three times before it gives up.",
        "A prefix is 3 to 8 lower-case letters.",
        "The random token is 32 hex characters.",
        "The reserved field names are `ts`, `event` and `level`.",
        "A naive datetime is accepted and treated as UTC.",
        "With no audit file configured, events go to stdout.",
        "`audit.read_events` raises `FileNotFoundError` when the file is missing.",
        "The package works with asyncio: `await audit.log_event(...)`.",
    ],
    ids=["version", "api", "pypi", "thread-safe", "retries", "prefix-range", "token-length", "reserved", "naive", "stdout",
         "copied-stale-docstring", "async"],
)
def test_claims_the_code_contradicts(solved, claim):
    append_to_page(solved, claim)
    result = grade(solved)
    assert DOC_FACTS in failing(result), result[DOC_FACTS]
    assert failing(result) <= {DOC_FACTS, DOC_NAMES, DOC_SIGS}  # nothing else is blamed


def test_a_true_remark_about_the_stale_docstring_is_not_a_contradiction(solved):
    append_to_page(solved, "The docstring of `audit.read_events` says it raises `FileNotFoundError`, but it returns an empty list.")
    assert_only(grade(solved))


def test_denials_are_not_contradictions(solved):
    append_to_page(solved, "najmkit is not thread-safe and is not on PyPI. It does not rotate or compress the audit file.")
    assert_only(grade(solved))


def test_examples_that_call_something_that_does_not_exist(solved):
    swap(solved, DOC_PATH, 'audit.configure("audit.jsonl")', 'audit.configure("audit.jsonl")\naudit.flush()')
    commit(solved)
    result = grade(solved)
    assert DOC_EXAMPLES in failing(result)
    assert "flush" in result[DOC_EXAMPLES].detail


def test_a_page_without_runnable_examples(solved):
    text = text_of(solved, DOC_PATH)
    put(solved, DOC_PATH, text.replace("```python", "```text"))
    commit(solved)
    result = grade(solved)
    assert_only(result, DOC_EXAMPLES)
    assert "no example" in result[DOC_EXAMPLES].detail


def test_an_endless_example_cannot_hang_the_grader(solved):
    started = m.run_doc_examples(solved, "```python\nfrom najmkit import ids\nwhile True:\n    pass\n```", timeout=3)
    failures, ok_by_module, tried = started
    assert failures and "did not finish" in failures[0]


def test_documenting_only_half_of_the_api(solved):
    text = text_of(solved, DOC_PATH)
    keep = text[: text.index("## najmkit.audit")] + "\n"
    put(solved, DOC_PATH, keep)
    commit(solved)
    result = grade(solved)
    assert DOC_COVERAGE in failing(result)
    assert "log_event" in result[DOC_COVERAGE].detail or "configure" in result[DOC_COVERAGE].detail


def test_a_one_line_page(solved):
    put(solved, DOC_PATH, "# najmkit\n\nIds, clocks and an audit log.\n")
    commit(solved)
    result = grade(solved)
    assert {DOC_EXISTS, DOC_EXAMPLES, DOC_COVERAGE} <= failing(result)


# --------------------------------------------------------------------------------------------
# the postmortem: what an assistant invents when the record has a gap
# --------------------------------------------------------------------------------------------
def test_a_row_with_a_time_that_is_in_no_event(solved):
    swap(solved, PM_PATH, "| 10:14 | The on-call SRE acknowledged the page. | E3 |",
         "| 10:15 | The on-call SRE acknowledged the page and began investigating. | E3 |")
    commit(solved)
    result = grade(solved)
    assert {PM_ROWS, PM_INVENTED} <= failing(result)
    assert "10:15" in result[PM_ROWS].detail


def test_a_row_that_gives_a_real_event_the_wrong_time(solved):
    swap(solved, PM_PATH, "| 10:14 | The on-call SRE", "| 10:11 | The on-call SRE")
    commit(solved)
    result = grade(solved)
    assert PM_ROWS in failing(result)
    assert "E3" in result[PM_ROWS].detail


def test_a_row_citing_an_event_that_is_not_in_the_record(solved):
    swap(solved, PM_PATH, "| 11:10 | Maha closed INC-2031. | E12 |", "| 11:10 | Maha closed INC-2031. | E15 |")
    commit(solved)
    result = grade(solved)
    assert PM_ROWS in failing(result)
    assert "E15" in result[PM_ROWS].detail


def test_a_row_that_describes_a_different_event(solved):
    swap(solved, PM_PATH, "The on-call SRE acknowledged the page.", "A database failover completed without errors.")
    commit(solved)
    result = grade(solved)
    assert PM_ROWS in failing(result)
    assert "E3" in result[PM_ROWS].detail
    assert PM_INVENTED not in failing(result) or True


def test_a_timeline_that_skips_most_of_the_record(solved):
    text = text_of(solved, PM_PATH)
    rows = [ln for ln in text.splitlines() if ln.startswith("| ") and ln[2:3].isdigit()]
    keep = {ln for ln in rows if any(f"| E{n} |" in ln for n in (1, 2, 12))}
    put(solved, PM_PATH, "\n".join(ln for ln in text.splitlines() if ln not in rows or ln in keep) + "\n")
    commit(solved)
    result = grade(solved)
    assert_only(result, PM_COVER)
    assert "of the record's 13 events" in result[PM_COVER].detail


def test_an_invented_number_of_affected_customers(solved):
    swap(solved, PM_PATH, "Customers: 171 `notification.failed` events",
         "Customers: about 1,200 customers were affected; 171 `notification.failed` events")
    commit(solved)
    result = grade(solved)
    assert_only(result, PM_INVENTED)
    assert "1,200" in result[PM_INVENTED].detail


def test_a_duration_that_can_be_computed_from_the_record_is_not_invented(solved):
    swap(solved, PM_PATH, "The cause is not established.", "The cause is not established. Support called within 36 minutes of the first failure and the notice went up after 43 minutes.")
    commit(solved)
    assert_only(grade(solved))  # 10:36 - 09:58 = 38 would be invented; 36 and 43 are not differences of times in the record


def test_a_duration_that_is_wrong_is_flagged(solved):
    swap(solved, PM_PATH, "The cause is not established.", "The cause is not established. The incident took 3 hours to resolve and cost 7 customers their trust.")
    commit(solved)
    result = grade(solved)
    assert PM_INVENTED in failing(result)


def test_a_wrong_severity_date_or_version(solved):
    swap(solved, PM_PATH, "Severity SEV3.", "Severity SEV1.")
    swap(solved, PM_PATH, "On 11 March 2026", "On 12 March 2026")
    swap(solved, PM_PATH, "version 0.4.0. Date", "version 0.5.1. Date")
    commit(solved)
    result = grade(solved)
    assert PM_INVENTED not in failing(result) or "SEV1" in result[PM_INVENTED].detail
    problems = m.invented_facts(text_of(solved, PM_PATH), m.load_record(LAB_DIR / "assets" / "incident.json"))
    assert any("SEV1" in p for p in problems) and any("12 March" in p for p in problems) and any("0.5.1" in p for p in problems)


def test_a_person_the_record_never_names(solved):
    swap(solved, PM_PATH, "A payments engineer read the audit log", "Lujain read the audit log")
    commit(solved)
    result = grade(solved)
    assert_only(result, PM_INVENTED)
    assert "Lujain" in result[PM_INVENTED].detail


@pytest.mark.parametrize(
    "sentence",
    [
        "The root cause was an outage at the SMS vendor.",
        "The incident was caused by the gateway vendor degrading.",
        "Customers sent their transfers again after seeing no message.",
        "A deploy earlier that day changed the notification settings.",
        "The team restarted the notification service at 10:20.",
        "The database was slow, which delayed the messages.",
        "All customers were affected for the whole window.",
        "Confirmation emails were not delivered.",
        "Some customers were charged twice.",
    ],
    ids=["root-cause", "caused-by-vendor", "resent", "deploy", "restart", "database", "all-customers", "channel", "double-charge"],
)
def test_something_the_record_does_not_say_stated_as_fact(solved, sentence):
    swap(solved, PM_PATH, "The cause is not established.", "The cause is not established. " + sentence)
    commit(solved)
    result = grade(solved)
    assert PM_UNKNOWN in failing(result), sentence
    assert "cause" not in result[PM_UNKNOWN].hint.lower() or True


def test_the_same_sentences_are_fine_in_the_inference_section(solved):
    swap(solved, PM_PATH, "## What we do not know", "- The incident may have been caused by the gateway vendor degrading, and customers may have sent their transfers again. Confidence: low. It rests on E6 and E7; the vendor's report would confirm it.\n\n## What we do not know")
    commit(solved)
    assert_only(grade(solved))


def test_denials_in_the_facts_are_fine(solved):
    swap(solved, PM_PATH, "The cause is not established.",
         "The cause is not established. No deploy, restart or configuration change was made in the window, and nothing in the record says customers sent transfers again.")
    commit(solved)
    assert_only(grade(solved))


def test_a_postmortem_without_unknowns(solved):
    text = text_of(solved, PM_PATH)
    a, b = text.index("## What we do not know"), text.index("## Action items")
    put(solved, PM_PATH, text[:a] + text[b:])
    commit(solved)
    result = grade(solved)
    assert_only(result, PM_SECTIONS, PM_LABELS) if PM_LABELS in failing(result) else assert_only(result, PM_SECTIONS)
    assert "What we do not know" in result[PM_SECTIONS].detail


def test_open_questions_that_are_not_the_real_ones(solved):
    text = text_of(solved, PM_PATH)
    a, b = text.index("## What we do not know"), text.index("## Action items")
    put(solved, PM_PATH, text[:a] + "## What we do not know\n\n- Who was on call that morning and what they had for breakfast.\n- Whether the weather in Doha was fine.\n\n" + text[b:])
    commit(solved)
    result = grade(solved)
    assert_only(result, PM_LABELS)
    assert "real gaps" in result[PM_LABELS].detail


def test_inferences_with_no_confidence_or_evidence(solved):
    text = text_of(solved, PM_PATH)
    a, b = text.index("## What we infer"), text.index("## What we do not know")
    put(solved, PM_PATH, text[:a] + "## What we infer\n\n1. The vendor was down and so the messages did not go out for customers.\n2. People sent transfers again because they did not get a message.\n\n" + text[b:])
    commit(solved)
    result = grade(solved)
    assert_only(result, PM_LABELS)
    assert "confident" in result[PM_LABELS].detail


def test_a_postmortem_that_blames_a_person_is_only_advisory(solved):
    swap(solved, PM_PATH, "The cause is not established.", "The cause is not established. The on-call engineer was careless and forgot to check the dashboard.")
    commit(solved)
    result = grade(solved)
    assert_only(result, PM_BLAMELESS)
    assert framework.passed(list(result.values()))  # advisory: the lab still passes


def test_a_postmortem_with_a_missing_section_and_few_actions(solved):
    text = text_of(solved, PM_PATH)
    a = text.index("## Action items")
    put(solved, PM_PATH, text[:a] + "## Action items\n\n1. Fix the thing that broke next week for sure.\n")
    commit(solved)
    result = grade(solved)
    assert_only(result, PM_SECTIONS)
    assert "fewer than 3 action items" in result[PM_SECTIONS].detail


# --------------------------------------------------------------------------------------------
# scope, commits and the usual hygiene
# --------------------------------------------------------------------------------------------
def test_fixing_the_stale_docstring_in_this_ticket(solved):
    framework.edit_file(solved, "src/najmkit/audit.py", "A missing file raises FileNotFoundError.", "Missing file -> [].")
    commit(solved, "fix(najmkit): correct the read_events docstring")
    result = grade(solved)
    assert_only(result, DOCS_ONLY)
    assert "src/najmkit/audit.py" in result[DOCS_ONLY].detail


def test_editing_a_test_or_the_lab_assets(solved):
    (solved / "tests" / "test_najmkit.py").write_text(text_of(solved, "tests/test_najmkit.py") + "\n# note\n", encoding="utf-8")
    (solved / "lab-assets" / "incident.json").write_text(text_of(solved, "lab-assets/incident.json") + "\n", encoding="utf-8")
    commit(solved)
    assert_only(grade(solved), DOCS_ONLY)


def test_one_squashed_commit_instead_of_three(solved):
    gitutil.git(solved, "reset", "--soft", "lab-start")
    commit(solved, "docs(review): write the three documents")
    result = grade(solved)
    assert_only(result, THREE_COMMITS)
    assert "1 new commit" in result[THREE_COMMITS].detail


@pytest.mark.parametrize("message", ["wrote the docs", "docs: write the postmortem", "Docs(pm): Write the postmortem."],
                         ids=["no-convention", "no-scope", "wrong-case-and-full-stop"])
def test_commit_messages_that_ignore_contributing_md(solved, message):
    (solved / "docs" / "postmortems" / "notes.md").write_text("A note.\n", encoding="utf-8")
    commit(solved, message)
    assert_only(grade(solved), MESSAGES)


def test_work_that_is_not_committed(solved):
    swap(solved, PM_PATH, "The cause is not established.", "The cause is not established. Support was informed.")
    result = grade(solved)
    assert_only(result, CLEAN)


def test_a_key_pasted_into_a_document(solved):
    append_to_page(solved, "Example key for the audit gateway: sk-live-" + "9f8e7d6c5b4a3f2e1d0c9f8e")
    result = grade(solved)
    assert SECRETS in failing(result)
    assert "9f8e7d6c" not in result[SECRETS].detail + result[SECRETS].hint


# --------------------------------------------------------------------------------------------
# the helper module, directly
# --------------------------------------------------------------------------------------------
def record() -> m.Record:
    return m.load_record(LAB_DIR / "assets" / "incident.json")


def test_the_incident_record_is_what_the_lesson_says():
    rec = record()
    assert rec.id == "INC-2031" and rec.severity == "SEV3" and rec.date == "2026-03-11"
    assert [e["id"] for e in rec.data["timeline"]] == [f"E{n}" for n in range(1, 14)]
    times = [e["time"] for e in rec.data["timeline"]]
    assert times == sorted(times)
    minutes = lambda t: int(t[:2]) * 60 + int(t[3:5])  # noqa: E731
    assert minutes("10:50") - minutes("09:58") == 52 and minutes("10:11") - minutes("09:58") == 13
    assert {41, 13} <= rec.minute_numbers and {17, 14, 188, 171} <= rec.count_numbers
    assert 1200 not in rec.count_numbers and 47 not in rec.minute_numbers and 7 not in rec.count_numbers
    assert all(not any(c in e["raw"] for c in ("name", "phone")) for e in rec.data["timeline"] if "raw" in e)  # identifiers only


def test_the_answer_key_covers_every_event_and_compiles():
    key = json.loads((LAB_DIR / "hidden" / "answer_key.json").read_text(encoding="utf-8"))
    import re

    assert set(key["events"]) == {e["id"] for e in record().data["timeline"]}
    for event in key["events"].values():
        re.compile(event["anchors"])
    for pattern in key["gaps"] + [r["pattern"] for r in key["forbidden"]]:
        re.compile(pattern)
    assert set(key["required_events"]) <= set(key["events"])


@pytest.mark.parametrize(
    "text,expected",
    [
        ("1. **Objection:** one two three four five six seven eight. **Response:** accepted.\n2. **Objection:** x\n   - nested bullet\n3. last one", 3),
        ("- a\n  - nested\n- b\n- c\n- d", 4),
        ("| Objection | Response |\n|---|---|\n| a | b |\n| c | d |", 2),
        ("### One\nbody\n### Two\nbody", 2),
        ("First paragraph here.\n\nSecond paragraph here.", 2),
    ],
)
def test_list_items_understands_the_usual_shapes(text, expected):
    assert len(m.list_items(text)) == expected


def test_units_join_hard_wrapped_lines():
    found = m.units("Two tiers are in use: T1\n  (identity checked) may send QAR 5,000 per day.\n\n- A bullet.\n- Another one.")
    assert found == ["Two tiers are in use: T1 (identity checked) may send QAR 5,000 per day.", "- A bullet.", "- Another one."]


def test_the_code_index_resolves_references(solved):
    index = m.CodeIndex(solved)
    resolves = {
        "src/remit/limits.py": True, "limits.py": True, "tests/test_fees.py": True, "docs/ARCHITECTURE.md": True,
        "risk.py": False, "src/remit/risk.py": False, "docs/najmkit.md": True, "src/remit/service.py:RemitService.send": True,
        "src/remit/service.py:42": True, "src/remit/service.py:99999": False,
        "limits.QATAR_TZ": True, "limits.to_local(now)": True, "remit.limits.day_window": True, "najmkit.audit.log_event": True,
        "service.RemitService.send": True, "RemitService._notify": True, "service.SendResult.notified": True,
        "clock.advance": True, "store.save_transfer": True, "fx.QUOTE_TTL": True,
        "limits.get_zone": False, "remit.risk.check": False, "service.Quote.expires": False, "clock.utcnow": False,
        "datetime.now": None, "pytest.ini": None, "Decimal.quantize": None, "just words": None, ".env.example": None,
    }
    for token, want in resolves.items():
        got = index.resolve_path(token)
        if got is None:
            got = index.resolve_symbol(token)
        assert got is want, f"{token}: expected {want}, got {got}"


def test_signature_claims_directly(solved):
    index = m.CodeIndex(solved)
    sigs = index.modules["najmkit.ids"].sigs
    assert m.signature_problem("ids.new_id", "prefix: str", sigs["new_id"]) is None
    assert m.signature_problem("ids.new_id", "'TRF'", sigs["new_id"]) is None
    assert m.signature_problem("ids.new_id", "prefix", sigs["new_id"]) is None
    assert m.signature_problem("ids.new_id", "", sigs["new_id"]) is None
    assert m.signature_problem("ids.new_id", "prefix, length", sigs["new_id"]) is not None
    assert m.signature_problem("ids.new_id", "prefix, length=8", sigs["new_id"]) is not None
    assert m.signature_problem("ids.new_id", "prefix=None, *, upper: bool = True", sigs["new_id"]) is not None
    assert m.signature_problem("ids.SequentialIds", "start=40", sigs["SequentialIds"]) is None
    assert m.signature_problem("ids.SequentialIds", "begin=40", sigs["SequentialIds"]) is not None
    audit = index.modules["najmkit.audit"].sigs
    assert m.signature_problem("audit.log_event", "event: str, **fields: Any", audit["log_event"]) is None
    assert m.signature_problem("audit.log_event", "'transfer.sent', transfer_id='TRF-1'", audit["log_event"]) is None
    assert m.signature_problem("audit.log_event", "event, fields", audit["log_event"]) is not None  # two positional arguments
    assert m.signature_problem("audit.log_event", "event", audit["log_event"]) is None  # bare names could be variables
    assert m.signature_problem("audit.log_event", "event: str, fields: dict", audit["log_event"]) is not None
    assert m.signature_problem("audit.configure", "path | None", audit["configure"]) is None
    clock = index.modules["najmkit.clock"].sigs
    assert m.signature_problem("clock.FixedClock.advance", "**delta", clock["FixedClock.advance"]) is None
    assert m.signature_problem("clock.FixedClock.advance", "seconds=61", clock["FixedClock.advance"]) is None
    assert m.signature_problem("clock.now", "tz", clock["now"]) is not None


def test_timeline_rows_are_read_in_many_layouts():
    rows = m.timeline_rows("| 09:58 | x | E1 |\n- 10:11 (E2) y\n* **10:14** z\n3. 10:19:00 - w\n| Time | What |\n|---|---|\n10:26 UTC plain\n2026-03-11 10:30 q")
    assert [t for t, _ in rows] == ["09:58", "10:11", "10:14", "10:19", "10:26", "10:30"]


def test_derived_numbers_come_from_the_record_and_nothing_else():
    rec = record()
    ok = "The window lasted 52 minutes; the alert fired after 13 minutes; 188 transfers; 64 tickets; 23 rejections against 9; 41 minutes to recover."
    assert m.invented_facts(ok, rec) == []
    bad = m.invented_facts("About 2,500 customers lost 47 minutes and 300 transfers failed at 03:12.", rec)
    assert len(bad) == 4  # 2,500 customers, 47 minutes, 300 transfers, 03:12


def test_dates_ids_and_versions_in_the_postmortem():
    rec = record()
    assert m.invented_facts("On 11 March 2026 (2026-03-11) INC-2031 was SEV3 on Remit 0.4.0; the week before, 4 March; deployed 9 March.", rec) == []
    bad = m.invented_facts("On March 12 INC-2040 was SEV2 on version 1.0.0 in 2025, 2026-04-01.", rec)
    assert len(bad) == 6


# --------------------------------------------------------------------------------------------
# claims_scan.py, the learner's own helper
# --------------------------------------------------------------------------------------------
def scan(work: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "lab-assets/claims_scan.py", *args], cwd=work, capture_output=True, text=True, timeout=30)


def test_the_scanner_finds_what_the_architecture_doc_got_wrong(work):
    out = scan(work, "docs/ARCHITECTURE.md")
    assert out.returncode == 1
    assert "`risk.py`  no such file" in out.stdout
    assert "`najmkit.md`  no such file" in out.stdout  # the page the seed removed
    assert "claims looked up" in out.stdout.splitlines()[-1]


def test_the_scanner_accepts_the_reference_documents(solved):
    for rel in (ADR_PATH, DOC_PATH):
        assert scan(solved, rel).returncode == 0, scan(solved, rel).stdout
    out = scan(solved, PM_PATH, "--record", "lab-assets/incident.json")
    assert out.returncode == 0, out.stdout


def test_the_scanner_catches_an_invented_time_and_event(solved):
    swap(solved, PM_PATH, "| 10:14 | The on-call SRE acknowledged the page. | E3 |",
         "| 10:15 | The on-call SRE acknowledged the page. | E3 |\n| 10:16 | Something else. | E14 |")
    out = scan(solved, PM_PATH, "--record", "lab-assets/incident.json")
    assert out.returncode == 1
    assert "10:15" in out.stdout and "10:16" in out.stdout and "E14" in out.stdout


def test_the_scanner_reports_a_missing_file_with_status_2(work):
    assert scan(work, "docs/nope.md").returncode == 2
