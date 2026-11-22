# Module 5 — Working as a team

*Qafila is still at Traction: about twelve people, one team, 300 merchants and about 4,000 deliveries a day, with changes going to production daily through continuous integration. Modules 3 and 4 gave the team the technical habits to change and run software safely. This module is about the people doing that work together. At two people, Maha and Faisal could keep everything in their heads and settle any question across a desk. At twelve, the same habits produce confusion: nobody is sure who decides, important work lives in chat threads, everyone is busy and yet little gets finished, and the people closest to a problem do not always say what they see. This module covers three everyday practices: clear roles and a team where it is safe to speak up, a simple agile rhythm built on an ordered backlog, and a visible board with limits on how much work is in progress at once. Each lesson leaves you with an artefact you can use on any team: a role map and a team working agreement, an ordered backlog with a definition of done and an iteration plan, and a board with work-in-progress limits and a weekly flow check.*

> **Steps:** Collaborate — agree who does what, make it safe to raise problems early, plan work in small steps, and keep everyone's work visible so the team finishes what matters most.

---

# 5.1 — Roles, collaboration and psychological safety
*Level: 🟡 Intermediate* · *Prerequisites: 3.1, 4.3* · *Step: Collaborate*

**After this you can** tell a role from a job title, write a decision table for a team's recurring decisions, explain what psychological safety is and is not, and draft a team working agreement that makes speaking up and asking for help normal. *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- A **role** is a set of responsibilities; a **job title** is a label on a contract. In a small team one person holds several roles.
- Much friction in a growing team comes from unclear decisions: two people think they decide, or nobody does. A **role map** fixes that in one page.
- **Psychological safety** is a team's shared belief that it is safe to take interpersonal risks: ask a "silly" question, admit a mistake, say "I think this is wrong".
- It does not mean lowering standards. Without it, problems stay hidden until they are expensive.
- The rule that matters most: **the person who sees a problem first must be able to say so at once, and be thanked for it.**
- Biggest trap: thinking safety is a poster. It is built by how people react the next time someone brings bad news.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

Qafila now has about twelve people: Maha, Faisal and five other engineers, Aisha (product), Karim (design), Salma (support and operations), Hamad (data) and Bilal (finance). A few weeks ago a database migration failed and orders were lost for about two hours until they were recovered from backups (lesson 4.3 tells that story).

The post-incident review surfaced two uncomfortable facts. One of the newer engineers had felt uneasy that the migration changed the orders table in one big step, but said nothing: Faisal had said "ship it, we have done a hundred of these". And Salma received the first merchant message about missing orders minutes after the deploy, but waited about twenty minutes before telling the engineers, because the last time she had passed on a merchant complaint she was told it was "probably the merchant's wifi".

Nobody had been told to stay quiet; the team had learned it from small reactions. Meanwhile Aisha and Faisal both thought they decided what the engineers worked on next, and Bilal did not know who could approve a new paid tool. Maha asks Aisha for two things: a map of who decides what, and an agreement on how the team works together, including how it raises problems.

## 📐 How it works

### 🟢 The essentials

**Roles, titles and people.** A **role** is a bundle of responsibilities that needs doing: deciding what to build next, reviewing payment code, answering merchants, being on call (at Qafila, a rota among engineers; lesson 4.2). A **job title** ("Software Engineer") is an employment label. In a team of twelve, almost everyone holds several roles, and some rotate. A **role map** lists the roles and who holds each. Writing it down shows gaps (nobody owns X), overlaps (two people think they own Y) and overload (one person holds eight roles, often the founder or the first engineer).

**Who decides, who does, who is asked, who is told.** For each recurring decision, a **decision table** names who **decides** (exactly one person or named forum, who answers for the call), who **does** the work, who must be **asked** before (few, each with a real reason) and who is **told** after (anyone affected). This is a simplified responsibility chart (a widely used variant is called RACI). The habit matters more than the tool: one decider per decision, written down where everyone can see it.

**Collaboration in plain words.** Prefer working together early (designer, engineer and product manager look at a problem before anyone commits to a solution) over **hand-offs**, where knowledge is lost each time work is passed on. **Pairing** (two people on one task) suits hard problems and teaching. Writing things down so others can respond later (**asynchronous** work) becomes essential once not everyone is in the room.

