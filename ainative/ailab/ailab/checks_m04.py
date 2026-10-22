"""Grader helpers for lab m04 (lesson 4.2): "Ship a small feature through the whole loop".

The lab is REMIT-318, the daily-limit warning. The result is graded by hidden acceptance tests (``labs/m04_limit_warning/hidden``);
this module holds the checks that look at HOW the work was done and at the learner's own tests:

* ``new_test_ids``            which test functions the learner added or changed (by AST, so appending to an existing file is fine)
* ``originals_intact``        no existing test, fixture or constant was edited or removed (weakening a test to go green)
* ``removal_check``           the new tests fail when every non-test file is put back to the starting code ("remove the feature")
* ``mutation_check``          the new tests fail when the warning is broken in seven deliberate ways. The breakage is applied by a
                              pytest plugin (``labs/m04_limit_warning/mutation/ailab_m04_mutants.py``) to the RUNNING program at its public
                              edges (what ``render`` returns, what the notifier delivers, the daily limits), so it works on any sound
                              implementation, whatever its structure
* ``no_floats``               the change adds no ``float`` to ``src/`` (CONTRIBUTING.md: money is Decimal)
* ``spec_check``, ``spec_first``, ``green_checkpoints``, ``small_commits``, ``blanket_except``, ``agent_log``   advisory loop-hygiene checks

Everything runs on throw-away copies, in subprocesses with timeouts; learner code is never imported here.
What this grader cannot tell: who wrote the code, whether the spec is GOOD (only its shape and a few facts), whether the Arabic
wording is good Arabic (the ticket supplies the approved copy), or whether the learner read the diff.
"""
from __future__ import annotations

import ast
import io
import os
import re
import subprocess
import tarfile
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from ailab import checks, gitutil, runner
from ailab.framework import LAB_START_TAG, Check
from ailab.gitutil import TOOL_NOISE

HERE = Path(__file__).resolve().parent
PLUGIN_DIR = HERE / "labs" / "m04_limit_warning" / "mutation"
PLUGIN = "ailab_m04_mutants"

SPEC_FILE = "specs/REMIT-318.md"
TEMPLATE_FILE = "specs/TEMPLATE.md"
LOG_FILE = "agent-log.md"

# Files a sound solution may touch. Everything else (money.py, fees.py, fx.py, ledger.py, cli.py, najmkit, CI, other docs) is out of scope.
ALLOWED = [
    "src/remit/notify.py",
    "src/remit/service.py",
    "src/remit/limits.py",
    "tests/**",
    "specs/**",
    "docs/**",
    LOG_FILE,
    "CLAUDE.md",
    "AGENTS.md",
    ".claude/**",
]
# For "the source change is small": these paths do not count as source.
NOT_SOURCE = ("tests/**", "specs/**", "docs/**", "**/*.md", ".claude/**", "lab-assets/**")
MAX_SOURCE_LINES = 120
MAX_SOURCE_FILES = 3
MAX_COMMIT_LINES = 200  # src + tests lines in one commit
MIN_COMMITS = 3
MAX_COMMITS = 15

# The deliberate breakages (id, what the learner is told when their tests miss it). The ids are known to the plugin.
MUTANTS: tuple[tuple[str, str], ...] = (
    ("drop", "the warning is never delivered"),
    ("blank", "the warning text loses its numbers"),
    ("percent_plus_one", "the percentage shown is one too high"),
    ("english_only", "Arabic customers get the English text"),
    ("western_digits", "Arabic text shows Western digits"),
    ("line_up", "the 80% line sits a little too high"),
    ("line_down", "the 80% line sits a little too low"),
)
MIN_KILLED = 5
WORKERS = 4  # independent pytest subprocesses at a time (each on its own copy)
_NUMBERED = re.compile(r"\s*\d+[.)]\s+\S")

# Check names (stable: the lesson and the tests quote them).
N_TESTS = "The whole test suite passes"
N_ORIGINALS = "The original tests are untouched"
N_HIDDEN = "The warning works as the ticket describes"
N_REMOVAL = "Your new tests fail when the warning is removed"
N_MUTANTS = "Your tests notice a broken warning"
N_SCOPE = "Only the expected files changed"
N_SIZE = "The source change is small"
N_FLOATS = "Money stays Decimal (no floats added)"
N_COMMIT_COUNT = "You worked in small commits"
N_MESSAGES = "Commit messages follow CONTRIBUTING.md"
N_CLEAN = "Everything is committed (nothing left over)"
N_SECRETS = "No secrets in the change"
N_SPEC = "A spec and plan were written"
N_SPEC_FIRST = "The spec was committed before the code"
N_GREEN = "Every commit is a green checkpoint"
N_SMALL = "No commit is large"
N_EXCEPT = "No blanket exception handler added"
N_LOG = "An agent log entry exists"


