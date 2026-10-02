# الوحدة 1 — المهارات التي يتحقق منها أصحاب العمل (The skills employers check)

*تخبر الشهادة الجامعية (degree) صاحبَ العمل (employer) بأنك قادر على التعلّم. لكنها لا تخبره بأنك قادر على العمل في قاعدة شيفرة مشتركة (shared codebase)، أو العثور على خطأ برمجي (bug) لم تكتبه بنفسك، أو التحقق مما أنتجه وكيل ذكاء اصطناعي (AI agent)، أو إبقاء البرمجيات تعمل (keep software running) بعد أن يستخدمها أناس حقيقيون. هذه هي الأشياء التي يبحث عنها اليوم مديرو التوظيف (hiring managers) ومُجرو المقابلات (interviewers) لدى المبتدئ (junior)، وكثير من الخرّيجين (graduates) لم يتعلّموها قط بشكل مباشر. تسمّي هذه الوحدة ذلك الحدّ الأدنى (baseline)، وتبيّن شكل "ما يكفي لمبتدئ" (good enough for a junior) في كل جزء منه. تبدأ بالمهارات اليومية (everyday skills): Git، وقراءة الشيفرة (reading code)، وتصحيح الأخطاء (debugging)، والاختبار (testing)، والتوثيق الكتابي (writing things down). ثم تتناول البناء باستخدام وكلاء البرمجة بالذكاء الاصطناعي (AI coding agents) بطريقة تُظهر حُسن تقديرك (judgement) بدلًا من أن تُخفي غيابه. وتنتهي بالتفكير الإنتاجي (production thinking): الفجوة بين "يعمل على حاسوبي" (it runs on my laptop) و"يعمل للمستخدمين" (it runs for users). سترافق عمر، الذي لم ينشر (deployed) أي شيء من قبل؛ وريم، التي تبني بسرعة مع الوكلاء (agents) لكنها لا تستطيع دائمًا شرح شيفرتها؛ وهدى ويوسف ومحمد. ويشرح خالد، مدير الهندسة (engineering manager) في بنك نجم (Najm Bank) الذي يوظّف المبتدئين، وطارق، الذي يُجري المقابلات التقنية (technical interviews)، كيف يميّزان الفرق. يحيلك كل درس إلى دروس أخرى في المكتبة (library) تبني المهارة بعمق، ويترك بين يديك مُنتَجًا (artefact): تدقيقًا للمهارات (skills audit)، وقائمة تحقق (verification checklist)، وقائمة جاهزية للإطلاق (ship-ready checklist).*

> **الخطوات (Steps):** Learn، Build — تعلُّم الحدّ الأدنى (baseline) الذي يتحقق منه كل صاحب عمل، وبناء العادات (habits) والأدلة (evidence) التي تُثبت أنك تملكه.

---

# 1.1 — الحدّ الأدنى للمبتدئ (The junior baseline): Git، وقراءة الشيفرة (reading code)، وتصحيح الأخطاء (debugging)، والاختبار (testing)، والتوثيق الكتابي (writing it down)
*المستوى (Level): 🟢 مبتدئ (Beginner)* · *المتطلبات (Prerequisites): 0.1، 0.2* · *الخطوة (Step): Learn, Build*

## ⚡ الدرس في دقيقة (In 60 seconds)
- أيًّا كان الدور (role) — برمجيات (software)، أو ذكاء اصطناعي (AI)، أو بيانات (data)، أو منصّات (platform)، أو أمن (security) — يتوقّع أصحاب العمل من المبتدئ (junior) خمس مهارات يومية: **Git**، و**قراءة الشيفرة (reading code)**، و**تصحيح الأخطاء (debugging)**، و**الاختبار (testing)**، و**التوثيق الكتابي (writing it down)**.
- لا شيء منها متقدّم (advanced). لكنها مجتمعةً تُثبت أنك قادر على العمل بأمان في قاعدة شيفرة (codebase) يملكها غيرك، وهذا ما يسأل عنه مدير التوظيف (hiring manager) في الحقيقة.
- القاعدة الأهم: **اترك أثرًا (leave a trail)**. إيداعات صغيرة (small commits) برسائل واضحة (clear messages)، واختبار يُثبت الإصلاح (a test that proves the fix)، وطلب دمج (pull request, PR) يشرح السبب (explains why). يجب أن يكون منطقك (reasoning) مرئيًا للشخص التالي.
- إشارة القرار (Decision cue): قبل أن تطلب المساعدة، هل تستطيع أن تقول ما الذي توقّعته (what you expected)، وما الذي حدث (what happened)، وما الذي جرّبته (what you tried)؟ إن لم تستطع، فأنت ما زلت في مرحلة تصحيح الأخطاء (debugging).
- أكبر فخ (Biggest trap): اعتبار هذه المهارات "أبسط من أن تُعرض" (too basic to show). يتحقق منها مُجرو المقابلات (interviewers) مباشرة، عبر سجلّ مستودعك (repository history)، وجولات تصحيح الأخطاء المباشرة (live debugging rounds)، وطلب "اشرح لي هذه الشيفرة" (walk me through this code).

## 🧭 لماذا يهم (Why it matters)
يحمل عمر شهادة في علوم الحاسوب (CS degree) بمرتبة الشرف الأولى (first-class)، ويتفوّق في ألغاز الخوارزميات (algorithm puzzles). في المهمة المنزلية (take-home) لبرنامج الخرّيجين في بنك نجم (Najm Bank)، يبني خدمة صغيرة لتصنيف المعاملات (transaction-categorisation service)، والشيفرة جيدة. يسلّمها ملفًا مضغوطًا (zip file): بلا سجلّ Git ‏(Git history)، وبلا اختبارات (tests)، وبملف README لا يقول سوى "run main.py". في مقابلة المتابعة (follow-up interview)، يعرض طارق مُدخلًا فاشلًا (failing input) لم يجرّبه عمر قط، ويطلب منه أن يجد السبب (find the cause). يقرأ عمر من الأعلى، ويغيّر ثلاثة أشياء دفعة واحدة (changes three things at once)، ثم يفقد القدرة على تتبّع أيّ تغيير كان المؤثّر. تمرّ عشرون دقيقة. كانت المشكلة افتراضًا حول صيغة التاريخ (date-format assumption) في السطر 41.

يشرح خالد القرار لعائشة، مسؤولة التوظيف (recruiter): "خوارزمياته (algorithms) أفضل من خوارزمياتي. لكنه في شهره الأول سيقضي معظم وقته في قراءة شيفرة لم يكتبها (read code he didn't write)، وملاحقة أخطاء لم يتسبّب بها (chase bugs he didn't cause)، وشرح تغييراته في طلبات الدمج (pull requests). لم أرَ أي دليل (evidence) على أنه قادر على ذلك بعد." يُدعى عمر إلى إعادة التقديم (reapply) في الدفعة التالية (next intake)، مع قائمة بما كان ناقصًا.

فجوة عمر شائعة، ولا علاقة لها بالذكاء (intelligence). الجامعة تقيّم الإجابة النهائية (final answer)؛ أما أماكن العمل فتقيّم العملية (process)، لأن أشخاصًا آخرين يعيشون مع عملك (live with your work).

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**لماذا هذه الخمس (Why these five).** نادرًا ما يبدأ المبتدئ (junior) من صفحة بيضاء (blank page). أنت تنضمّ إلى قاعدة شيفرة قائمة (existing codebase) وتغيّرها على أجزاء صغيرة (small pieces) يراجعها الآخرون (others review). هذه المهارات الخمس تجعل ذلك آمنًا:

