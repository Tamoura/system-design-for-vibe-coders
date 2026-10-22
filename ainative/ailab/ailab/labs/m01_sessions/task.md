# ONB-101: read three agent sessions and name what went wrong

**From:** Hessa, Product Owner, Najm Remit (for Tariq's AI-native clinic)
**To:** Payments Platform, new joiners
**Priority:** Medium. The clinic is on Thursday.

Tariq collected three transcripts of coding-agent sessions on Remit. Read each one and tell us what went
wrong and where. They are **constructed for teaching, not recorded from a real model**. Apart from the
invented partner SDK in session 3, the files, functions and commands they use are the ones in this repository
and the tool outputs were captured on a scratch copy, so you can check what you read. The agents' own edits
are not in your copy.

### What I need (part 1, required, no agent needed)

1. Read `s1-daily-summary.md`, `s2-fee-tier.md` and `s3-partner-sdk.md` in `lab-assets/sessions/`, turn by turn.
2. Fill `diagnosis.json` (it is here, with empty fields). For each session give one finding for each failure
   you see, at most two, in the order they happen. A finding has four fields:
   - `failure_mode`: one of `hallucinated-api`, `stale-knowledge`, `misread-requirement`, `symptom-fix`,
     `sycophancy`, `context-rot`, `runaway-loop`, `test-gaming`, `injection`, `scope-creep` (the field guide
     in lesson 1.1 defines them).
   - `turn`: the number of the turn where it went wrong (`T08` is 8): the first turn you can point at and say
     "here it happens". For text the agent reads, that is the turn where the agent acts on it. For a loop,
     any turn in the stretch where it clearly repeats itself. One turn either side is accepted.
   - `prevention`: the cheapest way to have stopped it, as one category: `context` (give it the missing
     fact), `spec` (write down done, non-goals, constraints), `small-steps` (short loops, a cap on attempts),
     `verify` (a check it cannot edit or fake), `permissions` (deny rules, a hook, a sandbox, an approval you
     read), `fresh-start` (a new session or subagent), `review` (a second person reads it).
   - `evidence`: a short quotation (8 to 300 characters) copied word for word from the session.
3. Commit your answers.

### Part 2 (optional, needs an agent)

Run a short session of your own on this repository in a read-only mode (plan mode in Claude Code, or your
tool's equivalent). Ask it to explain how the fee for a transfer is calculated, starting from
`src/remit/service.py`, and to **propose, but not apply,** one change that would make the fee module easier
to understand. Then fill in `session-notes.md` and `agent-log.md`. No agent? Skip it; part 1 does not depend
on it.

### Done when

- `diagnosis.json` is valid and every finding is filled in.
- Nothing changed except `diagnosis.json`, `session-notes.md` and `agent-log.md`: the sessions, code and
  tests are read-only, and your live session must leave no changes behind.
- Your work is committed, with a message that follows `CONTRIBUTING.md`.
- Grade it from the `ailab` folder of the course repository: `python -m ailab grade m01 --dir <this directory>`
