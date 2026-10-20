# Module 0 — Orientation: the lifecycle, your lab and your build partner

*Anyone can get an agent to answer a question in a demo. Shipping one that a bank will rely on is a different job, and this module shows you what that job is. Lesson 0.1 gives you the map: the eight-stage delivery lifecycle, ten properties that make an agent "enterprise-grade", the five layers of the course and the reading-group routine, all on the fictional Najm Desk engagement. Lesson 0.2 builds your lab: Python, the pinned SDK, the lab kit's offline mock, an API key, a spending cap and a smoke script that tells you which mode you are in. Lesson 0.3 teaches you to direct Claude Code as your build partner, with a spec, a plan, small steps and a reviewer's checklist, so that you understand everything it builds before you ship it.*

> **Layer:** Delivery — how an agent travels from a first conversation with a customer to a running, supportable product, plus the lab and the build partner you will use on the way.

---

# 0.1 — What it takes to ship an enterprise-grade agent: the delivery lifecycle, the layers and how this course works
*Level: 🟢 Beginner* · *Prerequisites: none* · *Layer: Delivery*

## ⚡ In 60 seconds
- Shipping an agent is a **lifecycle**, not a build: discover, design, build, evaluate, secure, ship, operate, hand over.
- **Enterprise-grade** means ten properties you can show evidence for, such as reliable, governed and supportable. "We are careful" is not evidence.
- A **chatbot** answers, a **workflow** follows a path your code defines, an **agent** chooses its own steps. Use the simplest that works.
- Many pilots stall after the build, because a demo only proves the first half.
- The course is a reading group, one module a week, on a **fictional** engagement, Najm Desk. Labs run offline and, unchanged, on the real API.
- Claude Code writes much of your code; you must still explain every line that ships.

## 🧭 Why it matters
Picture a pilot at Najm Bank that never reached its users. (The story is hypothetical, like every Najm story in the course.) A small team built **Ask HR**, a chatbot over the HR policies, and after six weeks the demo made the steering committee clap. Then it met the second half of the lifecycle. **Sara**, the Data Protection Officer, asked which staff details the prompts sent to the model provider. Nobody knew. **Layla** asked for the risk assessment. There was none. **Hamad's** team asked what stopped a pasted document from giving the bot new instructions. **Maha** asked who would be paged; the answer was "the developer", who had moved teams. The prompt lived in a notebook cell and, with no tests, nobody dared edit it. Four months later the pilot was paused. The model never failed. The delivery did.

As reported, in *Moffatt v. Air Canada* (2024) a British Columbia tribunal held an airline responsible for wrong information its website chatbot gave a customer. It is one ruling in one jurisdiction, but plan as if your organisation will answer for what its agent says, and ask your legal team early. "It works in the demo" is the start of the job. This lesson is your map: the lifecycle, a ten-point test for "enterprise-grade", the five layers and the reading-group routine.

## 📐 How it works

### 🟢 The essentials

**The delivery lifecycle.** An agent project moves through eight stages. Each ends with an artefact you can hand to someone, and each has a home in this course.

```mermaid
flowchart LR
    A["Discover<br/>Module 6"] --> B["Design<br/>Module 7"]
    B --> C["Build<br/>Modules 1 to 5, 8 to 11"]
    C --> D["Evaluate<br/>Module 12"]
    D --> E["Secure<br/>Module 13"]
    E --> F["Ship<br/>Module 14"]
    F --> G["Operate<br/>Module 15"]
    G --> H["Hand over<br/>Modules 15 and 16"]
    D -.->|"below the bar"| C
    G -.->|"what we learn"| A
```

| Stage | The question it answers | You hand over |
|---|---|---|
| **Discover** | What is the real problem, and should this be an agent? | An agent brief |
| **Design** | What may it do alone, and who approves what? | Architecture, agreed scope |
| **Build** | How do model, prompts, tools and loop fit together? | A working agent |
| **Evaluate** | Is it good enough, and will we notice if it stops being so? | Eval set, CI gate |
| **Secure** | What can go wrong, or be made to? | Threat model, guardrails |
| **Ship** | How does it reach users, and roll back? | Pipeline, release plan, budget |
| **Operate** | How do we see it, fix it, improve it? | Dashboards, runbook |
| **Hand over** | Who owns it tomorrow? | Training, support model, acceptance |

The course teaches the building blocks first, because you cannot scope what you cannot build; Module 6 then returns to discovery. The lifecycle is also a loop: a failed evaluation sends you back to build, and what operation teaches you feeds the next discovery.

**What "enterprise-grade" means.** The phrase is marketing until you turn it into questions a sceptic can ask. Here are ten, each with the evidence that answers it.

| Property | The sceptic's question | Evidence you can show |
|---|---|---|
| **Reliable** | Does it cope when a tool or the network misbehaves? | Timeouts, capped retries, loop limits |
| **Secure** | Can someone make it do what it should not? | Threat model, injection tests |
| **Governed** | Who approved it, and who may change it? | Risk assessment, sign-off |
| **Observable** | Can you see what it did and why? | A trace of every step |
| **Supportable** | Who gets the 3 a.m. call, and what do they do? | Runbook, on-call rota |
| **Cost-controlled** | What does a conversation cost, and what stops a runaway? | Per-request cost, budgets, caps |
| **Tested** | Did a change break anything? | Unit tests, eval set, CI gate |
| **Documented** | Could a newcomer or an auditor follow it? | Specification, decision records |
| **Accepted** | Did the customer agree it is done? | Signed acceptance criteria |
| **Improvable** | Does real use make it better? | Feedback flowing into the eval set |

Weak: "It is enterprise-grade. We use a strong model and we tested it." Strong: "Here is the eval set, the CI check that blocks a release when the score drops, last week's result, and the failure we added after the pilot." The strong answer is a set of artefacts someone else can open. Properties weigh differently per customer: a read-only copilot needs less governance than an agent that writes to a ticket system.

**Chatbot, workflow, agent.** A preview; Modules 1, 5 and 8 teach each properly. A **chatbot** makes one model call per turn, resending the conversation each time, and has no tools.

A **workflow** arranges model calls and tools along a path your code defines; it is predictable, testable and cheaper, and it solves a large share of real problems.

An **agent** lets the model direct its own process: it picks the next tool, reads the result and repeats until it decides it is done. That flexibility is also its risk, so agents need caps, traces and evals. The distinction follows Anthropic's "Building effective agents", which advises finding the simplest thing that works.

### 🟡 Going deeper

**Worked example: map Ask HR onto the lifecycle.** One line per stage: what happened, and what artefact exists.

| Stage | What happened | Artefact |
|---|---|---|
| Discover, Design | "A bot for HR questions"; no interviews; retrieval chosen on day one | None |
| Build | A notebook and a framework; it works well | The notebook |
| Evaluate | Ten questions tried by hand | Nothing kept |
| Secure to Hand over | Not discussed; demo from a laptop; no owner | None |

Build was the only stage with a finished artefact, a familiar shape for a stalled pilot. The causes recur: nobody defined success, so reviews became opinion; risk owners arrived late and vetoed it; nothing measured quality, so nobody could change anything safely; nobody owned the running system or its bill. A cheap defence is a **premortem**: before you start, write "six months from now this was paused because…" for each stage, then plan against the likeliest answers.

**The layers.** Every lesson carries a tag for the layer it works on; a lesson may carry two.

| Layer | What it covers | Modules |
|---|---|---|
| **Model** | An LLM as a stateless function: tokens, context, the API, prompts | 1–2 |
| **Applications** | Structured output, tools, retrieval, workflow patterns | 3–5 |
| **Delivery** | Customer-facing work: discovery, design, scope, release, handover | 6–7, and go-live in 14–16 |
| **Agents** | The agent loop, memory, MCP, multi-agent teams | 8–11 |
| **Production** | Evaluation, security and governance, deployment, cost, operation | 12–15 |

