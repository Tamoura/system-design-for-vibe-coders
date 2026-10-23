"""The lab framework: what a lab is, how labs are found, started, graded and solved.

A lab lives in ``ailab/labs/mNN_slug/`` and defines ``LAB = Lab(...)`` in ``lab.py``.
The framework knows nothing about any particular lab; ``cli.py`` is a thin shell over it.

Discovery is *tolerant*: labs are found by folder name, and a lab's ``lab.py`` is only
imported when that lab is asked for. A lab that fails to import shows up as BROKEN in
``python -m ailab list`` and never prevents any other lab from being found or run.
"""
from __future__ import annotations

import importlib
import re
import shutil
import sys
import traceback
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from ailab import gitutil, runner

KIT_DIR = Path(__file__).resolve().parent
BASE_REPO = KIT_DIR / "base" / "remit"
LABS_DIR = KIT_DIR / "labs"
LAB_START_TAG = gitutil.TAG_START

_DIR_RE = re.compile(r"^m(\d{2})(?:_[A-Za-z0-9_]+)?$")
_COPY_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache", "*.egg-info", ".git", ".DS_Store")

# Never part of a learner's work: kept out of git status with .git/info/exclude.
_LOCAL_EXCLUDES = (".claude/settings.local.json", ".DS_Store", ".aider*", ".idea/", ".vscode/")


class LabError(Exception):
    """A problem the learner (or lab author) should be told about plainly."""


@dataclass
class Check:
    """One line of a grade report.

    name      short label, e.g. "Tests pass"
    ok        did the work satisfy it?
    detail    what was found, in terms the learner can act on ("2 tests fail: ...")
    hint      what to try next; never the hidden answer
    required  only required checks decide whether the lab passes; the rest are advisory
    """

    name: str
    ok: bool
    detail: str = ""
    hint: str = ""
    required: bool = True


@dataclass
class Lab:
    """Everything the kit needs to know about a lab.

    seed(work)    turn the fresh Remit copy into this lab's starting situation (edit files,
                  add files, create branches or commits). Must be deterministic and offline.
    grade(work)   inspect the learner's work directory and return a list of Check. Must not
                  modify the work directory and must not execute learner code in-process.
    solve(work)   apply the reference solution so that grade() passes (it commits too if
                  the lab asks for commits).

    The remaining fields locate the lab's files; by default they are looked up next to
    lab.py: task.md, assets/, solution/, hidden/.
    """

    id: str  # "m00" .. "m14"; must equal the folder's prefix
    title: str
    lesson: str  # "0.2"
    needs_agent: bool
    seed: Callable[[Path], None]
    grade: Callable[[Path], list[Check]]
    solve: Callable[[Path], None]
    task_path: Path | None = None
    assets_path: Path | None = None
    home: Path | None = None  # the lab folder; set by discovery when left empty
    extra: dict[str, object] = field(default_factory=dict)  # free space for lab authors

    @property
    def task_file(self) -> Path:
        return self.task_path or self._home() / "task.md"

    @property
    def assets_dir(self) -> Path | None:
        path = self.assets_path or self._home() / "assets"
        return path if path.is_dir() else None

    @property
    def solution_dir(self) -> Path:
        return self._home() / "solution"

    @property
    def hidden_dir(self) -> Path:
        return self._home() / "hidden"

    def _home(self) -> Path:
        if self.home is None:
            raise LabError(f"lab {self.id} has no home folder (it was not loaded by discovery)")
        return self.home


# -- discovery -------------------------------------------------------------------
@dataclass
class LabEntry:
    """A lab folder and, once loaded, either its Lab or the reason it could not be loaded."""

    dirname: str
    lab: Lab | None = None
    error: str | None = None

    @property
    def id(self) -> str:
        return self.dirname.split("_", 1)[0].lower()

    @property
    def broken(self) -> bool:
        return self.lab is None


def lab_dirnames() -> list[str]:
    """Names of the lab folders, sorted, without importing anything."""
    if not LABS_DIR.is_dir():
        return []
    return sorted(p.name for p in LABS_DIR.iterdir() if p.is_dir() and _DIR_RE.match(p.name))


def normalise_id(text: str) -> str:
    """'m5', 'M05', '5' and '05' all mean 'm05'; a full folder name is reduced to its id."""
    text = text.strip().lower()
    if re.fullmatch(r"m?\d{1,2}", text):
        return f"m{int(text.lstrip('m')):02d}"
    return text.split("_", 1)[0]


def find_dirname(lab_id: str) -> str:
    """The folder for ``lab_id`` ('m05', 'M5', 'm05_loyalty_review'). Raises LabError if none."""
    wanted = normalise_id(lab_id)
    names = [n for n in lab_dirnames() if n.split("_", 1)[0].lower() == wanted]
    if not names:
        known = ", ".join(n.split("_", 1)[0] for n in lab_dirnames()) or "none"
        raise LabError(f"no lab {lab_id!r}. Labs found: {known}")
    if len(names) > 1:
        raise LabError(f"more than one folder for lab {wanted}: {', '.join(names)}")
    return names[0]


