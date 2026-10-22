"""Negative and alternative-solution tests for m03 (three vague tickets become specs an agent can build from).

The grader here reads Markdown, so the interesting tests are of five kinds:

* the whole lab: the starter fails for the right reasons (and never says what the hidden questions are), the reference
  solution passes, and a *different* sound solution, which decides every question the other way and is laid out
  differently, passes too (a grader has to accept every sound solution);
* the wrong specs people and agents really write: the ticket pasted back, the unfilled template, a generic
  boilerplate spec, questions instead of decisions, a line of keywords, vague criteria, invented files, a plan of
  fifteen steps or of one giant step, a plan that writes the code first, floats, banker's rounding and a new
  dependency, no second reviewer, three copies of one spec, the feature built instead of specified;
* each hidden ambiguity on its own: a natural sentence resolves it, the same sentence as a question does not;
* the readers behind the checks (blocks, list items, sections, plan steps) as plain unit tests;
* the kit's own consistency: the numbers in the reference specs are the ones the Remit code really produces, the
  template carries every heading the grader wants, and the task text agrees with the constants of the grader.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import time
from pathlib import Path

import pytest

from ailab import checks_m03 as m, framework, runner
from ailab.checks_m03 import (
    N_CLEAN, N_COMMITS, N_CRITERIA, N_DISTINCT, N_EXAMPLES, N_EXIST, N_FILES, N_FILLER, N_LISTS, N_LOG, N_PLACEHOLDERS,
    N_PLAN_SHAPE, N_PLAN_SIZE, N_REVIEW, N_RISKS, N_RULES, N_SCOPE, N_SECTIONS, N_TESTS, n_ambiguities,
)
from conftest import learner_commit, start
from m03_alt_specs import T1 as ALT_T1, T2 as ALT_T2, T3 as ALT_T3

HERE = Path(m.__file__).resolve().parent / "labs" / "m03_specs"
REFERENCE = {t: (HERE / "solution" / f"{t}.md").read_text(encoding="utf-8") for t in m.TICKETS}
ALTERNATIVE = {"T1": ALT_T1, "T2": ALT_T2, "T3": ALT_T3}
LOG_OK = (HERE / "solution" / "agent-log.md").read_text(encoding="utf-8")

AMB = {t: n_ambiguities(t) for t in m.TICKETS}
SECRETS = "No secrets in the change"
SPEC_ONLY = {N_EXIST, N_SECTIONS, N_PLACEHOLDERS, N_FILLER, N_EXAMPLES, N_CRITERIA, N_LISTS, N_FILES, *AMB.values(), N_RULES,
             N_REVIEW, N_PLAN_SIZE, N_PLAN_SHAPE, N_DISTINCT, N_RISKS, N_LOG}
ALL = SPEC_ONLY | {N_SCOPE, N_TESTS, N_COMMITS, N_CLEAN, SECRETS}
ADVISORY = {N_RISKS, N_LOG}
GOOD_MESSAGE = "docs(specs): write the three specs"


# --------------------------------------------------------------------------------------------
# fixtures and helpers
# --------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def template(tmp_path_factory) -> Path:
    return start("m03", tmp_path_factory.mktemp("m03-template") / "work")


@pytest.fixture
def work(template, tmp_path) -> Path:
    """A private copy of the started lab (the .git folder and the lab-start tag come with it)."""
    target = tmp_path / "work"
    shutil.copytree(template, target)
    return target


def write(work: Path, specs: dict[str, str], log: str | None = LOG_OK) -> None:
    for ticket, text in specs.items():
        (work / "specs" / f"{ticket}.md").write_text(text, encoding="utf-8")
    if log is not None:
        (work / "agent-log.md").write_text(log, encoding="utf-8")


def spec_grade(work: Path) -> dict[str, framework.Check]:
    """Only the spec checks (fast: no pytest run, no git)."""
    return {c.name: c for c in m.spec_checks(work)}


def full_grade(work: Path) -> dict[str, framework.Check]:
    return {c.name: c for c in framework.grade_lab(framework.load_lab("m03"), work, catch=False)}


def failing(result: dict[str, framework.Check]) -> set[str]:
    return {name for name, check in result.items() if not check.ok}


def assert_only(result: dict[str, framework.Check], *expected: str) -> None:
    got = failing(result)
    detail = "\n".join(f"  {'ok  ' if c.ok else 'FAIL'} {n}: {c.detail}" for n, c in result.items())
    assert got == set(expected), f"expected failures {set(expected)}, got {got}\n{detail}"


def edit(text: str, old: str, new: str) -> str:
    assert old in text, f"{old!r} is not in the text"
    return text.replace(old, new, 1)


def section_of(text: str, title: str) -> str:
    match = re.search(rf"^### {re.escape(title)}\b.*?(?=^### |\Z)", text, re.S | re.M)
    assert match, title
    return match.group(0)


def replace_section(text: str, title: str, body: str) -> str:
    return text.replace(section_of(text, title), f"### {title}\n{body.strip()}\n\n", 1)


def reference_with(**changes) -> dict[str, str]:
    """The reference specs; ``changes`` maps a ticket to a function that edits its text."""
    return {t: changes[t](text) if t in changes else text for t, text in REFERENCE.items()}


def one(ticket: str, text: str) -> m.Spec:
    return m.Spec(ticket, f"specs/{ticket}.md", text)


# --------------------------------------------------------------------------------------------
# the starter and the right answers
# --------------------------------------------------------------------------------------------
def test_the_starter_fails_for_the_right_reasons(work):
    result = full_grade(work)
    assert set(result) == ALL
    assert failing(result) == ALL - {N_SCOPE, N_TESTS, N_CLEAN, SECRETS}
    assert all(c.hint or c.detail for c in result.values() if not c.ok)
    assert all(not result[name].required for name in ADVISORY)


def test_the_starter_reveals_nothing_about_the_hidden_questions(work):
    """Details and hints may name a *family* of questions after an attempt, never the question itself."""
    text = " ".join(f"{c.detail} {c.hint}" for c in full_grade(work).values()).lower()
    for word in ("express", "surcharge", "std-b", "pkr", "manila", "karachi", "weekend", "friday", "half up", "min_send",
                 "max_send", "cut-off", "derived", "egypt"):
        assert word not in text, word


def test_the_reference_solution_passes_every_check(work):
    framework.solve_lab(framework.load_lab("m03"), work)
    assert_only(full_grade(work))


def test_an_alternative_sound_solution_with_the_opposite_decisions_is_accepted(work):
    write(work, ALTERNATIVE, log="# Agent log\n\nNo agent used: I wrote the specs from the code.\n")
    learner_commit(work, GOOD_MESSAGE)
    result = full_grade(work)
    assert_only(result)
    assert result[AMB["T1"]].detail == "4 of 4 resolved" and result[AMB["T3"]].detail == "6 of 6 resolved"


def test_tool_noise_and_extra_notes_in_specs_do_not_count_against_the_learner(work):
    write(work, REFERENCE)
    (work / "specs" / "interview-notes.md").write_text("What I asked the agent, and what I answered.\n", encoding="utf-8")
    (work / ".claude").mkdir()
    (work / ".claude" / "settings.local.json").write_text("{}", encoding="utf-8")
    (work / ".DS_Store").write_bytes(b"\0\0")
    learner_commit(work, GOOD_MESSAGE)
    assert_only(full_grade(work))


def test_many_small_commits_are_fine(work):
    for ticket in m.TICKETS:
        write(work, {ticket: REFERENCE[ticket]})
        learner_commit(work, f"docs(specs): spec {ticket}")
    assert_only(full_grade(work))


# --------------------------------------------------------------------------------------------
# the wrong files people and agents really write
# --------------------------------------------------------------------------------------------
def test_the_tickets_pasted_back_as_specs_resolve_nothing(work):
    tickets = {t: (work / "lab-assets" / "tickets" / f"{t}.md").read_text(encoding="utf-8") for t in m.TICKETS}
    notes = (work / "lab-assets" / "hessa-notes.md").read_text(encoding="utf-8")
    for ticket, text in tickets.items():
        for source in (text, notes, text + "\n\n" + notes):
            solved = m.resolution(ticket, one(ticket, source))
            assert not any(solved.values()), (ticket, solved)
    write(work, tickets)
    result = spec_grade(work)
    assert {N_SECTIONS, N_EXAMPLES, N_CRITERIA, N_FILES, N_PLAN_SIZE, N_PLAN_SHAPE, *AMB.values()} <= failing(result)


def test_the_unfilled_template_copied_three_times(work):
    template_text = (work / "specs" / "TEMPLATE.md").read_text(encoding="utf-8")
    write(work, {t: template_text for t in m.TICKETS})
    result = spec_grade(work)
    assert {N_PLACEHOLDERS, N_EXAMPLES, N_CRITERIA, N_FILES, N_PLAN_SIZE, N_PLAN_SHAPE, N_DISTINCT, *AMB.values()} <= failing(result)
    assert "TODO" in result[N_PLACEHOLDERS].detail


GENERIC = """\
# REMIT-341: Egypt discount

