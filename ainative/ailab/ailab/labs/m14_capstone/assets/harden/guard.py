#!/usr/bin/env python3
"""A baseline PreToolUse guard for Najm Remit (lab m14). Copy it to .claude/hooks/guard.py and read every line.

Claude Code runs this before each Bash tool call and writes one JSON document to standard input. Exit code 0
lets the call go ahead. Exit code 2 blocks it, and standard error is the reason the agent reads. Any other
exit code is a non-blocking error: the command RUNS. So this script must never crash, and it blocks anything
it cannot understand.

It is a guard rail, not a wall. It reads the text of a command; it cannot see what a script will do once it
starts. The sandbox and the permission rules are the wall. If you did lab m08, your own guard is better:
use that one instead.
"""
import json
import os
import re
import shlex
import sys

SHELLS = {"sh", "bash", "zsh", "dash", "ksh"}
INTERPRETERS = SHELLS | {"python", "python3", "perl", "ruby", "node"}
WRAPPERS = {"env", "nohup", "nice", "time", "timeout", "command", "exec", "xargs"}
INSTALLERS = {"pip": "install", "pip3": "install", "uv": "add", "poetry": "add", "npm": "install", "yarn": "add"}
GIT_OPTIONS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree"}
ENV_FILE = re.compile(r"(^|/)\.env(\.[\w-]+)?$")
SAFE_ENV_SUFFIXES = (".example", ".sample", ".template")
SECRET_PATH = re.compile(r"(^|/)\.(ssh|aws)(/|$)|(^|/)id_(rsa|dsa|ecdsa|ed25519)$")


def block(reason):
    print(f"Blocked: {reason}", file=sys.stderr)
    sys.exit(2)


def segments(command):
    """Split a command line into lists of words at ; && || | and newlines. Quoted text stays in one word."""
    lexer = shlex.shlex(command.replace("\n", " ; "), posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    lexer.commenters = ""
    result, current = [], []
    for token in lexer:
        if token and all(char in ";&|()" for char in token):
            if current:
                result.append(current)
            current = []
        else:
            current.append(token)
    if current:
        result.append(current)
    return result


def program_index(words):
    """Index of the program in a segment: skip VAR=value prefixes and harmless wrappers."""
    i = 0
    while i < len(words):
        if re.fullmatch(r"[A-Za-z_]\w*=.*", words[i]) or os.path.basename(words[i]) in WRAPPERS:
            i += 1
        else:
            break
    return i


def git_subcommand(args):
    i = 0
    while i < len(args) and args[i].startswith("-"):
        i += 2 if args[i] in GIT_OPTIONS_WITH_VALUE else 1
    return (args[i], args[i + 1:]) if i < len(args) else ("", [])


def judge(command, depth=0):
    """A short reason to block this command line, or None."""
    parts = segments(command)
    for number, words in enumerate(parts):
        start = program_index(words)
        if start >= len(words):
            continue
        program, args = os.path.basename(words[start]), words[start + 1:]
        if program in {"sudo", "doas"}:
            return "commands run as another user are not for agents"
        if program == "rm" and any(a == "--recursive" or re.fullmatch(r"-[A-Za-z]*[rR][A-Za-z]*", a) for a in args):
            return "deleting a directory tree needs a human"
        if program == "git":
            sub, rest = git_subcommand(args)
            if sub == "push":
                return "pushing is for a human"
            if sub == "reset" and "--hard" in rest:
                return "git reset --hard throws work away"
            if sub == "clean" and any(re.fullmatch(r"-[A-Za-z]*f[A-Za-z]*", a) or a == "--force" for a in rest):
                return "git clean -f deletes untracked files"
        if program in INSTALLERS and INSTALLERS[program] in args:
            return "adding a dependency needs a ticket and a second reviewer (CONTRIBUTING.md)"
        if program.startswith("python") and "-m" in args and "pip" in args and "install" in args:
            return "adding a dependency needs a ticket and a second reviewer (CONTRIBUTING.md)"
        if program in {"curl", "wget"} and number + 1 < len(parts):
            following = parts[number + 1]
            at = program_index(following)
            if at < len(following) and os.path.basename(following[at]) in INTERPRETERS:
                return "downloaded text must not be piped into a shell"
        if program in SHELLS and "-c" in args and depth < 3:
            index = args.index("-c")
            if index + 1 < len(args):
                reason = judge(args[index + 1], depth + 1)
                if reason:
                    return reason
        for word in words[start + 1:]:
            if SECRET_PATH.search(word) or (ENV_FILE.search(word) and not word.endswith(SAFE_ENV_SUFFIXES)):
                return "that file may hold secrets"
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        block("the hook input is not JSON, so it cannot be checked")
    if not isinstance(data, dict) or data.get("tool_name") != "Bash":
        sys.exit(0)  # the matcher in settings.json sends only Bash here; anything else is not our business
    tool_input = data.get("tool_input")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str) or not command.strip():
        block("a Bash call without a command cannot be checked")
    try:
        reason = judge(command)
    except ValueError:  # shlex could not read it (an unclosed quote, say)
        block("this command line cannot be parsed, so it cannot be checked")
    if reason:
        block(reason)
    sys.exit(0)


if __name__ == "__main__":
    main()
