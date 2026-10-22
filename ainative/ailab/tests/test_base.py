"""The pristine base repository (ailab/base/remit): its own test suite passes in a temporary copy,
it is deterministic, and it has the shape the lab plan relies on.

If a test here fails, a lab writer (or the kit builder) changed the base. The base is frozen: labs
change it only through ``seed()``.
"""
from __future__ import annotations

import ast
import json
import re
import shutil
from pathlib import Path

import pytest

from ailab import checks, framework, runner

BASE = framework.BASE_REPO
SRC = BASE / "src"


@pytest.fixture(scope="module")
def copy(tmp_path_factory):
    dest = tmp_path_factory.mktemp("base") / "remit"
    shutil.copytree(BASE, dest, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.egg-info"))
    return dest


def pytest_in(copy: Path, *args: str, env: dict[str, str] | None = None, timeout: float = 120):
    return runner.run_python(["-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "no:randomly", *args], cwd=copy,
                             extra_env=env, timeout=timeout)


def test_the_base_suite_passes_in_a_copy(copy):
    result = pytest_in(copy)
    assert result.ok, result.output[-3000:]
    assert re.search(r"\b99 passed\b", result.stdout), result.stdout[-300:]


def test_the_number_of_tests_is_in_the_planned_band():
    result = checks.run_pytest(BASE)
    assert result.ok and 60 <= result.passed <= 100, result.summary()


def test_running_the_suite_leaves_the_base_clean():
    checks.run_pytest(BASE)
    junk = [p for p in BASE.rglob("*") if p.name in ("__pycache__", ".pytest_cache", "remit.db", "audit.jsonl")]
    assert junk == [], f"stray files in the frozen base: {junk}"


@pytest.mark.parametrize("env", [{"TZ": "Asia/Tokyo"}, {"TZ": "America/Los_Angeles"}, {"PYTHONHASHSEED": "12345"}, {"LC_ALL": "C"}])
def test_the_suite_does_not_depend_on_timezone_hash_seed_or_locale(copy, env):
    result = pytest_in(copy, env=env)
    assert result.ok, result.output[-2000:]


def test_each_test_file_passes_on_its_own_and_in_reverse_order(copy):
    for path in sorted((copy / "tests").glob("test_*.py")):
        result = pytest_in(copy, f"tests/{path.name}")
        assert result.ok, f"{path.name} fails alone:\n{result.output[-1500:]}"
    files = [f"tests/{p.name}" for p in sorted((copy / "tests").glob("test_*.py"), reverse=True)]
    assert pytest_in(copy, *files).ok


def test_the_documented_command_works_without_installing_anything(copy):
    result = runner.run_python(["-m", "remit", "quote", "QAR", "500", "INR"], cwd=copy, pythonpath=[copy / "src"])
    assert result.ok and "Receive:   11286.00 INR" in result.stdout


# -- the shape the lab plan relies on ---------------------------------------------------------
REQUIRED_FILES = [
    "README.md", "CONTRIBUTING.md", "pyproject.toml", ".gitignore", ".env.example", ".github/workflows/ci.yml",
    "docs/ARCHITECTURE.md", "docs/najmkit.md", "docs/TOUR.md",
    "src/remit/__init__.py", "src/remit/__main__.py", "src/remit/cli.py", "src/remit/config.py", "src/remit/corridors.py",
    "src/remit/errors.py", "src/remit/fees.py", "src/remit/fx.py", "src/remit/ledger.py", "src/remit/limits.py",
    "src/remit/models.py", "src/remit/money.py", "src/remit/notify.py", "src/remit/screening.py", "src/remit/service.py",
    "src/remit/store.py", "src/najmkit/__init__.py", "src/najmkit/ids.py", "src/najmkit/clock.py", "src/najmkit/audit.py",
    "tests/conftest.py", "tests/test_money.py", "tests/test_fees.py", "tests/test_fx.py", "tests/test_limits.py",
    "tests/test_notify.py", "tests/test_service.py",
]


def test_the_expected_files_exist():
    assert [f for f in REQUIRED_FILES if not (BASE / f).is_file()] == []


def test_ledger_and_screening_have_no_tests_of_their_own():
    names = {p.name for p in (BASE / "tests").glob("*.py")}
    assert not names & {"test_ledger.py", "test_screening.py"}
    for path in (BASE / "tests").glob("test_*.py"):
        text = path.read_text(encoding="utf-8")
        assert not re.search(r"\bpost_transfer\b|\bmatch_score\b|\bscreening\.", text), f"{path.name} tests a legacy module"


def test_the_source_size_is_in_the_planned_band():
    def sloc(path: Path) -> int:
        lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
        return sum(1 for line in lines if line and not line.startswith("#"))

    total = sum(sloc(p) for p in (SRC / "remit").glob("*.py")) + sum(sloc(p) for p in (SRC / "najmkit").glob("*.py"))
    assert 1000 <= total <= 2000, total  # "about 1,000-1,500 lines" of code; docstrings count here


def test_the_deliberate_gaps_are_really_gaps():
    """Things later labs add. If one of these exists in the base, a lab's premise is gone."""
    assert not (SRC / "remit" / "risk.py").exists()  # D-ARCH-1: the architecture doc still mentions it
    assert "risk.py" in (BASE / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8")
    code = (
        "import json\n"
        "from remit import corridors, fees, fx, money, notify\n"
        "print(json.dumps({\n"
        "  'corridor': 'QAR-BDT' in corridors.CORRIDORS, 'rate': 'QAR-BDT' in fx.DEFAULT_MID_RATES,\n"
        "  'margin': 'QAR-BDT' in fx.CORRIDOR_MARGINS, 'currency': 'BDT' in money.CURRENCIES,\n"
        "  'arabic_name': 'BDT' in notify.CURRENCY_NAMES_AR, 'templates': sorted(notify.TEMPLATES),\n"
        "  'schedules': sorted(fees.SCHEDULES)}))\n"
    )
    result = runner.run_python(["-c", code], pythonpath=[SRC])
    assert result.ok, result.output
    got = json.loads(result.stdout)
    # BDT exists as a currency (and has an Arabic name), but the BDT corridor, rate, margin and fee schedule do not
    assert got == {"corridor": False, "rate": False, "margin": False, "currency": True, "arabic_name": True,
                   "templates": ["transfer_failed", "transfer_sent"], "schedules": ["STD-A", "STD-B"]}


def test_house_rules_hold_in_the_base_source():
    """CONTRIBUTING.md says money is never float and the service never reads the clock or uuid directly."""
    for path in (SRC / "remit").glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert not re.search(r"\bfloat\s*\(", text), f"{path.name} calls float()"
        assert "uuid" not in text and "datetime.now" not in text and "utcnow" not in text, path.name
    # sqlite stores money as TEXT: no REAL/FLOAT/DOUBLE column in the schema
    schema = re.search(r'_SCHEMA = """(.*?)"""', (SRC / "remit" / "store.py").read_text(encoding="utf-8"), re.S).group(1)
    assert not re.search(r"\b(REAL|FLOAT|DOUBLE|NUMERIC)\b", schema)


def test_the_najmkit_library_is_used_at_six_or_more_call_sites():
    uses = 0
    for path in (SRC / "remit").glob("*.py"):
        uses += len(re.findall(r"\b(?:ids\.new_id|audit\.log_event|audit\.configure|clock\.now|SystemClock)\(", path.read_text(encoding="utf-8")))
    assert uses >= 6, uses


def test_the_stale_todo_and_the_long_function_are_there():
    assert "TODO(farid, 2022)" in (SRC / "remit" / "screening.py").read_text(encoding="utf-8")
    tree = ast.parse((SRC / "remit" / "service.py").read_text(encoding="utf-8"))
    send = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "send")
    assert send.end_lineno - send.lineno >= 60  # one long function, on purpose


def test_no_secrets_in_the_base():
    from ailab.checks import find_secrets

    for path in BASE.rglob("*"):
        if path.is_file() and ".git" not in path.parts and path.suffix in {".py", ".md", ".toml", ".yml", ".example", ""}:
            assert find_secrets(path.read_text(encoding="utf-8")) == [], path
