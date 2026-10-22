"""Helpers that only lab m10 uses (kept out of ``checks.py``, which belongs to the kit).

``new_tests_fail_on_starter`` does what ``checks.tests_fail_on_starter`` does, but it copes with the places
agent tools put their work inside a repository: a git worktree under ``.claude/worktrees/`` is an *untracked
directory*, and the kit's helper tries to ``unlink`` it. The lab m10 learner is exactly the person who has
such directories lying around when they grade.
"""
from __future__ import annotations

import tempfile
from collections.abc import Sequence
from pathlib import Path

from ailab import checks, gitutil
from ailab.framework import LAB_START_TAG, Check


def new_tests_fail_on_starter(
    work: Path | str,
    *,
    since: str = LAB_START_TAG,
    name: str = "Your new tests fail on the original code",
    hint: str = "A test that passes before your change proves nothing. Add tests that need the new behaviour.",
    keep: Sequence[str] = ("tests/**",),
    timeout: float = 60.0,
    required: bool = False,
) -> Check:
    """The test files the learner added or changed contain tests that FAIL when every non-test file is put back
    to its state at ``since``. (Old tests in the same file still pass; one failure is enough.)"""
    work = Path(work)
    chosen = checks.new_test_files(work, since)
    if not chosen:
        return Check(name, False, "no new or changed test files found", "Add your tests in tests/test_*.py.", required)
    with tempfile.TemporaryDirectory(prefix="ailab-m10-") as scratch:
        root = checks.copy_work(work, Path(scratch) / "work")
        for path, state in gitutil.changed_status(work, since).items():  # tool noise is left out, so are nested worktrees
            if gitutil.glob_match(path, keep) or path.endswith("/"):
                continue
            target = root / path
            original = None if state == "A" else gitutil.show_bytes(work, since, path)
            if original is None:
                if target.is_file():
                    target.unlink()
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(original)
        existing = [p for p in chosen if (root / p).exists()]
        result = checks.run_pytest(root, existing, timeout=timeout)
    caught = result.failed + result.errors
    if result.timed_out or caught:
        detail = f"{checks.plural(caught, 'test')} fail on the original code, as they should" if caught else \
            "the tests do not finish on the original code"
        return Check(name, True, detail, "", required)
    return Check(name, False, "all of your new tests already pass on the original code, so they would not have caught its absence",
                 hint, required)
