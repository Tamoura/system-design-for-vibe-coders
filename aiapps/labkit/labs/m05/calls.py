# labs/m05/calls.py
"""The one place a model call happens: a concurrency limit, a deadline, error mapping, a trace row."""
import asyncio
import time
from dataclasses import dataclass, field

from anthropic import APIError, AsyncAnthropic


class StepError(Exception):
    """A failure the pipeline expects: recorded and handled, never a crash."""


@dataclass
class Run:
    client: AsyncAnthropic
    sem: asyncio.Semaphore                       # most calls in flight, across ALL notices
    timeout: float = 20.0                        # seconds per call, SDK retries included
    trace: list = field(default_factory=list)    # one dict per call


async def call(run, notice, step, model, system, messages, schema=None, attempt=1) -> str:
    """Send one request, return its text. Any failure raises StepError. Every call leaves a trace row."""
    row = {"notice": notice, "step": step, "attempt": attempt, "model": model, "status": "ok", "in_tok": 0, "out_tok": 0, "ms": 0}
    run.trace.append(row)                        # appended first: a call that never returns still leaves a row
    output = {"effort": "low"} | ({"format": {"type": "json_schema", "schema": schema}} if schema else {})
    try:
        async with run.sem:                      # held for ONE call, never while awaiting others (that deadlocks)
            t0 = time.perf_counter()
            try:
                async with asyncio.timeout(run.timeout):
                    resp = await run.client.messages.create(model=model, max_tokens=1024, system=system,
                                                            messages=messages, output_config=output)
            finally:
                row["ms"] = round((time.perf_counter() - t0) * 1000)
    except TimeoutError:                         # the server may still have finished, and billed, it
        row["status"] = "timeout"
        raise StepError(f"{step} timed out after {run.timeout}s")
    except APIError as e:                        # the SDK has already retried 429, 5xx and connection errors
        row["status"] = f"error {getattr(e, 'status_code', 'connection')}"
        raise StepError(f"{step} failed: {type(e).__name__}")
    row.update(in_tok=resp.usage.input_tokens, out_tok=resp.usage.output_tokens, request_id=resp._request_id)
    if resp.stop_reason != "end_turn":           # max_tokens or refusal: an identical retry would not help
        row["status"] = resp.stop_reason
        raise StepError(f"{step} stopped early: {resp.stop_reason}")
    return next((b.text for b in resp.content if b.type == "text"), "")      # the text block, never content[0]
