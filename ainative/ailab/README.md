# ailab: the lab kit for "A Practical Guide to Becoming an AI-Native Engineer"

Every lab in the course is a real task on **one shared codebase**, *Najm Remit* (a small, fictional
money-transfer service, Python, standard library only). This kit gives you that codebase, sets up each lab's
situation, and **grades the work you did**, offline and for free.

> **An honest note about what this is.** The kit grades *work*. It does not run any AI model, call any API or
> use the network, and it cannot tell whether a person, an agent or a chat assistant produced a change. You
> can use whichever tool you like (the course shows Claude Code; others work), or none. The hidden tests live
> in this repository, so you could read them; that would only cheat yourself of the practice, because the
> point of each lab is the habit, not the green tick. Everything in Remit (the bank, customers, rates, fees,
> limits) is fictional.

## Install

You need Python 3.11 or newer and git.

```bash
git clone https://github.com/Tamoura/system-design-for-vibe-coders.git
cd system-design-for-vibe-coders/ainative/ailab
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt               # pytest, nothing else
python -m ailab doctor                                  # checks Python, git, pytest and a writable folder
```

Run `python -m ailab ...` from this folder (`ainative/ailab`). To run it from anywhere, put this folder on
`PYTHONPATH` (`export PYTHONPATH=/path/to/ainative/ailab`).

## Commands

```bash
python -m ailab list                                      # the labs, their lessons, whether they need an agent
python -m ailab doctor                                    # check your setup
python -m ailab start m00 --dir ~/ainative/m00            # create the work directory and print the task
python -m ailab grade m00 --dir ~/ainative/m00 [--json]   # check your work: PASS/FAIL per check, with hints
python -m ailab solve m00 --dir ~/ainative/m00            # apply the reference solution (a peek: try first)
```

* `start` copies the Remit repository to the directory (it must be new or empty), makes it a git repository
  on branch `main`, commits it as **"Initial state"**, applies the lab's situation, commits that as **"Lab
  starting state"** and tags it **`lab-start`**. It also puts the ticket in `TASK.md` and any lab material in
  `lab-assets/` (both are part of the starting commit, so `git add -A` is safe). `git diff lab-start` always
  shows what *you* changed.
* `grade` runs the lab's checks and prints one line each: `[PASS]` or `[FAIL]`, what was found, and a hint (never
  the answer). It exits with status 0 only when every required check passes, 1 when some do not, and 2 when it
  could not run (wrong directory, unknown lab). `--json` gives the same report for tools.
  Grading never changes your directory and never runs your code inside the grader's own process.
* `solve` refuses if you have already changed files (use `--force`). The reference solution is there for the kit's
  own tests and for when you are truly stuck.

## How a lab is structured

```text
ailab/labs/m04_limit_warning/
  lab.py        LAB = Lab(id="m04", title=..., lesson="4.2", needs_agent=..., seed=..., grade=..., solve=...)
  task.md       the ticket the learner reads (copied to TASK.md)
  assets/       optional: files copied to lab-assets/ (sessions, logs, skeletons)
  hidden/       optional: hidden pytest files used by the grader
  solution/     data for solve() (a patch, files, a commit message)
```

* `seed(work)` turns a fresh copy of Remit into the lab's starting situation (plants a bug, adds a branch...).
* `grade(work)` returns a list of `Check(name, ok, detail, hint, required)` built mostly from `ailab.checks`
  (run the repo's tests and hidden acceptance tests, diff size, files in scope, commit messages, secrets,
  mutation-style checks, JSON and Markdown validators).
* `solve(work)` applies the reference solution, commits included.

The rules every lab follows: **the starter fails the grader and the reference solution passes it** (the kit's
generic test enforces this for every lab); hidden tests run in a subprocess on a copy of your work with a
timeout; everything is deterministic and offline; a lab runs in well under 20 seconds.

`ailab/labs/m00_first_fix/` is the exemplar: read its `lab.py`, which is commented line by line.

## Add a lab (for course authors)

1. Read `KIT_NOTES.md`: the facts of the Remit repository (every signature, fictional constant, seeded quirk and
   known smell with its id), the helper reference and the checklist. Never contradict it.
2. Copy `ailab/labs/m00_first_fix/` to `ailab/labs/mNN_slug/` and edit `lab.py`, `task.md`, `hidden/`, `solution/`.
   The folder prefix must equal `LAB.id`. Never edit `ailab/base/remit/`: seeds change the repo, the base is frozen.
3. Write `tests/test_labs_mNN.py` with **negative tests**: the wrong answers a learner or an agent will really
   produce (special-casing the example, floats for money, editing the tests, unrelated changes, a missing commit),
   and at least one *alternative* correct solution. A grader must accept every sound solution.
4. Run **your lab's tests only** (the full suite may contain other writers' unfinished labs, which fail only their own cases):

   ```bash
   pytest -q tests/test_labs_mNN.py tests/test_labs_generic.py -k mNN
   ```

   `python -m ailab list` shows a lab that does not import as `BROKEN` with the error; `start`, `grade` and `solve`
   load only the lab you name.
5. Before you finish, run everything: `pytest -q` from this folder must pass.
6. If a lesson shows one of your files (a starter the learner edits), start the block with
   `# ailab/<path relative to ainative/ailab>` and keep it byte-identical; `python3 ailab/check_blocks.py` (from `ainative/`) checks it.

## Run the kit's own tests

```bash
cd ainative/ailab
python -m pip install -r requirements.txt
pytest -q                      # the whole kit: framework, CLI, helpers, the base repo, every lab
pytest -q tests/test_base.py   # for example, just the pristine base repository (its 99 tests run in a temporary copy)
```

The base repository has its own suite (`ailab/base/remit/tests`, run with `pytest -q` inside a started lab). The kit's
suite runs it in a temporary copy and checks the documented quirks against `KIT_NOTES.md`.

## What is where

| Path | What |
|---|---|
| `ailab/cli.py` | `list`, `doctor`, `start`, `grade`, `solve` |
| `ailab/framework.py` | `Check`, `Lab`, tolerant discovery, the start/grade/solve lifecycle, seed helpers, `add_reference_memory`, `doctor_checks` |
| `ailab/checks.py` | the helpers graders reuse |
| `ailab/gitutil.py`, `ailab/runner.py` | git and subprocess plumbing (timeouts kill the whole process group) |
| `ailab/base/remit/` | the Najm Remit repository (README, CONTRIBUTING, docs, `src/remit`, `src/najmkit`, tests) |
| `ailab/labs/` | the labs |
| `ailab/stubs/claude` | a **stand-in** for the `claude` command, used by lab m09 only: it is not Claude Code, calls no model and needs no key; it imitates the documented shape of print mode (`claude -p`, `--output-format json`, `--max-turns`, exit codes) and classifies tickets with a keyword table, so a script can be graded offline |
| `tests/` | the kit's own tests |
| `check_blocks.py` | keeps lesson code blocks identical to the kit files they show |
| `KIT_NOTES.md` | the facts for lab and lesson writers |
