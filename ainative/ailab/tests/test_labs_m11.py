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
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from ailab import checks_m11 as m
from ailab import framework, gitutil
from conftest import learner_commit, start

KIT = Path(__file__).resolve().parent.parent / "ailab"
LAB_DIR = KIT / "labs" / "m11_lifecycle"
SOLUTION = LAB_DIR / "solution"
BASE_DOCS = KIT / "base" / "remit" / "docs"
LESSON = KIT.parent.parent / "modules" / "11-lifecycle.md"

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
DOC_KNOWN = "Docs: the stale comment is reported under Known problems"
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
       DOC_KNOWN, PM_SECTIONS, PM_ROWS, PM_COVER, PM_INVENTED, PM_UNKNOWN, PM_LABELS, PM_BLAMELESS, DOCS_ONLY, THREE_COMMITS, MESSAGES,
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


COMPACT_ADR = """# 3. Qatar days are fixed UTC+3 windows

Status: Accepted

**Context:** `limits.to_local` converts an aware time with `limits.QATAR_TZ`, a fixed offset (`limits.QATAR_UTC_OFFSET`, three hours),
and `limits.day_window` and `limits.month_window` build the windows from it, in `src/remit/limits.py`. Qatar has no daylight
saving, so the offset never changes, and timestamps are stored in UTC, so every comparison converts first.

**Decision:** We use a fixed UTC+3 offset for Qatar instead of the time-zone database.

**Consequences:** The code needs no dependency and no data file, and 21:00 UTC is easy to test as midnight in Qatar. The cost
is that the offset is a belief about the world written into a constant: if Qatar ever changed it, the constant would have to
change, and old transfers could land on the wrong day.

## Critic's objections

1. **Objection:** A hard-coded offset is a time bomb. **Response:** rejected for now, because the offset has not changed.
2. **Objection:** Two conversions can disagree at midnight. **Response:** accepted: `limits.to_local` is the one place that converts.
3. **Objection:** Storing the Qatar date beside each transfer is the better design. **Response:** deferred: it needs a migration.
"""


def test_an_adr_written_with_labels_instead_of_headings_is_accepted(solved):
    (solved / ADR_PATH).unlink()
    put(solved, "docs/adr/0003-qatar-days-are-fixed-offset-windows.md", COMPACT_ADR)
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
    assert_only(grade(solved), DOC_KNOWN)  # the old page cannot know about the stale comment: advisory only


def test_the_original_najmkit_page_without_examples_is_not_enough(solved):
    put(solved, DOC_PATH, (BASE_DOCS / "najmkit.md").read_text(encoding="utf-8"))
    commit(solved)
    result = grade(solved)
    assert_only(result, DOC_EXAMPLES, DOC_KNOWN)
    assert "najmkit.clock" in result[DOC_EXAMPLES].detail and "najmkit.audit" in result[DOC_EXAMPLES].detail


DIRECT_IMPORT_EXAMPLES = {
    "from najmkit import ids\n\nids.use_generator(ids.SequentialIds())\nprint(ids.new_id(\"TRF\"))  # TRF-000001\nprint(ids.new_id(\"CUS\"))  # CUS-000002\nids.use_generator(None)   # random tokens again":
        "from najmkit.ids import new_id, SequentialIds, use_generator\n\nuse_generator(SequentialIds())\nprint(new_id(\"TRF\"))  # TRF-000001\nprint(new_id(\"CUS\"))  # CUS-000002\nuse_generator(None)   # random tokens again",
    "from najmkit import clock\n\nfixed = clock.FixedClock(\"2026-03-02T09:00:00+00:00\")\nclock.set_clock(fixed)\nfixed.advance(seconds=61)\nprint(clock.now())  # 2026-03-02 09:01:01+00:00\nclock.reset_clock()":
        "from najmkit.clock import FixedClock, set_clock, now, reset_clock\n\nfixed = FixedClock(\"2026-03-02T09:00:00+00:00\")\nset_clock(fixed)\nfixed.advance(seconds=61)\nprint(now())  # 2026-03-02 09:01:01+00:00\nreset_clock()",
    "from najmkit import audit\n\naudit.configure(\"audit.jsonl\")\nrecord = audit.log_event(\"transfer.sent\", transfer_id=\"TRF-1\")\nprint(audit.read_events())  # [{'event': 'transfer.sent', 'transfer_id': 'TRF-1', 'ts': '...'}]\naudit.configure(None)":
        "from najmkit.audit import configure, log_event, read_events\n\nconfigure(\"/tmp/ailab-m11-demo.jsonl\")\nrecord = log_event(\"transfer.sent\", transfer_id=\"TRF-1\")\nprint(read_events())\nconfigure(None)",
}


def test_examples_that_import_the_names_directly_are_accepted(solved):
    """`from najmkit.ids import new_id` is as good as `ids.new_id`: the page may be written either way."""
    page = text_of(solved, DOC_PATH)
    for old, new in DIRECT_IMPORT_EXAMPLES.items():
        assert old in page, old[:40]
        page = page.replace(old, new)
    put(solved, DOC_PATH, page)
    commit(solved)
    assert_only(grade(solved))


def test_a_word_in_a_string_is_not_an_example_for_a_module(solved):
    """An example only counts for a module when the code uses it, not when the text of a string mentions it."""
    put(solved, DOC_PATH, text_of(solved, DOC_PATH).replace("```python", "```text"))
    put(solved, DOC_PATH, text_of(solved, DOC_PATH) + '\n```python\nprint("ids. clock. audit.")\n```\n')
    commit(solved)
    assert DOC_EXAMPLES in failing(grade(solved))


def test_the_stale_comment_not_reported_is_advisory_only(solved):
    page = text_of(solved, DOC_PATH)
    put(solved, DOC_PATH, page[: page.index("## Known problems")].rstrip() + "\n")
    commit(solved)
    result = grade(solved)
    assert_only(result, DOC_KNOWN)
    assert framework.passed(framework.grade_lab(framework.load_lab("m11"), solved))  # advisory: the lab still passes
    assert "no 'Known problems' section" in result[DOC_KNOWN].detail


