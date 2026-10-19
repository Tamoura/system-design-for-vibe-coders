# Building AI Applications & Agents: Zero to Hero — authoring guide

This is the contract every lesson follows. It is not published.

## What the course is

A free, bilingual (English/Arabic) course that takes a reader **from zero to hero in creating and shipping enterprise-grade AI agents**: from "what is a token" to "an agent running in production for a customer, with requirements, evals, guardrails, a runbook and a handover". It started as a reading-group course for junior developers (one module per week, labs you finish in an evening) and now covers the whole delivery lifecycle: **Discover → Design → Build → Evaluate → Secure → Ship → Operate → Hand over.**

Three promises to the learner:
1. **Concepts, then application.** Every idea is explained in plain language with a diagram before any code; then applied in a lab on one running customer scenario.
2. **Customer-ready, not demo-ready.** The course teaches how to **collect requirements, design with a customer, agree scope, deploy, ship and hand over**, not only how to call an API. Modules 6, 7, 14, 15 and 16 are the delivery half.
3. **Build with Claude Code, understand what it builds.** The learner is an AI-assisted builder who directs **Claude Code** (and their own delivery platform, referred to as "your platform") to write most of the code. So every lab has two parts: *understand it* (a small, complete, commented implementation you read and run) and *direct it* (a ready-to-paste spec for Claude Code, plus the checks and review questions that tell you whether what it built is right). The learner must be able to explain and verify every line that ships.

- **Audience:** engineers, technical consultants, solution architects and AI-assisted builders who will build agents **for customers or for the business**; junior developers in a reading group; GCC bank, government and enterprise staff. Prerequisite: can read a short Python function and run a command line. Claude Code can write the rest, but the learner must understand it.
- **Honest, not hype.** Say what agents are good at, where they fail, and when not to build one. Never invent statistics, prices, benchmark scores, quotes, dates, URLs, version numbers or company policies. Hedge anything that changes ("at the time of writing (2026)"). Prices are never quoted as facts: show how to compute cost from the current price page.
- **Reading-group edition kept.** Each module still ends with a weekly **deliverable** (what to commit) and a **group session** agenda. Free external readings are linked, never quoted or copied.
- **Companion courses** (relative links; catalogue in `LIBRARY.md`): *Running AI Agents in Production* (governed agent operations, levels L0–L5), *Secure AI & Application Security* (module 8 AI attacks, 9 securing LLM apps and agents), *Software Testing: Zero to Hero in the AI Era* (6 AI-era testing, 7 evals, RAG and agent tests), *AI Product Management* (discovery, specs, evaluation, launch), *AI Governance* (frameworks, EU AI Act), *Cloud & DevOps* (containers, CI/CD, SLOs, FinOps, GPUs), *Data Engineering & Analytics* (data for LLM apps), *System Design for Vibe Coders* (directing an AI team, 9.x), *From Graduate to Hired*. Point to them in one line where they go deeper; stay on the *build-and-ship decision* here.

## The running customer engagement: Najm Desk (use these facts consistently)

**Najm Bank** is the fictional mid-sized Gulf bank (Qatar, the UAE and the EU) used across the library; say it is fictional in lesson 0.1. The learner joins **Developer Enablement** to build **Najm Desk**, an AI assistant for the bank's **IT Service Desk**, from first conversation to go-live. All numbers below are **fictional** and must be presented as such (a "fictional baseline" label) wherever they appear.

