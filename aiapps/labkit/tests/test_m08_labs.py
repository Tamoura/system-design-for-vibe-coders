"""Tests for the Module 8 lab files (labs/m08): the guarded agent loop, the trace, the hand-off and the replay tool.

They run against the offline mock with the lab's own playbook (playbooks/m08_lab.json), and against fake clients where the
mock cannot produce a stop_reason (refusal, pause_turn, an unknown value) or where speed matters. They check mechanics only:
never whether a real model picks the right tool, writes a good answer or recovers well from an error."""
import copy
import importlib.util
import json
import os
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import anthropic
import pytest
import uvicorn

from labkit import mock_server

KIT = Path(__file__).resolve().parents[1]
LABS = KIT / "labs" / "m08"


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def lab_url():
    """A mock that has loaded the Module 8 playbook (scripted trajectories: a chain, a missing tool, bad arguments...)."""
    app = mock_server.create_app(str(KIT / "playbooks" / "m08_lab.json"))
    port = free_port()
    srv = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error"))
    threading.Thread(target=srv.run, daemon=True).start()
    for _ in range(100):
        if srv.started:
            break
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}"
    srv.should_exit = True


def load(name, monkeypatch=None):
    if monkeypatch:
        for var in ("MAX_STEPS", "TOKEN_BUDGET", "TIMEOUT_S"):
            monkeypatch.delenv(var, raising=False)
    spec = importlib.util.spec_from_file_location(f"m08_{name}", LABS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def loop(monkeypatch):
    return load("agent_loop", monkeypatch)


@pytest.fixture
def replay():
    return load("replay")


@pytest.fixture
def real(lab_url):
    """A real SDK client pointed at the mock, with no SDK retries so that failures are fast."""
    return anthropic.Anthropic(base_url=lab_url, api_key="mock", max_retries=0)


class Spy:
    """Wraps a client and records a copy of every messages list sent."""

    def __init__(self, inner):
        self.inner, self.calls = inner, []

    @property
    def messages(self):
        return self

    def create(self, **kw):
        self.calls.append(json.loads(json.dumps(kw["messages"], default=lambda o: o.model_dump())))
        return self.inner.messages.create(**kw)


class FakeClient:
    """Returns scripted responses, for stop_reasons the mock cannot produce. Optionally slow."""

    def __init__(self, *responses, delay=0.0):
        self.responses, self.calls, self.delay = list(responses), [], delay

    @property
    def messages(self):
        return self

    def create(self, **kw):
        self.calls.append(copy.deepcopy(kw["messages"]))
        time.sleep(self.delay)
        return self.responses.pop(0)


def fake(stop_reason, *content, details=None):
    usage = SimpleNamespace(input_tokens=10, output_tokens=5)
    return SimpleNamespace(stop_reason=stop_reason, content=list(content), usage=usage, stop_details=details, _request_id="req_fake")


def text(t):
    return SimpleNamespace(type="text", text=t)


def tool_use(name="get_ticket_status", args=None, id="toolu_1"):
    return SimpleNamespace(type="tool_use", id=id, name=name, input=args or {"ticket_id": "4471"})


def kinds(trace):
    return [e["event"] for e in trace.events]


def tool_events(trace):
    return [e for e in trace.events if e["event"] == "tool"]


# ------------------------------------------------------------------ the files themselves

@pytest.mark.parametrize("name", ["agent_loop", "replay"])
def test_lab_files_start_with_their_path_and_avoid_the_old_api(name):
    source = (LABS / f"{name}.py").read_text(encoding="utf-8")
    assert source.splitlines()[0] == f"# labs/m08/{name}.py"
    for banned in ("temperature", "content[0]", "tool_choice", "eval(", "exec(", "budget_tokens"):
        assert banned not in source


def test_the_playbook_is_valid_json_with_a_when_and_a_reply_in_every_rule():
    book = json.loads((KIT / "playbooks" / "m08_lab.json").read_text(encoding="utf-8"))
    assert book["rules"] and all("when" in r and "reply" in r for r in book["rules"])


def test_limits_come_from_the_environment(monkeypatch):
    monkeypatch.setenv("MAX_STEPS", "3")
    monkeypatch.setenv("TOKEN_BUDGET", "999")
    monkeypatch.setenv("TIMEOUT_S", "7")
    mod = load("agent_loop")
    assert (mod.Limits().max_steps, mod.Limits().token_budget, mod.Limits().timeout_s) == (3, 999, 7.0)


# ------------------------------------------------------------------ the happy paths

def test_two_tickets_are_looked_up_in_parallel_and_answered(loop, real):
    trace = loop.Trace()
    res = loop.run("Is ticket 4471 done yet? And what about 4472?", client=real, trace=trace, check=loop.mentions_every_ticket)
    assert res.ok and res.reason == "done" and res.steps == 2 and res.tokens > 0 and res.handoff is None
    assert "4471" in res.answer and "4472" in res.answer
    assert kinds(trace) == ["start", "model", "tool", "tool", "model", "stop"]
    first, second = [e for e in trace.events if e["event"] == "model"]
    assert second["input_tokens"] > first["input_tokens"]          # the tool results are re-sent: context growth, per step


def test_all_results_of_one_step_go_back_in_one_user_message(loop, real):
    spy = Spy(real)
    loop.run("Is ticket 4471 done yet? And what about 4472?", client=spy)
    asked = [b["id"] for b in spy.calls[1][1]["content"] if b["type"] == "tool_use"]
    answered = [b["tool_use_id"] for b in spy.calls[1][2]["content"] if b["type"] == "tool_result"]
    assert len(asked) == 2 and sorted(asked) == sorted(answered)


def test_a_three_step_chain_re_sends_a_longer_history_each_step(loop, real):
    trace = loop.Trace()
    res = loop.run("Check ticket 4474, then find the colleague Noura so I can forward it.", client=real, trace=trace)
    assert res.ok and res.steps == 3 and "noura@najm.example" in res.answer
    sizes = [e["input_tokens"] for e in trace.events if e["event"] == "model"]
    assert sizes == sorted(sizes) and len(set(sizes)) == 3


def test_the_trace_has_one_json_line_per_event_with_the_promised_fields(loop, real, tmp_path):
    path = tmp_path / "trace.jsonl"
    trace = loop.Trace(str(path))
    loop.run("Is ticket 4471 done yet?", client=real, trace=trace)
    lines = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert lines == trace.events and {e["run"] for e in lines} == {trace.run_id}
    assert [e["seq"] for e in lines] == list(range(1, len(lines) + 1))
    model = next(e for e in lines if e["event"] == "model")
    assert {"step", "stop_reason", "input_tokens", "output_tokens", "total_tokens", "ms", "request_id"} <= set(model)
    tool = next(e for e in lines if e["event"] == "tool")
    assert {"step", "tool", "input", "result_chars", "ms", "is_error"} <= set(tool)
    assert lines[-1]["event"] == "stop" and lines[-1]["reason"] == "done"


# ------------------------------------------------------------------ guard 1: the iteration cap

def test_the_iteration_cap_stops_a_loop_that_never_finishes(loop, real):
    trace = loop.Trace()
    lim = loop.Limits(max_steps=3, max_repeats=99)                  # switch the no-progress guard off to isolate the cap
    res = loop.run("Is ticket 4471 done yet? [mock:loop]", lim, client=real, trace=trace)
    assert not res.ok and res.reason == "iteration_cap" and res.steps == 3
    assert len(tool_events(trace)) == 3 and len(res.handoff["tried"]) == 3


# ------------------------------------------------------------------ guard 2: the token budget

def test_the_token_budget_stops_before_a_call_it_cannot_afford(loop, real):
    trace = loop.Trace()
    res = loop.run("Is ticket 4471 done yet?", loop.Limits(token_budget=1), client=real, trace=trace)
    assert res.reason == "token_budget" and res.steps == 1
    assert kinds(trace).count("model") == 1                          # step 2 was never sent
    assert res.handoff["tokens"] == res.tokens > 0


def test_a_budget_that_is_big_enough_changes_nothing(loop, real):
    assert loop.run("Is ticket 4471 done yet?", loop.Limits(token_budget=100_000), client=real).ok


# ------------------------------------------------------------------ guard 3: the wall clock

def test_the_wall_clock_stops_a_slow_run_between_steps(loop):
    client = FakeClient(fake("tool_use", tool_use()), fake("end_turn", text("done")), delay=0.05)
    res = loop.run("Is ticket 4471 done yet?", loop.Limits(timeout_s=0.01), client=client)
    assert res.reason == "timeout" and res.steps == 1 and len(client.calls) == 1


def test_the_slow_directive_trips_the_wall_clock(loop, real):
    res = loop.run("Is ticket 4471 done yet? [mock:slow]", loop.Limits(timeout_s=1), client=real)
    assert res.reason == "timeout" and res.steps == 1 and res.handoff["seconds"] >= 3


# ------------------------------------------------------------------ guard 4: no progress

def test_the_same_call_twice_is_refused_and_the_tool_runs_once(loop, real):
    trace = loop.Trace()
    res = loop.run("Are tickets 4471 and 4473 resolved? [mock:loop]", client=real, trace=trace)
    assert res.reason == "no_progress" and res.steps == 2
    ran = [e for e in tool_events(trace) if "refused" not in e]
    refused = [e for e in tool_events(trace) if "refused" in e]
    assert len(ran) == 1 and len(refused) == 1 and "get_ticket_status" in res.handoff["why"]


def test_a_model_that_ignores_is_error_is_caught_by_the_same_guard(loop, real):
    trace = loop.Trace()
    res = loop.run("What is the status of ticket 4480?", client=real, trace=trace)
    ran = [e for e in tool_events(trace) if "refused" not in e]
    assert res.reason == "no_progress" and len(ran) == 1 and ran[0]["is_error"] is True


# ------------------------------------------------------------------ silent give-up, premature finish, errors

def test_an_empty_answer_is_a_failure_not_a_success(loop, real):
    res = loop.run("Is ticket 4471 done yet? [mock:giveup]", client=real)
    assert not res.ok and res.reason == "empty_answer" and len(res.handoff["tried"]) == 1


def test_a_premature_finish_is_caught_by_a_completion_check(loop, real):
    res = loop.run("Summarise tickets 4477 and 4478 for the shift handover.", client=real, check=loop.mentions_every_ticket)
    assert res.reason == "failed_check" and "4478" in res.handoff["why"] and "4477" not in res.handoff["why"]
    assert loop.run("Summarise tickets 4477 and 4478 for the shift handover.", client=real).ok      # without the check, it "succeeds"


def test_the_completion_check_in_plain_code():
    mod = load("agent_loop")
    assert mod.mentions_every_ticket("Is 4471 done? And 4472?", "4471 is open, 4472 is closed") is None
    assert "4472" in mod.mentions_every_ticket("Is 4471 done? And 4472?", "4471 is open")


def test_the_server_failing_after_the_sdk_retries_ends_in_a_hand_off_not_a_crash(loop, real):
    trace = loop.Trace()
    res = loop.run("Is ticket 4471 done yet? [mock:overloaded]", client=real, trace=trace)
    assert res.reason == "model_error" and res.steps == 0 and res.handoff["tried"] == []
    err = next(e for e in trace.events if e["event"] == "model_error")
    assert err["status"] == 529 and err["error"] == "OverloadedError"


def test_the_final_line_is_always_a_single_stop(loop, real):
    for goal in ("Is ticket 4471 done yet?", "Is ticket 4471 done yet? [mock:loop]", "Is ticket 4471 done yet? [mock:giveup]",
                 "Is ticket 4471 done yet? [mock:overloaded]"):
        trace = loop.Trace()
        loop.run(goal, client=real, trace=trace)
        assert kinds(trace).count("stop") == 1 and kinds(trace)[-1] == "stop"


# ------------------------------------------------------------------ every stop_reason

def test_a_cut_off_turn_runs_no_tool_and_hands_off(loop):
    client = FakeClient(fake("max_tokens", tool_use()))
    trace = loop.Trace()
    res = loop.run("Is ticket 4471 done yet?", client=client, trace=trace)
    assert res.reason == "max_tokens" and tool_events(trace) == [] and len(client.calls) == 1


def test_a_refusal_runs_no_tool_and_records_the_details(loop):
    details = SimpleNamespace(category="cyber", explanation="declined")
    client = FakeClient(fake("refusal", tool_use(), details=details))
    trace = loop.Trace()
    res = loop.run("Is ticket 4471 done yet?", client=client, trace=trace)
    assert res.reason == "refusal" and tool_events(trace) == [] and "refusal" in res.handoff["why"] and "cyber" in res.handoff["why"]


def test_a_paused_turn_is_sent_back_to_resume_it(loop):
    client = FakeClient(fake("pause_turn", text("working on it")), fake("end_turn", text("Ticket 4471 is in progress.")))
    res = loop.run("Is ticket 4471 done yet?", client=client)
    assert res.ok and res.steps == 2
    assert client.calls[1][-1]["role"] == "assistant"                # the paused turn is the last message of the next request


def test_a_paused_turn_still_counts_against_the_cap(loop):
    client = FakeClient(*[fake("pause_turn", text("still working")) for _ in range(5)])
    res = loop.run("Is ticket 4471 done yet?", loop.Limits(max_steps=3), client=client)
    assert res.reason == "iteration_cap" and len(client.calls) == 3


def test_a_stop_reason_nobody_has_seen_is_handled_by_stopping(loop):
    res = loop.run("Is ticket 4471 done yet?", client=FakeClient(fake("model_context_window_exceeded", text("..."))))
    assert res.reason == "unknown_stop" and "model_context_window_exceeded" in res.handoff["why"]


# ------------------------------------------------------------------ the gap: tools, bad arguments, long results

def test_run_tool_never_raises_and_flags_every_failure(loop, monkeypatch):
    assert loop.run_tool("get_ticket_status", {"ticket_id": "4471"})[1] is False
    assert loop.run_tool("get_ticket_status", {"ticket_id": "9999"}) == ("No ticket 9999 found", False)     # empty is data, not an error
    for name, args in [("close_ticket", {"ticket_id": "4472"}), ("get_ticket_status", {"ticket": 4471}),
                       ("get_ticket_status", {"ticket_id": 4471}), ("get_ticket_status", {"ticket_id": "1", "x": "y"}), ("get_ticket_status", {})]:
        text_, is_error = loop.run_tool(name, args)
        assert is_error is True and isinstance(text_, str)
    monkeypatch.setitem(loop.TOOLS, "lookup_employee", ("d", "name", lambda name: 1 / 0))
    assert loop.run_tool("lookup_employee", {"name": "Rayan"}) == ("lookup_employee failed: division by zero", True)


def test_a_tool_the_model_invents_is_an_error_result_and_changes_nothing(loop, real):
    trace = loop.Trace()
    res = loop.run("Please close ticket 4472.", client=real, trace=trace)
    event = tool_events(trace)[0]
    assert res.ok and event["tool"] == "close_ticket" and event["is_error"] is True and "unknown tool" in event["result"]


def test_a_wrong_argument_name_is_corrected_on_the_next_step(loop, real):
    trace = loop.Trace()
    res = loop.run("What is the status of ticket 4479?", client=real, trace=trace)
    errors = [e["is_error"] for e in tool_events(trace)]
    assert res.ok and res.steps == 3 and errors == [True, False]


def test_a_long_tool_result_is_cut_before_it_enters_the_context(loop, real, monkeypatch):
    monkeypatch.setitem(loop.TOOLS, "get_ticket_status", ("d", "ticket_id", lambda ticket_id: "x" * 5000))
    spy, trace = Spy(real), loop.Trace()
    loop.run("Is ticket 4471 done yet?", loop.Limits(result_chars=100), client=spy, trace=trace)
    sent = spy.calls[1][2]["content"][0]["content"]
    assert len(sent) < 200 and "5000 characters in all" in sent
    assert tool_events(trace)[0]["result_chars"] == 5000              # the trace keeps the true size


# ------------------------------------------------------------------ the hand-off

def test_the_hand_off_carries_the_full_context_and_matches_the_trace(loop, real):
    trace = loop.Trace()
    res = loop.run("Are tickets 4471 and 4473 resolved? [mock:loop]", client=real, trace=trace)
    packet = res.handoff
    assert {"run", "reason", "why", "goal", "steps", "tokens", "seconds", "tried", "last_text"} <= set(packet)
    assert packet["run"] == trace.run_id and packet["goal"].startswith("Are tickets 4471")
    assert packet["tried"][0]["tool"] == "get_ticket_status" and packet["tried"][0]["input"] == {"ticket_id": "4471"}
    assert trace.events[-1]["handoff"] == packet                      # the trace alone is enough to rebuild the hand-off
    assert trace.run_id in res.answer and "no_progress" in res.answer


# ------------------------------------------------------------------ the replay tool

def make_trace(loop, real, path):
    for goal in ("Is ticket 4471 done yet?", "Are tickets 4471 and 4473 resolved? [mock:loop]", "Is ticket 4471 done yet? [mock:overloaded]"):
        loop.run(goal, client=real, trace=loop.Trace(str(path)))


def test_replay_tells_each_run_as_a_story(loop, real, replay, tmp_path):
    path = tmp_path / "t.jsonl"
    make_trace(loop, real, path)
    runs = replay.load(str(path))
    assert len(runs) == 3
    stories = [replay.story(events) for events in runs.values()]
    assert "DONE" in stories[0] and "tool  get_ticket_status" in stories[0]
    assert "REFUSED (same call again)" in stories[1] and "STOPPED by no_progress" in stories[1]
    assert "ERROR OverloadedError status=529" in stories[2] and "STOPPED by model_error" in stories[2]


def test_replay_flags_a_run_that_died_without_a_stop_line(loop, real, replay, tmp_path):
    path = tmp_path / "t.jsonl"
    make_trace(loop, real, path)
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line for line in lines if '"event": "stop"' not in line) + "\n", encoding="utf-8")     # drop every stop line
    stories = [replay.story(events) for events in replay.load(str(path)).values()]
    assert len(stories) == 3 and all("NO STOP LINE" in story for story in stories)


