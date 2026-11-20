# Module 6 — Release and change

*Module 5 produced tested, recorded, releasable software. This module is about the moment that software meets production and customers, which is where most of an IT department's arguments about speed and stability happen. At Najm Bank's Technology division the arguments are familiar: features that are finished but wait weeks for a monthly release window; a weekly change board that reads forty change forms in ninety minutes and still misses the one that causes the outage; a month-end freeze that pushes risk into the days after it; test environments that are booked out and patched by hand; and nobody able to say with confidence which version of the cards platform is running right now. This is not an engineering module. Release techniques, environments and infrastructure as code are taught elsewhere in the library, and each lesson links to them. Here you make the operating-model decisions: who decides to put software into production and who decides to give it to customers; how change control can judge risk by evidence rather than by meeting; and which environments the bank needs, who owns them, and how it keeps a trustworthy record of what is running where. Each lesson leaves an artefact: a release policy, a change model, and an environment map with a "what is running" record.*

> **Steps:** Release — move changes into production safely and often, decide separately when customers get them, approve by risk and evidence, and always know what is running.

---

# 6.1 — Release versus deployment, and who decides each
*Level: 🟡 Intermediate* · *Prerequisites: 5.1, 5.2* · *Step: Release*

**After this you can** write a one-page release policy for one product that separates the deployment decision from the release decision, names who makes each, sets release classes and their sign-offs, and states when a rollout is paused or rolled back. *Study time: reading about 20 min, hands-on about 95 min (estimate).*

## ⚡ In 60 seconds
- A **deployment** puts a version of software into an environment, such as production. A **release** makes a capability available to customers or users. They can happen at different times.
- Separated, each decision has the right owner: the **product team** deploys, within the change policy; the **product manager**, with the business, releases.
- The tools that separate them are ordinary: **feature flags**, **progressive rollouts** and **dark launches**.
- The rule that matters most: **deploy when it is ready; release when the business is ready.**
- Decision cue: if a marketing date forces a deployment date, the two decisions are still glued together.
- Biggest trap: treating feature flags as free. Each is a live control on production that needs an owner and an end date.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

Reem, Product Manager for Cards & Payments, had promised a "split a card purchase into instalments" feature for the summer travel season. Her team finished six weeks early, then waited: Najm Bank deployed customer-facing systems in a monthly Saturday-night window, and the campaign was fixed for the window after that. The code sat unused for six weeks, and on the night thirty-one changes from eleven teams went out together (illustrative figures).

The instalment feature worked. A change to the card authorisation service did not; it slowed responses at Monday's peak. Yousef, Head of IT Operations, faced an awkward choice: roll back the whole batch and withdraw a feature just advertised on television, or find one faulty change among thirty-one under pressure. It took nine hours.

At the review, Omar, the Chief Information Officer, asked why a feature finished in May shared a fate with an unrelated change in July. The bank had one decision ("go live on Saturday") where it needed two: "is this software safe in production?" and "do we want customers to have it now?". This lesson gives each an owner.

## 📐 How it works

### 🟢 The essentials

**Four words people mix up.** Write these definitions into the release policy; most arguments about "the release" are about which one is meant.

| Term | Plain meaning | Question it answers | Typical decider |
|---|---|---|---|
| **Deployment** | Installing a specific version of software (and its configuration) into an environment | Is this version safe to run in production? | The product team, within the change policy (lesson 6.2) |
| **Release** | Making a capability available to users, all or some | Do we want these customers to have this now? | The product manager, with the business owner |
| **Rollout** | The steps by which a deployment or release reaches everyone (for example 1%, 10%, 100%) | How fast, and how do we stop if it goes wrong? | The product team, with operations |
| **Launch** | The business event around a release: campaign, communications, training | Are customers, staff and channels ready? | The business owner, with marketing |

When deployment and release are one event, every release carries technical risk and every deployment carries business risk.

**How they are separated.** Three ordinary techniques:

- **Feature flags** (also called feature toggles): a setting the software checks at run time to decide whether a capability is on, off, or on for some users. The code is deployed with the flag off; the release is the moment someone turns it on.
- **Progressive rollout** (called a canary when the first step is small): the new version or capability goes to a small share of users or servers, is watched, then expands, or stops and reverses.
- **Dark launch**: the new code runs on real production traffic, but its results are not shown to users.

