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
* ``characterization_report``    the learner's ``tests/test_ledger*.py`` pass on the ORIGINAL ledger (and on a copy of it that
                                 only differs in comments, spacing and private names) and kill mutants of it
* ``suite_check``                the whole suite passes the way CI runs it (``pytest -q``: no working directory on the import path)
* ``green_commits``              each commit since the start leaves the whole suite green
* ``tests_not_deleted``          no test of the starter was deleted
* ``small_steps``                at least three commits that change something, and the tests are not committed together with src/

Every pytest run here is ``python -P -m pytest``: ``-P`` keeps the working directory off ``sys.path``, exactly as the ``pytest``
command that CONTRIBUTING.md and CI use does. (``python -m pytest`` adds it, which would let ``from tests.ledger_port import ...``
pass the grader and fail in CI.)
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
from ailab.framework import Check

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
    equivalent_ok: bool = True  # the tests also pass on a copy that only differs in comments, spacing and private names
    equivalent_detail: str = ""
    peeking: list[str] = field(default_factory=list)  # ways the tests read the source text instead of calling the code
    import_error: bool = False  # the tests say `from tests.x import ...`, which `pytest -q` cannot do
    killed: list[Mutant] = field(default_factory=list)
    survived: list[Mutant] = field(default_factory=list)
    not_applied: list[Mutant] = field(default_factory=list)

    @property
    def ready(self) -> bool:
        """Good enough to be judged by the mutants: they describe the original, whatever its text looks like."""
        return self.baseline_ok and self.equivalent_ok and not self.peeking

    @property
    def problem(self) -> str:
        """What is wrong with the tests before any mutant is tried (empty when ``ready``)."""
        if not self.baseline_ok:
            return f"on the original code: {self.baseline_detail}"
        if self.peeking:
            return f"they read the ledger's source text instead of calling it: {checks._short(self.peeking, 3)}"
        if not self.equivalent_ok:
            return ("they pass on the original ledger but fail on a copy of it that only differs in comments, spacing and the names of "
                    f"private helpers: {self.equivalent_detail}")
        return ""

    @property
    def hint(self) -> str:
        if self.ready:
            return ""
        if not self.baseline_ok:
            if self.import_error:
                return IMPORT_HINT
            return ("A characterization test describes what the code does today, and the seam must keep working with the original "
                    "module. Run python lab-assets/try_mutation.py: it runs your tests on the original code. Fix the test, not the code.")
        return ("A characterization test calls the code and compares what comes back. It must not depend on how ledger.py is written: "
                "its text, its hash, its line numbers.")


IMPORT_HINT = ("Your tests import from `tests.` (for example `from tests.ledger_port import ...`). That works under `python -m pytest` but not "
               "under `pytest -q`, which is what CI runs. Write `from ledger_port import make_ledger, ledger_of` instead.")
_NO_TESTS_PACKAGE = re.compile(r"No module named ['\"]tests(?:\.|['\"])")


def import_problem(output: str) -> bool:
    """True when pytest's output shows the ``from tests.x import ...`` mistake."""
    return bool(_NO_TESTS_PACKAGE.search(output))


