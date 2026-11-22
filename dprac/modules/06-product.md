# Module 6 — Product management in a team

*Qafila has reached Growth: about forty people in four teams, 2,000 merchants and about 25,000 deliveries a day, with several deploys to production a day. The product now includes a support desk and product analytics, and order tracking has a reliability target of 99.9% a month. At twelve people, Aisha could keep one ordered backlog and talk to every engineer daily. At forty, four teams pull in different directions, sales conversations turn into promised dates, and nobody can say whether last quarter's features changed anything for merchants. This module covers three everyday practices that keep a growing product pointed at the right problems: a roadmap and a way of prioritising that people trust, requirements that say clearly what "done" looks like, and measurement that shows whether the work made a difference. Yasmin, a graduate engineer who joins Qafila at this stage, sees each practice from the inside. Each lesson leaves you with an artefact: a now/next/later roadmap with a scored shortlist, user stories with acceptance criteria, and a measurement plan with an experiment brief.*

> **Steps:** Discover, Design — choose the problems worth solving next, describe the solution precisely enough to build and check, and measure whether it changed what customers do.

---

# 6.1 — Roadmaps and prioritisation
*Level: 🟡 Intermediate* · *Prerequisites: 1.3, 5.2* · *Step: Discover, Design*

**After this you can** explain what a roadmap is for, turn a list of features with dates into a now/next/later roadmap of problems and outcomes, score a shortlist with RICE and say what the score misses, and use cost of delay to order urgent work. *Study time: reading about 15 min, hands-on about 85 min (estimate).*

## ⚡ In 60 seconds
- A **roadmap** is a short, shared statement of which problems the teams will work on now, next and later, and why. It is a communication tool, not a release schedule.
- Scoring methods such as **RICE** and **cost of delay** make trade-offs visible and arguable. They support a decision; they do not make it.
- The rule that matters most: **a roadmap is a promise about problems, not about features.**
- Decision cue: before a date goes on a roadmap, ask "is there a real external deadline, and what happens if we miss it?"
- Biggest trap: a long list of features with months that everyone outside the team reads as promises.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

Qafila now has four teams: **Merchant** (merchant app and scheduling), **Courier** (courier app), **Payments** (billing and the payment provider) and **Support Tools** (the new support desk and the admin web page). In her second week, Yasmin, a graduate engineer on the Courier team, asks at planning: "Why are we building a new courier sign-up flow this month?" Nobody can answer beyond "it's on the roadmap".

The roadmap is a spreadsheet of forty-one features, each with a month, added by whoever asked: Maha after merchant visits, sales after meetings (including "bulk order upload for the pharmacy chain, by March", which Maha agreed to at a dinner), Faisal for database work. Each team picks rows it likes.

Aisha, now leading product across the four teams, sees two problems: the roadmap lists solutions, not problems, so nobody can check whether a row still makes sense; and with no shared way to choose, the loudest voice wins.

## 📐 How it works

### 🟢 The essentials

**What a roadmap is for.** A roadmap sits between long-term direction and the day-to-day backlog:

| Layer | Question it answers | Time span | Owner at Qafila |
|---|---|---|---|
| **Vision** | Why the product exists and for whom | Years | Maha |
| **Goals** | The few outcomes that matter this year | A year | Maha with the leads |
| **Roadmap** | Which problems we tackle now, next and later, and why | One to three quarters | Aisha with each team |
| **Backlog** | The ordered list of specific work items (lesson 5.2) | Weeks | Each team's product manager |

An **outcome** is a change in what customers or colleagues do that you can observe and count; an **output** is something the team ships. "Merchants schedule repeat orders without phoning us" is an outcome; "recurring-delivery screen" is an output. A good roadmap shows problems and outcomes and leaves the team room to find the best solution.

**Three common formats.**

| Format | What it shows | Good for | Risk |
|---|---|---|---|
| **Timeline** | Features against dates | Work with real fixed dates | Every row reads as a promise |
| **Now / next / later** | Problems or outcomes in three columns by how soon and how certain | Most product teams | People still ask "when is next?" |
| **Theme or goal-based** | Outcomes grouped by yearly goal, no dates | Talking to leadership | Too vague for a team to plan from |

The now/next/later format is widely credited to Janna Bastow, a co-founder of the roadmapping company ProdPad, as an alternative to timeline roadmaps (as reported by ProdPad). Its idea: **certainty falls with distance**. "Now" is understood; "next" is shaped but not started; "later" is a problem believed to matter but not explored.

**The questions behind any prioritisation.** Ask of every item: **value** (what changes, for how many?), **urgency** (what do we lose each week we wait?), **confidence** (what evidence?), **effort** (how much team time?) and **obligation or risk** (is it required, or does it reduce a serious risk?).

### 🟡 Going deeper

**RICE scoring.** RICE was developed at Intercom, a customer-messaging software company, and described by Sean McBride in a post on Intercom's blog (2018):

> **RICE score = Reach × Impact × Confidence ÷ Effort**

