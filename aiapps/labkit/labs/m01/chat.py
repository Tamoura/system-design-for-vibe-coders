# labs/m01/chat.py
"""Lab A: a chatbot with memory in about 40 lines. Read every comment: the comments are the lesson."""
import os

from anthropic import Anthropic

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")   # one place to change the model
client = Anthropic()                                    # reads ANTHROPIC_API_KEY (and ANTHROPIC_BASE_URL)

SYSTEM = "You are a helpful assistant for a bank's IT service desk. Answer briefly. If you don't know, say so."

history = []                                            # THIS is the memory: a plain list in your process


def text_of(resp) -> str:
    """The reply text: pick the text block. content can start with a thinking block, so never index content[0]."""
    return next((b.text for b in resp.content if b.type == "text"), "")


def ask(user_text: str) -> str:
    history.append({"role": "user", "content": user_text})
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=1024,                   # a ceiling on the reply; thinking tokens count against it too
            output_config={"effort": "low"},   # chat needs little thinking (delete this line on older models)
            system=SYSTEM,                     # a separate parameter, resent on EVERY call
            messages=history,                  # the whole conversation, every time
        )
    except Exception:
        history.pop()                          # the call failed: take the question back out of the list
        raise
    reply = text_of(resp)
    history.append({"role": "assistant", "content": reply})   # write it back or it is gone

    # These numbers are your bill. Watch input climb: that is the history being resent.
    print(f"[in={resp.usage.input_tokens} out={resp.usage.output_tokens} stop={resp.stop_reason}]")
    return reply


if __name__ == "__main__":
    while True:
        try:
            text = input("you> ")
        except EOFError:
            break
        if text.strip() in ("exit", "quit"):
            break
        print("bot>", ask(text))
