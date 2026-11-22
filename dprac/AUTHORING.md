# Digital Practice — authoring guide

This is the contract every lesson follows. It is not published.

## What the course is

A free, bilingual (English/Arabic) course on **digital practice**: the everyday skills of the people who discover, build, deliver, run and improve digital products, and how that work changes as a company grows from a few people to several hundred. Full title: *Digital Practice: Building and Running Digital Products, from One Person to a Whole Company*. Arabic: «الممارسة الرقمية: بناء المنتجات الرقمية وتشغيلها، من شخص واحد إلى شركة كاملة».

- **Audience:** early-career practitioners: new software engineers, analysts, testers, designers, product and operations staff, graduates and career changers who want to see how digital work fits together. No prior IT experience is assumed; every term is defined on first use. Managers and architects are pointed to [*Running IT as a Business*](../itbiz/index.html) for the operating-model view.
- **Breadth first, then links for depth.** This course teaches the essentials of each practice well enough to take part in it and make sound everyday decisions, and links to the library's specialist courses for depth (engineering, testing, cloud, security, data, product, AI, founding a company).
- **Original, not derived from any one framework.** The course is written from general practice (product discovery, software engineering, DevOps research, service management, lean and agile ways of working, architecture, IT finance, governance). It is **not** based on, derived from or aligned with any proprietary standard, body of knowledge or certification, and it is **not** training for any exam.
  - In particular it is **not** based on The Open Group's Digital Practitioner Body of Knowledge™ (DPBoK™) Standard. The Open Group's terms prohibit creating material derived from its standards with AI tools without written permission, and its trademark rules forbid its marks in the names of non-accredited courses. So: **never** describe the DPBoK's internal structure (its contexts, competency areas, chapter layout or terms of art); **never** organise a module around it; **never** use "DPBoK", "Digital Practitioner Body of Knowledge" or "Open Group Certified: Digital Practitioner" in a title, heading, toolkit name or quiz item. The course's growth stages below are this course's own and must not be described as the standard's contexts. The only place the DPBoK appears is lesson 12.3, named factually as "The Open Group Digital Practitioner Body of Knowledge™ Standard" with the ™ at first use, the attribution "DPBoK is a trademark of The Open Group", one neutral line on what it is for, and a link to The Open Group's own page. Do not quote it, paraphrase its content, or say this course covers it.
  - The same caution applies to other proprietary bodies of knowledge and frameworks (ITIL®, COBIT®, TOGAF®, SAFe®, Scrum, IT4IT™, VeriSM™, BABOK®, PMBOK®, the FinOps Framework and others): name them factually, say in one line what they are for, add the owner and mark (® or ™) at first use where the owner uses one, link to the owner's page, and never copy their structures, diagrams or wording. Teach the underlying ideas in this course's own words. Lesson 12.3 is the one place that compares them. The Scrum Guide is freely licensed (CC BY-SA); still describe Scrum briefly in your own words and link to it.
- **Honest, practical, no hype.** Every lesson leaves the reader with a skill practised or an artefact produced: a problem statement, an assumption map, a pull request checklist, a test plan, a pipeline sketch, a runbook, a post-incident review, a team working agreement, a board, a roadmap, user stories with acceptance criteria, a service page, a team map, an architecture decision record, a data inventory, a cost sheet, a supplier checklist, a risk register entry, a learning plan.
- **Not professional advice.** Law, accounting, procurement and regulation vary by country. Teach the concepts and the questions to ask; never state a legal or accounting conclusion.
- **No promises.** No promise of jobs, income, promotion or certification.

## The running case: Qafila (fictional)

**Qafila** (قافلة) is a fictional Gulf startup that builds a delivery-coordination app for small businesses (shops, bakeries, pharmacies) and their couriers. Say it is fictional in lesson 0.2. The course follows it through **five growth stages, this course's own**:

