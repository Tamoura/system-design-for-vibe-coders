"""Helpers that only lab m02 uses (kept out of ``checks.py``, which belongs to the kit): the project-memory
lint and the A/B notes check.

What "lint" means here
----------------------
A project memory file (``CLAUDE.md``, or ``AGENTS.md``) is context, not code, so nothing compiles it. This module
reads it the way a reviewer would and asks a fixed list of questions about it, each of which has a mechanical
answer in the repository:

* Is it the right size?                       (counts lines, imports included: an import costs context too)
* Do the commands in it work?                 (they are EXECUTED, in a throw-away copy, never through a shell)
* Does it say what the repo really does?      (Decimal money, test layout, the commit rule, najmkit)
* Does it name real files?                    (every path it mentions must exist)
* Is it free of filler and stale facts?       (phrases that say nothing; claims the architecture doc still makes
                                               but the code no longer does)
* Does it point instead of restating?         (a memory that copies the README is paid for twice)

What the lint cannot tell: whether the file is *useful* to an agent. It checks the shape of a good file, not the
judgement behind it. The lesson says so, and the A/B part of the lab is where usefulness is measured.

Safety: the only commands the lint ever runs are ``pytest ...`` and ``python -m remit ...`` with a short list of
options it recognises, as plain argument lists (no shell), in a copy of the learner's directory, with a scrubbed
environment, a temporary database and a timeout. Everything else in a code block is read, never run.
"""
from __future__ import annotations

import ast
import fnmatch
import re
import shlex
import tempfile
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from ailab import checks, gitutil, runner
from ailab.framework import LAB_START_TAG, Check

# ---------------------------------------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------------------------------------
MEMORY_CANDIDATES = ("CLAUDE.md", ".claude/CLAUDE.md", "AGENTS.md")  # the order Claude Code prefers them in
RULES_DIR = ".claude/rules"
MAX_IMPORT_DEPTH = 4  # the documented limit on @-imports
NOTES_FILE = "ab-notes.md"

# Files the learner may change in this lab.
ALLOWED_FILES = ("CLAUDE.md", "AGENTS.md", ".claude/CLAUDE.md", ".claude/rules/**", NOTES_FILE)

MIN_LINES = 15  # fewer non-blank lines than this cannot hold the essentials
MAX_LINES = 150  # the documented guideline is "under 200"; Remit is small
MIN_POINTERS = 3
MAX_COMMANDS_RUN = 8

# Check names (the tests refer to them, so they are constants).
N_EXISTS = "A project memory file exists"
N_SIZE = "The memory file is a sensible size"
N_COMMANDS = "The documented commands run and work"
N_MONEY = "Money is Decimal, never float"
N_TESTS = "The test layout is described correctly"
N_COMMITS = "The commit rule is stated correctly"
N_NAJMKIT = "najmkit is explained and pointed to"
N_NEVER = "A short, real never-do list"
N_POINTERS = "Every file it points to exists"
N_STALE = "Nothing stale copied from the architecture doc"
N_FILLER = "No filler"
N_RESTATE = "It points to the docs instead of restating them"
N_PYTHONPATH = "It says how the command line finds the package"
N_FIGURES = "No business figures that will go stale"
N_NOTES = "ab-notes.md is filled in"
N_QUOTES = "The notes quote real lines of your memory"

WAITING = "waiting for a memory file"

NEGATION = re.compile(
    r"\b(never|not|no|don'?t|do not|avoid|rejects?|rejected|refus\w*|forbid\w*|ban\w*|instead of|raises?|TypeError|"
    r"without|must not|neither|nor)\b",
    re.I,
)
# Words that say a thing is not there. NEGATION plus the ways people write "this does not exist here".
ABSENCE = re.compile(
    NEGATION.pattern + r"|\b(none|absent|missing|unavailable|unused|isn'?t|aren'?t|doesn'?t|hasn'?t|haven'?t)\b",
    re.I,
)
STALE_ACK = re.compile(
    r"\b(out of date|outdated|stale|lags?|drift\w*|disagree\w*|wrong|no longer|old|obsolete|does not exist|doesn'?t exist|"
    r"not exist|removed|gone|missing)\b",
    re.I,
)

# ---------------------------------------------------------------------------------------------------------
# reading the memory
# ---------------------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Ln:
    """One line of memory text and where it came from."""

    src: str  # file it came from, repo-relative
    no: int  # 1-based line number in that file
    text: str
    kind: str  # "own" | "import" | "rule" | "scoped"


@dataclass
class Memory:
    path: str  # the main file, repo-relative
    lines: list[Ln] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)  # things worth telling the learner (ignored AGENTS.md ...)
    missing_imports: list[str] = field(default_factory=list)

    @property
    def launch(self) -> list[Ln]:
        """What is loaded at the start of every session: the file, its imports and the unscoped rules."""
        return [ln for ln in self.lines if ln.kind != "scoped"]

    @property
    def own(self) -> list[Ln]:
        return [ln for ln in self.lines if ln.kind == "own"]

    @property
    def text(self) -> str:
        return "\n".join(ln.text for ln in self.lines)


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


_IMPORT = re.compile(r"(?<![\w@`/.])@([\w./~-]*[\w/])")
_CODE_SPAN = re.compile(r"`[^`\n]*`")


def _imports_in(text: str) -> list[str]:
    """@path imports in a line of prose: outside code spans, and only things that look like a file path."""
    prose = _CODE_SPAN.sub("", text)
    found = []
    for match in _IMPORT.finditer(prose):
        target = match.group(1)
        if "/" in target or re.search(r"\.\w+$", target):
            found.append(target)
    return found


def fenced(lines: Iterable[Ln]) -> Iterator[tuple[Ln, str | None]]:
    """(line, language) for every line outside a code fence the language is None; fence markers are skipped.

    Inside a fence the language is the text after the opening marker ('' for a bare fence)."""
    lang: str | None = None
    marker = ""
    for ln in lines:
        stripped = ln.text.strip()
        if lang is None:
            match = re.match(r"(```+|~~~+)\s*([\w+-]*)", stripped)
            if match:
                marker, lang = match.group(1)[:3], match.group(2).lower()
                continue
            yield ln, None
        else:
            if stripped.startswith(marker) and set(stripped) <= {marker[0], " "}:
                lang = None
                continue
            yield ln, lang


def prose(lines: Iterable[Ln]) -> list[Ln]:
    return [ln for ln, lang in fenced(lines) if lang is None]


def _expand(work: Path, rel: str, depth: int, seen: set[str], mem: Memory, kind: str) -> None:
    """Append the lines of ``rel`` to ``mem``; follow @imports (relative to the importing file) up to four hops."""
    path = work / rel
    text = _read(path)
    if text is None:
        return
    seen.add(rel)
    lines = text.splitlines()
    for number, line in enumerate(lines, start=1):
        mem.lines.append(Ln(rel, number, line, kind))
    for ln, lang in list(fenced(Ln(rel, i, t, kind) for i, t in enumerate(lines, start=1))):
        if lang is not None:
            continue
        for target in _imports_in(ln.text):
            if target.startswith("~"):
                continue  # a home-directory import is outside the repository; not checked
            resolved = (path.parent / target).resolve()
            try:
                relative = resolved.relative_to(work.resolve()).as_posix()
            except ValueError:
                mem.missing_imports.append(f"{rel}:{ln.no} imports {target}, which is outside the repository")
                continue
            if not resolved.is_file():
                mem.missing_imports.append(f"{rel}:{ln.no} imports {target}, which does not exist")
            elif relative not in seen and depth < MAX_IMPORT_DEPTH:
                _expand(work, relative, depth + 1, seen, mem, "import")


