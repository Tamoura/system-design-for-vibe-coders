# Storyboard: Digital Practice, lesson 4.3

> AI-drafted, not expert-reviewed. Written on 2026-11-22, after the course was drafted, not as part of its writing. Check every fact against the lesson (`dprac/modules/04-operate.md`) and its claims register (`academy/claims/dprac.md`) before production.

**Pick 1 of 3 for this course.** Qafila's first serious outage is the course's most dramatic moment, and it has a clock built in: a deploy at 11:50, orders vanishing, nobody in charge for over an hour, a restore from the 04:00 backup. A timeline that fills with red, then a review that turns "who ran this?" into conditions the team can fix, carries the whole lesson. Every time and figure comes from the lesson's own review.

## Two hours of lost orders, and the question that changed

**Lesson:** 4.3 Incidents, post-incident reviews and reliability targets
**Why this lesson:** It shows the three habits of the lesson (name a lead and restore first, review without blame, set a target in minutes) on one real-feeling morning, and the turn from "who ran this migration?" to "how could anyone have known?" is a strong emotional beat.
**Target viewer:** A new engineer, tester or support colleague who will soon carry an on-call phone or sit in their first post-incident review.
**Length:** about 85 seconds

## Scenes

**1. 0-10 s - A normal Tuesday deploy**
- On screen: A clock reads "Tuesday 11:50". A deploy bar fills with a small tag: "includes a database migration". Beside it, a staging database icon labelled "a few hundred test orders".
- Visual/animation: A green tick appears on staging; the deploy arrow moves on to production.
- On-screen text: "Qafila is fictional. All figures are illustrative, not benchmarks."
- VO (EN): "Tuesday, eleven fifty. Qafila's daily deploy includes a database migration: a script that moves orders into a new table. It worked in staging, which held a few hundred test orders."
- VO (AR): "يوم ثلاثاء، الساعة الحادية عشرة وخمسون دقيقة. يتضمّن النشر اليومي في قافلة ترحيلًا لقاعدة البيانات (database migration)، أي نصًا برمجيًا ينقل الطلبات إلى جدول جديد. وقد نجح في بيئة ما قبل الإنتاج، التي لم تحمل إلا بضع مئات من الطلبات التجريبية."

**2. 10-22 s - Orders disappear**
- On screen: Production. The migration bar stops halfway and cracks. Old order rows grey out ("unreadable"); new orders drop into a second table that the app does not look at.
- Visual/animation: A merchant's phone shows an order list; new orders blink in and vanish. A courier's phone shows an offer, then "order not found".
- On-screen text: "Failed halfway: old history unreadable, new orders in a table the app did not read"
- VO (EN): "In production it failed halfway. Older order history became unreadable, and new orders went into the new table, which the app did not read yet. Merchants watched new orders disappear. Couriers got offers, then the orders vanished."
- VO (AR): "أما في الإنتاج ففشل في منتصف الطريق. صار سجل الطلبات القديمة غير قابل للقراءة، وذهبت الطلبات الجديدة إلى الجدول الجديد الذي لم يكن التطبيق يقرأ منه بعد. رأى التجّار طلباتهم الجديدة تختفي، وتلقّى المندوبون العروض ثم تلاشت الطلبات."

**3. 22-38 s - Nobody in charge**
- On screen: A timeline builds left to right: "11:58 first merchant message to support · 12:20 code rolled back, problem continues · 12:45 restore debated · 13:10 Faisal named incident lead; writes paused · 13:15 first message to merchants".
- Visual/animation: At 12:20 a "rollback" arrow bounces off the cracked migration. Between 12:20 and 13:10, two chat bubbles (Faisal, Maha) argue back and forth; a "Merchants told: nothing" counter stays at zero until 13:15.
- On-screen text: "Rolling back code does not undo a migration."
- VO (EN): "Rolling back the code did not undo the migration. Faisal and Maha argued in the channel about restoring from backup. Nobody was in charge, and nobody told merchants anything for the first hour. Only at ten past one was Faisal named incident lead, and writes paused."
- VO (AR): "التراجع عن الشيفرة لم يُلغِ الترحيل. تجادل فيصل ومها في القناة حول الاستعادة من النسخة الاحتياطية. لم يكن أحد يتولى القيادة، ولم يُبلَّغ التجّار بشيء في الساعة الأولى. ولم يُسمَّ فيصل قائدًا للحادثة (incident lead) إلا في الواحدة وعشر دقائق، وعندها أُوقفت الكتابة."

**4. 38-50 s - Recovered, then the wrong question**
- On screen: "about 14:00": a backup tape labelled "04:00" slides in and the grey rows turn back to normal; new orders are copied back from the second table and ticked against support's list. "14:30 closed". Then night falls on the chat window and one message appears: "who ran this migration?"
- Visual/animation: The timeline bar from 11:50 to about 14:00 is shaded red: "orders lost for about two hours".
- On-screen text: "All orders recovered the same day."
- VO (EN): "Around two o'clock the team restored the damaged history from that morning's four a.m. backup and copied the new orders back. All orders were recovered the same day. That evening, Maha's first message was: who ran this migration?"
- VO (AR): "نحو الساعة الثانية استعاد الفريق السجل التالف من النسخة الاحتياطية المأخوذة في الرابعة من صباح ذلك اليوم، وأعاد نسخ الطلبات الجديدة. واستُعيدت الطلبات كلها في اليوم نفسه. وفي ذلك المساء كانت أول رسالة من مها: «من شغّل هذا الترحيل؟»"

