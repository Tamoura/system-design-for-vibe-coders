# Storyboard: AI Governance: Zero to Hero (AIGP-aligned), lesson 9.3

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 1 of 3 for this course.** One counter-intuitive idea, worked through with arithmetic that will not go out of date. It then leads into the course's best worked example: you cannot make every fairness measure equal at once.

## 94% accurate, and useless (Lesson 9.3: Testing, evaluation, validation and red-teaming)

**Why this lesson:** It shows the 'accuracy illusion' and the fairness trade-off, two ideas learners rarely grasp from text alone, using numbers from the lesson that will not date (09-data.md:464, :474-492).
**Target viewer:** A compliance, privacy or product professional with no data-science background, preparing for the AIGP.
**Length:** about 85 seconds.

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-10 | A grid of 100 applicant icons; 6 turn red. | A dashboard badge flips to a big green "94%". | 94% accurate? | Dana's credit model scores 94% accuracy. Sounds great. | نموذج دانة الائتماني دقيق بنسبة 94%. يبدو ذلك ممتازًا. |
| 2 | 10-22 | A rubber stamp hits every icon with "NO DEFAULT". | The 6 red icons get stamped too, and the badge still reads 94%. | A model that says "no default" to everyone | But if 6 in 100 applicants default, a model that says "no default" to everyone is also 94% accurate. And completely useless. | لكن إذا تعثّر 6 من كل 100 متقدّم، فإن نموذجًا يقول «لن يتعثّر» للجميع دقيق أيضًا بنسبة 94%. ولا فائدة منه إطلاقًا. |
| 3 | 22-34 | Four gauges appear: precision, recall, AUC, calibration. | The single badge breaks apart into four dials. | Ask for more than one number | So governance asks for more than accuracy: precision, recall, AUC and calibration tell the real story. | لذلك تطلب الحوكمة أكثر من الدقة: الدقة النوعية والاستدعاء ومنحنى AUC والمعايرة هي التي تكشف الصورة الحقيقية. |
| 4 | 34-50 | Two columns of 1,000 people, Group A and Group B; approval bars at 54% and 36%. | The bars grow and a ratio counter ticks to 0.67, below a dashed 0.8 line. | Parity: 0.67, below 0.8 | Now compare groups. Group A is approved at 54%, Group B at 36%: a ratio of 0.67, below the four-fifths line. Yet good applicants in both groups are approved at about 83%. | قارِن الآن بين المجموعتين. تُقبل المجموعة A بنسبة 54% والمجموعة B بنسبة 36%، أي بنسبة 0.67، دون حدّ الأربعة أخماس. ومع ذلك يُقبل المتقدّمون الجيّدون في المجموعتين بنحو 83%. |
| 5 | 50-64 | Group B's bar is forced up to 540 approvals; red icons pour in. | A precision meter drops from 92% to 74%; the false-positive meter rises to 23%. | Force parity: precision 74%, FPR 23% | Force equal approval rates, and Group B's precision falls to 74% while 23% of bad applicants get loans they cannot repay. That is a harm too. | فرضُ نسب قبول متساوية يُسقط الدقة النوعية للمجموعة B إلى 74%، ويحصل 23% من المتقدّمين غير المؤهّلين على قروض لا يستطيعون سدادها. وهذا ضرر أيضًا. |
| 6 | 64-76 | Three sliders labelled selection rate, error rate, precision; moving one pushes the others. | Linked sliders that cannot all line up. | You can't equalise them all | When base rates differ, you generally cannot equalise selection rates, error rates and precision at the same time. | عندما تختلف المعدلات الأساسية بين المجموعات، لا يمكن عمومًا مساواة نسب القبول ونسب الخطأ والدقة النوعية في آنٍ واحد. |
| 7 | 76-85 | A signature line labelled "Accountable owner". | A pen signs a documented trade-off. | Decided, documented, owned | So the choice is not a data scientist's to make quietly. The accountable owner must document it and accept it. | لذلك ليس هذا خيارًا يحسمه عالِم البيانات بصمت؛ بل يجب أن يوثّقه المسؤول صاحب القرار ويقبله. |

**Closing takeaway:** One good-looking number can hide a useless model, and fairness is a trade-off someone must own.
**Call to action:** Open Lesson 9.3 to work through the full fairness table and try the exercise yourself.

**Re-check before production:** The worked-example numbers (09-data.md:476-492) are arithmetically verified. Keep 'roughly 83%' because Group B is exactly 82.5%. Confirm the Arabic terms for precision and recall against TRANSLATING.md.
