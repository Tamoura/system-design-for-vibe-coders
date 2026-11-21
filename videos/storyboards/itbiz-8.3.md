# Storyboard: Running IT as a Business, lesson 8.3

> AI-drafted, not expert-reviewed. Written on 2026-11-20, after the course was published, not as part of the November 2026 content audit. Check every fact against the lesson (`itbiz/modules/08-run.md`) and its claims register (`academy/claims/itbiz.md`) before production.

**Pick 3 of 3 for this course.** A green "99.9%" that hid a four-hour card failure is a strong opening, and an error budget drawn as a fuel gauge is a natural visual. The numbers (10,000 bad requests a month, about 43 minutes, 60% used by the 20th) are simple and recomputed from the lesson.

## The green number that hid an outage

**Lesson:** 8.3 Service levels, SLOs and error budgets as a management tool
**Why this lesson:** It turns a vague argument (release more or release less?) into a shared number that product, operations and finance all agree in advance, and it shows the board-level trap of averaging availability across systems.
**Target viewer:** A head of IT operations, product manager or service owner who reports availability upwards and argues about release pace.
**Length:** about 85 seconds

## Scenes

**1. 0-10 s - All green**
- On screen: A quarterly report with one big green tile: "Availability 99.9%". Small print: "average of 140 systems · server ping".
- Visual/animation: Zoom into the tile; behind it, a red four-hour block labelled "Card payments down" is hidden under the green.
- On-screen text: "Najm Bank is fictional. All figures are illustrative, not benchmarks."
- VO (EN): "Omar's quarterly report showed ninety-nine point nine percent availability. It was an average over a hundred and forty systems, measured by whether servers answered a ping. The four-hour card failure that quarter didn't show. A board member asked why the number was green."
- VO (AR): "أظهر تقرير عمر الفصلي توافرًا بنسبة تسعة وتسعين فاصلة تسعة في المئة. لكنه كان متوسطًا لمئة وأربعين نظامًا، يُقاس بمدى استجابة الخوادم لأمر ping. ولم يظهر فيه تعطّل البطاقات الذي استمر أربع ساعات في ذلك الفصل. فسأل أحد أعضاء المجلس: لماذا الرقم أخضر؟"

**2. 10-20 s - Three people, no number**
- On screen: Reem holding a sign "Release weekly", Yousef holding "Release less", Tariq holding "How much reliability are we buying?"
- Visual/animation: Three speech bubbles collide in the middle with a question mark.
- On-screen text: "Opinions, not a number"
- VO (EN): "Meanwhile Reem wanted weekly releases. Yousef wanted fewer, because the last two had each caused an incident. Tariq wanted to know how much reliability the bank was paying for. Nobody had a number."
- VO (AR): "في الأثناء أرادت ريم إصدارات أسبوعية، وأراد يوسف إصدارات أقل لأن كلًّا من الإصدارين الأخيرين تسبّب في حادثة. وأراد طارق أن يعرف كم من الموثوقية يشتري البنك. ولم يكن لدى أحد منهم رقم."

**3. 20-34 s - Measure the journey, not the server**
- On screen: A card payment travels from a shop terminal to the bank's authorisation gateway. A stopwatch next to it: "answered within 2 seconds?" Ticks are green, a few are red.
- Visual/animation: The ticks pour into a ratio: "good answers ÷ all requests".
- On-screen text: "SLI: share of card authorisations answered within 2 seconds · SLO: 99.9% over a rolling 30 days"
- VO (EN): "So they measured the journey, not the servers: the share of card authorisations answered within two seconds. That's the indicator. The target, the service level objective, is ninety-nine point nine percent over a rolling thirty days."
- VO (AR): "فقاسوا رحلة العميل لا الخوادم: نسبة طلبات تفويض البطاقات التي تتلقى ردًا خلال ثانيتين. هذا هو المؤشر. أما الهدف، أي هدف مستوى الخدمة (SLO)، فهو تسعة وتسعون فاصلة تسعة في المئة على مدى ثلاثين يومًا متحركة."

**4. 34-48 s - The budget**
- On screen: A fuel gauge labelled "Error budget". "10 million requests a month × 0.1% = 10,000 bad requests allowed".
- Visual/animation: A ladder of nines beside it, each step shrinking the gauge tenfold: "99% → 100,000 · 99.9% → 10,000 · 99.99% → 1,000". A small tag: "as time: 99.9% ≈ 43 minutes in 30 days".
- On-screen text: "Error budget = 1 − SLO. Each extra nine: ten times smaller."
- VO (EN): "One minus the target is the error budget. At about ten million requests a month, that's ten thousand bad requests allowed. Each extra nine cuts the budget by a factor of ten. And a Google Cloud blog post warns it can be a hundred times more expensive to run a service that is ten times more reliable."
- VO (AR): "الفرق بين الهدف والمئة في المئة هو ميزانية الخطأ (error budget). ومع نحو عشرة ملايين طلب في الشهر، يُسمح بعشرة آلاف طلب سيئ. وكل تسعة إضافية تقلّص الميزانية عشر مرات. وتحذّر تدوينة على مدونة Google Cloud من أن تشغيل خدمة أكثر موثوقية بعشر مرات قد يكلّف مئة ضعف."

