# Module 5 — Build and integrate

*Module 4 turned asks into backlog items with quality requirements and a runway. This module is about the stretch between "a team starts building" and "a tested, trusted piece of software is ready to release". At Najm Bank's Technology division that stretch is where much of the hidden cost sits: many home-grown pipelines, test results nobody outside the team can read, audit evidence assembled by hand the week before a review, and products that quietly depend on hundreds of open-source libraries and outside services nobody has listed. This is not an engineering module; the engineering is taught elsewhere in the library, and each lesson links to it. Here you make the operating-model decisions: who owns the delivery pipeline and how it is run and funded as a product; which quality gates a change must pass, who sets them, and what evidence they leave that a manager, a risk officer or an auditor can trust; and how the bank knows, owns and manages every third-party, SaaS and open-source component inside its products. Each lesson leaves an artefact: a pipeline service card and scorecard, a gate card set with an evidence checklist, and a component policy with an inventory and a response playbook.*

> **Steps:** Build — run the path from code to tested, recorded, releasable software as a managed capability, with gates that produce trustworthy evidence and components that someone owns.

---

# 5.1 — Delivery pipelines as a managed capability
*Level: 🟡 Intermediate* · *Prerequisites: 2.2, 4.3* · *Step: Build*

**After this you can** write a service card for a shared delivery pipeline (owner, customers, standard steps, service levels, funding and the records it leaves), and a one-page pipeline scorecard with five measures, each paired with a measure that keeps it honest. *Study time: reading about 15 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- A **delivery pipeline** is the automated path that takes a change from version control to a tested, recorded artefact ready to deploy. It is a production system for the people who build software, and deserves an owner.
- Run the shared pipeline **as a product**: a named owner, known customers (the product teams), a standard path most teams use, published service levels, a roadmap and stable funding.
- Separate what is **standard and mandatory** (build once, test, scan, record, sign) from what each team **chooses** (languages, test tools, extra checks). Standardise the evidence, not the taste.
- The rule that matters most: **a pipeline nobody owns is a pipeline everybody works around.**
- Decision cue: if a broken build agent can stop a team for a day and nobody is paged, the pipeline is not yet managed.
- Biggest trap: measuring the platform team by how many teams it forced onto the platform, not by how much faster and safer they deliver.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

When Sami, Platform Engineering Lead, counted the ways code reached production at Najm Bank, he found fourteen: a hosted CI/CD system, an old build server whose author had left, and a script a senior developer ran from his laptop on release night, among others.

Then the old build server failed and Reem's Cards & Payments team could not build for three days while a card-declines fix waited. Internal audit told Nour, IT Risk and Controls Lead, that for sampled changes the bank could not show which tests had run against the deployed version. Tariq, IT Finance Business Partner, found four overlapping CI/CD licences. Omar, the Chief Information Officer, asked: "Who owns the way we build software?" Nobody answered. This lesson turns a collection of scripts into a capability with an owner, a standard, a budget and a record.

## 📐 How it works

### 🟢 The essentials

**What a pipeline is.** A **delivery pipeline** (often called a CI/CD pipeline) is a sequence of automated steps that runs whenever a developer submits a change to **version control** (the system that stores every version of the code and who changed it). It builds the software, runs tests and security checks, packages an **artefact** (the deployable package, such as a container image) with a unique version, and records what happened. **Continuous integration** (CI) means merging everyone's changes into a shared main line often, each merge checked automatically. Deployment and release are Module 6.

**Why a manager should care.** The pipeline sits on the path of every change: when it is slow, every team is slow; when it records nothing, every audit is manual archaeology. Many controls (review, testing, scanning) run inside it, so its design is a risk question too.

**From many scripts to a managed capability.** Five questions a manager can check:

| Question | Weak answer (Najm Bank before) | Strong answer (managed capability) |
|---|---|---|
| **Who owns it?** | "Each team owns its own" | The platform team owns the shared pipeline; product teams own the steps they add |
| **What is standard?** | Fourteen variants | A standard path (a **golden path** or **paved road**) with documented mandatory steps |
| **How good is it?** | Nobody measures | Published service levels and a scorecard reviewed with customers |
| **Who pays?** | Project budgets and four licences | A stable product budget (lesson 3.2), usage shown back to teams (lesson 7.3) |
| **What does it leave behind?** | Logs that expire in a week | A run record per change (who, version, checks, results, artefact), kept as long as risk requires |

**The platform team and its customers.** The pipeline is the classic platform product (lesson 2.2); its customers are the product teams, and it succeeds when they choose it because it makes their work easier, a view popularised by the book *Team Topologies* (Skelton and Pais).

**Standard versus chosen steps.** A standard pipeline should be strict about a small number of things and relaxed about the rest:

| Mandatory for every production change (the platform provides it) | Chosen by the product team (the platform supports it) |
|---|---|
| Build from version control only, never from a laptop | Programming language and build tool |
| Build the artefact **once** and promote that same artefact through every environment | Unit and integration test frameworks |
| Peer review recorded before merge to the main line | Extra tests (performance, accessibility, contract) |
| Automated tests run, with results stored | Thresholds above the bank's minimum |
| Dependency and code security scans run, with results stored | Extra quality tools |
| Artefact stored with a unique version and its run record | Notification and dashboard preferences |

