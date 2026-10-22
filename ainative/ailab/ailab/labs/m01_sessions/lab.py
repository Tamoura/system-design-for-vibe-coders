"""Lab m01 (lesson 1.2): "Read three agent sessions, name the failure, then run your own".

The story
---------
Tariq collected three transcripts of coding-agent sessions on Remit for the AI-native clinic. They are
CONSTRUCTED for teaching (never recorded from a real model; each file says so). Apart from the invented partner
SDK in session 3 and the agents' own edits (which are not in the learner's copy), the files, functions and
commands in them are the real ones in the repository, and their tool outputs were produced by running the
commands on a scratch copy. The learner reads them and fills ``diagnosis.json``: for every
failure, the failure-mode id (the ten ids of the field guide in lesson 1.1), the turn where it went wrong
and the cheapest prevention category. An optional second part (needs an agent) is a short read-only session
of their own, written up in ``session-notes.md`` and ``agent-log.md``.

What is seeded, and how it is graded
------------------------------------
``hidden/answers.json`` holds the truth: s1 shows ``hallucinated-api``, s2 shows ``runaway-loop`` and then
``test-gaming``, s3 shows ``injection``. The grader checks, per session, that the failure modes are the
seeded ones and are listed in the order they happen, and that each turn is within one turn of the seeded turn
(for a loop: anywhere in the stretch from the first attempt that gets repeated to the last repeat, plus one
turn either side). It cannot judge the quality of the thinking; it checks the result. Two things make a lucky
guess unlikely: the turn is checked as well as the name, and the quotation has to be copied word for word from
a turn of the session at the turn the finding points at (or one turn either side, or anywhere in the seeded
stretch for a loop), not from the file header or from another part of the session.

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
from dataclasses import replace
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
WAITING = "fix diagnosis.json first"


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
    """Compare quotations loosely: no backticks, bold markers or ``>`` quote marks, straight quotes, one space
    between words, lower case. Both the session and the learner's quotation go through this, so a quotation
    copied from the raw file and one copied from a rendered page compare equal."""
    text = text.replace("`", "").replace("**", "").replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"(?m)^[ \t]*>[ \t]?", "", text)
    return re.sub(r"\s+", " ", text).strip().strip("\"' ").lower()


MIN_QUOTE = 8  # characters left after normalise() and after dropping a final full stop


def quote_key(text: str) -> str:
    """A learner's quotation as it is compared: normalised, without a trailing full stop or similar."""
    return normalise(text).rstrip(".,;:!? ").strip("\"' ")


def _window(finding: dict, slack: int) -> range:
    """The turns accepted for a seeded finding: its turn, or the stretch ``earliest``..``latest`` when the failure
    spans turns (a loop), plus ``slack`` on either side."""
    low = finding.get("earliest", finding["turn"]) - slack
    high = finding.get("latest", finding["turn"]) + slack
    return range(low, high + 1)


def _accepts_turn(finding: dict, turn: int, slack: int) -> bool:
    return turn in _window(finding, slack)


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
    """Two checks per session: the failure modes (and their order), then the turns."""
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

        # 1. the failure modes, listed in the order they happen
        order_hint = "Compare the symptom column of the field guide (lesson 1.1) with what happens in the session; a session can show a failure that leads to another."
        if my_modes == seeded_modes:
            if [m["failure_mode"] for m in mine] == [f["failure_mode"] for f in seeded]:
                out.append(Check(mode_name, True, f"{len(mine)} finding(s) named"))
            else:
                out.append(Check(
                    mode_name, False, "you named the right failures, but not in the order in which they happen in the session",
                    "List the findings in the order they happen: the first failure leads to the next.",
                ))
        else:
            right = sum((my_modes & seeded_modes).values())
            if right == len(mine) and len(mine) < len(seeded):
                detail = f"you named {len(mine)} failure(s) and this session shows more; one of yours matches"
            else:
                detail = "your findings do not match what this session shows"
            out.append(Check(mode_name, False, detail, order_hint))

        # 2. the turns, for every seeded finding whose mode the learner named
        problems: list[str] = []
        unnamed = 0
        for finding in seeded:
            candidates = [(i, m) for i, m in enumerate(mine, start=1) if m["failure_mode"] == finding["failure_mode"]]
            if not candidates:
                unnamed += 1
                continue
            if not any(_accepts_turn(finding, m["turn"], slack) for _, m in candidates):
                index, first = candidates[0]
                stretch = "earliest" in finding or "latest" in finding
                where = ("is not in the stretch where it shows, even with one turn either side" if stretch
                         else "is more than one turn away from where it shows")
                problems.append(f"your turn for finding {index} ({first['turn']}) {where}")
        if unnamed == len(seeded):
            out.append(Check(turn_name, False, "no failure mode matched yet, so no turn can be checked",
                             "Name the failure first; then find the first turn where it shows."))
        elif problems or unnamed:
            detail = "; ".join(problems) if problems else "some failures are still unnamed, so their turns cannot be checked"
            out.append(Check(turn_name, False, detail,
                             "Re-read the turns around your answer. Not every tool result or user reply is where the failure happens; "
                             "look for the turn in which the agent does the wrong thing. If it shows later than it began, point at where it began."))
        else:
            out.append(Check(turn_name, True, "all turns close enough"))
    return out


