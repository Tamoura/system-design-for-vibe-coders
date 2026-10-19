"""A rough token estimator for the offline mock. It is NOT the real tokenizer.

Real token counts come from `client.messages.count_tokens(...)` or `response.usage`, and they
differ by model. This estimate only keeps the offline numbers growing in a believable way:
about one token per 4 ASCII characters, and one per 2 non-ASCII characters (so Arabic text
costs visibly more than English, as it usually does with real tokenizers; measure the real ratio)."""
from __future__ import annotations

import json
import math


def estimate(text: str) -> int:
    if not text:
        return 0
    ascii_chars = sum(1 for c in text if ord(c) < 128)
    other = len(text) - ascii_chars
    return max(1, math.ceil(ascii_chars / 4 + other / 2))


def block_text(block: dict) -> str:
    t = block.get("type")
    if t == "text":
        return block.get("text", "")
    if t == "tool_use":
        return block.get("name", "") + json.dumps(block.get("input", {}), ensure_ascii=False)
    if t == "tool_result":
        c = block.get("content", "")
        if isinstance(c, list):
            return " ".join(block_text(b) for b in c)
        return str(c)
    if t == "thinking":
        return block.get("thinking", "")
    return ""


def content_text(content) -> str:
    if isinstance(content, str):
        return content
    return " ".join(block_text(b) for b in content)


def estimate_request(system, messages, tools) -> int:
    n = estimate(system_text(system))
    for m in messages:
        n += 3 + estimate(content_text(m.get("content", "")))
    if tools:
        n += estimate(json.dumps(tools, ensure_ascii=False))
    return n


def system_text(system) -> str:
    if not system:
        return ""
    if isinstance(system, str):
        return system
    return " ".join(b.get("text", "") for b in system)
