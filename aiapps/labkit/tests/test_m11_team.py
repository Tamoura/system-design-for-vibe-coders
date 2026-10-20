"""Tests for the Module 11 lab files (labs/m11): the hand-off contracts, the supervisor, the guards and the team-versus-solo comparison.

They run against the offline mock with the lab's own playbook (playbooks/m11_lab.json), which SCRIPTS what each role says. So they
prove the mechanics (validation at every hand-off, role permissions, caps, escalation, accounting) and say nothing about whether a
real model researches, writes or reviews well."""
import importlib
import json
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
LABS = KIT / "labs" / "m11"
LAPTOP = "How do I request a new laptop?"
P2 = "What is the response time for a P2 ticket?"
HOURS = "When is the Service Desk open?"


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def lab_url():
    app = mock_server.create_app(str(KIT / "playbooks" / "m11_lab.json"))
    port = free_port()
    srv = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error"))
    threading.Thread(target=srv.run, daemon=True).start()
    for _ in range(100):
        if srv.started:
            break
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}"
    srv.should_exit = True


@pytest.fixture(scope="module")
def lab():
    """The lab files import each other by plain name, so put their folder on the path while they are loaded."""
    names = ("contracts", "team", "compare")
    saved = {n: sys.modules.pop(n, None) for n in names}
    sys.path.insert(0, str(LABS))
    try:
        yield SimpleNamespace(**{n: importlib.import_module(n) for n in names})
    finally:
        sys.path.remove(str(LABS))
        for n in names:
            sys.modules.pop(n, None)
            if saved[n]:
                sys.modules[n] = saved[n]


class Spy:
    """Wraps the real SDK client and records every request the team sends."""

    def __init__(self, inner):
        self.messages, self.calls = SimpleNamespace(create=self.create), []
        self.inner = inner

    def create(self, **kw):
        self.calls.append(json.loads(json.dumps(kw, default=lambda o: o.model_dump())))
        return self.inner.messages.create(**kw)

    def roles(self):
        return [c["system"].split(".")[0].replace("ROLE: ", "") for c in self.calls]


def scripted(*steps):
    """A fake client that plays back fixed replies: a str is a final text, a dict is a tool_use of search_policies."""
    it = iter(steps)

    def create(**kw):
        step = next(it)
        block = SimpleNamespace(type="text", text=step) if isinstance(step, str) else SimpleNamespace(
            type="tool_use", id="toolu_fake", name="search_policies", input=step)
        return SimpleNamespace(content=[block], stop_reason="end_turn" if isinstance(step, str) else "tool_use",
                               usage=SimpleNamespace(input_tokens=10, output_tokens=5), _request_id="req_fake")
    return SimpleNamespace(messages=SimpleNamespace(create=create))


@pytest.fixture
def client(lab_url):
    return anthropic.Anthropic(base_url=lab_url, api_key="mock", max_retries=0)


def events(team, name):
    return [e for e in team.events if e["event"] == name]


# ------------------------------------------------------------------ the playbook

def test_every_scripted_quote_is_word_for_word_in_the_policies_except_the_planted_one():
    rules = json.loads((KIT / "playbooks" / "m11_lab.json").read_text(encoding="utf-8"))["rules"]
    policies = {p.stem: " ".join(p.read_text(encoding="utf-8").split()) for p in (KIT / "labkit" / "data" / "policies").glob("*.md")}
    quotes = [(f["source"], f["quote"]) for r in rules for f in r["reply"].get("json", {}).get("findings", [])]
    assert len(quotes) >= 8
    invented = {q for source, q in quotes if q not in policies[source]}
    assert invented == {"Laptops are delivered within 1 business day, no approval needed."}      # the [drill:fabricate] lie


# ------------------------------------------------------------------ the contracts

def test_contracts_reject_what_was_not_agreed(lab):
    c = lab.contracts
    with pytest.raises(ValueError, match="at least 1 item"):
        c.Draft(answer="A perfectly good answer.", citations=[])
    with pytest.raises(ValueError, match="at least one issue"):
        c.Review(verdict="revise", issues=[])
    with pytest.raises(ValueError, match="Extra inputs"):
        c.Review(verdict="approve", issues=[], mood="happy")
    with pytest.raises(ValueError):
        c.Review(verdict="maybe", issues=[])
    with pytest.raises(ValueError):
        c.Finding(source="Laptop Requests", quote="Staff can request a new laptop.")
    with pytest.raises(ValueError):
        c.Brief(question="short")
    assert c.Review(verdict="approve", issues=[]).verdict == "approve"


