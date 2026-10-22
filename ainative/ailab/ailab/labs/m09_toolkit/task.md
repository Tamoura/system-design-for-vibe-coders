# REMIT-285: a project toolkit for AI-assisted work, and a triage script

**From:** Tariq (Engineering Lead) with Salem (Platform Engineering)
**To:** Payments Platform, everyone who uses an AI coding tool
**Priority:** Medium. We keep fixing the same things by hand.

Every review starts from a different pasted prompt. The agents that read our code can also edit it. A float slips into money
code about once a month. Hessa sorts forty support tickets a week by hand. Everything is local and fictional; `lab-assets/bin/claude` stands in for the `claude` program (no model, no key). No agent is needed; if you use
one, you stay accountable for every line.

**Part 1 — A review command: `.claude/skills/review-change/SKILL.md`** (or `.claude/commands/review-change.md`)

- Frontmatter between two `---` lines: a `description` of at least 8 words; `name`, if set, is `review-change`; only keys the
  skills documentation lists (Claude Code silently ignores any other). Pre-approved tools (`allowed-tools`), if any, cannot
  change files and none is a bare `Bash`; `Bash(git diff *)` is fine.
- The prompt says what to review (`$ARGUMENTS`, or a `` !`command` `` line), has a checklist of at least five points, covers at
  least four of the team's rules from `CONTRIBUTING.md` (money as `Decimal`, tests, scope, secrets, Arabic and English messages,
  `najmkit`, second reviewer and `AI-assisted` label, commit messages), and says it only reports.
  Advisory: a severity and `file:line` per finding; `disable-model-invocation` decided on purpose.

**Part 2 — A read-only reviewer: `.claude/agents/remit-reviewer.md`**

- Frontmatter: `name: remit-reviewer`; a `description` of at least 10 words; an explicit `tools` list with nothing that can
  change a file; only keys the subagents documentation lists. `model` and `maxTurns`, if set, must be valid; `permissionMode`
  must not widen anything. Advisory: no `Bash`, and a `maxTurns`.
- The body is its system prompt (at least 60 words): what it reviews, what to look for, that it must not edit, how to report.

**Part 3 — A post-edit hook: `.claude/hooks/post_edit.py` and `.claude/settings.json`**

Claude Code runs a `PostToolUse` hook after a successful `Edit` or `Write`, with one JSON document on standard input
(`lab-assets/hook-samples/` has four). The edit has already happened. Start from `lab-assets/post_edit_skeleton.py`.

- Not a `.py` file, no usable `file_path`, or a file that is gone: exit 0, silently.
- A `.py` file that does not parse: exit 2, and say on standard error which file and what is wrong.
- A `.py` file under `src/remit/` with a float literal (`0.15`, `1e-3`) or a call of `float(...)`: exit 2, and say that money is
  `Decimal`. A mention in a comment, docstring or string, or `isinstance(x, float)`, is not a float. Files outside `src/remit/`
  (tests above all: they use floats to prove `Money` rejects them) are not held to this. The untouched code must stay quiet.
- Input you cannot read is the hook's problem, not the agent's: never exit 2 for it. One line on standard error and exit 1
  (or 0), no traceback. Advisory: resolve a relative `file_path` against the document's `cwd`.
- `.claude/settings.json` registers the script under `hooks.PostToolUse`, matcher covering `Edit` and `Write`, as a `command`
  run from `$CLAUDE_PROJECT_DIR`.

**Part 4 — A triage script: `scripts/triage.py`**

`python scripts/triage.py TICKETS.json [--max-turns N] [--timeout SECONDS]` (defaults 3 and 60). `TICKETS.json` is a list of
`{"id": ..., "text": ...}` (samples in `lab-assets/tickets/`). Start from `lab-assets/triage_skeleton.py`. For each ticket run
`claude -p` once (the grader puts the stand-in first on `PATH`; read its docstring):

- Use `--output-format json`, `--max-turns N` and an explicit tool list that cannot change anything (`--tools` or
  `--allowedTools`: no bare `Bash`, `Edit` or `Write`; never skipped permissions). The ticket goes in on **standard input**
  (its text and nothing else; the instructions are the argument of `-p`), never in the command line.
- The reply must give `category` (bug, feature, question), `severity` (low, medium, high), `area` (fees, fx, limits, screening,
  notify, ledger, other) and `money_logic` (true or false). Accept nothing else. A reply may be fenced, not JSON, or out of
  range: report that ticket as an error, never guess. A non-zero exit is a failed run, whatever it printed. Retry at most once.
- Print **one JSON document** on standard output, `{"results": [...]}` in input order: `id`, `status: "ok"` and the four fields,
  or `id`, `status: "error"` and a non-empty `error`. Progress goes to standard error. Exit 0 when every ticket worked, 1 when
  some failed, 2 when the input is unusable (no such file, not a list).
  Advisory: `ok`, `failed`, `total_cost_usd` beside `results`; a budget cap per call; a working `--timeout`; the same input gives
  the same output; `money_logic` true for fees, fx, limits and ledger whatever the model said.

**Part 5 — What not to automate: `docs/automation-cards.md`**

Copy `lab-assets/automation-card-template.md` three times, under `## Card 1: run /review-change before every pull request`,
`## Card 2: let an agent approve and merge pull requests when the reviewer finds nothing` and
`## Card 3: run the triage script on every new support ticket`. Answer all eight questions in your own words, choose exactly one
decision and say why. The money-logic rule in `CONTRIBUTING.md` applies to Card 2.

**Done when** `pytest -q` passes with the existing tests untouched and your own in new `tests/test_*.py` files (at least six, for
the hook and the script; use the stand-in, never the real `claude`); only the toolkit files changed, in small commits that follow
`CONTRIBUTING.md`; no secrets; and `python -m ailab grade m09 --dir <this directory>` passes (run it from the `ailab` folder of
the course repository). Do not change `src/`: the hook has to be right about it, not the other way round.
