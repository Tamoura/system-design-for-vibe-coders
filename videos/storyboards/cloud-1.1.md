# Storyboard: Cloud & DevOps: Zero to Hero, lesson 1.1

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 1 of 3 for this course.** The lesson has one procedural mental model (DNS, then TCP, then TLS, then HTTP, each with its own tool) and a twist hook: every pod is healthy, yet customers can't connect. The protocols will not date, and the sequential gates animate naturally.

## Walk the chain: why restarting didn't fix it

**Why this lesson:** It teaches one habit, to test each hop in order instead of guessing, through a concrete scene where the obvious fix (restart) does nothing.

**Target viewer:** A new graduate or developer who has typed `curl` but never debugged a production outage.

**Length:** about 75 seconds.

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-8 | A phone showing a spinning app; a support ticket pops up: "app won't load" | Ticket slides in, alarm pulse | "It's down." | Monday morning. The bank's app won't load for customers. | صباح الاثنين، وتطبيق البنك لا يفتح عند العملاء. |
| 2 | 8-18 | A row of pods, all green; logs scroll clean | Green checkmarks; a hand presses "Restart"; pods blink and come back green | "Pods: healthy. Restart: no change." | Every pod is running. The logs show no errors. Someone restarts everything anyway, and nothing changes. | كل الحجيرات تعمل، والسجلات خالية من الأخطاء. أعاد أحدهم تشغيل كل شيء، ولم يتغيّر شيء. |
| 3 | 18-30 | A request token travels left to right towards four gates labelled DNS, TCP, TLS, HTTP | Road with four toll gates | "A request crosses 4 hops" | Every request crosses the same chain: DNS finds the address, TCP opens a connection, TLS proves who the server is, HTTP carries the request. | كل طلب يعبر السلسلة نفسها: DNS يجد العنوان، وTCP يفتح الاتصال، وTLS يثبت هوية الخادم، وHTTP يحمل الطلب. |
| 4 | 30-42 | Each gate shows its tool: dig, nc, openssl, curl -v | A magnifying glass stamps each gate with its tool name | "One hop. One tool." | Each hop has its own test: dig, nc, openssl, then curl -v. | لكل محطة أداة تختبرها: dig ثم nc ثم openssl ثم curl -v. |
| 5 | 42-55 | Token passes DNS (green), TCP (green), stops at TLS; gate turns red | Red gate flashes; terminal text appears | "certificate has expired" | One `curl -v` stops at the TLS handshake: certificate has expired. Renewed by hand once a year, by someone who'd moved teams. | أمر curl -v واحد توقّف عند مصافحة TLS: انتهت صلاحية الشهادة. كانت تُجدَّد يدويًا مرة في السنة، ومن كان يجدّدها انتقل إلى فريق آخر. |
| 6 | 55-65 | Split: healthy servers on one side, broken path on the other | Path between user and servers dissolves | "The app was fine. The path wasn't." | The application was healthy the whole time. Customers simply couldn't reach it. And a restart destroys evidence without fixing a certificate. | كان التطبيق سليمًا طوال الوقت، لكن العملاء لم يستطيعوا الوصول إليه. وإعادة التشغيل تمحو الأدلة ولا تصلح شهادة. |
| 7 | 65-75 | Closing card with the four gates in a row | Gates light up in order | "When it's down: walk the chain in order." | When it's down, don't guess. Walk the chain, in order. Open lesson 1.1 to build the script that does it for you. | حين يتعطّل شيء، لا تخمّن. امشِ على السلسلة بالترتيب. افتح الدرس 1.1 لتكتب السكربت الذي يفعل ذلك عنك. |

**Closing takeaway:** Walk DNS, TCP, TLS, HTTP in order, testing each hop with its own tool, before changing anything.

**Call to action:** Open lesson 1.1 and do the walk-the-chain script exercise.

**Re-check before production:** The Najm scene is fictional, so label it as a scenario. If the optional Facebook 4 October 2021 beat is added (about six hours; DNS routes withdrawn), confirm it against Meta's engineering posts. Make sure the on-screen `curl` error wording matches real output.