def _strip_frontmatter(text: str) -> tuple[str, str]:
    """(frontmatter, body) of a rule file; frontmatter is '' when there is none."""
    match = re.match(r"---\s*\n(.*?)\n---\s*\n?", text, flags=re.S)
    if not match:
        return "", text
    return match.group(1), text[match.end():]


def load_memory(work: Path) -> Memory | None:
    """The learner's memory as an agent would load it, or None when there is no (non-empty) memory file."""
    work = Path(work)
    primary = next((c for c in MEMORY_CANDIDATES if (_read(work / c) or "").strip()), None)
    if primary is None:
        return None
    mem = Memory(primary)
    seen: set[str] = set()
    _expand(work, primary, 0, seen, mem, "own")
    if primary != "AGENTS.md" and (work / "AGENTS.md").is_file() and "AGENTS.md" not in seen:
        mem.notes.append("AGENTS.md exists but is ignored: Claude Code reads it only when there is no CLAUDE.md "
                         "(put `@AGENTS.md` in CLAUDE.md to share one file)")
    rules = work / RULES_DIR
    if rules.is_dir():
        for path in sorted(rules.rglob("*.md")):
            text = _read(path)
            if text is None:
                continue
            front, body = _strip_frontmatter(text)
            kind = "scoped" if re.search(r"(?m)^paths\s*:", front) else "rule"
            rel = path.relative_to(work).as_posix()
            skipped = len(text.splitlines()) - len(body.splitlines())
            for number, line in enumerate(body.splitlines(), start=skipped + 1):
                mem.lines.append(Ln(rel, number, line, kind))
    return mem


def memory_history(work: Path) -> str:
    """The text of every memory file in the working tree and in every commit since the lab started.

    The notes may quote a line the learner deleted after the experiment (pruning is the point), so quotes are
    looked up in all versions, not just the last."""
    work = Path(work)
    chunks = []
    refs = ["WORKTREE"]
    try:
        refs += [c.sha for c in gitutil.commits_since(work, LAB_START_TAG)]
    except gitutil.GitError:
        pass
    for ref in refs:
        for rel in MEMORY_CANDIDATES:
            text = _read(work / rel) if ref == "WORKTREE" else gitutil.file_at(work, ref, rel)
            if text:
                chunks.append(text)
    rules = work / RULES_DIR
    if rules.is_dir():
        chunks += [t for p in sorted(rules.rglob("*.md")) if (t := _read(p))]
    return "\n".join(chunks)


# ---------------------------------------------------------------------------------------------------------
# small text tools
# ---------------------------------------------------------------------------------------------------------
def normalise(text: str) -> str:
    """Lower case, no markdown decoration, single spaces: for comparing a quote with the file it came from."""
    text = re.sub(r"[`*_>#|]", " ", text)
    text = re.sub(r"^\s*(?:[-+]|\d+[.)])\s+", " ", text, flags=re.M)
    return re.sub(r"\s+", " ", text).strip().lower()


def _where(ln: Ln) -> str:
    return f"line {ln.no}" if ln.kind == "own" else f"{ln.src} line {ln.no}"


def _first(items: Sequence[str], limit: int = 3) -> str:
    return checks._short(list(items), limit)  # noqa: SLF001 - the kit's own formatter, same style as every check


def _fail(name: str, detail: str, hint: str, required: bool = True) -> Check:
    return Check(name, False, detail, hint, required)


def _ok(name: str, detail: str = "", required: bool = True) -> Check:
    return Check(name, True, detail, "", required)


def _inline_spans(ln: Ln) -> list[str]:
    return [m.group(0)[1:-1].strip() for m in _CODE_SPAN.finditer(ln.text)]


_SENTENCE_END = re.compile(r"[.;!?](?=\s)")


def spans_in_context(ln: Ln) -> list[tuple[str, str, str]]:
    """(code span, words before it in its sentence, words after it in its sentence) for every inline span of a line.

    The context lets the lint tell a statement about a file or a tool ("there is no `requirements.txt`", "do not
    use `make`") from a claim ("see `docs/TOUR.md`", "run `pytest -q`")."""
    text = ln.text
    ends = [m for m in _SENTENCE_END.finditer(text)]
    result = []
    for match in _CODE_SPAN.finditer(text):
        low = max([m.end() for m in ends if m.end() <= match.start()], default=0)
        high = min([m.start() for m in ends if m.start() >= match.end()], default=len(text))
        result.append((match.group(0)[1:-1].strip(), text[low:match.start()], text[match.end():high]))
    return result


# ---------------------------------------------------------------------------------------------------------
# size
# ---------------------------------------------------------------------------------------------------------
def size_check(mem: Memory) -> Check:
    launch = [ln for ln in mem.launch if ln.text.strip()]
    n = len(launch)
    extra = ""
    imported = len([ln for ln in launch if ln.kind == "import"])
    if imported:
        extra = f" ({imported} of them pulled in by @-imports: an import does not save context)"
    if n < MIN_LINES:
        return _fail(N_SIZE, f"{n} non-blank lines is too few to hold what an agent needs{extra}",
                     "Aim for roughly 40 to 100 lines: commands, conventions, gotchas, a never list, pointers.")
    if n > MAX_LINES:
        return _fail(N_SIZE, f"{n} non-blank lines loaded at the start of every session{extra}",
                     "The guideline is under 200 lines, and shorter is followed better. Would removing a line cause a mistake?")
    return _ok(N_SIZE, f"{n} non-blank lines{extra}")


# ---------------------------------------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------------------------------------
SHELL_LANGS = {"", "bash", "sh", "shell", "console", "zsh", "shell-session", "terminal", "powershell"}

# Tools that a "typical" Python or JavaScript project has and this repository does not.
MARKER_FILES = {
    "make": ("Makefile", "makefile", "GNUmakefile"),
    "npm": ("package.json",), "npx": ("package.json",), "yarn": ("package.json",), "pnpm": ("package.json",),
    "node": ("package.json",),
    "docker": ("Dockerfile", "docker-compose.yml", "compose.yaml"),
    "docker-compose": ("docker-compose.yml", "compose.yaml"),
    "cargo": ("Cargo.toml",), "go": ("go.mod",), "mvn": ("pom.xml",), "gradle": ("build.gradle",),
    "tox": ("tox.ini",), "nox": ("noxfile.py",), "poetry": ("poetry.lock",), "uv": ("uv.lock",),
    "pre-commit": (".pre-commit-config.yaml",),
}
PYTHON_TOOLS = ("ruff", "black", "flake8", "mypy", "isort", "pylint", "pyright", "bandit", "coverage", "pipenv")
CONFIG_FILES = ("pyproject.toml", "setup.cfg", "tox.ini", ".pre-commit-config.yaml", "README.md", "CONTRIBUTING.md")

