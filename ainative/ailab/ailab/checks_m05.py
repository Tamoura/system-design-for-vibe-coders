"""Helpers for lab m05 (review a pull request an agent wrote). Used only by ``labs/m05_pr_review``.

Two jobs, both kept apart from the lab's ``lab.py`` so that they can be tested on their own:

1. **Read a review.** ``parse_review`` turns the learner's ``review.md`` into findings (file, line,
   severity, text) and ``match_findings`` pairs those findings with the problems seeded in the
   agent's branch (``FLAWS``). Matching is tolerant on purpose: a finding counts when it names the
   right file *and* either points near the right line *or* uses words that name what is wrong.
   It is a grader, not a judge: it can tell that the review mentions the problem, not that the
   reviewer understood it.
2. **Static checks on the fixed branch.** Small AST scans (imports, broad ``except``, floats, tests
   without assertions, tests that fake the fee code, deleted tests, the leaked key) that do not depend
   on how the learner chose to fix things.

Nothing here imports or executes learner code: files are parsed with ``ast`` and pytest runs in a
subprocess through ``ailab.checks``.
"""
from __future__ import annotations

import ast
import re
import sys
import tomllib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from ailab import checks, gitutil

# =================================================================================================
# 1. the seeded problems
# =================================================================================================
SEVERITIES = {
    "blocker": "blocker", "critical": "blocker",
    "major": "major", "high": "major",
    "minor": "minor", "medium": "minor", "low": "minor",
    "nit": "nit", "nitpick": "nit", "info": "nit",
}
RANK = {"blocker": 3, "major": 2, "minor": 1, "nit": 0}


@dataclass(frozen=True)
class Flaw:
    """One problem seeded in the agent's branch.

    ``markers`` locate the problem in the starting branch: (file, text on the offending line).
    ``keywords`` are regular expressions (case-insensitive); a finding that names the flaw's file
    needs at least one of them unless it points within ``LINE_TOLERANCE`` lines of a marker.
    ``min_severity`` is the lowest rating that is not an under-call, ``max_severity`` the highest that
    is not an over-call (a test too weak to fail is a major at most; the lesson's severity table says so).
    """

    id: str
    risk: str  # the review class it belongs to; shown to the learner only as a nudge
    files: tuple[str, ...]
    markers: tuple[tuple[str, str], ...]
    keywords: tuple[str, ...]
    min_severity: str = "major"
    max_severity: str = "blocker"


