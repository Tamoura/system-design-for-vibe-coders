# labs/m03/structured.py
"""Lab 3.2: one structured classification, validated with Pydantic, with a bounded retry that shows the model its mistake."""
import os
import sys
from typing import Literal

from anthropic import Anthropic, transform_schema
from pydantic import BaseModel, ConfigDict, ValidationError, model_validator

from trace import TraceLog      # labs/m03/trace.py

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
client = Anthropic()
SYSTEM = ("You triage IT service desk tickets for a bank: pick the category, say whether a human must take over, "
          "and summarise in one sentence. Security incidents always need a human.")


class Triage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: Literal["hardware", "access", "network", "software", "security", "other"]
    needs_human: bool
    summary: str

    @model_validator(mode="after")
    def security_needs_a_human(self):
        if self.category == "security" and not self.needs_human:
            raise ValueError("a security ticket must have needs_human = true")
        return self


class TriageFailed(Exception):
    """Raised after the last attempt: the caller hands the ticket to a human."""


def triage(ticket: str, max_attempts: int = 3, trace: TraceLog | None = None) -> Triage:
    trace = trace or TraceLog()
    messages = [{"role": "user", "content": ticket}]
    fmt = {"type": "json_schema", "schema": transform_schema(Triage)}
    problem = ""
    for attempt in range(1, max_attempts + 1):              # bounded: every retry is a paid call
        resp = client.messages.create(model=MODEL, max_tokens=1024, system=SYSTEM, messages=messages,
                                      output_config={"effort": "low", "format": fmt})
        if resp.stop_reason != "end_turn":                  # max_tokens (cut off) or refusal: not a validation error, so stop
            raise TriageFailed(f"stop_reason={resp.stop_reason}")
        text = next((b.text for b in resp.content if b.type == "text"), "")
        try:
            result = Triage.model_validate_json(text)       # validate anyway: a schema is not a business rule
        except ValidationError as e:
            problem = "; ".join(f"{'.'.join(map(str, x['loc'])) or 'ticket'}: {x['msg']}" for x in e.errors())
            trace.log("validation_error", attempt=attempt, problem=problem, raw=text)
            messages += [{"role": "assistant", "content": text},
                         {"role": "user", "content": f"That JSON failed validation: {problem}. Reply with corrected JSON only."}]
            continue
        trace.log("validated", attempt=attempt, result=result.model_dump())
        return result
    raise TriageFailed(f"still invalid after {max_attempts} attempts: {problem}")


if __name__ == "__main__":
    try:
        print(triage(" ".join(sys.argv[1:]) or "My VPN drops every ten minutes when I work from home",
                     trace=TraceLog(os.environ.get("TRACE_FILE"))).model_dump_json())
    except TriageFailed as e:
        print("TriageFailed:", e)
