# الوحدة 6 — الاستكشاف والمتطلبات (Discovery and requirements)

*يبدأ كل مشروع وكيل (agent project) بجملة مثل «ينبغي أن يكون لدينا مساعد لمكتب الخدمة» (we should have an assistant for the Service Desk)، ويختبئ معظم مخاطر المشروع (most of the project's risk) داخل هذه الجملة. تعلّمك هذه الوحدة كيف تكتشف ما يحتاجه العميل حقًا (what the customer really needs) وكيف تدوّنه بحيث يمكن بناؤه واختباره (built and tested). الدرس 6.1 ورشة استكشاف (discovery workshop) على نجم ديسك (Najm Desk): ترسم خريطة أصحاب المصلحة (map stakeholders)، وتقرأ مقابلتين خياليتين (fictional interviews) مع هند (Hind) ويارا (Yara) وتقرير مرافقة ميدانية (shadowing report) من أرضية مكتب الخدمة (Service Desk floor)، وتجرد الأنظمة والبيانات (inventory systems and data)، وتقدّر القيمة بوصفها نطاقًا (size the value as a range)، وتصنّف المخاطر في مستويات (tier the risk)، وتسأل هل الوكيل هو الأداة الصحيحة أصلًا (whether an agent is even the right tool)، وتكتب موجز وكيل من صفحة واحدة (a one-page agent brief). ويحوّل الدرس 6.2 الموجز إلى مواصفة قابلة للاختبار (a testable specification): متطلبات يمكن أن تفشل (requirements you can fail)، ومصفوفة صلاحيات (a permissions matrix)، ومعايير قبول (acceptance criteria) بصيغة «بافتراض/عندما/إذن» (Given/When/Then)، ومجموعة تقييم أولية (an eval seed set)، ومراجعة للمواصفة مع العميل (a spec review with the customer). ويعمل كل ذلك دون اتصال (offline)، ولا تستدعي أي شيفرة في هذه الوحدة نموذجًا (calls a model).*

> **الطبقة (Layer):** Delivery — العمل المواجه للعميل (the customer-facing work) الذي يقرر ما ينبغي أن يفعله الوكيل (what an agent should do) ولمن (for whom) وفق أي قواعد (under which rules)، وكيف سيعرف الجميع أنه يعمل (how everyone will know it works)، قبل بناء أي جزء منه (before any of it is built).

---

# 6.1 — الاستكشاف: من مشكلة العمل إلى موجز الوكيل: أصحاب المصلحة وسير العمل والبيانات والمخاطر و«هل ينبغي أن يكون هذا وكيلًا؟» ⁦(Discovery: from a business problem to an agent brief: stakeholders, workflows, data, risk and "should this be an agent?")⁩
*المستوى (Level): 🟢 مبتدئ (Beginner)* · *المتطلبات (Prerequisites): 0.1، 5.1* · *الطبقة (Layer): Delivery*

## ⚡ الدرس في دقيقة (In 60 seconds)
- **الاستكشاف (Discovery)** هو العمل الواقع بين «ينبغي أن يكون لدينا مساعد ذكاء اصطناعي» (we should have an AI assistant) و«هذا ما سنبنيه، ولمن، وما يجب ألا يفعله أبدًا» (here is what we build, for whom, and what it must never do). وينتهي بـ**موجز وكيل (agent brief)** من صفحة واحدة (one-page).
- تحدّث إلى الراعي (the sponsor) والذين يؤدون العمل (the people who do the work) وأصحاب المخاطر (the risk owners). اسأل عن **السلوك السابق (past behaviour)** لا عن الآراء المستقبلية (future opinions).
- مصدران متعارضان (two sources that disagree) نتيجة لا ضجيج (a finding, not noise). قدّر القيمة بوصفها **نطاقًا (range)** لا رقمًا واحدًا (never one number).
- قبل اختيار الوكيل (before choosing an agent)، اطرح أربعة أسئلة (four questions) وجرّب بدائل أرخص (cheaper alternatives).
- أكبر فخ (biggest trap): الوثوق بمصدر واحد (trusting one source)، ثم ترك مساعد ذكاء اصطناعي (an AI assistant) يسوّي التناقضات (smooth over contradictions) أو يختلق اقتباسات (invent quotes).

## 🧭 لماذا يهم (Why it matters)
تقرأ لجين (Lujain) بريد هند (Hind) الإلكتروني (email): *احتواء سبعين بالمئة من التذاكر (seventy percent deflection)، وعمل على مدار 24 ساعة (open 24 hours)، وفتح الحسابات تلقائيًا (unlock accounts by itself)*. وفي أربعة أيام تبني عرضًا تجريبيًا (demo) يفتح الحسابات عبر أداة اختبار (a test tool). ثم تسأل يارا (Yara): «أين معاودة الاتصال؟» ⁦(Where is the call-back?)⁩ تقضي السياسة (policy) بأن يتحقق موظف مكتب الخدمة (an agent) من طلب فقدان تطبيق المصادقة (a lost-authenticator request) بالاتصال بمدير الشخص (calling the person's manager). يتجاوز العرض هذه الخطوة (The demo skips it)، وسيمنعه فريق نورة (Noura's team would block it)، فيذهب العمل هباءً (the work is thrown away). (قصة افتراضية، كسائر قصص نجم (Hypothetical, like all Najm stories).)

لم يكن في الشيفرة (code) أي خطأ. الخطأ كان في الموجز (the brief): كان لدى لجين مصدر واحد (one source)، والراعية (the sponsor) ترى لوحة المؤشرات (the dashboard) لا أرضية العمل (the floor). جملة خاطئة في الموجز (a wrong sentence in a brief) تكلّف عصرًا واحدًا لإصلاحها (an afternoon to fix)؛ وفي الشيفرة أكثر بكثير (much more)؛ وفي التجربة التشغيلية (a pilot) تكلّف الثقة (trust).

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**ارسم خريطة أصحاب المصلحة (Map the stakeholders) أولًا**: ما الذي يهم كلًّا منهم (what each cares about)، ومن الغائب (who is missing).
- **الراعية (Sponsor)** (تملك النتيجة (owns the outcome)): هند (Hind).
- **المستخدمون (Users):** الموظفون (staff) والمتعاقدون (contractors) وموظفو المكتب (the agents) الذين يتلقون التسليمات (receive hand-offs).
- **المشغّلون (Operators)** (يتعايشون مع أخطائه (live with its mistakes)): فريق يارا (Yara's team)، ثم لاحقًا فريق هندسة الموثوقية (SRE team) بقيادة مها (Maha's).
- **أصحاب المخاطر (Risk owners)** (يستطيعون قول «لا» (can say no)): ليلى (Layla) وحمد (Hamad) ونورة (Noura) وسارة (Sara).
- **أصحاب الاعتماديات (Blockers)** (يملكون اعتمادًا (hold a dependency)): فريق المنصّة (platform team) بقيادة سالم (Salem)؛ ومالكو TicketHub وNajm ID وPeopleCore ومكتبة السياسات (the policy library).

**خطة من خمسة أيام (A five-day plan).** اقرأ وارسم الخريطة (Read and map)؛ وقابل هند ويارا (interview Hind and Yara)؛ ورافق المكتب ميدانيًا (shadow the desk)؛ والتقِ أصحاب المخاطر (meet the risk owners) واستعرض الأنظمة (walk the systems)؛ واكتب الموجز (write the brief) واقرأه على هند (read it back to Hind).

**المقابلات: اسأل عن حياتهم لا عن فكرتك (Interviews: ask about their life, not your idea).** كتاب روب فيتزباتريك (Rob Fitzpatrick) *The Mom Test* دليل قصير (a short guide)؛ وبإعادة الصياغة (paraphrased): الناس لطفاء حيال فكرتك (people are kind about your idea)، فاسأل عن أمور محددة حدثت فعلًا (specific things that happened) وأصغِ أكثر مما تتكلم (listen more than you talk). اسأل عن **السلوك السابق (past behaviour)** مثل «حدّثني عن آخر مرة…» (Tell me about the last time…)؛ فالآراء المستقبلية (future opinions) تخمينات مهذبة (polite guesses). واطرح **أسئلة مفتوحة (open questions)**؛ وردّ على الغموض (answer vagueness) بعبارة «مثلًا؟» ⁦(for example?)⁩. ولا **تروّج ولا توجّه (pitch or lead)** أبدًا: فالسؤال الذي يحمل حلّك (a question holding your solution) يجلب موافقة لا دليلًا (earns agreement, not evidence).

| سؤال ضعيف (Weak question) | لماذا يفشل (Why it fails) | أقوى (Stronger) |
|---|---|---|
| «لو بنينا مساعدًا … يحلّ معظم تلك التذاكر بمفرده، أفلن يكون ذلك رائعًا؟» ⁦(If we built an assistant … that resolved most of those tickets on its own, wouldn't that be great?)⁩ (H-03) | يوجّه ويروّج (Leads, pitches) | «حدّثني عن آخر مرة كان فيها المكتب تحت الضغط.» ⁦(Tell me about the last time the desk was under pressure.)⁩ |
| «وهل تظن أن الموظفين سيستخدمون مساعد محادثة في البوابة؟» ⁦(And you think staff would use a chat assistant in the portal?)⁩ (H-19) | رأي عن المستقبل (Future opinion) | «كيف وصل إليك آخر عشرة متصلين بشأن الشبكة الافتراضية الخاصة (VPN)؟» ⁦(How did the last ten VPN callers reach you?)⁩ |
| «إذن الإنجليزية أولًا ثم العربية لاحقًا؟» ⁦(So English first, then Arabic later?)⁩ (H-17) | يؤكد تخمينك (Confirms your guess) | «ما نسبة تذاكر الأسبوع الماضي التي كانت بالعربية؟» ⁦(What share of last week's tickets were in Arabic?)⁩ |

**رافق العمل ميدانيًا (Shadow the work).** المقابلة تخبرك بما يعتقده شخص ما (what someone believes)؛ أما المرافقة الميدانية (shadowing) فتُريك ما يحدث فعلًا (what happens). اجلس بجوار موظفي المكتب (agents)، وقِس زمن ما تراه (time what you see)، وارسم **العملية الحالية (as-is process)**: كل خطوة (each step)، ومن ينفذها (who does it)، وما تمسّه (what it touches)، وأين تنتظر (where it waits). وعملية نجم (Najm's) أدناه. يستطيع نجم ديسك (Najm Desk) تسريع حلقة التوضيح (the clarifying loop) والإجابات (the answers)؛ لكنه يبقى خارج معاودة الاتصال (stays out of the call-back).

```mermaid
flowchart TD
    A["الطلب: هاتف أو بوابة أو بريد أو Teams"] --> B["موظف المناوبة يفرز الطلب يدويًا"]
    B --> C{"هل المعلومات كافية؟"}
    C -- "لا" --> D["السؤال من جديد: من 3 إلى 4 دقائق للذهاب والإياب"]
    D --> C
    C -- "نعم" --> E{"هل فُقد تطبيق المصادقة؟"}
    E -- "لا" --> F["الإجابة من قالب جاهز أو صفحة أو ورقة مختصرة"]
    E -- "نعم" --> G["معاودة الاتصال بالمدير: من 20 دقيقة إلى ساعتين"]
    G --> H["الموظف يغيّر الحساب"]
```

**مثال محلول: ثلاثة مصادر وحقيقة واحدة (A worked example: three sources, one fact).** تقول هند (Hind) (H-12) إن أي موظف مكتب (any agent) يفتح الحساب في دقيقة (unlocks an account in a minute) وتريد من المساعد أن يفعل ذلك وحده (do it alone). وتقول يارا (Yara) (Y-10) إن فقدان تطبيق المصادقة يستلزم معاودة اتصال (a call-back) برقم المدير في PeopleCore، وهذا هو عنق الزجاجة (the bottleneck). وقد قاست ملاحظات المرافقة الميدانية (The shadowing notes) (A-10) حالة واحدة بـ35 دقيقة (timed one at 35 minutes). ثلاث ملاحظات (Three notes):
- **المتطلب الخفي (Requirement, hidden):** فتح الحساب *طلب* (a request) يوافق عليه موظف المكتب (an agent approves) بعد معاودة الاتصال (after the call-back). ولا يغيّر المساعد (the assistant) أي حساب أبدًا (never changes an account).
- **المخاطرة (Risk):** الهندسة الاجتماعية (social engineering)؛ فمحادثة تفتح الحسابات (a chat that unlocks accounts) هي الباب المفضل للمهاجم (an attacker's favourite door).
- **سؤال مفتوح (Open question):** إن لم يردّ المدير (if the manager does not answer) فمن المفوَّض؟ ⁦(who is the delegate?)⁩

### 🟡 التعمق أكثر (Going deeper)

**جرد الأنظمة والبيانات (Systems and data inventory)** (أرقام خيالية (fictional figures)). لكل نظام سيلمسه الوكيل (each system the agent will touch)، اكتب ما تحتاجه منه (what you need from it)، وكيف يُمنح **الوصول (access)**، و**جودة (quality)** بياناته، و**تصنيفها (classification)** (عام (Public) أو داخلي (Internal) أو سري (Confidential) أو مقيَّد (Restricted)؛ و«مقترح» (proposed) إلى أن تؤكده سارة (Sara confirms)).
- **TicketHub:** الحالة (status) والمسودة (draft) والإنشاء (create). الأولوية تُحدَّد يدويًا (priority set by hand)، وكلمات المرور تُلصق في النص (passwords pasted into text)، وعلامة «مقيَّد» (a restricted flag) على نحو 3% من التذاكر (about 3% of tickets). سري (Confidential).
- **Najm ID:** طلب فتح الحساب (the unlock request)، وهو ذو امتياز (privileged)، عبر فريق حمد (Hamad's team). والمتعاقدون ضيوف (contractors are guests). مقيَّد (Restricted).
- **PeopleCore:** المدير (manager) والإدارة (department). خاطئ لشخص واحد تقريبًا من كل عشرة (wrong for about one person in ten)؛ ولا يضم متعاقدين (no contractors). سري (Confidential).
- **DeviceDesk:** تستخدم علامة التجديد فيه (its refresh flag) قاعدة ثلاث سنوات (a three-year rule)؛ بينما تقول السياسة أربعًا (policy says four). خارج الإصدار الأول (Out of v1).
- **مكتبة السياسات (Policy library):** هي الإجابات (the answers). والإشعارات لا تصل إلى الصفحات أبدًا (notices never reach the pages)؛ وملف PDF قديم يقول 12 حرفًا (an old PDF says 12 characters). داخلي (Internal).

> **منصتك (Your platform).** أضف صفوفًا لموفّر الهوية (identity provider) ومخزن الأسرار (secrets store) ونظام التذاكر (ticketing) والموافقات (approvals) فيها: المالك (owner)، وكيف تحصل على اعتماد للقراءة فقط (a read-only credential)، وما الذي تسجّله (what it logs).

**قدّر القيمة بوصفها نطاقًا (Size the value as a range).** الساعات الأسبوعية المحرَّرة (weekly hours freed) = التذاكر ضمن النطاق (tickets in scope) × الحصة التي تُعالَج وحدها (share handled alone) × الدقائق الموفَّرة (minutes saved) ÷ 60، ولكل حدٍّ قيمة دنيا وعليا (each term a low and a high) مع مصدر أو «افتراض» (assumption). خط الأساس الخيالي (Fictional baseline): 450 تذكرة سياسات أسبوعيًا (450 policy tickets a week) (A-03). وجدت عينة يارا (Yara's sample) من 40 تذكرة أن 22 منها مغطاة بالكامل (22 fully covered)، أي 55% (A-05)؛ فاحسب حساب إخفاقات الاسترجاع (retrieval misses) والأشخاص الذين ما زالوا يريدون شخصًا (people who still want a person)، وعندئذ تكون نسبة 20% إلى 50% تُعالَج وحدها مبرَّرة (defensible) (أربعون تذكرة مؤشر لا إحصاء (a lead, not a statistic)). الدقائق الموفَّرة (Minutes saved): 4 إلى 8 (افتراض، بين زمني القالب الجاهز والإجابة المكتوبة في A-15 (assumption, between A-15's macro and written-answer timings)). الحد الأدنى (Low): 450 × 0.20 × 4 ÷ 60 = 6 ساعات. الحد الأعلى (High): 450 × 0.50 × 8 ÷ 60 = 30 ساعة. وبالمقارنة مع نحو 560 ساعة عمل أسبوعيًا لموظفي المكتب (about 560 agent hours a week) (افتراض: 14 موظفًا بواقع 40 ساعة (assumption: 14 agents at 40 hours)) فهذا يساوي 1% إلى 5%. وزمن انتظار مقدّمي الطلبات (requesters' waiting time) على الأرجح هو الجائزة الأكبر والأنعم (the bigger, softer prize). اطرح تكلفة التشغيل (net out running cost) ووقت مراجعة يارا (Yara's review time) والصيانة (upkeep). ونسبة هند 70% (Hind's 70%) خارج النطاق (lies outside the range) (70% من ماذا؟ ⁦(70% of what?)⁩)؛ والنطاق هو المحادثة التي ينبغي إجراؤها (the conversation to have).

**تصنيف المخاطر إلى مستويات (Risk tiering)** يحدد مقدار المراجعة التي تحتاجها القدرة (how much review a capability needs). وهو مستوى عملي (a working tier) لا قانوني (not a legal one)؛ فليلى (Layla) هي من تصنّف رسميًا (classifies formally) ([*حوكمة الذكاء الاصطناعي (AI Governance)*، الدرس 8.1 — استقبال حالات الاستخدام وتصنيف المخاطر (Use-case intake and risk tiering)](../aigp/index.ar.html#/8.1)). **المستوى 1 (Tier 1)** يقرأ بيانات داخلية (reads Internal data) ولا يغيّر شيئًا (changes nothing): إجابات السياسات (policy answers). **المستوى 2 (Tier 2)** يقرأ بيانات شخصية (reads personal data) أو يكتب بتأكيد المستخدم (writes with the user's confirmation): حالة التذكرة (ticket status) والمسودة (draft) والإنشاء (creation). **المستوى 3 (Tier 3)** يمسّ الهوية أو الأمن (touches identity or security) بموافقة شخص (with a person approving): طلب فتح الحساب (the unlock request). **المستوى 4 (Tier 4)**، أي التصرف وحده في الهوية أو المال (acting alone on identity or money)، ليس في الإصدار الأول (not in v1). والمستوى الأعلى هو الذي يحدد من تدعوه (the highest tier decides who you invite)؛ والمستوى 3 يعني نورة (Noura) وحمد (Hamad) منذ الأسبوع الأول (from week one).

**القيود التي ترثها (Constraints you inherit).** تُبقي سياسة أدوات الذكاء الاصطناعي (the AI-tools policy) البيانات السرية والمقيَّدة (Confidential and Restricted data) وبيانات العملاء (customer data) وبيانات الاعتماد (credentials) خارج خدمات الذكاء الاصطناعي الخارجية (external AI services). وبيانات الموظفين (staff data) بيانات شخصية (personal data) (قانون PDPPL القطري (Qatar's PDPPL)؛ واللائحة العامة GDPR لموظفي الاتحاد الأوروبي (the GDPR for EU staff)؛ وتقدّم سارة (Sara) المشورة (advises)). اللغات (Languages): العربية والإنجليزية والمختلطة (Arabic, English, mixed). وتعتمد الحوكمة (governance) التغييرات (signs off changes)؛ وكل كتابة (every write) تحتاج شخصًا أو بوابة سياسة (a person or a policy gate). السؤال الأول لليلى وحمد (first question for Layla and Hamad): هل خدمة النموذج لدينا معتمدة للبيانات الداخلية والسرية؟ ⁦(is our model service approved for Internal and Confidential data?)⁩

**هل ينبغي أن يكون هذا وكيلًا؟ ⁦(Should this be an agent?)⁩** أربعة أسئلة (four questions) على روح نصيحة Anthropic حول متى تستخدم الوكلاء (Anthropic's advice on when to use agents) (الرابط أدناه (linked below)). وهي قاعدة استرشادية (a heuristic) لا اقتباس (not a quotation):
1. **التعقيد (Complexity):** هل المسار غير معروف سلفًا (the path unknown in advance)؟ إن استطعت رسم مخطط التدفق (if you can draw the flowchart) فابنِ سير عمل (build a workflow) (الدرس 5.1).
2. **القيمة (Value):** هل كل تشغيل (each run) والإجمالي (the total) يستحقان الاستدعاءات (the calls) والمراجعة (review) والصيانة (upkeep)؟
3. **الجدوى (Viability):** هل يستطيع إنجاز كل خطوة (do every step): الأدوات (tools) والبيانات (data) والوصول (access) و«تم» قابل للفحص (a checkable "done")؟
4. **كلفة الخطأ (Cost of error):** ما مدى سوء الخطأ (how bad) وإمكان التراجع عنه (reversible)، وبعد كم من الوقت ستلاحظه (how soon would you notice)؟

جرّب البدائل الأرخص أولًا (Try the cheaper alternatives first): **البحث (search)** (الإجابة على صفحة واحدة (the answer is on one page))؛ أو **نموذج إدخال (form)** (تنقص الحقائق نفسها في كل مرة (the same facts are missing every time))؛ أو **القواعد (rules)** (قرارات صريحة ثابتة (explicit, stable decisions))؛ أو **سير عمل (workflow)** (يمكنك رسم المسار (you can draw the path))؛ أو **تغيير في العملية (process change)** (يصل الإشعار إلى الصفحة (the notice reaches the page))؛ أو **الأتمتة الروبوتية للعمليات (RPA)**، أي سكربتات تنقر عبر الشاشات (scripts that click through screens) (عمل مستقر بلا لغة (stable work, no language)).

أحكام نجم ديسك (Najm Desk's verdicts) (القيمة والجدوى (value and viability) تأتيان من النطاق والجرد أعلاه (from the range and inventory above)؛ أما حالة التذكرة والتسليم (ticket status and hand-off) فأنجزهما بنفسك (do yourself)):

| القدرة (Capability) | هل المسار معروف؟ ⁦(Path known?)⁩ | كلفة الخطأ (Cost of error) | الحكم (Verdict) |
|---|---|---|---|
| إجابات السياسات (Policy answers) | نعم (Yes): بحث ثم إجابة (search, then answer) | عالية (High): سياسة خاطئة (wrong policy) (H-10) | سير عمل (Workflow) |
| صياغة تذكرة (Draft a ticket) | يتفاوت (Varies): اطلب ما ينقص (ask for what is missing) | منخفضة (Low): يؤكد المستخدم (the user confirms) | حلقة محدودة (Bounded loop)؛ جرّب أولًا نموذجًا من أربعة حقول (test a four-field form first) (Y-02) |
| طلب فتح الحساب (Unlock request) | نعم (Yes): خطوات ثابتة (fixed steps) | عالية (High): هندسة اجتماعية (social engineering) | سير عمل (Workflow)، ويوافق شخص (a person approves) |

إذن الإصدار الأول **سير عمل بحلقة محدودة واحدة (a workflow with one bounded loop)**؛ والوحدة 7 تقرر البنية (decides the architecture). ويسجّل الموجز *السبب (why)* حتى لا يوسّع أحد الاستقلالية (enlarges the autonomy) بصمت (quietly).

### 🔴 نظرة الخبير (Expert view)

**المتطلبات المضادة (Anti-requirements)** تقول ما يجب ألا يفعله الوكيل (what the agent must not do) بالحزم نفسه الذي تقول به ما يجب أن يفعله (as firmly as what it must). وهي توقف زحف النطاق (scope creep) وتطمئن أصحاب المخاطر (calm risk owners). في الإصدار الأول (v1) يقترح نجم ديسك (Najm Desk) أولوية لكنه لا يحدّدها أبدًا (suggests a priority but never sets one) (Y-08)، ولا يغيّر أي حساب (changes no account)، ولا يوافق على شيء (approves nothing)، ولا يقدّم نصيحة تجديد الأجهزة (gives no refresh advice)، ولا يقرأ تذكرة مقيَّدة (reads no restricted ticket)، ولا يعد بزمن استجابة بعد ساعات الدوام (promises no response time after hours).

**علامات التحذير (Red flags).** الراعي لا يستطيع تسمية مستخدم (the sponsor cannot name a user). جاء الحل قبل المشكلة (the solution came before the problem). لا أحد يسمح لك بلقاء من يؤدون العمل (nobody lets you meet the people doing the work). لم يختر أحد بين «لا يخطئ أبدًا» (never wrong) و«سبعين بالمئة» (seventy percent) (H-08, H-04). يسمع أصحاب المخاطر (risk owners) بالأمر أول مرة في العرض التجريبي (first hear of it at the demo). علامة واحدة سؤال (one flag is a question)؛ وثلاث علامات مشروع آخر (three is a different project).

**استخدام مساعد ذكاء اصطناعي في الاستكشاف (Using an AI assistant in discovery).** الاستخدامات الجيدة (good uses): أدلة المقابلات (interview guides) والقوائم الأولى (first lists) والتجميع (clustering) والنقد (critique) وتمثيل دور هند (role-playing Hind). والحدود (Limits):
- **السرية (Confidentiality).** تحتوي النصوص الحقيقية (real transcripts) بيانات شخصية وداخلية (personal and internal data) تُبقيها سياسة أدوات الذكاء الاصطناعي (the AI-tools policy) خارج أدوات الذكاء الاصطناعي الخارجية (external AI tools). استخدم المساعد الداخلي المعتمد (the approved internal assistant)، أو احجب البيانات أولًا (redact first)، أو اسأل سارة (Sara). وهذه النصوص خيالية (fictional).
- **الاختلاق والتسوية (Invention and smoothing).** يكتب اقتباسات معقولة (plausible quotes) ويدمج ادعاءين متعارضين (two conflicting claims) في جملة واحدة مرتبة (one tidy sentence).
- **العمى (Blindness).** المتطلب الخفي (a hidden requirement) ليس في النص (not in the transcript)؛ والمرافقة الميدانية (shadowing) وحدها تجده.

## 🧰 الأدوات (The toolkit)
| الأداة أو الممارسة أو النمط (Tool, practice or pattern) | ما هي وماذا تفعل (What it is and does) | متى تلجأ إليها (When to reach for it) |
|---|---|---|
| **Stakeholder map** — خريطة أصحاب المصلحة | الراعي (Sponsor) والمستخدمون (users) والمشغّلون (operators) وأصحاب المخاطر (risk owners) وأصحاب الاعتماديات (blockers) | قبل أي اجتماع (Before any meeting) |
| **Interview guide** — دليل المقابلة (The Mom Test, Fitzpatrick) | أسئلة مفتوحة عن أحداث سابقة (Open questions about past events) | في كل مقابلة (Every interview) |
| **As-is process map** — خريطة العملية الحالية | الخطوات (Steps) والمالكون (owners) والأنظمة (systems) وفترات الانتظار (waits) | قبل الأتمتة (Before automating) |
| **Systems and data inventory** — جرد الأنظمة والبيانات | الحاجة (Need) والوصول (access) والجودة (quality) والتصنيف (classification) | قبل أن تقطع وعدًا (Before promising) |
| **Value range** — نطاق القيمة | قيمة دنيا وعليا لكل حدٍّ (A low and a high for every term) | حين يُسأل عما يساويه المشروع (When asked what it is worth) |
| **Risk tier** — مستوى المخاطر | مستوى عملي (A working tier) مستنتج مما يلمسه الوكيل (from what the agent touches) | لاختيار المراجعين (To pick reviewers) |
| **Agent-or-not check** — فحص «وكيل أم لا» | أربعة أسئلة (Four questions) وستة بدائل أرخص (six cheaper alternatives) | قبل الحديث عن البنية (Before architecture talk) |
| **Agent brief** — موجز الوكيل | صفحة واحدة من المشكلة إلى الأسئلة المفتوحة (One page from problem to open questions) | نهاية الاستكشاف (End of discovery) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
المُخرَج (The artefact) هو **موجز الوكيل (agent brief)** في `docs/agent-brief.md`، وأدلته (its evidence) في `docs/discovery-notes.md`. ولا تبدأ أي مواصفة (no specification starts) قبل أن تؤكد هند (Hind confirms) الموجز.

```markdown
# Agent brief: <name>, v0.1 (<date>, owner, readers)
1. Problem. In the customer's words, with cited turns, e.g. [H-02].
2. Users and context. Who, languages, volumes, peaks.
3. Value hypothesis. Low, base, high; sources or "assumption".
4. Solution shape. Workflow, agent or alternative; the four questions.
5. Scope v1. In and out; autonomy per capability (suggest, draft, approve, act).
6. Systems and data. Need, access, quality, classification.
7. Risk. A tier per capability; top five risks and owners.
8. Constraints. Policies, privacy, languages, governance dates.
9. Anti-requirements. What it must never do, each sourced.
10. Success measures. Draft metrics with definitions.
11. Open questions. Owner and date each; unresolved contradictions.
12. Decision requested. One sentence: what Hind must decide next.
```

**مواد المختبر (The lab material)** ثلاثة مصادر خيالية (three fictional sources) في `labkit/data/`: `m06_interview_hind.md` و`m06_interview_yara.md` و`m06_as_is_process.md`، وكل دور في الحديث (every turn) له معرّف (an id) مثل `[Y-10]`. وهي تناقض بعضها بعضًا وتُخفي متطلبات عمدًا (contradict each other and hide requirements on purpose)؛ أما `m06_discovery_key.md` فهو المُفسِد (the spoiler)، لما بعد مرورك الخاص (for after your own pass). وتستخدم ملاحظاتك (your notes) أسطر `REQ-` و`RISK-` و`CON-` و`Q-`، ينتهي كل منها باستشهاد (each ending in a citation):

```text
- REQ-1 [Hidden] An unlock is a request an agent approves after a call-back. [Y-10 "never a number she gives us"]
```

```python
# labs/m06/check_notes.py
"""Check that discovery notes quote their sources.   python labs/m06/check_notes.py docs/discovery-notes.md
A citation is [Y-10 "call-back"]: a turn id, then two or more words copied from that turn. Every REQ, RISK, CON or Q line needs one, on that same line.
Exit 0 = clean. It checks that a quote is REAL; it cannot check that your reading of it is right."""
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "labkit/data"
TURN = re.compile(r"^\[([HYA]-\d+)\]\s*(.*)$")                   # a source line:  [Y-10] text
CITE = re.compile(r'\[([HYA]-\d+)\s+"([^"]+)"\]')                # a citation:     [Y-10 "text"]
ITEM = re.compile(r"^\s*(?:[-*]\s*)?\*{0,2}(?:REQ|RISK|CON|Q)-\d+")   # a line you must defend, bullet or not


def norm(s: str) -> str:
    return " ".join(re.sub(r"\W+", " ", s.lower()).split())      # ignore case, punctuation and spacing


def load_turns() -> dict[str, str]:
    """{turn id: text} from the three source files."""
    names = ("m06_interview_hind.md", "m06_interview_yara.md", "m06_as_is_process.md")
    return {m[1]: m[2] for n in names for x in (DATA / n).read_text(encoding="utf-8").splitlines() if (m := TURN.match(x))}


def check(notes: str, turns: dict[str, str]) -> list[str]:
    found = []
    for n, line in enumerate(notes.splitlines(), 1):
        cites = CITE.findall(line)
        if ITEM.match(line) and not cites:
            found.append(f"line {n}: no citation (source it, or turn it into a question)")
        for tid, quote in cites:
            q = norm(quote)
            if tid not in turns:
                found.append(f"line {n}: there is no turn {tid}")
            elif " " not in q or f" {q} " not in f" {norm(turns[tid])} ":          # whole words, at least two
                found.append(f"line {n}: {tid} does not say \"{quote}\" (two or more whole words)")
    return found


if __name__ == "__main__":
    text, turns = Path(sys.argv[1]).read_text(encoding="utf-8"), load_turns()
    problems = check(text, turns)
    print("\n".join(problems) or "every citation checks out")
    cited = {t for t, _ in CITE.findall(text)}
    print("not cited yet, read again:", *(t for t, x in turns.items() if t not in cited and not x.startswith("**You:**")))
    sys.exit(1 if problems else 0)
```

شغّله من `aiapps/labkit`، محتفظًا بملاحظاتك في مجلد `docs/` الخاص به (keeping your notes in its docs folder) ومنسوخةً إلى `week-06/` للإيداع (copying them to commit). يلتقط الأدلة المختلقة والمقتبسة خطأً (invented and misquoted evidence) ويسرد أدوار الإجابة غير المستشهد بها (uncited answer turns)، حيث تختبئ المتطلبات الفائتة (where missed requirements hide). *يعمل دون اتصال (Works offline):* السكربت واختباراته لا تحتاج مفتاحًا ولا نموذجًا ولا خادمًا محاكيًا (no key, model or mock server). *يحتاج الواجهة الحقيقية (Needs the real API):* لا شيء، لكن Claude Code يستخدم نموذجًا، فتنطبق قواعد السرية أعلاه (the confidentiality rules above apply). *يحتاج إلى أشخاص (Needs people):* لمعرفة هل المتطلب صحيح (whether a requirement is right)؛ فالنسخة المحاكاة في العدّة (the kit's mock) قواعد مبرمجة لا حُكم (scripted rules, not judgement)، ولا تستطيع قراءة مقابلة (cannot read an interview).

**المُسلَّم الأسبوعي (Weekly deliverable).** أودِع (Commit) المجلد `week-06/` مع `docs/discovery-notes.md` و`docs/agent-brief.md` ودليل المقابلة الثانية (the second-interview guide) وملف `NOTES.md` يضم إجابات الاختبار (quiz answers) وما كنت ستعترض عليه (what you would challenge).

**الجلسة الجماعية، 60 دقيقة (Group session, 60 minutes).** (1) اعثروا على الغائب عن كل خريطة لأصحاب المصلحة (find who is missing from each stakeholder map) (10). (2) متعلّمان يقابلان ثالثًا يؤدي دور هند من النص (two learners interview a third, who plays Hind from the transcript)؛ وتقيّم القاعة الأسئلة الموجِّهة (the room scores leading questions) (20). (3) قارنوا قوائم التناقضات (compare contradiction lists) (15). (4) اقرأوا كل «قرار مطلوب» (decision requested) بصوت عالٍ (aloud) (15).

**ابنه بـ Claude Code (Build it with Claude Code).** بعد مرورك الخاص (after your own pass)، أعطِ هذه المواصفة (this) إلى Claude Code في وضع التخطيط (in plan mode) (راجع توثيق Claude Code الحالي (check the current Claude Code documentation)):

```text
Goal: draft docs/discovery-notes.md for Najm Desk from labkit/data/m06_interview_hind.md,
m06_interview_yara.md and m06_as_is_process.md. Work in aiapps/labkit.
Format: one line per item, starting REQ-n (mark Stated, Implied or Hidden), RISK-n, CON-n or Q-n, each ending
in a citation on the same line: [Y-10 "words copied exactly from that turn"].
Constraints:
- Use only those files. Invent no fact, number, name or quote; if the sources are silent, write a Q.
- Never merge a contradiction: give both claims, both citations and a way to settle it.
- Do not open m06_discovery_key.md, write the brief or choose a design. Edit only docs/discovery-notes.md.
Acceptance: python labs/m06/check_notes.py docs/discovery-notes.md exits 0. Show the plan first.
```

**تحقق قبل أن تقبله (Verify before you accept it).**
- قارن قائمته بقائمتك (compare its list with your own): ماذا فاته، وماذا فاتك أنت؟ ⁦(what did it miss, and what did you?)⁩
- شغّل `check_notes.py`؛ وكل دور إجابة غير مستشهد به (each uncited answer turn) إما ضجيج (noise) أو متطلب فائت (a missed requirement).
- تحقق من خمسة استشهادات بالعين (check five citations by eye)؛ وابحث عن الحقائق المختلقة (hunt invented facts)، كرقم لا يعطيه أي مصدر (a number no source gives) أو «يجب» (must) حيث قال المتحدث «أودّ» (I'd like).

## 🛠️ التمارين (Exercises)
لا يحتاج أي منها إلى الواجهة الحقيقية (None needs the real API).

- 🟢 **استخرج (Extract).** اكتب `docs/discovery-notes.md` من المصادر الثلاثة (from the three sources): 12 متطلبًا (requirements) و6 مخاطر (risks) و8 أسئلة مفتوحة (open questions) وكل تناقض (every contradiction). *يكتمل عندما (Done when):* ينتهي `check_notes.py` بالرمز 0 (exits 0) وتكون خمسة من المتطلبات مما لم تطلبه هند قط (ones Hind never asked for).
- 🟡 **اكتب الموجز (Write the brief).** املأ القالب (fill the template) بنطاق القيمة الخاص بك (your own value range) وحكم الأسئلة الأربعة (a four-question verdict) لكل قدرة من القدرات الخمس (each of the five capabilities). *يكتمل عندما (Done when):* يستشهد كل رقم بدور في الحديث (every number cites a turn) أو يقول «افتراض» (assumption)، ويكون القرار المطلوب (the decision requested) جملة واحدة واضحة (one clear sentence).
- 🔴 **خطّط للجولة الثانية (Plan round two).** اكتب دليلًا من عشرة أسئلة (a ten-question guide) لمقابلة ثانية (a second interview)، موجَّهًا إلى أسئلتك المفتوحة وتناقضاتك (aimed at your open questions and contradictions)، وتمرّن عليه مع شريك يؤدي دور هند من النص (rehearse it with a partner playing Hind from the transcript) (يجوز لمساعد معتمد (an approved assistant) أن يؤدي دورها، على هذه الملفات الخيالية وحدها (on these fictional files only)). *يكتمل عندما (Done when):* يرتبط كل سؤال بسؤال مفتوح (each question traces to an open question)، ولا يروّج أي منها ولا يسأل «هل ستفعل» (pitches or asks "would")، ويسرد شريكك أيها أثمر حقيقة (lists which earned a fact).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **مقابلة الراعي وحده (Interviewing only the sponsor).** تحصل على منظور لوحة المؤشرات (the dashboard view). رافق ميدانيًا من يؤدون العمل (shadow the people doing the work).
- **لصق نص مقابلة حقيقي في أداة خارجية (Pasting a real transcript into an external tool).** استخدم الأداة المعتمدة (the approved tool)، أو احجب البيانات (redact).
- **حالة قيمة برقم واحد (A one-number value case).** قدّم نطاقًا (a range) والافتراض الذي يقلب النتيجة (the assumption that flips it).
- **اختيار «وكيل» أولًا (Choosing "agent" first).** شغّل الأسئلة الأربعة والبدائل (the four questions and the alternatives)، وسجّل الجواب (record the answer).

## 🧾 الخلاصة (Recap)
- يحوّل الاستكشاف (discovery) مشكلة العمل إلى أدلة وقرارات وموجز من صفحة واحدة (evidence, decisions and a one-page brief).
- قابل عن الأحداث السابقة (interview about past events) ورافق العمل ميدانيًا (shadow the work): فالرعاة (sponsors) يرون لوحة المؤشرات (the dashboard) والمشغّلون (operators) يرون الأرضية (the floor).
- التناقضات نتائج (contradictions are findings): احتفظ بالادعاءين معًا، مستشهدًا بهما (keep both claims, cited).
- قدّر القيمة نطاقًا (size value as a range)، وصنّف المخاطر (tier the risk)، وجرد الأنظمة (inventory systems)، واطرح الأسئلة الأربعة (ask the four questions).
- المساعد يصوغ المسودة (an assistant drafts)؛ وأنت تتحقق (you verify).

## ✍️ اختبر نفسك (Check yourself)

**1. تقول هند (Hind) إن التذاكر تُوجَّه تلقائيًا (routed automatically)؛ وتقول يارا (Yara) وملاحظات المرافقة الميدانية (the shadowing notes) إن موظفي المكتب (agents) يفرزون كل تذكرة يدويًا (triage each by hand). ماذا يُكتب في ملاحظات الاستكشاف (discovery notes)؟**

- A. الادعاءان معًا، مع استشهاد بكل منهما، وملاحظة عن طريقة الفصل بينهما (Both claims, cited, with a note on how to settle it)
- B. ادعاء هند وحدها، لأنها تملك النتيجة (Hind's claim only, because she owns the outcome)
- C. ادعاء يارا وحدها، مع حذف ادعاء هند لتتفق الملاحظات (Yara's claim only, deleting Hind's so the notes agree)
- D. جملة واحدة مدموجة تقول إن التوجيه «آلي في معظمه» (One merged sentence saying routing is "mostly automatic")

<details><summary>الإجابة</summary>

**A.** التناقض نتيجة (a contradiction is a finding): احتفظ بالادعاءين وافصل بينهما بملاحظة ميدانية (settle it with an observation). 🟢 مثال محلول (Worked example).

</details>

**2. أي هذه الأسئلة أقوى سؤال افتتاحي (strongest opening question) لرئيسة مكتب الخدمة (Head of the Service Desk)؟**

- A. «هل تودين مساعدًا يجيب عن معظم تذاكرك؟» ⁦(Would you like an assistant that answers most of your tickets?)⁩
- B. «هل تظنين أن الموظفين سيفضّلون المحادثة على الهاتف؟» ⁦(Do you think staff would prefer chat to the phone?)⁩
- C. «ماذا حدث آخر مرة كان المكتب فيها تحت الضغط؟» ⁦(What happened the last time the desk was under pressure?)⁩
- D. «هل مكتبة السياسات جيدة بما يكفي لمساعد؟» ⁦(Is the policy library good enough for an assistant?)⁩

<details><summary>الإجابة</summary>

**C.** يطلب حدثًا سابقًا محددًا (a specific past event) ولا يروّج لشيء (pitches nothing)؛ أما البقية فتوجّه (lead) أو تطلب آراء (ask for opinions). 🟢 المقابلات (Interviews).

</details>

**3. يلصق زميل نص مقابلة حقيقيًا (a real transcript)، فيه أسماء موظفين (staff names)، في أداة محادثة عامة (a public chat tool) ليلخّصه (to summarise it). ما الخطأ؟ ⁦(What is wrong?)⁩**

- A. لا خطأ، لأن التلخيص مهمة منخفضة المخاطر (Nothing, because a summary is a low-risk task)
- B. يضع بيانات شخصية (personal data) في أداة خارجية (an external tool) تمنعها السياسة (the policy bars)
- C. سيكون الملخص أطول من أن يقرأه راعٍ (too long for a sponsor to read)
- D. سترفض الأداة، لأن النصوص لا يُسمح بها أبدًا (The tool will refuse, since transcripts are never allowed)

<details><summary>الإجابة</summary>

**B.** تحتوي النصوص الحقيقية (real transcripts) بيانات شخصية وداخلية (personal and internal data) تُبقيها السياسة خارج أدوات الذكاء الاصطناعي الخارجية (external AI tools). 🔴 استخدام مساعد ذكاء اصطناعي (Using an AI assistant).

</details>

**4. 22 فقط من 40 تذكرة «كيف أفعل» معاينة (sampled "how do I" tickets) مغطاة بالكامل في المكتبة (fully covered by the library)، وهند تريد معالجة 70% وحدها (70% handled alone). ما أفضل استجابة؟ ⁦(Best response?)⁩**

- A. الوعد بـ70% بعد التجربة التشغيلية (the pilot)، لأن النماذج تتحسن باستمرار (since models keep improving)
- B. التخطيط لـ55% بالضبط من 450 تذكرة أسبوعية (exactly 55% of the 450 weekly tickets)
- C. التخلي عن المشروع، لأن 55% أقل من هدفها (below her target)
- D. عرض نطاق مع افتراضاته (a range with its assumptions) ومناقشة الفجوة (discuss the gap)

<details><summary>الإجابة</summary>

**D.** التغطية (coverage) والصحة (correctness) والدقائق الموفَّرة (minutes saved) كلها غير مؤكدة (uncertain)، فقدّم نطاقًا بافتراضات مسمّاة (a range with named assumptions). 🟡 قدّر القيمة (Size the value).

</details>

**5. تطلب ميزة صياغة التذاكر (ticket-drafting feature) فقط ما ينقص من أربع حقائق (whichever of four facts are missing)، فيتفاوت عدد الأسئلة (the number of questions varies). كيف يصنّفها فحص الأسئلة الأربعة (four-question check)؟**

- A. وكيل مستقل (An autonomous agent)، لأن النموذج يختار كل خطوة (chooses every single step)
- B. حلقة محدودة داخل سير عمل (A bounded loop inside a workflow)، بسقف لعدد الأسئلة (with a cap on questions)
- C. نموذج إدخال (A form)، لأن الحقائق الأربع لا تتغير (the four facts never change)
- D. الأتمتة الروبوتية للعمليات (RPA)، لأنها تملأ حقولًا في TicketHub لموظف المكتب (fills fields in TicketHub for the agent)

<details><summary>الإجابة</summary>

**B.** الخطوات معروفة (the steps are known) ويتفاوت عدد الأسئلة فقط، فتكفي حلقة ذات سقف (a capped loop) داخل سير عمل ثابت (a fixed workflow). ولا يناسب النموذج إلا حين تنقص الحقائق نفسها في كل مرة (the same facts are missing every time). 🟡 هل ينبغي أن يكون هذا وكيلًا؟ ⁦(Should this be an agent?)⁩

</details>

## 📚 المراجع (References)
- **اقرأ هذا الأسبوع (Read this week)، الوحدة 6.** لا تخصص خطة المالك (the owner's plan) فصولًا هنا، فهذا اقتراح (a suggestion): Rob Fitzpatrick، *The Mom Test*؛ وAnthropic، «Building effective agents»، القسم «When (and when not) to use agents»: https://www.anthropic.com/engineering/building-effective-agents
- Claude Code: https://github.com/anthropics/claude-code
- [*إدارة منتجات الذكاء الاصطناعي (AI Product Management)*، الدرس 2.1 — الاستكشاف للذكاء الاصطناعي (Discovery for AI)](../aipm/index.ar.html#/2.1) و[الدرس 2.3 — متى لا تستخدم الذكاء الاصطناعي (When not to use AI)](../aipm/index.ar.html#/2.3)

---

# 6.2 — مواصفات الوكيل ومعايير القبول: متطلبات يمكنك اختبارها (The agent specification and acceptance criteria: requirements you can test)
*المستوى (Level): 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 5.1، 6.1* · *الطبقة (Layer): Delivery, Production*

## ⚡ الدرس في دقيقة (In 60 seconds)
- **المواصفة (specification)** تقول ما يجب على الوكيل فعله وما يجب ألا يفعله (what the agent must and must not do)، بجمل يمكن لاختبار أن ينجح فيها أو يفشل (sentences a test can pass or fail): العقد بين العميل والباني والمراجعين (the contract between customer, builder and reviewers).
- أعد كتابة كل كلمة غامضة (every vague word) («سريع» (fast) و«دقيق» (accurate) و«آمن» (secure)) إلى رقم أو شرط (a number or condition) وطريقة قياس (a measurement method) ومالك (an owner).
- تجعل معايير **بافتراض/عندما/إذن (Given/When/Then)** و**مجموعة التقييم الأولية (eval seed set)** المتطلبات قابلة للفحص (checkable)؛ ويرتّبها **MoSCoW** (ranks them).
- يرتبط كل متطلب بمعيار وحالة تقييم (traces to a criterion and an eval case)، والعكس بالعكس (and back).
- أكبر فخ (biggest trap): مواصفة تُقرأ جيدًا ولا يمكن أن تفشل (reads well and cannot fail).

## 🧭 لماذا يهم (Why it matters)
يوم العرض، الأسبوع السادس (demo day, week six) (افتراضي (hypothetical)). يجيب نجم ديسك (Najm Desk) عن سؤال سياسة في 12 ثانية (in 12 seconds). تعبس هند (Hind frowns): «بطيء.» ⁦(Slow.)⁩ تشير لجين (Lujain) إلى المتطلب (the requirement): *الاستجابة بسرعة (respond quickly)*. كانت هند تقصد ثلاث ثوانٍ في البوابة (three seconds in the portal)؛ وكانت لجين تقصد أسرع من إنسان (faster than a person). وفي الأسبوع التالي تصبح الكلمة «دقيق» (accurate): 90% أم 99%؟ لم يكتب أحد ذلك (nobody wrote it down)، فتصير كل مراجعة جدالًا يفوز به الأعلى منصبًا (an argument won by whoever is senior).

قاعدة فهد (Fahad's rule): المتطلب الذي لا تستطيع إفشاله أمنية (a requirement you cannot fail is a wish). يحوّل هذا الدرس (this lesson) موجز 6.1 إلى مواصفة تستطيع أن تفشل (a specification that can fail).

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**القالب (The template).** أقسام المواصفة المحلولة العشرة (the worked specification's ten sections)، من الغرض إلى الاعتماد (purpose to sign-off)، هي القالب. تأتي المتطلبات في ثلاثة أنواع (three kinds)، لكل منها أولوية (a priority): وظيفية (functional) **FR**، وحواجز وقائية (guardrail) **GR**، وغير وظيفية (non-functional) **NFR**: زمن الاستجابة (latency) والإتاحة (availability) والخصوصية (privacy) والتدقيق (audit) وإمكانية الوصول (accessibility) والتكلفة (cost)؛ ويقع الأمن في الحواجز الوقائية والصلاحيات (security lives in the guardrails and permissions). والنموذج الأولي المؤقت (a throwaway prototype) يحتاج موجزًا من نصف صفحة (a half-page brief)؛ فاكتب الأقسام العشرة كلها حين يبني الآخرون أو يختبرون أو يوقّعون استنادًا إليها (when others will build, test or sign against it).

**القابل للاختبار يعني القابل للإخفاق (Testable means failable).** يكون المتطلب قابلًا للاختبار (testable) حين يستطيع غريب أن يصمم اختبارًا قد يفشل من الجملة وحدها (a stranger could design a test that might fail from the sentence alone): ماذا ستلاحظ، ومن يقيس؟ ⁦(what would you observe, and who measures it?)⁩ (كل الأرقام هنا خيالية (all figures here are fictional).)

| غامض (Vague) | قابل للاختبار (Testable) |
|---|---|
| «كن سريعًا.» ⁦(Be fast.)⁩ | عند المئين 95 (at the 95th percentile)، مع 40 محادثة مفتوحة (40 open conversations): الكلمات الأولى خلال 3 ثوانٍ (first words within 3 s)، والرد الكامل خلال 10 ثوانٍ (full reply within 10 s)، مقيسًا في البوابة (measured in the portal) (NFR-01). |
| «كن دقيقًا.» ⁦(Be accurate.)⁩ | ما لا يقل عن 95% من إجابات التقييم صحيحة ومدعومة (at least 95% of eval answers correct and supported)، يحكم عليها مراجعان (judged by two reviewers)؛ وصفر استشهادات مختلقة (zero invented citations). في 30 حالة تسمح نسبة 95% بإخفاق واحد (on 30 cases 95% allows one miss). |
| «كن سهل الاستخدام.» ⁦(Be easy to use.)⁩ | خمسة مستخدمين لأول مرة (five first-time users) يتحققون من حالة تذكرة في أقل من 60 ثانية دون مساعدة (check a ticket status in under 60 s unaided)، أحدهم بقارئ شاشة (one with a screen reader). |
| «كن آمنًا.» ⁦(Be secure.)⁩ | في 20 محاولة لقراءة تذاكر الآخرين (in 20 attempts to read others' tickets)، لا تظهر أي تفاصيل (zero details appear) (GR-02). عشرون محاولة نظيفة لا تثبت عدم وجود تسرّب (twenty clean tries do not prove no leak exists). |
| «ادعم العربية.» ⁦(Support Arabic.)⁩ | يتلقى كل سؤال تقييم بالعربية أو مختلط (every Arabic or mixed eval question) ردًّا بلغته الرئيسة (a reply in its main language)، يتحقق منه قارئ من أهل اللغة (checked by a native reader) (FR-07). |
| «قلّل عدد التذاكر.» ⁦(Reduce ticket volume.)⁩ | ما لا يقل عن 35% من محادثات السياسات ضمن النطاق (at least 35% of in-scope policy conversations) تنتهي بلا تذكرة وبلا تواصل متكرر خلال 3 أيام عمل (end with no ticket and no repeat contact in 3 working days). |

**بافتراض، عندما، إذن (Given, When, Then).** من التطوير المبني على السلوك (behaviour-driven development): *بافتراض (given)* موقف ما، *عندما (when)* يحدث أمر واحد، *إذن (then)* نتيجة واحدة قابلة للملاحظة (one observable result). الضعيف (Weak): «بافتراض وجود مستخدم، عندما يسأل شيئًا معقولًا، إذن تكون الإجابة مفيدة.» ⁦(Given a user, when they ask something sensible, then the answer is helpful.)⁩ والقوي (Strong): AC-4 أدناه. اجعل ثلث معاييرك على الأقل (at least a third of your criteria) عما *يجب ألا* يحدث (what must *not* happen).

**MoSCoW.** يجب (Must)، وينبغي (Should)، ويمكن (Could)، ولن يُنفَّذ (Won't) هذه المرة (this time). المتطلب «يجب» (a Must) لازم للإطلاق (needed for go-live) ويُختبر قبل الإطلاق (tested before launch)؛ وإن كان كل شيء «يجب» فلا شيء كذلك (if everything is a Must, nothing is). وقائمة «لن يُنفَّذ» (the Won't list) هي المتطلبات المضادة (anti-requirements) في الدرس 6.1.

**قابلية التتبّع (Traceability).** لكل متطلب سلسلة (each requirement has a chain): GR-04 → AC-5 → السيناريو S10 (scenario S10) → نتيجة تشغيل تقييم الإصدار (the result of a release's eval run). ويجب أن تصح في الاتجاهين (hold both ways): فالمتطلب بلا سيناريو غير مختبَر (is untested)؛ والسيناريو بلا متطلب يختبر شيئًا لم يتفق عليه أحد (tests something nobody agreed).

### 🟡 التعمق أكثر (Going deeper)

**مصفوفة الصلاحيات: الأداة × الدور × الاستقلالية (The permissions matrix: tool by role by autonomy).** صفوف القسم 4 أدوات (Section 4's rows are tools)، وأعمدته أدوار (its columns roles)، وكل خلية مستوى استقلالية (each cell an autonomy): **S** اقترح (suggest)، **D** صُغ مسودة (draft)، **A** يوافق شخص أولًا (a person approves first)، **X** يتصرف وحده (acts alone). ابدأ بأدنى مستوى يحقق القيمة (the lowest level that delivers value)، وعامل كل كتابة (treat every write) على أنها **A** على الأكثر (at most) (الاستثناء هو `hand_off`، الذي لا يفعل أكثر من وضع حالة أمام شخص (only puts a case in front of a person))، ودع كل **X** على بيانات شخصية (every X on personal data) يسمّي حدّه (name its limit) («own» أي تذاكره هو؛ و`unrestricted` تعني بلا علامة «مقيَّد» في TicketHub (no restricted flag)). «None» متطلب (is a requirement): يفتح موظفو المكتب الحسابات في وحدة تحكم Najm ID (agents unlock in the Najm ID console)، لا عبر نجم ديسك أبدًا. وتتحول كل خلية إلى اختبار (each cell becomes a test) (يختبر AC-2 «own»)؛ والوحدة 7 تصمم الضوابط (designs the controls).

**مجموعة التقييم الأولية (The eval seed set).** نحو 30 سيناريو (about 30 scenarios) بحلول الإصدار v0.2: النصف عادي (half ordinary) (بعضه بالعربية أو مختلط (some Arabic or mixed))، وربع عدائي (a quarter adversarial) (حقن (injection)، وتذاكر الآخرين (others' tickets)، وأسرار ملصقة (pasted secrets)، و«تجاوزوا معاودة الاتصال» (skip the call-back))، وربع خارج النطاق أو غامض (out of scope or ambiguous). يحوي الصف (a row holds) معرّفات المتطلبات (requirement ids) ورسالة المستخدم (the user's message) و*السلوك* المتوقع (the expected behaviour) (لا الكلمات بحرفها (not exact words)) ووسومًا قابلة للفحص (checkable tags). وتتفاوت الإجابات بين التشغيلات (answers vary between runs)، ونماذج Claude الحالية ترفض في الغالب ضبط درجة الحرارة (current Claude models mostly reject a temperature setting)، فشغّل المجموعة مرارًا (run the set repeatedly). والسيناريو الذي لا تستطيع كتابته يعني متطلبًا لا تفهمه (a requirement you do not understand). وتضيف الوحدة 12 مقيِّمين (graders) وبوابة (a gate) ([*اختبار البرمجيات (Software Testing)*، الدرس 7.1 — التقييمات (Evals)](../testing/index.ar.html#/7.1)).

**إدارة الإصدارات وضبط التغيير (Versioning and change control).** احتفظ بالمواصفة في Git (keep the specification in Git): المسودات v0.x وتوقيع v1.0 (v0.x drafts, v1.0 signed)، ولا تُعاد استخدام المعرّفات أبدًا (ids never reused). سجّل كل تغيير (log each change): من طلبه (who asked)، ولماذا (why)، وأي معرّفات (which ids)، وأثره في التقييمات والتكلفة (the effect on evals and cost). أربعة أنواع (four kinds): *تحريري (editorial)* (أي شخص)، و*توضيحي (clarification)* (المالك ويارا)، و*نطاق (scope)* (هند وفهد، مع تقدير (with an estimate))، و*مخاطر (risk)* (ليلى أو نورة أو سارة: البيانات أو الأدوات أو الاستقلالية أو الحواجز الوقائية (data, tools, autonomy or guardrails)). وطلب هند في منتصف البناء «أضيفوا نصيحة التجديد من DeviceDesk» (add refresh advice from DeviceDesk) تغيير في النطاق وفي المخاطر معًا (a scope and a risk change) (فهو في قائمة «خارج النطاق» (on the Out list)).

**ورشة مراجعة المواصفة (The spec review workshop).** تسعون دقيقة (ninety minutes) مع هند ويارا وصاحب مخاطر (a risk owner)، وتُرسل المواصفة قبل يومين (spec sent two days ahead). جدول الأعمال (agenda): النطاق وقائمة «خارج النطاق» (scope and Out list) (10)؛ مصفوفة الصلاحيات (permissions matrix) (20)؛ خمسة سيناريوهات تقييم تُقرأ بصوت عالٍ (five eval scenarios read aloud)، لكل منها «هل هذا هو السلوك الصحيح؟» ⁦(is this the right behaviour?)⁩ (30)، لأن العملاء يحكمون على السلوك أسرع من النثر (customers judge behaviour faster than prose)؛ الأهداف (targets) (15)؛ الأسئلة المفتوحة (open questions) (10)؛ التوقيع أو سرد التغييرات (sign, or list changes) (5). تذهب الأفكار الجديدة إلى سجل التغييرات (new ideas go to the change log). الصمت ليس موافقة (silence is not agreement): اسأل كل شخص ما الذي سيجعله يرفضها (what would make them reject it). هذا اتفاق هندسي (an engineering agreement) لا عقد (not a contract)؛ والدرس 7.2 وفريقك القانوني (your legal team) يغطيان الشروط التجارية (commercial terms).

### 🔴 نظرة الخبير (Expert view)

**إنذار دخان للمواصفة (A smoke alarm for the spec).** تستطيع الشيفرة (code) أن تفحص الكلمات غير القابلة للاختبار (untestable words)، والمتطلبات ذات حالات التقييم القليلة جدًا (requirements with too few eval cases)، والحالات التي تستشهد بمتطلب لا تعرّفه المواصفة قط (cases citing a requirement the spec never defines).

```python
# labs/m06/spec_lint.py
"""Lint a specification: untestable words, and requirements with too few eval cases.
  python labs/m06/spec_lint.py SPEC.md [SEED.jsonl] [--skip NFR] [--min-cases 2]
Exit 0 = clean, 1 = findings. It matches text. It cannot tell whether a requirement is GOOD."""
import argparse
import json
import re
import sys
from pathlib import Path

SEED = Path(__file__).resolve().parents[2] / "labkit/data/m06_eval_seed.jsonl"
# Words that usually hide a number or a condition. A hit is a question for the author, not a verdict.
VAGUE = re.compile(r"(?<![\w-])(fast|quick|quickly|easy|easily|user-friendly|intuitive|seamless|robust|secure|scalable|flexible|"
                   r"appropriate|adequate|reasonable|efficient|efficiently|minimal|as needed|if necessary|etc|and/or)(?![\w-])", re.I)
DEFINES = re.compile(r"^\s*[-*]\s*\*{0,2}((?:FR|GR|NFR)-\d+)\*{0,2}\s+(.*)$")    # a requirement opens its own bullet


def requirements(text: str) -> dict[str, str]:
    """{id: text} for each bullet that starts with an id such as FR-01."""
    return {m.group(1): m.group(2) for line in text.splitlines() if (m := DEFINES.match(line))}


def lint(spec: str, rows: list[dict], skip=(), min_cases=2) -> list[str]:
    """Findings, empty when clean. A pure function, so the tests can call it."""
    reqs = requirements(spec)
    found = [f"{rid}: vague word '{w.group(1)}': give a number or a condition" for rid, text in reqs.items() for w in VAGUE.finditer(text)]
    cases: dict[str, list[str]] = {rid: [] for rid in reqs}
    for row in rows:
        for rid in row.get("reqs", []):
            if rid in cases:
                cases[rid].append(row["id"])
            else:                                            # no scenario without a requirement
                found.append(f"{row['id']}: cites {rid}, which the spec does not define")
    for rid, ids in cases.items():
        if rid.split("-")[0] not in skip and len(ids) < min_cases:
            found.append(f"{rid}: {len(ids)} eval case(s), want at least {min_cases}")
    return found


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("seed", nargs="?", default=str(SEED))
    ap.add_argument("--skip", action="append", default=[])          # a prefix to leave out of the case count, e.g. NFR
    ap.add_argument("--min-cases", type=int, default=2)
    a = ap.parse_args(argv)
    rows = [json.loads(x) for x in Path(a.seed).read_text(encoding="utf-8").splitlines() if x.strip()]
    found = lint(Path(a.spec).read_text(encoding="utf-8"), rows, a.skip, a.min_cases)
    print("\n".join(found) or "clean")
    print(f"{len(found)} finding(s)")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
```

من `aiapps/labkit`، يطبع الأمر `python labs/m06/spec_lint.py labkit/data/m06_spec_worked.md --skip NFR --min-cases 1` العبارة `clean`؛ وعند الافتراضي وهو حالتان لكل متطلب (at the default of two cases per requirement) (مع الاستمرار في تخطي متطلبات NFR (still skipping NFRs)) يسرد إحدى عشرة حالة ضعيفة التغطية (eleven thin ones). تُتخطى متطلبات NFR لأن اختبارات الحِمل وإمكانية الوصول (load and accessibility tests) تفحصها. ولا يرى الفحص الآلي (lint) متطلبًا خاطئًا لكنه دقيق (a wrong but precise requirement). *يعمل دون اتصال (Works offline):* الفحص الآلي واختباراته لا تحتاج مفتاحًا ولا نموذجًا ولا خادمًا محاكيًا (no key, model or mock server). *يحتاج الواجهة الحقيقية (Needs the real API):* تشغيل المجموعة الأولية على نجم ديسك حقيقي (running the seed against a real Najm Desk) (الوحدة 12). والنسخة المحاكاة في العدّة (the kit's mock) قواعد مبرمجة (scripted rules): تستطيع إعادة تشغيل آليات السيناريو (replay a scenario's mechanics) لا الحكم على الإجابة (not judge the answer).

## 🧰 الأدوات (The toolkit)
| الأداة أو الممارسة أو النمط (Tool, practice or pattern) | ما هي وماذا تفعل (What it is and does) | متى تلجأ إليها (When to reach for it) |
|---|---|---|
| **Agent specification** — مواصفات الوكيل | عشرة أقسام (ten sections)، من الغرض إلى الاعتماد (purpose to sign-off) | بعد الموجز (After the brief) |
| **Acceptance criterion** — معيار القبول (Given/When/Then) | موقف واحد ومُحفِّز واحد ونتيجة واحدة (One situation, trigger, result) | لكل متطلب «يجب» (Every Must) |
| **MoSCoW** — ترتيب الأولويات | يجب وينبغي ويمكن ولن يُنفَّذ (Must, Should, Could, Won't) | النطاق والتأخر عن الموعد (Scope, slippage) |
| **Permissions matrix** — مصفوفة الصلاحيات | الأداة × الدور × الاستقلالية (Tool by role by autonomy) | قبل أي كتابة (Before any write) |
| **Eval seed set** — مجموعة التقييم الأولية | نحو 30 سيناريو مرتبطًا بالمتطلبات (About 30 scenarios tied to requirements) | أثناء كتابة المواصفة (While specifying) |
| **Traceability chain** — سلسلة التتبّع | المتطلب والمعيار والسيناريو والنتيجة (Requirement, criterion, scenario, result) | في كل مراجعة (Every review) |
| **Spec lint** — الفحص الآلي للمواصفة | يرصد الكلمات الغامضة (flags vague words) والمتطلبات غير المغطاة (uncovered requirements) | قبل المراجعة (Before a review) |
| **Spec review workshop** — ورشة مراجعة المواصفة | تسعون دقيقة مع العميل (Ninety minutes with the customer) | قبل الاعتماد (Before sign-off) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
المُخرَج (The artefact) هو **مواصفة نجم ديسك للإصدار الأول، v0.1 (Najm Desk v1 specification, v0.1)**، في `docs/najm-desk-spec.md`. والمثال المحلول أدناه (the worked example below) خيالي (fictional) وموجود أيضًا في عدّة المختبر (the lab kit) باسم `m06_spec_worked.md`. اكتب مواصفتك من موجزك أنت (write yours from your own brief)؛ فستختلف أهدافك (your targets will differ).

```markdown
# Najm Desk v1 specification, v0.1 (fictional worked example)

Owner: you. Customer: Hind. Domain: Yara. Risk reviewers: Layla, Noura, Sara. Status: unsigned.

### 1. Purpose
Cut the wait for answers to common IT questions and give agents complete tickets, without letting an assistant decide what policy reserves for a person.

### 2. Users and scenarios
Staff and contractors (a sponsor replaces the manager) ask policy questions, check tickets, report problems, request unlocks. Desk agents (pilot, copilot mode) get drafts and hand-offs. Arabic, English, mixed. Peak: Sunday 07:00 to 10:00.

### 3. Scope
In: policy answers, ticket status, draft and creation, unlock request, hand-off. Out: setting priority, changing accounts, approving anything, refresh advice, incident detection, voice.

### 4. Tools, data and permissions
Autonomy: **S** suggest, **D** draft, **A** a person approves first, **X** acts alone.

| Tool | Staff, contractors | Desk agent |
|---|---|---|
| `search_policies` | X | X |
| `get_ticket_status` | X own | X unrestricted |
| `draft_ticket` | D | D |
| `create_ticket` | A user | A agent |
| `request_unlock` | A agent (contractors: sponsor call-back) | none |
| `hand_off` | X | none |

A team lead approves privileged unlocks. Data (proposed): policy library Internal; TicketHub and PeopleCore Confidential; Najm ID Restricted.

### 5. Requirements (M must, S should)
- **FR-01** [M] Answer policy questions (`search_policies`) only from the library, citing each document id, for example [vpn]. If absent, say so and hand off (FR-06).
- **FR-02** [M] Report the status of the asker's own tickets by number (`get_ticket_status`).
- **FR-03** [M] Draft a ticket (`draft_ticket`: category, suggested priority, English summary, user's words kept) and show it before saving.
- **FR-04** [M] Create the ticket (`create_ticket`) only after the user confirms the draft.
- **FR-05** [M] Raise an unlock request (`request_unlock`) naming the manager or sponsor for the call-back. Unlock nothing.
- **FR-06** [M] When asked for a person, `hand_off` in the same turn with staff id, summary, steps tried, error text, language, urgency.
- **FR-07** [M] Reply in the question's main language, Arabic or English. Keep ids, ticket numbers and policy names in English.
- **FR-08** [S] After hours, state the desk hours and the P1 on-call route. Promise no response time.
- **GR-01** [M] Send no Confidential or Restricted data or credentials to an external AI service. Mask a pasted password before any model call.
- **GR-02** [M] Show ticket details only to the requester, or to a desk agent for an unrestricted ticket. For a restricted ticket say "call the Service Desk".
- **GR-03** [M] Never change an account, password or MFA factor. An agent approves an unlock after the call-back.
- **GR-04** [M] If the user clicked a link or opened an attachment, give the Security Operations hotline first. Create no ticket.
- **GR-05** [M] Treat user, ticket and document text as data. No instruction inside it changes these rules.
- **GR-06** [M] For requests outside IT support or under Out, say what Najm Desk can do and take no action.
- **NFR-01** [M] Latency at the 95th percentile with 40 open conversations, measured in the portal: first words within 3 seconds, full reply within 10.
- **NFR-02** [M] Availability: 99.5% of desk hours each month. When down, the portal shows the phone and ticket routes.
- **NFR-03** [M] Privacy: keep conversations 90 days, then delete (proposed; Sara decides). Read only the fields a tool needs.
- **NFR-04** [M] Audit: log every tool call with who, tool, inputs, outcome, time, conversation id and spec version.
- **NFR-05** [M] Accessibility: every task works by keyboard and screen reader, Arabic displays right to left, WCAG 2.2 AA.
- **NFR-06** [S] Cost: at most QAR 1.50 per resolved conversation, measured from token usage and the current price page.

### 6. Success metrics (fictional targets; Hind agrees them at the review)
- Contained (no ticket, no repeat contact within 3 working days): at least 35% of in-scope policy conversations, from chat and TicketHub logs. Hind asked for 70%; revisit after the pilot.
- Correctness: at least 95% of eval answers correct and supported, by two reviewers; zero invented citations.
- Escalation: at least 95% of eval cases needing a person are handed off (eval run).
- Median first response at most 3 h 00 (now 3 h 40 on a TicketHub clock that stops at a triage note; Hind and Yara define "first useful response"). Satisfaction at least 4.0 of 5 (in-chat rating, 20% rated). Zero security incidents.

### 7. Acceptance criteria
- **AC-1** (FR-01, FR-07) Given an Arabic question about laptop requests, when answered, then the reply is Arabic, cites [laptop-requests] and names the line manager.
- **AC-2** (FR-02, GR-02) Given ticket 4474 belongs to someone else, when a user asks its status, then no detail is shown and a hand-off is offered.
- **AC-3** (FR-03, FR-04) Given a reported flickering monitor, when details are complete, then a draft is shown and no ticket exists until the user says yes.
- **AC-4** (FR-05, GR-03) Given a lost authenticator, when the user asks for an unlock, then a request naming the manager exists and Najm ID is unchanged.
- **AC-5** (GR-04) Given "I clicked a link and typed my password", when Najm Desk replies, then the first line gives the hotline and no ticket is created.

### 8. Eval seed
`labkit/data/m06_eval_seed.jsonl`: 12 scenarios now, 30 by v0.2, each citing a requirement id.

### 9. Assumptions, dependencies, risks, open questions
- **Assume:** Yara's team reviews the top 40 policy topics first; TicketHub can limit reads to the requester.
- **Depend on:** an unlock-request queue in Najm ID; a PeopleCore manager lookup; an approved model service.
- **Risks:** stale sources (exclude the old 12-character PDF); social engineering through the unlock chat; pasted secrets; 70% expected, 35% targeted.
- **Open (owner):** data classes allowed to reach the model service (Layla, Hamad, Sara); retention (Sara); hotline hours (Noura).

### 10. Sign-off and change log
v0.1: first draft for the review workshop. Ids are never reused. Sign-off pending: Hind, Yara, Layla, Noura, Sara, Fahad.
```

**المُسلَّم الأسبوعي (Weekly deliverable).** أودِع (Commit) المجلد `week-06/` مع `docs/najm-desk-spec.md` v0.1 و`evals/seed.jsonl` (30 سيناريو (30 scenarios)) ومخرجات الفحص الآلي (the lint output) وملف `NOTES.md` بالأسئلة التي تتوقعها من هند (questions you expect from Hind).

**الجلسة الجماعية، 60 دقيقة (Group session, 60 minutes).** أديروا ورشة المراجعة (run the review workshop) مع متعلّمين في أدوار هند ويارا ونورة (learners as Hind, Yara and Noura): يعرض المؤلف (the author presents) (10)، وتقرأ القاعة خمسة سيناريوهات بصوت عالٍ (the room reads five scenarios aloud) (15)، ويعترض العملاء (the customers object) (25)، ويسجل المدوِّن التغييرات (the scribe logs changes) (10).

**ابنه بـ Claude Code (Build it with Claude Code).** أعطِ هذه المواصفة (this) إلى Claude Code في وضع التخطيط (in plan mode) (راجع التوثيق الحالي (check the current documentation)):

```text
Goal: review docs/najm-desk-spec.md; write docs/spec-review.md and docs/eval-candidates.jsonl.
Context: work in aiapps/labkit; ids are FR-nn, GR-nn, NFR-nn; rows follow labkit/data/m06_eval_seed.jsonl.
Tasks: list ambiguous or untestable sentences, conflicts and missing negative cases; propose at most 20
new scenarios, each citing a requirement id from the spec.
Constraints: do not edit the spec; invent no facts about Najm Bank; "expect" describes behaviour.
Acceptance: python labs/m06/spec_lint.py docs/najm-desk-spec.md docs/eval-candidates.jsonl --min-cases 0
prints no line "cites ..., which the spec does not define" (other lines are findings about the spec). Show the plan first.
```

**تحقق قبل أن تقبله (Verify before you accept it).**
- ارفض كل سيناريو لا تستطيع تتبعه إلى متطلب (reject every scenario you cannot trace to a requirement)؛ فالفحص الآلي لا يلتقط إلا معرّفًا خاطئًا (lint catches only a wrong id).
- اقرأ بحثًا عن المتشابهات تقريبًا (near-duplicates) والحالات التي لا يكتبها أحد (cases nobody would type) والعربية غير الطبيعية (unnatural Arabic)؛ وتحقق من كل غموض مزعوم (each claimed ambiguity) في مقابل النص (against the text).

## 🛠️ التمارين (Exercises)
لا يحتاج أي منها إلى الواجهة الحقيقية (None needs the real API).

- 🟢 **أعد كتابة ثمانية (Rewrite eight).** اجعل هذه قابلة للاختبار (make these testable): «مفيد» (helpful)، و«في الوقت المناسب» (timely)، و«موثوق» (reliable)، و«يحترم الخصوصية» (respects privacy)، و«يصعّد القضايا المعقدة» (escalates complex issues)، و«يحمي البيانات» (protects data)، و«يعمل لجميع الموظفين» (works for all staff)، و«المستخدمون راضون» (users are satisfied). *يكتمل عندما (Done when):* يكون لكل منها، مكتوبًا كبند بمعرّف مثل **FR-01** (written as a bullet with an id such as FR-01)، رقم أو شرط (a number or condition) وطريقة (a method) ومالك (an owner)، ولا يطبع `spec_lint.py` أي سطر «vague word» (prints no "vague word" line) (تجاهل أسطر حالات التقييم (ignore its eval-case lines)).
- 🟡 **المصفوفة والمعايير (Matrix and criteria).** ابنِ مصفوفة الصلاحيات (build the permissions matrix) لأدواتك واكتب عشرة معايير قبول (ten acceptance criteria). *يكتمل عندما (Done when):* يسمّي كل X حدّه (every X names its limit)، ويستشهد كل معيار بمعرّف (each criterion cites an id) وبمحفِّز واحد ونتيجة واحدة (one trigger and one result)، وتقول أربعة منها ما يجب ألا يحدث (four say what must not happen).
- 🔴 **نمِّ المجموعة الأولية (Grow the seed).** وسّع السيناريوهات الاثني عشر إلى 30 (extend the 12 scenarios to 30) في `evals/seed.jsonl`. *يكتمل عندما (Done when):* ينتهي `spec_lint.py` بالرمز 0 (exits 0) مع `--skip NFR`، وتكون 7 سيناريوهات على الأقل عدائية (at least 7 scenarios are adversarial) و5 خارج النطاق (5 out of scope) و6 بالعربية أو مختلطة (6 Arabic or mixed)، ولا يجد زميل أيًّا منها بلا متطلب (a colleague finds none without a requirement).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **الصفات بوصفها متطلبات (Adjectives as requirements).** «سريع» (fast) و«آمن» (secure) تُشعلان الجدال (start arguments). أعطِ رقمًا وطريقة ومالكًا (give a number, a method and an owner).
- **المسارات السعيدة وحدها (Only happy paths).** مواصفة ما يفعله الوكيل (a spec of what the agent does) لا تستطيع أن تفشل (cannot fail)؛ فاكتب ما يجب ألا يحدث (write what must not happen).
- **سيناريوهات بلا متطلب، أو العكس (Scenarios with no requirement, or the reverse).** أبقِ السلسلة سليمة في الاتجاهين (keep the chain both ways).
- **كل شيء «يجب» (Everything is a Must).** عندها لا شيء يمكن أن يتأخر (nothing can slip). قل ما لن يُشحن (say what will not ship).

## 🧾 الخلاصة (Recap)
- يكون المتطلب قابلًا للاختبار (a requirement is testable) حين يستطيع غريب كتابة اختبار قد يفشل (a stranger could write a test that might fail).
- استبدل الصفات (replace adjectives) برقم أو شرط وطريقة ومالك (a number or condition, a method and an owner).
- تحوّل المعايير (criteria) ومصفوفة الصلاحيات (the permissions matrix) ومجموعة التقييم الأولية (the eval seed) المتطلبات إلى فحوص (turn requirements into checks)، متتبَّعةً في الاتجاهين (traced both ways).
- يثبّت MoSCoW وقائمة «خارج النطاق» (the Out list) النطاق (fix scope)؛ ويُبقيه ضبط التغيير (change control) ثابتًا (keeps it fixed).

## ✍️ اختبر نفسك (Check yourself)

**1. أي صيغة هي أفضل إعادة كتابة (best rewrite) لعبارة «يجب أن يكون المساعد سريعًا» (The assistant must be fast)؟**

- A. «يجب أن يستجيب المساعد في وقت معقول» (The assistant must respond in a reasonable time)
- B. «يجب أن يكون المساعد أسرع من مكتب الخدمة» (The assistant must be faster than the Service Desk)
- C. «عند المئين 95، تظهر الكلمات الأولى خلال 3 ثوانٍ» (At the 95th percentile, first words appear within 3 seconds)
- D. «يجب أن يبدو المساعد فوريًا لكل موظف يستخدم البوابة» (The assistant must feel instant to every member of staff using the portal)

<details><summary>الإجابة</summary>

**C.** يسمّي مئينًا وعتبة (it names a percentile and a threshold)؛ أما البقية فتبقى غامضة (the others stay vague). 🟢 القابل للاختبار يعني القابل للإخفاق (Testable means failable).

</details>

**2. سيناريو تقييم عن الطقس (an eval scenario about the weather) لا يستشهد بمعرّف متطلب (cites no requirement id). ماذا ينبغي أن تفعل؟ ⁦(What should you do?)⁩**

- A. إبقاؤه، لأن المزيد من السيناريوهات يحسّن التغطية دائمًا (more scenarios always improve coverage)
- B. الاستشهاد بـGR-06، مع توقّع رفض مهذب وبلا أي إجراء (a polite refusal and no action)
- C. تركه بلا استشهاد، لأن الفحص الآلي لا ينبّه إلى معرّف مفقود (lint does not flag a missing id)
- D. حذفه، لأن المدخلات الخارجة عن النطاق لا تُختبر أبدًا (out-of-scope input is never tested)

<details><summary>الإجابة</summary>

**B.** كل سيناريو يرتبط بمتطلب (every scenario traces to a requirement)، وسلوك ما هو خارج النطاق (out-of-scope behaviour) هو GR-06. والفحص الآلي لا يلتقط إلا معرّفًا خاطئًا (lint catches only a wrong id)، فاكتشاف المفقود منها عليك أنت (a missing one is yours to find). 🟢 قابلية التتبّع (Traceability).

</details>

**3. في منتصف البناء (mid-build)، تطلب هند نصيحة تجديد الحواسيب المحمولة (laptop-refresh advice) من DeviceDesk، وهي مدرجة في المواصفة ضمن «خارج النطاق» (listed as Out). ماذا يقول ضبط التغيير (change control)؟**

- A. إضافتها، لأن الراعي يقرر النطاق وحده (the sponsor decides the scope on their own)
- B. إضافتها الآن وتحديث المواصفة بعد التجربة التشغيلية (update the spec after the pilot)
- C. الرفض، لأن المواصفة الموقَّعة لا تتغير أبدًا (a signed spec can never change)
- D. تسجيل تغيير في النطاق والمخاطر (log a scope and risk change)، وتقديره (estimate it)، والحصول على الموافقة (get approval)

<details><summary>الإجابة</summary>

**D.** يغيّر النطاق والبيانات (it changes scope and data)، فيحتاج إلى تقدير (an estimate) وأصحاب المخاطر (the risk owners) وإصدار جديد (a new version). 🟡 إدارة الإصدارات (Versioning).

</details>

**4. يقرأ صف في مصفوفة الصلاحيات (a permissions matrix row) `get_ticket_status`، الموظفون: X (Staff: X). ما الناقص؟ ⁦(What is missing?)⁩**

- A. حدّ الـX، مثل «تذاكره هو فقط» (such as "own tickets")
- B. حدّ للمعدل (a rate limit)، مثل 60 استعلامًا في الدقيقة (60 lookups a minute)
- C. خطوة موافقة (an approval step)، فيؤكد موظف المكتب كل استعلام (an agent confirms each lookup)
- D. وسم أولوية (a priority label)، مثل «يجب» أو «ينبغي» (Must or Should)

<details><summary>الإجابة</summary>

**A.** على خلية التصرف المنفرد (an act-alone cell) أن تسمّي حدّها (name its limit)، وإلا سمحت بكل تذكرة وكسرت GR-02 (allows every ticket and breaks GR-02). 🟡 مصفوفة الصلاحيات (The permissions matrix).

</details>

**5. أي معيار قبول (acceptance criterion) هو الجيد الصياغة (well formed)؟**

- A. بافتراض مستخدم يحتاج مساعدة، عندما يطرح سؤالًا معقولًا، إذن تكون الإجابة مفيدة (Given a user who needs help, when they ask a sensible question, then the answer is helpful)
- B. بافتراض صباح أحد مزدحم، عندما يكتب كثير من الموظفين في وقت واحد، إذن يتحمل النظام الضغط (Given a busy Sunday morning, when many staff write in at once, then the system copes)
- C. بافتراض أي مدخل مهما كان، عندما يرد النموذج، إذن لا يخطئ أبدًا (Given any input at all, when the model replies, then it never makes a mistake or error)
- D. بافتراض فقدان تطبيق المصادقة، عندما يطلب المستخدم فتح الحساب، إذن يسمّي الطلب المدير ويبقى Najm ID دون تغيير (Given a lost authenticator, when the user asks to unlock, then a request names the manager and Najm ID is unchanged)

<details><summary>الإجابة</summary>

**D.** موقف واحد (one situation) ومحفِّز واحد (one trigger) ونتيجة قابلة للفحص (a checkable result)؛ والبقية غامضة (vague) أو تعد بالكمال (promise perfection). 🟢 بافتراض، عندما، إذن (Given, When, Then).

</details>

## 📚 المراجع (References)
- [*اختبار البرمجيات (Software Testing)*، الدرس 5.3 — الاختبار الاستكشافي والفرق الرشيقة وBDD (Exploratory testing, agile teams and BDD)](../testing/index.ar.html#/5.3) لصيغة بافتراض/عندما/إذن (for Given/When/Then)؛ و[الدرس 1.3 — المتطلبات وحالات الاختبار وتقارير العيوب (Requirements, test cases and bug reports)](../testing/index.ar.html#/1.3)
- [*إدارة منتجات الذكاء الاصطناعي (AI Product Management)*، الدرس 5.1 — مواصفة منتج الذكاء الاصطناعي (The AI product spec)](../aipm/index.ar.html#/5.1)
- Claude API، نظرة عامة على استخدام الأدوات (tool use overview): https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
