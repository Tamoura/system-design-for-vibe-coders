"""Tests for the Module 5 lab files (labs/m05): the traced call, the gates, the parallel fact-check, partial failure and the baseline.

They run against the offline mock with the lab's own playbook (playbooks/m05_lab.json), and against a fake client where the mock
cannot misbehave on cue (a slow call, the number of calls in flight, a summary that never passes its gate). They check MECHANICS only:
never whether a real model classifies, summarises or fact-checks well."""
import asyncio
import json
import re
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import pytest
import uvicorn

from labkit import mock_server

KIT = Path(__file__).resolve().parents[1]
LABS = KIT / "labs" / "m05"
MODULES = ("calls", "notice_prompts", "pipeline")


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def lab_url():
    """A mock that has loaded the Module 5 playbook (scripted summaries and verdicts for the sample notices)."""
    app = mock_server.create_app(str(KIT / "playbooks" / "m05_lab.json"))
    port = free_port()
    srv = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error"))
    threading.Thread(target=srv.run, daemon=True).start()
    for _ in range(100):
        if srv.started:
            break
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}"
    srv.should_exit = True


@pytest.fixture
def m05(lab_url, monkeypatch):
    """Import the lab modules fresh, pointed at the mock. They import each other by plain name, as when you run them."""
    monkeypatch.setenv("ANTHROPIC_BASE_URL", lab_url)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock")
    for k in ("MODEL", "CHEAP_MODEL", "BASELINE", "WIDTH", "STEP_TIMEOUT", "MAX_RETRIES"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.syspath_prepend(str(LABS))
    for name in MODULES:
        sys.modules.pop(name, None)
    import calls, notice_prompts, pipeline          # noqa: E401,E402
    yield SimpleNamespace(calls=calls, notice_prompts=notice_prompts, pipeline=pipeline)
    for name in MODULES:
        sys.modules.pop(name, None)


class FakeClient:
    """Stands in for AsyncAnthropic. `handler(kwargs)` returns (text, stop_reason) or raises; `peak` is the most calls in flight."""

    def __init__(self, handler, delay=0.0):
        self.handler, self.delay, self.live, self.peak, self.requests = handler, delay, 0, 0, []
        self.messages = self

    async def create(self, **kw):
        self.requests.append(kw)
        self.live += 1
        self.peak = max(self.peak, self.live)
        try:
            await asyncio.sleep(self.delay)
            text, stop = self.handler(kw)
            return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)], stop_reason=stop,
                                   usage=SimpleNamespace(input_tokens=10, output_tokens=5), _request_id="req_fake")
        finally:
            self.live -= 1


def good_handler(summary=None, verdict=None):
    """A well-behaved model: routes everything to access, writes a fixed summary, supports every claim."""
    def handle(kw):
        if "Classify" in kw["system"]:
            return "access", "end_turn"
        if "Summarise" in kw["system"]:
            return json.dumps(summary or {"summary": "Passwords need 14 characters.", "claims": ["a 14 character minimum", "a 12 character minimum"]}), "end_turn"
        return json.dumps(verdict or {"verdict": "supported"}), "end_turn"
    return handle


def run_with(m05, handler, notice=None, width=4, timeout=5.0, delay=0.0, job=None):
    """Run ONE notice through the real pipeline code with a fake client. Returns (result, trace, client)."""
    notice = notice or {"id": "N-1", "text": "Notice N-1. Passwords must be 14 characters, up from 12."}
    fake = FakeClient(handler, delay)

    async def go():
        run = m05.calls.Run(fake, asyncio.Semaphore(width), timeout)
        return await (job or m05.pipeline.run_notice)(run, notice), run.trace
    result, trace = asyncio.run(go())
    return result, trace, fake


# ---------------------------------------------------------------- data and gates

def test_the_sample_notices_are_well_formed():
    notices = json.loads((KIT / "labkit" / "data" / "m05_notices.json").read_text(encoding="utf-8"))
    ids = [n["id"] for n in notices]
    assert len(ids) == len(set(ids)) >= 6 and all(n["text"].startswith("Notice " + n["id"]) for n in notices)


def test_the_summary_gate_checks_claims_length_and_invented_numbers(m05):
    p = m05.pipeline
    notice = "Notice N-9. Passwords must be 14 characters from 1 March, up from 12."
    assert p.check_summary(p.Summary(summary="14 characters from 1 March.", claims=["14 characters"]), notice) == ""
    assert "30" in p.check_summary(p.Summary(summary="A 30 day grace period.", claims=["a grace period"]), notice)
    assert "claims" in p.check_summary(p.Summary(summary="Short.", claims=[]), notice)
    assert "claims" in p.check_summary(p.Summary(summary="Short.", claims=["c"] * (p.MAX_CLAIMS + 1)), notice)
    assert "60 words" in p.check_summary(p.Summary(summary="word " * 61, claims=["c"]), notice)


