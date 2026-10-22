"""Grader helpers for lab m07 (lesson 7.2): "tame an untested module, refactor it, then migrate a dependency".

Everything here reads the learner's work directory and never imports or executes it in the grader's own
process: code is parsed with ``ast`` or run in a subprocess with a timeout (``runner``), always on a
throw-away copy. The helpers are written for this lab only; the generic ones live in ``checks``.

What is checked here
--------------------
* ``module_state_problems``      the ledger keeps no state at module level (and nobody else started to)
* ``legacy_functions_left``      the old module-level ledger functions are gone
* ``v1_calls_left``              no call to najmkit's v1 names remains in ``src/remit`` or ``tests`` (import aware)
* ``v1_names_still_defined``     the deprecated v1 names are gone from the vendored najmkit (subprocess import)
* ``characterization_report``    the learner's ``tests/test_ledger*.py`` pass on the ORIGINAL ledger and kill mutants of it
* ``green_commits``              each commit since the start leaves the whole suite green
* ``tests_not_deleted``          no test of the starter was deleted
"""
from __future__ import annotations

import ast
import io
import json
import re
import shutil
import subprocess
import tarfile
import tempfile
from collections.abc import Iterable, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

from ailab import checks, gitutil, runner
from ailab.checks import Mutant

LEDGER = "src/remit/ledger.py"
LEGACY_FUNCTIONS = ("post_transfer", "balance", "accounts", "journal", "reset")
V1_NAMES = {
    "ids": ("new_id", "use_generator"),
    "clock": ("now", "set_clock", "get_clock", "reset_clock"),
    "audit": ("log_event",),
}

# The deliberate defects of the ORIGINAL ledger (src/remit/ledger.py as it is at lab-start). Each ``old`` text must occur
# exactly once there: tests/test_labs_m07.py checks that, so a changed base fails loudly. Descriptions name behaviour.
MUTANTS: tuple[Mutant, ...] = (
    Mutant("M01", LEDGER, "rounding=ROUND_HALF_EVEN)  # Q-LED-1", 'rounding="ROUND_HALF_UP")  # Q-LED-1',
           "the partner's share is rounded half-even, not half-up"),
    Mutant("M02", LEDGER, 'PARTNER_SHARE = Decimal("0.30")', 'PARTNER_SHARE = Decimal("0.35")',
           "the partner's share is 30% of the fee"),
    Mutant("M03", LEDGER, "    if account not in _BALANCES:\n        _BALANCES[account] = Decimal(\"0\")\n    return _BALANCES[account]",
           "    return _BALANCES.get(account, Decimal(\"0\"))",
           "asking for the balance of an unknown account creates it"),
    Mutant("M04", LEDGER, 'if any(e["transfer_id"] == transfer_id for e in _JOURNAL):', "if False:",
           "posting the same transfer twice is refused"),
    Mutant("M05", LEDGER, "    if income:\n", "    if True:\n", "a zero fee income is not posted as a zero-amount leg"),
    Mutant("M06", LEDGER, 'sign = 1 if side == "C" else -1', 'sign = 1 if side == "D" else -1',
           "a balance is credits minus debits"),
    Mutant("M07", LEDGER, 'if send_amount.currency != "QAR" or fee.currency != "QAR":', 'if send_amount.currency != "QAR":',
           "a fee in another currency is refused"),
    Mutant("M08", LEDGER, 'send_amount <= Money.zero("QAR")', 'send_amount < Money.zero("QAR")',
           "a zero send amount is refused"),
    Mutant("M09", LEDGER, 'if send_amount <= Money.zero("QAR") or fee.is_negative():', 'if send_amount <= Money.zero("QAR"):',
           "a negative fee is refused"),
    Mutant("M10", LEDGER, "return sorted(_BALANCES)", "return list(_BALANCES)", "accounts() are listed in alphabetical order"),
    Mutant("M11", LEDGER, "return list(_JOURNAL)", "return _JOURNAL", "journal() hands out a copy of the list"),
    Mutant("M12", LEDGER, '"D", send_amount.amount + fee.amount)', '"D", send_amount.amount)',
           "the customer is debited the send amount plus the fee"),
    Mutant("M13", LEDGER, "income = fee.amount - partner", 'income = (fee.amount * Decimal("0.70")).quantize(_CENT)',
           "the fee income is whatever is left after the partner's share"),
    Mutant("M14", LEDGER, 'ids.new_id("JNL")', 'ids.new_id("JRN")', "journal entry ids start with JNL-"),
    Mutant("M15", LEDGER, "clock.now().isoformat()", "clock.now().date().isoformat()",
           "each entry records the full time it was posted"),
    Mutant("M16", LEDGER, 'return f"CUSTOMER:{customer_id}"', 'return f"CUST:{customer_id}"',
           "the customer's account is named CUSTOMER:<id>"),
)
MIN_KILLED = 13  # of 16: a good suite catches nearly everything; the survivors are named in the detail