def _pytest(root: Path, targets: Sequence[str], *, stop_first: bool, timeout: float) -> runner.RunResult:
    """``pytest -q`` as CI runs it: ``-P`` keeps the working directory off ``sys.path`` (``python -m pytest`` would add it)."""
    args = ["-P", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", "-W", "ignore::DeprecationWarning"]
    if stop_first:
        args.append("-x")
    return runner.run_python([*args, *targets], cwd=root, pythonpath=[root / "src"], timeout=timeout)


def suite_check(work: Path | str, *, name: str, timeout: float = 60.0) -> Check:
    """The whole visible suite passes the way CI runs it (``pytest -q``), warnings and all."""
    with checks.work_copy(work) as root, tempfile.TemporaryDirectory(prefix="ailab-m07-junit-") as scratch:
        junit = Path(scratch) / "junit.xml"
        run = runner.run_python(["-P", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", f"--junitxml={junit}",
                                 "-o", "junit_family=xunit2", "tests"], cwd=root, pythonpath=[root / "src"], timeout=timeout)
        result = checks.PytestResult(returncode=run.returncode, timed_out=run.timed_out, duration=run.duration, output=run.output)
        if junit.exists():
            checks._parse_junit(junit, result)
    detail = result.summary()
    if result.failures:
        detail += f": {checks._short(result.failure_names)}"
    if result.ok:
        return Check(name, True, detail)
    hint = IMPORT_HINT if import_problem(run.output) else "Run `pytest -q` in your repository and read the first failure from the top."
    return Check(name, False, detail, hint)


# ---- the tests must describe behaviour, not the text of the file --------------------------------------------------------
def equivalent_source(source: str) -> str:
    """The original ledger written differently but behaving identically: a reviewer's comment, a reworded docstring, extra
    blank lines and renamed private helpers. A suite that passes on the original and fails here is fingerprinting the file."""
    text = re.sub(r"\b_CENT\b", "_ONE_CENT", source)
    text = re.sub(r"\b_post\b", "_post_entry", text)
    text = text.replace("LEGACY:", "LEGACY (reviewed in 2026):", 1)
    text = text.replace("\n\n\n", "\n\n\n\n")
    return "# Reviewed: no change in behaviour.\n" + text.rstrip("\n") + "\n\n# end of file\n"


_PEEK_MODULES = {"hashlib", "linecache", "tokenize", "dis", "ast"}
_PEEK_NAMES = {"getsource", "getsourcelines", "getsourcefile", "getfile", "__file__", "__code__"}


def source_peeking(work: Path | str, files: Sequence[str]) -> list[str]:
    """Places where the learner's tests look at the source text of the code instead of calling it (``file:line what``)."""
    found: list[str] = []
    for rel in files:
        try:
            tree = ast.parse((Path(work) / rel).read_text(encoding="utf-8"))
        except (OSError, SyntaxError, UnicodeDecodeError):
            continue
        docstrings = {id(node.body[0].value) for node in ast.walk(tree)
                      if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.body
                      and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant)}
        for node in ast.walk(tree):
            what = ""
            if isinstance(node, ast.Import):
                what = next((f"import {a.name}" for a in node.names if a.name.split(".")[0] in _PEEK_MODULES), "")
            elif isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] in _PEEK_MODULES:
                what = f"from {node.module} import ..."
            elif isinstance(node, ast.Attribute) and node.attr in _PEEK_NAMES:
                what = node.attr
            elif isinstance(node, ast.Name) and node.id in _PEEK_NAMES:
                what = node.id
            elif (isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstrings
                  and re.search(r"(?:^|[/\\])ledger\.py$|src[/\\]remit|remit[/\\]ledger", node.value)):
                what = "a path to the ledger's source file"
            if what:
                found.append(f"{rel}:{node.lineno} {what}")
    return sorted(set(found))


def passed_count(output: str) -> int:
    match = re.search(r"(\d+) passed", output)
    return int(match.group(1)) if match else 0


def characterization_report(work: Path | str, mutants: Sequence[Mutant] = MUTANTS, *, timeout: float = 30.0,
                            workers: int = 4) -> CharacterizationReport:
    """Run the learner's new ``tests/test_ledger*.py`` against the ORIGINAL repository, against a copy of it that only differs in
    comments and private names, and then against each mutant of it.

    The original is rebuilt from the ``lab-start`` tag, so the learner's tests must work on the code as it was before
    the refactor (that is what makes them characterization tests). ``tests/conftest.py`` is the original one too."""
    work = Path(work)
    tests, support = ledger_test_files(work)
    report = CharacterizationReport(tests=tests, n_tests=count_tests(work, tests))
    if not tests:
        report.baseline_detail = "no tests/test_ledger*.py file was added"
        return report
    report.peeking = source_peeking(work, [*tests, *support])
    with tempfile.TemporaryDirectory(prefix="ailab-m07-") as scratch:
        base = starter_tree(work, Path(scratch) / "base")
        for rel in [*tests, *support]:
            target = base / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(work / rel, target)
        first = _pytest(base, tests, stop_first=False, timeout=timeout * 2)
        report.baseline_ok = first.ok and "passed" in first.output
        report.n_tests = max(report.n_tests, passed_count(first.output))  # a parametrized test counts once per case
        if not report.baseline_ok:
            if first.timed_out:
                report.baseline_detail = "they did not finish in time"
            elif import_problem(first.output):
                report.import_error = True
                report.baseline_detail = "a test imports from `tests.`, which `pytest -q` cannot do (import error)"
            else:
                names = re.findall(r"^(?:FAILED|ERROR) (\S+)", first.output, flags=re.M)
                tail = first.output.strip().splitlines()[-1] if first.output.strip() else "no output"
                report.baseline_detail = tail + (f": {checks._short([n.split('::')[-1] for n in names], 3)}" if names else "")
            return report

        # the same ledger, written differently: the tests must not care
        ledger_path = base / LEDGER
        original_text = ledger_path.read_text(encoding="utf-8")
        ledger_path.write_text(equivalent_source(original_text), encoding="utf-8", newline="\n")
        twin = _pytest(base, tests, stop_first=True, timeout=timeout)
        ledger_path.write_text(original_text, encoding="utf-8", newline="\n")
        report.equivalent_ok = twin.ok and "passed" in twin.output
        if not report.equivalent_ok:
            names = re.findall(r"^(?:FAILED|ERROR) (\S+)", twin.output, flags=re.M)
            report.equivalent_detail = ("did not finish in time" if twin.timed_out
                                        else checks._short([n.split("::")[-1] for n in names], 3) or "see your tests")
        if not report.ready:
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


