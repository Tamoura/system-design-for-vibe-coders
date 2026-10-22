"""Lab m01 (lesson 1.2): "Read three agent sessions, name the failure, then run your own".

The story
---------
Tariq collected three transcripts of coding-agent sessions on Remit for the AI-native clinic. They are
CONSTRUCTED for teaching (never recorded from a real model; each file says so), but every file, function,
command and test result in them is the real one in the repository, and their tool outputs were produced
by running the commands on a scratch copy. The learner reads them and fills ``diagnosis.json``: for every
failure, the failure-mode id (the ten ids of the field guide in lesson 1.1), the turn where it went wrong
and the cheapest prevention category. An optional second part (needs an agent) is a short read-only session
of their own, written up in ``session-notes.md`` and ``agent-log.md``.

What is seeded, and how it is graded
------------------------------------
``hidden/answers.json`` holds the truth: s1 shows ``hallucinated-api``, s2 shows ``runaway-loop`` and then
``test-gaming``, s3 shows ``injection``. The grader checks, per session, that the failure modes are the
seeded ones and that each turn is within one turn of the seeded turn (for a loop: anywhere in the stretch
in which the agent repeats itself, plus one turn either side). It cannot judge the quality of the thinking;
it checks the result. Two things make a lucky guess unlikely: a quotation copied word for word from the
session must back each finding, and the turn is checked as well as the name.

What is NOT graded strictly
---------------------------
The prevention category is a judgement call: the grader only validates it against the fixed list (a required
check) and, as an advisory check, compares it with the field guide's answer(s). Part 2 is advisory.

Files
-----
    seed(work)    writes three templates at the repository root (diagnosis.json, session-notes.md, agent-log.md);
                  the sessions arrive in lab-assets/sessions/ from assets/.
    grade(work)   pure Python: it reads the learner's files, never runs learner code.
    solve(work)   copies solution/ into place and commits.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from ailab import checks, framework, gitutil
from ailab.framework import Check, Lab

HERE = Path(__file__).resolve().parent

# The ten ids of the Failure-mode field guide (lesson 1.1) and the seven prevention categories.
FAILURE_MODES = (
    "hallucinated-api",
    "stale-knowledge",
    "misread-requirement",
    "symptom-fix",
    "sycophancy",
    "context-rot",
    "runaway-loop",
    "test-gaming",
    "injection",
    "scope-creep",
)
PREVENTION = ("context", "spec", "small-steps", "verify", "permissions", "fresh-start", "review")
SESSIONS = ("s1", "s2", "s3")

DIAGNOSIS = "diagnosis.json"
NOTES = "session-notes.md"
LOG = "agent-log.md"
ANSWER_FILES = (DIAGNOSIS, NOTES, LOG)

# Part 2: the headings the notes must have (matched case-insensitively as a part of the heading text).
NOTES_SECTIONS = (
    "Setup",
    "The prompt I gave",
    "What the agent read and ran",
    "What it got right",
    "Where it went wrong or I stopped it",
    "Field-guide ids I saw",
    "What I would change next time",
)

# --- the shape of diagnosis.json -----------------------------------------------------------------------
FINDING_SCHEMA = {
    "type": "object",
    "required": ["failure_mode", "turn", "prevention", "evidence"],
    "properties": {
        "failure_mode": {"type": "string", "enum": list(FAILURE_MODES)},
        "turn": {"type": "integer", "minimum": 1, "maximum": 99},
        "prevention": {"type": "string", "enum": list(PREVENTION)},
        "evidence": {"type": "string", "minLength": 8, "maxLength": 300},
    },
}
SESSION_SCHEMA = {
    "type": "object",
    "required": ["findings"],
    "properties": {"findings": {"type": "array", "minItems": 1, "maxItems": 2, "items": FINDING_SCHEMA}},
}
DIAGNOSIS_SCHEMA = {
    "type": "object",
    "required": ["sessions"],
    "properties": {
        "sessions": {"type": "object", "required": list(SESSIONS), "properties": {s: SESSION_SCHEMA for s in SESSIONS}}
    },
}

VALID_NAME = "diagnosis.json is valid"
WAITING = "waiting for a valid diagnosis.json"


# ---------------------------------------------------------------------------------------------------
# the seeded truth and the transcripts (always read from the kit, never from the learner's copy)
# ---------------------------------------------------------------------------------------------------
def load_truth() -> dict:
    return json.loads((HERE / "hidden" / "answers.json").read_text(encoding="utf-8"))


def session_text(session: str, truth: dict | None = None) -> str:
    truth = truth or load_truth()
    return (HERE / "assets" / "sessions" / truth["sessions"][session]["file"]).read_text(encoding="utf-8")


def parse_turns(text: str) -> dict[int, tuple[str, str]]:
    """{turn number: (kind, body)} from the ``## T08 · agent`` headings of a session file."""
    turns: dict[int, tuple[str, str]] = {}
    parts = re.split(r"(?m)^## T(\d+) · (\w+)\s*$", text)
    for number, kind, body in zip(parts[1::3], parts[2::3], parts[3::3]):
        turns[int(number)] = (kind, body)
    return turns


