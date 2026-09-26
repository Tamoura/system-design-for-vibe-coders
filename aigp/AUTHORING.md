# AI Governance: Zero to Hero — authoring guide

This is the contract every lesson follows. It is not published.

## What the course is

An independent, free, bilingual (English/Arabic) course that takes a reader from zero to "hero" in AI governance and prepares them for the **IAPP AIGP** (Artificial Intelligence Governance Professional) certification. It is aligned to the **AIGP Body of Knowledge v2.1 (effective 2 February 2026)**.

- **Not affiliated with IAPP.** Never imply endorsement, never reproduce IAPP exam questions or copyrighted BoK text beyond the competency titles, never use IAPP logos. The course's own words everywhere.
- **Audience:** lawyers, privacy and compliance officers, risk managers, product managers, data scientists and engineers moving into AI governance — many in the GCC. No legal or technical background assumed at the start.
- **Running case:** **Najm Bank**, a fictional mid-sized Gulf bank (retail, SME and corporate lending) with operations and customers in Qatar, the UAE and the EU (a branch in Frankfurt, EU customers), rolling out AI: a credit-scoring model, a customer-service chatbot, a CV-screening tool bought from a vendor, a GenAI "credit memo copilot" for relationship managers, fraud detection, and employees using public GenAI tools. Najm's characters: **Layla** (Head of AI Governance, the reader's mentor), **Omar** (Chief Data Officer), **Sara** (DPO), **Khalid** (Head of Retail Lending, business owner), **Dana** (lead data scientist), **Yusuf** (procurement), the **AI Governance Committee**. Use them consistently.

## The exam facts (state exactly, and say "at the time of writing (2026)")

