#!/usr/bin/env python3
"""Your personal eval: validate it, check that its checks bite, score a tool's work, report.

Standard library only. Run it from anywhere inside the repository:

    python lab-assets/eval_runner.py validate    # tasks.jsonl: valid lines, fields, allowed commands, no network
    python lab-assets/eval_runner.py list        # one line per task
    python lab-assets/eval_runner.py baseline    # every check must FAIL on a clean copy; it prints why (read the reason)
    python lab-assets/eval_runner.py verify      # every reference must make its check PASS, and lazy answers must not
    python lab-assets/eval_runner.py prepare T03 --dir ../runs/T03     # a clean workspace for a tool; prints the prompt
    python lab-assets/eval_runner.py score T03 --dir ../runs/T03 --tool claude-code --model sonnet --minutes 7
    python lab-assets/eval_runner.py report      # pass counts per tool and model, from eval/results.jsonl (`score` appends there)

Options for every command: --tasks FILE (default eval/tasks.jsonl), --base REF (default lab-start), --repo DIR.

How the pieces fit. A task is a prompt plus a check. The tool works in a workspace made by `prepare`: a clean copy of
the repository at --base (with the task's setup patch applied and committed as "Eval start"), without eval/ and
lab-assets/, so it cannot read the check. `score` rebuilds that start, puts the tool's files on top (however it
committed), adds eval/ and lab-assets/, and runs the check there.

Where a check runs (the same in baseline, verify and score): from the root of a clean copy that is a git repository with
one commit, so `git diff` shows exactly what a solution changed; with PYTHONPATH=src; `python` and `pytest` mean the
interpreter that runs this file; no shell (no &&, no pipes), so put logic in a small script; relative paths with forward
slashes; at most TIMEOUT seconds per command. `validate` flags checks that use the network (they must stay offline, but
nothing blocks them). A check is code: read every check before you run it, yours or anyone's. The runner is NOT a
sandbox (a check runs as you); it only drops environment variables whose names look like secrets (KEY, TOKEN, SECRET,
PASSWORD). The course kit's grader imports this file, so `baseline` and `verify` say what the grader will say.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import io
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import zipfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

KINDS = ("fix", "feature", "refactor", "test", "docs", "explain", "review", "other")
REPOS = ("remit", "own")
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{1,23}$")
ALLOWED_PROGRAMS = ("pytest", "python", "python3", "grep", "git")
GIT_READ_ONLY = ("diff", "log", "show", "status", "grep", "ls-files", "rev-parse")
SHELL_OPERATORS = ("|", "||", "&&", ";", "&", ">", ">>", "<", "2>", "2>&1")
PATCH_ROOTS = ("eval/", "lab-assets/")
COURSE_FILES = ("eval", "lab-assets", "TASK.md")  # not product code: kept out of a tool's workspace
DEFAULT_BASE = "lab-start"
TIMEOUT = 60.0  # seconds per command (a busy machine can be slow; a hung command is still stopped)
MIN_REFERENCE_WORDS = 8  # a docs, explain or review reference is prose, not one pasted keyword
TEXT_KINDS = ("docs", "explain", "review")  # solutions that are prose

NETWORK = re.compile(
    r"https?://|\burllib\b|\bhttp\.client\b|\b(?:import|from)\s+(?:requests|httpx|socket|ftplib|smtplib|aiohttp)\b"
    r"|\b(?:requests|httpx)\.(?:get|post|put|delete|request|Session)\b|\bsocket\.|\bcurl\b|\bwget\b"
)
CLOCK = re.compile(r"\btime\.sleep\b|\bdatetime\.(?:now|utcnow|today)\b|\bdate\.today\b|\btime\.(?:time|monotonic)\(")
_IMPORT_FAIL = re.compile(r"ModuleNotFoundError: No module named '([^']+)'|ImportError: cannot import name '[^']+' from '([^']+)'")
_NO_MODULE = re.compile(r"No module named '?([\w.]+)'?")
_SYNTAX = re.compile(r"\b(?:SyntaxError|IndentationError|TabError)\b")
_NOT_FOUND = re.compile(r"file or directory not found: (\S+)")
OWN_FILES = ("eval/", "lab-assets/")  # a check's own files must exist; a file the tool is asked to create may not, yet


class RunnerError(Exception):
    """Something the person running the eval should be told plainly."""


# ----------------------------------------------------------------------------------------------
# tasks: read and validate
# ----------------------------------------------------------------------------------------------
def load_tasks(path: Path) -> tuple[list[dict], list[str]]:
    """Read a JSON Lines file. Returns (tasks, problems); every task gets a '_line' key."""
    path = Path(path)
    if not path.is_file():
        return [], [f"{path.name} does not exist"]
    tasks: list[dict] = []
    problems: list[str] = []
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except ValueError as exc:
            problems.append(f"line {number}: not valid JSON ({getattr(exc, 'msg', exc)}); write one complete object per line")
            continue
        if not isinstance(value, dict):
            problems.append(f"line {number}: expected one JSON object, found {type(value).__name__}; no arrays, one object per line")
            continue
        value["_line"] = number
        tasks.append(value)
    if not tasks and not problems:
        problems.append(f"{path.name} has no tasks")
    return tasks, problems


def label(task: dict) -> str:
    return f"{task.get('id', '?')} (line {task.get('_line', '?')})"


def parse_command(text: object) -> tuple[list[str] | None, str]:
    """Split a check command. Returns (argv, '') or (None, what is wrong). No shell is ever used."""
    if not isinstance(text, str) or not text.strip():
        return None, "the command is empty"
    if "\\" in text and text.split()[0] in ("pytest", "python", "python3") and not re.search(r"(^|\s)-c(\s|$)", text):
        return None, "write paths with forward slashes (eval/checks/check.py), also on Windows"  # shlex would silently eat the backslashes
    try:
        argv = shlex.split(text)
    except ValueError as exc:
        return None, f"cannot read the command ({exc})"
    for token in argv:
        if token in SHELL_OPERATORS:
            return None, f"'{token}' is a shell operator, and no shell is used: put the logic in a small script"
    if argv[0] not in ALLOWED_PROGRAMS:
        return None, f"'{argv[0]}' is not allowed here (use pytest, python, grep, or read-only git)"
    if argv[0] == "git" and (len(argv) < 2 or argv[1] not in GIT_READ_ONLY):
        return None, "git is allowed only for read-only commands: " + ", ".join(GIT_READ_ONLY)
    for index, token in enumerate(argv[1:], 1):
        if argv[index - 1] == "-c" and argv[0] in ("python", "python3"):
            continue  # inline code, not a path
        if token.startswith(("/", "~")) or ".." in PurePosixPath(token.replace("\\", "/")).parts:
            return None, f"'{token}': use paths relative to the repository root"
    return argv, ""


def _kind(argv: list[str]) -> str:
    if argv[0] == "pytest" or (argv[0] in ("python", "python3") and argv[1:3] == ["-m", "pytest"]):
        return "pytest"
    return {"python3": "python"}.get(argv[0], argv[0])


def task_problems(task: dict, repo: Path | None = None, *, commands: bool = True) -> list[str]:
    """What is wrong with one task's fields. With ``repo`` it also checks that the files it names exist;
    with ``commands`` it also checks that the check and guard commands are allowed."""
    problems: list[str] = []
    tid = task.get("id")
    if not isinstance(tid, str) or not ID_RE.match(tid):
        problems.append("id: 2 to 24 letters, digits, '-' or '_', starting with a letter (for example T01)")
    title = task.get("title")
    if not isinstance(title, str) or not 3 <= len(title.strip()) <= 80:
        problems.append("title: 3 to 80 characters")
    if task.get("kind") not in KINDS:
        problems.append("kind: one of " + ", ".join(KINDS))
    where = task.get("repo", "remit")
    if where not in REPOS:
        problems.append("repo: 'remit' (the default) or 'own'")
    prompt = task.get("prompt")
    if not isinstance(prompt, str) or len(prompt.split()) < 15:
        problems.append("prompt: the exact text you would give a tool, at least 15 words")
    check = task.get("check")
    if not isinstance(check, dict) or not isinstance(check.get("run"), str) or not check["run"].strip():
        problems.append("check.run: the command that decides pass or fail")
        return problems
    if "guard" in check and (not isinstance(check["guard"], str) or not check["guard"].strip()):
        problems.append("check.guard: a command, or leave it out")
    if where == "own":
        return problems
    for field_name in ("run", "guard") if commands else ():
        if isinstance(check.get(field_name), str):
            argv, why = parse_command(check[field_name])
            if argv is None:
                problems.append(f"check.{field_name}: {why}")
    for key in ("setup", "reference"):
        value = task.get(key)
        if value is None:
            continue
        if not isinstance(value, str) or not value.startswith(PATCH_ROOTS) or ".." in value or not value.endswith((".patch", ".diff")):
            problems.append(f"{key}: a .patch file under eval/ (for example eval/{key}/{tid or 'T01'}.patch)")
        elif repo is not None and not (Path(repo) / value).is_file():
            problems.append(f"{key}: {value} does not exist")
    return problems


def check_files(repo: Path, tasks: list[dict]) -> list[Path]:
    """The files the checks are made of: everything under eval/checks plus any .py a command names."""
    repo = Path(repo)
    found: set[Path] = set()
    checks_dir = repo / "eval" / "checks"
    if checks_dir.is_dir():
        found.update(p for p in checks_dir.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    for task in tasks:
        check = task.get("check") if isinstance(task.get("check"), dict) else {}
        for name in ("run", "guard"):
            argv, _ = parse_command(check.get(name))
            for token in argv or []:
                candidate = repo / token
                if token.endswith(".py") and candidate.is_file():
                    found.add(candidate)
    return sorted(found)


def lint(repo: Path, tasks: list[dict]) -> dict[str, list[str]]:
    """Static findings: 'network' (a check that needs the internet is flaky) and 'clock' (time makes it nondeterministic)."""
    findings: dict[str, list[str]] = {"network": [], "clock": []}
    sources: list[tuple[str, str]] = []
    for path in check_files(repo, tasks):
        try:
            sources.append((path.relative_to(repo).as_posix(), path.read_text(encoding="utf-8")))
        except (UnicodeDecodeError, OSError):
            continue
    for task in tasks:
        check = task.get("check") if isinstance(task.get("check"), dict) else {}
        for name in ("run", "guard"):
            if isinstance(check.get(name), str):
                sources.append((f"{task.get('id', '?')} check.{name}", check[name]))
    for where, text in sources:
        for number, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            if NETWORK.search(line):
                findings["network"].append(f"{where}:{number}")
            if CLOCK.search(line):
                findings["clock"].append(f"{where}:{number}")
    return findings


def patch_files(patch_text: str) -> tuple[list[str], list[str]]:
    """(created, modified) paths of a patch. Deleted and renamed files are left out."""
    entries: list[list] = []
    for line in patch_text.splitlines():
        if line.startswith("diff --git "):
            match = re.match(r"diff --git a/(.+) b/(.+)$", line)
            entries.append([match.group(2) if match else None, "modified"])
        elif entries and line.startswith("new file mode"):
            entries[-1][1] = "created"
        elif entries and line.startswith(("deleted file mode", "rename from", "rename to")):
            entries[-1][1] = "other"
    return [p for p, k in entries if p and k == "created"], [p for p, k in entries if p and k == "modified"]


def new_files_in_patch(patch_text: str) -> list[str]:
    """Paths the patch creates."""
    return patch_files(patch_text)[0]


def changed_words(patch_text: str) -> int:
    """Words on the added and removed lines of a patch."""
    return sum(len(line[1:].split()) for line in patch_text.splitlines()
               if line[:1] in "+-" and not line.startswith(("+++", "---")))


def reference_problem(task: dict, patch_text: str) -> str:
    """A text reference (a docs, explain or review solution, or any patch that touches only text files) that changes a
    word or two is a keyword, not a solution."""
    created, modified = patch_files(patch_text)
    files = created + modified
    text_only = bool(files) and all(PurePosixPath(path).suffix in (".md", ".markdown", ".txt", ".rst") for path in files)
    n = changed_words(patch_text)
    if (task.get("kind") in TEXT_KINDS or text_only) and n < MIN_REFERENCE_WORDS:
        return f"the reference changes only {n} word{'' if n == 1 else 's'}: a text solution is real prose (at least {MIN_REFERENCE_WORDS} words)"
    return ""


FILLER = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna "
          "aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
          "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur "
          "sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n")
TEXT_SUFFIXES = (".md", ".markdown", ".txt", ".rst", ".csv", ".html", ".yaml", ".yml", ".toml", ".cfg", ".ini", "")
EDIT_SUFFIXES = (".md", ".markdown", ".txt", ".rst", ".py")


def lazy_answers(path: str, prompt: str = "") -> list[tuple[str, str]]:
    """What a lazy tool leaves in a file it was asked to create: (description, content). Several for a note,
    because 'TODO' is only one way to say nothing: filler of a realistic length, or the prompt handed back."""
    name = PurePosixPath(path)
    if name.suffix == ".py":
        if name.name.startswith("test_") or name.name.endswith("_test.py"):
            return [("a test that asserts nothing", "def test_placeholder():\n    assert True\n")]
        return [("an empty module", "# TODO\n")]
    if name.suffix == ".json":
        return [("an empty JSON object", "{}\n")]
    if name.suffix in TEXT_SUFFIXES:
        found = [("a placeholder", "TODO\n"), ("filler text", FILLER)]
        if prompt.strip():
            found.append(("the prompt copied back", prompt.strip() + "\n"))
        return found
    return []


def stray_line(path: str) -> str:
    return "\n# TODO\n" if PurePosixPath(path).suffix == ".py" else "\nTODO\n"


# ----------------------------------------------------------------------------------------------
# workspaces: a clean copy of the repository, optionally with a planted bug or a known-good solution
# ----------------------------------------------------------------------------------------------
def _git(*args: str, cwd: Path | None = None, text: bool = True) -> subprocess.CompletedProcess:
    """Run git without the GIT_* variables of the caller's shell (a stray GIT_DIR would point it somewhere else)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", *args], cwd=None if cwd is None else str(cwd), env=env, capture_output=True, text=text)


