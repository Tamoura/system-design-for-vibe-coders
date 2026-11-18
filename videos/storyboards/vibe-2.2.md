# Storyboard: System Design for Vibe Coders, lesson 2.2

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 3 of 3 for this course.** A haunting hook (deleted files reappear), a mechanism that fits a loop animation (a pull-through bridge still switched on), and a quotable takeaway that works with any vendor (modules/02-data-storage-backups/module.md:172-197).

## The Files That Came Back From the Dead

**Why this lesson:** a mystery with a twist (the delete worked every time), one loop that is easy to animate, and a sentence that applies to every migration.
**Target viewer:** builders moving storage, a database or a host from one provider to another.
**Length:** about 70 seconds.

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-10 | An admin deletes a file; a check mark says 'gone' | A file icon dissolves | Deleted. Confirmed. | An admin deleted a file from storage. Checked: gone. | حذف المسؤول ملفًا من التخزين، وتحقّق: لقد اختفى. |
| 2 | 10-20 | A calendar flips one or two days; the file is back | The file reappears with a ghostly shimmer | ...it came back. | A day or two later, it was back. Delete it again, and it returns again. | وبعد يوم أو يومين عاد من جديد. احذفه مرة أخرى فيعود مرة أخرى. |
| 3 | 20-30 | Wrong theories cross themselves out: 'delete code?', 'stale cache?', 'two admins?' | Sticky notes get crossed out | It wasn't the delete code. | Everyone suspected the delete code. But the delete worked perfectly, every time. | شكّ الجميع في كود الحذف، لكن الحذف كان يعمل بإتقان في كل مرة. |
| 4 | 30-44 | Two buckets: old (GCS) and new (R2), joined by a glowing bridge | A bridge between two warehouses | The migration 'finished'... the bridge didn't. | Storage had been moved to a new provider. To make the move seamless, a bridge fetched any missing file from the old bucket, and it was still switched on. | كان التخزين قد نُقل إلى مزوّد جديد، ولجعل النقل سلسًا فُعّل جسر يجلب أي ملف مفقود من المخزن القديم، وظلّ هذا الجسر يعمل. |
| 5 | 44-56 | Loop: delete in new -> request finds it missing -> bridge pulls from old -> file reappears | A circular arrow animation repeats twice | Delete -> missing -> pull back -> resurrect | Delete in the new store, the next request finds it missing, the bridge pulls it back from the old one, and the file rises again. | يُحذف من المخزن الجديد، فيجده الطلب التالي مفقودًا، فيستعيده الجسر من القديم، ويعود الملف إلى الحياة. |
| 6 | 56-64 | The file is deleted from both buckets; a switch flips the bridge OFF; the loop stops | A big switch clicks off and the bridge goes dark | Delete from both. Turn the bridge off. | The fix: delete from both, then switch the bridge off, and end the dual-source phase on purpose. | الحل: الحذف من المخزنين، ثم إيقاف الجسر، وإنهاء مرحلة المصدرين عن قصد. |
| 7 | 64-72 | Title card | The old warehouse dims fully | Done = the old system can no longer act. | A migration isn't done when the new system works. It's done when the old system can no longer act. Open lesson 2.2. | لا تنتهي الهجرة حين يعمل النظام الجديد، بل حين يعجز النظام القديم عن الفعل. افتح الدرس 2.2. |

**Closing takeaway:** A migration isn't done when the new system works. It's done when the old system can no longer act.
**Call to action:** Open lesson 2.2 and write a migration runbook with an exit criterion for every phase.

**Re-check before production:** name the vendors (GCS, R2, Sippy) once at most so the video does not date. Confirm the 'a day or two later' timing and that the fix was 'delete from both, then turn the bridge off' against module.md:179 and :194-197. This is the author's own incident, so do not attach a company name.
