"""Reusable checks for lab graders.

A lab's ``grade(work)`` is usually a short list built from these helpers::

    def grade(work):
        return [
            checks.tests_pass(work),
            checks.hidden_tests_pass(work, HERE / "hidden"),
            checks.files_changed_within(work, ["src/remit/notify.py"]),
            checks.diff_size(work, max_lines=6),
            checks.conventional_commits(work),
        ]

Rules these helpers follow, and your own checks should too:

* They never modify the learner's work directory. Anything that runs code (pytest, a
  mutant) runs on a throw-away *copy* in a temporary folder, in a subprocess, with a
  timeout (``runner.run``). Learner code is never imported in the grader's process.
* "Changed" always means "compared with the ``lab-start`` tag", including uncommitted and
  untracked files, ignoring the noise editors and agent tools leave behind (gitutil.TOOL_NOISE).
* A failing ``Check`` says what was found in ``detail`` and what to try in ``hint``. Neither
  ever contains the hidden answer, hidden test code or an expected value.

Layout of this file: (1) pytest runners, (2) git-based checks, (3) secrets and forbidden patterns,
(4) mutation checking and "fails on the starter", (5) JSON validators, (6) Markdown helpers,
(7) small file checks and a static API lister.
"""
from __future__ import annotations

import ast
import re
import shutil
import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ailab import gitutil, runner
from ailab.framework import LAB_START_TAG, Check
from ailab.gitutil import TOOL_NOISE

# Folders that are never copied into a throw-away copy of the work directory.
_COPY_IGNORE = shutil.ignore_patterns(
    ".git", "__pycache__", "*.pyc", ".pytest_cache", ".venv", "venv", "node_modules", "*.egg-info", ".mypy_cache"
)


def _short(items: Sequence[str], limit: int = 4) -> str:
    shown = ", ".join(items[:limit])
    return shown + (f" (+{len(items) - limit} more)" if len(items) > limit else "")


def plural(n: int, word: str) -> str:
    return f"{n} {word}{'' if n == 1 else 's'}"


# =================================================================================
# 1. pytest
# =================================================================================
@dataclass
class PytestResult:
    returncode: int
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    failures: list[str] = field(default_factory=list)  # "module::test_name" of failed or errored tests
    timed_out: bool = False
    duration: float = 0.0
    output: str = ""

    @property
    def total(self) -> int:
        return self.passed + self.failed + self.errors + self.skipped

    @property
    def ok(self) -> bool:
        """Everything that was collected passed, and something was collected."""
        return self.returncode == 0 and not self.timed_out and self.passed > 0

    @property
    def failure_names(self) -> list[str]:
        """Just the test function names of the failures."""
        return [f.split("::")[-1] for f in self.failures]

    def summary(self) -> str:
        if self.timed_out:
            return "the tests did not finish in time"
        if self.total == 0:
            return "no tests ran" + (" (collection failed)" if self.returncode not in (0, 5) else "")
        parts = [f"{self.passed} passed"]
        if self.failed:
            parts.append(f"{self.failed} failed")
        if self.errors:
            parts.append(f"{self.errors} errored")
        if self.skipped:
            parts.append(f"{self.skipped} skipped")
        return ", ".join(parts)


def copy_work(work: Path | str, dest: Path | str | None = None) -> Path:
    """Copy the work directory (without .git, caches, virtualenvs) into ``dest`` or a new temp folder.

    The caller owns the result; for a temp folder use it inside ``tempfile.TemporaryDirectory`` or
    the ``work_copy`` context manager.
    """
    target = Path(dest) if dest else Path(tempfile.mkdtemp(prefix="ailab-"))
    shutil.copytree(work, target, ignore=_COPY_IGNORE, dirs_exist_ok=True)
    return target


class work_copy:
    """Context manager: ``with work_copy(work) as tmp:`` gives a throw-away copy that is deleted afterwards."""

    def __init__(self, work: Path | str) -> None:
        self._work = Path(work)
        self._tmp: tempfile.TemporaryDirectory[str] | None = None

    def __enter__(self) -> Path:
        self._tmp = tempfile.TemporaryDirectory(prefix="ailab-")
        copy = Path(self._tmp.name) / "work"
        shutil.copytree(self._work, copy, ignore=_COPY_IGNORE)
        return copy

    def __exit__(self, *exc_info: object) -> None:
        if self._tmp is not None:
            self._tmp.cleanup()


def _parse_junit(path: Path, result: PytestResult) -> None:
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError):
        return
    for case in root.iter("testcase"):
        ident = f"{case.get('classname', '')}::{case.get('name', '')}"
        if case.find("failure") is not None:
            result.failed += 1
            result.failures.append(ident)
        elif case.find("error") is not None:
            result.errors += 1
            result.failures.append(ident)
        elif case.find("skipped") is not None:
            result.skipped += 1
        else:
            result.passed += 1


