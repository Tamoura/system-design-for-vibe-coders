# REMIT-231: three pages the team is missing

**From:** Hessa, Product Owner, Najm Remit
**To:** Payments Platform
**Priority:** Medium. Internal audit asks to see these on Friday.

Three pieces of writing are overdue, and each one has to be *true*, not only tidy. Use an AI
assistant if you like. You are accountable for every sentence, so check what it tells you against
the code and the record before it goes into the repository.

This ticket is documentation only. Do not change code or tests, and do not edit anything in
`lab-assets/`. If you find a comment in the code that disagrees with what the code does, do not fix
it here: list it under "Known problems" at the end of the najmkit page.

## 1. An ADR for a decision we already made

Write `docs/adr/0001-<short-title>.md` in Michael Nygard's format: a title, then **Status**,
**Context**, **Decision** and **Consequences**, in that order (start from `lab-assets/adr-template.md`).
Pick one decision the code already embodies:

* Qatar days and months are fixed UTC+3 windows, not a time-zone database (`limits.py`)
* Money is `Decimal`, rounded half up, and floats are refused (`money.py`)
* A failed notification does not undo a transfer (`service.py`)
* Amounts are stored as text in SQLite (`store.py`)
* A quote is valid for 60 seconds (`fx.py`)
* najmkit is vendored in the repository, not installed (`src/najmkit/`)

Every claim about the code points at the code, with `path` or `module.name` in backticks. Consequences
say what gets harder, not only what gets easier.

Then ask a critic (an AI assistant, a colleague, you in a bad mood) to attack the decision and to make
the best case for the strongest alternative. Add a final section called "Critic's objections" with at
least three objections. For each one, say what you did about it: accepted (and changed the ADR),
rejected (with the reason), or deferred.

## 2. The najmkit page, back from the dead

`docs/najmkit.md` was lost in the docs migration. Write it again from the code in `src/najmkit/`
(`ids`, `clock`, `audit`): every public function and class, its signature, what it does, and at least
one short example per module. The examples must run. Nothing outside the bank has ever seen najmkit,
so no tool and no memory can tell you what it does; the code can. Anything the page says has to be
true, and checkable by someone who has not read it.

## 3. A postmortem for INC-2031

`lab-assets/incident.json` is the record of last Wednesday's incident (constructed for teaching).
Write `docs/postmortems/INC-2031.md` from it, starting from `lab-assets/postmortem-template.md`.

* The record is your only source. Use its times (UTC) and name the event id (E1, E2, ...) in every
  timeline row.
* Keep three things apart: what we **know** (the record says it), what we **infer** (you reason beyond
  the record: say what it rests on, how confident you are and what would confirm it), and what we
  **do not know** (the record cannot answer it: leave it open).
* No invented numbers, times, causes or people. Blameless: describe what happened and what the system
  allowed, not who was at fault.

`python lab-assets/claims_scan.py <file>` finds paths and names that point at nothing (add
`--record lab-assets/incident.json` for the postmortem). It cannot tell you whether a sentence is true.

## Done when

1. The ADR is in `docs/adr/`, follows the format, points at real code and records the critic's objections.
2. `docs/najmkit.md` covers the whole public API, its examples run and nothing in it contradicts the code.
3. The postmortem has its sections, every timeline row matches the record, and nothing unknown is stated as fact.
4. Only files under `docs/` changed. Each document is its own commit, with a message that follows
   `CONTRIBUTING.md`. Everything is committed.

When you think you are done, grade it from the `ailab` folder of the course repository:
`python -m ailab grade m11 --dir <this directory>`
