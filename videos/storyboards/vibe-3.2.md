# Storyboard: System Design for Vibe Coders, lesson 3.2

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 2 of 3 for this course.** This has the strongest hook in the course: raw JSON served as a page, invisible in logs. Its one-sentence mechanism, 'the URL was no longer a sufficient cache key', works with any vendor. The lesson already tells the story in the past tense and dates the vendor detail (lesson-2-cache-poisoning.md:47-60).

## Cache Poisoning: when the first visitor decides what everyone sees

**Why this lesson:** the symptom is eerie (intermittent, affects some users, fixes itself, invisible in logs), and the cause is one picture: one URL with two kinds of response, and a shared cache that stores only one.
**Target viewer:** builders who have just put a CDN in front of their app.
**Length:** about 85 seconds.

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-10 | A phone shows a wall of raw JSON instead of a page | Glitch effect; code text scrolls | Your homepage... is raw JSON. | A user opens your page and gets a wall of raw code. You open it yourself and it works fine. | يفتح مستخدم صفحتك فيرى كتلة من الشيفرة الخام، وتفتحها أنت فتعمل بشكل سليم. |
| 2 | 10-20 | Error tracker and server logs, both empty | Magnifying glass finds nothing | No errors. No logs. Sometimes it heals. | Nothing in the error tracker, nothing in the logs, and sometimes it fixes itself. | لا شيء في متتبع الأخطاء، ولا في السجلات، وأحيانًا يُصلح نفسه بنفسه. |
| 3 | 20-34 | One URL /item/42 with two doors: 'address bar' -> HTML page, 'in-app click' -> compact JSON | A single address splits into two doors | One URL. Two answers. | The framework answers the same URL two ways: a full page for the address bar, and a compact JSON payload when you click around inside the app. | يجيب الإطار عن الرابط نفسه بطريقتين: صفحة كاملة لشريط العنوان، وحمولة JSON مختصرة عند التنقّل داخل التطبيق. |
| 4 | 34-46 | Response carries a 'Vary' tag; the edge cache box ignores it | A tag slides off the box | Vary: "cache these separately" | The app labelled its responses with a Vary header, meaning 'cache these separately'. At the time, the CDN's default did not honour it. | وضع التطبيق على ردوده ترويسة Vary، أي «خزّن كلًّا منها على حدة». لكن الإعداد الافتراضي لشبكة التوزيع آنذاك لم يكن يحترمها. |
| 5 | 46-60 | First visitor (in-app click) reaches an empty edge; JSON gets stamped in; a queue of browsers all receive JSON | A rubber stamp 'PAGE' lands on the JSON; copies fan out | First request decides for everyone. | So the first request to an empty edge decided what everyone got. If it was an in-app click, the JSON was cached as the page. | فأول طلب يصل إلى عقدة حافة فارغة كان يحدّد ما يحصل عليه الجميع. وإن كان نقرة داخل التطبيق، خُزّنت حمولة JSON على أنها الصفحة. |
| 6 | 60-70 | A TTL timer counts down to zero, the cache empties, and the cycle can repeat | Hourglass resets | ...until the TTL expires. | Everyone got raw JSON until the cache expired, which is why it seemed to heal itself. | وظلّ الجميع يتلقّون JSON إلى أن تنتهي صلاحية الكاش، ولهذا بدا وكأنه يُصلح نفسه. |
| 7 | 70-85 | Title card with a key icon | A key labelled 'URL' is too short for the lock | The URL was no longer a sufficient cache key. | The URL was no longer a sufficient cache key, and the cache didn't know it. Know what your edge does today. Open lesson 3.2. | لم يعد الرابط مفتاحًا كافيًا للكاش، والكاش لا يعلم ذلك. اعرف ما تفعله حافتك اليوم. افتح الدرس 3.2. |

**Closing takeaway:** intermittent, per-user, self-healing and invisible in logs almost always means a shared cache is serving the wrong thing to the wrong people.
**Call to action:** Open lesson 3.2, *The Cache Poisoning Incident*, and check how your own edge treats `Vary`.

**Re-check before production:** keep the narration vendor-neutral and in the past tense; name Cloudflare at most once with 'at the time'. Re-check the Cloudflare changelog of 2 July 2026 (Cache Rules can honour Vary, opt-in) before release, because the lesson itself says defaults move. Avoid showing the Next.js name on screen unless the lesson's 'Next.js App Router' is confirmed (the Arabic version currently drops it).
