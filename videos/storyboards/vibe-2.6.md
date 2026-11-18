# Storyboard: System Design for Vibe Coders, lesson 2.6

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 1 of 3 for this course.** A real incident with one mechanism that is easy to animate. The lesson already contains the sequence diagram (modules/02-data-storage-backups/module.md:863-876), and the takeaway, 'you tested alone', applies to every vibe coder.

## Two Clicks at Once: the file that vanished

**Why this lesson:** one real incident, one mechanism (a read-modify-write race), and a storyboard that already exists as a sequence diagram. The takeaway does not depend on any vendor.
**Target viewer:** AI-first builders who test their app alone on their own laptop.
**Length:** about 75 seconds.

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-8 | An admin uploads files one at a time and a progress bar crawls | A clock spins fast; 114 file icons queue up | 114 files. One at a time. | An admin had to upload 114 files one by one, which took up to half an hour. | كان على المسؤول أن يرفع 114 ملفًا واحدًا تلو الآخر، في عملية تستغرق قرابة نصف ساعة. |
| 2 | 8-18 | Two files dropped together; the counter ends one short; no red error | A file icon quietly fades to nothing | Upload two at once... one disappears. | Upload two at once and a file silently disappears. No error, just a wrong count. | ارفع ملفين معًا فيختفي أحدهما بصمت، دون أي رسالة خطأ، فقط عدد ناقص. |
| 3 | 18-32 | One record card in the middle, Request A on the left, Request B on the right | Both tokens grab a copy of the card showing [x] | Both read: [x] | For each file, the server read the record, added the file to its list, and wrote it back. Both requests read the same list. | لكل ملف، كان الخادم يقرأ السجل، ويضيف الملف إلى قائمته، ثم يكتبه من جديد. والطلبان قرآ القائمة نفسها. |
| 4 | 32-46 | A writes [x, file1]; B then writes [x, file2] over it | B's card slams down on top of A's and file1 fades out | Last write wins. file1 is gone. | A writes its version, then B overwrites it with its own copy. Whoever writes last wins, and file1 is erased. | يكتب الطلب الأول نسخته، ثم يكتب الثاني فوقها نسخته هو. آخر من يكتب يفوز، ويُمحى الملف الأول. |
| 5 | 46-58 | A laptop with one request, then a busy server with many arrows | Single arrow vs a storm of arrows | You tested alone. | This is called a lost update. It never shows up in testing, because you tested alone. | يُسمّى هذا «التحديث الضائع»، ولا يظهر أبدًا في الاختبار، لأنك كنت تختبر وحدك. |
| 6 | 58-70 | Each file goes to its own storage slot, then one 'confirm' stamp | Separate lockers, then one atomic stamp | Separate keys. One atomic confirm. | The real fix: each file goes to its own key in storage, then one atomic confirm records them all together. | الحل الحقيقي: يُخزَّن كل ملف بمفتاح مستقل، ثم يسجّلها تأكيد ذرّي واحد معًا. |
| 7 | 70-78 | Title card | 20 arrows hit at once, all green | Test many at once. | The test that catches this bug is the one you never run: many at once. Open lesson 2.6 to run it. | الاختبار الذي يكشف هذا الخطأ هو الذي لا تجريه أبدًا: طلبات كثيرة في اللحظة نفسها. افتح الدرس 2.6 لتجريه. |

**Closing takeaway:** "It worked when I tested it" is guaranteed for this kind of bug, because the test that catches it is many requests at once.
**Call to action:** Open lesson 2.6, *Two Clicks at Once*, and run the 20-at-once test on your own app.

**Re-check before production:** the figures 114 files and 15-30 minutes (module.md:858); the claim that one atomic confirm was the actual fix (module.md:884-887). The incident is from the author's own platform, so do not attach a company name.
