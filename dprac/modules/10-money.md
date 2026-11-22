# Module 10 — Money and suppliers

*Qafila is now Established. About 400 people work there in 35 teams, about 30,000 merchants in four countries use the app, and the system coordinates about 400,000 deliveries a day. A payments partner integration and a data platform have joined the merchant app, the courier app, the routing service and the internal platform. At this size, money stops being something Maha checks on a spreadsheet at night. Bilal, now CFO, runs a yearly budget, every team's cloud usage shows up on one large bill, and dozens of outside companies (a cloud provider, a payment provider, a messaging service, a maps service, tools for support and monitoring, contractors) sit inside the product's daily work. Early-career practitioners are asked to take part in all of this: to write the case for a piece of work, to explain why their service's costs went up, to help check a supplier. This module shows how, through Yasmin, now in her third year as an engineer. First, how digital work is funded: budgets, business cases sized to the decision, and funding long-lived products rather than one-off projects. Second, what it costs to run digital products, and how to measure cost per unit of value instead of staring at the size of the bill. Third, how to choose, contract and leave suppliers, and what can and cannot be handed to an outsourcing partner. Each lesson leaves an artefact: a one-page business case with a funding plan, a unit-cost sheet with a savings list, and a supplier register entry with an exit plan.*

> **Steps:** Invest — decide what digital work is worth paying for, know what the product costs to run for each unit of value it delivers, and buy from outside companies without losing control of your own service.

---

# 10.1 — Funding digital work: budgets, business cases and funding products
*Level: 🔴 Advanced* · *Prerequisites: 1.3, 6.1* · *Step: Invest*

**After this you can** write a one-page business case for a piece of digital work that compares at least three options (including doing nothing), shows one-off and running costs as ranges, states a measurable benefit and a stop rule, and asks for money in stages tied to evidence. *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- A **budget** is a plan for how much money each part of the company may spend over a period, usually a year. A **business case** is the argument for spending money on one specific piece of work.
- Digital work is of three kinds: **run** (keeping what exists working), **change** (new or better capability) and **obligation** (things you must do, such as a contract or legal requirement). Each is argued for differently.
- Fund long-lived **products and teams** for a period, judged on outcomes, rather than one-off **projects** that end before the value arrives.
- The rule that matters most: **ask for money in the size of the next decision, and say in advance what would make you stop.**
- Decision cue: the bigger and harder to reverse the spend, the more evidence and the more people the decision needs. Small, reversible spends should be fast.
- Biggest trap: a business case with one option, one confident number and no running costs. Real cases compare options, give ranges and count the years after launch.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks, and money is in an illustrative currency unit ("units").

Every October, Bilal opens the budget round. At Launch there was no round: Maha decided over coffee. At Established there are 35 teams, four countries and a board that wants to know what the money buys. This year Bilal received 61 requests for new work. Some were one line ("more engineers for routing"); one was 40 pages long. Most had a single number, no options and no mention of what the thing would cost to run once built.

Yasmin's team, Courier Payouts, wanted money too. The service that calculates what each courier is paid was written at Traction for one country and one currency. Now it handles four, with country rules patched in by hand. Every month-end, two engineers spend about three days fixing payout runs, and couriers in the newest country complain about late or wrong payments. Yasmin's lead asked her to write the case for rebuilding it. Her first draft said "Rebuild payouts: 4 engineers, 9 months, 1.2 million units. Benefit: modern, scalable payouts."

Bilal sent it back with three questions: "What happens if we do nothing? What is the cheapest thing that would fix most of the pain? How will we know in three months whether this is working?" This lesson is how she answered them.

## 📐 How it works

### 🟢 The essentials

**Budgets: the yearly plan.** A **budget** sets how much each part of the company may spend, usually for a year, split by month or quarter. It is a plan, not a prediction: things change, and good finance teams re-forecast during the year. Two words you will hear:

- **Operating spend** (often "opex"): money spent on running the business in the period, such as salaries, cloud bills and subscriptions.
- **Capital spend** (often "capex"): money spent on something that will give value over several years, which accounting rules may let a company record as an asset and spread over time.

Whether building software counts as capital spend depends on accounting standards, the country and company policy. That is a question for your finance team, not something to decide yourself. What matters for you: ask Bilal's team early which kind your work is, because it changes which budget pays and what records (such as time sheets) you may be asked to keep.

**Three kinds of work.** Before arguing for money, say what kind of work it is:

| Kind | What it is | How to argue for it | Qafila example |
|---|---|---|---|
| **Run** | Keeping what exists working and safe | Cost of the service, risk if neglected | Cloud bill, on-call, patching |
| **Change** | New or better capability | Benefit to customers or the business, with a measure | Faster merchant onboarding |
| **Obligation** | Required by law, contract or a partner | The obligation and its deadline, not invented customer value | Changes the payments partner requires |

Calling obligation work "customer value" to win priority erodes trust in every other case.

**What a business case is.** A **business case** is a short, written argument that a piece of work is worth its cost and risk compared with the alternatives. It is a decision aid, not a sales brochure. The essential parts:

1. **Problem and evidence.** What is wrong, for whom, and how you know (data, not opinion).
2. **Options.** At least three, always including **do nothing** and a **cheapest useful step**.
3. **Costs.** One-off costs (building) *and* running costs (people, cloud, licences, support) for several years, as ranges.
4. **Benefits.** What will change, measured, with a baseline and a date.
5. **Risks.** What could go wrong and what you would do.
6. **The ask and the stop rule.** How much money for which stage, and what result would make you stop or change course.

**Who decides what.** Most companies set **spending limits**: amounts a team lead, a department head or the executive team may approve. At Qafila (illustrative), a team lead approves tools up to a set monthly amount, Faisal approves engineering spend within the engineering budget, and anything new above a threshold goes to Bilal and Maha. Find your company's limits before you write; they tell you how long and formal your case needs to be.

### 🟡 Going deeper

**Size the case to the decision.** A request to buy a small tool needs three sentences. A request for a year of a team's time needs a page. A multi-year platform change needs more. Writing 40 pages for a small decision wastes time; writing three lines for a large one wastes money.

**Ranges, not single numbers.** Every estimate is uncertain. Give a low, likely and high figure, and say what drives the difference ("high if the fourth country's payout rules need a new payment method"). Large studies of IT projects show why. A study by Bent Flyvbjerg and Alexander Budzier of 1,471 IT projects, published in the *Harvard Business Review* in 2011, is reported to have found an average cost overrun of 27%, but with a "fat tail": a minority of projects overran by far more, which averages hide. The lesson for a practitioner is not the exact percentage but the shape: plan for the bad case, not only the average.

**Cost of delay.** Waiting has a cost too. **Cost of delay** is what you lose for each week or month the work is not done: revenue not earned, costs still paid, risk still carried. The idea is associated with Don Reinertsen's book *The Principles of Product Development Flow* (2009). For Courier Payouts, every month of delay means another month-end of two engineers fixing runs and couriers paid late. Putting even a rough number on this helps leaders compare work fairly. Lesson 6.1 used the same question for the backlog; here it is used for money.

**Projects versus products.** A **project** has a start, an end, a fixed scope and a budget. When it closes, the team often disperses. A **product** lives for years and keeps changing. Funding products as projects causes familiar problems:

| Project funding habit | What goes wrong for a product |
|---|---|
| Scope and money fixed a year ahead | Learning mid-year needs a new approval round |
| Success judged at closing | Nobody owns the outcome afterwards |
| Team disbanded at the end | The knowledge leaves; the next change is slow |
| Running costs not in the case | The service is starved once "done" |

**Product funding** gives a long-lived team a budget for a period (often a quarter or a year), agreed outcomes to aim at, and guardrails (limits it must stay within), and then reviews results regularly. The team decides how to reach the outcome. For the manager's version, with portfolio reviews and funding memos, see [*Running IT as a Business*, lesson 3.2 — Prioritising and funding work: business cases, cost of delay and funding products not projects](../itbiz/index.html#/3.2).

**Total cost of ownership.** The **total cost of ownership** of a system is everything it costs over its life: building it, running it, supporting it, securing it, changing it and finally retiring it. For most software, the running years cost more than the first build. A case that counts only the build hides most of the bill.