FLAWS: tuple[Flaw, ...] = (
    Flaw(
        "hallucinated-dependency", "security",
        ("pyproject.toml", "src/remit/loyalty.py"),
        (("pyproject.toml", "najm-loyalty"), ("src/remit/loyalty.py", "from najm_loyalty import")),
        (r"najm[-_ ]?loyalty", r"depend", r"hallucinat", r"invent", r"made[- ]?up", r"fabricat", r"non-?existent",
         r"does(?: not|n.t) exist", r"not (?:a )?real", r"pypi", r"slopsquat", r"supply[- ]chain", r"unknown package",
         r"standard library only"),
    ),
    Flaw(
        "swallowed-exception", "correctness",
        ("src/remit/fees.py",),
        (("src/remit/fees.py", "except Exception"),),
        (r"swallow", r"except\s+exception", r"bare except", r"broad except", r"catch-?all", r"silent", r"suppress",
         r"hides?\b", r"masks?\b", r"ignores? (?:the )?error", r"unknown tier", r"error handling"),
    ),
    Flaw(
        "float-money", "correctness",
        ("src/remit/fees.py", "src/remit/loyalty.py"),
        (("src/remit/fees.py", "float(base.amount)"), ("src/remit/loyalty.py", "DISCOUNT_RATES =")),
        (r"\bfloats?\b", r"floating", r"binary", r"round\(", r"half[- ]?up", r"decimal"),
    ),
    Flaw(
        "test-asserts-nothing", "tests",
        ("tests/test_loyalty.py",),
        (("tests/test_loyalty.py", "def test_gold_gets_twenty_percent_off_the_fee"),),
        (r"no assert", r"without (?:an? )?assert", r"asserts? nothing", r"never asserts", r"(?:does(?: not|n.t)|doesnt) assert",
         r"no assertions?", r"only prints?", r"\bprint\b", r"always passes", r"vacuous", r"checks? nothing", r"proves? nothing",
         r"missing assert"),
        "minor", "major",
    ),
    Flaw(
        "over-mocked-test", "tests",
        ("tests/test_loyalty.py",),
        (("tests/test_loyalty.py", "patch.object(fees"),),
        (r"mock", r"patch", r"\bstubs?\b", r"fakes? the", r"replaces? the (?:function|helper|code)", r"tests? the (?:mock|test double)",
         r"under test"),
        "minor", "major",
    ),
    Flaw(
        "hard-coded-key", "security",
        ("src/remit/loyalty.py",),
        (("src/remit/loyalty.py", "LOYALTY_API_KEY ="),),
        (r"api[ _-]?key", r"secret", r"credential", r"hard-?coded", r"\bkey\b", r"\btoken\b", r"rotat", r"leak", r"env(?:ironment)? var"),
    ),
    Flaw(
        # The cap change is the problem; the _D -> _dec rename and the rewritten docstrings only cover it. A finding about
        # the rename alone is fair, but it is not this finding (it is counted as an extra the grader cannot judge).
        "scope-creep", "scope",
        ("src/remit/fees.py",),
        (("src/remit/fees.py", "total=min(base + surcharge, cap)"),),
        (r"express.{0,80}\bcap", r"\bcap\b.{0,80}express", r"surcharge.{0,80}\bcap", r"\bcap\b.{0,80}surcharge",
         r"min\(base", r"base \+ surcharge", r"\b165\b", r"price change", r"hard ceiling"),
    ),
    Flaw(
        "deleted-test", "tests",
        ("tests/test_fees.py",),
        (("tests/test_fees.py", "def test_the_fee_is_rounded_half_up_once"),),
        (r"delet", r"remov(?:ed|es|ing)", r"dropp?ed", r"missing test", r"no longer (?:exists|there)", r"express.{0,60}after.{0,20}cap",
         r"weaken", r"guard"),
    ),
)
FLAW_IDS = tuple(f.id for f in FLAWS)
LINE_TOLERANCE = 3  # "points at the right place" (the keyword route needs no line at all)
DELETED_TOLERANCE = 12  # a deleted test has no line of its own: its neighbours will do


# =================================================================================================
# 2. reading review.md
# =================================================================================================
@dataclass
class Finding:
    index: int
    title: str
    text: str
    files: list[str] = field(default_factory=list)  # repository paths, in order of appearance
    pairs: list[tuple[str, int]] = field(default_factory=list)  # (file, line) as written, e.g. fees.py:44
    lines: list[int] = field(default_factory=list)  # every line number mentioned in a Line field
    severity: str | None = None  # blocker | major | minor | nit
    line_given: bool = False  # a line number, or an explicit "-" / "n/a" for deleted code

    @property
    def complete(self) -> bool:
        return bool(self.files) and self.severity is not None and self.line_given


@dataclass
class Review:
    sections: dict[str, str]
    verdict: str
    findings: list[Finding]


_COMMENT = re.compile(r"<!--.*?-->", re.S)
_FILE = re.compile(
    r"(?<![\w/.-])([\w./-]*[\w-]\.(?:py|toml|md|txt|cfg|ini|yml|yaml|json))(?![\w-])(?:(?::|#L)(\d+)(?:\s*[-–]\s*L?(\d+))?)?"
)
_SEVERITY_FIELD = re.compile(r"(?i)severity\W{0,8}(blocker|critical|major|high|medium|minor|low|nit(?:pick)?|info)\b")
_SEVERITY_WORD = re.compile(r"(?i)\b(blocker|critical|major|minor|nit(?:pick)?)\b")
_LINE_FIELD = re.compile(r"(?i)\blines?\b\W{0,8}(\d+)(?:\s*(?:-|–|to)\s*(\d+))?")
_LINE_NONE = re.compile(r"(?i)\blines?\b\W{0,8}(?:-|–|n/?a|none|deleted|removed|whole file)(?![\w])")
_LIST_ITEM = re.compile(r"^(?:[-*+]|\d+[.)])\s+")


def resolve_path(token: str, known: Iterable[str]) -> str | None:
    """Map what the reviewer wrote (``fees.py``, ``src/remit/fees.py``, ``./tests/test_fees.py``) to a repository path."""
    token = token.strip("`*_ ").lstrip("./")
    known = list(known)
    if token in known:
        return token
    hits = sorted(k for k in known if k.endswith("/" + token))
    if len(hits) == 1:
        return hits[0]
    if hits:  # ambiguous basename: prefer the code over lab material
        code = [h for h in hits if h.startswith(("src/", "tests/"))]
        return code[0] if len(code) == 1 else None
    return None


