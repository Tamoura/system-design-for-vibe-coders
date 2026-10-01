# Secure AI & Application Security: Zero to Hero — authoring guide

This is the contract every lesson follows. It is not published.

## What the course is

A free, bilingual (English/Arabic) course that takes a reader from zero to "hero" in **securing applications and AI systems**: how attackers think and get in, threat modelling, the classic web, API, identity and cloud weaknesses and their fixes, cryptography and secrets for builders, a secure development life cycle and software supply chain, the new attack surface of LLM applications and AI agents (prompt injection, data and model attacks, excessive agency), detection and incident response, and running a security programme.

- **Audience:** developers (including people who build with AI coding agents), architects, product and engineering managers, security analysts moving into AppSec or AI security, and GCC bank, government and enterprise staff who own systems. No security background assumed at the start; basic familiarity with how web apps work helps (Module 1 of *System Design for Vibe Coders* is enough).
- **Defensive and educational.** Explain how attacks work at the level a defender needs to recognise, test for and prevent them. Use classic, widely published illustrative examples (e.g. `' OR '1'='1`, `<script>alert(1)</script>`, "ignore previous instructions"). Never give step-by-step weaponised exploit chains, working malware, evasion techniques, or instructions for attacking systems the reader does not own. Every attack section ends in the defence. Testing is always on your own systems or with written authorisation.
- **Not a certification prep course** and not affiliated with OWASP, MITRE, NIST, ISO or any certification body. It uses their public material and credits it.
- **Companion courses** (link by name, not URL): *System Design for Vibe Coders*, *SaaS Building Blocks*, *Production AI Agents*, *AI Governance: Zero to Hero*, *AI Product Management: Zero to Hero*. Point to them in one line where they go deeper (e.g. governance law → the governance course) and stay on the security decision.

## The running case: Najm Bank's security team

**Najm Bank** is the fictional mid-sized Gulf bank (retail, SME and corporate lending; customers in Qatar, the UAE and the EU) used across the library. Say it is fictional in lesson 0.3. Here we sit in its **Application & AI Security** team.

Systems (use them consistently):
- **Najm Mobile** — the retail banking app (iOS/Android) and its **public API** (accounts, transfers, cards).
- **Najm Assist** — the LLM assistant in the app that is growing into an agent with tools (freeze a card, dispute a transaction, look up fees) — the main AI-security example.
- **Credit Memo Copilot** — an internal GenAI tool that drafts credit memos with retrieval (RAG) over internal documents — data-boundary and indirect-prompt-injection example.
- **SME Portal** — a web app for small-business customers (uploads invoices, multi-user companies with roles) — web, upload and access-control example.
- **Smart Alerts** — the fraud-detection ML model — model-evasion and data-poisoning example.
- The bank's **cloud platform** (containers on a managed Kubernetes service, an object store, a managed database, CI/CD pipelines) and its **AI coding agents** used by developers.

