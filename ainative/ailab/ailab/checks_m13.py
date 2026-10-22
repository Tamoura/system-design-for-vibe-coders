"""Checks for lab m13 (lesson 13.2): a personal eval and a 90-day plan.

A helper written for this one lab and kept next to the shared ``checks.py`` (which a lab writer may not edit).

What it grades, in three groups:

1. ``eval_checks``  eval/tasks.jsonl: valid JSON Lines, enough well-formed tasks, and checks that really are checks.
   The kit RUNS them. It exports a clean copy of the repository at the ``lab-start`` tag, adds the learner's eval/,
   and asks four questions of each task:
     * does the check run at all (an allowed command, nothing missing, nothing hanging)?
     * does it FAIL on the untouched repository (a check that passes before any work proves nothing)?
     * does the guard (the "do not break anything" command) PASS there?
     * does a known-good reference solution make it PASS, and does a lazy placeholder answer NOT pass it?
   The running is done by ``assets/eval_runner.py``, the very file the learner is given, so ``baseline`` and
   ``verify`` in the learner's hands say what the grader will say. Tasks marked ``"repo": "own"`` come from the
   learner's own project; the kit cannot run those and says so.
2. ``plan_checks``  plan.md: required sections, a start date, a skills map, a realistic weekly routine, and goals
   that are measurable (a number, a baseline, a date inside the 90 days, a way to measure).
3. ``repo_checks``  only eval/ and plan.md changed, committed in steps, with CONTRIBUTING.md commit messages.

What it cannot tell: whether the tasks are the right tasks, whether a check measures what the prompt asks for
(only that it fails when nothing is done and passes on the reference), whether the plan is wise, or whether the
learner will follow it. It checks the artefacts, not the judgement behind them.
"""
from __future__ import annotations

import datetime
import importlib.util
import re
import sys
from pathlib import Path

from ailab import checks
from ailab.framework import Check

HERE = Path(__file__).resolve().parent / "labs" / "m13_personal_eval"
RUNNER_FILE = HERE / "assets" / "eval_runner.py"
EXAMPLES_FILE = HERE / "assets" / "tasks.example.jsonl"

TASKS_FILE = "eval/tasks.jsonl"
README_FILE = "eval/README.md"
RESULTS_FILE = "eval/results.jsonl"
PLAN_FILE = "plan.md"

MIN_TASKS = 8
MIN_REMIT_TASKS = 6
MIN_REFERENCES = 3
MIN_KINDS = 3
GRADER_TIMEOUT = 20.0  # seconds a single check may run while grading

# names (stable; the lesson and the tests use them)
N_JSONL = "eval/tasks.jsonl is valid JSON Lines"
N_COUNT = "At least eight tasks of your own"
N_FIELDS = "Every task is well formed"
N_KINDS = "Tasks cover three kinds of work"
N_RUNS = "Every check is allowed and runs"
N_FAILS = "Every check fails on the untouched repo"
N_GUARD = "Every guard passes on the untouched repo"
N_REFS = "Three references pass their checks"
N_PLACEHOLDER = "Checks reject a placeholder answer"
N_OFFLINE = "Checks stay offline"
N_CLOCK = "Checks do not read the clock"
N_GUARDED = "Code-changing tasks have a guard"
N_OWN = "One task comes from your own project"
N_README = "eval/README.md says how to run the eval"
N_RESULTS = "eval/results.jsonl is valid JSON Lines"
N_SECTIONS = "plan.md has the required sections"
N_START = "The plan has a start date"
N_SKILLS = "Skills map: six skills with a confidence and evidence"
N_ROUTINE = "The weekly routine is realistic"
N_GOALS = "Goals are measurable"
N_NO_AI = "The routine includes practice without the agent"
N_EVAL_GOAL = "A goal is tied to your eval"
N_SCOPE = "Only eval/ and plan.md changed"
N_STEPS = "The work is committed in steps"
N_COMMITS = "Commit messages follow CONTRIBUTING.md"
N_CLEAN = "Everything is committed"
N_SECRETS = "No secrets in the change"

