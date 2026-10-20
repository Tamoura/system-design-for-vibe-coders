"""Tests for the Module 14.2 lab (labs/m14/cost.py, router.py, reliable.py, report.py, probe.py, demo.py, prices.json).

They check MECHANICS against the offline mock: the cost arithmetic, the usage log, the budget guard, the routing rules, the escalation signal,
retries with backoff and jitter, the circuit breaker, the fallback model, and the report with its SLO exit codes. The mock's failure knobs
(MOCK_FAIL_EVERY, MOCK_RATE_LIMIT_EVERY and the [mock:...] directives) make the provider misbehave on a schedule.
They cannot show real prices, real latency or a real cache hit: the mock never caches (every cache field is zero), so prompt-cache savings
are checked here as ARITHMETIC only. Verifying a cache hit needs the real API."""
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import anthropic
import pytest

KIT = Path(__file__).resolve().parents[1]
LABS = KIT / "labs" / "m14"
CHEAP, MID, STRONG = "claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"
PRICES = {"checked": "test", "per_million_tokens": {
    CHEAP: {"input": 1, "output": 5, "cache_write": 1.25, "cache_read": 0.1},
    MID: {"input": 3, "output": 15, "cache_write": 3.75, "cache_read": 0.3}}}


@pytest.fixture
def lab(monkeypatch, server):
    """cost, router and report imported fresh from labs/m14, pointed at the mock."""
    monkeypatch.setenv("ANTHROPIC_BASE_URL", server)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock")
    monkeypatch.syspath_prepend(str(LABS))
    for n in ("cost", "router", "reliable", "report", "probe"):
        sys.modules.pop(n, None)
    import cost, probe, reliable, report, router                 # noqa: E401
    yield SimpleNamespace(cost=cost, router=router, reliable=reliable, report=report, probe=probe, url=server)
    for n in ("cost", "router", "reliable", "report", "probe"):
        sys.modules.pop(n, None)


def sdk(url, retries=0):
    return anthropic.Anthropic(base_url=url, api_key="mock", max_retries=retries)


def usage(i=0, o=0, w=0, r=0):
    return SimpleNamespace(input_tokens=i, output_tokens=o, cache_creation_input_tokens=w, cache_read_input_tokens=r)


def call(client, text="hello", model=MID, **kw):
    return client.create(model=model, max_tokens=1024, messages=[{"role": "user", "content": text}], **kw)


def provider_error(url, directive):
    """A real typed SDK error, produced by the mock, with its real response headers."""
    with pytest.raises(anthropic.APIError) as e:
        sdk(url).messages.create(model=MID, max_tokens=50, messages=[{"role": "user", "content": f"hi {directive}"}])
    return e.value


# ---------------------------------------------------------------- the cost arithmetic

def test_cost_uses_all_four_meters(lab):
    # 1000 uncached in, 200 out, 500 written to the cache, 2000 read from it; prices per million tokens
    got = lab.cost.cost_of(usage(1000, 200, 500, 2000), CHEAP, PRICES)
    assert got == pytest.approx((1000 * 1 + 200 * 5 + 500 * 1.25 + 2000 * 0.1) / 1e6)


def test_the_lessons_worked_example_six_turns_with_and_without_a_cached_system_prompt(lab):
    # lesson 14.2: 1,500-token system prompt, 60-token questions, 250-token answers, six turns, invented prices 1 and 5
    system, user, answer, turns = 1500, 60, 250, 6
    total_in = sum(system + t * user + (t - 1) * answer for t in range(1, turns + 1))
    total_out = turns * answer
    assert (total_in, total_out) == (14_010, 1_500)
    plain = lab.cost.cost_of(usage(total_in, total_out), CHEAP, PRICES)
    cached = lab.cost.cost_of(usage(total_in - turns * system, total_out, system, (turns - 1) * system), CHEAP, PRICES)
    assert plain * 1e6 == pytest.approx(21_510) and cached * 1e6 == pytest.approx(15_135)
    assert 1 - cached / plain == pytest.approx(0.2963, abs=1e-3)           # about 30% of the whole bill; the input alone falls 45%


def test_missing_cache_fields_count_as_zero_and_an_unpriced_model_is_none(lab):
    assert lab.cost.cost_of(usage(1_000_000, 0, None, None), CHEAP, PRICES) == pytest.approx(1.0)
    assert lab.cost.cost_of(usage(1, 1), "claude-opus-5-5", PRICES) is None


