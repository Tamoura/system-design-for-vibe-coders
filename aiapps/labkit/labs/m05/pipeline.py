# labs/m05/pipeline.py
"""Lab 5.2: classify -> route -> summarise -> parallel fact-check, a gate after each step.
  python labs/m05/pipeline.py [N-101 ...]     (no ids: all six)     BASELINE=1 python ...: ONE big prompt instead
Each notice ends as ok, needs_review, partial, human or failed."""
import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Literal

from anthropic import AsyncAnthropic, transform_schema
from pydantic import BaseModel, ConfigDict, ValidationError

from calls import Run, StepError, call
from notice_prompts import CLASSIFY, FACTCHECK, FOCUS, ONE_PROMPT, SUMMARISE

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")        # strong tier: summarise and fact-check
CHEAP = os.environ.get("CHEAP_MODEL", "claude-haiku-5-5")    # cheap tier: the router
NOTICES = json.loads((Path(__file__).resolve().parents[2] / "labkit/data/m05_notices.json").read_text(encoding="utf-8"))
MAX_CLAIMS = 6                                               # also the widest fan-out


class Summary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    summary: str
    claims: list[str]


class Verdict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    verdict: Literal["supported", "unsupported", "contradicted"]


def fenced(n, extra=""):
    return f"<notice>\n{n['text']}\n</notice>{extra}"


def check_summary(s: Summary, notice: str) -> str:
    """Gate 2, plain code: the problem found, or '' when the summary may go on."""
    if not 1 <= len(s.claims) <= MAX_CLAIMS:
        return f"list between 1 and {MAX_CLAIMS} claims"
    if len(s.summary.split()) > 60:
        return "the summary is over 60 words"
    new = sorted(set(re.findall(r"\d+", " ".join([s.summary, *s.claims]))) - set(re.findall(r"\d+", notice)))
    return f"numbers not in the notice: {', '.join(new)}" if new else ""


async def summarise(run, n, label, attempts=2) -> Summary:
    system = SUMMARISE.format(label=label, focus=FOCUS[label])        # routing is choosing this prompt
    messages = [{"role": "user", "content": fenced(n)}]
    for attempt in range(1, attempts + 1):                            # bounded: a retry is a paid call
        raw = await call(run, n["id"], "summarise", MODEL, system, messages, transform_schema(Summary), attempt)
        try:
            summary = Summary.model_validate_json(raw)
            problem = check_summary(summary, n["text"])
        except ValidationError as e:
            problem = "invalid JSON: " + e.errors()[0]["msg"]
        if not problem:
            return summary
        messages += [{"role": "assistant", "content": raw},           # show the model its mistake
                     {"role": "user", "content": f"That answer failed a check: {problem}. Reply again with corrected JSON only."}]
    raise StepError(f"summary still failing its gate after {attempts} attempts: {problem}")


async def fact_check(run, n, claim) -> dict:
    messages = [{"role": "user", "content": fenced(n, f"\n<claim>{claim}</claim>")}]
    raw = await call(run, n["id"], "fact_check", MODEL, FACTCHECK, messages, transform_schema(Verdict))
    v = Verdict.model_validate_json(raw)                              # unreadable = failed check, never a pass
    return {"claim": claim, "verdict": v.verdict}


async def run_notice(run, n) -> dict:
    out = {"id": n["id"], "status": "failed", "label": "", "summary": "", "checks": [], "reason": ""}
    try:
        label = await call(run, n["id"], "classify", CHEAP, CLASSIFY, [{"role": "user", "content": fenced(n)}])
        out["label"] = label = label.strip().strip("`\"'.").lower()
        if label not in FOCUS:                                        # gate 1: a known label is routed, the rest go to a person
            return out | {"status": "human", "reason": f"not routable (label {label!r}): handed to a person, no more model calls"}
        summary = await summarise(run, n, label)                      # gate 2 runs inside
        out["summary"] = summary.summary
        found = await asyncio.gather(*(fact_check(run, n, c) for c in summary.claims), return_exceptions=True)    # the fan-out
        out["checks"] = [f if isinstance(f, dict) else {"claim": c, "verdict": "unchecked", "error": str(f).split("\n")[0][:70] or type(f).__name__}
                         for c, f in zip(summary.claims, found)]      # a failed check is a gap in the report, not a pass
        verdicts = {c["verdict"] for c in out["checks"]}              # gate 3: the verdicts decide the status
        out["status"] = "needs_review" if verdicts & {"unsupported", "contradicted"} else "partial" if "unchecked" in verdicts else "ok"
    except StepError as e:                                            # classify or summarise failed: nothing to report
        out["reason"] = str(e)
    return out


async def one_prompt(run, n) -> dict:
    """The baseline: the whole job in ONE call, traced like any step. No gates, no independent check."""
    out = {"id": n["id"], "status": "ok", "label": "-", "summary": "", "checks": [], "reason": "one call, no gates"}
    try:
        out["summary"] = await call(run, n["id"], "one_prompt", MODEL, ONE_PROMPT, [{"role": "user", "content": fenced(n)}])
    except StepError as e:
        out |= {"status": "failed", "reason": str(e)}
    return out


async def run_all(notices, width=4, timeout=20.0, max_retries=2, job=run_notice):
    async with AsyncAnthropic(max_retries=max_retries) as client:    # the SDK's transport retries
        run = Run(client, asyncio.Semaphore(width), timeout)
        t0 = time.perf_counter()
        results = await asyncio.gather(*(job(run, n) for n in notices))      # notices run side by side too
        return results, run.trace, time.perf_counter() - t0


def report(results, trace, wall) -> None:
    for r in results:
        bad = [c for c in r["checks"] if c["verdict"] != "supported"]
        ok = f"{len(r['checks']) - len(bad)}/{len(r['checks'])} claims supported  " if r["checks"] else ""
        print(f"{r['id']}  {r['label'] or '-':<9}{r['status']:<13}{ok}{r['reason']}")
        for c in bad:
            print(f"        {c['verdict']}: {c['claim'][:60]}" + (f"  <- {c['error']}" if "error" in c else ""))
    print(f"\n{'step':<11}{'calls':>6}{'in':>7}{'out':>6}{'slowest ms':>12}{'not ok':>8}")        # the trace, rolled up by step
    for step in dict.fromkeys(t["step"] for t in trace):          # in first-run order
        rows = [t for t in trace if t["step"] == step]
        print(f"{step:<11}{len(rows):>6}{sum(t['in_tok'] for t in rows):>7}{sum(t['out_tok'] for t in rows):>6}"
              f"{max(t['ms'] for t in rows):>12}{sum(t['status'] != 'ok' for t in rows):>8}")
    print(f"wall clock {wall:.2f}s")


if __name__ == "__main__":
    chosen = [n for n in NOTICES if not sys.argv[1:] or n["id"] in sys.argv[1:]]
    report(*asyncio.run(run_all(chosen, int(os.environ.get("WIDTH", "4")), float(os.environ.get("STEP_TIMEOUT", "20")),
                                int(os.environ.get("MAX_RETRIES", "2")), one_prompt if os.environ.get("BASELINE") else run_notice)))