CODE_KINDS = ("fix", "feature", "refactor", "test")
TEMPLATE_HINT = "Start from lab-assets/plan-template.md and keep its headings and table columns."
RUNNER_HINT = "Run `python lab-assets/eval_runner.py validate`, `baseline` and `verify` and read what they say."


# ----------------------------------------------------------------------------------------------
# the runner (a stdlib-only file the learner also has)
# ----------------------------------------------------------------------------------------------
_RUNNER = None


def runner():
    """The learner's ``eval_runner.py``, loaded from the kit's own copy (never from the learner's directory)."""
    global _RUNNER
    if _RUNNER is None:
        spec = importlib.util.spec_from_file_location("m13_eval_runner", RUNNER_FILE)
        module = importlib.util.module_from_spec(spec)
        sys.modules["m13_eval_runner"] = module  # dataclasses look the module up by name
        spec.loader.exec_module(module)
        _RUNNER = module
    return _RUNNER


def _short(items: list[str], limit: int = 3) -> str:
    shown = "; ".join(items[:limit])
    return shown + (f" (+{len(items) - limit} more)" if len(items) > limit else "")


def _words(text: str) -> int:
    return len(text.split())


def _waiting(name: str, what: str, hint: str, required: bool = True) -> Check:
    return Check(name, False, f"waiting for {what}", hint, required)


# ----------------------------------------------------------------------------------------------
# 1. the eval
# ----------------------------------------------------------------------------------------------
def _norm_prompt(text: object) -> str:
    return " ".join(str(text).lower().split())


def example_prompts() -> set[str]:
    tasks, _ = runner().load_tasks(EXAMPLES_FILE)
    return {_norm_prompt(t.get("prompt", "")) for t in tasks}


