# ailab/labs/m09_toolkit/assets/triage_skeleton.py
"""Skeleton of scripts/triage.py: copy it to scripts/triage.py and finish it.

usage: python scripts/triage.py TICKETS.json [--max-turns N] [--timeout SECONDS]
Prints ONE JSON document on standard out. Exit 0 when every ticket was classified, 1 when some
failed, 2 when the input is unusable. TASK.md has the contract; TODO marks what is missing.
"""
import argparse
import json
import subprocess
import sys

CATEGORIES = ("bug", "feature", "question")
SEVERITIES = ("low", "medium", "high")
AREAS = ("fees", "fx", "limits", "screening", "notify", "ledger", "other")
INSTRUCTIONS = "TODO: say exactly what to return, in words that read_fields below can rely on"


def ask_claude(text, max_turns, timeout):
    """Run `claude -p` once for one ticket and return the JSON object it printed. TODO: flags, stdin, failures."""
    raise NotImplementedError("ask_claude is not written yet")


def read_fields(reply):
    """Take category, severity, area and money_logic from the reply; raise ValueError if it is not acceptable. TODO."""
    raise NotImplementedError("read_fields is not written yet")


def triage(ticket, max_turns, timeout):
    try:
        reply = ask_claude(ticket["text"], max_turns, timeout)
        fields = read_fields(reply)
    except (ValueError, OSError, subprocess.SubprocessError, NotImplementedError) as problem:
        return {"id": ticket.get("id"), "status": "error", "error": str(problem) or type(problem).__name__}
    entry = {"id": ticket["id"], "status": "ok", **fields}
    if isinstance(reply.get("total_cost_usd"), (int, float)):
        entry["cost_usd"] = reply["total_cost_usd"]  # what this run cost, added up as total_cost_usd in main()
    return entry


def main(argv=None):
    parser = argparse.ArgumentParser(description="Classify support tickets with claude -p")
    parser.add_argument("tickets", help="a JSON file: a list of {id, text}")
    parser.add_argument("--max-turns", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=60.0)
    args = parser.parse_args(argv)
    try:
        with open(args.tickets, encoding="utf-8") as handle:
            tickets = json.load(handle)
    except (OSError, ValueError) as problem:
        print(f"triage: cannot read {args.tickets}: {problem}", file=sys.stderr)
        return 2
    # TODO: tickets must be a list of objects with an id and a text; anything else is exit 2
    results = [triage(ticket, args.max_turns, args.timeout) for ticket in tickets]
    failed = sum(1 for result in results if result["status"] != "ok")
    total = round(sum(result.get("cost_usd", 0) for result in results), 6)
    print(json.dumps({"results": results, "ok": len(results) - failed, "failed": failed, "total_cost_usd": total}, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
