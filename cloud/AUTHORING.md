# Cloud & DevOps: Zero to Hero — authoring guide

This is the contract every lesson follows. It is not published.

## What the course is

A free, bilingual (English/Arabic) course that takes a reader from zero to "hero" in **getting software to production and keeping it healthy there**: Linux, networking and cloud fundamentals, identity and access, containers and Kubernetes, infrastructure as code and GitOps, CI/CD and safe releases, observability, SLOs and on-call, incidents, scaling and disaster recovery, cloud cost (FinOps), and running AI workloads.

- **Audience:** computer engineering, CS and data graduates aiming at cloud, platform, DevOps or site-reliability (SRE) roles; developers who want to own what they ship; GCC bank, government and enterprise staff moving systems to the cloud. Basic programming and command-line comfort help; nothing else assumed.
- **Cloud-neutral, hands-on, free to practise.** Teach concepts that transfer across **AWS, Microsoft Azure and Google Cloud**; show equivalents in a small table where useful; never claim one is best. Exercises run locally or on free tiers: **Docker**, **kind** or **k3d/minikube** (local Kubernetes), **OpenTofu or Terraform** against local providers or a free-tier account (with a budget alert set first), **GitHub Actions**, **Prometheus**, **Grafana**, **OpenTelemetry**, **Argo CD**. Never invent prices, quotas, SLAs or limits — tell readers to check the provider's current page.
- **Engineering judgement over tool tours:** every lesson leaves the reader able to make an operational decision (release this way, alert on this, size this, roll back now) or produce an artefact.
- **Companion courses** (relative links; catalogue in `LIBRARY.md`): *System Design for Vibe Coders* (Module 4 deploys, 7 observability, 10 scaling, 11 reaching the world — the non-coder view), *SaaS Building Blocks* (7.2 observability, 7.4 deployment and environments), *Secure AI & Application Security* (7.1 cloud security, 7.2 containers/Kubernetes/IaC security, 6.2 supply chain, 5.2 secrets), *Running AI Agents in Production* (operating agents), *Data Engineering & Analytics* (being written now: link by module), *From Graduate to Hired* (being written now: 2.4 is the cloud/platform role path). Point to them in one line where they go deeper — especially security — and stay on the operations decision here.

## The running case: Najm Bank's Platform Engineering team

**Najm Bank** is the fictional mid-sized Gulf bank (Qatar, the UAE and the EU) used across the library. Say it is fictional in lesson 0.3. Here we sit in its **Platform Engineering & SRE** team, moving services from a data centre to a managed cloud and building an internal developer platform.

Systems (use consistently):
- **Najm Mobile API** — the public API behind the retail app (containers on a managed Kubernetes service; PostgreSQL managed database; object storage; a CDN and WAF at the edge).
- **Payments service** — must not lose or duplicate a transfer; strict uptime and recovery targets.
- **Najm Assist** — the LLM assistant: an **LLM gateway** calling hosted model APIs and a small self-hosted model on GPUs.
- **The internal developer platform** — golden-path templates, CI/CD pipelines, a GitOps repo, observability stack, cost dashboards.
- The legacy **data-centre core banking** system that stays on-premises (hybrid connectivity).

