# Storyboard: Cloud & DevOps: Zero to Hero, lesson 4.2

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 3 of 3 for this course.** It pairs a well-sourced real incident (CrowdStrike, July 2024, about 8.5 million Windows devices) with one quotable rule and one mechanism, a canary that is judged by numbers and rolls back on its own.

## Never everyone at once

**Why this lesson:** One rule ('A change that reaches everyone at once can fail for everyone at once') and one mechanism (the canary dial) that can be shown in under 90 seconds.

**Target viewer:** A developer or new platform engineer whose team still deploys to all servers at once.

**Length:** about 85 seconds.

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-12 | A world map of dots; a single update arrow hits all at once and they turn red | Wave of red sweeping the map; icons of planes and hospitals | "19 July 2024" | On 19 July 2024, one content update for CrowdStrike's Falcon sensor reached Windows hosts everywhere at once. | في 19 يوليو 2024، وصل تحديث محتوى واحد لمستشعر Falcon من CrowdStrike إلى أجهزة Windows في كل مكان دفعة واحدة. |
| 2 | 12-22 | Counter climbs to ~8.5 million | Odometer spin | "~8.5 million devices" | Microsoft estimated about 8.5 million devices crashed. Flights, hospitals and banks were disrupted. | قدّرت Microsoft أن نحو 8.5 مليون جهاز تعطّل، فتأثّرت رحلات الطيران والمستشفيات والبنوك. |
| 3 | 22-32 | Rewind effect; the same update now passes through a dial | Tape rewinds; a big dial labelled 'traffic' appears | "What if it went to 5% first?" | CrowdStrike's own review said this content hadn't been rolled out in stages. Rewind. Send the change through a dial instead. | مراجعة CrowdStrike نفسها قالت إن هذا المحتوى لم يُطرح على مراحل. لنرجع إلى الوراء ونمرّر التغيير عبر مؤشّر تدريجي. |
| 4 | 32-46 | Bank scene: Payments service; dial set to 5%; two side-by-side graphs, old vs new | Graph lines drawing live | "Canary: 5% of traffic" | At Najm Bank, Maha's rule for the next Payments release: send 5% of traffic to the new version first and judge it by numbers. | في بنك نجم، قاعدة مها لإصدار خدمة المدفوعات القادم: 5% فقط من الحركة تذهب إلى الإصدار الجديد أولًا، والحكم للأرقام. |
| 5 | 46-60 | The new version's error line climbs past a threshold line; the dial snaps back to 0% | Needle snaps back with a click; green restored | "Bad numbers, automatic rollback" | If the new version's errors cross the line, the dial snaps back to zero on its own. No one has to wake up and decide. | إذا تجاوزت أخطاء الإصدار الجديد الحد، يعود المؤشّر إلى الصفر تلقائيًا، دون أن يضطر أحد للاستيقاظ واتخاذ القرار. |
| 6 | 60-72 | Flashback: the old Najm incident: 3% of transfers failing for 40 minutes, then a 15-minute rollback | Timeline bar filling slowly in amber | "Last quarter: 40 min unnoticed + 15 min rollback" | Last quarter, a release hit every pod in four minutes. Errors on 3% of transfers stayed under the alert for 40 minutes, and the unpractised rollback took 15 more. | في الربع الماضي، وصل إصدار إلى كل الحجيرات خلال أربع دقائق. بقيت الأخطاء في 3% من التحويلات تحت عتبة التنبيه 40 دقيقة، واستغرق التراجع غير المتدرَّب عليه 15 دقيقة أخرى. |
| 7 | 72-85 | Closing card with the quote | Text types on | "A change that reaches everyone at once can fail for everyone at once." | A change that reaches everyone at once can fail for everyone at once. Open lesson 4.2 to build a canary that rolls itself back. | التغيير الذي يصل إلى الجميع دفعة واحدة قد يفشل عند الجميع دفعة واحدة. افتح الدرس 4.2 لتبني إصدار كناري يتراجع من تلقاء نفسه. |

**Closing takeaway:** Stage every change, configuration and content included, and let numbers trigger the rollback.

**Call to action:** Open lesson 4.2 and do the Argo Rollouts canary exercise.

**Re-check before production:** Verify the 8.5 million estimate and CrowdStrike's staged-rollout commitments against the primary RCA PDF, not the homepage that 04-cicd.md:617 currently cites. The Najm numbers (5%, 3%, 40 min, 15 min, four minutes) are fictional scenario figures, so label them as an example. Keep the five-strategy table off screen.
