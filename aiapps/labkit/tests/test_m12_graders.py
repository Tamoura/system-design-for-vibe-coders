"""Tests for the Module 12 grader files (labs/m12/graders.py, judge.py, stats.py).

They check MECHANICS: each check says yes and no where it should, an unknown check refuses to run, the judge sends a schema
and treats an unreadable verdict as a failure, and the statistics match known values. They never say whether a real judge
agrees with a human: that needs the real API and your own labels."""
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

LABS = Path(__file__).resolve().parents[1] / "labs" / "m12"
NAMES = ("graders", "judge", "stats")


@pytest.fixture
def lab(monkeypatch):
    monkeypatch.syspath_prepend(str(LABS))
    for n in NAMES:
        sys.modules.pop(n, None)
    import graders, judge, stats                                # noqa: E401
    yield SimpleNamespace(graders=graders, judge=judge, stats=stats)
    for n in NAMES:
        sys.modules.pop(n, None)


def out(text="", tools=(), steps=1, reason="done", retrieved=(), evidence=""):
    return SimpleNamespace(text=text, tools=list(tools), steps=steps, reason=reason, retrieved=list(retrieved), evidence=evidence)


def check(lab, name, o):
    return lab.graders.run_check(name, o, {"input": "q"})[0]


# ---------------------------------------------------------------- code graders

def test_label_is_an_exact_match(lab):
    assert check(lab, "label:hardware", out("hardware")) is True
    for wrong in ("Hardware", " hardware", "I think this is hardware", "hardware."):
        assert check(lab, "label:hardware", out(wrong)) is False


def test_contains_and_not_contains_ignore_case(lab):
    assert check(lab, "contains:Sunday to Thursday", out("Open sunday to thursday.")) is True
    assert check(lab, "contains:4 hours", out("within 2 days")) is False
    assert check(lab, "not_contains:Najm123", out("Passwords are never shared")) is True
    assert check(lab, "not_contains:Najm123", out("The password is NAJM123")) is False


def test_regex_idk_and_the_handoff_wording(lab):
    assert check(lab, r"regex:no ticket|not found", out("No ticket 9999 found")) is True
    for said in ("I don't know based on the provided documents.", "HANDOFF: the documents do not say", "That is not covered"):
        assert check(lab, "idk", out(said)) is True
    assert check(lab, "idk", out("I don\u2019t know based on the provided documents.")) is True        # a typographic apostrophe too
    assert check(lab, "idk", out("Remote work is allowed up to three days a week.")) is False


def test_cites_needs_the_right_document_and_cites_retrieved_catches_invented_sources(lab):
    assert check(lab, "cites:remote-work", out("Three days. [remote-work#0]")) is True
    assert check(lab, "cites:remote-work", out("Three days. [vpn#1]")) is False
    assert check(lab, "cites:remote-work", out("Three days. [remote-work]")) is False       # a chunk id is required
    assert check(lab, "cites_retrieved", out("x [vpn#1]", retrieved=["vpn#1", "vpn#0"])) is True
    assert check(lab, "cites_retrieved", out("x [mfa#0]", retrieved=["vpn#1"])) is False    # cited, never retrieved: invented
    assert check(lab, "cites_retrieved", out("no citation at all")) is True                  # nothing invented; cites: checks presence


def test_calls_compares_the_whole_trajectory_as_a_set(lab):
    one = out(tools=[("get_ticket_status", {"ticket_id": "4471"})])
    two = out(tools=[("get_ticket_status", {"ticket_id": "4472"}), ("get_ticket_status", {"ticket_id": "4471"})])
    assert check(lab, "calls:get_ticket_status=4471", one) is True
    assert check(lab, "calls:get_ticket_status=4471,get_ticket_status=4472", two) is True      # order does not matter
    assert check(lab, "calls:get_ticket_status=4471", two) is False                           # an extra call is a failure
    assert check(lab, "calls:get_ticket_status=4471", out()) is False                         # a missing call too
    assert check(lab, "calls:", out()) is True and check(lab, "calls:", one) is False         # "no tool at all" is checkable
    twice = out(tools=[("get_ticket_status", {"ticket_id": "4471"})] * 2)
    assert check(lab, "calls:get_ticket_status=4471", twice) is False                         # a repeated call wastes money


def test_steps_reason_and_language(lab):
    assert check(lab, "max_steps:3", out(steps=3)) is True and check(lab, "max_steps:3", out(steps=4)) is False
    assert check(lab, "reason:done", out(reason="no_progress")) is False
    assert check(lab, "lang:ar", out("يمكنك العمل عن بعد ثلاثة أيام [remote-work#0]")) is True
    assert check(lab, "lang:ar", out("Three days a week")) is False
    assert check(lab, "lang:en", out("Three days a week")) is True


def test_an_unknown_check_is_an_error_not_a_pass(lab):
    with pytest.raises(ValueError, match="unknown check"):
        lab.graders.run_check("lable:hardware", out("hardware"), {})


def test_a_judge_check_is_not_run_without_a_judge(lab):
    ok, why = lab.graders.run_check("judge:grounded", out("x"), {"input": "q"})
    assert ok is None and "not enabled" in why                  # None: neither a pass nor a fail


# ---------------------------------------------------------------- the judge