| Stage | People | What changes | Modules where it is set |
|---|---|---|---|
| **Launch** | 1–5 | Maha and Faisal build the first version; everything is done by hand | 0–2 |
| **Traction** | about 12, one team | Paying customers, an on-call rota, a real backlog | 3–5 |
| **Growth** | about 40, three or four teams | Support desk, product analytics, service levels | 6–7 |
| **Scale-up** | about 120, a dozen teams | Platform team, many dependencies, architecture and data decisions | 8–9 |
| **Established** | about 400, several countries | Budgets, suppliers, security and audit, regulated customers (a payments partner), AI in daily work | 10–13 |

Cast (use consistently; each makes realistic mistakes the reader learns from):

- **Maha** — founder and CEO. Was a developer; writes the first code with Faisal; later learns to let go.
- **Faisal** — first engineer, later Head of Engineering. Fast; tends to skip tests and documentation early on.
- **Aisha** — joins at Traction as the first product manager.
- **Karim** — designer and user researcher.
- **Salma** — support and operations; becomes the service and reliability lead.
- **Hamad** — data analyst, later head of data.
- **Dana** — security and risk lead, joins at Scale-up.
- **Bilal** — finance lead, later CFO.
- **Yasmin** — a graduate engineer who joins at Growth. She is the reader's stand-in: many lessons show the practice through her first year.

**Qafila fact sheet (fixed; every module uses these figures and no others for the same thing).** All illustrative.

| Item | Launch | Traction | Growth | Scale-up | Established |
|---|---|---|---|---|---|
| People | 2 (Maha, Faisal), then 4 | 12 | 40 | 120 | 400 |
| Merchants using the app | 15 pilot shops | 300 | 2,000 | 9,000 | 30,000 in 4 countries |
| Deliveries per day | about 150 | about 4,000 | about 25,000 | about 120,000 | about 400,000 |
| Teams | none | 1 | 4 | 12 (incl. a platform team) | 35 |
| Deploys to production | by hand, weekly | daily via CI | several a day | many a day | many a day |
| Main product parts | merchant app, courier app, admin web page | + payments via a payment provider | + support desk, analytics | + routing service, platform | + payments partner integration, data platform |

Fixed facts: the first version runs on one cloud provider's managed services; the code lives in one repository until Scale-up; the first serious outage is a failed database migration during Traction (orders lost for about two hours, recovered from backups); the reliability target for order tracking is 99.9% monthly from Growth on; the first product manager (Aisha) arrives at Traction; Yasmin joins at Growth; Dana arrives at Scale-up after a security scare (an access key committed to a public repository); at Established the payments partner's due-diligence questionnaire drives the governance work in Module 11.

Numbers about Qafila (users, orders, costs, headcount, timings) are **illustrative figures, not benchmarks** and are labelled so the first time they appear in a lesson. Do not reuse the cast of other library courses (Tick, Layla, Najm Bank people) except in a link.

Regulation: when a lesson needs it, name the *kind* of rule (data protection, consumer protection, payments, employment) and the question to ask; never invent a law, article or date. Where the library has already verified a source (for example the QCB AI Guideline cited in `../aigp/`), you may link that lesson.

## Reusing the library (the main design rule)

Teach the essentials here; link out for depth with a relative link in the form `[*Cloud & DevOps: Zero to Hero*, lesson 4.2 — …](../cloud/index.html#/4.2)`. Rules:

- Link only to lessons that exist: check the heading in the target file (`../<course>/modules/*.md`) before linking. Use the link text "*Course name*, lesson N.M — title".
- Course folders and anchors: `vibe` (`../vibe/index.en.html#lN-M`), and `saas`, `aigp`, `aipm`, `secai`, `career`, `data`, `cloud`, `testing`, `aiapps`, `ainative`, `founder`, `itbiz` (`../<course>/index.html#/N.M`).
- Likely links: founding and pricing (`founder`), product discovery and roadmaps (`aipm`), shipping and operating software (`vibe`), pipelines, infrastructure and observability (`cloud`), testing (`testing`), security (`secai`), data (`data`), AI tools in daily work (`ainative`, `aiapps`), the manager's operating-model view (`itbiz`), careers (`career`).

## Steps (the lesson tag)

Every lesson is tagged with one or two steps of digital work, in English in both languages: **Discover · Design · Build · Deliver · Operate · Collaborate · Invest · Govern**. Header: `*Step: Build, Deliver*`. These are this course's own plain words, not any framework's terms.