- **Customer:** the IT Service Desk. **Hind**, Head of IT Service Desk (the sponsor and the "customer" in every discovery and acceptance conversation); **Yara**, Service Desk team lead (the domain expert who knows how tickets are really handled).
- **Delivery team:** **Fahad**, Head of Developer Enablement (the reader's mentor, runs the reading group and the design reviews); **Lujain**, graduate engineer (the reader's peer; makes the mistakes the reader should avoid).
- **Governance and platform (from the library):** **Layla** (Head of AI Governance), **Noura** (Application & AI Security), **Hamad** (CISO), **Sara** (Data Protection Officer), **Maha** (SRE lead), **Salem** (Platform Engineering), **Dana** (lead data scientist), **Tariq** (engineering lead).
- **The baseline (fictional):** about 1,800 tickets a week; roughly a quarter are "how do I…?" or policy questions answerable from the policy library; about a quarter are access, password and MFA problems; the rest are hardware, network, software, security and other. Median first response about 3 h 40 min. Fourteen agents, Sunday to Thursday, 07:00 to 17:00 Qatar time; staff write in English and Arabic.
- **Systems (fictional):** the ticketing system **TicketHub**; the identity provider **Najm ID**; the policy library (the markdown documents in the lab kit, `labkit/data/policies/`); the HR directory **PeopleCore**; the device manager **DeviceDesk**.
- **Constraints:** the data-classification and AI-tools policies (no Confidential or Restricted data into external AI tools); staff personal data (privacy law applies); Arabic and English; changes need governance sign-off; every write action needs a human or a policy gate.
- **Najm Desk v1 scope:** policy Q&A with citations (RAG); ticket status (read tool); draft or create a ticket (write tool, with confirmation); an account-unlock *request* (approval-gated); hand-off to a human with the full context. Rollout: pilot with Service Desk staff as a copilot, then one business unit, then everyone.
- **Success measures (fictional targets):** deflection rate, first-response time, answer correctness on an eval set, escalation correctness, staff satisfaction, cost per resolved conversation, zero security incidents.

## The lab kit (every lab runs offline AND against the real API)

The repository folder `aiapps/labkit/` (GitHub: https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/aiapps/labkit) is the shared lab kit. **Read `aiapps/labkit/README.md`, `labkit/brain.py`, `labkit/mock_server.py`, `labkit/tools.py`, `labkit/embeddings.py` and `labkit/data/` before you write.** It contains a local **mock of the Anthropic Messages API** so the real `anthropic` SDK runs unchanged with no key and no cost: `python -m labkit.mock_server`, then `ANTHROPIC_BASE_URL=http://127.0.0.1:8787 ANTHROPIC_API_KEY=mock`. The mock simulates *mechanics* (the messages list, `tool_use`/`tool_result` rules, errors, retries, streaming, token growth, structured output, directives such as `[mock:loop]`), **not intelligence**: it cannot judge prompts, retrieval quality or safety. Rules for lessons:
- Every lab states **which steps work offline and which need a real model** ("Needs the real API: …"). Never claim the mock proves prompt quality.
- The lab code is the same in both modes; only environment variables differ. Lessons say so in Module 0 and remind briefly in labs.
- **Reference lab code lives in `aiapps/labkit/labs/mNN/`** (e.g. `labs/m01/chat.py`). Every lab code block in a lesson **starts with a first-line comment giving its path** (`# labs/m01/chat.py`) and must be **byte-identical to that file** (checked by `check_labs.py`). Put shared helpers in `labs/common/` when several modules need them. Keep each lab file short (under about 120 lines), complete, commented, and runnable offline with the mock plus any playbook you ship in `labkit/playbooks/` (`MOCK_PLAYBOOK=`). Tests for your lab files go in `labkit/tests/` and must pass with `cd aiapps/labkit && pytest`.
- You may extend `labkit/data/` (new files only; never rewrite existing ones) and add playbooks; do not edit `brain.py`, `mock_server.py`, `tokens.py` or existing tests: if the mock needs a change, say so in your report.
- Verification environment (never mention in lessons): Python venv `/home/user/coursework/venv-ai/bin/python` (anthropic 1.x, mcp, chromadb, rank-bm25, pydantic, fastapi, uvicorn, pytest, python-dotenv). Real-API calls cannot be made here; verify mechanics against the mock and verify SDK usage against the real SDK's installed types and the Claude API reference in `/home/user/coursework/claude-api-skill/` (read `python/claude-api/README.md`, `python/claude-api/tool-use.md`, and the `shared/` files it points to for your topic).

