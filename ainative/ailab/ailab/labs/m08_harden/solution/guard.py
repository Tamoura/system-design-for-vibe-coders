#!/usr/bin/env python3
"""PreToolUse guard hook for Najm Remit (reference solution of lab m08).

Claude Code runs this before every Bash tool call and writes one JSON document to its stdin. Exit code 0 lets the
call go ahead; exit code 2 blocks it, and whatever is written to stderr is given to the agent as the reason. Any
other exit code is a non-blocking error: the call RUNS. So this script must never crash, and anything it cannot
understand it blocks.

This is a guard rail, not a wall. It reads the command text; it cannot see what a script it launches will do.
The sandbox is the wall.
"""
import json
import os
import re
import shlex
import sys

SEPARATORS = {";", ";;", "&&", "||", "|", "|&", "&", "(", ")", "<(", ">(", "((", "))"}
SHELLS = {"sh", "bash", "zsh", "dash", "ksh", "fish"}
INTERPRETERS = SHELLS | {"python", "python3", "perl", "ruby", "node"}
WRAPPERS = {"env", "nohup", "nice", "time", "timeout", "command", "exec", "stdbuf", "setsid", "builtin", "xargs"}
CURL_UPLOAD = {"-d", "-F", "-T", "--upload-file", "--json"}
CURL_UPLOAD_PREFIXES = ("--data", "--form")
WGET_UPLOAD_PREFIXES = ("--post-file", "--post-data", "--body-file", "--body-data")
INSTALLERS = {
    "pip": {"install"}, "pip3": {"install"}, "pipx": {"install"}, "poetry": {"add"}, "uv": {"add"},
    "npm": {"install", "i", "add"}, "yarn": {"add"}, "pnpm": {"add", "install"}, "conda": {"install"},
}
GIT_OPTIONS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
MAX_DEPTH = 3

ENV_FILE = re.compile(r"(?:^|[/=@:])\.env(?:\.[\w-]+)*$")
SAFE_ENV_SUFFIX = (".example", ".sample", ".template", ".dist")
SECRET_PATH = re.compile(r"(?:^|/)\.(?:ssh|aws)(?:/|$)|(?:^|/)id_(?:rsa|dsa|ecdsa|ed25519)$|(?:^|/)\.(?:netrc|pypirc)$")
SUBSTITUTION = re.compile(r"\$\(([^()]*)\)|`([^`]*)`")


def block(reason):
    """Exit code 2 is the documented way to block; stderr is the message the agent sees."""
    print(f"Blocked: {reason}", file=sys.stderr)
    sys.exit(2)


def split_lines(command):
    """Turn newlines that are outside quotes into semicolons, so each line is judged on its own."""
    out, quote, escaped = [], None, False
    for char in command:
        if escaped:
            escaped = False
        elif char == "\\" and quote != "'":
            escaped = True
        elif quote:
            quote = None if char == quote else quote
        elif char in "'\"":
            quote = char
        elif char == "\n":
            char = ";"
        out.append(char)
    return "".join(out)