def _blocks(text: str) -> tuple[str, list[tuple[str, str]]]:
    """(verdict text, [(title, body)]) for the findings in a review."""
    outline = checks.markdown_outline(text)
    sections = {s.title.lower(): s for s in outline}
    verdict = next((s.body for s in outline if "verdict" in s.title.lower()), "")
    start = next((i for i, s in enumerate(outline) if "finding" in s.title.lower() and s.level >= 2), None)
    if start is None:
        return verdict, []
    level = outline[start].level
    blocks: list[tuple[str, str]] = []
    for section in outline[start + 1:]:
        if section.level <= level:
            break
        blocks.append((section.title, section.body))
    if blocks:
        return verdict, blocks
    body = outline[start].body  # no sub-headings: a table or a list
    rows = [ln for ln in body.splitlines() if ln.strip().startswith("|")]
    rows = [ln for ln in rows if not re.fullmatch(r"[\s|:\-]+", ln)]
    if len(rows) >= 2:  # the first row is the header
        return verdict, [(f"row {i}", ln) for i, ln in enumerate(rows[1:], start=1)]
    items: list[list[str]] = []
    for ln in body.splitlines():
        if _LIST_ITEM.match(ln):
            items.append([ln])
        elif items and ln.strip():
            items[-1].append(ln)
    return verdict, [(f"item {i}", "\n".join(item)) for i, item in enumerate(items, start=1)]


def _finding(index: int, title: str, body: str, known: Sequence[str]) -> Finding:
    text = f"{title}\n{body}"
    finding = Finding(index, title.strip(), text)
    for match in _FILE.finditer(text):
        path = resolve_path(match.group(1), known)
        if path is None:
            continue
        if path not in finding.files:
            finding.files.append(path)
        if match.group(2):
            finding.pairs.append((path, int(match.group(2))))
            finding.line_given = True
    for match in _LINE_FIELD.finditer(text):
        first, last = int(match.group(1)), int(match.group(2) or match.group(1))
        finding.lines += [first, last]
        finding.line_given = True
        if finding.files:
            finding.pairs.append((finding.files[0], first))
    if _LINE_NONE.search(text):
        finding.line_given = True
    severity = _SEVERITY_FIELD.search(text) or _SEVERITY_WORD.search(text)
    if severity:
        finding.severity = SEVERITIES[severity.group(1).lower()]
    return finding


def parse_review(text: str, known_files: Iterable[str]) -> Review:
    """Parse the learner's review. Comments are ignored; findings are found under a "Findings" heading
    as sub-headings (the template), table rows or list items."""
    text = _COMMENT.sub("", text)
    known = list(known_files)
    verdict, blocks = _blocks(text)
    sections = checks.markdown_sections(text)
    findings = []
    for title, body in blocks:
        finding = _finding(len(findings) + 1, title, body, known)
        if finding.files or finding.severity:  # prose sub-sections ("Questions for the author") are not findings
            findings.append(finding)
            finding.index = len(findings)
    return Review(sections, verdict, findings)


VERDICT_BLOCKS = re.compile(r"(?i)request(?:ed)? changes|changes (?:are )?requested|reject|do not merge|don.t merge|block|not (?:ready|approved)|needs? (?:work|changes)")
VERDICT_APPROVES = re.compile(r"(?i)\bapprove[sd]?\b|\blgtm\b|ship it")


def verdict_blocks_merge(verdict: str) -> bool:
    """A verdict that asks for changes (or rejects). 'approve with comments' and plain 'approve' do not."""
    text = re.sub(r"(?i)approve with comments", "approve", verdict)
    if VERDICT_BLOCKS.search(text):
        return not re.search(r"(?i)^\W*(?:approve|lgtm)\b", text.strip())
    return False