**5. 50-62 s - A blameless review**
- On screen: Three days later. Salma at a whiteboard titled "Post-incident review". A draft line, "Engineer did not test the migration properly", is crossed out and rewritten: "Staging held a few hundred orders, so the failure could not appear there."
- Visual/animation: More sticky notes join it under "Contributing factors": "changed the orders table in one step", "no alert for orders created but not visible", "no incident lead for over an hour", "restores never practised on production-sized data", "deployed in the busiest hour". Maha deletes her "who ran this?" message.
- On-screen text: "Ask how the system allowed it, not who to blame."
- VO (EN): "Salma ran the review three days later. Maha opened by withdrawing her message. The draft said the engineer did not test properly. Salma asked how anyone could have known with such small test data, and the line became a condition the team could fix. Five more joined it."
- VO (AR): "أدارت سلمى المراجعة بعد ثلاثة أيام، وافتتحتها مها بسحب رسالتها. قالت المسودة إن المهندس لم يختبر الترحيل جيدًا، فسألت سلمى: كيف كان لأحد أن يعرف ببيانات اختبار بهذا الصغر؟ فتحوّل السطر إلى عامل مساهم (contributing factor) يستطيع الفريق إصلاحه، وانضمّت إليه خمسة عوامل أخرى."

**6. 62-74 s - Lucky, and what 43 minutes means**
- On screen: A "Where we got lucky" card: "Only older orders were damaged; the 04:00 backup held them." A dashed alternative shows the morning's orders damaged instead: "daily backups: up to 24 hours of data at risk, about eight hours of orders could have been gone".
- Visual/animation: A month bar of "30 × 24 × 60 = 43,200 minutes" with a thin sliver marked "99.9% target → about 43 minutes". The red two-hour block is dropped on it and overflows the sliver almost three times.
- On-screen text: "A two-hour outage would have used a 99.9% monthly budget almost three times over."
- VO (EN): "They also wrote down where they got lucky. With daily backups, about eight hours of orders could have been gone. And the numbers behind a reliability target: ninety-nine point nine percent of a thirty-day month leaves about forty-three minutes. This outage would have used that budget almost three times over."
- VO (AR): "ودوّنوا أيضًا أين حالفهم الحظ: فمع نسخ احتياطية يومية كان يمكن أن تضيع طلبات نحو ثماني ساعات. ثم أرقام هدف الموثوقية: تسعة وتسعون فاصلة تسعة في المئة من شهر من ثلاثين يومًا تترك نحو ثلاث وأربعين دقيقة فقط، وهي ميزانية الخطأ (error budget). وكان هذا الانقطاع سيستهلكها ثلاث مرات تقريبًا."

**7. 74-85 s - Closing card**
- On screen: Five action cards, each with an owner and a date: "Expand-and-contract migrations, second reviewer (Faisal, two weeks)", "Point-in-time recovery, monthly restore drill (an engineer, month end)", "Alert: orders created vs orders visible (on-call, next week)", "Severity scale, roles card, merchant message (Salma, Friday)", "Measure order tracking every minute (Salma and Faisal, this month)".
- Visual/animation: A crossed-out card "Be more careful" falls off the board.
- On-screen text: "Fix the system, not the person."
- VO (EN): "Five actions, each with an owner and a date, and none of them 'be more careful'. Fix the system, not the person; people are part of the system you are fixing. Open lesson 4.3 and write your first post-incident review."
- VO (AR): "خمسة إجراءات، لكل منها مالك وموعد، وليس بينها «كونوا أكثر حذرًا». أصلح النظام، لا الشخص؛ فالناس جزء من النظام الذي تصلحه. افتح الدرس 4.3 واكتب أول مراجعة لما بعد الحادثة (post-incident review)."

## Takeaway and call to action
Takeaway: in an incident, name a lead and restore service first; afterwards, look for the conditions that allowed the failure and leave with a few owned, dated actions. CTA: open lesson 4.3 and write a blameless review from the lesson's courier-login timeline.

## Re-check before production
- Times, roles and actions come from the lesson's "Why it matters" and its review in "In practice at Qafila" (`dprac/modules/04-operate.md`): 11:50 deploy, 11:58 first merchant message, 12:20 rollback, 12:45 restore debated, 13:10 lead named and writes paused, 13:15 first message to merchants, about 14:00 restore from the 04:00 backup, 14:30 closed. "About two hours" is the lesson's wording (11:50 to about 14:00); do not show a more precise duration.
- Error budget recomputed from the lesson's table: 30 × 24 × 60 = 43,200 minutes; × 0.001 = 43.2, shown as "about 43". 120 ÷ 43.2 = 2.8, the lesson's "almost three times over". Keep "would have": the 99.9% monthly target for order tracking applies only from Growth on (lesson 7.3), so Qafila had no target at Traction when this happened.
- "About eight hours of orders" is the lesson's own figure for the case where the morning's orders had been damaged (daily backups, an RPO of up to 24 hours). Do not convert it into a number of orders.
- The fact sheet in `dprac/AUTHORING.md` fixes this outage as "orders lost for about two hours, recovered from backups" at Traction. Keep the stage and wording consistent with it.
- No outside-world claim is used. Leave out the GitLab 2017 outage, the PagerDuty incident commander line and the SRE book references; they are "reported" only (claims register dprac-04-008 to dprac-04-018) and are not needed for this story. Do not attribute SLO, SLI or error budget definitions to any source on screen.
- Keep the "Qafila is fictional; figures illustrative" label on screen for the whole of scene 1 and as a small footer in scenes 3 to 6. Merchants, couriers and the cast are fictional; show no real app, brand or cloud provider on screen.
