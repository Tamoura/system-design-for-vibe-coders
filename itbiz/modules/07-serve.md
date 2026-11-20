# Module 7 — Serve: requests, access and consumption

*Once a product or platform is running, people inside the bank start to use it: they ask for things, sign up for things, get access to things and consume things that cost money. This module is about that everyday exchange between Najm Bank's Technology division and the people it serves. You will turn slow, ticket-driven asks into repeatable recipes and self-service, keep a clear and reviewable picture of who has signed up for what and who can do what, and make consumption and its cost visible to the business lines that drive it, before deciding whether to bill them.*

> **Steps:** Serve — make it easy, safe and visible for the business to ask for, use and pay for what IT provides.

---

# 7.1 — Request fulfilment and self-service
*Level: 🟡 Intermediate* · *Prerequisites: 2.3, 6.2* · *Step: Serve*

**After this you can** pick the five most frequent asks reaching your Technology division, write a recipe for each (steps, checks, approver, evidence, target time) and decide which ones move to self-service first. *Study time: reading about 15 min, hands-on about 110 min (estimate).*

## ⚡ In 60 seconds
- A **request** here means any ask from a person or team for something IT already knows how to provide: a test environment, a software licence, a shared mailbox, a database copy, a report extract. It is not a fault and it is not a new piece of work.
- Most delay in fulfilling requests is **waiting**, not working: waiting in a queue, waiting for an approver, waiting for a hand-off between teams.
- The rule that matters most: **a request you fulfil more than a few times a month deserves a recipe, and a recipe that never needs judgement deserves self-service.**
- A **recipe** is the written, agreed way to fulfil one kind of request: inputs, steps, checks, who approves (if anyone), what evidence is kept, and the target time.
- Decision cue: if the approver approves almost everything, the approval is a delay, not a control. Move the check into the recipe or the tool.
- Biggest trap: putting a web form in front of the same slow manual process and calling it self-service.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers in this lesson are illustrative figures, not benchmarks.

Reem's Cards & Payments team needed a new test environment to try a change to card limits. This was not the shared-environment booking queue from lesson 6.3. The ephemeral environments described there use synthetic data and cover routine tests; this one had to stay up for weeks, hold masked card data and get its own firewall rules, and no pipeline built an environment like that. She raised a ticket on Sunday. It reached Yousef's service desk, which passed it to the infrastructure team, which asked the security team to approve firewall rules, which asked Reem's team for a diagram, which went back to infrastructure. The environment arrived on the ninth day. When Huda later traced the ticket, the actual work (building the servers, opening the ports, loading the data) took about six hours. The rest was queues and hand-offs.

Meanwhile Sami's platform team had built a template that creates this longer-lived kind of environment in under an hour, with the approved network rules already in it. Hardly anyone used it, because nobody had told the service desk it existed, the security team had never formally agreed that the template's rules were acceptable, and there was no record linking environments built by the template to a product, an owner or a cost.

Omar heard about the nine days from the head of retail banking, not from IT. That is the point of this lesson: the business experiences IT through its requests. A slow, opaque request process makes even a good platform look like a bottleneck, and a fast but uncontrolled one creates risk and cost nobody can trace.

## 📐 How it works

### 🟢 The essentials

**Three kinds of ask.** Before you design anything, sort what arrives at the front door (lesson 4.1) into three plain groups:

| What the person wants | Example at Najm Bank | Where it goes |
|---|---|---|
| Something IT already provides, in a known way | A test environment, a licence, access to a report | **Request fulfilment** (this lesson) |
| Something that used to work and now does not | The payments dashboard will not load | Operations and incident handling (lesson 8.1) |
| Something new, or a change to what exists | A new card-limit feature | Demand and backlog (lessons 4.1, 4.2) |

The test is simple: "Do we already know exactly how to do this, and have we done it before?" If yes, it is a request. Mixing the three in one queue is a common cause of delay, because a five-minute licence waits behind a three-week feature.

**The recipe.** For each frequent kind of request, write one page:

1. **Name and who may ask** (for example, "Test environment, small; any product team lead").
2. **Inputs** the asker must give (product, owner, cost centre, data class, end date).
3. **Steps**, with which team or tool does each one.
4. **Checks** that must pass, and whether a person or the tool makes them.
5. **Approver**, if any, and why that person.
6. **Evidence kept** (what record shows it was done properly).
7. **Target time** and how it is measured.

The recipe is the management artefact. The service catalogue entry (lesson 2.3) is what the business sees; the recipe is how IT delivers it.

**Measure the wait, not just the work.** For each recipe, track two times: **elapsed time** (from ask to done, as the asker experiences it) and **touch time** (the minutes someone actually worked on it). The gap is waiting. In Reem's case the elapsed time was about nine days and the touch time about six hours (illustrative). Lesson 1.2 shows how to map this; here you only need the two numbers per recipe.

### 🟡 Going deeper

**From recipe to self-service.** Self-service means the asker gets the result directly from a portal, a command or an API, without a person in the middle. A recipe is ready for self-service when:

- the inputs can be checked by the tool (is the cost centre valid? is the product registered?);
- the checks are rules, not judgement (data class "test" with masked data only);
- any approval is either not needed, or can be replaced by a rule agreed once with its owner;
- the steps are already automated, or can be;
- the evidence is written automatically to the right record.

If any item fails, fix that item first. Do not build a portal over a manual process.

**Pre-agree the checks once.** Many approvals exist because someone needed assurance once, years ago. Security wanted to see firewall rules; finance wanted to know who pays. Instead of asking every time, agree the rule once and build it into the recipe or template: "environments built from template v3 use only these network rules, reviewed by security on this date and re-reviewed every six months." The approver moves from approving each request to approving the recipe. That is usually a stronger control, because the rule is applied the same way every time and leaves evidence every time.

**Rank by volume times wait.** You cannot fix every request. List the kinds of request from the last three months, with count and median elapsed time. Multiply them. The top five usually account for a large share of the total waiting, and they are where recipes and self-service pay back first.