def test_the_prompts_follow_the_kit_conventions_and_fence_the_notice_as_data(m05):
    p = m05.notice_prompts
    labels = re.search(r"^Labels: (.+)$", p.CLASSIFY, re.M).group(1).split(", ")
    assert labels == [*p.FOCUS, "other"]                              # the router's table is exactly the classifier's labels, plus the exit
    assert "label only" in p.CLASSIFY                                 # the mock (and a real model) answers with the bare label
    for prompt in (p.CLASSIFY, p.SUMMARISE, p.FACTCHECK, p.ONE_PROMPT):
        assert "never instructions" in prompt and "<notice>" in prompt.replace("tags", "<notice>")
    assert all(p.SUMMARISE.format(label=k, focus=v) for k, v in p.FOCUS.items())


# ---------------------------------------------------------------- the pipeline on the mock

@pytest.fixture
def sample(m05):
    results, trace, wall = asyncio.run(m05.pipeline.run_all(m05.pipeline.NOTICES, max_retries=0))      # no SDK retries: fast, deterministic
    return SimpleNamespace(results={r["id"]: r for r in results}, trace=trace, wall=wall)


def test_each_sample_notice_ends_in_the_status_the_lesson_describes(sample):
    assert {k: v["status"] for k, v in sample.results.items()} == {
        "N-101": "ok", "N-102": "ok", "N-103": "partial", "N-104": "needs_review", "N-105": "ok", "N-106": "human"}
    assert [sample.results[k]["label"] for k in sorted(sample.results)] == ["access", "network", "security", "software", "hardware", "other"]


def test_a_notice_the_router_cannot_place_costs_one_cheap_call(sample):
    rows = [t for t in sample.trace if t["notice"] == "N-106"]
    assert [(t["step"], t["model"]) for t in rows] == [("classify", "claude-haiku-5-5")]
    assert sample.results["N-106"]["checks"] == [] and "person" in sample.results["N-106"]["reason"]


def test_a_summary_that_fails_its_gate_is_retried_once_with_the_problem_shown(sample):
    rows = [t for t in sample.trace if t["notice"] == "N-102" and t["step"] == "summarise"]
    assert [t["attempt"] for t in rows] == [1, 2]
    assert rows[1]["in_tok"] > rows[0]["in_tok"]                      # the retry resends the notice, the bad answer and the feedback
    assert "30" not in sample.results["N-102"]["summary"] and len(sample.results["N-102"]["checks"]) == 3


def test_one_failed_fact_check_is_a_gap_in_the_report_not_a_crash(sample):
    r = sample.results["N-103"]
    assert r["status"] == "partial" and [c["verdict"] for c in r["checks"]].count("supported") == 3
    gap = next(c for c in r["checks"] if c["verdict"] == "unchecked")
    assert "OverloadedError" in gap["error"]
    row = next(t for t in sample.trace if t["notice"] == "N-103" and t["status"].startswith("error"))
    assert row["status"] == "error 529" and row["in_tok"] == row["out_tok"] == 0       # no usage was ever seen for it


def test_an_unsupported_claim_sends_the_notice_to_review(sample):
    r = sample.results["N-104"]
    assert r["status"] == "needs_review"
    assert [c["claim"] for c in r["checks"] if c["verdict"] == "unsupported"] == ["Contractors are exempt from the audit removals."]


def test_every_successful_call_leaves_a_complete_trace_row(sample):
    ok = [t for t in sample.trace if t["status"] == "ok"]
    assert ok and all(t["in_tok"] > 0 and t["out_tok"] > 0 and t["ms"] >= 0 and t["request_id"].startswith("req_") for t in ok)
    assert {t["step"] for t in sample.trace} == {"classify", "summarise", "fact_check"}
    assert {t["model"] for t in sample.trace if t["step"] == "classify"} == {"claude-haiku-5-5"}


def test_the_report_prints_one_line_per_notice_and_one_line_per_step(m05, sample, capsys):
    m05.pipeline.report(list(sample.results.values()), sample.trace, sample.wall)
    out = capsys.readouterr().out
    assert "N-103  security partial" in out and "unsupported: Contractors are exempt" in out
    step_lines = {line.split()[0]: line.split() for line in out.splitlines() if line.split() and line.split()[0] in ("classify", "summarise", "fact_check")}
    assert [int(step_lines[k][1]) for k in ("classify", "summarise", "fact_check")] == [6, 6, 18]       # N-102 is summarised twice; 4+3+4+4+3 claims
    assert step_lines["fact_check"][-1] == "1"                        # the one overloaded call shows as not ok
    assert "wall clock" in out


