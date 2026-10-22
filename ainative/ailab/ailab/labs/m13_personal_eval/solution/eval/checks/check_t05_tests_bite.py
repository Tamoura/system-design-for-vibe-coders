"""T05: do the tests the tool wrote pin down the half-even rounding of the partner's share?

Two runs. On the real code the tests must pass. On a copy where the share is rounded half up instead, they must
fail: tests that survive that change would not notice if someone 'fixed' the quirk.
"""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

TESTS = "tests/test_ledger_partner_share.py"
LEDGER = "src/remit/ledger.py"


def run_tests(root):
    env = dict(os.environ, PYTHONPATH=str(pathlib.Path(root).resolve() / "src"))
    result = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TESTS],
                            cwd=root, env=env, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


code, output = run_tests(".")
if code != 0:
    sys.exit(f"{TESTS} must exist and pass on the real code:\n" + output[-300:])

with tempfile.TemporaryDirectory() as tmp:
    copy = pathlib.Path(tmp) / "work"
    shutil.copytree(".", copy, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", "eval", "lab-assets"))
    ledger = copy / LEDGER
    source = ledger.read_text(encoding="utf-8")
    changed = source.replace("ROUND_HALF_EVEN", "ROUND_HALF_UP")
    assert changed != source, "the mutation did not apply: the ledger code changed"
    ledger.write_text(changed, encoding="utf-8")
    code, _ = run_tests(copy)
    if code == 0:
        sys.exit("the tests still pass when the partner's share is rounded half up: they do not pin the rule")
