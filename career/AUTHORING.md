# From Graduate to Hired — authoring guide

This is the contract every lesson follows. It is not published.

## What the course is

A free, bilingual (English/Arabic) course that takes a **computer science, data science or computer (software) engineering graduate** from "I have a degree" to "I have an offer, and I am trusted in my first 90 days" — in a market where AI coding agents do much of the routine work juniors used to do.

It is also the **front door to the whole library**: rather than re-teach engineering, it diagnoses what employers check for, sends the learner to the exact lessons in the other courses that build each skill, and teaches what no other course teaches: choosing a role, building proof, getting seen, passing interviews, negotiating, and starting well.

- **Audience:** final-year students and graduates of CS, data science and computer/software engineering (and bootcamp or self-taught people at the same stage); their career-centre advisers and lecturers; hiring managers who want a shared language. Basic programming assumed; no work experience assumed.
- **Honest, not hype.** The entry-level market is harder than a few years ago and changes fast. Say what employers check for and why; never promise outcomes ("guaranteed job"), never invent salaries, hiring statistics, acceptance rates or company policies. Where a number matters, say how to find the current one (job boards, salary surveys, recruiters) and hedge "at the time of writing (2026)".
- **Practical judgement over tips.** Every lesson leaves the learner with a decision made or an artefact produced: a target-role choice, a skills gap list, a project spec, a CV, an outreach message, an interview story bank, a 90-day plan.
- **Integrity:** no advice to fabricate experience, inflate titles, have AI sit an interview for you, plagiarise projects, or misrepresent AI-written work as your own unaided work. Disclose AI assistance honestly where it matters; show that you can explain and verify every line you submit.
- **Not affiliated** with any employer, platform, certification body or government programme. Name platforms and programmes as examples, not endorsements.

## Reusing the library (the main design rule)

The library already teaches most of the engineering. **Do not re-teach it.** In each lesson, teach the hiring view of a skill — what "good enough for a junior" looks like, how it is tested in interviews, how to prove it in a portfolio — and then point to the lesson that builds it, with a relative link, e.g.
`[*System Design for Vibe Coders*, lesson 4.4 — Rollback, staging, and release gates](../vibe/index.en.html#l4-4)`.
The full catalogue of courses, lessons and link formats is in `LIBRARY.md` (provided to writers). Rules:
- Link only to lessons that exist in the catalogue. Prefer one precise link over five vague ones.
- The two new sister courses, *Data Engineering & Analytics: Zero to Hero* (`../data/index.html#/N.M`) and *Cloud & DevOps: Zero to Hero* (`../cloud/index.html#/N.M`), are being written at the same time; link to them only by **module** using the module plans below (e.g. `../data/index.html#/1.1` for SQL, `../cloud/index.html#/4.1` for CI pipelines).
- Module 2 (role paths) is the map of the library: each role-path lesson includes a **study path table** — the skills that role needs, the lesson(s) that teach each one, and the proof that shows it.

Sister-course module plans (for links):
- *Data Engineering & Analytics*: 0 Orientation · 1 SQL and data modelling (1.1 SQL, 1.2 modelling, 1.3 warehouses/lakes) · 2 Ingestion and pipelines (2.1 batch/ELT/CDC, 2.2 orchestration, 2.3 streaming) · 3 Transformation and quality (3.1 dbt, 3.2 data quality, 3.3 performance and cost) · 4 Analytics (4.1 metrics, 4.2 dashboards, 4.3 experiments) · 5 Data science and ML in production (5.1 notebook to pipeline, 5.2 evaluation and drift, 5.3 data for LLM apps) · 6 Governance, privacy and security · 7 Capstone, data career, practice exam.
- *Cloud & DevOps*: 0 Orientation · 1 Foundations (1.1 Linux/networking, 1.2 cloud fundamentals, 1.3 IAM) · 2 Containers and Kubernetes · 3 Infrastructure as code and GitOps · 4 CI/CD and releases · 5 Observability and reliability (5.1 telemetry, 5.2 SLOs and on-call, 5.3 incidents) · 6 Scale, cost and AI infrastructure · 7 Capstone, cloud career, practice exam.

## The running case: Najm Bank's Graduate Programme

