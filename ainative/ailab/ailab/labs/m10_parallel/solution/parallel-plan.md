# Parallel plan: REMIT-361 Customer Care desk pack

## Task graph

| Task | Branch | Done by | Depends on | Size |
|---|---|---|---|---|
| A delay notice | feat/delay-notice | one session | nothing | S |
| B corridors command | feat/corridors-command | one session | nothing | M |
| C limits command | feat/limits-command | one session | nothing | M |
| D runbook | docs/care-runbook | me, after B and C | B, C and A (it quotes their real output) | S |

D cannot be written in parallel with the others: it copies real output. B and C both edit cli.py.

## Boundaries

| Task | May change | Must not change | Contract it promises the others |
|---|---|---|---|
| A | notify.py, a new test file | everything else | template id transfer_delayed (name, transfer_id, recipient) |
| B | corridors.py, cli.py, a new test file | limits.py, notify.py | corridors.describe(corridor) -> one line |
| C | limits.py, cli.py, a new test file | corridors.py, notify.py | limits.usage_line(tier, history, now) -> one line |
| D | docs/CARE.md | all code | none |

Shared file: src/remit/cli.py (B and C, at the two markers and in the usage list). I resolve it.

## Merge order

1. A, then B, then C, then D.

Why: A touches nothing shared. B before C so the conflict is met once, on C's merge. D last, because it quotes the integrated program.

## Verification

| After | Command or check | Who looks | Stop and ask if |
|---|---|---|---|
| each branch, before merging | pytest -q; read the diff | me | the diff touches a file outside the task's list |
| each merge | pytest -q; run the new commands by hand | me | a test or command that worked before fails |
| the last merge | ailab grade; run every command once | me | any check fails |

## Limits

- Streams at once: three, because the diffs are short and I read each one.
- Time box: 30 minutes per task; after that I read what exists and decide whether to stop the session.
