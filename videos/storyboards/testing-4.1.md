# Storyboard: Software Testing: Zero to Hero in the AI Era, lesson 4.1

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 2 of 3 for this course.** A verified dataset (mean 198 ms, p95 100 ms, p99 5 s) makes an ideal histogram reveal of why averages hide suffering customers. It is timeless statistics with a strong payday coda.

## The Average Lies (lesson 4.1)
**Why this lesson:** the arithmetic is checked and the reveal is purely visual: two 'healthy' numbers, then the one that is not.
**Target viewer:** developers and new testers who report 'average response time' as proof of performance.
**Length:** about 80 s

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-10 | A dashboard: '50 users, GET /health, average 4 ms: performance OK' | Thumbs-up stamp | Average 4 ms: 'performance OK'? | A first performance test: fifty virtual users calling a health check. Average four milliseconds. 'Performance OK.' | أول اختبار أداء: خمسون مستخدمًا افتراضيًا يستدعون فحص الصحة. المتوسط أربعة أجزاء من الألف من الثانية. «الأداء جيد». |
| 2 | 10-20 | 1,000 dots drop into a histogram: 980 short bars at 100 ms, 20 tall ones at 5 s | Raindrops filling columns | 1,000 requests | Now picture a thousand real requests. 980 take 100 milliseconds. Twenty take five seconds. | تخيّل الآن ألف طلب حقيقي: 980 منها تستغرق 100 جزء من الألف من الثانية، وعشرون تستغرق خمس ثوانٍ. |
| 3 | 20-32 | A 'mean' line at 198 ms and a 'p95' line at 100 ms, both green | Two gauges in the green zone | Mean 198 ms · p95 100 ms | The mean is 198 milliseconds. The 95th percentile is 100. Both look healthy. | المتوسط 198، والمئين الخامس والتسعون 100. كلاهما يبدو سليمًا. |
| 4 | 32-46 | A 'p99' line shoots up to 5,000 ms and turns red; two customer icons per second appear waiting with spinning wheels | Line rockets off the chart | p99 = 5,000 ms | But the 99th percentile is five seconds. At a hundred requests a second, that is two customers every second waiting five seconds. | لكن المئين التاسع والتسعين خمس ثوانٍ. وبمعدل مئة طلب في الثانية، يعني ذلك أن عميلين في كل ثانية ينتظران خمس ثوانٍ. |
| 5 | 46-58 | Code compare: 'Weak: assert mean < 200 ms' passes; 'Strong: assert p99 < 800 ms and error rate < 1%' fails on the same data | A weak test as a sleeping guard, a strong one as an alarm | Test percentiles, not averages | A test on the mean passes on this data. A test on p99 and error rate fails on the same data, and that failure is the point. | اختبار يعتمد على المتوسط ينجح على هذه البيانات، أما اختبار المئين 99 ونسبة الأخطاء فيفشل على البيانات نفسها، وهذا الفشل هو المطلوب. |
| 6 | 58-72 | A statement screen: '80 ms in QA' vs 'over 6 s on payday'; 20 rows vs thousands, with one query per row stacking up | Stack of queries towering over the QA one | 80 ms in QA, over 6 s on payday | And test with real data shapes. A statement screen answered in 80 ms in QA, but passed six seconds at p99 on payday: one query per row, 20 rows in QA, thousands in production. | واختبر بأحجام بيانات واقعية: شاشة كشف حساب استجابت في 80 جزءًا من الألف من الثانية في بيئة الاختبار، لكنها تجاوزت ست ثوانٍ يوم صرف الرواتب: استعلام لكل صف، و20 صفًا في الاختبار مقابل الآلاف في الإنتاج. |
| 7 | 72-80 | Motif tick and question | Tick pulses | Could this test fail? | Could your performance test fail? Open lesson 4.1 to write goals with percentiles. | هل يمكن لاختبار الأداء لديك أن يفشل؟ افتح الدرس 4.1 لتكتب أهدافًا بالمئينات. |

**Closing takeaway:** read the tail (p99) alongside throughput and errors; never trust the average. **Call to action:** open lesson 4.1.

**Re-check before production:** the numbers come from 04-qualities.md:42 and 24-25 (the payday story is an invented Najm scenario). Arabic VO should keep 'p95/p99' as on-screen labels; LCP/INP expansions are missing in the Arabic lesson (04-qualities.ar.md:194) but are not used here.