def find_repo(start: Path | None = None) -> Path:
    here = Path(start or Path.cwd())
    result = _git("rev-parse", "--show-toplevel", cwd=here)
    return Path(result.stdout.strip()) if result.returncode == 0 and result.stdout.strip() else here


def export_tree(repo: Path, ref: str, dest: Path) -> None:
    """Write the files of ``ref`` (no .git) into ``dest``."""
    result = _git("-C", str(repo), "archive", "--format=zip", ref, text=False)
    if result.returncode:
        raise RunnerError(f"cannot read '{ref}' from {repo}: {result.stderr.decode(errors='replace').strip() or 'git failed'}")
    Path(dest).mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(result.stdout)) as archive:
        archive.extractall(dest)


def _git_init(workspace: Path) -> None:
    if not (workspace / ".git").exists():
        _git("init", "-q", cwd=workspace)


def apply_patch(workspace: Path, patch: Path, *, key: str = "patch") -> None:
    _git_init(workspace)
    if not Path(patch).is_file():
        extra = (" Leave `setup` out of the task until the patch is saved: `prepare` the task, plant the bug in that copy, "
                 "save its `git diff` to this path, then add `setup` to the task.") if key == "setup" else ""
        raise RunnerError(f"{key} patch {Path(patch).name} does not exist yet.{extra}")
    result = _git("apply", "--whitespace=nowarn", str(patch), cwd=workspace)
    if result.returncode:
        reason = (result.stderr.strip().splitlines() or ["git apply failed"])[0]
        raise RunnerError(f"{Path(patch).name} does not apply to a clean copy: {reason}")


