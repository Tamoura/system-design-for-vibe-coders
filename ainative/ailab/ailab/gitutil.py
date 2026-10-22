"""Small git helpers for starting labs, seeding them and grading them.

Everything works on a *work directory* (a git repository created by ``ailab start``).
The tag ``lab-start`` marks the state the learner started from; "changed since the
start" always means "compared with that tag", including uncommitted and untracked files.

Commits made by the kit itself use a fixed author and date, so a started lab is the
same every time. Commits made by the learner are the learner's own.
"""
from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from ailab import runner

TAG_START = "lab-start"
KIT_AUTHOR = ("Najm Payments Platform", "payments-platform@najm.example")
KIT_DATE = "2026-03-02T08:00:00+00:00"

# Files that editors and agent tools create on their own. They are not the learner's work,
# so the "what changed" helpers skip them by default (pass ignore=() to see everything).
TOOL_NOISE: tuple[str, ...] = (
    ".claude/settings.local.json",
    ".claude/worktrees/**",
    ".aider*",
    ".DS_Store",
    ".idea/**",
    ".vscode/**",
    "**/__pycache__/**",
    "**/*.pyc",
    ".pytest_cache/**",
)


class GitError(RuntimeError):
    """A git command that was expected to succeed did not."""


@dataclass
class Commit:
    sha: str
    subject: str
    body: str
    author_name: str
    author_email: str
    date: str
    parents: list[str] = field(default_factory=list)

    @property
    def message(self) -> str:
        return self.subject + ("\n\n" + self.body if self.body else "")

    @property
    def is_merge(self) -> bool:
        return len(self.parents) > 1


@dataclass
class DiffStat:
    files: list[str]
    added: int
    deleted: int

    @property
    def total(self) -> int:
        """Lines added plus lines deleted."""
        return self.added + self.deleted

    @property
    def n_files(self) -> int:
        return len(self.files)


# -- running git ------------------------------------------------------------
def _env(extra: dict[str, str] | None = None) -> dict[str, str]:
    env = runner.clean_env()
    env.update(GIT_TERMINAL_PROMPT="0", GIT_CONFIG_NOSYSTEM="1", LC_ALL="C.UTF-8")
    if extra:
        env.update(extra)
    return env


def _author_env(author: tuple[str, str] | None, date: str | None) -> dict[str, str]:
    name, email = author or KIT_AUTHOR
    when = date or KIT_DATE
    return {
        "GIT_AUTHOR_NAME": name,
        "GIT_AUTHOR_EMAIL": email,
        "GIT_COMMITTER_NAME": name,
        "GIT_COMMITTER_EMAIL": email,
        "GIT_AUTHOR_DATE": when,
        "GIT_COMMITTER_DATE": when,
    }


def git(
    work: Path | str,
    *args: str,
    check: bool = True,
    env: dict[str, str] | None = None,
    input: str | None = None,
    timeout: float = 60.0,
) -> runner.RunResult:
    """Run ``git <args>`` in ``work``. Raises GitError on failure when ``check`` is true."""
    result = runner.run(["git", *args], cwd=work, env=_env(env), input=input, timeout=timeout)
    if check and not result.ok:
        raise GitError(f"git {' '.join(args)} failed ({result.returncode}): {result.output.strip()}")
    return result


def out(work: Path | str, *args: str, check: bool = True) -> str:
    """stdout of a git command, stripped."""
    return git(work, *args, check=check).stdout.strip()


# -- repository setup ---------------------------------------------------------
def init_repo(work: Path | str, branch: str = "main") -> None:
    """``git init`` with ``branch`` as the initial branch (works on old git versions too)."""
    git(work, "init", "-q")
    git(work, "symbolic-ref", "HEAD", f"refs/heads/{branch}")


def ensure_identity(work: Path | str) -> bool:
    """Make sure the learner can commit: set a local identity only if git has none. Returns True if set."""
    have_name = bool(out(work, "config", "--get", "user.name", check=False))
    have_email = bool(out(work, "config", "--get", "user.email", check=False))
    if have_name and have_email:
        return False
    if not have_name:
        git(work, "config", "user.name", "Najm Learner")
    if not have_email:
        git(work, "config", "user.email", "learner@najm.example")
    return True


def set_config(work: Path | str, key: str, value: str) -> None:
    git(work, "config", "--local", key, value)


def get_config(work: Path | str, key: str) -> str | None:
    value = out(work, "config", "--local", "--get", key, check=False)
    return value or None


def add_local_excludes(work: Path | str, patterns: Iterable[str]) -> None:
    """Append patterns to ``.git/info/exclude`` (a git-ignore that is not part of the repo)."""
    path = Path(work) / ".git" / "info" / "exclude"
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    with path.open("a", encoding="utf-8") as handle:
        for pattern in patterns:
            if pattern not in existing.splitlines():
                handle.write(pattern + "\n")


