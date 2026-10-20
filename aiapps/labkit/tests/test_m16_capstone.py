"""Tests for the Module 16.1 lab (labs/m16/capstone_audit.py and labkit/data/m16_checklist.json).

No model is involved. The audit checks EXISTENCE and LINKS: every deliverable on the checklist is present and not empty, nothing is a leftover
TODO in strict mode, the full governance pack passes Lab 13.2's checker at tier 3, every requirement id the specification defines is cited
downstream, and nothing cites an id the specification lacks. It cannot tell whether the evidence is good or true, and it never signs for anyone."""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

KIT = Path(__file__).resolve().parents[1]
LAB = KIT / "labs" / "m16" / "capstone_audit.py"
CHECKLIST = json.loads((KIT / "labkit" / "data" / "m16_checklist.json").read_text(encoding="utf-8"))
SPEC = KIT / "labkit" / "data" / "m06_spec_worked.md"
SEED = KIT / "labkit" / "data" / "m06_eval_seed.jsonl"
UAT = KIT / "labs" / "m15" / "handover" / "uat_script.md"
TEMPLATES = KIT / "labs" / "m13" / "templates"


@pytest.fixture(scope="module")
def audit():
    """Import the lab by path (it puts labs/m13 on sys.path to reuse pack_check); restore sys.path and sys.modules afterwards."""
    saved = list(sys.path)
    for name in ("pack_check", "guardrails"):
        sys.modules.pop(name, None)
    spec = importlib.util.spec_from_file_location("m16_capstone_audit", LAB)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    yield mod
    sys.path[:] = saved
    for name in ("pack_check", "guardrails"):
        sys.modules.pop(name, None)


def items(tier):
    """Every checklist item up to `tier` as (pattern, count)."""
    return [(i, 1) if isinstance(i, str) else tuple(i) for by in CHECKLIST.values() for t, its in by.items() if int(t) <= tier for i in its]


def finish(text, tools):
    """A blank governance template made into a finished one: TODO filled, the tool list written, every signature row approved."""
    text = text.replace("| `TODO` | TODO | TODO | TODO | TODO |", "\n".join(f"| `{t}` | read | x | none | 10 |" for t in tools))
    text = text.replace("TODO", "written")
    return re.sub(r"\| written \| written \|$", "| approved | 2026-11-02 |", text, flags=re.M)


def make_repo(root, tier, audit, finished=False):
    """A repository with everything the checklist asks for up to `tier`, and a cost sheet that cites every requirement id."""
    for pattern, count in items(tier):
        names = [pattern.replace("*", str(n)) for n in range(1, count + 1)] if "*" in pattern else [pattern]
        for name in names:
            (root / name).parent.mkdir(parents=True, exist_ok=True)
            (root / name).write_text("written by the learner\n", encoding="utf-8")
    (root / "docs" / "najm-desk-spec.md").write_text(SPEC.read_text(encoding="utf-8"), encoding="utf-8")
    ids = sorted(set(re.findall(r"^- \*\*((?:FR|GR|NFR|AC)-\d+)\*\*", SPEC.read_text(encoding="utf-8"), re.M)))
    (root / "docs" / "cost-and-reliability.md").write_text("Requirements covered: " + " ".join(ids) + "\n", encoding="utf-8")
    if tier >= 3:                                              # the whole pack, from the Module 13 templates
        sys.path.insert(0, str(KIT / "labs" / "m13"))
        try:
            import guardrails
            tools = list(guardrails.NAJM_DESK_V1)
        finally:
            sys.path.pop(0)
        for src in TEMPLATES.glob("*.md"):
            text = src.read_text(encoding="utf-8")
            (root / "docs" / "governance" / src.name).write_text(finish(text, tools) if finished else text, encoding="utf-8")
    return root


def problems(audit, repo, tier=1, strict=False):
    return sum(map(len, audit.exists(repo, tier, strict).values())) + sum(map(len, audit.linked(repo)))


def test_the_checklist_is_well_formed():
    names = list(CHECKLIST)
    assert [n.split()[0] for n in names] == [f"M{i}" for i in range(1, 9)]          # M1 to M8, in order
    paths = []
    for by_tier in CHECKLIST.values():
        assert "1" in by_tier and set(by_tier) <= {"1", "2", "3"}                    # every milestone has a core path
        for item in (i for its in by_tier.values() for i in its):
            pattern, count = (item, 1) if isinstance(item, str) else item
            assert count >= 1 and not pattern.startswith("/") and ".." not in pattern
            paths.append(pattern)
    assert len(paths) == len(set(paths))


def test_the_tiers_only_add_work():
    assert len(items(1)) < len(items(2)) < len(items(3))
    assert {p for p, _ in items(2)} >= {p for p, _ in items(1)}


def test_the_governance_documents_on_the_checklist_are_the_seven_that_pack_check_requires(audit):
    named = {Path(p).name for p, _ in items(3) if p.startswith("docs/governance/")}
    assert named == set(audit.pack_check.REQUIRED)
    assert {Path(p).name for p, _ in items(1) if p.startswith("docs/governance/")} < named          # the core path asks for two of them


@pytest.mark.parametrize("tier", [1, 2, 3])
def test_a_complete_repository_passes_its_tier(audit, tmp_path, tier):
    repo = make_repo(tmp_path, tier, audit)
    assert audit.main([str(repo), "--tier", str(tier)]) == 0