**How the course works.** By Module 16 you will have taken Najm Desk from first interview to go-live, with a brief, a specification, an eval gate, a governance pack, a runbook and a handover. It suits a reading group of juniors and a mentor, one module a week; Modules 0 to 16 make seventeen weeks, and a solo reader can go faster. Each week has six parts: the **lesson**; a **read**, the matching chapter of a source (the Grokking chapter first for the mental model, then the free sources for code); a **lab** you run and extend, offline first, designed to be finished in an evening; a **checkpoint** of five questions; a **deliverable**, a `week-NN/` folder with a `NOTES.md` in your own repository; and a **group session** of demos, one failure shown live, and discussion. Roles rotate weekly: facilitator, demo lead, sceptic (reviews one deliverable against the ten properties) and scribe.

**The sources, and using them without copying.** Five main sources plus an add-on; the course links to them and never reproduces them. **Grokking AI Applications** (Andrea De Mauro, Manning) is the one paid book; its tutorials use Langflow and KNIME, so treat them as demos. **Agentic Design Patterns** (Antonio Gulli) is a free draft; the course plan counted 21 patterns. **AI Agents for Beginners** (Microsoft) offers illustrated lessons with videos and notebooks; the plan counted eighteen and noted an Arabic translation. Anthropic's **Building effective agents** is the source of the workflow-versus-agent distinction. Chip Huyen's **aie-book** is the free companion to *AI Engineering*. The add-on, the free **LangChain Academy** course, serves only the multi-agent module. Contents change, so check each page. Take notes in your own words, add a line headed "what I would challenge", cite source and chapter in `NOTES.md`, and never paste their text or code into your repository.

**Framework churn.** At the time of writing, Microsoft's lessons use Microsoft's agent framework, Gulli's code uses LangChain, CrewAI and Google ADK, and the labs here use the raw Anthropic SDK. That is deliberate: a developer who has met one pattern in three syntaxes has learned the pattern, not the library. Frameworks churn; the agent loop does not. Raw SDK first, and no group standard before the comparison box in Module 11.

**How the labs run.** Every lab runs in two modes with identical code. The **offline** mock is free and scripted, so it suits mechanics: messages, tool results, loops, errors, token growth. The **real API** bills per token and gives a real model, which you need for prompt quality, retrieval, safety and true token counts. Switch by pointing `ANTHROPIC_BASE_URL` at the mock or unsetting it. Lesson 0.2 builds the setup.

### 🔴 Expert view

**Enterprise-grade is a negotiation, not a score.** The properties pull against each other: more guardrails add latency and cost, more autonomy demands more governance, more logging collides with privacy. Ask instead "how much evidence does this feature need?" The answer depends on its **autonomy level**: suggest, draft, decide with approval, or act. Najm Desk v1 mostly suggests and drafts, so it needs less evidence than the approval-gated account-unlock request, and a fully autonomous account change is outside v1 because its bar would be far higher.

**When not to build an agent.** If the process is stable and rule-based, write ordinary code. If a workflow does the job, add no loop. If you cannot say what "correct" looks like, you cannot evaluate it, so you cannot ship it. If a wrong action is severe and irreversible, keep a human deciding.

**What Claude Code changes.** It speeds up the build stage and does little for discovery, acceptance or ownership, which need conversations with people. Code now arrives faster than you can read it, so verification becomes the bottleneck: lesson 0.3.

## 🧰 The toolkit
| Tool, practice or pattern | What it is and does | When to reach for it |
|---|---|---|
| **Delivery lifecycle** | Eight stages, each with an artefact | At kickoff, and in reviews to find the missing stage |
| **Enterprise-grade checklist** | Ten properties, each with a question and evidence | Before agreeing scope and before go-live |
| **Premortem** (Gary Klein) | Imagine the project failed and write down why | At kickoff and before each stage gate |
| **Reading-group charter** | One page: schedule, roles, rules, done | In week 0 |
| **Engagement canon** | Fixed facts of the running case | Whenever you write notes or test data |

## 🏛️ In practice at Najm Bank
Your artefacts: the **engagement canon**, reused in every lab, and a **reading-group charter**.

