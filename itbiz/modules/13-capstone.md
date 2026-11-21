# Module 13 — Capstone and practice

*Najm Bank's Technology division has now produced more than forty artefacts: value-stream maps, a product canvas, a team map, catalogue entries, a portfolio one-pager, a funding memo, an intake form, a traceability convention, a pipeline service card, a release policy, a change model, recipes, SLO sheets, an information model, a cost model, a supplier register, a control matrix, a toolchain map, an AI use register, a framework register, an evidence review and a roadmap. Each was useful alone. Together they are only useful if they agree with each other and with how the division actually works. This module puts them together. In lesson 13.1 Huda assembles the division's IT operating blueprint, tests it for coherence by walking real work through it, and presents it to the board with the decisions it needs; you do the same for your own organisation. Lesson 13.2 is a practice exam of forty scenario questions across the whole course, so you can find the lessons worth rereading.*

> **Steps:** Plan, Fund, Build, Release, Serve, Run, Govern, Improve — join the pieces into one operating blueprint that a board can decide on, an auditor can follow and a team can work by, then check what you have learned.

---

# 13.1 — Capstone: Najm Bank's IT operating blueprint
*Level: 🔴 Advanced* · *Prerequisites: 12.2, 12.3* · *Step: Plan, Fund, Build, Release, Serve, Run, Govern, Improve*

**After this you can** assemble your organisation's IT operating blueprint from the artefacts of this course, with a one-page spine that names, for each of the eight steps, the decision, the decider, the record and its home, and the measure; run five coherence tests on it, including a walk-through of one real change and one real incident; and present a one-page board summary that asks for named decisions. *Study time: reading about 20 min, hands-on about 4 h (estimate).*

## ⚡ In 60 seconds
- An **IT operating blueprint** describes how your IT organisation works: who decides what, with which record, how it is measured, funded and governed. You assemble it from this course's artefacts, not from scratch.
- Its centre is the **spine**: one page, one row per step (Plan, Fund, Build, Release, Serve, Run, Govern, Improve), naming the decision, decider, record and home, measure and artefact.
- Test it before anyone relies on it: **one name**, **one identifier**, **closed loop**, **no contradictions**, and a **walk-through** of one real change and one real incident.
- The rule that matters most: **if two pages of the blueprint disagree, the organisation already does.**
- Decision cue: the blueprint is ready for the board when it asks for named, dated decisions, not applause.
- Biggest trap: a thick "target operating model" that describes a future nobody works in and nobody opens again.

## 🧭 Why it matters
Najm Bank and everyone in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

Six months into the roadmap of lesson 12.3, wave 1 had worked for Cards & Payments: change lead time was about 4 days and 9 of 10 sampled changes could be traced. Then the chair of the audit committee asked Omar, Chief Information Officer: "If I join a Cards team tomorrow, or the supervisor asks, what do I read to learn how your division now works?"

Omar's honest answer was "about forty documents in a shared folder", several of which disagreed. The access register said card-dispute roles were reviewed quarterly; Nour's draft control matrix for the card-dispute system said half-yearly. The cost model used the product identifier `CARDS-PAY`; the platform usage report still said "Cards". Wave 2 would copy every misfit to three more value streams.

Omar asked Huda, Head of Enterprise Architecture, to assemble the blueprint: short enough for a new manager to read in an afternoon, exact enough for an auditor to follow, honest about what was still only on paper.

## 📐 How it works

### 🟢 The essentials

**What it is, and is not.** The blueprint is the operating model written down: decisions, deciders, records, measures, money and controls, linked. It is not an org chart, a process manual or a copy of any framework's structure (lesson 12.1: borrow the question, keep your own map).

**Three layers**, so each reader finds their level fast:

| Layer | Length | Reader | What it holds |
|---|---|---|---|
| **Board summary** | One page | Board, audit committee | The five questions of lesson 0.1 with evidence, top three constraints, decisions requested |
| **Spine** | One page | Managers, auditors, new joiners | One row per step |
| **Artefact pages** | One page each | Teams who work by them | Current artefacts from Modules 1–12, with owner and status |

Detail beyond a page stays in the team's tools, linked.

**The spine.** One row per step. Najm Bank's, in short:

| Step | Main decision | Decider | Record and home | Measure | Artefacts (lesson) |
|---|---|---|---|---|---|
| **Plan** | Themes, and what we will not do | CIO with business heads | Portfolio, portfolio tool | Change money by theme | 3.1, 4.1 |
| **Fund** | What each product gets; review date | Investment committee; product manager within guardrails | Investment record with product identifier | Funding wait | 3.2, 10.1 |
| **Build** | What enters the product; evidence required | Product team within policy and gates | Backlog item; pipeline run record | Change lead time | 4.2, 5.1, 5.2, 5.3 |
| **Release** | Route of a change; when users get it | Team deploys; product manager releases; change authority for high risk | Change and release records, written by the pipeline | Change fail rate by route | 6.1, 6.2, 6.3 |
| **Serve** | What we offer, to whom, at what level and cost | Product and service owners | Catalogue entry; access register | Request elapsed time | 2.3, 7.1, 7.2, 7.3 |
| **Run** | What pages; how severe; what we fix for good | Incident commander; problem owner | Incident, problem and SLO records | SLO attainment; repeat incidents | 8.1, 8.2, 8.3 |
| **Govern** | Which risks, controls, suppliers and records we rely on | Control owners; second line (the risk function overseeing IT, lesson 10.3) challenges | Control matrix; supplier register | Key controls operating; trace-test result | 9.1, 10.2, 10.3, 11.1, 11.3 |
| **Improve** | What changes next in the model, and what stops | Sponsor at the transformation board | Evidence review; decision log | Outcome baseline over time | 12.1, 12.2, 12.3 |

Your spine will differ. The rule behind each cell must not: **one decision, one named decider, one home for the record, one measure someone reads.**

