# Storyboard: A Practical Guide to Becoming an AI-Native Engineer, lesson 3.1

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 2 of 3 for this course.** A precise, numeric image of why a spec matters: the ticket 'Raise it to 3,000' leaves the boundary unanswered, and the agent builds a guess as confidently as the right answer (ainative/modules/03-specs.md:25). It is beginner level, durable and tool-independent.

## Refused by one cent (lesson 3.1)

**Why this lesson:** It turns 'write a spec' into a concrete moment: a limit that refuses 3,000.00 by one cent, then a boundary table that settles it (ainative/modules/03-specs.md:25 and the table that follows).
**Target viewer:** A beginner who hands tickets straight to an agent.
**Length:** 70 seconds

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-8 | Ticket REMIT-288 as a sticky note | The note pins itself to a board | "Raise it to 3,000." | A one-line ticket: customers on the basic tier keep hitting their daily limit. Raise it to 3,000. | تذكرة من سطر واحد: عملاء الفئة الأساسية يصطدمون بحدّهم اليومي. ارفعوه إلى 3,000. |
| 2 | 8-18 | The agent's diff: one line in limits.py, six edited tests, all green | A tiny diff and a column of green ticks | 1 line. 6 tests edited. All green. | The agent changes one line and edits six tests. Everything passes. | يغيّر الوكيل سطرًا واحدًا ويعدّل ستة اختبارات. كل شيء ينجح. |
| 3 | 18-32 | Nada's review questions appear one by one around the note | Question marks orbit the ticket | Monthly 8,000.00? Exactly 3,000.00? Which tests should change? | In review Nada asks: does the monthly limit of 8,000 stay? Is exactly 3,000.00 allowed? Which of those six tests were meant to change? | في المراجعة تسأل ندى: هل يبقى الحد الشهري 8,000؟ هل يُسمح بـ 3,000.00 بالضبط؟ وأيّ الاختبارات الستة كان يُفترض أن يتغيّر؟ |
| 4 | 32-44 | A counter ticking up: 2,999.98 … 2,999.99 … 3,000.00 | At 3,000.00 a red 'REFUSED' gate slams down | Refused by one cent. | Leave the boundary unanswered and the agent guesses, as confidently as it would build the right answer. One possible result: a limit that refuses 3,000.00 by one cent. | إذا تُرك سؤال الحدّ بلا جواب يخمّن الوكيل، وبالثقة نفسها التي يبني بها الصواب. وقد تكون النتيجة حدًّا يرفض 3,000.00 بفارق سنت واحد. |
| 5 | 44-58 | The behaviour table from the spec | Rows snap into place: 3,000.00 allowed; 3,000.01 refused; 2,500 + 500.01 refused; monthly 7,500 + 600 refused | Behaviour pins the numbers. Decisions pin the meaning. | A spec answers those questions before the build: worked examples pin the numbers, and written decisions pin the meaning. | المواصفة تجيب عن هذه الأسئلة قبل البناء: الأمثلة المحلولة تثبّت الأرقام، والقرارات المكتوبة تثبّت المعنى. |
| 6 | 58-70 | The lesson card | The sticky note transforms into a one-page spec | A ticket states a wish. A spec says what done means. Open lesson 3.1. | A ticket states a wish. A spec says what 'done' means, so the agent can build from it and you can verify against it. Open lesson 3.1. | التذكرة تعبّر عن رغبة، والمواصفة تحدّد معنى «انتهى»، فيبني منها الوكيل وتتحقق أنت على أساسها. افتح الدرس 3.1. |

**Closing takeaway:** Answer the edge questions before the agent guesses.
**Call to action:** Open lesson 3.1.
**Re-check before production:** The scene is constructed, so label it fictional. If the Stack Overflow 2025 'almost right, but not quite' finding is cited, keep it marked as self-reported survey data. Use the table values exactly as the lesson states them (daily 3,000.00, monthly 8,000.00). Do not imply that the one-cent refusal actually happened in the REMIT-288 diff: the lesson presents it as what an unanswered boundary question produces.
