# Lesson-Authoring Spec — SaaS Building Blocks

Read this fully before writing a lesson for **SaaS Building Blocks**. It is the
contract every lesson follows so the course reads as one voice and the build
script can render it.

## What this course is

A written course for **junior developers** (0–3 years; they can code, they have
built CRUD apps and tutorials, they have never shipped or maintained a real SaaS).
Its thesis:

> **Almost every SaaS is the same ~25 components wearing a different product.**
> The product-specific part — the thing customers actually pay for — is usually
> 10–20% of the code. The rest is auth, organizations, billing, email, jobs,
> permissions, webhooks, audit logs… Learn those components once, learn where
> the best open-source implementations live, and every new SaaS gets faster.

Every lesson teaches one component **from beginner to advanced**, and points at
**the best open-source repositories** — both the libraries/services you would
adopt *and* the production SaaS codebases where you can watch the component
working in real life.

## The running example: Beacon

Every lesson applies the component to **Beacon**, a fictional B2B SaaS: *uptime
monitoring and public status pages for teams.* It was chosen because it needs every
component in the course:

- Users sign up, create an **organization** (workspace), invite teammates with roles.
- They add **monitors** (an HTTP check every 30s–5min → background jobs + scheduling).
- A **public status page** per org, optionally on a custom domain.
- When a monitor fails, Beacon opens an **incident** and **notifies** the team
  (email, Slack, SMS, in-app) and emails status-page **subscribers**.
- Plans: **Free** (5 monitors, 5-min checks), **Pro** ($29/mo, 50 monitors, 1-min
  checks, SMS credits), **Business** ($199/mo, SSO, audit log, 30s checks, API);
  SMS beyond the included credits is **usage-billed**.
- A **public REST API** with API keys, **outbound webhooks** on incident events,
  a Slack integration, an **audit log**, **SSO/SCIM** for enterprise, an internal
  **admin panel**, a **realtime** dashboard, and an AI "incident summary" feature.

Default stack for examples (not dogma — lessons mention equivalents): TypeScript,
Next.js (or any web framework), PostgreSQL, Redis, S3-compatible storage, Stripe.
When a lesson shows code, keep it short (≤ 30 lines per block) and readable by a
junior; mention the Python/Django, Ruby/Rails, Go, PHP/Laravel equivalents in prose
where natural — juniors come from many stacks.

## File layout and headings (the build depends on these)

Each module is ONE file: `saas/modules/NN-slug.md`.

- First line: `# Module N — Title`, then a 2–4 sentence italic intro paragraph, then `---`.
- Each lesson starts with `# N.M — Title` (em dash, spaces around it).
- The line right after a lesson heading is the **level line**, exactly one of:
  `*Level: 🟢 Beginner*` · `*Level: 🟡 Intermediate*` · `*Level: 🔴 Advanced*`
  optionally followed by ` · *Prerequisites: 1.1, 2.1*`.
- Separate lessons with a blank line, `---`, blank line.
- The last lesson ends with a one-line pointer to the next module.

## The lesson anatomy (EVERY lesson, in this order, EXACT headings)