def test_prices_file_is_complete_and_sane(lab):
    prices = lab.cost.load_prices()["per_million_tokens"]
    for model in lab.router.TIERS:
        p = prices[model]
        assert set(p) == {"input", "output", "cache_write", "cache_read"} and all(isinstance(v, (int, float)) for v in p.values())
        assert p["cache_read"] < p["input"] < p["cache_write"] and p["input"] < p["output"]
    assert set(prices) >= set(lab.router.TIERS)


def test_unchecked_prices_warn_and_checked_prices_do_not(lab, tmp_path, capsys):
    (tmp_path / "p.json").write_text(json.dumps({"checked": "", "per_million_tokens": {}}))
    lab.cost.load_prices(tmp_path / "p.json")
    assert "no 'checked' date" in capsys.readouterr().err
    (tmp_path / "q.json").write_text(json.dumps({"checked": "2026-10-20", "per_million_tokens": {}}))
    lab.cost.load_prices(tmp_path / "q.json")
    assert capsys.readouterr().err == ""


# ---------------------------------------------------------------- the usage log and the budget

def test_every_call_is_one_json_line_with_tokens_cost_and_a_request_id(lab, tmp_path):
    t = lab.cost.Tracked(sdk(lab.url), PRICES, tmp_path / "u.jsonl")
    r = call(t, "How many days can I work remotely?", tag="policy", convo="c1")
    (rec,) = [json.loads(line) for line in (tmp_path / "u.jsonl").read_text().splitlines()]
    assert rec["model"] == MID and rec["tag"] == "policy" and rec["convo"] == "c1"
    assert rec["input"] == r.usage.input_tokens and rec["output"] == r.usage.output_tokens
    assert rec["cost"] == pytest.approx(lab.cost.cost_of(r.usage, MID, PRICES)) and rec["request_id"] == r._request_id
    assert rec["cache_write"] == rec["cache_read"] == 0 and rec["ms"] >= 0 and rec["stop"] == "end_turn"


def test_the_question_text_is_never_logged(lab, tmp_path):
    t = lab.cost.Tracked(sdk(lab.url), PRICES, tmp_path / "u.jsonl")
    call(t, "My password is Summer2026! please help")
    assert "Summer2026" not in (tmp_path / "u.jsonl").read_text()


def test_a_failed_call_is_logged_and_still_raises(lab, tmp_path):
    t = lab.cost.Tracked(sdk(lab.url), PRICES, tmp_path / "u.jsonl")
    with pytest.raises(anthropic.OverloadedError):
        call(t, "hi [mock:overloaded]", convo="c9")
    (rec,) = [json.loads(line) for line in (tmp_path / "u.jsonl").read_text().splitlines()]
    assert rec["error"] == "OverloadedError" and "cost" not in rec and rec["convo"] == "c9"


def test_an_unpriced_model_is_logged_with_cost_none_and_does_not_fail_the_request(lab, tmp_path):
    t = lab.cost.Tracked(sdk(lab.url), PRICES, tmp_path / "u.jsonl")
    assert call(t, "hello", model=STRONG).stop_reason == "end_turn"
    assert json.loads((tmp_path / "u.jsonl").read_text())["cost"] is None


def test_the_budget_is_checked_before_the_call_and_fails_closed(lab, tmp_path):
    calls = []
    fake = SimpleNamespace(messages=SimpleNamespace(create=lambda **kw: calls.append(kw) or SimpleNamespace(
        usage=usage(1_000_000, 0), stop_reason="end_turn", _request_id="req_x")))
    t = lab.cost.Tracked(fake, PRICES, tmp_path / "u.jsonl", budget=1.5)
    call(t, model=CHEAP)                                    # 1.0 spent
    call(t, model=CHEAP)                                    # 2.0 spent: the cap can be overshot by one call, never by two
    with pytest.raises(lab.cost.BudgetExceeded):
        call(t, model=CHEAP)
    assert len(calls) == 2                                  # the third never reached the provider


def test_the_mock_never_caches_so_the_probe_fails_offline(lab, capsys):
    assert lab.probe.cache_probe(sdk(lab.url), MID, "You are Najm Desk. " * 200) is False
    assert "read 0" in capsys.readouterr().out


