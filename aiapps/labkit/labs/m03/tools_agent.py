# labs/m03/tools_agent.py
"""Lab 3.2: three tools, a generic tool loop with a step cap, every call traced, every failure returned as is_error."""
import ast
import json
import operator
import os
import sys
import time
from pathlib import Path

from anthropic import Anthropic, transform_schema
from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

from trace import TraceLog      # labs/m03/trace.py: Python puts this script's own folder first on sys.path

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
client = Anthropic()
SYSTEM = "You help IT service desk staff. Use the tools for sums, weather and tickets; never guess them."
TICKETS = json.loads((Path(__file__).resolve().parents[2] / "labkit/data/tickets.json").read_text(encoding="utf-8"))


# 1. Input models: the model's arguments are untrusted input. Validate them, extra fields included.
class ToolInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

class CalcIn(ToolInput):
    expression: str

class WeatherIn(ToolInput):
    city: str

class TicketIn(ToolInput):
    ticket_id: str

    @field_validator("ticket_id")
    @classmethod
    def digits_only(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError(f"must be digits only, like 4471; got {v!r}")
        return v


# 2. The tools are plain functions. A failure is an exception whose message tells the model how to recover.
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow}

def calculator(a: CalcIn) -> str:
    """Never eval() model output: parse it to a syntax tree and walk only the node types we allow."""
    def ev(n):
        if isinstance(n, ast.Constant) and type(n.value) in (int, float):
            return n.value
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return -ev(n.operand)
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            left, right = ev(n.left), ev(n.right)
            if isinstance(n.op, ast.Pow) and (abs(left) > 10**10 or abs(right) > 100):
                raise ValueError("power too large")          # 9**9**9 would keep the process busy for good
            return OPS[type(n.op)](left, right)
        raise ValueError("only numbers, + - * / ** and brackets are allowed")
    return str(ev(ast.parse(a.expression, mode="eval").body))

WEATHER = {"Doha": "39 C, clear", "Dubai": "41 C, humid", "Paris": "17 C, light rain"}      # fake data

def get_weather(a: WeatherIn) -> str:
    if a.city not in WEATHER:
        raise ValueError(f"no forecast for {a.city!r}; known cities: {', '.join(WEATHER)}")
    return f"{a.city}: {WEATHER[a.city]}"

def lookup_ticket(a: TicketIn) -> str:
    ticket = TICKETS.get(a.ticket_id)             # the model supplies a value, never a query
    return json.dumps(ticket, ensure_ascii=False) if ticket else f"No ticket {a.ticket_id} found"

# name -> (description, input model, function): the ONLY things the model can make happen
REGISTRY = {
    "calculator": ("Evaluate an arithmetic expression such as '18 * 52'. Call this for every sum.", CalcIn, calculator),
    "get_weather": ("Get the current weather for one city, e.g. Doha. Call this when asked about the weather.", WeatherIn, get_weather),
    "lookup_ticket": ("Look up one IT ticket by number: status, priority, summary. Call this when asked about a ticket.", TicketIn, lookup_ticket),
}
DEFINITIONS = [{"name": n, "description": d, "strict": True, "input_schema": transform_schema(m)} for n, (d, m, _) in REGISTRY.items()]


# 3. Run ONE tool call. Nothing in here may raise: every outcome becomes text for the model.
def run_tool(name: str, raw_input: dict) -> tuple[str, bool, str]:
    """Returns (text for the model, is_error, kind); kind is ok, unknown_tool, invalid_input or tool_error."""
    if name not in REGISTRY:
        return f"unknown tool {name!r}; available tools: {', '.join(REGISTRY)}", True, "unknown_tool"
    _, model, fn = REGISTRY[name]
    try:
        args = model.model_validate(raw_input)                       # never trust block.input
    except ValidationError as e:
        problems = "; ".join(f"{'.'.join(map(str, x['loc'])) or 'input'}: {x['msg']}" for x in e.errors())
        return f"invalid input for {name}: {problems}", True, "invalid_input"
    try:
        return fn(args), False, "ok"
    except Exception as e:                                           # a tool that raises must not crash the loop
        return f"{name} failed: {e}", True, "tool_error"


# 4. The loop from Module 1, now generic, bounded and traced.
def run_tool_loop(goal: str, max_steps: int = 6, trace: TraceLog | None = None) -> str:
    trace = trace or TraceLog()
    messages = [{"role": "user", "content": goal}]
    for step in range(1, max_steps + 1):                             # the cap: a loop without one is a bill without one
        t0 = time.perf_counter()
        resp = client.messages.create(model=MODEL, max_tokens=1024, output_config={"effort": "low"},
                                      system=SYSTEM, tools=DEFINITIONS, messages=messages)
        trace.log("model_call", step=step, stop_reason=resp.stop_reason, input_tokens=resp.usage.input_tokens,
                  output_tokens=resp.usage.output_tokens, ms=round((time.perf_counter() - t0) * 1000), request_id=resp._request_id)
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":                           # end_turn, max_tokens, refusal: stop and say why
            text = next((b.text for b in resp.content if b.type == "text"), "")
            trace.log("final", step=step, stop_reason=resp.stop_reason, text=text)
            return text if resp.stop_reason == "end_turn" else f"Stopped: stop_reason={resp.stop_reason}"
        results = []
        for block in resp.content:
            if block.type != "tool_use":
                continue
            trace.log("tool_call", step=step, id=block.id, tool=block.name, input=block.input)     # logged BEFORE it runs
            t0 = time.perf_counter()
            text, is_error, kind = run_tool(block.name, block.input)
            trace.log("tool_result", step=step, id=block.id, tool=block.name, kind=kind, is_error=is_error,
                      ms=round((time.perf_counter() - t0) * 1000), output=text)
            results.append({"type": "tool_result", "tool_use_id": block.id, "content": text, "is_error": is_error})
        messages.append({"role": "user", "content": results})        # ONE message, a tool_result for EVERY tool_use id
    trace.log("final", step=max_steps, stop_reason="step_cap", text="")
    return f"Stopped: step cap of {max_steps} reached."


if __name__ == "__main__":
    print(run_tool_loop(" ".join(sys.argv[1:]) or "What is the weather in Doha, and what is 18 * 52?",
                        trace=TraceLog(os.environ.get("TRACE_FILE", "m03_trace.jsonl"))))