def remove_course_files(workspace: Path) -> None:
    for name in COURSE_FILES:
        target = workspace / name
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()


_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache", ".git")


def overlay_checks(repo: Path, workspace: Path) -> None:
    """Put eval/ and lab-assets/ (the checks) into a workspace, right before a check runs."""
    for name in ("eval", "lab-assets"):
        source = Path(repo) / name
        if source.is_dir():
            shutil.copytree(source, workspace / name, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "results.jsonl"))


def commit_start(workspace: Path, task: dict) -> None:
    """Commit the starting state (the clean copy plus the setup patch), so `git diff` shows what a solution changed."""
    _git("add", "-A", cwd=workspace)
    _git("-c", "user.name=eval", "-c", "user.email=eval@example.invalid", "-c", "commit.gpgsign=false", "commit", "-q",
         "--allow-empty", "-m", f"Eval start: {task.get('id', 'task')}", cwd=workspace)


def make_workspace(repo: Path, base: str, task: dict, dest: Path, *, reference: bool = False, with_checks: bool = True) -> None:
    """A clean copy at ``base`` with the task's setup patch applied and committed; the reference patch (when asked) is
    applied on top, uncommitted, and the checks (eval/, lab-assets/) are copied in last."""
    repo, dest = Path(repo), Path(dest)
    export_tree(repo, base, dest)
    remove_course_files(dest)
    _git_init(dest)
    if task.get("setup"):
        apply_patch(dest, repo / task["setup"], key="setup")
    commit_start(dest, task)
    if reference and task.get("reference"):
        apply_patch(dest, repo / task["reference"], key="reference")
    if with_checks:
        overlay_checks(repo, dest)


