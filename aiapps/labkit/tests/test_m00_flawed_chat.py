"""Module 0, lesson 0.3: five seeded flaws in an 'agent-written' chat.py, each proven by the 1.x SDK or the mock.

Run only this file:  cd aiapps/labkit && pytest tests/test_m00_flawed_chat.py
The file under test is NOT fixed on purpose. Each test passes because the flaw is really there."""
import importlib.util
import re
import socket
import threading
import time
from pathlib import Path

import anthropic
import pytest
import uvicorn

from labkit import mock_server

KIT = Path(__file__).resolve().parents[1]
FLAWED = KIT / "labs" / "m00" / "flawed_chat.py"
PLAYBOOK = KIT / "playbooks" / "m00_flawed_chat.json"


@pytest.fixture(scope="module")
def playbook_server():
    """A mock that has the Module 0 playbook loaded: a model whose answer depends on seeing its own earlier answer."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    srv = uvicorn.Server(uvicorn.Config(mock_server.create_app(str(PLAYBOOK)), host="127.0.0.1", port=port, log_level="error"))
    threading.Thread(target=srv.run, daemon=True).start()
    for _ in range(100):
        if srv.started:
            break
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}"
    srv.should_exit = True


@pytest.fixture
def flawed(playbook_server, monkeypatch):
    """A fresh copy of the module for every test, so its global `history` starts empty."""
    monkeypatch.setenv("ANTHROPIC_BASE_URL", playbook_server)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock")
    monkeypatch.setenv("MODEL", "claude-sonnet-5-5")
    monkeypatch.setenv("NO_PROXY", "127.0.0.1,localhost")
    spec = importlib.util.spec_from_file_location("flawed_chat_under_test", FLAWED)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_it_looks_fine_on_the_happy_path(flawed):
    """That is the danger: a quick demo shows nothing wrong."""
    assert "Hardware" in flawed.ask("How do I request a laptop?")


def test_flaw_1_the_key_is_hard_coded_and_the_environment_is_ignored(flawed):
    assert flawed.client.api_key == "sk-ant-EXERCISE-NOT-A-REAL-KEY-0000"      # not the "mock" we exported
    assert re.search(r"sk-ant-[A-Za-z0-9_-]{10,}", FLAWED.read_text())          # what a secret scanner looks for
    # The mock accepts any key, so offline it still "works". The real API would answer 401 (needs the real API).


def test_flaw_2_content_zero_is_not_always_text(flawed):
    with pytest.raises(AttributeError, match="ThinkingBlock"):
        flawed.ask("[mock:thinking] How do I request a laptop?")
    # The fix: choose the block by type. The same call, read properly, works.
    resp = flawed.client.messages.create(model=flawed.MODEL, max_tokens=1024, messages=[{"role": "user", "content": "[mock:thinking] hi"}])
    assert resp.content[0].type == "thinking"
    assert next(b.text for b in resp.content if b.type == "text")


def test_flaw_3_the_assistant_reply_is_never_added_to_the_history(flawed):
    flawed.ask("How do I request a laptop?")
    answer = flawed.ask("And how long does it take?")
    assert [m["role"] for m in flawed.history] == ["user", "user"]               # no assistant turn, ever
    assert "How long does what take?" in answer                                   # the model never saw its own answer


def test_flaw_3_one_missing_line_is_the_whole_difference(flawed):
    first = flawed.ask("How do I request a laptop?")
    flawed.history.append({"role": "assistant", "content": first})              # the line the agent forgot
    assert "three working days" in flawed.ask("And how long does it take?")


def test_flaw_4_temperature_is_not_a_parameter_of_the_1x_sdk(flawed):
    with pytest.raises(TypeError, match="temperature"):
        flawed.brainstorm("wifi")


def test_flaw_5_max_tokens_is_missing_in_the_summary_call(flawed):
    flawed.history.append({"role": "user", "content": "How do I request a laptop?"})
    with pytest.raises(TypeError, match="max_tokens"):
        flawed.summarise_history()


def test_all_five_flaws_are_still_in_the_file():
    """Guard: if someone 'helpfully' fixes the exercise file, this tells them to fix their own copy instead."""
    src = FLAWED.read_text()
    assert 'api_key="sk-ant-' in src and "resp.content[0].text" in src and "temperature=1.0" in src
    assert src.count("max_tokens=") == 2 and src.count("messages.create(") == 3
    assert 'history.append({"role": "assistant"' not in src
    assert anthropic.__version__.split(".")[0] == "1"
