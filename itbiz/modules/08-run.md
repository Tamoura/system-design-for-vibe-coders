# Module 8 — Run: operations and reliability

*Everything the earlier modules built ends up running somewhere, and sooner or later it fails. This module is about the part of the operating model that keeps Najm Bank's services working and restores them quickly when they break: what the Technology division watches and who gets woken, how a major incident is led and recorded, how the bank finds and removes the causes behind repeated failures, and how an agreed level of reliability, written as a service level objective with an error budget, becomes a tool that product, operations and finance use to decide between new features and stability work. The engineering of monitoring and on-call is taught elsewhere in the library; here you design who decides, what record proves it and how it is measured.*

> **Steps:** Run — keep services working, restore them fast when they fail, and make each failure cheaper than the last.

---

# 8.1 — Monitoring, events and incident management
*Level: 🟡 Intermediate* · *Prerequisites: 2.3, 6.3* · *Step: Run*

**After this you can** write an incident model for one service: the customer symptoms that page someone, four severity levels in business terms, major-incident roles and rhythm, the incident record, and three measures of how well the model works. *Study time: reading about 15 min, hands-on about 95 min (estimate).*

## ⚡ In 60 seconds
- **Monitoring** produces signals; most are only logged, a few become **alerts**, fewer still **incidents** that people outside IT would notice. Design that funnel on purpose.
- The rule that matters most: **page on what customers feel; record what explains it.**
- Severity is a **business** judgement written in advance. It decides who is called, how often people hear and whether the regulator is told.
- A major incident needs **one incident commander** who coordinates rather than fixes.
- Decision cue: if customers or branch staff report outages before your monitoring does, fix detection first.
- Biggest trap: judging the model by one average such as mean time to restore.

## 🧭 Why it matters
Najm Bank, its people and every figure in this lesson are fictional and illustrative, not benchmarks.

On a Thursday evening before a public holiday, card payments at Najm Bank started failing for about one customer in five. The operations centre received around 3,000 alerts a day, and the night shift acknowledged them in bulk. A branch manager whose own card was declined raised the alarm, forty minutes in.

Then Yousef's team opened a bridge (a standing conference call for the incident) for infrastructure, the card-processing supplier opened its own, and Reem's team started a chat channel. Two groups restarted the same service at once; nobody told the contact centre what to say; Omar heard from a board member. After almost four hours the ticket said "payment issue, resolved", with no timeline or count of customers affected. Nour rebuilt it by hand when the central bank asked.

None of this needed better technology. It needed an operating model.

## 📐 How it works

### 🟢 The essentials

**From signal to incident.** Define these words once, division-wide. They are common in service management, where frameworks give formal definitions (lesson 12.1); here each is defined by what it asks someone to do.

| Term | Meaning in this course | Example at Najm Bank |
|---|---|---|
| **Monitoring** | Tools checking the estate's data against what we expect | A check that payment success stays above an agreed rate |
| **Event** | Something the tools noticed and logged; kept for later, nobody acts now | A server restarted; a certificate expires in 20 days |
| **Alert** | An event routed to a person or queue to look at | Disk at 85% on a database server (ticket) |
| **Page** | An alert urgent enough to interrupt a person now | Payment success below the agreed level for five minutes |
| **Incident** | Customers or staff can see something has stopped working or got worse; the job is to get it back | One customer in five cannot pay by card |
| **Major incident** | An incident serious enough to run with the special procedure below | A national payment outage on a holiday weekend |

A **service request** (a laptop, an access right) is not an incident (lesson 7.1).

**The funnel.** Many signals, fewer events kept, few alerts, very few pages. At Najm Bank almost everything reached a screen and nothing was trusted. Decide, for each kind of signal, which layer it stops at.

**Symptoms before causes.** Monitoring can watch **symptoms** (payments failing, pages slow) or **causes** (memory, disk, a busy database). Google's site reliability engineering (SRE) book is widely reported to recommend four "golden signals" for a user-facing system (**latency, traffic, errors and saturation**) and to favour alerting on symptoms. A cause alert fires whether or not anyone is hurt, which is why cause alerts make the most noise.

**The memorable rule: page on what customers feel; record what explains it.** Keep cause signals as events and dashboards, so responders can find the explanation once a symptom page fires.

**Severity in business terms.** Agree severity levels with the business before the next incident, in words a branch manager would understand.

| Severity | Business criteria (any one is enough) | Who is called | Update rhythm |
|---|---|---|---|
| **Sev 1** | Critical journey (payments, logins, transfers) down or badly degraded for many; data lost or exposed; likely regulatory notification | Commander, product and platform on-call, communications lead, duty executive | Every 30 minutes |
| **Sev 2** | Critical journey degraded for some, or a minor journey down for many; workaround exists | Product on-call and commander | Hourly |
| **Sev 3** | One branch or team affected, workaround in place | Owning team, working hours | At resolution |
| **Sev 4** | A non-critical journey, or a single customer or user, affected, with a workaround | Owning team's queue | At resolution |

Illustrative levels. A risk with no impact yet (a failed backup) is not an incident: raise a ticket, or a problem record (lesson 8.2). Two details matter most: **anyone may declare a higher severity** (downgrading is cheaper than discovering an hour late that an incident was major), and each change of severity is recorded with a time and a name.

**Who owns what.** In a product-aligned division (lesson 2.2): product teams watch their own components; Yousef's operations centre watches shared systems; the service desk links calls to open incidents; a trained rota (a rostered schedule) of incident commanders runs major incidents; Lina's contracts bind suppliers to the process (lesson 10.2); Nour, with the risk function, decides on regulatory notification.

### 🟡 Going deeper

**The roles in a major incident.** Google's SRE book is reported to base its incident roles on the Incident Command System used by emergency services. Four roles cover most bank incidents:

| Role | Does | Does not |
|---|---|---|
| **Incident commander** | Holds the incident, sets priorities, assigns people, decides on rollback (undoing a change) or failover (switching to a standby), holds any role not handed out | Debug; once the commander is fixing, nobody is commanding |
| **Operations lead** | Directs the people changing systems; keeps changes to one plan | Talk to executives |
| **Communications lead** | Sends updates on the agreed rhythm; drafts customer and regulator messages for approval | Promise times the operations lead has not given |
| **Scribe** | Keeps the timeline: what was seen, decided and done, by whom, when | Interpret; that comes in the review (lesson 8.2) |

Incident roles follow skill, not hierarchy: Omar, if he joins, receives updates; he is not the commander.

**One bridge, one channel, one record.** Decide in advance where a major incident lives. Suppliers join the bank's bridge rather than running their own; that obligation, with a joining time and a duty to share their timeline, is a contract point for Lina.

**The communication rhythm.** Silence makes everyone call the commander. A short update on a fixed rhythm (affected, known, doing, next update time) frees the team to work. Customer and regulator messages need an approver named in advance. Rules on reporting technology incidents to supervisors differ by country, so ask the risk function: which incidents must be reported, to whom, how fast, and who signs.

