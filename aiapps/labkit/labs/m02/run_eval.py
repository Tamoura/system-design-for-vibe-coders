# labs/m02/run_eval.py
"""Eval runner: a prompt over labelled tickets, exact-match grading, a confusion table, a saved run.
  run_eval.py classify_v2 --split dev [--reps 3]   |   run_eval.py --compare OLD.json NEW.json"""
import argparse
import json
import os
from collections import Counter
from pathlib import Path

from classify import LABELS, classify

DATA = Path(__file__).resolve().parents[2] / "labkit" / "data" / "tickets_labelled.jsonl"
RESULTS = Path(os.environ.get("EVAL_RESULTS_DIR", Path(__file__).parent / "results"))


def load_cases(split: str, path: Path = DATA) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    held_out = rows[2::3]                      # every third ticket, t03 to t30: never tuned on
    return {"dev": [r for r in rows if r not in held_out], "held_out": held_out, "all": rows}[split]


def run(prompt: str, split: str = "dev", reps: int = 1, cases: list[dict] | None = None, predict=classify) -> dict:
    rows, usage = [], Counter()
    for case in cases or load_cases(split):
        preds = [predict(case["text"], prompt) for _ in range(reps)]      # runs can differ: repeat
        for p in preds:
            usage["input"] += p.input_tokens
            usage["output"] += p.output_tokens
        got = [p.label for p in preds]
        rows.append({"id": case["id"], "text": case["text"], "expected": case["label"], "got": got,
                     "score": sum(g == case["label"] for g in got) / reps})     # the grader: exact match
    return {"prompt": prompt, "prompt_version": preds[-1].prompt_version, "model": preds[-1].model, "split": split,
            "reps": reps, "accuracy": sum(r["score"] for r in rows) / len(rows), "usage": dict(usage), "cases": rows}


def confusion(result: dict) -> dict[str, Counter]:
    table = {label: Counter() for label in LABELS}
    for row in result["cases"]:
        for got in row["got"]:
            table[row["expected"]][got if got in LABELS else "(invalid)"] += 1
    return table


def show(result: dict) -> None:
    cols = LABELS + ["(invalid)"]
    print(f"{result['prompt_version']} on {result['model']} | {result['split']} | accuracy {result['accuracy']:.0%} "
          f"(reps={result['reps']}, {len(result['cases'])} cases)")
    print(f"{'expected / got':<15}" + "".join(f"{c:>10}" for c in cols))
    for expected, counts in confusion(result).items():
        print(f"{expected:<15}" + "".join(f"{counts[c]:>10}" for c in cols))
    for r in [r for r in result["cases"] if r["score"] < 1][:8]:           # the misses: the next version's to-do list
        wrong = next(g for g in r["got"] if g != r["expected"])           # with --reps, show a wrong answer, not the first
        print(f"  miss {r['id']}: expected {r['expected']}, got {wrong[:30]!r}  {r['text'][:44]}")
    unstable = [r["id"] for r in result["cases"] if len(set(r["got"])) > 1]
    if unstable:
        print("  unstable across reps:", ", ".join(unstable))               # same prompt, different answers
    print(f"tokens: in={result['usage']['input']} out={result['usage']['output']}")   # cost = tokens x price


def compare(old: dict, new: dict) -> None:
    before = {r["id"]: r["score"] for r in old["cases"]}
    fixed = [r["id"] for r in new["cases"] if r["score"] > before.get(r["id"], 1)]
    broken = [r["id"] for r in new["cases"] if r["score"] < before.get(r["id"], 0)]
    print(f"{old['prompt_version']} -> {new['prompt_version']} ({new['split']}): {old['accuracy']:.0%} -> {new['accuracy']:.0%}")
    print(f"  fixed:  {', '.join(fixed) or 'none'}\n  broken: {', '.join(broken) or 'none'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", nargs="?")                       # a file in prompts/, no .txt
    ap.add_argument("--split", default="dev", choices=["dev", "held_out", "all"])
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--compare", nargs=2, metavar=("OLD", "NEW"))
    args = ap.parse_args()
    if args.compare:
        compare(*[json.loads(Path(p).read_text(encoding="utf-8")) for p in args.compare])
    elif not args.prompt:
        ap.error("give a prompt name, or --compare OLD NEW")
    else:
        result = run(args.prompt, args.split, args.reps)
        show(result)
        RESULTS.mkdir(parents=True, exist_ok=True)
        out = RESULTS / f"{result['prompt']}_{result['split']}.json"
        out.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
        print("saved", os.path.relpath(out))
