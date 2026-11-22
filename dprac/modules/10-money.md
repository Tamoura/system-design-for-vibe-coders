# Module 10 — Money and suppliers

*Qafila is now Established. About 400 people work there in 35 teams, about 30,000 merchants in four countries use the app, and the system coordinates about 400,000 deliveries a day. A payments partner integration and a data platform have joined the merchant app, the courier app, the routing service and the internal platform. At this size, money stops being something Maha checks on a spreadsheet at night. Bilal, now CFO, runs a yearly budget, every team's cloud usage shows up on one large bill, and dozens of outside companies (a cloud provider, a payment provider, a messaging service, a maps service, tools for support and monitoring, contractors) sit inside the product's daily work. Early-career practitioners are asked to take part in all of this: to write the case for a piece of work, to explain why their service's costs went up, to help check a supplier. This module shows how, through Yasmin, now in her third year and a senior engineer on Courier Payouts, one of the teams in Qafila's Payments area. First, how digital work is funded: budgets, business cases sized to the decision, and funding long-lived products rather than one-off projects. Second, what it costs to run digital products, and how to measure cost per unit of value instead of staring at the size of the bill. Third, how to choose, contract and leave suppliers, and what can and cannot be handed to an outsourcing partner. Each lesson leaves an artefact: a one-page business case with a funding plan, a unit-cost sheet with a savings list, and a supplier register entry with an exit plan.*

> **Steps:** Invest — decide what digital work is worth paying for, know what the product costs to run for each unit of value it delivers, and buy from outside companies without losing control of your own service.

---

# 10.1 — Funding digital work: budgets, business cases and funding products
*Level: 🔴 Advanced* · *Prerequisites: 1.3, 6.1* · *Step: Invest*

**After this you can** write a one-page business case for a piece of digital work that compares at least three options (including doing nothing), shows one-off and running costs as ranges, states a measurable benefit and a stop rule, and asks for money in stages tied to evidence. *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- A **budget** plans what each part of the company may spend, usually for a year. A **business case** argues for spending on one piece of work.
- Work is **run** (keeping what exists working), **change** (new capability) or **obligation** (required by law, contract or a partner). Each is argued differently.
- Fund long-lived **products and teams**, judged on outcomes, rather than **projects** that end before the value arrives.
- The rule that matters most: **ask for money in the size of the next decision, and say in advance what would make you stop.**
- Decision cue: the bigger and harder to reverse the spend, the more evidence it needs. Small, reversible spends should be fast.
- Biggest trap: one option, one confident number, no running costs.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative, not benchmarks; money is in illustrative "units".

Every October, Bilal opens the budget round. At Launch, Maha decided over coffee; now there are 35 teams and a board that wants to know what the money buys. This year Bilal received 61 requests. Most had a single number, no options and no mention of running costs.

Yasmin's team wanted money too. Couriers are paid every week, and at each month-end the weekly runs are reconciled against what the payment provider actually sent. The payout service was written at Traction for one country; now it handles four, with country rules patched in by hand. Every month-end, two engineers spend about three days fixing the reconciliation, and couriers in the newest country complain about late or wrong payments. Yasmin's first draft of the case said "Rebuild payouts: 4 engineers, 9 months, 1.2 million units. Benefit: modern, scalable payouts."

Bilal sent it back: "What happens if we do nothing? What is the cheapest thing that would fix most of the pain? How will we know in three months whether it is working?" This lesson is how she answered.

## 📐 How it works

### 🟢 The essentials

**Budgets: the yearly plan.** A **budget** sets how much each part of the company may spend, usually for a year. It is a plan, not a prediction: finance teams **re-forecast** during the year (update the expected spend for the months that remain). Two words you will hear: **operating spend** ("opex"), money spent on running the business in the period, such as salaries and cloud bills; and **capital spend** ("capex"), money spent on something that gives value over several years, which accounting rules may let a company record as an asset. Whether building software counts as capital spend depends on accounting rules and company policy, so ask your finance team early; it changes which budget pays and what records (such as time sheets) you keep.

**Three kinds of work.** Before arguing for money, say what kind of work it is:

| Kind | What it is | How to argue for it | Qafila example |
|---|---|---|---|
| **Run** | Keeping what exists working and safe | Cost of the service, risk if neglected | On-call, patching |
| **Change** | New or better capability | Measured benefit | Faster merchant onboarding |
| **Obligation** | Required by law, contract or a partner | The obligation and its deadline, not invented customer value | Changes the payments partner requires |

**What a business case is.** A **business case** is a short, written argument that a piece of work is worth its cost and risk compared with the alternatives: a decision aid, not a sales brochure. Its parts:

1. **Problem and evidence.** What is wrong, for whom, and how you know (data, not opinion).
2. **Options.** At least three, always including **do nothing** and a **cheapest useful step**.
3. **Costs.** One-off costs (building) *and* running costs (people, cloud, licences, support) for several years, as ranges.
4. **Benefits.** What will change, measured, with a baseline and a date.
5. **Risks.** What could go wrong and what you would do.
6. **The ask and the stop rule.** How much money for which stage, and what result would make you stop or change course.

**Who decides what.** Most companies set **spending limits** for a team lead, a department head and the executives. At Qafila (illustrative), a team lead approves small tools, a department head such as Faisal approves spend within the department's budget, and anything larger goes to the executives, Bilal and Maha. Find your limits before you write; they tell you how formal your case needs to be.

### 🟡 Going deeper

**Size the case to the decision.** A small tool needs three sentences; a year of a team's time needs a page; a multi-year platform change needs more.

**Ranges, not single numbers.** Every estimate is uncertain. Give a low, likely and high figure, and say what drives the difference ("high if the fourth country's payout rules need a new payment method"). A study of 1,471 IT projects by Bent Flyvbjerg and Alexander Budzier (*Harvard Business Review*, 2011) reported an average cost overrun of 27%, but about one project in six overran its cost by around 200% on average. Averages hide this "fat tail": plan for the bad case, not only the average.

