# AI Product Management: Zero to Hero — authoring guide

This is the contract every lesson follows. It is not published.

## What the course is

A free, bilingual (English/Arabic) course that takes a reader from zero to "hero" in **product management for AI**: finding problems worth solving with AI, understanding what the technology can and cannot do, designing trustworthy AI experiences, specifying and evaluating AI features, launching them safely, measuring value and cost, and leading AI product strategy and teams.

- **Audience:** product managers moving into AI; engineers, designers, data scientists and business owners who have to act as product people on AI work; founders; managers in banks, government and enterprises in the GCC who sponsor AI products. No technical background assumed at the start. By the end the reader can run an AI product from idea to scale and hold their own with engineers, data scientists, risk and executives.
- **Not a certification prep course.** It is not affiliated with any certification body. It uses well-known public frameworks and credits their authors.
- **Companion courses in the same library** (link to them where useful, by name, not by URL): *System Design for Vibe Coders*, *SaaS Building Blocks*, *Production AI Agents* (the agentic course) and *AI Governance: Zero to Hero*. This course is the product layer on top of them. Do not re-teach governance or engineering in depth; point to the companion course in one line and stay on the product decision.

## The running case: Najm Bank's AI product team

**Najm Bank** is a fictional mid-sized Gulf bank (retail, SME and corporate lending) with customers in Qatar, the UAE and the EU. The same bank appears in the AI governance course; here we sit in its **Digital & AI Products** team. Say it is fictional in lesson 0.3.

Products (use them consistently):
- **Credit Memo Copilot** — a GenAI assistant that drafts credit memos for relationship managers (internal, enterprise workflow). The flagship example.
- **Najm Assist** — the customer-facing assistant in the mobile app (answers questions, then grows into an agent that can do tasks like freezing a card or disputing a transaction).
- **SME Instant Finance** — an ML model that pre-approves small invoice-financing requests (a predictive, not generative, product; high-risk credit decisions).
- **Smart Alerts** — fraud and spending alerts (classic ML, precision/recall trade-offs, alert fatigue).
- **Staff GenAI** — the internal assistant for employees (build vs buy, adoption, change management).