def test_a_known_problems_section_that_names_nothing_is_not_enough(solved):
    page = text_of(solved, DOC_PATH)
    put(solved, DOC_PATH, page[: page.index("## Known problems")] + "## Known problems\n\nThere may be some problems with the comments in this library, but we have not looked at them yet.\n")
    commit(solved)
    result = grade(solved)
    assert_only(result, DOC_KNOWN)
    assert "read_events" not in result[DOC_KNOWN].detail  # the answer is not given away


def test_a_cause_tucked_into_the_lines_under_the_title_is_still_a_cause(solved):
    swap(solved, PM_PATH, "Incident commander: Maha. All times are UTC.", "Incident commander: Maha. The vendor outage caused it. All times are UTC.")
    commit(solved)
    assert_only(grade(solved), PM_UNKNOWN)


def test_nobody_and_neither_are_denials_too(solved):
    swap(solved, PM_PATH, "No deploy or configuration change was made during the window.",
         "Nobody deployed anything or changed any configuration during the window.")
    commit(solved)
    assert_only(grade(solved))


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
        "Money rounds half-even to two places.",
    ],
    ids=["t1-stale", "t2-stale", "no-monthly", "two-tiers", "quote-5-minutes", "qatar-utc-4", "all-placeholders", "money-half-even"],
)
def test_an_adr_that_repeats_a_stale_or_invented_figure(solved, sentence):
    """The figures docs/ARCHITECTURE.md got wrong (and a few an assistant invents) are contradicted by the code."""
    swap(solved, ADR_PATH, "## Consequences\n", "## Consequences\n\n" + sentence + "\n")
    commit(solved)
    assert_only(grade(solved), ADR_FACTS)


@pytest.mark.parametrize(
    "sentence",
    [
        "A critic could argue for a quote that is valid for 5 minutes, which would cut abandoned quotes.",
        "Python's Decimal defaults to half-even rounding, so Money sets half up explicitly.",
        "Marginal fees, charged band by band, are the alternative; the express surcharge could be added before the cap.",
        "The strongest alternative is a time-zone database; if Qatar adopted daylight saving, it would be needed.",
        "The ledger rounds the partner share half-even, unlike every other amount.",
    ],
    ids=["alternative-quote", "decimal-default", "alternative-fee-design", "alternative-tz", "ledger-exception"],
)
def test_an_adr_may_discuss_alternatives_and_exceptions(solved, sentence):
    """A sentence about the road not taken, or about a true exception, is not a claim about the code."""
    swap(solved, ADR_PATH, "## Consequences\n", "## Consequences\n\n" + sentence + "\n")
    commit(solved)
    assert_only(grade(solved))


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
    ],
    ids=["extra-parameter", "extra-argument", "delta-as-a-parameter", "dict-instead-of-kwargs", "limit"],
)
def test_signatures_that_are_not_the_real_ones(solved, claim):
    append_to_page(solved, claim)
    assert_only(grade(solved), DOC_SIGS)


def test_an_empty_pair_of_parentheses_is_shorthand_but_an_example_must_run(solved):
    append_to_page(solved, "Build a clock with `clock.FixedClock()`.")
    assert_only(grade(solved))  # prose shorthand for "the class" is not a claim about its arguments
    swap(solved, DOC_PATH, 'fixed = clock.FixedClock("2026-03-02T09:00:00+00:00")', "fixed = clock.FixedClock()")
    commit(solved)
    result = grade(solved)
    assert_only(result, DOC_EXAMPLES)
    assert "FixedClock" in result[DOC_EXAMPLES].detail


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
        "By default, events are printed to stdout.",
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


def test_doctest_style_examples_are_run_too(solved):
    text = text_of(solved, DOC_PATH)
    start_at = text.index("```python")
    session = """```pycon
>>> from najmkit import ids, clock, audit
>>> ids.new_id("TRF")[:4]
'TRF-'
>>> clock.FixedClock("2026-03-02T09:00:00+00:00").now().year
2026
>>> audit.log_event("demo.happened")["event"]
'demo.happened'
```

"""
    put(solved, DOC_PATH, text[:start_at].replace("```python", "```text") + session + text[start_at:].replace("```python", "```text"))
    commit(solved)
    assert_only(grade(solved))
    broken = session.replace('ids.new_id("TRF")[:4]', "ids.generate('TRF')")
    put(solved, DOC_PATH, text[:start_at].replace("```python", "```text") + broken + text[start_at:].replace("```python", "```text"))
    commit(solved)
    assert DOC_EXAMPLES in failing(grade(solved))


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
    assert_only(result, PM_INVENTED, PM_UNKNOWN)  # a number the record lacks, and a customer count it never gives
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
    assert PM_INVENTED in failing(grade(solved))
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
        "171 customers did not get their message.",
    ],
    ids=["root-cause", "caused-by-vendor", "resent", "deploy", "restart", "database", "all-customers", "channel", "double-charge", "events-are-not-customers"],
)
def test_something_the_record_does_not_say_stated_as_fact(solved, sentence):
    swap(solved, PM_PATH, "The cause is not established.", "The cause is not established. " + sentence)
    commit(solved)
    result = grade(solved)
    assert PM_UNKNOWN in failing(result), sentence


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
    assert_only(result, PM_SECTIONS, PM_LABELS)
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
    assert "action item(s) of five words or more" in result[PM_SECTIONS].detail


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
    ok = ("The window lasted 52 minutes; the alert fired 13 minutes after the first failure (E1, E2); 188 transfers; 64 tickets; "
          "23 rejections against 9; 41 minutes from the alert to its resolution (E2, E10).")
    assert m.invented_facts(ok, rec) == []
    bad = m.invented_facts("About 2,500 customers lost 47 minutes and 300 transfers failed at 03:12.", rec)
    assert len(bad) == 4  # 2,500 customers, 47 minutes, 300 transfers, 03:12


