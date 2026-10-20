"""Tests for the Module 13.2 lab (labs/m13/pack_check.py and labs/m13/templates/).

No model is involved. The checker verifies FORM and DRIFT: that every document exists with its sections, nothing is left as TODO, every
required person has signed, and the tool list on the system card equals the one the gate enforces. It cannot tell whether what is written is
good, true of the real system, or enough for a regulator: that is a person's review."""
import re
import subprocess
import sys
from pathlib import Path

import pytest

KIT = Path(__file__).resolve().parents[1]
LABS = KIT / "labs" / "m13"
TEMPLATES = LABS / "templates"


@pytest.fixture
def pc(monkeypatch):
    monkeypatch.syspath_prepend(str(LABS))
    for name in ("guardrails", "pack_check"):
        sys.modules.pop(name, None)
    import guardrails                                           # noqa: E402
    import pack_check                                           # noqa: E402
    yield pack_check, guardrails
    for name in ("guardrails", "pack_check"):
        sys.modules.pop(name, None)


def finish(tmp_path, tools):
    """Turn the blank templates into a finished pack: fill every TODO, list the tools, sign every row."""
    for src in TEMPLATES.glob("*.md"):
        text = src.read_text(encoding="utf-8")
        if src.name == "system_card.md":
            text = text.replace("| `TODO` | TODO | TODO | TODO | TODO |", "\n".join(f"| `{t}` | read | x | none | 10 |" for t in tools))
        text = text.replace("TODO", "written")
        text = re.sub(r"\| written \| written \|$", "| approved | 2026-11-02 |", text, flags=re.M)
        (tmp_path / src.name).write_text(text, encoding="utf-8")
    return tmp_path


def test_the_blank_templates_pass_the_structure_check_and_fail_the_strict_one(pc):
    check, _ = pc[0].check, pc[1]
    assert check(TEMPLATES, structure_only=True) == []
    strict = check(TEMPLATES)
    assert any("still has a TODO" in p for p in strict) and any("has not approved" in p for p in strict)


def test_a_finished_pack_passes(pc, tmp_path):
    pack_check, guardrails = pc
    assert pack_check.check(finish(tmp_path, list(guardrails.NAJM_DESK_V1))) == []


def test_every_template_has_the_sections_and_the_signers_the_checker_requires(pc):
    for name, (wanted, signers) in pc[0].REQUIRED.items():
        text = (TEMPLATES / name).read_text(encoding="utf-8")
        assert set(wanted) <= set(pc[0].sections(text)), name
        for who in signers:
            assert re.search(rf"^\|\s*{who}\s*\|", pc[0].sections(text)["Sign-off"], re.M), (name, who)
    assert sorted(p.name for p in TEMPLATES.glob("*.md")) == sorted(pc[0].REQUIRED)


def test_the_four_risk_owners_each_sign_something(pc):
    signers = {who for _, people in pc[0].REQUIRED.values() for who in people}
    assert signers == {"Layla", "Noura", "Hamad", "Sara"}


def test_a_missing_file_a_missing_section_and_an_empty_section_are_reported(pc, tmp_path):
    pack = finish(tmp_path, list(pc[1].NAJM_DESK_V1))
    (pack / "dpia_trigger.md").unlink()
    text = (pack / "change_policy.md").read_text(encoding="utf-8")
    (pack / "change_policy.md").write_text(text.replace("## Rollout and rollback", "## Rollout"), encoding="utf-8")
    text = (pack / "risk_register.md").read_text(encoding="utf-8")
    (pack / "risk_register.md").write_text(re.sub(r"## Risks\n.*?\n## Sign-off", "## Risks\n\n## Sign-off", text, flags=re.S), encoding="utf-8")
    problems = pc[0].check(pack)
    assert "dpia_trigger.md: missing" in problems
    assert "change_policy.md: no section 'Rollout and rollback'" in problems
    assert "risk_register.md: section 'Risks' is empty" in problems


def test_a_todo_left_in_a_section_is_reported(pc, tmp_path):
    pack = finish(tmp_path, list(pc[1].NAJM_DESK_V1))
    path = pack / "vendor_assessment.md"
    path.write_text(path.read_text(encoding="utf-8").replace("## Continuity and exit\n", "## Continuity and exit\nTODO\n"), encoding="utf-8")
    assert pc[0].check(pack) == ["vendor_assessment.md: section 'Continuity and exit' still has a TODO"]


@pytest.mark.parametrize("row", ["| Sara | Data Protection Officer | pending | 2026-11-02 |", "| Sara | Data Protection Officer | approved | soon |",
                                 "| Sara | Data Protection Officer | rejected | 2026-11-02 |"])
def test_a_signature_needs_approval_and_a_date(pc, tmp_path, row):
    pack = finish(tmp_path, list(pc[1].NAJM_DESK_V1))
    path = pack / "dpia_trigger.md"
    path.write_text(re.sub(r"^\| Sara .*$", row, path.read_text(encoding="utf-8"), flags=re.M), encoding="utf-8")
    assert pc[0].check(pack) == ["dpia_trigger.md: Sara has not approved"]


def test_a_removed_signer_row_is_caught(pc, tmp_path):
    pack = finish(tmp_path, list(pc[1].NAJM_DESK_V1))
    path = pack / "risk_register.md"
    path.write_text(re.sub(r"^\| Hamad .*\n", "", path.read_text(encoding="utf-8"), flags=re.M), encoding="utf-8")
    assert pc[0].check(pack) == ["risk_register.md: Hamad has not approved"]


def test_the_system_card_must_match_the_tools_the_gate_enforces(pc, tmp_path):
    rules = list(pc[1].NAJM_DESK_V1)
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    extra = pc[0].check(finish(tmp_path / "a", rules + ["send_email"]))
    assert extra == ["system_card.md: tools differ from guardrails.py: ['send_email']"]
    short = pc[0].check(finish(tmp_path / "b", [t for t in rules if t != "request_unlock"]))
    assert short == ["system_card.md: tools differ from guardrails.py: ['request_unlock']"]


def test_the_script_exit_codes(pc, tmp_path):
    def run(*args):
        return subprocess.run([sys.executable, str(LABS / "pack_check.py"), *args], capture_output=True, text=True, cwd=str(KIT), timeout=60)
    assert run(str(TEMPLATES), "--structure").returncode == 0
    blank = run(str(TEMPLATES))
    assert blank.returncode == 1 and "has not approved" in blank.stdout
    done = run(str(finish(tmp_path, list(pc[1].NAJM_DESK_V1))))
    assert done.returncode == 0 and "nothing to fix" in done.stdout