| Request kind | Count per quarter | Median elapsed days | Count × days | First move |
|---|---|---|---|---|
| Test environment | 120 | 9 | 1,080 | Template self-service |
| Read access to a reporting database | 300 | 3 | 900 | Pre-agreed rule for non-sensitive data |
| Software licence | 400 | 2 | 800 | Self-service from licence pool |
| Shared mailbox | 80 | 4 | 320 | Recipe, keep manual for now |
| Firewall change for a new partner | 15 | 12 | 180 | Keep as reviewed work |

Illustrative figures, not benchmarks. Note the last row: rare, risky asks with real judgement stay with people. Self-service is for the routine.

### 🔴 Expert view

**A platform is a product, and its users are your colleagues.** Sami's template failed not because it was technically poor but because nobody treated it as something to be adopted. Google Cloud's announcement of the 2024 DORA report lists four findings on platform engineering: internal developer platforms increased developer productivity; they were more common in larger organisations; a platform initiative might bring a temporary dip in performance before improvements show as the platform matures; and results were best when platform work put user-centred design, developer independence and a product-oriented approach first. For the engineering side, see [*Cloud & DevOps: Zero to Hero*, lesson 0.1 — What cloud, DevOps, platform engineering and SRE are](../cloud/index.html#/0.1). The operating-model point is that the platform team needs a named owner, users it talks to, an adoption measure, and a place in the service catalogue, like any other product.

**Self-service still needs records.** A request fulfilled in one click must still answer the questions an auditor or a cost owner will ask later: who asked, for which product, under which rule, at what cost, until when. If self-service skips the record, you have traded a slow, traceable process for a fast, untraceable one. Lesson 9.1 covers the records; lesson 7.3 covers the cost.

**End dates are part of the request.** Environments, licences and access granted "for now" tend to stay forever. Make an end date or a review date a required input, and let the platform remind the owner and then reclaim the item. This is one of the cheapest cost and risk controls available.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Request recipe** | One page per request kind: who may ask, inputs, steps, checks, approver, evidence, target time | For every request kind you see more than a few times a month |
| **Request ranking sheet** | Request kinds with count, median elapsed time and count × time | Quarterly, to choose which recipes to improve or automate |
| **Elapsed vs touch time chart** | For each recipe, the asker's wait against the minutes of work | To show where waiting, not effort, is the problem |
| **Self-service readiness check** | The five tests: inputs, rule-based checks, approvals, automation, automatic evidence | Before building any portal or form |
| **Pre-agreed rule record** | A short note of a check agreed once, its owner and its review date | When replacing a per-request approval |
| **Service management platform or developer portal** | Where recipes are run and recorded; examples include a service management platform or an internal developer portal | To run and record requests; examples only, not endorsements |

## 🏛️ In practice at Najm Bank
Fictional and illustrative. Yousef and Sami ran the ranking sheet together for one quarter. Test environments came out first. They wrote this recipe:

> **Recipe: test environment, small (v1).** *Who may ask:* product team leads. *Inputs:* product name (must exist in the product list), owner, cost centre, data class (test, masked only), end date (maximum 90 days, renewable). *Steps:* platform template v3 builds the environment; network rules come from the template. *Checks:* the tool validates product, cost centre and data class; no production data allowed. *Approver:* none per request; Nour's team and security reviewed template v3 once and will re-review it every six months. *Evidence:* the platform writes the environment, its owner, product, cost centre and end date to the environment record. *Target:* ready in under one working day; measured from submission to ready.

Yousef objected at first: "If nobody approves, who is accountable?" Nour answered that the accountability moved to the template review and the automatic record, which were easier to audit than nine e-mails. Within the next quarter, the median elapsed time for this request fell to under a day, and the service desk stopped handling it at all (illustrative). The firewall-change request stayed with people, as it should.

## 🛠️ Exercises
**🟢 Sort the asks.** Take 30 recent tickets from your service desk (or invent 30 realistic ones for Najm Bank). Sort each into "request", "something broken" or "something new".
*Done when:* every item is sorted, and you have written one sentence on how many of the "requests" were waiting in the same queue as the other two kinds.

<details><summary>Model answer and self-check</summary>

**Model answer.** A typical sort finds most items are requests, a smaller share are faults, and a few are disguised new work ("can you add a field to the report"). The useful finding is usually that all three share one queue and one priority scheme. **Self-check.**
- Did you apply the test "do we already know exactly how to do this"?
- Did you put disguised new work in "something new", even if it was raised as a request?
- Did you note any item that did not fit, rather than forcing it?

</details>

**🟡 Write two recipes.** For the two most frequent request kinds, write a one-page recipe with all seven parts, and record the current elapsed and touch time for each.
*Done when:* both recipes have all seven parts filled in, each approval has a stated reason, and each has an elapsed and touch time (measured or estimated, and labelled which).

<details><summary>Model answer and self-check</summary>

**Model answer.** See the Najm Bank recipe above for the shape. A good recipe is short, names the tool or team for each step, and states whose rule each check enforces. **Self-check.**
- Could a new service desk analyst follow it without asking anyone?
- Is every approver there for a reason you could explain to an auditor?
- Is the evidence written to a record someone else can find?
- Is there an end date or review date where one is needed?

</details>

**🔴 Make the self-service case.** For one recipe, apply the five readiness tests, list what fails, and write a half-page proposal to move it to self-service, including which approval becomes a pre-agreed rule and who must sign it.
*Done when:* the proposal names each failing test and its fix, names the rule owner, and states the measure you will use to show it worked.

<details><summary>Model answer and self-check</summary>

**Model answer.** A strong proposal says, for example: "Inputs: product list exists, cost centre check needs a finance feed (fix: API from the finance system). Checks: rule-based. Approval: security per request becomes a template review every six months, owner Head of Security. Automation: template exists. Evidence: platform must write to the environment record (fix: two weeks of work). Measure: median elapsed time and share of requests self-served." **Self-check.**
- Did you avoid building a form over a manual step?
- Is the replaced approval stronger, not weaker, as a control?
- Did you choose a measure the asker would recognise?

</details>

## ⚠️ Mistakes and traps
- **A form over a slow process.** A portal that creates the same ticket for the same queues changes nothing. Fix the steps and approvals first, then add the portal.
- **Approvals nobody refuses.** If an approver approves nearly everything, the approval is ceremony. Turn it into a rule agreed once and reviewed on a schedule.
- **One queue for everything.** Requests waiting behind faults and new work inflate every wait. Separate them at the front door.
- **Measuring only the work.** Teams report touch time and look efficient while askers wait days. Report elapsed time too.
- **Self-service without records.** Fast but untraceable creates cost and audit problems later. Every self-service path writes its evidence automatically.
- **No end dates.** Items granted "for now" stay forever. Make end or review dates a required input.

## 🧾 Recap
- A request is an ask for something IT already knows how to provide; keep it apart from faults and new work.
- Write a **recipe** for each frequent request kind: who may ask, inputs, steps, checks, approver, evidence, target time.
- Most of the delay is **waiting**: track elapsed and touch time per recipe.
- Move a recipe to **self-service** only when inputs, checks, approvals, automation and evidence are all ready.
- Replace per-request approvals with **rules agreed once** and reviewed on a schedule.
- Treat the platform as a **product** with users, an owner and an adoption measure.

## ✍️ Check yourself
**1. A product team asks for read access to a non-sensitive reporting database. The service desk has handled this ask hundreds of times. How should it be treated?**

- A. As new work for the backlog, because each team's needs differ and must be analysed.
- B. As a fault, because the team cannot do its job until it has the access it needs.
- C. As a request with a recipe, because IT already knows exactly how to provide it.
- D. As a portfolio item, because access affects risk and must go to the review board.

<details><summary>Answer</summary>

**C.** IT knows exactly how to provide it and has done it many times, which is the test for a request. A treats a routine ask as new work, B confuses "I am blocked" with "something broke", and D sends routine work to a board meant for investments. See "Three kinds of ask".

</details>

**2. Huda finds that Reem's environment took nine days, but the actual work took about six hours. What does this mainly show?**

- A. Most of the elapsed time was waiting in queues, approvals and hand-offs.
- B. The infrastructure team needs more staff to handle the volume of requests.
- C. The environment was too complex and should have been split into smaller asks.
- D. The service desk recorded the wrong times and the real work took much longer.

<details><summary>Answer</summary>

**A.** The gap between elapsed time and touch time is waiting. B assumes the work was the constraint, which the numbers do not show. C and D have no support in the scene. See "Measure the wait, not just the work".

</details>

**3. Security approves every test-environment request and has refused none in two years. What is the best change?**

- A. Remove the security approval with no replacement, since it never finds anything.
- B. Add a second approver from operations, so two teams share the accountability.
- C. Ask security to approve faster by setting a target time of one working day.
- D. Agree the network rules once in the template, reviewed by security on a schedule.

<details><summary>Answer</summary>

**D.** A rule agreed once and built into the template is applied every time, leaves evidence and is reviewed periodically. A drops the assurance entirely, B adds more waiting, and C keeps a step that adds delay but no control. See "Pre-agree the checks once".

</details>

**4. Sami proposes a new portal page for shared mailboxes. Behind it, the same three teams will still pass a ticket between them by hand. What is the main problem?**

- A. Portals are expensive to build, and shared mailboxes are too rare to justify one.
- B. It is a form over a manual process, so the asker will still wait for the same hand-offs.
- C. Shared mailboxes should be classed as new work, not as a request with a recipe.
- D. The service desk will lose visibility of the request once the portal is in place.

<details><summary>Answer</summary>

**B.** Self-service means the asker gets the result without people in the middle; a portal that feeds the same manual hand-offs does not change the wait. A may be true for some cases but is not the main issue, C misclassifies a routine ask, and D is not implied. See "From recipe to self-service".

</details>

**5. Which fact should decide which request kinds Najm Bank automates first?**

- A. The count of each request kind multiplied by its median elapsed time.
- B. Which request kinds the most senior business leaders complain about most.
- C. Which request kinds the platform team finds most interesting to automate.
- D. Which request kinds have the longest recipe, since those take the most effort.

<details><summary>Answer</summary>

**A.** Volume times wait shows where total waiting is concentrated and where automation pays back first. B and C rank by noise or preference, and D ranks by document length rather than delay. See "Rank by volume times wait".

</details>

## 📚 References
- Google Cloud blog, "Announcing the 2024 DORA report" (2024), section on platform engineering: https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 0.1 — What cloud, DevOps, platform engineering and SRE are](../cloud/index.html#/0.1).

---

# 7.2 — Subscriptions, entitlements and access rights
*Level: 🟡 Intermediate* · *Prerequisites: 7.1* · *Step: Serve*

**After this you can** write, for one product or platform, a one-page register that answers who has signed up to use it, what each sign-up allows, and who holds which technical access, and set the review rhythm that keeps those three answers true. *Study time: reading about 15 min, hands-on about 85 min (estimate).*

## ⚡ In 60 seconds
- Three different questions get mixed up under the word "access": **who has signed up to use this?**, **what does that sign-up allow?**, and **which named person or system can technically do what?**
- In this course: a **subscription** is what a business line or team has signed up to use, and keeps using until someone ends it. An **entitlement** is what that sign-up allows (a tier, a quantity, a set of features). An **access right** is the technical grant that lets one named person or system act.
- Each question has a different owner: the business owner of the sign-up, the product or service owner for what it allows, and the system owner for technical access.
- The rule that matters most: **every grant has an owner, a reason and an end; anything without all three is a finding waiting to happen.**
- Decision cue: when someone changes role or leaves, can you list everything they could do within an hour? If not, the records are not good enough.
- Biggest trap: reviewing access rights once a year by sending managers long spreadsheets they approve without reading.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers in this lesson are illustrative figures, not benchmarks.

Nour's team prepared for an internal audit of the card-dispute system. The auditors asked three questions. Which business units use the system? What are they allowed to use it for? Who can change a dispute outcome? The first answer came from a two-year-old spreadsheet. The second was in a contract with the system's supplier that nobody in IT had read. The third came from the system itself: 140 people could change outcomes, of whom 31 had moved to other roles and 6 had left the bank, though their accounts were disabled in the directory (illustrative).

Nobody had done anything wrong on purpose. People joined, moved and left; business units signed up and later stopped using parts of the system; the supplier licence was renewed at a higher tier "just in case". Each change was small. Together they made a picture that could not be explained.

Lina added a fourth problem: the bank was paying for 400 named-user licences, but only about 250 people had logged in during the last quarter (illustrative). The same missing records that worried Nour were costing Tariq's budget money. Access and consumption are two views of the same facts.

## 📐 How it works

### 🟢 The essentials

**Three questions, three owners.** Keep the three ideas apart. They answer different questions, are owned by different people, and change at different speeds.

| Question | The term in this course | Who owns the answer | Example at Najm Bank |
|---|---|---|---|
| Who has signed up to use this? | **Subscription** | The business owner who signed up (often a head of a business line or team) | Retail Cards has signed up to use the card-dispute system |
| What does that sign-up allow? | **Entitlement** | The product or service owner | Retail Cards may log disputes and see their outcomes, for up to 200 users, standard support hours |
| Which named person or system can do what? | **Access right** | The owner of the system, under rules from risk and security | Agent 1043 may change a dispute outcome up to a set amount |

A subscription is a business decision; it changes a few times a year. An entitlement is a product decision; it changes when the offer or the contract changes. Access rights change every day as people join, move and leave.

**Least privilege, in plain words.** Give each person or system only the access needed for their current job, for as long as they need it, and no more. It is simple to say and hard to keep, because access is easy to add and nobody is asked to remove it.

**Joiners, movers and leavers.** Most access problems come from three moments:

- **Joiner:** a new person needs access. The risk is copying a colleague's access ("give her what Ali has"), which copies years of extras.
- **Mover:** a person changes role. The risk is that they get the new role's access and keep the old one. Movers are where access builds up the most.
- **Leaver:** a person leaves. The risk is accounts that stay active in systems not connected to the central directory, or shared and service accounts that nobody owns.

Tie each moment to a trigger from the HR record, not to a manager remembering to raise a ticket.

### 🟡 Going deeper

**Roles, not individual grants.** Instead of granting access item by item, group access into roles that match real jobs ("dispute agent", "dispute supervisor"). Then the request in lesson 7.1 becomes "give this person the dispute agent role", the recipe is simple, and reviews ask a clear question: "should this person still be a dispute agent?" Keep the number of roles small and named in business language. Hundreds of technical roles nobody understands defeat the purpose.

**Separating duties.** Some combinations are risky even if each part is fine: the same person able to create a payment and approve it, or change a dispute outcome and approve the refund. List the risky pairs for each important system with Nour's team, and check them when roles are granted, not only at review time.

**Reviews that people actually do.** An access review asks the owner of each grant to confirm it is still needed. Reviews fail when they are huge, generic and annual. Make them work by:

- **Reviewing by exception:** show the reviewer what changed or looks unusual (a mover, a high-risk role, an account unused for 90 days), not every line.
- **Reviewing at events:** trigger a review when a person moves, not only once a year.
- **Making removal the default** for unused high-risk access: if nobody confirms, it ends.
- **Keeping evidence:** who reviewed, what they decided, when, and what was removed.

The frequency of reviews for important systems is often set by the bank's policies and, through them, by what its supervisor expects. Ask Nour's team and the risk function what applies; do not guess.

**Entitlements and contracts.** Entitlements often live in a supplier contract or a licence agreement: how many users, which modules, what tier. Lina should be able to answer "what are we entitled to, and how much of it do we use?" for each major supplier. Lesson 10.2 covers the supplier side; here the point is that the entitlement is recorded where IT can see it, next to the subscription it serves.

**Machine access counts too.** Service accounts, API keys and the identities of automated jobs and AI agents are access rights. Each needs an owner, a reason and an end like any person's. For how this is done in cloud platforms, see [*Cloud & DevOps: Zero to Hero*, lesson 1.3 — Identity and access in the cloud: users, roles, policies and workload identity](../cloud/index.html#/1.3); for how access control fails inside applications, see [*Secure AI & Application Security*, lesson 3.3 — Authorisation: broken access control, IDOR and multi-tenancy](../secai/index.html#/3.3).

### 🔴 Expert view

**Make sign-ups visible and reversible.** When a business line stops using part of a product, that should end the subscription, which should reduce the entitlement at the next renewal and remove access rights that only existed for it. In most banks these three changes happen in different teams with no link between them, so nothing ends. One owner per product (lesson 2.1) who sees all three is the simplest fix.

**Design for the questions you will be asked.** The auditors' three questions at Najm Bank are the questions any auditor, supervisor or finance partner will ask. Design the register so each one is answered from records in minutes, not reconstructed in weeks. That is a records question as much as an access question; lesson 9.1 picks it up.

**Unused is a signal.** Access that has not been used for a long time is either not needed (remove it) or needed rarely (consider a time-limited grant on request instead). Licences that have not been used are money. Both come from the same usage data, which lesson 7.3 uses for cost.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Three-question register** | For one product: who has signed up, what each sign-up allows, who holds which access, with owners | When a product or platform has more than one business user, or before an audit |
| **Role catalogue** | A short list of named roles per system, in business language, with the access each includes | Before simplifying access requests and reviews |
| **Risky-pair list** | Combinations of access that one person must not hold together, agreed with risk | For any system that moves money or changes customer outcomes |
| **Joiner-mover-leaver triggers** | Rules linking HR events to access changes | To stop access building up when people move |
| **Exception-based review pack** | A review that shows only changes, high-risk roles and unused access | To replace long annual spreadsheets |
| **Identity governance or service management platform** | Tools that hold roles, run reviews and keep evidence; examples include identity governance tools and service management platforms | When manual reviews no longer scale; examples only, not endorsements |

## 🏛️ In practice at Najm Bank
Fictional and illustrative. After the audit, Nour and Reem built a three-question register for the card-dispute system:

| Subscription (signed up) | Owner | Entitlement (allowed) | Roles in use | Review |
|---|---|---|---|---|
| Retail Cards | Head of Retail Cards | Log disputes, see outcomes; up to 200 users | Dispute agent, dispute supervisor | Quarterly, by exception |
| SME Banking | Head of SME | Log disputes only; up to 40 users | Dispute agent | Quarterly, by exception |
| Fraud Operations | Head of Fraud Ops | Read-only view of all disputes | Fraud viewer | Half-yearly |

They cut 23 technical permissions down to five roles, agreed one risky pair with Nour (no one may hold both "dispute supervisor" and "refund approver"), and linked role removal to the HR mover and leaver events. Lina used the same register to reduce the licence tier at the next renewal from 400 to 280 named users (illustrative). Yousef's only request was that the role changes go through the change process (lesson 6.2), which they did.

## 🛠️ Exercises
**🟢 Separate the three questions.** For one system you know (or the Najm Bank card-dispute system), write down who has signed up, what each sign-up allows and how many people hold access, with the owner of each answer.
*Done when:* you have three separate answers, each with a named owner, and you have marked any answer you could not find.

<details><summary>Model answer and self-check</summary>

**Model answer.** A good answer looks like the Najm Bank register: business units with owners, what each may do and how much, and the number of people per role. Often one of the three is missing; finding that gap is the result. **Self-check.**
- Did you keep "signed up", "allowed" and "can technically do" apart?
- Did each answer have a different owner where it should?
- Did you mark unknowns rather than guess?

</details>

**🟡 Design the roles and risky pairs.** For the same system, propose at most six roles in business language and list at least one risky pair to check with risk.
*Done when:* each role has a name a business manager would understand and the access it includes, and the risky pair is written with the reason it is risky.

<details><summary>Model answer and self-check</summary>

**Model answer.** For example: agent, supervisor, viewer, administrator, auditor (read-only). Risky pair: "can change an outcome" with "can approve the refund", because one person could then pay themselves or a friend without a second check. **Self-check.**
- Could a business manager review these roles without IT help?
- Did you avoid one role per person?
- Did you name who must agree the risky pair?

</details>

**🔴 Replace the annual review.** Write a half-page design for an exception-based review of the system: what is shown, to whom, when it is triggered, what happens if nobody responds, and what evidence is kept.
*Done when:* the design covers all five points and names the function you would ask about the required review frequency.

<details><summary>Model answer and self-check</summary>

**Model answer.** Shown: movers in the last quarter, high-risk roles, accounts unused for 90 days. To: the business owner of each subscription. Triggered: quarterly and on each mover event. No response: unused high-risk access is removed after a reminder. Evidence: reviewer, decision, date, items removed, kept with the system's records. Frequency: confirmed with the risk function. **Self-check.**
- Is the review small enough that someone will read it?
- Does silence lead to removal for high-risk access?
- Did you avoid stating a regulatory frequency you have not checked?

</details>

## ⚠️ Mistakes and traps
- **One word for three things.** Treating "access" as one question leaves sign-ups, entitlements and grants unowned. Keep the three apart, each with its owner.
- **Copying a colleague's access.** "Same as Ali" copies years of extras. Grant by role.
- **Forgetting movers.** Leavers get attention; movers quietly collect access. Trigger changes from HR events.
- **Rubber-stamp reviews.** Huge annual spreadsheets get approved unread. Review by exception, at events, with removal as the default for unused high-risk access.
- **Ignoring machine identities.** Service accounts and agent identities need owners and ends too.
- **Paying for unused entitlements.** Licences nobody uses are money. Check usage before renewal.

## 🧾 Recap
- **Subscription** (who signed up), **entitlement** (what it allows) and **access right** (who can technically do what) answer three different questions with three different owners.
- **Least privilege**: only the access needed for the current job, for as long as it is needed.
- Most problems come at **joiner, mover and leaver** moments; tie them to HR events.
- Use a small set of **business-named roles** and a list of **risky pairs**.
- Make reviews **exception-based and event-driven**, with evidence; ask risk about required frequency.
- Unused access is a risk; unused licences are a cost. The same usage data shows both.

## ✍️ Check yourself
**1. The auditors ask Nour, "What are SME Banking users allowed to do in the card-dispute system?" Which record answers this?**

- A. The subscription, which shows that SME Banking signed up to use the system.
- B. The entitlement, which shows what SME Banking's sign-up allows and how much.
- C. The access rights, which list each SME user and their technical permissions.
- D. The supplier invoice, which shows the number of licences the bank paid for.

<details><summary>Answer</summary>

**B.** What a sign-up allows is the entitlement. A answers who signed up, not what they may do; C shows what individuals can technically do, which may differ from what is allowed; D shows cost, not permitted use. See "Three questions, three owners".

</details>

**2. A dispute agent is promoted to supervisor in the same team. Six months later she still holds both roles. Which moment failed?**

- A. The joiner moment, because her first access should have been smaller.
- B. The leaver moment, because her old role should have been formally closed.
- C. The review moment, because annual reviews are the only place to catch this.
- D. The mover moment, because her old access was not removed when she changed role.

<details><summary>Answer</summary>

**D.** Changing role is a mover event, and the risk is keeping the old access. A and B name the wrong moment, and C treats the annual review as the only control when the change should have been triggered by the move itself. See "Joiners, movers and leavers".

</details>

**3. Managers at Najm Bank approve a 3,000-line access spreadsheet each year in minutes. What is the best improvement?**

- A. Show reviewers only changes, high-risk roles and unused accounts, triggered by events too.
- B. Send the spreadsheet twice a year, so each manager has more chances to spot problems.
- C. Ask IT security to review all 3,000 lines instead, since they understand the systems.
- D. Require managers to sign a statement that they read every line before they approve.

<details><summary>Answer</summary>

**A.** An exception-based, event-driven review is small enough to be read and focuses on what is risky. B doubles a review nobody reads, C moves the decision away from the people who know whether access is needed, and D adds paperwork without making the review readable. See "Reviews that people actually do".

</details>

**4. Which pair of access rights should Nour's team most want to prevent one person holding together?**

- A. Viewing dispute outcomes and logging a new dispute for a customer.
- B. Reading the dispute report and exporting it to a spreadsheet for analysis.
- C. Changing a dispute outcome and approving the resulting refund payment.
- D. Logging a dispute and adding a note to an existing dispute record.

<details><summary>Answer</summary>

**C.** Changing an outcome and approving the refund lets one person move money without a second check. The other pairs carry less risk of a single person causing a loss on their own. See "Separating duties".

</details>

**5. The bank pays for 400 named-user licences, but about 250 people logged in last quarter. What should Lina do before renewal?**

- A. Renew at 400, since unused licences give a buffer for future growth.
- B. Check usage with the owners and adjust the entitlement to real need.
- C. Remove all users who did not log in, then renew at the same tier.
- D. Ask the supplier which tier is usual for a bank of Najm Bank's size.

<details><summary>Answer</summary>

**B.** Usage data, checked with the owners of each sign-up, shows the real need, and the entitlement should match it. A pays for unused capacity, C removes access without checking and then wastes the saving, and D replaces your own evidence with the seller's view. See "Entitlements and contracts" and "Unused is a signal".

</details>

## 📚 References
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 1.3 — Identity and access in the cloud: users, roles, policies and workload identity](../cloud/index.html#/1.3).
- Library course: [*Secure AI & Application Security*, lesson 3.3 — Authorisation: broken access control, IDOR and multi-tenancy](../secai/index.html#/3.3).

---

# 7.3 — Usage, showback and chargeback
*Level: 🟡 Intermediate* · *Prerequisites: 7.2* · *Step: Serve*

**After this you can** design a monthly usage-and-cost report for one shared platform, choose between showback and chargeback for it with reasons, and list the questions to take to finance before any charge is made. *Study time: reading about 15 min, hands-on about 95 min (estimate).*

## ⚡ In 60 seconds
- **Usage** is how much of a service someone consumed: environments, storage, licences, API calls, compute hours.
- **Showback** shows each business line or product what its usage cost, without moving money. **Chargeback** actually moves the cost into their budget through the bank's internal accounting.
- The rule that matters most: **show before you charge; nobody accepts a bill they cannot read or influence.**
- A unit of usage is only useful if the consumer can **understand it and change it** ("test environments × days"), not if it is a technical unit they cannot control.
- Decision cue: if a business line cannot name one decision it would make differently after seeing its usage, the report is not ready.
- Biggest trap: allocating shared costs by a formula nobody can explain, then spending more time arguing about the formula than reducing the cost.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers in this lesson are illustrative figures, not benchmarks.

Each year Tariq spread the cost of the Technology division across the business lines by headcount. Retail, with the most staff, paid the most. Corporate Banking, with fewer staff but three heavy data platforms, paid little. Nobody believed the numbers, and nobody changed behaviour, because the charge had no link to anything they did.

Then the board asked Omar why cloud and platform costs had grown faster than the bank's revenue. Omar asked Tariq which products drove the growth. Tariq could not say. Sami could see which environments existed, but not which product or business line each one served. After lesson 7.1, the new environments carried a product, an owner and a cost centre. Most of the older ones did not.

The business lines wanted to know why their IT charge went up. IT wanted the business lines to use less. Neither side had the facts to talk about it. This lesson builds those facts first, and only then asks whether money should move.

## 📐 How it works

### 🟢 The essentials

**Three steps, in order.**

1. **Measure usage** with a link to who used it: each environment, licence, data store or account tagged with a product, an owner and a cost centre (the records from lessons 7.1 and 7.2).
2. **Show the cost** of that usage to the people who drive it (**showback**), every month, in units they recognise.
3. **Charge** it to their budgets (**chargeback**) only if the bank decides that moving money will improve decisions, and only after finance agrees the method.

Skipping step 1 makes steps 2 and 3 arguments. Skipping step 2 makes step 3 a surprise.

**Direct and shared cost.** Some cost belongs clearly to one consumer: a test environment tagged to Cards & Payments. Some is shared: the network, the security operations centre, the service desk, the platform team itself. Direct cost is easy to show. Shared cost must be **allocated**, meaning split by a rule (by usage, by number of transactions, by number of users). An even split will do only as a stopgap; lesson 10.1 explains why drivers that move with use are better. The rule should be simple enough that a business line can check its own share and see how to change it.

**Choose units people can act on.** "Compute core-hours" is a unit the platform understands; Reem cannot act on it. "Test environments kept open per month" or "cost per thousand card transactions processed" are units she can change. Pick one or two units per service that the consumer can both read and influence. Lesson 10.1 goes deeper on unit costs.

### 🟡 Going deeper

**Showback or chargeback?** Both are legitimate. The choice depends on the bank's accounting policy, its budgeting culture and what behaviour it wants to change.

| Question | Points to showback | Points to chargeback |
|---|---|---|
| Is the usage data complete and trusted? | Not yet | Yes, for this service |
| Can consumers change their usage? | Only a little | Yes, clearly |
| Does finance's internal accounting support moving the cost? | Not set up, or costly to run | Yes, with an agreed method |
| Is the aim awareness or accountability? | Awareness first | Budget accountability |
| Will the argument about the method cost more than the saving? | Likely | Unlikely |

The FinOps Foundation, the body that publishes the FinOps Framework for cloud financial management, is reported (from search summaries; the page was not opened for this lesson) to say on its invoicing and chargeback capability page that showback is needed in every FinOps practice while chargeback depends on an organisation's accounting policies. That fits the order in this lesson: show always, charge when the accounting supports it. For the cloud engineering side of allocating cost, see [*Cloud & DevOps: Zero to Hero*, lesson 6.2 — FinOps: understanding, allocating and cutting cloud cost](../cloud/index.html#/6.2).

**What to ask finance.** Moving money between budgets is an accounting decision, not an IT one. Questions to take to Tariq and the finance function:

- Does our internal accounting allow costs to be recharged between business lines, and how?
- Is there a policy on how shared costs are allocated, and who approves changes to it?
- Do any recharges cross legal entities or countries, and does that raise tax or transfer-pricing questions?
- How are capital and operating costs treated in a recharge?
- What happens to disputes, and who settles them?

Do not answer these yourself. Bring the usage data and the proposed method, and let finance decide.

**A good monthly report.** One page per business line or product:

- the top five cost lines, in units they recognise, with this month, last month and the trend;
- what changed and why (new environments, a licence renewal, a spike);
- untagged or unexplained cost, shown honestly as its own line;
- two or three suggested actions with an estimated saving (close idle environments, reduce a licence tier);
- who to talk to.

The untagged line matters. Hiding it inside an allocation makes the report look complete and teaches nobody to fix the tagging.

### 🔴 Expert view

**Chargeback changes behaviour, not always for the better.** When a business line pays directly, it may reduce waste. It may also avoid shared services, buy its own tools outside IT, or argue for months about the formula. Watch for these effects after any change, and keep shared, protective services (security monitoring, backup) out of any charge that might push people to skip them, or charge them as a fixed, non-optional amount.

**Showback without action is decoration.** A report nobody acts on costs time and earns nothing. Each month, ask each business line for one decision: keep, reduce, or explain. Track those decisions. If three months pass with none, change the units or the audience before adding more detail.

**Consumption and access share their data.** The same tags and records that tell you who holds which access (lesson 7.2) tell you who consumes what. Build them once. An environment, licence or account without an owner is a risk in lesson 7.2 and an unallocated cost here.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Tagging rule** | The required tags (product, owner, cost centre, end date) for every resource or licence, enforced at creation | Before any showback; it is the basis of all the numbers |
| **Monthly showback page** | One page per business line: top cost lines in usable units, trend, changes, untagged cost, suggested actions | Every month, once tagging covers most cost |
| **Allocation rule sheet** | For each shared cost, the split rule, its owner and its review date | When shared cost is a large part of the total |
| **Showback-or-chargeback table** | The five questions that point one way or the other, per service | Before proposing any chargeback to finance |
| **Finance question list** | The questions on recharging, allocation policy, entities, capital and operating cost, disputes | Before any money moves between budgets |
| **Cloud cost tool or IT financial management platform** | Tools that collect usage, apply tags and produce allocation reports; examples include cloud providers' own cost tools and IT financial management platforms | When spreadsheets can no longer keep up; examples only, not endorsements |

## 🏛️ In practice at Najm Bank
Fictional and illustrative. Tariq and Sami started with the shared platform. They set a tagging rule (product, owner, cost centre, end date) enforced by the platform template from lesson 7.1, and spent a month tagging older environments. About 80 percent of platform cost was tagged after that month; the rest stayed on the report as "untagged" (illustrative).

Their first monthly page for Cards & Payments showed:

| Cost line (unit) | Usage last month | Usage this month | Cost last month | Cost this month | Note |
|---|---|---|---|---|---|
| Test environments (environment-days) | 380 | 520 | 19.0 | 26.0 | 11 environments past their end date |
| Card analytics data store (TB-months) | 14 | 15 | 8.4 | 9.0 | Steady |
| Developer tool licences (named users) | 60 | 60 | 12.0 | 12.0 | 18 unused for 90 days |
| Share of platform team (temporary split) | — | — | 20.0 | 20.0 | Split evenly by number of products as a stopgap, until a usage driver is agreed (lesson 10.1) |
| Untagged cost attributed by owner guess | — | — | — | 4.0 | To be confirmed with the owners |
| **Total** | | | **59.4** | **71.0** | Up mainly because of open test environments |

Costs are in thousands of the bank's currency per month (illustrative). Below the table the page listed two suggested actions and a contact:

- **Close the 11 expired environments** (owner: Reem). Estimated saving: about 16 thousand a month (11 environments × 30 days × 0.05 thousand per environment-day).
- **Release the 18 unused licences at renewal** (owner: Reem, with Lina for the contract). Estimated saving: about 3.6 thousand a month (18 × 0.2 thousand per named user).
- **Contact:** Tariq for the figures and the allocation rule; Sami for tags and environments.

Reem closed nine of the eleven expired environments in a week and released the unused licences at renewal. Tariq proposed keeping showback for six months, then asking finance whether test environments, and only those, should move to chargeback. Omar agreed and told the board that platform cost was now visible by product, with the first reductions underway.

## 🛠️ Exercises
**🟢 Pick usable units.** For one shared service you know (or Najm Bank's platform), list its three largest cost lines and propose a unit for each that a business line could read and change.
*Done when:* each cost line has a unit, and for each unit you have written one action a consumer could take to reduce it.

<details><summary>Model answer and self-check</summary>

**Model answer.** For example: environments × days (close idle ones), data store TB-months (archive old data), named-user licences (release unused seats). **Self-check.**
- Could a business manager understand each unit without IT help?
- Did each unit come with a real action?
- Did you avoid purely technical units such as core-hours?

</details>

**🟡 Draft the monthly page.** Using real or illustrative data, draft a one-page showback report for one business line with the five elements from "A good monthly report".
*Done when:* the page has top cost lines with trend, what changed, an untagged line, at least two actions with estimated savings, and a contact.

<details><summary>Model answer and self-check</summary>

**Model answer.** See the Cards & Payments page above: usage and cost side by side with last month, a note on what changed, the untagged line, two actions with owners and estimated savings, and a contact. A good page is short, shows the untagged cost openly, and ends with actions. **Self-check.**
- Is the untagged cost visible, not hidden in an allocation?
- Does each action name an owner?
- Is every number labelled as real or illustrative?

</details>

**🔴 Make the case to finance.** For one service, fill in the showback-or-chargeback table, write a recommendation, and list the questions you will ask finance before any charge.
*Done when:* all five table questions are answered with evidence, the recommendation states showback or chargeback and why, and the question list covers recharging, allocation policy, entities, capital and operating cost, and disputes.

<details><summary>Model answer and self-check</summary>

**Model answer.** For example: "Test environments: data trusted (95 percent tagged), consumers can change usage, finance can recharge between business lines within one entity, aim is accountability, method dispute unlikely. Recommend chargeback after six months of showback, subject to finance agreeing the method." **Self-check.**
- Did you avoid stating an accounting or tax conclusion yourself?
- Did you consider behaviour effects such as avoiding protective shared services?
- Did you show before you charge?

</details>

## ⚠️ Mistakes and traps
- **Charging before showing.** A bill with no history becomes a dispute. Show usage for several months first.
- **Units nobody can act on.** Technical units produce reports nobody reads. Use units the consumer can change.
- **Hiding untagged cost.** Spreading it silently makes the report look complete and stops anyone fixing tags. Show it as its own line.
- **Formulas nobody can explain.** Complex allocation invites months of argument. Prefer a simple rule each business line can check.
- **Charging for protective services in a way that discourages them.** People will skip backup or monitoring to save money. Make those fixed and non-optional.
- **Deciding accounting questions in IT.** Recharging rules belong to finance. Bring data and questions, not conclusions.

## 🧾 Recap
- **Usage** with an owner is the basis of everything; tag at creation.
- **Showback** shows the cost of usage without moving money; **chargeback** moves it into budgets.
- Show before you charge, in **units people can read and change**.
- Allocate shared cost by a **simple, checkable rule** that moves with use (an even split only as a stopgap), and show untagged cost openly.
- The choice between showback and chargeback depends on data quality, the consumer's control, the bank's accounting and the behaviour you want; **finance decides** on moving money.
- The same records serve access (7.2) and cost (7.3): build them once.

## ✍️ Check yourself
**1. What is the difference between showback and chargeback?**

- A. Showback covers only cloud costs, while chargeback covers all of IT's costs.
- B. Showback is calculated monthly, while chargeback is calculated once each year.
- C. Showback uses estimates, while chargeback uses only exact invoice amounts.
- D. Showback shows the cost of usage, while chargeback moves it into budgets.

<details><summary>Answer</summary>

**D.** Showback makes cost visible without moving money; chargeback moves it into the consumer's budget through internal accounting. A, B and C describe differences of scope, frequency or precision that are not what separates the two. See "Three steps, in order".

</details>

**2. Tariq wants to start chargeback for the platform next month. About half the platform cost is not tagged to any product. What should he do first?**

- A. Charge all untagged cost to IT, so the business lines see only clean figures.
- B. Improve tagging and run showback for some months before proposing a charge.
- C. Allocate untagged cost by headcount, since that was the previous method used.
- D. Start chargeback now, since charging will push teams to fix their own tagging.

<details><summary>Answer</summary>

**B.** Untrusted data makes any charge an argument; tag first and show before charging. A and C hide the untagged cost inside an allocation, and D charges before the data or the consumers are ready. See "Showback or chargeback?" and "Charging before showing".

</details>

**3. Which unit is most useful in a showback report for Reem's Cards & Payments team?**

- A. Total compute core-hours used across all the platform's clusters.
- B. The percentage of the platform's yearly budget that has been spent so far.
- C. Test environments kept open per month, multiplied by the number of days.
- D. The number of tickets the service desk handled for the whole bank.

<details><summary>Answer</summary>

**C.** Reem can read it and change it by closing idle environments. A is a technical unit she cannot act on, B is a budget figure with no link to her usage, and D is not about her product. See "Choose units people can act on".

</details>

**4. After chargeback starts for security monitoring, two business lines ask to switch it off for their test systems to save money. What does this show?**

- A. Charging for a protective service can push people to skip it; charge it as fixed.
- B. The business lines are right, because test systems never need security monitoring.
- C. Chargeback is working, because the business lines are now looking for savings.
- D. Security monitoring should be moved under each business line's own budget.

<details><summary>Answer</summary>

**A.** Chargeback can change behaviour in harmful ways; protective services should be fixed and non-optional. B is a security judgement the lesson does not support, C mistakes harmful saving for a good result, and D makes skipping even easier. See "Chargeback changes behaviour, not always for the better".

</details>

**5. Tariq's proposal would recharge platform cost to a business line in another legal entity of the group. What should IT do?**

- A. Apply the same rule as for other business lines, since the cost is the same.
- B. Leave that entity out of the report, since recharges across entities are not allowed.
- C. Bring the data and method to finance and ask how cross-entity recharges are handled.
- D. Ask the platform team to decide the rule, since they understand the costs best.

<details><summary>Answer</summary>

**C.** Recharges across entities can raise accounting and tax questions that finance must answer. A and D make an accounting decision in IT, and B states a rule the lesson does not claim. See "What to ask finance".

</details>

## 📚 References
- FinOps Foundation, FinOps Framework capability "Invoicing & Chargeback" (reported from search summaries; page not opened for this lesson): https://www.finops.org/framework/capabilities/invoicing-chargeback/
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 6.2 — FinOps: understanding, allocating and cutting cloud cost](../cloud/index.html#/6.2).