def sync_tree(source: Path, workspace: Path) -> None:
    """Make the workspace hold exactly the files of ``source`` (the folder a tool worked in), keeping the workspace's own
    .git: whether the tool committed or not, `git diff` then shows its net change from the starting commit."""
    for entry in list(Path(workspace).iterdir()):
        if entry.name != ".git":
            shutil.rmtree(entry) if entry.is_dir() else entry.unlink()
    shutil.copytree(source, workspace, dirs_exist_ok=True, ignore=_IGNORE)


# ----------------------------------------------------------------------------------------------
# running a check
# ----------------------------------------------------------------------------------------------
@dataclass
class Outcome:
    verdict: str  # 'pass', 'fail' (it ran and said no), or 'broken' (it could not give an answer)
    detail: str = ""
    seconds: float = 0.0

    @property
    def passed(self) -> bool:
        return self.verdict == "pass"


SECRET_NAME = re.compile(r"KEY|TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL", re.I)  # a check is someone's code: it gets none of these


def _env(root: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("REMIT_", "NAJMKIT_", "PYTEST_", "GIT_")) and k not in ("PYTHONPATH", "PYTHONSTARTUP", "PYTHONINSPECT", "PYTHONOPTIMIZE")
           and not SECRET_NAME.search(k)}
    env.update(PYTHONPATH=str(Path(root) / "src"), PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", PYTHONIOENCODING="utf-8",
               PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTEST_ADDOPTS="-p no:cacheprovider", NO_COLOR="1")
    return env


def _executable(argv: list[str]) -> list[str] | None:
    if argv[0] == "pytest":
        return [sys.executable, "-m", "pytest", *argv[1:]]
    if argv[0] in ("python", "python3"):
        return [sys.executable, *argv[1:]]
    found = shutil.which(argv[0])
    return [found, *argv[1:]] if found else None


def _last_line(text: str) -> str:
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    return lines[-1][:160] if lines else ""


def _first_failure(out: str) -> str:
    """The first FAILED/ERROR line of a pytest run (it names the test and the reason), else the last line."""
    for line in out.splitlines():
        if line.startswith(("FAILED ", "ERROR ")):
            return line.strip()[:200]
    return _last_line(out)


