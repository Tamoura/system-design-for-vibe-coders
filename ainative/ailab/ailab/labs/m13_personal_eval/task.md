# GROW-13: your personal eval and your 90-day plan

**From:** Tariq, Engineering Lead, Payments Platform
**To:** you
**Priority:** Normal. Do it this week, then revisit it every month.

Tools change every few months, and a leaderboard cannot say which one is good at *our* work. I want two things you
keep: an eval you run yourself, and a plan that keeps your skills growing. Use an AI assistant if you like; you must
be able to explain every task and every number. Run commands in your lab repository unless told otherwise.

### 1. A personal eval: `eval/tasks.jsonl`

At least **eight different tasks** you would really give a coding agent, as JSON Lines: one complete JSON object per
line, no array. At least six must be about this repository; the rest may come from your own project (`"repo": "own"`;
the kit cannot run those, but they count). The four examples in `lab-assets/tasks.example.jsonl` do not count, and
copies of one task count once. A task has:

* `id` (unique, for example `"T01"`), `title`, `kind` (`fix`, `feature`, `refactor`, `test`, `docs`, `explain`,
  `review` or `other`) and `prompt`: the exact words you would give a tool, 15 words or more.
* `check`: `{"run": "<command>", "guard": "<command>"}`. `run` decides pass or fail. The optional `guard` must pass
  before the work and after a correct solution, so a tool that fixes the task and breaks something else fails.
* `reference`: a `.patch` file under `eval/` holding a solution you trust. Every task about this repository needs one;
  a docs, explain or review reference, or any that changes only text files, must change eight words or more.
* Optional `setup`: a `.patch` file under `eval/` that plants the starting situation (a bug, a file to review).

A check is one command (`pytest`, `python`, `grep` or read-only `git`; no shell operators; offline), kept under
`eval/` (for example `eval/checks/`) so a tool never sees it. It runs from the root of a clean copy of the repository,
a git repository with one commit, so `git diff` shows what a solution changed. There `PYTHONPATH` is `src`; `python`
and `pytest` are the runner's interpreter; paths are relative, with forward slashes; a command gets 60 seconds;
secret-looking environment variables are removed. (`grep` is missing on some systems; a Python script always works.)
A check must:

1. **fail on the untouched repository** (the `lab-start` state): a check that passes before any work proves nothing;
2. **pass on the reference**;
3. **reject a lazy answer**: a placeholder or filler note, a test that asserts nothing, or a stray edit must not pass.

`python lab-assets/eval_runner.py validate`, `baseline` and `verify` test all three; `baseline` prints why each check
fails, so read it. Also write `eval/README.md` (60 words or more): how to run the eval, what counts as a pass, how
many repeats, when you rerun it.

### 2. A 90-day plan: `plan.md`

Start from `lab-assets/plan-template.md` and keep its headings: a start date, a skills map for six skills, a weekly
routine (minutes per practice), three to six goals, days 1-30, 31-60 and 61-90, your eval cadence, and what you will
ignore. Write dates as YYYY-MM-DD. A goal has a metric, a baseline, a target with a number, a date inside the 90 days
and a way to measure it.

### Done when

Only `eval/` and `plan.md` changed, in at least two commits that follow `CONTRIBUTING.md` (for example
`test(eval): ...` and `docs(plan): ...`; any lower-case scope works), and everything is committed, except the log
`eval/results.jsonl` that `score` writes. Grade it from the `ailab` folder of the course repository:
`python -m ailab grade m13 --dir <this directory>`