def test_the_probe_passes_when_the_provider_reads_from_the_cache(lab):
    seq = iter([usage(10, 5, 900, 0), usage(10, 5, 0, 900)])
    fake = SimpleNamespace(messages=SimpleNamespace(create=lambda **kw: SimpleNamespace(usage=next(seq))))
    assert lab.probe.cache_probe(fake, MID, "x") is True


# ---------------------------------------------------------------- routing and escalation

@pytest.mark.parametrize("question, turns, tier", [
    ("How many days a week can I work remotely?", 0, 0),
    ("Which days is the Service Desk open?", 0, 0),                       # "open" as an adjective must not look like an action
    ("Please unlock my account", 0, 1),
    ("can you reset my password", 0, 1),
    ("Open a ticket for my broken keyboard", 0, 1),
    ("Compare tickets 4471 4472 4473", 0, 1),
    ("x" * 1600, 0, 1),
    ("How do I connect to the VPN?", 6, 1),
    ("How do I connect to the VPN?", 5, 0)])
def test_route_rules(lab, question, turns, tier):
    model, why = lab.router.route(question, turns)
    assert model == lab.router.TIERS[tier] and why


def test_known_limit_a_rule_misses_a_paraphrased_action_request(lab):
    # Honest limit of keyword rules, and the start of exercise 14.2-B: improve it, then change this test.
    assert lab.router.route("I need my account unlocked")[0] == lab.router.TIERS[0]


@pytest.mark.parametrize("text, ok", [
    ("Remote work is allowed up to three days a week. [remote-work]", True),
    ("Passwords must be at least 14 characters. [password-reset#0]", True),
    ("HANDOFF: the documents do not say. [vpn]", False),
    ("I don't know based on the provided documents.", False),
    ("Probably three days.", False)])
def test_confident_wants_a_citation_and_no_hand_off(lab, text, ok):
    assert lab.router.confident(text) is ok


def ask_factory(answers):
    seen = []

    def ask(model):
        seen.append(model)
        return answers[model]
    return ask, seen


def test_a_confident_cheap_answer_costs_one_call(lab):
    ask, seen = ask_factory({CHEAP: "Yes. [vpn]"})
    text, tried = lab.router.answer_with_escalation(ask, "Do I need the VPN?")
    assert tried == seen == [CHEAP] and text == "Yes. [vpn]"


def test_a_doubtful_cheap_answer_escalates_exactly_one_tier_then_stops(lab):
    ask, seen = ask_factory({CHEAP: "Not sure.", MID: "Also not sure.", STRONG: "never asked"})
    text, tried = lab.router.answer_with_escalation(ask, "Do I need the VPN?")
    assert tried == seen == [CHEAP, MID] and text == "Also not sure."         # an out-of-scope question costs two calls, never three


def test_a_hard_case_starts_in_the_middle_and_may_reach_the_top(lab):
    ask, seen = ask_factory({CHEAP: "never asked", MID: "Not sure.", STRONG: "Yes. [vpn]"})
    text, tried = lab.router.answer_with_escalation(ask, "Please unlock my account")
    assert tried == [MID, STRONG] and text == "Yes. [vpn]"


# ---------------------------------------------------------------- retries, backoff, breaker, fallback

class Flaky:
    """An `inner.create` that raises the given errors in order, then succeeds. Records the models it was asked for."""

    def __init__(self, errors):
        self.errors, self.models = list(errors), []

    def create(self, **kw):
        self.models.append(kw["model"])
        if self.errors:
            raise self.errors.pop(0)
        return "ok"


def reliable(lab, inner, **kw):
    sleeps = []
    r = lab.reliable.Reliable(inner, sleep=sleeps.append, rand=kw.pop("rand", lambda: 1.0), **kw)
    return r, sleeps


def test_backoff_doubles_with_full_jitter_and_is_capped(lab):
    e = anthropic.APIConnectionError(request=None)
    r, _ = reliable(lab, Flaky([]), base=0.5, cap=3.0)
    assert [r.delay(a, e) for a in range(5)] == [0.5, 1.0, 2.0, 3.0, 3.0]    # rand()=1 is the longest wait the jitter allows
    r0, _ = reliable(lab, Flaky([]), base=0.5, cap=3.0, rand=lambda: 0.0)
    assert [r0.delay(a, e) for a in range(5)] == [0.0] * 5                   # and rand()=0 the shortest: many clients do not retry in step
    r5, _ = reliable(lab, Flaky([]), base=0.5, cap=3.0, rand=lambda: 0.5)
    assert r5.delay(2, e) == 1.0