def _missing_imports(text: str) -> list[str]:
    return [a or b for a, b in _IMPORT_FAIL.findall(text)]


def classify(argv: list[str], code: int, out: str, err: str) -> tuple[str, str]:
    """Turn an exit status into 'pass', 'fail' (the work is not done) or 'broken' (the check itself is at fault)."""
    if code == 0:
        return "pass", ""
    kind = _kind(argv)
    text = out + "\n" + err
    ours = ("remit", "najmkit")
    if kind == "pytest":
        if "No module named pytest" in err or "No module named 'pytest'" in err:
            return "broken", "pytest is not installed for the Python that runs this eval (python -m pip install pytest)"
        if code == 1:
            return "fail", _first_failure(out)
        if code == 5:
            return "broken", "pytest collected no tests: check the path and any -k expression"
        if code == 4:
            missing_file = _NOT_FOUND.search(text)
            if missing_file:
                target = missing_file.group(1).replace("\\", "/").removeprefix("./")
                if target.startswith(OWN_FILES):
                    return "broken", f"the check file {target} does not exist"
                return "fail", f"{target} does not exist yet"
            return "broken", "pytest could not use that command line: " + (_last_line(err) or _last_line(out))
        if code == 2:
            if _SYNTAX.search(text):
                return "broken", "the check has a syntax error"
            missing = _missing_imports(text)
            if missing and all(name.split(".")[0] in ours for name in missing):
                return "fail", "the code under test does not exist yet (" + missing[0] + ")"
            return "broken", "pytest could not collect the check: " + (_last_line(err) or _last_line(out))
        return "broken", f"pytest stopped with exit code {code}: " + _last_line(out)
    if kind == "python":
        if "can't open file" in err:
            script = next((a for a in argv[1:] if a.endswith(".py")), "").replace("\\", "/").removeprefix("./")
            if script and not script.startswith(OWN_FILES):
                return "fail", f"{script} does not exist yet"
            return "broken", f"the script {script or '(unnamed)'} does not exist"
        if _SYNTAX.search(err):
            return "broken", "the check has a syntax error"
        missing = _missing_imports(err) or _NO_MODULE.findall(err)
        if missing:
            if all(name.split(".")[0] in ours for name in missing):
                return "fail", "the code under test does not exist yet (" + missing[0] + ")"
            return "broken", f"the check needs a module that is not installed: {missing[0]}"
        return "fail", _last_line(err) or _last_line(out)
    if kind == "grep":
        if code == 1:
            return "fail", "no match"
        if code == 2 and "No such file or directory" in err:
            return "fail", "the file is not there yet"
        return "broken", "grep reported an error: " + _last_line(err)
    if kind == "git" and code == 128:
        return "broken", "git failed: " + _last_line(err)
    return "fail", _last_line(err) or _last_line(out)


def run_check(command: str, cwd: Path, timeout: float | None = None) -> Outcome:
    argv, problem = parse_command(command)
    if argv is None:
        return Outcome("broken", problem)
    exe = _executable(argv)
    if exe is None:
        return Outcome("broken", f"'{argv[0]}' was not found on this machine")
    limit = TIMEOUT if timeout is None else timeout
    started = time.monotonic()
    try:
        proc = subprocess.Popen(exe, cwd=str(cwd), env=_env(Path(cwd)), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace",
                                start_new_session=(os.name == "posix"))
    except OSError as exc:
        return Outcome("broken", f"cannot start the command: {exc}")
    try:
        out, err = proc.communicate(timeout=limit)
    except subprocess.TimeoutExpired:
        try:
            if os.name == "posix":
                os.killpg(proc.pid, signal.SIGKILL)
            else:  # pragma: no cover
                proc.kill()
        except (ProcessLookupError, PermissionError):
            pass
        proc.communicate()
        return Outcome("broken", f"did not finish within {limit:g} s (too slow, or waiting for input)", time.monotonic() - started)
    verdict, detail = classify(argv, proc.returncode, out or "", err or "")
    for spelling in {str(Path(cwd)), str(Path(cwd).resolve())}:
        detail = detail.replace(spelling + os.sep, "").replace(spelling, ".")  # no temporary folder names in messages
    return Outcome(verdict, detail, time.monotonic() - started)


# ----------------------------------------------------------------------------------------------
# evaluating a task: baseline (nothing done) and reference (known-good solution)
# ----------------------------------------------------------------------------------------------
@dataclass
class TaskReport:
    task_id: str
    skipped: str = ""  # why nothing ran (an 'own' task)
    error: str = ""  # a setup or reference patch that does not apply
    baseline: Outcome | None = None  # the check on the untouched repository: it should FAIL
    guard_baseline: Outcome | None = None  # the guard on the untouched repository: it should PASS
    reference: Outcome | None = None  # the check after the reference solution: it should PASS
    guard_reference: Outcome | None = None  # the guard after the reference solution: it should PASS
    placeholders: list[tuple[str, Outcome]] = field(default_factory=list)  # (lazy answer, outcome): the check should FAIL each
    reference_issue: str = ""  # a reference too thin to be a solution (docs, explain and review tasks)


