# Module 12 — The bigger picture and your path

*Qafila is Established: about 400 people in 35 teams, about 30,000 merchants in four countries, about 400,000 deliveries a day (illustrative figures, as everywhere in this course). The payments partner has signed, the governance work from Module 11 is in place, and the company now has things a small startup never needed: a view of all its applications and the business abilities they serve, a yearly investment plan, and AI tools in almost everyone's daily work. Early-career practitioners meet all of this from below. A team proposal gets asked "which capability does this serve, and is there already something for it?" A support reply drafted by an AI assistant goes to a merchant. A manager asks which certification you plan to take next. This module shows the bigger picture from where you stand, mostly through Yasmin, still a senior engineer on Courier Payouts, one of the teams in Qafila's Payments area. First, enterprise architecture and the investment portfolio, seen from a team: what they are for, and how to make a proposal fit them. Second, AI in digital work: how to use it well and which controls keep it safe. Third, the frameworks and bodies of knowledge you will hear about at work, what each is for, and how to plan your own learning after this course. Each lesson leaves an artefact: a fit check for a team proposal, a personal and team AI use card, and a learning plan for your next year.*

> **Steps:** Govern, Collaborate — see how your team's work fits the company's map and investment plan, use AI with clear limits and named accountability, and choose your own next steps in a field full of frameworks.

---

# 12.1 — Enterprise architecture and portfolio, seen from a team
*Level: 🔴 Advanced* · *Prerequisites: 9.1, 10.1, 11.1* · *Step: Govern, Collaborate*

**After this you can** place a team proposal on the company's capability map, check it against the application portfolio and the technology standards, name the investment theme it belongs to, and write a one-page fit check that says whether to build, reuse, extend or stop. *Study time: reading about 15 min, hands-on about 75 min (estimate).*

## ⚡ In 60 seconds
- **Enterprise architecture** keeps a shared picture of what the business does, which systems support it and which technologies are preferred, so many teams' decisions add up.
- The **investment portfolio** is what the company chooses to fund, grouped so money goes where strategy says.
- From a team, both show up as questions: which capability, what exists, which standard, which theme?
- The rule that matters most: **check the map before you build.**
- Decision cue: if a capability already has two applications, a third needs a reason.
- Biggest trap: treating architecture as a gate to get past rather than a shared memory of past decisions.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

After the payments partner went live, merchants asked for a receipt by message every time a customer paid in the app. The Payments area asked Yasmin to lead it, and she and two colleagues sketched it in an hour: a small new service that would listen for payment events and send messages through a messaging supplier. (An **event** is a short message one service publishes when something happens, such as "payment taken"; other services listen for it on the event stream from lesson 9.2.) Faisal, now Head of Engineering, asked one question first: "Who else sends messages to merchants or couriers?"

Nobody knew. Yasmin spent a morning finding out, and found three messaging routes, two of them for merchants. The Merchant Orders team sent delivery updates to merchants through one messaging supplier. Support sent merchant notices through the support desk tool. The Courier Experience team had its own alerts service for couriers, built at Growth, using a second supplier. A new service would have added another supplier, another place holding merchants' phone numbers, and another answer to the payments partner's question "where does customer contact data go?" from Module 11.

That morning was enterprise architecture done by hand. At 35 teams nobody can hold the whole company in their head, so the company keeps a few shared maps.

## 📐 How it works

### 🟢 The essentials

**Why a company needs a shared picture.** With one team, the team's head is the map. With 35, not knowing what exists becomes expensive: duplicated services, extra suppliers, personal data in places nobody tracks. Enterprise architecture (**EA**) exists to keep that cost down. It does not design every system; it keeps a few shared pictures current and helps teams use them.

**Four maps you are likely to meet.**

| Map | What it shows | The question it answers for a team |
|---|---|---|
| **Capability map** | What the business does, as stable abilities ("take a payment", "notify a merchant") | Which business ability does our idea serve? |
| **Application portfolio** | Every application, with owner, capabilities supported, health and future | Does something already do this? |
| **Technology standards** | The technologies the company prefers, accepts or is leaving | Which choices are already made for us? |
| **Investment portfolio** | What is funded this year, grouped by investment theme | Which goal and budget does our work belong to? |

A **capability** is something the business is able to do, described by *what*, not *how* or *who*. "Notify a merchant" is a capability; "the SMS service" is an application that supports it; the Merchant Orders team owns that application. Capabilities change slowly and applications and teams often, so start with the capability map.

**What the maps look like at Qafila.** Part of Qafila's capability map, with the applications behind each capability (illustrative):

| Capability (level 1) | Capability (level 2) | Applications today | Owner teams |
|---|---|---|---|
| Customer contact | Notify a merchant | Order updates service; support desk notices | Merchant Orders; Support |
| Customer contact | Notify a courier | Courier alerts service | Courier Experience |
| Payments | Take a payment | Payments service; payments partner integration | Payments |
| Payments | Pay couriers | Courier payouts service | Courier Payouts |
| Delivery | Plan a route | Routing service | Routing |

Yasmin's receipts belong under "Notify a merchant", which already has two applications.

**Reading the application portfolio.** Each row records the owner, capabilities, data held (with its sensitivity level from lesson 9.2), suppliers, cost (lesson 10.2), and two judgements: how well it serves the business, and how healthy it is technically. Many companies then sort applications into four groups from those two judgements:

| Business fit | Technical health | What usually happens |
|---|---|---|
| Good | Good | **Invest:** build on it; new needs go here first |
| Poor | Good | **Keep as is:** run it, but do not add to it |
| Good | Poor | **Replace or modernise:** move its work to something healthier (lesson 9.3) |
| Poor | Poor | **Retire:** plan its end |

**The memorable rule.** Check the map before you build.

### 🟡 Going deeper

**Technology standards as a radar.** Many companies publish their technology standards as a **technology radar**: rings that say how much the company trusts each technology. The format was made popular by the consultancy Thoughtworks, whose radar uses four rings (adopt, trial, assess, hold) and which encourages companies to build their own. In plain words:

