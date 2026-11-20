# Module 3 — Strategy and portfolio

*Module 2 gave Najm Bank's Technology division products with named owners and teams arranged around them. That raises the next question: how much money and how many teams should each product and each new idea get, and who decides? Today the answer is an annual budget built from more than a hundred project requests, approved once a year and rarely changed. This module replaces it in three steps. First, the bank's strategy is turned into a few outcome themes, and every piece of IT spend and work is placed on one page, the investment portfolio, so that leaders can see whether the money says the same thing as the strategy. Second, work is prioritised by what delay costs, business cases are sized to the decision, and long-lived products are funded as teams with guardrails rather than as a string of projects. Third, the portfolio is reviewed on a steady cadence with evidence, and investments are re-planned or stopped by rules written before the money was spent. Each lesson leaves an artefact: a portfolio one-pager, a prioritised list with a product funding memo, and a review pack with a decision log.*

> **Steps:** Plan, Fund — decide what IT invests in and why, how money and team capacity follow the strategy, and how those choices are reviewed, changed and stopped.

---

# 3.1 — From strategy to an investment portfolio
*Level: 🟡 Intermediate* · *Prerequisites: 1.1, 2.1, 2.2* · *Step: Plan, Fund*

**After this you can** turn a stated business strategy into three to five outcome themes with measures, place every product, initiative and obligation of one IT area on a one-page investment portfolio by category and horizon, and show in one chart where the money and team capacity disagree with the strategy. *Study time: reading about 15 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- A **strategy** is a set of choices made in response to a clear diagnosis. A list of goals is not a strategy.
- An **investment portfolio** is everything IT spends money and team capacity on (products, initiatives, obligations), seen together so it can be balanced and changed.
- Turn the strategy into **three to five outcome themes** with measures; tag every investment with theme, **category** (run, change, obligation) and **horizon** (core, emerging, option).
- The rule that matters most: **your real strategy is what you fund.** If money and teams point elsewhere, the strategy document is a wish.
- Decision cue: if your portfolio cannot explain what it is *not* funding, it is a list, not a portfolio.
- Biggest trap: building next year's budget by adding up each business line's requests, then writing the strategy slide afterwards.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

The board approved a three-year strategy for Najm Bank with three headlines: grow SME banking through digital channels, lower the cost to serve retail customers, and become more resilient after three payment outages last year. Omar, the Chief Information Officer, was asked to show how the Technology plan supports it.

Tariq, the IT Finance Business Partner, pulled the whole division's numbers: 143 approved projects and about 420 applications, with roughly seven in ten of every unit of money spent keeping existing systems running. The largest share of change money went to a corporate treasury upgrade no headline mentioned; SME digital work received less than a tenth, and resilience was not a theme at all.

Each project had been approved on its own merits, but no one had asked whether, taken together, they said what the board said. Huda, Head of Enterprise Architecture, put it plainly: "We have a strategy and a budget, and nothing that connects them." This lesson builds that connection.

## 📐 How it works

### 🟢 The essentials

**Strategy, in a form you can fund.** Richard Rumelt's *Good Strategy Bad Strategy* describes the core of a good strategy as a **diagnosis**, a **guiding policy** and **coherent actions**, and warns against mistaking goals for strategy (as reported in summaries of the book). A strategy you can fund contains **choices**: what the bank will do more of, less of, and why. "Be the best digital bank in the region" is a goal. "SME customers leave because opening an account takes three weeks and a branch visit; we will make SME onboarding fully digital first" is a choice. You can fund the second.

**Outcome themes.** Between a board strategy and a team's work sits a small set of **outcome themes**: three to five statements of the change the bank wants to see, each with one or two measures. A theme is a result several investments contribute to, not a project or a department.

| Strategy headline | Outcome theme | Example measure |
|---|---|---|
| Grow SME banking digitally | SME customers can open and run accounts without a branch | Share of SME accounts opened digitally; time to open |
| Lower cost to serve retail | Retail customers solve routine needs themselves | Calls per active customer; cost per transaction |
| Become more resilient | Critical payment services recover quickly and fail rarely | Hours of critical service disruption; time to restore |

With ten themes, everything fits somewhere and nothing is excluded.

**The investment portfolio.** A **portfolio** is the whole set of investments seen together. An **investment** is any decision to spend money or team capacity for a purpose: a **product** (lesson 2.1, long-lived), an **initiative** (time-bound work with an end, such as a data-centre exit; the projects that remain legitimate) or an **obligation** (required by a law, regulator, audit finding, contract or end of support).

A **programme** (related projects managed together) is a delivery container; the portfolio is a decision tool. Tag every investment three ways:

- **Theme**: which outcome theme it serves, or "none".
- **Category**: **run** (keep an existing product or component working, safe and supported), **change** (improve a product or build something new), or **obligation** (must be done, by a date or condition, whatever its value).
- **Horizon**: **core** (improving what the bank does today), **emerging** (growing something new that is starting to work), or **option** (small bets that may matter later). These labels follow, in short form, the three horizons of *The Alchemy of Growth* by Baghai, Coley and White (as reported in summaries of the book).

### 🟡 Going deeper

**The portfolio one-pager.** One page a board member can read in five minutes: the **themes** with measures; the **allocation** of money and teams by theme, category and horizon, this year beside proposed; the **gaps** (under-funded themes, untagged investments, run costs rising without a decision); and the **choices** (start, grow, shrink, stop, and what will not be funded).

