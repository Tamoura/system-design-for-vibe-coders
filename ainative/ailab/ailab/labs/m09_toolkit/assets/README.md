# lab-assets for lab m09 (toolkit)

* `bin/claude` is a STAND-IN for the `claude` command, not Claude Code. It calls no model and needs no key. It imitates the
  documented shape of print mode (`claude -p`, `--output-format json`, `--max-turns`, an exit code) so that your triage script
  can be run, and graded, offline and the same way every time. It ignores the prompt and classifies by a keyword table.
  Read its docstring for the markers (such as `[stub:error]`) that make it misbehave on purpose. Use it with
  `export PATH="$PWD/lab-assets/bin:$PATH"` (macOS, Linux or WSL), or run `python lab-assets/bin/claude -p ...`.
  The grader always uses the kit's own copy, not this one.
* `tickets/sample-tickets.json` holds invented support tickets (English and Arabic). Some carry stand-in markers.
* `hook-samples/` holds four documents shaped like the JSON that Claude Code writes to a PostToolUse hook. The paths are
  relative so that they work wherever you cloned the repository (real documents carry absolute paths), and `tool_response`
  is a placeholder: its real fields depend on the tool.
* `post_edit_skeleton.py` and `triage_skeleton.py` are starting points for parts 3 and 4.
* `automation-card-template.md` is the card for part 5.

Everything here is constructed for teaching. Nothing was recorded from a real model or a real customer.
