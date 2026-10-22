# REMIT-330: turn three vague tickets into specs an agent can build from

**From:** Hessa, Product Owner, Najm Remit (with Tariq)
**To:** Payments Platform, new joiners
**Priority:** Medium. Three tickets are waiting, and I keep getting "what did you mean?" messages.

I wrote three tickets in a hurry: `lab-assets/tickets/T1.md` to `T3.md`, with my notes from the planning meeting in `lab-assets/hessa-notes.md`. Nobody, human or agent, can build from them as they stand: each hides questions that money software must answer before anyone writes code. My notes were typed on a phone and can pull in different directions; where they do, choose, say why and name who confirms.

**Please do not build anything.** Write one spec per ticket, in `specs/T1.md`, `specs/T2.md` and `specs/T3.md`, on `specs/TEMPLATE.md`, and keep its ten sections. I need:

- **Behaviour**: at least three worked examples with exact amounts, times or dates (for example 500.00 QAR, 10,000 INR, 18:00, 6pm or 2026-03-02), edges included.
- **Acceptance criteria**: at least four, one per bullet, each a statement that a test could prove or refute, two or more with an exact amount, time or date. "Works properly" is not a criterion.
- **Decisions and open questions**: every question the ticket leaves open, answered as one complete sentence that names its subject. A question is not an answer. Read the code first; where a document and the code disagree, the code wins. If only a person can know (me, Finance, Ops), decide, call it an assumption and say who confirms it. For text customers read in Arabic, write the Arabic sentence or say who supplies it (an agent or a translator can draft it; a native reader approves it before release).
- **Plan**: four to ten numbered steps, each small enough for one commit and naming its file, test or command, with the failing test written and run before the code it covers (the two may share one green commit: `CONTRIBUTING.md` wants the tests passing at every commit). It runs `pytest` and says how to roll back. If the whole ticket needs more than ten steps, plan the first slice and name the later slices in one sentence; the grader checks each step, not the total.
- Constraints, non-goals and decisions are bullet lists (at least three constraints, two non-goals and three decisions). `CONTRIBUTING.md` applies, and money logic needs a second human reviewer: write "second human reviewer" and name who (Nada from quality engineering, or Tariq). No filler, no placeholders (replace every `TODO`), and only files that exist, unless you say beside the file that it is new. Each spec has its own numbers and decisions; a copy of one with the names changed fails.

### Done when

- The three specs are complete and committed, with messages that follow `CONTRIBUTING.md` (`type(scope): subject`; any lower-case scope works, for example `docs(specs): spec the Egypt fee offer`). Nothing else changed except `agent-log.md` (optional), and `pytest -q` passes.
- Grade it from the `ainative/ailab` folder of the course repository, not from this directory: `python -m ailab grade m03 --dir <this directory>`. Lines marked (advisory) print FAIL until satisfied but never block PASSED.

An agent may interview you or review a draft, but you answer for every sentence: the grader checks the shape of a spec and the facts it can check, not whether your decisions are good.
