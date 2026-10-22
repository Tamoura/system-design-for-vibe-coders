"""Grader helpers for lab m06 (lesson 6.2, "Onboard to the codebase and fix a production bug from its logs").

These helpers live next to the lab rather than in ``checks.py`` (which the lab authors must not edit). They
are used only by ``ailab/labs/m06_onboard_debug/lab.py`` and are tested in ``tests/test_labs_m06.py``.

What is in here
---------------
* ``collect_repo_facts``  what really exists in the learner's repository (files, defined names), by AST, so a
  document can be checked against the code without importing anything.
* ``onboarding_checks``   checks ``docs/onboarding.md`` structurally and against the facts of the repository:
  every file it names exists, the transfer steps are in the order the code runs them, it does not call
  functions or name technologies that are not in the repository, and it does not repeat the stale claims
  in ``docs/ARCHITECTURE.md``.
* ``root_cause_checks``   checks ``docs/root-cause.md``: its sections, that it names the cause, and (advisory)
  that it covers both windows, points at the learner's own test and lists who was affected.
* ``tests_not_weakened``  no existing test was removed or changed (AST comparison, so import edits are fine).
* ``fix_is_small``        the fix is a handful of lines in ``src/remit/limits.py``.
* ``variant_check``       runs the learner's new tests against the starter's ``limits.py`` with one of the two
  seeded defects removed, to see which defect the tests really catch.
* ``one_concern_per_commit`` and ``agent_log_check``  small advisory hygiene checks.

Everything is read-only with respect to the learner's directory, runs learner code only in a subprocess (through
``checks.run_pytest``) and is deterministic.
"""
from __future__ import annotations

import ast
import builtins
import re
from dataclasses import dataclass, field
from pathlib import Path

from ailab import checks, gitutil
from ailab.framework import LAB_START_TAG, Check

LIMITS_FILE = "src/remit/limits.py"
ONBOARDING = "docs/onboarding.md"
ROOT_CAUSE = "docs/root-cause.md"
AGENT_LOG = "docs/agent-log.md"

# The seeded defect: the two window helpers convert "now" to UTC instead of Qatar time.
GOOD_CONVERSION = "    local = to_local(now)\n"
BAD_CONVERSION = "    local = now.astimezone(timezone.utc)\n"

ONBOARDING_SECTIONS = ("What Remit is", "Entry points", "Data flow", "Tests", "Risks and gaps", "Open questions")
ROOT_CAUSE_SECTIONS = ("Symptom", "Reproduction", "Root cause", "Why it was missed", "Fix", "Prevention")
ONBOARDING_WORDS = (250, 1500)

_SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "node_modules", ".mypy_cache"}

# A line (or the line after it) that says a document is wrong, or that something is missing, is not a false claim.
_DOUBT = re.compile(
    r"(?i)\b(stale|outdated|out[- ]of[- ]date|no longer|does ?n[o']t exist|do not exist|doesn’t exist|not exist|"
    r"nonexistent|non-existent|missing|absent|there is no|there are no|no such|not a real|wrong|incorrect|"
    r"inaccurate|mismatch|disagrees?|contradicts?|drift\w*|dangling|misleading|untrue|false|obsolete|"
    r"never existed|was removed|were removed|has been removed|is gone|are gone)\b"
)
# A statement that a DOCUMENT is wrong (used for the stale claims: "there is no monthly limit" is itself the stale claim).
_DOCS_WRONG = re.compile(
    r"(?i)\b(stale|outdated|out[- ]of[- ]date|no longer (?:true|correct|accurate|valid|applies)|wrong|incorrect|inaccurate|"
    r"mismatch\w*|disagrees?|contradicts?|drift\w*|misleading|untrue|not true|false|obsolete|superseded)\b"
)
_NEGATION = re.compile(r"(?i)\b(no|not|never|without|none|neither|nor|n't)\b|n’t")

_TECHNOLOGIES = (
    "FastAPI", "Flask", "Django", "SQLAlchemy", "PostgreSQL", "Postgres", "MySQL", "Kafka", "Redis", "Celery",
    "RabbitMQ", "MongoDB", "Stripe", "Twilio", "Kubernetes", "GraphQL", "gRPC",
)
_TECH_RE = re.compile(r"\b(" + "|".join(_TECHNOLOGIES) + r")\b", re.I)