# =================================================================================
# 1. static checks on the refactored code (ast only)
# =================================================================================
_MUTABLE_CALLS = {"dict", "list", "set", "defaultdict", "deque", "OrderedDict", "Counter", "bytearray", "ChainMap"}
_CONSTANT_CALLS = {"Decimal", "frozenset", "tuple", "str", "int", "float", "bool", "bytes", "timedelta", "compile", "getLogger",
                   "TypeVar", "NewType", "namedtuple", "MappingProxyType", "Path"}


def _call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


def _is_mutable_value(node: ast.AST) -> bool:
    if isinstance(node, (ast.List, ast.Dict, ast.Set, ast.ListComp, ast.DictComp, ast.SetComp)):
        return True
    return isinstance(node, ast.Call) and _call_name(node) in _MUTABLE_CALLS


def _is_constant_expr(node: ast.AST) -> bool:
    """A value that cannot hold state: literals, tuples of them, Decimal(...), names and attributes of constants,
    type aliases such as ``dict[str, Any]`` and lambdas."""
    if isinstance(node, (ast.Constant, ast.Name, ast.JoinedStr, ast.Lambda)):
        return True
    if isinstance(node, ast.Attribute):
        return _is_constant_expr(node.value)
    if isinstance(node, ast.Subscript):  # a type alias: Entry = dict[str, Any]
        return _is_constant_expr(node.value) and _is_constant_expr(node.slice)
    if isinstance(node, ast.Tuple):
        return all(_is_constant_expr(e) for e in node.elts)
    if isinstance(node, ast.UnaryOp):
        return _is_constant_expr(node.operand)
    if isinstance(node, ast.BinOp):
        return _is_constant_expr(node.left) and _is_constant_expr(node.right)
    if isinstance(node, ast.Call) and _call_name(node) in _CONSTANT_CALLS:
        def fine(arg: ast.AST) -> bool:
            if isinstance(arg, (ast.List, ast.Set)):
                return all(_is_constant_expr(e) for e in arg.elts)
            if isinstance(arg, ast.Dict):  # MappingProxyType({...}): a read-only view
                return all(k is not None and _is_constant_expr(k) for k in arg.keys) and all(_is_constant_expr(v) for v in arg.values)
            return _is_constant_expr(arg)

        return all(fine(a) for a in node.args) and all(fine(k.value) for k in node.keywords)
    return False


# A lookup table such as ``_SIGN = {"C": 1, "D": -1}`` is a mutable container, but it holds no state unless the module changes it.
_MUTATING_METHODS = {"append", "extend", "insert", "remove", "pop", "popitem", "clear", "update", "setdefault", "add", "discard", "sort",
                     "reverse", "difference_update", "intersection_update", "symmetric_difference_update"}


def _is_literal_table(node: ast.AST) -> bool:
    """A NON-EMPTY dict, list or set literal whose members are all constants (or nested tables of constants)."""
    def member(n: ast.AST) -> bool:
        return _is_constant_expr(n) or _is_literal_table(n)

    if isinstance(node, ast.Dict):
        return bool(node.keys) and all(k is not None and member(k) for k in node.keys) and all(member(v) for v in node.values)
    if isinstance(node, (ast.List, ast.Set)):
        return bool(node.elts) and all(member(e) for e in node.elts)
    return False


