# labs/m08/agent_loop.py
"""Lab 8.2: an agent loop from scratch: four guards, every stop_reason, a JSONL trace, a hand-off.
  python labs/m08/agent_loop.py "Is ticket 4471 done yet?"
  environment: MAX_STEPS, TOKEN_BUDGET, TIMEOUT_S, TRACE_FILE"""
import json
import os
import re
import sys
import time
import uuid
from collections import Counter, namedtuple
from dataclasses import asdict, dataclass
from pathlib import Path

import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labkit.tools import get_ticket_status, lookup_employee  # noqa: E402  fake, read-only tools

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
SYSTEM = ("You help IT service desk staff. "
          "Use the tools for tickets and colleagues; never guess them.")
TOOLS = {   # name -> (description, its one argument, function): all the model can make happen
    "get_ticket_status": (
        "Look up one IT ticket by number. Call this whenever asked about a ticket.",
        "ticket_id", get_ticket_status),
    "lookup_employee": (
        "Look up a colleague by first name: team and email. "
        "Call this for any question about a colleague.",
        "name", lookup_employee),
}


def definition(name, description, key):
    """What the model sees of one tool: name, description, one required string argument."""
    schema = {"type": "object", "properties": {key: {"type": "string"}}, "required": [key]}
    return {"name": name, "description": description, "input_schema": schema}


DEFINITIONS = [definition(n, d, k) for n, (d, k, _) in TOOLS.items()]


@dataclass(frozen=True)
class Limits:                                    # every number is a decision
    max_steps: int = int(os.environ.get("MAX_STEPS", 6))             # guard 1: model calls
    token_budget: int = int(os.environ.get("TOKEN_BUDGET", 25_000))  # guard 2: tokens, all calls
    timeout_s: float = float(os.environ.get("TIMEOUT_S", 30))        # guard 3: clock, whole run
    max_repeats: int = 2                         # guard 4: same call this often = no progress
    result_chars: int = 2_000                    # most a tool result may add to the context


# A namedtuple is a tuple with named fields: res.ok, res.reason... handoff is what a person receives
Result = namedtuple("Result", "ok reason answer steps tokens handoff")


class Trace:
    """One JSON object per line. Strings are clipped: tool output can hold personal data."""

    def __init__(self, path=None):
        self.path, self.run_id, self.events = path, uuid.uuid4().hex[:8], []

    def log(self, event, **fields):
        fields = {k: v[:300] if isinstance(v, str) else v for k, v in fields.items()}
        head = {"run": self.run_id, "seq": len(self.events) + 1, "ts": round(time.time(), 3)}
        self.events.append({**head, "event": event, **fields})
        if self.path:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(self.events[-1], ensure_ascii=False, default=str) + "\n")


def ms(since):
    return round((time.monotonic() - since) * 1000)


def run_tool(name, args):
    """The gap: the model proposes, this function disposes. Never raises: every outcome is text."""
    if name not in TOOLS:
        return f"unknown tool {name!r}; the tools are: {', '.join(TOOLS)}", True
    _, key, fn = TOOLS[name]
    if set(args) != {key} or not isinstance(args[key], str):
        got = json.dumps(args)[:80]
        return f"{name} takes exactly one string argument named {key!r}; got {got}", True
    try:
        return str(fn(args[key])), False
    except Exception as e:                       # a raising tool must not end the run
        return f"{name} failed: {e}", True


def mentions_every_ticket(goal, answer):
    """A completion check in plain code. Returns a problem, or None."""
    missing = [t for t in re.findall(r"\b\d{4}\b", goal) if t not in answer]
    return f"the answer never mentions {', '.join(missing)}" if missing else None


