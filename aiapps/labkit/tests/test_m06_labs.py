"""Tests for the Module 6 lab files (labs/m06) and the lab data they use (labkit/data/m06_*).

Nothing here calls a model, offline or real: discovery and specification work is done by people, and these scripts only
check what code can check (quotes are real, ids exist, untestable words are flagged, every scenario traces to a requirement).
They also keep the shipped data honest: the transcripts, the answer key, the worked spec and the eval seed must agree."""
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

KIT = Path(__file__).resolve().parents[1]
LABS = KIT / "labs" / "m06"
DATA = KIT / "labkit" / "data"


@pytest.fixture
def lab(monkeypatch):
    """Import the lab modules fresh, by plain name, as when you run them from the command line."""
    monkeypatch.syspath_prepend(str(LABS))
    for name in ("spec_lint", "check_notes"):
        sys.modules.pop(name, None)
    import check_notes, spec_lint          # noqa: E401,E402
    yield type("Lab", (), {"spec_lint": spec_lint, "check_notes": check_notes})
    for name in ("spec_lint", "check_notes"):
        sys.modules.pop(name, None)


def run(script: str, *args) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(LABS / script), *map(str, args)], capture_output=True, text=True, timeout=60)


def seed_rows() -> list[dict]:
    return [json.loads(x) for x in (DATA / "m06_eval_seed.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]


WORKED = (DATA / "m06_spec_worked.md").read_text(encoding="utf-8")


def turns_of(name: str) -> dict[str, str]:
    return {m.group(1): m.group(2) for x in (DATA / name).read_text(encoding="utf-8").splitlines() if (m := re.match(r"^\[([HYA]-\d+)\]\s*(.*)$", x))}


# ---------------------------------------------------------------- the source files

def test_lab_files_start_with_their_own_path_comment():
    for f in sorted(LABS.glob("*.py")):
        assert f.read_text(encoding="utf-8").splitlines()[0] == f"# labs/m06/{f.name}"


@pytest.mark.parametrize("name, prefix, speaker", [("m06_interview_hind.md", "H", "Hind"), ("m06_interview_yara.md", "Y", "Yara")])
def test_interviews_have_sequential_ids_and_alternating_speakers(name, prefix, speaker):
    turns = turns_of(name)
    assert list(turns) == [f"{prefix}-{i:02d}" for i in range(1, len(turns) + 1)]
    for i, text in enumerate(turns.values(), 1):
        assert text.startswith("**You:**" if i % 2 else f"**{speaker}:**"), f"turn {i} has the wrong speaker"


def test_as_is_notes_have_sequential_ids():
    turns = turns_of("m06_as_is_process.md")
    assert list(turns) == [f"A-{i:02d}" for i in range(1, len(turns) + 1)]


def test_the_as_is_numbers_add_up():
    t = turns_of("m06_as_is_process.md")
    assert sum(map(int, re.findall(r"(\d+)%", t["A-01"]))) == 100                       # channel shares
    cats = [int(n) for n in re.findall(r"\s(\d+)(?:;|\.)", t["A-03"].replace("Total 1,800.", ""))]
    assert sum(cats) == 1800 and 450 in cats                                             # categories add to the 1,800 baseline
    access = [int(n) for n in re.findall(r"about (\d+)", t["A-04"])]
    assert sum(access) == 450                                                            # inside the access slice
    assert (22, 10, 8) == tuple(int(n) for n in re.findall(r"(\d+) (?:were|was)", t["A-05"])[:3]) and 22 + 10 + 8 == 40


def test_the_contradictions_are_really_in_the_sources():
    h, y, a = turns_of("m06_interview_hind.md"), turns_of("m06_interview_yara.md"), turns_of("m06_as_is_process.md")
    assert "Half of them were passwords and access" in h["H-02"] and "a quarter of our tickets, not half" in y["Y-14"] and "access, password and MFA 450" in a["A-03"]
    assert "Ninety percent" in h["H-16"] and "a third in Arabic" in y["Y-22"]
    assert "Any agent can unlock" in h["H-12"] and "calling her manager" in y["Y-10"]
    assert "routed automatically" in h["H-16"] and "duty agent reads every new ticket" in y["Y-06"]
    assert "If they don't open a ticket" in h["H-26"] and "three working days" in y["Y-32"]
    assert "twenty-four hours" in h["H-28"] and "only P1" in y["Y-26"]


def test_the_key_cites_only_real_turns():
    known = set(turns_of("m06_interview_hind.md")) | set(turns_of("m06_interview_yara.md")) | set(turns_of("m06_as_is_process.md"))
    cited = set(re.findall(r"\b[HYA]-\d{2}\b", (DATA / "m06_discovery_key.md").read_text(encoding="utf-8")))
    assert cited and cited <= known, sorted(cited - known)


# ---------------------------------------------------------------- check_notes

NOTES_OK = '''- REQ-1 Identity is checked by a manager call-back. [Y-10 "Never a number she gives us."]
- **RISK-2** The old bot had no route to a person. [H-08 "no way to reach a person"]
- CON-3 Half versus a quarter. [H-02 "Half of them were passwords and access"] [A-03 "access, password and MFA 450"]
'''


def test_check_notes_accepts_real_quotes_ignoring_case_and_punctuation(lab):
    assert lab.check_notes.check(NOTES_OK, lab.check_notes.load_turns()) == []


def test_check_notes_catches_an_invented_quote_an_unknown_turn_and_a_missing_citation(lab):
    notes = '- REQ-1 x [Y-14 "we hate chatbots"]\n- RISK-2 x [Y-99 "anything"]\n- Q-3 nothing cited here\n- plain bullet, not an item\n'
    found = lab.check_notes.check(notes, lab.check_notes.load_turns())
    assert any("line 1" in f and "does not say" in f for f in found)
    assert any("line 2" in f and "no turn Y-99" in f for f in found)
    assert any("line 3" in f and "no citation" in f for f in found)
    assert len(found) == 3


def test_check_notes_holds_an_item_line_to_a_citation_with_or_without_a_bullet(lab):
    notes = 'REQ-1 no bullet, no citation\n**RISK-2** bold, no bullet, no citation\n* CON-3 star bullet, no citation\nQ-4 fine [H-04 "Seventy percent"]\n'
    found = lab.check_notes.check(notes, lab.check_notes.load_turns())
    assert [f.split(":")[0] for f in found] == ["line 1", "line 2", "line 3"] and all("no citation" in f for f in found)


def test_check_notes_rejects_a_one_word_quote_and_a_quote_cut_from_inside_a_word(lab):
    notes = '- REQ-1 x [Y-10 "the"]\n- REQ-2 x [Y-10 "all back"]\n- REQ-3 x [Y-10 "call-back"]\n'      # "all back" only occurs inside "call back"
    found = lab.check_notes.check(notes, lab.check_notes.load_turns())
    assert len(found) == 2 and all("two or more whole words" in f for f in found) and "line 3" not in " ".join(found)


def test_check_notes_cli_exit_codes_and_the_uncited_list(tmp_path):
    good, bad = tmp_path / "good.md", tmp_path / "bad.md"
    good.write_text(NOTES_OK, encoding="utf-8")
    bad.write_text('- REQ-1 x [H-02 "nothing like this"]\n', encoding="utf-8")
    ok, no = run("check_notes.py", good), run("check_notes.py", bad)
    assert ok.returncode == 0 and "every citation checks out" in ok.stdout
    assert "H-04" in ok.stdout and "Y-10" not in ok.stdout.split("read again:")[1]       # Y-10 was cited, H-04 was not
    assert no.returncode == 1 and "H-02 does not say" in no.stdout


# ---------------------------------------------------------------- spec_lint

SPEC = '''## Requirements
- **FR-01** [M] The reply is fast and easy to read.
- **FR-02** [M] Cite the policy id in brackets.
- **GR-01** [M] Never reveal a password.
- **NFR-01** [M] First words within 3 seconds at the 95th percentile.
A line that mentions FR-99 inside prose is not a definition.
'''


def row(i, *reqs):
    return {"id": i, "reqs": list(reqs)}


def test_requirements_are_bullets_that_open_with_an_id(lab):
    assert list(lab.spec_lint.requirements(SPEC)) == ["FR-01", "FR-02", "GR-01", "NFR-01"]


def test_untestable_words_are_flagged_with_the_requirement_id(lab):
    found = lab.spec_lint.lint(SPEC, [], skip=("FR", "GR", "NFR"))
    assert sorted(found) == sorted([
        "FR-01: vague word 'fast': give a number or a condition",
        "FR-01: vague word 'easy': give a number or a condition"])


def test_vague_words_are_whole_words_only(lab):
    spec = "- **FR-01** [M] Fasten the lid. Security: the 95th percentile. Easy-going is not here. etcetera.\n"
    assert lab.spec_lint.lint(spec, [], skip=("FR",)) == []


def test_every_requirement_needs_enough_cases_unless_skipped(lab):
    rows = [row("S1", "FR-01"), row("S2", "FR-01", "FR-02")]
    found = lab.spec_lint.lint(SPEC, rows, min_cases=2)
    assert "FR-02: 1 eval case(s), want at least 2" in found and "GR-01: 0 eval case(s), want at least 2" in found
    assert "NFR-01: 0 eval case(s), want at least 2" in found
    assert not any(f.startswith("FR-01:") and "eval case" in f for f in found)
    assert not any(f.startswith("NFR-01") for f in lab.spec_lint.lint(SPEC, rows, skip=("NFR",)))


def test_a_scenario_citing_an_undefined_requirement_is_an_orphan(lab):
    found = lab.spec_lint.lint(SPEC, [row("S9", "FR-77")], skip=("FR", "GR", "NFR"))
    assert found[-1] == "S9: cites FR-77, which the spec does not define" and len(found) == 3


def test_a_clean_spec_prints_clean_and_exits_zero(tmp_path):
    spec, seed = tmp_path / "spec.md", tmp_path / "seed.jsonl"
    spec.write_text("- **FR-01** [M] Cite the policy id in brackets.\n", encoding="utf-8")
    seed.write_text(json.dumps(row("S1", "FR-01")) + "\n" + json.dumps(row("S2", "FR-01")) + "\n", encoding="utf-8")
    done = run("spec_lint.py", spec, seed)
    assert done.returncode == 0 and done.stdout.splitlines() == ["clean", "0 finding(s)"]


def test_findings_exit_one_and_min_cases_can_be_lowered(tmp_path):
    spec, seed = tmp_path / "spec.md", tmp_path / "seed.jsonl"
    spec.write_text("- **FR-01** [M] Cite the policy id in brackets.\n", encoding="utf-8")
    seed.write_text(json.dumps(row("S1", "FR-01")) + "\n", encoding="utf-8")
    assert run("spec_lint.py", spec, seed).returncode == 1
    assert run("spec_lint.py", spec, seed, "--min-cases", "1").returncode == 0


# ---------------------------------------------------------------- the shipped spec and eval seed agree

def test_the_worked_spec_has_ten_sections_and_the_expected_requirements(lab):
    assert re.findall(r"^### (\d+)\. ", WORKED, re.M) == [str(i) for i in range(1, 11)]
    ids = list(lab.spec_lint.requirements(WORKED))
    assert [i for i in ids if i.startswith("FR")] == [f"FR-0{n}" for n in range(1, 9)]
    assert [i for i in ids if i.startswith("GR")] == [f"GR-0{n}" for n in range(1, 7)]
    assert [i for i in ids if i.startswith("NFR")] == [f"NFR-0{n}" for n in range(1, 7)]
    assert re.findall(r"\*\*AC-(\d)\*\*", WORKED) == list("12345")


def test_the_worked_spec_passes_its_own_vagueness_check(lab):
    reqs = lab.spec_lint.requirements(WORKED)
    assert not [r for r, text in reqs.items() if lab.spec_lint.VAGUE.search(text)]
    assert all(re.search(r"\d", reqs[i]) for i in ("NFR-01", "NFR-02", "NFR-03", "NFR-06"))     # the measurable ones carry a number


def test_the_eval_seed_is_valid_and_traces_to_the_worked_spec(lab):
    rows, defined = seed_rows(), set(lab.spec_lint.requirements(WORKED))
    assert len(rows) == 12 and len({r["id"] for r in rows}) == 12
    for r in rows:
        assert {"id", "reqs", "kind", "lang", "context", "user", "expect", "checks"} <= set(r), r["id"]
        assert r["reqs"] and set(r["reqs"]) <= defined and r["checks"] and r["user"].strip()
    kinds = {r["kind"] for r in rows}
    assert {"in_scope", "adversarial", "out_of_scope"} <= kinds
    assert any(r["lang"] == "ar" and re.search(r"[؀-ۿ]", r["user"]) for r in rows)


def test_the_starter_seed_covers_every_functional_and_guardrail_requirement_once_but_not_twice(lab):
    rows = seed_rows()
    assert lab.spec_lint.lint(WORKED, rows, skip=("NFR",), min_cases=1) == []                 # traceable and complete at one case each
    thin = lab.spec_lint.lint(WORKED, rows, skip=("NFR",))                                    # the exercise: grow it to two or more
    assert thin and all("eval case" in f for f in thin)


def test_the_acceptance_criteria_cite_real_requirements_and_real_data(lab):
    defined = set(lab.spec_lint.requirements(WORKED))
    for line in re.findall(r"^- \*\*AC-\d\*\*.*$", WORKED, re.M):
        cited = set(re.findall(r"\b(?:FR|GR|NFR)-\d+\b", line))
        assert cited and cited <= defined, line
    tickets = json.loads((DATA / "tickets.json").read_text(encoding="utf-8"))
    assert "4474" in tickets and "4471" in tickets                                              # tickets the seed and AC-2 mention
    policies = {p.stem for p in (DATA / "policies").glob("*.md")}
    assert {"vpn", "remote-work", "laptop-requests"} <= policies                                # document ids the spec cites


def test_tools_named_in_requirements_and_seed_tags_exist_in_the_permissions_matrix():
    matrix = set(re.findall(r"^\| `(\w+)` \|", WORKED, re.M))
    assert matrix == {"search_policies", "get_ticket_status", "draft_ticket", "create_ticket", "request_unlock", "hand_off"}
    requirements = WORKED.split("### 5.")[1].split("### 6.")[0]
    assert set(re.findall(r"`(\w+)`", requirements)) == matrix                                    # every tool is used by a requirement
    tagged = {t.split(":", 1)[1] for r in seed_rows() for t in r["checks"] if t.startswith(("tool:", "no_tool:"))}
    assert tagged - {"*"} <= matrix, tagged
