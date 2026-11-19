# Running IT as a Business — authoring guide

This is the contract every lesson follows. It is not published.

## What the course is

A free, bilingual (English/Arabic) course on **running an IT organisation as a business**: how value flows from an investment idea to a product customers use and back again as data, and how to design the operating model, records, tools, money and governance that make that flow fast, safe and visible. Full title: *Running IT as a Business: Products, Value Streams and the IT Operating Model*. Arabic: «إدارة تقنية المعلومات كعمل تجاري: المنتجات ومسارات القيمة ونموذج التشغيل».

- **Audience:** IT managers, enterprise and solution architects, heads of IT operations, service and delivery managers, IT finance and vendor managers, and engineers moving into those roles. Some IT background is assumed; every term is still defined on first use.
- **Not** an engineering course. Delivery pipelines, testing, cloud, observability, security, data and AI engineering are taught elsewhere in the library. Teach the **operating-model view** (who decides, what record proves it, how it is measured, how it is funded and governed) and link out for depth.
- **Original, not derived from any one framework.** This course is written from general management and engineering practice (lean value-stream thinking, product management, service management, DevOps research, IT financial management, enterprise architecture). It is **not** based on, derived from, or aligned with any proprietary standard or certification, and it is **not** training for any exam.
  - In particular it is **not** based on The Open Group IT4IT™ Standard. The Open Group's terms prohibit creating material derived from its standards with AI tools without written permission, and treat IT4IT-based training as commercial use needing a licence. So: **never** describe the IT4IT standard's internal structure (its value-stream names, functional components, data objects, backbones or levels); **never** organise a lesson around them; **never** use "IT4IT" in a title, heading, toolkit name or quiz item. The only place IT4IT appears is lesson 12.1 (the frameworks landscape), where it is named factually as "The Open Group IT4IT™ Standard, a reference architecture for managing the business of IT" with the ™ at first use, the attribution "IT4IT is a trademark of The Open Group", and a pointer to The Open Group's own site. Do not quote it, paraphrase its content, or say this course covers it.
  - The same caution applies to other proprietary bodies of knowledge (ITIL®, COBIT®, TOGAF®, SAFe®, VeriSM™, TBM, FinOps Framework and others): name them factually, say in one line what they are for, add the owner and mark (® or ™) at first use where the owner uses one, link to the owner's page, and never copy their structures, diagrams or wording. Teach the underlying ideas in this course's own words and structure. Lesson 12.1 is the one place that compares them.
- **Honest, practical, no hype.** Every lesson leaves the reader with a decision made or an artefact produced: a value-stream map, a product canvas, a portfolio board, a funding memo, an intake form, a release policy, a change model, a service catalogue entry, an SLO sheet, a cost model, a vendor scorecard, a control matrix, a toolchain map, a maturity assessment, a roadmap.
- **Not professional advice.** Accounting, procurement law, regulation and audit vary by country and organisation. Teach the concepts and the questions to ask finance, legal, risk or the regulator; never state a legal or accounting conclusion.

## The running case: Najm Bank IT

**Najm Bank** is the library's fictional mid-sized Gulf bank (retail, SME and corporate banking). Say it is fictional in lesson 0.2. Here we sit in its **Technology division** (about 600 staff plus suppliers), which is moving from a project-and-ticket IT department to a product-aligned one. Cast (use consistently; each makes realistic mistakes the reader learns from):

- **Omar** — Chief Information Officer. Sponsor of the change; under pressure from the board on cost and outages.
- **Huda** — Head of Enterprise Architecture. Owns the target operating model and the records design.
- **Yousef** — Head of IT Operations (service desk, operations centre, infrastructure). Sceptical of "product" talk; cares about stability.
- **Reem** — Product Manager for the Cards & Payments digital product.
- **Sami** — Platform Engineering Lead (pipelines, environments, internal developer platform).
- **Tariq** — IT Finance Business Partner (budgets, cost allocation, business cases).
- **Lina** — Vendor and Sourcing Manager (contracts, suppliers, multi-supplier integration).
- **Nour** — IT Risk and Controls Lead (second line liaison, audit, regulatory reporting).