- **Reach:** people or accounts affected in a set period, for example merchants per quarter.
- **Impact:** effect on each, on a small fixed scale; Intercom's version used 3 (massive), 2 (high), 1 (medium), 0.5 (low) and 0.25 (minimal).
- **Confidence:** how sure you are of the other numbers, as a percentage.
- **Effort:** total work in person-months (one person-month is one person's work for a month).

RICE makes reach and confidence explicit: a feature for one loud customer reaches one customer, and an idea with no evidence scores lower. Its weakness is false precision: four multiplied estimates look more exact than they are. Use scores to sort a list into "clearly high", "clearly low" and "needs discussion".

**Cost of delay.** **Cost of delay** asks how much value you lose for each week an item is not done. Don Reinertsen's book *The Principles of Product Development Flow* (2009) is reported to put it at the centre of an economic view of product work. When items differ in urgency and size, divide cost of delay by duration and do the highest first; this is often called **CD3** (cost of delay divided by duration). A small, urgent item usually jumps ahead of a large one: finishing it stops the loss sooner and delays the large item only a little. CD3 decides order, not worth.

**MoSCoW** (Must, Should, Could, Won't have this time), from the DSDM agile approach now maintained by the Agile Business Consortium, suits one **time box** (a fixed period, such as a two-week iteration); used long term, everything drifts into "must".

**Capacity before items.** Before ranking features, agree roughly how each team's time is split (illustrative):

| Kind of work | Share | Example at Qafila |
|---|---|---|
| Roadmap outcomes | About 60% | Fewer "where is my delivery?" contacts |
| Reliability and technical health | About 20% | Order tracking meets 99.9% a month; faster migrations |
| Support, interrupts and obligations | About 20% | On-call; the payment provider's announced changes |

Adjust it from what happened last quarter (lesson 5.3). It stops reliability work competing with features item by item, a contest it usually loses.

### 🔴 Expert view

**Scores are conversation aids.** The useful moment is when two people give one item very different numbers: "You said reach 2,000, I said 200: what do you know?" Write the reasoning next to the number.

**Commit to dates rarely, and on purpose.** A date belongs on a roadmap when there is a real external reason. Make it a **fixed date with flexible scope**: "by 1 March the pharmacy chain can upload orders from a spreadsheet; more comes later." Everything else gets a forecast with a range (lesson 5.2). Work that scores oddly in RICE (internal tools, security fixes, legal duties) is funded through the capacity split.

**Say no in writing.** A **not-doing list** records what you decided not to do this period, and why. When a founder's request jumps the queue, say openly what it displaces.

**The memorable rule.** A roadmap is a promise about problems, not about features.

For the manager's view of business cases and cost of delay, see [*Running IT as a Business*, lesson 3.2 — Prioritising and funding work: business cases, cost of delay and funding products not projects](../itbiz/index.html#/3.2).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Now/next/later roadmap** | Three columns of problems or outcomes, each with a measure | When a feature-and-date list is being read as promises |
| **RICE sheet** | Reach, impact, confidence, effort, score and a reasoning column | To sort a shortlist of customer-facing items |
| **Capacity split** | Agreed shares of team time for roadmap, reliability and interrupts | At the start of each quarter, before ranking |
| **Not-doing list** | Items deliberately not done, with reason and review date | After every prioritisation session |

## 🏛️ In practice at Qafila
Aisha ran a half-day session with the four team leads, Salma (support) and Hamad (data). Illustrative and fictional. They agreed the capacity split above, merged the forty-one rows into problems, and scored the customer-facing ones:

> **RICE shortlist (Growth, quarter 1).** Reach is merchants affected per quarter, out of 2,000.
>
> | Problem | Reach | Impact | Confidence | Effort | RICE | Reasoning |
> |---|---|---|---|---|---|---|
> | Merchants cannot see how far a delivery has got without phoning support (order tracking shows status only, not where the courier is) | 2,000 | 2 | 50% | 3 | 667 | Top support contact reason; unsure a tracking link fixes it |
> | Merchants rebuild monthly invoices by hand | 1,200 | 0.5 | 100% | 0.5 | 1,200 | Cheap; known pain |
> | Bakeries need time windows on any day, not just tomorrow | 900 | 1 | 80% | 2 | 360 | Extends Traction's scheduling work |
> | The pharmacy chain cannot upload orders in bulk | 60 | 3 | 80% | 2 | 72 | One chain, about 60 branches (3% of merchants); date promised |
>
> Funded from the capacity split, not scored: support desk search speed, faster database migrations, the payment provider's change to its webhook (the message its system sends to Qafila's when a payment succeeds or fails).

The cheap invoice fix scored highest; they did it at once. The pharmacy chain scored lowest but carried Maha's promise, so Aisha asked the cost-of-delay question: Bilal said the chain would pay only once bulk upload worked and might leave after March. They kept it with a fixed date and flexible scope, and Maha agreed to route future promises through Aisha.

> **Qafila roadmap (Growth, quarter 1)**
>
> | Now | Next | Later |
> |---|---|---|
> | Merchants see delivery progress without phoning (measure: "where is my delivery?" contacts per 1,000 deliveries) | Bakeries schedule time windows on any day (measure: share of bakery orders scheduled ahead) | Couriers plan their own shifts (unexplored) |
> | Pharmacy chain uploads orders in bulk by 1 March, spreadsheet only (measure: share of the chain's orders uploaded in bulk) | Courier sign-up in one visit instead of three (measure: days from application to first delivery) | Multi-shop merchants manage one account |
> | Merchants stop rebuilding monthly invoices by hand (measure: invoice-related support contacts) | | |
>
> **Not doing this quarter:** admin dark mode (one request); custom map styles (no evidence). Review in April.

Yasmin's question now had an answer: courier sign-up sat in "next", with a problem and a measure.

## 🛠️ Exercises
**🟢 From features and dates to now/next/later.** Rewrite this list (or one from a product you use) as a now/next/later roadmap of problems or outcomes, each with one measure: "Courier earnings screen (Feb); new logo (Feb); merchant chat with courier (Mar); multi-shop accounts (Apr); faster admin search (Apr); loyalty points for end customers (Jun)."
*Done when:* every item is a problem or outcome with a measure, no item has a month without a stated external reason, and at least one item is on a not-doing list with a reason.

<details><summary>Model answer and self-check</summary>

**Model answer.** Now: couriers cannot check earnings without asking the office (earnings questions per week); support agents wait for order search (median search time). Next: merchants and couriers cannot reach each other when an address is unclear (failed first attempts); multi-shop merchants juggle logins (their weekly active use). Later: end customers have no reason to prefer Qafila-delivered shops (unexplored). Not doing: new logo, no evidence it changes behaviour.

**Self-check.**
- Could someone check each measure from a record that exists or could exist?
- Did "later" stay a problem rather than a feature?
- Did you resist giving months to items with no external deadline?

</details>

**🟡 Score a shortlist and find what the score misses.** Score with RICE, choosing impact and confidence yourself, with one line of reasoning per item. Reach is in thousands of deliveries affected per quarter, out of about 2,250 (illustrative): (a) couriers see the shop's phone number in the app (reach 200, effort 0.25); (b) merchants get a text when a delivery is late (reach 300, effort 1); (c) a rebuild of the courier app in a new framework (effort 6); (d) end customers rate their courier (reach 2,250, effort 2). Then write three sentences on what the scores miss.
*Done when:* each scored item has four inputs, a score and a reason; at least one item is marked "does not fit RICE; fund another way"; and your sentences name at least one cost, risk or urgency the scores ignore.

<details><summary>Model answer and self-check</summary>

**Model answer.** Deliveries work as one reach unit because every item touches deliveries, whether it serves couriers, merchants or end customers. (a) 200 × 0.5 × 80% ÷ 0.25 = 320: cheap, clear evidence from support. (b) 300 × 1 × 50% ÷ 1 = 150: unsure merchants want more texts. (c) Does not fit: no direct customer reach; argue it from the capacity split with the risk it removes (slow releases, crashes on older phones). (d) 2,250 × 0.5 × 50% ÷ 2 ≈ 281: broad but unproven. Missed: (b) raises text costs per delivery; (d) raises fairness and privacy questions for couriers; no score shows a deadline.

**Self-check.**
- Did you use the same reach unit for every scored item, and could you say why it fits?
- Did you lower confidence where you had no evidence?
- Did you avoid scoring a technical rebuild as a customer feature?

</details>

**🔴 Order urgent work with cost of delay, then say no.** Three items compete for the Payments team. Cost of delay is in "value units", a made-up common scale for comparing items. A: the provider's webhook change; payments start failing after 2 weeks (cost of delay 10 units a week, duration 2 weeks). B: a refund button for support (4 a week, 1 week). C: a billing plan for large merchants (20 a week, 8 weeks). Order them with CD3 and draft a message to the sales lead who wanted C first.
*Done when:* you show CD3 per item and your order, and your message (five sentences or fewer) gives the reason, a forecast with a range for C, and what would change the decision.

<details><summary>Model answer and self-check</summary>

**Model answer.** CD3: A = 5, B = 4, C = 2.5, so A, B, C. With C first, A would wait 8 weeks and payments would fail from week 2. Message: "We start the large-merchant billing plan in three weeks, after the provider change that keeps payments working and a one-week refund fix. Starting it first would leave payments failing for weeks. Our forecast is about eleven weeks from now, give or take two. If a signed customer needs it sooner, tell me this week and we will look at a smaller first version."

**Self-check.**
- Did you treat A's deadline as a real risk, not just a number?
- Does your message give a range rather than a promise?
- Did you offer a way to change the decision?

</details>

## ⚠️ Mistakes and traps
- **Features with months, read as promises.** Put problems and outcomes on the roadmap; keep dates for real deadlines, with flexible scope.
- **Treating a score as the answer.** Use scores to sort and expose disagreement; then decide and write down why.
- **One formula for every kind of work.** Agree a capacity split first; rank customer items within the rest.
- **Silent "no".** Keep a not-doing list with reasons and review it each quarter.

## 🧾 Recap
- A roadmap shows which problems the teams tackle now, next and later, and why; it is not a release schedule.
- RICE makes reach and confidence visible; cost of delay and CD3 order work when urgency differs. Both support judgement.
- Agree a capacity split before ranking, so reliability and obligations are not traded away item by item.
- Rule: a roadmap is a promise about problems, not about features.

## ✍️ Check yourself
**1. Yasmin asks why her team is building a new courier sign-up flow, and the only answer is "it's on the roadmap". What is the most useful change to the roadmap?**

- A. Add the month each feature will ship.
- B. Add more detail to each feature row.
- C. Rewrite each row as a problem with a measure.
- D. Let each team rank its own rows.

<details><summary>Answer</summary>

**C.** A roadmap of problems and outcomes carries its own "why". A adds dates that become promises, B adds detail without the reason, and D gives each team its own list. See "What a roadmap is for".

</details>

**2. An item has reach 1,000 merchants per quarter, impact 2, confidence 50% and effort 2 person-months. What is its RICE score?**

- A. 500
- B. 1,000
- C. 2,000
- D. 250

<details><summary>Answer</summary>

**A.** RICE is reach × impact × confidence ÷ effort: 1,000 × 2 × 0.5 ÷ 2 = 500. B drops effort (dropping confidence instead also gives 1,000), C drops both confidence and effort (reach × impact only), and D divides by effort twice. See "RICE scoring".

</details>

**3. The pharmacy chain's bulk upload scores lowest in RICE, but Maha promised it for March and the chain may leave if it is late. What should Aisha do?**

- A. Drop it, since its score is the lowest.
- B. Put it first with full scope, since the founder promised.
- C. Raise its impact score so the numbers match.
- D. Keep the date, cut the scope, justify it by cost of delay.

<details><summary>Answer</summary>

**D.** RICE does not see urgency; cost of delay does. A fixed date with flexible scope meets the deadline without taking over the quarter. A ignores the deadline, B accepts the promise without trade-offs, and C bends the numbers. See "Commit to dates rarely, and on purpose".

</details>

**4. Faisal complains that database work never makes the roadmap because it always scores lower than features. What is the best fix?**

- A. Give technical items an impact of 3, so they compete fairly with customer features.
- B. Agree a capacity split per team that reserves a share for reliability and health work.
- C. Move all technical work to a separate platform team so feature teams stay focused.
- D. Wait for the next outage, since an incident will make the case better than any score.

<details><summary>Answer</summary>

**B.** Reliability work rarely wins item-by-item contests with features, so fund it from an agreed share. A games the score, C is a structural change for a later stage (Module 8), and D accepts customer harm. See "Capacity before items".

</details>

**5. Four items compete for one team. Which should usually go first under CD3?**

- A. Cost of delay 20 a week, duration 8 weeks.
- B. Cost of delay 6 a week, duration 6 weeks.
- C. Cost of delay 9 a week, duration 1 week.
- D. Cost of delay 2 a week, duration 1 week.

<details><summary>Answer</summary>

**C.** CD3 divides cost of delay by duration: C gives 9, A 2.5, B 1 and D 2. A has the largest weekly loss, but it is long; D is short but cheap to delay. See "Cost of delay".

</details>

## 📚 References
*Web pages below were opened and read on 2026-11-22. The book was not opened, so what the lesson says about it is reported.*

- Intercom blog, "RICE: Simple prioritization for product managers" (Sean McBride): https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/ — origin, formula and scales of RICE.
- ProdPad, "Why I invented the Now-Next-Later roadmap" (Janna Bastow): https://www.prodpad.com/blog/invented-now-next-later-roadmap/ — origin of the format.
- Reinertsen, D. G., *The Principles of Product Development Flow: Second Generation Lean Product Development* (Celeritas Publishing, 2009): cost of delay and scheduling by cost of delay divided by duration (full citation; not opened).
- Agile Business Consortium, "What is MoSCoW Prioritization?": https://www.agilebusiness.org/resource/what-is-moscow-prioritization/ — the four categories and their use within a time box.
- Library course: [*Running IT as a Business*, lesson 3.2 — Prioritising and funding work: business cases, cost of delay and funding products not projects](../itbiz/index.html#/3.2).

---

# 6.2 — Requirements, user stories and acceptance criteria
*Level: 🟡 Intermediate* · *Prerequisites: 5.2, 6.1* · *Step: Discover, Design*

**After this you can** tell functional requirements from quality requirements and constraints, write a user story that names a person, a need and a reason, add acceptance criteria as rules and given-when-then examples including unhappy paths, and split a large item into small stories that are each usable. *Study time: reading about 15 min, hands-on about 95 min (estimate).*

## ⚡ In 60 seconds
- A **requirement** says what a product must do or be. **Functional** requirements describe behaviour; **quality** (non-functional) requirements describe how well: speed, reliability, security, privacy, accessibility. **Constraints** limit how you may build it.
- A **user story** describes a need from a user's point of view. It is a reminder for a conversation, not a full specification.
- **Acceptance criteria** say how you will know a story is done. Concrete "given … when … then …" examples expose misunderstandings before code is written.
- The rule that matters most: **if you cannot say how you would check it, you do not yet know what you want.**
- Decision cue: before a story enters an iteration, ask "what happens when it goes wrong?"
- Biggest trap: a one-line ticket ("add photo upload") that each reader fills in differently.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

Yasmin's first real task on the Courier team is a ticket: "Proof of delivery: courier takes a photo at drop-off." In four days she has tapping "Delivered" open the camera, upload the photo and complete the order. It passes review and goes out behind a feature flag (lesson 3.3) to twenty couriers.

Within a week three groups are disappointed. Salma's support agents, who asked for photos to settle "my order never arrived" disputes, cannot see them in the support desk. Merchants expected to receive the photo. Couriers in stairwells with no signal cannot complete deliveries, because the upload must finish first; two start marking orders "Delivered" before going upstairs. Then Karim notices photos showing customers' faces and the inside of homes, and asks who decided what may be photographed and how long photos are kept.

Yasmin did exactly what the ticket said. It did not say who needed the photo, why, what happens without a signal, or what must not be captured.

## 📐 How it works

### 🟢 The essentials

**Three kinds of requirement.**

| Kind | What it says | Proof-of-delivery example |
|---|---|---|
| **Functional** | What the product does | The courier can attach a photo when marking an order delivered |
| **Quality** | How well it must do it, including security and privacy | The drop-off works with no network, the photo uploading later; only support and the order's merchant may view a photo |
| **Constraint** | A limit on how you may build it | Must work on the older Android phones couriers already use |

Quality requirements are the most often forgotten. Check at least: performance, reliability (what happens on failure), security, privacy (what personal data, who sees it, for how long), accessibility and operability (can support and on-call see what is happening). The ISO/IEC 25010 standard, revised in 2023, describes a reference model of product quality characteristics (as reported by ISO's page). For accessibility, the common reference is the W3C's Web Content Accessibility Guidelines (WCAG) 2.2, a W3C Recommendation since October 2023.

**User stories.** The best-known template is:

> **As a** (kind of user), **I want** (something), **so that** (reason).

Mike Cohn of Mountain Goat Software writes that it originated with agile coach Rachel Davies at Connextra, a UK company, in the early 2000s. "As a" names whose problem it is; "I want" states the need, ideally not as a screen; "so that" gives the reason, which lets the team find a better solution.

| Weak | Better |
|---|---|
| "Proof of delivery photo." | "As a support agent, I want to see a photo of where an order was left, so that I can settle 'never arrived' disputes without calling the courier." |

"As a user" hides the most important question: whose problem is this?

**Card, conversation, confirmation.** Ron Jeffries, a co-author of *Extreme Programming Installed*, described a story in a 2001 essay as three parts: the **card** (a short reminder), the **conversation** (where details are worked out) and the **confirmation** (the acceptance tests).

**Acceptance criteria.** **Acceptance criteria** are conditions one story must meet. They differ from the **definition of done** (lesson 5.2), which applies to every item. Two forms:

- **Rules:** statements that must be true. "Only the order's merchant and support agents can view the photo."
- **Examples** in given-when-then form:

> **Given** a courier at the drop-off point with no signal,
> **When** the courier takes a photo and taps "Delivered",
> **Then** the order shows as delivered on the phone at once,
> **And** the photo uploads when the signal returns,
> **And** support sees "photo pending" until it arrives.

The given-when-then form was developed by Dan North and Chris Matts as part of behaviour-driven development (BDD), where teams agree examples of behaviour before building (as reported by Martin Fowler's site). Examples flush out disagreements that rules hide.

### 🟡 Going deeper

**Is the story ready? INVEST.** Bill Wake proposed in 2003 that good stories are Independent, Negotiable, Valuable, Estimable, Small and Testable (as reported by the Agile Alliance glossary):

| Letter | Question | Fails when |
|---|---|---|
| Independent | Can it ship without waiting for another story? | "Part 2 of 5, needs 1, 3 and 4" |
| Negotiable | Is the "how" still open? | A finished design with no room to change |
| Valuable | Does someone outside the team gain from it alone? | "Create the photo database table" |
| Estimable | Do we understand it well enough to size it? | Nobody knows how offline storage works on courier phones |
| Small | Can it be done in a few days? | "Proof of delivery, everything" |
| Testable | Could we write acceptance criteria today? | "Make delivery proof better" |

If an unknown blocks estimating, a short time-boxed investigation (a **spike**) comes first.

**Splitting stories.** Split by what users experience, not by technical layer (lesson 5.2):

| Split by | Example |
|---|---|
| **Workflow steps** | Courier takes photo → support views it → merchant receives it |
| **Happy, then unhappy paths** | With signal → without signal → camera permission denied |
| **Business rules** | All orders → only "leave at door" orders |
| **Simple first** | Photo only → photo plus time stamp |

**Story maps** (lesson 2.2) work for one feature too: the journey left to right, stories stacked under each step from essential to optional, and a line marking a thin first release across the whole journey.

**Quality requirements as criteria.** Make them checkable: "fast" becomes "order search returns in under two seconds for 95% of searches" (illustrative). Those for all work go in the definition of done; those for one story go in its criteria.

### 🔴 Expert view

**Three viewpoints before building.** Hold a short conversation per story with product (why, for whom), engineering (how, what is hard) and testing (what could go wrong). Testing usually finds the unhappy paths the others missed. See [*Software Testing: Zero to Hero in the AI Era*, lesson 5.3 — Exploratory testing, agile teams and BDD: working with developers, product owners and users](../testing/index.html#/5.3).

**Personal data is a requirement.** When a story collects or shows personal data (photos of homes, phone numbers, locations), its criteria should answer: what is collected, why, who sees it, how long it is kept, how it is deleted. Data protection rules vary by country; the team's job is to ask early and involve whoever advises the company, not to decide the legal answer. Module 9 returns to this.

**AI tools draft; people decide.** An AI assistant can draft stories, but it does not know your couriers' buildings and may invent rules; check every criterion with the people who have the problem.

**The memorable rule.** If you cannot say how you would check it, you do not yet know what you want.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **User story card** | As a / I want / so that, with links to evidence | For every item near the top of the backlog |
| **Acceptance criteria** | Rules and given-when-then examples, including unhappy paths | Before a story enters an iteration |
| **Quality requirements prompt** | One question each on performance, reliability, security, privacy, accessibility, operability | When refining any user-facing story |
| **Story map** | Journey left to right, stories by importance, a first-release line | When a feature is too large for one list |

## 🏛️ In practice at Qafila
Yasmin, Aisha, Salma, Karim and a tester rewrote proof of delivery as a small map and stories. Illustrative and fictional.

> **Proof of delivery: story map**
>
> | Courier captures | Support uses | Merchant sees |
> |---|---|---|
> | Take a photo on "Delivered", works offline | View the photo on the order in the support desk | — |
> | Camera denied: deliver without photo, flagged | Search "delivered without photo" | — |
> | ———— first release line ———— | | |
> | Guidance: "show the door, not people" | | Photo shown on the merchant's order |

The merchant step is deliberately empty above the line: this release's journey is courier → support, because disputes were the problem to solve, and merchants come once privacy questions are settled.

> **Story 1.** As a courier, I want to take a photo when I mark an order delivered, even without a signal, so that I can finish the drop-off and move on.
>
> *Rules:* a photo is required only for "leave at door" orders; the order shows as delivered on the phone at once; how long photos are kept is an open question (owner: Aisha, with the company's adviser).
>
> *Examples:*
> - **Given** a "leave at door" order and no signal, **when** the courier takes a photo and taps "Delivered", **then** the order is delivered on the phone and the photo uploads within a minute of the signal returning.
> - **Given** camera access is denied, **when** the courier taps "Delivered", **then** the app explains why a photo is needed, offers settings, and allows delivery without one, flagged for support.
> - **Given** the phone restarts before the upload, **when** the app opens again, **then** the queued photo still uploads.
>
> **Story 2** (support views the photo) follows the same pattern: only support agents, and later the order's merchant, can open a photo, and every view is logged.

The forty-minute conversation changed the work. Salma pointed out that most deliveries are handed over in person, where a photo adds nothing, so photos became required only for "leave at door". The tester's restart question became the third example; Karim's about faces became a guidance story and an open question with an owner. Yasmin's capture code was kept; the offline queue took about three days.

## 🛠️ Exercises
**🟢 Repair three weak stories.** Rewrite each with a specific user, a need and a reason: (a) "Add export button"; (b) "As a user I want notifications"; (c) "Improve courier map".
*Done when:* each names a specific kind of user, the "I want" part is a need rather than a screen control, and the "so that" part gives a reason someone could disagree with.

<details><summary>Model answer and self-check</summary>

**Model answer.** (a) "As a merchant, I want my month's deliveries in a file my accountant opens, so that I stop retyping them." (b) "As a bakery owner, I want to know when a courier is over fifteen minutes late for a scheduled pickup, so that I can keep the order warm or call my customer." (c) "As a courier new to an area, I want the map to show the shop's entrance, so that I do not walk round the block."

**Self-check.**
- Would two engineers imagine the same thing from your story?
- Does each "so that" leave room for a different solution?
- Did you avoid naming a screen element in the "I want" part?

</details>

**🟡 Write acceptance criteria with unhappy paths.** For "As a merchant, I want to cancel a delivery before a courier picks it up, so that I am not charged for orders my customer cancelled", write rules and at least four given-when-then examples: one happy path, two unhappy paths and one quality requirement.
*Done when:* the rules say what is and is not allowed; the examples cover "courier on the way" and "courier has picked up"; and one example is a checkable quality requirement.

<details><summary>Model answer and self-check</summary>

**Model answer.** Rules: cancel any order not yet picked up; no fee before a courier is assigned; any later fee is an open question for Aisha and Bilal. Examples: (1) **Given** no courier assigned, **when** the merchant cancels, **then** there is no fee and the order leaves the courier queue. (2) **Given** a courier on the way, **when** the merchant cancels, **then** the merchant sees any fee before confirming and the courier's app shows "cancelled, do not go". (3) **Given** the order is picked up, **when** the merchant tries to cancel, **then** the app says it is on its way and offers support. (4) **Given** normal load, **when** the merchant cancels, **then** the courier is notified within ten seconds in 99% of cases (illustrative; check it is measurable).

**Self-check.**
- Did you write the courier's side as well as the merchant's?
- Is every "then" something a tester could observe?
- Did you name an owner for any rule you could not decide?

</details>

**🔴 Split an epic and draw a thin first release.** An **epic** is a large item to be split into stories. "Recurring deliveries" lets a merchant set up a delivery that repeats (for example every morning at 6 a.m.). Split it into at least six stories, arrange them as a story map with three or four journey steps, draw a first-release line, and run INVEST on the two riskiest stories above the line.
*Done when:* every story is usable on its own by a named user, the first release covers the whole journey thinly, and your INVEST notes name at least one problem and its fix.

<details><summary>Model answer and self-check</summary>

**Model answer.** Steps: set up → it runs → change or pause → see what happened. Above the line, each "As a bakery owner, I want…": my order repeated daily in the same time window, so that I stop re-entering it; each repeat to appear in my order list the night before, so that I can check it; to skip one day, so that holidays cost nothing; to see upcoming repeats, so that I know what is booked. Below: weekly patterns; different addresses per day; holiday calendar; monthly summary. INVEST: "appears the night before" is not estimable until someone checks how scheduled jobs (tasks the system runs automatically at set times) work on the platform (one-day spike). "Skip one day" depends on the upcoming list; fine if both ship together, otherwise merge them.

**Self-check.**
- Did any story above the line deliver nothing alone (a table, an API)?
- Can a merchant go from setup to seeing the result in the first release?
- Did you push rare cases below the line?

</details>

## ⚠️ Mistakes and traps
- **One-line tickets.** Name the user, the need and the reason, and add criteria.
- **Only the happy path.** Ask what happens with no signal, no permission or a restart.
- **Forgetting quality requirements.** Run the quality prompt for every user-facing story.
- **Splitting by technical layer.** "Back end" (server and database) and "front end" (screens) stories deliver nothing alone; split by step, rule or path.

## 🧾 Recap
- Requirements are functional (what), quality (how well) and constraints (limits on how); quality requirements are most often missed.
- A user story names who needs what and why; it is a reminder for a conversation confirmed by acceptance criteria.
- INVEST checks readiness; split by workflow, path or rule; a story map keeps the whole journey visible.
- Rule: if you cannot say how you would check it, you do not yet know what you want.

## ✍️ Check yourself
**1. The Merchant team lists four requirements for a new bakery order screen. Which is a quality (non-functional) requirement?**

- A. The merchant can pick a time window for any day next week.
- B. The screen loads in two seconds on a slow connection, 95% of the time.
- C. The merchant can copy yesterday's order into today's in one tap.
- D. The merchant can add a short note for the courier to each order.

<details><summary>Answer</summary>

**B.** It says how well the screen must work (speed under poor conditions), and it is checkable. A, C and D describe what the product does for the merchant, so they are functional. See "Three kinds of requirement".

</details>

**2. Yasmin built exactly what the ticket "Proof of delivery: courier takes a photo at drop-off" said, yet three groups were disappointed. What was mainly missing?**

- A. A detailed screen design for the photo step.
- B. A larger estimate, giving Yasmin more time.
- C. A separate ticket written by each group.
- D. The user, the reason and acceptance criteria.

<details><summary>Answer</summary>

**D.** The ticket named a solution but not who needed it, why, or what happens when things go wrong. A adds detail without the why, B gives more time for the wrong thing, and C multiplies one-line tickets. See "User stories".

</details>

**3. Yasmin's story passes all its given-when-then examples. The team's definition of done also asks for an updated support note, and nobody has written one. Is the story done?**

- A. No: the definition of done applies to every item too.
- B. Yes: its own criteria are the only test of a story.
- C. Yes: the support note is Salma's job, not the team's.
- D. No: its examples must be rewritten to check the note.

<details><summary>Answer</summary>

**A.** Acceptance criteria apply to one story; the definition of done is the shared bar for all work, so both must be met. B ignores the definition of done, C pushes shared work out of the team, and D confuses the two by copying a general rule into one story. See "Acceptance criteria".

</details>

**4. The Merchant team splits "recurring deliveries" into "database for repeats", "API for repeats" and "screens for repeats". What is the main problem?**

- A. The stories are too small to estimate.
- B. The stories do not start with "As a merchant".
- C. No single story gives a merchant anything usable.
- D. The stories are too independent to order.

<details><summary>Answer</summary>

**C.** Splitting by technical layer fails the "valuable" test: no piece helps a merchant alone. A misreads the problem, B fixes wording but not the split, and D is wrong because layers depend on each other. See "Splitting stories".

</details>

**5. Karim notices that delivery photos sometimes show customers' faces. What should the team do with this in the story?**

- A. Add privacy questions and an owner, and involve the adviser.
- B. Leave it out, as privacy is handled outside the team.
- C. Decide in the conversation which data protection law applies.
- D. Drop the feature, as photos of people make it unlawful.

<details><summary>Answer</summary>

**A.** Personal data questions belong in the criteria with a named owner; legal answers come from whoever advises the company. B hides the question, C asks the team for a legal conclusion, and D jumps to an unchecked one. See "Personal data is a requirement".

</details>

## 📚 References
*Web pages below were opened and read on 2026-11-22, except ISO's page, which refused automated access, so what the lesson says about ISO/IEC 25010 is reported.*

- Mountain Goat Software, "Why the three-part user story template works so well" (Mike Cohn): https://www.mountaingoatsoftware.com/blog/why-the-three-part-user-story-template-works-so-well — the template and its Connextra origin.
- Jeffries, R., "Essential XP: Card, Conversation, Confirmation" (2001): https://ronjeffries.com/xprog/articles/expcardconversationconfirmation/.
- Agile Alliance glossary, "INVEST": https://agilealliance.org/glossary/invest — credited to Bill Wake's 2003 article "INVEST in Good Stories, and SMART Tasks".
- Fowler, M., "GivenWhenThen": https://martinfowler.com/bliki/GivenWhenThen.html — origin in behaviour-driven development with Dan North and Chris Matts.
- ISO, "ISO/IEC 25010:2023 — Product quality model": https://www.iso.org/standard/78176.html.
- W3C, "Web Content Accessibility Guidelines (WCAG) 2.2": https://www.w3.org/TR/WCAG22/ and the October 2023 announcement: https://www.w3.org/news/2023/web-content-accessibility-guidelines-wcag-2-2-is-a-w3c-recommendation.
- Library course: [*Software Testing: Zero to Hero in the AI Era*, lesson 1.3 — Requirements, test cases and bug reports: from acceptance criteria to a defect someone can fix](../testing/index.html#/1.3).

---

# 6.3 — Measuring outcomes: product analytics and experiments
*Level: 🟡 Intermediate* · *Prerequisites: 3.3, 6.1* · *Step: Discover, Design*

**After this you can** choose a primary outcome metric with input and guardrail metrics, write a tracking plan of named events with a purpose and a privacy note, tell an actionable metric from a vanity metric, and design a simple controlled experiment with a hypothesis, a unit of randomisation, a fixed duration and a decision rule. *Study time: reading about 15 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- **Product analytics** is collecting and studying records of what people do in a product (events), to see whether the team's work changed behaviour.
- Pick one **primary metric** per goal, a few **input metrics** the team can influence directly, and **guardrail metrics** that must not get worse.
- An **experiment** (A/B test) compares a randomly chosen group that gets a change with one that does not, at the same time. Randomness is what lets you say the change caused the difference.
- The rule that matters most: **decide what would change your mind before you look at the data.**
- Decision cue: if you cannot write "we ship if this moves by about this much, and stop if that gets worse", you are not ready to measure.
- Biggest trap: counting what is easy (clicks, views) instead of what matters, then stopping a test as soon as the chart looks good.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

The top roadmap item from lesson 6.1 is "merchants see delivery progress without phoning". Order tracking so far shows status only, so the Merchant team builds a live tracking page: when a courier picks up an order, the merchant and the end customer get a link showing the courier on a map. It goes to all merchants on a Monday. On Friday the team's product manager posts a chart: "Tracking page views: 31,000 this week!"

Hamad, the data analyst, asks a different question: did "where is my delivery?" contacts to the support desk go down? Nobody knows. Support tags contacts by reason, but nobody linked the tags to the release, and the release week was also the week before a public holiday, when deliveries always rise. Two merchants have complained that the link shows the courier's location to their customers while the courier is on a break.

Page views say people opened the link, not whether behaviour changed or what harm the feature caused.

## 📐 How it works

### 🟢 The essentials

**Events and the tracking plan.** An **event** is a record that something happened: who (an identifier), what (a name), when (a time stamp) and details (properties). For example `delivery_tracking_viewed` with `order_id` and `viewer_type` (merchant or end customer). A **tracking plan** is the agreed list of events, their properties, meaning and purpose. Without one, names drift and nobody trusts the numbers. Review changes to it like code, and test that events fire.

**Choose metrics from the outcome.** Work down from the goal:

| Layer | What it is | Live tracking example |
|---|---|---|
| **Primary metric** | The outcome the work should move | "Where is my delivery?" contacts per 1,000 deliveries |
| **Input metrics** | Behaviours that drive it, which the team influences directly | Share of deliveries where the link was opened; link delivery success |
| **Guardrail metrics** | What must not get worse | Courier app crash rate; text cost per delivery; courier privacy complaints; order tracking availability (99.9% a month) |

Use **rates, not raw counts**: "contacts per 1,000 deliveries" compares fairly across busy and quiet weeks.

**Vanity versus actionable.** A **vanity metric** goes up and feels good but does not tell you what to do: total page views, sign-ups since launch, downloads. An **actionable metric** is tied to a decision. Test any metric with: "if this doubled or halved, what would we do differently?"

**Funnels and cohorts.** A **funnel** shows how many people complete each step of a journey (link sent → opened → map loaded); look first at the biggest drop. A **cohort** groups people by when they started and follows them over time, showing **retention**: whether people keep using something, which matters more than a first-week spike.

### 🟡 Going deeper

**Why before-and-after misleads.** Comparing the week before a release with the week after mixes your change with everything else: a holiday, a campaign, an outage. Treat before-and-after as a hint, not proof.

**Controlled experiments.** In an **experiment**, you randomly assign units to a **control** group (no change) and a **treatment** group (the change), run both at the same time, and compare. Holidays and weather hit both groups equally, so the difference that remains is most likely caused by the change. At Qafila, a feature flag (lesson 3.3) turns the feature on for one group only. Before starting, write down six things: the **hypothesis** (what will change, for whom, why), the **unit** assigned to each group, the one **primary metric** that decides, the **guardrails**, the **duration** (fixed in advance) and the **decision rule** (which result leads to which action). The brief in "In practice at Qafila" shows all six.

**Choosing the unit.** Randomise where the change is experienced and where groups do not affect each other. Randomising by end customer would give one shop both experiences, and the merchant might keep phoning for every order. If couriers serve shops in both groups, a courier-app change can leak into the control group. Discuss the unit with an analyst; it is usually the hardest decision.

**Fix the length; do not peek and stop.** The usual statistical tests assume you look once, at a planned end. A result is **statistically significant** when it is unlikely to be chance alone; **noise** is the random up-and-down that any metric shows. If you check daily and stop when the result looks significant, the chance of declaring a win that is really noise rises well above what the test reports. Evan Miller's 2010 essay "How Not To Run an A/B Test" is a well-known explanation. Run whole weeks, and ask an analyst or use a sample-size calculator to check you have enough units to see the difference you care about.

### 🔴 Expert view

**Check the experiment before trusting the result.** If you assigned units fifty-fifty, the groups should be close to fifty-fifty. If not, assignment or logging is broken. Kohavi, Tang and Xu's *Trustworthy Online Controlled Experiments* (Cambridge University Press, 2020) has a chapter on this **sample ratio mismatch** and other trust checks, and says the check should be included in every experiment. Check also that events and metrics work the same in both groups.

**Most ideas do not work as hoped.** Slides from a 2009 tutorial by Ron Kohavi and colleagues reported that about two-thirds of ideas tested at Microsoft did not improve the metric they were designed to improve (a finding for Microsoft at that time, not a general law).

**When a clean experiment is impossible.** Some changes reach too few units, cannot be split fairly (a price everyone sees) or will ship anyway. In order of strength: a **staged rollout** with a group held back for a few weeks; a similar group chosen before looking at results; before-and-after with everything else that changed listed; and qualitative evidence (support transcripts, interviews), often the best way to learn *why* a number moved.

**Analytics collects personal data.** Collect only what a stated purpose needs, keep it no longer than needed, restrict access, and check consent and notice duties with whoever advises the company.

**The memorable rule.** Decide what would change your mind before you look at the data.

For depth, see [*Data Engineering & Analytics: Zero to Hero*, lesson 4.3 — Experiments and statistics for analysts: A/B tests and the traps that fool smart people](../data/index.html#/4.3) and [*SaaS Building Blocks*, lesson 6.2 — Analytics: product, web and the event pipeline](../saas/index.html#/6.2).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Metric tree** | Goal, primary metric, input and guardrail metrics, each with a definition and source | Before building anything meant to change behaviour |
| **Tracking plan** | Event names, properties, meaning, purpose, owner and retention | Before events are added; reviewed like code |
| **Experiment brief** | Hypothesis, unit, metrics, duration, decision rule, written before the start | Whenever a change can be split between groups |
| **Trust checks** | Sample ratio, events firing in both groups, same metric calculation | Before reading any result |
| **Results note** | What we tested, what happened, what we decided and learned | After every experiment, including failures |

Tools are examples: a product analytics service, or a spreadsheet of support contacts joined to deliveries, is enough to start.

## 🏛️ In practice at Qafila
Hamad and the Merchant team's product manager turned the release into a proper test. Illustrative and fictional. They switched the flag off, fixed the privacy problem first (the map now shows the courier only between pickup and drop-off for that order), and wrote the brief:

> **Experiment brief: live tracking link (Growth, quarter 1)**
>
> - **Hypothesis:** if merchants and end customers can see the courier on the way, fewer will contact support to ask where a delivery is.
> - **Unit:** merchant account; all active merchants split at random, half and half.
> - **Primary metric:** "where is my delivery?" contacts per 1,000 deliveries (support reason tag joined to deliveries by merchant).
> - **Guardrails:** courier privacy complaints; text cost per delivery; courier app crash rate; order tracking availability.
> - **Duration:** four full weeks, decided in advance; no early decision unless a guardrail breaks.
> - **Decision rule:** ship to all if contacts per 1,000 deliveries are at least 3 lower in treatment than in control (from about 17), confirmed by Hamad's significance check, and every guardrail stays within its limit: text cost per delivery up no more than 25%, no more than 2 privacy complaints, crash rate and tracking availability no worse. Otherwise review the design.
> - **Trust checks:** split close to 50/50; events firing in both groups; agents tag reasons without knowing which group a merchant is in.

> **Results note (after four weeks)**
>
> | Metric | Control | Treatment |
> |---|---|---|
> | Merchants | 1,003 | 997 |
> | Contacts per 1,000 deliveries | 17 | 11 |
> | Link opened (share of deliveries) | — | 58% |
> | Text cost per delivery | baseline | up about a fifth |
> | Privacy complaints | 0 | 1 |
>
> **Decision:** ship to all, as the rule says: contacts fell by 6, the significance check passed, and text cost and complaints stayed inside their limits. To keep text cost well under its limit, send the link only when an order is expected to take more than 20 minutes; follow up the complaint. **Learned:** most opens came from end customers, not merchants.

The 1,003 to 997 split passed the sample ratio check. In week two the product manager wanted to stop early; Hamad pointed to the brief, and the difference narrowed a little but held. Contacts per 1,000 deliveries replaced the page-views chart in the weekly review. Yasmin, who added the courier-side events, learned that an event with no purpose does not get added.

## 🛠️ Exercises
**🟢 Replace vanity metrics.** Say why each is a vanity metric and propose an actionable one for the same goal: (a) total app downloads since launch; (b) features shipped this quarter; (c) help-centre page views; (d) total registered couriers.
*Done when:* each replacement is a rate or share tied to a behaviour, you can name its source record, and you can say what you would do if it moved.

<details><summary>Model answer and self-check</summary>

**Model answer.** (a) Downloads only grow; use "share of new merchants completing a first delivery within 7 days" (orders). (b) An output count; use "share of roadmap outcomes whose primary metric moved as intended" (results notes). (c) More views may mean more confusion; use "share of help-centre visits not followed by a support contact within a day". (d) Registered is not active; use "couriers completing at least one delivery a week".

**Self-check.**
- Could each new metric go down as well as up?
- Is each a rate or share?
- Can you say what decision a change would trigger?

</details>

**🟡 Write a tracking plan.** For proof of delivery (lesson 6.2) or a feature of your own, write four to six events: name, when it fires, properties, purpose (which metric it feeds) and a privacy note.
*Done when:* every event feeds a named metric, names follow one pattern (for example `object_action`, lower case), at least one property is left out on purpose with a reason, and any personal data is stated.

<details><summary>Model answer and self-check</summary>

**Model answer.** `delivery_photo_taken` (order_id, offline yes/no; share of "leave at door" orders with a photo). `delivery_photo_uploaded` (order_id, minutes queued; upload delay). `delivery_photo_skipped` (order_id, reason; skip rate). `delivery_photo_viewed` (order_id, viewer_type; share of disputes where support opened the photo). Left out: GPS coordinates, because the order already holds the address and precise location adds risk with no stated purpose. Privacy note: the photo itself is never in analytics; events hold identifiers only. The security access log that lesson 6.2 requires is a separate record kept by the system, not an analytics event.

**Self-check.**
- Does each event answer a question someone has actually asked?
- Did you keep photos and precise location out of analytics?
- Would two engineers name the next event the same way?

</details>

**🔴 Design an experiment, then find the flaws in a bad one.** Part 1: write a brief (hypothesis, unit, primary metric, two guardrails, duration, decision rule with a size, trust checks) for "show couriers the customer's building entrance and floor note", aiming for fewer failed first delivery attempts. Part 2: list at least five flaws in this report: "We turned the new courier home screen on for couriers who opted into beta. After three days, 'Start shift' taps were up 12% on last month, so we stopped and shipped it. Crash rate was not checked."
*Done when:* your brief fixes duration and a sized decision rule in advance with a unit that avoids leakage, and your flaw list names self-selection, a different-period comparison, early stopping, a metric that may not reflect the goal and a missing guardrail.

<details><summary>Model answer and self-check</summary>

**Model answer.** Part 1: couriers who see the entrance and floor note fail fewer first attempts; unit: courier; primary metric: failed first delivery attempts per 1,000 deliveries; guardrails: time per drop-off, crash rate; four full weeks; ship if failed first attempts fall by at least a quarter, confirmed by an analyst's significance check, with no guardrail worse; checks: 50/50 courier split, events in both groups. Part 2: beta volunteers are not random; last month is a different period with other changes; three days and stopping on a good result inflates false wins; "Start shift" taps may not reflect any real improvement; crash rate unchecked, so harm could hide.

**Self-check.**
- Did you write the decision rule before imagining the result?
- Is your unit where the change is experienced?
- Did you spot that the comparison was a different time, not a random group?

</details>

## ⚠️ Mistakes and traps
- **Celebrating vanity metrics.** Ask "if this doubled, what would we do differently?"
- **Before-and-after as proof.** Use a controlled comparison where you can; label before-and-after a hint.
- **Peeking and stopping early.** Fix duration and decision rule in advance; stop early only if a guardrail breaks.
- **Collecting everything "just in case".** Every event needs a purpose; personal data without one is a risk.

## 🧾 Recap
- Events record what happened; a tracking plan keeps their names, properties and purposes consistent.
- Work down from the goal: one primary metric, input metrics and guardrails; prefer rates to counts.
- Randomised experiments run at the same time separate a change's effect from everything else; choose the unit carefully, fix the length and check the sample ratio.
- Rule: decide what would change your mind before you look at the data.

## ✍️ Check yourself
**1. After the live tracking release, the team reports 31,000 tracking page views in a week. What does this tell them about the roadmap outcome?**

- A. The outcome was met: high usage shows value.
- B. The outcome was partly met: some viewers would have phoned.
- C. The feature failed: views are fewer than deliveries.
- D. Little: views do not show whether contacts changed.

<details><summary>Answer</summary>

**D.** The outcome is fewer contacts; views show the link was opened, not that behaviour changed. A and B assume the outcome from usage, and C uses a comparison that does not measure the outcome either. See "Vanity versus actionable".

</details>

**2. Why does Hamad randomise the live tracking test by merchant account rather than by end customer?**

- A. Fewer units make the test finish sooner.
- B. Each merchant should see one consistent experience.
- C. Data protection rules forbid randomising customers.
- D. Contacts are never recorded against orders.

<details><summary>Answer</summary>

**B.** By end customer, one shop would see both experiences and might keep phoning for every order, blurring the difference. A is not the reason (fewer units makes a real difference harder to detect), C states a legal conclusion the lesson does not make, and D is an assumption, not a design reason. See "Choosing the unit".

</details>

**3. In week two the treatment group already looks better, and the product manager wants to stop and ship. What should Hamad say?**

- A. Stop now: an early clear difference is strong evidence.
- B. Stop now if the sample ratio is exactly 50/50.
- C. Run the planned four weeks: early stops inflate false wins.
- D. Extend the test until the difference convinces everyone.

<details><summary>Answer</summary>

**C.** Checking repeatedly and stopping when the result looks good raises the chance of a false win. A is the trap itself, B confuses a trust check with a stopping rule, and D moves the end point. See "Fix the length; do not peek and stop".

</details>

**4. A test assigned merchants 50/50, but the results show 1,240 merchants in control and 760 in treatment. What should the team do first?**

- A. Distrust the result until they know why the split is off.
- B. Rescale treatment to 1,000 merchants, then compare.
- C. Accept it: the treatment group is still large enough.
- D. Rerun at once with the same assignment code.

<details><summary>Answer</summary>

**A.** A split far from the plan signals broken assignment or logging, so the result cannot be trusted until explained. B and C ignore the warning, and D repeats the fault without finding it. See "Check the experiment before trusting the result".

</details>

**5. Qafila will change its delivery fee for all merchants at once, so a clean randomised test is impossible. What is the most sensible way to measure the effect?**

- A. Skip measurement: without randomisation there is no evidence.
- B. Use a similar comparison group, list other changes, add interviews.
- C. Compare total orders the month before and after, as proof.
- D. Show different fees to customers secretly, as a hidden test.

<details><summary>Answer</summary>

**B.** Without a clean experiment, use the strongest comparison available, be open about what else changed, and add qualitative evidence. A gives up too soon, C treats before-and-after as proof, and D creates a fairness and trust problem. See "When a clean experiment is impossible".

</details>

## 📚 References
*Web pages below were opened and read on 2026-11-22.*

- Miller, E., "How Not To Run an A/B Test" (2010): https://www.evanmiller.org/how-not-to-run-an-ab-test.html — repeated checking and early stopping.
- Kohavi, R., Tang, D. and Xu, Y., *Trustworthy Online Controlled Experiments* (Cambridge University Press, 2020), ch. 21, "Sample Ratio Mismatch and Other Trust-Related Guardrail Metrics", pp. 219–225: https://doi.org/10.1017/9781108653985.027.
- Kohavi, R. and colleagues, KDD 2009 tutorial slides (part 1): https://ai.stanford.edu/~ronnyk/2009-06-28KDDTutorialT4part1.pdf — reports that about two-thirds of ideas tested at Microsoft did not improve the metric they were designed to improve.
- Library course: [*Data Engineering & Analytics: Zero to Hero*, lesson 4.1 — Defining metrics: one definition, a semantic layer and a metrics catalogue](../data/index.html#/4.1).
- Library course: [*Data Engineering & Analytics: Zero to Hero*, lesson 4.3 — Experiments and statistics for analysts: A/B tests and the traps that fool smart people](../data/index.html#/4.3).
- Library course: [*SaaS Building Blocks*, lesson 6.2 — Analytics: product, web and the event pipeline](../saas/index.html#/6.2) and [lesson 6.3 — Feature flags and experiments](../saas/index.html#/6.3).
