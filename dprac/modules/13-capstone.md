# Module 13 — Capstone and practice

*Qafila is now an Established company: about 400 people in 35 teams, serving merchants in four countries. Since lesson 0.1 you have watched its people write more than thirty artefacts. Maha drew a product and service sketch. Aisha built a backlog and a board. Salma wrote an alert catalogue, a post-incident review and a service-level sheet. Yasmin drafted a decision record, a data inventory, a business case, a threat model and an AI use card. Each was useful on its own. A new joiner still cannot use forty pages written in different years for different team sizes. This module puts them together. In lesson 13.1 Yasmin assembles Qafila's digital practice playbook: one front page, eight step cards and the artefacts behind them. She tests whether the pages agree, whether they fit the company's size today, and whether real work can follow them. You do the same with your own artefact folder. Lesson 13.2 is a practice exam of forty scenario questions across the whole course, so you can find the lessons worth rereading.*

> **Steps:** Discover, Design, Build, Deliver, Operate, Collaborate, Invest, Govern — join the habits of every step into one playbook that a new joiner can read in an afternoon and a team can work by, then check what you have learned.

---

# 13.1 — Capstone: Qafila's digital practice playbook
*Level: 🔴 Advanced* · *Prerequisites: 0.3, 12.2, 12.3* · *Step: Discover, Design, Build, Deliver, Operate, Collaborate, Invest, Govern*

**After this you can** assemble a digital practice playbook from the artefacts of this course (an index with an owner and status for every page, a one-page front page and a card for each of the eight steps), run five checks on it, and write a change log that keeps it alive. *Study time: reading about 20 min, hands-on about 4 h (estimate).*