def test_the_servers_retry_after_beats_our_own_guess_but_is_capped(lab):
    rate_limited = provider_error(lab.url, "[mock:ratelimit]")
    assert isinstance(rate_limited, anthropic.RateLimitError) and rate_limited.response.headers["retry-after"] == "1"
    r, _ = reliable(lab, Flaky([]), base=0.5, cap=8.0)
    assert r.delay(0, rate_limited) == 1.0
    r2, _ = reliable(lab, Flaky([]), base=0.5, cap=0.25)
    assert r2.delay(0, rate_limited) == 0.25


def test_transient_errors_are_retried_with_sleeps_between(lab):
    errors = [provider_error(lab.url, "[mock:overloaded]"), provider_error(lab.url, "[mock:ratelimit]")]
    inner = Flaky(errors)
    r, sleeps = reliable(lab, inner, tries=3)
    assert r.create(model=MID) == "ok" and inner.models == [MID] * 3 and sleeps == [0.5, 1.0]      # the second wait is the 429's retry-after: 1


def test_a_bad_request_is_never_retried(lab):
    bad = anthropic.BadRequestError("bad", response=SimpleNamespace(status_code=400, headers={}, request=None), body=None)
    inner = Flaky([bad])
    r, sleeps = reliable(lab, inner, tries=3, fallback=CHEAP)
    with pytest.raises(anthropic.BadRequestError):
        r.create(model=MID)
    assert inner.models == [MID] and sleeps == []                              # one call, no wait, no fallback: retrying repeats the bug


def test_when_retries_run_out_the_last_error_is_raised(lab):
    inner = Flaky([provider_error(lab.url, "[mock:overloaded]") for _ in range(5)])
    r, sleeps = reliable(lab, inner, tries=3)
    with pytest.raises(anthropic.OverloadedError):
        r.create(model=MID)
    assert len(inner.models) == 3 and len(sleeps) == 2                         # never sleeps after the last attempt


def test_the_fallback_model_takes_over_when_retries_run_out(lab):
    inner = Flaky([provider_error(lab.url, "[mock:overloaded]") for _ in range(3)])
    r, _ = reliable(lab, inner, tries=3, fallback=CHEAP)
    assert r.create(model=MID, max_tokens=5) == "ok" and inner.models == [MID, MID, MID, CHEAP]


def test_the_breaker_opens_after_consecutive_failures_and_stops_calling_the_provider(lab):
    now = [100.0]
    inner = Flaky([provider_error(lab.url, "[mock:overloaded]") for _ in range(10)])
    r, sleeps = reliable(lab, inner, tries=3, open_after=3, cool=30.0, clock=lambda: now[0])
    with pytest.raises(anthropic.OverloadedError):
        r.create(model=MID)                                                    # three failures: the circuit opens
    assert r.opened_at == 100.0 and len(inner.models) == 3
    with pytest.raises(lab.reliable.CircuitOpen):
        r.create(model=MID)                                                    # open: no call at all
    assert len(inner.models) == 3
    now[0] = 131.0                                                             # cooled: one trial call is allowed (half open)
    inner.errors = []
    assert r.create(model=MID) == "ok" and r.opened_at is None and r.fails == 0


def test_an_open_circuit_goes_straight_to_the_fallback(lab):
    inner = Flaky([provider_error(lab.url, "[mock:overloaded]") for _ in range(2)])
    r, _ = reliable(lab, inner, tries=2, open_after=2, fallback=CHEAP)
    assert r.create(model=MID) == "ok" and r.opened_at is not None             # two failures opened it; the fallback answered
    inner.models.clear()
    assert r.create(model=MID) == "ok" and inner.models == [CHEAP]


