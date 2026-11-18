# Secure AI & Application Security: Zero to Hero

**Secure the app and the AI inside it. A free, bilingual course that takes you from zero to confident defender of web apps, APIs, cloud systems, LLM applications and AI agents.**

> **Defensive and educational.** Every attack in this course is explained so you can recognise it, test for it and prevent it. Test only systems you own or have written permission to test. Practise on local labs and deliberately vulnerable training apps.

<!-- study-time -->
**Study time for the whole course: about 220 hours** (estimate: reading plus hands-on work, summed over every lesson). At about 6 hours a week that is roughly 37 weeks. Each lesson shows its own split; a pilot with real learners will replace these estimates.
<!-- /study-time -->

## What this is

Most breaches still come through a short list of doors: a missing access check, an injectable query, a leaked key, an unpatched dependency, a misconfigured cloud bucket. AI has added new doors, and now they are open too. A chatbot can be talked into revealing its instructions. An assistant that reads documents can be steered by text hidden inside them. An agent with tools can be tricked into acting for an attacker. A coding agent can confidently write vulnerable code or install a package that does not exist.

This course teaches you to close those doors. It covers how attackers think and how breaches really happen, threat modelling, the classic web, API, identity, mobile and cloud weaknesses and their fixes, cryptography and secrets for builders, a secure development life cycle and software supply chain, and the attack surface of LLM apps and agents. It ends with detection, incident response and leading a security programme. It is written for developers (including people who build with AI coding agents), architects, engineering and product managers, analysts moving into AppSec or AI security, and anyone who owns a system in a bank, a government body or an enterprise. It assumes no security background.

## How every lesson works

Every lesson has the same ten parts, so you always know where you are:

| Part | What you get |
|---|---|
| ⚡ **In 60 seconds** | The lesson in five bullets: what it is, the rule that matters most, the decision cue and the biggest trap. |
| 🧭 **Why it matters** | A situation at Najm Bank, or a real public incident, that makes the topic unavoidable. |
| 📐 **How it works** | The ideas, climbing a ladder: 🟢 *The essentials* → 🟡 *Going deeper* → 🔴 *Expert view*, with vulnerable and fixed code side by side. |
| 🧰 **The toolkit** | The controls, standards and tools that apply: what each does and when to reach for it. |
| 🏛️ **In practice at Najm Bank** | The artefact this lesson produces: a threat model, a secure-coding rule, an access-control matrix, a detection rule, a runbook. |
| 🛠️ **Exercises** | Three graded exercises (🟢 🟡 🔴), each with "done when" criteria. |
| ⚠️ **Mistakes and traps** | What goes wrong in practice, and what to do instead. |
| 🧾 **Recap** | The takeaways worth remembering. |
| ✍️ **Check yourself** | Five questions, mostly scenarios, with hidden answers and explanations. |
| 📚 **References** | OWASP, MITRE, NIST, RFCs, papers and other primary sources. |

Every lesson is tagged with its **security life cycle phase**: Plan, Design, Build, Test, Deploy, Operate, Respond or Govern. The [toolkit catalogue](./TOOLKIT.md) collects every control, standard and tool in one place.

## The running case: Najm Bank's security team

The course follows the **Application & AI Security** team at **Najm Bank**, the fictional Gulf bank used across this library. The team protects **Najm Mobile** and its public API, the **SME Portal** for business customers, **Najm Assist** (the LLM assistant growing into an agent with tools), the **Credit Memo Copilot** (internal GenAI with retrieval over bank documents), the **Smart Alerts** fraud model, and the bank's cloud platform and AI coding agents. **Noura**, Head of Application & AI Security, is your mentor. By the capstone you will have secured Najm Assist from threat model to incident drill.

## The path from zero to hero

| Stage | Modules | You will be able to… |
|---|---|---|
| 🟢 **Foundations** | 0–1 | Explain assets, attackers and risk, how breaches happen, and model threats with STRIDE. |
| 🟡 **Practitioner** | 2–7 | Find and fix web, identity, API, mobile, crypto, secrets, pipeline and cloud weaknesses. |
| 🔴 **Hero** | 8–12 | Secure LLM apps and agents, red-team AI, detect and respond to incidents, lead a security programme, and sit a 60-question practice exam. |

**Choose your path.** You do not have to do everything. Lesson 0.3 explains each route.

| You are… | Suggested path |
|---|---|
| A developer, including with AI coding agents | Modules 0–6, then 8.1–8.2 and 9; every 🟡 exercise on your own code or the starter lab |
| An architect | Modules 0, 1, 3, 7, 8 and 9.1–9.3; a threat model for each system you own |
| A product or engineering manager | 0, 1.3, 6.1, 8.1–8.2, 9.1–9.2, 10.1–10.2 and 11; the paper route for hands-on exercises |
| A security analyst moving into AppSec or AI security | The 12.3 practice exam first; then deep on 2–4 and 8–9 |
| A bank, government or enterprise system owner | 0, 1, 5.3, 7.1, 9.1, 10.1–10.2 and 11; the paper route |

**Time.** Reading the whole course takes about 15 hours. With the 🟢 and 🟡 exercises it is roughly 120 hours, about five hours a week for six months; the 🔴 exercises add about 100 more. **No code?** Every hands-on exercise has a paper route: review a supplied change or artefact instead of building it. **Before you start**, lesson 0.3 sets up the free practice lab (OWASP Juice Shop in Docker) and the course's offline [starter lab](./lab/README.md) for the AI exercises.

## Companion courses

This course is the security layer of the library. Where a lesson touches system design, SaaS building blocks, agents, governance law or product decisions, it points to the companion course instead of repeating it: *System Design for Vibe Coders*, *SaaS Building Blocks*, *Production AI Agents*, *AI Governance: Zero to Hero* and *AI Product Management: Zero to Hero*.

## Two languages

Every lesson is available in English and Arabic. In the Arabic edition, technical terms carry their English name in parentheses, for example «حقن الموجّهات (prompt injection)», because the standards, tools and advisories you will work with are in English.

## Where to go next

Open the course map, or start with lesson 0.1.
