"""Tests for the Module 1 lab files (labs/m01): the chatbot, trim() and the first agent loop.

They run against the offline mock, and against fake clients where the mock cannot produce a
stop_reason (refusal, pause_turn). They check mechanics only, never answer quality."""
import copy
import importlib.util
import json
import os
import socket
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import anthropic
import pytest
import uvicorn

from labkit import mock_server

LABS = Path(__file__).resolve().parents[1] / "labs" / "m01"


def load(name):
    """Load labs/m01/<name>.py under a unique module name (other modules also have an agent.py)."""
    spec = importlib.util.spec_from_file_location(f"m01_{name}", LABS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(autouse=True)
def _api_key(monkeypatch):
    """The lab files build a client at import time, which wants a key in the environment."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock")


class Spy:
    """Wraps a real client and records the messages list sent on every call."""

    def __init__(self, real):
        self.real, self.calls = real, []

    @property
    def messages(self):
        return self

    def create(self, **kw):
        self.calls.append(json.loads(json.dumps(kw["messages"], default=lambda o: o.model_dump())))
        return self.real.messages.create(**kw)


class FakeClient:
    """Returns scripted responses, so we can test stop_reasons the mock cannot produce."""

    def __init__(self, *responses):
        self.responses, self.calls = list(responses), []

    @property
    def messages(self):
        return self

    def create(self, **kw):
        self.calls.append(copy.deepcopy(kw["messages"]))
        return self.responses.pop(0)


def fake_response(stop_reason, content=(), stop_details=None):
    usage = SimpleNamespace(input_tokens=1, output_tokens=1)
    return SimpleNamespace(stop_reason=stop_reason, content=list(content), usage=usage, stop_details=stop_details)


def text_block(text):
    return SimpleNamespace(type="text", text=text)


@pytest.fixture
def chat(client):
    mod = load("chat")
    mod.client = client
    mod.history.clear()
    return mod


@pytest.fixture
def agent(client):
    mod = load("agent")
    mod.client = Spy(client)
    return mod


# ------------------------------------------------------------------ the files themselves

@pytest.mark.parametrize("name", ["chat", "trim", "agent"])
def test_lab_files_start_with_their_path_and_avoid_the_old_api(name):
    source = (LABS / f"{name}.py").read_text(encoding="utf-8")
    assert source.splitlines()[0] == f"# labs/m01/{name}.py"
    assert "temperature" not in source                  # not a parameter of messages.create() in SDK 1.x
    assert "content[0].text" not in source              # content can start with a thinking block
    assert "claude-sonnet-4-5" not in source            # the labs read MODEL from the environment


# ------------------------------------------------------------------ Lab A: chat.py

def test_the_memory_is_the_list_you_resend(chat, capsys):
    chat.ask("My name is Rayan.")
    assert "Rayan" in chat.ask("What is my name?")
    assert [m["role"] for m in chat.history] == ["user", "assistant", "user", "assistant"]


def test_one_call_alone_knows_nothing_about_the_last(chat):
    chat.ask("My name is Rayan.")
    only_the_newest = chat.history[-1:] + [{"role": "user", "content": "What is my name?"}]
    resp = chat.client.messages.create(model=chat.MODEL, max_tokens=100, system=chat.SYSTEM, messages=[only_the_newest[-1]])
    assert "don't know" in chat.text_of(resp)


def test_input_tokens_climb_as_the_history_is_resent(chat, capsys):
    for question in ("hello there", "tell me about laptops", "and about monitors"):
        chat.ask(question)
    seen = [int(line.split("in=")[1].split()[0]) for line in capsys.readouterr().out.splitlines() if line.startswith("[in=")]
    assert len(seen) == 3 and seen == sorted(seen) and seen[0] < seen[-1]


def test_text_of_skips_a_leading_thinking_block(chat):
    assert chat.ask("hello [mock:thinking]").startswith("(mock)")


def test_a_failed_call_leaves_the_history_valid(chat):
    with pytest.raises(anthropic.APIStatusError):
        chat.ask("hello [mock:overloaded]")
    assert chat.history == []


# ------------------------------------------------------------------ Exercise 1.1: trim.py

def words(history):                                       # a stand-in counter: one "token" per word
    return sum(len(m["content"].split()) for m in history)


def conversation(turns):
    history = []
    for i in range(turns):
        history += [{"role": "user", "content": f"question {i} " + "w " * 10}, {"role": "assistant", "content": f"answer {i} " + "w " * 10}]
    return history + [{"role": "user", "content": "the newest question"}]


def test_trim_leaves_a_history_that_already_fits_alone():
    trim = load("trim")
    history = conversation(2)
    assert trim.trim(history, 10_000, count=words) == history


def test_trim_drops_the_oldest_turns_and_keeps_the_newest_message():
    trim = load("trim")
    history = conversation(5)
    kept = trim.trim(history, 50, count=words)
    assert kept[-1] == history[-1] and kept[0]["role"] == "user" and len(kept) < len(history)
    assert words(kept) <= 50
    assert kept == history[-len(kept):]                    # a suffix: only the OLDEST turns went


def test_trim_does_not_mutate_the_callers_list():
    trim = load("trim")
    history = conversation(4)
    before = copy.deepcopy(history)
    trim.trim(history, 20, count=words)
    assert history == before


@pytest.mark.parametrize("budget", range(0, 60, 7))
def test_trim_always_returns_a_valid_list(budget):
    trim = load("trim")
    history = conversation(4)
    kept = trim.trim(history, budget, count=words)
    assert kept and kept[0]["role"] == "user" and kept[-1] == history[-1]
    assert all(a["role"] != b["role"] for a, b in zip(kept, kept[1:]))      # still alternates


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def small_window_url():
    """A mock whose context window is only 3,000 tokens, so a chat overflows in a few turns."""
    old = os.environ.get("MOCK_CONTEXT_WINDOW")
    os.environ["MOCK_CONTEXT_WINDOW"] = "3000"
    try:
        app = mock_server.create_app("")
    finally:
        if old is None:
            del os.environ["MOCK_CONTEXT_WINDOW"]
        else:
            os.environ["MOCK_CONTEXT_WINDOW"] = old
    port = free_port()
    srv = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error"))
    threading.Thread(target=srv.run, daemon=True).start()
    for _ in range(100):
        if srv.started:
            break
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}"
    srv.should_exit = True


def test_an_overflowing_chat_fails_without_trim_and_survives_with_it(small_window_url):
    trim = load("trim")
    trim.client = anthropic.Anthropic(base_url=small_window_url, api_key="mock", max_retries=0)
    chunk = "Staff connect to the corporate VPN before opening internal systems. " * 20      # ~1,400 chars

    def run(budget):
        history = []
        for turn in range(1, 9):
            history.append({"role": "user", "content": f"Turn {turn}. {chunk}"})
            view = trim.trim(history, budget) if budget else history
            resp = trim.client.messages.create(model=trim.MODEL, max_tokens=256, system=trim.SYSTEM, messages=view)
            history.append({"role": "assistant", "content": next(b.text for b in resp.content if b.type == "text")})
        return len(history)

    with pytest.raises(anthropic.BadRequestError) as e:
        run(None)
    assert "too long" in str(e.value)
    assert run(2000) == 16                                   # all eight turns completed, none was too long


# ------------------------------------------------------------------ Lab B: agent.py

def tool_use_message(calls):
    """The assistant turn and the tool_result user turn recorded in the Spy, or ([], []) when absent."""
    assistant = [b for b in calls[1][-2]["content"] if b["type"] == "tool_use"]
    results = [b for b in calls[1][-1]["content"] if b["type"] == "tool_result"]
    return assistant, results


def test_parallel_calls_are_answered_in_one_user_message(agent):
    answer = agent.run_agent("Is ticket 4471 done yet? And what about 4472?")
    assert "Closed" in answer
    calls = agent.client.calls
    assert len(calls) == 2
    asked, answered = tool_use_message(calls)
    assert len(asked) == 2 and [r["tool_use_id"] for r in answered] == [a["id"] for a in asked]
    assert calls[1][-1]["role"] == "user" and calls[1][-2]["role"] == "assistant"


def test_the_whole_assistant_content_goes_back_into_the_list(agent):
    agent.run_agent("Is ticket 4471 done yet?")
    assert any(b["type"] == "tool_use" for b in agent.client.calls[1][-2]["content"])


def test_the_step_cap_stops_a_runaway_loop(agent):
    answer = agent.run_agent("Is ticket 4471 done yet? [mock:loop]", max_steps=3)
    assert answer == "Stopped: step cap of 3 reached."
    assert len(agent.client.calls) == 3                      # exactly three paid calls, not infinity


def test_a_cap_of_one_cannot_finish_three_tickets(agent):
    answer = agent.run_agent("Status of tickets 4471, 4472 and 4473?", max_steps=1)
    assert answer.startswith("Stopped: step cap")
    assert agent.run_agent("Status of tickets 4471, 4472 and 4473?", max_steps=2).startswith("Here is what I found")


def test_an_unknown_ticket_is_data_not_an_error(agent):
    # The mock simply echoes the tool result, so this shows the mechanics, NOT the model's honesty.
    answer = agent.run_agent("What about ticket 9999?")
    _, answered = tool_use_message(agent.client.calls)
    assert "is_error" not in answered[0] and answered[0]["content"] == "No ticket 9999 found"
    assert "No ticket 9999 found" in answer


def test_a_failing_tool_is_reported_with_is_error_and_does_not_crash_the_loop(agent, monkeypatch):
    def boom(ticket_id):
        raise TimeoutError("TicketHub timed out")
    monkeypatch.setitem(agent.IMPLEMENTATIONS, "get_ticket_status", boom)
    answer = agent.run_agent("Is ticket 4471 done yet?")
    _, answered = tool_use_message(agent.client.calls)
    assert answered[0]["is_error"] is True and answered[0]["content"] == "Error: TicketHub timed out"
    assert "error" in answer.lower()


def test_an_unknown_tool_name_is_reported_not_run():
    agent = load("agent")
    block = SimpleNamespace(type="tool_use", id="toolu_1", name="delete_everything", input={})
    [result] = agent.run_tools([block])
    assert result["is_error"] is True and "unknown tool" in result["content"] and result["tool_use_id"] == "toolu_1"


def test_a_vague_tool_is_never_called_by_the_mock(agent):
    vague = [{"name": "tool_one", "description": "does stuff",
              "input_schema": {"type": "object", "properties": {"ticket_id": {"type": "string"}}, "required": ["ticket_id"]}}]
    answer = agent.run_agent("Is ticket 4471 done yet?", tools=vague)
    assert len(agent.client.calls) == 1 and answer.startswith("(mock)")


def test_a_truncated_reply_stops_the_loop_and_runs_no_tool(agent, monkeypatch):
    ran = []
    monkeypatch.setitem(agent.IMPLEMENTATIONS, "get_ticket_status", lambda ticket_id: ran.append(ticket_id) or "x")
    answer = agent.run_agent("Is ticket 4471 done yet?", max_tokens=1)
    assert "cut off" in answer and ran == []


def test_a_refusal_ends_the_loop_with_a_clear_message():
    agent = load("agent")
    agent.client = FakeClient(fake_response("refusal", stop_details="category: cyber"))
    answer = agent.run_agent("anything")
    assert answer.startswith("Stopped: stop_reason=refusal") and len(agent.client.calls) == 1


def test_pause_turn_resumes_by_sending_the_paused_turn_back():
    agent = load("agent")
    agent.client = FakeClient(fake_response("pause_turn", [text_block("working...")]),
                              fake_response("end_turn", [text_block("All done.")]))
    assert agent.run_agent("a long task") == "All done."
    resumed = agent.client.calls[1]
    assert resumed[-1]["role"] == "assistant" and resumed[-1]["content"][0].text == "working..."


def test_an_unexpected_stop_reason_stops_instead_of_guessing():
    agent = load("agent")
    agent.client = FakeClient(fake_response("stop_sequence", [text_block("partial")]))
    assert agent.run_agent("x").startswith("Stopped: stop_reason=stop_sequence")


def test_a_plain_string_instead_of_a_tool_result_block_is_a_400(client):
    """The third loop juniors write first: the mock rejects it exactly as the real API does."""
    agent = load("agent")
    messages = [{"role": "user", "content": "Is ticket 4471 done yet?"}]
    resp = client.messages.create(model=agent.MODEL, max_tokens=300, tools=agent.TOOLS, messages=messages)
    messages += [{"role": "assistant", "content": resp.content}, {"role": "user", "content": "In progress"}]
    with pytest.raises(anthropic.BadRequestError) as e:
        client.messages.create(model=agent.MODEL, max_tokens=300, tools=agent.TOOLS, messages=messages)
    assert "tool_result" in str(e.value)
