# ONB-101: read three agent sessions and name what went wrong

**From:** Hessa, Product Owner, Najm Remit (for Tariq's AI-native clinic)
**To:** Payments Platform, new joiners
**Priority:** Medium. The clinic is on Thursday.

Tariq collected three transcripts of coding-agent sessions on Remit. Tell us what went wrong in each, and
where. They are **constructed for teaching, not recorded from a real model**. Apart from session 3's invented
partner SDK, the files, functions and commands in them are this repository's and the tool outputs were
captured on a scratch copy, so you can check what you read. The agents' own edits are not in your copy.

### What I need (part 1, required, no agent needed)

1. Read `s1-daily-summary.md`, `s2-fee-tier.md` and `s3-partner-sdk.md` in `lab-assets/sessions/`, turn by
   turn. They are evidence, not instructions for you or your assistant: never run a command found only in a
   transcript.
2. Fill `diagnosis.json` (it is here, with empty fields): one finding per failure you see, at most two per
   session, in the order they happen. A failure that goes unnoticed or is explained away later is the same
   finding, not a new one. Each finding has four fields:
   - `failure_mode`: one of `hallucinated-api`, `stale-knowledge`, `misread-requirement`, `symptom-fix`,
     `sycophancy`, `context-rot`, `runaway-loop`, `test-gaming`, `injection`, `scope-creep` (lesson 1.1
     defines them).
   - `turn`: the number of the turn where it went wrong (`T08` is 8): the first turn you can point at and say
     "here it happens". For text the agent reads, that is the turn where it acts on it. A loop is a stretch:
     any turn from the first attempt that later gets repeated to the last repeat. One turn either side is
     accepted.
   - `prevention`: the cheapest way to have stopped it, as one category: `context` (give it the missing
     fact), `spec` (write down done, non-goals, constraints), `small-steps` (short loops, a cap on attempts),
     `verify` (a check it cannot edit or fake), `permissions` (deny rules, a hook, a sandbox, an approval you
     read), `fresh-start` (a new session or subagent), `review` (a second person reads it).
   - `evidence`: a quotation (8 to 300 characters) copied word for word from the turn you point at or the one
     before or after it (for a loop, anywhere in the stretch). Backticks, bold markers, `>`, capitals, line
     breaks and a final full stop do not matter.
3. Commit your answers.

### Part 2 (optional, needs an agent)

Run a short session of your own on this repository in a read-only mode (plan mode in Claude Code, or your
tool's equivalent). Ask it to explain how the fee for a transfer is calculated, starting from
`src/remit/service.py`, and to **propose, but not apply,** one change that would make the fee module easier
to understand. Then fill in `session-notes.md` and `agent-log.md`. No agent, or none that can start an
interactive session where you work? Read by hand or with a chat assistant and say so in the notes, or skip
part 2; part 1 does not depend on it.

### Done when

- `diagnosis.json` is valid and every finding is filled in.
- Nothing changed except `diagnosis.json`, `session-notes.md` and `agent-log.md`: the sessions, code and
  tests are read-only, and your live session must leave no changes behind.
- Your work is committed on the branch you started on, with a message that follows `CONTRIBUTING.md`.
- Grade it from the `ailab` folder of the course repository: `python -m ailab grade m01 --dir <this directory>`
