# Module 8 — Many teams

*Qafila is now at Scale-up. About 120 people work there in twelve teams, one of them a new platform team. About 9,000 merchants use the app for about 120,000 deliveries a day, teams deploy to production many times a day, and a routing service now decides which courier takes which order. At this size the hard problems are no longer inside one team: they sit between teams. Who owns the courier payout screen? Why does one small change need four teams to agree? Why does every new service start with two weeks of copying set-up from an older one? This module covers the practice of working as many teams, seen from the inside by Yasmin, now in her second year as an engineer. First, drawing team boundaries on purpose, with clear ownership and a sensible load for each team. Second, finding, reducing and managing the dependencies between teams, and planning together without a planning machine. Third, building an internal platform that other engineers choose to use, and measuring their experience of it. Each lesson leaves an artefact: a team map with one team page, a dependency register with a cross-team plan, and a platform one-pager with a golden-path checklist and a short developer-experience survey.*

> **Steps:** Collaborate — shape teams around the work, keep the links between them few and clear, and give every team a paved road so that many teams can move fast without tripping over each other.

---

# 8.1 — Team structures and boundaries: product, platform and enabling teams
*Level: 🟡 Intermediate* · *Prerequisites: 5.1, 5.3* · *Step: Collaborate*

**After this you can** draw a team map for a growing product (which team owns which part, what role each team plays, and how each pair of teams connects), write a one-page team page for one team, and spot the two most common boundary problems: work split by technical layer, and a team that owns more than it can understand. *Study time: reading about 15 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- Past one team, **where you draw boundaries decides how work flows.** A change across three teams waits at every hand-off.
- Most teams should **own one part of the product end to end**. A few play supporting roles: offering shared tools as self-service, coaching for a while, or holding rare expertise behind a clear interface.
- **Ownership** means one team answers for each part: its code, changes, alerts and users' problems.
- The rule that matters most: **draw boundaries around the flow of change, not around the technology.**
- Decision cue: if most changes need two or more teams, or a team cannot explain everything it owns, the boundary is wrong.
- Biggest trap: splitting teams by layer (an app team, a back-end team, a database team), so every user-facing change becomes a relay race.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

Qafila grew to about 120 people. Whenever a group got too big, it split by skill: the mobile developers became "Apps", the back-end developers (who build the services and data behind the screens) "Core API", two database specialists "Data Infra", Hamad's analysts "Analytics".

Then a merchant chain asked for something simple: let a shop mark an order as "ready for pickup", so couriers stop arriving early. Yasmin, now in her second year, picked it up. The button lived in the merchant app (Apps), the status in the order service (Core API), which needed a new column (Data Infra), and Hamad wanted it in reports (Analytics). Four teams, four backlogs: about a week of work took seven weeks to reach merchants.

Nobody was slow. The structure made every user-facing change cross every team.

## 📐 How it works

### 🟢 The essentials

**Why one big team stops working.** A group of *n* people has *n × (n − 1) / 2* possible one-to-one conversation paths: 66 for twelve people, 7,140 for 120. So people split into teams. The question is *where*: every boundary becomes a place where work waits.