# -- matching findings to the seeded problems ----------------------------------------------------------
def flaw_lines(work: Path | str, ref: str = gitutil.TAG_START) -> dict[str, dict[str, list[int]]]:
    """For each flaw, {file: [line numbers of its markers]} in the starting branch (1-based)."""
    cache: dict[str, list[str]] = {}
    found: dict[str, dict[str, list[int]]] = {}
    for flaw in FLAWS:
        found[flaw.id] = {}
        for path, marker in flaw.markers:
            if path not in cache:
                cache[path] = (gitutil.file_at(work, ref, path) or "").splitlines()
            for number, line in enumerate(cache[path], start=1):
                if marker in line:
                    found[flaw.id].setdefault(path, []).append(number)
    return found


def _score(finding: Finding, flaw: Flaw, lines: dict[str, list[int]]) -> int:
    """0 means no match. Otherwise higher is better: line, keywords and file all count."""
    file_ok = any(f in flaw.files for f in finding.files)
    if not file_ok:
        return 0
    tolerance = DELETED_TOLERANCE if flaw.id == "deleted-test" else LINE_TOLERANCE
    distances = [abs(number - marker) for path, number in finding.pairs if path in lines for marker in lines[path]]
    distance = min(distances) if distances else None
    near = distance is not None and distance <= tolerance
    words = sum(1 for rx in flaw.keywords if re.search(rx, finding.text, re.I))
    if not near and words == 0:
        return 0
    first = 1 if finding.files and finding.files[0] in flaw.files else 0
    closeness = max(0, 3 - distance) if near else 0  # two flaws a few lines apart: the nearer one wins
    return 4 * near + closeness + 2 * min(words, 3) + 1 + first


@dataclass
class Matches:
    found: dict[str, Finding]  # flaw id -> the finding that covers it
    extra: list[Finding]  # findings that match no seeded problem (they may still be fair)

    @property
    def count(self) -> int:
        return len(self.found)


def match_findings(findings: Sequence[Finding], lines: dict[str, dict[str, list[int]]]) -> Matches:
    """Pair findings with flaws, best score first, each finding and each flaw used at most once."""
    pairs = []
    for finding in findings:
        for order, flaw in enumerate(FLAWS):
            score = _score(finding, flaw, lines.get(flaw.id, {}))
            if score:
                pairs.append((-score, order, finding.index, flaw, finding))
    pairs.sort(key=lambda p: p[:3])
    found: dict[str, Finding] = {}
    used: set[int] = set()
    for _, _, _, flaw, finding in pairs:
        if flaw.id in found or finding.index in used:
            continue
        found[flaw.id] = finding
        used.add(finding.index)
    return Matches(found, [f for f in findings if f.index not in used])


def under_rated(matches: Matches) -> list[str]:
    """Flaw ids whose finding is rated lower than the risk deserves."""
    by_id = {f.id: f for f in FLAWS}
    return [fid for fid, finding in matches.found.items()
            if finding.severity is None or RANK[finding.severity] < RANK[by_id[fid].min_severity]]


def over_rated(matches: Matches) -> list[str]:
    """Flaw ids whose finding is rated higher than the risk deserves (a test too weak to fail is not a blocker)."""
    by_id = {f.id: f for f in FLAWS}
    return [fid for fid, finding in matches.found.items()
            if finding.severity is not None and RANK[finding.severity] > RANK[by_id[fid].max_severity]]


FLAT_MIN = 5  # a review of at least this many rated findings that are all blockers has not ranked anything


def all_blockers(findings: Sequence[Finding]) -> bool:
    """Every rated finding is a blocker: 'if everything is urgent, nothing is'."""
    rated = [f.severity for f in findings if f.severity]
    return len(rated) >= FLAT_MIN and all(severity == "blocker" for severity in rated)


# =================================================================================================
# 3. static checks on the fixed branch
# =================================================================================================
def _py_files(work: Path | str, folder: str) -> list[Path]:
    base = Path(work) / folder
    return sorted(p for p in base.rglob("*.py") if "__pycache__" not in p.parts and "_hidden" not in p.parts) if base.is_dir() else []


def _parse(path: Path) -> ast.AST | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return None


def _rel(work: Path | str, path: Path) -> str:
    return path.relative_to(Path(work)).as_posix()


