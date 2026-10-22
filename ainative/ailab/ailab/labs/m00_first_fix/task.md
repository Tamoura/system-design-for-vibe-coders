# REMIT-212: spelling mistake in the "transfer sent" message

**From:** Hessa, Product Owner, Najm Remit
**To:** Payments Platform
**Priority:** Low, but every customer who sends money sees it

A customer wrote to us: the English message we send after a transfer has a spelling
mistake in it. Please fix it.

Right now the test suite is red because of it. It is a good first task: small, safe, and
a chance to go through the whole loop once (find, fix, check, commit).

## What I need

1. The English "transfer sent" message is spelled correctly again.
2. `pytest -q` passes.
3. The change is as small as it can be: one message, nothing else. Please do not edit
   the tests; they are right.
4. It is committed as **one commit**, with a message that follows the team's rules in
   `CONTRIBUTING.md`.

## Notes

- Use whatever helps you: your editor, or an AI coding tool if you have one. If a tool
  makes the change, read the diff before you commit. You are the one who is accountable
  for it.
- Run `python -m ailab doctor` first if you have not already.
- When you think you are done, grade it from the `ailab` folder of the course repository:
  `python -m ailab grade m00 --dir <this directory>`