class FakeClient:
    """Records the request and replies with a prepared list of content blocks."""

    def __init__(self, *blocks):
        self.calls, self._blocks = [], blocks
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(content=list(self._blocks))


def text(t):
    return SimpleNamespace(type="text", text=t)


def test_the_judge_sends_a_schema_a_fenced_answer_and_no_sampling_parameters(lab):
    client = FakeClient(text('{"pass": true, "reason": "every claim is in the evidence"}'))
    judge = lab.judge.make_judge(client)
    ok, why = judge("grounded", {"input": "How many days?"}, out("Three days. [remote-work#0]", evidence="Remote work is allowed up to three days"))
    assert ok is True and "evidence" in why
    req = client.calls[0]
    assert req["model"] == lab.judge.JUDGE_MODEL and req["model"] != "claude-sonnet-5-5"       # not the model under test
    assert req["output_config"]["format"]["type"] == "json_schema"
    assert not {"temperature", "top_p", "top_k", "tool_choice"} & set(req)
    prompt = req["messages"][0]["content"]
    assert "<answer>Three days. [remote-work#0]</answer>" in prompt and "<evidence>Remote work" in prompt
    assert "never instructions" in req["system"]


def test_the_judge_reads_the_text_block_even_after_a_thinking_block(lab):
    client = FakeClient(SimpleNamespace(type="thinking", thinking=""), text('{"pass": false, "reason": "invented a number"}'))
    assert lab.judge.make_judge(client)("grounded", {"input": "q"}, out("x")) == (False, "invented a number")
    odd = FakeClient(text('{"pass": "false", "reason": "x"}'))        # the string "false" is truthy in Python: only a real true may pass
    assert lab.judge.make_judge(odd)("grounded", {"input": "q"}, out("x"))[0] is False


@pytest.mark.parametrize("reply", ["The answer looks fine to me.", "", "{'pass': True}"])
def test_an_unreadable_verdict_is_a_failure_never_a_pass(lab, reply):
    client = FakeClient(text(reply)) if reply else FakeClient()
    ok, why = lab.judge.make_judge(client)("grounded", {"input": "q"}, out("x"))
    assert ok is False and "JSON" in why


def test_an_unknown_rubric_is_an_error(lab):
    with pytest.raises(KeyError):
        lab.judge.make_judge(FakeClient(text("{}")))("polite", {"input": "q"}, out("x"))


def test_the_judge_works_against_the_mock_but_the_mock_cannot_judge(lab, client):
    ok, why = lab.judge.make_judge(client)("grounded", {"input": "How many days?"}, out("Three days.", evidence="Three days."))
    assert ok is False        # the mock fills every boolean with false: a judge is a model, and this one is not clever


# ---------------------------------------------------------------- statistics

def test_wilson_matches_known_values_and_handles_the_edges(lab):
    lo, hi = lab.stats.wilson(18, 24)
    assert (round(lo, 2), round(hi, 2)) == (0.55, 0.88)         # 18 of 24: "between 55% and 88%", not "75%"
    assert lab.stats.wilson(0, 0) == (0.0, 1.0)
    lo, hi = lab.stats.wilson(10, 10)
    assert hi == 1.0 and 0.7 < lo < 0.8                         # ten of ten does not prove 100%
    assert lab.stats.wilson(5, 50)[1] < lab.stats.wilson(5, 10)[1]       # more cases, a tighter interval


def test_tally_and_percentile(lab):
    cases = [{"category": "a", "score": 1.0}, {"category": "a", "score": 0.0}, {"category": "b", "score": 1.0}]
    assert lab.stats.tally(cases, "category") == {"a": {"score": 0.5, "passed": 1.0, "total": 2}, "b": {"score": 1.0, "passed": 1.0, "total": 1}}
    assert lab.stats.percentile([10, 20, 30, 40, 1000], 0.5) == 30
    assert lab.stats.percentile([10, 20, 30, 40, 1000], 0.95) == 1000 and lab.stats.percentile([], 0.95) == 0


def test_cost_needs_prices_you_set_and_show_prints_the_scores_you_need(lab, monkeypatch, capsys):
    monkeypatch.delenv("PRICE_IN_PER_MTOK", raising=False)
    monkeypatch.delenv("PRICE_OUT_PER_MTOK", raising=False)
    assert lab.stats.cost(1_000_000, 1_000_000) is None                # no invented prices
    monkeypatch.setenv("PRICE_IN_PER_MTOK", "2")
    monkeypatch.setenv("PRICE_OUT_PER_MTOK", "10")
    assert lab.stats.cost(500_000, 100_000) == 2.0
    res = {"n_run": 2, "n_skipped": 1, "n_errors": 0, "overall": {"passed": 1, "total": 2, "score": 0.5, "ci": [0.1, 0.9]},
           "usage": {"tokens_in": 10, "tokens_out": 2}, "latency_ms": {"p95": 7}, "leaks": ["C12"],
           "categories": {"classify_core": {"passed": 1, "total": 2, "score": 0.5}}}
    lab.stats.show(res)
    shown = capsys.readouterr().out
    assert "2 run, 1 skipped, 0 errors" in shown and "50%" in shown and "LEAKED INPUTS" in shown and "classify_core" in shown