ENV_ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
PLACEHOLDER = re.compile(r"<[^>\s]+>|\.\.\.|\$\{?\w|\{\w*\}|\[[^\]]*\]")
SEGMENT_SPLIT = re.compile(r"\s*(?:&&|\|\||;|\|)\s*")

_PYTEST_SHORT = re.compile(r"-(?:[qvxsl]+|r[a-zA-Z]+|h)\Z")
_PYTEST_LONG = re.compile(
    r"--(?:tb=(?:auto|long|short|line|native|no)|maxfail=\d+|durations=\d+|durations-min=[\d.]+|lf|ff|nf|co|collect-only|"
    r"no-header|disable-warnings|strict-markers|strict-config|verbose|quiet|exitfirst|showlocals|last-failed|failed-first|"
    r"new-first|setup-show|fixtures|markers|version|help|color=(?:yes|no|auto)|show-capture=(?:no|stdout|stderr|log|all)|"
    r"capture=(?:no|fd|sys|tee-sys)|import-mode=(?:prepend|append|importlib)|"
    r"(?:ignore|ignore-glob|deselect)=[\w./*:\[\]-]+)\Z"
)
_PYTEST_VALUE_FLAGS = {"-k", "-m", "-W", "-p"}
_PYTEST_PLUGIN_OK = {"no:randomly", "no:cacheprovider"}


@dataclass
class Command:
    kind: str  # "pytest" | "remit" | "absent"
    shown: str  # as the learner wrote it (one segment)
    args: list[str]
    env: dict[str, str]
    tool: str = ""  # for "absent": the tool name
    where: str = ""


@dataclass
class Outcome:
    command: Command
    ran: bool
    ok: bool
    note: str = ""


def tool_is_present(work: Path, tool: str) -> bool:
    """Does this repository use ``tool``? (A marker file for build tools; a mention in the config for the others.)"""
    if tool in MARKER_FILES:
        return any((Path(work) / name).exists() for name in MARKER_FILES[tool])
    texts = [(_read(Path(work) / name) or "") for name in CONFIG_FILES]
    workflows = Path(work) / ".github" / "workflows"
    if workflows.is_dir():
        texts += [(_read(p) or "") for p in workflows.glob("*.y*ml")]
    texts += [(_read(p) or "") for p in Path(work).glob("requirements*.txt")]
    return any(re.search(rf"\b{re.escape(tool)}\b", text) for text in texts)


def _classify(argv: list[str], shown: str, where: str) -> Command | None:
    env: dict[str, str] = {}
    while argv and ENV_ASSIGN.match(argv[0]):
        key, _, value = argv.pop(0).partition("=")
        env[key] = value
    if not argv:
        return None
    program = Path(argv[0]).name
    if program in {"export", "cd", "source", "set", "unset", "alias", "echo", "cat", "ls", "git", "grep", "rg", "find",
                   "head", "tail", "sed", "awk", "diff", "wc", "touch", "mkdir", "cp", "mv", "rm", "curl", "wget",
                   "sudo", "pip", "pip3", "which", "env", "claude"}:
        return None
    if program in {"python", "python3", "py"} or re.fullmatch(r"python3\.\d+", program):
        if len(argv) >= 3 and argv[1] == "-m":
            module, rest = argv[2], argv[3:]
            if module == "pytest":
                return Command("pytest", shown, rest, env, where=where)
            if module == "remit":
                # `python -m remit` on its own is a mention (it needs a sub-command to do anything), not a command
                return Command("remit", shown, rest, env, where=where) if rest else None
            if module in PYTHON_TOOLS or module in MARKER_FILES:
                return Command("absent", shown, rest, env, tool=module, where=where)
        return None
    if program in {"pytest", "py.test"}:
        return Command("pytest", shown, argv[1:], env, where=where)
    if program in PYTHON_TOOLS or program in MARKER_FILES:
        return Command("absent", shown, argv[1:], env, tool=program, where=where)
    return None


def _segments(candidate: str, where: str) -> list[Command]:
    commands = []
    candidate = re.sub(r"^\s*(?:\$|>)\s+", "", candidate)
    candidate = re.sub(r"\s+#.*$", "", candidate)
    for segment in SEGMENT_SPLIT.split(candidate.strip()):
        segment = segment.strip()
        if not segment:
            continue
        try:
            argv = shlex.split(segment)
        except ValueError:
            continue
        cleaned: list[str] = []
        skip = False
        for arg in argv:  # drop shell redirections (>, >>, <, 2>, 2>&1) and the file name after a bare one
            if skip:
                skip = False
            elif arg in {">", ">>", "<", "2>"}:
                skip = True
            elif not arg.startswith((">", "2>", "<")):
                cleaned.append(arg)
        argv = cleaned
        command = _classify(argv, segment, where)
        if command:
            commands.append(command)
    return commands


def extract_commands(mem: Memory) -> list[Command]:
    """Commands the memory documents: lines of shell code blocks and inline code that look like a command."""
    found: list[Command] = []
    pending = ""
    in_never_section = False
    for ln, lang in fenced(mem.lines):
        where = _where(ln)
        if lang is None:
            heading = re.match(r"#{1,6}\s", ln.text.strip())
            if heading:
                in_never_section = bool(NEVER_HEADING.search(ln.text))
            if not in_never_section:
                for span, before, after in spans_in_context(ln):
                    if NEGATION.search(before):  # "do not use `make`" is a warning, not a command
                        continue
                    commands = _segments(span, where)
                    if ABSENCE.search(after):
                        # "`make`, `ruff` and `black` are not used here" talks about the tools; a bare tool name with an
                        # absence word after it is a statement, not a command. With arguments it stays a command:
                        # "`black .` (no network needed)" would still be run, and fail.
                        commands = [c for c in commands if not (c.kind == "absent" and not c.args)]
                    found += commands
            pending = ""
            continue
        if lang not in SHELL_LANGS or in_never_section:
            pending = ""
            continue
        text = ln.text.rstrip()
        if text.endswith("\\"):
            pending += text[:-1] + " "
            continue
        text, pending = pending + text, ""
        if text.strip().startswith("#"):
            continue
        found += _segments(text, where)
    unique: list[Command] = []
    seen: set[tuple[str, ...]] = set()
    for command in found:
        key = (command.kind, command.tool, *command.args, *(f"{k}={v}" for k, v in sorted(command.env.items())))
        if key not in seen:
            seen.add(key)
            unique.append(command)
    return unique