**Najm Bank is fictional.** It is a mid-sized Gulf bank in Qatar, the UAE and the EU that appears across the course library, for instance in [*AI Governance*, lesson 0.3 — Meet Najm Bank: an AI inventory from day one](../aigp/index.html#/0.3). Every person, system, number and policy here is invented; never quote them as facts about a real organisation. A real fact (an SDK behaviour, a law, a case) is labelled and sourced.

**The engagement.** You join **Developer Enablement** to build **Najm Desk**, an AI assistant for the IT Service Desk, from first conversation to go-live. **Hind**, Head of IT Service Desk, is the sponsor and the customer in every discovery and acceptance conversation. **Yara**, the team lead, knows how tickets are really handled. **Fahad**, Head of Developer Enablement, is your mentor. **Lujain**, a graduate engineer, is your peer and makes the mistakes you should avoid. Around you are **Layla** (AI Governance), **Noura** (Application and AI Security), **Hamad** (CISO), **Sara** (Data Protection Officer), **Maha** (SRE), **Salem** (Platform Engineering), **Dana** (data science) and **Tariq** (engineering).

**The fictional baseline.** About 1,800 tickets a week. Roughly a quarter are "how do I…?" or policy questions answerable from the policy library, about a quarter are access, password and MFA problems, and the rest are hardware, network, software, security and other. Median first response is about 3 hours 40 minutes. Fourteen agents work Sunday to Thursday, 07:00 to 17:00 Qatar time; staff write in English and Arabic.

**Systems, constraints and scope.** Systems: ticketing **TicketHub**, identity **Najm ID**, the policy library (markdown files in the lab kit), the HR directory **PeopleCore** and the device manager **DeviceDesk**. Constraints: no Confidential or Restricted data in external AI tools, staff data is personal data, changes need governance sign-off, and every write action needs a human or a policy gate. **Najm Desk v1** answers policy questions with citations, reports ticket status, drafts or creates a ticket with confirmation, raises an approval-gated account-unlock *request*, and hands over to a human with full context, starting with Service Desk staff. In Module 6 you agree numeric success targets with Hind.

**The charter.** One page in your group repository:

```text
Charter v1
Meets: <day, time, place>, one module a week from <date>. Catch-up rule: <what if you miss a week>.
Roles (rotate weekly): facilitator, demo lead, sceptic, scribe. Customer role-player from Module 6.
Deliverable: week-NN/NOTES.md in your own repository, committed before the session.
Rules: no secrets in repositories; no pasted source text; every claim cites a lab output or a source.
Done for the week: lab runs offline, checkpoint answered, deliverable committed, one question ready.
```

## 🛠️ Exercises
None of these needs the real API.

- 🟢 **Define it for a system you know.** Write one page on what "enterprise-grade" would mean for a system you have worked on, using the ten properties or your own. *Done when:* every property names an artefact or says "no evidence" (expect at least two of those), and a colleague can find each artefact from your page alone.
- 🟡 **Map a past project.** Fill in the lifecycle table for a project you shipped or watched. *Done when:* every stage has an owner and an artefact (or "none"), the weakest stage has one concrete consequence, and you have written the question that would have exposed it.
- 🔴 **Set up the reading group.** Create the group repository with the charter, a seventeen-week calendar, a role rotation and a first-session agenda, then run a 20-minute premortem on the group itself. *Done when:* every member has approved the charter in a pull request, the first session is booked, and the premortem lists three causes of failure, each with a mitigation in the charter.

## ⚠️ Mistakes and traps
- **Treating the demo as the product.** It proves only the first half. Run a premortem in week one.
- **Building before "done" is agreed.** Without acceptance criteria, opinion decides, and it moves. Agree them in Module 6.
- **Using "enterprise-grade" as a slogan.** Replace it with the ten questions and their artefacts.
- **Copying instead of reading.** Pasted text or framework code teaches nothing and may breach licences. Write notes in your own words and rebuild with the raw SDK.

## 🧾 Recap
- An agent project is eight stages, each with an artefact; a stalled pilot often has only the build artefact.
- Enterprise-grade is ten properties, each backed by evidence someone else can open.
- Choose the simplest of chatbot, workflow and agent that does the job.
- Five layers tag every lesson; Delivery and Production cover the half a demo skips.
- The course is a weekly routine; labs run offline, then unchanged on the real API. Najm Bank is fictional.

## ✍️ Check yourself

**1. A pilot with a polished demo is paused four months later. Maha could not say who is paged, Layla found no risk assessment, and nobody could safely edit the prompt. What is the best diagnosis?**

- A. The model was not capable enough for a task this complex
- B. Stages after the build were never planned or owned
- C. The team picked the wrong agent framework
- D. The demo ran for too short a time

<details><summary>Answer</summary>

**B.** Every missing item belongs to a stage after the build: operate, secure, evaluate. The model did not fail. (🟡 Worked example.)

</details>

**2. A vendor says its agent is "enterprise-grade because we use the strongest model and we test it". Which reply applies this lesson?**

- A. Accept it, since model strength drives most properties
- B. Ask which framework it uses before anything else
- C. Ask for the security report only; the rest follow from it
- D. Ask for the artefact behind each of the ten properties

<details><summary>Answer</summary>

**D.** Enterprise-grade is shown by evidence: an eval set, a runbook, a cost report. A strong model does not produce any of those artefacts. (🟢 What "enterprise-grade" means.)

</details>

**3. Najm Desk must label each new ticket with one of six categories and send it to the right queue. Which design fits best?**

- A. A workflow: classify once, then route with plain code
- B. A multi-agent team with a supervisor and three workers
- C. An autonomous agent that decides its own tools and steps
- D. A chatbot that asks the requester to pick a category

<details><summary>Answer</summary>

**A.** The path is known in advance, so a routing workflow is simpler, cheaper and easier to test. (🟢 Chatbot, workflow, agent.)

</details>

**4. A group member pastes a framework example from a free source into the lab, and it runs. What does the course ask them to do?**

- A. Keep it as it is, since the source is free and the code runs
- B. Delete the lab and read the next chapter instead
- C. Rebuild the pattern with the raw SDK and cite the source
- D. Standardise the whole group on that framework

<details><summary>Answer</summary>

**C.** Labs use the raw SDK so you understand the pattern, and notes cite sources without copying. (🟡 Sources and framework churn.)

</details>

**5. Before go-live, Hamad's team asks what stops a pasted document from instructing the agent, and Layla asks who approved the change. Which stage and properties apply?**

- A. Discover, with accepted and documented
- B. Secure, with secure and governed
- C. Ship, with cost-controlled and reliable
- D. Operate, with supportable and observable

<details><summary>Answer</summary>

**B.** Resistance to injection is security, and approval and sign-off are governance; both belong to the Secure stage. (🟢 The lifecycle and the ten properties.)

</details>

## 📚 References
- Manning, *Grokking AI Applications* (Andrea De Mauro; the one paid book): https://www.manning.com/books/grokking-ai-applications
- Antonio Gulli, *Agentic Design Patterns* (free draft; if the link has moved, search the title): https://docs.google.com/document/d/1rsaK53T3Lg5KoGwvf8ukOUvbELRtH-V0LnOIFDxBryE/
- Microsoft, *AI Agents for Beginners*: https://github.com/microsoft/ai-agents-for-beginners
- Anthropic, "Building effective agents": https://www.anthropic.com/engineering/building-effective-agents
- Chip Huyen, *aie-book* (companion to *AI Engineering*): https://github.com/chiphuyen/aie-book
- LangChain Academy (free LangGraph course): https://academy.langchain.com/
- Anthropic developer documentation (start page): https://docs.anthropic.com/
- Companion course: [*Running AI Agents in Production*, levels L0–L5](../agentic/learning-path.html#level-2-agent-engineer), for the operations half of the lifecycle.
- **Read this week.** The course plan assigns no chapters for Module 0; the weekly chapter lists start in Module 1. This week, skim the contents of each source above so you know where agents, tools, retrieval, evaluation and deployment are covered, and decide which book you will read first.

---

# 0.2 — Your lab: setup, the lab kit, the API key and a spending cap
*Level: 🟢 Beginner* · *Prerequisites: 0.1* · *Layer: Model, Delivery*

## ⚡ In 60 seconds
- Your lab has two modes and one codebase: an **offline mock** (free, scripted) and the **real API** (billed). Only `ANTHROPIC_BASE_URL` and `ANTHROPIC_API_KEY` change.
- Set up once: Python 3.11 or newer, a virtual environment, the pinned SDK (`anthropic>=1,<2`) and the lab kit.
- A key lives in `.env`, and `.env` lives in `.gitignore`. Set a spending cap before the first real call.
- Run `hello.py` at the start of every session. It names the mode before it spends a cent.
- The mock teaches mechanics, not quality. It accepts any key and model id, and it cannot judge a prompt.
- Cost is arithmetic: tokens from `resp.usage` times prices from the current price page.

## 🧭 Why it matters
On her second Tuesday, Lujain pushes her API key to the team repository inside `chat.py`. (Hypothetical, like all Najm stories.) Noura's secret scanner flags it within minutes and the key is revoked. Without a scanner it could cost far more: treat any pushed key as public, since scrapers are widely reported to harvest keys from public repositories. On Thursday she thinks she is offline, but her shell has no `ANTHROPIC_BASE_URL` and her `.env` holds the real key, so a loop test makes dozens of billed calls. The cap she set on Wednesday keeps it small. Two habits prevent both: keep keys out of code, and know your mode before you spend.

## 📐 How it works

### 🟢 The essentials

**Install.** You need Python 3.11 or newer, the course repository (with the lab kit) and a virtual environment, a private package folder that keeps the course apart from other projects.

```bash
python3 --version                  # 3.11 or newer
git clone https://github.com/Tamoura/system-design-for-vibe-coders.git
cd system-design-for-vibe-coders/aiapps/labkit
printf '.env\n.venv/\n' >> ../../.git/info/exclude   # this clone does not ignore them: keep keys out of git
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt    # includes "anthropic>=1,<2"
python -c "import anthropic; print(anthropic.__version__)"    # 1.something
```

The labs rely on the 1.x SDK's shape, so keep the pin. The shell lines assume bash or zsh; on Windows, use WSL.

**Start the mock and run the smoke script.**

```bash
python -m labkit.mock_server --port 8787 &       # the offline "API" on your machine
MOCK_PID=$!                                       # remember the process id
sleep 2                                           # let it start
export ANTHROPIC_BASE_URL=http://127.0.0.1:8787 ANTHROPIC_API_KEY=mock
python labs/m00/hello.py
kill $MOCK_PID                                    # stop it when done
```

```text
mode     : MOCK (offline)  (free and scripted: good for mechanics, useless for judging answer quality)
endpoint : http://127.0.0.1:8787   model: claude-sonnet-5-5
key      : set, 4 characters, never printed
reply    : (mock) I received: Reply with one short sentence confirming you can hear me.
stop     : end_turn   request id: req_mock_1e53b1df9d8d
tokens   : in=18 out=19
```

**The API key.** For the real API, create an account in the Claude Console, add billing, and create a key named for the course. The Console usually shows a key once, so copy it into `.env` in the folder you run scripts from; commit only a `.env.example`.

```text
# .gitignore (first lines of your own repository)
.env
.venv/
__pycache__/
```

```text
# .env (stays on your machine, never committed)
ANTHROPIC_API_KEY=paste-your-real-key-here
MODEL=claude-sonnet-5-5
```

One key per person, never in code, a notebook, a chat message or a screenshot. If one leaks, revoke it in the Console first and clean up second. Before sharing a repository, check its history: `git log -p --all | grep -n "sk-ant-" || echo clean`.

**A spending cap.** Set one before the first real call. At the time of writing, the documentation describes a monthly organisation spend limit (on the Console's Billing page) and per-workspace spend limits with alerts. Give the course its own workspace so its key and limit stay separate. Names and places change, so check the Console and the rate-limits page. The cap is a backstop, not a meter: usage figures can lag.

### 🟡 Going deeper

**What the mock is, and what it is not.** It is a local server that speaks the Messages API, so the real SDK runs unchanged.

| The mock does… | The mock does not… |
|---|---|
| Keep mechanics honest: stateless calls, `tool_use` and `tool_result` pairing, `max_tokens` truncation, over-long prompts, sampling parameters rejected on the newest models | Understand anything: answers come from rules and keywords |
| Grow estimated token counts as the history grows | Count tokens like the real tokenizer or enforce real rate limits |
| Misbehave on request through directives | Check your key or model id: any key works, a typo gives no 404 |

Where a lab needs prompt quality, retrieval quality or safety, it says **Needs the real API**. A directive is a tag in a message that makes the mock misbehave: `[mock:thinking]` adds a thinking block, `[mock:ratelimit]` returns a 429, `[mock:slow]` waits three seconds. `MOCK_CONTEXT_WINDOW=8000` makes overflow cheap.

**One codebase, two modes.** The SDK reads two environment variables, a base URL and a key (any dummy value offline), and nothing else changes.

```mermaid
flowchart LR
    L["Your lab code<br/>identical in both modes"] --> K["anthropic SDK<br/>reads two variables"]
    K --> Q{"ANTHROPIC_BASE_URL<br/>set?"}
    Q -->|"yes, 127.0.0.1"| M["Lab kit mock<br/>free and scripted"]
    Q -->|"no"| R["Anthropic API<br/>billed per token"]
```

To go real, stop the mock and run `unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY`, so the key comes from `.env`. The unset matters: `load_dotenv` never overrides an exported variable, which is a feature until you forget you exported `mock`. The smoke script reports the mode so you need not remember.

```python
# labs/m00/hello.py
"""Smoke test: which mode are you in, and does one real SDK call work?
Offline: start the mock, then  export ANTHROPIC_BASE_URL=http://127.0.0.1:8787 ANTHROPIC_API_KEY=mock
Real: unset ANTHROPIC_BASE_URL and keep your key in .env. The code is the same; only the environment differs.
Exit codes: 0 worked, 1 the API call failed, 2 configuration problem."""
import os
import sys
from urllib.parse import urlparse

import anthropic
from anthropic import Anthropic
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))          # reads .env from where you run; exported variables win over the file
MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")   # never hard-code a model id in lab code


def detect_mode(base_url, api_key):
    """Return (mode, hint). A pure function, so a test can call it with no network."""
    if not api_key:
        return "NO KEY", "set ANTHROPIC_API_KEY (offline: mock; real: your key in .env)"
    host = urlparse(base_url).hostname if base_url else None
    if host in ("127.0.0.1", "localhost", "::1"):
        return "MOCK (offline)", "free and scripted: good for mechanics, useless for judging answer quality"
    if host in (None, "api.anthropic.com"):
        if api_key == "mock":
            return "MISCONFIGURED", "the dummy key would get a 401 from the real API: set ANTHROPIC_BASE_URL or a real key"
        return "REAL API (billable)", "every call costs money: is your spending cap set?"
    return "CUSTOM ENDPOINT", f"the gateway at {host} sees your key and prompts: trust whoever runs it"


def main() -> int:
    base_url, key = os.environ.get("ANTHROPIC_BASE_URL"), os.environ.get("ANTHROPIC_API_KEY")
    mode, hint = detect_mode(base_url, key)
    print(f"mode     : {mode}  ({hint})")
    print(f"endpoint : {base_url or 'https://api.anthropic.com (SDK default)'}   model: {MODEL}")
    print(f"key      : {f'set, {len(key)} characters, never printed' if key else 'NOT SET'}")
    if mode in ("NO KEY", "MISCONFIGURED"):
        return 2
    try:
        resp = Anthropic(max_retries=0).messages.create(      # max_retries=0: fail fast while you set up
            model=MODEL,
            max_tokens=1024,                                  # required; thinking tokens count as output
            messages=[{"role": "user", "content": "Reply with one short sentence confirming you can hear me."}],
        )
    except anthropic.APIConnectionError:                      # no HTTP response at all
        print("FAILED   : cannot connect. Is the mock running on that port? Behind a proxy? See the table.")
        return 1
    except anthropic.APIStatusError as e:                     # an HTTP error: 400, 401, 404, 429, 5xx ...
        print(f"FAILED   : {type(e).__name__} (HTTP {e.status_code}): {e.message}")
        return 1
    text = next((b.text for b in resp.content if b.type == "text"), "")      # never resp.content[0].text
    u = resp.usage
    print(f"reply    : {text}")
    print(f"stop     : {resp.stop_reason}   request id: {resp._request_id}")
    print(f"tokens   : in={u.input_tokens} out={u.output_tokens}")
    p_in, p_out = os.environ.get("PRICE_IN_PER_MTOK"), os.environ.get("PRICE_OUT_PER_MTOK")
    if p_in and p_out:
        print(f"cost     : {(u.input_tokens * float(p_in) + u.output_tokens * float(p_out)) / 1_000_000:.6f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

`MODEL` comes from the environment. `max_tokens` is required, and 1024 is a sensible floor on current models because thinking tokens count as output. The reply is the text block chosen by type, never `resp.content[0].text`. Log `resp.usage` and `resp._request_id` on every call. `stop` is `resp.stop_reason`; a production loop must handle every value (Module 1). The two `except` clauses show the SDK's split: no response at all, or an HTTP error with a status.

**From usage to money.** A call costs `(input tokens × input price + output tokens × output price) ÷ 1,000,000`. Prices change, so copy them from the current price page into two environment variables, never into code. `output_tokens` includes thinking tokens, and some newer model generations count the same text as about 30% more tokens (per the model reference), so re-measure after a model change. Usage also reports cache tokens, priced differently (Module 14). To count before sending, use `client.messages.count_tokens`, never `tiktoken`. Input grows fast, because every call resends the whole history.

```python
# labs/m00/cost.py
"""Turn token counts into money and project a pilot's bill. No price is hard-coded: copy the current prices
from the price page into PRICE_IN_PER_MTOK and PRICE_OUT_PER_MTOK (per million tokens), then for example:
  python labs/m00/cost.py --system 1500 --user 60 --answer 250 --turns 6 --conversations 450 --weeks 4"""
import argparse
import os


def call_cost(tokens_in: int, tokens_out: int, price_in: float, price_out: float) -> float:
    """One API call: tokens x price per million tokens."""
    return (tokens_in * price_in + tokens_out * price_out) / 1_000_000


def conversation_tokens(system: int, user: int, answer: int, turns: int) -> tuple[int, int]:
    """Total (input, output) tokens for one chat. Every call resends the system prompt and the whole history:
    call t sends  system + t user messages + (t-1) answers  and receives one answer."""
    return sum(system + t * user + (t - 1) * answer for t in range(1, turns + 1)), turns * answer


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for name, default in [("system", 1500), ("user", 60), ("answer", 250), ("turns", 6), ("conversations", 450), ("weeks", 4)]:
        ap.add_argument(f"--{name}", type=int, default=default)
    a = ap.parse_args()
    t_in, t_out = conversation_tokens(a.system, a.user, a.answer, a.turns)
    n = a.conversations * a.weeks
    print(f"one conversation: in={t_in} out={t_out} tokens;  pilot: {t_in * n:,} in, {t_out * n:,} out over {n:,} conversations")
    p_in, p_out = os.environ.get("PRICE_IN_PER_MTOK"), os.environ.get("PRICE_OUT_PER_MTOK")
    if p_in and p_out:
        one = call_cost(t_in, t_out, float(p_in), float(p_out))
        print(f"cost: {one:.5f} per conversation, {one * n:,.2f} for the pilot; budget at x2: {2 * one * n:,.2f}")
    else:
        print("set PRICE_IN_PER_MTOK and PRICE_OUT_PER_MTOK from the current price page to see money")
```

With invented prices of 1 and 5 units per million tokens, used only to show the arithmetic, `python labs/m00/cost.py --turns 12` prints:

```text
one conversation: in=39180 out=3000 tokens;  pilot: 70,524,000 in, 5,400,000 out over 1,800 conversations
cost: 0.05418 per conversation, 97.52 for the pilot; budget at x2: 195.05
```

Doubling the turns from six to twelve nearly tripled the input tokens (14,010 to 39,180). The "x2" is a rule of thumb; replace it with your measured ratio.

**Run the lab-kit tests.** From `aiapps/labkit`, run `pytest`. They check the mock against the real SDK, and this lesson's scripts; rerun them after any SDK upgrade. They say nothing about your prompts.

**Troubleshooting.** Real error texts differ from the mock's approximations, so read yours.

| Symptom | Likely cause | What to do |
|---|---|---|
| 401 `AuthenticationError`, or "Could not resolve authentication method" | Key missing, wrong or revoked; `mock` sent to the real API; `ANTHROPIC_AUTH_TOKEN` also set | Run `hello.py`; check `.env` is found from where you run; make a new key |
| 404 `NotFoundError` "model: …" | Typo (dots for dashes), a retired model, or one your organisation cannot use | Copy the id from the models page; the mock never rejects a model id |
| 400 `BadRequestError`, such as "prompt is too long" | History past the context window, an invalid parameter, a missing `tool_result` | Read `e.message`; trim old turns (Module 1) |
| 429 `RateLimitError`, or 500 and 529 | Rate limit; or provider-side trouble | The SDK retries twice; slow down, check `retry-after`, retry with backoff |
| "Connection refused" (`APIConnectionError`) | Mock not running, wrong port, a firewall | Start the mock; use `127.0.0.1` and the same port |
| Works at home, fails at the bank | A corporate proxy or TLS inspection | Set `HTTPS_PROXY`; add `127.0.0.1` to `NO_PROXY`; ask IT for the certificate bundle; or pass `DefaultHttpxClient(proxy=...)` to the client |

### 🔴 Expert view

**A key is a credential; a base URL is a trust decision.** Pair a real key with a non-local `ANTHROPIC_BASE_URL` and that server receives your key and every prompt. Enterprise gateways are legitimate, but treat one like any third party; that is why `hello.py` flags a custom endpoint. Custody also grows: `.env` suits a laptop, and later modules move keys into a secret manager, one per environment. The cap bounds any leak.

## 🧰 The toolkit
| Tool, practice or pattern | What it is and does | When to reach for it |
|---|---|---|
| **Pinned SDK** | `anthropic>=1,<2` fixes the major version | Always; upgrade on purpose |
| **.env file** | A local, git-ignored file of secrets | Keys and per-machine settings |
| **Lab kit mock** | An offline server speaking the Messages API | Mechanics, tests and CI, at no cost |
| **Smoke script** | `hello.py` names the mode and makes one call | The first command of every session |
| **Spending cap** | A provider-side limit on what an organisation or workspace can spend | Before the first real call |
| **Cost estimate** | Tokens × price, projected over a pilot | Before a pilot, then with measured numbers |

## 🏛️ In practice at Najm Bank
**Deliverable, part 1 of week 0: your lab repository.** Create a private repository next to the cloned course repository. Claude Code builds the skeleton below; you read every file it writes.

```text
najm-desk-lab/                  your own private repository
├── .gitignore  .env.example    names only; .env itself is ignored
├── requirements.txt  Makefile  scripts/use-mock.sh  scripts/use-real.sh
├── CLAUDE.md                   written in lesson 0.3
└── week-00/NOTES.md  hello-mock.txt  hello-real.txt   (one week-NN folder per module)
```

`week-00/NOTES.md` has five headings: **Spending cap**, **Key storage**, **Mode checks** (pasted output), **Cost estimate** (assumptions and a range) and **Surprises**.

**Group session, part 1: setup clinic (30 minutes).** Everyone shows the mode line of an offline run. One person stops the mock and shows the failure. Pairs search each other's history for `sk-ant-`. Everyone says where their cap is set.

**Build it with Claude Code.** Give it this spec, and approve its plan before it edits anything.

```text
GOAL
Create my lab repository "najm-desk-lab" next to the cloned course repo, with scripts to switch between the offline mock and the real API.

CONTEXT (read first)
../system-design-for-vibe-coders/aiapps/labkit/README.md, requirements.txt and labs/m00/hello.py. Do not modify anything in that repo.

BUILD
1. .gitignore (.env, .venv/, __pycache__/, .mock.pid) and .env.example (ANTHROPIC_API_KEY empty, MODEL=claude-sonnet-5-5, PRICE_IN_PER_MTOK and PRICE_OUT_PER_MTOK empty)
2. requirements.txt: anthropic>=1,<2 plus what labkit/requirements.txt lists
3. scripts/use-mock.sh and scripts/use-real.sh, meant to be sourced. use-mock exports ANTHROPIC_BASE_URL=http://127.0.0.1:8787 and ANTHROPIC_API_KEY=mock. use-real unsets both.
4. Makefile targets: setup, mock (start the mock, write its PID to .mock.pid, wait until the port answers), stop (kill only that PID), hello, test (the lab kit tests)
5. week-00/NOTES.md with the five headings from the lesson

CONSTRAINTS
Never read, print or write a real key. Do not call the real API. Python 3.11+. Scripts under 30 lines, commented. Never kill processes by name or pattern.

ACCEPTANCE CHECKS
- make setup && make mock && source scripts/use-mock.sh && make hello prints "mode     : MOCK (offline)" and exits 0
- make stop leaves nothing listening on port 8787
- make test passes
- a throwaway .env holding a fake key does not appear in git status

DO NOT
Add CI, Docker or extra features. Do not commit. Plan first and wait for my OK.
```

**Verify before you accept it.**
- Run all four acceptance checks yourself; "it should work" is no result.
- Read the Makefile for kill-by-name and for edits to the course repository.
- Read both scripts: does `use-real.sh` unset both variables, and does anything echo a key?

## 🛠️ Exercises
- 🟢 **The smoke script, offline.** Run `hello.py` with the mock running, with it stopped, and with the key unset. *Done when:* three outputs are saved in `week-00/` with their exit codes (0, 1, 2 from `echo $?`) and you can explain every line of the first. No real API needed.
- 🟡 **The same script, real API.** Put your key in `.env`, set the price variables, unset the mock variables and run it. *Done when:* the mode says `REAL API (billable)`, the token counts differ from the mock's, the request id is saved, the cost line matches your arithmetic, and a history search for `sk-ant-` finds nothing. **Needs the real API.**
- 🔴 **Record the cap and the estimate.** Run `cost.py` for the whole course under a low, an expected and a high scenario. *Done when:* `NOTES.md` states the cap (where, amount, who can change it), three scenario costs with assumptions, an alert threshold below the cap, and your response when usage reaches it. Needs Console access, not API calls.

## ⚠️ Mistakes and traps
- **A key in code, a notebook or a screenshot.** Use `.env`, ignore it, scan history, revoke at once if it leaks.
- **Not knowing your mode.** A forgotten variable turns "offline" into billed calls. Run `hello.py` first, every session.
- **Trusting the mock for quality.** It cannot tell a good prompt from a bad one. Use the real API for that.
- **Hard-coding the model id or prices.** Both change. Read them from the environment.

## 🧾 Recap
- One codebase, two modes: the mock is free and scripted, the real API is billed; two environment variables switch them.
- Pin `anthropic>=1,<2`, keep keys in an ignored `.env`, and set a spending cap before the first real call.
- The mock accepts any key and model id, and never judges quality.
- Cost is tokens times price, and input grows each turn because the history is resent.

## ✍️ Check yourself

**1. You think you are testing offline, but `.env` holds your real key and `ANTHROPIC_BASE_URL` is unset. What tells you before a billed surprise?**

- A. The SDK warns you before any billed call
- B. The mock intercepts anything that looks like a test
- C. The provider refuses calls from lab code
- D. Running `hello.py` first, since it prints the mode

<details><summary>Answer</summary>

**D.** `hello.py` reports `REAL API (billable)` before spending anything. Neither the SDK nor the provider warns. (🟡 One codebase, two modes.)

</details>

**2. Offline, every lab passes. The first real run fails with a not-found error naming the model. Most likely cause?**

- A. Your spending cap has been reached
- B. The mock accepted a mistyped model id that the real API rejects
- C. The SDK version is too new for the model
- D. The real API is rate limiting you

<details><summary>Answer</summary>

**B.** The mock does not check model ids, so a typo only fails against the real API. (🟡 What the mock is not.)

</details>

**3. A six-turn chat costs X in input tokens. Why does a twelve-turn chat cost well over 2X?**

- A. Every call resends the system prompt and the full history
- B. Later turns switch to a pricier model automatically
- C. The SDK retries more often in long chats
- D. Output tokens are billed at the input rate

<details><summary>Answer</summary>

**A.** Input grows every turn, so the total outpaces the turn count: `cost.py` shows 14,010 against 39,180 tokens. (🟡 From usage to money.)

</details>

**4. Your API key was pushed to the team repository an hour ago. What is the right first move?**

- A. Delete the file in a new commit and say nothing
- B. Rewrite the history before telling anyone
- C. Revoke the key in the Console, then clean up
- D. Wait a day to see whether anyone uses it

<details><summary>Answer</summary>

**C.** Assume it is compromised: only revoking stops misuse. Deleting the file or rewriting history does not undo exposure. (🟢 The API key.)

</details>

**5. Which problem can you only see against the real API, never against the offline mock?**

- A. A `tool_use` without its `tool_result` being rejected
- B. A reply cut off by a small `max_tokens`
- C. A rejected key returning a 401
- D. Input tokens growing as history is resent

<details><summary>Answer</summary>

**C.** The mock accepts any key; the other three are mechanics it reproduces. (🟡 What the mock is not.)

</details>

## 📚 References
- Anthropic SDK for Python: https://github.com/anthropics/anthropic-sdk-python
- Anthropic developer documentation (start page): https://docs.anthropic.com/
- Models overview: https://platform.claude.com/docs/en/about-claude/models/overview
- Pricing: https://platform.claude.com/docs/en/about-claude/pricing
- Rate limits and spend limits: https://platform.claude.com/docs/en/api/rate-limits
- Errors: https://platform.claude.com/docs/en/api/errors
- Token counting: https://platform.claude.com/docs/en/build-with-claude/token-counting
- Python virtual environments: https://docs.python.org/3/library/venv.html
- The course lab kit: https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/aiapps/labkit

---

# 0.3 — Your build partner: directing Claude Code to build agents (and what you must still understand)
*Level: 🟢 Beginner* · *Prerequisites: 0.1, 0.2* · *Layer: Delivery*

## ⚡ In 60 seconds
- Claude Code is your build partner, not your replacement, and not the `anthropic` SDK your agent's code calls. You are the architect and reviewer; the method is **spec, plan, small steps, verify, review the diff, commit**.
- It is fast, fluent and confident even when wrong: it can invent SDK parameters, weaken tests to get green, and build far more than you asked.
- A `CLAUDE.md` file holds your commands, conventions and safety rules; hooks and permissions enforce what instructions only request.
- Review agent-written agent code with a ten-point checklist; trust results up a pyramid, from offline checks to real-model evals.
- Decision cue: if you cannot say how you would know the result is right, do not delegate it yet.
- Biggest trap: green tests you have not read.

## 🧭 Why it matters
Lujain asks Claude Code for a Najm Desk chat script. Forty seconds later she has sixty tidy lines and passing tests. In review, Fahad asks: what happens when the reply starts with a thinking block? Where does the history grow, and where does it stop? What have you checked besides "it ran"? Lujain cannot answer: she has not read the code. (Hypothetical.)

Delegating the typing does not delegate the responsibility. As reported in July 2025, an AI coding assistant deleted a production database during a declared code freeze and then misdescribed what it had done. Details vary by account, but an agent acts on the instructions and permissions you give it.

## 📐 How it works

### 🟢 The essentials

**The method.** Six steps, and the loop matters more than any one of them.

```mermaid
flowchart LR
    S["Spec<br/>goal, limits, checks"] --> P["Plan<br/>you approve it"]
    P --> I["Implement<br/>one small step"]
    I --> V["Verify<br/>tests and evals"]
    V --> R["Review the diff<br/>checklist"]
    R --> C["Commit"]
    C --> I
    V -.->|"red"| P
    R -.->|"rejected"| S
```

1. **Spec.** Write the goal, the limits and the checks that prove it before any code. If you cannot write the checks, learn more first.
2. **Plan.** Ask for a plan and read it. A wrong plan is cheap to fix; a wrong implementation is not.
3. **Implement in small steps.** One behaviour at a time, so each diff is readable.
4. **Verify.** Run the tests and, when quality matters, the eval. Evidence beats the agent's summary.
5. **Review the diff** as you would a colleague's pull request, with the checklist below.
6. **Commit** once per step, with a message that says why.

**What it is good at, and where it fails.** It is strong at boilerplate, test scaffolding, mechanical refactors and explaining unfamiliar code. It is weak at knowing what the customer needs, at current SDK details (its knowledge lags the package), at keeping tests honest (it may loosen an assertion to get green), at restraint (extra retries, abstractions and features) and at saying "I am not sure".

Weak: "Write a chatbot for the service desk using Claude." Expect a framework, a web page and guessed parameters. Strong: "Add `ask(text)` to `chat.py`. Keep the history. Set `max_tokens` to 1024 and choose the text block by type. Add a test using `[mock:thinking]`. Use only the mock. Plan first." It names behaviour, limits and check, so the diff stays small.

### 🟡 Going deeper

**CLAUDE.md: project memory.** Claude Code reads this file at the start of a session (check the current documentation for how and where). Keep it short and specific (the documentation suggests staying under about 200 lines): commands, conventions and rules beat prose. This is a complete template for an agent project.

```markdown
# CLAUDE.md — Najm Desk agent project

### Purpose
Najm Desk is an AI assistant for the IT Service Desk of Najm Bank (a fictional engagement). Every write action needs a human or a policy gate. Keep code small and commented.

### Commands
- Setup: make setup
- Mock server (offline, free): make mock; make stop when done
- Smoke test: source scripts/use-mock.sh && make hello
- Tests (offline): make test for the lab kit, pytest -q for this repository
- Evals (from Module 12): python evals/run_eval.py --mode mock. Real-API evals cost money: only when I say "real API OK" and week-00/NOTES.md records a spending cap

### Conventions
- Python 3.11+, type hints, small functions, comments that explain why.
- The model id comes from the MODEL environment variable (default claude-sonnet-5-5). Never hard-code another.
- Every messages.create call: max_tokens of 1024 or more, the text block chosen by type (never content[0].text), stop_reason handled, no temperature, top_p or top_k.
- Every agent loop has an iteration cap; every tool_use gets a tool_result, all in one user message.
- Prompts live in prompts/ as versioned files; changing one needs an eval run.
- Fictional data only.

### Safety rules
- Never write, print or commit a key. Never read .env.
- Use the mock by default. Ask before any step that calls the real API.
- Never weaken, skip or delete a test to make it pass. If a test looks wrong, stop and explain.
- No eval() or exec() on model output. Ask before adding dependencies or running destructive commands (rm -rf, force push).

### Working style
- Plan first when more than one file is involved, and wait for my approval. Small steps; tests after each.
- Unsure of an SDK parameter? Read the installed package. Never guess.

### Platform facts
(Paste the "Your platform" answers here.)

### Definition of done
Tests pass offline; new behaviour has a test that fails without the change; evals not worse, or explained; no secrets; I have read the diff.
```

**The controls around it.** Instructions in `CLAUDE.md` are requests the model usually follows; these features are enforced by the program. Names and defaults change; check the current documentation.

| Control | What it does | How to use it on this course |
|---|---|---|
| **Plan mode** | Explores and proposes a plan without editing until you approve | Any change that touches more than one file |
| **Permissions** | Asks before commands and edits; an allow-list lets safe routine commands run | Allow tests, the mock and `git diff`; deny reading `.env` and force pushes. A rule is no sandbox: keep real keys out of reach |
| **Hooks** | Commands run automatically on events, such as after an edit | Run `pytest -q` or the eval after edits; block edits to `.env` |
| **Subagents** | Separate assistants with their own context and tool limits | A read-only reviewer fed the diff and the checklist |
| **MCP servers** | Add outside tools or data | Read-only sandbox access first; each is code you run and text the model reads, so vet it |
| **Headless mode** | A non-interactive run for scripts and CI | Advisory review comments; never auto-merge |

**A build-spec template.** Fill it in for every change; each field removes a way to guess.

```text
GOAL: <one sentence: the behaviour someone will see>
WHY: <the customer need>
READ FIRST: <CLAUDE.md and the files to change>

REQUIREMENTS
1. <a behaviour, as Given / When / Then or a short rule>

CONSTRAINTS
- <libraries, SDK rules, files you may touch>. Use the mock; no real API calls.

ACCEPTANCE CHECKS (I will run these)
- <command> -> <expected result>
- A new test that fails without your change and passes with it

DO NOT
- <out-of-scope features, refactors, renames, dependencies>

PROCESS: plan first and wait for my OK; small steps; tests after each; summarise the diff and your doubts.
```

### 🔴 Expert view

**A reviewer's checklist for agent-written agent code.** Ten things to look for.

| Look for | Why it bites | How to catch it |
|---|---|---|
| **Stale or invented parameters** (`temperature`, `budget_tokens`, prefill, forced `tool_choice`) | A `TypeError` for sampling arguments in the 1.x SDK; a 400 from current models for the rest | Run it; read the SDK signature and the models page |
| **`content[0].text`** | Breaks when a thinking block comes first | A `[mock:thinking]` test; choose the block by type |
| **No `max_tokens`, or no loop cap** | A `TypeError`, or a runaway loop and bill | Read every `create` and every `while` |
| **A missing `tool_result`** | A 400, or a model that loses the thread | One result per `tool_use` id, in one message |
| **No `stop_reason` handling** | A truncated or refused turn passes as an answer | Test with a tiny `max_tokens` |
| **Secrets in code** | Leaks; ignores your environment | Secret scan; search for `sk-ant-` |
| **`eval()` on model output** | Model text becomes your code | Parse and validate instead |
| **Unbounded retries** | A loop around the SDK's own retries multiplies calls | Cap attempts, back off, never retry a 400 |
| **Memory mistakes** | A reply never added to the history means amnesia; a history never trimmed means cost, then overflow | Ask a follow-up; test with `MOCK_CONTEXT_WINDOW` |
| **No tests, or tests of the mock** | Green means nothing | Break the code; the test must fail |

**The verification pyramid.** Climb from the cheap base; do not stop low when a higher rung matters.

1. **Static checks** (linter, types, secret scan): seconds, free, on every save.
2. **Offline unit tests against the mock**: mechanics, on every commit.
3. **Contract tests**: tool schemas and structured output validate.
4. **Evals on a real model**: quality on a golden set, which costs money (Module 12).
5. **Human review** of the diff and the traces: always.
6. **Production signals**: a pilot, then monitoring (Module 15).

For depth, see [*System Design for Vibe Coders*, lesson 9.4 — Verification before completion](../vibe/index.en.html#l9-4), [*Software Testing*, lesson 6.1 — Verifying AI-generated code: how coding agents fail and a reviewer's checklist](../testing/index.html#/6.1) and [*Software Testing*, lesson 6.2 — Tests as the specification for coding agents: test-first workflows, guardrails and mutation as the judge](../testing/index.html#/6.2).

**What you cannot delegate.** When Hind, Yara, Hamad or Layla asks, you answer without Claude Code in the room. What does it do when it is wrong? What can it change, and who approves? Where does staff data go? How do we know it works? What does a conversation cost? How do we turn it off? If you cannot explain a line to Yara, it does not ship. For directing a whole AI team, see [*System Design for Vibe Coders*, lesson 9.1 — You are the architect now](../vibe/index.en.html#l9-1).

**When not to delegate.** Write your first loop by hand (Modules 1 and 8). Keep security-critical choices and real customer data with a human. Never delegate a task whose check you cannot state.

> **Your platform.** You will probably deploy on an internal platform, yours, your employer's or your customer's. This course has no details of it and describes none. Fill this table in with its owners, then paste the answers into your `CLAUDE.md` so Claude Code stops guessing.

| Question | What to find out | Your answer |
|---|---|---|
| **Identity** | How do users and services sign in? Can the agent act as the user or only as a service account? What is the smallest scope per tool? | |
| **Secrets** | Where are keys stored and rotated, and how does the agent receive them at run time? | |
| **Deploy target** | Where do containers or functions run, who may deploy, and how are environments kept apart? | |
| **Observability** | Where do logs, traces and metrics go, for how long, and may they hold prompts and answers? | |
| **Ticketing** | Where do tasks, incidents and change requests live, and is there an API? | |
| **Approval workflow** | Who signs off a new tool, prompt or model change, with what evidence? | |
| **Data residency** | Where may prompts, logs and embeddings be processed and stored? Is your model provider approved for this data class? | |

## 🧰 The toolkit
| Tool, practice or pattern | What it is and does | When to reach for it |
|---|---|---|
| **CLAUDE.md** | Project memory: purpose, commands, conventions, rules, done | At the start of every repository |
| **Build spec** | Goal, limits, acceptance checks and out-of-scope list for one change | Before every request to Claude Code |
| **Hooks** | Commands the program runs on events | Rules that must hold every time, such as tests after edits |
| **Agent code review checklist** | Ten things to check in agent-written agent code | Every diff, human or AI |
| **Verification pyramid** | Static, offline, contract, eval, human, production checks | To decide how much evidence a change needs |

## 🏛️ In practice at Najm Bank
Fahad's rule: nothing an agent writes is merged unread. Your artefacts are a `CLAUDE.md`, the checklist as a pull-request template, and a first review. Lujain's agent wrote this `chat.py`. It runs, it looks fine, and it has five planted flaws. Read it as the reviewer.

```python
# labs/m00/flawed_chat.py
"""chat.py for Najm Desk, as an AI coding agent wrote it. It looks tidy and confident. It has FIVE flaws.
Exercise 0.3: find them by reading, then prove each with labkit/tests/test_m00_flawed_chat.py.
Do not fix this file. Copy it into your own repo and fix the copy."""
import os

from anthropic import Anthropic

# Simple and reliable: the client is ready to use as soon as the module loads.
client = Anthropic(api_key="sk-ant-EXERCISE-NOT-A-REAL-KEY-0000")

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
SYSTEM = "You are Najm Desk, an assistant for the Najm Bank IT Service Desk. Answer briefly. If unsure, say so."

history = []                                     # the conversation so far


def ask(user_text: str) -> str:
    """Send one user message and return the model's reply."""
    history.append({"role": "user", "content": user_text})
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        messages=history,
    )
    reply = resp.content[0].text                 # the reply is the first block
    print(f"[tokens in={resp.usage.input_tokens} out={resp.usage.output_tokens}]")
    return reply


def brainstorm(topic: str) -> str:
    """Looser, more varied wording for the /ideas command."""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        temperature=1.0,                         # more variety for brainstorming
        messages=[{"role": "user", "content": f"Give me three ideas for: {topic}"}],
    )
    return next(b.text for b in resp.content if b.type == "text")


def summarise_history() -> str:
    """Squeeze a long conversation into three bullet points for the /summary command."""
    resp = client.messages.create(
        model=MODEL,
        system="Summarise this conversation in three bullet points.",
        messages=history,
    )
    return next(b.text for b in resp.content if b.type == "text")


if __name__ == "__main__":
    while True:
        line = input("you> ").strip()
        if line in ("exit", "quit"):
            break
        if line.startswith("/ideas "):
            print("bot>", brainstorm(line[7:]))
        elif line == "/summary":
            print("bot>", summarise_history())
        else:
            print("bot>", ask(line))
```

The tests in `labkit/tests/test_m00_flawed_chat.py` prove each flaw against the 1.x SDK or the mock; to see the amnesia, start the mock with `--playbook playbooks/m00_flawed_chat.json` and ask "How do I request a laptop?", then "And how long does it take?". Do not fix the lab file: copy it into your repository and fix the copy.

**What the mock can and cannot show here.** The `TypeError`s come from the real 1.x SDK; the thinking block and the amnesia from the mock's scripted replies. It cannot show flaw 1's real effect (a 401; **Needs the real API**) or whether a real model answers well.

**Week 0 deliverable, complete.** In `week-00/`: the lesson 0.2 `NOTES.md` and outputs; a `review.md` with the five flaws; the 🔴 exercise's spec and diff review; the platform table; and, at the repository root, your `CLAUDE.md`.

**Group session (60 to 90 minutes).** The demo lead shows `hello.py` in both modes (10 minutes). Each member names the flaw found fastest; run the tests together (20). Swap `CLAUDE.md` files and adopt the best three rules (15). Review one volunteer's diff live (20). List the platform-table gaps (10).

## 🛠️ Exercises
- 🟢 **Find the five flaws.** Read `flawed_chat.py` as a reviewer before running anything, then run its tests. *Done when:* `review.md` lists five flaws, each with line, symptom, checklist item and fix; the tests pass, proving each; and your fixed copy has a test that would have caught one. No real API.
- 🟡 **Write `CLAUDE.md` for the course repository.** Adapt the template to your repository and platform answers. *Done when:* it is under 60 lines, every command runs, and a fresh Claude Code session follows three rules unprompted (no sampling parameters, mock by default, ask before the real API). Needs Claude Code, not the lab API key.
- 🔴 **Spec, diff, review.** Use the template to have Claude Code add a `/cost` command to your fixed chat, printing the running token total and, if the price variables are set, the cost. Review the diff against all ten items. *Done when:* the spec has acceptance checks, each item has pass or fail with a line number, you requested at least one change, a test fails without the feature, and the commit message says why. Needs Claude Code; the mock suffices.

## ⚠️ Mistakes and traps
- **Accepting green tests you have not read.** They may test the mock, or nothing. Break the code on purpose and watch the test fail.
- **A vague request.** "Build a chatbot" buys an over-built app with guessed parameters. Use the template.
- **A `CLAUDE.md` of wishes.** Long prose gets ignored. Keep rules short; put must-hold rules in hooks.
- **Broad permissions.** Unattended real-API access, production credentials or destructive commands cause stories like the deleted database. Allow-list narrowly.

## 🧾 Recap
- The method is spec, plan, small steps, verify, review the diff, commit.
- Claude Code invents parameters, weakens tests and over-builds, so you review everything.
- `CLAUDE.md` states the rules; hooks and permissions enforce them. Check the current documentation.
- Offline tests prove mechanics, evals prove quality; use the checklist and the pyramid.
- You must explain every line to the customer; the platform table holds facts Claude Code cannot guess.

## ✍️ Check yourself

**1. Claude Code returns an `ask()` that reads `resp.content[0].text`, and its mock tests pass. What should you do?**

- A. Accept it, since green tests mean the code is correct and safe
- B. Wrap the attribute access in a try block
- C. Pick the text block by type; add a `[mock:thinking]` test
- D. Switch to a model that never emits thinking blocks

<details><summary>Answer</summary>

**C.** No test sent a reply starting with a thinking block, so green proved little; a try block would hide the bug. (🔴 Checklist.)

</details>

**2. To make a failing test pass, the agent changes `assert status == "Closed"` to `assert status`. What do you do?**

- A. Reject it, find why it failed, then fix the code or spec
- B. Accept it, since the suite is now green and CI will pass
- C. Accept it if the commit message explains the loosened assertion
- D. Ask the agent to loosen the other tests the same way

<details><summary>Answer</summary>

**A.** A loosened assertion hides a real failure. (🟢 Where it fails.)

</details>

**3. Your `CLAUDE.md` says "run the tests after every edit", yet the agent sometimes skips them. What is the most reliable fix?**

- A. Rewrite the rule in capital letters at the top
- B. Repeat the same rule at the end of the file too
- C. Switch to a larger model for every session
- D. Add a hook that runs the tests after each edit

<details><summary>Answer</summary>

**D.** Instructions are requests; a hook is run by the program every time. Check the docs for how to configure one. (🟡 The controls.)

</details>

**4. A reviewer finds `while True:` around a model call and tool runs, with no counter, and one tool often errors. Which finding matters most?**

- A. Invented parameters: remove the extra arguments now
- B. A missing loop cap: add a hard iteration limit
- C. A memory mistake: trim the history
- D. No tests: write a unit test first

<details><summary>Answer</summary>

**B.** A failing tool can keep the loop spinning and billing; a hard cap comes first. (🔴 Checklist.)

</details>

**5. Hind asks how you know Najm Desk answers policy questions correctly. You say Claude Code wrote tests and they pass. What is missing?**

- A. Nothing, since passing tests prove the answers are correct
- B. A longer `CLAUDE.md` with many more rules in it
- C. A real-model eval on a golden set that you can explain
- D. A second Claude Code review of the same passing tests

<details><summary>Answer</summary>

**C.** Offline tests prove mechanics, not answer quality. Quality needs an eval on a real model that you can explain. (🔴 The pyramid.)

</details>

## 📚 References
- Claude Code overview: https://code.claude.com/docs/en/overview
- Claude Code memory (CLAUDE.md): https://code.claude.com/docs/en/memory
- Claude Code hooks: https://code.claude.com/docs/en/hooks
- Claude Code repository: https://github.com/anthropics/claude-code
- [*System Design for Vibe Coders*, lesson 9.5 — Claude Code power techniques](../vibe/index.en.html#l9-5)