def load_entry(dirname: str) -> LabEntry:
    """Import ``labs/<dirname>/lab.py`` and validate it. Never raises; failures become ``error``."""
    entry = LabEntry(dirname)
    folder = LABS_DIR / dirname
    module_name = f"ailab.labs.{dirname}.lab"
    if not (folder / "lab.py").is_file():
        entry.error = "lab.py is missing"
        return entry
    sys.modules.pop(module_name, None)
    importlib.invalidate_caches()  # a lab folder may have been created after the first import
    try:
        module = importlib.import_module(module_name)
    except BaseException as exc:  # a broken lab must never take the kit down (not even SystemExit)
        if isinstance(exc, KeyboardInterrupt):
            raise
        sys.modules.pop(module_name, None)
        last = traceback.format_exception_only(type(exc), exc)[-1].strip()
        entry.error = f"{last}"
        return entry
    lab = getattr(module, "LAB", None)
    if not isinstance(lab, Lab):
        entry.error = "lab.py does not define LAB = Lab(...)"
        return entry
    if lab.id.lower() != entry.id:
        entry.error = f"LAB.id is {lab.id!r} but the folder is {dirname!r}"
        return entry
    for attr in ("seed", "grade", "solve"):
        if not callable(getattr(lab, attr)):
            entry.error = f"LAB.{attr} is not callable"
            return entry
    if lab.home is None:
        lab.home = folder
    if not lab.task_file.is_file():
        entry.error = f"task.md is missing ({lab.task_file.name})"
        return entry
    entry.lab = lab
    return entry


def discover() -> list[LabEntry]:
    """Load every lab folder (tolerantly) and return the entries, sorted by id."""
    return [load_entry(name) for name in lab_dirnames()]


def load_lab(lab_id: str) -> Lab:
    """Load exactly one lab by id. Raises LabError if it does not exist or is broken."""
    entry = load_entry(find_dirname(lab_id))
    if entry.lab is None:
        raise LabError(f"lab {entry.id} is BROKEN: {entry.error}")
    return entry.lab


# -- seed helpers (for lab authors) ---------------------------------------------------
def read_file(work: Path, rel: str) -> str:
    return (Path(work) / rel).read_text(encoding="utf-8")


def write_file(work: Path, rel: str, text: str) -> Path:
    """Create or overwrite ``rel`` (parent folders are created)."""
    path = Path(work) / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def edit_file(work: Path, rel: str, old: str, new: str, *, count: int = 1) -> None:
    """Replace ``old`` with ``new`` in ``rel``; ``old`` must occur exactly ``count`` times.

    The strictness is the point: if the base repository ever changes under a seed, the
    seed fails loudly instead of silently doing nothing.
    """
    text = read_file(work, rel)
    found = text.count(old)
    if found != count:
        raise LabError(f"edit_file({rel}): expected {count} occurrence(s) of {old[:50]!r}, found {found}")
    write_file(work, rel, text.replace(old, new))


def remove_file(work: Path, rel: str) -> None:
    (Path(work) / rel).unlink()


def add_reference_memory(work: Path) -> bool:
    """Copy the reference project memory (labs/m02_*/solution/CLAUDE.md) into ``work``.

    Labs after m02 call this from ``seed`` when the learner should start with a good
    memory file. Returns True if a file was copied; a no-op returning False when the
    m02 lab or its solution file does not exist (yet).
    """
    for source in sorted(LABS_DIR.glob("m02_*/solution/CLAUDE.md")):
        shutil.copyfile(source, Path(work) / "CLAUDE.md")
        return True
    return False


# -- the lifecycle -----------------------------------------------------------------
def start_lab(lab: Lab, dest: Path | str) -> Path:
    """Create the work directory for ``lab``. Returns its (resolved) path.

    1. copy the base repository (no caches, no .git)   2. git init, commit "Initial state"
    3. lab.seed(work)                                   4. copy assets/ to lab-assets/ and write TASK.md
    5. commit everything as "Lab starting state" and tag it ``lab-start``.
    """
    work = Path(dest).expanduser().resolve()
    existed = work.exists()
    if existed and (not work.is_dir() or any(work.iterdir())):
        raise LabError(f"{work} already exists and is not empty; choose a new directory")
    work.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copytree(BASE_REPO, work, ignore=_COPY_IGNORE, dirs_exist_ok=True)
        gitutil.init_repo(work)
        gitutil.ensure_identity(work)
        gitutil.set_config(work, "ailab.lab", lab.id)
        gitutil.add_local_excludes(work, _LOCAL_EXCLUDES)
        gitutil.commit_all(work, "Initial state")
        lab.seed(work)
        if lab.assets_dir is not None:
            shutil.copytree(lab.assets_dir, work / "lab-assets", ignore=_COPY_IGNORE)
        shutil.copyfile(lab.task_file, work / "TASK.md")
        gitutil.commit_all(work, "Lab starting state", allow_empty=True, force=["lab-assets", "TASK.md"])
        gitutil.tag(work, LAB_START_TAG)
    except BaseException:
        if existed:  # leave the empty directory the learner gave us, but empty
            for child in work.iterdir():
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()
        else:
            shutil.rmtree(work, ignore_errors=True)
        raise
    return work