def eval_checks(work: Path) -> list[Check]:
    """All the checks about eval/ (the heavy ones run the learner's checks in throw-away copies)."""
    work = Path(work)
    R = runner()
    R.TIMEOUT = GRADER_TIMEOUT
    path = work / TASKS_FILE
    tasks, line_problems = R.load_tasks(path)
    out: list[Check] = []

    out.append(Check(N_JSONL, path.is_file() and not line_problems and bool(tasks),
                     _short(line_problems) if line_problems else ("" if tasks else "eval/tasks.jsonl does not exist"),
                     "One complete JSON object per line, no array, no pretty-printing, no code fences. "
                     "lab-assets/tasks.example.jsonl shows the shape."))

    examples = example_prompts()
    mine = [t for t in tasks if _norm_prompt(t.get("prompt", "")) not in examples]
    copied = len(tasks) - len(mine)

    # ids and the count
    seen: dict[str, int] = {}
    dupes: list[str] = []
    for task in mine:
        tid = task.get("id")
        if isinstance(tid, str):
            if tid in seen:
                dupes.append(f"id {tid} on lines {seen[tid]} and {task['_line']}")
            seen.setdefault(tid, task["_line"])
    if not tasks:
        out.append(_waiting(N_COUNT, "a valid eval/tasks.jsonl", "Create eval/tasks.jsonl first."))
    else:
        problems = []
        if len(mine) < MIN_TASKS:
            problems.append(f"{len(mine)} tasks of your own; the ticket asks for at least {MIN_TASKS}")
        if copied:
            problems.append(f"{copied} of the course's examples do not count")
        problems += dupes
        out.append(Check(N_COUNT, not problems, _short(problems) if problems else "",
                         "Write more tasks from work you really do, each with its own id. The examples are for the shape only."))

    # field problems
    if not tasks:
        out.append(_waiting(N_FIELDS, "a valid eval/tasks.jsonl", "Create eval/tasks.jsonl first."))
    else:
        field_problems = {id(t): R.task_problems(t, work, commands=False) for t in mine}
        bad = [f"{R.label(t)}: {_short(field_problems[id(t)], 2)}" for t in mine if field_problems[id(t)]]
        out.append(Check(N_FIELDS, not bad and bool(mine), _short(bad) if bad else ("" if mine else "no tasks of your own yet"),
                         "Each task needs id, title, kind, prompt (at least 15 words) and check.run; setup and reference are "
                         "optional .patch files under eval/. " + RUNNER_HINT))

    valid = [t for t in mine if not field_problems.get(id(t))] if tasks else []
    ids_ok: list[dict] = []
    used: set[str] = set()
    for task in valid:  # a repeated id counts once
        if task["id"] not in used:
            used.add(task["id"])
            ids_ok.append(task)
    kinds = {t["kind"] for t in ids_ok}
    if not ids_ok:
        out.append(_waiting(N_KINDS, "valid tasks", "Write the tasks first.", required=False))
    else:
        out.append(Check(N_KINDS, len(kinds) >= MIN_KINDS, f"kinds used: {', '.join(sorted(kinds))}",
                         "Real work is a mix. Add a fix, a feature, a question, a review or a refactor from your own week.",
                         required=False))

    remit = [t for t in ids_ok if t.get("repo", "remit") == "remit"]
    own = [t for t in ids_ok if t.get("repo", "remit") == "own"]

    # commands: allowed?
    command_problems: list[str] = []
    runnable: list[dict] = []
    for task in remit:
        bad_cmd = []
        for name in ("run", "guard"):
            if isinstance(task["check"].get(name), str):
                argv, why = R.parse_command(task["check"][name])
                if argv is None:
                    bad_cmd.append(f"check.{name}: {why}")
        if bad_cmd:
            command_problems.append(f"{R.label(task)}: {_short(bad_cmd, 1)}")
        else:
            runnable.append(task)

    reports: list = []
    if runnable:
        reports = R.evaluate_all(work, "lab-start", runnable)
    by_id = {r.task_id: r for r in reports}

    if not ids_ok:
        for name, req in ((N_RUNS, True), (N_FAILS, True), (N_GUARD, True), (N_REFS, True), (N_PLACEHOLDER, True)):
            out.append(_waiting(name, "valid tasks", RUNNER_HINT, req))

    if ids_ok:
        # --- runs
        broken: list[str] = list(command_problems)
        for task in runnable:
            r = by_id[task["id"]]
            if r.error:
                broken.append(f"{R.label(task)}: {r.error}")
                continue
            for outcome, what in ((r.baseline, "the check"), (r.guard_baseline, "the guard"),
                                  (r.reference, "the check after the reference"), (r.guard_reference, "the guard after the reference")):
                if outcome is not None and outcome.verdict == "broken":
                    broken.append(f"{R.label(task)}: {what} cannot run ({outcome.detail})")
                    break
        enough = len(remit) >= MIN_REMIT_TASKS
        detail = _short(broken) if broken else ""
        if not broken and not enough:
            detail = f"{len(remit)} tasks on the Remit repository run; at least {MIN_REMIT_TASKS} of your tasks must be about it (the kit cannot run the others)"
        out.append(Check(N_RUNS, not broken and enough, detail,
                         "Allowed commands: pytest, python, grep and read-only git, with paths relative to the repo root and no shell "
                         "operators. " + RUNNER_HINT))

        # --- fails on the untouched repo
        vacuous = [R.label(t) for t in runnable if (by_id[t["id"]].baseline is not None and by_id[t["id"]].baseline.passed)]
        out.append(Check(N_FAILS, not vacuous and bool(runnable),
                         ("these checks already pass before any work is done: " + _short(vacuous)) if vacuous
                         else ("" if runnable else "no runnable checks yet"),
                         "A check that passes on the untouched repository proves nothing. Make it test the change the prompt asks for."))

        # --- guards
        guards_bad = [R.label(t) for t in runnable
                      if by_id[t["id"]].guard_baseline is not None and by_id[t["id"]].guard_baseline.verdict == "fail"]
        out.append(Check(N_GUARD, not guards_bad, ("these guards fail on the untouched repo: " + _short(guards_bad)) if guards_bad else "",
                         "A guard must pass before the work and after a correct solution. Guard the neighbours, "
                         "not the tests the planted bug already breaks."))

        # --- references
        good, wrong = 0, []
        for task in runnable:
            r = by_id[task["id"]]
            if not task.get("reference") or r.error or r.reference is None:
                continue
            if r.reference.passed and (r.guard_reference is None or r.guard_reference.passed):
                good += 1
            elif r.reference.verdict == "fail":
                wrong.append(f"{R.label(task)}: the check still fails after the reference ({r.reference.detail or 'no detail'})")
            elif r.guard_reference is not None and r.guard_reference.verdict == "fail":
                wrong.append(f"{R.label(task)}: the guard fails after the reference")
        problems = list(wrong)
        if good < MIN_REFERENCES:
            problems.append(f"{good} {'reference passes its check' if good == 1 else 'references pass their checks'}; "
                            f"at least {MIN_REFERENCES} are needed")
        out.append(Check(N_REFS, not problems, _short(problems) if problems else "",
                         "Do the task yourself once in a scratch copy, save `git diff` as eval/reference/<id>.patch, and make sure "
                         "your check passes on it. A check you have never seen pass cannot be trusted."))

        # --- placeholders
        weak = []
        for task in runnable:
            for file_name, outcome in by_id[task["id"]].placeholders:
                if outcome.passed:
                    weak.append(f"{R.label(task)}: a placeholder in {file_name}")
        out.append(Check(N_PLACEHOLDER, not weak, ("the check accepts a lazy answer: " + _short(weak)) if weak else "",
                         "Check what the answer says or what the tests catch, not that a file exists. A test that asserts nothing "
                         "must fail your check."))

    # --- static lint (needs only the files)
    if ids_ok:
        findings = R.lint(work, ids_ok)
        out.append(Check(N_OFFLINE, not findings["network"],
                         ("network use in: " + _short(findings["network"])) if findings["network"] else "",
                         "A check that needs the internet is flaky and slow. Keep checks offline and deterministic."))
        out.append(Check(N_CLOCK, not findings["clock"],
                         ("clock or sleep in: " + _short(findings["clock"])) if findings["clock"] else "",
                         "Inject or fix the time; a check that depends on today's date changes its answer by itself.", required=False))
    else:
        out.append(_waiting(N_OFFLINE, "valid tasks", "Write the tasks first."))
        out.append(_waiting(N_CLOCK, "valid tasks", "Write the tasks first.", required=False))

    # --- advisory
    code_tasks = [t for t in remit if t["kind"] in CODE_KINDS]
    if code_tasks:
        guarded = [t for t in code_tasks if isinstance(t["check"].get("guard"), str)]
        out.append(Check(N_GUARDED, len(guarded) * 2 >= len(code_tasks), f"{len(guarded)} of {len(code_tasks)} have a guard",
                         "Add check.guard (for example `pytest -q`) so a tool that fixes the task and breaks something else fails.",
                         required=False))
    else:
        out.append(Check(N_GUARDED, False, "no code-changing tasks yet", "Add a fix, feature, test or refactor task.", required=False))
    out.append(Check(N_OWN, bool(own), "" if own else "every task is on the Remit repository",
                     'The best eval uses your real work. Add one task with "repo": "own"; the kit cannot run it, you can.',
                     required=False))

    readme = work / README_FILE
    readme_words = _words(readme.read_text(encoding="utf-8")) if readme.is_file() else 0
    out.append(Check(N_README, readme_words >= 60, "" if readme_words >= 60 else
                     ("eval/README.md does not exist" if not readme.is_file() else f"{readme_words} words; write at least 60"),
                     "Say how to run the eval, what counts as a pass, how many repeats you run and when you run it again.",
                     required=False))

    results = work / RESULTS_FILE
    if results.is_file():
        rows, row_problems = R.load_tasks(results)
        lacking = [f"line {r['_line']}" for r in rows if not {"task", "tool", "passed"} <= set(r)]
        problems = row_problems + ([f"missing task, tool or passed on {_short(lacking)}"] if lacking else [])
        out.append(Check(N_RESULTS, not problems, _short(problems) if problems else "",
                         "Use `eval_runner.py score` to append results; it writes valid lines.", required=False))
    else:
        out.append(Check(N_RESULTS, True, "no results yet (optional)", "", required=False))
    return out


