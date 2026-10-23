"""Helpers that only lab m00 uses (kept out of ``checks.py``, which belongs to the kit).

Why m00 has its own versions of a few generic checks
----------------------------------------------------
The generic helpers in ``checks.py`` are right for most labs, but a first lab is read by people who have never
used the kit, and in a first lab a wrong hint costs the most. Four things needed more care here:

* **Which branch is graded.** The grader reads the branch that is checked out. A learner who commits on a task
  branch and then switches back to ``main`` has not lost the commit, so the "no commits" hint must not tell them
  to commit again; it names the branch that holds the work. A merge commit (``git merge --no-ff``) is not a
  second change, so it is not counted.
* **Getting back to one commit.** The ticket demands exactly one. ``git rebase -i`` is hard for a beginner and
  does not work in many agent shells, so the hint gives ``git reset --soft lab-start`` and a new commit.
* **"Tiny" means exactly one word.** A size limit alone lets an unrelated edit of a few lines slip through, so
  the file must equal the starter with the misspelling corrected and nothing else (whitespace at line ends and
  line-ending style are ignored).
* **The commit message.** CONTRIBUTING.md defines the shape; this ticket fixes a customer-visible mistake in
  one module, so the type is ``fix`` and the scope is that module. The subject must say something, be in the
  imperative (not "fixed"), and not end in punctuation. All of this is written down in TASK.md and lesson 0.2.

Nothing here runs learner code in-process; the pytest-based checks still go through ``checks.run_*``.
"""
from __future__ import annotations

import difflib
import re
from pathlib import Path

from ailab import checks, gitutil
from ailab.framework import LAB_START_TAG, Check

# The one file a correct fix touches, and the word that is wrong in it.
TEMPLATE_FILE = "src/remit/notify.py"
WRONG_WORD = "recieved"
RIGHT_WORD = "received"
SCOPE = Path(TEMPLATE_FILE).stem  # "notify": the module the fix touches
TYPE = "fix"
MAX_CHANGED_LINES = 6

NAME_ONE_COMMIT = "Exactly one new commit"
NAME_MESSAGE = "Commit messages follow CONTRIBUTING.md"
NAME_TINY = "The change is tiny"
NAME_HIDDEN = "The message is right in English and Arabic"
NAME_UNEDITED = "The tests were not edited"
NAME_CLEAN = "The fix is committed (nothing left over)"

COMBINE_HINT = (
    "Combine your commits into one: `git reset --soft lab-start`, then `git commit` once with a message "
    "that follows CONTRIBUTING.md."
)


def _short(items: list[str], limit: int = 4) -> str:
    shown = ", ".join(items[:limit])
    return shown + (f" (+{len(items) - limit} more)" if len(items) > limit else "")


# ---------------------------------------------------------------------------------------------
# commits: how many, where, and what the message says
# ---------------------------------------------------------------------------------------------
def real_commits(work: Path, ref: str = "HEAD") -> list[gitutil.Commit]:
    """The commits on ``ref`` since the start, merge commits left out (a merge is not a second change)."""
    return [c for c in gitutil.commits_since(work, LAB_START_TAG, ref) if not c.is_merge]


def _where_is_my_commit(work: Path) -> tuple[str, str]:
    """When the checked-out branch has no new commit: (extra detail, hint). Names another branch that has one."""
    here = gitutil.current_branch(work)
    where = "the commit you have checked out" if here == "HEAD" else f"the branch you are on ({here})"
    others = []
    for branch in gitutil.branches(work):
        if branch != here:
            n = len(real_commits(work, branch))
            if n:
                others.append((branch, n))
    if others:
        branch, n = others[0]
        detail = f" on {where}; branch {branch} has {checks.plural(n, 'new commit')}"
        hint = (f"Your work is on branch {branch}, but the grader reads the branch that is checked out. "
                f"Run `git switch {branch}` and grade again.")
        return detail, hint
    return "", "Commit your finished change (git add -A && git commit)."


def wrong_branch(work: Path) -> str | None:
    """The branch that holds the learner's commit when the checked-out branch is still at the start.

    Only when the checked-out branch has no new commit AND nothing is changed in the work tree, so the work can
    only be elsewhere. Then every failing line would otherwise tell the learner to do what they already did.
    """
    if real_commits(work) or gitutil.changed_files(work, LAB_START_TAG):
        return None
    here = gitutil.current_branch(work)
    for branch in gitutil.branches(work):
        if branch != here and real_commits(work, branch):
            return branch
    return None


def point_at_branch(results: list[Check], branch: str) -> list[Check]:
    """Replace the hint of every failing check with the one thing to do: switch to the branch with the work."""
    note = (f"Your work is on branch {branch}, but the grader reads the branch that is checked out. "
            f"Run `git switch {branch}` and grade again.")
    for check in results:
        if not check.ok:
            check.hint = note
    return results


