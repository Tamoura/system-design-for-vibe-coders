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
* ``reproduction_check`` and ``variant_check``  run the learner's new tests against the starter (the first) or against
  the starter's ``limits.py`` with one of the two seeded defects removed (the second). A test counts only if it RUNS
  and fails (an assertion about behaviour): a collection or import error is not a reproduction.
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
ROOT_CAUSE_SECTIONS = ("Summary", "Symptom", "Reproduction", "Root cause", "Why it was missed", "Fix", "Impact",
                       "Prevention", "Open questions")
ONBOARDING_WORDS = (250, 1500)
# Words a section needs to count as written. "Open questions" may honestly be short ("None found.").
TOUR_MIN_WORDS = {"*": 12, "Open questions": 5}
NOTE_MIN_WORDS = {"*": 8, "Open questions": 1}

_SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "node_modules", ".mypy_cache"}

# A line (or the line after it) that says a document is wrong, or that something is missing, is not a false claim.
_DOUBT = re.compile(
    r"(?i)\b(stale|outdated|out[- ]of[- ]date|no longer|does ?n[o']t exist|do not exist|doesn’t exist|not exist|"
    r"nonexistent|non-existent|missing|absent|there is no|there are no|no such|not a real|wrong|incorrect|"
    r"inaccurate|mismatch|disagrees?|contradicts?|drift\w*|dangling|misleading|untrue|false|obsolete|"
    r"never existed|was removed|were removed|has been removed|is gone|are gone|"
    r"(?:is|are|was|were) not (?:in|on|at|present|there|here|found|part of|included|shipped|committed|checked in|"
    r"available|provided|a file|real)|(?:is|are|was|were)n['’]t (?:in|on|at|present|there|here|found|part of|included|"
    r"shipped|committed|checked in|available|provided)|"
    r"not (?:in|part of|included in|shipped with|present in) (?:the |this |our )?(?:repo\w*|checkout|tree|clone|project)|"
    r"never (?:committed|added|checked in|shipped|created|written|existed)|"
    r"(?:could not|couldn't|can not|cannot|can't|did not|didn't|do not|don't|does not|doesn't) "
    r"(?:find|see|locate|spot|ship|include|contain|have)|not found|no (?:such )?(?:file|module)|nowhere)\b"
)
# A sentence that attributes a claim to a document ("ARCHITECTURE.md says ...") reports it; it does not assert it.
_DOC_VERBS = re.compile(
    r"(?i)\b(?:says?|said|claims?|claimed|states?|stated|describes?|described|lists?|listed|mentions?|mentioned|"
    r"according to|promises|documents)\b"
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

# The steps of RemitService.send, in the order the code runs them (service.py), as patterns. A step is "named" by the
# word the code uses or a plain synonym. Underscores and digits are word breaks, so `quote_fee` names the fee step
# and `fx_quote` the fx step.
FLOW = (
    ("validate", re.compile(r"(?i)validat|verif|sanity|input check|request check")),
    ("limits", re.compile(r"(?i)limit|(?<![a-z])caps?(?![a-z])|quota")),
    ("screening", re.compile(r"(?i)screen|sanction|watch[- ]?list")),
    ("fee", re.compile(r"(?i)(?<![a-z])fees?(?![a-z])|(?<![a-z])charges?(?![a-z])")),
    ("fx", re.compile(r"(?i)(?<![a-z])fx(?![a-z])|exchange|(?<![a-z])rates?(?![a-z])|conversion")),
    ("ledger", re.compile(r"(?i)ledger|double[- ]entr|(?<![a-z])postings?(?![a-z])")),
    ("store", re.compile(r"(?i)(?<![a-z])stor(?:e|ed|es|ing|age)(?![a-z])|(?<![a-z])sav(?:e|ed|es|ing)(?![a-z])|persist|database|sqlite|repository")),
    ("notify", re.compile(r"(?i)notif|(?<![a-z])sms(?![a-z])|e-?mail|tells? the customer|message the customer")),
)
# The tour must say where the tests are thin. Accurate wordings differ ("no tests", "no dedicated tests", "only exercised
# through test_service", "not directly tested"): accept the plain ways of saying it.
_UNTESTED = re.compile(
    r"(?i)(?<![a-z])(?:no (?:[a-z-]+ ){0,2}tests?|no (?:[a-z-]+ ){0,2}test files?|untested|"
    r"(?:is|are|was|were)(?: not|n['’]t) (?:[a-z-]+ )?(?:tested|covered)|not (?:[a-z-]+ )?(?:tested|covered)|"
    r"(?:thinly|barely|poorly|weakly|lightly|indirectly|only indirectly) (?:tested|covered|exercised)|"
    r"without (?:any|their own|its own|a|dedicated|direct|unit) (?:[a-z-]+ )?tests?|lacks? (?:[a-z-]+ ){0,3}tests?|tests? of (?:its|their) own|"
    r"(?:only|just) (?:exercised|covered|tested|touched|run|reached)|no (?:[a-z-]+ )?coverage|uncovered|"
    r"(?:little|low|minimal|zero) (?:[a-z-]+ )?coverage)(?![a-z])"
)


def _short(items, limit: int = 4) -> str:
    items = list(items)
    shown = ", ".join(str(i) for i in items[:limit])
    return shown + (f" (+{len(items) - limit} more)" if len(items) > limit else "")


def _words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def _content_words(text: str) -> int:
    """Words that contain a letter or a digit (a lone dash or bullet is not a word)."""
    return sum(1 for token in text.split() if re.search(r"\w", token))


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


def sections_present(work: Path | str, rel: str, required: tuple[str, ...], *, min_words: dict[str, int], name: str,
                     hint: str) -> Check:
    """Like ``checks.sections_check`` but robust to a document title that contains a section's words.

    ``min_words`` maps a section name (or ``"*"`` for the rest) to the words it needs. A title above the sections and
    extra sections are fine; only the required headings are looked for."""
    path = Path(work) / rel
    if not path.is_file():
        return Check(name, False, f"{rel} does not exist", hint)
    sections = checks.markdown_sections(path)
    missing, thin = [], []
    for wanted in required:
        body = _section(sections, wanted)
        if body is None:
            missing.append(wanted)
        elif _content_words(body) < min_words.get(wanted, min_words["*"]):
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
    called_names: set[str] = field(default_factory=set)  # every function or method called in src and tests
    source_words: set[str] = field(default_factory=set)  # every identifier-like word in src and tests, comments and docstrings too


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
            source = (root / rel).read_text(encoding="utf-8")
            tree = ast.parse(source)
        except (SyntaxError, UnicodeDecodeError, OSError):
            continue
        facts.source_words.update(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", source))
        stem = Path(rel).stem
        if rel.startswith("src/"):
            facts.modules.add(stem)
        names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    facts.called_names.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    facts.called_names.add(node.func.attr)
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


_BULLET = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")


def _starts_item(line: str) -> bool:
    return not line.strip() or bool(_BULLET.match(line)) or line.lstrip().startswith(("#", "|"))


def _item_context(lines: list[str], index: int, span: int = 2) -> str:
    """The line plus the neighbouring lines of the same item (the same paragraph, list item or table row).

    A sentence that says "this file is missing" or "the document is stale" is usually on the line before or after the
    file name, because markdown is wrapped; but it must not leak into the next bullet or the next table row."""
    line = lines[index]
    parts = [line]
    if not (not line.strip() or line.lstrip().startswith(("#", "|")) or _BULLET.match(line)):
        back = index - 1
        while back >= 0 and index - back <= span and lines[back].strip() and not lines[back].lstrip().startswith(("#", "|")):
            parts.insert(0, lines[back])
            if _BULLET.match(lines[back]):
                break
            back -= 1
    if line.strip() and not line.lstrip().startswith(("#", "|")):
        ahead = index + 1
        while ahead < len(lines) and ahead - index <= span and not _starts_item(lines[ahead]):
            parts.append(lines[ahead])
            ahead += 1
    return " ".join(parts)


def _lines_with_context(text: str):
    """(line number, line, its item context) for every line outside a fenced block."""
    lines = text.splitlines()
    fenced = False
    for index, line in enumerate(lines):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced:
            continue
        yield index + 1, line, _item_context(lines, index)


def _all_lines_with_context(text: str):
    """Like ``_lines_with_context`` but also inside fenced blocks (a directory tree names files too)."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        yield index + 1, line, _item_context(lines, index)


# ---------------------------------------------------------------------------------------------
# docs/onboarding.md
# ---------------------------------------------------------------------------------------------
def _path_resolves(token: str, facts: RepoFacts) -> bool:
    wanted = token[2:] if token.startswith("./") else token
    if "/" in wanted:
        return wanted in facts.files or any(f.endswith("/" + wanted) for f in facts.files)
    return wanted in facts.basenames


def missing_paths(text: str, facts: RepoFacts) -> list[str]:
    """Files the text names that do not exist (a file named as missing, or a document named as stale, is skipped)."""
    bad: list[str] = []
    for _, line, context in _all_lines_with_context(text):
        if "://" in line or _DOUBT.search(context):
            continue
        for match in _PATH_TOKEN.finditer(line):
            token = match.group(1)
            if not _path_resolves(token, facts) and token not in bad:
                bad.append(token)
    return bad


def _stdlib_member_names() -> set[str]:
    """Public method and attribute names of the standard types a tour may mention (`astimezone(...)`, `replace(...)`)."""
    import collections
    import datetime
    import decimal
    import pathlib

    names: set[str] = set()
    for obj in (str, bytes, list, dict, set, tuple, int, float, datetime.datetime, datetime.date, datetime.time,
                datetime.timedelta, datetime.timezone, decimal.Decimal, pathlib.Path, collections.Counter,
                collections.deque, re.Pattern, re.Match):
        names |= {n for n in dir(obj) if not n.startswith("_")}
    return names


_STDLIB_MEMBERS = _stdlib_member_names()


def unknown_calls(text: str, facts: RepoFacts) -> list[str]:
    """Inline `name(...)` calls whose name does not occur anywhere in the repository's Python files (code, comments or
    docstrings), nor among the standard types' methods and the built-ins. (A bare `astimezone(...)` is a real method of a
    standard type, and `TODO(farid, 2022)` quotes a comment, so neither is an invented function.)"""
    known = (facts.all_names | facts.called_names | facts.source_words | _STDLIB_MEMBERS | set(dir(builtins))
             | {"pytest", "fixture", "raises", "parametrize"})
    bad: list[str] = []
    for _, line, context in _lines_with_context(text):
        if _DOUBT.search(context):
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
    for _, line, context in _lines_with_context(text):
        if _DOUBT.search(context) or _NEGATION.search(line):
            continue
        for match in _TECH_RE.finditer(line):
            name = match.group(1)
            if name not in found:
                found.append(name)
    return found


def stale_claims(text: str) -> list[str]:
    """Claims copied from docs/ARCHITECTURE.md that the code contradicts, stated as fact.

    A sentence that attributes the claim to a document ("ARCHITECTURE.md says T1 may send 5,000") or says that it is
    stale or wrong is a correct report, not a false claim."""
    found: list[str] = []
    for _, line, context in _all_lines_with_context(text):
        if _DOCS_WRONG.search(context) or _DOC_VERBS.search(context) or _STALE_CLAIM_EXEMPT.search(line):
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
        work, ONBOARDING, ONBOARDING_SECTIONS, min_words=TOUR_MIN_WORDS, name=names["sections"],
        hint="Use these headings, each with a few real sentences (a title above them and extra sections are fine): "
             + ", ".join(ONBOARDING_SECTIONS) + ".",
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
        "" if not bad_files else "If the file should exist, check the name and path with ls. If you mean to say that a document or a "
                                 "docstring names a file the repository does not have, say so in the same sentence "
                                 "(for example: 'X is not in the repository'). When a document and the code disagree, the code wins."))

    flow_text = _section(sections, "Data flow")
    if flow_text is None:
        result.append(Check(names["flow"], False, "there is no 'Data flow' section",
                            "Add a 'Data flow' section: the steps a transfer goes through when it is sent."))
    else:
        ok, why = flow_in_order(flow_text)
        result.append(Check(names["flow"], ok, "the steps are all there, in order" if ok else why,
                            "" if ok else "Open src/remit/service.py and read send() from the top: write the steps in the order the code runs them, "
                                          "naming each with the word the code uses (the module name is a good choice)."))

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
                                "name the document and say that it is wrong or what it says (\"ARCHITECTURE.md says ..., the code has ...\") "
                                "instead of stating the claim as a fact."))

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
_QATAR_TERM = re.compile(r"(?i)\bQatar\b|\bDoha\b|\bAST\b|UTC\s*\+\s*3|\+\s*03:00|\blocal (?:time|day|midnight|calendar)")


def _said_together(text: str, distance: int = 250) -> bool:
    """UTC and the Qatar time zone are mentioned close to each other (a mechanism, not a bag of keywords)."""
    utc = [m.start() for m in re.finditer(r"\bUTC\b", text)]
    local = [m.start() for m in _QATAR_TERM.finditer(text)]
    return any(abs(a - b) <= distance for a in utc for b in local)


def names_the_cause(root_cause_text: str) -> tuple[bool, list[str]]:
    """Does the "Root cause" section say what went wrong (UTC instead of Qatar time) and where?"""
    missing: list[str] = []
    if not re.search(r"\bUTC\b", root_cause_text):
        missing.append("which time zone the code used")
    if not _QATAR_TERM.search(root_cause_text):
        missing.append("which time zone it should have used")
    if not re.search(r"limits\.py|day_window|month_window|to_local", root_cause_text):
        missing.append("where in the code")
    if not missing and not _said_together(root_cause_text):
        missing.append("how the two relate (UTC where Qatar time was meant)")
    return not missing, missing


# Which way was a customer hurt? R: refused although they should have been allowed. A: let through although they
# should have been refused. Alternatives are tried left to right at each position, so the longer, more specific
# phrases win ("should not have been refused" is R; "refused correctly" says nothing about a defect).
_DIRECTION = re.compile(
    r"(?P<N>(?:refused|rejected|declined|blocked|stopped)\s+(?:correctly|rightly|properly)|"
    r"(?:correctly|rightly|properly)\s+(?:refused|rejected|declined|blocked|stopped))"
    r"|(?P<R>should\s+not\s+have\s+been\s+(?:refused|rejected|declined|blocked|stopped)|"
    r"should\s+have\s+been\s+(?:allowed|accepted|approved|sent|let\s+through)|not\s+allowed|disallowed|"
    r"limit[ _]exceeded|could(?:\s+not|n't)\s+send|unable\s+to\s+send)"
    r"|(?P<A>should\s+(?:have\s+been|be)\s+(?:refused|rejected|declined|blocked|stopped)|"
    r"should\s+have\s+(?:refused|rejected|blocked|stopped)|let\s+through|went\s+through|slipped\s+through|"
    r"got\s+through|allowed|accepted|approved|over(?:spent|drew|sent)|exceed\w*|transfer\.sent|(?:was|were)\s+sent)"
    r"|(?P<R2>refus\w*|reject\w*|declin\w*|denied|blocked|turned\s+away)",
    re.I,
)
_CLAUSE_BREAK = re.compile(r"(?<=[.;!?])\s+|\n+|\s+but\s+|\s+whereas\s+|\s+while\s+", re.I)
_CUSTOMER_ID = re.compile(r"\bC\d{4}\b")
_AND = re.compile(r"\s*,?\s+and\s+", re.I)


def _real_hits(clause: str) -> list[tuple[int, str]]:
    return [(m.start(), "R" if (m.group("R") or m.group("R2")) else "A")
            for m in _DIRECTION.finditer(clause) if not m.group("N")]


def _split_on_and(clause: str) -> list[str]:
    """Split "C1 and C2 were refused, and C7 was let through" where both sides say a direction of their own."""
    for match in _AND.finditer(clause):
        left, right = clause[:match.start()], clause[match.end():]
        if _real_hits(left) and _real_hits(right):
            return [left] + _split_on_and(right)
    return [clause]


def affected_by_direction(text: str, refused: tuple[str, ...], allowed: tuple[str, ...]) -> tuple[int, int]:
    """How many of the wrongly refused / wrongly accepted customers does the text name, in the right direction?

    The text is read clause by clause (sentences, table rows, list items, "..., but ..."). A clause that names ids and a
    direction gives them that direction (the nearest direction word, the one before the id if there are two); a
    clause that names ids and no direction (a list under "Wrongly refused:") takes the last direction said before it."""
    direction: dict[str, set[str]] = {}
    carried: str | None = None
    clauses = [part for chunk in _CLAUSE_BREAK.split(text) if chunk and chunk.strip() for part in _split_on_and(chunk)]
    for clause in clauses:
        hits = [(m.start(), "N" if m.group("N") else "R" if (m.group("R") or m.group("R2")) else "A")
                for m in _DIRECTION.finditer(clause)]
        real = [(pos, kind) for pos, kind in hits if kind != "N"]
        ids = [(m.start(), m.group(0)) for m in _CUSTOMER_ID.finditer(clause)]
        for pos, cid in ids:
            if real:
                before = [h for h in real if h[0] < pos]
                kind = before[-1][1] if before else real[0][1]
                if len({k for _, k in real}) == 1:
                    kind = real[0][1]
            elif hits:
                continue  # only "refused correctly": not about a defect
            elif carried:
                kind = carried
            else:
                continue
            direction.setdefault(cid, set()).add(kind)
        if real:
            carried = real[-1][1]
    return (sum(1 for c in refused if "R" in direction.get(c, ())),
            sum(1 for c in allowed if "A" in direction.get(c, ())))


def affected_in_text(text: str, refused: tuple[str, ...], allowed: tuple[str, ...]) -> tuple[int, int]:
    """How many of the customers are named at all, whatever the direction (see ``affected_by_direction``)."""
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
        work, ROOT_CAUSE, ROOT_CAUSE_SECTIONS, min_words=NOTE_MIN_WORDS, name=names["sections"],
        hint="Use these headings, each with real sentences (a title above them is fine): " + ", ".join(ROOT_CAUSE_SECTIONS) + ".")
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

    impact_text = _section(sections, "Impact") or text
    found_refused, found_allowed = affected_by_direction(impact_text, refused, allowed)
    ok = found_refused >= len(refused) - 1 and found_allowed >= 1
    result.append(Check(
        names["impact"], ok,
        f"{found_refused} of {len(refused)} wrongly refused customers and {found_allowed} of {len(allowed)} wrongly accepted ones "
        "are named with the right direction" if not ok else "the affected customers are listed, each with the way the defect hurt them",
        "" if ok else "Support names only some of the customers: replay prod.log through the corrected limits (the tiers are in kyc_tiers.csv). "
                      "Then list, under Impact and by id, who was refused who should not have been, and who was let through who should "
                      "have been refused, saying which is which.", required=False))
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
                     "The old tests are right. Put them back as they were at the start (git restore --source=lab-start -- tests), even if you have committed the edit, "
                     "and add your new tests next to them, in a new file or at the end of one.")
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


# A test that "fails" because a name it imports or reads does not exist yet says nothing about what the customers saw.
_BROKEN_TEST = re.compile(
    r"^FAILED \S+ - (?:ImportError|ModuleNotFoundError|NameError|SyntaxError|IndentationError|AttributeError: module)", re.M)


def behaviour_failures(result: checks.PytestResult) -> int:
    """Tests that ran and failed on an assertion or on what the code did, not on a collection or import error.

    A module that cannot be imported is an ``error`` in pytest's report and does not count; neither does a test whose
    body fails on an ImportError or NameError (a name that only exists in the learner's own fix)."""
    broken = len(_BROKEN_TEST.findall(result.output or ""))
    return max(result.failed - broken, 0)


def _run_new_tests_on_starter(work: Path, limits_text: str | None = None, timeout: float = 60.0):
    """Run the learner's new or changed tests against the starting code (every file outside tests/ put back to its
    lab-start state), optionally with a different limits.py. Returns the PytestResult, or None if there are no tests."""
    chosen = checks.new_test_files(work)
    if not chosen:
        return None
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
        if limits_text is not None:
            (root / LIMITS_FILE).write_text(limits_text, encoding="utf-8", newline="\n")
        chosen = [p for p in chosen if (root / p).exists()]
        # a wide terminal, so pytest's one-line failure summaries are not cut off before the error type
        # ...and keep going past a file that cannot be imported, so the other new tests still run
        return checks.run_pytest(root, chosen, timeout=timeout, args=("--continue-on-collection-errors",),
                                 extra_env={"COLUMNS": "400"})


def reproduction_check(work: Path | str, *, name: str, hint: str, timeout: float = 60.0) -> Check:
    """At least one of the learner's new tests RUNS on the original code and fails on what the code does.

    Reproducing a bug means a test that runs against today's code and fails for the customers' reason. A test file that
    cannot even be imported on the original code (it imports a constant or helper that only the fix adds) fails too, but
    proves nothing about the customers, so it does not count."""
    work = Path(work)
    result = _run_new_tests_on_starter(work, None, timeout)
    if result is None:
        return Check(name, False, "no new or changed test files found", "Add a test in tests/test_*.py.")
    caught = behaviour_failures(result)
    if caught:
        return Check(name, True, f"{caught} of your new test{'s' if caught != 1 else ''} fail{'s' if caught == 1 else ''} on the original code, as they should")
    if result.timed_out:
        return Check(name, False, "your new tests do not finish on the original code", hint)
    if result.failed or result.errors:
        return Check(name, False,
                     "your new tests error on the original code (for example they import a name that only your fix adds) instead of "
                     "running and failing, so they do not show what the customers saw",
                     "Test behaviour that exists today (check_limits, day_window, RemitService.send), so the test runs on the original "
                     "code and fails on its assertion. " + hint)
    return Check(name, False, "all of your new tests already pass on the original code, so they would not have caught the problem", hint)


def variant_check(work: Path | str, *, name: str, fix_day: bool, fix_month: bool, hint: str, required: bool,
                  success: str, failure: str, timeout: float = 60.0) -> Check:
    """Run the learner's new or changed tests against the starter's limits.py with one defect fixed.

    The check passes when at least one test runs and fails: the tests notice the defect that is still there. A test that
    only errors (cannot import something) does not count, as in ``reproduction_check``."""
    work = Path(work)
    if not checks.new_test_files(work):
        return Check(name, False, "no new or changed test files found", "Add your test in a tests/test_*.py file.", required)
    variant = starter_limits_with(work, fix_day=fix_day, fix_month=fix_month)
    if variant is None:
        return Check(name, False, "the starting code could not be reconstructed", "This is a bug in the lab, not in your work.", required)
    result = _run_new_tests_on_starter(work, variant, timeout)
    ok = behaviour_failures(result) > 0 or result.timed_out
    return Check(name, ok, success if ok else failure, "" if ok else hint, required)


# ---------------------------------------------------------------------------------------------
# hygiene
# ---------------------------------------------------------------------------------------------
def one_concern_per_commit(work: Path | str, name: str = "The tour and the fix are separate commits") -> Check:
    """No single commit touches both the source code and the onboarding tour (CONTRIBUTING.md: one logical change)."""
    work = Path(work)
    mixed: list[str] = []
    commits = gitutil.commits_since(work, LAB_START_TAG)
    if not commits:
        return Check(name, False, "no commits yet", "Commit the tour on its own, then the fix with its test, then the note.", required=False)
    for commit in commits:
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