**Five labels on every artefact page:** owner, version and date, source, records read or written, and **status**: defined, practised in one value stream, or practised widely (the same distinction as lesson 12.2's 0–3 scale). A page marked "defined" promises nothing yet.

### 🟡 Going deeper

**Five coherence tests.** Find the gaps on paper before people find them at 2 a.m.

| Test | Question | Typical finding |
|---|---|---|
| **One name** | Does every product, service, record, tool and control have exactly one accountable person? | A tool owner but no record owner (lesson 11.1) |
| **One identifier** | Does each product carry the same identifier on every page? | "Cards" on one page, `CARDS-PAY` on another |
| **Closed loop** | Do Serve and Run data reach Plan and Fund on a schedule? | Problem actions needing money with no route to the portfolio review |
| **No contradictions** | Do targets, frequencies, thresholds and terms agree across pages? | Access review quarterly on one page, half-yearly on another |
| **Walk-through** | Can one real change and one real incident pass through, page by page, without improvising? | A kind of work with no route |

The walk-through matters most and is skipped most. It is lesson 9.3's trace test applied to the operating model: does the description match what people did? Walk it with the doers, not the authors.

**Where contradictions come from.** Usually real disagreements each team settled alone, not typing errors: risk wrote the frequency it needs, the product team the one it can manage. The blueprint does not choose for them. It names who decides and keeps the value on **one home page** that other pages point to: lesson 11.1's "one record, one home", applied to the blueprint itself.

**What stays the same.** Add a page of fixed points: risk appetite, security policy, central major-incident command, obligations. It steadies people who fear everything is moving.

**Decision records and upkeep.** Record each trade-off (showback rather than chargeback, which work stays central) as a one-page decision record, like the architecture decision records of lesson 4.3. Give the blueprint one owner, a version and a change log; owners update their page when they change their practice; rerun the walk-through quarterly.

### 🔴 Expert view

**The board summary asks for decisions.** Answer lesson 0.1's five questions (customers, consumption, cost, flow, decisions and records) with one line of evidence each, marked measured, sampled or estimated. Then list decisions requested, each with an owner and a date. Without them it is a status report (lesson 3.3). Show a gap yourself rather than let the board find it.

**The blueprint is what AI will amplify.** DORA's announcement of its 2025 report says "AI doesn't fix a team; it amplifies what's already there" and reports "a direct correlation between a high quality internal platform and an organization's ability to unlock the value of AI". Show where AI is used (lesson 11.3) and which foundations it depends on.

**Scale only what has worked.** Wave 2 should copy the blueprint that worked in wave 1, gaps marked, not an improved version nobody has tried. DORA's announcement of its 2024 report says that instability in priorities "can significantly hinder progress". By analogy (our inference, not DORA's finding), a blueprint rewritten monthly unsettles the teams working by it. Batch revisions into wave reviews, except error fixes.

For the same work from the team's side, see [*Cloud & DevOps: Zero to Hero*, lesson 7.1 — Capstone: take a new Najm service from empty repo to production with an SLO](../cloud/index.html#/7.1).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Blueprint index** | Every artefact page with its five labels | First, to see what you have and what is missing |
| **Spine** | One row per step: decision, decider, record and home, measure, artefact | Next; most people read only this page |
| **Coherence test sheet** | The five tests, with findings, owners and dates | Before anyone outside the authors relies on it |
| **Walk-through log** | One real change and one real incident, with every point of improvisation | Before first use, then quarterly |
| **Operating-model decision record** | Context, decision, consequences, status | When a choice will be questioned later |
| **Board summary** | Five questions with evidence, constraints, dated decisions requested | For the board or audit committee |

Any document tool or wiki works; these are templates, not products.

## 🏛️ In practice at Najm Bank
Illustrative and fictional. Huda's first draft was 140 pages, every artefact pasted in full. Omar read four. She cut it to a board summary, the spine and 34 one-page artefact pages: 12 "practised widely", 15 "practised in one value stream" and 7 "defined" (illustrative). Sami, Platform Engineering Lead, wanted his pipeline card marked "practised widely" because 22 teams used the pipeline; only Cards produced the full run record, so it stayed at one value stream.

**Coherence findings** (three of nine):