def test_replay_runs_from_the_command_line_for_one_run_or_all(loop, real, tmp_path):
    path = tmp_path / "t.jsonl"
    make_trace(loop, real, path)
    everything = subprocess.run([sys.executable, str(LABS / "replay.py"), str(path)], capture_output=True, text=True, check=True).stdout
    assert everything.count("run ") >= 3 and "STOPPED by no_progress" in everything and "STOPPED by model_error" in everything
    run_id = json.loads(path.read_text(encoding="utf-8").splitlines()[0])["run"]
    one = subprocess.run([sys.executable, str(LABS / "replay.py"), str(path), run_id], capture_output=True, text=True, check=True).stdout
    assert run_id in one and "no_progress" not in one and "model_error" not in one


# ------------------------------------------------------------------ the command line

def test_the_agent_runs_from_the_command_line_and_writes_a_trace(lab_url, tmp_path):
    env = {"PATH": os.environ["PATH"], "ANTHROPIC_BASE_URL": lab_url, "ANTHROPIC_API_KEY": "mock", "TRACE_FILE": str(tmp_path / "cli.jsonl"), "MAX_STEPS": "1"}
    out = subprocess.run([sys.executable, str(LABS / "agent_loop.py"), "Is ticket 4471 done yet?"], env=env, capture_output=True, text=True).stdout
    assert "iteration_cap" in out and '"tried"' in out                # one step is not enough: the guard fired and printed the hand-off
    assert (tmp_path / "cli.jsonl").read_text(encoding="utf-8").count('"event": "stop"') == 1