def _mutated_names(tree: ast.Module) -> set[str]:
    """Names (and attribute names) that the code changes in place: ``x[k] = v``, ``del x[k]``, ``x += ...``, ``x.append(...)``,
    ``global x``. A heuristic: aliases are not followed (the hidden suite checks that two ledgers really are independent)."""
    names: set[str] = set()

    def base_names(target: ast.AST) -> None:
        while isinstance(target, (ast.Subscript, ast.Attribute)):
            if isinstance(target, ast.Attribute):
                names.add(target.attr)
            target = target.value
        if isinstance(target, ast.Name):
            names.add(target.id)

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, (ast.Subscript, ast.Attribute)):
                    base_names(target)
        elif isinstance(node, (ast.AugAssign, ast.AnnAssign)):
            base_names(node.target)
        elif isinstance(node, ast.Delete):
            for target in node.targets:
                base_names(target)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in _MUTATING_METHODS:
            base_names(node.func.value)
        elif isinstance(node, ast.Global):
            names.update(node.names)
    return names


def _holds_state(value: ast.AST, names: Sequence[str], mutated: set[str]) -> bool:
    """A mutable container is state, unless it is a filled-in lookup table that nothing in the module changes."""
    return _is_mutable_value(value) and not (_is_literal_table(value) and not set(names) & mutated)


def _dunder(names: Sequence[str]) -> bool:
    return bool(names) and all(n.startswith("__") and n.endswith("__") for n in names)


def _targets(node: ast.stmt) -> list[str]:
    if isinstance(node, ast.Assign):
        return [t.id for t in node.targets if isinstance(t, ast.Name)]
    if isinstance(node, (ast.AnnAssign, ast.AugAssign)) and isinstance(node.target, ast.Name):
        return [node.target.id]
    return []


def _module_statements(tree: ast.Module) -> Iterable[ast.stmt]:
    """Top-level statements, looking inside top-level if/try/with blocks (they are still module level)."""
    stack = list(tree.body)
    while stack:
        node = stack.pop(0)
        yield node
        if isinstance(node, (ast.If, ast.Try, ast.With)):
            stack = [*node.body, *getattr(node, "orelse", []), *getattr(node, "finalbody", []), *stack]


def module_state_problems(source: str, filename: str = "ledger.py") -> list[str]:
    """Reasons why a module keeps state at module level or in shared class attributes. Empty means it does not."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [f"{filename} does not parse (line {exc.lineno})"]
    problems: list[str] = []
    mutated = _mutated_names(tree)
    for node in _module_statements(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            value = getattr(node, "value", None)
            names = _targets(node)
            if _dunder(names):  # __all__, __version__ and friends
                continue
            if isinstance(node, ast.AugAssign):
                problems.append(f"{filename} line {node.lineno}: `{', '.join(names) or '...'}` is changed at module level")
            elif value is not None and not _is_constant_expr(value):
                if _is_mutable_value(value) and not _holds_state(value, names, mutated):
                    continue  # a lookup table nobody changes
                kind = "a mutable container" if _is_mutable_value(value) else "an object created at import time"
                problems.append(f"{filename} line {node.lineno}: module-level `{', '.join(names) or '...'}` holds {kind}")
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            problems.append(f"{filename} line {node.lineno}: a call is executed at import time")
    for node in ast.walk(tree):
        if isinstance(node, ast.Global):
            problems.append(f"{filename} line {node.lineno}: `global {', '.join(node.names)}` rebinds module state")
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                value = getattr(item, "value", None)
                if (isinstance(item, (ast.Assign, ast.AnnAssign)) and value is not None
                        and _holds_state(value, _targets(item), mutated)):
                    problems.append(f"{filename} line {item.lineno}: class attribute `{', '.join(_targets(item))}` is a mutable "
                                    "container shared by every instance")
    return problems


def legacy_functions_left(source: str) -> list[str]:
    """Names of the old module-level ledger functions that are still defined at module level."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    found = [n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in LEGACY_FUNCTIONS]
    for node in tree.body:
        found += [t for t in _targets(node) if t in LEGACY_FUNCTIONS]
    return sorted(set(found))


