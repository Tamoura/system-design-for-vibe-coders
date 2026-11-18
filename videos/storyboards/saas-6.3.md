# Storyboard: SaaS Building Blocks, lesson 6.3

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 1 of 3 for this course.** The course's strongest hook: a real, documented incident with a clear visual mechanism (eight servers, one stale, a reused flag), one takeaway, and a second built-in visual for the fix (0-99 hash buckets, 06-product-growth.md:611).

## The $440 Million Switch (lesson 6.3, Feature flags and experiments)

**Why this lesson:** a real incident with one visible mechanism and one rule, plus a clean visual for the fix.
**Target viewer:** a junior developer who ships code but has never run a staged rollout.
**Length:** about 75 s.

| # | Seconds | On screen | Visual / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-8 | Date card, then a trading floor drawn in line art | Clock starts ticking | 1 August 2012 | "On the first of August 2012, Knight Capital deployed new trading code." | "في الأول من أغسطس 2012، نشرت شركة Knight Capital شيفرة تداول جديدة." |
| 2 | 8-20 | Eight server icons; seven turn green, one stays grey | Deploy arrows reach seven servers and miss one | 1 of 8 servers missed the update | "One of eight servers didn't get the new code." | "لكن خادمًا واحدًا من ثمانية لم تصله الشيفرة الجديدة." |
| 3 | 20-32 | A toggle labelled 'Power Peg' with a dusty label | Toggle flips on; the grey server wakes up running old logic | Old flag. New meaning. | "The new code reused an old flag that once switched on a dead feature called Power Peg. When the flag was turned on, that one server ran the old logic against the live market." | "أعادت الشيفرة الجديدة استخدام مفتاح قديم كان يشغّل ميزة ميتة اسمها Power Peg. وحين شُغّل المفتاح، نفّذ ذلك الخادم المنطق القديم على السوق الحقيقية." |
| 4 | 32-42 | A counter racing upward beside a 45-minute timer | Money drains from a bar | ~45 minutes. ~$440 million. | "In about forty-five minutes Knight lost roughly 440 million dollars, and the firm didn't survive on its own." | "خلال نحو خمس وأربعين دقيقة خسرت الشركة قرابة 440 مليون دولار، ولم تنجُ كشركة مستقلة." |
| 5 | 42-52 | Split card: 'Deploy' (code on servers) and 'Release' (users run it) | The flag drawn as an `if` with a remote control | Deploy ≠ Release | "A feature flag is a runtime if-statement you control from outside the code. That's its power, and its danger." | "مفتاح الميزة شرط يُقيَّم أثناء التشغيل وتتحكم فيه من خارج الشيفرة. هنا تكمن قوته، وهنا يكمن خطره." |
| 6 | 52-66 | A strip of 100 buckets (0-99); org dots hashed into fixed buckets | Highlight moves from 5% to 20%; the first 5% stay lit | hash(flag + org) → 0-99 | "Roll out by hashing the flag and the org ID into a bucket from 0 to 99. The same org always lands in the same bucket, so going from 5% to 20% keeps the first 5% in." | "عند الطرح التدريجي، حوّل اسم المفتاح ومعرّف المنظمة إلى رقم من 0 إلى 99. تقع المنظمة نفسها دائمًا في الخانة نفسها، فإذا رفعت النسبة من 5% إلى 20% بقيت الـ5% الأولى ضمنها." |
| 7 | 66-75 | Old flag card stamped 'Delete'; lesson title card | Card crumples into a bin | Never repurpose a flag. Delete dead ones. | "Never repurpose an old flag, and delete dead flags with their code. Open lesson 6.3 to build it in Beacon." | "لا تُعِد استخدام مفتاح قديم أبدًا، واحذف المفاتيح الميتة مع شيفرتها. افتح الدرس 6.3 لتبنيها في Beacon." |

**Closing takeaway:** never repurpose an old flag; delete dead flags along with their code.
**Call to action:** open lesson 6.3, Feature flags and experiments.

**Re-check before production:** the loss figure. The lesson says 'roughly $440 million', but the SEC's 2013 order reportedly says more than $460 million ($440M was Knight's early estimate), so update the lesson and use the corrected figure on screen. Also drop the 'ever recorded' superlative.
