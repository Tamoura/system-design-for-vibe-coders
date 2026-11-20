# Module 12 — Frameworks and transformation

*By now Najm Bank's Technology division has the pieces of a product-aligned operating model on paper: value streams, products and platforms, a portfolio, one front door, managed pipelines, a change model, a catalogue, service levels, linked records, cost models, a supplier approach, controls and a toolchain map. Three questions remain before any of it becomes real. Which published frameworks should the bank use, and how, without letting them run the bank? Where does the division actually stand today, on evidence rather than opinion? And in what order should it change, and how should its leaders bring 600 people and their suppliers with them? This module answers those three questions. You will build a framework register (12.1), run an evidence-based maturity review (12.2) and write a transformation roadmap with a plan for leading the change (12.3). Lesson 12.1 is the one place in this course that names and compares frameworks; everywhere else the course uses its own words.*

> **Steps:** Improve, Govern — choose the references you borrow from, measure where you stand on evidence, and change the operating model in waves that people can follow and auditors can trace.

---

# 12.1 — The frameworks landscape: what each is for, and how to use them without becoming their servant
*Level: 🔴 Advanced* · *Prerequisites: 0.3, 2.2, 10.3* · *Step: Govern, Improve*

**After this you can** build a one-page framework register for your organisation that names, for each framework in use or proposed, its owner, the question it helps answer, where it is used, its internal owner, any licence or certification question to take to legal, and a decision (reference, selective use, certify against, or retire). *Study time: reading about 15 min, hands-on about 100 min (estimate).*

## ⚡ In 60 seconds
- A **framework** here is any published guidance, standard, reference model or research programme about managing IT. The kind matters: guidance you adapt, standards you certify against, research you learn from.
- The rule that matters most: **borrow the question, keep your own map.** Use a framework to check that you have not missed something, not as the design of your organisation.
- Each well-known framework is strongest on one question. Overlaps are normal.
- Decision cue: before adopting a framework, write the question it must answer and the decision it will change. If you cannot, you are buying vocabulary.
- Frameworks are owned. Ask legal before copying text, diagrams or structures.
- Biggest trap: becoming the framework's servant, where titles and tool menus follow the book and no outcome improves.

## 🧭 Why it matters
Najm Bank and everyone in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

At the first steering meeting of the operating-model programme, Omar, the CIO, asked: "Which framework are we following?" He got four answers. Yousef, Head of IT Operations, named the service desk's service management framework. Nour, IT Risk and Controls Lead, named the governance framework internal audit uses. Huda, Head of Enterprise Architecture, named her architects' certification. Reem, Product Manager for Cards & Payments, named the scaling framework a supplier was piloting with her teams.

Nobody was wrong, and nobody was answering the same question. Each framework had arrived to solve one group's problem, so "change", "service" and "product" meant different things on different floors. Omar wanted one framework for everyone. Huda argued instead for listing what is in use, keeping the bank's own operating model as the map, and using each framework for the question it answers best. This lesson gives you the method.

## 📐 How it works

### 🟢 The essentials

**Kinds of framework.** The kind tells you how to use it. **Guidance** describes practices you adapt. A **management-system standard** states requirements you can be certified against. A **governance standard** gives the board principles. An **architecture method** helps you check completeness. A **scaling framework** gives structures for many teams. **Research** publishes findings, not prescriptions. **Domain practice** covers one topic, such as cost or suppliers.

**What each well-known framework is for.** Owners, editions and dates below are as reported in search summaries (November 2026), not read on the owners' pages. Read the owner's own page before relying on any detail; versions change.

| Framework | Kind | Owner | What it is for, in one line |
|---|---|---|---|
| **ITIL®** | Guidance | PeopleCert (which acquired AXELOS, the previous owner, in 2021) | Guidance on designing, delivering, supporting and improving IT-enabled services |
| **COBIT®** | Guidance | ISACA | A framework for the governance and management of enterprise information and technology |
| **ISO/IEC 20000-1** | Management-system standard | ISO and IEC | Requirements for establishing, running and improving a service management system; certifiable |
| **ISO/IEC 38500** | Governance standard | ISO and IEC | Guidance for governing bodies on the effective, efficient and acceptable use of IT; a 2024 edition is reported as current |
| **TOGAF®** | Architecture method | The Open Group | An enterprise architecture methodology and framework; a 10th Edition was reported released in 2022 |
| **The Open Group IT4IT™ Standard** | Reference architecture | The Open Group | A reference architecture for managing the business of IT. IT4IT is a trademark of The Open Group; see its own site. This course is not based on it and does not describe it |
| **VeriSM™** | Guidance | IFDC (International Foundation for Digital Competences) | A service management approach for digital services that combines existing practices rather than replacing them |
| **SAFe®** | Scaling framework | Scaled Agile, Inc. | Patterns for running lean and agile delivery across many teams and a portfolio |
| **TBM framework and taxonomy** | Domain practice | TBM Council | A shared way to classify and report technology cost (see lesson 10.1) |
| **FinOps Framework** | Domain practice | FinOps Foundation | Practices for managing cloud and wider technology spend (see lesson 10.1) |
| **SIAM** | Domain practice | Body of knowledge published by Scopism, among others | Governing and coordinating services from several suppliers (see lesson 10.2) |
| **DORA research** | Research | DORA, now part of Google Cloud | Annual research on software delivery performance and the capabilities linked to it (see lesson 1.3) |