_STALE_CLAIMS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("a T1 daily limit of 5,000", re.compile(r"\bT1\b.*\b5[,.]?000\b")),
    ("a T2 daily limit of 25,000", re.compile(r"\bT2\b.*\b25[,.]?000\b")),
    ("no monthly limit", re.compile(r"(?i)\bno monthly (?:limit|cap|ceiling)s?\b")),
    ("only two KYC tiers", re.compile(r"(?i)\btwo\s+kyc\s+tiers\b|\bkyc\b[^\n]{0,30}\bonly two\b")),
)
_STALE_CLAIM_EXEMPT = re.compile(r"(?i)corridor|max_send|min_send|QAR-[A-Z]{3}")

_PATH_TOKEN = re.compile(r"(?<![\w/.-])((?:[\w.-]+/)*[\w.-]+\.(?:py|md|toml|ya?ml|json|txt|cfg|ini))(?![\w-])")
_INLINE_CODE = re.compile(r"`([^`\n]+)`")
_CALL = re.compile(r"^((?:[A-Za-z_]\w*\.)*[A-Za-z_]\w*)\s*\(.*\)$")

# The steps of RemitService.send, in the order the code runs them (service.py), as patterns.
FLOW = (
    ("validate", re.compile(r"(?i)validat")),
    ("limits", re.compile(r"(?i)limit")),
    ("screening", re.compile(r"(?i)screen")),
    ("fee", re.compile(r"(?i)\bfees?\b")),
    ("fx", re.compile(r"(?i)\bfx\b|exchange|\brates?\b")),
    ("ledger", re.compile(r"(?i)ledger")),
    ("store", re.compile(r"(?i)\bstor(?:e|ed|es|ing|age)\b|\bsav(?:e|ed|es|ing)\b|\bpersist|\bdatabase|sqlite")),
    ("notify", re.compile(r"(?i)notif")),
)
_UNTESTED = re.compile(
    r"(?i)\b(no tests?|untested|not tested|without tests?|no test files?|lacks? tests?|no unit tests?|"
    r"not covered|uncovered|no coverage|has no tests|have no tests)\b"
)


def _short(items, limit: int = 4) -> str:
    items = list(items)
    shown = ", ".join(str(i) for i in items[:limit])
    return shown + (f" (+{len(items) - limit} more)" if len(items) > limit else "")