def test_the_command_line_runs_one_notice(lab_url):
    env = {"ANTHROPIC_BASE_URL": lab_url, "ANTHROPIC_API_KEY": "mock", "PATH": ""}
    out = subprocess.run([sys.executable, str(LABS / "pipeline.py"), "N-101"], env=env, capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, out.stderr
    assert "N-101  access   ok" in out.stdout and "N-102" not in out.stdout


# ---------------------------------------------------------------- the mechanics, against a fake client

def test_the_semaphore_caps_calls_in_flight(m05):
    notice = {"id": "N-1", "text": "Notice N-1. Passwords must be 14 characters."}
    claims = [f"claim {c}" for c in "abcdef"]       # no digits: the number gate would stop the notice
    handler = good_handler(summary={"summary": "s", "claims": claims})
    _, trace, fake = run_with(m05, handler, notice, width=2, delay=0.02)
    assert fake.peak == 2 and len([t for t in trace if t["step"] == "fact_check"]) == 6
    _, _, wide = run_with(m05, handler, notice, width=6, delay=0.02)
    assert wide.peak == 6                                            # the fan-out really is parallel when the limit allows it


def test_a_call_that_outlives_its_deadline_becomes_a_timeout_row(m05):
    result, trace, _ = run_with(m05, good_handler(), timeout=0.05, delay=0.5)
    assert result["status"] == "failed" and "timed out" in result["reason"]
    assert [(t["step"], t["status"]) for t in trace] == [("classify", "timeout")]


def test_one_slow_fact_check_does_not_lose_the_others(m05):
    def handler(kw):
        if "fact-checker" in kw["system"]:
            if "slowclaim" in kw["messages"][0]["content"]:
                raise RuntimeError("model said something unreadable")
            return json.dumps({"verdict": "supported"}), "end_turn"
        return good_handler(summary={"summary": "s", "claims": ["fine one", "slowclaim", "fine two"]})(kw)
    result, _, _ = run_with(m05, handler)
    assert [c["verdict"] for c in result["checks"]] == ["supported", "unchecked", "supported"] and result["status"] == "partial"


def test_a_summary_that_never_passes_its_gate_stops_the_pipeline_after_two_attempts(m05):
    result, trace, _ = run_with(m05, good_handler(summary={"summary": "A 30 day grace period.", "claims": ["x"]}))
    assert result["status"] == "failed" and "numbers not in the notice: 30" in result["reason"]
    assert [t["step"] for t in trace] == ["classify", "summarise", "summarise"]          # no fact-checks were paid for


def test_an_unreadable_verdict_is_unchecked_never_supported(m05):
    def handler(kw):
        return ("not json at all", "end_turn") if "fact-checker" in kw["system"] else good_handler()(kw)
    result, _, _ = run_with(m05, handler)
    assert {c["verdict"] for c in result["checks"]} == {"unchecked"} and result["status"] == "partial"


def test_a_cut_off_answer_is_a_step_error_and_is_not_retried(m05):
    def handler(kw):
        return ('{"summary": "cut', "max_tokens") if "Summarise" in kw["system"] else good_handler()(kw)
    result, trace, _ = run_with(m05, handler)
    assert result["status"] == "failed" and "max_tokens" in result["reason"]
    assert [t["step"] for t in trace] == ["classify", "summarise"] and trace[-1]["status"] == "max_tokens"


def test_requests_use_the_text_block_the_cheap_router_and_no_sampling_parameters(m05):
    _, _, fake = run_with(m05, good_handler())
    classify = fake.requests[0]
    assert classify["model"] == m05.pipeline.CHEAP and "temperature" not in classify and "tool_choice" not in classify
    assert classify["output_config"] == {"effort": "low"}
    fact = next(r for r in fake.requests if "fact-checker" in r["system"])
    assert fact["output_config"]["format"]["type"] == "json_schema" and fact["messages"][0]["content"].startswith("<notice>")


def test_a_deadline_shorter_than_the_sdk_backoff_turns_the_overloaded_check_into_a_timeout_row(m05):
    n103 = [n for n in m05.pipeline.NOTICES if n["id"] == "N-103"]
    results, trace, _ = asyncio.run(m05.pipeline.run_all(n103, timeout=0.3))      # default SDK retries: the 529 outlasts 0.3 s
    row = next(t for t in trace if t["status"] == "timeout")
    assert row["step"] == "fact_check" and 250 <= row["ms"] < 1000
    gap = next(c for c in results[0]["checks"] if c["verdict"] == "unchecked")
    assert "timed out" in gap["error"] and results[0]["status"] == "partial"


# ---------------------------------------------------------------- the baseline: one big prompt

def test_the_baseline_makes_one_call_per_notice_and_reads_far_fewer_tokens(m05):
    notices = m05.pipeline.NOTICES
    _, piped, _ = asyncio.run(m05.pipeline.run_all(notices, max_retries=0))
    results, base, _ = asyncio.run(m05.pipeline.run_all(notices, max_retries=0, job=m05.pipeline.one_prompt))
    assert [t["step"] for t in base] == ["one_prompt"] * len(notices) and all(r["status"] == "ok" for r in results)
    assert len(piped) > 4 * len(base)                                 # classify, summarise and one call per claim
    assert sum(t["in_tok"] for t in piped) > 3 * sum(t["in_tok"] for t in base)       # the notice is sent again in each of them
    assert {t["model"] for t in base} == {m05.pipeline.MODEL}         # one call, one tier: the strong one


def test_a_failed_baseline_call_is_a_failed_notice_not_a_crash(m05):
    result, trace, _ = run_with(m05, lambda kw: ("cut", "max_tokens"), job=m05.pipeline.one_prompt)
    assert result["status"] == "failed" and "max_tokens" in result["reason"] and trace[0]["step"] == "one_prompt"