def test_the_size_of_the_record_itself_is_a_fact():
    assert m.invented_facts("The record has 13 events and the timeline lists all 13 events.", record()) == []


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


# ============================================================================================
# Repairs after the learner dry-run. One group per finding; each wrong shortcut gets a negative test and
# each sound variant a positive one.
# ============================================================================================
# -- a method's `self` is part of the def line: it may stay or go -------------------------------------------
def test_method_signatures_copied_from_the_def_line_with_self_are_accepted(solved):
    append_to_page(solved, "\n".join([
        "Methods, copied from the def lines:",
        "- `ids.SequentialIds.__call__(self) -> str`",
        "- `clock.FixedClock.now(self) -> datetime`",
        "- `clock.FixedClock.set(self, moment: datetime | str) -> None`",
        "- `clock.FixedClock.advance(self, **delta: int) -> datetime`",
        "- `clock.FixedClock.set(moment: datetime | str) -> None` (the same, without self)",
    ]))
    assert_only(grade(solved))


def test_self_is_not_a_parameter_of_a_plain_function(solved):
    append_to_page(solved, "Wrong: `ids.new_id(self, prefix: str) -> str`.")
    assert_only(grade(solved), DOC_SIGS)


@pytest.mark.parametrize(
    "claim,fragment",
    [
        ("`clock.FixedClock.set(when: datetime | str) -> None`", "'when' is not a parameter"),
        ("`ids.SequentialIds(start: int = 0)`", "default of 'start'"),
        ("`clock.get_clock() -> str`", "return type"),
        ("`audit.log_event() -> dict`", "leaves out 'event'"),
        ("`audit.read_events(path: int | None = None) -> list[dict]`", "type of 'path'"),
        ("`audit.read_events(path: str | None) -> list[dict]`", "optional in the code"),
        ("`ids.new_id(prefix: str, length: int = 8) -> str`", "'length' is not a parameter"),
    ],
    ids=["renamed", "wrong-default", "wrong-return", "dropped", "wrong-type", "default-dropped", "extra-parameter"],
)
def test_a_signature_is_compared_with_the_def_line_not_only_bounded_by_it(solved, claim, fragment):
    append_to_page(solved, f"Wrong on purpose: {claim}.")
    result = grade(solved)
    assert_only(result, DOC_SIGS)
    assert fragment in result[DOC_SIGS].detail


def test_the_signature_hint_says_self_may_stay_and_points_at_the_def_line(solved):
    append_to_page(solved, "Wrong on purpose: `clock.get_clock() -> str`.")
    hint = grade(solved)[DOC_SIGS].hint
    assert "def line" in hint and "self" in hint


def test_a_renamed_catch_all_and_a_simplified_type_are_sound(solved):
    append_to_page(solved, "Fine: `audit.log_event(event: str, **kwargs) -> dict` and `audit.read_events(path: str | None = None) -> list`.")
    assert_only(grade(solved))


def test_a_call_with_keywords_is_not_read_as_a_declaration(solved):
    append_to_page(solved, "Calls: `ids.SequentialIds(start=40)` and `clock.FixedClock.advance(seconds=61)`.")
    assert_only(grade(solved))


def test_a_def_line_in_a_code_block_is_checked_like_an_inline_signature(solved):
    good = "```text\nclass FixedClock:\n    def set(self, moment: datetime | str) -> None\n    def advance(self, **delta: int) -> datetime\n```"
    bad = good.replace("moment: datetime | str", "when: datetime | str")
    append_to_page(solved, good)
    assert_only(grade(solved))
    append_to_page(solved, bad)
    result = grade(solved)
    assert_only(result, DOC_SIGS)
    assert "'when'" in result[DOC_SIGS].detail


def test_every_signature_offender_is_listed_not_just_the_first_two(solved):
    append_to_page(solved, "`ids.new_id(prefix, length=8)` `clock.now(tz)` `audit.read_events(path, limit=100)` "
                           "`ids.use_generator(a, b)` `clock.set_clock(a, b)` `audit.configure(a, b)`")
    detail = grade(solved)[DOC_SIGS].detail
    assert "more)" not in detail
    for name in ("new_id", "now", "read_events", "use_generator", "set_clock", "configure"):
        assert name in detail


def test_names_without_a_signature_do_not_document_the_api(solved):
    names_only = "# najmkit\n\n" + "\n".join(f"- `{n}`" for n in m.public_names(solved)) + "\n\n" + "word " * 200
    put(solved, DOC_PATH, names_only)
    commit(solved)
    result = grade(solved)
    assert DOC_COVERAGE in failing(result)
    assert "signature" in result[DOC_COVERAGE].detail


# -- names in backticks that are files, or are quoted in order to be refuted --------------------------------
def test_a_file_name_in_backticks_is_not_a_missing_name(solved):
    swap(solved, ADR_PATH, "## Consequences\n", "## Consequences\n\nThe trail is written to `audit.jsonl`, which `.gitignore` lists.\n")
    commit(solved)
    assert_only(grade(solved))
    index = m.CodeIndex(solved)
    assert index.resolve_symbol("audit.jsonl") is None
    assert index.resolve_symbol("audit.log_event") is True and index.resolve_symbol("audit.nope") is False


def test_a_wrong_name_may_be_quoted_when_the_sentence_says_it_does_not_exist(solved):
    swap(solved, ADR_PATH, "## Consequences\n", "## Consequences\n\nThe old page names `risk.py`, which does not exist.\n")
    commit(solved)
    assert_only(grade(solved))
    append_to_page(solved, "An assistant invented `ids.generate`, which does not exist, and `clock.utcnow()`, which is no such function.")
    assert_only(grade(solved))


def test_the_same_wrong_name_is_a_failure_when_the_sentence_relies_on_it(solved):
    swap(solved, ADR_PATH, "## Consequences\n", "## Consequences\n\nThe checks live in `risk.py`.\n")
    commit(solved)
    assert_only(grade(solved), ADR_FACTS)
    append_to_page(solved, "Use `ids.generate` to make an id.")
    assert DOC_NAMES in failing(grade(solved))