# -- committing and tagging -----------------------------------------------------
def commit_all(
    work: Path | str,
    message: str,
    *,
    allow_empty: bool = False,
    force: Sequence[str] = (),
    author: tuple[str, str] | None = None,
    date: str | None = None,
) -> str:
    """Stage everything and commit; return the new commit's sha.

    ``force`` lists paths to stage even if .gitignore matches them (``git add -f``).
    The commit uses the kit's fixed author and date unless ``author`` / ``date`` are given
    (a lab seed that wants to imitate a colleague's or an agent's commit passes its own).
    With nothing to commit and ``allow_empty`` false, raises GitError.
    """
    git(work, "add", "-A")
    for path in force:
        if (Path(work) / path).exists():
            git(work, "add", "-f", "--", path)
    args = ["-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", message]
    if allow_empty:
        args.append("--allow-empty")
    git(work, *args, env=_author_env(author, date))
    return head(work)


def tag(work: Path | str, name: str, ref: str = "HEAD", *, force: bool = False) -> None:
    args = ["tag"] + (["-f"] if force else []) + [name, ref]
    git(work, *args)


def head(work: Path | str) -> str:
    return out(work, "rev-parse", "HEAD")


def rev_parse(work: Path | str, ref: str) -> str | None:
    result = git(work, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}", check=False)
    if not result.ok:
        return None
    return result.stdout.strip() or None


def has_ref(work: Path | str, ref: str) -> bool:
    return rev_parse(work, ref) is not None


def current_branch(work: Path | str) -> str:
    return out(work, "rev-parse", "--abbrev-ref", "HEAD")


def branches(work: Path | str) -> list[str]:
    text = out(work, "for-each-ref", "--format=%(refname:short)", "refs/heads")
    return text.splitlines()


def create_branch(work: Path | str, name: str, *, checkout: bool = True, start: str = "HEAD") -> None:
    if checkout:
        git(work, "checkout", "-q", "-b", name, start)
    else:
        git(work, "branch", name, start)


def checkout(work: Path | str, ref: str) -> None:
    git(work, "checkout", "-q", ref)