def _words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[`*_]", "", text)).strip().lower()


def _find_key(sections: dict[str, str], wanted: str) -> str | None:
    """The best heading for ``wanted``: an exact match (ignoring numbering), then one that starts with it, then
    one that contains it; among equals the one with the longest body (so a document title that happens to
    contain the words is not mistaken for the section)."""
    target = _norm(wanted)
    ranked: list[tuple[int, int, str]] = []
    for key, body in sections.items():
        bare = re.sub(r"^[\d.\s:)-]+", "", key)
        if bare == target:
            rank = 0
        elif bare.startswith(target):
            rank = 1
        elif target in key:
            rank = 2
        else:
            continue
        ranked.append((rank, -len(body.split()), key))
    return min(ranked)[2] if ranked else None


def _section(sections: dict[str, str], wanted: str) -> str | None:
    key = _find_key(sections, wanted)
    return sections[key] if key is not None else None


def sections_present(work: Path | str, rel: str, required: tuple[str, ...], *, min_words: int, name: str, hint: str,
                     ) -> Check:
    """Like ``checks.sections_check`` but robust to a document title that contains a section's words."""
    path = Path(work) / rel
    if not path.is_file():
        return Check(name, False, f"{rel} does not exist", hint)
    sections = checks.markdown_sections(path)
    missing, thin = [], []
    for wanted in required:
        body = _section(sections, wanted)
        if body is None:
            missing.append(wanted)
        elif _words(body) < min_words:
            thin.append(wanted)
    if missing or thin:
        parts = ([f"missing: {_short(missing)}"] if missing else []) + ([f"too short: {_short(thin)}"] if thin else [])
        return Check(name, False, "; ".join(parts), hint)
    return Check(name, True, "")


# ---------------------------------------------------------------------------------------------
# facts about the learner's repository
# ---------------------------------------------------------------------------------------------
@dataclass
class RepoFacts:
    files: set[str] = field(default_factory=set)  # repo-relative posix paths of every file
    basenames: set[str] = field(default_factory=set)
    modules: set[str] = field(default_factory=set)  # money, limits, ..., remit, najmkit
    names_by_module: dict[str, set[str]] = field(default_factory=dict)  # module stem -> names it defines or imports
    all_names: set[str] = field(default_factory=set)  # every def, class, method, constant, import in src and tests
    methods_by_class: dict[str, set[str]] = field(default_factory=dict)


def collect_repo_facts(work: Path | str) -> RepoFacts:
    """Walk the work directory (not .git, caches) and parse the Python files under src/ and tests/."""
    root = Path(work)
    facts = RepoFacts()
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if not path.is_file() or _SKIP_DIRS & set(rel.parts):
            continue
        facts.files.add(rel.as_posix())
        facts.basenames.add(path.name)
    facts.modules |= {"remit", "najmkit"}
    for rel in sorted(facts.files):
        if not rel.endswith(".py") or not (rel.startswith("src/") or rel.startswith("tests/")):
            continue
        try:
            tree = ast.parse((root / rel).read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError, OSError):
            continue
        stem = Path(rel).stem
        if rel.startswith("src/"):
            facts.modules.add(stem)
        names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                names.add(node.name)
            elif isinstance(node, ast.ClassDef):
                names.add(node.name)
                facts.methods_by_class.setdefault(node.name, set()).update(
                    m.name for m in node.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
                )
            elif isinstance(node, ast.Assign):
                names.update(t.id for t in node.targets if isinstance(t, ast.Name))
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                names.add(node.target.id)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    names.add((alias.asname or alias.name).split(".")[0])
        facts.names_by_module.setdefault(stem, set()).update(names)
        facts.all_names |= names
    return facts


def _lines_with_context(text: str):
    """(line number, line, line plus the next one) for every line outside a fenced block."""
    lines = text.splitlines()
    fenced = False
    for index, line in enumerate(lines):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced:
            continue
        yield index + 1, line, line + " " + (lines[index + 1] if index + 1 < len(lines) else "")


def _all_lines_with_context(text: str):
    """Like ``_lines_with_context`` but also inside fenced blocks (a directory tree names files too)."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        yield index + 1, line, line + " " + (lines[index + 1] if index + 1 < len(lines) else "")


# ---------------------------------------------------------------------------------------------
# docs/onboarding.md
# ---------------------------------------------------------------------------------------------
def _path_resolves(token: str, facts: RepoFacts) -> bool:
    wanted = token[2:] if token.startswith("./") else token
    if "/" in wanted:
        return wanted in facts.files or any(f.endswith("/" + wanted) for f in facts.files)
    return wanted in facts.basenames


def missing_paths(text: str, facts: RepoFacts) -> list[str]:
    """Files the text names that do not exist (lines that say the document is stale are skipped)."""
    bad: list[str] = []
    for _, line, with_next in _all_lines_with_context(text):
        if "://" in line or _DOUBT.search(with_next):
            continue
        for match in _PATH_TOKEN.finditer(line):
            token = match.group(1)
            if not _path_resolves(token, facts) and token not in bad:
                bad.append(token)
    return bad


def unknown_calls(text: str, facts: RepoFacts) -> list[str]:
    """Inline `name(...)` calls whose function is not defined, imported or built in anywhere in the repository."""
    known = facts.all_names | set(dir(builtins)) | {"pytest", "fixture", "raises", "parametrize"}
    bad: list[str] = []
    for _, line, with_next in _lines_with_context(text):
        if _DOUBT.search(with_next):
            continue
        for code in _INLINE_CODE.findall(line):
            match = _CALL.match(code.strip())
            if not match:
                continue
            parts = match.group(1).split(".")
            func = parts[-1]
            if len(parts) == 1:
                ok = func in known
            else:
                owner = parts[-2]
                if owner in facts.methods_by_class:
                    ok = func in facts.methods_by_class[owner]
                elif owner in facts.names_by_module and owner in facts.modules:
                    ok = func in facts.names_by_module[owner]
                else:
                    ok = True  # an object or library we cannot judge (self.store, pytest, a variable)
            if not ok and match.group(1) not in bad:
                bad.append(match.group(1))
    return bad


def invented_technology(text: str) -> list[str]:
    found: list[str] = []
    for _, line, with_next in _lines_with_context(text):
        if _DOUBT.search(with_next) or _NEGATION.search(line):
            continue
        for match in _TECH_RE.finditer(line):
            name = match.group(1)
            if name not in found:
                found.append(name)
    return found


def stale_claims(text: str) -> list[str]:
    """Claims copied from docs/ARCHITECTURE.md that the code contradicts (unless the line says they are stale)."""
    found: list[str] = []
    for _, line, with_next in _all_lines_with_context(text):
        if _DOCS_WRONG.search(with_next) or _STALE_CLAIM_EXEMPT.search(line):
            continue
        for label, pattern in _STALE_CLAIMS:
            if pattern.search(line) and label not in found:
                found.append(label)
    return found


def flow_in_order(section_text: str) -> tuple[bool, str]:
    """Do the transfer steps appear, in the order the code runs them, as a subsequence of the text?"""
    position = 0
    for name, pattern in FLOW:
        match = pattern.search(section_text, position)
        if match is None:
            earlier = pattern.search(section_text)
            if earlier is None:
                return False, f"the step '{name}' is not mentioned"
            return False, f"the step '{name}' comes before the step that should precede it"
        position = match.end()
    return True, ""


def onboarding_checks(work: Path | str) -> list[Check]:
    """The six checks on docs/onboarding.md. Names are stable and unique."""
    work = Path(work)
    path = work / ONBOARDING
    names = {
        "sections": "The tour exists and has its sections",
        "length": "The tour is a sensible length",
        "files": "Every file the tour names exists",
        "flow": "The tour lists the transfer steps in the order the code runs them",
        "claims": "The tour makes no claim the code contradicts",
        "essentials": "The tour covers the entry points, the tests, the gaps and the house rules",
    }
    section_check = sections_present(
        work, ONBOARDING, ONBOARDING_SECTIONS, min_words=12, name=names["sections"],
        hint="Use these headings, each with a few real sentences: " + ", ".join(ONBOARDING_SECTIONS) + ".",
    )
    if not path.is_file():
        reason = "docs/onboarding.md does not exist yet"
        return [section_check] + [Check(names[k], False, reason) for k in ("length", "files", "flow", "claims", "essentials")]

    text = path.read_text(encoding="utf-8", errors="replace")
    sections = checks.markdown_sections(path)
    facts = collect_repo_facts(work)
    result = [section_check]

    count = _words(text)
    low, high = ONBOARDING_WORDS
    result.append(Check(names["length"], low <= count <= high, f"{count} words (aim for {low} to {high})",
                        "" if low <= count <= high else
                        "A tour is one or two pages: cut it down, or say more about the parts a newcomer will touch first."))

    bad_files = missing_paths(text, facts)
    result.append(Check(
        names["files"], not bad_files,
        "all files named exist" if not bad_files else f"named but not in the repository: {_short(bad_files)}",
        "" if not bad_files else "List the folder with ls (or ask your tool to) before you write a file name down. "
                                 "Documents drift: when a document and the code disagree, the code wins."))

    flow_text = _section(sections, "Data flow")
    if flow_text is None:
        result.append(Check(names["flow"], False, "there is no 'Data flow' section",
                            "Add a 'Data flow' section: the steps a transfer goes through when it is sent."))
    else:
        ok, why = flow_in_order(flow_text)
        result.append(Check(names["flow"], ok, "the steps are all there, in order" if ok else why,
                            "" if ok else "Open src/remit/service.py and read send() from the top: write the steps in the order the code runs them."))

    problems: list[str] = []
    calls = unknown_calls(text, facts)
    if calls:
        problems.append("functions that are not in the code: " + _short(calls))
    tech = invented_technology(text)
    if tech:
        problems.append("technology the repository does not use: " + _short(tech))
    stale = stale_claims(text)
    if stale:
        problems.append("claims the code contradicts: " + _short(stale))
    result.append(Check(
        names["claims"], not problems, "no contradicted claims found" if not problems else "; ".join(problems),
        "" if not problems else "Check each of these against the code (grep for it, open the file). If a document is wrong, "
                                "say that it is wrong instead of repeating it."))

    lowered = text.lower()
    missing: list[str] = []
    if not re.search(r"python -m remit|remit\.cli|cli\.py", text):
        missing.append("the command line entry point")
    if "RemitService" not in text or not re.search(r"\bsend\b", text) or not re.search(r"\bquote\b", text):
        missing.append("RemitService with send and quote")
    if "pytest" not in lowered:
        missing.append("how to run the tests")
    if "conftest" not in lowered:
        missing.append("the shared test fixtures")
    gaps_text = " ".join(t for t in (_section(sections, "Tests"), _section(sections, "Risks and gaps")) if t)
    if not (re.search(r"(?i)\bledger\b", gaps_text) and re.search(r"(?i)\bscreening\b", gaps_text) and _UNTESTED.search(gaps_text)):
        missing.append("that the ledger and screening modules have no tests")
    if not re.search(r"(?i)\bdecimals?\b", text):
        missing.append("the money rule (Decimal, never float)")
    if "najmkit" not in lowered:
        missing.append("najmkit")
    result.append(Check(
        names["essentials"], not missing, "all there" if not missing else "missing: " + _short(missing, 7),
        "" if not missing else "These are the things a newcomer needs first. Find each in the repository (README.md, CONTRIBUTING.md, "
                               "the tests folder) and put it in the tour."))
    return result


# ---------------------------------------------------------------------------------------------
# docs/root-cause.md
# ---------------------------------------------------------------------------------------------
def names_the_cause(root_cause_text: str) -> tuple[bool, list[str]]:
    """Does the "Root cause" section say what went wrong (UTC instead of Qatar time) and where?"""
    missing: list[str] = []
    if not re.search(r"\bUTC\b", root_cause_text):
        missing.append("which time zone the code used")
    if not re.search(r"(?i)\bQatar\b|\bDoha\b|\bAST\b|UTC\s*\+\s*3|\+\s*03:00|\blocal (?:time|day|midnight|calendar)", root_cause_text):
        missing.append("which time zone it should have used")
    if not re.search(r"limits\.py|day_window|month_window|to_local", root_cause_text):
        missing.append("where in the code")
    return not missing, missing


def affected_in_text(text: str, refused: tuple[str, ...], allowed: tuple[str, ...]) -> tuple[int, int]:
    return sum(1 for c in refused if c in text), sum(1 for c in allowed if c in text)


def defined_test_names(work: Path, changed_test_files: list[str]) -> set[str]:
    names: set[str] = set()
    for rel in changed_test_files:
        try:
            tree = ast.parse((work / rel).read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError, OSError):
            continue
        names |= {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("test")}
    return names


def root_cause_checks(work: Path | str, refused: tuple[str, ...], allowed: tuple[str, ...]) -> list[Check]:
    """The checks on docs/root-cause.md (the last three are advisory)."""
    work = Path(work)
    path = work / ROOT_CAUSE
    names = {
        "sections": "The root-cause note exists and has its sections",
        "cause": "The root-cause note names the cause",
        "both": "The note covers every place the defect lived",
        "repro": "The note's reproduction points at your own test",
        "impact": "The note lists who was affected",
    }
    sections_result = sections_present(
        work, ROOT_CAUSE, ROOT_CAUSE_SECTIONS, min_words=8, name=names["sections"],
        hint="Use these headings, each with real sentences: " + ", ".join(ROOT_CAUSE_SECTIONS) + ".")
    if not path.is_file():
        reason = "docs/root-cause.md does not exist yet"
        return [
            sections_result,
            Check(names["cause"], False, reason, "Write the note after the fix, from the evidence you collected."),
            Check(names["both"], False, reason, "", required=False),
            Check(names["repro"], False, reason, "", required=False),
            Check(names["impact"], False, reason, "", required=False),
        ]
    text = path.read_text(encoding="utf-8", errors="replace")
    sections = checks.markdown_sections(path)
    result = [sections_result]

    cause_text = _section(sections, "Root cause") or ""
    ok, missing = names_the_cause(cause_text)
    result.append(Check(
        names["cause"], ok, "names the cause" if ok else "the 'Root cause' section does not say " + _short(missing),
        "" if ok else "A root cause is a mechanism, not a symptom: say what the code does, where, and what it should do instead."))

    fix_text = " ".join(t for t in (cause_text, _section(sections, "Fix") or "") if t)
    has_both = bool(re.search(r"(?i)\bmonth", fix_text)) and bool(re.search(r"(?i)\bday|daily", fix_text))
    result.append(Check(
        names["both"], has_both, "day and month both mentioned" if has_both else "the note speaks only of one window",
        "" if has_both else "When one line is wrong, look for its twin: where else is the same mistake made?", required=False))

    repro_text = _section(sections, "Reproduction") or ""
    changed_tests = checks.new_test_files(work)
    defined = defined_test_names(work, changed_tests)
    cited = set(re.findall(r"\btest\w*", repro_text))
    cited_files = {rel for rel in changed_tests if Path(rel).name in repro_text or rel in repro_text}
    ok = bool(defined & cited) or bool(cited_files)
    result.append(Check(
        names["repro"], ok, "the note names a test you added or changed" if ok else "no test you added or changed is named in the 'Reproduction' section",
        "" if ok else "Say which test reproduces the problem and how to run it (for example the pytest command).", required=False))

    found_refused, found_allowed = affected_in_text(text, refused, allowed)
    ok = found_refused >= len(refused) - 1 and found_allowed >= 1
    result.append(Check(
        names["impact"], ok,
        f"{found_refused} of {len(refused)} wrongly refused customers and {found_allowed} of {len(allowed)} wrongly accepted ones are named" if not ok
        else "the affected customers are listed",
        "" if ok else "Replay prod.log through the corrected limits (the tiers are in kyc_tiers.csv): who was refused who should not have been, "
                      "and who was let through who should have been refused?", required=False))
    return result


# ---------------------------------------------------------------------------------------------
# the fix and the tests
# ---------------------------------------------------------------------------------------------
def _function_sources(source: str) -> dict[str, str]:
    """Qualified name -> normalised source (ast.unparse) of every test function and method."""
    out: dict[str, str] = {}
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return out

    def visit(body, prefix: str) -> None:
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                out[prefix + node.name] = ast.unparse(node)
            elif isinstance(node, ast.ClassDef):
                visit(node.body, prefix + node.name + ".")

    visit(tree.body, "")
    return out


def tests_not_weakened(work: Path | str, name: str = "The existing tests were not edited or removed") -> Check:
    """Every test and fixture that existed at lab-start is still there, unchanged (additions are welcome)."""
    work = Path(work)
    problems: list[str] = []
    for path, state in gitutil.changed_status(work, LAB_START_TAG).items():
        if not path.startswith("tests/") or not path.endswith(".py"):
            continue
        before = gitutil.file_at(work, LAB_START_TAG, path)
        if before is None:
            continue  # a new file: always fine
        if state == "D" or not (work / path).is_file():
            problems.append(f"{path} was deleted")
            continue
        after = (work / path).read_text(encoding="utf-8", errors="replace")
        old, new = _function_sources(before), _function_sources(after)
        for func, source in old.items():
            if func not in new:
                problems.append(f"{path}: {func} was removed")
            elif new[func] != source:
                problems.append(f"{path}: {func} was changed")
    if problems:
        return Check(name, False, _short(problems, 3),
                     "The old tests are right. Put them back (git restore tests) and add your new tests next to them, in a new file or at the end of one.")
    return Check(name, True, "")


def _numstat(work: Path, path_spec: str) -> list[tuple[str, int, int]]:
    rows: list[tuple[str, int, int]] = []
    raw = gitutil.git(work, "diff", "--numstat", "--no-renames", "-z", LAB_START_TAG, "--", path_spec).stdout
    for record in raw.split("\0"):
        if not record:
            continue
        added, deleted, path = record.split("\t", 2)
        rows.append((path, int(added) if added.isdigit() else 0, int(deleted) if deleted.isdigit() else 0))
    untracked = gitutil.git(work, "ls-files", "--others", "--exclude-standard", "-z", "--", path_spec).stdout
    for path in (p for p in untracked.split("\0") if p):
        if gitutil.glob_match(path, gitutil.TOOL_NOISE):
            continue
        try:
            lines = len((work / path).read_bytes().splitlines())
        except OSError:
            lines = 0
        rows.append((path, lines, 0))
    return rows


def fix_is_small(work: Path | str, max_lines: int = 20, name: str = "The fix is a few lines in one place") -> Check:
    work = Path(work)
    rows = _numstat(work, "src")
    if not rows:
        return Check(name, False, "nothing in src has changed yet",
                     "The cause is in the code, not in the tests: reproduce it first, then find it.")
    limits_rows = [r for r in rows if r[0] == LIMITS_FILE]
    if not limits_rows:
        return Check(name, False, "you changed " + _short(sorted(r[0] for r in rows)) + ", but the defect is not there",
                     "Where does the code decide which day and which month a moment belongs to? Look there, and prove it with a test.")
    changed = sum(a + d for _, a, d in limits_rows)
    ok = changed <= max_lines
    return Check(name, ok, f"{changed} lines changed in the module that decides the limits (limit {max_lines})",
                 "" if ok else "A fix for one wrong line should be a few lines. Is there a smaller change that is still correct? "
                               "A reviewer of money logic has five minutes.")


def starter_limits_with(work: Path | str, *, fix_day: bool = False, fix_month: bool = False) -> str | None:
    """The starter's limits.py with the seeded defect removed from the day helper, the month helper or both."""
    text = gitutil.file_at(work, LAB_START_TAG, LIMITS_FILE)
    if text is None or text.count(BAD_CONVERSION) != 2:
        return None
    first = text.find(BAD_CONVERSION)
    second = text.find(BAD_CONVERSION, first + 1)
    if fix_month:
        text = text[:second] + GOOD_CONVERSION + text[second + len(BAD_CONVERSION):]
    if fix_day:
        text = text[:first] + GOOD_CONVERSION + text[first + len(BAD_CONVERSION):]
    return text


def variant_check(work: Path | str, *, name: str, fix_day: bool, fix_month: bool, hint: str, required: bool,
                  success: str, failure: str, timeout: float = 60.0) -> Check:
    """Run the learner's new or changed tests against the starter's limits.py with one defect fixed.

    The check passes when at least one test fails or errors: the tests notice the defect that is still there.
    """
    work = Path(work)
    chosen = checks.new_test_files(work)
    if not chosen:
        return Check(name, False, "no new or changed test files found", "Add your test in a tests/test_*.py file.", required)
    variant = starter_limits_with(work, fix_day=fix_day, fix_month=fix_month)
    if variant is None:
        return Check(name, False, "the starting code could not be reconstructed", "This is a bug in the lab, not in your work.", required)
    with checks.work_copy(work) as root:
        for path, state in gitutil.changed_status(work, LAB_START_TAG, ignore=()).items():
            if gitutil.glob_match(path, ["tests/**"]):
                continue
            target = root / path
            original = None if state == "A" else gitutil.show_bytes(work, LAB_START_TAG, path)
            if original is None:
                target.unlink(missing_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(original)
        (root / LIMITS_FILE).write_text(variant, encoding="utf-8", newline="\n")
        chosen = [p for p in chosen if (root / p).exists()]
        result = checks.run_pytest(root, chosen, timeout=timeout)
    # A collection error counts, like a failure: a sound solution may add a helper that its tests import, and that
    # import cannot succeed against the starter's code. (The stock tests_fail_on_starter treats errors the same way.)
    ok = (result.failed + result.errors) > 0 or result.timed_out
    return Check(name, ok, success if ok else failure, "" if ok else hint, required)


# ---------------------------------------------------------------------------------------------
# hygiene
# ---------------------------------------------------------------------------------------------
def one_concern_per_commit(work: Path | str, name: str = "The tour and the fix are separate commits") -> Check:
    """No single commit touches both the source code and the onboarding tour (CONTRIBUTING.md: one logical change)."""
    work = Path(work)
    mixed: list[str] = []
    for commit in gitutil.commits_since(work, LAB_START_TAG):
        files = set(gitutil.git(work, "show", "--name-only", "--format=", commit.sha).stdout.split())
        if ONBOARDING in files and any(f.startswith("src/") for f in files):
            mixed.append(commit.sha[:7])
    if mixed:
        return Check(name, False, "one commit changes both the code and the tour: " + _short(mixed),
                     "One logical change per commit (CONTRIBUTING.md). Split the commit: the tour is one change, the fix is another.", required=False)
    return Check(name, True, "", "", required=False)


def agent_log_check(work: Path | str, name: str = "Your agent log is in docs/agent-log.md") -> Check:
    path = Path(work) / AGENT_LOG
    if not path.is_file():
        return Check(name, False, "docs/agent-log.md does not exist",
                     "Write down, for each agent session: the prompt, what it did, what you corrected, how long it took. "
                     "If you used no agent, say so and say what you did by hand.", required=False)
    words = _words(path.read_text(encoding="utf-8", errors="replace"))
    ok = words >= 40
    return Check(name, ok, f"{words} words", "" if ok else "A log of a few lines is not a log: say what you asked, what came back and what you changed.", required=False)
