"""Tests for the Module 7 lab (labs/m07/demo.py): the thin-slice Najm Desk demo, its router, its guards, its hand-off and its
data files (the requesters, the demo script, the lab playbook).

They run against the offline mock with the lab's own playbook (playbooks/m07_lab.json), which scripts one model mistake (an
invented source). They check MECHANICS only: that the guards fire, that nothing leaks, that the model is not called when it
should not be. They cannot show whether a real model answers well, cites faithfully or routes sentences correctly."""
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
LABS = KIT / "labs" / "m07"
DATA = KIT / "labkit" / "data"
MODULES = ("demo", "rag", "bm25", "compare")
KINDS = {"answer", "status", "idk", "refused", "declined", "withheld", "degraded"}


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def lab_url():
    """A mock that has loaded the Module 7 playbook (one scripted mistake: a source the model was never given)."""
    app = mock_server.create_app(str(KIT / "playbooks" / "m07_lab.json"))
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
def m07(lab_url, monkeypatch):
    """Import demo.py (and, through it, the Module 4 lab) fresh, pointed at the mock; remove them afterwards."""
    monkeypatch.setenv("ANTHROPIC_BASE_URL", lab_url)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock")
    for k in ("MODEL", "EMBEDDER", "MIN_SIM"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.syspath_prepend(str(LABS))
    for name in MODULES:
        sys.modules.pop(name, None)
    import demo                                   # noqa: E402
    yield SimpleNamespace(demo=demo, rag=demo.rag, url=lab_url)
    for name in MODULES:
        sys.modules.pop(name, None)


class Spy:
    """Wraps rag.client and records every request that would reach the model."""

    def __init__(self, real):
        self.real, self.calls, self.messages = real, [], self

    def create(self, **kw):
        self.calls.append(kw)
        return self.real.messages.create(**kw)


def run_demo(m07, *args):
    import os
    env = {**os.environ, "ANTHROPIC_BASE_URL": m07.url, "ANTHROPIC_API_KEY": "mock"}
    env.pop("EMBEDDER", None)
    return subprocess.run([sys.executable, str(LABS / "demo.py"), *args], capture_output=True, text=True, env=env, cwd=KIT, timeout=120)


# ---------------------------------------------------------------- the whole demo, as a customer would see it

def test_the_whole_demo_script_passes_every_slice_check(m07):
    done = run_demo(m07)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "7/7 slice checks passed" in done.stdout
    assert done.stdout.count("] PASS") == 7 and "] FAIL" not in done.stdout       # the titles say FAILURE: look at the verdicts


def test_one_question_from_the_command_line_respects_who_is_asking(m07):
    mine = run_demo(m07, "What is the status of ticket 4473?", "Rayan")
    theirs = run_demo(m07, "What is the status of ticket 4473?", "Lujain")
    assert "Locked out" in mine.stdout
    assert "can't find a ticket 4473" in theirs.stdout and "Locked out" not in theirs.stdout


# ---------------------------------------------------------------- the router

@pytest.mark.parametrize("sentence, expected", [
    ("How many days a week can I work remotely?", "policy"),
    ("How do I reset my password?", "policy"),                  # a question about the policy is not a request to act
    ("Please reset my password", "action"),
    ("Can you unlock my account?", "action"),
    ("What is the status of ticket 4471?", "ticket"),
    ("Is case 4473 closed yet?", "ticket"),
    ("My VPN number is 4471 and I need help", "policy"),        # a bare number is not a ticket request: keywords are crude
])
def test_router_sends_each_sentence_down_one_path(m07, sentence, expected):
    assert m07.demo.route(sentence) == expected


# ---------------------------------------------------------------- guard 1: tickets belong to their requester

def test_an_owner_sees_the_ticket_and_no_hand_off_is_made(m07):
    _, reply = m07.demo.respond("Rayan", "What is the status of ticket 4471?")
    assert reply.kind == "status" and "VPN drops" in reply.text and reply.handoff is None


def test_a_stranger_gets_no_detail_and_cannot_tell_a_real_ticket_from_a_missing_one(m07):
    _, someone_elses = m07.demo.respond("Rayan", "What is the status of ticket 4472?")
    _, missing = m07.demo.respond("Rayan", "What is the status of ticket 9999?")
    assert someone_elses.kind == missing.kind == "refused"
    assert "charger" not in someone_elses.text.lower()
    assert someone_elses.text.replace("4472", "N") == missing.text.replace("9999", "N")
    assert someone_elses.handoff["reason"] == "not the requester's ticket"


def test_every_ticket_in_the_kit_has_a_requester_who_exists():
    tickets = json.loads((DATA / "tickets.json").read_text(encoding="utf-8"))
    owners = json.loads((DATA / "m07_requesters.json").read_text(encoding="utf-8"))
    names = {e["name"] for e in json.loads((DATA / "employees.json").read_text(encoding="utf-8"))}
    assert set(owners) == set(tickets) and set(owners.values()) <= names


# ---------------------------------------------------------------- guard 2: the citation gate, and the model that must not be called

def test_a_policy_answer_carries_a_source_that_was_retrieved(m07):
    _, reply = m07.demo.respond("Rayan", "How many days a week can I work remotely?")
    assert reply.kind == "answer" and "[remote-work#0]" in reply.text and reply.handoff is None


def test_an_invented_source_is_withheld_and_the_hand_off_names_it(m07):
    _, reply = m07.demo.respond("Rayan", "Who pays for a new laptop, and how long does it take?")
    assert reply.kind == "withheld"
    assert "department" not in reply.text.lower() and "finance-budget" not in reply.text
    assert "finance-budget#3" in reply.handoff["reason"] and reply.handoff["retrieved"]


def test_an_answer_with_no_citation_at_all_is_withheld(m07, monkeypatch):
    monkeypatch.setattr(m07.rag, "answer", lambda question, hits: "Three days, I think.")
    _, reply = m07.demo.respond("Rayan", "How many days a week can I work remotely?")
    assert reply.kind == "withheld" and "no citation" in reply.handoff["reason"]


def test_nothing_in_the_library_means_no_model_call_and_a_hand_off(m07, monkeypatch):
    spy = Spy(m07.rag.client)
    monkeypatch.setattr(m07.rag, "client", spy)
    _, reply = m07.demo.respond("Rayan", "What is on the cafeteria menu today?")
    assert reply.kind == "idk" and reply.handoff["reason"] == "no answer in the library"
    assert spy.calls == []


def test_an_action_request_is_declined_before_any_model_or_tool_runs(m07, monkeypatch):
    spy = Spy(m07.rag.client)
    monkeypatch.setattr(m07.rag, "client", spy)
    name, reply = m07.demo.respond("Rayan", "Please reset my password")
    assert (name, reply.kind) == ("action", "declined") and reply.handoff["reason"] == "action not in scope"
    assert spy.calls == []


# ---------------------------------------------------------------- degraded mode

def test_when_the_model_is_down_the_closest_passage_is_shown_as_such(m07, monkeypatch):
    live, seen, real_policy = m07.rag.client, {}, m07.demo.policy

    def watch(user, text):                              # look at the client the drill installs, then run the real code
        seen["url"], seen["retries"] = str(m07.rag.client.base_url), m07.rag.client.max_retries
        return real_policy(user, text)
    monkeypatch.setattr(m07.demo, "policy", watch)
    _, reply = m07.demo.respond("Rayan", "How many days a week can I work remotely?", outage=True)
    assert reply.kind == "degraded" and "closest policy text, not an answer" in reply.text
    assert "[remote-work#0]" in reply.text and reply.handoff["reason"] == "model unavailable"
    assert "127.0.0.1:1" in seen["url"] and seen["retries"] == 0     # a real connection failure, aimed away from the mock
    assert m07.rag.client is live                                    # the drill never leaves its client installed


def test_the_real_client_comes_back_even_when_the_answer_code_crashes(m07, monkeypatch):
    live = m07.rag.client

    def boom(user, text):
        raise RuntimeError("crash")
    monkeypatch.setattr(m07.demo, "policy", boom)
    with pytest.raises(RuntimeError):
        m07.demo.respond("Rayan", "How many days a week can I work remotely?", outage=True)
    assert m07.rag.client is live


# ---------------------------------------------------------------- the hand-off summary and the data files

def test_every_hand_off_has_the_same_fields(m07):
    asked = ["What is the status of ticket 4472?", "What is on the cafeteria menu today?", "Please reset my password",
             "Who pays for a new laptop, and how long does it take?"]
    for sentence in asked:
        _, reply = m07.demo.respond("Rayan", sentence)
        assert set(reply.handoff) == {"user", "asked", "route", "reason", "retrieved"}
        assert reply.handoff["user"] == "Rayan" and reply.handoff["asked"] == sentence


def test_the_demo_script_is_well_formed():
    script = json.loads((DATA / "m07_demo_script.json").read_text(encoding="utf-8"))
    assert [s["id"] for s in script] == [f"D{i}" for i in range(1, len(script) + 1)]       # D, not S: S01 to S12 are Module 6's eval cases
    for s in script:
        assert {"id", "title", "user", "say", "kind", "contains", "handoff", "reqs"} <= set(s) and s["kind"] in KINDS and s["reqs"]
    assert sum("FAILURE" in s["title"] for s in script) >= 2              # a script that never fails shows nothing
    assert any(s.get("outage") for s in script)


def test_the_lab_playbook_uses_only_keys_the_mock_understands():
    pb = json.loads((KIT / "playbooks" / "m07_lab.json").read_text(encoding="utf-8"))
    allowed = {"system_contains", "user_contains", "user_regex", "has_tool_result", "tool_result_contains", "tools_include", "model_contains", "turn"}
    assert pb["rules"] and all(set(r["when"]) <= allowed and "reply" in r for r in pb["rules"])


def test_every_scenario_traces_to_a_requirement_that_exists_in_the_module_6_specification():
    spec = DATA / "m06_spec_worked.md"
    if not spec.exists():
        pytest.skip("the Module 6 worked specification is not in this checkout")
    known = set(re.findall(r"\b(?:FR|GR|NFR|AC)-\d+\b", spec.read_text(encoding="utf-8")))
    script = json.loads((DATA / "m07_demo_script.json").read_text(encoding="utf-8"))
    for s in script:
        assert set(s["reqs"]) <= known, (s["id"], set(s["reqs"]) - known)
    assert "AC-2" in next(s for s in script if s["id"] == "D3")["reqs"]       # someone else's ticket is the spec's AC-2


def test_the_declined_reply_says_what_najm_desk_can_do_as_the_specification_asks(m07):
    _, reply = m07.demo.respond("Rayan", "Please reset my password")
    assert "answers policy questions and shows ticket status" in reply.text