## Module and lesson plan (numbers are fixed)

| Module | File | Lessons |
|---|---|---|
| 0 Orientation | 00-orientation.md | 0.1 What digital practice is: products, services and the work behind them · 0.2 Meet Qafila and the eight steps · 0.3 How to use this course, and what it is not |
| 1 Digital value and the customer | 01-value.md | 1.1 What makes a product digital, and how it creates value · 1.2 Understanding customers: problems, jobs and evidence · 1.3 Business models, costs and the unit of value |
| 2 From idea to first product | 02-first-product.md | 2.1 Discovery: framing a problem and testing assumptions · 2.2 The smallest useful product: scope, prototypes and learning · 2.3 Choosing technology: build, buy, cloud and SaaS |
| 3 Building software well | 03-build.md | 3.1 Version control, code review and working agreements · 3.2 Automated testing and continuous integration · 3.3 Continuous delivery and safe deployment |
| 4 Running what you built | 04-operate.md | 4.1 Infrastructure as code and cloud basics for practitioners · 4.2 Monitoring, alerts and on-call · 4.3 Incidents, post-incident reviews and reliability targets |
| 5 Working as a team | 05-team.md | 5.1 Roles, collaboration and psychological safety · 5.2 Agile ways of working: backlogs, iterations and flow · 5.3 Making work visible and limiting work in progress |
| 6 Product management in a team | 06-product.md | 6.1 Roadmaps and prioritisation · 6.2 Requirements, user stories and acceptance criteria · 6.3 Measuring outcomes: product analytics and experiments |
| 7 Service and support | 07-service.md | 7.1 Designing the service around the product: support model and knowledge · 7.2 Requests, changes and the service desk in a growing company · 7.3 Service levels and talking to customers when things go wrong |
| 8 Many teams | 08-teams.md | 8.1 Team structures and boundaries: product, platform and enabling teams · 8.2 Dependencies, planning and coordination across teams · 8.3 Internal platforms and developer experience |
| 9 Architecture and data | 09-architecture.md | 9.1 Architecture decisions and trade-offs · 9.2 Data as an asset: quality, ownership and privacy · 9.3 Technical debt and modernisation |
| 10 Money and suppliers | 10-money.md | 10.1 Funding digital work: budgets, business cases and funding products · 10.2 The cost of running digital products: cloud costs and unit economics · 10.3 Suppliers, contracts and outsourcing |
| 11 Governance, risk and security | 11-govern.md | 11.1 Governance that enables: decision rights and guardrails · 11.2 Security and risk in everyday practice · 11.3 Compliance and audit without paralysis |
| 12 The bigger picture and your path | 12-path.md | 12.1 Enterprise architecture and portfolio, seen from a team · 12.2 AI in digital work: using it well, with controls · 12.3 Frameworks, bodies of knowledge and your learning path |
| 13 Capstone and practice | 13-capstone.md | 13.1 Capstone: Qafila's digital practice playbook · 13.2 Practice exam: 40 scenario questions |

41 lessons. Levels: 🟢 Beginner for Modules 0–3, 🟡 Intermediate for 4–9, 🔴 Advanced for 10–13 (use judgement per lesson). Steps by module: M0 Discover · M1 Discover · M2 Discover, Design · M3 Build · M4 Operate · M5 Collaborate · M6 Discover, Design · M7 Operate · M8 Collaborate · M9 Design · M10 Invest · M11 Govern · M12 Govern, Collaborate · M13 all.

## Facts to get right (and how to hedge)

- **No statistics without a source.** Any number about delivery performance, costs, failure rates, adoption, salaries or benchmarks needs a primary or reputable source (published research such as the DORA reports, official publications, peer-reviewed work, well-known books) in the lesson's References and a row in the claims register. Otherwise do not state it. Qafila numbers are illustrative.
- **Research findings:** state what the source found, for whom and when ("the 2024 DORA report found…"), never as a universal law.
- **Frameworks and standards:** see "Original, not derived". Never claim a framework requires something unless the owner's public page states it.
- **Tools and vendors:** name categories (version control host, CI system, cloud provider, observability platform, ticketing tool) and at most one or two examples as illustrations, never endorsements. Never quote a vendor price or limit as current.
- **Law, accounting, procurement, regulation:** name the kind of rule and the question to ask. Never state a legal or accounting conclusion.

