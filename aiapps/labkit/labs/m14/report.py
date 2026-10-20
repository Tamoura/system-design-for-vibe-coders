# labs/m14/report.py
"""Lab 14.2: read usage.jsonl and answer Hind: what did it cost, how fast, inside its SLOs? Exit 1 on a breach.
  python labs/m14/report.py usage.jsonl --resolved 9"""
import argparse
import json
import sys
from collections import defaultdict


def p95(values: list) -> int:
    """Nearest rank: the value that 95% of calls were at or under."""
    v = sorted(values)
    return v[-(-len(v) * 95 // 100) - 1] if v else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--resolved", type=int, default=0, help="conversations resolved without a person (from the ticket system)")
    for name, default in (("p95-ms", 20_000), ("error-rate", 0.02), ("convo-cost", 0.01)):      # targets: edit to taste
        ap.add_argument(f"--slo-{name}", type=type(default), default=default)
    a = ap.parse_args(argv)
    rows = [json.loads(line) for line in open(a.log, encoding="utf-8") if line.strip()]
    ok = [r for r in rows if "error" not in r]
    models, convos = defaultdict(list), defaultdict(float)
    for r in ok:
        models[r["model"]].append(r)
        convos[r["convo"]] += r["cost"] or 0.0
    for m, rs in sorted(models.items()):
        print(f"{m:<19}{len(rs):>3} calls {sum(r['input'] for r in rs):>6} in {sum(r['output'] for r in rs):>5} out "
              f"cost {sum(r['cost'] or 0 for r in rs):.5f}  p95 {p95([r['ms'] for r in rs])} ms")
    total, per_convo = sum(convos.values()), sum(convos.values()) / max(1, len(convos))
    print(f"total {total:.5f} over {len(convos)} conversations = {per_convo:.5f} each"
          + (f"; {total / a.resolved:.5f} per resolved ticket" if a.resolved else "") + f"; {len(rows) - len(ok)} errors")
    bad = {"p95 latency": p95([r["ms"] for r in ok]) > a.slo_p95_ms, "error rate": 1 - len(ok) / max(1, len(rows)) > a.slo_error_rate,
           "cost per conversation": per_convo > a.slo_convo_cost, "unpriced calls": any(r["cost"] is None for r in ok)}
    breaches = [name for name, hit in bad.items() if hit]
    print("SLO: " + ("BREACH of " + ", ".join(breaches) if breaches else "all inside their targets"))
    return 1 if breaches else 0


if __name__ == "__main__":
    sys.exit(main())