### 🔴 Expert view

**Fund in stages.** Instead of asking for the whole amount at once, split the work into stages and release money for each stage only when the previous one produced evidence. Stage one is often small and fast: a prototype, a fix for the worst cause, a measurement. This turns one large bet into a series of small ones, and makes stopping cheap.

**Write the stop rule before you start.** People find it hard to stop work they have already spent money on. Psychologists call this the **sunk cost effect**: continuing because of what has been spent, not because of what further spending will bring. The defence is to write, before the money is released, what result would make you stop or change course ("if month-end fixes are not below one day by the end of stage one, we stop and reconsider").

**Opportunity cost is people.** At Qafila, most of the cost of change is people's time, and people are the scarcest resource. Funding one piece of work means not doing something else with the same engineers. A good case names what will *not* be done.

**Benefits need an owner and a date.** A benefit nobody checks is a wish. Name who will measure it, from which record, and when the review happens. For measuring outcomes, see lesson 6.3.

**The memorable rule.** Ask for money in the size of the next decision, and say in advance what would make you stop.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **One-page business case** | Problem and evidence, options, costs as ranges, benefits with measures, risks, ask, stop rule | Any request for money or a team's time above a trivial amount |
| **Options table** | Three or more options, including do nothing and the cheapest useful step, scored on cost, benefit and risk | Before committing to one solution |
| **Cost-of-delay estimate** | What each month of waiting costs, with its basis | When competing for priority or arguing urgency |
| **Staged funding plan** | Stages, money per stage, evidence needed to unlock the next | For work larger than one quarter of a team |
| **Spending-limit table** | Who may approve how much, for what kind of spend | Before writing a case, to know who decides |
| **Total-cost-of-ownership sheet** | One-off and yearly running costs over three to five years | When comparing build, buy and rebuild options |

## 🏛️ In practice at Qafila
Yasmin rewrote her case. Illustrative and fictional; money in units.

