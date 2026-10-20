# labs/m02/classify.py
"""Najm Desk ticket classification: a prompt file and a ticket in, a label out. Same code on the mock and the real API."""
import logging
import os
from dataclasses import dataclass

from anthropic import Anthropic

from promptfile import load_prompt

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")   # evaluate the model you will ship
LABELS = ["hardware", "access", "network", "software", "security", "other"]
client = Anthropic()                                    # reads ANTHROPIC_API_KEY (and ANTHROPIC_BASE_URL)
log = logging.getLogger("najm.classify")


@dataclass
class Prediction:
    label: str            # cleaned up but not forced into LABELS, so a wrong format stays visible
    prompt_version: str   # PROMPT_VERSION: which prompt text produced it
    model: str            # read from the response, not from our config
    input_tokens: int     # usage: an eval's cost is arithmetic on these two numbers
    output_tokens: int


def classify(ticket_text: str, prompt_name: str = "classify_v3") -> Prediction:
    prompt = load_prompt(prompt_name)
    fenced = ticket_text.replace("<", "&lt;")          # no tag inside a ticket can close the fence (hygiene, not a defence)
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1024,                  # thinking tokens count against it, even for a one-word answer
        output_config={"effort": "low"},  # little thinking needed (delete on older models)
        system=prompt.text,               # the specification lives in the file
        messages=[{"role": "user", "content": f"<ticket>\n{fenced}\n</ticket>"}],
    )
    raw = next((b.text for b in resp.content if b.type == "text"), "")      # the text block, never content[0]
    log.info("prompt=%s model=%s in=%d out=%d stop=%s", prompt.version, resp.model, resp.usage.input_tokens,
             resp.usage.output_tokens, resp.stop_reason)                    # PROMPT_VERSION on every call
    return Prediction(raw.strip().strip("`\"'.").lower(), prompt.version, resp.model,
                      resp.usage.input_tokens, resp.usage.output_tokens)