## Goal
Implement a robust and scalable discount feature that provides a seamless, user-friendly experience for customers sending money to Egypt.

## Context
Najm Remit is a remittance platform. The team follows best practices, writes clean code and handles edge cases, etc.

## Behaviour
The system shall apply the discount properly and the fee should be calculated correctly as expected for all customers.

## Acceptance criteria
- The discount works properly for all users
- The fee is displayed correctly
- The message is user-friendly and easy to use
- All tests pass and the code is production-ready

## Constraints
- Follow best practices and write clean, maintainable code
- Make sure the feature is robust and scalable
- Leverage the existing architecture

## Non-goals
- Anything not mentioned in the ticket

## Decisions and open questions
- Should the discount apply to express transfers?
- What about the minimum fee?
- How should we round?

## Risks
There may be risks; the team will monitor them closely and handle them appropriately.

## Test plan
Write unit tests that ensure everything works.

## Plan
1. Implement the feature.
2. Test the feature.
3. Deploy the feature.
"""


def test_a_generic_boilerplate_spec_fails_where_it_should(work):
    write(work, {t: GENERIC for t in m.TICKETS})
    result = spec_grade(work)
    assert {N_FILLER, N_EXAMPLES, N_CRITERIA, N_FILES, N_PLAN_SIZE, N_PLAN_SHAPE, N_DISTINCT, *AMB.values()} <= failing(result)
    assert "vague quality word" in result[N_FILLER].detail
    assert not any(m.resolution("T1", one("T1", GENERIC)).values())


def test_a_missing_section_is_named(work):
    write(work, reference_with(T2=lambda t: t.replace(section_of(t, "Non-goals"), "")))
    result = spec_grade(work)
    assert_only(result, N_SECTIONS, N_LISTS)
    assert "T2: missing Non-goals" in result[N_SECTIONS].detail


def test_a_one_line_section_is_too_thin(work):
    write(work, reference_with(T3=lambda t: replace_section(t, "Behaviour", "See the ticket.")))
    result = spec_grade(work)
    assert N_SECTIONS in failing(result) and N_EXAMPLES in failing(result)
    assert "Behaviour" in result[N_SECTIONS].detail


def test_a_placeholder_left_behind(work):
    write(work, reference_with(T1=lambda t: edit(t, "### Context\n", "### Context\nTODO: add the link to the planning notes.\n")))
    result = spec_grade(work)
    assert_only(result, N_PLACEHOLDERS)
    assert "T1: line" in result[N_PLACEHOLDERS].detail


@pytest.mark.parametrize(
    "phrase",
    ["The result is user-friendly.", "Everything works as expected.", "Cover all edge cases, etc.", "We leverage the existing code.",
     "The code follows best practices.", "The system shall be robust."],
)
def test_filler_is_caught(work, phrase):
    write(work, reference_with(T2=lambda t: edit(t, "### Risks\n", f"### Risks\n{phrase}\n")))
    assert_only(spec_grade(work), N_FILLER)


def test_behaviour_without_exact_examples(work):
    prose = "The discount applies to Egypt transfers and the customer sees a smaller fee than before on the quote screen."
    write(work, reference_with(T1=lambda t: replace_section(t, "Behaviour", prose)))
    result = spec_grade(work)
    assert N_EXAMPLES in failing(result)
    assert "T1: 0 line(s)" in result[N_EXAMPLES].detail


@pytest.mark.parametrize(
    "criteria",
    [
        "- The discount works properly\n- The fee is correct\n- The message looks good\n- Everything behaves as expected",
        "- The fee is `8.08` on 260.00 QAR\n- The saving is `1.42`",
        "- Given 260.00 QAR\n- When the fee is priced\n- Then the fee is 8.08 QAR",
    ],
    ids=["vague", "too few", "given-when-then-as-three-items-is-fine-only-if-merged"],
)
def test_criteria_that_cannot_be_checked(work, criteria):
    write(work, reference_with(T1=lambda t: replace_section(t, "Acceptance criteria", criteria)))
    result = spec_grade(work)
    assert N_CRITERIA in failing(result)


def test_given_when_then_lines_are_one_criterion_not_three(work):
    criteria = "\n".join(
        [
            "- Given a transfer of 260.00 QAR to `QAR-EGP`",
            "- When the fee is priced",
            "- Then `quote_fee` returns 8.08 QAR",
            "- Given a transfer of 100.00 QAR to `QAR-EGP`",
            "- When the fee is priced",
            "- Then `quote_fee` returns 5.10 QAR",
            "- Given a transfer of 500.00 QAR to `QAR-PKR`",
            "- When the fee is priced",
            "- Then `quote_fee` returns 15.50 QAR",
            "- Given a transfer of 500.00 QAR to `QAR-INR`",
            "- When the fee is priced",
            "- Then `quote_fee` returns 12.00 QAR",
        ]
    )
    assert len(m.list_items(criteria)) == 4
    write(work, reference_with(T1=lambda t: replace_section(t, "Acceptance criteria", criteria)))
    assert_only(spec_grade(work))


def test_a_table_of_criteria_is_read_without_its_header(work):
    table = ("| Id | Criterion |\n|---|---|\n| A1 | `quote_fee` for 260.00 QAR on `QAR-EGP` returns 8.08 QAR |\n"
             "| A2 | the fee for 100.00 QAR on `QAR-EGP` is 5.10 QAR |\n| A3 | `QAR-PKR` still returns 15.50 QAR for 500.00 QAR |\n"
             "| A4 | the saving printed for 260.00 QAR is \"1.42 QAR\" |")
    assert len(m.list_items(table)) == 4
    write(work, reference_with(T1=lambda t: replace_section(t, "Acceptance criteria", table)))
    assert_only(spec_grade(work))


# --- files -----------------------------------------------------------------------------------
def test_a_file_that_does_not_exist_is_named(work):
    write(work, reference_with(T1=lambda t: edit(t, "Files: ", "Files: `src/remit/discounts.py` (already there), ")))
    result = spec_grade(work)
    assert_only(result, N_FILES)
    assert "src/remit/discounts.py" in result[N_FILES].detail


def test_the_stale_architecture_doc_trap(work):
    """docs/ARCHITECTURE.md still describes risk.py. Copying that into a spec names a file that is not there."""
    write(work, reference_with(T3=lambda t: edit(t, "### Context\n", "### Context\n- Limits and screening are checked in `src/remit/risk.py`, as the architecture document says.\n")))
    result = spec_grade(work)
    assert_only(result, N_FILES)
    assert "src/remit/risk.py" in result[N_FILES].detail


def test_saying_that_a_file_is_gone_or_new_is_fine(work):
    gone = "- `docs/ARCHITECTURE.md` still describes `src/remit/risk.py`, which no longer exists; the code wins.\n"
    new = "- Create a new file `tests/test_discount_property.py` for the add-up loop.\n"
    write(work, reference_with(T1=lambda t: edit(t, "### Context\n", "### Context\n" + gone + new)))
    assert_only(spec_grade(work))


def test_a_spec_that_names_no_tests_or_no_code(work):
    no_tests = lambda t: re.sub(r"tests/[\w./-]+", "the tests", t)  # noqa: E731
    write(work, reference_with(T2=no_tests))
    result = spec_grade(work)
    assert N_FILES in failing(result)
    assert "src/" in result[N_FILES].detail and "tests/" in result[N_FILES].detail


# --- the hidden ambiguities -------------------------------------------------------------------
def test_a_line_of_keywords_resolves_nothing(work):
    stuffed = {
        "T1": "express surcharge minimum discount round half up Decimal QAR-EGP only PKR STD-B",
        "T2": "INR QAR round up at least tier boundary inclusive min_send derived amount",
        "T3": "Qatar cut-off 18:00 exactly inclusive tomorrow Friday weekend cash_pickup only Arabic-Indic digits",
    }
    for ticket, line in stuffed.items():
        solved = m.resolution(ticket, one(ticket, f"# {ticket}\n\n## Decisions\n{line}\n"))
        assert sum(solved.values()) <= 1, (ticket, solved)
        # even repeated seven times in seven sections, a line of keywords is only as good as the number of separate lines
        many = "\n".join(f"## Section {i}\n{line}\n" for i in range(3))
        assert sum(m.resolution(ticket, one(ticket, many)).values()) <= 3


def test_one_sentence_cannot_resolve_two_questions(work):
    text = "The express surcharge and the minimum fee of 6.00 are both left out of the 15% discount in this offer.\n"
    solved = m.resolution("T1", one("T1", text))
    assert sum(solved.values()) == 1, solved


def test_questions_are_not_decisions(work):
    questions = """\
