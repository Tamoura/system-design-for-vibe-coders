# Glossary — plain language, no prerequisites

Every term the course uses, defined for a reader who has never coded. Arabic
equivalents included; the Arabic mirror is [GLOSSARY.ar.md](./GLOSSARY.ar.md).
Lessons link here the first time a term appears.

## The machines

| Term | بالعربية | Plain meaning |
|---|---|---|
| Server | خادم | A computer that runs your product all day and never sleeps. Usually rented, sitting in a data center. |
| Client | عميل | Whatever the user holds: a browser, a phone app, a TV app. It asks; the server answers. |
| VPS | خادم افتراضي | A rented slice of a big computer that behaves like your own server. |
| The cloud | السحابة | Other people's servers, rented by the hour. |
| Data center | مركز بيانات | The warehouse full of servers where "the cloud" physically lives. |

## The journey of a request

| Term | بالعربية | Plain meaning |
|---|---|---|
| Request / Response | طلب / استجابة | The client asks (request); the server answers (response). The web is only this, billions of times. |
| DNS | نظام أسماء النطاقات | The internet's phone book: turns a name (`relay.app`) into the address of a server. |
| Domain | نطاق | Your product's public name on the internet. |
| HTTP / HTTPS | — | The language requests and responses are spoken in; the S means encrypted. |
| TLS / Certificate | التشفير / الشهادة | The lock that makes HTTPS private, and the paper that proves the site is really you. |
| CDN | شبكة توزيع المحتوى | A worldwide chain of helper computers that keep copies of your pages close to users so they load fast — and shield your server. |
| Edge | الحافة | The CDN's computers near the user (as opposed to your "origin"). |
| Origin | الخادم الأصل | Your actual server as the CDN reaches it: through your reverse proxy. Testing it directly "bypasses the CDN." |
| App port | منفذ التطبيق | The numbered door (for example 3000) your app program listens on, behind the proxy. Testing it directly skips the proxy too. |
| Endpoint | نقطة نهاية | One address your API answers at, like `/api/posts`: one door into the server. |
| Middleware | البرمجية الوسيطة | Code inside your app that every request passes through before your handler: request IDs, login checks, logging. Not the reverse proxy, which is a separate program in front of the app. |
| BGP | بروتوكول البوابة الحدودية | How networks tell each other which routes lead where: the internet's road signs. Withdraw your routes and nobody can reach you. |
| Reverse proxy | الخادم الوسيط العكسي | The doorman program on your server (often "nginx") that receives every request and routes it to the right internal program. |
| Header | ترويسة | A sticky note attached to a request or response — who it's from, how long to keep it, what shape it is. Machines read these. |
| Latency | الكمون | How long a round trip takes. Measured in milliseconds; felt in patience. |

## Code and shipping

| Term | بالعربية | Plain meaning |
|---|---|---|
| Code | الكود | Your product's instructions, written precisely enough for a machine to follow. |
| Repo (repository) | المستودع | The product's home folder plus its complete history of saved versions (kept by a tool called git). |
| Commit | إيداع | One saved version in that history, with a note about what changed. |
| Branch | فرع | A parallel draft of the product where changes can be made safely before joining the main version. |
| PR (pull request) | طلب دمج | A proposal: "here are my changes — review them before they join the main version." |
| Deploy | نشر | Copying a chosen version of the code onto the always-on server so the world gets it. |
| Rollback | تراجع | Deploying yesterday's known-good version because today's went wrong. |
| Build | البناء | The step that turns human-written code into the optimized files the server actually runs. |
| Environment | بيئة | One complete copy of your system: your machine (local), a rehearsal copy (staging), the real one (production). |
| Env var (environment variable) | متغير بيئة | A named setting the code reads at runtime — like which database to use — different in each environment. |
| CI | التكامل المستمر | A robot that runs your checks (tests, rules) automatically on every proposed change. |
| Staging | بيئة التجهيز | A rehearsal copy of production: same shape, no real users, safe to break. Changes run here before the real thing. |
| Diff | الفروق | The exact changes between two versions: lines removed, lines added. What you review before a change joins. |
| Mermaid | — | A way to write diagrams as plain text in a markdown file; previews show it as boxes and arrows. This course's diagrams are Mermaid. |
| Blue-green deploy | النشر الأزرق-الأخضر | Keeping two copies of the app; switch traffic to the new one only after it proves healthy — so deploys don't interrupt users. |

## Data