def _pytest_args_problem(args: list[str]) -> str:
    """'' when every option is one the grader knows is safe to pass; otherwise why not."""
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in _PYTEST_VALUE_FLAGS:
            if i + 1 >= len(args):
                return f"{arg} needs a value"
            if arg == "-p" and args[i + 1] not in _PYTEST_PLUGIN_OK:
                return f"the plugin option `-p {args[i + 1]}`"
            i += 2
            continue
        if arg.startswith("-"):
            if not (_PYTEST_SHORT.match(arg) or _PYTEST_LONG.match(arg)):
                return f"the option `{arg}`"
        else:
            target = arg.split("::", 1)[0]
            if target.startswith(("/", "~")) or ".." in Path(target).parts:
                return f"the path `{arg}` (use a path inside the repository)"
        i += 1
    return ""


def run_command(root: Path, command: Command, database: str, timeout: float = 60.0) -> Outcome:
    """Run one documented command in ``root`` (a throw-away copy) and say whether it worked."""
    # The copy is thrown away, so bytecode may be written in it (the kit's default is off): later commands start faster.
    extra = {"REMIT_DB": database, "PYTHONDONTWRITEBYTECODE": ""}
    for key in ("REMIT_LANG", "REMIT_ENV"):
        if command.env.get(key) in {"en", "ar", "dev", "test", "prod"}:
            extra[key] = command.env[key]
    if command.kind == "pytest":
        problem = _pytest_args_problem(command.args)
        if problem:
            return Outcome(command, False, False, f"was not run: the grader does not accept {problem}; use plain forms such as `pytest -q tests/test_fees.py`")
        argv = ["-m", "pytest", *command.args]
    else:
        argv = ["-m", "remit", *command.args]
    result = runner.run_python(argv, cwd=root, pythonpath=[root / "src"], timeout=timeout, extra_env=extra)
    if result.timed_out:
        return Outcome(command, True, False, f"did not finish within {int(timeout)} seconds")
    if result.returncode == 0:
        return Outcome(command, True, True)
    lines = [ln.strip() for ln in (result.stderr + "\n" + result.stdout).splitlines() if ln.strip()]
    tail = next((ln for ln in reversed(lines) if re.search(r"error|not found|usage|no module|failed", ln, re.I)),
                lines[-1] if lines else "no output")
    return Outcome(command, True, False, f"exit status {result.returncode}: {tail[:140]}")


def command_checks(work: Path, mem: Memory) -> list[Check]:
    commands = extract_commands(mem)
    absent = [c for c in commands if c.kind == "absent" and not tool_is_present(work, c.tool)]
    runnable = [c for c in commands if c.kind in {"pytest", "remit"}
                and not any(PLACEHOLDER.search(a) for a in c.args)]
    templates = [c for c in commands if c.kind in {"pytest", "remit"} and any(PLACEHOLDER.search(a) for a in c.args)]
    problems: list[str] = []
    for command in absent:
        problems.append(f"`{command.shown}` ({command.where}): this repository has no {command.tool}")
    outcomes: list[Outcome] = []
    if runnable:
        with checks.work_copy(work) as root, tempfile.TemporaryDirectory(prefix="ailab-m02-db-") as scratch:
            database = str(Path(scratch) / "remit.db")
            for command in runnable[:MAX_COMMANDS_RUN]:
                outcomes.append(run_command(root, command, database))
    failed = [o for o in outcomes if o.ran and not o.ok]
    refused = [o for o in outcomes if not o.ran]
    for outcome in failed + refused:
        problems.append(f"`{outcome.command.shown}` ({outcome.command.where}) {outcome.note}")
    verified_tests = [o for o in outcomes if o.ok and o.command.kind == "pytest"]
    if not verified_tests and not any(o.command.kind == "pytest" for o in outcomes):  # else a failing one is reported above
        if not [c for c in commands if c.kind == "pytest"]:
            problems.append("it does not say how to run the tests")
        else:
            problems.append("its test commands are templates with placeholders; give at least one you can run as written")
    if problems:
        return [_fail(N_COMMANDS, "; ".join(problems[:3]) + (f" (+{len(problems) - 3} more)" if len(problems) > 3 else ""),
                      "The grader runs your commands in a copy of the repository. Run each one from the root and keep only what works.")]
    ran = len([o for o in outcomes if o.ran and o.ok])
    return [_ok(N_COMMANDS, f"{ran} command{'s' if ran != 1 else ''} ran and exited 0")]


def pythonpath_check(mem: Memory) -> Check:
    mentions_cli = re.search(r"python3?\s+-m\s+remit", mem.text)
    explains = re.search(r"PYTHONPATH|pip\s+install\s+-e|python\s+-m\s+pip\s+install\s+-e", mem.text)
    if not mentions_cli or explains:
        return _ok(N_PYTHONPATH, "" if explains else "the memory does not document the command line", required=False)
    return _fail(N_PYTHONPATH, "it documents `python -m remit` but not how Python finds the `remit` package",
                 "The tests find `src` through pyproject.toml; `python -m remit` does not. Follow your own file in a fresh shell.",
                 required=False)


# ---------------------------------------------------------------------------------------------------------
# conventions
# ---------------------------------------------------------------------------------------------------------
ALLOW_FLOAT = re.compile(
    r"\b(use|uses|using|store[sd]?|stored as|prefer(?:red)?|fine|ok|okay|allowed)\b[^\n.]{0,50}\bfloats?\b|"
    r"\bfloats?\b[^\n.]{0,30}\b(?:is|are) (?:fine|ok|okay|allowed|acceptable)\b",
    re.I,
)


def _unnegated(pattern: re.Pattern[str], text: str) -> bool:
    """Does ``pattern`` match somewhere in ``text`` without a negation in or just before the match?"""
    for match in pattern.finditer(text):
        window = text[max(0, match.start() - 40): match.end()]
        if not NEGATION.search(window):
            return True
    return False


def money_check(mem: Memory) -> Check:
    has_decimal = re.search(r"\bDecimal\b", mem.text) is not None
    forbids = any(re.search(r"\bfloats?\b", ln.text, re.I) and NEGATION.search(ln.text) for ln in mem.lines)
    allowing = [ln for ln in prose(mem.lines) if _unnegated(ALLOW_FLOAT, ln.text)]
    if allowing:
        return _fail(N_MONEY, f"{_where(allowing[0])} allows float for money, which CONTRIBUTING.md forbids",
                     "In this repository money is `Decimal`, always, through the `Money` class. A float anywhere is a bug.")
    if not has_decimal or not forbids:
        missing = "mentions neither Decimal nor float" if not has_decimal and not forbids else (
            "never says Decimal" if not has_decimal else "never says that float is forbidden")
        return _fail(N_MONEY, missing,
                     "The rule an agent breaks most easily. Say what money is and what it must never be, in one line.")
    return _ok(N_MONEY)


def layout_check(mem: Memory) -> Check:
    text = mem.text
    has_dir = re.search(r"(?<![\w/])tests/|`tests`|\btests (?:folder|directory|dir)\b", text) is not None
    has_pytest = re.search(r"\bpytest\b", text) is not None
    has_naming = re.search(r"test_(?:<|\*|\w+\.py)|conftest", text) is not None
    foreign = re.compile(r"\b(unittest|nose2?|jest|mocha|vitest|junit)\b", re.I)
    wrong_line = next((ln for ln in prose(mem.lines) if _unnegated(foreign, ln.text)), None)
    if wrong_line:
        return _fail(N_TESTS, f"{_where(wrong_line)} names a test framework this repository does not use",
                     "Look at the first lines of any file in tests/ to see what the repository actually uses.")
    missing = [label for label, ok in (("the tests/ folder", has_dir), ("pytest", has_pytest),
                                       ("how the test files are named or what conftest.py provides", has_naming)) if not ok]
    if missing:
        return _fail(N_TESTS, "it does not mention " + ", ".join(missing),
                     "Say where tests live, how they are named and what tests/conftest.py gives a test.")
    return _ok(N_TESTS)