- Should the 15% discount apply to the express surcharge as well as the base fee?
- Does the discount go below the minimum fee of 6.00 for the smallest transfers?
- How is the discounted fee rounded: half up to 0.01, or some other way?
- Is the offer for the corridor QAR-EGP only, or for every corridor that uses STD-B?
"""
    text = "# T1\n\n## Decisions and open questions\n" + questions
    assert not any(m.resolution("T1", one("T1", text)).values())
    answered = questions.replace("?", ".")  # the same words as statements resolve them
    assert sum(m.resolution("T1", one("T1", "# T1\n\n## Decisions and open questions\n" + answered)).values()) == 4


def test_a_question_and_its_answer_in_one_bullet(work):
    bullet = ("- Q: Does the 15% discount apply to the express surcharge? A: No, only the base fee is discounted, "
              "and the express surcharge of 20.00 stays as it is.\n")
    assert m.resolution("T1", one("T1", "# T1\n\n## Decisions\n" + bullet))["express"]


def test_a_short_crisp_decision_counts():
    assert m.resolution("T1", one("T1", "# T1\n\n### Decisions\n- The express surcharge is not discounted.\n"))["express"]


def test_a_decision_under_its_own_sub_heading_counts():
    text = "# T1\n\n### Decisions and open questions\n#### Express surcharge\nNot discounted: only the base fee gets the 15%.\n"
    assert m.resolution("T1", one("T1", text))["express"]


def test_feedback_arrives_before_all_three_specs_exist(work):
    """One finished spec is graded on its own; the checks that need all three say so only when nothing else is wrong."""
    write(work, {"T1": GENERIC}, log=None)
    result = spec_grade(work)
    assert "T1:" in result[N_FILLER].detail and "no specs yet" not in result[N_FILLER].detail
    assert "specs/T2.md" in result[N_EXIST].detail
    write(work, {"T1": REFERENCE["T1"]}, log=None)
    result = spec_grade(work)
    assert result[N_FILLER].detail == "T1 ok; waiting for specs/T2.md, specs/T3.md" and result[AMB["T1"]].ok
    assert result[N_SECTIONS].detail == "T1 ok; waiting for specs/T2.md, specs/T3.md"
    write(work, {"T2": REFERENCE["T2"]}, log=None)
    result = spec_grade(work)
    assert result[N_SECTIONS].detail == "T1, T2 ok; waiting for specs/T3.md"
    assert result[N_DISTINCT].detail == "T1, T2 ok; waiting for specs/T3.md" and not result[N_DISTINCT].ok


def test_a_bold_question_lead_in_does_not_swallow_its_answer():
    text = "# T1\n\n### Decisions\n- **Rounding?** The discounted fee is rounded half up to 0.01 with Decimal.\n"
    assert m.resolution("T1", one("T1", text))["rounding"]
    quoted = '- The ticket asks "how much do I send?" and we decide: the customer pays in QAR, the family gets INR.\n'
    assert m.resolution("T2", one("T2", "# T2\n\n### Decisions\n" + quoted))["currency"]


RESOLVERS = {
    ("T1", "express"): "The express surcharge of 20.00 is not discounted; the 15% discount applies to the base fee only.",
    ("T1", "minimum"): "The discount is applied after the minimum fee of 6.00, so a small transfer can end up below that minimum.",
    ("T1", "rounding"): "The discount is rounded half up to 0.01 using Decimal, so 1.425 becomes 1.43 on the fee.",
    ("T1", "corridor"): "The offer applies to the corridor QAR-EGP only; QAR-PKR shares STD-B and stays unchanged.",
    ("T2", "currency"): "The typed amount is in the receive currency, such as INR, while the customer pays in QAR.",
    ("T2", "direction"): "The send amount is rounded up to the next 0.01 QAR so the family receives at least the target.",
    ("T2", "tier"): "The fee tier is taken from the derived send amount, so a target on a tier boundary can change the fee.",
    ("T2", "limits"): "The derived QAR amount must stay within min_send and max_send, both inclusive.",
    ("T3", "zone"): "The cut-off of 18:00 is read in Qatar time, which is UTC+3 all year.",
    ("T3", "boundary"): "A transfer at exactly 18:00:00 is after the cut-off, and 17:59:59 is before it.",
    ("T3", "day"): "Tomorrow means the next calendar day in Qatar time, and weekends are not handled here.",
    ("T3", "scope"): "Only cash_pickup transfers get the note; bank_deposit and wallet keep the old message.",
    ("T3", "ar-wording"): "بما أنك أرسلت التحويل بعد الساعة مساءً بتوقيت قطر يمكن للمستلم استلام المبلغ غداً",
    ("T3", "ar-digits"): "Times in the Arabic message use Arabic-Indic digits through localize_digits and names stay Latin.",
}
ALL_PAIRS = [(t, a.id) for t, ambs in m.AMBIGUITIES.items() for a in ambs]


def test_every_hidden_ambiguity_has_a_resolver_in_these_tests():
    assert set(RESOLVERS) == set(ALL_PAIRS)


@pytest.mark.parametrize(("ticket", "amb"), ALL_PAIRS, ids=[f"{t}-{a}" for t, a in ALL_PAIRS])
def test_a_natural_sentence_resolves_exactly_its_ambiguity_and_a_question_does_not(ticket, amb):
    sentence = RESOLVERS[(ticket, amb)]
    solved = m.resolution(ticket, one(ticket, f"# {ticket}\n\n## Decisions\n- {sentence}\n"))
    assert solved[amb], sentence
    asked = sentence.rstrip(".") + (" ؟" if amb == "ar-wording" else "?")
    assert not any(m.resolution(ticket, one(ticket, f"# {ticket}\n\n## Decisions\n- {asked}\n")).values()), asked


# Other sound ways of putting the same decisions: found by reading what learners and agents naturally write. Each must resolve
# its ambiguity, and the same words as a question must not.
OTHER_WORDINGS = [
    ("T1", "express", "The offer does not cover the express surcharge."),
    ("T1", "express", "Express transfers keep their full 20.00 surcharge; only the base fee is reduced."),
    ("T1", "minimum", "The minimum fee of 6.00 still applies after the offer, so a small transfer pays at least that."),
    ("T1", "rounding", "The discounted fee is rounded to the nearest 0.01 QAR, with ties going up."),
    ("T1", "corridor", "The discount is for the Egypt corridor and nothing else."),
    ("T1", "corridor", "Egypt transfers get 15% off; Pakistan, which uses the same schedule, is excluded."),
    ("T2", "currency", "The amount the customer enters is denominated in the destination currency, while the debit is in QAR."),
    ("T2", "currency", "The target is in the recipient's currency; the sender is always debited in Qatari riyals."),
    ("T2", "direction", "We take the smallest send amount that delivers the target or more."),
    ("T2", "direction", "If the exact amount does not exist, the family gets slightly more rather than slightly less."),
    ("T2", "tier", "Fees are calculated on the QAR amount we derive, not on the typed target."),
    ("T2", "limits", "A target that needs more than 25,000.00 QAR is refused with AmountOutOfRange."),
    ("T3", "zone", "The evening cut-off is measured in the customer's local time in Doha."),
    ("T3", "boundary", "Anything before 18:00 is unchanged, anything from 18:00 onwards gets the note."),
    ("T3", "day", "We say 'tomorrow' and do not promise a weekday; Friday and Saturday are open questions for Ops."),
    ("T3", "scope", "The pickup note applies just to cash pick-up deliveries."),
    ("T3", "ar-digits", "Numbers in the Arabic text are rendered with Arabic numerals."),
    # found by the learner dry-run: sound sentences that the first keyword lists missed
    ("T1", "minimum", "The floor of 6.00 QAR is kept for small transfers."),
    ("T1", "rounding", "Round half up to the cent, with Decimal."),
    ("T2", "tier", "The fee is priced on the send amount that results from the search, as for a normal quote."),
    ("T2", "limits", "The smallest or largest allowed transfer is checked against the amount we derive."),
    ("T3", "ar-wording", "The Arabic sentence is left to the native reader."),
    ("T3", "ar-wording", "A translator drafts the Arabic text and a native reader approves it before release."),
    ("T3", "ar-wording", "The Arabic wording is supplied by the native Arabic reader before the build, so this spec does not fix the sentence."),
]


@pytest.mark.parametrize(("ticket", "amb", "sentence"), OTHER_WORDINGS, ids=[f"{t}-{a}-{i}" for i, (t, a, _) in enumerate(OTHER_WORDINGS)])
def test_other_natural_wordings_of_a_decision_count_and_their_questions_do_not(ticket, amb, sentence):
    assert m.resolution(ticket, one(ticket, f"# {ticket}\n\n## Decisions\n- {sentence}\n"))[amb], sentence
    asked = sentence.rstrip(".") + "?"
    assert not any(m.resolution(ticket, one(ticket, f"# {ticket}\n\n## Decisions\n- {asked}\n")).values()), asked


def test_a_sentence_for_one_ticket_does_not_resolve_another_tickets_questions():
    for ticket, amb in ALL_PAIRS:
        for other in m.TICKETS:
            if other == ticket:
                continue
            solved = m.resolution(other, one(other, f"# {other}\n\n## Decisions\n- {RESOLVERS[(ticket, amb)]}\n"))
            # a few shared words are allowed to coincide (rounding, boundaries) but never more than one question at a time
            assert sum(solved.values()) <= 1, (ticket, amb, other, solved)


def test_decisions_may_live_in_behaviour_or_criteria_not_only_in_decisions(work):
    """The alternative T3 decides the zone and the boundary in its Behaviour section, and passes."""
    solved = m.resolution("T3", one("T3", ALT_T3))
    assert solved["zone"] and solved["boundary"]


def test_failing_ambiguities_name_only_families(work):
    partial = "\n".join(f"- {RESOLVERS[('T3', amb)]}" for amb in ("zone", "boundary", "scope"))
    write(work, reference_with(T3=lambda t: "# T3\n\n## Decisions\n" + partial + "\n"))
    result = spec_grade(work)
    detail = result[AMB["T3"]].detail
    assert detail == "3 of 6 resolved; still open: time and zones (1 of 2), Arabic (all 2)", detail
    assert result[AMB["T3"]].hint and "Qatar" not in result[AMB["T3"]].hint
    assert result[AMB["T1"]].ok and result[AMB["T2"]].ok


# --- house rules ------------------------------------------------------------------------------
@pytest.mark.parametrize(
    ("line", "label"),
    [
        ("Compute the fee with a float and round(x, 2), then format it.", "float money"),
        ("Use banker's rounding (ROUND_HALF_EVEN) for the discount.", "banker's rounding"),
        ("Call datetime.now() in the service to find the time.", "a direct clock or id call"),
        ("Use pytz for the time zone conversion.", "a new dependency"),
        ("Run pip install babel to format the Arabic numbers.", "a new dependency"),
    ],
)
def test_decisions_that_break_the_house_rules(work, line, label):
    write(work, reference_with(T1=lambda t: edit(t, "### Constraints\n", f"### Constraints\n- {line}\n")))
    result = spec_grade(work)
    assert_only(result, N_RULES)
    assert label in result[N_RULES].detail


def test_saying_what_you_will_not_do_is_not_breaking_the_rule(work):
    ok = "- Never use a float for money, do not call datetime.now() and do not add pytz or any other dependency.\n"
    ledger = "- The ledger's partner share is rounded half-even (Q-LED-1); that quirk is left alone.\n"
    write(work, reference_with(T1=lambda t: edit(t, "### Constraints\n", "### Constraints\n" + ok + ledger)))
    assert_only(spec_grade(work))


@pytest.mark.parametrize(
    "sentence",
    [
        "Customer requests for a refund after a rejected quote could rise.",
        "Support receives many requests about reverse quotes each week.",  # no negation word to hide behind
        "A reverse quote requests the same checks as a forward quote.",
    ],
)
def test_requests_in_prose_is_not_a_dependency(work, sentence):
    write(work, reference_with(T2=lambda t: edit(t, "### Risks\n", f"### Risks\n{sentence}\n")))
    assert_only(spec_grade(work))


def test_the_requests_library_is_a_dependency(work):
    write(work, reference_with(T2=lambda t: edit(t, "### Constraints\n", "### Constraints\n- Fetch the live rate with the requests library.\n")))
    result = spec_grade(work)
    assert_only(result, N_RULES)
    assert "a new dependency" in result[N_RULES].detail


# --- reviewers ----------------------------------------------------------------------------------
def test_money_logic_without_a_second_reviewer(work):
    no_review = lambda t: re.sub(r"[^\n]*second (?:human )?reviewer[^\n]*", "", t)  # noqa: E731
    write(work, reference_with(T1=no_review, T3=no_review))
    result = spec_grade(work)
    assert N_REVIEW in failing(result)
    assert "T1:" in result[N_REVIEW].detail and "T3:" in result[N_REVIEW].detail and "T2:" not in result[N_REVIEW].detail


@pytest.mark.parametrize("wording", ["An independent reviewer approves it.", "A reviewer other than the author approves it.", "It gets a four-eyes review."])
def test_other_ways_of_naming_the_second_reviewer_count(work, wording):
    no_review = lambda t: re.sub(r"[^\n]*second (?:human )?reviewer[^\n]*", wording, t)  # noqa: E731
    write(work, reference_with(T1=no_review))
    assert_only(spec_grade(work))


def test_a_second_reviewer_in_the_plan_counts(work):
    def move(t: str) -> str:
        t = re.sub(r"[^\n]*second human reviewer[^\n]*\n", "", t)
        return edit(t, "Rollback:", "Rollback: a second human reviewer approves before merge.")

    write(work, reference_with(T1=move))
    assert_only(spec_grade(work))


# --- plans ----------------------------------------------------------------------------------------
def with_plan(plan: str):
    return lambda t: t[: t.index("### Plan")] + "### Plan\n" + plan.strip() + "\n"


FIFTEEN = "\n".join(f"{i}. Change a little more of `src/remit/fees.py` and run `pytest -q`." for i in range(1, 16)) + "\nRollback: git revert."


def test_a_plan_of_fifteen_steps(work):
    write(work, reference_with(T1=with_plan(FIFTEEN)))
    result = spec_grade(work)
    assert N_PLAN_SIZE in failing(result)
    assert "15 numbered steps" in result[N_PLAN_SIZE].detail


def test_a_plan_of_one_giant_step(work):
    plan = ("1. Implement the whole feature in `src/remit/fees.py`, `src/remit/service.py`, `src/remit/notify.py` and `src/remit/cli.py`, "
            "with all the tests, update every document, run `pytest -q`, fix whatever fails and then prepare the pull request text.\n"
            "Rollback: git revert.")
    write(work, reference_with(T1=with_plan(plan)))
    result = spec_grade(work)
    assert N_PLAN_SIZE in failing(result)
    assert "1 numbered steps" in result[N_PLAN_SIZE].detail


def test_a_step_that_is_too_long_or_touches_too_many_files(work):
    long_step = "Rewrite " + "the whole module and all its helpers carefully " * 12 + "in `src/remit/fees.py`."
    broad = "Edit `src/remit/fees.py`, `src/remit/fx.py`, `src/remit/service.py` and `src/remit/notify.py` together."
    plan = f"1. Run `pytest -q` and note the baseline.\n2. Add a failing test in `tests/test_fees.py`.\n3. {long_step}\n4. {broad}\n5. Run `pytest -q`.\nRollback: git revert."
    write(work, reference_with(T1=with_plan(plan)))
    detail = spec_grade(work)[N_PLAN_SIZE].detail
    assert "step 3 is" in detail and "step 4 touches more than 3 files" in detail


def test_a_step_that_names_nothing_to_check(work):
    plan = ("1. Run `pytest -q`.\n2. Add a failing test in `tests/test_fees.py`.\n3. Think about the design for a while.\n"
            "4. Change `src/remit/fees.py` and run `pytest -q`.\nRollback: git revert.")
    write(work, reference_with(T1=with_plan(plan)))
    assert "step 3 names no file" in spec_grade(work)[N_PLAN_SIZE].detail


def test_a_plan_that_writes_the_code_first(work):
    plan = ("1. Create the branch `remit-341` and run `pytest -q`.\n2. Add the discount in `src/remit/fees.py`.\n"
            "3. Add tests in `tests/test_fees.py` and run `pytest -q tests/test_fees.py`.\n4. Show the saving in `src/remit/service.py`.\n"
            "Rollback: git revert.")
    write(work, reference_with(T1=with_plan(plan)))
    result = spec_grade(work)
    assert_only(result, N_PLAN_SHAPE)
    assert "changes the code before step 3 writes the test" in result[N_PLAN_SHAPE].detail


def test_a_step_that_names_the_failing_tests_without_the_word_add_is_a_test_step(work):
    plan = ("1. Create the branch `remit-341` and run `pytest -q`.\n2. Failing tests for the table in Behaviour: `tests/test_fees.py`.\n"
            "3. Change `src/remit/fees.py` until they pass; run `pytest -q`.\n4. Show the saving in `src/remit/service.py`; run `pytest -q`.\n"
            "Rollback: git revert.")
    write(work, reference_with(T1=with_plan(plan)))
    assert_only(spec_grade(work))


def test_a_test_and_its_code_in_one_step_is_fine(work):
    plan = ("1. Create the branch `remit-341` and run `pytest -q`.\n2. Add a failing test in `tests/test_fees.py`, then make it pass in `src/remit/fees.py`.\n"
            "3. Show the saving in `src/remit/service.py` and run `pytest -q`.\n4. Add the message in `src/remit/notify.py` and run `pytest -q`.\n"
            "Rollback: git revert.")
    write(work, reference_with(T1=with_plan(plan)))
    assert_only(spec_grade(work))


@pytest.mark.parametrize(
    ("drop", "message"),
    [("no tests", "no step writes a test"), ("no pytest", "no step runs pytest"), ("no rollback", "no rollback")],
)
def test_a_plan_missing_its_test_check_or_rollback(work, drop, message):
    steps = ["Create the branch `remit-341` and note the baseline with `git status`.", "Add a failing test in `tests/test_fees.py`.",
             "Change `src/remit/fees.py` to make it pass.", "Run `pytest -q`, read `git diff --stat` and ask the reviewer."]
    if drop == "no tests":
        steps[1] = "Look at `tests/test_fees.py` for the existing fee tests."
    if drop == "no pytest":
        steps[3] = "Read `git diff --stat` and ask the reviewer to look at `src/remit/fees.py`."
        steps[0] = "Create the branch `remit-341` and note the baseline with `git status`."
    plan = "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1)) + ("" if drop == "no rollback" else "\nRollback: git revert the commits.")
    write(work, reference_with(T1=with_plan(plan)))
    assert message in spec_grade(work)[N_PLAN_SHAPE].detail


def test_a_plan_in_sub_sections_with_checkboxes_is_read(work):
    plan = """\