def one_commit(work: Path) -> Check:
    commits = real_commits(work)
    merges = len(gitutil.commits_since(work, LAB_START_TAG)) - len(commits)
    detail = f"{checks.plural(len(commits), 'new commit')} since the start"
    if len(commits) == 1:
        return Check(NAME_ONE_COMMIT, True, detail + (" (a merge commit is not counted)" if merges else ""))
    if not commits:
        extra, hint = _where_is_my_commit(work)
        return Check(NAME_ONE_COMMIT, False, detail + extra, hint)
    return Check(NAME_ONE_COMMIT, False, detail, COMBINE_HINT)


_SHAPE = re.compile(r"^(?P<type>[A-Za-z]+)\((?P<scope>[^)]*)\)(?P<bang>!)?:(?P<space>\s?)(?P<subject>.*)$")
# Imperative verbs that merely end in "ed" or "ing".
_IMPERATIVE_OK = {"embed", "need", "speed", "feed", "seed", "proceed", "succeed", "exceed", "bleed", "shed", "breed",
                  "bring", "string"}


def header_problems(header: str) -> list[str]:
    """What is wrong with this commit header for THIS ticket (empty = fine).

    First the generic CONTRIBUTING.md rules (``checks.commit_header_problems``), with clearer words for the
    mistakes beginners make (several scopes, capital letters, no space after the colon). Only a header with a valid
    shape is then held to the ticket's own expectations.
    """
    problems = checks.commit_header_problems(header)
    shape = _SHAPE.match(header)
    if shape is not None:
        specific = []
        if shape["type"] != shape["type"].lower():
            specific.append("the type must be lower case")
        if not re.fullmatch(r"[a-z0-9][a-z0-9._/-]*", shape["scope"]):
            specific.append("the scope must be one lower-case word such as the module name (no commas, spaces or capitals)")
        if not shape["space"]:
            specific.append("put a space after the colon")
        if specific:
            problems = specific + [p for p in problems if "does not look like" not in p]
    if problems:
        return problems
    shape = _SHAPE.match(header)
    if shape is None:  # cannot happen when the generic check found nothing, but stay safe
        return ["it does not look like `type(scope): subject`"]
    out: list[str] = []
    if shape["type"] != TYPE:
        out.append(f"this ticket fixes a customer-visible mistake, so the type is `{TYPE}`, not `{shape['type']}`")
    if shape["scope"] != SCOPE:
        out.append(f"the scope `{shape['scope']}` is not the module you changed (the file name without .py)")
    subject = shape["subject"].strip()
    words = subject.split()
    if len(words) < 2 or len(subject) < 8:
        out.append("the subject should say what the change does, in a few words")
    if subject[-1:] in ".:;,!?…":
        out.append("the subject should not end with punctuation")
    first = re.sub(r"[^a-z]", "", words[0].lower()) if words else ""
    if first.endswith(("ed", "ing")) and first not in _IMPERATIVE_OK:
        out.append("start the subject with a verb in the imperative (`correct`, not `corrected` or `correcting`)")
    return out


def message(work: Path) -> Check:
    commits = real_commits(work)
    if not commits:
        extra, hint = _where_is_my_commit(work)
        return Check(NAME_MESSAGE, False, f"found 0 commits since the start; expected 1{extra}", hint)
    bad = []
    for commit in commits:
        problems = header_problems(commit.subject)
        if problems:
            bad.append(f'"{commit.subject}": {"; ".join(problems[:2])}')
    if bad:
        return Check(
            NAME_MESSAGE, False, _short(bad, 2),
            "Open CONTRIBUTING.md and follow its commit format. Rewrite the message with `git commit --amend` "
            "(or `git reset --soft lab-start` and commit again).",
        )
    return Check(NAME_MESSAGE, True, f"{checks.plural(len(commits), 'commit message')} checked")


def left_over(work: Path) -> Check:
    dirty = gitutil.status_porcelain(work)
    if not dirty:
        return Check(NAME_CLEAN, True)
    detail = f"{checks.plural(len(dirty), 'uncommitted change')}: {_short([d.strip() for d in dirty])}"
    if real_commits(work):
        hint = ("Fold it into your commit with `git add -A && git commit --amend --no-edit`, or discard it "
                "if you do not need it (a second commit would break \"one commit\").")
    else:
        hint = "Commit your work (git add -A && git commit) or discard what you do not need."
    return Check(NAME_CLEAN, False, detail, hint)