## File format (the build parses this — follow exactly)

```
# Module 1 — Digital value and the customer

*One-paragraph italic module intro: what the module covers and why, tied to Qafila's stage.*

> **Steps:** Discover — …(one line in the course's words)

---

# 1.1 — What makes a product digital, and how it creates value
*Level: 🟢 Beginner* · *Prerequisites: 0.1, 0.2* · *Step: Discover*

**After this you can** … (a measurable outcome). *Study time: reading about 20 min, hands-on about 90 min (estimate).*

## ⚡ In 60 seconds
- 4–6 bullets: what it is, the rule that matters most, the decision cue, the biggest trap.

## 🧭 Why it matters
A moment at Qafila (or a widely reported public situation, with source) that makes the topic unavoidable. 1–3 paragraphs.

## 📐 How it works

### 🟢 The essentials
### 🟡 Going deeper
### 🔴 Expert view
(Plain explanations first; define every term on first use; tables, checklists, before/after examples; one memorable rule per lesson. Mermaid diagrams allowed: `flowchart LR` in English.)

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Problem statement** | … | … |
(3–8 rows. The first cell MUST start with the name in bold; names match across languages. Tools are examples, not endorsements.)

## 🏛️ In practice at Qafila
The artefact this lesson produces, as a cast member used it: concrete, illustrative, labelled as fictional.

## 🛠️ Exercises
Three graded exercises: 🟢 …, 🟡 …, 🔴 …, each with a checkable "*Done when:*" line. Exercises must be doable by an early-career learner without access to a company: use Qafila material given in the lesson, a personal or open-source project, or a free tool. After each exercise, a collapsed model answer:

<details><summary>Model answer and self-check</summary>

**Model answer.** … **Self-check.** 3–5 bullets.

</details>

## ⚠️ Mistakes and traps
4–6 bullets: the trap, then what to do instead.

## 🧾 Recap
4–6 bullets.

## ✍️ Check yourself
Five multiple-choice questions (at least three scenario-based, set at Qafila). Format:

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
- Lesson 13.2 (practice exam) follows the same outer format but its body is: ⚡ (how to use it; say it is practice on this course only, not preparation for any certification), then `## ✍️ Practice exam` with 40 questions numbered 1–40 in the same Q/A format, spread across all modules and answerable from the lessons, each question followed by its step and lesson tag in italics, e.g. `*(Build · 3.2)*`.
- Answer options: the correct option must **not** be predictable by length, position, specificity or hedging. Similar length and detail, plausible distractors, key letters spread evenly (A–D) across each lesson's 5 items and across the exam.

## Style

- Plain, warm, direct English; short sentences; define jargon on first use; no hype, no fear, no filler. Write for a capable newcomer in their first or second year who wants to understand how the whole thing works.
- Lengths: 2,000–3,500 words per lesson (13.2 excepted). Every lesson's five questions must be answerable from that lesson.
- Use the cast consistently. Do not start any non-quiz line with `**N.` (bold number + dot).
- Do not name any real person, company or product as a case without a cited primary source and a claims-register row. Never write an email address. Never name a real bank.

## Arabic edition

Written as Arabic by a careful writer, not translated word for word. Follow `TRANSLATING.md`: an English gloss in parentheses only on a technical term at its first use in a lesson; product, framework and acronym names in Latin letters without parentheses; the header tags (`*Level`, `*Prerequisites`, `*Step`) keep the English step names; "DPO" always with «حماية»; diagrams run right to left. `python3 dprac/check_ar.py dprac/modules/NN-x.md dprac/modules/NN-x.ar.md` must pass.

## Claims register

Every number, regulation, study or case stated as fact needs a row in `academy/claims/dprac.md` (claim, lesson, source link, date checked, method, review-by date). Facts known only from search summaries are "reported", never "verified". Writers return their rows to the lead.