def _evidence_turns(finding: dict, seeded: list[dict], slack: int) -> set[int]:
    """The turns a quotation for this finding may come from: the turn it points at and the turns next to it, plus
    the whole accepted window of the seeded finding with the same failure mode (so a right quotation at a
    wrong turn costs one failed line, not two, and a loop may be quoted anywhere in its stretch)."""
    allowed = set(range(finding["turn"] - slack, finding["turn"] + slack + 1))
    for truth_finding in seeded:
        if truth_finding["failure_mode"] == finding["failure_mode"]:
            allowed |= set(_window(truth_finding, slack))
    return allowed


def _evidence_check(data: dict | None, truth: dict) -> Check:
    name = "Your evidence is quoted from the sessions"
    hint = ("Copy the words from the turn you point at, or the turn before or after it (for a loop, from anywhere in its stretch). "
            "Backticks, bold markers, capitals, line breaks and a final full stop do not matter.")
    if data is None:
        return Check(name, False, WAITING)
    slack = int(truth.get("tolerance", 1))
    absent, elsewhere, short = [], [], []
    for session in SESSIONS:
        turns = parse_turns(session_text(session, truth))
        bodies = {number: normalise(body) for number, (_kind, body) in turns.items()}
        seeded = truth["sessions"][session]["findings"]
        for index, finding in enumerate(_findings(data, session), start=1):
            label = f"{session} finding {index}"
            quote = quote_key(finding["evidence"])
            if len(quote) < MIN_QUOTE:
                short.append(label)
            elif not any(quote in body for body in bodies.values()):
                absent.append(label)
            elif not any(quote in bodies.get(number, "") for number in _evidence_turns(finding, seeded, slack)):
                elsewhere.append(label)
    if absent or elsewhere or short:
        parts = []
        if absent:
            parts.append(f"not found word for word in a turn: {', '.join(absent)}")
        if elsewhere:
            parts.append(f"found, but not at the turn you point at (or next to it): {', '.join(elsewhere)}")
        if short:
            parts.append(f"too short once markers and punctuation are ignored: {', '.join(short)}")
        return Check(name, False, "; ".join(parts), hint)
    return Check(name, True)


def _prevention_check(data: dict | None, truth: dict) -> Check:
    name = "Your prevention choices agree with the field guide"
    hint = ("A different choice can be defensible. Compare with the Prevention column of the field guide "
            "and bring your reason to the group session.")
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
    hint = "Optional: fill every heading of session-notes.md, or ignore this line."
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
            parts = ["not started"]
        return Check(name, False, "; ".join(parts), hint, required=False)
    seen = sections[next(k for k in sections if "field-guide ids" in k)].lower()
    if "none" not in seen and not any(mode in seen for mode in FAILURE_MODES):
        return Check(name, False, "the 'Field-guide ids I saw' section names no id and does not say 'none seen'", hint, required=False)
    return Check(name, True, required=False)


def _log_check(work: Path) -> Check:
    name = "Part 2: your agent log has an entry (optional)"
    hint = "Optional: add one entry (lesson 0.1 format), or ignore this line."
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


def _other_branches_with_commits(work: Path) -> list[str]:
    """Other local branches holding commits made since the start (the grader reads the checked-out branch only)."""
    here = gitutil.current_branch(work)
    found = []
    for branch in gitutil.branches(work):
        if branch == here:
            continue
        count = gitutil.git(work, "rev-list", "--count", f"{checks.LAB_START_TAG}..{branch}", check=False).stdout.strip()
        if count not in ("", "0"):
            found.append(branch)
    return found


def _branch_hint(work: Path) -> str:
    """A hint for 'no commits yet' that does not contradict a learner whose commits are on another branch."""
    others = _other_branches_with_commits(work)
    if not others:
        return ""
    return (f"The grader reads the branch that is checked out ({gitutil.current_branch(work)}), and your commits are on "
            f"{', '.join(others)}: switch to it (git switch {others[0]}) or merge it into this one.")


def _commit_count_check(work: Path) -> Check:
    check = checks.commit_count(work, at_least=1, name="Your answers are committed")
    return replace(check, hint=_branch_hint(work) or check.hint) if not check.ok else check


def _commit_message_check(work: Path) -> Check:
    """CONTRIBUTING.md's commit format, with a hint that is right when the bad message is not the last commit."""
    check = checks.conventional_commits(work)
    if not check.ok and check.hint.startswith("Open CONTRIBUTING.md"):
        check = replace(check, hint="Follow the commit format in CONTRIBUTING.md. Fix the last commit with git commit --amend; "
                                    "to rewrite all your commits as one, run git reset --soft lab-start and commit again.")
    elif not check.ok and "found 0 commit" in check.detail:
        check = replace(check, hint=_branch_hint(work) or check.hint)
    return check


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
             "and the live session was meant to propose a change, not apply it. Put each named file back as it was at the start "
             "(git restore --source=lab-start -- <file>; delete a file you added), then commit.",
    ))
    results.append(_commit_count_check(work))
    results.append(_commit_message_check(work))
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
