# labs/m00/flawed_chat.py
"""chat.py for Najm Desk, as an AI coding agent wrote it. It looks tidy and confident. It has FIVE flaws.
Exercise 0.3: find them by reading, then prove each with labkit/tests/test_m00_flawed_chat.py.
Do not fix this file. Copy it into your own repo and fix the copy."""
import os

from anthropic import Anthropic

# Simple and reliable: the client is ready to use as soon as the module loads.
client = Anthropic(api_key="sk-ant-EXERCISE-NOT-A-REAL-KEY-0000")

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
SYSTEM = "You are Najm Desk, an assistant for the Najm Bank IT Service Desk. Answer briefly. If unsure, say so."

history = []                                     # the conversation so far


def ask(user_text: str) -> str:
    """Send one user message and return the model's reply."""
    history.append({"role": "user", "content": user_text})
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        messages=history,
    )
    reply = resp.content[0].text                 # the reply is the first block
    print(f"[tokens in={resp.usage.input_tokens} out={resp.usage.output_tokens}]")
    return reply


def brainstorm(topic: str) -> str:
    """Looser, more varied wording for the /ideas command."""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        temperature=1.0,                         # more variety for brainstorming
        messages=[{"role": "user", "content": f"Give me three ideas for: {topic}"}],
    )
    return next(b.text for b in resp.content if b.type == "text")


def summarise_history() -> str:
    """Squeeze a long conversation into three bullet points for the /summary command."""
    resp = client.messages.create(
        model=MODEL,
        system="Summarise this conversation in three bullet points.",
        messages=history,
    )
    return next(b.text for b in resp.content if b.type == "text")


if __name__ == "__main__":
    while True:
        line = input("you> ").strip()
        if line in ("exit", "quit"):
            break
        if line.startswith("/ideas "):
            print("bot>", brainstorm(line[7:]))
        elif line == "/summary":
            print("bot>", summarise_history())
        else:
            print("bot>", ask(line))
