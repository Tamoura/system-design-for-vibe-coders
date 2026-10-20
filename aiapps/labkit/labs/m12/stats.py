# labs/m12/stats.py
"""Lab 12.2: the numbers a results file needs besides one pass rate, and how a run is shown."""
import hashlib
import math
import os
import time
from collections import defaultdict
from pathlib import Path


def wilson(k: float, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% interval for k passes in n trials: the pass rates this evidence cannot rule out."""
    if n == 0:
        return 0.0, 1.0
    p, d = k / n, 1 + z * z / n
    centre, margin = (p + z * z / (2 * n)) / d, z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, centre - margin), min(1.0, centre + margin)


def tally(cases: list[dict], key: str) -> dict:
    """Mean score per group (category or agent): an average hides a broken corner, so report the corners."""
    groups = defaultdict(list)
    for c in cases:
        groups[c[key]].append(c["score"])
    return {k: {"score": round(sum(v) / len(v), 4), "passed": round(sum(v), 2), "total": len(v)} for k, v in sorted(groups.items())}


def percentile(values: list[int], q: float) -> int:
    """Nearest rank. The mean hides the slow tail; the 95th percentile is what a user feels on a bad day."""
    values = sorted(values)
    return values[min(len(values) - 1, math.ceil(q * len(values)) - 1)] if values else 0


def cost(tokens_in: int, tokens_out: int):
    """Tokens times the prices YOU read off the current price page (per million tokens); None until you set them."""
    price = [float(os.environ.get(k, 0)) for k in ("PRICE_IN_PER_MTOK", "PRICE_OUT_PER_MTOK")]
    return round((tokens_in * price[0] + tokens_out * price[1]) / 1e6, 4) if all(price) else None


def show(res: dict) -> None:
    o, u = res["overall"], res["usage"]
    print(f"{res['n_run']} run, {res['n_skipped']} skipped, {res['n_errors']} errors | overall {o['passed']:g}/{o['total']} = {o['score']:.0%}"
          f" (95% CI {o['ci'][0]:.0%} to {o['ci'][1]:.0%}) | tokens {u['tokens_in']}+{u['tokens_out']} | p95 {res['latency_ms']['p95']} ms")
    if res["leaks"]:
        print("LEAKED INPUTS (also examples in a prompt):", ", ".join(res["leaks"]))
    for name, s in res["categories"].items():
        print(f"  {name:<22}{s['passed']:>5g}/{s['total']:<3}{s['score']:>5.0%}")


def summarise(rows: list[dict], dataset: Path, **meta) -> dict:
    """The results file: counts, the overall score with its interval, scores by category, tokens, latency, then every case."""
    scored = [r for r in rows if "score" in r]
    k, n = sum(r["score"] for r in scored), len(scored)
    tin = sum(r["tokens_in"] for r in scored) * meta["reps"]
    tout = sum(r["tokens_out"] for r in scored) * meta["reps"]
    ms = [r["ms"] for r in scored]
    return {**meta, "started": time.strftime("%Y-%m-%d %H:%M"), "dataset_sha": hashlib.sha256(dataset.read_bytes()).hexdigest()[:12],
            "n_run": n, "n_skipped": sum("skipped" in r for r in rows), "n_errors": sum("error" in r for r in rows),
            "overall": {"score": round(k / n, 4) if n else 0.0, "passed": round(k, 2), "total": n, "ci": [round(x, 4) for x in wilson(k, n)]},
            "categories": tally(scored, "category"), "flaky": [r["id"] for r in scored if 0 < r["score"] < 1],
            "usage": {"tokens_in": tin, "tokens_out": tout, "judge_tokens": sum(r["judge_tokens"] for r in scored), "cost": cost(tin, tout)},
            "latency_ms": {"p50": percentile(ms, 0.5), "p95": percentile(ms, 0.95)}, "cases": rows}
