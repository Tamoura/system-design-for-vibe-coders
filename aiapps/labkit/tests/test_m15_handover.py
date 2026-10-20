"""Tests for the Module 15.2 lab: labs/m15/uat_runner.py and the handover documents in labs/m15/handover/ and labs/m15/runbooks/.

The runner executes the scenario table of the UAT script against an app and reports. Offline, the app is Lab 7.2's thin slice on the
mock, so a PASS proves that the check ran and the code-decided behaviour holds, never that a real model answers well. The document
tests check FORM and DRIFT (every row has a file, every owner agrees, nothing is pre-signed). Whether the content is true is a
person's review, and the sign-off is people's."""
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

KIT = Path(__file__).resolve().parents[1]
LABS = KIT / "labs" / "m15"
HANDOVER, RUNBOOKS = LABS / "handover", LABS / "runbooks"
SPEC = KIT / "labkit" / "data" / "m06_spec_worked.md"
CAST = {"Maha", "Yara", "Lujain", "Noura", "Hind", "Sara", "Salem", "Layla", "Hamad", "Fahad"}


def load(name):
    spec = importlib.util.spec_from_file_location(f"m15_{name}", LABS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def uat():
    return load("uat_runner")


@pytest.fixture
def script():
    return (HANDOVER / "uat_script.md").read_text(encoding="utf-8")


def reply(kind="answer", text="", handoff=None):
    return SimpleNamespace(kind=kind, text=text, handoff=handoff)


def table(*rows):
    head = "| ID | Criterion | Who | Says | Expect | How |\n|---|---|---|---|---|---|\n"
    return "# s\n\n## Scenarios\n" + head + "".join(f"| {' | '.join(r)} |\n" for r in rows) + "\n## Next\ntext\n"


# ------------------------------------------------------------------ the script as data

def test_the_shipped_script_parses_into_fourteen_unique_rows_with_known_checks(uat, script):
    rows = uat.parse(script)
    assert [r.id for r in rows] == [f"U-{i:02d}" for i in range(1, 15)]
    assert {r.how for r in rows} == {"auto", "real", "person"}
    for r in rows:
        assert r.who and r.says and r.criterion


@pytest.mark.parametrize("rows, message", [
    ([("U-01", "FR-01", "Rayan", "hi", "colour=red", "auto")], "unknown check"),
    ([("U-01", "FR-01", "Rayan", "hi", "kind=answer", "sometimes")], "'how' must be"),
])
def test_a_typo_in_the_script_fails_before_anything_runs(uat, rows, message):
    with pytest.raises(ValueError, match=message):
        uat.parse(table(*rows))


def test_a_script_without_the_table_and_a_short_row_are_rejected(uat):
    with pytest.raises(ValueError, match="no '## Scenarios' table"):
        uat.parse("# nothing here\n")
    with pytest.raises(ValueError, match="U-01: a row needs 6 cells"):
        uat.parse("## Scenarios\n| ID | a | b | c | d | e |\n|---|---|---|---|---|---|\n| U-01 | FR-01 | Rayan |\n")


def test_person_rows_may_say_anything_in_the_expect_cell(uat):
    rows = uat.parse(table(("U-12", "NFR-05", "Yara", "Use the keyboard only", "every task works; Arabic reads right to left", "person")))
    assert rows[0].how == "person"


# ------------------------------------------------------------------ the checks

def test_each_check_tests_one_thing(uat):
    c = uat.CHECKS
    r = reply("refused", "Call the hotline now.\nWe cannot see ticket 4474.", handoff={"x": 1})
    assert c["kind"](r, "refused") and not c["kind"](r, "answer")
    assert c["has"](r, "HOTLINE") and not c["has"](r, "password")          # case does not matter
    assert c["no"](r, "password") and not c["no"](r, "ticket 4474")
    assert c["first"](r, "hotline") and not c["first"](r, "4474")           # only the first line counts
    assert c["handoff"](r, "yes") and not c["handoff"](r, "no") and c["handoff"](reply(), "no")


def test_the_language_check_counts_letters_not_citations(uat):
    arabic = reply(text="يمكنك طلب جهاز جديد عبر البوابة [laptop-requests#0]")
    english = reply(text="Request it through the portal. [laptop-requests#0]")
    assert uat.CHECKS["lang"](arabic, "ar") and not uat.CHECKS["lang"](arabic, "en")
    assert uat.CHECKS["lang"](english, "en") and not uat.CHECKS["lang"](english, "ar")


# ------------------------------------------------------------------ running rows against an app

def test_a_row_passes_only_when_every_check_holds_and_a_fail_says_what_the_app_returned(uat):
    rows = uat.parse(table(("U-01", "FR-01", "Rayan", "hi", "kind=answer; has=three days", "auto"), ("U-02", "FR-01", "Rayan", "hi", "kind=answer; has=four days", "auto")))
    results = uat.run(rows, lambda who, says: reply("answer", "Three days a week."), real=False)
    assert [(r.id, res) for r, res, _ in results] == [("U-01", "PASS"), ("U-02", "FAIL")]
    assert results[1][2] == "has=four days (got kind=answer)"


def test_an_app_that_crashes_has_failed_acceptance(uat):
    def broken(who, says):
        raise KeyError("ticket")
    results = uat.run(uat.parse(table(("U-01", "FR-02", "Rayan", "hi", "kind=status", "auto"))), broken, real=False)
    assert results[0][1:] == ("FAIL", "the app raised KeyError")


def test_real_rows_wait_for_the_real_model_and_person_rows_always_wait_for_a_person(uat):
    rows = uat.parse(table(("U-01", "AC-1", "Rayan", "hi", "has=x", "real"), ("U-02", "NFR-05", "Yara", "try it", "works", "person")))
    seen = []

    def app(who, says):
        seen.append(says)
        return reply(text="x")
    offline = uat.run(rows, app, real=False)
    assert [(res, why) for _, res, why in offline] == [("SKIP", "needs the real model"), ("SKIP", "a person runs this row")] and seen == []
    online = uat.run(rows, app, real=True)
    assert [res for _, res, _ in online] == ["PASS", "SKIP"] and seen == ["hi"]


def test_real_mode_means_not_the_mock_and_a_real_key(uat, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "http://127.0.0.1:9015")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock")
    assert not uat.is_real()
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    assert not uat.is_real()                                                 # a real key but a local base URL is still the mock
    monkeypatch.delenv("ANTHROPIC_BASE_URL")
    assert uat.is_real()
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock")
    assert not uat.is_real()


def test_the_verdict_never_says_accepted_unless_every_row_passed_and_even_then_leaves_the_signing_to_people(uat, capsys):
    def verdict(*results):
        rows = [(SimpleNamespace(id=f"U-0{i}", criterion="FR-01", how="auto"), res, "") for i, res in enumerate(results, 1)]
        uat.report(rows)
        return capsys.readouterr().out.splitlines()[-1]
    assert verdict("PASS", "FAIL", "SKIP").startswith("verdict: NOT ACCEPTED")
    assert verdict("PASS", "SKIP").startswith("verdict: NOT READY TO SIGN")
    last = verdict("PASS", "PASS")
    assert last.startswith("verdict: ALL ROWS PASSED") and "people sign" in last


# ------------------------------------------------------------------ the command line

APP = '''from types import SimpleNamespace
def app(user, text):
    return SimpleNamespace(kind="answer", text="Three days a week. [remote-work#0]", handoff=None)
'''


def run_cli(tmp_path, script_text, *args, **env):
    (tmp_path / "fake_app.py").write_text(APP, encoding="utf-8")
    (tmp_path / "s.md").write_text(script_text, encoding="utf-8")
    full = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_BASE_URL"} | {"PYTHONPATH": str(tmp_path), "ANTHROPIC_API_KEY": "mock", **env}
    return subprocess.run([sys.executable, str(LABS / "uat_runner.py"), str(tmp_path / "s.md"), "--app", "fake_app:app", *args], cwd=tmp_path, env=full, capture_output=True, text=True)


ALL_PASS = table(("U-01", "FR-01", "Rayan", "hi", "kind=answer; has=three days; has=[remote-work", "auto"))
ONE_WAITING = ALL_PASS.replace("\n## Next", "| U-02 | NFR-05 | Yara | try it | works | person |\n\n## Next")


def test_exit_codes_a_pass_a_fail_and_the_strict_flag(tmp_path):
    assert run_cli(tmp_path, ALL_PASS).returncode == 0
    assert run_cli(tmp_path, ALL_PASS.replace("three days", "four days")).returncode == 1
    assert run_cli(tmp_path, ONE_WAITING).returncode == 0                                # something waits for a person: not a failure...
    strict = run_cli(tmp_path, ONE_WAITING, "--strict")
    assert strict.returncode == 1 and "NOT READY TO SIGN" in strict.stdout                # ...unless you ask for strict


def test_the_evidence_file_records_the_mode_the_rows_and_a_date(tmp_path):
    out = tmp_path / "evidence.json"
    assert run_cli(tmp_path, ONE_WAITING, "--evidence", str(out)).returncode == 0
    data = json.loads(out.read_text())
    assert data["mode"] == "offline" and re.fullmatch(r"\d{4}-\d{2}-\d{2}", data["date"])
    assert [(r[0], r[1]) for r in data["rows"]] == [("U-01", "PASS"), ("U-02", "SKIP")]


def test_the_thin_slice_on_the_mock_passes_what_code_decides_and_fails_the_features_it_lacks(server):
    """The lab's own result: this is Lab 7.2's thin slice, not Najm Desk v1, and the script says so by failing U-09 and U-10."""
    env = {**os.environ, "ANTHROPIC_BASE_URL": server, "ANTHROPIC_API_KEY": "mock"}
    r = subprocess.run([sys.executable, "-I", str(LABS / "uat_runner.py")], cwd=KIT, env=env, capture_output=True, text=True)
    rows = {m.group(1): m.group(2) for m in re.finditer(r"^(U-\d\d)\s.*?\s(PASS|FAIL|SKIP)\b", r.stdout, re.M)}
    assert rows == {"U-01": "SKIP", **{f"U-0{i}": "PASS" for i in range(2, 9)}, "U-09": "FAIL", "U-10": "FAIL",
                    "U-11": "SKIP", "U-12": "SKIP", "U-13": "SKIP", "U-14": "SKIP"}
    assert r.returncode == 1 and "7 passed, 2 failed, 5 not run: U-01, U-11, U-12, U-13, U-14" in r.stdout
    assert "verdict: NOT ACCEPTED" in r.stdout and "(got kind=answer)" in r.stdout


# ------------------------------------------------------------------ the handover documents

def test_every_acceptance_criterion_and_requirement_in_the_script_exists_in_the_spec_and_every_ac_is_covered(uat, script):
    spec = SPEC.read_text(encoding="utf-8")
    defined = set(re.findall(r"\*\*((?:FR|GR|NFR|AC)-\d+)\*\*", spec)) | set(re.findall(r"^- \*\*(AC-\d)\*\*", spec, re.M))
    used = {tok for r in uat.parse(script) for tok in r.criterion.split()}
    assert used - defined == set(), f"ids in the script that the spec does not define: {sorted(used - defined)}"
    assert {"AC-1", "AC-2", "AC-3", "AC-4", "AC-5"} <= used                      # the script is derived from ALL the acceptance criteria


def test_no_one_has_signed_anything_in_the_reference_documents(script):
    sign = script.split("## Sign-off")[1]
    rows = [r for r in sign.splitlines() if r.startswith("| ") and not r.startswith("| Name") and not r.startswith("|---")]
    assert [r.split("|")[1].strip() for r in rows] == ["Hind", "Yara", "Noura", "Layla", "Fahad"]
    assert all(r.split("|")[-3].strip() == "TODO" and r.split("|")[-2].strip() == "TODO" for r in rows)
    check = (HANDOVER / "handover_checklist.md").read_text(encoding="utf-8")
    assert "- [x]" not in check.lower() and check.count("- [ ]") >= 20


def test_every_checklist_item_names_an_owner_and_the_evidence_that_proves_it():
    items = [line for line in (HANDOVER / "handover_checklist.md").read_text(encoding="utf-8").splitlines() if line.startswith("- [ ]")]
    assert items
    for line in items:
        owner = re.search(r"Owner: (\w+)", line)
        assert owner and owner.group(1) in CAST, line
        assert re.search(r"Evidence: \S", line), line


def test_the_runbook_index_lists_every_runbook_that_exists_and_no_file_that_does_not():
    index = (HANDOVER / "runbook_index.md").read_text(encoding="utf-8")
    linked = re.findall(r"\]\(\.\./runbooks/([\w.]+)\)", index)
    assert len(linked) == len(set(linked))
    assert sorted(linked) == sorted(p.name for p in RUNBOOKS.glob("*.md") if p.name != "_template.md")
    for name in linked:
        assert (RUNBOOKS / name).exists()


def test_the_index_and_each_runbook_name_the_same_owners():
    index = (HANDOVER / "runbook_index.md").read_text(encoding="utf-8")
    for row in (r for r in index.splitlines() if "](../runbooks/" in r):
        name = re.search(r"runbooks/([\w.]+)\)", row).group(1)
        cells = [c.strip() for c in row.strip("|").split("|")]
        owner_in_index = set(re.findall(r"[A-Z][a-z]+", cells[-2])) & CAST
        line = next(l for l in (RUNBOOKS / name).read_text(encoding="utf-8").splitlines() if l.startswith("Owner:"))
        assert owner_in_index == set(re.findall(r"[A-Z][a-z]+", line.split("Last drilled")[0])) & CAST, (name, cells)


def test_every_runbook_has_the_same_eight_sections_in_order():
    wanted = ["Trigger", "First five minutes", "Diagnose", "Fix or mitigate", "Tell people", "Recover and resume", "After"]
    for path in sorted(RUNBOOKS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        assert re.findall(r"^## (.+?)\s*$", text, re.M) == wanted, path.name
        assert re.search(r"^Owner: .+Last drilled: TODO date", text, re.M), path.name      # drilled dates are filled in by people, after a drill


def test_every_incident_runbook_starts_with_the_kill_switch_before_diagnosis():
    for path in RUNBOOKS.glob("*.md"):
        if path.name in {"_template.md", "kill_switch.md", "change_prompt_or_model.md", "monthly_eval_refresh.md"}:
            continue
        first = re.search(r"## First five minutes\n(.*?)\n## ", path.read_text(encoding="utf-8"), re.S).group(1)
        assert "kill_switch.md" in first, path.name


def test_every_runbook_reference_to_another_runbook_or_a_lab_script_points_at_something_real():
    for path in RUNBOOKS.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        for name in re.findall(r"`([\w]+\.md)`", text):
            assert (RUNBOOKS / name).exists(), (path.name, name)
        for script in re.findall(r"labs/m15/(\w+\.py)", text):
            assert (LABS / script).exists(), (path.name, script)


def test_the_user_guide_promises_nothing_the_spec_puts_out_of_scope():
    guide = (HANDOVER / "user_guide.md").read_text(encoding="utf-8")
    cannot = guide.split("## What it can and cannot do")[1].split("## How to ask")[0]
    for promise in ("priority", "Unlock, reset or change an account", "Promise a response time"):
        assert promise in cannot
    assert "TODO" in guide.split("## Hours and contacts")[1]                       # phone numbers are the customer's to fill in
    for needed in ("hotline", "rating", "reference id", "[vpn#0]"):
        assert needed in guide


def test_every_reference_file_that_hands_work_to_a_person_leaves_the_numbers_to_the_customer():
    for name in ("handover_checklist.md", "runbook_index.md", "user_guide.md"):
        assert "TODO" in (HANDOVER / name).read_text(encoding="utf-8"), name