# ---------------------------------------------------------------------------------------------
# the change itself: one word, nothing else
# ---------------------------------------------------------------------------------------------
def _normal(text: str) -> list[str]:
    """Lines without line-ending style, trailing spaces or trailing blank lines (invisible edits do not count)."""
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return lines


def lines_beyond_the_fix(work: Path) -> list[int] | None:
    """Line numbers where the template file differs from "the starter with the misspelling corrected".

    ``[]`` means the file is exactly that. ``None`` means the file or the starter could not be read.
    """
    starter = gitutil.file_at(work, LAB_START_TAG, TEMPLATE_FILE)
    path = Path(work) / TEMPLATE_FILE
    if starter is None or not path.is_file():
        return None
    expected = _normal(starter.replace(WRONG_WORD, RIGHT_WORD))
    actual = _normal(path.read_text(encoding="utf-8", errors="replace"))
    differing: list[int] = []
    for tag, _i1, _i2, j1, j2 in difflib.SequenceMatcher(None, expected, actual, autojunk=False).get_opcodes():
        if tag != "equal":
            differing.extend(range(j1 + 1, max(j2, j1 + 1) + 1))
    return differing


def tiny(work: Path) -> Check:
    stat = gitutil.diff_numstat(work, LAB_START_TAG)
    detail = f"{checks.plural(stat.n_files, 'file')}, +{stat.added} -{stat.deleted} lines"
    if stat.total == 0:
        return Check(NAME_TINY, False, detail + " (nothing has changed yet)", "Fix the misspelled word first.")
    if stat.total > MAX_CHANGED_LINES or stat.n_files > 1:
        why = f" (limit {MAX_CHANGED_LINES} changed lines in {checks.plural(1, 'file')})"
        return Check(NAME_TINY, False, detail + why,
                     "This is a one-word fix. Look at `git diff lab-start` and undo everything else.")
    beyond = lines_beyond_the_fix(work)
    if beyond is None:
        return Check(NAME_TINY, False, detail + f" ({TEMPLATE_FILE} is missing or unreadable)",
                     "Look at `git diff lab-start` and restore the file.")
    if beyond:
        return Check(
            NAME_TINY, False,
            detail + f"; besides the misspelled word, {TEMPLATE_FILE} differs from the starter at line "
            + _short([str(n) for n in beyond], 5),
            "Change only the misspelled word, as the ticket says. `git diff lab-start` shows everything else you "
            "changed; undo it.",
        )
    return Check(NAME_TINY, True, detail)


# ---------------------------------------------------------------------------------------------
# the hidden tests, with a hint that fits what actually failed
# ---------------------------------------------------------------------------------------------
_ENGLISH_TESTS = {
    "test_english_transfer_sent_spells_received_correctly",
    "test_english_transfer_sent_is_otherwise_unchanged",
}
_OTHER_TEXT_TESTS = {"test_arabic_transfer_sent_is_unchanged", "test_transfer_failed_messages_are_unchanged"}
_SOURCE_TEST = "test_the_misspelling_is_gone_from_the_whole_source_tree"


def hidden_hint(failed: set[str]) -> str:
    parts = []
    if failed & _ENGLISH_TESTS:
        parts.append("Compare your customers' message with the sentence the failing test expects.")
        if _SOURCE_TEST in failed:
            parts.append("The wrong spelling must go from comments in src/ too.")
    elif _SOURCE_TEST in failed:
        parts.append("The message your customers get looks right, but the wrong spelling is still somewhere in src/: "
                     "a comment or docstring, or a fix applied only when the message is built. "
                     "Search src/ for it and fix it where it is written.")
    if failed & _OTHER_TEXT_TESTS:
        parts.append("The Arabic message and the failure messages must stay exactly as they were: "
                     "`git diff lab-start` shows what you changed.")
    return " ".join(parts) or "Run `pytest -q` and compare the messages your code builds with what the tests expect."


def hidden(work: Path, hidden_dir: Path) -> Check:
    result = checks.run_hidden_pytest(work, hidden_dir)
    if result.ok:
        return Check(NAME_HIDDEN, True, f"{checks.plural(result.passed, 'hidden check')} passed")
    if result.timed_out:
        return Check(NAME_HIDDEN, False, "the acceptance tests did not finish in time (an endless loop?)",
                     "Run `pytest -q` and read what it says.")
    if result.total == 0:
        return Check(NAME_HIDDEN, False,
                     "the acceptance tests could not run (does your code still import? run `pytest -q`)",
                     "Run `pytest -q` and read the first error from the top.")
    bad = result.failed + result.errors
    detail = f"{bad} of {result.total} hidden checks failed"
    if result.failures:
        detail += f": {_short(result.failure_names)}"
    return Check(NAME_HIDDEN, False, detail, hidden_hint(set(result.failure_names)))