### Files
`src/remit/fees.py`, `tests/test_fees.py`, `src/remit/service.py`, `tests/test_service.py`

### Steps
- [ ] 1. Create the branch `remit-341` and run `pytest -q`.
- [ ] 2. Add a failing test in `tests/test_fees.py` for the table in Behaviour.
- [ ] 3. Change `src/remit/fees.py` until it passes; run `pytest -q tests/test_fees.py`.
- [ ] 4. Show the saving in `src/remit/service.py`; run `pytest -q`.

### Rollback
Delete the branch before merge, or `git revert` the commits.
"""
    assert len(m.plan_steps(one("T1", "## Plan\n" + plan))) == 4
    write(work, reference_with(T1=with_plan(plan)))
    assert_only(spec_grade(work))


def test_unnumbered_bullets_are_not_steps(work):
    plan = "- Create the branch and run `pytest -q`.\n- Add a failing test in `tests/test_fees.py`.\n- Change `src/remit/fees.py`.\n- Run `pytest -q`.\nRollback: git revert."
    write(work, reference_with(T1=with_plan(plan)))
    assert "0 numbered steps" in spec_grade(work)[N_PLAN_SIZE].detail


# --- three copies, risks, the log -----------------------------------------------------------------
def test_three_copies_of_one_spec(work):
    write(work, {t: REFERENCE["T1"] for t in m.TICKETS})
    result = spec_grade(work)
    assert N_DISTINCT in failing(result) and result[N_DISTINCT].required
    assert {AMB["T2"], AMB["T3"]} <= failing(result)


def test_one_spec_copied_into_another_ticket_fails_a_required_check_whatever_it_resolves(work):
    """T1's text with only the ticket id changed used to pass every required check for T2 (the hidden questions were met by words
    that T1 also contains). The copy check is required now."""
    copy = REFERENCE["T1"].replace("REMIT-341", "REMIT-342")
    write(work, {"T1": REFERENCE["T1"], "T2": copy, "T3": REFERENCE["T3"]})
    result = spec_grade(work)
    assert not result[N_DISTINCT].ok and result[N_DISTINCT].required
    assert result[N_DISTINCT].detail == "too similar: T1 and T2"
    write(work, {"T2": REFERENCE["T1"].replace("REMIT-341", "REMIT-342")}, log=None)
    learner_commit(work, GOOD_MESSAGE)
    assert not framework.passed(framework.grade_lab(framework.load_lab("m03"), work, catch=False))


def test_specs_that_share_only_the_template_are_not_copies(work):
    write(work, REFERENCE)
    assert spec_grade(work)[N_DISTINCT].ok
    write(work, ALTERNATIVE)
    assert spec_grade(work)[N_DISTINCT].ok


def test_risks_and_the_log_are_advisory(work):
    write(work, reference_with(T1=lambda t: t.replace(section_of(t, "Risks"), "")), log=None)
    (work / "agent-log.md").write_text("# Agent log\n\nEntry:\nPrompt:\n", encoding="utf-8")
    result = full_grade(work)
    assert N_RISKS in failing(result) and N_LOG in failing(result)
    assert not result[N_RISKS].required and not result[N_LOG].required
    learner_commit(work, GOOD_MESSAGE)
    assert framework.passed(framework.grade_lab(framework.load_lab("m03"), work, catch=False))


def test_a_filled_agent_log_counts(work):
    filled = ("# Agent log\n\nEntry: 2026-03-02, T1\nPrompt (paste or summarise): interview me about REMIT-341\n"
              "What the agent did: asked eleven questions\nWhat I corrected: it assumed the discount covers express\n"
              "What I checked myself: every answer against fees.py\nMinutes: 35\nWould I delegate it again? Yes, the interview\n")
    write(work, REFERENCE, log=filled)
    assert m.log_check(work).ok


# --------------------------------------------------------------------------------------------
# the typical wrong moves around the spec: building it, editing tests, bad commits, secrets
# --------------------------------------------------------------------------------------------
def test_building_the_feature_instead_of_specifying_it(work):
    write(work, REFERENCE)
    framework.edit_file(work, "src/remit/fees.py", "SCHEDULES: dict[str, FeeSchedule]", "EGYPT_DISCOUNT = _D('0.15')\n\nSCHEDULES: dict[str, FeeSchedule]")
    learner_commit(work, "feat(fees): add the Egypt discount")
    result = full_grade(work)
    assert_only(result, N_SCOPE)
    assert "src/remit/fees.py" in result[N_SCOPE].detail


def test_editing_an_existing_test_to_fit_the_plan(work):
    write(work, REFERENCE)
    framework.edit_file(work, "tests/test_fees.py", 'quote_fee(qar("500.00"), PKR) == qar("15.50")', 'quote_fee(qar("500.00"), PKR) == qar("13.18")')
    learner_commit(work, "test(fees): expect the discounted fee")
    result = full_grade(work)
    assert_only(result, N_SCOPE, N_TESTS)


def test_changing_the_tickets_or_the_template_is_not_allowed_except_the_template(work):
    write(work, REFERENCE)
    (work / "lab-assets" / "tickets" / "T1.md").write_text("# REMIT-341: nothing to see here\n", encoding="utf-8")
    learner_commit(work, GOOD_MESSAGE)
    assert_only(full_grade(work), N_SCOPE)


def test_uncommitted_specs(work):
    write(work, REFERENCE)
    result = full_grade(work)
    assert_only(result, N_COMMITS, N_CLEAN)
    assert "specs/T1.md" in result[N_CLEAN].detail


@pytest.mark.parametrize("message", ["wrote the specs", "docs: write the specs", "Docs(specs): Write the specs", "docs(specs): write the specs."],
                         ids=["no-convention", "no-scope", "wrong-case", "full-stop"])
def test_commit_messages_that_ignore_contributing_md(work, message):
    write(work, REFERENCE)
    learner_commit(work, message)
    result = full_grade(work)
    assert_only(result, N_COMMITS)
    assert "CONTRIBUTING.md" in result[N_COMMITS].hint


def test_a_secret_pasted_into_a_spec(work):
    write(work, reference_with(T1=lambda t: edit(t, "### Context\n", "### Context\n- The staging key is sk_live_" + "9f8e7d6c5b4a3f2e1d0c9b8a" + " (do not lose it).\n")))
    learner_commit(work, GOOD_MESSAGE)
    result = full_grade(work)
    assert_only(result, SECRETS)
    assert "9f8e7d6c" not in result[SECRETS].detail + result[SECRETS].hint


def test_a_missing_spec_is_reported_once_and_the_rest_waits(work):
    write(work, reference_with(), log=None)
    (work / "specs" / "T2.md").unlink()
    result = spec_grade(work)
    assert "specs/T2.md" in result[N_EXIST].detail
    assert "waiting for specs/T2.md" in result[N_SECTIONS].detail
    assert result[AMB["T1"]].ok and result[AMB["T3"]].ok and not result[AMB["T2"]].ok


# --------------------------------------------------------------------------------------------
# hostile and huge input cannot hang or crash the grader
# --------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "line",
    ["`" * 60000, "|" * 60000, "src/" + "a." * 30000, "a" * 100000, "- " * 30000, "." * 100000, "1. " * 20000, "ا" * 100000,
     "(" * 50000],
    ids=["backticks", "pipes", "path", "word", "bullets", "dots", "steps", "arabic", "parens"],
)
def test_hostile_lines_do_not_hang_the_grader(work, line):
    big = "\n".join([REFERENCE["T1"], line, REFERENCE["T1"]])
    write(work, reference_with(T1=lambda t: big))
    began = time.monotonic()
    result = spec_grade(work)
    assert time.monotonic() - began < 8
    assert set(result) == SPEC_ONLY


def test_a_very_long_spec_is_graded_quickly(work):
    long_text = REFERENCE["T2"] + "\n".join(f"- Extra note {i}: the quote keeps the rate for 60 seconds." for i in range(4000))
    write(work, reference_with(T2=lambda t: long_text))
    began = time.monotonic()
    spec_grade(work)
    assert time.monotonic() - began < 8


def test_unreadable_bytes_and_odd_files_do_not_crash(work):
    (work / "specs" / "T1.md").write_bytes(b"\xff\xfe\x00# not utf-8 \x80\x81\n## Goal\n")
    write(work, {t: REFERENCE[t] for t in ("T2", "T3")})
    result = spec_grade(work)
    assert N_SECTIONS in failing(result)
    (work / "specs" / "T3.md").unlink()
    (work / "specs" / "T3.md").mkdir()  # a directory where a spec should be
    assert "specs/T3.md" in spec_grade(work)[N_EXIST].detail


# --------------------------------------------------------------------------------------------
# the readers behind the checks
# --------------------------------------------------------------------------------------------
def test_blocks_reads_items_rows_paragraphs_and_code_lines():
    text = """\