def _run_pytest_in(
    root: Path,
    targets: Sequence[str],
    *,
    timeout: float,
    args: Sequence[str],
    extra_env: dict[str, str] | None,
) -> PytestResult:
    """Run pytest with ``root`` as the project (rootdir, cwd and ``root/src`` on PYTHONPATH)."""
    with tempfile.TemporaryDirectory(prefix="ailab-junit-") as scratch:
        junit = Path(scratch) / "junit.xml"
        cmd = ["-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", f"--junitxml={junit}",
               "-o", "junit_family=xunit2", *args, *targets]
        run = runner.run_python(cmd, cwd=root, pythonpath=[root / "src"], timeout=timeout, extra_env=extra_env)
        result = PytestResult(returncode=run.returncode, timed_out=run.timed_out, duration=run.duration,
                              output=run.output)
        if junit.exists():
            _parse_junit(junit, result)
    return result


def run_pytest(
    work: Path | str,
    paths: Sequence[str] = ("tests",),
    *,
    timeout: float = 60.0,
    args: Sequence[str] = (),
    extra_env: dict[str, str] | None = None,
) -> PytestResult:
    """Run the learner's own tests (``paths`` are relative to the work directory) on a copy.

    ``PYTHONPATH`` is the copy's ``src`` folder (and the copy itself), the environment is scrubbed
    (runner.clean_env), and the run is killed after ``timeout`` seconds.
    """
    with work_copy(work) as root:
        return _run_pytest_in(root, list(paths), timeout=timeout, args=args, extra_env=extra_env)


