# labs/m12/gate.py
"""Lab 12.2: the regression gate. Exit 0 = pass, 1 = a regression (block the merge), 2 = the eval itself cannot be trusted."""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

PASS = 0.5     # the flake rule: a case passes when more than half of its repetitions pass


def load(path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def judge(new: dict, base: dict, cfg: dict, today: date):
    """Returns (broken, failed, notes): problems with the eval, problems with the agent, things worth a look."""
    broken, failed, notes = [], [], []
    if new["n_errors"] > cfg["max_errors"]:
        broken.append(f"{new['n_errors']} cases errored: the harness is broken, the score means nothing")
    if new["leaks"]:
        broken.append(f"eval inputs are prompt examples ({', '.join(new['leaks'])}): that score proves nothing")
    broken += [f"{k} changed ({base.get(k)} -> {new.get(k)}): re-baseline on purpose, in its own commit" for k in ("mode", "judge", "dataset_sha", "n_run") if new.get(k) != base.get(k)]
    if broken:
        return broken, failed, notes                         # a gate that compares different things is worse than none
    quiet = {i for i, until in cfg["quarantine"].items() if date.fromisoformat(until) >= today}
    failed += [f"the quarantine of {i} has ended: fix the case or delete it" for i in cfg["quarantine"] if i not in quiet]
    now, old = ({c["id"]: c for c in r["cases"] if "score" in c and c["id"] not in quiet} for r in (new, base))
    mean = lambda cs: sum(c["score"] for c in cs) / max(1, len(cs))
    tokens = lambda cs: sum(c["tokens_in"] + c["tokens_out"] for c in cs) / max(1, len(cs))
    if mean(old.values()) - mean(now.values()) > cfg["max_overall_drop"]:
        failed.append(f"overall score fell from {mean(old.values()):.1%} to {mean(now.values()):.1%}")
    regressed = [i for i, c in now.items() if i in old and old[i]["score"] > PASS >= c["score"]]
    if any(now[i]["critical"] for i in regressed):           # a critical case that used to pass: no budget, no discussion
        failed.append("critical cases that used to pass now fail: " + ", ".join(i for i in regressed if now[i]["critical"]))
    if len(regressed) > cfg["max_regressed_cases"]:
        failed.append(f"{len(regressed)} cases regressed (limit {cfg['max_regressed_cases']}): {', '.join(regressed)}")
    for cat, floor in cfg["floors"].items():
        cs = [c for c in now.values() if c["category"] == cat]
        if cs and mean(cs) < floor:
            failed.append(f"category {cat} is {mean(cs):.0%}, below its floor of {floor:.0%}")
    if tokens(now.values()) > tokens(old.values()) * (1 + cfg["max_token_increase"]):
        failed.append(f"tokens per case rose from {tokens(old.values()):.0f} to {tokens(now.values()):.0f}")
    if new["latency_ms"]["p95"] > cfg["max_p95_ms"]:
        failed.append(f"p95 latency {new['latency_ms']['p95']} ms is over {cfg['max_p95_ms']} ms")
    notes += [f"{i} is critical and fails here and in the baseline: an open defect, not a regression"
              for i, c in now.items() if c["critical"] and c["score"] <= PASS and i in old and old[i]["score"] <= PASS]
    return broken, failed, notes + [f"{k} changed: {base['versions'].get(k)} -> {v}" for k, v in new["versions"].items() if base["versions"].get(k) != v]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("results")
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--config", default=str(Path(__file__).with_name("gate.json")))
    a = ap.parse_args()
    broken, failed, notes = judge(load(a.results), load(a.baseline), load(a.config), date.today())
    for tag, lines in (("note", notes), ("BROKEN", broken), ("FAIL", failed)):
        print(*[f"{tag}: {line}" for line in lines], sep="\n", end="\n" if lines else "")
    print("gate:", "the eval is broken (exit 2)" if broken else "regression (exit 1)" if failed else "pass (exit 0)")
    sys.exit(2 if broken else 1 if failed else 0)
