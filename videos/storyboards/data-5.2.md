# Storyboard: Data Engineering & Analytics: Zero to Hero, lesson 5.2

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 1 of 3 for this course.** It has the course's strongest visual paradox (05-ml.md:309). One number becomes a counter-intuitive lesson, the follow-up about thresholds and review capacity gives a second beat, and the idea will not date.

## The 99.9% Accurate Model That Catches Nothing

**Why this lesson:** One number, 99.9%, flips from impressive to useless in ten seconds. The fix (precision, recall, a threshold chosen from cost and capacity) can be shown as a single slider.
**Target viewer:** Graduates and analysts moving into ML or fraud analytics, and bank staff who sit on risk committees.
**Length:** 75 s

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-8 | A risk-committee slide with a giant '99.9% accuracy' headline | The headline slams in; applause icons pop up, then freeze | "99.9% accuracy" | Huda presents her new fraud model with one headline: 99.9% accuracy. | تعرض هدى نموذج الاحتيال الجديد بعنوان واحد: دقة 99.9%. |
| 2 | 8-20 | A grid of 1,000 card-payment dots, one of them red | The camera pulls back to show the grid; the single red dot pulses | 1 in 1,000 is fraud | Fraud is rare. Say one transaction in a thousand is fraudulent. | الاحتيال نادر. لنفترض أن معاملة واحدة من كل ألف احتيالية. |
| 3 | 20-32 | A 'model' stamp labels every dot green, including the red one | The stamp sweeps across; an accuracy gauge fills to 99.9% while a 'fraud caught' counter stays at 0 | Accuracy 99.9% · Fraud caught: 0 | A "model" that calls everything genuine is 99.9% accurate, and catches nothing. | «نموذج» يصف كل شيء بأنه سليم تبلغ دقته 99.9%، ولا يكشف شيئًا. |
| 4 | 32-44 | A 2x2 confusion matrix builds from the dots | Dots slide into four cells: TP, FP, FN, TN | Precision = TP / (TP + FP) · Recall = TP / (TP + FN) | Ask two better questions. Of the alerts, how many were fraud? That's precision. Of the fraud, how much did we catch? That's recall. | اسأل سؤالين أفضل: من بين التنبيهات، كم منها كان احتيالًا؟ هذه هي الدقة (precision). ومن الاحتيال كله، كم كشفنا؟ هذا هو الاستدعاء (recall). |
| 5 | 44-58 | A threshold slider over a score axis | Sliding up: fewer alerts, the precision bar rises, the recall bar falls. Sliding down: the reverse | Not 0.5 by default | The model gives a score; the business picks the threshold. Raise it and you get fewer, cleaner alerts, but more fraud slips through. | النموذج يعطي درجة، والعمل يختار العتبة. ارفعها تحصل على تنبيهات أقل وأنظف، لكن يفلت احتيال أكثر. |
| 6 | 58-68 | Alerts flow into a fraud-operations queue with a fixed-width review door | At a low threshold the queue overflows the door | Costs + review capacity | So choose it from the cost of a miss, the cost of a false alarm, and how many alerts your team can actually review. | لذا اخترها من كلفة الحالة الفائتة، وكلفة الإنذار الكاذب، وعدد التنبيهات التي يستطيع فريقك مراجعتها فعلًا. |
| 7 | 68-75 | The 99.9% headline crossed out and replaced by 'caught / bothered / capacity' | Strike-through, then three icons appear | Judge a model by the decision it drives | Judge a model by the decision it drives. Lesson 5.2 shows you how. | احكم على النموذج بالقرار الذي يقوده. يشرح لك الدرس 5.2 كيف. |

**Closing takeaway:** For rare events, accuracy misleads. Use precision and recall at a threshold chosen from costs and team capacity.
**Call to action:** Open lesson 5.2 and run the 200,000-transaction exercise, where an all-genuine model beats yours on accuracy.

**Re-check before production:**
- The '1 in 1,000' rate is the lesson's illustrative 'say' figure (05-ml.md:309). Label it as illustrative. The exercise uses about 0.2%.
- The Arabic file renders Precision as 'الدقة', the everyday word also used for accuracy. Agree one Arabic term for each before narration.
- The Arabic formula lines (05-ml.ar.md:325-326) are currently truncated. Take the on-screen formulas from the English lines.