**Psychological safety.** The organisational researcher Amy Edmondson defined team psychological safety, in a 1999 study of 51 work teams in a manufacturing company, as a shared belief that the team is safe for interpersonal risk taking. She found it was associated with learning behaviour, such as asking for help, seeking feedback and discussing errors, and that learning behaviour in turn was linked to team performance (as reported from the paper's abstract).

In everyday terms: people can ask a basic question, say "I made a mistake", tell someone senior "I think this will break", ask for help early and bring bad news early, without fearing humiliation or punishment.

### 🟡 Going deeper

**What the research says, and what it does not.** Besides Edmondson's study, two sources are often cited:

- **Google's Project Aristotle**, an internal study of its own teams. Google's guide on team effectiveness reports that how members interact mattered more than who was on the team, and lists five dynamics: psychological safety first, then dependability, structure and clarity, meaning and impact (as reported from summaries of Google's re:Work guide).
- **DORA**, a long-running research programme on software delivery now part of Google Cloud. Its culture guide draws on the sociologist Ron Westrum's typology of organisations by how they handle information, and reports that a high-trust culture that emphasises information flow is predictive of software delivery and organisational performance (as reported from the DORA page).

Read these as findings about particular samples, not laws: no single practice guarantees a high-performing team. Westrum's typology gives a concrete test: is the messenger who brings bad news punished, ignored, or thanked and helped? Qafila's "probably the merchant's wifi" reply taught Salma that early, uncertain bad news was not welcome.

**Safety is not comfort.** Psychological safety does not mean everyone agrees or poor work is accepted. Safety with low standards is comfortable but drifts; high standards without safety make people hide mistakes. Learning happens where standards are high *and* it is safe to say "this is not good enough yet", including about your own work.

**What builds it, in behaviour.** Safety comes from repeated small reactions, especially from people with more power:

| Situation | Reaction that destroys safety | Reaction that builds it |
|---|---|---|
| Someone reports a possible problem at night | "Probably nothing, go to bed" | "Thanks for raising it. Let us check together for five minutes" |
| A newer person asks a basic question | Sigh, or "it is in the docs" | Answer, then fix the docs so the next person finds it |
| Someone admits a mistake in a review | "How did you miss that?" | "Thanks for saying it. What made it easy to miss?" |
| Nobody speaks in a meeting | Take silence as agreement | Ask each person directly, or ask for written comments |

**Leaders go first.** When Faisal says in the review "I pushed for the migration and brushed off the warning signs; that is on me", others learn that admitting mistakes is allowed. Blameless reviews (lesson 4.3) depend on this; see [*Cloud & DevOps: Zero to Hero*, lesson 5.3 — Incidents and blameless postmortems](../cloud/index.html#/5.3).

### 🔴 Expert view

**The team working agreement.** Lesson 3.1 wrote a working agreement for code. A team also needs one for *how it works together*: one page, written by the team, covering seven topics: decisions (link the decision table), communication (which channel for what, what must be written), meetings (which exist and why), speaking up (how, at any hour, and what we promise in return), asking for help, disagreement, and a review date.

**Disagree, then commit.** Anyone may argue a decision before it is made; the named decider decides and explains why; then everyone acts on it, and new evidence may reopen it. What this rules out is quietly doing something else.

**Make speaking up cheap and specific.** "We value openness" changes nothing. Specific rules do: "anyone may hold a release by writing 'hold' in the release channel"; "support may page the on-call engineer for any suspected order loss, and is never told off for a false alarm"; "stuck for more than about two hours? Ask". For quieter people and remote colleagues, add a written route (comments on a document) as well as a spoken one, and write decisions where everyone can see them.

**New people are a test.** How a team treats its newest member's questions shows its real culture. See [*From Graduate to Hired*, lesson 6.2 — Your first 90 days: onboarding, the first pull request and asking good questions](../career/index.html#/6.2) for the newcomer's side, and [*A Practical Guide to Becoming an AI-Native Engineer*, lesson 12.1 — Team practice: conventions, review norms, ownership, juniors, metrics and policy](../ainative/index.html#/12.1) for bringing juniors along.

**Roles change with growth.** As the company grows, roles split and move into separate teams (Module 8), so date the role map and expect to change it. For the operating-model view, see [*Running IT as a Business*, lesson 2.2 — Designing a product-aligned operating model: product, platform and enabling teams](../itbiz/index.html#/2.2).

**The memorable rule.** The person who sees a problem first must be able to say so at once, and be thanked for it.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Role map** | A table of the team's recurring roles and who holds each | When people ask "who does this?" more than once a week |
| **Decision table** | For each recurring decision: who decides, does, is asked, is told | When two people both think they decide, or nobody does |
| **Team working agreement** | One page on decisions, communication, meetings, speaking up, help and disagreement | When a team forms, grows or has a painful misunderstanding |
| **Speak-up rule** | A specific promise: anyone may raise a concern or hold a release, and is thanked | After any incident where someone saw a problem and stayed silent |

## 🏛️ In practice at Qafila
Aisha drafts the role map and the agreement with Salma and two engineers; the whole team edits them in a one-hour session. Illustrative and fictional.

> **Qafila decision table (Traction, version 1)**
>
> | Decision | Decides | Does | Asked | Told |
> |---|---|---|---|---|
> | What the team works on next | Aisha | Team | Maha, Faisal, Salma | Everyone |
> | How a feature is built | The engineer leading it | Engineers | Faisal for payments, data or migrations | Aisha |
> | Whether a release goes out | The engineer releasing | Engineer | Anyone may write "hold" | Team channel |
> | Waking the on-call engineer | Salma or anyone who suspects order loss | On-call engineer | Nobody | Faisal next morning |
> | Buying a paid tool | Faisal up to the agreed amount, Bilal above it | Requester | Bilal | Team |
>
> **Qafila team working agreement (Traction, version 1)**
>
> | Topic | We agree |
> |---|---|
> | Speaking up | Anyone may raise a concern about a release, a migration or a customer report at any hour. The answer is always "thank you", even when it turns out to be nothing |
> | Hold | Writing "hold" in the release channel pauses a release until the releasing engineer and the person who wrote it have talked |
> | Help | Stuck for more than about two hours? Ask in the team channel |
> | Disagreement | Argue before the decision; the decider decides and writes why; then we all act on it. New evidence reopens it |
> | Channels | Team channel for work; release channel for releases; phone for anything affecting merchants now. Decisions are written in the ticket or pull request |
> | Meetings | Daily check-in 15 minutes; planning, review and retrospective every two weeks (lesson 5.2). No other recurring meeting without a written purpose |
> | Next review | In six weeks |

In the session, Faisal proposed that only he could hold a release. Salma asked whether that would have helped in the migration incident, when the person with the doubt was not Faisal. Faisal agreed that anyone could, and Maha added "the answer is always thank you".

## 🛠️ Exercises
**🟢 Map the roles in a team you know.** Pick a team you belong to or have belonged to (a student project, a club, a part-time job), or use Qafila. List at least eight recurring roles (things that need doing) and who holds each.
*Done when:* at least eight roles each have a named holder, and you have marked one gap, one overlap and one overloaded person (or written why none exists).

<details><summary>Model answer and self-check</summary>

**Model answer.** For a four-person student project: decide scope (nobody: gap), set meeting times (two people: overlap), write code (three), test (nobody), present (one), talk to the lecturer (one person who also holds four other roles: overload), manage the repository (one), write the report (all, so effectively nobody). Fix: one decider for scope, one owner for testing, two roles moved off the overloaded person.

**Self-check.**
- Did you write roles as things that need doing, not job titles?
- Is every role held by a named person, or marked as a gap?
- Did you spot who holds too many roles?

</details>

**🟡 Build a decision table.** For the team you used, or for Qafila, choose six recurring decisions and fill in a decision table: decides, does, asked, told.
*Done when:* every row has exactly one decider, "asked" holds only people with a clear reason, and at least one row was unclear before you wrote it.

<details><summary>Model answer and self-check</summary>

**Model answer.** Beyond the Qafila table: "Change the delivery fee" (decides: Maha; does: an engineer; asked: Aisha, Bilal, Salma; told: merchants, team); "Add a field to the order data" (decides: the engineer leading it; asked: Hamad, Faisal; told: Salma).

**Self-check.**
- Is there exactly one decider per row?
- Could a newcomer use the table to find out whom to ask?
- Did you keep "asked" short, so decisions do not stall waiting for everyone?

</details>

**🔴 Draft a team working agreement with a speak-up rule.** Write a one-page working agreement for a team of five to twelve people covering the seven topics in the expert view, with one speak-up rule that would have changed Qafila's migration incident and one rule for remote work.
*Done when:* the agreement fits on one page, every rule is specific enough that you could tell whether someone followed it, it includes a review date, and it contains no slogans ("we value openness") without a concrete behaviour attached.

<details><summary>Model answer and self-check</summary>

**Model answer.** Similar to Qafila's version 1, with a speak-up rule such as "before any migration that touches the orders table, the engineer running it posts the plan in the release channel; anyone with a doubt writes 'hold', and the migration waits until they have talked" and a remote rule such as "every decision taken in a call is written in the ticket within the day".

**Self-check.**
- Would the newest person on the team feel able to use the speak-up rule?
- Does each rule describe a behaviour you could observe?
- Does the agreement say how disagreements end?

</details>

## ⚠️ Mistakes and traps
- **Treating job titles as roles.** "She is the product manager" does not say who decides the release date. Write decisions down.
- **More than one decider.** Two deciders means none. Name one person or forum.
- **Confusing safety with comfort.** Avoiding hard feedback is not safety. Keep standards high and make it safe to say "this is not good enough yet".
- **Punishing the messenger by accident.** A sigh or a dismissive "probably nothing" teaches silence. Thank people for early, uncertain warnings, especially false alarms.
- **Leaders who never admit mistakes.** If the most senior people never say "I was wrong", nobody else will. Go first.

## 🧾 Recap
- A role is a responsibility; a title is a label. Map roles to find gaps, overlaps and overload.
- Every recurring decision needs exactly one decider, plus who does, who is asked and who is told.
- Psychological safety is a shared belief that it is safe to take interpersonal risks; research associates it with team learning and better delivery.
- Safety and high standards go together; safety is built by small, repeated reactions.
- A team working agreement turns intentions into specific rules for speaking up and ending disagreements.
- Rule: the person who sees a problem first must be able to say so at once, and be thanked for it.

## ✍️ Check yourself
**1. During the migration incident, Salma waited about twenty minutes before passing on a merchant's report of missing orders, because an earlier report had been dismissed. What does this most clearly show?**

- A. Salma lacked the technical knowledge to judge whether the report was serious enough.
- B. The team needed a monitoring tool that would have detected the missing orders itself.
- C. An earlier reaction taught her that raising uncertain bad news was not welcome.
- D. Support staff should not alert engineers until a problem has been fully confirmed.

<details><summary>Answer</summary>

**C.** The "probably wifi" reply taught silence. A blames the person, B does not explain why a human signal was held back, and D would lengthen the delay. See "What builds it, in behaviour" and "Why it matters".

</details>

**2. Aisha and Faisal both believe they decide what the engineers work on next. What should the team do first?**

- A. Write a decision table that names one decider and lists who must be asked and told.
- B. Let the engineers choose for themselves, so neither Aisha nor Faisal has to give way.
- C. Have Aisha and Faisal decide jointly and require their agreement on every single item.
- D. Ask Maha to decide the order of work herself, since she is the founder and the CEO.

<details><summary>Answer</summary>

**A.** One named decider, with Faisal consulted, removes the overlap. B avoids the question, C creates two deciders, and D overloads Maha instead of clarifying the role. See "Who decides, who does, who is asked, who is told".

</details>

**3. Which statement about psychological safety is accurate?**

- A. It means the team avoids criticism so that everyone feels comfortable at work.
- B. It is a personality trait that some people have and others simply do not have.
- C. It is mainly the responsibility of the human resources function, not the team itself.
- D. It is a shared belief that the team is safe for asking, admitting and disagreeing.

<details><summary>Answer</summary>

**D.** That is Edmondson's definition. A confuses safety with comfort, B makes it individual rather than shared, and C moves it away from the daily reactions that create it. See "Psychological safety" and "Safety is not comfort".

</details>

**4. In a planning meeting, two newer engineers say nothing while Faisal explains his plan. What should Aisha, who runs the meeting, do?**

- A. Treat their silence as agreement, so the meeting can end on time.
- B. Ask each of them directly what they see, or invite written comments after.
- C. Tell them after the meeting that silence in meetings reflects badly on them.
- D. Ask Faisal to present his plans by email only, so nobody feels any pressure.

<details><summary>Answer</summary>

**B.** Silence is not agreement; a direct question or a written route gives quieter people a way in. A misreads silence, C punishes it, and D removes the discussion. See "What builds it, in behaviour" and "Make speaking up cheap and specific".

</details>

**5. The team agrees that anyone may write "hold" to pause a release. A tester holds a release, and it turns out to be a false alarm. What response best fits the agreement?**

- A. Thank the tester, check briefly what made it look wrong, and continue.
- B. Remind the tester that holds cost time and should be used only when sure.
- C. Limit holds to senior engineers from now on, to avoid more false alarms.
- D. Release without comment, so the tester is not embarrassed by the mistake.

<details><summary>Answer</summary>

**A.** The agreement promises thanks; false alarms are the price of early warnings. B and C teach people to wait until sure, which is how the migration warning was lost, and D misses a chance to learn. See "Make speaking up cheap and specific".

</details>

## 📚 References
- Edmondson, A. (1999). "Psychological Safety and Learning Behavior in Work Teams". *Administrative Science Quarterly*, 44(2), 350–383. https://doi.org/10.2307/2666999 — definition of team psychological safety; field study of 51 teams in a manufacturing company; link to learning behaviour and performance (reported from search summaries of the abstract; the full text was not opened).
- Google re:Work, "Guide: Understanding team effectiveness": https://rework.withgoogle.com/en/guides/understanding-team-effectiveness — Project Aristotle's five team dynamics, with psychological safety first (reported from search summaries; the page could not be opened from this environment on 2026-11-22).
- DORA, "Capabilities: Generative organizational culture": https://dora.dev/capabilities/generative-organizational-culture/ — Westrum's typology and DORA's finding that a high-trust, information-flow culture predicts delivery and organisational performance (reported from search summaries; not opened).
- Westrum, R. (2004). "A typology of organisational cultures". *Quality and Safety in Health Care*, 13(suppl 2), ii22–ii27. https://doi.org/10.1136/qshc.2003.009522 — the source of the three culture types (cited via DORA; not opened).
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 5.3 — Incidents and blameless postmortems](../cloud/index.html#/5.3).
- Library course: [*From Graduate to Hired*, lesson 6.2 — Your first 90 days: onboarding, the first pull request and asking good questions](../career/index.html#/6.2).
- Library course: [*A Practical Guide to Becoming an AI-Native Engineer*, lesson 12.1 — Team practice: conventions, review norms, ownership, juniors, metrics and policy](../ainative/index.html#/12.1).
- Library course: [*Running IT as a Business*, lesson 2.2 — Designing a product-aligned operating model: product, platform and enabling teams](../itbiz/index.html#/2.2).

---

# 5.2 — Agile ways of working: backlogs, iterations and flow
*Level: 🟡 Intermediate* · *Prerequisites: 2.2, 5.1* · *Step: Collaborate*

**After this you can** explain the ideas behind agile ways of working, turn a pile of requests into one ordered backlog, write a definition of done, plan a short iteration with a clear goal, and choose between iterations and continuous flow for a team. *Study time: reading about 20 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- **Agile** ways of working deliver in small, frequent steps, learn from real feedback and adjust the plan.
- A **backlog** is one ordered list of the work a team might do next: one item is first, one is second, no ten "top priorities".
- An **iteration** (in Scrum, a "Sprint") is a short fixed period, often one or two weeks, with a goal, a review and a retrospective.
- A **flow** approach skips fixed periods: the team pulls the next item whenever it has room, and plans and reviews on a regular rhythm.
- The rule that matters most: **one ordered list, small items, and "done" means usable by a customer.**
- Biggest trap: copying the meetings and boards without their point: learning sooner and finishing what matters.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

When Aisha joins Qafila as its first product manager, she asks where the list of planned work lives. The honest answer is "everywhere": the team chat, a spreadsheet from Launch, sticky notes on Faisal's monitor, emails from the payment provider, about forty support tickets Salma has tagged "for engineering", and ideas in Maha's head.

The engineers work on whatever was mentioned most recently or loudly. A bakery chain with about a tenth of Qafila's merchant accounts asked for scheduled deliveries three months ago; nobody has started. Meanwhile two engineers spent a week on a dark mode for the admin web page that one person asked for once.

Nobody is lazy. The team has no shared, ordered view of what matters and no regular moment to choose, check and adjust. Aisha proposes a simple rhythm, tried for six weeks and then reviewed.

## 📐 How it works

### 🟢 The essentials

**Where agile comes from.** In 2001 a group of software practitioners published the *Manifesto for Agile Software Development*, with four value preferences: individuals and interactions over processes and tools; working software over comprehensive documentation; customer collaboration over contract negotiation; responding to change over following a plan. It says the items on the right still have value. Read it as preferences, not a ban on plans or documents.

In practice, agile ways of working share a few ideas: **small batches**, so wrong guesses show up while cheap to fix; **short feedback loops**, showing working results often; **one ordered list**, so the team works on the most valuable thing rather than the loudest; **regular reflection** on how the team works; and a **cross-functional team** that holds the skills to finish the work without hand-offs.

**The backlog.** A **backlog** is a single ordered list of things the team might work on: features, fixes, improvements, research. One person (at Qafila, Aisha) is responsible for its order, after listening to others. Items near the top are small, clear and ready to start; items further down can be rough ideas.

A backlog item usually has a **title** saying what changes for whom ("Merchants can schedule a delivery for a later time"), **why** it matters (problem, evidence, who asked), **how we will know it is done** (acceptance criteria; lesson 6.2) and a rough **size** (small, medium, large). **Refinement** is a short regular session to get the top items ready: splitting, clarifying, adding criteria and sizes.

**The definition of done.** A **definition of done** is a short checklist that every item must meet before the team calls it done. It stops "done" from meaning "the code is written but untested and not released".

| Qafila's definition of done (version 1) |
|---|
| Code reviewed and merged (lesson 3.1) |
| Automated tests added and passing (lesson 3.2) |
| Deployed to production, behind a flag if needed (lesson 3.3) |
| Monitoring or an alert covers the new behaviour if it can fail (lesson 4.2) |
| Salma's team has a short note on what changed for merchants or couriers |
| Acceptance criteria checked by the person who asked, or by Aisha |

**An iteration, step by step.** The team repeats a short cycle of four events:

| Event | Purpose | Typical length for a two-week iteration |
|---|---|---|
| **Planning** | Agree an iteration goal and pick the items that serve it | 1–2 hours |
| **Daily check-in** | Coordinate: what is moving, what is stuck, who needs help | 15 minutes |
| **Review** | Show finished work to the people who asked for it; adjust the backlog | 45–60 minutes |
| **Retrospective** | Look at how the team worked; agree one or two changes | 45–60 minutes |

The lengths are common practice, not rules. An **iteration goal** is one sentence saying what will be true at the end ("Merchants can schedule deliveries for tomorrow"), so the team can make trade-offs when something runs long.

### 🟡 Going deeper

**Scrum, briefly.** Scrum is a widely used framework for iteration-based work, described in the freely licensed *Scrum Guide*. In its 2020 version, a small team (typically ten or fewer people) works in fixed-length Sprints of one month or less, with three accountabilities: a Product Owner who orders the backlog, Developers who do the work, and a Scrum Master who helps the team use Scrum well (as reported from summaries of the 2020 guide). If your team uses Scrum, read the short guide itself; this lesson does not replace it.

**Kanban and flow, briefly.** Kanban visualises work, limits how much is in progress and manages flow, without fixed iterations. *The Kanban Guide* describes it; lesson 5.3 teaches the practice.

**Iterations or flow?** Both work. Pick by the team's situation:

| If the team… | Lean towards | Because |
|---|---|---|
| Is new to working together and needs a rhythm | Iterations of one or two weeks | Regular planning and review create shared habits |
| Has many unplanned interruptions (support, incidents) | Flow, or iterations with a reserved share for interrupts | Fixed plans break when a third of the work is unplanned |
| Already releases many times a day and items are small | Flow with a weekly planning and review rhythm | The iteration boundary adds little |

Many teams mix the two: they plan and review every two weeks, but pull work continuously and release whenever an item is done. That is what Qafila chooses.

**Ordering the backlog.** Ask of each item: how much value or learning, for how many customers, how urgent (a deadline or a growing cost of delay), how big, and what risk it reduces. Lesson 6.1 covers methods; the key habit is that one person owns the order, explains it, and anyone can ask why.

**Size items small.** Items longer than a few days are hard to plan and finish. Split by customer value, not technical layer: "schedule for tomorrow" then "for any day this week" beats "scheduling backend" then "scheduling screens", because each slice is usable alone.

**Estimation, lightly.** Estimates help spot items to split and surface disagreement ("you said one day, I said a week: what do you know?"). They are guesses, not promises, and a points total does not measure value or productivity. Counting finished items is often enough (lesson 5.3).

**The retrospective.** Here the team improves how it works, which needs the psychological safety of lesson 5.1. A simple format: what helped, what got in our way, what we will try next (one or two changes, each with an owner). Start the next one by checking whether those changes happened.

### 🔴 Expert view

**Agile is about learning, not speed.** Short cycles exist to find out sooner whether you are building the right thing. A team that ships fast but never looks at what customers do with the result is busy, not agile. Bring evidence to reviews: support tickets, usage data (lesson 6.3), merchant feedback.

**Interrupts are real work.** Qafila's engineers also handle on-call alerts, urgent support and payment-provider changes; plans that ignore these fail. Reserve a share of each iteration for unplanned work, sized from recent iterations, or rotate one engineer a week as the "interrupt handler" who protects the others' focus.

**Ceremony is not the goal.** Teams sometimes keep every meeting and lose the purpose: the daily check-in becomes a status report to a manager, the review is skipped because "nothing is finished". If a meeting has no clear purpose, change it or stop it.

**Agile and the wider company.** When others want fixed dates, share a forecast with a range ("likely in the next two iterations") and update it as you learn. The manager's view of backlogs and traceability is in [*Running IT as a Business*, lesson 4.2 — From requirement to backlog, with traceability](../itbiz/index.html#/4.2); how testers fit into agile teams is in [*Software Testing: Zero to Hero in the AI Era*, lesson 5.3 — Exploratory testing, agile teams and BDD: working with developers, product owners and users](../testing/index.html#/5.3).

**Frameworks are tools.** Scrum, Kanban and scaled frameworks each put these ideas into practice one way (lesson 12.3 compares them). Adopt one if it helps your team, and keep checking that it does.

**The memorable rule.** One ordered list, small items, and "done" means usable by a customer.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Ordered backlog** | One list of possible work, in order, owned by one person | As soon as requests come from more than one place |
| **Backlog item template** | Title (what changes for whom), why, how we know it is done, rough size | For every item that reaches the top third of the backlog |
| **Definition of done** | A short checklist every item meets before it counts as done | From the first iteration; review it at retrospectives |
| **Iteration plan** | One-sentence goal plus the items that serve it, with a share kept for interrupts | At each planning session |
| **Retrospective format** | Helped us, got in our way, try next time (with owners) | At the end of every iteration or every two weeks |
| **Work tracking tool** | A board or ticketing tool (for example Jira or GitHub Projects, named only as illustrations) that holds the backlog | When a spreadsheet or wall can no longer be shared by everyone |

## 🏛️ In practice at Qafila
Aisha gathers every request into one backlog in a week, with Salma's help on the support tickets. Illustrative and fictional.

> **Qafila backlog, top eight (Traction, week 1)**
>
> | # | Item | Why | Size |
> |---|---|---|---|
> | 1 | Merchants can schedule a delivery for tomorrow | Requested by the bakery chain (about a tenth of merchant accounts) and 12 support tickets | Medium |
> | 2 | Orders-table migrations done in safe, reviewed steps | Post-incident action from the migration outage (lesson 4.3) | Small |
> | 3 | Couriers see the shop's opening hours | Support tickets about couriers at closed shops | Small |
> | 4 | Merchants get a receipt by text message | Merchant interviews: needed for their own records | Medium |
> | 5 | Merchants can schedule a delivery for any day this week | Follows item 1 | Medium |
> | 6 | Payment provider's new webhook format | Provider's announced change; deadline in two months | Medium |
> | 7 | Admin page loads faster on order search | Salma's team waits several seconds per search | Small |
> | 8 | Dark mode for the admin web page | One request | Small |
>
> **Iteration 1 plan (two weeks).** Goal: *"Merchants can schedule deliveries for tomorrow, and orders-table migrations run only in safe, reviewed steps."* Items 1, 2 and 3. About a quarter of the team's time is kept for on-call and urgent support, based on the last month.

At the first review, the bakery chain's operations manager tries scheduling by video and points out that bakeries want a *time window* ("between 6 and 8 a.m."), not an exact time; item 5 is rewritten before anyone builds it. At the first retrospective, the team notices the daily check-in has become each engineer reporting to Aisha, and agrees to walk the board instead (lesson 5.3).

## 🛠️ Exercises
**🟢 Turn a pile of requests into one ordered backlog.** Take the ten requests below (or ten from your own project) and put them into one ordered list, with a one-line reason for each position.

Qafila requests: courier app crashes on one older phone model; merchants want a monthly invoice; scheduled deliveries; support wants to search orders by phone number; payment provider webhook change due in two months; a new logo; couriers want to see tips; faster admin search; merchants want to add a second shop; a weekly email report for Maha.

*Done when:* no two items share a position, each reason mentions value, urgency, size or risk, and the top three are small enough to finish in two weeks (split them if not).

<details><summary>Model answer and self-check</summary>

**Model answer.** One defensible order: (1) courier app crash, since couriers who cannot work stop deliveries; (2) scheduled deliveries, "tomorrow" slice first; (3) support search by phone number, small and used daily; (4) webhook change, fixed deadline; (5) faster admin search; (6) monthly invoice; (7) second shop; (8) couriers see tips; (9) weekly email for Maha; (10) new logo. Other orders are fine if the reasons are explicit.

**Self-check.**
- Is there exactly one item at each position?
- Did you consider deadlines (the webhook) as well as value?
- Did you split any large item into a first usable slice?

</details>

**🟡 Write a definition of done and an iteration plan.** For your own project (or Qafila), write a definition of done of five to eight lines, then plan a two-week iteration: a one-sentence goal, the items that serve it, and a share of time kept for unplanned work, with its reason.
*Done when:* every definition-of-done line can be checked yes or no, every planned item serves the goal, and the unplanned share rests on evidence (past interruptions, an on-call rota).

<details><summary>Model answer and self-check</summary>

**Model answer.** A definition of done adapted from Qafila's. Goal: "Couriers never arrive at a closed shop, and support can find an order by phone number." Items: opening hours in the courier app; search by phone number; an alert when an order is assigned outside opening hours. Unplanned share: about a quarter, because over the last four weeks about one day in four went to on-call and support (illustrative).

**Self-check.**
- Could two people disagree about whether a line is met? Make it more specific.
- Did you add unrelated "while we are at it" items?
- Is the unplanned share based on evidence?

</details>

**🔴 Choose iterations or flow, and design the rhythm.** Describe a team you know (or invent one: size, kind of work, share of unplanned work). Choose iterations, flow or a mix, and design its recurring meetings: purpose, length and attendees, with total hours per person per two weeks.
*Done when:* the choice rests on at least two facts about the team, every meeting has a one-line purpose, and total meeting time per person is stated and below about 10% of working time, or you explain why not.

<details><summary>Model answer and self-check</summary>

**Model answer.** A six-person team with about 40% unplanned work: flow with a two-week rhythm. Weekly 45-minute planning and refinement (product manager, designer, two engineers); daily 15-minute board walk; two-weekly 45-minute review with requesters and 45-minute retrospective. Per person, about 4 to 5.5 hours in two weeks, roughly 5 to 7% of an 80-hour fortnight.

**Self-check.**
- Did the amount of unplanned work drive your choice?
- Does each meeting produce a decision, an order or an agreed change?
- Do the people who asked for the work get to see it?

</details>

## ⚠️ Mistakes and traps
- **Several "top priorities".** If everything is priority one, the loudest request wins. Keep one ordered list and explain the order.
- **"Done" that is not done.** Code merged but untested, unreleased or unknown to support is not done. Use a written definition of done.
- **Planning only for planned work.** Interrupts always come. Reserve a share based on recent evidence, or rotate an interrupt handler.
- **Big items.** Items that take weeks hide problems and never finish. Split them into small slices that are each usable.
- **Using estimates as promises or productivity scores.** Estimates are guesses for planning; points totals do not measure value. Count finished, used work instead.

## 🧾 Recap
- Agile ways of working deliver in small steps, learn from real feedback and adjust the plan.
- A backlog is one ordered list owned by one person; the top items are small, clear and ready.
- A definition of done keeps "done" honest; an iteration has a one-sentence goal.
- Iterations give rhythm; flow suits teams with many interrupts and small items; many teams mix both.
- Rule: one ordered list, small items, and "done" means usable by a customer.

## ✍️ Check yourself
**1. Before Aisha arrived, Qafila's engineers worked on whatever was mentioned most recently or loudly. Which change addresses the cause most directly?**

- A. Ask every engineer to keep a personal to-do list and share it at the end of each week.
- B. Gather all requests into one ordered backlog that one named person owns and explains.
- C. Hold a longer weekly meeting where everyone argues for the requests they care about.
- D. Buy a work tracking tool and move every chat message and ticket into it unchanged.

<details><summary>Answer</summary>

**B.** The cause was no shared, ordered view and no owner of the order. A keeps many lists, C rewards the loudest voice, and D moves the mess into a tool without ordering it. See "The backlog" and "Why it matters".

</details>

**2. An engineer says the opening-hours feature is "done": the code is merged, but it is not released and support does not know about it. According to Qafila's definition of done, what is true?**

- A. It is done, because merging the code into main is the team's main measure of progress.
- B. It is done for engineering, and release and support notes belong to a separate stage.
- C. It is nearly done, so it can be counted in the iteration review as a finished item.
- D. It is not done, because it is not in production and support has no note about it.

<details><summary>Answer</summary>

**D.** Qafila's definition of done includes production and a note for Salma's team. A and B narrow "done" to engineering work, and C counts unfinished work as finished. See "The definition of done".

</details>

**3. About a third of the Qafila team's time goes to on-call alerts and urgent support. Their iteration plans fail every time. What is the best first adjustment?**

- A. Ban support requests during iterations so that the plan can be protected.
- B. Make iterations longer, so that interruptions spread over more working days.
- C. Reserve a share of each iteration for unplanned work, based on recent evidence.
- D. Stop planning at all, and let each engineer choose work as they see fit each day.

<details><summary>Answer</summary>

**C.** Planning for interrupts that reliably come makes the plan realistic. A ignores customers and on-call duties, B slows feedback without addressing the cause, and D throws away the shared order and goal. See "Interrupts are real work" and "Iterations or flow?".

</details>

**4. Which is the best way to split the large "scheduled deliveries" item?**

- A. First "schedule for tomorrow", then "schedule for any day this week", each usable alone.
- B. First the database changes, then the backend logic, then the merchant app screens.
- C. First a design document for the whole feature, then the full build in one large step.
- D. Assign the backend to one engineer and the app to another, working in parallel.

<details><summary>Answer</summary>

**A.** Slicing by customer value gives something usable after each step. B and D split by technical layer, so nothing is usable until all parts are done, and C delays feedback to the end. See "Size items small".

</details>

**5. After three iterations, Qafila's retrospectives repeat the same complaint about slow reviews, and nothing changes. What should the team do?**

- A. Skip retrospectives for a while, since they are clearly not helping the team.
- B. Agree one specific change with an owner, and check it at the next retrospective.
- C. Ask Maha to attend the retrospectives so complaints reach someone with power.
- D. Move the complaint into the backlog as a low-priority item for later review.

<details><summary>Answer</summary>

**B.** A retrospective works when it ends with a small, owned change that is checked next time. A removes the improvement loop, C may reduce psychological safety and still produces no change, and D parks the problem. See "The retrospective".

</details>

## 📚 References
- *Manifesto for Agile Software Development* (2001): https://agilemanifesto.org/ — the four value statements (reported from search summaries reproducing the text; the page could not be opened from this environment on 2026-11-22).
- Schwaber, K. and Sutherland, J., *The 2020 Scrum Guide*: https://scrumguides.org/scrum-guide.html — Scrum Team typically ten or fewer people; Product Owner, Scrum Master and Developers; Sprints of one month or less (reported from search summaries; not opened). Licensed under Creative Commons Attribution-ShareAlike.
- *The Kanban Guide*: https://kanbanguides.org/ — definition of workflow, visualisation and work-in-progress control (reported from search summaries; not opened).
- Library course: [*Running IT as a Business*, lesson 4.2 — From requirement to backlog, with traceability](../itbiz/index.html#/4.2).
- Library course: [*Software Testing: Zero to Hero in the AI Era*, lesson 5.3 — Exploratory testing, agile teams and BDD: working with developers, product owners and users](../testing/index.html#/5.3).

---

# 5.3 — Making work visible and limiting work in progress
*Level: 🟡 Intermediate* · *Prerequisites: 5.2* · *Step: Collaborate*

**After this you can** design a team board that matches how work really flows, set and use work-in-progress limits, explain with Little's Law why less work in progress means faster delivery, and run a weekly flow check with four simple measures. *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- **Work in progress (WIP)** is everything started and not yet finished. Too much of it is a common, barely visible reason teams feel busy and finish little.
- A **board** shows every item and where it is. Work not on the board is hidden work.
- A **WIP limit** caps how many items a column can hold. When it is full, help finish something instead of starting something new.
- **Little's Law**: average time per item = work in progress ÷ items finished per week. Halve WIP at the same pace and items finish in about half the time.
- The rule that matters most: **stop starting, start finishing.**
- Biggest trap: a board that shows only the planned work. Support, on-call, reviews and "quick favours" must be on it too.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

A few weeks into the new rhythm, Aisha notices something odd at a daily check-in. Six engineers report fourteen items in progress between them, almost all "nearly done": three wait for review, two for the payment provider, one for Karim's design, and several have been in progress for over two weeks.

Everyone is busy all day, yet scheduled deliveries for tomorrow, the iteration goal, is not live: its engineer was also pulled into two support issues, a review and an urgent change for Maha that nobody else knew about. Salma asks why a "small" change she requested a month ago is still not finished.

The problem is not effort. It is too much work started at once, much of it invisible. Aisha and Faisal decide to put every piece of work on one board, with limits.

## 📐 How it works

### 🟢 The essentials

**Why too much WIP hurts.** Started-but-unfinished items sit **waiting** in queues (for review, for an answer) while nobody works on them; people lose focus **switching** between them; **feedback** comes late because nothing reaches customers; long-open branches drift and conflict (lesson 3.1); and nobody can **predict** when anything will be finished.

**The board.** A **board** (physical or in a tool) has **columns** for the real steps of the work (drawn from how work actually flows, not an ideal process), one **card** per item with an owner, **markers** for blocked items and for kinds of work (planned, unplanned, bug), and **policies** per column saying what must be true for a card to enter or leave it. A simple board:

| Ready | In progress | In review | Releasing | Done (this week) |
|---|---|---|---|---|
| Top items from the backlog, clear and small | Someone is actively working on it | Pull request open, waiting or under review | Merged; deploying, behind a flag or being checked | In production and meets the definition of done |

**Make all work visible.** If support issues, on-call follow-ups or a favour for the CEO are not on the board, the board lies, and nobody can see why planned items are slow. Put every task over about half an hour on the board, marked by type.

**The WIP limit.** A **WIP limit** is the maximum number of cards allowed in a column (or several columns together). When a column is at its limit, nobody pulls a new card into it; people look right on the board for something to help finish: a review, a blocked item, a test. This is **pulling** work: you take new work only when you have finished something. A starting point: a limit near the number of people for "In progress", and a small one for "In review".

**Stop starting, start finishing.** Before taking a new card from "Ready", ask: can I help something already on the board move right?

### 🟡 Going deeper

**Little's Law.** In 1961, John Little published in *Operations Research* a proof of a queueing relationship now known as Little's Law: in a stable system, the average number of items in the system equals their average arrival rate multiplied by the average time each spends there (L = λW). For a team, rearranged:

> **Average time an item takes = average work in progress ÷ average throughput**

**Throughput** is how many items finish per week. **Cycle time** is how long one item takes from start (enters "In progress") to finish (reaches "Done").

Worked example (illustrative): 14 items in progress, about 7 finished a week, so an item takes on average 14 ÷ 7 = 2 weeks. Cut WIP to 7 at the same pace and it takes about 1 week. Nobody worked harder; items spent less time waiting. Treat this as a rule of thumb: the law holds for long-run averages in a fairly stable system, so expect the direction to be right and the numbers to wobble.

**Four flow measures.** A team needs only a few numbers, collected from the board, to see its flow:

| Measure | What it is | What it tells you |
|---|---|---|
| **WIP** | Items started and not finished, now | Whether the team is overloaded |
| **Throughput** | Items finished per week | The team's actual pace, without estimates |
| **Cycle time** | Days from start to done, per item | How long a typical item takes; use the range, not only the average |
| **Work item age** | Days an item still in progress has been there | Which items are stuck *now*, before they become old |

An item in progress for twice the usual cycle time deserves a conversation at today's check-in.

**Walk the board, right to left.** At the daily check-in, instead of going round the people ("what did you do yesterday?"), go through the board from the right: what is closest to done, what blocks it, who can help? This keeps attention on finishing and stops the check-in becoming a status report (the trap Qafila found in lesson 5.2).

**What the research reports.** DORA, the software delivery research programme met in lesson 5.1, describes WIP limits and visual displays of work, combined with other lean practices, as associated with better delivery performance. It advises limits that reflect real capacity, including support and meetings; improving the cause of a delay rather than raising a limit that leaves someone idle; and choosing displayed measures with the team (as reported from DORA's pages). This is the core of the Kanban method, described in *The Kanban Guide*.

### 🔴 Expert view

**Blocked is information.** A blocked card is not a personal failure. Mark it, write why, and count each kind of blocker. If a third of blocked items wait for the same thing, that is the next improvement.

**Swarming.** When an important item is stuck, several people work on it together: code, tests, release note. Slower for each individual, often much faster for the team.

**Limits create useful pain.** A WIP limit will sometimes leave a person with nothing to start. That exposes a bottleneck. At Qafila the review column fills up because nearly all payment code waits for Faisal (lesson 3.1). Raising the limit hides this; training more reviewers fixes it.

**Measures are for the team, not for ranking people.** Throughput and cycle time describe the *system*: the board, the policies, the dependencies. Ranking individuals with them invites gaming (splitting cards, avoiding hard items) and destroys the psychological safety of lesson 5.1. Discuss them at the retrospective and change the system. The library's [*Running IT as a Business*, lesson 1.3 — Flow and delivery metrics that matter, and the ones that mislead](../itbiz/index.html#/1.3) covers this from the manager's side.

**Visible beyond the team.** A good board answers questions without a meeting: Salma sees where her change is; Maha sees that her "urgent" request displaced the iteration goal ("if this goes in now, what comes out?"). For flow across a whole company, see [*Running IT as a Business*, lesson 1.1 — From projects to value: outcomes, value streams and flow](../itbiz/index.html#/1.1).

**Start simple, then evolve.** Begin with the columns you really have and a generous limit, and change one thing per retrospective. Boards that model every possible state in week one are soon abandoned.

**The memorable rule.** Stop starting, start finishing.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Team board** | Columns for the real steps of the work, one card per item, markers for blocked items and work type | From the day more than two people share work |
| **Column policies** | A line per column saying what must be true to enter and to leave it | When people disagree about where a card belongs |
| **WIP limits** | A maximum number of cards per column or across columns | When many items are "nearly done" and few are done |
| **Blocker log** | A simple count of what blocked items were waiting for | When the same kinds of waits keep coming back |
| **Weekly flow check** | WIP, throughput, cycle time range and oldest items, from the board, reviewed for 10 minutes | Once a week, and at each retrospective |
| **Board tool** | A wall, or a board in a work tracking tool (for example Trello, named only as an illustration) | A tool as soon as anyone works remotely |

## 🏛️ In practice at Qafila
Aisha and Faisal run a one-hour session to build the board with the team. Illustrative and fictional.

> **Qafila team board (Traction, version 1)**
>
> | Column | WIP limit | Policy to enter | Policy to leave |
> |---|---|---|---|
> | Ready | 8 | Ordered by Aisha; has acceptance criteria and a rough size | Someone starts it |
> | In progress | 6 | Pulled by an engineer with no other card in progress (except an interrupt) | Pull request opened with the template (lesson 3.1) |
> | In review | 3 | Pull request open, checks green | Approved and merged |
> | Releasing | 2 | Merged | In production; checked after release (lesson 3.3) |
> | Done (this week) | none | Meets the definition of done (lesson 5.2) | Cleared at the weekly review |
>
> Card types: planned (white), unplanned support or on-call (orange), bug (red). Blocked cards get a "blocked" label and a line saying what they wait for.
>
> **First weekly flow check (week 1 of the board):** WIP 14, then 11 after a clean-up (still above the limits, so nobody starts a new card until it falls); throughput 7 items; cycle time 2 to 15 days; oldest item 19 days (a payment-provider question nobody had chased). Blockers this week: 3 waiting for payment-code review, 2 waiting for the provider, 1 waiting for design.

Three of the 14 cards had nobody working on them: one was dropped, two went back to "Ready". The orange cards surprised everyone: almost a third of the work in progress was unplanned, which explained the slipping plans. First actions: Faisal pairs with two engineers on payment reviews, Aisha chases the provider herself, and Maha agrees that her urgent requests go on the board as cards, so the team can say what they displace.

Four weeks later (illustrative): WIP stays at about 6 to 7, throughput is still about 7 items a week, and most items take under a week. Scheduled deliveries for tomorrow went live in week two.

## 🛠️ Exercises
**🟢 Make your own work visible.** For one week, put everything you work on (study, projects, a job) on a board with three columns: To do, Doing, Done, using a free board tool, a document or sticky notes. Add every task over about half an hour, with unplanned ones in a different colour.
*Done when:* the board has at least ten cards, unplanned items are marked, and you have written two sentences on what surprised you.

<details><summary>Model answer and self-check</summary>

**Model answer.** A learner's week: 14 cards, 4 unplanned (a friend's laptop problem, an extra shift, two urgent emails). On Wednesday, 6 items were in "Doing" at once and none finished that day. Surprise: "I start new things whenever I feel stuck, so many things are open and few get done."

**Self-check.**
- Did unplanned work go on the board too?
- How many items were in "Doing" at the busiest moment?
- Which item stayed longest in "Doing", and why?

</details>

**🟡 Design a board with WIP limits and policies.** For Qafila or a team or project you know, design a board: columns that match how work really flows, WIP limits, and a policy to enter and leave each column.
*Done when:* every policy can be checked yes or no, the "in progress" limit is at or below the number of people, any waiting column (such as review) has a limit, and blocked and unplanned work are marked.

<details><summary>Model answer and self-check</summary>

**Model answer.** For a four-person student project: Ready (limit 5; has a clear "done when"), Doing (limit 4; one card per person), Waiting for feedback (limit 2; sent to the lecturer or a teammate), Done (meets the group's checklist). Blocked: a red mark and a note. Unplanned: an orange card.

**Self-check.**
- Do your columns match what really happens, or an ideal process?
- Is there a limit on waiting, not only on working?
- Could a newcomer tell from the policies where a card belongs?

</details>

**🔴 Run a flow check with Little's Law.** Using the data below, calculate the average cycle time Little's Law predicts, compare it with the measured cycle times, find the items needing attention, and propose one change with its expected effect.

Data (illustrative): over four weeks, WIP was 12, 13, 11 and 12 items at the end of each week; throughput was 5, 6, 6 and 5 items per week; measured cycle times of finished items ranged from 2 to 21 days, median 9 days. Items in progress now: A (3 days), B (18 days, waiting for a decision), C (6 days), D (25 days, waiting for review), E to L (1 to 8 days).

*Done when:* you have the averages, the predicted time compared with the median, the items needing attention with reasons, and one change with a measurable expected effect.

<details><summary>Model answer and self-check</summary>

**Model answer.** Average WIP = (12 + 13 + 11 + 12) ÷ 4 = 12. Average throughput = (5 + 6 + 6 + 5) ÷ 4 = 5.5 items a week. Predicted average time = 12 ÷ 5.5 ≈ 2.2 weeks, about 15 calendar days. The measured median is 9 days; a few very old items pull the average above the median. B and D are far older than usual and both are waiting, not being worked on. Change: a WIP limit of 2 on "In review", with the rule "review before starting new work", and a decision deadline for blocked items. Expected effect: WIP down to about 8, and, if throughput holds at about 5.5, average time near 1.5 weeks; check in four weeks.

**Self-check.**
- Did you average over several weeks?
- Did you notice that waiting, not working, made B and D old?
- Is your expected effect a number you can check later?

</details>

## ⚠️ Mistakes and traps
- **Hidden work.** Support, on-call and favours left off the board make planned work look mysteriously slow. Put all work on the board, marked by type.
- **Columns from an ideal process.** A board that does not match how work really flows is ignored. Draw what actually happens, then improve it.
- **Raising the limit when it hurts.** A full column is a signal. Fix the cause (more reviewers, a faster decision) instead of allowing more WIP.
- **Going round the people at the check-in.** Status reports per person hide blocked items. Walk the board from right to left.
- **Using flow measures to rank individuals.** That invites gaming and kills safety. Use them to improve the system, with the team.

## 🧾 Recap
- Too much work in progress causes waiting, switching, late feedback and unpredictable delivery.
- A board shows all work, including unplanned work, in columns that match the real flow, with clear policies.
- WIP limits make the team pull new work only when something is finished; full columns expose bottlenecks.
- Little's Law: average time = average WIP ÷ average throughput, so less WIP at the same pace means faster delivery.
- Watch four measures weekly: WIP, throughput, cycle time and work item age; use them to improve the system, not to judge people.
- Rule: stop starting, start finishing.

## ✍️ Check yourself
**1. Qafila's six engineers have fourteen items in progress, most "nearly done", and the iteration goal is late. What is the most effective first step?**

- A. Ask each engineer to work longer hours until all fourteen items are finished.
- B. Add two more engineers so that more items can be worked on at the same time.
- C. Split the fourteen items into smaller items so that each one looks less late.
- D. Put all work on the board, stop starting new items and help finish open ones.

<details><summary>Answer</summary>

**D.** The cause is too much work in progress, much of it hidden. A and B add effort or people to an overloaded system, and C makes the numbers look better without finishing anything. See "Why too much WIP hurts" and "Stop starting, start finishing".

</details>

**2. A team has, on average, 20 items in progress and finishes about 5 items a week. According to Little's Law, about how long does an item take on average?**

- A. About one week from start to finish.
- B. About four weeks from start to finish.
- C. About five weeks from start to finish.
- D. About twenty weeks from start to finish.

<details><summary>Answer</summary>

**B.** Average time = WIP ÷ throughput = 20 ÷ 5 = 4 weeks. C uses the throughput as the time, and A and D misapply the formula. See "Little's Law".

</details>

**3. The "In review" column at Qafila keeps hitting its limit because nearly all payment code waits for Faisal's review. What should the team do?**

- A. Treat the full column as a bottleneck and train more payment-code reviewers.
- B. Raise the review limit so engineers can keep moving their cards to the right.
- C. Remove the review column and let engineers merge payment changes themselves.
- D. Ask Faisal to review faster by working on reviews in the evenings as well.

<details><summary>Answer</summary>

**A.** A full column exposes the bottleneck; spreading the skill removes it. B hides the problem, C removes a safeguard on money-related code, and D overloads one person and is not sustainable. See "Limits create useful pain".

</details>

**4. Maha wants to see each engineer's throughput and cycle time on a dashboard to decide who is performing best. What is the main problem with this?**

- A. Throughput and cycle time are too hard to measure accurately from a team board.
- B. These measures only make sense for teams that use fixed-length iterations.
- C. They describe the system, so ranking people invites gaming and harms safety.
- D. Individual measures should be private and only shared with each engineer.

<details><summary>Answer</summary>

**C.** Flow measures reflect the board, policies and dependencies; ranking individuals leads to gaming and damages psychological safety. A is wrong (they come straight from the board), B is wrong (they suit flow-based teams too), and D still judges individuals. See "Measures are for the team, not for ranking people".

</details>

**5. At the daily check-in, which approach best supports finishing work?**

- A. Each person in turn says what they did yesterday and what they will do today.
- B. The product manager asks each engineer for a percentage complete per item.
- C. The team discusses only new items in "Ready" and who will start each one next.
- D. The team walks the board from right to left, asking what blocks each item.

<details><summary>Answer</summary>

**D.** Walking the board from the right focuses on finishing and surfaces blocked items. A and B turn the check-in into a status report that can hide blockers, and C focuses on starting rather than finishing. See "Walk the board, right to left".

</details>

## 📚 References
- Little, J. D. C. (1961). "A Proof for the Queuing Formula: L = λW". *Operations Research*, 9(3), 383–387. https://doi.org/10.1287/opre.9.3.383 — the proof of Little's Law (reported from search summaries of the bibliographic record; the full text was not opened).
- DORA, "Capabilities: Work in process limits": https://dora.dev/capabilities/wip-limits/ — limits that reflect real capacity including support and meetings; improve the cause of delays rather than raising limits (reported from search summaries; the page could not be opened from this environment on 2026-11-22).
- DORA, "Capabilities: Visual management": https://dora.dev/capabilities/visual-management/ — visual displays combined with WIP limits and production feedback associated with higher delivery performance; involve the team in choosing measures (reported from search summaries; not opened).
- *The Kanban Guide*: https://kanbanguides.org/ — definition of workflow, Kanban board and WIP control (reported from search summaries; not opened).
- Library course: [*Running IT as a Business*, lesson 1.3 — Flow and delivery metrics that matter, and the ones that mislead](../itbiz/index.html#/1.3).
- Library course: [*Running IT as a Business*, lesson 1.1 — From projects to value: outcomes, value streams and flow](../itbiz/index.html#/1.1).