## ⚡ In 60 seconds
- A **digital practice playbook** is a short, linked set of pages saying how a team actually does its digital work, and who owns each habit.
- Assemble it from the artefacts you already have (lesson 0.3's folder), not from scratch or a framework's structure.
- Three layers: a **front page**, a **step card** for each of the eight steps, and the **artefact pages** behind them.
- Test it with five checks before anyone relies on it.
- The rule that matters most: **a playbook holds the habits people actually use, each with an owner; everything else is an archive.**
- Biggest trap: a thick binder written once, admired once and never opened again.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

Twelve graduates were joining Qafila next month. Maha asked Yasmin: "What do they read in their first week to learn how we work?" Yasmin had learned by asking Salma and Faisal, which does not scale to twelve new people spread across 35 teams.

The shared drive held about forty pages from five growth stages, and some disagreed. Support called its most urgent tickets "P1" (priority 1); the incident pages said "SEV1" (severity 1) for the same thing. The newest team had copied the Traction working agreement, including "Faisal approves every infrastructure change": sensible for twelve people, a queue for 35 teams.

The playbook had to be short enough to read in an afternoon, exact enough for the payments partner's due-diligence team (lesson 11.3), and honest about which pages were habits and which were hopes.

## 📐 How it works

### 🟢 The essentials

**What it is, and is not.** A playbook is the way your team works, written down and linked: not an org chart, a manual nobody follows, or a copy of a framework's chapters (lesson 12.3).

| Layer | Who reads it | What it holds (one page each) |
|---|---|---|
| **Front page** | New joiners, partners, leaders | Product, stage, one line per step, fixed points, "your first week" |
| **Step cards** | Everyone in a team | Habit, rule, artefacts and owners, trigger, hand-offs |
| **Artefact pages** | The people who use them | Template, one worked example, five labels |

**Five labels on every artefact page:** owner; version and date; the stage or team size it was written for; next review date; and **status**, which is one of:

- **Draft:** written, not yet used on real work.
- **Tried once:** used on at least one real piece of work, with lessons noted.
- **Habit:** used routinely by more than one team; someone would notice if it stopped. On a personal project, read this as: used by you on every change for several weeks.

Honest status matters most when outsiders read it (lesson 11.3: "partly, with a plan and a date" beats a "yes" an audit later disproves).

**The step cards.** Qafila's set, in short:

| Step | The habit, in one line | Main artefacts (lesson) | Owner |
|---|---|---|---|
| **Discover** | Believe what people did; test the riskiest assumption first | Evidence log (1.2), assumption map (2.1), experiment brief (6.3) | Karim |
| **Design** | Name the qualities, compare options, write down what we gave up | Decision records (9.1), user stories (6.2), debt register (9.3); data inventory (9.2) owned by Hamad | Faisal |
| **Build** | Small changes, reviewed and explained; a red build comes first | Working agreement (3.1), test plan and CI (3.2), golden path (8.3) | Platform team lead |
| **Deliver** | Deploy small and often; never deploy what you cannot undo | Release plan and flag register (3.3), change route card (7.2) | Platform team lead |
| **Operate** | Every page points to customer pain; fix the system, not the person | Alert catalogue (4.2), severity scale and SLO sheet (4.3), support model (7.1), message kit (7.3) | Salma |
| **Collaborate** | One ordered list; stop starting, start finishing | Backlog (5.2), board (5.3), team map (8.1), dependency register (8.2) | Aisha |
| **Invest** | Know what one unit costs; ask for money in the size of the next decision | Unit-cost sheet (10.2), business case (10.1), supplier register (10.3) | Bilal |
| **Govern** | Decide who decides; ask what can go wrong; build evidence into the work | Decision-rights map (11.1), risk register (11.2), control-to-evidence map (11.3), AI use card (12.2) | Dana |

Terms from earlier lessons, briefly: an **SLO** (service level objective) is the internal reliability target (4.3); a **golden path** is the platform team's supported, recommended way to do a common task (8.3); a **flag register** lists feature flags with owners and removal dates (3.3); a **guardrail** is a built-in, usually automatic check that blocks only what is clearly unsafe (11.1).

Your playbook will differ; the rule behind each row should not: **one habit, one owner, one home for each artefact.** Where a card holds a page someone else owns, such as Hamad's data inventory, the card names that owner.

**The front page** fits on one screen: the product, the stage, one line per step, and the **fixed points** no team changes alone. At Qafila these were the 99.9% monthly order-tracking target, the severity scale, the three change routes and the data sensitivity levels. It ends with "your first week": which cards each role reads first (lesson 0.3).

### 🟡 Going deeper

**Five checks.** Find the gaps on paper before an incident finds them.

| Check | The question | A typical finding |
|---|---|---|
| **Same words** | Does each important term have one definition, on one home page? | "P1" and "SEV1" used for the same thing |
| **Same numbers** | Do targets, limits and periods agree on every page? | Phone numbers kept 30 days on one page, a year on another |
| **One owner, one date** | Does every page have a named owner and a review date? | A register whose owner left in a reorganisation |
| **Right size** | Does each page fit the size of the teams using it today? | A Traction rule that one person approves everything |
| **Follow one piece of work** | Can one real change and one real incident pass through without improvising? | A kind of work with no route |

The fifth check matters most at the **seams**, where one step hands work to another: the week's top contact reasons reaching product's evidence log (7.1 → 1.2), review actions reaching the board (4.3 → 5.2), a release plan naming the alerts that will watch the feature (3.3 → 4.2). Most failures happen there, not inside a card.

**Where disagreements come from.** Rarely typing errors: two teams each settled a real question alone. Support keeps phone numbers to call merchants back; the data owner wrote 30 days because deliveries need no more. Do not quietly edit a page. Name who decides (lesson 11.1), keep the agreed value on **one home page**, and point other pages to it. Where two terms are both needed (severity and priority, lessons 4.3 and 7.2), the home page defines both.

**Right size is this course's special test.** A rule right for two people can be dangerous for 400 ("anyone may change production by hand"); a rule right for 400 can smother a new team of three. Ask which stage each page was written for and whether it fits now; where one size does not fit all, write the difference into the card.

**Follow one piece of work as it really happened**, from the people who did it or its records (commits, tickets, the review), not from the pages' authors. Every "we just…" is a missing or unused page.

### 🔴 Expert view

**Keep it in version control.** Store pages as text in a repository; the card owner reviews changes as pull requests (lesson 3.1), and the history becomes the change log and evidence (lesson 11.3).

**Run it as a product** (lesson 8.3). Ask new joiners and teams which page they opened last month and where they got stuck; archive pages nobody uses. Expect a short dip when teams change how they work (lesson 8.3 has a similar finding on platforms). Fix errors at once; batch other changes quarterly.

**AI can help check it**: an approved assistant can spot two pages with different numbers, if a named person checks every finding (lesson 12.2). Your playbook is also evidence for your learning plan (lesson 12.3), once confidential material is removed. For the manager's view, see [*Running IT as a Business*, lesson 13.1 — Capstone: Najm Bank's IT operating blueprint](../itbiz/index.html#/13.1).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Playbook index** | Every artefact page with its five labels | First, to see what is missing |
| **Front page** | Product, stage, one line per step, fixed points, "your first week" | Next; most readers stop here |
| **Step card** | Habit, rule, artefacts and owners, trigger, hand-offs | One per step |
| **Check sheet** | The five checks, each finding with an owner and a date | Before others rely on it |
| **Walk-through log** | One real change and one incident, page by page, with every point of improvising | Before first use, then quarterly |
| **Playbook change log** | Dated changes with reason and owner, in version-control history | Every change |

Any wiki or repository works; these are templates, not products.

## 🏛️ In practice at Qafila
Illustrative and fictional. Yasmin's first draft pasted every artefact in full: 160 pages. Maha read six. Yasmin cut it to a front page, eight cards and 38 artefact pages: 14 "habit", 16 "tried once", 8 "draft". The golden path stayed "tried once": four teams had each followed it end to end once, but none used it routinely.

**Check findings** (three of eleven):

| Check | Finding | Resolution and owner |
|---|---|---|
| Same words | "P1" and "SEV1" used for the same thing | One home page defines severity and priority and which priorities open an incident. Salma |
| Same numbers | Phone numbers: 30 days in the data inventory, a year in support tickets | The data owner decides after consulting the data protection adviser (9.2); the inventory holds the value. Hamad |
| Right size | Fourth-country team: "Faisal approves every infrastructure change" | Replaced by a plan review checklist (4.1) and a guardrail blocking plans that destroy a data store. Faisal |

**The walk-through.** Salma followed the payment receipts feature (lesson 12.1) from contact reason to release. Two points needed improvising: the messaging provider now received payment amounts, but nobody had rechecked the supplier (lesson 10.3), so Dana did; and no contact reason or knowledge article existed for "I did not get a receipt", so Salma added both.

**The front page** ended: read two cards for your role, pair with a card owner for an hour, and make one small playbook change through a pull request. Yasmin owns the playbook for a year; the graduates' first-week feedback is its first review.

## 🛠️ Exercises

**🟢 Build your playbook index.** Use your artefact folder from lesson 0.3, or the Qafila examples in lessons 0.1 to 12.3. List each artefact with step, lesson and the five labels, then name the steps with no artefact or only drafts.

*Done when:* at least 20 rows (top up from the Qafila examples if your own folder is smaller), every row with all five labels, all eight steps present, and three gaps written as actions with dates.

<details><summary>Model answer and self-check</summary>

**Model answer.** A learner with a room-booking app listed 24 rows. Three of them, in full:

- Working agreement · Build · 3.1 · owner: me · v2, 2026-10 · written for 2 people · review 2027-01 · tried once
- Threat model · Govern · 11.2 · owner: me · v1, 2026-11 · written for 1 person, no users yet · review 2027-02 · tried once
- SLO sheet · Operate · 4.3 · owner: me · v1, 2026-09 · written for a first 50 users · review 2027-01-15 or at launch, whichever is first · draft

Only the commit-message rule, used on every change for two months, earned "habit". Gaps: (1) no rollback runbook; write and try one by 2026-12-15. (2) Operate pages are all drafts (no users yet); review them by 2027-01-15 or at launch, whichever is first. (3) No data inventory; write one by 2026-12-31, because the app will store names and email addresses.

**Self-check.**
- Is every status honest? An unused page is a draft, however good it looks.
- Does every row have an owner and the size it was written for?
- Are your gaps actions with dates?

</details>

**🟡 Write the front page and two step cards, then run four checks.** Write the front page and cards for the two steps you know best, then run the first four checks across your pages.

*Done when:* the front page fits one screen, each card has habit, rule, artefacts with owners, trigger and hand-offs, and the check sheet has at least three findings, each with a resolution, owner and date.

<details><summary>Model answer and self-check</summary>

**Model answer.** Qafila's Operate card: *Habit:* restore service first, then a blameless review. *Rule:* fix the system, not the person. *Artefacts (Salma):* alert catalogue, severity scale, order-tracking SLO at 99.9% monthly, message kit. *Trigger:* a new paging alert, any SEV1 or SEV2. *Hand-offs:* in from Deliver (release plans name signals); out to Collaborate (review actions) and Discover (contact reasons). Findings: (1) a sales page says "99.95% uptime"; Salma and the sales lead agree one wording (7.3) within two weeks. (2) Two runbooks have no owner; on-call adopts them this week. (3) One alert-noise review for all teams no longer fits; Salma splits it by area by 2027-03-31. The front page and the Build card follow the same pattern.

**Self-check.**
- Could a new joiner act on each card without asking you?
- Does each number live on one home page?
- Did you settle disagreements by naming a decider, not by quietly editing?

</details>

**🔴 Follow one piece of work, and keep the playbook alive.** Choose one real change and one incident: your project, an open-source project's merged pull requests and closed issues, or Qafila's migration incident (4.3) and payment receipts (12.1). Walk each through your pages, record every point of improvising, then write three change-log entries and a ten-minute first-week tour.

*Done when:* the log covers at least six steps for the change and four for the incident, ties each improvising point to a missing or unused page, each change-log entry has a reason, owner and date, and the tour lists pages with minutes adding up to ten.

<details><summary>Model answer and self-check</summary>

**Model answer.** *Change, payment receipts (12.1):* contact reasons → evidence log → story with criteria → fit check → threat model → supplier recheck → flag and release plan → alert → knowledge article. Improvising: (a) no recheck when new data reaches a supplier (supplier register, 10.3, unused); (b) no contact reason or article for missing receipts (7.1, missing).

*Incident, failed migration (4.3):* declared (severity scale) → roles named → merchants told → restored from backup (RPO, how much recent data could be lost, noted) → review → actions on the board. Improvising: (c) no message kit (7.3, missing), so merchants heard nothing for an hour; (d) no incident lead for over an hour (roles card, 4.3, missing).

Change log: (1) "Message kit linked from the roles card, because the first message took an hour; Salma; 2026-12-01." (2) "Severity scale names an incident lead as the first step of every SEV1, because nobody led for over an hour; Aisha; 2026-12-08." (3) "Migrations use expand and contract (add the new structure, remove the old later) with a second reviewer, because the migration could not be undone; Faisal; 2026-12-15." Tour: front page (2 minutes), two role cards (5), one worked example (3).

**Self-check.**
- Own or open-source project: did you check each step against the real history (commits, issue comments, the review)? Qafila: against what lessons 4.3 and 12.1 say happened?
- Does each change-log entry change practice, not only wording?
- Would the tour really take ten minutes?

</details>

## ⚠️ Mistakes and traps
- **Pasting everything in.** 160 pages is an archive; keep three layers.
- **Marking hopes as habits.** A page used once by one team is "tried once".
- **Fixing disagreements by editing.** Name the decider, keep the value on one home page, point to it.
- **Skipping the walk-through.** Reading finds typing errors; following real work finds missing routes.
- **Writing it once.** Without an owner, a review rhythm and a change log, it dies at the next reorganisation.

## 🧾 Recap
- Front page, eight step cards, artefact pages; each page with five labels and an honest status.
- Watch the seams between steps.
- Five checks: same words, same numbers, one owner and one date, right size, one real piece of work.
- Version control, run as a product, changes batched except for errors.

## ✍️ Check yourself

**1. Yasmin receives four drafts for the playbook. Which one is a playbook in this lesson's sense?**

- A. Every existing artefact pasted in full into one 160-page folder, all marked "habit"
- B. A new manual organised by a known framework's chapters, one owner per chapter
- C. A front page, eight step cards and existing artefact pages, all labelled
- D. A front page and eight step cards on one wall diagram, with nothing behind them

<details><summary>Answer</summary>

**C.** Three layers from existing artefacts, each owned and labelled. A is an archive with dishonest status, B follows a framework's structure, and D has nothing behind its cards. See "The essentials".

</details>

**2. Under the playbook, a new team of three in the fourth country must get every change approved by a weekly meeting, and now ships once a month. Which check should have caught this?**

- A. Right size: the rule was written for a far larger part of the company
- B. Same words: the team uses a different term for the approval route
- C. Same numbers: the weekly meeting clashes with the monthly release
- D. One owner: the weekly approval meeting has no named chair

<details><summary>Answer</summary>

**A.** Right size asks whether a page fits the teams using it now. B and C look for clashing terms and figures; D finds orphan pages. See "Right size is this course's special test".

</details>

**3. The walk-through finds that the messaging provider now receives payment amounts, but nobody checked the supplier again. What kind of finding is this?**

- A. Same numbers: the register's data list is out of date, so correct the entry
- B. Right size: the supplier rules were written for a smaller company, so rewrite them
- C. Archive: the supplier register is unused, so move it out of the playbook
- D. A missing route: rerun the supplier checks and add a recheck route

<details><summary>Answer</summary>

**D.** Following real work finds work with no route; lesson 10.3 says to recheck a supplier before adding a data type. A calls it a wrong figure, B blames a rule never triggered, and C removes the page the work needed. See "In practice at Qafila".

</details>

**4. The data inventory says phone numbers are deleted after 30 days; the support model keeps them in tickets for a year. What should Yasmin do?**

- A. Change the support model to 30 days, since the inventory is newer
- B. Have the data owner decide and keep the value on one home page
- C. Keep both numbers, since support and delivery have separate needs
- D. Ask an AI assistant which figure is more common and use it on both

<details><summary>Answer</summary>

**B.** Name the decider and keep one value on one home page. A quietly edits, C leaves the contradiction, and D hands the decision to a tool. See "Where disagreements come from".

</details>

**5. Three months in, nobody has opened the "architecture advice forum" page, and its owner has left. What fits this lesson's rule?**

- A. Find an owner and ask teams why they skip it, or archive it
- B. Keep it on one home page, since a playbook covers every topic
- C. Make it compulsory reading for new joiners so it gets used
- D. Delete it now, with the pages that link to it

<details><summary>Answer</summary>

**A.** An unused, ownerless page needs an owner and a reason, or it goes to the archive. B keeps an archive inside the playbook, C forces use without asking why, and D breaks links without asking users. See "Run it as a product".

</details>

## 📚 References
- This course, lessons 0.1 to 12.3: each artefact is taught, with its sources, in the lesson named beside it.
- Library course: [*Running IT as a Business*, lesson 13.1 — Capstone: Najm Bank's IT operating blueprint](../itbiz/index.html#/13.1).
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 7.1 — Capstone: take a new Najm service from empty repo to production with an SLO](../cloud/index.html#/7.1).

---

# 13.2 — Practice exam: 40 scenario questions
*Level: 🔴 Advanced* · *Prerequisites: 13.1* · *Step: Discover, Design, Build, Deliver, Operate, Collaborate, Invest, Govern*

**After this you can** answer forty scenario questions across all fourteen modules in about an hour, then spend about 45 minutes reading the explanations and listing the lessons your wrong answers send you back to. *Study time: reading about 30 min, hands-on about 105 min (estimate).*

## ⚡ In 60 seconds
- Forty scenario questions spread across the whole course, set at Qafila. Use your wrong answers to choose the lessons to reread.
- It is practice on this course only. It is not preparation for any certification, and a score here proves nothing to an employer.
- Set it up like this: cover the answers, give yourself about an hour, answer all forty before you open any explanation, then mark them.
- Read every explanation, including for questions you got right: the wrong options are common real mistakes.
- Questions follow the course: 1 to 3 on Module 0, then three for each of Modules 1 to 12 (4 to 39), and 40 on the capstone. Each question is tagged with its step and lesson, and each explanation names the lesson to reread.
- Qafila, its people and its figures are fictional and illustrative. Questions on money, law, security and regulation test the idea and the question to ask the right person, never a rule for your organisation.

## ✍️ Practice exam

**1. A new support agent at Qafila says: "My job is answering tickets. The app is the engineers' problem." What does lesson 0.1's rule suggest?**

*(Discover · 0.1)*

- A. She is right, because support and engineering are separate jobs with separate goals
- B. A product is software plus its service and people, so her work is part of the product
- C. She should move to engineering, since only code changes ever improve the product
- D. She should wait for a project to be set up before she raises any product problems

<details><summary>Answer</summary>

**B.** A product is software plus the service around it plus the people who keep both going; what support sees is part of the product and feeds the next discovery. A and D treat her job title as her whole job, and C sees only the code. (Lesson 0.1.)

</details>

**2. At Launch, Maha and Faisal skip anything to do with Invest and Govern: "We will do those when we are big." What does lesson 0.2 say?**

*(Discover · 0.2)*

- A. They are right: at Launch only Build and Deliver count as real work for two people
- B. They are right: the last three steps only start once a company has several teams
- C. They are wrong: they should hire a governance lead before writing any more code
- D. They are wrong: those steps happen anyway; the only choice is whether on purpose

<details><summary>Answer</summary>

**D.** Every step happens, whether anyone plans it or not; at Launch the ignored steps are the ones that hurt. A and B are the "only Build and Deliver are real work" trap, and C jumps to a hire a team of two does not need. (Lesson 0.2.)

</details>

**3. Yasmin wants to quote Qafila's "about 400,000 deliveries a day" in a university talk as a typical figure for delivery apps. What should she do?**

*(Discover · 0.3)*

- A. Leave it out, or label it illustrative: Qafila numbers are not benchmarks of anything
- B. Use it, since a course written from general practice will use typical industry figures
- C. Use it after rounding it, so the audience reads it as an estimate rather than a fact
- D. Use it if an AI assistant says that it is in line with similar companies' numbers

<details><summary>Answer</summary>

**A.** Every Qafila number is illustrative, not a benchmark; a figure you reuse needs a source note. B and C still present an invented number as evidence, and D treats an AI answer as a source. (Lesson 0.3.)

</details>

**4. After the pilot demo, twelve of the fifteen shop owners say they love the app. Faisal calls it proof of value. What would lesson 1.1 ask first?**

*(Discover · 1.1)*

- A. Whether the shops still rate the demo as highly when asked again one month later
- B. How many separate features the shops praised, so the team can build more of them
- C. Whether the shops now work differently, for example making fewer phone calls
- D. Nothing more, since twelve of fifteen pilot shops is a strong share for any pilot

<details><summary>Answer</summary>

**C.** Value is counted in the customer's day: what people do differently, and how you would see it. A and D rely on liking the demo, the trap the lesson names, and B counts features, which are the means, not the value. (Lesson 1.1.)

</details>

**5. Karim is preparing a customer interview with bakery staff. Which question follows lesson 1.2?**

*(Discover · 1.2)*

- A. "Tell me about the last time an order went out late. What happened, step by step?"
- B. "Would you use an app that tells your couriers when each order is ready to collect?"
- C. "How much would you pay each month for a tool that saved you most of these calls?"
- D. "Do you think the other shops on your street have the same problem with couriers?"

<details><summary>Answer</summary>

**A.** Ask about specific things that already happened; believe what people did, not what they say they will do. B is the "would you use an app that…" trap, C asks for a prediction, and D asks for an opinion about other people. (Lesson 1.2.)

</details>

**6. Suppose a new same-day pharmacy service (a hypothetical, with illustrative figures) earns 1.00 unit per delivery but costs about 1.30 to serve, mostly staff time phoning couriers. Its manager plans a big sales push. What does lesson 1.3 advise?**

*(Discover · 1.3)*

- A. Go ahead, because fixed costs per delivery will fall as the number of deliveries grows
- B. Go ahead, but leave staff time out of the sheet, since it is not a cost of the software
- C. Go ahead with the push, then raise the price for new shops once volumes are larger
- D. Hold the push: each extra delivery loses money until the cost of one unit is fixed

<details><summary>Answer</summary>

**D.** Contribution per unit is negative (1.00 − 1.30), so growth makes things worse; know what one unit earns and costs before selling more. Compare Qafila's own Launch sheet in lesson 1.3, where a cost of 0.80 left a positive 0.20. A confuses fixed costs with cost to serve, B forgets the human time the lesson calls the biggest early variable cost, and C still sells more loss-making units first. (Lesson 1.3.)

</details>

**7. The team wants to test whether counter staff will tap "ready in 5 / 10 / 15" during the rush. Which plan follows lesson 2.1?**

*(Discover · 2.1)*

- A. Build the full feature, release it to every shop, and judge the results afterwards
- B. Write down the result that would prove the idea wrong before the test starts
- C. Ask the staff whether they would tap the button, and count how many say yes
- D. Run the test first, then decide the pass line once the data can be seen

<details><summary>Answer</summary>

**B.** Decide what result would prove you wrong before you run the test, and use the cheapest test that shows behaviour. A is the "build it all and call it success" trap, C collects opinions, and D lets the data choose its own pass line. (Lesson 2.1.)

</details>

**8. For the first slice of "order ready", Faisal proposes a polished screen for shops and nothing yet for couriers. What does lesson 2.2 say?**

*(Discover, Design · 2.2)*

- A. Good: perfect one step first, so it is finished before the other steps follow
- B. Good: shops are the ones who pay, so their screen should always come first
- C. Change it: a thin first slice should work end to end, from shop to delivery
- D. Change it: build every step in full before any real shop sees the product

<details><summary>Answer</summary>

**C.** Cut across the whole journey, not down one step: the first slice is the thinnest version that works end to end. A and B cut down one step, and D gives up on a small first product altogether. (Lesson 2.2.)

</details>

**9. At Launch, Faisal wants to build Qafila's own login system and its own text-message sending. What does lesson 2.3 advise?**

*(Design · 2.3)*

- A. Build both, because owning every part of the product removes all supplier risk
- B. Build login only, because passwords are too sensitive to trust to any supplier
- C. Choose whichever option has the lowest monthly price on the supplier's page today
- D. Rent both, compare total cost and how hard each is to leave, and record why

<details><summary>Answer</summary>

**D.** Build what makes you different, buy or rent the rest; choose what you can run, afford and leave, and write down why. A and B build routine parts that rarely make a young product different, and C judges by the price tag, not total cost. (Lesson 2.3.)

</details>

**10. On Friday evening Faisal opens a 2,000-line pull request titled "misc fixes". What does Qafila's working agreement, following lesson 3.1, call for?**

*(Build · 3.1)*

- A. Split it into small pull requests, each saying what, why, how to check and how to undo
- B. Approve it quickly, since Faisal knows the code better than anyone else on the team
- C. Merge it tonight and review it next week, when the rest of the team has more time
- D. Ask a second reviewer to share the reading, so the large change is reviewed faster

<details><summary>Answer</summary>

**A.** Small changes, merged often, each one reviewed and explained; if a reviewer cannot understand it over one coffee, split it. B and C skip review for the person most likely to skip tests, and D shares the load without making the change understandable. (Lesson 3.1.)

</details>

**11. One test fails at random about once a day, and engineers press "re-run" until it goes green. What does lesson 3.2 suggest?**

*(Build · 3.2)*

- A. Keep re-running it, since a pass on the second try proves the code itself is fine
- B. Delete the test, since a test that fails at random is adding little value now
- C. Log it with an owner and take it out of required checks until it is reliable again
- D. Raise the automatic retry count in CI, so the test passes without anyone's help

<details><summary>Answer</summary>

**C.** Flaky tests teach people to ignore red; record them in a flaky test log with an owner and a date to return to required checks. A and D hide the problem, and B throws away the protection the test was written for. (Lesson 3.2.)

</details>

**12. The scheduled-deliveries code is ready, but merchants should get the feature only next month. How does lesson 3.3 keep deploying and releasing apart?**

*(Build, Deliver · 3.3)*

- A. Keep the code on a long-lived branch until the launch date, then merge it all at once
- B. Use a feature flag: deploy the code now, and turn it on for merchants later
- C. Move to a monthly deploy window, so every launch happens on the same day
- D. Write a rollback plan, so the code can be removed if the launch date slips

<details><summary>Answer</summary>

**B.** Deploying puts code on servers; releasing turns behaviour on for users; feature flags keep them apart. A creates the long-lived branch lessons 3.1 and 3.3 warn against, C makes deployments larger and rarer, and D is needed anyway but does not separate deploy from release. (Lesson 3.3.)

</details>

**13. An infrastructure plan for a small name change says the orders database will be "replaced". What should the reviewer do?**

*(Operate · 4.1)*

- A. Apply it, because the provider keeps daily backups and a replacement is harmless
- B. Apply it late at night, when fewer merchants would notice a short interruption
- C. Make the change by hand in the console instead, so that no plan is needed at all
- D. Stop: "replaced" can mean deleted and created empty, so fix the change first

<details><summary>Answer</summary>

**D.** Look for *replace* and *destroy* on anything that holds data; one such line can mean losing it. A and B accept data loss, and C breaks the rule that what is not in code does not exist reliably. (Lesson 4.1.)

</details>

**14. An alert for "CPU above 80%" wakes the on-call engineer four nights a week; customers are never affected. What does lesson 4.2 advise?**

*(Operate · 4.2)*

- A. Make it a ticket; page only for symptoms customers feel
- B. Keep the page, but add a second person so nobody is woken up alone
- C. Raise the threshold to 95%, so that it pages a little less often at night
- D. Keep it as it is, since high CPU always comes before a real outage

<details><summary>Answer</summary>

**A.** Every page must point to customer pain and a first action; causes such as CPU explain symptoms rather than page for them. B doubles the noise, C keeps a cause-based page, and D assumes a link the evidence did not show. (Lesson 4.2.)

</details>

**15. Salma sets order tracking at 99.9% monthly. About how much error budget does that leave in a 30-day month?**

*(Operate · 4.3)*

- A. About 4 minutes of bad time
- B. About 43 minutes of bad time
- C. About 7 hours of bad time
- D. About 22 minutes of bad time

<details><summary>Answer</summary>

**B.** A 30-day month has 43,200 minutes; 0.1% of that is 43.2, about 43 minutes. A is roughly the budget for 99.99%, C for 99% and D for 99.95%. (Lesson 4.3.)

</details>

**16. Yasmin saw a wrong fee in a release but said nothing, because a senior engineer had approved it. What does lesson 5.1 suggest the team do?**

*(Collaborate · 5.1)*

- A. Remind her privately that new joiners should check their facts before speaking up
- B. Add a senior sign-off on every release, so juniors never need to raise problems
- C. Ask what stopped her, and add a speak-up rule that anyone may hold a release
- D. Leave it, because psychological safety means not making anyone uncomfortable

<details><summary>Answer</summary>

**C.** The person who sees a problem first must be able to say so at once, and be thanked; a speak-up rule makes that specific. A punishes the messenger, B adds a gate and leaves the silence, and D confuses safety with low standards. (Lesson 5.1.)

</details>

**17. Requests reach Aisha's team from Maha, sales and support, and each sends a "top priority". There are now ten. What does lesson 5.2 recommend?**

*(Collaborate · 5.2)*

- A. One ordered backlog owned by one person: one item first, one item second
- B. A separate list for each requester, so that nobody's work gets forgotten
- C. Ten parallel streams of work, one for each top priority, started at once
- D. A weekly vote by the whole company on what the team should do next

<details><summary>Answer</summary>

**A.** A backlog is one ordered list owned by one person, with no ten "top priorities". B and D spread ownership so nobody orders the work, and C is the too-much-work-in-progress trap of lesson 5.3. (Lesson 5.2.)

</details>

**18. A team has about 24 items in progress and finishes about 6 a week. What does Little's Law say, and what follows?**

*(Collaborate · 5.3)*

- A. About 6 weeks per item; start more items so the team's throughput can rise
- B. About 2 weeks per item; raise the WIP limits so that nobody waits for work
- C. About 1 week per item; the board shows the team is already working fast
- D. About 4 weeks per item; halving WIP at the same pace would roughly halve it

<details><summary>Answer</summary>

**D.** Average time = WIP ÷ throughput = 24 ÷ 6 = 4 weeks; less WIP at the same pace means faster delivery. A, B and C misapply the formula, and A and B also start more work instead of finishing it. (Lesson 5.3.)

</details>

**19. Sales asks for the roadmap to say "bulk upload in March, dark mode in April". What does lesson 6.1 advise?**

*(Discover, Design · 6.1)*

- A. Add both with their months, since a roadmap is the team's release schedule
- B. Add both without months, but keep the roadmap as a list of planned features
- C. Show the problems behind them in now, next and later, each with a measure
- D. Refuse, since a roadmap is only for the team and sales should not see it

<details><summary>Answer</summary>

**C.** A roadmap is a promise about problems, not about features; a date goes on only for a real external deadline. A is the feature-and-date trap, B keeps it a feature list, and D forgets that a roadmap is a communication tool. (Lesson 6.1.)

</details>

**20. A ticket in the backlog says only "add photo upload". What should be added before it enters an iteration?**

*(Discover, Design · 6.2)*

- A. A precise screen design, so engineers need no further conversation about it
- B. Acceptance criteria as given-when-then examples, including unhappy paths
- C. An estimate in hours, so that the iteration plan adds up to the team's capacity
- D. The name of one engineer, so that ownership of the work is clear to everyone

<details><summary>Answer</summary>

**B.** If you cannot say how you would check it, you do not yet know what you want; examples including "what happens when it goes wrong" expose misunderstandings. A treats a story as a full specification instead of a conversation, and C and D do not say what "done" means. (Lesson 6.2.)

</details>

**21. Three days into the live-tracking experiment, the chart looks good and the product manager wants to stop and ship. What does lesson 6.3 say?**

*(Discover, Design · 6.3)*

- A. Stop now, because an early, clear lead is the strongest kind of result there is
- B. Stop now, as long as the two groups have exactly the same number of merchants
- C. Run it longer, until the result looks good on every metric the team collects
- D. Keep to the brief: the duration and decision rule were fixed before it started

<details><summary>Answer</summary>

**D.** Decide what would change your mind before you look at the data; stopping when the chart looks good is the trap the lesson names. A is that trap, B mistakes a trust check for a decision rule, and C keeps looking until something agrees. (Lesson 6.3.)

</details>

**22. "How do I add a second branch?" arrives at support about fifteen times a week. What does lesson 7.1 suggest?**

*(Operate · 7.1)*

- A. Write a knowledge article now; if the question keeps coming, ask for a product change
- B. Answer each one personally, since individual replies keep merchants more satisfied
- C. Escalate each one to the engineers, because they built the branch feature in the app
- D. Drop it from the contact reason list, because it is far too common to be useful

<details><summary>Answer</summary>

**A.** Answer each question well once, write it down, and make the next answer faster; a question that keeps arriving needs a product change. B and C repeat the work every time, and D throws away the clearest signal of where the product confuses people. (Lesson 7.1.)

</details>

**23. A merchant is waiting, and an engineer wants to correct a wrong fee "just quickly" by editing the production database by hand. What does lesson 7.2 require?**

*(Operate · 7.2)*

- A. Make the edit now, and tell the team about it afterwards in the chat channel
- B. Make the edit, as long as the merchant has agreed to the change in writing
- C. Use the data-fix procedure: a script, a second reviewer and a logged run
- D. Refuse, because data in production must never be changed once it is written

<details><summary>Answer</summary>

**C.** Every change to the live system, including data, goes through a known route that leaves a record. A is the "just quickly" trap, B adds the customer's consent but no review or record, and D forbids a fix the procedure allows. (Lesson 7.2.)

</details>

**24. A salesperson wants to promise the pharmacy chain "99.99% uptime"; the internal target for order tracking is 99.9%. What does lesson 7.3 advise?**

*(Operate · 7.3)*

- A. Promise 99.99%, because a higher number reassures a large regulated customer
- B. Promise less than the internal target, and define what is measured and excluded
- C. Promise exactly 99.9%, so that the contract and the internal target always match
- D. Promise nothing in writing, because every service level in a contract is risky

<details><summary>Answer</summary>

**B.** Promise in writing only what you measure, can usually beat and can explain; promise less than you aim for. A is the trap the lesson names, C leaves no margin, and D ignores that customers may reasonably ask for a defined promise. (Lesson 7.3.)

</details>

**25. A change trace shows "ready for pickup" touched four teams (Apps, Core API, Data Infra, Analytics) and took seven weeks. What does lesson 8.1 suggest?**

*(Collaborate · 8.1)*

- A. Add a coordinator who chases all four teams each week until the change ships
- B. Redraw boundaries around the flow of change, so a team owns a part end to end
- C. Split each team further by technical layer, so each layer can move faster
- D. Ask every team to set aside more of its time for other teams' requests

<details><summary>Answer</summary>

**B.** Draw boundaries around the flow of change, not around the technology; layer teams turn each change into a relay race. A and D manage the hand-offs instead of removing them, and C makes the layer problem worse. (Lesson 8.1.)

</details>

**26. Dispatch needs Routing to accept pickup times up to seven days ahead. In what order does lesson 8.2 work through the dependency?**

*(Collaborate · 8.2)*

- A. Coordinate first by agreeing a date with Routing, then look for other options
- B. Put it behind a contract first, then check whether it could be removed instead
- C. Escalate it to the Head of Engineering, who sets the date for both teams
- D. Try to remove it, then make it self-service, then a contract, then coordinate

<details><summary>Answer</summary>

**D.** The dependency ladder runs remove, self-service, contract, coordinate; Qafila removed this one for slice 1. A and B reverse the ladder, and C coordinates by escalation without trying to remove the wait. (Lesson 8.2.)

</details>

**27. One month after the Platform team launches a golden path, some teams are slightly slower, and a manager wants to scrap it. What does lesson 8.3 suggest?**

*(Collaborate · 8.3)*

- A. Expect a possible early dip, warn people, and keep improving it from feedback
- B. Scrap it now, since any slowdown at all proves the platform was a mistake
- C. Make it mandatory for every team at once, so that the dip ends sooner
- D. Hide the slower figures until the platform has been running for a year

<details><summary>Answer</summary>

**A.** The 2024 DORA findings cited in the lesson mention a possible temporary dip, and best results when platforms are user-centred. B overreacts, C forces a platform on teams, the trap the lesson names, and D hides evidence. (Lesson 8.3.)

</details>

**28. A team wants to split the main application into many small services "because that is what everyone does now". What does lesson 9.1 advise?**

*(Design · 9.1)*

- A. Adopt them, since large companies' choices fit companies of every size
- B. Reject them, since a single application is usually the safer choice
- C. Name the qualities first, compare options, and record what is given up
- D. Let each engineer choose a style for the part of the code they work on

<details><summary>Answer</summary>

**C.** Name the qualities first, then compare options against them, then write down what you gave up; monolith, modular monolith and services each fit some situations. A is the fashion trap, B is the same mistake in reverse, and D ignores that architecture decisions are expensive to change. (Lesson 9.1.)

</details>

**29. Two reports show different numbers of "active merchants" for the same month. What should Hamad's team do?**

*(Design · 9.2)*

- A. Find the definition each report uses, and agree one in writing with the owner
- B. Average the two figures and use the average in every board report from now on
- C. Use whichever figure is higher, since it shows the business at its strongest
- D. Delete the older report, so that only one number is left for people to discuss

<details><summary>Answer</summary>

**A.** If two reports disagree, find the definition each uses and agree one with the owner, on a definition page. B and C hide the disagreement, and D removes a report without settling what "active" means. (Lesson 9.2.)

</details>

**30. The Dispatch code is tangled and untested. Faisal proposes rewriting all of it in one go over two quarters. What does lesson 9.3 advise?**

*(Design · 9.3)*

- A. Approve it, because one clean rewrite removes all of the debt at the same time
- B. Leave it as it is for now, because it still works and customers see no problem
- C. Freeze all feature work in Dispatch until the full rewrite has been finished
- D. Replace it slice by slice behind a seam, with the product running throughout

<details><summary>Answer</summary>

**D.** Pay down the debt you keep tripping over, in small steps, while the product keeps running; the big rewrite is the trap. A and C are the big rewrite, and B ignores the cue: Dispatch is changed often, so its debt is the expensive kind even while it still works. (Lesson 9.3.)

</details>

**31. Yasmin's first business case had one option, one confident cost and no running costs. What does lesson 10.1 add?**

*(Invest · 10.1)*

- A. More detail on the one option, so that its single number becomes more precise
- B. Options with doing nothing, cost ranges with running costs, a stop rule
- C. A fifth added to the cost, to cover any risks that might have been missed
- D. A request for the whole three-year amount at once, to save time on approvals

<details><summary>Answer</summary>

**B.** A good case compares options including doing nothing, shows one-off and running costs as ranges, and asks for money in the size of the next decision with a stop rule. A and C polish the single number, and D asks for more than the next decision needs. (Lesson 10.1.)

</details>

**32. This month the cloud bill rose 20% while deliveries rose 30%. Maha is alarmed. What does lesson 10.2 suggest?**

*(Invest · 10.2)*

- A. Cut spending by a fifth at once, to bring the bill back to last month's level
- B. Ignore it, because a cloud bill always rises when a company keeps growing
- C. Look at cost per 1,000 deliveries: it fell, so explain each part's change
- D. Move to a cheaper provider, because a rising bill shows this one is costly

<details><summary>Answer</summary>

**C.** Measure cost per unit of value, not just the size of the bill: 1.2 ÷ 1.3 is about 0.92, so unit cost fell by about 8%, and each change still needs a reason. A cuts without asking what the cost buys, B skips the explanation, and D judges by the total. (Lesson 10.2.)

</details>

**33. For payment receipts, the messaging provider will now receive payment amounts, a kind of data it never had before. What does lesson 10.3 call for?**

*(Invest · 10.3)*

- A. Nothing new, since the supplier was checked when the contract was first signed
- B. Nothing until the yearly review, when all suppliers are checked again together
- C. An email from the supplier's sales team confirming that everything is in order
- D. The due-diligence checks run again for the new data, and the exit plan reviewed

<details><summary>Answer</summary>

**D.** Due diligence is scaled to the supplier's rank and repeated before adding a data type; you can hand over the work, never the accountability. A and B rely on an old check, and C accepts a sales assurance instead of evidence. (Lesson 10.3.)

</details>

**34. After the security scare, someone proposes a central meeting that approves every production change. What does lesson 11.1 advise?**

*(Govern · 11.1)*

- A. Decide who decides, then make the safe way the default with guardrails
- B. Agree, since a central gate on every change is the safest answer to a scare
- C. Agree, but hold the meeting every day instead of weekly so it is faster
- D. Let each team set its own guardrails, since teams know their own changes best

<details><summary>Answer</summary>

**A.** Use many guardrails and few gates; keep gates for rare, hard-to-reverse decisions. B and C are the trap the lesson names (answering a scare with a central approval step), and D leaves each team to invent its own rules, with nobody deciding who decides or what the shared default is. (Lesson 11.1.)

</details>

**35. A team will add a new login option to the courier app. What does lesson 11.2 ask for first?**

*(Govern · 11.2)*

- A. A request for the security team to review it once the release has gone live
- B. A wait for the next yearly penetration test to find any problems in it
- C. Fifteen minutes on a four-question threat model before the team builds it
- D. Nothing extra, since logins come from the provider's managed service anyway

<details><summary>Answer</summary>

**C.** If a change touches logins, money, personal data or access rights, spend fifteen minutes on a threat model before building. A and B look after the fact, and D treats security as someone else's job, the trap the lesson names. (Lesson 11.2.)

</details>

**36. The payments partner's questionnaire asks: "Do you review all access every quarter?" Qafila does this for production systems, not yet for analytics. How should Dana answer?**

*(Govern · 11.3)*

- A. "Yes", because most access is reviewed and a "no" might lose the partnership
- B. "Partly", naming the gap, the plan to close it, its owner and a date
- C. Leave the question blank, so that nothing untrue is written down
- D. "Yes" for now, and start reviewing analytics access next quarter

<details><summary>Answer</summary>

**B.** An honest "partly, with a plan and a date" builds more trust than a "yes" an audit later disproves. A and D answer with what you hope is true, and C hides the gap instead of explaining it. (Lesson 11.3.)

</details>

**37. A team proposes building a new notification service. The capability map shows two applications already support "Notify a merchant". What does lesson 12.1 advise?**

*(Govern, Collaborate · 12.1)*

- A. Check the map first: a third application for one capability needs a reason
- B. Build it, because a new service is quicker than learning the two old ones
- C. Send it to the architecture team for approval and wait for their verdict
- D. Replace both existing applications with the new one in a single change

<details><summary>Answer</summary>

**A.** Check the map before you build; if a capability already has two applications, a third needs a reason, which a fit check states. B ignores the map, C treats architecture as a gate to get past, and D is a big-bang replacement nobody has argued for. (Lesson 12.1.)

</details>

**38. To debug faster, an engineer pastes an unmasked production log into a personal AI chat account. What does lesson 12.2 say?**

*(Govern, Collaborate · 12.2)*

- A. It is fine, as long as the engineer deletes the conversation straight afterwards
- B. It is fine, because the AI's answer is checked before any code is changed
- C. It is fine for logs, because logs hold only technical data, never personal data
- D. It is not fine: check the data level and whether the tool is approved for it

<details><summary>Answer</summary>

**D.** Before pasting, ask what data this is and whether the tool is approved for it; Qafila's card forbids personal accounts and unmasked production logs. A and B apply controls after the data has left, and C is wrong: logs can hold personal data. (Lesson 12.2.)

</details>

**39. A graduate at Qafila asks whether to take three certifications this year. What does lesson 12.3 suggest?**

*(Govern, Collaborate · 12.3)*

- A. Take all three, since certificates count for more than artefacts at interviews
- B. Take none, since practice matters far more than any certificate
- C. Take one only if a role or contract you want asks for it, beside practice
- D. Take the cheapest one, since all of them teach much the same ideas

<details><summary>Answer</summary>

**C.** Take a certification for a stated goal, such as a role or contract that asks for it, or for structured study, and never instead of practice. A is the certificate-collecting trap, B goes too far, and D ignores that each framework answers a different question. (Lesson 12.3.)

</details>

**40. Building the playbook, Yasmin finds the support desk's "P1" and the incident scale's "SEV1" used for the same thing in chat. What does the capstone lesson advise?**

*(Discover, Design, Build, Deliver, Operate, Collaborate, Invest, Govern · 13.1)*

- A. Let each team keep its own scale, each defined on its own home page
- B. Define both on one home page, show how they relate, and link other pages to it
- C. Merge both into one new scale, and rename every past ticket and incident to match
- D. Remove the ticket priority scale, since an incident severity scale alone is enough

<details><summary>Answer</summary>

**B.** The "same words" check keeps each term on one home page; where two terms are both needed (severity for incidents, priority for tickets) the home page defines both and shows how they relate. A keeps the confusion, C rewrites history instead of settling definitions, and D drops a scale the service desk needs. (Lesson 13.1.)

</details>

## 📚 References
- This course, lessons 0.1 to 13.1: each explanation names the lesson that answers it. The sources behind any research finding mentioned in an explanation are listed in that lesson's References.
- Harvey, N. and DeBellis, D., "Announcing the 2024 DORA report" (article heading: "Highlights from the 10th DORA report"), Google Cloud blog, 22 October 2024 (opened 2026-11-22; source of the platform engineering findings behind question 27): https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