**Cost of delay.** **Cost of delay** is what you lose for each month the work is not done: revenue not earned, costs still paid, risk still carried (an idea associated with Don Reinertsen's 2009 book *The Principles of Product Development Flow*, and used for the backlog in lesson 6.1). For Courier Payouts, each month of delay is another month-end of fixes and late pay.

**Projects versus products.** A **project** has a start, an end, a fixed scope and a budget; when it closes, the team disperses and nobody owns the outcome. A **product** lives for years and keeps changing. **Product funding** gives a long-lived team a budget for a period (often a quarter or a year), agreed outcomes and guardrails (limits it must stay within), and reviews results regularly. For the manager's version, with the **portfolio** (the full set of work and products a company funds) and funding memos, see [*Running IT as a Business*, lesson 3.2 — Prioritising and funding work: business cases, cost of delay and funding products not projects](../itbiz/index.html#/3.2).

**Total cost of ownership.** The **total cost of ownership** is everything a system costs over its life, from building to retiring it. Software usually stays in use for years, and its running, support and change costs over those years can easily exceed the first build.

### 🔴 Expert view

**Fund in stages.** Split the work into stages and release money for each only when the previous one produced evidence. Stage one is small and fast: a prototype, a fix for the worst cause, a measurement. One large bet becomes several small ones, and stopping stays cheap.

**Write the stop rule before you start.** The **sunk cost effect** (described by Hal Arkes and Catherine Blumer in 1985) is continuing because of what has been spent, not because of what further spending will bring. The defence is to write, before the money is released, what result would make you stop. A stop line is usually looser than the target on purpose: it marks "this is not working", not "not yet perfect". Yasmin's case below aims for fixes below one day but stops only if they are still above 1.5 days after two month-ends.

**Opportunity cost is people.** Funding one piece of work means not doing something else with the same engineers. A good case names what will *not* be done.

**Benefits need an owner and a date.** A benefit nobody checks is a wish. Name who measures it, from which record, and when (lesson 6.3).

**The memorable rule.** Ask for money in the size of the next decision, and say in advance what would make you stop.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **One-page business case** | The six parts on one page | Any non-trivial request for money or time |
| **Options table** | Three or more options with one-off and yearly costs, benefit and risk | Before committing to one solution |
| **Staged funding plan** | Stages, money per stage, evidence to unlock the next | Work larger than a team-quarter |
| **Spending-limit table** | Who may approve how much | Before writing, to know who decides |
| **Total-cost-of-ownership sheet** | One-off and yearly costs over three to five years | Comparing build, buy and rebuild |

## 🏛️ In practice at Qafila
Yasmin rewrote her case. Illustrative and fictional; money in units.

> **Business case: Courier Payouts, month-end reliability (one page)**
>
> **Problem and evidence.** Month-end reconciliation of the weekly payout runs needs manual fixes: about 3 days of 2 engineers each month-end for six months (incident log). In the newest country, about 4% of couriers raised a payout ticket last month (support desk).
>
> **Options (costs as low / likely / high).**
>
> | Option | One-off cost | Yearly running cost | Main benefit | Main risk |
> |---|---|---|---|---|
> | A. Do nothing | 0 | About 14 engineer-weeks of fixes a year (3 days × 2 engineers × 12 month-ends), rising if the planned fifth country launches | None | Couriers leave; errors grow |
> | B. Fix the three worst causes (country rules in configuration, validation before each run, a reconciliation report) | 120k / 180k / 260k | 10k / 20k / 40k (keeping rules and the report up to date) | Most manual fixes removed | Some country cases remain hand-patched |
> | C. Full rebuild | 900k / 1.2m / 1.8m | About today's cost, plus 6–12 months of running old and new side by side | Clean design for future countries | Long; two systems run in parallel |
>
> **Recommendation.** B now, as stage one (about a quarter, 2 engineers). Decide on C with stage one's evidence.
>
> **Benefits and measures.** Month-end fixes below 1 day by the end of stage one; payout tickets in the newest country below 1% within two months. Owner: Yasmin's lead; review at the first month-end after release.
>
> **Risks.** A country rule is misread when moved into configuration: each country's rules are checked by its operations lead before release.
>
> **Stop rule.** If fixes are not below 1.5 days after two month-ends, stop and review the rebuild option with the evidence.
>
> **Not done instead.** The courier earnings screen redesign moves one quarter later.

Bilal approved stage one in ten minutes: it was small, measurable and had a stop rule. Faisal asked why not the rebuild; Yasmin showed that B removed most of the pain for about 15% of C's likely cost, and C stayed open. After two month-ends, fixes were down to half a day.

## 🛠️ Exercises
**🟢 Name the kind of work and the decision maker.** Label each as run, change or obligation: (1) renewing the observability tool's licence; (2) adding Arabic voice notes for couriers; (3) changing how card data is handled because the payments partner requires it; (4) upgrading the database before support for the old version ends. Say who would approve each.
*Done when:* every item has one label with a one-line reason, and each names a likely approver level (team lead, department head or executive).

<details><summary>Model answer and self-check</summary>

**Model answer.** (1) Run: keeps an existing service working. Team lead, within the existing budget. (2) Change: new capability for couriers. Department head (head of product), with a short case. (3) Obligation: a partner's contractual requirement with a deadline. Executive (Maha and Bilal), advised by Dana and legal. (4) Run, argued from risk: unsupported software is a security and reliability risk. Department head (Faisal), within the engineering budget.

**Self-check.**
- Did you avoid calling the partner's requirement "customer value"?
- Did you argue (4) from risk, not benefit?

</details>

**🟡 Turn a one-number request into an options table.** Qafila's routing team asks: "Buy a commercial route-optimisation service: 300k units a year. Benefit: better routes." Write an options table (including do nothing and a cheapest useful step) with one-off and yearly costs as ranges, a measurable benefit and the main risk for each.
*Done when:* the table has at least three options, every cost is a range with a basis, at least one benefit is a number with a baseline and a date, and running costs appear for every option.

<details><summary>Model answer and self-check</summary>

**Model answer.** Costs as low / likely / high; all illustrative.

| Option | One-off | Yearly running | Benefit | Main risk |
|---|---|---|---|---|
| A. Do nothing | 0 / 0 / 0 | 0 extra | None; distance per delivery stays at last quarter's baseline (routing records) | Courier time keeps rising with volume |
| B. Tune routing for the two busiest cities | 40k / 60k / 90k (one engineer, 2–4 months) | 5k / 10k / 20k (rule upkeep) | Distance per delivery down about 5% there within two months | Gains may not carry to other cities |
| C. Buy the service | 60k / 100k / 150k (two engineers, about a quarter) | 300k / 300k / 360k (vendor quote; high if renewal price rises) | Distance down 8–12% (vendor claim, to test) | Lock-in; sharing location data |
| D. Trial C in one city for two months | 15k / 25k / 40k (integration plus trial fee) | 0 unless C is chosen | Measured change against a similar city | Trial city may not be typical |

Recommendation: B now, D in parallel; decide on C from the trial.

**Self-check.**
- Did you treat the vendor's benefit as a claim to test?
- Does every option show a yearly running cost, including 0 for do nothing?

</details>

**🔴 Write a one-page business case with stages and a stop rule.** Use work from your own job or project, or Qafila's "merchant onboarding takes too long" problem (new merchants wait about 5 working days for activation, mostly for manual document checks; illustrative). Write a one-page case with all six parts, at least two funding stages and a stop rule.
*Done when:* the page fits on one side, includes all six parts and do nothing, gives costs as ranges with one-off and running parts, names a benefit owner and review date, and the stop rule is a measurable condition decided before the money is spent.

<details><summary>Model answer and self-check</summary>

**Model answer.** All figures illustrative; costs as low / likely / high.
- **Problem and evidence:** activation takes about 5 working days; about a fifth of sign-ups never complete (onboarding funnel).
- **Options:** (A) do nothing: one-off 0, running 0 extra; sign-ups keep being lost. (B) Stage one, a checklist and shared queue: one-off 10k / 15k / 25k (2 weeks of an engineer and an operations specialist), running 0 / 2k / 5k a year. (C) Stage two, automated document checks with a supplier: one-off 80k / 120k / 180k (3 months), running 40k / 60k / 90k a year (fee and upkeep).
- **Benefit:** median activation under 2 working days within a quarter. Owner: onboarding product manager; review at quarter end.
- **Risks:** the supplier rejects valid documents in one country (test a sample from each country first); merchant documents go to a supplier (due diligence first, lesson 10.3).
- **Ask:** money for stage one only; stage two decided at its review.
- **Stop rule:** if stage one does not cut median activation below 3 days within six weeks, do not start stage two until the cause is understood.

**Self-check.**
- Is stage one small enough to produce evidence within weeks?
- Could a sceptical finance colleague check every number's basis?
- Does the stop rule name a number and a date, not a feeling?

</details>

## ⚠️ Mistakes and traps
- **One option, one number.** It invites a yes-or-no fight. Compare at least three options and give ranges.
- **Forgetting running costs.** Over a system's life they can outweigh the build. Add them for every option.
- **Vague benefits.** "Modern, scalable" is not a benefit. Write who will do what differently, by how much, by when.
- **Asking for everything at once.** It makes stopping expensive. Fund in stages, each unlocked by evidence.
- **Deciding accounting treatment yourself.** Capital or operating spend is for finance to decide. Ask early.
- **Disguising obligations.** Argue required work from the requirement and its deadline.

## 🧾 Recap
- Budgets plan a year's spend; business cases argue for one piece of work against alternatives.
- Label work as run, change or obligation.
- A good case has evidence, options including do nothing, costs as ranges with running costs, measured benefits, risks, and an ask with a stop rule.
- Fund long-lived products for a period; fund large uncertain work in stages.
- Rule: ask for money in the size of the next decision, and say in advance what would make you stop.

## ✍️ Check yourself
**1. Yasmin's first draft asked for 1.2 million units for a rebuild, with "modern, scalable payouts" as the benefit. What was most missing?**

- A. A more detailed technical design of the new payout service, so finance could check it.
- B. A stronger statement of urgency from the Head of Engineering to support the request.
- C. Alternatives including do nothing, costs as ranges and a benefit that can be measured.
- D. A comparison with what similar companies in other countries spend on courier payouts.

<details><summary>Answer</summary>

**C.** Without alternatives and a measure, Bilal cannot judge the case. A adds detail but no decision basis, B is persuasion, not evidence, and D says nothing about Qafila's options. See "What a business case is".

</details>

**2. Which of these is the best stop rule for Qafila's onboarding work?**

- A. Stop if more than 60,000 units have been spent by the end of the second month of stage one.
- B. Stop if median activation is not below 3 working days six weeks into stage one.
- C. Stop if median activation has not improved when measured after the full rebuild is complete.
- D. Stop on 30 June if the team then agrees the work is no longer delivering enough value.

<details><summary>Answer</summary>

**B.** A stop rule is a measurable result with a date, set before spending. A measures spending, not results; C measures only after all the money is gone; D has a date but no measure. See "Write the stop rule before you start".

</details>

**3. The payments partner requires Qafila to change how card data flows by a fixed date. How should the team present this work?**

- A. As change work, with a forecast rise in merchant satisfaction to win priority.
- B. As run work, since it touches an existing service and needs no new capability.
- C. As a technical debt item, to be scheduled when the team has spare capacity.
- D. As obligation work, argued from the partner's requirement and its deadline.

<details><summary>Answer</summary>

**D.** Partner-required work is an obligation, argued from the requirement and date. A dresses it up as customer value, B ignores the deadline and new work, and C risks missing the date. See "Three kinds of work".

</details>

**4. The routing team's case for a new internal tool shows one cost: 150k units to build it. What is the most important gap?**

- A. Yearly running, support and change costs over the years the tool will be in use.
- B. A 10% contingency added to the build cost so the single number is safer.
- C. A split of the build cost into capital and operating spend, made by the team itself.
- D. A comparison with what competitors are reported to spend on similar tools.

<details><summary>Answer</summary>

**A.** Total cost of ownership covers years of running, support and change, which can exceed the build. B keeps one confident number, C is finance's decision, and D says nothing about Qafila's costs. See "Total cost of ownership".

</details>

**5. Faisal wants the routing rebuild funded as one 18-month request so "we don't have to keep asking". What is the strongest reason to stage it?**

- A. Smaller requests usually pass finance faster, so the team spends less time waiting.
- B. Each stage can be given to a different team, which spreads knowledge of routing.
- C. Each stage produces evidence before more money is released, so stopping stays cheap.
- D. Stages let the team revise its outcome measures after each one to fit the results.

<details><summary>Answer</summary>

**C.** Staging turns one large bet into smaller ones, each unlocked by evidence. A is not the reason, B is unrelated to funding risk, and D defeats measures set in advance. See "Fund in stages".

</details>

## 📚 References
- Flyvbjerg, B. and Budzier, A., "Why Your IT Project May Be Riskier Than You Think", *Harvard Business Review* 89(9), 2011. 1,471 projects, 27% average overrun, about one in six averaging about 200%, per the arXiv abstract (checked for claims row itbiz-03-009; not re-opened here): https://arxiv.org/abs/1304.0265
- Reinertsen, D. G., *The Principles of Product Development Flow* (Celeritas, 2009). Cost of delay, as reported; not opened.
- Arkes, H. R. and Blumer, C., "The psychology of sunk cost", *Organizational Behavior and Human Decision Processes* 35(1): 124–140 (1985). As reported; not opened.
- Library course: [*Running IT as a Business*, lesson 3.2 — Prioritising and funding work: business cases, cost of delay and funding products not projects](../itbiz/index.html#/3.2).
- Library course: [*Running IT as a Business*, lesson 10.1 — IT financial management: cost models, unit costs and the cost of a product](../itbiz/index.html#/10.1).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 3.1 — Unit economics in plain words, including AI and model costs](../founder/index.html#/3.1).

---

# 10.2 — The cost of running digital products: cloud costs and unit economics
*Level: 🔴 Advanced* · *Prerequisites: 1.3, 4.1* · *Step: Invest*

**After this you can** read a cloud bill by service and by team, calculate the cost per unit of value for one product (such as cost per 1,000 deliveries), explain a month's change in that number, and draw up a ranked list of savings that does not weaken the reliability target. *Study time: reading about 20 min, hands-on about 85 min (estimate).*

## ⚡ In 60 seconds
- In the cloud, every engineer who creates or resizes a resource is spending money. Cost is a design decision.
- The bill has a few big parts: compute, storage, data transfer, managed services and outside services (messaging, maps, AI models). People's time sits outside it.
- **Unit cost** is cost divided by units of value (deliveries, payouts). It shows whether growth is efficient; the total bill cannot.
- The rule that matters most: **measure cost per unit of value, not just the size of the bill.**
- Decision cue: before cutting, ask what the cost buys. Savings that break the 99.9% reliability target or slow every team are not savings.
- Biggest trap: costs nobody owns, such as untagged resources and forgotten test environments.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative, not benchmarks; money is in illustrative "units".

In March, Bilal brought one chart to the leadership meeting: over a year, Qafila's monthly cloud bill had grown by about 70%, deliveries by about 35%. "Either we are buying something valuable with that difference, or we are wasting it. Which?" Nobody could answer. About a fifth of the spend carried no tag saying which team owned it.

Faisal asked each team to explain its own costs. Yasmin's team, Courier Payouts, had never looked. In one afternoon she found a full copy of the production database kept for testing and never switched off, logs kept forever at the most expensive storage level, and a nightly report that copied all payout data across regions. None had been a decision; each had been a default. This lesson shows how to read such costs, measure them per unit of value and reduce them without breaking anything.

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

Outside services often arrive on separate invoices and are easy to forget. Count them. In the cloud an engineer can create a large database in minutes, so every instance size, retention setting and region choice is a small spending decision.

**Tags and ownership.** A **tag** (or label) is a short piece of text attached to a cloud resource, such as `team=courier-payouts` or `env=test` (lesson 4.1). With tags, the bill can be split by team, product and environment; without them, cost is one number nobody owns. In **showback**, each team sees its costs but a shared budget pays; in **chargeback**, each team's own budget pays. Showback is usually the right start.

**Reading the bill by team and service.** With tags, the provider's cost tools group the bill by team, service or both. Sort by the biggest rise since last month, then ask of each line whether the rise was a decision (a new feature, a new country) or something left running.

**Unit cost.** **Unit cost** is cost divided by units of value delivered in the same period. Lesson 1.3 chose Qafila's unit: a delivery coordinated, read per 1,000 at this scale. A monthly cost of 360,000 units for about 12 million deliveries (about 400,000 a day) is 30 units per 1,000 deliveries. The bill can rise while unit cost falls; that is healthy growth. If unit cost rises, something needs explaining.

### 🟡 Going deeper

**Fixed and variable at scale.** Some costs grow with deliveries (messages, map calls), some with teams or countries (test environments, data stores). A cost that grows with *time* rather than use, such as data kept forever, is a warning sign: it rises even if the business stands still.

**The usual savings, roughly in order of ease.**

| Lever | What it means | Typical risk |
|---|---|---|
| **Switch off what is idle** | Stop test environments at night and weekends; delete forgotten resources | Low, if owners agree first |
| **Right-size** | Match machine and database sizes to actual use | Low to medium; check peak load |
| **Storage levels and retention** | Move old data to cheaper storage; delete what you no longer need (within the retention rules from lesson 9.2) | Medium; slower to read old data back |
| **Commitment discounts** | Promise the provider a level of use for a period (often a year or more) in return for a lower price | Medium; you pay even if use falls |
| **Design changes** | Avoid copying data between regions, cache map lookups, batch messages | Higher effort; best done with an architecture decision record (lesson 9.1) |

Prices, discounts and limits change; check the provider's current documentation before relying on any of them.

**Waste is common, and reported.** Flexera, which sells cost-management software, surveys cloud users each year. In its 2025 report, respondents reportedly estimated that about 27% of their spend on cloud infrastructure and platform services (IaaS and PaaS) was wasted, and 84% said managing cloud spend was a challenge, the most often cited. The 2026 report reportedly put the IaaS and PaaS estimate at 29%, the first rise in five years, linked to AI. These are self-reported vendor-survey estimates: a conversation starter, not a target.

**FinOps.** **FinOps** is a practice that brings engineering, finance and business people together so that technology spending is visible, owned by the people who cause it, and weighed against its value. The FinOps Foundation (part of the Linux Foundation) publishes the FinOps Framework on its own site. FinOps began with cloud bills; in 2026 the Foundation widened its definition from cloud to technology spending in general (reported). For hands-on depth with real tools, see [*Cloud & DevOps: Zero to Hero*, lesson 6.2 — FinOps: understanding, allocating and cutting cloud cost](../cloud/index.html#/6.2).

### 🔴 Expert view

**Cost is a quality attribute.** As in lesson 9.1, weigh cost like speed: when you design a feature, ask what it will cost per 1,000 deliveries. A design that triples data transfer is a cost decision, whether or not anyone called it one.

**Do not save your way out of reliability.** Order tracking targets 99.9% a month. Removing a **standby copy** (a second database kept ready to take over if the main one fails) or shrinking capacity below peak load may lower the bill and break that promise. Every saving on a production system should say what it does to reliability and who agreed. Cheap and down is not a bargain.

**Watch for surprises, not only totals.** Set **budget alerts** (a message when a team's spend passes a threshold) and **anomaly alerts** (a message when spend jumps unusually fast). A runaway job found the same day costs a little; found at month-end, it costs a month.

**AI and other per-call costs.** Per-call services (messaging, maps, AI models) grow with use and change fastest; an AI assistant's cost per conversation belongs in the unit-cost sheet from day one. See [*Founder's Playbook for AI-First Builders*, lesson 3.1 — Unit economics in plain words, including AI and model costs](../founder/index.html#/3.1).

**People are still a cost to serve.** Support time, manual fixes (lesson 10.1) and on-call load are costs per unit too.

**The memorable rule.** Measure cost per unit of value, not just the size of the bill.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Unit-cost sheet** | Monthly cost by part, units, cost per 1,000, change with reasons | Monthly, per product or service |
| **Tagging policy** | Required tags and a check that blocks untagged resources | Before anyone creates cloud resources |
| **Provider cost tools** | The provider's billing pages and cost explorer (a page that groups and charts spend by service, tag and time) | Weekly look at spend; investigating a jump |
| **Budget and anomaly alerts** | Messages when spend passes a threshold or jumps unusually | Once per team and environment |
| **Savings list** | Each idea with saving, effort, reliability risk, owner, status | After each monthly review |
| **Cost estimate in pull requests** | Tools such as Infracost (an example, not an endorsement) that estimate the cost of an infrastructure-as-code change | When infrastructure is reviewed as code (lesson 4.1) |

## 🏛️ In practice at Qafila
Yasmin built the first unit-cost sheet for Courier Payouts. Illustrative and fictional; money in units.

> **Courier Payouts: unit-cost sheet, March**
>
> Unit of value: payouts completed (one per courier per weekly pay run; roughly 50,000–55,000 couriers are paid each week). Payouts: February about 211,000; March about 220,000.
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
> | **Cost per 1,000 payouts** | **about 143** (30,200 ÷ 211) | **about 143** (31,500 ÷ 220) | Flat: growth paid for, waste hidden |
>
> **Savings list.**
>
> | Idea | Estimated monthly saving | Effort | Reliability risk | Owner |
> |---|---|---|---|---|
> | Stop the test database outside working hours; use a smaller masked copy | 2,500–3,000 | 2 days | None (not production) | Yasmin |
> | Logs: 30 days fast, then cheaper storage, delete after the agreed retention period | 1,500–2,200 | 3 days | Low; older logs slower to search | Yasmin, with Dana for retention |
> | Nightly report reads in one region | about 1,500 | 1 week | Low; report runs later | Data platform team |
> | Commitment discount for payout compute | Small | Finance decision | None, but locks in use | Bilal's team |

Yasmin's first draft also removed the payout database's standby copy. Salma stopped it: the weekly runs depend on that database, and a failure on a pay day with no standby would breach the courier contracts. Dana pointed out that the test copy held real courier bank details and should have been masked anyway. After two months, cost per 1,000 payouts fell to about 115 (illustrative), and Faisal asked every team for a sheet like it.

## 🛠️ Exercises
**🟢 Read a bill and explain a unit cost.** Illustrative figures: January 330,000 units for 11 million deliveries; February 345,000 for 11.2 million; March 390,000 for 11.3 million. By team and service:

| Team: service | February | March |
|---|---|---|
| Orders: compute and database | 92,000 | 95,000 |
| Routing: compute | 70,000 | 71,000 |
| Routing: maps provider (outside service) | 38,000 | 52,000 |
| Data platform: storage and queries | 55,000 | 58,000 |
| Data platform: cross-region transfer | 12,000 | 12,500 |
| Notifications: messaging provider | 30,000 | 30,500 |
| No team tag | 48,000 | 71,000 |
| **Total** | **345,000** | **390,000** |

Calculate cost per 1,000 deliveries for each month, say which month needs explaining, name the two lines that drove most of its rise, and write a question for each.
*Done when:* you have three unit costs to one decimal place, the two drivers together explain most of March's 45,000 rise, and each driver has a question aimed at a cause.

<details><summary>Model answer and self-check</summary>

**Model answer.** January: 330,000 ÷ 11,000 = 30.0 per 1,000. February: 345,000 ÷ 11,200 ≈ 30.8. March: 390,000 ÷ 11,300 ≈ 34.5. March needs explaining: cost rose 45,000 (about 13%) while deliveries grew under 1%. Driver 1: untagged spend, up 23,000. Question: "Who created the new untagged resources this month, and are they still needed?" Driver 2: the maps provider, up 14,000 with almost flat deliveries. Question to Routing: "Did a change make more map calls per delivery (a new feature, a lost cache), or did the price per call change?" Together they explain 37,000 of the 45,000; the rest is small rises spread across teams.

**Self-check.**
- Did you sort lines by their change, not their size?
- Are your questions aimed at a cause, not a culprit?

</details>

**🟡 Tag and allocate.** Use your own cloud account (a free tier is fine) or this Qafila list: order database (no tags), "test-db-old" (no tags), routing cluster (`team=routing`), payout service (`team=courier-payouts`, `env=prod`), a storage bucket named "tmp-export-2025" (no tags). Write a tagging policy with four required tags and, for each untagged resource, a question to find its owner and whether it is still needed.
*Done when:* the policy names four tags with allowed values, every untagged resource has an owner question and a "keep, resize or delete" proposal, and nothing is deleted without the agreement of its owner (or, if no owner is found, of the lead who takes it over).

<details><summary>Model answer and self-check</summary>

**Model answer.** Policy: `team` (from the team list), `product` (merchant, courier, routing, payouts, platform, data), `env` (prod, staging, test, dev), `purpose` (free text, under 40 characters); new resources without them are blocked by a check in the pipeline. Order database: "Which team owns the order database?" Likely the Orders team; keep and tag. test-db-old: "Who created it, and is anything reading from it?" Check access logs; delete once an owner agrees, or, if no owner is found after two weeks, escalate to the platform team lead, who takes ownership and decides. tmp-export-2025: "What is in it, and does it hold personal data?" Check with Dana; delete once the owner agrees, or apply the retention rule.

**Self-check.**
- Is the policy enforced, not just written?
- Does every deletion wait for a named person's agreement?

</details>

**🔴 Build a savings list that protects reliability.** From Yasmin's sheet (or a service you know), list at least four savings ideas, each with a saving range, effort, effect on reliability or other teams, an owner and a recommendation. Rank them.
*Done when:* every idea has all six fields, at least one idea is rejected or deferred for a stated reliability or security reason, and the ranking puts low-risk, high-saving, low-effort ideas first.

<details><summary>Model answer and self-check</summary>

**Model answer.** (1) Schedule the test database off outside working hours and use a masked, smaller copy: 2,500–3,000 a month, 2 days, no production effect, owner Yasmin, recommend first. (2) Log retention and cheaper storage after 30 days: 1,500–2,200, 3 days, older logs slower to search, owner Yasmin with Dana, recommend. (3) Nightly report reads in one region: 1,200–1,600, a week, report later in the morning, owner data platform team, recommend after checking who reads it. (4) Commitment discount for compute: small, finance decision, locks in use for a period, owner Bilal's team, defer until the design settles. (5) Remove the payout database standby: 1,500–2,500, 1 day, breaks recovery on pay days and risks the courier contracts, owner Yasmin, reject.

**Self-check.**
- Did you record why the rejected idea was rejected, so it does not return?
- Are savings ranges, not single numbers?

</details>

## ⚠️ Mistakes and traps
- **Watching only the total bill.** Track cost per unit of value and explain its changes.
- **Untagged resources.** Require tags and block resources without them.
- **Saving at reliability's expense.** Every production saving states its reliability effect and who agreed.
- **Forgetting outside services and people.** Put messaging, maps, AI calls and manual work on the same sheet.
- **Keeping data forever by default.** Set retention with the data owner (lesson 9.2).
- **Trusting old price assumptions.** Check current terms before relying on a price.

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
- D. How much the bill would fall if non-production environments were switched off at night.

<details><summary>Answer</summary>

**A.** Unit cost and its drivers show whether the extra spend bought value. B jumps to switching providers, C cuts good and bad spending alike, and D is a sensible saving that answers a different question. See "Unit cost".

</details>

**2. In March, spend with no team tag rose from 48,000 to 71,000 units. What should the platform team do first?**

- A. Ask finance to spread the untagged spend across all teams' budgets in proportion to size.
- B. Delete untagged resources older than one month, since nobody has claimed them yet.
- C. Move every team to chargeback so that each one pays for whatever it cannot disown.
- D. Find who created the untagged resources, get them tagged, then block new untagged ones.

<details><summary>Answer</summary>

**D.** Finding owners and then enforcing tags fixes the cause. A hides the cost, B deletes without agreement and may break something in use, and C starts accounting fights before owners are known. See "Tags and ownership".

</details>

**3. The data platform team proposes switching off the order database's read replica (a copy used for reports and as a standby) to save about 3,000 units a month. What should come first?**

- A. Approval, since this saving is larger than any other item on this month's savings list.
- B. A check of what the replica does for recovery and the 99.9% target, agreed by its owner.
- C. Approval from finance, since the decision is about a cost that appears on the monthly bill.
- D. Deferral to next year's budget round, when all savings ideas are reviewed side by side.

<details><summary>Answer</summary>

**B.** A production saving must state its reliability effect and who agreed. A ignores risk, C hands a reliability decision to finance, and D delays a decision that could be made now. See "Do not save your way out of reliability".

</details>

**4. A vendor survey reports that respondents estimate about a quarter of their cloud infrastructure spend is wasted. How should Qafila use that figure?**

- A. As a target: cut exactly that share of every team's bill this year.
- B. As evidence for the board that Qafila probably wastes a similar share.
- C. As a prompt to look for waste, not as a measure of Qafila's own spending.
- D. As a benchmark to compare Qafila's measured waste against each quarter.

<details><summary>Answer</summary>

**C.** A self-reported vendor-survey estimate suggests where to look but says nothing exact about Qafila. A and B treat it as a fact about Qafila, and D treats it as a reliable benchmark. See "Waste is common, and reported".

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
- FinOps Foundation, "What is FinOps?" (defines FinOps around the business value of technology, with a heritage in cloud; checked for claims row itbiz-10-004 on 2026-11-20, not re-opened here): https://www.finops.org/introduction/what-is-finops/
- FinOps Foundation, "2026 FinOps Framework" and "Mission update" (the 2026 widening from cloud to technology, as reported in search summaries; not opened): https://www.finops.org/insights/2026-finops-framework/ and https://www.finops.org/insights/mission-update/
- Flexera, press release "New Flexera Report Finds that 84% of Organizations Struggle to Manage Cloud Spend", 19 March 2025 (84%; 27% IaaS and PaaS waste; 759 respondents; as reported, not opened): https://www.flexera.com/about-us/press-center/new-flexera-report-finds-84-percent-of-organizations-struggle-to-manage-cloud-spend
- Flexera, press release "Flexera Finds Cloud Value is Rising While AI Waste Grows" (2026; 29% IaaS and PaaS waste; 753 respondents; as reported, not opened): https://www.flexera.com/about-us/press-center/flexera-finds-cloud-value-is-rising-while-ai-waste-grows
- Infracost, open-source repository (as reported; not opened): https://github.com/infracost/infracost
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 6.2 — FinOps: understanding, allocating and cutting cloud cost](../cloud/index.html#/6.2).
- Library course: [*Running IT as a Business*, lesson 10.1 — IT financial management: cost models, unit costs and the cost of a product](../itbiz/index.html#/10.1).
- Library course: [*AI Product Management*, lesson 8.2 — Unit economics: cost to serve, pricing models and margins](../aipm/index.html#/8.2).

---

# 10.3 — Suppliers, contracts and outsourcing
*Level: 🔴 Advanced* · *Prerequisites: 2.3, 7.3* · *Step: Invest*

**After this you can** list the outside suppliers one product depends on and rank them by how much the service would suffer without them, run a basic due-diligence check on a new supplier, read a contract summary for the terms that matter to practitioners (scope, price changes, service levels, data, security evidence, exit), and write an exit plan for one supplier. *Study time: reading about 20 min, hands-on about 110 min (estimate).*

## ⚡ In 60 seconds
- Every product depends on **suppliers**: cloud providers, software-as-a-service tools, APIs (messaging, maps, payments), open-source components and people (contractors, outsourcing partners).
- A **contract** sets what the supplier does, at what price, to what standard, with what data, and how either side can leave. Practitioners check it gives the service what it needs.
- **Due diligence** is checking a supplier before relying on it: data, security, reliability, and what happens if it fails or you leave.
- The rule that matters most: **you can hand over the work, never the accountability; know how you would leave before you sign.**
- Decision cue: the closer a supplier sits to the core service, the more checking and the better the exit plan it needs.
- Biggest trap: signing on a good demo and a low price.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

On a Friday evening in the busiest week of the year, couriers in one of Qafila's four countries stopped receiving order texts. The messaging provider had a problem with a local carrier. It took Salma's team forty minutes to find out: nobody had the supplier's status page bookmarked, and support covered email in office hours only.

The following Monday, the maps provider gave notice of a price rise per lookup from the next quarter. And Maha had agreed with a software company abroad to build the integration for a planned fifth country; the draft contract had arrived, and nobody in engineering had read it.

Meanwhile the payments partner's due-diligence questionnaire (Module 11) asked Qafila to list the suppliers that handle merchant or courier data and show how it controls them. Dana asked Yasmin, who knew the code that called outside services, to help. This lesson is what they learned.

## 📐 How it works

### 🟢 The essentials

**Kinds of supplier.** Suppliers come in several shapes, and each brings different risks:

| Kind | What you buy | Qafila example | Typical risk |
|---|---|---|---|
| **Cloud provider** | Computing, storage, managed services | The main cloud provider since Launch | Deep dependency; hard to leave |
| **Software-as-a-service (SaaS) tool** | Software someone else runs, used through a browser or API | Support desk, monitoring, team chat | Holds your data; price and terms change |
| **API service** | A function called by your code | Messaging, maps, payment provider | On the critical path; outages are your outages |
| **Open-source component** | Code you include, often free | Libraries in every service | No contract at all; security and upkeep are yours |
| **People** | Contractors or an outsourcing partner doing work for you | The integration team for the planned fifth country | Knowledge and quality leave with them |

Lesson 2.3 covered build or buy; here the question is managing many suppliers.

**The terms that matter to practitioners.** Legal and procurement write contracts, but they cannot check that a contract matches how the service really works; you can. Read for these:

| Term | Plain question to ask |
|---|---|
| **Scope** | What exactly will they provide, and what is excluded? |
| **Price and changes** | How is it charged (per user, per call, per month)? How much notice before prices change? |
| **Service levels** | What availability and support response do they promise, measured how, and what if they miss it? |
| **Data** | What data will they hold, where, who sees it, which other companies get it, and how is it returned or deleted? |
| **Security evidence** | What independent evidence do they offer (audit reports, certifications), and how will they tell us about a breach? |
| **Liability** | If they cause us harm, what are they responsible for, and up to what limit? |
| **Term and exit** | How long is the contract, how do we leave, how much notice, and what help do we get to move our data? |

You are not deciding what these mean legally; you are spotting gaps and raising them with the people who decide.

**Why supplier service levels matter to you.** Lesson 7.3 showed that two services in a chain, each available 99.9%, give about 99.8% together. Your promise to merchants cannot be stronger than your critical suppliers allow, unless you add a fallback. A missed supplier target usually earns a small credit off the bill, which rarely covers your actual loss.

### 🟡 Going deeper

**Map dependencies before you rank them.** A **supplier dependency map** lists every outside service a product uses and what happens if it stops. Yasmin searched the code for outside API calls and the finance system for invoices; each found suppliers the other missed.

| Supplier | What breaks without it | Fallback today | Data it holds | Rank |
|---|---|---|---|---|
| Messaging provider | Couriers miss order alerts (app push still works) | None for text | Courier phone numbers | High |
| Maps provider | Routing slower, estimates worse | Cached routes for 1 hour | Addresses, locations | High |
| Payment provider | Merchants cannot pay; payouts stop | None | Payment and bank details | Critical |
| Support desk tool | Agents work from email | Email inbox | Merchant and courier messages | Medium |
| Team chat | Inconvenient, not customer-facing | Email, phone | Internal messages | Low |

Critical and high suppliers need careful contracts, review, a fallback and an exit plan; low ones need a register entry and a yearly check.

**Due diligence in proportion.** **Supplier due diligence** is checking a supplier before you rely on it: a short pass for a low-risk tool, evidence for a critical one. A basic checklist:

| Check | What to look for | Where to find it |
|---|---|---|
| **Security evidence** | An independent report or certification, and what it covers | The supplier's security or trust page; ask for the report |
| **Reliability history** | Incidents in the last year, how long, how openly explained | Status page and incident history |
| **Sub-processors** | Which other companies (sub-processors) handle your data, and where | Data processing terms or sub-processor list |
| **Deletion and export** | How you get data out; when it is deleted after you leave | Terms, help pages |
| **Business health** | Will they be there in three years? | Finance or procurement |

Two common kinds of security evidence: a **SOC 2 report**, an independent auditor's report under criteria set by the AICPA (the American Institute of Certified Public Accountants), and certification to **ISO/IEC 27001**, the international standard for information security management systems. Read the scope: a certificate covering one office says nothing about your service.

**Data protection rules reach into contracts.** Many data protection laws require a written contract when a supplier processes personal data for you. Article 28 of the EU's General Data Protection Regulation (GDPR), for example, is reported to require terms such as acting only on documented instructions, keeping data secure, using sub-processors only with authorisation, and deleting or returning data at the end. For each new supplier ask: "does our data protection law require specific terms here, and has our adviser checked them?" For AI suppliers, see [*AI Governance: Zero to Hero*, lesson 11.2 — Buying AI: vendor due diligence and contracts](../aigp/index.html#/11.2).

**Outsourcing work, not accountability.** **Outsourcing** is paying another company to do work you would otherwise do: building a feature, running night support, operating a system. Contracts are commonly **fixed price** (good for small, well-understood work; every change becomes a negotiation), **time and materials** (pay for time; fits uncertain work you steer closely, but cost can grow) or **outcome-based** (pay for measured results; hard to define fairly). Whatever the contract, Qafila stays accountable for what the supplier builds or runs. Safeguards: the partner works in Qafila's repository and pipeline, with Qafila reviewing every change (lesson 3.1); documentation and handover are paid deliverables; and a Qafila engineer pairs with the partner so the knowledge stays.

### 🔴 Expert view

**Plan the exit at the start.** **Lock-in** is when leaving a supplier would be so costly or slow that you effectively cannot. Some lock-in is a fair price for speed; the danger is lock-in you did not choose. An **exit plan** answers: how do we get our data out, in what format, how long would moving take, what runs meanwhile, and what does the contract say about notice and help? Write it while relations are good. See also [*Founder's Playbook for AI-First Builders*, lesson 7.2 — Costs, vendors and lock-in](../founder/index.html#/7.2).

**Regulated customers pass their rules down.** The payments partner's regulators expect it to control its suppliers, Qafila included, and so it asks about Qafila's own suppliers too. For example, the EU's Digital Operational Resilience Act (DORA, Regulation (EU) 2022/2554), applying to EU financial firms from 17 January 2025, is reported to require exit strategies for ICT (information and communication technology) services supporting their critical or important functions (roughly, those whose failure would seriously harm the firm or its customers). Ask: "what does our partner's regulation expect of its suppliers, and what will we have to show?" (Module 11).

**Price-change notice is a design input.** The maps price rise will move cost per 1,000 deliveries (lesson 10.2). Caching lookups, batching calls or keeping a second provider ready reduces that exposure.

**Review suppliers, not just contracts.** Critical suppliers get a named owner, a yearly review (service levels, incidents, price, security evidence, exit plan) and a check whenever something changes: a new data type, a new country, an acquisition.

**The memorable rule.** You can hand over the work, never the accountability; know how you would leave before you sign.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Supplier register** | One row per supplier: what it does, owner, data, rank, contract and review dates | Once you have more than a handful |
| **Supplier dependency map** | Outside services, what breaks, fallback, rank | Before ranking; before a reliability review |
| **Due-diligence checklist** | The five checks above, scaled to the rank | Before signing or adding a data type |
| **Contract terms question sheet** | The seven plain questions | When a draft or renewal arrives |
| **Exit plan** | Data out, move time, what runs meanwhile, notice and help | Every critical and high supplier, at signing |
| **Supplier status page list** | Status pages and support contacts, linked from the runbook | Before the next incident |

## 🏛️ In practice at Qafila
Dana and Yasmin built the supplier register. Illustrative and fictional.

> **Supplier register entry: messaging provider (texts to couriers and shop customers)**
>
> | Field | Entry |
> |---|---|
> | What it does | Sends order alerts and delivery updates by text in all four countries |
> | Internal owner | Salma (service); Bilal (contract) |
> | Rank | High: couriers miss alerts; app push still works |
> | Data held | Courier and shop-customer phone numbers; message text |
> | Contract | Yearly, auto-renews unless cancelled with 60 days' notice; per message; 30 days' notice of price changes |
> | Service levels | Availability target stated; email support in office hours only (gap) |
> | Security evidence | Independent report received; covers the messaging platform |
> | Sub-processors | Local carriers in each country (list requested) |
> | Data protection | Contract terms checked by adviser in two countries; two pending |
> | Exit plan | Second provider tested in one country; switching takes about a day; templates in Qafila's repository |
> | Next review | Before renewal and after any major incident |
> | Actions | Negotiate out-of-hours support; status page added to the runbook (done) |

The integration partner's draft contract went through the same questions. Yasmin noticed the partner would work in its own repository and hand over "the final software" at the end; the contract was changed so it worked in Qafila's repository from day one, with Qafila reviewing every change. Because the planned fifth country's rules were unclear, Bilal and Maha chose time and materials with a monthly cap over Faisal's fixed price.

## 🛠️ Exercises
**🟢 Map one product's suppliers.** Use your own project, an app you use, or Qafila's courier app (cloud provider, messaging, maps, payment provider for payouts, a crash-reporting tool, an analytics tool). List each supplier, what breaks without it, any fallback, the data it holds, and a rank (critical, high, medium, low).
*Done when:* every supplier has all five fields, the ranks are justified in a phrase, and at least one supplier is ranked low with a reason.

<details><summary>Model answer and self-check</summary>

**Model answer.** Cloud provider: everything stops; no fallback; all data; critical. Payment provider: payouts stop; none; bank details; critical. Messaging: alerts missed; app push; phone numbers; high. Maps: routes slower; cached routes; locations; high. Crash reporting: bugs found later; server logs; device data and possibly personal data in crash traces; medium. Analytics: product decisions wait a few days, couriers notice nothing; none needed short-term; usage events with no names or numbers (checked); low, because nothing customer-facing breaks and no personal data is sent.

**Self-check.**
- Did you rank by effect on the service, not by cost?
- Did you check what personal data each supplier receives, including in crash reports?

</details>

**🟡 Check a real supplier: contract questions and due diligence.** Find the public terms, data processing terms and security page of one SaaS tool, such as a free-tier monitoring or form tool. (1) Answer the seven contract questions from what is published. (2) Fill four checklist rows for it: security evidence, reliability history from its status page, sub-processors, deletion and export. Mark each "found", "unclear" or "not found".
*Done when:* all seven questions and all four checklist rows have an answer and a status, every "found" answer points to the page or section, and you list the two questions you would raise before relying on the tool for a business.

<details><summary>Model answer and self-check</summary>

**Model answer.** A typical free-tier result. *Contract:* scope found (service page); price changes found ("with notice"); service levels not found for the free tier; data partly found (deletion on closure, timing unclear); security evidence found (independent report on request); liability found (capped at fees paid, near nothing on a free tier); exit unclear. *Due diligence:* security report found, shared only under a non-disclosure agreement on paid plans; reliability found (status page: three incidents last year, longest about two hours, each explained); sub-processors found (published list with countries); deletion and export unclear (export format given; deletion from backups not stated). Questions: what service level applies on a paid plan, and when is data deleted from backups?

**Self-check.**
- Did you mark only what is stated or missing, without legal conclusions?
- Did you read the status page's history, not just today's status?

</details>

**🔴 Write an exit plan for a critical or high-rank supplier.** For Qafila's maps provider (or a critical or high supplier from your map), write: what data and configuration to take, in what format; how to test an alternative; how long a move takes and what runs meanwhile; what the contract should say about notice and help; and one design change that makes leaving easier.
*Done when:* the plan has all five parts, the time estimate is a range with its main driver, and the design change is specific enough to put on a backlog.

<details><summary>Model answer and self-check</summary>

**Model answer.** Data: cached routes and geocoded merchant addresses (exportable files); configuration and keys (Qafila's repository and secret store). Test: a second provider in shadow mode in one city for two weeks, comparing estimated and actual times. Time: 4 to 10 weeks; driver: how many services call the maps provider directly. Meanwhile: current provider stays on; cached routes cover short outages. Contract: 90 days' notice of price changes or termination; free data export; whether Qafila may keep geocoded addresses (a question for legal). Design change: put all map calls behind one internal "location service".

**Self-check.**
- Is your time estimate a range with a named driver?
- Did you turn contract wishes into questions for legal?

</details>

## ⚠️ Mistakes and traps
- **Buying on the demo and the price.** Run the checklist and the seven contract questions first.
- **Treating all suppliers the same.** Rank them by what breaks without them.
- **Trusting service credits.** Design fallbacks for critical suppliers.
- **Letting knowledge leave with the partner.** Keep work in your repository, review every change, pair your engineers.
- **No exit plan until it is needed.** Write it at signing.
- **Drawing legal conclusions yourself.** Raise gaps; let legal and advisers decide.

## 🧾 Recap
- Each kind of supplier brings different risks.
- Practitioners check that contracts match the service.
- Rank suppliers by what breaks without them; scale due diligence, review and fallbacks to the rank.
- Outsourcing moves work, not accountability.
- Rule: you can hand over the work, never the accountability; know how you would leave before you sign.

## ✍️ Check yourself
**1. During the Friday messaging outage, what was Qafila's main supplier-management gap?**

- A. Qafila had chosen a messaging provider that was too small to serve four countries.
- B. The messaging provider's contract had no service-level target written into it.
- C. Qafila should have built its own text-messaging system instead of buying one.
- D. No status page or out-of-hours support route was known for a high-rank supplier.

<details><summary>Answer</summary>

**D.** The forty minutes were lost because nobody knew where to look or whom to call. A and C jump to conclusions about the supplier choice, and B is contradicted by the register entry. See "Supplier status page list".

</details>

**2. How should Qafila decide how much due diligence each supplier needs?**

- A. By the size of the yearly invoice, since expensive suppliers matter most.
- B. By what breaks without the supplier and what data it holds, as in the ranking.
- C. By applying the full checklist to every supplier equally, to be consistent.
- D. By the supplier's own description of how critical its service usually is.

<details><summary>Answer</summary>

**B.** Effort follows the effect on the service and the data at stake. A confuses cost with importance, C wastes effort on low-risk tools, and D lets the supplier grade itself. See "Map dependencies before you rank them".

</details>

**3. The integration partner's draft contract says it will work in its own repository and hand over "the final software" at the end. What is the main risk Yasmin raised?**

- A. Qafila cannot review changes as they happen, and knowledge stays with the partner.
- B. The partner may charge more for work done in its own repository than in Qafila's.
- C. The partner's repository may use a different programming language from Qafila's.
- D. A single handover at the end leaves too little time to agree the final price.

<details><summary>Answer</summary>

**A.** Qafila must review the code throughout and keep the knowledge. B and C are guesses, and D is about price, not control of the code. See "Outsourcing work, not accountability".

</details>

**4. The maps provider's contract offers a small credit off the monthly fee if it misses its availability target. What should a practitioner conclude?**

- A. The credit compensates Qafila for an outage, so a fallback is optional for this supplier.
- B. The credit gives the supplier a reason to meet its target, so its record can be trusted.
- C. The credit is usually far below the real loss, so critical and high-rank suppliers need fallbacks.
- D. The credit should be raised at renewal until it matches Qafila's expected loss from outages.

<details><summary>Answer</summary>

**C.** Credits are small next to an outage's harm; reliability comes from design. A and B overrate the credit, and D is a negotiation point that still leaves routing degraded during an outage. See "Why supplier service levels matter to you".

</details>

**5. When is the right time to write an exit plan for a critical supplier?**

- A. When the supplier announces a price increase that makes leaving worth considering.
- B. When signing, while relations are good and terms for leaving can still be agreed.
- C. When the contract is close to renewal and procurement asks for alternatives.
- D. When an outage lasts long enough to breach the agreed service level in the contract.

<details><summary>Answer</summary>

**B.** Notice periods and export help must be in the contract, so plan before you need it. A, C and D wait until there is pressure and leverage is weaker. See "Plan the exit at the start".

</details>

## 📚 References
- Regulation (EU) 2016/679 (GDPR), Article 28 "Processor", EUR-Lex: https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng. Contract terms as reported in search summaries, including the UK ICO's guidance (not opened): https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/contracts-and-liabilities-between-controllers-and-processors-multi/what-needs-to-be-included-in-the-contract/
- Regulation (EU) 2022/2554 (DORA), EUR-Lex: https://eur-lex.europa.eu/eli/reg/2022/2554/oj. Application from 17 January 2025 and Article 28(8) exit strategies, as reported in search summaries, including the Dutch AFM's page (not opened): https://www.afm.nl/en/sector/themas/belangrijke-europese-wet--en-regelgeving/dora/derde-aanbieders
- AICPA & CIMA (owner of SOC 2 and the Trust Services Criteria; page not opened): https://www.aicpa-cima.com. Secondary summary, as reported: EY, "To the Point: AICPA revises guidance on applying its trust services criteria and SOC 2 description criteria": https://www.ey.com/en_us/technical/accountinglink/to-the-point-aicpa-revises-guidance-on-applying-its-trust-services-criteria-and-soc-2-description-criteria
- ISO, ISO/IEC 27001:2022, information security management systems (standard page; as reported, not opened): https://www.iso.org/standard/27001
- Library course: [*Running IT as a Business*, lesson 10.2 — Sourcing, suppliers and multi-supplier integration](../itbiz/index.html#/10.2).
- Library course: [*Running IT as a Business*, lesson 5.3 — Third-party, SaaS and open-source components in the product](../itbiz/index.html#/5.3).
- Library course: [*AI Governance: Zero to Hero*, lesson 11.2 — Buying AI: vendor due diligence and contracts](../aigp/index.html#/11.2).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 7.2 — Costs, vendors and lock-in](../founder/index.html#/7.2).
- Library course: [*Secure AI & Application Security: Zero to Hero*, lesson 6.2 — The software supply chain: dependencies, SBOMs, SLSA and signing](../secai/index.html#/6.2).