| المهارة (Skill) | كيف يبدو "ما يكفي لمبتدئ" (good enough for a junior) | كيف يبدو "ليس بعد" (not yet) |
|---|---|---|
| **Git** | إنشاء فرع (branch)، وإيداع تغييرات صغيرة (commit small changes) برسائل واضحة، وفتح طلب دمج (open a pull request)، والاستجابة للمراجعة (respond to review)، وحلّ تعارض بسيط (resolve a simple conflict)، والتراجع عن خطأ بهدوء (undo a mistake calmly) | مشاركة الشيفرة كملفات مضغوطة (zip files) أو كإيداع واحد ضخم (one giant commit) اسمه "final"؛ الخوف من الطرفية (terminal)؛ الدفع القسري (force-pushing) فوق عمل الآخرين |
| **قراءة الشيفرة (Reading code)** | العثور على نقطة الدخول (entry point)، وتتبّع طلب واحد (follow one request) عبر الشيفرة، واستخدام البحث (search)، وقراءة الاختبارات (read the tests) | القراءة من السطر 1 حتى النهاية؛ إعادة كتابة شيفرة لم تفهمها بعد (rewriting code you do not understand yet) |
| **تصحيح الأخطاء (Debugging)** | إعادة إنتاج الخطأ (reproduce)، وقراءة تتبّع المكدّس (stack trace)، وتضييق النطاق (narrow down)، واختبار فكرة واحدة في كل مرة (test one idea at a time)، وتأكيد الإصلاح (confirm the fix) | تغيير الأشياء عشوائيًا (at random) حتى تعمل؛ عدم معرفة سبب عملها الآن |
| **الاختبار (Testing)** | كتابة اختبار وحدة (unit test)، وتشغيل مجموعة الاختبارات (run the suite)، وإضافة اختبار يفشل قبل إصلاحك وينجح بعده (fails before your fix and passes after) | "اختبرتُه يدويًا" (I tested it manually)؛ اختبارات لا تتحقق من شيء؛ حذف اختبار فاشل (deleting a failing test) لكي "ينجح" |
| **التوثيق الكتابي (Writing it down)** | رسائل إيداع (commit messages) تقول السبب (say why)، وطلب دمج يستطيع المراجع (reviewer) تتبّعه، وملف README يستطيع الآخرون تشغيله، وأسئلة تذكر ما جرّبته (what you tried) | "fixed stuff"؛ "لا يعمل، ساعدوني" (it doesn't work, help)؛ ملف README لا يستطيع استخدامه أحد سواك |

**Git باختصار (Git, briefly).** **Git** نظام للتحكم في الإصدارات (version control system): يسجّل كل تغيير (records every change) بحيث ترى من غيّر ماذا، ومتى، ولماذا، وتستطيع العودة إلى الوراء (go back). **الإيداع (commit)** تغيير واحد محفوظ مع رسالة (one saved change with a message). **الفرع (branch)** مسار عمل منفصل (separate line of work). **طلب الدمج (pull request, PR)** — ويسمّيه GitLab طلب الدمج (merge request) — يطلب مراجعة فرعك ودمجه (reviewed and merged)، وعادةً على GitHub أو GitLab أو Bitbucket. إن كان هذا جديدًا عليك، فإن [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس F.3 — الإصدارات والمستودعات والنشر: كيف تنتقل البرمجيات (Versions, repos, and deploys — how software moves)](../vibe/index.ar.html#lF-3) في المكتبة يشرحه من الصفر (from scratch).

رسالة الإيداع (commit message) هي حيث يعيش منطقك (reasoning). قارن:

| ضعيفة (Weak) | قوية (Strong) |
|---|---|
| `fix` | `Parse transaction dates in day-first format` |
| `changes` | `Reject negative amounts in categoriser input` |
| `final version 2` | `Add test for empty merchant name` |

كل صيغة قوية تقول ما يفعله الإيداع (what the commit does)، بتغيير واحد لكل إيداع (one change each)؛ وحين لا يكون السبب واضحًا، أضِف متنًا (body) بعد سطر فارغ (blank line) يشرح السبب. تستخدم بعض الفرق **الإيداعات الاصطلاحية (Conventional Commits)** ‏(`fix: …`، `feat: …`)؛ اتّبع ما يعتمده الفريق (follow the team).

**قراءة الشيفرة (Reading code).** المهارة التي لا يعلّمها أحد (nobody teaches)، والتي ستستخدمها أكثر من غيرها. إليك طريقة (method) للتعامل مع مستودع غير مألوف (unfamiliar repository):

1. اقرأ ملف README واعرف كيف تشغّله (how to run it) وكيف تشغّل اختباراته (run its tests). شغّل الاثنين.
2. اعثر على **نقطة الدخول (entry point)**: دالة `main`، أو مسار الويب (web route)، أو الأمر (command)، أو المهمة المجدولة (scheduled job).
3. اختر إجراءً حقيقيًا واحدًا (one real action) ("يرفع المستخدم كشف حساب" (a user uploads a statement)) وتتبّعه عبر الشيفرة (follow it through the code)، مدوّنًا الملفات والدوال (files and functions) التي يمرّ بها.
4. اقرأ **الاختبارات (tests)** الخاصة بذلك الجزء: فهي تُظهر ما يُفترض أن تفعله الشيفرة (what the code is supposed to do)، مع أمثلة (examples).
5. ابحث (Search) — باستخدام `git grep` أو "البحث في الملفات" (find in files) — عن رسالة الخطأ (error message) أو اسم الدالة (function name) بدلًا من التمرير (scrolling).

يطبّق [*لبنات بناء SaaS ‏(SaaS Building Blocks)*، الدرس 0.2 — كيف تقرأ قاعدة شيفرة مفتوحة المصدر ضخمة دون أن تغرق (How to read a giant open-source codebase without drowning)](../saas/index.ar.html#/0.2) في المكتبة الطريقةَ نفسها على المشاريع مفتوحة المصدر الكبيرة (large open-source projects).

**تصحيح الأخطاء (Debugging).** تصحيح الأخطاء حلقة (loop) يمكنك اتّباعها تحت الضغط (under pressure)، وليس موهبة (talent):

```mermaid
flowchart RL
    R["أعِد إنتاج الخطأ بشكل موثوق<br/>(Reproduce it reliably)"] --> O["لاحِظ: اقرأ رسالة الخطأ وتتبّع المكدّس<br/>(Observe: read the error and stack trace)"]
    O --> H["كوّن فرضية واحدة<br/>(Form one hypothesis)"]
    H --> T["اختبرها بتغيير واحد أو طباعة واحدة<br/>(Test it with one change or one print)"]
    T -->|"خاطئة (wrong)"| H
    T -->|"صحيحة (right)"| F["أصلِح الخطأ وأضِف اختبارًا<br/>(Fix it and add a test)"]
    F --> V["تحقّق من الحالة الأصلية ومن مجموعة الاختبارات<br/>(Verify the original case and the suite)"]
```

عادتان هما الأهم: **أعِد الإنتاج أولًا (reproduce first)** (وإلا فلن تعرف أنك أصلحته)، و**غيّر شيئًا واحدًا في كل مرة (change one thing at a time)**. **تتبّع المكدّس (stack trace)** يسرد استدعاءات الدوال (function calls) التي كانت نشطة لحظة وقوع الخطأ؛ والسطر المفيد عادةً هو آخر سطر في شيفرتك *أنت* (the last one in *your* code). تعلّم **مصحّح الأخطاء (debugger)** في محرّرك (editor) — نقاط التوقف (breakpoints)، والتنفيذ خطوة بخطوة (stepping)، وفحص المتغيرات (inspecting variables) — فهو يتفوّق على عشرين جملة طباعة (print statements).

**الاختبار (Testing).** **اختبار الوحدة (unit test)** يتحقق من جزء صغير واحد من الشيفرة (عادةً دالة (function)) بمعزل عن غيره (in isolation). **اختبار التكامل (integration test)** يتحقق من أن عدة أجزاء تعمل معًا (work together)، كشيفرتك مع قاعدة بيانات حقيقية (real database) مثلًا. تتّبع معظم الاختبارات الشكل **التهيئة، التنفيذ، التأكيد (arrange, act, assert)**: جهّز المُدخل (set up the input)، وشغّل الشيفرة (run the code)، وتحقّق من النتيجة (check the result).

```python
# A regression test: it failed before Omar's fix and passes after it
from categoriser import parse_date

def test_parses_day_first_dates():
    # arrange: a date that is ambiguous if read month-first
    raw = "03/11/2025"
    # act
    result = parse_date(raw)
    # assert: 3 November, not 11 March
    assert (result.day, result.month) == (3, 11)
```

عادة المبتدئ (The junior habit): **كل إصلاح لخطأ يأتي مع اختبار كان سيكتشفه (every bug fix comes with a test that would have caught it).** إنه دليلك (proof)، وهو يمنع الخطأ من العودة (stops the bug returning).

**التوثيق الكتابي (Writing it down).** رسائل الإيداع (commit messages)، وأوصاف طلبات الدمج (pull request descriptions)، وملفات README، والأسئلة (questions) تغطّي معظم ما يكتبه المبتدئ. السؤال الجيد الموجّه إلى زميل (colleague) له أربعة أجزاء (four parts): ما الذي تحاول فعله (what you are trying to do)، وما الذي توقّعته (what you expected)، وما الذي حدث بدلًا من ذلك (what happened instead) (مع رسالة الخطأ بنصّها (exact error))، وما الذي جرّبته بالفعل (what you already tried). سؤال "الاختبارات لا تعمل، هل يمكنك المساعدة؟" ⁦(The tests don't work, can you help?)⁩ يكلّف المهندس الأقدم (senior) عشر دقائق من الأسئلة؛ أما الصيغة ذات الأجزاء الأربعة (four-part version) فغالبًا ما تُجاب في رسالة واحدة.

### 🟡 التعمق أكثر (Going deeper)

**كيف تختبر المقابلاتُ الحدَّ الأدنى (How interviews test the baseline).** قليلة هي المقابلات التي تقول "الآن سنختبر مهاراتك في Git". فالمهارات يُتحقَّق منها بشكل غير مباشر (indirectly):

| أين (Where) | ما الذي ينظرون إليه (What they look at) | كيف تبدو الإشارة القوية (What a strong signal looks like) |
|---|---|---|
| مستودعك على GitHub أو مستودع المهمة المنزلية (take-home repository) | سجلّ الإيداعات (commit history)، والاختبارات (tests)، وملف README | إيداعات صغيرة كثيرة (many small commits) برسائل واضحة؛ اختبارات تعمل؛ ملف README يستطيع الغريب (stranger) اتّباعه |
| جولة تصحيح الأخطاء المباشرة (Live debugging round) | طريقتك في العمل تحت ضغط خفيف (process under mild pressure) | تعيد الإنتاج أولًا (reproduce first)، وتصرّح بفرضية (state a hypothesis)، وتغيّر شيئًا واحدًا في كل مرة |
| جولة قراءة الشيفرة (Code-reading round) | هل تستطيع تتبّع شيفرة غير مألوفة (follow unfamiliar code) | تتتبّع المُدخلات إلى المُخرجات (trace inputs to outputs) وتلتقط حالة حدّية (edge case) |
| "اشرح لي مشروعك" (Walk me through your project) | هل تفهم عملك أنت (understand your own work) | تستطيع شرح أي ملف، وأي قرار (any decision)، وما الذي كنت ستغيّره |

تغطّي الوحدة 5 أنماط المقابلات (interview formats). المستودع المُعتنى به (well-kept repository) دليل (evidence) يستطيع مُجري المقابلة التحقق منه قبل أن يلتقيك.

**طلب دمج يستطيع المراجع تتبّعه (A pull request a reviewer can follow).** يجب أن يجيب الوصف (description) عن ثلاثة أسئلة: ما الذي تغيّر (what changed)، ولماذا (why)، وكيف تعرف أنه يعمل (how you know it works).

```text
What:
Parse statement dates as day-first (DD/MM/YYYY).

Why:
Najm's CSV export uses day-first dates. We parsed them month-first,
so 03/11 became 11 March. Reported in issue #14.

How I tested it:
- Added `test_parses_day_first_dates` (fails on main, passes here).
- Ran the full suite: 42 passed.
- Imported the November sample file; all 318 rows have correct dates.
```

اجعل طلبات الدمج صغيرة (Keep pull requests small): تغيير من 50 سطرًا يحظى بمراجعة متأنّية (careful review)؛ وتغيير من 2,000 سطر يُتصفَّح على عجل (gets skimmed).

**التراجع والبحث في السجل (Undoing and searching history).** اعرف طرق النجاة (escape routes): `git status` و`git diff` لترى أين أنت، و`git restore` للتخلّص من التغييرات غير المودَعة (uncommitted changes)، و`git revert` للتراجع عن إيداع مشترك (shared commit) بإيداع جديد، و`git reflog` للعثور على إيداع "مفقود" (lost commit). تجنّب الدفع القسري (force-pushing) إلى فرع مشترك (shared branch). يُجري `git bisect` بحثًا ثنائيًا (binary-searches) في السجل عن الإيداع الذي أدخل الخطأ (introduced a bug)؛ مع الإيداعات الصغيرة يشير إلى خمسة أسطر، ومع إيداع واحد ضخم يشير إلى كل شيء.

**الاختبار بما يتجاوز الأساسيات (Testing beyond the basics).** المبتدئون يوسّعون مجموعة اختبارات قائمة (extend an existing suite) بدلًا من تصميم استراتيجية (design a strategy). اعرف المصطلحات (vocabulary): **التجهيزات (fixtures)** (إعداد مشترك (shared setup))، و**البدائل الوهمية (mocks)** (بدائل لأشياء خارجية (stand-ins for external things) مثل واجهة برمجة الدفع (payment API))، و**التغطية (coverage)** (تلميح مفيد، وهدف سيئ (a useful hint, a bad target))، و**التكامل المستمر (continuous integration)** (CI: تُشغَّل الاختبارات تلقائيًا مع كل دفع (on every push)). يبيّن [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 8.2 — الاختبارات بوصفها المواصفة التي لا يستطيع الوكيل تجاهلها (Tests as the spec the agent can't ignore)](../vibe/index.ar.html#l8-2) في المكتبة لماذا تزداد أهمية الاختبارات حين يكتب الوكيل (agent) الشيفرة، ويغطّي [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 8.3 — الفحص التمهيدي في CI واختبار "الراعي الكذّاب" (CI preflight and the boy-who-cried-wolf check)](../vibe/index.ar.html#l8-3) التكاملَ المستمر (CI).

**الحدّ الأدنى بحسب الدور (The baseline by role).** هدى (علم البيانات (data science)) تقرأ SQL وشيفرة خطوط البيانات (pipeline code)، وتتضمّن اختباراتها فحوصًا للبيانات (data checks) مثل "لا صفوف مكرّرة" (no duplicate rows). يوسف (الحوسبة السحابية (cloud)) يقرأ شيفرة البنية التحتية (infrastructure code) والسجلات (logs). محمد (المعسكر التدريبي (bootcamp)) لديه عادات جيدة في Git ‏(good Git habits)؛ وفجوته هي قراءة قواعد شيفرة أكبر من قاعدته (codebases larger than his own). ترسم الوحدة 2 خريطة كل دور (maps each role).

### 🔴 نظرة الخبير (Expert view)

**ما الذي يلاحظه المهندسون الأقدم فعلًا (What seniors actually notice).** حين يراجع خالد الشهر الأول لمبتدئ (junior's first month)، لا يعدّ أسطر الشيفرة (lines of code). بل يسأل: هل التغييرات **صغيرة وقابلة للتراجع (small and reversible)**، وهل يأتي كل إصلاح مع **دليل (evidence)**، وهل يستطيع **تتبّع المنطق (follow the reasoning)** دون أن يسأل؟ المبتدئون الذين يفعلون ذلك يُؤتمنون على عمل أكبر (trusted with bigger work) في وقت أبكر.

**لماذا يجعل الذكاء الاصطناعي الحدَّ الأدنى أكثر أهمية (Why AI makes the baseline more important).** كلما كتبت أدوات الذكاء الاصطناعي (AI tools) مزيدًا من الشيفرة الروتينية (routine code)، انتقل الجهد البشري (human effort) إلى مهارات هذا الدرس: قراءة شيفرة الوكيل (reading the agent's code)، وتصحيح إخفاقات لم تتسبّب بها (debugging failures you did not cause)، والاختبار للتحقق من ادّعاء (testing to verify a claim)، وتدوين ما تغيّر (writing down what changed). يبني الدرس 1.2 على هذا. الخرّيج الذي يستطيع توليد الشيفرة (generate code) دون التحقق منها يمكن أن تحلّ الأداة محلّه (replaceable by the tool)؛ أما من يستطيع التحقق من عمل الأداة (check the tool's work) فهو من يحتاجه الفريق.

**الكتابة مهارة تقنية (Writing is a technical skill).** كثير من العمل الهندسي يجري في البلاغات (issues) وطلبات الدمج (pull requests) والمحادثات (chat). وفي الخليج (the Gulf)، تُعدّ الإنجليزية التقنية الواضحة (clear technical English)، إلى جانب شرح الأمر نفسه بالعربية لمستخدم من جهة الأعمال (business user)، ميزة حقيقية (real advantage). ضع الخلاصة أولًا (put the conclusion first) وأدرِج الأمر أو رسالة الخطأ بنصّهما (exact command or error).

**اجعل حدّك الأدنى مرئيًا (Make your baseline visible).** عبارة "متمكّن من Git" ‏(Proficient in Git) في السيرة الذاتية (CV) لا تعني شيئًا. أما سجلّ مستودع نظيف (clean repository history)، وطلب دمج موصوف جيدًا (well-described pull request)، واختبارات في CI ‏(tests in CI)، وتقرير قصير عن خطأ (short bug write-up)، فهي التي تُثبته. تحوّل الوحدة 3 هذا إلى معرض أعمال (portfolio).

## 🧰 الأدوات (The toolkit)
| المورد أو الأداة أو النموذج (Resource, tool or template) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **Pro Git** — تأليف سكوت شاكون وبن ستراوب (Scott Chacon and Ben Straub) | كتاب Git الرسمي المجاني (free, official Git book): المفاهيم (concepts)، والأوامر (commands)، والتفريع (branching)، والتراجع عن الأخطاء (undoing mistakes) | لتعلّم Git كما ينبغي (learning Git properly) بدلًا من حفظ الأوامر (memorising commands) |
| **Conventional Commits** — الإيداعات الاصطلاحية | اصطلاح خفيف (lightweight convention) لرسائل الإيداع (`fix:`، `feat:`، `docs:`) | حين يستخدمه الفريق، أو في مشاريعك الخاصة لإبقاء السجل مقروءًا (keep history readable) |
| **git bisect** | أمر مدمج في Git ‏(built-in Git command) يبحث بحثًا ثنائيًا (binary-searches) في السجل للعثور على الإيداع الذي أدخل الخطأ (introduced a bug) | خطأ "كان يعمل من قبل" (used to work)؛ التدرّب عليه في مشروعك الخاص |
| **pytest** | إطار اختبار (test framework) واسع الاستخدام في Python، باختبارات بسيطة قائمة على `assert` ‏(يؤدّي Jest وJUnit الدور نفسه في JavaScript وJava) | كتابة أولى اختبارات الوحدة (unit tests) واختبارات الانحدار (regression tests) |
| **Minimal reproducible example** — المثال الأدنى القابل لإعادة الإنتاج | أصغر شيفرة ومُدخل لا يزالان يُظهران الخطأ (smallest code and input that still shows the bug)، كما يصفه مركز مساعدة Stack Overflow ‏(Stack Overflow's help centre) | قبل طرح سؤال في أي مكان؛ وكثيرًا ما يكشف الإجابة (reveals the answer) |
| **Pull request template** — قالب طلب الدمج | نموذج قصير بالبنود ما / لماذا / كيف اختبرته / ملاحظات (What / Why / How I tested it / Notes) يُضاف إلى المستودع | كل طلب دمج، بما في ذلك المشاريع الفردية (solo projects) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
يطلب خالد من كل خرّيج أن يملأ **تدقيق الحدّ الأدنى للمبتدئ (Junior baseline audit)** في الأسبوع صفر (week zero) من برنامج نجم للخرّيجين التقنيين (Najm Tech Graduate Programme)، ويعطي القالب نفسه (same template) للمرشّحين المدعوّين إلى إعادة التقديم (invited to reapply). القاعدة هي "أدلة لا صفات" (evidence, not adjectives): كل تقييم (rating) يحتاج إلى رابط (link) يستطيع شخص آخر التحقق منه. إليك تدقيق عمر، الذي أنجزه بعد ستة أسابيع من مقابلته الأولى، وقبل أن يعيد التقديم.

| المهارة (Skill) | هل أستطيع إظهارها؟ الدليل (رابط أو ملف) ⁦(Can I show it? Evidence (link or file))⁩ | التقييم: ليس بعد / في الطريق / جاهز (Rating: not yet / getting there / ready) | الإجراء التالي وتاريخه (Next action and date) |
|---|---|---|---|
| Git | مستودع المصنِّف (Categoriser repository) فيه 37 إيداعًا و4 طلبات دمج مدموجة (merged pull requests) | في الطريق (Getting there) | حلّ تعارض دمج حقيقي (real merge conflict) في مشروع ثنائي (pair project) بحلول 15 نوفمبر |
| قراءة الشيفرة (Reading code) | تتبّع من صفحة واحدة (one-page trace) لكيفية انتقال عملية الرفع (upload) عبر شيفرة تطبيق مالي مفتوح المصدر (open-source finance app) | في الطريق (Getting there) | تتبّع مشروع ثانٍ، هذه المرة بلغة أعرفها بدرجة أقل (a language I know less well) |
| تصحيح الأخطاء (Debugging) | تقرير مكتوب (write-up) عن خطأ صيغة التاريخ (date-format bug)، يتضمّن إعادة الإنتاج (reproduce) والفرضية (hypothesis) والإصلاح (fix) والاختبار (test) | جاهز (Ready) | التدرّب على تمرين "أصلِح الاختبار الفاشل" (fix the failing test) موقوت (timed) مرة كل أسبوع |
| الاختبار (Testing) | 42 اختبارًا تعمل في CI ‏(running in CI)، واختبار انحدار (regression test) لكل خطأ أُصلح | جاهز (Ready) | تعلّم التجهيزات (fixtures) والبدائل الوهمية (mocks) لعميل واجهة البنك البرمجية (bank-API client) |
| التوثيق الكتابي (Writing it down) | ملف README اتّبعه زميل دراسة (classmate) من الصفر في عشر دقائق؛ أوصاف طلبات الدمج (pull request descriptions) وفق القالب | في الطريق (Getting there) | أن أطلب من هدى مراجعة وصفين لطلبَي دمج |

أسئلة المراجعة (review questions) التي يطرحها خالد على كل صف: "هل يستطيع غريب التحقق من هذا في دقيقتين؟ هل التقييم صادق؟ هل الإجراء التالي محدّد؟" ⁦(Could a stranger verify this in two minutes? Is the rating honest? Is the next action specific?)⁩ ويراجعه المرشد (mentor) مرة أخرى في اليوم 30 ‏(day 30) (الوحدة 6).

## 🛠️ التمارين (Exercises)
- 🟢 ضع مشروعًا قائمًا لديك في Git، وأنشئ خمسة إيداعات صغيرة (five small commits) يفعل كل منها شيئًا واحدًا: ملف README بتعليمات التشغيل (run instructions)، وملف `.gitignore`، واختبار واحد (one test)، وإصلاح صغير واحد (one small fix)، وترتيب واحد (one tidy-up). *يكتمل عندما (Done when):* يُظهر `git log --oneline` خمسة إيداعات أو أكثر يستطيع زميل دراسة (classmate) فهم رسائلها دون فتح الشيفرة.
- 🟡 في مشروع صغير مفتوح المصدر (small open-source project)، استخدم طريقة القراءة ذات الخطوات الخمس (five-step reading method) لتتبّع إجراء مستخدم واحد (one user action) من نقطة الدخول (entry point) حتى النتيجة، ودوّن الملفات والدوال بالترتيب على صفحة واحدة. شغّل اختباراته، ثم اكسر شيئًا واحدًا عمدًا (break one thing on purpose) وانظر أي اختبار يفشل. *يكتمل عندما (Done when):* تكون الملاحظة موجودة، ويستطيع زميل (peer) يتّبع قائمة ملفاتك العثور على المسار نفسه في أقل من عشر دقائق.
- 🔴 اطلب من صديق أن يُخفي خطأً واقعيًا (realistic bug) بين عدة إيداعات صغيرة في مشروعك. اعثر عليه باستخدام `git bisect`، وأصلحه مع اختبار انحدار (regression test)، وافتح طلب دمج (pull request) باستخدام قالب هذا الدرس. *يكتمل عندما (Done when):* يُظهر طلب الدمج الاختبار الذي يفشل ثم ينجح (failing-then-passing test)، ويذكر الوصف الإيداعَ الذي أدخل الخطأ (the commit that introduced the bug)، ويستطيع شخص آخر مراجعته دون أن يطرح عليك أي سؤال.

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **الظنّ بأن الحدّ الأدنى أبسط من أن يُعرض (Thinking the baseline is too basic to show).** يتحقق منه مُجرو المقابلات مباشرة. بدلًا من ذلك، اجعله مرئيًا (make it visible): سجلّ نظيف (clean history)، واختبارات (tests)، وملف README، وتقرير عن تصحيح خطأ (debugging write-up).
- **إيداع واحد ضخم في النهاية (One giant commit at the end).** يُخفي طريقتك في العمل (hides your process) ويجعل المراجعة مستحيلة (makes review impossible). أودِع خطوات صغيرة عاملة (small, working steps) أولًا بأول.
- **تغيير عدة أشياء دفعة واحدة أثناء تصحيح الأخطاء (Changing several things at once while debugging).** تفقد القدرة على معرفة ما الذي أصلح المشكلة. أعِد الإنتاج (reproduce)، ثم اختبر فرضية واحدة في كل مرة (one hypothesis at a time).
- **إصلاح خطأ دون اختبار (Fixing a bug without a test).** يعود الخطأ (the bug comes back) ولا يستطيع أحد التحقق من ادّعائك (verify your claim). أضِف اختبار انحدار (regression test) يفشل قبل الإصلاح.
- **السؤال بعبارة "لا يعمل، ساعدوني؟" ⁦(Asking "it doesn't work, help?")⁩.** يكلّف المهندسَ الأقدم (senior) عشر دقائق ليكتشف ما تعرفه أنت أصلًا. اسأل مع ذكر الهدف (goal)، والتوقّع (expectation)، والنتيجة الفعلية (actual result)، وما جرّبته (what you tried).

## 🧾 الخلاصة (Recap)
- الحدّ الأدنى للمبتدئ (junior baseline) خمس مهارات يومية (five everyday skills): Git، وقراءة الشيفرة (reading code)، وتصحيح الأخطاء (debugging)، والاختبار (testing)، والتوثيق الكتابي (writing it down).
- صحّح الأخطاء بحلقة (debug with a loop): أعِد الإنتاج (reproduce)، ولاحِظ (observe)، وكوّن فرضية واحدة (one hypothesis)، واختبرها (test it)، وأصلِح مع اختبار (fix with a test)، وتحقّق (verify).
- كل إصلاح يحصل على اختبار انحدار (regression test)؛ وكل تغيير يحصل على رسالة تقول السبب (a message that says why).
- أدوات الذكاء الاصطناعي (AI tools) ترفع قيمة هذه المهارات: تصبح القراءة (reading) والتحقق (checking) والشرح (explaining) جزءًا أكبر من العمل.
- أظهِر الحدّ الأدنى بالأدلة (with evidence) — سجلّ المستودع (repository history)، والاختبارات، والتقارير المكتوبة (write-ups) — لا بالصفات (adjectives) في السيرة الذاتية (CV).

## ✍️ اختبر نفسك (Check yourself)

**1. في مقابلة المتابعة (follow-up) للمهمة المنزلية (take-home) الخاصة بعمر، يعرض طارق مُدخلًا فاشلًا (failing input) ويطلب منه أن يجد السبب (find the cause). ما الذي ينبغي أن يفعله عمر أولًا؟**

- A. أن يقرأ قاعدة الشيفرة (codebase) كلها من الأعلى ليفهم كل شيء قبل أن يلمس أي شيء
- B. أن يعيد إنتاج الإخفاق بشكل موثوق (reproduce the failure reliably) ويقرأ رسالة الخطأ وتتبّع المكدّس (error and stack trace)
- C. أن يغيّر الأسطر الثلاثة الأكثر احتمالًا دفعة واحدة (at once) لتوفير الوقت
- D. أن يعيد كتابة دالة التحليل (parsing function) بأسلوب أنظف (cleaner style)

<details><summary>الإجابة</summary>

**B.** لا يمكنك أن تعرف أنك أصلحت خطأً لا تستطيع إعادة إنتاجه (cannot reproduce)، وتتبّع المكدّس (stack trace) يشير إلى حيث ينبغي أن تنظر. الخيار C هو ما فعله عمر، وقد أخفى أيّ تغيير كان المؤثّر. (🟢 الأساسيات (The essentials)، حلقة تصحيح الأخطاء (debugging loop).)

</details>

**2. أيّ رسالة إيداع (commit message) تتّبع نصيحة هذا الدرس على أفضل وجه؟**

- A. `final version`
- B. `fixed bug`
- C. `changes to parser and tests and readme`
- D. `Parse statement dates as day-first`

<details><summary>الإجابة</summary>

**D.** تقول ما يفعله الإيداع (what the commit does)، بصيغة الأمر (in the imperative)، وتغطّي تغييرًا واحدًا (one change). الخيار C يذكر على الأقل ما الذي تغيّر، لكنه يجمع ثلاثة تغييرات غير مترابطة (bundles three unrelated changes) ولا يقول السبب. (🟢 الأساسيات (The essentials)، Git.)

</details>

**3. هدى عالقة أمام اختبار فاشل لاستيراد البيانات (failing data-import test) وتريد أن تطلب المساعدة من دانة في محادثة الفريق (team chat). أيّ رسالة هي الأكثر فائدة؟**

- A. "يفشل `pytest tests/test_import.py` مع الخطأ `KeyError: 'amount'` على ملف مارس (March file). كنت أتوقّع أن يُتجاوز صف العناوين (header row to be skipped). الملف فيه صف عناوين، وملف يناير ينجح. هل تغيّرت صيغة تصدير مارس (March export format)؟"
- B. "اختبارات الاستيراد (import tests) معطّلة مرة أخرى منذ دمج هذا الصباح (this morning's merge)، وليست لديّ أي فكرة عن السبب. هل يمكنك أن تلقي نظرة حين يتّسع وقتك اليوم؟"
- C. "هل يوجد أي توثيق (documentation) لشيفرة الاستيراد (import code)؟ أريد أن أفهم كيف يُقرأ ملف مارس قبل أن ألمس أي شيء فيه."
- D. "أظن أن في شيفرة الاستيراد خطأً (bug) في طريقة قراءة عمود المبلغ (amount column). هل ينبغي أن أعيد كتابة الوحدة كلها من الصفر (rewrite the whole module from scratch)؟"

<details><summary>الإجابة</summary>

**A.** تذكر الهدف (goal)، ورسالة الخطأ بنصّها (exact error)، والتوقّع (expectation)، وما تحقّقت منه بالفعل (what she already checked)، بحيث تستطيع دانة الإجابة بسرعة. الخيار B يبدو مهذّبًا لكنه يُجبر دانة على البدء من الصفر (start from zero). (🟢 الأساسيات (The essentials)، التوثيق الكتابي (writing it down).)

</details>

**4. أُعطيت مستودعًا غير مألوف (unfamiliar repository) وطُلب منك تغيير طريقة توليد تقرير واحد (how one report is generated). وفقًا لطريقة القراءة (reading method) في هذا الدرس، ما أفضل خطوة مبكرة بعد تشغيل المشروع؟**

- A. أن تقرأ كل ملف في المستودع بالترتيب الأبجدي (alphabetical order)، حتى لا يفوتك شيء
- B. أن تحذف الشيفرة التي تبدو غير مستخدمة (looks unused)، لتقليل ما يجب أن تقرأه وتراجعه
- C. أن تعثر على نقطة دخول التقرير (report's entry point)، وتتتبّعها عبر الشيفرة، وتقرأ اختباراتها (read its tests)
- D. أن تطلب من أداة ذكاء اصطناعي (AI tool) إعادة كتابة الوحدة كلها بأسلوب تفهمه مسبقًا

<details><summary>الإجابة</summary>

**C.** تتبّع إجراء حقيقي واحد (one real action) من نقطة دخوله (entry point)، مع الاختبارات بوصفها أمثلة (tests as examples)، هو أسرع طريق للدخول. الخيار B خطير: فالشيفرة التي "تبدو غير مستخدمة" (unused-looking) قد تعالج حالة لم ترها بعد. (🟢 الأساسيات (The essentials)، قراءة الشيفرة (reading code).)

</details>

**5. يقول خالد إن مهارات الحدّ الأدنى الخمس (five baseline skills) صارت أهمّ لا أقل، الآن وقد صار وكلاء الذكاء الاصطناعي (AI agents) يكتبون كثيرًا من الشيفرة الروتينية (routine code). لماذا؟**

- A. لأن أدوات الذكاء الاصطناعي لا تستطيع استخدام Git، فلا بدّ أن يُنشئ إنسانٌ كل إيداع (commit) يدويًا
- B. لأن الجهد البشري (human effort) ينتقل نحو التحقق من الشيفرة التي أنتجتها الأداة وشرحها (checking and explaining)
- C. لأن معظم أصحاب العمل حظروا الآن أدوات البرمجة بالذكاء الاصطناعي (AI coding tools) على المطوّرين المبتدئين (junior developers)
- D. لأن هذه المهارات ضرورية لاجتياز المقابلة (pass the interview)، حتى لو لم يعد العمل يستخدمها

<details><summary>الإجابة</summary>

**B.** حين تكتب الأداةُ الشيفرة، لا بدّ أن يتحقق منها أحد ويشرحها (check and explain it)، وهذا هو الحدّ الأدنى (baseline). الخيار C غير صحيح عمومًا؛ فالسياسات (policies) تختلف باختلاف صاحب العمل والمهمة. (🔴 نظرة الخبير (Expert view).)

</details>

## 📚 المراجع (References)
- سكوت شاكون وبن ستراوب (Scott Chacon and Ben Straub)، *Pro Git* (مجاني على الإنترنت (free online)) — https://git-scm.com/book/en/v2
- توثيق Git ‏(Git documentation)، `git bisect` — https://git-scm.com/docs/git-bisect
- الإيداعات الاصطلاحية (Conventional Commits) — https://www.conventionalcommits.org/
- توثيق GitHub ‏(GitHub Docs)، حول طلبات الدمج (About pull requests) — https://docs.github.com/en/pull-requests
- توثيق pytest ‏(pytest documentation) — https://docs.pytest.org/
- مركز مساعدة Stack Overflow ‏(Stack Overflow Help Center)، كيف تُنشئ مثالًا أدنى قابلًا لإعادة الإنتاج (How to create a Minimal, Reproducible Example) — https://stackoverflow.com/help/minimal-reproducible-example
- [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس F.3 — الإصدارات والمستودعات والنشر: كيف تنتقل البرمجيات (Versions, repos, and deploys — how software moves)](../vibe/index.ar.html#lF-3)

---

# 1.2 — البناء مع وكلاء البرمجة بالذكاء الاصطناعي (AI coding agents) دون أن يحملوك (without being carried by them)
*المستوى (Level): 🟢 مبتدئ (Beginner)* · *المتطلبات (Prerequisites): 1.1* · *الخطوة (Step): Learn, Build*

## ⚡ الدرس في دقيقة (In 60 seconds)
- يتوقّع كثير من أصحاب العمل (employers) أن يُحسن المطوّرون استخدام أدوات البرمجة بالذكاء الاصطناعي (AI coding tools). وهم يتحققون مما إذا كان **حُسن تقديرك (your judgement)** مرئيًا: أنت تحدّد المطلوب (specify)، وتقرأ (read)، وتتحقق (verify)، وتستطيع الشرح (explain).
- تكون **محمولًا (carried)** حين لا تستطيع شرح الشيفرة التي كتبها الوكيل (agent)، أو تغييرها، أو تصحيح أخطائها. ومُجرو المقابلات (interviewers) بارعون في كشف ذلك.
- القاعدة الأهم: **أنت تملك كل سطر تسلّمه (you own every line you submit)**، أيًّا كان من كتبه أو ما كتبه. إن لم تستطع شرحه، فلست مستعدًا لإيداعه (commit).
- إشارة القرار (Decision cue): قبل أن تقبل تغيير الوكيل (agent's change)، اسأل: "هل أستطيع شرح هذا الفرق (diff) سطرًا سطرًا لطارق، وإظهار كيف أعرف أنه يعمل؟" ⁦(could I explain this diff, line by line, to Tariq, and show how I know it works?)⁩
- النزاهة (Integrity): قواعد الذكاء الاصطناعي (AI rules) تختلف بين أصحاب العمل وبين الجولات (rounds). **اسأل دائمًا (Always ask)**، والتزم بالإجابة، وأفصح عن مساعدة الذكاء الاصطناعي بصدق (disclose AI help honestly).
- أكبر فخ (Biggest trap): استخدام الوكيل لتخطّي التعلّم (skip the learning). يظهر ذلك عند أول سؤال في المقابلة يتعمّق مستوى واحدًا (goes one level deeper).

## 🧭 لماذا يهم (Why it matters)
ريم هي الأسرع بناءً (fastest builder) في الدفعة (cohort): بمساعدة وكيل برمجة بالذكاء الاصطناعي (AI coding agent) بنت ثلاثة مشاريع جانبية (side projects) في شهر واحد. وفي المهمة المنزلية (take-home) لبنك نجم، التي سمحت بأدوات الذكاء الاصطناعي (AI tools) بشرط أن يذكر المرشّحون ما استخدموه، تسلّم خدمة مصقولة (polished service) في فترة ما بعد الظهر، مع اختبارات (tests) وملف README جيد، وتُفصح عن أدواتها (discloses her tools).

لكن مقابلة المتابعة (follow-up interview) تجري على نحو مختلف. يفتح طارق شيفرتها ويطرح ثلاثة أسئلة. "لماذا تنتظر حلقة إعادة المحاولة (retry loop) مدة أطول في كل مرة؟" ريم غير متأكدة؛ فالوكيل هو من أضافها. "هذا الاختبار يستخدم بديلًا وهميًا لقاعدة البيانات (mocks the database). ما الذي سيحدث مع قاعدة بيانات حقيقية لو وصل طلبان في الوقت نفسه (two requests arrived at once)؟" لا تعرف. "في ملف الإعدادات (config file) مفتاح واجهة برمجية (API key) داخل تجهيزة اختبار (test fixture). هل هو حقيقي؟" نعم هو حقيقي: مفتاح من الفئة المجانية (free-tier key) كانت قد لصقته في المحادثة مع الوكيل، فوضعه الوكيل في الملف. لا ينزعج طارق من استخدامها للذكاء الاصطناعي. ما يزعجه أن الشيفرة كانت أقدر من صاحبتها (more capable than its author).

ملاحظات خالد (Khalid's feedback): "ريم ممتازة في إنجاز البناء (getting things built). لكننا نحتاج إلى أن نرى أنها هي المسيطرة على ما يُبنى (in charge of what gets built)." يدور هذا الدرس حول هذا الفرق.

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**ثلاثة مستويات من مساعدة الذكاء الاصطناعي (Three levels of AI help).** تختلف أدوات البرمجة (coding tools) بحسب مقدار ما تفعله من تلقاء نفسها (on their own):

| المستوى (Level) | ماذا يفعل (What it does) | أمثلة (Examples) (وقت كتابة هذا الدرس، 2026) | الخطر الرئيسي على المبتدئ (Main risk for a junior) |
|---|---|---|---|
| الإكمال التلقائي (Autocomplete) | يقترح الأسطر التالية أثناء الكتابة (suggests the next lines as you type) | الاقتراحات المضمّنة (inline suggestions) في GitHub Copilot ومعظم المحرّرات (editors) | قبول أسطر تبدو معقولة (plausible lines) دون قراءتها |
| مساعد المحادثة (Chat assistant) | يجيب عن الأسئلة ويكتب مقتطفات (snippets) تلصقها بنفسك | لوحات المحادثة في المحرّرات (editor chat panels)؛ المساعدات العامة (general assistants) | لصق شيفرة في سياق لا يناسبها (a context it does not fit) |
| وكيل البرمجة (Coding agent) | يقرأ المستودع (repository)، ويعدّل ملفات كثيرة، ويشغّل الأوامر والاختبارات (runs commands and tests)، ويكرّر المحاولة (iterates) | Claude Code، وميزات الوكيل في GitHub Copilot ‏(GitHub Copilot's agent features)، ووضع الوكيل في Cursor ‏(Cursor's agent mode)، وغيرها | تغييرات كبيرة واثقة (large, confident changes) لم تقرأها كاملة قط |

الأدوات تتغيّر بسرعة؛ أما المبادئ (principles) التالية فلا تتغيّر.

**ما الذي يتحقق منه أصحاب العمل (What employers check).** خلف أسئلة المقابلة، تكمن هذه الأسئلة:
- **هل تستطيع التحديد؟ ⁦(Can you specify?)⁩** هل تستطيع تحويل طلب مبهم (vague request) إلى مهمة صغيرة واضحة (clear, small task) بمعايير قبول (acceptance criteria)؟
- **هل تستطيع المراجعة؟ ⁦(Can you review?)⁩** هل تقرأ الفرق (diff) — أي الأسطر التي تغيّرت بالضبط (the exact lines changed) — وتلاحظ ما هو خاطئ (wrong) أو ناقص (missing) أو غير ضروري (unnecessary)؟
- **هل تستطيع التحقق؟ ⁦(Can you verify?)⁩** هل تُثبت أنه يعمل بالاختبارات والتشغيل الفعلي (tests and real runs)، بدلًا من الثقة بملخّص الوكيل (agent's summary)؟
- **هل تستطيع الشرح؟ ⁦(Can you explain?)⁩** هل تستطيع أن تقول لماذا يوجد كل جزء (why each part is there)، وما الذي كنت ستغيّره؟
- **هل أنت صادق؟ ⁦(Are you honest?)⁩** هل تلتزم بقواعد استخدام الذكاء الاصطناعي (rules about AI use) وتذكر ما استخدمته؟

لاحظ أن هذه هي مهارات الحدّ الأدنى (baseline skills) في الدرس 1.1، موجّهةً إلى شيفرة كتبها غيرك (someone else) — أي الوكيل.

**سير عمل يُبقيك مسيطرًا (A workflow that keeps you in charge).**

```mermaid
flowchart RL
    S["حدّد مهمة صغيرة بمعايير قبول<br/>(Specify a small task with acceptance criteria)"] --> G["يقترح الوكيل التغيير أو يكتبه<br/>(Agent proposes or writes the change)"]
    G --> R["تقرأ الفرق كاملًا<br/>(You read the whole diff)"]
    R -->|"غير واضح أو خاطئ (unclear or wrong)"| S
    R --> V["شغّل الاختبارات وأجرِ تحقّقًا فعليًا<br/>(Run tests and a real check)"]
    V -->|"فشل (fails)"| S
    V --> E["اشرح بالعكس: هل تستطيع الدفاع عن كل سطر<br/>(Explain-back: could you defend every line)"]
    E -->|"لا (no)"| L["تعلّم الجزء الذي لا تستطيع شرحه<br/>(Learn the part you cannot explain)"]
    L --> E
    E -->|"نعم (yes)"| C["أودِع برسالة صادقة<br/>(Commit with an honest message)"]
```

ثلاث عادات تجعل هذه الحلقة (loop) تعمل:
1. **مهام صغيرة (Small tasks).** مهمة "تحقّق من حقل المبلغ (Validate the amount field)، رافضًا القيم السالبة وغير الرقمية (rejecting negatives and non-numbers)، مع اختبارات" قابلة للمراجعة (reviewable)؛ أما "ابنِ الواجهة الخلفية" (build the backend) فليست كذلك.
2. **اقرأ الفرق كاملًا (Read the whole diff)،** لا ملخّص الوكيل (agent's summary). فالوكلاء يُبلغون أحيانًا عن نجاح (report success) لعمل غير مكتمل (incomplete work)، أو يلمسون ملفات لم تذكرها.
3. **اختبار الشرح بالعكس (The explain-back test).** قبل الإيداع (before committing)، اشرح التغيير كأنك تشرحه لمراجع (reviewer). كل تردّد (hesitation) هو شيء عليك أن تتعلّمه قبل أن تُودِع.

**قواعد النزاهة (Integrity rules).** استخدام الذكاء الاصطناعي ليس غشًّا (not cheating) حين يكون مسموحًا. أما هذه الأمور فهي غشّ:
- ادّعاء أن عملًا كتبه الذكاء الاصطناعي هو عملك الخاص دون مساعدة (your own unaided work) حين طُلب منك أن تعمل وحدك (work alone).
- استخدام الذكاء الاصطناعي في جولة مقابلة (interview round) لا يُسمح فيها بذلك، بما في ذلك الأدوات الخفية (hidden tools) التي تلقّنك الإجابات أثناء مقابلة مباشرة (live interview).
- تسليم شيفرة لا تستطيع شرحها (code you cannot explain) بوصفها دليلًا على مهارتك.
- لصق شيفرة أو بيانات سرّية (confidential code or data) لصاحب عمل أو جامعة في أداة غير معتمدة لذلك (not approved for it).

القاعدة العملية (The practical rule): **اسأل قبل كل تقييم (ask before every assessment)** ("هل يُسمح بأدوات الذكاء الاصطناعي في هذه الجولة؟ هل ينبغي أن أذكر ما استخدمته؟" ⁦(Are AI tools allowed in this round? Should I say which I used?)⁩). كثير من أصحاب العمل يسمحون بالذكاء الاصطناعي أو يتوقّعونه في بعض الجولات، كالمهام المنزلية (take-homes)، ويحظرونه في جولات أخرى، كجولات الخوارزميات المباشرة (live algorithm rounds). لا تفترض أبدًا (Never assume).

### 🟡 التعمق أكثر (Going deeper)

**ما الذي يخطئ فيه الوكلاء عادةً (What agents commonly get wrong).** معرفة الإخفاقات المعتادة (usual failures) تخبرك أين تنظر في الفرق (diff):

| الإخفاق (Failure) | كيف يبدو (What it looks like) | كيف تكتشفه (How to catch it) |
|---|---|---|
| واجهات برمجية أو حزم مُختلَقة (Invented APIs or packages) | دالة أو مكتبة غير موجودة (does not exist)، أو اسم حزمة يكاد يكون صحيحًا (almost right) | شغّله؛ راجع التوثيق الرسمي (official docs)؛ تحقّق من سجلّ الحزم (package registry) قبل التثبيت |
| حالات حدّية تبدو معقولة لكنها خاطئة (Plausible but wrong edge cases) | يعمل مع المثال؛ ويفشل مع المُدخل الفارغ (empty input)، أو المناطق الزمنية (time zones)، أو تقريب العملات (currency rounding)، أو الطلبات المتزامنة (concurrent requests) | اكتب بنفسك اختبارات للحالات الحدّية (tests for the edges) قبل أن تطلب الشيفرة |
| تغييرات واسعة أكثر من اللازم (Over-broad changes) | طُلب منه إصلاح خطأ واحد، فـ"رتّب" (tidied) أيضًا خمسة ملفات لا علاقة لها بالأمر | اقرأ قائمة الملفات الكاملة (full file list) في الفرق؛ ارفض التغييرات التي لم تطلبها |
| اختبارات مُضعَفة (Weakened tests) | يُعدَّل اختبار فاشل أو يُحذف حتى ينجح (until it passes) | اعتبر أي تغيير في الاختبارات مثيرًا للريبة (suspicious)؛ واسأل لماذا كان الاختبار خاطئًا |
| إعدادات افتراضية غير آمنة (Insecure defaults) | SQL مبنيّ بتجميع النصوص (string-built SQL)، أو غياب فحوص التفويض (missing authorisation checks)، أو أسرار في الشيفرة (secrets in code)، أو إعدادات متساهلة أكثر من اللازم (overly permissive settings) | استخدم قائمة تحقق أمنية (security checklist)؛ شغّل فحص الأسرار (secret scanning) والتحليل الساكن (static analysis) |
| ملخّصات واثقة لكنها خاطئة (Confident wrong summaries) | "جميع الاختبارات ناجحة" (All tests pass) بينما جرى تخطّي بعضها (some were skipped) | شغّل الاختبارات بنفسك واقرأ المُخرَج (read the output) |

تتناول المكتبة هذه الأمور بعمق: [*أمن الذكاء الاصطناعي والتطبيقات (Secure AI & Application Security)*، الدرس 6.3 — تأمين الشيفرة المولَّدة بالذكاء الاصطناعي: ما الذي يخطئ فيه وكلاء البرمجة (Securing AI-generated code: what coding agents get wrong)](../secai/index.ar.html#/6.3) للجانب الأمني (security side)، و[*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 9.4 — التحقق قبل الإكمال (Verification before completion)](../vibe/index.ar.html#l9-4) لعادة إثبات أن العمل قد أُنجز (proving work is done).

**التحديد بالاختبارات أولًا (Specifying with tests first).** اكتب حالات الاختبار (test cases) قبل أن يكتب الوكيل الشيفرة: أنت تقرّر ما معنى "صحيح" (what "correct" means)، وعلى الوكيل أن يستوفيه. مُوجِّه (prompt) كهذا يُظهر حُسن تقدير مرئيًا (visible judgement):

```text
Task: add amount validation to POST /transactions.
Rules: reject negative amounts, zero, non-numeric strings and more
than 2 decimal places, with HTTP 422 and a clear error message.
Do not change any other endpoint. Do not modify existing tests.
First, show me the test cases you will add. Wait for my approval
before writing the implementation.
```

يبني [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 8.2 — الاختبارات بوصفها المواصفة التي لا يستطيع الوكيل تجاهلها (Tests as the spec the agent can't ignore)](../vibe/index.ar.html#l8-2) هذه العادة بالكامل.

**كيف تختبر المقابلاتُ ذلك (How interviews probe it).** توقّع بعض هذه الأشكال، واسأل مسبقًا أيّها ينطبق:
- **"اشرح لي مهمتك المنزلية" (Walk me through your take-home).** يختار مُجري المقابلة سطرًا عشوائيًا (random line) ويسأل عن سببه. هنا يُكشف المرشّحون المحمولون (carried candidates).
- **"وسّعها مباشرةً" (Extend it live)،** أحيانًا دون أدوات الذكاء الاصطناعي.
- **البرمجة المباشرة مع السماح بالذكاء الاصطناعي (AI-allowed live coding).** يراقب مُجري المقابلة كيف تكتب المُوجِّهات (prompt)، وتقرأ (read)، وتتحقق (verify).
- **مراجعة طلب دمج معيب كتبه الذكاء الاصطناعي (Reviewing a flawed AI-written pull request).** يُذكر أنه تمرين يزداد شيوعًا (increasingly common exercise) وقت كتابة هذا الدرس (2026)؛ ويتناوله الدرس 5.2.
- **جولات الخوارزميات دون ذكاء اصطناعي (Algorithm rounds without AI).** لا تزال شائعة في شركات التقنية الكبيرة (large technology firms). وهي تختبر تفكيرًا لا يمكنك استعارته (reasoning you cannot borrow).

**وضع التعلّم مقابل وضع الإنتاج (Learning mode versus producing mode).** حين تكون في وضع **التعلّم (learning)**، اطلب من الوكيل أن يشرح (explain)، أو يختبرك (quiz you)، أو يراجع شيفرة كتبتها *أنت* (review code *you* wrote). وحين تكون في وضع **الإنتاج (producing)** في مجال تفهمه، دعه يكتب أكثر، وراجع بعناية (review carefully). بقيت ريم في وضع الإنتاج في موضوعات — كإعادة المحاولة (retries) والتزامن (concurrency) — لم تتعلّمها قط. قاعدة بسيطة (A simple rule): **في أول مرة تستخدم فيها مفهومًا ما، اكتبه بنفسك أو ادرسه حتى تصبح قادرًا على كتابته (the first time you use a concept, write it yourself or study it until you could).**

**السرعة ليست هي الإنتاجية (Speed is not the same as productivity).** في دراسة أجرتها METR، وهي منظمة غير ربحية لأبحاث الذكاء الاصطناعي (AI research non-profit)، في يوليو 2025، كان المطوّرون المتمرّسون في المشاريع مفتوحة المصدر (experienced open-source developers) الذين يعملون على مستودعاتهم الخاصة أبطأ في المتوسط (on average slower) مع أدوات الذكاء الاصطناعي، رغم أنهم اعتقدوا أن الأدوات سرّعتهم (sped them up). كانت دراسة واحدة في بيئة واحدة (one study in one setting)، وقد تغيّرت الأدوات منذ ذلك الحين؛ فقِس نتائجك بنفسك (measure your own results) بدلًا من الثقة بالإحساس بالسرعة (feeling of speed).

### 🔴 نظرة الخبير (Expert view)

**أنت توجّه زميلًا في الفريق (You are directing a teammate).** الوكيل (agent) زميل سريع واسع الاطلاع (fast, widely read colleague) لا يقول أبدًا "لا أعرف" (I don't know): يحتاج إلى مهام واضحة (clear tasks)، وسياق (context)، ومراجعة (review). تعلّم المكتبة هذه المهارات في [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 9.1 — أنت المعماري الآن (You are the architect now)](../vibe/index.ar.html#l9-1)، و[*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 9.2 — هندسة السياق (Context engineering)](../vibe/index.ar.html#l9-2)، و[المسار التعليمي لـ*تشغيل وكلاء الذكاء الاصطناعي في الإنتاج (Running AI Agents in Production)*، المستوى 1 — البنّاء (Level 1 — Builder)](../agentic/learning-path.ar.html#level-1-builder). بالنسبة إلى المبتدئ، فإن ملف تعليمات الوكيل (agent instruction file)، والاختبارات المكتوبة قبل الشيفرة (tests written before code)، والإيداعات الصغيرة المُراجَعة (small reviewed commits) هي *أدلة (evidence)* على أنك المسيطر.

**إلى أين تنتقل القيمة (Where the value moves).** حين يصبح توليد الشيفرة رخيصًا (code is cheap to generate)، تصبح المهارات النادرة (scarce skills) هي: تقرير ما يُبنى (deciding what to build)، وتقسيمه إلى أجزاء قابلة للتحقق (checkable pieces)، وملاحظة ما هو خاطئ (noticing what is wrong)، وتشغيل النتيجة (operating the result) (الدرس 1.3). وأساسيات علوم الحاسوب (computer science fundamentals) لديك هي ما تكتشف به أخطاء الوكيل (spot the agent's mistakes).

**إفصاح يبني الثقة (Disclosure that builds trust).** تكفي ملاحظة قصيرة في ملف README أو طلب دمج (pull request): أي أداة (which tool)، ولأي غرض (for what)، وكيف تحقّقت منها (how you verified it). "استخدمتُ وكيل برمجة بالذكاء الاصطناعي لبناء الهيكل الأولي لمسارات الواجهة البرمجية (scaffold the API routes) وصياغة مسوّدات الاختبارات (draft tests)؛ وكتبتُ بنفسي قواعد التحقق (validation rules) وحالات الاختبار (test cases)، وراجعتُ كل تغيير، وأضفتُ اختبار التزامن (concurrency test) بعد أن وجدتُ حالة تسابق (race) في الشيفرة المولَّدة (generated code)." هذه الجملة نقطة قوة (strength) في المقابلة، لا اعتراف (not a confession).

**بيانات صاحب العمل وأدواته (Employer data and tools).** في بنك مثل نجم، الشيفرة والبيانات سرّية وخاضعة للتنظيم (confidential and regulated)، وعادةً ما يعتمد أصحاب العمل أدوات ذكاء اصطناعي محدّدة لبيانات محدّدة (approve specific AI tools for specific data). اعرف ما هو معتمد (what is approved) قبل أن تلصق أي شيء؛ وذِكرُ ذلك في المقابلات يُظهر وعيًا (awareness) يقدّره أصحاب العمل الخاضعون للتنظيم (regulated employers). منظور الحوكمة (governance view) موجود في [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 9.8 — نظرة على الحوكمة: أنت تملك ما يُطلقه وكيلك (The governance glance: you own what your agent ships)](../vibe/index.ar.html#l9-8).

## 🧰 الأدوات (The toolkit)
| المورد أو الأداة أو النموذج (Resource, tool or template) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **AI coding agent** — وكيل البرمجة بالذكاء الاصطناعي (على سبيل المثال Claude Code، وGitHub Copilot، وCursor) | أدوات تقرأ المستودع (read a repository)، وتعدّل الملفات (edit files)، وتشغّل الأوامر (run commands)، وتكرّر العمل على المهمة (iterate on a task) | إنتاج الشيفرة في مجالات تفهمها، تحت المراجعة والاختبارات (under review and tests) |
| **Explain-back test** — اختبار الشرح بالعكس | شرح التغيير سطرًا سطرًا (line by line)، بصوت عالٍ أو كتابةً، قبل إيداعه | كل تغيير كتبه الوكيل؛ ودائمًا قبل مقابلة عن مشروعك الخاص |
| **Test-first prompt** — مُوجِّه الاختبارات أولًا | مُوجِّه (prompt) يثبّت القواعد (fixes the rules) ويطلب حالات الاختبار (test cases) قبل التنفيذ (implementation) | أي مهمة يكون لـ"الصحيح" فيها حالات حدّية (edge cases): المال (money)، والتواريخ (dates)، والصلاحيات (permissions) |
| **Diff review checklist** — قائمة التحقق لمراجعة الفرق | قائمة قصيرة بما يجب فحصه في الفرق (diff): النطاق (scope)، والاختبارات (tests)، والأمن (security)، والأسرار (secrets)، والواجهات البرمجية المُختلَقة (invented APIs) | مراجعة تغيير الوكيل، أو طلب دمج معيب (flawed pull request) في مقابلة |
| **AI use log** — سجلّ استخدام الذكاء الاصطناعي | ملاحظة مستمرة (running note) بالمواضع التي ساعد فيها الذكاء الاصطناعي، وما غيّرته، وكيف تحقّقت منه | كتابة إفصاحات صادقة (honest disclosures) |
| **Secret scanning** — فحص الأسرار (على سبيل المثال gitleaks، والحماية عند الدفع في المنصّة (platform push protection)) | يكتشف المفاتيح وكلمات المرور (keys and passwords) في الشيفرة قبل دفعها (before they are pushed) | كل مستودع، وخاصة حين يعدّل الوكلاء ملفات الإعدادات (config) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
بعد مقابلة ريم، يكتب خالد وطارق **قواعد العمل بمساعدة الذكاء الاصطناعي (AI-assisted work rules)** في صفحة واحدة، يتسلّمها كل خرّيج في نجم في اليوم الأول (day one). كيّفها لتناسبك (Adapt them).

**الجزء أ: القواعد (Part A: the rules)**

| القاعدة (Rule) | ماذا تعني عمليًا (What it means in practice) |
|---|---|
| استخدم الأدوات المعتمدة فقط (Use approved tools only) | فقط الأدوات المدرجة في القائمة الداخلية (internal list)، وبإعداداتها. لا تذهب أي شيفرة لنجم أو بيانات عملاء (customer data) إلى أي مكان آخر. |
| أنت تملك كل سطر (You own every line) | أيًّا كان من كتبه، فاسمك على الإيداع (your name is on the commit). إن لم تستطع شرحه، فلا تُودِعه. |
| مهام صغيرة ومحدّدة (Small, specified tasks) | أعطِ الوكيل مهامّ تستطيع مراجعتها في خمس عشرة دقيقة، مع معايير قبول (acceptance criteria). |
| الاختبارات ملكك (Tests are yours) | اكتب حالات الاختبار أو وافق عليها بنفسك. أي تغيير في اختبار قائم (existing test) يحتاج إلى سبب في طلب الدمج. |
| أفصِح في طلب الدمج (Disclose in the pull request) | سطر واحد: الأداة (tool)، وما فعلته (what it did)، وكيف تحقّقت منه (how you verified it). |
| التعلّم أولًا (Learning first) | في أول مرة تقابل فيها مفهومًا (concept)، اكتبه بنفسك أو ادرسه حتى تصبح قادرًا على كتابته. |

**الجزء ب: كتلة الإفصاح والتحقق في طلب الدمج (Part B: the pull request disclosure and verification block)** (كتلة ريم، في أول طلب دمج لها في نجم)

```text
AI assistance and verification:
- Tool: approved coding agent (internal list, version as configured).
- Used for: drafting the retry wrapper and its tests.
- I wrote: the retry policy (3 attempts, exponential backoff with jitter,
  only on timeouts and 503s, never on 4xx; every attempt reuses the
  same idempotency key, so a retry cannot pay twice), and the test cases.
- Verified by: unit tests (12, all mine or reviewed line by line);
  a manual run against the sandbox with the payment service stopped;
  secret scan clean.
- I changed from the draft: removed a retry on 400 errors
  (would have resent invalid requests) and a hard-coded timeout.
```

تعليق طارق (Tariq's comment): "أستطيع أن أرى أين ساعد الوكيل (where the agent helped)، وأين نقضتِ قراره (where you overruled it)، وكيف تعرفين أنه يعمل (how you know it works)."

## 🛠️ التمارين (Exercises)
- 🟢 لثلاثة ملفات من مشروع بنيته بمساعدة كبيرة من الذكاء الاصطناعي (heavy AI help)، أجرِ اختبار الشرح بالعكس (explain-back test) كتابةً: جملة أو جملتان لكل دالة (per function) عمّا تفعله ولماذا. علِّم كل فجوة (Mark every gap). *يكتمل عندما (Done when):* تكون الملاحظة موجودة، وتكون كل فجوة معلَّمة إمّا قد تعلّمتها (مع إضافة جملة) أو أدرجتها بندًا للدراسة لاحقًا (next study item).
- 🟡 اختر ميزة صغيرة (small feature) لأحد مشاريعك. اكتب حالات الاختبار أولًا (test cases first)، ثم استخدم وكيلًا مع مُوجِّه الاختبارات أولًا (test-first prompt) لتنفيذها. راجع الفرق (diff) باستخدام قائمة التحقق من 🟡 التعمق أكثر (Going deeper)، وسجّل كل تغيير رفضته أو عدّلته (rejected or edited). *يكتمل عندما (Done when):* تُدمج الميزة عبر طلب دمج (pull request) يتضمّن وصفُه كتلة مساعدة الذكاء الاصطناعي والتحقق (AI-assistance and verification block) مثل كتلة نجم، ويُسجَّل تغيير واحد على الأقل رُفض أو عُدّل مع ذكر السبب.
- 🔴 مع صديق، يستخدم كلٌّ منكما وكيلًا لإضافة ميزة صغيرة إلى مشروع الآخر، ثم يزرع خللًا واقعيًا واحدًا (plant one realistic flaw): غياب فحص تفويض (missing authorisation check)، أو اختبار مُضعَف (weakened test)، أو خطأ بفارق يوم في تاريخ (date off-by-one)، أو سرّ مكتوب مباشرة في الشيفرة (hard-coded secret). راجعا طلب دمج كلٍّ منكما للآخر دون تمهيد (cold)، في 20 دقيقة. *يكتمل عندما (Done when):* يكون كلٌّ منكما قد كتب تعليقات المراجعة (review comments)، وتقارنانها بالخلل المزروع (planted flaw)، وتدوّنان ما فاتكما ولماذا.

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **تسليم شيفرة لا تستطيع شرحها (Submitting code you cannot explain).** أسرع طريق للرسوب في مقابلة المتابعة (follow-up interview). أجرِ اختبار الشرح بالعكس (explain-back test) قبل كل إيداع.
- **افتراض قواعد الذكاء الاصطناعي (Assuming AI rules).** القواعد تختلف باختلاف صاحب العمل والجولة (by employer and by round). اسأل كتابةً (ask in writing) قبل التقييم والتزم بالإجابة.
- **إخفاء استخدام الذكاء الاصطناعي، أو المبالغة في الاعتذار عنه (Hiding AI use, or over-apologising for it).** كلاهما يضرّ بالثقة (damage trust). أفصِح باختصار (disclose briefly)، مع ذكر كيف تحقّقت.
- **ترك الوكيل يغيّر الاختبارات لتنجح (Letting the agent change tests to make them pass).** اعتبر أي تغيير في الاختبارات سؤالًا تصميميًا (design question) يحتاج إلى سبب.
- **تخطّي التعلّم (Skipping the learning).** إنتاج شيفرة في موضوع لم تدرسه قط يتركك أجوف (hollow) فيه. اكتبها بنفسك في المرة الأولى.

## 🧾 الخلاصة (Recap)
- يتحقق أصحاب العمل من حُسن التقدير (judgement) حين تستخدم أدوات الذكاء الاصطناعي: التحديد (specify)، والمراجعة (review)، والتحقق (verify)، والشرح (explain)، والصدق (be honest).
- تكون محمولًا (carried) حين لا تستطيع شرح ما كتبه الوكيل، أو تغييره، أو تصحيح أخطائه.
- اعمل بمهام صغيرة ومحدّدة (small, specified tasks)، واقرأ الفرق كاملًا (whole diff)، وتحقّق باختباراتك وتشغيلك الخاص (your own tests and runs)، ثم اشرح بالعكس (explain back).
- اعرف إخفاقات الوكلاء الشائعة (common agent failures): الواجهات البرمجية المُختلَقة (invented APIs)، والحالات الحدّية الخاطئة (wrong edge cases)، والتغييرات الواسعة أكثر من اللازم (over-broad changes)، والاختبارات المُضعَفة (weakened tests)، والإعدادات الافتراضية غير الآمنة (insecure defaults)، والملخّصات الواثقة (confident summaries).
- اسأل دائمًا عن قواعد الذكاء الاصطناعي في كل تقييم (each assessment)، وأفصِح باختصار، ولا تلصق أبدًا شيفرة سرّية (confidential code) في أدوات غير معتمدة (unapproved tools).
- أساسيات علوم الحاسوب (computer science fundamentals) لديك هي ما تكتشف به أخطاء الوكيل.

## ✍️ اختبر نفسك (Check yourself)

**1. سمحت المهمة المنزلية (take-home) لريم بأدوات الذكاء الاصطناعي (AI tools)، وقد أفصحت عنها. فلماذا جرت مقابلة المتابعة (follow-up interview) على نحو سيئ رغم ذلك؟**

- A. استخدام الذكاء الاصطناعي في المهمة المنزلية سبب دائم للرفض (always a reason for rejection)، حتى حين يكون مسموحًا
- B. لم تكن في شيفرتها اختبارات (no tests)، فلم يستطع طارق أن يعرف هل يعمل أي جزء منها
- C. لم تستطع شرح أجزاء أساسية من شيفرتها (explain key parts of her own code)، مثل منطق إعادة المحاولة (retry logic)
- D. استخدمت أداة ذكاء اصطناعي غير مدرجة في قائمة الأدوات المعتمدة (approved tools) لدى صاحب العمل

<details><summary>الإجابة</summary>

**C.** كانت المشكلة أنها محمولة (being carried): الشيفرة كانت أقدر من صاحبتها (more capable than its author). الخيار A خاطئ: فالجولة سمحت بالذكاء الاصطناعي، ولم يمانع طارق ذلك. (🧭 لماذا يهم (Why it matters).)

</details>

**2. دُعي محمد إلى مقابلة تقنية (technical interview) لدى سديم باي (Sadeem Pay). الدعوة (invitation) لا تذكر أدوات الذكاء الاصطناعي. ماذا ينبغي أن يفعل؟**

- A. أن يسأل مسؤول التوظيف (recruiter) كتابةً عمّا إذا كانت أدوات الذكاء الاصطناعي مسموحة في كل جولة (each round)، ويلتزم بالإجابة
- B. أن يستخدم أدوات الذكاء الاصطناعي في كل الجولات، ما دامت الدعوة لا تمنعها
- C. أن يتجنّب ذكر الذكاء الاصطناعي تمامًا، حتى لا يُطرح السؤال أبدًا خلال العملية
- D. أن يستخدم مساعد ذكاء اصطناعي (AI assistant) خفيةً في نافذة ثانية (second window) أثناء الجولة المباشرة (live round)

<details><summary>الإجابة</summary>

**A.** القواعد تختلف بين أصحاب العمل وبين الجولات، لذا فالقاعدة هي أن تسأل (ask)، ولا تفترض أبدًا (never assume). الخيار D عدم أمانة صريح (plain dishonesty)، والخيار B يفترض إذنًا (assumes permission) قد لا يكون موجودًا. (🟢 الأساسيات (The essentials)، قواعد النزاهة (integrity rules).)

</details>

**3. يُبلغ وكيلٌ (agent) بأنه "أصلح الخطأ، وجميع الاختبارات ناجحة" ⁦(Fixed the bug, all tests pass)⁩. ويُظهر الفرق (diff) أنه عدّل أيضًا القيمة المتوقَّعة (expected value) في اختبار قائم (existing test). ما أفضل ردّ؟**

- A. أن تقبله، لأن مجموعة الاختبارات كاملة (full suite) ناجحة والوكيل يقول إن الخطأ أُصلح
- B. أن تطلب من الوكيل تلخيص تغييره مرة أخرى (summarise its change again)، بتفصيل أكبر هذه المرة
- C. أن تتراجع عن تغيير الاختبار وحده (revert only the test change) وتدمج الباقي دون تشغيل أي شيء
- D. أن تعرف لماذا تغيّرت القيمة المتوقَّعة وتشغّل مجموعة الاختبارات بنفسك (run the suite yourself)

<details><summary>الإجابة</summary>

**D.** إضعاف الاختبارات (Weakening tests) إخفاق شائع لدى الوكلاء؛ ومجموعة اختبارات ناجحة لا تعني الكثير إذا لُوي الاختبار ليطابق الخطأ (bent to match the bug)، لذا اعتبر التعديل مثيرًا للريبة (suspicious) ولا تقبله إلا مع سبب معلَن (stated reason). الخيار C لا يثق بالتعديل لكنه يدمج دون تحقق (merges unverified). (🟡 التعمق أكثر (Going deeper)، ما الذي يخطئ فيه الوكلاء عادةً (what agents commonly get wrong).)

</details>

**4. تريد هدى أن تتعلّم كيف تعمل معاملات قاعدة البيانات (database transactions)، وهي تحتاج إليها في مشروعها. وفقًا لهذا الدرس، كيف ينبغي أن تستخدم أداة الذكاء الاصطناعي لديها؟**

- A. أن تدع الوكيل يكتب كل شيفرة المعاملات، لأن ذلك أسرع وتستطيع قراءتها لاحقًا
- B. أن تكتبها بنفسها أولًا (write it herself first)، مستخدمةً الأداة للشرح (explain)، واختبارها (quiz her)، ومراجعة شيفرتها (review her code)
- C. أن تتجنّب أدوات الذكاء الاصطناعي تمامًا لبقية المشروع، لكي تتعلّم كل شيء بالطريقة الصعبة (the hard way)
- D. أن تنسخ مثالًا على المعاملات من نافذة المحادثة في الأداة (tool's chat window) وتعدّله حتى تنجح الاختبارات

<details><summary>الإجابة</summary>

**B.** هذا هو وضع التعلّم (learning mode): في أول مرة تقابل فيها مفهومًا، اكتبه بنفسك أو ادرسه حتى تصبح قادرًا على كتابته، واستخدم الأداة معلّمًا (tutor) ومراجعًا (reviewer). أما الخياران A وD فيُبقيانها في وضع الإنتاج (producing mode) ويتركانها عاجزة عن شرح النتيجة أو تصحيح أخطائها. (🟡 التعمق أكثر (Going deeper)، وضع التعلّم مقابل وضع الإنتاج (learning mode versus producing mode).)

</details>

**5. أيّ ملاحظة في طلب الدمج (pull request note) تُظهر على أفضل وجه الإفصاح الصادق والمفيد (honest, useful disclosure) الذي يوصي به هذا الدرس؟**

- A. "كتبتُه كله بنفسي، من الصفر، خلال عطلة نهاية الأسبوع. كل سطر هو عملي الخاص، ويسعدني شرح أي جزء منه."
- B. "صاغ وكيلٌ مسوّدة المسارات والاختبارات (drafted the routes and tests)؛ وكتبتُ قواعد التحقق (validation rules)، وراجعتُ كل تغيير، وأضفتُ اختبارًا لحالة تسابق (race) وجدتُها."
- C. "آسفة، استخدمتُ الذكاء الاصطناعي في معظم هذا العمل. أعرف أن هذا ليس مثاليًا، وسأحاول أن أكتب المزيد منه بنفسي في المرة القادمة."
- D. "مولَّد بالذكاء الاصطناعي باستخدام وكيل (AI-generated with an agent). لم يتّسع وقتي لمراجعته كله، لذا يُرجى فحصه بعناية قبل الدمج."

<details><summary>الإجابة</summary>

**B.** تقول ما فعله الوكيل (what the agent did)، وما فعلتَه أنت (what you did)، وكيف تحقّقت منه (how you verified it). الخيار D يُلقي عبء التحقق على المراجع (hands verification to the reviewer)؛ والخيار A غير صادق (dishonest) إن كان الذكاء الاصطناعي قد ساعد؛ والخيار C يعتذر دون تفاصيل مفيدة (without useful detail). (🔴 نظرة الخبير (Expert view)، إفصاح يبني الثقة (disclosure that builds trust).)

</details>

## 📚 المراجع (References)
- METR — https://metr.org/ (دراسة عن أدوات الذكاء الاصطناعي وإنتاجية المطوّرين المتمرّسين في المشاريع مفتوحة المصدر (study on AI tools and experienced open-source developer productivity)، يوليو 2025)
- توثيق GitHub ‏(GitHub Docs)، GitHub Copilot — https://docs.github.com/en/copilot
- توثيق Anthropic ‏(Anthropic documentation) (Claude Code) — https://docs.anthropic.com/
- قائمة OWASP لأهم عشرة مخاطر في تطبيقات النماذج اللغوية الكبيرة (OWASP Top 10 for Large Language Model Applications) — https://owasp.org/www-project-top-10-for-large-language-model-applications/
- [*أمن الذكاء الاصطناعي والتطبيقات (Secure AI & Application Security)*، الدرس 6.3 — تأمين الشيفرة المولَّدة بالذكاء الاصطناعي: ما الذي يخطئ فيه وكلاء البرمجة (Securing AI-generated code: what coding agents get wrong)](../secai/index.ar.html#/6.3)
- [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 9.4 — التحقق قبل الإكمال (Verification before completion)](../vibe/index.ar.html#l9-4)
- [*تشغيل وكلاء الذكاء الاصطناعي في الإنتاج (Running AI Agents in Production)*، المسار التعليمي (learning path)، المستوى 1 — البنّاء (Level 1 — Builder)](../agentic/learning-path.ar.html#level-1-builder)

---

# 1.3 — التفكير الإنتاجي (Production thinking): الفجوة بين "يعمل على حاسوبي" (it runs on my laptop) و"يعمل للمستخدمين" (it runs for users)
*المستوى (Level): 🟢 مبتدئ (Beginner)* · *المتطلبات (Prerequisites): 1.1، 1.2* · *الخطوة (Step): Learn, Build*

## ⚡ الدرس في دقيقة (In 60 seconds)
- **بيئة الإنتاج (Production)** هي حيث يوجد المستخدمون الحقيقيون والبيانات الحقيقية (real users and data). أن يعمل التطبيق على حاسوبك اختبارٌ واحد (one test)؛ أما الإنتاج فيطلب أكثر: مستخدمَين في الوقت نفسه (two users at once)، وقاعدة بيانات بطيئة (slow database)، ومُدخلات عدائية (hostile input)، وإعادة تشغيل (restart)، وإصدارًا سيئًا (bad release).
- لا يتوقّع أصحاب العمل من المبتدئين تصميم أنظمة كبيرة (design large systems). لكنهم يتوقّعون منك أن **تطرح أسئلة الإنتاج (ask the production questions)**، وأن تكون قد أطلقت شيئًا حيًّا (put something live) وأبقيته يعمل مرة واحدة على الأقل.
- القاعدة الأهم: **إن لم تستطع رؤيته (see it)، والتراجع عنه (roll it back)، واستعادة بياناته (restore its data)، فلست مستعدًا لإطلاقه (ship it).**
- إشارة القرار (Decision cue): لكل مشروع، اسأل: "أين الإعدادات والأسرار (config and secrets)؟ كيف أعرف أنه معطّل (broken)؟ كيف أتراجع عن نشر سيئ (undo a bad deploy)؟ ماذا يحدث للبيانات؟" ⁦(Where are config and secrets? How do I know it is broken? How do I undo a bad deploy? What happens to the data?)⁩
- مشروع صغير واحد منشور فعلًا ومُشغَّل (actually deployed and operated) يتفوّق على خمسة مشاريع لا تعمل إلا محليًا (only run locally).
- أكبر فخ (Biggest trap): الإفراط في الهندسة (over-engineering) لتبدو مهندسًا أقدم (look senior). استخدام Kubernetes لثلاثة مستخدمين يُظهر حُسن تقدير (judgement) أقل من نشر بسيط (simple deploy) تستطيع شرحه.

## 🧭 لماذا يهم (Why it matters)
يختتم برنامج الخرّيجين (graduate programme) في نجم شهره الأول بهاكاثون داخلي (internal hackathon) مدته يومان. على كل فريق أن يُطلق تطبيقًا صغيرًا حيًّا (put a small app live) على منصّة البيئة التجريبية (sandbox platform) في البنك، وفي اليوم الثاني يُجري فريق المنصّة (platform team) بقيادة سالم "يوم اختبار الأعطال" (game day): يعيدون تشغيل الخوادم (restart servers)، ويُبطئون قاعدة البيانات (slow the database down)، ويرسلون طلبات مشوّهة (malformed requests).

يبني فريق عمر نظامًا لحجز مواعيد الفروع (branch-appointment booker) يعمل بلا عيب على حاسوبه. لكنه على البيئة التجريبية (sandbox) يفشل خلال عشر دقائق. عنوان قاعدة البيانات (database address) مكتوب مباشرة في الشيفرة (hard-coded) على أنه `localhost`، وكلمة مرورها مودَعة في المستودع (committed in the repository). وحين يعيد سالم تشغيل الخادم، تختفي كل الحجوزات: لقد كانت مخزّنة في الذاكرة (stored in memory). يحجز مختبِران (testers) آخر موعد متاح (last slot) في اللحظة نفسها، وينجح كلاهما. وطلب ينقصه حقل (missing field) يُسقط التطبيق (crashes the app) دون أي سجلّ (no log)، فيقضي الفريق ساعة في التخمين (guessing). لم يسبق لعمر أن نشر (deployed) أي شيء.

أما فريق يوسف، رغم أن شيفرته أقل صقلًا (less polished)، فيبلي بلاءً أفضل بكثير. يوسف، القادم من هندسة الحاسوب (computer engineering)، طرح الأسئلة المملّة (dull questions) في اليوم الأول: من أين تأتي الإعدادات (config)، وأين السجلات (logs)، وماذا يحدث عند إعادة التشغيل (on restart)؟ تعليق خالد في جلسة المراجعة الختامية (debrief): "كتابة شيفرة تعمل هي تذكرة الدخول (entry ticket). أما معرفة ما الذي يمكن أن يسوء بعد إطلاقه (once it's live)، فهي ما يجعلني أثق بمبتدئ في شيء حقيقي." يعطيك هذا الدرس تلك الأسئلة.

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**ما الذي يتغيّر في الإنتاج (What changes in production).** على حاسوبك يوجد مستخدم واحد (أنت)، ومُدخلات ودودة (friendly input)، وقاعدة بيانات محلية سريعة (fast local database)، ولا أحد يلاحظ إن تعطّل شيء. يعرض [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 0.1 — "إنه يعمل" ليست خاصية من خصائص النظام ("It works" is not a property of a system)](../vibe/index.ar.html#l0-1) في المكتبة الحجّة كاملة. بالنسبة إلى المبتدئ، تختصر الفجوة في عشرة أسئلة (ten questions):

| السؤال (Question) | إجابة الإنتاج (على مستوى المبتدئ) (Production answer (junior level)) | درس المكتبة الذي يبنيها (Library lesson that builds it) |
|---|---|---|
| كيف تُضبط إعداداته؟ ⁦(How is it configured?)⁩ | من متغيّرات البيئة (environment variables) أو ملفات إعدادات لكل بيئة (config files per environment) | [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 5.7 — الأسرار والإعدادات: مفاتيح المملكة (Secrets and configuration: the keys to the kingdom)](../vibe/index.ar.html#l5-7) |
| أين الأسرار؟ ⁦(Where are the secrets?)⁩ | ليست في المستودع أبدًا؛ بل في مخزن الأسرار في المنصّة (platform's secret store)؛ وملف `.env.example` يسرد الأسماء فقط (names only) | [*أمن الذكاء الاصطناعي والتطبيقات (Secure AI & Application Security)*، الدرس 5.2 — إدارة الأسرار: المفاتيح والرموز وأين تتسرّب (Secrets management: keys, tokens and where they leak)](../secai/index.ar.html#/5.2) |
| أين تعيش البيانات؟ ⁦(Where does data live?)⁩ | في قاعدة بيانات حقيقية أو تخزين (storage) يصمد بعد إعادة التشغيل (survives restarts)، مع نسخ احتياطية اختبرتها (backups you have tested) | [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 2.3 — النسخ الاحتياطية: ماذا، لا هل فقط (Backups: what, not just whether)](../vibe/index.ar.html#l2-3) |
| ماذا لو تصرّف مستخدمان في الوقت نفسه؟ ⁦(What if two users act at once?)⁩ | قيود قاعدة البيانات والمعاملات (database constraints and transactions) تمنع الحجز المزدوج (double bookings) والتحديثات المفقودة (lost updates) | [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 2.6 — نقرتان في الوقت نفسه: حالات التسابق والمعاملات والكتابات المتساوية الأثر (Two clicks at once: races, transactions, and idempotent writes)](../vibe/index.ar.html#l2-6) |
| ماذا لو كان المُدخل سيئًا أو عدائيًا؟ ⁦(What if input is bad or hostile?)⁩ | تحقّق من كل مُدخل (validate every input)؛ وأعِد أخطاء واضحة (clear errors)؛ ولا تبنِ الاستعلامات من نصوص خام (raw strings) أبدًا | [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 5.4 — مُدخلات لم تدرك أنك تثق بها (Input you didn't realize you were trusting)](../vibe/index.ar.html#l5-4) |
| كيف أعرف أنه معطّل؟ ⁦(How do I know it is broken?)⁩ | السجلات المهيكلة (structured logs)، ومتتبّع الأخطاء (error tracker)، وفحص التوافر (uptime check) تُخبرك قبل أن يُخبرك المستخدمون | [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 1.3 — عيون اليوم الأول: أول متتبّع أخطاء وأول فحص توافر لديك (Day-one eyes: your first error tracker and uptime check)](../vibe/index.ar.html#l1-3) |
| كيف يُنشر؟ ⁦(How does it get deployed?)⁩ | نشر قابل للتكرار ومؤتمت (repeatable, automated deploy) من المستودع، ويُفضَّل أن يكون عبر CI | [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 4.1 — الإطلاق نظامٌ بحدّ ذاته (Shipping is a system)](../vibe/index.ar.html#l4-1) |
| كيف أتراجع عن تغيير سيئ؟ ⁦(How do I undo a bad change?)⁩ | تراجع (rollback) إلى الإصدار السابق (previous version)، تدرّبتَ عليه مرة واحدة | [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 4.4 — التراجع وبيئة التجهيز وبوابات الإصدار (Rollback, staging, and release gates)](../vibe/index.ar.html#l4-4) |
| ما الاعتماديات التي يستخدمها؟ ⁦(Which dependencies does it use?)⁩ | مثبّتة الإصدارات في ملف قفل (pinned in a lock file) ومفحوصة بحثًا عن الثغرات المعروفة (known vulnerabilities) | [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 8.4 — البرمجيات التي لم تكتبها: الاعتماديات وسلسلة التوريد (The software you didn't write: dependencies and supply chain)](../vibe/index.ar.html#l8-4) |
| كم يكلّف؟ ⁦(What does it cost?)⁩ | تعرف ما الذي تدفع مقابله، ولديك تنبيه للميزانية (budget alert)، وتُطفئ ما لا تستخدمه | [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 11.4 — هندسة التكلفة (Cost engineering)](../vibe/index.ar.html#l11-4) |

لا تحتاج إلى إجابات عميقة عن الأسئلة العشرة كلها: اعرف الأسئلة (know the questions)، وضع إجابة بسيطة لها في مشاريعك (a simple answer in your projects)، واعرف أين تتعلّم المزيد.

**الطريق من الحاسوب إلى المستخدمين (The path from laptop to users).** إعداد صغير لكنه حقيقي (small but real setup) يبدو هكذا:

```mermaid
flowchart RL
    L["الحاسوب: الشيفرة والاختبارات<br/>(Laptop: code and tests)"] --> G["مستودع Git<br/>(Git repository)"]
    G --> C["التكامل المستمر: اختبارات وفحوص مع كل دفع<br/>(CI: tests and checks on every push)"]
    C --> S["بيئة التجهيز: نسخة من بيئة الإنتاج<br/>(Staging: a copy of production)"]
    S --> P["بيئة الإنتاج: مستخدمون وبيانات حقيقية<br/>(Production: real users and data)"]
    P --> M["السجلات والأخطاء وتنبيهات التوافر<br/>(Logs, errors and uptime alerts)"]
    M -->|"اكتُشف خطأ (bug found)"| L
    P -->|"إصدار سيئ (bad release)"| B["التراجع إلى الإصدار السابق<br/>(Roll back to the previous version)"]
```

كل سهم دليل لمعرض الأعمال (portfolio evidence): شارة CI ‏(CI badge)، ورابط حيّ (live URL)، وتنبيه (alert)، وملاحظة عن تراجع (rollback note).

**ثلاث عادات صغيرة في الشيفرة تقطع شوطًا طويلًا (Three tiny code habits that carry a long way).**

```python
# Before: works on Omar's laptop only
DB_URL = "postgresql://omar:secret123@localhost/booker"

# After: configured per environment, secret kept out of the code
import os
DB_URL = os.environ["DATABASE_URL"]  # fails loudly at startup if missing
```

```python
# Before: a missing field crashes the app with no trace
slot = request.json["slot_id"]

# After: validate, return a clear error, and log enough to debug
body = request.get_json(silent=True) or {}  # None if the body is not JSON
slot = body.get("slot_id")
if slot is None:
    log.warning("booking rejected: missing slot_id", extra={"request_id": req_id})
    return {"error": "slot_id is required"}, 422
```

```python
# A health-check endpoint the platform and uptime checks can call
@app.get("/health")
def health():
    try:
        db.execute("SELECT 1")  # proves the database is reachable
    except Exception:
        log.exception("health check: database unreachable")
        return {"status": "unavailable"}, 503
    return {"status": "ok"}
```

لا شيء منها متقدّم (advanced)؛ لكنها مجتمعةً تجيب عن ثلاثة من الأسئلة العشرة.

### 🟡 التعمق أكثر (Going deeper)

**كيف تختبر المقابلاتُ التفكيرَ الإنتاجي (How interviews probe production thinking).** نادرًا ما تطلب مقابلات المبتدئين تصميم نظام عالمي (global system design)، لكنها كثيرًا ما تطرح أسئلة كهذه أثناء شرح المشروع (project walk-through):

| يسأل مُجري المقابلة (Interviewer asks) | إجابة ضعيفة (Weak answer) | إجابة قوية لمبتدئ (Strong junior answer) |
|---|---|---|
| "كيف ستنشره؟" ⁦("How would you deploy this?")⁩ | "سأضعه على خادم." ⁦("I'd put it on a server.")⁩ | "إنه حاوية (container) ينشرها CI من الفرع الرئيسي (main branch) إلى منصّة مُدارة (managed platform)؛ يُنشر على بيئة التجهيز (staging) أولًا، وأستطيع التراجع (roll back) إلى الصورة السابقة (previous image)." |
| "ماذا يحدث إذا تعطّلت قاعدة البيانات؟" ⁦("What happens if the database is down?")⁩ | "لن تتعطّل." ⁦("It wouldn't be.")⁩ | "يفشل فحص الصحة (health check)، فتتوقّف المنصّة عن إرسال الحركة (traffic)، ويرى المستخدمون صفحة خطأ (error page)، ويرسل لي تنبيه التوافر (uptime alert) بريدًا. لم أُضِف إعادة المحاولة (retries) بعد؛ سأضيفها بحدّ أقصى (with a limit)." |
| "كيف ستعرف أنه معطّل؟" ⁦("How would you know it was broken?")⁩ | "سيخبرني المستخدمون." ⁦("Users would tell me.")⁩ | "تذهب الأخطاء إلى متتبّع الأخطاء (error tracker)، ويستدعي فحص التوافر (uptime check) المسار `/health` كل بضع دقائق." |
| "أين مفتاح الواجهة البرمجية؟" ⁦("Where's the API key?")⁩ | "في ملف الإعدادات." ⁦("In the config file.")⁩ | "في مخزن الأسرار في المنصّة (platform's secret store). المستودع لا يحتوي إلا على `.env.example` بأسماء المتغيّرات (variable names)." |
| "ما الذي كنت ستفعله بشكل مختلف لو كان المستخدمون أكثر بألف مرة؟" ⁦("What would you do differently with a thousand times more users?")⁩ | "أستخدم Kubernetes." ⁦("Use Kubernetes.")⁩ | "أولًا سأقيس أين يذهب الوقت (measure where the time goes)، وغالبًا في استعلامات قاعدة البيانات (database queries)؛ وسأضيف فهارس (indexes) وربما تخزينًا مؤقتًا (caching) قبل إضافة خوادم أكثر." |

الإجابات القوية محدّدة (specific)، وصادقة بشأن ما لم يُنجز بعد (honest about what is not done yet)، ومتناسبة (proportionate). يتناول الدرس 5.3 مقابلات تصميم الأنظمة (system design interviews) للمبتدئين.

**التفكير الإنتاجي بحسب الدور (Production thinking by role).** تتّخذ الأسئلة العشرة أشكالًا مختلفة:
- **مهندسو البرمجيات وتطبيقات الذكاء الاصطناعي (Software and AI application engineers):** القائمة أعلاه، مضافًا إليها لميزات الذكاء الاصطناعي (AI features): تكلفة كل طلب (cost per request)، وتقييمات جودة الإجابات (answer-quality evaluations)، وما يحدث حين يتعطّل مزوّد النموذج (model provider is down). انظر [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 6.7 — أنت أيضًا عميلٌ لأحدهم: كيف تنجو من الواجهات البرمجية للأطراف الثالثة (You are someone's client too: surviving third-party APIs)](../vibe/index.ar.html#l6-7).
- **أدوار البيانات (Data roles):** تتعلّم هدى أن دفتر الملاحظات (notebook) الذي عمل مرة واحدة ليس خط بيانات (pipeline). الإنتاج يعني إعادة تشغيل آمنة (safe reruns) دون تكرار البيانات (duplicating data)، وفحوص جودة (quality checks)، وتنبيهات حين يتغيّر المصدر (source changes)، وأرقامًا يمكن تتبّعها إلى مصدرها (traceable to their source). يبني المساق الشقيق (sister course) ذلك، من [*هندسة البيانات والتحليلات (Data Engineering & Analytics)*، الوحدة 2 — الاستيعاب وخطوط البيانات (Ingestion and pipelines)](../data/index.ar.html#/2.1) إلى [*هندسة البيانات والتحليلات (Data Engineering & Analytics)*، الوحدة 5 — علم البيانات وتعلّم الآلة في الإنتاج (Data science and ML in production)](../data/index.ar.html#/5.1).
- **أدوار السحابة والمنصّات (Cloud and platform roles):** بالنسبة إلى يوسف، الإنتاج هو المنتج نفسه (production is the product): البنية التحتية بوصفها شيفرة (infrastructure as code)، والوصول بأقل الصلاحيات (least-privilege access)، والقياس عن بُعد في كل مكان (telemetry everywhere). يغطّيه المساق الشقيق، من [*الحوسبة السحابية وDevOps ‏(Cloud & DevOps)*، الوحدة 1 — الأسس (Foundations)](../cloud/index.ar.html#/1.1) إلى [*الحوسبة السحابية وDevOps ‏(Cloud & DevOps)*، الوحدة 5 — قابلية المراقبة والموثوقية (Observability and reliability)](../cloud/index.ar.html#/5.1).

**مشروع معرض أعمال بعقلية إنتاجية (A production-minded portfolio project)** صغير ومُشغَّل بشكل ظاهر (visibly operated): رابط حيّ (live URL)، وCI مع كل دفع (on every push)، ولا أسرار في السجل (no secrets in history)، ونقطة نهاية `/health` مع فحص توافر (uptime check)، ومتتبّع أخطاء (error tracker)، وقسم "العمليات" (Operations) في ملف README (النشر (deploy)، والتراجع (roll back)، والاستعادة (restore))، و**تقرير ما بعد الحادثة (postmortem)** قصير واحد: تقرير مكتوب لا يلوم أحدًا (blameless write-up) عمّا ساء، وكيف اكتشفته، وما الذي غيّرته. تبني الوحدة 3 هذا في مشروعك الختامي (capstone). عمليات النشر الصغيرة (small deploys) رخيصة أو مجانية على منصّات كثيرة وقت كتابة هذا الدرس (2026)؛ تحقّق من الشروط الحالية (current terms) واضبط تنبيهًا للميزانية (budget alert).

### 🔴 نظرة الخبير (Expert view)

**الإنتاج لدى صاحب عمل خاضع للتنظيم (Production in a regulated employer).** في بنك مثل نجم، تمرّ التغييرات عبر **إدارة التغيير (change management)** — وهي عملية معتمدة ومسجّلة (approved, recorded process) لتحديد ما يُطلق ومتى — ويكون الوصول إلى بيئة الإنتاج (production access) مقيّدًا ومسجّلًا (restricted and logged)، وتخضع بيانات العملاء (customer data) لقوانين مثل قانون حماية خصوصية البيانات الشخصية في قطر (Qatar's Personal Data Privacy Protection Law) ‏(PDPPL، القانون رقم 13 لسنة 2016 (Law No. 13 of 2016)). بوصفك مبتدئًا، لن تنشر على الأرجح إلى بيئة الإنتاج وحدك لعدة أشهر. والخرّيجون الذين يفهمون *لماذا* توجد الضوابط (why the controls exist) يستقرّون أسرع، ويقدّر ذلك أصحاب العمل الخاضعون للتنظيم في دول الخليج (regulated GCC employers) — البنوك، والجهات الحكومية، والطاقة، والصحة: فأن تقول لماذا لن تختبر أبدًا ببيانات عملاء حقيقية (real customer data) يساوي أكثر من أي مصطلح رنّان (buzzword).

**أنت تبنيه، وأنت تشغّله (You build it, you run it).** تتوقّع فرق كثيرة من البنّائين (builders) أن يساعدوا في تشغيل خدمتهم (operate their service)، بما في ذلك **المناوبة (on call)** — أي الاستجابة للتنبيهات خارج ساعات العمل وفق جدول دوري (rota) — وعادةً بعد بضعة أشهر من المرافقة والمراقبة (shadowing). تشغيل مشروعك الصغير بنفسك هو أفضل تحضير؛ و[*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الوحدة 12 — المشروع الختامي: يصلك نداء الطوارئ (Capstone: You Get Paged)](../vibe/index.ar.html#l12) يحاكي ذلك.

**التناسب هو مهارة المهندس الأقدم (Proportion is the senior skill).** التفكير الإنتاجي يعني مواءمة الضمانات مع المخاطر (matching safeguards to risk). المشروع الشخصي يحتاج إلى نشر قابل للتكرار (repeatable deploy)، وسجلات (logs)، وفحص صحة (health check)، ونسخة احتياطية (backup)؛ أما خدمة الدفع (payment service) فتحتاج إلى أكثر من ذلك بكثير. والخدمات المصغّرة (microservices) أو Kubernetes أو طوابير الرسائل (message queues) حيث لا حاجة إليها توحي بالتكرار لا بالتفكير (repeating rather than reasoning). يبيّن [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 0.3 — البناء أم الشراء: القرار الأعلى أثرًا الذي ستتخذه (Build vs buy: the highest-leverage decision you'll make)](../vibe/index.ar.html#l0-3) كيف تختار.

**وكلاء الذكاء الاصطناعي والإنتاج (AI agents and production).** كثيرًا ما يُغفل الوكلاء التفاصيل التشغيلية (operational details) مثل القيم المكتوبة مباشرة في الشيفرة (hard-coded values) والأسرار في تجهيزات الاختبار (secrets in fixtures) (الدرس 1.2)؛ فاذكر متطلبات الإنتاج (production requirements) في المهمة وتحقّق منها في المراجعة (check them in review).

## 🧰 الأدوات (The toolkit)
| المورد أو الأداة أو النموذج (Resource, tool or template) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **The Twelve-Factor App** — منهجية التطبيق ذي العوامل الاثني عشر، من وضع آدم ويغينز ومساهمين آخرين (Adam Wiggins and contributors) | مبادئ واسعة الاستشهاد (widely cited principles) للخدمات الويب القابلة للنشر (deployable web services): الإعدادات في البيئة (config in the environment)، والسجلات بوصفها تدفّقات (logs as streams)، والعمليات القابلة للاستبدال (disposable processes) | قبل أول نشر لك (first deploy) |
| **Ship-ready checklist** — قائمة الجاهزية للإطلاق | أسئلة الإنتاج العشرة (ten production questions) مع دليل لكل منها (نسخة نجم أدناه) | قبل أن تصف أي مشروع في معرض أعمالك بأنه "مكتمل" (done) |
| **.env.example** | ملف مودَع (committed file) يسرد أسماء متغيّرات الإعدادات (configuration variable names) بقيم زائفة (fake values)، ولا يحتوي أبدًا على أسرار حقيقية | كل مشروع يحتاج إلى إعدادات |
| **Health-check endpoint** — نقطة نهاية فحص الصحة | رابط بسيط (simple URL) يُبلغ عمّا إذا كان التطبيق واعتمادياته الرئيسية (key dependencies) تعمل | كل خدمة ويب؛ تستخدمه المنصّات (platforms)، وموازنات الحمل (load balancers)، وفحوص التوافر (uptime checks) |
| **Error tracker** — متتبّع الأخطاء (على سبيل المثال Sentry) | يجمع أخطاء التطبيق (application errors) مع تتبّعات المكدّس (stack traces) والسياق (context)، وينبّهك (alerts you) | من أول نشر لك؛ توجد فئات مجانية (free tiers) وقت كتابة هذا الدرس (2026) |
| **Uptime check** — فحص التوافر | خدمة خارجية (external service) تستدعي رابطك وفق جدول (on a schedule) وتنبّهك حين يفشل | كل مشروع منشور، لكي تعلم بالأعطال (outages) قبل المستخدمين |
| **Postmortem** — تقرير ما بعد الحادثة | تقرير مكتوب لا يلوم أحدًا (blameless write-up) عن حادثة (incident): ما الذي حدث، والأثر (impact)، والسبب (cause)، وما الذي غيّرته | بعد أي إخفاق حقيقي في مشروعك؛ وهو عنصر قوي في معرض الأعمال (strong portfolio item) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
بعد الهاكاثون، يحوّل سالم وخالد إخفاقات يوم اختبار الأعطال (game-day failures) إلى **قائمة الجاهزية للإطلاق لخرّيجي نجم (Najm graduate ship-ready checklist)**، التي تُستخدم في كل مشروع خرّيج. إليك نظام الحجز الخاص بعمر (Omar's booker)، بعد أسبوعين.

| السؤال (Question) | الدليل المطلوب (Evidence required) | دليل عمر (Omar's evidence) | الحالة (Status) |
|---|---|---|---|
| الإعدادات لكل بيئة (Configured per environment) | الإعدادات من البيئة (config from environment)؛ والبيئات لا تختلف إلا في الإعدادات | `DATABASE_URL` و`LOG_LEVEL` من البيئة | مكتمل (Done) |
| لا أسرار في المستودع (No secrets in the repository) | فحص الأسرار (secret scan) نظيف على السجل الكامل (full history)؛ وملف `.env.example` موجود | كلمة المرور غُيّرت (rotated) وأُزيلت من السجل (purged from history)؛ والفحص نظيف | مكتمل (Done) |
| البيانات تصمد بعد إعادة التشغيل ولها نسخ احتياطية (Data survives restarts and is backed up) | قاعدة بيانات حقيقية؛ واستعادة (restore) مُختبرة مرة واحدة | Postgres مُدار (Managed Postgres)؛ نسخة احتياطية يومية (daily backup)؛ استعادة مُختبرة في بيئة التجهيز (staging) في 12 نوفمبر | مكتمل (Done) |
| آمن عند الاستخدام المتزامن (Safe under concurrent use) | قيد (constraint) أو معاملة (transaction) تمنع حالة التسابق المعروفة (known race) | قيد تفرّد (unique constraint) على الموعد والتاريخ (slot and date)؛ واختبار بحجزين متوازيين (two parallel bookings) | مكتمل (Done) |
| المُدخلات مُتحقَّق منها (Inputs validated) | أخطاء 4xx واضحة للمُدخلات السيئة (bad input)؛ واختبارات للحالات الحدّية (edge cases) | تحقّق على نقاط النهاية الثلاث (all three endpoints)؛ و9 اختبارات للمُدخلات السيئة | مكتمل (Done) |
| مرئي حين يتعطّل (Visible when broken) | سجلات مهيكلة (structured logs)، ومتتبّع أخطاء، وفحص توافر على `/health` | الثلاثة كلها قائمة؛ والسجلات تحمل معرّفات الطلبات (request IDs) | مكتمل (Done) |
| نشر قابل للتكرار (Repeatable deploy) | نشر من الفرع الرئيسي (main branch) بواسطة CI؛ وبيئة التجهيز أولًا | CI يشغّل الاختبارات، وينشر إلى بيئة التجهيز، مع موافقة يدوية (manual approval) للانتقال إلى الإنتاج | مكتمل (Done) |
| التراجع مُتدرَّب عليه (Rollback practised) | تراجعتَ مرة واحدة، عمدًا (on purpose)، وسجّلتَ ذلك | تراجع عن إصدار سيئ متعمَّد (deliberate bad release) في 4 دقائق؛ ودوّن ذلك في README | مكتمل (Done) |
| الاعتماديات مثبّتة ومفحوصة (Dependencies pinned and scanned) | ملف قفل (lock file)؛ وفحص للاعتماديات (dependency scan) في CI | كلاهما موجود؛ ولا نتائج عالية الخطورة (high-severity findings) | مكتمل (Done) |
| التكلفة معروفة (Cost known) | تقدير شهري للتكلفة (monthly cost estimate) وتنبيه للميزانية (budget alert) | لم يُعَدّ بعد (Not set up yet) | التالي: بحلول 20 نوفمبر (Next: by 20 Nov) |

يقدّم قسم "العمليات" (Operations) في ملف README الأوامر الدقيقة (exact commands) لـ*النشر (Deploy)* و*التراجع (Roll back)* و*استعادة البيانات (Restore data)*، ويربط بأول تقرير ما بعد حادثة (postmortem) كتبه عمر: "ضياع الحجوزات عند إعادة التشغيل" (Bookings lost on restart).

## 🛠️ التمارين (Exercises)
- 🟢 خذ أحد مشاريعك وأجِب عن أسئلة الإنتاج العشرة (ten production questions) الخاصة به في جدول، بصدق (honestly)، مع "ليس بعد" (not yet) حيث تكون تلك هي الحقيقة. *يكتمل عندما (Done when):* يكون الجدول مودَعًا في المستودع (على سبيل المثال باسم `OPERATIONS.md`)، ولكل "ليس بعد" خطة من سطر واحد (one-line plan).
- 🟡 انشر مشروعًا صغيرًا واحدًا مع إعدادات من البيئة (config from the environment)، ودون أسرار في السجل (no secrets in history)، ونقطة نهاية `/health`، وفحص توافر (uptime check)، ومتتبّع أخطاء (error tracker). *يكتمل عندما (Done when):* يستطيع صديق فتح الرابط الحيّ (live URL)، وتستطيع أن تُظهر سجلّ فحص التوافر وخطأً تجريبيًا (test error) التقطه متتبّع الأخطاء، ويكون فحص الأسرار (secret scan) للسجل الكامل نظيفًا.
- 🔴 أجرِ يوم اختبار أعطال خاصًا بك (run your own game day): أعِد تشغيل التطبيق، واجعل قاعدة البيانات غير قابلة للوصول (unreachable)، وأرسل طلبات مشوّهة ومتزامنة (malformed and concurrent requests)، وأطلق إصدارًا معطوبًا (broken release) ثم تراجع عنه. اكتب تقرير ما بعد الحادثة (postmortem) من صفحة واحدة عن أسوأ إخفاق وأصلحه. *يكتمل عندما (Done when):* يكون تقرير ما بعد الحادثة مربوطًا من ملف README، والإصلاح في طلب دمج (pull request) مع اختبار، ويسرد قسم "العمليات" (Operations) في README خطوات النشر (deploy) والتراجع (rollback) والاستعادة (restore) الدقيقة التي نفّذتها فعلًا.

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **وصف المشروع بأنه "مكتمل" لأنه يعمل محليًا (Calling a project "done" because it runs locally).** لقد اجتاز اختبارًا واحدًا من بين اختبارات كثيرة. انشره (deploy it) وأجِب عن الأسئلة العشرة.
- **الأسرار في المستودع (Secrets in the repository).** حذف الملف لا يكفي؛ فالسرّ يبقى في السجل (stays in history). غيّر السرّ (rotate the secret)، ونظّف السجل (clean the history)، وأضِف فحص الأسرار (secret scanning).
- **لا وسيلة لرؤية الإخفاقات (No way to see failures).** دون سجلات (logs)، ومتتبّع أخطاء (error tracker)، وفحص توافر (uptime check)، فأنت تصحّح الأخطاء بالتخمين (debug by guessing).
- **عدم التدرّب أبدًا على التراجع أو الاستعادة (Never practising rollback or restore).** النسخة الاحتياطية أو التراجع غير المُختبَر (untested backup or rollback) أمنيةٌ لا خطة (a hope, not a plan). نفّذ كلًّا منهما مرة واحدة، عمدًا.
- **الإفراط في الهندسة لتبدو مهندسًا أقدم (Over-engineering to look senior).** البنية التحتية الثقيلة (heavy infrastructure) لمشروع صغير جدًا تشير إلى النسخ (copying) لا إلى حُسن التقدير (judgement). وائِم الضمانات مع المخاطر (match safeguards to risk) واشرح السبب.
- **الاختبار ببيانات شخصية حقيقية (Testing with real personal data).** مشكلة قانونية ومشكلة ثقة (legal and trust problem)، خاصة في القطاعات الخاضعة للتنظيم (regulated sectors). استخدم بيانات اصطناعية (synthetic) أو مُجهَّلة الهوية (anonymised).

## 🧾 الخلاصة (Recap)
- بيئة الإنتاج (Production) هي حيث يوجد المستخدمون الحقيقيون والبيانات الحقيقية؛ ونجاح التطبيق على الحاسوب (laptop success) ليس إلا الاختبار الأول.
- يتوقّع أصحاب العمل من المبتدئين أن يطرحوا أسئلة الإنتاج (production questions): الإعدادات (config)، والأسرار (secrets)، والبيانات (data)، والتزامن (concurrency)، والمُدخلات (input)، والرؤية (visibility)، والنشر (deploy)، والتراجع (rollback)، والاعتماديات (dependencies)، والتكلفة (cost).
- العادات الصغيرة (small habits) — الإعدادات من البيئة (config from the environment)، والتحقق من المُدخلات (input validation)، وفحص الصحة (health check) — تجيب عن عدة أسئلة دفعة واحدة.
- لدى أصحاب العمل الخاضعين للتنظيم (regulated employers)، يُعدّ فهم سبب وجود إدارة التغيير (change management) وحماية البيانات (data protection) ميزة حقيقية.
- التناسب هو مهارة المهندس الأقدم (Proportion is the senior skill): وائِم الضمانات مع المخاطر (match the safeguards to the risk).

## ✍️ اختبر نفسك (Check yourself)

**1. خلال يوم اختبار الأعطال (game day)، يعيد سالم تشغيل الخادم (restarts the server) فتختفي كل حجوزات عمر. أيّ سؤال من أسئلة الإنتاج (production question) فات فريقَ عمر؟**

- A. كيف يُنشر، وهل النشر قابل للتكرار (repeatable)؟
- B. كم يكلّف، وهل يوجد تنبيه للميزانية (budget alert)؟
- C. ما الاعتماديات (dependencies) التي يستخدمها، وهل هي مثبّتة الإصدارات (pinned)؟
- D. أين تعيش البيانات (Where does the data live)؟

<details><summary>الإجابة</summary>

**D.** كانت الحجوزات تعيش في الذاكرة (lived in memory)، فمحتها إعادة التشغيل؛ ويجب أن تعيش البيانات في قاعدة بيانات أو تخزين يصمد بعد إعادة التشغيل (survives restarts). الخيار A مهمّ أيضًا، لكن لا توجد عملية نشر (deploy process) تنقذ بيانات لا تعيش إلا في الذاكرة. (🟢 الأساسيات (The essentials)، الأسئلة العشرة (the ten questions).)

</details>

**2. في مقابلة، يسأل طارق محمدًا: "ماذا يحدث لتطبيقك إذا تعطّلت قاعدة البيانات؟" ⁦(What happens to your app if the database goes down?)⁩ أيّ إجابة هي الأقوى لمبتدئ؟**

- A. "لن يحدث ذلك. أستخدم قاعدة بيانات مُدارة (managed database) من مزوّد كبير يُبقيها تعمل."
- B. "يفشل `/health`، ويحصل المستخدمون على صفحة خطأ (error page)، وينبّهني فحص التوافر (uptime check). لا إعادة محاولة (retries) بعد؛ سأضيف إعادة محاولة محدودة (limited one)."
- C. "سأنقل التطبيق كله إلى Kubernetes لكي يعالج نفسه ذاتيًا (self-heal) حين يفشل أي شيء."
- D. "سأسأل مهندسًا أقدم (senior engineer) في الفريق، لأنه سيعرف الإجابة."

<details><summary>الإجابة</summary>

**B.** إنها محدّدة (specific)، وصادقة بشأن ما لم يُنجز بعد (honest about what is not done yet)، ومتناسبة (proportionate). الخيار C يلجأ إلى بنية تحتية ثقيلة (heavy infrastructure) لا تعالج السؤال؛ والخيار A ينكر أن الإخفاق يمكن أن يحدث. (🟡 التعمق أكثر (Going deeper)، كيف تختبر المقابلاتُ التفكيرَ الإنتاجي (how interviews probe production thinking).)

</details>

**3. يكتشف عمر أن كلمة مرور قاعدة البيانات (database password) أُودعت في مستودعه قبل ثلاثة أسابيع. فيحذف الملف في إيداع جديد (new commit). ما الذي يجب أن يفعله أيضًا؟**

- A. أن يغيّر كلمة المرور (rotate the password)، ويزيلها من السجل (purge it from history)، ويضيف فحص الأسرار (secret scanning)
- B. لا شيء آخر، لأن الإيداع الأخير لم يعد يحتوي على الملف
- C. أن يجعل المستودع خاصًا (private)، وهذا يحلّ المشكلة تمامًا
- D. أن يضيف تعليقًا في الشيفرة (code comment) يطلب من الناس عدم استخدام كلمة المرور القديمة

<details><summary>الإجابة</summary>

**A.** يبقى السرّ في سجلّ Git ‏(Git history) وربما نُسخ بالفعل، لذا غيّره (rotate)، ونظّف السجل (clean history)، وامنع تكرار ذلك (prevent a repeat). الخيار C يقلّل الانكشاف (reduces exposure) لكنه لا يُلغي التسرّب (does not undo the leak). (⚠️ أخطاء وفخاخ (Mistakes and traps).)

</details>

**4. يعمل نموذج هدى (Huda's model) جيدًا في دفتر الملاحظات (notebook). أيّ تغيير سينقله أكثر نحو بيئة الإنتاج، من منظور أدوار البيانات (data role)؟**

- A. إضافة مزيد من الرسوم البيانية والشروح (charts and explanations) ليتمكّن الفريق من متابعة كل خطوة في دفتر الملاحظات
- B. إعادة تدريب النموذج (retrain the model) بمزيد من الخصائص (features) وضبطه حتى تصبح الدقة (accuracy) أعلى بوضوح
- C. تحويله إلى خط بيانات (pipeline) يُعاد تشغيله بأمان (reruns safely)، ويتحقق من جودة البيانات (data quality)، وينبّه عند تغيّر المصدر (source changes)
- D. مشاركة ملف دفتر الملاحظات مع الفريق عبر البريد الإلكتروني (by email) ليتمكّن أي أحد من تشغيله عند الحاجة

<details><summary>الإجابة</summary>

**C.** بالنسبة إلى أدوار البيانات، يعني الإنتاج إعادة تشغيل آمنة (safe reruns)، وفحوص جودة (quality checks)، وتنبيهات (alerting). قد يحسّن الخيار B الدقة، لكنه يُبقي العمل دفتر ملاحظات لمرة واحدة (one-off notebook). (🟡 التعمق أكثر (Going deeper)، التفكير الإنتاجي بحسب الدور (production thinking by role).)

</details>

**5. تريد ريم أن يبدو مشروع معرض أعمالها (portfolio project) مشروعَ مهندس أقدم (look senior)، وتخطّط لإضافة Kubernetes وثلاث خدمات مصغّرة (microservices) وطابور رسائل (message queue) إلى تطبيق لا يستخدمه إلا عدد قليل من المستخدمين. بماذا سينصحها خالد على الأرجح؟**

- A. أن تمضي قُدمًا، لأن مزيدًا من البنية التحتية (infrastructure) يُبهر دائمًا مُجري المقابلات في بنك مثل نجم
- B. أن تُزيل النشر (deployment) تمامًا وتعرض الشيفرة وحدها، لأن المبتدئين لا يُتوقّع منهم تشغيل أي شيء
- C. أن تضيف البنية التحتية، لكن أن تُغفلها في ملف README حتى لا تشتّت انتباه مُجري المقابلات
- D. أن تُبقيه بسيطًا (keep it simple): نشر (deploy)، وسجلات (logs)، وفحص صحة (health check)، ونسخ احتياطية (backups)، وتراجع (rollback) تستطيع شرحه

<details><summary>الإجابة</summary>

**D.** التناسب هو مهارة المهندس الأقدم (Proportion is the senior skill)؛ والأدوات الثقيلة لمشكلة صغيرة جدًا توحي بالنسخ (copying) لا بحُسن التقدير (judgement)، وتستطيع ريم أن تقول ما الذي ستضيفه عند نطاق أكبر (at larger scale). الخيار B يُضيّع دليل التفكير الإنتاجي (evidence of production thinking). (🔴 نظرة الخبير (Expert view)، التناسب (proportion).)

</details>

## 📚 المراجع (References)
- منهجية التطبيق ذي العوامل الاثني عشر (The Twelve-Factor App) — https://12factor.net/
- Google، كتب هندسة موثوقية المواقع (Site Reliability Engineering books) (مجانية على الإنترنت (free online)) — https://sre.google/books/
- قائمة OWASP لأهم عشرة مخاطر (OWASP Top 10) — https://owasp.org/www-project-top-ten/
- توثيق Sentry ‏(Sentry documentation) — https://docs.sentry.io/
- الميزان، البوابة القانونية القطرية (Al Meezan, Qatar Legal Portal) (القانون رقم 13 لسنة 2016 بشأن حماية خصوصية البيانات الشخصية (Law No. 13 of 2016, Personal Data Privacy Protection)) — https://www.almeezan.qa/
- [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 0.1 — "إنه يعمل" ليست خاصية من خصائص النظام ("It works" is not a property of a system)](../vibe/index.ar.html#l0-1)
- [*الحوسبة السحابية وDevOps من الصفر إلى الاحتراف (Cloud & DevOps: Zero to Hero)*، الوحدة 5 — قابلية المراقبة والموثوقية (Observability and reliability)](../cloud/index.ar.html#/5.1)
- [*هندسة البيانات والتحليلات من الصفر إلى الاحتراف (Data Engineering & Analytics: Zero to Hero)*، الوحدة 2 — الاستيعاب وخطوط البيانات (Ingestion and pipelines)](../data/index.ar.html#/2.1)
