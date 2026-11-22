# Module 7 — Service and support

*Qafila is now at Growth. About forty people work there in four teams, about 2,000 merchants use the app for about 25,000 deliveries a day, the teams deploy to production several times a day, and the company has just set up a support desk and product analytics. At this size the product is no longer only software. Merchants and couriers experience a service: an app, plus the people who answer when something is confusing, the way their requests get done, and the promises Qafila makes about how well it all works. This module covers that service side, seen from the inside by Yasmin, a graduate engineer in her first year. First, designing a support model and a shared knowledge base, so that questions reach the right person and every answer is written down once. Second, telling apart questions, requests, incidents and changes, and handling each through one front door without slowing the teams down. Third, agreeing service levels in numbers, deciding what to promise customers in writing, and talking to them honestly when things go wrong. Each lesson leaves an artefact: a support model with a contact-reason list and a first knowledge article, a request catalogue with a change rule, and a service-level sheet with an incident message kit.*

> **Steps:** Operate — run the product as a service people can rely on: answer them well, do what they ask through a known route, change the live system safely, and keep the promises you make in numbers and in words.

---

# 7.1 — Designing the service around the product: support model and knowledge
*Level: 🟡 Intermediate* · *Prerequisites: 4.2, 4.3* · *Step: Operate*

**After this you can** describe a product's support model (who contacts you, through which channels, who answers at each level and how a question moves between them), sort a week of contacts by reason, and write a knowledge article that someone else can follow without asking you. *Study time: reading about 20 min, hands-on about 85 min (estimate).*

## ⚡ In 60 seconds
- A **product** is what people use; a **service** is the product plus the people, routes and promises around it. Customers judge the service, not the code.
- A **support model** says who can contact you, through which **channels** (in-app chat, email, phone), who answers first, and when and how a question moves to someone with more specialist knowledge (**escalation**).
- A **knowledge base** is the shared, searchable set of written answers, best written while you solve the problem.
- The rule that matters most: **answer each question well once, write it down, and make the next answer faster.**
- Decision cue: a question that arrives several times a week needs an article; if it keeps arriving, it needs a product change.
- Biggest trap: treating support as a cost to shrink, not as your clearest signal of where the product confuses people.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

When Qafila had 300 merchants, support was Salma and a shared inbox, and it worked because everyone knew everyone. Now about 2,000 merchants and their couriers make about 25,000 deliveries a day.

In Yasmin's second week, a bakery owner messaged her personally (a friend had passed on her number) to ask why the app showed a courier "arriving" for forty minutes. Yasmin asked in the engineering channel and got three different answers. One, a guess about GPS settings, was wrong, and the bakery owner told two other merchants to change a setting that made things worse.

The same week, Salma counted that in the last month her new desk had answered "how do I add a second branch?" more than sixty times, each answer typed from memory and slightly different. Nobody in the product team knew.

The product worked; the service around it did not. This lesson designs that service: who answers what, how hard questions travel, and how answers become shared knowledge and product changes.

## 📐 How it works

### 🟢 The essentials

**Product and service.** The app is the product. The service is everything a merchant meets: the app, the help screens, the chat with support, the person who sorts out a wrong payment, the message when deliveries are delayed. For the manager's view, see [*Running IT as a Business*, lesson 2.1 — Digital products, services and projects: what each is and who owns it](../itbiz/index.html#/2.1).

**Who contacts you.** Start by listing the groups who need help, because they need different things:

