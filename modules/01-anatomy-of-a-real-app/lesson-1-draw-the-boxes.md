# Module 1 — Anatomy of a Real App

*Three lessons on seeing the system you already have. Before you can protect a
product you have to be able to draw it: the boxes it is made of, what each one is
for, and what each one quietly lies about. Then you follow a single request all
the way through those boxes, and wire the two instruments that tell you when one
of them breaks. Terms are defined on first use; the
[Glossary](../../GLOSSARY.md) has the rest.*

---

# 1.1 — Draw the Boxes Before the Agent Writes the Code

*Module 1: Anatomy of a Real App*

---

## 🔥 The War Story

After a routine zero-downtime deploy, the main site was fine. Every check was green.
Then the admin team reported that the upload dashboard — which lives on its own
subdomain — was throwing generic network errors on every file.

Nothing had changed in the uploader's code. Nothing in its deploy. The main site,
sharing the same backend, worked perfectly.

The cause was a map nobody had drawn. The platform's deploys are *blue-green*: two
copies of the API exist, and each deploy starts the new copy on a different port,
then flips traffic to it. The **main** site's proxy config had been updated to route
through a shared upstream that follows the flip. But two *sibling* subdomains —
`upload.` and `direct.` — had their own proxy configs, written months earlier, each
hardcoding the API's old port:

```mermaid
graph TD
    subgraph edge["nginx — three configs, one truth?"]
        MAIN["www config<br/><small>proxy_pass → upstream ✓</small>"]
        UP["upload. config<br/><small>proxy_pass → :5000 ✗</small>"]
        DIR["direct. config<br/><small>proxy_pass → :5000 ✗</small>"]
    end
    MAIN --> U["shared upstream<br/><small>follows the flip</small>"]
    U --> GREEN["API green :5010<br/><small>ALIVE</small>"]
    UP -.-> DEAD["API blue :5000<br/><small>stopped after flip</small>"]
    DIR -.-> DEAD
    style DEAD stroke-dasharray: 5 5
```

When the flip moved the live API from port 5000 to 5010 and stopped the old copy,
the main site followed. The siblings kept pointing at a corpse.

The fix was mechanical — route every config through the same shared upstream, and
make the deploy script *assert* it. But notice what the bug actually was: **nobody's
mental model of the system matched the system.** Everyone "knew" the architecture.
Nobody had drawn it recently enough to see that three configs claimed to know where
the API lives, and only one of them was maintained.

You cannot reason about what you cannot draw. And your AI agent can't either — it
was an agent that wrote those sibling configs, correctly, against the architecture
*as it existed that day*.

---

## 📐 The Principle

### 1. Every production app is the same seven boxes

Strip away the frameworks and every serious web product converges on the same
anatomy. Here is the real reference architecture this course draws its incidents
from — a platform serving web, iOS, Android, and TV clients worldwide:

```mermaid
graph TD
    subgraph clients["Clients"]
        B["Browser<br/><small>Next.js SSR pages</small>"]
        M["Mobile apps<br/><small>iOS · Android</small>"]
        TV["TV apps"]
    end
    subgraph edge["Edge — someone else's computers"]
        CDN["CDN / WAF<br/><small>Cloudflare: TLS, cache, bot rules</small>"]
    end
    subgraph origin["Origin — one VPS"]
        NG["Reverse proxy<br/><small>nginx: routing, TLS to origin</small>"]
        WEB["Web app<br/><small>Next.js: SSR + assets</small>"]
        API["API<br/><small>Express: business logic</small>"]
        RED[("Redis<br/><small>cache + presence + limits</small>")]
        DB[("MongoDB<br/><small>source of truth</small>")]
    end
    subgraph ext["External services"]
        R2[("Object storage<br/><small>R2: media files</small>")]
        SMTP["Email<br/><small>SMTP provider</small>"]
        PUSH["Push<br/><small>APNs / FCM</small>"]
    end
    B --> CDN
    M --> CDN
    TV --> CDN
    CDN --> NG
    NG --> WEB
    NG --> API
    WEB --> API
    API --> RED
    API --> DB
    API --> R2
    API --> SMTP
    API --> PUSH
```

