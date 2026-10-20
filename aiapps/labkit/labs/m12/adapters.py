# labs/m12/adapters.py
"""Lab 12.2: the three agents under test, behind one shape. Each adapter calls the agent you built in an earlier module
the way its own command line does, and returns an Output. Nothing in this file judges anything: that is graders.py."""
import contextlib
import hashlib
import io
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

from anthropic.resources.messages import Messages

for lab in ("m02", "m04", "m08"):      # the earlier labs import each other by plain name; append, so this folder wins
    sys.path.append(str(Path(__file__).resolve().parents[1] / lab))
CLASSIFY_PROMPT = os.environ.get("CLASSIFY_PROMPT", "classify_v3")     # the prompt file under test (Module 2)


@dataclass
class Output:
    text: str = ""                                  # what the user would see: a label, an answer, a reply
    tools: list = field(default_factory=list)       # [(tool name, input dict)] in the order the agent called them
    steps: int = 0                                  # model calls the agent made
    reason: str = "done"                            # how the run ended: done, no_progress, token_budget...
    retrieved: list = field(default_factory=list)   # chunk ids the policy agent was shown
    evidence: str = ""                              # the text of those chunks: what a judge needs to check a claim


class Meter:
    """Counts every Messages.create call made while it is open: calls and tokens. It patches the SDK class, so the
    agents stay untouched (you rarely own the code of every agent you must evaluate)."""

    def __enter__(self):
        self.calls = self.tokens_in = self.tokens_out = 0
        self._create, meter = Messages.create, self

        def create(this, *args, **kwargs):
            resp = meter._create(this, *args, **kwargs)
            meter.calls += 1
            meter.tokens_in += resp.usage.input_tokens
            meter.tokens_out += resp.usage.output_tokens
            return resp
        Messages.create = create
        return self

    def __exit__(self, *exc):
        Messages.create = self._create


def classifier(text: str) -> Output:
    from classify import classify                    # labs/m02: imported on first use, so --only skips what it does not run
    return Output(text=classify(text, CLASSIFY_PROMPT).label, steps=1)


def policy(question: str) -> Output:
    import bm25, rag                                 # labs/m04: the hybrid search and the cited answer
    with contextlib.redirect_stderr(io.StringIO()):  # rag.ask logs one JSON line per question; the results file keeps ours
        answer, hits = rag.ask(question, 3, bm25.hybrid_search)
    return Output(text=answer, steps=1 if hits else 0, retrieved=[h["id"] for h in hits],
                  evidence="\n".join(h["text"] for h in hits))


def ticket(goal: str) -> Output:
    import agent_loop                                # labs/m08: the guarded loop; its trace is the trajectory
    trace = agent_loop.Trace()
    res = agent_loop.run(goal, trace=trace)
    if res.reason == "model_error":                  # the API failed after the SDK's retries: plumbing, not a wrong answer
        raise RuntimeError(res.handoff["why"])       # so the runner records an error, never a failed case
    calls = [(e["tool"], e["input"]) for e in trace.events if e["event"] == "tool" and "refused" not in e]
    return Output(text=res.answer, tools=calls, steps=res.steps, reason=res.reason)


AGENTS = {"classifier": classifier, "policy": policy, "ticket": ticket}


def versions(agents) -> dict:
    """What was under test: change any of these and the score is not comparable until you say so."""
    sha = lambda s: hashlib.sha256(s.encode()).hexdigest()[:8]
    v = {"model": os.environ.get("MODEL", "claude-sonnet-5-5")}
    if "classifier" in agents:
        from promptfile import load_prompt
        v["classify_prompt"] = load_prompt(CLASSIFY_PROMPT).version
    if "policy" in agents:
        import rag
        v["policy_prompt"] = sha(rag.SYSTEM)
    if "ticket" in agents:
        import agent_loop
        v["ticket_agent"] = sha(agent_loop.SYSTEM + json.dumps(agent_loop.DEFINITIONS))
    return v


def prompt_examples() -> set:
    """Tickets quoted as examples inside the classify prompt. An eval input that is also an example is a leaked answer."""
    from promptfile import load_prompt
    return {e.lower() for e in re.findall(r'^Example: "(.+?)" =>', load_prompt(CLASSIFY_PROMPT).text, re.M)}


def timed(agent: str, text: str):
    """Run one adapter; returns (Output, Meter, milliseconds)."""
    with Meter() as meter:
        t0 = time.perf_counter()
        out = AGENTS[agent](text)
    return out, meter, round((time.perf_counter() - t0) * 1000)