> **Business case: Courier Payouts, month-end reliability (one page)**
>
> **Problem and evidence.** Monthly payout runs need manual fixes: about 3 days of 2 engineers each month-end over the last six months (from the team's incident log). In the newest country, about 4% of couriers raised a payout ticket last month (support desk). Late payment is a reason couriers give for leaving (exit survey, small sample).
>
> **Options (costs as low / likely / high).**
>
> | Option | One-off cost | Yearly running cost | Main benefit | Main risk |
> |---|---|---|---|---|
> | A. Do nothing | 0 | About 6 engineer-weeks of fixes a year, rising with each country | None | Couriers leave; errors grow with country five |
> | B. Fix the three worst causes (country rules in configuration, validation before each run, a reconciliation report) | 120k / 180k / 260k | Small | Most manual fixes removed | Some country cases remain hand-patched |
> | C. Full rebuild | 900k / 1.2m / 1.8m | Similar to today | Clean design for future countries | Long; two systems run side by side for months |
>
> **Recommendation.** Option B now, as stage one (about one quarter, 2 engineers). Decide on C only after stage one, with its evidence.
>
> **Benefits and measures.** Month-end manual fixes below 1 day by the end of stage one; payout tickets in the newest country below 1% within two months. Owner: Yasmin's lead. Review: first month-end after release.
>
> **Stop rule.** If fixes are not below 1.5 days after two month-ends, stop and review the rebuild option with the evidence.
>
> **Not done instead.** The courier earnings screen redesign moves one quarter later.
>
> **Kind of work.** Change, with part obligation (one country's payout timing is set in Qafila's courier contracts; checked with legal).

Bilal approved stage one in ten minutes, because it was small, measurable and had a stop rule. Faisal asked why the rebuild was not recommended; Yasmin showed that option B removed most of the pain for about a sixth of the likely cost, and that option C stayed open. After two month-ends, fixes were down to half a day, and the rebuild was not needed that year.

## 🛠️ Exercises
**🟢 Name the kind of work and the decision maker.** Using the "Three kinds of work" table, label each of these Qafila items as run, change or obligation: (1) renewing the observability tool's licence; (2) adding Arabic voice notes for couriers; (3) changing how card data is handled because the payments partner requires it; (4) upgrading the database version before support for the old version ends. Then say who, in an ordinary company, would approve each.
*Done when:* every item has one label with a one-line reason, and each names a likely approver level (team lead, department head or executive).

<details><summary>Model answer and self-check</summary>

**Model answer.** (1) Run: keeps an existing service working; team lead or department head within the existing budget. (2) Change: new capability for couriers; product lead, with a case if it needs a team for more than a few weeks. (3) Obligation: required by a partner's contract; the head of the area with Dana and legal, with the deadline as the main argument. (4) Run, with some risk reduction: no new capability, but unsupported software is a security and reliability risk; Faisal, within the engineering budget.

**Self-check.**
- Did you avoid calling the partner's requirement "customer value"?
- Did you notice that (4) can be argued from risk, not benefit?
- Are your approver levels tied to size and kind of spend, not to who shouts loudest?

</details>

**🟡 Turn a one-number request into an options table.** Take this request from Qafila's routing team: "Buy a commercial route-optimisation service: 300k units a year. Benefit: better routes." Write an options table with at least three options (including do nothing and a cheapest useful step), costs as ranges for one-off and yearly running, a measurable benefit and the main risk for each.
*Done when:* the table has at least three options, every cost is a range with a basis, at least one benefit is a number with a baseline and a date, and running costs appear for every option.

<details><summary>Model answer and self-check</summary>

**Model answer.** A. Do nothing: no cost; average courier distance per delivery stays at today's level (baseline from the routing service). B. Tune the existing routing service for the two busiest cities: 40k to 90k one-off, small running cost; benefit: average distance per delivery down 5% in those cities within two months (illustrative). C. Buy the commercial service: integration 60k to 150k, plus about 300k a year (vendor quote, subject to change); benefit: distance down 8 to 12% (vendor claim, to be tested in a trial); risks: lock-in and data sharing. D. Trial C in one city for two months before deciding. Recommendation: D in parallel with B.

**Self-check.**
- Did you treat the vendor's benefit as a claim to test, not a fact?
- Does every option show yearly running cost, not just the first payment?
- Is "better routes" replaced by a measure someone can pull from a record?

</details>

**🔴 Write a one-page business case with stages and a stop rule.** Choose a piece of work from your own job, a personal or open-source project, or use Qafila's "merchant onboarding takes too long" problem (new merchants wait about 5 working days for activation, mostly for manual document checks; illustrative). Write a one-page case with all six parts, a staged funding plan (at least two stages) and a stop rule.
*Done when:* the page fits on one side, includes do nothing, gives costs as ranges with one-off and running parts, names a benefit owner and review date, and the stop rule is a measurable condition decided before the money is spent.

<details><summary>Model answer and self-check</summary>

**Model answer.** Problem: activation takes about 5 working days; about a fifth of new sign-ups never complete (onboarding funnel). Options: do nothing; a checklist and a shared queue for the operations team (stage one, about 2 weeks of one engineer and one operations specialist); automated document checks with a supplier (stage two, 3 months, plus a yearly fee); full self-service onboarding (later). Benefit: median activation under 2 working days within one quarter; owner: the onboarding product manager; review at quarter end. Stop rule: if stage one does not cut median activation below 3 days within six weeks, do not start stage two until the cause is understood. Not done instead: the merchant reports refresh.

**Self-check.**
- Is stage one small enough to finish within a few weeks and produce evidence?
- Could a sceptical finance colleague check every number's basis?
- Does the stop rule name a number and a date, not a feeling?
- Did you say what will not be done because of this?

</details>

## ⚠️ Mistakes and traps
- **One option, one number.** A case with no alternatives and no range invites a yes-or-no fight. Compare at least three options and give ranges.
- **Forgetting running costs.** The build is often the smaller part of total cost. Add yearly running costs for every option.
- **Vague benefits.** "Modern, scalable" is not a benefit. Write who will do what differently, by how much, by when.
- **Asking for everything at once.** A large single request makes stopping expensive. Fund in stages, each unlocked by evidence.
- **Deciding accounting treatment yourself.** Whether work is capital or operating spend is for finance to decide under the rules that apply. Ask early.
- **Disguising obligations.** Label work required by law, contract or a partner as obligation; argue from the requirement and its deadline.

## 🧾 Recap
- Budgets plan a year's spend; business cases argue for one piece of work against its alternatives.
- Label work as run, change or obligation; each is argued for differently.
- A good case has problem and evidence, options (including do nothing), costs as ranges with running costs, measured benefits, risks, and an ask with a stop rule.
- Fund long-lived products and teams for a period, judged on outcomes; fund large uncertain work in stages.
- Rule: ask for money in the size of the next decision, and say in advance what would make you stop.

## ✍️ Check yourself
**1. Yasmin's first draft asked for 1.2 million units for a full rebuild, with "modern, scalable payouts" as the benefit. What was the most important thing missing?**

- A. A more detailed technical design of the new payout service, so finance could check it.
- B. A stronger statement of urgency from the Head of Engineering to support the request.
- C. Alternatives including do nothing, costs as ranges and a benefit that can be measured.
- D. A comparison with what similar companies in other countries spend on courier payouts.

<details><summary>Answer</summary>

**C.** A business case is a comparison of options with measurable benefits; without alternatives and a measure, Bilal cannot judge it. A adds detail but not a decision basis, B is persuasion rather than evidence, and D gives an outside number that says nothing about Qafila's options. See "What a business case is".

</details>

**2. Which of these is the best stop rule for Qafila's onboarding work?**

- A. Stop if median activation is not below 3 working days six weeks after stage one starts.
- B. Stop if the team feels the work is no longer delivering enough value for merchants.
- C. Stop when the full budget for the year has been spent, whatever the results show.
- D. Stop if a more important project appears in the portfolio during the coming year.

<details><summary>Answer</summary>

**A.** A stop rule is a measurable condition with a date, written before money is spent. B is a feeling that sunk costs will bend, C stops on spending rather than evidence, and D describes reprioritisation, not a test of whether the work is working. See "Write the stop rule before you start".

</details>

**3. The payments partner requires Qafila to change how card data flows by a fixed date. How should the team present this work for funding?**

- A. As change work, with a forecast rise in merchant satisfaction to win priority.
- B. As run work, since it touches an existing service and needs no new capability.
- C. As a technical debt item, to be scheduled when the team has spare capacity.
- D. As obligation work, argued from the partner's requirement and its deadline.

<details><summary>Answer</summary>

**D.** Work required by a contract or partner is an obligation; its case rests on the requirement and the date. A dresses it up as customer value, B ignores that it is new required work with a deadline, and C risks missing the date. See "Three kinds of work".

</details>

**4. Why does a business case need running costs for several years, not just the cost of building?**

- A. Because accounting rules everywhere require running costs to appear in every case.
- B. Because for most software the years of running often cost more than the first build.
- C. Because suppliers usually charge less for building than for annual licence renewals.
- D. Because running costs are easier to estimate accurately than one-off build costs.

<details><summary>Answer</summary>

**B.** Total cost of ownership includes running, supporting, securing and changing the system, which usually outweighs the build. A states a legal rule the lesson does not claim, C is a narrow supplier point, and D is not true in general. See "Total cost of ownership".

</details>

**5. Faisal wants to fund the routing rebuild as one 18-month request so "we don't have to keep asking". What is the strongest reason to fund it in stages instead?**

- A. Each stage produces evidence before more money is released, so stopping stays cheap.
- B. Smaller requests are always approved faster by finance, whatever their content.
- C. Staged funding means the team does not need to estimate the total cost at all.
- D. Stages let the team change its outcome measures whenever the results disappoint.

<details><summary>Answer</summary>

**A.** Staging turns one large bet into smaller ones, each unlocked by evidence. B may be true sometimes but is not the reason, C is wrong (a total range is still needed), and D undermines the point of measures set in advance. See "Fund in stages".

</details>

## 📚 References
- Flyvbjerg, B. and Budzier, A., "Why Your IT Project May Be Riskier Than You Think", *Harvard Business Review* 89(9), September 2011. Sample of 1,471 IT projects, average cost overrun of 27% and the "fat tail", as reported in search summaries of the SSRN abstract (not opened): https://papers.ssrn.com/abstract=2229735. Author preprint: https://arxiv.org/abs/1304.0265
- Reinertsen, D. G., *The Principles of Product Development Flow: Second Generation Lean Product Development* (Celeritas, 2009). Cost of delay, as reported in summaries; book not opened.
- Arkes, H. R. and Blumer, C., "The psychology of sunk cost", *Organizational Behavior and Human Decision Processes* 35(1): 124–140 (1985). Citation as reported in search summaries; paper not opened.
- Library course: [*Running IT as a Business*, lesson 3.2 — Prioritising and funding work: business cases, cost of delay and funding products not projects](../itbiz/index.html#/3.2) (the manager's view of portfolio funding).
- Library course: [*Running IT as a Business*, lesson 10.1 — IT financial management: cost models, unit costs and the cost of a product](../itbiz/index.html#/10.1).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 3.1 — Unit economics in plain words, including AI and model costs](../founder/index.html#/3.1).

---

# 10.2 — The cost of running digital products: cloud costs and unit economics
*Level: 🔴 Advanced* · *Prerequisites: 1.3, 4.1* · *Step: Invest*

**After this you can** read a cloud bill by service and by team, calculate the cost per unit of value for one product (such as cost per 1,000 deliveries), explain a month's change in that number, and draw up a ranked list of savings that does not weaken the reliability target. *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- In the cloud, every engineer who creates or resizes a resource is spending money. Cost is a design decision, not only a finance task.
- The bill has a few big parts: compute, storage, data transfer, managed services, and outside services (messaging, maps, monitoring, AI models). People's time sits outside the bill but is often the largest cost of all.
- **Unit cost** is total cost divided by units of value (deliveries, active merchants). It shows whether the business is getting more efficient as it grows; the total bill alone cannot.
- The rule that matters most: **measure cost per unit of value, not just the size of the bill.**
- Decision cue: before cutting, ask what the cost buys. Savings that break the 99.9% reliability target or slow every team are not savings.
- Biggest trap: costs nobody owns. Untagged resources and forgotten test environments grow quietly until someone notices the bill.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks, and money is in an illustrative currency unit ("units").

In March, Bilal brought one chart to the leadership meeting. Over the past year Qafila's monthly cloud bill had grown by about 70%, while deliveries had grown by about 35%. "Either we are buying something valuable with that difference," he said, "or we are wasting it. Which?" Nobody in the room could answer. The bill listed thousands of resources; about a fifth of the spend carried no tag saying which team owned it.

Faisal asked each team to explain its own costs. Yasmin's team, Courier Payouts, had never looked. She found three things in one afternoon: a full copy of the production database kept for testing and never switched off, logs kept forever at the most expensive storage level, and a nightly report that copied all payout data across regions. None of them had been a decision; each had been a default.

At Launch (lesson 1.3), the software lines of cost to serve were tiny and Maha's time was the biggest cost. At Established the picture has changed: software is now a large cost in its own right, spread across 35 teams. This lesson shows how a practitioner reads it, measures it per unit of value and reduces it without breaking anything.

## 📐 How it works

### 🟢 The essentials

**What is on the bill.** Cloud providers charge for what you use, usually by the hour, second, request or gigabyte. The main parts:

| Part | What you pay for | Qafila example |
|---|---|---|
| **Compute** | Virtual machines, containers, serverless functions, by size and time | Order service, routing service, courier app back end |
| **Storage** | Data kept, by amount and storage level (faster costs more) | Order history, photos of proof of delivery, logs |
| **Data transfer** | Data moving out of the cloud, or between regions and zones | Reports copied across regions; app traffic to phones |
| **Managed services** | Databases, queues, search, data platform, priced by size and use | The main order database; the data platform |
| **Outside services** | Other companies' APIs and tools, often per call or per user | Text messages, maps, monitoring, support desk, AI model calls |

Outside services often arrive on separate invoices, so they are easy to forget when people talk about "the cloud bill". Count them.

**Who creates cost.** In a company's own data centre, buying a server took weeks and a purchase order. In the cloud, an engineer can create a large database in minutes. That speed is valuable, and it moves spending decisions to the people building the system. You do not need to be in finance to affect costs: every instance size, retention setting and region choice is a small spending decision.

**Tags and ownership.** A **tag** (or label) is a short piece of text attached to a cloud resource, such as `team=courier-payouts` or `env=test`. Lesson 4.1 asked you to tag everything; this is why. With tags, the bill can be split by team, product and environment. Without them, cost is a single number nobody owns. Two common ways to use the split:

- **Showback:** each team sees what its resources cost, but the money comes from a shared budget.
- **Chargeback:** each team's costs are charged to its own budget.

Showback is usually the right start; it creates awareness without arguments over accounting.

**Unit cost.** **Unit cost** is cost divided by the number of units of value delivered in the same period. Lesson 1.3 chose Qafila's unit of value: a delivery coordinated. At this scale, it is easier to read per 1,000 deliveries. If the monthly cloud and outside-service cost is 360,000 units and Qafila coordinates about 12 million deliveries a month (about 400,000 a day), the unit cost is 30 units per 1,000 deliveries, or 0.03 per delivery. The total bill can rise while unit cost falls; that is healthy growth. If unit cost rises, something needs explaining.

### 🟡 Going deeper

**Fixed and variable at scale.** Some costs grow with deliveries (messages, map calls, compute for the order flow). Some grow with the number of teams or countries (each team's test environments, each country's separate data store). Some grow with data kept (history, logs). Knowing which is which tells you what to expect next year. A cost that grows with *time* rather than with use, such as data kept forever, is a warning sign: it rises even if the business stands still.

**The usual savings, roughly in order of ease.**

| Lever | What it means | Typical risk |
|---|---|---|
| **Switch off what is idle** | Stop test environments at night and weekends; delete forgotten resources | Low, if owners agree first |
| **Right-size** | Match machine and database sizes to actual use | Low to medium; check peak load |
| **Storage levels and retention** | Move old data to cheaper storage; delete what you no longer need (within the retention rules from lesson 9.2) | Medium; slower to read old data back |
| **Commitment discounts** | Promise the provider a level of use for a period (often a year or more) in return for a lower price | Medium; you pay even if use falls |
| **Interruptible capacity** | Spare capacity sold cheaply that the provider can reclaim at short notice | Only for work that can be stopped and restarted |
| **Design changes** | Avoid copying data between regions, cache map lookups, batch messages | Higher effort; best done with an architecture decision record (lesson 9.1) |

Prices, discounts and limits change; check the provider's current documentation before relying on any of them.

**Waste is common, and reported.** Surveys suggest unowned spending is widespread. Flexera, a company that sells cost-management software, publishes a yearly *State of the Cloud* report based on a survey of cloud users. Its 2025 report is reported to say that respondents estimated about 27% of their cloud spend was wasted, and that 84% named managing cloud spend as their top cloud challenge; its 2026 report is reported to put the waste estimate at 29%, linked to AI workloads. These are self-reported estimates from a vendor's survey, not measurements of any single company, so use them to start a conversation, not to set a target.

**FinOps.** **FinOps** is the name used for the practice of bringing finance, engineering and business people together to manage cloud spending. The FinOps Foundation, part of the Linux Foundation, defines it (as reported) as an operational framework and cultural practice that maximises the business value of cloud, enables timely data-driven decision making and creates financial accountability through collaboration. The FinOps Framework is the Foundation's own publication; read it on their site rather than through summaries. The core idea this lesson teaches in its own words is simple: the people who create costs should see them, own them and weigh them against value. For hands-on depth with real tools, see [*Cloud & DevOps: Zero to Hero*, lesson 6.2 — FinOps: understanding, allocating and cutting cloud cost](../cloud/index.html#/6.2).

### 🔴 Expert view

**Cost is a quality attribute.** In lesson 9.1, cost was one of the qualities weighed in an architecture decision. Treat it the same way in daily work: when you design a feature, ask what it will cost per 1,000 deliveries, as you would ask how fast it will be. A design that triples data transfer is a cost decision, whether or not anyone called it one.

**Do not save your way out of reliability.** Order tracking targets 99.9% a month. Removing the standby database or shrinking capacity below peak load may lower the bill and break that promise. Every saving on a production system should say what it does to reliability and who agreed. Cheap and down is not a bargain.

**Watch for surprises, not only totals.** Set **budget alerts** (a message when a team's spend passes a threshold) and **anomaly alerts** (a message when spend jumps unusually fast). A runaway job found the same day costs a little; found at month-end, it costs a month.

**AI and other per-call costs.** Services that charge per call, such as messaging, maps or AI models, grow directly with use and can change fastest. If Qafila adds an AI assistant that answers courier questions, its cost per conversation belongs in the unit-cost sheet from day one. For how products count model costs, see [*Founder's Playbook for AI-First Builders*, lesson 3.1 — Unit economics in plain words, including AI and model costs](../founder/index.html#/3.1).

**People are still a cost to serve.** Cloud is the visible bill, but support time per delivery, manual fixes and on-call load are also costs per unit. Lesson 10.1's payout fixes were a people cost. A full unit-cost view puts both side by side.

**The memorable rule.** Measure cost per unit of value, not just the size of the bill.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Unit-cost sheet** | Monthly cost by part, units delivered, cost per 1,000 units, change from last month with reasons | Monthly, for each product or service a team owns |
| **Tagging policy** | Required tags (team, product, environment, purpose) and a check that blocks untagged resources | Before anyone can create cloud resources |
| **Provider cost tools** | The cloud provider's own billing and cost-explorer pages (each major provider has one) | Weekly look at your team's spend; investigating a jump |
| **Budget and anomaly alerts** | Messages when spend passes a threshold or jumps unusually | Set once per team and environment; review monthly |
| **Savings list** | Each idea with estimated saving, effort, risk to reliability, owner and status | After each monthly review, to choose what to do next |
| **Cost estimate in pull requests** | Tools that estimate the cost change of an infrastructure-as-code change, such as Infracost (an example, not an endorsement) | When infrastructure changes are reviewed as code (lesson 4.1) |

## 🏛️ In practice at Qafila
Yasmin built the first unit-cost sheet for Courier Payouts. Illustrative and fictional; money in units.

> **Courier Payouts: unit-cost sheet, March**
>
> Unit of value: payouts completed (one per courier per pay period). Payouts this month: about 220,000.
>
> | Cost part | February | March | Change and reason |
> |---|---|---|---|
> | Compute (payout service) | 6,200 | 6,400 | More couriers in country four |
> | Main database | 4,800 | 4,900 | Steady |
> | Test copy of production database | 3,900 | 3,900 | Never switched off; nobody uses it at night |
> | Logs (kept forever, fastest storage level) | 2,700 | 3,100 | Grows every month, whatever the volume |
> | Cross-region copy for nightly report | 1,600 | 1,700 | Copies all data; report needs one region |
> | Payment provider fees for payouts | 11,000 | 11,500 | Per payout; more couriers |
> | **Total** | **30,200** | **31,500** | |
> | **Cost per 1,000 payouts** | **about 143** | **about 143** | Flat: growth paid for, waste hidden |
>
> **Savings list.**
>
> | Idea | Estimated monthly saving | Effort | Reliability risk | Owner |
> |---|---|---|---|---|
> | Stop the test database outside working hours; use a smaller masked copy | 2,500–3,000 | 2 days | None (not production) | Yasmin |
> | Logs: 30 days fast, then cheaper storage, delete after the agreed retention period | 1,500–2,200 | 3 days | Low; older logs slower to search | Yasmin, with Dana for retention |
> | Nightly report reads in one region | about 1,500 | 1 week | Low; report runs later | Data platform team |
> | Commitment discount for payout compute | Small | Finance decision | None, but locks in use | Bilal's team |

Yasmin's first draft proposed removing the payout database's standby copy too, which would have saved more. Salma stopped it: payouts run once a month, and a database failure that day with no standby would breach the courier contracts. It stayed. Dana pointed out that the test copy held real courier bank details and should have been masked anyway, so the fix was also a security fix. After two months, cost per 1,000 payouts fell to about 115 (illustrative), and Faisal asked every team to bring a sheet like it to the monthly review.

## 🛠️ Exercises
**🟢 Calculate and read a unit cost.** Using these illustrative Qafila figures, calculate cost per 1,000 deliveries for each month and say what changed: January, total cost 330,000 units for 11 million deliveries; February, 345,000 for 11.2 million; March, 390,000 for 11.3 million.
*Done when:* you have three unit costs to one decimal place, you name which month needs explaining, and you write one question you would ask the teams.

<details><summary>Model answer and self-check</summary>

**Model answer.** January: 330,000 ÷ 11,000 = 30.0 per 1,000. February: 345,000 ÷ 11,200 ≈ 30.8. March: 390,000 ÷ 11,300 ≈ 34.5. February is roughly flat (small rise); March jumped by about 12% while deliveries barely grew. Question: "Which team's or service's costs rose in March, and was it a decision (a new feature, a new country) or something left running?"

**Self-check.**
- Did you divide by thousands of deliveries, not by deliveries?
- Did you notice that the total rose every month but only March needs explaining?
- Is your question aimed at finding a cause, not a culprit?

</details>

**🟡 Tag and allocate.** Look at your own cloud account (a free tier is fine), a personal project, or this Qafila list of resources: order database (no tags), "test-db-old" (no tags), routing cluster (`team=routing`), payout service (`team=courier-payouts`, `env=prod`), a storage bucket named "tmp-export-2025" (no tags). Write a tagging policy with four required tags and, for each untagged resource, the question you would ask to find its owner and whether it is still needed.
*Done when:* the policy names four tags with allowed values, every untagged resource has an owner question and a "keep, resize or delete" proposal, and nothing is deleted without its owner's agreement.

<details><summary>Model answer and self-check</summary>

**Model answer.** Policy: `team` (from the team list), `product` (merchant, courier, routing, payouts, platform, data), `env` (prod, staging, test, dev), `purpose` (free text, under 40 characters); new resources without them are blocked by a check in the pipeline. Order database: "Which team owns the order database?" Likely the Orders team; keep and tag. test-db-old: "Who created it, and is anything reading from it?" Check access logs; propose delete after two weeks' notice. tmp-export-2025: "What is in it, and does it hold personal data?" Check with Dana; propose delete after the owner confirms, or apply the retention rule.

**Self-check.**
- Is there a way to enforce the policy, not just a document?
- Did you check for personal data before proposing deletion or keeping?
- Did you give owners notice rather than deleting quietly?

</details>

**🔴 Build a savings list that protects reliability.** Using Yasmin's unit-cost sheet above (or a service you know), list at least four savings ideas. For each, give an estimated saving range, effort, the effect on the 99.9% reliability target or on other teams, an owner and whether you recommend it. Then rank them.
*Done when:* every idea has all six fields, at least one idea is rejected or deferred for a stated reliability or security reason, and the ranking puts low-risk, high-saving, low-effort ideas first.

<details><summary>Model answer and self-check</summary>

**Model answer.** (1) Schedule the test database off outside working hours and use a masked, smaller copy: 2,500–3,000 a month, 2 days, no production effect, recommend first. (2) Log retention and cheaper storage after 30 days: 1,500–2,200, 3 days, older logs slower to search, recommend with Dana's retention input. (3) Nightly report reads in one region: about 1,500, a week, report later in the morning, recommend after checking who reads it. (4) Commitment discount for compute: small, finance decision, locks in use for a period, defer until the design settles. (5) Remove the payout database standby: about 2,000, 1 day, breaks recovery on payout day and risks the courier contracts, reject.

**Self-check.**
- Did you write down why the rejected idea was rejected, so it does not come back next month?
- Are savings ranges, not single confident numbers?
- Did you check which ideas need another team's or Dana's agreement?

</details>

## ⚠️ Mistakes and traps
- **Watching only the total bill.** A growing bill can be healthy. Track cost per unit of value and explain changes in it.
- **Untagged resources.** Cost without an owner keeps growing. Require tags and block resources without them.
- **Saving at reliability's expense.** Removing standbys or shrinking below peak load may break the 99.9% target. Every production saving states its reliability effect and who agreed.
- **Forgetting outside services and people.** Messaging, maps, monitoring, AI calls and manual work are part of cost to serve. Put them on the same sheet.
- **Keeping data forever by default.** Storage that grows with time, not use, rises even when the business stands still. Set retention with the data owner and the rules from lesson 9.2.
- **Trusting old price assumptions.** Prices and discounts change. Check current terms before relying on a number in a plan.

## 🧾 Recap
- In the cloud, engineers' design choices are spending decisions; cost is a quality like speed or reliability.
- The bill splits into compute, storage, data transfer, managed services and outside services; tags turn it into costs teams own.
- Unit cost (cost per 1,000 deliveries or per payout) shows whether growth is efficient; explain every change.
- Savings come from switching off idle resources, right-sizing, retention, commitments and design changes, each weighed against reliability.
- Rule: measure cost per unit of value, not just the size of the bill.

## ✍️ Check yourself
**1. Qafila's cloud bill grew 70% in a year while deliveries grew 35%. What should Bilal's team look at first?**

- A. How cost per 1,000 deliveries changed, and which teams and services drove the rise.
- B. Which cloud provider offers the lowest list prices for the services Qafila uses today.
- C. Whether all teams can cut their cloud spend by the same fixed percentage next quarter.
- D. How much the bill would fall if every non-production environment were deleted at once.

<details><summary>Answer</summary>

**A.** The question is whether the extra spend bought value; unit cost and its drivers answer that. B jumps to switching providers before understanding the cause, C cuts blindly, including good spending, and D could destroy work in progress. See "Unit cost".

</details>

**2. What is the main purpose of tagging cloud resources with team, product and environment?**

- A. To let the cloud provider apply its volume discounts to each team separately.
- B. To stop engineers creating any new resources without finance approval first.
- C. To make resources easier to find when the provider's console search is slow.
- D. To split costs so each team can see and own the spending it causes.

<details><summary>Answer</summary>

**D.** Tags turn one bill into costs with owners, which is what makes showback or chargeback possible. A confuses tags with discounts, B describes a heavy approval gate tags do not create, and C is a minor side effect. See "Tags and ownership".

</details>

**3. Yasmin proposes removing the payout database's standby copy to save about 2,000 units a month. Why did Salma stop it?**

- A. Because standby copies are free on most cloud providers, so no saving was possible.
- B. Because recovery on payout day depended on it, putting reliability and contracts at risk.
- C. Because only finance may change production infrastructure that has a monthly cost.
- D. Because the saving was too small to be worth the engineering time it would need.

<details><summary>Answer</summary>

**B.** Savings must be weighed against reliability; without the standby, a failure on payout day could breach the courier contracts. A is false, C misplaces the decision, and D misses the real reason (the risk, not the size). See "Do not save your way out of reliability".

</details>

**4. A vendor survey reports that respondents estimate about a quarter of cloud spend is wasted. How should Qafila use that figure?**

- A. As a target: cut exactly that share of every team's bill this year.
- B. As proof that Qafila wastes the same share, to include in the board report.
- C. As a prompt to look for waste, not as a measure of Qafila's own spending.
- D. As a reason to ignore cost work, since waste is normal across the industry.

<details><summary>Answer</summary>

**C.** The figure is a self-reported estimate from a vendor's survey; it suggests where to look but says nothing exact about Qafila. A and B treat a survey of other companies as a fact about Qafila, and D draws the wrong conclusion from it. See "Waste is common, and reported".

</details>

**5. Which of these costs grows with time rather than with the number of deliveries?**

- A. Text messages sent to couriers and shop customers for each delivery.
- B. Logs kept forever in the fastest storage level, whatever the volume.
- C. Map lookups made by the routing service when assigning each order.
- D. Payment provider fees charged on each payout to a courier's account.

<details><summary>Answer</summary>

**B.** Data kept forever keeps growing even if the business stands still. A, C and D are per-use costs that grow with deliveries or payouts. See "Fixed and variable at scale".

</details>

## 📚 References
- FinOps Foundation, "What is FinOps?" (definition as quoted in Microsoft Learn's FinOps training module and in search summaries; the Foundation's page could not be opened from this environment): https://www.finops.org/introduction/what-is-finops/
- Microsoft Learn, "What is FinOps?" training unit, which quotes the FinOps Foundation definition (as reported in search summaries; not opened): https://learn.microsoft.com/en-ie/training/modules/get-started-with-finops/2-what-is-finops
- Flexera, press release "New Flexera Report Finds that 84% of Organizations Struggle to Manage Cloud Spend", 19 March 2025 (84% and 27% figures as reported in search summaries; not opened): https://www.flexera.com/about-us/press-center/new-flexera-report-finds-84-percent-of-organizations-struggle-to-manage-cloud-spend
- Flexera, press release "Flexera Finds Cloud Value is Rising While AI Waste Grows" (2026 report; 29% waste estimate as reported in search summaries; not opened): https://www.flexera.com/about-us/press-center/flexera-finds-cloud-value-is-rising-while-ai-waste-grows
- Infracost, open-source repository (an example of a tool that estimates the cost of infrastructure-as-code changes in pull requests; description as reported in search summaries; not opened): https://github.com/infracost/infracost
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 6.2 — FinOps: understanding, allocating and cutting cloud cost](../cloud/index.html#/6.2).
- Library course: [*Running IT as a Business*, lesson 10.1 — IT financial management: cost models, unit costs and the cost of a product](../itbiz/index.html#/10.1).
- Library course: [*AI Product Management*, lesson 8.2 — Unit economics: cost to serve, pricing models and margins](../aipm/index.html#/8.2).

---

# 10.3 — Suppliers, contracts and outsourcing
*Level: 🔴 Advanced* · *Prerequisites: 2.3, 7.3* · *Step: Invest*

**After this you can** list the outside suppliers one product depends on and rank them by how much the service would suffer without them, run a basic due-diligence check on a new supplier, read a contract summary for the terms that matter to practitioners (scope, price changes, service levels, data, security evidence, exit), and write an exit plan for one supplier. *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- Every digital product depends on **suppliers**: cloud providers, software-as-a-service tools, APIs (messaging, maps, payments), open-source components and people (contractors and outsourcing partners).
- A **contract** sets what the supplier will do, at what price, to what standard, with what data, and how either side can leave. Practitioners do not write contracts, but they know what the service needs and must check the contract gives it.
- **Due diligence** is checking a supplier before relying on it: what it does with your data, how secure and reliable it is, and what happens if it fails or you leave.
- The rule that matters most: **you can hand over the work, never the accountability; know how you would leave before you sign.**
- Decision cue: the closer a supplier sits to the core service (taking orders, tracking deliveries, paying couriers), the more checking, the more contract care and the better the exit plan it needs.
- Biggest trap: signing because the demo was good and the price was low, without asking about data, service levels, price rises or exit.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

On a Friday evening in the busiest week of the year, couriers in one of Qafila's four countries stopped receiving order texts. The messaging provider that sent them had a problem with a local carrier. It took Salma's team forty minutes to find out, because nobody at Qafila had the supplier's status page bookmarked and the support contract only covered email during the supplier's office hours. Merchants phoned; deliveries piled up.

The following Monday, two more supplier issues arrived. The maps provider gave notice that its price per lookup would rise from the next quarter. And Maha had agreed with a software company in another country to build the integration for Qafila's fifth country under contract, to move faster without hiring; the draft contract had arrived, and nobody in engineering had read it.

At the same time, the payments partner sent its due-diligence questionnaire (Module 11 covers it in full). One section asked Qafila to list the suppliers that handle merchant or courier data and to show how it controls them. Dana asked Yasmin, who knew the code that called outside services, to help build the list. This lesson is what they learned.

## 📐 How it works

### 🟢 The essentials

**Kinds of supplier.** Suppliers come in several shapes, and each brings different risks:

| Kind | What you buy | Qafila example | Typical risk |
|---|---|---|---|
| **Cloud provider** | Computing, storage, managed services | The main cloud provider since Launch | Deep dependency; hard to leave |
| **Software-as-a-service (SaaS) tool** | Software someone else runs, used through a browser or API | Support desk, monitoring, team chat | Holds your data; price and terms change |
| **API service** | A function called by your code | Messaging, maps, payment provider | On the critical path; outages are your outages |
| **Open-source component** | Code you include, often free | Libraries in every service | No contract at all; security and upkeep are yours |
| **People** | Contractors or an outsourcing partner doing work for you | The fifth-country integration team | Knowledge and quality leave with them |

Lesson 2.3 covered the first choice of build or buy. Here the question is how to manage suppliers once you depend on many.

**The terms that matter to practitioners.** Contracts are written and approved by legal and procurement teams. But they cannot check that the contract matches how the service really works; you can. Read the summary, or the contract, for these:

| Term | Plain question to ask |
|---|---|
| **Scope** | What exactly will they provide, and what is excluded? |
| **Price and changes** | How is it charged (per user, per call, per month)? How much notice before prices change? |
| **Service levels** | What availability and support response do they promise, measured how? What happens if they miss it (often a small credit, not real compensation)? |
| **Data** | What data will they hold, where, who can see it, do they use it for anything else, which other companies do they pass it to, and how is it returned or deleted at the end? |
| **Security evidence** | What independent evidence do they offer (audit reports, certifications), and how will they tell us about a breach? |
| **Liability** | If they cause us harm, what are they responsible for, and up to what limit? |
| **Term and exit** | How long is the contract, how do we leave, how much notice, and what help do we get to move our data? |

You are not deciding what any of these mean legally. You are spotting gaps between the contract and the service, and raising them with the people who decide.

**Why service levels from suppliers matter to you.** Lesson 7.3 showed that if two services in a chain are each available 99.9% of the time, the chain is available only about 99.8%. Your promise to merchants can never be stronger than the suppliers on the critical path allow, unless you add a fallback. A supplier's service-level promise usually comes with a credit off next month's bill if missed, which rarely covers your actual loss.

### 🟡 Going deeper

**Map dependencies before you rank them.** A **supplier dependency map** lists every outside service a product uses and what happens if it stops. Yasmin built Qafila's by searching the code for outside API calls and the finance system for invoices; each found suppliers the other missed. Then rank each one:

| Supplier | What breaks without it | Fallback today | Data it holds | Rank |
|---|---|---|---|---|
| Messaging provider | Couriers miss order alerts (app push still works) | None for text | Courier phone numbers | High |
| Maps provider | Routing slower, estimates worse | Cached routes for 1 hour | Addresses, locations | High |
| Payment provider | Merchants cannot pay; payouts stop | None | Payment and bank details | Critical |
| Support desk tool | Agents work from email | Email inbox | Merchant and courier messages | Medium |
| Team chat | Inconvenient, not customer-facing | Email, phone | Internal messages | Low |

The ranking decides how much effort each supplier gets: critical and high suppliers need careful contracts, regular review, a fallback and an exit plan; low ones need a register entry and a yearly check.

**Due diligence in proportion.** **Supplier due diligence** means checking a supplier before you rely on it. For a low-risk tool, a short checklist is enough. For a critical supplier, ask for evidence:

- **Security reports and certifications.** Two common kinds of evidence: a **SOC 2 report**, an independent auditor's report under criteria set by the AICPA (the American Institute of Certified Public Accountants), covering security and optionally availability, processing integrity, confidentiality and privacy; and certification to **ISO/IEC 27001**, the international standard for information security management systems. A **Type 2** SOC 2 report is reported to test how controls worked over a period, a **Type 1** at a single point in time. Read the scope: a certificate that covers only one office says nothing about the service you use.
- **Reliability history.** Their public status page and incident history.
- **Data handling.** Where data is stored, which other companies (sub-processors) handle it, how it is deleted.
- **Financial and business health.** Will they be there in three years? Finance can check.

**Data protection rules reach into contracts.** Many data protection laws require a written contract when a supplier processes personal data on your behalf. For example, Article 28 of the EU's General Data Protection Regulation (GDPR) is reported to require such contracts to say, among other things, that the supplier acts only on documented instructions, keeps the data confidential and secure, uses other sub-processors only with authorisation, and deletes or returns the data at the end. Qafila's four countries each have their own rules; the question for each new supplier is "does our data protection law require specific contract terms here, and has our adviser checked them?" For contracts with AI suppliers, see [*AI Governance: Zero to Hero*, lesson 11.2 — Buying AI: vendor due diligence and contracts](../aigp/index.html#/11.2).

**Outsourcing work, not accountability.** **Outsourcing** means paying another company to do work you would otherwise do yourself: building a feature, running support at night, operating a system. Three common ways to pay:

| Contract type | How it works | Good for | Watch out for |
|---|---|---|---|
| **Fixed price** | An agreed price for an agreed scope | Small, well-understood work | Every change becomes a negotiation; quality may be cut to fit the price |
| **Time and materials** | Pay for time spent at agreed rates | Uncertain work you can steer closely | Cost can grow; you must manage the work |
| **Outcome-based** | Payment tied to measured results | Mature services with clear measures | Hard to define fairly; gaming the measure |

Whatever the contract, Qafila stays accountable to merchants, couriers and the payments partner for what the supplier builds or runs. Practical safeguards: Qafila's own engineers review the partner's code through the same pull-request process (lesson 3.1); the partner works in Qafila's repository and pipeline, not its own; documentation and handover are deliverables, paid for, not favours; and at least one Qafila engineer is paired with the partner throughout so the knowledge stays.

### 🔴 Expert view

**Plan the exit at the start.** **Lock-in** is when leaving a supplier would be so costly or slow that you effectively cannot. Some lock-in is a fair price for speed (the cloud provider's managed database saved Qafila years). The danger is lock-in you did not choose. An **exit plan** answers: how would we get our data out, in what format, how long would moving take, what would we run in the meantime, and what does the contract say about notice and help? Write it while relations are good; you will not get good terms in a dispute. For a builder's view of costs and lock-in, see [*Founder's Playbook for AI-First Builders*, lesson 7.2 — Costs, vendors and lock-in](../founder/index.html#/7.2).

**Regulated customers pass their rules down.** When Qafila works with a payments partner, the partner's own regulators expect it to control its suppliers, and Qafila is one of them. So the partner asks about Qafila's suppliers too (sometimes called fourth parties). Financial-sector rules illustrate the kind of expectation. For example, the EU's Digital Operational Resilience Act (Regulation (EU) 2022/2554), which applies to EU financial entities from 17 January 2025, is reported to require exit strategies for ICT services supporting critical or important functions. Whether any such rule reaches Qafila depends on its countries and contracts; the question to ask is "what does our partner's regulation expect of its suppliers, and what will they ask us to show?" Module 11 picks this up.

**Price-change notice is a design input.** When the maps provider announced its price rise, the cost per 1,000 deliveries (lesson 10.2) moved overnight. Mature teams treat per-call suppliers as a cost line they can reduce by design: caching lookups, batching calls, or keeping a second provider ready. Know which suppliers can change your unit cost and how much notice the contract gives.

**Review suppliers, not just contracts.** A supplier register is only useful if someone looks at it. Critical suppliers get a named internal owner, a review at least yearly (performance against service levels, incidents, price, security evidence still current, exit plan still valid), and a check whenever something changes: a new data type, a new country, an acquisition.

**The memorable rule.** You can hand over the work, never the accountability; know how you would leave before you sign.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Supplier register** | One row per supplier: what it does, internal owner, data held, rank, contract dates, review date | Always; start it when you have more than a handful of suppliers |
| **Supplier dependency map** | Every outside service a product uses, what breaks without it, fallback, rank | Before ranking suppliers; before a reliability review |
| **Due-diligence checklist** | Questions on data, security evidence, reliability, sub-processors, business health, scaled to the rank | Before signing with a new supplier or adding a new data type |
| **Contract terms question sheet** | The seven plain questions (scope, price, service levels, data, security, liability, exit) | When a draft contract or renewal reaches your team |
| **Exit plan** | How to get data out, how long a move would take, what runs meanwhile, contract notice and help | For every critical and high-rank supplier, written at signing |
| **Supplier status page list** | Bookmarked status pages and support contacts for every critical supplier, linked from the runbook | Before the next incident, not during it |

## 🏛️ In practice at Qafila
Dana and Yasmin built the supplier register; Salma added the runbook links; Bilal added contract dates. Illustrative and fictional.

> **Supplier register entry: messaging provider (texts to couriers and shop customers)**
>
> | Field | Entry |
> |---|---|
> | What it does | Sends order alerts and delivery updates by text in all four countries |
> | Internal owner | Salma (service); Bilal (contract) |
> | Rank | High: couriers miss alerts without it; app push notifications still work |
> | Data held | Courier and shop-customer phone numbers; message text (includes shop name and address) |
> | Contract | Yearly, renews automatically unless cancelled with 60 days' notice; price per message; 30 days' notice of price changes |
> | Service levels | Availability target stated; support by email in office hours only (gap: no out-of-hours support) |
> | Security evidence | Independent security report requested; received; scope covers the messaging platform |
> | Sub-processors | Local carriers in each country (list requested) |
> | Data protection | Processing contract terms checked by adviser for two countries; two pending |
> | Fallback | None for text; app push covers most couriers |
> | Exit plan | Second provider tested in one country; switching is a configuration change taking about a day; message templates kept in Qafila's repository; numbers and history exported monthly |
> | Next review | Before renewal; and after any major incident |
> | Actions | Negotiate out-of-hours support at renewal; add the status page to the on-call runbook (done); finish data protection checks in two countries |

The draft contract with the integration partner went through the same questions. Yasmin noticed it said the partner would work in its own code repository and hand over "the final software" at the end; she raised it, and the contract was changed so the partner worked in Qafila's repository from day one, with Qafila reviewing every change. Faisal had wanted a fixed price; because the fifth country's rules were not yet clear, Bilal and Maha chose time and materials with a monthly cap and a review every month.

## 🛠️ Exercises
**🟢 Map one product's suppliers.** Choose a personal or open-source project, an app you use, or Qafila's courier app (which uses: the cloud provider, the messaging provider, the maps provider, the payment provider for payouts, a crash-reporting tool and an analytics tool). List every supplier, what breaks without it, any fallback, what data it holds, and a rank (critical, high, medium, low).
*Done when:* every supplier has all five fields, the ranks are justified in a phrase, and at least one supplier is ranked low with a reason.

<details><summary>Model answer and self-check</summary>

**Model answer.** Cloud provider: everything stops; no fallback; all data; critical. Payment provider: payouts stop; none; bank details; critical. Messaging: alerts missed; app push; phone numbers; high. Maps: routes slower; cached routes; locations; high. Crash reporting: bugs found later; logs; device data and possibly personal data in crash traces; medium. Analytics: decisions slower; none needed short-term; usage events; low to medium (check whether events include personal data).

**Self-check.**
- Did you rank by effect on the service, not by how much the supplier costs?
- Did you check what personal data each supplier actually receives, including in logs and crash reports?
- Did you find at least one supplier you would not have listed before you looked?

</details>

**🟡 Run the contract questions on real terms.** Find the public terms of service and data processing terms (if published) of one SaaS tool you use or could use, such as a free-tier monitoring, form or email tool. Answer the seven questions (scope, price and changes, service levels, data, security evidence, liability, term and exit) from what is published, and mark each answer "found", "unclear" or "not found".
*Done when:* all seven questions have an answer and a status, every "found" answer quotes or points to the section, and you list the two questions you would raise before relying on the tool for a business.

<details><summary>Model answer and self-check</summary>

**Model answer.** A typical result for a free-tier tool: scope found (service description page); price changes found ("we may change prices with notice"); service levels not found for the free tier; data partly found (data processing terms list sub-processors; deletion on account closure stated, timing unclear); security evidence found (security page mentions an independent report, available on request); liability found (capped at fees paid, which on a free tier is close to nothing); exit unclear (export available, format unclear). Questions to raise: what service level applies on a paid plan, and how long after closure is data deleted from backups?

**Self-check.**
- Did you avoid drawing legal conclusions, marking only what is stated or missing?
- Did you note that free tiers usually come with few or no service-level promises?
- Are your two questions ones a practitioner can raise with procurement or legal?

</details>

**🔴 Write an exit plan for a critical supplier.** For the maps provider in Qafila's courier app (or a critical supplier from your own map), write an exit plan: what data and configuration you would need to take, in what format; how you would test an alternative; how long a move would take and what would run in the meantime; what the contract should say about notice and help; and one design change that would make leaving easier.
*Done when:* the plan has all five parts, the time estimate is a range with its main driver, and the design change is specific enough to put on a backlog.

<details><summary>Model answer and self-check</summary>

**Model answer.** Data: cached routes and geocoded merchant addresses (Qafila's own records, exportable as files); configuration and keys (in Qafila's repository and secret store). Test: run a second provider in shadow mode in one city for two weeks, comparing estimated and actual delivery times. Time: 4 to 10 weeks; driver: how many services call the maps provider directly. Meanwhile: current provider stays on; cached routes cover short outages. Contract: at least 90 days' notice of price changes or termination; data export at no extra charge; no restriction on keeping geocoded addresses Qafila paid for (to confirm with legal). Design change: put all map calls behind one internal "location service" so switching provider changes one service, not twelve.

**Self-check.**
- Did you separate data Qafila owns from data the supplier owns?
- Is your time estimate a range with a named driver?
- Did you turn contract wishes into questions for legal rather than conclusions?
- Is the design change something one team could start next quarter?

</details>

## ⚠️ Mistakes and traps
- **Buying on the demo and the price.** A good demo says nothing about data, service levels or exit. Run the due-diligence checklist and the seven contract questions first.
- **Treating all suppliers the same.** Checking a team-chat tool as hard as the payment provider wastes effort. Rank suppliers by what breaks without them.
- **Trusting service credits.** A small credit off the bill rarely covers your loss. Design fallbacks for critical suppliers.
- **Letting knowledge leave with the outsourcing partner.** Require work in your repository and pipeline, review every change, and pair your own engineers with the partner.
- **No exit plan until it is needed.** In a dispute or an emergency it is too late to negotiate. Write the exit plan at signing.
- **Drawing legal conclusions yourself.** Raise gaps and questions; let legal, procurement and data protection advisers decide what the terms mean.

## 🧾 Recap
- Products depend on cloud providers, SaaS tools, API services, open-source components and people; each brings different risks.
- Practitioners check that contracts match the service: scope, price changes, service levels, data, security evidence, liability, exit.
- Map dependencies, rank suppliers by what breaks without them, and scale due diligence, review and fallbacks to the rank.
- Outsourcing moves work, not accountability; keep code, review and knowledge inside the company.
- Rule: you can hand over the work, never the accountability; know how you would leave before you sign.

## ✍️ Check yourself
**1. During the Friday messaging outage, what was the main supplier-management gap at Qafila?**

- A. Qafila had chosen a messaging provider that was too small for four countries.
- B. The messaging provider's contract had no service-level target written into it.
- C. Qafila should have built its own text-messaging system instead of buying one.
- D. No status page or out-of-hours support route was known for a high-rank supplier.

<details><summary>Answer</summary>

**D.** The forty minutes were lost because nobody knew where to look or whom to call, and support covered office hours only. A and C jump to conclusions about the choice of supplier, and B is contradicted by the register entry, which lists an availability target. See "Supplier status page list" and "Review suppliers, not just contracts".

</details>

**2. How should Qafila decide how much due diligence each supplier needs?**

- A. By the size of the yearly invoice, since expensive suppliers matter most.
- B. By what breaks without the supplier and what data it holds, as in the ranking.
- C. By applying the full checklist to every supplier equally, to be consistent.
- D. By the supplier's own description of how critical its service usually is.

<details><summary>Answer</summary>

**B.** Effort should follow the effect on the service and the data at stake. A confuses cost with importance (a cheap supplier can be critical), C wastes effort on low-risk tools, and D lets the supplier grade itself. See "Map dependencies before you rank them".

</details>

**3. The integration partner's draft contract says it will work in its own repository and hand over "the final software" at the end. What is the main risk Yasmin raised?**

- A. Qafila cannot review changes as they happen, and knowledge stays with the partner.
- B. The partner may charge more for work done in its own repository than in Qafila's.
- C. The partner's repository may use a different programming language from Qafila's.
- D. Handing over software at the end makes the project faster than Qafila can absorb.

<details><summary>Answer</summary>

**A.** Outsourcing moves work, not accountability; Qafila needs to see and review the code throughout and keep the knowledge. B and C are guesses not raised in the lesson, and D gets the risk backwards. See "Outsourcing work, not accountability".

</details>

**4. A supplier's contract offers a credit of a small part of the monthly fee if it misses its availability target. What should a practitioner conclude?**

- A. The credit fully protects Qafila, so no fallback for this supplier is needed.
- B. The credit means the supplier will never miss its target, so it can be trusted.
- C. The credit rarely covers the real loss, so critical suppliers still need fallbacks.
- D. The credit is a legal conclusion that the practitioner should approve on behalf of legal.

<details><summary>Answer</summary>

**C.** Service credits are usually small compared with the harm of an outage; reliability comes from design. A and B overrate the credit, and D gives the practitioner a legal decision that is not theirs. See "Why service levels from suppliers matter to you".

</details>

**5. When is the right time to write an exit plan for a critical supplier?**

- A. When the supplier announces a price increase that makes leaving worth considering.
- B. When an outage lasts long enough to breach the agreed service level in the contract.
- C. When the contract is close to renewal and procurement asks for alternatives.
- D. When signing, while relations are good and terms for leaving can still be agreed.

<details><summary>Answer</summary>

**D.** An exit plan is cheapest and most useful before you need it; notice periods and data-export help must be in the contract. A, B and C all wait until there is pressure, when options and leverage are weaker. See "Plan the exit at the start".

</details>

## 📚 References
- Regulation (EU) 2016/679 (General Data Protection Regulation), Article 28 "Processor", text on EUR-Lex: https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng. Required contract terms as reported in search summaries of the Article and of the UK Information Commissioner's Office guidance (not opened): https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/contracts-and-liabilities-between-controllers-and-processors-multi/what-needs-to-be-included-in-the-contract/
- Regulation (EU) 2022/2554 on digital operational resilience for the financial sector (DORA), EUR-Lex: https://eur-lex.europa.eu/eli/reg/2022/2554/oj. Application from 17 January 2025 and the Article 28 exit-strategy requirement for services supporting critical or important functions as reported in search summaries, including the Dutch AFM's page on third-party providers (not opened): https://www.afm.nl/en/sector/themas/belangrijke-europese-wet--en-regelgeving/dora/derde-aanbieders
- EY, "To the Point: AICPA revises guidance on applying its trust services criteria and SOC 2 description criteria" (SOC 2 and the AICPA Trust Services Criteria: security, availability, processing integrity, confidentiality, privacy; Type 1 and Type 2 reports as described in secondary guides; all as reported in search summaries; the AICPA's own pages were not opened): https://www.ey.com/en_us/technical/accountinglink/to-the-point-aicpa-revises-guidance-on-applying-its-trust-services-criteria-and-soc-2-description-criteria
- ISO, ISO/IEC 27001:2022 — Information security, cybersecurity and privacy protection — Information security management systems — Requirements (standard page; title and edition as reported in search summaries; not opened): https://www.iso.org/standard/27001
- Library course: [*Running IT as a Business*, lesson 10.2 — Sourcing, suppliers and multi-supplier integration](../itbiz/index.html#/10.2) (the manager's view of sourcing).
- Library course: [*Running IT as a Business*, lesson 5.3 — Third-party, SaaS and open-source components in the product](../itbiz/index.html#/5.3).
- Library course: [*AI Governance: Zero to Hero*, lesson 11.2 — Buying AI: vendor due diligence and contracts](../aigp/index.html#/11.2).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 7.2 — Costs, vendors and lock-in](../founder/index.html#/7.2).
- Library course: [*Secure AI & Application Security: Zero to Hero*, lesson 6.2 — The software supply chain: dependencies, SBOMs, SLSA and signing](../secai/index.html#/6.2) (open-source components as suppliers).
