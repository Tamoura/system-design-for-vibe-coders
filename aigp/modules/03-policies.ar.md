# الوحدة (Module) 3 — السياسات عبر دورة الحياة (Policies across the life cycle)

*منحت الوحدة (Module) 2 بنك نجم (Najm Bank) مبادئ (principles)، وشهية مخاطر (risk appetite)، وأشخاصًا يملكون مخاطر الذكاء الاصطناعي (AI risk). أما هذه الوحدة فتمنح هؤلاء الأشخاص قواعد يتبعونها. يرسم الدرس (Lesson) 3.1 خريطة دورة حياة (life cycle) الذكاء الاصطناعي (AI) ومنظومة السياسات والإجراءات (policy stack) التي تحكم كل مرحلة (stage) منها، من سياسة الذكاء الاصطناعي (AI policy) العليا وصولًا إلى عملية الاستثناءات (exception process). ويتناول الدرس 3.2 مجالَي السياسات (policies) اللذين تتعثر فيهما المؤسسات أكثر من غيرهما: حوكمة البيانات للذكاء الاصطناعي (data governance for AI) (المصدر (provenance)، والجودة (quality)، والاحتفاظ (retention)، والاستخدام المشروع (lawful use))، والملكية الفكرية (intellectual property) (الحقوق في بيانات التدريب (rights to training data)، وملكية المخرجات (ownership of outputs)، والمعلومات السرية في الأوامر النصية (confidential information in prompts)). ويعالج الدرس 3.3 حقيقة أن معظم أنظمة الذكاء الاصطناعي (AI systems) في نجم لا تُبنى داخليًا: منتجات الموردين (vendor products)، وواجهات برمجة التطبيقات (APIs) للنماذج الأساسية (foundation models)، والنماذج مفتوحة المصدر (open-source models)، وما تحتاجه من العناية الواجبة (due diligence) والعقود (contracts) والرصد (monitoring). هذه الدورة تعليمية وليست استشارة قانونية (legal advice).*

> **التغطية ضمن مجال المعرفة (BoK coverage):** I.C — السياسات والإجراءات (policies and procedures) التي تحكم الذكاء الاصطناعي (AI) عبر دورة حياته (its life cycle)، بما في ذلك حوكمة البيانات (data governance) والملكية الفكرية (intellectual property) ومخاطر الطرف الثالث (third-party risk).

---

# 3.1 — دورة حياة الذكاء الاصطناعي (AI life cycle) ومنظومة السياسات (policy stack)
*المستوى: 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 2.1، 2.2* · *مجال المعرفة (BoK): I.C*

## ⚡ الدرس في دقيقة (In 60 seconds)
- تمتد **دورة حياة الذكاء الاصطناعي (AI life cycle)** من التخطيط والتصميم (plan and design)، مرورًا ببناء البيانات والنموذج (data and model building)، والتحقق والمصادقة (verify and validate)، والنشر (deployment)، والتشغيل والرصد (operate and monitor)، وصولًا إلى الإيقاف والتقاعد (retirement). وتنطبق الحوكمة (governance) على كل مرحلة (stage)، لا عند الإطلاق (launch) فقط.
- المراجع القياسية لدورة الحياة (Standard life-cycle references): مراحل دورة الحياة (life-cycle stages) لدى **OECD** و**NIST AI RMF**، و**ISO/IEC 22989** (المفاهيم والمراحل (concepts and stages))، و**ISO/IEC 5338** (عمليات دورة الحياة (life-cycle processes)).
- تتكوّن **منظومة السياسات (policy stack)** من طبقات: سياسة الذكاء الاصطناعي (المبادئ (principles) والنطاق والأدوار (roles))، وسياسة الاستخدام المقبول / الذكاء الاصطناعي التوليدي (acceptable-use / GenAI policy) (ما يجوز للموظفين فعله)، وإجراء سجل الأنظمة وتصنيف المخاطر (inventory and risk-classification procedure)، ومعايير إدارة مخاطر النماذج (model risk management standards)، وعملية الاستثناءات (exception process).
- السياسات (policies) تقول *ماذا* و*لماذا*؛ والمعايير (standards) تحدد *الحد الأدنى من المتطلبات (minimum requirements)*؛ والإجراءات (procedures) تقول *كيف*؛ والإرشادات (guidelines) تقدّم النصح. حافظ على تمايز هذه الطبقات.
- إشارة الامتحان (Exam cue): سجل أنظمة الذكاء الاصطناعي (AI inventory) هو الأساس. إذا سأل سيناريو عمّا تحتاجه المؤسسة قبل أن تتمكن من حوكمة (governance) ذكائها الاصطناعي، فالإجابة (Answer) غالبًا هي السجل (والتصنيف (classification)).
- الفخ الأكبر (Biggest trap): نهج "بوابة الإطلاق فقط (launch gate only)". فالمخاطر التي تنشأ في مرحلتي التصميم أو البيانات (design or data stages)، والانجراف (drift) بعد النشر (deployment)، تفلت من بوابة واحدة (single gate).

## 🧭 لماذا يهم (Why it matters)
بُنيت الضوابط القائمة (existing controls) في بنك نجم (Najm Bank) للبرمجيات التقليدية (traditional software): مجلس استشاري للتغيير (change advisory board) يوافق على الإصدارات (releases)، وفريق مخاطر النماذج (model risk team) يصادق على النماذج الإحصائية (statistical models) المستخدمة في حسابات رأس المال (capital calculations). وحين تطابق ليلى مساعد الائتمان (credit copilot)، وهو أداة ذكاء اصطناعي توليدي (GenAI tool) تصوغ مذكرات الائتمان لمديري العلاقات (relationship managers)، مع تلك الضوابط (controls)، تظهر الثغرات (gaps) جلية. لم يراجع أحد قرار السماح له بقراءة القوائم المالية للعملاء (وهو خيار تصميمي (design choice)). ولم يتحقق أحد من ترخيص مستندات الاسترجاع (licence of the retrieval documents) التي يفهرسها (وهو خيار يتعلق بالبيانات (data)). وكان "إصداره" تعديلًا على الأمر النصي (prompt) دُفع بعد ظهر يوم ثلاثاء، ولم يمرّ قط على المجلس الاستشاري للتغيير. ولا أحد يراقب ما إذا كانت ملخّصاته تسوء كلما حدّث مزوّد النموذج الأساسي (underlying model provider) نموذجه (وهي ثغرة في الرصد (monitoring gap)).

تقع كل ثغرة من هذه الثغرات (gaps) عند نقطة مختلفة من دورة الحياة (life cycle)، وتحتاج كل منها إلى قاعدة مختلفة. ولهذا تُكثر أطر حوكمة الذكاء الاصطناعي (AI governance frameworks) من الحديث عن دورة الحياة، ولهذا لا تكفي وثيقة واحدة بعنوان "سياسة الذكاء الاصطناعي (AI policy)" وحدها أبدًا.

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**دورة حياة الذكاء الاصطناعي (AI life cycle).** ترسم الأطر (frameworks) المختلفة المراحل (stages) بصورة مختلفة قليلًا، لكنها تصف الرحلة نفسها. وهذه خلاصة عملية (practical synthesis):

| المرحلة (stage) | ما يحدث | أسئلة الحوكمة المعتادة (Typical governance questions) |
|---|---|---|
| 1. التخطيط والتصميم (plan and design) | تحديد المشكلة، والغرض المقصود (intended purpose)، والمستخدمين (users) والأشخاص المتأثرين (affected people)؛ وتقرير ما إذا كان الذكاء الاصطناعي (AI) هو الأداة المناسبة | هل حالة الاستخدام (use case) هذه مسموح (Allowed) بها؟ ما فئة المخاطر (risk tier)؟ من يملكها؟ |
| 2. جمع البيانات ومعالجتها (collect and process data) | الحصول على البيانات ووسمها وتنظيفها وتوثيقها (Source, label, clean and document data) | هل لدينا حقوق استخدامها (rights to use it)؟ هل هي ممثِّلة (representative) وذات جودة جيدة (of good quality)؟ هل تتضمن بيانات شخصية (personal data)؟ |
| 3. البناء والتدريب (build and train) | اختيار النموذج أو تدريبه (Select or train the model)؛ وفي الذكاء الاصطناعي التوليدي (GenAI)، اختيار نموذج أساسي (foundation model) وأوامر نصية (prompts) ومصادر استرجاع (retrieval sources) | نبني أم نشتري (Build or buy)؟ هل خيارات التصميم موثّقة (Documented design choices)؟ |
| 4. التحقق والمصادقة (verify and validate) | اختبار الأداء والمتانة (robustness) والعدالة (fairness) والأمن (security)؛ ومصادقة مستقلة للفئة العليا (independent validation for high-tier) | هل يستوفي معايير القبول (acceptance criteria) التي حُددت في التصميم (design)؟ |
| 5. النشر (deployment) | الدمج (integration) في العمليات التجارية (business processes)، وتدريب المستخدمين (User training)، والإطلاق (launch) | هل اكتملت الموافقات (Approvals)؟ هل توجد شفافية تجاه المستخدمين (users)؟ هل الإشراف مزوّد بالموظفين (Oversight staffed)؟ |
| 6. التشغيل والرصد (operate and monitor) | تتبّع الأداء والانجراف (drift) والحوادث (incidents) والشكاوى (complaints) والتغييرات من الموردين (changes from vendors) | هل ما زال ضمن حدود التحمّل (within tolerance)؟ من يستجيب للتنبيهات (alerts)؟ |
| 7. الإيقاف والتقاعد (retirement) | الإيقاف (decommission)، وأرشفة الوثائق (archive documentation)، والتعامل مع البيانات (data)، وإبلاغ المستخدمين (tell users) | ماذا يحدث للبيانات (data) وللقرارات التي اتُّخذت بالفعل؟ |

يستخدم **NIST AI RMF** تسلسلًا مشابهًا (التخطيط والتصميم (plan and design)؛ جمع البيانات ومعالجتها (collect and process data)؛ بناء النموذج واستخدامه (build and use model)؛ التحقق والمصادقة (verify and validate)؛ النشر والاستخدام (deploy and use)؛ التشغيل والرصد (operate and monitor)) ويضيف الأشخاص "الذين يستخدمون النظام أو يتأثرون به". وتصف **OECD** مراحل مماثلة وتؤكد أنها تكرارية لا خطية (iterative, not linear). ويعرّف **ISO/IEC 22989** مفاهيم الذكاء الاصطناعي (AI concepts) ويصف مراحل دورة الحياة (life-cycle stages) من النشأة (inception) حتى الإيقاف والتقاعد (retirement)، ويحدد **ISO/IEC 5338** عمليات دورة حياة أنظمة الذكاء الاصطناعي (AI system life-cycle processes)، مبنيةً على المعايير (standards) الراسخة لعمليات هندسة الأنظمة والبرمجيات (systems and software engineering). ويتوقع امتحان AIGP منك أن تتعرّف على هذه المراحل (stages) وأن تضع أنشطة الحوكمة (governance activities) في موضعها منها.

```mermaid
flowchart RL
    P[التخطيط والتصميم] --> D[البيانات]
    D --> B[البناء]
    B --> V[التحقق والمصادقة]
    V --> Dep[النشر]
    Dep --> O[التشغيل والرصد]
    O -->|تغيير أو انجراف| P
    O --> R[الإيقاف والتقاعد]
```

للحلقة العائدة من الرصد (monitoring) إلى التصميم (design) أهميتها: فأنظمة الذكاء الاصطناعي (AI systems) تتغيّر بعد الإطلاق (launch)، عبر إعادة التدريب (retraining)، أو تحديثات نماذج الموردين (vendor model updates)، أو التحولات في البيانات (data) التي تتعامل معها.

**منظومة السياسات (policy stack).** تأتي وثائق الحوكمة (Governance documents) في طبقات. واستخدام المصطلحات بدقة يجنّب الالتباس لاحقًا:

- **السياسة (Policy):** بيان قصير (short statement) يعتمده مجلس الإدارة (board) أو الإدارة التنفيذية (management)، يحدد النية والنطاق والمبادئ والأدوار (intent, scope, principles and roles). ونادرًا ما يتغيّر.
- **المعيار (Standard):** متطلبات دنيا إلزامية (mandatory minimum requirements)، تقنية في الغالب (مثلًا: "يجب أن يكون للنماذج (models) عالية الفئة (high-tier) اختبار عدالة موثّق (documented fairness testing) باستخدام مقاييس معتمدة (approved metrics)").
- **الإجراء (Procedure):** تعليمات خطوة بخطوة (step-by-step instructions) لعملية ما (كيفية تسجيل حالة استخدام (use case)، وكيفية طلب استثناء (exception)).
- **الإرشاد (Guideline):** ممارسة موصى بها (recommended practice)، غير إلزامية (دليل لكتابة الأوامر النصية (prompt-writing guide)).

تبدو منظومة سياسات الذكاء الاصطناعي (AI policy stack) في بنك نجم على هذا النحو:

| الوثيقة (Document) | النوع | ما تغطيه (What it covers) | المالك (owner) |
|---|---|---|---|
| سياسة الذكاء الاصطناعي (AI policy) | سياسة (policy) | المبادئ (principles)، والنطاق، وتعريف "نظام الذكاء الاصطناعي" (definition of "AI system")، والأدوار (roles)، والنهج القائم على المخاطر (risk-based approach)، والروابط مع السياسات الأخرى (links to other policies) | رئيس حوكمة الذكاء الاصطناعي (Head of AI Governance)، باعتماد لجنة المخاطر في مجلس الإدارة (board risk committee) |
| سياسة الاستخدام المقبول للذكاء الاصطناعي / الذكاء الاصطناعي التوليدي (Acceptable Use of AI / GenAI Policy) | سياسة (policy) | ما يجوز وما لا يجوز لجميع الموظفين فعله بأدوات الذكاء الاصطناعي (AI tools)؛ والأدوات المعتمدة (approved tools)؛ وقواعد البيانات (data rules) | رئيس حوكمة الذكاء الاصطناعي (Head of AI Governance) مع رئيس أمن المعلومات (CISO) |
| إجراء سجل أنظمة الذكاء الاصطناعي وتصنيف المخاطر (AI Inventory and Risk Classification Procedure) | إجراء | كيفية تسجيل حالات الاستخدام (use cases) وتصنيفها في فئات (tiered) وإعادة تصنيفها (re-tiered) | رئيس حوكمة الذكاء الاصطناعي (Head of AI Governance) |
| معيار دورة حياة الذكاء الاصطناعي (AI Life-cycle Standard) | معيار (standard) | الحد الأدنى من الضوابط (Minimum controls) لكل فئة (per tier) في كل مرحلة (stage) من دورة الحياة (life cycle) | رئيس حوكمة الذكاء الاصطناعي (Head of AI Governance) |
| معيار إدارة مخاطر النماذج (الموسَّع ليشمل الذكاء الاصطناعي (AI)) | معيار (standard) | المصادقة (validation)، ورصد الأداء (performance monitoring)، وتغيير النماذج (model change) | رئيس مخاطر النماذج (Head of Model Risk) |
| إجراء استثناءات الذكاء الاصطناعي (AI Exception Procedure) | إجراء | كيفية طلب الاستثناءات (exceptions) والموافقة (approval) عليها وتسجيلها وإنهاء صلاحيتها | رئيس حوكمة الذكاء الاصطناعي (Head of AI Governance) |
| مرتبطة (Linked): حوكمة البيانات (data governance)، والخصوصية (privacy)، وأمن المعلومات (information security)، ومخاطر الطرف الثالث (third-party risk)، والاحتفاظ بالسجلات (keeping records) | سياسات قائمة (Existing policies) | محدَّثة ببنود خاصة بالذكاء الاصطناعي (انظر 3.2 و3.3) | مالكوها الحاليون (Their existing owners) |

### 🟡 التعمق أكثر (Going deeper)

**ما الذي تتضمنه سياسة الذكاء الاصطناعي (AI policy).** تكون سياسة الذكاء الاصطناعي (the AI policy) القوية قصيرة عادةً (بضع صفحات) وتتضمن:

1. **الغرض والنطاق (Purpose and scope):** الكيانات (entities) والمناطق الجغرافية (geographies) والأنظمة التي تشملها، بما في ذلك الذكاء الاصطناعي (AI) المشترى والمدمج (bought and embedded)، لا النماذج المبنية داخليًا (models built in-house) فقط.
2. **تعريف نظام الذكاء الاصطناعي (Definition of AI system):** تتوافق مؤسسات كثيرة مع تعريف OECD (المحدَّث في نوفمبر 2023)، وهو أيضًا أساس التعريف الوارد في قانون الذكاء الاصطناعي الأوروبي (EU AI Act). والتعريف الواضح (clear definition) يمنع حجج "إنها مجرد تحليلات (analytics)".
3. **المبادئ (principles):** المبادئ المعتمدة من الدرس (Lesson) 2.1.
4. **النهج القائم على المخاطر (risk-based approach):** تُسجَّل كل حالة استخدام (use case) للذكاء الاصطناعي (AI) وتُصنَّف في فئة (tiered)؛ وتتدرج الضوابط (controls scale) بحسب الفئة (by tier)؛ وبعض الاستخدامات (uses) محظورة تمامًا (مثلًا: كل ما تحظره المادة 5 (Art. 5) من EU AI Act، إضافة إلى الخطوط الحمراء (red lines) الخاصة بالبنك).
5. **الأدوار والمساءلة (accountability):** مالك العمل (business owner)، وقائد الحوكمة (governance lead)، واللجنة (committee)، والخطوط الثلاثة (three lines).
6. **العمليات الإلزامية (Mandatory processes):** الاستقبال (intake)، وتقييمات الأثر (impact assessments)، والمصادقة (validation)، والموافقة (approval)، والرصد (monitoring)، والإبلاغ عن الحوادث (incident reporting)، والإيقاف والتقاعد (retirement).
7. **السياسات ذات الصلة (Related policies)** وكيفية حل التعارض بينها.
8. **الاستثناءات والمخالفات وعواقبها (Exceptions, breaches and consequences).**
9. **دورة المراجعة (Review cycle):** سنويًا على الأقل، وعند أي تغيير قانوني أو تقني كبير.