# ----------------------------------------------------------------------------------------------
# 2. the plan
# ----------------------------------------------------------------------------------------------
SECTION_PATTERNS: dict[str, tuple[str, int]] = {
    "Where I am": (r"where i am|starting point|skills map", 20),
    "Weekly routine": (r"weekly|routine|each week|every week", 15),
    "Goals": (r"\bgoals?\b", 20),
    "Days 1-30": (r"days?\s*1\s*(?:-|–|—|to)\s*30|first 30|month 1\b", 12),
    "Days 31-60": (r"days?\s*31\s*(?:-|–|—|to)\s*60|second 30|month 2\b", 12),
    "Days 61-90": (r"days?\s*61\s*(?:-|–|—|to)\s*90|last 30|third 30|month 3\b", 12),
    "Eval cadence": (r"cadence|re-?run|when i run", 20),
    "What I will ignore": (r"ignore|not doing|stop doing|noise", 10),
}


def _find_section(outline, pattern: str):
    for section in outline:
        title = checks._norm(section.title)
        if re.search(pattern, title) and section.level >= 2:
            return section
    return None


def parse_table(body: str) -> tuple[list[str], list[list[str]]] | None:
    """The first Markdown table in ``body``: (header cells, data rows). Empty rows are dropped."""
    lines = [line.strip() for line in body.splitlines()]
    start = next((i for i, line in enumerate(lines) if line.startswith("|")), None)
    if start is None:
        return None
    block: list[str] = []
    for line in lines[start:]:
        if not line.startswith("|"):
            break
        block.append(line)
    if len(block) < 2:
        return None

    def cells(line: str) -> list[str]:
        inner = line.replace("\\|", "\u0000").strip().strip("|")
        return [c.replace("\u0000", "|").replace("**", "").replace("`", "").strip() for c in inner.split("|")]

    headers = [c.lower() for c in cells(block[0])]
    rows = []
    for line in block[1:]:
        row = cells(line)
        if all(re.fullmatch(r":?-{2,}:?", c) or not c for c in row) and any(c for c in row):
            continue  # the separator row
        if not any(row):
            continue
        row = (row + [""] * len(headers))[: max(len(headers), len(row))]
        rows.append(row)
    return headers, rows


