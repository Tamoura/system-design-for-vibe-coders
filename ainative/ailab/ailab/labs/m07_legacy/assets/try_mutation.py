"""Break the ORIGINAL ledger in one place and see whether your characterization tests notice.

Run it from the root of your lab repository (the folder with TASK.md and .git):

    python lab-assets/try_mutation.py
        runs your tests/test_ledger_*.py on the original code (the lab-start tag); they must all pass

    python lab-assets/try_mutation.py src/remit/ledger.py "OLD TEXT" "NEW TEXT"
        replaces OLD TEXT (it must occur exactly once in the file) in a scratch copy of the original
        code and runs your tests there

KILLED means a test failed: you have pinned that behaviour. SURVIVED means every test still passed:
that behaviour is not pinned (or the change does not alter behaviour at all). If the module crashed (a
NameError, a missing import) instead of one behaviour changing, the script says so: that kill proves
nothing, so fix the replacement and run it again.

Your working copy is never touched; everything happens in a temporary folder. Standard library only.
"""
import io
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path


def counts(output: str) -> dict[str, int]:
    return {word: int(n) for n, word in re.findall(r"(\d+) (passed|failed|error)", output)}


def main(argv: list[str]) -> int:
    root = Path.cwd()
    if len(argv) not in (0, 3) or not (root / ".git").exists() or not (root / "tests").is_dir():
        print(__doc__)
        return 2
    with tempfile.TemporaryDirectory(prefix="m07-original-") as scratch:
        copy = Path(scratch)
        archive = subprocess.run(["git", "archive", "--format=tar", "lab-start"], cwd=root, capture_output=True, check=True).stdout
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            try:
                tar.extractall(copy, filter="data")
            except TypeError:  # Python before 3.11.4 has no extraction filters; this archive comes from your own git
                tar.extractall(copy)
        mine, helpers = [], []  # your new test files, and the new helpers they import (the seam)
        for path in sorted((root / "tests").rglob("*.py")):
            rel = path.relative_to(root).as_posix()
            if "__pycache__" in path.parts or path.name == "conftest.py" or (copy / rel).exists():
                continue  # not yours: a file the lab started with
            if path.name.startswith("test_ledger"):
                mine.append(rel)
            elif not path.name.startswith("test_"):
                helpers.append(rel)
        if not mine:
            print("No tests/test_ledger_*.py yet: write some first.")
            return 2
        for rel in mine + helpers:
            (copy / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / rel, copy / rel)
        if argv:
            target, old, new = argv
            text = (copy / target).read_text(encoding="utf-8")
            if text.count(old) != 1:
                print(f"{target} contains that text {text.count(old)} times; it must occur exactly once. Change the text you search for.")
                return 2
            (copy / target).write_text(text.replace(old, new), encoding="utf-8", newline="\n")
        run = subprocess.run([sys.executable, "-P", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-W", "ignore::DeprecationWarning",
                              *mine], cwd=copy, capture_output=True, text=True)
    found = counts(run.stdout)
    total = sum(found.values())
    failed = found.get("failed", 0) + found.get("error", 0)
    if not argv:
        if run.returncode == 0:
            print(f"OK: your {found.get('passed', 0)} tests pass on the original code.")
            return 0
        print(f"Your tests do not pass on the original code ({failed} of {total} fail). First lines of the output:")
        print("\n".join(run.stdout.strip().splitlines()[-12:]))
        return 1
    if run.returncode == 0:
        print(f"SURVIVED: all {total} tests still pass. Nothing you have written notices this change.")
        return 1
    crash = re.search(r"^E\s+((?:NameError|SyntaxError|IndentationError|ImportError|ModuleNotFoundError)\b.*)$", run.stdout, flags=re.M)
    if crash or failed == total:
        why = f"with {crash.group(1)}" if crash else f"and all {total} tests failed"
        print(f"KILLED, but the module crashed ({why}) instead of one behaviour changing.")
        print("That proves nothing: fix the replacement text (an import you did not add?) and run it again.")
        return 1
    print(f"KILLED by {failed} of {total} tests: you have pinned this behaviour.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