**Structure shapes the product.** In a 1968 paper in *Datamation*, "How Do Committees Invent?", Melvin Conway argued that organisations which design systems are constrained to produce designs that copy their own communication structures (as reported; the idea is now called **Conway's law**). Parts that change independently need teams that can change independently.

**Two ways to cut.** There are two basic ways to split work between teams:

| Cut | What a team owns | What happens to a typical change | Example at Qafila |
|---|---|---|---|
| **By layer or technology** | One technical layer for the whole product (mobile, back end, database) | Crosses every layer, so every team | Apps, Core API, Data Infra |
| **By flow of change** | One part of the product end to end, for one user group or journey | Usually stays inside one team | Merchant Orders: merchant screens, order service, its data |

Cutting by layer feels natural, but users experience journeys (placing an order, being paid, tracking a delivery), not layers.

**Product teams.** A **product team** is a long-lived team that owns one part of the product and the change that flows through it. It has the skills to build, ship and run that part without waiting for others, and the right to deploy. Most teams in a healthy company of 120 people are product teams.

**Ownership.** Write down one owning team for each part. Owning means:

- the team decides what changes in that part, and in what order;
- the team reviews and merges changes to its code;
- the team's on-call rota answers that part's alerts (lesson 4.2);
- the team is the place support sends that part's problems (lesson 7.1).

A part with two owners, or "owned by everyone", has none.

### 🟡 Going deeper

**Supporting roles.** For each remaining piece of work, ask: *what would let product teams stop waiting for it?* The answer gives a supporting role. A team can play more than one.

| Role | Choose it when | How product teams use it | Warning sign |
|---|---|---|---|
| **Offer shared tools as self-service** | Many teams need the same thing (pipelines, environments, storage for **secrets**, meaning keys and passwords) | Without a ticket or a conversation | Product teams queue for someone to do it for them |
| **Coach for a while** | Teams lack a skill they will need for good (reliability, security, testing) | Side by side, until an end date | The coaches end up doing the work permanently |
| **Hold rare expertise** | One part needs deep knowledge few can learn (a routing algorithm) | Through a clear interface (an **API**, a defined way for software to call another piece of software) | The part is "rare" only because nobody wrote it down |

In everyday speech, a team whose main role is self-service is a **platform team** (lesson 8.3) and one whose main role is coaching is an **enabling team**. Other writers sort teams differently: the book *Team Topologies* by Matthew Skelton and Manuel Pais (IT Revolution, 2019) proposes a fuller model of team types and named interactions. This lesson does not teach that model; lesson 12.3 shows where such frameworks fit.

**How teams connect.** For each pair of teams that must interact, write down how. The default is a **documented self-service interface**: an API, a tool or a written process used without a meeting. **Close joint work** suits something new and uncertain, such as designing an interface; it is expensive, so give it an end date. If two teams need joint work all the time, move the boundary or merge them.

**Team load check.** A team can only carry so many services, technologies and on-call duties. This course checks it with four questions:

1. Can the team explain, without notes, what each thing it owns does and why?
2. How much of its time goes to keeping things running rather than improving them?
3. How often does it wait for someone outside the team for a routine change?
4. Does a new member understand the team's area within a few weeks?

If the answers are bad, do not just add people. Narrow what the team owns, move routine needs to self-service, or split the team along a seam in the flow of change.

**The team page.** Each team keeps a short public page so others can work with it without a meeting. This course's version has five parts:

| Part | What goes in it |
|---|---|
| **Purpose** | One sentence: which users, which part of the product, which outcome |
| **Ownership list** | Every service, app, data store and dashboard the team owns, each linked |
| **Ask us, or do it yourself** | What other teams can do through self-service, and where to ask for the rest |
| **Our promises** | Alert and support response times, and how much notice we give before changing an interface (lesson 8.2) |
| **Last load check** | Date, the four answers, any change agreed |

### 🔴 Expert view

**Design the teams for the product you want.** Because structure shapes the product, some organisations change team boundaries first, on purpose, to get the architecture they want. DORA (DevOps Research and Assessment, a long-running research programme on software delivery) describes this as the **Inverse Conway Maneuver** in its guide to loosely coupled teams. Plan the team change and the code change together (lesson 9.1).

**Not every quarter.** Each reorganisation costs trust. Review the team map twice a year; change it when the evidence (cross-team changes, overload, orphaned parts) is clear.

**The memorable rule.** Draw boundaries around the flow of change, not around the technology.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Team map** | One diagram: every team, its main role, what it owns, and how each pair connects | Past three or four teams; twice a year |
| **Ownership list** | Every service, app, data store and dashboard with one owning team | Before an incident finds an orphan |
| **Team page** | One public page: purpose, ownership list, ask us or do it yourself, our promises, last load check | Every team |
| **Team load check** | Four questions on understanding, run time, waiting and onboarding | Every quarter, or when a team says it is drowning |
| **Change trace** | Count the teams each of five recent user-facing changes touched | To test whether boundaries follow the flow of change |

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
> | Fix wrong ETA (estimated time of arrival) on tracking screen | Apps, Core API | 2 weeks |
>
> **Qafila team map v2 (Scale-up, twelve teams)**
>
> | Team | Main role | Owns |
> |---|---|---|
> | Merchant Onboarding | Owns a part | Sign-up, branches, shop settings |
> | Merchant Orders | Owns a part | Order creation and statuses, merchant order screens |
> | Courier Experience | Owns a part | Courier app screens, shift handling |
> | Courier Earnings | Owns a part | Earnings, tips, payouts |
> | Live Tracking | Owns a part | Tracking screens, location updates, ETA |
> | Dispatch | Owns a part | Matching orders to couriers, using routing |
> | Routing | Owns a part; rare expertise | The routing service and its algorithm |
> | Payments | Owns a part | Merchant billing, payment-provider integration |
> | Support Tools | Owns a part | Help-desk integration, the logged support view |
> | Data & Analytics | Owns a part (internal users) | Analytics pipeline, reports, data definitions |
> | Platform | Self-service | Pipeline, environments, monitoring defaults, secrets store |
> | Practices | Coaching | Reliability and security coaching (Salma and Dana's experts) |
>
> **Connections this half-year:** Dispatch and Routing work jointly until the routing interface is stable (end date set); product teams use Platform's self-service offers; Practices coaches Live Tracking on its 99.9% tracking target until the end of the half-year, then Payments.

Faisal's first draft kept Apps as one team "because mobile skills are rare". Aisha ran the trace on it: four of the five changes still crossed Apps. They spread the mobile developers across product teams, with a weekly guild meeting (a cross-team group for one skill). Yasmin moved to Merchant Orders, which owns "ready for pickup" end to end.

## 🛠️ Exercises
**🟢 Run a change trace.** Use the Qafila change trace above, or five merged pull requests in an open-source project. For each change, list the teams (or folders and maintainers) it touched and say whether it stayed inside one boundary.
*Done when:* you have five rows with a count each, and one sentence naming the boundary most changes cross.

<details><summary>Model answer and self-check</summary>

**Model answer (Qafila).** Teams touched: 4, 3, 3, 2, 2; none stayed inside one team. Most crossed Apps and Core API: cut by user journey, not layer.

**Self-check.**
- Did you name one boundary, not "communication in general"?
- Did you notice that calendar time grows with the number of teams, even when the work itself is small?

</details>

**🟡 Update a team map for new work.** Start from Qafila's v2 map above. A year later, Qafila adds two things at once: a merchant loyalty feature (shops give repeat customers points) and a second city. Update the map: decide which team owns loyalty (an existing team or a new one, with a reason from the load check), what the second city changes, and how each new pair of teams connects.
*Done when:* loyalty has exactly one owning team and a role; the second city has not created a team that copies every journey; every new connection is either a self-service interface or joint work with an end date; and no part is "shared by everyone".

<details><summary>Model answer and self-check</summary>

**Model answer.** Loyalty starts small, so Merchant Orders owns it (points are earned on orders); its next load check decides whether loyalty becomes its own team. Merchant Orders and Payments work jointly on a "discount at charge time" field until the end of the quarter; after that, Payments offers it as a documented interface. The second city gets no new team: a team per city would copy every journey. Dispatch adds the city's delivery zones to what it owns, and Platform adds a self-service way to set up a city's environments.

**Self-check.**
- Did you place loyalty using the load check, not just "whoever has time"?
- Does your joint-work pair have a date when it becomes a self-service interface?
- Did you resist cutting by geography when the journeys are the same?

</details>

**🔴 Write a team page and run a load check.** Pick one team from your map (or your own team, study group or open-source project). Write its team page with all five parts, answering the four load-check questions honestly for the last part, and propose one change if the load is too high.
*Done when:* the page fits on one screen, lists every owned item with a link or name, says what others can do themselves and where to ask for the rest, states at least one promise, and the load check ends with either "load is fine because…" or one concrete change (narrow scope, move to self-service, or split).

<details><summary>Model answer and self-check</summary>

**Model answer (Merchant Orders).** Purpose: merchants create and follow orders without calling us. Ownership list: order service, statuses, merchant order screens, order dashboard. Ask us, or do it yourself: read order data through the order API on the developer portal; other requests in our team channel. Our promises: order alerts answered within 15 minutes; 30 days' notice before any breaking API change (illustrative). Last load check: the team spends about a day a week on an old order export nobody uses; change: retire it after checking with Data & Analytics.

**Self-check.**
- Did your load check produce an action, not just a feeling?
- Did you avoid the reflex "add more people"?

</details>

## ⚠️ Mistakes and traps
- **Splitting by technical layer.** It makes every feature a relay race. Cut by the flow of change: a user journey or part of the product, owned end to end.
- **"Everyone owns it."** Name one team per part, even for shared services.
- **Coaches who never leave.** Coaching should end with the other team able to do the work. Set an end date.
- **Fixing overload by adding people.** Large teams split informally and slow down. Narrow scope or move work to self-service instead.

## 🧾 Recap
- Most teams should own a part of the product end to end; supporting roles (self-service, coaching, rare expertise) exist to make them faster.
- Every part needs one owning team; every team needs a team page and a load it can carry.
- Teams connect through documented self-service interfaces by default; joint work gets an end date.
- Rule: draw boundaries around the flow of change, not around the technology.

## ✍️ Check yourself
**1. A change to add "ready for pickup" touched the Apps, Core API, Data Infra and Analytics teams and took seven weeks. What is the most likely root cause?**

- A. The engineers on those four teams lacked the experience to work quickly.
- B. The teams were split by technical layer, so user-facing changes crossed all of them.
- C. The change was badly specified, so each team built its part to a different meaning.
- D. The company had no project manager to chase each team about the change weekly.

<details><summary>Answer</summary>

**B.** A layer split makes every user-facing feature need every layer team; the waiting took seven weeks. C and D do not explain why every recent change crossed teams, and A blames people for structure. See "Two ways to cut".

</details>

**2. Qafila is adding courier ratings: merchants rate each delivery, and couriers see their average. Which option gives the feature an owner in the way this lesson recommends?**

- A. A project group drawn from three teams for one quarter, disbanded once ratings ship.
- B. Mobile developers build the rating screens; a back-end group builds the rating service.
- C. A review board approves the ratings design; any team with spare time then builds it.
- D. Courier Experience owns ratings end to end: screens, service, data, alerts and problems.

<details><summary>Answer</summary>

**D.** A long-lived team that owns the part end to end keeps most future rating changes inside one team. A leaves nobody owning the result, B is a split by layer, and C adds a gate without naming an owner. See "Product teams" and "Ownership".

</details>

**3. Qafila's product teams queue for days for the platform team to create environments for them. What should change?**

- A. The platform team makes environment creation self-service for product teams.
- B. Each product team hires its own platform engineer to stop waiting for others.
- C. The platform team adds staff and promises to handle each request within a day.
- D. Product teams plan environment requests a month ahead so they can be scheduled.

<details><summary>Answer</summary>

**A.** A queue means the self-service team is acting as a ticket desk. C shortens the queue but keeps it, D hides the wait in planning, and B repeats the work in every product team. See "Supporting roles".

</details>

**4. Six months after the team map was redrawn, Salma's reliability experts are still doing Live Tracking's on-call because "they know it best". What is the problem?**

- A. Reliability experts should never work with product teams; it confuses ownership.
- B. Live Tracking should be relabelled a rare-expertise team, as reliability is scarce.
- C. Coaches should help a team for a set time, then step back, not do its work for good.
- D. On-call is a shared tool, so the platform team should take over Live Tracking's rota.

<details><summary>Answer</summary>

**C.** Coaches help others learn, then leave; otherwise Live Tracking never owns its reliability. A goes too far, B mislabels an ordinary product part, and D moves the problem elsewhere. See "Supporting roles" and "Mistakes and traps".

</details>

**5. The Dispatch team says it is overloaded: it owns nine services, spends most of its time keeping them running, and new members take months to become useful. What is the best first response?**

- A. Narrow what the team owns: move routine work to self-service, or split along a seam.
- B. Add four more engineers so there are enough people to look after all nine services.
- C. Ask the team to work longer hours for one quarter while the running work is cleared.
- D. Merge Dispatch with Routing, so one larger team shares the load and the knowledge.

<details><summary>Answer</summary>

**A.** The load check shows the team owns more than it can understand; reducing what it owns addresses the cause. B makes a large team that splits informally, C is not sustainable and fixes nothing, and D makes the load problem bigger. See "Team load check".

</details>

## 📚 References
- Conway, M. E., "How Do Committees Invent?", *Datamation* 14(4), April 1968; reprint (not opened from this environment; as reported): https://www.melconway.com/Home/Committees_Paper.html
- DORA, "Capabilities: Loosely coupled teams" (source file read on GitHub, 2026-11-22): https://dora.dev/capabilities/loosely-coupled-teams/
- Skelton, M. and Pais, M., *Team Topologies: Organizing Business and Technology Teams for Fast Flow* (IT Revolution, 2019); site https://teamtopologies.com.
- Library course: [*Running IT as a Business*, lesson 2.2 — Designing a product-aligned operating model: product, platform and enabling teams](../itbiz/index.html#/2.2) (the manager's view).
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 0.1 — What cloud, DevOps, platform engineering and SRE are](../cloud/index.html#/0.1) (the engineering vocabulary).

---

# 8.2 — Dependencies, planning and coordination across teams
*Level: 🟡 Intermediate* · *Prerequisites: 6.1, 8.1* · *Step: Collaborate*

**After this you can** list the dependencies of work that crosses teams, sort them by kind, decide for each whether to remove it, make it self-service, put it behind a contract or coordinate it, and keep a dependency register and a light cross-team plan that show who needs what from whom, by when. *Study time: reading about 15 min, hands-on about 95 min (estimate).*

## ⚡ In 60 seconds
- A **dependency** is anything a team needs from outside itself before its work can be finished or used. Each one is a place where work waits.
- Work through them in order: **remove**, make **self-service**, put behind a **contract** (a documented, versioned interface), and only then **coordinate** with dates and owners.
- The rule that matters most: **a dependency you cannot remove gets an owner, a date and a contract.**
- Decision cue: if work needs four or more teams to deliver at once, slice it until each slice lands in one or two.
- Biggest trap: changing an interface other teams use without warning, and calling the breakage "their problem".

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

In the month after the new team map (lesson 8.1), two things happened. First, the Courier Earnings team tidied its earnings API, renaming one field from `total` to `total_amount`. By evening, Support Tools' support view showed every courier's earnings as zero and Data & Analytics' payout report was blank. Salma's desk took more than two hundred courier contacts. Nobody had known that two other teams read that field.

Second, Aisha and Maha announced the quarter's biggest bet: **scheduled deliveries**, letting merchants book a delivery for later. Every team nodded in the planning meeting. Six weeks later, Yasmin on Merchant Orders had built the booking screen, but nothing could be released: Dispatch was waiting for Routing to support future time slots, Routing had put that in "next quarter" because nobody had asked it directly, and Payments had not been told about the different charge time. "Who was supposed to know all this?" Yasmin asked. Nobody in particular.

## 📐 How it works

### 🟢 The essentials

**Kinds of dependency.** Each kind has its own remedy:

| Kind | What the team waits for | Qafila example | Usual remedy |
|---|---|---|---|
| **Code** | Another team to change its code | Routing must accept future time slots | Clear interface; move the boundary |
| **Interface (API)** | An API to exist or stay the same | Support Tools reads the earnings API | Versioned contract, change notice |
| **Data** | Data owned elsewhere | Analytics needs the "scheduled" status | Data definitions with owners (lesson 9.2) |
| **Expertise** | A person with rare knowledge | Two people understand the routing algorithm | Document, pair, coaching |
| **Approval** | Someone outside to say yes | Security review for card data changes | Pre-agreed automated checks |
| **Shared resource** | A shared environment or tool | One staging environment for all | Self-service (lesson 8.3) |
| **Timing** | Another team to release first | Payments must change charge time first | Plan the order; a feature flag removes the wait to release |

**Reduce before you manage.** Work down this ladder and stop at the first step that works:

1. **Remove it.** Slice the work so this team does not need the other, or move the boundary (lesson 8.1).
2. **Make it self-service.** Let the needing team do it itself (one environment per team; an automatic check instead of a manual approval).
3. **Put it behind a contract.** Document the interface, version it, and promise how changes will be announced.
4. **Coordinate it.** For what is left, agree an owner on each side, a date and a definition of done, written where both teams see it.

**The dependency register.** A **dependency register** is a shared list of the dependencies that remain after the ladder. Each row names the needing and providing teams with an owner on each side, what exactly is needed, by when, its kind, its status (agreed, in progress, done, at risk) and **if late**: the fallback. That last column matters most, because it forces a fallback plan before one is needed. The worked example below shows one.

### 🟡 Going deeper

**Interfaces as contracts.** An interface other teams call is a **contract**: a promise about what you can send, what you get back and what it means. The earnings outage happened because the contract was implicit:

- **Document it** where callers can find it (lesson 8.3), including who calls it.
- **Prefer backward-compatible changes**, which do not break existing callers: adding an optional field is usually safe; renaming or removing one is not. To rename, add the new field, tell callers, wait until they have moved, then remove the old one ("expand, then contract", lesson 3.3).
- **Label breaking changes.** Semantic Versioning (SemVer), a free specification, increases the MAJOR version for incompatible API changes, MINOR for backward-compatible new functionality and PATCH for backward-compatible bug fixes.
- **Announce and wait.** A breaking change needs a written notice to every caller and time for them to plan.
- **Test the contract.** A **contract test** checks automatically that a provider still behaves as its callers expect. See [*Software Testing*, lesson 2.2 — Integration testing: databases, queues, test data and contract tests](../testing/index.html#/2.2).

**Who reviews what.** While much of Qafila's code sits in one repository, a **code-owners file** maps folders to owning teams; on GitHub, for example, code owners are automatically requested for review when a pull request modifies code they own.

**Planning across teams, lightly.** Twelve teams need some shared planning, not a planning machine. A light quarterly rhythm:

1. **Shared outcomes first:** a few company outcomes for the quarter (lesson 6.1).
2. **Each team drafts its plan,** including what it needs from others.
3. **A joint planning session** where teams post **needs** and **offers** side by side. Every need must meet an offer from a named team; unmatched needs are the session's most valuable output.
4. **Reserve capacity** for other teams' requests and surprises, and write the figure down.
5. **A short weekly cross-team check** on the register only: what is at risk, late or needs a decision.
6. **One owner per cross-team initiative** (usually a product manager) keeps the whole picture.

**Slicing across teams.** Slice big bets so each slice is useful on its own and lands in as few teams as possible: scheduled deliveries could start as "later today, one city", with no Routing change.

**Decouple the releases.** A **feature flag** (a switch that turns a feature on or off without a deployment, lesson 3.3) lets each team release its part when ready, switched off. It does not remove a timing dependency; it removes the wait to release.

### 🔴 Expert view

**Adding people rarely rescues late work.** In *The Mythical Man-Month* (1975), Fred Brooks is reported to have observed that adding people to a late software project makes it later. Adding a fifth team to a late initiative likewise adds coordination faster than progress. Slice instead.

**Persistent dependencies are a design signal.** Two teams in the register quarter after quarter usually means a wrong boundary or a missing self-service offer. DORA's guide to **loosely coupled teams** describes teams that can test and deploy on demand without orchestrating with other services, and says DORA research shows effective organisational and technical structures predict continuous delivery. Use the register as evidence at the team-map review (lesson 8.1).

**Watch the critical path.** The **critical path** is the longest chain of steps that must happen one after another; any delay on it delays the outcome. Put fallback plans there, and escalate early with options (wait, slice down, workaround). For the manager's view, see [*Running IT as a Business*, lesson 3.2 — Prioritising and funding work: business cases, cost of delay and funding products not projects](../itbiz/index.html#/3.2).

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
Aisha owned scheduled deliveries as a cross-team initiative and built the register with Yasmin. Illustrative and fictional.

> **Scheduled deliveries — dependency register (week 7 re-plan; excerpt: five of the twelve remaining rows)**
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

The first draft had 23 rows; the ladder removed eleven. Faisal wanted Routing in "because the full feature needs it"; Aisha moved it to slice 2. Instead of a review meeting for Dana, Payments added a pipeline check she had agreed in advance. Slice 1 went live in week 11 in one city.

## 🛠️ Exercises
**🟢 Sort the dependencies.** Six fictional Qafila needs: (1) Dispatch needs Live Tracking to expose courier location to its matching service; (2) Support Tools reads the order status API; (3) Payments needs Dana's sign-off on any change to card handling; (4) every team shares one staging environment; (5) only one Routing engineer understands the ETA (estimated time of arrival) model; (6) Merchant Onboarding must release its new branch screen before Merchant Orders can show branch names on orders. Give each a kind and a first rung on the ladder.
*Done when:* all six have a kind and a ladder step, and at least two are "remove" or "self-service" rather than "coordinate".

<details><summary>Model answer and self-check</summary>

**Model answer.** (1) Interface; contract: Live Tracking publishes a documented, versioned location API that Dispatch calls, with a contract test. (2) Interface; contract with a contract test. (3) Approval; self-service through pre-agreed automated checks. (4) Shared resource; self-service, one environment per team. (5) Expertise; coordinate now, plus pairing and documentation. (6) Timing; coordinate the order, and use a feature flag so neither team waits to release.

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

**🔴 Re-plan a cross-team initiative.** Take scheduled deliveries (or any feature that needs four or more teams, such as "merchant loyalty points"). Build a dependency register, apply the ladder to every row, slice the work so the first slice needs as few teams as possible, mark the critical path, and write the "if late" column. Then list each remaining row as a need and the matching offer from a named team; mark any unmatched need and the decision for it.
*Done when:* the first slice is useful to real users on its own and needs no more than two or three teams; every remaining row has owners on both sides and a date; every need has a named offer or a written decision; and the critical path is named.

<details><summary>Model answer and self-check</summary>

**Model answer (merchant loyalty points).** The full version needs four teams. Slice 1: merchants see a count of repeat customers on their dashboard (Data & Analytics query, Merchant Orders screen): two teams. Slice 2: points per order (Merchant Orders; Payments contract for a discount at charge time). Slice 3: support view (Support Tools). Needs and offers: Merchant Orders needs a discount at charge time; Payments offers it for week 6. Merchant Orders needs repeat-customer counts; Data & Analytics offers a query, week 2. Support Tools needs a points view: no offer this quarter; decision: support reads the merchant dashboard until slice 3. Critical path for slice 2: Payments discount field → end-to-end test → flag on. If Payments is late: launch earning without redeeming.

**Self-check.**
- Did slicing remove dependencies, or just postpone them all to slice 2?
- Is your first slice something merchants would notice and use?

</details>

## ⚠️ Mistakes and traps
- **Managing dependencies instead of removing them.** Apply the ladder first; coordinate only what is left.
- **Silent interface changes.** Renaming or removing a field breaks callers you do not know about. Expand, announce, wait, then contract, with contract tests.
- **Nodding in planning.** Agreement in a meeting is not a commitment. Every need must match a named offer with a date, in writing.
- **All-or-nothing launches.** Slice the feature, and use feature flags to decouple releases.
- **Treating repeat dependencies as normal.** Take the same pair of teams, quarter after quarter, to the team-map review.

## 🧾 Recap
- A dependency is anything a team waits for from outside itself; each kind has its own remedy.
- Work down the ladder: remove, make self-service, put behind a contract, then coordinate.
- Interfaces other teams use are contracts: document them, change them compatibly, announce breaking changes and test them automatically.
- Plan across teams lightly: shared outcomes, needs matched to offers, reserved capacity, a short weekly check and one owner per initiative.
- Rule: a dependency you cannot remove gets an owner, a date and a contract.

## ✍️ Check yourself
**1. Courier Earnings renamed a field in its earnings API, and two other teams' features broke the same evening. What would most directly have prevented this?**

- A. A rule that the Head of Engineering approves every API change before it is merged.
- B. A monthly meeting where all teams present the changes they plan to their services.
- C. An expand-then-contract change: new field first, a notice, and callers' contract tests.
- D. A merger of Support Tools and Data & Analytics into Courier Earnings, with one backlog.

<details><summary>Answer</summary>

**C.** Expand-then-contract keeps callers working, and contract tests catch a break before merging. A and B add slow manual steps that rely on someone noticing; D merges teams to fix a missing contract. See "Interfaces as contracts".

</details>

**2. Dispatch cannot start scheduled deliveries until Routing supports future time slots, and Routing has scheduled that for next quarter. What should the team try first?**

- A. Slice it so the first version needs no Routing change, with Dispatch holding bookings.
- B. Escalate to Maha and ask her to order Routing to move the work into this quarter.
- C. Lend Routing two engineers from Merchant Orders so that it can finish sooner.
- D. Mark the dependency "at risk" and wait for Routing's next planning session.

<details><summary>Answer</summary>

**A.** The ladder starts with removing the dependency; slicing lets the first slice ship without Routing. B and D coordinate before trying to remove it, and C adds people to a rare-expertise team, which usually slows it first. See "Reduce before you manage" and "Slicing across teams".

</details>

**3. In Qafila's joint planning session, Merchant Orders lists "Payments: charge at pickup time" as a need, but Payments has no matching offer. What does this mean?**

- A. The plan is fine: Payments heard the need in the room and can add it later.
- B. Merchant Orders should make the change itself in the Payments code.
- C. The session failed and should be repeated next week with every team present.
- D. A gap to resolve now: agree an owner and date, change the slice, or plan a fallback.

<details><summary>Answer</summary>

**D.** Finding unmatched needs is what joint planning is for; each needs a decision now. A repeats the "everyone nodded" failure, B breaks ownership, and C treats a useful finding as failure. See "Planning across teams, lightly".

</details>

**4. Which change to an API that other teams call is backward compatible?**

- A. Renaming the field `total` to `total_amount` so names match the other APIs.
- B. Adding a new optional field `charge_at` that existing callers can ignore.
- C. Changing the `amount` field from whole currency units to hundredths, keeping its name.
- D. Removing the `legacy_id` field, since the provider believes no caller still reads it.

<details><summary>Answer</summary>

**B.** Callers keep working when an optional field is added. A and D break callers of the old field; C is worst: same name, new meaning, so callers silently compute wrong values. See "Interfaces as contracts".

</details>

**5. Data & Analytics and Merchant Orders appear together in the dependency register for the third quarter running. What is the best interpretation?**

- A. The teams work well together and should keep coordinating the same way.
- B. Data & Analytics is too slow and should reserve more capacity for Merchant Orders.
- C. The register is too detailed and should track only dependencies already at risk.
- D. The boundary or interface between them needs changing; raise it at the map review.

<details><summary>Answer</summary>

**D.** Persistent dependencies are a design signal: move the boundary or make the providing side self-service. A accepts a lasting cost, B blames one team for a structural issue, and C hides the evidence. See "Persistent dependencies are a design signal".

</details>

## 📚 References
- Semantic Versioning 2.0.0 specification, summary (source text on GitHub; opened 2026-11-22): https://github.com/semver/semver/blob/master/semver.md — public site https://semver.org
- GitHub Docs, "About code owners" (source file read on GitHub, 2026-11-22): https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- DORA, "Capabilities: Loosely coupled teams" (source file read on GitHub, 2026-11-22): https://dora.dev/capabilities/loosely-coupled-teams/
- Brooks, F. P., *The Mythical Man-Month: Essays on Software Engineering* (Addison-Wesley, 1975; anniversary edition 1995). Full citation; Brooks's law as reported.
- Library course: [*Software Testing*, lesson 2.2 — Integration testing: databases, queues, test data and contract tests](../testing/index.html#/2.2).
- Library course: [*System Design for Vibe Coders*, lesson 6.6 — API Design That Survives Its Clients](../vibe/index.en.html#l6-6).
- Library course: [*Running IT as a Business*, lesson 3.2 — Prioritising and funding work: business cases, cost of delay and funding products not projects](../itbiz/index.html#/3.2).

---

# 8.3 — Internal platforms and developer experience
*Level: 🟡 Intermediate* · *Prerequisites: 3.3, 4.1, 8.1* · *Step: Collaborate*

**After this you can** explain what an internal platform is and why it should be run as a product, write a golden-path checklist for one common task, describe a platform on one page, and run a short developer-experience survey whose results point to one improvement. *Study time: reading about 15 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- An **internal platform** is the shared tools, templates and documentation product teams use to build, ship and run software, offered as **self-service**, without waiting for anyone.
- A **golden path** (or paved road) is the supported, recommended way to do a common task, with good defaults (tests, pipeline, monitoring, secrets: keys and passwords) built in.
- **Developer experience** is how engineers experience getting work done: feedback, mental load, focus.
- The rule that matters most: **run the platform as a product, and make the right way the easy way.**
- Decision cue: if several teams build the same thing by hand, it is a platform candidate; if no team asked for it, not yet.
- Biggest trap: building a large platform nobody asked for, then forcing teams to use it.

## 🧭 Why it matters
Qafila and everyone in it are fictional. All numbers about Qafila in this lesson are illustrative figures, not benchmarks.

Yasmin was asked to set up a small new service to send "ready for pickup" alerts to couriers. There was no standard way to start one. She copied the most recent service, spent days removing what did not apply, asked in four channels why the pipeline failed, and waited two days for a database. It reached production after eleven working days; the code that did the work had taken two.

She had also copied a cloud access key sitting in a configuration file. A few months earlier, an engineer had pushed a similar service to a public repository, key included; the key was misused for a few hours before it was revoked. That scare is why Qafila hired Dana as security and risk lead. She found that every team copied set-up from the nearest service, inheriting its mistakes.

The new Platform team from the team map (lesson 8.1), four engineers who had been doing this work informally, had no offer yet. Dana's first request to it was not a new rule: "Make the safe way the quickest way to start a service."

## 📐 How it works

### 🟢 The essentials

**What an internal platform is.** An **internal platform** is what a company provides once, centrally, so each product team does not build it again. At a company like Qafila it typically includes:

| Platform part | What it gives a product team | Without it |
|---|---|---|
| **Service template** | A new service with tests, pipeline and monitoring already set up | Copy an old service and its mistakes |
| **Delivery pipeline** | Build, test, checks and deploy on every merge (lesson 3.3) | Each team keeps its own scripts |
| **Environments** | A test environment per team, created on demand | Queue for one shared staging environment |
| **Secrets management** | A safe store for keys and passwords, read by services at run time | Keys in configuration files and chat messages |
| **Observability defaults** | Logs, metrics, dashboards and standard alerts (lesson 4.2) | Each team guesses what to measure |
| **Developer portal** | One place to find every service, its owner, docs and API | Ask around in chat |

**Golden paths.** A **golden path** is the supported, recommended route for a common task: one way with the choices already made. Spotify's engineering blog is reported to have described its Golden Paths in 2020 as a response to fragmentation in its tools and practices. Two features matter: it is **the easy way**, faster than going alone because the defaults are done; and it is **supported, not forced**: teams may leave it with a reason, but then own what the path would have handled.

**Run the platform as a product, and self-service.** Its users are other engineers: treat them like customers (Module 1), learn what slows them down, and measure adoption. A platform that answers requests ("please create a database") is a ticket desk with a new name. Start with the smallest thing that helps, even a well-kept wiki page.

### 🟡 Going deeper

**What developer experience means.** **Developer experience** (DevEx or DX) is how engineers experience building and shipping software. A 2023 *ACM Queue* article, "DevEx: What Actually Drives Productivity" by Abi Noda, Margaret-Anne Storey, Nicole Forsgren and Michaela Greiler, is reported to describe three dimensions:

| Dimension | Plain meaning | Qafila example of poor DevEx | Platform fix |
|---|---|---|---|
| **Feedback loops** | How quickly you learn whether your change works | Pipeline takes 40 minutes; review waits a day | Faster pipeline; test environment per change |
| **Cognitive load** | How much you must keep in your head to do a task | Starting a service means knowing nine tools and four teams | One template, one portal page |
| **Flow state** | How often you can work with uninterrupted focus | Constant pings asking who owns what | Owners and docs findable without asking |

**Measuring without a single number.** A 2021 *ACM Queue* article by Nicole Forsgren and colleagues, "The SPACE of Developer Productivity", is reported to argue that productivity cannot be captured by one metric, and to describe five dimensions: satisfaction and well-being, performance, activity, communication and collaboration, and efficiency and flow. So combine a few kinds of measure:

- **Ask people:** a short quarterly survey, plus "What slowed you down most this month?"
- **Measure the path:** time from "new service" to production; pipeline duration; a new engineer's time to a first production change.
- **Measure adoption:** share of services from the template or using the secrets store.

Do not measure individuals by commits or lines of code: easy to game, and silent on whether work got easier.

**A platform team's product practices:** watch users work; document first (undocumented features do not exist for users); and run the platform reliably, with its own on-call (lesson 4.2), since everyone depends on it.

### 🔴 Expert view

**What the research found.** Google Cloud's announcement of the 2024 DORA report (DORA is DevOps Research and Assessment, a long-running research programme on software delivery) lists findings on platform engineering, among them: internal development platforms increased developer productivity; a platform initiative "might lead to a temporary decrease in performance before improvements manifest as the platform matures"; and for best results, platform efforts should prioritise user-centred design, developer independence and a product-oriented approach. These are survey findings, not guarantees. Expect a dip and say so in advance.

**Guardrails, not gates.** A **gate** stops work until a person approves it. A **guardrail** is an automatic check in the path that blocks only what is clearly unsafe, like Dana's: the pipeline blocks any merge containing a key. For the engineering detail, see [*Cloud & DevOps: Zero to Hero*, lesson 3.3 — Policy as code, drift and guardrails](../cloud/index.html#/3.3).

**Mandatory or optional?** Mandating everything gets adoption but loses feedback on whether the platform is good. A middle ground: a few guardrails mandatory (secrets, access, basic monitoring), each with a stated reason, the rest optional but convenient. Teams leaving the path is user research, not disobedience.

**Build, buy or assemble.** Platform parts can be built, bought or assembled from open source (Backstage, for example, is an open-source developer-portal framework; not an endorsement). Build only what is specific to you (lesson 2.3). For the manager's view, see [*Running IT as a Business*, lesson 5.1 — Delivery pipelines as a managed capability](../itbiz/index.html#/5.1).

**The memorable rule.** Run the platform as a product, and make the right way the easy way.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Platform one-pager** | Eight rows: users, problem, offer, mandatory guardrails with reasons, optional golden path, help, measures, next | When a platform team forms; each quarter |
| **Golden-path checklist** | Steps and built-in defaults for one common task | For each task several teams do by hand |
| **Service template** | Starter repository with tests, pipeline, monitoring and secrets handling | Once two teams start services the same way |
| **Developer portal** | Every service with owner, docs and API | When "who owns this?" is a daily question |
| **DevEx survey** | Five or six questions on feedback, load and focus, plus one open question | Every quarter, results shared openly |
| **Path measures** | Time to a new service in production, pipeline duration, adoption share | Monthly |

## 🏛️ In practice at Qafila
The Platform team's first quarter, with Yasmin seconded as its "first user". Illustrative and fictional.

> **Qafila Platform — one-pager (v1)**
>
> | Item | Content |
> |---|---|
> | Users | Engineers in the eleven other teams |
> | Problem | Starting a service takes about eleven working days, copies old mistakes, and needs four teams |
> | Offer v1 | Service template; secrets store; standard dashboards and alerts; one test environment per team, self-service |
> | Mandatory guardrails | Secrets only from the store, and the pipeline blocks committed keys (a leaked key has already been misused once); every service listed with an owner in the portal (incidents need an owner within minutes); standard alerts on (the 99.9% tracking target depends on knowing first) |
> | Optional golden path | Everything else in the template: folder layout, test set-up, deployment steps |
> | Help | Platform channel, answered within half a working day; office hours on Wednesdays |
> | Measures | Time from "new service" to production; share of new services from the template; quarterly DevEx survey |
> | Next | Faster pipeline (currently 40 minutes); a portal page for every API (lesson 8.2) |
>
> **Golden path: start a new service (checklist)**
> 1. Run the template generator with the service name and owning team.
> 2. The template creates the repository, code-owners entry, pipeline, dashboards and alerts.
> 3. Request secrets through the store's self-service page; the service reads them at run time.
> 4. Register the service in the portal: owner, purpose, API documentation link.
> 5. Merge the first change; the pipeline deploys it to test, then production behind a feature flag.
>
> **DevEx survey, first round:** easiest: deploying an existing service. Hardest: getting a test environment, finding who owns an API. Top answer to "what slowed you down most?": waiting for review from another team.

Yasmin rebuilt her pickup-alert service with the first template, timing every step: two days instead of eleven. Faisal wanted the whole template mandatory; Dana argued for three guardrails and an optional path, and eight of the next nine services used it anyway. The top survey complaint went to the team-map review (lesson 8.1). The first month was slower while teams learned, as the platform lead had warned.

## 🛠️ Exercises
**🟢 Spot the platform candidates.** Qafila teams do these: (1) set up a pipeline for a new service; (2) design the loyalty screen; (3) create a test database; (4) tune the routing algorithm; (5) add standard alerts; (6) store the payment provider's API key; (7) write a help article; (8) find the owner of the earnings API. Mark each "platform candidate" or "product team work", with a one-line reason.
*Done when:* every item is marked with a reason, and each platform candidate is something several teams do in much the same way.

<details><summary>Model answer and self-check</summary>

**Model answer.** Platform candidates: (1), (3), (5), (6) and (8) (a portal): every team does these the same way. Product team work: (2), (4) and (7): each is specific to one product area and needs its knowledge.

**Self-check.**
- Did you avoid putting product decisions (screens, algorithms) on the platform?
- Did you notice that (6) is both a convenience and a security guardrail?

</details>

**🟡 Write a golden-path checklist.** Pick a common task in a project you know (setting up a laptop for development, publishing a package) or Qafila's "a new engineer's first production change". Write a five-to-eight-step checklist and mark the defaults the path provides.
*Done when:* read as a stranger, no step uses a name, tool or person the checklist has not introduced; each step is one action; the safe defaults (tests, secrets, monitoring or equivalent) are built in rather than left to the user, and you have timed or estimated how long it takes.

<details><summary>Model answer and self-check</summary>

**Model answer (new engineer's first change at Qafila).** 1. Run the laptop set-up script. 2. Read the portal page "Your first week". 3. Clone the team repository; run tests with one command. 4. Pick a "first change" item from the board. 5. Open a pull request; code owners review it. 6. The pipeline tests and deploys to the test environment, then production behind a flag. Defaults: tool versions, access, pipeline checks, secrets. Target: first week (illustrative).

**Self-check.**
- Must the newcomer ask anyone a question at any step? Can the path answer it instead?
- Did you build the safe choice in, rather than adding a "remember to…" step?

</details>

**🔴 Design a platform one-pager and a DevEx survey.** For Qafila's Platform team (or the shared tools of a study project), write a one-pager with the eight rows from this lesson and a quarterly survey of five or six questions covering feedback loops, cognitive load and flow, plus one open question. Name the measure that would show, in three months, whether the platform helped.
*Done when:* the one-pager names its users and one problem in numbers, separates mandatory guardrails from the optional path with a reason for each guardrail, the survey covers all three DevEx dimensions, and you have chosen one or two measures with a starting value.

<details><summary>Model answer and self-check</summary>

**Model answer (guardrails).** Secrets from the store only: a leaked key was misused before. Every service has an owner in the portal: incidents need someone to call. Standard alerts on: the tracking target depends on knowing first. **Survey (1–5 scales).** (1) How quickly do you learn whether a change works? (feedback) (2) How easy is it to get a test environment? (feedback) (3) How easy is it to find the owner and docs of a service you depend on? (load) (4) How easy was it to start your last piece of work without help? (load) (5) How often do you get two uninterrupted hours in a week? (flow) (6) What slowed you down most this month? Measures: time from "new service" to production (start: about eleven working days, illustrative); share of new services from the template (start: zero).

**Self-check.**
- Does every mandatory guardrail protect customers or the company, rather than being someone's preference?
- Are your measures about the work getting easier, not about how busy individuals are?

</details>

## ⚠️ Mistakes and traps
- **Building a platform nobody asked for.** Start from what several teams already do by hand and find painful; build the smallest thing that helps.
- **A platform that takes tickets.** Aim for self-service and measure waiting.
- **Making everything mandatory.** Mandate a few guardrails; make the rest attractive.
- **Measuring individuals.** Measure the path, adoption and what people tell you.
- **Expecting instant gains.** Warn people about an early dip, and keep listening.

## 🧾 Recap
- An internal platform offers shared tools, templates and documentation as self-service.
- Golden paths make the recommended way the easiest way; a few guardrails are mandatory, the rest is supported and optional.
- Developer experience covers feedback loops, cognitive load and flow; measure it with surveys, path timings and adoption, not one number.
- DORA's 2024 research reported productivity gains from internal platforms, a possible early dip, and best results when user-centred.
- Rule: run the platform as a product, and make the right way the easy way.

## ✍️ Check yourself
**1. Yasmin's new service took eleven working days to reach production, though the code took two. What is the best first platform response?**

- A. Require the Platform team to review every new service before it is created.
- B. Offer a service template and self-service steps that make starting a service quick.
- C. Ask each product team to keep one engineer who specialises in service set-up.
- D. Reduce new services by asking teams to add features to existing ones instead.

<details><summary>Answer</summary>

**B.** A self-service template removes the nine days of set-up and builds in safe defaults. A adds a gate, C repeats the work in every product team, and D bends the architecture. See "Golden paths" and "Run the platform as a product, and self-service".

</details>

**2. After the access-key incident, Dana wants to make sure no service has keys in its code. Which approach best fits this lesson?**

- A. A gate: Dana reviews every pull request that touches configuration files before merging.
- B. A reminder: a monthly message to all engineers about keys, with a short training video.
- C. A guardrail: the template reads secrets from the store; the pipeline blocks merges with a key.
- D. A move: all services into one repository, so the security team can watch every change.

<details><summary>Answer</summary>

**C.** A guardrail makes the unsafe action impossible without making anyone wait. A turns Dana into a bottleneck, B relies on memory, and D changes the layout without stopping the mistake. See "Guardrails, not gates".

</details>

**3. Which set of measures best tells Qafila's Platform team whether developer experience is improving?**

- A. Time from "new service" to production, template adoption, and a quarterly survey.
- B. The number of deployments each team makes per week, compared across all teams.
- C. The number of tickets the Platform team closes each month, and how fast.
- D. Pipeline duration alone, tracked weekly and shown on the Platform team's dashboard.

<details><summary>Answer</summary>

**A.** Path timings, adoption and what people say cover the experience from several sides. B is activity compared across teams and invites gaming, C rewards a ticket-desk platform, and D is one number for one part of the path. See "Measuring without a single number".

</details>

**4. In the platform's first month, delivery at Qafila got slightly slower while teams learned the template. What is the best reading?**

- A. The template has failed and should be withdrawn before more teams depend on it.
- B. Delivery should be measured only after six months, so early results confuse no one.
- C. Product teams are resisting and should be required to use the whole template.
- D. An early dip can happen while teams learn; keep listening to users and tracking it.

<details><summary>Answer</summary>

**D.** The 2024 DORA findings mention a possible temporary dip; warn people and keep improving from feedback. A overreacts, B hides evidence, and C treats a learning cost as disobedience. See "What the research found".

</details>

**5. Several teams leave the golden path to use their own deployment scripts. What should the Platform team do first?**

- A. Make the golden path mandatory and remove access to other deployment routes.
- B. Accept it, because golden paths are optional and teams may choose their own way.
- C. Find out why they left and treat their reasons as user research.
- D. Report the teams to the Head of Engineering so it is raised in their reviews.

<details><summary>Answer</summary>

**C.** Teams leaving a convenient path is a signal about the path. A loses that feedback, B ignores it, and D punishes users for a product problem. See "Mandatory or optional?".

</details>

## 📚 References
- Google Cloud blog, "Announcing the 2024 DORA report" (October 2024; sections on platform engineering and developer experience; opened 2026-11-22): https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
- Noda, A., Storey, M.-A., Forsgren, N. and Greiler, M., "DevEx: What Actually Drives Productivity", *ACM Queue*, 2023: https://queue.acm.org/detail.cfm?id=3595878 (could not be opened from this environment; as reported).
- Forsgren, N., Storey, M.-A., Maddila, C., Zimmermann, T., Houck, B. and Butler, J., "The SPACE of Developer Productivity", *ACM Queue* 19(1), 2021: https://queue.acm.org/detail.cfm?id=3454124 (could not be opened from this environment; as reported).
- Spotify Engineering, "How We Use Golden Paths to Solve Fragmentation in Our Software Ecosystem" (August 2020): https://engineering.atspotify.com/2020/8/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem (could not be opened from this environment; as reported).
- Backstage repository README (opened 2026-11-22): https://github.com/backstage/backstage
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 3.3 — Policy as code, drift and guardrails](../cloud/index.html#/3.3).
- Library course: [*Running IT as a Business*, lesson 5.1 — Delivery pipelines as a managed capability](../itbiz/index.html#/5.1).
- Library course: [*From Graduate to Hired*, lesson 6.2 — Your first 90 days: onboarding, the first pull request and asking good questions](../career/index.html#/6.2).