def normalise(text: str) -> str:
    """Compare quotations loosely: no backticks, straight quotes, one space between words, lower case."""
    text = text.replace("`", "").replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip().strip("\"' ").lower()


def _accepts_turn(finding: dict, turn: int, slack: int) -> bool:
    """The seeded turn, or the stretch ``earliest``..``latest`` when the failure spans turns (a loop), plus ``slack``."""
    low = finding.get("earliest", finding["turn"]) - slack
    high = finding.get("latest", finding["turn"]) + slack
    return low <= turn <= high


def _findings(data: dict, session: str) -> list[dict]:
    """The learner's findings for a session (assumes the file already passed the schema)."""
    return list(data["sessions"][session]["findings"])


# ---------------------------------------------------------------------------------------------------
# seed: the starting templates
# ---------------------------------------------------------------------------------------------------
# One finding per session to start with; add a second object to a "findings" list when a session shows two failures.
DIAGNOSIS_TEMPLATE_TEXT = """{
  "sessions": {
    "s1": { "findings": [ { "failure_mode": "", "turn": 0, "prevention": "", "evidence": "" } ] },
    "s2": { "findings": [ { "failure_mode": "", "turn": 0, "prevention": "", "evidence": "" } ] },
    "s3": { "findings": [ { "failure_mode": "", "turn": 0, "prevention": "", "evidence": "" } ] }
  }
}
"""
DIAGNOSIS_TEMPLATE = json.loads(DIAGNOSIS_TEMPLATE_TEXT)

NOTES_TEMPLATE = """# Session notes (part 2, optional)

Fill this in after your own short, read-only session on this repository. Replace each comment with your own
words. Keep it short: a few sentences under each heading is plenty.

## Setup

<!-- Which tool and model, which mode (for example plan mode), the date, and what was in the context at the start. -->

## The prompt I gave

<!-- Paste the prompt you sent, word for word. -->

## What the agent read and ran

<!-- The first five or so tool calls, in order: files read, searches, commands. -->

## What it got right

<!-- Claims you checked against the code and found true. -->

## Where it went wrong or I stopped it

<!-- Anything you corrected, doubted or interrupted. If nothing, say what you checked that makes you sure. -->

## Field-guide ids I saw

<!-- Failure-mode ids from lesson 1.1 that you saw, or "none seen". -->

## What I would change next time

<!-- One change to the prompt, the context or the way you supervised. -->
"""

LOG_TEMPLATE = """# Agent log

Entry:
Prompt (paste or summarise):
What the agent did:
What I corrected:
What I checked myself:
Minutes:
Would I delegate it again?
"""


def seed(work: Path) -> None:
    """Three templates at the root. The sessions are copied to lab-assets/sessions/ by the framework."""
    framework.write_file(work, DIAGNOSIS, DIAGNOSIS_TEMPLATE_TEXT)
    framework.write_file(work, NOTES, NOTES_TEMPLATE)
    framework.write_file(work, LOG, LOG_TEMPLATE)