Cast:
- **Rania** — Head of AI Products; the reader's mentor.
- **Faisal** — a new AI product manager (the reader's peer; makes the mistakes the reader should avoid).
- **Hessa** — product designer (UX research, AI interaction patterns).
- **Tariq** — engineering lead (platform, cost, latency).
- **Dana** — lead data scientist (models, evaluation).
- **Khalid** — Head of Retail Lending (business owner, sceptical, wants ROI).
- **Layla** — Head of AI Governance (risk tiering, approvals; from the governance course).
- **Sara** — Data Protection Officer. **Yusuf** — procurement. **Omar** — Chief Data Officer.

## Product lifecycle stages (the lesson tag)

Every lesson is tagged with one or two stages, in English, in both languages: **Discover · Define · Design · Build · Evaluate · Launch · Grow · Lead**. In the lesson header: `*Stage: Discover*` or `*Stage: Build, Evaluate*`.

## Module and lesson plan (numbers are fixed)

| Module | File | Lessons |
|---|---|---|
| 0 Orientation | 00-orientation.md | 0.1 What AI product management is, and what it is not · 0.2 How AI products differ: probabilistic, data-hungry, costly per use, trust-bound · 0.3 Meet Najm Bank's AI product team, and how to use this course |
| 1 AI literacy for product people | 01-ai-literacy.md | 1.1 Machine learning, generative AI, LLMs and agents: what each is good for · 1.2 Capabilities and limits: errors, hallucination, context, latency and cost · 1.3 The build spectrum: prompt, retrieval (RAG), fine-tune, train, or buy |
| 2 Finding problems worth solving | 02-discovery.md | 2.1 Discovery for AI: jobs, workflows and where AI fits · 2.2 Scoring and choosing use cases: value, feasibility, risk · 2.3 When not to use AI, and killing ideas early |
| 3 Data as the product's foundation | 03-data.md | 3.1 Data readiness: do we have what the product needs? · 3.2 Feedback loops, flywheels and learning products · 3.3 Privacy, consent and data rights: what the PM must own |
| 4 Designing AI experiences | 04-design.md | 4.1 Levels of automation: suggest, draft, decide, act · 4.2 Designing for trust: expectations, explanations, errors and recovery · 4.3 Conversational and agentic experiences |
| 5 Specifying and building | 05-build.md | 5.1 The AI product spec: behaviour, quality bars and evals as requirements · 5.2 Prototyping fast and working with ML and AI engineers · 5.3 Prompts, context and tools as product surface |
| 6 Evaluation: knowing it works | 06-evaluation.md | 6.1 Quality you can measure: metrics, golden sets and error analysis · 6.2 LLM-as-judge, human review and red-teaming · 6.3 Online evaluation: experiments, A/B tests and staged rollouts |
| 7 Launching AI products | 07-launch.md | 7.1 Launch readiness: guardrails, governance gates and support · 7.2 Go-to-market: positioning, pricing signals and enablement · 7.3 Adoption and change management inside the enterprise |
| 8 Metrics, economics and growth | 08-metrics.md | 8.1 Product metrics for AI: value, quality, adoption, trust · 8.2 Unit economics: cost to serve, pricing models and margins · 8.3 Monitoring, drift and the iteration loop after launch |
| 9 Strategy and leadership | 09-strategy.md | 9.1 AI product strategy and defensibility · 9.2 Roadmaps under uncertainty: bets, platforms and model change · 9.3 Teams, roles and operating model for AI products · 9.4 Responsible AI and regulation: the PM's part |
| 10 Hero: capstone and practice exam | 10-capstone.md | 10.1 Capstone: take Najm Assist from idea to scale · 10.2 The AI PM career: interviews, portfolio and growth · 10.3 Practice exam: 60 scenario questions |

Levels (zero → hero): 🟢 Beginner for Modules 0–1, 🟡 Intermediate for 2–6, 🔴 Advanced for 7–10 (use judgement per lesson).

## Facts to get right (and how to hedge)

State only what you are confident is true. Model prices, context windows, benchmark scores and vendor features change monthly: teach the **method** (how to estimate cost per task, how to compare models), not today's numbers. When you use a number, label it illustrative ("say $X per million tokens") or dated ("at the time of writing (2026)"). Never invent statistics, quotes, studies or company results.

Frameworks — credit the source on first use:
- **Jobs to be Done** (Clayton Christensen; Anthony Ulwick's Outcome-Driven Innovation). **Opportunity Solution Tree** and continuous discovery (Teresa Torres, *Continuous Discovery Habits*, 2021). **Four big risks: value, usability, feasibility, business viability** (Marty Cagan, *Inspired*). **Double Diamond** (UK Design Council, 2005). **Lean Startup / MVP / build-measure-learn** (Eric Ries, 2011). **RICE** prioritisation (Intercom). **Kano model** (Noriaki Kano, 1984). **North Star metric**; **HEART** framework (Google: Happiness, Engagement, Adoption, Retention, Task success; Rodden, Hutchinson and Fu, 2010); **AARRR** pirate metrics (Dave McClure). **Wizard of Oz** prototyping. **Levels of automation** (Sheridan and Verplank, 1978).
- **Human-AI interaction:** Google **People + AI Guidebook** (PAIR); Microsoft **Guidelines for Human-AI Interaction** (18 guidelines, Amershi et al., CHI 2019); Apple Human Interface Guidelines on machine learning.
- **Experimentation:** Kohavi, Tang and Xu, *Trustworthy Online Controlled Experiments* (2020): OEC, guardrail metrics, sample ratio mismatch, novelty effects.
- **Evaluation:** precision, recall, F1, confusion matrix, ROC/AUC, calibration; golden (reference) datasets; error analysis; LLM-as-judge (e.g. Zheng et al., 2023, "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena") and its biases (position, verbosity, self-preference); human evaluation with rubrics and inter-rater agreement; red-teaming.
- **Technology:** tokens and context windows; temperature; retrieval-augmented generation; fine-tuning; embeddings; tool use / function calling; agents; the **Model Context Protocol (MCP)** (introduced by Anthropic, Nov 2024) as a standard way to connect models to tools and data; open-weight vs closed models; latency and cost per request. Keep it vendor-neutral; name vendors only as examples.
- **Governance hooks** (one line each, then point to *AI Governance: Zero to Hero*): EU AI Act risk tiers and that credit scoring of individuals is high-risk; GDPR Art. 22 on solely automated decisions; NIST AI RMF; ISO/IEC 42001; Qatar PDPPL (Law No. 13 of 2016); QCB's AI guideline for financial institutions (no invented clause numbers).

Real cases you may use (well documented only; hedge figures):
- Air Canada chatbot misstatement — *Moffatt v. Air Canada* (2024), airline held liable.
- A Chevrolet dealer's website chatbot agreeing to "sell" a car for $1 after prompt manipulation (Dec 2023).
- DPD's delivery chatbot swearing and criticising the company after an update (Jan 2024).
- New York City's MyCity business chatbot giving answers that contradicted the law (reported 2024).
- Google's Bard launch demo with a factual error about the James Webb telescope (Feb 2023).
- Zillow Offers wound down in 2021 after its pricing algorithm mispriced homes (large write-downs).
- IBM Watson Health: large investment, units sold in 2022 — the gap between demo and workflow.
- Klarna's AI assistant (announced Feb 2024 as handling a large share of customer chats; in 2025 the company said it would bring more human service back) — use as a lesson on measuring quality, not only cost.
- GitHub Copilot: GitHub's 2022 controlled study reported developers completing a task faster with Copilot — cite as GitHub's own study.
- Outcome-based pricing: Intercom's Fin priced per resolved conversation (from 2023); Salesforce Agentforce launched with per-conversation pricing (2024) — hedge exact prices.
- Morgan Stanley's internal GPT-4 assistant for financial advisers (2023) — enterprise knowledge copilot.
- Duolingo Max (2023) — GenAI features priced as a premium tier.

## File format (the build parses this — follow exactly)

```
# Module 4 — Designing AI experiences

*One-paragraph italic module intro: what the module covers and why, tied to Najm Bank.*

> **Stages:** Design — …(one line in the course's words)

---

# 4.1 — Levels of automation: suggest, draft, decide, act
*Level: 🟡 Intermediate* · *Prerequisites: 1.2, 2.1* · *Stage: Design*

## ⚡ In 60 seconds
- 4–6 bullets: what it is, the idea that matters most, the decision cue, the biggest trap.

## 🧭 Why it matters
A Najm Bank scenario (or a real public case) that makes the topic unavoidable. 1–3 paragraphs.

## 📐 How it works
### 🟢 The essentials
### 🟡 Going deeper
### 🔴 Expert view
(Plain explanations first; define every term on first use; tables and one mermaid diagram where it genuinely helps. Mermaid: flowchart or sequence only, `flowchart LR` or `TD`, short labels in double quotes, no parentheses inside labels.)

## 🧰 The toolkit
| Tool or framework | What it is and does | When to reach for it |
|---|---|---|
| **Opportunity Solution Tree** (Teresa Torres) | … | … |
(3–8 rows. The first cell MUST start with the tool's name in bold — e.g. **Jobs to be Done**, **RICE**, **Golden set**, **LLM-as-judge**, **HEART framework**, **Cost-per-task model** — optionally followed by a short credit in parentheses. Keep bold names identical wherever the same tool appears; they build the toolkit catalogue.)

## 🏛️ In practice at Najm Bank
The product artefact this lesson produces: a one-page opportunity brief, a use-case scorecard, an eval plan, a PRD section, a launch checklist, a pricing sheet, a metrics tree, a roadmap slide. Concrete, reusable, in a table or a short template.

## 🛠️ Exercises
Three graded exercises: 🟢 …, 🟡 …, 🔴 …, each with a "*Done when:*" line.

## ⚠️ Mistakes and traps
4–6 bullets: the trap, then what to do instead.

## 🧾 Recap
4–6 bullets.

## ✍️ Check yourself
Five multiple-choice questions (at least three scenario-based, set at Najm Bank or a neutral company). Format:

**1. Question text?**

- A. …
- B. …
- C. …
- D. …

<details><summary>Answer</summary>

**B.** Why B is right, and why the tempting distractor is wrong. (Pointer to the section.)

</details>

## 📚 References
Books, papers and official product/research pages only (e.g. pair.withgoogle.com, microsoft.com/research, nist.gov, eur-lex.europa.eu, producttalk.org, svpg.com, experimentguide.com, arxiv.org for papers). Plain links; no invented URLs — link to a top-level page if unsure of the deep link.
```

- Separate lessons with a `---` line.
- Lesson 10.3 (practice exam) follows the same outer format but its body is: ⚡ (how to take it), then `## ✍️ Practice exam` with 60 questions numbered 1–60 in the same Q/A format, spread across the stages (about 7–8 per stage), each answer ending with its stage and the lesson to review, e.g. *(Evaluate · 6.1)*; then 🧾 and 📚. Its 🧰/🏛️/🛠️/⚠️ sections may be short.

## Style

- Plain, direct English; short sentences; define jargon on first use; no hype; no filler. Explain *why*, not just *what*. Opinionated where practice is clear, balanced where it is not.
- Product judgement over theory: every lesson must leave the reader able to make a decision or produce an artefact.
- Lengths: 2,000–3,500 words per lesson (10.3 excepted). Every lesson's five questions must be answerable from that lesson.
- Use the running cast consistently.
