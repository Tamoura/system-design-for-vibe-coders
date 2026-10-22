# A Practical Guide to Becoming an AI-Native Engineer

**A free, bilingual, hands-on course for software engineers who want to work well with AI coding agents: give them context, specify the work, verify what they produce, secure your setup, automate the loop, and stay accountable for everything that ships. Every lab is a real task with an offline grader.**

## What this is

Almost every engineer now has an AI agent that can read a repository, edit files, run commands and open a pull request. Using one is easy. Using one *well* is a skill: the engineers who get the most from agents are not the ones who type the least, but the ones who give the right context, write down what "done" means, work in small verified steps, and notice when the confident answer is wrong.

This course teaches that skill by practice. You join the **Payments Platform** team at **Najm Bank** (a fictional bank used across this library) and work through one codebase, **Najm Remit**, for fourteen weeks: onboarding to unfamiliar code, shipping features, reviewing an agent's pull request, fixing a production bug from its logs, taming legacy code, hardening your setup, automating your agent with hooks, skills and subagents, running agents in parallel, and writing your team's playbook.

You do not need an API key to do the labs. The lab kit (`ailab`) starts each task, and its hidden tests and checks grade your result offline. Use **Claude Code** (the course's worked example), any other agentic tool, or no agent at all: the grader only sees the work.

## The five habits

1. **Context first.** Tell the agent what it needs to know before you tell it what to do.
2. **Specify before you delegate.** Write down what "done" means, then plan.
3. **Small verified steps.** Check after every step; stop an agent early rather than late.
4. **Trust evidence, not fluency.** Tests, reproductions, diffs and logs are evidence. A confident paragraph is not.
5. **Automate the loop, keep the skill.** Turn repeated steps into commands and hooks, and keep practising the fundamentals so you can tell when the agent is wrong.

The loop is **specify → delegate → verify → integrate**, with context feeding every step and safety wrapping all of it.

## How every lesson works

Every lesson has the same ten parts:

| Part | What you get |
|---|---|
| ⚡ **In 60 seconds** | The lesson in a few bullets: what it is, the rule that matters most, the decision cue and the biggest trap. |
| 🧭 **Why it matters** | A situation at Najm Bank, or a well-documented public failure, that makes the topic unavoidable. |
| 📐 **How it works** | The ideas, climbing a ladder: 🟢 *The essentials* → 🟡 *Going deeper* → 🔴 *Expert view*. |
| 🧰 **The toolkit** | The tools, practices and patterns that apply: what each does and when to reach for it. |
| 🏛️ **In practice at Najm Bank** | The artefact the lesson produces; in labs, the ticket, how to start, how it is graded, the weekly deliverable and the group session. |
| 🛠️ **Exercises** | Three graded exercises (🟢 🟡 🔴), each with "done when" criteria and a note on whether it needs an agent. |
| ⚠️ **Mistakes and traps** | What goes wrong in practice, and what to do instead. |
| 🧾 **Recap** | The takeaways worth remembering. |
| ✍️ **Check yourself** | Five questions, mostly scenarios, with hidden answers and explanations. |
| 📚 **References** | Official documentation and primary sources; concept lessons add a short "Go deeper" list. |

Every lesson is tagged with its **focus**: Mindset, Context, Workflow, Verify, Secure, Automate or Team. The [toolkit catalogue](./TOOLKIT.md) collects every tool and pattern in one place.

## The lab kit: Najm Remit and `ailab`

**Najm Remit** is a small Python service (fees, exchange-rate quotes, limits, screening, a legacy ledger, notifications in English and Arabic) with an internal helper library, `najmkit`, that no AI model has ever seen. The kit is in `ainative/ailab/` in the course repository:

```text
python -m ailab list                       # the labs
python -m ailab start m04 --dir ~/ainative/m04   # a repository with the task, ready to work in
python -m ailab grade m04 --dir ~/ainative/m04   # hidden tests and checks, offline
```

Every lab says whether it needs an agent and gives a path without one. The labs are checked by the kit's own tests: each starts failing, and a reference solution makes it pass.

## The path

| Stage | Modules | You will be able to… |
|---|---|---|
| 🟢 **Foundations** | 0–3 | Explain what an AI-native engineer does differently, how coding agents really work and fail, give an agent the right context, and turn a vague ticket into a spec an agent can build from. |
| 🟡 **Practitioner** | 4–9, 11 | Run the daily loop, verify and review AI-written code, debug and onboard to unfamiliar code, change legacy code safely, secure your setup, and automate your agent with hooks, skills, subagents and headless scripts. |
| 🔴 **Hero** | 10, 12–14 | Run agents in parallel, set team practice and metrics, keep your own skills sharp, and take a change through the whole cycle. |

## Companion courses

*Building AI Applications & Agents* (if you build AI products rather than work with AI tools), *Software Testing: Zero to Hero in the AI Era*, *Secure AI & Application Security*, *Running AI Agents in Production*, *System Design for Vibe Coders*, *Cloud & DevOps*, *AI Governance*, *AI Product Management* and *From Graduate to Hired*.

## Two languages

Every lesson is available in English and Arabic. In the Arabic edition, technical terms carry their English name in parentheses, for example «هندسة السياق (context engineering)», because the tools, documentation and job ads you will work with are in English.

## Where to go next

Open the course map, or start with lesson 0.1.
