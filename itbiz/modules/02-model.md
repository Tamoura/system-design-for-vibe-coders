# Module 2 — Products, services and the operating model

*Module 1 showed that Najm Bank's Technology division cannot see value while its unit of management is a project that ends before value arrives. This module decides what the division manages instead, and who does the managing. First, three words used loosely in every bank, product, service and project, are pinned down, and each gets one accountable owner. Second, teams are arranged around those products: long-lived product teams, platform teams that serve them, and enabling teams that help and then move on, with clear rules for who decides what. Third, the division writes down what it actually offers in a service catalogue, in words the business and its own engineers recognise. Each lesson leaves an artefact: a product and service inventory with named owners and one product canvas, a team map with a decision-rights table, and catalogue entries that pass a test with real users.*

> **Steps:** Plan, Serve — decide what IT manages as products and services, who owns each one, how teams are arranged around them, and how the offer is shown to the people who use it.

---

# 2.1 — Digital products, services and projects: what each is and who owns it
*Level: 🟢 Beginner* · *Prerequisites: 1.1* · *Step: Plan, Serve*

**After this you can** sort ten to twenty items from your organisation's application list, project list and request forms into products, services, projects and components, name one accountable owner for each product and service, and write a one-page canvas for one product. *Study time: reading about 15 min, hands-on about 95 min (estimate).*

## ⚡ In 60 seconds
- A **digital product** is something people use (customers or colleagues) that the bank keeps changing for years, owned by a long-lived team and judged on outcomes, reliability and cost together.
- A **service** is the offer through which people get and use something: what they get, how to ask, what level of service to expect, what it costs and where to get help.
- A **project** is temporary work with a start, an end, a budget and a defined result. It is still the right tool for some work, and the wrong container for a product.
- The rule that matters most: **every product and every service has exactly one accountable name; every project has an end date.**
- Decision cue: call something a product only if users recognise it, you can measure what it changes, and one team could own most of it.
- Biggest trap: renaming the application list "the product list". About 420 applications are not 420 products, and a committee is not an owner.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

Omar asked a simple question at the monthly leadership meeting: "Who owns the cards app?" Reem said she owned the backlog for new features. Yousef said his operations centre owned it when it broke. Sami said his platform ran its pipelines. Tariq said its costs sat inside the "Digital Channels Programme", a project that had closed last year. Lina said the card-processing supplier owned the part that authorised payments. Nour said the risk register named "Head of Digital Channels", a role that no longer existed.

Then Omar asked what the cards app had cost last year and whether it was improving. Nobody could answer. Each slice was well managed, but the thing customers used had no owner. The same week, the head of SME banking complained that the service desk had eleven request forms with "payments" in the name, none saying what a new relationship manager would get. A missing **product** owner and a missing **service** are two faces of the same gap. This lesson names both, and separates them from **projects**.

## 📐 How it works

### 🟢 The essentials

**Three words, three jobs.** In this course:

| Term | Plain meaning | Judged on | Lifetime | Accountable person |
|---|---|---|---|---|
| **Digital product** | Something people use, which the bank keeps changing to improve outcomes | Outcomes, reliability, cost, risk | Years; ends only when retired | Product manager (or product owner) |
| **Service** | The offer through which people get and use something, with its terms | Whether people get what was promised, on the terms promised | As long as it is offered | Service owner |
| **Project** | Temporary work to produce a defined result by a date, within a budget | Result, date, budget | Months; ends by design | Project manager, with a sponsor |

The Project Management Institute describes a project in similar terms, as temporary work to create a unique product, service or result (as reported on its public pages). "Temporary" is the important word: a project is designed to end; a product is designed to keep going.

**How the three relate.** The Cards & Payments app is a **product**: the thing that is built, run and changed. "Card controls for retail customers" and "Test environment, small" are **services**: offers with terms. Moving the card-processing interface to a new supplier by a contract date could be a **project**; when it ends, the product carries on. One product can sit behind several services, and one service ("New employee setup") can draw on several products.

**Who is accountable for what.** The product manager is the one person who can give Omar a joined-up answer at any time: what the product is for, whether it is changing its outcomes, what comes next and why, how reliable it is, and what it costs. The service owner answers narrower questions: what people get, who may have it, how they ask, how long it takes and what it costs. The two can be the same person (Reem can own "Card controls" as a service) or different people (the service desk can own a request service).

**Accountable is not the same as responsible.** Many people are **responsible**: they do parts of the work. One person is **accountable**: they answer for the result and decide trade-offs. A steering group or a role title cannot be accountable, because it cannot be called at 2 a.m. or asked why a decision was made. Put a person's name and role title on every product and every service.

### 🟡 Going deeper

**Products are not applications.** Most banks keep an application list: every system IT installs, licenses or builds. Najm Bank's has about 420 entries. It is a list of **components**, the technical parts that run. A product usually spans several components, and some components serve many products.

| Item on the application list | A product? | Better description |
|---|---|---|
| Cards mobile front end | Not on its own | A component of Cards & Payments |
| Core banking system | Usually not | A shared component behind many products (see the expert view) |
| Corporate payments portal | Yes, with its interfaces and back-office tools | The Corporate Payments product |
| Internal developer platform | Yes | A platform product whose users are other teams (lesson 2.2) |
| Contract management tool (SaaS) | Yes, as a bought service with a bank owner | An enterprise service the bank configures but does not code |

A first product list for a division of Najm Bank's size might hold twenty to forty products. Each application is then mapped to the products it serves; lesson 9.1 makes that mapping a record with a short product identifier.

**Five tests for a product boundary.**

| Test | Question | Fails when |
|---|---|---|
| **Recognised** | Would users recognise it by name and say what it does for them? | Only engineers know the name ("ESB-2") |
| **Measurable** | Can you name an outcome it changes and measure it? | The only measures are uptime and tickets closed |
| **Ownable** | Could one team, perhaps with help, understand and change most of it? | Every change needs five teams to agree |
| **Releasable** | Can changes reach users without waiting for unrelated products? | It is always released with something else |
| **Costable** | Can most of its costs be attributed to it? | Costs are spread over many shared budget lines |

No boundary passes perfectly. A candidate failing three or more is usually too big (a "Digital Channels" product that is really six) or too small (a "card block screen" that is a feature).

**When a project is still the right tool.** Closing a data centre, switching card processor by a contract date, a one-off regulatory submission: genuinely temporary work suits a project. Two rules apply: every project names the products it changes, and their owners agree to receive what it leaves behind; when it ends, its knowledge and running costs go somewhere named. Funding is lesson 3.2.

