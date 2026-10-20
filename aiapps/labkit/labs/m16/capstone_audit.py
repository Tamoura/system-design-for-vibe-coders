# labs/m16/capstone_audit.py
"""Lab 16.1: audit a capstone repository. Is the evidence there, and does it link up?
  python labs/m16/capstone_audit.py REPO [--tier 1|2|3] [--strict]      strict: a leftover TODO is a problem
EXISTS: each deliverable in labkit/data/m16_checklist.json is present and not empty, milestone by milestone.
LINKED: each requirement id the spec defines is cited downstream, and no cited id is missing from the spec.
Tier 3 also runs Lab 13.2's pack check on docs/governance (with --strict, every signer's row must say approved).
It cannot tell whether evidence is good or true, or whether an "approved" row was really given: that stays with people."""
import argparse
import json
import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[2]
CHECKLIST = json.loads((KIT / "labkit" / "data" / "m16_checklist.json").read_text(encoding="utf-8"))   # milestone -> tier -> items
sys.path.insert(0, str(KIT / "labs" / "m13"))
import pack_check                                             # noqa: E402  Lab 13.2: the governance pack check

REQ = r"(?:FR|GR|NFR|AC)-\d+"                                 # ids as in lesson 6.2


def exists(repo: Path, tier: int, strict: bool) -> dict:
    """milestone -> problems, counting the items up to `tier`. A glob item needs at least `count` files."""
    report = {}
    for milestone, by_tier in CHECKLIST.items():
        problems = report[milestone] = []
        for t, items in by_tier.items():
            for item in items if int(t) <= tier else []:
                pattern, count = (item, 1) if isinstance(item, str) else item
                found = [p for p in sorted(repo.glob(pattern)) if p.is_file()]
                if len(found) < count:
                    problems.append(f"{pattern}: {len(found)} found, {count} needed")
                elif any(p.stat().st_size == 0 for p in found):
                    problems.append(f"{pattern}: an empty file")
                elif strict and any("TODO" in p.read_text(encoding="utf-8", errors="replace") for p in found):
                    problems.append(f"{pattern}: still has a TODO")
    return report


def linked(repo: Path):
    """(ids the spec defines that nothing downstream cites, ids cited downstream that the spec lacks)."""
    spec = repo / "docs" / "najm-desk-spec.md"
    if not spec.is_file():
        return [], []
    defined = set(re.findall(rf"^- \*\*({REQ})\*\*", spec.read_text(encoding="utf-8"), re.M))
    downstream = [p for p in [*repo.glob("evals/*.jsonl"), *repo.glob("docs/**/*.md")] if p != spec]
    cited = set().union(*[set(re.findall(rf"\b{REQ}\b", p.read_text(encoding="utf-8"))) for p in downstream])
    return sorted(defined - cited), sorted(cited - defined)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    ap.add_argument("--tier", type=int, choices=(1, 2, 3), default=1)
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args(argv)
    problems = 0
    for milestone, issues in exists(a.repo, a.tier, a.strict).items():
        print(f"{milestone:40} {'fix' if issues else 'ok'}")
        for issue in issues:
            print("    " + issue)
        problems += len(issues)
    untraced, orphans = linked(a.repo)
    notes = [f"{i}: defined in the spec, cited nowhere downstream" for i in untraced]
    notes += [f"{i}: cited downstream, not defined in the spec" for i in orphans]
    if a.tier == 3:                                           # the seven-document pack is a tier 3 deliverable
        notes += ["governance: " + p for p in pack_check.check(a.repo / "docs" / "governance", structure_only=not a.strict)]
    print(*notes, sep="\n", end="\n" if notes else "")
    problems += len(notes)
    print(f"audit (tier {a.tier}{', strict' if a.strict else ''}): {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