Cast:
- **Salem** — Head of Platform Engineering; the reader's mentor.
- **Yousef** — new graduate platform engineer (computer-engineering degree; the reader's peer; makes the mistakes the reader should avoid).
- **Maha** — SRE lead (SLOs, on-call, incidents).
- **Tariq** — engineering lead for the app teams (also in the security course).
- **Noura** — Head of Application & AI Security (from the security course); **Jassim** — SOC and incident response lead; **Hamad** — CISO; **Mona** — FinOps analyst in Finance.

## Phases (the lesson tag)

Every lesson is tagged with one or two phases of the delivery loop, in English, in both languages: **Plan · Code · Build · Test · Release · Deploy · Operate · Monitor**. Header: `*Phase: Deploy*` or `*Phase: Operate, Monitor*`.

## Module and lesson plan (numbers are fixed)

| Module | File | Lessons |
|---|---|---|
| 0 Orientation | 00-orientation.md | 0.1 What cloud, DevOps, platform engineering and SRE are · 0.2 The path to production: from a commit to a customer, and everything that can break on the way · 0.3 Meet Najm Bank's platform team, and how to use this course |
| 1 Foundations | 01-foundations.md | 1.1 Linux, the shell and networking essentials: processes, files, ports, DNS, HTTP and TLS · 1.2 Cloud fundamentals: regions, zones, compute, storage, managed services and shared responsibility · 1.3 Identity and access in the cloud: users, roles, policies and workload identity |
| 2 Containers and Kubernetes | 02-containers.md | 2.1 Containers done right: images, layers, Dockerfiles and registries · 2.2 Kubernetes fundamentals: pods, deployments, services and how the cluster thinks · 2.3 Kubernetes in practice: config, secrets, health probes, autoscaling and Helm |
| 3 Infrastructure as code | 03-iac.md | 3.1 Infrastructure as code with Terraform/OpenTofu: state, modules and plans · 3.2 Environments and GitOps: promoting changes from dev to production · 3.3 Policy as code, drift and guardrails |
| 4 CI/CD and safe releases | 04-cicd.md | 4.1 Continuous integration: pipelines, tests, artefacts and fast feedback · 4.2 Release strategies: rolling, blue-green, canary, feature flags and rollback · 4.3 Securing the pipeline: secrets, signed artefacts and least-privilege deploys |
| 5 Observability and reliability | 05-observability.md | 5.1 Telemetry: logs, metrics, traces and OpenTelemetry · 5.2 SLOs, error budgets, alerting and on-call that people can sustain · 5.3 Incidents and blameless postmortems |
| 6 Scale, cost and AI infrastructure | 06-scale.md | 6.1 Scaling and resilience: autoscaling, multi-zone, backups and disaster recovery · 6.2 FinOps: understanding, allocating and cutting cloud cost · 6.3 Running AI workloads: GPUs, model serving, LLM gateways and their cost |
| 7 Hero: capstone and practice exam | 07-capstone.md | 7.1 Capstone: take a new Najm service from empty repo to production with an SLO · 7.2 The cloud career: roles, certifications, interviews and a portfolio · 7.3 Practice exam: 60 scenario questions |

Levels: 🟢 Beginner for Modules 0–1, 🟡 Intermediate for 2–5, 🔴 Advanced for 6–7 (use judgement per lesson).

## Facts to get right (and how to hedge)

State only what you are confident is true; name versions; hedge anything that changes "at the time of writing (2026)"; never invent prices, quotas, SLAs, statistics, quotes or dates.
- **DevOps & SRE:** DORA's four key metrics (deployment frequency, lead time for changes, change failure rate, time to restore service — DORA later added a reliability measure and refined names; hedge); *Accelerate* (Forsgren, Humble, Kim, 2018); Google's *Site Reliability Engineering* (2016) and *The Site Reliability Workbook* (2018): SLIs, SLOs, error budgets, toil, blameless postmortems; the Twelve-Factor App; platform engineering and internal developer platforms (CNCF platforms white paper — hedge; Backstage as an open-source portal).
- **Linux & networking:** processes, signals, file permissions, systemd basics; TCP/UDP, ports, DNS record types (A, AAAA, CNAME, TXT), TTLs; HTTP status classes; TLS 1.3 (RFC 8446); private vs public subnets, NAT, load balancers (L4 vs L7).
- **Cloud:** regions and availability zones; IaaS/PaaS/SaaS/serverless; the shared responsibility model; object vs block vs file storage; managed databases; IAM principals, roles, policies, least privilege; workload identity / OIDC federation for CI (no long-lived keys); cloud equivalents (AWS EC2/EKS/S3/IAM, Azure VMs/AKS/Blob Storage/Entra ID, Google Compute Engine/GKE/Cloud Storage/IAM). Well-Architected frameworks exist for all three providers (one line).
- **Containers & Kubernetes:** OCI image spec; layers and caching; multi-stage builds; non-root users; image digests vs tags; registries; Kubernetes objects (Pod, Deployment, ReplicaSet, Service, Ingress/Gateway API, ConfigMap, Secret, Namespace), requests/limits, liveness/readiness/startup probes, Horizontal Pod Autoscaler, rolling updates; Helm charts; Kubernetes Secrets are base64-encoded, not encrypted by default (enable encryption at rest, or use an external secrets manager).
- **IaC & GitOps:** Terraform (HashiCorp; licence changed to BSL in Aug 2023) and **OpenTofu** (the open-source fork under the Linux Foundation); state files, remote state and locking, plan/apply, modules, drift; Pulumi and cloud-native templates (CloudFormation, Bicep) exist; GitOps principles (OpenGitOps): declarative, versioned, pulled automatically, continuously reconciled; Argo CD and Flux (CNCF graduated projects); policy as code with Open Policy Agent (OPA)/Conftest, Kyverno; Checkov/tfsec-style scanners (hedge names, point to *Secure AI* 7.2).
- **CI/CD:** trunk-based development; build once, promote the same artefact; caching; test pyramid; GitHub Actions/GitLab CI/Jenkins as examples; deployment strategies (recreate, rolling, blue-green, canary, shadow), feature flags (OpenFeature), automated rollback on SLO burn; SLSA, Sigstore/cosign signing, SBOMs (point to *Secure AI* 6.2).
- **Observability:** the three signals plus profiles; OpenTelemetry (CNCF) for traces/metrics/logs; Prometheus (pull model, PromQL) and Grafana; RED (rate, errors, duration) and USE (utilisation, saturation, errors) methods; Google's four golden signals; multi-window, multi-burn-rate SLO alerts (SRE Workbook); alert fatigue.
- **Incidents & resilience:** incident roles (incident commander, communications, operations); severity levels; blameless postmortems; RTO and RPO; backup testing; multi-AZ vs multi-region; chaos engineering (start small, in non-production first).
- **FinOps:** FinOps Foundation framework (Inform, Optimise, Operate phases); tagging and cost allocation; rightsizing; autoscaling; reserved capacity/savings plans and spot/preemptible instances (concepts, no prices); unit cost (cost per transaction); egress costs exist — check pricing pages.
- **AI infrastructure:** GPUs and their scarcity/cost (no prices); model serving (e.g. vLLM, NVIDIA Triton, KServe as examples); batching, quantisation, KV cache (concepts); LLM gateways (routing, rate limits, caching, fallbacks, cost tracking); token-based cost; managed model APIs vs self-hosting trade-offs; point to *Running AI Agents in Production* for agent operations.
- **Regulation (one line each, hedge, point to the governance and security courses):** cloud outsourcing and data residency expectations from GCC financial regulators (e.g. Qatar Central Bank; no invented clause numbers); EU DORA (digital operational resilience for financial entities, applies from Jan 2025) — ICT risk, incident reporting, resilience testing, third-party (cloud) risk.

Real cases you may use (well documented only; hedge figures): GitLab's 2017 database deletion and backup failures (public postmortem); the AWS us-east-1 S3 outage of Feb 2017 caused by a mistyped command (public summary); the Facebook/Meta outage of Oct 2021 (BGP/DNS, public engineering post); the CrowdStrike Falcon content update of July 2024 that crashed Windows hosts (staged rollout lesson); Knight Capital 2012 (deployment to a server with old code — SEC order).

## File format (the build parses this — follow exactly)

```
# Module 2 — Containers and Kubernetes

*One-paragraph italic module intro: what the module covers and why, tied to Najm Bank.*

> **Phases:** Build, Deploy — …(one line in the course's words)

---

# 2.1 — Containers done right: images, layers, Dockerfiles and registries
*Level: 🟡 Intermediate* · *Prerequisites: 1.1, 1.2* · *Phase: Build, Deploy*

## ⚡ In 60 seconds
- 4–6 bullets: what it is, the rule that matters most, the decision cue, the biggest trap.

## 🧭 Why it matters
A Najm Bank scenario (or a well-documented public incident) that makes the topic unavoidable. 1–3 paragraphs.

## 📐 How it works
### 🟢 The essentials
### 🟡 Going deeper
### 🔴 Expert view
(Plain explanations first; define every term on first use; short correct snippets (shell, Dockerfile, Kubernetes YAML, HCL, GitHub Actions YAML, PromQL) in fenced blocks — risky vs hardened side by side where it helps; tables; one mermaid diagram where it genuinely helps. Mermaid: flowchart or sequence only, `flowchart LR` or `TD`, short labels in double quotes, no parentheses inside labels.)

## 🧰 The toolkit
| Tool, practice or service | What it is and does | When to reach for it |
|---|---|---|
| **Multi-stage build** | … | … |
(3–8 rows. The first cell MUST start with the name in bold — e.g. **Docker**, **Helm**, **OpenTofu**, **Argo CD**, **Canary release**, **OpenTelemetry**, **Error budget** — optionally followed by a short credit in parentheses. Keep bold names identical wherever the same item appears; they build the toolkit catalogue.)

## 🏛️ In practice at Najm Bank
The artefact this lesson produces: an architecture note, a hardened Dockerfile, a deployment manifest, an IaC module interface, a pipeline definition, a release checklist, an SLO document, an alert rule, an incident runbook, a postmortem, a DR test plan, a cost report. Concrete, reusable, in a table or a short template.

## 🛠️ Exercises
Three graded exercises: 🟢 …, 🟡 …, 🔴 …, each with a "*Done when:*" line. Exercises run locally (Docker, kind/k3d, OpenTofu with local providers) or on a free-tier account with a budget alert set first — never on an employer's account without permission.

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
Official docs and primary sources only (kubernetes.io, docs.docker.com, opentofu.org, developer.hashicorp.com, argo-cd.readthedocs.io, fluxcd.io, opentelemetry.io, prometheus.io, grafana.com/docs, sre.google, dora.dev, finops.org, cncf.io, docs.github.com, the providers' documentation sites, rfc-editor.org, eur-lex.europa.eu). Plain links; no invented URLs — link to a top-level page if unsure of the deep link.
```

- Separate lessons with a `---` line.
- Lesson 7.3 (practice exam) follows the same outer format but its body is: ⚡ (how to take it), then `## ✍️ Practice exam` with 60 questions numbered 1–60 in the same Q/A format, spread across the phases and modules, each answer ending with its phase and the lesson to review, e.g. *(Deploy · 4.2)*; then 🧾 and 📚. Its 🧰/🏛️/🛠️/⚠️ sections may be short.

## Style

- Plain, direct English; short sentences; define jargon on first use; no hype, no filler. Explain *why*, not just *what*.
- Snippets: short, correct and safe by default (pinned versions or digests, non-root, least privilege, no secrets in code).
- Lengths: 2,000–3,500 words per lesson (7.3 excepted). Every lesson's five questions must be answerable from that lesson.
- Use the running cast consistently. Do not start any non-quiz line with `**N.` (bold number + dot).
