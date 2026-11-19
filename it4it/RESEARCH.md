# IT4IT™ course: primary-source research

Status: research only. No lessons written. Sections 0, 1, 2 and 4 were re-checked by a second agent against the live sources on 2026-11-19, and its corrections are applied.
All sources were read on **2026-11-19**, and every fact below was read on that date unless a row says otherwise.
Sources are limited to The Open Group's own sites: www.opengroup.org, publications.opengroup.org and pubs.opengroup.org.
"confirm" means the fact could not be checked against a source that was readable here. It must be checked before any lesson uses it.

IT4IT™ is a trademark of The Open Group. This file is internal research notes. It is not an accredited course or course material.

---

## 0. Blockers to resolve before writing any lesson (read first)

These come from The Open Group's own terms. They affect whether, and how, this course can be built at all.

| # | Finding | Source |
|---|---|---|
| B1 | **AI notice.** The Open Group "strictly prohibits the incorporation of its standards, guides, and other copyrighted material … into any form of Artificial Intelligence (AI) tools". The notice names several assistants, including the one used to prepare this file. It also says the creation of derivatives of its IP "using Artificial Intelligence is strictly prohibited" without "the explicit written permission of The Open Group VP of Standards". The last line of the page content reads "Updated May 2026". | https://www.opengroup.org/copyrights |
| B2 | **AI USE RESTRICTION in the publication licences.** The licences for the IT4IT Standard 3.0, 3.0.1, 2.1 and the 3.1 Snapshot each say that use of the publication "to generate any data or content" with LLM or generative-AI tools is "NOT PERMITTED". | https://publications.opengroup.org/standards/it4it/c24a · /c221 · /c171 · /s261 (licence pop-up text in each page) |
| B3 | **Training counts as commercial use.** The Commercial Licence page says: "Commercial purposes include … providing IT4IT based consultancy, expertise, or training services". Such use needs an annual IT4IT Standard, Version 3.0 Commercial License, which also covers 3.0.1. The Non-Commercial licence says the same. | https://www.opengroup.org/it4it/ra/license_comm · https://www.opengroup.org/it4it/ra/license_nc |
| B4 | **Trademark in course names.** "If your organization is advertising a non-accredited course then as per the commercial license it is forbidden to use the trademark in the course name." The trademark may be used in subtitles and descriptive material if it is acknowledged and the guidelines are followed. | https://www.opengroup.org/certifications/accreditation/course-naming |
| B5 | **Unlicensed training is named as possible infringement.** The trademark page gives "IT4IT™ … Training without a commercial license" as an example of unlicensed use. | https://www.opengroup.org/trademarks |

Consequence for this file: the standard itself was **not** read. It is behind a login (see §6), and B1/B2 forbid feeding it to an AI tool in any case. Section 2 therefore holds only what The Open Group states on its public web pages. Everything else is marked "confirm" and was **not** filled in from memory. The course owner should get written permission (B1) and the right licence (B3) before any lesson is drafted from the standard. A human author holding a licence may also need to do that drafting.

---

## 1. Current standard

