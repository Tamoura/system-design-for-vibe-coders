# My 90-day plan

Start date: 2026-11-02

## Where I am

| Skill | Last did it without AI | Confidence (1-5) | Evidence |
|---|---|---|---|
| Reading unfamiliar code | September, the screening module | 3 | I could trace a transfer through send() without help, but not the fuzzy matching |
| Debugging | August, a failing fixture | 3 | I find the cause quickly when the failure reproduces, slowly when it does not |
| Systems thinking | July, drawing the quote flow | 2 | I could not say what breaks when the ledger posts and the store fails |
| Data structures | June, a coding practice site | 3 | I pick lists and dicts well, and guess at heaps and graphs |
| Testing | October, three fee tests by hand | 4 | I write boundary tests first and can say what a mutation test shows |
| Security basics | September, the quote-mark search bug | 2 | I can spot string-built SQL but not explain a full threat model |

## Weekly routine

| Day | Practice | Minutes |
|---|---|---|
| Monday | One kata without the agent, then the agent as a tutor for hints only | 45 |
| Wednesday | Read one merged pull request from another team and write what I would have asked | 30 |
| Thursday | Explain-back: tell a colleague what the agent changed and why, without notes | 20 |
| Friday | Release notes and one small experiment with a new feature, written up in five lines | 25 |
| Sunday | Review my agent log: what I corrected, what I accepted too fast | 20 |

## Goals

| Goal | Metric | Baseline | Target | By | How I will measure it |
|---|---|---|---|---|---|
| Debug more of my own bugs unaided | Bugs found and fixed without asking the agent first | 0 in the last month | 6 | 2026-12-15 | A tally in my agent log, checked against the git history |
| Keep my review skill sharp | Seeded flaws I find in the practice pull requests | 4 of 7 in m05 | 6 of 7 | 2026-12-31 | Re-run the review exercise on a fresh branch and count |
| Know which tool is good at what | Pass rate of my eval per tool, three runs each | no eval yet | 8 tasks run 3 times | 2027-01-15 | eval/results.jsonl and the report command |
| Explain every change I ship | Pull requests where I can explain every line to my reviewer | not tracked | 10 of 10 | 2027-01-31 | A reviewer comment or a tick in my notes after each pull request |

## Days 1-30

Set up the weekly routine and keep it for four weeks. Run the baseline and verify commands until all eight
Remit tasks pass both. Count my unaided debugging sessions from the first day so I have a real baseline.

## Days 31-60

Run each eval task three times with the tool I use every day, record minutes and corrections, and read the
diffs of the passes. Pick one weak skill from the map, systems thinking, and read one design document a week.

## Days 61-90

Run the eval on a second tool or model, compare the pass rates and the minutes, and write a one-page note for
Tariq: which tasks I would hand to which tool, and which I keep. Re-score the skills map honestly.

## Eval cadence

I run the eval again every month and whenever my main tool or model changes. The result decides what I
delegate: a task type with fewer than two passes in three goes back to me, with the agent as a reviewer.
I add one new task from real work each month and drop one that no longer matches my work.

## What I will ignore

Weekly leaderboard changes, announcements with no release notes, and tools I have no task for. I look at a new
tool only when a task in my eval fails for every tool I already have.