def test_the_scanner_treats_file_names_and_refuted_names_like_the_grader(solved):
    put(solved, "docs/scratch.md", "The trail is `audit.jsonl`. The old page names `risk.py`, which does not exist.\nThe checks live in `risk.py`.\n")
    out = scan(solved, "docs/scratch.md")
    assert "audit.jsonl" not in out.stdout
    assert out.stdout.count("risk.py") == 1 and "scratch.md:2" in out.stdout  # only the unrefuted one, on line 2


# -- layouts a sound page may use --------------------------------------------------------------------------------
def test_a_signature_in_a_table_cell_with_an_escaped_pipe_is_still_checked(solved):
    append_to_page(solved, "| Name | What it does |\n|---|---|\n| `clock.FixedClock.set(moment: datetime \\| str) -> None` | Jumps to a time. |")
    assert_only(grade(solved))
    append_to_page(solved, "| `clock.FixedClock.set(when: datetime \\| str) -> None` | Jumps to a time. |")
    result = grade(solved)
    assert_only(result, DOC_SIGS)
    assert "'when'" in result[DOC_SIGS].detail


def test_a_critic_section_written_as_a_label_line_works_like_a_heading(solved):
    text = text_of(solved, ADR_PATH)
    cut = text.index("## Critic's objections")
    objections = text[cut:].replace("## Critic's objections\n", "Critic's objections:\n")
    put(solved, ADR_PATH, text[:cut] + objections)
    commit(solved)
    assert_only(grade(solved))
    put(solved, ADR_PATH, text[:cut] + "Critic's objections:\n\n1. Retries? Deferred.\n")
    commit(solved)
    assert_only(grade(solved), ADR_CRITIC)


# -- floors the ticket now states ------------------------------------------------------------------------------
def test_the_floors_are_the_ones_the_ticket_states():
    assert m.ADR_MINIMUM_WORDS == {"context": 25, "decision": 8, "consequences": 20} and m.OBJECTION_WORDS == 8
    task = (LAB_DIR / "task.md").read_text(encoding="utf-8")
    assert "Context needs 25 words or more, Decision 8, Consequences 20" in task
    assert "each of eight words or more" in task
    assert "Cover nine of the thirteen events or more" in task and "Three or more action items" in task
    assert m.PAGE_MIN_PROSE == 40 and "40 words of prose or more" in task


def test_a_thin_context_is_named_with_its_floor(solved):
    text = text_of(solved, ADR_PATH)
    a, b = text.index("## Context"), text.index("## Decision")
    put(solved, ADR_PATH, text[:a] + "## Context\n\nIt runs `src/remit/service.py` and `ledger.post_transfer`.\n\n" + text[b:])
    commit(solved)
    result = grade(solved)
    assert_only(result, ADR_FORMAT)
    assert "at least 25 words" in result[ADR_FORMAT].detail


def test_the_lessons_own_sample_adr_passes_the_format_check():
    if not LESSON.exists():
        pytest.skip("the lesson is not in this checkout")
    lesson = LESSON.read_text(encoding="utf-8")
    block = re.search(r"```markdown\n(# 4\. Fee tiers are chosen by the whole amount\n.*?)```", lesson, re.S)
    assert block, "the sample ADR of lesson 11.1 moved"
    compact = block.group(1)
    assert m.adr_format_problems(compact) == []
    headed = re.sub(r"^(Status|Context|Decision|Consequences): ", lambda g: f"## {g.group(1)}\n\n", compact, flags=re.M)
    assert headed != compact
    assert m.adr_format_problems(headed) == [], headed  # pasted in the template's shape


# -- the critic's objections: what you did must be a decision -------------------------------------------------------
def test_responses_that_decide_nothing_do_not_count(solved):
    text = text_of(solved, ADR_PATH)
    put(solved, ADR_PATH, text[: text.index("## Critic's objections")] + """## Critic's objections

1. **Objection:** A customer who is not told sends again, so one failure becomes several transfers. **Response:** noted.
2. **Objection:** Nothing retries, so a lost message stays lost, which is the standard complaint. **Response:** noted for the record.
3. **Objection:** An outbox in the same database would be the textbook alternative to this choice. **Response:** see above.
""")
    commit(solved)
    result = grade(solved)
    assert_only(result, ADR_CRITIC)
    assert "what you did" in result[ADR_CRITIC].detail


def test_a_table_cell_that_only_says_noted_does_not_count(solved):
    text = text_of(solved, ADR_PATH)
    cut = text.index("## Critic's objections")
    put(solved, ADR_PATH, text[:cut] + """## Critic's objections

| Objection | Response |
|---|---|
| A customer who is not told sends again, so one failure becomes several transfers. | noted |
| Nothing retries, so a lost message stays lost, which is the standard complaint. | noted for now |
| An outbox in the same database would be the textbook alternative to this choice. | see above |
""")
    commit(solved)
    assert_only(grade(solved), ADR_CRITIC)


def test_one_clause_objections_get_an_honest_message(solved):
    text = text_of(solved, ADR_PATH)
    cut = text.index("## Critic's objections")
    put(solved, ADR_PATH, text[:cut] + "## Critic's objections\n\n1. Retries? Deferred.\n2. Outbox? Rejected.\n3. Alerts? Accepted.\n")
    commit(solved)
    result = grade(solved)
    assert_only(result, ADR_CRITIC)
    assert "too short to count" in result[ADR_CRITIC].detail and "3 more" in result[ADR_CRITIC].detail


@pytest.mark.parametrize("word", ["accepted", "rejected because the ledger is elsewhere", "deferred to a follow-up ticket", "we keep the decision", "declined"])
def test_any_clear_decision_word_is_enough_when_the_objection_is_a_sentence(solved, word):
    text = text_of(solved, ADR_PATH)
    cut = text.index("## Critic's objections")
    body = "\n".join(f"{n}. A customer who is not told sends again, so one failure becomes several transfers (#{n}). **Response:** {word}." for n in (1, 2, 3))
    put(solved, ADR_PATH, text[:cut] + "## Critic's objections\n\n" + body + "\n")
    commit(solved)
    assert_only(grade(solved))


