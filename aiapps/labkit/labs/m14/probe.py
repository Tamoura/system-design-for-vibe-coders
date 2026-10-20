# labs/m14/probe.py
"""Lab 14.2: is the prompt cache working? Send the same prefix twice: the second call must READ it. NEEDS THE REAL API.
The offline mock never caches, so there it prints zeros and exits 1.   python labs/m14/probe.py"""
import os
import sys
from pathlib import Path

import anthropic

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
POLICIES = Path(__file__).resolve().parents[2] / "labkit" / "data" / "policies"


def cache_probe(client, model: str, system: str) -> bool:
    used = [client.messages.create(model=model, max_tokens=1024, output_config={"effort": "low"}, messages=[{"role": "user", "content": "Reply: ok"}],
                                   system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]).usage for _ in range(2)]
    print(f"first call wrote {used[0].cache_creation_input_tokens or 0} cached tokens; second call read {used[1].cache_read_input_tokens or 0}")
    return bool(used[1].cache_read_input_tokens)


if __name__ == "__main__":
    prefix = "You are Najm Desk.\n" + "\n\n".join(p.read_text(encoding="utf-8") for p in sorted(POLICIES.glob("*.md")))     # long enough to cache
    sys.exit(0 if cache_probe(anthropic.Anthropic(), MODEL, prefix) else 1)