"Build once" matters: if the tested artefact is rebuilt for production, nobody can prove that what was tested is what runs. Lesson 6.3 returns to this; [*Cloud & DevOps: Zero to Hero*, lesson 4.1 — Continuous integration: pipelines, tests, artefacts and fast feedback](../cloud/index.html#/4.1) shows the engineering.

### 🟡 Going deeper

**Service levels for a pipeline.** A product's customers can expect stated service levels (lesson 8.3 goes deeper). Keep them few, visible and measured from the customer's side: **availability** (share of working hours in which teams can run the pipeline), **feedback time** (from submitting a change to knowing whether it passed, median and 90th percentile), **queue time** (how long a run waits for a free build agent, often worst at month end), **platform-caused failure rate** (failed runs caused by the pipeline, not the team's code; trust falls fast when "red" is the platform's fault) and **support response**. Sami's service card below shows illustrative targets.

**Pair every measure.** Lesson 1.3 showed that a single measure becomes a target and stops telling the truth. Pair fast feedback with escaped defects (problems found in production that the pipeline should have caught): deleting slow tests improves the first and worsens the second. Pair adoption (share of teams on the standard path) with developer satisfaction: forced adoption raises one and drops the other. Report the scorecard separately from DORA's delivery metrics (lesson 1.3): they describe the whole delivery system, and a great pipeline can coexist with changes waiting weeks for a change board (Module 6).

**What the research says about platforms.** Google's announcement of the 2024 DORA report (DORA is DevOps Research and Assessment, a research programme now part of Google Cloud) says internal developer platforms "effectively increase productivity", may bring a temporary performance drop before gains, and work best when user-centred and product-oriented. The 2025 announcement says 90% of organisations had adopted at least one platform and links platform quality to the ability to unlock the value of AI. These are survey findings for particular years. The reading for a manager: expect a dip, run the platform as a product, measure what it does for customers.

**Funding, mandate or attract?** A platform funded as projects decays between them, so fund it as a product (lesson 3.2) and show each team its share of the cost (lesson 7.3). Mandate outcomes: every production change goes through a pipeline that produces the required evidence. Attract teams to the standard path by making it the easiest way to meet them. A team may run its own pipeline if it meets the same evidence standard and pays for its upkeep; most stop wanting to once they see the cost.

### 🔴 Expert view

**The pipeline is a control, so control the pipeline.** Once review, testing and scanning happen inside the pipeline, its definition becomes a control the risk function relies on. Three consequences follow.

1. **Changes to the pipeline are changes.** The definition lives in version control, is reviewed by someone other than its author, and leaves a record. A developer who can quietly remove the security scan has defeated the control.
2. **Segregation of duties is enforced by the system.** Many banks expect that no one person can write a change and put it into production unreviewed. The pipeline can enforce and record this, which beats a signature on a form. Ask your risk function what policy requires.
3. **Break-glass is designed, not improvised.** **Break-glass** is a pre-agreed emergency bypass. Decide in advance who may bypass which step, which steps can never be bypassed, how each use is logged, and who reviews it within a set time.

**The pipeline has its own supply chain.** Build agents, plug-ins, base images and deployment credentials are attractive targets: compromise them and you compromise everything built through them. Apply lesson 5.3 to them; see [*Cloud & DevOps: Zero to Hero*, lesson 4.3 — Securing the pipeline: secrets, signed artefacts and least-privilege deploys](../cloud/index.html#/4.3).

**The run record as the backbone of traceability.** Each run can link a backlog item (lesson 4.2) to a review, test and scan results and an artefact version; lesson 9.3 builds on it. More changes from AI coding tools make feedback and queue time the constraint (lesson 1.2), so plan pipeline capacity first.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Pipeline service card** | One page: owner, customers, steps, service levels, funding, records | When declaring the pipeline a product; twice a year |
| **Pipeline scorecard** | Five measures with definitions, targets and pairs | Monthly review with customers |
| **Golden path template** | Ready-to-use pipeline definition with mandatory steps built in | New services and migrations |
| **Pipeline inventory** | Every path to production, owner, evidence standard met or not | First step of rationalisation; yearly |
| **Break-glass procedure** | Who may bypass which step, logging, review deadline | Agreed with risk before the first emergency |
| **CI/CD system** | The tool that runs pipelines, such as GitHub Actions or GitLab CI (examples, not endorsements) | Chosen by the platform team with its customers |

## 🏛️ In practice at Najm Bank
Illustrative and fictional. Sami drafted the service card with Huda and Nour, then reviewed it with product managers including Reem.

> **Pipeline service card — Najm Delivery Pipeline v1**
> **Owner:** Sami (Platform Engineering). **Customers:** 22 product teams (illustrative figure).
> **Standard steps (mandatory for production):** build from main line; recorded peer review; unit and integration tests; dependency and code scans; build once, store artefact with version; signed run record.
> **Service levels:** availability 99.5% in working hours; median feedback under 15 min; platform-caused failures under 2% of runs; highest-priority (P1) platform ticket response 30 min (all illustrative targets).
> **Funding:** product budget line for a team of eight (illustrative); usage shown back to teams quarterly.
> **Records:** run record per change, retained for the period Nour's team confirms with the bank's record-retention policy.
> **Break-glass:** Head of IT Operations or delegate may bypass a mandatory step; every use reviewed by risk within two working days. Peer review on tier 1 changes (lesson 5.2) is never skipped: in an emergency the on-call senior engineer reviews before merge.

Yousef, Head of IT Operations, asked for operations to own break-glass, since his team runs the operations centre at night; the card changed. Tariq used the inventory to retire two of the four licences. The audit finding closed when Nour's team pulled the run record for five random changes in minutes.

One mistake stayed in version 1: the scorecard counted adoption but not satisfaction, so the platform team celebrated 80% adoption while two teams kept laptop scripts for urgent fixes. A paired survey revealed it a quarter later.

## 🛠️ Exercises
**🟢 Inventory your paths to production.** For one IT area (or Najm Bank's Cards & Payments), list every way code reaches production: tool, owner, users, and whether test and review results are stored per change.
*Done when:* every path you can find is listed (at least three), each with an owner or "nobody" and a yes/no for stored evidence.

<details><summary>Model answer and self-check</summary>

**Model answer.** Cards & Payments: hosted CI/CD (platform team; evidence yes); old build server (owner nobody; evidence no, logs expire in seven days); laptop release script (one developer; evidence no); vendor-run deployment of the card package (vendor under Lina's contract; evidence unknown). **Self-check.**
- Did you include informal paths (laptop scripts, vendor deployments, hotfixes)? That is where the risk usually is.
- Did you check evidence storage rather than assume it?

</details>

**🟡 Write a pipeline service card.** Write a service card for a shared pipeline: owner, customers, mandatory and chosen steps, three to five service levels, funding, records, break-glass.
*Done when:* it fits on one page, every mandatory step is checkable in a run record, and every service level has a number and a definition.

<details><summary>Model answer and self-check</summary>

**Model answer.** See Sami's card: a named owner, a few mandatory steps each tied to evidence, service levels the customer feels, a budget line, retention set with risk, and break-glass with an approver, steps it cannot skip and a review deadline. **Self-check.**
- Did you leave tool choices to teams?
- Are service levels measured from the customer's side (time to feedback), not the platform's (servers up)?
- Are retention and break-glass agreed with risk, or marked "to confirm"?

</details>

**🔴 Build a paired scorecard and a mandate decision.** Write a five-measure scorecard (definition, illustrative target, paired measure). Then write a half-page decision: what you mandate, how you attract teams to the standard path, and when a team may run its own pipeline.
*Done when:* every measure has a pair that would expose gaming, the scorecard is kept apart from DORA's delivery metrics, and the decision separates mandated outcomes from encouraged tools.

<details><summary>Model answer and self-check</summary>

**Model answer.** Feedback time with escaped defects; availability with platform-caused failures; month-end queue time with build cost per team; adoption with developer satisfaction; support time to fix with repeat tickets; DORA metrics reported separately. Decision: mandate the run record for every production change; attract with a template that sets up a new service in a day; allow own pipelines that meet the evidence standard and fund their upkeep. **Self-check.**
- Would each pair catch the obvious way to game its measure?
- Did you mandate outcomes (evidence) rather than a tool?

</details>

## ⚠️ Mistakes and traps
- **Treating the pipeline as a project.** The project closes and the pipeline decays. Fund it as a product.
- **Standardising everything.** A mandated language or test tool breeds side doors. Standardise the evidence.
- **Celebrating adoption alone.** High adoption with low satisfaction is compliance, not benefit. Pair it.
- **Leaving the pipeline definition unguarded.** If mandatory steps can be removed unreviewed, the control is decorative.
- **Expecting gains on day one.** Plan for a dip and measure through it.

## 🧾 Recap
- Run the shared pipeline as a **product**: owner, customers, service levels, roadmap, stable funding.
- Keep a short list of **mandatory, evidence-producing steps**; let teams choose tools; **build once**.
- Use a small **paired scorecard**, reported separately from DORA's delivery metrics.
- The pipeline is a **control**: protect its definition, enforce segregation of duties, design break-glass in advance.
- Each run leaves a **complete, retained run record**, the backbone of traceability.

## ✍️ Check yourself
**1. Omar asks who owns the way Najm Bank builds software. Fourteen pipelines exist, each run by the team that built it. What is the best first step?**

- A. Ask every team to document its own pipeline in a shared wiki and leave ownership as it is.
- B. Buy one new CI/CD tool and order every team to migrate to it before the next quarter starts.
- C. Name the platform team as owner of a shared pipeline product and inventory every path first.
- D. Ask internal audit to review all fourteen pipelines and rank them from strongest to weakest.

<details><summary>Answer</summary>

**C.** A managed capability starts with an owner and an inventory. A changes nothing, B forces a tool before knowing what exists, D ranks but names no owner. See "From many scripts to a managed capability".

</details>

**2. Through Lina, the card package vendor's delivery lead proposes rebuilding the artefact for production "to pick up the latest settings". Sami objects. Why is Sami right?**

- A. Rebuilding means the test evidence is about a different artefact from the one deployed.
- B. Rebuilding is slower, and the bank's service level for feedback time would then be missed.
- C. Rebuilding uses more build capacity, so the cost shown back to product teams would rise.
- D. Rebuilding for production needs a separate licence from the vendor, which Lina has not bought.

<details><summary>Answer</summary>

**A.** Building once lets the bank prove that what was tested is what runs. B and C are side effects, not the reason; D is a commercial detail that misses the evidence problem. See "Standard versus chosen steps".

</details>

**3. After a year, 80% of teams use the standard pipeline, but a survey shows developers find it slow and two teams still use laptop scripts for urgent fixes. What does this most likely show?**

- A. The platform is a success, because the adoption target of 80% has now been reached.
- B. The laptop scripts should be ignored, since they are only used for urgent fixes.
- C. The survey is unreliable, because developers usually complain about any shared tool.
- D. Adoption was measured without its paired customer measure, so it hid real problems.

<details><summary>Answer</summary>

**D.** Adoption can rise through compliance while customers suffer. A trusts one measure, B ignores the riskiest path, C dismisses the paired evidence. See "Pair every measure".

</details>

**4. Two quarters after the standard pipeline launches, Tariq sees that feedback time has worsened for the teams that migrated. What is the best reading?**

- A. The platform has failed, so roll the migrated teams back to their old pipelines.
- B. Adoption is too low to show gains, so mandate the platform for every remaining team.
- C. An early dip is expected, so keep running it as a product and measure through the dip.
- D. The numbers are unreliable while teams migrate, so stop measuring until things settle.

<details><summary>Answer</summary>

**C.** The 2024 DORA announcement says platforms may bring a temporary drop before gains and work best when run as user-centred products. A gives up before the gains, B forces adoption without fixing the cause, D removes the evidence needed to see the recovery. See "What the research says about platforms".

</details>

**5. A developer edits his team's pipeline definition to skip the dependency scan "to save time", with no review. What is the main operating-model problem?**

- A. The scan is too slow, so the platform team should simply remove it for every team.
- B. A control the bank relies on was removed unreviewed, so pipeline changes need review.
- C. The platform team should re-add the scan to that team's pipeline and remind the developer.
- D. The security team should run the dependency scan by hand for that team every month.

<details><summary>Answer</summary>

**B.** The pipeline definition is itself a control, so changes to it need review and a record. A removes the control for all; C fixes this one symptom but leaves the definition open to the next unreviewed edit; D replaces an automatic control with a slower manual one. See "The pipeline is a control, so control the pipeline".

</details>

## 📚 References
- Google Cloud blog, "Announcing the 2024 DORA report", 22 October 2024 (opened 2026-11-20): https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report — platform findings (productivity, temporary dip, user-centred and product-oriented platforms).
- Google Cloud blog, "Announcing the 2025 DORA Report: State of AI-Assisted Software Development", 23 September 2025 (opened 2026-11-20): https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report — "90% of organizations have adopted at least one platform" and the link between platform quality and AI value.
- Skelton, M. and Pais, M., *Team Topologies* (IT Revolution, 2019). Background on platform teams and the "thinnest viable platform".
- Humble, J. and Farley, D., *Continuous Delivery* (Addison-Wesley, 2010). Background on the deployment pipeline and building artefacts once.

---

# 5.2 — Quality gates and evidence a manager can trust
*Level: 🟡 Intermediate* · *Prerequisites: 4.2, 5.1* · *Step: Build*

**After this you can** write gate cards for the checks a change must pass (purpose, check, threshold, owner, override rule and evidence), set them in proportion to risk with a three-tier gate matrix, and test any piece of delivery evidence against a six-point trust checklist. *Study time: reading about 15 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- A **quality gate** is a point on the path to production where a defined check must pass. Which gates exist, their thresholds and overrides are **management decisions**.
- **Evidence** is the record that a check ran, on what, with what result. Trustworthy evidence is generated by the work itself and tied to the exact artefact.
- Set gates **in proportion to risk**: a payment change and an internal report tweak need different gates.
- The rule that matters most: **evidence is a by-product of doing the work, never a separate document written about it.**
- Decision cue: if audit proof takes a week to assemble, it is being written, not generated.
- Biggest trap: gates that are green because they check little, or red so often (flaky tests) that people ignore them.

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

Nour, IT Risk and Controls Lead, sampled a March change to card limit rules for an internal audit and asked for proof it had been tested. The Cards & Payments team sent a spreadsheet of forty cases marked "passed" by hand and an email saying "QA signed off". The spreadsheet named no software version, the pipeline logs had expired after seven days, and the email predated the final code change by two days.

Nobody had lied, and the team had tested carefully, but the bank could not show it. Meanwhile the team spent about two days per release on sign-off templates that mostly repeated what the pipeline already knew: heavy paperwork, weak proof. Reem, Product Manager for Cards & Payments, wanted fewer forms; Nour wanted stronger evidence. This lesson shows how both are possible: gates inside the pipeline, set in proportion to risk, whose evidence is generated as the work happens.

## 📐 How it works

### 🟢 The essentials

**Gates, checks and evidence.** Three often-blurred terms:

| Term | Meaning | Example |
|---|---|---|
| **Check** | A test or inspection that produces a result | Run the test suite; scan dependencies |
| **Gate** | A rule the check's result must meet before the change moves on, with an owner and an override rule | "No merge unless all tests pass and a second person approved" |
| **Evidence** | The stored record of the check: which artefact, what result, passed or overridden | The run record for build 4.12.3 |

A check without a gate is information; a gate without evidence is a promise.

**The common gates.** The engineering of each is taught elsewhere (see References); here the question is what each gate is for and who sets its threshold.

| Gate | What it protects against | Typical threshold owner |
|---|---|---|
| **Peer review** | Mistakes and unreviewed changes; one person acting alone | Engineering lead, with risk agreeing the minimum |
| **Automated tests** | Regressions (things that used to work breaking) | Product team, within a bank minimum |
| **Security scans** | Known vulnerable code patterns (found by static and dynamic analysis, SAST and DAST) and components (software composition analysis, SCA) | Security, with product teams |
| **Component policy** | Banned or unapproved libraries and licences (lesson 5.3) | Platform and legal |
| **Quality requirements** | Breaking the speed, resilience or capacity targets of lesson 4.3 | Product manager and architect |
| **Human judgement** | Risks no automation sees: usability, a new regulatory rule | Product manager, with risk where needed |

**The gate card.** Every gate should be describable on one card. If nobody can fill it in, the gate is folklore.

| Field | Example (peer review gate, Cards & Payments) |
|---|---|
| **Purpose** | No change reaches the main line unread by a second competent person |
| **Check** | Approval in version control by someone other than the author |
| **Threshold** | One approval for tiers 2 and 3; two for tier 1 (see below) |
| **Owner** | Product team's engineering lead; minimum set by risk |
| **Override** | Tier 1: never skipped; in an emergency the on-call senior engineer reviews before merge. Tier 2 and 3: break-glass under lesson 5.1's procedure, reviewed by risk within two working days |
| **Evidence** | Approval linked to the change and artefact version, kept with the run record |
| **Measures** | Override rate; time in gate; reviews approved in under two minutes (rubber-stamping) |

### 🟡 Going deeper

**What makes evidence trustworthy.** An auditor or a busy manager must be able to rely on evidence without redoing the work. Six properties make that possible:

1. **Generated, not written.** The system that did the work produced the record. A hand-typed "passed" is a claim.
2. **Tied to the exact artefact.** The record names the version (or unique fingerprint, a hash) of what was tested, matching what was deployed (lesson 5.1's "build once").
3. **Time-stamped and tamper-evident.** Stored where its producers cannot quietly edit it.
4. **Complete.** Failures, overrides and re-runs are kept, not only the final green run.
5. **Retained.** Kept as long as the bank's retention rules require; ask the risk function.
6. **Meaningful.** The check tests something that matters. Coverage from tests that assert nothing passes points 1 to 5 and fails this one.

The March evidence failed points 1, 2, 4 and 5. It passed point 3, and its dates are what exposed the stale sign-off. The fix was moving the work into the pipeline so the record appears on its own.

**Proportion to risk: the gate matrix.** Payment-grade gates on every internal tool slow everything and teach that gates are bureaucracy. Set tiers with risk and product owners by impact of failure:

| Gate | Tier 1: customer money or regulated data | Tier 2: customer-facing, no money movement | Tier 3: internal, low impact |
|---|---|---|---|
| Peer review | Two reviewers, one senior | One reviewer | One reviewer |
| Automated tests | Full suite plus contract tests (checks that two services still agree on their interface) | Full suite | Unit and smoke tests (a quick check that the main functions start and respond) |
| Security scans | Code, dependency and container scans (checks of the packaged image); no unresolved critical findings | Code and dependency scans; critical findings need an owner and date | Dependency scan |
| Quality requirements | Performance test against lesson 4.3 targets for each release | Performance test when the risky path changes | Not required |
| Human judgement | Product manager acceptance; risk consulted for regulatory changes | Product manager acceptance | Team decides |

Tiers and thresholds are illustrative. What matters is that the matrix is written and agreed, so nobody argues gate by gate on release night.

**Flaky tests destroy gates.** A **flaky test** sometimes passes and sometimes fails on the same code. A 2016 Google Testing Blog post reported that almost 16% of Google's tests had some level of flakiness. When a gate is often red for no reason, people re-run it until green and it means nothing. Track the flaky rate, quarantine flaky tests with a named owner and a deadline, and do not let quarantine become a graveyard. See [*Software Testing: Zero to Hero in the AI Era*, lesson 2.3 — Are your tests any good? Coverage, mutation testing, property-based testing and flaky tests](../testing/index.html#/2.3).

**Measure the gates themselves.** Beyond each card's measures, watch **escaped defects** (production problems a gate should have caught, the truest test of a gate) and **evidence retrieval time** for a sampled change.

**Targets on gate numbers.** A mandated coverage percentage is the classic case of lesson 1.3's warning: teams reach it with tests that check nothing. Use coverage as information; escaped defects and mutation testing (checking whether tests catch deliberately introduced faults) are stronger signals.

### 🔴 Expert view

**From controls to gates.** The risk function keeps a list of **controls** (activities that reduce a risk, such as "changes are reviewed before production"), many written for manual steps such as a signed form. Nour's most valuable move is to map each delivery control to the gate that now performs it and the evidence it produces. Auditors and the second line (the independent risk function) can then test controls by sampling run records, not by interviewing people. Lesson 10.3 builds the full control matrix. NIST's *Secure Software Development Framework* (SSDF, SP 800-218, version 1.1, 2022; NIST has since published a draft version 1.2 for comment) is one public reference for secure development practices, not a requirement this course claims for your bank.

**Human gates that add value.** A product manager accepting that a change meets customer needs is judgement no tool provides. Keep such gates fast (a named decider and a time limit), record them in the run record, and remove human gates that only re-confirm what a machine proved.

**AI-written code and AI reviewers.** Google's announcement of the 2024 DORA report says 39% of respondents reported little to no trust in AI-generated code. The evidence must show which checks ran and which human accepted the change: an AI reviewer can be a check, not the only gate on a tier 1 change. See [*Software Testing: Zero to Hero in the AI Era*, lesson 6.1 — Verifying AI-generated code: how coding agents fail and a reviewer's checklist](../testing/index.html#/6.1).

**Evidence the regulator may ask for.** Rules differ by country. Ask the risk function which expectations apply to change and testing evidence, how long it must be kept, and whether system-generated evidence is accepted in place of signatures.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Gate card** | Purpose, check, threshold, owner, override, evidence, measures | Adding, changing or questioning a gate |
| **Risk-tier gate matrix** | Gates and thresholds per risk tier, agreed with risk and product owners | Setting up a product's pipeline; yearly |
| **Evidence trust checklist** | The six properties of trustworthy evidence | Before relying on evidence or designing a gate |
| **Override log** | Every bypass: who, why, which gate, review | Monthly review with risk |
| **Flaky-test quarantine list** | Quarantined tests with owner and fix-by date | Weekly team review |
| **Control-to-gate map** | Each delivery control linked to its gate and evidence | Before audits |

## 🏛️ In practice at Najm Bank
Illustrative and fictional. After the March sample, Nour, Reem and Sami rebuilt the Cards & Payments gates.

Card limits and payments became tier 1, card-benefits pages tier 2, an internal dashboard tier 3. Of the old release checklist's 34 items, 22 were already covered by the pipeline and dropped, 7 became automated checks and 5 stayed as human decisions with a named decider.

Nour's control-to-gate map for "changes are tested before production" reads: gates, automated tests plus performance tests for tier 1; evidence, reports in the run record for the deployed version; test method, sample five changes a quarter.

Reem made one mistake: a 90% coverage target. Coverage hit 91% within a month; escaped defects did not move, because many new tests checked nothing. Escaped defects and a quarterly mutation-testing sample became the measures.

The next audit sample took 20 minutes for five changes, against about a week before. Yousef also asked that tier 1 changes in the last three days of the month wait for operations to confirm capacity. That is a release-time change check, not build evidence, so it went to the change model of lesson 6.2.

## 🛠️ Exercises
**🟢 Test evidence against the checklist.** Score one piece of delivery evidence (yours, or Najm Bank's March spreadsheet and email) on the six-point checklist, one line per point.
*Done when:* all six points are marked pass or fail with a reason, plus one change that fixes the weakest.

<details><summary>Model answer and self-check</summary>

**Model answer.** March evidence: generated, fail (typed); tied to artefact, fail (no version); time-stamped, pass (the dates exist and show the sign-off predates the final change); complete, fail (no failures or re-runs); retained, fail (logs expired); meaningful, unknown. Fix: run tests in the pipeline and store the report with the deployed version's run record. **Self-check.**
- Did you separate "the testing was poor" from "the evidence is poor"? They are different problems.
- Is your fix a change in how the work is done, not a better template?

</details>

**🟡 Write three gate cards and a tier matrix.** For one product, write gate cards for peer review, automated tests and one other gate, then draft a three-tier gate matrix with at least four rows.
*Done when:* each card has all seven fields filled, each gate has an override rule (even if it is "none"), and the matrix gives a different treatment to at least two tiers for every row.

<details><summary>Model answer and self-check</summary>

**Model answer.** See "The gate card" and the tier matrix. A strong third card is security scans: thresholds from the matrix; owner security with the product team; override by the security lead with a dated risk acceptance; scan reports in the run record; measures override rate and age of open critical findings. **Self-check.**
- Does every card name an owner who can change the threshold?
- Is tier 3 genuinely lighter?

</details>

**🔴 Map controls to gates and fix one manual control.** Take three delivery controls (yours, or Najm Bank's "changes are reviewed", "changes are tested", "emergency changes are reviewed after the fact"). For each, name the gate, the evidence and a sampling test. Then rewrite one manual control so a gate performs it.
*Done when:* each control has a gate, an evidence description that meets the six-point checklist, and a sampling test; and the rewritten control no longer depends on a signature or meeting.

<details><summary>Model answer and self-check</summary>

**Model answer.** (1) "Changes are reviewed": peer review gate; non-author approval linked to the artefact; sample five deployed versions. (2) "Changes are tested": test gate, plus performance for tier 1; reports in the run record; check sampled reports match the deployed fingerprint. (3) "Emergency changes are reviewed after the fact": override log; check every override in the quarter was reviewed within two working days. Rewritten: "A second person signs the change form" becomes "The pipeline blocks merge until a non-author approves in version control; the approval is kept with the run record." **Self-check.**
- Could an auditor test each control without interviewing anyone?
- Did you avoid claiming what a specific regulation requires?

</details>

## ⚠️ Mistakes and traps
- **Writing evidence after the fact.** Sign-off emails assembled before an audit are claims.
- **One set of gates for everything.** It teaches people that gates are bureaucracy. Write a tier matrix.
- **Living with flaky tests.** Re-run until green and the gate means nothing. Quarantine with an owner, then fix.
- **Targets on coverage.** Met with tests that check nothing. Manage escaped defects instead.
- **An AI reviewer as the only gate on tier 1 changes.** Keep a named human accountable.

## 🧾 Recap
- A **check** produces a result, a **gate** decides on it, **evidence** proves it.
- Describe every gate on a **gate card**. Trustworthy evidence is **generated, tied to the artefact, time-stamped, complete, retained and meaningful**.
- Set gates **in proportion to risk**; keep human gates where judgement is the point.
- Map delivery **controls to gates** so they can be tested by sampling records.

## ✍️ Check yourself
**1. Nour samples a March change. The team provides a hand-filled spreadsheet marked "passed" and a sign-off email dated before the final code change. What is the core problem?**

- A. The spreadsheet has too few test cases, so the change was clearly not tested well enough.
- B. The evidence was written by hand and is not tied to the version that actually went live.
- C. The email should have come from the product manager, not from the test lead on the team itself.
- D. Spreadsheets are not allowed for testing, so the team broke a rule of the risk function.

<details><summary>Answer</summary>

**B.** The evidence fails "generated" and "tied to the exact artefact". A judges the testing, not the evidence; C changes the signer; D invents a rule. See "What makes evidence trustworthy".

</details>

**2. The Cards & Payments team wants one set of gates for every change, "to be safe". Reem worries this will slow internal tools. What does the lesson recommend?**

- A. Apply the strictest gates everywhere, because any change in a bank can harm customers.
- B. Let each developer choose the gates for each change, since they know the code best.
- C. Keep one set of gates, but let teams skip some for internal tools when time is short.
- D. Agree a written tier matrix with risk and product owners that sets gates by impact.

<details><summary>Answer</summary>

**D.** Written, agreed tiers avoid both bureaucracy and gaps. A treats everything as tier 1, B removes the standard, C turns every skip into an unrecorded negotiation. See "Proportion to risk: the gate matrix".

</details>

**3. The tier 1 test gate fails about once a day and passes when re-run with no code change. Developers now re-run it by habit. What should the team do?**

- A. Track the flaky rate, quarantine flaky tests with an owner and date, and then fix.
- B. Remove the test gate for tier 1, because a gate that fails randomly has no real value.
- C. Allow unlimited re-runs and record only the final green result in the run record.
- D. Raise the gate's threshold so that a few failed tests no longer block the change.

<details><summary>Answer</summary>

**A.** Quarantine with an owner and deadline, then fix, so red means something again. B drops a tier 1 control, C breaks "complete", D hides real failures. See "Flaky tests destroy gates".

</details>

**4. Reem sets a 90% code coverage target. A month later coverage is 91% but escaped defects have not changed. What is the best reading?**

- A. The target worked, and escaped defects will fall once the new tests have time to settle.
- B. Raise the target to 95% next quarter so the extra tests reach the riskiest code paths.
- C. The target was met with tests that check little, so manage escaped defects in future.
- D. Escaped defects are the wrong measure, because production problems have many causes.

<details><summary>Answer</summary>

**C.** Coverage targets can be met by tests that check nothing. A and B trust the target; D discards the truest signal. See "Targets on gate numbers".

</details>

**5. Nour wants auditors to test the control "changes are reviewed before production" without interviewing staff. What should she build?**

- A. A quarterly meeting where engineering leads confirm that every change was reviewed.
- B. A new form that each developer signs to say a colleague has looked at the change.
- C. A quarterly sample of change tickets whose "reviewed" box was ticked by the developer.
- D. A control-to-gate map linking the control to the review gate and its run records.

<details><summary>Answer</summary>

**D.** The map lets auditors test by sampling generated records. A, B and C all rely on people's statements, not on records the system produced. See "From controls to gates".

</details>

## 📚 References
- Google Cloud blog, "Announcing the 2024 DORA report", 22 October 2024 (opened 2026-11-20): https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report — the 39% trust figure.
- Micco, J., "Flaky Tests at Google and How We Mitigate Them", Google Testing Blog, May 2016 (the "almost 16%" figure as reported in search results; the page could not be opened from this environment): https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
- NIST, SP 800-218, *Secure Software Development Framework (SSDF) Version 1.1*, February 2022: https://csrc.nist.gov/pubs/sp/800/218/final
- NIST, SP 800-218 Rev. 1 (initial public draft), *SSDF Version 1.2*, 17 December 2025 (as reported in search results): https://csrc.nist.gov/pubs/sp/800/218/r1/ipd
- Library course: [*Software Testing: Zero to Hero in the AI Era*, lesson 5.2 — Testing in CI/CD and in production: fast pipelines, flaky-test policy, feature flags, canaries and synthetic monitoring](../testing/index.html#/5.2).
- Library course: [*Secure AI & Application Security: Zero to Hero*, lesson 6.1 — A secure development life cycle: requirements, review and testing (SAST, DAST, SCA)](../secai/index.html#/6.1).

---

# 5.3 — Third-party, SaaS and open-source components in the product
*Level: 🟡 Intermediate* · *Prerequisites: 4.3, 5.1, 5.2* · *Step: Build*

**After this you can** write a component policy (what may enter a product, on what conditions, and who decides), set up a component inventory that answers "where do we use X?" in minutes, and draft a response playbook for the day a widely used component turns out to be vulnerable. *Study time: reading about 20 min, hands-on about 105 min (estimate).*

## ⚡ In 60 seconds
- Products are mostly made of things the bank did not write: **open-source libraries**, **commercial components** and **outside services** (SaaS and APIs).
- Each brings five exposures: **security**, **licence**, **continuity**, **data** and **cost**.
- Keep a pipeline-generated **component inventory**; a **software bill of materials** (SBOM) is its standard form.
- The rule that matters most: **if it runs in your product, it is in your inventory, and someone by name owns it.**
- Decision cue: when the next big vulnerability is announced, can you list affected products and owners within an hour?
- Biggest trap: treating open source as "free" and SaaS as "the vendor's problem".

## 🧭 Why it matters
Najm Bank, its Technology division and the people in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

In December 2021 a critical vulnerability in Apache Log4j, a widely used open-source Java logging library, was disclosed as CVE-2021-44228, "Log4Shell" (a CVE is the public ID given to a known vulnerability). The US Cybersecurity and Infrastructure Security Agency (CISA) urged organisations to upgrade or apply mitigations, and on 22 December 2021 it and partner agencies issued a joint advisory (AA21-356A) warning that malicious actors were actively scanning for and exploiting it. For many organisations the hard part was "where do we use it?": the library often arrived inside other libraries and commercial products.

In March 2024 CISA reported malicious code in versions 5.6.0 and 5.6.1 of XZ Utils, a data compression package that may be present in Linux distributions (CVE-2024-3094): a deliberate backdoor, not a bug.

When Nour, IT Risk and Controls Lead, ran a Log4Shell-style desk exercise, Najm Bank took nine days to confirm which products were affected. Reem's Cards & Payments app depended on more than 600 open-source packages, most never chosen directly, and seven outside services, such as fraud scoring and SMS, that Lina, Vendor and Sourcing Manager, had contracted but nobody had linked to the product.This lesson makes such components visible, owned and managed.

## 📐 How it works

### 🟢 The essentials

**Three kinds of component.**

| Kind | What it is | Example at Najm Bank (fictional) |
|---|---|---|
| **Open-source library** | Code anyone may use on its licence's terms; a developer adds it, and it brings its own dependencies | A date-handling library |
| **Commercial component** | Code or a package bought and run inside the bank | The card management package |
| **Outside service (SaaS or API)** | A function another company runs, called over the network at run time | Fraud scoring, SMS one-time passwords |

A **direct dependency** is a library your team chose; a **transitive dependency** is one your libraries depend on, and so on down. Most components are transitive, so "we never chose that" is no defence.

**Five exposures.** Questions the product owner must be able to answer for each component:

| Exposure | The question | Who helps answer it |
|---|---|---|
| **Security** | Known vulnerabilities, and how fast are they fixed? | Security, with the product team |
| **Licence** | What do the terms allow and require? | Legal |
| **Continuity** | Maintained? Still offered? What is our exit? | Product team; Lina for contracts |
| **Data** | Does customer data flow to it, and where? | Data protection officer and Nour |
| **Cost** | Cost now and at scale, including staying current | Tariq |

**Who owns what.** Write the split down:

- The **product team** owns the components in its product, transitive ones included: it keeps them current and responds when they are vulnerable.
- The **platform team** (lesson 5.1) provides the tools: inventory generation, scanning, and a mirror of approved packages (an internal copy of vetted libraries that builds fetch from).
- **Security** sets vulnerability thresholds and leads response to major events.
- **Lina** owns commercial relationships (lesson 10.2); **Nour** owns the third-party risk view (lesson 10.3); **legal** interprets licences and contracts.

**The inventory.** A **software bill of materials** (SBOM) lists the components in a piece of software and how they relate. The US National Telecommunications and Information Administration (NTIA) published *The Minimum Elements for a Software Bill of Materials* in July 2021, which uses the definition from US Executive Order 14028: "a formal record containing the details and supply chain relationships of various components used in building software". The SBOM should be **generated by the pipeline on every build**, **stored with the run record** (lesson 5.2) so it describes what was deployed, and **searchable across products**, so "where do we use X?" is a query.

Outside services do not appear in an SBOM built from code, so keep a **third-party service register** per product: service, supplier, contract, data sent, owner, exit plan. SBOM plus register is the full inventory.

### 🟡 Going deeper

**A component policy: allowed, conditional, blocked.** Decide in advance what may enter a product, so teams are not blocked case by case:

| Category | Meaning | Example conditions (illustrative) |
|---|---|---|
| **Allowed** | Use without asking | Approved licence; maintained; no unresolved critical vulnerability |
| **Conditional** | Short recorded review | Licence needs legal view; single maintainer; tier 1 product; customer data leaves the bank |
| **Blocked** | The pipeline gate stops it (lesson 5.2) | Known malicious; licence ruled out by legal; unsupported end-of-life |

The pipeline's component gate (lesson 5.2) enforces it: conditional items need a recorded approval, and everything lands in the SBOM.

**Licences: ask, do not decide.** Some open-source licences (often called **permissive**) mainly ask for attribution; others (often called **copyleft**) can require sharing software built with them under the same terms in some distribution situations. Code with no licence is not free to use. Whether an obligation applies is a legal question. Black Duck, a tools vendor, reported in its 2026 *Open Source Security and Risk Analysis* that 68% of the 947 commercial codebases it audited had licence conflicts, up from 56% a year earlier (vendor research on its own audits, not a census). Catch licence questions at intake, with legal setting the approved list.

**Judging the health of an open-source project.** An excellent library is still risky if one tired volunteer maintains it. Look at recent releases, active maintainers and speed of security fixes. The OpenSSF (Open Source Security Foundation) runs **Scorecard**, a tool for "security health metrics for Open Source" that scores projects 0 to 10 on automated checks such as Maintained and Code-Review. Use scores as input to a conditional review, never as a verdict.

**Outside services in the product.** A SaaS or API in the critical path is a runtime dependency: when it is down, your product is down. Settle four things:

- **Service levels** matching the product's quality requirements (lesson 4.3), monitored on the real service (lesson 8.1), and notice of API changes.
- **Data**: what customer data is sent and where it is processed; ask the data protection officer.
- **Exit**: how you would replace it, how long it would take, whether the data comes back.
- **Regulation**: whether a service counts as outsourcing under the bank's rules, and what approval it needs, is for Nour's team to decide.

For the build-or-buy decision behind a service, see [*System Design for Vibe Coders*, lesson 0.3 — Build vs Buy: the Highest-Leverage Decision You'll Make](../vibe/index.en.html#l0-3).

### 🔴 Expert view

**Vulnerability response as a measured process.** What decides the outcome is speed from "advisory published" to "fixed everywhere it matters". Treat it as a value stream (lesson 1.2) with four stages: know (needs the inventory), decide (needs owners and tiers), fix (needs a fast pipeline, lesson 5.1), confirm (needs the new SBOM). Agree targets by severity and tier with security, and measure real events against them.

**Provenance and integrity.** XZ Utils showed that a component can be malicious. **SLSA** (Supply-chain Levels for Software Artifacts, an OpenSSF project) describes levels of assurance for how an artefact was built and its provenance record (who built it, how, from which inputs). Signing, the approved-package mirror and pinned versions all make a tampered component harder to slip in. See [*Secure AI & Application Security: Zero to Hero*, lesson 6.2 — The software supply chain: dependencies, SBOMs, SLSA and signing](../secai/index.html#/6.2). The manager's decision is which products must meet which level, and by when.

**AI assistants add components too.** The policy and gate apply equally to components a coding agent suggests; see [*A Practical Guide to Becoming an AI-Native Engineer*, lesson 8.1 — When an agent has your keyboard: injection, secrets, destructive commands, hallucinated packages, permissions and sandboxes](../ainative/index.html#/8.1) for how agents can suggest packages that do not exist.

**Commercial products contain open source too.** Ask suppliers, through Lina's contracts, for an SBOM or equivalent and vulnerability response commitments; otherwise the inventory has a hole where you have least control.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Component policy** | Allowed, conditional and blocked categories with conditions and deciders | Written with security, legal and risk; yearly |
| **SBOM (software bill of materials)** | Machine-readable list of components and their relationships, generated per build (formats such as SPDX and CycloneDX) | Every build; stored with the run record |
| **Third-party service register** | Each outside service per product: supplier, contract, data sent, owner, service levels, exit plan | When adding a service; reviewed with Lina and Nour; an exit plan for every tier 1 service |
| **Software composition analysis (SCA) tool** | Scans dependencies for known vulnerabilities and licences, often producing the SBOM | In the component gate |
| **Vulnerability response playbook** | Stages, owners, targets by severity and tier | Rehearsed twice a year |

## 🏛️ In practice at Najm Bank
Illustrative and fictional. After the desk exercise, Sami, Nour, Lina and Reem produced three artefacts.

**The component policy (extract).**

> **Allowed:** licence on legal's approved list, a release in the last 12 months, no unresolved critical vulnerability.
> **Conditional (recorded approval by the product's engineering lead and security):** licence not on the list (legal decides); single active maintainer; any library in a tier 1 payment path; any outside service that receives customer data (Nour and the data protection officer consulted).
> **Blocked:** security's blocklist; versions with known malicious code; components past end of support without an agreed exception.
> **Owner of the policy:** Huda, Head of Enterprise Architecture; reviewed yearly.

**The inventory.** Sami's team added SBOM generation to the golden path, with a search page for "which products contain library X at version Y?". Lina and Reem built the Cards & Payments service register: seven services, each with an owner, a data note and an exit note. It showed the SMS provider in the payment path with no fallback.

**The playbook.** Know, decide, fix, confirm, with targets for critical tier 1 issues: affected list in four hours, decision in one working day, fix or mitigation in five, confirmation by new SBOM. Security leads; product teams fix; Yousef's operations team coordinates out-of-hours deployment. Six months later the desk exercise took 40 minutes for golden-path products.

One mistake: Reem's team first blocked every library below a fixed Scorecard result. Developers copied a small, well-run library's code into the app, making it invisible to the inventory. Low scores now trigger a conditional review instead.

## 🛠️ Exercises
**🟢 Find what is in one product.** For one product (or Najm Bank's Cards & Payments), list its outside services and its direct and transitive dependency counts, from an SBOM or dependency list if you can, otherwise by asking the team.
*Done when:* each service has an owner or "unknown", each count is a number or an honest "unknown" with how you would find out, and you have recorded where the product's SBOM is stored and timed one "where do we use library X?" search across products.

<details><summary>Model answer and self-check</summary>

**Model answer.** Cards & Payments (fictional): fraud scoring (owner Reem), SMS one-time passwords (owner unclear), address lookup (Reem), card network link (operations), cloud monitoring (platform), and two more found only in network configuration. Open source: about 40 direct and over 600 total dependencies. SBOM: none stored, so the "where do we use X?" search took two days of emails; with SBOMs in the golden path it took minutes. **Self-check.**
- Did you count transitive dependencies, or only the ones the team chose?
- Did you time the search, rather than estimate it?

</details>

**🟡 Write a component policy.** Draft a one-page policy: allowed, conditional and blocked categories, their conditions, who decides conditional cases, and how the pipeline enforces it.
*Done when:* each category has at least two concrete conditions, every conditional case names a decider, licence questions route to legal, and outside services are covered as well as libraries.

<details><summary>Model answer and self-check</summary>

**Model answer.** See the Najm Bank extract. A strong policy also stores conditional approvals with the run record and sends low-scoring libraries to review rather than blocking them. **Self-check.**
- Did you avoid deciding licence questions yourself?
- Does any rule give people a reason to hide components? Soften it.
- Are services receiving customer data conditional, with risk and data protection consulted?

</details>

**🔴 Draft a response playbook and rehearse it.** Write a playbook with four stages (know, decide, fix, confirm), owners and targets by severity and tier. Then run a 30-minute desk exercise: assume a critical vulnerability in a widely used library today, and time how long listing affected products and owners takes.
*Done when:* each stage has an owner and target, the "know" stage has a recorded time, and you have named the change that would most shorten it.

<details><summary>Model answer and self-check</summary>

**Model answer.** Know (security, via SBOM search and service register), decide (product owners with security, by tier), fix (product teams via the pipeline), confirm (security, via new SBOMs), with targets as in Najm Bank's playbook. Risk informs management and, where rules require, the regulator; Lina contacts suppliers. A first run often cannot finish in 30 minutes; the usual fix is SBOMs in every pipeline. **Self-check.**
- Did you include commercial products and outside services, not just your own code?
- Is your improvement a change to records or the pipeline, not a promise to "be faster"?

</details>

## ⚠️ Mistakes and traps
- **"The vendor handles it."** A SaaS outage is your outage. Contract for service levels and an SBOM; plan your exit.
- **Hand-written inventories.** Stale the next day. Generate the SBOM on every build.
- **Deciding licence questions in IT.** Route them to legal.
- **Policies so strict that people hide components.** Use conditional review instead.
- **Falling years behind on updates.** The urgent fix becomes a risky big upgrade on the worst day. Update in small steps and budget upkeep as run cost (lesson 10.1).

## 🧾 Recap
- Products are built largely from **open-source libraries, commercial components and outside services**; the **product team owns** them all, transitive dependencies included.
- Keep a **component inventory**: pipeline-generated **SBOMs** plus a **third-party service register**.
- Use a **component policy** (allowed, conditional, blocked) enforced by the pipeline.
- Treat **vulnerability response as a measured value stream**.

## ✍️ Check yourself
**1. A critical vulnerability is announced in a popular open-source library. Omar asks which Najm Bank products are affected. What makes this answerable within an hour?**

- A. Searchable SBOMs generated by the pipeline on every build, plus the service register.
- B. A request to every team lead to check the code and report back by email within a week.
- C. The commercial contracts for each product, which list the open-source libraries used.
- D. A search of the bank's own source code for the library's name in import lines.

<details><summary>Answer</summary>

**A.** SBOMs cover direct and transitive dependencies of what was built; the register covers services. B is slow, C rarely lists open source, D misses transitive and commercial components. See "The inventory".

</details>

**2. A developer says the cards app does not use a library because "we never added it". The SBOM shows it is there. How is that possible?**

- A. The SBOM tool is wrong, because a library cannot be in a product unless someone added it.
- B. It is a transitive dependency, brought in by another library that the team did choose.
- C. A supplier installed it on the servers, so it belongs to the vendor, not the bank.
- D. It was added by the platform team, so the product team is not responsible for keeping it.

<details><summary>Answer</summary>

**B.** Most components arrive transitively, and the product team still owns them. A denies how dependencies work; C and D move ownership away. See "Three kinds of component".

</details>

**3. Reem's team blocks every library with a low Scorecard result. Developers start copying a small library's code into the app to get past the gate. What should change?**

- A. Raise the blocking score further, so developers pick larger, better-maintained libraries.
- B. Add the small library to an exception list so it passes the gate without further review.
- C. Send low-scoring libraries to a recorded conditional review rather than blocking them.
- D. Scan the copied code with the security tools and leave the gate and its threshold as they are.

<details><summary>Answer</summary>

**C.** Scores should trigger review, not a verdict; rules that drive hiding blind the inventory. A worsens the hiding, B fixes one case but keeps the rule, D leaves copied code outside the SBOM. See "Judging the health of an open-source project".

</details>

**4. The cards app uses an outside SMS service for one-time passwords in the payment path. Lina has the contract. What is the most important gap if there is no exit plan?**

- A. Lina has no documented alternative supplier to use as leverage at the next price review.
- B. The bank cannot show auditors that the SMS supplier holds current security certifications.
- C. The SMS service is missing from the SBOM, so a vulnerability in it would not be found.
- D. If the service fails or is replaced, the bank has no known way to keep payments working.

<details><summary>Answer</summary>

**D.** A critical service is a runtime dependency; without an exit plan the payment path has no fallback. A is a smaller commercial point, B a different gap, and C confuses the SBOM with the service register. See "Outside services in the product".

</details>

**5. A team asks IT management whether a library's copyleft licence obliges the bank to publish its app's source code. What is the right response?**

- A. Ask the security team to decide, since it already runs the licence scan in the pipeline.
- B. Route the question to legal, which decides by how the software is used and distributed.
- C. Let the product's engineering lead decide, since the team knows how the app is distributed.
- D. Replace the library with a permissively licensed one now, without asking anyone else.

<details><summary>Answer</summary>

**B.** Whether an obligation applies depends on use and distribution, a legal question. A and C hand a legal conclusion to people who cannot interpret the licence; D may be costly and unnecessary, and still skips legal. See "Licences: ask, do not decide".

</details>

## 📚 References
- CISA, FBI, NSA and international partners, "Mitigating Log4Shell and Other Log4j-Related Vulnerabilities", advisory AA21-356A, 22 December 2021 (as reported in search results): https://www.cisa.gov/news-events/alerts/2021/12/22/mitigating-log4shell-and-other-log4j-related-vulnerabilities
- CISA, "Reported Supply Chain Compromise Affecting XZ Utils Data Compression Library, CVE-2024-3094", alert, 29 March 2024 (as reported in search results): https://www.cisa.gov/news-events/alerts/2024/03/29/reported-supply-chain-compromise-affecting-xz-utils-data-compression-library-cve-2024-3094
- NTIA, *The Minimum Elements for a Software Bill of Materials (SBOM)*, July 2021 (as reported in search results): https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom
- Federal Register, "Software Bill of Materials Elements and Considerations", 2 June 2021, quoting the Executive Order 14028 SBOM definition (as reported in search results): https://www.federalregister.gov/documents/2021/06/02/2021-11592/software-bill-of-materials-elements-and-considerations
- OpenSSF, Scorecard project repository (opened 2026-11-20): https://github.com/ossf/scorecard — description, 0 to 10 scoring and check names.
- SLSA, "Security levels" (OpenSSF; as reported in search results): https://slsa.dev/spec/v1.0/levels
- Black Duck, *2026 Open Source Security and Risk Analysis* (OSSRA) report page, March 2026 (68% of 947 audited codebases with licence conflicts, against 56% the year before, as reported in search results; vendor research): https://www.blackduck.com/resources/analyst-reports/open-source-security-risk-analysis.html