# -- 'posted twice' is not a customer sending again ---------------------------------------------------------------------
def test_a_true_sentence_about_two_vendor_posts_is_accepted(solved):
    swap(solved, PM_PATH, "The cause is not established.",
         "The cause is not established. The vendor's public status page posted twice: an investigation notice at 10:30 (E6) and a resolution notice at 11:02 (E11).")
    commit(solved)
    assert_only(grade(solved))


@pytest.mark.parametrize(
    "sentence",
    [
        "Customers sent the transfer twice.",
        "There were duplicate transfers in the window.",
        "Many callers tried twice before they gave up.",
        "The same payment was sent two times.",
    ],
    ids=["customers-twice", "duplicate-transfers", "callers-twice", "payment-two-times"],
)
def test_a_resend_without_evidence_is_still_rejected(solved, sentence):
    swap(solved, PM_PATH, "The cause is not established.", "The cause is not established. " + sentence)
    commit(solved)
    assert PM_UNKNOWN in failing(grade(solved))


def test_a_message_quotes_the_words_that_caused_it(solved):
    swap(solved, PM_PATH, "The cause is not established.", "The cause is not established. " + "Filler words that run on for quite a while before the point. " * 3
         + "Then the failures originated in the vendor's gateway, as everyone knows.")
    commit(solved)
    detail = grade(solved)[PM_UNKNOWN].detail
    assert "originated in the vendor" in detail  # not just the start of the sentence


# -- causes, actions and states the record does not give --------------------------------------------------------------------
@pytest.mark.parametrize(
    "sentence",
    [
        "The failures originated in the vendor's gateway.",
        "Confirmations were late because the notification gateway was slow.",
        "The gateway was down.",
        "The team paused outbound messages and re-queued them (E8).",
        "Support worked around it by phoning customers.",
    ],
    ids=["originated", "because-slow", "gateway-down", "paused-and-requeued", "workaround"],
)
def test_causes_and_actions_without_the_usual_words_are_still_not_facts(solved, sentence):
    swap(solved, PM_PATH, "The cause is not established.", "The cause is not established. " + sentence)
    commit(solved)
    assert PM_UNKNOWN in failing(grade(solved)), sentence


def test_the_vendors_own_statement_may_be_reported(solved):
    swap(solved, PM_PATH, "The cause is not established.",
         "The cause is not established. The vendor's status page reported that delivery was degraded (E6) and later that it was back to normal (E11).")
    commit(solved)
    assert_only(grade(solved))


@pytest.mark.parametrize(
    "sentence",
    [
        "Every notification.failed event in the window had reason notification_error.",
        "All failures had the reason notification_error throughout.",
    ],
    ids=["every-event", "all-failures"],
)
def test_what_one_engineer_read_at_one_time_is_not_a_fact_about_the_whole_window(solved, sentence):
    swap(solved, PM_PATH, "The cause is not established.", "The cause is not established. " + sentence)
    commit(solved)
    result = grade(solved)
    assert PM_UNKNOWN in failing(result)
    assert "who found it and when" in result[PM_UNKNOWN].detail


def test_the_same_finding_with_its_source_is_accepted(solved):
    swap(solved, PM_PATH, "The cause is not established.",
         "The cause is not established. At 10:26 a payments engineer found every notification.failed event with reason notification_error (E5).")
    commit(solved)
    assert_only(grade(solved))


# -- numbers: percentages, gaps in minutes, a count that belongs to another measure ------------------------------------------
@pytest.mark.parametrize(
    "sentence,fragment",
    [
        ("About 91% of sent transfers had no confirmation.", "percentage 91%"),
        ("The window began 17 minutes after the first failure.", "17 minutes"),
        ("The window began 17 minutes after the first failure (E1).", "17 minutes"),
        ("176 transfers were sent in the window.", "176 is not the record's figure"),
        ("188 notification failures were recorded.", "188 is not the record's figure"),
        ("About five hundred customers were affected.", "500 customers"),
        ("About two thousand customers were affected.", "2000 customers"),
    ],
    ids=["percent", "coincident-gap", "gap-with-the-wrong-anchor", "last-weeks-count", "count-of-another-measure",
         "five-hundred-in-words", "two-thousand-in-words"],
)
def test_derived_and_mis_assigned_numbers_are_rejected(solved, sentence, fragment):
    swap(solved, PM_PATH, "The cause is not established.", "The cause is not established. " + sentence)
    commit(solved)
    result = grade(solved)
    assert PM_INVENTED in failing(result), sentence
    assert fragment in result[PM_INVENTED].detail, result[PM_INVENTED].detail


@pytest.mark.parametrize(
    "sentence",
    [
        "The alert fired 13 minutes after the first failure (E1, E2).",
        "The alert fired thirteen minutes after the first failure (E1, E2).",
        "176 transfers were sent in the same window one week earlier (4 March).",
        "The failure rate was above 20% when the alert fired (E2).",
    ],
    ids=["gap-with-its-events", "gap-in-words", "last-weeks-count-said-so", "a-percentage-the-record-writes"],
)
def test_worked_out_numbers_that_cite_their_source_are_accepted(solved, sentence):
    swap(solved, PM_PATH, "The cause is not established.", "The cause is not established. " + sentence)
    commit(solved)
    assert_only(grade(solved))