# ---------------------------------------------------------------------------------------------------
# grade
# ---------------------------------------------------------------------------------------------------
def _session_checks(data: dict | None, truth: dict) -> list[Check]:
    """Two checks per session: the failure modes, then the turns."""
    slack = int(truth.get("tolerance", 1))
    out: list[Check] = []
    for session in SESSIONS:
        seeded = truth["sessions"][session]["findings"]
        mode_name = f"Session {session}: the failure mode"
        turn_name = f"Session {session}: the turn where it went wrong"
        if data is None:
            out.append(Check(mode_name, False, WAITING))
            out.append(Check(turn_name, False, WAITING))
            continue
        mine = _findings(data, session)
        seeded_modes = Counter(f["failure_mode"] for f in seeded)
        my_modes = Counter(f["failure_mode"] for f in mine)

        # 1. the set of failure modes
        if my_modes == seeded_modes:
            out.append(Check(mode_name, True, f"{len(mine)} finding(s) named"))
        else:
            right = sum((my_modes & seeded_modes).values())
            if right == 0:
                detail = "none of your findings matches what this session shows"
            elif len(mine) < len(seeded):
                detail = f"you named {len(mine)} failure(s) and this session shows more; one of yours matches"
            elif right < len(mine):
                detail = "one of your findings does not match what this session shows"
            else:
                detail = "your findings do not match what this session shows"
            out.append(Check(
                mode_name, False, detail,
                "Compare the symptom column of the field guide (lesson 1.1) with what happens in the session; "
                "a session can show a failure that leads to another.",
            ))

        # 2. the turns, for every seeded finding whose mode the learner named
        problems: list[str] = []
        unnamed = 0
        for finding in seeded:
            candidates = [m for m in mine if m["failure_mode"] == finding["failure_mode"]]
            if not candidates:
                unnamed += 1
                continue
            if not any(_accepts_turn(finding, m["turn"], slack) for m in candidates):
                problems.append(f"your turn for {finding['failure_mode']} ({candidates[0]['turn']}) is more than one turn away from where it shows")
        if unnamed == len(seeded):
            out.append(Check(turn_name, False, "no failure mode matched yet, so no turn can be checked",
                             "Name the failure first; then find the first turn where it shows."))
        elif problems or unnamed:
            detail = "; ".join(problems) if problems else "some failures are still unnamed, so their turns cannot be checked"
            out.append(Check(turn_name, False, detail,
                             "Re-read the turns around your answer. Not every tool result or user reply is where the failure happens; "
                             "look for the turn in which the agent does the wrong thing."))
        else:
            out.append(Check(turn_name, True, "all turns close enough"))
    return out


def _evidence_check(data: dict | None, truth: dict) -> Check:
    name = "Your evidence is quoted from the sessions"
    hint = "Copy the words exactly from the session file (backticks and line breaks do not matter), not a paraphrase."
    if data is None:
        return Check(name, False, WAITING)
    missing = []
    for session in SESSIONS:
        haystack = normalise(session_text(session, truth))
        for index, finding in enumerate(_findings(data, session), start=1):
            if normalise(finding["evidence"]) not in haystack:
                missing.append(f"{session} finding {index}")
    if missing:
        return Check(name, False, f"not found word for word: {', '.join(missing)}", hint)
    return Check(name, True)


def _prevention_check(data: dict | None, truth: dict) -> Check:
    name = "Your prevention choices agree with the field guide"
    hint = ("A different choice can be defensible. Compare with the Prevention column of the field guide, "
            "write your reason in the evidence or in your notes, and bring it to the group session.")
    if data is None:
        return Check(name, False, WAITING, required=False)
    differ = []
    for session in SESSIONS:
        mine = _findings(data, session)
        for finding in truth["sessions"][session]["findings"]:
            accepted = {finding["prevention"], *finding.get("also", [])}
            chosen = [m for m in mine if m["failure_mode"] == finding["failure_mode"]]
            if chosen and chosen[0]["prevention"] not in accepted:
                differ.append(session)
    if differ:
        return Check(name, False, f"differs in: {', '.join(sorted(set(differ)))}", hint, required=False)
    return Check(name, True, required=False)


def _words(text: str) -> Counter:
    text = re.sub(r"(?s)<!--.*?-->", " ", text)
    return Counter(re.findall(r"[\w'-]+", text.lower()))


def _notes_check(work: Path) -> Check:
    name = "Part 2: your session notes are filled in (optional)"
    path = work / NOTES
    hint = "Optional, needs an agent: fill every heading of session-notes.md, or ignore this line."
    if not path.is_file():
        return Check(name, False, f"{NOTES} does not exist", hint, required=False)
    sections = checks.markdown_sections(path)
    missing, thin = [], []
    for wanted in NOTES_SECTIONS:
        key = next((k for k in sections if wanted.lower() in k), None)
        if key is None:
            missing.append(wanted)
        elif sum(_words(sections[key]).values()) < 6:
            thin.append(wanted)
    if missing or thin:
        parts = ([f"missing: {', '.join(missing)}"] if missing else []) + ([f"too short: {', '.join(thin)}"] if thin else [])
        if len(missing) + len(thin) == len(NOTES_SECTIONS):
            parts = ["not started (this part is optional)"]
        return Check(name, False, "; ".join(parts), hint, required=False)
    seen = sections[next(k for k in sections if "field-guide ids" in k)].lower()
    if "none" not in seen and not any(mode in seen for mode in FAILURE_MODES):
        return Check(name, False, "the 'Field-guide ids I saw' section names no id and does not say 'none seen'", hint, required=False)
    return Check(name, True, required=False)