def test_a_repository_built_for_a_smaller_tier_fails_a_larger_one(audit, tmp_path):
    one, two = make_repo(tmp_path / "one", 1, audit), make_repo(tmp_path / "two", 2, audit)
    assert problems(audit, one, 1) == 0 and problems(audit, one, 2) > 0 and problems(audit, one, 3) > 0
    assert problems(audit, two, 2) == 0 and problems(audit, two, 3) > 0


def test_a_larger_repository_still_passes_a_smaller_tier(audit, tmp_path):
    assert problems(audit, make_repo(tmp_path, 3, audit), 1) == 0


def test_a_missing_file_an_empty_file_and_a_short_glob_are_each_named(audit, tmp_path):
    repo = make_repo(tmp_path, 1, audit)
    (repo / "docs" / "proposal.md").unlink()
    (repo / "docs" / "rollout-plan.md").write_text("", encoding="utf-8")
    (repo / "docs" / "adr" / "3.md").unlink()
    said = [p for ps in audit.exists(repo, 1, False).values() for p in ps]
    assert "docs/proposal.md: 0 found, 1 needed" in said
    assert "docs/rollout-plan.md: an empty file" in said
    assert "docs/adr/*.md: 2 found, 3 needed" in said
    assert audit.main([str(repo)]) == 1


def test_strict_mode_turns_a_leftover_todo_into_a_problem(audit, tmp_path):
    repo = make_repo(tmp_path, 1, audit)
    (repo / "docs" / "proposal.md").write_text("Scope: TODO\n", encoding="utf-8")
    assert problems(audit, repo, 1, strict=False) == 0 and problems(audit, repo, 1, strict=True) == 1


def test_strict_tier_3_wants_a_finished_signed_pack_and_accepts_one(audit, tmp_path):
    blank = make_repo(tmp_path / "blank", 3, audit)                                  # the unsigned templates: fine as structure only
    assert audit.main([str(blank), "--tier", "3"]) == 0
    assert audit.main([str(blank), "--tier", "3", "--strict"]) == 1
    done = make_repo(tmp_path / "done", 3, audit, finished=True)
    assert audit.main([str(done), "--tier", "3", "--strict"]) == 0
    vendor = done / "docs" / "governance" / "vendor_assessment.md"           # no TODO anywhere, but Hamad has not signed
    vendor.write_text(re.sub(r"(\| Hamad[^\n]*\|) approved ", r"\1 pending ", vendor.read_text(encoding="utf-8")), encoding="utf-8")
    assert problems(audit, done, 3, strict=True) == 0                          # the existence check cannot see it
    assert audit.main([str(done), "--tier", "3", "--strict"]) == 1             # Lab 13.2's checker can
    assert audit.main([str(done), "--tier", "1", "--strict"]) == 0             # and below tier 3 the pack is not required in full


def test_tier_3_checks_the_pack_structure_even_when_not_strict(audit, tmp_path):
    repo = make_repo(tmp_path, 3, audit)
    card = repo / "docs" / "governance" / "system_card.md"
    card.write_text(card.read_text(encoding="utf-8").replace("## Known limits", "## Limits"), encoding="utf-8")
    assert problems(audit, repo, 3) == 0
    assert audit.main([str(repo), "--tier", "3"]) == 1


def test_linked_on_the_courses_own_spec_seed_and_uat_script_finds_the_requirements_nothing_covers(audit, tmp_path):
    for src, dst in ((SPEC, "docs/najm-desk-spec.md"), (SEED, "evals/seed.jsonl"), (UAT, "docs/handover/uat_script.md")):
        (tmp_path / dst).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / dst).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    untraced, orphans = audit.linked(tmp_path)
    assert untraced == ["NFR-01", "NFR-03", "NFR-04", "NFR-06"]       # a test, a retention job, the audit log and the cost sheet are still to write
    assert orphans == []


def test_linked_catches_an_orphan_and_ignores_the_spec_citing_itself(audit, tmp_path):
    repo = make_repo(tmp_path, 1, audit)
    assert audit.linked(repo) == ([], [])
    (repo / "docs" / "architecture.md").write_text("The cache serves FR-99 and NFR-07.\n", encoding="utf-8")
    assert audit.linked(repo) == ([], ["FR-99", "NFR-07"])
    (repo / "docs" / "cost-and-reliability.md").write_text("only NFR-01\n", encoding="utf-8")
    untraced, _ = audit.linked(repo)
    assert "GR-03" in untraced and "NFR-01" not in untraced          # AC lines in the spec itself cite GR-03, which does not count


def test_without_a_spec_there_is_nothing_to_link_but_the_checklist_still_complains(audit, tmp_path):
    repo = make_repo(tmp_path, 1, audit)
    (repo / "docs" / "najm-desk-spec.md").unlink()
    assert audit.linked(repo) == ([], [])
    assert audit.main([str(repo)]) == 1


def test_the_command_line_reports_and_sets_the_exit_code(audit, tmp_path):
    repo = make_repo(tmp_path, 1, audit)
    run = lambda *a: subprocess.run([sys.executable, str(LAB), *a], capture_output=True, text=True, cwd=KIT)
    ok = run(str(repo))
    assert ok.returncode == 0 and "M8 runbook, handover and go-live" in ok.stdout and "0 problem(s)" in ok.stdout
    bad = run(str(tmp_path / "nowhere"))
    assert bad.returncode == 1 and "docs/agent-brief.md: 0 found, 1 needed" in bad.stdout