def test_a_schema_cannot_hold_grounding_so_code_checks_it(lab):
    c = lab.contracts
    seen = {"mfa": "A lost phone must be reported to the Service  Desk immediately."}
    good = c.Notes(findings=[c.Finding(source="mfa", quote="A lost phone must be reported to the Service Desk")], gaps=[])
    c.check_notes(good, seen)                                           # whitespace differences do not matter
    invented = c.Notes(findings=[c.Finding(source="mfa", quote="A lost phone can wait until Monday morning.")], gaps=[])
    with pytest.raises(ValueError, match="word for word"):
        c.check_notes(invented, seen)
    unseen = c.Notes(findings=[c.Finding(source="vpn", quote="The corporate VPN is required outside offices.")], gaps=[])
    with pytest.raises(ValueError, match="word for word"):
        c.check_notes(unseen, seen)                                     # a source the tool never returned has nothing to quote from
    with pytest.raises(ValueError, match="not among the sources"):
        c.check_citations(c.Draft(answer="Report the lost phone at once.", citations=["mfa", "vpn"]), {"mfa"})
    c.check_citations(c.Draft(answer="Report the lost phone at once.", citations=["mfa"]), {"mfa"})


def test_a_quote_from_a_later_line_of_a_policy_is_still_grounded(lab, client, monkeypatch, tmp_path):
    """The kit's policies are one line each; a real policy has several. The record of what search returned must hold all of it."""
    (tmp_path / "vpn-abroad.md").write_text("# VPN abroad\nStaff travelling abroad must use the corporate VPN.\nReport a lost token to the Service Desk.\n", encoding="utf-8")
    monkeypatch.setattr(lab.team, "POLICIES", tmp_path)
    t = lab.team.Team(LAPTOP, client=client)
    t.tool("researcher", "search_policies", {"query": "staff travelling abroad corporate VPN"})
    c = lab.contracts
    c.check_notes(c.Notes(findings=[c.Finding(source="vpn-abroad", quote="Report a lost token to the Service Desk.")], gaps=[]), t.seen)
    with pytest.raises(ValueError, match="word for word"):
        c.check_notes(c.Notes(findings=[c.Finding(source="vpn-abroad", quote="Report a lost token to nobody at all.")], gaps=[]), t.seen)


def test_search_policies_returns_ids_and_admits_silence(lab):
    out = lab.team.search_policies(LAPTOP)
    assert "[laptop-requests]" in out and "Hardware > New device" in out
    assert lab.team.search_policies("Can I bring my own laptop to work?").endswith("No policies matched.")


# ------------------------------------------------------------------ the team

def test_the_happy_path_validates_every_hand_off(lab, client):
    t = lab.team.Team(LAPTOP, client=client)
    r = t.run()
    assert r.ok and r.reason == "done" and r.citations == ["laptop-requests"] and "Hardware > New device" in r.answer
    assert r.calls == 4 and set(t.by_role) == {"researcher", "writer", "reviewer"} and t.by_role["researcher"][0] == 2
    assert [(e["agent"], e["contract"]) for e in events(t, "handoff")] == [("researcher", "Notes"), ("writer", "Draft"), ("reviewer", "Review")]
    assert t.tokens == sum(v[1] + v[2] for v in t.by_role.values()) == r.tokens
    assert t.events[-1]["event"] == "stop" and t.events[-1]["handoff"] is None


def test_the_reviewer_loop_catches_a_wrong_draft_and_the_second_draft_wins(lab, client):
    t = lab.team.Team(P2, client=client)
    r = t.run()
    assert r.ok and "within 4 hours" in r.answer and "2 hours" not in r.answer
    assert [(e["round"], e["verdict"]) for e in events(t, "review")] == [(1, "revise"), (2, "approve")]
    assert r.calls == 6 and t.by_role["writer"][0] == 2 and t.by_role["reviewer"][0] == 2


def test_a_broken_contract_gets_one_repair(lab, client):
    t = lab.team.Team(HOURS, client=client)
    r = t.run()
    broken = events(t, "contract_broken")
    assert r.ok and r.calls == 5 and len(broken) == 1
    assert broken[0]["agent"] == "writer" and "citations" in broken[0]["problem"]
    assert "7:00 to 17:00" in r.answer


def test_a_reviewer_who_never_approves_hits_the_round_cap(lab, client):
    t = lab.team.Team(LAPTOP + " [drill:never-approve]", client=client)
    r = t.run()
    assert not r.ok and r.reason == "max_rounds" and r.calls == 6
    assert r.packet["last_draft"]["citations"] == ["laptop-requests"] and r.packet["last_issues"] == ["The draft is not specific enough."]
    assert "ref " + t.run_id in r.answer                                # the person is told whom to ask about
    assert lab.team.Team(P2, client=client, max_rounds=1).run().reason == "max_rounds"       # the cap is a parameter


