# Module 7 — Service and support

*Qafila is now at Growth. About forty people work there in four teams, about 2,000 merchants use the app for about 25,000 deliveries a day, the teams deploy to production several times a day, and the company has just set up a support desk and product analytics. At this size the product is no longer only software. Merchants and couriers experience a service: an app, plus the people who answer when something is confusing, the way their requests get done, and the promises Qafila makes about how well it all works. This module covers that service side, seen from the inside by Yasmin, a graduate engineer in her first year. First, designing a support model and a shared knowledge base, so that questions reach the right person and every answer is written down once. Second, telling apart questions, requests, incidents and changes, and handling each through one front door without slowing the teams down. Third, agreeing service levels in numbers, deciding what to promise customers in writing, and talking to them honestly when things go wrong. Each lesson leaves an artefact: a support model with five knowledge articles, a request catalogue with a change rule, and a service-level sheet with an incident message kit.*

> **Steps:** Operate — run the product as a service people can rely on: answer them well, do what they ask through a known route, change the live system safely, and keep the promises you make in numbers and in words.

---

# 7.1 — Designing the service around the product: support model and knowledge
*Level: 🟡 Intermediate* · *Prerequisites: 4.2, 4.3* · *Step: Operate*

**After this you can** describe a product's support model (who contacts you, through which channels, who answers at each level and how a question moves between them), sort a week of contacts by reason, and write a knowledge article that someone else can follow without asking you. *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- A **product** is what people use; a **service** is the product plus the people, routes and promises around it. Customers judge the service, not the code.
- A **support model** says who can contact you, through which **channels** (in-app chat, email, phone), who answers first, and when and how a question moves to someone with more specialist knowledge (**escalation**).
- A **knowledge base** is the shared, searchable set of written answers. The best time to write an answer down is while you solve the problem, not "later".
- The rule that matters most: **answer each question well once, write it down, and make the next answer faster.**
- Decision cue: if the same question arrives more than a few times a week, it needs a knowledge article; if it keeps arriving after that, it needs a product change.
- Biggest trap: treating support as a cost to shrink instead of the clearest signal you have about where the product confuses people.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

When Qafila had 300 merchants, support was Salma and a shared inbox. Merchants also messaged Maha directly, and couriers called whoever had once given them a phone number. It worked because everyone knew everyone.

Now about 2,000 merchants and their couriers make about 25,000 deliveries a day. In Yasmin's second week, a bakery owner messaged her personally (a friend of a friend had passed on her number) to ask why the app showed a courier "arriving" for forty minutes. Yasmin did not know. She asked in the engineering channel; three people gave three different answers. One of them, a guess about GPS settings, was wrong, and the bakery owner told two other merchants to change a setting that made things worse.

The same week, Salma counted that her new two-person support desk had answered the question "how do I add a second branch?" more than sixty times, each answer typed from memory and slightly different. Nobody in the product team knew this. The roadmap that quarter did not mention branches at all.

Nothing here was a technical failure. The product worked; the service around it did not. This lesson designs that service: who answers what, how hard questions travel, and how answers become shared knowledge and product changes.

## 📐 How it works

### 🟢 The essentials

**Product and service.** The app is the product. The service is everything a merchant meets: the app, the help screens, the chat with support, the person who sorts out a wrong payment, the message when deliveries are delayed. Two companies can have the same app quality and very different reputations because of the service around it. For the manager's view of the same distinction, see [*Running IT as a Business*, lesson 2.1 — Digital products, services and projects: what each is and who owns it](../itbiz/index.html#/2.1).

**Who contacts you, and why.** Start a support model by listing the groups who need help, because they need different things:

| Group | Typical needs | Qafila example |
|---|---|---|
| **Merchants** (paying customers) | Set-up, billing, how-to, "where is my delivery?" | A pharmacy adding a second branch |
| **Couriers** (people doing the work) | Log-in, payouts, route problems, safety | A courier whose earnings did not update |
| **End customers** (the merchant's customers) | Usually go to the merchant, sometimes to you | Someone tracking a parcel from a bakery |
| **Internal colleagues** | Access, data, "is this a bug?" | Sales asking if a feature exists |

**Contact reasons.** A **contact reason** is a short, agreed label for why someone got in touch ("add branch", "courier payout missing", "tracking stuck"). Give every contact one reason. After a few weeks you can count them, and the counts tell you where the service and the product hurt most.

**Channels.** A **channel** is a route in: in-app chat, email, phone, a help page, a messaging app. More channels feel friendlier but split your knowledge and your queue. Pick a small number, say which is for what (urgent delivery problems by phone or chat; billing by email), and send stray messages back to them politely. Personal phone numbers are not a channel.

**Levels of support.** Most support models arrange people in levels. The words vary between companies; the idea is the same:

| Level | Who | What they handle | Qafila at Growth |
|---|---|---|---|
| **Self-help** | The customer, using help pages and in-app hints | Questions with a known, written answer | Help centre with about 30 articles |
| **First line** | The support desk | Most contacts: how-to, account set-up, known issues | Salma's desk, two people plus Salma |
| **Second line** | People with deeper product or operations knowledge | Problems that need investigation or special access | An operations specialist and the on-call engineer |
| **Third line** | The team that owns the code or system | Bugs and design problems | The product team that owns that part |

The point of levels is not hierarchy. It is that each question is answered by the cheapest person who can answer it **correctly**, and that hard questions reach the right expert fast, with enough information that the expert does not have to start again.

**Escalation with a good hand-off.** An **escalation** moves a question to the next level. A good one carries: who is affected, what they saw (screenshots, order number), what has already been tried, how urgent it is, and the contact reason. A bad one says "merchant says app broken, please check".

### 🟡 Going deeper

**The knowledge base.** A **knowledge article** is a short written answer to one question or problem, written so that someone other than the author can use it. Good articles share a shape:

| Part | What goes in it | Example (Qafila) |
|---|---|---|
| **Title in the customer's words** | What they would type or say | "I want to add a second branch" |
| **Environment** | Which app, version, user type, country | Merchant app, any version, owner account |
| **Answer or steps** | Numbered, one action per step | 1. Open Settings → Branches … |
| **Cause** (if a problem) | Why it happens, in plain words | Branch set-up is only visible to owner accounts |
| **When to escalate** | The sign that this article is not enough | If "Branches" is missing, escalate to second line |
| **Status and owner** | Draft or validated; who keeps it current | Validated; owner: support desk |

There are two audiences. **Internal articles** are for the desk and engineers (they may mention admin tools and internal names). **Public articles** are for merchants and couriers (plain words, no internal detail). Many answers start internal and become public once they are checked.

**Capture knowledge while you solve.** The common failure is "we will document it later". Later never comes. The practical rule is: when you answer a question and no article exists, write a draft article as part of answering; when an article exists, use it and fix anything wrong in it on the spot. One widely used method built on this idea is **Knowledge-Centered Service (KCS®)**, maintained by the Consortium for Service Innovation, a non-profit; its materials describe building the use, improvement and creation of knowledge into the everyday work of solving issues (as reported from search summaries; KCS® is reported to be a registered service mark of the Consortium). You do not need any method's full practice to start: one template, one place, and the habit of writing as you go.

**From contacts to product changes.** Support is where the product's confusing parts show up first. Set up a loop:

1. Every contact gets a reason label.
2. Every week, someone counts the top reasons and their trend.
3. The top few go to the product manager with counts and two or three real examples.
4. The product team decides: fix the product, improve an article, or accept it.
5. When a fix ships, the count for that reason should fall. Check that it did.

Lesson 6.3 covered product analytics; contact reasons are a second, very human source of evidence for the same decisions.

**Personal data in support.** Support conversations are full of personal data: names, phone numbers, addresses, sometimes health hints (a pharmacy delivery). Data protection rules in most countries set duties on how such data is collected, kept, shared and deleted. Ask your company: which fields may we store in tickets, who can see them, how long we keep them, and what we must never paste into a chat or an AI tool. Do not invent your own answer.

### 🔴 Expert view

**Contacts the product causes.** Some contacts are value (a merchant asking how to use a feature they want). Many are caused by the product or service failing to do something right the first time: a confusing screen, a payout that did not update, a status that lies. Track these separately. Reducing contacts the product causes is usually cheaper than hiring more support staff, and it makes the product better.

**Engineers in support.** Many teams put engineers on a support rotation, for example one engineer per team spending a day a fortnight with the desk, answering second-line questions. It is uncomfortable at first and very effective: engineers see how merchants actually use what they built. Keep it time-boxed and paired with the on-call rota from lesson 4.2 so nobody is on everything at once.

**Support tools and safe access.** Support staff often need to see a customer's account to help. Give them a purpose-built, logged support view rather than database access, and limit what they can change. For how admin panels and "act as this user" features should be built and guarded, see [*SaaS Building Blocks*, lesson 7.1 — The admin panel: support tools and impersonation](../saas/index.html#/7.1).

**AI in support.** Drafting replies and suggesting articles with an AI tool can help, if the answers come from your checked knowledge base, a person stays accountable, customers are told when they are talking to an automated assistant where that is expected, and there is a clear route to a human. For a small-scale view of these limits, see [*Founder's Playbook for AI-First Builders*, lesson 5.2 — Support at one-person scale with AI: boundaries, escalation, disclosure](../founder/index.html#/5.2). An AI assistant on top of a poor knowledge base gives wrong answers faster.

**The memorable rule.** Answer each question well once, write it down, and make the next answer faster.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Support model sheet** | Groups served, channels and what each is for, support levels, hours, escalation routes | When support stops being "whoever is around" |
| **Contact reason list** | 15–30 agreed labels, each with a one-line meaning | From the first week of a support desk; reviewed monthly |
| **Escalation hand-off template** | Who, what they saw, what was tried, urgency, reason, links | Every time a question moves up a level |
| **Knowledge article template** | Title in customer words, environment, steps, cause, when to escalate, status, owner | Whenever an answer does not yet exist in writing |
| **Weekly contact report** | Top reasons with counts, trend and examples, sent to product | Every week, before backlog review |
| **Help-desk or ticketing tool** | A shared queue with labels, history and a linked knowledge base (many vendors offer one; examples, not endorsements) | When a shared inbox no longer shows who is handling what |

## 🏛️ In practice at Qafila
Salma drafts Qafila's first support model with Yasmin, who has volunteered after the bakery mix-up. Illustrative and fictional.

> **Qafila support model v1 (Growth)**
>
> | Item | Decision |
> |---|---|
> | Groups | Merchants, couriers; end customers are sent to the merchant except for safety issues |
> | Channels | In-app chat (merchants and couriers, 07:00–23:00); email for billing; phone line for urgent delivery problems only. Personal numbers: reply once with the chat link |
> | First line | Support desk (Salma plus two agents); target: most contacts closed here |
> | Second line | Operations specialist (payouts, merchant set-up); on-call engineer for suspected faults |
> | Third line | The owning team: merchant app, courier app, payments, or analytics |
> | Escalation | Hand-off template required; second line acknowledges within one working hour (illustrative) |
> | Knowledge | Internal and public articles in the help-desk tool; "write it as you solve it"; Salma owns the template |
> | Feedback | Top five contact reasons to Aisha every Monday with counts and examples |
>
> **First week of labelled contacts (illustrative, about 1,100 contacts):** add branch · tracking stuck at "arriving" · courier payout missing · change opening hours · invoice copy.

Yasmin wrote the article for "tracking stuck at arriving" after shadowing the on-call engineer. Her first draft said "GPS issue". Salma asked how a merchant would know that. The final version explained that the courier app stops sending location when the phone's battery saver is on, gave the steps for couriers, and said when to escalate. Aisha saw "add branch" at the top of the Monday report two weeks running and moved branch set-up into the next quarter's roadmap.

## 🛠️ Exercises
**🟢 Label a week of contacts.** Here are ten fictional contacts to Qafila's desk: (1) "How do I add my new shop in the new district?"; (2) "Courier has been 'arriving' for 35 minutes"; (3) "My payout for last week is missing"; (4) "Can I get last month's invoice again?"; (5) "Where is the setting for opening hours?"; (6) "App says arriving but courier is still at the shop"; (7) "I opened a second branch, how do I set it up?"; (8) "Courier earnings did not update after 12 deliveries"; (9) "Need a VAT invoice copy"; (10) "Tracking frozen on 'arriving'". Create no more than six contact reasons, label each contact, and count them.
*Done when:* every contact has exactly one reason, each reason has a one-line meaning, and you can name the top reason with its count.

<details><summary>Model answer and self-check</summary>

**Model answer.** Reasons: *add branch* (1, 7) = 2; *tracking stuck* (2, 6, 10) = 3; *courier payout missing* (3, 8) = 2; *invoice copy* (4, 9) = 2; *opening hours* (5) = 1. Top reason: tracking stuck, 3. It is also a contact the product causes, so it goes to the product team as well as getting an article.

**Self-check.**
- Are your labels about the customer's need, not about the suspected cause ("GPS bug")?
- Could a new agent apply your labels the same way you did?
- Did you notice which reasons are caused by the product failing, not by a wish to do something new?

</details>

**🟡 Write one knowledge article.** Pick a question you have answered more than once in your own life or project (how to set up a development environment, how to reset a password in an app you look after, how to submit a form at your college) or use Qafila's "change opening hours". Write an article using the template in this lesson.
*Done when:* the title uses the asker's words, the steps are numbered with one action each, there is a "when to escalate" line, a status and an owner, and a friend who has never done it can follow it without asking you anything.

<details><summary>Model answer and self-check</summary>

**Model answer.** Title: "I want to change my shop's opening hours". Environment: merchant app, owner or manager account. Steps: 1. Open the menu. 2. Tap Settings → Shop details. 3. Tap Opening hours. 4. Change the day you need and tap Save. 5. Check that the new hours appear on your shop page. Cause (if the option is missing): staff accounts cannot change hours. When to escalate: if an owner account cannot see "Opening hours", send the hand-off to second line with a screenshot. Status: draft. Owner: support desk.

**Self-check.**
- Did you test it on someone, and fix the step where they hesitated?
- Is anything internal (admin tool names, database terms) in a public article? Move it to an internal one.
- Does the article say what to do when it does not work?

</details>

**🔴 Design a support model for a product you know.** For an open-source project, a club, a small business you know, or Qafila at Traction (12 people, 300 merchants), write a support model sheet: groups, channels and their purposes, levels with named roles, escalation rule with a time, where knowledge lives, and the feedback loop to whoever decides product changes.
*Done when:* every channel has a stated purpose, every level names a role (not "someone"), the escalation rule has a hand-off template and an acknowledgement time, and the feedback loop names who receives the report and how often.

<details><summary>Model answer and self-check</summary>

**Model answer (Qafila at Traction).** Groups: merchants, couriers. Channels: in-app chat for everything; phone for urgent delivery problems. First line: Salma (working hours), the on-call engineer after hours for urgent cases only. Second line: the on-call engineer. Third line: the one team, through the backlog. Escalation: hand-off template, acknowledged within two working hours (illustrative). Knowledge: one shared folder of articles with the template; Salma owns it. Feedback: top five reasons to Aisha every two weeks.

**Self-check.**
- Is the model the right size for the organisation, or did you copy a big company's tiers onto twelve people?
- Did you keep after-hours work limited, so on-call stays sustainable (lesson 4.2)?
- Could you show where personal data from support conversations is stored and who can see it?

</details>

## ⚠️ Mistakes and traps
- **Too many channels.** Each new channel splits knowledge and creates a queue nobody watches. Choose a few and say what each is for.
- **"We will document it later."** Write the draft article while you solve the problem; improve it every time it is used.
- **Escalating without information.** "Please check" forces the expert to start again. Use the hand-off template every time.
- **Counting tickets but not reasons.** Volume alone tells you how busy you are, not why. Label every contact.
- **Support as a cost centre only.** If the product team never sees contact reasons, the same problems keep costing money. Send the top reasons to product weekly.
- **Giving support staff database access "to be quick".** Build a logged support view with limited actions instead.

## 🧾 Recap
- Customers experience a service (product plus people, routes and promises), not only an app.
- A support model names the groups served, the channels, the levels of support and how questions escalate with a proper hand-off.
- Knowledge articles have a standard shape, an owner and a status; write them while you solve, and fix them whenever you use them.
- Contact reasons, counted weekly, are evidence for product decisions; contacts the product causes are the cheapest to remove.
- Rule: answer each question well once, write it down, and make the next answer faster.

## ✍️ Check yourself
**1. A merchant messages Yasmin on her personal phone with a question about tracking. What should she do?**

- A. Answer fully from her own knowledge, since she is an engineer and can probably work it out.
- B. Ignore the message, because personal numbers are not part of Qafila's official support routes.
- C. Reply once, kindly, with the in-app chat link, and tell the desk so the merchant is looked after.
- D. Forward the message to the engineering channel so that the most senior engineer can answer it.

<details><summary>Answer</summary>

**C.** Personal numbers are not a channel; redirecting politely keeps the answer consistent and recorded, and alerting the desk means the merchant is not dropped. A repeats the bakery mistake (an unchecked answer outside the system), B leaves a customer without help, and D pulls engineers into first-line work without a hand-off. See "Channels".

</details>

**2. What is the main purpose of support levels (first, second, third line)?**

- A. Each question is answered correctly by the least specialised person who can, and hard ones reach experts fast.
- B. Senior engineers are protected from customers so they can spend all their time on new features.
- C. Customers learn to wait longer for difficult answers, which keeps the overall contact volume down.
- D. Each level can be measured separately, so that managers can compare the productivity of staff.

<details><summary>Answer</summary>

**A.** Levels route each question to the cheapest correct answer and move hard ones quickly with context. B is a side effect at best and cuts engineers off from customer reality, C mistakes delay for a goal, and D is about reporting, not service. See "Levels of support".

</details>

**3. Salma's desk has answered "how do I add a second branch?" more than sixty times. What is the best next step?**

- A. Hire another support agent, since the volume shows that the desk is clearly understaffed.
- B. Ask agents to reply faster to this question, using their own words to keep answers personal.
- C. Remove branch set-up from the app until the product team has time to redesign it properly.
- D. Write a validated article, publish it, and send the count to product as evidence for a fix.

<details><summary>Answer</summary>

**D.** One written answer makes every reply consistent and faster, and the count is evidence for a product change. A adds cost without removing the cause, B keeps inconsistent answers, and C removes something merchants need. See "Capture knowledge while you solve" and "From contacts to product changes".

</details>

**4. Which escalation hand-off is most useful to second line?**

- A. "Merchant says the app is broken again; this is urgent, please check as soon as you can."
- B. "Pharmacy, order 4471: tracking stuck on 'arriving' 40 min; restart tried; screenshots attached."
- C. "Several merchants are unhappy today; could someone from engineering take a look at tracking?"
- D. "Possible GPS bug in the courier app; recommend a hotfix before this evening's busy period."

<details><summary>Answer</summary>

**B.** It says who, what they saw, what was tried and includes evidence, so the expert can start immediately. A and C carry no detail, and D guesses a cause and a fix instead of reporting what the customer saw. See "Escalation with a good hand-off".

</details>

**5. A product manager asks why the support desk labels every contact with a reason. Which answer is best?**

- A. Counts of reasons over time show where the product and service confuse people, and whether fixes worked.
- B. Labels make each agent's work easier to audit, so that managers can see who answered which contact.
- C. Labels let the desk close contacts faster, because a labelled contact counts as handled in reports.
- D. Labels are needed to decide which contacts can be deleted after a week to reduce the data kept.

<details><summary>Answer</summary>

**A.** Contact reasons turn support into evidence for product decisions and let you check whether a fix reduced contacts. B and C are about reporting on staff rather than learning, and D confuses labelling with data retention, which is a separate question. See "Contact reasons" and "From contacts to product changes".

</details>

## 📚 References
- Consortium for Service Innovation, Knowledge-Centered Service (KCS) overview: https://www.serviceinnovation.org/kcs/ — the method's maintainer (page could not be opened from this environment; the description and the service-mark status are as reported in search summaries).
- Consortium for Service Innovation, "KCS Unlocks Hidden Knowledge": https://www.serviceinnovation.org/kcs-unlocks-hidden-knowledge/ (found in search; not opened).
- Library course: [*Running IT as a Business*, lesson 2.1 — Digital products, services and projects: what each is and who owns it](../itbiz/index.html#/2.1) (the manager's view of products and services).
- Library course: [*SaaS Building Blocks*, lesson 7.1 — The admin panel: support tools and impersonation](../saas/index.html#/7.1) (building safe support tools).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 5.2 — Support at one-person scale with AI: boundaries, escalation, disclosure](../founder/index.html#/5.2) (AI in support, at small scale).

---

# 7.2 — Requests, changes and the service desk in a growing company
*Level: 🟡 Intermediate* · *Prerequisites: 3.3, 7.1* · *Step: Operate*

**After this you can** sort incoming work into questions, service requests, incidents, changes and ideas, set a priority from impact and urgency, write a request catalogue entry with its steps and target time, and choose the right route (standard, normal or emergency) for a change to the live system, including a one-off data fix. *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- Work arrives in different kinds: a **question** (how do I…?), a **service request** (please do a standard thing for me), an **incident** (something is broken), a **change** (we want to alter the live system) and an **idea** (could the product do…?). Each kind needs a different route.
- A **service desk** is the one front door where these arrive, get recorded as **tickets**, are sorted and are tracked until done.
- **Priority** comes from **impact** (how many are affected, how badly) and **urgency** (how fast harm grows), not from who shouts loudest.
- A **request catalogue** lists the standard things people can ask for, with a form, any approval, the steps and a target time. Frequent, simple requests become self-service.
- The rule that matters most: **every change to the live system, including data, goes through a known route that leaves a record.**
- Biggest trap: "just quickly" changing production by hand because a customer is waiting.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

On a Wednesday afternoon a sales colleague messaged Yasmin: a large merchant had been promised a lower delivery fee from today, the change was not in the app, and could she "just update the number in the database"? Yasmin had production read access for debugging, and a senior engineer had shown her where fees were stored. It would take one line.

She paused and asked Salma. Salma pointed her to an incident from two months earlier. Faisal had fixed a courier's region directly in the database to help a merchant quickly. The fix used the wrong region code. For three days that courier received no offers, and nobody linked it to the manual change because there was no record of it. The courier lost three days of earnings; support spent hours on it.

At forty people, things arrive at Qafila from every direction: chat, email, sales, the payments provider, colleagues in the corridor. Some are questions, some are standard requests, some are urgent faults, some are changes to the live system, and some are ideas for the roadmap. When all of them arrive the same way and are handled the same way, urgent things wait, ideas get built without a decision, and risky changes happen with no record. This lesson sorts the work and gives each kind a route.

## 📐 How it works

### 🟢 The essentials

**Five kinds of incoming work.**

| Kind | Plain meaning | Qafila example | Route |
|---|---|---|---|
| **Question** | Someone needs information | "How do I export my deliveries?" | Answer from the knowledge base (lesson 7.1) |
| **Service request** | A standard, expected ask with known steps | "Add a staff account", "set up a new branch", "invoice copy" | Request catalogue entry |
| **Incident** | Something is broken or about to be | "No courier offers in one city since 10:00" | Incident process (lesson 4.3) |
| **Change** | A deliberate alteration to the live system: code, configuration, infrastructure or data | "Apply the agreed fee for one merchant", "raise a rate limit" | Change route (below) |
| **Idea** | A wish for the product to do something new | "Could merchants schedule deliveries a week ahead?" | Product backlog, decided by the product manager (Module 6) |

A single message can contain several kinds ("tracking is broken and also can you add my branch?"). Split it into separate tickets.

Many companies use words like these; they are common across service management practice. The best-known source of this vocabulary is **ITIL®**, a widely used body of service management guidance now owned by PeopleCert (as reported from search summaries; the owner writes it as ITIL®). This course does not follow ITIL's structure; it uses the ideas in plain words. For more, see the owner's site and lesson 12.3.

**The service desk and tickets.** A **service desk** is the single place where work comes in and is tracked. A **ticket** is the record of one piece of work: who asked, what kind it is, the reason, the priority, who owns it now, what has been done, and when it closed. One front door does not mean one channel; it means every channel ends in the same queue. For the manager's view of intake, see [*Running IT as a Business*, lesson 4.1 — Intake and demand management: one front door for ideas and requests](../itbiz/index.html#/4.1).

**Priority from impact and urgency.** Agree a small matrix in advance:

| | **Urgency high** (harm grows by the hour) | **Urgency low** (can wait days) |
|---|---|---|
| **Impact high** (many customers, or money or safety) | P1 | P2 |
| **Impact low** (one customer, small effect) | P2 | P3 |

A big merchant shouting is not high impact by itself; a hundred small merchants who cannot get couriers is. Write the definitions down with examples, like the severity scale in lesson 4.3. Incidents use the severity scale; the matrix sets the queue order for everything else.

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

The catalogue does three things. Agents follow the same steps, so results are consistent. Customers know what to expect. And the team can see which requests are frequent and simple enough to automate or turn into **self-service** (the customer does it in the product, with no ticket). A good order for automation is: frequent, simple, low-risk first. For the manager's view, see [*Running IT as a Business*, lesson 7.1 — Request fulfilment and self-service](../itbiz/index.html#/7.1).

**Access requests are requests too.** "Give me production access", "add me to the payments dashboard": these are service requests with an approval step by the owner of the system, a reason and, ideally, an end date. Give the least access that does the job. Remove access when people change roles. Dana will tighten this at Scale-up (Module 11), but the habit starts here.

**Three routes for a change.** A **change** is any deliberate alteration to the live system. Changes vary hugely in risk, so they need different routes:

| Route | When | Qafila example | What it needs |
|---|---|---|---|
| **Standard change** | Low risk, done often, with a proven procedure | Daily code deploy through the pipeline; adding a delivery zone with the admin tool | The procedure itself is the approval: tests, review, pipeline record (lesson 3.3) |
| **Normal change** | Not routine, or higher risk | A database migration on the orders table; changing the payment provider's settings | Written plan, second reviewer from the owning team, rollback plan, agreed time window |
| **Emergency change** | Needed now to stop or prevent an incident | Turning off a broken feature flag during an incident | Incident lead's agreement at the time; record and review afterwards |

Most of Qafila's changes should be standard: small, tested, reviewed in a pull request and deployed by the pipeline, which leaves a record automatically. The aim is to make the safe route the easy route.

**Data fixes are changes.** Changing a value in the production database (a fee, a region, an order status) is a change to the live system, even though no code ships. The safe route: write the change as a script, have a second person review it, run it through a tool that logs who ran what and when, check the result, and link it to the ticket. If a data fix is needed often, that is a sign the admin tool is missing a feature.

### 🔴 Expert view

**Approval that helps, and approval that only slows.** It is tempting to add a meeting where a group of senior people approve every change. DORA (DevOps Research and Assessment, a research programme now part of Google Cloud) reports on its capability page on streamlining change approval that heavyweight approval by an external body, such as a change advisory board or a senior manager, was found to have a negative effect on software delivery performance, with no evidence that it lowered change failure rates; it recommends peer review during development, supported by automation (as reported from search summaries; the page could not be opened from this environment). The practical lesson is not "no approval". It is: put the check close to the work, done by people who understand it, recorded automatically. For how a larger organisation balances this, see [*Running IT as a Business*, lesson 6.2 — Change control that protects stability without stopping flow](../itbiz/index.html#/6.2).

**Measuring the desk without gaming it.** Useful measures: volume by kind and reason, time to first response, time to resolve by priority, how many tickets are reopened, and the age of the oldest open tickets. Watch for distortions. If agents are judged only on closing quickly, tickets get closed before the problem is solved and reopened later; if they are judged only on volume, hard problems get passed around. Look at several measures together, and read a sample of tickets every month.

**When the desk sees an incident first.** Often the desk notices a pattern before monitoring does: five merchants in ten minutes report the same thing. Give the desk a clear rule: three or more contacts with the same symptom within a short window (illustrative) means "tell the on-call engineer now", using the incident route from lesson 4.3. The desk is part of your monitoring.

**The memorable rule.** Every change to the live system, including data, goes through a known route that leaves a record.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Work-kind guide** | One page defining question, request, incident, change and idea, with examples and routes | Training new agents and engineers; sorting a mixed message |
| **Priority matrix** | Impact × urgency → P1–P3, with written examples | Every ticket that is not an incident |
| **Request catalogue** | Standard requests with who can ask, information, approval, steps, owner, target time, self-service plan | When the same request arrives more than a few times |
| **Change route card** | Standard, normal and emergency changes: criteria and what each needs | Before any change to code, configuration, infrastructure or data |
| **Data-fix procedure** | Script, second reviewer, logged run, result check, link to ticket | Any manual change to production data |
| **Desk measures sheet** | Volume by kind, first response, resolve time by priority, reopen rate, oldest open | Weekly desk review |

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
> **Change rule v1.** Code and infrastructure: standard route through pull request and pipeline. Orders and payments schema changes: normal route, second reviewer from the owning team, rollback plan, outside 11:00–14:00 and 18:00–21:00. Production data: never by hand; data-fix procedure, linked to a ticket. Emergencies: the incident lead decides, the change is recorded in the incident timeline and reviewed afterwards.

The fee for the large merchant went through the new "merchant-specific delivery fee" entry. Bilal found the signed agreement set the new fee from the first of next month, not today. Faisal added a "fees" screen to the admin tool so fee changes no longer needed a script; Yasmin wrote the tests for it as her first change to the payments area.

## 🛠️ Exercises
**🟢 Sort the queue.** Classify each fictional message as question, service request, incident, change or idea, and give a priority (P1–P3) to the non-incidents using the matrix: (a) "Can I get a copy of my March invoice?"; (b) "None of my couriers in the north zone have had offers for 20 minutes"; (c) "Could the app let me set delivery slots?"; (d) "Please raise the rate limit for our partner's order API from tomorrow"; (e) "How do I change my shop logo?"; (f) "I need a staff account for my new cashier today, she starts at 4 pm".
*Done when:* each message has one kind, each non-incident has a priority with a one-line reason, and the incident is sent to the incident route.

<details><summary>Model answer and self-check</summary>

**Model answer.** (a) Service request, P3. (b) Incident: incident route and severity scale (likely SEV2, one zone degraded). (c) Idea: product backlog, no ticket priority. (d) Change: normal route (configuration affecting a partner), P2 because it is needed tomorrow. (e) Question: knowledge article, P3. (f) Service request, P2: low impact (one merchant) but urgent (needed this afternoon).

**Self-check.**
- Did you keep the idea out of the desk's queue and send it to the product manager?
- Did urgency, not the customer's tone, decide (f)?
- Did you recognise (d) as a change even though it sounds like a request?

</details>

**🟡 Write a catalogue entry.** Choose a standard request from your own life or project (getting access to a shared drive, joining a club's chat group, requesting a reference letter) or Qafila's "staff account for a merchant". Write a full catalogue entry with every field in this lesson, and say whether and how it could become self-service.
*Done when:* the entry names who can ask, the information needed, the approval (or "none" with the reason), numbered steps, who does it, a target time labelled illustrative, and a self-service decision.

<details><summary>Model answer and self-check</summary>

**Model answer.** "Join the project's maintainers' chat". Who can ask: contributors with at least one merged pull request. Information: chat username, link to merged pull request. Approval: one existing maintainer. Steps: 1. Check the pull request is merged. 2. Maintainer approves in the request thread. 3. Send invitation. 4. Add name to the members list. Who: any maintainer. Target: within three days (illustrative). Self-service: not yet; the approval needs judgement about the person, so keep it manual but automate the pull-request check.

**Self-check.**
- Is every step an action someone can do, not "handle request"?
- Did you avoid an approval that adds waiting without adding judgement?
- If you proposed self-service, did you keep any check that matters?

</details>

**🔴 Turn a risky habit into a route.** Faisal's manual region change caused a three-day problem for a courier. Write (1) a data-fix procedure Qafila could use from tomorrow, and (2) a short proposal for removing the need for most data fixes. Use the change routes in this lesson.
*Done when:* the procedure has a script, a second reviewer, a logged run, a result check and a ticket link; the proposal names the two or three most frequent data fixes and the admin-tool feature or product change that would replace each.

<details><summary>Model answer and self-check</summary>

**Model answer.** (1) Procedure: open a ticket with the reason; write the change as a script that prints the before and after values; a second engineer from the owning team reviews it; run it through the logged job runner (not a personal session); check the affected record and the customer's view; paste the output into the ticket. (2) Proposal: the most frequent fixes are courier region changes, merchant fees and stuck order statuses. Replace them with an admin-tool screen for regions with a list of valid codes, the fees screen with a start date, and a "release stuck order" action with a reason field. Each is logged and needs no database access.

**Self-check.**
- Would your procedure have caught the wrong region code (a review or a validation step)?
- Is there a record someone could find three days later when the courier complains?
- Did your proposal reduce the need for manual fixes, not just make them more formal?

</details>

## ⚠️ Mistakes and traps
- **One queue, one treatment for everything.** Sort by kind first; questions, requests, incidents, changes and ideas need different routes.
- **"Just quickly" in production.** Manual changes without a record are the hardest problems to trace. Use the data-fix procedure, then build the admin feature.
- **Priority by volume of complaint.** A loud customer is not high impact by definition. Use the written matrix.
- **A change board for everything.** Heavy approval of routine changes slows delivery without making it safer. Make routine changes standard, with checks built into the pipeline.
- **Ideas entering through the desk.** A feature request is not a ticket to build. Send it to the product manager with the customer's words.
- **Judging agents only on closing speed.** Pair it with reopen rate and a monthly read of real tickets.

## 🧾 Recap
- Incoming work comes in five kinds: questions, service requests, incidents, changes and ideas; each has its own route.
- A service desk is one front door with tickets; priority comes from impact and urgency, agreed in advance.
- A request catalogue makes standard requests consistent and shows which ones to automate or turn into self-service.
- Changes take a standard, normal or emergency route; data fixes are changes too.
- Rule: every change to the live system, including data, goes through a known route that leaves a record.

## ✍️ Check yourself
**1. A sales colleague asks Yasmin to update a merchant's fee directly in the production database. What should she do?**

- A. Make the update, since she has database access and the merchant has been promised the fee today.
- B. Route it as a change through the agreed request entry, with the signed agreement and a logged record.
- C. Refuse and tell sales that fees can only be changed after the next quarterly pricing review.
- D. Ask the senior engineer who showed her the table to make the change instead, to save time.

<details><summary>Answer</summary>

**B.** A fee change is a change to live data and needs a known route with evidence and a record. A and D are the same manual, unrecorded change (D only moves who does it), and C invents a rule that blocks legitimate work. See "Data fixes are changes" and "In practice at Qafila".

</details>

**2. "None of my couriers in the north zone have had offers for 20 minutes." What kind of work is this?**

- A. A service request, because the merchant is asking Qafila to do something for them quickly.
- B. A question, because the merchant needs information about the state of their deliveries.
- C. An idea, because it suggests that offers in the north zone need a better design next quarter.
- D. An incident, because a core journey is not working and harm grows while it continues.

<details><summary>Answer</summary>

**D.** Something is broken now and the harm grows with time, so it goes to the incident route. A and B treat it as routine and would put it in a queue, and C turns a live fault into a future plan. See "Five kinds of incoming work".

</details>

**3. Which change is the best candidate for the standard route?**

- A. A small code change, tested and reviewed in a pull request, deployed by the usual pipeline.
- B. A one-off migration that reorganises how orders are stored in the production database.
- C. Switching all merchants to a new payment provider configuration during the evening peak.
- D. A manual edit of a courier's region code in the database, done to help a merchant quickly.

<details><summary>Answer</summary>

**A.** Standard changes are low risk, frequent and follow a proven procedure that is itself the approval. B and C are higher risk and need the normal route with a plan and rollback, and D is the unrecorded manual change this lesson warns against. See "Three routes for a change".

</details>

**4. Faisal proposes that a weekly meeting of senior staff approve every change. What does the DORA material cited in this lesson suggest?**

- A. It suggests that weekly external approval makes failures rarer, so the meeting should approve every change.
- B. It suggests that approval should be removed entirely, because any form of review slows delivery down.
- C. Heavyweight external approval was found to hurt delivery performance; peer review with automation is advised.
- D. It suggests that approval meetings are fine as long as they happen daily instead of once a week.

<details><summary>Answer</summary>

**C.** As reported, DORA found heavyweight external approval had a negative effect on delivery performance without evidence of lower failure rates, and recommends peer review supported by automation. A states the opposite, B goes too far (review stays, closer to the work), and D changes the frequency but not the problem. See "Approval that helps, and approval that only slows".

</details>

**5. Salma wants to choose which service requests to automate first. Which choice fits this lesson?**

- A. The rarest requests, because they are the ones agents are least practised at handling well.
- B. The requests with the most senior approvers, because automation removes the approval step.
- C. The requests that sales teams ask for most, because they are closest to new revenue.
- D. Frequent, simple, low-risk requests such as invoice copies, which can become self-service.

<details><summary>Answer</summary>

**D.** Frequent, simple and low-risk requests give the biggest gain for the least risk. A gives little gain, B removes judgement where it may matter, and C picks by who asks rather than by volume and risk. See "The request catalogue".

</details>

## 📚 References
- DORA, "Capabilities: Streamlining change approval": https://dora.dev/capabilities/streamlining-change-approval/ — source of the finding on external change approval (could not be opened from this environment; content as reported in search summaries).
- DORA, 2019 Accelerate State of DevOps Report: https://dora.dev/research/2019/dora-report/ — recommends moving from heavyweight external approvals to peer review with automation (as reported in search summaries; not opened).
- PeopleCert, "PeopleCert completes Axelos acquisition": https://www.peoplecert.org/news-and-announcements/peoplecert-completes-axelos-acquisition — ITIL's owner (as reported in search summaries; not opened).
- Library course: [*Running IT as a Business*, lesson 4.1 — Intake and demand management: one front door for ideas and requests](../itbiz/index.html#/4.1).
- Library course: [*Running IT as a Business*, lesson 7.1 — Request fulfilment and self-service](../itbiz/index.html#/7.1).
- Library course: [*Running IT as a Business*, lesson 6.2 — Change control that protects stability without stopping flow](../itbiz/index.html#/6.2).

---

# 7.3 — Service levels and talking to customers when things go wrong
*Level: 🟡 Intermediate* · *Prerequisites: 4.3, 7.1, 7.2* · *Step: Operate*

**After this you can** write a service-level sheet for one journey (indicator, internal target, error budget in minutes, budget policy), explain why a written promise to customers should be looser than the internal target and what questions to ask before signing one, and write the first message, an update and a closing note for a customer-facing incident. *Study time: reading about 25 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- A **service level** is how well a service performs, stated in numbers: how available, how fast, how quickly support answers.
- Inside the company, set **service level objectives (SLOs)**: targets for indicators customers feel. Qafila's target for order tracking, from Growth on, is **99.9% monthly**, which allows about 43 minutes of bad time in a 30-day month.
- Outside, a **service level agreement (SLA)** is a promise in a contract, often with consequences such as service credits. Promise less than you aim for, so trouble shows before a promise breaks.
- When things go wrong, customers need to hear from you early, in plain words, at a known rhythm, with what to do now.
- The rule that matters most: **promise in writing only what you measure, can usually beat, and can explain.**
- Biggest trap: a salesperson promising "99.99% uptime" in an email because it sounds reassuring.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

At Growth, Qafila signed its largest customer so far: a chain of pharmacies with dozens of branches. Their procurement team sent a contract draft asking for "99.99% availability, a 15-minute response to all support requests, 24 hours a day, and full refund of the monthly fee for any breach". The sales lead had already written back "no problem".

Two weeks later, on a Thursday evening, a faulty release froze order tracking for merchants in one city and delayed courier offers there by about fifty minutes. Monitoring caught it; the on-call engineer rolled back. But the first message to merchants went out an hour after the problem began, it said "technical issue, we are investigating", and it gave no next update time. Support received hundreds of contacts. The pharmacy chain's operations manager asked, reasonably, how that matched "99.99%".

Salma, now Qafila's service and reliability lead, did the arithmetic for Maha. In a 30-day month, 99.99% allows about four minutes of bad time. Qafila's own internal target for order tracking was 99.9%, about 43 minutes, and that evening alone had used more than the whole month. The contract as drafted would have been broken in its first fortnight. This lesson covers setting service levels you can keep, promising customers less than you aim for, and talking to customers so that a bad evening does not become a lost customer.

## 📐 How it works

### 🟢 The essentials

**Three terms, briefly.** Lesson 4.3 introduced them, using the definitions in Google's *Site Reliability Engineering* book (as reported from summaries of its chapter on service level objectives):

| Term | Plain meaning | Who sees it |
|---|---|---|
| **Service level indicator (SLI)** | A carefully defined measure of some part of the service, usually good events ÷ all events | The team, on dashboards |
| **Service level objective (SLO)** | The target for an SLI over a period | The team and company; the basis for decisions |
| **Service level agreement (SLA)** | A promise to a customer, usually in a contract, often with a consequence if it is missed | The customer, lawyers, finance |

**Choose indicators customers feel.** "Server CPU below 80%" is not a service level; merchants do not feel CPU. Choose indicators from the customer's journey:

| Journey | Indicator (illustrative definition) |
|---|---|
| **Order tracking** | Share of minutes in which merchants can see the current status of their orders |
| **Courier offers** | Share of orders that get a courier offer within 3 minutes |
| **Support** | Share of chat contacts that get a first human reply within 10 minutes during opening hours |

Support is part of the service, so it can have service levels too: first response time and resolution time, set per priority (lesson 7.2), not one number for everything.

**The error budget, again.** The error budget is 100% minus the target. For Qafila's order-tracking SLO of 99.9% monthly:

| Month length | Minutes in the month | Allowed bad minutes at 99.9% |
|---|---|---|
| 30 days | 43,200 | 43.2 (about 43) |
| 31 days | 44,640 | 44.6 (about 45) |

The fifty minutes of frozen tracking on that Thursday used more than a whole 30-day month's budget in one evening. That number, not anyone's feelings, is what started the conversation about release safety.

**SLA looser than SLO.** If the internal target is 99.9%, the contractual promise should be lower, for example 99.5%, so the team sees the problem and acts long before the customer is owed anything. Google's SRE material makes the same point: an SLO stricter than any SLA gives a safety margin (as reported from summaries). A promise stricter than your own target is a promise you plan to break.

### 🟡 Going deeper

**What a written promise must define.** An SLA is a contract, and contracts and consumer protection rules differ by country, so a lawyer must review it; this lesson does not give legal advice. Practitioners should still make sure the draft answers these questions before anyone signs:

| Question | Why it matters |
|---|---|
| **What exactly is measured?** | "Availability" of what: the whole app, order tracking, the API? |
| **How, and by whom?** | Your monitoring, the customer's, or an agreed third source? |
| **Over what period?** | Monthly is usual; weekly is harsher; yearly hides bad months |
| **What is excluded?** | Announced maintenance windows, the customer's own systems, failures of their network |
| **What are the consequences?** | Service credits (a discount on a later bill) are common; refunds or termination rights are heavier |
| **How is it reported?** | Monthly report, who sends it, and how disputes are handled |
| **Can we measure it today?** | If not, you cannot know whether you kept it |

**Your promise depends on your suppliers.** Qafila's payments go through a payment provider. If order completion needs both Qafila's service and the provider's, and each is available 99.9% of the time independently, the chance both are working is about 0.999 × 0.999 ≈ 0.998, or 99.8%. A promise above that, for a journey that needs the provider, is not one you control. Read your suppliers' terms before you write your own (Module 10 covers supplier contracts).

**The error budget policy.** A **budget policy** says in advance what happens as the budget is used: for example, at half spent, the owning team reviews recent changes; when fully spent, only reliability fixes and low-risk changes ship until the journey is back within target, and the product manager agrees which roadmap items move. Google's SRE Workbook publishes an example error budget policy in an appendix (as reported from search summaries). Agree yours with product, engineering and support before you need it.

**Talking to customers when things go wrong.** Silence is worse than bad news. A good incident message:

1. **Says what is happening, in the customer's terms.** "Courier offers in the central zone are delayed by up to 50 minutes", not "degraded performance in the dispatch service".
2. **Says who is affected,** so unaffected merchants can relax.
3. **Says what to do now,** if anything ("orders placed now are still saved; you can call your regular courier for urgent deliveries").
4. **Says when the next update is,** and keeps that promise even if there is no news.
5. **Avoids guessing the cause** and avoids blaming a supplier publicly before you know.

Send it through the channels customers already watch: an in-app banner, a **status page** (a public or customer-only page showing current service health and incident updates), and, for large customers, a direct message from their contact. Qafila's merchants work in Arabic and English, so templates exist in both, written in advance.

**After the incident.** Within an agreed time, send a short closing note: what happened in plain words, how long, who was affected, what you are changing so it is less likely to happen again, and how to get help with any lasting effect (late deliveries, refunds). The internal post-incident review (lesson 4.3) feeds it, but the note is written for customers, without internal blame or jargon. For more on wording, see [*Founder's Playbook for AI-First Builders*, lesson 5.3 — When something breaks: telling customers, and the post-incident note](../founder/index.html#/5.3).

### 🔴 Expert view

**Too reliable can be a problem.** If a service is much more reliable than its stated target for a long time, the people who depend on it start to assume it never fails and build that assumption in. Google's SRE book describes this with its Chubby lock service, where planned outages were used so that users would not depend on more availability than was promised (as reported from summaries of the chapter). The lesson for Qafila is milder: publish the real target, and design partner integrations to cope with short failures.

**Green reports, unhappy customers.** A report can show every SLA met while customers are unhappy, because the measure is too narrow ("the API answered" while couriers got no offers) or averages hide a bad hour. Check service levels against contact reasons (lesson 7.1) and customer feedback each month. If they disagree, the indicator is probably wrong.

**Service reviews with large customers.** For the biggest merchants, hold a short monthly or quarterly review: service levels achieved, incidents and what changed, top contact reasons from their branches, upcoming changes that will affect them. It turns the SLA from a stick into a shared picture.

**Compensation is a decision, not a reflex.** Decide in advance who may offer credits or goodwill gestures, within what limits, and how they are recorded and approved by finance. Bilal's concern is reasonable: inconsistent, unrecorded promises cost money and fairness. For the management view of service levels, see [*Running IT as a Business*, lesson 8.3 — Service levels, SLOs and error budgets as a management tool](../itbiz/index.html#/8.3); for engineering depth, [*Cloud & DevOps: Zero to Hero*, lesson 5.2 — SLOs, error budgets, alerting and on-call that people can sustain](../cloud/index.html#/5.2).

**The memorable rule.** Promise in writing only what you measure, can usually beat, and can explain.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Service-level sheet** | Per journey: SLI definition, SLO and period, error budget in minutes, data source, owner | For every journey customers depend on |
| **Error budget policy** | What happens at half and full budget spent, and who decides | Agreed before the first budget runs out |
| **SLA question list** | What is measured, how, period, exclusions, consequences, reporting, can we measure it | Before any customer contract mentions service levels; with legal review |
| **Incident message kit** | First message, update and closing note templates in each customer language, with the update rhythm | Written in advance; used in every customer-facing incident |
| **Status page** | A page showing current health and incident updates (hosted products exist; examples, not endorsements) | Once customers are too many to message one by one |
| **Service review pack** | Levels achieved, incidents, contact reasons, upcoming changes | Monthly or quarterly with large customers |

## 🏛️ In practice at Qafila
After the Thursday evening, Salma and Yasmin prepare the service-level sheet for order tracking and the incident message kit; Aisha, Faisal and Bilal agree the budget policy; Maha takes the SLA answer to the pharmacy chain with a lawyer's review. Illustrative and fictional.

> **Service-level sheet: order tracking (Growth)**
>
> | Item | Value |
> |---|---|
> | SLI | Share of minutes in which a test merchant account and real merchant requests can load current order status within 2 seconds |
> | SLO | 99.9% per calendar month |
> | Error budget | About 43 minutes (30-day month), about 45 (31-day month) |
> | Data source | Synthetic check every minute plus request logs; dashboard owned by Salma |
> | Budget policy | Half spent: owning team reviews the month's changes. Fully spent: reliability work and low-risk changes only until back within target; Aisha re-plans the roadmap |
>
> **Offer to the pharmacy chain (draft, for legal review).** Order tracking 99.5% monthly, measured by Qafila's monitoring, report sent monthly; announced maintenance excluded (at most twice a month, outside 07:00–23:00, notice 3 days ahead); service credit of a stated percentage of the monthly fee per band missed. Support: first reply within 15 minutes for P1 issues around the clock; 2 working hours for P2; 1 working day for P3. Monthly service review with their operations manager.
>
> **First message template (English; Arabic version alongside).** "We are seeing [problem in customer words] affecting [who]. [What to do now.] Orders you place are [saved / not affected]. Next update by [time]."

Bilal asked where the credit percentage came from; nobody knew yet, so the draft left it blank for finance and the lawyer. Faisal wanted to offer 99.9% "because that is our target". Salma showed him the arithmetic for two services in a chain and the fifty-minute evening; he agreed the margin was the point. The pharmacy chain accepted 99.5% with a monthly review. Yasmin rewrote the Thursday message using the template; the new version was half as long and said what merchants could do.

## 🛠️ Exercises
**🟢 Work out the budgets.** For Qafila's journeys, calculate the allowed bad minutes in a 30-day month at each target, and say which incident would exhaust each: targets (a) order tracking 99.9%, (b) courier offers 99.5%, (c) merchant reports 99%. Incidents: (1) 50 minutes of delayed offers; (2) 3 hours of reports not loading; (3) 20 minutes of tracking down.
*Done when:* each target has its minutes shown with the calculation, and for each incident you say what share of the relevant budget it used.

<details><summary>Model answer and self-check</summary>

**Model answer.** 43,200 minutes in a 30-day month. (a) 0.1% → 43.2 minutes. (b) 0.5% → 216 minutes. (c) 1% → 432 minutes. (1) Offers: 50 of 216 minutes, about 23%. (2) Reports: 180 of 432 minutes, about 42%. (3) Tracking: 20 of 43.2 minutes, about 46%. None alone exhausts its budget, but incident 3 is the most serious in budget terms even though it was the shortest.

**Self-check.**
- Did you use the minutes in the month, not hours or a year?
- Did you notice that the same length of outage matters more on a stricter target?
- Would you raise incident 3 with the owning team at the next review because nearly half the budget is gone?

</details>

**🟡 Review an SLA draft.** Take the pharmacy chain's first request from this lesson ("99.99% availability, a 15-minute response to all support requests, 24 hours a day, full refund of the monthly fee for any breach"). Using the SLA question list, write the questions you would raise and a counter-offer with reasons. Do not state any legal conclusion.
*Done when:* you raise at least five questions from the list, the counter-offer sets an availability below Qafila's internal target, sets support times by priority, and marks what needs legal and finance review.

<details><summary>Model answer and self-check</summary>

**Model answer.** Questions: availability of what (whole app, tracking, API)? Measured by whose monitoring? Monthly or another period? Are announced maintenance and the payment provider's failures excluded? What counts as "support request" and "response"? Is a full refund proportionate, and what does the lawyer advise? Can we measure every term today? Counter-offer: order tracking 99.5% monthly (internal target 99.9%; 99.99% allows about 4 minutes a month, which we cannot honestly promise); P1 15 minutes around the clock, P2 2 working hours, P3 1 working day; service credits instead of refunds, amounts for finance and legal; monthly report and review.

**Self-check.**
- Did you show the arithmetic for 99.99%, so the conversation is about numbers, not mood?
- Did you avoid saying what the law requires, and send that question to a lawyer instead?
- Is every promise in your counter-offer something Qafila measures today?

</details>

**🔴 Write the message kit and replay the Thursday evening.** Write the first message, one update and the closing note for the fifty-minute courier-offer delay, using the five points in this lesson. Then write a one-paragraph comparison with the original message ("technical issue, we are investigating"), and propose the update rhythm and who sends what.
*Done when:* the first message names the problem in customer words, who is affected, what to do now and the next update time; the closing note says what happened, how long, who was affected, what will change and how to get help; and the rhythm names roles, not people.

<details><summary>Model answer and self-check</summary>

**Model answer.** First message (19:15): "Order tracking in the central zone is not updating, and courier offers there are delayed by up to 45 minutes. Merchants in other cities are not affected. Orders you place are saved and will be offered to couriers; for urgent deliveries you may use your own courier. Next update by 19:45." Update (19:45): "We have reversed a change made earlier this evening and offers are returning to normal. We are checking that waiting orders are being offered. Next update by 20:15." Closing note (next day): "Yesterday from about 18:50 to 19:40, a change to our app delayed courier offers in the central zone by up to 50 minutes. About [n] merchants were affected. We have reversed the change and will now release such changes to a small share of orders first and check offer times before releasing further. If an order was late and a customer complained, reply to this message and our team will help." Comparison: the original gave no impact, no action and no next time, so merchants contacted support instead. Rhythm: incident communications role sends banner and status page within 30 minutes, then every 30 minutes; account manager messages large customers directly; support lead sends the closing note within one working day.

**Self-check.**
- Did the first message go out within the agreed time, even without knowing the cause?
- Did any message blame a person or a supplier?
- Did the closing note promise a specific change, not "we will be more careful"?

</details>

## ⚠️ Mistakes and traps
- **Promising what you aim for.** If the SLA equals or beats the SLO, any bad month becomes a breach. Keep a margin.
- **Indicators customers do not feel.** CPU and server uptime miss what merchants experience. Measure journeys.
- **Ignoring suppliers.** Your promise cannot be stronger than the chain it depends on. Do the multiplication.
- **"Technical issue, investigating."** Say what is affected, who, what to do and when you will update.
- **Compensation by whoever is on the phone.** Decide who may offer what, within limits, and record it.
- **Signing without a lawyer.** Practitioners shape the numbers; legal and finance review the contract.

## 🧾 Recap
- Service levels describe in numbers how well the service works; SLIs measure, SLOs set internal targets, SLAs make promises to customers.
- Qafila's order-tracking SLO from Growth on is 99.9% monthly, about 43 minutes of budget in a 30-day month.
- Promise less than you aim for, define exactly what is measured and excluded, and check what your suppliers promise you.
- In an incident, tell customers early, in their words, with what to do now and a next update time; close with a plain-language note.
- Rule: promise in writing only what you measure, can usually beat, and can explain.

## ✍️ Check yourself
**1. Qafila's internal target for order tracking is 99.9% monthly. What should the contractual promise to the pharmacy chain be?**

- A. 99.99%, because a stricter promise reassures the customer that Qafila takes reliability seriously.
- B. 99.9%, exactly the internal target, so that the team and the customer share a single number.
- C. 100%, with exclusions for maintenance, because customers expect a service that never fails.
- D. A lower figure such as 99.5%, so the team sees trouble and acts before any promise is broken.

<details><summary>Answer</summary>

**D.** An SLA looser than the SLO gives a safety margin. A promises about four minutes a month, which Qafila cannot keep, B turns every bad month into a breach, and C is a promise no service can keep. See "SLA looser than SLO".

</details>

**2. How many minutes of bad time does a 99.9% monthly target allow in a 30-day month?**

- A. About 4 minutes, because 0.1% of a day is roughly that much.
- B. About 43 minutes, because 0.1% of 43,200 minutes is 43.2.
- C. About 7 hours, because 0.1% of a month is close to a full shift.
- D. About 432 minutes, because each day has a 14-minute allowance.

<details><summary>Answer</summary>

**B.** 30 × 24 × 60 = 43,200 minutes, and 0.1% of that is 43.2. A is roughly the 99.99% figure, C is roughly the 99% figure, and D is the 99% figure with an invented daily split. See "The error budget, again".

</details>

**3. Order completion needs both Qafila's service and the payment provider, each independently available 99.9% of the time. About how available is the journey?**

- A. 99.9%, because the weaker of the two services sets the level for the journey.
- B. 99.95%, because two independent services back each other up during failures.
- C. 99.8%, because both must work at once: 0.999 × 0.999 is about 0.998.
- D. 99.0%, because each extra dependency removes about one percentage point.

<details><summary>Answer</summary>

**C.** When a journey needs two services in a chain, their availabilities multiply. A ignores the second service's failures, B treats a chain as if it were a backup, and D uses an invented rule. See "Your promise depends on your suppliers".

</details>

**4. Courier offers are delayed in one city. Which first message to merchants is best?**

- A. "Courier offers in the central zone are delayed up to 50 min; other cities fine; orders are saved; next update 19:45."
- B. "We are currently experiencing a technical issue and our engineers are investigating it as a priority."
- C. "A faulty change by our dispatch team has delayed offers; we apologise and are fixing it right now."
- D. "Our payment provider appears to be having problems; offers may be slow until they resolve the issue."

<details><summary>Answer</summary>

**A.** It names the problem in customer terms, who is affected, what is safe and when the next update comes. B is the original vague message, C blames a team, and D guesses a cause and blames a supplier before anyone knows. See "Talking to customers when things go wrong".

</details>

**5. Every monthly report to the pharmacy chain shows the SLA met, but their branches keep complaining. What does this lesson suggest?**

- A. The complaints can be ignored, because the contract defines what good service means.
- B. The SLA should be tightened to 99.99%, so the report shows a more demanding target.
- C. Compare the indicator with contact reasons; it may be measuring too narrow a thing.
- D. Stop sending reports, since they are causing friction with the customer's managers.

<details><summary>Answer</summary>

**C.** Green reports with unhappy customers usually mean the indicator misses what customers feel or averages hide bad hours. A treats the contract as the whole truth, B changes the target without fixing the measure, and D hides the problem. See "Green reports, unhappy customers".

</details>

## 📚 References
- Google, *Site Reliability Engineering*, chapter 4, "Service Level Objectives": https://sre.google/sre-book/service-level-objectives/ — SLI, SLO and SLA definitions and the Chubby planned-outage example (could not be opened from this environment; content as reported in search summaries).
- Google, *The Site Reliability Workbook*, Appendix B, "Example Error Budget Policy": https://sre.google/workbook/error-budget-policy/ (as reported in search summaries; not opened).
- Google Cloud blog, "SRE fundamentals: SLIs, SLAs and SLOs" (2018): https://cloud.google.com/blog/products/devops-sre/sre-fundamentals-slis-slas-and-slos (found in search; not opened).
- Library course: [*Founder's Playbook for AI-First Builders*, lesson 5.3 — When something breaks: telling customers, and the post-incident note](../founder/index.html#/5.3).
- Library course: [*Running IT as a Business*, lesson 8.3 — Service levels, SLOs and error budgets as a management tool](../itbiz/index.html#/8.3).
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 5.2 — SLOs, error budgets, alerting and on-call that people can sustain](../cloud/index.html#/5.2).
