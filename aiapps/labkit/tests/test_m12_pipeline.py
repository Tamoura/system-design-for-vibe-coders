"""Tests for the Module 12 pipeline (labs/m12): the dataset, the runner, the gate and the CI workflow.

The runner is exercised against the offline mock, and the gate against the committed baseline and against synthetic results.
They prove the PIPELINE works: that a regression is caught, that a broken eval is refused, that nothing silently passes.
They say nothing about whether a real model answers well: the mock follows keyword rules, a real model does not."""
import copy
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

KIT = Path(__file__).resolve().parents[1]
LABS = KIT / "labs" / "m12"
DATASET = KIT / "labkit" / "data" / "m12_eval_50.jsonl"
NAMES = ("adapters", "graders", "judge", "stats", "run_eval", "gate", "classify", "promptfile", "rag", "bm25", "agent_loop")


def cases():
    return [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]


@pytest.fixture(scope="module")
def m12(server):
    """The lab modules, imported fresh and pointed at the mock; the earlier labs they call are imported fresh too."""
    mp = pytest.MonkeyPatch()
    mp.setenv("ANTHROPIC_BASE_URL", server)
    mp.setenv("ANTHROPIC_API_KEY", "mock")
    for var in ("MODEL", "CLASSIFY_PROMPT", "PRICE_IN_PER_MTOK", "PRICE_OUT_PER_MTOK"):
        mp.delenv(var, raising=False)
    mp.syspath_prepend(str(LABS))
    for n in NAMES:
        sys.modules.pop(n, None)
    import adapters, gate, run_eval                              # noqa: E401
    yield SimpleNamespace(adapters=adapters, gate=gate, run_eval=run_eval, mp=mp)
    mp.undo()
    for n in NAMES:
        sys.modules.pop(n, None)