def test_a_half_open_failure_reopens_the_circuit(lab):
    now = [0.0]
    inner = Flaky([provider_error(lab.url, "[mock:overloaded]") for _ in range(9)])
    r, _ = reliable(lab, inner, tries=1, open_after=2, cool=10.0, clock=lambda: now[0])
    for _ in range(2):
        with pytest.raises(anthropic.OverloadedError):
            r.create(model=MID)
    now[0] = 11.0
    with pytest.raises(anthropic.OverloadedError):
        r.create(model=MID)                                                    # the trial fails
    assert r.opened_at == 11.0                                                 # and the cool-down starts again


# ---------------------------------------------------------------- against the mock's failure knobs

def test_the_sdks_own_retries_hide_every_other_overload(lab, monkeypatch):
    monkeypatch.setenv("MOCK_FAIL_EVERY", "2")                                 # every second request is a 529
    monkeypatch.setattr(anthropic._base_client.SyncAPIClient, "_sleep_for_retry", lambda *a, **k: None)     # do not really wait
    c = sdk(lab.url, retries=2)
    assert all(call(c.messages).stop_reason == "end_turn" for _ in range(6))   # a failure is always followed by a success


def test_without_retries_exactly_half_the_calls_fail(lab, monkeypatch):
    monkeypatch.setenv("MOCK_FAIL_EVERY", "2")
    c, failures = sdk(lab.url, retries=0), 0
    for _ in range(6):
        try:
            call(c.messages)
        except anthropic.OverloadedError as e:                              # 529 arrives as a 5xx error
            assert e.status_code == 529
            failures += 1
    assert failures == 3


def test_reliable_survives_the_overload_schedule_and_logs_every_attempt(lab, monkeypatch, tmp_path):
    monkeypatch.setenv("MOCK_FAIL_EVERY", "2")
    t = lab.cost.Tracked(sdk(lab.url), PRICES, tmp_path / "u.jsonl")
    r, sleeps = reliable(lab, t, tries=3)
    assert all(call(r).stop_reason == "end_turn" for _ in range(6))
    rows = [json.loads(line) for line in (tmp_path / "u.jsonl").read_text().splitlines()]
    assert sum("error" in x for x in rows) == len(sleeps) >= 3                 # every failed attempt is in the log and was followed by a wait
    assert sum("error" not in x for x in rows) == 6


def test_rate_limits_are_retried_after_the_servers_retry_after(lab, monkeypatch):
    monkeypatch.setenv("MOCK_RATE_LIMIT_EVERY", "2")
    r, sleeps = reliable(lab, SimpleNamespace(create=lambda **kw: sdk(lab.url).messages.create(**kw)), tries=3)
    assert all(call(r).stop_reason == "end_turn" for _ in range(4))
    assert sleeps and set(sleeps) == {1.0}                                     # the mock sends retry-after: 1


def test_a_permanent_rate_limit_ends_in_a_typed_error_after_a_bounded_wait(lab, monkeypatch):
    monkeypatch.setenv("MOCK_RATE_LIMIT_EVERY", "1")                           # every request is a 429
    r, sleeps = reliable(lab, SimpleNamespace(create=lambda **kw: sdk(lab.url).messages.create(**kw)), tries=4)
    with pytest.raises(anthropic.RateLimitError):
        call(r)
    assert len(sleeps) == 3 and sum(sleeps) == 3.0


def test_stacked_retry_layers_multiply_the_calls(lab, monkeypatch):
    """Why Reliable wants max_retries=0: the SDK's two retries inside each of our three tries make nine requests, not three."""
    from labkit import mock_server
    monkeypatch.setenv("MOCK_RATE_LIMIT_EVERY", "1")
    monkeypatch.setattr(anthropic._base_client.SyncAPIClient, "_sleep_for_retry", lambda *a, **k: None)     # do not really wait
    for sdk_retries, expected in ((0, 3), (2, 9)):
        r, _ = reliable(lab, SimpleNamespace(create=lambda **kw: sdk(lab.url, sdk_retries).messages.create(**kw)), tries=3)
        before = next(mock_server.counter)
        with pytest.raises(anthropic.RateLimitError):
            call(r)
        assert next(mock_server.counter) - before - 1 == expected


# ---------------------------------------------------------------- the report

def rec(model=CHEAP, convo="c1", ms=100, cost=0.001, **kw):
    return {"ts": 1.0, "tag": "t", "convo": convo, "model": model, "ms": ms, "input": 100, "output": 20, "cache_write": 0, "cache_read": 0,
            "cost": cost, "stop": "end_turn", "request_id": "r", **kw}