def mutable_module_names(source: str) -> set[str]:
    """Module-level names bound to mutable containers (for 'did anyone else start keeping state?')."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    names: set[str] = set()
    mutated = _mutated_names(tree)
    for node in _module_statements(tree):
        value = getattr(node, "value", None)
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and value is not None and _holds_state(value, _targets(node), mutated):
            names.update(_targets(node))
    return names


def new_module_state(work: Path | str, root: str = "src/remit") -> list[str]:
    """Mutable module-level names that exist now in ``root`` but did not at lab-start (ledger.py is judged separately)."""
    work = Path(work)
    found: list[str] = []
    for path in sorted((work / root).rglob("*.py")):
        rel = path.relative_to(work).as_posix()
        if rel == LEDGER:
            continue
        before = gitutil.file_at(work, gitutil.TAG_START, rel)
        old = mutable_module_names(before) if before is not None else set()
        now = mutable_module_names(path.read_text(encoding="utf-8"))
        found += [f"{rel}: `{name}`" for name in sorted(now - old)]
    return found


# =================================================================================
# 2. the najmkit migration: static scan (import aware) and a subprocess import
# =================================================================================
class _V1Finder(ast.NodeVisitor):
    def __init__(self) -> None:
        self.aliases: dict[str, str] = {}  # local name -> najmkit module name (ids, clock, audit)
        self.hits: list[tuple[int, str]] = []
        self._shadow: list[set[str]] = []  # parameter names of the functions we are inside

    def visit_Import(self, node: ast.Import) -> None:
        for item in node.names:
            parts = item.name.split(".")
            if parts[0] == "najmkit" and len(parts) == 2 and parts[1] in V1_NAMES:
                self.aliases[item.asname or parts[1]] = parts[1]

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module == "najmkit":
            for item in node.names:
                if item.name in V1_NAMES:
                    self.aliases[item.asname or item.name] = item.name
        elif node.module and node.module.startswith("najmkit."):
            module = node.module.split(".", 1)[1]
            for item in node.names:
                if item.name in V1_NAMES.get(module, ()):
                    self.hits.append((node.lineno, f"from {node.module} import {item.name}"))

    def _function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        args = node.args
        names = {a.arg for a in [*args.posonlyargs, *args.args, *args.kwonlyargs]}
        names |= {n.id for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}  # locals
        self._shadow.append(names)
        self.generic_visit(node)
        self._shadow.pop()

    visit_FunctionDef = _function
    visit_AsyncFunctionDef = _function

    def visit_Attribute(self, node: ast.Attribute) -> None:
        base = node.value
        if isinstance(base, ast.Name) and base.id in self.aliases and not any(base.id in s for s in self._shadow):
            module = self.aliases[base.id]
            if node.attr in V1_NAMES[module]:
                self.hits.append((node.lineno, f"{base.id}.{node.attr}"))
        elif (isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name) and base.value.id == "najmkit"
              and base.attr in V1_NAMES and node.attr in V1_NAMES[base.attr]):
            self.hits.append((node.lineno, f"najmkit.{base.attr}.{node.attr}"))
        self.generic_visit(node)


def v1_calls_left(work: Path | str, roots: Sequence[str] = ("src/remit", "tests")) -> list[str]:
    """Uses of najmkit's v1 names in ``roots`` (``file:line name``). The injected clock objects' ``.now()`` is not one."""
    work = Path(work)
    found: list[str] = []
    for root in roots:
        for path in sorted((work / root).rglob("*.py")):
            rel = path.relative_to(work).as_posix()
            if "_hidden" in path.parts or "__pycache__" in path.parts:
                continue
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except (SyntaxError, UnicodeDecodeError):
                continue
            finder = _V1Finder()
            finder.visit(tree)
            found += [f"{rel}:{line} {what}" for line, what in sorted(finder.hits)]
    return found


_PROBE = """
import json
import najmkit.audit as audit, najmkit.clock as clock, najmkit.ids as ids
mods = {"ids": ids, "clock": clock, "audit": audit}
print(json.dumps([f"{m}.{n}" for m, names in %r.items() for n in names if hasattr(mods[m], n)]))
""" % V1_NAMES


def v1_names_still_defined(work: Path | str, *, timeout: float = 20.0) -> list[str] | None:
    """The v1 names najmkit still defines (imports the learner's najmkit in a subprocess). None if it cannot be imported."""
    with checks.work_copy(work) as root:
        result = runner.run_python(["-c", _PROBE], cwd=root, pythonpath=[root / "src"], timeout=timeout)
    if not result.ok:
        return None
    try:
        return list(json.loads(result.stdout.strip().splitlines()[-1]))
    except (ValueError, IndexError):
        return None


# =================================================================================
# 3. the learner's characterization tests, judged on the ORIGINAL code
# =================================================================================
def starter_tree(work: Path | str, dest: Path, ref: str = gitutil.TAG_START) -> Path:
    """Extract ``ref`` (default: the lab-start tag) of the learner's repository into ``dest`` with ``git archive``."""
    proc = subprocess.run(["git", "archive", "--format=tar", ref], cwd=str(work), capture_output=True, check=True,
                          env=runner.clean_env())
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as archive:
        try:
            archive.extractall(dest, filter="data")  # Python 3.11.4+ and 3.12+
        except TypeError:  # an older 3.11: the archive is our own `git archive`, not untrusted input
            archive.extractall(dest)  # noqa: S202
    return dest


def ledger_test_files(work: Path | str) -> tuple[list[str], list[str]]:
    """(characterization test files, support files) the learner ADDED under tests/: ``tests/test_ledger*.py`` and any
    other new non-test ``.py`` file (the adapter). ``tests/conftest.py`` is never one of them."""
    status = gitutil.changed_status(Path(work))
    tests, support = [], []
    for path, state in status.items():
        if state != "A" or not path.startswith("tests/") or not path.endswith(".py") or "_hidden" in path:
            continue
        name = path.rsplit("/", 1)[-1]
        if name == "conftest.py":
            continue
        if re.fullmatch(r"test_ledger[\w]*\.py", name):
            tests.append(path)
        elif not name.startswith("test_"):
            support.append(path)
    return sorted(tests), sorted(support)


def count_tests(work: Path | str, files: Sequence[str]) -> int:
    """Number of ``def test_*`` functions (a parametrized test counts once) in ``files``."""
    total = 0
    for rel in files:
        try:
            tree = ast.parse((Path(work) / rel).read_text(encoding="utf-8"))
        except (OSError, SyntaxError, UnicodeDecodeError):
            continue
        total += sum(1 for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test_"))
    return total


@dataclass
class CharacterizationReport:
    tests: list[str] = field(default_factory=list)
    n_tests: int = 0
    baseline_ok: bool = False
    baseline_detail: str = ""
    killed: list[Mutant] = field(default_factory=list)
    survived: list[Mutant] = field(default_factory=list)
    not_applied: list[Mutant] = field(default_factory=list)


def _pytest(root: Path, targets: Sequence[str], *, stop_first: bool, timeout: float) -> runner.RunResult:
    args = ["-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", "-W", "ignore::DeprecationWarning"]
    if stop_first:
        args.append("-x")
    return runner.run_python([*args, *targets], cwd=root, pythonpath=[root / "src"], timeout=timeout)


def characterization_report(work: Path | str, mutants: Sequence[Mutant] = MUTANTS, *, timeout: float = 30.0,
                            workers: int = 4) -> CharacterizationReport:
    """Run the learner's new ``tests/test_ledger*.py`` against the ORIGINAL repository, then against each mutant of it.

    The original is rebuilt from the ``lab-start`` tag, so the learner's tests must work on the code as it was before
    the refactor (that is what makes them characterization tests). ``tests/conftest.py`` is the original one too."""
    work = Path(work)
    tests, support = ledger_test_files(work)
    report = CharacterizationReport(tests=tests, n_tests=count_tests(work, tests))
    if not tests:
        report.baseline_detail = "no tests/test_ledger*.py file was added"
        return report
    with tempfile.TemporaryDirectory(prefix="ailab-m07-") as scratch:
        base = starter_tree(work, Path(scratch) / "base")
        for rel in [*tests, *support]:
            target = base / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(work / rel, target)
        first = _pytest(base, tests, stop_first=False, timeout=timeout * 2)
        report.baseline_ok = first.ok and "passed" in first.output
        if not report.baseline_ok:
            if first.timed_out:
                report.baseline_detail = "they did not finish in time"
            else:
                names = re.findall(r"^(?:FAILED|ERROR) (\S+)", first.output, flags=re.M)
                tail = first.output.strip().splitlines()[-1] if first.output.strip() else "no output"
                report.baseline_detail = tail + (f": {checks._short([n.split('::')[-1] for n in names], 3)}" if names else "")
            return report

        def try_mutant(mutant: Mutant) -> tuple[Mutant, str]:
            path = base / mutant.file
            original = path.read_text(encoding="utf-8")
            if original.count(mutant.old) != mutant.count:
                return mutant, "not_applied"
            copy = Path(scratch) / f"mutant-{mutant.id}"
            shutil.copytree(base, copy, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", ".git"))
            target = copy / mutant.file
            target.write_text(original.replace(mutant.old, mutant.new), encoding="utf-8", newline="\n")
            result = _pytest(copy, tests, stop_first=True, timeout=timeout)
            shutil.rmtree(copy, ignore_errors=True)
            return mutant, ("survived" if result.ok else "killed")

        with ThreadPoolExecutor(max_workers=workers) as pool:
            for mutant, outcome in pool.map(try_mutant, mutants):
                getattr(report, outcome).append(mutant)
    return report


# =================================================================================
# 4. process checks: every commit green, no test deleted
# =================================================================================
def green_commits(work: Path | str, *, max_commits: int = 12, workers: int = 4, timeout: float = 60.0) -> tuple[list[str], int]:
    """Run the whole suite at each commit since lab-start. Returns (red commits as 'sha subject', commits examined)."""
    work = Path(work)
    commits = [c for c in gitutil.commits_since(work) if not c.is_merge]
    if len(commits) > max_commits:  # keep the first, the last and an even spread between
        step = (len(commits) - 1) / (max_commits - 1)
        commits = [commits[round(i * step)] for i in range(max_commits)]
    red: list[str] = []

    def run(commit: gitutil.Commit) -> tuple[gitutil.Commit, bool]:
        with tempfile.TemporaryDirectory(prefix="ailab-m07-commit-") as scratch:
            tree = starter_tree(work, Path(scratch) / "tree", ref=commit.sha)
            result = _pytest(tree, ["tests"], stop_first=True, timeout=timeout)
            return commit, result.ok and "passed" in result.output

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for commit, ok in pool.map(run, commits):
            if not ok:
                red.append(f"{commit.sha[:7]} {commit.subject}")
    return red, len(commits)


def _test_names(source: str) -> list[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    return [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test_")]


def tests_not_deleted(work: Path | str) -> list[str]:
    """Starter tests that are gone. A test counts as kept when a test with the same name exists anywhere in tests/, or a
    newly added test has a very similar name (the migration renames ``test_new_id_...`` to ``test_make_id_...``)."""
    import difflib

    work = Path(work)
    listing = gitutil.out(work, "ls-tree", "-r", "--name-only", gitutil.TAG_START, "--", "tests").splitlines()
    before: dict[str, list[str]] = {}
    for rel in listing:
        if re.fullmatch(r"tests/test_[\w]+\.py", rel):
            before[rel] = _test_names(gitutil.file_at(work, gitutil.TAG_START, rel) or "")
    after: set[str] = set()
    for path in sorted((work / "tests").rglob("test_*.py")):
        if "_hidden" not in path.parts:
            after.update(_test_names(path.read_text(encoding="utf-8", errors="replace")))
    old_names = {name for names in before.values() for name in names}
    added = sorted(after - old_names)
    problems: list[str] = []
    for rel, names in before.items():
        for name in names:
            if name in after:
                continue
            if difflib.get_close_matches(name, added, n=1, cutoff=0.85):
                continue
            problems.append(f"{name} (in {rel}) is gone")
    return problems
