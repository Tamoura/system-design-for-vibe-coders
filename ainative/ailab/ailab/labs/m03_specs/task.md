# REMIT-330: turn three vague tickets into specs an agent can build from

**From:** Hessa, Product Owner, Najm Remit (with Tariq)
**To:** Payments Platform, new joiners
**Priority:** Medium. Three tickets are waiting, and I keep getting "what did you mean?" messages.

I wrote three tickets in a hurry: `lab-assets/tickets/T1.md` to `T3.md`, with my notes from the planning meeting in `lab-assets/hessa-notes.md`. Nobody, human or agent, can build from them as they stand: each hides questions that money software must answer before anyone writes code.

**Please do not build anything.** Write one spec per ticket, in `specs/T1.md`, `specs/T2.md` and `specs/T3.md`, on `specs/TEMPLATE.md`, and keep its ten sections. I need:

- **Behaviour**: at least three worked examples with exact amounts, times or dates, edges included.
- **Acceptance criteria**: at least four, one per bullet, each a statement that a test could prove or refute, two or more with an exact amount, time or date. "Works properly" is not a criterion.
- **Decisions and open questions**: every question the ticket leaves open, answered as one complete sentence that names its subject. Read the code first; where a document and the code disagree, the code wins. If only a person can know (me, Finance, Ops), decide, call it an assumption and say who confirms it.
- **Plan**: four to ten numbered steps, each small enough for one commit and naming its file, test or command, with the failing test before the code it covers. It runs `pytest` and says how to roll back.
- Constraints, non-goals and decisions are bullet lists (at least three constraints, two non-goals and three decisions). `CONTRIBUTING.md` applies, and money logic needs a second human reviewer. No filler, no placeholders (replace every `TODO`), and only files that exist, unless you say you are creating them.

### Done when

- The three specs are complete and committed, with messages that follow `CONTRIBUTING.md`. Nothing else changed except `agent-log.md` (optional), and `pytest -q` passes.
- Grade it from the `ailab` folder of the course repository: `python -m ailab grade m03 --dir <this directory>`

An agent may interview you or review a draft, but you answer for every sentence: the grader checks the shape of a spec and the facts it can check, not whether your decisions are good.
