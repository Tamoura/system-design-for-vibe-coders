# ailab/labs/m09_toolkit/assets/post_edit_skeleton.py
"""Skeleton of a PostToolUse hook: copy it to .claude/hooks/post_edit.py and finish it.

Claude Code runs it after a successful Edit or Write and writes ONE JSON document to standard
input. The edit has already happened. The exit code decides what follows:
  0      nothing to report
  2      the WORK is wrong: standard error goes to the agent, which can then fix it
  other  the HOOK is broken (use 1): a non-blocking error; the agent carries on
As written it checks nothing and always exits 0. TODO marks what is missing.
"""
import json
import sys


def check_file(path):
    """Return a short description of what is wrong with the file at `path`, or None if it is fine."""
    # TODO: resolve a relative path against the document's "cwd"; skip what is not a .py file
    # TODO: report a file that does not parse; report a float in money code (src/remit/ only)
    return None


def main():
    try:
        document = json.load(sys.stdin)
        path = document["tool_input"].get("file_path")
    except (ValueError, KeyError, TypeError, AttributeError):
        print("post_edit: could not read the hook input", file=sys.stderr)
        sys.exit(1)  # the hook's problem, not the agent's: never 2
    if not isinstance(path, str) or not path:
        sys.exit(0)  # an edit with no file path: nothing to check
    problem = check_file(path)
    if problem:
        print(problem, file=sys.stderr)  # exit 2 sends this text to the agent
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