def _column(headers: list[str], *keys: str) -> int | None:
    for index, header in enumerate(headers):
        tokens = re.findall(r"[a-z]+", header)
        if any(token.startswith(key) for token in tokens for key in keys):
            return index
    return None


def _start_date(text: str) -> tuple[datetime.date | None, str]:
    match = re.search(r"^\W*start date\W*:\W*(\d{4}-\d{2}-\d{2})\b", text, flags=re.I | re.M)
    if not match:
        return None, "no line `Start date: YYYY-MM-DD`"
    try:
        return datetime.date.fromisoformat(match.group(1)), ""
    except ValueError:
        return None, f"{match.group(1)} is not a real date"


def plan_checks(work: Path) -> list[Check]:
    work = Path(work)
    path = work / PLAN_FILE
    names = [(N_SECTIONS, True), (N_START, True), (N_SKILLS, True), (N_ROUTINE, True), (N_GOALS, True), (N_NO_AI, False), (N_EVAL_GOAL, False)]
    if not path.is_file():
        return [_waiting(name, "plan.md", TEMPLATE_HINT, req) for name, req in names]

    text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)  # guidance comments in the template do not count
    outline = checks.markdown_outline(text)
    out: list[Check] = []

    # sections
    found: dict[str, object] = {}
    missing, thin = [], []
    for title, (pattern, minimum) in SECTION_PATTERNS.items():
        section = _find_section(outline, pattern)
        if section is None:
            missing.append(title)
        else:
            found[title] = section
            if _words(section.body) < minimum:
                thin.append(title)
    problems = ([f"missing: {_short(missing, 4)}"] if missing else []) + ([f"too short: {_short(thin, 4)}"] if thin else [])
    out.append(Check(N_SECTIONS, not problems, "; ".join(problems), TEMPLATE_HINT))

    # start date
    start, why = _start_date(text)
    out.append(Check(N_START, start is not None, why, "Write `Start date: 2026-11-02` (a real date, year-month-day) under the title."))

    # skills map
    out.append(_skills_check(found.get("Where I am")))
    # routine
    routine_rows = _routine_rows(found.get("Weekly routine"))
    out.append(_routine_check(found.get("Weekly routine"), routine_rows))
    # goals
    goals_table = parse_table(found["Goals"].body) if "Goals" in found else None
    out.append(_goals_check(found.get("Goals"), goals_table, start))

    # advisory
    no_ai = re.compile(r"without (the |an? )?(ai|agent|assistant|tool|copilot|chatbot)|no[- ]ai|no agent|by hand|unaided|"
                       r"from memory|on paper|offline", re.I)
    practices = " ".join(row[0] for row in routine_rows[1]) if routine_rows else ""
    out.append(Check(N_NO_AI, bool(no_ai.search(practices)), "" if no_ai.search(practices) else "every practice in the routine uses the agent",
                     "Keep one weekly practice where you work without the agent: a kata, reading code, explaining a change from memory.",
                     required=False))
    goal_text = " ".join(" ".join(row) for row in goals_table[1]) if goals_table else ""
    has_eval = re.search(r"\beval\b|tasks\.jsonl|results\.jsonl|pass rate", goal_text, re.I)
    out.append(Check(N_EVAL_GOAL, bool(has_eval), "" if has_eval else "no goal mentions your eval",
                     "Tie one goal to the eval you built: runs completed, a pass rate, a decision it informed.", required=False))
    return out