Intro paragraph that continues
on a second line.

- first item
  continued here
- second item
1. numbered item
- [ ] checkbox item

| A | B |
|---|---|
| one | two |

```text
a code line
```

### Sub-heading
A paragraph under a sub-heading.
"""
    got = [(b.kind, b.text) for b in m.blocks(text)]
    assert got == [
        ("para", "Intro paragraph that continues on a second line."),
        ("item", "first item continued here"),
        ("item", "second item"),
        ("item", "numbered item"),
        ("item", "checkbox item"),
        ("row", "one | two"),
        ("code", "a code line"),
        ("para", "Sub-heading: A paragraph under a sub-heading."),
    ]


def test_statements_drop_questions_and_keep_decimals():
    block = m.Block("Does it round? The fee is 12.50 QAR. Is that right? Yes it is.", "para")
    assert m.statements(block) == "The fee is 12.50 QAR. Yes it is."
    assert m.split_sentences('**Rounding?** Half up. He said "why?" and left.') == ["Rounding?", "Half up.", 'He said "why?', "and left."]
    row = m.Block("Question? | Decision: round half up to 0.01 | Source: fees.py", "row")
    assert m.statements(row) == "Decision: round half up to 0.01 Source: fees.py"


def test_sections_include_their_sub_sections_and_test_plan_is_not_plan():
    text = "# T\n\n## Test plan\nRun the tests in `tests/test_fees.py` and read the failures.\n\n## Plan\nFiles first.\n### Steps\n1. Do it.\n"
    spec = one("T1", text)
    assert "Run the tests" in spec.sections["Test plan"] and "Run the tests" not in spec.sections["Plan"]
    assert "### Steps" in spec.sections["Plan"] and "1. Do it." in spec.sections["Plan"]


def test_headings_with_numbers_and_emoji_are_recognised():
    spec = one("T1", "## 1. Goal\nx\n## \U0001f3af Acceptance Criteria\ny\n## Non goals\nz\n## Open questions and decisions\nw\n")
    assert {"Goal", "Acceptance criteria", "Non-goals", "Decisions"} <= set(spec.sections)


def test_checkable_examples():
    assert m.checkable("`quote_fee` for 260.00 QAR returns 8.08 QAR")
    assert m.checkable("The English text ends with \"You saved 1.42 QAR\"")
    assert m.checkable("The Arabic confirmation contains the sentence above, byte for byte")
    assert not m.checkable("The fee is calculated correctly for all customers")
    assert not m.checkable("It works properly for 4 corridors")
    assert not m.checkable("Tests pass")
    assert not m.checkable("The message is user-friendly and looks nice on the phone")


def test_the_template_carries_every_heading_the_grader_wants(work):
    spec = one("T1", (work / "specs" / "TEMPLATE.md").read_text(encoding="utf-8"))
    assert set(spec.sections) == {rule.key for rule in m.SECTION_RULES}
    assert (HERE / "templates" / "spec-template.md").read_text(encoding="utf-8") == (work / "specs" / "TEMPLATE.md").read_text(encoding="utf-8")


def test_the_task_text_agrees_with_the_constants_of_the_grader():
    task = (HERE / "task.md").read_text(encoding="utf-8")
    assert f"at least {['zero', 'one', 'two', 'three'][m.MIN_EXAMPLES]} worked examples" in task
    assert "four to ten numbered steps" in task and (m.MIN_STEPS, m.MAX_STEPS) == (4, 10)
    assert "at least four" in task and m.MIN_CRITERIA == 4
    assert "keeping its ten sections" in task and len(m.SECTION_RULES) == 10
    assert "Decisions and open questions" in task and "second human reviewer" in task and "TODO" in task


# --------------------------------------------------------------------------------------------
# the numbers in the reference specs are the ones the Remit code really produces
# --------------------------------------------------------------------------------------------
NUMBERS_SCRIPT = r"""
import json
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from remit.corridors import get_corridor
from remit.fees import explain_fee
from remit.fx import fx_quote, StaticRateProvider
from remit.limits import to_local
from remit.money import Money

