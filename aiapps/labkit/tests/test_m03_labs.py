"""Tests for the Module 3 lab files (labs/m03): the safe tools, run_tool, the traced loop, the trace file, and the
structured-output triage with its bounded retry.

They run against the offline mock with the lab's own playbook (playbooks/m03_lab.json), and against fake clients where the
mock cannot produce a stop_reason. They check mechanics only: never whether a real model picks the right tool or label."""
import ast
import copy
import importlib.util
import json
import socket
import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import anthropic
import pytest
import uvicorn
from pydantic import ValidationError

from labkit import mock_server

KIT = Path(__file__).resolve().parents[1]
LABS = KIT / "labs" / "m03"


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def lab_url():
    """A mock that has loaded the Module 3 playbook (scripted tool mistakes and a stubborn triage model)."""
    app = mock_server.create_app(str(KIT / "playbooks" / "m03_lab.json"))
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
def lab_folder(monkeypatch):
    """The lab imports its sibling trace.py, but the standard library also has a module called trace.
    Put the lab folder first on sys.path and make sure the lab's trace is the one that gets imported."""
    original = sys.modules.pop("trace", None)
    monkeypatch.syspath_prepend(str(LABS))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock")
    yield
    sys.modules.pop("trace", None)
    if original is not None:
        sys.modules["trace"] = original