def _log_check(work: Path) -> Check:
    name = "Part 2: your agent log has an entry (optional)"
    hint = "Optional: add one entry in the lesson 0.1 format, or ignore this line."
    path = work / LOG
    if not path.is_file():
        return Check(name, False, f"{LOG} does not exist", hint, required=False)
    extra = _words(path.read_text(encoding="utf-8")) - _words(LOG_TEMPLATE)
    if sum(extra.values()) < 15:
        return Check(name, False, "the log has no entry yet", hint, required=False)
    return Check(name, True, required=False)


def _accept_turn_labels(data) -> None:
    """Be kind to the natural way of writing a turn: "T08" (or "8") means 8. Anything else is left for the schema to reject."""
    try:
        findings = [f for session in data["sessions"].values() for f in session["findings"]]
    except (KeyError, TypeError, AttributeError):
        return
    for finding in findings:
        if isinstance(finding, dict) and isinstance(finding.get("turn"), str):
            match = re.fullmatch(r"\s*[Tt]?(\d{1,2})\s*", finding["turn"])
            if match:
                finding["turn"] = int(match.group(1))


def _valid_check(work: Path) -> tuple[Check, dict | None]:
    """diagnosis.json exists, is JSON and has the right shape. Also returns the data when it is usable."""
    hint = "Each of s1, s2 and s3 needs 1 or 2 findings with all four fields (see the task)."
    data, error = checks.load_json(work / DIAGNOSIS)
    if error:
        return Check(VALID_NAME, False, error, hint), None
    _accept_turn_labels(data)
    problems = checks.validate(data, DIAGNOSIS_SCHEMA)
    if problems:
        first = re.sub(r"must be one of \[.*\]", "must be one of the ids in the task", problems[0])
        more = f" (and {len(problems) - 1} more)" if len(problems) > 1 else ""
        return Check(VALID_NAME, False, f"{len(problems)} field(s) still need a valid value; the first: {first}{more}", hint), None
    return Check(VALID_NAME, True), data


def grade(work: Path) -> list[Check]:
    truth = load_truth()
    results: list[Check] = []

    # 1. diagnosis.json: present, valid JSON, the right shape
    valid_check, usable = _valid_check(work)
    results.append(valid_check)

    # 2. the substance
    results.extend(_session_checks(usable, truth))
    results.append(_evidence_check(usable, truth))
    results.append(_prevention_check(usable, truth))

    # 3. part 2 (optional)
    results.append(_notes_check(work))
    results.append(_log_check(work))

    # 4. hygiene: the same habits as every lab
    results.append(checks.files_changed_within(
        work, list(ANSWER_FILES),
        name="Only your answer files changed", require_change=False,
        hint="Only diagnosis.json, session-notes.md and agent-log.md may change. The sessions and the code are read-only, "
             "and the live session was meant to propose a change, not apply it: undo the rest (git restore <file>, or delete the new file).",
    ))
    results.append(checks.commit_count(work, at_least=1, name="Your answers are committed"))
    results.append(checks.conventional_commits(work))
    results.append(checks.all_committed(work, name="Nothing is left uncommitted"))
    results.append(checks.no_secrets(work))
    return results


# ---------------------------------------------------------------------------------------------------
# solve: the reference answers (used by the kit's own tests; a peek for a stuck learner)
# ---------------------------------------------------------------------------------------------------
def solve(work: Path) -> None:
    for name in ANSWER_FILES:
        text = (HERE / "solution" / name).read_text(encoding="utf-8")
        framework.write_file(work, name, text)
    message = (HERE / "solution" / "commit_message.txt").read_text(encoding="utf-8").strip()
    gitutil.commit_all(work, message, author=("Najm Learner", "learner@najm.example"), date="2026-03-02T09:30:00+00:00")


LAB = Lab(
    id="m01",
    title="Read three agent sessions, name the failure, then run your own",
    lesson="1.2",
    needs_agent=False,  # the required part is reading; only the optional live session needs an agent
    seed=seed,
    grade=grade,
    solve=solve,
)
