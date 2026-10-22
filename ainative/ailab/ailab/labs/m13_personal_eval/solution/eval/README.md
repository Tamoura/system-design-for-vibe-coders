# My Najm Remit eval

Nine tasks that I would really give a coding agent. Eight run on the Najm Remit repository; T09 comes from
my own project, so the course kit cannot run it. Each task is a prompt plus a check that decides pass or fail.

## How to run it

1. `python lab-assets/eval_runner.py validate` and `baseline`: the file is valid, and every check fails on a
   clean copy of the repository (a check that passes before any work proves nothing).
2. `python lab-assets/eval_runner.py verify`: every reference solution makes its check pass, and a
   placeholder answer does not.
3. `prepare T03 --dir ../runs/T03-claude`: a clean workspace without `eval/`, so the tool cannot read the check.
   Give the tool the prompt printed by `prepare`, nothing else.
4. `score T03 --dir ../runs/T03-claude --tool claude-code --model sonnet --minutes 6 --note "..."`.
5. `report`: pass counts per tool and model.

## What counts as a pass

The check passes and the guard passes. A guard is a command that must keep passing, for example the whole
test suite: a tool that fixes the task and breaks something else fails. I read the diff of every pass before I
trust it; the check is a floor, not a review.

## Repeats, and when I run it again

A single run proves little because the same tool can pass one day and fail the next. I run every task at least
three times per tool and model, from a clean workspace each time, and record minutes and what I corrected.
I run the whole eval again when a model or tool version changes and every month, whichever comes first.