Seven kinds of box, each with exactly one job:

| Box | Its one job | What it must NOT become |
|---|---|---|
| Client | Render state, capture intent | A place where business rules live |
| CDN | Absorb traffic, terminate TLS | A cache of things that vary per user |
| Reverse proxy | Route requests to the right process | A pile of copy-pasted configs |
| App / API | Business logic | A file server or a job runner |
| Cache | Make reads cheap, absorb load | A database (it may vanish any moment) |
| Database | Be the source of truth | A queue, a cache, or an analytics warehouse |
| Object storage | Hold big immutable blobs | A filesystem you mutate in place |

This is the C4 model's "container diagram" level (Simon Brown's term — see
references), and it's the single most useful drawing you will ever make. Not
because it's sophisticated, but because every incident in this course is a story
about two of these boxes disagreeing.

### 2. Every box lies

The reason system design is a discipline and not a diagram is that each box
routinely reports a reality that isn't true. From this course's own incident bank:

| Box | The lie | Incident that proved it |
|---|---|---|
| CDN | "I respect your caching headers" | Ignored `Vary`, poisoned pages with JSON *(3.2)* |
| Reverse proxy | "I reloaded the config" | Stale worker kept routing to a dead port *(4.3)* |
| Build system | "This build is fresh" | Webpack cache shipped stale JS twice *(4.5)* |
| Cache | "I'm just an optimization" | FLUSHDB wiped live-presence state *(3.4)* |
| Database | "The test passed" | Mocked models let broken queries ship *(8.2)* |
| Object storage | "That file is deleted" | Replication bridge resurrected every delete *(2.2)* |
| Client | "I'm sending honest data" | Anonymous telemetry inflated rankings *(5.4)* |

Knowing the boxes is level one. Knowing what each one lies about is what this
course is actually for.

### 3. The drawing is a contract, not documentation

The sibling-subdomain incident happened because the architecture existed in three
places: the running system, people's heads, and some configs written at different
times. Three copies of the truth — so they diverged (a theme you'll meet again in
lesson 6.4: *any two sources of truth drift*).

The discipline that fixes this is cheap:

1. **One diagram file lives in the repo** (Mermaid in markdown — it diffs, it
   reviews, it can't rot invisibly in a wiki).
2. **Structural changes update the diagram in the same PR.** A new subdomain, a
   new service, a new store — no merge without the drawing.
3. **Anything the diagram claims, a script asserts.** "All subdomains route through
   the shared upstream" became a deploy-time assertion after the incident. A claim
   with no assertion is a hope.

### 4. For a vibe coder, the diagram is agent context

Here's the part classic courses don't teach. Your AI agent has no persistent
picture of your system: every session it reconstructs its understanding from the
code it happens to read. If the architecture lives only in code, the agent
rediscovers it — expensively, sometimes wrongly — every single time.

An architecture section in your agent's project memory (CLAUDE.md or equivalent)
is the highest-leverage document you will ever write. It's the difference between
an agent that *guesses* where uploads go and an agent that *knows*.

---

## 🎛️ Direct Your Agent

Time to start Relay — the accounts + creator content + media + feeds product you'll
carry through the whole course. You direct; the agent builds. You never need to
write a line yourself — the 🔧 boxes are optional, for readers who want to.

1. **Draw before anyone generates.** Tell your agent:
   > *"Before writing any code: draw Relay v1's architecture as a Mermaid diagram —
   > browser → web app → database, nothing else — save it as `docs/architecture.md`,
   > and explain each box's single job to me in plain language."*
   Push back on any box you didn't ask for. Every box is a seam you now own.
2. **Scaffold it.**
   > *"Scaffold Relay exactly as the diagram shows: one web app, one API process,
   > one database, running locally. Then show it to me running in the browser, and
   > tell me which box each thing I can see came from."*
3. **The boxes table.**
   > *"Add a table to `docs/architecture.md`: each box, its one job, and what it
   > must never become."*
4. **Install the contract rule.**
   > *"Add to CLAUDE.md: any change that adds a service, store, subdomain, or
   > external dependency must update `docs/architecture.md` in the same PR."*
5. **Predict the future.**
   > *"Add dashed boxes to the diagram for what we expect to add later: CDN, cache,
   > object storage, queue."*
   You now have a map of the seams you'll be learning, drawn before you need them.

Finish: *"Commit everything with the message `01-1-boxes-drawn`."*

> 🔧 **Under the hood** (optional): the diagram is plain text — Mermaid's `graph TD`
> syntax inside markdown. The scaffold is `npx create-next-app` (or your stack's
> equivalent) plus a database via Docker. Read `docs/architecture.md` in the repo
> after the agent writes it; it's the most readable file you own.

### The context and the guardrail

**The failure mode:** agents make *locally correct, globally wrong* decisions.
The agent that wrote the sibling subdomain configs did nothing wrong — it matched
the system as it found it. It had no way to know a deploy-model change elsewhere
would invalidate the pattern. Global knowledge is your job to supply.

**Context to give (put this in project memory, not in one chat):**

```markdown
## Architecture (contract — update in the same PR as any structural change)
- Diagram: docs/architecture.md (Mermaid). It is the source of truth.
- All API traffic routes through the shared nginx upstream `app_backend`.
  NEVER write a proxy_pass pointing at a literal port.
- Redis is disposable cache + soft state only. Nothing in Redis may be
  the only copy of anything.
- Object storage is immutable: write new keys, never mutate in place.
```

**Review questions for any structural change:**

1. "Which boxes does this change touch, and does `docs/architecture.md` still
   describe the system after it merges?"
2. "Does this duplicate a source of truth that already exists (routing, config,
   schema)? If yes, derive it or assert it."