| Ring (Thoughtworks' word) | Plain meaning for a team |
|---|---|
| **Adopt** | The default. Use it without asking. |
| **Trial** | Allowed for real work, with care; tell the platform team so they learn with you |
| **Assess** | Worth exploring in a spike or prototype, not yet in production |
| **Hold** | Do not start anything new with it; existing uses may continue while they are moved |

At Qafila the platform team (lesson 8.3) keeps the radar. The Courier Experience team's messaging supplier is on **hold**: its contract ends next year and everyone is to move to one supplier.

**The investment portfolio, seen from a team.** Bilal and the leadership group group spending (lesson 10.1) into a few **investment themes**: the year's broad goals, each with a share of the budget (illustrative):

| Theme | What it means | Share of change budget |
|---|---|---|
| **Merchant growth in the new countries** | Win and keep merchants in the two newest countries | About 35% |
| **Payments and trust** | Payments partner, fraud, security and audit work | About 25% |
| **Cost to serve** | Lower cost per delivery, including retiring duplicates | About 20% |
| **Keep the lights on** | Upgrades, patches, renewals, reliability | About 20% |

From a team, the theme tells you what your work will be judged on. Yasmin's receipts could fit "merchant growth" (merchants asked for them) or "payments and trust" (receipts reduce disputes). Choose honestly: the theme follows the outcome and its measure. For the manager's view of how a strategy becomes a portfolio, see [*Running IT as a Business*, lesson 3.1 — From strategy to an investment portfolio](../itbiz/index.html#/3.1).

**Who does architecture at Qafila.** A small architecture group keeps the maps current and runs a weekly open session where any team can bring a proposal. Under the decision rights from lesson 11.1, teams decide inside their own area; the group decides only what crosses areas, such as a new supplier for a shared capability.

### 🔴 Expert view

**A fit check, not a gate.** The most useful thing you can bring to an architecture conversation is a page that answers the shared questions before anyone asks. A **fit check** has six parts:

1. **The need.** One sentence, as an outcome (lesson 1.1): who will do what differently.
2. **Capability.** Where it sits on the capability map.
3. **What exists.** The applications that already support that capability, their owners, and their group (invest, keep, replace, retire).
4. **Standards.** The technology choices it needs, and where each sits on the radar.
5. **Theme.** The investment theme it serves, and the measure that theme is judged on.
6. **Recommendation.** One of four: **reuse** what exists, **extend** what exists, **build** something new (with the reason), or **stop**.

It comes before a business case (lesson 10.1) or decision record (lesson 9.1).

**When the map is wrong.** Maps decay. The portfolio may list a service that was switched off, or miss a tool a team bought with a card. Tell the row's owner and get it fixed: a map that teams correct is a map teams trust.

**When architecture becomes a gate.** Architecture helps when it is quick, visible and close to the work. It hurts when proposals wait weeks for a board or every decision goes up instead of only those that cross areas. If you see these signs, do not go around architecture. Bring a fit check, ask for a decision by a date, and say what waiting costs. For the manager's view of architecture runway and non-functional requirements, see [*Running IT as a Business*, lesson 4.3 — Architecture, non-functional requirements and the runway](../itbiz/index.html#/4.3).

**Stopping is a decision too.** A fit check that ends in "stop" is a success: a retired duplicate saves cost and risk every month after. For how portfolios stop work, see [*Running IT as a Business*, lesson 3.3 — Portfolio governance: reviewing, re-planning and stopping work](../itbiz/index.html#/3.3).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Capability map** | Stable business abilities in two levels, with applications and owners | Before proposing any new service or tool |
| **Application portfolio entry** | Owner, capabilities, data, suppliers, cost, business fit, technical health, group | When you build, buy, change or retire an application |
| **Technology radar** | Technology choices in rings, each with a reason and a contact | When a design needs a new technology |
| **Investment theme list** | The year's themes with goal, budget share and measure | When writing a proposal or roadmap item |
| **Fit check** | One page: need, capability, what exists, standards, theme, recommendation (reuse, extend, build, stop) | Before a business case or decision record |

Many companies keep these maps in a wiki or spreadsheet; the habit matters more than the tool.

## 🏛️ In practice at Qafila
Yasmin's fit check for merchant payment receipts, after she found the three existing routes (two for merchants). Illustrative and fictional.

> **Fit check: payment receipts by message**
>
> **Need.** Merchants in the two newest countries get a receipt message within a minute of every in-app payment, so payment-confirmation calls to support halve within a quarter (baseline: about 600 a month, from the support desk).
>
> **Capability.** Customer contact → Notify a merchant.
>
> **What exists.** Order updates service (Merchant Orders team; invest: healthy, widely used, supplier A). Support desk notices (Support; keep as is: fine for manual notices, not built for events). Related: courier alerts service (Courier Experience team; serves "Notify a courier"; replace, since supplier B is on hold).
>
> **Standards.** Event stream: adopt. Messaging supplier A: adopt. Supplier B: hold. No new database needed.
>
> **Theme.** Merchant growth in the new countries (measure: merchant retention and support contacts per merchant). Secondary: cost to serve, if courier alerts move to the same service later.
>
> **Recommendation.** **Extend** the order updates service with a payment-receipt message, owned by Merchant Orders, with Payments publishing the payment event. Raise with the architecture group: move courier alerts to the same service before supplier B's contract ends.

The architecture session took twenty minutes. The Merchant Orders lead agreed to own the new message type if Payments wrote the first version in their repository, with their review. The portfolio still listed a messaging tool switched off a year earlier, so Faisal asked Yasmin to tell that row's owner, who removed it. The receipts shipped in three weeks instead of the two months a new service would have taken.

Yasmin's mistake: her first draft placed the work under "payments and trust" because that theme had more money left. Aisha pointed out that the measure, merchants' support calls, belongs to merchant growth.

## 🛠️ Exercises
**🟢 Place three ideas on the map.** Using Qafila's capability map above, place each idea at level 2 and list the applications already supporting it: (a) couriers see their weekly earnings in the app; (b) merchants get an alert when a courier is more than ten minutes late; (c) better routes for couriers carrying both food and medicine.
*Done when:* each idea has one level-2 capability, the existing applications are named, and you have said for each whether a new application would be the third (or more) for that capability.

<details><summary>Model answer and self-check</summary>

**Model answer.** (a) Payments → Pay couriers; existing: courier payouts service; a new application would be the second, not the third, so extend it. (b) Customer contact → Notify a merchant; existing: order updates service and support desk notices; a new service would be the third, so extend order updates. (c) Delivery → Plan a route; existing: routing service; a new application would be the second, not the third, so extend it with a rule for mixed loads.

**Self-check.**
- Did you name capabilities by what the business does, not by system or team?
- For (b), did you notice it is the same capability as Yasmin's receipts?

</details>

**🟡 Write an application portfolio entry.** Pick one application you know (at work, in an open-source project, or Qafila's courier alerts service). Write its entry with every toolkit field and place it in one of the four groups.
*Done when:* every field is filled or marked "unknown, ask X", business fit and technical health each have a one-line reason, and the group follows from those two judgements.

<details><summary>Model answer and self-check</summary>

**Model answer.** Courier alerts service. Owner: Courier Experience team. Capability: Notify a courier. Users: active couriers. Data: courier phone numbers (confidential). Supplier: B (on hold). Cost: unknown, ask Bilal's team. Business fit: good, couriers rely on alerts. Technical health: poor, no tests on retry logic and a supplier on hold. Group: replace; move alerts to the order updates service (as proposed in Yasmin's fit check) before supplier B's contract ends.

**Self-check.**
- Does the group follow from the two judgements, not from your opinion of the team?
- Did you name the data and its sensitivity?
- Did you write "unknown" with a person to ask, instead of guessing a cost?

</details>

**🔴 Write a fit check.** Write one for idea (b) above (late-courier alerts) or a real proposal of your own, with all six parts and one of the four recommendations.
*Done when:* the need is an outcome with a measure, the capability and existing applications are named, each technology choice has a radar ring, the theme matches the measure, and the recommendation follows from the rest of the page.

<details><summary>Model answer and self-check</summary>

**Model answer.** Need: merchants know when a courier will be late, so late-pickup calls to support fall by a third. Capability: Notify a merchant. Existing: order updates service (invest), support desk notices (keep as is). Standards: event stream and supplier A (adopt); a new "estimated delay" event from Routing (needs their agreement). Theme: merchant growth. Recommendation: extend the order updates service; no new service.

**Self-check.**
- Did you pick the theme from the measure, not the money?
- If you recommended "build", did you give a reason the existing applications cannot be extended?

</details>

## ⚠️ Mistakes and traps
- **Building before looking.** A duplicate service adds cost and risk for years.
- **Naming capabilities after systems or teams.** "The SMS service" is not a capability; "Notify a merchant" is.
- **Choosing the investment theme by budget left.** The theme follows the outcome and its measure. A mismatch shows up at the year-end review.
- **Going around architecture.** It repeats the duplication architecture exists to prevent. Bring a fit check instead.

## 🧾 Recap
- Four maps matter to a team: capability map, application portfolio, technology standards (often a radar), investment portfolio with themes.
- A capability is what the business can do, named without systems or teams; start there.
- A fit check answers the shared questions before anyone asks: need, capability, what exists, standards, theme, recommendation.
- Rule: check the map before you build.

## ✍️ Check yourself
**1. Which of these is a capability, in the sense this lesson uses?**

- A. The order updates service that sends merchant messages
- B. Notify a merchant about an event that concerns them
- C. The Merchant Orders team and the suppliers it uses
- D. Messaging supplier A and its contract with Qafila

<details><summary>Answer</summary>

**B.** A capability is named by what the business does, not how or who. A is an application, C an owner team, D a supplier. See "Four maps you are likely to meet".

</details>

**2. Yasmin and her colleagues want to build a new service to send payment receipts. The capability map shows two applications already supporting "Notify a merchant". What should she do first?**

- A. Build the new service quickly, then ask the architecture group to add it to the map.
- B. Ask the architecture group to approve a new service before any design work starts.
- C. Pick the messaging supplier with the lowest price, since cost is the main concern.
- D. Check the two existing applications and whether one can be extended to do the job.

<details><summary>Answer</summary>

**D.** A third application for one capability needs a reason; first see whether an existing one can be extended. A adds duplication, B hands over work the team can prepare itself, and C skips what exists. See "A fit check, not a gate".

</details>

**3. On Qafila's technology radar, messaging supplier B is in the "hold" ring. What does that mean for a new piece of work?**

- A. Do not start anything new with it; existing uses may continue while they move.
- B. It may be used for real work with care, as long as the platform team is told.
- C. It may be explored in a prototype or spike, but not yet used in production.
- D. It is the default choice and may be used without asking anyone for approval.

<details><summary>Answer</summary>

**A.** B describes trial, C assess, and D adopt. See "Technology standards as a radar".

</details>

**4. Yasmin first placed the receipts work under "payments and trust" because that theme had more budget left. Its measure is fewer merchant calls to support. What is the right theme?**

- A. Payments and trust, because the work involves payment events and that theme has money.
- B. Keep the lights on, because sending messages is routine work that every product does.
- C. Merchant growth, because the outcome and its measure are about merchants' support calls.
- D. Cost to serve, because any reduction in support calls will lower the cost per delivery.

<details><summary>Answer</summary>

**C.** The theme follows the outcome and its measure, not the budget left. A is Yasmin's mistake; B mislabels new work as run work; D is tempting, but the stated measure belongs to merchant growth. See "The investment portfolio, seen from a team".

</details>

**5. Yasmin finds that the application portfolio lists a messaging tool that was switched off a year ago. What should she do?**

- A. Raise it at the next weekly architecture session and leave the row as it is until then.
- B. Tell the row's owner and get it corrected, since teams rely on the map being true.
- C. Add a note about the switched-off tool on her own team's wiki page so her team knows.
- D. Edit the row herself, since she has access to the portfolio and knows it is wrong.

<details><summary>Answer</summary>

**B.** Maps decay; trust depends on people correcting them through the row's owner, who may know more (for example, a replacement in progress). A leaves the wrong row in place for no reason, C fixes only her own team's picture, and D bypasses the owner. See "When the map is wrong".

</details>

## 📚 References
Both Thoughtworks pages were opened on 22 November 2026.
- Thoughtworks, "Technology Radar FAQ" (the four rings): https://www.thoughtworks.com/radar/faq
- Thoughtworks, "Build your own Technology Radar": https://www.thoughtworks.com/insights/blog/build-your-own-technology-radar
- Library course: [*Running IT as a Business*, lesson 3.1 — From strategy to an investment portfolio](../itbiz/index.html#/3.1)
- Library course: [*Running IT as a Business*, lesson 3.3 — Portfolio governance: reviewing, re-planning and stopping work](../itbiz/index.html#/3.3)
- Library course: [*Running IT as a Business*, lesson 4.3 — Architecture, non-functional requirements and the runway](../itbiz/index.html#/4.3)

---

# 12.2 — AI in digital work: using it well, with controls
*Level: 🔴 Advanced* · *Prerequisites: 3.1, 9.2, 11.2* · *Step: Govern, Collaborate*

**After this you can** sort AI-assisted tasks by risk, choose the check each needs, decide which data may go into which tool, and write a one-page AI use card naming tools, data limits, checks and who is accountable for each output. *Study time: reading about 20 min, hands-on about 80 min (estimate).*

## ⚡ In 60 seconds
- AI assistants now help with almost every step of digital work.
- Research so far is mixed: very wide reported use, uneven gains, and a link between more AI use and less stable delivery.
- The rule that matters most: **the AI drafts; a named person decides, and checks in proportion to the risk.**
- Three controls cover most everyday use: **approved tools by data level**, **checks sized to risk**, and **a named owner for every output** that leaves your hands.
- Decision cue: before pasting, ask "what data is this, and is this tool approved for it?"
- Biggest trap: fluent output that looks finished. Plausible is not correct.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

By Established, almost everyone at Qafila used AI tools daily: engineers a coding assistant, Salma's support agents the support desk tool's built-in assistant, Hamad's analysts a chat assistant. Nobody had written down any limits, because each use had started small.

Then, in one month, a newer engineer on Yasmin's team, Courier Payouts, asked the coding assistant to change how payouts were rounded for the newest country's currency. The assistant wrote the change and the tests, and every test passed. Yasmin, asked to review it as a payments domain reviewer, saw that the tests had been written from the new code, not from the payout rules. The rounding was wrong by one decimal place; in production it would have underpaid thousands of couriers a little every week.

The same month, a support agent pasted a merchant's dispute, with the customer's name, phone number and last card digits, into a free public chatbot on a personal account to get a better translation. The payments partner's questionnaire (Module 11) had asked: "Where can staff send customer data?" The honest answer was now "we do not fully know."

Maha asked Dana and Faisal for something short everyone could follow; this lesson is what they wrote.

## 📐 How it works

### 🟢 The essentials

**What AI assistants are.** They are built on **large language models** (LLMs): programs trained on very large amounts of text to predict likely next words. That makes them good at fluent text and code in the shape you ask for, and unreliable about whether it is true. They can invent a function, a package or a source with the same confidence as a real one.

**What the evidence says so far.** Findings are recent, mixed and about specific groups.

| Source | What it reports | For whom, and the caution |
|---|---|---|
| 2024 DORA report (Google Cloud's research programme on software delivery) | A 25% increase in AI adoption was associated with gains such as a 3.1% increase in code review speed; as adoption increased, delivery throughput fell an estimated 1.5% and delivery stability an estimated 7.2% | Survey data; associations, not proof of cause |
| 2025 DORA report on AI-assisted software development | 90% of survey respondents reported using AI at work; "AI doesn't fix a team; it amplifies what's already there" | Nearly 5,000 technology professionals; self-reported |
| METR study, July 2025 | In a randomised trial, 16 experienced open-source developers took about 19% longer on tasks where AI tools were allowed, while believing they had been faster | Experienced developers on projects they knew well; the authors warn against generalising, and in February 2026 METR marked these results out of date, saying developers were likely sped up more by early 2026 tools but that its new data was weak evidence |

The fair reading: gains are not automatic, and depend on the basics this course has taught: small changes, good tests, review and fast feedback.

**The three everyday controls.**

1. **Approved tools by data level.** Each AI tool is approved up to one of the sensitivity levels from lesson 9.2, depending on the supplier contract: where data goes, whether it is kept or used for training. A free public chatbot on a personal account is approved for no company data.
2. **Checks sized to risk.** A note to a colleague needs a read; payout code needs tests written from the rules and a domain reviewer. The more harm a wrong output could do, the stronger the independent check.
3. **A named owner for every output.** Whoever sends, merges or publishes AI-assisted work owns it as if they had written it. "The AI wrote it" is never an explanation.

**The memorable rule.** The AI drafts; a named person decides, and checks in proportion to the risk.

### 🟡 Going deeper

**Sorting tasks by risk.** Ask: how much harm could a wrong output do, and how easily is it noticed and undone?

| | Easy to notice and undo | Hard to notice or undo |
|---|---|---|
| **Low harm** | Read and use (notes, a commit message) | Read carefully; check facts (a summary others rely on) |
| **High harm** | Independent check before use (a query feeding a decision, a draft reply about money checked before sending) | Tests from the source of truth plus a second person (payout code, security settings, anything already sent to customers) |

A message sent to a customer cannot be recalled, so the check must happen on the draft.

The rounding change sits bottom right. The dispute translation was high harm twice over: a wrong translation misleads, and the data went where nobody could take it back.

**Checks that actually catch AI mistakes.** Reading is weak, because fluent text persuades. Stronger checks:

- **Tests written from the rules, not from the code.** Write expected results from the requirement (lesson 6.2) before reading generated code; if the AI wrote the tests, a person checks each expected result against the rule. See [*Software Testing: Zero to Hero in the AI Era*, lesson 6.1 — Verifying AI-generated code: how coding agents fail and a reviewer's checklist](../testing/index.html#/6.1).
- **Compare with a source.** Open the source for every fact or figure; if there is none, leave it out.
- **Run it small first.** A small known dataset for a query; a feature flag for a change (lesson 3.3).
- **Check names exist.** Confirm every new dependency an assistant suggests is the real, established package and is approved (lesson 11.2); [*Secure AI & Application Security: Zero to Hero*, lesson 6.3 — Securing AI-generated code: what coding agents get wrong](../secai/index.html#/6.3) explains invented package names and why they are an attack route.

**AI inside the product is different.** When AI becomes part of what Qafila offers customers (an assistant answering courier questions, say), it also needs product-level controls: an evaluation set run on every change, limits on what it can do, monitoring and an incident route. Its security has its own risks, such as prompt injection, where crafted text steers the model against its instructions. The *Building AI Applications & Agents* and *Secure AI & Application Security* courses (lesson 12.3) go deep on both.

**Rules that may apply.** AI use can touch data protection, consumer protection, sector rules, employment rules and, in some countries, AI-specific laws. They differ by country; this course will not say which apply. Bring legal or compliance a precise question: which tool, which data fields, which customers, and what they are told.

### 🔴 Expert view

**Write down the limits where people work.** Dana and Faisal wrote no long policy, but a one-page **AI use card** per team, linked from its working agreement (lesson 3.1), and a company **AI use register** of approved tools, their uses and owners. For the bigger picture, risk colleagues may use the NIST AI Risk Management Framework, a voluntary US framework published in January 2023; see [*AI Governance: Zero to Hero*, lesson 7.1 — OECD principles and the NIST AI RMF](../aigp/index.html#/7.1).

**Keep your own skill.** If an assistant does every hard part, you stop learning it and lose the ability to tell when it is wrong. Write the first attempt yourself on tasks you are learning, then compare; explain generated code before merging it.

**Measure the work, not the tool.** "AI wrote 40% of our code" says nothing about value or safety. Keep measuring change lead time, change fail rate and failed deployment recovery time (lesson 3.3), bugs customers report after release, and cost per delivery (lesson 10.2). If the change fail rate rises, look at how AI-assisted changes are reviewed.

**Disclosure.** Say when AI helped, where it matters: in a pull request ("tests drafted with the assistant; expected results checked against the payout rules by me") and wherever company rules require it. It tells the reviewer where to look harder.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **AI use card** | One page: approved tools, data limits, risk boxes with checks, output owners, disclosure | When a team starts using AI tools; at each working-agreement review |
| **AI use register** | Approved AI tools with supplier, data levels, uses, owner, review date | Before using any new AI tool for work |
| **Risk box** | Harm if wrong × easy to notice and undo, each box with a minimum check | Before relying on any AI output |
| **Rules-first test list** | Expected results written from the requirement first | High-harm AI-assisted changes |
| **Paste check** | What data is this, which level, is this tool approved for it? | Every time, before pasting |

Tool categories only; none is endorsed.

## 🏛️ In practice at Qafila
The AI use card Yasmin wrote with her team after the rounding review, using Dana's template. Illustrative and fictional.

> **AI use card: Courier Payouts team**
>
> **Approved tools.** Company coding assistant (up to "confidential"). Company chat assistant (up to "internal"). No personal accounts.
>
> **Never paste.** Card data, partner credentials, customer payment details ("restricted"), unmasked production logs.
>
> **Risk boxes for our work.**
> - *Low harm, easy to undo:* commit messages, notes. Read and use.
> - *Low harm, hard to notice:* docs others rely on. Check facts against the source.
> - *High harm, easy to undo:* queries feeding decisions, drafts of payment support replies. Second person checks before use or sending.
> - *High harm, hard to undo:* payment, payout, refund and fee code; security settings; migrations. Rules-first tests checked by a person; domain reviewer; feature flag on first release.
>
> **Ownership.** The pull request author owns everything in it; the reviewer owns the review.
>
> **Disclosure.** Pull requests say what was AI-drafted and what the author checked by hand.
>
> **Learning.** First-year engineers write payment logic themselves first, then compare.
>
> **Review.** Quarterly with the working agreement, and after any AI-related incident.

Salma fixed the support side. The support desk's built-in assistant, covered by Qafila's supplier contract, was approved up to "confidential", so agents could translate inside the tool once card digits were removed. Dana logged the incident in the risk register (lesson 11.2), and Qafila told the payments partner what had happened and what had changed.

Faisal's first instinct had been to ban AI tools near payments. Yasmin argued that a ban would push people to personal accounts, the worst outcome.

## 🛠️ Exercises
**🟢 Sort ten tasks into the risk boxes.** List ten tasks you have used, or might use, an AI tool for. Place each in a risk box and write its minimum check. Include at least one task where the data you would paste, not the output, is the risk.
*Done when:* all ten tasks are placed, each box's check matches the table in "Sorting tasks by risk", at least two tasks sit in the high-harm row, and one task names its data risk and the paste check.

<details><summary>Model answer and self-check</summary>

**Model answer.** Summarise my notes, draft a commit message (low, easy: read). A README others follow, a meeting summary (low, hard: check every command and fact). A query feeding a report, a draft refund reply checked before sending (high, easy: known data, second person). Authentication code, a database migration, cloud security settings (high, hard: tests from the rules, domain reviewer). Translating a merchant dispute that contains personal data (high, hard to undo once sent; data risk: the dispute is confidential and card digits restricted, so card digits removed first, approved tool only, a second person checks the reply).

**Self-check.**
- Did you judge harm by the cost of a wrong output, not the task's difficulty?
- Are your high-harm checks independent of the AI?
- Does your data-risk task name the data level and an approved tool?

</details>

**🟡 Find the weak test.** The rule: "courier fees in currency Q are rounded to three decimal places; half rounds up". An AI-drafted function rounds to two places, and its test asserts `round_fee(1.2345)` returns `1.23`. Explain what went wrong, write expected results from the rule for three cases (one a half), and say how review should have caught it.
*Done when:* you name the cause (test derived from the code, not the rule), give three expected results that follow the stated rule, and propose one process change.

<details><summary>Model answer and self-check</summary>

**Model answer.** The test checks that the code does what it does; both share one misunderstanding. From the rule, computed with decimal arithmetic: `round_fee(1.2345)` → `1.235` (an exact half rounds up); `round_fee(2.0004)` → `2.000`; `round_fee(0.1236)` → `0.124`. Money should never use binary floating point: in Python, `round(1.2345, 3)` gives `1.234`, because the float stored is slightly below 1.2345. Use a decimal type with an explicit half-up rounding mode; a rules-first test catches this too. Process change: for payout or fee logic, a person writes expected results from the rule before reading generated code, and the pull request says where each came from.

**Self-check.**
- Did your expected values follow the rule exactly, including the half case?
- Would your process change still work if no AI were involved?

</details>

**🔴 Write an AI use card.** Write one for yourself or a team you know (a study group, an open-source project, a workplace team, or Qafila's Support team), with every section of the Courier Payouts card.
*Done when:* the card fits on one page, names real tool categories (not brands as endorsements), has a never-paste list tied to data levels, gives each risk box a check, names who owns outputs, and has a review date.

<details><summary>Model answer and self-check</summary>

**Model answer.** Qafila's Support team. Tools: the support desk's built-in assistant (up to confidential), the company chat assistant (up to internal). Never paste: card data or payment details (restricted). Risk boxes: notes (read); knowledge-base drafts (second agent reads); draft replies about money (check every fact against the order record before sending); messages to many merchants (team lead approves). Ownership: the sender owns the reply. Disclosure: the company's customer-communication rule. Learning: new agents write their first twenty replies unaided. Review: quarterly.

**Self-check.**
- Is every never-paste item tied to a data level from lesson 9.2?
- Could a new joiner follow it on day one?

</details>

## ⚠️ Mistakes and traps
- **Trusting fluency.** Check high-harm output against rules, sources or tests, not against how it reads.
- **Letting the AI write both code and tests unchecked.** They share one misunderstanding. Check expected results against the requirement.
- **Banning tools outright.** Bans push people to personal accounts. Approve tools by data level instead.
- **Pasting first, thinking later.** Data sent to an unapproved tool cannot be recalled. Run the paste check.
- **Stopping learning.** Use AI to go faster at what you understand, not to skip learning.

## 🧾 Recap
- Published evidence is mixed: very wide use, uneven gains, and a link with less stable delivery.
- Three everyday controls: approved tools by data level, checks sized to risk, a named owner for every output.
- The risk box (harm if wrong, ease of noticing and undoing) tells you how much checking a task needs.
- Rule: the AI drafts; a named person decides, and checks in proportion to the risk.

## ✍️ Check yourself
**1. In the rounding case, every test passed, yet the change was wrong. What was the underlying problem?**

- A. The coding assistant was not approved for confidential data at Qafila.
- B. The engineer should have used a different and more capable AI model.
- C. The tests were derived from the generated code rather than from the rules.
- D. The change was too small to need a review by someone outside the team.

<details><summary>Answer</summary>

**C.** Tests that check the code does what it does cannot catch a misread rule. A is about which data goes into the tool, not whether the tests check the rule; B assumes a better model removes checks, and D gets review backwards. See "Checks that actually catch AI mistakes".

</details>

**2. A support agent wants a better translation of a merchant dispute that includes a customer's name, phone number and card digits. What should she do?**

- A. Remove the card digits, then use the support desk's approved assistant.
- B. Use a free public chatbot, but delete the conversation afterwards to be safe.
- C. Remove the merchant's name only, then use whichever chatbot translates best.
- D. Ask a colleague to paste it into their own personal account instead of hers.

<details><summary>Answer</summary>

**A.** Card digits are restricted and go nowhere; the rest is confidential, which the support desk's assistant is approved for. B and D send customer data to unapproved tools (deleting a chat recalls nothing). C keeps the card digits and uses an unapproved tool. See "The three everyday controls" and "In practice at Qafila".

</details>

**3. Faisal proposes banning AI tools for all work that touches payments. Why did the team prefer an AI use card?**

- A. Because bans are not allowed under the payments partner's questionnaire.
- B. Because a ban would breach the terms of the coding assistant's supplier contract.
- C. Because the card removes the need for human review of payment changes.
- D. Because bans push people to personal accounts, the least controlled option.

<details><summary>Answer</summary>

**D.** A ban moves use out of sight; approved tools with checks keep it visible. A and B invent rules the lesson never mentions, and C contradicts the card. See "In practice at Qafila".

</details>

**4. Hamad's analyst used an assistant to draft a query whose result will go into a pricing decision. The query is easy to rerun and fix. Which check fits the risk box?**

- A. Read the query once, since queries are low harm and easy to fix afterwards.
- B. Run it on known data and have a second person check it before the decision.
- C. Ask the same assistant whether its own query is correct before using it.
- D. No check is needed if the query runs without errors on production data.

<details><summary>Answer</summary>

**B.** A number feeding a decision is high harm. A under-rates the harm, C is not independent, and D confuses "runs" with "correct". See "Sorting tasks by risk".

</details>

**5. A team lead wants to report that "AI now writes 40% of our code" as evidence the tools are working. What is the better measure?**

- A. Delivery measures such as change lead time, change fail rate and customer-found bugs.
- B. The number of AI tool licences bought for the team over the past quarter.
- C. The share of engineers who say they feel faster when using the AI tools.
- D. The number of lines of code merged each week, compared with last year.

<details><summary>Answer</summary>

**A.** The tools help if the work gets better. B and D measure inputs or volume; C is tempting, but the METR study reported developers felt faster while being slower. See "Measure the work, not the tool".

</details>

## 📚 References
All sources below were opened on 22 November 2026.
- Google Cloud blog, "Announcing the 2024 DORA report", 22 October 2024: https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
- Google Cloud blog, "Announcing the 2025 DORA report", 23 September 2025: https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report
- METR, "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity", 10 July 2025: https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ (paper: https://arxiv.org/abs/2507.09089)
- METR, "We are Changing our Developer Productivity Experiment Design", 24 February 2026: https://metr.org/blog/2026-02-24-uplift-update/
- OWASP GenAI Security Project, Top 10 for LLM Applications 2025: https://genai.owasp.org/
- NIST, AI RMF 1.0 (NIST AI 100-1), January 2023 (as cited in the library's *AI Governance* course): https://doi.org/10.6028/NIST.AI.100-1
- Library course: [*Secure AI & Application Security: Zero to Hero*, lesson 6.3 — Securing AI-generated code: what coding agents get wrong](../secai/index.html#/6.3)
- Library course: [*Software Testing: Zero to Hero in the AI Era*, lesson 6.1 — Verifying AI-generated code: how coding agents fail and a reviewer's checklist](../testing/index.html#/6.1)
- Library course: [*A Practical Guide to Becoming an AI-Native Engineer*](../ainative/index.html), lessons 12.1 (team practice) and 13.1 (avoiding deskilling)

---

# 12.3 — Frameworks, bodies of knowledge and your learning path
*Level: 🔴 Advanced* · *Prerequisites: 0.3* · *Step: Govern, Collaborate*

**After this you can** say in one line what each well-known framework is for and who owns it, decide whether a certification is worth your time for a stated goal, and write a one-page learning plan for the next twelve months. *Study time: reading about 20 min, hands-on about 85 min (estimate).*

## ⚡ In 60 seconds
- At work you will hear many framework names (Scrum, ITIL®, COBIT®, TOGAF®, SAFe® and more). Each is one owner's answer to one kind of question, often with a certification scheme.
- This course is written from general practice in its own words; it is not based on any of them and is not training for any exam.
- The rule that matters most: **learn the idea, then the vocabulary.**
- Decision cue: take a certification when a role or contract you want asks for it, or for structured study; never instead of practice.
- Your next step is a learning plan: one **home practice** to go deep in, one **adjacent practice**, and projects that leave evidence.
- Biggest trap: collecting certificates instead of artefacts and experience.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

At her yearly review, Yasmin's manager asked where she wanted to go next. She had three ideas and no plan. She enjoyed being Courier Payouts' security champion (lesson 11.2). She had liked seeing the whole map while writing the fit check in lesson 12.1. And a recruiter had sent her a delivery-lead role asking for "a scaled agile certification".

Meanwhile Salma, now the service and reliability lead, interviewed a candidate with four service management certificates who could not describe his first hour in an outage, and a graduate with none who walked her through a post-incident review she had written for a student project. Salma hired the graduate.

Neither story means certificates are useless. Names and badges are easy to collect and hard to judge; practice is the other way round.

## 📐 How it works

### 🟢 The essentials

**What these things are.** "Framework" covers several kinds of published guidance, and the kind tells you how to use it: **guidance** (practices you adapt in your company's words), a **certifiable standard** (requirements an organisation is audited against, followed exactly where it certifies), a **body of knowledge** (a structured description of what a profession knows, for study), a **scaling framework** (ready-made structures for coordinating many teams) and **research** (findings such as the DORA reports, to inform choices).

Most are owned by an organisation that protects the name with a trademark and runs or licenses training and certification. That is legitimate; it also means you name them accurately and do not copy their content without checking the owner's terms.

**The names you are likely to meet.** Owners and editions are as reported (November 2026); versions change, so check the owner's page.

| Name | Owner | What it is for, in one line |
|---|---|---|
| **Scrum** | Described in *The Scrum Guide* by Ken Schwaber and Jeff Sutherland, freely licensed under Creative Commons (CC BY-SA 4.0) | A lightweight way for one team to deliver in short, fixed iterations with regular review and adjustment |
| **Kanban** (for knowledge work) | No single owner | Making work visible and limiting work in progress |
| **ITIL®** | PeopleCert | Guidance on designing, delivering, supporting and improving IT-enabled services |
| **COBIT®** | ISACA | Guidance for boards and managers on who decides about technology, and how it is controlled and measured |
| **TOGAF®** | The Open Group | A method and framework for enterprise architecture |
| **SAFe®** | Scaled Agile, Inc. | A framework for running lean and agile delivery across many teams and a portfolio |
| **PMBOK® Guide** | Project Management Institute (PMI); an eighth edition was reported published in 2025 | Principles and practices of project management |
| **BABOK® Guide** | International Institute of Business Analysis (IIBA); version 3 reported released in 2015 | A body of knowledge for business analysis |
| **SWEBOK Guide** | IEEE Computer Society; version 4.0 released in 2024, free to download for individual, non-commercial use | A body of knowledge for software engineering |
| **FinOps Framework** | FinOps Foundation (part of the Linux Foundation) | Practices for managing cloud and wider technology spending |
| **The Open Group IT4IT™ Standard** | The Open Group | A model of the data and tools an IT department needs to run its own work end to end |
| **VeriSM™** | IFDC (International Foundation for Digital Competences) | An approach to service management for digital organisations |
| **DORA research** | DORA, a research programme now part of Google Cloud | Yearly research on software delivery performance and the capabilities linked to it |

One more name you may meet: **The Open Group Digital Practitioner Body of Knowledge™ Standard**. It is a standard published by The Open Group for people who work on digital products and services. DPBoK is a trademark of The Open Group. This course is not based on it, does not cover it and does not prepare anyone for its certification; for what it contains, see The Open Group's own page, listed in References.

For a manager's way of choosing among frameworks, see [*Running IT as a Business*, lesson 12.1 — The frameworks landscape: what each is for, and how to use them without becoming their servant](../itbiz/index.html#/12.1).

**The memorable rule.** Learn the idea, then the vocabulary.

### 🟡 Going deeper

**Working inside a company's framework.** Most companies mix adapted parts of several frameworks. You will be more useful if you:

- **Learn the local words.** If your company says "sprint" or "CAB", use those words, and know the ideas behind them.
- **Ask what a practice protects.** "What goes wrong if we skip this?" If nobody knows, raise it gently.
- **Do not import a framework to win an argument.** Explain the problem and the outcome you want instead.
- **Respect the owner's terms.** Ask who has checked the licence before copying framework text or diagrams into templates.

**Certifications: when they are worth it.** A certification shows you studied a body of material and passed an assessment, not that you can do the work. It can be worth it when:

| Good reason | Weak reason |
|---|---|
| A job or contract you want requires it | Everyone on LinkedIn seems to have it |
| Your employer pays and you want structured study in that area | You hope it will replace practical experience |
| It is a recognised entry requirement in your country or sector | You want a quick win after finishing a course |

Before you start one, ask: who recognises it in the jobs I want, what it costs in money and hours (including renewal), and what I will be able to do afterwards. This course promises no certification, job or income. For certifications by role, see the career lessons in *Cloud & DevOps* ([7.2](../cloud/index.html#/7.2)) and *Secure AI & Application Security* ([12.2](../secai/index.html#/12.2)).

**Depth and breadth.** A useful practitioner is often called **T-shaped**: deep in one area (the vertical bar), with enough understanding of neighbouring areas to collaborate (the horizontal bar). This course has been the horizontal bar: discovery, design, building, delivery, operations, teams, money and governance, each well enough to take part. Your next step is the vertical bar.

### 🔴 Expert view

**Choosing a home practice.** Your **home practice** is the area you will go deep in for the next year or two. Choose it from evidence, not fashion. Look back through your artefacts and ask:

- Which lessons did I finish fastest and enjoy most?
- Which exercises did I redo or extend without being asked?
- Which kind of problem do people already bring to me?
- Which roles exist in the places I want to work? (*From Graduate to Hired*, [lesson 0.2](../career/index.html#/0.2), maps them.)

Then choose one **adjacent practice**: a neighbour your home practice depends on (operations for a backend engineer, product for a tester).

**Where the library goes deeper.** Where to start, by home practice:

- **Software engineering:** [*System Design for Vibe Coders*](../vibe/index.en.html), then [*A Practical Guide to Becoming an AI-Native Engineer*](../ainative/index.html).
- **SaaS products from shared parts** (login, billing, jobs): [*SaaS Building Blocks*](../saas/index.html).
- **Testing and quality:** [*Software Testing: Zero to Hero in the AI Era*](../testing/index.html).
- **Operations, cloud and platforms:** [*Cloud & DevOps: Zero to Hero*](../cloud/index.html).
- **Data and analytics:** [*Data Engineering & Analytics: Zero to Hero*](../data/index.html).
- **Security:** [*Secure AI & Application Security: Zero to Hero*](../secai/index.html).
- **Building AI features and agents:** [*Building AI Applications & Agents: Zero to Hero*](../aiapps/index.html).
- **Product management:** [*AI Product Management: Zero to Hero*](../aipm/index.html).
- **Governance and risk for AI:** [*AI Governance: Zero to Hero*](../aigp/index.html).
- **Management and operating models:** [*Running IT as a Business*](../itbiz/index.html).
- **Starting your own product:** [*Founder's Playbook for AI-First Builders*](../founder/index.html).
- **Finding your first role:** [*From Graduate to Hired*](../career/index.html).

**Evidence over completion.** What persuades is evidence you can show: an artefact, a project, a write-up, a contribution. Plan each quarter around one piece of evidence, not around finishing courses, and put review dates in your calendar. Your artefact folder from lesson 0.3 is the start; the capstone in lesson 13.1 turns it into one playbook. For presenting evidence and growing past junior, see *From Graduate to Hired*, lessons [3.2](../career/index.html#/3.2) and [6.3](../career/index.html#/6.3).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Framework note** | Name with its mark, owner, purpose in one line, where your company uses it, local words | When a framework name comes up at work or in an advert |
| **Certification check** | Who recognises it, what it costs (money, hours, renewal), what you can do afterwards | Before you sign up for any certification |
| **Home practice finder** | Four questions: artefacts, enjoyment, what people ask you, roles available | When choosing what to go deep in |
| **Learning plan (next twelve months)** | Home and adjacent practice, quarterly evidence, courses, mentor, limits, review dates | After this course; review quarterly |
| **Evidence log** | Dated list of artefacts, projects and feedback | Monthly; before reviews and interviews |

## 🏛️ In practice at Qafila
Yasmin's learning plan after her review, shared with her manager and with Dana as mentor. Illustrative and fictional.

> **Learning plan: Yasmin, next twelve months**
>
> **Home practice.** Application security. Evidence: threat modelling was my favourite work this year (lesson 11.2); teams already bring me access-control questions; Qafila has a path from champion to security engineer.
>
> **Adjacent practice.** Architecture: the fit check (lesson 12.1) showed me how security choices sit inside the capability map.
>
> **Quarterly evidence.**
> - Q1: threat models for three Payments changes, findings turned into tests.
> - Q2: a secure-by-default service template with the platform team (lesson 8.3).
> - Q3: lead the security part of one architecture decision record.
> - Q4: run a tabletop incident exercise with Salma's team: talking through an imagined incident step by step, without touching systems (lesson 4.3).
>
> **Library courses.** *Secure AI & Application Security*, one lesson a week; *Running IT as a Business*, lesson 4.3.
>
> **Certification.** One recognised application security certification in Q3, if Dana confirms the security engineer role values it. Not the scaled agile one from the recruiter's advert: no role I want asks for it.
>
> **Limits.** One course at a time. Evidence first, certificate second.
>
> **Reviews.** End of each quarter with my manager; monthly coffee with Dana.

## 🛠️ Exercises
**🟢 Write three framework notes.** Pick three framework names from this lesson or from job adverts. For each, write a note: name with its mark, owner (checked on the owner's own site), purpose in one line in your own words, and one related idea from this course.
*Done when:* three notes exist, each owner is confirmed on the owner's site, and each one-line purpose is in your own words, not copied.

<details><summary>Model answer and self-check</summary>

**Model answer.** Scrum: *The Scrum Guide* by Ken Schwaber and Jeff Sutherland, CC BY-SA 4.0; one team delivering in short iterations and adjusting; related idea, lesson 5.2. ITIL®: PeopleCert; guidance on running IT-enabled services; related idea, lesson 7.2. FinOps Framework: FinOps Foundation; managing cloud spending; related idea, lesson 10.2.

**Self-check.**
- Did you open the owner's own page?
- Did you avoid claiming that the course covers the framework?

</details>

**🟡 Run the certification check.** Choose one certification you have seen in an advert. Answer the three questions with real findings (adverts that ask for it; cost and renewal from the owner's site; what you could do afterwards), then decide: take it now, later, or skip it.
*Done when:* each question has an answer with a source or a "could not find", and the decision follows from the answers.

<details><summary>Model answer and self-check</summary>

**Model answer.** A cloud provider's associate-level certification. Recognised: several cloud-engineer adverts I found in my country mention it. Cost: exam fee, study hours and renewal terms from the provider's own pages. Afterwards: I could explain a basic multi-zone deployment. Decision: take it later, after one practice project, so the certificate confirms practice rather than replacing it.

**Self-check.**
- Did you include renewal and hours, not only the exam fee?
- Would your decision change if your employer paid?

</details>

**🔴 Write your learning plan.** Using the home practice finder and Yasmin's plan as a model, write your plan for the next twelve months: home practice with evidence, adjacent practice with a reason, one evidence goal per quarter, library courses, a certification decision (including "none"), three limits and review dates.
*Done when:* the plan fits on one page, every quarter has a piece of evidence someone else could see, the home practice is justified by your own artefacts or experience, and review dates are in your calendar.

<details><summary>Model answer and self-check</summary>

**Model answer.** A graduate tester. Home practice: test automation (I extended the Module 3 CI exercises unasked). Adjacent: product (better acceptance criteria, lesson 6.2). Q1: merged API tests for an open-source project. Q2: a risk-based test strategy for a personal project. Q3: an exploratory testing report. Q4: an accessibility review of a public app. Courses: *Software Testing*, Modules 2, 3 and 5. Certification: none this year. Limits: one course at a time, one evidence piece per quarter, weekends free. Reviews: last Sunday of each quarter.

**Self-check.**
- Is every quarter's goal something another person could see?
- Did the home practice come from evidence, not fashion?
- Is the plan small enough to keep alongside work or study?

</details>

## ⚠️ Mistakes and traps
- **Treating a framework as the truth.** Each is one owner's answer to one kind of question. Learn the idea behind it.
- **Copying framework content.** Text, diagrams and structures are owned. Check the licence first.
- **Collecting certificates instead of evidence.** A certificate can open a door; evidence of practice is what gets you through it.
- **Planning without reviewing.** A plan with no review dates drifts.

## 🧾 Recap
- Frameworks come in kinds (guidance, certifiable standards, bodies of knowledge, scaling frameworks, research); the kind tells you how to use it.
- Most are owned: name them accurately and respect the owner's terms.
- Certifications are worth it for a stated goal (a role, a contract, structured study), not as a substitute for practice.
- Your next step is a learning plan with a home practice, an adjacent practice, quarterly evidence and review dates.
- Rule: learn the idea, then the vocabulary.

## ✍️ Check yourself
**1. Yasmin's new team uses a framework she has never studied, with its own words for familiar practices. What is the most useful first step?**

- A. Take the framework's certification before contributing to the team's work.
- B. Learn the team's words and ask what each unfamiliar practice protects against.
- C. Propose replacing it with the practices she used on her previous team.
- D. Ignore the framework's vocabulary and keep using the words from this course.

<details><summary>Answer</summary>

**B.** Local words plus the purpose behind each practice let her contribute at once. A delays her for a badge, C imposes old habits, D makes her harder to understand. See "Working inside a company's framework".

</details>

**2. Yasmin's plan points to application security roles. A recruiter's advert for a delivery-lead role asks for a scaled agile certification, which would take her about forty evening hours plus a renewal (illustrative). What does the certification check suggest?**

- A. Take it now, since the recruiter's advert shows what the market values.
- B. Take it only if Qafila pays the fee, since money is the main cost.
- C. Skip it for now, since it serves a role outside the path she has chosen.
- D. Take it later, after a practice project, so it confirms her practice.

<details><summary>Answer</summary>

**C.** The first question is who recognises it in the jobs you want, and this advert is for a different role. D is the near miss: sequencing after practice is sound when a certificate serves your goal, but this one does not. A generalises from one advert, and B ignores her hours. See "Certifications: when they are worth it".

</details>

**3. Which statement about Scrum matches this lesson?**

- A. It is a trademarked method whose guide must be licensed before a team uses it.
- B. It is a scaling framework for coordinating many teams across a portfolio.
- C. It is guidance owned by PeopleCert for supporting and improving IT services.
- D. It is described in a freely licensed guide for one team working in short iterations.

<details><summary>Answer</summary>

**D.** *The Scrum Guide* is freely licensed (CC BY-SA 4.0) and describes one team delivering in short iterations. A confuses Scrum with owned frameworks, B describes SAFe, and C describes ITIL. See "The names you are likely to meet".

</details>

**4. Salma's two candidates: one with four certificates who cannot describe an outage's first hour, one with none who shows a post-incident review. What conclusion does the lesson draw?**

- A. A certificate shows study, while a piece of real work shows practice and is easier to judge.
- B. Certificates matter little in hiring and are rarely worth an early-career practitioner's time.
- C. The certified candidate knows more, so the role should be redesigned around his knowledge.
- D. Both candidates are equal, since study and practice are two routes to the same skill.

<details><summary>Answer</summary>

**A.** Certificates show study; evidence shows practice. B overstates it (the lesson lists good reasons for certificates), C treats certificates as proof of ability, and D ignores that only one candidate could show the work. See "Why it matters" and "Certifications: when they are worth it".

</details>

**5. Yasmin chooses application security as her home practice. Which choice of adjacent practice best fits the lesson's advice?**

- A. Product, since it is a common neighbour for engineers and keeps her options open.
- B. Data, since data skills appear in many job adverts in her country this year.
- C. Architecture, since her security work depends on how systems are designed.
- D. Operations, since on-call is the practice she already knows best.

<details><summary>Answer</summary>

**C.** An adjacent practice is a neighbour the home practice depends on. A keeps options open without a link to security, B chooses by demand rather than evidence, and D picks what she already knows rather than what her security work depends on. See "Choosing a home practice" and "Depth and breadth".

</details>

## 📚 References
The owners' pages were opened on 22 November 2026, except PMI's and PeopleCert's, which refused automated access; for those, and for the BABOK Guide v3 date, which IIBA's page does not state, owners, editions and dates are as reported in search summaries (November 2026).
- Schwaber, K. and Sutherland, J., *The Scrum Guide* (2020), CC BY-SA 4.0: https://scrumguides.org/scrum-guide.html
- PeopleCert, ITIL: https://www.peoplecert.org/ITIL-4
- ISACA, COBIT: https://www.isaca.org/cobit
- The Open Group, TOGAF Standard: https://www.opengroup.org/togaf
- Scaled Agile, Inc., SAFe: https://scaledagileframework.com/
- Project Management Institute, *PMBOK® Guide*: https://www.pmi.org/standards/pmbok
- IIBA, *BABOK® Guide* v3: https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/
- IEEE Computer Society, *SWEBOK Guide* V4.0: https://www.computer.org/education/bodies-of-knowledge/software-engineering
- FinOps Foundation, "What is FinOps?": https://www.finops.org/introduction/what-is-finops/ and "About" (a project of the Linux Foundation): https://www.finops.org/about/
- The Open Group, IT4IT™: https://www.opengroup.org/about-it4it%E2%84%A2
- IFDC, "About VeriSM": https://verism.global/about/
- The Open Group, publisher of the Digital Practitioner Body of Knowledge™ Standard: https://www.opengroup.org/dpbok
- Library course: [*Running IT as a Business*, lesson 12.1 — The frameworks landscape: what each is for, and how to use them without becoming their servant](../itbiz/index.html#/12.1)
- Library course: [*From Graduate to Hired*, lesson 6.3 — Growing from junior to mid-level: feedback, ownership and continuous learning](../career/index.html#/6.3)
