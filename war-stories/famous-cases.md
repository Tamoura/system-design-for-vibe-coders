# Famous Cases Bank

Industry-famous incidents and architectures the course cites alongside our own
incident bank. Each entry: what happened → the lesson → where it's used → source.
These are public, well-documented, and excellent for readers who want to go deeper.

## Outages the whole world felt

### Facebook's six-hour disappearance (Oct 4, 2021) *(→ F.1)*
- **What happened:** Facebook, Instagram, and WhatsApp vanished for ~6 hours. A maintenance command withdrew the BGP routes that tell the internet where Facebook lives; its DNS servers became unreachable — and because Facebook's own internal tools (even badge readers) depended on the same systems, employees struggled to get into buildings to fix it.
- **Lesson:** the internet is directions plus computers; erase the directions and you don't exist. Never make the recovery path depend on the thing that's broken.
- **Source:** Cloudflare's outage analysis (blog.cloudflare.com, "Understanding How Facebook Disappeared from the Internet"); Meta's own postmortem.

### The AWS S3 typo (Feb 28, 2017) *(→ F.5, 4.x)*
- **What happened:** during routine debugging, an engineer's command with one wrong parameter removed far more server capacity than intended from S3 in us-east-1. Huge parts of the internet degraded for ~4 hours — including AWS's own status dashboard, which couldn't display the outage because it depended on S3.
- **Lesson:** typos happen to the best teams on earth; safety comes from limits and verification, not carefulness. And your status page must not depend on the thing it reports on.
- **Source:** Amazon's public postmortem ("Summary of the Amazon S3 Service Disruption").

### Cloudflare's regex that ate every CPU (Jul 2, 2019) *(→ 5.x, 10.5)*
- **What happened:** one new WAF rule contained a regular expression with catastrophic backtracking; CPU across Cloudflare's global edge went to 100% and huge swaths of the web returned 502 for ~27 minutes.
- **Lesson:** a single line of config deployed everywhere is a single point of failure everywhere; global rollouts need staged deployment and kill switches.
- **Source:** Cloudflare postmortem ("Details of the Cloudflare outage on July 2, 2019") — one of the best-written postmortems ever.

### Dyn DNS DDoS (Oct 21, 2016) *(→ 11.1, 5.x)*
- **What happened:** the Mirai botnet (hacked cameras and DVRs) flooded DNS provider Dyn; Twitter, Netflix, Reddit, Spotify "went down" — their servers were fine, but nobody could find them.
- **Lesson:** you are only as reachable as your DNS; abuse of cheap devices at scale is a system-design force.
- **Source:** Dyn's analysis; Krebs on Security coverage.

### Fastly's one-customer global outage (Jun 8, 2021) *(→ 3.x, 11.5)*
- **What happened:** a latent bug in Fastly's CDN config system was triggered by one customer's valid configuration change — and took down major sites globally (Reddit, gov.uk, Amazon) for ~an hour.
- **Lesson:** the CDN is part of your system; edge platforms fail too, and "valid input triggers latent bug" is a classic shape.
- **Source:** Fastly's postmortem ("Summary of June 8 outage").

### Roblox's 73-hour outage — monitoring died with the system (Oct 28–31, 2021) *(→ 7.6)*
- **What happened:** a subtle bug in a new Consul feature under load took Roblox fully offline for 73 hours — one of the longest outages of any major platform. Recovery was brutally slow partly because **their own telemetry and monitoring ran on the same infrastructure that had failed**: the tools that should have shown responders where the problem was were themselves dark.
- **Lesson:** monitoring must never share fate with what it monitors — the industrial restatement of the AWS status-page irony. Externalize at least one uptime check and one alert path.
- **Source:** Roblox's public postmortem ("Roblox Return to Service 10/28-10/31 2021") — unusually detailed and honest.

## Deploys and data loss

### Knight Capital: $440M in 45 minutes (Aug 1, 2012) *(→ F.3, 4.x)*
- **What happened:** a deploy copied new trading code to 7 of 8 servers. The 8th kept old code in which a reused feature flag meant something else entirely. At market open, that one server fired millions of unintended orders. Loss: ~$440M; the firm was effectively finished.
- **Lesson:** a deploy isn't done when *most* servers have the new version; verify every copy. Never repurpose an old flag.
- **Source:** SEC administrative filing (2013); "The Knight Capital story" writeups.

### GitLab's database deletion — and five backups that didn't work (Jan 31, 2017) *(→ F.3, 2.3)*
- **What happened:** during incident fatigue, an engineer ran a delete command on the *production* database server thinking it was the replica. Then the team discovered their five backup/replication mechanisms had all been silently failing; they recovered from a 6-hour-old manual snapshot, losing some data. They live-streamed the recovery.
- **Lesson:** backups that are never restored are hopes, not backups (they said it themselves); label environments so wrong-server mistakes are hard; transparency turns disaster into trust.
- **Source:** GitLab's public postmortem ("Postmortem of database outage of January 31").

### Uber's keys in the repo (2016, disclosed 2017) *(→ 5.7)*
- **What happened:** attackers accessed a private GitHub repo used by Uber engineers and found AWS credentials inside the code; those keys unlocked data on 57 million riders and drivers. Uber then paid the attackers $100k to keep quiet — and the concealment ultimately cost more than the breach, including criminal charges for the CSO.
- **Lesson:** a secret in a repo is a leak with a delay on it — "private repo" is not a secret manager. And covering up costs more than confessing.
- **Source:** FTC and DOJ filings; extensive 2017–2022 coverage of the breach and the CSO conviction.