# =================================================================================
# 5. small steps: commits that change something, and the tests before the refactor
# =================================================================================
def commit_files(work: Path | str, sha: str) -> dict[str, str]:
    """Path -> 'A', 'M' or 'D' for what one commit changed (tool noise left out; a merge commit changes nothing here)."""
    raw = gitutil.git(work, "diff-tree", "--no-commit-id", "--name-status", "-r", "--no-renames", "-z", sha).stdout.split("\0")
    changes = {path: code[0] for code, path in zip(raw[0::2], raw[1::2]) if code}
    return {p: s for p, s in changes.items() if not gitutil.glob_match(p, gitutil.TOOL_NOISE)}


def is_ledger_test(path: str) -> bool:
    return path.startswith("tests/") and bool(re.fullmatch(r"test_ledger[\w]*\.py", path.rsplit("/", 1)[-1]))


def small_steps(work: Path | str, *, name: str, at_least: int = 3) -> Check:
    """At least ``at_least`` commits that change a file (an empty commit is no step), and the commit that first adds the ledger
    tests changes nothing under ``src/``: the net is committed before the structure moves."""
    work = Path(work)
    commits = [c for c in gitutil.commits_since(work) if not c.is_merge]
    changes = {c.sha: commit_files(work, c.sha) for c in commits}
    real = [c for c in commits if changes[c.sha]]
    total = len(gitutil.commits_since(work))
    detail = f"{checks.plural(total, 'new commit')} since the start"
    if len(real) < total:
        detail += f" ({total - len(real)} of them change no file)"
    problems: list[str] = []
    if len(real) < at_least:
        problems.append(detail)
    first = next((c for c in real if any(s == "A" and is_ledger_test(p) for p, s in changes[c.sha].items())), None)
    if first is not None:
        touched = sorted(p for p in changes[first.sha] if p.startswith("src/"))
        if touched:
            problems.append(f"the commit that adds your ledger tests ({first.sha[:7]}) also changes {checks._short(touched, 2)}")
    if problems:
        hints = []
        if len(real) < at_least:
            hints.append("Commit the tests, the refactor and the migration as separate steps: at least three commits, each changing a file "
                         "and leaving the suite green.")
        if first is not None and touched:
            hints.append("Commit your ledger tests on their own, before anything under src/ changes: `git reset lab-start` un-commits "
                         "everything and keeps your files; then commit again in pieces, the tests first.")
        return Check(name, False, "; ".join(problems), " ".join(hints))
    return Check(name, True, f"{checks.plural(len(real), 'commit')} that change something, the ledger tests first" if first else
                 f"{checks.plural(len(real), 'commit')} that change something")


# =================================================================================
# 6. documents that go stale
# =================================================================================
# Files whose statements about the ledger were true before this ticket and are false after it. The learner's own plan and
# notes (docs/refactoring-plan.md, docs/najmkit-v2-migration.md, docs/onboarding.md) are not swept: they talk about the old state.
SWEPT_DOCS = ("CLAUDE.md", "AGENTS.md", "README.md", "docs/ARCHITECTURE.md", "docs/TOUR.md")
_STALE = re.compile(
    r"(?i)ledger.{0,100}?(\bno tests?\b|\bno test file\b|\buntested\b|\bwithout tests\b|\bmodule[- ]level\b)"
    r"|(\bno test file for\b|\bno tests? for\b|\buntested\b|\bwithout tests\b).{0,40}ledger"
)
_PAST = re.compile(r"(?i)\b(no longer|used to|formerly|previously|instead of|removed|gone|no module[- ]level|not module[- ]level)\b")


def stale_document_lines(work: Path | str, files: Sequence[str] = SWEPT_DOCS) -> list[str]:
    """``file:line text`` for lines (or two lines read together) that still call the ledger untested or module-level."""
    found: list[str] = []
    for rel in files:
        path = Path(work) / rel
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        seen: set[int] = set()
        for index, line in enumerate(lines):
            for window in (line, f"{line} {lines[index + 1]}" if index + 1 < len(lines) else line):
                hit = _STALE.search(window)
                # a match that starts in the next line belongs to that line, which gets its own turn
                if index not in seen and hit and hit.start() < len(line) and not _PAST.search(window):
                    seen.add(index)
                    found.append(f"{rel}:{index + 1} {line.strip()}")
    return found
