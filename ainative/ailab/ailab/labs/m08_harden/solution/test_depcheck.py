"""Tests for the dependency check: build a tiny project in a temporary folder and run the script on it (reference solution of lab m08)."""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "depcheck.py"


def check(root):
    result = subprocess.run([sys.executable, str(SCRIPT), str(root)], capture_output=True, text=True, timeout=10)
    flags = [line.split()[1].rstrip(":") for line in result.stdout.splitlines() if line.startswith("FLAG ")]
    return result.returncode, flags


def make(root, **files):
    for rel, text in files.items():
        path = root / rel.replace("__", "/")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def test_a_project_with_only_listed_packages_is_clean(tmp_path):
    make(tmp_path, **{"requirements.txt": "colourlib>=1.0\n", "deps-allowlist.txt": "colourlib\n"})
    assert check(tmp_path) == (0, [])


def test_an_unlisted_package_is_flagged_whether_declared_or_imported(tmp_path):
    make(tmp_path, **{"requirements.txt": "najm-utils\n", "deps-allowlist.txt": "pytest\n", "src__app.py": "import requests\n"})
    code, flags = check(tmp_path)
    assert code == 1 and sorted(flags) == ["najm-utils", "requests"]


def test_names_are_compared_after_normalising_them(tmp_path):
    make(tmp_path, **{"requirements.txt": "Typing_Helpers[fast]>=1 ; python_version >= '3.11'\n", "deps-allowlist.txt": "typing-helpers\n"})
    assert check(tmp_path) == (0, [])


def test_a_package_from_a_url_is_always_flagged(tmp_path):
    make(tmp_path, **{"requirements.txt": "helper @ https://files.example.invalid/helper.tar.gz\n", "deps-allowlist.txt": "helper\n"})
    assert check(tmp_path) == (1, ["helper"])
