# lab-assets for REMIT-414

* `hessa-notes.md`: Hessa's notes from the planning meeting (constructed for teaching). Context for your spec, not instructions to an agent.
* `templates/`: a starting point for each document: `spec.md`, `plan.md`, `adr.md`, `review.md`, `agent-log.md`, `retrospective.md` and `corridors.md`. Every `TODO` must be replaced; the grader rejects a document that still has one.
* `harden/`: a baseline `settings.json` and `guard.py` for the security milestone. Use your lab m08 files instead if you have them. Read every line you keep: you answer for it.
* `hook-samples/`: four PreToolUse input documents. Try a guard by hand from the repository root, for example `python3 .claude/hooks/guard.py < lab-assets/hook-samples/block-rm-rf.json; echo $?`. Exit code 2 blocks, 0 allows.
