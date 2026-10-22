# REMIT-393: three pages the team is missing

**From:** Hessa, Product Owner, Najm Remit
**To:** Payments Platform
**Priority:** Medium. Internal audit asks to see these on Friday.

Three pieces of writing are overdue, and each must be *true*, not only tidy. Use an AI assistant if
you like; you are accountable for every sentence. This ticket is documentation only: do not change
code, tests or `lab-assets/`. A code comment that disagrees with what the code does goes under
"Known problems" at the end of the najmkit page; do not fix it here.

### 1. An ADR for a decision we already made

Write `docs/adr/0001-<short-title>.md` in Michael Nygard's format: a title, then **Status**,
**Context**, **Decision**, **Consequences**, in that order (start from `lab-assets/adr-template.md`).
Pick one decision the code embodies: fixed UTC+3 windows (`limits.py`), `Decimal` rounded half up
(`money.py`), a failed notification not undoing a transfer (`service.py`), amounts stored as text
(`store.py`), a 60-second quote (`fx.py`), or najmkit vendored in the repository.

Every claim about the code points at the code, with `path` or `module.name` in backticks, and
Consequences name a downside. Then ask a critic (an AI assistant, a colleague, you in a bad mood) to
attack the decision and make the best case for the strongest alternative. Add a final section
"Critic's objections": at least three, each with what you did (accepted, rejected, deferred).

### 2. The najmkit page, back from the dead

`docs/najmkit.md` was lost in the docs migration. Write it again from `src/najmkit/` (`ids`, `clock`,
`audit`): every public function and class, its signature, what it does, and a short example per
module that runs. Nothing outside the bank has seen najmkit, so no tool and no memory can tell you
what it does; the code can.

### 3. A postmortem for INC-2031

`lab-assets/incident.json` is the record of last Wednesday's incident (constructed for teaching).
Write `docs/postmortems/INC-2031.md` from it, starting from `lab-assets/postmortem-template.md`.

* The record is your only source. Use its times (UTC) and name the event id (E1, E2, ...) in every
  timeline row, and cover most of the record's events, not three highlights.
* Keep apart what we **know** (the record says it), what we **infer** (say what it rests on, how
  confident you are, what would confirm it) and what we **do not know** (leave it open).
* No invented numbers, times, causes or people. Blameless: what happened and what the system
  allowed, not who was at fault.
* At least three action items, each with an owner (a role or a team) and a way to see it is done.

`python lab-assets/claims_scan.py <file>` finds paths and names that point at nothing (add
`--record lab-assets/incident.json` for the postmortem). It cannot tell whether a sentence is true.

### Done when

Each document passes its checks, only `docs/` changed, and each document is its own commit with a
message that follows `CONTRIBUTING.md`. Grade it from the `ailab` folder of the course repository:
`python -m ailab grade m11 --dir <this directory>`