def _skills_check(section) -> Check:
    hint = "Use the six rows of the template: skill, when you last did it without AI, a confidence from 1 to 5, and the evidence."
    if section is None:
        return _waiting(N_SKILLS, "a 'Where I am' section", hint)
    table = parse_table(section.body)
    if table is None:
        return Check(N_SKILLS, False, "no table in 'Where I am'", hint)
    headers, rows = table
    conf, evid = _column(headers, "confidence", "rating", "score", "level"), _column(headers, "evidence", "because", "why", "example")
    if conf is None or evid is None:
        return Check(N_SKILLS, False, "the table needs a confidence column and an evidence column", hint)
    problems = []
    if len(rows) < 6:
        problems.append(f"{len(rows)} skills; at least 6")
    for row in rows:
        name = row[0] or "(unnamed)"
        if not re.search(r"\b[1-5]\b", row[conf]):
            problems.append(f"{name}: confidence is not a number from 1 to 5")
        elif _words(row[evid]) < 3:
            problems.append(f"{name}: evidence needs at least 3 words")
    return Check(N_SKILLS, not problems, _short(problems) if problems else "", hint)


def _routine_rows(section) -> tuple[list[str], list[list[str]]] | None:
    if section is None:
        return None
    table = parse_table(section.body)
    if table is None:
        return None
    headers, rows = table
    practice, minutes = _column(headers, "practice", "activity", "what", "task"), _column(headers, "minute", "min", "duration", "time")
    if practice is None or minutes is None:
        return None
    return headers, [[row[practice], row[minutes]] for row in rows]


