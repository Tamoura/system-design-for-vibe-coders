# labs/m12/graders.py
"""Lab 12.2: code graders. A check is a string "name:argument" in the dataset; run_check() returns (ok, why).
ok is None when the check did not run (a judge: check without --judge). Code first: free, exact, repeatable."""
import re

IDK = r"don.t know|do not know|not covered|no information|cannot find|can.t find|HANDOFF"      # "." matches any apostrophe


def calls(out) -> list:
    """The trajectory as sorted "tool=first argument" strings: order does not matter, extra calls do."""
    return sorted(f"{name}={next(iter(args.values()), '')}" for name, args in out.tools)


def arabic_share(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    return sum(0x600 <= ord(c) <= 0x6FF for c in letters) / max(1, len(letters))    # the Arabic Unicode block


CHECKS = {   # name -> (output, argument) -> bool
    "label": lambda o, a: o.text == a,                                                  # exact: the label alone
    "contains": lambda o, a: a.lower() in o.text.lower(),
    "not_contains": lambda o, a: a.lower() not in o.text.lower(),
    "regex": lambda o, a: re.search(a, o.text, re.I) is not None,
    "idk": lambda o, a: re.search(IDK, o.text, re.I) is not None,
    "cites": lambda o, a: a in set(re.findall(r"\[([\w-]+)#\d+\]", o.text)),            # cited the policy [doc#chunk]
    "cites_retrieved": lambda o, a: set(re.findall(r"\[([\w-]+#\d+)\]", o.text)) <= set(o.retrieved),   # no invented source
    "calls": lambda o, a: calls(o) == sorted(filter(None, a.split(","))),              # these calls, no extras
    "max_steps": lambda o, a: o.steps <= int(a),
    "reason": lambda o, a: o.reason == a,
    "lang": lambda o, a: (arabic_share(o.text) > 0.5) == (a == "ar"),
}


def run_check(check: str, out, case: dict, judge=None):
    name, _, arg = check.partition(":")
    if name == "judge":
        return (None, "judge not enabled") if judge is None else judge(arg, case, out)
    if name not in CHECKS:
        raise ValueError(f"unknown check {check!r}: a typo must never pass silently")
    ok = CHECKS[name](out, arg)
    return ok, "" if ok else f"got {out.text[:60]!r}"