def write_log(tmp_path, rows):
    p = tmp_path / "u.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    return str(p)


def test_p95_uses_the_nearest_rank(lab):
    assert lab.report.p95(list(range(1, 101))) == 95 and lab.report.p95([7]) == 7 and lab.report.p95([]) == 0
    assert lab.report.p95([1] * 19 + [1000]) == 1                              # one slow call in twenty does not move p95 ...
    assert lab.report.p95([1] * 18 + [1000, 1000]) == 1000                     # ... two in twenty does


def test_report_totals_per_conversation_and_per_resolved_ticket(lab, tmp_path, capsys):
    log = write_log(tmp_path, [rec(convo="a", cost=0.002), rec(convo="a", cost=0.002), rec(MID, convo="b", cost=0.006)])
    assert lab.report.main([log, "--resolved", "4", "--slo-convo-cost", "1"]) == 0     # four tickets resolved across two conversations
    out = capsys.readouterr().out
    assert "total 0.01000 over 2 conversations = 0.00500 each; 0.00250 per resolved ticket" in out and "all inside" in out
    assert CHEAP in out and MID in out


@pytest.mark.parametrize("rows, args, breach", [
    ([rec(ms=30_000)], [], "p95 latency"),
    ([rec(), rec(error="InternalServerError", ms=5)], ["--slo-error-rate", "0.1"], "error rate"),
    ([rec(cost=0.5)], [], "cost per conversation"),
    ([rec(cost=None)], [], "unpriced calls")])
def test_each_slo_breach_exits_one_and_is_named(lab, tmp_path, capsys, rows, args, breach):
    assert lab.report.main([write_log(tmp_path, rows), *args]) == 1
    assert f"BREACH of {breach}" in capsys.readouterr().out


def test_the_breach_message_names_every_breached_slo(lab, tmp_path, capsys):
    lab.report.main([write_log(tmp_path, [rec(ms=30_000, cost=0.5)])])
    out = capsys.readouterr().out
    assert "p95 latency" in out and "cost per conversation" in out and "error rate" not in out


def test_errors_are_not_counted_in_latency_or_cost(lab, tmp_path, capsys):
    rows = [rec(ms=100), rec(ms=5, cost=None, error="RateLimitError")]
    del rows[1]["cost"]
    assert lab.report.main([write_log(tmp_path, rows), "--slo-error-rate", "0.9"]) == 0
    assert "1 errors" in capsys.readouterr().out


# ---------------------------------------------------------------- the whole lab, end to end

def test_the_demo_writes_a_usage_log_that_the_report_can_read(lab, tmp_path):
    env = {"ANTHROPIC_BASE_URL": lab.url, "ANTHROPIC_API_KEY": "mock", "USAGE_LOG": str(tmp_path / "usage.jsonl"), "PATH": "/usr/bin:/bin"}
    run = subprocess.run([sys.executable, str(LABS / "demo.py")], cwd=tmp_path, env=env, capture_output=True, text=True, timeout=60)
    assert run.returncode == 0, run.stderr
    lines = run.stdout.strip().splitlines()
    assert len(lines) == 12 and sum("claude-haiku-5-5" in x for x in lines) >= 8
    rows = [json.loads(x) for x in (tmp_path / "usage.jsonl").read_text().splitlines()]
    assert {r["model"] for r in rows} == {CHEAP, MID} and len({r["convo"] for r in rows}) == 6 and all(r["cost"] > 0 for r in rows)
    rep = subprocess.run([sys.executable, str(LABS / "report.py"), str(tmp_path / "usage.jsonl"), "--resolved", "9"], capture_output=True, text=True)
    assert rep.returncode == 0 and "per resolved ticket" in rep.stdout and "0 errors" in rep.stdout


def test_the_cache_probe_script_exits_nonzero_offline(lab):
    env = {"ANTHROPIC_BASE_URL": lab.url, "ANTHROPIC_API_KEY": "mock", "PATH": "/usr/bin:/bin"}
    run = subprocess.run([sys.executable, str(LABS / "probe.py")], env=env, capture_output=True, text=True, timeout=60)
    assert run.returncode == 1 and "read 0" in run.stdout                     # the honest offline answer: the mock cannot cache
