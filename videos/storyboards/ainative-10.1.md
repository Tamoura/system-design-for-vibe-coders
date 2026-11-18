# Storyboard: A Practical Guide to Becoming an AI-Native Engineer, lesson 10.1

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 3 of 3 for this course.** Four green branches merge into a red main, and a simple queue model (N ≤ A ÷ R) shows why one reviewer caps the number of streams. It is a real mechanism that works better shown than told, and it holds for any tool (ainative/modules/10-parallel.md:126).

## You are the integration point (lesson 10.1)

**Why this lesson:** The scene of four green branches merging into a red main, plus the review-queue model, makes 'parallel agents save waiting, not reading' obvious. The lesson is honest that no cited study measures a speed-up (ainative/modules/10-parallel.md:27).
**Target viewer:** An engineer tempted to run several agents at once.
**Length:** 85 seconds

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-10 | Four agent windows, four tickets | Four progress bars race; each ends with a green tick | 4 sessions. 4 green branches. | Friday: Lujain starts four agent sessions on four tickets she believes are independent. By five, every branch is green. | يوم الجمعة تشغّل لجين أربع جلسات وكيل على أربع تذاكر تظنّها مستقلة. بحلول الخامسة كل الفروع خضراء. |
| 2 | 10-22 | Four branch lines merge into main | At the merge point the line flashes red: CI fails | Each right alone. Wrong together. | She merges them, and CI goes red. One ticket changed how Arabic amounts are written; another added a test expecting the old text. | تدمجها، فيحمرّ التكامل المستمر. إحدى التذاكر غيّرت طريقة كتابة المبالغ بالعربية، وأخرى أضافت اختبارًا يتوقع النص القديم. |
| 3 | 22-32 | Two bar labels: 'typing saved 4 h' and 'integration 5 h' | The integration bar grows past the savings bar | "The agents did their jobs. Nobody did yours." | Four hours of typing saved, five hours of integration. Tariq: "The agents did their jobs. Nobody did yours." | وفّرت أربع ساعات من الكتابة، وأنفقت خمس ساعات في الدمج. يقول طارق: «أدّت الوكلاء عملها، ولم يؤدِّ أحد عملك». |
| 4 | 32-48 | One reviewer at a desk, a conveyor belt of results | Results arrive every A ÷ N minutes; the reviewer takes R minutes each | A = agent minutes per result · R = your review minutes · N = streams | While you review one result, the other streams keep working. Each agent needs A minutes per result; you need R minutes to check one. | بينما تراجع نتيجة واحدة تواصل المسارات الأخرى العمل. يحتاج كل وكيل A دقيقة لكل نتيجة، وتحتاج أنت R دقيقة لفحصها. |
| 5 | 48-62 | The belt with N = 2, then N = 4 (A = 20, R = 10) | At N = 2 the queue stays level; at N = 4 boxes pile up and spill | Keep up while N ≤ A ÷ R | You keep up only while N is at most A divided by R. With twenty minutes per result and ten to review, that is two streams. Four, and the queue overflows. | تواكب ما دام N لا يتجاوز A مقسومًا على R. عشرون دقيقة لكل نتيجة وعشر للمراجعة تعني مسارين. أربعة، فيفيض الطابور. |
| 6 | 62-72 | A money-logic task: A = 20, R = 30 | The formula gives less than one; the belt collapses into a single line | Under 1: go serial. | For money logic with a second reviewer, the answer is under one stream. Go serial. | وفي منطق الأموال مع مراجع ثانٍ يكون الناتج أقل من مسار واحد. اعمل بالتتابع. |
| 7 | 72-85 | The lesson card | Four streams fold into two, both feeding one reviewer marked 'you' | You are the integration point. Test after every merge. Open lesson 10.1. | No study we cite measures a speed-up from running several agents at once. You are the integration point: test after every merge. Open lesson 10.1. | لا تقيس أي دراسة نستشهد بها تسريعًا من تشغيل عدة وكلاء معًا. أنت نقطة الدمج: اختبر بعد كل دمج. افتح الدرس 10.1. |

**Closing takeaway:** Set your stream count from your measured review minutes, not from how many agents you can start.
**Call to action:** Open lesson 10.1.
**Re-check before production:** All numbers (A, R, the 4 h and 5 h) are fictional examples from the lesson, so label them. If METR's February 2026 note or the DORA 2024/2025 stability findings are cited, keep the lesson's framing (survey associations; METR says its time measurements are unreliable with several agents). Do not show product commands such as `claude --worktree` on screen, because they may change.