def test_a_fabricated_quote_never_reaches_the_writer(lab, client):
    t = lab.team.Team(LAPTOP + " [drill:fabricate]", client=client)
    r = t.run()
    assert not r.ok and r.reason == "contract" and "twice" in r.packet["why"]
    assert "writer" not in t.by_role and r.calls == 3                   # search, notes, one repair: then a person
    assert len(events(t, "contract_broken")) == 2


def test_a_draft_that_cites_an_unknown_source_is_repaired_once_then_escalated(lab):
    notes = '{"findings": [{"source": "laptop-requests", "quote": "Staff can request a new laptop through the IT Service Desk portal"}], "gaps": []}'
    stray = '{"answer": "Ask your manager; see the remote work policy.", "citations": ["remote-work"]}'
    t = lab.team.Team(LAPTOP, client=scripted({"query": LAPTOP}, notes, stray, stray))
    r = t.run()
    assert r.reason == "contract" and "writer" in r.packet["why"] and "remote-work" in r.packet["why"]
    assert t.by_role["writer"][0] == 2 and "reviewer" not in t.by_role         # a bad draft never reaches the reviewer


def test_the_token_budget_is_checked_before_each_call(lab, client):
    t = lab.team.Team(LAPTOP, client=client, budget=300)
    r = t.run()
    assert r.reason == "token_budget" and r.calls == 2 and "writer" not in t.by_role
    assert r.tokens > 300                                               # the cap is checked BEFORE a call, so one call can overshoot it
    assert lab.team.Team(LAPTOP, client=client, budget=1).run().calls == 1


def test_no_sources_stops_the_team_before_the_writer(lab, client):
    t = lab.team.Team("Can I bring my own laptop to work?", client=client)
    r = t.run()
    assert r.reason == "no_sources" and r.calls == 2 and set(t.by_role) == {"researcher"}
    assert "No policy" in r.packet["why"]


def test_a_bad_question_fails_the_brief_without_any_model_call(lab, client):
    t = lab.team.Team("short", client=client)
    r = t.run()
    assert r.reason == "bad_brief" and r.calls == 0 and "at least 10 characters" in r.packet["why"]


def test_an_agent_that_never_finishes_hits_the_step_cap(lab, client):
    t = lab.team.Team(LAPTOP + " [mock:loop]", client=client)
    r = t.run()
    assert r.reason == "step_cap" and r.calls == lab.team.STEPS == t.by_role["researcher"][0]


def test_model_errors_end_in_a_hand_off_not_a_crash(lab, client):
    r = lab.team.Team(LAPTOP + " [mock:ratelimit]", client=client).run()           # the client here has max_retries=0
    assert r.reason == "model_error" and "RateLimitError" in r.packet["why"] and r.calls == 0


@pytest.mark.parametrize("stop", ["max_tokens", "refusal", "pause_turn"])
def test_stop_reasons_that_carry_no_contract_escalate(lab, stop):
    class Fake:
        messages = SimpleNamespace(create=lambda **kw: SimpleNamespace(
            content=[], stop_reason=stop, usage=SimpleNamespace(input_tokens=5, output_tokens=1), _request_id="req_fake"))
    r = lab.team.Team(LAPTOP, client=Fake()).run()
    assert r.reason == "stop_reason" and stop in r.packet["why"]


# ------------------------------------------------------------------ permissions and isolation

def test_tool_permissions_are_enforced_by_code_not_by_the_prompt(lab, client):
    t = lab.team.Team(LAPTOP, client=client)
    msg, bad = t.tool("writer", "search_policies", {"query": "laptop request"})
    assert bad and "not available to the writer" in msg and t.seen == {}
    assert t.tool("reviewer", "search_policies", {"query": "laptop request"})[1]
    assert t.tool("researcher", "create_ticket", {})[1] and t.seen == {}
    out, bad = t.tool("researcher", "search_policies", {"query": "laptop request"})
    assert not bad and "laptop-requests" in t.seen
    assert {r: sorted(spec[1]) for r, spec in lab.team.ROLES.items()} == {
        "researcher": ["search_policies"], "writer": [], "reviewer": [], "solo": ["search_policies"]}