| Item | Value | Source |
|---|---|---|
| Exact name | The Open Group IT4IT™ Standard, Version 3.0.1: A Reference Architecture for Managing Digital | https://publications.opengroup.org/standards/it4it/c24a |
| Version | 3.0.1. The page calls it "a minor maintenance update" that "incorporates Technical Corrigendum 1 of the IT4IT Standard, Version 3.0". | same |
| Document number | C24A | same |
| Publication date | 24 Oct 2024 | same |
| US ISBN | 1-957866-52-9 | same |
| Status | Adopted. Type: The Open Group Standard. Common name: "IT4IT Standard V3.0.1". | same |
| Supersedes | The Open Group IT4IT™ Standard, Version 3.0: A Reference Architecture for Managing Digital (C221, published 18 Oct 2022, ISBN 1-947754-91-1) | https://publications.opengroup.org/standards/it4it/c221 |
| C221 supersedes | The Open Group IT4IT™ Reference Architecture, Version 2.1 (C171, published 30 Jan 2017, 178 pages, ISBN 1-937218-84-3) | https://publications.opengroup.org/standards/it4it/c171 |
| Corrigendum | The Open Group IT4IT™ Standard, Version 3.0: A Reference Architecture for Managing Digital Technical Corrigendum 1 (U246). The page shows "23 Oct 2024" and type "Guides". Contents not readable (login). | https://publications.opengroup.org/u246 |
| Next version (draft) | The Open Group IT4IT™ Standard, Version 3.1 (Snapshot), S261, published 12 Oct 2026, 289 pages. The page says it is "a Snapshot document of what is intended to become" Version 3.1 and is "valid through March 31, 2027". Snapshots are "draft standards", and The Open Group "makes no commitment regarding publication". | https://publications.opengroup.org/standards/it4it/s261 |
| One-line purpose (publisher's wording) | 3.0.1 "describes a reference architecture that can be used to manage the business of Information Technology (IT) and the associated end-to-end lifecycle management of Digital Products." | https://publications.opengroup.org/standards/it4it/c24a |
| Publisher's other claims | The standard is meant to give "a prescriptive Target Architecture". It is "independent of specific technologies, vendors, organization structures, process models, and methodologies", and it "addresses every Digital Product lifecycle phase from investment decision-making to end-of-life". | same |

### What changed, as far as public pages say

- **2.1 → 3.0.** The 3.0 excerpt Snapshot (S210, 22 Jan 2021) describes "a pivot towards managing Digital Products". It also mentions "modern value stream flow" and "more emphasis on iterative thinking". Source: https://publications.opengroup.org/standards/it4it/s210
- The certification FAQ says 2.1 knowledge "has just been completed by additional concepts e.g. Digital Product and revised value streams". Source: https://www.opengroup.org/certifications/it4it-certification-program-faqs
- In 2.1, the IT Value Chain had four value streams: Strategy to Portfolio, Requirement to Deploy, Request to Fulfill and Detect to Correct. The FAQ says they "generally align to" "Plan, Build, Deliver, Run", and that an IT Value Chain model reinvents this "into 'Plan, Source, Offer, Manage'". Source: https://www.opengroup.org/membership/forums/it4it-forum/it4it-faq. The four names appear in its ITIL answer. This is an undated, 2.x-era FAQ that is still online, and it never says "2.1". Linking it to 2.1 rests on the C171 page.
- The 3.0 certification material names seven value streams instead: Evaluate, Explore, Integrate, Deploy, Release, Consume and Operate. See §2.1.
- A detailed list of changes between 2.1 and 3.0 has not been read: **confirm** (it should be in the standard's front matter, which needs a login).
- **3.0 → 3.0.1:** "minor maintenance update", which incorporates Technical Corrigendum 1 (C24A page).
- **3.0.1 → 3.1:** only the Snapshot exists. Its changes have not been read: **confirm**.

### Licence and terms for quoting

- **Getting a copy:** the 3.0 standard is "available to all free-of-charge to download for non-commercial use" after registration. Options are:
  - a 90-day Evaluation License, then a free perpetual Non-Commercial License;
  - a Member License, for IT4IT Forum members;
  - an annual Commercial License, needed for commercial use including training (B3).

  Source: https://www.opengroup.org/IT4IT/downloads (page titled "IT4IT™ Standard, Version 3.0 Licensed Downloads").
- **Redistribution:** the evaluation licence says "Redistribution of the Documentation, in part or in whole, is not permitted." Source: https://publications.opengroup.org/standards/it4it/i24a
- **Quoting:**
  - "you may extract a few portions to incorporate into your work", with attribution, unless the document's own notice restricts this.
  - "Substantial portions, or any charts, graphics and other extracts … require a permission to use."
  - The site gives a Publications Copyright Permissions Form.

  Source: https://www.opengroup.org/copyrights. The AI notice on the same page (B1) overrides this for any AI-assisted work.
- **Site content** (not publications) may be copied "for non-commercial use within your organization only". Source: https://www.opengroup.org/copyrights

---

## 2. Structure of the standard (public statements only)

Most of this section is **confirm**. The standard text is gated (§6), and AI use of it is prohibited (B1/B2).

### 2.1 Value streams (3.0 / 3.0.1)

The names are exactly as listed in the IT4IT 3 Foundation datasheet and the exam plan:

| Value stream | Purpose | Activities / stages |
|---|---|---|
| Evaluate | confirm | confirm |
| Explore | confirm | confirm |
| Integrate | confirm | confirm |
| Deploy | confirm | confirm |
| Release | confirm | confirm |
| Consume | confirm | confirm |
| Operate | confirm | confirm |

Sources:
- https://www.opengroup.org/sites/default/files/images/Accreditation/IT4IT-3-Foundation-Certification-datasheet.pdf, which lists "The purpose and content of the Evaluate value stream" and so on for each of the seven.
- https://www.opengroup.org/certifications/it4it-certification-program-faqs (exam plan).

The S210 excerpt description names the lifecycle concerns the information model controls: "exploration, integration, release, deployment, fulfillment, operations, and evaluation of Digital Products". Source: https://publications.opengroup.org/standards/it4it/s210. Whether "fulfillment" maps to Consume is **confirm**.

### 2.2 Other structural elements

| Element | What public pages say | Status |
|---|---|---|
| Digital Product | One of the "new concepts" introduced in 3.0 (FAQ; datasheet: "Digital Product and related concepts"). | Definition: confirm |
| Digital Product Backbone | Datasheet: "The Digital Product Backbone functional component and associated data objects". The singular "functional component" is the datasheet's own wording. | Contents: confirm |
| Service Offer Backbone | Datasheet: "The Service Offer Backbone functional components and associated data objects". | Contents: confirm |
| Functional components per value stream | Not public. | confirm |
| Key data objects; essential vs auxiliary distinction | Not public for 3.0. Whether 3.0 keeps the essential/auxiliary terms is unknown. | confirm |
| Reference architecture abstraction levels | Not public for 3.0. The 2.x FAQ mentions "Level II" modelled in ArchiMate. | confirm for 3.0 |
| Value stream / value network | The IT4IT home page has a diagram whose alt text (not a visible caption) is "Digital Value Network" and calls the standard "a flexible, value stream-based approach". The 2.x FAQ uses "IT Value Chain". | 3.0 definitions: confirm |
| Supporting activities | Not public. | confirm |
| Capabilities | C24A/C221 pages say the standard "describes and connects the capabilities, value streams, functions, and operational data needed to manage a Digital Product Portfolio at scale". | Capability list: confirm |
| Reference Architecture vs Operating Model | 2.1 (C171 page) is described as "a standard reference architecture and value chain-based operating model for managing the business of IT". The forum FAQ also calls IT4IT "not a process model" but "an information model". No 3.0 statement on this distinction was found. | 3.0: confirm |
| ArchiMate model | C24A page: "The model is provided as a zipped XML file with Version 3.0." | Readable only after login |

Sources: https://www.opengroup.org/it4it · https://publications.opengroup.org/standards/it4it/c24a · https://publications.opengroup.org/standards/it4it/c221 · https://publications.opengroup.org/standards/it4it/c171 · https://www.opengroup.org/membership/forums/it4it-forum/it4it-faq

---

## 3. Stated relationships with other frameworks

Only The Open Group's public pages were read. What the 3.0 standard itself says is **confirm**.

| Framework | What The Open Group says | Source / era |
|---|---|---|
| ITIL | "complementary". ITIL is "a process and capability-based framework"; IT4IT "provides a foundation upon which best practice-based process models like ITIL may run". | Forum FAQ (2.x era) |
| Agile / DevOps / SAFe | IT4IT "Provides a standard reference model for a DevOps toolchain" and "a mapping of SAFe (Scaled Agile Framework) concepts into traditional project and portfolio management". It is "agnostic" to the development method (Waterfall or Agile). The IT4IT home page mentions "re-tooling for Agile or DevOps". | Forum FAQ (2.x era) · https://www.opengroup.org/it4it |
| ArchiMate | The IT4IT Forum "uses the ArchiMate modeling language" to express the reference architecture. | Forum FAQ |
| Multi-sourcing (SIAM-type concerns) | The FAQ describes managing "multi-sourced IT" and supplier on- and off-boarding, but does not use the term SIAM. | Forum FAQ. SIAM by name: confirm |
| TOGAF | No statement found on public IT4IT pages. | confirm |
| COBIT | No statement found. | confirm |

Forum FAQ URL: https://www.opengroup.org/membership/forums/it4it-forum/it4it-faq. It describes the four 2.x value streams, so its statements may not reflect 3.0.

---

## 4. Certification

### 4.1 Programme

- The IT4IT Certification Program "encompasses IT4IT Foundation certification and IT4IT 3 Foundation certification". These are based on Version 2.1 and Version 3.0 respectively. Source: https://www.opengroup.org/certifications/it4it
- The 2.1-based IT4IT Foundation continues "as long as the market needs it". IT4IT 3 Foundation is "a new and separate certification".
- "There are currently no plans to add an IT4IT 3 Level 2 Certification."
- The FAQ places Foundation at Bloom's levels 1 and 2 (remembering and understanding).
- The certification "does not expire". It "is to a given version of the Body of Knowledge", with no renewal requirement. The FAQ says the same for IT4IT Foundation. Source: the datasheet.

  Source for the first three points above: https://www.opengroup.org/certifications/it4it-certification-program-faqs
- An IT4IT 3 Foundation Open Badge is issued. Prerequisites: none. Source: the datasheet PDF (URL below).

### 4.2 IT4IT 3 Foundation exam

| Item | Value | Source |
|---|---|---|
| Name | IT4IT™ 3 Foundation | Datasheet |
| Format | Multiple-choice examination | Datasheet |
| Questions / duration | 40 questions / 60 minutes | Datasheet; FAQ |
| Pass mark | "at least 60%" | FAQ |
| Open book | NO (closed book); supervised: YES | Datasheet |
| Delivery | At home or in an office through the test provider's online proctoring, or at the test provider's centres | Datasheet |
| Languages | "Initially … English and English with an ESL … time allowance" | FAQ |
| Exam code | The FAQ lists "OGIT-101" under "Available now". Whether this is the IT4IT 3 Foundation code is **confirm**, because the examinations list on certification.opengroup.org was blocked. | FAQ |
| Retake | Retaking within one month voids the result. This is stated on the older IT4IT Foundation page, so whether it applies to IT4IT 3 is **confirm** (the current exam policy is X251, Version 1.1, which supersedes X1603). | https://www.opengroup.org/certifications/it4it-individual-certification |

Datasheet URL: https://www.opengroup.org/sites/default/files/images/Accreditation/IT4IT-3-Foundation-Certification-datasheet.pdf (marked "Copyright © 2023").

For comparison, the older IT4IT Foundation (2.1) exam, "IT4IT Part 1", has 40 simple multiple-choice questions and a pass mark of 65% (26 of 40). Source: https://www.opengroup.org/certifications/it4it-individual-certification. Do not mix this up with IT4IT 3.

### 4.3 Syllabus topic areas, exactly as published (exam plan, 40 questions)

| Topic area | Questions |
|---|---|
| IT4IT Introduction | 5 |
| Digital Product | 8 |
| Digital Product Backbone Functional Components and Data Objects | 7 |
| Service Offer Backbone Functional Components and Data Objects | 6 |
| Evaluate Value Stream | 2 |
| Explore Value Stream | 2 |
| Integrate Value Stream | 2 |
| Deploy Value Stream | 2 |
| Release Value Stream | 2 |
| Consume Value Stream | 2 |
| Operate Value Stream | 2 |

Source: https://www.opengroup.org/certifications/it4it-certification-program-faqs ("What is the exam plan for the IT4IT 3 Foundation Exam?"). The counts add up to 40.

The datasheet's "demonstrated their understanding of" list, verbatim:
- The basic concepts of the IT4IT Reference Architecture
- The Digital Product and related concepts within the context of the IT4IT Reference Architecture
- The Digital Product Backbone functional component and associated data objects
- The Service Offer Backbone functional components and associated data objects
- The purpose and content of the Evaluate / Explore / Integrate / Deploy / Release / Consume / Operate value stream (one line each)

**Detailed learning outcomes:** these are defined in X236, "The Open Group Certification for People: IT4IT™ Conformance Requirements (Level 1), Version 3.0" (published 27 Mar 2023). Its PDF needs a login, so the exact learning-outcome wording is **confirm**. Related documents:
- X235, Program Configuration, Version 3.0 (27 Mar 2023)
- X1603, Certification Policy for Examination-Based Programs, Version 1.0 (18 Apr 2016). Its page marks it "(Superseded)" by X251, Version 1.1, which was not read: confirm.

Sources: https://publications.opengroup.org/x236 · /x235 · /x1603

### 4.4 Training material and trademark rules

- **Accredited versus non-accredited:** accredited providers are assessed on course, personnel and organisation. Their course fee includes the exam. Some may distribute "the official pdf copy of the standard". Source: https://www.opengroup.org/certifications/it4it-individual-certification
- **Accreditation needs:** an IT4IT™ Commercial License, a Training Course Accreditation Agreement and a Trademark License Agreement. It also requires compliance with the Training Course Accreditation Policy (X255) and Requirements (X256). Annual fees are US$3,250 for a first course (one language and one delivery method). Each further course is US$2,500, each extra language US$1,800, and each extra delivery method US$1,200. "IT4IT™ 3 Training Course Materials" are "provided upon registration and payment of the fees". Source: https://www.opengroup.org/certifications/accreditation/atc
- **Course names:**
  - Only an accredited course may carry the trademark in its name, and only with permission.
  - A course name may not include "Certification", "Accredited" or "The Open Group".
  - The trademark may appear in subtitles and descriptive material "as long as the trademark and attribution are acknowledged, and the trademark usage guidelines are followed". The ™ symbol rule comes from the trademark guidelines.

  Source: https://www.opengroup.org/certifications/accreditation/course-naming
- **Trademark use:**
  - "IT4IT™ and IT4IT™ logo" are listed as unregistered trademarks of The Open Group.
  - Use the ™ symbol at the first and most significant use, with an attribution of ownership.
  - Do not use the mark as a generic term, "in connection with book titles, white papers, seminars, or conferences" without authorisation, or in ways that imply endorsement or certification.
  - Editorial use is allowed without prior permission if the guidelines are followed; advertising use needs permission.

  Sources: https://www.opengroup.org/trademarks · https://www.opengroup.org/permissions
- **Corporate name:** write "The Open Group" with "The" capitalised, and never abbreviate it. Source: https://www.opengroup.org/permissions
- **Trainers** of IT4IT 3 accredited courses must pass the IT4IT 3 Foundation exam. Source: the certification FAQ.

---

## 5. Terminology (proposed)

The English definitions are paraphrased **only** from the public pages cited above. Where no public definition was found, the cell says confirm. All Arabic renderings are **proposed by this research and do not come from the standard**. The Open Group has published English–Chinese translation glossaries (C236 for 3.0, C201 for 2.1), but no Arabic glossary was found.

| English term | One-line meaning (paraphrased; source) | Proposed MSA rendering (proposed, not from the standard) |
|---|---|---|
| IT4IT™ Reference Architecture / IT4IT Standard | Reference architecture for managing the business of IT and the end-to-end lifecycle of Digital Products (C24A page). | البنية المرجعية IT4IT™ / معيار IT4IT™ |
| Digital Product | Central managed unit in 3.0. Definition: confirm. | المنتج الرقمي |
| Digital Product Portfolio | The set of Digital Products the standard aims to manage "at scale" (C24A page). | محفظة المنتجات الرقمية |
| Value stream | The standard's organising unit ("value stream-based approach", it4it page). Definition: confirm. | مسار القيمة (تدفّق القيمة) |
| Digital Value Network | Shown on the IT4IT home page. Definition: confirm. | شبكة القيمة الرقمية |
| IT Value Chain (2.x) | 2.x value-chain framework of four value streams (C171 page; forum FAQ). | سلسلة قيمة تقنية المعلومات |
| Evaluate / Explore / Integrate / Deploy / Release / Consume / Operate | The seven 3.0 value streams (datasheet). Purposes: confirm. | التقييم / الاستكشاف / التكامل / النشر / الإصدار / الاستهلاك / التشغيل |
| Digital Product Backbone | Part of the architecture tested with its data objects (datasheet). Definition: confirm. | العمود الفقري للمنتج الرقمي |
| Service Offer Backbone | Part of the architecture tested with its functional components and data objects (datasheet). Definition: confirm. | العمود الفقري لعرض الخدمة |
| Functional component | Building block of the architecture (datasheet, FAQ). Definition: confirm. | المكوّن الوظيفي |
| Data object | Information element associated with functional components (datasheet). Definition: confirm. | كائن البيانات |
| Capability | Listed among what the standard "describes and connects" (C24A page). Definition: confirm. | القدرة |
| Body of Knowledge (BoK) | Subset of the standard defined as learning units in the Conformance Requirements (certification FAQ). | مجموعة المعارف |
| Conformance Requirements | The syllabus document defining the BoK, X236 (certification FAQ). | متطلبات المطابقة |
| Accredited Training Course | Course assessed and accredited by The Open Group (individual certification page). | دورة تدريبية معتمدة |
| Snapshot | Draft standard published for feedback, with no commitment to publish (S261 page). | لقطة (مسودة معيار) |
| Technical Corrigendum | Correction document, U246, incorporated in 3.0.1 (C24A page). | تصويب فني |

---

## 6. Could not read (confirm)

| URL | Reason | What it would settle |
|---|---|---|
| https://pubs.opengroup.org/it4it/ (and /it4it/3.0.1/, /it4it/3.1/, /it4it/3.0/) | Redirects to an OAuth login at identity.opengroup.org; the network proxy also blocks that host. | All of §2, exact definitions |
| https://publications.opengroup.org/standards/it4it/c24a, /i24a, /i24am (PDF, HTML, ArchiMate model) | "Login to Download" | §1 change log, §2 |
| https://publications.opengroup.org/standards/it4it/s261 (3.1 Snapshot) | Login to download | 3.1 changes |
| https://publications.opengroup.org/u246 (Technical Corrigendum 1) | Login to download | 3.0 → 3.0.1 detail |
| https://publications.opengroup.org/x236 (Conformance Requirements L1, v3.0) | "Free PDF Edition", but needs a login | Exact learning outcomes |
| https://publications.opengroup.org/x235 · https://publications.opengroup.org/x1603 · X251 (current exam policy, v1.1) | Login | Programme configuration, retake and conduct rules |
| https://certification.opengroup.org/docs/datasheets/it4it-exams.pdf · https://certification.opengroup.org/examinations | Host blocked by this environment's network policy (proxy 403), not by The Open Group | Exam code and summary |
| https://publications.opengroup.org/standards/it4it/c236 | Login | Official Chinese glossary, only as a model for the Arabic glossary |
| https://www.opengroup.org/sites/default/files/Accreditation2025/X255.pdf · X256.pdf · TMLA%20v2.0_ff.pdf | Downloaded but **not reviewed** in this pass | Detailed accreditation and trademark obligations |

Also not done, deliberately: I did not search third-party sites for the standard's content. The task limited sources to The Open Group, and B1 prohibits reconstructing it with AI.