Security and AI frameworks are compared elsewhere: see [*Secure AI & Application Security: Zero to Hero*, lesson 11.1 — Frameworks: NIST CSF 2.0, ISO/IEC 27001, NIST SSDF and OWASP SAMM](../secai/index.html#/11.1) and [*AI Governance: Zero to Hero*, lesson 7.3 — The global map: other frameworks that shape practice](../aigp/index.html#/7.3). Internal control frameworks are introduced in lesson 10.3.

**Start from questions, not from frameworks.** List the questions your operating model must answer and note which reference helps with each:

| Question your operating model must answer | Course lessons | References that address it |
|---|---|---|
| How do we decide what IT should do and who is accountable to the board? | 3.1, 3.3, 10.3 | COBIT, ISO/IEC 38500 |
| How do we design, deliver and support services people can rely on? | 2.3, 7.x, 8.x | ITIL, ISO/IEC 20000-1, VeriSM |
| How do we shape the architecture and the target state? | 4.3, 9.1 | TOGAF |
| How do many teams deliver together without a coordination tax? | 2.2, 5.1 | SAFe, *Team Topologies*, Scrum |
| How fast and safely do we deliver, and what capabilities drive that? | 1.3, 5.x, 6.x | DORA research |
| What does IT cost, per product and per unit? | 7.3, 10.1 | TBM, FinOps Framework |
| How do we run one service across many suppliers? | 10.2 | SIAM |

No single reference answers every row. The right question is "which reference for which decision, and who owns that choice?"

### 🟡 Going deeper

**The framework register.** One row per framework in use or proposed, kept by enterprise architecture and reviewed yearly:

| Field | What to write |
|---|---|
| **Framework and version** | Name, owner, edition in use |
| **Question it answers here** | The decision it informs at your organisation, in one sentence |
| **Where it is used** | Teams, processes, tools, contracts, audits |
| **Internal owner** | Who decides how it is applied here |
| **Use decision** | One of the four below |
| **Terms and licences** | Open questions for legal: trademarks, copying, training, vendor "alignment" claims |
| **Mapping** | Where its terms differ from the bank's own words, and the bank's word to use |
| **Evidence of value** | What outcome improved since it was adopted, or "unknown" |

**Four use decisions.** Most organisations need only these four:

- **Reference.** Consulted when designing; no training programme. Cheapest, and usually right.
- **Selective use.** Named practices adopted and adapted (say, for major incidents). Write down which and why.
- **Certify against.** A formal scope is audited, usually because a customer, contract or regulator asks. Scope it tightly: a certificate proves only that its scope conforms.
- **Retire.** It no longer answers a live question. Remove its vocabulary from tools and titles over time.

**Your words, mapped to theirs.** Write the operating model in your own words. A **term map** shows where a reference uses a different word for the same idea, or the same word for a different idea ("change", "release", "service" and "product" usually collide). It maps *your* model to each reference, so you never reconcile two books with each other.

**Certification and training are businesses.** Most proprietary frameworks come with certification schemes, trainers and consultancies. That is legitimate, with two cautions. A count of certified staff is an input, not an outcome. And owners publish terms on the use of their names, text, diagrams and training material: ask legal to read them before building internal training, templates or tool configurations from a framework's content.

**Regulators and frameworks.** Do not assume. Ask the risk function: "Does our supervisor expect certification to any specific standard, or only outcomes under its rules?" The answer decides between "certify against" and "reference".

### 🔴 Expert view

**How to tell you have become the framework's servant.** Warning signs:

| Sign | What to do instead |
|---|---|
| **Process count as progress** ("18 of 22 practices implemented") | Report the outcome each practice was meant to improve |
| **Tool shaped by the book** (menus for processes nobody performs) | Configure tools around your records and decisions (lesson 11.1) |
| **Titles follow the framework**, not how work flows | Name roles after the decisions they own (lesson 2.2) |
| **Audit by conformance only** | Test controls against risk and evidence (lesson 10.3) |
| **"The framework says so"** ends debates | Ask what outcome the practice protects, and test it |
| **Several frameworks, no map** | Keep one operating model and a term map per reference |

**Research is not prescription.** DORA's findings are associations in survey data. Use them to choose capabilities and measures, and never turn its measures into team targets (lesson 1.3).

**Frameworks and AI tools.** AI assistants can generate a "framework-aligned" process document in minutes: the servant trap at speed, with the added risk of reproducing protected wording or structures. Use AI on your own register and term map, and treat any generated policy as a draft a named owner checks (lesson 11.3).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Framework register** | One row per framework: owner, question, use, internal owner, decision, terms, mapping, evidence of value | At the start of an operating-model change, then yearly |
| **Question-to-reference grid** | Your key questions, and the references that help with each | When someone asks "which framework are we following?" |
| **Term map** | Your word, each reference's word for the same idea, and collisions | Before configuring tools, writing policies or training |
| **Use-decision rules** | Reference, selective use, certify against, retire, with criteria | When a team proposes a new framework or training |

Frameworks are named factually; none is endorsed, and this course is not derived from any of them.

## 🏛️ In practice at Najm Bank
Huda built the register in two weeks. Illustrative, fictional extract:

| Framework | Question it answers here | Internal owner | Use decision | Evidence of value |
|---|---|---|---|---|
| ITIL® | How we design and support services | Yousef | Selective use: incident, request and major-incident practices | Faster major-incident reviews since training |
| COBIT® | How internal audit frames IT governance reviews | Nour | Reference | No outcome measure |
| TOGAF® | How architecture work is structured | Huda | Reference | Unknown; review in 12.2 |
| SAFe® | How the three Cards teams plan together | Reem | Under review: pilot ends in Q2 | Pilot measures not yet defined |
| ISO/IEC 27001 | Security management, data centre scope | Nour | Certify against | Required by two client contracts |
| DORA research | What to measure in delivery | Sami | Reference | Baseline in 12.2 |

The register settled three arguments. Omar stopped looking for one framework. Reem agreed the scaling pilot needed outcome measures before it expanded. Yousef found three configured service-platform processes nobody used and planned their retirement (lesson 11.2). Huda's term map records that the bank uses "release" for making a feature available to customers (lesson 6.1).

## 🛠️ Exercises
**🟢 List and classify.** List every framework, standard or method named in your organisation's policies, job descriptions, tool configurations and contracts. Classify each by kind and name its owner.
*Done when:* you have a list of at least five entries, each with a kind and an owner checked against the owner's own website.

<details><summary>Model answer and self-check</summary>

**Model answer.** A typical bank list: service management guidance, a governance framework used by audit, a security standard with a certified scope, an architecture framework, a scaling framework in one area, an internal-control framework used by the second line (the risk function that oversees IT, lesson 10.3), and DORA research, each with kind, owner and where you found it.

**Self-check.**
- Did you look beyond policies, at tools and job titles?
- Did you check each owner on its own site?
- Did you separate certifiable standards from guidance?

</details>

**🟡 Fill the register.** For three of those entries, complete every field of the register row.
*Done when:* three complete rows exist, each with a single use decision, a named internal owner and at least one open question for legal or "none" with a reason.

<details><summary>Model answer and self-check</summary>

**Model answer.** For a service management reference: question "how we design and support services"; used by the service desk; owner the Head of IT Operations; decision "selective use" of incident and major-incident practices; legal question "may we build internal training from guidance we purchased?"; evidence "major-incident review times since adoption". The other rows follow the pattern.

**Self-check.**
- Is each question one the bank actually has to answer, not the framework's own purpose statement?
- Does each row have exactly one use decision?
- Is "evidence of value" an outcome, not a count of trained staff?

</details>

**🔴 Find the servant signs.** Review one area (say, change management) against the warning signs. Find two, and for each propose a change that puts an outcome in place of conformance.
*Done when:* a short note names two signs with evidence (a report title, a meeting name) and two proposed changes, each with the outcome measure it protects.

<details><summary>Model answer and self-check</summary>

**Model answer.** "Sign 1, process count: the quarterly report shows '14 of 16 change practices implemented'. Proposal: report change lead time and change fail rate for the top five products (lessons 1.3, 6.2). Sign 2, tool shaped by the book: a configured process with no records in a year. Proposal: retire it; measure: share of change records completed in the main workflow, and time spent maintaining unused configuration."

**Self-check.**
- Is each sign backed by something you can show, not an impression?
- Does each proposal name an outcome measure?
- Did you avoid replacing one framework's vocabulary with another's?

</details>

## ⚠️ Mistakes and traps
- **Picking one framework for everything.** No single reference answers every operating-model question. Keep your own model and use each reference for the question it answers best.
- **Counting certifications as progress.** Trained staff are inputs. Report outcomes: lead time, stability, cost, audit findings closed.
- **Copying content without checking terms.** Framework text, diagrams and structures are owned. Ask legal first.
- **Assuming the regulator's expectation.** Ask the risk function what the rules actually require.

## 🧾 Recap
- Frameworks differ in kind, and the kind tells you how to use it.
- **Borrow the question, keep your own map.** Your operating model is the map; each framework is a reference for the question it answers best.
- The **framework register** records owner, question, use, internal owner, use decision, terms, term map and evidence of value.
- Four use decisions are enough: reference, selective use, certify against, retire.
- Watch for servant signs: process counts, tools shaped by the book, framework titles, conformance-only audits.

## ✍️ Check yourself
**1. Omar asks the steering group, "Which framework are we following?" What is the most useful response?**

- A. Choose the framework with the most certified staff at the bank and make all teams adopt it.
- B. Tell him the bank follows no framework at all, so the existing ones should be removed.
- C. List the questions the model must answer, and record which reference helps with each one.
- D. Ask the largest supplier which framework it prefers, since it delivers most of the work.

<details><summary>Answer</summary>

**C.** No single framework answers every operating-model question. A treats a count of certifications as a reason, which the lesson calls an input. B throws away useful references, and D hands an internal design decision to a supplier. See "Start from questions, not from frameworks".

</details>

**2. Nour wants the data centre to hold a formal certificate because two corporate clients require one in their contracts. Which use decision fits?**

- A. Certify against a management-system standard, with a tightly defined audit scope.
- B. Selective use of the standard's practices, telling the clients no certificate will be issued.
- C. Certify against the standard for the whole Technology division, so the certificate covers everything.
- D. Reference only, and send the clients a mapping of the bank's practices to the standard.

<details><summary>Answer</summary>

**A.** A contract that requires certification is the classic reason to certify against a standard, and a tight scope keeps the cost and claim honest. B and D do not give the clients what the contract requires. C is tempting but widens the scope: a certificate proves only that its scope conforms, and a division-wide scope costs more without proving more. See "Four use decisions".

</details>

**3. A team proposes using an AI assistant to generate a complete set of "framework-aligned" process documents for the service desk in one afternoon. What is the main concern?**

- A. AI tools cannot write process documents to the quality a regulated bank needs.
- B. The documents would be ready too quickly for the steering group to review them.
- C. The service desk would need new tooling before it could follow any new processes.
- D. It speeds up the servant trap and may reproduce protected wording or structures.

<details><summary>Answer</summary>

**D.** Generated framework content creates conformance documents without outcomes, faster, and may copy owned material. A overstates the tool's limits; the issue is purpose and rights. B and C are not the risks the lesson names. See "Frameworks and AI tools".

</details>

**4. Huda's term map shows that the bank uses "release" to mean making a feature available to customers, while one reference uses a related word differently. What should the bank do?**

- A. Rename the bank's term to match the reference, so that new staff find it familiar.
- B. Keep the bank's meaning, and note where the reference uses the word differently.
- C. Build a crosswalk between the two references and use whichever term wins the vote.
- D. Avoid the word "release" altogether, so that no confusion can arise in future.

<details><summary>Answer</summary>

**B.** The operating model is written in the organisation's words; noting each reference's usage is what a term map does. A lets the framework redesign the bank's vocabulary, C reconciles books with each other, and D removes a word the bank needs. See "Your words, mapped to theirs".

</details>

**5. The quarterly report for the change process says "14 of 16 practices implemented". What would make it a better management report?**

- A. Add the number of staff trained in the framework that the practices came from.
- B. Add a comparison with the number of practices other banks report implementing.
- C. Add the date each practice was implemented and the name of the person responsible.
- D. Replace the count with measures such as change lead time and change fail rate.

<details><summary>Answer</summary>

**D.** A practice count measures conformance; managers need the outcomes each practice protects. A and C add inputs, and B compares conformance counts, which says nothing about this bank's results. See "How to tell you have become the framework's servant".

</details>

## 📚 References
Owners' sites could not be opened from this environment; owners, editions and dates are as reported in search summaries (November 2026), and URLs are as found in search. Check each owner's page for current versions and terms.
- PeopleCert, ITIL: https://www.peoplecert.org/ITIL-4
- ISACA, COBIT: https://www.isaca.org/cobit
- ISO, "ISO/IEC 20000-1:2018 Information technology — Service management — Part 1: Service management system requirements": https://www.iso.org/standard/70636.html
- ISO, "ISO/IEC 38500:2024 Information technology — Governance of IT for the organization": https://www.iso.org/standard/81684.html
- The Open Group, TOGAF Standard page: https://www.opengroup.org/togaf
- The Open Group, IT4IT™ page: https://www.opengroup.org/about-it4it%E2%84%A2
- IFDC, "About VeriSM": https://verism.global/about/
- Scopism, "SIAM Body of Knowledge (BoK)": https://www.scopism.com/products-services/siam-body-of-knowledge-bok/
- FinOps Foundation, "What is FinOps?": https://www.finops.org/introduction/what-is-finops/
- TBM Council, "About the Council": https://www.tbmcouncil.org/about/
- Skelton, M. and Pais, M., *Team Topologies* (IT Revolution, 2019). Full citation.
- Library course: [*Secure AI & Application Security: Zero to Hero*, lesson 11.1 — Frameworks: NIST CSF 2.0, ISO/IEC 27001, NIST SSDF and OWASP SAMM](../secai/index.html#/11.1)
- Library course: [*AI Governance: Zero to Hero*, lesson 7.3 — The global map: other frameworks that shape practice](../aigp/index.html#/7.3)

---

# 12.2 — Assessing where you are: a maturity and evidence review
*Level: 🔴 Advanced* · *Prerequisites: 1.3, 9.3, 10.3, 12.1* · *Step: Improve, Govern*

**After this you can** run an evidence-based review of your IT operating model across twelve capabilities, score each from 0 to 3 only on evidence you have seen, trace a sample of real work end to end, and produce a heat map, a baseline of outcome measures and a statement of the top three constraints. *Study time: reading about 15 min, hands-on about 125 min (estimate).*

## ⚡ In 60 seconds
- An **evidence review** asks "how well do we do this?" for each capability, with one rule: no score without evidence you have seen.
- The rule that matters most: **score what you can show, not what you say.** A policy shows something is defined; only records of real work show it happens.
- Assess **capabilities linked to outcomes**, not a ladder of levels. The aim is to find today's constraint, not to reach "level 4".
- Pair scores with **outcome measures** such as lead time, service levels and unit cost.
- Decision cue: the review is done when you can name the top three constraints, each with evidence, and the owner who will act on each.
- Biggest trap: a generous self-assessment survey presented as a heat map and used to compare teams.

## 🧭 Why it matters
Najm Bank and everyone in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

Six months into the programme, Omar asked for a board progress report. The programme office sent department heads a survey: rate your area from 1 to 5 on twelve capabilities. Product ownership scored 4, change management 4, records 3.

Nour, IT Risk and Controls Lead, was uneasy. Internal audit had just found sampled Cards & Payments changes with no link between change record, deployment and tested build. Reem, Product Manager for Cards & Payments, admitted her "product" was still funded project by project. Omar wanted a review that would hold up if the board, internal audit or the regulator asked "how do you know?". Huda and Nour designed it. This lesson is their method.

## 📐 How it works

### 🟢 The essentials

**Maturity versus capability.** Many maturity models describe levels to climb, implying everyone climbs the same steps and improvement ends at the top. *Accelerate* (Forsgren, Humble and Kim, 2018), which reports DORA's research, is reported to argue for **capabilities, not maturity**: improve the capabilities that move the outcomes you need, and keep going, because technology and business keep changing. This lesson follows that view; the 0–3 scale below shows gaps, it is not a ladder.

**The twelve capabilities.** Use the course's modules as the checklist:

| Capability | Lesson | Question the review answers |
|---|---|---|
| **Value-stream visibility** | 1.1, 1.2 | Can we see lead time and waits for our main value streams? |
| **Product and platform ownership** | 2.1, 2.2 | Does each product and platform have an owner with a funded team? |
| **Service catalogue** | 2.3 | Does the business see a current catalogue with owners and service levels? |
| **Portfolio and funding** | 3.1–3.3 | Is money allocated to products and outcomes, reviewed and re-planned? |
| **Intake and demand** | 4.1, 4.2 | Is there one front door, with decisions at a known cadence? |
| **Pipelines and quality evidence** | 5.1, 5.2 | Do pipelines produce evidence a manager can trust? |
| **Release and change** | 6.1–6.3 | Are changes risk-based, with fast paths for standard changes? |
| **Requests and access** | 7.1, 7.2 | Are common requests self-service with clear entitlements? |
| **Incidents, problems and service levels** | 8.1–8.3 | Do we restore quickly, learn from failure and manage to SLOs? |
| **Records and traceability** | 9.1–9.3 | Can we trace investment to change to running service to incident? |
| **Money, suppliers and controls** | 10.1–10.3 | Do we know product cost, manage suppliers as one service, and evidence controls? |
| **Toolchain and automation** | 11.1–11.3 | Does each record have one system of record, and is AI use controlled? |

**The scale: 0 to 3, on evidence.** Each level is defined by what you can see:

| Score | Meaning | Evidence required |
|---|---|---|
| **0 Absent** | Not done, or done only by individual heroics | Nothing, or only people's descriptions |
| **1 Defined** | Written down: policy, process, role, template | The document, approved and current |
| **2 Practised** | Happens in real work, most of the time | A sample of real records showing it happened |
| **3 Measured and improving** | Measured, reviewed and changed on the results | A measure over time and a decision made because of it |

**For a control, "most of the time" is not enough.** Before sampling, agree a pass bar with the second line (the risk function that oversees IT, lesson 10.3), for example 9 of 10 sampled items complying, with any exception explained. Below the bar, a defined control scores 1.

The scale's key move is separating **defined** (1) from **practised** (2): a common failure in self-assessments is scoring a policy as if it were practice.

**Three sources of evidence.** Use all three and compare them:

- **Artefacts:** documents, records, tool configurations. They show what is defined and what happened.
- **Data:** measures from tools. They show how often and how well.
- **Conversations:** short interviews with people who do the work and those they serve. They explain why.

Disagreement among them is itself a finding.

### 🟡 Going deeper

**Trace a sample of real work.** The most revealing test is to follow a few recent items end to end (lesson 9.3). Take five changes deployed last month for one product and find for each: backlog item and investment, build and quality evidence, change record and approval, deployment record, components affected, and any incident after. Every missing link is evidence for several capabilities. Five items give no statistics, but they show whether records link at all.

**Outcome baseline.** Record a few outcome measures, with source and date, for the roadmap (12.3) to move:

| Outcome area | Example measures | Source lesson |
|---|---|---|
| **Flow** | Lead time from approved idea to customer use | 1.2 |
| **Delivery** | DORA's software delivery measures | 1.3 |
| **Reliability** | SLO attainment and time to restore | 8.3 |
| **Cost** | Cost per product and one or two unit costs | 10.1 |
| **Control** | Open audit findings by age; control tests passed | 10.3 |
| **People** | Staff and user satisfaction from existing surveys | 2.2, 7.1 |

DORA's online Quick Check is reported to use five questions and to be meant as a conversation starter for one team and one service. Treat it as one input, not as the review.

**Running the review.** A practical sequence:

1. **Scope and sponsor.** Agree with the CIO the scope and who signs off the findings.
2. **Evidence request.** Ask each capability owner for evidence, not scores.
3. **Sample trace.** Trace two or three products end to end.
4. **Data pull.** Extract the outcome measures, with caveats.
5. **Conversations.** Short interviews, including people who consume IT services.
6. **Calibration.** A panel (for example, enterprise architecture and the second-line liaison) agrees scores across capabilities, so a 2 means the same everywhere.
7. **Findings.** Heat map, outcome baseline and the top three constraints, each with evidence and an owner.

**Finding the constraint.** You cannot fix every gap. Look for the **constraint**: the capability whose weakness limits outcomes most, often because others depend on it. Weak records weaken change, controls, cost and incident learning at once. Write each constraint as a sentence: "Because X, we cannot Y, as shown by Z."

### 🔴 Expert view

**The review must survive "how do you know?".** If the board, internal audit or a supervisor might read the results, design the review like a control test (lesson 10.3): documented method, defined scale, sampled evidence, calibration, and a record of who decided each score. Ask internal audit early whether they would rely on it. Never present a self-assessment survey as an independent review.

**Do not turn scores into targets.** Once the board sees a heat map, managers will want to improve their colour, which can reward writing documents (0 to 1) instead of changing practice (1 to 2). Rule: **only outcome measures go on the board's dashboard**; capability scores stay with the teams as a diagnostic. And never rank teams against each other on scores or on DORA measures; lesson 1.3 explains why DORA's own guidance warns against that use.

**Assessing with AI help.** AI tools can collate evidence fast, and can also invent a plausible link that does not exist. Use them to find and organise evidence; have a person check every item that changes a score, and record in the method how AI was used and checked (lesson 11.3).

**Repeat, but not too often.** This course suggests a full review yearly, with a light quarterly re-score of the top three constraints.

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Capability list** | Twelve capabilities, each with its question and source lesson | At the start; adapt once and keep stable |
| **Evidence scale** | 0–3, each level with the evidence it requires, plus the control pass bar | For every score; publish it with the results |
| **Evidence request** | A short form asking owners for artefacts and samples, not self-scores | Week one of the review |
| **Sample trace sheet** | Per sampled change: investment, backlog item, build evidence, change, deployment, components, incidents | To test records, change and controls together |
| **Outcome baseline sheet** | Flow, delivery, reliability, cost, control and people measures, with source and date | Before the roadmap; repeat at each review |
| **Heat map and constraint statements** | Scores on one page, plus "Because X, we cannot Y, as shown by Z" for the top three | To report findings and hand them to the roadmap |

For a security programme's version of the same idea, see [*Secure AI & Application Security: Zero to Hero*, lesson 11.3 — Building a security programme and culture: champions, metrics and budgets](../secai/index.html#/11.3).

## 🏛️ In practice at Najm Bank
Huda and Nour ran a five-week review: five traced changes each from Cards & Payments and the corporate lending platform, outcome data for both, and twenty interviews. Illustrative, fictional extract:

| Capability | Survey score (1–5) | Evidence score (0–3) | Key evidence |
|---|---|---|---|
| Product and platform ownership | 4 | 1 | Product owners named; funding still per project, no product budget (portfolio records) |
| Release and change | 4 | 1 | Policy current; 4 of 10 sampled changes had approvals recorded after deployment, against an agreed bar of 9 of 10 |
| Records and traceability | 3 | 1 | 3 of 10 sampled changes linked from backlog item to deployment record (Cards 1 of 5, lending 2 of 5) |
| Incidents, problems and service levels | 3 | 2 | Major-incident reviews held for all major incidents in the quarter; SLOs exist for 2 services only |
| Pipelines and quality evidence | 3 | 2 | Pipeline stores test and scan evidence for Cards; lending platform builds by hand |
| Portfolio and funding | 3 | 1 | Quarterly review defined; no work stopped or re-planned in the past year |

The constraint statements:

1. Because the portfolio funds projects, product owners cannot move money to the most valuable work, as shown by twelve change requests to business cases last year.
2. Because change, deployment and backlog records are not linked, we cannot show what is running and why, as shown by 3 of 10 traceable samples.
3. Because the lending platform has no managed pipeline, its changes are slow and carry no quality evidence, as shown by a change lead time (approved change to production) of about 40 days against about 9 for Cards.

Yousef challenged the change score; Nour showed him the samples, and he asked to own the fix. Omar took only the outcome baseline and the three constraints to the board.

## 🛠️ Exercises
**🟢 Re-score with evidence.** Take one capability your organisation rates itself on (or use "release and change"). Write its current self-rating, then score it 0–3 on the evidence scale, listing each artefact or record you looked at.
*Done when:* one capability has an evidence score with at least three named pieces of evidence, and a sentence explaining any gap from the self-rating.

<details><summary>Model answer and self-check</summary>

**Model answer.** "Release and change: self-rating 4 of 5. Evidence: the change policy (current: supports 1); 10 change records from last month (6 with approvals before deployment, below the agreed control bar of 9 of 10, so not 2); no change-outcome measure reviewed in any meeting minutes (so not 3). Evidence score: 1. Gap: the self-rating counted the policy as practice."

**Self-check.**
- Did each piece of evidence come from a record you saw?
- Did you keep "defined" and "practised" apart, using a pass bar for controls?
- Did you avoid scoring 3 without a measure and a decision on it?

</details>

**🟡 Trace five items.** Pick five recent changes for one product and trace each end to end: investment, backlog item, build evidence, change record, deployment, running components, any incident after.
*Done when:* a sample trace sheet has five rows with each link marked found, missing or partial, and a count of fully traceable items.

<details><summary>Model answer and self-check</summary>

**Model answer.** Five rows, seven link columns. A typical mid-change result: build evidence for all five; change records for all five but linked to the backlog item for two; deployment linked to change for three; running components identified for one; investment link for none. Fully traceable: zero of five. Finding: records exist but do not link, which affects records, change, controls and cost at once.

**Self-check.**
- Did you choose the five items before looking at them?
- Did you mark "partial" where a link exists only in free text?
- Did you note which capability each missing link affects?

</details>

**🔴 Write the constraint statements.** Using a full or partial heat map and your outcome baseline, write the top three constraints in the form "Because X, we cannot Y, as shown by Z", and name an owner for each.
*Done when:* three statements exist, each citing evidence and an outcome measure, each with a named owner, and none is simply "low score on capability N".

<details><summary>Model answer and self-check</summary>

**Model answer.** "Because a weekly board approves changes at all risk levels, we cannot deploy low-risk fixes in under a week, as shown by a median change lead time of 8 days and 70% of changes classed as low risk (illustrative). Owner: Head of IT Operations." Two more follow the same form, typically on funding and records.

**Self-check.**
- Does each name a cause, an effect on outcomes and evidence?
- Are the three really different constraints?
- Can each owner change the cause?

</details>

## ⚠️ Mistakes and traps
- **Survey scores presented as findings.** Self-ratings can be generous. Ask for evidence and sample real work.
- **Scoring policy as practice.** A current document earns "defined". Only records of real work earn "practised".
- **Climbing levels for their own sake.** Remove the constraint on outcomes instead.
- **Putting capability scores on the board's dashboard.** They become targets. Show outcomes to the board; keep scores as a diagnostic.
- **Comparing teams in a league table.** It rewards gaming. Compare each area with itself over time.
- **Trusting AI-collated evidence unchecked.** Have a person verify anything that changes a score.

## 🧾 Recap
- An evidence review scores capabilities only on what can be shown: **score what you can show, not what you say.**
- Use a short list of capabilities from your operating model and a 0–3 scale that separates **defined** from **practised**.
- Combine artefacts, data and conversations, and trace a small sample of real work end to end.
- Pair scores with an **outcome baseline**, and name the top three **constraints** with evidence and owners.
- Show the board outcomes, not scores; never rank teams; design the review to survive "how do you know?".

## ✍️ Check yourself
**1. The survey rates change management 4 of 5, and the policy is current. Nour agreed a bar of 9 of 10 with the second line; her sample shows 4 of 10 changes approved after deployment. What evidence score fits?**

- A. 3, because the policy is current and approved, and the change board meets weekly.
- B. 1, because the process is defined, but the sample shows it is not consistently practised.
- C. 2, because more than half of the sampled changes were approved before deployment.
- D. 0, because any late approval means the process does not exist in any meaningful way.

<details><summary>Answer</summary>

**B.** A current policy earns "defined", and 6 of 10 compliant is below the agreed bar of 9 of 10, so the control is not yet "practised". C is tempting because 6 of 10 is a majority, but for a control the lesson sets the bar in advance, not at "most of the time". A scores policy as measurement, and D ignores the defined policy. See "The scale: 0 to 3, on evidence".

</details>

**2. A consultant offers Omar a five-level maturity ladder and a target of "level 4 in every capability by year end". What should Huda propose instead?**

- A. A target of level 3 in every capability, which is more realistic for a division mid-change.
- B. The consultant's ladder, scored on evidence rather than self-rating, with the same target.
- C. A target only for the lowest-scoring capability, whatever outcomes the bank needs to move.
- D. Improve the capabilities that limit the outcomes the bank needs, and keep improving.

<details><summary>Answer</summary>

**D.** The capability view, reported from *Accelerate*, improves the capabilities that move needed outcomes, and keeps going. A and B still aim at a level everywhere; evidence scoring does not fix that. C is tempting, but the lowest score is not always the constraint on outcomes. See "Maturity versus capability" and "Finding the constraint".

</details>

**3. Huda wants one test that reveals weaknesses in records, change and controls at the same time. What should she do?**

- A. Trace a small sample of recent changes end to end through their linked records.
- B. Send a longer survey with separate questions for records, change and controls.
- C. Ask the tool vendor for a report on how many processes are configured in the tool.
- D. Interview each department head about the links they believe their records have.

<details><summary>Answer</summary>

**A.** Following real work through its records shows every missing link, each tied to several capabilities. B and D collect opinions, and C counts configuration, not practice. See "Trace a sample of real work".

</details>

**4. Omar is preparing the board report after the review. What should go on the board's dashboard?**

- A. The full heat map of capability scores, coloured by department, to show where effort goes.
- B. A ranking of product teams by their DORA measures, to encourage healthy competition.
- C. Outcome measures from the baseline, plus the top constraints and their named owners.
- D. The number of documents written since the last review, as proof of visible progress.

<details><summary>Answer</summary>

**C.** Outcomes and named constraints are what the board needs; capability scores stay as a diagnostic so they do not become targets. A turns scores into targets, B ranks teams, which the lesson warns against, and D rewards documents over practice. See "Do not turn scores into targets".

</details>

**5. The team used an AI assistant to scan 200 change records for missing links. It flagged 30 records as fully linked that Nour had not seen. What should happen before scores change?**

- A. A person checks the flagged records, and the method records how the AI was used.
- B. Scores change at once, since the assistant scanned far more records than people.
- C. A person spot-checks five of the 30, and if those hold, the rest are accepted.
- D. The scores change, and the method notes that an AI assistant was used for the scan.

<details><summary>Answer</summary>

**A.** AI can report links that do not exist; a person verifies anything that changes a score, and the method records the use. B trusts it unchecked. C and D are tempting but leave unchecked items changing scores; D records the AI use without the check. See "Assessing with AI help".

</details>

## 📚 References
- Forsgren, N., Humble, J. and Kim, G., *Accelerate: The Science of Lean Software and DevOps* (IT Revolution, 2018). Full citation; the "capabilities, not maturity" argument is as reported in search summaries of excerpts, and the book was not opened for this lesson.
- DORA, "Take the DORA Quick Check" (five questions and conversation-starter purpose as reported in search summaries; not opened): https://dora.dev/quickcheck/
- DORA, "DORA's software delivery performance metrics" (as reported; not opened): https://dora.dev/guides/dora-metrics/
- Library course: [*Secure AI & Application Security: Zero to Hero*, lesson 11.3 — Building a security programme and culture: champions, metrics and budgets](../secai/index.html#/11.3)

---

# 12.3 — A transformation roadmap and leading the change
*Level: 🔴 Advanced* · *Prerequisites: 3.3, 12.1, 12.2* · *Step: Improve, Govern*

**After this you can** write a 12–18-month transformation roadmap in three waves, each with the outcome it must move, a pilot value stream, the things to stop doing, the decisions and records it needs, and a stop-or-continue review; and pair it with a change-leadership plan that names the sponsor's actions, the managers' role, what changes for each affected group, and how resistance is heard. *Study time: reading about 20 min, hands-on about 120 min (estimate).*

## ⚡ In 60 seconds
- A **transformation roadmap** is a plan of outcome-driven waves, not a list of deliverables.
- The rule that matters most: **change one value stream end to end before changing one layer everywhere.**
- Sequence by dependency: funding and ownership before renaming roles; records and definitions before tool replacements; a working pilot before scaling.
- Plan for a possible **dip before the gain** (this course's advice); explain it in advance and measure through it.
- Middle managers decide whether change happens. Give each affected group answers to five questions.
- Biggest trap: announcing the target model, renaming everyone, and calling it done.

## 🧭 Why it matters
Najm Bank and everyone in it are fictional. All numbers about Najm Bank in this lesson are illustrative figures, not benchmarks.

With the 12.2 review in hand, Omar wanted to move quickly. A consultancy's plan had 47 workstreams starting together in January: a new service platform, new job titles, a scaled agile rollout, a CMDB (configuration management database, the record of what is running; lesson 9.2) clean-up and a cost model. Lina, Vendor and Sourcing Manager, counted six suppliers changing processes at once.

Yousef said what many thought: "If everything changes at once and something breaks, nobody will know which change broke it." Huda agreed with the destination, not the route. She proposed three waves over eighteen months, one pilot value stream to prove the model, and things to stop in each wave. Omar's job was to keep priorities stable and be seen leading. This lesson shows how.

## 📐 How it works

### 🟢 The essentials

**Outcomes, not deliverables.** A deliverable roadmap says "Q2: new service platform live". An outcome roadmap says "by end of wave 1: Cards & Payments change lead time halved, with nearly every change traceable". If the tool goes live and the outcome does not move, the wave is not done.

**The shape of a wave.** Each wave has seven parts:

| Part | What to write |
|---|---|
| **Outcome** | One or two baseline measures (12.2) to move, with a target range |
| **Constraint addressed** | Which top constraint from the review it attacks |
| **Where** | Value streams, products or departments in scope |
| **Changes** | Funding, roles, process, records, tools, suppliers |
| **Stops** | Reports, meetings, approvals or tools that stop |
| **Decisions and records** | Decision rights and records the change needs (lessons 9.1, 10.3) |
| **Review** | Date, measures and who decides to continue, adjust or stop |

The **Stops** row is most often left empty. If nothing old stops, the new practice is added on top and people drift back.

**Pilot first: one value stream end to end.** Choose a pilot important enough to matter, small enough to change in months, and led by willing people. Change every layer together: product funding, a stable team, a managed pipeline, a risk-based change path, linked records, catalogue entries with SLOs, and a cost view. The pilot proves the pieces fit and produces numbers others can believe.

**Sequencing rules.** Dependencies decide order:

| Rule | Why |
|---|---|
| **Funding and ownership before renaming** | A product manager without a product budget is a project manager renamed (lesson 3.2) |
| **Definitions and records before tools** | A new tool on undefined records copies old confusion faster (lessons 9.1, 11.2) |
| **Risk-based change before more deployments** | Faster pipelines into a weekly board create queues (lesson 6.2) |
| **One working pilot before scaling** | Scaling an untested model multiplies its defects |
| **Controls redesigned with the second line** | Late controls block go-live (lesson 10.3) |
| **Suppliers in the plan, not informed of it** | Supplier contracts often set the real pace (lesson 10.2) |

### 🟡 Going deeper

**Three waves, a typical shape.**

| Wave | Typical focus | Typical outcomes to move |
|---|---|---|
| **Wave 1: prove** (months 0–6) | One pilot value stream end to end | Lead time, change fail rate and traceability for the pilot |
| **Wave 2: extend** (months 6–12) | Two to four more value streams; platform as a product; a portfolio review that can stop work | Same measures; share of spend funded as products; SLO attainment |
| **Wave 3: embed** (months 12–18) | Remaining value streams; cost per product; supplier contracts; tool rationalisation; retire old boards | Unit costs; audit findings closed; reports and tools retired |

Treat the dates as a hypothesis; each wave review can move the next wave's scope.

**Plan for the dip.** DORA's announcement of its 2024 report says that implementing a platform engineering initiative "might lead to a temporary decrease in performance before improvements manifest as the platform matures". That finding is about platform engineering. This course's advice is to plan for a similar possible dip in any operating-model change: tell the sponsor and business in advance, agree what size and length of dip triggers a review, and keep the old path available until the new one is proven.

**Keep priorities stable.** The same 2024 announcement says that "instability in priorities, even with strong leadership, comprehensive documentation, and a user-centered approach — all known to be highly beneficial — can significantly hinder progress". So fix each wave's scope at its start, change it only at wave reviews barring an emergency, and make the sponsor the person who says no mid-wave.

**AI amplifies what is already there.** DORA's announcement of its 2025 report says: "AI doesn't fix a team; it amplifies what's already there." It also reports a direct correlation between a high-quality internal platform and an organisation's ability to unlock the value of AI. So add AI tools where pipeline, records and controls are already sound (lesson 11.3).

**Governing the transformation itself.** Govern the roadmap like a portfolio (lesson 3.3): a monthly **transformation board** chaired by the sponsor, a **decision log** of scope changes and exceptions, and **wave reviews** that can stop a failing workstream. Ask the risk function early whether any change (to outsourcing or critical services, say) needs notifying to the supervisor. Do not assume.

### 🔴 Expert view

**Leading the change: five questions every person asks.** Published change models include John Kotter's eight-step process, from his 1996 book *Leading Change*, which works at the level of the organisation, and Prosci's ADKAR® model, which describes individual change through five elements. This course follows neither; it uses one plain test. Each affected group must be able to answer five questions:

| Question | What leaders provide |
|---|---|
| **Why now?** | The outcome problem in numbers from the 12.2 baseline, explained by the sponsor in person |
| **What changes for me?** | A one-page "before and after" per group: decisions, meetings, records, tools |
| **What do I stop doing?** | The wave's Stops list, explicitly |
| **Who helps me learn?** | Named coaches, time set aside, practice on real work |
| **How will we know it worked?** | The outcome measures, shown openly at each review, even when worse |

Where a group cannot answer one, expect resistance, usually reasonable.

**Middle managers decide.** Sponsors announce change; middle managers make it happen or quietly stop it, and their own roles often change most. Involve them in designing their part, give them their "before and after" first, and settle grades and titles with HR before announcing. Never promise what HR has not agreed.

**Turn sceptics into owners.** The person most worried about a change often knows its real risk. Give them ownership of the part that addresses it, with authority to stop it if the risk appears. A **resistance log** records concerns, who raised them, the answer and any change made; reviewing it at the board shows people they were heard.

**Sponsor behaviour is the message.** People watch what the sponsor does: attending pilot reviews, refusing a mid-wave initiative, talking openly about the dip. A sponsor who still asks for the old status report signals the old model is the real one.

For enterprise adoption, see [*AI Product Management: Zero to Hero*, lesson 7.3 — Adoption and change management inside the enterprise](../aipm/index.html#/7.3); for roadmaps under uncertainty, see [*AI Product Management: Zero to Hero*, lesson 9.2 — Roadmaps under uncertainty: bets, platforms and model change](../aipm/index.html#/9.2).

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Wave sheet** | One page per wave with the seven parts | For each wave, before it starts |
| **Sequencing checklist** | The six dependency rules, checked against each wave | Before approving the roadmap |
| **Before-and-after sheet** | Per affected group: decisions, meetings, records and tools | Before announcing each wave to that group |
| **Five-questions check** | The five questions, answered per group | Before and during each wave |
| **Resistance log and decision log** | Concerns and answers; scope changes and exceptions, with who decided | Reviewed at each transformation board |

## 🏛️ In practice at Najm Bank
Omar adopted Huda's three-wave roadmap. Illustrative, fictional extract of wave 1:

| Part | Wave 1: prove (months 0–6) |
|---|---|
| **Outcome** | Cards & Payments: change lead time from about 9 days to 3–5 days; traceable sampled changes from 1 of 5 (the Cards share of the 12.2 trace) to at least 9 of 10; change fail rate not worse than baseline |
| **Constraint addressed** | Project funding (constraint 1) and unlinked records (constraint 2), for the pilot only |
| **Where** | Cards & Payments value stream: three teams, two suppliers |
| **Changes** | Product budget agreed with Tariq; risk-based change path with a catalogue of standard changes (pre-approved, low-risk change types; lesson 6.2) owned by Yousef; linked backlog, build, change and deployment records designed by Huda; the Cards service catalogue entry published by Yousef with two SLOs; a first Cards cost view from Tariq; new change-notification terms with both suppliers, agreed by Lina |
| **Stops** | Weekly change board for Cards' standard changes; the monthly project status report for Cards; the separate supplier change spreadsheet |
| **Decisions and records** | Reem can move up to an agreed share of the Cards budget between features; Nour agrees the control redesign and the evidence the auditors will test |
| **Review** | Month 6, transformation board: continue to wave 2, adjust, or stop |

The leadership plan named Omar's actions: open each wave in person, attend two pilot reviews, and refuse mid-wave initiatives (he refused two, and said why). Yousef, the loudest sceptic, owned the standard-change catalogue, with authority to put any change type back on the board if failures rose.

In weeks three to six, Cards' lead time got worse while teams learned; Omar had warned the board. By month six, lead time was about 4 days and 9 of 10 sampled changes were traceable (illustrative figures). The board approved wave 2 but moved one value stream to wave 3, because its supplier contract could not change in time.

## 🛠️ Exercises
**🟢 Write the Stops list.** For one planned improvement (or wave 1 at Najm Bank), list at least three things that will stop, and who must agree to each.
*Done when:* a list of at least three Stops exists, each with the person who must agree and the date it stops.

<details><summary>Model answer and self-check</summary>

**Model answer.** For a pilot moving to risk-based change: stop the weekly change board for standard changes (Head of IT Operations, month 2); stop the monthly project status report (portfolio office and CIO, month 1); stop the supplier change spreadsheet (vendor manager and suppliers, month 2, once the change record replaces it).

**Self-check.**
- Do people actually spend time on each item today?
- Does each have someone with authority to stop it?
- Is there a date, not "eventually"?

</details>

**🟡 Draft the three waves.** Using a constraint from your own review (or from 12.2 at Najm Bank), write a wave sheet with all seven parts for a pilot value stream. Then sketch waves 2 and 3 on one page: focus, outcome measures, value streams in scope, and what each depends on from the wave before. Check all three waves against the sequencing checklist.
*Done when:* wave 1 has all seven parts (a baselined outcome with target range, changes across at least three layers, at least three Stops, a dated review that can stop it); three dated waves span 12–18 months, each with an outcome measure and a review date; and each of the six sequencing rules is marked met or not met, with a reason for any rule not met.

<details><summary>Model answer and self-check</summary>

**Model answer.** Wave 1 (months 0–6) shaped like the Najm Bank extract, with changes in funding, change process, records, catalogue and SLOs, cost view and supplier terms, and a month-6 review. Wave 2 (months 6–12): three more value streams including the lending platform, which first needs a managed pipeline; measures: lead time, traceability, share of spend funded as products; depends on wave 1's change model and records design; review month 12. Wave 3 (months 12–18): remaining value streams, supplier contracts, tool rationalisation; measures: unit costs, audit findings closed, reports retired; review month 18. Checklist: all six rules met except "suppliers in the plan" for one wave-2 supplier whose contract renews late, so that value stream moves to wave 3.

**Self-check.**
- Does each wave's outcome come from a baseline you can measure today?
- Does the pilot change several layers together, not one?
- Is every sequencing rule marked, with a reason where it is not met?

</details>

**🔴 Plan the people side.** For the same wave, write a before-and-after sheet for one affected group and answer the five questions for them. Name the sceptic you expect, what part you would give them to own, and two visible actions for the sponsor.
*Done when:* the sheet exists, all five questions have specific answers, the sceptic has ownership with authority, and two sponsor actions have dates.

<details><summary>Model answer and self-check</summary>

**Model answer.** Group: change managers. Before: a weekly board reviewing every change. After: they own the standard-change catalogue, review normal changes by risk and analyse failures monthly. Why now: 9-day change lead time. What stops: the weekly board for standard changes. Who helps: a platform coach, four hours a week for two months. How we know: lead time and change fail rate. Sceptic: the head of operations, owning the catalogue with authority to return any change type to full review. Sponsor: opens the wave on day one; attends the month-3 review.

**Self-check.**
- Would someone in that group recognise their own week in the sheet?
- Are the answers specific, not slogans?
- Does the sceptic have real authority, not a token role?

</details>

## ⚠️ Mistakes and traps
- **A deliverable roadmap.** "Tool live in Q2" can succeed while nothing improves. Write each wave as an outcome to move, with a baseline.
- **No Stops list.** New practices on top of old ones double the work, and people drift back. Stop something in every wave.
- **Hiding the dip.** Explain it in advance and set a review trigger.
- **Shifting priorities mid-wave.** Fix scope per wave; change it at reviews.
- **Leading by announcement.** Slides and new titles are not change. Answer the five questions for each group and involve middle managers early.

## 🧾 Recap
- A transformation roadmap is a sequence of **outcome-driven waves**, each with Stops and a review.
- **Change one value stream end to end before changing one layer everywhere**; scale only a model that has worked.
- Sequence by dependency: funding before titles, records before tools, controls and suppliers inside the plan.
- Plan for a possible dip, keep priorities stable, and add AI tools where foundations are sound.
- Lead people with five answered questions, middle managers as designers, sceptics as owners and a sponsor whose actions match the plan.

## ✍️ Check yourself
**1. The consultancy's plan starts 47 workstreams in January. Which change to its shape best follows this lesson?**

- A. Keep all 47 workstreams but add a second programme office to manage the reporting load.
- B. Start with the tool workstreams first, since tools are the easiest part to measure early.
- C. Run the workstreams in alphabetical order, so that each department has a predictable slot.
- D. Prove the model in one value stream across every layer, then extend it in later waves.

<details><summary>Answer</summary>

**D.** A thin slice through every layer tests the model before it scales. A adds governance to the same risk, B puts tools before records, and C sequences by name, not dependency. See "Pilot first: one value stream end to end".

</details>

**2. Reem has been made a "product manager", but every budget change still needs a new business case. Which sequencing rule has been broken?**

- A. Definitions and records before tools.
- B. Funding and ownership before renaming.
- C. Risk-based change before more deployments.
- D. Suppliers in the plan, not informed of it.

<details><summary>Answer</summary>

**B.** A product manager without a product budget is a project manager with a new title. The other rules address different dependencies. See "Sequencing rules".

</details>

**3. In weeks three to six of wave 1, Cards' lead time gets worse. What should have been done beforehand?**

- A. Shorten the pilot from six months to three, so that any slowdown ends sooner.
- B. Report lead time to the board only at the month-6 review, once the new path settles.
- C. Warn the sponsor and board of a likely dip and agree what size would trigger a review.
- D. Switch the pilot to a different value stream, since this one is clearly not suitable.

<details><summary>Answer</summary>

**C.** The course advises planning for a possible dip (DORA reported one for platform engineering initiatives in 2024); explaining it in advance and agreeing a review trigger keeps trust. A cuts the time the pilot needs to prove the model without managing the dip. B is tempting but hides evidence the board needs to judge the dip, and D abandons the pilot without a review. See "Plan for the dip".

</details>

**4. Yousef is openly sceptical of the new change path. What does the lesson recommend?**

- A. Give him ownership of the standard-change catalogue, with authority to pull change types back.
- B. Move him out of the programme so that his doubts do not slow the pilot's early progress.
- C. Ask him to sign a statement of support before the wave begins, so the board sees unity.
- D. Wait for the month-6 review, when the measures will either convince him or prove him right.

<details><summary>Answer</summary>

**A.** The sceptic often knows the real risk; giving him that part, with authority, turns the concern into a control. B loses that knowledge, C buys agreement without addressing the concern, and D leaves resistance unheard for months. See "Turn sceptics into owners".

</details>

**5. Midway through wave 1, a business unit asks Omar to add a new chatbot project to the pilot team's scope. What should he do?**

- A. Accept it, because new initiatives show the business that the transformation is working.
- B. Decline it for this wave and bring it to the wave review, to keep priorities stable.
- C. Accept it, but ask the pilot team to fit it in alongside the work already planned.
- D. Accept it, but only if the business unit funds an extra person for the pilot team.

<details><summary>Answer</summary>

**B.** DORA's 2024 announcement reports that instability in priorities can significantly hinder progress; the sponsor protects each wave's scope and considers changes at reviews. A and C add work mid-wave. D is tempting, but extra money still changes the pilot's scope and focus mid-wave. See "Keep priorities stable".

</details>

## 📚 References
- Harvey, N. and DeBellis, D., "Highlights from the 10th DORA report" (announcing the 2024 DORA report), Google Cloud blog, 22 October 2024 (opened 2026-11-20; source of the quotes on the temporary decrease in performance and on instability in priorities): https://cloud.google.com/blog/products/devops-sre/announcing-the-2024-dora-report
- Harvey, N. and DeBellis, D., "Announcing the 2025 DORA Report: State of AI-Assisted Software Development", Google Cloud blog, 23 September 2025 (opened 2026-11-20; source of the "amplifies" quote and the platform finding): https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report
- Kotter, J. P., *Leading Change* (Harvard Business School Press, 1996). Full citation; the eight-step process as reported in search summaries.
- Prosci, "ADKAR vs Kotter" (ADKAR's five elements and its individual focus as reported in search summaries; not opened): https://prosci.com/blog/adkar-vs-kotter
- Library course: [*AI Product Management: Zero to Hero*, lesson 7.3 — Adoption and change management inside the enterprise](../aipm/index.html#/7.3)
- Library course: [*AI Product Management: Zero to Hero*, lesson 9.2 — Roadmaps under uncertainty: bets, platforms and model change](../aipm/index.html#/9.2)