**The incident record.** It is what lets lessons 8.2 and 9.3 work. Keep mandatory fields few and fill most automatically: affected catalogue entry (lesson 2.3); severity with its history; times of impact start, detection, declaration, mitigation and resolution; how it was detected (monitoring, staff, customer, supplier); customers or transactions affected, with the estimation method; recent changes, pulled from lesson 6.3's records; the linked problem record (lesson 8.2); and the review due date.

**Alert hygiene as a management habit.** Tired people miss real incidents and leave. Review paging monthly per team: pages per shift, share that needed a human, rules to delete. The engineering detail is in [*Cloud & DevOps: Zero to Hero*, lesson 5.2 — SLOs, error budgets, alerting and on-call that people can sustain](../cloud/index.html#/5.2).

### 🔴 Expert view

**Measuring the model, not just the incidents.** Treat mean time to restore (MTTR) with care: one long outage moves the average more than any improvement. Štěpán Davidovič's report *Incident Metrics in SRE*, published by Google, is reported to use simulations to show that mean-time metrics are poorly suited to spotting trends or judging whether a change helped. Use instead:

| Measure | Why it helps | Pair it with |
|---|---|---|
| **Share of Sev 1–2 detected by monitoring** | Tests whether you watch the right symptoms | Pages per shift |
| **Time to declare and to mitigate, as a distribution** (median, slowest tenth) | Shows the process, not one event's luck | Customer impact |
| **Customer impact in SLO terms** (failed payments) | Measures harm, not clock time | Lesson 8.3's error budget |
| **Share of major incidents with complete record and timely review** | Tests whether learning can happen | Repeat incidents (lesson 8.2) |

A 2019 Google Cloud blog post puts it plainly: during an incident, SLOs "tell you when something is bad, and, more importantly, exactly how bad it is" (lesson 8.3).

**Detection is mostly a design decision.** If customers detect many of your Sev 1 incidents, the cure is usually two or three owned journey symptoms per product, not another tool. For synthetic checks, see [*Software Testing: Zero to Hero in the AI Era*, lesson 5.2 — Testing in CI/CD and in production: fast pipelines, flaky-test policy, feature flags, canaries and synthetic monitoring](../testing/index.html#/5.2).

**Changes and incidents meet here.** "What changed recently on these components?" should be answerable in a minute from lesson 6.3's records, and during a Sev 1 the commander can stop further releases. Security incidents add containment and evidence; see [*Secure AI & Application Security: Zero to Hero*, lesson 10.2 — Incident response: prepare, detect, contain, recover, learn](../secai/index.html#/10.2). AI assistants may draft updates, but not declare severity or approve messages (lesson 11.3).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Signal funnel sheet** | Each kind of signal marked event, ticket or page, with owner | When the operations centre is drowning |
| **Severity matrix** | Four business-terms levels, who is called, rhythm, notification check | Before the next incident; after each Sev 1 |
| **Incident role cards** | One page per role: does, does not, first actions | Commander rota and drills |
| **Incident record template** | The fields above, mostly filled automatically | Configured in the service management platform (a category, not a product) |
| **Paging review** | Monthly pages per shift, actionable share, rules to delete | Team and operations reviews |
| **Incident drill** | A simulated Sev 1 with a real bridge and roles | Twice a year per critical product |

## 🏛️ In practice at Najm Bank
After the holiday outage, Yousef and Reem wrote an incident model for Cards & Payments. Fictional and illustrative:

> **Incident model: Cards & Payments (v1).**
> **Symptoms paged:** authorisation success below the agreed level for 5 minutes; median authorisation time above 2 seconds for 10 minutes; app login failures above the agreed level for 5 minutes. All page Reem's on-call; the first two also page the commander rota.
> **Demoted:** 41 cause alerts (CPU, memory, disk, queue depth) moved to dashboards and tickets.
> **Roles:** commander from a rota of eight trained managers; operations lead is the on-call engineer; communications lead from the service desk; supplier joins the bank bridge within 15 minutes (Lina to add at contract renewal).
> **Record:** auto-filled with recent changes from the deployment log; review due in 5 working days for Sev 1, 10 for Sev 2.
> **Measures:** share of Sev 1–2 detected by monitoring; time to declare and mitigate (median, slowest tenth); failed authorisations per incident.

Yousef objected: "If the disk fills, payments stop." Reem replied that a disk trending towards full should be a ticket days earlier, not a 3 a.m. page. They agreed a one-quarter trial. In the first drill Omar started questioning engineers; the commander moved him to the executive update, and he wrote that into the role cards himself.

## 🛠️ Exercises
**🟢 Sort the signals.** For one service you know (or Najm Bank's Cards & Payments), list ten monitored signals and mark each as event only, ticket, or page. For each page, name the customer symptom.
*Done when:* ten signals are classified, and every page names a customer-visible symptom (any that cannot is moved to event or ticket).

<details><summary>Model answer and self-check</summary>

**Model answer.** Page: authorisation success, authorisation time, login failures. Ticket: disk trending full, certificate expiring in 20 days, failed nightly batch with a morning deadline. Event only: server restarts, autoscaling, a successful deployment, a supplier heartbeat that recovered. **Self-check.**
- Does each page describe something a customer or staff member would notice?
- Did you keep cause signals as events rather than deleting them?
- Is there a ticket path for slow-building risks?

</details>

**🟡 Write the severity matrix.** Write four severity levels in business terms, with criteria, who is called, update rhythm and a regulatory notification check. Test it against three past incidents.
*Done when:* the matrix has four levels, each criterion could be judged by a non-engineer, and each of three past incidents maps to exactly one level (or you have noted why the matrix needs changing).

<details><summary>Model answer and self-check</summary>

**Model answer.** Start from the lesson's table, name your journeys, and add "ask risk (Nour) within 30 minutes" for Sev 1. The holiday outage is Sev 1; one customer unable to download a statement, with a branch copy as workaround, is Sev 4; a failed backup with no impact yet is not an incident but a ticket with a due date. **Self-check.**
- Are criteria about customers, money and regulation rather than servers?
- May anyone raise severity, with changes recorded?
- Is the regulatory step "ask the named person", not a legal conclusion?

</details>

**🔴 Design and drill the major incident model.** Write role cards for commander, operations lead, communications lead and scribe; name the bridge, channel and record; list the incident record's mandatory fields, marking which are filled automatically; choose three measures from "Measuring the model"; then run a 45-minute tabletop drill of a Sev 1 with real colleagues.
*Done when:* four role cards exist; the record's fields are listed with the automatic ones marked; three measures are chosen, each with what it is paired with; a drill has been held with a written timeline; and at least three improvements from the drill have owners and dates.

<details><summary>Model answer and self-check</summary>

**Model answer.** Record fields: catalogue entry, recent changes and the five timestamps filled by the tools; severity history logged on each change; detection source, customers affected (with method), problem link and review date filled by people. Measures: share of Sev 1–2 detected by monitoring (with pages per shift), time to declare and mitigate as median and slowest tenth (with customer impact), and failed authorisations per incident (with the error budget). Drill trigger: "authorisation success falls to 80% at 19:40 on a holiday eve", with a complication every ten minutes (the supplier opens its own bridge, an executive joins). Typical findings: no named message approver, stale supplier contacts, a commander who started debugging. **Self-check.**
- Did the commander coordinate rather than fix?
- Are most record fields automatic?
- Do the improvements have owners, dates and backlog items?

</details>

## ⚠️ Mistakes and traps
- **Paging on causes.** Thousands of alerts teach people to ignore them all. Page on journey symptoms.
- **No one in charge.** Several bridges and senior people produce conflicting actions. Name one incident commander who coordinates.
- **Severity defined by IT alone.** Engineers rate by technical drama, the business by customers and money. Write severity together.
- **A record written from memory.** "Resolved" teaches nothing and cannot answer the regulator. Keep a timeline as you go; fill fields automatically.

## 🧾 Recap
- Design the funnel from signal to incident; very few signals should wake a person.
- **Page on what customers feel; record what explains it.**
- Write four severity levels in business terms, with a notification check owned by risk.
- Run major incidents with named roles, one bridge, one channel and one record; suppliers join the bank's process.
- Measure the model with detection source, time distributions and customer impact, not one average.

## ✍️ Check yourself
**1. Najm Bank's operations centre receives about 3,000 alerts a day, and the night shift acknowledges them in bulk. What should Yousef change first?**

- A. Hire more night-shift operators so that every alert can be read and handled.
- B. Buy a second monitoring tool that groups the alerts into fewer events.
- C. Page only on journey symptoms, and turn cause alerts into events or tickets.
- D. Raise every alert threshold by a fixed amount so fewer fire each night.

<details><summary>Answer</summary>

**C.** Cause alerts fire whether or not customers are hurt; paging on symptoms fixes the funnel. A adds cost, B keeps the same design, and D cuts noise blindly. See "Symptoms before causes".

</details>

**2. During a Sev 1 payment outage, the incident commander starts reading logs and testing fixes herself. Why is this a problem?**

- A. While she debugs, nobody is coordinating people, decisions and updates.
- B. Commanders do not normally have the skills to read production logs.
- C. Only the supplier may change payment systems during a major incident.
- D. Reading logs during an incident breaks segregation of duties controls.

<details><summary>Answer</summary>

**A.** Once the commander is fixing, the command role is empty. B is not the reason, C is not a rule in the lesson, and D confuses incident roles with change controls. See "The roles in a major incident".

</details>

**3. Omar wants one headline measure for the board pack to show that incident management is improving. Which choice best follows the lesson?**

- A. Mean time to restore across all incidents in the quarter, compared with last quarter.
- B. The total number of incidents raised in the quarter, since fewer means more stability.
- C. The number of alerts the operations centre acknowledged within five minutes.
- D. How many serious outages our own tools spotted before anyone else, with customers hurt.

<details><summary>Answer</summary>

**D.** Who detected serious incidents, read with how many customers were affected, shows whether the model works and what failures cost. A is swamped by one long outage, B falls if people stop raising incidents, and C rewards acknowledging noise. See "Measuring the model, not just the incidents".

</details>

**4. The card processor opens its own bridge during a Najm Bank outage and restarts a service without telling the bank's team. What is the best lasting fix?**

- A. Ask the operations centre to watch the supplier's systems more closely in future.
- B. Agree in the contract and role cards that the supplier joins the bank's single bridge.
- C. Replace the processor at the next renewal with a supplier that has fewer incidents.
- D. Let the supplier lead future incidents on its systems and send the bank a summary.

<details><summary>Answer</summary>

**B.** One bridge, one channel and one record keep actions coordinated, and the obligation belongs in the contract. A does not stop parallel actions, C does not fix the process, and D splits the facts again. See "One bridge, one channel, one record".

</details>

**5. Reem's team proposes severity levels based on how many servers are affected. Nour objects. What should the levels be based on instead?**

- A. The number of affected systems, weighted by each system's criticality tier.
- B. Customer, money and regulatory impact, agreed with the business in advance.
- C. The regulator's own incident categories, so the bank needs no levels of its own.
- D. The on-call engineer's judgement, since they see the technical detail first.

<details><summary>Answer</summary>

**B.** Severity decides who is called and whether a notification is needed, so it must reflect business impact. A still counts systems, not harm; C confuses reporting rules with the bank's own levels; D rates by technical drama. See "Severity in business terms".

</details>

## 📚 References
Pages on sre.google could not be opened from this environment; what this lesson says of them is as reported in search summaries.
- Taylor, M., "Shrinking the impact of production incidents using SRE principles—CRE Life Lessons", Google Cloud blog, 9 September 2019 (opened 2026-11-20): https://cloud.google.com/blog/products/devops-sre/shrinking-the-impact-of-production-incidents-using-sre-principles-cre-life-lessons/
- Beyer, B., Jones, C., Petoff, J. and Murphy, N. R. (eds.), *Site Reliability Engineering* (O'Reilly, 2016), chapter 6, "Monitoring Distributed Systems": https://sre.google/sre-book/monitoring-distributed-systems/ (golden signals; symptom-based alerting).
- *Site Reliability Engineering*, chapter 14, "Managing Incidents": https://sre.google/sre-book/incident-response/ (roles; basis in the Incident Command System).
- Davidovič, Š., *Incident Metrics in SRE* (O'Reilly/Google, 2021): https://sre.google/resources/practices-and-processes/incident-metrics-in-sre/ (mean-time metrics).
- Library lessons are linked where they are used in the text.

---

# 8.2 — Problem management and learning from failure
*Level: 🟡 Intermediate* · *Prerequisites: 8.1* · *Step: Run, Improve*

**After this you can** run a blameless post-incident review, open a problem record that links repeated incidents to their causes, and get the resulting fixes into a product backlog with an owner, a date and funding. *Study time: reading about 20 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- An **incident** is about getting service back; a **problem** is what must change so it stops happening, usually several things. Incident management restores service; problem management makes failure rarer or smaller.
- A **post-incident review** is **blameless**: it asks what made each action seem sensible at the time, not who to punish.
- The rule that matters most: **an action without an owner, a date and a backlog link is a wish.**
- Look for **contributing factors**; a single "root cause" usually means the analysis stopped early.
- Decision cue: three similar incidents in a quarter, each "resolved by restart", is an unmanaged problem, not bad luck.
- Biggest trap: problem work as unfunded spare-time work. Reserve capacity for it.

## 🧭 Why it matters
Najm Bank, its people and every figure in this lesson are fictional and illustrative, not benchmarks.

For five months, card authorisations at Najm Bank slowed for about twenty minutes at every month-end, and in two of those months again the next morning. Each time, the on-call engineer restarted a connection pool (a shared set of open database connections) and the symptom went away. Seven incidents, seven closed "resolved by restart". Different people handled each, and none was severe enough for a review, so nobody connected them. They were separate from the two-hour salary-day app slowdown of lesson 4.3, which was reviewed and had a different cause: a peak load nobody had specified or tested.

The bigger incidents had formal reports. Nour counted them for an internal audit: eleven reports, 63 actions, 14 completed. The rest sat in documents, assigned to "IT operations" or to people who had changed role. The holiday outage of lesson 8.1 shared two contributing factors with a report from the previous spring, whose action "add a timeout on the processor connection" had never been done.

The division did not lack analysis. It lacked a path from analysis to funded work, and a habit of looking across incidents.

## 📐 How it works

### 🟢 The essentials

**Four words, used consistently.** These words are common in service management, and the frameworks compared in lesson 12.1 define them formally; this course defines each by the work it asks for.

| Term | What it means here | Example |
|---|---|---|
| **Incident** | Customers or staff can see something has stopped working or got worse; get it back (lesson 8.1) | Month-end authorisation slowdown on 31 May |
| **Problem** | The thing we must change so this stops happening; often several things, and at first unknown | Something makes authorisations slow under month-end load |
| **Workaround** | What the on-call engineer does to get service back today | Restart the connection pool |
| **Cause understood** | A problem status: we know why, the workaround is written down, the fix waits in the backlog | A batch job exhausts the pool; restart works; fix planned |

Incident management is measured on **restoring service fast**, problem management on **making failures rarer or smaller**. Mixing them gives either slow restoration (debugging while customers wait) or no learning.

**Two ways problems are found.**
- **Found from incidents:** every Sev 1 and Sev 2 opens or links to a problem record; so does any pattern of smaller incidents (three similar ones in a quarter is a reasonable starting threshold).
- **Found from trends and risks:** rising error rates, a component near end of support, a lucky near miss, a risk with no impact yet.

**The problem record.** Like the incident record, keep it short and linked.

| Field | Purpose |
|---|---|
| Linked incidents | Frequency and total impact |
| Affected service and components | Links to the catalogue and what is running (lessons 2.3, 6.3) |
| Contributing factors so far | Current understanding, updated as it improves |
| Workaround | So the next on-call engineer does not rediscover it |
| Actions, each with owner, due date and backlog link | The path to a fix |
| Problem owner | One named person, usually in the owning product or platform team |
| Status | Open, cause understood, fix in progress, closed with evidence |

**The post-incident review** (often called a postmortem). A structured meeting soon after a qualifying incident, producing a written report. Google's SRE book is reported to list triggers such as user-visible downtime beyond a threshold and data loss of any kind, and to let any stakeholder request a review. A bank should add regulatory triggers and serious near misses, all set in advance.

A useful report has six parts:
1. **Summary** in plain words: what happened, impact, duration.
2. **Timeline** from the scribe's record (lesson 8.1), with what people knew at each point.
3. **Contributing factors:** technical, process, information, organisational.
4. **What went well,** so it is kept.
5. **Where we got lucky,** because luck hides risks.
6. **Actions,** each with owner, date and backlog link.

**Blameless, and why.** John Allspaw, then at Etsy, described in a widely cited 2012 post engineers who made mistakes giving a detailed account of what they did, expected and assumed, without fear of punishment, because that account is how the organisation learns. Expecting blame, people give thin accounts. Blameless does not mean unaccountable: accountability here means **giving an account**, fully and honestly. Deliberate misconduct goes through a separate HR process.

**The memorable rule: an action without an owner, a date and a backlog link is a wish.** Put it at the top of the report template.

### 🟡 Going deeper

**Contributing factors, not a root cause.** The physician and safety researcher Richard Cook, in *How Complex Systems Fail* (1998), is widely quoted for the point that attributing an accident to a single "root cause" is fundamentally wrong, because failures in complex systems need several faults together. A review ending "root cause: engineer applied wrong configuration" has stopped too early. Better questions:

| Instead of | Ask |
|---|---|
| Who made the mistake? | What made that action look right at the time? |
| Why didn't they follow the procedure? | Was the procedure findable, current and workable at 2 a.m.? |
| What was the root cause? | Which conditions had to be true together for this to happen? |
| Why wasn't it caught? | Which checks existed, and why did each not stop it? |
| How do we stop people doing that? | How do we make the safe action the easy one? |

The "five whys" technique digs past the first answer, but alone it follows one chain and tends to end at a person.

**Four kinds of action.** Sort actions so the set is balanced:

| Kind | Aim | Example from the month-end slowdown |
|---|---|---|
| **Prevent** | Make the failure less likely | Move the batch job off the shared pool |
| **Detect** | Find it sooner | Page on authorisation time at month-end, not only on failures |
| **Mitigate** | Make it smaller when it happens | A feature flag (a switch that turns a function off without a release) to shed non-urgent work |
| **Recover and learn** | Restore faster, spread the lesson | Add the workaround to the runbook (step-by-step operating instructions); share the review |

**From action to funded work.**
- **Actions go into the owning team's backlog,** linked to the problem record (lesson 9.3), not a spreadsheet.
- **Capacity is reserved** for reliability and problem work, reviewed quarterly; lesson 8.3 shows how the error budget can move it.
- **Large fixes go to portfolio review** (lesson 3.3), with incident history as evidence and Tariq sizing them.
- **Open actions are reviewed monthly** by age, chaired by someone senior enough to unblock them.

**Culture is measurable enough to matter.** DORA's capability guidance on culture draws on the sociologist Ron Westrum's typology of pathological, bureaucratic and generative organisations: in a generative culture, failure leads to inquiry; in a pathological one, to scapegoating. DORA reports that a high-trust culture with good information flow predicts better software delivery and organisational performance. The practical test: when someone reports a near miss, are they thanked or questioned?

### 🔴 Expert view

**Look across incidents, not only at each one.** Once a quarter, run a **trend review**: group incidents by service, component, time pattern, change link and supplier, and ask which groups have no problem record.

**Measuring problem management.** The headline is the **repeat incident rate**: incidents linked to an already-known problem, which falls only when fixes work (audit a sample, because it also falls if people stop linking). Add the age of open problems and actions by owner (where to unblock or fund), the share of actions done by their due date, and the share of qualifying incidents reviewed on time. Do not set targets on the number of problems closed: closing is easy, fixing is not.

**Sharing, suppliers and audit.** Publish review summaries internally. When a supplier contributes, the problem record still belongs to the bank, with the supplier's action tracked in Lina's supplier review (lesson 10.2); "supplier issue" never closes a record without evidence of a fix. The chain of incident, review, problem and completed actions is also audit evidence: ask Nour which incidents need a formal cause analysis for the supervisor, and by when.

**AI in reviews.** AI tools can draft a timeline or cluster similar incidents. Treat output as a checked draft, keep incident data in approved tools, and never let it replace people's own account. For an engineering view of the review practice, see [*Cloud & DevOps: Zero to Hero*, lesson 5.3 — Incidents and blameless postmortems](../cloud/index.html#/5.3); for turning AI system incidents into tests, see [*Software Testing: Zero to Hero in the AI Era*, lesson 7.3 — Safety, robustness, fairness and monitoring: red-teaming, metamorphic tests, drift and turning incidents into tests](../testing/index.html#/7.3).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Problem record template** | The fields above | Every Sev 1–2, and any pattern of three similar incidents |
| **Post-incident review template** | The six parts above | After each qualifying incident |
| **Review triggers list** | The conditions that require a review, set in advance, including regulatory ones | Once, then reviewed yearly with risk |
| **Facilitator question card** | The "instead of / ask" questions above | Handed to whoever runs the review |
| **Action balance check** | Sort actions into prevent, detect, mitigate, recover and learn | Before the report is signed off |
| **Trend review** | Quarterly grouping of incidents by pattern | To find problems no single incident shows |
| **Open actions review** | Monthly list of problem actions by age, owner and blocker | Chaired by someone who can unblock |

## 🏛️ In practice at Najm Bank
Huda's first trend review found the seven month-end incidents in ten minutes. Yousef opened a problem record; Reem named an engineer from her team as owner. Fictional and illustrative:

> **PRB-0142: Card authorisation slow at month-end.**
> **Linked incidents:** 7 in 5 months (each month-end, twice again the next morning), each about 20 minutes, plus a contributing factor in the holiday Sev 1.
> **Contributing factors:** (1) a month-end reporting batch, added last year by another team, holds connections from the same pool as live authorisations; (2) the pool size was set years ago and never reviewed; (3) no alert on authorisation time, only on failures; (4) restarts worked, so nobody escalated; (5) the earlier action "add a timeout on the processor connection" was never done because it had no backlog item.
> **Workaround:** restart the pool; now in the runbook with a "link to PRB-0142" step.
> **Actions:** move the batch to its own pool (prevent; Sami's platform team; backlog item CARDS-881; 3 weeks); page on authorisation time (detect; Reem's team; CARDS-882; 1 week); add the processor timeout (mitigate; Reem's team; CARDS-883; 2 weeks); share the review with the other payment teams (learn; Reem; CARDS-884; next month's session).
> **Funding:** fits in the 20% protected foundation share from lesson 4.3, whose spending rule puts incident causes first; Tariq confirmed no extra funding is needed.

The engineer who had added the batch job expected blame. Huda asked what he knew when he chose the shared pool: the platform documentation showed one pool and no limits. That produced a fifth action, updated guidance from Sami's team. Nour closed her audit finding three months later, when the repeat incidents had stopped.

## 🛠️ Exercises
**🟢 Find a hidden problem.** Take the last three months of incidents for one service (or invent a realistic list of fifteen). Group them by component and time pattern. Name at least one group that has no problem record.
*Done when:* you have a grouped list, at least one group of two or more related incidents, and a one-line problem statement for it.

<details><summary>Model answer and self-check</summary>

**Model answer.** Typical findings: "slow login" every Monday morning; certificate expiries on different servers; incidents after every release of one component. A problem statement: "Login slows every Monday 08:00–08:30; four incidents in a quarter; cause unknown; workaround: none." **Self-check.**
- Did you group by pattern, not just by service name?
- Is the problem statement about a cause to be found, not a fix already chosen?
- Would any single incident have shown the group? If not, that is the point.

</details>

**🟡 Run a blameless review.** Hold a 60-minute review of a real recent incident (or the holiday payment outage in lesson 8.1) using the six-part template and the facilitator question card.
*Done when:* a report exists with a timeline, at least four contributing factors across at least two categories (technical, process, information, organisational), and actions sorted into the four kinds.

<details><summary>Model answer and self-check</summary>

**Model answer.** For the holiday outage: cause alerts flooded the operations centre (information); no single commander (process); supplier ran its own bridge (organisational); a missing processor timeout (technical); an unfinished action from an earlier review (organisational). Actions: page on symptoms (detect), commander rota (recover), supplier clause (mitigate), add the timeout (prevent), share the review (learn). **Self-check.**
- Does the report name conditions, not culprits?
- Did you include "what went well" and "where we got lucky"?
- Is every action owned by a person, not a department?

</details>

**🔴 Build the path from action to funded work.** For one product, design how problem actions become backlog items, how much capacity is reserved, who reviews open actions monthly, and when a fix goes to portfolio review instead. Agree it with the product owner and finance partner.
*Done when:* a one-page policy exists, the product owner and finance partner have commented on it, and at least three existing open actions have been moved into the backlog with owners and dates.

<details><summary>Model answer and self-check</summary>

**Model answer.** Every action becomes a linked backlog item within five working days; 15–20% of capacity is reserved for two quarters, then reviewed using repeat incidents and error budget use (lesson 8.3); fixes beyond a quarter's capacity go to portfolio review; the product manager (at Najm Bank, Reem) reviews open actions monthly with the business head (the head of retail banking) and the head of operations; the finance partner (Tariq) comments on the reserved capacity. **Self-check.**
- Is the reserved capacity explicit and time-limited?
- Is there a route for fixes too big for one team?
- Did the old open actions really move, or only get re-listed?

</details>

## ⚠️ Mistakes and traps
- **Closing incidents "resolved by restart" and moving on.** Patterns stay invisible. Run a quarterly trend review.
- **Hunting a single root cause.** The analysis stops at the first convenient answer, often a person. List contributing factors of every kind.
- **Blame dressed as accountability.** People stop giving full accounts. Keep discipline out of reviews.
- **Actions in a document, not a backlog.** They are never weighed against features. Link each to a backlog item.

## 🧾 Recap
- Incidents are about getting service back; problems are what must change, found from incidents and from trends and risks.
- Run blameless reviews against triggers set in advance; find contributing factors and balance the four kinds of action.
- **An action without an owner, a date and a backlog link is a wish.**
- Reserve product capacity for problem work, send large fixes to portfolio review, and review open actions monthly.
- Measure repeat incidents, action completion and review timeliness, not the number of problems closed.

## ✍️ Check yourself
**1. Seven month-end slowdowns at Najm Bank were each closed "resolved by restart". What practice would most likely have found the pattern earlier?**

- A. Raising the severity of every slowdown so that each one received a full review.
- B. A quarterly trend review grouping incidents by component and time pattern.
- C. Asking the on-call engineers to write longer resolution notes on each ticket.
- D. Replacing the connection pool with a newer product during the next release.

<details><summary>Answer</summary>

**B.** The pattern was invisible in any single incident; grouping shows it. A overloads reviews, C still looks at one ticket at a time, and D picks a fix before knowing the causes. See "Look across incidents, not only at each one".

</details>

**2. A review concludes: "Root cause: engineer applied the wrong configuration. Action: retrain the engineer." What is the main weakness?**

- A. The action is too weak; a second approver for every configuration change is needed.
- B. It names the engineer, so the report must be anonymised before it is shared.
- C. It needs a five-whys analysis to trace the error down to its one true root cause.
- D. It stops at a person and ignores the conditions that made the error easy to make.

<details><summary>Answer</summary>

**D.** Asking what made the action look right, and why checks missed it, leads to fixes that help everyone. A adds a control before anyone knows why the error looked right; B hides the name but keeps the flawed analysis; C still hunts a single root cause along one chain. See "Contributing factors, not a root cause".

</details>

**3. Nour finds that 14 of 63 post-incident actions from the past year were completed. Which change best addresses this?**

- A. Ask each review to produce fewer actions so the completion rate looks better.
- B. Move the actions to a shared spreadsheet that the operations centre maintains.
- C. Put each action in the owning team's backlog, with capacity reserved for the work.
- D. Hold the reviews sooner after each incident, while the details are still fresh.

<details><summary>Answer</summary>

**C.** Actions outside the backlog compete for no capacity and are lost. A games the measure, B keeps them outside the backlog, and D improves reviews but not their actions. See "From action to funded work".

</details>

**4. In the month-end slowdown review, the engineer who added the batch job expects blame. How should Huda run it to learn the most?**

- A. Ask what information he had when he chose the shared pool, and record it.
- B. Exclude him from the meeting so that others can speak more freely about the error.
- C. Agree beforehand that nobody is accountable, so the review can be kept short.
- D. Note the error in his file, then focus the rest of the meeting on technical fixes.

<details><summary>Answer</summary>

**A.** A blameless review seeks a full account of what people knew; that found the documentation gap. B loses the best witness, C confuses blameless with unaccountable, and D brings blame into learning. See "Blameless, and why".

</details>

**5. Which measure best shows whether Najm Bank's problem management is actually working?**

- A. The number of problem records closed each month across all product teams.
- B. The number of post-incident reviews held, whatever the length of their reports.
- C. The average number of actions each review produces across the whole division.
- D. The rate of incidents linked to already-known problems, checked by sample audit.

<details><summary>Answer</summary>

**D.** Repeat incidents fall only when fixes work; a sample audit guards against people not linking. A rewards closing without fixing, B counts activity, and C rewards long lists. See "Measuring problem management".

</details>

## 📚 References
None of these sources could be opened from this environment; what this lesson says of them is as reported in search summaries.
- Beyer, B., Jones, C., Petoff, J. and Murphy, N. R. (eds.), *Site Reliability Engineering* (O'Reilly, 2016), chapter 15, "Postmortem Culture: Learning from Failure": https://sre.google/sre-book/postmortem-culture/ (review triggers; any stakeholder may ask for one).
- Allspaw, J., "Blameless PostMortems and a Just Culture", Etsy Code as Craft blog, May 2012: https://www.etsy.com/codeascraft/blameless-postmortems
- Cook, R. I., *How Complex Systems Fail* (Cognitive Technologies Laboratory, University of Chicago, 1998, revised 2000) (the point on "root cause").
- DORA, "Generative organizational culture", capability guide: https://dora.dev/capabilities/generative-organizational-culture/ (Westrum typology; culture finding).
- Westrum, R., "A typology of organisational cultures", *Quality and Safety in Health Care* 13 (suppl. 2), 2004 (citation as given in DORA's guidance).

---

# 8.3 — Service levels, SLOs and error budgets as a management tool
*Level: 🟡 Intermediate* · *Prerequisites: 1.3, 2.3, 8.1* · *Step: Run*

**After this you can** write an SLO sheet for two customer journeys (indicator, exclusions, target, window, error budget, owner, data source) and agree with the business, operations and finance an error budget policy that says what changes when the budget runs low. *Study time: reading about 20 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- A **service level indicator (SLI)** measures how the service behaves for users; a **service level objective (SLO)** is its target over a window; a **service level agreement (SLA)** is a promise with a penalty.
- The **error budget** is the unreliability the SLO allows: at 99.9%, 0.1% of requests may fail in the window.
- The rule that matters most: **the SLO is a business decision written as a number.**
- A budget only manages anything if a **policy**, agreed in advance, says what changes when it runs low.
- Decision cue: if product and operations argue about release pace with opinions, write the SLO and policy.
- Biggest trap: measuring servers, or averaging across systems; "99.9% availability" can hide a four-hour payment outage.

## 🧭 Why it matters
Najm Bank, its people and every figure in this lesson are fictional and illustrative, not benchmarks.

Omar's report showed 99.9% availability for the quarter of the holiday outage (lesson 8.1): an average over 140 systems, measured by whether servers answered a ping. The four-hour card failure did not show. A board member asked why the number was green.

Meanwhile Reem wanted weekly releases of Cards & Payments; Yousef wanted fewer, because the last two had each caused an incident. Neither had a number. Tariq, asked to fund a resilience project, wanted to know how much reliability the bank was buying.

An SLO with an error budget gives all three the same number: how reliable each journey must be, and how much unreliability is left this month.

## 📐 How it works

### 🟢 The essentials

**Three terms.** A 2018 Google Cloud blog post by two Google product managers gives short definitions, restated here in this course's words:

| Term | In plain words | Najm Bank example |
|---|---|---|
| **SLI** | A direct measurement of how the service behaves | Share of card authorisations answered within 2 seconds |
| **SLO** | The target for an SLI over a time window | 99.9% good, over a rolling 30 days |
| **SLA** | A promise to someone using the service, with a penalty if missed | A supplier contract term with service credits (a fee reduction when the target is missed) |

The same post notes that an SLA's target is normally **looser** than the internal SLO, so the internal objective warns before the external promise breaks.

**The error budget** is one minus the SLO: the share of events (or time) allowed to be bad in the window.

| SLO over 30 days | Error budget | As time, if the SLI were time-based | As failed requests, at 10 million requests a month |
|---|---|---|---|
| 99% | 1% | about 7.2 hours | 100,000 |
| 99.5% | 0.5% | about 3.6 hours | 50,000 |
| 99.9% | 0.1% | about 43 minutes | 10,000 |
| 99.95% | 0.05% | about 22 minutes | 5,000 |
| 99.99% | 0.01% | about 4.3 minutes | 1,000 |

The request volume is an illustrative figure. Each extra "nine" cuts the budget by a factor of ten, and in practice raises the cost of running the service. A 2019 Google Cloud blog post on production incidents states that reliability costs "tend to be exponential", and that it "can be 100 times more expensive to run a service that is 10 times more reliable". That is why 100% is the wrong target. Google's SRE book is reported to add that users cannot tell the difference between very high and perfect, because their own devices are less reliable still: a user on a 99%-reliable smartphone cannot tell 99.99% from 99.999%.

**Choose journeys, not systems.** Write SLOs for the few **customer journeys** that matter (pay by card, log in, transfer money), measured as close to the customer as practical, not for each server.

**Good SLIs share four features.** These are this course's recommendations.
- **User-centred:** it would move if customers had a worse experience.
- **Ratio of events:** good events over valid events, which handles busy and quiet hours fairly.
- **Clear exclusions:** for example, a decline because the card is blocked is a "good" outcome; say so in writing.
- **From an existing record:** the data comes from logs or monitoring already collected, not a monthly spreadsheet.

**The memorable rule: the SLO is a business decision written as a number.** Engineers propose what is measurable and achievable; product, operations and finance agree what is worth paying for.

### 🟡 Going deeper

**The error budget policy.** An SLO without a policy is a dashboard. Google's *Site Reliability Workbook* has an example policy, reported to pause changes other than urgent and security fixes when a service has exceeded its budget over the previous four weeks, and to require a postmortem (the post-incident review of lesson 8.2) when one incident consumes more than 20% of that budget. A 2018 Google Cloud blog post, "Good housekeeping for error budgets", calls a release freeze "a last-resort action", suggests alternatives such as moving the team from mostly feature work to an even split while out of SLO, and warns that changes pile up during a freeze.

A bank's policy can have four bands:

| Budget remaining in the window | What changes | Who decides |
|---|---|---|
| **More than half** | Normal release pace; risky experiments allowed | Product team |
| **A quarter to a half** | Larger changes need a reviewed rollback plan; reliability items move up | Product manager with on-call lead |
| **Less than a quarter** | Only small or reliability-improving changes; agreed capacity shifts to reliability | Product manager and head of operations |
| **Exhausted** | Pause feature releases and hold a review; urgent, regulatory and security fixes go ahead only with Omar's approval, logged as exceptions | Head of retail banking with Yousef; Omar for exceptions |

Illustrative bands. The policy is **signed before it is needed** by the product owner, head of operations and finance partner, with the business head consulted. Budget left over is information too: release more boldly, or lower an unneeded target.

**SLOs connect to the change model.** Lesson 6.2 set scrutiny by change risk; the budget adds a second input, replacing "operations says no" with a rule both sides wrote.

**Dependencies limit what you can promise.** A journey that depends in sequence on core banking, the network and the processor can be no more reliable than the weakest of them, and is usually less. That tells Reem which dependency to tackle first. The engineering is in [*Cloud & DevOps: Zero to Hero*, lesson 5.2 — SLOs, error budgets, alerting and on-call that people can sustain](../cloud/index.html#/5.2).

**SLAs, SLOs and suppliers.** Keep three numbers distinct: the internal SLO (tight, to steer), any SLA to customers or business lines (looser), and supplier SLAs (what the bank is promised). If a supplier SLA is looser than a dependent journey's SLO, the bank carries that gap: a sourcing and risk question for Lina and Nour.

### 🔴 Expert view

**SLOs as a management tool, not an engineering metric.** In its 2021 report, DORA expanded a measure it had previously called availability into reliability, asking respondents to rate their ability to meet or exceed their reliability targets. The Google Cloud announcement says teams "see better outcomes when they also prioritize operational performance", and names the SLI/SLO framework as a practical technique. The same budget then serves several forums: backlog capacity (lesson 8.2), the change path (lesson 6.2), portfolio funding of platform fixes (lesson 3.3), cost reviews (lesson 10.1), supplier reviews (lesson 10.2) and board risk reporting (lesson 10.3).

**How SLOs get gamed, and the defence.**

| Gaming pattern | Defence |
|---|---|
| Excluding "maintenance" or "supplier incidents" | Exclusions listed and reviewed by Nour |
| Targets set at last quarter's result | Start from customer need and cost |
| Redefining "good" after a bad month | Version the SLO sheet; approve changes |

**Reliability and regulation.** Operational resilience rules, where a supervisor has them, may ask how much disruption important services can tolerate. That differs from an SLO, which steers day-to-day work, so do not relabel one as the other. Ask Nour: which services does our supervisor treat as important, and how should SLO data feed that evidence?

**Reporting to the board.** Replace estate-wide availability with five to eight journeys, each with its SLO, met or not, budget left and one sentence of action.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **SLO sheet** | Per journey: SLI, exclusions, target, window, budget, data source, owner, version | Each critical journey; review twice a year |
| **Error budget table** | Each target as time and failed events at your volume | When agreeing a target |
| **Error budget policy** | Budget bands, what changes, who decides, exception log | Signed before the first SLO goes live |
| **Dependency chain sketch** | In-sequence dependencies and each one's SLO or SLA | Before setting targets |
| **Budget burn report** | Budget used, by cause (releases, incidents, suppliers) | Weekly in the team |
| **Board reliability table** | Journeys, SLO met, budget left, trend, action | Executive reports |

## 🏛️ In practice at Najm Bank
Reem drafted two SLO sheets; Yousef checked the data; Tariq priced the targets; Nour reviewed the exclusions. Fictional and illustrative:

> **SLO sheet: Pay by card (v1).**
> **SLI:** share of card authorisation requests that receive a valid answer (approve or decline) within 2 seconds, measured at the bank's authorisation gateway.
> **Valid events:** all authorisation requests reaching the gateway. **Good:** answered within 2 seconds. Declines for customer reasons (insufficient funds, blocked card) count as good.
> **Exclusions:** none for planned maintenance; processor failures count, and are reported separately for Lina's supplier review.
> **Target and window:** 99.9% over a rolling 30 days. At about 10 million requests a month, the budget is about 10,000 bad requests.
> **Owner:** Reem (product); data from the gateway logs (Sami's platform).
>
> **SLO sheet: Log in to the app (v1).** SLI: share of login attempts with valid credentials that succeed within 3 seconds; target 99.5% over 30 days; owner Reem.
>
> **Error budget policy:** the four bands in this lesson, signed by Reem, Yousef and Tariq, with the head of retail banking consulted; exceptions approved by Omar and logged.

Lesson 4.3's quality requirements sheet had asked for 99.95% of each calendar month. Tariq priced it: Sami estimated that 99.95% needed a second processor link and faster failover, and 99.99% a second active processing site as well, several times today's running cost. The head of retail banking chose 99.9% over a rolling 30 days for now; Huda updated the 4.3 requirement and recorded why. By the 20th of the first month 60% of the card budget was used, mostly by one release; the team entered the "quarter to a half" band, reviewed rollback plans and brought forward the processor timeout from lesson 8.2. The release argument now took ten minutes.

## 🛠️ Exercises
**🟢 Turn availability into journey SLIs.** Pick two customer journeys in your organisation. For each, write the SLI as a ratio of good events to valid events, with what counts as good, what is valid, what is excluded, where the data comes from and who owns it.
*Done when:* both SLIs name an owner and a data source, and a peer outside IT can say whether their last use of each journey would have counted as good.

<details><summary>Model answer and self-check</summary>

**Model answer.** "Transfer money: share of valid transfer submissions confirmed within 5 seconds, measured at the mobile API gateway. Rejections for customer reasons (limit reached) count as good. No exclusions. Data: gateway logs. Owner: the payments product manager." "Log in: share of logins with valid credentials that succeed within 3 seconds; data from the identity service logs; owner: the app product manager." **Self-check.**
- Would the SLI move if customers had a worse experience?
- Is it a ratio of events rather than server uptime?
- Are exclusions few, and does the data already exist?

</details>

**🟡 Price the nines and finish the sheets.** For each of your two journeys, fill the error budget table for three possible targets at your real monthly volume, estimate roughly with a finance or operations colleague what each higher target would need, and recommend one. Then complete both SLO sheets.
*Done when:* each journey has three targets with budgets as events and as time over 30 days, each with a rough cost note, and two complete SLO sheets (SLI, exclusions, target, window, budget, owner, data source) name who must agree.

<details><summary>Model answer and self-check</summary>

**Model answer.** Transfers, at 2 million a month (illustrative): 99.5% allows about 10,000 failures or 3.6 hours; 99.9% about 2,000 or 43 minutes; 99.95% about 1,000 or 22 minutes. 99.9% may need better alerting and a rehearsed rollback (modest cost); 99.95% a second active site (major cost). Sheet: the 🟢 SLI, 99.9% over a rolling 30 days. Login, at 4 million a month (illustrative): 99.5%, about 20,000 failures or 3.6 hours; 99.9%, about 4,000 or 43 minutes; 99.95%, about 2,000 or 22 minutes. 99.9% would need a standby identity service (modest cost); 99.95% a second active site and a resilient identity supplier (major cost). Sheet: the 🟢 login SLI, 99.5% over a rolling 30 days for now, revisited after two quarters of data. Both agreed by the product owner, head of operations and finance partner. **Self-check.**
- Did you use your real volumes, labelled as such?
- Does each step up have a cost note, and did you avoid 100%?
- Does each sheet have every field, with named approvers?

</details>

**🔴 Agree the error budget policy.** Draft a four-band policy for one product, including how exceptions are approved and recorded. Walk it through with the product owner, head of operations and finance partner, using one realistic month of budget data.
*Done when:* the policy is signed or has written comments from all three, and you have shown what it would have changed in the sample month.

<details><summary>Model answer and self-check</summary>

**Model answer.** Start from the four bands and add the window, the weekly burn report, what counts as reliability work, who grants and logs exceptions, and a review date. For the sample month, show when each band was crossed and what would have changed. **Self-check.**
- Were all three parties involved before the policy was needed?
- Does exhaustion change something real, with exceptions recorded?
- Did you avoid making a freeze the only response?

</details>

## ⚠️ Mistakes and traps
- **Measuring servers, not journeys.** Servers can be up while customers fail. Define SLIs at the journey.
- **Averaging everything.** An estate-wide figure hides the outage that matters. One SLO per journey, on a rolling window.
- **Chasing 100%.** Each extra nine costs far more and customers often cannot tell. Price the targets and choose.
- **An SLO with no policy.** A number nobody acts on changes nothing. Sign the policy first.
- **Excluding what hurts.** "Supplier incidents excluded" flatters the number while customers suffer. Keep exclusions few and reviewed.

## 🧾 Recap
- An SLI measures the journey as good over valid events; an SLO is its target over a window; an SLA is an external promise, usually looser.
- The error budget is one minus the SLO; each extra nine shrinks it tenfold and raises cost steeply.
- **The SLO is a business decision written as a number**, agreed by product, operations and finance.
- An error budget policy, signed in advance, says what changes as the budget runs low; a freeze is a last resort.
- Use SLOs in backlog, change, portfolio, cost, supplier and board decisions.

## ✍️ Check yourself
**1. Omar's report shows 99.9% availability across 140 systems for a quarter in which card payments failed for four hours. What is the main flaw?**

- A. The quarter is too short a window to calculate a reliable availability figure.
- B. Availability should be reported as downtime in minutes rather than as a percentage.
- C. The target of 99.9% is too low for a bank, so it should be raised to 99.99%.
- D. It averages server checks across systems instead of measuring customer journeys.

<details><summary>Answer</summary>

**D.** The figure averages server checks across the estate, so one journey's failure disappears. A and B change presentation, not what is measured; C raises a target on a meaningless indicator. See "Choose journeys, not systems".

</details>

**2. The card journey's SLO is 99.9% over 30 days, at about 10 million requests a month. Roughly how many bad requests does the error budget allow?**

- A. About 1,000 bad requests in the window.
- B. About 10,000 bad requests in the window.
- C. About 100,000 bad requests in the window.
- D. About 43,000 bad requests in the window.

<details><summary>Answer</summary>

**B.** 0.1% of 10 million is 10,000. A is the budget at 99.99%, C at 99%, and D confuses the 43 minutes of a time-based budget with a request count. See "The error budget".

</details>

**3. Reem's card budget is exhausted by the 25th. The new policy says feature releases pause. A regulatory change must go live on the 28th. What should happen?**

- A. Release it as an exception approved by the named executive and recorded.
- B. Delay it until the new window starts, because the policy allows no exceptions.
- C. Release it quietly through the standard path, since regulatory work is not a feature.
- D. Lower the SLO for this month so that the budget is no longer shown as exhausted.

<details><summary>Answer</summary>

**A.** The policy's "Exhausted" band lets an urgent, regulatory or security fix go ahead only with Omar's approval, logged as an exception. B ignores that, C skips the approval the band requires, and D games the target. See "The error budget policy".

</details>

**4. Tariq asks whether the bank should simply set every critical journey's SLO at 99.99%. Which response best follows the lesson?**

- A. No: higher targets cannot be measured with the bank's current observability tools.
- B. Yes: set 99.99% now, and lower it later if the cost proves too high in practice.
- C. No: each extra nine costs far more and customers may not notice; price, then choose.
- D. No: a higher SLO would make the error budget larger and allow too many failures.

<details><summary>Answer</summary>

**C.** Reliability costs rise steeply with each nine, so the target is a priced business decision. A is not a claim the lesson makes, B commits spending before anyone has priced the target, and D reverses the arithmetic. See "The error budget".

</details>

**5. The processor's contract promises 99.5% availability, but Reem's internal SLO for card payments is 99.9%. What is the right next step?**

- A. Exclude processor failures from the SLO so that the bank's own figure stays accurate.
- B. Treat the gap as a sourcing and risk question for Lina and Nour, with evidence.
- C. Lower the internal SLO to 99.5% so that it matches the supplier's promise exactly.
- D. Accept the gap, since the contract's service credits compensate for any shortfall.

<details><summary>Answer</summary>

**B.** The bank carries the gap between what it is promised and what customers need. A hides harm, C lets the supplier set the target, and D confuses money back with reliability customers can feel. See "SLAs, SLOs and suppliers".

</details>

## 📚 References
The Google Cloud posts were opened on 2026-11-20. Pages on sre.google could not be opened; what this lesson says of them is as reported in search summaries.
- Judkowitz, J. and Carter, M., "SRE fundamentals: SLIs, SLAs and SLOs", Google Cloud blog, 19 July 2018: https://cloud.google.com/blog/products/devops-sre/sre-fundamentals-slis-slas-and-slos (definitions; SLA looser than internal SLO).
- Warner, A. and Bramley, A., "Good housekeeping for error budgets—CRE life lessons", Google Cloud blog, 28 June 2018: https://cloud.google.com/blog/products/devops-sre/good-housekeeping-error-budgetscre-life-lessons (freeze as a last resort).
- Taylor, M., "Shrinking the impact of production incidents using SRE principles—CRE Life Lessons", Google Cloud blog, 9 September 2019: https://cloud.google.com/blog/products/devops-sre/shrinking-the-impact-of-production-incidents-using-sre-principles-cre-life-lessons/ (cost of reliability).
- Smith, D., "2021 Accelerate State of DevOps report addresses burnout, team performance", Google Cloud blog, 21 September 2021: https://cloud.google.com/blog/products/devops-sre/announcing-dora-2021-accelerate-state-of-devops-report
- Thurgood, S., "Example Error Budget Policy", *The Site Reliability Workbook* (O'Reilly, 2018), Appendix B: https://sre.google/workbook/error-budget-policy/ (the example policy).
- *Site Reliability Engineering* (O'Reilly, 2016), chapter 3, "Embracing Risk": https://sre.google/sre-book/embracing-risk/ (error budget; users cannot tell very high from perfect), and chapter 4, "Service Level Objectives": https://sre.google/sre-book/service-level-objectives/