### 🔴 Expert view

**Shared systems are the hard case.** Core banking, the payments switch and mainframe batch serve almost every product, and changing them is slow and risky. Banks usually mix three patterns:

| Pattern | How it works | Works when | Risk |
|---|---|---|---|
| **Platform product** | A team owns the system and offers it through clear interfaces and a catalogue (lesson 2.3) | It can be wrapped in stable interfaces | The team becomes a queue if interfaces are poor |
| **Specialist component team** | A few experts own the internals and work with product teams on changes | Expertise is scarce and change is rare | Every product waits for the same experts |
| **Supplier-owned, bank-governed** | The supplier owns the code; a bank owner manages contract, roadmap and service levels | It is a bought package | Change runs at the vendor's pace (lesson 10.2) |

Whatever the pattern, the shared system still needs one accountable name inside the bank.

**Owners need authority, not just a title.** Before naming owners, run an **ownership check**: can they decide the order of work within an agreed budget? Do they see the product's costs and incidents? Do they have a say in when changes go live? Three "no" answers make the owner a coordinator with a new title (decision rights: 2.2; funding: 3.2; owner records: 9.1). For the product manager's discovery work, see [*AI Product Management*, lesson 2.1 — Discovery for AI: jobs, workflows and where AI fits](../aipm/index.html#/2.1).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Product and service inventory** | Products, services and live projects, each with type, owner, role title and identifier; a spreadsheet will do | First artefact; review quarterly |
| **Product boundary test** | Five questions: recognised, measurable, ownable, releasable, costable | When drawing or redrawing a product's edges |
| **Application-to-product map** | Each application linked to the products it serves | After the first inventory, to find orphans and shared components |
| **Product canvas** | One page: purpose, users, outcomes, services, components, dependencies, owner, costs, top risks | For every product, before funding or a team change |
| **Ownership check** | Three questions on order of work, visibility of cost and incidents, and say in release timing | Before naming an owner, and a year later |

## 🏛️ In practice at Najm Bank
Fictional and illustrative. Huda ran a two-day sorting workshop with Reem, Yousef, Sami and Tariq. They produced a first inventory of 31 products and 58 services, and found 46 applications nobody could map to a product. Reem wrote the first canvas:

> **Product canvas: Cards & Payments (draft v1)**
>
> - **Identifier:** CARDS-PAY. **Owner:** Reem, Product Manager. **Kind:** customer-facing.
> - **Purpose:** let retail and SME customers manage cards and everyday payments themselves, safely, without calling the bank.
> - **Outcomes:** share of lost-card blocks done in the app; card calls to the contact centre per thousand customers; fraud losses on lost cards.
> - **Services:** card controls in the app (retail); card administration portal (SME); card controls, contact-centre view.
> - **Components:** cards mobile front end, card-limit rules engine, notification service, card-processor interface (supplier-run).
> - **Depends on:** core banking (platform pattern), identity platform, developer platform, card-processing supplier.
> - **Costs:** open, with Tariq. **Top risk:** the supplier's change notice period.

Yousef asked: "If Reem owns it, is she woken when card payments fail at midnight?" Huda recorded it for lesson 2.2 and Module 8: the team would be on call for its own components, the operations centre would watch shared ones, and incidents would be recorded against CARDS-PAY either way. Tariq's blank cost line became the starting point for lesson 10.1.

## 🛠️ Exercises
**🟢 Sort ten to twenty items.** Take ten to twenty items from your application list, project list and request forms (or these ten Najm Bank items: cards app, core banking, test environment, new joiner laptop, data centre exit, card-limit rules engine, corporate payments portal, password reset, dispute-handling tool, card-processor migration). Label each product, service, project or component, with one line of reasoning. Mark any item you are unsure of and say what would decide it.
*Done when:* every item has a label and a reason, every "project" has an end date and names the products it changes, and every "unsure" item names the fact that would settle it.

<details><summary>Model answer and self-check</summary>

**Model answer.** Cards app and corporate payments portal: products. Dispute-handling tool: product (internal users), though unsure until a business owner is agreed. Core banking and card-limit rules engine: components (core banking is shared; it still gets one owner's name in the next exercise). Test environment, new joiner laptop, password reset: services. Data centre exit and card-processor migration: projects with dates, naming the products whose hosting or interfaces change.

**Self-check.**
- Did you avoid calling every application a product?
- Does every service name what people get, not the system behind it?
- Did each "unsure" item name the fact that would decide it?

</details>

**🟡 Name the owners.** For the products and services from the first exercise, and for any shared system such as core banking (it still needs one accountable name), write one accountable name (or "none") and a role title. Run the ownership check on two products.
*Done when:* each line has one person or an explicit "none", no line names a committee or team, and the check is answered yes, partly or no for two products.

<details><summary>Model answer and self-check</summary>

**Model answer.** Cards & Payments: Reem; corporate payments portal: a named head of corporate payments, not the steering group; test environment: Sami; new joiner setup: a named service owner in Yousef's service desk; core banking (a shared component, still one name): the head of its platform team; dispute tool: "none" until a business owner is agreed. Check for Cards & Payments: order of work, yes; cost and incidents, partly (incidents only); release timing, partly (the change board decides). Check for the portal: order of work, partly (the steering group still reorders it); cost and incidents, no (a shared budget line; incidents logged against the application); release timing, no. Omar must grant the order of work; Tariq must split out the costs.

**Self-check.**
- Is there exactly one person per line?
- Did you write "none" instead of guessing?
- Did the check expose at least one owner without real authority, and say who must grant it?

</details>

**🔴 Write one product canvas.** Write a one-page canvas for one product. Show it to one user and one engineer, and record what each would change.
*Done when:* it fits one page, has at least two measurable outcomes, separates services from components, and records both reviewers' comments and what you changed.

<details><summary>Model answer and self-check</summary>

**Model answer.** Reem's canvas is a model: purpose in users' words, countable outcomes, services separate from components, dependencies with owners, honest blanks such as cost. Users usually change purpose and service names; engineers add forgotten components.

**Self-check.**
- Are outcomes changes in behaviour, not outputs?
- Are blank cells open questions with a name attached?
- Did a reviewer's comment actually change the canvas?

</details>

## ⚠️ Mistakes and traps
- **Renaming the application list.** Hundreds of "products" with no owners. Group components into products users recognise, then map them.
- **Naming a committee as owner.** Name a person and a role title; let the committee advise.
- **Owners without authority.** Run the ownership check before announcing names.
- **Abolishing projects entirely.** Keep projects for genuinely temporary work, and make them name the products they change.
- **Confusing the service with the system.** "ERP access" is a system; "Raise and approve purchase orders" is a service. Describe what people get.

## 🧾 Recap
- A **product** is something people use that the bank keeps changing; a **service** is the offer through which they get it; a **project** is temporary work with an end date.
- **Every product and every service has exactly one accountable name; every project has an end date.**
- Products are not applications: test boundaries for being recognised, measurable, ownable, releasable and costable.
- Shared systems need a deliberate pattern and still one name inside the bank.
- An owner needs authority over order of work, sight of cost and incidents, and a say in release timing.

## ✍️ Check yourself
**1. Omar asks Huda for "the product list". She has the application list with about 420 entries. What should she do first?**

- A. Publish the 420 applications as products, listing each one's current support team as owner.
- B. Ask each department head to nominate a committee to own the applications in their own area.
- C. Group the applications into products that users would recognise, then map each one to them.
- D. Wait for a new portfolio tool to be bought, because a spreadsheet cannot hold a product list.

<details><summary>Answer</summary>

**C.** Applications are components; products are what users recognise, and components are mapped to them. A renames the application list, B names committees, and D delays a decision a spreadsheet can start. See "Products are not applications".

</details>

**2. Tariq asks whether "Card controls in the app" and "Cards & Payments" should each have a budget line and an owner. Which is the product, which is the service, and why?**

- A. Cards & Payments is the product, built and changed for years; card controls is a service people use it through.
- B. Card controls is the product, because customers see it; Cards & Payments is a service shared by several teams.
- C. Both are services, because both are offered to customers; the product is the card-limit rules engine behind them.
- D. Cards & Payments is a project, because it has a budget line; card controls is the product that project delivers.

<details><summary>Answer</summary>

**A.** The product is what is built, run and changed over years, with one owner and a cost; the service is an offer with terms that the product sits behind. B judges by visibility, C confuses a component with the product, and D treats a long-lived product as temporary work. See "Three words, three jobs" and "How the three relate".

</details>

**3. The risk register names "Digital Steering Group" as owner of the corporate payments portal. Nour asks whether that is acceptable. What is the best answer?**

- A. Yes, because a group spreads the risk and gives each decision more senior support.
- B. Yes, provided the group meets at least monthly and keeps minutes of each meeting.
- C. No, because only the head of operations may own a system running in production.
- D. No, because a group cannot be accountable; name a person and let the group advise.

<details><summary>Answer</summary>

**D.** Accountability needs one person who answers for the result. A and B confuse support with accountability, and C ties ownership to operations instead of the product. See "Accountable is not the same as responsible".

</details>

**4. Najm Bank must move its card-processing interface to a new supplier by a fixed contract date. How should this work be organised?**

- A. As a new product with a permanent team that keeps the migration work going after the date.
- B. As a project with a date and budget, naming the products it changes and who receives them.
- C. As a catalogue service, so that product teams can request the migration when they need it.
- D. As backlog work only, with no date at all, because products should never contain projects.

<details><summary>Answer</summary>

**B.** Temporary work with a fixed date fits a project that names the products it changes and hands over to their owners. A makes temporary work permanent, C misuses the catalogue, and D ignores a real deadline. See "When a project is still the right tool".

</details>

**5. Huda proposes a product called "Digital Channels" covering the cards app, internet banking, the SME portal and the chatbot. Applying the boundary tests, what is the most likely problem?**

- A. It is too big: many teams must agree on each change, and outcomes cannot be measured as one.
- B. It passes, because one owner for every channel gives customers a consistent experience.
- C. It fails only the costable test, which a single shared budget line would be enough to fix.
- D. The chatbot should become its own product first; the other three can then stay grouped as one.

<details><summary>Answer</summary>

**A.** A boundary that fails the ownable, releasable and measurable tests is usually too big. B ignores the ownable and releasable tests, C hides a structural problem behind a budget line, and D removes the smallest part while the rest stays too big. See "Five tests for a product boundary".

</details>

## 📚 References
- Project Management Institute, "What is a project?" (definition reported in search results, 2026-11-19; the page could not be opened from this environment): https://www.pmi.org/about/what-is-a-project
- Kersten, M., *Project to Product* (IT Revolution, 2018): a practitioner's case for managing software by products rather than projects (full citation; not opened).
- Library course: [*AI Product Management*, lesson 2.1 — Discovery for AI: jobs, workflows and where AI fits](../aipm/index.html#/2.1).

---

# 2.2 — Designing a product-aligned operating model: product, platform and enabling teams
*Level: 🟢 Beginner* · *Prerequisites: 1.2, 2.1* · *Step: Plan*

**After this you can** place the recurring work of one value stream, draw its team map with product, platform and enabling teams, write a decision-rights table for eight recurring decisions, and plan which functional teams change first. *Study time: reading about 15 min, hands-on about 110 min (estimate).*

## ⚡ In 60 seconds
- An **operating model** is how an organisation is set up to work: teams, ownership, decision rights, records, funding and measures. This lesson covers teams and decision rights.
- Start from the work: place each recurring piece **with the product**, **as a self-service capability**, or as **time-limited help**. Product, platform and enabling teams follow from the answers.
- The rule that matters most: **design teams around the products and flow you want, because the structure you choose will show up in what gets built.**
- Decision cue: if a typical change needs more than two teams to agree, the boundaries or interfaces are wrong.
- Biggest trap: reorganising the whole division on one date from a chart drawn on paper.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

Huda went back to the map from lesson 1.2: small changes to the cards app took about 21.5 days of work and about 106 working days (around five months) from idea to customers, with nine hand-offs. This time she asked who owned each step. The nine steps belonged to eight groups: demand review, investment committee, Reem's team (requirements and build), architecture, testing centre, security, change board and the operations team running the release window. Only one answered for the outcome. Nobody was slow; each group had its own queue and served dozens of others.

Omar wanted to announce product teams division-wide next quarter, from a chart drawn in a weekend. Yousef warned that moving people without changing decisions, records and money would just rename the queues. This lesson starts from the work and starts small enough to learn.

## 📐 How it works

### 🟢 The essentials

**Structure shapes the product.** In a 1968 paper in *Datamation*, "How Do Committees Invent?", Melvin Conway argued that organisations which design systems are constrained to produce designs that copy their own communication structures (as reported; now called Conway's law, introduced in lesson 0.1). If cards, fraud and payments sit in three departments with three backlogs, customers feel three systems. Choose team structure with the product and the flow in mind, not only reporting lines.

**Start from the work, not the boxes.** List the recurring work in one value stream (the lesson 1.2 steps, plus running the product) and ask of each piece: *where should this sit so a typical change need not wait for it?*

| Where the work sits | Choose it when | Example in the cards stream | Warning sign |
|---|---|---|---|
| **With the product** | It changes with the product's outcomes, is needed most weeks and needs product knowledge | Requirements, build, most testing, routine releases | The team cannot explain parts of what it owns |
| **As a self-service capability** | Many teams need it in the same way, and it can be offered without a conversation | Environments, pipelines, databases, standard access roles | Each use still needs a ticket |
| **As time-limited help** | A team lacks a skill it will need for good and can learn within months | Automated testing, threat modelling | Helpers still there a year later, doing the work |

Some work (security policy, second-line risk, major-incident command) stays central by written choice. Shared systems such as core banking take a pattern from lesson 2.1.

**The teams follow from the answers.** A long-lived **product team** holds the first row for one product: product management, design, engineering, testing and enough operations knowledge to run what it builds, free of other teams' queues for routine work. A **platform team** runs the second row as internal products. An **enabling team** gives the third: it helps a team until it can work alone, then moves on.

These three names are widely used; their best-known source is *Team Topologies* by Matthew Skelton and Manuel Pais (IT Revolution, 2019), which defines a fuller model of team types and named ways for teams to interact. This lesson does not teach that model; it starts from where each piece of work sits.

**Every line between teams says how work crosses, and when it ends.** A line on a team map means one team needs something from another. Write two things on it:

| On the line | Options | Healthy when |
|---|---|---|
| **Route** | Self-service; request (ticket, form or meeting); joint work | Routine needs go by self-service |
| **End** | None (stable self-service); a date | Every request and joint-work line has a date to become self-service or stop |

This course's test: **a request line with no end date is a queue**, the lesson 1.2 hand-off renamed. Joint work suits a new interface or a hard problem, but is costly if it never ends.

### 🟡 Going deeper

**What happens to functional teams.** Each function lands in one or more of four places.

| Function at Najm Bank | Into product teams | Platform (self-service) | Enabling (time-limited help) | Stays central |
|---|---|---|---|---|
| Testing centre | Testers join teams | Test tooling in pipelines | Small coaching team | — |
| Database team | Routine schema changes | Database-as-a-service | Performance coaching | Production data access controls |
| Security | Security champions | Scanning in pipelines | Threat-modelling coaching | Policy, monitoring, second-line liaison |
| IT operations | On-call for own components | Monitoring tools | Reliability coaching | Service desk, major incidents, shared-systems operations |

**On-call** means being reachable out of hours to restore a service. "Stays central" is legitimate in a regulated bank, but it should be a written choice, not a side effect of who argues hardest.

**Platform teams must act like product teams.** Google Cloud's announcement of the 2024 DORA report lists platform-engineering findings: internal developer platforms increased developer productivity; a platform initiative might bring a temporary dip in performance before improvements show; and results were best with user-centred design, developer independence and a product-oriented approach. So each platform team needs a product manager, a catalogue (lesson 2.3), users it talks to and an adoption measure. For the engineering view, see [*Cloud & DevOps: Zero to Hero*, lesson 0.1 — What cloud, DevOps, platform engineering and SRE are](../cloud/index.html#/0.1).

**Decision rights.** A **decision-rights table** lists recurring decisions with who decides, who is consulted, and a **guardrail**: a rule set in advance that lets a team decide alone while inside it. A **standard change** is a low-risk change of a pre-approved kind. The **change authority** is the person or body that approves risky changes (both in lesson 6.2). **Least privilege** means only the access needed, for only as long as needed (lesson 7.2).

| Decision | Decides | Consulted | Guardrail |
|---|---|---|---|
| What the product team works on next | Product manager | Users, operations, risk for regulated features | Agreed outcomes and budget (Module 3) |
| How to build a change | Product team | Architecture, for shared interfaces | Standards and approved patterns |
| When a change goes live | Product team for standard changes; change authority for high-risk ones | Operations, for shared components | The change policy (lesson 6.2) |
| Who can access production | System owner | Security, risk | Least privilege, time-limited, logged |
| Accepting a risk above appetite | A named senior risk owner, not the team | Nour's team (second line) | The bank's risk policy |
| Changing a platform service | Platform product manager | Teams that use it | Published deprecation notice period |

Review it after the first three disputes; disputes are its test.

**Team load check.** This course's check of whether a team owns too much: can it explain everything it owns, how much time goes to keeping things running, and how often does it wait on experts for routine changes? Move routine needs to a self-service capability, narrow the boundary or split the team; adding people to one large team rarely helps. The *Team Topologies* authors are reported to frame a related idea as team cognitive load, the mental effort a team can carry.

### 🔴 Expert view

**Start with one value stream.** Reorganising 600 people on one date teaches little, because everything changes at once. Pick one stream people complain about, design its teams, decision rights, records and measures, run it for a quarter or two, compare lead time, change fail rate and team load before and after, then extend.

**Controls must move with the work.** When product teams release their own changes, risk functions worry about **segregation of duties**: one person both writing and releasing a change. The answer is usually controls built into the flow, not a team back in the path: recorded peer review, automated gates, deployment by the pipeline rather than personal access, and evidence kept automatically. Agree them with Nour's team first (lessons 6.2, 10.3); [*Cloud & DevOps: Zero to Hero*, lesson 4.3 — Securing the pipeline: secrets, signed artefacts and least-privilege deploys](../cloud/index.html#/4.3) covers the engineering. Draw suppliers on the map too: a contract with ten days' notice per change is a hand-off (lesson 10.2).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Work placement sheet** | Each recurring piece of work: with the product, self-service, time-limited help, or central | First step of any team design |
| **Team map** | The teams in a value stream, what each owns, and every line labelled with its route and its end | Before and after any team change |
| **Decision-rights table** | Recurring decisions with one decider, consulted parties and a guardrail | When disputes repeat |
| **Function landing table** | Where each functional team's work lands | Planning the transition with function heads |
| **Team load check** | Can the team explain what it owns; time spent keeping things running; how often it waits on experts | Quarterly, and before adding scope |
| **Pilot scorecard** | Lead time, change fail rate, team load and user feedback, before and after | Before extending the pilot |

## 🏛️ In practice at Najm Bank
Fictional and illustrative. Omar agreed to pilot the cards change stream. Huda, Reem, Sami and Yousef wrote the target map:

> **Team map: cards change stream (pilot)**
>
> - **Cards & Payments product team** (Reem): requirements, build, testing and routine releases for the app, rules engine and notifications; two testers join; on-call for its own components from month three.
> - **Platform team** (Sami): pipelines, environments, observability, databases. Line: *self-service*, no end; has a platform product manager.
> - **Quality coaching** (enabling): line *time-limited help*, twelve weeks, on automated tests in the pipeline.
> - **Core banking platform team**: *self-service* for existing interfaces; *joint work* ending after eight weeks on the new card-limit interface.
> - **Card-processing supplier**: line *request* by contract, ten days' notice per change; Lina to renegotiate by the end of the pilot.
> - **Stays central:** security policy, major incidents, shared-systems operations (Yousef), second-line risk (Nour).
> - **Decision rights:** standard changes go live on the team's decision through the pipeline, with evidence recorded automatically; high-risk changes go to the change authority. Nour's team agreed the pipeline controls first.
> - **Baseline (from the lesson 1.2 map):** lead time about 106 working days for a small change; nine hand-offs across eight groups.

Yousef's condition, that operations can stop releases during a major incident, went into the decision-rights table. Omar announced the pilot and its scorecard, not a division-wide model.

## 🛠️ Exercises
**🟢 Draw today's team map.** For one value stream (or the cards stream on the lesson 1.2 map), list every team one real recent change touched, what each did, and how work reached it (ticket, meeting, shared tool, conversation).
*Done when:* every team is listed with its role and arrival route, and you have counted teams and hand-offs.

<details><summary>Model answer and self-check</summary>

**Model answer.** Najm Bank today, from the lesson 1.2 map: eight groups and nine hand-offs, mostly scheduled meetings or windows (demand review, funding, architecture review, change board, release) or tickets into shared queues (testing, security). Only Reem's team answers for the outcome. Add the card-processing supplier for changes that touch its interface.

**Self-check.**
- Did you trace a real change, not the documented process?
- Did you include suppliers and approval bodies?
- Can you see which hand-offs are tickets?

</details>

**🟡 Design the target map.** Place each piece of recurring work, then redesign the stream with product, platform and enabling teams, labelling every line with its route and end.
*Done when:* a typical change needs no more than two teams to agree, every line has a route and an end, every request or joint-work line has a date, and what stays central has a reason.

<details><summary>Model answer and self-check</summary>

**Model answer.** Huda's pilot map is a model: a product team that takes routine changes to production, a self-service platform, twelve weeks of coaching, joint work with core banking ending after eight weeks, a dated supplier line, and a short central list with reasons.

**Self-check.**
- Could the product team take a routine change live without another team's queue?
- Does every request and joint-work line have a date?
- Is everything left central there for a reason, not habit?

</details>

**🔴 Decision rights and the first step.** Write a decision-rights table for eight recurring decisions, and a one-page pilot plan: which functional teams change first, the scorecard baseline, and who in risk and controls must agree before it starts.
*Done when:* each decision has one decider, consulted parties and a checkable guardrail; the plan names each affected function and what happens to it; the baseline is recorded; and the risk agreement has a name and a date.

<details><summary>Model answer and self-check</summary>

**Model answer.** Keep the six rows in "Decision rights" and add local ones, for example:

| Decision | Decides | Consulted | Guardrail |
|---|---|---|---|
| Change a fraud rule threshold | Fraud operations lead | Reem; Nour's team | Within the approved range, logged, reviewed weekly |
| Retire a catalogue entry | The entry's owner | Its recent users; service desk | Notice period announced to users (lesson 2.3) |

The plan mirrors Huda's pilot, with operations keeping a right to stop releases during a major incident. Baseline: the lesson 1.2 figures, taken before anything moves. Risk agreement, one line: "Nour, IT Risk and Controls Lead: pipeline control set v1 agreed, signed by <date>; pilot starts only after this." 

**Self-check.**
- Does any decision have two deciders or a committee?
- Is each guardrail a rule someone can check?
- Is the risk agreement a precondition, not an afterthought?

</details>

## ⚠️ Mistakes and traps
- **Big-bang reorganisation.** Pilot one value stream, measure, then extend.
- **Renaming queues.** A "platform" that needs a ticket for every use is the old team renamed. Offer self-service, and date every request line.
- **Enabling teams that never leave.** Set an end date and a test of when the receiving team is ready.
- **Overloaded product teams.** Run the team load check.
- **Forgetting the controls.** Agree pipeline controls with risk before moving release decisions.

## 🧾 Recap
- Start from the work: place it **with the product**, **as a self-service capability**, as **time-limited help**, or central by written choice; the teams follow.
- Label every line between teams with its route and its end; a request line with no end date is a queue.
- **Design teams around the products and flow you want, because the structure you choose will show up in what gets built.**
- Pilot one value stream, and move controls into the flow with risk's agreement.

## ✍️ Check yourself
**1. Omar wants to announce product teams across the whole Technology division on the first day of next quarter. What does this lesson recommend instead?**

- A. Announce the full model now, but delay team moves for a year until all tools are replaced.
- B. Pilot one value stream, measure lead time and team load before and after, then scale it up.
- C. Ask each department head to redesign their own department separately, then report back.
- D. Hire an outside firm to run the reorganisation so that internal disagreement stays minimal.

<details><summary>Answer</summary>

**B.** A measured pilot lets the division learn before scaling. A delays without learning, C repeats the functional split, and D outsources decisions without reducing big-bang risk. See "Start with one value stream".

</details>

**2. Sami's team renames itself "the platform", but every environment still needs a ticket and a five-day wait. What is missing?**

- A. A larger budget, since a platform needs more money than the old infrastructure team had.
- B. A coaching engagement with each product team before it may use any environment.
- C. A separate team of environment experts, so that the platform team can focus on pipelines.
- D. Self-service through a clear interface, run like a product with real users and measures.

<details><summary>Answer</summary>

**D.** Environments are a routine shared need, so they belong in a self-service capability run like a product. A, B and C add money, a gate or another team without fixing the queue. See "Start from the work, not the boxes" and "Platform teams must act like product teams".

</details>

**3. Testing-centre coaches were sent to help Reem's team adopt automated testing. Six months later they write most of the tests themselves. What has gone wrong?**

- A. Nothing serious: tests are being written, and coaches can hand over once quality improves.
- B. The coaches should have joined the platform team so the tests run in the pipeline.
- C. Coaching has turned into doing the work; it needs an end date and a readiness test.
- D. The product team was too small and should merge with the testing centre for good.

<details><summary>Answer</summary>

**C.** Time-limited help should leave the team able to work alone. A accepts a dependency with no end, B confuses tooling with skill, and D undoes the product team. See "Every line between teams".

</details>

**4. Nour worries that if Reem's team releases its own changes, the bank loses segregation of duties. Which response fits this lesson?**

- A. Agree pipeline controls with risk first: recorded review, automated gates, pipeline deploys.
- B. A release manager in the operations team countersigns each change before it goes live.
- C. Reem, as product manager, approves her own team's releases in place of a second reviewer.
- D. Supplier engineers release the changes, since they sit outside the bank's reporting lines.

<details><summary>Answer</summary>

**A.** Controls move into the flow, agreed with risk first. B puts a queue back in every change's path, C is not segregation because Reem leads the team that wrote the change, and D shifts risk to a supplier without a control. See "Controls must move with the work".

</details>

**5. Huda drafts four rows for the cards stream's decision-rights table. Which row is written well?**

- A. "Production access. Decides: Sami and Yousef jointly. Consulted: security. Guardrail: least privilege, logged."
- B. "Risk above appetite. Decides: Reem. Consulted: Nour's team. Guardrail: the bank's risk policy."
- C. "How to build a change. Decides: product team. Consulted: architecture. Guardrail: good engineering judgement."
- D. "Next work for cards. Decides: Reem. Consulted: users and risk. Guardrail: agreed outcomes and budget."

<details><summary>Answer</summary>

**D.** One decider, named consulted parties and a checkable guardrail. A has two deciders, B gives Reem a decision that belongs to a named senior risk owner, and C's guardrail cannot be checked. See "Decision rights".

</details>

## 📚 References
- Google Cloud blog, "Announcing the 2024 DORA report" (22 October 2024; opened 2026-11-19), platform engineering section: https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
- Team Topologies, "Team Shape Templates" (GitHub, CC BY-SA 4.0; the model's team types and interaction modes; opened 2026-11-20): https://github.com/TeamTopologies/Team-Shape-Templates
- Skelton, M. and Pais, M., *Team Topologies: Organizing Business and Technology Teams for Fast Flow* (IT Revolution, 2019); site https://teamtopologies.com (full citation; the site could not be opened from this environment). Its use of team cognitive load is reported from search summaries.
- Conway, M. E., "How Do Committees Invent?", *Datamation* 14(4), 28–31, April 1968 (citation as reported in search results, including BibBase: https://bibbase.org/network/publication/conway-howdocommitteesinvent-1968; not opened).
- Library course: [*AI Product Management*, lesson 9.3 — Teams, roles and operating model for AI products](../aipm/index.html#/9.3).

---

# 2.3 — The service catalogue: the offer the business actually sees
*Level: 🟢 Beginner* · *Prerequisites: 2.1, 2.2* · *Step: Serve*

**After this you can** write catalogue entries for one product and one platform service using a standard set of fields, test them with three real users, and set the rules for adding, changing and retiring entries. *Study time: reading about 15 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- A **service catalogue** is the published list of what IT offers, in the words of the people who use it: what you get, who may have it, how to ask, what service level to expect, what it costs, where to get help and who owns it.
- At Najm Bank it has two front doors: staff use the service portal, engineers the developer portal. It is still one catalogue, with one set of fields.
- An entry is a **promise**. It is not the list of systems (the inventory) and not the steps IT follows to deliver (the recipe in lesson 7.1).
- The rule that matters most: **if a user cannot find it, understand it and order it without calling someone, it is not in the catalogue yet.**
- Decision cue: an entry with no owner, no requests in six months, or a promise IT does not keep should be fixed or retired.
- Biggest trap: hundreds of entries copied from the system list, in IT's language, with no service levels and no owner.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

Najm Bank already had a "service catalogue" in its service management platform: 312 entries, built five years earlier by copying the application list and adding a form to each line. When Yousef's team checked, 190 entries had no requests in the past year, 41 had owners who had left the bank, and the three most requested items (new joiner setup, shared mailbox, report access) were each split across several confusingly named entries. The eleven "payments" forms from lesson 2.1 came straight from it.

Meanwhile Sami's platform team kept its own list of offers for engineers on a wiki page: clearer, but invisible to the service desk. The bank had two catalogues, one too big and one too hidden. A catalogue that promises what IT does not deliver teaches the business to distrust IT's promises. This lesson rebuilds it from the products and services named in lesson 2.1.

## 📐 How it works

### 🟢 The essentials

**What the catalogue is, and what it is not.**

| List | What one entry means | Who reads it | Lesson |
|---|---|---|---|
| **Service catalogue** | One thing a person or team can request, subscribe to or use, with its terms | Staff, business lines, engineers | This lesson |
| **Product list** | One product with its owner, purpose and outcomes | Leaders, product managers, finance | 2.1 |
| **Component inventory** | One running system, application or asset | Engineers, operations, audit | 9.1, 9.2 |
| **Request recipe** | How IT fulfils one kind of request, step by step | The people and tools that deliver | 7.1 |

They link: a product offers entries; each entry is delivered through a recipe; the recipe touches components. But each has a different reader and job.

**Two front doors, one catalogue.** Najm Bank's problem was two lists: the service desk's for staff and Sami's wiki for engineers. The fix was not to force one audience into the other's tool, but to make both front doors show the same kind of entry.

| Front door | Who comes in | Typical entries at Najm Bank | Tool |
|---|---|---|---|
| **Service portal** | Bank staff and business lines | New joiner setup; Corporate payments portal access; Report access | Service management platform |
| **Developer portal** | Engineers in product and platform teams | Test environment, small; Pipeline for a new service; Managed database | Developer portal |

Both use the same fields, owners and product identifiers, so requests, costs and incidents can be traced (lesson 9.1).

**The fields of an entry**, in the order a user asks:

| Field | The user's question | Example: Test environment, small |
|---|---|---|
| **Name** | What is it called? | Test environment, small |
| **What you get** | What exactly will I have? | A working environment for one service, with masked test data, monitoring and network rules already set |
| **Not included** | What should I not expect? | Production data; full-scale performance testing |
| **Who may have it** | Am I allowed? | Product team leads |
| **How to get it** | How do I ask? | Self-service in the developer portal; give product identifier, cost centre, end date |
| **Service level** | How fast and reliable? | Ready within one working day; supported in working hours |
| **Cost** | What will it cost my team? | Shown monthly to the product's cost centre (lesson 7.3) |
| **Help** | Where do I go if it fails? | Platform support channel; incidents through the service desk |
| **Owner** | Who answers for it? | Sami, Platform Engineering Lead |
| **Status and review date** | Is it current? | Live; review in six months |

**Service levels in plain words.** A **service level** is what the user can expect: support hours, fulfilment time, availability, response to problems. A level agreed in writing with a business line is often called a **service level agreement (SLA)**; a team's internal reliability target, a **service level objective (SLO)**. Lesson 8.3 covers both, and [*Cloud & DevOps: Zero to Hero*, lesson 5.2 — SLOs, error budgets, alerting and on-call that people can sustain](../cloud/index.html#/5.2) covers the engineering. For the catalogue: publish only a level you measure and usually meet.

### 🟡 Going deeper

**Start from users, not systems.** Group three months of requests, emails and chat messages to the service desk and platform team by what people wanted, in their words. The largest groups become the first entries. Only then link each entry to its product and components.

**Bundle what people need together.** Users want to do something, not obtain a system. "New joiner setup" bundles a laptop, accounts, standard software and team folders. "Corporate payments portal access" bundles an account, a role, a hardware token and training. Several teams may work behind a bundle; the user sees one entry.

**Retire as carefully as you add.**

1. **Adding:** a new entry needs a named owner, a product identifier, a recipe and a service level the owner measures. No owner, no entry.
2. **Changing:** anything that reduces what users get, raises their cost or slows the service level is announced to current users with notice.
3. **Retiring:** an entry with no requests for a set period (Najm Bank chose six months), or whose owner left without a replacement, is fixed or retired, and its users are told what replaces it.

**Measure the catalogue itself.**

| Measure | Warning sign |
|---|---|
| Share of requests made through a catalogue entry | Many requests still arrive by email or chat |
| Entries with no current named owner | Any above zero |
| Entries with no requests in six months | A large share of the catalogue |
| Entries whose service level was met last quarter | Published levels routinely missed |
| Users' rating of finding and understanding entries | "I called someone instead" |

### 🔴 Expert view

**The catalogue is where products meet money and records.** An entry is the unit people consume, so it is where **showback** (showing each team what it used and what that cost, without billing it) or **chargeback** (actually billing it) appears (lesson 7.3); it is what a subscription refers to, so **entitlements** (records of what a person or team is allowed to have) and access rights hang from it (lesson 7.2); and it is what a service level is promised for, so incidents should be recorded against it and its product (Module 8). A catalogue built with product identifiers links all three; a list of forms links none.

**Developer portals.** Many engineering organisations keep the engineers' front door in a **developer portal**, where engineers find services, documentation, templates and owners. One open-source example is Backstage, which its repository describes as a framework for building developer portals around a central software catalogue, hosted by the Cloud Native Computing Foundation as an Incubation-level project (at the time of writing); an illustration, not an endorsement. The operating-model point: the portal and the business catalogue must share product identifiers and owners, or the bank has two disconnected lists again. Lesson 11.1 decides which tool is the system of record for what.

**Customer-facing offers.** Customers see the feature itself, under commitments the business sets; ask what was promised externally before writing a weaker internal level.

**Do not let the catalogue become a wall.** Keep one route for "I need something that is not here", leading to demand management (lesson 4.1); review those asks monthly.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Catalogue entry template** | The ten fields, from name to status and review date | For every entry, business or technical |
| **Request grouping sheet** | Three months of requests grouped by what users wanted, in their words, with counts | Before building or rebuilding a catalogue |
| **Catalogue rules** | Add, change and retire rules with notice and review periods | When the catalogue is published; review yearly |
| **Catalogue health measures** | Requests through the catalogue, ownerless and unused entries, levels met, user rating | Monthly or quarterly with entry owners |
| **User test script** | Three users try to find, understand and order an entry while you note where they stop | Before publishing a new or rewritten entry |
| **Service management platform or developer portal** | Front doors for staff and for engineers; Backstage is one open-source portal | Examples only, not endorsements; share identifiers across tools |

## 🏛️ In practice at Najm Bank
Fictional and illustrative. Yousef, Sami and Reem rebuilt the catalogue for the cards stream first. Yousef found 18 request groups covering most of the volume; Sami moved his wiki list into the developer portal with the same fields; Reem wrote a service-portal entry:

> **Catalogue entry: Card controls, contact-centre view (v1)**, the name used in Reem's canvas (lesson 2.1)
>
> - **What you get:** agents see a customer's card status and limits, block and unblock cards, and see the last ten card events, in the agent desktop.
> - **Not included:** credit-limit changes (credit team); disputes (dispute-handling tool).
> - **Who may have it:** contact-centre agents and team leaders, through the "card agent" role.
> - **How to get it:** the team leader orders the role in the service portal; granted the same day once training is complete.
> - **Service level:** available whenever the cards app is; availability published monthly; problems answered within 30 minutes in contact-centre hours.
> - **Cost:** inside the Cards & Payments product cost; shown to the contact-centre cost centre quarterly.
> - **Help:** service desk, category "Cards". **Owner:** Reem (CARDS-PAY). **Status:** live; review in six months.

Reem tested it with three team leaders. Two searched for "block card", so she added that keyword; one asked what to do when the app is down, so she added the fallback route to Help. Yousef retired eleven old entries it replaced and told their 40 recent users what to use instead. Nour linked the "card agent" role to the access reviews of lesson 7.2.

## 🛠️ Exercises
**🟢 Write one entry.** Pick something people often ask your organisation for (or the Najm Bank test environment) and write its entry with the ten fields.
*Done when:* every field is filled or marked "unknown" with a name for who will find out, "what you get" uses the user's words, and the owner confirms the service level is measured.

<details><summary>Model answer and self-check</summary>

**Model answer.** The "Test environment, small" example is a model: what users get and do not get, who may order it and how, a measured level, cost, help, a named owner and a review date. Templates and network rules stay in the recipe.

**Self-check.**
- Could a user order it from the entry alone, without calling anyone?
- Does "what you get" describe an outcome, not a system name?
- Is the owner a named person with a role title?

</details>

**🟡 Audit twenty entries.** Take twenty entries from your catalogue (or request forms). For each record the current owner, requests in six months, whether a service level is published and met, and any duplicate. Decide keep, fix, merge or retire.
*Done when:* all twenty have the four facts and a decision, every "retire" says what replaces it and how users will be told, and one sentence states the biggest pattern.

<details><summary>Model answer and self-check</summary>

**Model answer.** A typical Najm Bank result: six keep, five fix (missing owner or level), five merge into two bundles, four retire. The pattern: entries named after systems, not what users want, which caused the duplicates.

**Self-check.**
- Did you check request counts rather than guess?
- Are merged entries named in users' words?
- Did you resist keeping entries "just in case"?

</details>

**🔴 Design both front doors for one product.** Write the service-portal entries for one product's main offers and the developer-portal entries for the platform services its team uses. Write the add, change and retire rules, and run the user test with three real users.
*Done when:* both sets of entries share fields and the product identifier, the rules state notice and review periods, and you have recorded where each of three users stopped and what you changed.

<details><summary>Model answer and self-check</summary>

**Model answer.** For Cards & Payments: service portal, card controls in the app (internal view of the customer offer), card controls, contact-centre view, and card administration portal (SME) access; developer portal, test environment, pipeline for a new service, managed database, log and metrics collection, each with CARDS-PAY or the platform identifier and a named owner. Rules: owner, identifier, recipe and measured level to add; 30 days' notice for reductions (illustrative); review after six months without requests. User tests usually change names and search words and add missing help routes.

**Self-check.**
- Could a request, a cost line and an incident all be traced to the same entry?
- Did the user test change at least one entry?
- Can the service desk see the technical entries too?

</details>

## ⚠️ Mistakes and traps
- **Copying the system list.** Start from what users ask for, in their words.
- **Promising what you do not measure.** Publish only levels you measure and usually meet.
- **Two disconnected catalogues.** Share product identifiers and owners across the service portal and the developer portal.
- **Never retiring.** Set a retirement rule and use it.
- **The catalogue as a wall.** Keep a clear route to demand management for needs with no entry.

## 🧾 Recap
- The **service catalogue** is IT's offer in users' words: what you get, who may have it, how to ask, service level, cost, help and owner.
- It differs from the product list, the component inventory and the request recipe, and links to all three through product identifiers.
- Staff and engineers may use different front doors (service portal, developer portal), but the entries share fields, owners and identifiers.
- **If a user cannot find it, understand it and order it without calling someone, it is not in the catalogue yet.**
- Build from real requests, bundle, retire as carefully as you add, and measure the catalogue itself.

## ✍️ Check yourself
**1. Yousef finds that 190 of the catalogue's 312 entries had no requests last year. What should he do?**

- A. Ask each listed owner to confirm at the next quarterly review whether the entry is still needed.
- B. Move them to an "archived" section of the portal, where they can still be ordered if needed.
- C. Apply a retirement rule, retire or merge them, and tell their recent users what replaces them.
- D. Rename them in users' words and feature them on the portal home page for one quarter.

<details><summary>Answer</summary>

**C.** A retirement rule with announced replacements reduces clutter without surprising anyone. A relies on owners, 41 of whom have left the bank; B keeps the clutter under another heading; and D promotes entries before checking anyone needs them. See "Retire as carefully as you add".

</details>

**2. Sami's draft entry for "Test environment, small" lists: (1) a working environment for one service, with masked test data; (2) the template version and network rules used to build it; (3) ready within one working day; (4) the five tool steps that run after a request arrives. What should he move into the request recipe?**

- A. Item 1 only, because the kind of test data is a technical detail that users do not need.
- B. Item 3 only, because a fulfilment time belongs in a service level agreement, not an entry.
- C. Items 1 and 3, because an entry should hold only the name, the owner and the cost.
- D. Items 2 and 4, because they describe how IT delivers it, not what the user gets.

<details><summary>Answer</summary>

**D.** The entry states what users get and on what terms (items 1 and 3); the template, network rules and tool steps are delivery details for the recipe (lesson 7.1). A and C remove what users need to decide, and B moves the service level out of the field built for it. See "What the catalogue is, and what it is not".

</details>

**3. Sami's developer portal lists "Managed database" and Yousef's service portal lists "DB provisioning (Oracle/Postgres)" for the same offer, with different owners. What is the best fix?**

- A. One entry named in users' words, with one owner and the same identifiers in both tools.
- B. Keep both, since engineers and business users search with different names for it.
- C. Delete the developer portal entry, because the service portal is the official catalogue.
- D. Let users choose whichever entry they prefer, and track which one gets more requests.

<details><summary>Answer</summary>

**A.** The front doors can be different tools but must share the entry, owner and identifiers. B keeps duplicate owners, C removes engineers' front door, and D makes design a popularity contest. See "Two front doors, one catalogue" and "Developer portals".

</details>

**4. Reem wants to publish "99.99% availability" for the contact-centre card view. Her team does not yet measure its availability. What does the lesson advise?**

- A. Publish it, because a high target motivates the team and reassures the contact centre.
- B. Publish only a level the team measures and usually meets, and start measuring first.
- C. Publish no level at all, because service levels belong only in supplier contracts.
- D. Copy the level from the card processor's contract, since it runs part of the service.

<details><summary>Answer</summary>

**B.** A published level is a promise the owner should measure and usually meet. A risks a broken promise, C removes a field users need, and D borrows a supplier number that does not cover the whole service. See "Service levels in plain words".

</details>

**5. Three months after the new catalogue launched, many requests still arrive by email and chat. Which measure shows most directly whether this is improving?**

- A. The total number of entries published across the service portal and the developer portal.
- B. The number of service desk staff assigned to answering email and chat each day.
- C. The share of requests made through a catalogue entry rather than email or chat.
- D. The number of new entries that product owners added during the last quarter.

<details><summary>Answer</summary>

**C.** It directly shows whether people use the catalogue instead of going around it. A and D count entries, which can grow while use falls, and B measures staffing. See "Measure the catalogue itself".

</details>

## 📚 References
- Backstage, GitHub repository README (open-source framework for building developer portals with a central software catalogue; hosted by the CNCF as an Incubation-level project; opened 2026-11-19): https://github.com/backstage/backstage
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 5.2 — SLOs, error budgets, alerting and on-call that people can sustain](../cloud/index.html#/5.2).
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 0.3 — Meet Najm Bank's platform team, and how to use this course](../cloud/index.html#/0.3) (the platform team behind the developer portal).

---