def test_a_gap_in_minutes_must_cite_the_events_it_spans():
    rec = m.load_record(LAB_DIR / "assets" / "incident.json")
    key = json.loads((LAB_DIR / "hidden" / "answer_key.json").read_text(encoding="utf-8"))
    assert m.invented_facts("The alert fired 13 minutes after the first failure.", rec)  # no event cited
    assert m.invented_facts("The alert fired 13 minutes after the first failure (E1, E2).", rec) == []
    assert m.invented_facts("The alert fired 13 minutes after the first failure (09:58 and 10:11).", rec) == []
    assert m.invented_facts("It took 17 minutes (E1).", rec)  # E1 + 17 minutes is no event
    assert m.invented_facts("The incident was open 52 minutes.", rec) == []  # the record's own title says so
    assert m.misassigned_counts("188 transfers were sent, 171 notification.failed events, 64 tickets, 23 limit_exceeded rejections.", rec, key) == []
    assert m.misassigned_counts("64 transfers were sent.", rec, key)
    assert m.misassigned_counts("12 support tickets.", rec, key)


# -- people the record never names ----------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "sentence",
    [
        "Hassan, the on-call SRE, acknowledged the page (E3).",
        "The on-call SRE, Hassan, acknowledged the page (E3).",
        "The alert paged Hassan (E2).",
        "The alert fired and Hassan acknowledged it (E3).",
        "A payments engineer, Fatima, read the audit log (E5).",
    ],
    ids=["name-comma-role", "role-comma-name", "paged-name", "name-verb", "engineer-comma-name"],
)
def test_a_person_introduced_by_name_is_an_invented_person(solved, sentence):
    swap(solved, PM_PATH, "The cause is not established.", "The cause is not established. " + sentence)
    commit(solved)
    result = grade(solved)
    assert PM_INVENTED in failing(result), sentence
    assert "is not named in the record" in result[PM_INVENTED].detail


def test_people_the_record_names_and_capitalised_places_are_fine(solved):
    swap(solved, PM_PATH, "The cause is not established.",
         "The cause is not established. Maha, the incident commander, closed it (E12); support in Qatar was told by the customer support lead (E7), "
         "and Payments Platform was paged on Wednesday.")
    commit(solved)
    assert_only(grade(solved))


# -- action items ------------------------------------------------------------------------------------------------------------
def test_action_items_without_an_owner_or_a_way_to_see_they_are_done_do_not_count(solved):
    text = text_of(solved, PM_PATH)
    a = text.index("## Action items")
    put(solved, PM_PATH, text[:a] + "## Action items\n\n1. Alert earlier than ten minutes next time.\n2. Add the in-app notice to the runbook for good.\n"
        "3. Think about how failed messages could be retried someday.\n")
    commit(solved)
    result = grade(solved)
    assert_only(result, PM_SECTIONS)
    assert "owner" in result[PM_SECTIONS].detail and "done" in result[PM_SECTIONS].detail


def test_action_items_with_an_owner_and_a_check_in_other_words_count(solved):
    text = text_of(solved, PM_PATH)
    a = text.index("## Action items")
    put(solved, PM_PATH, text[:a] + """## Action items

- Alert on the failure rate over a shorter window. Salem (platform engineering) is responsible; we will know it works when a replay of INC-2031 fires it early.
- Show the in-app notice automatically. The payments team owns it; verified by a test alert that turns the notice on.
- Decide how failed confirmations are retried. Hessa to propose; the ADR is merged when the decision is made.
""")
    commit(solved)
    assert_only(grade(solved))


# -- blame ---------------------------------------------------------------------------------------------------------------
def test_blaming_wording_without_the_usual_words_is_flagged_but_advisory(solved):
    swap(solved, PM_PATH, "The cause is not established.",
         "The cause is not established. The on-call SRE was slow to respond and should have acknowledged the page sooner.")
    commit(solved)
    result = grade(solved)
    assert_only(result, PM_BLAMELESS)
    assert framework.passed(list(result.values()))


# -- wrong statements about the code that a plain number or a plain verb gives away ------------------------------------------
@pytest.mark.parametrize(
    "claim",
    [
        "The `ids.new_id` tokens are 8 characters long.",
        "Tokens from `ids.new_id` are eight characters.",
        "`audit.log_event` takes a lock while it appends.",
        "`audit.log_event` writes each record atomically.",
    ],
    ids=["token-8", "token-eight", "lock", "atomic"],
)
def test_wrong_plain_statements_about_the_code_are_caught(solved, claim):
    append_to_page(solved, claim)
    assert DOC_FACTS in failing(grade(solved))


def test_true_statements_about_token_length_pass(solved):
    append_to_page(solved, "A random token is 12 hex characters; a sequential token is six digits, like 000001. `audit.log_event` takes no lock.")
    assert_only(grade(solved))


UNANTICIPATED = "`audit.read_events` returns the newest event first"


def test_a_false_sentence_with_no_rule_still_passes_and_the_lesson_says_so(solved):
    """The sieve's honest limit: lesson 11.2 names this sentence as one the grader cannot catch. If a rule ever catches it,
    the lesson (and its quiz question 5) must change to another example."""
    append_to_page(solved, UNANTICIPATED + ".")
    assert_only(grade(solved))
    if LESSON.exists():
        assert UNANTICIPATED in LESSON.read_text(encoding="utf-8")


def test_a_retry_nobody_wrote_in_the_notification_decision_is_caught(solved):
    swap(solved, ADR_PATH, "## Consequences\n", "## Consequences\n\nThe `service.RemitService._notify` method retries three times with exponential backoff.\n")
    commit(solved)
    assert_only(grade(solved), ADR_FACTS)


def test_discussing_retries_as_the_alternative_is_fine(solved):
    swap(solved, ADR_PATH, "## Consequences\n",
         "## Consequences\n\nA retry queue would be the alternative to `service.RemitService._notify` carrying on; nothing retries today.\n")
    commit(solved)
    assert_only(grade(solved))


