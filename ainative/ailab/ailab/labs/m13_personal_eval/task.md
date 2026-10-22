# GROW-13: your personal eval and your 90-day plan

**From:** Tariq, Engineering Lead, Payments Platform
**To:** you
**Priority:** Normal. Do it this week, then revisit it every month.

Tools change every few months, and a leaderboard cannot say which one is good at *our* work. I want two things you
keep: a small eval you run yourself, and a plan that keeps your skills growing. Use an AI assistant if you like;
you must be able to explain every task and every number.

### 1. A personal eval: `eval/tasks.jsonl`

At least **eight tasks** you would really give a coding agent, as JSON Lines: one complete JSON object per line, no
array. `lab-assets/tasks.example.jsonl` has three worked examples (they do not count). A task has:

* `id` (unique, for example `"T01"`), `title`, `kind` (`fix`, `feature`, `refactor`, `test`, `docs`, `explain`,
  `review` or `other`) and `prompt`: the exact words you would give a tool, 15 words or more.
* `check`: `{"run": "<command>", "guard": "<command>"}`. `run` decides pass or fail. The optional `guard` must pass
  before the work and after a correct solution, so a tool that fixes the task and breaks something else fails.
* Optional `setup` and `reference`: `.patch` files under `eval/`. A setup plants the starting situation (a bug, a
  file to review); a reference is a solution you trust.
* Optional `"repo": "own"` for a task from your own project, which the kit cannot run. At least six tasks must be
  about this repository.

A check is one command (`pytest`, `python`, `grep` or a read-only `git` command; paths relative to the repository
root; no shell operators; offline), kept in `eval/checks/` so a tool never sees it. It must:

1. **fail on the untouched repository** (the `lab-start` state): a check that passes before any work proves nothing;
2. **pass on a reference solution**: give at least three tasks a `reference`;
3. **reject a lazy answer**: an empty note, or a test that asserts nothing, must not pass.

`python lab-assets/eval_runner.py validate`, `baseline` and `verify` test all three. Also write `eval/README.md`
(60 words or more): how to run the eval, what counts as a pass, how many repeats, when you run it again.

### 2. A 90-day plan: `plan.md`

Start from `lab-assets/plan-template.md` and keep its headings: a start date, a skills map for six skills, a weekly
routine (minutes per practice), three to six goals, days 1-30, 31-60 and 61-90, your eval cadence, and what you will
ignore. A goal has a metric, a baseline, a target with a number, a date inside the 90 days and a way to measure it.

### Done when

Only `eval/` and `plan.md` changed, in at least two commits (the eval, then the plan) that follow `CONTRIBUTING.md`.
Grade it from the `ailab` folder of the course repository: `python -m ailab grade m13 --dir <this directory>`
