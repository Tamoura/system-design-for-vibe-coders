# Storyboard: AI Governance: Zero to Hero (AIGP-aligned), lesson 10.2

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 2 of 3 for this course.** A concrete failure on a dashboard, where the average hides a collapse in one group. It has a traceable root cause and a strong real-world cold open (Zillow), and it teaches why segment-level monitoring and incident clocks matter.

## The dashboard was green (Lesson 10.2: Monitoring, drift and incidents)

**Why this lesson:** It turns 'AI fails quietly' into a single image: a green gauge hiding a subgroup collapse (10-release-monitor.md:256-258).
**Target viewer:** Risk, compliance and product staff who will own or review monitoring for a deployed model.
**Length:** about 80 seconds.

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-12 | A house with a price tag; the ground under it slides. | The house stays still while the landscape moves. | Zillow, 2021 | In 2021 Zillow wound down its home-buying business after finding house prices far harder to forecast than expected. No one broke the model. The world moved under it. | في عام 2021 أوقفت Zillow نشاط شراء المنازل بعد أن تبيّن أن التنبؤ بالأسعار أصعب بكثير مما توقّعت. لم «يكسر» أحد النموذج، بل تحرّك العالم من تحته. |
| 2 | 12-24 | Najm Bank's monitoring dashboard: one big gauge in green. | A gentle pulse on the gauge, everything calm. | Overall approval rate: OK | At Najm Bank, four months after credit-scoring version 2 went live, the headline dashboard is green. | في بنك نجم، وبعد أربعة أشهر من إطلاق الإصدار الثاني لنموذج التقييم الائتماني، تبدو لوحة المتابعة الرئيسية خضراء. |
| 3 | 24-38 | Camera zooms into one slice: UAE, under 25. | The slice's bar drops by a third, turning red, while the main gauge stays green. | Under-25s in the UAE: approvals down by a third | But zoom in, and approvals for applicants under 25 in the UAE have fallen by a third. Complaints about 'declined without explanation' are rising. | لكن عند التدقيق، نجد أن الموافقات للمتقدّمين دون 25 عامًا في الإمارات انخفضت بمقدار الثلث، وأن الشكاوى من «الرفض دون تفسير» في ازدياد. |
| 4 | 38-52 | A data pipeline from an HR-data vendor; one field label changes to "unknown employer". | A tag is quietly rewritten upstream and flows into the model, which flags it high-risk. | Upstream field recoded | The cause: an upstream vendor recoded the employer-category field. Young staff at new government entities arrived as 'unknown employer', which the model treats as high risk. | السبب: قام مزوّد بيانات خارجي بإعادة ترميز حقل فئة صاحب العمل، فوصل الموظفون الشباب في الجهات الحكومية الجديدة بوصفهم «صاحب عمل غير معروف»، وهي قيمة يعاملها النموذج على أنها عالية المخاطر. |
| 5 | 52-64 | The single gauge splits into many small gauges by segment. | Segment dials light up, and one flashes red early. | Monitor segments, not just averages | AI fails quietly. Harm usually starts in a segment that the average hides, so monitor by group, not just overall. | الذكاء الاصطناعي يفشل بصمت. يبدأ الضرر عادةً في شريحة يخفيها المتوسط، لذا راقِب حسب الفئات لا الأرقام الإجمالية فقط. |
| 6 | 64-76 | Two stopwatches start: "15 days" and "72 hours". | Clocks start running side by side. | Several clocks can run at once | And if it is an incident, deadlines start: up to 15 days for serious incidents under the EU AI Act, and 72 hours for a personal data breach under the GDPR. | وإذا كان الأمر حادثًا، تبدأ المُهل: حتى 15 يومًا للحوادث الخطيرة بموجب قانون الذكاء الاصطناعي الأوروبي، و72 ساعة لخرق البيانات الشخصية بموجب GDPR. |
| 7 | 76-80 | A checklist icon. | | Who to tell, by when | | |

**Closing takeaway:** A green average is not a healthy model; watch the segments and know which clocks start ticking.
**Call to action:** Open Lesson 10.2 to design a monitoring plan that would have caught this in days, not months.

**Re-check before production:** Check the Zillow wording (2021, winding down Zillow Offers) against a dated source and show it on screen. Confirm the Art. 73 'within 15 days at most' wording and the faster deadlines for the gravest cases against the current AI Act text, since the Omnibus amended dates. Scene 7 is a silent end card. The Najm story is fictional, so label it.
