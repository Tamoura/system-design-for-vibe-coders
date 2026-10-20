# labs/m12/run_eval.py
"""Lab 12.2: run the 50 cases over three agents and write a results file.
--mode mock proves the pipeline. --mode real measures quality and spends money: set a spending cap first."""
import argparse
import json
import os
import sys
from pathlib import Path

import adapters
import graders
import stats

DATASET = Path(__file__).resolve().parents[2] / "labkit" / "data" / "m12_eval_50.jsonl"
KEYS = ("id", "agent", "category", "critical")


def load_cases(path=DATASET) -> list[dict]:
    cases = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    for c in cases:                                          # a typo fails here, not later as a silent pass
        if c["agent"] not in adapters.AGENTS or any(x.partition(":")[0] not in {*graders.CHECKS, "judge"} for x in c["checks"]):
            raise ValueError(f"case {c['id']}: unknown agent or check")
    return cases


def run_case(case: dict, reps: int, judge) -> dict:
    """One case, `reps` times. A harness failure is an error, never a fail: plumbing is not the agent's fault."""
    head, runs = {k: case[k] for k in KEYS}, []
    for _ in range(reps):
        try:
            out, meter, ms = adapters.timed(case["agent"], case["input"])
            with adapters.Meter() as jm:                     # the judge's tokens are counted apart from the agent's
                checks = [(c, *graders.run_check(c, out, case, judge)) for c in case["checks"]]
        except Exception as e:
            return {**head, "error": f"{type(e).__name__}: {e}"[:120]}
        ran = [c for c in checks if c[1] is not None]        # None = not run: it neither passes nor fails the case
        runs.append({"ok": bool(ran) and all(c[1] for c in ran), "text": out.text[:200], "ms": ms, "in": meter.tokens_in,
                     "out": meter.tokens_out, "judge": jm.tokens_in + jm.tokens_out, "why": [f"{c[0]}: {c[2]}" for c in ran if not c[1]]})
    avg = lambda key: round(sum(r[key] for r in runs) / reps)
    return {**head, "score": sum(r["ok"] for r in runs) / reps, "ms": avg("ms"), "tokens_in": avg("in"), "tokens_out": avg("out"),
            "judge_tokens": sum(r["judge"] for r in runs), "output": runs[0]["text"], "failed": next((r["why"] for r in runs if not r["ok"]), [])}


def run_all(cases: list[dict], mode: str, reps: int = 1, judge=None) -> dict:
    seen = adapters.prompt_examples() if any(c["agent"] == "classifier" for c in cases) else set()
    rows = [{**{k: c[k] for k in KEYS}, "skipped": "real_only"} if c["real_only"] and mode == "mock" else run_case(c, reps, judge) for c in cases]
    return stats.summarise(rows, DATASET, mode=mode, reps=reps, judge=judge is not None, versions=adapters.versions({c["agent"] for c in cases}),
                           leaks=sorted(c["id"] for c in cases if c["input"].lower() in seen))      # data hygiene: no answer key in a prompt


def check_mode(mode: str) -> None:
    """Fail closed: a mock run must never reach the real API, and a real run must never pass for a mock one."""
    local = os.environ.get("ANTHROPIC_BASE_URL", "").startswith(("http://127.0.0.1", "http://localhost"))
    if (mode == "mock") != local or (mode == "real" and os.environ.get("ANTHROPIC_API_KEY", "mock") == "mock"):
        sys.exit(f"--mode {mode} does not match ANTHROPIC_BASE_URL and ANTHROPIC_API_KEY: refusing to run")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["mock", "real"], required=True)
    ap.add_argument("--out", default="results.json")
    ap.add_argument("--reps", type=int, default=int(os.environ.get("EVAL_REPS", 1)))
    ap.add_argument("--judge", action="store_true")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    check_mode(a.mode)
    judge = None
    if a.judge:
        if a.mode == "mock":
            sys.exit("the mock cannot judge: it answers every yes/no field with false")
        import anthropic
        import judge as judge_module
        judge = judge_module.make_judge(anthropic.Anthropic())
    res = run_all([c for c in load_cases() if a.only in ("", c["agent"])], a.mode, a.reps, judge)
    Path(a.out).write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    stats.show(res)