COMMIT_TYPES = ("feat", "fix", "docs", "test", "refactor", "perf", "chore", "ci", "build", "revert")
_SCOPED_EXAMPLE = re.compile(rf"\b(?:{'|'.join(COMMIT_TYPES)})\([a-z][a-z0-9-]*\)!?:\s+\S")
_UNSCOPED_EXAMPLE = re.compile(rf"(?:^|[`\s\"'(])(?:{'|'.join(COMMIT_TYPES)}):\s+\S")
_FOREIGN_TYPES = re.compile(r"\b(style|wip|hotfix|misc|bugfix|feature|improvement|deps|release)\b", re.I)


def commit_check(mem: Memory) -> Check:
    text = mem.text
    for ln in prose(mem.lines):
        # "the scope is required, not optional" says the opposite of "the scope is optional": skip a negated match
        optional = [m for m in re.finditer(r"scope[^.\n]{0,30}optional|optional[^.\n]{0,15}scope", ln.text, re.I)
                    if not NEGATION.search(m.group(0))]
        if optional or re.search(r"scope[^.\n]{0,20}\b(?:not required|can be omitted|may be omitted|is omitted)\b", ln.text, re.I):
            return _fail(N_COMMITS, f"{_where(ln)} says the scope is optional", "Read the commit section of CONTRIBUTING.md again.")
        spans = _inline_spans(ln) or [ln.text]
        if any(_UNSCOPED_EXAMPLE.search(span) and not _SCOPED_EXAMPLE.search(span) for span in spans) and \
                re.search(r"\b(commit|message|example|e\.g\.)\b", ln.text, re.I):
            return _fail(N_COMMITS, f"{_where(ln)} shows a commit without a scope", "This repository requires a scope: `type(scope): subject`.")
        types_here = sum(1 for t in COMMIT_TYPES if re.search(rf"\b{t}\b", ln.text))
        if types_here >= 3:
            # "there is no `style` type" names a type the repository does not allow in order to say so: skip a negated mention
            foreign = next((f for f in _FOREIGN_TYPES.finditer(ln.text)
                            if not NEGATION.search(ln.text[max(0, f.start() - 60): f.start()])), None)
            if foreign:
                return _fail(N_COMMITS, f"{_where(ln)} lists a commit type (`{foreign.group(0).lower()}`) that CONTRIBUTING.md does not allow",
                             "Copy the types from CONTRIBUTING.md.")
    if not (re.search(r"type\(scope\)\s*:\s*subject", text) or _SCOPED_EXAMPLE.search(text)):
        return _fail(N_COMMITS, "it does not give the commit format with a scope",
                     "CONTRIBUTING.md defines the header. Write the format and one example.")
    return _ok(N_COMMITS)


def najmkit_names(work: Path) -> dict[str, set[str]]:
    """The public names of najmkit's modules, read from the source (nothing is imported)."""
    names: dict[str, set[str]] = {}
    for module in ("ids", "clock", "audit"):
        found: set[str] = set()
        source = _read(Path(work) / "src" / "najmkit" / f"{module}.py")
        if source:
            try:
                tree = ast.parse(source)
            except SyntaxError:
                tree = ast.Module(body=[], type_ignores=[])
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    found.add(node.name)
                elif isinstance(node, ast.Assign):
                    found |= {t.id for t in node.targets if isinstance(t, ast.Name)}
                elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                    found.add(node.target.id)
        names[module] = found
    return names


_FILE_EXTENSIONS = {"py", "md", "jsonl", "json", "log", "db", "toml", "yml", "yaml", "txt", "cfg", "ini", "sqlite3"}
_NAJMKIT_REF = re.compile(r"(?<![\w.])(?:najmkit\.)?(ids|clock|audit)\.([A-Za-z_]\w*)")


def najmkit_check(work: Path, mem: Memory) -> Check:
    text = mem.text
    if not re.search(r"najmkit", text, re.I):
        return _fail(N_NAJMKIT, "najmkit is not mentioned",
                     "It is Najm's own library, in no model's training data. What will tell the agent what exists?")
    if "docs/najmkit.md" not in text:
        return _fail(N_NAJMKIT, "it mentions najmkit but does not point to the file that documents it",
                     "Point to the file that documents it instead of copying its API into the memory.")
    real = najmkit_names(work)
    invented = []
    for match in _NAJMKIT_REF.finditer(text):
        module, attr = match.group(1), match.group(2)
        if attr in _FILE_EXTENSIONS or not real.get(module):
            continue
        if attr not in real[module]:
            invented.append(f"{module}.{attr}")
    if invented:
        return _fail(N_NAJMKIT, f"it names {_first(sorted(set(invented)))}, which najmkit does not have",
                     "Check each name against docs/najmkit.md. Agents invent plausible names; do not add to them.")
    return _ok(N_NAJMKIT)


# ---------------------------------------------------------------------------------------------------------
# the never-do list
# ---------------------------------------------------------------------------------------------------------
PROHIBITION = re.compile(r"(?:never|do not|don'?t|must not|should not|shouldn'?t|mustn'?t|avoid)\b", re.I)
NEVER_HEADING = re.compile(r"\b(never|do not|don'?t|must not|off.?limits|forbidden)\b", re.I)
TOPICS = {
    "money": re.compile(r"\bfloats?\b|\bDecimal\b|\bmoney\b", re.I),
    "secrets": re.compile(r"secret|token|credential|password|api key|\.env\b|customer data|personal data", re.I),
    "dependencies": re.compile(r"dependenc|pip install|standard library|new package", re.I),
    "tests": re.compile(r"\btests?\b", re.I),
    "determinism": re.compile(r"uuid|datetime\.now|time\.time|\brandom\b|najmkit|real clock", re.I),
    "legacy": re.compile(r"ledger|screening|legacy", re.I),
    "git": re.compile(r"\bcommit|\bpush\b|force|amend|\bmain\b|pull request", re.I),
}
TEST_TAMPERING = re.compile(r"\b(edit|delete|skip|weaken|disable|change|modify|remove|rewrite|loosen)\w*\b", re.I)
MIN_NEVER, MAX_NEVER = 2, 12


_MARKER = re.compile(r"^(?:important|note|warning|critical|rule)\s*[:\-–—]\s*", re.I)
# "Money must not be a float", "Secrets must not appear in logs", "Money is never a float": a short subject, then the modal
_MODAL_PROHIBITION = re.compile(r"^[^.;!]{1,40}?\b(?:must not|should not|mustn'?t|shouldn'?t|is never|are never|can never)\b", re.I)


