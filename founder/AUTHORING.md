# Founder's Playbook for AI-First Builders — authoring guide

This is the contract every lesson follows. It is not published.

## What the course is

A free, bilingual (English/Arabic) course for people who build a product with AI tools and now have to turn it into a business: **a solo founder or a team of up to five, with no organisation behind them**. Many readers do not code; the library's *System Design for Vibe Coders* is their engineering companion and this course is the business half.

- **Audience:** AI-first builders (vibe coders, no-code and low-code builders, technical and non-technical solo founders, small-team founders), and the people who coach them.
- **Not** product management inside a company (that is *AI Product Management: Zero to Hero*, `../aipm/`), not billing code (*SaaS Building Blocks*, `../saas/`), not shipping and operating software (*System Design for Vibe Coders*, `../vibe/`). Teach the founder's decision and link to those courses for depth. Never re-teach them.
- **Honest, not hype.** Never promise income, funding, users, jobs or outcomes. No "make money with AI" framing, no growth hacks that rely on deception, no spam, no fake reviews, no invented testimonials. Failure is normal; the course teaches how to find out cheaply that an idea is wrong.
- **Practical judgement.** Every lesson leaves the reader with a decision made or an artefact produced: a problem statement, an interview script, a smoke-test page brief, a kill list, a price test plan, a cash table, an outreach message, a launch checklist, a support policy, a terms-and-privacy question list, a handover pack.
- **Not advice.** The course is education. It is **not legal, tax, accounting, investment or financial advice**, and rules differ by country and change. Wherever a lesson reaches law, tax, company registration, data protection, IP or investment, teach the *concepts and the questions to ask a qualified professional*, never "the rule is X". Say this plainly in lesson 0.3 and in the lessons of modules 3 and 6.
- **Integrity:** no advice to mislead customers, hide AI use where disclosure is expected, scrape in breach of terms, fabricate traction, or misrepresent AI-written work. Disclose AI use to customers where it matters.
- **Not affiliated** with any platform, payment provider, investor, accelerator, bank, government programme or regulator. Name tools and platforms as examples, never as endorsements. Never name a real company as the example of success or failure unless a primary source is cited in the lesson's References **and** a row exists in the claims register (see below). Prefer the labelled fictional cases below.

## The running case: Tick

**Tick** is a fictional appointment-reminder app for small service businesses (salons, tutors, clinics, repair shops). Say it is fictional in lesson 0.1. The cast (use consistently; each makes realistic mistakes the reader learns from):

- **Layla** — the founder. Non-technical, built Tick's first version by directing an AI coding agent. Fast, but tends to skip checking.
- **Nadia** — runs a small salon; Tick's first design-partner customer.
- **Sam** — freelance designer and contractor Layla hires for the landing page and logo.
- **Mona** — a founder-in-residence at a fictional co-working space, Layla's mentor.
- **Hana** — an accountant (appears only to show *what to ask a professional*).
- **Rashid** — a lawyer (appears only to show *what to ask a professional*).

Neutral setting: do not tie Tick to one country. Gulf, European, South-Asian or other examples are allowed only as clearly labelled illustrations. No real bank, employer or named organisation as the case.

## Reusing the library (the main design rule)

The library teaches most of the engineering and a lot of product. **Do not re-teach it.** In each lesson, teach the founder's view (what to decide, what proof to ask for) and link out for depth, with a relative link in the form
`[*System Design for Vibe Coders*, lesson 4.4 — Rollback, staging, and release gates](../vibe/index.en.html#l4-4)`.
`../career/LIBRARY.md` is the catalogue of link formats and the lessons that exist for older courses (it predates *AI-Native Engineer*, *Building AI Applications & Agents* and *Software Testing*; for those, find real lessons by listing the headings in `../<course>/modules/*.md`). Rules:

- Link only to lessons that exist: check the heading in the target file before linking.
- Use the link text "*Course name*, lesson N.M — title". Prefer one precise link per topic.
- A link supplements a lesson; it never replaces teaching the decision here.
- Course folders: `vibe` (`../vibe/index.en.html#lN-M`), `saas`, `aigp`, `aipm`, `secai`, `career`, `data`, `cloud`, `testing`, `aiapps`, `ainative` (`../<course>/index.html#/N.M`).

## Steps (the lesson tag)

