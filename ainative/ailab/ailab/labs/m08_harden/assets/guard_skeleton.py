# ailab/labs/m08_harden/assets/guard_skeleton.py
"""Guard hook skeleton for lab m08: copy it to .claude/hooks/guard.py and finish it. TASK.md has the rules.

Exit 0 allows the call; exit 2 blocks it (stderr is the reason the agent reads); any other code lets it RUN.
"""
import json
import sys


def block(reason):
    print(f"Blocked: {reason}", file=sys.stderr)
    sys.exit(2)


def reason_to_block(command):
    """Return a short reason when this shell command must not run, else None. TODO: the rules."""
    return None


def main():
    data = json.load(sys.stdin)  # TODO: what exit code does Python end with when this raises, and what happens then?
    if data.get("tool_name") != "Bash":
        sys.exit(0)
    command = data["tool_input"]["command"]  # TODO: and when there is no command?
    reason = reason_to_block(command)
    if reason:
        block(reason)
    sys.exit(0)


if __name__ == "__main__":
    main()
