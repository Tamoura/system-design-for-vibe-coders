# labs/m06/spec_lint.py
"""Lint a specification: untestable words, and requirements with too few eval cases.
  python labs/m06/spec_lint.py SPEC.md [SEED.jsonl] [--skip NFR] [--min-cases 2]
Exit 0 = clean, 1 = findings. It matches text. It cannot tell whether a requirement is GOOD."""
import argparse
import json
import re
import sys
from pathlib import Path

SEED = Path(__file__).resolve().parents[2] / "labkit/data/m06_eval_seed.jsonl"
# Words that usually hide a number or a condition. A hit is a question for the author, not a verdict.
VAGUE = re.compile(r"(?<![\w-])(fast|quick|quickly|easy|easily|user-friendly|intuitive|seamless|robust|secure|scalable|flexible|"
                   r"appropriate|adequate|reasonable|efficient|efficiently|minimal|as needed|if necessary|etc|and/or)(?![\w-])", re.I)
DEFINES = re.compile(r"^\s*[-*]\s*\*{0,2}((?:FR|GR|NFR)-\d+)\*{0,2}\s+(.*)$")    # a requirement opens its own bullet


def requirements(text: str) -> dict[str, str]:
    """{id: text} for each bullet that starts with an id such as FR-01."""
    return {m.group(1): m.group(2) for line in text.splitlines() if (m := DEFINES.match(line))}


def lint(spec: str, rows: list[dict], skip=(), min_cases=2) -> list[str]:
    """Findings, empty when clean. A pure function, so the tests can call it."""
    reqs = requirements(spec)
    found = [f"{rid}: vague word '{w.group(1)}': give a number or a condition" for rid, text in reqs.items() for w in VAGUE.finditer(text)]
    cases: dict[str, list[str]] = {rid: [] for rid in reqs}
    for row in rows:
        for rid in row.get("reqs", []):
            if rid in cases:
                cases[rid].append(row["id"])
            else:                                            # no scenario without a requirement
                found.append(f"{row['id']}: cites {rid}, which the spec does not define")
    for rid, ids in cases.items():
        if rid.split("-")[0] not in skip and len(ids) < min_cases:
            found.append(f"{rid}: {len(ids)} eval case(s), want at least {min_cases}")
    return found


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("seed", nargs="?", default=str(SEED))
    ap.add_argument("--skip", action="append", default=[])          # a prefix to leave out of the case count, e.g. NFR
    ap.add_argument("--min-cases", type=int, default=2)
    a = ap.parse_args(argv)
    rows = [json.loads(x) for x in Path(a.seed).read_text(encoding="utf-8").splitlines() if x.strip()]
    found = lint(Path(a.spec).read_text(encoding="utf-8"), rows, a.skip, a.min_cases)
    print("\n".join(found) or "clean")
    print(f"{len(found)} finding(s)")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
