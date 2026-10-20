# labs/m01/agent.py
"""Lab B: your first agent. One tool, a step cap, every stop_reason handled, no framework."""
import os
import sys

from anthropic import Anthropic

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
client = Anthropic()

SYSTEM = "You help IT service desk staff at a bank. Use the tool for questions about tickets."

# 1. Describe the tool. This JSON is ALL the model sees about it: the name, the description, the schema.
TOOLS = [{
    "name": "get_ticket_status",
    "description": "Look up the status of an IT support ticket by its number. Call this whenever the user asks about a ticket.",
    "input_schema": {"type": "object",
                     "properties": {"ticket_id": {"type": "string", "description": "The ticket number, e.g. 4471"}},
                     "required": ["ticket_id"]},
}]


def get_ticket_status(ticket_id: str) -> str:
    """2. The real implementation. Fake data for now; Module 3 connects the kit's tools."""
    fake_db = {"4471": "In progress, assigned to Networks", "4472": "Closed", "4473": "Open"}
    return fake_db.get(ticket_id, f"No ticket {ticket_id} found")


IMPLEMENTATIONS = {"get_ticket_status": get_ticket_status}     # the ONLY things the model can make happen


def text_of(resp) -> str:
    return next((b.text for b in resp.content if b.type == "text"), "")


def run_tools(blocks) -> list[dict]:
    """YOUR code disposes. Permission checks, approvals and audit logs all go here, in this gap."""
    results = []
    for block in blocks:
        if block.type != "tool_use":
            continue
        print(f"  model proposes {block.name}({block.input})")
        try:
            fn = IMPLEMENTATIONS.get(block.name)
            if fn is None:
                raise LookupError(f"unknown tool {block.name!r}")
            result = {"type": "tool_result", "tool_use_id": block.id, "content": fn(**block.input)}
        except Exception as e:     # a failing tool must not crash the loop: report it to the model instead
            result = {"type": "tool_result", "tool_use_id": block.id, "content": f"Error: {e}", "is_error": True}
        results.append(result)     # every tool_use id needs a tool_result, or the next call is a 400
    return results


def run_agent(goal: str, max_steps: int = 5, max_tokens: int = 1024, tools: list = TOOLS) -> str:
    messages = [{"role": "user", "content": goal}]
    for step in range(1, max_steps + 1):                                  # 3. ALWAYS cap the loop
        resp = client.messages.create(model=MODEL, max_tokens=max_tokens, output_config={"effort": "low"},
                                      system=SYSTEM, tools=tools, messages=messages)
        print(f"[step {step}] stop_reason={resp.stop_reason} in={resp.usage.input_tokens} out={resp.usage.output_tokens}")
        messages.append({"role": "assistant", "content": resp.content})  # 4. the WHOLE content list, not just the text
        if resp.stop_reason == "end_turn":                                # 5a. final answer
            return text_of(resp) or "Stopped: the model returned no text."
        if resp.stop_reason == "tool_use":                                # 5b. the model asked; your code answers
            messages.append({"role": "user", "content": run_tools(resp.content)})   # ONE message, ALL the results
        elif resp.stop_reason == "pause_turn":                            # 5c. paused mid-turn: send it back to resume
            continue
        elif resp.stop_reason == "max_tokens":                            # 5d. cut off: never run a half-written call
            return f"Stopped: reply cut off at max_tokens={max_tokens}. {text_of(resp)}".strip()
        else:                                                             # 5e. refusal, model_context_window_exceeded, stop_sequence, or a future value
            return f"Stopped: stop_reason={resp.stop_reason} {resp.stop_details or ''}".strip()
    return f"Stopped: step cap of {max_steps} reached."                   # 6. the guard fired


if __name__ == "__main__":
    print(run_agent(" ".join(sys.argv[1:]) or "Is ticket 4471 done yet? And what about 4472?"))