Every lesson is tagged with one or two steps of the founder journey, in English in both languages: **Explore · Validate · Scope · Price · Sell · Launch · Protect · Run**. Header: `*Step: Validate*`. Steps by module: M0 Explore · M1 Explore, Validate · M2 Scope · M3 Price · M4 Sell · M5 Launch · M6 Protect · M7 Run · M8 all.

## Module and lesson plan (numbers are fixed)

| Module | File | Lessons |
|---|---|---|
| 0 Orientation | 00-orientation.md | 0.1 What changed, and what did not, when AI builds the product · 0.2 The founder's map: eight steps and the Tick cast · 0.3 How to use this course, and what it is not (not legal, tax or investment advice) |
| 1 A problem worth solving | 01-problem.md | 1.1 Pick a problem you can reach: customer, pain, frequency · 1.2 Customer interviews that find the truth · 1.3 AI-assisted research without fooling yourself · 1.4 Smoke tests: a landing page and a pre-sale before you build |
| 2 The smallest sellable thing | 02-scope.md | 2.1 One job, one customer: scope and the kill list · 2.2 Build, buy or borrow · 2.3 Directing an agent to a first version, and checking it |
| 3 Money | 03-money.md | 3.1 Unit economics in plain words, including AI and model costs · 3.2 Pricing: choose, test and change a price · 3.3 Cash, runway and invoicing: what to ask your accountant |
| 4 First customers | 04-customers.md | 4.1 Where your first ten customers are · 4.2 Outreach and sales calls without spam · 4.3 Onboarding: the first result, fast |
| 5 Launch and support | 05-launch.md | 5.1 A launch you can undo · 5.2 Support at one-person scale with AI: boundaries, escalation, disclosure · 5.3 When something breaks: telling customers, and the post-incident note |
| 6 Trust, law and risk | 06-trust.md | 6.1 What you promise: terms, privacy notice and refunds, drafted with AI and checked by a professional · 6.2 Customer data and AI models: what you may send, consent, retention · 6.3 Who owns what: AI-written code, contractors, open-source licences, names (questions for a lawyer) |
| 7 Running a small company with AI agents | 07-run.md | 7.1 What to hand to agents or people, and what to keep · 7.2 Costs, vendors and lock-in · 7.3 Key-person risk: access, backups and a 30-minute handover pack |
| 8 Capstone and practice | 08-capstone.md | 8.1 Capstone: your venture file and 30-day plan · 8.2 Practice exam: 40 scenario questions |

27 lessons. Levels: 🟢 Beginner for Modules 0–2, 🟡 Intermediate for 3–5, 🔴 Advanced for 6–8 (use judgement per lesson).

## Facts to get right (and how to hedge)

- **No statistics without a source.** Any number about markets, failure rates, conversion, pricing, churn, costs of tools or time saved needs a primary or reputable source cited in the lesson's References and a row in the claims register. Otherwise do not state it. Tick's own numbers (prices, costs, counts) are **illustrative** and must be labelled "illustrative figures, not benchmarks".
- **Prices and plans of tools change.** Never quote a vendor price or limit as current. Teach how to check the vendor's pricing page and how to compute the cost per customer from it.
- **Law, tax, registration, consumer protection, data protection, IP, employment, export rules** vary by country and change. Name the *kind* of rule (for example "data protection law such as the EU GDPR or a national equivalent"), say that rules differ, and give the reader the **question to ask a qualified professional** and what to bring to the meeting. Never state a legal conclusion. Who owns AI-generated output, and what training or terms allow, is unsettled or varies: say so and tell the reader to read the tool's terms and ask a lawyer.
- **Payments and platforms:** name categories (payment provider, invoicing tool, email service, analytics) and at most one or two examples as illustrations, never endorsements.
- **Investment and funding:** teach what a founder should understand (what investors ask for, what a term sheet contains at a high level) only in the capstone context; never advise to raise or not to raise; never promise funding.
- **Customer research ethics:** consent, no deception in interviews, no scraping in breach of site terms, no unsolicited bulk messaging; say that anti-spam and marketing laws exist and vary.

## File format (the build parses this — follow exactly)