Cast:
- **Noura** — Head of Application & AI Security; the reader's mentor.
- **Ali** — a new security engineer (the reader's peer; makes the mistakes the reader should avoid).
- **Mariam** — red-team lead (authorised testing, AI red-teaming).
- **Jassim** — security operations (SOC) and incident response lead.
- **Tariq** — engineering lead; **Dana** — lead data scientist; **Rania** — Head of AI Products; **Layla** — Head of AI Governance; **Sara** — Data Protection Officer (DPO); **Hamad** — Chief Information Security Officer (CISO).

## Security life cycle phases (the lesson tag)

Every lesson is tagged with one or two phases, in English, in both languages: **Plan · Design · Build · Test · Deploy · Operate · Respond · Govern**. In the lesson header: `*Phase: Design*` or `*Phase: Build, Test*`.

## Module and lesson plan (numbers are fixed)

| Module | File | Lessons |
|---|---|---|
| 0 Orientation | 00-orientation.md | 0.1 What application and AI security is: assets, attackers and risk · 0.2 How breaches really happen: the attack chain and the usual suspects · 0.3 Meet Najm Bank's security team, and how to use this course |
| 1 Thinking like a defender | 01-foundations.md | 1.1 Threat modelling: data flows, trust boundaries and STRIDE · 1.2 Security principles: least privilege, defence in depth, secure defaults, zero trust · 1.3 Rating and prioritising risk: likelihood, impact and CVSS |
| 2 Web application security | 02-web.md | 2.1 Injection: SQL, command and template injection · 2.2 Browser attacks: XSS, CSRF, and the headers that stop them · 2.3 Server-side traps: SSRF, file uploads, path traversal and deserialisation |
| 3 Identity and access | 03-identity.md | 3.1 Authentication: passwords, MFA, passkeys and sessions · 3.2 OAuth 2.0, OpenID Connect and token pitfalls · 3.3 Authorisation: broken access control, IDOR and multi-tenancy |
| 4 APIs, mobile and abuse | 04-api-mobile.md | 4.1 The OWASP API Security Top 10 in practice · 4.2 Abuse, bots, rate limits and business-logic flaws · 4.3 Mobile app security: what you can and cannot trust on the device |
| 5 Data, cryptography and secrets | 05-data-crypto.md | 5.1 Cryptography for builders: TLS, hashing, encryption and keys · 5.2 Secrets management: keys, tokens and where they leak · 5.3 Protecting personal data: minimisation, logging and privacy engineering |
| 6 Secure development and supply chain | 06-sdlc.md | 6.1 A secure development life cycle: requirements, review and testing (SAST, DAST, SCA) · 6.2 The software supply chain: dependencies, SBOMs, SLSA and signing · 6.3 Securing AI-generated code: what coding agents get wrong |
| 7 Cloud and infrastructure | 07-cloud.md | 7.1 Cloud security: shared responsibility, IAM and misconfiguration · 7.2 Containers, Kubernetes and infrastructure as code · 7.3 Networks and the edge: segmentation, WAFs and DDoS |
| 8 How AI systems get attacked | 08-ai-threats.md | 8.1 The AI attack surface: OWASP Top 10 for LLM Applications and MITRE ATLAS · 8.2 Prompt injection and jailbreaks, direct and indirect · 8.3 Attacks on data and models: poisoning, evasion, extraction and inference |
| 9 Securing LLM apps and agents | 09-ai-defence.md | 9.1 Guardrails and output handling: never trust model output · 9.2 Agents and tools: excessive agency, least-privilege tools and MCP · 9.3 Securing retrieval (RAG): data boundaries and access control · 9.4 AI red-teaming and security evaluation |
| 10 Detection and response | 10-response.md | 10.1 Logging, monitoring and detection engineering · 10.2 Incident response: prepare, detect, contain, recover, learn · 10.3 Vulnerability management, disclosure and bug bounties |
| 11 Governance and leadership | 11-governance.md | 11.1 Frameworks: NIST CSF 2.0, ISO/IEC 27001, NIST SSDF and OWASP SAMM · 11.2 Regulation that touches security: GDPR, PDPPL, the EU AI Act and financial-sector rules · 11.3 Building a security programme and culture: champions, metrics and budgets |
| 12 Hero: capstone and practice exam | 12-capstone.md | 12.1 Capstone: secure Najm Assist from threat model to incident drill · 12.2 The security career: roles, certifications and portfolio · 12.3 Practice exam: 60 scenario questions |

Levels (zero → hero): 🟢 Beginner for Modules 0–1, 🟡 Intermediate for 2–7, 🔴 Advanced for 8–12 (use judgement per lesson).

## Facts to get right (and how to hedge)

State only what you are confident is true. Standards are revised: name the edition and say "at the time of writing (2026)" for anything that may have moved; tell readers to check the current version. Never invent CVE numbers, breach figures, fines, dates, quotes or statistics. Describe real incidents only as publicly reported, without unverified figures.

- **OWASP Top 10** — the 2021 edition (A01 Broken Access Control, A02 Cryptographic Failures, A03 Injection, A04 Insecure Design, A05 Security Misconfiguration, A06 Vulnerable and Outdated Components, A07 Identification and Authentication Failures, A08 Software and Data Integrity Failures, A09 Security Logging and Monitoring Failures, A10 SSRF). OWASP published a 2025 update; refer to categories by name and tell readers to check the current list rather than relying on numbering.
- **OWASP API Security Top 10 (2023):** API1 Broken Object Level Authorization (BOLA), API2 Broken Authentication, API3 Broken Object Property Level Authorization, API4 Unrestricted Resource Consumption, API5 Broken Function Level Authorization, API6 Unrestricted Access to Sensitive Business Flows, API7 SSRF, API8 Security Misconfiguration, API9 Improper Inventory Management, API10 Unsafe Consumption of APIs.
- **OWASP Top 10 for LLM Applications (2025 version):** LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Supply Chain, LLM04 Data and Model Poisoning, LLM05 Improper Output Handling, LLM06 Excessive Agency, LLM07 System Prompt Leakage, LLM08 Vector and Embedding Weaknesses, LLM09 Misinformation, LLM10 Unbounded Consumption. OWASP GenAI Security Project also publishes agentic-AI threat guidance — mention without inventing item numbers.
- **OWASP ASVS** (Application Security Verification Standard; version 5.0 released 2025), **MASVS/MASTG** for mobile, **OWASP SAMM**, **Cheat Sheet Series**.
- **MITRE ATT&CK** (adversary tactics and techniques), **MITRE ATLAS** (adversarial threats to AI systems), **CWE** and the CWE Top 25, **CVE**, **CVSS v4.0** (published Nov 2023; v3.1 still widely used), **EPSS**, **CISA KEV** catalogue.
- **NIST:** CSF 2.0 (Feb 2024; functions Govern, Identify, Protect, Detect, Respond, Recover); SP 800-218 SSDF; SP 800-63-4 digital identity guidelines (final 2025 — hedge); SP 800-61 Rev. 3 incident response (2025, aligned to CSF 2.0 — hedge); NIST AI 100-2 adversarial machine learning taxonomy; AI RMF 1.0 and the GenAI profile (AI 600-1).
- **Supply chain:** SBOM formats SPDX and CycloneDX; SLSA framework levels; Sigstore/cosign signing; dependency confusion and typosquatting; "slopsquatting" (package names hallucinated by AI tools and then registered by attackers) — described in research from 2024–2025, hedge numbers.
- **Identity:** OAuth 2.0 (RFC 6749), PKCE (RFC 7636), OAuth 2.0 Security Best Current Practice (RFC 9700, 2025), OpenID Connect, JWT (RFC 7519) pitfalls (`alg: none`, algorithm confusion, no expiry, secrets in payload), WebAuthn/passkeys (FIDO2), session fixation, credential stuffing.
- **Crypto:** TLS 1.3 (RFC 8446); password hashing with Argon2id, scrypt or bcrypt (never plain fast hashes); AES-GCM; envelope encryption with a KMS; never roll your own crypto; post-quantum migration exists as a planning topic (NIST FIPS 203/204/205 published Aug 2024) — one paragraph at most.
- **Cloud/Kubernetes:** shared responsibility model; IAM least privilege; public storage buckets; instance metadata endpoints and SSRF (cloud metadata services, IMDSv2 as a mitigation on AWS); Kubernetes RBAC, network policies, Pod Security Standards; CIS Benchmarks; infrastructure-as-code scanning.
- **AI-specific:** direct vs indirect prompt injection (Greshake et al., 2023, "Not what you've signed up for"); jailbreaks; no complete technical fix for prompt injection exists at the time of writing — defend with architecture (least privilege, isolation, human approval for consequential actions, output handling); data poisoning; model extraction; membership inference; adversarial examples / evasion; training-data extraction (Carlini et al.); MCP (Model Context Protocol, introduced by Anthropic Nov 2024) and tool poisoning / confused-deputy risks; "lethal trifecta" framing (private data + untrusted content + external communication, Simon Willison, 2025) — credit it.
- **Regulation (one line each, hedge, point to the governance course):** GDPR Art. 32 (security of processing) and Arts. 33–34 (breach notification, 72 hours to the authority where feasible); Qatar PDPPL (Law No. 13 of 2016); Qatar's National Cyber Security Agency (NCSA) and its national information assurance standards — describe without inventing clause numbers; QCB's cybersecurity and AI expectations for banks — no invented clause numbers; EU AI Act Art. 15 (accuracy, robustness and cybersecurity of high-risk AI); EU DORA (digital operational resilience for financial entities, applies from Jan 2025); NIS2. PCI DSS v4.0 for card data.

Real cases you may use (well documented only; hedge figures):
- Equifax 2017 breach via an unpatched Apache Struts vulnerability (CVE-2017-5638).
- Capital One 2019 breach involving SSRF and a cloud metadata service / over-privileged role.
- SolarWinds Orion build-system compromise (disclosed Dec 2020) — supply chain.
- Log4Shell (CVE-2021-44228, Dec 2021) — dependency risk and SBOMs.
- The xz Utils backdoor (CVE-2024-3094, Mar 2024) — maintainer social engineering, caught before wide release.
- MOVEit Transfer SQL injection exploited at scale (2023).
- Optus (2022) exposure reported to involve an unauthenticated API — BOLA/inventory lesson; hedge details.
- Samsung staff pasting confidential code into a public chatbot (2023) — data leakage via AI tools.
- Bing Chat / "Sydney" system prompt leak via prompt injection (Feb 2023).
- Chevrolet dealer chatbot "selling" a car for $1 (Dec 2023); Air Canada chatbot (*Moffatt v. Air Canada*, 2024) — reliability and liability of AI output.
- Indirect prompt injection demonstrations against email/document-reading assistants (research 2023–2025) — describe the pattern, not a specific unverified exploit.

## File format (the build parses this — follow exactly)

```
# Module 2 — Web application security

*One-paragraph italic module intro: what the module covers and why, tied to Najm Bank.*

> **Phases:** Build, Test — …(one line in the course's words)

---

# 2.1 — Injection: SQL, command and template injection
*Level: 🟡 Intermediate* · *Prerequisites: 1.1, 1.2* · *Phase: Build, Test*

## ⚡ In 60 seconds
- 4–6 bullets: what it is, the rule that matters most, the decision cue, the biggest trap.

## 🧭 Why it matters
A Najm Bank scenario (or a real public case) that makes the topic unavoidable. 1–3 paragraphs.

## 📐 How it works
### 🟢 The essentials
### 🟡 Going deeper
### 🔴 Expert view
(Plain explanations first; define every term on first use; short code snippets in fenced blocks where they help — vulnerable vs fixed side by side; tables; one mermaid diagram where it genuinely helps. Mermaid: flowchart or sequence only, `flowchart LR` or `TD`, short labels in double quotes, no parentheses inside labels.)

## 🧰 The toolkit
| Control, standard or tool | What it is and does | When to reach for it |
|---|---|---|
| **Parameterised queries** | … | … |
(3–8 rows. The first cell MUST start with the name in bold — e.g. **STRIDE**, **OWASP ASVS**, **Content Security Policy**, **Passkeys**, **SBOM**, **Semgrep**, **Least-privilege tools** — optionally followed by a short credit in parentheses. Keep bold names identical wherever the same item appears; they build the toolkit catalogue.)

## 🏛️ In practice at Najm Bank
The security artefact this lesson produces: a threat model excerpt, a secure-coding rule, an access-control matrix, a review checklist, a detection rule, an incident runbook, a red-team scope, a policy clause. Concrete, reusable, in a table or a short template.

## 🛠️ Exercises
Three graded exercises: 🟢 …, 🟡 …, 🔴 …, each with a "*Done when:*" line. Hands-on exercises run only against your own code, a local lab, or deliberately vulnerable training apps (e.g. OWASP Juice Shop) — say so.

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
Official and primary sources only (owasp.org, genai.owasp.org, attack.mitre.org, atlas.mitre.org, nist.gov / csrc.nist.gov, cwe.mitre.org, first.org for CVSS, cisa.gov, rfc-editor.org, slsa.dev, eur-lex.europa.eu, arxiv.org for papers). Plain links; no invented URLs — link to a top-level page if unsure of the deep link.
```

- Separate lessons with a `---` line.
- Lesson 12.3 (practice exam) follows the same outer format but its body is: ⚡ (how to take it), then `## ✍️ Practice exam` with 60 questions numbered 1–60 in the same Q/A format, spread across the phases and modules, each answer ending with its phase and the lesson to review, e.g. *(Build · 2.1)*; then 🧾 and 📚. Its 🧰/🏛️/🛠️/⚠️ sections may be short.

## Style

- Plain, direct English; short sentences; define jargon on first use; no hype, no fear-mongering, no filler. Explain *why*, not just *what*.
- Defender's judgement over trivia: every lesson must leave the reader able to make a security decision or produce an artefact.
- Code snippets: short, language-neutral where possible (Python, JavaScript/TypeScript or SQL), always showing the safe version.
- Lengths: 2,000–3,500 words per lesson (12.3 excepted). Every lesson's five questions must be answerable from that lesson.
- Use the running cast consistently.
