# labs/m01/trim.py
"""Exercise 1.1, reference answer: send a trimmed VIEW of the history so the call fits the window."""
import os

from anthropic import Anthropic

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
client = Anthropic()
SYSTEM = "You are a helpful assistant for a bank's IT service desk. Answer briefly. If you don't know, say so."   # as in chat.py


def count(history: list[dict]) -> int:
    """Input tokens the API would see. Exact on the real API; an estimate on the mock."""
    return client.messages.count_tokens(model=MODEL, system=SYSTEM, messages=history).input_tokens


def trim(history: list[dict], max_tokens: int, count=count) -> list[dict]:
    """Drop the oldest turns until the history fits. Call it AFTER appending the new user message.
    The system prompt is a separate parameter, so it can never be trimmed; the newest message
    always stays, and the result starts with a user message, as the API requires."""
    kept = list(history)                              # never mutate the caller's list
    while len(kept) > 1 and count(kept) > max_tokens:
        del kept[0]                                   # the oldest message...
        while len(kept) > 1 and kept[0]["role"] != "user":
            del kept[0]                               # ...and its orphaned reply
    return kept