NOW = datetime(2026, 3, 2, 9, 0, tzinfo=timezone.utc)
out = {"t1": {}, "t2": {}, "t3": {}}

egp = get_corridor("QAR", "EGP")
for amount in ("100.00", "260.00", "1000.00", "15000.00"):
    for express in (False, True):
        fee = explain_fee(Money(amount, "QAR"), egp, express=express)
        disc = (fee.base.amount * Decimal("0.85")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        out["t1"][f"{amount}/{express}"] = [str(fee.base.amount), str(disc), str(fee.base.amount - disc), str(disc + fee.surcharge.amount),
                                           fee.minimum_applied, fee.cap_applied]
out["t1"]["pkr500"] = str(explain_fee(Money("500.00", "QAR"), get_corridor("QAR", "PKR")).total.amount)
out["t1"]["inr500"] = str(explain_fee(Money("500.00", "QAR"), get_corridor("QAR", "INR")).total.amount)

provider = StaticRateProvider()
for target, currency in (("11286.00", "INR"), ("11286.01", "INR"), ("10000.00", "INR"), ("1128.60", "INR"), ("1000.00", "INR"),
                         ("6501.00", "EGP")):
    corridor = get_corridor("QAR", currency)
    send = Decimal(0)
    start = max(1, int(Decimal(target) / Decimal("80") * 100) - 20)
    for cents in range(start, start + 100_000):
        send = (Decimal(cents) / 100).quantize(Decimal("0.01"))
        if fx_quote(Money(send, "QAR"), corridor, provider, NOW).receive.amount >= Decimal(target):
            break
    quote = fx_quote(Money(send, "QAR"), corridor, provider, NOW)
    fee = explain_fee(Money(send, "QAR"), corridor)
    inside = corridor.min_send.amount <= send <= corridor.max_send.amount
    out["t2"][f"{target}/{currency}"] = [str(send), str(quote.receive.amount), str(fee.total.amount), str(send + fee.total.amount), inside,
                                         fee.tier_index]
out["t2"]["rate"] = str(fx_quote(Money("500.00", "QAR"), get_corridor("QAR", "INR"), provider, NOW).rate)

for iso in ("2026-03-02T14:59:59+00:00", "2026-03-02T15:00:00+00:00", "2026-03-02T20:59:59+00:00", "2026-03-02T21:00:00+00:00"):
    local = to_local(datetime.fromisoformat(iso))
    out["t3"][iso] = [local.strftime("%H:%M:%S"), local.strftime("%A")]
print(json.dumps(out))
"""


@pytest.fixture(scope="module")
def numbers(template) -> dict:
    result = runner.run([sys.executable, "-c", NUMBERS_SCRIPT], cwd=template, env=runner.clean_env(pythonpath=[template / "src"]), timeout=60)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def table_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if line.startswith("|") and not re.fullmatch(r"\|[\s:|-]+\|?", line):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def plain(cell: str) -> str:
    return re.sub(r"\s*\(.*\)", "", cell).replace(",", "").strip()


def test_t1_numbers_agree_with_the_code(numbers):
    rows = [r for r in table_rows(section_of(REFERENCE["T1"], "Behaviour")) if re.fullmatch(r"[\d,]+\.\d\d", r[0])]
    assert len(rows) == 6
    for amount, express, base, discounted, saving, charged in rows:
        want = numbers["t1"][f"{plain(amount)}/{express == 'yes'}"]
        assert [plain(base), plain(discounted), plain(saving), plain(charged)] == [want[0], want[1], want[2], want[3]], amount
    assert "15.50" in REFERENCE["T1"] and numbers["t1"]["pkr500"] == "15.50" and numbers["t1"]["inr500"] == "12.00"
    assert numbers["t1"]["100.00/False"][4] is True and numbers["t1"]["15000.00/False"][5] is True  # "minimum applied", "cap applied"


def test_t2_numbers_agree_with_the_code(numbers):
    assert numbers["t2"]["rate"] == "22.5720"
    rows = [r for r in table_rows(section_of(REFERENCE["T2"], "Behaviour")) if r[0].endswith("INR")]
    assert len(rows) == 5
    for target, send, receives, fee, total, _note in rows:
        send_amount, got_receive, got_fee, got_total, inside, _tier = numbers["t2"][f"{plain(target.split()[0])}/INR"]
        if not inside:
            assert plain(send) == send_amount and receives == fee == total == "none"
        else:
            assert plain(send) == send_amount and plain(receives.split()[0]) == got_receive
            assert plain(fee) == got_fee and plain(total) == got_total
    assert numbers["t2"]["6501.00/EGP"][:3] == ["500.00", "6501.00", "15.50"]
    assert numbers["t2"]["11286.00/INR"][5] == 0 and numbers["t2"]["11286.01/INR"][5] == 1  # first and second fee tier


def test_t3_instants_agree_with_the_code(numbers):
    rows = [r for r in table_rows(section_of(REFERENCE["T3"], "Behaviour")) if r[0].startswith("2026-")]
    assert len(rows) == 6
    for sent, qatar, *_ in rows:
        clock, day = qatar.split(", ")
        got = numbers["t3"][sent.replace("Z", "+00:00")]
        assert got == [clock, day], sent


# --------------------------------------------------------------------------------------------
# the lab folder keeps the promises of its docstring
# --------------------------------------------------------------------------------------------
def test_the_lab_declares_what_the_lesson_says():
    lab = framework.load_lab("m03")
    assert (lab.id, lab.lesson, lab.needs_agent) == ("m03", "3.2", False)
    assert sorted(p.name for p in (lab.assets_dir / "tickets").iterdir()) == ["T1.md", "T2.md", "T3.md"]
    assert (lab.assets_dir / "hessa-notes.md").is_file()
    for ticket in m.TICKETS:  # the reference solution is a spec like any other: it starts with the ticket's id
        head = REFERENCE[ticket].splitlines()[0]
        assert head.startswith("# REMIT-34")
        assert head.split(":")[0].lstrip("# ") in (lab.assets_dir / "tickets" / f"{ticket}.md").read_text(encoding="utf-8")


# --------------------------------------------------------------------------------------------
# repairs after the learner dry-run
# --------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "line",
    ["A customer who sends 500 QAR to Egypt pays a fee of 13 QAR.", "The family should receive 10,000 INR.", "Sent at 6pm the note appears.",
     "Sent at 6:00 PM the note appears.", "Sent at 5:59 p.m. the note does not appear.", "On 2 March 2026 the offer starts.",
     "On March 2, 2026 the offer starts.", "Sent on 2026-03-02 the offer starts.", "| 500 | 13 | 513 |", "Sent at 18:00 exactly.",
     "The saving is 1.42 QAR.", "The fee is \u0661\u0662\u066b\u0665\u0660."],
)
def test_exact_amounts_times_and_dates_come_in_many_forms(line):
    assert m._EXAMPLE_TOKEN.search(line), line


@pytest.mark.parametrize("line", ["The customer pays less than before.", "A small transfer to Egypt.", "The 15% offer, version 3.", "In 2 cases the fee is lower."])
def test_prose_is_not_an_exact_example(line):
    assert not m._EXAMPLE_TOKEN.search(line), line


def test_whole_number_amounts_with_a_currency_and_clock_words_are_exact_examples(work):
    behaviour = """\
Corridor `QAR-EGP`, schedule `STD-B`. The discounted fee is the usual fee times 0.85, so a customer who sends 100 QAR pays less than the usual fee.

| Send | Usual fee | Fee charged |
|---|---|---|
| 100 QAR | 6 QAR | 5 QAR |
| 260 QAR | 9 QAR | 8 QAR |
| 15,000 QAR | 120 QAR | 102 QAR |
"""
    criteria = """\
- `quote_fee` for 100 QAR on `QAR-EGP` returns 5 QAR.
- `quote_fee` for 15,000 QAR on `QAR-EGP` returns 102 QAR.
- For 260 QAR the saving shown on the quote is 1 QAR.
- The existing Pakistan tests pass unedited, so 500 QAR to `QAR-PKR` is still 15 QAR.
"""
    t3_behaviour = """\
- Sent at 5:59pm Qatar time on a Monday, the usual text is sent.
- Sent at 6pm exactly, the pickup note is added; sent at 11:59pm it is added.
- Sent at 12:00am on the Tuesday, the usual text is sent again, and a bank deposit at 6pm gets the usual text.
"""
    write(work, reference_with(T1=lambda t: replace_section(replace_section(t, "Behaviour", behaviour), "Acceptance criteria", criteria),
                               T3=lambda t: replace_section(t, "Behaviour", t3_behaviour)))
    assert_only(spec_grade(work))


def test_behaviour_in_prose_without_any_amount_still_fails_and_says_which_forms_count(work):
    prose = "The customer pays a smaller fee than before on the quote screen and sees the saving. The confirmation mentions the saving."
    write(work, reference_with(T1=lambda t: replace_section(t, "Behaviour", prose)))
    detail = spec_grade(work)[N_EXAMPLES].detail
    assert "0 line(s)" in detail and "10,000 INR" in detail and "6pm" in detail


def test_criteria_without_any_exact_value_say_which_forms_count(work):
    criteria = "\n".join(f"- `quote_fee` returns the discounted fee for case number {word}." for word in ("one", "two", "three", "four"))
    write(work, reference_with(T1=lambda t: replace_section(t, "Acceptance criteria", criteria)))
    assert "6pm" in spec_grade(work)[N_CRITERIA].detail


def test_a_criterion_that_names_what_is_compared_in_plain_words_is_checkable():
    assert m.checkable("The customer is charged the fee that was on the quote.")
    assert m.checkable("The confirmation includes the saving in English and Arabic.")
    assert m.checkable("The fee debited on send is the same as the fee on the quote.")
    assert not m.checkable("The customer is happy with the result of the quote.")
    assert not m.checkable("The fee is shown correctly on the quote.")


def test_talking_about_todo_comments_is_not_a_placeholder_but_a_real_tbd_is(work):
    talk = "- No `TODO` comments are left in the code, and the word \"TBD\" never appears in a commit message.\n"
    write(work, reference_with(T1=lambda t: edit(t, "### Non-goals\n", "### Non-goals\n" + talk)))
    assert_only(spec_grade(work))
    write(work, reference_with(T1=lambda t: edit(t, "### Non-goals\n", "### Non-goals\n- The release date is TBD with Ops.\n")))
    assert_only(spec_grade(work), N_PLACEHOLDERS)


SOUP = "Rounding half up; boundary inclusive; QAR corridor EGP; fee minimum cap express; Qatar time UTC; Arabic digits."


def test_a_string_of_keywords_is_not_a_statement():
    assert m.keyword_line(SOUP, "item")
    assert m.keyword_line("express surcharge minimum discount round half up Decimal QAR-EGP only PKR STD-B", "para")
    for ticket in m.TICKETS:
        assert not any(m.resolution(ticket, one(ticket, f"# {ticket}\n\n## Decisions\n- {SOUP}\n- {SOUP}\n- {SOUP}\n")).values()), ticket
    # real statements, terse ones and table rows are never taken for keywords
    for text, kind in (("The express surcharge is not discounted.", "item"), ("Express surcharge: not discounted, 20.00 stays.", "item"),
                       ("Rounding is half up to 0.01, ties go up, Decimal only.", "item"), ("Express | not discounted | Hessa confirms", "row"),
                       ("\u0628\u0645\u0627 \u0623\u0646\u0643 \u0623\u0631\u0633\u0644\u062a \u0627\u0644\u062a\u062d\u0648\u064a\u0644 \u0628\u0639\u062f \u0627\u0644\u0633\u0627\u0639\u0629", "para")):
        assert not m.keyword_line(text, kind), text


def test_a_soup_line_among_real_decisions_does_not_hide_anything_and_resolves_nothing(work):
    write(work, reference_with(T1=lambda t: edit(t, "### Decisions and open questions\n", "### Decisions and open questions\n- " + SOUP + "\n")))
    assert_only(spec_grade(work))
    text = "# T1\n\n## Decisions\n- " + SOUP + "\n"
    assert sum(m.resolution("T1", one("T1", text)).values()) == 0


def test_an_untouched_template_is_not_previewed_as_a_list_of_open_questions(work):
    template = (work / "specs" / "TEMPLATE.md").read_text(encoding="utf-8")
    write(work, {"T1": REFERENCE["T1"], "T3": template}, log=None)
    check = spec_grade(work)[AMB["T3"]]
    assert not check.ok and check.detail == "specs/T3.md is still the blank template"
    text = (check.detail + " " + check.hint).lower()
    for word in ("time", "arabic", "boundar", "currency", "rounding", "fee parts", "of 6"):
        assert word not in text, word
    # a title and one line do not unlock the preview either; real content does
    sketch = template.replace("# TODO: ticket id and title", "# REMIT-343: cash pickup").replace(
        "TODO: what changes, for whom, and why, in two sentences.", "A note after the cut-off.")
    write(work, {"T3": sketch}, log=None)
    assert spec_grade(work)[AMB["T3"]].detail == "specs/T3.md is still the blank template"
    write(work, {"T3": sketch.replace("### Context\nTODO:", "### Context\n" + " ".join(["word"] * 45) + " TODO:")}, log=None)
    assert "of 6 resolved; still open:" in spec_grade(work)[AMB["T3"]].detail


def test_a_family_with_several_questions_shows_how_many_are_open():
    text = "# T2\n\n## Decisions\n" + "\n".join(f"- {RESOLVERS[('T2', amb)]}" for amb in ("currency", "direction", "tier")) + "\n"
    assert m.ambiguity_problems("T2", one("T2", text)) == (3, ["boundaries (1 of 2)"])
    assert m.ambiguity_problems("T2", one("T2", "# T2\n\n## Decisions\n- Nothing is decided here at all, for now.\n"))[1] == [
        "currency and corridors", "rounding", "boundaries (all 2)"]


def test_leaving_the_arabic_wording_to_the_native_reader_is_a_sound_t3(work):
    """Hessa's notes require a native reader's approval, so a spec may leave the sentence to them instead of writing it."""
    no_arabic = lambda t: "\n".join(ln for ln in t.splitlines() if not re.search("[\u0600-\u06ff]", ln))  # noqa: E731
    decisions = ("- Arabic wording: the Arabic sentence is supplied by the native Arabic reader on the team, who also approves it before release; "
                 "this spec does not fix it.\n- Arabic digits: any time inside the Arabic sentence uses Arabic-Indic digits through `localize_digits`, "
                 "and names and ids stay Latin and unchanged.\n")
    write(work, reference_with(T3=lambda t: edit(no_arabic(t), "### Risks\n", decisions + "\n### Risks\n")))
    result = spec_grade(work)
    assert result[AMB["T3"]].ok and result[AMB["T3"]].detail == "6 of 6 resolved", result[AMB["T3"]].detail
    assert_only(result)


def test_hessas_note_alone_does_not_decide_the_arabic_wording():
    note = "A native Arabic reader on the team must approve the Arabic sentence before it ships."
    assert not m.resolution("T3", one("T3", f"# T3\n\n## Decisions\n- {note}\n"))["ar-wording"]


@pytest.mark.parametrize(
    ("line", "label"),
    [
        ("The saving is held as a float, not as a string, and is rounded half even.", "float money"),
        ("The service calls `datetime.now()` and does not use the injected clock.", "a direct clock or id call"),
        ("In the ledger the offer is posted as a float amount and rounded half even.", "float money"),
        ("The fee is rounded down to the cent.", m.ROUND_DOWN),
        ("The receive amount is truncated to two decimals.", m.ROUND_DOWN),
        ("The derived send amount is rounded down to 0.01 QAR.", m.ROUND_DOWN),  # fine for T2, not for T1 (see below)
    ],
)
def test_house_rule_breaches_that_hide_behind_a_negation_elsewhere_in_the_sentence(work, line, label):
    write(work, reference_with(T1=lambda t: edit(t, "### Constraints\n", f"### Constraints\n- {line}\n")))
    result = spec_grade(work)
    assert_only(result, N_RULES)
    assert label in result[N_RULES].detail


@pytest.mark.parametrize(
    "line",
    [
        "Floats are banned: money is Decimal everywhere.",
        "`datetime.now()` is never used; the injected clock is.",
        "Time comes from the injected clock, never from datetime.now().",
        "Money is Decimal through Money; no floats.",
        "Rounding is half up, not half-even like the ledger.",
        "The send amount is rounded up to the next 0.01 QAR, so that the family gets at least the target.",
        "Should the fee be rounded down?",
        "We do not truncate or round down any money amount.",
        "The ledger's partner share is rounded half-even (Q-LED-1); that quirk is left alone.",
    ],
)
def test_sentences_that_forbid_or_ask_are_not_breaches(work, line):
    write(work, reference_with(T1=lambda t: edit(t, "### Constraints\n", f"### Constraints\n- {line}\n")))
    assert_only(spec_grade(work))


def test_t2_may_choose_to_round_the_derived_send_amount_down(work):
    line = "The derived send amount is rounded down to 0.01 QAR, so the family may get a little less."
    write(work, reference_with(T2=lambda t: edit(t, "### Constraints\n", f"### Constraints\n- {line}\n")))
    assert_only(spec_grade(work))


def test_an_unrelated_add_on_the_same_line_does_not_excuse_a_missing_file(work):
    line = "- Limits are checked in `src/remit/risk.py`, as `docs/ARCHITECTURE.md` says, and we add a check there.\n"
    write(work, reference_with(T1=lambda t: edit(t, "### Context\n", "### Context\n" + line)))
    result = spec_grade(work)
    assert_only(result, N_FILES)
    assert "src/remit/risk.py" in result[N_FILES].detail


@pytest.mark.parametrize(
    "line",
    [
        "- Add `tests/test_offer.py` with the failing tests.",
        "- In `src/remit/offers.py` (new) the rule lives.",
        "- Write the failing tests for all six Behaviour rows in `tests/test_offer.py`.",
        "- `src/remit/risk.py`, which `docs/ARCHITECTURE.md` still names, no longer exists.",
        "- The old docstring says see `KIT_NOTES.md`, which is not in this repository.",
        "- `docs/ARCHITECTURE.md` is stale: it names `src/remit/risk.py`.",
    ],
)
def test_new_or_gone_beside_the_path_still_counts(work, line):
    write(work, reference_with(T1=lambda t: edit(t, "### Context\n", f"### Context\n{line}\n")))
    assert_only(spec_grade(work))


def test_commit_hints_fit_what_the_learner_did(work):
    hint = full_grade(work)[N_COMMITS].hint
    assert "Commit your change" not in hint and "docs(specs)" in hint and "git add -A" in hint
    write(work, {"T1": REFERENCE["T1"]}, log=None)
    learner_commit(work, "wrote the first spec")
    write(work, reference_with(), log=LOG_OK)
    learner_commit(work, GOOD_MESSAGE)
    result = full_grade(work)
    assert_only(result, N_COMMITS)
    assert "git reset --soft lab-start" in result[N_COMMITS].hint and "newest" in result[N_COMMITS].hint
    # and that advice works
    runner.run(["git", "reset", "--soft", "lab-start"], cwd=work, env=runner.clean_env(), timeout=20)
    learner_commit(work, GOOD_MESSAGE)
    assert_only(full_grade(work))


def test_the_scope_hint_works_for_an_edit_that_is_already_committed(work):
    write(work, REFERENCE)
    framework.edit_file(work, "src/remit/fees.py", "SCHEDULES: dict[str, FeeSchedule]", "EGYPT_DISCOUNT = _D('0.15')\n\nSCHEDULES: dict[str, FeeSchedule]")
    learner_commit(work, "feat(fees): add the Egypt discount")
    result = full_grade(work)
    assert "--source=lab-start" in result[N_SCOPE].hint
    runner.run(["git", "restore", "--source=lab-start", "src/remit/fees.py"], cwd=work, env=runner.clean_env(), timeout=20)
    learner_commit(work, "fix(fees): undo the edit")
    assert_only(full_grade(work))


def test_the_task_documents_the_rules_the_grader_enforces():
    task = (HERE / "task.md").read_text(encoding="utf-8")
    for needle in ("10,000 INR", "6pm", "2026-03-02", "a question is not an answer", "write the Arabic sentence or say who supplies it",
                   "write \"second human reviewer\" and name who", "Nada", "any lower-case scope works", "plan the first slice",
                   "The failing test is written and run before the code it covers", "share one green commit", "ainative/ailab", "(advisory)",
                   "pull in different directions", "no copies", 'write "new" beside the file'):
        assert needle in task, needle
    assert "first slice" in (HERE / "templates" / "spec-template.md").read_text(encoding="utf-8")


LIFTED = [
    "Half up everywhere, except the ledger's partner share (half-even, an old quirk).",
    "Fee tier by the whole amount, upto inclusive; min_send, max_send and limits are inclusive; a quote expires at or after expires_at.",
    "Senders pay in QAR; BDT is a currency without a corridor; one fee schedule can price two corridors.",
    "Raw fee, then minimum and cap, then the express surcharge after the cap.",
    "Stored in UTC; a Qatar day runs 21:00 to 21:00 UTC, no daylight saving; the clock is injected.",
    "Arabic-Indic digits; names inserted unchanged; English wording pinned by tests.",
]


def test_sentences_lifted_from_the_lesson_do_not_stand_in_for_the_decisions(work):
    """The dry-run replaced each Decisions section by six lines of the lesson's table of what the code says (nothing about the
    ticket) and still got every question, because Behaviour and Context carried the same words. At least half of the answers
    must sit in Decisions now."""
    hollow = "\n".join(f"- {line}" for line in LIFTED)
    write(work, reference_with(**{t: (lambda text: replace_section(text, "Decisions and open questions", hollow)) for t in m.TICKETS}))
    result = spec_grade(work)
    for ticket in m.TICKETS:
        assert not result[AMB[ticket]].ok and "the Decisions section answers only" in result[AMB[ticket]].detail, ticket
    for ticket in m.TICKETS:  # the reference specs answer every question in Decisions
        answered, need = m.decisions_shortfall(ticket, one(ticket, REFERENCE[ticket]))
        assert answered == len(m.AMBIGUITIES[ticket]) >= need


def test_a_decisions_section_that_answers_nothing_fails_even_when_the_examples_state_the_rules(work):
    empty = "- Nothing else was decided here for now, see Behaviour.\n- Rounding is a detail for later.\n- Anything else is left for later too, as agreed."
    write(work, reference_with(T1=lambda t: replace_section(t, "Decisions and open questions", empty)))
    detail = spec_grade(work)[AMB["T1"]].detail
    assert detail.startswith("4 of 4 resolved, but the Decisions section answers only 0; at least 2 must sit there"), detail


def test_a_spec_may_keep_a_few_answers_outside_decisions(work):
    """The alternative T3 decides the zone and the boundary in Behaviour and the rest in Decisions: four of six is enough."""
    in_decisions, need = m.decisions_shortfall("T3", one("T3", ALT_T3))
    assert in_decisions >= need
    write(work, ALTERNATIVE)
    assert spec_grade(work)[AMB["T3"]].ok