def merge(work: Path | str, branch: str, *, message: str | None = None, no_ff: bool = False,
          author: tuple[str, str] | None = None, date: str | None = None, check: bool = True) -> runner.RunResult:
    """``git merge`` with the kit's author (so it works without a configured identity)."""
    args = ["-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "merge", "-q"]
    if no_ff:
        args.append("--no-ff")
    args += ["-m", message or f"Merge {branch}"]
    args.append(branch)
    return git(work, *args, check=check, env=_author_env(author, date))


def apply_patch(work: Path | str, patch: str | Path) -> None:
    """Apply a unified diff (text, or a path to a .patch file) to the working tree."""
    text = Path(patch).read_text(encoding="utf-8") if isinstance(patch, Path) else patch
    git(work, "apply", "--whitespace=nowarn", "-", input=text)


# -- inspecting the work ----------------------------------------------------------
def glob_match(path: str, patterns: Iterable[str]) -> bool:
    """Match a repo-relative posix path against glob patterns; ``**`` spans directories."""
    return any(_glob_regex(p).match(path) for p in patterns)


_GLOB_CACHE: dict[str, re.Pattern[str]] = {}


def _glob_regex(pattern: str) -> re.Pattern[str]:
    if pattern not in _GLOB_CACHE:
        i, parts = 0, []
        while i < len(pattern):
            c = pattern[i]
            if pattern.startswith("**/", i):
                parts.append("(?:.*/)?")
                i += 3
                continue
            if pattern.startswith("**", i):
                parts.append(".*")
                i += 2
                continue
            parts.append("[^/]*" if c == "*" else "[^/]" if c == "?" else re.escape(c))
            i += 1
        _GLOB_CACHE[pattern] = re.compile("".join(parts) + r"\Z")
    return _GLOB_CACHE[pattern]


def _untracked(work: Path | str) -> list[str]:
    text = git(work, "ls-files", "--others", "--exclude-standard", "-z").stdout
    return [p for p in text.split("\0") if p]


def changed_status(
    work: Path | str,
    since: str = TAG_START,
    *,
    include_untracked: bool = True,
    ignore: Sequence[str] = TOOL_NOISE,
) -> dict[str, str]:
    """Map path -> 'A' (added), 'M' (modified) or 'D' (deleted) compared with ``since``.

    Compares the working tree (committed, staged, unstaged and untracked) with ``since``.
    Paths matching a pattern in ``ignore`` are left out.
    """
    status: dict[str, str] = {}
    raw = git(work, "diff", "--name-status", "--no-renames", "-z", since, "--").stdout.split("\0")
    for code, path in zip(raw[0::2], raw[1::2]):
        if code:
            status[path] = code[0]
    if include_untracked:
        for path in _untracked(work):
            status.setdefault(path, "A")
    return {p: s for p, s in sorted(status.items()) if not glob_match(p, ignore)}


def changed_files(work: Path | str, since: str = TAG_START, *, include_untracked: bool = True,
                  ignore: Sequence[str] = TOOL_NOISE) -> list[str]:
    """Sorted paths changed since ``since`` (see ``changed_status``)."""
    return list(changed_status(work, since, include_untracked=include_untracked, ignore=ignore))


def _count_lines(path: Path) -> int:
    try:
        data = path.read_bytes()
    except OSError:
        return 0
    if b"\0" in data[:8000]:
        return 0
    return len(data.splitlines())


def diff_numstat(work: Path | str, since: str = TAG_START, *, include_untracked: bool = True,
                 ignore: Sequence[str] = TOOL_NOISE) -> DiffStat:
    """Lines added and deleted since ``since``, and the files involved.

    Untracked files count all their lines as added. Binary files count as changed files
    with zero lines.
    """
    added = deleted = 0
    files: list[str] = []
    raw = git(work, "diff", "--numstat", "--no-renames", "-z", since, "--").stdout
    for record in raw.split("\0"):
        if not record:
            continue
        a, d, path = record.split("\t", 2)
        if glob_match(path, ignore):
            continue
        files.append(path)
        added += int(a) if a.isdigit() else 0
        deleted += int(d) if d.isdigit() else 0
    if include_untracked:
        for path in _untracked(work):
            if glob_match(path, ignore) or path in files:
                continue
            files.append(path)
            added += _count_lines(Path(work) / path)
    return DiffStat(sorted(files), added, deleted)


def commits_since(
    work: Path | str,
    since: str = TAG_START,
    ref: str = "HEAD",
    *,
    first_parent: bool = False,
    no_merges: bool = False,
) -> list[Commit]:
    """Commits reachable from ``ref`` but not from ``since``, oldest first."""
    fmt = "%H%x1f%an%x1f%ae%x1f%aI%x1f%P%x1f%s%x1f%b%x1e"
    args = ["log", "--reverse", f"--format={fmt}"]
    args += ["--first-parent"] if first_parent else []
    args += ["--no-merges"] if no_merges else []
    args.append(f"{since}..{ref}")
    text = git(work, *args).stdout
    commits = []
    for record in text.split("\x1e"):
        record = record.strip("\n")
        if not record:
            continue
        sha, name, email, date, parents, subject, body = record.split("\x1f", 6)
        commits.append(Commit(sha, subject, body.strip(), name, email, date, parents.split()))
    return commits


def status_porcelain(work: Path | str, *, ignore: Sequence[str] = TOOL_NOISE) -> list[str]:
    """Lines of ``git status --porcelain`` (uncommitted changes), minus ignored noise."""
    lines = git(work, "status", "--porcelain", "--untracked-files=all").stdout.splitlines()
    return [line for line in lines if not glob_match(line[3:].strip('"'), ignore)]


def is_clean(work: Path | str, *, ignore: Sequence[str] = TOOL_NOISE) -> bool:
    return not status_porcelain(work, ignore=ignore)


def file_at(work: Path | str, ref: str, path: str) -> str | None:
    """Contents of ``path`` at ``ref``, or None if it does not exist there."""
    result = git(work, "show", f"{ref}:{path}", check=False)
    return result.stdout if result.ok else None


def show_bytes(work: Path | str, ref: str, path: str) -> bytes | None:
    """Raw bytes of ``path`` at ``ref`` (exact, also for binary files), or None if it does not exist there."""
    import subprocess

    proc = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=str(work), env=_env(), capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def is_ancestor(work: Path | str, ancestor: str, descendant: str = "HEAD") -> bool:
    """True when commit ``ancestor`` is reachable from ``descendant`` (that is, it has been merged in)."""
    return git(work, "merge-base", "--is-ancestor", ancestor, descendant, check=False).returncode == 0


def merged_branches(work: Path | str, into: str = "main", *, exclude: Sequence[str] = ("main", "master")) -> list[str]:
    """Local branches whose tips are already part of ``into`` (excluding ``into`` itself and ``exclude``)."""
    text = out(work, "branch", "--merged", into, "--format=%(refname:short)")
    return [b for b in text.splitlines() if b and b != into and b not in exclude]


def is_git_repo(work: Path | str) -> bool:
    return (Path(work) / ".git").exists()
