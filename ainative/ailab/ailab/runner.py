"""Run external commands with a timeout, captured output and a controlled environment.

Everything in the kit that starts a subprocess (pytest, git, a learner's script) goes
through ``run`` so that a hung command can never hang a grader: on timeout the whole
process group is killed.
"""
from __future__ import annotations

import os
import shutil
import signal
import subprocess
import sys
import time
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

DEFAULT_TIMEOUT = 60.0

# Environment variables that must never leak from the learner's shell into a grader run.
_SCRUB_PREFIXES = ("REMIT_", "NAJMKIT_", "PYTEST_", "GIT_")
_SCRUB_EXACT = ("PYTHONPATH", "PYTHONSTARTUP", "PYTHONINSPECT", "PYTHONOPTIMIZE", "VIRTUAL_ENV_PROMPT")


@dataclass
class RunResult:
    cmd: list[str]
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool
    duration: float

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and not self.timed_out

    @property
    def output(self) -> str:
        """stdout followed by stderr."""
        return self.stdout + self.stderr


def clean_env(
    pythonpath: Iterable[str | os.PathLike[str]] = (),
    extra: Mapping[str, str] | None = None,
    *,
    keep_git: bool = False,
) -> dict[str, str]:
    """A copy of ``os.environ`` made safe and deterministic for running a grader.

    * Variables starting with REMIT_, NAJMKIT_, PYTEST_ and GIT_ are removed (GIT_ ones
      only when ``keep_git`` is False; a leaked GIT_DIR would redirect git elsewhere),
      as are PYTHONPATH and friends.
    * ``PYTHONPATH`` is then set to ``pythonpath`` (joined with os.pathsep) when given.
    * Bytecode writing is off, hash seeds fixed, pytest plugin auto-loading is off.
    * ``extra`` is applied last and wins.
    """
    env: dict[str, str] = {}
    for key, value in os.environ.items():
        if key in _SCRUB_EXACT:
            continue
        if key.startswith(_SCRUB_PREFIXES) and not (keep_git and key.startswith("GIT_")):
            continue
        env[key] = value
    env.update(
        PYTHONDONTWRITEBYTECODE="1",
        PYTHONHASHSEED="0",
        PYTHONIOENCODING="utf-8",
        PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
        NO_COLOR="1",
    )
    paths = [str(p) for p in pythonpath]
    if paths:
        env["PYTHONPATH"] = os.pathsep.join(paths)
    if extra:
        env.update(extra)
    return env


def _kill_group(proc: subprocess.Popen[str]) -> None:
    try:
        if os.name == "posix":
            os.killpg(proc.pid, signal.SIGKILL)
        else:  # pragma: no cover - Windows
            proc.kill()
    except (ProcessLookupError, PermissionError):
        pass


def run(
    cmd: Sequence[str | os.PathLike[str]],
    *,
    cwd: str | os.PathLike[str] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    env: Mapping[str, str] | None = None,
    input: str | None = None,
) -> RunResult:
    """Run ``cmd`` and return a RunResult. Never raises for a failing or missing command.

    ``env`` is used as the complete environment when given (build it with ``clean_env``);
    otherwise the current environment is inherited. A command that does not finish within
    ``timeout`` seconds is killed together with its children and ``timed_out`` is True.
    """
    argv = [str(part) for part in cmd]
    started = time.monotonic()
    try:
        proc = subprocess.Popen(
            argv,
            cwd=str(cwd) if cwd is not None else None,
            env=dict(env) if env is not None else None,
            stdin=subprocess.PIPE if input is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            start_new_session=(os.name == "posix"),
        )
    except FileNotFoundError as exc:
        return RunResult(argv, 127, "", f"command not found: {exc.filename or argv[0]}\n", False, 0.0)
    except NotADirectoryError as exc:
        return RunResult(argv, 127, "", f"bad working directory: {exc}\n", False, 0.0)
    timed_out = False
    try:
        stdout, stderr = proc.communicate(input=input, timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_group(proc)
        stdout, stderr = proc.communicate()
    return RunResult(argv, proc.returncode if not timed_out else -9, stdout or "", stderr or "", timed_out,
                     time.monotonic() - started)


def run_python(
    args: Sequence[str | os.PathLike[str]],
    *,
    cwd: str | os.PathLike[str] | None = None,
    pythonpath: Iterable[str | os.PathLike[str]] = (),
    timeout: float = DEFAULT_TIMEOUT,
    extra_env: Mapping[str, str] | None = None,
    input: str | None = None,
) -> RunResult:
    """Run ``python <args>`` with the interpreter that runs the kit and a clean environment."""
    env = clean_env(pythonpath, extra_env)
    return run([sys.executable, *args], cwd=cwd, timeout=timeout, env=env, input=input)


def which(program: str) -> str | None:
    return shutil.which(program)