def _cached(cache: dict | None, key: tuple, compute):
    if cache is None:
        return compute()
    if key not in cache:
        cache[key] = compute()
    return cache[key]


def evaluate(repo: Path, base: str, task: dict, *, run_baseline: bool = True, run_reference: bool = True,
             cache: dict | None = None) -> TaskReport:
    """Run one task's check (and guard) on the untouched repository and on the reference solution, then try lazy answers."""
    report = TaskReport(str(task.get("id", "?")))
    if task.get("repo", "remit") == "own":
        report.skipped = "a task from your own project: the kit cannot run it"
        return report
    check = task["check"]
    guard = check.get("guard")
    setup, reference = task.get("setup"), task.get("reference")
    try:
        if run_baseline:
            with tempfile.TemporaryDirectory(prefix="eval-") as tmp:
                ws = Path(tmp) / "ws"
                make_workspace(repo, base, task, ws)
                report.baseline = run_check(check["run"], ws)
                if guard:
                    report.guard_baseline = _cached(cache, ("guard", setup, None, guard), lambda: run_check(guard, ws))
        if run_reference and reference:
            patch_text = (Path(repo) / reference).read_text(encoding="utf-8")
            report.reference_issue = reference_problem(task, patch_text)
            created, modified = patch_files(patch_text)
            with tempfile.TemporaryDirectory(prefix="eval-") as tmp:
                ws = Path(tmp) / "ws"
                make_workspace(repo, base, task, ws, reference=True)
                report.reference = run_check(check["run"], ws)
                if guard:
                    report.guard_reference = run_check(guard, ws)
                for path in created:  # a file the reference creates, replaced by each way of saying nothing
                    answers = lazy_answers(path, str(task.get("prompt", "")))
                    target = ws / path
                    if not answers or not target.is_file():
                        continue
                    original = target.read_text(encoding="utf-8")
                    target.unlink()
                    needed = not run_check(check["run"], ws).passed  # if it passes without the file, the check does not read it
                    for what, text in answers if needed else []:
                        target.write_text(text, encoding="utf-8")
                        report.placeholders.append((f"{what} in {path}", run_check(check["run"], ws)))
                    target.write_text(original, encoding="utf-8")
            edited = [path for path in modified if PurePosixPath(path).suffix in EDIT_SUFFIXES]
            if edited:  # a lazy edit: the starting state plus a stray line in each file the reference edits
                with tempfile.TemporaryDirectory(prefix="eval-") as tmp:
                    ws = Path(tmp) / "ws"
                    make_workspace(repo, base, task, ws)
                    for path in edited:
                        if (ws / path).is_file():
                            with (ws / path).open("a", encoding="utf-8") as handle:
                                handle.write(stray_line(path))
                    report.placeholders.append((f"a stray line in {', '.join(edited[:2])}", run_check(check["run"], ws)))
    except RunnerError as exc:
        report.error = str(exc)
    return report


def evaluate_all(repo: Path, base: str, tasks: list[dict], *, workers: int = 4, **kwargs) -> list[TaskReport]:
    """Evaluate every task (in parallel, results in task order)."""
    cache: dict = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        return list(pool.map(lambda t: evaluate(repo, base, t, cache=cache, **kwargs), tasks))


# ----------------------------------------------------------------------------------------------
# command line
# ----------------------------------------------------------------------------------------------
def _add_common(parser: argparse.ArgumentParser, *, suppress: bool) -> None:
    """The options every command takes. On a sub-command they use SUPPRESS so they work before or after the command."""
    def default(value):
        return argparse.SUPPRESS if suppress else value

    parser.add_argument("--tasks", default=default(None), help="the tasks file (default: eval/tasks.jsonl in the repository)")
    parser.add_argument("--base", default=default(DEFAULT_BASE), help="git ref of the clean starting state (default: lab-start)")
    parser.add_argument("--repo", default=default(None), help="the repository (default: the one you are in)")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="eval_runner.py", description="Run and check your personal eval.")
    _add_common(parser, suppress=False)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "list", "baseline", "verify", "report", "prepare", "score"):
        p = sub.add_parser(name)
        _add_common(p, suppress=True)
        if name not in ("prepare", "score"):
            continue
        p.add_argument("task", help="the task id, for example T03")
        p.add_argument("--dir", required=True, help="the workspace folder" + (" (new or empty)" if name == "prepare" else " the tool worked in"))
    score = sub.choices["score"]
    score.add_argument("--tool", required=True, help="for example claude-code, or 'me' for a no-AI run")
    score.add_argument("--model", default="")
    score.add_argument("--minutes", type=float, default=None, help="how long the run took, by your clock")
    score.add_argument("--note", default="", help="what you had to correct")
    score.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")
    score.add_argument("--no-record", action="store_true", help="do not append to eval/results.jsonl")
    return parser