| Group | Typical needs | Qafila example |
|---|---|---|
| **Merchants** (paying customers) | Set-up, billing, how-to, "where is my delivery?" | A pharmacy adding a second branch |
| **Couriers** (people doing the work) | Log-in, payouts, route problems, safety | A courier whose earnings did not update |
| **End customers** (the merchant's customers) | Usually go to the merchant, sometimes to you | Someone tracking a parcel from a bakery |

**Contact reasons.** A **contact reason** is a short, agreed label for why someone got in touch ("add branch", "tracking stuck"). Give every contact one reason; after a few weeks the counts show where the service and the product hurt most.

**Channels.** A **channel** is a route in: in-app chat, email, phone, a help page. More channels split your knowledge and your queue. Pick a few, say which is for what (urgent delivery problems by phone; billing by email), and send stray messages back to them politely. Personal phone numbers are not a channel.

**Levels of support.** Most support models arrange people in levels; the words vary between companies:

| Level | Who | What they handle | Qafila at Growth |
|---|---|---|---|
| **Self-help** | The customer, using help pages and in-app hints | Questions with a known, written answer | Help centre with about 30 articles |
| **First line** | The support desk | Most contacts: how-to, account set-up, known issues | Salma's desk, two people plus Salma |
| **Second line** | People with deeper product or operations knowledge | Problems that need investigation or special access | An operations specialist and the on-call engineer |
| **Third line** | The team that owns the code or system | Bugs and design problems | The product team that owns that part |

The point of levels is not hierarchy: each question is answered by the cheapest person who can answer it **correctly**, and hard questions reach the right expert fast.

**Escalation with a good hand-off.** An **escalation** moves a question to the next level. A good one carries who is affected, what they saw (screenshots, order number), what was tried, how urgent it is, and the contact reason. A bad one says "merchant says app broken, please check".

### 🟡 Going deeper

**The knowledge base.** A **knowledge article** is a short written answer to one question, usable by someone other than its author. Good articles share a shape:

| Part | What goes in it | Example (Qafila) |
|---|---|---|
| **Title in the customer's words** | What they would type or say | "I want to add a second branch" |
| **Environment** | Which app, version, user type, country | Merchant app, any version, owner account |
| **Answer or steps** | Numbered, one action per step | 1. Open Settings → Branches … |
| **Cause** (if a problem) | Why it happens, in plain words | Branch set-up is only visible to owner accounts |
| **When to escalate** | The sign that this article is not enough | If "Branches" is missing, escalate to second line |
| **Status and owner** | Draft or validated; who keeps it current | Validated; owner: support desk |

**Internal articles** are for the desk and engineers (they may name admin tools). **Public articles** are for merchants and couriers (plain words, no internal detail).

**Capture knowledge while you solve.** Later never comes, so: when you answer a question and no article exists, write a draft as part of answering; when an article exists, use it and fix anything wrong in it on the spot. One widely used method built on this idea is **Knowledge-Centered Success (KCS®; formerly Knowledge-Centered Service)**, maintained by the [Consortium for Service Innovation](https://www.serviceinnovation.org/kcs/). To start, you need only one template, one place, and the habit of writing as you go.

**From contacts to product changes.** Support is where the product's confusing parts show up first. Every week, count the top contact reasons and send the top few to the product manager with counts and real examples. The product team decides: fix the product, improve an article, or accept it. When a fix ships, check that the count fell. Contact reasons are a second, very human source of evidence beside the product analytics of lesson 6.3.

**Personal data.** Support conversations hold names, phone numbers, addresses, sometimes health hints (a pharmacy delivery), and data protection rules in most countries set duties on such data. Ask your company which fields may go in tickets, who can see them, how long they are kept, and what must never go into an AI tool.

### 🔴 Expert view

**Contacts the product causes.** Some contacts are value (a merchant asking about a feature they want). Many are caused by the product failing: a confusing screen, a payout that did not update, a status that lies. Track these separately; removing them is usually cheaper than hiring more support staff.

**Support tools and safe access.** Give support staff a purpose-built, logged support view of a customer's account rather than database access, and limit what they can change. See [*SaaS Building Blocks*, lesson 7.1 — The admin panel: support tools and impersonation](../saas/index.html#/7.1).

**AI in support.** An AI tool that drafts replies helps only if it draws on your checked knowledge base, a person stays accountable, and customers can reach a human; on a poor knowledge base it gives wrong answers faster. See [*Founder's Playbook for AI-First Builders*, lesson 5.2 — Support at one-person scale with AI: boundaries, escalation, disclosure](../founder/index.html#/5.2).

**The memorable rule.** Answer each question well once, write it down, and make the next answer faster.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Support model sheet** | Groups served, channels and what each is for, support levels, hours, escalation routes | When support stops being "whoever is around" |
| **Contact reason list** | 15–30 agreed labels, each with a one-line meaning | From the first week of a support desk; reviewed monthly |
| **Escalation hand-off template** | Who, what they saw, what was tried, urgency, reason, links | Every time a question moves up a level |
| **Knowledge article template** | Title in customer words, environment, steps, cause, when to escalate, status, owner | Whenever an answer does not yet exist in writing |
| **Help-desk or ticketing tool** | A shared queue with labels, history and a linked knowledge base (many vendors offer one) | When a shared inbox no longer shows who is handling what |

## 🏛️ In practice at Qafila
Salma drafts Qafila's first support model with Yasmin. Illustrative and fictional.

> **Qafila support model v1 (Growth)**
>
> | Item | Decision |
> |---|---|
> | Groups | Merchants, couriers; end customers are sent to the merchant except for safety issues |
> | Channels | In-app chat (merchants and couriers, 07:00–23:00); email for billing; phone line for urgent delivery problems only, answered by the desk until 23:00 and by the on-call engineer after that. Personal numbers: reply once with the chat link |
> | First line | Support desk (Salma plus two agents); target: most contacts closed here |
> | Second line | Operations specialist (payouts, merchant set-up); on-call engineer for suspected faults |
> | Third line | The owning team: merchant app, courier app, payments, or analytics |
> | Escalation | Hand-off template required; second line acknowledges within one working hour (illustrative) |
> | Knowledge | Internal and public articles in the help-desk tool; Salma owns the template |
> | Feedback | Top five contact reasons to Aisha every Monday with counts and examples |
>
> **First week of labelled contacts (illustrative, about 1,100 contacts):** add branch · tracking stuck at "arriving" · courier payout missing · change opening hours · invoice copy.

Yasmin wrote the article for "tracking stuck at arriving". Her first draft said "GPS issue"; Salma asked how a merchant would know that. The final version explained that the courier app stops sending location when the phone's battery saver is on, gave the steps, and said when to escalate. Aisha saw "add branch" top the Monday report two weeks running and put branch set-up on the next quarter's roadmap.

## 🛠️ Exercises
**🟢 Label a week of contacts.** Here are ten fictional contacts to Qafila's desk: (1) "How do I add my new shop in the new district?"; (2) "Courier has been 'arriving' for 35 minutes"; (3) "My payout for last week is missing"; (4) "Can I get last month's invoice again?"; (5) "Where is the setting for opening hours?"; (6) "App says arriving but courier is still at the shop"; (7) "I opened a second branch, how do I set it up?"; (8) "Courier earnings did not update after 12 deliveries"; (9) "Need a copy of a tax invoice"; (10) "Tracking frozen on 'arriving'". Create no more than six contact reasons, give each a one-line meaning, label each contact, and count them.
*Done when:* every contact has exactly one reason, each reason has a one-line meaning, and you can name the top reason with its count.

<details><summary>Model answer and self-check</summary>

**Model answer.**
- *Tracking stuck* — the app shows a status that does not match where the courier is (2, 6, 10) = 3.
- *Add branch* — a merchant wants a new shop location set up (1, 7) = 2.
- *Courier payout missing* — a courier's earnings or payout did not arrive or update (3, 8) = 2.
- *Invoice copy* — a merchant needs a copy of a past invoice (4, 9) = 2.
- *Opening hours* — a merchant wants to see or change shop hours (5) = 1.

Top reason: tracking stuck, 3. The product causes it, so it goes to the product team as well as getting an article.

**Self-check.**
- Are your labels about the customer's need, not a suspected cause ("GPS bug")?
- Could a new agent apply them the same way, using only the one-line meanings?
- Did you spot which reasons the product causes?

</details>

**🟡 Write one knowledge article.** Pick a question you have answered more than once (how to set up a development environment, how to submit a form at your college) or use Qafila's "change opening hours". Write an article using this lesson's template.
*Done when:* the title uses the asker's words, steps are numbered with one action each, there is a "when to escalate" line, a status and an owner, and a friend can follow it without asking you anything.

<details><summary>Model answer and self-check</summary>

**Model answer.** Title: "I want to change my shop's opening hours". Environment: merchant app, owner or manager account. Steps: 1. Open the menu. 2. Tap Settings → Shop details. 3. Tap Opening hours. 4. Change the day you need and tap Save. 5. Check that the new hours appear on your shop page. Cause (if the option is missing): staff accounts cannot change hours. When to escalate: if an owner account cannot see "Opening hours", send the hand-off to second line with a screenshot. Status: draft. Owner: support desk.

**Self-check.**
- Did you test it on someone, and fix the step where they hesitated?
- Is anything internal (admin tool names) in a public article?
- Does it say what to do when it does not work?

</details>

**🔴 Design a support model.** For an open-source project, a club, a small business, or Qafila at Traction (12 people, 300 merchants), write a support model sheet: groups, channels and their purposes, levels with named roles, an escalation rule with a time, where knowledge lives, and the feedback loop to whoever decides product changes.
*Done when:* every channel has a purpose, every level names a role, the escalation rule has a hand-off template and an acknowledgement time, and the feedback loop names who gets the report and how often.

<details><summary>Model answer and self-check</summary>

**Model answer (Qafila at Traction).** Groups: merchants, couriers. Channels: in-app chat for everything; phone for urgent delivery problems. First line: Salma (working hours); after hours, urgent cases only, to the on-call engineer. Second line: the on-call engineer. Third line: the one team, through the backlog. Escalation: hand-off template, acknowledged within two working hours (illustrative). Knowledge: one shared folder of articles with the template; Salma owns it. Feedback: top five reasons to Aisha every two weeks.

**Self-check.**
- Is the model the right size, or did you copy a big company's tiers onto twelve people?
- Did you keep after-hours work limited, so on-call stays sustainable (lesson 4.2)?
- Could you show where personal data from support is stored and who can see it?

</details>

## ⚠️ Mistakes and traps
- **Too many channels.** Each new channel splits knowledge and creates a queue nobody watches. Choose a few.
- **"We will document it later."** Write the draft article while you solve the problem; improve it every time it is used.
- **Escalating without information.** "Please check" forces the expert to start again. Use the hand-off template every time.
- **Counting tickets but not reasons.** Volume tells you how busy you are, not why. Label every contact and send the top reasons to product.

## 🧾 Recap
- Customers experience a service (product plus people, routes and promises), not only an app.
- A support model names the groups, channels, levels and how questions escalate with a proper hand-off.
- Knowledge articles have a standard shape, an owner and a status; write them while you solve.
- Contact reasons, counted weekly, are evidence for product decisions.
- Rule: answer each question well once, write it down, and make the next answer faster.

## ✍️ Check yourself
**1. A merchant messages Yasmin on her personal phone with a question about tracking. What should she do?**

- A. Answer fully from her own knowledge, since she is an engineer and can probably work it out.
- B. Ignore the message, because personal numbers are not part of Qafila's official support routes.
- C. Reply once, kindly, with the in-app chat link, and tell the desk so the merchant is looked after.
- D. Forward the message to the engineering channel so that the most senior engineer can answer it.

<details><summary>Answer</summary>

**C.** Redirecting politely keeps the answer consistent and recorded, and the desk makes sure the merchant is not dropped. A repeats the bakery mistake, B leaves a customer without help, and D pulls engineers into first-line work without a hand-off. See "Channels".

</details>

**2. A courier tells the desk his payout for last week is missing. The article on payouts does not cover his case. What happens next?**

- A. The agent escalates to the operations specialist with his ID, week, amount and what was checked.
- B. The agent forwards the chat to the payments team's engineers and asks them to look at it when they can.
- C. The agent tells the courier to wait another week, since most missing payouts tend to appear on their own.
- D. The agent asks the courier to email finance directly, because payouts are a money question, not support.

<details><summary>Answer</summary>

**A.** When the article runs out, the question moves to second line (the operations specialist handles payouts) with a hand-off the expert can start from. B skips a level with no detail, C guesses, and D sends the courier to a route that is not a support channel. See "Levels of support" and "Escalation with a good hand-off".

</details>

**3. In the last month Salma's desk has answered "how do I add a second branch?" more than sixty times. What is the best next step?**

- A. Hire another support agent, since the volume shows that the desk is clearly understaffed.
- B. Ask agents to reply faster to this question, using their own words to keep answers personal.
- C. Remove branch set-up from the app until the product team has time to redesign it properly.
- D. Write a validated article, publish it, and send the count to product as evidence for a fix.

<details><summary>Answer</summary>

**D.** One written answer makes every reply consistent, and the count is evidence for a product change. A adds cost without removing the cause, B keeps inconsistent answers, and C removes something merchants need. See "From contacts to product changes".

</details>

**4. Which escalation hand-off is most useful to second line?**

- A. "Pharmacy, order 4471: GPS in courier app is broken, needs an urgent release before tonight's peak."
- B. "Pharmacy, order 4471: tracking stuck on 'arriving' 40 min; restart tried; screenshots attached."
- C. "Pharmacy, order 4471: merchant very upset about tracking again, please call them back today."
- D. "Pharmacy, order 4471: same tracking bug as last week, probably the map; please fix it quickly."

<details><summary>Answer</summary>

**B.** It says who, what they saw and what was tried, with evidence. A and D guess a cause instead of reporting what the customer saw, and C reports a mood, not a symptom. See "Escalation with a good hand-off".

</details>

**5. A product manager asks why the support desk labels every contact with a reason. Which answer is best?**

- A. Counts of reasons over time show where the product confuses people, and whether fixes worked.
- B. Labels make each agent's work easier to audit, so that managers can see who answered which contact.
- C. Labels let the desk close contacts faster, because a labelled contact counts as handled in reports.
- D. Labels are needed to decide which contacts can be deleted after a week to reduce the data kept.

<details><summary>Answer</summary>

**A.** Contact reasons turn support into evidence for product decisions. B and C are about reporting on staff, and D confuses labelling with data retention. See "Contact reasons".

</details>

## 📚 References
- Consortium for Service Innovation, "Knowledge-Centered Success (KCS®)": https://www.serviceinnovation.org/kcs/ — the method's maintainer; the method was formerly called Knowledge-Centered Service.
- Library course: [*Running IT as a Business*, lesson 2.1 — Digital products, services and projects: what each is and who owns it](../itbiz/index.html#/2.1) (the manager's view of products and services).
- Library course: [*SaaS Building Blocks*, lesson 7.1 — The admin panel: support tools and impersonation](../saas/index.html#/7.1) (building safe support tools).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 5.2 — Support at one-person scale with AI: boundaries, escalation, disclosure](../founder/index.html#/5.2) (AI in support, at small scale).

---

# 7.2 — Requests, changes and the service desk in a growing company
*Level: 🟡 Intermediate* · *Prerequisites: 3.3, 7.1* · *Step: Operate*

**After this you can** sort incoming work into questions, service requests, incidents, changes and ideas, set a priority from impact and urgency, write a request catalogue entry with its steps and target time, and choose the right route (routine, planned or urgent) for a change to the live system, including a one-off data fix. *Study time: reading about 20 min, hands-on about 85 min (estimate).*

## ⚡ In 60 seconds
- Work arrives in five kinds, each with its own route: **question**, **service request**, **incident**, **change** and **idea**.
- A **service desk** is the one front door where work arrives, is recorded as **tickets**, sorted and tracked until done.
- **Priority** comes from **impact** (how many are affected, how badly) and **urgency** (how fast harm grows), not from who shouts loudest.
- A **request catalogue** lists the standard things people can ask for, with any approval, the steps and a target time.
- The rule that matters most: **every change to the live system, including data, goes through a known route that leaves a record.**
- Biggest trap: "just quickly" changing production by hand because a customer is waiting.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

On a Wednesday afternoon a sales colleague messaged Yasmin: a large merchant had been promised a lower delivery fee from today, and could she "just update the number in the database"? A senior engineer had shown her where fees were stored. It would take one line.

She asked Salma first. Salma pointed her to an incident from two months earlier: Faisal had fixed a courier's region directly in the database, using the wrong region code. For three days that courier received no offers, and nobody linked it to the manual change because there was no record of it.

At forty people, work arrives from every direction: chat, email, sales, the payment provider, the corridor. When it is all handled the same way, urgent things wait, ideas get built without a decision, and risky changes happen with no record. This lesson sorts the work and gives each kind a route.

## 📐 How it works

### 🟢 The essentials

**Five kinds of incoming work.**

| Kind | Plain meaning | Qafila example | Route |
|---|---|---|---|
| **Question** | Someone needs information | "How do I export my deliveries?" | Answer from the knowledge base (lesson 7.1) |
| **Service request** | A standard, expected ask with known steps | "Add a staff account", "set up a new branch", "invoice copy" | Request catalogue entry |
| **Incident** | Something is broken or about to be | "No courier offers in one city since 10:00" | Incident process (lesson 4.3) |
| **Change** | A deliberate alteration to the live system: code, configuration, infrastructure or data | "Apply the agreed fee for one merchant", "raise a partner's rate limit" (the cap on how many requests that partner's system may send per minute) | Change route (below) |
| **Idea** | A wish for the product to do something new | "Could merchants schedule deliveries a week ahead?" | Product backlog, decided by the product manager (Module 6) |

Split a message that mixes kinds into separate tickets.

Much of this vocabulary was popularised by [**ITIL®**](https://www.peoplecert.org/ITIL-4), a widely used body of guidance on running IT-enabled services, owned by PeopleCert (which acquired the previous owner, AXELOS, in 2021). This course teaches the ideas in its own words; lesson 12.3 compares frameworks.

**The service desk and tickets.** A **ticket** records one piece of work: who asked, what kind, the reason, the priority, who owns it now, what was done, and when it closed. One front door does not mean one channel; it means every channel ends in the same queue. For the manager's view, see [*Running IT as a Business*, lesson 4.1 — Intake and demand management: one front door for ideas and requests](../itbiz/index.html#/4.1).

**Priority from impact and urgency.** Agree a small matrix in advance:

| | **Urgency high** (harm grows by the hour) | **Urgency low** (can wait days) |
|---|---|---|
| **Impact high** (many customers, or money or safety) | P1 | P2 |
| **Impact low** (one customer, small effect) | P2 | P3 |

A big merchant shouting is not high impact by itself; a hundred small merchants who cannot get couriers is. Incidents use the severity scale from lesson 4.3; the matrix orders everything else.

### 🟡 Going deeper

**The request catalogue.** A **request catalogue** lists the service requests people can make. Each entry says:

| Field | Example: "Set up a new branch for a merchant" |
|---|---|
| **Who can ask** | Merchant owner account |
| **Information needed** | Branch name, address, opening hours, contact number |
| **Approval** | None (the owner is entitled) |
| **Steps** | Check owner identity → create branch in admin tool → assign delivery zone → confirm to merchant |
| **Who does it** | Support desk; operations specialist if the address is outside current zones |
| **Target time** | Within one working day (illustrative) |
| **Self-service?** | Planned: merchant app branch set-up next quarter |

Agents follow the same steps, customers know what to expect, and the team can see which requests to turn into **self-service** (the customer does it in the product, with no ticket): frequent, simple, low-risk ones first. For the manager's view, see [*Running IT as a Business*, lesson 7.1 — Request fulfilment and self-service](../itbiz/index.html#/7.1).

**Access requests are requests too.** "Give me production access" is a service request with an approval by the system's owner, a reason and, ideally, an end date. Give the least access that does the job. Dana, who joins at Scale-up, will tighten this later (Module 11), but the habit starts here.

**Three routes for a change.** Changes vary hugely in risk, so this course uses three routes:

| Route | When to use it | Qafila example | What it needs |
|---|---|---|---|
| **Routine route** | Small, frequent, low risk, done the same way every time | Daily code deploy through the pipeline; adding a delivery zone with the admin tool | No separate sign-off: the tests, pull request review and pipeline record are the check (lesson 3.3) |
| **Planned route** | Not routine, or higher risk | A database migration on the orders table; changing the payment provider's settings | Written plan, second reviewer from the owning team, rollback plan, agreed time window |
| **Urgent route** | Needed now to stop or prevent an incident | Turning off a broken feature flag during an incident | Incident lead's agreement at the time; record and review afterwards |

ITIL and many service desks call these three standard, normal and emergency changes; you will hear those words at work.

Most of Qafila's changes should take the routine route, which leaves a record automatically. Make the safe route the easy route.

**Data fixes are changes.** Changing a value in the production database (a fee, a region) is a change, even though no code ships. The safe route: write the change as a script, have a second person review it, run it through a **job runner** (a tool that runs scripts and records who ran what, and when), check the result, and link it to the ticket. If a data fix is needed often, the admin tool is missing a feature.

### 🔴 Expert view

**Approval that helps, and approval that only slows.** It is tempting to add a meeting where senior people approve every change, often called a **change advisory board** (a regular meeting that approves changes). DORA (DevOps Research and Assessment, a long-running research programme on software delivery) says on its capability page on streamlining change approval that its research found approval by an external body, such as a change advisory board or a senior manager, had a negative impact on software delivery performance, and found no evidence that a more formal approval process went with lower change failure rates. It recommends peer review during development, backed by automated testing and monitoring. The lesson is not "no approval": put the check close to the work, done by people who understand it, recorded automatically. For how a larger organisation balances this, see [*Running IT as a Business*, lesson 6.2 — Change control that protects stability without stopping flow](../itbiz/index.html#/6.2).

**Measuring the desk.** Track volume by kind, first response, resolve time by priority, reopened tickets and the oldest open ticket. Judged only on closing fast, agents close tickets too early; look at several measures together.

**When the desk sees an incident first.** Give the desk a rule: three contacts with the same symptom within a short window (illustrative) means "tell the on-call engineer now". The desk is part of your monitoring.

**The memorable rule.** Every change to the live system, including data, goes through a known route that leaves a record.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Work-kind guide** | One page defining the five kinds of work, with examples and routes | Training new agents; sorting a mixed message |
| **Priority matrix** | Impact × urgency → P1–P3, with written examples | Every ticket that is not an incident |
| **Request catalogue** | Standard requests with who can ask, information, approval, steps, owner, target time, self-service plan | When the same request arrives more than a few times |
| **Change route card** | Routine, planned and urgent routes: when to use each and what each needs | Before any change to code, configuration, infrastructure or data |
| **Data-fix procedure** | Script, second reviewer, logged run, result check, link to ticket | Any manual change to production data |

## 🏛️ In practice at Qafila
After the fee request, Salma, Faisal and Yasmin write Qafila's first request catalogue and change rule. Illustrative and fictional.

> **Qafila request catalogue v1 (top five by volume)**
>
> | Request | Approval | Done by | Target (illustrative) | Self-service plan |
> |---|---|---|---|---|
> | New branch | None (owner) | Support desk | 1 working day | Merchant app, next quarter |
> | Staff account for a merchant | Owner confirms in app | Support desk | 4 working hours | Already possible; article updated |
> | Invoice copy | None | Support desk | 4 working hours | Download from billing page, this month |
> | Merchant-specific delivery fee | Signed agreement from sales, checked by finance (Bilal) | Operations specialist via admin tool | 2 working days | Not planned |
> | Courier region change | Courier request plus operations check | Operations specialist via admin tool | 1 working day | Not planned |
>
> **Change rule v1.** Code and infrastructure: routine route through pull request and pipeline. Changes to the structure of the orders and payments tables (the database **schema**): planned route, second reviewer from the owning team, rollback plan, outside 11:00–14:00 and 18:00–21:00. Production data: never by hand; data-fix procedure, linked to a ticket. Emergencies: urgent route; the incident lead decides, the change is recorded in the incident timeline and reviewed afterwards.

The fee went through the new catalogue entry, and Bilal found the signed agreement set it from the first of next month, not today. Faisal added a "fees" screen to the admin tool; Yasmin wrote its tests as her first change to the payments area.

## 🛠️ Exercises
**🟢 Sort the queue.** Classify each fictional message as question, service request, incident, change or idea. Give a priority (P1–P3) with a one-line reason to each question, request and change, using the matrix; ideas go to the backlog without a priority. Messages: (a) "Can I get a copy of my March invoice?"; (b) "None of my couriers in the north zone have had offers for 20 minutes"; (c) "Could the app let me set delivery slots?"; (d) "Please raise the rate limit for our partner's order system from tomorrow"; (e) "How do I change my shop logo?"; (f) "I need a staff account for my new cashier today, she starts at 4 pm".
*Done when:* each message has one kind, each question, request and change has a priority with a one-line reason, the idea goes to the backlog, and the incident is sent to the incident route.

<details><summary>Model answer and self-check</summary>

**Model answer.**
- (a) Service request, P3: one merchant, and nothing gets worse if it waits a day.
- (b) Incident: incident route and severity scale (likely SEV2, one zone degraded).
- (c) Idea: product backlog for the product manager, no ticket priority.
- (d) Change: planned route (configuration affecting a partner); P2: one partner (low impact) but needed tomorrow (high urgency).
- (e) Question: knowledge article; P3: one merchant, no harm while waiting.
- (f) Service request, P2: one merchant (low impact) but needed this afternoon (high urgency).

**Self-check.**
- Did the idea go to the product manager, not the desk's queue?
- Did urgency, not tone, decide (f)?
- Did you see (d) as a change although it sounds like a request?

</details>

**🟡 Write a catalogue entry.** Choose a standard request from your own life or project (access to a shared drive, a reference letter) or Qafila's "staff account for a merchant". Write a catalogue entry with every field in this lesson, including a self-service decision.
*Done when:* the entry names who can ask, the information needed, the approval (or "none" with the reason), numbered steps, who does it, a target time labelled illustrative, and a self-service decision.

<details><summary>Model answer and self-check</summary>

**Model answer.** "Join the project's maintainers' chat". Who can ask: contributors with at least one merged pull request. Information: chat username, link to merged pull request. Approval: one existing maintainer. Steps: 1. Check the pull request is merged. 2. Maintainer approves in the request thread. 3. Send invitation. 4. Add name to the members list. Who: any maintainer. Target: within three days (illustrative). Self-service: not yet; the approval needs judgement about the person, so keep it manual but automate the pull-request check.

**Self-check.**
- Is every step an action, not "handle request"?
- Does any approval add judgement, not only waiting?
- If you proposed self-service, did you keep the checks that matter?

</details>

**🔴 Turn a risky habit into a route.** Faisal's manual region change caused a three-day problem for a courier. Here are Qafila's manual data fixes from last quarter (illustrative): stuck order status released, 22; courier region changed, 14; merchant fee changed, 9; duplicate courier account merged, 3. Write (1) a data-fix procedure Qafila could use from tomorrow, and (2) a short proposal for removing the need for most data fixes. Use the change routes in this lesson.
*Done when:* the procedure has a script, a second reviewer, a logged run, a result check and a ticket link; the proposal picks the most frequent fixes from the list (at least the top two) and names the admin-tool feature or product change that would replace each.

<details><summary>Model answer and self-check</summary>

**Model answer.** (1) Procedure: open a ticket with the reason; write a script that prints before and after values; a second engineer from the owning team reviews it; run it through the job runner; check the record and the customer's view; paste the output into the ticket. (2) Proposal: the top three are stuck order statuses (22), courier region changes (14) and merchant fees (9), together 45 of 48 fixes. Replace them with a "release stuck order" action with a reason field, and find out why orders get stuck; a region screen that offers only valid codes; and the fees screen with a start date. Each is logged; duplicate accounts (3) stay on the procedure.

**Self-check.**
- Would your procedure have caught the wrong region code?
- Could someone find the record three days later?
- Does your proposal remove manual fixes, not just formalise them?

</details>

## ⚠️ Mistakes and traps
- **One queue, one treatment for everything.** Sort by kind first; questions, requests, incidents, changes and ideas need different routes.
- **"Just quickly" in production.** Manual changes without a record are the hardest problems to trace. Use the data-fix procedure, then build the admin feature.
- **Priority by volume of complaint.** A loud customer is not high impact by definition.
- **A change board for everything.** Heavy approval of routine changes slows delivery without making it safer. Put routine changes on the routine route, with checks built into the pipeline.

## 🧾 Recap
- Incoming work comes in five kinds: questions, service requests, incidents, changes and ideas; each has its own route.
- A service desk is one front door with tickets; priority comes from impact and urgency, agreed in advance.
- Changes take a routine, planned or urgent route (often called standard, normal and emergency); data fixes are changes too.
- Rule: every change to the live system, including data, goes through a known route that leaves a record.

## ✍️ Check yourself
**1. A sales colleague asks Yasmin to update a merchant's fee directly in the production database. What should she do?**

- A. Make the update now, since she has database access and the fee was promised for today.
- B. Route it through the agreed request entry, with the signed agreement and a logged record.
- C. Refuse, and tell sales that fees can only change after the next quarterly pricing review.
- D. Ask the senior engineer who showed her the table to make the change instead, to save time.

<details><summary>Answer</summary>

**B.** A fee change is a change to live data and needs a known route with evidence and a record. A and D are the same unrecorded change, and C invents a rule. See "Data fixes are changes".

</details>

**2. "None of my couriers in the north zone have had offers for 20 minutes." What kind of work is this?**

- A. A service request, because the merchant is asking Qafila to do something for them quickly.
- B. A question, because the merchant needs information about the state of their deliveries now.
- C. An idea, because it suggests that offers in the north zone need a better design next quarter.
- D. An incident, because a core journey is not working and the harm grows while it continues.

<details><summary>Answer</summary>

**D.** Something is broken now and harm grows with time. A and B would put it in a queue, and C turns a live fault into a future plan. See "Five kinds of incoming work".

</details>

**3. Which change is the best candidate for the routine route?**

- A. A small code change, tested and reviewed in a pull request, deployed by the usual pipeline.
- B. A one-off migration that reorganises how all orders are stored in the production database.
- C. Switching all merchants to a new payment provider configuration during the evening peak.
- D. A manual edit of a courier's region code in the database, done to help a merchant quickly.

<details><summary>Answer</summary>

**A.** The routine route is for small, frequent, low-risk changes where the built-in checks are enough. B and C need the planned route, and D is the unrecorded manual change this lesson warns against. See "Three routes for a change".

</details>

**4. Faisal proposes that a weekly meeting of senior staff approve every change. What does the DORA page cited in this lesson suggest?**

- A. It suggests external approval goes with fewer failed changes, so the meeting should review every change.
- B. It suggests all approval should be dropped, because any kind of review slows the delivery of software.
- C. It suggests external approval hurts delivery performance, and advises peer review backed by automation.
- D. It suggests approval meetings work well as long as they are held every day instead of once a week.

<details><summary>Answer</summary>

**C.** DORA found external approval hurt delivery performance, with no evidence of fewer failed changes, and recommends peer review backed by automation. A states the opposite, B goes too far, and D changes only the frequency. See "Approval that helps, and approval that only slows".

</details>

**5. Salma wants to choose which service requests to automate first. Which choice fits this lesson?**

- A. The rarest requests, because they are the ones agents are least practised at handling well.
- B. The requests with the most senior approvers, because automation removes the approval step.
- C. The requests that the sales team asks for most, because they are closest to new revenue.
- D. Frequent, simple, low-risk requests such as invoice copies, which can become self-service.

<details><summary>Answer</summary>

**D.** Frequent, simple, low-risk requests give the biggest gain for the least risk. A gives little gain, B removes judgement, and C picks by who asks. See "The request catalogue".

</details>

## 📚 References
- DORA, "Capabilities: Streamlining change approval": https://dora.dev/capabilities/streamlining-change-approval/ — the finding on external change approval and the advice to use peer review backed by automation.
- PeopleCert, ITIL: https://www.peoplecert.org/ITIL-4 — the owner's page for ITIL®.
- Library course: [*Running IT as a Business*, lesson 4.1 — Intake and demand management: one front door for ideas and requests](../itbiz/index.html#/4.1).
- Library course: [*Running IT as a Business*, lesson 7.1 — Request fulfilment and self-service](../itbiz/index.html#/7.1).
- Library course: [*Running IT as a Business*, lesson 6.2 — Change control that protects stability without stopping flow](../itbiz/index.html#/6.2).

---

# 7.3 — Service levels and talking to customers when things go wrong
*Level: 🟡 Intermediate* · *Prerequisites: 4.3, 7.1, 7.2* · *Step: Operate*

**After this you can** write a service-level sheet for one journey (indicator, internal target, error budget in minutes, budget policy), explain why a written promise to customers should be looser than the internal target and what questions to ask before signing one, and write the first message, an update and a closing note for a customer-facing incident. *Study time: reading about 20 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- A **service level** is how well a service performs, in numbers: how available, how fast, how quickly support answers.
- Inside, set **service level objectives (SLOs)** for what customers feel. Qafila's order-tracking target from Growth on is **99.9% monthly**: about 43 bad minutes in a 30-day month.
- Outside, a **service level agreement (SLA)** is a contractual promise. Promise less than you aim for.
- When things go wrong, tell customers early, in plain words, at a known rhythm, with what to do now.
- The rule that matters most: **promise in writing only what you measure, can usually beat, and can explain.**
- Biggest trap: a salesperson promising "99.99% uptime" in an email because it sounds reassuring.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

At Growth, Qafila signed its largest customer so far, a chain of pharmacies. Their contract draft asked for "99.99% availability, a 15-minute response to all support requests, 24 hours a day, and full refund of the monthly fee for any breach". The sales lead had already written back "no problem".

Two weeks later, on a Thursday evening, a faulty release froze order tracking for merchants in the central zone and delayed their courier offers by up to fifty minutes, from about 18:50 to 19:40. The on-call engineer rolled back. But the first message to merchants went out about forty minutes after the problem began, said "technical issue, we are investigating", and gave no next update time. Support received hundreds of contacts, and the pharmacy chain asked how that matched "99.99%".

Salma, now the service and reliability lead, did the arithmetic. In a 30-day month, 99.99% allows about four minutes of bad time. Qafila's own target, 99.9%, allows about 43, and that evening alone had used more. This lesson covers service levels you can keep, promises you can honour, and talking to customers when things go wrong.

## 📐 How it works

### 🟢 The essentials

**Three terms, briefly.** Lesson 4.3 introduced them:

| Term | Plain meaning | Who sees it |
|---|---|---|
| **Service level indicator (SLI)** | A defined measure of one part of the service as customers feel it; a common form is good events ÷ all events | The team, on dashboards |
| **Service level objective (SLO)** | The target for an SLI over a period | The team and company; the basis for decisions |
| **Service level agreement (SLA)** | A promise to a customer, usually in a contract, often with a consequence if it is missed | The customer, lawyers, finance |

**Choose indicators customers feel.** Merchants do not feel "server CPU below 80%". Choose indicators from their journeys:

| Journey | Indicator (illustrative definition) |
|---|---|
| **Order tracking** | Share of minutes in which merchants can see the current status of their orders |
| **Courier offers** | Share of minutes in which at least 95% of new orders get a courier offer within 3 minutes |
| **Support** | Share of chat contacts with a first human reply within 10 minutes, in opening hours |

**The error budget, again.** The error budget is 100% minus the target. For Qafila's order-tracking SLO of 99.9% monthly:

| Month length | Minutes in the month | Allowed bad minutes at 99.9% |
|---|---|---|
| 30 days | 43,200 | 43.2 (about 43) |
| 31 days | 44,640 | 44.6 (about 45) |

The fifty minutes of frozen tracking used more than a whole month's budget in one evening. That number, not anyone's feelings, started the conversation about release safety.

**SLA looser than SLO.** If the internal target is 99.9%, promise less, for example 99.5%, so the team acts long before the customer is owed anything. A promise stricter than your own target is a promise you plan to break.

### 🟡 Going deeper

**What a written promise must define.** An SLA is a contract, and contract rules differ by country, so a lawyer must review it; this is not legal advice. Practitioners should still check that the draft answers these questions:

| Question | Why it matters |
|---|---|
| **What exactly is measured?** | "Availability" of what: the whole app, order tracking, the API? |
| **How, and by whom?** | Your monitoring, the customer's, or an agreed third source? |
| **Over what period?** | Monthly is usual; weekly is harsher; yearly hides bad months |
| **What is excluded?** | Announced maintenance, the customer's own systems and network |
| **What are the consequences?** | Service credits (a discount on a later bill) are common; refunds are heavier |
| **Can we measure it today?** | If not, you cannot know whether you kept it |

**Your promise depends on your suppliers.** Qafila's payments go through a payment provider. If order completion needs both Qafila's service and the provider's, and each is available 99.9% of the time independently, the chance both are working is about 0.999 × 0.999 ≈ 0.998, or 99.8%. A higher promise for that journey is not one you control. Read your suppliers' terms first (Module 10).

**The error budget policy.** A **budget policy** says in advance what happens as the budget is used (Qafila's is in the sheet below). Google's *Site Reliability Workbook* publishes an example error budget policy in its Appendix B. Agree yours before you need it.

**Talking to customers when things go wrong.** Silence is worse than bad news. A good message:

1. **Says what is happening, in the customer's terms.** "Order tracking and courier offers in the central zone are delayed", not "degraded performance in the dispatch service".
2. **Says who is affected,** so unaffected merchants can relax.
3. **Says what to do now** ("orders are saved; use your own courier for urgent deliveries").
4. **Says when the next update is,** and keeps that promise even with no news.
5. **Does not guess the cause** or blame a supplier publicly.

Send it where customers already look: an in-app banner, a **status page** (a page showing current service health and incident updates), and a direct message to large customers. Write templates in advance, in Arabic and English.

**After the incident.** Send a short closing note: what happened, how long, who was affected, what you are changing, and how to get help with any lasting effect. The post-incident review (lesson 4.3) feeds it, but it is written for customers, without blame or jargon. See [*Founder's Playbook for AI-First Builders*, lesson 5.3 — When something breaks: telling customers, and the post-incident note](../founder/index.html#/5.3).

### 🔴 Expert view

**Green reports, unhappy customers.** A report can show every SLA met while customers are unhappy, because the measure is too narrow ("the API answered" while couriers got no offers) or averages hide a bad hour. Check service levels against contact reasons (lesson 7.1) each month; if they disagree, the indicator is probably wrong.

**Service reviews and compensation.** Hold a monthly review with the biggest merchants: levels achieved, incidents, top contact reasons, upcoming changes. Decide in advance who may offer credits, within what limits, recorded by finance. For the management view, see [*Running IT as a Business*, lesson 8.3 — Service levels, SLOs and error budgets as a management tool](../itbiz/index.html#/8.3); for engineering depth, [*Cloud & DevOps: Zero to Hero*, lesson 5.2 — SLOs, error budgets, alerting and on-call that people can sustain](../cloud/index.html#/5.2).

**The memorable rule.** Promise in writing only what you measure, can usually beat, and can explain.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Service-level sheet** | Per journey: SLI definition, SLO and period, error budget in minutes, data source, owner, budget policy | For every journey customers depend on |
| **SLA question list** | What is measured, how, period, exclusions, consequences, can we measure it | Before any contract mentions service levels |
| **Incident message kit** | First message, update and closing note templates in each language, with the update rhythm | Written in advance; used in every customer-facing incident |
| **Status page** | A page showing current health and incident updates (hosted products exist) | Once customers are too many to message one by one |

## 🏛️ In practice at Qafila
After the Thursday evening, Salma and Yasmin prepare the sheet and message kit, and Maha takes a lawyer-reviewed SLA answer to the pharmacy chain. Illustrative and fictional.

> **Service-level sheet: order tracking (Growth)**
>
> | Item | Value |
> |---|---|
> | SLI | Good minutes ÷ all minutes; a minute is good when merchants' requests load current order status within 2 seconds |
> | SLO | 99.9% per calendar month |
> | Error budget | About 43 minutes (30-day month), about 45 (31-day month) |
> | Data source | A synthetic check (lesson 4.2: an automated test request, here sent every minute as if from a merchant) plus request logs |
> | Owner | Salma (dashboard); the tracking team (fixes) |
> | Budget policy | Half spent: owning team reviews the month's changes. Fully spent: reliability work and low-risk changes only until back within target; Aisha re-plans the roadmap |
>
> **Offer to the pharmacy chain (draft, for legal review).** Order tracking 99.5% monthly, measured by Qafila's monitoring; announced maintenance excluded (outside 07:00–23:00, 3 days' notice); service credits per band missed. Support: first reply within 15 minutes for P1 from 07:00 to 23:00; 2 working hours for P2; 1 working day for P3. Monthly service review.
>
> **First message template (English; Arabic version alongside).** "We are seeing [problem in customer words] affecting [who]. [What to do now.] Orders you place are [saved / not affected]. Next update by [time]."

Faisal wanted to offer 99.9% "because that is our target"; Salma showed him the supplier chain and the fifty-minute evening, and he agreed the margin was the point. Salma also cut "P1 around the clock": after 23:00 only the urgent phone line and the on-call engineer cover P1, and nobody had measured how fast they answer. The pharmacy chain accepted 99.5% with a monthly review.

## 🛠️ Exercises
**🟢 Work out the budgets, then write a sheet.** (1) Calculate the allowed bad minutes in a 30-day month for (a) order tracking 99.9%, (b) courier offers 99.5%, (c) merchant reports 99%. For each incident, say what share of the relevant budget it used and whether it exhausts it: incident 1, 50 minutes of delayed offers; incident 2, 3 hours of reports not loading; incident 3, 20 minutes of tracking down. (2) For Qafila's courier-offers journey, or a service you use, write a service-level sheet: SLI as good minutes ÷ all minutes (so a budget in minutes is valid), SLO and period, budget in minutes, data source, owner, and a two-step budget policy.
*Done when:* each target shows its minutes and calculation; each incident has its share and an exhausts-or-not answer; the sheet has all six fields, its SLI says what counts as a good minute, and its policy says what happens at each step and who decides.

<details><summary>Model answer and self-check</summary>

**Model answer.** (1) 43,200 minutes in a 30-day month. (a) 0.1% → 43.2 minutes. (b) 0.5% → 216 minutes. (c) 1% → 432 minutes. Incident 1: 50 of 216 minutes, about 23%. Incident 2: 180 of 432 minutes, about 42%. Incident 3: 20 of 43.2 minutes, about 46%. None exhausts its budget; the shortest, incident 3, used the largest share.

(2) *Courier offers.* SLI: good minutes ÷ all minutes; a minute is good when at least 95% of new orders get a courier offer within 3 minutes. SLO: 99.5% per calendar month. Budget: about 216 minutes in a 30-day month. Data source: dispatch logs. Owner: the dispatch team. Policy: half spent, the owner reviews the month's changes with Aisha; fully spent, only reliability work and low-risk changes ship until back within target, and Aisha decides which roadmap items move.

**Self-check.**
- Did you use the minutes in the month, not hours or a year?
- Did you see that the same outage matters more on a stricter target?
- Does your SLI count something users notice, from a source that exists?

</details>

**🟡 Review an SLA draft.** Take the pharmacy chain's first request from this lesson. Using the SLA question list, write the questions you would raise and a counter-offer with reasons. Do not state any legal conclusion.
*Done when:* you raise at least five questions from the list, the counter-offer sets an availability below Qafila's internal target, sets support times by priority within the hours Qafila staffs, and marks what needs legal and finance review.

<details><summary>Model answer and self-check</summary>

**Model answer.** Questions: availability of what? Measured by whom? Over what period? Are maintenance and the payment provider's failures excluded? What counts as a "response"? Is a full refund proportionate (for the lawyer)? Can we measure every term today? Counter-offer: order tracking 99.5% monthly (99.99% allows about 4 minutes a month, which we cannot honestly promise); P1 within 15 minutes from 07:00 to 23:00, with an after-hours target only once the on-call phone route is measured; P2 2 working hours; P3 1 working day; service credits instead of refunds, amounts for finance and legal; monthly review.

**Self-check.**
- Did you show the arithmetic for 99.99%?
- Did you send legal questions to a lawyer instead of answering them?
- Is every promise something Qafila measures today?

</details>

**🔴 Write the message kit and replay the Thursday evening.** Write the first message, one update and the closing note for the Thursday incident (central zone, about 18:50 to 19:40, tracking frozen and offers delayed by up to 50 minutes), using the five points in this lesson. Then compare it in a few lines with the original message, and propose the update rhythm and who sends what.
*Done when:* the first message has the problem in customer words, who is affected, what to do now and the next update time; the closing note says what happened, how long, who, what will change and how to get help; the rhythm names roles, not people.

<details><summary>Model answer and self-check</summary>

**Model answer.** First message (19:05, with what was known then): "Order tracking in the central zone is not updating, and courier offers there are delayed. Other zones are not affected. Orders you place are saved; for urgent deliveries you may use your own courier. Next update by 19:35." Update (19:35): "We have reversed a change made this evening and the fix is rolling out; tracking and offers should be back to normal within minutes. Some orders have waited up to 50 minutes. Next update by 20:05." Closing note (next day): "Yesterday from about 18:50 to 19:40, a change to our app stopped order tracking from updating and delayed courier offers by up to 50 minutes for merchants in the central zone. About [n] merchants were affected. We reversed the change, and will now release such changes to a small share of orders first. If an order was late, reply to this message and our team will help." Comparison: the original gave no impact, no action and no next time, so merchants contacted support instead. Rhythm: the incident communications role posts the banner and status page within 15 minutes, then every 30; the account manager messages large customers; the support lead sends the closing note within one working day.

**Self-check.**
- Did the first message go out quickly, even without knowing the cause?
- Did any message blame a person or a supplier?
- Does the closing note promise a specific change?

</details>

## ⚠️ Mistakes and traps
- **Promising what you aim for.** If the SLA equals or beats the SLO, any bad month becomes a breach. Keep a margin.
- **Indicators customers do not feel.** Measure journeys, not CPU.
- **Ignoring suppliers.** Your promise cannot be stronger than the chain it depends on. Do the multiplication.
- **"Technical issue, investigating."** Say what is affected, who, what to do and when you will update.
- **Promising hours you do not staff.** Check every support time in an SLA against your support model's hours and who covers the rest.

## 🧾 Recap
- Service levels describe in numbers how well the service works; SLIs measure, SLOs set internal targets, SLAs make promises to customers.
- Promise less than you aim for, define what is measured and excluded, and check your suppliers' promises.
- In an incident, tell customers early, in their words, with what to do now and a next update time.
- Rule: promise in writing only what you measure, can usually beat, and can explain.

## ✍️ Check yourself
**1. Qafila's internal target for order tracking is 99.9% monthly. What should the contractual promise to the pharmacy chain be?**

- A. 99.99%, because a stricter promise reassures the customer that Qafila takes reliability seriously.
- B. 99.9%, exactly the internal target, so that the team and the customer share one single number.
- C. 100%, with exclusions for maintenance, because customers today expect a service that never fails.
- D. A lower figure, such as 99.5%, so the team sees trouble early and can act before any promise is broken.

<details><summary>Answer</summary>

**D.** An SLA looser than the SLO gives a safety margin. A allows about four minutes a month, B turns every bad month into a breach, and C is a promise no service can keep. See "SLA looser than SLO".

</details>

**2. The courier-offers SLO is 99.5% monthly. How many bad minutes does it allow in a 31-day month?**

- A. About 216, because 0.5% of 43,200 minutes is 216.
- B. About 223, because 0.5% of 44,640 minutes is 223.2.
- C. About 22, because 0.05% of 44,640 minutes is 22.3.
- D. About 2,628, because 0.5% of a year is 2,628 minutes.

<details><summary>Answer</summary>

**B.** 31 × 24 × 60 = 44,640 minutes, and 0.5% of that is 223.2. A uses a 30-day month, C moves the decimal point (0.05% instead of 0.5%), and D works out the budget for a year, not a month. See "The error budget, again".

</details>

**3. Order completion needs both Qafila's service and the payment provider, each independently available 99.9% of the time. About how available is the journey?**

- A. 99.9%, because the weaker of the two services sets the journey's level.
- B. 99.95%, because two independent services back each other up in failures.
- C. 99.8%, because both must work at once: 0.999 × 0.999 is about 0.998.
- D. 99.0%, because each extra dependency removes about one percentage point.

<details><summary>Answer</summary>

**C.** Availabilities in a chain multiply. A ignores the second service's failures, B treats a chain as a backup, and D invents a rule. See "Your promise depends on your suppliers".

</details>

**4. Tracking and offers in the central zone are delayed. Which first message to merchants is best?**

- A. "Central zone: tracking and offers delayed by a dispatch-team change; sorry, we are fixing it now."
- B. "Central zone: tracking and offers delayed; other zones fine; orders are saved; next update 19:35."
- C. "Central zone: tracking and offers delayed by our payment provider's outage; please wait for them."
- D. "Central zone: tracking and offers delayed; our engineers are investigating; we will update you."

<details><summary>Answer</summary>

**B.** It names the problem, who is affected, what is safe and the next update time. A blames a team, C guesses a cause and blames a supplier, and D gives no update time and nothing to do. See "Talking to customers when things go wrong".

</details>

**5. Every monthly report to the pharmacy chain shows the SLA met, but their branches keep complaining. What does this lesson suggest?**

- A. The complaints can be ignored, because the contract defines what good service means.
- B. The SLA should be tightened to 99.99%, so the report shows a more demanding target.
- C. Compare the indicator with contact reasons; it may be measuring too narrow a thing.
- D. Stop sending the reports, since they are causing friction with the customer's managers.

<details><summary>Answer</summary>

**C.** Green reports with unhappy customers usually mean the indicator misses what customers feel. A treats the contract as the whole truth, B changes the target, not the measure, and D hides the problem. See "Green reports, unhappy customers".

</details>

## 📚 References
- Google, *The Site Reliability Workbook*, Appendix B, "Example Error Budget Policy": https://sre.google/workbook/error-budget-policy/
- Google, *The Site Reliability Workbook*, chapter 2, "Implementing SLOs": https://sre.google/workbook/implementing-slos/ — SLIs, SLOs and error budgets in practice.
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 5.3 — When something breaks: telling customers, and the post-incident note](../founder/index.html#/5.3).
- Library course: [*Running IT as a Business*, lesson 8.3 — Service levels, SLOs and error budgets as a management tool](../itbiz/index.html#/8.3).
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 5.2 — SLOs, error budgets, alerting and on-call that people can sustain](../cloud/index.html#/5.2).