def import_problems(work: Path | str) -> list[str]:
    """Imports of anything that is not the standard library, Remit or najmkit (tests may also use pytest),
    plus a changed dependency list in pyproject.toml or a new requirements file."""
    problems: list[str] = []
    base = set(sys.stdlib_module_names) | {"remit", "najmkit"}
    for folder, allowed in (("src", base), ("tests", base | {"pytest", "conftest", "_pytest"})):
        for path in _py_files(work, folder):
            tree = _parse(path)
            if tree is None:
                continue
            for node in ast.walk(tree):
                names = []
                if isinstance(node, ast.Import):
                    names = [a.name.split(".")[0] for a in node.names]
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    names = [node.module.split(".")[0]]
                for name in names:
                    if name not in allowed:
                        problems.append(f"{name} imported in {_rel(work, path)}")
    try:
        data = tomllib.loads((Path(work) / "pyproject.toml").read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        problems.append("pyproject.toml cannot be read")
        data = {}
    project = data.get("project", {})
    if project.get("dependencies", []) != []:
        problems.append("pyproject.toml lists runtime dependencies")
    if project.get("optional-dependencies", {}) != {"dev": ["pytest"]}:
        problems.append("pyproject.toml changes the optional dependencies")
    for extra in sorted(Path(work).glob("requirements*.txt")):
        problems.append(f"{extra.name} added")
    return sorted(set(problems))


def _is_broad(handler: ast.ExceptHandler) -> bool:
    def broad(node: ast.expr | None) -> bool:
        if node is None:
            return True
        if isinstance(node, ast.Name):
            return node.id in {"Exception", "BaseException"}
        if isinstance(node, ast.Tuple):
            return any(broad(e) for e in node.elts)
        return False

    return broad(handler.type)


def broad_except_problems(work: Path | str) -> list[str]:
    """``except:`` / ``except Exception:`` handlers in src/ that do not re-raise (the repo catches specific errors)."""
    problems = []
    for path in _py_files(work, "src"):
        tree = _parse(path)
        if tree is None:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and _is_broad(node) and not any(isinstance(n, ast.Raise) for n in ast.walk(node)):
                problems.append(f"{_rel(work, path)}:{node.lineno}")
    return problems


MONEYISH = re.compile(r"(?i)money|decimal|amount|fee|rate|discount|price|total|base|surcharge|tier|silver|gold|percent|cent|qar|"
                      r"\bcap\b|minimum|balance|ledger|loyalty|charge|pay")


def _scopes(tree: ast.Module) -> Iterable[ast.stmt]:
    """The units a float literal is judged in: a module-level statement, a function, a method."""
    for top in tree.body:
        if isinstance(top, ast.ClassDef):
            yield from top.body
        else:
            yield top


def _identifiers(node: ast.AST) -> str:
    names = []
    for item in ast.walk(node):
        if isinstance(item, ast.Name):
            names.append(item.id)
        elif isinstance(item, ast.Attribute):
            names.append(item.attr)
        elif isinstance(item, ast.arg):
            names.append(item.arg)
        elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.append(item.name)
    return " ".join(names)


def float_problems(work: Path | str) -> list[str]:
    """``float()`` calls anywhere in the code that handles money (everything in src/remit except money.py, which mentions
    float only to refuse it), and float literals in any unit of code whose names talk about money (rates, fees, amounts...).
    A float that has nothing to do with money (a timeout, say) is not a finding."""
    found: dict[tuple[str, int, str], None] = {}
    for path in _py_files(work, "src/remit"):
        if path.name == "money.py":
            continue
        tree = _parse(path)
        if not isinstance(tree, ast.Module):
            continue
        for scope in _scopes(tree):
            about_money = bool(MONEYISH.search(_identifiers(scope)))
            for node in ast.walk(scope):
                if about_money and isinstance(node, ast.Constant) and type(node.value) is float:
                    found[(_rel(work, path), node.lineno, "float literal")] = None
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "float":
                    found[(_rel(work, path), node.lineno, "float()")] = None
    return [f"{kind} in {rel}:{line}" for rel, line, kind in sorted(found)]


def _test_functions(tree: ast.AST) -> Iterable[ast.FunctionDef | ast.AsyncFunctionDef]:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
            yield node


def _asserts(function: ast.AST) -> bool:
    for node in ast.walk(function):
        if isinstance(node, ast.Assert):
            return True
        if isinstance(node, ast.Call):
            func = node.func
            name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ""
            if name.lower().startswith("assert") or name in {"raises", "warns", "fail", "deprecated_call"}:
                return True
    return False


def list_test_files(work: Path | str) -> list[Path]:
    return [p for p in _py_files(work, "tests") if p.name.startswith("test_")]


def unasserted_tests(work: Path | str) -> list[str]:
    """Test functions with no assertion: no ``assert``, no ``pytest.raises``, no ``assert_*`` call, and no call to a helper
    defined in the same file that asserts."""
    problems = []
    for path in list_test_files(work):
        tree = _parse(path)
        if tree is None:
            continue
        helpers = {n.name for n in ast.walk(tree)
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and not n.name.startswith("test") and _asserts(n)}
        for function in _test_functions(tree):
            calls = {c.func.id for c in ast.walk(function) if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)}
            calls |= {c.func.attr for c in ast.walk(function) if isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute)}
            if not _asserts(function) and not (calls & helpers):
                problems.append(f"{_rel(work, path)}::{function.name}")
    return problems