The engineering is taught in [*Cloud & DevOps: Zero to Hero*, lesson 4.2 — Release strategies: rolling, blue-green, canary, feature flags and rollback](../cloud/index.html#/4.2) and [*SaaS Building Blocks*, lesson 6.3 — Feature flags and experiments](../saas/index.html#/6.3).

**Who decides each.** A decision-rights table prevents most release-night arguments:

| Decision | Decides | Must be consulted | Record |
|---|---|---|---|
| Deploy a version to production | Product team (engineer on duty), within the change policy | Operations, if shared components or a busy period are affected | Deployment record from the pipeline |
| Release a capability to some or all customers | Product manager | Business owner; compliance where customer terms, fees or disclosures change | Flag change record with the decision and who made it |
| Pause or roll back a rollout | Anyone on the product team or in operations, without asking | Product manager informed straight away | Rollback record with the trigger that fired |
| Launch (campaign, communications) | Business owner | Product manager, marketing, service desk | Launch plan with its date and the release it depends on |

Two lines matter most. **Stopping is always allowed**: anyone who sees the agreed warning signs may pause or roll back, and the record follows. And **some releases carry regulatory weight**: a change to fees, terms or disclosures may need compliance or legal sign-off; which ones is for Nour's risk team and compliance to say.

### 🟡 Going deeper

**Release classes.** Three or four classes work better than one rule for everything:

| Class | Example at Najm Bank | Release sign-off | Rollout |
|---|---|---|---|
| **Invisible** | Performance fix, refactoring, a deployment with all new capability flagged off | None beyond the deployment record | Progressive deployment, automatic stop on error signals |
| **Visible, low impact** | New wording on a screen, a new filter in transaction history | Product manager | Staff first, then a small share of customers, then all |
| **Visible, customer-affecting** | Instalment plans, a new card control, changed limits | Product manager and business owner; service desk briefed | Staged by customer segment, with a named owner watching agreed signals |
| **Regulated or contractual** | Fee changes, new terms, changes to disclosures or consent | Adds compliance (or legal) as the bank's policy requires | On the agreed effective date, often to all at once, after deployment was proven earlier |

Even a fixed-date release does not fix the deployment date: deploy weeks earlier with the capability off, and release by flag on the effective date.

**Watching a rollout.** A rollout is only as good as its signals and stopping rule. Google's site reliability engineers, writing on the Google Cloud blog in 2017, suggested a first canary step of "normally somewhere between 1% and 10%" depending on the user base, and at least 24 hours between stages because traffic often follows a daily pattern. That is one organisation's practice, not a standard. For a manager the output is a **rollout rule** per release class: steps, signals (error rate, response time, failed payments, contact-centre calls), the stop threshold, and who is told.

**Rollback as a normal act.** A companion post argues that "rollbacks are normal": roll back first, investigate second. If rollback feels like failure, people fix forward at 3 a.m. under pressure. Make it the expected first move, practise it, and record it without blame. It has limits (a database change or a message sent to a customer cannot always be undone); see [*System Design for Vibe Coders*, lesson 4.4 — Rollback, staging, and release gates](../vibe/index.en.html#l4-4).

**Feature flags are a managed inventory.** Pete Hodgson's article "Feature Toggles (aka Feature Flags)" is reported to sort flags into release, experiment, ops and permissioning toggles, each with a different lifespan. In operating-model terms:

- **Every flag has an owner, a purpose, a class and an expiry date.** Release flags go within weeks of full release; a permanent ops flag belongs in the runbook.
- **Changing a flag in production is a change.** It needs a record (who, when, why). How it fits the change model is set out in lesson 6.2: a flag change that follows the agreed rollout rule is pre-approved, and a regulated-class flag change takes the high-risk route.
- **Old flags are risk.** They can be reused by mistake; lesson 6.3 tells a public story of exactly that.

### 🔴 Expert view

**Trains and windows.** A **release train** (a fixed, frequent schedule on which whatever is ready departs) beats monthly batches but still ties deployment to a calendar. Keep fixed windows only for a real constraint, such as a core banking batch, and write the reason into the policy.

**Where you do not control deployment.** **Mobile apps** pass app-store review and customers update when they choose, so server-side flags matter more and old versions must keep working. **Vendor-run SaaS** is deployed by the supplier; the bank controls enablement and configuration. Ask, through Lina's contracts, for notice, new capabilities delivered off, and a test tenant that gets changes first (lesson 10.2).

**Measuring the separation.** DORA (DevOps Research and Assessment, the research programme in lesson 1.3) defines deployment frequency, in a Google Cloud post on its "Four Keys" metrics, as "how often an organization successfully releases to production". That measure does not distinguish deploying from releasing to customers, so report both: deployment frequency and change fail rate show the delivery system's health; time from "deployed" to "released" and flags past expiry show whether unreleased work is piling up as inventory (lesson 1.2).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Release policy** | One page: definitions, decision rights, release classes, rollout rules, stop rights, records | When a team starts deploying independently; review twice a year |
| **Decision-rights table** | Who decides deploy, release, pause and launch, who is consulted, and what record is made | Before the first argument on a release night |
| **Rollout rule card** | Per release class: steps, signals, stop thresholds, who is told | For every visible release; agreed with operations |
| **Flag register** | Every flag with owner, purpose, class, expiry date and current state per environment | From the first flag; reviewed monthly |
| **Feature-flag service** | A tool that stores flags, targets users and records changes (open-source and hosted options exist) | When flags outgrow configuration files |

## 🏛️ In practice at Najm Bank
Illustrative and fictional. After the nine-hour incident, Reem drafted a release policy for Cards & Payments with Sami, Yousef and Nour:

> **Release policy — Cards & Payments v1**
> **Deploy:** any working day, by the engineer on duty, through the standard pipeline, within the change model (lesson 6.2). New capabilities ship with their flag off.
> **Release classes and sign-offs:** invisible (none); visible low impact (product manager); customer-affecting (plus business owner); regulated (plus compliance).
> **Rollout rule (customer-affecting):** staff, then 5%, 25%, all customers, at least one business day per step (illustrative). Stop if authorisation errors or response times exceed agreed thresholds, or contact-centre calls about the feature double.
> **Stop rights:** anyone on the team or in the operations centre; product manager informed at once.
> **Fit with the change model (lesson 6.2):** a flag change that follows this rollout rule is a pre-approved (standard) change, with Reem as its change authority; a regulated-class flag change takes the high-risk route, with compliance as an approver.
> **Flags:** registered with owner and expiry; release flags removed within 30 days of full release (illustrative).
> **Fixed windows:** only for changes touching the overnight card settlement batch.

Yousef asked to see everything deployed that day, so a 2 a.m. alert can be matched to recent changes; Sami put the pipeline's deployment records on the operations centre's screen. Nour asked that every regulated flag change carry the compliance approval reference.

The next instalment change was deployed on a Tuesday with the flag off, released to staff on Wednesday and to customers in steps that week. One mistake survived: the register had no expiry dates at first, and by month three the team had 47 flags, nine for features long released (illustrative). A monthly review removed them.

## 🛠️ Exercises
**🟢 Separate the decisions in a recent go-live.** For a recent change (or Najm Bank's instalment feature), write down when it was deployed, when it was released, who decided each, and what record exists for each.
*Done when:* you have two dates (or a note that they were one event), a named decider for each, and a yes/no for whether a record of each decision exists.

<details><summary>Model answer and self-check</summary>

**Model answer.** Before: deployed and released together in the Saturday window, decided in effect by the marketing calendar; records: one batch change form and an email. After: deployed Tuesday by the engineer on duty (pipeline record), released by Reem in steps from Wednesday (flag change records with her name). **Self-check.**
- Did you separate the two events even if they happened at once?
- Did you name a person or role for each decision, not "IT"?
- Did you find an actual record, not assume one?

</details>

**🟡 Write a release policy.** Using the toolkit, write a one-page release policy for one product: definitions, decision rights, three or four release classes with sign-offs, one rollout rule, stop rights, flag rules and any fixed windows with their reason.
*Done when:* the page fits on one side, each class has a named sign-off, the rollout rule has a measurable stop threshold, and every fixed window states its constraint.

<details><summary>Model answer and self-check</summary>

**Model answer.** For a mobile banking product: deploy any working day through the pipeline, flags off. Classes: invisible (no sign-off), low impact (product manager), customer-affecting (plus business owner), regulated (plus compliance). Rollout: staff, 5%, 25%, all; stop if login failures rise above 2% or app-store complaints double (illustrative). Anyone may stop. Flags owned, with an expiry date. One fixed window, for the core banking batch. **Self-check.**
- Is "stop" open to anyone, with the record afterwards?
- Did you keep compliance for the regulated class rather than every release?
- Are thresholds numbers on a screen, not "if it looks bad"?

</details>

**🔴 Design for a release you do not control.** For a vendor-run SaaS or a mobile app in your estate, write what the bank controls and what the supplier or app store controls, the contract terms or settings that would return the release decision to you, and how you would know which version users have.
*Done when:* you have a two-column table (we control / they control), at least three contract or configuration asks, and a way to see the version in use.

<details><summary>Model answer and self-check</summary>

**Model answer.** Card dispute SaaS: the supplier controls deployment timing and version; the bank controls enabled capabilities, roles and configuration. Asks for Lina: 30 days' notice of visible changes (illustrative), new capabilities delivered off, a test tenant that gets releases first, a right to defer non-security changes. Version: read from the admin console after each update. **Self-check.**
- Did you separate what you decide from what you can only request?
- Are the asks specific enough for Lina to negotiate?
- Did you plan to see the version in use, not just the version published?

</details>

## ⚠️ Mistakes and traps
- **Letting the launch date set the deployment date.** It forces big batches. Deploy early with the capability off; release on the date.
- **Asking permission to stop.** Damage grows while people look for an approver. Give everyone stop rights.
- **Flags without owners or expiry.** They pile up. Keep a register and review it monthly.
- **Assuming you control vendor releases.** You often control only enablement. Write what you need into the contract.

## 🧾 Recap
- **Deployment** puts software into production; **release** gives a capability to users. Deploy when ready; release when the business is ready.
- The team deploys within the change policy; the product manager releases with the business; **anyone may stop**.
- **Release classes** match sign-offs to risk, adding compliance where terms, fees or disclosures change.
- Write a **rollout rule** with steps, signals and stop thresholds; treat **rollback as normal**.
- Keep a **flag register** with owner, class and expiry; a flag change is a recorded change.

## ✍️ Check yourself
**1. Reem's instalment feature is finished six weeks before the marketing campaign. Under a policy that separates deployment from release, what should happen?**

- A. Deploy it to pre-production now and keep it there until campaign week, then promote it.
- B. Deploy it soon with the flag off, prove it, and release it when the campaign starts.
- C. Release it to all customers now, and ask marketing to bring the campaign date forward.
- D. Deploy it in the next monthly window with the other teams, so that operations can watch it.

<details><summary>Answer</summary>

**B.** Deploying early with the capability hidden keeps batches small and proves the software; the release waits for the business. A and D keep the two decisions glued together (A also leaves the code unproven in production), and C lets deployment drive the launch. See "How they are separated".

</details>

**2. During a progressive rollout of a new card control, an operations analyst sees authorisation errors cross the agreed threshold at 2 a.m. Reem is asleep. What does a good release policy say?**

- A. Call Reem first, since a release decision belongs to the product manager, then act on it.
- B. Hold the rollout at its current step without rolling back, and let the team decide in the morning.
- C. Ask the change board for an emergency approval before taking any action on the rollout.
- D. Pause or roll back now, inform Reem straight away, and record the trigger that fired.

<details><summary>Answer</summary>

**D.** Stopping is always allowed on agreed signs; the record follows. A and C add delay while customers suffer, and B leaves the customers already on the new control exposed after the threshold fired. See "Who decides each".

</details>

**3. Najm Bank must change card fees for all customers on a fixed date, after compliance approval. Which approach fits the lesson?**

- A. Deploy the fee logic early with its flag off; release it on the date after compliance signs.
- B. Deploy and release on the date in one step, since a fixed date means they cannot be separated.
- C. Release the new fees to 5% of customers first, as with any customer-affecting rollout.
- D. Let the product team set the date, because releases belong to the people who built the change.

<details><summary>Answer</summary>

**A.** The regulated release is fixed in time, but the deployment can come earlier and be proven first. B misses that, C leaves customers on different fees, and D hands a compliance decision to the team. See "Release classes".

</details>

**4. After three months the Cards & Payments team has 47 feature flags, nine for features long since released. What is the main operating-model problem?**

- A. The flag tool shows no usage data, so the team should buy one that reports unused flags.
- B. The engineers should clean up flags once a year, as part of the annual technical debt sprint.
- C. Nobody was accountable for retiring each flag by a set date, so stale switches stayed live.
- D. Flags should be replaced by separate deployments for each feature, so nothing stays hidden.

<details><summary>Answer</summary>

**C.** Without an owner and expiry, flags accumulate and can be reused by mistake. A changes the tool, not the ownership; B leaves stale flags live for up to a year; D gives up separating deployment from release. See "Feature flags are a managed inventory".

</details>

**5. Najm Bank uses a vendor-run SaaS for card disputes. The supplier deploys updates on its own schedule. What can the bank most usefully control?**

- A. The supplier's deployment dates, by asking it to follow the bank's monthly release window.
- B. Which new capabilities are switched on, plus contract terms for notice and a test tenant.
- C. Its own regression tests, run after each update has reached the production tenant.
- D. The supplier's source code, by requiring every change to pass the bank's own pipeline.

<details><summary>Answer</summary>

**B.** The bank usually controls enablement and configuration, and can negotiate notice and a test tenant. A and D ask for control the model does not give; C is useful but finds problems only after customers may have met them. See "Where you do not control deployment".

</details>

## 📚 References
- Hilton, A., "How release canaries can save your bacon—CRE life lessons", Google Cloud blog, 31 March 2017 (opened 2026-11-20): https://cloud.google.com/blog/products/gcp/how-release-canaries-can-save-your-bacon-cre-life-lessons — first canary step "between 1% and 10%", at least 24 hours between stages, automated canary analysis.
- Hilton, A., "Reliable releases and rollbacks—CRE life lessons", Google Cloud blog, 24 March 2017 (opened 2026-11-20): https://cloud.google.com/blog/products/gcp/reliable-releases-and-rollbacks-cre-life-lessons/ — "rollbacks are normal"; roll back first, investigate second.
- Hodgson, P., "Feature Toggles (aka Feature Flags)", martinfowler.com (four toggle categories as reported): https://martinfowler.com/articles/feature-toggles.html
- Google Cloud blog, "Using the Four Keys to measure your DevOps performance" (opened 2026-11-20): https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance — deployment frequency: "How often an organization successfully releases to production"; change failure rate: "The percentage of deployments causing a failure in production".
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 4.2 — Release strategies: rolling, blue-green, canary, feature flags and rollback](../cloud/index.html#/4.2).
- Library course: [*SaaS Building Blocks*, lesson 6.3 — Feature flags and experiments](../saas/index.html#/6.3).
- Library course: [*System Design for Vibe Coders*, lesson 4.4 — Rollback, staging, and release gates](../vibe/index.en.html#l4-4).
- Library course: [*Software Testing: Zero to Hero in the AI Era*, lesson 5.2 — Testing in CI/CD and in production: fast pipelines, flaky-test policy, feature flags, canaries and synthetic monitoring](../testing/index.html#/5.2).

---

# 6.2 — Change control that protects stability without stopping flow
*Level: 🟡 Intermediate* · *Prerequisites: 6.1, 2.2* · *Step: Release*

**After this you can** design a change model for one product area with four approval routes, the risk questions that place a change on a route, the evidence and approver for each, and five measures that show whether the model protects stability without slowing flow. *Study time: reading about 20 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- A **change** is anything added, modified or removed that could affect a live service: code, configuration, infrastructure, a feature flag, a supplier's update. **Change control** decides which changes go ahead, on what evidence, and keeps a record.
- Spend human attention where risk is. Most changes are routine and can be **pre-approved by kind**; a few deserve a real decision by people who understand them.
- *Accelerate* (2018, using 2014–2017 survey data from DORA, the DevOps Research and Assessment programme in lesson 1.3) is reported to have found external approval linked to slower delivery and not to fewer failed changes; DORA's guidance favours peer review plus automated checks.
- The rule that matters most: **approve the kind, not every instance, and let evidence do the approving.**
- Decision cue: if your change board approves almost everything it sees and still misses the changes that cause outages, it is reading descriptions, not judging risk.
- Biggest trap: answering an outage with another approval layer. It brings delay and bigger batches, themselves a risk.

## 🧭 Why it matters
Najm Bank and its people are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

Every Thursday Najm Bank's change advisory board, chaired by Yousef, spent ninety minutes on about forty change requests, mostly routine, and approved almost all. Changes waited about eight days, so teams bundled them, and emergency changes, the only fast route, had grown to a fifth of the total.

Then a firewall rule change, approved on a two-line description, cut the link between the mobile app and the card authorisation service for forty minutes on a Saturday. Nobody on the board had known the rule was shared. Omar asked: "What did the board actually check?" and "How do we make changes safer without making them slower?". Nour added audit's question: how will the bank show who approved each change, and that its author did not approve it alone? This lesson answers all three.

## 📐 How it works

### 🟢 The essentials

**Terms.** A **change authority** is the person or group allowed to approve a kind of change. A **change advisory board** (CAB) is a meeting that advises on or approves changes. **Segregation of duties** means no single person can both make and approve a change. **Blast radius** is how much of the business a failed change could affect.

**Four approval routes.** This course sorts changes onto four routes by who must approve them. (Standard, normal and emergency are common service-management labels, used for example in ITIL® (PeopleCert); the routes and questions here are this course's own, and lesson 12.1 compares frameworks.)

| Route | What travels on it | Who approves | Evidence |
|---|---|---|---|
| **Pre-approved (standard)** | A repeatable, low-risk change with a proven procedure, approved once as a kind (certificate renewal, a flag change that follows its rollout rule) | Nobody per instance | Automated record of each use; the kind is reviewed if one fails |
| **Peer-reviewed (low risk)** | A change to one product, reversible, with no regulated impact | A peer reviewer on the team, recorded in the delivery platform | Pipeline record: review, tests, scans, deployment |
| **Authority-decided (high risk)** | Wide blast radius, hard to reverse, new to the bank, or with customer-money, data or regulatory impact | A named change authority with the right knowledge (operations for shared network; compliance too for regulated releases) | Pipeline record plus a short risk note, rollback plan and timing |
| **Emergency** | A change needed now to restore service or close an exploited weakness | The on-duty incident lead, with a second person | Recorded at the time; reviewed within a set number of working days |

Aim to move most changes onto the first two routes, where the pipeline produces the evidence, so human judgement goes to the third.

**Segregation of duties without a board.** Peer review recorded in the delivery platform, which stops authors approving their own change, is a form of segregation of duties. Deployment by the pipeline, not personal production access, adds another. An auditor can test these by sampling records, often stronger evidence than meeting minutes. Agree the design with risk and internal audit before switching (lessons 5.1 and 10.3).

### 🟡 Going deeper

**What the research says.** Nicole Forsgren's announcement of the 2019 Accelerate State of DevOps report on the Google Cloud blog said that "heavyweight change processes don't work". Explaining why, in the 2019 data, organisations with more than 5,000 employees were lower performers, it named heavyweight process and controls among the reasons for "slower speed and the associated instability". The same post lists "clear change management" among capabilities that can positively affect software delivery performance: clear and light, not absent.

DORA's capability guide on streamlining change approval is reported to recommend peer review backed by automated checks, and to name reliance on a central change approval board as a pitfall. *Accelerate* (Forsgren, Humble and Kim, 2018) is reported to have found, from 2014–2017 survey data, that approval by an external body was associated with slower lead times, lower deployment frequency and slower restoration, and not with lower change failure rates. These are survey findings, not a law, and they do not say "remove all approval".

Yet change is where risk lives: the Google SRE book's introduction is reported to state that roughly 70% of outages are due to changes in a live system. So put the control where it works: small, reviewed, tested, reversible changes, with people judging the few risky ones.

**Placing a change on a route.** Five questions decide the route. Write them into the change tool so that the answers, not the author's optimism, set it:

1. **Blast radius**: one product, or shared components and many products?
2. **Reversibility**: can it be rolled back in minutes, or not at all (data migrations, customer messages)?
3. **Novelty**: has this kind of change been done safely here before?
4. **Impact class**: does it touch customer money, personal data, regulated reporting or customer terms?
5. **Evidence quality**: did the pipeline produce a complete record (review, tests, scans)?

Any "shared", "irreversible", "new" or regulated answer sends the change to the high-risk route; missing evidence sends it back to the team.

**How release decisions fit (lesson 6.1).** A flag change is a change, so the two policies must agree. A customer-affecting flag change that follows an approved rollout rule card answered the five questions when the card was approved; it is pre-approved, with the product manager as its change authority. A regulated-class flag change (fees, terms, disclosures) takes the high-risk route, with compliance as an approver. A flag change outside its card is judged afresh.

**Freezes and calendars.** A **change freeze** stops changes for a period, such as month end. It feels safe but pushes changes into bigger batches afterwards. Prefer a narrower rule: in busy periods close the high-risk route except for emergencies. Keep a **change calendar** so teams see busy periods and each other's high-risk changes.

**What the board becomes.** The CAB can become a weekly forum that reviews the few high-risk changes, spots collisions between teams, and reviews failures to withdraw or approve pre-approved kinds.

### 🔴 Expert view

**Configuration and supplier changes are changes.** Many change models miss configuration, flags, infrastructure settings and supplier updates. The July 2024 outage caused by a faulty CrowdStrike content update for Windows hosts is a widely reported example: CrowdStrike's preliminary post-incident review, as reported, described a content configuration update (Channel File 291) and committed to staggered deployment starting with a canary, and to giving customers more control over when such content is delivered; its Root Cause Analysis followed on 6 August 2024. For every supplier that can change software in your estate, ask how updates are staged, whether a test ring can get them first, and who is told; Lina writes the answers into contracts (lesson 10.2).

**Measure the change model.** Five measures show whether it works. Change fail rate is DORA's: "the percentage of deployments causing a failure in production" (lesson 1.3).

| Measure | What it shows | Warning sign |
|---|---|---|
| Approval wait (raised to approved), by route | Whether the route is fast where it should be | Low-risk changes waiting days |
| Share of changes pre-approved or peer-reviewed | Whether routine work has left the board | Falling, or flat for a year |
| Change fail rate by route | Whether routes are set correctly | A pre-approved kind that fails often should be withdrawn |
| Share of emergency changes | Whether people use emergency as a fast lane | Rising while incidents are flat |
| Unrecorded changes found | Whether the model covers reality | Deployments with no change record (lesson 6.3) |

**Regulation.** What Najm Bank's supervisor expects of change management is a question for Nour's team. Do not confuse DORA the research programme with the EU's Digital Operational Resilience Act, which shares the acronym.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Change model** | One page: the four routes, who approves each, evidence required, and the five risk questions | When redesigning change control; reviewed twice a year with risk |
| **Standard change catalogue** | The list of pre-approved kinds of change, each with its procedure, owner and failure history | Grow it monthly from the most frequent low-risk changes |
| **Risk questions in the change tool** | The five questions as required fields that route the change automatically | When configuring the change tool |
| **Change calendar** | Busy periods, freezes and scheduled high-risk changes | Weekly, by teams and operations |
| **Change measures sheet** | The five measures above with owners and warning signs | Monthly operations and risk review |
| **Service management platform** | Holds change records and links them to deployments and incidents (for example ServiceNow; an example, not an endorsement) | Integrate it with the pipeline rather than re-typing records |

## 🏛️ In practice at Najm Bank
Illustrative and fictional. Yousef and Nour drafted the change model, and Sami and Reem tested it on a month of changes.

> **Change model — Technology division v1**
> **Risk questions (required fields):** blast radius (one product or shared); reversible in minutes (yes/no); done safely here before (yes/no); impact class (customer money, personal data, regulated reporting, customer terms, none); evidence complete (yes/no).
> **Pre-approved (standard):** 18 kinds at launch, including certificate renewal, scaling within agreed limits, and flag changes that follow an approved rollout rule card (lesson 6.1; the product manager is change authority). Each kind has an owner; any failure triggers a review.
> **Peer-reviewed (low risk):** peer review in the delivery platform (author cannot approve), full pipeline record. No board.
> **Authority-decided (high risk):** shared network, core banking interfaces, data migrations, regulated releases including regulated flag changes (compliance approves). Decided by the named change authority for that area; reviewed at the Thursday forum if it affects more than one product.
> **Emergency:** incident lead plus a second person; reviewed by the forum within two working days.
> **Freeze:** month-end close and the two days of salary payment, high-risk route only by exception.
> **Measures:** approval wait by route; share pre-approved or peer-reviewed; change fail rate by route; emergency share; unrecorded changes found.

The Saturday firewall change would now be high risk, because the rule was shared. In month one the wait for low-risk changes fell from eight days to under one, and emergency changes from a fifth to a twentieth of the total (illustrative). Audit asked for one addition: a monthly sample of twenty low-risk changes checked for recorded peer review.

One mistake: the first catalogue pre-approved "database index change". One such change locked a payments table for twelve minutes, and the forum withdrew the kind until a safer procedure was proven.

## 🛠️ Exercises
**🟢 Sort a month of changes.** Take twenty recent changes (or invent twenty for Najm Bank). Place each on one of the four routes using the five risk questions.
*Done when:* every change has a route and the answers to the five questions, and you can say what share would no longer need a board.

<details><summary>Model answer and self-check</summary>

**Model answer.** Two worked rows: *shared firewall rule*: blast radius shared; reversible yes; done before yes; impact none; evidence partial → high risk, and back for evidence. *Wording change on a card screen*: one product; reversible yes; done before yes; impact none; evidence complete → peer-reviewed. Across the month: about a third pre-approved, half peer-reviewed, the rest high risk plus one emergency patch (illustrative). **Self-check.**
- Did every shared, irreversible, new or regulated change go to the high-risk route?
- Did you count configuration and flag changes, not only code?

</details>

**🟡 Write a change model.** Using the toolkit, write a one-page change model for one area: the four routes with approver and evidence, the five risk questions, freeze rules, and the board's new role.
*Done when:* each route names a role that approves it (or "none per instance"), each evidence item can be pulled from a record, and the freeze rule is narrower than "no changes".

<details><summary>Model answer and self-check</summary>

**Model answer.** For internet banking: the five risk questions as required fields (as in Najm Bank's model); pre-approved kinds with owners; recorded peer review for low risk; named authorities for high risk (operations for shared network, compliance for regulated releases); incident lead plus a second person for emergencies, reviewed within two working days; at month end only the high-risk route closes; the board reviews high-risk changes and failures weekly. **Self-check.**
- Does the author ever approve their own change? It should be impossible.
- Did you plan how a pre-approved kind is withdrawn after a failure?

</details>

**🔴 Set measures and test with audit's eyes.** Write the five measures with an owner and a warning sign each. Then write five questions an auditor would ask, and the record that answers each.
*Done when:* every measure has a data source, and every audit question is answered by a record that exists or a note of what must be built.

<details><summary>Model answer and self-check</summary>

**Model answer.** Measures, owner and source: approval wait by route (Yousef; change tool timestamps); share pre-approved or peer-reviewed (Yousef; change tool route field); change fail rate by route (Nour; deployment records joined to incident records); emergency share (Yousef; change tool); unrecorded changes found (Sami; deployment and configuration events reconciled with change records). Audit questions and records: who approved (platform review record); could the author self-approve (platform setting and a sample); was it tested (pipeline record); how are pre-approved kinds approved and withdrawn (catalogue history); are all changes recorded (deployments and configuration changes reconciled with change records). **Self-check.**
- Is every measure computed from records, not surveys?
- Could an auditor sample, not interview?
- Did you avoid claiming the design satisfies the regulator without asking?

</details>

## ⚠️ Mistakes and traps
- **One route for every change.** Routine changes queue behind risky ones. Pre-approve the routine.
- **Adding approvals after an outage.** More sign-offs mean bigger, slower batches. Fix the route, the evidence or the test that failed.
- **Trusting the author's risk rating.** Free-text "low risk" is optimism. Use the five questions as required fields.
- **Freezing everything.** It moves risk to the days after. Close only the high-risk route.
- **Covering code only.** Configuration, flags and supplier updates break services too. Bring them in.
- **Assuming audit agrees.** Confirm the design with risk and audit first.

## 🧾 Recap
- A **change** is anything that could affect a live service, including flags and supplier updates.
- Use **four routes**: pre-approved, peer-reviewed (with pipeline evidence), authority-decided (high risk), emergency.
- *Accelerate* (2018) reportedly linked **external approval** with slower delivery, not fewer failed changes; DORA favours **peer review plus automated checks**.
- Five **risk questions** set the route: blast radius, reversibility, novelty, impact class, evidence quality.
- **Measure** wait by route, share routine, fail rate by route, emergency share and unrecorded changes.

## ✍️ Check yourself
**1. Najm Bank's change board approves almost every request it reviews, yet a firewall change it approved caused an outage. What does this most likely show?**

- A. The board needs more time per change, so it should meet twice a week instead of once.
- B. The review judged a two-line description; nothing made it ask whether the rule was shared.
- C. The board lacked a network specialist, so one should join to review every network change.
- D. Changes need a fuller written risk assessment from their authors before the board sees them.

<details><summary>Answer</summary>

**B.** Approving nearly everything while missing the dangerous change shows the review rested on descriptions, not on questions such as blast radius. A adds time, not judgement. C keeps every network change at the board instead of routing shared ones to a named authority. D relies on the author's own rating. See "Why it matters" and "Placing a change on a route".

</details>

**2. Reem's team wants to change the wording on a card-control screen. The change touches one product, is reversible in minutes and has full pipeline evidence. Which route fits?**

- A. Peer-reviewed: a recorded peer review and the pipeline record are enough.
- B. Authority-decided: any change customers can see goes to a named change authority.
- C. Board pre-review: add a CAB look at customer-visible changes, then peer review.
- D. Emergency: the change is small, so the fastest available route is the right one.

<details><summary>Answer</summary>

**A.** Single product, reversible and well evidenced: the low-risk route. B and C confuse visibility with risk and bring routine work back to an approver who adds little; D misuses emergency as a fast lane. See "Four approval routes".

</details>

**3. Internal audit asks how Najm Bank can show segregation of duties without the weekly board. Which answer fits?**

- A. Restrict production access to operations staff, who deploy every change on the teams' behalf.
- B. Have each team lead sign a monthly attestation that every change was reviewed by someone else.
- C. Keep the board for approval but let it sign off changes in batches by email between meetings.
- D. Record peer review in the platform, block self-approval, and agree the design with audit first.

<details><summary>Answer</summary>

**D.** Recorded peer review with self-approval blocked gives sampled evidence of two people per change, agreed with audit first. A adds a hand-off queue and a deployer who did not review the code. B is an attestation, not per-change evidence, and C keeps the board's weak review. See "Segregation of duties without a board".

</details>

**4. After a bad month, Omar proposes freezing all changes for the last week of every month. What does the lesson suggest instead?**

- A. Freeze the last week but let teams apply for exceptions through the weekly board.
- B. Move all changes to weekends during that week, when customer traffic is lower.
- C. Close only the high-risk route in busy periods, except for emergencies.
- D. Freeze the whole week but double the pipeline tests on changes made just before it.

<details><summary>Answer</summary>

**C.** Broad freezes push changes into bigger batches afterwards; a narrow rule keeps low-risk work moving. A keeps the broad freeze and sends routine work back to the board, B changes timing without judging risk, and D still bunches changes before and after. See "Freezes and calendars".

</details>

**5. Najm Bank's change model covers its own teams' code. A security supplier can push content updates to every bank laptop. What should Yousef and Lina do?**

- A. Add the supplier's maintenance window to the bank's change calendar so updates are visible.
- B. Bring supplier updates into the model: ask how they are staged, and get a test ring first.
- C. Require each supplier update to go to the weekly board before it reaches any laptop.
- D. Accept the supplier's assurance of testing, recorded as a clause in the contract.

<details><summary>Answer</summary>

**B.** Supplier changes inside the estate are changes; know how they are staged and get a test ring first where possible. A shows when updates arrive, not how they are staged. C could hold up urgent security content, and D relies on a promise rather than staging the bank can see. See "Configuration and supplier changes are changes".

</details>

## 📚 References
- Forsgren, N., "The 2019 Accelerate State of DevOps: Elite performance, productivity, and scaling", Google Cloud blog, 22 August 2019 (opened 2026-11-20): https://cloud.google.com/blog/products/devops-sre/the-2019-accelerate-state-of-devops-elite-performance-productivity-and-scaling — "heavyweight change processes don't work"; enterprise organisations (more than 5,000 employees) lower performers, with heavyweight process and controls among the reasons for "slower speed and the associated instability"; "clear change management" among positive capabilities.
- Google Cloud blog, "Using the Four Keys to measure your DevOps performance" (opened 2026-11-20): https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance — change failure rate: "The percentage of deployments causing a failure in production".
- DORA, "Streamlining change approval", capability guide (as reported): https://dora.dev/capabilities/streamlining-change-approval/
- Forsgren, N., Humble, J. and Kim, G., *Accelerate: The Science of Lean Software and DevOps* (IT Revolution, 2018). External-approval findings as reported.
- Beyer, B., Jones, C., Petoff, J. and Murphy, N. R. (eds.), *Site Reliability Engineering* (O'Reilly, 2016), Introduction (the "roughly 70% of outages" statement as reported): https://sre.google/sre-book/introduction/
- CrowdStrike, "Falcon Content Update Preliminary Post Incident Report" (as reported): https://www.crowdstrike.com/en-us/blog/falcon-content-update-preliminary-post-incident-report/
- CrowdStrike, "Executive Summary: Root Cause Analysis, Channel File 291", 6 August 2024 (as reported): https://crowdstrike.com/wp-content/uploads/2024/08/Executive-Summary_Root-Cause-Analysis_Channel-File-291.pdf
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 4.3 — Securing the pipeline: secrets, signed artefacts and least-privilege deploys](../cloud/index.html#/4.3).

---

# 6.3 — Environments, configuration and the record of what is running
*Level: 🟡 Intermediate* · *Prerequisites: 6.1, 5.1* · *Step: Release*

**After this you can** draw an environment map for one product (each environment's purpose, owner, data, who may change it and how close it is to production), specify a "what is running" record that is produced automatically from deployments, and set a drift check with an owner. *Study time: reading about 20 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- An **environment** is a place where software runs for a purpose: development, testing, pre-production, production. **Configuration** is the set of settings that change how the same software behaves in each place (addresses, limits, flags, credentials).
- Promote the **same artefact** from environment to environment; only configuration should differ, and configuration is versioned, reviewed and deployed like code.
- Keep a **record of what is running**: for each service in each environment, the artefact version, configuration version, flag state and the change that put it there, written by the pipeline at deployment.
- The rule that matters most: **if the record of what is running is typed by hand, it is already wrong.**
- Decision cue: if three people give three answers to "which version is in production?", you do not have a record, you have opinions.
- Biggest trap: **drift**, the slow gap between what you think is running and what is, grown from hand fixes and console changes.

## 🧭 Why it matters
Najm Bank and its people are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

An internal auditor asked Nour a simple question: "Which version of the card authorisation service is running in production, and since when?" Nour asked three people. The configuration management database (CMDB, the register of IT components and how they relate) said version 4.2. Sami's pipeline showed 4.6 deployed three weeks earlier. Yousef's team knew of a hotfix a supplier engineer had applied by hand to one of the four servers during an incident. All three were partly right, which meant the bank could not answer.

The same month, a change passed every test in pre-production and failed in production, because a timeout setting differed; someone had changed one by hand a year earlier. And Reem's team waited nine working days (illustrative) to book the shared test environment, so they tested less and later.

Omar's question to Huda, Head of Enterprise Architecture, was blunt: "Why don't we know what we are running?" This lesson answers it with three artefacts: an environment map, a configuration rule, and a record of what is running that nobody types.

## 📐 How it works

### 🟢 The essentials

**Environments and their jobs.** Most products need fewer environments than they have, each with a clear job:

| Environment | Job | Typical owner | Data |
|---|---|---|---|
| **Development** | Where engineers build and try changes | The product team | Synthetic or small fake data |
| **Integration or test** | Where automated tests run against other services | The product team, on a platform from Sami's team | Synthetic or masked data |
| **Pre-production** (also called staging) | A close copy of production for final checks, performance and rehearsal | Platform or operations, shared | Masked data; real customer data only with approval |
| **Production** | Where customers are served | Operations with the product team | Real data, fully controlled |
| **Ephemeral** | Short-lived copies created for one change or test, then destroyed | Created by the pipeline | Synthetic data |

Ephemeral environments remove the booking queue for many tests, often the cheapest way to cut a wait on the value-stream map (lesson 1.2).

**The environment map.** For one product, write one row per environment with: purpose, owner, data, who may change it and how, and **parity** (how closely it matches production in versions, configuration and capacity). "How" is normally the pipeline, plus **break-glass**: emergency access outside the pipeline, logged and reviewed afterwards. Parity matters because a test only proves something about the environment it ran in; where parity is deliberately low, write that down.

**Configuration separate from code.** The Twelve-Factor App, a widely used set of principles for building services, is reported to call for "strict separation of config from code", because configuration varies between deployments while code does not. Two rules follow:

- **The same artefact everywhere.** The artefact tested is the artefact deployed (lesson 5.1's "build once"). Only configuration differs between environments.
- **Configuration is a change.** It is stored in version control, reviewed, deployed through the pipeline and recorded, like code. Secrets (passwords, keys, certificates) are configuration too, but they live in a **secrets vault** and are never written into code or ordinary configuration files.

**The record of what is running.** For each service in each environment, the record holds: artefact version, configuration version, feature-flag state, infrastructure version, when it was deployed, by which pipeline run, and which change record authorised it. The pipeline writes it at every deployment. That record answers the auditor in seconds and feeds the CMDB, rather than relying on someone to update it (lesson 9.2).

### 🟡 Going deeper

**Desired state and actual state.** Modern practice describes what should be running (servers, network rules, versions, settings) in files kept in version control, and lets tools make reality match. This is **infrastructure as code**; when a tool continuously compares the files with what is running and applies the difference, it is often called **GitOps**. Engineering: [*Cloud & DevOps: Zero to Hero*, lesson 3.1 — Infrastructure as code with Terraform/OpenTofu: state, modules and plans](../cloud/index.html#/3.1) and [*Cloud & DevOps: Zero to Hero*, lesson 3.2 — Environments and GitOps: promoting changes from dev to production](../cloud/index.html#/3.2). The operating-model gain is that "what should be running" becomes a reviewable record, and "what is running" can be compared with it.

**Baselines.** A **baseline** is an agreed snapshot of a system's configuration that later changes are measured against. A NIST (US National Institute of Standards and Technology) glossary entry is reported to describe a baseline configuration as a documented set of specifications, formally reviewed and agreed at a point in time, which can be changed only through change control. In infrastructure as code, the reviewed files in version control are the baseline.

**Drift.** **Drift** is any difference between the baseline and what is actually running. It comes from hand fixes during incidents, settings changed in a console, a supplier engineer's patch, or a deployment that reached some servers but not others. Manage it like this:

| Step | What to decide | Najm Bank example |
|---|---|---|
| Detect | How often actual state is compared with desired state, and by what tool | Nightly comparison for production, weekly for pre-production |
| Alert | Who is told, and how fast | The product team's on-duty engineer, next working morning |
| Decide | Restore the baseline, or accept the change into it through change control | Hotfix accepted into code within two days, or removed |
| Measure | How much drift is found and how long it lives | Drift items open, median age, repeat sources |

Drift found is also a test of the change model: every drift item is a change that went around it (lesson 6.2's "unrecorded changes found").

**Test data.** Copying production data into test puts real customers' personal data where controls are weaker. Prefer synthetic or masked data; real data outside production is a decision for the bank's data protection officer.

**Environments cost money.** Give each an owner and a budget line, show its cost to the teams that use it (lesson 7.3), and switch off ephemeral ones automatically.

### 🔴 Expert view

**A public case: Knight Capital, 2012.** In October 2013 the US Securities and Exchange Commission (SEC) announced that Knight Capital Americas would pay $12 million to settle charges of violating the SEC's market access rule (Rule 15c3-5) after a trading incident on 1 August 2012, in which the firm reportedly lost more than $460 million. The SEC's order (Release No. 34-70694) is reported to say that new code was not copied to one of eight servers running an order router, and that a repurposed flag then activated old, unused code on that server.

Read it as an operating-model story, not one about a technician:

- **Deployment was not verified.** Nothing confirmed that every target received the new version. A record of what is running per server, checked after each deployment, would have shown seven matching and one not.
- **An old flag was reused, and old code was left in place.** Lesson 6.1's flag register and expiry rule exist for exactly this.

The engineering habit behind the first point is taught in [*System Design for Vibe Coders*, lesson 4.5 — Verify the artifact, not the source](../vibe/index.en.html#l4-5).

**Where the record lives.** Do not build a second CMDB. The pipeline writes the "what is running" events; the CMDB (Module 9) consumes them and links them to services, changes and incidents. Huda's records design (lesson 9.1) should name the pipeline as the **system of record** for deployed versions.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Environment map** | One row per environment: purpose, owner, data, who may change it, parity with production, cost | When a product is set up or audited; reviewed yearly |
| **Configuration rule** | One page: same artefact everywhere; configuration in version control, reviewed and deployed; secrets in a vault | Agreed once across the division; checked in pipeline reviews |
| **What-is-running record** | Per service and environment: artefact, configuration, flags, infrastructure version, when, pipeline run, change reference | Specified with Sami and Huda; written by the pipeline |
| **Drift check** | Scheduled comparison of desired and actual state, with an owner and a decision rule | For production first, then pre-production |
| **Infrastructure-as-code tool** | Describes environments in files and applies them (examples include Terraform and OpenTofu) | When environments are still built by hand; examples, not endorsements |
| **Secrets vault** | Stores and rotates passwords, keys and certificates, and records who used them | Before any secret is found in code or a shared document |

## 🏛️ In practice at Najm Bank
Illustrative and fictional. Huda and Sami wrote the environment map for the card authorisation service, and Nour reviewed it.

**Environment map — card authorisation service v1**

| Environment | Owner | Data | Changed by | Parity |
|---|---|---|---|---|
| Ephemeral test | Pipeline | Synthetic | Pipeline only | Same versions, small capacity |
| Integration | Cards & Payments team | Synthetic | Pipeline only | Same versions and configuration keys |
| Pre-production | Platform team | Masked, approved by the data protection officer | Pipeline; break-glass logged | Same versions and configuration; half capacity (written down) |
| Production | Operations with the team | Real | Pipeline; break-glass logged | Not applicable |

> **What-is-running record:** written by the pipeline at every deployment, per server; checked after deployment that every server reports the new version. Fed to the CMDB nightly.
> **Drift:** nightly for production; findings to the team's on-duty engineer; restore or accept through change within two working days.

The first nightly drift check found eleven differences in production (illustrative), including the supplier's hand-applied hotfix and the timeout that had caused the pre-production pass and production failure. Lina added a clause to the supplier's contract: no changes by hand without a change record, and every emergency fix brought back into the supplier's release within a set period. Reem's team stopped booking the shared environment for most tests once ephemeral environments arrived; the nine-day wait disappeared from their value-stream map.

The mistake: the first version recorded versions per service, not per server, and so would not have caught a deployment that missed one server. Nour spotted it after reading about the Knight Capital case; the record changed to per-server.

## 🛠️ Exercises
**🟢 Ask the three-answer question.** For one important service, ask three sources (the CMDB, the pipeline or deployment tool, and the operations team) which version is running in production and since when. Write down the answers and the differences.
*Done when:* you have three answers with their source and date, and a sentence explaining any difference.

<details><summary>Model answer and self-check</summary>

**Model answer.** For Najm Bank's card authorisation service: CMDB 4.2 (last updated by hand eight months ago); pipeline 4.6 deployed three weeks ago; operations: 4.6 on three servers, 4.6 plus a supplier hotfix on the fourth. Explanation: the CMDB is updated by hand and is stale; the pipeline does not see hand-applied fixes. **Self-check.**
- Did you ask at the level of each server or instance, not only the service?
- Did you note how each source gets its data (typed or automatic)?
- Did you find any change that no record shows?

</details>

**🟡 Draw the environment map.** For one product, write the environment map: one row per environment with purpose, owner, data, who may change it and parity with production. Mark any environment you could replace with ephemeral ones.
*Done when:* every environment has an owner and a data rule, parity gaps are written down, and you have named at least one wait the map would remove.

<details><summary>Model answer and self-check</summary>

**Model answer.** See the Najm Bank map above: one owner per environment, synthetic or masked data outside production, changes only through the pipeline (break-glass logged), parity gaps stated ("half capacity: not valid for performance sign-off"), and ephemeral environments instead of shared booking where possible. **Self-check.**
- Did you name a person or team, not "IT", as owner?
- Did you decide the data rule with the data protection function?
- Did you write parity gaps down rather than hide them?

</details>

**🔴 Specify the record and the drift check.** Write the fields of a "what is running" record for one service, where each field comes from, how deployment completeness is verified, and a drift check with frequency, owner and decision rule. Add one paragraph on how the record feeds the CMDB.
*Done when:* every field has an automatic source, the record works per server or instance, and the drift rule says who decides between restoring and accepting.

<details><summary>Model answer and self-check</summary>

**Model answer.** Fields: service, environment, server or instance, artefact version and digest (a fingerprint that proves the exact build; from the pipeline), configuration version (from the configuration repository), flag state (from the flag service), infrastructure version (from infrastructure as code), deployed at, pipeline run, change reference. Completeness: after deployment, each instance reports its version and the pipeline fails the deployment if any differ. Drift: nightly for production, owner the product's on-duty engineer, restore or accept through change within two working days, monthly drift report to Yousef. CMDB: consumes deployment events nightly and links them to the service, change and incident records; nobody edits versions by hand. **Self-check.**
- Is any field typed by a person? It should not be.
- Would your record catch one server out of eight on the old version?
- Does every drift item end in a decision and a record?
- Did you name the pipeline as system of record for deployed versions?

</details>

## ⚠️ Mistakes and traps
- **Rebuilding for each environment.** Then tests prove nothing about production. Promote one artefact; vary only configuration.
- **Configuration changed by hand.** It creates silent differences between environments. Version, review and deploy configuration like code.
- **A CMDB typed by people.** It goes stale within weeks. Feed it from deployment events.
- **Recording per service, not per server.** A partial deployment hides inside "version 4.6". Record and verify every instance.
- **Real customer data in test.** It moves personal data to weaker controls. Use synthetic or masked data; ask the data protection function.
- **Ignoring drift.** Every drift item is an unrecorded change. Detect it, decide on it, and measure it.

## 🧾 Recap
- Give every **environment** a job, an owner, a data rule and a stated parity with production; use **ephemeral** environments to remove booking waits.
- Promote the **same artefact**; only **configuration** differs, and it is versioned, reviewed and deployed like code, with secrets in a vault.
- Keep a **what-is-running record** per service, environment and instance, written by the pipeline and verified after each deployment.
- Detect and decide on **drift** against an agreed **baseline**; drift is an unrecorded change.
- The pipeline is the **system of record** for deployed versions; the CMDB joins them to everything else.

## ✍️ Check yourself
**1. An auditor asks which version of the card authorisation service runs in production. The CMDB, the pipeline and operations give three different answers. What is the root problem?**

- A. Make the CMDB the system of record, with a post-deployment checklist owned by operations.
- B. The supplier's hand-applied hotfix broke the rules, so the contract needs a clause banning hand changes.
- C. The pipeline cannot see hand fixes, so a quarterly manual audit of every server should be the reference.
- D. Nothing writes a per-server record at deployment and checks it later, so sources drift apart.

<details><summary>Answer</summary>

**D.** The record should be written by the deployment itself, per instance, checked for drift, and fed to the CMDB. A keeps people typing the record, so it still goes stale. B is a useful clause (Najm Bank added one) but fixes one source of drift, not the missing record. C gives a snapshot that is out of date the day after. See "The record of what is running".

</details>

**2. A change passed every test in pre-production and failed in production because a timeout setting differed. What rule would most likely have prevented it?**

- A. Run every test twice in pre-production, so that rare failures have more chances to show.
- B. Version configuration, deploy and record it like code, and check environment parity.
- C. Ask the change board to review every configuration file before each production deployment.
- D. Copy all production data into pre-production, so tests run against real customer records.

<details><summary>Answer</summary>

**B.** The difference came from an unrecorded hand change; versioned configuration and a drift check would have exposed it. A repeats tests in the wrong setting, C adds approval without fixing the source, and D creates a data protection problem. See "Configuration separate from code" and "Drift".

</details>

**3. Reem's team waits nine working days to book the shared test environment. Which change best fits the lesson?**

- A. Add a second shared test environment and assign a coordinator to manage both booking queues.
- B. Ask teams to plan their testing further ahead, so bookings are made weeks before they are needed.
- C. Use ephemeral environments created by the pipeline for most tests, and destroyed after use.
- D. Give each team a fixed weekly slot in the shared environment, published on the change calendar.

<details><summary>Answer</summary>

**C.** On-demand, short-lived environments remove the queue for most tests and are switched off automatically. A, B and D manage the queue rather than removing it. See "Environments and their jobs".

</details>

**4. The nightly drift check finds that a supplier engineer applied a hotfix by hand to one production server. What should happen next?**

- A. Keep it, since it fixed an incident, and ask the supplier to include it in its next release.
- B. Roll it back at the next maintenance window, because hand changes are against the policy.
- C. Update the CMDB by hand to show the hotfix, so the register matches what is running.
- D. Decide through change control to restore the baseline or accept the fix into the code.

<details><summary>Answer</summary>

**D.** Drift needs a decision and a record: either restore the agreed baseline or bring the change into it properly. A leaves an unrecorded difference until some later release, B may reopen the incident without anyone deciding, and C records the drift by hand without resolving it. See "Drift".

</details>

**5. Huda is designing where the "what is running" record lives. Which design fits the lesson?**

- A. The pipeline writes deployment events per instance, and the CMDB consumes and links them.
- B. A new, separate register is built for deployed versions, kept apart from the existing CMDB.
- C. The CMDB is the system of record, and operations reconcile it with the pipeline each week.
- D. Each product team keeps its own spreadsheet of deployed versions and shares it on request.

<details><summary>Answer</summary>

**A.** The pipeline is the system of record for deployed versions; the CMDB joins them to services, changes and incidents. B duplicates registers, C makes a weekly hand reconciliation the source of truth, and D depends on people typing records. See "Where the record lives".

</details>

## 📚 References
- US Securities and Exchange Commission, press release 2013-222, Knight Capital Americas settlement (as reported): https://www.sec.gov/news/press-release/2013-222 — and the order, SEC Release No. 34-70694, 16 October 2013, Administrative Proceeding File No. 3-15570 (as reported).
- The Twelve-Factor App, "III. Config" (as reported): https://12factor.net/config
- NIST Computer Security Resource Center glossary, "baseline configuration" (as reported): https://csrc.nist.gov/glossary/term/baseline_configuration
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 3.1 — Infrastructure as code with Terraform/OpenTofu: state, modules and plans](../cloud/index.html#/3.1).
- Library course: [*Cloud & DevOps: Zero to Hero*, lesson 3.2 — Environments and GitOps: promoting changes from dev to production](../cloud/index.html#/3.2).
- Library course: [*System Design for Vibe Coders*, lesson 4.5 — Verify the artifact, not the source](../vibe/index.en.html#l4-5).