1. `## 🧭 Why every SaaS has this` — open with a concrete scenario at Beacon (or a
   well-known real public incident/case — only ones you are sure happened, e.g.
   GitHub's 2012 mass-assignment incident, the Okta/Auth0 or Heroku OAuth token
   incidents, Stripe webhook retries, Slack's multi-tenant data leak bug class).
   What breaks, or what customers demand, without this component. 2–4 short
   paragraphs. Land the core idea in **one bold sentence**.

2. `## 📐 How it works` — first principles, terms defined before use. Must include
   **at least one Mermaid diagram** and at least one Markdown table. Structure the
   depth ladder with these exact sub-headings:
   - `### 🟢 The essentials` — what a beginner must understand to ship v1.
   - `### 🟡 Going deeper` — what changes once you have real customers.
   - `### 🔴 At scale / enterprise` — what senior engineers worry about.
   (Every lesson has all three, even Beginner-level ones — the level line says where
   the lesson *starts*, the ladder shows where it *goes*.)

3. `## 🏆 The best repos` — a Markdown table with columns exactly:
   `| Repo | What it is | Stack | License | Pick it when |`
   Repo cell format: `[owner/name](https://github.com/owner/name)`. 5–10 rows.
   Then a short paragraph **"If you only study one:"** naming one repo and why.
   Then **"Buy, build, or self-host?"** — 3 bullets: when to use a managed service
   (name the well-known ones, e.g. Clerk, WorkOS, Stripe, Resend, Algolia),
   when to self-host an OSS option, when to build it yourself.

4. `## 🔍 Study it in the wild` — 2–4 production open-source SaaS codebases that
   implement this component (from the reference shelf below). For each: what it
   does well, and **how to find the code** — prefer search instructions ("open the
   repo, press `t`/use code search for `stripe` and `webhook`; start from the
   Prisma schema's `Membership` model") over deep file paths. Only give a concrete
   path if you are highly confident it exists (top-level folders like `apps/web`,
   `packages/prisma` in Cal.com/Documenso/Dub monorepos are fine), and say
   "at the time of writing". End with a **"What to notice"** bullet list of 3–5
   design decisions the reader should look for.

5. `## 🛠️ Build it into Beacon` — three graded exercises with these exact sub-headings:
   `### 🟢 Beginner exercise`, `### 🟡 Intermediate exercise`, `### 🔴 Advanced exercise`.
   Each: the task in 2–5 sentences, then **Done when:** followed by 2–4 checkable
   acceptance criteria as a bullet list. Optional short code sketch (≤ 30 lines).

6. `## ⚠️ Mistakes juniors make` — 4–7 bullets, each **bold mistake** — then why it
   hurts and what to do instead. Concrete, not generic.

7. `## 🧾 Recap` — 4–6 bullets, the memorable takeaways.

8. `## 📚 References` — 4–8 bullets of real, checkable sources: official docs,
   RFCs/specs (OAuth 2.0 RFC 6749, OIDC Core, SAML 2.0, SCIM RFC 7643/7644,
   Standard Webhooks spec, OWASP cheat sheets), well-known engineering blog posts
   you are sure exist, and the repos' own docs. **Never invent URLs.** If you are not
   sure of an exact deep URL, link the docs root (e.g. `https://docs.stripe.com`).

## Voice

A senior engineer mentoring a junior they like. Direct, concrete, a little dry.
Short paragraphs. No hype, no "in today's fast-paced world", no emoji outside the
headings. Define every term on first use. Explain *why* before *how*. Be honest
about trade-offs; say "it depends" only when followed by exactly what it depends on.

Length: **2,000–3,200 words per lesson.** Dense beats long.

## Mermaid rules (the build pre-renders with Mermaid 11 and fails on errors)

- Use `flowchart LR/TD`, `sequenceDiagram`, `erDiagram`, `stateDiagram-v2`.
- Quote every node label that contains spaces or punctuation: `A["Web app (Next.js)"]`.
- No parentheses/brackets/colons unquoted in labels; no HTML except `<br/>`.
- In sequenceDiagram messages avoid semicolons and `#`. Keep diagrams ≤ 15 nodes.
- erDiagram attribute types must be single words (`string`, `uuid`, `int`, `timestamp`).

## Accuracy rules (critical — juniors will click everything)

- **Only recommend repos you are certain exist at that exact `owner/name`.**
  When in doubt, leave it out. Prefer the canonical list below.
- Licenses change (several projects moved to AGPL/FSL/ELv2 in recent years).
  Give the license you are confident of; the course README carries a
  "verify licenses before adopting" note, so do not hedge in every row.
- Do not claim star counts, funding, or version numbers.
- Do not invent incidents, quotes, or benchmarks.

### Known facts (as of mid-2026) — use these, don't contradict them

- **Lucia** (`lucia-auth/lucia`) was deprecated as a library in 2025 and is now a
  learning resource on implementing sessions yourself — recommend it *as reading*.
- **Auth.js** (`nextauthjs/next-auth`) — in 2025 its maintenance moved under the
  Better Auth team; Better Auth (`better-auth/better-auth`) is the recommended
  path for new TypeScript projects.
- **BoxyHQ SAML Jackson** (`boxyhq/jackson`) was acquired by Ory in 2025 and
  continues as **Ory Polis**; mention both names.
- **MinIO** (`minio/minio`) moved its community edition toward source-only /
  maintenance in 2025; mention **Garage** (Deuxfleurs, hosted on their own Gitea,
  not GitHub — link `https://garagehq.deuxfleurs.fr`) and **SeaweedFS**
  (`seaweedfs/seaweedfs`) as alternatives.
- **Zitadel** relicensed to AGPL-3.0 in 2025. **Sentry** uses the FSL (Functional
  Source License). **n8n** uses the Sustainable Use License (fair-code, not OSI).
- **Permify** was acquired by FusionAuth in 2025; the repo `Permify/permify` remains.
- **Cal.com** is now MIT-licensed with no `ee` folder (it used to be AGPL + commercial `ee`).
  For the open-core pattern, point at PostHog, Infisical or Sentry's history instead.
- **Unleash** core is AGPL-3.0; **imgproxy** is Apache-2.0; **Flipt** uses the Fair Core
  License (FCL-1.0-MIT); **Directus** uses the Monospace Sustainable Core License.
- Verify every license cell against the repo's LICENSE file before merging a lesson.
- **HyperDX** was acquired by ClickHouse (part of ClickStack); `hyperdxio/hyperdx`.

### Canonical repos by component (safe to use; add others only if certain)

- Auth: better-auth/better-auth, nextauthjs/next-auth, lucia-auth/lucia,
  supabase/auth, keycloak/keycloak, ory/kratos, ory/hydra, zitadel/zitadel,
  logto-io/logto, supertokens/supertokens-core, goauthentik/authentik,
  pocketbase/pocketbase, django/django (contrib.auth), heartcombo/devise,
  pennersr/django-allauth, panva/openid-client, panva/jose.
- AuthZ: casbin/casbin, stalniy/casl, openfga/openfga, authzed/spicedb,
  cerbos/cerbos, Permify/permify, osohq/oso (library deprecated; Oso Cloud),
  open-policy-agent/opa, ory/keto.
- SSO/SCIM: boxyhq/jackson, keycloak/keycloak, zitadel/zitadel, goauthentik/authentik.
- DB/ORM/migrations: prisma/prisma, drizzle-team/drizzle-orm, kysely-org/kysely,
  supabase/supabase, neondatabase/neon, postgres/postgres, citusdata/citus,
  pgvector/pgvector, sqlc-dev/sqlc, golang-migrate/migrate, flyway/flyway,
  sqitchers/sqitch, pressly/goose, ariga/atlas, tursodatabase/libsql.
- Storage/uploads: transloadit/uppy, tus/tusd, pingdotgg/uploadthing,
  seaweedfs/seaweedfs, minio/minio, aws/aws-sdk-js-v3.
- Search: meilisearch/meilisearch, typesense/typesense, opensearch-project/OpenSearch,
  paradedb/paradedb, quickwit-oss/tantivy, elastic/elasticsearch.
- Billing: stripe/stripe-node, getlago/lago, killbill/killbill,
  juspay/hyperswitch, polarsource/polar, openmeterio/openmeter,
  flexprice/flexprice, useautumn/autumn, lmsqueezy/lemonsqueezy.js.
- Email: resend/react-email, mjmlio/mjml, knadh/listmonk, postalserver/postal,
  mautic/mautic, nodemailer/nodemailer, maizzle/framework, unsend-dev/unsend (now "useSend").
- Notifications/realtime: novuhq/novu, 
  centrifugal/centrifugo, soketi/soketi, supabase/realtime, yjs/yjs,
  electric-sql/electric, partykit/partykit, socketio/socket.io, ueberdosis/hocuspocus,
  rocicorp/mono (Zero), tldraw/tldraw.
- Jobs/workflows: taskforcesh/bullmq, timgit/pg-boss, graphile/worker,
  triggerdotdev/trigger.dev, inngest/inngest, temporalio/temporal, hatchet-dev/hatchet,
  sidekiq/sidekiq, rails/solid_queue, celery/celery, riverqueue/river,
  hibiken/asynq, windmill-labs/windmill, n8n-io/n8n, activepieces/activepieces,
  NangoHQ/nango, restatedev/restate.
- API/keys/rate limit/gateway: unkeyed/unkey, Kong/kong, TykTechnologies/tyk,
  apache/apisix, arcjet/arcjet-js, upstash/ratelimit-js, OAI/OpenAPI-Specification,
  hoppscotch/hoppscotch, scalar/scalar, trpc/trpc.
- Webhooks: svix/svix-webhooks, frain-dev/convoy, hook0/hook0,
  standard-webhooks/standard-webhooks.
- Feature flags: Unleash/unleash, Flagsmith/flagsmith, growthbook/growthbook,
  open-feature/spec, flipt-io/flipt, PostHog/posthog.
- Analytics: PostHog/posthog, plausible/analytics, umami-software/umami,
  Openpanel-dev/openpanel, jitsucom/jitsu, rudderlabs/rudder-server, matomo-org/matomo.
- Observability: getsentry/sentry, glitchtip (on GitLab — link https://glitchtip.com),
  open-telemetry/opentelemetry-js, SigNoz/signoz, grafana/grafana, grafana/loki,
  grafana/tempo, prometheus/prometheus, hyperdxio/hyperdx, openobserve/openobserve,
  pinojs/pino, getsentry/sentry-javascript.
- Audit logs: retracedhq/retraced (BoxyHQ), BemiHQ/bemi, pgaudit/pgaudit,
  paper-trail-gem/paper_trail, django-commons/django-simple-history.
- Admin/internal tools: marmelab/react-admin, refinedev/refine, SoftwareBrothers/adminjs,
  appsmithorg/appsmith, ToolJet/ToolJet, directus/directus, payloadcms/payload,
  activeadmin/activeadmin, filamentphp/filament, django admin, avo-hq/avo.
- UI/app shell: shadcn-ui/ui, tailwindlabs/tailwindcss, radix-ui/primitives,
  TanStack/table, tremorlabs/tremor, react-hook-form/react-hook-form, colinhacks/zod.
- Deploy/self-host: coollabsio/coolify, basecamp/kamal, dokku/dokku, Dokploy/dokploy,
  caprover/caprover, docker/compose, helm/helm, opentofu/opentofu, pulumi/pulumi,
  sst/sst, caddyserver/caddy, traefik/traefik.
- Security/compliance/secrets: Infisical/infisical, openbao/openbao, hashicorp/vault
  (BSL), getsops/sops, trycompai/comp, getprobo/probo, OWASP/CheatSheetSeries,
  gitleaks/gitleaks, trufflesecurity/trufflehog, aquasecurity/trivy.
- AI: vercel/ai, BerriAI/litellm, langfuse/langfuse, Helicone/helicone,
  langchain-ai/langchainjs, run-llama/llama_index, pgvector/pgvector,
  qdrant/qdrant, promptfoo/promptfoo, modelcontextprotocol/specification.

### The reference shelf — production OSS SaaS to study (use these in 🔍)

TypeScript / Next.js monorepos: calcom/cal.com (scheduling; orgs, teams, SSO via
SAML Jackson, Stripe, workflows, webhooks, API keys, app store of integrations),
documenso/documenso (e-signatures; teams, Stripe, webhooks, API, audit log of
document events, background jobs), dubinc/dub (link management; workspaces,
Stripe, usage limits, API keys, webhooks, analytics via Tinybird, SAML SSO),
formbricks/formbricks (surveys; orgs/environments, RBAC, integrations),
twentyhq/twenty (CRM; workspaces, GraphQL+REST API, webhooks, workflows, jobs
with BullMQ), makeplane/plane (project mgmt; Django + Next.js, workspaces,
roles, notifications), mfts/papermark (doc sharing; teams, Stripe, analytics),
midday-ai/midday (business OS; Supabase, jobs), unkeyed/unkey (API keys; itself a
SaaS), triggerdotdev/trigger.dev (itself a SaaS), Infisical/infisical (secrets
SaaS; RBAC, SSO/SCIM, audit logs, orgs), openstatusHQ/openstatus (**an open-source
status page + uptime monitor — literally a real Beacon; use it often**),
hoppscotch/hoppscotch, lobehub/lobe-chat (AI app).

Python: PostHog/posthog (Django; orgs/projects, feature flags, Celery),
getsentry/sentry (Django; orgs, RBAC, SSO, audit log, integrations),
makeplane/plane (Django API), saleor/saleor (GraphQL commerce), zulip/zulip.

Ruby: chatwoot/chatwoot (Rails; accounts, roles, Sidekiq, webhooks, integrations),
gitlabhq/gitlabhq (Rails; the encyclopedia of every SaaS component),
discourse/discourse (Rails; jobs, plugins, notifications), mastodon/mastodon,
maybe-finance/maybe (Rails 8, Solid Queue; archived but excellent reading).

Go / other: mattermost/mattermost, gitea (go-gitea/gitea), grafana/grafana,
supabase/supabase (platform), louislam/uptime-kuma (self-hosted uptime monitor —
another Beacon to study).

Starter kits / boilerplates (show "what a SaaS skeleton includes"):
nextjs/saas-starter (official, minimal: auth, Stripe, teams, RBAC, activity log),
vercel/next-forge (formerly haydenbleasel/next-forge), wasp-lang/open-saas,
boxyhq/saas-starter-kit (enterprise features: SSO, SCIM, audit, webhooks),
ixartz/SaaS-Boilerplate, t3-oss/create-t3-app, laravel/laravel + laravel/cashier-stripe,
apptension/saas-boilerplate (Django + React).

## Do not

- Do not invent repos, URLs, file paths, incidents, or quotes.
- Do not write a listicle. Every repo you name should come with *why* and *when*.
- Do not skip any of the eight sections or the three depth/exercise sub-headings.
- Do not use headings other than the exact ones above at the `##` level.

---

# Version 2 additions

## Two new sections in every lesson (English)

1. `## ⚡ In 60 seconds` — placed **immediately after the level line**, before
   `## 🧭`. 4–6 bullets a busy junior can read in one minute: what the component
   is, the one rule that matters most, the default choice for a v1, and the
   biggest trap. No new facts that the lesson body doesn't support.
2. `## ✍️ Check yourself` — placed **after `## 🧾 Recap` and before `## 📚
   References`**. Exactly 5 questions: 2 recall, 2 applied to Beacon, 1 "spot the
   bug / what breaks" scenario. Each in this exact shape (the blank lines matter):

   ```
   **1. The question text?**

   <details><summary>Answer</summary>

   Two to four sentences. Point back to the section that explains it.

   </details>
   ```

## The Arabic mirror

Each module `saas/modules/NN-slug.md` gets a mirror `saas/modules/NN-slug.ar.md`:
the same lessons, sections, diagrams, tables, exercises, questions and references,
in the same order — a faithful translation, not a paraphrase or a summary.

### Register

Professional, concise Modern Standard Arabic — the style of good Arabic technical
documentation (Hsoub Academy / حسوب). Read the "Arabic register" section of
`notes/LESSON-SPEC.md` (the sister course's rules, which apply here unchanged) and
calibrate on `modules/03-caching/module.ar.md`. In short:

- Short, clear sentences with verbs and normal connectors (لأن، عندما، لكن، لذلك).
  No literary flourishes, no rhymed prose, no telegraphic fragments.
- Technical terms: Arabic first with the English in parentheses on first use,
  Arabic alone after: المصادقة (Authentication)، التفويض (Authorization)،
  المستأجر (Tenant)، الاشتراك (Subscription)، الويب هوك (Webhook)، الطابور (Queue)،
  المهمة الخلفية (Background Job)، سجل التدقيق (Audit Log)، الدخول الموحد (SSO).
- Product, repo, library and protocol names stay Latin: Stripe, Postgres, Beacon,
  OAuth, SAML, SCIM, `owner/repo`.
- Numbers as Western digits (29 دولارًا، 5 دقائق). Keep "SaaS" as SaaS.
- Code blocks, commands, file paths, identifiers, JSON and URLs are **not**
  translated. Code comments may stay English.
- Mermaid: translate node labels and messages to Arabic, keep Latin product
  names; keep the diagram's structure identical. Quote every label.
- Table cells: translate prose; keep repo links, stacks and licenses in Latin.

### Exact Arabic headings (the build depends on these)

| English | Arabic |
|---|---|
| `# Module N — Title` | `# الوحدة N — العنوان` |
| `# N.M — Title` | `# N.M — العنوان` (same number) |
| `*Level: 🟢 Beginner*` / `🟡 Intermediate` / `🔴 Advanced` | `*المستوى: 🟢 مبتدئ*` / `*المستوى: 🟡 متوسط*` / `*المستوى: 🔴 متقدم*` |
| ` · *Prerequisites: 1.1, 2.1*` | ` · *المتطلبات: 1.1، 2.1*` |
| `## ⚡ In 60 seconds` | `## ⚡ الدرس في دقيقة` |
| `## 🧭 Why every SaaS has this` | `## 🧭 لماذا يحتاجه كل SaaS` |
| `## 📐 How it works` | `## 📐 كيف يعمل` |
| `### 🟢 The essentials` | `### 🟢 الأساسيات` |
| `### 🟡 Going deeper` | `### 🟡 التعمق أكثر` |
| `### 🔴 At scale / enterprise` | `### 🔴 على نطاق واسع وللمؤسسات` |
| `## 🏆 The best repos` | `## 🏆 أفضل المستودعات` |
| table header | `\| المستودع \| ما هو \| التقنيات \| الترخيص \| اختره عندما \|` |
| **If you only study one:** | **إن درست مستودعًا واحدًا فقط:** |
| **Buy, build, or self-host?** | **اشترِ أم ابنِ أم استضف بنفسك؟** |
| `## 🔍 Study it in the wild` | `## 🔍 ادرسه في مشاريع حقيقية` |
| **What to notice** | **ما الذي تلاحظه** |
| `## 🛠️ Build it into Beacon` | `## 🛠️ ابنِه في Beacon` |
| `### 🟢 Beginner exercise` | `### 🟢 تمرين المبتدئ` |
| `### 🟡 Intermediate exercise` | `### 🟡 تمرين المستوى المتوسط` |
| `### 🔴 Advanced exercise` | `### 🔴 تمرين المستوى المتقدم` |
| **Done when:** | **يكتمل عندما:** |
| `## ⚠️ Mistakes juniors make` | `## ⚠️ أخطاء يقع فيها المبتدئون` |
| `## 🧾 Recap` | `## 🧾 الخلاصة` |
| `## ✍️ Check yourself` | `## ✍️ اختبر نفسك` |
| `<summary>Answer</summary>` | `<summary>الإجابة</summary>` |
| `## 📚 References` | `## 📚 المراجع` |

References keep their original titles and URLs (add an Arabic gloss after the
dash if helpful). Links like `(../REPOS.md)` stay as they are.
