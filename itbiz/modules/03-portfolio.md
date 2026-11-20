# Module 3 — Strategy and portfolio

*Module 2 gave Najm Bank's Technology division products with named owners and teams arranged around them. That raises the next question: how much money and how many teams should each product and each new idea get, and who decides? Today the answer is an annual budget built from more than a hundred project requests, approved once a year and rarely changed. This module replaces it in three steps. First, the bank's strategy is turned into a few outcome themes, and every piece of IT spend and work is placed on one page, the investment portfolio, so that leaders can see whether the money says the same thing as the strategy. Second, work is prioritised by what delay costs, business cases are sized to the decision, and long-lived products are funded as teams with guardrails rather than as a string of projects. Third, the portfolio is reviewed on a steady cadence with evidence, and investments are re-planned or stopped by rules written before the money was spent. Each lesson leaves an artefact: a portfolio one-pager, a prioritised list with a product funding memo, and a review pack with a decision log.*

> **Steps:** Plan, Fund — decide what IT invests in and why, how money and team capacity follow the strategy, and how those choices are reviewed, changed and stopped.

---

# 3.1 — From strategy to an investment portfolio
*Level: 🟡 Intermediate* · *Prerequisites: 1.1, 2.1, 2.2* · *Step: Plan, Fund*

**After this you can** turn a stated business strategy into three to five outcome themes with measures, place every product, initiative and obligation of one IT area on a one-page investment portfolio by category and horizon, and show in one chart where the money and team capacity disagree with the strategy. *Study time: reading about 20 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- A **strategy** is a set of choices about where to compete and how, made in response to a clear diagnosis of the situation. A list of goals is not a strategy.
- An **investment portfolio** is the full set of things IT spends money and team capacity on (products, time-bound initiatives and obligations) seen together, so they can be compared, balanced and changed.
- Translate the strategy into **three to five outcome themes**, each with a measure, and tag every investment with the theme it serves, its **category** (run, change or obligation) and its **horizon** (today's core, emerging, or options for later).
- The rule that matters most: **your real strategy is what you fund.** If the money and the teams point somewhere else, the strategy document is a wish.
- Decision cue: if your portfolio cannot explain what it is *not* funding and why, it is a list, not a portfolio.
- Biggest trap: allocating next year's budget by adding up this year's requests from each business line, then writing the strategy slide afterwards.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

The board approved a three-year strategy for Najm Bank with three headlines: grow SME banking through digital channels, lower the cost to serve retail customers, and become more resilient after two payment outages last year. Omar, the Chief Information Officer, was asked to show how the Technology plan supports it.

Tariq, the IT Finance Business Partner, pulled the numbers. The Technology plan for next year held 143 approved projects and about 420 applications to keep running. When he sorted the spend, roughly seven in ten of every unit of money went to keeping existing systems running, licensed and patched. Of the change money that remained, the largest single share went to a corporate treasury upgrade that no strategy headline mentioned, and SME digital work received less than a tenth. Resilience appeared nowhere as a theme; it was spread across infrastructure lines that nobody had connected to the outages.

Nobody had done anything wrong. Each project had a sponsor and a business case, and each was approved on its own merits in last year's cycle. But no one had ever looked at all of them together and asked: does this set of investments, taken as a whole, say what the board said? Huda, Head of Enterprise Architecture, put it plainly at the next leadership meeting: "We have a strategy and we have a budget. We do not have anything that connects them." This lesson builds that connection.

## 📐 How it works

### 🟢 The essentials

**Strategy, in a form you can fund.** Strategy writers disagree on many things, but a useful test comes from Richard Rumelt's *Good Strategy Bad Strategy*, which describes the core of a good strategy as three parts (as reported in summaries of the book): a **diagnosis** of what is going on, a **guiding policy** for dealing with it, and **coherent actions** that carry the policy out. Rumelt also warns against mistaking goals for strategy. For an IT leader, the practical point is that a strategy you can fund must contain **choices**: what the bank will do more of, what it will do less of, and why.

"Be the best digital bank in the region" is a goal. "SME customers leave us because opening an account takes three weeks and needs a branch visit; we will make SME onboarding fully digital before anything else in SME" is a choice. You can fund the second one. You can only applaud the first.

**Outcome themes.** Strategies are written for boards. Investments are made by teams. Between them sits a small set of **outcome themes**: three to five statements of the change the bank wants to see, each with one or two measures. An outcome theme is not a project and not a department. It is a result in the world that several investments might contribute to.

| Strategy headline | Outcome theme | Example measure |
|---|---|---|
| Grow SME banking digitally | SME customers can open and run accounts without a branch | Share of SME accounts opened digitally; time to open |
| Lower cost to serve retail | Retail customers solve routine needs themselves | Calls per active customer; cost per transaction |
| Become more resilient | Critical payment services recover quickly and fail rarely | Hours of critical service disruption; time to restore |

Three to five themes is enough. With ten themes, everything fits somewhere and nothing is excluded.

**The investment portfolio.** A **portfolio** is the whole set of investments seen together. In this course an **investment** is any decision to spend money or team capacity for a purpose, and it comes in three forms:

1. **Products** (lesson 2.1): long-lived, funded year after year, owned by a product manager.
2. **Initiatives**: time-bound pieces of work with an end, such as a data-centre exit or a supplier migration. These are the projects that remain legitimate.
3. **Obligations**: work the bank must do because of a law, a regulator, an audit finding, a contract or a technology reaching end of support.

A portfolio is different from a **programme** (a group of related projects managed together toward one goal) and from the **application list** (the components IT runs). A programme is a delivery container. The portfolio is a decision tool.

**Three tags on every investment.** Place every investment on the page with three tags:

- **Theme**: which outcome theme it serves, or "none".
- **Category**: **run** (keep an existing product or component working, safe and supported), **change** (improve a product or build something new), or **obligation** (must be done, by a date or condition, whatever its value).
- **Horizon**: **core** (improving what the bank does today), **emerging** (growing something new that is starting to work), or **option** (small bets on things that may matter later). The idea of managing several time horizons at once is often associated with *The Alchemy of Growth* by Baghai, Coley and White (as reported in summaries of the book); this course uses its own three labels.

With these tags, a portfolio of a hundred items fits on one chart: money and team capacity by theme, by category and by horizon.

### 🟡 Going deeper

**The portfolio one-pager.** The artefact this lesson produces is one page, readable by a board member in five minutes. It has four parts:

1. **The themes**, each with its measure and current value.
2. **The allocation table**: money and teams by theme, category and horizon, with this year's figures beside the proposed ones.
3. **The gaps**: themes that are under-funded, investments with no theme, and run costs that are rising without a decision.
4. **The choices**: what the portfolio will start, grow, shrink or stop, and what it deliberately will not fund.

| Investment | Type | Theme | Category | Horizon | Money (share) | Teams | Owner |
|---|---|---|---|---|---|---|---|
| Cards & Payments app | Product | Retail self-service | Change and run | Core | 6% | 3 | Reem |
| SME digital onboarding | Product (new) | SME digital | Change | Emerging | 2% | 1 | To be named |
| Payments resilience | Initiative | Resilience | Change | Core | 3% | 2 | Yousef |
| Core banking end-of-support upgrade | Obligation | Resilience | Obligation | Core | 5% | 2 | Huda |
| Corporate treasury upgrade | Initiative | None | Change | Core | 7% | 3 | Treasury sponsor |

Illustrative figures, not benchmarks. One row already raises a question: the treasury upgrade is the largest change item on the page and serves no theme. That does not mean it should stop. It means someone must explain the choice in the open.

**Money and capacity are two currencies.** Banks budget in money, but software work is limited by **team capacity**: the number of stable teams able to do the work. A theme can be "funded" in the budget and still starve because no team is free. Show both columns. When Tariq added a "teams" column, the resilience theme had money for infrastructure purchases but only two teams' worth of people to change anything, while 140 projects competed for the same specialists.

**Run is a decision too.** In many IT budgets, run spend is treated as fixed and change spend as the only thing to discuss. That hides choices. Run spend grows when nothing is retired, when old versions need extended support, and when **technical debt** (the accumulated cost of earlier shortcuts that makes change slower or riskier) is left alone. A healthy portfolio shows run cost per product and asks, for the largest items, "Should we keep, simplify, replace or retire this?" Lesson 10.1 builds the cost model; here, just make run visible and owned.

**Obligations are honest, not hidden.** Regulatory and audit work is legitimate and often urgent. Label it as obligation and measure it honestly (on time, and with how much effort), rather than dressing it up as customer value or burying it in a product's budget, as lesson 1.1 warned. Obligations also have options: the date may be fixed, but how much to do and how to do it usually are not.

**Outcome measures, not activity.** A theme's measure should describe a change in what customers or colleagues do, or in the bank's results, not in IT's activity. "Number of SME features delivered" is activity. "Share of SME accounts opened digitally" is an outcome. Many organisations write these as **objectives and key results (OKRs)**: an objective that says what is to be achieved and a few measurable key results that show progress. The approach is widely credited to Andy Grove at Intel and was popularised by John Doerr's book *Measure What Matters* (as reported in summaries). You do not need the label; you need a measure for each theme that a team can move.

### 🔴 Expert view

**The portfolio reveals the strategy you actually have.** Whatever the strategy document says, the allocation table shows what the organisation has chosen. Leaders often find this uncomfortable. That is the point. A useful exercise for a leadership meeting is to show the current allocation chart with the theme labels removed and ask people to guess the strategy from the money. If nobody guesses the board's headlines, the gap is now visible to everyone in the room.

**Balance, not optimisation.** It is tempting to rank every investment by expected return and fund from the top. That fails for three reasons. Run and obligation work does not compete on return; it is the cost of staying in business. Emerging and option work has highly uncertain returns, so ranking it against core work by a single number punishes the future. And a portfolio needs a deliberate **mix**: enough core improvement to keep today's products competitive, enough emerging work to grow, and a small amount of options so the bank is not surprised. Decide the target mix first, at the leadership table, then rank within each part (lesson 3.2).

**Stable priorities are an asset.** A portfolio that changes every month is no portfolio at all. Google Cloud's announcement of the 2024 DORA report says that "instability in priorities, even with strong leadership, comprehensive documentation, and a user-centered approach … can significantly hinder progress." Its announcement of the 2023 report states that teams that focus on the user have 40% higher organizational performance than teams that don't. Read together, these suggest that a portfolio tied to clear user outcomes and changed on a steady cadence (lesson 3.3) is worth more than a clever one that is re-planned whenever a senior person asks.

**Risk appetite belongs in the portfolio.** A bank's board sets a **risk appetite**: how much risk of what kinds it is willing to take to meet its goals. The portfolio should show where it spends to reduce risk (resilience, security, end-of-support) and where it takes risk (new products, new suppliers, AI). For a regulated bank, ask the risk function which investments touch operational resilience, outsourcing or technology risk rules, because those may need notifications or approvals that affect timing. For how a bank sets AI strategy and risk appetite, see [*AI Governance: Zero to Hero*, lesson 2.1 — From principles to strategy and risk appetite](../aigp/index.html#/2.1); for product strategy in the AI context, see [*AI Product Management*, lesson 9.1 — AI product strategy and defensibility](../aipm/index.html#/9.1).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Strategy kernel page** | Diagnosis, guiding policy and coherent actions for the area, in half a page | Before writing themes; if you cannot fill it in, ask the business for its choices |
| **Outcome theme sheet** | Three to five themes, each with one or two outcome measures, a baseline and an owner | When translating a board strategy into something IT can fund |
| **Portfolio one-pager** | Every investment with theme, category, horizon, money, teams and owner, plus the gaps and the choices | Annual planning, and each quarterly review (lesson 3.3) |
| **Allocation mix chart** | Money and teams by theme, category and horizon, current against target | To start the leadership conversation about balance |
| **Run review list** | The largest run costs by product, each with keep, simplify, replace or retire | When run spend rises without anyone deciding it should |
| **Spreadsheet or portfolio management tool** | Where the portfolio lives; a spreadsheet is enough at first, a portfolio tool later | Examples only, not endorsements; move to a tool when the spreadsheet has many editors |

## 🏛️ In practice at Najm Bank
Huda and Tariq built the first portfolio one-pager for the retail and SME area together. Illustrative and fictional:

> **Retail and SME technology portfolio: one-pager (draft for leadership)**
>
> **Themes:** (1) SME digital: share of SME accounts opened digitally, today about 10%. (2) Retail self-service: calls per active retail customer per year, today about 4. (3) Resilience: hours of disruption to critical payment services per quarter, last quarter about 9.
>
> **Allocation today (share of the area's money / teams):** Run 68% / 9 teams. Change 22% / 11 teams. Obligation 10% / 4 teams. By theme, change money: SME digital 8%, retail self-service 41%, resilience 12%, no theme 39%.
>
> **Gaps:** SME digital, the board's first headline, receives the smallest share. Thirty-one projects carry no theme. Run cost for the old internet-banking platform rose by about a fifth after extended support was bought; no decision was recorded.
>
> **Proposed choices:** grow SME digital onboarding to two teams; fund payments resilience as a named initiative with its own measure; decide keep, simplify or retire for the old internet-banking platform within one quarter; ask the treasury sponsor to explain the treasury upgrade against a theme or as an obligation.
>
> **Not funded this year:** a new branch-queue system and a retail chatbot pilot, because neither moves a theme measure more than the work above.

Huda's first draft had eleven themes, one per business line. Omar sent it back: "Eleven themes means we are still funding departments." Tariq made a different mistake. He spent two weeks splitting shared infrastructure costs across every product to two decimal places before anyone had agreed the themes; Yousef pointed out that a rough split would have answered the same question. The draft above uses rough shares, and the precise model waits for lesson 10.1.

## 🛠️ Exercises
**🟢 Write the themes.** Take your organisation's published or internal strategy (or Najm Bank's three headlines). Write a half-page strategy kernel (diagnosis, guiding policy, coherent actions) and three to five outcome themes, each with one outcome measure and its current value or "unknown".
*Done when:* there are no more than five themes, each measure describes what customers, colleagues or the business do differently (not IT activity), and the kernel names at least one thing the organisation will do less of.

<details><summary>Model answer and self-check</summary>

**Model answer.** For Najm Bank: diagnosis, "SME customers leave because onboarding is slow and branch-bound; retail call volumes are high for routine needs; two payment outages damaged trust". Guiding policy: "digital SME onboarding first; self-service for the ten most common retail requests; resilience of payment services before new payment features". Less of: "new branch technology and bespoke corporate projects without a theme". Themes and measures as in the 🏛️ section.

**Self-check.**
- Could a stranger disagree with your guiding policy? If not, it is still a goal.
- Is every measure something a team's work could move within a year?
- Did you write the "less of" line honestly, even if it is uncomfortable?
- Did you mark "unknown" rather than invent a baseline?

</details>

**🟡 Build the portfolio one-pager.** For one IT area (at least fifteen investments), list every product, initiative and obligation with theme, category, horizon, rough share of money, number of teams and owner. Add the gaps and a first set of proposed choices.
*Done when:* every row has all three tags and an owner (or "none", flagged as a gap), the money and teams columns each add up to the area total, and the page names at least one thing that will not be funded.

<details><summary>Model answer and self-check</summary>

**Model answer.** A first one-pager usually shows a large run share, several items with no theme, at least one theme that is under-funded relative to its importance, and teams spread thinly across many items. The strongest drafts make two or three clear proposals (grow one theme, decide on one large run item, challenge one untagged initiative) rather than reallocating everything at once.

**Self-check.**
- Did you include run and obligation work, not only new projects?
- Is the teams column in real, stable teams, not in fractions of people spread across projects?
- Did the "no theme" items get a question, not an automatic stop?
- Could a board member read it in five minutes?

</details>

**🔴 Show the gap and propose a target mix.** Draw the allocation mix chart (money and teams by theme, category and horizon) for today, and a target mix for next year. Write five lines on what must change to move from one to the other, and which risks the change creates.
*Done when:* both mixes are on one chart with the same scale, the target mix keeps run and obligation work realistic, each of the five lines names an owner, and at least one line names a risk or regulatory question for the risk function.

<details><summary>Model answer and self-check</summary>

**Model answer.** Najm Bank's target mix moves SME digital from 8% to about 20% of change money (illustrative), funds resilience as its own initiative, and reduces "no theme" change work from 39% to below 10%. Run falls only slightly, through one retirement decision, because a realistic plan cannot cut run quickly. The five lines: Omar agrees the target mix with the business heads; Tariq moves two teams' funding at the next quarterly review; Huda leads the retire-or-keep decision on the old internet-banking platform; Reem shares one team with SME onboarding for a quarter; Nour checks whether the payments resilience work touches operational resilience rules that need notice to the regulator.

**Self-check.**
- Is the target mix achievable within a year, given that teams cannot be moved overnight?
- Did you avoid cutting run or obligation work just to make the chart look better?
- Did you name a person for each line?
- Did you ask a question of the risk function rather than state a regulatory conclusion?

</details>

## ⚠️ Mistakes and traps
- **Budget by accumulation.** Adding up each business line's requests produces a budget that reflects last year's politics. Start from themes and a target mix, then invite requests against them.
- **Too many themes.** Ten themes exclude nothing. Keep three to five, and accept that some good ideas will not fit.
- **Activity measures dressed as outcomes.** "Features delivered" or "projects completed" will rise whatever happens to customers. Measure what customers, colleagues or the business do differently.
- **Run treated as fixed.** Run spend hides choices about retiring, simplifying and paying down technical debt. Show run per product and decide on the largest items.
- **Money without teams.** A theme can be funded in the budget and still have no team to do the work. Show capacity beside money.
- **Precision before agreement.** Spending weeks on exact cost splits before the themes are agreed wastes effort. Use rough shares first.

## 🧾 Recap
- A strategy you can fund contains **choices**: a diagnosis, a guiding policy and coherent actions, including what to do less of.
- Translate it into **three to five outcome themes**, each with an outcome measure and a baseline.
- The **portfolio** is all products, initiatives and obligations seen together; tag each with **theme, category and horizon**, and show money and teams.
- **Your real strategy is what you fund**; the allocation chart shows whether money and strategy agree.
- Decide a deliberate **mix** of run, change and obligation, and of core, emerging and option work, before ranking anything.
- Keep priorities **stable** and tied to user outcomes; change them on a cadence, not on request.

## ✍️ Check yourself
**1. The board's strategy says "be the leading digital bank for SMEs". Huda wants to turn it into something IT can fund. What should she do first?**

- A. Ask each business line for its project list and group the projects under the headline.
- B. Buy a portfolio management tool so that SME projects can be tracked in one place.
- C. Ask what is stopping SME customers today and agree the choices that follow from that.
- D. Set a target for the number of SME features the teams must deliver in the next year.

<details><summary>Answer</summary>

**C.** A fundable strategy starts from a diagnosis and the choices that follow. A builds the budget by accumulation under a new label, B buys a tool before the decision exists, and D sets an activity target rather than an outcome. See "Strategy, in a form you can fund".

</details>

**2. Tariq's portfolio shows that the SME theme has money for next year, but no team is free to work on it. What does this tell Omar?**

- A. The theme is under-resourced, because capacity as well as money limits what gets done.
- B. The theme is adequately resourced, since money can always be turned into people later.
- C. The theme should be removed, since a theme without a team cannot have a useful measure.
- D. The theme is a run cost and should be moved into the category that keeps systems going.

<details><summary>Answer</summary>

**A.** Money and team capacity are two currencies; a theme can be funded and still starve. B assumes hiring or moving teams is instant, C drops a strategic theme instead of fixing capacity, and D confuses category with resourcing. See "Money and capacity are two currencies".

</details>

**3. Which of these is an outcome measure suitable for Najm Bank's retail self-service theme?**

- A. The number of self-service screens released in the retail app during the year.
- B. The share of the retail change budget that has been spent by the end of each quarter.
- C. The number of retail projects closed on time and within budget during the year.
- D. The number of calls per active retail customer for routine needs such as card limits.

<details><summary>Answer</summary>

**D.** It describes what customers do differently. A and C count IT activity that would rise whatever customers do, and B measures spending, not results. See "Outcome measures, not activity".

</details>

**4. A corporate treasury upgrade is the largest change item in the portfolio and serves no theme. What should the portfolio one-pager do with it?**

- A. Stop it at once, because any work without a theme is outside the strategy by definition.
- B. Flag it as a gap and ask its sponsor to explain it against a theme or as an obligation.
- C. Leave it off the page, because corporate work belongs to a different business line.
- D. Assign it to the resilience theme, since most upgrades make systems more reliable.

<details><summary>Answer</summary>

**B.** An item with no theme is a question to answer in the open, not an automatic stop. A acts without evidence, C hides spend from the portfolio, and D relabels the work to make the chart look tidy. See "The portfolio one-pager".

</details>

**5. Omar proposes ranking every investment, including run and obligation work, by expected financial return and funding from the top. What is the main problem?**

- A. Run and obligation work do not compete on return, and early bets would be unfairly ranked.
- B. Financial return cannot be estimated for any IT investment, so no ranking is possible.
- C. A ranking would take too long, because a portfolio has too many investments to compare.
- D. Ranking by return is reserved for the board and cannot be done by the IT leadership team.

<details><summary>Answer</summary>

**A.** Run and obligation work are the cost of staying in business, and emerging or option work has returns too uncertain for one number. Decide the mix first, then rank within each part. B overstates the problem, C is not the issue, and D invents a rule. See "Balance, not optimisation".

</details>

## 📚 References
- Google Cloud blog, "Announcing the 2024 DORA report", 22 October 2024 (opened 2026-11-20; source of the quoted finding on unstable priorities): https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
- Google Cloud blog, "2023 State of DevOps Report: Culture is everything", October 2023 (opened 2026-11-20; source of the 40% user-focus finding): https://cloud.google.com/blog/products/devops-sre/announcing-the-2023-state-of-devops-report
- Rumelt, R. P., *Good Strategy Bad Strategy: The Difference and Why It Matters* (Crown Business, 2011). The "kernel" (diagnosis, guiding policy, coherent action) as reported in summaries; book not opened.
- Baghai, M., Coley, S. and White, D., *The Alchemy of Growth: Practical Insights for Building the Enduring Enterprise* (Perseus Books; first published 1999, sources differ between 1999 and 2000). The three-horizons idea as reported in summaries; book not opened.
- Doerr, J., *Measure What Matters* (Portfolio/Penguin, 2018); Grove, A. S., *High Output Management* (Random House, 1983). Origin and definition of OKRs as reported in summaries; books not opened.
- Library course: [*AI Governance: Zero to Hero*, lesson 2.1 — From principles to strategy and risk appetite](../aigp/index.html#/2.1) (risk appetite set by the board, in the AI context).
- Library course: [*AI Product Management*, lesson 9.1 — AI product strategy and defensibility](../aipm/index.html#/9.1) (product strategy for one product, below the portfolio).

---

# 3.2 — Prioritising and funding work: business cases, cost of delay and funding products not projects
*Level: 🟡 Intermediate* · *Prerequisites: 1.2, 2.1, 3.1* · *Step: Fund*

**After this you can** size a business case to the decision it supports, estimate the cost of delay for five pieces of work and put them in order by cost of delay divided by duration, and write a one-page funding memo that funds a product as a team with guardrails and a review date. *Study time: reading about 25 min, hands-on about 110 min (estimate).*

## ⚡ In 60 seconds
- A **business case** is the argument for spending money: the problem, the options (including doing nothing), costs and benefits as ranges, risks and the assumptions that would change the answer. Its size should match the size of the decision.
- **Cost of delay** is the value lost for each week a piece of work is not in use. It turns "this is urgent" into a number people can compare and challenge.
- When team capacity is the constraint, do first the work with the highest **cost of delay divided by duration** (often called **CD3**). Short, valuable items go first; long ones wait unless their delay costs a lot.
- The rule that matters most: **fund the team for the period, steer the work every week, and ask for a business case only in proportion to the decision.**
- Decision cue: if a change that takes two weeks to build waits two months for money, the funding model, not the team, is the bottleneck.
- Biggest trap: precise-looking business cases built on single-point estimates, approved once and never checked again.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

When Najm Bank mapped its card-change value stream in lesson 1.2, the longest wait was not in building or testing. It was the funding decision: about 30 working days, because the investment committee met quarterly and asked for a business case for every change above a modest threshold. Reem, Product Manager for Cards & Payments, had a card freeze feature that her team could build in three weeks. Customers who lose a card were calling the contact centre to block it, and the fraud team said lost-card fraud often happened in the hours before the call got through. The feature waited a full quarter for money.

The business case Reem eventually submitted ran to fourteen pages, with a five-year net present value calculated to the nearest thousand. Tariq, the IT Finance Business Partner, admitted that most of the numbers were guesses with decimal places. Meanwhile, a large corporate treasury upgrade had been approved two years earlier on an equally confident business case; it was now nearly twice its original cost, and no one had reopened the case.

So the bank had two problems at once. Small, valuable work waited too long because the process treated it like a large investment. Large, risky work kept going because its approval was a one-time event. This lesson fixes both: business cases sized to the decision, priorities set by the cost of waiting, and long-lived products funded as teams within guardrails.

## 📐 How it works

### 🟢 The essentials

**What a business case is for.** A **business case** is a structured argument that a particular use of money and people is worth it compared with the alternatives. A useful one answers six questions:

1. **Problem or opportunity**: what outcome theme (lesson 3.1) does this serve, and what is wrong today?
2. **Options**: at least two, plus **doing nothing**, which always has a cost too.
3. **Costs**: to build, to run each year, and to stop or retire later, as ranges.
4. **Benefits**: what will change, how it will be measured, and when, as ranges.
5. **Risks**: delivery, operational, security, supplier and regulatory.
6. **Assumptions that would change the answer**: the two or three things that, if wrong, would turn "yes" into "no".

The sixth question matters most. It tells reviewers what to check, and it tells the portfolio review (lesson 3.3) what evidence would justify stopping.

**Size the case to the decision.** Not every decision needs the same paperwork. A simple tiering works:

| Decision size | Example | What is needed | Who decides |
|---|---|---|---|
| Within a funded product's budget and guardrails | Card freeze feature | A backlog item with its outcome and cost of delay | Product manager |
| New, time-bound, moderate | Supplier interface migration | A one-page case with options and ranges | Portfolio board (lesson 3.3) |
| Large, new or high-risk | New SME onboarding platform | Full case, independent estimate review, staged funding | Investment committee, with risk input |

The thresholds are the bank's to set with finance. The point is that the effort of the case should be a small fraction of the cost of the work.

**Cost of delay.** **Cost of delay** is the value lost, per unit of time, while a piece of work is not yet in use. It includes money not earned, costs not saved, losses not prevented and risks left open. Don Reinertsen's *The Principles of Product Development Flow* (2009) made the idea widely known in product development; it is often quoted with the advice that if you quantify only one thing, it should be the cost of delay (wording varies between sources).

Estimate it by asking: "If this arrives one week later, what do we lose in that week?" For the card freeze feature, Reem's team listed calls to the contact centre that would continue (a cost per call) and fraud losses that the fraud team attributed to slow blocking. The answer was a range, not a number, and that is fine.

**Shapes of urgency.** Cost of delay is not always constant. Four common shapes:

| Shape | What it looks like | Example at Najm Bank |
|---|---|---|
| **Steady** | Each week of delay loses about the same amount | Card freeze: calls and fraud continue weekly |
| **Deadline** | Little loss until a date, then a large one | A card-scheme rule change with a fixed compliance date |
| **Closing window** | Value shrinks the later you arrive, then disappears | A seasonal SME campaign tied to a trade event |
| **Risk reduction** | Small expected loss each week, but a rare large one | Replacing a component that has reached end of support |

Recognising the shape tells you how to schedule. Deadline work must start early enough to finish by the date, but not necessarily first. Closing-window work must go first or not at all.

### 🟡 Going deeper

**Ordering work by CD3.** When the constraint is a team's capacity, the order of work changes the total cost of waiting. A common rule is to divide cost of delay by duration (the time the work occupies the team) and do the highest result first. Joshua Arnold's Black Swan Farming site calls this **CD3** (cost of delay divided by duration), and the same ratio appears under the name **weighted shortest job first** in some sources (as reported in search summaries).

Reem's four items (cost of delay in thousands of the bank's currency per week, illustrative figures):

| Item | Cost of delay per week | Duration (weeks) | CD3 |
|---|---|---|---|
| Card freeze | 30 | 3 | 10.0 |
| Fee display fix | 8 | 1 | 8.0 |
| Mobile wallet support | 50 | 10 | 5.0 |
| Rewards card design | 20 | 8 | 2.5 |

If the team works through them one at a time, the total cost of waiting (each item's weekly cost of delay times the week it finishes) is about 1,262 in CD3 order, about 1,486 if the biggest cost of delay goes first (wallet first), and about 1,468 if the shortest goes first. The difference comes from letting short, valuable items go early instead of making them wait behind a long one. The numbers are illustrative; the pattern is the lesson.

Three cautions. First, CD3 orders work within one constraint; it does not decide the mix across themes, which leadership sets first (lesson 3.1). Second, deadline and obligation work is scheduled to its date, not ranked by CD3. Third, the inputs are estimates; use ranges and simple scales (for example, 1, 2, 5, 10, 20) when people cannot agree on money, and say so.

**Estimates as ranges, and the outside view.** Single-point estimates ("it will cost 4.2 million and deliver in nine months") hide uncertainty. Ask for a low, likely and high figure, and say what drives the spread. Then compare with what similar past work actually cost and took. This **outside view**, called **reference class forecasting**, was proposed for project management by Bent Flyvbjerg, building on the work of Daniel Kahneman and Amos Tversky on decisions under uncertainty (Flyvbjerg, *Project Management Journal*, 2006, as reported in search summaries). It counters **optimism bias** (the tendency to expect things to go better than they usually do).

Large IT work deserves particular care. Flyvbjerg and Alexander Budzier, writing in *Harvard Business Review* in 2011, reported on a sample of 1,471 IT projects: the average cost overrun was 27%, but one in six projects had a cost overrun averaging 200% and a schedule overrun of almost 70% (figures as reported in search summaries; the article was not opened). The lesson for a portfolio is not "IT projects fail". It is that averages hide a fat tail, so large investments should be staged, so that the bank can stop before it has spent everything.

**Three ways to fund work.** How money is released shapes behaviour as much as how much is released.

| Funding model | How it works | Fits | Watch out for |
|---|---|---|---|
| **Project funding** | Money for a defined scope, date and budget; the team disbands at the end | Truly time-bound work: a data-centre exit, a one-off migration | Re-approval needed to change course; people and knowledge leave at the end |
| **Product (team) funding** | A stable team and its run costs funded for a period (for example a year, reviewed quarterly), steering its own backlog within guardrails | Long-lived digital products and platforms | Funding becomes permanent by habit unless outcomes are reviewed |
| **Staged (metered) funding** | A new bet gets a small amount to test its riskiest assumptions; more money follows evidence | New products, emerging and option horizons | Teams told to "prove it" with no time or money to do so |

Najm Bank used project funding for everything. The target is product funding for its products and platforms, staged funding for new bets, and project funding only where work really ends.

**Guardrails make product funding safe.** Funding a team for a year worries finance and risk for good reason: what stops the money drifting? The answer is **guardrails**, rules set in advance inside which the product manager decides alone (lesson 2.2 introduced the idea):

- the outcome measures the product must move and report each quarter;
- a spending envelope for people, run costs and suppliers;
- a ceiling on run cost growth before a portfolio decision is needed;
- a size threshold above which a new initiative goes to the portfolio board;
- the bank's risk appetite and change policy, unchanged.

Inside the guardrails, the product manager reorders the backlog weekly by cost of delay. Outside them, the portfolio board decides.

### 🔴 Expert view

**Annual budgets and changing priorities.** Most banks set budgets once a year, for good reasons: shareholders, regulators and capital planning expect them. Product funding does not abolish the annual budget; it changes what the budget buys (teams and envelopes rather than project scopes) and adds quarterly re-allocation at the portfolio level. Some organisations go further. The Beyond Budgeting movement argues for dynamic resource allocation instead of fixed annual allocations; Bjarte Bogsnes describes Equinor's (formerly Statoil's) practice of allocating resources dynamically, with targets, mandates and decision gates instead of an annual allocation (as reported in secondary sources and his presentations). You do not need to go that far to gain most of the benefit; quarterly reviews with guardrails already shorten the funding wait from months to weeks.

**Questions for finance, not conclusions.** Funding teams instead of projects raises accounting questions that IT should not answer alone. Ask Tariq and the finance function: under the bank's accounting policy, which software development costs may be capitalised (recorded as an asset and spread over years) and which must be expensed when incurred, and does the answer depend on whether the work is a project or a product team's ongoing work? How will the bank evidence time spent on capitalisable work without making teams fill in timesheets by project code? How does a quarterly re-allocation fit the bank's budget approval rules? These are accounting and governance decisions; the operating model must make the evidence easy to produce.

**Check the case after the fact.** A business case is a forecast. Its value to the next decision comes from comparing the forecast with what happened. Keep each case's key assumptions and expected measures in the investment record (lesson 9.1), and review them at the quarterly portfolio review. Over time this builds the bank's own reference class, and it teaches sponsors that their numbers will be read again.

**Beware the hidden incentive.** If the only way to get money is a business case with large benefits, sponsors will write large benefits. If the only way to keep a team is to keep a project alive, managers will keep projects alive. Product funding with outcome reviews removes both incentives, but only if the reviews actually move money. For how an AI use case is assessed and approved with risk tiers, see [*AI Governance: Zero to Hero*, lesson 8.1 — Use-case intake, business case and risk tiering](../aigp/index.html#/8.1); for planning bets when the technology itself is uncertain, see [*AI Product Management*, lesson 9.2 — Roadmaps under uncertainty: bets, platforms and model change](../aipm/index.html#/9.2).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Business case tiers** | A table of decision sizes, what each needs and who decides | When small changes wait for large-investment paperwork |
| **One-page business case** | Problem, options with "do nothing", costs and benefits as ranges, risks, the assumptions that would change the answer | For moderate, time-bound investments |
| **Cost of delay sheet** | Each item's weekly cost of delay (or a relative score), urgency shape, duration and CD3 | When ordering a product backlog or competing initiatives |
| **Reference class log** | Planned and actual cost and duration of past investments, by type | Before approving any large estimate |
| **Product funding memo** | Team, period, spending envelope, outcome measures, guardrails, review date | When moving a product from project funding to team funding |
| **Finance question list** | Capitalisation, time evidence, re-allocation rules and approval thresholds to agree with finance | Before the first product funding memo is signed |

## 🏛️ In practice at Najm Bank
Tariq and Reem wrote Najm Bank's first product funding memo for Cards & Payments. Illustrative and fictional:

> **Product funding memo: Cards & Payments (draft for the investment committee)**
>
> **What is funded:** three stable product teams (about 24 people, including two supplier engineers), the product's run costs and its share of the card-processing contract, for the next financial year, reviewed each quarter.
>
> **Outcome measures (theme: retail self-service):** calls per active card customer for routine card needs, today about 1.1 a year; lost-card fraud losses per quarter; card app rating among active users. Reliability: card payment availability against the agreed service level (lesson 8.3).
>
> **Guardrails:** spend within the envelope agreed with finance; run cost growth above 10% in a quarter goes to the portfolio board; any new initiative above about eight team-weeks, or touching another product's interface, goes to the portfolio board; the change policy and risk appetite are unchanged.
>
> **How work is ordered:** weekly, by cost of delay divided by duration, with obligation work scheduled to its date. The cost of delay sheet is visible to the portfolio office.
>
> **Questions agreed with finance before signing:** which development costs the bank will capitalise; how team time on capitalisable work is evidenced from the delivery tool rather than timesheets; how a quarterly re-allocation is approved.
>
> **Review:** quarterly at the portfolio board, with outcome, cost and flow evidence (lesson 3.3). First review in three months.

The first draft had mistakes. Reem's guardrail said "spend as needed within the product's goals", which Tariq rejected as a blank cheque. Tariq's first draft required a business case for any item above two team-weeks, which would have sent half the backlog back to the committee; they settled on eight. Nour asked that the risk appetite line be explicit, because the second line would read the memo. The committee approved it as a one-year pilot, with the card freeze feature built in the first three weeks.

## 🛠️ Exercises
**🟢 Tier your decisions.** Write a business case tier table for your organisation: three decision sizes, an example of each, what is needed and who decides. Then take five recent funding requests and place each in a tier.
*Done when:* each tier has a threshold someone could check (money, team-weeks or risk), the five requests are placed, and you have marked any that received more or less scrutiny than their tier suggests.

<details><summary>Model answer and self-check</summary>

**Model answer.** Najm Bank's table: (1) within a funded product's guardrails, no case, product manager decides; (2) new and time-bound up to an agreed size, one-page case, portfolio board; (3) larger, new or high-risk, full case with an independent estimate review and staged funding, investment committee with risk input. Of five recent requests, two small card changes had full cases (over-scrutinised) and one large supplier extension was renewed without any case (under-scrutinised).

**Self-check.**
- Is each threshold measurable, not "significant" or "strategic"?
- Did you find at least one request treated wrongly for its size?
- Does every tier name one decider, not a committee of committees?

</details>

**🟡 Order five items by CD3.** Take five items competing for one team (or use Reem's four plus one of your own). For each, estimate the cost of delay per week as a range or a relative score, name its urgency shape, estimate its duration and compute CD3. Order them, and compare the total cost of waiting with one other order.
*Done when:* each item has a cost of delay with its reasoning, a shape, a duration and a CD3; deadline items are scheduled to their date rather than ranked; and the comparison shows the totals for both orders.

<details><summary>Model answer and self-check</summary>

**Model answer.** With Reem's four items, CD3 order is card freeze, fee display fix, mobile wallet support, rewards card design, total waiting cost about 1,262 against about 1,486 for "biggest first". Adding a card-scheme rule change with a deadline in twelve weeks and a four-week duration: it is not ranked, but must start no later than week eight, so it is placed after the fee fix and before the wallet work, which delays the wallet by four weeks; the plan should state that cost.

**Self-check.**
- Did you write down why each cost of delay is what it is, so someone can challenge it?
- Did you treat deadline work separately?
- Did you use ranges or relative scores where money was guesswork, and say so?
- Is duration the time the item occupies the team, not the calendar time it waits?

</details>

**🔴 Write a product funding memo.** For one product (yours or Najm Bank's corporate payments product), write a one-page funding memo: what is funded, outcome measures with baselines, guardrails, how work is ordered, questions for finance, and the review date.
*Done when:* the memo fits on one page, every guardrail is a checkable rule, the outcome measures have baselines or "unknown", the finance questions are questions rather than accounting conclusions, and the review date is within three months.

<details><summary>Model answer and self-check</summary>

**Model answer.** A good memo resembles the Cards & Payments one: a stable team funded for a year and reviewed quarterly; two or three outcome measures plus one reliability measure; four or five guardrails (spending envelope, run-cost ceiling, size threshold for new initiatives, change policy and risk appetite unchanged); weekly ordering by cost of delay; three finance questions on capitalisation, evidence of time and re-allocation approval; a first review date.

**Self-check.**
- Could finance tell from your guardrails when the product manager must come back for a decision?
- Is any guardrail really a principle in disguise ("act responsibly")?
- Did you leave the accounting answers to finance?
- Does the memo say what evidence the first review will look at?

</details>

## ⚠️ Mistakes and traps
- **One process for every size.** Treating a three-week change like a three-year programme makes small work wait and large work look routine. Tier the business case to the decision.
- **False precision.** A five-year net present value to the nearest thousand built on guesses misleads. Use ranges, name the assumptions that matter and compare with past actuals.
- **Ranking without cost of delay.** "High, medium, low" priority labels hide the reasons. Estimate what a week of delay costs, even roughly, so the reasons can be challenged.
- **Product funding without guardrails.** A team funded "to deliver value" with no measures, envelope or thresholds will lose finance's trust quickly. Write checkable guardrails.
- **Approve once, never re-read.** A business case not reviewed against what happened teaches sponsors that numbers do not matter. Record assumptions and check them each quarter.
- **IT deciding accounting.** Capitalisation and budget rules belong to finance. Bring questions and make the evidence easy, but do not state the answer.

## 🧾 Recap
- A **business case** compares options (including doing nothing) with ranges and names the assumptions that would change the answer; its effort should match the **size of the decision**.
- **Cost of delay** is the value lost per week of waiting; recognise its **shape** (steady, deadline, closing window, risk reduction).
- When one team is the constraint, order work by **cost of delay divided by duration (CD3)**; schedule deadline work to its date.
- Use **ranges and the outside view**; large IT work has a fat tail of overruns, so stage large investments.
- **Fund products as teams** for a period with **guardrails**, new bets in **stages**, and only truly temporary work as **projects**.
- Bring **questions** on capitalisation and budget rules to finance, and **re-read** every case against what happened.

## ✍️ Check yourself
**1. Reem's card freeze feature takes three weeks to build but waited a full quarter for a funding decision. What change addresses the cause?**

- A. Ask Reem's team to build faster, so that the funding wait matters less in the total time.
- B. Require a longer business case, so that the investment committee can approve it sooner.
- C. Move the feature to a separate project with its own budget, manager and steering group.
- D. Fund the product as a team within guardrails, so small items need no committee decision.

<details><summary>Answer</summary>

**D.** The wait was in the funding process; product funding with guardrails lets the product manager decide small items. A targets the wrong step, B adds effort without speed, and C adds overhead to a three-week change. See "Size the case to the decision" and "Three ways to fund work".

</details>

**2. Two items compete for one team. Item X has a cost of delay of 40 a week and takes 8 weeks. Item Y has 15 a week and takes 2 weeks. Which goes first by CD3, and why?**

- A. X, because its cost of delay per week is the larger of the two and that alone decides.
- B. Y, because its cost of delay divided by duration (7.5) is higher than X's (5.0).
- C. X, because longer items should start first so that they are not left until the end.
- D. Y, because shorter items should always go first whatever their cost of delay may be.

<details><summary>Answer</summary>

**B.** CD3 is 40/8 = 5.0 for X and 15/2 = 7.5 for Y, so Y goes first. A ignores duration, C has no basis, and D ignores cost of delay; a short item with almost no cost of delay should not jump the queue. See "Ordering work by CD3".

</details>

**3. A card-scheme rule must be met by a fixed date in twelve weeks; the work takes four weeks. How should Reem schedule it?**

- A. Rank it by CD3 with everything else, since all items should be compared by one rule.
- B. Put it first in the queue, since anything with a regulatory deadline must start at once.
- C. Schedule it to start early enough to finish by the date, and state what it delays.
- D. Leave it until the last four weeks, since starting earlier gains nothing for the bank.

<details><summary>Answer</summary>

**C.** Deadline work is scheduled to its date, with a safety margin, and its effect on other work is made visible. A misapplies CD3, B wastes the slack, and D leaves no room for anything going wrong. See "Shapes of urgency" and the cautions under "Ordering work by CD3".

</details>

**4. The sponsor of a large new platform presents a single estimate: "4.2 million, nine months". What should Tariq ask for first?**

- A. A low, likely and high range, and a comparison with what similar past work cost and took.
- B. A second estimate from the same team, to confirm the first figure is correct to the unit.
- C. A longer list of benefits, so that the case stays positive even if costs turn out higher.
- D. Approval of the full amount now, so the team does not lose time during later reviews.

<details><summary>Answer</summary>

**A.** Ranges and the outside view (reference class forecasting) counter optimism bias, and staged funding follows from them. B repeats the inside view, C inflates the case, and D removes the chance to stop early. See "Estimates as ranges, and the outside view".

</details>

**5. Finance worries that funding Cards & Payments as a team for a year is a blank cheque. Which addition best answers the concern?**

- A. A promise from Reem that the team will spend responsibly and deliver as much value as it can.
- B. A rule that every backlog item needs its own business case before the team starts work.
- C. Guardrails: outcome measures, a spending envelope, a run-cost ceiling and a size threshold.
- D. A decision to keep project funding until the product has proven itself for several years.

<details><summary>Answer</summary>

**C.** Checkable guardrails tell finance when the product manager must come back for a decision. A is a principle, not a rule; B recreates the slow process; D never lets the product prove itself. See "Guardrails make product funding safe".

</details>

## 📚 References
- Reinertsen, D. G., *The Principles of Product Development Flow: Second Generation Lean Product Development* (Celeritas, 2009). Cost of delay and the "quantify one thing" advice, as reported in summaries (wording varies between sources); book not opened.
- Black Swan Farming (Joshua Arnold), "Qualitative Cost of Delay" and related pages on CD3 (definition of CD3 as cost of delay divided by duration, as reported in search summaries; page not opened): https://blackswanfarming.com/qualitative-cost-delay/
- Flyvbjerg, B., "From Nobel Prize to Project Management: Getting Risks Right", *Project Management Journal* 37(3): 5–15 (2006), as reported in search summaries; not opened: https://doi.org/10.1177/875697280603700302
- Flyvbjerg, B. and Budzier, A., "Why Your IT Project May Be Riskier Than You Think", *Harvard Business Review* 89(9), September 2011. Figures (1,471 projects; 27% average; one in six with about 200% cost and almost 70% schedule overrun) as reported in search summaries; article not opened. Working-paper version listed at SSRN: https://papers.ssrn.com/abstract=2229735
- Bogsnes, B., "Beyond Budgeting at Equinor: how to become more adaptive and more human", Global Peter Drucker Forum blog (as reported in search summaries; not opened): https://www.druckerforum.org/blog/beyond-budgeting-at-equinor-how-to-become-more-adaptive-and-more-humanby-bjarte-bogsnes
- Library course: [*AI Governance: Zero to Hero*, lesson 8.1 — Use-case intake, business case and risk tiering](../aigp/index.html#/8.1).
- Library course: [*AI Product Management*, lesson 9.2 — Roadmaps under uncertainty: bets, platforms and model change](../aipm/index.html#/9.2).

---

# 3.3 — Portfolio governance: reviewing, re-planning and stopping work
*Level: 🟡 Intermediate* · *Prerequisites: 3.1, 3.2* · *Step: Plan, Fund*

**After this you can** design a quarterly portfolio review with a fixed evidence pack, write a stop rule for every investment before it is funded, apply continue, change course, scale or stop decisions to a real list of investments, and keep a decision log that shows what was stopped and where the freed capacity went. *Study time: reading about 25 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- **Portfolio governance** is how an organisation reviews its investments together, on a steady cadence, and decides what to continue, change, grow or stop. Its output is decisions, not status reports.
- Each review uses the same **evidence pack** for every investment: outcome measures against what was expected, spend against the envelope, flow, run cost and incidents, risks, and the status of the key assumptions.
- There are four decisions: **continue**, **change course**, **scale up** and **stop**. Obligations are re-planned rather than stopped.
- The rule that matters most: **every investment carries its own stop rule, written before the money is spent.** Stopping then becomes a planned outcome, not a public failure.
- Decision cue: if your portfolio has not stopped anything in a year, it is not being governed; it is being accumulated.
- Biggest trap: "we have spent too much to stop now". Money already spent is gone whatever you decide; the only question is whether the *next* unit of money is worth spending.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

Najm Bank's loan origination replacement started three years ago with an eighteen-month plan. It has reported "amber" for seven quarters in a row. Its cost is now about 1.8 times the original business case, the first release has slipped three times, and the old loan system it was meant to replace still runs, with its own support contract renewed twice "for the last time". When Omar, the CIO, asked whether it should be stopped, the sponsor replied that the bank had already spent too much to walk away, and that the team was "nearly there".

It was not the only one. When Huda and Tariq built the portfolio one-pager in lesson 3.1, they found twelve investments older than two years with no measure of what they had achieved, and 143 active projects competing for the same specialists. Yousef pointed out that his operations teams were supporting six systems that were meant to have been retired by projects that had since been closed. Nobody had decided to keep any of these going. Nobody had decided to stop them either.

The portfolio had a front door for new money (lesson 3.2) but no exit. Investments started easily and ended only when they finished, which some never did. This lesson builds the exit: a regular review that looks at evidence, a set of decisions it is allowed to make, rules written in advance for when to stop, and a log that shows the board what was decided and why.

## 📐 How it works

### 🟢 The essentials

**What portfolio governance is.** **Portfolio governance** is the set of meetings, rules, evidence and decision rights through which an organisation reviews its investments together and changes them. It differs from **project governance**, which asks whether one project is on track against its plan. Portfolio governance asks a different question: given everything we now know, is this still the best use of this money and these teams, compared with everything else we could do?

**The portfolio board.** A **portfolio board** is the group that makes those decisions for an area. At Najm Bank it is chaired by Omar and includes the business heads for retail, SME and corporate banking, Huda, Tariq and Yousef. Nour attends as an observer from risk and controls, so that the second line sees decisions as they are made rather than months later. The board's decision rights are written down (lesson 2.2): it decides the mix across themes, approves initiatives above the product guardrails, and continues, changes, scales or stops investments. It does not reorder product backlogs; product managers do that within their guardrails (lesson 3.2).

**Cadence and triggers.** Reviews happen on a fixed **cadence**, usually quarterly, so that teams can plan around them and priorities stay stable between them. A small set of **triggers** brings an item to the board early: a guardrail breached, a stop rule met, a major incident with a structural cause, or a regulatory change. Everything else waits for the next review. That combination gives both stability and responsiveness.

**The evidence pack.** Every investment comes to the review with the same page:

| Evidence | Question it answers | Where it comes from |
|---|---|---|
| Outcome measures against expected | Is it changing what it was funded to change? | Product analytics, business data |
| Spend against envelope and forecast | Is the money going where we agreed? | Finance system, investment record |
| Flow: lead time and work in progress | Is work moving, or piling up? | Delivery tool (lessons 1.2, 1.3) |
| Run cost and incidents | What does it cost to keep, and how reliable is it? | Cost model, incident records (lesson 9.3) |
| Risks and obligations | What could hurt us, and what must be done by when? | Risk register, obligation list |
| Key assumptions | Are the assumptions that would change the answer holding? | Business case (lesson 3.2) |

The same page for every investment makes them comparable and stops the loudest sponsor from setting the format. It should be produced from records, not written for the meeting.

**Four decisions.** For each investment the board makes one of four decisions and writes down why:

| Decision | When | What happens next |
|---|---|---|
| **Continue** | Evidence is on track or improving | Nothing changes; next review as normal |
| **Change course** | The goal still matters, but the approach is not working | New approach, scope or team, with a new stop rule and an early review |
| **Scale up** | Evidence is strong and more capacity would speed results | More teams or money, taken from somewhere named |
| **Stop** | The stop rule is met, or the goal no longer matters | Stop new work, close down well, move people and money, record it |

Obligations are a special case. The board cannot stop a regulatory requirement, but it can change how the bank meets it: scope, approach, supplier or timing within the deadline.

### 🟡 Going deeper

**Write the stop rule at the start.** A **stop rule** (often called a kill criterion) is a sentence written when an investment is funded, stating the evidence that would end it. It should name a measure, a threshold and a date: "If fewer than 30% of new SME accounts are opened digitally by the end of the second quarter after launch, we stop and reconsider the approach." "If the first release is not in production with real users within six months, we return to the board with options, including stopping." Written in advance, a stop rule protects everyone. The team knows the test, the sponsor has agreed to it, and the board does not have to argue about what failure means after the money is spent.

**Why stopping is hard.** Two well-studied effects push organisations to continue failing work. The **sunk cost effect** is the tendency to keep investing because of what has already been spent; Hal Arkes and Catherine Blumer's 1985 paper "The psychology of sunk cost" is a classic study, reporting for example that theatre-goers who had paid full price for season tickets attended more performances than those who had received a discount (as reported in search summaries). **Escalation of commitment** is the tendency to put more resources into a failing course of action, especially by the people who chose it; Barry Staw's 1976 paper "Knee-deep in the big muddy" is credited with introducing the idea (as reported in search summaries). The practical defences are simple: stop rules written in advance, evidence produced from records rather than by the sponsor, and a decision that asks only whether the *next* spend is worth it.

**Limit what runs at once.** A portfolio with too many active investments moves slowly, because specialists are split across all of them and every item waits for someone. Lesson 1.2 showed that lead time grows with work in progress when throughput stays the same. The same holds at portfolio level. Set a **limit on active initiatives** for each area, based on the teams available, and start a new initiative only when one finishes or stops. At Najm Bank, Huda proposed reducing 143 active projects to no more than 40 active initiatives across the division, plus the funded products (illustrative). The first review did not need to stop 100 items; most were small and were folded into product backlogs.

**Stopping well.** Stopping is a piece of work with its own checklist:

- **Users**: who uses what has been built, and what will they do instead?
- **Data**: what records must be kept, for how long and where, under the bank's retention rules? Ask the data protection and records functions.
- **Contracts**: what notice periods, exit terms and licence commitments apply? Ask Lina, the Vendor and Sourcing Manager.
- **Components**: what must be switched off and removed from the configuration records, so that it does not become another system nobody owns?
- **Regulation**: does stopping or replacing this affect a critical service or an outsourcing arrangement the regulator has been told about? Ask Nour and the risk function whether any notification is needed.
- **People**: where do the team members go, and what knowledge must be written down first?
- **Learning**: what did the bank learn, and which assumptions turned out to be wrong?

**The decision log.** A **decision log** records each portfolio decision: the date, the investment, the decision, the evidence it rested on, the dissent, the stop rule (new or unchanged), and where any freed money and teams went. It is the record that lets the board, auditors and the next CIO see that decisions were made deliberately. It also makes one useful health measure possible: the number of investments stopped or changed in course each year, and the capacity they released.

### 🔴 Expert view

**Status colours are not evidence.** Many portfolio reports rely on red, amber and green ratings set by the project manager. A project can show green on every line while its users do not use what it delivers, a pattern sometimes called a "watermelon" report (green outside, red inside). Lesson 1.3 warned against self-reported status. Replace colours with the evidence pack, or at least require that every colour points to a measure.

**Stable priorities, deliberate change.** Governance that re-plans every month damages delivery. Google Cloud's announcement of the 2024 DORA report says that instability in priorities "can significantly hinder progress", even with strong leadership and good documentation. The quarterly cadence with a small set of triggers is the answer: the board changes the portfolio on purpose, at known times, and teams are protected between reviews. If the board finds itself making unplanned decisions every few weeks, it should look at its triggers, not add meetings.

**Separate the evidence from the advocate.** The person who sponsored an investment is the worst-placed person to judge whether it should stop, through no fault of their own. Two practices help. The portfolio office (the small team that runs the reviews, formerly the project office, lesson 2.2) prepares the evidence pack from records. And for the largest investments, an independent review at agreed points (someone from another area, or an external reviewer) tests the assumptions before more money is released. Neither replaces the sponsor's judgement; both stop the decision resting on one voice.

**Governance and assurance in a bank.** In a regulated bank the portfolio board is a first-line management body. The second line (risk and compliance) sets the rules for risk and checks that they are followed, and internal audit gives independent assurance. Nour's observer seat lets the second line see that stopping a supplier, changing a critical system or delaying an obligation was decided with the right information. It does not make the board a risk committee. Ask the risk function which portfolio decisions they need to be told about, and how, rather than assuming either "all of them" or "none". Module 10 covers controls and audit in more depth.

**Stopping is a skill the organisation learns.** The first stop is the hardest. After that, a board that stops one or two investments a quarter, with a clear record of what was learned and where the capacity went, finds that sponsors start writing better stop rules and more honest business cases. For killing ideas before they become investments, see [*AI Product Management*, lesson 2.3 — When not to use AI, and killing ideas early](../aipm/index.html#/2.3); for the same habit at the scale of a small business, see [*Founder's Playbook for AI-First Builders*, lesson 2.1 — One job, one customer: scope and the kill list](../founder/index.html#/2.1).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Portfolio board charter** | Members, decision rights, cadence, triggers and what the board does not decide | Before the first review; revisit after three reviews |
| **Evidence pack** | One page per investment: outcomes, spend, flow, run cost and incidents, risks, key assumptions | Each quarterly review, produced from records |
| **Stop rule line** | Measure, threshold and date that would end the investment | Written at funding; renewed whenever course changes |
| **Active initiative limit** | Maximum number of initiatives running at once per area | When specialists are split across too many items |
| **Stopping checklist** | Users, data, contracts, components, regulation, people, learning | Every time an investment is stopped or replaced |
| **Decision log** | Date, investment, decision, evidence, dissent, stop rule, where capacity went | Every board decision; read by the board, auditors and successors |

## 🏛️ In practice at Najm Bank
After the first quarterly portfolio review under the new model, Tariq's portfolio office published the decision log. Illustrative and fictional:

> **Retail and SME portfolio board: decision log, first quarter (extract)**
>
> | Investment | Decision | Evidence | Stop rule from now | Capacity |
> |---|---|---|---|---|
> | Loan origination replacement | **Change course**: stop the custom build; fund a ten-week comparison of two alternatives (configure a packaged system, or extend the current one) | 1.8 times original cost; first release slipped three times; two key assumptions (data migration effort, supplier staffing) failed | If no option is chosen with a costed plan in ten weeks, stop and keep the current system with a support plan | Two of four teams released to SME onboarding |
> | Cards & Payments | **Continue** | Routine card calls down from about 1.1 to 0.9 per customer a year; lead time falling; run cost within guardrail | Unchanged from funding memo | No change |
> | SME digital onboarding | **Scale up** | Digital share of new SME accounts up from 10% to 18% in a pilot branch region | Below 30% two quarters after full launch: reconsider approach | Two teams added (from loan origination) |
> | Branch queue system | **Stop** | No theme; no users beyond a pilot; stop rule (pilot adoption) not met | — | Supplier notice given; stopping checklist owner: Lina |
> | Core banking end-of-support upgrade | **Re-plan** (obligation) | On track for the date, but testing capacity short | Not applicable; deadline fixed | Platform team to provide test environments |
>
> **Dissent recorded:** the loan origination sponsor disagreed with the change of course and asked that the comparison include completing the current build; the board agreed to include it as a third option.
>
> **Active initiatives:** 61, down from 143 projects at the start of the year (most folded into product backlogs). Target: 40 by year end.

Mistakes were made on the way. Omar's first instinct was to stop the loan origination work outright at the meeting; Huda pointed out that no alternative had been costed and the old system's support contract was due for renewal, so stopping without a plan would have left the bank with neither. Tariq's first evidence pack was a status report written by each sponsor, and three items arrived green with no measures; the second pack was produced from records. Nour asked for the branch queue stop to be checked against the bank's outsourcing register before the supplier notice went out; it was not on the register, and the notice went ahead.

## 🛠️ Exercises
**🟢 Write stop rules.** Take five investments in your portfolio (or Najm Bank's). For each, write a stop rule with a measure, a threshold and a date.
*Done when:* each of the five rules names a measure that is already collected or can be collected from records, a threshold, and a date within the next twelve months, and none says only "if it is not delivering value".

<details><summary>Model answer and self-check</summary>

**Model answer.** Examples for Najm Bank: SME onboarding, "below 30% digital share of new SME accounts two quarters after full launch: reconsider the approach"; payments resilience, "if critical payment disruption is not below six hours a quarter by the end of the third quarter, return with options"; branch queue pilot, "if fewer than half of pilot branches use it daily after three months, stop". Obligations get a date-and-scope rule rather than a stop rule.

**Self-check.**
- Could a person who was not in the room tell whether the rule has been met?
- Is the measure an outcome or reliability measure, not a delivery milestone only?
- Did you agree the rule with the sponsor, or would they dispute it later?

</details>

**🟡 Run a mock portfolio review.** Prepare a one-page evidence pack for each of five investments, using real records where you can. With two colleagues playing board members, make one of the four decisions for each and fill in the decision log.
*Done when:* each pack covers outcomes, spend, flow, run cost and incidents, risks and key assumptions (or says "no record"); every decision has evidence, any dissent and a stop rule; and at least one decision is not "continue".

<details><summary>Model answer and self-check</summary>

**Model answer.** A typical first mock review finds that most packs lack outcome data, so the most common decision is "continue, with a measure to be in place by the next review". At least one item usually meets its stop rule or has no theme and no users, and one well-performing product is a candidate to scale up. The decision log is more valuable than the meeting: it shows which evidence was missing.

**Self-check.**
- Were the packs produced from records, or written by the sponsors?
- Did you record dissent, rather than presenting a false consensus?
- For any "scale up", did you name where the capacity comes from?
- For any "stop", did you start the stopping checklist?

</details>

**🔴 Design the governance and set an initiative limit.** Write a portfolio board charter for one area: members, decision rights, cadence, triggers, the evidence pack, and what the board does not decide. Set an active initiative limit based on the number of teams, and list which current initiatives would be folded into product backlogs, finished or stopped to meet it.
*Done when:* the charter fits on one page, each trigger is a checkable event, the limit is justified by team numbers, the list accounts for every current initiative, and the charter names which decisions the risk function must be told about (as agreed with them, or as an open question).

<details><summary>Model answer and self-check</summary>

**Model answer.** Najm Bank's charter: chaired by Omar; business heads, Huda, Tariq and Yousef as members; Nour as observer. Decides the theme mix, initiatives above product guardrails, and continue, change, scale or stop. Does not reorder product backlogs or approve individual changes. Quarterly cadence; triggers are a guardrail breach, a stop rule met, a major incident with a structural cause, or a regulatory change. Limit: about one active initiative per two available teams outside the funded products (illustrative), giving 40. Of 143 projects, about 80 fold into product backlogs, 15 finish within the quarter, 8 are stopped and the rest stay as initiatives. Open question to Nour: which stops and supplier exits need second-line review before notice is given.

**Self-check.**
- Does the charter say what the board does *not* decide, so it does not become a bottleneck?
- Is the limit based on capacity, not on a round number?
- Did you account for every current item, not just the easy ones?
- Did you leave the regulatory judgement to the risk function?

</details>

## ⚠️ Mistakes and traps
- **Reviews that only report.** A meeting that hears status and makes no decisions is not governance. Every item ends with continue, change course, scale up or stop, and the reason.
- **Stop rules written after the fact.** Deciding what failure means once the money is spent invites argument and sunk-cost thinking. Write the rule at funding.
- **Sponsor-written evidence.** Packs written by the people who chose the investment tend to be optimistic. Produce the evidence from records, and use independent review for the largest items.
- **Stopping without a plan.** Ending work abruptly can leave users, data, contracts and systems orphaned. Use the stopping checklist and give someone ownership of it.
- **Too many things at once.** A portfolio with no limit on active work moves slowly everywhere. Set a limit and start new work when something finishes or stops.
- **Re-planning on request.** Changing priorities between reviews whenever a senior person asks damages delivery. Use a fixed cadence and a short list of triggers.

## 🧾 Recap
- **Portfolio governance** reviews all investments together on a steady **cadence**, with **triggers** for early review, and produces **decisions**, not status reports.
- Every investment comes with the same **evidence pack**, produced from records: outcomes, spend, flow, run cost and incidents, risks and key assumptions.
- The board makes one of four decisions: **continue, change course, scale up or stop**; obligations are re-planned, not stopped.
- **Write the stop rule at funding**; it counters the sunk cost effect and escalation of commitment.
- **Limit active initiatives**, **stop well** with a checklist, and keep a **decision log** that shows what was stopped and where capacity went.
- In a bank, the board is a first-line body; agree with the risk function which decisions it must see.

## ✍️ Check yourself
**1. The loan origination sponsor argues that the bank has already spent too much to stop. What question should the board ask instead?**

- A. How much more must be spent to recover the money already invested in the work?
- B. Whether the next spend is worth it, given what we now know and the alternatives.
- C. Whether the sponsor still has confidence that the team is nearly finished with it.
- D. How the money already spent can be shown as an asset so that stopping costs less.

<details><summary>Answer</summary>

**B.** Money already spent is gone whatever the board decides; only future spend is in question. A and D are sunk-cost reasoning in different forms, and C relies on the person most exposed to escalation of commitment. See "Why stopping is hard".

</details>

**2. Which is a well-written stop rule for SME digital onboarding?**

- A. If the work stops delivering value for SME customers, the board will consider stopping it.
- B. If the sponsor loses confidence in the approach, the team will bring options to the board.
- C. If the project is reported amber or red for two quarters, it will be reviewed for stopping.
- D. If digital share of new SME accounts is below 30% two quarters after launch, reconsider.

<details><summary>Answer</summary>

**D.** It names a measure, a threshold and a date that anyone can check. A is vague, B depends on one person's view, and C relies on self-reported colours rather than outcomes. See "Write the stop rule at the start".

</details>

**3. The board decides to scale up SME onboarding by adding two teams. What must the decision also record?**

- A. Where the two teams come from, so the capacity is taken from somewhere named.
- B. A new business case of full length, since any increase needs a full approval cycle.
- C. A promise that the stop rule will be removed now that the evidence is positive.
- D. The names of the SME customers who took part in the pilot, for the board's file.

<details><summary>Answer</summary>

**A.** Scaling up is a reallocation, so the log records where capacity comes from. B ignores the tiering in lesson 3.2, C removes a safeguard just when more money is at stake, and D is not needed and raises data protection concerns. See "Four decisions" and "The decision log".

</details>

**4. Tariq's first evidence pack is a set of status reports written by each sponsor, and three items arrive green with no measures. What should change?**

- A. Ask the sponsors to add more detail and commentary to explain each of their colours.
- B. Drop the evidence pack and let each sponsor present their investment in person instead.
- C. Produce the pack from records, with the same page of measures for every investment.
- D. Accept green items without discussion, so the board can spend its time on red items.

<details><summary>Answer</summary>

**C.** A common page produced from records makes investments comparable and removes the advocate from the evidence. A and B keep the sponsor in control of the evidence, and D trusts colours that can hide problems. See "The evidence pack" and "Status colours are not evidence".

</details>

**5. Between quarterly reviews, the head of corporate banking asks Omar to switch two teams to a new corporate project at once. No trigger has been met. What should Omar do?**

- A. Agree at once, because a senior business head's request is a trigger in its own right.
- B. Bring it to the next quarterly review, unless it meets one of the agreed triggers.
- C. Call an extra board meeting this week, so that the request can be decided quickly.
- D. Ask the two teams to split their time between both pieces of work until the review.

<details><summary>Answer</summary>

**B.** A fixed cadence with defined triggers keeps priorities stable; requests that meet no trigger wait for the review. A and C turn every senior request into re-planning, which the 2024 DORA findings associate with hindered progress, and D splits teams and raises work in progress. See "Cadence and triggers" and "Stable priorities, deliberate change".

</details>

## 📚 References
- Google Cloud blog, "Announcing the 2024 DORA report", 22 October 2024 (opened 2026-11-20; source of the quoted finding on unstable priorities): https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
- Arkes, H. R. and Blumer, C., "The psychology of sunk cost", *Organizational Behavior and Human Decision Processes* 35(1): 124–140 (1985). Citation and the season-ticket finding as reported in search summaries; paper not opened.
- Staw, B. M., "Knee-deep in the big muddy: A study of escalating commitment to a chosen course of action", *Organizational Behavior and Human Performance* 16: 27–44 (1976). Citation as reported in search summaries; paper not opened.
- Wikipedia, "Escalation of commitment" (overview and further reading; as reported in search summaries; not opened): https://en.wikipedia.org/wiki/Escalation_of_commitment
- Library course: [*AI Product Management*, lesson 2.3 — When not to use AI, and killing ideas early](../aipm/index.html#/2.3).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 2.1 — One job, one customer: scope and the kill list](../founder/index.html#/2.1).