def test_a_writer_that_reaches_for_a_tool_is_refused_and_the_run_continues(lab, client):
    t = lab.team.Team(LAPTOP + " [drill:overreach]", client=client)
    r = t.run()
    assert r.ok and r.calls == 5
    assert [(e["agent"], e["tool"]) for e in events(t, "tool_refused")] == [("writer", "search_policies")]
    assert [e["agent"] for e in events(t, "tool")] == ["researcher"]


def test_a_refused_tool_call_goes_back_to_the_model_as_an_error_result(lab, lab_url):
    spy = Spy(anthropic.Anthropic(base_url=lab_url, api_key="mock", max_retries=0))
    r = lab.team.Team(LAPTOP + " [drill:overreach]", client=spy).run()
    writer = [c for c in spy.calls if c["system"].startswith("ROLE: writer")]
    assert r.ok and len(writer) == 2
    result = writer[1]["messages"][-1]["content"][0]                 # the writer's second request ends with the refusal
    assert result["type"] == "tool_result" and result["is_error"] is True and "not available to the writer" in result["content"]


def test_each_agent_sees_only_its_own_contract_and_the_requests_follow_the_api_rules(lab, lab_url):
    spy = Spy(anthropic.Anthropic(base_url=lab_url, api_key="mock", max_retries=0))
    r = lab.team.Team(LAPTOP, client=spy).run()
    assert r.ok and spy.roles() == ["researcher", "researcher", "writer", "reviewer"]
    blob = [json.dumps(c["messages"]) for c in spy.calls]
    assert "Results for" not in blob[2] and "Results for" not in blob[3]       # context isolation: raw search results stay with the researcher
    assert "high-spec" not in blob[2] and "high-spec" not in blob[3]            # ...and so do the policy sentences nobody quoted
    assert "Hardware > New device" in blob[2] and "NOTES" in blob[3] and "DRAFT" in blob[3]
    assert all("ROLE: researcher" not in json.dumps(c["system"]) for c in spy.calls[2:])
    for c in spy.calls:
        assert c["model"] == lab.team.MODEL and c["max_tokens"] >= 1024
        assert not {"temperature", "top_p", "top_k", "tool_choice"} & set(c)             # sampling and forced tools are rejected by current models
        assert c["output_config"]["effort"] == "low" and c["output_config"]["format"]["type"] == "json_schema"
    assert ["tools" in c for c in spy.calls] == [True, True, False, False]              # only the researcher is given a tool


def test_the_trace_is_one_json_object_per_line(lab, client, tmp_path):
    path = tmp_path / "trace.jsonl"
    t = lab.team.Team(P2, client=client, trace_file=str(path))
    t.run()
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == len(t.events) and {r["run"] for r in rows} == {t.run_id}
    assert [r["seq"] for r in rows] == list(range(1, len(rows) + 1)) and rows[-1]["event"] == "stop"
    assert all(r["request_id"].startswith("req_") for r in rows if r["event"] == "model")


# ------------------------------------------------------------------ the comparison

def test_solo_answers_in_two_calls(lab, client):
    t = lab.team.Team(LAPTOP, client=client)
    r = t.run_solo()
    assert r.ok and r.calls == 2 and set(t.by_role) == {"solo"} and r.citations == ["laptop-requests"]


def test_the_team_costs_more_than_one_agent_on_every_task(lab, client):
    for question, expect in lab.compare.TASKS:
        team, solo = lab.team.Team(question, client=client), lab.team.Team(question, client=client)
        a, b = team.run(), solo.run_solo()
        assert a.ok and b.ok and expect in a.answer and expect in b.answer
        assert a.calls > b.calls and a.tokens > b.tokens


def test_compare_prints_a_table_and_the_ratios(lab, lab_url, capsys, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_BASE_URL", lab_url)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock")
    monkeypatch.setattr(lab.compare, "PRICE", [3.0, 15.0])
    lab.compare.compare()
    out = capsys.readouterr().out
    assert out.count(" right ") == 10 and "wrong" not in out
    assert "team / solo: calls x" in out and "tokens x" in out and out.count(", cost 0.") == 2


def test_command_lines_run_end_to_end(lab_url, tmp_path):
    env = {"ANTHROPIC_BASE_URL": lab_url, "ANTHROPIC_API_KEY": "mock", "PATH": "/usr/bin:/bin", "TRACE_FILE": str(tmp_path / "trace.jsonl")}
    for args, expect in ((["team.py", HOURS], "service-desk-hours"), (["compare.py"], "team / solo")):
        out = subprocess.run([sys.executable, str(LABS / args[0]), *args[1:]], capture_output=True, text=True, env=env, cwd=tmp_path, timeout=60)
        assert out.returncode == 0 and expect in out.stdout, out.stderr
