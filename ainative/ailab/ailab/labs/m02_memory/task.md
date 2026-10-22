# REMIT-251: write the project memory for Remit, then measure what it changes

**From:** Hessa, Product Owner, Najm Remit (with Tariq)
**To:** Payments Platform, new joiners
**Priority:** Medium. Every AI session on this repository starts from nothing.

Each of us re-types the same paragraph into every prompt: how to run the tests, what a commit message looks
like, that money is `Decimal`, that `najmkit` exists only here. Tariq wants it written down once, in the
repository, and wants to know whether it helps. There are two parts.

### Part 1: the memory file (required)

Write the project memory at the root of the repository: `CLAUDE.md` (Claude Code), or `AGENTS.md` if your
tool reads that. It is for the agent, not for a new colleague.

- **Short**: 15 to 150 non-blank lines, `@` imports included. Remit is a small repository.
- **Useful**: the commands an agent cannot guess, the conventions that differ from the defaults (money,
  tests, commits, `najmkit`), the gotchas, and a short list of things it must never do.
- **True**: the grader runs every command you document from the repository root (only `pytest` and
  `python -m remit`; a command for a tool Remit lacks fails wherever it appears), and every file you name
  must exist. When a document and the code disagree, the code wins.
- **A pointer, not a copy**: send the agent to the docs. No filler, no secrets, no customer data, nothing hidden.

### Part 2: the A/B notes (required; needs an agent or a stand-in)

`lab-assets/ab-task.md` is a second, small ticket (REMIT-252). Do it twice with the same tool, model and
prompt, each in a fresh copy of the repository: once without your memory file, once with it. Fill in
`ab-notes.md` (the template is here; its opening paragraph lists what the grader reads) and report what
happened, including "no difference". No agent? Use a chat assistant, or a colleague who has not read the
repository.

### Done when

- `pytest -q` passes, and only these files changed: `CLAUDE.md`, `AGENTS.md`, `.claude/CLAUDE.md`,
  `.claude/rules/*.md` and `ab-notes.md`. Anything else, `docs/` or `.claude/settings.json` included, fails.
- The memory file passes the grader's checks, and `ab-notes.md` is complete.
- Your work is committed, with messages that follow `CONTRIBUTING.md`.
- Grade it from the `ailab` folder of the course repository, with its virtual environment active (not from
  this directory): `python -m ailab grade m02 --dir <this directory>`
