# Storyboard: Data Engineering & Analytics: Zero to Hero, lesson 1.1

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 2 of 3 for this course.** Join fan-out is a highly visual mechanism tied to the grain rule that runs through the whole course (01-sql-modelling.md:35). The corrected CTE version (line 112) gives a clean before-and-after.

## Why Your Customer Count Is 40 Times Too Big

**Why this lesson:** Watching rows multiply through a join makes an invisible bug obvious, and the fix (state the grain, aggregate before joining) is a rule that will not date.
**Target viewer:** Graduates with some SQL and analysts who write reporting queries.
**Length:** 70 s

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-8 | Kareem's chat bubble | The question types itself out | "How many retail customers were active in September, and how much did they spend?" | Kareem asks a simple question for the monthly retail review. | يطرح كريم سؤالًا بسيطًا لمراجعة التجزئة الشهرية. |
| 2 | 8-18 | Huda's six-line query: customers JOIN accounts JOIN transactions, COUNT(*) | Code types fast; a 'done in 10 minutes' timer stops | Written in 10 minutes | Huda writes the query in ten minutes. It runs. It returns a number. | تكتب هدى الاستعلام في عشر دقائق. يعمل ويعيد رقمًا. |
| 3 | 18-32 | One customer card joins to account rows, then to 40 transaction rows | Rows clone and cascade downward; a COUNT(*) ticker climbs from 1 to 40 | 1 customer → 40 rows | But one customer with 40 card payments becomes 40 rows, and is counted 40 times. | لكن العميل الذي لديه 40 دفعة بالبطاقة يصبح 40 صفًا، فيُحسب 40 مرة. |
| 4 | 32-42 | Green salary-credit rows mixed in with red spend rows | Green rows flash, labelled 'credit' | Spend includes salary credits | And "spend" quietly includes incoming salary, because nobody said debits only. | و«الإنفاق» يشمل الرواتب الواردة بصمت، لأن أحدًا لم يقل: الخصومات فقط. |
| 5 | 42-52 | A label 'grain' pinned to each table: one row per customer / account / transaction | Each table gets a tag; the mismatched join glows red | Grain = what one row means | The database did exactly what it was told. The question had no grain: what one row is supposed to mean. | نفّذت قاعدة البيانات ما طُلب منها بالضبط. المشكلة أن السؤال بلا حبيبية (grain): ماذا يمثل الصف الواحد. |
| 6 | 52-64 | The CTE version: September debits, then per_customer, then the join to customers | The 40 rows collapse into 1 row per customer; the ticker snaps back to 1; credits peel away | Collapse to one row per customer, then join | Filter to debits, collapse to one row per customer, and only then join. Each step states its grain. | صفِّ الخصومات، واختصرها إلى صف واحد لكل عميل، ثم اربط بعدها فقط. كل خطوة تعلن حبيبيتها. |
| 7 | 64-70 | Title card | Fade | Know your grain before you join | Know your grain before you join. Lesson 1.1. | اعرف الحبيبية قبل أن تربط. الدرس 1.1. |

**Closing takeaway:** Joining a one-to-many relationship before aggregating silently inflates every COUNT and SUM. Aggregate to the grain you want, then join.
**Call to action:** Open lesson 1.1, recreate the mistake on purpose, and explain the exact ratio.

**Re-check before production:**
- Use the query exactly as the lesson prints it (01-sql-modelling.md:24-33 and the corrected CTE ending at line 112), including the Doha +03 timestamps.
- The Arabic term for 'grain' is not confirmed in this audit. Take it from 01-sql-modelling.ar.md so narration matches the lesson.
