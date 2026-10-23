# lab-assets/example/check_ex4.py
"""Example EX4: do the tests the tool wrote notice when the rule changes?

Running the new tests is not enough for a "write tests" task: a test that asserts nothing passes. This check runs them
twice. On the real code they must pass. On a copy where the rule has been changed they must fail. To reuse it, change
the three constants: the tests file the prompt asks for, the code it is about, and the one-line change to the rule.
"""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

TESTS = "tests/test_fees_express_cap.py"
TARGET = "src/remit/fees.py"
OLD, NEW = "total=base + surcharge,", "total=min(base + surcharge, cap),"  # the cap would now cover the express surcharge


def tests_pass(root):
    env = dict(os.environ, PYTHONPATH=str(pathlib.Path(root).resolve() / "src"))
    run = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TESTS]
    return subprocess.run(run, cwd=root, env=env, capture_output=True, text=True).returncode == 0


if not pathlib.Path(TESTS).is_file():
    sys.exit(f"{TESTS} does not exist yet")
if not tests_pass("."):
    sys.exit(f"{TESTS} must pass on the real code")
with tempfile.TemporaryDirectory() as tmp:
    copy = pathlib.Path(tmp) / "work"
    shutil.copytree(".", copy, ignore=shutil.ignore_patterns(".git", "__pycache__", "eval", "lab-assets"))
    target = copy / TARGET
    source = target.read_text(encoding="utf-8")
    assert OLD in source, "the line to change was not found: has the code changed?"
    target.write_text(source.replace(OLD, NEW), encoding="utf-8")
    if tests_pass(copy):
        sys.exit("the tests still pass when the rule is changed: they do not pin it down")
