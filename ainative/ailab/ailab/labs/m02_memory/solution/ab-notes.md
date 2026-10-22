# A/B notes: Remit with and without project memory

The task is REMIT-252 (`lab-assets/ab-task.md`). Run it twice with the same tool, the same model and the same
prompt, each time in a fresh copy of the repository: A without the memory file, B with it. Replace each placeholder
with your own text. Report what happened. "No difference" is a valid result; an invented improvement is not.

*Illustrative reference notes, constructed for the kit's own tests. They are not a recording of a real model run;
yours must come from your own runs.*

## Setup

- Tool and model (or "chat assistant", "colleague", "by hand"): an agentic coding tool in Manual permission mode (constructed example)
- The prompt, identical in both runs (paste it): the text of `lab-assets/ab-task.md`, pasted whole, followed by "Plan first. Commit when the tests pass."
- How the two copies were made, and anything that differed besides the memory file: two `ailab start m02` directories with the lab files removed; B also had `CLAUDE.md` committed before the session. Same machine, same day, new session each time.

## Results

| Measure | A: without memory | B: with memory |
|---|---|---|
| Minutes until I accepted the result | 22 | 14 |
| Wrong turns I had to correct | 3 | 1 |
| Files changed | 3 | 2 |
| Lines changed (added plus deleted) | 71 | 46 |
| `pytest -q` passes at the end (yes or no) | yes | yes |
| Commit message follows CONTRIBUTING.md (yes or no) | no | yes |

## What was different

In A the agent ran `python -m remit quote` without `PYTHONPATH=src`, got a ModuleNotFoundError and spent two turns on it. It
serialised amounts with `float()` first, and I had to ask for strings. It also put a new test file in a new folder. It committed as
"add json output to quote". In B it used the documented command, kept the amounts as strings, added its tests to the existing CLI test
file and wrote a scoped commit message. Both versions passed `pytest -q`, and both left the plain-text output unchanged.

## The memory line that mattered

> IMPORTANT: money is `Decimal`, never `float`. Use `Money` from `src/remit/money.py`: it rounds half up and raises `TypeError` on a float.

## A memory line that changed nothing

> Every message to a customer exists in English and Arabic (`TEMPLATES` in `src/remit/notify.py`); change both.

I would keep it for tasks that touch notifications, but this task never went near them. It is the first line I would review at the next prune.

## What I changed in the memory afterwards

Nothing yet. B still needed one search for the CLI test file, but a rule added after one run is a guess. I will add the file name only if it costs time again.

## Limits of this comparison

One run each is an anecdote: the agent is not deterministic, and A may have been unlucky. I also knew which run was which and judged
"wrong turn" myself. Next time I would repeat A and B twice, and have a colleague count the wrong turns from the diffs.