def check_work_dir(work: Path | str) -> Path:
    """Validate that ``work`` was made by ``ailab start``; return it resolved."""
    path = Path(work).expanduser().resolve()
    if not path.is_dir():
        raise LabError(f"{path} is not a directory")
    if not gitutil.is_git_repo(path) or not gitutil.has_ref(path, LAB_START_TAG):
        raise LabError(f"{path} was not created by `python -m ailab start` (no '{LAB_START_TAG}' tag)")
    return path


def started_lab_id(work: Path) -> str | None:
    return gitutil.get_config(work, "ailab.lab")


def grade_lab(lab: Lab, work: Path | str, *, catch: bool = True) -> list[Check]:
    """Run the lab's grader. With ``catch`` a crashing grader becomes a failing check."""
    path = check_work_dir(work)
    if not catch:
        return lab.grade(path)
    try:
        checks = lab.grade(path)
    except Exception as exc:  # a grader bug must not look like a learner's mistake
        last = traceback.format_exception_only(type(exc), exc)[-1].strip()
        return [Check("Grader ran", False, f"internal grader error: {last}",
                      "This is a bug in the lab, not in your work. Tell the course maintainers.")]
    if not checks:
        return [Check("Grader ran", False, "the grader returned no checks", "This is a bug in the lab.")]
    return checks


def passed(checks: list[Check]) -> bool:
    """True when every required check passed (advisory checks never block)."""
    return all(c.ok for c in checks if c.required)


def solve_lab(lab: Lab, work: Path | str, *, force: bool = False) -> None:
    """Apply the reference solution. Refuses when the learner has already changed things, unless ``force``."""
    path = check_work_dir(work)
    if not force and gitutil.changed_files(path):
        raise LabError("you already have changes in this directory; use --force to apply the solution anyway")
    lab.solve(path)


# -- doctor ---------------------------------------------------------------------------
def doctor_checks(directory: Path | str | None = None) -> list[Check]:
    """The environment checks behind ``python -m ailab doctor``."""
    checks: list[Check] = []
    version = ".".join(str(part) for part in sys.version_info[:3])
    checks.append(Check("Python 3.11 or newer", sys.version_info >= (3, 11), f"Python {version} ({sys.executable})",
                        "Install Python 3.11+ and run the kit with it."))

    git_path = runner.which("git")
    git_version = runner.run(["git", "--version"], timeout=15) if git_path else None
    checks.append(Check("git is installed", bool(git_version and git_version.ok),
                        git_version.stdout.strip() if git_version and git_version.ok else "git was not found on PATH",
                        "Install git (https://git-scm.com) and make sure `git --version` works."))

    pytest_result = runner.run([sys.executable, "-c", "import pytest; print(pytest.__version__)"],
                               env=runner.clean_env(), timeout=30)
    checks.append(Check("pytest can be imported", pytest_result.ok,
                        f"pytest {pytest_result.stdout.strip()}" if pytest_result.ok else "import pytest failed",
                        f"Run: {sys.executable} -m pip install pytest"))

    target = Path(directory).expanduser() if directory else Path.cwd()
    writable, why = _writable(target)
    checks.append(Check("working directory is writable", writable, why or str(target.resolve()),
                        "Choose a directory you can write to (use --dir)."))

    identity = runner.run(["git", "config", "--get", "user.email"], timeout=15, env=runner.clean_env()) if git_path else None
    has_identity = bool(identity and identity.ok and identity.stdout.strip())
    checks.append(Check("git knows who you are (needed to commit)", has_identity,
                        identity.stdout.strip() if has_identity and identity else "no user.email configured",
                        'Run: git config --global user.name "Your Name" && git config --global user.email "you@example.com"',
                        required=False))
    base_ok = (BASE_REPO / "pyproject.toml").is_file() and (BASE_REPO / "src" / "remit").is_dir()
    checks.append(Check("lab kit is complete", base_ok, str(BASE_REPO) if base_ok else "base repository missing",
                        "Re-clone the course repository."))
    return checks


def _writable(directory: Path) -> tuple[bool, str]:
    import tempfile

    probe = directory
    while not probe.exists() and probe != probe.parent:  # a directory to be created: test its parent
        probe = probe.parent
    try:
        with tempfile.NamedTemporaryFile(dir=probe):
            pass
    except OSError as exc:
        return False, f"cannot write in {probe}: {exc.strerror or exc}"
    return True, ""
