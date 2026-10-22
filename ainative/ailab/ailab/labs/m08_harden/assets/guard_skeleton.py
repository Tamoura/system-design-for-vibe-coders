# ailab/labs/m08_harden/assets/guard_skeleton.py
"""Skeleton of the guard hook for lab m08: copy it to .claude/hooks/guard.py and finish it.

Exit 0 allows the call; exit 2 blocks it, and stderr is the reason the agent reads; any other exit code
lets the call RUN. TASK.md has the rules. As it stands, this lets everything through.
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
    # TODO: what exit code does Python end with when this line raises, and what does Claude Code do with it?
    data = json.load(sys.stdin)
    if data.get("tool_name") != "Bash":
        sys.exit(0)
    command = data["tool_input"]["command"]  # TODO: and when there is no command?
    reason = reason_to_block(command)
    if reason:
        block(reason)
    sys.exit(0)


if __name__ == "__main__":
    main()
