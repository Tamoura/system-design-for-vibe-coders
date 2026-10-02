# The course library — catalogue for cross-links (not published)

All courses are free, bilingual (EN/AR) and live side by side on one site (the vibe course is deployed at /vibe/).
From a page in a new course at `/<course>/index.html`, link to another course's lesson with a RELATIVE link:

| Course | Link to a lesson (English) | Arabic page |
|---|---|---|
| System Design for Vibe Coders (production engineering for people who build with AI agents) | `../vibe/index.en.html#l4-1` (lesson 4.1; foundations F.2 → `#lF-2`; capstone module 12 → `#l12`) | `../vibe/index.ar.html#l4-1` |
| SaaS Building Blocks (the ~25 components every SaaS shares, with open-source repos) | `../saas/index.html#/2.1` | `../saas/index.ar.html#/2.1` |
| AI Governance: Zero to Hero (AIGP-aligned) | `../aigp/index.html#/6.2` | `../aigp/index.ar.html#/6.2` |
| AI Product Management: Zero to Hero | `../aipm/index.html#/6.1` | `../aipm/index.ar.html#/6.1` |
| Secure AI & Application Security: Zero to Hero | `../secai/index.html#/3.3` | `../secai/index.ar.html#/3.3` |
| Running AI Agents in Production (levels L0–L5, labs, playbook, skills assessment) | `../agentic/learning-path.html#level-2-agent-engineer` | `../agentic/learning-path.ar.html` |
| Each course's self-assessment | `../<course>/assessment.html` (vibe: `../vibe/assessment.html`) | `assessment.ar.html` |

Rules: link only to lessons listed below (they exist); use the link text "*Course name*, lesson N.M — title"; a link
supplements the lesson, it never replaces teaching the decision in this course.

## System Design for Vibe Coders (vibe)


**Part 0 — Foundations (no prerequisites)**
- F.1 What happens when you open a website.
- F.2 What a server actually is (and what code is).
- F.3 Versions, repos, and deploys — how software moves.
- F.4 Meet your agent: how to direct a builder you can't watch.
- F.5 Your first live page — with proof.

**Module 0 — The Vibe Coder's Gap**
- 0.1 "It works" is not a property of a system.
- 0.2 The map of everything that can hurt you.
- 0.3 Build vs buy: the highest-leverage decision you'll make.

**Module 1 — Anatomy of a Real App**
- 1.1 Draw the boxes before the agent writes the code.
- 1.2 The request's journey.
- 1.3 Day-one eyes: your first error tracker and uptime check.

**Module 2 — Data, Storage & Backups**
- 2.1 The database is the easy part.
- 2.2 Object storage and the two-owner trap.
- 2.3 Backups: what, not just whether.
- 2.4 Retention, deletion, and the data you promised to erase.
- 2.5 Indexes, queries, and the working set.
- 2.6 Two clicks at once: races, transactions, and idempotent writes.

**Module 3 — Caching: the Sharpest Knife in the Drawer**
- 3.1 Why caching is where correctness goes to die.
- 3.2 The cache poisoning incident.
- 3.3 Invalidation in real life.
- 3.4 When the cache takes you down.

**Module 4 — Deploys Without Downtime**
- 4.1 Shipping is a system.
- 4.2 Blue-green and the shared-directory 502s.
- 4.3 The proxy lies: stale workers and trusting your own verification.
- 4.4 Rollback, staging, and release gates.
- 4.5 Verify the artifact, not the source.

**Module 5 — Real Users, Real Abuse**
- 5.1 Your first attacker is a script.
- 5.2 Rate limiting that survives a CDN.
- 5.3 Auth that you can operate.
- 5.4 Input you didn't realize you were trusting.
- 5.5 Email is production infrastructure.
- 5.6 The OWASP Top 10, mapped to a real app.
- 5.7 Secrets and configuration: the keys to the kingdom.

**Module 6 — One Backend, Many Clients**
- 6.1 The client fleet problem.
- 6.2 Over-the-air updates and the revert trap.
- 6.3 Feature flags done once, not five times.
- 6.4 Deep links and the drift problem.
- 6.5 Sign in with Google & Apple, on every client.
- 6.6 API design that survives its clients.
- 6.7 You are someone's client too: surviving third-party APIs.

**Module 7 — Observability: You Can't Fix What You Can't See**
- 7.1 The dashboard that lies and the metric that doesn't.
- 7.2 Errors, logs, and the noise floor.
- 7.3 Search is telemetry.
- 7.4 Background jobs: the code nobody watches.
- 7.5 Product analytics in practice: GA, Cloudflare, and owning your events.
- 7.6 Your monitoring stack: Sentry, uptime checks, metrics, and alerts.