```
# Module 1 — A problem worth solving

*One-paragraph italic module intro: what the module covers and why, tied to Layla and Tick.*

> **Steps:** Explore, Validate — …(one line in the course's words)

---

# 1.1 — Pick a problem you can reach: customer, pain, frequency
*Level: 🟢 Beginner* · *Prerequisites: 0.1, 0.2* · *Step: Explore*

## ⚡ In 60 seconds
- 4–6 bullets: what it is, the rule that matters most, the decision cue, the biggest trap.

## 🧭 Why it matters
A scenario with Layla (or a widely reported public situation, with source) that makes the topic unavoidable. 1–3 paragraphs.

## 📐 How it works

### 🟢 The essentials
### 🟡 Going deeper
### 🔴 Expert view
(Plain explanations first; define every term on first use; tables, checklists, before/after examples (a weak vs strong problem statement, interview question, price page, support reply); no code needed; one memorable rule per lesson.)

## 🧰 The toolkit
| Resource, tool or template | What it is and does | When to reach for it |
|---|---|---|
| **Problem statement template** | … | … |
(3–8 rows. The first cell MUST start with the name in bold, e.g. **Interview script**, **Kill list**, **Unit-economics sheet**, **Launch checklist**, **Handover pack**; names must match across languages. Tools are examples, not endorsements.)

## 🏛️ In practice with Tick
The artefact this lesson produces, as Layla (or another cast member) used it: a problem statement, an interview log, a smoke-test brief, a kill list, a price test plan, a cash table, an outreach message, an onboarding checklist, a launch checklist, a support policy, a question list for the accountant or lawyer, a handover pack. Concrete, illustrative, labelled as fictional.

## 🛠️ Exercises
Three graded exercises: 🟢 …, 🟡 …, 🔴 …, each with a "*Done when:*" line that is checkable (a file exists, a message was sent, a peer could verify it).

## ⚠️ Mistakes and traps
4–6 bullets: the trap, then what to do instead.

## 🧾 Recap
4–6 bullets.

## ✍️ Check yourself
Five multiple-choice questions (at least three scenario-based, set with Layla and Tick). Format:

**1. Question text?**

- A. …
- B. …
- C. …
- D. …

<details><summary>Answer</summary>

**B.** Why B is right, and why the tempting distractor is wrong. (Pointer to the section.)

</details>

## 📚 References
Primary and reputable sources only (official documentation of tools and platforms, government and regulator guidance pages, published research, well-known books and reputable writers on starting businesses). Each reference line has a working URL you checked or a full citation; never invent a URL or a title.
```

- Separate lessons with a `---` line.
- Lesson 8.2 (practice exam) follows the same outer format but its body is: ⚡ (how to use it), then `## ✍️ Practice exam` with 40 questions numbered 1–40 in the same Q/A format, spread across all modules and answerable from the lessons.
- Answer options: the correct option must **not** be predictable by length, position, specificity or hedging. Make the options of an item similar in length and detail, make every distractor plausible and plainly wrong on reading, and spread the key letters (A–D) about evenly across the 5 items of each lesson and across the exam. The cue audit (`python3 scripts/qa/quiz_cues.py`, see `scripts/qa/README.md`) must stay within its limits.

## Style

- Plain, direct English; short sentences; warm but honest; define jargon on first use; no hype, no fear, no filler.
- Write for someone who has built something and is nervous about selling it: specific next actions, not motivation.
- Lengths: 2,000–3,500 words per lesson (8.2 excepted). Every lesson's five questions must be answerable from that lesson.
- Use the running cast consistently. Do not start any non-quiz line with `**N.` (bold number + dot).
- Every lesson states a measurable outcome in its first bullet or opening paragraph ("After this you can …").
- Do not name any real person, company, bank or product as a case without a cited primary source. Never write an email address.

## Arabic edition

Written as Arabic by a careful writer, not translated word for word. See `TRANSLATING.md` (copy the rules in `../career/TRANSLATING.md`, adapted) and the standing rules: an English gloss in parentheses only on a **technical term at its first use in the lesson** (not on plain phrases, not repeated); product, protocol and acronym names stay in Latin letters without parentheses; the three-line header tags (`*Level`, `*Prerequisites`, `*Step`) keep the same English words as the English file where the builder needs them; any "DPO" is written with the Arabic word for protection (حماية) close by; diagrams (if any) run right to left. Each Arabic lesson keeps the exact structure of its English twin: `python3 founder/check_ar.py founder/modules/NN-x.md founder/modules/NN-x.ar.md` must pass.

## Claims register

Every number, law, regulation, case or study stated as fact in a lesson needs a row in `academy/claims/founder.md` with: the claim, the lesson, the source link, the date checked, the method ("opened the page" or "search summary"), and a review-by date. Facts known only from search summaries are described as "reported", never "verified". Writers return their rows to the lead; the lead assembles the file.