def _rules_in(line: str) -> list[str]:
    """The sentences of a line that are prohibitions ('Never x. Do not y.' is two rules).

    A prohibition starts with a prohibiting word ('Never ...', 'Do not ...'), after an optional marker such as
    'IMPORTANT:', or is a short subject followed by 'must not' / 'is never'."""
    body = re.sub(r"^(?:[-*+]|\d+[.)])?\s*", "", line.strip())
    sentences = re.split(r"(?<=[.;!])\s+", body)
    rules = []
    for sentence in sentences:
        text = _MARKER.sub("", re.sub(r"^[*_\s]+", "", sentence))
        if PROHIBITION.match(text) or _MODAL_PROHIBITION.match(text):
            rules.append(sentence)
    return rules


def never_check(mem: Memory) -> Check:
    items: list[Ln] = []
    heading_is_never = False
    for ln in prose(mem.lines):
        stripped = ln.text.strip()
        if re.match(r"#{1,6}\s", stripped):
            heading_is_never = bool(NEVER_HEADING.search(stripped))
            continue
        is_bullet = bool(re.match(r"(?:[-*+]|\d+[.)])\s+\S", stripped))
        rules = _rules_in(stripped)
        if rules:
            items += [ln] * len(rules)
        elif heading_is_never and is_bullet:
            items.append(ln)
    count = len(items)
    if count < MIN_NEVER:
        return _fail(N_NEVER, f"{count} never-do line{'s' if count != 1 else ''} found; at least {MIN_NEVER} are needed",
                     "Name the two or three things an agent must never do here, as one-line rules.")
    if count > MAX_NEVER:
        return _fail(N_NEVER, f"{count} rules in the never-do list; a list this long stops being read",
                     "Keep the rules whose breach would hurt. Move the rest into tests, hooks or deny rules.")
    covered = {
        topic for topic, pattern in TOPICS.items()
        if any(pattern.search(ln.text) and (topic != "tests" or TEST_TAMPERING.search(ln.text)) for ln in items)
    }
    if len(covered) < 2:
        return _fail(N_NEVER, "the never-do list does not name anything specific to this repository",
                     "Generic rules change nothing. Name what is true here: the money type, tests, secrets, dependencies, the clock, the legacy modules.")
    return _ok(N_NEVER, f"{count} rules")


# ---------------------------------------------------------------------------------------------------------
# pointers
# ---------------------------------------------------------------------------------------------------------
_PATH_EXT = r"(?:py|md|toml|ya?ml|json|jsonl|txt|cfg|ini|sqlite3?|db|log|example|lock)"
_FILENAME_IN_TEXT = re.compile(rf"(?<![\w/.:-])(?:[\w.-]+/)*[\w.-]*\w\.{_PATH_EXT}\b")
SAFE_UNCREATED = {"CLAUDE.local.md"}


def _gitignored(work: Path) -> list[str]:
    patterns = []
    for line in (_read(Path(work) / ".gitignore") or "").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line.rstrip("/"))
    return patterns


def _looks_like_path(token: str) -> bool:
    if not token or re.search(r"\s", token) or token.startswith(("http://", "https://", "-", "$", "~")):
        return False
    if re.search(r"[(){}=|<>,;\"']", token):
        return False
    base = token.rstrip("/")
    if "/" in base or (token.endswith("/") and len(base) > 1):
        return True
    if base.startswith("."):
        return len(base) > 2
    return re.search(rf"\.{_PATH_EXT}\Z", base) is not None


def _clean_token(token: str) -> str:
    token = token.strip().strip("`").lstrip("@")
    token = re.sub(r"::[\w\[\]\-.]*\Z", "", token)  # pytest node ids
    token = re.sub(r":\d+(?::\d+)?\Z", "", token)  # file:line
    token = token.split("#", 1)[0]
    token = token.rstrip(".,;:)")
    return token[2:] if token.startswith("./") else token


def _is_path_claim(work: Path, token: str) -> bool:
    """`origin/main` and `yes/no` are not claims about files; `src/remit/risk.py` and `docs/` are.

    A token with a slash counts when it has a file extension, ends in a slash, or starts at something that exists."""
    if "/" not in token.rstrip("/") or token.endswith("/") or re.search(rf"\.{_PATH_EXT}\Z", token):
        return True
    return (Path(work) / token.split("/", 1)[0]).exists()


def path_references(work: Path, mem: Memory) -> list[tuple[Ln, str]]:
    """Everything in the memory that claims to be a file or folder in the repository."""
    refs: list[tuple[Ln, str]] = []
    for ln, lang in fenced(mem.lines):
        if lang is None:
            candidates = [span for span, before, after in spans_in_context(ln)
                          if not (NEGATION.search(before) or NEGATION.search(after))]  # "there is no `requirements.txt`"
            candidates += [m.group(1) for m in re.finditer(r"\]\(([^)\s]+)\)", ln.text)]
            candidates += _imports_in(ln.text)
            if _TREE_GLYPHS.search(ln.text):  # a directory tree drawn without a code fence
                candidates += [m.group(0) for m in _FILENAME_IN_TEXT.finditer(ln.text)]
        elif lang in {"", "text", "txt", "markdown", "md"}:
            candidates = [m.group(0) for m in _FILENAME_IN_TEXT.finditer(ln.text)]
        else:
            continue
        for raw in candidates:
            # a span such as `pytest -q tests/test_fees.py` holds a path; look at each word of a short command
            words = [raw] if _looks_like_path(_clean_token(raw)) else raw.split() if len(raw.split()) <= 8 else []
            for word in words:
                token = _clean_token(word)
                if _looks_like_path(token) and _is_path_claim(work, token):
                    refs.append((ln, token))
    return refs


def _exists(work: Path, token: str, ignored: list[str]) -> bool:
    work = Path(work)
    if token in SAFE_UNCREATED:
        return True
    if any(ch in token for ch in "*?["):
        return bool(list(work.glob(token)))
    base = token.rstrip("/")
    if "/" in base or base.startswith("."):
        if (work / base).exists():
            return True
    else:
        if (work / base).exists() or any(p for p in work.rglob(base) if ".git" not in p.parts and "__pycache__" not in p.parts):
            return True
    name = Path(base).name
    return any(fnmatch.fnmatch(name, pat) or fnmatch.fnmatch(base, pat) for pat in ignored)


def pointer_check(work: Path, mem: Memory) -> Check:
    refs = path_references(work, mem)
    ignored = _gitignored(work)
    missing: list[str] = []
    good: set[str] = set()
    for ln, token in refs:
        if _exists(work, token, ignored):
            if not any(ch in token for ch in "*?[") and not any(fnmatch.fnmatch(Path(token.rstrip('/')).name, p) for p in ignored):
                good.add(token.rstrip("/"))
        else:
            missing.append(f"`{token}` ({_where(ln)})")
    missing += [m for m in mem.missing_imports]
    if missing:
        unique = list(dict.fromkeys(missing))
        return _fail(N_POINTERS, f"{_first(unique, 3)} does not exist" if len(unique) == 1 else f"not in the repository: {_first(unique, 3)}",
                     "Check each path with ls. Documents drift; when a doc and the code disagree, the code wins.")
    if len(good) < MIN_POINTERS:
        return _fail(N_POINTERS, f"it points to {len(good)} real file{'s' if len(good) != 1 else ''}; at least {MIN_POINTERS} are expected",
                     "Point to the docs to read first, the files that matter and the tests, with their paths.")
    return _ok(N_POINTERS, f"{len(good)} pointers resolve")