def _context(args: argparse.Namespace) -> tuple[Path, Path, list[dict], list[str]]:
    repo = Path(args.repo) if args.repo else find_repo()
    path = Path(args.tasks) if args.tasks else repo / "eval" / "tasks.jsonl"
    tasks, problems = load_tasks(path)
    return repo, path, tasks, problems


def _results_path(repo: Path) -> Path:
    return Path(repo) / "eval" / "results.jsonl"


def _full_problems(repo: Path, tasks: list[dict], problems: list[str]) -> list[str]:
    problems = list(problems)
    seen: dict[str, int] = {}
    for task in tasks:
        problems += [f"{label(task)}: {p}" for p in task_problems(task, repo)]
        tid = task.get("id")
        if isinstance(tid, str):
            if tid in seen:
                problems.append(f"{label(task)}: id {tid} is already used on line {seen[tid]}")
            seen.setdefault(tid, task["_line"])
    return problems


def _line(task: dict, text: str) -> str:
    return f"{str(task.get('id', '?')):<6}{str(task.get('kind', '?')):<10}{text}"


def cmd_validate(args: argparse.Namespace, out) -> int:
    repo, path, tasks, problems = _context(args)
    problems = _full_problems(repo, tasks, problems)
    for kind, spots in lint(repo, tasks).items():
        if spots and kind == "network":
            problems.append("checks must work offline; found network use at " + ", ".join(spots[:4]))
        elif spots:
            print(f"note: these checks read the clock, which makes them nondeterministic: {', '.join(spots[:4])}", file=out)
    for problem in problems:
        print(f"problem: {problem}", file=out)
    print(f"{len(tasks)} tasks read from {path.name}; {len(problems)} problems", file=out)
    return 1 if problems else 0


def cmd_list(args: argparse.Namespace, out) -> int:
    _, _, tasks, problems = _context(args)
    for problem in problems:
        print(f"problem: {problem}", file=out)
    for task in tasks:
        print(_line(task, f"{task.get('title', '')}" + ("  [own project]" if task.get("repo") == "own" else "")), file=out)
    return 1 if problems else 0


def _describe(outcome: Outcome | None, want_pass: bool, what: str) -> tuple[bool, str]:
    if outcome is None:
        return True, ""
    if outcome.verdict == "broken":
        return False, f"{what} is BROKEN ({outcome.detail})"
    if want_pass and not outcome.passed:
        return False, f"{what} FAILS but should pass" + (f" ({outcome.detail})" if outcome.detail else "")
    if not want_pass and outcome.passed:
        return False, f"{what} PASSES but nothing is done yet: it proves nothing"
    return True, ""


def cmd_baseline(args: argparse.Namespace, out) -> int:
    repo, _, tasks, problems = _context(args)
    bad = bool(_full_problems(repo, tasks, problems))
    if bad:
        print("Fix `validate` first.", file=out)
        return 1
    reports = evaluate_all(repo, args.base, tasks, run_reference=False)
    failures = 0
    for task, report in zip(tasks, reports):
        if report.skipped:
            print(_line(task, f"not run: {report.skipped}"), file=out)
            continue
        if report.error:
            print(_line(task, f"setup problem: {report.error}"), file=out)
            failures += 1
            continue
        ok1, why1 = _describe(report.baseline, False, "the check")
        ok2, why2 = _describe(report.guard_baseline, True, "the guard")
        if ok1 and ok2:
            reason = f" ({report.baseline.detail})" if report.baseline and report.baseline.detail else ""
            print(_line(task, "ok: the check fails on the untouched repository" + reason
                        + (", the guard passes" if report.guard_baseline else "")), file=out)
        else:
            print(_line(task, why1 or why2), file=out)
            failures += 1
    print(f"{failures} problems", file=out)
    return 1 if failures else 0


def cmd_verify(args: argparse.Namespace, out) -> int:
    repo, _, tasks, problems = _context(args)
    if _full_problems(repo, tasks, problems):
        print("Fix `validate` first.", file=out)
        return 1
    reports = evaluate_all(repo, args.base, tasks, run_baseline=False)
    failures = 0
    for task, report in zip(tasks, reports):
        if report.skipped:
            print(_line(task, f"not run: {report.skipped}"), file=out)
            continue
        if not task.get("reference"):
            print(_line(task, "MISSING: every task on this repository needs a `reference`, a patch that solves it"), file=out)
            failures += 1
            continue
        if report.error:
            print(_line(task, f"reference problem: {report.error}"), file=out)
            failures += 1
            continue
        ok1, why1 = _describe(report.reference, True, "the check after the reference")
        ok2, why2 = _describe(report.guard_reference, True, "the guard after the reference")
        weak = [what for what, outcome in report.placeholders if outcome.passed]
        if ok1 and ok2 and not weak and not report.reference_issue:
            tried = (f", and {len(report.placeholders)} lazy answers do not" if len(report.placeholders) != 1 else ", and a lazy answer does not")
            print(_line(task, "ok: the reference passes" + (tried if report.placeholders else "; no lazy-answer probe applied")), file=out)
        else:
            print(_line(task, why1 or why2 or report.reference_issue or f"{weak[0]} passes the check: it is too weak"), file=out)
            failures += 1
    print(f"{failures} problems", file=out)
    return 1 if failures else 0


