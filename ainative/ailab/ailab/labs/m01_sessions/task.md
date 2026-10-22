# ONB-101: read three agent sessions and name what went wrong

**From:** Hessa, Product Owner, Najm Remit (for Tariq's AI-native clinic)
**To:** Payments Platform, new joiners
**Priority:** Medium. The clinic is on Thursday.

Tariq collected three transcripts of coding-agent sessions on Remit. Before the clinic, read each one and
tell us what went wrong and where. They are **constructed for teaching, not recorded from a real model**,
but every file, function, command and test result in them is the one in this repository, so you can check
what you read against your own working copy.

## What I need (part 1, required, no agent needed)

1. Read `s1-daily-summary.md`, `s2-fee-tier.md` and `s3-partner-sdk.md` in `lab-assets/sessions/`, turn by
   turn. Check any claim you doubt against this repository.
2. Fill `diagnosis.json` (it is here, with empty fields). For each session give one finding for each
   failure you see, at most two, in the order they happen. A session can show more than one failure. A
   finding has four fields:
   - `failure_mode`: one of `hallucinated-api`, `stale-knowledge`, `misread-requirement`, `symptom-fix`,
     `sycophancy`, `context-rot`, `runaway-loop`, `test-gaming`, `injection`, `scope-creep`. The field guide
     in lesson 1.1 defines each.
   - `turn`: the number of the turn where it went wrong (`T08` is 8). That is the first turn you can point
     at and say "here it happens". For text the agent reads, it is the turn where the agent acts on the
     text. For a loop, any turn in the stretch where the agent clearly repeats itself. The grader allows one
     turn either side.
   - `prevention`: the cheapest way to have stopped it, as one category: `context` (give it the missing
     fact), `spec` (write down done, non-goals and constraints), `small-steps` (short loops, a cap on
     attempts), `verify` (a check it cannot edit or fake), `permissions` (deny rules, a hook, a sandbox, an
     approval you read), `fresh-start` (a new session, a compaction or a subagent), `review` (a second
     person reads it).
   - `evidence`: a short quotation (8 to 300 characters) copied word for word from the session.
3. Commit your answers.

## Part 2 (optional, needs an agent)

Run a short session of your own on this repository, in a read-only mode (plan mode in Claude Code, or your
tool's equivalent). Ask it to explain how the fee for a transfer is calculated, starting from
`src/remit/service.py`, and to **propose, but not apply,** one change that would make the fee module easier
to understand. Then fill in `session-notes.md` and `agent-log.md`. No agent? Skip this part: nothing in
part 1 depends on it.

## Done when

- `diagnosis.json` is valid and every finding is filled in.
- Nothing else changed except `diagnosis.json`, `session-notes.md` and `agent-log.md`. The sessions, the code
  and the tests are read-only, and your live session must not leave changes behind.
- Your work is committed, with a message that follows `CONTRIBUTING.md`.
- Grade it from the `ailab` folder of the course repository:
  `python -m ailab grade m01 --dir <this directory>`