def run_hidden_pytest(
    work: Path | str,
    hidden: Path | str | Sequence[Path | str],
    *,
    timeout: float = 60.0,
    args: Sequence[str] = (),
    extra_env: dict[str, str] | None = None,
) -> PytestResult:
    """Run a lab's hidden tests against the learner's code.

    ``hidden`` is a folder or file(s) inside the kit. They are copied into ``tests/_hidden/`` of a
    throw-away copy of the work directory, so they can use the project's ``tests/conftest.py`` fixtures
    and import ``remit`` from the learner's ``src``. Only the hidden tests are run. Give hidden test files
    unique names (``test_m04_*.py``); a ``conftest.py`` placed next to them applies to them only.
    """
    sources = [Path(hidden)] if isinstance(hidden, (str, Path)) else [Path(h) for h in hidden]
    with work_copy(work) as root:
        target = root / "tests" / "_hidden"
        target.mkdir(parents=True, exist_ok=True)
        for source in sources:
            if source.is_dir():
                shutil.copytree(source, target, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copyfile(source, target / source.name)
        return _run_pytest_in(root, ["tests/_hidden"], timeout=timeout, args=args, extra_env=extra_env)


def tests_pass(
    work: Path | str,
    paths: Sequence[str] = ("tests",),
    *,
    name: str = "Your tests pass",
    timeout: float = 60.0,
    hint: str = "Run `pytest -q` in your repository and read the first failure from the top.",
    required: bool = True,
) -> Check:
    """The learner's own visible tests (all of ``tests/`` by default) pass."""
    result = run_pytest(work, paths, timeout=timeout)
    detail = result.summary()
    if result.failures:
        detail += f": {_short(result.failure_names)}"
    return Check(name, result.ok, detail, "" if result.ok else hint, required)


def hidden_tests_pass(
    work: Path | str,
    hidden: Path | str | Sequence[Path | str],
    *,
    name: str = "Acceptance tests pass",
    reveal: str = "names",
    timeout: float = 60.0,
    hint: str = "Re-read the ticket: which behaviour does it ask for that you have not checked yourself?",
    required: bool = True,
) -> Check:
    """The lab's hidden tests pass against the learner's code.

    ``reveal`` controls how much the learner learns about a failure: ``"names"`` lists the failing
    test function names (so choose them as you would a hint), ``"count"`` only says how many failed.
    Assertion messages and test code are never shown.
    """
    result = run_hidden_pytest(work, hidden, timeout=timeout)
    if result.ok:
        return Check(name, True, f"{plural(result.passed, 'hidden check')} passed")
    if result.timed_out:
        detail = "the acceptance tests did not finish in time (an endless loop?)"
    elif result.total == 0:
        detail = "the acceptance tests could not run (does your code still import? run `pytest -q`)"
    else:
        bad = result.failed + result.errors
        detail = f"{bad} of {result.total} hidden checks failed"
        if reveal == "names" and result.failures:
            detail += f": {_short(result.failure_names)}"
    return Check(name, False, detail, hint, required)


# =================================================================================
# 2. git-based checks
# =================================================================================
def files_changed_within(
    work: Path | str,
    allowed: Sequence[str],
    *,
    since: str = LAB_START_TAG,
    ignore: Sequence[str] = TOOL_NOISE,
    name: str = "Only the expected files changed",
    hint: str = "Revert what is not needed for this task (git restore <file> or git rm <file>).",
    require_change: bool = True,
    required: bool = True,
) -> Check:
    """Every file changed since ``since`` matches one of the ``allowed`` globs (``**`` spans folders).

    With ``require_change`` (default) it also fails when nothing changed at all.
    """
    changed = gitutil.changed_files(work, since, ignore=ignore)
    outside = [p for p in changed if not gitutil.glob_match(p, allowed)]
    if outside:
        return Check(name, False, f"unrelated files changed: {_short(outside)}", hint, required)
    if require_change and not changed:
        return Check(name, False, "no files have changed yet", "Make the change the ticket asks for.", required)
    return Check(name, True, f"changed: {_short(changed)}" if changed else "nothing changed", "", required)


def files_unchanged(
    work: Path | str,
    protected: Sequence[str],
    *,
    since: str = LAB_START_TAG,
    ignore: Sequence[str] = TOOL_NOISE,
    name: str = "Protected files untouched",
    hint: str = "Do not edit these files; restore them with git restore <file>.",
    required: bool = True,
) -> Check:
    """No file matching the ``protected`` globs was added, changed or deleted (for example the tests)."""
    touched = [p for p in gitutil.changed_files(work, since, ignore=ignore) if gitutil.glob_match(p, protected)]
    if touched:
        return Check(name, False, f"changed but should not be: {_short(touched)}", hint, required)
    return Check(name, True, "", "", required)


def diff_size(
    work: Path | str,
    max_lines: int,
    *,
    max_files: int | None = None,
    min_lines: int = 0,
    since: str = LAB_START_TAG,
    ignore: Sequence[str] = TOOL_NOISE,
    name: str = "The change is small",
    hint: str = "Keep the diff to what the ticket needs; look at `git diff lab-start --stat`.",
    required: bool = True,
) -> Check:
    """Lines added plus lines deleted since ``since`` are at most ``max_lines`` (and files at most ``max_files``)."""
    stat = gitutil.diff_numstat(work, since, ignore=ignore)
    detail = f"{plural(stat.n_files, 'file')}, +{stat.added} -{stat.deleted} lines"
    ok = stat.total <= max_lines and stat.total >= min_lines and (max_files is None or stat.n_files <= max_files)
    if stat.total > max_lines:
        detail += f" (limit {max_lines} changed lines)"
    if max_files is not None and stat.n_files > max_files:
        detail += f" (limit {plural(max_files, 'file')})"
    if stat.total < min_lines:
        detail += " (nothing substantial has changed yet)"
    return Check(name, ok, detail, "" if ok else hint, required)


def commit_count(
    work: Path | str,
    *,
    exactly: int | None = None,
    at_least: int | None = None,
    at_most: int | None = None,
    since: str = LAB_START_TAG,
    name: str | None = None,
    hint: str | None = None,
    required: bool = True,
) -> Check:
    """The number of commits made since ``since`` is as required."""
    count = len(gitutil.commits_since(work, since))
    ok = (exactly is None or count == exactly) and (at_least is None or count >= at_least) and \
         (at_most is None or count <= at_most)
    want = (f"exactly {exactly}" if exactly is not None else
            " and ".join(x for x in (f"at least {at_least}" if at_least is not None else "",
                                     f"at most {at_most}" if at_most is not None else "") if x))
    label = name or f"Commit count ({want})"
    detail = f"{plural(count, 'new commit')} since the start"
    default_hint = "Commit your finished change (git add -A && git commit)." if count == 0 else \
        "Squash or split your commits to match the task (git rebase -i is fine; so is starting the commit again)."
    return Check(label, ok, detail, "" if ok else (hint or default_hint), required)


def all_committed(
    work: Path | str,
    *,
    ignore: Sequence[str] = TOOL_NOISE,
    name: str = "Everything is committed",
    required: bool = True,
) -> Check:
    """No uncommitted or untracked changes are left in the work directory."""
    dirty = gitutil.status_porcelain(work, ignore=ignore)
    if dirty:
        return Check(name, False, f"{plural(len(dirty), 'uncommitted change')}: {_short([d.strip() for d in dirty])}",
                     "Commit your work (git add -A && git commit) or discard what you do not need.", required)
    return Check(name, True, "", "", required)


CC_TYPES = ("feat", "fix", "docs", "test", "refactor", "perf", "chore", "ci", "build", "revert")
_CC_HEADER = re.compile(r"^(?P<type>[a-z]+)\((?P<scope>[a-z0-9][a-z0-9._/-]*)\)(?P<bang>!)?: (?P<subject>\S.*)$")
_CC_NO_SCOPE = re.compile(r"^(?P<type>[a-z]+)(?P<bang>!)?: (?P<subject>\S.*)$")


def commit_header_problems(
    header: str,
    *,
    types: Sequence[str] = CC_TYPES,
    require_scope: bool = True,
    max_header: int = 72,
) -> list[str]:
    """Problems with one commit header against CONTRIBUTING.md; an empty list means it is fine."""
    problems: list[str] = []
    match = _CC_HEADER.match(header)
    if match is None:
        if _CC_NO_SCOPE.match(header):
            if require_scope:
                problems.append("it has no scope: write type(scope): subject, for example fix(notify): ...")
            match = _CC_NO_SCOPE.match(header)
        else:
            problems.append("it does not look like `type(scope): subject`")
    if match is not None:
        if match.group("type") not in types:
            problems.append(f"the type `{match.group('type')}` is not one of: {', '.join(types)}")
        if match.group("subject").endswith("."):
            problems.append("the subject should not end with a full stop")
    if len(header) > max_header:
        problems.append(f"the header is {len(header)} characters; the limit is {max_header}")
    return problems


def conventional_commits(
    work: Path | str,
    *,
    since: str = LAB_START_TAG,
    require_scope: bool = True,
    max_header: int = 72,
    types: Sequence[str] = CC_TYPES,
    min_commits: int = 1,
    name: str = "Commit messages follow CONTRIBUTING.md",
    required: bool = True,
) -> Check:
    """Every commit since ``since`` has a Conventional Commits header as CONTRIBUTING.md describes.

    Merge commits are skipped. Fails when fewer than ``min_commits`` commits exist.
    """
    commits = [c for c in gitutil.commits_since(work, since) if not c.is_merge]
    hint = "Open CONTRIBUTING.md and follow its commit format (amend with: git commit --amend)."
    if len(commits) < min_commits:
        return Check(name, False, f"found {plural(len(commits), 'commit')} since the start; expected at least {min_commits}",
                     "Commit your change.", required)
    bad: list[str] = []
    for commit in commits:
        problems = commit_header_problems(commit.subject, types=types, require_scope=require_scope,
                                          max_header=max_header)
        if problems:
            bad.append(f'"{commit.subject}": {problems[0]}')
    if bad:
        return Check(name, False, _short(bad, 2), hint, required)
    return Check(name, True, f"{plural(len(commits), 'commit message')} checked", "", required)


# =================================================================================
# 3. secrets
# =================================================================================
SECRET_PATTERNS: dict[str, re.Pattern[str]] = {
    "AWS access key id": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key block": re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "Slack token": re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"),
    "API key (sk-...)": re.compile(r"\bsk-(?:ant-|live-|proj-)?[A-Za-z0-9_-]{20,}\b"),
    "payment key (sk_live_...)": re.compile(r"\b[sr]k_(?:live|test)_[A-Za-z0-9]{16,}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "bearer token": re.compile(r"\b[Bb]earer\s+[A-Za-z0-9._~+/-]{20,}=*"),
    "hard-coded credential": re.compile(
        r"""(?ix)(?P<name>\w*(?:api[_-]?key|secret|token|passwd|password|private[_-]?key|credential)\w*)
            ["']?\s*[:=]\s*["'](?P<value>[^"'\s]{12,})["']"""),
}
# Names that mention "token" or "secret" but hold something harmless (token_url, secret_name, ...).
_HARMLESS_NAME = re.compile(r"(?i)(url|uri|path|file|name|type|header|field|endpoint|expiry|expires|ttl|length|count|limit|label)s?$")
_PLACEHOLDER = re.compile(r"(?i)change.?me|your[_-]|example|placeholder|dummy|fake|x{4,}|\*{3,}|<[^>]+>|\$\{|%\(|os\.environ|getenv")


def find_secrets(text: str) -> list[tuple[str, int]]:
    """Key-like strings in ``text`` as (rule name, 1-based line number). Placeholders are not reported."""
    found: list[tuple[str, int]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        for rule, pattern in SECRET_PATTERNS.items():
            for match in pattern.finditer(line):
                value = match.groupdict().get("value") or match.group(0)
                if _PLACEHOLDER.search(value):
                    continue
                if rule == "hard-coded credential" and (
                    _HARMLESS_NAME.search(match.group("name")) or "://" in value or _PLACEHOLDER.search(line)
                ):
                    continue
                found.append((rule, number))
                break
    return found


def added_text(work: Path | str, since: str = LAB_START_TAG, ignore: Sequence[str] = TOOL_NOISE) -> dict[str, str]:
    """For each changed text file, the text the learner added: all of a new file, the '+' lines of a modified one."""
    work = Path(work)
    texts: dict[str, str] = {}
    for path, state in gitutil.changed_status(work, since, ignore=ignore).items():
        if state == "D":
            continue
        full = work / path
        try:
            data = full.read_bytes()
        except OSError:
            continue
        if b"\0" in data[:8000] or len(data) > 2_000_000:
            continue
        if state == "A":
            texts[path] = data.decode("utf-8", errors="replace")
        else:
            diff = gitutil.git(work, "diff", "-U0", "--no-color", since, "--", path).stdout
            texts[path] = "\n".join(line[1:] for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++"))
    return texts


def no_secrets(
    work: Path | str,
    *,
    since: str = LAB_START_TAG,
    scan: str = "added",
    ignore: Sequence[str] = TOOL_NOISE,
    name: str = "No secrets in the change",
    required: bool = True,
) -> Check:
    """No key-like strings in what the learner added (``scan="added"``) or anywhere (``scan="all"``).

    Also scans the commit messages since ``since``. Reports rule names and file:line, never the secret.
    """
    work = Path(work)
    hits: list[str] = []
    if scan == "all":
        texts = {}
        for path in sorted(set(gitutil.out(work, "ls-files").splitlines()) | set(gitutil.changed_files(work, since, ignore=ignore))):
            if gitutil.glob_match(path, ignore) or not (work / path).is_file():
                continue
            data = (work / path).read_bytes()
            if b"\0" not in data[:8000] and len(data) <= 2_000_000:
                texts[path] = data.decode("utf-8", errors="replace")
    else:
        texts = added_text(work, since, ignore)
    for path, text in texts.items():
        for rule, line in find_secrets(text):
            hits.append(f"{rule} in {path}" + (f":{line}" if scan == "all" else ""))
    for commit in gitutil.commits_since(work, since):
        for rule, _ in find_secrets(commit.message):
            hits.append(f"{rule} in the message of commit {commit.sha[:7]}")
    if hits:
        return Check(name, False, _short(hits),
                     "Remove the secret, rotate it if it was ever real, and read it from an environment variable instead. "
                     "If it is already committed, rewrite that commit (do not just add another).", required)
    return Check(name, True, "", "", required)


def forbid_patterns(
    work: Path | str,
    patterns: dict[str, str | re.Pattern[str]],
    *,
    globs: Sequence[str] = ("**/*.py",),
    since: str = LAB_START_TAG,
    ignore: Sequence[str] = TOOL_NOISE,
    name: str = "No forbidden constructs in the change",
    hint: str = "Look at CONTRIBUTING.md: the team's rules say why this is not allowed.",
    required: bool = True,
) -> Check:
    """None of the regexes in ``patterns`` ({label: regex}) match a line the learner added to a file in ``globs``.

    Example: ``forbid_patterns(work, {"float arithmetic": r"\\bfloat\\s*\\("})``. Only added lines are looked at, so
    code that was already in the repository never counts against the learner. Reports label and file, not the line.
    """
    compiled = {label: re.compile(rx) if isinstance(rx, str) else rx for label, rx in patterns.items()}
    hits: list[str] = []
    for path, text in added_text(work, since, ignore).items():
        if not gitutil.glob_match(path, globs):
            continue
        for label, rx in compiled.items():
            if any(rx.search(line) for line in text.splitlines()):
                hits.append(f"{label} in {path}")
    if hits:
        return Check(name, False, _short(hits), hint, required)
    return Check(name, True, "", "", required)


# =================================================================================
# 4. mutation checking
# =================================================================================
@dataclass(frozen=True)
class Mutant:
    """One deliberate defect: replace ``old`` with ``new`` in ``file`` (relative to the work dir).

    ``old`` must occur exactly ``count`` times. ``description`` is shown to the learner when the
    mutant survives, so describe the behaviour ("the 80% threshold"), never the code.
    """

    id: str
    file: str
    old: str
    new: str
    description: str = ""
    count: int = 1


@dataclass
class MutationReport:
    baseline_ok: bool
    baseline_summary: str
    killed: list[Mutant] = field(default_factory=list)
    survived: list[Mutant] = field(default_factory=list)
    not_applied: list[Mutant] = field(default_factory=list)  # the code no longer contains `old`

    @property
    def total(self) -> int:
        return len(self.killed) + len(self.survived) + len(self.not_applied)


def as_mutants(mutants: Iterable[Mutant | tuple[str, str, str]]) -> list[Mutant]:
    """Accept Mutant objects or plain (file, old, new) tuples (numbered M1, M2, ...)."""
    out: list[Mutant] = []
    for index, item in enumerate(mutants, start=1):
        out.append(item if isinstance(item, Mutant) else Mutant(f"M{index}", item[0], item[1], item[2]))
    return out


def new_test_files(work: Path | str, since: str = LAB_START_TAG, pattern: str = "tests/**/test_*.py") -> list[str]:
    """Test files the learner added or changed since the start (for ``mutants_killed(test_paths=...)``)."""
    return [p for p, state in gitutil.changed_status(work, since).items()
            if state != "D" and gitutil.glob_match(p, [pattern, "tests/test_*.py"])]


def mutants_killed(
    work: Path | str,
    mutants: Iterable[Mutant | tuple[str, str, str]],
    test_paths: Sequence[str] | None = None,
    *,
    timeout: float = 30.0,
) -> MutationReport:
    """Count how many deliberate defects the learner's tests would catch.

    The work directory is copied to a temporary folder. First the ``test_paths`` (default: the test
    files the learner added or changed, see ``new_test_files``) are run on the untouched copy; if they
    do not pass, no mutant is tried (``baseline_ok`` is False). Then each mutant is applied in turn, the
    tests are run (stopping at the first failure), and the file is restored. A mutant is *killed* when
    the tests fail, error or time out, and *survived* when they still pass. A mutant whose ``old`` text
    is no longer in the file is reported in ``not_applied``.
    """
    work = Path(work)
    chosen = list(test_paths) if test_paths is not None else new_test_files(work)
    plan = as_mutants(mutants)
    if not chosen:
        return MutationReport(False, "no test files to run")
    with work_copy(work) as root:
        chosen = [p for p in chosen if (root / p).exists()]
        if not chosen:
            return MutationReport(False, "none of the test files exist")
        base = _run_pytest_in(root, chosen, timeout=timeout, args=(), extra_env=None)
        report = MutationReport(base.ok, base.summary())
        if not base.ok:
            return report
        for mutant in plan:
            path = root / mutant.file
            original = path.read_text(encoding="utf-8") if path.is_file() else ""
            if original.count(mutant.old) != mutant.count:
                report.not_applied.append(mutant)
                continue
            path.write_text(original.replace(mutant.old, mutant.new), encoding="utf-8", newline="\n")
            try:
                result = _run_pytest_in(root, chosen, timeout=timeout, args=("-x",), extra_env=None)
            finally:
                path.write_text(original, encoding="utf-8", newline="\n")
            (report.survived if result.ok else report.killed).append(mutant)
    return report


def mutation_check(
    work: Path | str,
    mutants: Iterable[Mutant | tuple[str, str, str]],
    test_paths: Sequence[str] | None = None,
    *,
    min_killed: int | None = None,
    name: str = "Your tests catch real defects",
    timeout: float = 30.0,
    hint: str = "Add assertions that would fail if that behaviour broke: check the exact values, not just that nothing crashed.",
    required: bool = True,
) -> Check:
    """A Check around ``mutants_killed``: at least ``min_killed`` mutants (default: all) must be caught."""
    plan = as_mutants(mutants)
    report = mutants_killed(work, plan, test_paths, timeout=timeout)
    if not report.baseline_ok:
        return Check(name, False, f"your new tests do not pass on your own code ({report.baseline_summary})",
                     "Add tests in a new tests/test_*.py file and make them pass first.", required)
    need = len(plan) if min_killed is None else min_killed
    ok = len(report.killed) >= need
    detail = f"your tests catch {len(report.killed)} of {len(plan)} deliberate defects"
    survivors = [m.description or m.id for m in report.survived + report.not_applied]
    if not ok and survivors:
        detail += f"; they miss: {_short(survivors)}"
    return Check(name, ok, detail, "" if ok else hint, required)


def tests_fail_on_starter(
    work: Path | str,
    test_paths: Sequence[str] | None = None,
    *,
    since: str = LAB_START_TAG,
    keep: Sequence[str] = ("tests/**",),
    timeout: float = 60.0,
    name: str = "Your new tests fail on the original code",
    hint: str = "A test that passes before the fix proves nothing. Make it reproduce the problem first.",
    required: bool = True,
) -> Check:
    """The learner's new tests (default: test files added or changed since ``since``) FAIL on the starting code.

    This is the "regression test" check: the work directory is copied, every file that does not match
    ``keep`` (default: anything outside ``tests/``) is put back to its state at ``since``, and the chosen
    tests are run. They must fail (or error) there. Pair it with ``tests_pass(work, test_paths)`` to
    prove the same tests pass on the learner's fix.
    """
    work = Path(work)
    chosen = list(test_paths) if test_paths is not None else new_test_files(work, since)
    if not chosen:
        return Check(name, False, "no new or changed test files found", "Add a test in tests/test_*.py.", required)
    with work_copy(work) as root:
        for path, state in gitutil.changed_status(work, since, ignore=()).items():
            if gitutil.glob_match(path, keep):
                continue
            target = root / path
            original = None if state == "A" else gitutil.show_bytes(work, since, path)
            if original is None:
                target.unlink(missing_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(original)
        chosen = [p for p in chosen if (root / p).exists()]
        result = _run_pytest_in(root, chosen, timeout=timeout, args=(), extra_env=None)
    caught = result.failed + result.errors
    if result.timed_out or caught:
        return Check(name, True, f"{plural(caught, 'test')} fail on the original code, as they should" if caught
                     else "the tests do not finish on the original code", "", required)
    return Check(name, False, "all of your new tests already pass on the original code, so they would not have caught the problem",
                 hint, required)


# =================================================================================
# 5. JSON helpers (no third-party libraries)
# =================================================================================
_MISSING = object()


def load_json(path: Path | str) -> tuple[Any, str | None]:
    """Parse a JSON file. Returns (data, None) or (None, error message)."""
    import json

    try:
        return json.loads(Path(path).read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, f"{Path(path).name} does not exist"
    except (ValueError, UnicodeDecodeError) as exc:
        return None, f"{Path(path).name} is not valid JSON ({exc})"


def get_path(data: Any, path: str, default: Any = None) -> Any:
    """Read ``a.b[0].c`` from nested dicts and lists; ``default`` if any step is missing."""
    node = data
    for part in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        if part.startswith("["):
            index = int(part[1:-1])
            if not isinstance(node, list) or index >= len(node):
                return default
            node = node[index]
        else:
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
    return node


def json_has(data: Any, path: str, *, equals: Any = _MISSING, one_of: Iterable[Any] | None = None,
             type_: type | tuple[type, ...] | None = None, non_empty: bool = False) -> bool:
    """Is there a value at ``path`` (``a.b[0].c``) that satisfies the given conditions?"""
    value = get_path(data, path, _MISSING)
    if value is _MISSING:
        return False
    if equals is not _MISSING and value != equals:
        return False
    if one_of is not None and value not in list(one_of):
        return False
    if type_ is not None and (not isinstance(value, type_) or (type_ is int and isinstance(value, bool))):
        return False
    if non_empty and (value is None or (hasattr(value, "__len__") and len(value) == 0) or
                      (isinstance(value, str) and not value.strip())):
        return False
    return True


_TYPES: dict[str, Callable[[Any], bool]] = {
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "array": lambda v: isinstance(v, list),
    "object": lambda v: isinstance(v, dict),
    "null": lambda v: v is None,
}


def validate(data: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """Validate ``data`` against a small subset of JSON Schema; returns a list of error messages.

    Supported keywords: type (name or list of names), enum, const, required, properties,
    additionalProperties (false only), items, minItems, maxItems, minLength, maxLength, pattern,
    minimum, maximum. Unknown keywords are ignored.
    """
    errors: list[str] = []
    wanted = schema.get("type")
    if wanted is not None:
        names = [wanted] if isinstance(wanted, str) else list(wanted)
        if not any(_TYPES[n](data) for n in names):
            return [f"{path}: expected {' or '.join(names)}, got {type(data).__name__}"]
    if "enum" in schema and data not in schema["enum"]:
        errors.append(f"{path}: must be one of {schema['enum']}")
    if "const" in schema and data != schema["const"]:
        errors.append(f"{path}: must be {schema['const']!r}")
    if isinstance(data, str):
        if "minLength" in schema and len(data) < schema["minLength"]:
            errors.append(f"{path}: needs at least {schema['minLength']} characters")
        if "maxLength" in schema and len(data) > schema["maxLength"]:
            errors.append(f"{path}: at most {schema['maxLength']} characters")
        if "pattern" in schema and not re.search(schema["pattern"], data):
            errors.append(f"{path}: does not match the required pattern")
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        if "minimum" in schema and data < schema["minimum"]:
            errors.append(f"{path}: must be at least {schema['minimum']}")
        if "maximum" in schema and data > schema["maximum"]:
            errors.append(f"{path}: must be at most {schema['maximum']}")
    if isinstance(data, list):
        if "minItems" in schema and len(data) < schema["minItems"]:
            errors.append(f"{path}: needs at least {schema['minItems']} items")
        if "maxItems" in schema and len(data) > schema["maxItems"]:
            errors.append(f"{path}: at most {schema['maxItems']} items")
        if "items" in schema:
            for index, item in enumerate(data):
                errors += validate(item, schema["items"], f"{path}[{index}]")
    if isinstance(data, dict):
        for key in schema.get("required", []):
            if key not in data:
                errors.append(f"{path}: missing '{key}'")
        props = schema.get("properties", {})
        for key, sub in props.items():
            if key in data:
                errors += validate(data[key], sub, f"{path}.{key}")
        if schema.get("additionalProperties") is False:
            for key in data:
                if key not in props:
                    errors.append(f"{path}: unexpected '{key}'")
    return errors


def json_check(
    work: Path | str,
    rel: str,
    schema: dict[str, Any],
    *,
    name: str | None = None,
    hint: str = "Fix the file so it matches the structure described in the task.",
    required: bool = True,
) -> Check:
    """``rel`` exists, is valid JSON and matches ``schema`` (see ``validate``)."""
    label = name or f"{rel} is valid"
    data, error = load_json(Path(work) / rel)
    if error:
        return Check(label, False, error, hint, required)
    problems = validate(data, schema)
    if problems:
        return Check(label, False, _short(problems, 3), hint, required)
    return Check(label, True, "", "", required)


# =================================================================================
# 6. Markdown helpers
# =================================================================================
@dataclass
class Section:
    level: int
    title: str
    body: str  # text up to the next heading of any level (code fences respected)


_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def _norm(title: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[`*_]", "", title)).strip().lower()


def markdown_outline(source: Path | str) -> list[Section]:
    """Headings of a Markdown file (or text) with their bodies. ``#`` lines inside code fences are not headings."""
    text = Path(source).read_text(encoding="utf-8") if isinstance(source, Path) else source
    sections: list[Section] = []
    fence: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            fence = None if fence == marker else (fence or marker)
        match = None if fence else _HEADING.match(line)
        if match:
            sections.append(Section(len(match.group(1)), match.group(2).strip(), ""))
        elif sections:
            sections[-1].body += line + "\n"
    for section in sections:
        section.body = section.body.strip()
    return sections


def markdown_sections(source: Path | str) -> dict[str, str]:
    """Map normalised heading text (lower case, no markup) -> section body. Repeated titles get ' #2', ' #3'."""
    result: dict[str, str] = {}
    for section in markdown_outline(source):
        key = _norm(section.title)
        n = 2
        while key in result:
            key = f"{_norm(section.title)} #{n}"
            n += 1
        result[key] = section.body
    return result


def sections_check(
    work: Path | str,
    rel: str,
    required_sections: Sequence[str],
    *,
    min_words: int = 5,
    name: str | None = None,
    hint: str = "Use the section headings from the task, and write something under each.",
    required: bool = True,
) -> Check:
    """``rel`` exists and has a non-trivial section whose heading contains each required title (case-insensitive)."""
    label = name or f"{rel} has the required sections"
    path = Path(work) / rel
    if not path.is_file():
        return Check(label, False, f"{rel} does not exist", hint, required)
    sections = markdown_sections(path)
    missing, thin = [], []
    for wanted in required_sections:
        key = next((k for k in sections if _norm(wanted) in k), None)
        if key is None:
            missing.append(wanted)
        elif len(sections[key].split()) < min_words:
            thin.append(wanted)
    if missing or thin:
        parts = ([f"missing: {_short(missing)}"] if missing else []) + ([f"too short: {_short(thin)}"] if thin else [])
        return Check(label, False, "; ".join(parts), hint, required)
    return Check(label, True, "", "", required)


# =================================================================================
# 7. small file checks
# =================================================================================
def files_exist(work: Path | str, paths: Sequence[str], *, name: str = "Expected files exist",
                hint: str = "Create the files the task asks for.", required: bool = True) -> Check:
    missing = [p for p in paths if not (Path(work) / p).exists()]
    if missing:
        return Check(name, False, f"missing: {_short(missing)}", hint, required)
    return Check(name, True, "", "", required)


_COMPILE_SCRIPT = (
    "import pathlib, sys\n"
    "bad = []\n"
    "for top in sys.argv[1:]:\n"
    "    for f in sorted(pathlib.Path(top).rglob('*.py')):\n"
    "        try:\n"
    "            compile(f.read_text(encoding='utf-8'), str(f), 'exec')\n"
    "        except (SyntaxError, ValueError) as exc:\n"
    "            bad.append(f'{f}: {exc}')\n"
    "print('\\n'.join(bad))\n"
    "sys.exit(1 if bad else 0)\n"
)


def python_compiles(work: Path | str, paths: Sequence[str] = ("src", "tests"), *, name: str = "Python files compile",
                    required: bool = True) -> Check:
    """Every .py file under ``paths`` is syntactically valid (checked in a subprocess; nothing is written)."""
    existing = [p for p in paths if (Path(work) / p).exists()]
    if not existing:
        return Check(name, False, "nothing to compile", "", required)
    result = runner.run_python(["-c", _COMPILE_SCRIPT, *existing], cwd=work, timeout=60)
    if result.ok:
        return Check(name, True, "", "", required)
    return Check(name, False, _short(result.stdout.strip().splitlines() or ["compile failed"], 2),
                 "Fix the syntax error reported above.", required)


def public_api(work: Path | str, root: str = "src") -> dict[str, str]:
    """List the public functions, classes and methods under ``root`` without importing anything.

    Returns ``{"najmkit.ids.new_id": "(prefix: str) -> str", "remit.money.Money.zero": "(currency: str) -> Money", ...}``:
    dotted name -> signature text as written in the source (``self``/``cls`` dropped). Classes appear as
    ``"class"``. Names starting with an underscore are skipped. Handy for checking that documentation only
    claims functions that exist (parse the doc, look each name up here).
    """
    base = Path(work) / root
    api: dict[str, str] = {}

    def signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        args = ast.unparse(node.args)
        args = re.sub(r"^(self|cls)(,\s*)?", "", args)
        return f"({args})" + (f" -> {ast.unparse(node.returns)}" if node.returns else "")

    for path in sorted(base.rglob("*.py")):
        parts = list(path.relative_to(base).with_suffix("").parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
        module = ".".join(parts)
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
                api[f"{module}.{node.name}"] = signature(node)
            elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
                api[f"{module}.{node.name}"] = "class"
                for member in node.body:
                    if isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)) and not member.name.startswith("_"):
                        api[f"{module}.{node.name}.{member.name}"] = signature(member)
    return api