**Module 8 — Safety Nets for AI-Generated Code**
- 8.1 The 600-file near-miss.
- 8.2 Tests as the spec the agent can't ignore.
- 8.3 CI preflight and the boy-who-cried-wolf check.
- 8.4 The software you didn't write: dependencies and supply chain.

**Module 9 — Directing an AI Team**
- 9.1 You are the architect now.
- 9.2 Context engineering.
- 9.3 Every repeated review comment is a missing guardrail.
- 9.4 Verification before completion.
- 9.5 Claude Code power techniques.
- 9.6 Building your agent team: custom agents and skills.
- 9.7 Code audit and review at agent speed.
- 9.8 The governance glance: you own what your agent ships.

**Module 10 — Scaling Beyond One Server**
- 10.1 Stateless services and load balancing.
- 10.2 Queues and asynchronous work.
- 10.3 Scaling the database.
- 10.4 Realtime: presence, websockets, and heartbeats.
- 10.5 Performance and capacity.

**Module 11 — Reaching the World**
- 11.1 Domains, DNS, and TLS.
- 11.2 Internationalization and RTL.
- 11.3 SEO and AEO: being found by crawlers and cited by answer engines.
- 11.4 Cost engineering.
- 11.5 Your edge platform in practice: Cloudflare end to end.

**Module 12 — Capstone: You Get Paged**

## SaaS Building Blocks (saas)


**Module 0 — Orientation: Every SaaS Is the Same App**
- 0.1 The 80% nobody sells: the anatomy of every SaaS
- 0.2 How to read a giant open-source codebase without drowning
- 0.3 The reference shelf: the SaaS codebases and starter kits we study

**Module 1 — Identity & Access**
- 1.1 Authentication: proving who someone is
- 1.2 Users, organizations & invitations: the multi-tenant skeleton
- 1.3 Authorization: roles, permissions, and "can this user do this?"
- 1.4 Enterprise identity: SSO, SAML, OIDC and SCIM

**Module 2 — Data**
- 2.1 The data layer: Postgres, ORMs, migrations and seeds
- 2.2 File uploads and object storage
- 2.3 Search: from `LIKE '%x%'` to a search engine
- 2.4 Multi-tenancy deep dive: isolation, noisy neighbours, residency

**Module 3 — Money**
- 3.1 Subscriptions and payments: checkout, webhooks, the customer portal
- 3.2 Plans, limits and entitlements: turning pricing into code
- 3.3 Usage-based billing and metering

**Module 4 — Communication**
- 4.1 Transactional email that actually arrives
- 4.2 Notifications: in-app, push, Slack, SMS — and preferences
- 4.3 Real-time and collaboration: WebSockets to CRDTs

**Module 5 — Background Work & Integrations**
- 5.1 Background jobs, queues and scheduled tasks
- 5.2 The public API: API keys, versioning and rate limits
- 5.3 Outbound webhooks and third-party integrations
- 5.4 Workflow engines and durable execution

**Module 6 — Product & Growth**
- 6.1 The app shell: marketing site, onboarding, dashboard and settings
- 6.2 Analytics: product, web and the event pipeline
- 6.3 Feature flags and experiments

**Module 7 — Operating the SaaS**
- 7.1 The admin panel: support tools and impersonation
- 7.2 Observability: logs, errors, metrics and traces
- 7.3 Audit logs and activity feeds
- 7.4 Deployment, environments and self-hostable SaaS

**Module 8 — Trust & the Frontier**
- 8.1 Security and compliance: secrets, encryption, SOC 2, GDPR
- 8.2 AI features as a SaaS component

**Module 9 — Capstone**
- 9.1 Assemble Beacon: reference architecture, build-vs-buy and a 90-day plan

## AI Governance: Zero to Hero (aigp)


**Module 0 — Orientation**
- 0.1 What AI governance is, and what the AIGP proves
- 0.2 How the exam thinks: BoK v2.1, question styles, a study plan
- 0.3 Meet Najm Bank: an AI inventory from day one

**Module 1 — What AI is and why it needs governance**
- 1.1 AI, machine learning, generative AI and agents
- 1.2 Risks and harms to people, groups, organisations and society
- 1.3 Why AI is different: the traits that demand governance

**Module 2 — Organisational expectations**
- 2.1 From principles to strategy and risk appetite
- 2.2 Roles, accountability and the AI governance committee
- 2.3 AI literacy, training and culture

**Module 3 — Policies across the life cycle**
- 3.1 The AI life cycle and the policy stack
- 3.2 Data governance and intellectual-property policies for AI
- 3.3 Third-party and supply-chain risk