@pytest.fixture(scope="module")
def baseline():
    return json.loads((LABS / "baseline_mock.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def cfg():
    return json.loads((LABS / "gate.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def full_run(m12):
    return m12.run_eval.run_all(m12.run_eval.load_cases(), "mock")


TODAY = date(2026, 12, 1)


# ---------------------------------------------------------------- the dataset

def test_fifty_cases_with_unique_ids_and_known_agents_and_checks(m12):
    rows = cases()
    assert len(rows) == 50 and len({r["id"] for r in rows}) == 50
    assert Counter(r["agent"] for r in rows) == {"classifier": 18, "policy": 16, "ticket": 16}
    m12.run_eval.load_cases()                                     # raises on an unknown agent or check name


def test_every_category_has_cases_of_one_agent_and_critical_cases_exist(m12):
    by_cat = {}
    for r in cases():
        by_cat.setdefault(r["category"], []).append(r)
    assert all(len(v) >= 2 and len({r["agent"] for r in v}) == 1 for v in by_cat.values())
    assert sum(r["critical"] for r in cases()) >= 10
    assert all(r["lang"] == "ar" for r in cases() if r["real_only"]) and sum(r["real_only"] for r in cases()) == 4


def test_every_case_traces_to_a_requirement_in_the_worked_specification():
    spec = (KIT / "labkit" / "data" / "m06_spec_worked.md").read_text(encoding="utf-8")
    defined = set(re.findall(r"\*\*((?:FR|GR|NFR)-\d\d)\*\*", spec))
    for r in cases():
        assert r["reqs"] and set(r["reqs"]) <= defined, r["id"]       # a case with no requirement tests something nobody agreed
    covered = {q for r in cases() for q in r["reqs"]}
    assert {"FR-01", "FR-02", "FR-03", "FR-06", "FR-07", "GR-01", "GR-04", "GR-05", "GR-06"} <= covered
    assert not {"FR-04", "FR-05", "GR-03"} & covered              # no tool for these yet: the gap is known, not hidden


def test_the_dataset_holds_no_personal_data():
    text = DATASET.read_text(encoding="utf-8")
    assert not [e for e in re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text) if not e.endswith("@najm.example")]
    assert not re.search(r"\b\d{8,}\b", text)                      # no phone, card or id numbers


def test_the_prompt_in_use_leaks_no_eval_input_but_the_overfit_prompt_does(m12):
    m12.mp.setattr(m12.adapters, "CLASSIFY_PROMPT", "classify_v3")
    inputs = {r["input"].lower() for r in cases()}
    assert not inputs & m12.adapters.prompt_examples()
    m12.mp.setattr(m12.adapters, "CLASSIFY_PROMPT", "classify_v4_overfit")
    assert len(inputs & m12.adapters.prompt_examples()) == 2      # two eval tickets pasted into a prompt as examples
    m12.mp.setattr(m12.adapters, "CLASSIFY_PROMPT", "classify_v3")


# ---------------------------------------------------------------- the runner

def test_a_full_offline_run_has_the_documented_shape(full_run):
    r = full_run
    assert (r["n_run"], r["n_skipped"], r["n_errors"], r["mode"], r["leaks"]) == (46, 4, 0, "mock", [])
    assert set(r["versions"]) == {"model", "classify_prompt", "policy_prompt", "ticket_agent"}
    assert len(r["categories"]) == 13 and r["usage"]["tokens_in"] > 0 and r["usage"]["judge_tokens"] == 0
    assert r["usage"]["cost"] is None                              # no price given: the runner never invents one
    lo, hi = r["overall"]["ci"]
    assert lo < r["overall"]["score"] < hi
    skipped = [c for c in r["cases"] if "skipped" in c]
    assert [c["id"] for c in skipped] == ["C17", "C18", "P15", "P16"] and all("score" not in c for c in skipped)
    json.dumps(r, ensure_ascii=False)                              # serialisable


def test_known_offline_failures_are_the_expected_ones(full_run):
    failing = sorted(c["id"] for c in full_run["cases"] if c.get("score", 1) < 1)
    assert failing == ["C12", "C13", "C14", "P06", "P07", "P11", "P12", "T08"]
    assert full_run["overall"]["passed"] == 38 and full_run["flaky"] == []


def test_the_offline_run_is_repeatable(m12, full_run):
    again = m12.run_eval.run_all(m12.run_eval.load_cases(), "mock")
    assert {c["id"]: c.get("score") for c in again["cases"]} == {c["id"]: c.get("score") for c in full_run["cases"]}
    assert (again["usage"]["tokens_in"], again["usage"]["tokens_out"]) == (full_run["usage"]["tokens_in"], full_run["usage"]["tokens_out"])


def test_the_ticket_adapter_returns_the_trajectory_the_steps_and_how_the_run_ended(m12):
    done = m12.adapters.ticket("Is ticket 4471 done yet?")
    assert done.tools == [("get_ticket_status", {"ticket_id": "4471"})] and done.steps == 2 and done.reason == "done"
    stuck = m12.adapters.ticket("[mock:loop] Is ticket 4471 done yet?")              # the mock asks for the same call again
    assert stuck.reason == "no_progress" and "Service Desk" in stuck.text and stuck.steps == 2


def test_cost_is_arithmetic_on_tokens_and_prices_you_supply(m12, monkeypatch):
    monkeypatch.setenv("PRICE_IN_PER_MTOK", "3")                   # illustrative numbers for the test, not real prices
    monkeypatch.setenv("PRICE_OUT_PER_MTOK", "15")
    one = [c for c in m12.run_eval.load_cases() if c["id"] == "C01"]
    r = m12.run_eval.run_all(one, "mock")
    expected = (r["usage"]["tokens_in"] * 3 + r["usage"]["tokens_out"] * 15) / 1e6
    assert r["usage"]["cost"] == pytest.approx(expected, abs=1e-4) and r["usage"]["cost"] > 0


def test_the_mode_guard_fails_closed(m12, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
    with pytest.raises(SystemExit, match="does not match"):
        m12.run_eval.check_mode("mock")                            # a "mock" run that would reach the real API
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "http://localhost.example.com")
    with pytest.raises(SystemExit, match="does not match"):
        m12.run_eval.check_mode("mock")                            # a look-alike host is not the local mock: compare the host, not a prefix
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "http://127.0.0.1:8787")
    with pytest.raises(SystemExit, match="does not match"):
        m12.run_eval.check_mode("real")                            # a "real" run that would hit the mock
    monkeypatch.delenv("ANTHROPIC_BASE_URL")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock")
    with pytest.raises(SystemExit):
        m12.run_eval.check_mode("real")                            # the placeholder key is not a real key
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-not-real")
    m12.run_eval.check_mode("real")                                # a real-looking key and no mock URL: allowed
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "http://127.0.0.1:8787")
    m12.run_eval.check_mode("mock")


def test_the_cli_refuses_the_judge_on_the_mock_and_a_mismatched_mode(server, tmp_path):
    env = {**{k: v for k, v in os.environ.items() if k not in ("MODEL", "CLASSIFY_PROMPT")}, "ANTHROPIC_BASE_URL": server, "ANTHROPIC_API_KEY": "mock"}
    run = lambda *args: subprocess.run([sys.executable, str(LABS / "run_eval.py"), *args], capture_output=True, text=True, env=env, cwd=tmp_path)
    r = run("--mode", "mock", "--judge")
    assert r.returncode != 0 and "cannot judge" in r.stderr
    r = run("--mode", "real")
    assert r.returncode != 0 and "does not match" in r.stderr


def test_the_cli_writes_results_and_the_gate_cli_passes_them(server, tmp_path):
    env = {**{k: v for k, v in os.environ.items() if k not in ("MODEL", "CLASSIFY_PROMPT")}, "ANTHROPIC_BASE_URL": server, "ANTHROPIC_API_KEY": "mock"}
    res = tmp_path / "results.json"
    r = subprocess.run([sys.executable, str(LABS / "run_eval.py"), "--mode", "mock", "--out", str(res)], capture_output=True, text=True, env=env, cwd=tmp_path)
    assert r.returncode == 0 and "46 run, 4 skipped, 0 errors" in r.stdout and res.exists()
    g = subprocess.run([sys.executable, str(LABS / "gate.py"), str(res), "--baseline", str(LABS / "baseline_mock.json")], capture_output=True, text=True)
    assert g.returncode == 0 and "gate: pass (exit 0)" in g.stdout and "P11" in g.stdout


def test_a_harness_error_is_an_error_not_a_fail_and_the_gate_refuses_it(m12, baseline, cfg, monkeypatch):
    def boom(text):
        raise ConnectionError("the API is down")
    monkeypatch.setitem(m12.adapters.AGENTS, "ticket", boom)
    r = m12.run_eval.run_all([c for c in m12.run_eval.load_cases() if c["category"] == "ticket_lookup"], "mock")
    assert r["n_errors"] == 6 and r["n_run"] == 0 and all("score" not in c for c in r["cases"])
    broken, failed, _ = m12.gate.judge({**r, "dataset_sha": baseline["dataset_sha"]}, baseline, cfg, TODAY)
    assert any("harness is broken" in b for b in broken) and failed == []       # exit 2, not "0 cases failed, all good"


def test_an_api_outage_is_an_error_even_when_the_ticket_agent_catches_it(m12):
    """agent_loop hands off with reason model_error instead of raising; the adapter must not let that pass for a wrong answer."""
    case = {"id": "T99", "agent": "ticket", "category": "ticket_lookup", "critical": False, "real_only": False,
            "input": "[mock:overloaded] Is ticket 4471 done yet?", "checks": ["calls:get_ticket_status=4471"]}
    row = m12.run_eval.run_case(case, 1, None)
    assert "score" not in row and row["error"].startswith("RuntimeError") and "after the SDK's retries" in row["error"]       # an error, not a failed case


def test_repetitions_give_a_fractional_score_and_a_flaky_list(m12, monkeypatch):
    replies = iter(["hardware", "hardware", "software"])           # the same ticket, three runs, one different answer
    monkeypatch.setitem(m12.adapters.AGENTS, "classifier", lambda text: m12.adapters.Output(text=next(replies), steps=1))
    one = [c for c in m12.run_eval.load_cases() if c["id"] == "C01"]
    r = m12.run_eval.run_all(one, "mock", reps=3)
    assert r["cases"][0]["score"] == pytest.approx(2 / 3) and r["flaky"] == ["C01"]
    assert r["cases"][0]["failed"] and "label:hardware" in r["cases"][0]["failed"][0]


def test_judge_tokens_are_counted_apart_from_the_agents(m12, client):
    import judge
    case = {**next(c for c in m12.run_eval.load_cases() if c["id"] == "P01"), "checks": ["cites:remote-work", "judge:grounded"]}
    r = m12.run_eval.run_case(case, 1, judge.make_judge(client))
    assert r["judge_tokens"] > 0 and r["tokens_in"] > 0
    assert r["score"] == 0.0 and any(w.startswith("judge:grounded") for w in r["failed"])      # the mock's judge says no
    assert len(r["judged"]) == 1 and r["judged"][0].startswith("judge:grounded: fail, ")        # the verdict is kept beside the output
    plain = m12.run_eval.run_case(case, 1, None)                   # no judge: the judge check is skipped, the case is graded on code
    assert plain["score"] == 1.0 and plain["judge_tokens"] == 0 and plain["judged"] == []
    only_judge = m12.run_eval.run_case({**case, "checks": ["judge:grounded"]}, 1, None)
    assert only_judge["score"] == 0.0                              # no check ran: that is not a pass


# ---------------------------------------------------------------- the gate against the committed baseline

def test_the_current_agents_pass_the_gate_against_the_committed_baseline(m12, full_run, baseline, cfg):
    broken, failed, notes = m12.gate.judge(full_run, baseline, cfg, TODAY)
    assert broken == [] and failed == []
    assert full_run["usage"]["tokens_in"] == baseline["usage"]["tokens_in"]       # the mock is deterministic: tokens match to the unit
    assert full_run["usage"]["tokens_out"] == baseline["usage"]["tokens_out"]
    assert full_run["dataset_sha"] == baseline["dataset_sha"]                      # edit the dataset or an agent, regenerate the baseline
    assert {n.split()[0] for n in notes if "open defect" in n} == {"P11", "P12"}      # open defects, shown every run


def test_a_prompt_regression_is_caught_and_names_what_changed(m12, baseline, cfg):
    m12.mp.setattr(m12.adapters, "CLASSIFY_PROMPT", "classify_v1")          # the vague first draft: chatty replies fail exact match
    try:
        bad = m12.run_eval.run_all(m12.run_eval.load_cases(), "mock")
    finally:
        m12.mp.setattr(m12.adapters, "CLASSIFY_PROMPT", "classify_v3")
    broken, failed, notes = m12.gate.judge(bad, baseline, cfg, TODAY)
    assert broken == [] and any(f.startswith("critical cases that used to pass") for f in failed)
    assert any("classify_core is 0%" in f for f in failed) and any("overall score fell" in f for f in failed)
    assert any(n.startswith("classify_prompt changed: classify_v3@") for n in notes)


def test_a_leaked_prompt_looks_like_an_improvement_but_the_gate_refuses_it(m12, baseline, cfg):
    m12.mp.setattr(m12.adapters, "CLASSIFY_PROMPT", "classify_v4_overfit")
    try:
        leaky = m12.run_eval.run_all(m12.run_eval.load_cases(), "mock")
    finally:
        m12.mp.setattr(m12.adapters, "CLASSIFY_PROMPT", "classify_v3")
    assert leaky["overall"]["score"] > baseline["overall"]["score"] and leaky["leaks"] == ["C12", "C14"]
    broken, failed, _ = m12.gate.judge(leaky, baseline, cfg, TODAY)
    assert any("C12, C14" in b for b in broken) and failed == []


def test_a_subset_run_or_an_edited_dataset_is_not_comparable(m12, full_run, baseline, cfg):
    subset = m12.run_eval.run_all([c for c in m12.run_eval.load_cases() if c["agent"] == "classifier"], "mock")
    broken, _, _ = m12.gate.judge(subset, baseline, cfg, TODAY)
    assert any(b.startswith("n_run changed (46 -> 16)") for b in broken)
    edited = {**full_run, "dataset_sha": "000000000000"}
    assert any(b.startswith("dataset_sha changed") for b in m12.gate.judge(edited, baseline, cfg, TODAY)[0])
    real = {**full_run, "mode": "real"}
    assert any(b.startswith("mode changed") for b in m12.gate.judge(real, baseline, cfg, TODAY)[0])


def test_a_run_without_the_judge_is_not_comparable_with_a_baseline_made_with_it(m12, full_run, baseline, cfg):
    judged = {**baseline, "judge": True}          # the judge checks decide some cases: a run that skipped them is a different eval
    assert any(b.startswith("judge changed") for b in m12.gate.judge(full_run, judged, cfg, TODAY)[0])


# ---------------------------------------------------------------- the gate rules, one at a time, on synthetic results

def case(i, score=1.0, category="cat", critical=False, tin=100, tout=10):
    return {"id": i, "agent": "ticket", "category": category, "critical": critical, "score": score, "ms": 5, "tokens_in": tin, "tokens_out": tout}


def results(*cs, errors=0, p95=10, leaks=()):
    return {"mode": "mock", "dataset_sha": "abc", "n_run": len(cs), "n_errors": errors, "leaks": list(leaks), "versions": {"model": "m"},
            "latency_ms": {"p50": 5, "p95": p95}, "cases": list(cs), "categories": {}}


CFG = {"max_errors": 0, "max_overall_drop": 0.25, "max_regressed_cases": 1, "max_token_increase": 0.25, "max_p95_ms": 1000,
       "floors": {"cat": 0.5}, "quarantine": {}}
BASE = results(*[case(f"x{i}") for i in range(10)])


def verdict(g, new, cfg=CFG, base=BASE, today=TODAY):
    """The first word of every finding, sorted: enough to say WHICH rule fired."""
    broken, failed, _ = g.judge(new, base, cfg, today)
    return sorted(line.split()[0] for line in broken + failed)


@pytest.fixture
def g(m12):
    return m12.gate


def test_gate_passes_an_identical_run(g):
    assert verdict(g, copy.deepcopy(BASE)) == []


def test_one_regressed_case_is_within_the_limit_two_are_not(g):
    one = results(*[case(f"x{i}", 0.0 if i == 0 else 1.0) for i in range(10)])
    two = results(*[case(f"x{i}", 0.0 if i < 2 else 1.0) for i in range(10)])
    assert verdict(g, one) == [] and verdict(g, two) == ["2"]


def test_a_critical_regression_has_no_budget(g):
    base = results(*[case(f"x{i}", critical=i == 0) for i in range(10)])
    new = results(*[case(f"x{i}", 0.0 if i == 0 else 1.0, critical=i == 0) for i in range(10)])
    assert verdict(g, new, base=base) == ["critical"]                  # one case, inside max_regressed_cases, still blocks


def test_a_critical_case_failing_in_the_baseline_is_a_note_not_a_failure(g):
    base = results(*[case(f"x{i}", 0.0 if i == 0 else 1.0, critical=i == 0) for i in range(10)])
    broken, failed, notes = g.judge(copy.deepcopy(base), base, CFG, TODAY)
    assert failed == [] and notes == ["x0 is critical and fails here and in the baseline: an open defect, not a regression"]


def test_the_overall_drop_and_the_category_floor(g):
    base = results(*[case(f"x{i}") for i in range(10)])
    new = results(*[case(f"x{i}", 0.0 if i < 3 else 1.0) for i in range(10)])
    assert verdict(g, new, cfg={**CFG, "max_regressed_cases": 9, "floors": {"cat": 0.9}}, base=base) == ["category", "overall"]


def test_a_case_that_passes_most_repetitions_still_passes(g):
    flaky = results(*[case(f"x{i}", 2 / 3 if i == 0 else 1.0) for i in range(10)])
    assert verdict(g, flaky, cfg={**CFG, "max_regressed_cases": 0, "max_overall_drop": 0.5}) == []
    worse = results(*[case(f"x{i}", 1 / 3 if i == 0 else 1.0) for i in range(10)])
    assert verdict(g, worse, cfg={**CFG, "max_regressed_cases": 0, "max_overall_drop": 0.5}) == ["1"]
    half = results(*[case(f"x{i}", 0.5 if i == 0 else 1.0) for i in range(10)])        # exactly half is not "more than half"
    assert verdict(g, half, cfg={**CFG, "max_regressed_cases": 0, "max_overall_drop": 0.5}) == ["1"]


def test_tokens_and_latency(g):
    heavy = results(*[case(f"x{i}", tin=140) for i in range(10)])           # 110 -> 150 tokens per case: +36%
    assert verdict(g, heavy) == ["tokens"]
    assert verdict(g, results(*[case(f"x{i}") for i in range(10)], p95=2000)) == ["p95"]
    light = results(*[case(f"x{i}", tin=120) for i in range(10)])           # +18%: inside the 25% allowance
    assert verdict(g, light) == []


def test_quarantine_hides_a_flaky_case_until_the_date_then_demands_a_fix(g):
    flaky = results(*[case(f"x{i}", 0.0 if i < 2 else 1.0) for i in range(10)])
    cfg = {**CFG, "quarantine": {"x0": "2026-12-31", "x1": "2026-12-31"}}
    assert verdict(g, flaky, cfg=cfg) == []
    assert verdict(g, flaky, cfg=cfg, today=date(2027, 1, 1)) == ["2", "the", "the"]        # expired: fix it or delete it


def test_a_broken_eval_returns_no_verdict_on_the_agent(g):
    broken, failed, _ = g.judge(results(*[case(f"x{i}", 0.0) for i in range(10)], errors=1), BASE, CFG, TODAY)
    assert len(broken) == 1 and failed == []                       # it did not even compare scores


def test_exit_codes_through_the_command_line(tmp_path):
    good, bad, broken = tmp_path / "g.json", tmp_path / "b.json", tmp_path / "x.json"
    base, cfg_file = tmp_path / "base.json", tmp_path / "cfg.json"
    for path, data in ((base, BASE), (good, BASE), (bad, results(*[case(f"x{i}", 0.0) for i in range(10)])),
                       (broken, results(*[case(f"x{i}") for i in range(10)], errors=2)), (cfg_file, CFG)):
        path.write_text(json.dumps(data))
    run = lambda f: subprocess.run([sys.executable, str(LABS / "gate.py"), str(f), "--baseline", str(base), "--config", str(cfg_file)],
                                   capture_output=True, text=True)
    assert (run(good).returncode, run(bad).returncode, run(broken).returncode) == (0, 1, 2)
    assert "FAIL:" in run(bad).stdout and "BROKEN:" in run(broken).stdout


def test_the_real_gate_config_has_the_same_keys_and_floors_only_for_known_categories(cfg):
    real = json.loads((LABS / "gate_real.json").read_text(encoding="utf-8"))
    assert set(real) == set(cfg)
    assert set(real["floors"]) <= {c["category"] for c in cases()} and set(cfg["floors"]) <= {c["category"] for c in cases()}
    assert not (LABS / "baseline_real.json").exists()              # the first real baseline is a human decision, not a file we ship


# ---------------------------------------------------------------- the CI workflow and the lab files

WORKFLOW = yaml.safe_load((LABS / "eval.yml").read_text(encoding="utf-8"))


def test_the_workflow_parses_and_has_the_documented_shape():
    triggers = WORKFLOW.get("on", WORKFLOW.get(True))              # YAML 1.1 reads the bare key `on` as the boolean True
    assert {"pull_request", "workflow_dispatch", "schedule"} <= set(triggers) and "pull_request_target" not in triggers
    assert WORKFLOW["permissions"] == {"contents": "read"}
    assert set(WORKFLOW["jobs"]) == {"offline-eval", "real-model-eval"}


def test_only_the_real_model_job_can_see_the_secret_and_it_never_runs_for_pull_requests():
    offline, real = WORKFLOW["jobs"]["offline-eval"], WORKFLOW["jobs"]["real-model-eval"]
    assert "secrets." not in json.dumps(offline) and "ANTHROPIC_API_KEY" in json.dumps(offline)
    assert real["if"] == "github.event_name != 'pull_request'" and real["environment"] == "eval-real"
    assert "secrets.ANTHROPIC_API_KEY" in json.dumps(real) and "--mode real" in json.dumps(real)
    assert "--mode real" not in json.dumps(offline) and "mock" in json.dumps(offline)
    assert "echo" not in "".join(s.get("run", "") for s in real["steps"] if "secrets" in json.dumps(s))     # a secret is never echoed


def test_the_offline_job_starts_the_mock_waits_for_it_then_runs_tests_eval_and_gate():
    runs = [s.get("run", "") for s in WORKFLOW["jobs"]["offline-eval"]["steps"]]
    start = next(i for i, r in enumerate(runs) if "labkit.mock_server" in r)
    assert "/health" in runs[start] and "&" in runs[start]
    order = [next(i for i, r in enumerate(runs) if key in r) for key in ("pytest", "labkit.mock_server", "run_eval.py", "gate.py")]
    assert order == sorted(order)
    real_steps = WORKFLOW["jobs"]["real-model-eval"]["steps"]
    assert any(s.get("if") == "always()" and "upload-artifact" in s.get("uses", "") for s in real_steps)       # keep a real run's results


def test_every_file_the_workflow_runs_exists():
    text = (LABS / "eval.yml").read_text(encoding="utf-8")
    for rel in set(re.findall(r"labs/m12/[\w.]+", text)):
        assert (KIT / rel).exists() or rel.endswith("baseline_real.json"), rel
    assert list(KIT.glob("tests/test_m12_*.py"))


def test_lab_files_start_with_their_own_path_and_avoid_the_forbidden_things():
    for f in sorted(LABS.glob("*.py")) + [LABS / "eval.yml"]:
        body = f.read_text(encoding="utf-8")
        assert body.splitlines()[0].startswith(f"# labs/m12/{f.name}"), f.name
        if f.suffix == ".py":
            for bad in ("temperature", "top_p", "tool_choice", "content[0]", "eval(", "prefill"):
                assert bad not in body, (f.name, bad)
