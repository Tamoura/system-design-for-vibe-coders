# REMIT-258: harden how agents work in this repository

**From:** Noura, Application and AI Security (with Tariq, Engineering Lead)
**To:** Payments Platform, everyone who uses an AI coding tool
**Priority:** High. An agent has the same hands you have.

Last week Lujain's agent proposed `pip install` for a package nobody knew, and a vendor README we nearly pasted into a session
had instructions for the AI reading it. The repository should carry its own guard rails, reviewed like code. Everything is
local and fictional; no agent is needed, and if you use one, you stay accountable.

**Part 1 — Permission rules: `.claude/settings.json`**

A `permissions` object (`allow`, `ask`, `deny`) and a `hooks` object, in the syntax of the Claude Code permissions page.

- **Deny** reading a `.env` file, anything under `~/.ssh` and `~/.aws`, and the shell commands `git push` and `rm -rf`. A Bash
  rule matches the command's text: try yours on `git push origin main` and `rm -rf build`. Do not deny so much that everyday
  work (`git status`, `pytest`, reading source) stops.
- **Allow** only narrow commands you run all day: nothing that could delete, publish, download-and-run or read secrets, no
  interpreter or launcher (`python *`, `env *`, `find *`, `npx *`), no editing of `.claude/`.
- **Register the guard** from Part 2: a `PreToolUse` hook for `Bash` that runs `.claude/hooks/guard.py` from the project folder.
- Advisory: ask before `curl`, `wget` and edits to `money`, `fees`, `fx`, `limits`, `ledger` and `service`.

**Part 2 — A guard hook: `.claude/hooks/guard.py`**

Python. Claude Code runs it before every `Bash` call with one JSON document on standard input (`lab-assets/hook-samples/` has
six). **Block: exit with code 2 and write a sentence starting `Blocked:` to standard error** (the JSON `deny` form of the
hooks documentation, with its `hookEventName`, also counts). **Allow: exit 0.** Any other exit code is a non-blocking error: the
command runs, so never end that way.

Block a `Bash` command that would **run** one of these; text that merely mentions them is not a command, and pieces of words
are not words. A command can span lines: a newline separates commands like `;`, a `#` inside a word is not a comment, and a
heredoc body (`<<'EOF'` to `EOF`) is text.

1. **Delete a tree:** `rm` with `-r`, `-R` or `--recursive`, however the program or flags are spelled, after `;` `&&` `||`
   `|`, `env` or `timeout`, or inside `bash -c "..."`. `rm file.txt` is fine.
2. **Rewrite or publish history:** `git push` (also `git -C <dir> push`), `git reset --hard`, `git clean -f` (`-n` is fine).
3. **Run downloaded code:** `curl` or `wget` piped into `sh`, `bash`, `zsh` or an interpreter.
4. **Send data out:** `curl` with `-d`, `--data*`, `-F`, `--form*`, `-T`, `--upload-file`; `wget` with `--post-*`.
5. **Touch credentials:** naming a real `.env` file (`.env`, `.env.production`; not `.env.example`), a path inside `.ssh` or
   `.aws`, or a key such as `id_ed25519`; also `printenv`.
6. **Add a dependency:** `pip install`, `python -m pip install`, `uv add`, `poetry add`, `npm install` and the like.
7. **Change user:** anything under `sudo` or `doas`.

Everything else goes through (`curl` with no body, `pip list`), and so does every tool that is not `Bash`. **If the input is not
JSON, or a `Bash` call has no command, block it.** Cases this ticket does not describe are not graded: choose the safer reading
and say so in a comment. Advisory: also see through `find ... -delete`, `$(...)`, a Python one-liner calling `shutil.rmtree`,
and `xargs rm -rf`.

**Part 3 — A dependency check: `scripts/depcheck.py`**

`python scripts/depcheck.py [ROOT]` (default `.`) only reads files.

- **Known:** in `deps-allowlist.txt` or pinned in `requirements.lock` (both optional). Compare names after normalising:
  lower case, runs of `-` `_` `.` become one `-`. Allow-list: one package per line, `#` comments, `package: module1, module2`
  for import names. Lockfile: `name==version` lines, optionally followed by `--hash=...` lines.
- **Declared:** `[project] dependencies` and every group of `[project.optional-dependencies]` in `pyproject.toml`, and every
  `requirements*.txt` directly in ROOT. Lines may have extras, specifiers, a `;` marker, a comment or a trailing `\`; lines
  starting with `-` are options, not requirements.
- **Imported:** absolute imports anywhere in `*.py` under `src/` and `tests/`. The standard library, your own modules (directly
  in `src/` or `tests/`) and known packages are fine; files that do not parse are skipped.
- Print `FLAG <name>: <reason>` once per unknown package and **exit 1**; `name @ URL` is always flagged. Otherwise print
  `OK: ...` and **exit 0**.
- Create `deps-allowlist.txt` so the check passes here. `lab-assets/sample-project/` has problems to try it on.

**Part 4 — Notes: `injection-notes.md`**

Do this part yourself, not through an agent: reading the README is the attack. `lab-assets/vendor-readme/README.md` is
constructed: `csvtidy` is a made-up vendor library (a real package with a similar name may exist and is unrelated), the
instructions are not real and every address ends in `.invalid`. Read it as text, as a suspicious person would, and run
nothing from it. Then fill in `lab-assets/injection-notes-template.md`: every instruction aimed at an AI, what it would cost if
obeyed, and which of your rules would stop it (and which would not).

**Done when** `pytest -q` passes in under a minute with the existing tests untouched and your own in `tests/test_guard.py` and
`tests/test_depcheck.py`; no secrets (the `.env` here is fake and git-ignored, for trying your deny rule); everything is
committed, one commit per part with its tests and code, as `type(scope): subject` where the scope is any lower-case word for
the area (`security`, `hooks`, `deps`: CONTRIBUTING.md's list is examples); only `.claude/`, `scripts/`, new files under
`tests/`, `deps-allowlist.txt`, `requirements.lock`, `injection-notes.md`, `docs/`, top-level Markdown files, `.gitignore` and a
CI step in `.github/workflows/` changed; and `python -m ailab grade m08 --dir <this directory>` passes (run it from the
`ainative/ailab` folder of the course repository).