**Module 4 — Privacy and data protection law**
- 4.1 Data protection principles meet AI
- 4.2 Automated decisions, individual rights and transparency
- 4.3 DPIAs and the global privacy map, from the EU to the GCC

**Module 5 — Other laws that already apply**
- 5.1 Non-discrimination in hiring, credit and services
- 5.2 Intellectual property in AI inputs and outputs
- 5.3 Consumer protection, product liability and sector rules

**Module 6 — The EU AI Act**
- 6.1 Scope, roles and the risk pyramid
- 6.2 High-risk obligations for providers and deployers
- 6.3 General-purpose AI, transparency, enforcement and the timeline

**Module 7 — Standards and frameworks**
- 7.1 OECD principles and the NIST AI RMF
- 7.2 ISO/IEC 42001 and the AI standards family
- 7.3 The global map: other frameworks that shape practice

**Module 8 — Governing design and build**
- 8.1 Use-case intake, business case and risk tiering
- 8.2 Designing for trustworthiness
- 8.3 Documentation, and build versus buy

**Module 9 — Data for training and testing**
- 9.1 Sourcing, lineage and rights to use data
- 9.2 Quality, representativeness and bias
- 9.3 Testing, evaluation, validation and red-teaming

**Module 10 — Release, monitoring and maintenance**
- 10.1 Release readiness and conformity
- 10.2 Monitoring, drift and incidents
- 10.3 Change management, maintenance and retirement

**Module 11 — Deploying and using AI**
- 11.1 The deploy decision: context, stakeholders and alternatives
- 11.2 Buying AI: vendor due diligence and contracts
- 11.3 Assessing the system: impact assessments, audits and assurance
- 11.4 Governing use: oversight, transparency and incident response

**Module 12 — Hero: capstone and exam**
- 12.1 Capstone: governing Najm's credit copilot end to end
- 12.2 Exam strategy and the traps that cost marks
- 12.3 Full mock exam: 100 questions

## AI Product Management: Zero to Hero (aipm)


**Module 0 — Orientation**
- 0.1 What AI product management is, and what it is not
- 0.2 How AI products differ: probabilistic, data-hungry, costly per use, trust-bound
- 0.3 Meet Najm Bank's AI product team, and how to use this course

**Module 1 — AI literacy for product people**
- 1.1 Machine learning, generative AI, LLMs and agents: what each is good for
- 1.2 Capabilities and limits: errors, hallucination, context, latency and cost
- 1.3 The build spectrum: prompt, retrieval (RAG), fine-tune, train, or buy

**Module 2 — Finding problems worth solving**
- 2.1 Discovery for AI: jobs, workflows and where AI fits
- 2.2 Scoring and choosing use cases: value, feasibility, risk
- 2.3 When not to use AI, and killing ideas early

**Module 3 — Data as the product's foundation**
- 3.1 Data readiness: do we have what the product needs?
- 3.2 Feedback loops, flywheels and learning products
- 3.3 Privacy, consent and data rights: what the PM must own

**Module 4 — Designing AI experiences**
- 4.1 Levels of automation: suggest, draft, decide, act
- 4.2 Designing for trust: expectations, explanations, errors and recovery
- 4.3 Conversational and agentic experiences

**Module 5 — Specifying and building**
- 5.1 The AI product spec: behaviour, quality bars and evals as requirements
- 5.2 Prototyping fast and working with ML and AI engineers
- 5.3 Prompts, context and tools as product surface

**Module 6 — Evaluation: knowing it works**
- 6.1 Quality you can measure: metrics, golden sets and error analysis
- 6.2 LLM-as-judge, human review and red-teaming
- 6.3 Online evaluation: experiments, A/B tests and staged rollouts

**Module 7 — Launching AI products**
- 7.1 Launch readiness: guardrails, governance gates and support
- 7.2 Go-to-market: positioning, pricing signals and enablement
- 7.3 Adoption and change management inside the enterprise

**Module 8 — Metrics, economics and growth**
- 8.1 Product metrics for AI: value, quality, adoption, trust
- 8.2 Unit economics: cost to serve, pricing models and margins
- 8.3 Monitoring, drift and the iteration loop after launch

**Module 9 — Strategy and leadership**
- 9.1 AI product strategy and defensibility
- 9.2 Roadmaps under uncertainty: bets, platforms and model change
- 9.3 Teams, roles and operating model for AI products
- 9.4 Responsible AI and regulation: the PM's part

**Module 10 — Hero: capstone and practice exam**
- 10.1 Capstone: take Najm Assist from idea to scale
- 10.2 The AI PM career: interviews, portfolio and growth
- 10.3 Practice exam: 60 scenario questions