@pytest.mark.parametrize(
    "sentence,ok",
    [
        ("A quote lasts five minutes (`fx.QUOTE_TTL`), which gives the customer time.", False),
        ("A quote lasts 300 seconds (`fx.QUOTE_TTL`).", False),
        ("A quote lasts one minute (`fx.QUOTE_TTL`).", True),
        ("A quote lasts sixty seconds (`fx.QUOTE_TTL`).", True),
        ("T1 customers may send up to QAR five thousand per day.", False),
    ],
    ids=["five-minutes", "300-seconds", "one-minute", "sixty-seconds", "five-thousand"],
)
def test_figures_written_in_words_are_compared_like_digits(solved, sentence, ok):
    swap(solved, ADR_PATH, "## Consequences\n", "## Consequences\n\n" + sentence + "\n")
    commit(solved)
    if ok:
        assert_only(grade(solved))
    else:
        assert_only(grade(solved), ADR_FACTS)


def test_words_to_numbers():
    assert m.words_to_numbers("five minutes, sixty seconds and twenty-five hundred customers") == "5 minutes, 60 seconds and 2500 customers"
    assert m.words_to_numbers("about two thousand, a hundred, a minute") == "about 2000, 100, 1 minute"
    assert m.words_to_numbers("no one, a transfer, one of two") == "no 1, a transfer, 1 of 2"
    assert m.words_to_numbers("two thousand and five", minimum=4) == "2000 and 5"
    assert m.words_to_numbers("thirteen minutes, two events", minimum=4) == "13 minutes, two events"


def test_the_helpers_for_signatures_and_messages():
    assert m.read_annotation(" -> dict[str, Any] | None: ...") == "dict[str, Any] | None"
    assert m.read_annotation(" -> str and returns the id") == "str"
    assert m.read_annotation(" not an arrow") is None
    assert m.annotation_tokens("Optional[str]") == m.annotation_tokens("str | None") == frozenset({"str", "None"})
    assert m.annotation_tokens("os.PathLike[str] | str") == frozenset({"PathLike", "str"})
    assert m.annotation_tokens("datetime") <= m.annotation_tokens("datetime | str")
    text = "x" * 60 + " the failures originated in the vendor " + "y" * 60
    start = text.index("originated")
    shown = m.around(text, start, start + len("originated in the vendor"))
    assert "originated in the vendor" in shown and shown.startswith("...") and shown.endswith("...") and len(shown) < 120


# -- one commit per document -------------------------------------------------------------------------------------------------
def test_one_commit_with_all_three_documents_and_two_empty_commits_is_not_three_commits(solved):
    gitutil.git(solved, "reset", "--soft", "lab-start")
    commit(solved, "docs(review): write the three documents")
    gitutil.git(solved, "commit", "--allow-empty", "-m", "docs(review): tidy the first document")
    gitutil.git(solved, "commit", "--allow-empty", "-m", "docs(review): tidy the second document")
    result = grade(solved)
    assert_only(result, THREE_COMMITS)
    assert "3 new commits" in result[THREE_COMMITS].detail and "first committed together" in result[THREE_COMMITS].detail


def test_one_commit_with_all_three_documents_and_two_whitespace_commits(solved):
    gitutil.git(solved, "reset", "--soft", "lab-start")
    commit(solved, "docs(review): write the three documents")
    for n in range(2):
        (solved / DOC_PATH).write_text(text_of(solved, DOC_PATH) + "\n", encoding="utf-8")
        commit(solved, f"docs(najmkit): tidy {n}")
    assert_only(grade(solved), THREE_COMMITS)


def test_two_documents_in_one_commit_are_named(solved):
    gitutil.git(solved, "reset", "--soft", "lab-start")
    gitutil.git(solved, "reset", "-q")
    gitutil.git(solved, "add", ADR_PATH, DOC_PATH)
    gitutil.git(solved, "commit", "-q", "-m", "docs(review): the adr and the page")
    gitutil.git(solved, "add", PM_PATH)
    gitutil.git(solved, "commit", "-q", "-m", "docs(postmortem): the review")
    result = grade(solved)
    assert_only(result, THREE_COMMITS)
    assert "the ADR and the najmkit page were first committed together" in result[THREE_COMMITS].detail


def test_three_commits_in_any_order_plus_later_fixes_are_fine(solved):
    gitutil.git(solved, "reset", "--soft", "lab-start")
    gitutil.git(solved, "reset", "-q")
    for rel, message in ((PM_PATH, "docs(postmortem): write the review"), (ADR_PATH, "docs(adr): record the decision"),
                         (DOC_PATH, "docs(najmkit): restore the page")):
        gitutil.git(solved, "add", rel)
        gitutil.git(solved, "commit", "-q", "-m", message)
    (solved / ADR_PATH).write_text(text_of(solved, ADR_PATH) + "\nA closing remark.\n", encoding="utf-8")
    commit(solved, "docs(adr): add a closing remark")
    assert_only(grade(solved))


def test_a_document_that_is_not_committed_is_named(solved):
    gitutil.git(solved, "reset", "--soft", "HEAD~1")
    gitutil.git(solved, "reset", "-q")
    result = grade(solved)
    assert THREE_COMMITS in failing(result)
    assert "the postmortem is not committed yet" in result[THREE_COMMITS].detail


# -- secrets in prose ---------------------------------------------------------------------------------------------------------
def test_a_password_written_without_quotes_is_a_secret(solved):
    append_to_page(solved, "The demo login is password=hunter2hunter2 for the audit viewer.")
    result = grade(solved)
    assert SECRETS in failing(result)
    assert "hunter2" not in result[SECRETS].detail + result[SECRETS].hint


def test_prose_about_passwords_and_example_keys_is_fine(solved):
    append_to_page(solved, "Never commit a password: use the vault. The AWS documentation example key is AKIAIOSFODNN7EXAMPLE. Set password=changeme-in-vault.")
    assert_only(grade(solved))


# -- the lesson and the ticket agree -----------------------------------------------------------------------------------------
def test_the_ticket_in_the_lesson_is_the_ticket_in_the_kit():
    if not LESSON.exists():
        pytest.skip("the lesson is not in this checkout")
    lesson = LESSON.read_text(encoding="utf-8")
    block = re.search(r"\*\*The ticket\.\*\*[^\n]*\n\n```text\n(.*?)```", lesson, re.S)
    assert block, "the ticket block of lesson 11.2 moved"
    assert block.group(1).strip() == (LAB_DIR / "task.md").read_text(encoding="utf-8").strip()


