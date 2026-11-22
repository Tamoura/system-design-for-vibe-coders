# Module 8 — Many teams

*Qafila is now at Scale-up. About 120 people work there in twelve teams, one of them a new platform team. About 9,000 merchants use the app for about 120,000 deliveries a day, teams deploy to production many times a day, and a routing service now decides which courier takes which order. At this size the hard problems are no longer inside one team: they sit between teams. Who owns the courier payout screen? Why does one small change need four teams to agree? Why does every new service start with two weeks of copying set-up from an older one? This module covers the practice of working as many teams, seen from the inside by Yasmin, now in her second year as an engineer. First, drawing team boundaries on purpose, with clear ownership and a sensible load for each team. Second, finding, reducing and managing the dependencies between teams, and planning together without a planning machine. Third, building an internal platform that other engineers choose to use, and measuring their experience of it. Each lesson leaves an artefact: a team map with one team page, a dependency register with a cross-team plan, and a platform one-pager with a golden-path checklist and a short developer-experience survey.*

> **Steps:** Collaborate — shape teams around the work, keep the links between them few and clear, and give every team a paved road so that many teams can move fast without tripping over each other.

---

# 8.1 — Team structures and boundaries: product, platform and enabling teams
*Level: 🟡 Intermediate* · *Prerequisites: 5.1, 5.3* · *Step: Collaborate*

**After this you can** draw a team map for a growing product (which team owns which part, which kind of team each is, and how each pair of teams works together), write a one-page team page for one team, and spot the two most common boundary problems: work split by technical layer, and a team that owns more than it can understand. *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- Past one team, **where you draw boundaries decides how work flows.** A change inside one team is fast; a change across three teams waits at every hand-off.
- Most teams should be **product teams** that own one part of the product end to end. A few make them faster: a **platform team** (shared tools as self-service), an **enabling team** (coaching), sometimes a **specialist team** (a part too hard for everyone to learn).
- **Ownership** means one team answers for each part: its code, changes, alerts and users' problems. "Shared by everyone" means owned by no one.
- The rule that matters most: **draw boundaries around the flow of change, not around the technology.**
- Decision cue: if most changes need two or more teams, or a team cannot explain everything it owns, the boundary is wrong.
- Biggest trap: splitting teams by layer (an app team, a back-end team, a database team), so every user-facing change becomes a relay race.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

Over eighteen months after Growth, Qafila grew to about 120 people. Whenever a group got too big, it split by skill: the mobile developers became "Apps", the back-end developers "Core API", two database specialists "Data Infra", Hamad's analysts "Analytics".

Then a merchant chain asked for something simple: let a shop mark an order as "ready for pickup", so couriers stop arriving early. Yasmin, now in her second year, picked it up. The button lived in the merchant app (Apps), the new status in the order service (Core API), which needed a new column (Data Infra); the courier app had to show it (Apps, a different sprint) and Hamad wanted it in the reports (Analytics). Four teams, four backlogs, four sets of priorities: about a week of work took seven weeks to reach merchants.

Nobody was slow. The structure made every user-facing change cross every team. This lesson is about drawing boundaries so that most changes stay inside one team.

## 📐 How it works

### 🟢 The essentials

**Why one big team stops working.** In a group of *n* people there are *n × (n − 1) / 2* possible one-to-one conversation paths. Twelve people have 66; forty people have 780; 120 people have 7,140. So people split into teams. The question is not *whether* to split, but *where*: every boundary becomes a place where work waits and priorities clash.