def tokenize(command):
    lexer = shlex.shlex(split_lines(command), posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    lexer.commenters = ""
    return list(lexer)


def segments(tokens):
    """Split a token list into (operator_before, words) pairs; redirections and their targets are kept as words."""
    result, current, before = [], [], ""
    for token in tokens:
        if token in SEPARATORS:
            if current:
                result.append((before, current))
            current, before = [], token
        else:
            current.append(token)
    if current:
        result.append((before, current))
    return result


def is_redirection(token):
    return bool(token) and all(char in "<>&|;()" for char in token) and token not in SEPARATORS


def words_of(segment):
    """The segment without redirection operators (the target of a redirection stays: it can name a secret)."""
    return [token for token in segment if not is_redirection(token)]


def command_word(words):
    """Index of the program in a segment: skip VAR=value prefixes and harmless wrappers (not sudo)."""
    i = 0
    while i < len(words):
        word = words[i]
        base = os.path.basename(word)
        if re.fullmatch(r"[A-Za-z_]\w*=.*", word):
            i += 1
        elif base in WRAPPERS:
            i += 1
            while i < len(words) and (words[i].startswith("-") or re.fullmatch(r"\d+[smhd]?", words[i])
                                      or re.fullmatch(r"[A-Za-z_]\w*=.*", words[i])):
                i += 1
        else:
            break
    return i


def is_recursive_rm(args):
    for arg in args:
        if arg == "--recursive" or re.fullmatch(r"-[A-Za-z]*[rR][A-Za-z]*", arg):
            return True
    return False


def git_subcommand(args):
    """(subcommand, rest) after git's own options, which may take a value (-C dir, -c key=value, ...)."""
    i = 0
    while i < len(args) and args[i].startswith("-"):
        i += 2 if args[i] in GIT_OPTIONS_WITH_VALUE else 1
    return (args[i], args[i + 1:]) if i < len(args) else ("", [])


def short_flags(args):
    letters = ""
    for arg in args:
        if re.fullmatch(r"-[A-Za-z]+", arg):
            letters += arg[1:]
    return letters


def judge_segment(words, before, previous, depth):
    start = command_word(words)
    if start >= len(words):
        # only assignments / wrappers: `env` on its own prints every variable
        return "printing the whole environment" if words and os.path.basename(words[0]) == "env" else None
    program = os.path.basename(words[start])
    args = words[start + 1:]

    if program in {"sudo", "doas"}:
        return "commands run as another user are not allowed for agents"
    if program == "printenv":
        return "printing the environment can reveal secrets"
    if program == "rm" and is_recursive_rm(args):
        return "deleting a directory tree (rm with a recursive flag) needs a human"
    if program == "find" and ("-delete" in args or "-exec" in args and "rm" in args):
        return "deleting files with find needs a human"
    if program == "git":
        sub, rest = git_subcommand(args)
        letters = short_flags(rest)
        if sub == "push":
            return "git push: publishing is done by a person, not an agent"
        if sub == "reset" and "--hard" in rest:
            return "git reset --hard throws work away"
        if sub == "clean" and ("f" in letters or "--force" in rest) and "n" not in letters and "--dry-run" not in rest:
            return "git clean -f deletes untracked files for good"
        if sub == "branch" and "D" in letters:
            return "git branch -D deletes a branch even if it is not merged"
    if program == "curl" and any(
        arg in CURL_UPLOAD or arg.startswith(CURL_UPLOAD_PREFIXES) or re.fullmatch(r"-[sSLkvfgiI]*[dFT]", arg) for arg in args
    ):
        return "curl sending data out"
    if program == "wget" and any(arg.startswith(WGET_UPLOAD_PREFIXES) for arg in args):
        return "wget sending data out"
    if program in INTERPRETERS and before in {"|", "|&"} and previous in {"curl", "wget"}:
        return "running downloaded code (a download piped into a shell or interpreter)"
    if program in INSTALLERS:
        sub = next((arg for arg in args if not arg.startswith("-")), "")
        if sub in INSTALLERS[program]:
            return "adding a dependency needs a ticket and a second reviewer, so a person does it"
    if program == "uv" and args[:2] == ["pip", "install"]:
        return "adding a dependency needs a ticket and a second reviewer, so a person does it"
    if program.startswith("python") and "-m" in args:
        at = args.index("-m")
        if args[at + 1:at + 2] == ["pip"] and "install" in args[at + 2:]:
            return "adding a dependency needs a ticket and a second reviewer, so a person does it"
    if program in SHELLS | {"eval"}:
        if program == "eval":
            nested = " ".join(args)
        else:
            nested = args[args.index("-c") + 1] if "-c" in args and args.index("-c") + 1 < len(args) else ""
        if nested and depth < MAX_DEPTH:
            inner = judge(nested, depth + 1)
            if inner:
                return inner
    if program.startswith("python") and "-c" in args and "rmtree" in " ".join(args):
        return "deleting a directory tree from Python needs a human"
    return None


def touches_credentials(token):
    if ENV_FILE.search(token) and not token.endswith(SAFE_ENV_SUFFIX):
        return "naming a real .env file (read .env.example instead)"
    if SECRET_PATH.search(token):
        return "naming a credential file (.ssh, .aws or a private key)"
    return None


def judge(command, depth=0):
    """Return a reason when the command must not run, otherwise None."""
    try:
        tokens = tokenize(command)
    except ValueError:
        return "the command could not be parsed (unbalanced quotes), so it cannot be checked"
    for token in tokens:
        for match in SUBSTITUTION.finditer(token):  # $(...) and `...` inside quotes still run
            inner = match.group(1) or match.group(2)
            if inner and depth < MAX_DEPTH and (reason := judge(inner, depth + 1)):
                return reason
        if reason := touches_credentials(token):
            return reason
    if re.search(r"(?:^|[\s;&|])(?:sh|bash|zsh|source|\.)\s+<\(\s*(?:curl|wget)\b", command):
        return "running downloaded code (process substitution)"
    previous = None
    for before, segment in segments(tokens):
        words = words_of(segment)
        reason = judge_segment(words, before, previous, depth)
        if reason:
            return reason
        start = command_word(words)
        previous = os.path.basename(words[start]) if start < len(words) else None
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:  # not JSON, empty, binary: do not crash (a crash exits 1 and the call would run)
        block("the hook input is not valid JSON, so the call cannot be checked")
    if not isinstance(data, dict):
        block("the hook input is not a JSON object, so the call cannot be checked")
    if data.get("tool_name") != "Bash":
        sys.exit(0)  # this guard only reads shell commands
    tool_input = data.get("tool_input")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str) or not command.strip():
        block("a Bash call without a command cannot be checked")
    try:
        reason = judge(command)
    except Exception:  # whatever went wrong, do not let the command through unchecked
        block("the command could not be analysed")
    if reason:
        block(reason)
    sys.exit(0)


if __name__ == "__main__":
    main()
