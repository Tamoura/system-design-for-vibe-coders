# labs/m15/trace_report.py
"""Lab 15.1: one page for the on-call person, from JSONL traces (Lab 8.2's format, plus release and prompt_version).
  python labs/m15/trace_report.py TRACE.jsonl [--by release]    exit 1 on an SLO breach, personal data or a broken log
Set PRICE_IN_PER_MTOK and PRICE_OUT_PER_MTOK (per million tokens) from the price page: prices never live in code."""
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

SLO = {"success": 0.90, "p95_seconds": 10.0}      # decisions, not facts: take yours from NFR-01 and your own data
PII = {"email": r"[\w.+-]+@[\w-]+\.[\w.]+", "card": r"\b(?:\d[ -]?){13,16}\b", "secret": r"(?i)\b(?:password|passcode)\s*(?:is|=|:)\s*\S+"}
PRICE = [float(os.environ.get(k, "nan")) for k in ("PRICE_IN_PER_MTOK", "PRICE_OUT_PER_MTOK")]


def pct(xs, p):
    """Nearest-rank percentile: averages hide the tail, where users wait."""
    xs = sorted(xs)
    return xs[max(0, math.ceil(p / 100 * len(xs)) - 1)] if xs else float("nan")


def report(label, runs):
    """Print one group of runs (each a list of events); return True when it breaches an SLO."""
    stops = [next((e for e in ev if e["event"] == "stop"), {}) for ev in runs]       # no stop event: the process died or was killed
    reasons, secs = Counter(s.get("reason", "no_stop_line") for s in stops), [s["seconds"] for s in stops if "seconds" in s]
    usage = [[sum(e.get(k, 0) for e in ev if e["event"] == "model") for k in ("input_tokens", "output_tokens")] for ev in runs]
    n, done, money = len(runs), reasons["done"], sum(a * PRICE[0] + b * PRICE[1] for a, b in usage) / 1e6
    print(f"== {label}: {n} runs ==\noutcomes : " + " | ".join(f"{k} {v} ({v / n:.0%})" for k, v in reasons.most_common()))
    print(f"latency  : run p50 {pct(secs, 50):.1f} s, p95 {pct(secs, 95):.1f} s | tokens per run p95 {pct([a + b for a, b in usage], 95):,.0f}")
    if not math.isnan(money):                      # failed runs cost too: divide by RESOLVED conversations
        print(f"cost     : {money:.2f} in all, {money / max(done, 1):.4f} per resolved conversation")
    ok = {f"success {done / n:.1%} (want {SLO['success']:.0%}+)": done / n >= SLO["success"],
          f"p95 {pct(secs, 95):.1f} s (want {SLO['p95_seconds']:g} s or less)": pct(secs, 95) <= SLO["p95_seconds"]}
    print("slo      : " + " | ".join(f"{k} {'ok' if v else 'BREACH'}" for k, v in ok.items()))
    return not all(ok.values())


if __name__ == "__main__":
    runs, bad, leaks = defaultdict(list), 0, Counter()
    for line in open(sys.argv[1], encoding="utf-8"):
        try:
            e = json.loads(line)
            run, kind = e["run"], e["event"]
        except (ValueError, KeyError, TypeError):
            bad += bool(line.strip())                  # a pipeline that drops lines is a finding too
            continue
        runs[run].append(e)
        for field, v in e.items():                     # kinds and places are safe to print; the values are not
            leaks.update((what, f"{kind}.{field}") for what, rx in PII.items() if isinstance(v, str) and re.search(rx, v))
    by, groups = (sys.argv[sys.argv.index("--by") + 1] if "--by" in sys.argv else None), defaultdict(list)
    for ev in runs.values():
        groups[next((e for e in ev if e["event"] == "start"), {}).get(by, "(none)") if by else "all"].append(ev)
    print(f"{len(runs)} runs, {bad} unreadable lines")
    breached = [report(label, g) for label, g in sorted(groups.items())]
    print("privacy  : " + (", ".join(f"{k} in {w} x{n}" for (k, w), n in sorted(leaks.items())) or "no personal-data patterns found"))
    sys.exit(1 if any(breached) or leaks or bad or not runs else 0)        # no traces at all is an incident too