**Structure shapes the product.** In 1968 Melvin Conway published a paper, "How Do Committees Invent?", arguing that organisations which design systems are constrained to produce designs that copy their own communication structures (as reported in summaries of the paper; the idea is now called **Conway's law**). At Qafila, three layer teams produced a product of three walled layers that every feature had to drill through. Parts that change independently need teams that can change independently.

**Two ways to cut.** There are two basic ways to split work between teams:

| Cut | What a team owns | What happens to a typical change | Example at Qafila |
|---|---|---|---|
| **By layer or technology** | One technical layer for the whole product (mobile, back end, database) | Crosses every layer, so every team | Apps, Core API, Data Infra |
| **By flow of change** | One part of the product end to end, for one user group or journey | Usually stays inside one team | Merchant Orders: merchant screens, order service, its data |

Cutting by layer feels natural, because people with the same skills like working together. But users experience journeys (placing an order, being paid, tracking a delivery), not layers. Cut along the journeys.

**Product teams.** A **product team** (also called a stream-aligned team, a term from the book *Team Topologies*) is a long-lived team that owns one part of the product and the change that flows through it. It has the skills to discover, build, ship and run that part without waiting for others: engineers for the screens and the services behind them, testing skills, access to design and product management, and the right to deploy. Most teams in a healthy company of 120 people are product teams.

**Ownership.** For each part of the product, write down one owning team. Owning means:

- the team decides what changes in that part, and in what order;
- the team reviews and merges changes to its code, even when someone else wrote them;
- the team's on-call rota answers that part's alerts (lesson 4.2);
- the team is the place support sends that part's problems (lesson 7.1).

A part with two owners has none; a part "owned by everyone" rots quietly.

### 🟡 Going deeper

**Three more kinds of team.** Three other kinds of team exist to make product teams faster. The names are widely used; their best-known source is *Team Topologies* by Matthew Skelton and Manuel Pais (IT Revolution, 2019), whose team-shape templates are freely licensed (CC BY-SA 4.0) on GitHub. This lesson describes the ideas in its own words.

| Kind of team | What it is for | How others use it | Warning sign |
|---|---|---|---|
| **Platform team** | Builds and runs shared tools and services that product teams would otherwise each build: the deployment pipeline, environments, monitoring defaults, secrets storage | As **self-service**: product teams use it without opening a ticket or waiting | Product teams queue for the platform team to do things for them |
| **Enabling team** | Experts who help product teams learn a skill (reliability, security, accessibility, testing), then step back | For a **time-boxed** period, side by side | The enabling team ends up doing the work permanently |
| **Specialist team** | Owns one part that needs rare, deep knowledge (a routing algorithm, a payments ledger) | Through a clear interface (an **API**, a defined way for software to call another piece of software) | The part is "specialist" only because nobody wrote it down |

Lesson 8.3 is about the platform team in depth.

**Three ways teams work together.** For each pair of teams that must interact, decide *how*:

- **Work closely for a while** on something new and uncertain. Useful, expensive, and it should end on a date.
- **Use as a service:** one team provides a documented API or self-service tool the other uses with little conversation.
- **Coach:** one team (usually an enabling team) helps another learn, then leaves.

Most interactions should be "use as a service". If two teams need to work closely all the time, they probably belong in one team, or the boundary between them is in the wrong place.

**Team load.** A team can only carry so much: so many services, so many technologies, so much on-call and support. The *Team Topologies* authors are reported to call this a team's **cognitive load**, the mental effort a team has to spend to do its work. You can check it with plain questions:

1. Can the team explain, without notes, what each thing it owns does and why?
2. How much of its time goes to keeping things running rather than improving them?
3. How often does it wait for someone outside the team for a routine change?
4. Does a new member understand the team's area within a few weeks?

If the answers are bad, do not just add people; large teams split into sub-groups anyway. Narrow what the team owns, move routine needs to self-service, or split the team along a seam in the flow of change.

**The team page.** Each team keeps a short public page so other teams can work with it without a meeting:

| Section | What goes in it |
|---|---|
| **Mission** | One sentence: which users, which part of the product, which outcome |
| **What we own** | Services, apps, data and dashboards, each linked |
| **How to work with us** | Where to ask, how to request a change, what we offer as a service |
| **On-call and support** | Rota link, what we answer, response times |
| **Current focus** | This quarter's outcomes (lesson 6.1) |
| **People** | Members and roles |

### 🔴 Expert view

**Design the teams for the product you want.** Because structure shapes the product, some organisations change team boundaries first, on purpose, to get the architecture they want; this is reported to be called the **inverse Conway manoeuvre**, and DORA's guidance on loosely coupled teams points to it (as reported in search summaries). It works only if the code can follow; plan the team change and the code change together (lesson 9.1).

**Boundaries are not forever, but not every quarter.** Each reorganisation costs context and trust. Review the team map twice a year, change it when the evidence (many cross-team changes, overloaded teams, orphaned parts) is clear, and prefer moving a responsibility to a stable team over breaking up a team that works well (lesson 5.1).

**The memorable rule.** Draw boundaries around the flow of change, not around the technology.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Team map** | One diagram: every team, its kind (product, platform, enabling, specialist), what it owns, and how each pair interacts | When the company passes three or four teams, and at each twice-yearly review |
| **Ownership list** | Every service, app, data store and dashboard with exactly one owning team | Before an incident shows that nobody owns something |
| **Team page** | A one-page public description of a team: mission, what it owns, how to work with it, on-call, focus, people | For every team; linked from the team map |
| **Team load check** | Four questions on understanding, run time, waiting and onboarding | Every quarter, or when a team says it is drowning |
| **Change trace** | Pick five recent user-facing changes and count the teams each one touched | To find out whether boundaries follow the flow of change |

## 🏛️ In practice at Qafila
After the "ready for pickup" change, Maha asked Faisal (now Head of Engineering) and Aisha to redraw the teams. Yasmin joined them to run the change trace. Illustrative and fictional.

> **Change trace (five recent user-facing changes)**
>
> | Change | Teams touched | Calendar time |
> |---|---|---|
> | "Ready for pickup" status | Apps, Core API, Data Infra, Analytics | 7 weeks |
> | Courier tip in the app | Apps, Core API, Payments | 5 weeks |
> | Opening hours per branch | Apps, Core API, Data Infra | 4 weeks |
> | New payout report | Core API, Analytics | 3 weeks |
> | Fix wrong ETA on tracking screen | Apps, Core API | 2 weeks |
>
> **Qafila team map v2 (Scale-up, twelve teams)**
>
> | Team | Kind | Owns |
> |---|---|---|
> | Merchant Onboarding | Product | Sign-up, branches, shop settings |
> | Merchant Orders | Product | Order creation and statuses, merchant order screens |
> | Courier Experience | Product | Courier app screens, shift handling |
> | Courier Earnings | Product | Earnings, tips, payouts |
> | Live Tracking | Product | Tracking screens, location updates, ETA |
> | Dispatch | Product | Matching orders to couriers, using routing |
> | Routing | Specialist | The routing service and its algorithm |
> | Payments | Product | Merchant billing, payment-provider integration |
> | Support Tools | Product | Help-desk integration, the logged support view |
> | Data & Analytics | Product (internal users) | Analytics pipeline, reports, data definitions |
> | Platform | Platform | Pipeline, environments, monitoring defaults, secrets |
> | Practices | Enabling | Reliability and security coaching (Salma and Dana's experts) |
>
> **Interactions this half-year:** Dispatch and Routing work closely until the routing interface is stable (end date set); product teams use Platform as a service; Practices coaches Live Tracking on its 99.9% tracking target, then Payments.

Faisal's first draft kept Apps as one team "because mobile skills are rare". Aisha ran the trace on it: four of the five changes still crossed Apps. They spread the mobile developers across product teams and gave them a weekly guild meeting (a cross-team group for one skill). Hamad's team page now says Data & Analytics owns the shared data definitions. Yasmin moved to Merchant Orders, which owns "ready for pickup" end to end.

## 🛠️ Exercises
**🟢 Run a change trace.** Use the Qafila change trace above, or five recent changes in an open-source project you can browse (look at merged pull requests and which folders or maintainers each touched). For each change, list the teams (or folders and maintainers) involved and say whether the change stayed inside one boundary.
*Done when:* you have five rows, each with a count of teams or areas touched, and one sentence naming the boundary most changes cross.

<details><summary>Model answer and self-check</summary>

**Model answer (Qafila).** Teams touched: 4, 3, 3, 2, 2; none stayed inside one team. Most changes crossed Apps and Core API, which points to cutting by user journey rather than by layer.

**Self-check.**
- Did you name one boundary, not "communication in general"?
- Did you notice that calendar time grows with the number of teams, even when the work itself is small?

</details>

**🟡 Draw a team map.** For Qafila at Scale-up (use the parts in the fact sheet and the team list above as a starting point, or design your own) or for a product you know well, draw a team map: every team, its kind, what it owns, and how each pair that must interact will work (closely for a while, as a service, or coaching).
*Done when:* every part of the product has exactly one owning team, each team has a kind, no team is "shared by everyone", and every "work closely" pair has an end date.

<details><summary>Model answer and self-check</summary>

**Model answer.** Like the Qafila v2 map: about nine product teams cut by user journey, one platform, one specialist (routing) and one enabling team; product teams use Platform as a service; Dispatch and Routing work closely until a set date.

**Self-check.**
- Is any team mostly a layer (all the mobile work, all the database work)? Why?
- Does any product team depend on another team for almost every change? Move the boundary.

</details>

**🔴 Write a team page and run a load check.** Pick one team from your map (or your own team, study group or open-source project). Write its team page with all six sections, then answer the four load-check questions honestly and propose one change if the load is too high.
*Done when:* the page fits on one screen, lists every owned item with a link or name, says how others should ask for things, and the load check ends with either "load is fine because…" or one concrete change (narrow scope, move to self-service, or split).

<details><summary>Model answer and self-check</summary>

**Model answer (Merchant Orders).** Mission: merchants create and follow orders without calling us. Owns: order service, statuses, merchant order screens, order dashboard. Work with us: team channel; changes through our backlog; order API on the developer portal. On-call: weekly rota for order alerts. Focus: "ready for pickup" used by 30% of merchants this quarter (illustrative). People: six engineers, a product manager, a shared designer. Load check: the team spends about a day a week on an old order export nobody uses; proposal: retire it after checking with Data & Analytics.

**Self-check.**
- Did your load check produce an action, not just a feeling?
- Did you avoid the reflex "add more people"?

</details>

## ⚠️ Mistakes and traps
- **Splitting by technical layer.** It makes every feature a relay race. Cut by the flow of change: a user journey or part of the product, owned end to end.
- **"Everyone owns it."** Shared ownership becomes no ownership. Name one team per part, even for shared services.
- **Enabling teams that never leave.** Coaching should end with the other team able to do the work. Set an end date.
- **Fixing overload by adding people.** Large teams split informally and slow down. Narrow scope or move work to self-service instead.

## 🧾 Recap
- Beyond one team, boundaries decide how work flows; draw them where little work needs to cross.
- Most teams should be product teams owning a part of the product end to end; platform, enabling and specialist teams exist to make them faster.
- Every part needs one owning team; every team needs a team page and a load it can carry.
- Rule: draw boundaries around the flow of change, not around the technology.

## ✍️ Check yourself
**1. A change to add "ready for pickup" touched the Apps, Core API, Data Infra and Analytics teams and took seven weeks. What is the most likely root cause?**

- A. The engineers on those four teams were not experienced enough to work at the right speed.
- B. The teams were split by technical layer, so every user-facing change had to cross all of them.
- C. The change was badly specified, so each team built its part to a slightly different meaning.
- D. The company was missing a project manager to chase each of the teams about the change every week.

<details><summary>Answer</summary>

**B.** Splitting by layer means a feature visible to users needs every layer team; the waiting, not the work, took seven weeks. C and D do not explain why every recent change crossed several teams, and A blames people for a structure problem. See "Two ways to cut".

</details>

**2. Which description best fits a product team?**

- A. A temporary group formed for one project, which disbands when the feature is delivered.
- B. A team of the same specialists, such as all the mobile developers, serving every product area.
- C. A team that sets the standards for engineering and approves other teams' designs before work.
- D. A long-lived team that owns one part of the product end to end, from building to running it.

<details><summary>Answer</summary>

**D.** A product team is long-lived and owns its part end to end, so most changes stay inside it. A describes a project team that leaves nobody owning the result, B is a layer team, and C is a review function, not a team that delivers. See "Product teams".

</details>

**3. Qafila's product teams queue for days for the platform team to create environments for them. What should change?**

- A. The platform team should make environment creation self-service, so product teams do it themselves.
- B. Each product team should hire its own platform engineer, so that it can stop waiting for others.
- C. The platform team should add staff and promise to process each environment request within a day.
- D. Product teams should plan environment requests a month ahead, so the platform team can schedule them.

<details><summary>Answer</summary>

**A.** A platform team's purpose is self-service; a queue means it is acting as a ticket desk. C shortens the queue but keeps it, D hides the wait in planning, and B multiplies the same work across twelve teams. See "Three more kinds of team".

</details>

**4. Salma's reliability experts have spent a year doing on-call for Live Tracking because "they know it best". What is the problem?**

- A. Reliability experts should never work with product teams, since it confuses who owns the work.
- B. Live Tracking should have been made a specialist team, because reliability is a rare skill.
- C. An enabling team should coach a team for a set time and then step back, not do its work for good.
- D. On-call is a platform service, so the platform team should take over Live Tracking's rota instead.

<details><summary>Answer</summary>

**C.** Enabling teams help others learn and then leave; doing the work permanently means Live Tracking never owns its own reliability. A goes too far (coaching is the point), B mislabels an ordinary product part, and D moves the same problem to another team. See "Three more kinds of team" and "Mistakes and traps".

</details>

**5. The Dispatch team says it is overloaded: it owns nine services, spends most of its time keeping them running, and new members take months to become useful. What is the best first response?**

- A. Narrow what the team owns, moving routine work to self-service or splitting along a seam in the flow.
- B. Add four more engineers to the team so that it has enough people to look after all nine of its services.
- C. Ask the team to work longer hours for one quarter while the backlog of running work is cleared.
- D. Merge Dispatch with Routing, so that one larger team shares the load and the knowledge between them.

<details><summary>Answer</summary>

**A.** The load check shows the team owns more than it can understand; reducing what it owns addresses the cause. B makes a large team that splits informally, C is not sustainable and fixes nothing, and D makes the load problem bigger. See "Team load".

</details>

## 📚 References
- Team Topologies, "Team Shape Templates" (GitHub, CC BY-SA 4.0; lists the model's team types and interaction modes; opened 2026-11-22): https://github.com/TeamTopologies/Team-Shape-Templates
- Skelton, M. and Pais, M., *Team Topologies: Organizing Business and Technology Teams for Fast Flow* (IT Revolution, 2019); site https://teamtopologies.com (full citation; the site could not be opened from this environment; its account of cognitive load is reported from search summaries).
- Conway, M. E., "How Do Committees Invent?", *Datamation* 14(4), April 1968 (citation and thesis as reported in search summaries; the paper itself was not opened).
- DORA, "Capabilities: Loosely coupled teams": https://dora.dev/capabilities/loosely-coupled-teams/ (found in search; could not be opened from this environment; the mention of the inverse Conway manoeuvre is as reported).
- Library course: [*Running IT as a Business*, lesson 2.2 — Designing a product-aligned operating model: product, platform and enabling teams](../itbiz/index.html#/2.2) (the manager's view).
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 0.1 — What cloud, DevOps, platform engineering and SRE are](../cloud/index.html#/0.1) (the engineering vocabulary).

---

# 8.2 — Dependencies, planning and coordination across teams
*Level: 🟡 Intermediate* · *Prerequisites: 6.1, 8.1* · *Step: Collaborate*

**After this you can** list the dependencies of a piece of work that crosses teams, sort them by kind, decide for each one whether to remove it, make it self-service, put it behind a clear contract or coordinate it, and keep a dependency register and a light cross-team plan that show who needs what from whom, by when. *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- A **dependency** is anything a team needs from outside itself before its work can be finished or used: another team's code change, an API, data, an expert, an approval, a shared environment. Each one is a place where work waits.
- Work through them in order: **remove**, make **self-service**, put behind a **contract** (a documented, versioned interface), and only then **coordinate** with dates and owners.
- The rule that matters most: **a dependency you cannot remove gets an owner, a date and a contract.**
- Decision cue: if work needs four or more teams to deliver at once, slice it until each slice lands in one or two.
- Biggest trap: changing an interface other teams use without warning, and calling the breakage "their problem".

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

Two things happened in the month after the new team map (lesson 8.1).

First, the Courier Earnings team tidied its earnings API (the interface other software calls to read a courier's earnings), renaming one field from `total` to `total_amount`. By that evening, Support Tools' support view showed every courier's earnings as zero and Data & Analytics' payout report was blank. Salma's desk took more than two hundred courier contacts. Nobody had known that two other teams read that field.

Second, Aisha and Maha announced the quarter's biggest bet: **scheduled deliveries**, letting merchants book a delivery for later. Every team nodded in the planning meeting. Six weeks later, Yasmin on Merchant Orders had built the booking screen, but nothing could be released: Dispatch was waiting for Routing to support future time slots, Routing had put that in "next quarter" because nobody had asked it directly, and Payments had not been told that scheduled deliveries needed a different charge time. "Who was supposed to know all this?" Yasmin asked. Nobody in particular. This lesson is about making dependencies visible, reducing them, and coordinating the ones that remain.

## 📐 How it works

### 🟢 The essentials

**What a dependency is.** A **dependency** exists when one team cannot finish or use its work until something outside the team happens. Dependencies come in several kinds, and each kind has its own remedy:

| Kind | What the team waits for | Qafila example | Usual remedy |
|---|---|---|---|
| **Code** | Another team to change its code | Routing must accept future time slots | Clear interface; move the boundary |
| **Interface (API)** | An API to exist or stay the same | Support Tools reads the earnings API | Versioned contract, change notice |
| **Data** | Data owned elsewhere | Analytics needs the "scheduled" status | Data definitions with owners (lesson 9.2) |
| **Expertise** | A person with rare knowledge | Two people understand the routing algorithm | Document, pair, enabling team |
| **Approval** | Someone outside to say yes | Security review for card data changes | Pre-agreed automated checks |
| **Shared resource** | A shared environment or tool | One staging environment for all | Self-service (lesson 8.3) |
| **Timing** | Another team to release first | Payments must change charge time first | Feature flag; plan the order |

**Reduce before you manage.** More meetings and tracking come last. Work down this ladder and stop at the first step that works:

1. **Remove it.** Slice the work so this team does not need the other, or move the boundary (lesson 8.1).
2. **Make it self-service.** Let the needing team do it itself with a tool or documented process (one environment per team; an automatic check instead of a manual approval).
3. **Put it behind a contract.** Document the interface, version it, and promise how changes will be announced.
4. **Coordinate it.** For what is left, agree an owner on each side, a date and how you will know it is done, written where both teams see it.

**The dependency register.** A **dependency register** is a shared list (a table, a board column, a page) of the dependencies that remain after the ladder. Each row says:

| Column | Example |
|---|---|
| **Needing team and owner** | Dispatch, its tech lead |
| **Providing team and owner** | Routing, its tech lead |
| **What, exactly** | Routing API accepts a requested pickup time up to 7 days ahead |
| **Needed by** | End of week 4 |
| **Kind** | Code and interface |
| **Status** | Agreed / in progress / done / at risk |
| **If late** | Scheduled deliveries launch for same-day slots only |

The last column matters most: it forces a fallback plan before one is needed.

### 🟡 Going deeper

**Interfaces as contracts.** An interface other teams call is a **contract**: a promise about what you can send, what you get back and what it means. The earnings outage happened because the contract was implicit. Make it explicit:

- **Document it** where callers can find it (lesson 8.3), including who calls it.
- **Prefer backward-compatible changes**, which do not break existing callers: adding an optional field is usually safe; renaming or removing one is not. To rename, add the new field, tell callers, wait until they have moved, then remove the old one. This "expand, then contract" pattern also works for database changes (lesson 3.3).
- **Label breaking changes.** Semantic Versioning (SemVer), a widely used free specification, increases the MAJOR version for incompatible API changes, MINOR for backward-compatible new functionality and PATCH for backward-compatible bug fixes. Even without version numbers, label every change as breaking or not before merging.
- **Announce and wait.** A breaking change needs a written notice to every caller (what, why, what they must do, by when) and time for them to plan.
- **Test the contract.** A **contract test** checks automatically that a provider still behaves as its callers expect. With Support Tools' expectations in Courier Earnings' pipeline, the rename would have failed before merging. See [*Software Testing*, lesson 2.2 — Integration testing: databases, queues, test data and contract tests](../testing/index.html#/2.2).

For how to design APIs that survive their callers, see [*System Design for Vibe Coders*, lesson 6.6 — API Design That Survives Its Clients](../vibe/index.en.html#l6-6).

**Who reviews what.** While much of Qafila's code still sits in one repository, a **code-owners file** (offered by several version-control hosts) maps folders to owning teams; on GitHub, for example, code owners are automatically asked to review pull requests that change their code (as described in GitHub's documentation, found in search).

**Planning across teams, lightly.** A company of twelve teams needs some shared planning, but not a planning machine. A light quarterly rhythm:

1. **Shared outcomes first:** a few company outcomes for the quarter (lesson 6.1).
2. **Each team drafts its plan,** including what it needs from others.
3. **A joint planning session** where teams post **needs** and **offers** side by side. Every need must meet a matching offer from a named team, or it is not a plan; unmatched needs are the session's most valuable output.
4. **Reserve capacity** for other teams' requests and surprises; write the figure down and check it against reality.
5. **A short weekly cross-team check** on the register only: what is at risk, late or needs a decision.
6. **One owner per cross-team initiative** (usually a product manager) keeps the whole picture; the parts stay with their teams.

**Slicing across teams.** Slice big bets so each slice is useful on its own and lands in as few teams as possible. Scheduled deliveries could start as "later today, one city", with Dispatch holding the booking and no Routing change at all.

**Decouple the releases.** A **feature flag** (a configuration switch that turns a feature on or off without a deployment, lesson 3.3) lets each team release its part when ready, switched off, and turn the whole feature on once all parts are live.

### 🔴 Expert view

**Adding people rarely rescues late cross-team work.** In *The Mythical Man-Month* (1975), Fred Brooks observed that adding people to a late software project makes it later, because newcomers need training and the number of communication paths grows faster than the number of people (as reported in summaries of the book). Adding a fifth team to a late four-team initiative likewise adds coordination faster than progress. Slice instead.

**Persistent dependencies are a design signal.** Two teams in the register quarter after quarter usually means a wrong boundary or a missing self-service offer. DORA's research programme describes **loosely coupled teams**, teams that can test, deploy and change their systems without depending on other teams, as a capability that predicts continuous delivery (as reported in search summaries of DORA's capability guide). Use the register as evidence at the twice-yearly team-map review (lesson 8.1).

**Watch the critical path.** The **critical path** is the longest chain of steps that must happen one after another; any delay on it delays the outcome. Put attention and fallback plans there.

**Escalate early, with options** (wait, slice down, workaround), not just "we are blocked".

**Do not build a coordination layer.** A layer of people whose job is chasing other people usually means the team structure and architecture need fixing. For the manager's view of planning and funding across many teams, see [*Running IT as a Business*, lesson 3.2 — Prioritising and funding work: business cases, cost of delay and funding products not projects](../itbiz/index.html#/3.2).

**The memorable rule.** A dependency you cannot remove gets an owner, a date and a contract.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Dependency register** | Shared table: who needs what from whom, by when, kind, status, "if late" | Any work needing more than one team |
| **Dependency ladder** | Remove, self-service, contract, coordinate, in that order | Every new dependency |
| **Needs and offers board** | Each team's needs and offers, every need matched to a named offer | Quarterly joint planning |
| **API change notice** | What, why, who is affected, what to do, by when, who to ask | Before any breaking interface change |
| **Contract test** | Automated check that a provider still meets its callers' expectations | Every interface another team relies on |
| **Code-owners file** | Maps folders to owning teams, who are asked to review changes | While teams share one repository |

## 🏛️ In practice at Qafila
Aisha took ownership of scheduled deliveries as a cross-team initiative and built the register with Yasmin. Illustrative and fictional.

> **Scheduled deliveries — dependency register (week 7 re-plan)**
>
> | Needing → providing | What exactly | Kind | Ladder decision | Needed by | If late |
> |---|---|---|---|---|---|
> | Dispatch → Routing | Accept a requested pickup time up to 7 days ahead | Code, interface | Removed for slice 1: Dispatch holds bookings until the booked time | Slice 2 only | Slice 1 unaffected |
> | Merchant Orders → Payments | Charge at pickup time, not at booking | Timing | Contract: optional `charge_at` field | Week 9 | Launch with charge at booking, refunds on cancel |
> | Merchant Orders → Data & Analytics | Report scheduled orders separately | Data | Self-service: Merchant Orders adds the status to the shared data definitions | Week 10 | Report a week later |
> | Courier Experience → Merchant Orders | Show "scheduled" label on courier job card | Interface | Coordinate | Week 10 | Couriers see a normal job |
> | All → Platform | A test environment per team for the feature | Shared resource | Self-service (lesson 8.3) | Week 8 | Share staging, book slots |
>
> **Slice 1:** later-today bookings, one city, behind a feature flag. **Critical path:** Payments `charge_at` → end-to-end test → switch on.
>
> **API change notice (Courier Earnings, after the outage):** "We will add `total_amount` and keep `total` until 30 days after the last known caller has moved. Known callers: Support Tools, Data & Analytics, whose contract tests now run in our pipeline."

The first draft had 23 rows; applying the ladder removed eleven. Faisal wanted Routing in "because the full feature needs it"; Aisha moved it to slice 2. Dana asked to see the charge-time change; instead of a meeting, Payments added a pipeline check she had agreed in advance. Slice 1 went live in week 11 in one city.

## 🛠️ Exercises
**🟢 Sort the dependencies.** Here are six fictional needs from Qafila teams: (1) Live Tracking needs Courier Experience to send location every 10 seconds instead of 30; (2) Support Tools reads the order status API; (3) Payments needs Dana's sign-off on any change to card handling; (4) every team shares one staging environment; (5) only one Routing engineer understands the ETA model; (6) Merchant Onboarding must release its new branch screen before Merchant Orders can show branch names on orders. Give each one a kind from the table in this lesson and a first rung on the ladder.
*Done when:* all six have a kind and a ladder step, and at least two are "remove" or "self-service" rather than "coordinate".

<details><summary>Model answer and self-check</summary>

**Model answer.** (1) Code/interface; contract, or remove by letting Live Tracking own the location-sending code. (2) Interface; contract with a contract test. (3) Approval; self-service through pre-agreed automated checks. (4) Shared resource; self-service, one environment per team. (5) Expertise; coordinate now, plus pairing and documentation. (6) Timing; remove with a feature flag.

**Self-check.**
- Did you try "remove" and "self-service" before "coordinate"?
- Did you treat the single expert as a risk to reduce, not just a person to book?

</details>

**🟡 Write an API change notice.** Use the Courier Earnings rename, or a MAJOR release in an open-source library you use (see its changelog). Write a change notice with all six parts, and plan the expand-then-contract steps.
*Done when:* the notice names who is affected, what they must do and by when; the steps keep the old behaviour working until callers have moved; and you have labelled the change MAJOR, MINOR or PATCH in SemVer terms.

<details><summary>Model answer and self-check</summary>

**Model answer.** What: `total` will be replaced by `total_amount`. Why: consistent naming. Who: Support Tools, Data & Analytics (other callers, please tell us). What to do: read `total_amount`, available today. By when: `total` goes no earlier than 30 days after the last known caller confirms. Ask: Courier Earnings channel. Steps: add `total_amount` (MINOR); callers switch; contract tests updated; remove `total` (MAJOR) after confirmation.

**Self-check.**
- Is there any moment when a caller's code would break? If so, add a step.
- Is the removal tied to callers moving, not just to a calendar date?

</details>

**🔴 Re-plan a cross-team initiative.** Take scheduled deliveries (or any feature you can imagine that needs four or more teams, such as "merchant loyalty points"). Build a dependency register, apply the ladder to every row, slice the work so the first slice needs as few teams as possible, mark the critical path, and write the "if late" column.
*Done when:* the first slice is useful to real users on its own, needs no more than two or three teams, every remaining row has owners on both sides and a date, and the critical path is named.

<details><summary>Model answer and self-check</summary>

**Model answer (merchant loyalty points).** The full version needs five teams. Slice 1: merchants see a count of repeat customers on their dashboard (Data & Analytics query, Merchant Orders screen): two teams. Slice 2: points per order (Merchant Orders; Payments contract for a discount at charge time). Slice 3: support view (Support Tools). Critical path for slice 2: Payments discount field → end-to-end test → flag on. If Payments is late: launch earning without redeeming.

**Self-check.**
- Did slicing remove dependencies, or just postpone them all to slice 2?
- Is your first slice something merchants would notice and use?

</details>

## ⚠️ Mistakes and traps
- **Managing dependencies instead of removing them.** Apply the ladder first; coordinate only what is left.
- **Silent interface changes.** Renaming or removing a field breaks callers you do not know about. Expand, announce, wait, then contract, with contract tests.
- **Nodding in planning.** Agreement in a meeting is not a commitment. Every need must match a named offer with a date, in writing.
- **All-or-nothing launches.** A feature that needs five teams to finish at once rarely ships on time. Slice it, and use feature flags to decouple releases.
- **Treating repeat dependencies as normal.** The same pair of teams in the register every quarter is a team-boundary or architecture problem; take it to the team-map review.

## 🧾 Recap
- A dependency is anything a team waits for from outside itself; each kind has its own remedy.
- Work down the ladder: remove, make self-service, put behind a contract, then coordinate.
- Interfaces other teams use are contracts: document them, change them compatibly, announce breaking changes and test them automatically.
- Plan across teams lightly: shared outcomes, needs matched to offers, reserved capacity, a short weekly check and one owner per initiative.
- Rule: a dependency you cannot remove gets an owner, a date and a contract.

## ✍️ Check yourself
**1. Courier Earnings renamed a field in its earnings API, and two other teams' features broke the same evening. What would most directly have prevented this?**

- A. A rule that every API change must be approved by the Head of Engineering before it is merged.
- B. A monthly meeting where all teams present the changes they plan to make to their services.
- C. Add the new field first, tell callers, and run their contract tests before removing the old one.
- D. Moving Support Tools and Data & Analytics into the Courier Earnings team so they share one backlog.

<details><summary>Answer</summary>

**C.** Expand-then-contract keeps callers working, the notice tells them what to do, and contract tests catch a break before merging. A and B add slow manual steps that rely on someone noticing; D merges teams to fix a missing contract. See "Interfaces as contracts".

</details>

**2. Dispatch cannot start scheduled deliveries until Routing supports future time slots, and Routing has scheduled that for next quarter. What should the team try first?**

- A. Slice it so the first version needs no Routing change, for example Dispatch holding the bookings.
- B. Escalate to Maha and ask her to order Routing to move the work into the current quarter's plan.
- C. Add two engineers from Merchant Orders to the Routing team, so that Routing can finish it sooner.
- D. Record the dependency in the register as "at risk" and wait for Routing's next planning session.

<details><summary>Answer</summary>

**A.** The ladder starts with removing the dependency; slicing lets the first slice ship without Routing. B and D coordinate before trying to remove it, and C adds people to a specialist team, which usually slows it first. See "Reduce before you manage" and "Slicing across teams".

</details>

**3. In Qafila's joint planning session, Merchant Orders lists "Payments: charge at pickup time" as a need, but Payments has no matching offer. What does this mean?**

- A. The plan is fine, because Payments heard the need in the room and can add it later during the quarter.
- B. Merchant Orders should build the charging change itself in the Payments code to avoid waiting.
- C. The planning session failed and should be repeated next week with all of the teams present.
- D. It is a gap to resolve right now: agree an owner and a date, change the slice, or plan a fallback.

<details><summary>Answer</summary>

**D.** An unmatched need is exactly what joint planning is for finding; it needs a decision now. A repeats the "everyone nodded" failure, B breaks ownership of the payments code, and C treats a useful finding as a failure. See "Planning across teams, lightly".

</details>

**4. Which change to an API that other teams call is backward compatible?**

- A. Renaming the field `total` to `total_amount` so that names are consistent with other APIs.
- B. Adding a new optional field `charge_at` that existing callers can ignore if they do not need it.
- C. Changing the `amount` field from whole riyals to fils without changing the name of the field.
- D. Removing the `legacy_id` field, since the provider team believes that no caller still reads it today.

<details><summary>Answer</summary>

**B.** Existing callers keep working when an optional field is added. A and D break callers that read the old field, and C is the most dangerous: same name, different meaning, so callers silently compute wrong values. See "Interfaces as contracts".

</details>

**5. Data & Analytics and Merchant Orders appear together in the dependency register for the third quarter running. What is the best interpretation?**

- A. The two teams have a good working relationship and should keep coordinating the same way.
- B. Data & Analytics is too slow and should be asked to reserve much more capacity for Merchant Orders.
- C. The register is too detailed and should only track dependencies that are already at risk.
- D. The boundary or interface between them probably needs changing; raise it at the team-map review.

<details><summary>Answer</summary>

**D.** Persistent dependencies are a design signal: move the boundary or make the providing side self-service. A accepts a lasting cost, B blames one team for a structural issue, and C hides the evidence. See "Persistent dependencies are a design signal".

</details>

## 📚 References
- Semantic Versioning 2.0.0 specification, summary (source text on GitHub; opened 2026-11-22): https://github.com/semver/semver/blob/master/semver.md — public site https://semver.org
- GitHub Docs, "About code owners" (found in search; not opened): https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- DORA, "Capabilities: Loosely coupled teams" (found in search; could not be opened from this environment; content as reported): https://dora.dev/capabilities/loosely-coupled-teams/
- Brooks, F. P., *The Mythical Man-Month: Essays on Software Engineering* (Addison-Wesley, 1975; anniversary edition 1995). Full citation; the statement of Brooks's law is as reported in summaries.
- Library course: [*Software Testing*, lesson 2.2 — Integration testing: databases, queues, test data and contract tests](../testing/index.html#/2.2).
- Library course: [*System Design for Vibe Coders*, lesson 6.6 — API Design That Survives Its Clients](../vibe/index.en.html#l6-6).
- Library course: [*Running IT as a Business*, lesson 3.2 — Prioritising and funding work: business cases, cost of delay and funding products not projects](../itbiz/index.html#/3.2).

---

# 8.3 — Internal platforms and developer experience
*Level: 🟡 Intermediate* · *Prerequisites: 3.3, 4.1, 8.1* · *Step: Collaborate*

**After this you can** explain what an internal platform is and why it should be run as a product, write a golden-path checklist for one common task (such as starting a new service), describe a platform on one page (users, offer, measures), and run a short developer-experience survey whose results point to one improvement. *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- An **internal platform** is the shared tools, templates and documentation product teams use to build, ship and run software, offered as **self-service**, without waiting for anyone.
- A **golden path** (or paved road) is the supported, recommended way to do a common task, with good defaults (tests, pipeline, monitoring, secrets) built in.
- **Developer experience** is how much effort engineers spend getting work done: how fast they get feedback, how much they must hold in their heads, how often they can focus.
- The rule that matters most: **run the platform as a product, and make the right way the easy way.**
- Decision cue: if several teams build the same thing by hand, it is a platform candidate; if no team asked for it, it is not, yet.
- Biggest trap: building a large platform nobody asked for, then forcing teams to use it.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

Yasmin was asked to set up a small new service to send "ready for pickup" alerts to couriers. There was no standard way to start one. She copied the most recent service, then spent days removing what did not apply, asking in four channels why the pipeline failed, and waiting two days for someone to create a database. It reached production after eleven working days; the code that did the work had taken two.

She had also copied a cloud access key sitting in a configuration file, a pattern from the early days. A few months earlier, an engineer had pushed a similar service to a public repository for a demo, key included; the key was misused for a few hours before it was revoked. That scare is why Qafila hired Dana as security and risk lead. She found that every team copied set-up from the nearest service, inheriting its mistakes.

Faisal formed a Platform team from four engineers already doing this work informally. Dana's first request was not a new rule: "Make the safe way the quickest way to start a service." This lesson is about building that.

## 📐 How it works

### 🟢 The essentials

**What an internal platform is.** An **internal platform** is what a company provides once, centrally, so each product team does not build it again. The CNCF (Cloud Native Computing Foundation) platforms working group's glossary is reported to describe a platform as portals, APIs, command-line tools, documentation, standards and golden-path templates (as reported in search summaries). At a company like Qafila it typically includes:

| Platform part | What it gives a product team | Without it |
|---|---|---|
| **Service template** | A new service with folder layout, tests, pipeline and monitoring already set up | Copy an old service and its old mistakes |
| **Delivery pipeline** | Build, test, security checks and deploy on every merge (lessons 3.2, 3.3) | Each team maintains its own scripts |
| **Environments** | A test environment per team or per change, created on demand | Queue for one shared staging environment |
| **Secrets management** | A safe store for keys and passwords, read by services at run time | Keys in configuration files and chat messages |
| **Observability defaults** | Logs, metrics, dashboards and standard alerts for every service (lesson 4.2) | Each team guesses what to measure |
| **Developer portal** | One place to find every service, its owner, its documentation and its API | Ask around in chat |

**Self-service is the point.** A platform that answers requests ("please create a database") is a ticket desk with a new name. The measure: how often does a product team wait for the platform team?

**Golden paths.** A **golden path** is the supported, recommended route for a common task. Spotify's engineering blog described its Golden Paths in 2020 as a response to fragmentation in its tools and practices: an opinionated and supported way to build something, with tutorials per kind of work (as reported in search summaries of the post). Two features matter: it is **the easy way**, faster than going alone because the defaults are done; and it is **supported, not forced**: teams may leave it with a reason, but then own what the path would have handled.

**Run the platform as a product.** Its users are other engineers: treat them like customers (Module 1), learn what slows them down, offer the smallest thing that helps, and measure adoption. The *Team Topologies* authors are reported to recommend a **thinnest viable platform**, building no more platform than needed, which might begin as no more than a well-kept wiki page (as reported in search summaries). 

### 🟡 Going deeper

**What developer experience means.** **Developer experience** (DevEx or DX) is how engineers experience building and shipping software: tools, processes and environment. A 2023 article in *ACM Queue*, "DevEx: What Actually Drives Productivity" by Abi Noda, Margaret-Anne Storey, Nicole Forsgren and Michaela Greiler, describes three dimensions (as reported in search summaries):

| Dimension | Plain meaning | Qafila example of poor DevEx | Platform fix |
|---|---|---|---|
| **Feedback loops** | How quickly you learn whether your change works | Pipeline takes 40 minutes; review waits a day | Faster pipeline; test environment per change |
| **Cognitive load** | How much you have to know and keep in your head to do a task | Starting a service means knowing nine tools and four teams | One template, one portal page |
| **Flow state** | How often you can work with full, uninterrupted focus | Constant pings asking who owns what | Owners and docs findable without asking |

The article is reported to warn that DevEx is not only about tools.

**Measuring without a single number.** A 2021 *ACM Queue* article by Nicole Forsgren and colleagues, "The SPACE of Developer Productivity", is reported to argue that productivity cannot be captured by one metric, and to describe five dimensions: satisfaction and well-being, performance, activity, communication and collaboration, and efficiency and flow (as reported in search summaries). So combine a few kinds of measure:

- **Ask people:** a short quarterly survey, plus "What slowed you down most this month?"
- **Measure the path:** time from "new service" to production; pipeline duration; a new engineer's time to a first production change.
- **Measure adoption:** share of services from the template or using the secrets store.

Do not measure individuals by commits or lines of code: easy to game, and silent on whether the work got easier.

**A platform team's product practices:** watch users work and read the help channel; publish a one-page offer; document first (undocumented features do not exist for users); keep a public roadmap; run the platform reliably, with its own on-call and incident reviews (lesson 4.3), since everyone now depends on it; and retire old paths with notice (lesson 8.2).

**Onboarding is a platform test.** A new engineer's time to a first production change is one of the clearest DevEx signals. For the newcomer's side, see [*From Graduate to Hired*, lesson 6.2 — Your first 90 days: onboarding, the first pull request and asking good questions](../career/index.html#/6.2).

### 🔴 Expert view

**What the research found.** Google Cloud's announcement of the 2024 DORA report (DORA is DevOps Research and Assessment, a long-running research programme on software delivery) lists four findings on platform engineering: internal development platforms increased developer productivity; they were more common in larger organisations; a platform initiative "might lead to a temporary decrease in performance before improvements manifest as the platform matures"; and for best results, platform efforts should prioritise user-centred design, developer independence and a product-oriented approach. These are survey findings, not guarantees. Expect a dip, say so in advance, and keep listening to users.

**Guardrails, not gates.** A **gate** stops work until a person approves it. A **guardrail** is an automatic check in the path that blocks only what is clearly unsafe. Dana's secrets rule became a guardrail: the template reads secrets from the store, and the pipeline blocks any merge containing a key. Nobody waits for Dana. For the engineering detail, see [*Cloud & DevOps: Zero to Hero*, lesson 3.3 — Policy as code, drift and guardrails](../cloud/index.html#/3.3).

**Mandatory or optional?** Mandating everything gets quick adoption and loses the feedback on whether the platform is good. A common middle ground: a few guardrails mandatory (secrets, access, basic monitoring), the rest optional but convenient. Teams leaving the path is user research, not disobedience.

**Build, buy or assemble.** Platform parts can be built, bought or assembled from open source; Backstage, for example, is an open-source framework for developer portals, created by Spotify and hosted by the CNCF (an example, not an endorsement). Follow lesson 2.3: build only what is specific to you. For the manager's view of a pipeline run as a managed capability, see [*Running IT as a Business*, lesson 5.1 — Delivery pipelines as a managed capability](../itbiz/index.html#/5.1).

**The memorable rule.** Run the platform as a product, and make the right way the easy way.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Platform one-pager** | Users, offer, how to start, help, what is next, measures | When a platform team forms; each quarter |
| **Golden-path checklist** | Steps and built-in defaults for one common task | For each task several teams do by hand |
| **Service template** | Starter repository with tests, pipeline, monitoring and secrets handling | Once two teams start services the same way |
| **Developer portal** | Every service with owner, docs and API (for example, open-source Backstage; not an endorsement) | When "who owns this?" is a daily question |
| **DevEx survey** | Five or six questions on feedback, load and focus, plus one open question | Every quarter, results shared openly |
| **Path measures** | Time to a new service in production, pipeline duration, adoption share | Monthly |

## 🏛️ In practice at Qafila
The Platform team's first quarter, with Yasmin seconded to it for six weeks as the "first user". Illustrative and fictional.

> **Qafila Platform — one-pager (v1)**
>
> | Item | Content |
> |---|---|
> | Users | Engineers in the eleven other teams (about 70 people) |
> | Problem | Starting a service takes about eleven working days, copies old mistakes, and needs four teams |
> | Offer v1 | Service template; secrets store; standard dashboards and alerts; one test environment per team, self-service |
> | Mandatory guardrails | Secrets only from the store (pipeline blocks committed keys); every service listed with an owner in the portal; standard alerts on |
> | Optional golden path | Everything else in the template: folder layout, test set-up, deployment steps |
> | Help | Platform channel, answered within half a working day; office hours on Wednesdays |
> | Measures | Time from "new service" to production; share of new services from the template; quarterly DevEx survey |
> | Next | Faster pipeline (currently 40 minutes); a portal page for every API (lesson 8.2) |
>
> **Golden path: start a new service (checklist)**
> 1. Run the template generator with the service name and owning team.
> 2. Template creates the repository, code-owners entry, pipeline, dashboards and alerts.
> 3. Request secrets through the store's self-service page; the service reads them at run time.
> 4. Register the service in the portal: owner, purpose, API documentation link.
> 5. Merge the first change; the pipeline deploys to the team's test environment, then production behind a feature flag.
>
> **DevEx survey, first round (about 60 answers):** easiest: deploying an existing service. Hardest: getting a test environment, finding who owns an API, understanding pipeline failures. Most common answer to "what slowed you down most?": waiting for review from another team.

Yasmin rebuilt her pickup-alert service with the first template, timing every step: two days instead of eleven, and four sticking points fixed before launch. Faisal wanted the whole template mandatory; Dana argued for three guardrails and an optional path, and eight of the next nine services used it anyway. The top survey complaint (waiting for other teams' reviews) went to the team-map review (lesson 8.1). The first month was slower while teams learned, as the platform lead had warned.

## 🛠️ Exercises
**🟢 Spot the platform candidates.** Qafila teams do these: (1) set up a pipeline for a new service; (2) design the loyalty screen; (3) create a test database; (4) tune the routing algorithm; (5) add standard alerts; (6) store the payment provider's API key; (7) write a help article; (8) find the owner of the earnings API. Mark each "platform candidate" or "product team work", with a one-line reason.
*Done when:* every item is marked with a reason, and each platform candidate is something several teams do in much the same way.

<details><summary>Model answer and self-check</summary>

**Model answer.** Platform candidates: (1) pipeline set-up, (3) test database, (5) standard alerts, (6) secrets storage, (8) ownership lookup (portal): every team does these the same way. Product team work: (2) the loyalty screen, (4) the routing weighting, (7) the help article: each is specific to one product area and needs its knowledge.

**Self-check.**
- Did you avoid putting product decisions (screens, algorithms) on the platform?
- Did you notice that (6) is both a convenience and a security guardrail?

</details>

**🟡 Write a golden-path checklist.** Pick a common task in a project you know (setting up a development laptop, adding a page to a website, publishing a package) or Qafila's "a new engineer's first production change". Write a five-to-eight-step checklist and mark the defaults the path provides.
*Done when:* someone who has never done the task could follow it, each step is one action, the safe defaults (tests, secrets, monitoring or equivalent) are built in rather than left to the user, and you have timed or estimated how long it takes.

<details><summary>Model answer and self-check</summary>

**Model answer (new engineer's first change at Qafila).** 1. Run the laptop set-up script. 2. Read the portal page "Your first week". 3. Clone the team repository; run tests with one command. 4. Pick a small "first change" item from the board. 5. Open a pull request; code owners and a buddy review it. 6. The pipeline tests, checks and deploys to the test environment. 7. After merge, it reaches production behind a flag. Defaults: tool versions, access groups, pipeline checks, secrets, dashboards. Target: first week (illustrative).

**Self-check.**
- Is there any step where the newcomer must ask someone a question? Can the path answer it instead?
- Did you build the safe choice in, rather than adding a "remember to…" step?

</details>

**🔴 Design a platform one-pager and a DevEx survey.** For Qafila's Platform team (or the shared tools of an open-source or study project), write a one-pager with the eight rows from this lesson and a quarterly survey of five or six questions covering feedback loops, cognitive load and flow, plus one open question. Name the measure that would show, in three months, whether the platform helped.
*Done when:* the one-pager names its users and one problem in numbers, separates mandatory guardrails from the optional path with a reason for each guardrail, the survey covers all three DevEx dimensions, and you have chosen one or two measures with a starting value.

<details><summary>Model answer and self-check</summary>

**Model answer (survey, 1–5 scales).** (1) How quickly do you learn whether a change works? (feedback) (2) How easy is it to get a test environment? (feedback) (3) How easy is it to find the owner and docs of a service you depend on? (load) (4) How easy was it to start your last piece of work without help? (load) (5) How often do you get two uninterrupted hours in a week? (flow) (6) What slowed you down most this month? Measures: time from "new service" to production (start: about eleven working days, illustrative); share of new services from the template (start: zero).

**Self-check.**
- Does every mandatory guardrail protect customers or the company, rather than being someone's preference?
- Are your measures about the work getting easier, not about how busy individuals are?

</details>

## ⚠️ Mistakes and traps
- **Building a platform nobody asked for.** Start from what several teams already do by hand and find painful; build the thinnest thing that helps.
- **A platform that takes tickets.** If teams wait for the platform team, it is a bottleneck. Aim for self-service and measure waiting.
- **Making everything mandatory.** You lose feedback. Mandate a few guardrails; make the rest attractive.
- **Measuring individuals.** Commit counts invite gaming. Measure the path, adoption and what people tell you.
- **Expecting instant gains.** DORA reported that platform initiatives may bring a temporary dip before improvements. Say so in advance and keep listening.

## 🧾 Recap
- An internal platform offers shared tools, templates and documentation as self-service.
- Golden paths make the recommended way the easiest way; a few guardrails are mandatory, the rest is supported and optional.
- Developer experience covers feedback loops, cognitive load and flow; measure it with surveys, path timings and adoption, never with one number.
- DORA's 2024 research reported productivity gains from internal platforms, a possible early dip, and best results when user-centred.
- Rule: run the platform as a product, and make the right way the easy way.

## ✍️ Check yourself
**1. Yasmin's new service took eleven working days to reach production, though the code took two. What is the best first platform response?**

- A. Write a policy that every new service must be reviewed by the Platform team before it can be created.
- B. Offer a service template and self-service steps that make starting any new service quick and safe.
- C. Ask each product team to keep one engineer who specialises in setting up new services for it.
- D. Reduce the number of new services by asking teams to add features to the existing ones instead.

<details><summary>Answer</summary>

**B.** A self-service template removes the nine days of set-up and builds in safe defaults. A adds a gate, C repeats the work in twelve teams, and D bends the architecture to avoid the problem. See "Golden paths" and "Self-service is the point".

</details>

**2. After the access-key incident, Dana wants to make sure no service has keys in its code. Which approach best fits this lesson?**

- A. Ask Dana to review every pull request that touches configuration files before it can be merged.
- B. Send all engineers a reminder each month about not committing keys, with a short training video.
- C. Template reads secrets from the store, and the pipeline blocks any merge that contains a key.
- D. Move all services into one repository so that the security team can watch every change made.

<details><summary>Answer</summary>

**C.** A guardrail on the golden path makes the unsafe action impossible without making anyone wait. A is a gate that turns Dana into a bottleneck, B relies on memory, and D changes the repository layout without stopping the mistake. See "Guardrails, not gates".

</details>

**3. Which set of measures best tells Qafila's Platform team whether developer experience is improving?**

- A. Time from "new service" to production, template adoption, and a quarterly developer survey.
- B. The number of commits and lines of code each engineer produces per week, compared by team.
- C. The number of tickets the Platform team closes each month, and how fast it closes them all.
- D. The number of tools the Platform team runs, and the total spending on its cloud resources.

<details><summary>Answer</summary>

**A.** Path timings, adoption and what people say cover the experience from several sides. B invites gaming, C rewards a ticket-desk platform, and D measures size, not experience. See "Measuring without a single number".

</details>

**4. In the platform's first month, delivery at Qafila got slightly slower while teams learned the template. What is the best reading?**

- A. The template has failed and should be withdrawn before more teams start depending on it.
- B. Delivery should be measured only after six months, so that early results do not confuse anyone.
- C. The product teams are resisting the change and should be required to use the template fully.
- D. DORA reported that such an early dip can happen; keep listening to users and keep tracking it.

<details><summary>Answer</summary>

**D.** DORA's 2024 findings mention a possible temporary dip; warn people and keep improving from feedback. A overreacts, B hides evidence, and C treats a learning cost as disobedience. See "What the research found".

</details>

**5. Several teams leave the golden path to use their own deployment scripts. What should the Platform team do first?**

- A. Make the golden path mandatory for all teams and remove their access to any other deployment route.
- B. Accept it, because golden paths are optional and teams are free to choose their own way.
- C. Find out why they left, treating their reasons as user research to improve the golden path itself.
- D. Report the teams to the Head of Engineering so that it can be raised in their reviews.

<details><summary>Answer</summary>

**C.** Teams leaving a convenient path is a signal about the path; learning why is product practice. A loses that feedback, B ignores it, and D punishes users for a product problem. See "Mandatory or optional?".

</details>

## 📚 References
- Google Cloud blog, "Announcing the 2024 DORA report" (October 2024; sections on platform engineering and developer experience; opened 2026-11-22): https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
- Noda, A., Storey, M.-A., Forsgren, N. and Greiler, M., "DevEx: What Actually Drives Productivity", *ACM Queue*, 2023: https://queue.acm.org/detail.cfm?id=3595878 (found in search; not opened; as reported).
- Forsgren, N., Storey, M.-A., Maddila, C., Zimmermann, T., Houck, B. and Butler, J., "The SPACE of Developer Productivity", *ACM Queue* 19(1), 2021: https://queue.acm.org/detail.cfm?id=3454124 (found in search; not opened; as reported).
- Spotify Engineering, "How We Use Golden Paths to Solve Fragmentation in Our Software Ecosystem" (August 2020): https://engineering.atspotify.com/2020/8/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem (found in search; not opened; as reported).
- CNCF TAG App Delivery, Platforms working group glossary: https://tag-app-delivery.cncf.io/wgs/platforms/glossary/ (found in search; not opened; as reported).
- Backstage repository README (opened 2026-11-22): https://github.com/backstage/backstage
- Skelton, M. and Pais, M., *Team Topologies* (IT Revolution, 2019). Full citation; "thinnest viable platform" as reported in search summaries.
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 3.3 — Policy as code, drift and guardrails](../cloud/index.html#/3.3).
- Library course: [*Running IT as a Business*, lesson 5.1 — Delivery pipelines as a managed capability](../itbiz/index.html#/5.1).
- Library course: [*From Graduate to Hired*, lesson 6.2 — Your first 90 days: onboarding, the first pull request and asking good questions](../career/index.html#/6.2).
