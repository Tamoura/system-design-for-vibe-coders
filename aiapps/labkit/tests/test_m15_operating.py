"""Tests for the Module 15.1 lab files (labs/m15/trace_report.py, labs/m15/kill_switch.py) and the sample traces.

The trace report is plain arithmetic over a file and runs without a model. The kill-switch drill runs against the offline mock,
using its [mock:loop] directive to play an agent that never finishes. They check MECHANICS: that the arithmetic is right, that the
switch fails closed, that a flip stops a loop within one step and refuses new work, that the cost breaker pulls the switch and
that the traces carry no text. They cannot show whether your real thresholds are sensible or your real agent loops the same way."""
import importlib.util
import json
import math
import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

KIT = Path(__file__).resolve().parents[1]
LABS = KIT / "labs" / "m15"
TRACES = KIT / "labkit" / "data" / "m15_traces.jsonl"


def load(name):
    """Import a lab file by path, under a private name, so that tests never share state through sys.modules."""
    spec = importlib.util.spec_from_file_location(f"m15_{name}", LABS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def report(monkeypatch):
    for var in ("PRICE_IN_PER_MTOK", "PRICE_OUT_PER_MTOK"):
        monkeypatch.delenv(var, raising=False)
    return load("trace_report")


@pytest.fixture
def ks(server, monkeypatch):
    """kill_switch.py pointed at the offline mock. It borrows Lab 8.2's Trace by plain name; remove it afterwards."""
    monkeypatch.setenv("ANTHROPIC_BASE_URL", server)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock")
    sys.modules.pop("agent_loop", None)
    yield load("kill_switch")
    sys.modules.pop("agent_loop", None)


def run_report(path, *args, **env):
    full = {k: v for k, v in os.environ.items() if not k.startswith("PRICE_")} | env
    return subprocess.run([sys.executable, "-I", str(LABS / "trace_report.py"), str(path), *args], cwd=KIT, env=full, capture_output=True, text=True)


def write_trace(path, events):
    path.write_text("".join(json.dumps(e) + "\n" for e in events), encoding="utf-8")
    return path


def run_events(run, reason="done", tokens=(1000, 100), seconds=2.0, tools=(), **start):
    """The events of one run in the Lab 8.2 format; reason None leaves out the stop event (a process that died)."""
    ev = [{"run": run, "seq": 1, "ts": 1.0, "event": "start", **start},
          {"run": run, "seq": 2, "ts": 2.0, "event": "model", "step": 1, "stop_reason": "end_turn", "input_tokens": tokens[0], "output_tokens": tokens[1], "ms": 500}]
    ev += [{"run": run, "seq": 3 + i, "ts": 2.5, "event": "tool", "tool": t, "ms": 10, **extra} for i, (t, extra) in enumerate(tools)]
    if reason:
        ev.append({"run": run, "seq": 9, "ts": 3.0, "event": "stop", "step": 1, "reason": reason, "tokens": sum(tokens), "seconds": seconds})
    return ev


# ------------------------------------------------------------------ trace_report: the arithmetic

def test_the_nearest_rank_percentile(report):
    ten = list(range(1, 11))
    assert report.pct(ten, 50) == 5 and report.pct(ten, 95) == 10 and report.pct(ten, 100) == 10 and report.pct([7], 95) == 7
    assert report.pct([4, 1, 3, 2], 50) == 2                     # the input need not be sorted
    assert math.isnan(report.pct([], 95))


def test_cost_is_tokens_times_the_price_per_million(tmp_path):
    out = run_report(write_trace(tmp_path / "t.jsonl", run_events("a", tokens=(1000, 100))), PRICE_IN_PER_MTOK="2", PRICE_OUT_PER_MTOK="10").stdout
    assert "cost     : 0.00 in all, 0.0030 per resolved conversation" in out                  # 1000 x 2 + 100 x 10 = 3000 per million


def test_a_run_with_no_stop_event_is_an_outcome_not_missing_data(tmp_path):
    path = write_trace(tmp_path / "t.jsonl", run_events("a", reason=None) + run_events("b"))
    out = run_report(path).stdout
    assert "no_stop_line 1 (50%)" in out and "done 1 (50%)" in out


def test_cost_per_resolved_conversation_charges_failed_runs_to_the_resolved_ones(tmp_path):
    events = run_events("a", tokens=(1_000_000, 0)) + run_events("b", reason="iteration_cap", tokens=(3_000_000, 0))
    out = run_report(write_trace(tmp_path / "t.jsonl", events), PRICE_IN_PER_MTOK="1", PRICE_OUT_PER_MTOK="5").stdout
    assert "4.00 in all, 4.0000 per resolved conversation" in out         # (1 + 3) / one resolved run, not 4 / 2


def test_without_prices_the_report_says_nothing_about_money(tmp_path):
    out = run_report(write_trace(tmp_path / "t.jsonl", run_events("a"))).stdout
    assert "tokens per run p95 1,100" in out and "cost" not in out


def test_grouping_by_a_start_field_compares_releases_and_names_a_missing_field(tmp_path):
    events = run_events("a", release="r1") + run_events("b", release="r2") + run_events("c")
    out = run_report(write_trace(tmp_path / "t.jsonl", events), "--by", "release").stdout
    assert "== r1: 1 runs ==" in out and "== r2: 1 runs ==" in out and "== (none): 1 runs ==" in out


# ------------------------------------------------------------------ trace_report: what makes it exit 1

def test_a_healthy_trace_exits_zero(tmp_path):
    events = [e for i in range(10) for e in run_events(f"r{i}", seconds=2.0)]
    r = run_report(write_trace(tmp_path / "t.jsonl", events))
    assert r.returncode == 0 and "success 100.0%" in r.stdout and "BREACH" not in r.stdout


def test_a_success_rate_below_the_slo_and_a_slow_tail_each_breach(tmp_path):
    events = [e for i in range(10) for e in run_events(f"r{i}", reason="done" if i < 8 else "no_progress")]       # 80% against 90%
    r = run_report(write_trace(tmp_path / "t.jsonl", events))
    assert r.returncode == 1 and "success 80.0% (want 90%+) BREACH" in r.stdout and "p95 2.0 s (want 10 s or less) ok" in r.stdout
    slow = [e for i in range(10) for e in run_events(f"s{i}", seconds=30.0)]
    r = run_report(write_trace(tmp_path / "s.jsonl", slow))
    assert r.returncode == 1 and "p95 30.0 s (want 10 s or less) BREACH" in r.stdout


def test_personal_data_in_the_log_fails_the_report_and_never_prints_the_values(tmp_path):
    secret_email, secret_pw = "rayan@najm.example", "Summer2026!"
    events = run_events("a", goal=f"reset the MFA for {secret_email}") + run_events("b", note=f"my password is {secret_pw}") + run_events("c", goal="card 4111 1111 1111 1111")
    r = run_report(write_trace(tmp_path / "t.jsonl", events))
    assert r.returncode == 1
    assert "email in start.goal x1" in r.stdout and "secret in start.note x1" in r.stdout and "card in start.goal x1" in r.stdout
    assert secret_email not in r.stdout + r.stderr and secret_pw not in r.stdout + r.stderr


def test_unreadable_lines_and_an_empty_file_are_findings_not_silence(tmp_path):
    good = [json.dumps(e) for e in run_events("a")]
    path = tmp_path / "t.jsonl"
    path.write_text("\n".join(good + ["not json", '{"run": "x"}', "[1]"]) + "\n", encoding="utf-8")
    r = run_report(path)
    assert r.returncode == 1 and "1 runs, 3 unreadable lines" in r.stdout
    (tmp_path / "empty.jsonl").write_text("", encoding="utf-8")
    r = run_report(tmp_path / "empty.jsonl")
    assert r.returncode == 1 and "0 runs" in r.stdout                                # no traces at all is an incident too


# ------------------------------------------------------------------ the sample traces

def test_the_sample_traces_are_the_ones_the_lesson_describes():
    events = [json.loads(line) for line in TRACES.read_text(encoding="utf-8").splitlines()]
    runs = {}
    for e in events:
        runs.setdefault(e["run"], []).append(e)
    starts = {r: next(e for e in ev if e["event"] == "start") for r, ev in runs.items()}
    assert len(runs) == 83 and {s["release"] for s in starts.values()} == {"r41", "r42-canary"}
    assert all([e["seq"] for e in ev] == sorted(e["seq"] for e in ev) for ev in runs.values())
    raw_text = sorted(k for e in events for k in e if k in {"goal", "answer", "result", "input"})
    assert raw_text == ["goal", "goal", "goal"]                  # the three planted leaks of the old logger, and nothing else


def test_the_sample_shows_a_healthy_baseline_and_a_canary_that_must_be_rolled_back():
    out = run_report(TRACES, "--by", "release", PRICE_IN_PER_MTOK="1", PRICE_OUT_PER_MTOK="5")
    baseline, canary = out.stdout.split("== r42-canary")
    assert out.returncode == 1
    assert "== r41: 57 runs ==" in baseline and "done 53 (93%)" in baseline and "BREACH" not in baseline
    assert "26 runs ==" in canary and "done 17 (65%)" in canary and "success 65.4% (want 90%+) BREACH" in canary and "p95 11.9 s" in canary
    assert "card in start.goal x1, email in start.goal x1, secret in start.goal x1" in out.stdout


# ------------------------------------------------------------------ kill_switch: the switch

def test_the_switch_fails_closed_for_a_missing_torn_or_odd_file(ks, tmp_path):
    sw = ks.Switch(tmp_path / "switch.json")
    assert not sw.allowed("model_calls")                                 # missing: off, never on
    sw.path.write_text('{"flags": {"model_c', encoding="utf-8")
    assert not sw.allowed("model_calls")                                 # torn
    sw.path.write_text(json.dumps({"flags": {"model_calls": "maybe"}}), encoding="utf-8")
    assert not sw.allowed("model_calls") and not sw.allowed("write_tools") and not sw.allowed("no_such_flag")


def test_set_flips_flags_separately_leaves_no_temp_file_and_records_who_and_why(ks, tmp_path):
    sw = ks.Switch(tmp_path / "switch.json")
    sw.set("on", "ci", "start")
    assert sw.allowed("model_calls") and sw.allowed("write_tools")
    sw.set("off", "maha", "loop on r42", ("write_tools",))
    assert sw.allowed("model_calls") and not sw.allowed("write_tools")  # read-only mode: the model still answers
    assert json.loads(sw.path.read_text())["by"] == "maha"
    rows = [json.loads(line) for line in (tmp_path / "switch.json.log").read_text().splitlines()]
    assert [(r["by"], r["value"], r["flags"]) for r in rows] == [("ci", "on", ["model_calls", "write_tools"]), ("maha", "off", ["write_tools"])]
    assert sorted(p.name for p in tmp_path.iterdir()) == ["switch.json", "switch.json.log"]


def test_a_mistyped_flag_or_value_is_refused_so_a_press_that_did_nothing_cannot_look_like_one_that_worked(ks, tmp_path):
    sw = ks.Switch(tmp_path / "switch.json")
    sw.set("on", "ci", "start")
    before = sw.path.read_text()
    for value, flags in [("off", ("model_call",)), ("of", ("model_calls",)), ("OFF", ("model_calls",))]:
        with pytest.raises(ValueError):
            sw.set(value, "amal", "typo", flags)
    assert sw.path.read_text() == before and sw.allowed("model_calls")
    r = subprocess.run([sys.executable, "labs/m15/kill_switch.py", "flip", str(sw.path), "model_call", "off", "amal", "typo"], cwd=KIT, capture_output=True, text=True)
    assert r.returncode != 0 and "ValueError" in r.stderr and sw.path.read_text() == before


def test_flipping_one_flag_on_a_missing_file_does_not_switch_the_other_on(ks, tmp_path):
    sw = ks.Switch(tmp_path / "switch.json")
    sw.set("on", "ci", "only the model", ("model_calls",))
    assert sw.allowed("model_calls") and not sw.allowed("write_tools")


def test_the_command_in_the_runbook_works_as_printed(ks, tmp_path):
    sw = ks.Switch(tmp_path / "switch.json")
    sw.set("on", "ci", "start")
    runbook = (LABS / "runbooks" / "kill_switch.md").read_text(encoding="utf-8")
    cmd = next(line for line in runbook.splitlines() if "kill_switch.py flip" in line and "model_calls" in line).strip().strip("`")
    argv = cmd.replace("SWITCH_FILE", str(sw.path)).replace("YOUR_NAME", "amal").replace('"what you saw"', "sparks in the tool").split()
    assert argv[:2] == ["python", "labs/m15/kill_switch.py"]
    subprocess.run([sys.executable, *argv[1:]], cwd=KIT, check=True)
    assert not sw.allowed("model_calls") and sw.allowed("write_tools")
    assert json.loads(sw.path.read_text())["why"] == "sparks in the tool" and json.loads(sw.path.read_text())["by"] == "amal"
    subprocess.run([sys.executable, "labs/m15/kill_switch.py", "flip", str(sw.path), "all", "off", "amal", "stop everything"], cwd=KIT, check=True)
    assert not sw.allowed("write_tools")


# ------------------------------------------------------------------ kill_switch: the breaker

def test_the_breaker_trips_once_when_the_window_total_passes_the_limit(ks, tmp_path):
    sw = ks.Switch(tmp_path / "switch.json")
    sw.set("on", "ci", "start")
    breaker = ks.Breaker(sw, limit=1000)
    breaker.add(600)
    assert sw.allowed("model_calls")
    breaker.add(400)
    assert sw.allowed("model_calls")                                     # exactly the limit is still within it
    breaker.add(1)
    assert not sw.allowed("model_calls") and sw.allowed("write_tools")  # only the model is stopped
    rows = [json.loads(line) for line in (tmp_path / "switch.json.log").read_text().splitlines()]
    assert rows[-1]["by"] == "cost-breaker" and "1001 tokens" in rows[-1]["why"]
    breaker.add(5000)                                                    # already off: no second log row
    assert len((tmp_path / "switch.json.log").read_text().splitlines()) == len(rows)


def test_spend_outside_the_window_no_longer_counts(ks, tmp_path, monkeypatch):
    clock = [1000.0]
    monkeypatch.setattr(ks, "time", SimpleNamespace(time=lambda: clock[0], monotonic=time.monotonic))
    sw = ks.Switch(tmp_path / "switch.json")
    sw.set("on", "ci", "start")
    breaker = ks.Breaker(sw, limit=1000, window_s=60)
    breaker.add(900)
    clock[0] += 61
    breaker.add(900)                                                     # 900 now, not 1800
    assert sw.allowed("model_calls")
    clock[0] += 10
    breaker.add(200)
    assert not sw.allowed("model_calls")


# ------------------------------------------------------------------ kill_switch: the drill, against the mock

def test_without_the_switch_the_loop_really_does_loop(ks, tmp_path):
    """The negative control: if this stopped by itself, a green drill would prove nothing."""
    sw = ks.Switch(tmp_path / "switch.json")
    sw.set("on", "ci", "start")
    trace = ks.Trace(tmp_path / "t.jsonl")
    reason = ks.run_agent("Show the full history of ticket 4471 [mock:loop]", sw, ks.Breaker(sw, 10**9), trace, max_steps=7)
    assert reason == "iteration_cap" and sum(e["event"] == "model" for e in trace.events) == 7


def test_a_stop_reason_other_than_end_turn_is_reported_as_itself_not_as_done(ks, tmp_path, monkeypatch):
    class Resp:
        stop_reason, content, usage = "refusal", [], SimpleNamespace(input_tokens=5, output_tokens=0)

    class Client:
        messages = SimpleNamespace(create=lambda **kw: Resp())
    monkeypatch.setattr(ks.anthropic, "Anthropic", lambda **kw: Client())
    sw = ks.Switch(tmp_path / "switch.json")
    sw.set("on", "ci", "start")
    assert ks.run_agent("hi", sw, ks.Breaker(sw, 10**9), ks.Trace(tmp_path / "t.jsonl")) == "refusal"


def test_an_ordinary_request_finishes_with_done(ks, tmp_path):
    sw = ks.Switch(tmp_path / "switch.json")
    sw.set("on", "ci", "start")
    trace = ks.Trace(tmp_path / "t.jsonl")
    assert ks.run_agent("Show me the history for 4471", sw, ks.Breaker(sw, 10**9), trace) == "done"
    assert [e["event"] for e in trace.events] == ["start", "model", "tool", "model", "stop"]


def test_the_operator_drill_stops_the_loop_after_the_flip_and_refuses_new_work(ks, tmp_path):
    r = ks.drill("operator", tmp_path)
    assert r["reason"] == "killed" and r["model_calls"] == 5             # flipped after call 5; call 6 never started
    assert r["new_request"] == "killed" and r["new_request_calls"] == 0  # a new conversation does not reach the model
    again = [json.loads(line) for line in (tmp_path / "operator-again.jsonl").read_text().splitlines()]
    assert [e["event"] for e in again] == ["start", "stop"]
    flips = [json.loads(line) for line in (tmp_path / "operator.switch.json.log").read_text().splitlines()]
    assert [(f["by"], f["value"]) for f in flips] == [("drill", "on"), ("maha", "off")]


def test_the_breaker_drill_stops_the_runaway_without_a_person_and_overshoots_by_at_most_one_call(ks, tmp_path):
    r = ks.drill("breaker", tmp_path)
    trace = [json.loads(line) for line in (tmp_path / "breaker.jsonl").read_text().splitlines()]
    last_call = [e for e in trace if e["event"] == "model"][-1]
    assert r["reason"] == "killed" and 5 < r["model_calls"] < 500
    assert 12_000 < r["tokens"] <= 12_000 + last_call["input_tokens"] + last_call["output_tokens"]
    assert r["new_request_calls"] == 0
    flips = [json.loads(line) for line in (tmp_path / "breaker.switch.json.log").read_text().splitlines()]
    assert flips[-1]["by"] == "cost-breaker"


def test_a_drill_can_be_repeated_in_the_same_folder(ks, tmp_path):
    first = ks.drill("operator", tmp_path)
    second = ks.drill("operator", tmp_path)                              # the switch is set on again at the start of each drill
    assert first["model_calls"] == second["model_calls"] == 5 and second["reason"] == "killed"


def test_a_flip_from_another_process_stops_a_running_agent(ks, tmp_path):
    sw = ks.Switch(tmp_path / "switch.json")
    sw.set("on", "ci", "start")
    trace = ks.Trace(tmp_path / "t.jsonl")
    result = {}
    t = threading.Thread(target=lambda: result.update(reason=ks.run_agent("Show the full history of ticket 4471 [mock:loop]", sw, ks.Breaker(sw, 10**9), trace)), daemon=True)
    t.start()
    while sum(e["event"] == "model" for e in trace.events) < 3:
        time.sleep(0.005)
    subprocess.run([sys.executable, "labs/m15/kill_switch.py", "flip", str(sw.path), "model_calls", "off", "oncall", "loop"], cwd=KIT, check=True)
    t.join(timeout=20)
    assert not t.is_alive() and result["reason"] == "killed"
    assert sum(e["event"] == "model" for e in trace.events) < 500


def test_the_drill_traces_hold_no_text_and_the_report_reads_them(ks, tmp_path):
    ks.drill("breaker", tmp_path)
    blob = (tmp_path / "breaker.jsonl").read_text() + (tmp_path / "breaker-again.jsonl").read_text()
    assert "ticket 4471" not in blob and "done yet" not in blob and '"goal"' not in blob       # lengths, not words
    both = tmp_path / "all.jsonl"
    both.write_text(blob, encoding="utf-8")
    r = run_report(both)
    assert "killed 2 (100%)" in r.stdout and "no personal-data patterns found" in r.stdout
    assert r.returncode == 1                                             # killed runs are not successes: the SLO says so