- 100 questions (85 scored, 15 unscored pilot), multiple choice, many scenario-based; 2 h 45 min; scaled score 100–500, pass = 300.
- BoK v2.1 domains and IAPP's published question ranges: **I Foundations of AI governance (16–20)**, **II How laws, standards and frameworks apply to AI (19–23)**, **III How to govern AI development (21–25)**, **IV How to govern AI deployment and use (21–25)**.
- Competencies (use these IDs; paraphrase titles in the course's own words):
  - I.A What AI is and why it needs governance · I.B Establishing and communicating organisational expectations (roles, responsibilities, training) · I.C Policies and procedures across the AI life cycle (incl. data governance, IP and third-party risk policies)
  - II.A How existing data privacy laws apply to AI · II.B How other existing laws apply (non-discrimination, IP, consumer protection, product liability) · II.C The main elements of the EU AI Act · II.D The main industry standards and frameworks
  - III.A Governing the design and building of the AI system · III.B Governing the collection and use of data for training and testing · III.C Governing release, monitoring and maintenance
  - IV.A Evaluating key factors and risks before deciding to deploy · IV.B Performing key assessments of the AI system · IV.C Governing deployment and use
- v2.1 shifted wording from "AI model" to "AI system" in Domains III–IV: teach system-level governance.

## Facts to get right (and how to hedge)

State only what you are confident is true. When something may have changed after mid-2026, say so ("at the time of writing", "check the current status"). Never invent article numbers, fines, dates, statistics or quotes. If unsure of an article number, describe the obligation without the number.

- **EU AI Act** — Regulation (EU) 2024/1689; in force 1 Aug 2024. Application: prohibited practices and AI-literacy duty from 2 Feb 2025; GPAI-model obligations and governance/penalties from 2 Aug 2025; most remaining rules incl. Annex III high-risk from 2 Aug 2026; high-risk AI in Annex I regulated products from 2 Aug 2027. Note: in Nov 2025 the Commission proposed a "Digital Omnibus" that would postpone some high-risk deadlines — tell readers to check the current status; the exam tests the Act as adopted. Roles: provider, deployer, importer, distributor, authorised representative, product manufacturer. Risk tiers: prohibited (Art. 5), high-risk (Art. 6 + Annexes I/III), transparency obligations (Art. 50), minimal. Max fines: €35m/7% (prohibited practices), €15m/3% (most other obligations), €7.5m/1% (incorrect information). GPAI with systemic risk presumed above 10^25 FLOPs of training compute; GPAI Code of Practice published July 2025. Deployers of certain high-risk systems (public bodies, and credit-scoring/insurance pricing uses) must do a Fundamental Rights Impact Assessment (Art. 27). Credit scoring of natural persons is Annex III high-risk (fraud detection excluded). AI Office; national market-surveillance authorities; regulatory sandboxes.
- **GDPR** — Art. 5 principles; Art. 6 lawful bases; Art. 9 special categories; Arts 13–15 transparency/access incl. "meaningful information about the logic involved"; Art. 22 solely automated decisions with legal or similarly significant effects; Art. 25 data protection by design; Art. 35 DPIA. EDPB Opinion 28/2024 on AI models (anonymity of models, legitimate interest, unlawfully processed training data). CJEU *SCHUFA* (C-634/21, Dec 2023): a credit score can itself be an Art. 22 decision when it plays a determining role.
- **NIST AI RMF 1.0** (Jan 2023): functions Govern, Map, Measure, Manage; trustworthy characteristics — valid and reliable; safe; secure and resilient; accountable and transparent; explainable and interpretable; privacy-enhanced; fair with harmful bias managed. Generative AI Profile NIST AI 600-1 (July 2024). Playbook. Voluntary.
- **ISO/IEC**: 42001:2023 AI management system (certifiable, Plan-Do-Check-Act, Annex A controls); 23894:2023 AI risk management guidance; 22989:2022 concepts and terminology; 42005:2025 AI system impact assessment; 38507 governance implications for boards; 5338 AI life cycle; 42006 requirements for bodies certifying 42001.
- **OECD AI Principles** (2019, updated May 2024); OECD definition of "AI system" (updated Nov 2023, basis of the EU AI Act definition). **UNESCO Recommendation on the Ethics of AI** (2021). **Council of Europe Framework Convention on AI and Human Rights, Democracy and the Rule of Law** (opened for signature Sept 2024). **G7 Hiroshima Process** code of conduct (2023).
- **US**: no comprehensive federal AI law; EO 14110 (2023) revoked Jan 2025; agencies use existing laws (FTC Act s.5, ECOA/Reg B adverse-action notices, Fair Housing Act, Title VII, ADA). NYC Local Law 144 (bias audits for automated employment decision tools). Colorado AI Act (SB 24-205) — effective date was postponed to 30 June 2026; check current status. Hedge state-law details.
- **Other**: EU Product Liability Directive (EU) 2024/2853 covers software incl. AI; the proposed AI Liability Directive was withdrawn (2025). China: algorithm recommendation provisions (2022), deep synthesis (2023), Interim Measures for Generative AI Services (2023), AI-content labelling measures (2025). Singapore Model AI Governance Framework (and GenAI version 2024), AI Verify. UK principles-based, regulator-led approach.
- **GCC**: Qatar — Law No. 13 of 2016 on Personal Data Privacy Protection (PDPPL); Qatar Central Bank has issued AI guidance for regulated financial institutions (describe as "QCB's AI guideline for financial institutions" without inventing clause numbers); Qatar's national AI strategy. Saudi Arabia — Personal Data Protection Law (in force 2023), SDAIA AI Ethics Principles. UAE — Federal Decree-Law 45/2021 (PDPL), DIFC Data Protection Law with Regulation 10 on autonomous systems, UAE AI Charter/strategy. Hedge specifics; point readers to official sources.
- **Real cases you may use** (well documented only): Amazon's scrapped recruiting model (reported 2018); Dutch childcare-benefits scandal (toeslagenaffaire); Moffatt v. Air Canada (2024, chatbot misstatement, airline liable); Italian Garante vs OpenAI (2023 temporary limitation; €15m fine Dec 2024); Clearview AI fines by several EU DPAs; COMPAS recidivism debate (ProPublica 2016); Apple Card / NYDFS review (2021); EEOC v. iTutorGroup settlement (2023, age discrimination via automated screening); Samsung staff pasting code into ChatGPT (2023); SCHUFA (CJEU 2023).

## Module and lesson plan (numbers are fixed)

| Module | File | Lessons |
|---|---|---|
| 0 Orientation | 00-orientation.md | 0.1 What AI governance is, and what the AIGP proves · 0.2 How the exam thinks: BoK v2.1, question styles, a study plan · 0.3 Meet Najm Bank: an AI inventory from day one |
| 1 What AI is and why it needs governance (I.A) | 01-foundations.md | 1.1 AI, machine learning, generative AI and agents · 1.2 Risks and harms to people, groups, organisations and society · 1.3 Why AI is different: the traits that demand governance |
| 2 Organisational expectations (I.B) | 02-organisation.md | 2.1 From principles to strategy and risk appetite · 2.2 Roles, accountability and the AI governance committee · 2.3 AI literacy, training and culture |
| 3 Policies across the life cycle (I.C) | 03-policies.md | 3.1 The AI life cycle and the policy stack · 3.2 Data governance and intellectual-property policies for AI · 3.3 Third-party and supply-chain risk |
| 4 Privacy and data protection law (II.A) | 04-privacy.md | 4.1 Data protection principles meet AI · 4.2 Automated decisions, individual rights and transparency · 4.3 DPIAs and the global privacy map, from the EU to the GCC |
| 5 Other laws that already apply (II.B) | 05-other-laws.md | 5.1 Non-discrimination in hiring, credit and services · 5.2 Intellectual property in AI inputs and outputs · 5.3 Consumer protection, product liability and sector rules |
| 6 The EU AI Act (II.C) | 06-eu-ai-act.md | 6.1 Scope, roles and the risk pyramid · 6.2 High-risk obligations for providers and deployers · 6.3 General-purpose AI, transparency, enforcement and the timeline |
| 7 Standards and frameworks (II.D) | 07-frameworks.md | 7.1 OECD principles and the NIST AI RMF · 7.2 ISO/IEC 42001 and the AI standards family · 7.3 The global map: other frameworks that shape practice |
| 8 Governing design and build (III.A) | 08-design-build.md | 8.1 Use-case intake, business case and risk tiering · 8.2 Designing for trustworthiness · 8.3 Documentation, and build versus buy |
| 9 Data for training and testing (III.B) | 09-data.md | 9.1 Sourcing, lineage and rights to use data · 9.2 Quality, representativeness and bias · 9.3 Testing, evaluation, validation and red-teaming |
| 10 Release, monitoring and maintenance (III.C) | 10-release-monitor.md | 10.1 Release readiness and conformity · 10.2 Monitoring, drift and incidents · 10.3 Change management, maintenance and retirement |
| 11 Deploying and using AI (IV.A–IV.C) | 11-deployment.md | 11.1 The deploy decision: context, stakeholders and alternatives · 11.2 Buying AI: vendor due diligence and contracts · 11.3 Assessing the system: impact assessments, audits and assurance · 11.4 Governing use: oversight, transparency and incident response |
| 12 Hero: capstone and exam | 12-capstone.md | 12.1 Capstone: governing Najm's credit copilot end to end · 12.2 Exam strategy and the traps that cost marks · 12.3 Full mock exam: 100 questions |

Levels (zero → hero): 🟢 Beginner for Modules 0–1 and the essentials, 🟡 Intermediate for 2–7, 🔴 Advanced for 8–12 (use judgement per lesson).

## File format (the build parses this — follow exactly)

```
# Module 6 — The EU AI Act

*One-paragraph italic module intro: what the module covers and why, tied to Najm Bank.*

> **BoK coverage:** II.C — …(one line in the course's words)

---

# 6.1 — Scope, roles and the risk pyramid
*Level: 🟡 Intermediate* · *Prerequisites: 1.1, 4.1* · *BoK: II.C*

## ⚡ In 60 seconds
- 4–6 bullets: what it is, the rule that matters most, the exam cue, the biggest trap.

## 🧭 Why it matters
A Najm Bank scenario (or a real public case) that makes the topic unavoidable. 1–3 paragraphs.

## 📐 How it works
### 🟢 The essentials
### 🟡 Going deeper
### 🔴 Expert view
(Plain explanations first; define every term on first use; tables and one mermaid diagram where they genuinely help. Mermaid: flowchart/sequence only, short labels, no parentheses inside node labels.)

## ⚖️ The instruments
| Instrument | What it requires or recommends | Exam cue |
|---|---|---|
| **EU AI Act** — Art. 6 & Annex III | … | … |
(3–8 rows. First cell MUST start with the instrument's name in bold — e.g. **GDPR**, **EU AI Act**, **NIST AI RMF**, **ISO/IEC 42001**, **OECD AI Principles**, **Qatar PDPPL**, **NYC Local Law 144** — optionally followed by " — Art. X". Keep bold names consistent across lessons; they build the instruments catalogue.)

## 🏛️ In practice at Najm Bank
The governance artefact this lesson produces: a policy clause, a RACI, an intake form, a checklist, a committee decision, an impact-assessment excerpt. Concrete, reusable, in a table or a short template.

## 🛠️ Exercises
Three graded exercises: 🟢 …, 🟡 …, 🔴 …, each with a "*Done when:*" line.

## ⚠️ Mistakes and exam traps
4–6 bullets: the trap, then what to do or answer instead.

## 🧾 Recap
4–6 bullets.

## ✍️ Check yourself
Five AIGP-style multiple-choice questions (at least two scenario-based, set at Najm Bank or a neutral organisation). Format:

**1. Question text?**

- A. …
- B. …
- C. …
- D. …

<details><summary>Answer</summary>

**B.** Why B is right, and why the tempting distractor is wrong. (Pointer to the section.)

</details>

## 📚 References
Official sources only (legislation on eur-lex.europa.eu, nist.gov, iso.org pages, oecd.ai, edpb.europa.eu, iapp.org for the BoK, national regulators). Plain links; no invented URLs — link to a top-level official page if unsure of the deep link.
```

- Separate lessons with a `---` line.
- Lesson 12.3 (mock exam) follows the same outer format but its body is: ⚡ (how to take it), then `## ✍️ Mock exam` with 100 questions numbered 1–100 in the same Q/A format, grouped by domain in blueprint proportions (I ≈18, II ≈21, III ≈23, IV ≈23, plus ≈15 mixed scenario questions counted inside those), each answer ending with its competency ID, then 🧾 and 📚. Its ⚖️/🏛️/🛠️/⚠️ sections may be short.

## Style

- Plain, direct English; short sentences; define jargon on first use; no hype; no filler. Explain *why*, not just *what*.
- Balanced and accurate on law: describe what an instrument requires, who it applies to, and when; distinguish binding law from voluntary frameworks; say "this is not legal advice" once per module intro, not per lesson.
- Lengths: 2,000–3,500 words per lesson (12.3 excepted). Every lesson's five questions must be answerable from that lesson.
- Use the running cast consistently; Najm Bank is fictional — say so in 0.3.