def run(goal, lim=Limits(), client=None, trace=None, check=None):
    client = client or anthropic.Anthropic(timeout=30.0)    # the SDK retries transient errors twice
    trace = trace or Trace()
    t0, spent, last_in, seen = time.monotonic(), 0, 0, Counter()
    messages = [{"role": "user", "content": goal}]
    trace.log("start", goal=goal, model=MODEL, **asdict(lim))

    def stop(reason, step, text="", why=""):     # the only exit: one "stop" line per run
        ok, secs = reason == "done", round(time.monotonic() - t0, 1)
        keys = ("step", "tool", "input", "result", "refused")
        tried = [{k: e[k] for k in keys if k in e} for e in trace.events if e["event"] == "tool"]
        packet = None if ok else {"run": trace.run_id, "reason": reason, "why": why, "goal": goal,
                                  "steps": step, "tokens": spent, "seconds": secs,
                                  "tried": tried, "last_text": text[:300]}
        trace.log("stop", step=step, reason=reason, why=why, tokens=spent, seconds=secs,
                  answer=text, handoff=packet)
        sorry = (f"I could not finish this ({reason}). I passed it to the Service Desk "
                 f"with everything I tried: ref {trace.run_id}.")
        return Result(ok, reason, text if ok else sorry, step, spent, packet)

    for step in range(1, lim.max_steps + 1):                 # guard 1: the hard cap
        if time.monotonic() - t0 > lim.timeout_s:             # guard 3: before every call
            return stop("timeout", step - 1, why=f"more than {lim.timeout_s} s on the clock")
        if spent + last_in > lim.token_budget:                # guard 2: the next call re-sends this
            why = f"{spent} spent, and the next call needs {last_in}+ of {lim.token_budget}"
            return stop("token_budget", step - 1, why=why)
        t1 = time.monotonic()
        try:
            resp = client.messages.create(model=MODEL, max_tokens=1024,
                                          output_config={"effort": "low"},
                                          system=SYSTEM, tools=DEFINITIONS, messages=messages)
        except anthropic.APIError as e:                   # the SDK's retries are spent: hand off
            trace.log("model_error", step=step, error=type(e).__name__,
                      status=getattr(e, "status_code", None), ms=ms(t1))
            return stop("model_error", step - 1, why=f"{type(e).__name__} after the SDK's retries")
        used = resp.usage
        last_in, spent = used.input_tokens, spent + used.input_tokens + used.output_tokens
        trace.log("model", step=step, stop_reason=resp.stop_reason, input_tokens=used.input_tokens,
                  output_tokens=used.output_tokens, total_tokens=spent, ms=ms(t1),
                  request_id=resp._request_id)
        messages.append({"role": "assistant", "content": resp.content})   # the WHOLE content list
        text = next((b.text for b in resp.content if b.type == "text"), "")
        if resp.stop_reason == "end_turn":
            if not text.strip():
                return stop("empty_answer", step, why="end_turn with no text: a silent give-up")
            problem = check(goal, text) if check else None    # "done" needs the code to agree
            return stop("failed_check" if problem else "done", step, text, why=problem or "")
        if resp.stop_reason == "pause_turn":              # paused: send it back; the cap counts it
            continue
        if resp.stop_reason != "tool_use":                    # max_tokens, refusal, or a new value
            known = resp.stop_reason in ("max_tokens", "refusal")
            why = f"stop_reason={resp.stop_reason} {resp.stop_details or ''}".strip()
            return stop(resp.stop_reason if known else "unknown_stop", step, text, why=why)
        results = []                                      # cut-off and refused turns never get here
        for block in (b for b in resp.content if b.type == "tool_use"):
            call = (block.name, json.dumps(block.input, sort_keys=True))
            seen[call] += 1
            if seen[call] >= lim.max_repeats:                 # guard 4: the same call again
                trace.log("tool", step=step, tool=block.name, input=block.input,
                          refused="same call again")
                why = f"{block.name} asked for again with the same input"
                return stop("no_progress", step, text, why=why)
            t2 = time.monotonic()
            out, is_error = run_tool(block.name, block.input)
            trace.log("tool", step=step, tool=block.name, input=block.input, result_chars=len(out),
                      result=out, is_error=is_error, ms=ms(t2))
            shown = out[:lim.result_chars]
            if len(out) > lim.result_chars:
                shown += f" [cut: {len(out)} characters in all]"
            results.append({"type": "tool_result", "tool_use_id": block.id,
                            "content": shown, "is_error": is_error})
        messages.append({"role": "user", "content": results})  # ONE message: a result per tool_use
    why = f"{lim.max_steps} steps used and no final answer"
    return stop("iteration_cap", lim.max_steps, why=why)


if __name__ == "__main__":
    goal = " ".join(sys.argv[1:]) or "Is ticket 4471 done yet? And what about 4472?"
    trace = Trace(os.environ.get("TRACE_FILE", "m08_trace.jsonl"))
    res = run(goal, trace=trace, check=mentions_every_ticket)
    print(res.answer)
    if res.handoff:
        print(json.dumps(res.handoff, indent=2, ensure_ascii=False))