| Test | Finding | Resolution |
|---|---|---|
| One identifier | Usage report and two catalogue entries said "Cards" | Product identifier mandatory in the tagging template (Sami) |
| No contradictions | Access review quarterly in the register (7.2), half-yearly in Nour's draft control matrix for the card-dispute system | Nour confirmed with the second line that quarterly is required; the register holds the value, the matrix points to it |
| No contradictions | "Change fail rate" on one page, "change failure rate" on another | One term, "change fail rate" (DORA's current name), with one definition in the term map of lesson 12.1 (Huda); the 6.2 measures and the 12.3 wave sheet use it |

**The walk-through.** Yousef, Head of IT Operations, picked awkward examples: a month-end slowdown linked to problem record PRB-0142, and an update pushed by the card-processing supplier. The incident passed cleanly. The supplier change did not: it arrived by contract notice, not the front door (4.1) or the pipeline, so the change model (6.2) had no route. Huda added "supplier-originated change" to the change model, owned by Lina, Vendor and Sourcing Manager, on the high-risk route by default.

**The board summary** asked for four decisions: confirm wave 2's scope and dates; fund two more products on the Cards guardrails; keep chargeback out of scope this year; and make the five-incident trace test a standing audit sample. The board agreed three and deferred funding one quarter, asking Tariq, IT Finance Business Partner, for two quarters of Cards cost trend.

## 🛠️ Exercises
**🟢 Write your spine.** For your organisation (or Najm Bank), write one row per step: decision, decider, record and home, measure, artefact. Mark gaps "unknown".
*Done when:* all eight rows exist; each decider is a named role, not a committee with no named chair; each record names one home; each unknown has a person to ask.

<details><summary>Model answer and self-check</summary>

**Model answer.** First spines are usually strong on Release and Run, where change and incident records exist, and weak on Fund and Improve. Example Improve row: "decision: next change to the model; decider: unknown, no sponsor named; record: unknown; measure: none".

**Self-check.**
- One decider per row, not "IT" or "the business"?
- One home per record, where it is created?
- Is each measure read for a decision (lesson 1.3)?

</details>

**🟡 Assemble and test.** Build the index (at least ten artefacts with five labels each), then run the one-name, one-identifier, closed-loop and no-contradiction tests.
*Done when:* the index is complete; each test's method is noted; at least three findings have an owner and date; each contradiction names its home page.

<details><summary>Model answer and self-check</summary>

**Model answer.** An example from another organisation, not Najm. Twelve pages: four practised widely, six in one value stream, two defined. Findings: (1) cost reports use project codes that end with projects; the finance partner adds product identifiers by quarter-end (lesson 9.1). (2) Problem actions needing money have no route to the portfolio; the portfolio office adds a "needs funding" flag, read by the evidence pack, before the next review (lessons 3.3, 8.2). (3) The SLO sheet for online payments says 99.5% of payments succeed over 28 days; the quality requirements say 99.9% monthly availability. They use different indicators and windows, so the business owner of the product decides by month-end on one definition and one number, as Najm's head of retail banking did in lesson 8.3; the SLO sheet becomes home (lessons 4.3, 8.3).

**Self-check.**
- Is each status based on evidence you have seen?
- Does each contradiction name a decider and one home instead of copying the value?
- Did the closed-loop test follow real data, not a diagram?

</details>

**🔴 Walk it through and take it to the board.** Walk one recent, awkward real change and one real incident through the blueprint with the people who handled them, logging every improvisation. Then write the board summary with decisions requested.
*Done when:* both walks are logged with fix owners; at least one fix changed a page (new version); every board claim has a customer, number and record, marked measured, sampled or estimated; three to five decisions have owners and dates.

<details><summary>Model answer and self-check</summary>

**Model answer.** An emergency database fix during a Sev 2: the emergency route worked, but the fix was typed on the server, with no backlog key; the nightly drift check (lesson 6.3) flagged it and nobody followed up. Fix: the emergency route opens a backlog item, owned by the on-duty engineer (change model v1.3, a new version). Board summary: Cards lead time about 9 to 4 days (measured), other streams not yet measured (stated); decisions: wave 2 scope by month 7 (CIO), product funding for two products (investment committee), trace test as a standing audit sample (audit committee chair).

**Self-check.**
- Did the doers walk it, not the authors?
- Is each board number's status marked?
- Can the board actually decide each item by its date?

</details>

## ⚠️ Mistakes and traps
- **The 140-page blueprint.** Nobody works by what nobody reads. Use three short layers.
- **Describing the future as today.** "Defined" is a plan, not a practice; label status from evidence.
- **Settling contradictions by editing text.** Name who decides, keep the value in one home, point to it.
- **Skipping the walk-through.** Coherent on paper is not coherent in practice.
- **Freezing it, or rewriting it monthly.** Update pages with practice; batch revisions into wave reviews.

## 🧾 Recap
- The **blueprint** has three layers: board summary, spine, artefact pages.
- The **spine** names, per step, decision, decider, record and home, measure and artefact.
- Run **five coherence tests**, above all the walk-through of real work.
- **If two pages of the blueprint disagree, the organisation already does**; keep each value in one home.
- The **board summary** asks for named, dated decisions.

## ✍️ Check yourself
**1. Huda's first blueprint pasted every artefact in full: 140 pages. Omar read four. What should she change first?**

- A. Add a glossary and a colour-coded index, so that readers find their pages faster.
- B. Ask each artefact owner to cut their own page by half, keeping the structure.
- C. Build a one-page summary and spine, keep one page per artefact, link to detail.
- D. Send it as it is, since an audit committee prefers a complete document.

<details><summary>Answer</summary>

**C.** Three layers let each reader find their level. A and B make a long document easier to search or shorter, but still nobody's starting point; D confuses completeness with use. See "Three layers".

</details>

**2. The access register says card-dispute roles are reviewed quarterly; a draft control matrix says half-yearly. What does the lesson recommend?**

- A. Have the right person decide, keep the value on one home page, and point to it.
- B. Use the stricter frequency on both pages, since reviewing more often is safe.
- C. Leave both as they are, because each team wrote what suits its own work.
- D. Remove the frequency from both and let each reviewer choose it at the time.

<details><summary>Answer</summary>

**A.** A contradiction is a real disagreement: name who decides, record the value once, refer to it. B skips the decision and copies the value into two places that will drift; C keeps the dispute; D removes the control. See "Where contradictions come from".

</details>

**3. Before go-live of a new blueprint, Lina's team receives a supplier's certificate-rotation notice that matches no route in the change model. Which test would have shown this gap first?**

- A. The one-identifier test, because the notice does not carry the product's code.
- B. The one-name test, because no owner is listed for the supplier's certificates.
- C. The closed-loop test, because supplier data never reaches the portfolio review.
- D. A walk-through of a real supplier change, with the people who actually handled it.

<details><summary>Answer</summary>

**D.** Only walking real work through the pages shows whether a kind of work has a route. The other three tests compare pages with each other, so a kind of work that no page mentions passes them all. See "Five coherence tests".

</details>

**4. Sami wants his pipeline card marked "practised widely" because 22 teams use the pipeline; only Cards produces the full run record. Which status fits?**

- A. Practised widely, because adoption by 22 teams is itself strong evidence.
- B. Practised in one value stream, until other teams produce the full record.
- C. Defined, because only internal audit can confirm that a page is practised.
- D. None, because status labels belong on the board summary, not on pages.

<details><summary>Answer</summary>

**B.** Status comes from evidence of the practice, not tool adoption (lesson 12.2: score what you can show). A confuses use of the tool with the practice; C sets a bar the lesson does not; D is wrong, since every page carries a status. See "Five labels on every artefact page".

</details>

**5. Tariq's draft board summary on IT cost ends: "The committee is asked to note progress." What should change?**

- A. Attach every artefact finished this year, so the committee can see the work done.
- B. Replace the ending with one maturity score, averaged and tracked each quarter.
- C. Ask the committee to endorse the blueprint as a whole, rather than note progress.
- D. End with decisions requested, each with a named owner and a date to decide by.

<details><summary>Answer</summary>

**D.** A board summary exists to get decisions; "note progress" makes it a status report. A reports activity, B hides trade-offs in one number (lessons 1.3, 12.2), and C still asks for approval of everything rather than a decision on anything. See "The board summary asks for decisions".

</details>

## 📚 References
- Harvey, N. and DeBellis, D., "Announcing the 2025 DORA Report: State of AI-Assisted Software Development", Google Cloud blog, 23 September 2025 (opened 2026-11-20; source of the "amplifies" quote and the internal platform finding): https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report
- Harvey, N. and DeBellis, D., "Highlights from the 10th DORA report" (announcing the 2024 DORA report), Google Cloud blog, 22 October 2024 (opened 2026-11-20; source of the quote on instability in priorities): https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 7.1 — Capstone: take a new Najm service from empty repo to production with an SLO](../cloud/index.html#/7.1)
- Library course: [*AI Product Management: Zero to Hero*, lesson 10.1 — Capstone: take Najm Assist from idea to scale](../aipm/index.html#/10.1)
- Library course: [*Secure AI & Application Security: Zero to Hero*, lesson 12.1 — Capstone: secure Najm Assist from threat model to incident drill](../secai/index.html#/12.1)

---

# 13.2 — Practice exam: 40 scenario questions
*Level: 🔴 Advanced* · *Prerequisites: 13.1* · *Step: Plan, Fund, Build, Release, Serve, Run, Govern, Improve*

**After this you can** answer forty scenario questions across all fourteen modules in about an hour, mark them, and list the lessons your wrong answers send you back to. *Study time: reading about 30 min, hands-on about 105 min (estimate).*

## ⚡ In 60 seconds
- After this lesson you can answer forty scenario questions spread across the whole course, and use your wrong answers to choose the lessons to reread.
- It is practice on this course only. It is not preparation for any certification or framework exam, and a score here proves nothing to an employer or an auditor.
- Set it up like this: cover the answers, give yourself about an hour, answer all forty before you open any explanation, then mark them.
- Read every explanation, including for questions you got right: the wrong options are common real mistakes.
- Questions follow the course: 1 to 3 on Module 0, then three for each of Modules 1 to 12 (4 to 39), and 40 on the capstone. Each explanation names the lesson to reread.
- Najm Bank, its people and its figures are fictional and illustrative. Questions on finance, law, audit and regulation test the concept and the question to ask the right function, never a rule for your organisation.

## ✍️ Practice exam
**1. A board member asks whether IT is good value. Tariq replies: "IT is about 8% of bank costs." By the course rule, what is missing from his answer?**

- A. A comparison with other banks' IT spending, so the board can see where Najm sits
- B. A customer, a decision the number serves, and the record the number comes from
- C. A five-year trend, so the board can see whether the 8% figure is rising or falling
- D. A split by department, so each head of IT can explain their own share of the total

<details><summary>Answer</summary>

**B.** Every claim about IT needs a customer, a number and a record; a total answers no decision. A and C add context to the same unanchored number, and D splits it by org chart rather than by what customers consume. (Lesson 0.1.)

</details>

**2. Huda maps the eight steps onto departments ("Build is development, Run is operations") and calls the map finished. What is the main objection?**

- A. The map should use the terms of a recognised framework so that auditors can follow it
- B. The steps need more detail, so each department should add its own sub-steps first
- C. Departments should be merged until each one of the eight steps has a single team
- D. The steps are a loop, so trace real changes and show data from Run reaching Plan

<details><summary>Answer</summary>

**D.** The steps are a loop, not a sequence of departments, and value often leaks at hand-offs; tracing real work shows the real cycle. A adopts someone else's map, B adds detail to the wrong picture, and C reorganises before understanding the flow. (Lesson 0.2.)

</details>

**3. Tariq wants to quote the course's Najm Bank cost shares as benchmarks in a paper for the finance committee. What should he do?**

- A. Use them, but round each figure to the nearest five per cent so that they look less exact
- B. Leave them out, as they are illustrative, and take his questions to the finance controller
- C. Use them as benchmarks, since they come from a course built on general management practice
- D. Use them only if an AI assistant confirms they are in line with typical figures for banks

<details><summary>Answer</summary>

**B.** Najm Bank numbers are illustrative, not benchmarks, and the course is not professional advice; accounting questions go to the right function. A and C still present invented figures as evidence, and D treats an AI answer as a source. (Lesson 0.3.)

</details>

**4. Cards App 2.0 closes on time and on budget, and Omar announces it as a success. What would the course ask before agreeing?**

- A. Whether the supplier invoices were all paid before the project's closing date
- B. Whether the team's velocity rose during the final three sprints of the project
- C. What customers now do differently, measured against a baseline and a date
- D. Whether the project board signed the closure report with every box ticked

<details><summary>Answer</summary>

**C.** Closing on time and budget is an output; success is an outcome (a change in what people do) and then value. A, B and D all measure the project's activity or paperwork, not its effect. (Lesson 1.1.)

</details>

**5. The cards value-stream map shows a 30-day wait for the quarterly funding decision, while build is the busiest step at 8 days of work. Where should the team act first?**

- A. On the funding wait, because the rule is to shorten the longest wait first
- B. On the build step, because it has the most process time of any single step
- C. On the test step, because shared environments are always the bottleneck
- D. On every step at once, so that the whole stream improves at the same pace

<details><summary>Answer</summary>

**A.** Shorten the longest wait, not the busiest step: waiting usually dominates lead time. B is the tempting trap of optimising the busy step; C assumes a cause the data did not show; D spreads effort and hides which change worked. (Lesson 1.2.)

</details>

**6. Omar wants a single target for every product team: double deployment frequency this year. What is the main problem with it?**

- A. It should target change lead time instead, the better single measure of speed
- B. Teams should be ranked against each other instead, to create competition
- C. Targets should be set only by the platform team, who own the pipelines
- D. It measures speed alone; pair it with stability, and never as a target

<details><summary>Answer</summary>

**D.** Measure speed and stability together, never one without the other; DORA's guide is reported to warn against using its measures as targets or league tables. A swaps one speed target for another, B is the league-table trap, and C changes who sets the target, not the problem. (Lesson 1.3.)

</details>

**7. After a workshop, someone proposes renaming the inventory of about 420 applications "the product list". What does the course recommend instead?**

- A. Test each candidate: recognised by users, measurable, ownable, with one owner's name
- B. Keep all 420 names, but assign each one a product manager from the business side
- C. Group the applications by technology platform and call each platform a product
- D. Wait until the CMDB has been fully cleaned before deciding what the products are

<details><summary>Answer</summary>

**A.** Products are not applications; a boundary must be recognised by users, measurable, ownable, releasable and costable, with exactly one accountable name. B makes 420 products and a crowd of owners, C groups by technology, and D waits for a clean-up that never finishes. (Lesson 2.1.)

</details>

**8. A typical change to the cards app needs four teams to agree before it can ship. What does this most likely tell Huda?**

- A. The teams need a weekly coordination meeting with minutes and an action log
- B. The change process needs another approval step to manage the risk of hand-offs
- C. The team boundaries or the interfaces between teams are drawn in the wrong place
- D. The product needs a larger single team that absorbs all four of the other teams

<details><summary>Answer</summary>

**C.** If a typical change needs more than two teams to agree, the boundaries or interfaces are wrong; structure shows up in what gets built. A and B add coordination to a design problem, and D is a guess that may create a team too large to work as one. (Lesson 2.2.)

</details>

**9. A catalogue entry has no named owner and no requests in the last six months. What should happen to it?**

- A. Keep it, since removing entries confuses users who might need it one day
- B. Move it to a hidden section of the portal where only IT staff can see it
- C. Leave it until the annual catalogue review, when all entries are checked
- D. Fix it with an owner and a real promise, or retire it and tell its users

<details><summary>Answer</summary>

**D.** An entry with no owner, no requests in six months or a broken promise should be fixed or retired, and retired as carefully as it was added. A and C keep a dead promise, and B hides it without deciding anything. (Lesson 2.3.)

</details>

**10. Next year's IT budget is being built by adding up each business line's requests; the strategy slide will be written afterwards. What is the course's main objection?**

- A. Your real strategy is what you fund, so set themes and the mix before the requests
- B. Business lines should submit fewer requests, so the total stays within last year's
- C. The strategy slide should come first only because the board expects it on top
- D. Requests should be ranked by the seniority of the sponsor who submitted them

<details><summary>Answer</summary>

**A.** If money and teams point elsewhere, the strategy is a wish; translate strategy into three to five outcome themes and decide the mix by category and horizon before ranking. B caps spending without choosing, C is about presentation, and D ranks by rank. (Lesson 3.1.)

</details>

**11. Three items compete for one team. Fraud rule: cost of delay 20 a week, 2 weeks of work. Statement redesign: 30 a week, 6 weeks. Limit alert: 12 a week, 1 week (illustrative units). Which goes first by CD3?**

- A. The statement redesign, because it has the highest cost of delay of the three
- B. The fraud rule, because it sits in the middle on both cost of delay and duration
- C. The limit alert, because 12 divided by 1 week gives the highest CD3 of the three
- D. The fraud rule and the limit alert together, since both are under three weeks

<details><summary>Answer</summary>

**C.** CD3 is cost of delay divided by duration: limit alert 12, fraud rule 10, statement redesign 5. A ignores duration, which is the trap; B and D are not the CD3 order. (Lesson 3.2.)

</details>

**12. At the portfolio review, a sponsor says: "We have spent too much on loan origination to stop now." How should the board treat that argument?**

- A. As decisive, because stopping now would waste everything that has been spent so far
- B. As a reason to double the budget, so that the project finishes sooner than planned
- C. As sunk cost: spent money is gone, so ask only whether the next spend is worth it
- D. As a matter for the sponsor alone, since the board should not overrule sponsors

<details><summary>Answer</summary>

**C.** The only question is whether the next spend is worth it; a stop rule written at funding counters sunk cost and escalation of commitment. A and B are escalation of commitment, and D gives up governance. (Lesson 3.3.)

</details>

**13. A new regulatory report must be changed by a fixed date set by the supervisor. Which triage path does it take at the front door?**

- A. Catalogue request, because the reporting team already knows how to change reports
- B. Portfolio decision, because every regulatory item must be approved by the board
- C. Product backlog, ranked by CD3 against the product's other features in the queue
- D. Obligation: it must be done, and only how and when it is delivered remain open

<details><summary>Answer</summary>

**D.** An obligation must be done; only the how and when are open, and it is scheduled to its date. A treats new work as a known request, B sends it for a decision that is not open, and C ranks it as if it could lose. (Lesson 4.1.)

</details>

**14. Nobody can trace five random requirements to their tests and release in ten minutes. What change does the lesson recommend?**

- A. Link at the moment of work: keys on items and commits, checked by the pipeline
- B. Hire an analyst to build a traceability matrix before each audit takes place
- C. Write a fuller requirements document up front, so every item has a source
- D. Ask teams to add links to last quarter's work before the next audit sample

<details><summary>Answer</summary>

**A.** A link recorded during the work costs seconds; one rebuilt for an audit costs weeks. B and D rebuild links after the fact, and C produces a document traceable only to itself. (Lesson 4.2.)

</details>

**15. The cards app's requirements say "the app must be fast". What makes this a useful quality requirement?**

- A. Adding "very" and asking the architecture board to approve the wording before build
- B. Moving it to the non-functional section, where architects review it at the end
- C. A testable scenario with a number, like 95% of payments confirmed within 2 seconds
- D. Leaving it to the supplier, who knows best what speed their platform can achieve

<details><summary>Answer</summary>

**C.** A quality requirement is useful only when measurable and testable, written as a scenario with a number and a check. A and B change wording or place, not testability, and D gives away a decision the product owns. (Lesson 4.3.)

</details>

**16. A broken build agent stops a product team for a whole day and nobody is paged. What does this say about the pipeline?**

- A. That teams should keep their own build scripts on laptops as a backup route
- B. That the platform team should force every remaining team onto the pipeline
- C. That the build agents should be replaced with a different vendor's product
- D. It is not yet managed: it needs an owner, customers, service levels and funding

<details><summary>Answer</summary>

**D.** A pipeline nobody owns is a pipeline everybody works around; run it as a product with an owner, service levels and stable funding. A is the workaround the rule warns about; B pushes adoption, which lesson 5.1 warns is the wrong thing to measure a platform by; and C changes the tool, not the management. (Lesson 5.1.)

</details>

**17. Reem's team set a 90% test coverage target. Coverage reached 91% in a month; escaped defects did not change. What should she measure instead?**

- A. Escaped defects, with a regular mutation-testing sample to show tests check something
- B. Coverage at 95%, since the 90% target was clearly set too low to make a difference
- C. The number of tests written per sprint, reported to the board as a quality measure
- D. Nothing new; the coverage target is met, so the quality gate is working as designed

<details><summary>Answer</summary>

**A.** Evidence must be meaningful: coverage rose because new tests checked nothing. Outcome measures (escaped defects) and a mutation sample test whether tests work. B and C raise activity targets, and D trusts a green gate that checks little. (Lesson 5.2.)

</details>

**18. Reem's team blocked every library below a fixed score; developers then copied a small library's code into the app. What does the lesson's fix look like?**

- A. Lower the fixed score threshold, so that the small library can pass the check
- B. Ban copying code into the app, and discipline anyone found doing it in future
- C. Remove the component policy entirely, because it slows teams without benefit
- D. Make a low score trigger a conditional review by a named owner, not a block

<details><summary>Answer</summary>

**D.** If it runs in your product, it is in your inventory with a named owner; a blanket block pushed code out of sight, while a conditional review keeps it visible. A moves the line without fixing the incentive, B punishes the symptom, and C removes the control. (Lesson 5.3.)

</details>

**19. Marketing has fixed a launch date, so the team plans to deploy the new instalment feature that same morning. What does the release lesson recommend?**

- A. Move the launch date to suit the next monthly release window for the cards app
- B. Deploy on the launch morning, but add an extra approval from the change board
- C. Deploy earlier with the flag off, then release to customers on the business date
- D. Deploy and release on the launch morning, with every engineer on standby all day

<details><summary>Answer</summary>

**C.** Deploy when it is ready; release when the business is ready. A feature flag separates the two, so the marketing date sets the release, not the deployment. A and D keep the decisions glued together, and B adds approval to the same risk. (Lesson 6.1.)

</details>

**20. After an outage caused by a weekend firewall change, Omar proposes that every change, however small, go to the weekly change board. What is the course's view?**

- A. Route by risk instead: another approval layer adds delay and bigger batches
- B. Agree, because a single board reviewing every change gives one consistent view
- C. Require a second engineer to sign off every weekend change, whatever its size
- D. Ban all changes at weekends, so that every change happens during working hours

<details><summary>Answer</summary>

**A.** Approve the kind, not every instance; *Accelerate* is reported to have linked external approval with slower delivery and not with fewer failed changes. The firewall change was a shared, high-risk change and belongs on the high-risk route. B and C add the approval layer the lesson calls the biggest trap, and D bans a kind of change instead of routing it by risk. (Lesson 6.2.)

</details>

**21. Three people give three different answers to "which version is in production?". What does the lesson recommend?**

- A. A shared spreadsheet that each engineer updates after every deployment they do
- B. A what-is-running record written by the pipeline at each deployment, per server
- C. A weekly meeting where teams confirm the versions that they believe are running
- D. A quarterly audit of production servers by an independent external firm

<details><summary>Answer</summary>

**B.** If the record of what is running is typed by hand, it is already wrong; the pipeline writes it at deployment and checks every server. A and C are hand-typed opinions, and D finds drift months late. (Lesson 6.3.)

</details>

**22. The approver for test environments approves 99% of requests, and each approval adds two days. What should Yousef and Sami do?**

- A. Add a second approver, so that the rare bad request is caught by one of them
- B. Ask the approver to respond faster, with a service level of four working hours
- C. Remove the checks entirely, since nearly every request turns out to be fine
- D. Move the checks into a reviewed template and recipe, and drop the approval

<details><summary>Answer</summary>

**D.** If the approver approves almost everything, the approval is a delay, not a control; agree the rules once, build them into the recipe or tool, and review them on a schedule. A doubles the delay, B shortens a wait that adds nothing, and C drops the control instead of moving it. (Lesson 7.1.)

</details>

**23. Each year managers receive long spreadsheets of their staff's access and approve them without reading. What does the lesson suggest?**

- A. Send the spreadsheets twice a year instead, so that each one is shorter
- B. Ask internal audit to perform the review on the managers' behalf each year
- C. Event-driven reviews at join, move and leave, plus exception-based checks
- D. Grant broader standard roles, so that there are fewer rows to review each time

<details><summary>Answer</summary>

**C.** Most problems come at joiner, mover and leaver moments; make reviews event-driven and exception-based, with evidence, and ask risk about the required frequency. A repeats the ritual, B moves the first line's job to audit, and D breaks least privilege. (Lesson 7.2.)

</details>

**24. Tariq wants to start charging business lines for the shared platform next month, using an allocation formula. What should come first?**

- A. A more detailed formula, so that each business line's share is exact to two decimals
- B. Showback in units they can read and change, then finance's decision on moving money
- C. A memo to business heads explaining that the charges are not open to negotiation
- D. Chargeback straight away, since showing costs without charging changes nothing

<details><summary>Answer</summary>

**B.** Show before you charge: nobody accepts a bill they cannot read or influence, and finance decides on moving money. A makes the formula the argument, C removes influence, and D skips the step that builds trust in the data. (Lesson 7.3.)

</details>

**25. The on-call engineer is paged at 3 a.m. for high CPU on a server while card payments are working normally. What does the incident lesson recommend?**

- A. Keep the page, but raise the CPU threshold from 80% to 95% before it fires again
- B. Page on customer symptoms; move cause alerts such as CPU to dashboards and tickets
- C. Page the whole team at once, so that the alert is handled faster by more people
- D. Remove CPU monitoring altogether, since it does not affect card payments directly

<details><summary>Answer</summary>

**B.** Page on what customers feel; record what explains it. A server's CPU explains, it does not page. A still pages on a cause, C wakes more people for the same noise, and D loses the data needed to explain incidents. (Lesson 8.1.)

</details>

**26. Card authorisation was slow three times this quarter at month-end; each time it was "resolved by restart". What should happen?**

- A. Open a problem record, find the contributing factors, give actions owners and dates
- B. Ask the operations centre to restart the service at the start of every month-end
- C. Add the restart to the runbook as the standard fix and close all three incidents
- D. Find the engineer who made the last change and ask them to explain what went wrong

<details><summary>Answer</summary>

**A.** Repeated incidents resolved by restart are an unmanaged problem; an action without an owner, a date and a backlog link is a wish. B and C make the workaround permanent, and D seeks blame instead of contributing factors. (Lesson 8.2.)

</details>

**27. The "Pay by card" SLO is 99.9% of requests answered within 2 seconds, over 30 days, at about 10 million requests a month. What is the error budget?**

- A. About 1,000 bad requests in each rolling 30-day window
- B. About 10,000 bad requests in each rolling 30-day window
- C. About 100,000 bad requests in each rolling 30-day window
- D. Zero bad requests, since any failure breaks the objective

<details><summary>Answer</summary>

**B.** The error budget is one minus the SLO: 0.1% of 10 million is 10,000. A and C are a factor of ten off, the common slip when counting nines, and D confuses an objective with perfection. (Lesson 8.3.)

</details>

**28. A consultant proposes a "single source of truth" programme to model every entity IT could ever need. What does the information-model lesson recommend?**

- A. Approve it, provided it delivers a complete model within the first year
- B. Approve it, but buy one platform first so that the model has a home
- C. Let each team design its own records, so that nobody imposes a model
- D. Start from decisions; a record earns its place only if a decision reads it

<details><summary>Answer</summary>

**D.** Model the decisions first, then only the records and links they need; about ten core records cover most IT organisations. A and B are the universal-model trap, and C gives up the shared identifiers that make records link. (Lesson 9.1.)

</details>

**29. Yousef's team checks the accuracy sample of its own CMDB records each month. What did Nour object to, and why?**

- A. Accuracy matters less than completeness, so the team should measure that instead
- B. A sample of thirty records is too small, so every record should be checked instead
- C. An owner checking its own records is not independent evidence, so swap the samples
- D. The sample should be checked once a year by audit rather than every month by teams

<details><summary>Answer</summary>

**C.** Accuracy from an independent sample matters most; an owner checking itself is not independent. A swaps in a weaker measure, B wastes effort a sample avoids, and D makes the check rare and late. (Lesson 9.2.)

</details>

**30. Before the next five-incident trace test, Reem asks her team to add missing backlog keys to last quarter's changes by hand. What should happen?**

- A. Stop it: back-filling measures effort, not the process; fix how links are made
- B. Allow it, because the links are correct and will make the trace test pass
- C. Back-fill only the changes linked to incidents that audit is likely to pick
- D. Postpone the trace test until every change has been fully back-filled by the team

<details><summary>Answer</summary>

**A.** A trace is only as strong as its weakest link; put identifiers in the work. Back-filling before a test hides the broken process the test is meant to find. B, C and D all spend effort on passing the test instead of fixing how links are made. (Lesson 9.3.)

</details>

**31. The cost per thousand card authorisations fell this quarter, and the product team calls it an efficiency gain. What should Tariq check first?**

- A. Whether the cost model used the most recent exchange rates for supplier invoices
- B. Whether the team's headcount fell during the quarter, since staff are the main cost
- C. Whether volume grew over a fixed cost base, which lowers the average by itself
- D. Whether the authorisation count came from the card switch or from the app itself

<details><summary>Answer</summary>

**C.** A falling average unit cost is not efficiency if growth over a fixed cost explains it; distinguish average from marginal cost. A and D check data details that may matter but do not answer the efficiency claim, and B looks at one line only. (Lesson 10.1.)

</details>

**32. Each card supplier meets its own service levels, yet customers cannot pay for twenty minutes. What does the sourcing lesson say to fix first?**

- A. Add penalties to every supplier contract, so each one tightens its own targets
- B. Keep the integrator role in the bank and set service levels from the journey
- C. Replace the supplier whose component failed last, as a warning to the others
- D. Hand the whole journey to one supplier, so that it becomes accountable for it

<details><summary>Answer</summary>

**B.** You can outsource the work, never the accountability; name the integrator, run one incident process, and derive service levels from the customer journey. A tightens targets that already pass, C punishes without fixing the gap, and D still leaves the bank accountable. (Lesson 10.2.)

</details>

**33. Audit finds no evidence of independent review for production changes, although peer review is built into the pipeline. What is the best response?**

- A. Add a manual sign-off by a manager for every production change from now on
- B. Show auditors how to sample pipeline records of author and approver themselves
- C. Ask the auditors to accept a written statement that review always happens
- D. Replace the pipeline with one that has a stronger, more detailed audit log

<details><summary>Answer</summary>

**B.** The design was sound; the gap was evidence. A control you cannot evidence is a control you do not have, and evidence the flow already produces can close the finding. A is the manual sign-off trap, C is assertion, and D replaces a tool that already holds the evidence. (Lesson 10.3.)

</details>

**34. Both the pipeline and the service platform can create change records for Cards & Payments. What does the toolchain map tell Huda to do?**

- A. Keep both, and reconcile the two sets of change records at each month-end
- B. Move all change records into a new tool that replaces both the existing ones
- C. Give the record one home; the other tool writes to it through an interface
- D. Let each team choose which of the two tools it uses to record its changes

<details><summary>Answer</summary>

**C.** One record, one home: each core record has exactly one system of record, and other tools read, link or feed it, with one writer per field. A institutionalises the overlap, B is a big-bang replacement, and D makes the overlap permanent. (Lesson 11.1.)

</details>

**35. A tool rationalisation programme reports success as "eight tools removed". What should it report instead?**

- A. Fewer manual feeds and conflicting records, and faster answers, at full cost
- B. The number of tools that will be removed next year, to show continued momentum
- C. The size of the new platform's configuration, to show how much it now covers
- D. The share of licences now with one vendor, as a sign of better negotiating power

<details><summary>Answer</summary>

**A.** Success is fewer manual feeds, fewer conflicting records and faster answers, with full cost counted, not a shorter tool list. B, C and D all report activity or scale rather than outcomes. (Lesson 11.2.)

</details>

**36. In a pilot, an AI restart agent runs with Sami's own administrator credentials "just for now". What must change before it leaves the pilot?**

- A. The agent should be moved to run only at night, when fewer customers are online
- B. Its own least-privilege identity, approval for high-impact actions, a full log
- C. A vendor certificate stating that the AI model is safe to use in production
- D. A rule that Sami personally reviews all of the agent's actions once a quarter

<details><summary>Answer</summary>

**B.** Any AI that can change something running needs its own least-privilege identity, approval for high-impact actions and a full log, and a named person stays accountable. A limits timing, not power; C is not a control the bank operates; D reviews too late. (Lesson 11.3.)

</details>

**37. Omar is offered a framework to adopt "wholesale" across the division. What should Huda ask first?**

- A. Which question must it answer here, and which decision will it change for us?
- B. How many of our staff will need to be certified in it in the first year?
- C. Which tool vendors have built their menus around this framework's structure?
- D. Whether the board would prefer this framework or a rival one with more users

<details><summary>Answer</summary>

**A.** Borrow the question, keep your own map: if you cannot name the question and the decision, you are buying vocabulary. B, C and D are the servant signs: certificates, tool menus shaped by the book, and popularity. (Lesson 12.1.)

</details>

**38. A self-assessment survey scores release and change at 4 out of 5, but sampled records show approvals logged after deployment. What score should the review use?**

- A. The survey score, because it reflects the views of the people who do the work
- B. An average of the survey score and the sample, to balance views and evidence
- C. No score at all, because surveys and samples cannot be compared on one scale
- D. The evidence score from the samples: you score what you can show, not say

<details><summary>Answer</summary>

**D.** Score what you can show, not what you say; a policy shows definition, only records of real work show practice. A trusts opinion, B dilutes evidence with it, and C abandons the review. (Lesson 12.2.)

</details>

**39. The executive team plans to announce the target operating model, rename all roles on one date and call the change done. What does the roadmap lesson advise?**

- A. Go ahead, but hire a larger programme office to manage the reporting load
- B. Change one value stream end to end first; put funding before renaming roles
- C. Rename the roles first, since titles signal change and the work follows titles
- D. Delay the whole announcement until all the existing tools have been replaced

<details><summary>Answer</summary>

**B.** Change one value stream end to end before changing one layer everywhere; sequence funding and ownership before renaming. A adds overhead to the same plan, C reverses the sequencing rule, and D puts tools before records and funding. (Lesson 12.3.)

</details>

**40. Before wave 2, Huda's team wants to rewrite the blueprint into an improved version, using ideas no value stream has tried yet. What does the capstone lesson advise?**

- A. Rewrite it now, since wave 2 is the cheapest moment to adopt the better design
- B. Let each new value stream write its own blueprint, then merge them all at year-end
- C. Publish monthly revisions during wave 2, so teams always have the latest ideas
- D. Copy the version that worked in wave 1, gaps marked; batch changes into reviews

<details><summary>Answer</summary>

**D.** Scale only what has worked: wave 2 copies the blueprint that worked in wave 1, with its gaps marked, and revisions are batched into wave reviews, except error fixes. A spreads an untried design to three value streams at once, B gives up the one identifier and one name across streams, and C keeps rewriting the pages teams work by. (Lesson 13.1.)

</details>

## 📚 References
- This course, lessons 0.1 to 13.1: each explanation names the lesson that answers it. The sources behind any research finding mentioned in an explanation are listed in that lesson's References.
- Harvey, N. and DeBellis, D., "Announcing the 2025 DORA Report: State of AI-Assisted Software Development", Google Cloud blog, 23 September 2025 (opened 2026-11-20): https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report
- Harvey, N. and DeBellis, D., "Highlights from the 10th DORA report" (announcing the 2024 DORA report), Google Cloud blog, 22 October 2024 (opened 2026-11-20): https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