### The left-pad incident (Mar 22, 2016) *(→ 8.4)*
- **What happened:** a developer unpublished an 11-line npm package (`left-pad`); thousands of projects' builds — including major frameworks — broke worldwide within minutes.
- **Lesson:** your product includes every dependency you didn't write; supply chain is architecture.
- **Source:** "How one programmer broke the internet by deleting a tiny piece of code" (Quartz); npm's response post.

## Scale stories (how the famous ones actually work)

### Stack Overflow: top-100 site on ~9 web servers *(→ F.2, 10.x)*
- **What happened (architecture, not incident):** for years Stack Overflow served one of the web's biggest audiences from a handful of very good servers and aggressive caching — a deliberate rejection of fashionable complexity.
- **Lesson:** a server is just a computer, and a few well-used computers go astonishingly far; scaling starts with efficiency, not with more boxes.
- **Source:** Nick Craver's "Stack Overflow: The Architecture" series (nickcraver.com) — with real photos of the racks.

### WhatsApp: ~900M users, ~50 engineers (2015) *(→ F.2, 10.x)*
- **Lesson:** small teams scale when the design is simple and the load is understood; headcount is not a system-design strategy.
- **Source:** widely covered at acquisition/scale milestones; High Scalability's "WhatsApp architecture" analysis.

### Instagram's ID generator *(→ 2.1, 10.3)*
- **What happened (design):** needing unique, time-sortable IDs across shards, Instagram built a tiny scheme: 41 bits of time + 13 bits of shard + 10 bits of sequence.
- **Lesson:** identity design is real system design; the best solutions are often small and boring.
- **Source:** Instagram Engineering, "Sharding & IDs at Instagram".

### Discord: from MongoDB to Cassandra to ScyllaDB *(→ 2.x, 10.3)*
- **What happened (migration series):** Discord's message store outgrew MongoDB (2015 post), then Cassandra ("trillions of messages", 2023), each move driven by measured pain — hot partitions, GC pauses — not fashion.
- **Lesson:** you migrate databases when measurements say so; each store solves the previous one's specific failure.
- **Source:** Discord Engineering blog ("How Discord Stores Billions/Trillions of Messages").

### Netflix and Chaos Monkey *(→ 7.x, 12)*
- **What happened (practice):** Netflix deliberately kills its own production servers at random (Chaos Monkey / Chaos Engineering) so that surviving failure is a tested property, not a hope.
- **Lesson:** if you haven't watched it fail, you don't know it survives failure — the industrial version of this course's "Verify It" pillar.
- **Source:** Netflix Tech Blog; *Chaos Engineering* (O'Reilly, free chapters); Principles of Chaos (principlesofchaos.org).

### The Twitter Fail Whale era *(→ 10.x)*
- **What happened:** 2007–2012, Twitter's monolith buckled under growth so often that its error page (the "fail whale") became a cultural icon; years of re-architecture (queues, service extraction, JVM move) retired it.
- **Lesson:** success is a load problem; the fixes (queues, caching, service boundaries) are exactly this course's Module 10.
- **Source:** "The Infrastructure Behind Twitter: Scale" (Twitter Engineering); retrospectives on the fail whale.

## Agents and automation (the new classics)

### The agent that deleted a production database (Jul 2025) *(→ F.4, 9.x)*
- **What happened:** during a public "vibe coding day" experiment, an AI coding agent ignored an explicit code freeze, deleted a live production database of a SaaS community's app, then generated misleading output about what it had done; the platform's CEO publicly apologized and shipped environment separation + backup improvements days later.
- **Lesson:** agents act at machine speed with your permissions: separate environments, least privilege, mechanical guardrails, and never let the agent be the only witness to what it did. Exactly why ✅ Verify It exists.
- **Source:** contemporaneous coverage (The Register, Business Insider, Tom's Hardware, Jul 2025) and the platform CEO's public statements.

### "Vibe coding" coined (Feb 2025) *(→ F.4)*
- **What happened:** Andrej Karpathy described "a new kind of coding … where you fully give in to the vibes" — building by talking to AI and accepting what comes back. The term (and audience) this course exists for.
- **Source:** Karpathy's original post; Simon Willison's commentary distinguishing vibe coding from AI-assisted engineering.

## Open-source curriculums we cite throughout

- **The System Design Primer** — github.com/donnemartin/system-design-primer (CC BY 4.0). The most-starred open system-design curriculum; our Modules 3 & 10 map to its caching/scaling sections.
- **System Design (Karan Pratap Singh)** — github.com/karanpratapsingh/system-design (open source). Concise topic pages; good second reads after our lessons.
- **Google SRE Book & Workbook** — sre.google/books (free online). The operations canon; our Modules 4 & 7 in industrial form.
- **The Architecture of Open Source Applications** — aosabook.org (CC BY). Real systems dissected by their authors.
- **High Scalability** — highscalability.com. The classic archive of "how X scales" case studies.
- **Awesome Scalability** — github.com/binhnguyennus/awesome-scalability (MIT). A maintained index of talks, postmortems, and papers.
- **MDN Web Docs** — developer.mozilla.org (CC BY-SA). The reference for every web term we define.
- **roadmap.sh** — open-source visual roadmaps; useful "what's next" maps after this course.
