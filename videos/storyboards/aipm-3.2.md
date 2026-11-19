# Storyboard: AI Product Management: Zero to Hero, lesson 3.2

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 3 of 3 for this course.** A self-reinforcing blind spot is hard to grasp from text and easy to grasp from an animation. The Smart Alerts story (aipm/modules/03-data.md:241) and the holdout remedy (03-data.md:284, :352) give it a durable, fictional shape that will not date.

## The flashlight that only sees what it already lit (lesson 3.2)

**Why this lesson:** it makes the 'degenerate feedback loop' visible, a risk that most PMs never see until it bites (03-data.md:241, :275).
**Target viewer:** a PM or sponsor who has been told the product 'learns from user feedback'.
**Length:** about 70 s.

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-8 | A slide titled 'Data flywheel' with a spinning wheel | The wheel spins and then wobbles | 'It gets smarter every week' | Every AI team claims its product learns from feedback. | كل فريق ذكاء اصطناعي يقول إن منتجه يتعلّم من ملاحظات المستخدمين. |
| 2 | 8-20 | A dark field of transactions; a flashlight beam labelled 'Fraud model' | The beam lights some transactions; a phone pops 'Yes, this was me' | Only flagged cases get a label | Smart Alerts learns from customer replies, but customers only reply to transactions the model flagged. | يتعلّم نظام التنبيهات الذكية من ردود العملاء، لكن العملاء لا يردّون إلا على العمليات التي نبّه عليها النموذج. |
| 3 | 20-34 | Calendar flips month 1 to 6; beam narrows and sharpens | The lit circle tightens and brightens | Month 6: very good at what it already flags | Over six months it gets very good at the kinds of fraud it already flagged. | خلال ستة أشهر يصبح بارعًا جدًا في أنواع الاحتيال التي كان ينبّه عليها أصلًا. |
| 4 | 34-46 | In the dark area, a new red cluster grows | Red dots multiply outside the beam, unseen | New fraud pattern: no alerts, no labels | Meanwhile a new pattern grows in the dark. It never triggers an alert, so it never produces a label. | وفي الظلام ينمو نمط احتيال جديد. لا يُطلق أي تنبيه، فلا ينتج أي تصنيف. |
| 5 | 46-58 | A second, small beam sweeps random spots | Random spots light up; one lands on the red cluster | Fix: review a small random sample the model did not flag | The fix: review a small random sample of transactions the model did not flag, so some labels come from outside its own choices. | والعلاج: مراجعة عيّنة عشوائية صغيرة من العمليات التي لم ينبّه عليها النموذج، لتأتي بعض التصنيفات من خارج اختياراته. |
| 6 | 58-64 | Cost tag on the sample | A scale: analyst time vs. blind spot | It costs analyst time, so agree the size | It costs analyst time, so the PM agrees its size with fraud operations. | وهذا يكلّف وقت المحلّلين، لذا يتّفق مدير المنتج مع فريق عمليات الاحتيال على حجمها. |
| 7 | 64-70 | End card | Text builds up | When the product decides what gets labelled, it learns its own blind spots. | If your product decides what gets labelled, budget for a holdout sample. | إذا كان منتجك هو من يقرّر ما يُصنَّف، فخصّص ميزانية لعيّنة مراقبة. |

**Closing takeaway:** a learning loop needs labels from outside the model's own choices.
**Call to action:** 'Open lesson 3.2, Feedback loops, and write a loop spec with one holdout signal.'

**Re-check before production:** the '0.5% random sample of unflagged transactions' figure (03-data.md:352) is illustrative, so either keep it off screen or label it. Use the fixed Arabic term for holdout sample from the .ar file. The Sculley et al. (2015) citation should stay in the text, not the video.
