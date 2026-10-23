# A/B notes: Remit with and without project memory

The task is REMIT-252 (`lab-assets/ab-task.md`). Run it twice with the same tool, the same model and the same
prompt, each time in a fresh copy of the repository: A without the memory file, B with it. Replace each placeholder
with your own text. Report what happened. "No difference" is a valid result; an invented improvement is not.

How the grader reads this file: no placeholder left; each section has a few real words (Setup 8, What was different 12,
Limits 8, the memory changes 2: "Nothing yet." counts); the first four table rows are numbers (`~10`, `<1`, `0.4`, `none`
and a unit such as `min` are fine) and the last two are yes or no; each of the two quote sections starts with a block quote
(`>`) of at least 15 characters copied from your memory file, a different line in each.

## Setup

- Tool and model (or "chat assistant", "colleague", "by hand"): TODO
- The prompt, identical in both runs (paste it): TODO
- How the two copies were made, and anything that differed besides the memory file: TODO

## Results

| Measure | A: without memory | B: with memory |
|---|---|---|
| Minutes until I accepted the result | TODO | TODO |
| Wrong turns I had to correct | TODO | TODO |
| Files changed | TODO | TODO |
| Lines changed (added plus deleted) | TODO | TODO |
| `pytest -q` passes at the end (yes or no) | TODO | TODO |
| Commit message follows CONTRIBUTING.md (yes or no) | TODO | TODO |

A run under a minute is `<1`; do not round it up.

## What was different

TODO: in your own words, what the agent did differently with the memory, and what it did the same.

## The memory line that mattered

TODO: quote the one line of your memory that you can show changed what the agent did (copy it exactly, as a block quote).
If no line did, quote the line most likely to have mattered and say you could not show it.

## A memory line that changed nothing

TODO: quote a line that did not matter for this task (copy it exactly, as a block quote). Say whether you would delete it.

## What I changed in the memory afterwards

TODO: what you added, deleted or reworded because of what you saw.

## Limits of this comparison

TODO: one run each is an anecdote. Say what could explain the difference besides the memory.