FAKED = ("fees", "loyalty", "quote_fee", "explain_fee", "discount")
_PATCHERS = {"patch", "setattr", "object", "dict", "multiple"}


def faked_fee_code(work: Path | str) -> list[str]:
    """Tests that patch or monkeypatch the fee code (patch(...), patch.object(...), monkeypatch.setattr(...))."""
    problems = []
    for path in list_test_files(work):
        tree = _parse(path)
        if tree is None:
            continue
        for function in _test_functions(tree):
            for node in ast.walk(function):
                if not isinstance(node, ast.Call):
                    continue
                func = node.func
                name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ""
                chain = ast.unparse(func)
                if name not in _PATCHERS or not ("patch" in chain or "monkeypatch" in chain or "mocker" in chain):
                    continue
                if name == "dict" and "environ" in ast.unparse(node):
                    continue
                target = " ".join(ast.unparse(a) for a in node.args[:2]).lower()
                if any(word in target for word in FAKED):
                    problems.append(f"{_rel(work, path)}::{function.name}")
                    break
    return sorted(set(problems))


def list_test_names(work: Path | str, ref: str | None = None) -> set[str]:
    """Names of all test functions in the working tree, or at git ``ref`` when given."""
    names: set[str] = set()
    if ref is None:
        for path in list_test_files(work):
            tree = _parse(path)
            if tree is not None:
                names |= {f.name for f in _test_functions(tree)}
        return names
    listing = gitutil.git(work, "ls-tree", "-r", "--name-only", ref, "--", "tests", check=False).stdout.splitlines()
    for rel in listing:
        if rel.endswith(".py") and Path(rel).name.startswith("test_"):
            source = gitutil.file_at(work, ref, rel) or ""
            try:
                tree = ast.parse(source)
            except SyntaxError:
                continue
            names |= {f.name for f in _test_functions(tree)}
    return names


