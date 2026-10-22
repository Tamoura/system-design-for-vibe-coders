---
name: review-change
description: Review the current change, or the files named in the arguments, against Najm Remit's team rules and report findings without editing anything. Use before opening a pull request.
argument-hint: "[files, or a git range such as main...HEAD]"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(git log *), Bash(git status *)
---
Review a change for the Payments Platform team. You report; you do not edit, create or delete any file.

What to review: $ARGUMENTS. If no argument was given, review the working tree against the last commit. Hand the reading to the remit-reviewer subagent, which can only read files, and put its findings into your report.

The state of the change right now:

!`git status --short`

!`git diff --stat HEAD`

Go through this checklist and answer each point with "ok" or with a finding:

1. Money is `Decimal` through the `Money` class. No `float` anywhere in money code; rounding is half up.
2. New behaviour has a test, and no existing test was edited, skipped or deleted to make the suite pass.
3. Scope: only the files the ticket needs have changed, and nothing else was "tidied" on the way.
4. No secrets, tokens or real customer data in code, tests, logs or commit messages.
5. Every message to a customer exists in English and Arabic.
6. Ids, time and audit events come from `najmkit`, not from `uuid` or `datetime.now()`.
7. Changes to money, fees, fx, limits, ledger or service need a second human reviewer: say so. AI-assisted changes carry the `AI-assisted` label.
8. Commit messages follow `type(scope): subject` from CONTRIBUTING.md.

Report one line per finding, in this form: `severity | file:line | what is wrong | how to check it`, where severity is blocker, major or minor. End with a verdict: ready, ready with minor changes, or not ready. You are the reviewer, not the author: never fix anything yourself.
