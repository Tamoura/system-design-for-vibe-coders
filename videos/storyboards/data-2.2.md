# Storyboard: Data Engineering & Analytics: Zero to Hero, lesson 2.2

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 3 of 3 for this course.** Two precise bugs lead to one memorable rule (02-pipelines.md:298). The doubled 14 September bar is easy to animate, and the outcome is backed by the three-reruns exercise (line 523).

## The Retry That Doubled a Day

**Why this lesson:** It shows a 'successful' retry silently corrupting finance numbers, and ends on one rule every data engineer should know by heart.
**Target viewer:** Software engineers and graduates writing their first scheduled pipelines.
**Length:** 80 s

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-10 | A finance bar chart of daily card spend; the 14 September bar is twice as tall | The bar grows past the others; a red question mark appears | 14 September: 2× spend? | The finance dashboard shows card spend for 14 September at almost exactly twice the usual amount. | تُظهر لوحة المالية إنفاق البطاقات ليوم 14 سبتمبر بضعف المعتاد تقريبًا. |
| 2 | 10-24 | A task box 'append yesterday's rows' writes into a warehouse; the insert commits | A wire from the warehouse back to the orchestrator snaps after the commit tick | Insert committed. Acknowledgement lost. | The nightly task appended rows. The insert committed, but the connection dropped before the orchestrator heard back. | أضاف المهمة الليلية الصفوف. تم تثبيت الإدخال، لكن الاتصال انقطع قبل أن يصل الرد إلى المنسّق. |
| 3 | 24-34 | The orchestrator marks the task failed, then retries | A 'retry' arrow fires; a second identical block of rows stacks on the first | Retry = append again | So it marked the task failed and retried it, and the same day was appended a second time. | فاعتبرها فاشلة وأعاد تشغيلها، فأُضيف اليوم نفسه مرة ثانية. |
| 4 | 34-48 | A calendar: Saturday's load fails; a hand presses 'rerun' on Monday | The query `CURRENT_DATE - 1` resolves to Sunday; the Saturday slot stays empty | CURRENT_DATE - 1 on Monday = Sunday | A second, quieter bug: a failed Saturday load rerun by hand on Monday loaded Sunday again. Saturday never arrived. | وخطأ ثانٍ أهدأ: إعادة تشغيل حمل السبت يدويًا يوم الاثنين حمّلت الأحد مرة أخرى، ولم يصل السبت أبدًا. |
| 5 | 48-62 | The fixed task: receives a data interval, then deletes that day and inserts it in one transaction | Rewind; replay three reruns; the 14 September bar stays at the same height each time | Fixed data interval · delete + insert | The fix: the orchestrator hands the task its data interval, and the task replaces that day as a whole instead of appending. | الحل: يسلّم المنسّق المهمة فترة بياناتها (data interval)، فتستبدل المهمة ذلك اليوم كاملًا بدل الإضافة إليه. |
| 6 | 62-72 | Three rerun counters tick 1, 2, 3; the total stays the same | A checkmark stamps the stable bar | Same result, once or five times | Run it once or five times: the result is the same. That is idempotency. | شغّلها مرة أو خمس مرات، تبقى النتيجة نفسها. هذه هي قابلية التكرار الآمن (idempotency). |
| 7 | 72-80 | Faisal's rule on a card | The text holds | Every task must be safe to run twice, for any date, at any time. | Every task must be safe to run twice, for any date, at any time. Lesson 2.2. | يجب أن تكون كل مهمة آمنة عند تشغيلها مرتين، لأي تاريخ، وفي أي وقت. الدرس 2.2. |

**Closing takeaway:** A task that appends, or picks its own 'today', breaks on the first retry or backfill. Work on a fixed data interval and replace it.
**Call to action:** Open lesson 2.2 and prove it yourself: run both versions three times and compare the day's totals.

**Re-check before production:**
- Show only the Airflow terms the lesson uses (data_interval_start/end, 02-pipelines.md:397-398).
- If an Airflow schedule appears on screen, apply the Airflow 3 cron-interval caveat (02-pipelines.md:362).
- Check that the Arabic narration matches the wording in 02-pipelines.ar.md, and use 'تستطيع أن' in any outcome line that is read aloud.
