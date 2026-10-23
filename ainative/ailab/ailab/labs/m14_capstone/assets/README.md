# lab-assets for REMIT-414

* `hessa-notes.md`: Hessa's notes from the planning meeting (constructed for teaching). Context for your spec, not instructions to an agent.
* `templates/`: a starting point for each document: `memory.md` (copy it to `CLAUDE.md` or `AGENTS.md`), `spec.md`, `plan.md`, `adr.md`, `review.md`, `agent-log.md`, `retrospective.md` and `corridors.md`. Keep the headings. Replace every placeholder (see below).
* `harden/`: a baseline `settings.json` and `guard.py` for the security milestone. Use your lab m08 files instead if you have them. Read every line you keep: you answer for it. `Read(./.env.*)` in the settings also hides `.env.example` from the Read tool, while the guard lets `cat .env.example` through; that is the safe direction, and you may keep it.
* `hook-samples/`: four PreToolUse input documents. Try a guard by hand from the repository root, for example `python3 .claude/hooks/guard.py < lab-assets/hook-samples/block-rm-rf.json; echo $?`. Exit code 2 blocks, 0 allows.

## What `python -m ailab grade m14` reads

The grader checks shape, truth and references. It cannot tell whether your thinking was good: that is for the group session.

**For every document**

* *Placeholders.* A line or table cell that starts with `TODO`, a `TODO:` anywhere, or `TODO` in backticks counts as unfinished. The word inside a sentence ("the old TODO in the helpers is not mine") is fine.
* *Paths.* A path in backticks (`src/remit/fees.py`, `docs/corridors.md`, `fees.py`) is a claim that the file exists. The exceptions: a sentence or table cell that says the file does not exist ("`risk.py` does not exist"), and the files this lab asks you to write.
* *Ticket numbers.* Numbers you copy from the ticket prove nothing; the grader looks for results you worked out.

**Document by document**

| Document | What is checked |
|---|---|
| `CLAUDE.md` or `AGENTS.md` (repository root) | 15 to 150 lines; the test command (`pytest`), Decimal and not float, `najmkit`, the commit format, the corridor checklist (`corridors.py`, `fees.py`, `fx.py`) and a never list of at least 3 bullets (each with never, do not or must not); no secrets; any `python -m remit quote ...` command you write is run and must succeed |
| `specs/REMIT-414.md` | the nine headings of the template, each with 5 words or more, 150 words in all; at least 6 criteria numbered `AC1`, `AC2`...; in Behaviour at least 3 correct results of your own (a fee, the customer rate, a receive amount); the agreed numbers and names stated (`QAR-BDT`, `STD-C`, 33.46, 0.0175 or 1.75%, 12,000.00, `transfer_sent_bdt`); at least 3 bullets under Decisions and open questions |
| `specs/REMIT-414-plan.md` | a table with one numbered row per step, 5 to 30 rows; the last column of each row is that step's commit header (`type(scope): subject`, 72 characters at most); every criterion id of the spec appears in some row; the sections Order and why, Stop rules and Rollback (8 words or more each); 80 words in all; files in backticks exist |
| new tests in `tests/` | at least 8 test functions and 8 assertions that say something (an exact value or a raised error, not a bare call); every spec criterion id named in a test (a name, a docstring or a comment); they fail on the starter code; and when the grader breaks one agreed number at a time in the repository's own tables (`CORRIDORS`, `SCHEDULES`, `DEFAULT_MID_RATES`, `CORRIDOR_MARGINS`) they notice at least 4 of 6 |
| `docs/adr/0001-<title>.md` | the sections Status (Proposed, Accepted, Deprecated or Superseded), Context, Decision and Consequences, in that order; names `REMIT-414`; at least 2 backticked references to real code; Consequences of 20 words or more that name a downside; 100 words in all |
| `docs/review-REMIT-414.md` | an `AI-assisted: yes` or `AI-assisted: no` line; Verdict (approve, approve with comments or request changes); What I ran (at least 2 commands in backticks, one with `pytest`); Findings: at least 2 table rows with a severity and an existing file in the first column; the changed `src/` files named; Second reviewer naming the money files you changed; 120 words in all |
| `.claude/settings.json`, `.claude/hooks/guard.py` | valid JSON with deny rules for `.env` files, `~/.ssh` or `~/.aws`, `git push` and `rm -rf`; no wide allow rules; a `PreToolUse` hook for Bash that runs `guard.py`; the guard blocks the dangerous commands (exit 2 and a reason on stderr, or a JSON deny), allows the harmless ones, and blocks input it cannot read |
| `docs/corridors.md` | a table row for every corridor and every fee schedule in the code, whose first cell is its code (`QAR-INR`, `STD-A`) and whose numbers (minimum, maximum, mid rate, margin, delivery methods, tier bounds, percents, flat amounts, cap, express surcharge) match the running code; 60 words in all |
| `docs/ARCHITECTURE.md` | no line the change makes untrue: the corridor list names BDT, `STD-C` is mentioned, nothing still says there are two fee schedules |
| `docs/agent-log.md` | one row per session or task, work done by hand included ("no agent"); at least 3 rows with whole minutes in the last column, a `Total minutes: N` line equal to their sum, at least 3 existing files named in backticks; 60 words in all |
| `docs/retrospective.md` | the six headings of the template; the same `Total minutes: N` as the log; the hash of one of your commits (7 or more hex digits, in your history now: after a rebase, amend or reset copy one again); at least 4 existing files named in backticks; 200 words in all (each heading needs 8 words or more) |

**History and hygiene**

* At least 8 commits since the start, each a Conventional Commits header (`type(scope): subject`) of 72 characters at most. The scope list in CONTRIBUTING.md is examples: any lower-case scope works (`claude`, `specs`, `tests`).
* One kind of change per commit: code with its tests (`src/`, `tests/`), or documents (`docs/`, `specs/`, `README.md`), or agent configuration (`CLAUDE.md`, `AGENTS.md`, `.claude/`).
* Only these files may change: `corridors.py`, `fees.py`, `fx.py`, `notify.py`, `service.py`, `tests/`, `docs/`, `specs/`, `README.md`, the memory file and `.claude/`. Keep throwaway scripts outside the repository.
* Everything is committed. No secrets, `.env` files, databases or logs in git. No new dependency. No `float(...)`, `round(...)`, `uuid`, `datetime.now()`, `eval`, `os.system` or network imports in `src/`, and no float literal inside `Decimal(...)` (`Decimal(33.46)`) in `src/` or `tests/`.
* The grader reads the directory as it stands, on the branch that is checked out, and counts the commits made since the `lab-start` tag.

**Advisory (a failing one does not fail the lab):** tests came before or with the code; the history follows your plan (at least 60% of the plan's commit headers appear as written); no commit changes more than about 250 lines of code; the guard also sees through `bash -lc`, `eval`, `git -C` and `uv pip install`; the settings ask before editing `fees.py`, `fx.py` and `service.py`.