def _routine_check(section, parsed) -> Check:
    hint = "A table with a Practice column and a Minutes column: at least three practices, 5 to 240 minutes each, 60 to 600 a week."
    if section is None:
        return _waiting(N_ROUTINE, "a 'Weekly routine' section", hint)
    if parsed is None:
        return Check(N_ROUTINE, False, "no table with a Practice column and a Minutes column", hint)
    problems, total = [], 0
    rows = parsed[1]
    if len(rows) < 3:
        problems.append(f"{len(rows)} practices; at least 3")
    for practice, minutes in rows:
        number = re.search(r"\d+", minutes)
        if not number:
            problems.append(f"'{practice[:30]}': minutes is not a number")
            continue
        value = int(number.group())
        total += value
        if not 5 <= value <= 240:
            problems.append(f"'{practice[:30]}': {value} minutes is outside 5 to 240")
        if _words(practice) < 3:
            problems.append(f"'{practice[:30]}': say what you will do, in at least 3 words")
    if rows and not problems and not 60 <= total <= 600:
        problems.append(f"{total} minutes a week; between 60 and 600 is realistic for a part-time plan")
    return Check(N_ROUTINE, not problems, _short(problems) if problems else f"{total} minutes a week", hint)


def _goals_check(section, table, start: datetime.date | None) -> Check:
    hint = ("One row per goal with Goal, Metric, Baseline, Target (with a number), By (YYYY-MM-DD, inside your 90 days) and "
            "How I will measure it. Three to six goals.")
    if section is None:
        return _waiting(N_GOALS, "a 'Goals' section", hint)
    if table is None:
        return Check(N_GOALS, False, "no table under Goals", hint)
    headers, rows = table
    cols = {
        "goal": _column(headers, "goal"), "metric": _column(headers, "metric"), "baseline": _column(headers, "baseline", "today", "now"),
        "target": _column(headers, "target"), "by": _column(headers, "by", "date", "deadline", "due"),
        "how": _column(headers, "how", "evidence", "measure"),
    }
    lacking = [name for name, index in cols.items() if index is None]
    if lacking:
        return Check(N_GOALS, False, "the table has no column for: " + ", ".join(lacking), hint)
    problems = []
    if not 3 <= len(rows) <= 6:
        problems.append(f"{len(rows)} goals; between 3 and 6 keeps a plan honest")
    for number, row in enumerate(rows, 1):
        tag = f"goal {number}"
        if _words(row[cols["goal"]]) < 4:
            problems.append(f"{tag}: say the goal in at least 4 words")
        if _words(row[cols["metric"]]) < 2:
            problems.append(f"{tag}: name the metric (at least 2 words)")
        if not row[cols["baseline"]].strip():
            problems.append(f"{tag}: write today's baseline, even if it is 'none yet'")
        if not re.search(r"\d", row[cols["target"]]):
            problems.append(f"{tag}: the target has no number")
        if _words(row[cols["how"]]) < 3:
            problems.append(f"{tag}: say how you will measure it (at least 3 words)")
        when = row[cols["by"]].strip()
        try:
            date = datetime.date.fromisoformat(when)
        except ValueError:
            problems.append(f"{tag}: '{when[:20]}' is not a YYYY-MM-DD date")
            continue
        if start is None:
            problems.append(f"{tag}: add a valid Start date first so the date can be checked")
        elif not start <= date <= start + datetime.timedelta(days=90):
            problems.append(f"{tag}: {when} is outside the 90 days from {start.isoformat()}")
    return Check(N_GOALS, not problems, _short(problems, 4) if problems else f"{len(rows)} goals", hint)


# ----------------------------------------------------------------------------------------------
# 3. the repository
# ----------------------------------------------------------------------------------------------
def repo_checks(work: Path) -> list[Check]:
    return [
        checks.files_changed_within(work, ["eval/**", "plan.md"], name=N_SCOPE,
                                    hint="This ticket adds files only under eval/ and plan.md. Move or revert anything else "
                                         "(lab-assets/ and the Remit code stay as they are)."),
        checks.commit_count(work, at_least=2, name=N_STEPS,
                            hint="Commit the eval and the plan separately, for example `test(eval): ...` then `docs(plan): ...`."),
        checks.conventional_commits(work, name=N_COMMITS),
        checks.all_committed(work, name=N_CLEAN),
        checks.no_secrets(work, name=N_SECRETS),
    ]


def grade(work: Path) -> list[Check]:
    return eval_checks(work) + plan_checks(work) + repo_checks(work)
