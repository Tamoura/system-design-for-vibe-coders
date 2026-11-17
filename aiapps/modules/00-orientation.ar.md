# الوحدة 0 — التوجيه (Orientation): دورة حياة التسليم ومختبرك وشريكك في البناء

*يستطيع أي شخص أن يجعل وكيلًا (agent) يجيب عن سؤال في عرض تجريبي (demo). أما إطلاق وكيل يعتمد عليه بنك فهو عمل مختلف، وتُريك هذه الوحدة ماهيّته. يمنحك الدرس 0.1 الخريطة: دورة حياة التسليم ذات المراحل الثماني، وعشر خصائص (ten properties) تجعل الوكيل «بمستوى المؤسسات» ("enterprise-grade")، والطبقات الخمس للدورة (five layers)، وروتين مجموعة القراءة (reading-group routine)، وكل ذلك على مشروع نجم ديسك الخيالي. ويبني الدرس 0.2 مختبرك (lab): لغة Python، وحزمة التطوير المثبَّتة (pinned SDK)، والمحاكي دون اتصال (offline mock) في عدّة المختبر (lab kit)، ومفتاح الواجهة البرمجية (API key)، وسقف الإنفاق (spending cap)، وسكربت الفحص السريع (smoke script) الذي يخبرك في أي وضع (mode) أنت. ويعلّمك الدرس 0.3 كيف توجّه Claude Code شريكًا لك في البناء (build partner) بمواصفة (spec) وخطة (plan) وخطوات صغيرة (small steps) وقائمة فحص للمراجِع (reviewer's checklist)، حتى تفهم كل ما يبنيه قبل أن تطلقه (ship).*

> **الطبقة (Layer):** Delivery — كيف يسافر الوكيل من أول محادثة مع العميل (customer) إلى منتج يعمل ويمكن دعمه، إضافةً إلى المختبر وشريك البناء اللذين ستستخدمهما في الطريق.

---

# 0.1 — ما الذي يلزم لإطلاق وكيل بمستوى المؤسسات: دورة حياة التسليم والطبقات وكيف تعمل الدورة
*المستوى (Level): 🟢 مبتدئ (Beginner)* · *المتطلبات (Prerequisites): لا يوجد (none)* · *الطبقة: Delivery*

## ⚡ الدرس في دقيقة (In 60 seconds)
- إطلاق الوكيل **دورة حياة (lifecycle)** وليس عملية بناء (build) فحسب: استكشف (discover)، وصمّم (design)، وابنِ، وقيّم (evaluate)، وأمّن (secure)، وأطلق، وشغّل (operate)، وسلّم (hand over).
- معنى **بمستوى المؤسسات (enterprise-grade)** هو عشر خصائص تستطيع أن تقدّم دليلًا (evidence) عليها، مثل أن يكون الوكيل موثوقًا (reliable) وخاضعًا للحوكمة (governed) وقابلًا للدعم (supportable). عبارة «نحن حريصون» ليست دليلًا.
- **روبوت الدردشة (chatbot)** يجيب، و**سير العمل (workflow)** يتبع مسارًا تحدّده شيفرتك، و**الوكيل (agent)** يختار خطواته بنفسه. استخدم أبسط خيار ينجح.
- كثيرًا ما تتعثّر التجارب التشغيلية (pilots) بعد مرحلة البناء، لأن العرض التجريبي لا يثبت إلا النصف الأول.
- الدورة مجموعة قراءة (reading group)، بمعدل وحدة أسبوعيًا، على مشروع عميل **خيالي** (fictional engagement) هو نجم ديسك (Najm Desk). وتعمل المختبرات (labs) دون اتصال (offline)، كما تعمل دون أي تغيير على الواجهة البرمجية الحقيقية (real API).
- يكتب Claude Code جزءًا كبيرًا من شيفرتك؛ ومع ذلك يجب أن تشرح كل سطر يُطلَق.

## 🧭 لماذا يهم
تخيّل تجربة تشغيلية (pilot) في بنك نجم (Najm Bank) لم تصل قط إلى مستخدميها. (القصة افتراضية (hypothetical)، مثل كل قصص نجم.) بنى فريق صغير **اسأل الموارد البشرية (Ask HR)**، وهو روبوت دردشة يعمل على سياسات الموارد البشرية (HR policies)، وبعد ستة أسابيع صفّقت اللجنة التوجيهية (steering committee) للعرض التجريبي. ثم اصطدم المشروع بالنصف الثاني من دورة الحياة. فسألت **سارة (Sara)**، مسؤولة حماية البيانات (Data Protection Officer)، عن بيانات الموظفين التي ترسلها الموجّهات (prompts) إلى مزوّد النموذج (model provider). لم يعرف أحد. وطلبت **ليلى (Layla)** تقييم المخاطر (risk assessment). ولم يكن هناك تقييم. وسأل فريق **حمد (Hamad)** عمّا يمنع مستندًا ملصقًا (pasted document) من إعطاء الروبوت تعليمات جديدة (حقن الموجّه (prompt injection)، الوحدة 13). وسألت **مها (Maha)** عمّن سيتلقى نداء التنبيه (paged)؛ فكان الجواب «المطوّر»، وقد انتقل إلى فريق آخر. وكان الموجّه (prompt) في خلية دفتر (notebook cell) ولا اختبارات له، فلم يجرؤ أحد على تعديله. وبعد أربعة أشهر أُوقفت التجربة التشغيلية. النموذج لم يفشل قط. الذي فشل هو التسليم (delivery).

وفق ما نُشر، قضت هيئة تحكيم (tribunal) في كولومبيا البريطانية (British Columbia) في قضية *Moffatt v. Air Canada* (2024) بأن شركة الطيران مسؤولة عن معلومات خاطئة قدّمها روبوت الدردشة في موقعها إلى أحد العملاء. هذا حكم واحد (one ruling) في ولاية قضائية واحدة (one jurisdiction)، لكن خطّط وكأن مؤسستك ستُسأل عمّا يقوله وكيلها، واسأل فريقك القانوني (legal team) مبكرًا. إن عبارة «يعمل في العرض التجريبي» هي بداية العمل.

## 📐 كيف يعمل

### 🟢 الأساسيات

**دورة حياة التسليم (The delivery lifecycle).** يمرّ مشروع الوكيل (agent project) بثماني مراحل (eight stages). تنتهي كل مرحلة بمُخرَج (artefact) تستطيع أن تسلّمه لشخص آخر، ولكل مرحلة موضع في هذه الدورة.

```mermaid
flowchart RL
    A["الاستكشاف<br/>الوحدة 6<br/>(Discover<br/>Module 6)"] --> B["التصميم<br/>الوحدة 7<br/>(Design<br/>Module 7)"]
    B --> C["البناء<br/>الوحدات 1 إلى 5 و8 إلى 11<br/>(Build<br/>Modules 1 to 5, 8 to 11)"]
    C --> D["التقييم<br/>الوحدة 12<br/>(Evaluate<br/>Module 12)"]
    D --> E["التأمين<br/>الوحدة 13<br/>(Secure<br/>Module 13)"]
    E --> F["الإطلاق<br/>الوحدة 14<br/>(Ship<br/>Module 14)"]
    F --> G["التشغيل<br/>الوحدة 15<br/>(Operate<br/>Module 15)"]
    G --> H["التسليم<br/>الوحدتان 15 و16<br/>(Hand over<br/>Modules 15 and 16)"]
    D -.->|"دون المستوى المطلوب (below the bar)"| C
    G -.->|"ما نتعلّمه (what we learn)"| A
```

| المرحلة (Stage) | السؤال الذي تجيب عنه | ما تسلّمه |
|---|---|---|
| **الاستكشاف (Discover)** | ما المشكلة الحقيقية (real problem)، وهل ينبغي أن يكون الحل وكيلًا؟ | موجز الوكيل (agent brief) |
| **التصميم (Design)** | ما الذي يجوز له فعله بمفرده، ومن يوافق (approves) على ماذا؟ | المعمارية (architecture) والنطاق المتفق عليه (agreed scope) |
| **البناء (Build)** | كيف يتكامل النموذج (model) والموجّهات والأدوات (tools) والحلقة (loop)؟ | وكيل يعمل |
| **التقييم (Evaluate)** | هل هو جيد بما يكفي، وهل سننتبه إذا توقف عن ذلك؟ | مجموعة التقييم (eval set) وبوابة التكامل المستمر (CI gate) |
| **التأمين (Secure)** | ما الذي قد يسوء، أو يمكن دفعه إلى السوء عمدًا، ومن يعتمد (signs off)؟ | نموذج التهديدات (threat model) والحواجز الوقائية (guardrails) واعتماد الحوكمة (governance sign-off) |
| **الإطلاق (Ship)** | كيف يصل إلى المستخدمين، وكيف نتراجع عنه (roll back)؟ | خط النشر (pipeline) وخطة الإصدار (release plan) والميزانية (budget) |
| **التشغيل (Operate)** | كيف نراه ونصلحه ونحسّنه؟ | لوحات المتابعة (dashboards) ودليل التشغيل (runbook) |
| **التسليم (Hand over)** | من يملكه غدًا؟ | التدريب (training) ونموذج الدعم (support model) والقبول (acceptance) |

تعلّمك الدورة لبنات البناء (building blocks) أولًا، لأنك لا تستطيع تحديد نطاق (scope) ما لا تستطيع بناءه؛ ثم تعود الوحدة 6 إلى الاستكشاف (discovery). ودورة الحياة أيضًا حلقة: فالتقييم الفاشل (failed evaluation) يعيدك إلى البناء، وما يعلّمك إياه التشغيل (operation) يغذّي الاستكشاف التالي.

**ماذا يعني «بمستوى المؤسسات» (What "enterprise-grade" means).** تبقى العبارة تسويقًا (marketing) حتى تحوّلها إلى أسئلة يستطيع المتشكّك (sceptic) طرحها. وهذه عشرة منها، لكل سؤال الدليل الذي يجيب عنه.

| الخاصية (Property) | سؤال المتشكّك | الدليل الذي تستطيع تقديمه (Evidence you can show) |
|---|---|---|
| **موثوق (Reliable)** | هل يتدبّر أمره حين تضطرب أداة (tool) أو الشبكة (network)؟ | المهلات (timeouts) وإعادة المحاولات المحدودة (capped retries) وحدود الحلقة (loop limits) |
| **آمن (Secure)** | هل يستطيع أحد دفعه إلى ما لا ينبغي أن يفعله؟ | نموذج التهديدات واختبارات الحقن (injection tests) |
| **خاضع للحوكمة (Governed)** | من وافق عليه، ومن يحق له تغييره؟ | تقييم المخاطر والاعتماد (sign-off) |
| **قابل للمراقبة (Observable)** | هل تستطيع أن ترى ما فعله ولماذا؟ | تتبّع (trace) لكل خطوة |
| **قابل للدعم (Supportable)** | من يتلقى مكالمة الثالثة فجرًا (3 a.m. call)، وماذا يفعل؟ | دليل التشغيل وجدول المناوبة (on-call rota) |
| **مضبوط التكلفة (Cost-controlled)** | كم تكلّف المحادثة، وما الذي يوقف التكلفة المنفلتة (runaway)؟ | التكلفة لكل طلب (per-request cost) والميزانيات (budgets) والسقوف (caps) |
| **مُختبَر (Tested)** | هل كسر التغيير (change) شيئًا؟ | اختبارات الوحدة (unit tests) ومجموعة التقييم وبوابة التكامل المستمر |
| **موثَّق (Documented)** | هل يستطيع القادم الجديد (newcomer) أو المدقّق (auditor) متابعته؟ | المواصفات (specification) وسجلات القرار (decision records) |
| **مقبول (Accepted)** | هل وافق العميل على أنه اكتمل؟ | معايير القبول الموقّعة |
| **قابل للتحسين (Improvable)** | هل يجعله الاستخدام الحقيقي أفضل؟ | ملاحظات (feedback) تتدفق إلى مجموعة التقييم |

ضعيف (Weak): «إنه بمستوى المؤسسات. نستخدم نموذجًا قويًا واختبرناه.» ⁦⁩ قوي (Strong): «هذه مجموعة التقييم، وفحص التكامل المستمر (CI check) الذي يمنع الإصدار (release) حين تنخفض الدرجة، ونتيجة الأسبوع الماضي، والإخفاق الذي أضفناه بعد التجربة التشغيلية.» ⁦⁩ الإجابة القوية مجموعة من المُخرَجات (artefacts) يستطيع شخص آخر فتحها. وتختلف أوزان الخصائص من عميل لآخر: فمساعد القراءة فقط (read-only copilot) يحتاج حوكمة (governance) أقل من وكيل يكتب في نظام التذاكر (ticket system).

**روبوت الدردشة وسير العمل والوكيل (Chatbot, workflow, agent).** هذه لمحة أولية؛ وتعلّم الوحدات 1 و5 و8 كلًّا منها كما ينبغي. **روبوت الدردشة (chatbot)** يجري استدعاءً واحدًا للنموذج في كل دور (turn)، ويعيد إرسال المحادثة (conversation) في كل مرة، ولا يملك أدوات.

أما **سير العمل (workflow)** فينظّم استدعاءات النموذج (model calls) والأدوات على مسار تحدّده شيفرتك؛ فهو قابل للتنبؤ (predictable) وقابل للاختبار (testable) وأرخص، ويحل جزءًا كبيرًا من المشكلات الحقيقية.

وأما **الوكيل (agent)** فيترك النموذج يوجّه عمليته بنفسه: يختار الأداة التالية (next tool)، ويقرأ النتيجة (result)، ويكرر حتى يقرر أنه أنجز. وهذه المرونة هي مصدر مخاطرته أيضًا، ولذا تحتاج الوكلاء إلى حدود وتتبّع (traces) وتقييمات (evals). ويتبع التمييز بين سير العمل والوكيل (workflow-versus-agent split) مقال Anthropic «Building effective agents»، الذي ينصح بالبحث عن أبسط ما ينجح؛ أما «روبوت الدردشة» ("chatbot") فتسمية خاصة بهذه الدورة.

### 🟡 التعمق أكثر (Going deeper)

**مثال تطبيقي: ربط «اسأل الموارد البشرية» بدورة الحياة (Worked example: map Ask HR onto the lifecycle).** سطر واحد لكل مرحلة: ما الذي حدث، وأي مُخرَج موجود.

| المرحلة | ما الذي حدث | المُخرَج |
|---|---|---|
| الاستكشاف والتصميم (Discover, Design) | «روبوت لأسئلة الموارد البشرية»؛ دون مقابلات؛ واختير الاسترجاع (retrieval) في اليوم الأول | لا شيء |
| البناء | دفتر (notebook) وإطار عمل (framework)؛ ويعمل جيدًا | الدفتر |
| التقييم | عشرة أسئلة جُرّبت يدويًا | لا شيء محفوظ (Nothing kept) |
| من التأمين إلى التسليم | لم تُناقَش؛ عرض من حاسوب محمول؛ بلا مالك | لا شيء |

كانت مرحلة البناء المرحلة الوحيدة التي لها مُخرَج مكتمل (finished artefact)، وهذا شكل مألوف للتجربة التشغيلية المتعثرة (stalled pilot). وتتكرر الأسباب: لم يحدّد أحد معنى النجاح (success)، فصارت المراجعات (reviews) آراء؛ ووصل أصحاب المخاطر (risk owners) متأخرين فاعترضوا عليه (vetoed it)؛ ولم يقِس شيء الجودة (quality)، فلم يستطع أحد تغيير أي شيء بأمان؛ ولم يملك أحد النظام العامل (running system) ولا فاتورته (bill). والدفاع الرخيص هو **التحليل الاستباقي للفشل (premortem)**: قبل أن تبدأ، اكتب لكل مرحلة «بعد ستة أشهر أُوقف هذا المشروع لأن…»، ثم خطّط ضد أرجح الإجابات.

**الطبقات (The layers).** يحمل كل درس وسمًا (tag) للطبقة التي يعمل عليها؛ وقد يحمل الدرس وسمين.

| الطبقة | ما الذي تغطيه | الوحدات (Modules) |
|---|---|---|
| **Model** (النموذج) | النموذج اللغوي الكبير (LLM) بوصفه دالة عديمة الحالة (stateless function): الرموز (tokens) والسياق (context) والواجهة البرمجية والموجّهات | 1–2 |
| **Applications** (التطبيقات) | المخرجات المهيكلة (structured output) والأدوات والاسترجاع وأنماط سير العمل (workflow patterns) | 3–5 |
| **Delivery** (التسليم) | العمل المواجه للعميل (customer-facing work): الاستكشاف والتصميم والنطاق والإصدار والتسليم (handover) | 6–7، والإطلاق الفعلي (go-live) في 14–16 |
| **Agents** (الوكلاء) | حلقة الوكيل (agent loop) والذاكرة (memory) وMCP وفرق تعدد الوكلاء (multi-agent teams) | 8–11 |
| **Production** (الإنتاج) | التقييم (evaluation) والأمن والحوكمة والنشر (deployment) والتكلفة (cost) والتشغيل | 12–15 |

**كيف تعمل الدورة (How the course works).** بحلول الوحدة 16 تكون قد أخذت نجم ديسك من المقابلة الأولى إلى الإطلاق الفعلي، بموجز (brief) ومواصفات وبوابة تقييم (eval gate) وحزمة حوكمة (governance pack) ودليل تشغيل وتسليم. وهي تناسب مجموعة قراءة مع مرشد (mentor)، بمعدل وحدة أسبوعيًا، أي سبعة عشر أسبوعًا (seventeen weeks)؛ ويستطيع القارئ المنفرد أن يمضي أسرع. لكل أسبوع ستة أجزاء (six parts): **الدرس (lesson)**؛ و**القراءة (read)**، وهي الفصل المطابق من أحد المصادر (فصل Grokking أولًا للنموذج الذهني (mental model)، ثم المصادر المجانية للشيفرة)؛ و**المختبر (lab)** الذي تشغّله وتوسّعه، دون اتصال أولًا، وقد صُمّم لينتهي في أمسية واحدة؛ و**نقطة التحقق (checkpoint)** من خمسة أسئلة؛ و**المُسلَّم (deliverable)**، وهو مجلد `week-NN/` يضم ملف `NOTES.md` في مستودعك الخاص؛ و**جلسة المجموعة (group session)** من عروض تجريبية (demos) وإخفاق واحد يُعرض مباشرة ونقاش. وتتناوب الأدوار أسبوعيًا: الميسِّر (facilitator)، وقائد العرض (demo lead)، والمتشكّك الذي يراجع مُسلَّمًا واحدًا مقابل الخصائص العشر، والمدوِّن (scribe).

**المصادر، وكيف تستخدمها دون نسخ (The sources, and using them without copying).** خمسة مصادر رئيسية وإضافة واحدة (add-on)؛ تربط الدورة بها ولا تعيد إنتاجها أبدًا. كتاب **Grokking AI Applications** هو الكتاب الوحيد المدفوع؛ وتذكر خطة الدورة (course plan) أن دروسه التطبيقية (tutorials) تستخدم Langflow وKNIME، فتعامل معها بوصفها عروضًا تجريبية. و**Agentic Design Patterns** (Antonio Gulli) مسودة مجانية (free draft)؛ وقد عدّت الخطة 21 نمطًا (21 patterns). و**AI Agents for Beginners** (من Microsoft) يقدّم دروسًا مصوّرة (illustrated lessons) مع مقاطع فيديو ودفاتر؛ وقد عدّت الخطة ثمانية عشر درسًا (eighteen) وأشارت إلى ترجمة عربية. ومقال Anthropic **Building effective agents** هو مصدر التمييز بين سير العمل والوكيل (workflow-versus-agent distinction). وكتاب **aie-book** لـChip Huyen هو الرفيق المجاني (free companion) لكتاب *AI Engineering*. أما الإضافة، وهي دورة **LangChain Academy** المجانية، فتخدم وحدة تعدد الوكلاء (multi-agent module) فقط. وأرقام الفصول والأعداد في الخطة تعود إلى مالك الدورة (course owner) ولم تُراجَع بصورة مستقلة (independently checked)؛ والمحتوى يتغير، فتحقق من كل صفحة. دوّن ملاحظاتك بكلماتك الخاصة، وأضف سطرًا بعنوان «ما الذي كنت سأعترض عليه» ("what I would challenge")، واذكر المصدر والفصل في `NOTES.md`، ولا تلصق نصوصهم أو شيفرتهم في مستودعك أبدًا.

**تقلّب الأطر (Framework churn).** وقت كتابة الدرس، تستخدم دروس Microsoft إطار الوكلاء (agent framework) الخاص بها، وتستخدم شيفرة Gulli كلًّا من LangChain وCrewAI وGoogle ADK، وتستخدم المختبرات هنا حزمة Anthropic SDK الخام. وهذا مقصود: فالمطوّر الذي قابل نمطًا واحدًا بثلاث صيغ برمجية (three syntaxes) تعلّم النمط (pattern) لا المكتبة (library). حزمة SDK الخام أولًا، ولا معيار موحّد للمجموعة قبل صندوق المقارنة (comparison box) في الوحدة 11.

**كيف تعمل المختبرات (How the labs run).** يعمل كل مختبر بوضعين (two modes) وبشيفرة متطابقة. المحاكي (mock) **دون اتصال (offline)** مجاني ومبرمج مسبقًا (scripted)، فيناسب الآليات (mechanics): الرسائل (messages) ونتائج الأدوات (tool results) والحلقات (loops) والأخطاء (errors) ونمو الرموز (token growth). أما **الواجهة البرمجية الحقيقية (real API)** فتُحاسَب لكل رمز وتعطيك نموذجًا حقيقيًا، وتحتاج إليه لجودة الموجّهات (prompt quality) والاسترجاع والسلامة (safety) وأعداد الرموز الحقيقية. وتبدّل بينهما بتوجيه `ANTHROPIC_BASE_URL` إلى المحاكي أو بإلغاء ضبطه (unsetting it). ويبني الدرس 0.2 الإعداد.

### 🔴 نظرة الخبير (Expert view)

**مستوى المؤسسات تفاوض لا درجة (Enterprise-grade is a negotiation, not a score).** تتجاذب الخصائص فيما بينها: فمزيد من الحواجز الوقائية يضيف زمن استجابة (latency) وتكلفة، ومزيد من الاستقلالية (autonomy) يتطلب مزيدًا من الحوكمة، ومزيد من التسجيل (logging) يصطدم بالخصوصية. اسأل بدلًا من ذلك: «كم من الدليل تحتاج هذه الميزة؟» ⁦⁩ يعتمد الجواب على **مستوى الاستقلالية (autonomy level)**: أن يقترح (suggest)، أو يصوغ مسودة (draft)، أو يقرّر بموافقة (decide with approval)، أو يتصرف (act). يقترح نجم ديسك v1 (Najm Desk v1) ويصوغ المسودات في الغالب، فيحتاج دليلًا أقل من طلب إلغاء قفل الحساب المقيّد بالموافقة، ويقع تغيير الحساب المستقل بالكامل خارج الإصدار v1 لأن معياره (bar) سيكون أعلى بكثير.

**متى لا تبني وكيلًا (When not to build an agent).** إن كانت العملية مستقرة وقائمة على قواعد، فاكتب شيفرة عادية. وإن كان سير العمل يؤدي المهمة، فلا تضف حلقة. وإن لم تستطع أن تقول كيف يبدو «الصحيح» ("correct")، فلا تستطيع تقييمه، وبالتالي لا تستطيع إطلاقه. وإن كان الإجراء الخاطئ جسيمًا ولا رجعة فيه، فأبقِ إنسانًا هو من يقرّر.

**ما الذي يغيّره Claude Code (What Claude Code changes).** يسرّع مرحلة البناء (build stage) ولا يفعل إلا القليل للاستكشاف والقبول والملكية (ownership)، وهي أمور تحتاج إلى محادثات مع الناس. فالشيفرة تصل الآن أسرع مما تستطيع قراءته، فيصبح التحقق (verification) هو عنق الزجاجة (bottleneck): الدرس 0.3.

## 🧰 الأدوات
| الأداة أو الممارسة أو النمط (Tool, practice or pattern) | ما هي وماذا تفعل | متى تلجأ إليها |
|---|---|---|
| **Delivery lifecycle** — دورة حياة التسليم | ثماني مراحل، لكل منها مُخرَج | عند الانطلاق، وفي المراجعات لاكتشاف المرحلة المفقودة (missing stage) |
| **Enterprise-grade checklist** — قائمة فحص مستوى المؤسسات | عشر خصائص، لكل منها سؤال (question) ودليل | قبل الاتفاق على النطاق وقبل الإطلاق الفعلي |
| **Premortem** (Gary Klein) — التحليل الاستباقي للفشل | تخيّل أن المشروع فشل واكتب السبب | عند الانطلاق وقبل كل بوابة مرحلة (stage gate) |
| **Reading-group charter** — ميثاق مجموعة القراءة | صفحة واحدة (one page): الجدول (schedule) والأدوار (roles) والقواعد (rules) ومعنى الاكتمال (done) | في الأسبوع 0 (week 0) |
| **Engagement canon** — المرجع الثابت للمشروع | الحقائق الثابتة (fixed facts) للحالة الجارية (running case) | كلما كتبت ملاحظات أو بيانات اختبار (test data) |

## 🏛️ عمليًا في بنك نجم
مُخرَجاتك: **المرجع الثابت للمشروع (engagement canon)** الذي يُعاد استخدامه في كل مختبر، و**ميثاق مجموعة القراءة (reading-group charter)**.

**بنك نجم خيالي (Najm Bank is fictional).** إنه بنك خليجي متوسط الحجم (mid-sized Gulf bank) في قطر والإمارات والاتحاد الأوروبي يظهر في مكتبة الدورات (course library)، كما في [*حوكمة الذكاء الاصطناعي (AI Governance)*، الدرس 0.3 — تعرّف على بنك نجم: سجل أنظمة الذكاء الاصطناعي منذ اليوم الأول](../aigp/index.ar.html#/0.3). كل شخص ونظام ورقم وسياسة هنا مختلق (invented)؛ فلا تقتبسها أبدًا بوصفها حقائق عن مؤسسة حقيقية (real organisation). والحقيقة الواقعية (سلوك حزمة التطوير، أو قانون، أو قضية) تُوسَم بوضوح وتُذكر مصادرها.

**المشروع (The engagement).** تنضم إلى فريق **تمكين المطوّرين (Developer Enablement)** لبناء **نجم ديسك (Najm Desk)**، وهو مساعد ذكاء اصطناعي (AI assistant) لـ**مكتب خدمة تقنية المعلومات (IT Service Desk)**، من أول محادثة (first conversation) إلى الإطلاق الفعلي. **هند (Hind)**، رئيسة مكتب خدمة تقنية المعلومات، هي الراعية (sponsor) والعميلة في كل محادثة استكشاف وقبول. و**يارا (Yara)**، قائدة الفريق (team lead)، تعرف كيف تُعالَج التذاكر (tickets) فعلًا. و**فهد (Fahad)**، رئيس فريق تمكين المطوّرين، هو مرشدك. و**لجين (Lujain)**، مهندسة خرّيجة (graduate engineer)، هي زميلتك (peer) وترتكب الأخطاء التي ينبغي أن تتجنبها. ومن حولك **ليلى (Layla)** (حوكمة الذكاء الاصطناعي)، و**نورة (Noura)** (أمن التطبيقات والذكاء الاصطناعي)، و**حمد (Hamad)** (رئيس أمن المعلومات (CISO))، و**سارة (Sara)** (مسؤولة حماية البيانات)، و**مها (Maha)** (هندسة موثوقية المواقع (SRE))، و**سالم (Salem)** (هندسة المنصّات)، و**دانة (Dana)** (علوم البيانات)، و**طارق (Tariq)** (الهندسة).

**خط الأساس الخيالي (The fictional baseline).** نحو 1,800 تذكرة أسبوعيًا. نحو الربع أسئلة «كيف أفعل…؟» ⁦⁩ أو أسئلة سياسات (policy questions) يمكن الإجابة عنها من مكتبة السياسات (policy library)، ونحو الربع مشكلات وصول وكلمات مرور والمصادقة متعددة العوامل، والباقي أجهزة وشبكات وبرمجيات وأمن وغيرها. متوسط زمن الاستجابة الأولى نحو 3 ساعات و40 دقيقة. ويعمل أربعة عشر موظف دعم (fourteen agents) من الأحد إلى الخميس، من 07:00 إلى 17:00 بتوقيت قطر؛ ويكتب الموظفون بالإنجليزية والعربية.

**الأنظمة والقيود والنطاق (Systems, constraints and scope).** الأنظمة (systems): نظام التذاكر (ticketing) **TicketHub**، والهوية (identity) **Najm ID**، ومكتبة السياسات (ملفات markdown في عدّة المختبر)، ودليل الموارد البشرية (HR directory) **PeopleCore**، ومدير الأجهزة (device manager) **DeviceDesk**. القيود (constraints): لا بيانات سرّية (Confidential) أو مقيَّدة (Restricted) في أدوات الذكاء الاصطناعي الخارجية (external AI tools)، وبيانات الموظفين بيانات شخصية (personal data)، والتغييرات تحتاج إلى اعتماد الحوكمة، وكل إجراء كتابة (write action) يحتاج إلى إنسان أو بوابة سياسات (policy gate). ويجيب **نجم ديسك v1 (Najm Desk v1)** عن أسئلة السياسات مع الاستشهادات (citations)، ويبلّغ عن حالة التذكرة (ticket status)، ويعدّ مسودة تذكرة أو ينشئها بعد التأكيد (confirmation)، ويرفع *طلب* إلغاء قفل حساب (account-unlock request) مقيّدًا بالموافقة (approval-gated)، ويسلّم المحادثة إلى إنسان بسياقها الكامل (full context)، بدءًا بموظفي مكتب الخدمة. وفي الوحدة 6 تتفق مع هند على أهداف نجاح رقمية.

**الميثاق (The charter).** صفحة واحدة في مستودع مجموعتك (group repository):

```text
Charter v1
Meets: <day, time, place>, one module a week from <date>. Catch-up rule: <what if you miss a week>.
Roles (rotate weekly): facilitator, demo lead, sceptic, scribe. Customer role-player from Module 6.
Deliverable: week-NN/NOTES.md in your own repository, committed before the session.
Rules: no secrets in repositories; no pasted source text; every claim cites a lab output or a source.
Done for the week: lab runs offline, checkpoint answered, deliverable committed, one question ready.
```

## 🛠️ التمارين (Exercises)
لا يحتاج أي منها إلى الواجهة البرمجية الحقيقية.

- 🟢 **عرّفه لنظام تعرفه (Define it for a system you know).** اكتب صفحة واحدة عمّا يعنيه «مستوى المؤسسات» لنظام عملت عليه، مستخدمًا الخصائص العشر أو خصائصك. *يكتمل عندما (Done when):* تسمّي كل خاصية مُخرَجًا أو تقول «لا دليل» (توقّع اثنتين منها على الأقل)، ويستطيع زميل أن يجد كل مُخرَج من صفحتك وحدها.
- 🟡 **ارسم خريطة مشروع سابق (Map a past project).** املأ جدول دورة الحياة (lifecycle table) لمشروع أطلقته أو تابعته. *يكتمل عندما:* يكون لكل مرحلة مالك (owner) ومُخرَج (أو «لا شيء»)، ويكون للمرحلة الأضعف عاقبة ملموسة واحدة، وتكون قد كتبت السؤال الذي كان سيكشفها.
- 🔴 **أسّس مجموعة القراءة (Set up the reading group).** أنشئ مستودع المجموعة مع الميثاق (charter) وتقويم من سبعة عشر أسبوعًا (seventeen-week calendar) وتناوب للأدوار (role rotation) وجدول أعمال الجلسة الأولى (first-session agenda)، ثم أجرِ تحليلًا استباقيًا للفشل مدته 20 دقيقة على المجموعة نفسها. *يكتمل عندما:* يوافق كل عضو على الميثاق في طلب دمج (pull request)، ويُحجز موعد الجلسة الأولى، ويسرد التحليل الاستباقي ثلاثة أسباب للفشل، لكل منها إجراء تخفيف (mitigation) في الميثاق.

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **معاملة العرض التجريبي على أنه المنتج (Treating the demo as the product).** إنه لا يثبت إلا النصف الأول. أجرِ تحليلًا استباقيًا للفشل في الأسبوع الأول.
- **البناء قبل الاتفاق على معنى «الاكتمال» (Building before "done" is agreed).** من دون معايير قبول (acceptance criteria) يحسم الرأي الأمر، والرأي يتحرك. اتفقوا عليها في الوحدة 6.
- **استخدام «مستوى المؤسسات» شعارًا (Using "enterprise-grade" as a slogan).** استبدل به الأسئلة العشرة ومُخرَجاتها.
- **النسخ بدل القراءة (Copying instead of reading).** النص أو الشيفرة الملصقة لا تعلّم شيئًا وقد تخرق التراخيص (breach licences). دوّن ملاحظاتك بكلماتك الخاصة وأعد البناء بحزمة SDK الخام (raw SDK).

## 🧾 الخلاصة (Recap)
- مشروع الوكيل ثماني مراحل، لكل منها مُخرَج؛ وكثيرًا ما لا يملك المشروع المتعثر سوى مُخرَج البناء (build artefact).
- «بمستوى المؤسسات» عشر خصائص، تسندها أدلة يستطيع شخص آخر فتحها.
- اختر أبسط ما يؤدي المهمة من روبوت الدردشة وسير العمل والوكيل.
- خمس طبقات تَسِم كل درس؛ وتغطي طبقتا Delivery وProduction النصف الذي يتخطاه العرض التجريبي.
- الدورة روتين أسبوعي (weekly routine)؛ تعمل المختبرات دون اتصال، ثم دون أي تغيير على الواجهة البرمجية الحقيقية. وبنك نجم خيالي (fictional).

## ✍️ اختبر نفسك (Check yourself)

**1. أُوقفت تجربة تشغيلية (pilot) بعرض تجريبي (demo) متقن بعد أربعة أشهر. لم تستطع مها أن تقول من يتلقى نداء التنبيه (paged)، ولم تجد ليلى تقييم مخاطر (risk assessment)، ولم يستطع أحد تعديل الموجّه (prompt) بأمان. ما أفضل تشخيص؟**

- A. لم يكن النموذج قادرًا بما يكفي على مهمة بهذا التعقيد
- B. لم تُخطَّط المراحل التي تلي البناء ولم يملكها أحد
- C. اختار الفريق إطار وكلاء (agent framework) خاطئًا
- D. استمر العرض التجريبي وقتًا أقصر مما ينبغي

<details><summary>الإجابة</summary>

**B.** كل بند ناقص ينتمي إلى مرحلة تلي البناء: التشغيل (operate) والتأمين (secure) والتقييم (evaluate). لم يفشل النموذج. (🟡 مثال تطبيقي (Worked example).)

</details>

**2. يقول مورّد (vendor) إن وكيله (agent) «بمستوى المؤسسات لأننا نستخدم أقوى نموذج ونختبره» ("enterprise-grade because we use the strongest model and we test it"). أي رد يطبّق هذا الدرس؟**

- A. اقبله، لأن قوة النموذج (model strength) تحدد معظم الخصائص
- B. اسأل أولًا عن الإطار (framework) الذي يستخدمه قبل أي شيء آخر
- C. اطلب تقرير الأمن (security report) وحده؛ فالباقي يتبعه
- D. اطلب المُخرَج (artefact) الذي يقف وراء كل خاصية من الخصائص العشر (ten properties)

<details><summary>الإجابة</summary>

**D.** يُثبَت مستوى المؤسسات بالدليل (evidence): مجموعة تقييم (eval set) ودليل تشغيل (runbook) وتقرير تكلفة (cost report). والنموذج القوي (strong model) لا ينتج أيًّا من هذه المُخرَجات (artefacts). (🟢 ماذا يعني «بمستوى المؤسسات».)

</details>

**3. يجب أن يصنّف نجم ديسك (Najm Desk) كل تذكرة جديدة بإحدى ست فئات (six categories) ويرسلها إلى الطابور (queue) الصحيح. أي تصميم (design) يناسب أكثر؟**

- A. سير عمل (workflow): يصنّف مرة واحدة، ثم يوجّه (route) بشيفرة عادية
- B. فريق تعدد وكلاء (multi-agent team) بمشرف (supervisor) وثلاثة عمّال (workers)
- C. وكيل مستقل (autonomous agent) يقرر أدواته وخطواته بنفسه
- D. روبوت دردشة (chatbot) يطلب من مقدّم الطلب (requester) اختيار فئة أولًا

<details><summary>الإجابة</summary>

**A.** المسار معروف مسبقًا، فسير العمل القائم على التوجيه الشرطي (routing workflow) أبسط وأرخص وأسهل اختبارًا. (🟢 روبوت الدردشة وسير العمل والوكيل.)

</details>

**4. يلصق أحد أعضاء المجموعة مثال إطار عمل (framework example) من مصدر مجاني (free source) في المختبر، ويعمل. ماذا تطلب الدورة منه أن يفعل؟**

- A. يبقيه كما هو، لأن المصدر مجاني والشيفرة تعمل
- B. يحذف المختبر ويقرأ الفصل التالي بدلًا منه
- C. يعيد بناء النمط (pattern) بحزمة SDK الخام (raw SDK) ويستشهد بالمصدر
- D. يوحّد المجموعة كلها على ذلك الإطار

<details><summary>الإجابة</summary>

**C.** تستخدم المختبرات حزمة SDK الخام (raw SDK) لتفهم النمط (pattern)، وتستشهد الملاحظات بالمصادر (cite sources) دون نسخ (without copying). (🟡 المصادر وتقلّب الأطر.)

</details>

**5. قبل الإطلاق الفعلي (go-live)، يسأل فريق حمد عمّا يمنع مستندًا ملصقًا (pasted document) من توجيه الوكيل (agent)، وتسأل ليلى من وافق على التغيير. أي مرحلة وأي خصائص تنطبق؟**

- A. الاستكشاف (Discover)، مع مقبول (accepted) وموثَّق (documented)
- B. التأمين (Secure)، مع آمن (secure) وخاضع للحوكمة (governed)
- C. الإطلاق (Ship)، مع مضبوط التكلفة (cost-controlled) وموثوق (reliable)
- D. التشغيل (Operate)، مع قابل للدعم (supportable) وقابل للمراقبة (observable)

<details><summary>الإجابة</summary>

**B.** مقاومة الحقن أمن (security)، والموافقة والاعتماد حوكمة (governance)؛ وكلاهما ينتمي إلى مرحلة التأمين (Secure). (🟢 دورة الحياة والخصائص العشر.)

</details>

## 📚 المراجع (References)
- Manning، *Grokking AI Applications* (Andrea De Mauro؛ الكتاب الوحيد المدفوع؛ ابحث بالعنوان) — https://www.manning.com/
- Antonio Gulli، *Agentic Design Patterns* (مسودة مجانية؛ إن انتقل الرابط فابحث بالعنوان) — https://docs.google.com/document/d/1rsaK53T3Lg5KoGwvf8ukOUvbELRtH-V0LnOIFDxBryE/
- Microsoft، *AI Agents for Beginners* — https://github.com/microsoft/ai-agents-for-beginners
- Anthropic، «Building effective agents» — https://www.anthropic.com/engineering/building-effective-agents
- Chip Huyen، *aie-book* (رفيق كتاب *AI Engineering*) — https://github.com/chiphuyen/aie-book
- LangChain Academy (دورة LangGraph مجانية) — https://academy.langchain.com/
- وثائق مطوّري Anthropic (صفحة البداية) — https://docs.anthropic.com/
- الدورة المصاحبة (Companion course): [*تشغيل وكلاء الذكاء الاصطناعي في الإنتاج (Running AI Agents in Production)*، المستويات L0–L5 (levels L0–L5)](../agentic/learning-path.ar.html#level-2-agent-engineer)، للنصف التشغيلي من دورة الحياة.
- **اقرأ هذا الأسبوع (Read this week).** لا تحدد خطة الدورة فصولًا للوحدة 0؛ وتبدأ قوائم الفصول الأسبوعية من الوحدة 1. في هذا الأسبوع، تصفّح فهرس كل مصدر من المصادر أعلاه لتعرف أين تُغطّى مواضيع الوكلاء (agents) والأدوات والاسترجاع والتقييم والنشر، وقرّر أي كتاب ستقرأ أولًا.

---

# 0.2 — مختبرك: الإعداد وعدّة المختبر ومفتاح الواجهة البرمجية وسقف الإنفاق
*المستوى: 🟢 مبتدئ* · *المتطلبات: 0.1* · *الطبقة: Model, Delivery*

## ⚡ الدرس في دقيقة (In 60 seconds)
- لمختبرك وضعان وقاعدة شيفرة واحدة (one codebase): **محاكٍ دون اتصال (offline mock)** (مجاني ومبرمج مسبقًا) و**واجهة برمجية حقيقية (real API)** (مدفوعة). ولا يتغير سوى `ANTHROPIC_BASE_URL` و`ANTHROPIC_API_KEY`.
- الإعداد مرة واحدة: Python 3.11 أو أحدث، وبيئة افتراضية (virtual environment)، وحزمة التطوير المثبَّتة (`anthropic>=1,<2`)، وعدّة المختبر.
- يعيش المفتاح (key) في `.env`، ويعيش `.env` في `.gitignore`. اضبط سقف إنفاق قبل أول استدعاء حقيقي.
- شغّل `hello.py` في بداية كل جلسة. فهو يسمّي الوضع قبل أن ينفق أي شيء.
- يعلّمك المحاكي الآليات لا الجودة: فهو يقبل أي مفتاح ومعرّف نموذج (model id) ولا يستطيع الحكم على موجّه.
- التكلفة حساب بسيط (arithmetic): الرموز من `resp.usage` مضروبة في الأسعار (prices) من صفحة الأسعار الحالية (current price page).

## 🧭 لماذا يهم
في ثاني يوم ثلاثاء لها، ترفع **لجين (Lujain)** مفتاح الواجهة البرمجية الخاص بها إلى مستودع الفريق (team repository) داخل `chat.py`. (افتراضية، مثل كل قصص نجم.) ويرصده ماسح الأسرار (secret scanner) لدى **نورة (Noura)** في دقائق، ويُلغى المفتاح (revoked). عامل أي مفتاح رُفع إلى مستودع (pushed key) على أنه علني: فقد أُفيد على نطاق واسع بأن برامج الكشط (scrapers) تحصد المفاتيح (harvest keys). وفي الخميس تظن لجين أنها تعمل دون اتصال، لكن صدفتها (shell) لا تحتوي `ANTHROPIC_BASE_URL` و`.env` الخاص بها يحمل المفتاح الحقيقي (real key)، فينتج عن اختبار حلقة (loop test) عشرات الاستدعاءات المدفوعة. والسقف (cap) الذي ضبطته يوم الأربعاء يُبقي التكلفة صغيرة.

## 📐 كيف يعمل

### 🟢 الأساسيات

**التثبيت (Install).** تحتاج إلى Python 3.11 أو أحدث، ومستودع الدورة (course repository) (ومعه عدّة المختبر)، وبيئة افتراضية، وهي مجلد حزم خاص يعزل هذه الدورة عن المشاريع الأخرى.

```bash
python3 --version                  # 3.11 or newer
git clone https://github.com/Tamoura/system-design-for-vibe-coders.git
cd system-design-for-vibe-coders/aiapps/labkit
printf '.env\n.venv/\n' >> ../../.git/info/exclude   # this clone does not ignore them: keep keys out of git
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt    # includes "anthropic>=1,<2"
python -c "import anthropic; print(anthropic.__version__)"    # 1.something
```

تعتمد المختبرات على شكل الإصدار 1.x من حزمة التطوير (1.x SDK)، فأبقِ التثبيت. وتفترض أسطر الصدفة (shell lines) أنك تستخدم bash أو zsh؛ وعلى Windows استخدم WSL.

**شغّل المحاكي ثم سكربت الفحص السريع (Start the mock and run the smoke script).**

```bash
python -m labkit.mock_server --port 8787 &       # the offline "API" on your machine
MOCK_PID=$!
sleep 2                                           # let it start
export ANTHROPIC_BASE_URL=http://127.0.0.1:8787 ANTHROPIC_API_KEY=mock
python labs/m00/hello.py
kill $MOCK_PID                                    # stop it when done
```

```text
mode     : MOCK (offline)  (free and scripted: good for mechanics, useless for judging answer quality)
endpoint : http://127.0.0.1:8787   model: claude-sonnet-5-5
key      : set, 4 characters, never printed
reply    : (mock) I received: Reply with one short sentence confirming you can hear me.
stop     : end_turn   request id: req_mock_1e53b1df9d8d
tokens   : in=18 out=19
```

**مفتاح الواجهة البرمجية (The API key).** للواجهة الحقيقية، أنشئ حساب Claude Console، وأضف بيانات الفوترة (billing)، وأنشئ مفتاحًا يحمل اسم الدورة. وتعرض Console المفتاح عادةً مرة واحدة فقط، فانسخه إلى `.env` في المجلد الذي تشغّل منه السكربتات (scripts)؛ وأودِع (commit) ملف `.env.example` فقط.

```text
# .gitignore (first lines of your own repository)
.env
.venv/
__pycache__/
```

```text
# .env (stays on your machine, never committed)
ANTHROPIC_API_KEY=paste-your-real-key-here
MODEL=claude-sonnet-5-5
```

مفتاح واحد لكل شخص، ولا يوضع أبدًا في شيفرة أو دفتر أو رسالة محادثة (chat message) أو لقطة شاشة (screenshot). وإن تسرّب مفتاح، فألغِه (revoke) في Console أولًا ونظّف ثانيًا. وقبل مشاركة مستودع، افحص تاريخه دون طباعة مفتاح مسرَّب: `git log -p --all | grep -q "sk-ant-" && echo FOUND || echo clean`. ومستودع الدورة نفسه يطبع FOUND: فالملف `flawed_chat.py` في الدرس 0.3 يزرع مفتاحًا مزيفًا (fake key) عمدًا.

**سقف الإنفاق (A spending cap).** اضبط واحدًا قبل أول استدعاء حقيقي. وقت كتابة الدرس، يصف التوثيق سقف إنفاق شهريًا لكل شريحة استخدام (usage tier)، وحدًّا أقل منه تضبطه بنفسك في Console، وحدود إنفاق ومعدل لكل مساحة عمل (workspace) (وليس للمساحة الافتراضية، فأنشئ مساحة عمل للدورة). وحين يُبلَغ أحد الحدود، تفشل الاستدعاءات (راجع استكشاف الأخطاء). الأسماء والأماكن تتغير؛ فراجع صفحة حدود المعدل (rate-limits page). والسقف شبكة أمان (backstop) لا عدّاد (meter): فراقب صفحة الاستخدام (Usage page) أيضًا.

### 🟡 التعمق أكثر

**ما هو المحاكي وما ليس هو (What the mock is, and what it is not).** إنه خادم محلي (local server) يتحدث بواجهة الرسائل (Messages API)، فتعمل حزمة التطوير الحقيقية (real SDK) دون تغيير.

| ما يفعله المحاكي ⁦⁩ | ما لا يفعله المحاكي ⁦⁩ |
|---|---|
| يُبقي الآليات صادقة: استدعاءات عديمة الحالة (stateless calls)، واقتران `tool_use` بـ`tool_result` (pairing)، وقطع الإخراج بسبب `max_tokens` (truncation)، والموجّهات الطويلة جدًا (over-long prompts)، ورفض معاملات أخذ العينات (sampling parameters) في أحدث النماذج (يأتي `TypeError` من حزمة التطوير أولًا) | يفهم أي شيء (understand anything): فالإجابات تأتي من قواعد وكلمات مفتاحية |
| يزيد أعداد الرموز المقدَّرة كلما نما السجل (history) | يعدّ الرموز مثل المُجزّئ الحقيقي (real tokenizer) أو يفرض حدود معدل حقيقية |
| يُخطئ عند الطلب عبر التوجيهات (directives) | يتحقق من مفتاحك أو معرّف النموذج: أي مفتاح يعمل، والخطأ المطبعي (typo) لا يعطي 404 |

حيث يحتاج المختبر إلى جودة الموجّهات أو جودة الاسترجاع (retrieval quality) أو السلامة، يكتب **يحتاج الواجهة البرمجية الحقيقية (Needs the real API)**. والتوجيهة (directive) وسم في رسالة يجعل المحاكي يُخطئ عمدًا: يضيف `[mock:thinking]` كتلة تفكير (thinking block)، ويعيد `[mock:ratelimit]` الخطأ 429، وينتظر `[mock:slow]` ثلاث ثوانٍ. ويجعل `MOCK_CONTEXT_WINDOW=8000` تجربة التجاوز (overflow) رخيصة. وتشغيل `pytest` في `aiapps/labkit` يتحقق من المحاكي مقابل حزمة التطوير الحقيقية.

**قاعدة شيفرة واحدة بوضعين (One codebase, two modes).** تقرأ حزمة التطوير (SDK) متغيري بيئة، عنوانًا أساسيًا ومفتاحًا (أي قيمة وهمية (dummy value) دون اتصال)، ولا يتغير شيء آخر.

```mermaid
flowchart RL
    L["شيفرة مختبرك<br/>متطابقة في الوضعين<br/>(Your lab code<br/>identical in both modes)"] --> K["حزمة التطوير anthropic<br/>تقرأ متغيرين<br/>(anthropic SDK<br/>reads two variables)"]
    K --> Q{"المتغير ANTHROPIC_BASE_URL<br/>هل هو مضبوط؟<br/>(ANTHROPIC_BASE_URL<br/>set?)"}
    Q -->|"نعم، 127.0.0.1 (yes, 127.0.0.1)"| M["محاكي عدّة المختبر<br/>مجاني ومبرمج مسبقًا<br/>(Lab kit mock<br/>free and scripted)"]
    Q -->|"لا (no)"| R["واجهة Anthropic البرمجية<br/>تُحاسَب لكل رمز<br/>(Anthropic API<br/>billed per token)"]
```

للتحول إلى الوضع الحقيقي، أوقف المحاكي ونفّذ `unset ANTHROPIC_BASE_URL ANTHROPIC_API_KEY` ليأتي المفتاح من `.env`: فالدالة `load_dotenv` لا تتجاوز أبدًا متغيرًا مُصدَّرًا (exported variable)، وهي ميزة إلى أن تنسى أنك صدّرت القيمة `mock`. ويُبلغك سكربت الفحص السريع بالوضع فلا تحتاج إلى التذكّر.

```python
# labs/m00/hello.py
"""Smoke test: which mode are you in, and does one real SDK call work?
Offline: start the mock, then  export ANTHROPIC_BASE_URL=http://127.0.0.1:8787 ANTHROPIC_API_KEY=mock
Real: unset ANTHROPIC_BASE_URL and keep your key in .env. The code is the same; only the environment differs.
Exit codes: 0 worked, 1 the API call failed, 2 configuration problem."""
import os
import sys
from urllib.parse import urlparse

import anthropic
from anthropic import Anthropic
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))          # nearest .env, here or in a parent folder; exported variables win over the file
MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")   # never hard-code a model id in lab code


def detect_mode(base_url, api_key):
    """Return (mode, hint). A pure function, so a test can call it with no network."""
    if not api_key:
        return "NO KEY", "set ANTHROPIC_API_KEY (offline: mock; real: your key in .env)"
    host = urlparse(base_url).hostname if base_url else None
    if host in ("127.0.0.1", "localhost", "::1"):
        return "MOCK (offline)", "free and scripted: good for mechanics, useless for judging answer quality"
    if host in (None, "api.anthropic.com"):
        if api_key == "mock":
            return "MISCONFIGURED", "the dummy key would get a 401 from the real API: set ANTHROPIC_BASE_URL or a real key"
        return "REAL API (billable)", "every call costs money: is your spending cap set?"
    return "CUSTOM ENDPOINT", f"the gateway at {host} sees your key and prompts: trust whoever runs it"


def main() -> int:
    base_url, key = os.environ.get("ANTHROPIC_BASE_URL"), os.environ.get("ANTHROPIC_API_KEY")
    mode, hint = detect_mode(base_url, key)
    print(f"mode     : {mode}  ({hint})")
    print(f"endpoint : {base_url or 'https://api.anthropic.com (SDK default)'}   model: {MODEL}")
    print(f"key      : {f'set, {len(key)} characters, never printed' if key else 'NOT SET'}")
    if mode in ("NO KEY", "MISCONFIGURED"):
        return 2
    try:
        resp = Anthropic(max_retries=0).messages.create(      # max_retries=0: fail fast while you set up
            model=MODEL,
            max_tokens=1024,                                  # required; thinking tokens count as output
            messages=[{"role": "user", "content": "Reply with one short sentence confirming you can hear me."}],
        )
    except anthropic.APIConnectionError:                      # no HTTP response at all
        print("FAILED   : cannot connect. Is the mock running on that port? Behind a proxy? See the table.")
        return 1
    except anthropic.APIStatusError as e:                     # an HTTP error: 400, 401, 404, 429, 5xx ...
        print(f"FAILED   : {type(e).__name__} (HTTP {e.status_code}): {e.message}")
        return 1
    text = next((b.text for b in resp.content if b.type == "text"), "")      # never resp.content[0].text
    u = resp.usage
    print(f"reply    : {text}")
    print(f"stop     : {resp.stop_reason}   request id: {resp._request_id}")
    print(f"tokens   : in={u.input_tokens} out={u.output_tokens}")
    p_in, p_out = os.environ.get("PRICE_IN_PER_MTOK"), os.environ.get("PRICE_OUT_PER_MTOK")
    if p_in and p_out:
        print(f"cost     : {(u.input_tokens * float(p_in) + u.output_tokens * float(p_out)) / 1_000_000:.6f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

يأتي `MODEL` من البيئة (environment). و`max_tokens` مطلوب (required)؛ والقيمة 1024 حدّ أدنى معقول (sensible floor) في النماذج الحالية لأن رموز التفكير (thinking tokens) تُحسب ضمن المخرجات (output). والرد هو كتلة النص (text block) المختارة بحسب النوع، وليس أبدًا `resp.content[0].text`. سجّل `resp.usage` و`resp._request_id` في كل استدعاء، وعالج كل `stop_reason` في حلقة الإنتاج (production loop) (الوحدة 1).

**من الاستخدام إلى المال (From usage to money).** يكلّف الاستدعاء (call) `(input tokens × input price + output tokens × output price) ÷ 1,000,000`. الأسعار تتغير، فانسخها من صفحة الأسعار الحالية إلى متغيري بيئة، ولا تضعها أبدًا في الشيفرة. و`output_tokens` يشمل رموز التفكير، وتذكر ملاحظات Anthropic عن النماذج (model notes) أن بعض الأجيال الأحدث تعدّ النص نفسه بعدد رموز أكبر بنحو 30% (about 30% more tokens)، فأعد القياس بعد أي تغيير للنموذج. ومع تفعيل التخزين المؤقت (caching on)، يعدّ `input_tokens` الجزء غير المخزَّن فقط (uncached part) وتُسعَّر حقول التخزين المؤقت (cache fields) بشكل مختلف (الوحدة 14). عُدّ الرموز قبل الإرسال بـ`client.messages.count_tokens`، وليس أبدًا `tiktoken`. ويكبر الإدخال (input) بسرعة، لأن كل استدعاء يعيد إرسال السجل.

```python
# labs/m00/cost.py
"""Turn token counts into money and project a pilot's bill. No price is hard-coded: copy the current prices
from the price page into PRICE_IN_PER_MTOK and PRICE_OUT_PER_MTOK (per million tokens), then for example:
  python labs/m00/cost.py --system 1500 --user 60 --answer 250 --turns 6 --conversations 450 --weeks 4"""
import argparse
import os


def call_cost(tokens_in: int, tokens_out: int, price_in: float, price_out: float) -> float:
    """One API call: tokens x price per million tokens."""
    return (tokens_in * price_in + tokens_out * price_out) / 1_000_000


def conversation_tokens(system: int, user: int, answer: int, turns: int) -> tuple[int, int]:
    """Total (input, output) tokens for one chat. Every call resends the system prompt and the whole history:
    call t sends  system + t user messages + (t-1) answers  and receives one answer."""
    return sum(system + t * user + (t - 1) * answer for t in range(1, turns + 1)), turns * answer


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for name, default in [("system", 1500), ("user", 60), ("answer", 250), ("turns", 6), ("conversations", 450), ("weeks", 4)]:
        ap.add_argument(f"--{name}", type=int, default=default)
    a = ap.parse_args()
    t_in, t_out = conversation_tokens(a.system, a.user, a.answer, a.turns)
    n = a.conversations * a.weeks
    print(f"one conversation: in={t_in} out={t_out} tokens;  pilot: {t_in * n:,} in, {t_out * n:,} out over {n:,} conversations")
    p_in, p_out = os.environ.get("PRICE_IN_PER_MTOK"), os.environ.get("PRICE_OUT_PER_MTOK")
    if p_in and p_out:
        one = call_cost(t_in, t_out, float(p_in), float(p_out))
        print(f"cost: {one:.5f} per conversation, {one * n:,.2f} for the pilot; budget at x2: {2 * one * n:,.2f}")
    else:
        print("set PRICE_IN_PER_MTOK and PRICE_OUT_PER_MTOK from the current price page to see money")
```

بأسعار مختلقة (invented prices) هي 1 و5 وحدات لكل مليون رمز، لإظهار الحساب فقط، يطبع الأمر `PRICE_IN_PER_MTOK=1 PRICE_OUT_PER_MTOK=5 python labs/m00/cost.py --turns 12` ما يلي:

```text
one conversation: in=39180 out=3000 tokens;  pilot: 70,524,000 in, 5,400,000 out over 1,800 conversations
cost: 0.05418 per conversation, 97.52 for the pilot; budget at x2: 195.05
```

أدّت مضاعفة الأدوار من ستة إلى اثني عشر إلى ضرب رموز الإدخال (input tokens) في نحو 2.8 (من 14,010 إلى 39,180). ويتجاهل نموذج التكلفة التخزين المؤقت (caching) ومخططات الأدوات (tool schemas) والاسترجاع، ويجب أن يشمل `--answer` رموز التفكير. و«×2» ("x2") قاعدة تقريبية (rule of thumb)؛ فاستخدم نسبتك المقيسة (measured ratio).

**استكشاف الأخطاء (Troubleshooting).** تختلف نصوص الأخطاء الحقيقية عن تقريبات المحاكي (mock's approximations)، فاقرأ نصّك أنت.

| العَرَض (Symptom) | السبب المرجّح (Likely cause) | ما تفعله |
|---|---|---|
| `TypeError` «Could not resolve authentication method» (لم يُرسَل شيء)، أو 401 `AuthenticationError` | لا مفتاح؛ أو مفتاح خاطئ أو مُلغى؛ أو إرسال `mock` إلى الواجهة الحقيقية؛ أو ضبط `ANTHROPIC_AUTH_TOKEN` أيضًا | شغّل `hello.py`؛ وتأكد من العثور على `.env`؛ وأنشئ مفتاحًا جديدًا |
| 404 `NotFoundError` «model: …» | خطأ مطبعي (نقاط بدل شرطات)، أو نموذج متقاعد (retired model)، أو نموذج لا تستطيع مؤسستك استخدامه | انسخ المعرّف (id) من صفحة النماذج (models page) (المحاكي لا يرفض أيًّا منها أبدًا) |
| 400 `BadRequestError`، مثل «prompt is too long» | تجاوز السجل لنافذة السياق (context window)، أو معامل غير صالح (invalid parameter)، أو `tool_result` مفقود (missing) | اقرأ `e.message`؛ وقصّ الأدوار القديمة (الوحدة 1) |
| 429 `RateLimitError`، أو 500 و529 | حد المعدل (rate limit)؛ أو مشكلة من جهة المزوّد (provider-side trouble) | تعيد حزمة التطوير المحاولة مرتين (retries twice)؛ فأبطئ، وافحص `retry-after`، وأعد المحاولة بتراجع أسي (retry with backoff) |
| 400 «You have reached your specified API usage limits»، أو 402 `billing_error`، أو 429 دون `retry-after` | حد إنفاقك (spend limit)، أو السقف الشهري للشريحة، أو مشكلة فوترة (billing problem) | ارفع الحد، أو أصلح الفوترة (fix billing)، أو انتظر إعادة الضبط؛ فإعادة المحاولة (retries) لا تفيد |
| «Connection refused» (`APIConnectionError`) | المحاكي لا يعمل، أو منفذ خاطئ، أو جدار ناري (firewall) | شغّل المحاكي؛ واستخدم `127.0.0.1` والمنفذ نفسه |
| يعمل في البيت ويفشل في البنك | خادم وسيط مؤسسي (corporate proxy) أو فحص TLS (TLS inspection) | اضبط `HTTPS_PROXY` و`NO_PROXY=127.0.0.1`؛ ووجّه `SSL_CERT_FILE` إلى حزمة الشهادات (certificate bundle) لدى فريق تقنية المعلومات؛ أو مرّر `DefaultHttpxClient(proxy=...)` |

### 🔴 نظرة الخبير

**المفتاح بيانات اعتماد (a key is a credential)، والعنوان الأساسي (base URL) قرار ثقة (trust decision).** إن أقرنت مفتاحًا حقيقيًا بـ`ANTHROPIC_BASE_URL` غير محلي، فسيتلقى ذلك الخادم (server) مفتاحك وكل موجّه. والبوابات المؤسسية (enterprise gateways) مشروعة؛ لكن عاملها بوصفها طرفًا ثالثًا (third party)، ولهذا ينبّه `hello.py` عليها. ويناسب `.env` حاسوبًا محمولًا؛ وتنقل الوحدات اللاحقة المفاتيح إلى مدير أسرار (secret manager)، مفتاحًا لكل بيئة.

## 🧰 الأدوات
| الأداة أو الممارسة أو النمط | ما هي وماذا تفعل | متى تلجأ إليها |
|---|---|---|
| **Pinned SDK** — حزمة التطوير المثبَّتة | يثبّت `anthropic>=1,<2` الإصدار الرئيسي (major version) | دائمًا؛ والترقية (upgrade) عن قصد |
| **.env file** — ملف .env | ملف محلي تتجاهله git للأسرار | المفاتيح والإعدادات الخاصة بكل جهاز (per-machine settings) |
| **Lab kit mock** — محاكي عدّة المختبر | خادم دون اتصال (offline server) يتحدث بواجهة الرسائل | الآليات والاختبارات (tests) والتكامل المستمر (CI)، دون تكلفة |
| **Smoke script** — سكربت الفحص السريع | يسمّي `hello.py` الوضع ويجري استدعاءً واحدًا (one call) | أول أمر في كل جلسة |
| **Spending cap** — سقف الإنفاق | حد من جهة المزوّد (provider-side limit) على ما تستطيع مؤسسة أو مساحة عمل إنفاقه | قبل أول استدعاء حقيقي |
| **Cost estimate** — تقدير التكلفة | الرموز × السعر (price)، مُسقَطة على تجربة تشغيلية | قبل التجربة التشغيلية، ثم بالأرقام المقيسة (measured numbers) |

## 🏛️ عمليًا في بنك نجم
**المُسلَّم، الجزء 1 من الأسبوع 0: مستودع مختبرك (Deliverable, part 1 of week 0: your lab repository).** أنشئ مستودعًا خاصًا (private repository) بجوار مستودع الدورة المستنسخ. يبني Claude Code الهيكل (skeleton) أدناه؛ وأنت تقرأ كل ملف.

```text
najm-desk-lab/                  your own private repository
├── .gitignore  .env.example    names only; .env itself is ignored
├── requirements.txt  Makefile  scripts/use-mock.sh  scripts/use-real.sh
├── CLAUDE.md                   written in lesson 0.3
└── week-00/NOTES.md  hello-mock.txt  hello-real.txt   (one week-NN folder per module)
```

يضم `week-00/NOTES.md` خمسة عناوين (five headings): **سقف الإنفاق (Spending cap)**، و**تخزين المفتاح (Key storage)**، و**فحوص الوضع (Mode checks)** (المخرجات الملصقة)، و**تقدير التكلفة (Cost estimate)** (الافتراضات ومدى)، و**المفاجآت (Surprises)**. والتمرين 🟡 وحده يحتاج إلى الواجهة الحقيقية؛ ولا شيء هذا الأسبوع يُظهر ما إذا كان نموذج حقيقي يجيب جيدًا (answers well).

**جلسة المجموعة، الجزء 1: عيادة الإعداد، 30 دقيقة (Group session, part 1: setup clinic, 30 minutes).** يعرض كل شخص سطر الوضع (mode line) من تشغيل دون اتصال (offline run)؛ ويوقف شخص واحد المحاكي ويُظهر الفشل. ويبحث كل اثنين في تاريخ بعضهما عن `sk-ant-`. ويقول كل شخص أين ضُبط سقفه.

**ابنه مع Claude Code (Build it with Claude Code).** أعطه هذه المواصفة، ووافق على خطته قبل أن يعدّل أي شيء.

```text
GOAL
Create my lab repository "najm-desk-lab" next to the cloned course repo, with scripts to switch between the offline mock and the real API.

CONTEXT (read first)
../system-design-for-vibe-coders/aiapps/labkit/README.md, requirements.txt and labs/m00/hello.py. Do not modify anything in that repo.

BUILD
1. .gitignore (.env, .venv/, __pycache__/, .mock.pid) and .env.example (ANTHROPIC_API_KEY empty, MODEL=claude-sonnet-5-5, PRICE_IN_PER_MTOK and PRICE_OUT_PER_MTOK empty)
2. requirements.txt: anthropic>=1,<2 plus what labkit/requirements.txt lists
3. scripts/use-mock.sh and scripts/use-real.sh, meant to be sourced. use-mock exports ANTHROPIC_BASE_URL=http://127.0.0.1:8787 and ANTHROPIC_API_KEY=mock. use-real unsets both.
4. Makefile targets: setup, mock (start the mock, write its PID to .mock.pid, wait until the port answers), stop (kill only that PID), hello, test (the lab kit tests)
5. week-00/NOTES.md with the five headings from the lesson

CONSTRAINTS
Never read, print or write a real key. Do not call the real API. Python 3.11+. Scripts under 30 lines, commented. Never kill processes by name or pattern.

ACCEPTANCE CHECKS
- make setup && make mock && source scripts/use-mock.sh && make hello prints "mode     : MOCK (offline)" and exits 0
- make stop leaves nothing listening on port 8787
- make test passes
- a throwaway .env holding a fake key does not appear in git status

DO NOT
Add CI, Docker or extra features. Do not commit. Plan first and wait for my OK.
```

**تحقّق قبل أن تقبله (Verify before you accept it).**
- شغّل فحوص القبول الأربعة بنفسك؛ فعبارة «يفترض أن يعمل» ليست نتيجة.
- اقرأ ملف Makefile بحثًا عن أوامر إنهاء العمليات بالاسم (kill-by-name) وعن تعديلات على مستودع الدورة.
- اقرأ السكربتين (both scripts): هل يُلغي `use-real.sh` ضبط المتغيرين كليهما، وهل يطبع أي شيء مفتاحًا؟

## 🛠️ التمارين
- 🟢 **سكربت الفحص السريع دون اتصال (The smoke script, offline).** شغّل `hello.py` والمحاكي يعمل، ثم وهو متوقف (stopped)، ثم والمفتاح غير مضبوط (key unset). *يكتمل عندما:* تُحفظ ثلاثة مخرجات (three outputs) في `week-00/` مع رموز الخروج (exit codes) (0 و1 و2 من `echo $?`) وتستطيع شرح كل سطر من الأول. شغّل الثالثة حيث لا يوفّر أي `.env`، في المجلد أو في مجلد أب، مفتاحًا. لا حاجة إلى واجهة حقيقية.
- 🟡 **السكربت نفسه على الواجهة الحقيقية (The same script, real API).** ضع مفتاحك في `.env`، واضبط متغيرات الأسعار (price variables)، وألغِ ضبط متغيرات المحاكي، وشغّله. *يكتمل عندما:* يقول الوضع `REAL API (billable)`، وتختلف أعداد الرموز (token counts) عن أعداد المحاكي، ويُحفظ معرّف الطلب (request id)، ويطابق سطر التكلفة (cost line) حسابك، ولا يجد بحث التاريخ (history search) أي `sk-ant-`. **يحتاج الواجهة البرمجية الحقيقية (Needs the real API).**
- 🔴 **سجّل السقف والتقدير (Record the cap and the estimate).** شغّل `cost.py` للدورة كلها في سيناريو منخفض وآخر متوقع وثالث مرتفع. *يكتمل عندما:* يذكر `NOTES.md` السقف (أين وكم ومن يستطيع تغييره)، وتكاليف السيناريوهات الثلاثة مع افتراضاتها (assumptions)، وعتبة تحذير (warning threshold) تحت السقف (تنبيه Console إن وُجد، وإلا فتذكير في التقويم)، وردّك حين يبلغها الاستخدام. يحتاج إلى وصول إلى Console لا إلى استدعاءات الواجهة.

## ⚠️ أخطاء وفخاخ
- **مفتاح في الشيفرة أو دفتر أو لقطة شاشة (A key in code, a notebook or a screenshot).** استخدم `.env`، وافحص التاريخ (scan history)، وألغِ المفتاح فورًا إن تسرّب.
- **عدم معرفة وضعك (Not knowing your mode).** متغير منسي (forgotten variable) يحوّل «دون اتصال» ("offline") إلى استدعاءات مدفوعة (billed calls). شغّل `hello.py` أولًا.
- **الوثوق بالمحاكي في الجودة (Trusting the mock for quality).** لا يستطيع التمييز بين موجّه جيد وسيئ؛ استخدم الواجهة الحقيقية.
- **تثبيت معرّف النموذج أو الأسعار داخل الشيفرة (Hard-coding the model id or prices).** كلاهما يتغير؛ فاقرأهما من البيئة.

## 🧾 الخلاصة
- قاعدة شيفرة واحدة بوضعين: المحاكي مجاني ومبرمج مسبقًا، والواجهة الحقيقية مدفوعة (billed)؛ ويبدّل بينهما متغيران (two variables).
- ثبّت `anthropic>=1,<2` (pin)، وأبقِ المفاتيح في `.env` متجاهَل (ignored)، وضع سقفًا للإنفاق (cap spending) قبل أول استدعاء حقيقي.
- يقبل المحاكي أي مفتاح ومعرّف نموذج ولا يحكم على الجودة أبدًا.
- التكلفة هي الرموز × السعر؛ ويكبر الإدخال في كل دور لأن السجل يُعاد إرساله.

## ✍️ اختبر نفسك

**1. تظن أنك تختبر دون اتصال (offline)، لكن `.env` يحمل مفتاحك الحقيقي (real key) و`ANTHROPIC_BASE_URL` غير مضبوط. ما الذي يُخبرك قبل مفاجأة الفوترة (billed surprise)؟**

- A. تحذّرك حزمة التطوير (SDK) قبل أي استدعاء مدفوع (billed call)
- B. يعترض المحاكي (mock) كل ما يبدو اختبارًا
- C. يرفض المزوّد (provider) الاستدعاءات القادمة من شيفرة المختبر (lab code)
- D. تشغيل `hello.py` أولًا، لأنه يطبع الوضع (mode)

<details><summary>الإجابة</summary>

**D.** يُبلغ `hello.py` عن `REAL API (billable)` قبل أن ينفق أي شيء. ولا حزمة التطوير (SDK) ولا المزوّد (provider) يحذّر. (🟡 قاعدة شيفرة واحدة بوضعين (One codebase, two modes).)

</details>

**2. دون اتصال (offline)، تنجح كل المختبرات. ويفشل أول تشغيل حقيقي (first real run) بخطأ «غير موجود» (not-found error) يذكر النموذج. ما السبب الأرجح؟**

- A. بلغتَ سقف إنفاقك (spending cap)
- B. قبل المحاكي (mock) معرّف نموذج مكتوبًا خطأً ترفضه الواجهة الحقيقية (real API)
- C. إصدار حزمة التطوير (SDK version) أحدث من أن يناسب النموذج
- D. تفرض عليك الواجهة الحقيقية حد المعدل (rate limiting)

<details><summary>الإجابة</summary>

**B.** لا يتحقق المحاكي (mock) من معرّفات النماذج (model ids)، فلا يفشل الخطأ المطبعي (typo) إلا أمام الواجهة الحقيقية. (🟡 ما ليس هو المحاكي.)

</details>

**3. تكلّف محادثة من ستة أدوار (six-turn chat) مقدارًا X من رموز الإدخال (input tokens). لماذا تكلّف محادثة من اثني عشر دورًا أكثر بكثير من 2X؟**

- A. يعيد كل استدعاء إرسال موجّه النظام (system prompt) والسجل كاملًا (full history)
- B. تنتقل الأدوار اللاحقة إلى نموذج أغلى (pricier model) تلقائيًا
- C. تعيد حزمة التطوير المحاولة (retries) أكثر في المحادثات الطويلة
- D. تُحاسَب رموز الإخراج (output tokens) بسعر الإدخال (input rate)

<details><summary>الإجابة</summary>

**A.** يكبر الإدخال (input) في كل دور، فيتجاوز المجموع عدد الأدوار: يُظهر `cost.py` الرقمين 14,010 مقابل 39,180 رمزًا. (🟡 من الاستخدام إلى المال.)

</details>

**4. رُفع مفتاح الواجهة البرمجية (API key) الخاص بك إلى مستودع الفريق (team repository) قبل ساعة. ما الخطوة الأولى الصحيحة (the right first move)؟**

- A. احذف الملف في إيداع جديد ولا تقل شيئًا
- B. أعد كتابة التاريخ قبل أن تخبر أحدًا
- C. ألغِ المفتاح (revoke) في Console، ثم نظّف (clean up)
- D. انتظر يومًا لترى هل يستخدمه أحد

<details><summary>الإجابة</summary>

**C.** افترض أنه اختُرق (compromised): الإلغاء وحده يوقف إساءة الاستخدام. أما حذف الملف أو إعادة كتابة التاريخ فلا يلغي الانكشاف (exposure). (🟢 مفتاح الواجهة البرمجية.)

</details>

**5. أي مشكلة لا تراها إلا أمام الواجهة الحقيقية (real API) ولا تراها أبدًا أمام المحاكي دون اتصال (offline mock)؟**

- A. رفض `tool_use` بلا `tool_result`
- B. رد مقطوع بسبب `max_tokens` صغير
- C. مفتاح مرفوض (rejected key) يعيد 401
- D. نمو رموز الإدخال (input tokens) مع إعادة إرسال السجل (history)

<details><summary>الإجابة</summary>

**C.** يقبل المحاكي (mock) أي مفتاح؛ والثلاثة الأخرى آليات (mechanics) يعيد إنتاجها. (🟡 ما ليس هو المحاكي.)

</details>

## 📚 المراجع
- حزمة Anthropic SDK لـPython — https://github.com/anthropics/anthropic-sdk-python
- نظرة عامة على النماذج (Models overview) — https://platform.claude.com/docs/en/about-claude/models/overview
- الأسعار (Pricing) — https://platform.claude.com/docs/en/about-claude/pricing
- حدود المعدل وحدود الإنفاق — https://platform.claude.com/docs/en/api/rate-limits
- مساحات العمل (Workspaces) — https://platform.claude.com/docs/en/manage-claude/workspaces
- الأخطاء — https://platform.claude.com/docs/en/api/errors
- عدّ الرموز (Token counting) — https://platform.claude.com/docs/en/build-with-claude/token-counting
- البيئات الافتراضية في Python — https://docs.python.org/3/library/venv.html
- عدّة مختبر الدورة — https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/aiapps/labkit

---

# 0.3 — شريكك في البناء: توجيه Claude Code لبناء الوكلاء، وما يجب أن تفهمه أنت رغم ذلك
*المستوى: 🟢 مبتدئ* · *المتطلبات: 0.1، 0.2* · *الطبقة: Delivery*

## ⚡ الدرس في دقيقة (In 60 seconds)
- Claude Code شريكك في البناء، وليس بديلًا عنك، وليس حزمة `anthropic` التي تستدعيها شيفرة وكيلك. أنت المهندس المعماري (architect) والمراجِع (reviewer)؛ والمنهج هو **المواصفة (spec)، والخطة (plan)، وخطوات صغيرة (small steps)، والتحقق (verify)، ومراجعة الفروقات (review the diff)، والإيداع (commit)**.
- إنه سريع وطلق وواثق حتى حين يخطئ: فقد يخترع معاملات (parameters) في حزمة التطوير، ويُضعف الاختبارات (weaken tests) ليحصل على اللون الأخضر، ويبني أكثر بكثير مما طلبت.
- يحمل ملف `CLAUDE.md` أوامرك (commands) واصطلاحاتك (conventions) وقواعد السلامة (safety rules)؛ وتفرض الخطافات (hooks) والأذونات (permissions) ما تكتفي التعليمات بطلبه.
- راجع شيفرة الوكلاء التي يكتبها وكيل بقائمة فحص من عشر نقاط (ten-point checklist)؛ وثق بالنتائج صعودًا في هرم (pyramid)، من الفحوص دون اتصال (offline checks) إلى تقييمات النموذج الحقيقي (real-model evals).
- مؤشر القرار (Decision cue): إن لم تستطع أن تقول كيف ستعرف أن النتيجة صحيحة، فلا تفوّضها بعد.
- أكبر فخ (Biggest trap): اختبارات خضراء (green tests) لم تقرأها.

## 🧭 لماذا يهم
تطلب **لجين (Lujain)** من Claude Code سكربت محادثة (chat script) لنجم ديسك. وبعد أربعين ثانية يصبح بين يديها ستون سطرًا مرتبًا واختبارات ناجحة (passing tests). وفي المراجعة (review) يسأل **فهد (Fahad)**: ماذا يحدث حين يبدأ الرد بكتلة تفكير؟ وأين ينمو السجل، وأين يتوقف؟ ولا تستطيع لجين الإجابة: فهي لم تقرأ الشيفرة. (افتراضي.)

تفويض الكتابة لا يفوّض المسؤولية. وفق ما نُشر في يوليو 2025 (as reported in July 2025)، حذف مساعد برمجة بالذكاء الاصطناعي (AI coding assistant) قاعدة بيانات إنتاج (production database) خلال تجميد معلن للشيفرة ثم وصف ما فعله وصفًا خاطئًا (misdescribed). وتختلف التفاصيل بحسب الرواية، لكن الوكيل يتصرف بالأذونات التي تمنحها له.

## 📐 كيف يعمل

### 🟢 الأساسيات

**المنهج (The method).** ست خطوات (six steps)، والحلقة أهم من أي واحدة منها.

```mermaid
flowchart RL
    S["المواصفة<br/>الهدف والحدود والفحوص<br/>(Spec<br/>goal, limits, checks)"] --> P["الخطة<br/>توافق عليها أنت<br/>(Plan<br/>you approve it)"]
    P --> I["التنفيذ<br/>خطوة صغيرة واحدة<br/>(Implement<br/>one small step)"]
    I --> V["التحقق<br/>الاختبارات والتقييمات<br/>(Verify<br/>tests and evals)"]
    V --> R["مراجعة الفروقات<br/>قائمة الفحص<br/>(Review the diff<br/>checklist)"]
    R --> C["الإيداع<br/>(Commit)"]
    C --> I
    V -.->|"أحمر (red)"| P
    R -.->|"مرفوض (rejected)"| S
```

1. **المواصفة (Spec).** اكتب الهدف (goal) والحدود (limits) والفحوص (checks) التي تثبته قبل أي شيفرة. فإن لم تستطع كتابة الفحوص، فتعلّم أكثر أولًا.
2. **الخطة (Plan).** اطلب خطة واقرأها. الخطة الخاطئة رخيصة الإصلاح؛ أما التنفيذ الخاطئ فليس كذلك.
3. **نفّذ بخطوات صغيرة (Implement in small steps).** سلوك واحد في كل مرة، لتبقى كل مجموعة فروقات (diff) مقروءة.
4. **تحقّق (Verify).** شغّل الاختبارات وحين تهم الجودة شغّل التقييم (eval). فالدليل يتفوق على ملخص الوكيل (agent's summary).
5. **راجع الفروقات (Review the diff)** كما تراجع طلب دمج من زميل، بقائمة الفحص أدناه (checklist below).
6. **أودِع (Commit)** مرة لكل خطوة، برسالة (message) تقول لماذا (says why).

**فيمَ يجيد وأين يفشل (What it is good at, and where it fails).** هو قوي في الشيفرة النمطية (boilerplate)، وهياكل الاختبار (test scaffolding)، وإعادة الهيكلة الآلية (mechanical refactors)، وشرح الشيفرة غير المألوفة. وهو ضعيف في معرفة ما يحتاجه العميل، وفي تفاصيل حزمة التطوير الحالية (فمعرفته تتأخر عن الحزمة)، وفي إبقاء الاختبارات صادقة (فقد يخفف عبارة تحقق (assertion) ليحصل على اللون الأخضر)، وفي ضبط النفس (restraint) (إعادات محاولة وتجريدات وميزات زائدة)، وفي قول «لست متأكدًا».

ضعيف: «اكتب روبوت دردشة لمكتب الخدمة باستخدام Claude.» ⁦⁩ توقّع إطار عمل وصفحة ويب ومعاملات مخمَّنة (guessed parameters). قوي: «أضف `ask(text)` إلى `chat.py`. احتفظ بالسجل. اضبط `max_tokens` على 1024 واختر كتلة النص بحسب النوع. أضف اختبارًا يستخدم `[mock:thinking]`. استخدم المحاكي فقط. ضع الخطة أولًا (Plan first).» إنه يسمّي السلوك والحدود والفحص، فتبقى الفروقات صغيرة.

### 🟡 التعمق أكثر

**CLAUDE.md: ذاكرة المشروع (project memory).** يقرأ Claude Code هذا الملف في بداية الجلسة (session). أبقِه قصيرًا ومحددًا (يقترح التوثيق (documentation) ألا يتجاوز نحو 200 سطر): فالأوامر والاصطلاحات والقواعد تتفوق على النثر (prose). وهذا قالب كامل (complete template) لمشروع وكيل.

```markdown
# CLAUDE.md — Najm Desk agent project

### Purpose
Najm Desk is an AI assistant for the IT Service Desk of Najm Bank (a fictional engagement). Every write action needs a human or a policy gate. Keep code small and commented.

### Commands
- Setup: make setup
- Mock server (offline, free): make mock; make stop when done
- Smoke test: source scripts/use-mock.sh && make hello
- Tests (offline): make test for the lab kit, pytest -q for this repository
- Evals (add the command in Module 12). Real-API runs cost money: only when I say "real API OK" and week-00/NOTES.md records a spending cap

### Conventions
- Python 3.11+, type hints, small functions, comments that explain why.
- The model id comes from the MODEL environment variable (default claude-sonnet-5-5). Never hard-code another.
- Every messages.create call: max_tokens of 1024 or more, the text block chosen by type (never content[0].text), stop_reason handled, no temperature, top_p or top_k.
- Every agent loop has an iteration cap; every tool_use gets a tool_result, all in one user message.
- Prompts live in prompts/ as versioned files; changing one needs an eval run.
- Fictional data only.

### Safety rules
- Never write, print or commit a key. Never read .env.
- Use the mock by default. Ask before any step that calls the real API.
- Never weaken, skip or delete a test to make it pass. If a test looks wrong, stop and explain.
- No eval() or exec() on model output. Ask before adding dependencies or running destructive commands (rm -rf, force push).

### Working style
- Plan first when more than one file is involved, and wait for my approval. Small steps; tests after each.
- Unsure of an SDK parameter? Read the installed package. Never guess.

### Platform facts
(Paste the "Your platform" answers here.)

### Definition of done
Tests pass offline; new behaviour has a test that fails without the change; evals not worse, or explained; no secrets; I have read the diff.
```

**الضوابط المحيطة به (The controls around it).** التعليمات في `CLAUDE.md` طلبات يتبعها النموذج عادةً؛ أما هذه الميزات فيفرضها البرنامج. تتغير الأسماء والإعدادات الافتراضية؛ فراجع التوثيق الحالي (current documentation).

| الضابط (Control) | ما يفعله | كيف تستخدمه في هذه الدورة |
|---|---|---|
| **وضع التخطيط (Plan mode)** | يستكشف ويقترح خطة دون تعديل حتى توافق | أي تغيير يمس أكثر من ملف واحد |
| **الأذونات (Permissions)** | يسأل قبل الأوامر والتعديلات؛ وتتيح قائمة السماح (allow-list) تشغيل الأوامر الروتينية الآمنة | اسمح بالاختبارات والمحاكي و`git diff`؛ وامنع قراءة `.env` والدفع القسري (force pushes). القاعدة ليست بيئة معزولة: أبقِ المفاتيح الحقيقية بعيدة المنال |
| **الخطافات (Hooks)** | أوامر تعمل تلقائيًا عند الأحداث، مثل ما بعد التعديل | شغّل `pytest -q` أو التقييم بعد التعديلات؛ وامنع تعديل `.env` (block edits) |
| **الوكلاء الفرعيون (Subagents)** | مساعدون منفصلون بسياقهم الخاص وحدود أدواتهم (tool limits) | مراجِع للقراءة فقط (read-only reviewer) يُعطى الفروقات وقائمة الفحص (checklist) |
| **خوادم MCP (MCP servers)** | تضيف أدوات أو بيانات خارجية | وصول للقراءة فقط إلى بيئة معزولة أولًا؛ وكل خادم شيفرة تشغّلها ونص يقرؤه النموذج، فافحصه (vet it) |
| **الوضع بلا واجهة (Headless mode)** | تشغيل غير تفاعلي (non-interactive run) (`claude -p`) للسكربتات والتكامل المستمر | تعليقات مراجعة استشارية؛ ولا دمج تلقائي (never auto-merge) أبدًا |

**قالب مواصفة البناء (A build-spec template).** املأه لكل تغيير؛ فكل حقل يزيل طريقة للتخمين.

```text
GOAL: <one sentence: the behaviour someone will see>
WHY: <the customer need>
READ FIRST: <CLAUDE.md and the files to change>

REQUIREMENTS
1. <a behaviour, as Given / When / Then or a short rule>

CONSTRAINTS
- <libraries, SDK rules, files you may touch>. Use the mock; no real API calls.

ACCEPTANCE CHECKS (I will run these)
- <command> -> <expected result>
- A new test that fails without your change and passes with it

DO NOT
- <out-of-scope features, refactors, renames, dependencies>

PROCESS: plan first and wait for my OK; small steps; tests after each; summarise the diff and your doubts.
```

### 🔴 نظرة الخبير

**قائمة فحص المراجِع لشيفرة الوكلاء التي يكتبها وكيل (A reviewer's checklist for agent-written agent code).** عشرة أشياء تبحث عنها.

| ما الذي تبحث عنه (Look for) | لماذا يضرّ | كيف تلتقطه |
|---|---|---|
| **معاملات قديمة أو مخترعة (Stale or invented parameters)** (`temperature` و`budget_tokens` والملء المسبق (prefill) و`tool_choice` القسري) | `TypeError` لوسائط أخذ العينات (sampling arguments) في الإصدار 1.x من حزمة التطوير (1.x SDK)؛ و400 من أحدث النماذج للباقي | شغّله؛ واقرأ توقيع حزمة التطوير (SDK signature) وصفحة النماذج |
| **`content[0].text`** | ينكسر حين تأتي كتلة تفكير أولًا | اختبار `[mock:thinking]`؛ واختر الكتلة بحسب النوع |
| **غياب `max_tokens`، أو غياب سقف للحلقة (no loop cap)** | `TypeError`، أو حلقة منفلتة وفاتورة منفلتة | اقرأ كل `create` وكل `while` |
| **غياب `tool_result` (a missing tool_result)** | 400، أو نموذج يفقد الخيط | نتيجة واحدة لكل معرّف `tool_use`، في رسالة واحدة (one message) |
| **غياب معالجة `stop_reason` (no stop_reason handling)** | يمر دور مقطوع أو مرفوض على أنه إجابة (answer) | اختبر بـ`max_tokens` ضئيل (tiny) |
| **أسرار في الشيفرة (Secrets in code)** | تسريبات (leaks)؛ وتتجاهل بيئتك | فحص الأسرار (secret scan)؛ وابحث عن `sk-ant-` |
| **`eval()` على مخرجات النموذج (on model output)** | يتحول نص النموذج إلى شيفرتك | حلّل (parse) وتحقق (validate) بدلًا من ذلك |
| **إعادات محاولة بلا حدود (Unbounded retries)** | حلقة حول إعادات المحاولة الخاصة بحزمة التطوير تضاعف الاستدعاءات (multiplies calls) | حدّد المحاولات (cap attempts)، وتراجع تدريجيًا (back off)، ولا تعِد محاولة أي خطأ 400 أبدًا (never retry a 400) |
| **أخطاء الذاكرة (Memory mistakes)** | رد لا يُضاف إلى السجل يعني فقدان الذاكرة (amnesia)؛ وسجل لا يُقصّ (trimmed) أبدًا يعني تكلفة ثم تجاوزًا | اطرح سؤال متابعة (follow-up)؛ واختبر بـ`MOCK_CONTEXT_WINDOW` |
| **غياب الاختبارات أو اختبارات المحاكي (No tests, or tests of the mock)** | اللون الأخضر لا يعني شيئًا | اكسر الشيفرة (break the code)؛ ويجب أن يفشل الاختبار |

**هرم التحقق (The verification pyramid).** اصعد من القاعدة الرخيصة (cheap base)؛ ولا تتوقف عند مستوى منخفض حين يهم درج أعلى (higher rung).

1. **الفحوص الساكنة (Static checks)** (المدقّق (linter) والأنواع (types) وفحص الأسرار): عند كل حفظ.
2. **اختبارات الوحدة دون اتصال أمام المحاكي (Offline unit tests against the mock)**: الآليات، عند كل إيداع.
3. **اختبارات العقود (Contract tests)**: تجتاز مخططات الأدوات والمخرجات المهيكلة التحقق من الصحة.
4. **تقييمات على نموذج حقيقي (Evals on a real model)**: الجودة على مجموعة ذهبية (golden set)، وهي تكلّف مالًا (الوحدة 12).
5. **المراجعة البشرية (Human review)** للفروقات وللتتبّعات: دائمًا.
6. **إشارات الإنتاج (Production signals)**: تجربة تشغيلية، ثم المراقبة (monitoring) (الوحدة 15).

للتعمق، انظر [*تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)*، الدرس 9.4 — التحقق قبل إعلان الإنجاز (Verification before completion)](../vibe/index.ar.html#l9-4)، و[*اختبار البرمجيات (Software Testing)*، الدرس 6.1 — التحقق من الشيفرة المولَّدة بالذكاء الاصطناعي: كيف تفشل وكلاء البرمجة وقائمة فحص المراجِع](../testing/index.ar.html#/6.1)، و[*اختبار البرمجيات*، الدرس 6.2 — الاختبارات بوصفها المواصفة لوكلاء البرمجة: سير العمل الذي يبدأ بالاختبار والحواجز الوقائية واختبار الطفرات حَكَمًا](../testing/index.ar.html#/6.2).

**ما لا يمكنك تفويضه (What you cannot delegate).** حين تسأل **هند (Hind)** أو **يارا (Yara)** أو **حمد (Hamad)** أو **ليلى (Layla)**، تجيب أنت دون وجود Claude Code في الغرفة. ماذا يفعل حين يخطئ؟ ما الذي يستطيع تغييره، ومن يوافق؟ إلى أين تذهب بيانات الموظفين (staff data)؟ كيف نعرف أنه يعمل؟ كم تكلّف المحادثة؟ كيف نوقفه؟ وإن لم تستطع أن تشرح سطرًا لـ**يارا**، فلن يُطلَق. ولتوجيه فريق ذكاء اصطناعي كامل، انظر [*تصميم الأنظمة لمبرمجي الفايب*، الدرس 9.1 — أنت المهندس المعماري الآن](../vibe/index.ar.html#l9-1).

**متى لا تفوّض (When not to delegate).** اكتب حلقتك الأولى (first loop) بيدك (الوحدتان 1 و8). وأبقِ القرارات الحرجة أمنيًا (security-critical choices) وبيانات العملاء الحقيقية (real customer data) عند إنسان. ولا تفوّض أبدًا مهمة لا تستطيع أن تصف فحصها.

> **منصتك (Your platform).** على الأرجح ستنشر (deploy) على منصة داخلية (internal platform)، منصتك أو منصة صاحب عملك أو عميلك. لا تملك هذه الدورة تفاصيل عنها ولا تصف أيًّا منها. املأ هذا الجدول مع أصحابها (owners)، ثم الصق الإجابات في `CLAUDE.md` ليكفّ Claude Code عن التخمين (stops guessing).

| السؤال | ما الذي تكتشفه | إجابتك |
|---|---|---|
| **الهوية (Identity)** | كيف يسجّل المستخدمون والخدمات الدخول (sign in)؟ هل يستطيع الوكيل أن يتصرف بصفة المستخدم أم بحساب خدمة (service account) فقط؟ ما أصغر نطاق صلاحية (smallest scope) لكل أداة؟ | |
| **الأسرار (Secrets)** | أين تُخزَّن المفاتيح وتُدوَّر، وكيف يتلقاها الوكيل وقت التشغيل؟ | |
| **وجهة النشر (Deploy target)** | أين تعمل الحاويات (containers) أو الدوال (functions)، ومن يحق له النشر، وكيف تُفصل البيئات (environments) بعضها عن بعض؟ | |
| **قابلية المراقبة (Observability)** | أين تذهب السجلات (logs) والتتبّعات والمقاييس (metrics)، ولكم من الوقت، وهل يجوز أن تحمل الموجّهات والإجابات (answers)؟ | |
| **نظام التذاكر (Ticketing)** | أين تعيش المهام (tasks) والحوادث (incidents) وطلبات التغيير (change requests)، وهل توجد واجهة برمجية (API)؟ | |
| **سير عمل الموافقة (Approval workflow)** | من يعتمد أداة جديدة أو تغيير موجّه أو نموذج، وبأي دليل؟ | |
| **إقامة البيانات (Data residency)** | أين يجوز معالجة الموجّهات والسجلات والتضمينات (embeddings) وتخزينها؟ وهل مزوّد النموذج لديك معتمد لهذه الفئة من البيانات (data class)؟ | |

## 🧰 الأدوات
| الأداة أو الممارسة أو النمط | ما هي وماذا تفعل | متى تلجأ إليها |
|---|---|---|
| **CLAUDE.md** — ملف CLAUDE.md | ذاكرة المشروع: الغرض (purpose) والأوامر والاصطلاحات والقواعد ومعنى الاكتمال | في بداية كل مستودع |
| **Build spec** — مواصفة البناء | الهدف والحدود وفحوص القبول (acceptance checks) وقائمة ما هو خارج النطاق (out-of-scope list) لتغيير واحد | قبل كل طلب إلى Claude Code |
| **Hooks** — الخطافات | أوامر ينفذها البرنامج عند الأحداث (events) | قواعد يجب أن تصمد في كل مرة، مثل الاختبارات بعد التعديلات |
| **Agent code review checklist** — قائمة فحص مراجعة شيفرة الوكلاء | عشرة أشياء تفحصها في شيفرة الوكلاء التي يكتبها وكيل | كل فروقات، بشرية أو بالذكاء الاصطناعي |
| **Verification pyramid** — هرم التحقق | فحوص ساكنة (static)، وفحوص دون اتصال، وفحوص العقود (contract)، والتقييم، والمراجعة البشرية (human)، والإنتاج (production) | لتقرر كم من الدليل يحتاج التغيير |

## 🏛️ عمليًا في بنك نجم
قاعدة **فهد**: لا يُدمج شيء كتبه وكيل دون قراءة. مُخرَجاتك هي `CLAUDE.md`، وقائمة الفحص بوصفها قالب طلب دمج (pull-request template)، ومراجعة أولى (first review). كتب وكيل **لجين** هذا `chat.py`. إنه يعمل ويبدو سليمًا، وفيه خمسة عيوب مزروعة (إضافة إلى ثغرات عادية (ordinary gaps)، مثل غياب فحص `stop_reason`، يمكنك أن تسردها إضافات). اقرأه بصفتك المراجِع.

```python
# labs/m00/flawed_chat.py
"""chat.py for Najm Desk, as an AI coding agent wrote it. It looks tidy and confident. It has FIVE flaws.
Exercise 0.3: find them by reading, then prove each with labkit/tests/test_m00_flawed_chat.py.
Do not fix this file. Copy it into your own repo and fix the copy."""
import os

from anthropic import Anthropic

# Simple and reliable: the client is ready to use as soon as the module loads.
client = Anthropic(api_key="sk-ant-EXERCISE-NOT-A-REAL-KEY-0000")

MODEL = os.environ.get("MODEL", "claude-sonnet-5-5")
SYSTEM = "You are Najm Desk, an assistant for the Najm Bank IT Service Desk. Answer briefly. If unsure, say so."

history = []                                     # the conversation so far


def ask(user_text: str) -> str:
    """Send one user message and return the model's reply."""
    history.append({"role": "user", "content": user_text})
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        messages=history,
    )
    reply = resp.content[0].text                 # the reply is the first block
    print(f"[tokens in={resp.usage.input_tokens} out={resp.usage.output_tokens}]")
    return reply


def brainstorm(topic: str) -> str:
    """Looser, more varied wording for the /ideas command."""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        temperature=1.0,                         # more variety for brainstorming
        messages=[{"role": "user", "content": f"Give me three ideas for: {topic}"}],
    )
    return next(b.text for b in resp.content if b.type == "text")


def summarise_history() -> str:
    """Squeeze a long conversation into three bullet points for the /summary command."""
    resp = client.messages.create(
        model=MODEL,
        system="Summarise this conversation in three bullet points.",
        messages=history,
    )
    return next(b.text for b in resp.content if b.type == "text")


if __name__ == "__main__":
    while True:
        line = input("you> ").strip()
        if line in ("exit", "quit"):
            break
        if line.startswith("/ideas "):
            print("bot>", brainstorm(line[7:]))
        elif line == "/summary":
            print("bot>", summarise_history())
        else:
            print("bot>", ask(line))
```

تُثبت الاختبارات في `labkit/tests/test_m00_flawed_chat.py` كل عيب أمام الإصدار 1.x من حزمة التطوير أو المحاكي (prove each flaw against the 1.x SDK or the mock)؛ ولترى فقدان الذاكرة، شغّل المحاكي بالخيار `--playbook playbooks/m00_flawed_chat.json` واسأل ⁦"How do I request a laptop?"⁩ (أي: كيف أطلب حاسوبًا محمولًا؟) ثم ⁦"And how long does it take?"⁩ (أي: وكم يستغرق ذلك؟).

**ما الذي يستطيع المحاكي إظهاره هنا وما لا يستطيع (What the mock can and cannot show here).** تأتي أخطاء `TypeError` من الإصدار الحقيقي 1.x من حزمة التطوير (real 1.x SDK)؛ أما كتلة التفكير وفقدان الذاكرة فمن ردود المحاكي المبرمجة مسبقًا (scripted replies). ولا يستطيع أن يُظهر الأثر الحقيقي للعيب 1 (flaw 1) (وهو 401؛ **يحتاج الواجهة البرمجية الحقيقية (Needs the real API)**) ولا ما إذا كان نموذج حقيقي يجيب جيدًا. وقد يتخطى نموذج حقيقي كتلة التفكير في موجّه معين، وهكذا يختبئ العيب 2 (flaw 2) في العروض التجريبية.

**مُسلَّم الأسبوع 0، مكتملًا (Week 0 deliverable, complete).** في `week-00/`: ملف `NOTES.md` من الدرس 0.2 ومخرجاته؛ وملف `review.md` يضم العيوب الخمسة (five flaws)؛ ومواصفة التمرين 🔴 ومراجعة فروقاته؛ وجدول المنصة (platform table)؛ وفي جذر المستودع (repository root) ملف `CLAUDE.md` الخاص بك.

**جلسة المجموعة، من 60 إلى 90 دقيقة (Group session, 60 to 90 minutes).** يعرض قائد العرض `hello.py` في الوضعين (both modes) (10 دقائق). ويسمّي كل عضو العيب الذي وجده أسرع؛ وتُشغَّل الاختبارات معًا (20). وتتبادلون ملفات `CLAUDE.md` وتتبنون أفضل ثلاث قواعد (15). وتراجعون فروقات أحد المتطوعين مباشرة (20). وتسردون ثغرات جدول المنصة (platform-table gaps) (10).

## 🛠️ التمارين
- 🟢 **ابحث عن العيوب الخمسة (Find the five flaws).** اقرأ `flawed_chat.py` بصفتك مراجِعًا قبل تشغيل أي شيء، ثم شغّل اختباراته. *يكتمل عندما:* يسرد `review.md` خمسة عيوب، لكل منها السطر والعَرَض وبند قائمة الفحص (checklist item) والإصلاح (fix)؛ وتنجح الاختبارات مثبتةً كل عيب؛ وتحتوي نسختك المصلحة (fixed copy) على اختبار كان سيلتقط أحدها. لا حاجة إلى واجهة حقيقية.
- 🟡 **اكتب `CLAUDE.md` لمستودع الدورة (Write CLAUDE.md for the course repository).** كيّف القالب مع مستودعك وإجاباتك عن المنصة (platform answers). *يكتمل عندما:* يقل عن 60 سطرًا (under 60 lines)، وكل أمر يعمل، وتتبّع جلسة Claude Code جديدة ثلاث قواعد دون تذكير (unprompted) (لا معاملات أخذ العينات، والمحاكي افتراضيًا، والسؤال قبل استخدام الواجهة الحقيقية). يحتاج Claude Code لا مفتاح واجهة المختبر.
- 🔴 **المواصفة والفروقات والمراجعة (Spec, diff, review).** استخدم القالب لتجعل Claude Code يضيف أمر `/cost` إلى محادثتك المصلحة، يطبع المجموع الجاري للرموز وكذلك التكلفة إن ضُبطت متغيرات الأسعار. راجع الفروقات مقابل البنود العشرة كلها. *يكتمل عندما:* تحتوي المواصفة على فحوص قبول، ولكل بند نجاح أو فشل (pass or fail) مع رقم سطر (line number)، وقد طلبت تغييرًا واحدًا على الأقل، ويفشل اختبار من دون الميزة، وتقول رسالة الإيداع (commit message) لماذا. يحتاج Claude Code؛ ويكفي المحاكي.

## ⚠️ أخطاء وفخاخ
- **قبول اختبارات خضراء لم تقرأها (Accepting green tests you have not read).** قد تختبر المحاكي، أو لا شيء. اكسر الشيفرة عمدًا وشاهد الاختبار يفشل.
- **طلب غامض (A vague request).** عبارة «ابنِ روبوت دردشة» تشتري لك تطبيقًا مبالغًا في بنائه (over-built app) بمعاملات مخمَّنة. استخدم القالب.
- **ملف `CLAUDE.md` من الأمنيات (A CLAUDE.md of wishes).** النثر الطويل يُتجاهل. أبقِ القواعد قصيرة؛ وضع القواعد الواجبة الصمود (must-hold rules) في الخطافات.
- **أذونات واسعة (Broad permissions).** الوصول إلى الواجهة الحقيقية دون إشراف أو بيانات اعتماد الإنتاج (production credentials) أو الأوامر المدمّرة (destructive commands) تصنع قصصًا مثل قاعدة البيانات المحذوفة. ضيّق قائمة السماح (allow-list narrowly).

## 🧾 الخلاصة
- المنهج هو المواصفة والخطة وخطوات صغيرة والتحقق ومراجعة الفروقات والإيداع.
- يخترع Claude Code معاملات (invents parameters) ويُضعف الاختبارات (weakens tests) ويبالغ في البناء (over-builds)، ولذا تراجع كل شيء.
- يذكر `CLAUDE.md` القواعد؛ وتفرضها الخطافات والأذونات. راجع التوثيق الحالي.
- الاختبارات دون اتصال (offline tests) تثبت الآليات، والتقييمات تثبت الجودة؛ فاستخدم قائمة الفحص والهرم.
- يجب أن تشرح كل سطر للعميل؛ ويحمل جدول المنصة حقائق لا يستطيع Claude Code تخمينها (cannot guess).

## ✍️ اختبر نفسك

**1. يعيد Claude Code دالة `ask()` تقرأ `resp.content[0].text`، وتنجح اختباراتها على المحاكي (mock tests). ماذا ينبغي أن تفعل؟**

- A. اقبلها، لأن الاختبارات الخضراء (green tests) تعني أن الشيفرة صحيحة وآمنة
- B. لفّ الوصول إلى الخاصية في كتلة try
- C. اختر كتلة النص بحسب النوع؛ وأضف اختبار `[mock:thinking]`
- D. انتقل إلى نموذج لا يُخرج كتل تفكير (thinking blocks) أبدًا

<details><summary>الإجابة</summary>

**C.** لم يرسل أي اختبار ردًّا يبدأ بكتلة تفكير (thinking block)، فلم يثبت اللون الأخضر إلا القليل؛ وكتلة try ستخفي الخطأ. (🔴 قائمة الفحص (Checklist).)

</details>

**2. ليجعل اختبارًا فاشلًا ينجح (to make a failing test pass)، يغيّر الوكيل (agent) `assert status == "Closed"` إلى `assert status`. ماذا تفعل؟**

- A. ارفضه، واعرف لماذا فشل، ثم أصلح الشيفرة أو المواصفة
- B. اقبله، لأن مجموعة الاختبارات (suite) صارت خضراء وسينجح التكامل المستمر (CI)
- C. اقبله إن شرحت رسالة الإيداع (commit message) عبارة التحقق المخففة (loosened assertion)
- D. اطلب من الوكيل (agent) أن يخفف الاختبارات الأخرى بالطريقة نفسها

<details><summary>الإجابة</summary>

**A.** عبارة التحقق المخففة (loosened assertion) تخفي فشلًا حقيقيًا (real failure). (🟢 أين يفشل.)

</details>

**3. يقول `CLAUDE.md` الخاص بك «شغّل الاختبارات بعد كل تعديل» ("run the tests after every edit")، ومع ذلك يتخطاها الوكيل (agent) أحيانًا. ما أوثق حل (most reliable fix)؟**

- A. أعد كتابة القاعدة بأحرف كبيرة (capital letters) في أعلى الملف
- B. كرّر القاعدة نفسها (same rule) في نهاية الملف أيضًا
- C. انتقل إلى نموذج أكبر (larger model) في كل جلسة
- D. أضف خطافًا (hook) يشغّل الاختبارات بعد كل تعديل

<details><summary>الإجابة</summary>

**D.** التعليمات طلبات؛ أما الخطاف فيشغّله البرنامج في كل مرة. راجع التوثيق (docs) لتعرف كيف تضبط واحدًا. (🟡 الضوابط.)

</details>

**4. يجد مراجِع `while True:` حول استدعاء نموذج (model call) وتشغيلات أدوات (tool runs)، بلا عدّاد، وإحدى الأدوات تخطئ كثيرًا. أي ملاحظة هي الأهم؟**

- A. معاملات مخترعة (invented parameters): أزل الوسائط الزائدة الآن
- B. غياب حد الحلقة: أضف حدًّا صارمًا للتكرارات
- C. خطأ في الذاكرة (memory mistake): قصّ السجل
- D. غياب الاختبارات: اكتب اختبار وحدة (unit test) أولًا

<details><summary>الإجابة</summary>

**B.** قد تُبقي الأداة الفاشلة (failing tool) الحلقة تدور والفاتورة تتصاعد؛ والحد الصارم (hard cap) يأتي أولًا. (🔴 قائمة الفحص (Checklist).)

</details>

**5. تسألك هند كيف تعرف أن نجم ديسك (Najm Desk) يجيب عن أسئلة السياسات (policy questions) إجابة صحيحة. فتقول إن Claude Code كتب اختبارات وهي تنجح. ما الذي ينقص؟**

- A. لا شيء، لأن الاختبارات الناجحة (passing tests) تثبت صحة الإجابات
- B. `CLAUDE.md` أطول وفيه قواعد أكثر بكثير للوكيل
- C. تقييم على نموذج حقيقي (real-model eval) فوق مجموعة ذهبية من الأسئلة
- D. مراجعة ثانية من Claude Code للاختبارات الناجحة نفسها قبل كل دمج

<details><summary>الإجابة</summary>

**C.** الاختبارات دون اتصال (offline tests) تثبت الآليات (mechanics) لا جودة الإجابات (answer quality). وتحتاج الجودة إلى تقييم (eval) على نموذج حقيقي تستطيع شرحه. (🔴 الهرم.)

</details>

## 📚 المراجع
- نظرة عامة على Claude Code (Claude Code overview) — https://code.claude.com/docs/en/overview
- ذاكرة Claude Code (CLAUDE.md) — https://code.claude.com/docs/en/memory
- خطافات Claude Code — https://code.claude.com/docs/en/hooks
- مستودع Claude Code — https://github.com/anthropics/claude-code
- [*تصميم الأنظمة لمبرمجي الفايب*، الدرس 9.5 — تقنيات Claude Code المتقدمة (Claude Code power techniques)](../vibe/index.ar.html#l9-5)
- [*دليل عملي لتصبح مهندسًا أصيلًا في الذكاء الاصطناعي*، الدرس 0.3 — الحلقة الأصيلة في الذكاء الاصطناعي: حدِّد وفوِّض وتحقّق وادمج (specify, delegate, verify, integrate)، ومن يبقى مسؤولًا](../ainative/index.ar.html#/0.3) — منظور الهندسة اليومية الأصيلة في الذكاء الاصطناعي (AI-native engineering) لهذا الموضوع
- [*دليل عملي لتصبح مهندسًا أصيلًا في الذكاء الاصطناعي*، الدرس 4.1 — استكشف وخطّط ونفّذ وافحص وأودِع: الخطوات الصغيرة ونقاط الاستعادة ومتى تتولى القيادة](../ainative/index.ar.html#/4.1) — منظور الهندسة اليومية الأصيلة في الذكاء الاصطناعي لهذا الموضوع