def test_the_starter_grade_block_in_the_lesson_is_what_the_grader_prints(work):
    if not LESSON.exists():
        pytest.skip("the lesson is not in this checkout")
    lesson = LESSON.read_text(encoding="utf-8")
    block = re.search(r"On the untouched starter[^\n]*\n\n```text\n(.*?)```", lesson, re.S)
    assert block, "the starter grade block of lesson 11.2 moved"
    run = subprocess.run([sys.executable, "-m", "ailab", "grade", "m11", "--dir", str(work)], cwd=KIT.parent, capture_output=True, text=True,
                         timeout=120)
    printed = run.stdout.splitlines()
    assert printed, run.stderr
    for line in block.group(1).splitlines():
        if line.strip() in ("", "..."):
            continue
        assert line in printed, line


def test_the_first_draft_lines_in_the_lesson_are_what_the_grader_prints_for_that_draft(solved):
    """The lesson shows three failing lines for a constructed first draft; rebuild the draft and compare."""
    if not LESSON.exists():
        pytest.skip("the lesson is not in this checkout")
    block = re.search(r"three of the failing lines look like this[^\n]*\n\n```text\n(.*?)```", LESSON.read_text(encoding="utf-8"), re.S)
    assert block, "the first-draft block of lesson 11.2 moved"
    append_to_page(solved, "Also: `ids.generate(prefix, length=8)` makes an id, `clock.utcnow()` reads the time and `audit.write(event, fields)` "
                           "records an event.\nnajmkit is thread-safe and installs with pip install najmkit.")
    text = text_of(solved, PM_PATH)
    a, b = text.index("## Summary"), text.index("## Impact")
    text = text[:a] + ("## Summary\n\nOn 11 March 2026 an outage at our SMS gateway vendor, caused by a configuration change on their side,\n"
                       "stopped confirmation messages for roughly 2,000 customers for 52 minutes. The on-call engineer restored\n"
                       "service by failing over to the backup provider at 10:40.\n\n") + text[b:]
    text = text.replace("| 10:14 | The on-call SRE acknowledged the page. | E3 |",
                        "| 10:15 | The on-call SRE acknowledged the page and began investigating. | E3 |")
    text = text.replace("| 10:50 | Last `notification.failed` event of the window. | E9 |",
                        "| 10:40 | The on-call engineer failed over to the backup provider. | E9 |")
    put(solved, PM_PATH, text)
    commit(solved)
    result = grade(solved)
    shown = [ln for ln in block.group(1).splitlines() if ln.strip()]
    assert len(shown) == 3
    for line in shown:
        name = next(n for n in result if line.startswith(f"[FAIL] {n}: "))
        assert line == f"[FAIL] {name}: {result[name].detail}", line
    # and the Summary of the lesson's draft is the one used here
    assert "caused by a configuration change on their side" in LESSON.read_text(encoding="utf-8")


# -- a bare `name()` where the signature belongs ------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "line",
    [
        "| `ids.new_id()` | Makes an id. |",
        "### `audit.log_event()`",
        "- `clock.FixedClock()` is a clock you move yourself.",
        "1. `ids.use_generator()` installs a token source.",
    ],
    ids=["table-row", "heading", "list-item", "numbered-item"],
)
def test_a_signature_that_leaves_out_required_parameters_is_named(solved, line):
    append_to_page(solved, line)
    result = grade(solved)
    assert_only(result, DOC_SIGS)
    assert "leaves out" in result[DOC_SIGS].detail


@pytest.mark.parametrize(
    "line",
    [
        "| `ids.new_id()` | see `new_id(prefix)` |",
        "- `clock.now()` returns the current time.",
        "- `audit.current_path()` returns the audit file or None.",
        "Build a clock with `clock.FixedClock()` and call `ids.new_id()` in prose.",
    ],
    ids=["same-row-has-the-parameters", "no-required-parameter", "no-required-parameter-2", "prose-shorthand"],
)
def test_empty_parentheses_are_fine_when_nothing_is_required_or_it_is_prose(solved, line):
    append_to_page(solved, line)
    assert_only(grade(solved))


def test_a_terse_page_with_short_descriptions_is_accepted(solved):
    page = text_of(solved, DOC_PATH)
    rows = re.findall(r"^\|\s*(`[^`]+`)\s*\|\s*(`[^`]+`)\s*\|\s*([^|]+?)\s*\|$", page, re.M)
    terse = "# najmkit\n\n" + "\n".join(f"| {n} | {sig} | {' '.join(desc.split()[:3])} |" for n, sig, desc in rows) + "\n"
    terse += "".join(f"\n```python\n{re.sub(r'  +#.*$', '', block, flags=re.M)}\n```\n" for lang, block in m.code_blocks(page) if lang == "python")
    terse += "\n## Known problems\n\nThe docstring of `audit.read_events` says a missing file raises an error; running it returns an empty list.\n"
    assert m.prose_word_count(terse) < 80 and len(terse.split()) < 260  # short on purpose
    put(solved, DOC_PATH, terse)
    commit(solved)
    assert_only(grade(solved))


def test_a_page_that_only_lists_signatures_does_not_say_what_anything_does(solved):
    page = text_of(solved, DOC_PATH)
    signatures = ", ".join(f"`{sig}`" for sig in re.findall(r"^\|\s*`[^`]+`\s*\|\s*`([^`]+)`\s*\|", page, re.M))
    examples = "".join(f"\n```python\n{block}\n```\n" for lang, block in m.code_blocks(page) if lang == "python")
    put(solved, DOC_PATH, "# najmkit\n\n" + signatures + "\n" + examples + "\n## Known problems\n\nThe docstring of `audit.read_events` says a missing file raises an error; it returns an empty list.\n")
    commit(solved)
    result = grade(solved)
    assert DOC_EXISTS in failing(result)
    assert "almost nothing about what they do" in result[DOC_EXISTS].detail