## Claude API facts every lab must respect (verified against the current SDK reference; this is where the owner's draft was out of date)

- **SDK:** `pip install "anthropic>=1,<2"`; `from anthropic import Anthropic`; `client = Anthropic()` reads `ANTHROPIC_API_KEY` (and `ANTHROPIC_BASE_URL`). The 1.x SDK is built on `httpx2`. Typed errors: `anthropic.BadRequestError`, `RateLimitError`, `APIStatusError`, `APIConnectionError`; the SDK retries 408/409/429/5xx/connection errors twice by default (`max_retries`, `with_options(...)`); default timeout 10 minutes.
- **Models (use exact ids; never invent ids; never append dates):** the labs default to **`claude-sonnet-5-5`** read from an environment variable (`MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")`); the cheap tier for routing and bulk eval work is **`claude-haiku-5-5`**; the strongest tier is `claude-opus-5-5`. Others in the current table: `claude-fable-5-1`, `claude-opus-5`, `claude-opus-4-8`, `claude-opus-4-7`, `claude-opus-4-6`, `claude-sonnet-5`, `claude-sonnet-4-6`, `claude-haiku-4-5`. Tell readers to check the models page or `client.models.retrieve(id)` (`max_input_tokens`, `max_tokens`, `capabilities`) because lists change. Context windows: current models list 1M tokens (Haiku 4.5: 200K). Show cost as arithmetic from the current price page, never as remembered numbers.
- **No sampling parameters:** `temperature`, `top_p`, `top_k` are **not parameters of `messages.create()` in the 1.x SDK** (passing them is a `TypeError`), and Claude Opus 5.5, Sonnet 5.5, Haiku 5.5, Opus/Sonnet 5, Fable 5.x and Opus 4.7/4.8 reject non-default values anyway; older models (Sonnet 4.6, Haiku 4.5…) accept them via `extra_body={"temperature": ...}`. Teach temperature as a concept, say honestly that you mostly cannot set it on current Claude models, and teach what gives consistency instead: precise prompts, structured outputs, schemas, retries with validation, caching results, and testing the *shape* of answers.
- **Thinking and effort:** current models think adaptively by default (`thinking={"type": "adaptive"}` or omitted). Thinking tokens are output tokens: set `max_tokens` generously (use **at least 1024**; the Claude API reference suggests about 16000 for non-streaming general use) and control depth and cost with `output_config={"effort": "low"|"medium"|"high"|"xhigh"|"max"}` (Sonnet 5.5 default `high`, Haiku 5.5 and Opus 5.5 default `medium`); the labs use `effort: "low"` for chat-style work. `budget_tokens` is removed on current models. Response `content` can start with a `thinking` block, so **never write `resp.content[0].text`**: take the text block (`next(b.text for b in resp.content if b.type == "text")`), or iterate and check `block.type`.
- **Stop reasons:** `end_turn`, `max_tokens` (truncated: raise the limit or stream), `stop_sequence`, `tool_use`, `pause_turn`, `refusal` (safety classifiers; `stop_details`). A production loop handles all of them.
- **Tool use protocol (the heart of Modules 3 and 8):** declare tools as `{name, description, input_schema}` (JSON Schema; `strict: true` guarantees input matches the schema); the model replies with `tool_use` blocks (`id`, `name`, `input`) and `stop_reason == "tool_use"`; **your code** runs the tool and replies with **one user message** containing a `tool_result` block (`tool_use_id`, `content`, optional `is_error: true`) for **every** `tool_use` id (parallel calls: all results in a single message). Append `resp.content` (the whole list) as the assistant turn. A missing `tool_result` is a 400. Forced `tool_choice` (`any`/`tool`) is rejected by the newest models (Sonnet 5.5, Opus 5.5, Fable 5.1): use `auto` plus an instruction, `strict: true`, or structured outputs. The SDK also offers a beta **tool runner** (`client.beta.messages.tool_runner` with `@beta_tool`) that runs the loop for you; teach the manual loop first.
- **Structured outputs:** `output_config={"format": {"type": "json_schema", "schema": {...}}}`, or the SDK helper `client.messages.parse(...)` with a Pydantic model; validate anyway and retry with the validation error as feedback. (`output_format` is deprecated; do not use it. Prefill of the assistant turn is removed on current models: do not teach it.)
- **Token counting:** `client.messages.count_tokens(model=..., messages=..., system=..., tools=...)`; never use `tiktoken` for Claude. Usage per call: `resp.usage.input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`.
- **Prompt caching:** prefix match (tools → system → messages); `cache_control={"type": "ephemeral"}` (top-level automatic or per block); verify with `cache_read_input_tokens`; any byte change in the prefix invalidates what follows; minimum cacheable prefix depends on the model. **Batch API** (`client.messages.batches`): asynchronous, about half price, results in any order keyed by `custom_id`. **Streaming:** `client.messages.stream(...)`/`.get_final_message()`.
- **Other surfaces (name them, link the docs, keep the manual loop as the teaching vehicle):** the beta tool runner; **Managed Agents** (Anthropic-hosted agent loop and sandbox; beta; persistent agent configs and sessions); the **Claude Agent SDK** (Claude Code's harness as a library: a *different* package); the **MCP connector** in the Messages API; server tools (web search, web fetch, code execution); context editing and compaction (beta) for long conversations; the memory tool. Mark betas as betas and hedge availability by platform ("check the platform availability table").
- **Observability:** the SDK can emit OpenTelemetry spans; the OpenTelemetry GenAI semantic conventions exist (hedge: still evolving). Log per call: model, latency, input/output/cached tokens, stop reason, request id (`resp._request_id`), tool calls, cost estimate.
- **Never in lessons:** hard-coded API keys; `eval()` on model output; real customer data; instructions to attack systems you do not own.

## Other facts to get right (and how to hedge)

State only what you are confident is true; hedge anything that changes; never invent.
- **Agents and workflows:** Anthropic's "Building effective agents" distinguishes *workflows* (LLMs and tools orchestrated by predefined code paths: prompt chaining, routing, parallelisation, orchestrator-workers, evaluator-optimiser) from *agents* (the model directs its own process and tool use); start with the simplest thing that works. ReAct (Yao et al., 2022); reflection/self-refine; planning; the agent loop; stopping conditions (max iterations, token budget, wall-clock timeout, no-progress detection). Multi-agent: supervisor/worker, hand-offs, shared state; costs multiply and errors compound; most tasks need one agent with good tools.
- **RAG:** embeddings and similarity (cosine), chunking strategies and overlap, vector stores (Chroma, pgvector, others), lexical search BM25, **hybrid search** with reciprocal rank fusion, reranking, citations, query rewriting; failure modes: bad chunks, missed retrieval, wrong-but-confident answers, stale documents, access-control leakage (point to *Secure AI* 9.3); evaluate retrieval (recall@k, MRR) separately from generation (groundedness); embedding models are separate from chat models (Anthropic does not offer an embeddings endpoint in the Messages API: name providers generically and use the lab kit's toy embedding offline).
- **MCP (Model Context Protocol):** open protocol (introduced by Anthropic, Nov 2024; now under open governance, hedge); hosts, clients, servers; primitives: **tools, resources, prompts**; transports: stdio and Streamable HTTP; authorisation via OAuth 2.1 for HTTP servers; official SDKs (Python `mcp` with `FastMCP`); name spec revisions by date and tell readers to check modelcontextprotocol.io. Security: tool poisoning, over-broad scopes, confused deputy, untrusted servers (point to *Secure AI* 9.2). When MCP is worth it (many clients, shared tools, third-party tools) versus plain functions (one app, one team).
- **Memory:** short-term (context), working (scratchpad/state), long-term (store), episodic vs semantic memory; summarisation/compaction; memory writes as tools; what not to remember (secrets, personal data without a purpose); forgetting and retention (privacy duties); memory poisoning.
- **Evaluation:** golden sets, error analysis before metrics, graders (code, LLM-as-judge with known biases, humans), trajectory evaluation for agents, regression gates in CI, online evaluation; point to *Software Testing* 7.1–7.3 and *AI Product Management* 6.1–6.3 instead of repeating them; here teach how to *put an agent under an eval and a CI gate*.
- **Security and governance:** OWASP Top 10 for LLM Applications (2025 edition) incl. prompt injection, sensitive information disclosure, excessive agency; MITRE ATLAS; least privilege for tools; human-in-the-loop approvals; PII masking; audit logs; the "lethal trifecta" idea (private data + untrusted content + external communication — Simon Willison; present as one practitioner's framing); NIST AI RMF and its Generative AI profile; ISO/IEC 42001; **EU AI Act** (risk tiers; obligations on providers and deployers; point to *AI Governance* 6.x; no article numbers beyond those you are sure of); GCC data-protection and financial-regulator expectations (hedge; no clause numbers; Qatar's PDPPL and the EU GDPR by name only).
- **Enterprise-grade controls:** agent identity and delegated access (OAuth on-behalf-of vs a service account; least privilege per tool and per user); secrets management; multi-tenancy and data isolation; data residency; audit trails; rate limits and quotas; kill switches; model/prompt change management (versioned, reviewed, evaluated, rolled out gradually); vendor and model-provider risk; business continuity (fallback model, degraded mode); documentation (system card, risk register, runbooks).
- **Shipping:** containers, environments (dev/test/staging/prod), secrets and config, queues and asynchronous work, **durable execution** (Temporal, AWS Step Functions, others) for long-running agents, idempotency keys, timeouts, retries with exponential backoff and jitter, circuit breakers; CI/CD with **evals as a gate**; versioning prompts, tools and models; canary and shadow releases, feature flags, rollback; cost tracking per request, budgets and alerts, caching, batching, model routing (cheap model first, escalate); point to *Cloud & DevOps* 4.1–4.2, 5.1–5.2, 6.2–6.3 and *System Design for Vibe Coders*.
- **Operating and handover:** observability (traces of every step), SLOs for agents (task success, latency, cost, escalation rate), alerting without fatigue, incident response and blameless reviews, feedback loops from users into the eval set, support model (L1/L2/L3), training and change management, acceptance testing, benefits tracking; point to *Running AI Agents in Production*.
- **Requirements and design with customers (Modules 6–7, 16):** stakeholder mapping (sponsor, users, operators, risk owners); discovery interviews (open questions, past behaviour over opinions; "The Mom Test" by Rob Fitzpatrick as a guide); shadowing and process mapping; jobs-to-be-done; user stories and acceptance criteria (Given/When/Then); functional and non-functional requirements (latency, availability, security, privacy, language, accessibility, auditability, cost); out-of-scope lists; assumptions and risks; **autonomy levels** (suggest → draft → decide with approval → act); human-in-the-loop design; MoSCoW prioritisation; RACI; **architecture decision records** (Michael Nygard, 2011); the **C4 model** (Simon Brown) for diagrams; prototypes and "Wizard of Oz" tests; proposals and statements of work (scope, deliverables, assumptions, acceptance, change control, phases); estimating under uncertainty (ranges, spikes); pilots and phased rollout; benefits cases (fictional numbers only unless the reader supplies their own); change requests. Never give legal or contract advice beyond general practice; tell readers to involve their legal and procurement teams.
- **Claude Code (Module 0.3 and the "Build it with Claude Code" boxes):** use only well-known, stable features and hedge ("check the current Claude Code documentation"): `CLAUDE.md` project memory; plan mode (plan before editing); permissions and allow-lists; slash commands; subagents; hooks (run commands on events, e.g. run tests or evals after edits); MCP servers added to Claude Code; headless/non-interactive mode in CI. The method (not the product) is the lesson: **spec → plan → implement in small steps → verify with tests and evals → review the diff → commit.** Never claim Claude Code guarantees correctness. Point to *System Design for Vibe Coders* 9.x and *Software Testing* 6.1–6.2 for verifying agent-written code.
- **Your platform ("connectsw"):** the owner builds with Claude Code **and their own delivery platform**. Where deployment or integration is discussed, include a short, generic **"Your platform"** box: the questions to answer about any internal platform (identity, secrets, deploy target, observability, ticketing, approval workflow, data residency), with a table the reader fills in. Do not describe a platform you have not been given details of.

Real cases you may use (well documented only; hedge details): Air Canada's chatbot ruling (Moffatt v. Air Canada, 2024, British Columbia Civil Resolution Tribunal); the July 2025 report of an AI coding agent deleting a production database (Replit/SaaStr, as reported); documented prompt-injection demonstrations against email/document assistants (name generically); Knight Capital (2012) for release discipline. Otherwise use clearly hypothetical Najm scenarios.

## Layer (the lesson tag)

Every lesson is tagged with one or two layers, in English, in both languages, chosen only from: **Model · Applications · Delivery · Agents · Production**. Header: `*Layer: Agents*` or `*Layer: Delivery, Production*`.

## Module and lesson plan (numbers are fixed)

| Module | File | Lessons |
|---|---|---|
| 0 Orientation: the lifecycle, your lab and your build partner | 00-orientation.md | 0.1 What it takes to ship an enterprise-grade agent: the delivery lifecycle, the layers and how this course works · 0.2 Your lab: setup, the lab kit, the API key and a spending cap · 0.3 Your build partner: directing Claude Code to build agents (and what you must still understand) |
| 1 How an LLM application actually works | 01-llm-app.md | 1.1 The one idea: a stateless function, tokens, the context window and the messages list · 1.2 Lab: a chatbot with memory, break it on purpose, then your first agent loop |
| 2 Prompting as engineering | 02-prompting.md | 2.1 System prompts as specifications: role, task, format, constraints, examples and reasoning · 2.2 Lab: from a vague prompt to a versioned, tested prompt with a 20-case eval set |
| 3 Structured output and tool use | 03-tools.md | 3.1 Schemas and tools: how the model "calls" a function (you do), validation and retries · 3.2 Lab: three tools, every call traced, errors handled |
| 4 Retrieval-Augmented Generation | 04-rag.md | 4.1 RAG: embeddings, chunking, vector stores, hybrid search, reranking, citations, and why it fails · 4.2 Lab: a policy Q&A bot with Chroma, then BM25 and a comparison |
| 5 Workflow patterns | 05-workflows.md | 5.1 Chaining, routing and parallelisation: when a workflow beats an agent · 5.2 Lab: a document pipeline: classify, route, summarise, fact-check in parallel |
| 6 Discovery and requirements | 06-requirements.md | 6.1 Discovery: from a business problem to an agent brief: stakeholders, workflows, data, risk and "should this be an agent?" · 6.2 The agent specification and acceptance criteria: requirements you can test |
| 7 Designing the solution with the customer | 07-design.md | 7.1 Architecture and autonomy design: workflow or agent, tool surface, human-in-the-loop, failure design, build or buy · 7.2 Prototype, propose and agree scope: demos, proposals, phased rollout and change control |
| 8 The agent loop, properly | 08-agent-loop.md | 8.1 Plan, act, observe, repeat: reflection, stopping conditions and the first failure modes · 8.2 Lab: an agent loop from scratch in about 80 lines, with a hard cap and full trace logging |
| 9 Memory and state | 09-memory.md | 9.1 Short-term, working and long-term memory: what to remember and what never to · 9.2 Lab: persistent memory across sessions, with a "forget" command |
| 10 MCP and connecting to the real world | 10-mcp.md | 10.1 The Model Context Protocol: servers, tools, resources, authorisation and least privilege · 10.2 Lab: expose the ticket system as an MCP server and let the agent use it |
| 11 Multi-agent systems | 11-multi-agent.md | 11.1 Supervisors, workers and hand-offs: when multi-agent is the wrong answer · 11.2 Lab: a three-agent team with explicit hand-off contracts |
| 12 Evaluation and testing | 12-evaluation.md | 12.1 Evaluating agents: eval sets, graders, LLM-as-judge, trajectories and regression gates · 12.2 Lab: put every agent under a 50-case eval and a CI check |
| 13 Guardrails, security and governance | 13-security.md | 13.1 Threats and guardrails: prompt injection, tool permissions, PII, approvals and audit logs · 13.2 Enterprise controls: agent identity, multi-tenancy, data residency, compliance and the governance pack |
| 14 Shipping to production | 14-shipping.md | 14.1 Deploying an agent: containers, environments, queues, durable execution, release strategies and rollback · 14.2 Cost, latency and reliability engineering: budgets, caching, routing, retries and SLOs |
| 15 Operating and handing over | 15-operating.md | 15.1 Running an agent in production: observability, alerts, incidents, runbooks and the improvement loop · 15.2 Handover and adoption: training, support model, acceptance, change management and benefits tracking |
| 16 Hero: capstone and practice exam | 16-capstone.md | 16.1 Capstone: take Najm Desk from discovery to go-live, with the customer · 16.2 Practice exam: 60 scenario questions |

Levels: 🟢 Beginner for Modules 0–3 (and 6.1), 🟡 Intermediate for Modules 4–5, 6.2–7, 8–11, 12.1, 🔴 Advanced for 12.2, Modules 13–16 (use judgement per lesson).
**Odd-numbered lessons (N.1) are concept lessons; N.2 lessons are labs** (for Modules 1–5 and 8–12 and 14–15 the second lesson is a lab or applied project; Modules 6, 7, 13 and 16 are applied workshops). In every lab lesson, the 🏛️ section carries the weekly **deliverable**, the **group session** agenda and the **"Build it with Claude Code"** box (a fenced `text` block with the spec to give Claude Code, then a "Verify before you accept it" checklist). In every concept lesson, 📚 References carries the **"Read this week"** list from `/home/user/coursework/aiapps-source.md` for that module (keep the owner's chapter mappings as given; no quotes; links only to the sources listed in lesson 0.1's references).

## Code snippets (they will be run)

Every runnable snippet is executed by a verifier before publication:
- Python 3.11+, the 1.x `anthropic` SDK, Pydantic 2, `chromadb`, `rank-bm25`, the Python `mcp` SDK. Show imports. Comment liberally ("read every comment, the comments are the lesson"). No framework until Module 11's comparison box; teach the pattern raw first.
- Where a snippet is *meant* to fail, say so in a comment and show the output in a separate block.
- Lab code blocks carry the path comment and equal the file in `labkit/labs/mNN/` (see above). Output blocks are tagged ```text.
- Shell commands: real, current flags only. Fenced blocks have a language tag (`python`, `bash`, `yaml`, `json`, `text`, `dockerfile`).

## File format (the build parses this — follow exactly)

```
# Module 3 — Structured output and tool use

*One-paragraph italic module intro: what the module covers and why, tied to Najm Desk.*

> **Layer:** Applications — …(one line in the course's words)

---

# 3.1 — Schemas and tools: how the model "calls" a function (you do), validation and retries
*Level: 🟡 Intermediate* · *Prerequisites: 1.2, 2.1* · *Layer: Applications*

## ⚡ In 60 seconds
- 4–6 bullets: what it is, the rule that matters most, the decision cue, the biggest trap.

## 🧭 Why it matters
A Najm Desk scenario (or a well-documented public failure) that makes the topic unavoidable. 1–3 paragraphs.

## 📐 How it works
### 🟢 The essentials
### 🟡 Going deeper
### 🔴 Expert view
(Plain explanations first; define every term on first use; short correct snippets in fenced blocks; tables; one mermaid diagram where it genuinely helps. Mermaid: flowchart or sequence only, `flowchart LR` or `TD`, short labels in double quotes, no parentheses inside labels.)

## 🧰 The toolkit
| Tool, practice or pattern | What it is and does | When to reach for it |
|---|---|---|
| **Tool definition** | … | … |
(3–8 rows. The first cell MUST start with the name in bold, e.g. **Tool use loop**, **Prompt caching**, **MCP server**, **Eval gate**, **Agent brief**, **ADR**; optionally followed by a short credit in parentheses. Keep bold names identical wherever the same item appears; they build the toolkit catalogue.)

## 🏛️ In practice at Najm Bank
The artefact this lesson produces (a spec, a prompt file, a tool schema, an eval set, a runbook, a handover pack…) and, in lab lessons, the weekly deliverable, group-session agenda and the "Build it with Claude Code" box. Concrete and reusable, about Najm Desk.

## 🛠️ Exercises
Three graded exercises: 🟢 …, 🟡 …, 🔴 …, each with a "*Done when:*" line. Say for each whether it needs the real API.

## ⚠️ Mistakes and traps
4–6 bullets: the trap, then what to do instead.

## 🧾 Recap
4–6 bullets.

## ✍️ Check yourself
Five multiple-choice questions (at least three scenario-based). Format:

**1. Question text?**

- A. …
- B. …
- C. …
- D. …

<details><summary>Answer</summary>

**B.** Why B is right, and why the tempting distractor is wrong. (Pointer to the section.)

</details>

## 📚 References
Official docs and primary sources only (docs.anthropic.com / platform.claude.com docs, github.com/anthropics, modelcontextprotocol.io, owasp.org / genai.owasp.org, nist.gov, eur-lex.europa.eu, sre.google, opentelemetry.io, docs.python.org, pydantic.dev, trychroma.com, the five course sources named in lesson 0.1). Plain links; if unsure of a deep link, link the top-level page. For concept lessons, add the "Read this week" list.
```

- Separate lessons with a `---` line.
- Lesson 16.2 (practice exam) follows the same outer format but its body is: ⚡ (how to take it), then `## ✍️ Practice exam` with 60 questions numbered 1–60 in the same Q/A format, mixed across all seventeen modules, each answer ending with its layer and the lesson to review, e.g. *(Agents · 8.2)*; then 🧾 and 📚.

## Quiz quality rules (every ✍️ block and the exam)

- Exactly one clearly correct option, defensible from the lesson; three distractors that are plausible mistakes practitioners really make. No "all/none of the above", no "Which is NOT".
- **The correct option must not be systematically the longest or the shortest.** Options of similar length and grammatical form; the correct one must not be the only hedged or qualified option. Across a lesson's five questions it may be the longest in at most two and the shortest in at most two (exam: each at most about a quarter).
- Spread the correct letters across A–D (no letter more than twice in a lesson's five; exam: roughly 15 each).
- Test judgement and application in scenarios, not trivia or wording recall.

## Style

- Plain, direct English; short sentences; define jargon on first use; no hype, no filler. Explain *why*, not just *what*.
- Lengths: 2,000–3,500 words per lesson (16.2 excepted). Every lesson's five questions must be answerable from that lesson.
- Use the running cast and the Najm Desk canon consistently. Do not start any non-quiz line with `**N.` (bold number + dot).
- Cross-course references: the reader auto-links any bare "lesson N.M", "lessons N.M", "see N.M", "(N.M" to a lesson of THIS course, so another course's lesson number may only appear inside a markdown link's text, e.g. `[*Software Testing*, lesson 7.1 — Evals](../testing/index.html#/7.1)`.