**Najm Bank** is the fictional mid-sized Gulf bank (Qatar, the UAE and the EU) used across the library. Say it is fictional in lesson 0.3. Here we follow the **Najm Tech Graduate Programme** recruiting and onboarding its new cohort — and, for contrast, graduates applying to other employers (a Doha fintech startup **Sadeem Pay**, a regional telecom, a government digital agency, a multinational's regional office; all fictional or generic).

The cohort (use consistently; each makes realistic mistakes the reader learns from):
- **Omar** — CS graduate; strong at algorithms, has never deployed anything; targets software engineering.
- **Huda** — data science graduate; good at notebooks and models, weak at SQL and production; discovers data engineering.
- **Yousef** — computer engineering graduate; embedded and networks background; moves toward cloud/platform engineering.
- **Reem** — CS graduate who built side projects with AI coding agents; fast but cannot always explain her code; targets AI application engineering.
- **Mohammed** — career-switcher from a bootcamp; strong portfolio, no degree in the field.
Mentors and hiring side:
- **Khalid** — Engineering Manager at Najm Bank who hires juniors; the reader's mentor.
- **Aisha** — Talent Acquisition lead (recruiter); explains screens, CVs and offers.
- **Tariq** — engineering lead (also in the security course); runs technical interviews.
- **Dana** — lead data scientist; interviews data candidates.
- **Salem** — Head of Platform Engineering; interviews cloud candidates.

## Steps (the lesson tag)

Every lesson is tagged with one or two steps of the job-readiness journey, in English, in both languages: **Explore · Learn · Build · Prove · Apply · Interview · Start · Grow**. Header: `*Step: Explore*` or `*Step: Build, Prove*`.

## Module and lesson plan (numbers are fixed)

| Module | File | Lessons |
|---|---|---|
| 0 Orientation | 00-orientation.md | 0.1 The entry-level tech market in the AI era: what changed and what didn't · 0.2 The roles map: what software, AI, data, platform and security juniors actually do all day · 0.3 Meet the cohort, and how to use this course and the library |
| 1 The skills employers check | 01-skills.md | 1.1 The junior baseline: Git, reading code, debugging, testing and writing it down · 1.2 Building with AI coding agents without being carried by them · 1.3 Production thinking: the gap between "it runs on my laptop" and "it runs for users" |
| 2 Role paths through the library | 02-paths.md | 2.1 Software and full-stack engineer · 2.2 AI application engineer · 2.3 Data engineer, analyst and data scientist · 2.4 Cloud, platform, DevOps and security engineer |
| 3 Proof: the portfolio | 03-portfolio.md | 3.1 Projects that prove you can do the job: one capstone spec per role · 3.2 Your GitHub, READMEs and writing about your work · 3.3 Experience before your first job: internships, open source, freelancing, hackathons and competitions |
| 4 Getting seen | 04-getting-seen.md | 4.1 A CV that survives the applicant-tracking system and the six-second human scan · 4.2 LinkedIn, networking and referrals without awkwardness · 4.3 Where the jobs are: graduate programmes, job boards, startups, the public sector and the GCC market |
| 5 Interviews | 05-interviews.md | 5.1 The hiring loop, the recruiter screen and behavioural interviews (STAR) · 5.2 Technical interviews today: algorithms, live coding, take-homes and reviewing AI-written code · 5.3 System design, data and ML interviews for juniors |
| 6 Offer and the first 90 days | 06-first-job.md | 6.1 Offers: comparing, negotiating and choosing well · 6.2 Your first 90 days: onboarding, the first pull request and asking good questions · 6.3 Growing from junior to mid-level: feedback, ownership and continuous learning |
| 7 Hero: capstone and practice | 07-capstone.md | 7.1 Capstone: your 12-week job-readiness plan, from audit to offer · 7.2 Practice interview pack: 40 scenario questions |

Levels: 🟢 Beginner for Modules 0–2, 🟡 Intermediate for 3–5, 🔴 Advanced for 6–7 (use judgement per lesson).

## Facts to get right (and how to hedge)

- **Market:** describe trends qualitatively and hedge: AI coding tools have changed what entry-level work looks like; several 2025 analyses reported weaker hiring for early-career workers in AI-exposed occupations (e.g. Brynjolfsson, Chandar and Chen, Stanford Digital Economy Lab, Aug 2025, "Canaries in the Coal Mine?") — cite only as "reported", no figures unless you are certain; demand stays strong for people who can ship, verify and operate software, data and AI systems. No invented percentages.
- **ATS:** applicant-tracking systems (e.g. Workday, Greenhouse, Lever, SuccessFactors) parse CVs; simple one-column layouts, standard headings, real text (not images) and the job's own keywords help; "ATS score" tools are unreliable. Do not claim any ATS auto-rejects for a specific reason.
- **Interviews:** STAR (Situation, Task, Action, Result); data-structures-and-algorithms screens (LeetCode/HackerRank-style) remain common at large tech firms, less so elsewhere; take-homes and pair programming are common; many employers now allow or expect AI tools in some rounds and ban them in others — always ask, never assume; reviewing a flawed AI-generated pull request is an increasingly common exercise (present as a trend, hedge).
- **Certifications:** cloud (AWS, Azure, Google Cloud associate levels), Kubernetes (CKA/CKAD), security (CompTIA Security+), data (cloud data-engineer associate certifications) — useful signals for some roles, never a substitute for proof; names change, tell readers to check current names.
- **GCC market (hedge, no invented quotas):** workforce nationalisation programmes exist and shape hiring (Qatarization in Qatar, Emiratisation/Nafis in the UAE, Saudization/Nitaqat in Saudi Arabia); graduate and national development programmes at banks, energy companies, telecoms and government; regulated sectors (banking, government, energy, health) are large employers and value security, data protection (Qatar PDPPL — Law No. 13 of 2016) and governance awareness; bilingual Arabic/English technical communication is an advantage. Visa/sponsorship rules vary and change — say "check current rules".
- **Compensation:** never give salary figures; teach how to research ranges (recruiters, salary surveys, peers, job-ad ranges where published) and total compensation (base, allowances, bonus, equity at startups, benefits).

## File format (the build parses this — follow exactly)

```
# Module 1 — The skills employers check

*One-paragraph italic module intro: what the module covers and why, tied to the cohort.*

> **Steps:** Learn, Build — …(one line in the course's words)

---

# 1.1 — The junior baseline: Git, reading code, debugging, testing and writing it down
*Level: 🟢 Beginner* · *Prerequisites: 0.1, 0.2* · *Step: Learn, Build*

## ⚡ In 60 seconds
- 4–6 bullets: what it is, the rule that matters most, the decision cue, the biggest trap.

## 🧭 Why it matters
A cohort scenario (or a widely reported public situation) that makes the topic unavoidable. 1–3 paragraphs.

## 📐 How it works
### 🟢 The essentials
### 🟡 Going deeper
### 🔴 Expert view
(Plain explanations first; define every term on first use; tables, checklists, before/after examples (a weak vs strong CV bullet, a weak vs strong README, a weak vs strong interview answer); short code snippets only where they help; one mermaid diagram where it genuinely helps. Mermaid: flowchart or sequence only, `flowchart LR` or `TD`, short labels in double quotes, no parentheses inside labels.)

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **STAR method** | … | … |
(3–8 rows. The first cell MUST start with the name in bold — e.g. **STAR method**, **Story bank**, **Project README template**, **Conventional Commits**, **LeetCode**, **Applicant-tracking system (ATS)**, **Brag document** — optionally followed by a short credit in parentheses. Keep bold names identical wherever the same item appears; they build the toolkit catalogue.)

## 🏛️ In practice at Najm Bank
The artefact this lesson produces, as used in Najm's graduate programme or by a cohort member: a skills audit, a study-path table, a project spec, a CV section, an outreach message, an interview story, a scoring rubric, an offer comparison, a 30-60-90 plan. Concrete, reusable, in a table or a short template.

## 🛠️ Exercises
Three graded exercises: 🟢 …, 🟡 …, 🔴 …, each with a "*Done when:*" line that is checkable (a file exists, a link works, a peer could verify it).

## ⚠️ Mistakes and traps
4–6 bullets: the trap, then what to do instead.

## 🧾 Recap
4–6 bullets.

## ✍️ Check yourself
Five multiple-choice questions (at least three scenario-based, set with the cohort or a neutral company). Format:

**1. Question text?**

- A. …
- B. …
- C. …
- D. …

<details><summary>Answer</summary>

**B.** Why B is right, and why the tempting distractor is wrong. (Pointer to the section.)

</details>

## 📚 References
Primary and reputable sources only (official docs of tools and platforms, university career services, government labour-market and nationalisation-programme sites, published research such as arxiv.org or ssrn.com papers, well-known engineering-ladder and interviewing guides published by companies). Plain links; no invented URLs — link to a top-level page if unsure of the deep link. Library links (relative) may also appear here.
```

- Separate lessons with a `---` line.
- Lesson 7.2 (practice interview pack) follows the same outer format but its body is: ⚡ (how to use it), then `## ✍️ Practice exam` with 40 questions numbered 1–40 in the same Q/A format, spread across the modules (scenario-based: which project to build, which CV bullet is stronger, how to answer, which offer to take, what to do in week two), each answer ending with its step and the lesson to review, e.g. *(Interview · 5.1)*; then 🧾 and 📚. Its 🧰/🏛️/🛠️/⚠️ sections may be short.

## Style

- Plain, direct English; short sentences; warm but honest; define jargon on first use; no hype, no fear, no filler.
- Write for someone anxious about getting a first job: specific next actions, not motivation.
- Lengths: 2,000–3,500 words per lesson (7.2 excepted). Every lesson's five questions must be answerable from that lesson.
- Use the running cast consistently. Do not start any non-quiz line with `**N.` (bold number + dot).
