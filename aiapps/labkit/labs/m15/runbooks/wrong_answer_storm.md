# Runbook: wrong-answer storm, Najm Desk
<!-- Quality incidents raise no error. Someone has to notice: users, the desk, or a canary question. -->
Owner: Yara (domain) and Lujain (builder)   Last drilled: TODO date   Version: 1

## Trigger
Thumbs-down or "that is wrong" reports rise above the weekly norm; the desk reports staff quoting wrong policy; the daily canary questions fail; the share of answers with a citation drops on the dashboard (the lab's trace report shows it only after you add a `cited` flag to `stop`).

## First five minutes
1. Is the wrong answer harmful (security advice, an access decision, a deadline)? Then press the kill switch (`kill_switch.md`).
2. Save three example run ids (the user's reference) before anything changes.

## Diagnose
1. What changed? `python labs/m15/trace_report.py TRACE --by release` and `--by prompt_version`: did the bad share start at a release?
2. Is the cited passage itself wrong or stale? Open it in the policy library and check its date and owner.
3. Is retrieval missing the right passage? Run the question through the retrieval step alone.

## Fix or mitigate
Bad release or prompt: roll back to the previous version (`change_prompt_or_model.md`, step "Promote or roll back"). Wrong or stale passage: the policy owner fixes or removes it, then reindex. Retrieval gap: hand-off for that topic until fixed (builder).

## Tell people
Yara tells the desk which topics to double-check and what the right answer is. Hind hears if staff acted on a wrong answer.

## Recover and resume
Re-run the eval set and the three saved examples. Resume only when the eval gate is green and the examples are right.

## After
Each wrong answer becomes an eval case with its requirement id. Postmortem if staff acted on it.