def _find(tasks: list[dict], task_id: str) -> dict:
    for task in tasks:
        if task.get("id") == task_id:
            return task
    raise RunnerError(f"no task {task_id!r} in the tasks file")


def cmd_prepare(args: argparse.Namespace, out) -> int:
    repo, _, tasks, _ = _context(args)
    task = _find(tasks, args.task)
    dest = Path(args.dir)
    if dest.exists() and any(dest.iterdir()):
        raise RunnerError(f"{dest} is not empty; choose a new folder")
    make_workspace(repo, args.base, task, dest, with_checks=False)
    print(f"A clean workspace for {task['id']} is ready in {dest} (no eval/, no checks). Give your tool this prompt:\n", file=out)
    print(task["prompt"], file=out)
    print(f"\nWhen it is done: python {Path(sys.argv[0]).as_posix()} score {task['id']} --dir {dest} --tool <name> --minutes <n>", file=out)
    return 0


def cmd_score(args: argparse.Namespace, out) -> int:
    repo, path, tasks, _ = _context(args)
    task = _find(tasks, args.task)
    if task.get("repo", "remit") == "own":
        raise RunnerError("this task comes from your own project: run its check there by hand")
    source = Path(args.dir)
    if not source.is_dir():
        raise RunnerError(f"{source} is not a folder")
    with tempfile.TemporaryDirectory(prefix="eval-") as tmp:
        ws = Path(tmp) / "ws"
        make_workspace(repo, args.base, task, ws, with_checks=False)  # the start the tool had, committed
        sync_tree(source, ws)  # the tool's files on top, however it committed
        remove_course_files(ws)
        overlay_checks(repo, ws)
        outcome = run_check(task["check"]["run"], ws)
        guard = task["check"].get("guard")
        guard_outcome = run_check(guard, ws) if guard else None
    if outcome.verdict == "broken" or (guard_outcome and guard_outcome.verdict == "broken"):
        broken = outcome if outcome.verdict == "broken" else guard_outcome
        raise RunnerError(f"the check could not give an answer: {broken.detail}")
    passed = outcome.passed and (guard_outcome is None or guard_outcome.passed)
    print(f"{task['id']}: {'PASS' if passed else 'FAIL'}"
          + ("" if outcome.passed else f" (check: {outcome.detail or 'failed'})")
          + ("" if guard_outcome is None or guard_outcome.passed else f" (guard: {guard_outcome.detail or 'failed'})"), file=out)
    if not args.no_record:
        record = {"task": task["id"], "tool": args.tool, "model": args.model, "passed": passed,
                  "check": outcome.verdict, "guard": None if guard_outcome is None else guard_outcome.verdict,
                  "minutes": args.minutes, "note": args.note, "base": args.base,
                  "date": args.date or datetime.date.today().isoformat()}
        results = _results_path(repo)  # always eval/results.jsonl, whichever tasks file you scored from
        results.parent.mkdir(parents=True, exist_ok=True)
        with results.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"recorded in {results.name}", file=out)
    return 0 if passed else 1


def cmd_report(args: argparse.Namespace, out) -> int:
    repo, _, tasks, _ = _context(args)
    results, problems = load_tasks(_results_path(repo))
    if problems and not results:
        print("no results yet: use `score` after a run", file=out)
        return 0
    ids = [str(t.get("id")) for t in tasks]
    groups: dict[tuple[str, str], dict[str, list[bool]]] = {}
    for row in results:
        if str(row.get("task", "?")) in ids:  # only the tasks of the file you asked about
            groups.setdefault((str(row.get("tool", "?")), str(row.get("model", ""))), {}).setdefault(str(row.get("task", "?")), []).append(bool(row.get("passed")))
    print(f"{'tool / model':<28}" + "".join(f"{i:>6}" for i in ids) + "   total", file=out)
    for (tool, model), by_task in sorted(groups.items()):
        cells = []
        for tid in ids:
            runs = by_task.get(tid)
            cells.append(f"{sum(runs)}/{len(runs)}" if runs else "-")
        passes = sum(sum(v) for v in by_task.values())
        total = sum(len(v) for v in by_task.values())
        print(f"{(tool + ' ' + model).strip():<28}" + "".join(f"{c:>6}" for c in cells) + f"   {passes}/{total}", file=out)
    return 0


COMMANDS = {"validate": cmd_validate, "list": cmd_list, "baseline": cmd_baseline, "verify": cmd_verify,
            "prepare": cmd_prepare, "score": cmd_score, "report": cmd_report}


def main(argv: list[str] | None = None, out=None) -> int:
    out = out or sys.stdout
    args = _parser().parse_args(argv)
    try:
        return COMMANDS[args.command](args, out)
    except RunnerError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