def _fingerprint(function: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """The body of a test as a tree, without its docstring: the same test under another name has the same fingerprint."""
    body = list(function.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        body = body[1:]
    return "\n".join(ast.dump(statement) for statement in body)


def _tests(work: Path | str, ref: str | None) -> list[tuple[str, str]]:
    """(name, body fingerprint) of every test function in the working tree, or at git ``ref`` when given."""
    sources: list[str] = []
    if ref is None:
        sources = [path.read_text(encoding="utf-8", errors="replace") for path in list_test_files(work)]
    else:
        listing = gitutil.git(work, "ls-tree", "-r", "--name-only", ref, "--", "tests", check=False).stdout.splitlines()
        sources = [gitutil.file_at(work, ref, rel) or "" for rel in listing if rel.endswith(".py") and Path(rel).name.startswith("test_")]
    found = []
    for source in sources:
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        found += [(f.name, _fingerprint(f)) for f in _test_functions(tree)]
    return found


def missing_tests(work: Path | str, base: str = "main") -> list[str]:
    """Tests that exist on ``base`` and are gone now. A test is *not* missing when a test with the same name is still there,
    or when its body survives under another name (restored, but renamed): the check is about the evidence, not the label."""
    if not gitutil.has_ref(work, base):
        return []
    now = _tests(work, None)
    names = {name for name, _ in now}
    bodies = {body for _, body in now}
    return sorted({name for name, body in _tests(work, base) if name not in names and body not in bodies})


def failing_on_original(work: Path | str, since: str = gitutil.TAG_START, timeout: float = 60.0) -> tuple[int, int]:
    """(how many of the learner's new or changed tests FAIL, how many new or changed test files there are) when every
    non-test file is put back to how the agent left it. Errors do not count: a test that cannot even be imported on the
    agent's code proves nothing. A good fix leaves tests behind that would have caught the agent's bugs."""
    work = Path(work)
    chosen = checks.new_test_files(work, since)
    if not chosen:
        return 0, 0
    with checks.work_copy(work) as root:
        for path, state in gitutil.changed_status(work, since, ignore=()).items():
            if gitutil.glob_match(path, ["tests/**"]):
                continue
            target = root / path
            original = None if state == "A" else gitutil.show_bytes(work, since, path)
            if original is None:
                target.unlink(missing_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(original)
        chosen = [p for p in chosen if (root / p).exists()]
        result = checks._run_pytest_in(root, chosen, timeout=timeout, args=(), extra_env=None)  # noqa: SLF001 (kit-internal helper)
    return (0 if result.timed_out else result.failed), len(chosen)


# -- the leaked key ---------------------------------------------------------------------------------------------------------
KEY_SHAPE = re.compile(r"najm-loy-[A-Za-z0-9_-]{8,}")  # what the agent committed: the prefix alone (najm-loy-) is not the key
_ENV_READERS = {"os.environ.get", "os.getenv", "environ.get", "getenv"}
_SECRET_NAME = re.compile(r"(?i)key|token|secret|passw|credential")
_PLACEHOLDER = re.compile(r"(?i)change.?me|your[_-]|example|placeholder|dummy|fake|x{4,}|\*{3,}|<[^>]+>|\$\{|%\(|test")
_KEY_IGNORE = ("TASK.md", "lab-assets/**", "**/__pycache__/**", "**/*.pyc", ".pytest_cache/**", ".claude/settings.local.json")


def _text(node: ast.AST) -> str | None:
    """The value of a string built only from literals: 'a', 'a' + 'b', f'a{...}' is not (None)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = _text(node.left), _text(node.right)
        return left + right if left is not None and right is not None else None
    if isinstance(node, ast.JoinedStr) and all(isinstance(v, ast.Constant) for v in node.values):
        return "".join(str(v.value) for v in node.values)  # type: ignore[attr-defined]
    return None


def leaked_key_problems(work: Path | str, since: str = gitutil.TAG_START) -> list[str]:
    """Where the key the agent committed (or anything shaped like it) still is, and secrets with a hard-coded fallback.

    Looks in every file of the repository, review.md included (a review is shared text: refer to a secret by file and line),
    and sees through ``'najm-loy-' + 'live-...'``. Reports file:line and never the value."""
    work = Path(work)
    original = re.search(r"LOYALTY_API_KEY\s*=\s*[\"']([^\"']+)", gitutil.file_at(work, since, "src/remit/loyalty.py") or "")
    exact = original.group(1) if original else None
    hits: dict[str, None] = {}

    def leaked(text: str) -> bool:
        return bool(KEY_SHAPE.search(text)) or bool(exact and exact in text)

    names = sorted(set(gitutil.out(work, "ls-files").splitlines()) | set(gitutil.changed_files(work, since, ignore=())))
    for rel in names:
        path = work / rel
        if gitutil.glob_match(rel, _KEY_IGNORE) or not path.is_file():
            continue
        data = path.read_bytes()
        if b"\0" in data[:8000] or len(data) > 2_000_000:
            continue
        text = data.decode("utf-8", errors="replace")
        for number, line in enumerate(text.splitlines(), start=1):
            if leaked(line):
                hits[f"the old key is still in {rel}:{number}"] = None
        if rel.endswith(".py"):
            tree = _parse(path)
            for node in ast.walk(tree) if tree else ():
                value = _text(node) if isinstance(node, (ast.BinOp, ast.JoinedStr)) else None
                if value is not None and leaked(value):
                    hits[f"the old key is still in {rel}:{node.lineno}"] = None
                if isinstance(node, ast.Call) and ast.unparse(node.func) in _ENV_READERS and len(node.args) >= 1:
                    var = _text(node.args[0]) or ""
                    default = _text(node.args[1]) if len(node.args) > 1 else next(
                        (_text(k.value) for k in node.keywords if k.arg == "default"), None)
                    if _SECRET_NAME.search(var) and default and len(default) >= 8 and not _PLACEHOLDER.search(default):
                        hits[f"a secret has a hard-coded fallback in {rel}:{node.lineno}"] = None
    return list(hits)  # one report per place: the plain-text scan and the tree scan can find the same line