3. "You just added a box. What does this box lie about, and which assertion or
   test catches the lie?"

**Guardrail to install:** a deploy-time assertion for every claim the diagram
makes about routing — the exact fix the incident shipped. Grep your proxy configs
for literal ports in CI; fail if any appear outside the upstream block.

---

## ✅ Verify It

Accept this lesson as done only when every box is checked — none requires reading code:

- [ ] `docs/architecture.md` exists and the diagram **renders as boxes and arrows**
      (open the file preview; if you see text soup, it's not done).
- [ ] The running app matches the drawing: for each box, you can name the thing you
      *clicked or saw* that proves it exists (page loads → web app is real; data
      survives a restart → database is real — ask the agent to restart it and show you).
- [ ] **Cold-start test:** open a brand-new agent session and ask *"where does
      uploaded media go, and what must never live only in the cache?"* It answers
      correctly from CLAUDE.md alone, without you explaining anything.
- [ ] Ask the agent: *"search all proxy/config files for hardcoded ports and show me
      the raw output."* The output is empty outside the shared upstream block.
- [ ] You can redraw the seven-box diagram from memory on paper. (This one is for you.)

---

## 🧾 Recap card

- Seven boxes: client, CDN, proxy, app, cache, database, object storage. One job each.
- Every box lies; the incident bank is a catalog of the lies.
- The diagram is a contract: repo-versioned, PR-updated, script-asserted.
- Your agent reconstructs architecture from scratch every session — write it down
  or watch it guess.
- A claim with no assertion is a hope.

## 📚 References & further wandering

- Simon Brown, **The C4 Model for visualising software architecture** — [c4model.com](https://c4model.com). The container-diagram level used in this lesson.
- Martin Kleppmann, **Designing Data-Intensive Applications** (O'Reilly, 2017) — ch. 1 on reliability, scalability, maintainability; the deep version of "every box lies."
- **The Twelve-Factor App** — [12factor.net](https://12factor.net). Factors III (config) and VI (stateless processes) are lessons 5.3 and 10.1 in embryo.
- Betsy Beyer et al., **Site Reliability Engineering** (Google, 2016) — free at [sre.google/sre-book](https://sre.google/sre-book/table-of-contents/); ch. 3 "Embracing Risk" for why "green checks" lie.
- nginx docs, **Using nginx as HTTP load balancer / upstream module** — the shared-upstream pattern from the incident fix.

*Source incidents: [incident bank — Deployment & Infrastructure](../../war-stories/incident-bank.md)*