## Secure AI & Application Security: Zero to Hero (secai)


**Module 0 — Orientation**
- 0.1 What application and AI security is: assets, attackers and risk
- 0.2 How breaches really happen: the attack chain and the usual suspects
- 0.3 Meet Najm Bank's security team, and how to use this course

**Module 1 — Thinking like a defender**
- 1.1 Threat modelling: data flows, trust boundaries and STRIDE
- 1.2 Security principles: least privilege, defence in depth, secure defaults, zero trust
- 1.3 Rating and prioritising risk: likelihood, impact and CVSS

**Module 2 — Web application security**
- 2.1 Injection: SQL, command and template injection
- 2.2 Browser attacks: XSS, CSRF, and the headers that stop them
- 2.3 Server-side traps: SSRF, file uploads, path traversal and deserialisation

**Module 3 — Identity and access**
- 3.1 Authentication: passwords, MFA, passkeys and sessions
- 3.2 OAuth 2.0, OpenID Connect and token pitfalls
- 3.3 Authorisation: broken access control, IDOR and multi-tenancy

**Module 4 — APIs, mobile and abuse**
- 4.1 The OWASP API Security Top 10 in practice
- 4.2 Abuse, bots, rate limits and business-logic flaws
- 4.3 Mobile app security: what you can and cannot trust on the device

**Module 5 — Data, cryptography and secrets**
- 5.1 Cryptography for builders: TLS, hashing, encryption and keys
- 5.2 Secrets management: keys, tokens and where they leak
- 5.3 Protecting personal data: minimisation, logging and privacy engineering

**Module 6 — Secure development and supply chain**
- 6.1 A secure development life cycle: requirements, review and testing (SAST, DAST, SCA)
- 6.2 The software supply chain: dependencies, SBOMs, SLSA and signing
- 6.3 Securing AI-generated code: what coding agents get wrong

**Module 7 — Cloud and infrastructure**
- 7.1 Cloud security: shared responsibility, IAM and misconfiguration
- 7.2 Containers, Kubernetes and infrastructure as code
- 7.3 Networks and the edge: segmentation, WAFs and DDoS

**Module 8 — How AI systems get attacked**
- 8.1 The AI attack surface: OWASP Top 10 for LLM Applications and MITRE ATLAS
- 8.2 Prompt injection and jailbreaks, direct and indirect
- 8.3 Attacks on data and models: poisoning, evasion, extraction and inference

**Module 9 — Securing LLM apps and agents**
- 9.1 Guardrails and output handling: never trust model output
- 9.2 Agents and tools: excessive agency, least-privilege tools and MCP
- 9.3 Securing retrieval (RAG): data boundaries and access control
- 9.4 AI red-teaming and security evaluation

**Module 10 — Detection and response**
- 10.1 Logging, monitoring and detection engineering
- 10.2 Incident response: prepare, detect, contain, recover, learn
- 10.3 Vulnerability management, disclosure and bug bounties

**Module 11 — Governance and leadership**
- 11.1 Frameworks: NIST CSF 2.0, ISO/IEC 27001, NIST SSDF and OWASP SAMM
- 11.2 Regulation that touches security: GDPR, PDPPL, the EU AI Act and financial-sector rules
- 11.3 Building a security programme and culture: champions, metrics and budgets

**Module 12 — Hero: capstone and practice exam**
- 12.1 Capstone: secure Najm Assist from threat model to incident drill
- 12.2 The security career: roles, certifications and portfolio
- 12.3 Practice exam: 60 scenario questions

## Running AI Agents in Production (agentic)

Levels (anchors on learning-path.html): Level 0 — Literate (`#level-0-literate`), Level 1 — Builder (`#level-1-builder`),
Level 2 — Agent Engineer (`#level-2-agent-engineer`), Level 3 — Production Engineer (`#level-3-production-engineer`),
Level 4 — Regulated-AI Specialist (`#level-4-regulated-ai-specialist`), Level 5 — Hero / Program Lead (`#level-5-hero-program-lead`).
Also: production-playbook.html, on-ramp-poster.html, assessment.html (skills assessment).

## New courses being written now (link by course name; their lesson plans are in their AUTHORING.md)

- From Graduate to Hired (career) — `../career/index.html#/N.M` — plan: /home/user/system-design-for-vibe-coders/career/AUTHORING.md
- Data Engineering & Analytics: Zero to Hero (data) — `../data/index.html#/N.M` — plan: /home/user/system-design-for-vibe-coders/data/AUTHORING.md
- Cloud & DevOps: Zero to Hero (cloud) — `../cloud/index.html#/N.M` — plan: /home/user/system-design-for-vibe-coders/cloud/AUTHORING.md

