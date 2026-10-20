# labs/m02/ask_policy.py
"""Najm Desk answers a policy question from documents. The prompt is a file; its version is logged on every call.
  PROMPT=najm_desk_v1 python labs/m02/ask_policy.py "How long does a new laptop request take?" laptop-requests"""
import json
import os
import sys
import time
from pathlib import Path

from anthropic import Anthropic

from promptfile import load_prompt

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
POLICIES = {p.stem: p for p in (Path(__file__).resolve().parents[2] / "labkit" / "data" / "policies").glob("*.md")}
client = Anthropic()


def ask(question: str, doc_ids: list[str], prompt_name: str = "najm_desk_v1", cache: bool = False) -> str:
    prompt = load_prompt(prompt_name)
    docs = "\n".join(f'<document id="{d}">\n{POLICIES[d].read_text(encoding="utf-8").strip()}\n</document>' for d in doc_ids)
    user = f"<documents>\n{docs}\n</documents>\n\n<question>\n{question.replace('<', '&lt;')}\n</question>"      # documents first, question last
    system = [{"type": "text", "text": prompt.text, "cache_control": {"type": "ephemeral"}}] if cache else prompt.text
    started = time.time()
    resp = client.messages.create(model=MODEL, max_tokens=1024, output_config={"effort": "low"}, system=system,
                                  messages=[{"role": "user", "content": user}])
    u = resp.usage
    print(json.dumps({"prompt_version": prompt.version, "model": resp.model, "input_tokens": u.input_tokens,
                      "output_tokens": u.output_tokens, "cache_read": u.cache_read_input_tokens, "stop": resp.stop_reason,
                      "request_id": resp._request_id, "seconds": round(time.time() - started, 2)}), file=sys.stderr)   # the log line
    if resp.stop_reason != "end_turn":      # cut off (max_tokens) or refused
        raise RuntimeError(f"no usable answer: {resp.stop_reason}")
    return next((b.text for b in resp.content if b.type == "text"), "")


if __name__ == "__main__":
    print(ask(sys.argv[1], sys.argv[2:] or ["laptop-requests"], os.environ.get("PROMPT", "najm_desk_v1")))