# ---------------------------------------------------------------------------------------------------------
# stale facts, filler, restating
# ---------------------------------------------------------------------------------------------------------
STALE_FACTS = (
    ("a module that no longer exists", re.compile(r"\brisk\.(?:py|check)\b", re.I)),
    ("an old limits rule (no monthly limit)", re.compile(r"\bno monthly limits?\b", re.I)),
    ("an old limits rule (two KYC tiers)", re.compile(r"\btwo (?:KYC )?tiers\b", re.I)),
    ("an old per-day limit for T1", re.compile(r"\bT1\b[^\n]{0,60}\b5,?000\b")),
    ("an old per-day limit for T2", re.compile(r"\bT2\b[^\n]{0,60}\b25,?000\b")),
)


def stale_check(mem: Memory) -> Check:
    hits = []
    for ln in mem.lines:
        if STALE_ACK.search(ln.text):
            continue  # a line that says the doc is out of date is not repeating the stale claim
        for label, pattern in STALE_FACTS:
            if pattern.search(ln.text):
                hits.append(f"{_where(ln)}: {label}")
    if hits:
        return _fail(N_STALE, _first(hits, 2),
                     "docs/ARCHITECTURE.md is partly out of date. Check each claim against src/, or point to the file instead.")
    return _ok(N_STALE)


FILLER = (
    ("clean, readable or maintainable code",
     re.compile(r"\b(clean|readable|maintainable|idiomatic|elegant|high[- ]quality|production[- ]ready|robust)\b[\w, -]{0,25}\b(code|python|solutions?|software)\b", re.I)),
    ("best practices", re.compile(r"\bbest[- ]practices?\b", re.I)),
    ("be careful", re.compile(r"\b(?:be|being) (?:very |extra )?(?:careful|thorough|diligent)\b", re.I)),
    ("a role-play opening", re.compile(r"\byou are (?:a|an|the)\b[^.\n]{0,40}\b(?:expert|engineer|developer|assistant|senior)\b|\bact as\b", re.I)),
    ("think step by step", re.compile(r"\bthink step[- ]by[- ]step\b", re.I)),
    ("PEP 8", re.compile(r"\bPEP[- ]?8\b")),
    ("design slogans (SOLID, DRY, KISS)", re.compile(r"\b(?:SOLID|DRY|KISS|YAGNI)\b")),
    ("good names", re.compile(r"\b(?:descriptive|meaningful|clear|good) (?:variable |function )?names\b", re.I)),
    ("well-documented, well-tested, scalable", re.compile(r"\b(?:well[- ]documented|well[- ]structured|well[- ]tested|scalable)\b", re.I)),
    ("type hints and docstrings", re.compile(r"\b(?:type hints?|type annotations?)\b|\b(?:add|write|include|use|needs?)\s+(?:\w+\s+){0,3}docstrings?\b", re.I)),
)


def filler_check(mem: Memory) -> Check:
    hits: dict[str, Ln] = {}
    for ln in mem.lines:
        for label, pattern in FILLER:
            if label not in hits and pattern.search(ln.text):
                hits[label] = ln
    if hits:
        shown = [f"'{label}' ({_where(ln)})" for label, ln in hits.items()]
        return _fail(N_FILLER, "filler found: " + _first(shown, 3),
                     "Delete it. Would removing the line cause a mistake? Generic advice only dilutes the lines that matter.")
    return _ok(N_FILLER)


_TREE_GLYPHS = re.compile(r"[├└│]──|^\s*[│├└]")
_FILE_BULLET = re.compile(r"^\s*(?:[-*+]\s+|\|\s*)?`?[\w./-]+\.(?:py|md|toml|ya?ml)`?\s*(?::|—|–|-|\|)\s*\S")


DOC_FILES = ("README.md", "CONTRIBUTING.md")


def authored(mem: Memory) -> list[Ln]:
    """The lines the learner wrote: the memory file, other memory files it imports and the rules; not the repository's docs."""
    return [ln for ln in mem.lines if ln.kind != "import" or not (ln.src in DOC_FILES or ln.src.startswith("docs/"))]


def _doc_corpus(work: Path) -> str:
    parts = []
    for name in ("README.md", "CONTRIBUTING.md"):
        parts.append(_read(Path(work) / name) or "")
    docs = Path(work) / "docs"
    if docs.is_dir():
        parts += [(_read(p) or "") for p in sorted(docs.glob("*.md"))]
    return normalise("\n".join(parts))


def restate_check(work: Path, mem: Memory) -> Check:
    own = authored(mem)
    tree = next((ln for ln in own if _TREE_GLYPHS.search(ln.text)), None)
    if tree:
        return _fail(N_RESTATE, f"{_where(tree)} draws the directory tree; the agent can list directories itself",
                     "Delete the tree; the agent can list directories. Name only the files that are not obvious.")
    inventory = [ln for ln in prose(own) if _FILE_BULLET.match(ln.text)]
    if len(inventory) > 10:
        return _fail(N_RESTATE, f"{len(inventory)} lines describe one file each (from {_where(inventory[0])}); that is the README's job",
                     "Describe only files whose purpose is not obvious; point to docs/TOUR.md for the rest.")
    corpus = _doc_corpus(work)
    candidates = [normalise(ln.text) for ln in prose(own)]
    candidates = [c for c in candidates if len(c) >= 45]
    copied = [c for c in candidates if c in corpus]
    if len(copied) >= 5 and len(copied) / max(1, len(candidates)) >= 0.4:
        return _fail(N_RESTATE, f"{len(copied)} of {len(candidates)} longer lines are copied word for word from README.md, CONTRIBUTING.md or docs/",
                     "Point to the doc; keep only what it does not say.")
    return _ok(N_RESTATE)


FIGURE = re.compile(r"\b(?:QAR|INR|PHP|EGP|PKR|BDT)\s?\d[\d,]*(?:\.\d+)?|\b\d[\d,]*(?:\.\d+)?\s?(?:QAR|INR|PHP|EGP|PKR|BDT)\b|\b\d+(?:\.\d+)?\s?%")


def figures_check(mem: Memory) -> Check:
    hits = [ln for ln in prose(authored(mem)) if FIGURE.search(_CODE_SPAN.sub("", ln.text))]
    if hits:
        return _fail(N_FIGURES, f"{_where(hits[0])} states a limit, fee or rate" + (f" (and {len(hits) - 1} more lines)" if len(hits) > 1 else ""),
                     "Business numbers live in limits.py, fees.py and fx.py and change. Point to the file.", required=False)
    return _ok(N_FIGURES, required=False)


