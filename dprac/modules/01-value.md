# Module 1 — Digital value and the customer

*Before anyone writes a line of code, three questions decide whether the work will be worth it: what makes this product digital, and how could it create value; who is the customer, and what evidence says they have the problem; and how will the business pay for each unit of value it delivers? This module answers them at Qafila's Launch stage, when Maha and Faisal are building the first version for 15 pilot shops and still coordinate most deliveries by hand. Each lesson leaves you with an artefact you can use in any job: a value sheet for one customer group, a problem statement with an evidence log, and a one-page unit-economics sheet.*

> **Steps:** Discover — find out who the product is for, what change it makes in their day, what evidence supports that, and whether the business can afford to deliver it.

---

# 1.1 — What makes a product digital, and how it creates value
*Level: 🟢 Beginner* · *Prerequisites: 0.1, 0.2* · *Step: Discover*

**After this you can** describe one digital product in terms of who it serves, what it changes in their day and how that change becomes value for the customer and for the business, and write a one-page value sheet for one customer group with a measure you could check. *Study time: reading about 20 min, hands-on about 80 min (estimate).*

## ⚡ In 60 seconds
- A **digital product** is used through software (an app, a website, an interface other software calls): built once, copied cheaply, changed often, run every day.
- It creates **value** only when someone does something differently because of it. Features are the means, not the value.
- Most digital products serve several groups. Qafila serves shop owners and couriers, and each needs its own reason to use it.
- The rule that matters most: **value is counted in the customer's day, not in your feature list.**
- Decision cue: before building anything, ask "what will this person do differently next week, and how would we see it?"
- Biggest trap: confusing "people liked the demo" with "people changed how they work".

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

It is Launch. Maha and Faisal have a first version running on one cloud provider's managed services: a merchant app where a shop logs a delivery, a courier app that shows the next pickup, and an admin web page where Maha watches everything. Fifteen pilot shops use it, for about 150 deliveries a day. Faisal deploys by hand once a week.

Faisal's plan for next month: a loyalty-points screen, a dark mode and a charts dashboard for shop owners. "The pilot shops love the app," he says. "Let's give them more."

Maha has spent the afternoon in a bakery. The owner typed a phone order into Qafila, then phoned a courier anyway "to make sure he saw it". A courier arrived, found the order not ready, and left. Nobody looked at a chart. The owner's real question was "will my order reach my customer on time without me chasing anyone?" Before they spend a month, Maha and Faisal need a plain, shared description of what value Qafila creates, and for whom.

## 📐 How it works

### 🟢 The essentials

**What makes a product digital.** A **product** is something offered to a group of people to meet a need, again and again, by the same organisation. It is **digital** when people use it mainly through software. Four properties set digital products apart from, say, a delivery van or a printed timetable:

| Property | Plain meaning | At Qafila |
|---|---|---|
| **Cheap to copy, not free to run** | The first version is expensive to build; serving one more user costs little, but never nothing | Adding a sixteenth shop needs no new code, but it adds messages, storage, support calls |
| **Changes all the time** | The product is never "finished"; it is updated weekly, daily or more often | Faisal ships a new version every week |
| **Produces data as it is used** | Every action leaves a record that can show what people actually do | Each delivery has a created time, a pickup time and a drop-off time |
| **Connects people and systems** | It often sits between groups, or between other software | It links shops, couriers and, later, a payment provider |

The economist Hal Varian described information as "costly to produce but cheap to reproduce" in a 1998 paper (as reported in summaries of it). That is why lesson 1.3 looks so carefully at the costs that *do* grow with use.

**Product, service, project.** A **product** is the thing offered (the Qafila app). A **service** is the ongoing promise around it: it works, and someone answers when it does not (Module 7). A **project** is temporary work, such as "build the courier app". Value comes from use over time, not from a project finishing. For the manager's view of the difference, see [*Running IT as a Business*, lesson 2.1 — Digital products, services and projects: what each is and who owns it](../itbiz/index.html#/2.1).

**What value means.** **Value** is the benefit someone gets, judged by them, minus what it costs them (money, time, effort, risk). Two sides:

- **Customer value:** saving time or money, earning more, avoiding mistakes, feeling in control.
- **Business value:** what the organisation gains when customers get theirs: revenue, lower cost, lower risk, or learning.

Business value follows customer value: if shop owners gain nothing, they stop using the app.

**From feature to value.** A useful chain, read left to right:

```mermaid
flowchart LR
  F[Feature: courier sees order is ready] --> B[Behaviour: courier arrives when the order is ready]
  B --> C[Customer value: shop stops phoning couriers; fewer late drop-offs]
  C --> V[Business value: shops keep paying; Qafila needs fewer support calls]
```

People skip the middle box. A feature that changes nobody's behaviour creates no value.

### 🟡 Going deeper

**More than one customer.** Many digital products have two or more groups who must each find a reason to take part. Qafila has at least four:

| Group | What they want from Qafila | What would make them leave |
|---|---|---|
| **Shop owners** | Orders reach their customers on time without chasing | More work than a phone call; late or lost orders |
| **Couriers** | Steady work, short waits, clear pickup details | Waiting at shops; unclear addresses; late pay |
| **Shop customers** | Their order arrives when promised | Late deliveries; no idea where the order is |

Shop customers never open the app, yet their experience decides whether the shop stays. List the people who feel a product's effects, not only those who log in.

**A value proposition in one sentence.** A **value proposition** states who the product is for, what problem it solves, and why it beats what they do today:

> For **[group]** who **[situation or problem]**, **[product]** helps them **[change in their day]**, unlike **[today's alternative]**, which **[its weakness]**.

For Qafila's shop owners: "For small shops that deliver to local customers, Qafila helps them get each order to the customer on time without phoning anyone, unlike chat groups and phone calls to couriers, which need constant chasing and lose orders at busy times."

Every customer already has an alternative, even a notebook and a phone. Value is measured against it, not against nothing.

**The four risks of a new product.** Marty Cagan, a product management author at Silicon Valley Product Group, names four risks every new product or feature carries (as reported in summaries of his work; the second edition of his book *Inspired*, 2018, lists all four):

| Risk | The question | Qafila example |
|---|---|---|
| **Value** | Will people choose to use it? | Will bakeries log orders in the app rather than phoning couriers? |
| **Usability** | Can they work out how to use it? | Can a busy shop assistant log an order in under a minute? |
| **Feasibility** | Can we build and run it with what we have? | Can two people support courier tracking on old phones? |
| **Viability** | Does it work for the business: costs, law, partners, reputation? | Will each delivery earn more than it costs to coordinate? |

### 🔴 Expert view

**Value is a guess until behaviour shows it.** Every early value statement is a hypothesis. Praise is weak evidence; repeated behaviour is strong (lesson 1.2). Track a **leading signal** weekly (shops log every order in the app) so you can change course before the **lagging signal** (shops still paying after three months) arrives.

**Hidden manual work.** Early products often hide human effort behind the screen: Maha phones couriers when an assignment looks wrong. That is often wise; Paul Graham's essay "Do Things that Don't Scale" (July 2013) argues founders should do manual work early to learn and win first users. But write the steps down: they are part of what customers buy, they cost money, and they hide how far the software is from delivering value alone.

**The memorable rule.** Value is counted in the customer's day, not in your feature list.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Value sheet** | One page per customer group: who, today's alternative, the change in their day, a measure, the evidence so far | Before planning a new product or a big feature |
| **Value proposition sentence** | "For [group] who [problem], [product] helps them [change], unlike [alternative], which [weakness]" | When people describe the product in different ways |
| **Feature-to-value chain** | Feature, behaviour change, customer value, business value, written in four boxes | When a plan lists features with no "so that" |
| **Four-risks check** | Value, usability, feasibility, viability, one line each with the open question | Before committing weeks of build time |

## 🏛️ In practice at Qafila
Maha and Faisal rewrite the plan as a value sheet for shop owners. Illustrative and fictional.

> **Qafila value sheet: shop owners (Launch, draft 1)**
>
> | Field | Entry |
> |---|---|
> | Group | Owners and staff of small shops in the pilot (15 shops: bakeries, a pharmacy, grocers) |
> | Today's alternative | Phone or chat message to a courier they know; owner chases if late |
> | Value proposition | For small shops that deliver locally, Qafila gets each order to the customer on time without anyone phoning, unlike chat and calls, which need chasing and lose orders at busy times |
> | Change in their day | Shop logs the order once and does not phone the courier |
> | Leading measure | Share of pilot orders with no shop-to-courier phone call (asked in a weekly check-in; baseline unknown) |
> | Lagging measure | Pilot shops still using Qafila after the free period ends |
> | Evidence so far | One afternoon's observation at one bakery: owner phoned the courier after logging the order, on 4 of the 6 orders seen |
> | Four risks | Value: unproven. Usability: logging takes about 2 minutes, too long at rush hour. Feasibility: fine at 150 deliveries a day. Viability: unknown, see lesson 1.3 |
> | Manual work | Maha re-checks courier assignments each morning and phones when one looks wrong (about 45 min a day) |
>
> **Decision:** drop loyalty points and dark mode for now. Next month: an "order ready" button for shops and a pickup alert for couriers, aimed at the phone call.

Faisal objected that couriers had asked for dark mode; Maha logged it as a request, with who asked and why, to revisit later. She also kept "baseline unknown": an honest gap beats a made-up number.

## 🛠️ Exercises
**🟢 Describe a digital product you use.** Pick one app or website you use every week (a ride, food, banking, learning or messaging app). Write down: who it serves (all groups, not only you), what you did before it existed, what it changed in your day, and one way the company could see that change in its data.
*Done when:* you list at least two groups, name a real alternative, and describe a change in behaviour rather than a feature.

<details><summary>Model answer and self-check</summary>

**Model answer.** A food-ordering app serves diners, restaurants and riders. Before it, I phoned restaurants and waited without knowing when food would arrive. Now I stop phoning to ask where the food is. The company could see that as fewer "where is my order" contacts per order, and as repeat orders.

**Self-check.**
- Is your "change" something a person does, not something the app has?

</details>

**🟡 Write a value sheet for Qafila's couriers.** Using the facts in this lesson, write a one-page value sheet for couriers with the same fields as the shop-owner sheet: group, today's alternative, value proposition sentence, change in their day, leading and lagging measure, evidence so far, four risks, manual work.
*Done when:* every field is filled, any number you do not have is written as "unknown", and the value proposition sentence follows the template.

<details><summary>Model answer and self-check</summary>

**Model answer.** Group: couriers with pilot shops. Alternative: calls and chats from several shops; arriving early and waiting. Proposition: "For couriers who take orders from several small shops, Qafila shows which order is ready and where to go next, unlike calls and chats, which leave them waiting at counters." Change: less waiting, more deliveries per shift. Leading measure: average wait at pickup. Lagging: couriers still active after two months. Evidence: one courier seen leaving the bakery without the order. Risks: value plausible, usability unknown on old phones, feasibility fine, viability depends on courier pay. Manual work: Maha's morning check.

**Self-check.**
- Did you avoid inventing numbers that the lesson does not give?
- Is your leading measure something Qafila's own records could produce?
- Does your sheet show that couriers want something different from shop owners?

</details>

**🔴 Turn a feature list into value chains.** Take Faisal's original plan (loyalty points, dark mode, charts dashboard) plus Maha's proposal (an "order ready" button). For each of the four, write the feature-to-value chain (feature, behaviour change, customer value, business value) and the four-risks line. Then rank them and explain the ranking in three sentences.
*Done when:* each chain has a specific behaviour change, at least one chain is marked "no clear behaviour change", and the ranking is justified by evidence or by the size of the risk, not by taste.

<details><summary>Model answer and self-check</summary>

**Model answer.** "Order ready" button: couriers arrive when the order is ready; shops stop phoning; fewer late drop-offs; shops stay. Value plausible, with bakery evidence. Dashboard: no clear behaviour change; no owner has asked; value risk high. Loyalty points: shop customers might order more, but Qafila does not serve them directly; viability unknown. Dark mode: easier night use for couriers; a usability gain unrelated to the main pain. Ranking: button first (observed pain), dark mode second if couriers confirm it is cheap and wanted, the rest later until there is evidence of behaviour change.

**Self-check.**
- Did you rank by evidence of behaviour change, not by interest?
- Did you name which group each feature serves?

</details>

## ⚠️ Mistakes and traps
- **Listing features as value.** "Has a dashboard" is not a benefit. Ask "so that who does what differently?"
- **Forgetting the alternative.** Customers compare you with what they do today, often a phone call. Write the alternative down and check you beat it.
- **Serving only the user who logs in.** Shop customers and couriers decide whether shops stay. List every group the product affects.

## 🧾 Recap
- A digital product is used through software, costly to build, cheap to copy but not free to run, always changing and full of usage data.
- Value is the benefit a person gets, judged by them, minus their cost to get it; business value follows customer value.
- A feature creates value only through a change in behaviour; write the full chain.
- Products often serve several groups; each compares you with today's alternative.
- Check four risks (value, usability, feasibility, viability) before committing build time.
- Rule: value is counted in the customer's day, not in your feature list.

## ✍️ Check yourself
**1. Faisal says the pilot shops "love the app", so the next step is to add more features. What is the main weakness in his reasoning?**

- A. Pilot shops are too few to give any useful information about the product yet.
- B. Praise is weak evidence; he has not shown that shops changed their habits.
- C. Adding features is always wrong until the product has paying customers.
- D. Shop owners are not the right group to judge whether a product is useful.

<details><summary>Answer</summary>

**B.** Polite praise does not show a change in behaviour; Maha's visit showed the shop still phoning couriers. A is too strong (15 shops can show a lot), C is a blanket rule the lesson does not make, and D is wrong because shop owners are a key group. See "Value is a guess until behaviour shows it".

</details>

**2. Which statement best describes the cost of serving one more shop with Qafila's digital product?**

- A. Zero, because the software is already built and copying it costs nothing.
- B. The same as the first shop, because each shop needs its own copy built.
- C. Unknown, because digital products have no costs that grow with usage at all.
- D. Small but real: more messages, storage and support, though no new code to write.

<details><summary>Answer</summary>

**D.** Digital products are cheap to copy but not free to run. A is the common trap of treating "cheap to copy" as "free", B describes a custom build, and C is false: some costs grow with use (lesson 1.3). See "What makes a product digital".

</details>

**3. Which of these is a value proposition sentence in the form the lesson recommends?**

- A. For small local shops, Qafila gets orders out on time without calls, unlike chats that need chasing.
- B. Qafila is a modern delivery-coordination platform with apps for merchants, couriers and admins.
- C. Qafila will reach 300 merchants and grow its daily deliveries fast by adding loyalty points and dashboards.
- D. Our vision is to make every small business in the region as efficient as the largest delivery companies.

<details><summary>Answer</summary>

**A.** It names the group, the change in their day and the alternative with its weakness. B describes the product's parts, C states business targets and features, and D is a vision statement with no customer change in it. See "A value proposition in one sentence".

</details>

**4. Maha wonders whether each delivery will earn more than it costs to coordinate. Which of the four risks is she thinking about?**

- A. Value risk, because it is about whether shops will choose to use the app.
- B. Usability risk, because it is about how much effort each delivery takes.
- C. Viability risk, as it concerns whether the business model works.
- D. Feasibility risk, because it is about what the team is able to build.

<details><summary>Answer</summary>

**C.** Whether the business can afford to deliver each unit is viability. A is the tempting one, but value risk is about whether customers choose the product, not whether it pays. B and D are about ease of use and ability to build. See "The four risks of a new product".

</details>

**5. Maha re-checks courier assignments by hand every morning. What should Qafila do about this at Launch?**

- A. Stop at once, because manual work means the product is not really digital.
- B. Keep doing it if it helps, but write it down with the time it takes daily.
- C. Hide it from shops, so they judge the software on its own merits alone.
- D. Automate it before adding any more shops, whatever the cost of doing so.

<details><summary>Answer</summary>

**B.** Early manual work is often wise, but it must be visible because it is part of what customers receive and of what it costs. A and D overreact, and C hides the real cost and quality of the service. See "Hidden manual work".

</details>

## 📚 References
- Varian, H. R., "Markets for Information Goods", 1998 paper, University of California, Berkeley: https://people.ischool.berkeley.edu/~hal/Papers/japan/japan.html — source of "costly to produce but cheap to reproduce" (reported from search summaries; the page could not be opened from this environment).
- Shapiro, C. and Varian, H. R., *Information Rules: A Strategic Guide to the Network Economy* (Harvard Business School Press, 1999) (full citation; not opened).
- Cagan, M., "Product Risk Taxonomies", Silicon Valley Product Group: https://svpg.com/product-risk-taxonomies — the four risks of value, usability, feasibility and viability (reported from search summaries; not opened).
- Cagan, M., *Inspired: How to Create Tech Products Customers Love*, 2nd edition (Wiley, 2018) (full citation; not opened).
- Graham, P., "Do Things that Don't Scale", July 2013: https://paulgraham.com/ds.html (reported from search summaries; not opened).
- Library course: [*Running IT as a Business*, lesson 2.1 — Digital products, services and projects: what each is and who owns it](../itbiz/index.html#/2.1).
- Library course: [*Running IT as a Business*, lesson 1.1 — From projects to value: outcomes, value streams and flow](../itbiz/index.html#/1.1) (outcomes and value from a manager's view).

---

# 1.2 — Understanding customers: problems, jobs and evidence
*Level: 🟢 Beginner* · *Prerequisites: 1.1* · *Step: Discover*

**After this you can** write a problem statement for one customer group, run a short interview that asks about past behaviour rather than opinions, and keep an evidence log that grades each finding by how much it should be trusted. *Study time: reading about 20 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- A **problem statement** names who has the problem, in what situation, what it costs them, and how they cope today. It says nothing about the solution.
- A **job to be done** is the progress a person is trying to make in a situation ("get this order to my customer before it goes cold"), not the product they use to make it.
- Good customer conversations ask about **specific things that already happened**, not about what people think or would do. Do not pitch your idea while you listen.
- Evidence comes in grades: opinions are weakest, past behaviour is stronger, a commitment (time, money, data) is stronger still.
- The rule that matters most: **believe what people did, not what they say they will do.**
- Biggest trap: asking "would you use an app that…?" Almost everyone says yes, and it tells you almost nothing.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

Maha and Faisal agree that the shop-to-courier phone call is the pain to attack. Faisal sends the 15 pilot shops a survey: "Would you use an 'order ready' button if we built one?" Fourteen reply; thirteen say yes.

Maha is uneasy. The same shops said yes to the original app and still phone couriers, and the question tells shops which answer Qafila hopes for. A pharmacy owner in the pilot told her, "Of course I'd use it." He has logged three orders in two weeks.

The survey gave confidence, not evidence. They need to learn what happens in a shop at rush hour, and which beliefs are facts and which are hopes.

## 📐 How it works

### 🟢 The essentials

**Problem first, then solution.** New products most often fail by solving something nobody needed badly enough to change habits. So describe the problem first, in a **problem statement** with five parts:

1. **Who:** a specific group ("counter staff of small bakeries in the pilot"), not "businesses".
2. **Situation:** when it happens ("during the lunch rush").
3. **The problem:** what goes wrong, in their words if possible.
4. **What it costs them:** time, money, mistakes, stress, lost customers.
5. **How they cope today:** phone calls, a notebook, a relative who drives.

| Weak | Strong |
|---|---|
| "Shops need better delivery software." | "Counter staff at small bakeries, during the lunch rush, do not know whether a courier has seen an order, so they phone the courier for most orders. Each call takes a minute or two at the busiest time, and orders go cold when the courier arrives late." |

The strong version can be checked by watching a lunch rush, and it leaves room for solutions other than an app feature.

**Jobs to be done.** A **job to be done** is the progress a person is trying to make in a particular situation. The idea was set out by Clayton Christensen and colleagues in "Know Your Customers' Jobs to Be Done" in the *Harvard Business Review* (September 2016). The point is that people "hire" a product to make progress, and "fire" it when something else does the job better.

A bakery owner with a phone order and a queue at the counter does not want "delivery-coordination software"; the job is "get this order to the customer warm and on time, without leaving the counter". Qafila, a nephew with a motorbike, a courier the owner knows, or asking the customer to collect can all do that job. They are all competitors.

A job statement has three parts: **when** (the situation), **I want to** (the progress), **so I can** (the deeper reason).

> When a phone order comes in during the rush, I want it picked up as soon as it is ready, so I can keep serving the queue and the customer gets warm bread.

**Talking to customers.** The fastest way to understand a problem is to talk with the people who have it and, where you can, watch them. Rob Fitzpatrick's book *The Mom Test* (2013) is a widely used guide; its three rules, as reported in summaries, are:

- Talk about their life, not your idea.
- Ask about specifics in the past, not opinions or the future.
- Talk less and listen more.

| Bad question (invites opinion or politeness) | Better question (asks about what happened) |
|---|---|
| "Would you use an 'order ready' button?" | "Tell me about the last delivery that went wrong. What happened?" |
| "Is coordinating couriers a big problem for you?" | "How many times did you phone a courier yesterday? Why each time?" |
| "How much would you pay for this?" | "What do you spend on deliveries now, and who decides that?" |

### 🟡 Going deeper

**Grades of evidence.** From weakest to strongest:

| Grade | What it is | Qafila example | How much to trust it |
|---|---|---|---|
| 1. **Opinion or prediction** | What people say they think or would do | "I'd definitely use it" | Low: people are polite and bad at predicting themselves |
| 2. **Story about the past** | A specific account of what happened | "Yesterday I called the courier four times for one order" | Medium: real, but memory blurs |
| 3. **Observed behaviour** | What you saw them do, or what records show | Usage data: three orders logged in two weeks; you watched four calls in an afternoon | High for what was observed; check it is typical |
| 4. **Commitment** | They give up something: time, money, data, reputation | Shop agrees to a paid trial, or introduces Qafila to two other shops | Highest: costly signals are rarely given out of politeness |

Faisal's survey is grade 1; Maha's bakery afternoon is grade 3, however many survey answers there are.

**Running an interview.** A practical shape for 20–30 minutes:

1. **Set up.** Who you are, why you ask, how long it takes, what happens to the notes; ask permission to take notes.
2. **Context.** Their role, a typical day, where deliveries fit.
3. **The last time.** "Walk me through the last order you delivered." Follow with "what happened next?" and "why?".
4. **Workarounds and costs.** What they do today, what it costs, what they tried and dropped.
5. **Close.** "Who else should I talk to?" and, if fitting, a small commitment ("Could I watch one lunch rush?").

Write notes the same day in three columns: **said**, **did or showed you**, **what you think it means**.

**Observation.** Watching people work (shadowing) finds habits people do not mention: the bakery owner never spoke of the calls; she just made them. Watch when the problem happens, not at a quiet time.

**How many conversations?** No magic number. Stop when new conversations repeat what you heard, and cover different kinds of people (bakery and pharmacy, busy and quiet, owner and counter staff).

**Assumptions.** An **assumption** is something treated as true without enough evidence. Write each as a statement that could be wrong, mark its importance and evidence, and test the important, weakly supported ones first (lesson 2.1).

### 🔴 Expert view

**Bias in your own head.** **Confirmation bias** is noticing what supports what you already believe. Write your prediction down before a conversation and look for evidence that would prove you wrong. Pilot shops chose to join and are probably keener than average; ask a few shops that said no why.

**Research ethics and personal data.** Ask for consent, say what you keep and for how long, store notes safely, and drop names you do not need. Recording may need explicit permission, and data-protection rules in many countries cover notes about identifiable people. Ask someone who knows the rules where you operate: what may we collect, how must we store it, what have we told people?

**AI tools, carefully.** An assistant can draft a guide or cluster notes, but not replace customers; pasting personal notes into an outside tool is a data-protection question. See [*Founder's Playbook for AI-First Builders*, lesson 1.3 — AI-assisted research without fooling yourself](../founder/index.html#/1.3).

**The memorable rule.** Believe what people did, not what they say they will do.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Problem statement** | Who, situation, problem, cost to them, how they cope today; no solution | Before discussing any feature or product |
| **Job statement** | "When [situation], I want to [progress], so I can [deeper reason]" | To see the real competition, including non-software ones |
| **Interview guide** | Five parts: set up, context, the last time, workarounds and costs, close | Before each customer conversation |
| **Evidence log** | One row per finding: source, date, grade (opinion, story, observed, commitment), what it supports | After every conversation, observation or data pull |

## 🏛️ In practice at Qafila
Maha and Faisal agree on four interviews and two observations before building anything. Illustrative and fictional.

> **Problem statement (shops, draft 2).** Counter staff at small food shops in the pilot, during the lunch and evening rush, cannot tell whether a courier has seen an order or when they will arrive, so they phone the courier for most orders. Each call interrupts service at the busiest time, and orders wait or go cold when couriers arrive early or late. Today they cope with phone calls, chat messages, and a courier they know personally.
>
> **Job statement.** When a phone order comes in during the rush, I want it collected as soon as it is ready, so I can keep serving the queue and my customer gets the food warm.
>
> **Evidence log (extract)**
>
> | # | Finding | Source and date | Grade | Supports |
> |---|---|---|---|---|
> | 1 | 13 of 14 shops "would use" an order-ready button | Survey, week 6 | Opinion | Weakly: button wanted |
> | 2 | Owner phoned courier after logging the order on 4 of 6 orders | Maha, bakery observation, week 5 | Observed | Problem is real at this shop |
> | 3 | Pharmacy logged 3 orders in 2 weeks; owner says most deliveries are prescriptions he takes himself | App records + interview, week 7 | Observed + story | Pharmacy's job differs: privacy, not speed |
> | 4 | Grocer's counter assistant: "I call because the courier never knows when it's ready" | Interview, week 7 | Story | Problem is "ready" timing, not "courier saw it" |
> | 5 | Second bakery agreed to let Faisal watch two lunch rushes | Interview close, week 7 | Commitment | Shops willing to invest time |
>
> **What changed.** Finding 4 moved the problem from "has the courier seen it?" to "does the courier know when it will be ready?". Finding 3 suggests pharmacies have a different job; they are set aside, not forced into the bakery solution.

Faisal argued the survey had "more data". Maha pointed to the grade column: fourteen opinions are still opinions. The survey stays in the log, graded honestly.

## 🛠️ Exercises
**🟢 Fix the questions.** Rewrite each of these interview questions so it asks about specific past behaviour, not opinion or prediction: (a) "Would you use an app to track your deliveries?" (b) "Is waiting for couriers annoying?" (c) "How much would you pay for faster pickups?" (d) "What features should we add?"
*Done when:* every rewritten question asks about something that already happened, and none of them mentions your product or idea.

<details><summary>Model answer and self-check</summary>

**Model answer.** (a) "Tell me about the last delivery you sent. How did you know where it was?" (b) "Yesterday, how long did couriers wait at your counter?" (c) "What did you spend on deliveries last month, and how did you choose that arrangement?" (d) "When did you last get stuck with a delivery? What did you do?"

**Self-check.**
- Would a polite person find it hard to give a flattering but empty answer?

</details>

**🟡 Interview someone about a real problem.** Choose a small, everyday problem in someone else's life that you could plausibly help with (how a friend or relative plans meals, gets to work, shares chores, or tracks spending). With their permission, run a 20-minute conversation using the five-part guide. Then write a problem statement and a job statement from your notes.
*Done when:* your notes separate "said", "did or showed" and "my interpretation"; the problem statement has all five parts; and the job statement follows "when… I want to… so I can…".

<details><summary>Model answer and self-check</summary>

**Model answer.** Topic: a relative's weekly groceries. Said: "I always forget something." Showed: a list on an envelope; three extra shop trips last week. Interpretation: the problem is remembering during the week, not weekend planning. Problem statement: "A working parent of three remembers missing items only while cooking on weekdays, so makes two or three extra trips, each about 30 minutes. She copes with a paper list on the fridge nobody else updates." Job: "When I notice we are out of something, I want it captured where the whole family sees it, so I can do one shop a week."

**Self-check.**
- Is the problem statement free of any solution?

</details>

**🔴 Grade the evidence and choose what to learn next.** Use Qafila's evidence log above. Add two new rows: one finding that would *weaken* the case for the "order ready" button, and one commitment-grade finding you would want before Faisal builds it. Then write three assumptions behind the button, mark each for importance (high, medium, low) and evidence (strong, some, none), and say which one you would test first and how.
*Done when:* each new row has a source, a grade and what it supports or weakens; the assumptions can each be shown false; and your first test aims at the assumption that is most important with the least evidence.

<details><summary>Model answer and self-check</summary>

**Model answer.** Weakening row: "Grocer's couriers wait inside and chat; the owner does not mind" (observed; weakens "waiting is costly" for grocers). Commitment row: "Three shops agree to press 'ready' on every order for a week and share their call log". Assumptions: (1) counter staff will remember to press "ready" in the rush (high importance, no evidence); (2) couriers will check the app instead of waiting for a call (high, some); (3) knowing when an order is ready cuts calls a lot (high, some). Test assumption 1 first, on paper: two bakeries send a message whenever an order is ready during one lunch rush; count how often they do.

**Self-check.**
- Is your first test cheap, fast and done before any code?
- Did you include evidence that could prove Qafila wrong?

</details>

## ⚠️ Mistakes and traps
- **Pitching instead of listening.** Once you describe your idea, people react to it politely. Keep it out of the conversation until the end, if at all.
- **Counting opinions as data.** A hundred "yes" answers to "would you use it?" are still opinions. Grade every finding.
- **Collecting personal data carelessly.** Ask consent, keep only what you need, and ask someone who knows the local rules what applies.

## 🧾 Recap
- A problem statement names who, the situation, the problem, its cost and today's workaround, with no solution.
- A job to be done is the progress a person wants in a situation; anything that delivers that progress is a competitor.
- Ask about specific past events, do not pitch, and listen more than you talk.
- Grade evidence: opinion, story about the past, observed behaviour, commitment; test important, weakly supported assumptions first.
- Rule: believe what people did, not what they say they will do.

## ✍️ Check yourself
**1. Faisal's survey found 13 of 14 pilot shops "would use" an order-ready button. How should it be recorded in the evidence log?**

- A. As observed behaviour, because the answers came directly from the shops themselves.
- B. As a commitment, because the shops took time out of their day to answer the survey.
- C. As an opinion or prediction, the weakest grade, even when many agree.
- D. As proof the problem is solved, since nearly all shops in the pilot answered yes.

<details><summary>Answer</summary>

**C.** "Would use" is a prediction, the lowest grade, however many people say it. A confuses a direct answer with observed behaviour, B overstates a small effort as a commitment, and D treats intentions as results. See "Grades of evidence".

</details>

**2. Which question is most likely to produce reliable evidence in an interview with a bakery owner?**

- A. "Walk me through the last order that arrived late. What happened, step by step?"
- B. "If we built a button to tell couriers an order is ready, how often would you use it?"
- C. "On a scale of one to ten, how frustrating is it to coordinate couriers in general?"
- D. "What features would make our app the best delivery tool for your bakery?"

<details><summary>Answer</summary>

**A.** It asks about a specific past event without mentioning the product. B asks for a prediction about Qafila's idea, C asks for a general opinion, and D asks the customer to design the product. See "Talking to customers".

</details>

**3. Which of these is a job statement in the form the lesson recommends?**

- A. Bakeries need a faster and much simpler way to send all their orders to couriers.
- B. Qafila will add an order-ready button so couriers know when to come.
- C. Shop owners rate courier coordination as their second-biggest problem.
- D. At rush hour, I want each order collected as soon as it is ready, so I can keep serving.

<details><summary>Answer</summary>

**D.** It names the situation, the progress wanted and the deeper reason, with no solution. A is a vague need, B is a solution, and C is a survey finding. See "Jobs to be done".

</details>

**4. The pharmacy logged only three orders in two weeks; the owner says he delivers most prescriptions himself. What is the best conclusion for now?**

- A. The pharmacy is a poor customer and should be removed from the pilot early.
- B. The pharmacy may have a different job, such as privacy, worth exploring.
- C. The app has a usability problem that a better tutorial would solve.
- D. The pharmacy has the same problem as the bakeries but needs more reminders.

<details><summary>Answer</summary>

**B.** The behaviour and his story point to a different job, so it should not be forced into the bakery solution. A throws away a learning, and C and D assume a cause the evidence does not support. See "In practice at Qafila".

</details>

**5. Maha wants to record interviews on her phone to save time writing notes. What should she do first?**

- A. Ask each person's permission, say what she keeps and why, and check local rules.
- B. Record without asking, since the interviews are informal conversations with friendly shops.
- C. Avoid any notes or recordings, since personal data in research is never allowed.
- D. Record everything and paste the transcripts into an AI tool to summarise them later.

<details><summary>Answer</summary>

**A.** Consent, a clear purpose and a check of local data-protection rules come first. B ignores consent, C is wrong because research notes can be kept properly, and D adds a new data-protection question without answering the first. See "Research ethics and personal data".

</details>

## 📚 References
- Christensen, C. M., Hall, T., Dillon, K. and Duncan, D. S., "Know Your Customers' 'Jobs to Be Done'", *Harvard Business Review*, September 2016: https://hbr.org/2016/09/know-your-customers-jobs-to-be-done (reported from search summaries; not opened).
- Fitzpatrick, R., *The Mom Test: How to talk to customers and learn if your business is a good idea when everyone is lying to you* (self-published, 2013): https://www.momtestbook.com/ — the three conversation rules (reported from search summaries; not opened).
- Torres, T., *Continuous Discovery Habits* (Product Talk, 2021): a practitioner's guide to regular customer interviews and assumption testing (full citation; not opened).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 1.2 — Customer interviews that find the truth](../founder/index.html#/1.2).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 1.3 — AI-assisted research without fooling yourself](../founder/index.html#/1.3).
- Library course: [*AI Product Management*, lesson 2.1 — Discovery for AI: jobs, workflows and where AI fits](../aipm/index.html#/2.1).

---

# 1.3 — Business models, costs and the unit of value
*Level: 🟢 Beginner* · *Prerequisites: 1.1, 1.2* · *Step: Discover*

**After this you can** describe a digital product's business model in plain words, choose the unit of value it is paid for, and build a one-page sheet that compares the revenue and the cost to serve for one unit, separating fixed from variable costs and showing the manual work. *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- A **business model** answers four questions: who pays, for what, how the product reaches them, and what it costs to deliver.
- The **unit of value** is the one thing the customer gets and the business is paid for: a delivery, a user per month, a document processed. Pick one and measure everything against it.
- **Fixed costs** stay the same whether you serve 10 units or 1,000. **Variable costs** grow with each unit. **Cost to serve** is the variable cost of one unit, including people's time.
- **Contribution** is revenue per unit minus variable cost per unit. If it is negative, growth makes things worse.
- The rule that matters most: **know what one unit earns and what it costs before you try to sell more of them.**
- Biggest trap: forgetting the human time behind each unit, which is often the biggest variable cost at the start.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks, and the money figures are in an illustrative currency unit ("units").

The pilot is free for its 15 shops. In three months it ends, and Maha must tell shops what Qafila will cost. Faisal suggests a flat monthly fee "like every software company". Maha's friend who runs a grocery says he would rather pay per delivery, "because some weeks I send ten and some weeks a hundred".

Maha looks at her own week: about 45 minutes every morning checking courier assignments, most afternoons answering shop calls, and text messages and a map lookup for every delivery. None of that shows when Faisal says "software costs almost nothing to run". Before choosing a price, they need to know what Qafila sells, what one unit costs to deliver, and which costs grow as shops go from 15 towards 300.

## 📐 How it works

### 🟢 The essentials

**What a business model is.** A **business model** is a plain description of how an organisation creates value for customers and gets paid enough to keep doing it. For a small digital product, four questions cover it:

| Question | Qafila at Launch |
|---|---|
| **Who pays?** | Shops (not couriers, not shop customers, at least for now) |
| **For what?** | Getting local orders to customers on time without chasing |
| **How does it reach them?** | Maha visits shops in person; the merchant and courier apps; the admin web page |
| **What does it cost to deliver?** | Cloud services, messages, maps, Maha's and Faisal's time, courier coordination |

A widely used one-page template for these questions is the **Business Model Canvas**, created by Alexander Osterwalder and published by Strategyzer, with nine boxes from customer segments to cost structure; it is reported to be shared under a Creative Commons licence. It is useful in workshops but not required.

**Common ways digital products charge.** Patterns, not rules; many products mix them:

| Pattern | How it works | Fits when |
|---|---|---|
| **Subscription** | A fixed fee per month or year, per account or user | Use is steady and predictable |
| **Per transaction** | A fee for each unit (each delivery, each payment) | Use varies a lot; value is felt per unit |
| **Commission** | A percentage of the value passing through | The product sits in the middle of a sale |
| **Freemium or tiers** | A free or small tier, and bigger paid bundles | Customers differ a lot in size or needs |

**The unit of value.** The **unit of value** is the thing the customer receives and the business is paid for, counted one at a time. Choosing it well matches price to what customers value, lets you cost each unit, and gives the team one number to watch. Qafila's candidates:

- **A shop per month.** Simple to bill, but a busy bakery and a quiet pharmacy pay the same.
- **A delivery coordinated.** Matches what shops value ("this order got there"), and most costs grow per delivery too.
- **A percentage of order value.** Ties Qafila to shop sales, but a cheap bread order and an expensive medicine order cost the same to coordinate.

Maha and Faisal measure against **a delivery coordinated**, whatever pricing they finally choose.

**Fixed and variable costs.** A **fixed cost** does not change with the number of units in the short term: the base cloud setup, tools, salaries. A **variable cost** grows with each unit: messages, map lookups, payment fees later, support time. Many costs that look fixed have a variable part; a managed database has a base price, but storage and traffic grow with use.

### 🟡 Going deeper

**Cost to serve one unit.** The **cost to serve** is what it takes to deliver one more unit, beyond fixed costs. List each line with an amount per unit and its source. Qafila's first attempt (illustrative, in units):

| Cost line, per delivery | Amount | Basis |
|---|---|---|
| Text messages to courier and shop customer | 0.10 | Last month's provider invoice divided by deliveries |
| Map and route lookups | 0.05 | Provider dashboard divided by deliveries |
| Cloud usage that grows with deliveries | 0.05 | Cloud bill above the base setup, divided by deliveries |
| Maha's manual checks and shop calls | 0.60 | About 3 hours a day at an internal rate, over about 150 deliveries |
| **Total cost to serve** | **0.80** | |

The software lines are small; the human time is three times all of them together. That is normal at Launch, it is what "software costs almost nothing" misses, and it shows where software pays off: anything that cuts Maha's calls lowers the cost of every delivery.

**Contribution.** **Contribution per unit** is revenue per unit minus cost to serve: what each unit contributes towards fixed costs and, eventually, profit. At a price of 1.00 and a cost of 0.80, each delivery contributes 0.20; at about 150 deliveries a day that is around 900 in a 30-day month. If fixed costs are higher (they will be), volume must grow, cost to serve must fall, or the price must rise. Which is realistic is the real business question. If contribution is **negative**, selling more loses money faster. That is the most important thing the sheet can show.

**What changes with scale.** Some costs per unit fall with volume (better message prices; fixed work spread wider); others rise (support for more varied shops; disputes once payments start). Write down which lines you expect to move, and why. At Traction the fact sheet has about 4,000 deliveries a day; if Maha's checks grew with deliveries, they alone would need several full-time people.

### 🔴 Expert view

**Price is not cost plus a margin.** Cost to serve is the floor below which each sale loses money. What customers will pay depends on the value they get and their alternatives: a courier the owner already knows sets a low ceiling. See [*Founder's Playbook for AI-First Builders*, lesson 3.2 — Pricing: choose, test and change a price](../founder/index.html#/3.2).

**Hidden costs that are easy to miss.**

- **People time per unit:** support calls, manual checks, onboarding visits.
- **Payment fees:** from Traction, payments go through a payment provider and each carries a fee; never assume today's price will hold.
- **Failed units:** a failed delivery costs a re-trip, a refund or a call; include the average cost of failures.
- **Obligations:** data protection, consumer protection and tax rules may add work per customer; ask someone who knows the local rules.

**Measure from records, not memory.** Each line should point to an invoice, a dashboard, a time log or a count of calls. Label estimates and replace them when records arrive; unlabelled guesses get trusted.

**AI features.** Each AI model call often has a cost per use; see [*AI Product Management*, lesson 8.2 — Unit economics: cost to serve, pricing models and margins](../aipm/index.html#/8.2).

**The memorable rule.** Know what one unit earns and what it costs before you try to sell more of them.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Business model in four questions** | Who pays, for what, how it reaches them, what it costs to deliver | When starting a product, or when people describe it differently |
| **Business Model Canvas** | A one-page, nine-box template by Strategyzer, reported to be shared under a Creative Commons licence | In workshops where a shared visual helps; not required |
| **Unit-economics sheet** | Revenue per unit, each variable cost line with source and confidence, contribution, fixed costs | Before pricing, and every month after |
| **Spreadsheet** | Any spreadsheet tool; one tab per month so changes are visible | For the sheet itself; keep formulas simple and labelled |

## 🏛️ In practice at Qafila
Maha builds a one-page sheet for the end of the pilot. Illustrative and fictional.

> **Qafila unit-economics sheet (Launch, month 3, draft)**
>
> **Unit of value:** one delivery coordinated, from order logged to drop-off confirmed.
>
> | Line | Per delivery (units) | Source | Confidence |
> |---|---|---|---|
> | Revenue (proposed price) | 1.00 | Proposal; to be tested with 3 shops | Low |
> | Messages | 0.10 | Provider invoice, month 2 | High |
> | Maps | 0.05 | Provider dashboard, month 2 | High |
> | Cloud usage above base | 0.05 | Cloud bill, month 2 | Medium |
> | Manual checks and calls | 0.60 | Maha's time log, 2 weeks | Medium |
> | Failed deliveries (re-trips, goodwill) | 0.05 | About 1 in 50 deliveries, from admin notes | Low |
> | **Cost to serve** | **0.85** | | |
> | **Contribution** | **0.15** | | |
>
> **Fixed costs per month (outside this sheet):** base cloud setup, domain and tools, two founders' pay (not yet drawn).
>
> **What would change the picture:** the "order ready" button (lessons 1.1 and 1.2), if it cuts shop calls, lowers manual time; a monthly minimum for busy shops; price testing with three shops in the last month of the pilot.

Faisal objected to counting Maha's time: "we're not paying ourselves yet." Maha kept it: someone will be paid for that work at 300 shops, and leaving it out makes every delivery look cheaper than it is.

## 🛠️ Exercises
**🟢 Describe a business model in four questions.** Pick a digital product you use (a music service, a ride app, a learning app, a free email service). Answer the four questions: who pays, for what, how it reaches them, what it costs to deliver. Then name its unit of value.
*Done when:* you name who pays (which may not be the user), the unit of value is one countable thing, and you list at least two costs that grow with use.

<details><summary>Model answer and self-check</summary>

**Model answer.** A music streaming service. Who pays: subscribers, and advertisers for free listeners. For what: any song on demand. How it reaches them: app stores, phones, speakers. Costs: payments to rights holders that grow with listening, bandwidth per stream, support. Unit: one paying subscriber per month (revenue), or one stream (costs).

**Self-check.**
- Did you notice when the user and the payer are different people?
- Is your unit countable, so you could put a number against it?

</details>

**🟡 Build a cost-to-serve sheet.** For Qafila at Traction, use the fact sheet figure of about 4,000 deliveries a day. Assume message, map and cloud costs per delivery stay as in Maha's sheet, and that manual work falls to 0.20 per delivery because the "order ready" button worked and a part-time coordinator was hired (illustrative). Recalculate the cost to serve and the contribution at a price of 1.00, and work out the monthly contribution for a 30-day month.
*Done when:* every line is shown with its per-delivery figure, you show your arithmetic, and you state one assumption that could make the result wrong.

<details><summary>Model answer and self-check</summary>

**Model answer.** 0.10 + 0.05 + 0.05 + 0.20 + 0.05 (failures) = 0.45 cost to serve. Contribution = 1.00 − 0.45 = 0.55. Monthly: 0.55 × 4,000 × 30 = 66,000 units (illustrative). Weak assumption: payment fees are missing, though at Traction payments go through a payment provider; and failures may not stay at 1 in 50.

**Self-check.**
- Did you keep every line from the original sheet and change only what the task said?
- Did you spot that a new variable cost (payment fees) arrives at Traction?

</details>

**🔴 Compare three pricing options.** For a set of five illustrative shops sending 5, 10, 10, 20 and 60 deliveries a day, compare (a) a subscription of 300 units per shop per month, (b) 1.00 per delivery, and (c) a tiered plan you design. For each option, calculate monthly revenue from the five shops and the contribution after a cost to serve of 0.85 per delivery. Then say which option you would test first and what customer evidence (lesson 1.2) you would need.
*Done when:* all three options have revenue and contribution figures, you identify any shop that loses Qafila money under an option, and your recommendation names a test, not just a preference.

<details><summary>Model answer and self-check</summary>

**Model answer.** Deliveries per month (30 days): 150, 300, 300, 600, 1,800; total 3,150. Cost to serve: 3,150 × 0.85 = 2,677.50. (a) Subscription: 5 × 300 = 1,500 revenue; contribution = 1,500 − 2,677.50 = −1,177.50. The 600- and 1,800-delivery shops each cost more than they pay (510 and 1,530 against 300). (b) Per delivery: 3,150 revenue; contribution 472.50; every shop contributes 0.15 per delivery. (c) Tiered: up to 200 deliveries a month for 180, up to 600 for 540, above that 0.95 per delivery: revenue 180 + 540 + 540 + 540 + 1,710 = 3,510; contribution 832.50. Test per delivery first, with three shops of different sizes, watching whether shops stop logging deliveries to save money. Evidence needed: what shops spend on deliveries today.

**Self-check.**
- Did you find that a flat subscription loses money on the busiest shop?
- Does your recommendation include a way to learn from real behaviour, not just a calculation?

</details>

## ⚠️ Mistakes and traps
- **"Software is free to run."** Messages, maps, cloud usage and above all people's time grow with every unit. List them.
- **Pricing from cost alone.** Cost sets the floor; customer value and alternatives set what people will pay. Test the price with real shops.
- **One flat price for very different customers.** The busiest customer can quietly lose you money. Check contribution for your largest customers.
- **Unlabelled guesses.** Mark each line with its source and confidence, and replace estimates with records as soon as you can.

## 🧾 Recap
- A business model answers: who pays, for what, how it reaches them, what it costs to deliver.
- Choose one unit of value that matches what the customer values and what drives your costs.
- Separate fixed costs from variable ones; cost to serve is the variable cost of one unit, people's time included.
- Contribution per unit is revenue minus cost to serve; if it is negative, growth makes things worse.
- Price is set between the cost floor and the value ceiling, and must be tested with real customers.
- Rule: know what one unit earns and what it costs before you try to sell more of them.

## ✍️ Check yourself
**1. Faisal says "our software costs almost nothing to run, so any price is profit". What does Maha's sheet show?**

- A. He is right, because message, map and cloud costs per delivery are all very small.
- B. He is wrong only about cloud costs, which turn out to be the largest single cost line.
- C. He is right for now, because unpaid founder time does not count as a real cost.
- D. He is wrong, because human time per delivery is far larger than the software costs.

<details><summary>Answer</summary>

**D.** On the sheet, manual checks and calls cost more than all software lines together. A looks only at software lines, B misreads the sheet (cloud is a small line), and C ignores that the work will need paid people later. See "Cost to serve one unit".

</details>

**2. Which is the best unit of value for Qafila to measure its economics against?**

- A. One shop per month, because subscriptions are what most software companies use.
- B. One delivery coordinated, because shops value it and most costs grow with it.
- C. One app download, because downloads show how many people tried the product.
- D. One percentage point of shop sales, because it links Qafila to shop revenue.

<details><summary>Answer</summary>

**B.** A delivery is what shops value and what drives most variable costs. A is a billing choice, not what drives cost; C measures interest, not value; and D ties Qafila to order value even though a cheap and an expensive order cost the same to coordinate. See "The unit of value".

</details>

**3. With a price of 1.00 and a cost to serve of 0.85 per delivery, what happens if Qafila doubles its deliveries and nothing else changes?**

- A. Total contribution falls, because extra deliveries add more cost than revenue.
- B. Total contribution stays the same, because fixed costs absorb the extra volume.
- C. Total contribution doubles, but it may still not cover the fixed costs.
- D. Total contribution cannot be known without the full Business Model Canvas.

<details><summary>Answer</summary>

**C.** Contribution per unit is positive (0.15), so doubling units doubles total contribution; whether that covers fixed costs is a separate question. A describes negative contribution, B confuses contribution with fixed costs, and D treats a template as required for arithmetic. See "Contribution".

</details>

**4. Under a flat subscription of 300 units a month, a shop sends 1,800 deliveries a month at a cost to serve of 0.85 each. What should Maha conclude?**

- A. This shop costs Qafila more than it pays, so the pricing needs a usage element too.
- B. This shop is the most valuable, because it uses the product the most often.
- C. This shop's costs are covered by the quieter shops, so nothing needs to change.
- D. This shop should be asked to leave the pilot, since it is not profitable.

<details><summary>Answer</summary>

**A.** Its cost to serve (1,530) is far above its fee (300), which argues for a tier or a per-delivery element. B confuses use with value to the business, C hides a growing loss, and D throws away a customer when the price is the problem. See exercise 🔴 and "What changes with scale".

</details>

**5. Bilal (a future finance lead) later asks why "failed deliveries" is a line on the cost-to-serve sheet. What is the best answer?**

- A. It records refunds for tax purposes, which the sheet must show by law.
- B. It is a fixed cost of the courier app, so it belongs on every sheet we make.
- C. It is a placeholder that can be removed once the pilot is finally over.
- D. Failures cost re-trips, refunds or calls, so their average belongs here.

<details><summary>Answer</summary>

**D.** The average cost of failures is part of what each delivery costs to serve. A states a legal conclusion the lesson does not make, B confuses a variable cost with a fixed one, and C assumes failures stop after the pilot. See "Hidden costs that are easy to miss".

</details>

## 📚 References
- Strategyzer, "What is a business model?": https://www.strategyzer.com/library/what-is-a-business-model — the nine building blocks of the Business Model Canvas (reported from search summaries; not opened).
- Osterwalder, A. and Pigneur, Y., *Business Model Generation* (Wiley, 2010) (full citation; not opened).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 3.1 — Unit economics in plain words, including AI and model costs](../founder/index.html#/3.1).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 3.2 — Pricing: choose, test and change a price](../founder/index.html#/3.2).
- Library course: [*AI Product Management*, lesson 8.2 — Unit economics: cost to serve, pricing models and margins](../aipm/index.html#/8.2).
- Library course: [*SaaS Building Blocks*, lesson 3.1 — Subscriptions and payments: checkout, webhooks, the customer portal](../saas/index.html#/3.1).