# ---------------------------------------------------------------------------------------------
# reading test files by AST
# ---------------------------------------------------------------------------------------------
def _parse(source: str | None) -> ast.Module | None:
    if source is None:
        return None
    try:
        return ast.parse(source)
    except (SyntaxError, ValueError):
        return None


def _definitions(tree: ast.Module) -> dict[str, str]:
    """Top-level functions, classes' methods and module constants: key -> a dump that ignores formatting and line numbers."""
    found: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            found[node.name] = ast.dump(node)
        elif isinstance(node, ast.ClassDef):
            for inner in node.body:
                if isinstance(inner, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    found[f"{node.name}.{inner.name}"] = ast.dump(inner)
                elif isinstance(inner, ast.Assign):
                    for target in inner.targets:
                        if isinstance(target, ast.Name):
                            found[f"{node.name}.{target.id}"] = ast.dump(inner.value)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    found[target.id] = ast.dump(node.value)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            found[node.target.id] = ast.dump(node)
    return found


def _is_test(key: str) -> bool:
    return key.rsplit(".", 1)[-1].startswith("test")


def _tests_at_start(work: Path, since: str) -> list[str]:
    listing = gitutil.git(work, "ls-tree", "-r", "--name-only", since, "--", "tests", check=False).stdout.splitlines()
    return [p for p in listing if p.endswith(".py")]


def new_test_ids(work: Path | str, since: str = LAB_START_TAG) -> list[str]:
    """Pytest node ids of the test functions the learner added or changed (a new file counts in full)."""
    work = Path(work)
    ids: list[str] = []
    for rel, state in gitutil.changed_status(work, since).items():
        if state == "D" or not gitutil.glob_match(rel, ["tests/**/test_*.py", "tests/test_*.py"]):
            continue
        try:
            text = (work / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        new_tree = _parse(text)
        if new_tree is None:
            ids.append(rel)  # a file that does not even parse: running it reports the error
            continue
        old_tree = _parse(gitutil.file_at(work, since, rel)) if state != "A" else None
        old = _definitions(old_tree) if old_tree is not None else {}
        for key, dump in _definitions(new_tree).items():
            if _is_test(key) and old.get(key) != dump:
                ids.append(f"{rel}::" + key.replace(".", "::"))
    return ids


def originals_intact(work: Path | str, since: str = LAB_START_TAG) -> Check:
    """No test, fixture, helper or constant that existed at the start was edited or removed. Adding is fine."""
    work = Path(work)
    broken: list[str] = []
    for rel in _tests_at_start(work, since):
        current = work / rel
        if not current.is_file():
            broken.append(f"{rel} (deleted)")
            continue
        old_tree = _parse(gitutil.file_at(work, since, rel))
        new_tree = _parse(current.read_text(encoding="utf-8", errors="replace"))
        if old_tree is None:
            continue
        if new_tree is None:
            broken.append(f"{rel} (no longer valid Python)")
            continue
        now = _definitions(new_tree)
        for key, dump in _definitions(old_tree).items():
            if now.get(key) != dump:
                broken.append(f"{rel}::{key}")
    if broken:
        return Check(N_ORIGINALS, False, f"edited or removed: {checks._short(broken)}",  # noqa: SLF001 (kit-internal helper)
                     "Add new tests next to the old ones. If an old test fails, the code is wrong, not the test: undo your edit "
                     "(git restore tests).")
    return Check(N_ORIGINALS, True, "no existing test, fixture or constant was changed")


# ---------------------------------------------------------------------------------------------
# running the learner's new tests
# ---------------------------------------------------------------------------------------------
def _run(root: Path, targets: list[str], *, timeout: float = 60.0, args: tuple[str, ...] = (),
         env: dict[str, str] | None = None) -> checks.PytestResult:
    return checks._run_pytest_in(root, targets, timeout=timeout, args=args, extra_env=env)  # noqa: SLF001 (kit-internal helper)


def _restore_starting_code(work: Path, root: Path, since: str) -> None:
    """In the copy ``root``, put every file that is not a test back to how it was at ``since``."""
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


def removal_check(work: Path | str, since: str = LAB_START_TAG, timeout: float = 60.0) -> Check:
    """The learner's new tests fail (or error, or hang) once the code outside tests/ is the starting code again."""
    work = Path(work)
    ids = new_test_ids(work, since)
    if not ids:
        return Check(N_REMOVAL, False, "no new tests found", "Add tests in tests/ (a new file such as tests/test_limit_warning.py is fine).")
    with checks.work_copy(work) as root:
        _restore_starting_code(work, root, since)
        result = _run(root, ids, timeout=timeout)
    caught = result.failed + result.errors
    if result.timed_out or caught:
        return Check(N_REMOVAL, True, f"{checks.plural(caught, 'new test')} {'fails' if caught == 1 else 'fail'} without the warning, as they should" if caught
                     else "the new tests do not finish without the warning")
    return Check(N_REMOVAL, False, "all of your new tests pass even without the warning, so they would not notice it missing",
                 "A test that passes before the feature exists proves nothing. Make each new test fail first, then build the feature.")


def _mutant_env(root: Path, mutant: str) -> dict[str, str]:
    return {"PYTHONPATH": os.pathsep.join([str(root / "src"), str(PLUGIN_DIR)]), "AILAB_M04_MUTANT": mutant}


def mutation_report(work: Path | str, since: str = LAB_START_TAG, timeout: float = 30.0) -> tuple[bool, str, list[str], list[str]]:
    """(control run passed, its summary, descriptions of killed mutants, descriptions of survivors)."""
    work = Path(work)
    ids = new_test_ids(work, since)
    if not ids:
        return False, "no new tests found", [], []
    with checks.work_copy(work) as root:
        control = _run(root, ids, timeout=timeout, args=("-p", PLUGIN), env=_mutant_env(root, "control"))
        if not control.ok:
            return False, control.summary(), [], []

        def one(mutant: str) -> bool:
            """True when the learner's tests still PASS with this mutant (it survived)."""
            with checks.work_copy(root) as private:
                return _run(private, ids, timeout=timeout, args=("-x", "-p", PLUGIN), env=_mutant_env(private, mutant)).ok

        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            outcomes = list(pool.map(one, [mutant for mutant, _ in MUTANTS]))
    killed = [description for (_, description), survived_it in zip(MUTANTS, outcomes) if not survived_it]
    survived = [description for (_, description), survived_it in zip(MUTANTS, outcomes) if survived_it]
    return True, control.summary(), killed, survived


def mutation_check(work: Path | str, since: str = LAB_START_TAG, min_killed: int = MIN_KILLED) -> Check:
    ok_control, summary, killed, survived = mutation_report(work, since)
    if not ok_control:
        if summary == "no new tests found":
            return Check(N_MUTANTS, False, summary, "Add tests in tests/ (a new file is fine) and make them pass first.")
        return Check(N_MUTANTS, False, f"your new tests do not pass on your own code ({summary})",
                     "Make your new tests pass first; then the grader can break the warning on purpose and see whether they notice.")
    ok = len(killed) >= min_killed
    detail = f"your tests catch {len(killed)} of {len(MUTANTS)} deliberate defects"
    if survived and not ok:
        detail += f"; they miss: {checks._short(survived, 3)}"  # noqa: SLF001
    elif survived:
        detail += f" (still missing: {checks._short(survived, 3)})"  # noqa: SLF001
    return Check(N_MUTANTS, ok, detail,
                 "" if ok else "Pin the exact message in both languages, the number it shows, and the lines just under and exactly at 80%.")


# ---------------------------------------------------------------------------------------------
# house rules in the diff
# ---------------------------------------------------------------------------------------------
def _float_uses(tree: ast.Module) -> int:
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            count += 1
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "float":
            count += 1
    return count


def no_floats(work: Path | str, since: str = LAB_START_TAG) -> Check:
    """The change adds no float literal and no float() call to src/ (a float next to money is how rounding bugs start)."""
    work = Path(work)
    added: list[str] = []
    for rel, state in gitutil.changed_status(work, since).items():
        if state == "D" or not gitutil.glob_match(rel, ["src/**/*.py"]):
            continue
        new_tree = _parse((work / rel).read_text(encoding="utf-8", errors="replace"))
        old_tree = _parse(gitutil.file_at(work, since, rel)) if state != "A" else None
        if new_tree is not None and _float_uses(new_tree) > (_float_uses(old_tree) if old_tree is not None else 0):
            added.append(rel)
    if added:
        return Check(N_FLOATS, False, f"a float appears in {checks._short(added)}",  # noqa: SLF001
                     "CONTRIBUTING.md: money is Decimal, never float. Compare and divide Decimal values; a Decimal compared with a float "
                     "is compared exactly, so 0.8 is not the same number as Decimal('0.8').")
    return Check(N_FLOATS, True, "no float literal or float() call was added")


def blanket_except(work: Path | str) -> Check:
    return checks.forbid_patterns(
        work, {"a blanket exception handler": r"^\s*except\s*:|^\s*except\s+(?:Exception|BaseException)\b"},
        globs=["src/**/*.py"], name=N_EXCEPT,
        hint="Catch the specific error you expect. For a best-effort notification the service already has a helper that catches "
             "NotificationError and audits it; read how the transfer_sent message is sent.", required=False)


# ---------------------------------------------------------------------------------------------
# the loop: spec first, small commits, green checkpoints
# ---------------------------------------------------------------------------------------------
def _commit_files(work: Path, sha: str) -> list[str]:
    return gitutil.git(work, "show", "--name-only", "--format=", sha).stdout.split()


def _commit_lines(work: Path, sha: str, globs: list[str]) -> int:
    total = 0
    for line in gitutil.git(work, "show", "--numstat", "--format=", sha).stdout.splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3 and gitutil.glob_match(parts[2], globs):
            total += int(parts[0]) if parts[0].isdigit() else 0
            total += int(parts[1]) if parts[1].isdigit() else 0
    return total


def _export_commit(work: Path, sha: str, dest: Path) -> bool:
    """Write the files of commit ``sha`` into ``dest`` (git archive, read back safely). False if it failed."""
    proc = subprocess.run(["git", "archive", "--format=tar", sha], cwd=str(work), env=runner.clean_env(), capture_output=True)
    if proc.returncode != 0:
        return False
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as archive:
        for member in archive.getmembers():
            parts = Path(member.name).parts
            if member.name.startswith("/") or ".." in parts or not (member.isfile() or member.isdir()):
                continue
            try:
                archive.extract(member, dest, filter="data")
            except TypeError:  # Python before 3.11.4 has no extraction filters
                archive.extract(member, dest)
    return True


def spec_check(work: Path | str) -> Check:
    """The spec exists on the template's headings, has no placeholders left, and its plan has 4 to 10 numbered steps."""
    work = Path(work)
    path = work / SPEC_FILE
    hint = f"Copy {TEMPLATE_FILE} to {SPEC_FILE}, replace every TODO, and give the Plan four to ten numbered steps."
    if not path.is_file():
        return Check(N_SPEC, False, f"{SPEC_FILE} does not exist", hint, False)
    sections = checks.markdown_sections(path)
    problems: list[str] = []
    for wanted in ("goal", "behaviour", "acceptance criteria", "non-goals", "decisions and open questions", "plan"):
        key = next((k for k in sections if wanted in k), None)
        if key is None:
            problems.append(f"no '{wanted}' section")
        elif len(sections[key].split()) < 8:
            problems.append(f"'{wanted}' is thin")
    text = path.read_text(encoding="utf-8")
    if "TODO" in text:
        problems.append("a TODO placeholder is left")
    plan_key = next((k for k in sections if "plan" in k and "test" not in k), None)
    steps = [ln for ln in (sections.get(plan_key, "") if plan_key else "").splitlines() if _NUMBERED.match(ln)]
    if not 4 <= len(steps) <= 10:
        problems.append(f"the plan has {len(steps)} numbered steps (4 to 10 expected)")
    if problems:
        return Check(N_SPEC, False, checks._short(problems, 4), hint, False)  # noqa: SLF001
    return Check(N_SPEC, True, f"{SPEC_FILE} has its sections and a plan of {len(steps)} steps", "", False)


def spec_first(work: Path | str, since: str = LAB_START_TAG) -> Check:
    work = Path(work)
    commits = [c for c in gitutil.commits_since(work, since) if not c.is_merge]
    spec_at = src_at = None
    for index, commit in enumerate(commits):
        files = _commit_files(work, commit.sha)
        if spec_at is None and SPEC_FILE in files:
            spec_at = index
        if src_at is None and any(f.startswith("src/") for f in files):
            src_at = index
    hint = "Write and commit the spec and plan first (docs(specs): ...), then start the code. The spec is what you review the diff against."
    if spec_at is None:
        return Check(N_SPEC_FIRST, False, f"no commit adds {SPEC_FILE}", hint, False)
    if src_at is None:
        return Check(N_SPEC_FIRST, False, "no commit changes the code yet", "", False)
    if spec_at >= src_at:
        return Check(N_SPEC_FIRST, False, "the code was committed no later than the spec", hint, False)
    return Check(N_SPEC_FIRST, True, "the spec was committed before the first code change", "", False)


def green_checkpoints(work: Path | str, since: str = LAB_START_TAG, max_commits: int = 12) -> Check:
    """Every commit, checked out on its own, passes the tests it contains (CONTRIBUTING.md: tests pass before you commit)."""
    work = Path(work)
    commits = [c for c in gitutil.commits_since(work, since) if not c.is_merge]
    if not commits:
        return Check(N_GREEN, False, "no commits yet", "Commit after each small step, when the tests are green.", False)
    def one(commit) -> bool:
        """True when the commit, checked out alone, has green tests (or could not be exported)."""
        with tempfile.TemporaryDirectory(prefix="ailab-m04-") as tmp:
            root = Path(tmp) / "work"
            if not _export_commit(work, commit.sha, root):
                return True
            return _run(root, ["tests"], timeout=60.0).ok

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        greens = list(pool.map(one, commits[:max_commits]))
    red = [f'"{commit.subject}"' for commit, green in zip(commits, greens) if not green]
    if red:
        return Check(N_GREEN, False, f"{checks.plural(len(red), 'commit')} leave the tests red: {checks._short(red, 2)}",  # noqa: SLF001
                     "A commit is a save point you may need to return to. Commit when `pytest -q` is green; if a step needs two files "
                     "to be green, commit them together.", False)
    return Check(N_GREEN, True, f"{checks.plural(min(len(commits), max_commits), 'commit')} checked, all green", "", False)


def small_commits(work: Path | str, since: str = LAB_START_TAG) -> Check:
    work = Path(work)
    big: list[str] = []
    for commit in (c for c in gitutil.commits_since(work, since) if not c.is_merge):
        lines = _commit_lines(work, commit.sha, ["src/**", "tests/**"])
        if lines > MAX_COMMIT_LINES:
            big.append(f'"{commit.subject}" ({lines} lines)')
    if big:
        return Check(N_SMALL, False, checks._short(big, 2), f"Aim for commits under about {MAX_COMMIT_LINES} changed lines of code and tests: "  # noqa: SLF001
                     "one step, one check, one commit.", False)
    return Check(N_SMALL, True, f"no commit changes more than {MAX_COMMIT_LINES} lines of code and tests", "", False)


def agent_log(work: Path | str, since: str = LAB_START_TAG) -> Check:
    work = Path(work)
    path = work / LOG_FILE
    hint = f"Fill one entry in {LOG_FILE}: prompt, what the agent did, what you corrected, what you checked, minutes. If you used no agent, say so and why."
    if not path.is_file():
        return Check(N_LOG, False, f"{LOG_FILE} does not exist", hint, False)
    text = path.read_text(encoding="utf-8", errors="replace")
    original = gitutil.file_at(work, since, LOG_FILE) or ""
    added_words = len(text.split()) - len(original.split())
    if text.strip() == original.strip() or (added_words < 15 and "no agent" not in text.lower()):
        return Check(N_LOG, False, "the log has no entry yet", hint, False)
    return Check(N_LOG, True, "the log has an entry", "", False)


def source_size(work: Path | str, since: str = LAB_START_TAG) -> Check:
    return checks.diff_size(
        work, MAX_SOURCE_LINES, max_files=MAX_SOURCE_FILES, min_lines=1, since=since, ignore=(*TOOL_NOISE, *NOT_SOURCE), name=N_SIZE,
        hint="The ticket needs one template and a short piece of logic. Look at `git diff lab-start --stat -- src` and remove what the "
             "ticket did not ask for.",
    )