| Term | بالعربية | Plain meaning |
|---|---|---|
| Database (DB) | قاعدة البيانات | The notebook your product never loses: users, content, orders — the source of truth. |
| Schema | مخطط البيانات | The agreed shape of what's stored: what a "user" record contains, what identifies it. |
| Query | استعلام | A question asked of the database. |
| Index | فهرس | The database's table of contents — the difference between finding a record instantly and reading the whole notebook. |
| Migration | هجرة | A controlled change to the data's shape or home. |
| Object storage | تخزين الكائنات | A warehouse for big files (audio, images, video) — separate from the database. |
| Backup | نسخة احتياطية | A copy of the data you could rebuild the product from. Only real once you've practiced restoring it. |
| Retention / TTL | الاحتفاظ / مدة البقاء | How long data is kept before automatic deletion. TTL = "time to live." |
| Cache | الكاش | A fast short-term memory holding copies of recent answers so the slow, true source is asked less. May vanish anytime — by design. |
| Redis | — | A popular, very fast in-memory store, used mostly as a cache and for short-lived state such as counters and sessions. |
| Hit rate | نسبة الإصابة | The share of requests the cache answers itself (a hit) instead of asking the slow source (a miss). 90% means 9 in 10 served from cache. |
| Cache invalidation | إبطال الكاش | Removing a cached answer because the truth changed. One of the two famously hard things. |

## Accounts and safety

| Term | بالعربية | Plain meaning |
|---|---|---|
| Auth (authentication) | المصادقة | Proving who you are (login). Authorization = what you're allowed to do. |
| Token | رمز | A temporary pass the client carries to prove it already logged in. |
| OAuth | — | "Sign in with Google/Apple": borrowing a login from a provider instead of a new password. |
| Rate limiting | تحديد المعدل | "Maximum N requests per minute" — the bouncer that keeps scripts from flooding you. |
| CAPTCHA / Turnstile | اختبار البشرية | The "prove you're human" gate on forms. |
| SSRF | — | Tricking a server into making requests to places it shouldn't (like its own internals). One of the classic attacks. |
| OWASP Top 10 | — | The security community's list of the ten most common ways web apps get broken into. |
| Secret | سر | A password, key, or token your system holds. Never in code; never in chat; rotated when exposed. |

## Operating

| Term | بالعربية | Plain meaning |
|---|---|---|
| Observability | المراقبة | Being able to see what your system is doing: logs, errors, metrics — so 3am problems wake a dashboard, not a user. |
| Log | سجل | The system's diary: one line per thing that happened. |
| Metric | مقياس | A number tracked over time (requests/minute, errors/hour). |
| Uptime / Downtime | التشغيل / الانقطاع | The time your product is working / not working. |
| Incident | حادثة | The window between "something is wrong" and "it's fixed and understood." |
| Postmortem | مراجعة ما بعد الحادثة | The honest write-up afterward: symptoms, cause, fix, lesson. This course is built from these. |
| p99 (99th percentile) | المئين 99 | The time within which 99 of every 100 requests finish. It shows the slow tail that an average hides. |
| Runbook | دليل تشغيل | A written step-by-step for a known situation (roll back, restore a backup), so anyone can do it calmly at 3am. |
| Load balancer | موازن الحِمل | A traffic director that spreads requests across several copies of your app and stops sending to a copy that is sick. |
| Feature flag | مفتاح ميزة | An on/off switch for a feature, controlled without redeploying. |
| Background job | وظيفة خلفية | Work the system does on its own schedule (send newsletter, clean up) — nobody is watching, so it needs locks, records, and receipts. |
| Idempotent | آمن التكرار | Safe to run twice: doing it again changes nothing extra. The property that makes retries harmless. |
| Idempotency key | مفتاح اللاأثر | A unique ID the client sends with a request; a repeat with the same key runs only once. |
| Queue | طابور | A waiting line for work: requests drop tasks in; workers take them out at a sustainable pace. |
| Webhook | — | One system ringing another's doorbell when something happens. |

## Directing agents

| Term | بالعربية | Plain meaning |
|---|---|---|
| Agent | وكيل | An AI that can take actions (write code, run commands) — not just chat. Your builder. |
| CLAUDE.md | — | The agent's standing memory file in your repo: what the product is, the rules, the architecture. Its job description. |
| Context | السياق | Everything the agent can currently see. It forgets between sessions — that's why memory files exist. |
| Prompt | موجّه | The instruction you give. Good ones carry a goal, constraints, and the evidence you demand back. |
| Hook | خطّاف | An automatic rule that runs at fixed moments (e.g., before every commit) — enforcing what memory alone can't. |
| Skill | مهارة | A saved, repeatable procedure the agent can run (a deploy skill, an audit skill). |
| Guardrail | حاجز أمان | Any mechanical protection — hook, test, assertion — that stops a known mistake without a human remembering to. |
| Drift guard | كاشف الانجراف | A test that fails when two things that must match stop matching (a list vs reality). |
| Verification | التحقق | Demanding evidence from the layer users touch, instead of trusting "done." The soul of this course. |
