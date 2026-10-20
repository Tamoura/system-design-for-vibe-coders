# labs/m07/demo.py
"""Lab 7.2: the thin-slice Najm Desk demo: policy Q&A and ticket status, three guards, a degraded mode, one hand-off.
  python labs/m07/demo.py                                run the seven scenarios in labkit/data/m07_demo_script.json
  python labs/m07/demo.py "Who approves a laptop?" Rayan      one question, asked by one person
Reuses Module 4 and the kit's ticket tool. The router is plain keywords on purpose: a thin slice proves the shape;
the real router is a cheap-model call (ADR 001)."""
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import anthropic

KIT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(KIT), str(KIT / "labs" / "m04")]            # the kit and the Module 4 lab, by plain name
import rag                                                       # noqa: E402  Module 4: Chroma index, answer(), IDK
from bm25 import hybrid_search                                   # noqa: E402  Module 4: vector + BM25 fused
from labkit.tools import get_ticket_status                       # noqa: E402  the kit's read-only ticket tool

DATA = KIT / "labkit" / "data"
OWNERS = json.loads((DATA / "m07_requesters.json").read_text(encoding="utf-8"))     # ticket id -> who raised it


@dataclass
class Reply:
    kind: str                       # answer | status | idk | refused | declined | withheld | degraded
    text: str                       # exactly what the customer sees
    handoff: dict | None = None     # what a Service Desk agent receives


def hand_off(user, text, route_name, reason, hits=()):
    """Who asked, what, why the assistant stopped, and what it had retrieved."""
    return {"user": user, "asked": text, "route": route_name, "reason": reason, "retrieved": [h["id"] for h in hits]}


def route(text: str) -> str:
    low = text.lower()
    if re.match(r"(please |can you |could you )?(reset|unlock|change|disable)\b", low):
        return "action"                                          # a request to DO something: not in v1
    if re.search(r"\b\d{4}\b", low) and re.search(r"ticket|status|case", low):
        return "ticket"
    return "policy"


def policy(user: str, text: str) -> Reply:
    hits = hybrid_search(text, 3)
    try:
        answer = rag.answer(text, hits)                          # no hits: the Module 4 "I don't know", no model call
    except anthropic.APIError:                                   # degraded mode: the best passage, no generation
        return Reply("degraded", f"The assistant is offline, so this is the closest policy text, not an answer: {hits[0]['text']} [{hits[0]['id']}]",
                     hand_off(user, text, "policy", "model unavailable", hits))
    if answer.strip() == rag.IDK:
        return Reply("idk", f"{rag.IDK} I have passed your question to the Service Desk.", hand_off(user, text, "policy", "no answer in the library", hits))
    unknown = rag.check_citations(answer, hits)
    if unknown or not re.search(r"\[[\w-]+#\d+\]", answer):      # gate: cite, and only what was retrieved
        return Reply("withheld", "I could not verify that answer against the policies, so I am not showing it. A person will follow up.",
                     hand_off(user, text, "policy", f"citation gate: {unknown or 'no citation'}", hits))
    return Reply("answer", answer)


def ticket(user: str, text: str) -> Reply:
    ticket_id = re.search(r"\b\d{4}\b", text).group(0)
    if OWNERS.get(ticket_id) != user:                            # same words for 'not yours' and 'does not exist'
        return Reply("refused", f"I can't find a ticket {ticket_id} raised by you.", hand_off(user, text, "ticket", "not the requester's ticket"))
    return Reply("status", get_ticket_status(ticket_id))         # a stored record needs no model to be shown


def respond(user: str, text: str, outage: bool = False) -> tuple[str, Reply]:
    name = route(text)
    if name == "action":
        return name, Reply("declined", "That is outside this version of Najm Desk, which answers policy questions and shows ticket status. "
                           "I have asked the Service Desk to help.", hand_off(user, text, name, "action not in scope"))
    if name == "ticket":
        return name, ticket(user, text)
    live = rag.client
    if outage:                                                   # the fire drill: point the client at a dead port, no retries
        rag.client = live.with_options(base_url="http://127.0.0.1:1", max_retries=0)
    try:
        return name, policy(user, text)
    finally:
        rag.client = live                                        # always put the real client back


def run_script(path: Path = DATA / "m07_demo_script.json") -> bool:
    results = []
    for s in json.loads(path.read_text(encoding="utf-8")):
        name, reply = respond(s["user"], s["say"], s.get("outage", False))
        low, leak = reply.text.lower(), s.get("absent", "").lower()          # "absent": text that must NOT appear (a leak check)
        ok = reply.kind == s["kind"] and s["contains"].lower() in low and bool(reply.handoff) == s["handoff"] and not (leak and leak in low)
        results.append(ok)
        print(f'--- {s["id"]} {s["title"]}\n{s["user"]}> {s["say"]}\nnajm-desk> {reply.text}')
        print(f'    [route={name} kind={reply.kind}] {"PASS" if ok else "FAIL"}   hand-off: {reply.handoff or "none"}')
    print(f"\n{sum(results)}/{len(results)} slice checks passed")
    return all(results)


if __name__ == "__main__":
    if len(sys.argv) > 1:                                        # demo.py "question" [person]
        print(respond(sys.argv[2] if len(sys.argv) > 2 else "Rayan", sys.argv[1])[1].text)
    else:
        sys.exit(0 if run_script() else 1)