**سياسة الاستخدام المقبول / الذكاء الاصطناعي التوليدي (acceptable-use / GenAI policy).** هذه هي السياسة (policy) التي سيقرؤها معظم الموظفين فعلًا. ويجب أن تكون ملموسة: ما الأدوات المعتمدة (مثلًا: بيئة الذكاء الاصطناعي التوليدي المؤسسية (enterprise GenAI tenant) الخاصة بالبنك، حيث يحظر عقد المورد (vendor contract) التدريب (training) على مدخلات نجم (Najm's inputs))؛ وما الأدوات المحظورة (الحسابات الاستهلاكية (consumer accounts) للأدوات العامة (public tools) لأي بيانات مصرفية (bank data))؛ وما فئات البيانات (data categories) التي يجوز إدخالها وأين؛ وواجب التحقق من المخرجات (duty to check outputs) قبل الاعتماد عليها؛ وقواعد الإفصاح (متى يُبلَّغ العميل بأن الذكاء الاصطناعي (AI) استُخدم)؛ وكيفية طلب أداة جديدة. أما الحظر المطلق (Absolute bans) للذكاء الاصطناعي التوليدي (GenAI) فيميل إلى الفشل ويدفع الاستخدام إلى الظل (shadows)؛ والقنوات المعتمدة (approved channels) الواضحة مع قواعد البيانات (data rules) تنجح أكثر.

**إجراء السجل والتصنيف (inventory and classification procedure).** لا يمكنك حوكمة ما لا تراه (You cannot govern what you cannot see). السجل (inventory) قائمة بكل نظام ذكاء اصطناعي (AI system) قيد الاستخدام أو التطوير، يتضمن في حده الأدنى: معرّفًا فريدًا (unique ID)، والاسم والوصف (name and description)، والغرض المقصود (intended purpose)، ومالك العمل (business owner)، ومرحلة دورة الحياة (life-cycle stage)، وما إذا كان مبنيًا (built) أو مشترى (bought) أو مدمجًا (embedded)، وتفاصيل المورد والنموذج (vendor and model details)، وفئات البيانات (data categories) المستخدمة (بما في ذلك البيانات الشخصية (personal data) وبيانات الفئات الخاصة (special-category data))، والأشخاص المتأثرين (affected people)، والولايات القضائية (jurisdictions)، وفئة المخاطر (risk tier) وسببها، وتصنيف EU AI Act (EU AI Act classification) ودور المؤسسة (مقدّم النظام (provider) أو المُشغِّل (deployer))، والتقييمات المنجزة (assessments completed)، وحالة الموافقة (approval status)، وتاريخ المراجعة التالية (next review date). ويوضح الإجراء من يجب عليه التسجيل (كل من يبدأ حالة استخدام (use case) للذكاء الاصطناعي (AI)، وقسم المشتريات (procurement) لأي عملية شراء (purchase) تتضمن ذكاءً اصطناعيًا)، وكيف يجري التصنيف (استبيان (questionnaire) يقيّمه فريق الحوكمة (governance team))، ومتى تُستدعى إعادة التصنيف (تغيّر الغرض أو البيانات (data) أو المستخدمين (users) أو الولاية القضائية (jurisdiction) أو النموذج (model)).

إن العثور على الذكاء الاصطناعي القائم (existing AI) مشروع بحد ذاته: استطلع وحدات العمل (business units)، وافحص سجلات المشتريات (procurement records) ومطالبات النفقات (expense claims) بحثًا عن اشتراكات (subscriptions) في أدوات ذكاء اصطناعي (AI)، واسأل الموردين (vendors) عمّا إذا كانت منتجاتهم تتضمن ميزات ذكاء اصطناعي (AI features)، وتحقق من سجلات الشبكة (network logs) بحثًا عن حركة مرور (traffic) إلى خدمات الذكاء الاصطناعي العامة (public AI services).

**إدارة مخاطر النماذج (model risk management).** لدى البنوك أصلًا تخصصات لإدارة مخاطر النماذج (model risk management - MRM)، والجهات الرقابية (regulators) تتوقع أن تشمل نماذج الذكاء الاصطناعي (AI models). ففي الولايات المتحدة، تضع الإرشادات الرقابية (supervisory guidance) SR 11-7 (2011) توقعات بتطوير متين للنماذج (robust model development)، ومصادقة مستقلة ("التحدي الفعّال" (effective challenge))، وحوكمة (governance) تشمل سجلًا للنماذج (model inventory). وفي المملكة المتحدة، يضع البيان الرقابي (supervisory statement) SS1/23 الصادر عن هيئة التنظيم الاحترازي (Prudential Regulation Authority) مبادئ إدارة مخاطر النماذج (model risk management principles) للبنوك ويأخذ في الحسبان صراحةً نماذج الذكاء الاصطناعي (the AI models) وتعلّم الآلة (machine learning). ويحمل إرشاد QCB للذكاء الاصطناعي (QCB's AI guideline) في المؤسسات المالية توقعات مماثلة للبنوك القطرية؛ تحقق من النص الحالي (current text). والخطوة الصحيحة في الحوكمة (governance move) هي توسيع إدارة مخاطر النماذج (models) لتشمل الذكاء الاصطناعي (AI) بدلًا من تكرارها: وسّع تعريف "النموذج" (definition of "model") ليغطي أنظمة الذكاء الاصطناعي (AI systems) بما فيها الذكاء الاصطناعي التوليدي (GenAI)، وأضف مصادقة خاصة بالذكاء الاصطناعي (العدالة (fairness)، والمتانة (robustness)، وقابلية التفسير (explainability)، وتقييم الذكاء الاصطناعي التوليدي (GenAI evaluation))، وأضف محفّزات (triggers) لتغييرات نماذج الموردين (vendor model changes). وفي أبريل 2026 حلّت محلّها إرشادات **SR 26-2** (*Revised Guidance on Model Risk Management*) التي أصدرها الاحتياطي الفيدرالي (Federal Reserve) وOCC وFDIC. وهي أكثر اعتمادًا على المبادئ (principles-based)، وتربط شدة التحقق بأهمية النموذج (materiality) بدلًا من دورات ثابتة (fixed cycles)، وتضيّق تعريف النموذج (definition of a model)، وتُخضع نماذج المورّدين (vendor models) للمعيار (standard) نفسه؛ راجع نصّها الحالي لمعرفة كيف تتعامل مع الذكاء الاصطناعي التوليدي (the GenAI) والوكيلي (agentic).

**عملية الاستثناءات (exception process).** لن تناسب القواعد كل حالة أحيانًا. وعملية الاستثناءات (exceptions) الجيدة تجعل الانحرافات (deviations) مرئية ومحددة زمنيًا (time-bound) ولها مالك (owner)، بدلًا من أن تكون صامتة:

- يذكر مقدّم الطلب (requester) القاعدة (rule)، والسبب (reason)، والمخاطر، والضوابط التعويضية (compensating controls)، وتاريخ الانتهاء المقترح (proposed expiry date).
- تتدرج صلاحية الموافقة (approval authority) بحسب المخاطر (قائد الحوكمة (governance lead) للمخاطر المنخفضة؛ واللجنة (committee) للفئة العليا (high tier)؛ ولا موافقة إطلاقًا على المتطلبات المفروضة قانونًا (legally mandated requirements)، إذ لا يمكن استثناؤها داخليًا).
- يُدرَج كل استثناء (exception) في سجل الاستثناءات (exception register)، ويُبلَّغ به إلى اللجنة (committee)، وتنتهي صلاحيته. ويتطلب التجديد (renewal) قرارًا جديدًا (fresh decision).
- تكرار الاستثناءات (exceptions) من القاعدة (rule) نفسها إشارة إلى أن القاعدة تحتاج إلى تغيير.

### 🔴 نظرة الخبير (Expert view)

**اربط الضوابط بالمراحل والفئات (Map controls to stages and tiers).** أكثر أداة منفردة فائدةً في برنامج ناضج (mature programme) هي مصفوفة ضوابط دورة الحياة (life-cycle control matrix): صفوفها مراحل دورة الحياة (life-cycle stages)، وأعمدتها فئات المخاطر (risk tiers)، وتسرد كل خلية الضوابط الإلزامية (mandatory controls) والأدلة (evidence). إنها تحوّل السياسة (policy) إلى شيء يستطيع المهندسون (engineers) اتباعه ويستطيع المدققون (auditors) اختباره. والملحق A (Annex A) من **ISO/IEC 42001** منظّم بطريقة مشابهة، بمجموعات ضوابط (control groups) تغطي سياسات الذكاء الاصطناعي (AI policies)، والتنظيم الداخلي (internal organisation)، والموارد (resources)، وتقييم الأثر (impact assessment)، ودورة حياة نظام الذكاء الاصطناعي (AI system life cycle)، والبيانات لأنظمة الذكاء الاصطناعي (data for AI systems)، والمعلومات للأطراف المعنية (information for interested parties)، واستخدام أنظمة الذكاء الاصطناعي (use of AI systems)، والعلاقات مع الأطراف الثالثة والعملاء (third-party and customer relationships). وتستخدمه مؤسسات كثيرة قائمةَ تحقق (checklist) لمنظومة سياساتها (their policy stack).

**المتطلبات التنظيمية تعيش داخل المنظومة (Regulatory requirements live inside the stack).** بالنسبة لمقدّمي الأنظمة (providers) عالية المخاطر (high-risk)، يشترط EU AI Act نظامًا لإدارة المخاطر (risk management system) يعمل طوال دورة الحياة (life cycle) كاملة (المادة 9 (Art. 9)) ونظامًا لإدارة الجودة (quality management system) بسياسات (policies) وإجراءات وتعليمات مكتوبة (المادة 17 (Art. 17)). وللمُشغِّلين (deployers) واجباتهم الخاصة (المادة 26 (Art. 26))، بما في ذلك استخدام الأنظمة وفقًا لتعليمات الاستخدام (instructions for use)، ورصد تشغيلها (monitoring their operation)، والاحتفاظ (retention) بالسجلات المولَّدة آليًا (automatically generated logs) الخاضعة لسيطرتهم لمدة مناسبة لا تقل عن ستة أشهر ما لم ينص قانون آخر على غير ذلك. ومنظومة السياسات (policy stack) هي المكان الذي تُسند فيه هذه الالتزامات ويُوثَّق الوفاء بها.

**الذكاء الاصطناعي التوليدي يطمس حدود دورة الحياة (GenAI blurs the life cycle).** مع نموذج أساسي مشترى (bought foundation model)، يصبح "البناء (build)" اختيارَ نموذج (model)، وكتابة أوامر نصية، وتهيئة الاسترجاع (configuring retrieval)، وإضافة حواجز الحماية (guardrails). وقد يكون "الإصدار (release)" تغييرًا في الإعدادات (configuration) دون أي نشر للشيفرة (code deployment). ويجب أن يعامل إجراء إدارة التغيير (change management procedure) لديك تغييرات الأوامر النصية (prompts) ومصادر الاسترجاع (retrieval sources) وإصدارات النماذج (model versions) على أنها تغييرات، مصنّفة بحسب أثرها. فتغيير الأمر النصي (prompt) لمساعد الائتمان (credit copilot) بما يغيّر طريقة تلخيصه لعوامل المخاطر تغيير جوهري (material)؛ أما تصحيح خطأ إملائي فليس كذلك.

**التناسب يبقي المنظومة حيّة (Proportionality keeps the stack alive).** إذا استغرق تسجيل أداة داخلية (Internal) منخفضة المخاطر (low-risk) ستة أسابيع، يتوقف الناس عن التسجيل (registration). والمسار السريع (fast track) لحالات الاستخدام (use cases) منخفضة الفئة (نموذج قصير (short form)، وقرار خلال أيام) هو ما يجعل السجل (inventory) مكتملًا، والاكتمال (completeness) أثمن من الصرامة (rigour) في الأنظمة التافهة.

## ⚖️ الأدوات التنظيمية (The instruments)
| الأداة | ما تشترطه أو توصي به (What it requires or recommends) | إشارة الامتحان (Exam cue) |
|---|---|---|
| **ISO/IEC 5338** | عمليات دورة حياة أنظمة الذكاء الاصطناعي (AI system life-cycle processes)، مبنية على المعايير (standards) القائمة لدورة حياة الأنظمة والبرمجيات (systems and software life-cycle) | معيار العمليات (process standard) لدورة حياة الذكاء الاصطناعي (AI life cycle) |
| **ISO/IEC 22989** | مفاهيم الذكاء الاصطناعي (AI concepts) ومصطلحاته (terminology) ووصف لمراحل دورة الحياة (life-cycle stages) | مفردات مشتركة (Shared vocabulary)؛ المراحل (stages) تمتد من النشأة (inception) إلى الإيقاف والتقاعد (retirement) |
| **NIST AI RMF** | مراحل دورة الحياة (life-cycle stages) والجهات الفاعلة في الذكاء الاصطناعي (AI actors)؛ وتدعو وظيفة Govern (Govern function calls) إلى سياسات (policies) وعمليات وسجل لأنظمة الذكاء الاصطناعي (AI inventory) | السجل (inventory) والسياسات (policies) يقعان ضمن Govern |
| **OECD AI Principles** | تعريف نظام الذكاء الاصطناعي (المحدَّث في نوفمبر 2023) ووصف تكراري لدورة الحياة (iterative life-cycle description) | تعريف EU AI Act مبني على تعريف OECD (OECD definition) |
| **ISO/IEC 42001** — البند 5.2 (Clause 5.2) والملحق A (Annex A) | سياسة ذكاء اصطناعي (AI policy) تعتمدها الإدارة العليا (top management)؛ وضوابط الملحق A (Annex A controls) للسياسات (policies) ودورة الحياة (life cycle) والبيانات (data) والأطراف الثالثة (third parties) وغيرها | الملحق A (Annex A) قائمة تحقق عملية (practical checklist) لمنظومة السياسات (policy stack) |
| **EU AI Act** — المواد 9 و17 و26 | إدارة المخاطر عبر دورة الحياة (Life-cycle risk management) وإدارة الجودة (quality management) لمقدّمي الأنظمة (providers) عالية المخاطر (high-risk)؛ وواجبات المُشغِّل (deployer duties) بما فيها الرصد (monitoring) والاحتفاظ بالسجلات لستة أشهر على الأقل (log retention of at least six months) | الالتزامات تختلف بين مقدّمي الأنظمة (providers) والمُشغِّلين (deployers) |
| **SR 11-7** | (حلّت محلّها **SR 26-2** في أبريل 2026.) إرشادات رقابية أمريكية بشأن إدارة مخاطر النماذج (model risk management): تطوير سليم، ومصادقة مستقلة (independent validation)، وحوكمة (governance)، وسجل | "التحدي الفعّال (effective challenge)" والمصادقة المستقلة (independent validation) ينطبقان على نماذج الذكاء الاصطناعي (AI models) في البنوك |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
**مصفوفة ضوابط دورة حياة الذكاء الاصطناعي (مقتطف)** التي أعدّتها ليلى، وهي جزء من معيار دورة حياة الذكاء الاصطناعي (AI Life-cycle Standard):

| المرحلة (stage) | فئة منخفضة (مثل ملخّص محاضر الاجتماعات (meeting-notes summariser)) | فئة متوسطة (مثل فرز تنبيهات الاحتيال (fraud-alert triage)) | فئة عليا (مثل التقييم الائتماني (credit scoring)، وفرز السير الذاتية (CV screening)، ومساعد الائتمان (credit copilot)) |
|---|---|---|---|
| التخطيط والتصميم (plan and design) | التسجيل في السجل (Register in inventory)؛ وتسمية المالك (owner named) | + غرض مقصود وحالات إساءة استخدام (misuse cases) موثّقة؛ وفحص أولي للخصوصية (privacy screen) | + موافقة اللجنة على المضي (Committee approval to proceed)؛ وتقييم الأثر على حماية البيانات (DPIA)؛ وتقييم الأثر على الحقوق الأساسية (FRIA) حيث يلزم؛ وتسجيل تصنيف EU AI Act (EU AI Act classification) |
| البيانات (data) | مصادر بيانات معتمدة (Approved data sources) فقط | + سجل مصدر البيانات (Data provenance record)؛ وفحوص الجودة (quality checks) | + تحليل التمثيل والتحيّز (Representativeness and bias analysis)؛ وتأكيد قسم الشؤون القانونية (Legal) لحقوق الاستخدام (rights-to-use) |
| البناء (build) | أدوات ومنصات معتمدة (Approved tools and platforms) | + توثيق النموذج (بطاقة النموذج (model card)) | + الاتفاق على نهج قابلية التفسير (Explainability approach)؛ ونموذج التهديدات الأمنية (security threat model) |
| التحقق والمصادقة (verify and validate) | اختبار ذاتي (self-test) من المالك (owner) | + مراجعة الأقران (Peer review) للاختبارات | + مصادقة مستقلة (independent validation) من فريق مخاطر النماذج (model risk team)؛ واختبار الفريق الأحمر (red-teaming) للذكاء الاصطناعي التوليدي (GenAI) |
| النشر (deployment) | نشر إرشادات المستخدم (User guidance) | + تدريب المستخدمين (User training) | + موافقة اللجنة على الإطلاق (Committee launch approval)؛ وتدريب المشرفين (overseer training) قبل منح الوصول؛ وإشعار الشفافية (transparency notice) للعملاء |
| التشغيل والرصد (operate and monitor) | إقرار سنوي (Annual attestation) من المالك (owner) | + مراجعة ربع سنوية للأداء (Quarterly performance review) | + رصد شهري (Monthly monitoring) مقابل حدود التحمّل (tolerances)؛ ودليل التعامل مع الحوادث (incident playbook)؛ ومحفّزات تغييرات الموردين (vendor-change triggers) |
| الإيقاف والتقاعد (retirement) | الحذف من السجل (Remove from inventory) | + أرشفة الوثائق (archive documentation) | + اعتماد خطة الإيقاف (Retirement plan)؛ وتطبيق الاحتفاظ بالبيانات (data retention)؛ وإبلاغ المستخدمين المتأثرين (affected users) |

**قيد في سجل الاستثناءات (مثال):**

| المعرّف (ID) | القاعدة (rule) | مقدّم الطلب (requester) | السبب (reason) | الضوابط التعويضية (compensating controls) | الجهة الموافقة (Approved by) | تاريخ الانتهاء (expiry date) |
|---|---|---|---|---|---|---|
| EX-004 | مصادقة مستقلة للفئة العليا (independent validation for high-tier) قبل الإطلاق (launch) | خالد | موعد تنظيمي نهائي (Regulatory deadline) لمنتج المنشآت الصغيرة والمتوسطة (SME) | تجربة محدودة (Limited pilot) على 200 طلب؛ ومراجعة بشرية بنسبة 100% (100% human review)؛ واكتمال المصادقة (validation) خلال 60 يومًا | لجنة حوكمة الذكاء الاصطناعي (AI Governance Committee) | 60 يومًا من تاريخ الموافقة (approval) |

## 🛠️ التمارين (Exercises)

### 🟢 مبتدئ (Beginner)
ضع كل نشاط من أنشطة نجم (Najm activities) التالية في مرحلة من مراحل دورة الحياة (life-cycle stage): اختيار مستندات الاسترجاع (retrieval documents) لمساعد الائتمان (credit copilot)؛ فحص معدلات تنبيهات نموذج الاحتيال (fraud-model) كل شهر؛ تقرير ما إذا كانت الأسئلة الشائعة (FAQs) لروبوت المحادثة (chatbot) تحتاج إلى ذكاء اصطناعي (AI)؛ حذف بيانات تدريب (training data) نموذج التقييم القديم (old scoring model).
*يكتمل عندما (Done when):* يُطابَق كل نشاط مع مرحلة (stage) مع جملة واحدة من التعليل.

### 🟡 متوسط (Intermediate)
اكتب قيد السجل (inventory record) لأداة فرز السير الذاتية (CV-screening tool)، مستخدمًا الحقول (fields) المذكورة في 🟡 التعمق أكثر (Going deeper).
*يكتمل عندما (Done when):* يُملأ كل حقل، ويكون لفئة المخاطر (risk tier) سبب، ويُذكر تصنيف EU AI Act (EU AI Act classification) ودور (role) نجم (مقدّم النظام (provider) أو المُشغِّل (deployer)).

### 🔴 متقدم (Advanced)
صُغ إجراء استثناءات الذكاء الاصطناعي (AI Exception Procedure) في نجم في أقل من 400 كلمة: من يحق له الطلب، وما يجب أن يقدّمه، وصلاحية الموافقة (approval authority) بحسب الفئة (by tier)، وما لا يمكن استثناؤه، والتسجيل (registration)، وانتهاء الصلاحية (expiry)، والإبلاغ.
*يكتمل عندما (Done when):* يمنع الإجراء الاستثناءات الصامتة الدائمة (permanent silent exceptions)، وينص على أن المتطلبات المفروضة قانونًا (legally mandated requirements) لا يمكن التنازل عنها داخليًا.

## ⚠️ أخطاء وفخاخ الامتحان (Mistakes and exam traps)
- **حوكمة بوابة الإطلاق فقط (Launch-gate-only governance).** الإجابات التي تضع جميع الضوابط (controls) عند النشر (deployment) تغفل مخاطر التصميم (design) والبيانات (data) والرصد (monitoring). فضّل الإجابات القائمة على دورة الحياة (life-cycle answers).
- **السجل كفكرة لاحقة (Inventory as an afterthought).** المؤسسة التي لم تحصر ذكاءها الاصطناعي (its AI) في سجل لا تستطيع تصنيفه أو تقييمه أو رصده. والسجل (inventory) عادةً هو "الخطوة التشغيلية الأولى (first operational step)" الصحيحة.
- **النماذج الداخلية وحدها هي المعتبرة (Only in-house models count).** أدوات الذكاء الاصطناعي التوليدي (GenAI tools) المشتراة والمدمجة (embedded) والتي يستخدمها الموظفون تنتمي إلى السجل (inventory) وتخضع لسياسة الاستخدام المقبول (acceptable-use policy).
- **الحظر الشامل للذكاء الاصطناعي التوليدي (Blanket GenAI bans).** نادرًا ما يكون الإجابة الأفضل (the best answer)؛ فالأدوات المعتمدة (approved tools) مع قواعد البيانات (data rules) والتدريب (training) تنجح أكثر وتقلل الذكاء الاصطناعي الخفي (shadow AI).
- **استثناءات بلا تاريخ انتهاء (Exceptions without expiry).** الاستثناء الذي ليس له تاريخ انتهاء (expiry date) هو تغيير في السياسة (policy) لم يوافق عليه أحد.
- **الخلط بين السياسة والإجراء (Policy vs procedure confusion).** السياسات (policies) تحدد النية (intent) والأدوار (roles)؛ والإجراءات (procedures) تقدّم الخطوات. وقد تختبر أسئلة الامتحان في أي وثيقة ينتمي أمر ما.

## 🧾 الخلاصة (Recap)
- تمتد دورة حياة الذكاء الاصطناعي (AI life cycle) من التخطيط والتصميم (plan and design)، مرورًا بالبيانات (data) والبناء (build) والمصادقة (validation) والنشر (deployment) والرصد (monitoring)، وصولًا إلى الإيقاف والتقاعد (retirement)، وتعود حلقتها إلى البداية عند التغيير.
- تصف OECD وNIST AI RMF وISO/IEC 22989 وISO/IEC 5338 دورة الحياة (life cycle)؛ فاعرف المراحل (stages).
- منظومة السياسات (policy stack): سياسة الذكاء الاصطناعي (AI policy)، وسياسة الاستخدام المقبول / الذكاء الاصطناعي التوليدي (acceptable-use / GenAI policy)، وإجراء السجل والتصنيف (inventory and classification procedure)، ومعيار دورة الحياة (life-cycle standard)، وإدارة مخاطر النماذج (model risk management)، وإجراء الاستثناءات (exception procedure)، إضافة إلى بنود الذكاء الاصطناعي (AI) في السياسات (policies) القائمة.
- السجل (inventory) هو الأساس؛ ومصفوفة ضوابط دورة الحياة (life-cycle control matrix) تجعل الضوابط (controls) متناسبة (proportionate) وقابلة للاختبار.
- يجب أن تكون الاستثناءات (exceptions) مرئية، ولها مالك (owner)، ومعوَّضة بضوابط (controls)، ومحددة زمنيًا (time-bound).

## ✍️ اختبر نفسك (Check yourself)

**1. يريد بنك نجم أن يبدأ حوكمة الذكاء الاصطناعي (AI governance) لكنه لا يعرف عدد أنظمة الذكاء الاصطناعي (AI systems) التي يستخدمها. ماذا ينبغي أن يفعل أولًا؟**

- A. شراء منصة لرصد الذكاء الاصطناعي (AI monitoring platform)
- B. بناء سجل لأنظمة الذكاء الاصطناعي (AI inventory)، يشمل الذكاء الاصطناعي (AI) المشترى والمدمج (bought and embedded)، وتصنيف كل نظام بحسب المخاطر
- C. التكليف بتمرين اختبار الفريق الأحمر (red-team exercise) على روبوت المحادثة (chatbot)
- D. كتابة معايير تقنية تفصيلية (detailed technical standards) لمصادقة النماذج (model validation)

<details><summary>الإجابة (Answer)</summary>

**B.** لا يمكنك حوكمة ما لا تراه (You cannot govern what you cannot see)؛ فالسجل والتصنيف (inventory and classification) يمكّنان كل ما عداهما. أما الخيارات الأخرى فمفيدة لاحقًا، لكنها تفترض أنك تعرف ما لديك. (انظر 🟡 التعمق أكثر (Going deeper)، السجل (inventory).)

</details>

**2. أي وثيقة تتضمن عادةً تعليمات خطوة بخطوة (step-by-step instructions) لتسجيل (registration) حالة استخدام (use case) جديدة للذكاء الاصطناعي (AI)؟**

- A. إجراء
- B. سياسة الذكاء الاصطناعي (AI policy)
- C. إرشاد (guideline)
- D. بيان شهية المخاطر (risk appetite statement)

<details><summary>الإجابة (Answer)</summary>

**A.** تصف الإجراءات (procedures) كيفية تنفيذ عملية ما؛ والسياسات (policies) تحدد النية (intent) والنطاق والأدوار (roles)؛ والإرشادات (guidelines) استشارية. (انظر 🟢 الأساسيات (The essentials)، منظومة السياسات (policy stack).)

</details>

**3. تصرّف مساعد التسوق (shopping assistant) القائم على الذكاء الاصطناعي التوليدي (GenAI) لدى متجر تجزئة (retailer) تصرفًا جيدًا عند الإطلاق (launch)، لكن إجاباته تراجعت بعد أن حدّث مورد النموذج الأساسي (foundation-model vendor) نموذجه. أي ضابط (control) من ضوابط دورة الحياة (life-cycle controls) كان غائبًا بأوضح صورة؟**

- A. دراسة جدوى (business case) في مرحلة التصميم (design stage)
- B. مراجعة ترخيص البيانات (data licence review)
- C. رصد تشغيلي (Operational monitoring) مع محفّزات (triggers) لتغييرات نماذج الموردين (vendor model changes)
- D. سياسة ذكاء اصطناعي (AI policy) معتمدة من مجلس الإدارة (board)

<details><summary>الإجابة (Answer)</summary>

**C.** التراجع بعد تغيير من المورد (vendor) إخفاق في مرحلة التشغيل والرصد (operate-and-monitor). فدورة الحياة (life cycle) تعود في حلقة بعد النشر (deployment)، ويجب أن تفعل الحوكمة (governance) الشيء نفسه. (انظر 🔴 نظرة الخبير (Expert view).)

</details>

**4. ما الغرض الرئيسي من تاريخ انتهاء الصلاحية (expiry date) لاستثناء (exception) معتمد من السياسة (policy)؟**

- A. الامتثال (compliance) لمادة محددة في EU AI Act بشأن الاستثناءات (exceptions)
- B. السماح لمقدّم الطلب (requester) بتمديده تلقائيًا
- C. تقليل عدد اجتماعات اللجنة (committee meetings)
- D. ضمان أن تكون الانحرافات (deviations) مؤقتة وأن يُعاد البت فيها بدلًا من أن تصبح تغييرات صامتة ودائمة في السياسة (policy)

<details><summary>الإجابة (Answer)</summary>

**D.** يفرض انتهاء الصلاحية (expiry) اتخاذ قرار جديد ويُبقي سجل الاستثناءات (exception register) ذا معنى. ولا توجد في قانون الذكاء الاصطناعي (AI Act) مادة بشأن الاستثناءات الداخلية (internal exceptions)، فالخيار A مختلَق. (انظر 🟡 التعمق أكثر (Going deeper)، الاستثناءات (exceptions).)

</details>

**5. أي معيار (standard) من معايير (standards) ISO/IEC يحدد عمليات دورة حياة أنظمة الذكاء الاصطناعي (AI system life-cycle processes)؟**

- A. ISO/IEC 42005
- B. ISO/IEC 5338
- C. ISO/IEC 38507
- D. ISO/IEC 42006

<details><summary>الإجابة (Answer)</summary>

**B.** يغطي ISO/IEC 5338 عمليات دورة حياة أنظمة الذكاء الاصطناعي (AI system life-cycle processes). أما 42005 فيتعلق بتقييم الأثر (impact assessment)، و38507 بالحوكمة على مستوى مجلس الإدارة (board-level governance)، و42006 يغطي الجهات التي تمنح شهادة 42001. (انظر ⚖️ الأدوات التنظيمية (The instruments).)

</details>

## 📚 المراجع (References)
- إطار NIST لإدارة مخاطر الذكاء الاصطناعي (NIST AI Risk Management Framework): https://www.nist.gov/itl/ai-risk-management-framework
- مبادئ (principles) OECD للذكاء الاصطناعي (AI) وتعريف نظام الذكاء الاصطناعي (Definition of AI system): https://oecd.ai/en/ai-principles
- اللجنة (committee) ISO/IEC JTC 1/SC 42 (ISO/IEC 5338 و22989 وعائلة معايير الذكاء الاصطناعي (AI standards family)): https://www.iso.org/committee/6794475.html
- ISO/IEC 42001:2023: https://www.iso.org/standard/81230.html
- قانون الذكاء الاصطناعي الأوروبي (EU AI Act)، اللائحة (EU) 2024/1689: https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- الاحتياطي الفيدرالي الأمريكي (US Federal Reserve) SR 11-7، إرشادات إدارة مخاطر النماذج (model risk management): https://www.federalreserve.gov/boarddocs/srletters/2011/sr1107.htm
- الاحتياطي الفيدرالي (Federal Reserve) وOCC وFDIC، SR 26-2 الإرشادات (guidelines) المنقّحة بشأن إدارة مخاطر النماذج (Revised Guidance on Model Risk Management)، أبريل 2026: https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm
- هيئة التنظيم الاحترازي في بنك إنجلترا (مبادئ إدارة مخاطر النماذج (model risk management principles) SS1/23): https://www.bankofengland.co.uk/prudential-regulation
- مصرف قطر المركزي (Qatar Central Bank): https://www.qcb.gov.qa/

---

# 3.2 — سياسات حوكمة البيانات والملكية الفكرية للذكاء الاصطناعي (Data governance and intellectual-property policies for AI)
*المستوى: 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 3.1* · *مجال المعرفة (BoK): I.C*

## ⚡ الدرس في دقيقة (In 60 seconds)
- ترث أنظمة الذكاء الاصطناعي (AI systems) نقاط قوة بياناتها وعيوبها. وتغطي حوكمة البيانات للذكاء الاصطناعي (data governance for AI) **مصدر البيانات (provenance)** (من أين جاءت البيانات (data))، و**تسلسل البيانات (lineage)** (كيف انتقلت وتغيّرت)، و**الجودة والتمثيل (quality and representativeness)**، و**الاحتفاظ (retention)**، و**الاستخدام المشروع (lawful use)** (الأساس القانوني (lawful basis)، والغرض، والحقوق).
- بالنسبة للأنظمة عالية المخاطر (high-risk)، تشترط **المادة 10 (Art. 10) من EU AI Act** ممارسات لحوكمة البيانات (data governance practices) تشمل بيانات التدريب والتحقق والاختبار (training, validation and testing data)، بما في ذلك فحصها بحثًا عن التحيّزات (biases) المحتملة. وتظل مبادئ (principles) **GDPR** (تحديد الغرض (purpose limitation)، وتقليل البيانات (minimisation)، وتحديد مدة التخزين (storage limitation)) سارية على البيانات الشخصية (personal data) المستخدمة في الذكاء الاصطناعي (AI).
- يجب أن تغطي سياسات الملكية الفكرية (IP policies) ثلاثة أمور: **الحقوق في بيانات التدريب (rights to training data)** (التراخيص (licences)، وحق المؤلف (copyright)، وحدود التنقيب في النصوص والبيانات (text-and-data mining))، و**الحقوق في المخرجات (rights in outputs)** (من يملكها، وهل هي محمية أصلًا)، و**المعلومات السرية في الأوامر النصية (confidential information in prompts)** (الأسرار التجارية (trade secrets) وبيانات العملاء (customer data) التي تتسرب إلى الأدوات).
- إشارة الامتحان (Exam cue): عبارة "البيانات لدينا بالفعل (we have the data already)" ليست أساسًا قانونيًا (lawful basis) لغرض جديد. ابحث عن توافق الأغراض (purpose compatibility) وفحوص الحقوق (rights checks).
- الفخ الأكبر (Biggest trap): افتراض أن البيانات (data) المتاحة علنًا (publicly available) على الإنترنت حرة الاستخدام في التدريب (training)، أو أن مخرجات الذكاء الاصطناعي (AI outputs) مملوكة للمؤسسة تلقائيًا.

## 🧭 لماذا يهم (Why it matters)
يريد فريق دانة تحسين نموذج الائتمان (credit model) للمنشآت الصغيرة والمتوسطة (SME) بإضافة عشر سنوات من ملفات القروض التاريخية (historical loan files)، وبيانات المعاملات (transaction data) من الحسابات الجارية (current accounts)، ومجموعة بيانات (dataset) عن القوائم المالية للشركات (company financials) اشتُريت من وسيط بيانات (data broker) قبل خمس سنوات. وفي الوقت نفسه، يبني فريق عمر مكتبة الاسترجاع (retrieval library) لمساعد الائتمان (credit copilot) في بنك نجم (Najm Bank)، وقد رفع أحدهم تقارير بحثية (research reports) قطاعية من خدمة اشتراك (subscription service) مدفوعة. ويريد مديرو العلاقات (relationship managers) لصق مسوّدات مذكرات الائتمان، التي تتضمن أسماء العملاء وبياناتهم المالية، في أداة ذكاء اصطناعي توليدي عامة (public GenAI tool) لتحسين صياغتها.

يثير كل من هذه الأمور سؤالًا يتعلق بالبيانات (data) أو الملكية الفكرية (intellectual property) لم يكتب البنك قاعدة له. هل جُمعت بيانات القروض التاريخية لغرض يتوافق مع تدريب النماذج (model training)؟ هل تعكس السنوات العشر قاعدة العملاء الحالية (current customer base)، أم فترةً كانت فيها فئات معينة (certain groups) محرومة من الخدمة (under-served)؟ هل يسمح ترخيص الوسيط (broker licence) باستخدامها في تعلّم الآلة (machine learning)؟ هل يسمح اشتراك الأبحاث (research subscription) بنسخ المحتوى إلى فهرس ذكاء اصطناعي (AI index)؟ وماذا يحدث لبيانات العملاء (customer data) التي تُكتب في أداة ذكاء اصطناعي استهلاكية (consumer AI tool)؟ والحالات الواقعية تُظهر حجم ما هو على المحك: فقد قيّدت هيئة حماية البيانات الإيطالية (Italian data protection authority) ChatGPT مؤقتًا في إيطاليا عام 2023، وغرّمت OpenAI مبلغ 15 مليون يورو في ديسمبر 2024، لأسباب منها الأساس القانوني (lawful basis) لبيانات التدريب (training data)؛ كما قيّدت Samsung استخدام الذكاء الاصطناعي التوليدي (GenAI) عام 2023 بعد أن لصق موظفون، بحسب التقارير، شيفرة سرية (Confidential) في روبوت محادثة عام (public chatbot).

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**لماذا يحتاج الذكاء الاصطناعي (AI) إلى قواعد بيانات خاصة به (its own data rules).** تركّز حوكمة البيانات التقليدية (Traditional data governance) على الدقة (accuracy) لأغراض إعداد التقارير وعلى أمن البيانات المخزنة (security of stored data). ويضيف الذكاء الاصطناعي متطلبات جديدة (new demands):

- تُستخدم البيانات (data) *لتعلّم الأنماط (learn patterns)*، فتتحول التحيّزات التاريخية (historical biases) إلى قرارات مستقبلية (نموذج التوظيف (recruiting model) لدى Amazon، الذي أفادت التقارير بالتخلي عنه عام 2018، تعلّم خفض تقييم السير الذاتية المرتبطة بالنساء لأنه دُرّب على تاريخ توظيف يهيمن عليه الذكور).
- كثيرًا ما *يُعاد توظيف (repurposed)* البيانات (data): تُجمع لسبب (reason)، ثم تُستخدم لتدريب (training) نموذج (model) لسبب آخر.
- يمكن للنماذج (models) أن *تحفظ (memorise)* بيانات التدريب (training data) وأن تكشفها أحيانًا، فما يدخل قد يخرج.
- تأتي البيانات (data) من مصادر كثيرة (الأنظمة الداخلية (internal systems)، والوسطاء (brokers)، وكشط الويب (web scraping)، والتوليد الاصطناعي (synthetic generation)، والموردين (vendors))، ولكل منها حقوقه وجودته.

**العناصر الأساسية لسياسة حوكمة البيانات للذكاء الاصطناعي (core data governance policy elements for AI):**

| العنصر (Element) | ما يعنيه (What it means) | القاعدة العملية في نجم (Najm rule of thumb) |
|---|---|---|
| المصدر (provenance) | سجل بمصدر كل مجموعة بيانات (dataset)، وبأي شروط، وكيف ومتى جُمعت | لا تُستخدم أي مجموعة بيانات (dataset) للذكاء الاصطناعي (AI) دون سجل مصدر (provenance record) |
| التسلسل (lineage) | كيف حُوّلت البيانات (data) ودُمجت وصُفّيت ووُسمت بين المصدر (provenance) والنموذج (model) | تسجيل خطوط المعالجة (Pipelines) بحيث يمكن تتبّع أي مدخل للنموذج (model) إلى أصله |
| الجودة (quality) | الدقة والاكتمال والاتساق والحداثة (Accuracy, completeness, consistency, timeliness)، مع معدلات خطأ (error rates) معروفة | فحوص جودة (Quality checks) وعتبات (thresholds) محددة لكل مجموعة بيانات (dataset) |
| التمثيل (representativeness) | مدى عكس البيانات (data) للفئة السكانية (population) والسياق اللذين سيخدمهما النظام | مقارنة الفئة السكانية (population) للتدريب (training) بقاعدة العملاء الحالية (current customer base) |
| الاستخدام المشروع (lawful use) | أساس قانوني للمعالجة (legal basis for the processing)، وتوافق الأغراض (purpose compatibility)، وقيود الفئات الخاصة (special-category limits)، وقواعد النقل (transfer rules) | توقيع مسؤول حماية البيانات (Data Protection Officer, DPO) على البيانات الشخصية (personal data) في أي نظام متوسط أو عالي الفئة (medium or high-tier) |
| تقليل البيانات (minimisation) | البيانات (data) اللازمة للغرض فقط | تبرير كل خاصية من خصائص البيانات الشخصية (personal-data feature) |
| الاحتفاظ (retention) | مدة الاحتفاظ (retention) ببيانات التدريب (training data) ومجموعات الاختبار (test sets) والسجلات (logs) والأوامر النصية (prompts) والمخرجات (outputs)، وسبب ذلك | جدول احتفاظ (Retention schedule) لكل نوع من البيانات (data)، متوافق مع التجميد القانوني (legal holds) وواجبات حفظ السجلات (record-keeping duties) |
| الوصول والأمن (Access and security) | من يمكنه رؤية مجموعات البيانات (datasets) وتغييرها؛ والحماية من العبث (تسميم البيانات (data poisoning)) | وصول قائم على الأدوار (Role-based access)؛ وفحوص سلامة (integrity checks) على بيانات التدريب (training data) |

**الاستخدام المشروع (lawful use) للبيانات الشخصية (personal data).** حيثما تكون البيانات الشخصية (the personal data) معنية، ينطبق **GDPR** (على عملاء نجم في الاتحاد الأوروبي (EU)) و**Qatar PDPPL** (القانون رقم 13 لسنة 2016) على الذكاء الاصطناعي (AI) كما ينطبقان على أي معالجة أخرى. ومبادئ (principles) GDPR في المادة 5 (Art. 5) صارمة: *تحديد الغرض (purpose limitation)* يعني أن البيانات (data) المجمعة لخدمة قرض لا يمكن إعادة استخدامها تلقائيًا لتدريب (training) نموذج تسويقي (marketing model)؛ و*تقليل البيانات (minimisation)* يقصر الخصائص على ما هو ضروري؛ و*تحديد مدة التخزين (storage limitation)* يعني ألا تُحفظ مجموعات التدريب إلى الأبد "احتياطًا". وتحتاج المعالجة (processing) إلى أساس قانوني (lawful basis) بموجب المادة 6 (Art. 6)، وتحتاج الفئات الخاصة (مثل الصحة أو الأصل العرقي) إلى شرط من شروط المادة 9 (Art. 9). ويتناول رأي EDPB رقم 28/2024 (EDPB Opinion 28/2024) بشأن نماذج الذكاء الاصطناعي (AI models) متى يمكن اعتبار النموذج (model) مجهول الهوية (anonymous)، وكيف يمكن تقييم المصلحة المشروعة (legitimate interest) لتطوير النماذج (models) ونشرها، والعواقب المترتبة حين يكون النموذج قد دُرّب على بيانات شخصية عولجت بصورة غير مشروعة (unlawfully processed). وتغطي الوحدة (Module) 4 قانون الخصوصية (privacy law) بعمق؛ أما النقطة هنا فهي أن سياسة البيانات (data policy) يجب أن تمرّر استخدام البيانات الشخصية (personal-data use) عبر فريق الخصوصية (privacy team).

### 🟡 التعمق أكثر (Going deeper)

**المادة 10 (Art. 10) من EU AI Act.** بالنسبة لأنظمة الذكاء الاصطناعي (AI systems) عالية المخاطر (high-risk) التي تُدرَّب بالبيانات (data)، يشترط القانون أن تخضع مجموعات بيانات التدريب والتحقق والاختبار (training, validation and testing datasets) لممارسات حوكمة وإدارة للبيانات (data governance and management practices) مناسبة للغرض المقصود (intended purpose). وتشمل هذه، من بين أمور أخرى: خيارات التصميم (design choices) ذات الصلة؛ وعمليات جمع البيانات (data collection processes) ومنشأها (وبالنسبة للبيانات الشخصية (personal data)، الغرض الأصلي من جمعها (original purpose of collection))؛ وإعداد البيانات (data preparation) مثل التعليق التوضيحي (annotation) والوسم (labelling) والتنظيف والإثراء (enrichment)؛ والافتراضات (assumptions) التي يُقصد أن تمثلها البيانات؛ وتقييم توافرها وكميتها وملاءمتها (availability, quantity and suitability)؛ وفحصها في ضوء التحيّزات المحتملة (possible biases) التي يُرجَّح أن تؤثر على الصحة والسلامة (health and safety) أو الحقوق الأساسية (fundamental rights) أو تؤدي إلى تمييز محظور (prohibited discrimination)؛ وتدابير لاكتشاف تلك التحيّزات (biases) ومنعها والتخفيف منها؛ وتحديد الفجوات أو أوجه القصور في البيانات (data gaps or shortcomings). ويجب أن تكون مجموعات البيانات (datasets) ذات صلة، وممثِّلة بدرجة كافية (sufficiently representative)، وخالية من الأخطاء (free of errors) ومكتملة قدر الإمكان في ضوء الغرض المقصود. ويسمح القانون أيضًا لمقدّمي الأنظمة (providers)، استثناءً (exception) ومع ضمانات صارمة (strict safeguards)، بمعالجة الفئات الخاصة من البيانات الشخصية (special categories of personal data) حيث يكون ذلك ضروريًا بصورة صارمة لاكتشاف التحيّز وتصحيحه (detect and correct bias). ونجم هو مقدّم النظام (provider) لنموذج التقييم الائتماني (credit-scoring model) الذي بناه داخليًا، وهو عالي المخاطر بموجب الملحق III (Annex III)، لذا تنطبق المادة 10 على مجموعات بيانات دانة.

**توثيق البيانات (Data documentation).** الممارسة الجيدة هي توثيق مجموعات البيانات (datasets) كما تُوثَّق النماذج (models): "ورقة بيانات" (datasheet) أو بطاقة بيانات (data card) تصف الدافع (motivation)، والتكوين (composition)، وعملية الجمع (collection process)، والمعالجة المسبقة (preprocessing)، والاستخدامات (uses)، والتوزيع (distribution)، والصيانة (maintenance). وتصبح دليلًا (evidence) لأغراض المادة 10 (Art. 10)، ولتقييمات الأثر على حماية البيانات (DPIAs)، وللقائمين على المصادقة (validators).

**الاحتفاظ في سياق الذكاء الاصطناعي (Retention for AI).** يضيف الذكاء الاصطناعي (AI) أنواعًا جديدة عدة من البيانات (data) إلى جدول الاحتفاظ (retention schedule): مجموعات بيانات التدريب (training data) والاختبار، وإصدارات النماذج (التي قد تتضمن بيانات شخصية (personal data))، والأوامر النصية (prompts) ومخرجات أدوات الذكاء الاصطناعي التوليدي (outputs of GenAI tools)، والسجلات (logs). ويجب أن يوازن الاحتفاظ (retention) بين واجبات متعارضة (competing duties). فتحديد مدة التخزين (storage limitation) يقول احذف حين لا تعود البيانات لازمة. وواجبات حفظ السجلات والمساءلة (Record-keeping and accountability duties) تقول احتفظ بما يكفي لتفسير القرارات وإعادة بنائها: إذ يجب على مُشغِّلي الأنظمة عالية المخاطر (deployers of high-risk systems) بموجب EU AI Act الاحتفاظ بالسجلات (keeping records) الخاضعة لسيطرتهم لمدة لا تقل عن ستة أشهر ما لم ينص قانون آخر على غير ذلك، وكثيرًا ما تشترط قواعد حفظ السجلات المصرفية (banking record-keeping rules) مدة أطول لقرارات الائتمان (credit decisions). وينبغي أن تحدد السياسة (policy)، لكل نوع من البيانات، المدة والسبب (reason) والمحرّك القانوني (legal driver).

**الملكية الفكرية: الحقوق في بيانات التدريب (Intellectual property: training data rights).** قد تكون البيانات (data) والمحتوى المستخدمان لتدريب الذكاء الاصطناعي (AI training) أو تأسيسه (ground) محميين بحق المؤلف (copyright)، أو بحقوق قواعد البيانات (database rights)، أو بالعقد (شروط الترخيص (licence terms))، أو بالأسرار التجارية (trade secrets). النقاط الرئيسية:

- **"المتاح علنًا" لا يعني "حر الاستخدام" (Publicly available is not free to use).** محتوى الويب (Web content) محمي بحق المؤلف (copyright) في العادة. وفي الاتحاد الأوروبي، تنص توجيهة حق المؤلف في السوق الرقمية الموحدة (Digital Single Market Copyright Directive) (EU) 2019/790 على استثناءات للتنقيب في النصوص والبيانات (text-and-data mining): أحدها لمنظمات البحث (research organisations) ومؤسسات التراث الثقافي (cultural heritage institutions) لأغراض البحث العلمي (scientific research)، واستثناء (exception) عام يمكن لأصحاب الحقوق (rightsholders) الانسحاب منه (بالنسبة للمحتوى على الإنترنت، بطريقة قابلة للقراءة آليًا (machine-readable)). وتتبع ولايات قضائية (jurisdictions) أخرى مقاربات مختلفة، والتقاضي (litigation) بشأن تدريب الذكاء الاصطناعي (AI training) جارٍ في عدة دول؛ تحقق من الموقف الحالي (current position).
- **التراخيص مهمة (Licences matter).** تخضع مجموعة بيانات الوسيط (broker dataset) واشتراك الأبحاث (research subscription) لدى نجم للعقد (contract). وتقصر تراخيص (licences) كثيرة الاستخدام على التحليل الداخلي (internal analysis) ولا تسمح بتعلّم الآلة (machine learning) أو إعادة التوزيع (redistribution) أو المنتجات المشتقة (derived products). ويجب أن يتحقق قسم الشؤون القانونية (Legal) من ذلك.
- **يجب على مقدّمي نماذج GPAI (GPAI model providers) معالجة حق المؤلف (copyright).** بموجب EU AI Act، يجب على مقدّمي نماذج الذكاء الاصطناعي للأغراض العامة (GPAI) وضع سياسة (policy) للامتثال (compliance) لقانون حق المؤلف (copyright law) في الاتحاد الأوروبي (EU)، بما في ذلك احترام الانسحاب من التنقيب في النصوص والبيانات (TDM opt-outs)، ونشر ملخص مفصّل (detailed summary) بما يكفي عن المحتوى المستخدم في التدريب (نشر مكتب الذكاء الاصطناعي (AI Office) نموذجًا له (a template) عام 2025). وهذا يساعد نجم، بوصفه مستخدمًا لاحقًا في السلسلة (downstream user)، على تقييم مقدّمي النماذج الأساسية (foundation-model providers) الذين يتعامل معهم.

**الملكية الفكرية: المخرجات (Intellectual property: outputs).** سؤالان منفصلان:

- *هل المخرجات (outputs) محمية أصلًا؟* تشترط أنظمة حق المؤلف (Copyright systems) عمومًا تأليفًا بشريًا (human authorship) أو أصالة (originality). وإرشادات مكتب حق المؤلف الأمريكي (US Copyright Office) هي أن المواد التي يولّدها الذكاء الاصطناعي (AI) دون مساهمة إبداعية بشرية كافية (sufficient human creative contribution) غير قابلة للتسجيل (not registrable)، وإن كان الاختيار والترتيب والتعديل البشري (human selection, arrangement and modification) قد يكون قابلًا للتسجيل (registration). وتختلف المواقف من بلد إلى آخر. والنتيجة العملية: لا يستطيع نجم أن يفترض أنه يملك حقوقًا حصرية (exclusive rights) في صورة تسويقية (marketing image) مولّدة بالكامل بالذكاء الاصطناعي.
- *هل يمكن أن تنتهك المخرجات (outputs) حقوق الآخرين؟* قد تعيد المخرجات إنتاج مواد محمية (protected material) أو علامات تجارية (trademarks). وينبغي أن تشترط السياسات (policies) مراجعة محتوى الذكاء الاصطناعي المنشور خارجيًا (externally published AI content)، وأن تعالج العقود (contracts) مع مقدّمي الأنظمة (providers) التعويضات المتعلقة بالملكية الفكرية (انظر 3.3).

**المعلومات السرية في الأوامر النصية (confidential information in prompts).** الأوامر النصية (prompts) عمليات نقل للبيانات (data transfers). فكتابة البيانات المالية (financials) للعملاء في أداة ذكاء اصطناعي توليدي استهلاكية (consumer GenAI tool) قد تكشف بيانات سرية (confidential data) وشخصية لطرف ثالث (third party) يمكنه تخزينها، أو استخدامها لتدريب النماذج (بحسب الشروط)، أو كشفها في حادثة اختراق. وقد يخالف ذلك التزامات السرية المصرفية (bank secrecy obligations)، وعقود العملاء (client contracts)، وقانون حماية البيانات (data protection law). وقد يُضعف أيضًا حماية الأسرار التجارية (trade-secret protection): فبموجب توجيهة الأسرار التجارية الأوروبية (EU Trade Secrets Directive) (EU) 2016/943، لا تُحمى المعلومات بوصفها سرًا تجاريًا (trade secret) إلا إذا اتخذ حائزها خطوات معقولة (reasonable steps) للحفاظ على سريتها، واللصق غير المنضبط (uncontrolled pasting) في الأدوات العامة (public tools) يقوّض هذه الحجة. وينبغي أن تصنّف سياسة الاستخدام المقبول (acceptable-use policy) البيانات (data) وتحدد أي الفئات يجوز إدخالها في أي الأدوات، مدعومةً باتفاقيات مؤسسية (enterprise agreements) تحظر التدريب (training) على المدخلات (inputs)، وبضوابط تقنية (technical controls) مثل منع تسرب البيانات (data loss prevention).

### 🔴 نظرة الخبير (Expert view)

**حقوق البيانات تنتقل مع النموذج (Data rights travel with the model).** إذا دُرّب نموذج (model) على بيانات لم يكن للمؤسسة حق استخدامها، فإن المشكلة لا تختفي بانتهاء التدريب (training). فالجهات الرقابية (regulators) يمكنها أن تأمر بالحذف، وفي بعض الحالات اشترطت حذف النماذج (models) أو الخوارزميات (algorithms) المشتقة من بيانات حُصل عليها بصورة غير سليمة. ويناقش رأي EDPB رقم 28/2024 (EDPB Opinion 28/2024) كيف يمكن للمعالجة غير المشروعة (unlawful processing) في مرحلة التطوير (development stage) أن تؤثر على مشروعية النشر اللاحق (lawfulness of later deployment). ولهذا يجب تسجيل المصدر (provenance) *قبل* التدريب، لا إعادة بنائه بعد ورود شكوى (complaint).

**العدالة تحتاج إلى بيانات قد لا ترغب في حيازتها (Fairness needs data you may not want to hold).** لاختبار ما إذا كان نموذج (model) ائتماني يضر بفئة محمية (protected group)، تحتاج إلى معرفة الانتماء إلى تلك الفئة (group membership)، لكن قواعد تقليل البيانات (minimisation) والفئات الخاصة (special categories) لا تشجع على جمعها. وتشمل الخيارات: استخدام الإذن الضيق (narrow allowance) في EU AI Act لاكتشاف التحيّز (bias) في الأنظمة عالية المخاطر (مع ضماناته)، أو استخدام مؤشرات بديلة (proxies) بحذر، أو استخدام مجموعات بيانات (datasets) اختبار منفصلة ومضبوطة الوصول (access-controlled). وينبغي أن تسمّي سياسة البيانات (data policy) من يمكنه الإذن بذلك وبأي شروط؛ ويجب أن يشارك كل من مسؤول حماية البيانات (Data Protection Officer, DPO) وإدارة الامتثال (compliance).

**البيانات الاصطناعية والمجهّلة ليست آمنة تلقائيًا (Synthetic and anonymised data are not automatically safe).** البيانات الاصطناعية (Synthetic data) المولّدة من بيانات شخصية (personal data) قد تسرّب معلومات عن أفراد حقيقيين، والبيانات (data) "المجهّلة (anonymised)" قد يكون من الممكن إعادة تحديد هوية (re-identifiable) أصحابها. تعامل مع ادعاءات إخفاء الهوية (anonymity) على أنها أمر يجب التحقق منه، كما يفعل رأي EDPB بالنسبة للنماذج (models) ذاتها.

**مجموعة سياسات واحدة، وولايات قضائية كثيرة (One policy set, many jurisdictions).** يعالج نجم البيانات (data) في قطر والإمارات والاتحاد الأوروبي (EU). وتختلف قواعد توطين البيانات (Data residency) ونقلها عبر الحدود (cross-border transfer) وقواعد السرية القطاعية (sector secrecy rules). والنمط الشائع هو معيار لبيانات الذكاء الاصطناعي على مستوى المجموعة (group-wide AI data standard) عند أشد مستوى مشترك، إضافة إلى ملاحق محلية (مثل متطلبات PDPPL في قطر؛ وقانون حماية البيانات الشخصية (personal data protection) الإماراتي (UAE PDPL)، وبالنسبة لكيانات مركز دبي المالي العالمي (DIFC entities)، قانون حماية البيانات (data protection law) لمركز دبي المالي العالمي (DIFC Data Protection Law)). تحفّظ في التفاصيل المحلية وأكّدها مع المستشار القانوني المحلي (local counsel).

## ⚖️ الأدوات التنظيمية (The instruments)
| الأداة | ما تشترطه أو توصي به (What it requires or recommends) | إشارة الامتحان (Exam cue) |
|---|---|---|
| **EU AI Act** — المادة 10 (Art. 10) | حوكمة بيانات التدريب والتحقق والاختبار (Data governance for training, validation and testing data) للأنظمة عالية المخاطر (high-risk): المنشأ (origin)، والإعداد (preparation)، وفحص التحيّز والتخفيف منه (bias examination and mitigation)، والتمثيل (representativeness)، وفجوات البيانات (data gaps) | التزام على مقدّم النظام (Provider obligation)؛ وفحص التحيّز (bias examination) منصوص عليه صراحةً |
| **EU AI Act** — المادة 53 (Art. 53) | مقدّمو نماذج GPAI (GPAI model providers): سياسة (policy) للامتثال (compliance) لحق المؤلف (بما في ذلك الانسحاب من التنقيب في النصوص والبيانات (TDM opt-outs)) وملخص علني لمحتوى التدريب (public summary of training content) | يمكن للمستخدمين اللاحقين (downstream users) استخدام ذلك لتقييم مقدّمي النماذج (model providers) |
| **GDPR** — المواد 5 و6 و9 | تحديد الغرض (purpose limitation)، وتقليل البيانات (minimisation)، وتحديد مدة التخزين (storage limitation)؛ والأساس القانوني (lawful basis)؛ وشروط الفئات الخاصة (special-category conditions) | البيانات الموجودة (Existing data) لا تأتي معها أغراض جديدة |
| **EDPB Opinion 28/2024** | إخفاء هوية النموذج (Model anonymity)، والمصلحة المشروعة (legitimate interest) لتطوير الذكاء الاصطناعي (AI) ونشره، وأثر بيانات التدريب (training data) المعالَجة (processing) بصورة غير مشروعة | يجب إثبات إخفاء هوية النموذج (Model anonymity) لا افتراضه |
| **EU DSM Copyright Directive** — (EU) 2019/790، المادتان 3–4 | استثناءات التنقيب في النصوص والبيانات (Text-and-data-mining exceptions)؛ ويمكن لأصحاب الحقوق (rightsholders) الانسحاب من الاستثناء العام (general exception) | "المتاح علنًا (Publicly available)" ليس ترخيصًا (licence) |
| **EU Trade Secrets Directive** — (EU) 2016/943 | تتوقف الحماية على اتخاذ خطوات معقولة (reasonable steps) للحفاظ على سرية المعلومات (secrecy of information) | ضوابط الأوامر النصية (Prompt controls) تساعد في الحفاظ على صفة السر التجاري (trade-secret status) |
| **Qatar PDPPL** — القانون رقم 13 لسنة 2016 | قانون حماية البيانات الشخصية في قطر (Qatar's personal data protection law)، وينطبق على معالجة البيانات الشخصية (personal data) بما في ذلك لأغراض الذكاء الاصطناعي (AI) | قانون محلي (Local law) إلى جانب GDPR بالنسبة لنجم؛ تحقق من النص الرسمي |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
البنود (clauses) التي تضيفها ليلى وعمر وسارة إلى **سياسة حوكمة البيانات (Data Governance Policy)** و**سياسة الاستخدام المقبول للذكاء الاصطناعي (Acceptable Use of AI Policy)** في نجم:

> **بنود بيانات الذكاء الاصطناعي (سياسة حوكمة البيانات (Data Governance Policy)، القسم (section) 9)**
> 9.1 لا يجوز استخدام أي مجموعة بيانات (dataset) لتدريب (training) نظام ذكاء اصطناعي (AI system) أو ضبطه ضبطًا دقيقًا (fine-tune) أو تقييمه أو تأسيسه (ground) ما لم يكن لها سجل مصدر (provenance record) يبيّن المصدر (provenance)، وطريقة الجمع (collection method)، والنطاق الزمني (date range)، والترخيص (licence) أو الأساس القانوني (lawful basis)، ومالك البيانات (data owner).
> 9.2 لا يجوز استخدام البيانات الشخصية (personal-data use) لغرض جديد من أغراض الذكاء الاصطناعي (new AI purpose) إلا بعد أن يقيّم مسؤول حماية البيانات (Data Protection Officer, DPO) توافق الغرض (purpose compatibility) والأساس القانوني (lawful basis)، وبالنسبة للأنظمة متوسطة الفئة وعالية الفئة (medium and high-tier)، بعد اكتمال الفحص الأولي (screen) لتقييم الأثر على حماية البيانات (data protection impact assessment).
> 9.3 لا يجوز استخدام بيانات الطرف الثالث (Third-party data) ومحتواه (مجموعات البيانات المرخّصة (licensed datasets)، والاشتراكات (subscriptions)، ومحتوى الويب (Web content)) للذكاء الاصطناعي (AI) إلا بعد أن يؤكد قسم الشؤون القانونية (Legal) أن الترخيص (licence) يسمح بالاستخدام المقصود (intended use).
> 9.4 تتطلب الأنظمة عالية الفئة (high-tier) بطاقة بيانات (data card) توثّق التمثيل (representativeness)، والفجوات المعروفة (known gaps)، وفحص التحيّز (bias examination)، وتدابير التخفيف (mitigations)، يعتمدها مالك النموذج (model owner) وتُراجَع في المصادقة (validation).
> 9.5 تخضع بيانات التدريب (training data)، وإصدارات النماذج (model versions)، والأوامر النصية (prompts)، والمخرجات (outputs)، والسجلات (logs) لجدول الاحتفاظ الخاص بالذكاء الاصطناعي (AI retention schedule) في الملحق C (Annex C). ويُحتفظ بسجلات الأنظمة عالية المخاطر (high-risk) الواقعة ضمن نطاق EU AI Act للمدة المطلوبة قانونًا (legally required period) على الأقل.

> **قواعد الأوامر النصية والمخرجات (سياسة الاستخدام المقبول للذكاء الاصطناعي (Acceptable Use of AI Policy)، القسم (section) 4)**
>
> | فئة البيانات (Data class) | الذكاء الاصطناعي التوليدي المؤسسي (enterprise GenAI) في نجم (بلا تدريب على المدخلات (no training on inputs)، واستضافة (hosting) في الاتحاد الأوروبي (EU)/قطر) | أدوات الذكاء الاصطناعي الاستهلاكية العامة (Public consumer AI tools) |
> |---|---|---|
> | عامة (Public) | مسموح (Allowed) | مسموح |
> | داخلية (Internal) | مسموح (Allowed) | غير مسموح (Not allowed) |
> | سرية (بيانات العملاء (customer data)، وملفات الائتمان (credit files)) | مسموح (Allowed) فقط في حالات الاستخدام (use cases) المعتمدة (مثل مساعد الائتمان (credit copilot)) | ممنوع إطلاقًا (Never) |
> | مقيّدة (بيانات الفئات الخاصة (special-category data)، والأسرار الأمنية (security secrets)، والشيفرة المصدرية (source code)) | فقط بموافقة محددة (specific approval) | ممنوع إطلاقًا (Never) |
>
> 4.3 يجب أن يراجع شخصٌ مخرجات الذكاء الاصطناعي (AI outputs) قبل استخدامها في أي تواصل مع العملاء (customer communication)، أو قرار ائتماني (credit decision)، أو نشر خارجي (external publication). 4.4 لا تفترض أن نجم يملك حقوقًا حصرية (exclusive rights) في المحتوى المولّد بالذكاء الاصطناعي (AI-generated content)؛ راجع قسم الشؤون القانونية (Legal) قبل تسجيله أو الاعتماد عليه بوصفه ملكية خاصة (proprietary).

## 🛠️ التمارين (Exercises)

### 🟢 مبتدئ (Beginner)
لكل من مجموعات البيانات الثلاث (three proposed datasets) التي تقترحها دانة (ملفات القروض التاريخية (historical loan files)، ومعاملات الحسابات الجارية (current-account transactions)، والقوائم المالية للشركات (company financials) من الوسيط (broker))، اكتب السؤال الوحيد الذي يجب الإجابة عنه (answer it) قبل الاستخدام.
*يكتمل عندما (Done when):* يكون لديك سؤال واحد عن الاستخدام المشروع (lawful use) أو الحقوق لكل مجموعة بيانات (dataset)، مع تسمية من يجيب عنه.

### 🟡 متوسط (Intermediate)
صُغ مخططًا لبطاقة بيانات (data card outline) بيانات التدريب (training data) لنموذج الائتمان (credit model) للمنشآت الصغيرة والمتوسطة (SME)، يتضمن ثمانية عناوين (headings) على الأقل، واملأ اثنين منها بمحتوى معقول من نجم.
*يكتمل عندما (Done when):* يغطي المخطط (outline) المنشأ (origin)، وغرض الجمع (collection purpose)، والإعداد (preparation)، والتمثيل (representativeness)، والفجوات المعروفة (known gaps)، وفحص التحيّز (bias examination)، والاحتفاظ (retention).

### 🔴 متقدم (Advanced)
قد لا تكون التقارير البحثية (research reports) الموجودة بالفعل في مكتبة الاسترجاع (retrieval library) لمساعد الائتمان (credit copilot) مرخّصة لاستخدامها في الذكاء الاصطناعي (AI). اكتب مذكرة قرار (decision memo) قصيرة للجنة (committee): الخيارات (الإزالة (remove)، أو الترخيص (licence)، أو الإبقاء مع قيود (keep with restrictions))، ومخاطر كل منها، وتوصيتك.
*يكتمل عندما (Done when):* تميّز المذكرة بين المخاطر التعاقدية (contract risk) ومخاطر حق المؤلف (copyright risk)، وتعالج المخرجات (outputs) التي تقتبس من التقارير، وتحدد مالكًا (owner) للإجراء وتاريخًا.

## ⚠️ أخطاء وفخاخ الامتحان (Mistakes and exam traps)
- **"البيانات لدينا أصلًا (We already hold the data)."** حيازة البيانات (Holding data) ليست أساسًا قانونيًا (lawful basis) لغرض جديد من أغراض الذكاء الاصطناعي (new AI purpose). ابحث عن فحوص توافق الغرض (purpose compatibility) والأساس القانوني.
- **العلني يعني المجاني (Public equals free).** محتوى الويب العام (Public web content) ومجموعات البيانات المشتراة (purchased datasets) محمية عادةً بحق المؤلف (copyright) أو بالعقد (contract). اختر الإجابات التي تتحقق من الحقوق والتراخيص (licences).
- **مخرجات الذكاء الاصطناعي ملكنا تلقائيًا (AI outputs are automatically ours).** حماية المواد المولّدة بالكامل بالذكاء الاصطناعي (purely AI-generated material) غير مؤكدة أو غير متاحة في أنظمة كثيرة؛ والمساهمة البشرية (human contribution) مهمة.
- **الأوامر النصية غير ضارة (Prompts are harmless).** الأوامر النصية (prompts) تنقل البيانات (data) إلى طرف ثالث (third party)؛ فتعامل معها كأي نقل للبيانات (data transfer) واضبطها وفق التصنيف (classification).
- **الاحتفاظ بكل شيء إلى الأبد (Keep everything forever).** يسري تحديد مدة التخزين (storage limitation) وجداول الاحتفاظ (retention schedules) على بيانات التدريب (training data) والأوامر النصية (prompts) والسجلات (logs)، مع موازنتها بواجبات حفظ السجلات (record-keeping duties) القانونية.
- **التحيّز مشكلة في النموذج وحده (Bias is a model problem only).** معظم التحيّز (bias) يدخل عبر البيانات (data)؛ والمادة 10 (Art. 10) تضع فحص التحيّز (bias examination) ضمن حوكمة البيانات (data governance).

## 🧾 الخلاصة (Recap)
- تغطي حوكمة بيانات الذكاء الاصطناعي (AI data governance) المصدر (provenance)، والتسلسل (lineage)، والجودة (quality)، والتمثيل (representativeness)، والاستخدام المشروع (lawful use)، وتقليل البيانات (minimisation)، والاحتفاظ (retention)، والأمن (security).
- تحدد المادة 10 (Art. 10) من EU AI Act واجبات حوكمة البيانات (data governance) لمقدّمي الأنظمة (providers) عالية المخاطر (high-risk)، بما في ذلك فحص التحيّز (bias examination)؛ ويحكم GDPR والقوانين المحلية مثل Qatar PDPPL البيانات الشخصية (personal data).
- تغطي سياسة الملكية الفكرية (IP policy) الحقوق في بيانات التدريب (حق المؤلف (copyright)، والتراخيص (licences)، والانسحاب من التنقيب في النصوص والبيانات (TDM opt-outs))، والحقوق في المخرجات (التأليف البشري (human authorship))، والمعلومات السرية في الأوامر النصية (الأسرار التجارية (trade secrets)، وسرية العملاء (client confidentiality)).
- سجّل المصدر (provenance) قبل التدريب (training): فمشكلات البيانات (data) تنتقل مع النموذج (model).
- اضبط الأوامر النصية (prompts) بتصنيف البيانات (data classification)، والاتفاقيات المؤسسية (enterprise agreements)، والضوابط التقنية (technical controls).

## ✍️ اختبر نفسك (Check yourself)

**1. تريد دانة استخدام بيانات خدمة القروض (loan-servicing data) المجمّعة على مدى عشر سنوات لتدريب (training) نموذج جديد للميل التسويقي (new marketing-propensity model). ما سؤال حوكمة البيانات (data governance question) الرئيسي؟**

- A. ما إذا كان الغرض الجديد متوافقًا مع الغرض الأصلي (original purpose) وله أساس قانوني (lawful basis)
- B. ما إذا كانت البيانات (data) مخزنة في السحابة (cloud)
- C. ما إذا كان لدى علماء البيانات (data scientists) تراخيص البرمجيات (software licences) الصحيحة
- D. ما إذا كان النموذج (model) سيكون أدق من النموذج القديم

<details><summary>الإجابة (Answer)</summary>

**A.** يحكم تحديدُ الغرض (purpose limitation) والأساسُ القانوني (lawful basis) إعادةَ توظيف البيانات الشخصية (personal data). وحيازة البيانات (Holding data) لا تكفي. (انظر 🟢 الأساسيات (The essentials)، الاستخدام المشروع (lawful use).)

</details>

**2. بموجب EU AI Act، أي متطلب ينطبق على بيانات تدريب (training data) أنظمة الذكاء الاصطناعي (AI systems) عالية المخاطر (high-risk)؟**

- A. يجب أن تكون جميع بيانات التدريب (training data) اصطناعية (synthetic)
- B. يجب تخزين بيانات التدريب (training data) في الاتحاد الأوروبي (EU)
- C. ممارسات لحوكمة البيانات (data governance practices) تشمل الفحص بحثًا عن التحيّزات المحتملة (possible biases) وتدابير لاكتشافها ومنعها والتخفيف منها
- D. يجب نشر بيانات التدريب (training data)

<details><summary>الإجابة (Answer)</summary>

**C.** تشترط المادة 10 (Art. 10) ممارسات لحوكمة البيانات (data governance practices) تشمل فحص التحيّز والتخفيف منه (bias examination and mitigation). أما الخيارات الأخرى فليست من متطلبات المادة 10. (انظر 🟡 التعمق أكثر (Going deeper).)

</details>

**3. يقول فريق تسويق إن صور الويب (web images) "متاحة علنًا (publicly available)" ولذلك يمكن استخدامها بحرية للضبط الدقيق (fine-tuning) لنموذج صور (image model). ما أفضل رد؟**

- A. الموافقة (Agree)، لأن كل ما هو على الإنترنت ملك عام (public domain)
- B. استخدام الصور التي لا تحمل علامة مائية (watermark) فقط
- C. استخدام الصور دون إخبار أحد
- D. التحقق من حق المؤلف (copyright) وشروط الترخيص (licence terms) وأي انسحاب من التنقيب في النصوص والبيانات (text-and-data mining) قبل الاستخدام

<details><summary>الإجابة (Answer)</summary>

**D.** الإتاحة العلنية (Public availability) لا تُسقط حق المؤلف (copyright)؛ وفي الاتحاد الأوروبي (EU) يمكن لأصحاب الحقوق (rightsholders) الانسحاب من الاستثناء العام (general exception) للتنقيب في النصوص والبيانات (text-and-data mining). (انظر 🟡 التعمق أكثر (Going deeper)، الحقوق في بيانات التدريب (rights to training data).)

</details>

**4. يلصق مديرو العلاقات (relationship managers) في أحد البنوك البيانات المالية (financials) للعملاء في أداة ذكاء اصطناعي توليدي استهلاكية (consumer GenAI tool). أي مزيج من السياسات (policies) يعالج ذلك على أفضل وجه؟**

- A. سياسة استخدام مقبول (acceptable-use policy) تصنّف البيانات (data) بحسب الأداة، وأداة مؤسسية معتمدة (approved enterprise tool) تحظر شروطها التدريب (training) على المدخلات (inputs)، وضوابط تقنية (technical controls) مثل منع تسرب البيانات (data loss prevention)
- B. بريد إلكتروني تذكيري (reminder email) يطلب من الموظفين توخي الحذر
- C. حظر تام (total ban) لكل أشكال الذكاء الاصطناعي (AI) في البنك
- D. مطالبة مورد الأداة (tool's vendor) بحذف البيانات (data)

<details><summary>الإجابة (Answer)</summary>

**A.** الجمع بين قواعد واضحة، وقناة معتمدة آمنة، وضوابط تقنية (technical controls) يعالج المخاطر؛ أما B فضعيف، وC يدفع إلى الاستخدام الخفي (shadow use)، وD تفاعلي (reactive) بعد وقوع المشكلة. (انظر 🟡 التعمق أكثر (Going deeper)، المعلومات السرية في الأوامر النصية (confidential information in prompts).)

</details>

**5. لماذا قد يُضعف اللصقُ غير المنضبط (uncontrolled pasting) للمعلومات السرية (confidential information) في أدوات الذكاء الاصطناعي العامة (public AI tools) الموقفَ القانوني (legal position) للمؤسسة بما يتجاوز التسرب المباشر (immediate leak)؟**

- A. لأنه ينقل حق المؤلف (copyright) تلقائيًا إلى مورد الذكاء الاصطناعي (AI vendor)
- B. لأنه يجعل المؤسسة مقدّمًا لنموذج GPAI (GPAI provider)
- C. لأنه يخالف المادة 5 من EU AI Act (EU AI Act Art. 5)
- D. لأن حماية الأسرار التجارية (trade-secret protection) تتوقف على اتخاذ خطوات معقولة (reasonable steps) للحفاظ على سرية المعلومات (secrecy of information)، والإفصاح غير المنضبط (uncontrolled disclosure) يقوّض ذلك

<details><summary>الإجابة (Answer)</summary>

**D.** بموجب توجيهة الأسرار التجارية الأوروبية (EU Trade Secrets Directive)، تتطلب الحماية تدابير معقولة للحفاظ على السرية (reasonable secrecy measures). أما الخيارات الأخرى فتسيء عرض القانون. (انظر 🟡 التعمق أكثر (Going deeper).)

</details>

## 📚 المراجع (References)
- قانون الذكاء الاصطناعي الأوروبي (EU AI Act)، اللائحة (EU) 2024/1689: https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- اللائحة العامة لحماية البيانات (GDPR)، اللائحة (EU) 2016/679: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- المجلس الأوروبي لحماية البيانات (European Data Protection Board) (الرأي 28/2024 بشأن نماذج الذكاء الاصطناعي (Opinion 28/2024 on AI models)): https://www.edpb.europa.eu/
- التوجيهة (EU) 2019/790 بشأن حق المؤلف في السوق الرقمية الموحدة (copyright in the Digital Single Market): https://eur-lex.europa.eu/eli/dir/2019/790/oj
- التوجيهة (EU) 2016/943 بشأن الأسرار التجارية (trade secrets): https://eur-lex.europa.eu/eli/dir/2016/943/oj
- مكتب حق المؤلف الأمريكي (US Copyright Office)، حق المؤلف (copyright) والذكاء الاصطناعي (US Copyright Office, Copyright and Artificial Intelligence): https://www.copyright.gov/ai/
- البوابة القانونية القطرية (Qatar legal portal) الميزان (Al Meezan) (القانون رقم 13 لسنة 2016، PDPPL): https://www.almeezan.qa/
- مكتب الذكاء الاصطناعي في المفوضية الأوروبية (European Commission AI Office) وإرشادات قانون الذكاء الاصطناعي (AI Act guidance): https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai

---

# 3.3 — مخاطر الطرف الثالث وسلسلة التوريد (Third-party and supply-chain risk)
*المستوى: 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 3.1، 3.2* · *مجال المعرفة (BoK): I.C*

## ⚡ الدرس في دقيقة (In 60 seconds)
- تشتري معظم المؤسسات من الذكاء الاصطناعي (AI) أكثر بكثير مما تبنيه: منتجات ذكاء اصطناعي من الموردين (vendor AI products)، وميزات ذكاء اصطناعي مدمجة في البرمجيات القائمة (AI features embedded in existing software)، وواجهات برمجة تطبيقات للنماذج الأساسية (foundation-model APIs)، ونماذج مفتوحة المصدر أو مفتوحة الأوزان (open-source or open-weight models)، وخدمات البيانات والوسم (data and labelling services).
- **المساءلة (accountability) لا تنتقل مع الشراء (purchase).** بوصفك مُشغِّلًا (deployer)، تظل مسؤولًا عن طريقة استخدامك للنظام؛ وبموجب EU AI Act، للمُشغِّلين (deployers) واجباتهم الخاصة، بل قد يصبح المُشغِّل مقدّمًا للنظام (provider).
- لحوكمة الذكاء الاصطناعي (AI governance) لدى الطرف الثالث (third-party) أربع مراحل (stages): **الحصر والتصنيف في فئات (inventory and tiering)**، و**العناية الواجبة (due diligence)** (استبيان (questionnaire) خاص بالذكاء الاصطناعي (AI) مع الأدلة (evidence))، و**الضوابط التعاقدية (contractual controls)** (استخدام البيانات (data use)، والإخطار بالتغيير (change notification)، والتدقيق (audit)، والحوادث (incidents)، والملكية الفكرية (intellectual property)، والخروج (exit))، و**الرصد المستمر (ongoing monitoring)**.
- تحتاج النماذج مفتوحة المصدر (open-source models) إلى فحوص خاصة بها: شروط الترخيص (كثير من النماذج (models) "المفتوحة" تحمل قيودًا على الاستخدام)، والمصدر (provenance)، وأمن ملفات النموذج (model files)، ومن يقدّم الدعم (support) لها.
- إشارة الامتحان (Exam cue): حين يتضمن سيناريو أداةً من مورد تسببت في ضرر، فإن أفضل إجابة عادةً تجمع بين مساءلة المؤسسة ذاتها (organisation's own accountability) وضوابط العقد (contract controls) والرصد (monitoring)، لا "إلقاء اللوم على المورد (vendor)".
- الفخ الأكبر (Biggest trap): الاعتماد على الادعاءات التسويقية (marketing claims) للمورد ("خالٍ من التحيّز (bias-free)"، "ممتثل (compliant)") بدلًا من الأدلة (evidence)، والاختبار في سياقك الخاص، والحقوق التعاقدية (contractual rights).

## 🧭 لماذا يهم (Why it matters)
وقّع يوسف من قسم المشتريات (procurement) عقد أداة فرز السير الذاتية (CV-screening tool) لبنك نجم (Najm Bank) قبل عامين على نموذج عقد البرمجيات القياسي (standard software template). ولا يذكر العقد (contract) شيئًا عن بيانات التدريب (training data)، أو اختبار التحيّز (bias testing)، أو استخدام بيانات المرشحين (candidate data) الخاصة بنجم، أو تغييرات النموذج (model). والآن تريد إدارة الموارد البشرية (HR) في فرانكفورت استخدام الأداة للتوظيف (hiring) في الاتحاد الأوروبي (EU). والتوظيف واختيار المرشحين (Recruitment and candidate selection) مدرجان بوصفهما عالي المخاطر (high-risk) في الملحق III (Annex III) من EU AI Act، ما يجعل نجم مُشغِّلًا (deployer) لنظام عالي المخاطر عليه واجبات قانونية خاصة، وبعضها (مثل اتباع تعليمات الاستخدام (instructions for use) ورصد النظام (monitoring the system)) مستحيل دون تعاون المورد (vendor's cooperation).

وفي الوقت نفسه، يعمل مساعد الائتمان (credit copilot) على نموذج أساسي يُوصل إليه عبر واجهة برمجة تطبيقات (API)؛ وقد غيّر المورد (vendor) إصدار النموذج الأساسي (foundation model) مرتين هذا العام بإشعار في سجل التغييرات المخصص للمطورين (developer changelog). وقد نزّل فريق دانة نموذجًا (model) مفتوح الأوزان (open-weight) من منصة عامة (public hub) لتلخيص سرديات الاحتيال (fraud-narrative) دون أن يتحقق أحد من ترخيصه. وقد حُمّلت Air Canada المسؤولية عمّا قاله روبوت المحادثة (chatbot) الخاص بها لأحد العملاء؛ فشراء نظام أو تنزيله لا يعفيك من هذا النوع من المخاطر.

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**أنواع الذكاء الاصطناعي لدى الطرف الثالث (Kinds of third-party AI).**

| النوع | مثال من نجم | المخاطر الرئيسية |
|---|---|---|
| منتج ذكاء اصطناعي من مورد (Vendor AI product) | أداة فرز السير الذاتية (CV-screening tool) | نموذج غامض (Opaque model)، وتحيّز (bias)، واستخدام المورد (vendor) لبياناتك، ووصول محدود للاختبار (limited testing access) |
| ذكاء اصطناعي مدمج في برمجيات قائمة (AI embedded in existing software) | ميزة "رؤى الذكاء الاصطناعي (AI insights)" الجديدة المفعّلة في منصة إدارة علاقات العملاء (CRM) | يصل الذكاء الاصطناعي (AI) دون مراجعة المشتريات (procurement review)؛ وتتغير تدفقات البيانات (data flows) بصمت |
| واجهة برمجة تطبيقات لنموذج أساسي (Foundation-model API) | النموذج (model) الذي يقف خلف مساعد الائتمان (credit copilot) | تغيّر النموذج دون إشعار (Model changes without notice)، واحتفاظ المزوّد بالبيانات (data retention by provider)، والانقطاعات (outages)، والتركّز (concentration) لدى عدد قليل من المزوّدين (providers) |
| نموذج مفتوح المصدر / مفتوح الأوزان (Open-source / open-weight model) | نموذج (model) منزَّل لملخّصات الاحتيال | قيود الترخيص (Licence restrictions)، وبيانات تدريب مجهولة (unknown training data)، وملفات خبيثة أو معبوث بها (malicious or tampered files)، وغياب دعم المورد (no vendor support) |
| خدمات البيانات والوسم (data and labelling services) | مجموعات بيانات الوسيط (Broker datasets)، والوسم المسند إلى جهات خارجية (outsourced labelling) | المصدر (provenance) والحقوق (انظر 3.2)، وقضايا العمالة والجودة (labour and quality issues) |

**المساءلة تبقى عندك (Accountability stays with you).** المبدأ المحوري (central principle): المؤسسة التي تستخدم نظام ذكاء اصطناعي (AI system) من طرف ثالث (third party) تظل مسؤولة عن نتائج ذلك الاستخدام. فالجهات الرقابية (regulators) والمحاكم تنظر إلى المؤسسة التي اتخذت القرار بشأن العميل أو المرشح. ويمكن للعقود (contracts) أن توزّع التكاليف وواجبات التعاون (cooperation duties) بين الأطراف، لكنها لا تُسقط التزاماتك تجاه الأشخاص المتأثرين (affected people).

**سلسلة القيمة في EU AI Act (EU AI Act value chain).** يوزّع القانون الواجبات بحسب الدور (role):

- **مقدّمو الأنظمة (Providers)** (من يطوّرون نظام ذكاء اصطناعي (AI system) أو يكلّفون بتطويره ويطرحونه في السوق باسمهم) يتحملون معظم التزامات الأنظمة عالية المخاطر (high-risk): إدارة المخاطر (risk management)، وحوكمة البيانات (data governance)، والوثائق التقنية (technical documentation)، وتعليمات الاستخدام (instructions for use)، وتقييم المطابقة (conformity assessment).
- **المُشغِّلون (Deployers)** (من يستخدمون نظام ذكاء اصطناعي (AI system) تحت سلطتهم في سياق مهني (professional context)) يجب عليهم، بالنسبة للأنظمة عالية المخاطر (high-risk)، استخدامها وفقًا لتعليمات الاستخدام (instructions for use)، وإسناد الإشراف البشري (human oversight) إلى أشخاص أكفاء، وضمان أن تكون بيانات الإدخال (input data) الخاضعة لسيطرتهم ذات صلة وممثِّلة بدرجة كافية (sufficiently representative)، ورصد التشغيل (monitor operation) وإبلاغ مقدّم النظام (provider) بالمخاطر أو الحوادث الجسيمة (serious incidents)، والاحتفاظ بالسجلات (keeping records)، وإبلاغ ممثلي العمال (workers' representatives) والعمال المتأثرين (affected workers) قبل استخدام ذكاء اصطناعي عالي المخاطر في مكان العمل (workplace). ويجب على بعض المُشغِّلين، ومنهم من يستخدمون الذكاء الاصطناعي (AI) لتقييم الجدارة الائتمانية (credit scoring) للأشخاص الطبيعيين (natural persons)، إجراء تقييم الأثر على الحقوق الأساسية (fundamental rights impact assessment) (المادة 27 (Art. 27)).
- **المستوردون والموزّعون (Importers and distributors)** عليهم واجبات تحقق (verification duties) عند إدخال الأنظمة إلى سوق الاتحاد الأوروبي (EU market).
- يصبح المُشغِّل (deployer) أو أي طرف ثالث (third party) آخر **مقدّمًا للنظام** إذا وضع اسمه أو علامته التجارية (name or trademark) على نظام عالي المخاطر (high-risk)، أو أدخل عليه تعديلًا جوهريًا (substantial modification)، أو غيّر الغرض المقصود (intended purpose) لنظام ما بحيث يصبح عالي المخاطر (المادة 25 (Art. 25)). فإذا أعاد نجم تسمية أداة السير الذاتية لتصبح "Najm TalentMatch" أو أعاد تدريبها تدريبًا جوهريًا (retrains it substantially)، فقد يرث التزامات مقدّم النظام (provider obligations).

**أربع مراحل (stages) لحوكمة الذكاء الاصطناعي (AI governance) لدى الطرف الثالث (third-party).**

```mermaid
flowchart RL
    I[التحديد والتصنيف] --> DD[العناية الواجبة]
    DD --> C[الضوابط التعاقدية]
    C --> M[الرصد المستمر]
    M -->|تغيير أو مشكلة| DD
    M --> X[الخروج أو التجديد]
```

### 🟡 التعمق أكثر (Going deeper)

**التحديد والتصنيف (Identify and tier).** المشتريات (procurement) هي نقطة الاختناق (choke point). فلكل عملية شراء (purchase) وتجديد، يسأل إجراء المشتريات (procurement procedure) في نجم الآن ما إذا كان المنتج يستخدم الذكاء الاصطناعي (AI) أو سيضيفه. فإن كان الجواب نعم، تُسجَّل عملية الشراء في سجل أنظمة الذكاء الاصطناعي (AI inventory) وتُصنَّف مثل أي حالة استخدام (use case) داخلية (3.1). ويُلتقط الذكاء الاصطناعي المدمج (Embedded AI) عند التجديد (renewal).

**العناية الواجبة (due diligence).** متناسبة (proportionate) مع الفئة. ويكمّل استبيانُ عناية واجبة (due-diligence questionnaire) خاص بالذكاء الاصطناعي (AI) الفحوصَ المعتادة للأمن (security) والخصوصية (privacy) والوضع المالي (financial):

| المجال (Area) | أسئلة نموذجية (Sample questions) | الأدلة المطلوبة (Evidence to ask for) |
|---|---|---|
| الغرض المقصود والحدود (Intended purpose and limits) | لأي غرض صُمّم النظام وجرت المصادقة (validation) عليه؟ ما القيود المعروفة (Known limitations) والاستخدامات غير الملائمة (unsuitable uses)؟ | تعليمات الاستخدام (instructions for use)، وبطاقة النموذج أو النظام (model or system card) |
| الوضع التنظيمي (Regulatory status) | هل النظام عالي المخاطر (high-risk) بموجب EU AI Act؟ هل أنتم مقدّم النظام (provider)؟ ما حالة المطابقة (Conformity status)؟ | إعلان المطابقة الأوروبي (EU declaration of conformity) والتسجيل (registration) حيث ينطبق |
| بيانات التدريب (training data) | المصادر، والحقوق، والبيانات الشخصية (personal data)، ومدى التمثيل (representativeness) لفئتنا السكانية (our population) | وثائق البيانات (Data documentation)، وملخص محتوى التدريب (training content summary) لنماذج (models) GPAI |
| الأداء والعدالة (Performance and fairness) | الدقة (accuracy) ومعدلات الخطأ (error rates) بحسب الفئات ذات الصلة (relevant groups)؛ ومنهجية الاختبار (test methodology) | تقارير الاختبار (Test reports)؛ ونتائج التدقيق المستقل (independent audit results)؛ والإذن بإجراء اختباراتنا الخاصة (our own testing) |
| قابلية التفسير (explainability) | ما التفسيرات التي يمكن تقديمها للمستخدمين (users) والأشخاص المتأثرين (affected people)؟ | نماذج من المخرجات (Sample outputs)، ورموز الأسباب (reason codes) |
| الإشراف البشري (human oversight) | ما الضوابط (controls) المتاحة للمشرفين (overseers) لفهم النظام أو تجاوزه أو إيقافه؟ | عرض توضيحي للواجهة (Interface demo)، والوثائق (documentation) |
| استخدام البيانات (data use) | هل تستخدمون مدخلاتنا أو مخرجاتنا لتدريب النماذج (model training) أو تحسينها؟ ما مدة الاحتفاظ (retention)؟ الموقع؟ المعالِجون الفرعيون (Subprocessors)؟ | اتفاقية معالجة البيانات (Data processing agreement)، وقائمة المعالِجين الفرعيين (subprocessor list) |
| الأمن (security) | الحماية من حقن الأوامر (prompt injection)، وتسميم البيانات (data poisoning)، واستخراج النموذج (model extraction)؛ والتطوير الآمن (secure development) | الشهادات الأمنية (Security certifications)، وملخصات اختبارات الاختراق (penetration test) |
| إدارة التغيير (change management) | كيف ومتى تغيّرون النماذج (models)؟ هل ستخطروننا؟ | سياسة الإصدارات (Release policy)، وإدارة الإصدارات (versioning) |
| الحوادث (incidents) | كيف تكتشفون حوادث الذكاء الاصطناعي (AI incidents) وتتعاملون معها وتخطرون بها؟ | عملية التعامل مع الحوادث (Incident process)، وسجل الحوادث السابقة (past incident history) |
| الحوكمة (governance) | هل لديكم نظام لإدارة الذكاء الاصطناعي (AI management system) أو برنامج للذكاء الاصطناعي المسؤول (responsible AI programme)؟ | شهادة ISO/IEC 42001 (ISO/IEC 42001 certificate) إن وُجدت؛ والسياسات (policies) |
| الاعتماد على النماذج الأساسية (Foundation-model dependencies) | على أي نماذج أساسية (foundation models) أو مكونات من أطراف ثالثة (third-party components) يعتمد منتجكم؟ | قائمة المكونات (Component list) |

لا تتوقف عند الاستبيان (questionnaire): بالنسبة للأنظمة عالية الفئة (high-tier)، اختبر في سياقك الخاص وببياناتك الخاصة.

**الضوابط التعاقدية (contractual controls).** يتضمن ملحق عقود الذكاء الاصطناعي (AI contract schedule) في نجم ما يلي:

- **استخدام البيانات (data use):** عدم استخدام مدخلات نجم (Najm's inputs) أو مخرجاته أو بيانات عملائه (its customer data) لتدريب (training) نماذج المورد (vendor models) أو تحسينها دون اتفاق صريح؛ وحدود للاحتفاظ (retention limits)؛ وموقع البيانات (data location)؛ والموافقة على المعالِجين الفرعيين (subprocessor approval)؛ واتفاقية معالجة بيانات (data processing agreement) تستوفي المادة 28 (Art. 28) من GDPR حيث يعالج المورد (vendor) بيانات شخصية (personal data) بصفته معالِجًا (processor).
- **الشفافية والتوثيق (Transparency and documentation):** تسليم تعليمات الاستخدام (instructions for use) والمعلومات التقنية (technical information) اللازمة لالتزامات نجم الخاصة (تقييم الأثر على حماية البيانات (DPIA)، وتقييم الأثر على الحقوق الأساسية (FRIA)، والإشراف البشري (human oversight)، والتفسيرات للعملاء).
- **الإخطار بالتغيير (change notification):** إشعار مسبق (Advance notice) بالتغييرات الجوهرية (material changes) في النموذج (model) أو البيانات (data) أو الميزات؛ والحق في الاختبار (right to test) قبل سريان التغييرات بالنسبة للاستخدامات (uses) عالية الفئة (high-tier)؛ وتثبيت الإصدار (version pinning) حيثما أمكن.
- **التزامات الأداء والعدالة (Performance and fairness commitments):** مقاييس متفق عليها (agreed metrics)، وإعداد التقارير، والمعالجة (reporting and remediation).
- **حقوق التدقيق والاختبار (Audit and testing rights):** حقوق لنجم ومدققيه والجهات الرقابية (regulators) في الوصول إلى المعلومات والاختبار والتدقيق (audit).
- **الإخطار بالحوادث (incident notification):** مهل زمنية لإخطار نجم بالحوادث (incidents) والاختراقات الأمنية (security breaches) والأعطال الجسيمة (serious malfunctions)؛ والتعاون في التحقيقات والإبلاغ التنظيمي (regulatory reporting).
- **التعاون التنظيمي (Regulatory cooperation):** تعاون المورد (vendor's cooperation) مع التزامات نجم بموجب EU AI Act وحماية البيانات (data protection) وتجاه الجهات الرقابية المصرفية (banking regulator).
- **الملكية الفكرية (intellectual property):** ضمانات بشأن الحقوق في بيانات التدريب (rights to training data)؛ وتعويضات عن مطالبات الأطراف الثالثة المتعلقة بالملكية الفكرية (third-party IP claims) الناشئة عن المخرجات (outputs)؛ ووضوح بشأن ملكية المخرجات (ownership of outputs) والنماذج المضبوطة ضبطًا دقيقًا (fine-tuned models).
- **المسؤولية والتأمين والخروج (Liability, insurance and exit):** إعادة البيانات (data) وحذفها، ودعم الانتقال (transition support)، والاستمرارية (continuity) إذا سحب المورد (vendor) النموذج (model).

بالنسبة لمقدّمي الأنظمة (providers) عالية المخاطر (high-risk)، يتوقع EU AI Act أيضًا وجود اتفاقيات مكتوبة (written agreements) مع الأطراف الثالثة (third parties) التي تورّد أنظمة ذكاء اصطناعي (AI systems) أو أدوات أو خدمات أو مكونات مدمجة في النظام عالي المخاطر، تحدد المعلومات والقدرات والوصول التقني والمساعدة اللازمة لاستيفاء متطلبات القانون (المادة 25 (Art. 25))، وينص على أن يضع مكتب الذكاء الاصطناعي (AI Office) شروطًا تعاقدية نموذجية طوعية (voluntary model contractual terms). وفي الخدمات المالية (financial services)، تنطبق أيضًا القواعد القطاعية (sector rules) بشأن الإسناد الخارجي ومخاطر الأطراف الثالثة في تقنية المعلومات والاتصالات (ICT third-party risk)؛ ففي الاتحاد الأوروبي، يسري قانون المرونة التشغيلية الرقمية (Digital Operational Resilience Act) (DORA، اللائحة (EU) 2022/2554) منذ يناير 2025 على ترتيبات الأطراف الثالثة في تقنية المعلومات والاتصالات (ICT) لدى الكيانات المالية (financial entities) الواقعة ضمن نطاقه. أكّد النطاق لأي كيان بعينه.

**الرصد المستمر (ongoing monitoring).** أنظمة الذكاء الاصطناعي (AI systems) تتغير. ويشمل الرصد (monitoring) تتبّع ملاحظات الإصدار (release notes) وإصدارات النماذج (model versions)، وإجراء فحوص دورية للأداء والعدالة (Performance and fairness) على نتائج نجم الخاصة، ومراجعة الشكاوى (complaints) وحالات التجاوز (overrides)، وإعادة تقييم المورد (re-assessing the vendor) سنويًا أو عند أي تغيير جوهري (material).

### 🔴 نظرة الخبير (Expert view)

**النماذج الأساسية تنشئ سلسلة توريد متعددة الطبقات (Foundation models create a layered supply chain).** يشمل مساعد الائتمان (credit copilot) ثلاثة أطراف على الأقل: مقدّم النموذج الأساسي (foundation-model provider)، ومنصة أو جهة تكامل (integrator)، ونجم الذي يهيّئ الأوامر النصية (prompts) والاسترجاع (retrieval). ويمكن لكل طبقة أن تُدخل مخاطر، ولكل منها معرفة مختلفة. ويعالج EU AI Act ذلك جزئيًا عبر التزامات على مقدّمي نماذج الذكاء الاصطناعي للأغراض العامة (المادة 53 (Art. 53))، بما في ذلك الوثائق التقنية (technical documentation)، والمعلومات والوثائق (documentation) لمقدّمي الأنظمة اللاحقين (downstream providers) الذين يدمجون النموذج (model) في أنظمتهم، وسياسة (policy) لحق المؤلف (copyright)، وملخص علني لمحتوى التدريب (public summary of training content)؛ ولمقدّمي نماذج GPAI (GPAI model providers) ذات المخاطر النظامية (systemic risk) (المفترضة عند تجاوز 10^25 عملية فاصلة عائمة (floating-point operations) من الحوسبة في التدريب (training compute)) واجبات إضافية مثل التقييمات، والاختبار العدائي (adversarial testing)، والإبلاغ عن الحوادث (incident reporting)، والأمن السيبراني (cybersecurity). ومدونة الممارسات (Code of Practice) لنماذج (models) GPAI (GPAI Code of Practice) المنشورة في يوليو 2025 أداة طوعية يمكن لمقدّمي النماذج (model providers) استخدامها لإثبات الامتثال (compliance). وبوصف نجم مستخدمًا لاحقًا في السلسلة (downstream user)، ينبغي له طلب هذه الوثائق والتحقق مما إذا كان مقدّم النموذج الذي يتعامل معه قد وقّع على المدونة. ويدرج أيضًا ملف الذكاء الاصطناعي التوليدي (Generative AI Profile) من NIST (NIST AI 600-1) مخاطر سلسلة القيمة (value chain) ودمج المكونات (component integration) ضمن المخاطر الفريدة للذكاء الاصطناعي التوليدي (GenAI) أو التي يفاقمها.

**النماذج مفتوحة المصدر ومفتوحة الأوزان (Open-source and open-weight models).** كلمة "مفتوح" تشمل أشياء كثيرة: فبعض النماذج (models) يستخدم تراخيص مفتوحة المصدر متساهلة (permissive open-source licences)، بينما يحمل كثير من النماذج "مفتوحة الأوزان (open-weight)" تراخيص مخصصة (custom licences) فيها قيود على الاستخدام أو عتبات تجارية (commercial thresholds). ويضع تعريف الذكاء الاصطناعي مفتوح المصدر (Open Source AI Definition) الصادر عن مبادرة المصدر المفتوح (Open Source Initiative) عام 2024 معيارًا (standard) أعلى من مجرد نشر الأوزان (releasing weights). وتشمل فحوص الحوكمة (governance) للنماذج المفتوحة (open models): مراجعة قسم الشؤون القانونية (Legal) للترخيص (licence)؛ والمصدر (الناشر الرسمي (official publisher) مقابل إعادة رفع (re-upload))؛ وسلامة الملفات (بعض صيغ ملفات النماذج (model file formats) يمكنها تنفيذ شيفرة عند تحميلها، فاستخدم صيغًا آمنة (safe formats) وفحصًا)؛ والوثائق (documentation) المتاحة عن بيانات التدريب (training data) والتقييمات؛ وخطة للدعم (support) والترقيع (patching)، لأنه لا يوجد مورد (vendor) يمكن الاتصال به. وبموجب EU AI Act، يستفيد الذكاء الاصطناعي (AI) الصادر بتراخيص حرة ومفتوحة المصدر (free and open-source licences) من إعفاءات (exemptions) معينة، لكن ليس إذا طُرح في السوق نظامًا عالي المخاطر (high-risk)، أو وقع تحت المحظورات (prohibitions)، أو استدعى التزامات الشفافية (transparency obligations)؛ ونماذج GPAI مفتوحة المصدر (open-source) معفاة من بعض واجبات التوثيق (documentation duties) ما لم تنطوِ على مخاطر نظامية (systemic risk).

**في الاتجاهين (Both directions).** حين يقدّم نجم لعملائه من المنشآت الصغيرة والمتوسطة (SME) ميزة للتنبؤ بالتدفقات النقدية (cash-flow forecasting) قائمة على الذكاء الاصطناعي (AI)، يكون نجم هو المورد (vendor)، ويجب عليه الإجابة عن الاستبيانات (answer the questionnaires) التي يرسلها إلى الآخرين. ويتناول الملحق A (Annex A) من **ISO/IEC 42001** العلاقات مع الأطراف الثالثة (third parties) *و*العملاء معًا، وتغطي وظيفة Govern في **NIST AI RMF** مخاطر الذكاء الاصطناعي (AI risk) الناشئة عن برمجيات الأطراف الثالثة وبياناتها وسلاسل التوريد (supply chains).

**التركّز والخروج (Concentration and exit).** يرتكز جزء كبير من السوق على عدد قليل من مقدّمي النماذج الأساسية (foundation-model providers) والخدمات السحابية (cloud providers)؛ وقد يؤدي انقطاع واحد أو سحب نموذج (model) واحد إلى تعطيل أنظمة كثيرة في آن واحد. سجّل الاعتماديات (dependencies)، وصمّم من أجل قابلية النقل (مجموعات تقييم (evaluation suites) تتيح لك اختبار نموذج بديل (replacement model) بسرعة)، واحتفظ بخطط خروج (exit plans) للأنظمة الحرجة (critical systems).

## ⚖️ الأدوات التنظيمية (The instruments)
| الأداة | ما تشترطه أو توصي به (What it requires or recommends) | إشارة الامتحان (Exam cue) |
|---|---|---|
| **EU AI Act** — المادة 25 (Art. 25) | المسؤوليات على امتداد سلسلة القيمة (Responsibilities along the value chain)؛ يصبح المُشغِّل (deployer) أو الطرف الثالث (third party) مقدّمًا للنظام بإعادة التسمية التجارية (rebranding)، أو التعديل الجوهري (substantial modification)، أو تغيير الغرض المقصود (intended purpose) إلى غرض عالي المخاطر (high-risk)؛ واتفاقيات مكتوبة (written agreements) مع موردي المكونات (component suppliers) | إعادة التسمية التجارية (rebranding) لنظام عالي المخاطر (high-risk) أو تعديله جوهريًا (substantially modifying) قد يجعلك مقدّم النظام (provider) |
| **EU AI Act** — المادة 26 (Art. 26) | واجبات المُشغِّل (deployer duties) في الذكاء الاصطناعي (AI) عالي المخاطر (high-risk): اتباع التعليمات (follow instructions)، والإشراف البشري (human oversight)، وبيانات الإدخال (input data) ذات الصلة، والرصد (monitoring)، والسجلات (logs)، وإبلاغ العمال (informing workers) | شراء النظام لا يُسقط واجبات المُشغِّل (deployer duties) |
| **EU AI Act** — المادة 53 (Art. 53) | مقدّمو نماذج GPAI (GPAI model providers): الوثائق التقنية (technical documentation)، والمعلومات لمقدّمي الأنظمة اللاحقين (information for downstream providers)، وسياسة (policy) حق المؤلف (copyright)، وملخص محتوى التدريب (training content summary) | اطلب هذه الوثائق (documentation) من مقدّمي النماذج الأساسية (foundation-model providers) |
| **GDPR** — المادة 28 (Art. 28) | الشروط التعاقدية (Contract terms) حين يعالج المورد (vendor) بيانات شخصية (personal data) بصفته معالِجًا (processor) | موردو الذكاء الاصطناعي (AI vendors) الذين يعالجون بيانات العملاء (customer data) يحتاجون إلى اتفاقية معالجة بيانات (DPA) |
| **NIST AI RMF** — وظيفة Govern | سياسات (policies) وإجراءات لمخاطر الذكاء الاصطناعي (AI risk) الناشئة عن برمجيات الأطراف الثالثة (third parties) وبياناتها وسلسلة التوريد (supply chain) | مخاطر الطرف الثالث (third-party risk) جزء من الحوكمة (governance)، لا من المشتريات (procurement) فقط |
| **NIST AI 600-1** | ملف الذكاء الاصطناعي التوليدي (Generative AI Profile)؛ ويشمل مخاطر سلسلة القيمة (value chain) ودمج المكونات (component integration) | سلاسل توريد الذكاء الاصطناعي التوليدي (GenAI supply chains) تحتاج إلى شفافية إضافية |
| **ISO/IEC 42001** — الملحق A (Annex A) | ضوابط (controls) للعلاقات مع الأطراف الثالثة والعملاء (third-party and customer relationships)، بما في ذلك توزيع المسؤوليات (allocating responsibilities) وإدارة الموردين (supplier management) | يغطي مورديك (your suppliers) وعملاءك على حد سواء |
| **DORA** — اللائحة (EU) 2022/2554 | إدارة مخاطر تقنية المعلومات والاتصالات (ICT) ومخاطر الأطراف الثالثة (third-party risk) فيها للكيانات المالية (financial entities) الأوروبية الواقعة ضمن النطاق | القواعد القطاعية (sector rules) تضاف إلى القواعد الخاصة بالذكاء الاصطناعي (AI) بالنسبة للبنوك؛ أكّد النطاق |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
**قائمة التحقق للعناية الواجبة والتعاقد مع موردي الذكاء الاصطناعي (AI vendor due-diligence and contracting checklist)** التي أعدّها يوسف وليلى لأداة فرز السير الذاتية (فئة عليا (High tier)):

| الخطوة (Step) | الإجراء | المالك (owner) | الحالة (Status) |
|---|---|---|---|
| 1 | تسجيل الأداة في سجل أنظمة الذكاء الاصطناعي (AI inventory)؛ وتصنيفها عالية المخاطر (التوظيف (hiring) ضمن الملحق III (Annex III))؛ وتسجيل نجم بوصفه مُشغِّلًا (deployer) | ليلى | منجز (Done) |
| 2 | التحقق من محفّزات التحول إلى مقدّم نظام (provider triggers): لا إعادة تسمية تجارية (rebranding)، ولا تعديل جوهري (substantial modification)، والغرض المقصود (intended purpose) دون تغيير | الشؤون القانونية (Legal) | منجز (Done): يبقى نجم مُشغِّلًا (deployer) |
| 3 | إرسال استبيان العناية الواجبة (due-diligence questionnaire) الخاص بالذكاء الاصطناعي (AI)؛ وطلب تعليمات الاستخدام (instructions for use)، وإعلان المطابقة (declaration of conformity) وتفاصيل التسجيل (registration)، وتقارير اختبار العدالة (fairness testing) | يوسف | مُرسَل (Sent) |
| 4 | إجراء اختبار الأثر السلبي (adverse-impact test) الخاص بنجم على 12 شهرًا من الطلبات التاريخية المجهّلة (anonymised historical applications) | دانة مع الموارد البشرية (HR) | مُجدوَل (Scheduled) |
| 5 | تقييم الأثر على حماية البيانات (data protection impact assessment) لبيانات المرشحين (candidate data)؛ وتأكيد أن المورد (vendor) معالِج؛ واتفاقية معالجة بيانات (data processing agreement) وفق المادة 28 (Art. 28)؛ وعدم التدريب (training) على بيانات نجم (Najm data) | سارة | قيد التنفيذ (In progress) |
| 6 | إبلاغ ممثلي العمال (workers' representatives) في فرانكفورت قبل الاستخدام | الموارد البشرية (HR) | مخطَّط (Planned) |
| 7 | تعديل العقد (Contract amendment): ملحق الذكاء الاصطناعي (استخدام البيانات (data use)، والإخطار بالتغيير (change notification) بإشعار مدته 30 يومًا للتغييرات الجوهرية (material changes)، وحقوق التدقيق والاختبار (Audit and testing rights)، والإخطار بالحوادث (incident notification)، والتعاون التنظيمي (Regulatory cooperation)، والتعويض عن الملكية الفكرية (IP indemnity)، والخروج (exit)) | يوسف مع الشؤون القانونية (Legal) | قيد الصياغة (Drafting) |
| 8 | تدريب مسؤولي التوظيف (Recruiter training) على الإشراف (oversight) والتجاوز قبل منح الوصول | الموارد البشرية (HR) | مخطَّط (Planned) |
| 9 | خطة الرصد (Monitoring plan): تحليل ربع سنوي لمعدلات الاختيار بحسب الفئة (selection-rate analysis by group)؛ ومراجعة ملاحظات إصدارات المورد (vendor release-note)؛ وإعادة تقييم سنوية (annual reassessment) | مالك العمل في الموارد البشرية (HR business owner) | مُعَدّة كمسوّدة (Drafted) |
| 10 | موافقة اللجنة على النشر (Committee approval to deploy) في الاتحاد الأوروبي (EU)، مع شروط | لجنة حوكمة الذكاء الاصطناعي (AI Governance Committee) | بانتظار الخطوات (Pending steps) 3–9 |

**قاعدة النماذج مفتوحة المصدر (المضافة إلى معيار دورة حياة الذكاء الاصطناعي (AI Life-cycle Standard)):** "لا يجوز تنزيل النماذج مفتوحة المصدر (open-source models) أو مفتوحة الأوزان (open-weight) إلا من مستودع الناشر الرسمي (official publisher's repository)، وبصيغ ملفات آمنة (safe file formats)، بعد أن يراجع قسم الشؤون القانونية (Legal) الترخيص (licence) في ضوء الاستخدام المقصود (intended use) لنجم، ويُسجَّل النموذج (model) في سجل أنظمة الذكاء الاصطناعي (AI inventory). وتتطلب التجارب (Experiments) التي تستخدم بيانات العملاء (customer data) الموافقات (Approvals) نفسها التي تتطلبها أي حالة استخدام (use case) أخرى للذكاء الاصطناعي (AI)."

## 🛠️ التمارين (Exercises)

### 🟢 مبتدئ (Beginner)
اسرد اعتماديات (dependencies) نجم على الذكاء الاصطناعي (AI) لدى الأطراف الثالثة (third parties) الواردة في هذا الدرس (Lesson)، وصنّف كلًا منها بحسب النوع (منتج مورد (vendor product)، أو مدمج (embedded)، أو واجهة برمجة تطبيقات لنموذج أساسي (Foundation-model API)، أو نموذج مفتوح (open model)، أو خدمة بيانات (data service)).
*يكتمل عندما (Done when):* يكون لكل اعتمادية (dependency) نوع وخطر رئيسي واحد.

### 🟡 متوسط (Intermediate)
اكتب عشرة بنود تعاقدية (جملة واحدة لكل منها) لاتفاقية نجم مع مقدّم النموذج الأساسي (foundation-model provider) لمساعد الائتمان (credit copilot).
*يكتمل عندما (Done when):* تغطي البنود (clauses) استخدام البيانات (data use)، والاحتفاظ (retention) والموقع، والإخطار بالتغيير (change notification)، والإخطار بالحوادث (incident notification)، وحقوق التدقيق (audit rights) أو المعلومات، والتعاون التنظيمي (Regulatory cooperation)، والملكية الفكرية (intellectual property)، والخروج (exit).

### 🔴 متقدم (Advanced)
تريد إدارة الموارد البشرية (HR) إعادة تسمية (rename) أداة السير الذاتية إلى "Najm TalentMatch"، وإعادة تدريبها على بيانات التوظيف (hiring data) الخاصة بنجم، وتقديمها لشركة شقيقة (sister company). حلّل ما إذا كان نجم يصبح مقدّمًا للنظام بموجب EU AI Act، والالتزامات المترتبة على ذلك، وما الذي توصي به.
*يكتمل عندما (Done when):* يطبّق تحليلك محفّزات (triggers) إعادة التسمية التجارية (rebranding) والتعديل الجوهري (substantial modification) والغرض المقصود (intended purpose)، ويسرد التزامات مقدّم النظام (provider obligations) الرئيسية التي ستنطبق، ويقدّم توصية واضحة مع شروط.

## ⚠️ أخطاء وفخاخ الامتحان (Mistakes and exam traps)
- **"المورد (vendor) هو المسؤول."** يحتفظ المُشغِّلون (deployers) بالتزاماتهم الخاصة ويظلون مسؤولين أمام الأشخاص المتأثرين (affected people). اختر الإجابات التي تجمع بين ضوابطك (your controls) وتعاون المورد (vendor's cooperation).
- **الاستبيان وحده (Questionnaire only).** الإجابات المبلَّغ عنها ذاتيًا (Self-reported answers) ليست أدلة (evidence). بالنسبة للأنظمة عالية الفئة (high-tier)، فضّل الإجابات التي تتضمن الاختبار في سياقك وحقوق التدقيق (audit rights) التعاقدية.
- **إغفال الذكاء الاصطناعي المدمج (Missing embedded AI).** ميزات الذكاء الاصطناعي (AI features) المضافة إلى البرمجيات القائمة (existing software) تتجاوز المشتريات (procurement) ما لم تُفحص التجديدات (renewals) وإفصاحات الموردين (vendor disclosures).
- **"المصدر المفتوح يعني بلا قيود (Open source means no restrictions)."** كثير من تراخيص النماذج مفتوحة الأوزان (open-weight licences) يقيّد الاستخدام؛ راجع التراخيص (licences) والمصدر (provenance).
- **نسيان التحول إلى مقدّم نظام (Forgetting provider conversion).** إعادة التسمية التجارية (rebranding)، أو التعديل الجوهري (substantial modification)، أو تغيير الغرض المقصود (intended purpose) قد يحوّل المُشغِّل (deployer) إلى مقدّم نظام بموجب EU AI Act.
- **العناية الواجبة لمرة واحدة (One-off due diligence).** النماذج (models) والموردون (vendors) يتغيرون؛ وبنود الرصد (monitoring) والإخطار بالتغيير (change notification) أساسية.

## 🧾 الخلاصة (Recap)
- يشمل الذكاء الاصطناعي (AI) لدى الأطراف الثالثة (third parties) منتجات الموردين (vendor products)، والميزات المدمجة (embedded)، وواجهات برمجة التطبيقات للنماذج الأساسية (foundation-model APIs)، والنماذج المفتوحة (open models)، وخدمات البيانات (data)، ولكل منها مخاطر مميزة.
- تبقى المساءلة (accountability) عن الاستخدام على عاتق المؤسسة المُشغِّلة (deploying organisation)؛ ويمنح EU AI Act المُشغِّلين (deployers) واجبات خاصة بهم، وقد يحوّلهم إلى مقدّمي (providers) أنظمة.
- احكم سلسلة التوريد (supply chain) في أربع مراحل (stages): التحديد والتصنيف (Identify and tier)، والعناية الواجبة (due diligence) مع الأدلة (evidence) والاختبار الذاتي (own testing)، والضوابط التعاقدية (contractual controls) الخاصة بالذكاء الاصطناعي (AI)، والرصد المستمر (ongoing monitoring) مع خطط الخروج (exit plans).
- على مقدّمي النماذج الأساسية (foundation-model providers) التزامات GPAI بموجب المادة 53 (Art. 53) يمكن للمستخدمين اللاحقين (downstream users) الاعتماد عليها في الحصول على الوثائق (documentation).
- تحتاج النماذج (models) مفتوحة الأوزان (open-weight) إلى فحوص للترخيص (licence)، والمصدر (provenance)، وسلامة الملفات (integrity of files)، والدعم (support).

## ✍️ اختبر نفسك (Check yourself)

**1. يستخدم نجم أداة من مورد (vendor) لفرز السير الذاتية (CV screening) للتوظيف (hiring) في فرعه بالاتحاد الأوروبي (EU). بموجب EU AI Act، ما دور (role) نجم، وهل عليه التزامات؟**

- A. مقدّم النظام (provider)؛ وعليه جميع الالتزامات
- B. مُشغِّل (deployer) لنظام عالي المخاطر (high-risk)؛ وعليه التزاماته الخاصة مثل الإشراف البشري (human oversight) والرصد (monitoring) واتباع تعليمات الاستخدام (instructions for use)
- C. لا دور (role) له، لأنه لم يبنِ الأداة
- D. موزّع (Distributor)؛ وعليه فقط التحقق من علامة CE (CE marking)

<details><summary>الإجابة (Answer)</summary>

**B.** أدوات التوظيف (hiring) عالية المخاطر (high-risk) بموجب الملحق III (Annex III)، ونجم يستخدم النظام تحت سلطته، ما يجعله مُشغِّلًا (deployer) عليه واجبات المادة 26 (Art. 26). والخيار C هو الفخ الكلاسيكي (classic trap). (انظر 🟢 الأساسيات (The essentials).)

</details>

**2. أي إجراء قد يجعل مُشغِّل (deployer) نظام ذكاء اصطناعي (AI system) عالي المخاطر (high-risk) مقدّمًا له بموجب EU AI Act؟**

- A. تدريب (training) موظفيه على النظام
- B. إبلاغ مقدّم النظام (provider) بحادث (incident)
- C. وضع اسمه أو علامته التجارية (name or trademark) على النظام
- D. الاحتفاظ بسجلات النظام (keeping the system's logs)

<details><summary>الإجابة (Answer)</summary>

**C.** إعادة التسمية التجارية (rebranding)، أو التعديل الجوهري (substantial modification)، أو تغيير الغرض المقصود (intended purpose) بحيث يصبح النظام عالي المخاطر (high-risk)، قد يحوّل المُشغِّل (deployer) إلى مقدّم نظام (المادة 25 (Art. 25)). أما الخيارات الأخرى فأنشطة عادية للمُشغِّل. (انظر 🟢 الأساسيات (The essentials).)

</details>

**3. أكمل مورد (vendor) ذكاء اصطناعي (AI) لدى شركة لوجستية (logistics company) استبيانًا (questionnaire) يدّعي فيه أن نموذجه لتحسين المسارات (route-optimisation) "خالٍ من التحيّز (bias-free) وممتثل (compliant) بالكامل". وسيؤثر النظام على نوبات عمل السائقين (drivers' shifts) وأجورهم. ما أفضل خطوة تالية؟**

- A. قبول الإجابة (Answer) وتوقيع العقد (contract)
- B. مطالبة المورد (vendor) بإضافة الادعاء إلى تسويقه
- C. رفض المورد (vendor) لأن كل ذكاء اصطناعي (AI) متحيّز
- D. طلب أدلة داعمة (supporting evidence)، واختبار النظام على بيانات الشركة (company's own data) وسياقها، وتأمين حقوق التدقيق (audit rights) والإخطار بالتغيير (change notification) في العقد (contract)

<details><summary>الإجابة (Answer)</summary>

**D.** الادعاءات تحتاج إلى أدلة (evidence)، واختبار محلي، وحقوق تعاقدية (contractual rights). أما A فيعتمد على الإبلاغ الذاتي (self-reporting)؛ وC غير متناسب (disproportionate). (انظر 🟡 التعمق أكثر (Going deeper).)

</details>

**4. حدّث مقدّم النموذج الأساسي (foundation-model provider) الذي يقف خلف مساعد الائتمان (credit copilot) في نجم نموذجه دون إشعار مباشر، فتغيّرت جودة المخرجات (outputs). أي بند تعاقدي كان سيساعد بصورة مباشرة أكثر من غيره؟**

- A. الإخطار المسبق بالتغييرات الجوهرية (material changes) في النموذج (model) مع الحق في الاختبار (right to test) قبل سريانها
- B. تعويض عن الملكية الفكرية (IP indemnity)
- C. بند بشأن مواقع مكاتب المورد (vendor's office locations)
- D. مدة سداد (payment term) أطول

<details><summary>الإجابة (Answer)</summary>

**A.** الإخطار بالتغيير (change notification) وحقوق الاختبار (testing rights) يعالجان تغييرات النماذج (models) الصامتة. أما التعويض عن الملكية الفكرية (IP indemnity) فيعالج خطرًا مختلفًا. (انظر 🟡 التعمق أكثر (Going deeper)، الضوابط التعاقدية (contractual controls).)

</details>

**5. يريد فريق دانة استخدام نموذج (model) مفتوح الأوزان (open-weight) منزَّل من منصة عامة (public hub). أي فحص هو الأهم قبل الاستخدام؟**

- A. لا شيء، لأن النماذج المفتوحة (open models) لا تحمل أي قيود
- B. التحقق من عدد مرات التنزيل (number of downloads) فقط
- C. مراجعة الترخيص (licence) في ضوء الاستخدام المقصود (intended use)، والتحقق من المصدر (provenance) وسلامة الملفات (integrity of files)، وتسجيل النموذج (model) في السجل (inventory)
- D. مطالبة مؤلفي النموذج (model's authors) بتوقيع عقد الموردين القياسي (standard vendor contract) لنجم

<details><summary>الإجابة (Answer)</summary>

**C.** قد تقيّد تراخيص النماذج مفتوحة الأوزان (open-weight licences) الاستخدام، والمصدر (provenance) وسلامة الملفات (integrity of files) مهمان للأمن (security). والشعبية (Popularity) ليست ضمانة، وكثيرًا ما لا يوجد مورد (vendor) يمكن التعاقد معه. (انظر 🔴 نظرة الخبير (Expert view).)

</details>

## 📚 المراجع (References)
- قانون الذكاء الاصطناعي الأوروبي (EU AI Act)، اللائحة (EU) 2024/1689: https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- مكتب الذكاء الاصطناعي في المفوضية الأوروبية (European Commission AI Office)، مدونة الممارسات (Code of Practice) لنماذج (models) GPAI وإرشادات قانون الذكاء الاصطناعي (AI Act guidance): https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
- اللائحة العامة لحماية البيانات (GDPR)، اللائحة (EU) 2016/679: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- قانون المرونة التشغيلية الرقمية (DORA)، اللائحة (EU) 2022/2554: https://eur-lex.europa.eu/eli/reg/2022/2554/oj
- إطار NIST لإدارة مخاطر الذكاء الاصطناعي (NIST AI Risk Management Framework): https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI 600-1، ملف الذكاء الاصطناعي التوليدي (Generative AI Profile): https://doi.org/10.6028/NIST.AI.600-1
- ISO/IEC 42001:2023: https://www.iso.org/standard/81230.html
- مبادرة المصدر المفتوح (Open Source Initiative)، تعريف الذكاء الاصطناعي مفتوح المصدر (Open Source Initiative, Open Source AI Definition): https://opensource.org/ai