def load(name):
    spec = importlib.util.spec_from_file_location(f"m03_{name}", LABS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Spy:
    """Wraps a real client and records every messages list sent."""

    def __init__(self, real):
        self.real, self.calls = real, []

    @property
    def messages(self):
        return self

    def create(self, **kw):
        self.calls.append(json.loads(json.dumps(kw["messages"], default=lambda o: o.model_dump())))
        return self.real.messages.create(**kw)


class FakeClient:
    """Returns scripted responses, for stop_reasons the mock cannot produce."""

    def __init__(self, *responses):
        self.responses, self.calls = list(responses), []

    @property
    def messages(self):
        return self

    def create(self, **kw):
        self.calls.append(copy.deepcopy(kw["messages"]))
        return self.responses.pop(0)


def fake(stop_reason, content=()):
    usage = SimpleNamespace(input_tokens=1, output_tokens=1)
    return SimpleNamespace(stop_reason=stop_reason, content=list(content), usage=usage, _request_id="req_fake")


@pytest.fixture
def agent(lab_folder, lab_url):
    mod = load("tools_agent")
    mod.client = Spy(anthropic.Anthropic(base_url=lab_url, api_key="mock", max_retries=0))
    return mod


def tool_results(calls, index):
    return [b for b in calls[index][-1]["content"] if b["type"] == "tool_result"]


# ------------------------------------------------------------------ the files themselves

@pytest.mark.parametrize("name", ["trace", "tools_agent", "structured"])
def test_lab_files_start_with_their_path_and_avoid_the_old_api(name):
    source = (LABS / f"{name}.py").read_text(encoding="utf-8")
    assert source.splitlines()[0] == f"# labs/m03/{name}.py"
    assert "temperature" not in source and "content[0]" not in source and "claude-sonnet-4-5" not in source
    assert "tool_choice" not in source and "prefill" not in source.lower()
    calls = {n.func.id for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert not calls & {"eval", "exec"}                      # never run model output


def test_the_playbook_is_valid_json_with_rules():
    pb = json.loads((KIT / "playbooks" / "m03_lab.json").read_text(encoding="utf-8"))
    assert pb["name"] and len(pb["rules"]) >= 5


# ------------------------------------------------------------------ the three tools

@pytest.mark.parametrize("expr, expected", [("18 * 52", "936"), ("2 + 3 * 4", "14"), ("(2 + 3) * 4", "20"),
                                            ("-5 + 3", "-2"), ("10 / 4", "2.5"), ("2 ** 10", "1024"), ("7 - 10", "-3")])
def test_calculator_does_arithmetic(agent, expr, expected):
    assert agent.run_tool("calculator", {"expression": expr}) == (expected, False, "ok")


@pytest.mark.parametrize("expr", ["__import__('os').getcwd()", "open('/etc/passwd')", "[1, 2]", "'a' * 3",
                                  "(1).__class__", "x + 1", "lambda: 1", "2 +", "10 / 0", "9 ** 9 ** 9", "2 ** 1000", "(10 ** 10) ** 100 ** 2"])
def test_calculator_refuses_everything_that_is_not_arithmetic_and_never_hangs(agent, expr):
    started = time.perf_counter()
    text, is_error, kind = agent.run_tool("calculator", {"expression": expr})
    assert is_error and kind == "tool_error" and "calculator failed" in text
    assert time.perf_counter() - started < 1


def test_weather_failure_tells_the_model_how_to_recover(agent):
    assert agent.run_tool("get_weather", {"city": "Doha"}) == ("Doha: 39 C, clear", False, "ok")
    text, is_error, kind = agent.run_tool("get_weather", {"city": "Atlantis"})
    assert is_error and kind == "tool_error" and "known cities: Doha, Dubai, Paris" in text


def test_ticket_lookup_returns_data_and_a_missing_ticket_is_not_an_error(agent):
    text, is_error, _ = agent.run_tool("lookup_ticket", {"ticket_id": "4471"})
    assert not is_error and json.loads(text)["category"] == "network"
    assert agent.run_tool("lookup_ticket", {"ticket_id": "9999"}) == ("No ticket 9999 found", False, "ok")


def test_a_ticket_id_cannot_smuggle_a_query(agent):
    text, is_error, kind = agent.run_tool("lookup_ticket", {"ticket_id": "4471' OR '1'='1"})
    assert is_error and kind == "invalid_input" and "digits only" in text


# ------------------------------------------------------------------ run_tool: nothing raises

def test_unknown_tool_is_reported_not_run(agent):
    text, is_error, kind = agent.run_tool("delete_everything", {})
    assert is_error and kind == "unknown_tool" and "available tools: calculator, get_weather, lookup_ticket" in text


@pytest.mark.parametrize("bad", [{}, {"ticket_id": 4471}, {"ticket_id": None}, {"ticket_id": "INC-4471"},
                                 {"ticket_id": "4471", "force": True}, {"id": "4471"}])
def test_bad_input_is_an_error_with_a_reason_the_model_can_use(agent, bad):
    text, is_error, kind = agent.run_tool("lookup_ticket", bad)
    assert is_error and kind == "invalid_input" and text.startswith("invalid input for lookup_ticket: ")


def test_bad_input_messages_name_the_field(agent):
    assert "ticket_id: Field required" in agent.run_tool("lookup_ticket", {})[0]
    assert "ticket_id: Input should be a valid string" in agent.run_tool("lookup_ticket", {"ticket_id": 4471})[0]
    assert "force: Extra inputs are not permitted" in agent.run_tool("lookup_ticket", {"ticket_id": "4471", "force": 1})[0]


def test_a_tool_that_raises_becomes_tool_error(agent, monkeypatch):
    def boom(_):
        raise TimeoutError("TicketHub timed out")
    registry = dict(agent.REGISTRY)
    registry["lookup_ticket"] = (registry["lookup_ticket"][0], registry["lookup_ticket"][1], boom)
    monkeypatch.setattr(agent, "REGISTRY", registry)
    assert agent.run_tool("lookup_ticket", {"ticket_id": "4471"}) == ("lookup_ticket failed: TicketHub timed out", True, "tool_error")


def test_definitions_are_strict_closed_schemas_with_valid_names(agent):
    assert [d["name"] for d in agent.DEFINITIONS] == ["calculator", "get_weather", "lookup_ticket"]
    for d in agent.DEFINITIONS:
        assert d["strict"] is True and d["description"].endswith(".") and d["input_schema"]["type"] == "object"
        assert d["input_schema"]["additionalProperties"] is False and d["input_schema"]["required"]


# ------------------------------------------------------------------ the loop

def test_parallel_calls_are_answered_in_one_user_message(agent):
    answer = agent.run_tool_loop("What is the weather in Doha, and what is 18 * 52?")
    calls = agent.client.calls
    assert len(calls) == 2 and "936" in answer and "39 C" in answer
    asked = [b for b in calls[1][-2]["content"] if b["type"] == "tool_use"]
    answered = tool_results(calls, 1)
    assert len(asked) == 2 and [r["tool_use_id"] for r in answered] == [a["id"] for a in asked]
    assert calls[1][-1]["role"] == "user" and all(r["is_error"] is False for r in answered)


def test_two_tickets_make_two_parallel_lookups(agent):
    agent.run_tool_loop("Is ticket 4471 done yet? And what about 4473?")
    assert [b["input"]["ticket_id"] for b in agent.client.calls[1][-2]["content"] if b["type"] == "tool_use"] == ["4471", "4473"]


def test_bad_input_comes_back_as_is_error_and_the_model_fixes_it(agent):
    trace = agent.TraceLog()
    answer = agent.run_tool_loop("What is the status of ticket INC-4471?", trace=trace)
    results = [e for e in trace.events if e["event"] == "tool_result"]
    assert [(r["kind"], r["is_error"]) for r in results] == [("invalid_input", True), ("ok", False)]
    assert "digits only" in tool_results(agent.client.calls, 1)[0]["content"] and tool_results(agent.client.calls, 1)[0]["is_error"] is True
    assert "In progress" in answer and trace.events[-1]["event"] == "final"


def test_a_stubborn_model_is_stopped_by_the_step_cap_after_exactly_that_many_paid_calls(agent):
    trace = agent.TraceLog()
    assert agent.run_tool_loop("Look up ticket 4471 (stubborn)", max_steps=4, trace=trace) == "Stopped: step cap of 4 reached."
    assert len(agent.client.calls) == 4
    assert [e["kind"] for e in trace.events if e["event"] == "tool_result"] == ["invalid_input"] * 4
    assert trace.events[-1]["stop_reason"] == "step_cap"


def test_mock_loop_directive_is_also_capped(agent):
    assert agent.run_tool_loop("Is ticket 4471 done yet? [mock:loop]", max_steps=3).startswith("Stopped: step cap of 3")
    assert len(agent.client.calls) == 3


def test_an_unknown_tool_name_does_not_crash_the_loop(agent):
    trace = agent.TraceLog()
    answer = agent.run_tool_loop("Please archive ticket 4471", trace=trace)
    [result] = [e for e in trace.events if e["event"] == "tool_result"]
    assert result["kind"] == "unknown_tool" and result["is_error"] and "unknown tool" in answer


def test_a_tool_exception_reaches_the_model_as_is_error(agent):
    trace = agent.TraceLog()
    answer = agent.run_tool_loop("What is the weather in Atlantis?", trace=trace)
    assert tool_results(agent.client.calls, 1)[0]["is_error"] is True and "known cities" in answer


def test_whole_assistant_content_goes_back_into_the_list(agent):
    agent.run_tool_loop("What is 6 * 7?")
    assert any(b["type"] == "tool_use" for b in agent.client.calls[1][-2]["content"])


def test_a_refusal_or_truncation_runs_no_tool_and_stops(agent):
    ran = []
    block = SimpleNamespace(type="tool_use", id="toolu_1", name="calculator", input={"expression": "1 + 1"})
    agent.client = FakeClient(fake("max_tokens", [block]))
    agent.REGISTRY["calculator"] = (agent.REGISTRY["calculator"][0], agent.REGISTRY["calculator"][1], lambda a: ran.append(a) or "2")
    assert agent.run_tool_loop("1 + 1") == "Stopped: stop_reason=max_tokens" and ran == []
    agent.client = FakeClient(fake("refusal"))
    assert agent.run_tool_loop("x") == "Stopped: stop_reason=refusal"


# ------------------------------------------------------------------ the trace

def test_the_trace_file_is_one_json_object_per_line_and_tool_call_precedes_result(agent, tmp_path):
    path = tmp_path / "trace.jsonl"
    log = agent.TraceLog(str(path))
    agent.run_tool_loop("What is the weather in Doha, and what is 18 * 52?", trace=log)
    lines = path.read_text(encoding="utf-8").splitlines()
    events = [json.loads(line) for line in lines]
    assert events == log.events and [e["seq"] for e in events] == list(range(1, len(events) + 1))
    assert {e["run"] for e in events} == {log.run_id}
    kinds = [e["event"] for e in events]
    assert kinds[0] == "model_call" and kinds[-1] == "final"
    for call in (e for e in events if e["event"] == "tool_call"):
        result = next(e for e in events if e["event"] == "tool_result" and e["id"] == call["id"])
        assert call["seq"] < result["seq"]


def test_trace_clips_long_values_and_appends_across_runs(agent, tmp_path):
    trace_mod = sys.modules["trace"]
    path = tmp_path / "t.jsonl"
    a, b = trace_mod.TraceLog(str(path)), trace_mod.TraceLog(str(path))
    assert len(a.log("tool_result", output="x" * 5000)["output"]) == 300
    b.log("final", text="ok")
    events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert [e["run"] for e in events] == [a.run_id, b.run_id] and a.run_id != b.run_id


def test_the_trace_command_prints_one_line_per_event(agent, tmp_path):
    import subprocess
    path = tmp_path / "t.jsonl"
    agent.run_tool_loop("What is 6 * 7?", trace=agent.TraceLog(str(path)))
    out = subprocess.run([sys.executable, str(LABS / "trace.py"), str(path)], capture_output=True, text=True, check=True).stdout
    assert [ln.split()[2] for ln in out.splitlines()] == ["model_call", "tool_call", "tool_result", "model_call", "final"]


# ------------------------------------------------------------------ structured.py: the Pydantic contract and the bounded retry

@pytest.fixture
def lab(lab_folder, lab_url):
    spec = importlib.util.spec_from_file_location("m03_structured", LABS / "structured.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.client = Spy(anthropic.Anthropic(base_url=lab_url, api_key="mock", max_retries=0))
    return mod


def test_the_contract_enforces_the_business_rule_a_schema_cannot_express(lab):
    ok = {"category": "security", "needs_human": True, "summary": "x"}
    assert lab.Triage(**ok).needs_human is True
    with pytest.raises(ValidationError) as e:
        lab.Triage(**{**ok, "needs_human": False})
    assert "needs_human = true" in str(e.value)
    with pytest.raises(ValidationError):
        lab.Triage(**{**ok, "category": "banana"})
    with pytest.raises(ValidationError):
        lab.Triage(**{**ok, "extra": 1})


def test_the_schema_sent_to_the_api_is_closed_and_uses_output_config(lab):
    seen = {}
    real = lab.client.real

    class Capture(Spy):
        def create(self, **kw):
            seen.update(kw)
            return real.messages.create(**kw)
    lab.client = Capture(real)
    result = lab.triage("My VPN drops every ten minutes when I work from home")
    assert result.category == "network"
    schema = seen["output_config"]["format"]["schema"]
    assert seen["output_config"]["format"]["type"] == "json_schema" and schema["additionalProperties"] is False
    assert set(schema["required"]) == {"category", "needs_human", "summary"}
    assert "output_format" not in seen and "temperature" not in seen


def test_a_valid_answer_takes_one_attempt_and_is_traced(lab):
    trace = lab.TraceLog()
    result = lab.triage("My laptop battery only lasts twenty minutes now", trace=trace)
    assert result.category == "hardware" and len(lab.client.calls) == 1
    assert [e["event"] for e in trace.events] == ["validated"]


def test_a_schema_error_is_fed_back_and_the_second_attempt_is_valid(lab):
    trace = lab.TraceLog()
    result = lab.triage("My VPN drops every ten minutes [mock:bad_json]", trace=trace)
    assert isinstance(result, lab.Triage)
    assert [e["event"] for e in trace.events] == ["validation_error", "validated"]
    assert trace.events[0]["problem"] == "category: Field required"
    second = lab.client.calls[1]
    assert [m["role"] for m in second] == ["user", "assistant", "user"]
    assert "category" not in json.loads(second[1]["content"])                 # the model sees its own bad JSON...
    assert "category: Field required" in second[2]["content"]                 # ...and exactly what was wrong with it


def test_a_model_that_never_fixes_the_rule_is_stopped_after_max_attempts(lab):
    trace = lab.TraceLog()
    with pytest.raises(lab.TriageFailed) as e:
        lab.triage("I clicked a phishing link in an email", trace=trace)
    assert "still invalid after 3 attempts" in str(e.value) and "needs_human = true" in str(e.value)
    assert len(lab.client.calls) == 3 and [t["event"] for t in trace.events] == ["validation_error"] * 3
    with pytest.raises(lab.TriageFailed):
        lab.triage("I clicked a phishing link in an email", max_attempts=1)
    assert len(lab.client.calls) == 4


@pytest.mark.parametrize("stop", ["max_tokens", "refusal"])
def test_a_truncated_or_refused_reply_is_not_retried(lab, stop):
    lab.client = FakeClient(fake(stop, [SimpleNamespace(type="text", text='{"category": "net')]))
    with pytest.raises(lab.TriageFailed) as e:
        lab.triage("anything")
    assert stop in str(e.value) and len(lab.client.calls) == 1


def test_the_sdk_parse_helper_returns_a_typed_object_or_raises(lab, lab_url):
    client = anthropic.Anthropic(base_url=lab_url, api_key="mock", max_retries=0)
    kw = dict(model=lab.MODEL, max_tokens=1024, system=lab.SYSTEM, output_format=lab.Triage)
    good = client.messages.parse(messages=[{"role": "user", "content": "My laptop battery only lasts twenty minutes now"}], **kw)
    assert isinstance(good.parsed_output, lab.Triage) and good.parsed_output.category == "hardware"
    with pytest.raises(ValidationError):                                       # parse raises; you never see the raw text
        client.messages.parse(messages=[{"role": "user", "content": "My VPN drops [mock:bad_json]"}], **kw)