def memory_checks(work: Path) -> list[Check]:
    """Every check on the memory file itself (the notes and git hygiene are added by the lab)."""
    work = Path(work)
    mem = load_memory(work)
    names = [N_SIZE, N_COMMANDS, N_PYTHONPATH, N_MONEY, N_TESTS, N_COMMITS, N_NAJMKIT, N_NEVER, N_POINTERS,
             N_STALE, N_FILLER, N_RESTATE, N_FIGURES]
    optional = {N_PYTHONPATH, N_FIGURES}
    if mem is None:
        exists = _fail(N_EXISTS, "none of CLAUDE.md, .claude/CLAUDE.md or AGENTS.md exists (or it is empty)",
                       "Create CLAUDE.md at the root of the repository (or AGENTS.md if your tool reads that).")
        return [exists] + [Check(n, False, WAITING, "", n not in optional) for n in names]
    results: dict[str, Check] = {}

    def safe(name: str, fn) -> None:  # one bug in one rule must not hide all the others
        try:
            produced = fn()
        except Exception as exc:  # pragma: no cover - a defensive net, covered by the tests of the lint itself
            produced = [_fail(name, f"internal error in this check: {type(exc).__name__}: {exc}", "This is a bug in the lab, not in your file.")]
        for check in produced if isinstance(produced, list) else [produced]:
            results[check.name] = check

    safe(N_SIZE, lambda: size_check(mem))
    safe(N_COMMANDS, lambda: command_checks(work, mem))
    safe(N_PYTHONPATH, lambda: pythonpath_check(mem))
    safe(N_MONEY, lambda: money_check(mem))
    safe(N_TESTS, lambda: layout_check(mem))
    safe(N_COMMITS, lambda: commit_check(mem))
    safe(N_NAJMKIT, lambda: najmkit_check(work, mem))
    safe(N_NEVER, lambda: never_check(mem))
    safe(N_POINTERS, lambda: pointer_check(work, mem))
    safe(N_STALE, lambda: stale_check(mem))
    safe(N_FILLER, lambda: filler_check(mem))
    safe(N_RESTATE, lambda: restate_check(work, mem))
    safe(N_FIGURES, lambda: figures_check(mem))
    detail = mem.path + (f" ({'; '.join(mem.notes)})" if mem.notes else "")
    return [_ok(N_EXISTS, detail)] + [results[n] for n in names if n in results]


# ---------------------------------------------------------------------------------------------------------
# the A/B notes
# ---------------------------------------------------------------------------------------------------------
NOTES_SECTIONS = (
    ("setup", 12),
    ("what was different", 25),
    ("the memory line that mattered", 4),
    ("a memory line that changed nothing", 4),
    ("what i changed in the memory afterwards", 8),
    ("limits of this comparison", 12),
)
TABLE_ROWS = (
    ("minutes", "Minutes until I accepted the result", "int"),
    ("wrong turns", "Wrong turns I had to correct", "int"),
    ("files changed", "Files changed", "int"),
    ("lines changed", "Lines changed", "int"),
    ("pytest", "`pytest -q` passes at the end", "yesno"),
    ("commit message", "Commit message follows CONTRIBUTING.md", "yesno"),
)
_INT_CELL = re.compile(r"\s*(\d+)\s*(?:min(?:ute)?s?)?\s*\Z", re.I)
_YESNO_CELL = re.compile(r"\s*(yes|no)\b", re.I)


def _table_cells(body: str) -> list[list[str]]:
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("|") and not re.fullmatch(r"\|[\s:|-]+\|?", line):
            rows.append([c.strip() for c in line.strip("|").split("|")])
    return rows


def _quotes(body: str) -> list[str]:
    """Quoted lines in a section: block quotes, code spans and double-quoted text."""
    found = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith(">"):
            found.append(stripped.lstrip("> ").strip())
    found += [m.group(1) for m in re.finditer(r"`([^`\n]+)`", body)]
    found += [m.group(1) for m in re.finditer(r"[\"“]([^\"”\n]{12,})[\"”]", body)]
    return [q for q in found if q]


def notes_checks(work: Path) -> list[Check]:
    work = Path(work)
    path = work / NOTES_FILE
    if not path.is_file():
        return [_fail(N_NOTES, f"{NOTES_FILE} is missing", "Restore the notes template from the starting commit and fill it in."),
                _fail(N_QUOTES, WAITING, "")]
    text = path.read_text(encoding="utf-8", errors="replace")
    problems: list[str] = []
    if "TODO" in text:
        left = text.count("TODO")
        problems.append(f"{left} TODO placeholder{'s' if left != 1 else ''} left")
    sections = checks.markdown_sections(path)

    def section(title: str) -> str | None:
        key = next((k for k in sections if title in k), None)
        return sections.get(key) if key else None

    for title, min_words in NOTES_SECTIONS:
        body = section(title)
        if body is None:
            problems.append(f"no section '{title}'")
        elif "TODO" not in body and len(body.split()) < min_words:
            problems.append(f"'{title}' is too short ({len(body.split())} words; at least {min_words})")
    results = section("results")
    if results is None:
        problems.append("no section 'results'")
    else:
        rows = {cells[0].lower(): cells for cells in _table_cells(results) if len(cells) >= 3}
        for key, label, kind in TABLE_ROWS:
            cells = next((c for name, c in rows.items() if key in name), None)
            if cells is None:
                problems.append(f"the results table has no row for '{label}'")
                continue
            for column, cell in zip(("A", "B"), cells[1:3]):
                if "TODO" in cell or not cell:
                    continue  # already reported as a TODO / reported below as empty
                pattern = _INT_CELL if kind == "int" else _YESNO_CELL
                if not pattern.match(cell):
                    expected = "a whole number" if kind == "int" else "yes or no"
                    problems.append(f"'{label}', column {column}, should be {expected}")
            if any(not c for c in cells[1:3]):
                problems.append(f"'{label}' has an empty cell")
    notes = _fail(N_NOTES, _first(problems, 3) + (f" (+{len(problems) - 3} more)" if len(problems) > 3 else ""),
                  "Fill every section. Report what happened, including 'no difference'. The grader checks completeness, not that the memory won.") if problems else _ok(N_NOTES)
    # quotes
    history = normalise(memory_history(work))
    quote_problems = []
    if not history:
        return [notes, _fail(N_QUOTES, WAITING, "")]
    for title in ("the memory line that mattered", "a memory line that changed nothing"):
        body = section(title)
        if body is None or "TODO" in body:
            quote_problems.append(f"'{title}' is not filled in")
            continue
        quotes = [q for q in _quotes(body) if len(normalise(q)) >= 15]
        if not quotes:
            quote_problems.append(f"'{title}' has no quoted line (put the line itself in a block quote or backticks)")
        elif not any(normalise(q) in history for q in quotes):
            quote_problems.append(f"'{title}' quotes something that is not in your memory file")
    quotes_check = _fail(N_QUOTES, _first(quote_problems, 2),
                         "Copy the line exactly from your memory file into a block quote. A paraphrase cannot be checked.") if quote_problems else _ok(N_QUOTES)
    return [notes, quotes_check]