**5. 48-60 s - Pricing the nines**
- On screen: Three price tags on a shelf: "99.9%: today's set-up", "99.95%: + second processor link, faster failover", "99.99%: + second active processing site, several times today's running cost".
- Visual/animation: The head of retail banking taps 99.9%; a stamp reads "rolling 30 days, for now".
- On-screen text: "The SLO is a business decision written as a number."
- VO (EN): "Tariq priced the targets. Ninety-nine point nine five needed a second processor link. Ninety-nine point nine nine needed a second active site as well, several times today's running cost. The business chose ninety-nine point nine, for now."
- VO (AR): "سعّر طارق الأهداف: نسبة تسعة وتسعين فاصلة تسعة خمسة تحتاج إلى وصلة ثانية بالمعالج، ونسبة تسعة وتسعين فاصلة تسعة تسعة تحتاج فوق ذلك إلى موقع معالجة ثانٍ نشط، بأضعاف تكلفة التشغيل الحالية. فاختار قطاع الأعمال تسعة وتسعين فاصلة تسعة في الوقت الحالي."

**6. 60-74 s - The gauge drops**
- On screen: A calendar flips to the 20th. The gauge drops to 40% left; one release is marked as the main cause. A four-band strip lights up: "more than half · a quarter to a half · less than a quarter · exhausted". The needle sits in "a quarter to a half".
- Visual/animation: Two actions pop up: "review rollback plans", "bring forward the processor timeout fix". A clock beside the argument shrinks to "10 minutes".
- On-screen text: "60% used by the 20th → about 4,000 bad requests left → band: a quarter to a half"
- VO (EN): "By the twentieth of the first month, sixty percent of the budget was gone, mostly from one release. The policy, signed in advance, said what that meant: review rollback plans and move the reliability fix up. The release argument now took ten minutes."
- VO (AR): "بحلول اليوم العشرين من الشهر الأول كان ستون في المئة من الميزانية قد استُهلك، معظمه بسبب إصدار واحد. وكانت السياسة الموقّعة مسبقًا تحدد ما يعنيه ذلك: مراجعة خطط التراجع، وتقديم إصلاح الموثوقية. وصار الجدل حول الإصدارات يستغرق عشر دقائق."

**7. 74-85 s - Closing card**
- On screen: The board report rebuilt as a short table of journeys: "Pay by card · Log in", each with its target, met or not, and budget left.
- Visual/animation: The old single green tile fades out behind the new table.
- On-screen text: "Write the SLO and the policy before you need them."
- VO (EN): "Report journeys, not averages. The SLO is a business decision written as a number, and the policy is signed before it's needed. Open lesson 8.3 and write your first SLO sheet."
- VO (AR): "اعرض رحلات العملاء لا المتوسطات. هدف مستوى الخدمة قرار عمل مكتوب على هيئة رقم، والسياسة تُوقَّع قبل الحاجة إليها. افتح الدرس 8.3 واكتب أول ورقة لأهداف مستوى الخدمة."

## Takeaway and call to action
Takeaway: the SLO is a business decision written as a number, and an error budget only manages anything if a policy agreed in advance says what changes when it runs low. CTA: open lesson 8.3 and write an SLO sheet for two customer journeys.

## Re-check before production
- Recomputed from the lesson's error budget table and SLO sheet (`itbiz/modules/08-run.md`): 10,000,000 × 0.001 = 10,000; × 0.01 = 100,000; × 0.0001 = 1,000. As time over 30 days: 43,200 minutes × 0.001 = 43.2 minutes (lesson: "about 43 minutes"). By the 20th, 60% used leaves 40% (about 4,000 bad requests, computed here; the lesson gives only the 60% and the band), which is in the lesson's "a quarter to a half" band.
- The card SLI is request-based, so "about 43 minutes" applies only "if the SLI were time-based", as the lesson's table says. Keep that qualifier on the tag in scene 4.
- Do not compute on screen how much budget the four-hour outage would have used; the lesson does not state it.
- The "100 times more expensive ... 10 times more reliable" line is from a 2019 Google Cloud blog post (claims register itbiz-08-011, primary text, checked). Show the source and year on screen and keep "can be".
- The bands, the 10 million monthly volume and the cost of 99.95% and 99.99% are Najm Bank's illustrative figures, not benchmarks or vendor prices. "Several times today's running cost" is the lesson's own wording; do not turn it into a number.
- "ping" stays in Latin letters in the Arabic VO. Keep the "Najm Bank is fictional; figures illustrative" label on screen in scene 1 and as a footer in scenes 4 to 6.