Other Najm Bank people from the library may appear briefly where a lesson links to their course (for example the bank's data protection officer, «مسؤول حماية البيانات», in AIGP). Numbers about Najm Bank (budgets, headcount, counts, timings) are **illustrative figures, not benchmarks** and must be labelled so the first time they appear in a lesson.

Regulation: Najm Bank is supervised by a central bank. Where a lesson needs a regulatory example, prefer the clauses the library has already verified (the QCB Artificial Intelligence Guideline, in force 4 September 2024, as cited in `../aipm/` and `../aigp/`), and otherwise name the *kind* of rule (outsourcing, operational resilience, technology risk, data protection) and the question to ask the risk function. Never invent a regulation, article or date.

## Reusing the library (the main design rule)

Do not re-teach the library. Teach the operating-model decision here and link out for depth with a relative link in the form `[*Cloud & DevOps: Zero to Hero*, lesson 4.2 — …](../cloud/index.html#/4.2)`. Rules:

- Link only to lessons that exist: check the heading in the target file (`../<course>/modules/*.md`) before linking. Use the link text "*Course name*, lesson N.M — title".
- Course folders and anchors: `vibe` (`../vibe/index.en.html#lN-M`), and `saas`, `aigp`, `aipm`, `secai`, `career`, `data`, `cloud`, `testing`, `aiapps`, `ainative`, `founder` (`../<course>/index.html#/N.M`).
- Likely links: delivery pipelines and release (`cloud`, `vibe` 4.x), testing and quality gates (`testing`), observability and incidents (`cloud`, `vibe` 7.x), security and third-party risk (`secai`), AI governance and the QCB guideline (`aigp`, `aipm`), data platforms (`data`), AI agents in delivery (`ainative`, `aiapps`), product discovery (`aipm`).

## Steps (the lesson tag)

Every lesson is tagged with one or two steps of the IT operating cycle, in English in both languages: **Plan · Fund · Build · Release · Serve · Run · Govern · Improve**. Header: `*Step: Plan, Fund*`. These are this course's own words, chosen to be plain; they are not any framework's terms.

## Module and lesson plan (numbers are fixed)

| Module | File | Lessons |
|---|---|---|
| 0 Orientation | 00-orientation.md | 0.1 What it means to run IT as a business, and what digital products and AI change · 0.2 Meet Najm Bank's Technology division and the eight steps · 0.3 How to use this course, and what it is not |
| 1 Value and flow | 01-value.md | 1.1 From projects to value: outcomes, value streams and flow · 1.2 Mapping a value stream end to end: lead time, waits and hand-offs · 1.3 Flow and delivery metrics that matter, and the ones that mislead |
| 2 Products, services and the operating model | 02-model.md | 2.1 Digital products, services and projects: what each is and who owns it · 2.2 Designing a product-aligned operating model: product, platform and enabling teams · 2.3 The service catalogue: the offer the business actually sees |
| 3 Strategy and portfolio | 03-portfolio.md | 3.1 From strategy to an investment portfolio · 3.2 Prioritising and funding work: business cases, cost of delay and funding products not projects · 3.3 Portfolio governance: reviewing, re-planning and stopping work |
| 4 Demand and requirements | 04-demand.md | 4.1 Intake and demand management: one front door for ideas and requests · 4.2 From requirement to backlog, with traceability · 4.3 Architecture, non-functional requirements and the runway |
| 5 Build and integrate | 05-build.md | 5.1 Delivery pipelines as a managed capability · 5.2 Quality gates and evidence a manager can trust · 5.3 Third-party, SaaS and open-source components in the product |
| 6 Release and change | 06-release.md | 6.1 Release versus deployment, and who decides each · 6.2 Change control that protects stability without stopping flow · 6.3 Environments, configuration and the record of what is running |
| 7 Serve: requests, access and consumption | 07-serve.md | 7.1 Request fulfilment and self-service · 7.2 Subscriptions, entitlements and access rights · 7.3 Usage, showback and chargeback |
| 8 Run: operations and reliability | 08-run.md | 8.1 Monitoring, events and incident management · 8.2 Problem management and learning from failure · 8.3 Service levels, SLOs and error budgets as a management tool |
| 9 The records that run IT | 09-records.md | 9.1 The information model: the few records that matter and how they link · 9.2 Configuration and asset data quality: ownership, reconciliation and decay · 9.3 Traceability from investment to incident and back |
| 10 Money, suppliers and risk | 10-money-risk.md | 10.1 IT financial management: cost models, unit costs and the cost of a product · 10.2 Sourcing, suppliers and multi-supplier integration · 10.3 Risk, controls and audit in a regulated bank |
| 11 Tooling and automation | 11-tooling.md | 11.1 The toolchain map: which tool is the system of record for what · 11.2 Integrating and rationalising tools without a big bang · 11.3 AI in IT operations and delivery, with controls |
| 12 Frameworks and transformation | 12-change.md | 12.1 The frameworks landscape: what each is for, and how to use them without becoming their servant · 12.2 Assessing where you are: a maturity and evidence review · 12.3 A transformation roadmap and leading the change |
| 13 Capstone and practice | 13-capstone.md | 13.1 Capstone: Najm Bank's IT operating blueprint · 13.2 Practice exam: 40 scenario questions |

41 lessons. Levels: 🟢 Beginner for Modules 0–2, 🟡 Intermediate for 3–8, 🔴 Advanced for 9–13 (use judgement per lesson). Steps by module: M0 Plan · M1 Improve · M2 Plan, Serve · M3 Plan, Fund · M4 Plan, Build · M5 Build · M6 Release · M7 Serve · M8 Run · M9 Govern · M10 Fund, Govern · M11 Build, Run · M12 Improve, Govern · M13 all.

## Facts to get right (and how to hedge)

- **No statistics without a source.** Any number about delivery performance, costs, failure rates, adoption or benchmarks needs a primary or reputable source (published research such as the DORA reports, official publications, peer-reviewed work, well-known books) in the lesson's References and a row in the claims register. Otherwise do not state it. Najm Bank numbers are illustrative.
- **Research findings:** state what the source found, for whom and when ("the 2024 DORA report found…"), never as a universal law. Prefer the source's own wording for definitions of its metrics.
- **Frameworks and standards:** see "Original, not derived" above. Never claim a framework requires or says something unless the owner's public page states it; otherwise describe the practice in this course's own words.
- **Tools and vendors:** name categories (service management platform, CI/CD system, observability platform, CMDB, cloud cost tool) and at most one or two examples as illustrations, never endorsements. Never quote a vendor price or limit as current.
- **Law, accounting, procurement, regulation:** name the kind of rule and the question to ask the right function. Never state a legal or accounting conclusion.

## File format (the build parses this — follow exactly)

```
# Module 1 — Value and flow

*One-paragraph italic module intro: what the module covers and why, tied to Najm Bank's Technology division.*

> **Steps:** Improve — …(one line in the course's words)

---

# 1.1 — From projects to value: outcomes, value streams and flow
*Level: 🟢 Beginner* · *Prerequisites: 0.1, 0.2* · *Step: Improve*

**After this you can** … (a measurable outcome). *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- 4–6 bullets: what it is, the rule that matters most, the decision cue, the biggest trap.

## 🧭 Why it matters
A scenario at Najm Bank (or a widely reported public situation, with source) that makes the topic unavoidable. 1–3 paragraphs.

## 📐 How it works

### 🟢 The essentials
### 🟡 Going deeper
### 🔴 Expert view
(Plain explanations first; define every term on first use; tables, checklists, before/after examples; one memorable rule per lesson. Mermaid diagrams allowed: `flowchart LR` in English.)

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Value-stream map** | … | … |
(3–8 rows. The first cell MUST start with the name in bold; names match across languages. Tools are examples, not endorsements.)

## 🏛️ In practice at Najm Bank
The artefact this lesson produces, as a cast member used it: concrete, illustrative, labelled as fictional.

## 🛠️ Exercises
Three graded exercises: 🟢 …, 🟡 …, 🔴 …, each with a checkable "*Done when:*" line. After each exercise, a collapsed model answer:

<details><summary>Model answer and self-check</summary>

**Model answer.** … **Self-check.** 3–5 bullets.

</details>

## ⚠️ Mistakes and traps
4–6 bullets: the trap, then what to do instead.

## 🧾 Recap
4–6 bullets.

## ✍️ Check yourself
Five multiple-choice questions (at least three scenario-based, set at Najm Bank). Format:

**1. Question text?**

- A. …
- B. …
- C. …
- D. …

<details><summary>Answer</summary>

**B.** Why B is right, and why the tempting distractor is wrong. (Pointer to the section.)

</details>

## 📚 References
Primary and reputable sources only, each with a working URL you checked or a full citation; never invent a URL or a title.
```

- Separate lessons with a `---` line. The "After this you can" and "Study time" line goes right after the level line (the study time is rewritten later by `scripts/study_time.py`; write any estimate).
- Lesson 13.2 (practice exam) follows the same outer format but its body is: ⚡ (how to use it; say it is practice on this course only, not preparation for any certification), then `## ✍️ Practice exam` with 40 questions numbered 1–40 in the same Q/A format, spread across all modules and answerable from the lessons.
- Answer options: the correct option must **not** be predictable by length, position, specificity or hedging. Similar length and detail, plausible distractors, key letters spread evenly (A–D) across each lesson's 5 items and across the exam.

## Style

- Plain, direct English; short sentences; define jargon on first use; no hype, no fear, no filler. Write for a busy IT manager who must make a decision on Monday.
- Lengths: 2,000–3,500 words per lesson (13.2 excepted). Every lesson's five questions must be answerable from that lesson.
- Use the cast consistently. Do not start any non-quiz line with `**N.` (bold number + dot).
- Do not name any real person, company, bank or product as a case without a cited primary source and a claims-register row. Never write an email address.
- No promise of jobs, income, certification or exam results.

## Arabic edition

Written as Arabic by a careful writer, not translated word for word. Follow `TRANSLATING.md`: an English gloss in parentheses only on a technical term at its first use in a lesson; product, framework and acronym names in Latin letters without parentheses; the header tags (`*Level`, `*Prerequisites`, `*Step`) keep the English step names; "DPO" always with «حماية»; diagrams run right to left. `python3 itbiz/check_ar.py itbiz/modules/NN-x.md itbiz/modules/NN-x.ar.md` must pass.

## Claims register

Every number, regulation, study or case stated as fact needs a row in `academy/claims/itbiz.md` (claim, lesson, source link, date checked, method "opened the page" or "search summary", review-by date). Facts known only from search summaries are "reported", never "verified". Writers return their rows to the lead.
