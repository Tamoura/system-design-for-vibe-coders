# SaaS Building Blocks

**Every SaaS is the same app wearing a different product. Learn the ~25 components
they all share — once — from the best open-source code there is.**

## What this is

A written course for **junior developers** who can build a CRUD app but have never
shipped or run a real SaaS. Open ten successful SaaS products — a scheduling tool,
a CRM, a link shortener, an error tracker — and you will find the same machinery in
every one of them: sign-up and login, organizations and invitations, roles, a
billing page, transactional email, background jobs, an API with keys, outbound
webhooks, an audit log, an admin panel, SSO for the big customers. The part the
customer actually pays for is often a small fraction of the code.

That is good news. It means the fastest way to become useful on any SaaS team is to
learn those shared components well, and to know where the best implementations
already live. This course does both:

- **One component per lesson**, taught from first principles and climbing from the
  basics to what senior engineers worry about at scale.
- **The best repos for each component** — the libraries and self-hostable services
  you would adopt, *and* the production open-source SaaS codebases (Cal.com,
  Documenso, Dub, Twenty, Plane, PostHog, Sentry, GitLab, Chatwoot, Infisical…)
  where you can read the component working for real.
- **One product built across the whole course**: **Beacon**, uptime monitoring and
  public status pages for teams — chosen because it needs every component.

## How every lesson works

Each lesson has the same eight parts, so you always know where you are:

| Part | What you get |
|---|---|
| 🧭 **Why every SaaS has this** | The scenario at Beacon (or a real public case) that makes the component unavoidable. |
| 📐 **How it works** | The concepts, climbing a ladder: 🟢 *The essentials* → 🟡 *Going deeper* → 🔴 *At scale / enterprise*. |
| 🏆 **The best repos** | A comparison table of the best open-source options, the one to study first, and a buy / self-host / build verdict. |
| 🔍 **Study it in the wild** | Where real production SaaS codebases implement it, how to find the code, and what to notice. |
| 🛠️ **Build it into Beacon** | Three graded exercises — 🟢 beginner, 🟡 intermediate, 🔴 advanced — each with "done when" criteria. |
| ⚠️ **Mistakes juniors make** | The traps, and what to do instead. |
| 🧾 **Recap** | The takeaways worth remembering. |
| 📚 **References** | Specs, official docs and the repos' own documentation. |

## Learning paths

Every lesson carries a level badge showing where it *starts*: 🟢 Beginner,
🟡 Intermediate or 🔴 Advanced. Pick the track that matches you.

### 🟢 Beginner track — "ship a SaaS v1" (≈ 4 weeks)

Read Module 0, then lessons 1.1, 1.2, 2.1, 2.2, 3.1, 4.1 and 6.1. Do the 🟢
exercise in each. At the end you have a Beacon that people can sign up to, create
a workspace in, invite teammates to, pay for, and receive email from.

### 🟡 Intermediate track — "survive real customers" (≈ 5 weeks)

Lessons 1.3, 2.3, 3.2, 4.2, 5.1, 5.2, 5.3, 6.2, 6.3, 7.1, 7.2 and 7.3 — plus the 🟡
exercises in the Beginner lessons you already read. This is the layer that separates
a demo from a product: permissions, background jobs, a public API, webhooks,
analytics, feature flags, an admin panel, observability and an audit log.

### 🔴 Advanced track — "win enterprise deals and scale" (≈ 4 weeks)

Lessons 1.4, 2.4, 3.3, 4.3, 5.4, 7.4, 8.1 and 8.2, the 🔴 exercises everywhere, and
the capstone (9.1). SSO and SCIM, tenant isolation, usage-based billing, realtime
collaboration, durable workflows, self-hosting, compliance and AI features.

### A 12-week plan for a junior cohort

| Week | Read | Do |
|---|---|---|
| 1 | 0.1, 0.2, 0.3 | Run one reference SaaS locally; map its components. |
| 2 | 1.1, 1.2 | Beacon sign-up, login, organizations, invitations. |
| 3 | 2.1, 2.2 | Schema, migrations, seeds; status-page logo upload. |
| 4 | 3.1, 4.1 | Stripe checkout + webhooks; verification and invite emails. |
| 5 | 6.1, 1.3 | App shell, onboarding, settings; roles and permission checks. |
| 6 | 5.1 | The monitor-check scheduler and workers. |
| 7 | 3.2, 4.2 | Plan limits; incident notifications with preferences. |
| 8 | 5.2, 5.3 | Public API with keys and rate limits; outbound webhooks and Slack. |
| 9 | 6.2, 6.3, 2.3 | Analytics events, a feature flag rollout, search. |
| 10 | 7.1, 7.2, 7.3 | Admin panel, observability, audit log. |
| 11 | pick 3 from Module 1.4–8.2 | One 🔴 exercise each. |
| 12 | 9.1 | Capstone review: present Beacon's architecture and build-vs-buy choices. |

Mentors: have juniors present the "🔍 Study it in the wild" findings to each other.
Reading real code and explaining it out loud is the skill this course is really
teaching.

## What you need

- Comfort with one web stack (the examples use TypeScript, Next.js and PostgreSQL,
  and each lesson names the Django, Rails, Laravel and Go equivalents).
- Git, Docker, and a GitHub account for reading and running the reference repos.
- No prior SaaS experience. Terms are defined the first time they appear.

## A note on the repos

The course names roughly two hundred repositories. They were chosen because they
are widely used, actively maintained, or unusually readable — not because anyone
paid for a mention. Two cautions:

- **Licenses change.** Several well-known projects have moved between MIT/Apache,
  AGPL, and source-available licenses (FSL, BSL, ELv2, "fair-code") in recent
  years. Lesson 0.3 explains what each means for you. Always read the repo's
  `LICENSE` before you copy code or self-host commercially.
- **Projects move.** Repos get renamed, archived or acquired. The full list lives in
  the [repo catalog](./REPOS.md); run `npm run saas:repos` to check every link.

## Where to go next

Open the [course map](./OUTLINE.md) or start with lesson 0.1.