An extract from the division-wide page (Cards & Payments grew from the pilot's one team in lesson 2.2 to three once the pilot was extended):

| Investment | Type | Theme | Category | Horizon | Money (share of division) | Teams | Owner |
|---|---|---|---|---|---|---|---|
| Cards & Payments app | Product | Retail self-service | Change and run | Core | 6% | 3 | Reem |
| SME digital onboarding | Product (new) | SME digital | Change | Emerging | 2% | 1 | To be named |
| Payments resilience | Initiative | Resilience | Change | Core | 3% | 2 | Yousef |
| Core banking end-of-support upgrade | Obligation | Resilience | Obligation | Core | 5% | 2 | Huda |
| Corporate treasury upgrade | Initiative | None | Change | Core | 7% | 3 | Treasury sponsor |

Illustrative figures, not benchmarks. The treasury upgrade is the largest change item and serves no theme. That does not mean it should stop; someone must explain the choice in the open.

**Money and capacity are two currencies.** Banks budget in money, but software work is limited by **team capacity**: the number of stable teams able to do it. A theme can be funded and still starve because no team is free. Show both columns.

**Run is a decision too.** Run spend grows when nothing is retired, when old versions need extended support, and when **technical debt** (the accumulated cost of earlier shortcuts that makes change slower or riskier) is left alone. Show run cost per product and ask, for the largest items, "keep, simplify, replace or retire?" (lesson 10.1 builds the cost model). Label obligations honestly too (lesson 1.1): the date may be fixed, but how much to do and how usually are not.

**Outcome measures, not activity.** "SME features delivered" is activity; "share of SME accounts opened digitally" is an outcome. Some organisations write these as **objectives and key results (OKRs)**, an objective with a few measurable key results, popularised by John Doerr's *Measure What Matters* (as reported in summaries). The label is optional; a measure the teams can move is not.

### 🔴 Expert view

**The portfolio reveals the strategy you actually have.** Whatever the document says, the allocation table shows what the organisation has chosen. Try showing leaders the twenty largest investments and their money, with no theme tags, and ask them to guess the board's strategy. If nobody guesses the headlines, the gap is visible to everyone.

**Balance, not optimisation.** Ranking every investment by expected return fails. Run and obligation work is the cost of staying in business, and emerging and option work has returns too uncertain for one number. Decide the target **mix** first, then rank within each part (lesson 3.2).

**Stable priorities are an asset.** Google Cloud's announcement of the 2024 DORA report says that "instability in priorities, even with strong leadership, comprehensive documentation, and a user-centered approach … can significantly hinder progress." Google Cloud's post on the 2023 DORA report states that teams that focus on the user have 40% higher organizational performance than teams that don't. This course reads the two together as favouring a portfolio tied to user outcomes and changed on a steady cadence (lesson 3.3) over one re-planned whenever a senior person asks.

**Risk appetite belongs in the portfolio.** Show where the portfolio spends to reduce risk and where it takes risk, against the board's **risk appetite** (how much risk of what kinds it will take to meet its goals). Ask the risk function which investments touch operational resilience, outsourcing or technology risk rules. See [*AI Governance: Zero to Hero*, lesson 2.1 — From principles to strategy and risk appetite](../aigp/index.html#/2.1); for product strategy in the AI context, see [*AI Product Management*, lesson 9.1 — AI product strategy and defensibility](../aipm/index.html#/9.1).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Strategy kernel page** | Diagnosis, guiding policy and coherent actions, in half a page | Before writing themes |
| **Outcome theme sheet** | Three to five themes with measures, baselines and owners | Translating a board strategy into something IT can fund |
| **Portfolio one-pager** | Every investment with its tags, money, teams and owner, plus gaps and choices | Annual planning and each quarterly review (lesson 3.3) |
| **Allocation mix chart** | Money and teams by theme, category and horizon, current against target | Starting the leadership conversation about balance |
| **Spreadsheet or portfolio management tool** | Where the portfolio lives; a spreadsheet first, a tool later | When the spreadsheet has many editors (examples, not endorsements) |

## 🏛️ In practice at Najm Bank
Huda and Tariq built the first portfolio one-pager for the retail and SME area (24 teams and about 50 of the division's 143 projects). Illustrative and fictional:

> **Retail and SME technology portfolio: one-pager (draft for leadership)**
>
> **Themes:** (1) SME digital: share of SME accounts opened digitally, today about 10%. (2) Retail self-service: calls per active retail customer per year, today about 4. (3) Resilience: hours of disruption to critical payment services per quarter, last quarter about 9.
>
> **Allocation today (share of the area's money / teams):** Run 68% / 9 teams. Change 22% / 11 teams. Obligation 10% / 4 teams. By theme, change money: SME digital 8%, retail self-service 41%, resilience 12%, no theme 39%.
>
> **Gaps:** SME digital, the board's first headline, receives the smallest share. Thirty-one projects carry no theme. Run cost for the old internet-banking platform rose by about a fifth after extended support was bought; no decision was recorded.
>
> **Proposed choices:** grow SME digital onboarding to two teams; fund payments resilience as a named initiative with its own measure; decide keep, simplify or retire for the old internet-banking platform within one quarter; ask each sponsor of an untagged project to name its theme or obligation before the next review.
>
> **Not funded this year:** a full roll-out of the branch-queue system (its existing pilot runs only until its stop rule is checked) and a retail chatbot pilot, because neither moves a theme measure more than the work above.

Huda's first draft had eleven themes, one per business line. Omar sent it back: "Eleven themes means we are still funding departments." Tariq spent two weeks splitting shared costs to two decimal places before themes were agreed; Yousef pointed out that a rough split would do.

## 🛠️ Exercises
**🟢 Write the themes.** Take your organisation's strategy (or Najm Bank's three headlines). Write a half-page strategy kernel and three to five outcome themes, each with one measure and its current value or "unknown".
*Done when:* there are at most five themes, each measure is an outcome or reliability result rather than IT activity, and the kernel names at least one thing to do less of.

<details><summary>Model answer and self-check</summary>

**Model answer.** Diagnosis: "SME onboarding is slow and branch-bound; routine retail calls are high; three payment outages damaged trust". Guiding policy: "digital SME onboarding first; self-service for the ten commonest retail requests; payment resilience before new payment features". Less of: "new branch technology and projects without a theme". Themes as in the 🏛️ section.

**Self-check.**
- Could a stranger disagree with your guiding policy? If not, it is still a goal.
- Is every measure something a team's work could move within a year?
- Did you mark "unknown" rather than invent a baseline?

</details>

**🟡 Build the portfolio one-pager.** For one IT area (at least fifteen investments), list each with theme, category, horizon, share of money, teams and owner. Add the gaps and proposed choices.
*Done when:* every row has three tags and an owner (or "none", flagged as a gap), money and teams add up to the area total, and the page names at least one thing that will not be funded.

<details><summary>Model answer and self-check</summary>

**Model answer.** A first one-pager usually shows a large run share, several untagged items, an under-funded theme and teams spread thinly. Strong drafts make two or three clear proposals rather than reallocating everything.

**Self-check.**
- Did you include run and obligation work, not only new projects?
- Is the teams column in real, stable teams, not fractions of people?
- Did the "no theme" items get a question, not an automatic stop?

</details>

**🔴 Show the gap and propose a target mix.** Draw the allocation mix chart for today and a target for next year. Write five lines on what must change, and the risks it creates.
*Done when:* both mixes share one chart and scale, run and obligation work stay realistic, each line names an owner, and at least one line is a question for the risk function.

<details><summary>Model answer and self-check</summary>

**Model answer.** Najm Bank's target mix moves SME digital from 8% to about 20% of change money (illustrative), funds resilience as its own initiative, and cuts "no theme" change work from 39% to below 10%; run falls slightly through one retirement. The five lines: Omar agrees the mix with the business heads; Tariq moves two teams' funding at the next quarterly review; Huda leads the retire-or-keep decision on the old internet-banking platform; Reem shares one team with SME onboarding for a quarter; Nour asks whether the resilience work touches rules that need notice to the regulator.

**Self-check.**
- Is the target mix achievable within a year, given that teams cannot move overnight?
- Did you avoid cutting run or obligation work to flatter the chart?
- Did you ask the risk function a question rather than state a regulatory conclusion?

</details>

## ⚠️ Mistakes and traps
- **Budget by accumulation.** Adding up requests reproduces last year's politics. Start from themes and a target mix.
- **Too many themes.** Ten themes exclude nothing. Keep three to five.
- **Activity measures dressed as outcomes.** "Features delivered" rises whatever customers do. Measure outcomes.
- **Run treated as fixed.** Decide keep, simplify, replace or retire on the largest run items.
- **Precision before agreement.** Use rough cost shares until themes are agreed.

## 🧾 Recap
- A fundable strategy contains **choices**: diagnosis, guiding policy, coherent actions, and what to do less of.
- Translate it into **three to five outcome themes** with measures and baselines.
- The **portfolio** holds all products, initiatives and obligations, tagged by **theme, category and horizon**, with money and teams.
- **Your real strategy is what you fund.**
- Decide the **mix** before ranking, and change priorities on a **cadence**.

## ✍️ Check yourself
**1. The board's strategy says "be the leading digital bank for SMEs". Huda wants to turn it into something IT can fund. What should she do first?**

- A. Ask each business line for its project list and group the projects under the headline.
- B. Buy a portfolio management tool so that SME projects can be tracked in one place.
- C. Ask what is stopping SME customers today and agree the choices that follow from that.
- D. Set a target for the number of SME features the teams must deliver in the next year.

<details><summary>Answer</summary>

**C.** A fundable strategy starts from a diagnosis and the choices that follow. A is budgeting by accumulation, B buys a tool before the decision exists, and D is an activity target. See "Strategy, in a form you can fund".

</details>

**2. Tariq's portfolio shows that the SME theme has money for next year, but no team is free to work on it. What does this tell Omar?**

- A. The theme is under-resourced, because capacity as well as money limits what gets done.
- B. The theme is adequately resourced, since money can always be turned into people later.
- C. The theme should be removed, since a theme without a team cannot have a useful measure.
- D. The theme is a run cost and should be moved into the category that keeps systems going.

<details><summary>Answer</summary>

**A.** Money and team capacity are two currencies; a theme can be funded and still starve. B assumes moving teams is instant, C drops a strategic theme, and D confuses category with resourcing. See "Money and capacity are two currencies".

</details>

**3. Which of these is an outcome measure suitable for Najm Bank's retail self-service theme?**

- A. The number of self-service screens released in the retail app during the year.
- B. The share of the retail change budget that has been spent by the end of each quarter.
- C. The number of retail projects closed on time and within budget during the year.
- D. The number of calls per active retail customer for routine needs such as card limits.

<details><summary>Answer</summary>

**D.** It describes what customers do differently. A and C count IT activity that would rise whatever customers do, and B measures spending, not results. See "Outcome measures, not activity".

</details>

**4. A corporate treasury upgrade is the largest change item in the division's portfolio and serves no theme. What should the portfolio one-pager do with it?**

- A. Stop it at once, because any work without a theme is outside the strategy by definition.
- B. Flag it as a gap and ask its sponsor to explain it against a theme or as an obligation.
- C. Leave it off the page, because corporate work belongs to a different business line.
- D. Assign it to the resilience theme, since most upgrades make systems more reliable.

<details><summary>Answer</summary>

**B.** An item with no theme is a question to answer in the open, not an automatic stop. A acts without evidence, C hides spend, and D relabels the work to tidy the chart. See "The portfolio one-pager".

</details>

**5. Omar proposes ranking every investment, including run and obligation work, by expected financial return and funding from the top. What is the main problem?**

- A. Run and obligation work do not compete on return, and early bets would be unfairly ranked.
- B. Financial return cannot be estimated for any IT investment, so no ranking is possible.
- C. A ranking would take too long, because a portfolio has too many investments to compare.
- D. Ranking by return is reserved for the board and cannot be done by the IT leadership team.

<details><summary>Answer</summary>

**A.** Run and obligation work are the cost of staying in business, and early bets have returns too uncertain for one number. B overstates the problem, C is not the issue, and D invents a rule. See "Balance, not optimisation".

</details>

## 📚 References
- Google Cloud blog, "Announcing the 2024 DORA report", 22 October 2024 (opened 2026-11-20; source of the quoted finding on unstable priorities): https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
- Google Cloud blog, "2023 State of DevOps Report: Culture is everything", October 2023 (opened 2026-11-20; source of the 40% user-focus finding): https://cloud.google.com/blog/products/devops-sre/announcing-the-2023-state-of-devops-report
- Rumelt, R. P., *Good Strategy Bad Strategy: The Difference and Why It Matters* (Crown Business, 2011). The "kernel" (diagnosis, guiding policy, coherent action) as reported in summaries; book not opened.
- Baghai, M., Coley, S. and White, D., *The Alchemy of Growth* (Perseus Books, 1999; some sources give 2000). Three horizons as reported in summaries; book not opened.
- Doerr, J., *Measure What Matters* (Portfolio/Penguin, 2018). OKRs as reported in summaries; book not opened.
- Library course: [*AI Governance: Zero to Hero*, lesson 2.1 — From principles to strategy and risk appetite](../aigp/index.html#/2.1) (risk appetite set by the board, in the AI context).
- Library course: [*AI Product Management*, lesson 9.1 — AI product strategy and defensibility](../aipm/index.html#/9.1) (product strategy for one product, below the portfolio).

---

# 3.2 — Prioritising and funding work: business cases, cost of delay and funding products not projects
*Level: 🟡 Intermediate* · *Prerequisites: 1.2, 2.1, 3.1* · *Step: Fund*

**After this you can** size a business case to the decision it supports, estimate the cost of delay for five pieces of work and put them in order by cost of delay divided by duration, and write a one-page funding memo that funds a product as a team with guardrails and a review date. *Study time: reading about 15 min, hands-on about 110 min (estimate).*

## ⚡ In 60 seconds
- A **business case** is the argument for spending money: problem, options (including doing nothing), costs and benefits as ranges, risks, and deciding assumptions. Its size should match the decision.
- **Cost of delay** is the value lost for each week a piece of work is not in use. It turns "urgent" into a number people can challenge.
- When team capacity is the constraint, do first the work with the highest **cost of delay divided by duration** (**CD3**).
- The rule that matters most: **fund the team for the period, steer the work every week, and ask for a business case only in proportion to the decision.**
- Decision cue: if a two-week change waits two months for money, the funding model is the bottleneck.
- Biggest trap: precise-looking business cases built on single-point estimates, approved once and never checked again.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

In lesson 1.2's value-stream map, the longest wait was the funding decision: the investment committee met quarterly and wanted a business case for every change above a modest threshold (the monthly small-change experiment agreed there covered only smaller items). Reem, Product Manager for Cards & Payments, had a card freeze feature above that threshold, three weeks of work: a temporary, reversible freeze for a mislaid card, unlike the existing permanent block. Most such customers phoned the contact centre to block the card outright, and the fraud team said lost-card fraud often happened before the call got through. The feature waited a quarter for money.

Reem's case ran to fourteen pages, with a five-year **net present value** (future cash flows converted to today's money) to the nearest thousand. Tariq, the IT Finance Business Partner, admitted most numbers were guesses with decimal places. Meanwhile, a corporate treasury upgrade approved two years earlier on an equally confident case was nearly twice its original cost, and no one had reopened it.

Small work waited because it was treated like a large investment; large, risky work kept going because approval was a one-time event. This lesson fixes both.

## 📐 How it works

### 🟢 The essentials

**What a business case is for.** A **business case** argues that a use of money and people is worth it compared with the alternatives. It covers the **problem** (which outcome theme, lesson 3.1), the **options** (always including **doing nothing**, which has a cost too), **costs** to build, run and retire, **benefits** and how they will be measured, all as ranges, the **risks**, and the two or three **assumptions that would change the answer**. That last item tells reviewers what to check, and the portfolio review (lesson 3.3) what evidence would justify stopping.

**Size the case to the decision.** A simple tiering:

| Decision size | Example | What is needed | Who decides |
|---|---|---|---|
| Within a funded product's guardrails | Card freeze feature | A backlog item with outcome and cost of delay | Product manager |
| New, time-bound, moderate | Supplier interface migration | A one-page case with options and ranges | Portfolio board (lesson 3.3) |
| Large, new or high-risk | New SME onboarding platform | Full case, independent estimate review, staged funding | Investment committee, with risk input |

The thresholds are the bank's to set with finance.

**Cost of delay.** **Cost of delay** is the value lost, per unit of time, while work is not yet in use: money not earned, costs not saved, losses not prevented, risks left open. Don Reinertsen's *The Principles of Product Development Flow* (2009) made the idea widely known. Ask: "If this arrives one week later, what do we lose in that week?" For card freeze, Reem's team counted continuing contact-centre calls and the fraud losses attributed to slow blocking. The answer was a range, and that is fine.

**Shapes of urgency.** Cost of delay is not always constant:

| Shape | What it looks like | Example at Najm Bank |
|---|---|---|
| **Steady** | Each week of delay loses about the same amount | Card freeze: calls and fraud continue weekly |
| **Deadline** | Little loss until a date, then a large one | A card-scheme rule change with a fixed compliance date |
| **Closing window** | Value shrinks the later you arrive, then disappears | A seasonal SME campaign tied to a trade event |

Deadline work must start early enough to finish by the date, not necessarily first. Closing-window work goes first or not at all.

### 🟡 Going deeper

**Ordering work by CD3.** When a team's capacity is the constraint, the order of work changes the total cost of waiting. Divide cost of delay by duration (the time the work occupies the team) and do the highest first. Joshua Arnold's Black Swan Farming site calls this **CD3**. Reinertsen's book calls the general idea weighted shortest job first; some variants divide by job size rather than duration (as reported in search summaries). Reem's four items (cost of delay in thousands of the bank's currency per week, illustrative):

| Item | Cost of delay per week | Duration (weeks) | CD3 |
|---|---|---|---|
| Card freeze | 30 | 3 | 10.0 |
| Fee display fix | 8 | 1 | 8.0 |
| Mobile wallet support | 50 | 10 | 5.0 |
| Rewards card design | 20 | 8 | 2.5 |

One at a time, the total cost of waiting (each item's weekly cost of delay times its finishing week) is about 1,262 in CD3 order, 1,486 biggest-first and 1,468 shortest-first (illustrative).

Three cautions. CD3 orders work within one constraint; it does not set the mix (lesson 3.1). Deadline and obligation work is scheduled to its date. And the inputs are estimates: use ranges or relative scales (1, 2, 5, 10, 20) when people cannot agree on money.

**Estimates as ranges, and the outside view.** A single-point estimate ("4.2 million, nine months") hides uncertainty. Ask for low, likely and high figures, and compare with similar past work. This **outside view**, **reference class forecasting**, was proposed for project management by Bent Flyvbjerg, building on Daniel Kahneman and Amos Tversky's work (as reported in search summaries). It counters **optimism bias**, the tendency to expect things to go better than they usually do.

Flyvbjerg and Alexander Budzier (*Harvard Business Review*, 2011) reported on 1,471 IT projects: the average cost overrun was 27%, but one in six had a cost overrun averaging 200% and a schedule overrun of almost 70% (as reported; the figures match the SSRN abstract). Averages hide a fat tail, so stage large investments.

**Three ways to fund work.**

| Funding model | How it works | Fits | Watch out for |
|---|---|---|---|
| **Project funding** | Money for a scope, date and budget; the team disbands at the end | Truly time-bound work, such as a data-centre exit | Re-approval to change course; knowledge leaves |
| **Product (team) funding** | A stable team and its run costs funded for a period, reviewed quarterly | Long-lived products and platforms | Funding becomes permanent by habit |
| **Staged (metered) funding** | A small amount to test the riskiest assumptions; more money follows evidence | New products; emerging and option horizons | "Prove it" with no time or money to do so |

Apart from the small-change experiment, Najm Bank used project funding for everything. The target: product funding for products and platforms, staged funding for new bets, project funding only where work really ends.

**Guardrails make product funding safe.** **Guardrails** (lesson 2.2) are rules set in advance inside which the product manager decides alone: outcome measures reported quarterly, a spending envelope, a ceiling on run-cost growth, a size threshold above which new initiatives go to the portfolio board, and the bank's risk appetite and change policy, unchanged. Inside them, the product manager reorders the backlog weekly by cost of delay.

### 🔴 Expert view

**Annual budgets and changing priorities.** Product funding keeps the annual budget but changes what it buys (teams and envelopes, not project scopes) and adds quarterly re-allocation.

**Questions for finance, not conclusions.** Ask Tariq and the finance function: under the bank's accounting policy, which development costs may be capitalised (recorded as an asset and spread over years), and does that depend on project or product-team work? How is time evidenced without project timesheets? How does quarterly re-allocation fit approval rules? Finance decides; the operating model makes the evidence easy.

**Check the case after the fact.** Keep each case's key assumptions in the investment record (lesson 9.1) and review them quarterly; this builds the bank's own reference class, and stops sponsors being rewarded for large promises. For AI use cases with risk tiers, see [*AI Governance: Zero to Hero*, lesson 8.1 — Use-case intake, business case and risk tiering](../aigp/index.html#/8.1); for planning bets when the technology itself is uncertain, see [*AI Product Management*, lesson 9.2 — Roadmaps under uncertainty: bets, platforms and model change](../aipm/index.html#/9.2).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Business case tiers** | Decision sizes, what each needs and who decides | When small changes wait for large-investment paperwork |
| **One-page business case** | Problem, options, ranges, risks, deciding assumptions | Moderate, time-bound investments |
| **Cost of delay sheet** | Each item's cost of delay, urgency shape, duration and CD3 | Ordering a backlog or competing initiatives |
| **Product funding memo** | Team, period, envelope, measures, guardrails, review date | Moving a product to team funding |
| **Finance question list** | Capitalisation, time evidence, re-allocation and approval rules | Before the first funding memo is signed |

## 🏛️ In practice at Najm Bank
Tariq and Reem wrote Najm Bank's first product funding memo for Cards & Payments. Illustrative and fictional:

> **Product funding memo: Cards & Payments (draft for the investment committee)**
>
> **What is funded:** three stable product teams (about 24 people, two from a supplier; the product grew from one team after the lesson 2.2 pilot), the product's run costs and the card-processing contract, for one year, reviewed quarterly.
>
> **Outcome measures (theme: retail self-service):** routine card calls per active card customer, today about 1.1 a year; lost-card fraud losses per quarter. Reliability: card payment availability against its service level (lesson 8.3).
>
> **Guardrails:** spend within the agreed envelope; run cost growth above 10% in a quarter, or any new initiative above about eight team-weeks or touching another product's interface, goes to the portfolio board; change policy and risk appetite unchanged.
>
> **How work is ordered:** weekly by CD3, obligations scheduled to their dates; the sheet is visible to the portfolio office (the team, formerly the project office, that prepares portfolio evidence).
>
> **Questions agreed with finance before signing:** which development costs the bank will capitalise; how team time is evidenced from the delivery tool rather than timesheets; how a quarterly re-allocation is approved.
>
> **Review:** quarterly at the portfolio board, with outcome, cost and flow evidence (lesson 3.3); first in three months.

Reem's first guardrail said "spend as needed within the product's goals"; Tariq rejected it as a blank cheque. His first threshold, two team-weeks, would have sent half the backlog back to the committee; they settled on eight. The committee approved a one-year pilot, and card freeze was built in the first three weeks.

## 🛠️ Exercises
**🟢 Tier your decisions.** Write a three-tier business case table (size, example, what is needed, who decides) and place five recent funding requests in it.
*Done when:* each tier has a checkable threshold (money, team-weeks or risk), the five requests are placed, and any over- or under-scrutinised are marked.

<details><summary>Model answer and self-check</summary>

**Model answer.** Najm Bank's table is the one in "Size the case to the decision". Two small card changes had full cases (over-scrutinised); one large supplier extension was renewed with no case (under-scrutinised).

**Self-check.**
- Is each threshold measurable, not "significant" or "strategic"?
- Did you find at least one request treated wrongly for its size?
- Does every tier name one decider?

</details>

**🟡 Order five items by CD3.** Take five items competing for one team (or Reem's four plus one). Estimate each one's cost of delay, shape, duration and CD3. Order them and compare the total cost of waiting with one other order.
*Done when:* each item has a reasoned cost of delay, a shape, a duration and a CD3; deadline items are scheduled to their date; and both totals are shown.

<details><summary>Model answer and self-check</summary>

**Model answer.** CD3 order for Reem's four items is card freeze, fee display fix, mobile wallet, rewards design: about 1,262 against about 1,486 for "biggest first". A card-scheme rule change due in twelve weeks, taking four, is not ranked; it must start by week eight, so it goes after the fee fix and before the wallet, delaying the wallet four weeks, a cost the plan should state.

**Self-check.**
- Did you write down why each cost of delay is what it is?
- Did you treat deadline work separately?
- Is duration the time the item occupies the team?

</details>

**🔴 Write a product funding memo.** For one product (yours or Najm Bank's corporate payments product), write a one-page memo: what is funded, outcome measures, guardrails, how work is ordered, questions for finance, review date.
*Done when:* it fits on one page, every guardrail is checkable, measures have baselines or "unknown", finance items are questions not conclusions, and the review is within three months.

<details><summary>Model answer and self-check</summary>

**Model answer.** A good memo resembles the Cards & Payments one: a stable team funded for a year, reviewed quarterly; two or three outcome measures plus a reliability measure; four or five checkable guardrails; weekly ordering by cost of delay; finance questions; a first review date.

**Self-check.**
- Could finance tell from your guardrails when the product manager must come back?
- Is any guardrail really a principle in disguise ("act responsibly")?
- Did you leave the accounting answers to finance?

</details>

## ⚠️ Mistakes and traps
- **One process for every size.** A three-week change treated like a three-year programme waits. Tier the case to the decision.
- **False precision.** A net present value to the nearest thousand built on guesses misleads. Use ranges and past actuals.
- **Ranking without cost of delay.** "High, medium, low" labels hide the reasons. Estimate what a week of delay costs, even roughly.
- **Product funding without guardrails.** A team funded "to deliver value" with no thresholds loses finance's trust. Write checkable guardrails.
- **IT deciding accounting.** Capitalisation and budget rules belong to finance. Bring questions.

## 🧾 Recap
- A **business case** compares options (including doing nothing) with ranges and names the deciding assumptions; its effort matches the **size of the decision**.
- **Cost of delay** is the value lost per week of waiting; order work by **CD3** and schedule deadline work to its date.
- Use **ranges and the outside view**; IT work has a fat tail of overruns, so stage large investments.
- **Fund products as teams** with **guardrails**, new bets in **stages**, and only truly temporary work as **projects**.
- Bring **questions** to finance, and **re-read** every case against what happened.

## ✍️ Check yourself
**1. Reem's card freeze feature takes three weeks to build but waited a full quarter for a funding decision. What change addresses the cause?**

- A. Ask Reem's team to build faster, so that the funding wait matters less in the total time.
- B. Require a longer business case, so that the investment committee can approve it sooner.
- C. Move the feature to a separate project with its own budget, manager and steering group.
- D. Fund the product as a team within guardrails, so small items need no committee decision.

<details><summary>Answer</summary>

**D.** The wait was in funding; guardrails let the product manager decide small items. A targets the wrong step, B adds effort, and C adds overhead to a three-week change. See "Size the case to the decision".

</details>

**2. Two items compete for one team. Item X has a cost of delay of 40 a week and takes 8 weeks. Item Y has 15 a week and takes 2 weeks. Which goes first by CD3, and why?**

- A. X, because its cost of delay per week is the larger of the two and that alone decides.
- B. Y, because its cost of delay divided by its duration is the higher of the two items.
- C. X, because longer items should start first so that they are not left until the end.
- D. Y, because shorter items should always go first whatever their cost of delay may be.

<details><summary>Answer</summary>

**B.** CD3 is 40/8 = 5.0 for X and 15/2 = 7.5 for Y. A ignores duration, C has no basis, and D ignores cost of delay. See "Ordering work by CD3".

</details>

**3. A card-scheme rule must be met by a fixed date in twelve weeks; the work takes four weeks. How should Reem schedule it?**

- A. Rank it by CD3 with everything else, since all items should be compared by one rule.
- B. Put it first in the queue, since anything with a regulatory deadline must start at once.
- C. Schedule it to start early enough to finish by the date, and state what it delays.
- D. Leave it until the last four weeks, since starting earlier gains nothing for the bank.

<details><summary>Answer</summary>

**C.** Deadline work is scheduled to its date, with a margin, and its effect on other work is shown. A misapplies CD3, B wastes the slack, and D leaves no margin. See "Shapes of urgency".

</details>

**4. The sponsor of a large new platform presents a single estimate: "4.2 million, nine months". What should Tariq ask for first?**

- A. A low, likely and high range, and a comparison with what similar past work cost and took.
- B. A second estimate from the same team, to confirm the first figure is correct to the unit.
- C. A longer list of benefits, so that the case stays positive even if costs turn out higher.
- D. Approval of the full amount now, so the team does not lose time during later reviews.

<details><summary>Answer</summary>

**A.** Ranges and the outside view (reference class forecasting) counter optimism bias. B repeats the inside view, C inflates the case, and D removes the chance to stop early. See "Estimates as ranges, and the outside view".

</details>

**5. Finance worries that funding Cards & Payments as a team for a year is a blank cheque. Which addition best answers the concern?**

- A. A promise from Reem that the team will spend responsibly and deliver as much value as it can.
- B. A monthly report of story points delivered, compared against the team's planned total.
- C. A set of outcome measures, a spending envelope, a run-cost ceiling and a size threshold.
- D. A decision to keep project funding until the product has proven itself for several years.

<details><summary>Answer</summary>

**C.** These checkable guardrails tell finance when the product manager must come back for a decision. A is a principle, not a rule; B measures activity, not outcomes or spend; D never lets the product prove itself. See "Guardrails make product funding safe".

</details>

## 📚 References
- Reinertsen, D. G., *The Principles of Product Development Flow* (Celeritas, 2009). Cost of delay, as reported in summaries; book not opened.
- Black Swan Farming (Joshua Arnold), "Cost of Delay Divided by Duration" (CD3 and its relation to weighted shortest job first, as reported in search summaries; not opened): https://blackswanfarming.com/cost-of-delay-divided-by-duration/
- Flyvbjerg, B., "From Nobel Prize to Project Management: Getting Risks Right", *Project Management Journal* 37(3): 5–15 (2006) (as reported in search summaries; not opened): https://doi.org/10.1177/875697280603700302
- Flyvbjerg, B. and Budzier, A., "Why Your IT Project May Be Riskier Than You Think", *Harvard Business Review* 89(9), September 2011 (page range differs between sources). Figures reported; they match the SSRN abstract: https://papers.ssrn.com/abstract=2229735. Author preprint: arXiv:1304.0265, https://arxiv.org/abs/1304.0265
- Library course: [*AI Governance: Zero to Hero*, lesson 8.1 — Use-case intake, business case and risk tiering](../aigp/index.html#/8.1).
- Library course: [*AI Product Management*, lesson 9.2 — Roadmaps under uncertainty: bets, platforms and model change](../aipm/index.html#/9.2).

---

# 3.3 — Portfolio governance: reviewing, re-planning and stopping work
*Level: 🟡 Intermediate* · *Prerequisites: 3.1, 3.2* · *Step: Plan, Fund*

**After this you can** design a quarterly portfolio review with a fixed evidence pack, write a stop rule for every investment before it is funded, apply continue, change course, scale or stop decisions to a real list of investments, and keep a decision log that shows what was stopped and where the freed capacity went. *Study time: reading about 15 min, hands-on about 105 min (estimate).*

## ⚡ In 60 seconds
- **Portfolio governance** reviews investments together, on a steady cadence, and decides what to continue, change, grow or stop. Its output is decisions, not status reports.
- Each review uses the same **evidence pack** for every investment: outcomes, spend, flow, run cost, incidents, risks and assumptions.
- Four decisions: **continue**, **change course**, **scale up**, **stop**. Obligations are re-planned, not stopped.
- The rule that matters most: **every investment carries its own stop rule, written before the money is spent.**
- Decision cue: if your portfolio has stopped nothing in a year, it is being accumulated, not governed.
- Biggest trap: "we have spent too much to stop now". Spent money is gone; the only question is whether the *next* spend is worth it.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

Najm Bank's loan origination replacement started three years ago with an eighteen-month plan. It has reported "amber" for seven quarters, costs about 1.8 times the original business case, and its first release has slipped three times; the old loan system still runs. When Omar, the CIO, asked whether to stop it, the sponsor replied that the bank had spent too much to walk away, and the team was "nearly there".

It was not alone. Huda and Tariq's one-pager (lesson 3.1) showed twelve investments older than two years with no measure of what they had achieved, and Yousef's teams supported six systems that closed projects were meant to have retired. Nobody had decided to keep these going or to stop them.

The portfolio had a front door for money (lesson 3.2) but no exit. This lesson builds one: regular review of evidence, allowed decisions, stop rules written in advance, and a decision log.

## 📐 How it works

### 🟢 The essentials

**What portfolio governance is.** **Portfolio governance** is the meetings, rules, evidence and decision rights through which an organisation reviews its investments together and changes them. **Project governance** asks whether one project is on plan. Portfolio governance asks: given what we now know, is this still the best use of this money and these teams?

**The portfolio board.** The **portfolio board** makes those decisions for an area. Najm Bank's first board covers the retail and SME area: Omar chairs it, with the retail and SME business heads, Huda, Tariq and Yousef. Nour observes, so the **second line** (the risk and compliance functions that set and check risk rules) sees decisions as they are made. Its written decision rights (lesson 2.2): the mix across themes, initiatives above product guardrails, and continue, change, scale or stop. It does not reorder product backlogs; product managers do that within their guardrails (lesson 3.2).

**Cadence and triggers.** Reviews happen on a fixed **cadence**, usually quarterly, so priorities stay stable between them. A short list of **triggers** brings an item early: a guardrail breached, a stop rule met, a major incident with a structural cause, a regulatory change. Everything else waits.

**The evidence pack.** Every investment comes with the same page:

| Evidence | Question it answers | Where it comes from |
|---|---|---|
| Outcome measures against expected | Is it changing what it was funded to change? | Product analytics, business data |
| Spend against envelope and forecast | Is the money going where we agreed? | Finance system, investment record |
| Flow: lead time and work in progress | Is work moving, or piling up? | Delivery tool (lessons 1.2, 1.3) |
| Run cost and incidents | What does it cost to keep, and how reliable is it? | Cost model, incident records (lesson 9.3) |
| Risks and obligations | What could hurt us, and what must be done by when? | Risk register, obligation list |
| Key assumptions | Are the assumptions that would change the answer holding? | Business case (lesson 3.2) |

The same page makes investments comparable. Produce it from records, not for the meeting.

**Four decisions.** For each investment the board makes one, and writes down why:

| Decision | When | What happens next |
|---|---|---|
| **Continue** | Evidence is on track or improving | Nothing changes; next review as normal |
| **Change course** | The goal still matters, but the approach is not working | New approach, scope or team, with a new stop rule and an early review |
| **Scale up** | Evidence is strong and more capacity would speed results | More teams or money, taken from somewhere named |
| **Stop** | The stop rule is met, or the goal no longer matters | Stop new work, close down well, move people and money, record it |

The board cannot stop an obligation, but it can change how the bank meets it: scope, approach, supplier or timing within the deadline.

### 🟡 Going deeper

**Write the stop rule at the start.** A **stop rule** (often called a kill criterion) is a sentence written at funding that names a measure, a threshold and a date: "If fewer than 30% of new SME accounts are opened digitally two quarters after launch, we reconsider the approach." The team knows the test, the sponsor has agreed it, and nobody argues about what failure means after the money is spent.

**Why stopping is hard.** The **sunk cost effect** is the tendency to keep investing because of what has been spent; Hal Arkes and Catherine Blumer's 1985 paper "The psychology of sunk cost" reported, for example, that theatre-goers who paid full price for season tickets attended more performances in the first half of the season than those given a discount (as reported in search summaries). **Escalation of commitment** is the tendency to put more into a failing course, especially by those who chose it; Barry Staw's 1976 paper "Knee-deep in the big muddy" is credited with the idea (as reported in search summaries). The defences: stop rules written in advance, evidence from records, and a question only about the *next* spend.

**Limit what runs at once.** Too many active investments split specialists and make everything wait. Lesson 1.2 showed that lead time grows with work in progress when **throughput** (items finished per week) stays the same; the same holds for a portfolio. Set a **limit on active initiatives** per area, based on teams available, and start new work only when something finishes or stops. For the retail and SME area, Huda proposed cutting about 50 active projects to at most 10 active initiatives plus the funded products (illustrative); most small projects were folded into product backlogs.

**Stopping well.** Stopping is work with a checklist: **users** (what will they do instead?), **data** (what must be kept, and for how long? ask the data protection and records functions), **contracts** (notice and exit terms; ask Lina, the Vendor and Sourcing Manager), **components** (switched off and removed from the configuration records), **regulation** (does it affect a critical service or a known outsourcing arrangement? ask Nour whether notification is needed), **people** (where they go, what knowledge to write down) and **learning** (which assumptions were wrong).

**The decision log.** A **decision log** records each decision: date, investment, decision, evidence, dissent, stop rule, and where freed money and teams went. It shows auditors that decisions were deliberate, and gives a health measure: investments stopped or changed each year.

### 🔴 Expert view

**Status colours are not evidence.** Red, amber and green ratings set by the project manager can show green while users ignore what is delivered, a "watermelon" report (green outside, red inside; lesson 1.3). Require that every colour points to a measure, or drop colours.

**Stable priorities, deliberate change.** Google Cloud's announcement of the 2024 DORA report says that instability in priorities "can significantly hinder progress", even with strong leadership and good documentation. A quarterly cadence with a few triggers lets the board change the portfolio on purpose and protects teams between reviews.

**Separate the evidence from the advocate.** The sponsor is the worst-placed person to judge whether their investment should stop. The portfolio office (lesson 3.2) prepares the evidence from records, and the largest investments get an independent review before more money is released.

**Governance and assurance in a bank.** The portfolio board is a first-line management body; Nour's seat does not make it a risk committee. Ask the risk function which decisions they must be told about (lesson 10.3). For killing ideas before they become investments, see [*AI Product Management*, lesson 2.3 — When not to use AI, and killing ideas early](../aipm/index.html#/2.3); for the same habit at the scale of a small business, see [*Founder's Playbook for AI-First Builders*, lesson 2.1 — One job, one customer: scope and the kill list](../founder/index.html#/2.1).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Portfolio board charter** | Members, decision rights, cadence, triggers, and what the board does not decide | Before the first review |
| **Evidence pack** | One page per investment, the same for all, produced from records | Each quarterly review |
| **Stop rule line** | Measure, threshold and date that would end the investment | At funding and at each change of course |
| **Active initiative limit** | Maximum initiatives running at once per area, set from team numbers | When specialists are split across too many items |
| **Stopping checklist** | Users, data, contracts, components, regulation, people, learning | Every stop or replacement |
| **Decision log** | Date, investment, decision, evidence, dissent, stop rule, where capacity went | Every board decision |

## 🏛️ In practice at Najm Bank
After the first quarterly review under the new model, Tariq's portfolio office published the decision log. Illustrative and fictional:

> **Retail and SME portfolio board: decision log, first quarter (extract; area figures)**
>
> | Investment | Decision | Evidence | Stop rule from now | Capacity |
> |---|---|---|---|---|
> | Loan origination replacement | **Change course**: stop the custom build; ten-week comparison of a packaged system against extending the current one | 1.8 times original cost; three slips; two key assumptions (data migration, supplier staffing) failed | No costed option in ten weeks: stop and keep the current system with a support plan | Two of four teams to SME onboarding |
> | Cards & Payments | **Continue** | Routine card calls down from about 1.1 to 0.9 per customer a year; run cost within guardrail | Unchanged | No change |
> | SME digital onboarding | **Scale up** | Digital share of new SME accounts up from 10% to 18% in a pilot region | Below 30% two quarters after full launch: reconsider | Two teams added |
> | Branch queue system | **Stop** | No theme; pilot adoption below its threshold, so the stop rule was met | — | Supplier notice; checklist owner Lina |
> | Core banking end-of-support upgrade | **Re-plan** (obligation) | On track, but testing capacity short | Deadline fixed | Platform team provides test environments |
>
> **Dissent recorded:** the loan origination sponsor asked that completing the current build be compared too; the board agreed.
>
> **Active initiatives in the area:** 21, down from about 50 projects (most folded into product backlogs). Target: 10 by year end.

Omar's first instinct was to stop loan origination outright; Huda pointed out that no alternative was costed. Tariq's first evidence pack was written by the sponsors, and three items arrived green with no measures; the second was produced from records. Nour had the branch queue stop checked against the outsourcing register before notice went out.

## 🛠️ Exercises
**🟢 Write stop rules.** For five investments (yours or Najm Bank's), write a stop rule with a measure, a threshold and a date.
*Done when:* each rule's measure can be collected from records, each has a threshold and a date within twelve months, and none says only "if it is not delivering value".

<details><summary>Model answer and self-check</summary>

**Model answer.** For Najm Bank: payments resilience, "if critical payment disruption is not below six hours a quarter by the end of the third quarter, return with options"; branch queue pilot, "if fewer than half of pilot branches use it daily after three months, stop". Obligations get a date-and-scope rule instead.

**Self-check.**
- Could someone not in the room tell whether the rule has been met?
- Is the measure an outcome or reliability measure, not a delivery milestone only?
- Did you agree the rule with the sponsor, or would they dispute it later?

</details>

**🟡 Run a mock portfolio review.** Prepare an evidence pack for five investments from real records where you can. With two colleagues as board members, make one of the four decisions for each and fill in the decision log.
*Done when:* each pack covers all six evidence rows (or says "no record"); every decision has evidence, dissent if any, and a stop rule; and at least one decision is not "continue".

<details><summary>Model answer and self-check</summary>

**Model answer.** A first mock review usually finds most packs lack outcome data, so the commonest decision is "continue, with a measure in place by next review". Usually one item meets its stop rule, and one strong product is a candidate to scale. The log shows which evidence was missing.

**Self-check.**
- Were the packs produced from records, or written by the sponsors?
- For any "scale up", did you name where the capacity comes from?
- For any "stop", did you start the stopping checklist?

</details>

**🔴 Design the governance and set an initiative limit.** Write a one-page board charter for one area (members, decision rights, cadence, triggers, evidence pack, what the board does not decide). Set an active initiative limit from team numbers, and say which current initiatives fold into backlogs, finish or stop.
*Done when:* each trigger is a checkable event, the limit is justified by team numbers, every current initiative is accounted for, and the charter names which decisions the risk function must see (agreed with them, or as an open question).

<details><summary>Model answer and self-check</summary>

**Model answer.** Najm Bank's charter follows "The portfolio board" and "Cadence and triggers"; the board does not approve individual changes. Limit (illustrative): the area has 24 teams; 14 are funded as product or platform teams, leaving 10 for initiatives. At most one active initiative per available team gives 10. Of the area's 52 projects, 30 fold into product backlogs this quarter; of the rest, 8 finish and 4 stop by year end, leaving 10. Open question to Nour: which stops and supplier exits need second-line review before notice.

**Self-check.**
- Does the charter say what the board does *not* decide?
- Is the limit based on capacity, not a round number?
- Did you leave the regulatory judgement to the risk function?

</details>

## ⚠️ Mistakes and traps
- **Reviews that only report.** Every item ends with a decision and the reason.
- **Stop rules written after the fact.** Defining failure once the money is spent invites sunk-cost argument. Write the rule at funding.
- **Sponsor-written evidence.** Produce packs from records; review the largest items independently.
- **Stopping without a plan.** Abrupt stops orphan users, data and contracts. Use the checklist.
- **Re-planning on request.** Use a fixed cadence and a short list of triggers.

## 🧾 Recap
- **Portfolio governance** reviews investments together on a **cadence**, with **triggers**, and produces **decisions** from the same **evidence pack**, produced from records.
- Four decisions: **continue, change course, scale up, stop**; obligations are re-planned.
- **Write the stop rule at funding**; it counters sunk cost and escalation of commitment.
- **Limit active initiatives**, **stop well**, and keep a **decision log**; agree with the risk function which decisions it must see.

## ✍️ Check yourself
**1. The loan origination sponsor argues that the bank has already spent too much to stop. What question should the board ask instead?**

- A. How much more must be spent to recover the money already invested in the work?
- B. Whether the next spend is worth it, given what we now know and the alternatives.
- C. Whether the sponsor still has confidence that the team is nearly finished with it.
- D. How the money already spent can be shown as an asset so that stopping costs less.

<details><summary>Answer</summary>

**B.** Money already spent is gone whatever the board decides. A and D are sunk-cost reasoning, and C relies on the person most exposed to escalation of commitment. See "Why stopping is hard".

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
- C. A shorter review date, with no change to where the extra capacity comes from.
- D. The total spent on onboarding so far, so the scale-up can be judged against it.

<details><summary>Answer</summary>

**A.** Scaling up is a reallocation, so the log records where capacity comes from. B ignores the tiering in lesson 3.2, C leaves the capacity question open, and D looks back at sunk cost. See "Four decisions".

</details>

**4. Tariq's first evidence pack is a set of status reports written by each sponsor, and three items arrive green with no measures. What should change?**

- A. Ask the sponsors to add more detail and commentary to explain each of their colours.
- B. Drop the evidence pack and let each sponsor present their investment in person instead.
- C. Produce the pack from records, with the same page of measures for every investment.
- D. Accept green items without discussion, so the board can spend its time on red items.

<details><summary>Answer</summary>

**C.** A common page produced from records makes investments comparable and separates the evidence from the advocate. A and B keep the sponsor in control of the evidence, and D trusts colours. See "The evidence pack" and "Status colours are not evidence".

</details>

**5. Between quarterly reviews, the head of retail banking asks Omar to switch two teams to a new retail project at once. No trigger has been met. What should Omar do?**

- A. Agree, because the retail project is new and early work is cheapest to start now.
- B. Bring it to the next quarterly review, unless it meets one of the agreed triggers.
- C. Call an extra board meeting this week, so that the request can be decided quickly.
- D. Ask the two teams to split their time between both pieces of work until the review.

<details><summary>Answer</summary>

**B.** A fixed cadence with defined triggers keeps priorities stable. A re-plans for a reason that is not a trigger, C turns a senior request into an extra meeting, and D splits teams and raises work in progress. See "Cadence and triggers".

</details>

## 📚 References
- Google Cloud blog, "Announcing the 2024 DORA report", 22 October 2024 (opened 2026-11-20; source of the quoted finding on unstable priorities): https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
- Arkes, H. R. and Blumer, C., "The psychology of sunk cost", *Organizational Behavior and Human Decision Processes* 35(1): 124–140 (1985). Citation and the season-ticket finding as reported in search summaries; paper not opened.
- Staw, B. M., "Knee-deep in the big muddy: A study of escalating commitment to a chosen course of action", *Organizational Behavior and Human Performance* 16: 27–44 (1976). Citation as reported in search summaries; paper not opened.
- Library course: [*AI Product Management*, lesson 2.3 — When not to use AI, and killing ideas early](../aipm/index.html#/2.3).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 2.1 — One job, one customer: scope and the kill list](../founder/index.html#/2.1).
