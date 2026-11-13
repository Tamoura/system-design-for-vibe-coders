# الوحدة 10 — البطل: المشروع الختامي والامتحان التدريبي (Hero: capstone and practice exam)

*لقد تعرّفت على كل جزء من إدارة منتجات الذكاء الاصطناعي (AI product management) درسًا بعد درس. هذه الوحدة تعيد تجميعها معًا. في المشروع الختامي (capstone) تأخذ نجم أسيست (Najm Assist)، مساعد العملاء (customer assistant) في تطبيق الهاتف المحمول (mobile app) لبنك نجم (Najm Bank)، من فكرة غامضة (vague idea) إلى منتج يعمل على نطاق واسع (running at scale)، وتُنتج في الطريق وثيقة (artefact) واحدة من كل وحدة سابقة: موجز الفرصة (opportunity brief)، وبطاقة تقييم حالات الاستخدام (use-case scorecard)، وفحص جاهزية البيانات (data readiness check)، وخريطة الأتمتة (automation map)، والمواصفات مع التقييمات (spec with evals)، وقائمة التحقق من الإطلاق (launch checklist)، وشجرة المقاييس (metrics tree)، ونموذج التكلفة لكل مهمة (cost-per-task model)، وخارطة الطريق (roadmap). ثم ننتقل إليك أنت: كيف تعرض هذا العمل في المقابلات (interviews) وفي ملف الأعمال (portfolio)، وكيف تواصل النمو (keep growing) بوصفك مدير منتجات ذكاء اصطناعي (AI product manager) بعد انتهاء الدورة. وتُختتم الوحدة بامتحان تدريبي (practice exam) من 60 سؤالًا يغطي المراحل الثماني كلها (all eight stages).*

> **المراحل (Stages):** Discover إلى Lead — دورة الحياة كاملة (the whole lifecycle)، من البداية إلى النهاية (end to end)، على منتج واحد (one product) ثم في امتحان واحد (one exam).

---

# 10.1 — المشروع الختامي: خذ نجم أسيست من الفكرة إلى النطاق الواسع (Capstone: take Najm Assist from idea to scale)
*المستوى (Level): 🔴 متقدم (Advanced)* · *المتطلبات (Prerequisites): الوحدات 0–9 (Modules 0–9)* · *المرحلة (Stage): Discover, Define, Design, Build, Evaluate, Launch, Grow, Lead*

## ⚡ الدرس في دقيقة (In 60 seconds)
- يمرّ المشروع الختامي (capstone) بمنتج واحد، هو **نجم أسيست (Najm Assist)**، عبر المراحل الثماني كلها (all eight stages): Discover وDefine وDesign وBuild وEvaluate وLaunch وGrow وLead. وكل مرحلة تُنتج وثيقة واحدة (one artefact) تعلّمت صنعها من قبل.
- كل وثيقة تجيب عن **سؤال قرار (decision question)** («هل تستحق الحل؟ ⁦(worth solving?)⁩»، «كم من الاستقلالية؟ ⁦(how much autonomy?)⁩»، «هل هو جيد بما يكفي للإطلاق؟ ⁦(good enough to ship?)⁩»، «هل يُدرّ عائدًا؟ ⁦(does it pay?)⁩»). إذا لم تغيّر أي قرار (changes no decision)، فاحذفها (cut it).
- الوثائق مترابطة (Artefacts connect): مهمة من الاكتشاف (discovery job) تصبح مهمة تقييم (eval task)؛ ومعيار الجودة في المواصفات (spec quality bar) يصبح بوابة إطلاق (launch gate) ثم تنبيه مراقبة (monitoring alert). والروابط المقطوعة (Broken links) هي حيث تفشل منتجات الذكاء الاصطناعي (AI products fail).
- ينمو نجم أسيست على **درجات أتمتة (automation steps)** — الإجابة (answer)، ثم الإرشاد (guide)، ثم التنفيذ مع التأكيد (act with confirmation) (تجميد بطاقة (freeze a card))، ثم المهام الأعلى خطورة (higher-stakes tasks) (الاعتراضات على المعاملات (disputes)). وكل درجة تعيد فتح مراحل Define وDesign وEvaluate.
- إشارة القرار (Decision cue): قبل كل مرحلة، اكتب «ما الذي سيجعلنا نتوقف؟ ⁦(what would make us stop?)⁩». والخطة التي لا تتضمن معيار إيقاف (kill criterion) هي مجرد عرض ترويجي (pitch).
- أكبر فخ (Biggest trap): التعامل مع المشروع الختامي على أنه تمرين في كتابة الوثائق (document exercise). فالمهارة الحقيقية (The skill) هي الحكم بين الوثائق (judgement between artefacts).

## 🧭 لماذا يهم (Why it matters)
الشهر يناير (January). تعرض رانيا على الفريق شريحة واحدة (one slide): معظم مكالمات مركز الاتصال (contact-centre calls) في العام الماضي دارت حول عدد قليل من المواضيع (handful of topics) — إيقاف البطاقات (card blocks)، والمعاملات المعترض عليها (disputed transactions)، وحدود التحويل (transfer limits)، والرسوم (fees)، و«أين أموالي؟ (where is my money)». الرئيس التنفيذي (CEO) يريد مساعدًا داخل التطبيق (app assistant). يسأل خالد عمّا سيكلّفه وعمّا سيوفّره (cost and save). وتسأل ليلى عمّا يحدث عندما يعطي عميلًا من الاتحاد الأوروبي (EU customer) إجابة خاطئة عن الرسوم (wrong answer about fees). وتسأل سارة أين ستُخزَّن نصوص المحادثات (transcripts will be stored). ويسأل طارق عن زمن الاستجابة (latency)؛ وحصة عمّا يريده العملاء (what customers want).

فيصل يريد عرضًا توضيحيًا (demo) بحلول الخميس. رانيا: «العرض التوضيحي سهل (The demo is easy). الجزء الصعب هو القرارات التي تقع بين العرض التوضيحي ومنتج يأتمنه العملاء على أموالهم (a product customers trust with their money). لنتخذها بالترتيب (in order)، ولنكتب كل قرار منها (write each one down).»

للقرارات التي يتم تخطّيها (Skipped decisions) تكاليف علنية (public costs). في قضية *Moffatt v. Air Canada* (2024)، حمّلت هيئة قضائية (tribunal) شركة الطيران المسؤولية (held the airline responsible) عمّا قاله روبوت المحادثة (chatbot) الخاص بها لعميل بشأن أسعار تذاكر الحداد (bereavement fares). وروبوت محادثة التوصيل (delivery chatbot) لدى DPD شتم وانتقد الشركة بعد تحديث (after an update) في يناير 2024. وأعلنت Klarna في فبراير 2024 أن مساعدها يتولى حصة كبيرة من محادثات العملاء (large share of customer chats)، ثم قالت في 2025 إنها ستعيد مزيدًا من الخدمة البشرية (bring more human service back). كل حالة منها فشل يقع *بين* الوثائق (a failure *between* artefacts): مواصفات بلا قاعدة إسناد (spec without a grounding rule)، وتحديث بلا بوابة انحدار (update without a regression gate)، ومقياس تكلفة بلا ثقل موازن من الجودة (cost metric without a quality counterweight). والمشروع الختامي هو المكان الذي تتدرّب فيه على سدّ هذه الفجوات (closing those gaps).

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**المشروع الختامي (A capstone)** هنا هو مرور واحد من البداية إلى النهاية (end-to-end pass) عبر دورة الحياة (lifecycle) على منتج واحد، يُنتج مجموعة مترابطة من الوثائق (linked set of artefacts): **ملف المنتج (product dossier)**. تسلّمه رانيا إلى مدير منتج جديد (new PM) في يومه الأول؛ وتقرؤه ليلى عند بوابات الحوكمة (governance gates)؛ ويقرؤه خالد قبل اعتماد الميزانية (approving budget).

صفحة الملخص (summary page) في قسم 🏛️ أدناه تسرد الوثائق التسع (nine artefacts)، واحدة أو اثنتين لكل مرحلة (per stage)، وكل منها مربوطة بالدرس الذي علّمها (the lesson that taught it). ثلاث قواعد تجعل الملف يعمل (make the dossier work):

1. **كل وثيقة تذكر قرارها وأدلتها (Every artefact states its decision and its evidence)** («تجميد البطاقة أولًا (card freeze first): متكرر (frequent)، وقابل للتراجع عنه (reversible)، ومنخفض المخاطر (low-risk)»).
2. **كل وثيقة تسمّي مُدخَل الوثيقة التالية (Every artefact names the next one's input).** فأهم المهام في الموجز (brief's top jobs) تصبح شرائح في المجموعة المرجعية (golden-set slices)؛ ومعايير الجودة في المواصفات (spec's quality bars) تصبح بوابات إطلاق (launch gates).
3. **لكل مرحلة قاعدة إيقاف (Every stage has a stop rule).** إذا انطلقت (If it fires)، تعود مرحلة إلى الوراء (go back a stage) أو تقتل الفكرة (kill the idea). وهذا يعني أن العملية تعمل كما ينبغي (the process working).

جميع الأرقام أدناه توضيحية (illustrative).

**الاكتشاف (Discover).** تستمع حصة وفيصل إلى تسجيلات المكالمات (call recordings) (بموافقة سارة (Sara's approval))، ويقرآن مراجعات التطبيق (app reviews)، ويرافقان خمسة من موظفي مركز الاتصال (shadow five contact-centre agents). ويصوغان العمل وفق إطار **المهام المطلوب إنجازها (Jobs to be Done)** (كلايتون كريستنسن (Clayton Christensen)): «عندما أرى معاملة لا أتعرّف عليها (a transaction I don't recognise)، أريد أن أوقف مزيدًا من الضرر (stop further damage) وأستعيد أموالي (get my money back).» و**شجرة الفرص والحلول (Opportunity Solution Tree)** لديهما (تيريزا توريس (Teresa Torres)) فيها نتيجة واحدة (one outcome) (العملاء يحلّون احتياجاتهم الشائعة داخل التطبيق دون انتظار (resolve common needs in the app without waiting))، وأربع فرص (four opportunities) (المعاملات غير المعروفة (unknown transactions)، والبطاقات المفقودة (lost cards)، والرسوم المربكة (confusing fees)، وحدود التحويل (transfer limits))، وحلول مرشحة (candidate solutions) تحت كل فرصة. وبعضها فقط يحتاج إلى الذكاء الاصطناعي (Only some need AI): فصفحة رسوم أوضح (clearer fee page) تعالج جزءًا من الالتباس في الرسوم أفضل من أي روبوت محادثة (better than any chatbot).

**التعريف (Define).** تقيّم بطاقة التقييم (scorecard) كل مرشح من حيث القيمة (value) والجدوى التقنية (feasibility) والمخاطر (risk). الإجابة عن أسئلة الرسوم والسياسات (fee and policy questions) من وثائق البنك تحصل على درجة عالية في القيمة والجدوى التقنية، ومتوسطة في المخاطر (medium on risk) (فالإجابات الخاطئة عن الرسوم مكلفة (wrong fee answers are costly)، كما تعلّمت Air Canada). وتجميد البطاقة (Freezing a card) عالي القيمة ومنخفض المخاطر (high value, low risk)، لأنه قابل للتراجع عنه (reversible). والاعتراض على معاملة (Disputing a transaction) عالي القيمة لكنه أعلى مخاطرة (higher risk): فهو يبدأ عملية منظّمة رقابيًا (regulated process) لها مواعيد نهائية (deadlines). أما المشورة الاستثمارية المخصّصة (Personalised investment advice) فـ**تُقتل (killed)** (مخاطر عالية (high risk)، وقيمة غير واضحة (unclear value)، ومسألة ترخيص (licensing question))، ويُسجَّل السبب (the reason is recorded) حتى لا يُعاد فتحها كل ربع سنة (every quarter).

يسأل فحص جاهزية البيانات (data readiness check) عمّا إذا كان لدى البنك ما تحتاجه كل حالة استخدام (each use case): مجموعة نصوص حالية ومملوكة للرسوم والشروط (current, owned fee and terms corpus) (جزئيًا (partly) — توجد ثلاث نسخ من جدول الرسوم (fee schedule)، فيسمّي فريق عمر مالكًا واحدًا (one owner))؛ ومحادثات تاريخية للتقييم (historical conversations for evaluation) (نعم، بعد التنقيح وحجب البيانات (after redaction))؛ وواجهات برمجة البطاقات (card APIs) (نعم، يستخدمها التطبيق أصلًا). وتسجّل مذكرة حقوق البيانات (data rights note) التي أعدّتها سارة الأساس القانوني (lawful basis) بموجب قانون حماية خصوصية البيانات الشخصية في قطر (Qatar's PDPPL) (القانون رقم 13 لسنة 2016 (Law No. 13 of 2016)) واللائحة العامة لحماية البيانات (GDPR) للعملاء من الاتحاد الأوروبي، إضافة إلى مدة الاحتفاظ (retention). التفاصيل مكانها دورة *AI Governance: Zero to Hero*؛ أما مدير المنتج (PM) فيتأكد من وجود المذكرة قبل البناء (before build).

### 🟡 التعمق أكثر (Going deeper)

**التصميم (Design).** تبني حصة **خريطة الأتمتة (automation map)** مستخدمةً مستويات الأتمتة (levels of automation) (شيريدان وفيربلانك (Sheridan and Verplank)، 1978) ضمن مستويات المنتج الأربعة في الدورة (course's four product levels): الاقتراح (suggest)، والصياغة (draft)، والقرار (decide)، والتنفيذ (act).

| المهمة (Task) | المستوى عند الإطلاق (Level at launch) | السبب (Why) | شرط الانتقال إلى الأعلى (Condition to move up) |
|---|---|---|---|
| الإجابة عن أسئلة الرسوم والسياسات (Answer fee and policy questions) | اقتراح، مع المصادر (Suggest, with sources) | العميل يقرر ما يفعله (Customer decides what to do) | يبقى هنا (Stays here) |
| تغيير حد التحويل (Change a transfer limit) | صياغة: تعبئة مسبقة، والعميل يرسل (Draft: prefill, customer submits) | العميل يتحكم في حركة الأموال (Customer controls money movement) | معدل خطأ منخفض في التعبئة المسبقة (Low prefill error rate) لمدة ربع سنة |
| تجميد بطاقة (Freeze a card) | تنفيذ، مع التأكيد (Act, with confirmation) | متكرر، وعاجل، وقابل للتراجع بلمسة واحدة (Frequent, urgent, reversible in one tap) | في المستوى المستهدف أصلًا (Already at target) |
| فتح اعتراض (Open a dispute) | صياغة: العميل يؤكد، والموظف يراجع (Draft: customer confirms, agent reviews) | عملية منظّمة رقابيًا، ومواعيد نهائية، وأموال على المحك (Regulated process, deadlines, money at stake) | أدلة من التقييم والتدقيق (Eval and audit evidence)؛ وإعادة موافقة ليلى (Layla's re-approval) |

أنماط الثقة (trust patterns) مأخوذة من دليل **People + AI Guidebook** من Google ومن **Guidelines for Human-AI Interaction** من Microsoft (أمرشي وآخرون ⁦(Amershi et al.)⁩، 2019): صرّح بأنه ذكاء اصطناعي وبما يستطيع فعله (say it is an AI and what it can do)؛ واعرض المصادر (show sources)؛ واطلب التأكيد قبل أي إجراء (confirm before any action)؛ وأبقِ خيار «التحدث إلى شخص (talk to a person)» ظاهرًا؛ وعند عدم اليقين (when unsure)، سلّم المحادثة إلى إنسان مع إرفاق المحادثة (hand over with the conversation attached). وواجب الشفافية (transparency duty) لروبوتات المحادثة في قانون الذكاء الاصطناعي الأوروبي (EU AI Act) يشير إلى الاتجاه نفسه؛ وتؤكد ليلى التفاصيل.

**البناء (Build).** تحوّل المواصفات (spec) القرارات إلى متطلبات قابلة للاختبار (testable requirements):

- *قاعدة الإسناد (Grounding rule):* إجابات الرسوم والسياسات تأتي فقط من مجموعة النصوص المعتمدة (approved corpus) عبر الاسترجاع (retrieval) (التوليد المعزّز بالاسترجاع (RAG))؛ وإذا لم يُعثر على شيء ذي صلة (nothing relevant is found)، يقول المساعد ذلك ويعرض التحويل إلى شخص (offers a person). ولا يجوز أن يظهر أي رسم أو سعر أو حد (No fee, rate or limit) ما لم يكن موجودًا في مصدر مُسترجَع (retrieved source).
- *معايير الجودة على شكل تقييمات (Quality bars as evals):* على سبيل المثال، 95% من أسئلة الرسوم في المجموعة المرجعية (golden-set fee questions) صحيحة مع المصدر الصحيح (right source)، وصفر أرقام غير مُسندة (zero ungrounded numbers) في مجموعة الفريق الأحمر (red-team set)، و100% من الإجراءات مؤكَّدة (actions confirmed) (أرقام توضيحية (illustrative)؛ تضع دانة وفيصل المعايير الحقيقية (real bars) انطلاقًا من خط الأساس (baseline)).
- *الأدوات بوصفها سطحًا للمنتج (Tools as product surface):* عند الإطلاق يحصل المساعد على `get_card_status` و`freeze_card` ولا شيء غيرهما. وتُكتب أوصاف الأدوات (Tool descriptions) كما يُكتب نص واجهة المستخدم (UI copy)، لأن النموذج (model) يقرؤها ليقرر ما يفعله. أما كيفية ربط الأدوات (How tools are connected) (مثلًا عبر **Model Context Protocol**، الذي قدّمته Anthropic في نوفمبر 2024) فهو قرار طارق (Tariq's call).
- *ميزانيات زمن الاستجابة والتكلفة (Latency and cost budgets):* زمن مستهدف لأول رد (target time to first response) وسقف للتكلفة لكل محادثة (cost ceiling per conversation).

قبل ذلك، أجرى فيصل اختبار **Wizard of Oz** («ساحر أوز»: إنسان خلف نافذة المحادثة (a human behind the chat window)) ليتعلم كيف يصوغ العملاء احتياجاتهم (how customers phrase their needs)، ثم نموذجًا أوليًا رفيعًا للاسترجاع (thin retrieval prototype) على مجموعة النصوص الحقيقية (real corpus).

**التقييم (Evaluate).** لخطة التقييم (eval plan) التي وضعتها دانة ثلاث طبقات (three layers)، تطابق الوحدة 6 (Module 6):

1. **دون اتصال (Offline)**: مجموعة مرجعية (golden set) من محادثات حقيقية منقّحة (redacted real conversations)، مقسّمة إلى شرائح حسب المهمة (job) واللغة (language) (الإنجليزية والعربية (English and Arabic)) ودرجة الصعوبة (difficulty). ويقرأ تحليل الأخطاء (Error analysis) حالات الفشل يدويًا (reads failures by hand) قبل أن يعدّل أحد أي موجّه (tunes a prompt).
2. **المحكَّمة والعدائية (Judged and adversarial)**: **نموذج لغوي كبير حَكَمًا (LLM-as-judge)** يقيّم الإسناد (grounding) والنبرة (tone) على نطاق واسع (at scale)، مُعايَرًا مقابل مقيّمين بشريين (calibrated against human raters) لأن للحكّام تحيّزات معروفة (judges have known biases) (جنغ وآخرون ⁦(Zheng et al.)⁩، 2023). ويحاول فريق أحمر (red-team) تنفيذ حقن الموجّهات (prompt injection)، وتجاوز الحدود (limit overrides)، والتلاعب من نوع «سيارة بدولار واحد ("$1 car" manipulation)» الذي شوهد لدى وكيل سيارات Chevrolet في ديسمبر 2023، وأسئلة تستدرج المساعد إلى ذكر رسوم لا يجدها (baiting the assistant to state fees it cannot find).
3. **عبر الإنترنت (Online)**: إطلاق مرحلي (staged rollout) (الموظفون، ثم 1% و10% و50% من المستخدمين) مع **اختبار A/B (A/B test)** مقابل مركز المساعدة الحالي (existing help centre). واتباعًا لكوهافي وتانغ وشو (Kohavi, Tang and Xu)، يتفق الفريق مسبقًا (in advance) على **معيار التقييم الشامل (overall evaluation criterion)** ويضيف **مقاييس وقائية (guardrail metrics)** (الشكاوى (complaints)، ومعدل التحويل إلى إنسان (handoff rate)، وبلاغات الإجابات الخاطئة (wrong-answer reports)) قادرة على إيقاف الإطلاق بمفردها (stop the rollout on their own).

```mermaid
flowchart RL
  D["الاكتشاف: المهام وشجرة الفرص<br/>(Discover: jobs and OST)"] --> F["التعريف: بطاقة التقييم وفحص البيانات<br/>(Define: scorecard and data check)"]
  F --> G["التصميم: خريطة الأتمتة<br/>(Design: automation map)"]
  G --> B["البناء: المواصفات والتقييمات<br/>(Build: spec and evals)"]
  B --> E["التقييم: المجموعة المرجعية والفريق الأحمر والاختبار المقارن<br/>(Evaluate: golden set, red-team, A/B)"]
  E -->|"تحققت المعايير (bars met)"| L["الإطلاق: بوابة الجاهزية<br/>(Launch: readiness gate)"]
  E -->|"لم تتحقق المعايير (bars missed)"| B
  L --> R["النمو: المقاييس والتكلفة والانجراف<br/>(Grow: metrics, cost, drift)"]
  R -->|"مهمة أو مستوى جديد (new task or level)"| F
  R --> K["القيادة: الاستراتيجية وخارطة الطريق<br/>(Lead: strategy and roadmap)"]
  K -->|"الرهان التالي (next bet)"| D
```

**الإطلاق (Launch).** لقائمة التحقق من الجاهزية (readiness checklist) أربع كتل (four blocks): *الجودة (quality)* (تحقُّق كل معيار في المواصفات على النسخة نفسها من النموذج والموجّه التي ستُطلق (exact model and prompt version shipping))، و*الضوابط الوقائية (guardrails)* (المرشحات مفعّلة (filters live)، والتأكيدات مختبَرة (confirmations tested)، ومفتاح إيقاف (kill switch) يعطّل الأدوات خلال دقائق (within minutes))، و*الحوكمة (governance)* (موافقة ليلى، ونتيجة تقييم الأثر على حماية البيانات (DPIA outcome) من سارة، واعتماد نص الإفصاح (disclosure text approved))، و*الدعم (support)* (موظفون مدرَّبون على التحويلات (agents trained on handoffs)، ومالك للحوادث مناوب (incident owner on call)). والتموضع (Positioning) متواضع (modest): «مساعدة سريعة للخدمات المصرفية اليومية (fast help for everyday banking)». ويعتمد التبنّي داخل البنك (Adoption inside the bank) على مركز الاتصال (contact centre): فإذا رأى الموظفون فيه تهديدًا (see a threat)، تتضرر التحويلات (handoffs suffer)، ولذلك تُشرك رانيا رئيسهم (involves their head) منذ مرحلة Discover فصاعدًا.

### 🔴 نظرة الخبير (Expert view)

**النمو (Grow).** تبدأ شجرة المقاييس (metrics tree) لدى فيصل من **مقياس نجم الشمال (North Star metric)** واحد: *احتياجات العملاء التي تُحل داخل التطبيق دون تواصل متكرر خلال سبعة أيام (customer needs resolved in the app without a repeat contact within seven days)*. فمعدل الاحتواء (Containment) (المحادثات التي لا تصل أبدًا إلى إنسان (chats that never reach a human)) يسهل تضخيمه (easy to inflate) بإخفاء خيار «التحدث إلى شخص (talk to a person)»؛ أما الحل دون تواصل متكرر (resolution without repeat contact) فلا. وتحته تقع فئات **HEART** (رودن وهتشنسون وفو (Rodden, Hutchinson and Fu)، 2010) — السعادة (happiness)، والتفاعل (engagement)، والتبنّي (adoption)، والاحتفاظ (retention)، ونجاح المهمة (task success) — ومقاييس الثقة (trust metrics): معدل التحويل إلى إنسان (handoff rate)، وبلاغات الإجابات الخاطئة (wrong-answer reports)، والشكاوى (complaints).

**نموذج التكلفة لكل مهمة (cost-per-task model)**: التكلفة لكل محادثة محلولة (cost per resolved conversation) = (تكلفة النموذج والاسترجاع لكل محادثة (model and retrieval cost per conversation) + تكلفة الأدوات والمنصة (tool and platform cost) + معدل التحويل إلى إنسان × تكلفة التواصل البشري (handoff rate × cost of a human contact) + الأعباء الإضافية للمراقبة (monitoring overhead)) ÷ معدل الحل (resolution rate). بأرقام توضيحية (illustrative numbers) — بضعة سنتات من تكلفة النموذج (a few cents of model cost)، وتواصل بشري يكلّف أضعاف ذلك (many times that)، ومعدل تحويل إلى إنسان يبلغ 25% — فإن التحويلات، لا النموذج، هي التي تهيمن (handoffs, not the model, dominate). لذلك فإن أفضل رافعة للنمو (best growth lever) هي تحسين الحل في أهم المهام (better resolution on the top jobs)، لا نموذج أرخص (not a cheaper model).

تعيد خطة المراقبة (monitoring plan) استخدام المواصفات (reuses the spec). تعمل مجموعة التقييمات (eval suite) كل ليلة (nightly) على عينات منقّحة من المحادثات الحية (sampled, redacted live conversations)؛ وتنطلق التنبيهات (alerts fire) عندما ينخفض الإسناد عن معيار الإطلاق (grounding falls below the launch bar)، أو ترتفع التحويلات في مهمة ما (handoffs rise on a job)، أو تظهر أنواع جديدة من الأسئلة (new question types) لا تغطيها المجموعة المرجعية (الانجراف (drift)، مثلًا بعد جدول رسوم جديد (new fee schedule)). وكل تغيير في النموذج أو الموجّه (model or prompt change) يُشغّل المجموعة الكاملة أولًا (runs the full suite first) — وهي بوابة الانحدار (regression gate) التي افتقدتها حالة DPD.

**القيادة (Lead).** تقول صفحة الاستراتيجية الواحدة (strategy one-pager) التي أعدّتها رانيا إن القابلية للدفاع (defensibility) لا تأتي من النموذج، الذي يستطيع المنافسون شراءه (competitors can buy)، بل من التكامل مع الأنظمة الأساسية (core-system integration)، ومجموعة نصوص حالية (current corpus)، ومحادثات مُصنَّفة (labelled conversations) تشحذ التقييمات (sharpen evals)، والثقة (trust). وخارطة الطريق (roadmap) مجموعة من **الرهانات (bets)** ذات بوابات أدلة (evidence gates)، لا تواريخ ميزات (not feature dates): «صياغة الاعتراضات (dispute drafting)، إذا تجاوز تقييم الربع الثاني المعيار (Q2 eval clears the bar) وأعادت ليلى الموافقة». ومجموعة تقييمات محايدة تجاه النموذج (model-agnostic eval suite) تجعل تبديل المزوّدين (switching providers) مجرد تشغيل تقييم (an eval run)، لا إعادة كتابة (not a rewrite). ويسمّي نموذج التشغيل (operating model) المالكين (owners): فيصل (المنتج والمقاييس (product and metrics))، ودانة (التقييم (evaluation))، وطارق (المنصة وزمن الاستجابة والتكلفة (platform, latency, cost))، ومركز الاتصال (التحويلات (handoffs))، ومكتب ليلى (أي انتقال إلى الأعلى في خريطة الأتمتة (any move up the automation map)). ويسري الذكاء الاصطناعي المسؤول (Responsible AI) في كل وثيقة بدلًا من أن يجلس في فصل أخير (final chapter).

**قرارات الحكم بين الوثائق (The judgement calls between artefacts).** ثلاث لحظات تُظهر الفرق بين مدير منتج بطل (hero PM) وكاتب وثائق (document writer):

- *التقييم يُخفق في بلوغ المعيار بقليل (The eval misses the bar by a little).* الإسناد في الرسوم (Fee grounding) يبلغ 92% مقابل معيار 95%؛ ويريد فيصل «إصلاحه لاحقًا (fix it later)». تحليل الأخطاء أولًا (Error analysis first): إذا تجمّعت الإخفاقات في نوع واحد من الرسوم (misses cluster in one fee type)، فأخرج ذلك النوع من النطاق (remove that type from scope) («دعني أوصلك بموظف (let me connect you)») وأطلق الباقي (launch the rest). تضييق النطاق (Narrowing scope) قرار منتج (product decision)؛ أما خفض المعيار بصمت (quietly lowering the bar) فليس كذلك.
- *اختبار A/B يفوز في التكلفة ويخسر في الثقة (The A/B test wins on cost, loses on trust).* المقياس الوقائي هو الذي يغلب (The guardrail wins)؛ حقّق قبل التوسّع (investigate before expanding).
- *قطاع الأعمال يريد مستوى الأتمتة التالي مبكرًا (The business wants the next automation level early).* يريد خالد اعتراضات مؤتمتة بالكامل (fully automated disputes). وتجيب رانيا بأن ذلك سيحدث عندما تتوافر الأدلة وإعادة الموافقة (when the evidence and re-approval exist)، وتوضح ما يتطلبه ذلك (shows what that takes).

## 🧰 الأدوات (The toolkit)
| الأداة أو الإطار (Tool or framework) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **Product dossier** — ملف المنتج | وثائق مترابطة لمنتج واحد (Linked artefacts for one product)، تذكر كل منها القرار والأدلة وقاعدة الإيقاف (decision, evidence and stop rule) | من الفكرة إلى النطاق الواسع (Idea to scale)؛ وتهيئة مدير منتج جديد (onboarding a PM)؛ وبوابات الحوكمة (governance gates) |
| **Use-case scorecard** — بطاقة تقييم حالات الاستخدام | تقيّم المرشحين من حيث القيمة والجدوى التقنية والمخاطر (value, feasibility and risk)، مع معايير إيقاف صريحة (explicit kill criteria) | مرحلة Define: اختيار حالات الاستخدام الأولى (choosing the first use cases) وتسجيل ما قُتل (recording kills) |
| **Automation map** (استنادًا إلى شيريدان وفيربلانك (after Sheridan and Verplank)) — خريطة الأتمتة | تعيّن لكل مهمة مستوى (assigns each task a level) (اقتراح، صياغة، قرار، تنفيذ (suggest, draft, decide, act)) وشرطًا للانتقال إلى الأعلى (condition for moving up) | مرحلة Design: تحديد الاستقلالية لكل مهمة لا لكل منتج (autonomy per task, not per product) |
| **Golden set** — المجموعة المرجعية | مهام حقيقية مقسّمة إلى شرائح (Sliced real tasks) مع إجابات مرجعية (reference answers) | تحويل المواصفات إلى اختبارات (turning the spec into tests) وبوابات انحدار (regression gates) |
| **Launch readiness checklist** — قائمة التحقق من جاهزية الإطلاق | شروط الجودة والضوابط الوقائية والحوكمة والدعم (Quality, guardrail, governance and support conditions)، وكلها يجب أن تتحقق للإطلاق (all true to ship) | اجتماع قرار المضي أو عدم المضي (go or no-go meeting) |
| **Cost-per-task model** — نموذج التكلفة لكل مهمة | تكلفة خدمة مهمة واحدة محلولة (Cost to serve one resolved task)، بما في ذلك التحويلات إلى البشر (human handoffs) | التقديرات في مرحلة Define (Estimates in Define)، والأرقام الفعلية في مرحلة Grow (actuals in Grow) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
**ملف منتج نجم أسيست — صفحة الملخص (Najm Assist product dossier — summary page)** الذي أعدّه فيصل (الإصدار 1.0 (v1.0)، بمراجعة رانيا). كل صف مربوط بالوثيقة الكاملة (links to the full artefact).

| # | المرحلة (Stage) | الوثيقة (Artefact) | القرار المسجَّل (Decision recorded) | قاعدة الإيقاف (Stop rule) |
|---|---|---|---|---|
| 1 | Discover | موجز الفرصة + شجرة الفرص والحلول (Opportunity brief + OST) (2.1) | التركيز على أربع مهام (Focus on four jobs): المعاملات غير المعروفة (unknown transactions)، والبطاقات المفقودة (lost cards)، والرسوم (fees)، وحدود التحويل (transfer limits) | إذا كانت أهم المهام تحتاج إلى حكم بشري (need human judgement) في معظم الحالات، فلا تبنِ مساعدًا (do not build an assistant) |
| 2 | Define | بطاقة تقييم حالات الاستخدام (Use-case scorecard) (2.2، 2.3) | الإطلاق بإجابات الرسوم والسياسات وتجميد البطاقة (fee/policy answers and card freeze)؛ الاعتراضات لاحقًا (dispute later)؛ المشورة الاستثمارية قُتلت (investment advice killed) | أي مرشح يحصل على مخاطر عالية دون تخفيف (high risk with no mitigation) يُركن جانبًا (is parked) |
| 3 | Define | تقييم جاهزية البيانات + قسم الخصوصية وحقوق البيانات (Data Readiness Assessment + privacy and data rights section) (3.1، 3.3) | مالك واحد لجدول الرسوم (Single owner for fee schedule)؛ نصوص محادثات منقّحة للتقييم (redacted transcripts for eval)؛ تسجيل الأساس القانوني (lawful basis recorded) | لا إطلاق حتى يوجد مصدر رسوم حالي واحد (one current fee source) |
| 4 | Design | سجل قرار مستوى الأتمتة، ومواصفات تصميم الثقة، وكتالوج الإجراءات (Automation Level Decision Record, Trust Design Spec, Action Catalogue) (4.1–4.3) | اقتراح (Suggest) (للإجابات)، وتنفيذ مع التأكيد (act with confirmation) (للتجميد)، وصياغة (draft) (للاعتراضات) | العملاء يسيئون فهم التأكيد في الاختبار (misunderstand the confirmation in testing) ← إعادة التصميم (redesign) |
| 5 | Build | مواصفات منتج الذكاء الاصطناعي + ورقة السلوك (AI product spec + behaviour sheet) (5.1–5.3) | قاعدة الإسناد (Grounding rule)؛ قائمة أدوات مقصورة على أداتين (tool list limited to two)؛ ميزانيات زمن الاستجابة والتكلفة (latency and cost budgets) | معايير جودة لم تتفق عليها دانة وفيصل (Quality bars not agreed) ← لا اعتماد للبناء (no build sign-off) |
| 6 | Evaluate | خطة التقييم والفريق الأحمر، وموجز الإطلاق والتجربة (Evaluation and Red-Team Plan, rollout and experiment brief) (6.1–6.3) | مجموعة مرجعية حسب المهمة واللغة (Golden set by job and language)؛ الحَكَم مُعايَر (judge calibrated)؛ تم اجتياز الفريق الأحمر (red-team passed)؛ تصميم اختبار A/B مع معيار التقييم الشامل والمقاييس الوقائية (A/B design with OEC and guardrails) | أي معيار لم يتحقق (Any bar missed) ← تضييق النطاق أو الإصلاح (narrow scope or fix)؛ ولا خفض صامت أبدًا (never lower silently) |
| 7 | Launch | قائمة التحقق من جاهزية الإطلاق + خطة التبنّي (Launch Readiness Checklist + adoption plan) (7.1–7.3) | إطلاق مرحلي (Staged rollout)؛ الموظفون مدرَّبون (agents trained)؛ مفتاح الإيقاف مختبَر (kill switch tested) | أي بند لم يُؤشَّر عليه (Any unchecked item) ← لا إطلاق (no launch) |
| 8 | Grow | شجرة المقاييس، وورقة اقتصاديات الوحدة، وخطة المراقبة ودليل التشغيل (Metrics tree, unit economics sheet, monitoring plan and runbook) (8.1–8.3) | نجم الشمال (North Star) = الحل دون تواصل متكرر خلال 7 أيام (resolved without repeat contact in 7 days) | خرق مقياس وقائي (Guardrail breach) ← إيقاف الإطلاق مؤقتًا (pause rollout)؛ تنبيه انجراف (drift alert) ← مراجعة (review) |
| 9 | Lead | صفحة الاستراتيجية الواحدة، وخارطة طريق الرهانات، ونموذج التشغيل (Strategy one-pager, bets roadmap, operating model) (9.1–9.4) | القابلية للدفاع من التكامل ومجموعة النصوص والثقة (Defensibility from integration, corpus and trust)؛ الاعتراضات بوصفها الرهان التالي (disputes as next bet) | أدلة الرهان لم تتحقق عند بوابتها (Bet evidence not met by its gate) ← إسقاطه أو إعادة تحديد نطاقه (drop or re-scope) |

تعليق رانيا (Rania's comment): *«سيسأل المدققون (Auditors) عن الصفين 3 و7، وخالد عن الصف 8. أما الصف 1 فهو الذي سننساه (the one we'll forget) — راجعوه كل ستة أشهر (revisit it every six months).»*

## 🛠️ التمارين (Exercises)
- 🟢 اكتب ثلاثة صفوف من الملف بالكامل (three rows of the dossier in full) (مثلًا بطاقة التقييم مع خمسة مرشحين (scorecard with five candidates)، وخريطة الأتمتة مع ست مهام (automation map with six tasks)، وقائمة التحقق من الإطلاق (launch checklist)). *يكتمل عندما (Done when):* يذكر كل منها قراره وأدلته وقاعدة إيقافه (decision, evidence and stop rule)، ويسمّي المُدخَل الذي يمرّره (names the input it passes on).
- 🟡 اكتب ملخص الملف (dossier summary) لـ**التنبيهات الذكية (Smart Alerts)** أو **مساعد الموظفين التوليدي (Staff GenAI)**، صفًا لكل مرحلة (one row per stage). *يكتمل عندما (Done when):* تُملأ الصفوف التسعة كلها، ويختلف ثلاثة منها على الأقل في المضمون (differ in substance) عن نجم أسيست، مع سبب من جملة واحدة لكل منها (one-sentence reason) (تعلّم آلي تقليدي (classic ML)، أو أداة داخلية (internal tool)).
- 🔴 نفّذ المشروع الختامي كاملًا (Run the full capstone) على منتج من مؤسستك (your own organisation) أو على منتج عام (public product). اعرضه في 10 دقائق على زميل يؤدي دور خالد ثم ليلى ثم طارق بالتناوب (in turn). *يكتمل عندما (Done when):* تتسع كل وثيقة في صفحة واحدة (fits on one page)، وتكون الروابط صريحة (links are explicit)، وتكون قد كتبت إجابات عن أصعب ثلاثة أسئلة لديهم (three hardest questions)، وتغيّرت وثيقة واحدة على الأقل بسببها (changed because of them).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **البدء من مرحلة Build (Starting at Build).** العرض التوضيحي (demo) يجيب عن «هل نستطيع؟ ⁦(can we?)⁩»، لا عن «هل يجب؟ ⁦(should we?)⁩». ابدأ بالمهام وبطاقة التقييم (jobs and the scorecard).
- **وثائق لا تتحاور فيما بينها (Artefacts that do not talk to each other).** مجموعة تقييم تفتقد أهم المهام (eval set missing the top jobs)، أو مراقبة تتجاهل معايير الإطلاق (monitoring that ignores the launch bars)، تترك فجوات تعيش فيها الإخفاقات (gaps where failures live).
- **مستوى أتمتة واحد للمنتج كله (One automation level for the whole product).** عبارة «نجم أسيست وكيل (Najm Assist is an agent)» تُخفي حقيقة أن الإجابة والتجميد والاعتراض (answering, freezing and disputing) تحمل مخاطر مختلفة جدًا (very different risk). حدّد المستوى لكل مهمة (Set the level per task).
- **قياس الاحتواء بدلًا من الحل (Measuring containment instead of resolution).** الاحتواء (Containment) يكافئ إخفاء الخيار البشري (hiding the human option). استخدم نجم شمال (North Star) يعدّ المشكلات المحلولة فعلًا (problems actually solved)، مع مقاييس الثقة بوصفها مقاييس وقائية (trust metrics as guardrails).
- **لا قواعد إيقاف (No stop rules).** من دون شرط مكتوب للتوقف (written condition for stopping)، تحمل التكلفة الغارقة (sunk cost) المنتجات الضعيفة إلى الإطلاق. اكتب قاعدة الإيقاف قبل أن تبدأ المرحلة (before the stage starts).

## 🧾 الخلاصة (Recap)
- يأخذ المشروع الختامي (capstone) منتجًا واحدًا عبر المراحل الثماني كلها ويُنتج **ملف منتج (product dossier)** مترابطًا، بوثيقة واحدة لكل مرحلة (one artefact per stage).
- كل وثيقة تجيب عن سؤال قرار (decision question)، وتستشهد بالأدلة (cites evidence)، وتسمّي قاعدة إيقاف (stop rule)، وتغذّي الوثيقة التالية (feeds the next).
- معايير الجودة في المواصفات (Spec quality bars) تصبح بوابات إطلاق (launch gates) ثم تنبيهات مراقبة (monitoring alerts)؛ وهذه السلسلة (chain) هي ما يجعل تغيير منتج الذكاء الاصطناعي آمنًا (safe to change).
- انمُ على أساس نجم شمال (North Star) يعدّ الحل الحقيقي (real resolution)، ونموذج تكلفة لكل مهمة (cost-per-task model) يشمل البشر (includes humans).
- مهارة البطل (The hero skill) هي الحكم بين الوثائق (judgement between artefacts): ضيّق النطاق بدلًا من خفض معيار (narrow scope rather than lower a bar)، ودع المقاييس الوقائية تتغلب على المكاسب اللافتة (let guardrails beat headline wins)، ولا تنقل الاستقلالية إلا بناءً على الأدلة (move autonomy only on evidence).

## ✍️ اختبر نفسك (Check yourself)

**1. تبلغ درجة الإسناد (grounding score) لدى نجم أسيست في أسئلة الرسوم 92% مقابل معيار إطلاق (launch bar) قدره 95%. ويُظهر تحليل الأخطاء (Error analysis) أن معظم الإخفاقات تتعلق بنوع واحد من رسوم التحويل الدولي (international transfer fee). ماذا يجب أن يفعل فيصل؟**

- A. الإطلاق كما هو مخطط وإصلاح المشكلة في الإصدار التالي (next release)
- B. خفض المعيار إلى 90% (lower the bar) للمساعد كله، لأن بقية النتائج قوية والفجوة صغيرة
- C. إخراج هذا النوع من الرسوم من النطاق (scope)، وتوجيه أسئلته إلى شخص، وإطلاق الباقي إذا تحققت المعايير الأخرى
- D. إلغاء الإطلاق وإعادة بدء الاكتشاف (discovery) من البداية، لأن الإخفاق يُظهر أن الفريق أساء فهم حاجات العملاء

<details><summary>الإجابة</summary>

**C.** تضييق النطاق (Narrowing scope) يُبقي معيار الجودة سليمًا (keeps the quality bar intact). أما الإطلاق على أي حال (A) أو خفض المعيار (B) فيكسر الرابط بين المواصفات وبوابة الإطلاق (link between spec and launch gate)؛ وD رد فعل مبالغ فيه (overreacts) تجاه إخفاق ضيق ومفهوم (narrow, understood failure). (🔴 نظرة الخبير (Expert view): قرارات الحكم بين الوثائق (the judgement calls between artefacts).)

</details>

**2. أي مقياس نجم شمال (North Star metric) يناسب نجم أسيست أكثر من غيره؟**

- A. احتياجات العملاء (customer needs) المحلولة في التطبيق دون تواصل متكرر خلال سبعة أيام
- B. عدد الرسائل المرسلة إلى المساعد شهريًا (messages per month) عبر جميع العملاء وجميع القنوات
- C. نسبة المحادثات التي لا تصل أبدًا إلى موظف بشري (human agent) خلال الشهر الأول بعد الإطلاق
- D. متوسط تكلفة النموذج (model cost) لكل محادثة، محسوبًا على جميع المحادثات التي يعالجها المساعد

<details><summary>الإجابة</summary>

**A.** فهو يقيس القيمة الحقيقية (real value) ولا يمكن رفعه بإخفاء الخيار البشري (hiding the human option). أما الاحتواء (Containment) (C) فقد يرتفع بينما تسوء الخدمة (service gets worse). وB وD مُدخلات لا نتائج (inputs, not outcomes). (🔴 نظرة الخبير (Expert view): Grow.)

</details>

**3. لماذا تضع خريطة الأتمتة (automation map) تجميد البطاقة عند مستوى «التنفيذ مع التأكيد (act with confirmation)» عند الإطلاق، بينما تضع فتح الاعتراض عند مستوى «الصياغة (draft)»؟**

- A. يستخدم تجميد البطاقة نموذجًا أرخص (cheaper model)، فتكون تكلفة تشغيله عند الإطلاق أقل من تكلفة فتح الاعتراضات
- B. تجميد البطاقة متكرر وعاجل ويسهل التراجع عنه (reversible)؛ أما الاعتراضات فتبدأ عملية منظّمة رقابيًا تكون فيها الأموال والمواعيد النهائية على المحك
- C. لا يمكن تنفيذ الاعتراضات عبر واجهة برمجة تطبيقات (API)، فلا يستطيع المساعد إلا تجهيز مسودة يرسلها الموظف
- D. يفضّل العملاء كتابة اعتراضاتهم بأنفسهم (disputes)، فيكتفي المساعد بصياغتها ولا يتصرف أبدًا

<details><summary>الإجابة</summary>

**B.** يُحدَّد مستوى الأتمتة (Automation level) لكل مهمة (per task) حسب المخاطر وقابلية التراجع (risk and reversibility). فالتجميد يُلغى بلمسة واحدة (undone in one tap)؛ أما الاعتراض الذي يُعالَج بشكل سيئ (mishandled dispute) فقد يكلّف العميل مالًا. (🟡 التعمق أكثر (Going deeper): Design.)

</details>

**4. في اختبار A/B (A/B test)، تُظهر مجموعة المعالجة (treatment group) انخفاضًا بنسبة 18% في المكالمات إلى مركز الاتصال، لكن مع ارتفاع في الشكاوى التي تذكر المساعد (complaints mentioning the assistant)، وهو مقياس وقائي متفق عليه مسبقًا (pre-agreed guardrail metric). ما الخطوة التالية الصحيحة؟**

- A. التوسّع إلى 100% لأن التوفير في التكلفة كبير (cost saving) والرقم الرئيسي أفضل بوضوح
- B. التحوّل إلى نموذج أرخص (cheaper model) لزيادة التوفير، ثم إعادة الاختبار نفسه في الشهر القادم
- C. إزالة الشكاوى من قائمة المقاييس الوقائية (guardrails)، لأن التغيير يمسّ مجموعة صغيرة من المستخدمين فقط
- D. إيقاف التوسّع مؤقتًا (pause) والتحقيق في الشكاوى قبل اتخاذ القرار

<details><summary>الإجابة</summary>

**D.** يمكن للمقاييس الوقائية (Guardrail metrics) أن توقف الإطلاق بمفردها (stop a rollout on their own)، مهما كان الرقم الرئيسي جيدًا (however good the headline) (كوهافي وتانغ وشو (Kohavi, Tang and Xu)). وA وC يُبطلان الغرض منها (defeat their purpose). (🟡 التعمق أكثر (Going deeper): Evaluate؛ 🔴 نظرة الخبير (Expert view).)

</details>

**5. يُظهر نموذج التكلفة لكل مهمة (cost-per-task model) لدى فيصل أن استدعاءات النموذج (model calls) تكلّف بضعة سنتات لكل محادثة، بينما يكلّف كل تحويل إلى إنسان (handoff to a human) أضعاف ذلك. ماذا يعني هذا لأولويات النمو (growth priorities)؟**

- A. التحوّل إلى نموذج أرخص (cheaper model) هو الرافعة الرئيسية، لأن استدعاءات النموذج هي الجزء من الفاتورة الذي يتحكم فيه الفريق مباشرة
- B. تحسين الحل في أكثر المهام شيوعًا (resolution)، وهو ما يقلّل التحويلات، هو على الأرجح الرافعة الأكبر
- C. إزالة خيار «التحدث إلى شخص» (human option) ستخفض التكلفة بأمان
- D. التكلفة لا تهم (cost) بعد إطلاق المنتج، لأن الفريق يستطيع ضبطها لاحقًا

<details><summary>الإجابة</summary>

**B.** عندما تهيمن التحويلات على التكلفة (handoffs dominate cost)، فإن تحسين الحل في أهم المهام (better resolution on top jobs) هو ما يوفّر أكثر. أما النموذج الأرخص (A) فيقلّص الجزء الصغير (trims the small part)؛ وC يضرّ بالثقة (harms trust). (🔴 نظرة الخبير (Expert view): Grow.)

</details>

## 📚 المراجع (References)
- Teresa Torres, *Continuous Discovery Habits* (2021) — https://www.producttalk.org
- Marty Cagan, *Inspired* (2nd ed., 2017) — https://www.svpg.com
- Google PAIR, People + AI Guidebook — https://pair.withgoogle.com/guidebook
- Amershi et al., "Guidelines for Human-AI Interaction", CHI 2019 — https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/
- Kohavi, Tang and Xu, *Trustworthy Online Controlled Experiments* (2020) — https://experimentguide.com
- Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (2023) — https://arxiv.org/abs/2306.05685
- Rodden, Hutchinson and Fu, "Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications", CHI 2010 — https://research.google/pubs/
- Model Context Protocol — https://modelcontextprotocol.io
- EU AI Act, Regulation (EU) 2024/1689 — https://eur-lex.europa.eu/eli/reg/2024/1689/oj

---

# 10.2 — مسيرة مدير منتجات الذكاء الاصطناعي: المقابلات وملف الأعمال والنمو (The AI PM career: interviews, portfolio and growth)
*المستوى (Level): 🔴 متقدم (Advanced)* · *المتطلبات (Prerequisites): 10.1* · *المرحلة (Stage): Lead*

## ⚡ الدرس في دقيقة (In 60 seconds)
- إدارة منتجات الذكاء الاصطناعي (AI product management) هي إدارة منتج (product management) أولًا. فالمحاورون (Interviewers) ما زالوا يختبرون حسّ المنتج (product sense) والتنفيذ (execution) والمقاييس (metrics) والقيادة (leadership)؛ أما جانب الذكاء الاصطناعي فيختبر ما إذا كنت تستطيع التفكير المنطقي في **السلوك الاحتمالي والبيانات والتقييم والتكلفة والثقة (probabilistic behaviour, data, evaluation, cost and trust)** حين تتخذ تلك القرارات.
- لا توجد وظيفة واحدة اسمها «مدير منتجات ذكاء اصطناعي (AI PM)». فالأدوار (Roles) تتراوح بين إضافة ميزات ذكاء اصطناعي إلى منتج قائم (adding AI features to an existing product)، وبناء منتجات أصيلة في الذكاء الاصطناعي (AI-native products)، وتشغيل منصات ذكاء اصطناعي داخلية (internal AI platforms). اعرف أيها تتقدّم إليه (which one you are applying for).
- أقوى إجابات المقابلات (strongest interview answers) تتبع بنية ظاهرة (visible structure): المستخدم والمهمة (user and job) ← هل الذكاء الاصطناعي هو الخيار الصحيح؟ ⁦(is AI right?)⁩ ← مستوى الأتمتة (level of automation) ← البيانات (data) ← معيار الجودة والتقييمات (quality bar and evals) ← أنماط الفشل والضوابط الوقائية (failure modes and guardrails) ← المقاييس والتكلفة (metrics and cost) ← الإطلاق (rollout). إنها الدورة كلها في فقرة واحدة (the course in one paragraph).
- ملف الأعمال (portfolio) يتفوّق على قائمة من الادعاءات (list of claims). فدراستا حالة أو ثلاث (Two or three case studies) تُظهر **القرار والأدلة والمفاضلة والنتيجة (decision, the evidence, the trade-off and the result)** — بما فيها حالة قتلت فيها شيئًا أو ضيّقته (killed or narrowed something) — تقول أكثر من أي شهادة (certificate).
- يأتي النمو (Growth) من الإطلاق (shipping) والقياس (measuring) وتدوين ما تعلّمته (writing down what you learned)، لا من متابعة كل إصدار نموذج (every model release). ابنِ عادة تعلّم (learning habit) تستطيع المحافظة عليها لسنوات.
- أكبر فخ (Biggest trap): الحديث عن النماذج (talking about models) بدلًا من المستخدمين والنتائج (users and outcomes). فعبارة «سأستخدم أحدث نموذج مع التوليد المعزّز بالاسترجاع ⁦(I'd use the latest model with RAG)⁩» ليست إجابة منتج (product answer).

## 🧭 لماذا يهم (Why it matters)
بعد ستة أشهر من إطلاق نجم أسيست (Najm Assist)، يتقدّم فيصل لوظيفة مدير منتجات ذكاء اصطناعي أول (senior AI PM role) في مساعد مذكرات الائتمان (Credit Memo Copilot). يقول لرانيا: «أنا أعرف المادة (I know the material)، لكن في سؤال تصميم مدته 30 دقيقة (30-minute design question) أبدأ بالنموذج وأضيع (start with the model and get lost).» تُجري رانيا مقابلة تجريبية (mock interview): «صمّم مساعدًا يساعد مديري العلاقات (relationship managers) على الاستعداد لاجتماعات العملاء (client meetings).» يفتتح فيصل بخطوط الاسترجاع (retrieval pipelines) وقوالب الموجّهات (prompt templates). توقفه رانيا بعد دقيقتين. «لم تخبرني من هو مدير العلاقة (RM)، ولا ما يفعله اليوم (what they do today)، ولا كيف سنعرف أن الحل يعمل (how we'd know it works).»

المرشحون الذين قرؤوا كثيرًا عن الذكاء الاصطناعي (Candidates who have read a lot about AI) غالبًا ما يجيبون كمهندسين قرؤوا عن المنتج (engineers who have read about product). أما مديرو التوظيف (Hiring managers) فيريدون العكس (the reverse): أشخاص منتج يفكرون بوضوح في ما يغيّره الذكاء الاصطناعي (product people who reason clearly about what AI changes). وفي الوقت نفسه توظّف رانيا نفسها مديري منتجات ذكاء اصطناعي (AI PMs)، وعليها أن تقرر شكل الأداء الجيد (what good looks like) من الجانب الآخر من الطاولة (other side of the table).

هذا الدرس عن الجانبين (both sides): كيف تُظهر ما تستطيع فعله (show what you can do)، وكيف تواصل التحسّن (keep getting better) بعد أن تحصل على الوظيفة.

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**ما أنواع أدوار مديري منتجات الذكاء الاصطناعي الموجودة (What kinds of AI PM roles exist).** تختلف المسميات (Titles) من شركة إلى أخرى، فاقرأ الوصف الوظيفي (job description) بدلًا من المسمى. في وقت كتابة هذا النص (At the time of writing) (2026)، تندرج معظم الأدوار في أربعة أشكال (four shapes):

| شكل الدور (Role shape) | ما تملكه (What you own) | ما الذي سيستقصونه (What they will probe) |
|---|---|---|
| مدير منتج لميزات الذكاء الاصطناعي (AI feature PM) | ميزات ذكاء اصطناعي داخل منتج قائم (AI features inside an existing product) (مثل الردود الذكية في تطبيق مصرفي (smart replies in a banking app)) | الدمج في سير العمل (Integration into workflows)، والتبنّي (adoption)، والجودة مقابل التكلفة (quality vs cost)، وعدم كسر ما يعمل (not breaking what works) |
| مدير منتج أصيل في الذكاء الاصطناعي (AI-native product PM) | منتج قيمته الأساسية هي الذكاء الاصطناعي (A product whose core value is the AI) (مثل نجم أسيست (Najm Assist) ومساعد مذكرات الائتمان (Credit Memo Copilot)) | التقييم (Evaluation)، وتصميم الثقة (trust design)، واقتصاديات الوحدة (unit economics)، وسرعة التكرار (iteration speed) |
| مدير منتج لمنصة الذكاء الاصطناعي (AI platform PM) | منصة داخلية تبني عليها الفرق الأخرى (Internal platform other teams build on): الوصول إلى النماذج (model access)، وأدوات التقييم (eval tooling)، والضوابط الوقائية (guardrails)، وبوابات الأدوات (tool gateways) | تجربة المطوّرين (Developer experience)، وإعادة الاستخدام (reuse)، والحوكمة المدمجة (governance built in)، وتوزيع التكاليف (cost allocation) |
| مدير منتج للبيانات والتعلّم الآلي (Data/ML PM) | النماذج التنبؤية والبيانات التي خلفها (Predictive models and the data behind them) (مثل التمويل الفوري للشركات الصغيرة (SME Instant Finance) والتنبيهات الذكية (Smart Alerts)) | مقاييس مثل الدقة (precision) والاستدعاء (recall)، وخطوط البيانات (data pipelines)، ومخاطر النماذج (model risk)، والتنظيم الرقابي (regulation) |

**ما الذي تختبره المقابلات (What interviews test).** تختلف الصيغ (Formats) من شركة إلى أخرى، لكن معظم سلاسل مقابلات مديري منتجات الذكاء الاصطناعي (AI PM loops) تمزج بين ما يلي:

1. **حسّ المنتج (Product sense)**: «صمّم ميزة ذكاء اصطناعي لـ X ⁦(design an AI feature for X)⁩». هل تجد المستخدم والمهمة قبل الحل (user and job before the solution)؟
2. **الطلاقة في الذكاء الاصطناعي (AI fluency)**: «الاسترجاع أم الضبط الدقيق؟ ⁦(retrieval or fine-tuning?)⁩»، «لماذا يختلق النموذج أشياء؟ ⁦(why does the model make things up?)⁩». إنها معرفة الوحدة 1 (Module 1 literacy)، لا عمق هندسي (not engineering depth).
3. **التقييم والمقاييس (Evaluation and metrics)**: «كيف ستعرف أنه جيد؟ ⁦(how would you know it's good?)⁩»، «ما مقياس نجم الشمال لديك؟ ⁦(what's your North Star?)⁩» (الوحدتان 6 و8 (Modules 6 and 8)).
4. **التنفيذ (Execution)**: «التقييم أدنى من المعيار والإطلاق الأسبوع المقبل ⁦(the eval is below the bar and launch is next week)⁩».
5. **الاستراتيجية (Strategy)**: «منافس يطلق الميزة نفسها على النموذج نفسه؛ فما خندقنا التنافسي؟ ⁦(a competitor ships the same feature on the same model; what's our moat?)⁩» (الوحدة 9 (Module 9)).
6. **السلوكية (Behavioural)**: مواقف سابقة (past situations)، تُروى وفق **STAR** (الموقف (situation)، والمهمة (task)، والإجراء (action)، والنتيجة (result)).
7. **دراسة حالة أو مهمة منزلية (Case or take-home)**، وأحيانًا نموذج أولي صغير مع تقرير مكتوب (small prototype with a write-up).

**بنية الإجابة (The answer structure).** في أي سؤال من نوع «صمّم منتج ذكاء اصطناعي (design an AI product)»، سِر على هذا المسار بصوت مرتفع (walk this path out loud):

```mermaid
flowchart TD
  A["من المستخدم، وما المهمة؟<br/>(Who is the user, what is the job?)"] --> B["هل الذكاء الاصطناعي هو الأداة الصحيحة؟<br/>(Is AI the right tool?)"]
  B -->|"لا (no)"| X["حل أبسط: قلها صراحة<br/>(Simpler fix: say so)"]
  B -->|"نعم (yes)"| C["مستوى الأتمتة لكل مهمة<br/>(Level of automation per task)"]
  C --> D["البيانات: هل نملكها، وهل يحق لنا استخدامها؟<br/>(Data: have it, may we use it?)"]
  D --> E["معيار الجودة وكيف نقيّم<br/>(Quality bar and how we evaluate)"]
  E --> F["أنماط الفشل والضوابط الوقائية<br/>(Failure modes and guardrails)"]
  F --> G["المقاييس والتكلفة لكل مهمة<br/>(Metrics and cost per task)"]
  G --> H["الإطلاق وما الذي سيجعلنا نتوقف<br/>(Rollout and what would make us stop)"]
```

لن يتسع لك الوقت للتعمق في كل خطوة (go deep on every step). قل البنية في جملة واحدة في البداية («سأبدأ بالمستخدم، وأتحقق من أن الذكاء الاصطناعي هو الأداة الصحيحة، ثم أغطي الأتمتة والبيانات والجودة والمخاطر والمقاييس والإطلاق (I'll start with the user, check AI is the right tool, then cover automation, data, quality, risks, metrics and rollout)»)، ثم اقضِ معظم الوقت حيث تكون المشكلة أصعب (where the problem is hardest). في مساعد مصرفي (banking assistant) يكون ذلك عادةً الثقة وأنماط الفشل (trust and failure modes)؛ وفي أداة داخلية (internal tool) يكون غالبًا التبنّي (adoption).

### 🟡 التعمق أكثر (Going deeper)

**الإجابة عن أسئلة الطلاقة في الذكاء الاصطناعي (Answering AI fluency questions).** يختبر المحاورون ما إذا كنت تستطيع اتخاذ قرارات منتج جيدة مع المهندسين (good product decisions with engineers)، لا ما إذا كنت تستطيع بناء نموذج (build a model). للإجابات الجيدة ثلاثة أجزاء: المفهوم بكلمات بسيطة (concept in plain words)، والمفاضلة التي يخلقها (trade-off it creates)، وقرار المنتج الذي يقوده (product decision it drives). على سبيل المثال:

> *«لماذا تهلوس النماذج اللغوية الكبيرة، وماذا ستفعل حيال ذلك؟ ⁦(Why do LLMs hallucinate, and what would you do about it?)⁩»* — «النموذج يولّد نصًا مرجّحًا (generates likely text)؛ وليس لديه فحص مدمج (built-in check) يتأكد من أن النص صحيح. لذلك، في أي أمر واقعي (anything factual)، سأُسند الإجابات إلى مصادرنا نحن عبر الاسترجاع (ground answers in our own sources with retrieval)، وأعرض تلك المصادر (show those sources)، وأجعل «لا أعرف (I don't know)» إجابة مسموحًا بها في المواصفات (allowed answer in the spec). ثم سأقيس الادعاءات غير المُسندة (ungrounded claims) في مجموعة التقييم (eval set) وأضع معيارًا قبل الإطلاق (set a bar before launch). وفي الحقائق عالية الخطورة (high-stakes facts) مثل الرسوم، سأحجب أيضًا أي رقم غير موجود في مصدر مُسترجَع (block any number that isn't in a retrieved source).»

الإجابات الضعيفة (Weak answers) تتوقف بعد الجملة الأولى، أو تقفز إلى اسم مزوّد (vendor name). وتجنّب ذكر أسعار اليوم (today's prices) أو أحجام نوافذ السياق (context window sizes) أو درجات المقاييس المعيارية (benchmark scores) على أنها حقائق؛ فهي تتغيّر شهريًا (change monthly)، والمحاور يريد المنهج (wants the method).

**أسئلة التقييم (Evaluation questions)** هي أكثر ما يميّز بين المرشحين (separate candidates most). الإجابة القوية تسمّي الطبقة غير المتصلة (offline layer) (مجموعة مرجعية (golden set) مقسّمة حسب المهام المهمة (sliced by the jobs that matter)، وتحليل الأخطاء (error analysis))، والطبقة القابلة للتوسّع (scalable layer) (نموذج لغوي كبير حَكَمًا (LLM-as-judge) مُعايَر مقابل البشر (calibrated against humans)، والفريق الأحمر (red-teaming))، والطبقة المتصلة (online layer) (إطلاق مرحلي (staged rollout)، واختبار A/B (A/B test) بمعيار متفق عليه (agreed criterion) ومقاييس وقائية (guardrail metrics)). وتسمية تحيّز واحد للحَكَم (one judge bias) (الموضع (position)، أو الإسهاب (verbosity)، أو تفضيل الذات (self-preference)) وكيف ستتحقق منه (how you would check it) يُظهر أنك قمت بالعمل فعلًا (you have done the work).

**أسئلة التنفيذ (Execution questions)** تكافئ قرارات الحكم (judgement calls) من الدرس 10.1: ضيّق النطاق بدلًا من خفض معيار (narrow scope instead of lowering a bar)؛ ودع مقياسًا وقائيًا يوقف الإطلاق (let a guardrail metric stop a rollout)؛ ولا ترتقِ سلّم الأتمتة (automation ladder) إلا بناءً على الأدلة (only on evidence). قل ما ستفعله، وما ستقوله لمالك الأعمال (business owner)، وما الذي سيغيّر رأيك (what would change your mind).

**الأسئلة السلوكية (Behavioural questions)** كثيرًا ما تسأل عن أمر سار على نحو خاطئ (something that went wrong)، أو خلاف مع الهندسة أو علم البيانات (disagreement with engineering or data science)، أو مرة قلت فيها لا (a time you said no). حضّر قصصًا ذات زاوية ذكاء اصطناعي (stories with an AI angle): نتيجة تقييم غيّرت خطة (eval result that changed a plan)، أو ميزة قتلتها (feature you killed). وكن دقيقًا بشأن دورك (precise about your role): فكلمة «نحن (we)» تُخفي ما فعلته أنت؛ وكلمة «أنا (I)» قد تبالغ في نسب عمل الفريق إليك (overclaim what the team did).

**ملف الأعمال (The portfolio).** ملف الأعمال (portfolio) هو دراستا حالة أو ثلاث قصيرة (two or three short case studies)، كل منها في صفحة أو صفحتين، إضافة إلى مواد داعمة اختيارية (optional supporting material) (نموذج أولي (prototype)، أو مجموعة تقييم (eval set)، أو تقرير منشور (published write-up)). ودراسة الحالة الجيدة (good case study) تتبع منطق الملف (dossier logic) من الدرس 10.1:

| القسم (Section) | ما تكتبه (What to write) | الفخ الذي يجب تجنّبه (Trap to avoid) |
|---|---|---|
| السياق (Context) | المستخدم، والمهمة، ولماذا كانت مهمة، ودورك (User, job, why it mattered, your role) | عبارة مبهمة مثل «بنينا منصة ذكاء اصطناعي (we built an AI platform)» |
| القرار (Decision) | قرار المنتج الرئيسي (key product decision) (النطاق (scope)، ومستوى الأتمتة (automation level)، والبناء مقابل الشراء (build vs buy)، والقتل (kill)) | سرد الميزات بدلًا من القرارات (Listing features instead of decisions) |
| الأدلة (Evidence) | الاكتشاف (Discovery)، ونتائج التقييم (eval results)، ونتائج التجارب (experiment outcomes) | أرقام مختلقة أو غير مُبلَّغ عنها (Invented or unreported numbers) |
| المفاضلة (Trade-off) | ما تخلّيت عنه ولماذا (What you gave up and why) | التظاهر بعدم وجود جانب سلبي (Pretending there was no downside) |
| النتيجة (Result) | ما حدث، بما في ذلك ما لم ينجح (including what didn't work) | قصص النجاح فقط (Only success stories) |
| الدرس (Lesson) | ما الذي كنت ستفعله بشكل مختلف (What you would do differently) | عبارة عامة مثل «التواصل هو المفتاح (communication is key)» |

**السرية أولًا (Confidentiality comes first).** لا تنشر أبدًا بيانات جهة عملك (employer's data)، أو مقاييسها الداخلية (internal metrics)، أو معلومات العملاء (customer information)، أو خططها غير المعلنة (unreleased plans). أعد كتابة دراسات الحالة بمستوى تفصيل تقبله جهة عملك (level of detail your employer would accept)، واستخدم الأرقام النسبية (relative numbers) («خفّضنا التحويلات إلى النصف تقريبًا في أهم مهمة (roughly halved handoffs on the top job)») فقط إذا سُمح لك بمشاركتها، أو استخدم مشروعًا عامًا أو شخصيًا (public or personal project) بدلًا من ذلك. والمشروع الختامي من الدرس 10.1 مطبّقًا على منتج عام (applied to a public product)، مع توضيح أنه تحليلك الخاص (clearly labelled as your own analysis)، قطعة ممتازة في ملف أعمال (fine portfolio piece) لشخص لم يُطلق بعد عملًا في الذكاء الاصطناعي (without shipped AI work yet).

**بناء الإثبات دون مسمى ذكاء اصطناعي (Building proof without an AI title).** تطوّع لتملّك التقييم (own evaluation) في ميزة ذكاء اصطناعي يبنيها فريقك؛ وأجرِ اختبار Wizard of Oz واكتب عنه (write it up)؛ وابنِ نموذجًا أوليًا صغيرًا (small prototype) مع مجموعة مرجعية (golden set) من 30 مهمة حقيقية (30 real tasks) وانشر ما علّمك إياه التقييم (what the eval taught you)؛ وتولَّ عمل جاهزية البيانات (data readiness) أو بوابات الحوكمة (governance-gate work) الذي لا يريده أحد. كل منها يمنحك قصة فيها قرار وأدلة (a story with a decision and evidence).

### 🔴 نظرة الخبير (Expert view)

**النمو من مدير منتج إلى قائد (Growing from PM to leader).** تتغيّر الوظيفة مع نموّك (The job changes as you grow). في البداية تملك ميزة ومقاييسها (a feature and its metrics). وبوصفك مدير منتج أول (senior PM) تملك منتجًا واستراتيجيته (a product and its strategy). وبوصفك قائدًا أو رئيسًا (lead or head) (دور رانيا (Rania's role)) تملك محفظة (a portfolio): أي الرهانات تُموَّل (which bets get funded)، وكيف تُشكَّل الفرق (how teams are shaped)، وكيف تقرر المؤسسة معنى «جيد بما يكفي (good enough)». وتكبر المهارات الخاصة بالذكاء الاصطناعي (AI-specific skills) معك:

| المستوى (Level) | المهارة الأساسية لمدير منتجات الذكاء الاصطناعي (Core AI PM skill) | الأدلة التي يمكنك عرضها (Evidence you can show) |
|---|---|---|
| مدير منتج (PM) | كتابة مواصفات تكون فيها التقييمات متطلبات (spec with evals as requirements)؛ وإجراء تحليل الأخطاء مع علم البيانات (error analysis with data science) | خطة تقييم (eval plan) وإطلاق كنت مالكه (a launch you owned) |
| مدير منتج أول (Senior PM) | وضع معايير الجودة ومستويات الأتمتة (quality bars and automation levels)؛ وتملّك اقتصاديات الوحدة (unit economics)؛ والتعامل مع تغيير النموذج (handle a model change) | ملف منتج (product dossier) ونموذج تكلفة لكل مهمة (cost-per-task model) قاد قرارًا (drove a decision) |
| قائد / مدير منتج مجموعة (Lead / Group PM) | وضع خارطة طريق من الرهانات (roadmap of bets)؛ وبناء ممارسة مشتركة للتقييم والضوابط الوقائية (shared eval and guardrail practice) عبر الفرق | خارطة طريق ببوابات أدلة (roadmap with evidence gates)؛ وقتل قُدته أنت (a kill you led) |
| رئيس منتجات الذكاء الاصطناعي (Head of AI Products) | نموذج التشغيل (Operating model)، والمواهب (talent)، والشراكة مع الحوكمة (governance partnership)، واستراتيجية المحفظة (portfolio strategy) | كيف تُطلق المؤسسة الذكاء الاصطناعي بأمان وبشكل متكرر (ships AI safely and repeatedly) |

**التوظيف بوصفك المحاور (Hiring as the interviewer).** تقيّم لجنة رانيا (Rania's panel) البنية نفسها من الجانب الآخر (انظر 🏛️)، إضافة إلى سؤال آخر: هل يستطيع المرشح تغيير رأيه بناءً على الأدلة (change their mind on evidence)؟ وهي تتجنب الأسئلة التافهة عن أسماء النماذج (trivia about model names)، التي تكافئ متابعة الأخبار (following the news) بدلًا من الحكم (judgement). ويحصل كل مرشح على الأسئلة الأساسية نفسها (same core questions)، ويقيّم أعضاء اللجنة كلٌّ على حدة (score independently) قبل المناقشة.

**مواكبة المستجدات دون مطاردة الضجيج (Staying current without chasing hype).** النماذج والأدوات والأسعار (Models, tools and prices) تتغيّر شهريًا؛ أما المنهج الأساسي (underlying method) فيتغيّر ببطء. وهذه عادة مستدامة (sustainable habit):

- *أسبوعيًا (Weekly):* اقرأ مصدرًا أوليًا أو اثنين (primary sources) (ملاحظات الإصدار (release notes)، أو ورقة بحثية (paper)، أو تحديثًا من جهة رقابية (regulator's update)) واسأل «هل يغيّر هذا أي قرار في ملفي؟ ⁦(does this change any decision in my dossier?)⁩». وفي العادة لا يغيّر شيئًا.
- *شهريًا (Monthly):* شغّل مجموعة التقييمات الخاصة بك (your own eval suite) على نموذج أو تقنية جديدة واحدة (one new model or technique). فمجموعتك المرجعية (golden set) تتفوّق على المقاييس المعيارية العامة (public benchmarks) بالنسبة إلى منتجك.
- *ربع سنويًا (Quarterly):* اكتب ملاحظة قصيرة (short note) عمّا علّمتك إياه بيانات منتجك (what your product's data taught you). فالكتابة تحوّل الخبرة إلى حكم يستطيع الآخرون استخدامه (turns experience into judgement others can use).
- *سنويًا (Yearly):* أعد قراءة الأسس (re-read the foundations) (كاغان (Cagan)، وتوريس (Torres)، وكوهافي (Kohavi)). فهي تزداد فائدة كلما أطلقت أكثر (the more you ship).

**الأخلاقيات بوصفها رصيدًا مهنيًا (Ethics as a career asset).** مدير المنتج الذي يستطيع أن يقول «ليس بعد (not yet)» مستندًا إلى الأدلة، كما فعلت رانيا في أتمتة الاعتراضات (dispute automation)، يكسب ثقة المخاطر والشؤون القانونية والإدارة التنفيذية (risk, legal and executives). وفي القطاع المصرفي الخليجي (Gulf banking)، هذه الثقة هي ما يجعل المنتجات الأكبر تحظى بالموافقة (gets bigger products approved). الحوكمة (Governance) تغطيها دورة *AI Governance: Zero to Hero*؛ أما دورك فهو كتابة قواعد الإيقاف والالتزام بها (writing stop rules and honouring them).

## 🧰 الأدوات (The toolkit)
| الأداة أو الإطار (Tool or framework) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **AI product answer structure** — بنية إجابة منتج الذكاء الاصطناعي | المستخدم والمهمة (User and job) ← هل الذكاء الاصطناعي صحيح (is AI right) ← الأتمتة (automation) ← البيانات (data) ← الجودة والتقييمات (quality and evals) ← أنماط الفشل (failure modes) ← المقاييس والتكلفة (metrics and cost) ← الإطلاق (rollout) | أي سؤال مقابلة من نوع «صمّم منتج ذكاء اصطناعي (design an AI product)»، واجتماعات الانطلاق الحقيقية (real kick-off meetings) |
| **CIRCLES method** (لويس لين (Lewis Lin)، *Decode and Conquer*) — منهج CIRCLES | بنية عامة لمقابلات تصميم المنتج (general product-design interview structure)، من فهم الموقف والعميل (understanding the situation and customer) إلى المفاضلات والملخص (trade-offs and summary) | أسئلة حسّ المنتج (Product-sense questions)؛ ادمجه مع خطوات الذكاء الاصطناعي أعلاه (combine with the AI steps above) |
| **STAR** | الموقف والمهمة والإجراء والنتيجة (Situation, task, action, result): بنية للإجابات السلوكية (structure for behavioural answers) | الأسئلة السلوكية عن العمل السابق (Behavioural questions about past work) |
| **Portfolio case study** — دراسة حالة لملف الأعمال | صفحة أو صفحتان (One or two pages): السياق، والقرار، والأدلة، والمفاضلة، والنتيجة، والدرس (context, decision, evidence, trade-off, result, lesson) | طلبات التوظيف (Job applications)، وملفات الترقية (promotion cases)، والظهور الداخلي (internal visibility) |
| **Interview scorecard** — بطاقة تقييم المقابلة | معايير ثابتة (Fixed criteria) يقيّمها كل عضو في اللجنة على حدة (scored independently by each panel member) | عندما تكون أنت من يوظّف مديري منتجات الذكاء الاصطناعي (the one hiring AI PMs) |
| **Learning cadence** — إيقاع التعلّم | عادات أسبوعية وشهرية وربع سنوية وسنوية (Weekly, monthly, quarterly and yearly habits) مرتبطة بقرارات منتجك الخاصة (tied to your own product decisions) | مواكبة المستجدات دون مطاردة كل إصدار (Staying current without chasing every release) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
**بطاقة تقييم مقابلات مديري منتجات الذكاء الاصطناعي (AI PM interview scorecard)** لدى رانيا (المستخدمة لوظيفة مدير المنتج الأول لمساعد مذكرات الائتمان (senior Credit Memo Copilot role))، مع التقييم الذاتي لفيصل (Faisal's self-assessment) بعد مقابلته التجريبية (mock interview):

| المعيار (Criterion) | كيف يبدو الأداء «القوي» (What "strong" looks like) | فيصل (تجريبية) (Faisal (mock)) | الإجراء (Action) |
|---|---|---|---|
| المستخدم والمهمة أولًا (User and job first) | يسمّي مدير العلاقة (RM)، ومهمته في التحضير للاجتماع (meeting-prep job)، وألم اليوم (today's pain) قبل أي حل | ضعيف — افتتح بالبنية التقنية (Weak — opened with architecture) | التدرّب على الافتتاح بدقيقتين عن المستخدم والمهمة (2 minutes on user and job) |
| هل الذكاء الاصطناعي صحيح؟ ⁦(Is AI right?)⁩ | يتحقق من خيارات أبسط (simpler options) (القوالب (templates)، والبحث الأفضل (better search)) ويقول متى تتفوّق (when they win) | لم يُغطَّ (Not covered) | إضافة جملة واحدة إلى كل إجابة (one sentence to every answer) |
| مستوى الأتمتة (Automation level) | يضع مستوى لكل مهمة مع الأسباب (level per task with reasons) (صياغة الإحاطة (draft briefing): نعم؛ الإرسال إلى العميل (send to client): لا) | جيد (Good) | — |
| البيانات والحقوق (Data and rights) | يسمّي المصادر (sources)، والفجوات (gaps)، والموافقة (consent)، وسرية بيانات العملاء (confidentiality of client data) | جزئي — فاتته سرية العميل (Partial — missed client confidentiality) | مراجعة الدرس 3.3 (Review 3.3) |
| معيار الجودة والتقييمات (Quality bar and evals) | مجموعة مرجعية من إحاطات اجتماعات حقيقية (golden set of real meeting briefs)، ومعيار إسناد (grounding bar)، وعينة مراجعة من مديري العلاقات (RM review sample)، ومعايرة الحَكَم (judge calibration) | قوي — استخدم خبرته في نجم أسيست (Strong — used Najm Assist experience) | البدء بهذه القصة (Lead with this story) |
| أنماط الفشل (Failure modes) | أرقام خاطئة (Wrong figures)؛ وبيانات قديمة (stale data)؛ والاعتماد المفرط من مدير العلاقة (RM overreliance) | جزئي (Partial) | إضافة تحيّز الأتمتة (Add automation bias) |
| المقاييس والتكلفة (Metrics and cost) | نجم شمال (North Star) قائم على وقت مدير العلاقة الموفَّر مع الحفاظ على الجودة (RM time saved with quality held)؛ والتكلفة لكل إحاطة (cost per briefing) | ضعيف في التكلفة (Weak on cost) | بناء مسودة سريعة للتكلفة لكل مهمة (quick cost-per-task sketch) |
| الأدلة السلوكية (Behavioural evidence) | قصة وفق STAR فيها قرار وأدلة ودور صادق (decision, evidence and honest role) | جيد — قصة نطاق الرسوم 92% مقابل 95% (Good — the 92% vs 95% fee-scope story) | الاختصار إلى 90 ثانية (Tighten to 90 seconds) |

و**دراسة الحالة في صفحة واحدة لملف أعمال فيصل (Faisal's one-page portfolio case study)**، التي أعاد كتابتها مع رانيا لتفي بقواعد السرية في البنك (bank's confidentiality rules):

> **نجم أسيست: إطلاق مساعد مصرفي مُسند (Najm Assist: launching a grounded banking assistant) (دوري: مدير المنتج (my role: product manager)).** *السياق (Context):* كان العملاء ينتظرون على الهاتف من أجل احتياجات بسيطة (simple needs)؛ وكنت مالك الإصدار الأول للمساعد (assistant's first release). *القرار (Decision):* الإطلاق بإجابات الرسوم وتجميد البطاقة فقط (fee answers and card freeze only)، وإخراج نوع واحد من الرسوم من النطاق (remove one fee type from scope) عندما أخفق في بلوغ معيار الإسناد (missed the grounding bar)، بدلًا من تأجيل الإطلاق أو خفض المعيار (delaying launch or lowering the bar). *الأدلة (Evidence):* مجموعة مرجعية حسب المهمة واللغة (golden set by job and language)؛ وأظهر تحليل الأخطاء (error analysis) أن الإخفاقات تجمّعت في نوع واحد من الرسوم (misses clustered in one fee type). *المفاضلة (Trade-off):* العملاء الذين يطرحون ذلك السؤال ما زالوا ينتظرون شخصًا (still wait for a person). *النتيجة (Result):* أُطلق في موعده (launched on schedule) مع تحقق جميع المعايير (all bars met)؛ وأُضيف نوع الرسوم المستبعد (excluded fee type) في الإصدار التالي بعد إصلاح مجموعة النصوص (after the corpus was fixed). *الدرس (Lesson):* اتفق على معايير الجودة قبل البناء (agree the quality bars before build)، حتى يكون قرار الإطلاق فحصًا لا نقاشًا (a check, not a debate).

## 🛠️ التمارين (Exercises)
- 🟢 أجب عن هذا بصوت مرتفع في 15 دقيقة، مع تسجيل نفسك (recording yourself): «صمّم ميزة ذكاء اصطناعي تساعد عملاء الأعمال الصغيرة على فهم تدفقهم النقدي ⁦(Design an AI feature that helps small-business customers understand their cash flow.)⁩» استخدم بنية الإجابة ذات الخطوات الثماني (eight-step answer structure). *يكتمل عندما (Done when):* تستطيع إعادة تشغيل التسجيل (play back the recording) والإشارة إلى كل خطوة من الخطوات الثماني، ولا تتضمن أول دقيقتين لديك أي ذكر للنماذج أو التقنية (no mention of models or technology).
- 🟡 اكتب دراسة حالة واحدة لملف الأعمال (one portfolio case study) (صفحة واحدة) من عملك الخاص أو من مشروعك الختامي في الدرس 10.1 (your 10.1 capstone)، مستخدمًا الأقسام الستة في الجدول (six sections in the table). ثم اطلب من شخص أن يقرأها ويخبرك، في جملة واحدة، بالقرار الذي اتخذته (what decision you made). *يكتمل عندما (Done when):* تطابق جملته قرارك (their sentence matches your decision)، ويكون كل رقم إما حقيقيًا وقابلًا للمشاركة (real and shareable) أو محذوفًا (removed)، وتتضمن دراسة الحالة مفاضلة (includes a trade-off).
- 🔴 صمّم سلسلة مقابلات (interview loop) لتوظيف مدير منتجات ذكاء اصطناعي في مؤسستك (أو في بنك نجم (Najm Bank)): أربع مقابلات (four interviews)، والأسئلة لكل منها، وبطاقة تقييم (scorecard) من ستة معايير على الأقل (at least six criteria)، وكيف يبدو الأداء «القوي (strong)» و«الضعيف (weak)» في كل منها. أجرِ مقابلة واحدة مع زميل (Run one interview with a colleague). *يكتمل عندما (Done when):* يرتبط كل معيار بمهارة من إحدى وحدات الدورة (skill from a course module)، ويستطيع عضوان في اللجنة تقييم الإجابة نفسها كلٌّ على حدة (score the same answer independently)، وتكون قد عدّلت سؤالًا واحدًا على الأقل بعد التشغيل التجريبي (after the trial run).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **البدء بالنموذج (Leading with the model).** البدء بالبنية التقنية (architecture) أو باسم مزوّد (vendor name) يشير إلى اهتمام هندسي (engineering interest)، لا إلى حكم منتج (product judgement). ابدأ بالمستخدم والمهمة (user and the job).
- **عدم السؤال أبدًا عمّا إذا كان الذكاء الاصطناعي ضروريًا (Never asking whether AI is needed).** كثيرًا ما يزرع المحاورون مشكلات (plant problems) يتفوّق فيها حل أبسط (simpler fix wins). وقول ذلك، باختصار، يحصل على تقييم جيد (scores well).
- **ذكر أرقام اليوم على أنها حقائق (Quoting today's numbers as facts).** الأسعار ونوافذ السياق ودرجات المقاييس المعيارية (Prices, context windows and benchmark scores) تتغيّر. اشرح المنهج (Explain the method) وصِف أي رقم بأنه توضيحي (label any number as illustrative).
- **ملفات أعمال تُسرّب أو تبالغ في الادعاء (Portfolios that leak or overclaim).** نشر بيانات داخلية (internal data) أو تقديم عمل الفريق على أنه عملك (presenting team work as yours) قد يكلّفك أكثر من غياب دراسة حالة (missing case study). تحقّق من السرية (Check confidentiality) واذكر دورك بدقة (state your role precisely).
- **قصص النجاح فقط (Only success stories).** القتل أو النطاق المضيَّق (A kill or a narrowed scope)، إذا شُرح جيدًا، يُظهر الحكم أفضل من إطلاق «سار على نحو رائع (went great)».

## 🧾 الخلاصة (Recap)
- إدارة منتجات الذكاء الاصطناعي (AI PM) هي إدارة المنتج مضافًا إليها تفكير واضح (clear reasoning) في السلوك الاحتمالي والبيانات والتقييم والتكلفة والثقة (probabilistic behaviour, data, evaluation, cost and trust).
- اعرف شكل الدور الذي تتقدّم إليه (which role shape you are applying for): ميزات الذكاء الاصطناعي (AI feature)، أو منتج أصيل في الذكاء الاصطناعي (AI-native product)، أو منصة (platform)، أو بيانات وتعلّم آلي (data/ML).
- استخدم بنية إجابة ظاهرة (visible answer structure): المستخدم والمهمة، وهل الذكاء الاصطناعي صحيح، والأتمتة، والبيانات، والجودة والتقييمات، وأنماط الفشل، والمقاييس والتكلفة، والإطلاق (user and job, is AI right, automation, data, quality and evals, failure modes, metrics and cost, rollout).
- ابنِ ملف أعمال (portfolio) من دراستي حالة أو ثلاث صادقة (honest case studies) تُظهر القرارات والأدلة والمفاضلات (decisions, evidence and trade-offs)، ضمن حدود السرية (within confidentiality limits).
- انمُ بالإطلاق وتدوين ما تتعلمه (shipping and writing down what you learn)؛ وحافظ على إيقاع (cadence) يربط النماذج والتقنيات الجديدة بتقييماتك الخاصة (your own evals).

## ✍️ اختبر نفسك (Check yourself)

**1. في مقابلة، طُلب من فيصل أن «يصمّم مساعد ذكاء اصطناعي لمديري العلاقات الذين يستعدون لاجتماعات العملاء (design an AI assistant for relationship managers preparing for client meetings)». ما أفضل طريقة للبدء؟**

- A. وصف خط الاسترجاع (retrieval pipeline) والنموذج الذي سيُستخدم
- B. ذكر حجم نافذة السياق (context window) لأحدث النماذج وشرح كيف يحدّ هذا الحجم من كمية مواد العميل التي يستطيع المساعد قراءتها
- C. اقتراح نموذج تسعير (pricing model) للمساعد، بسعر لكل مقعد ونظرة تقريبية إلى الهامش
- D. توضيح من هو مدير العلاقة، وما يفعله اليوم للتحضير، وأين الألم (pain)، ثم التحقق من أن الذكاء الاصطناعي هو الأداة الصحيحة

<details><summary>الإجابة</summary>

**D.** تبدأ الإجابات القوية (Strong answers) بالمستخدم والمهمة (user and the job)، ثم تتساءل عمّا إذا كان الذكاء الاصطناعي مناسبًا (whether AI fits). والبدء بالبنية التقنية (Leading with architecture) (A) هو الفخ الكلاسيكي (classic trap) الذي أوقفته رانيا في المقابلة التجريبية. وذكر أرقام اليوم (Quoting today's numbers) (B) هشّ وخارج عن الموضوع (fragile and off the point). (🟢 الأساسيات (The essentials): بنية الإجابة (the answer structure).)

</details>

**2. عند سؤالك «كيف ستعرف أن مساعدنا المصرفي جيد؟ ⁦(how would you know our banking assistant is good?)⁩»، أي إجابة تُظهر مهارة مدير منتجات الذكاء الاصطناعي (AI PM skill) على أفضل وجه؟**

- A. «سنتتبّع تقييمات العملاء (customer ratings) بعد الإطلاق ونحقّق في أي شهر ينخفض فيه متوسط الدرجات.»
- B. «سنختار النموذج الذي يحتل المرتبة الأعلى في لوحات الصدارة العامة (public leaderboards) ونعيد فحص الترتيب كل ربع سنة.»
- C. «مجموعة مرجعية من مهام حقيقية (golden set) مقسّمة حسب المهمة واللغة، مع تحليل الأخطاء؛ ونموذج لغوي كبير حَكَم مُعايَر مقابل البشر (LLM judge) إضافة إلى الفريق الأحمر؛ ثم إطلاق مرحلي بمعيار متفق عليه ومقاييس وقائية.»
- D. «سيُجري فريق الهندسة مجموعة كاملة من اختبارات الوحدات (unit tests) على كل إصدار ويمنع أي بناء يفشل فيها.»

<details><summary>الإجابة</summary>

**C.** فهي تغطي طبقات التقييم غير المتصلة والقابلة للتوسّع والمتصلة (offline, scalable and online layers of evaluation). أما التقييمات وحدها (Ratings alone) (A) فتأتي متأخرة وتفوّت الأخطاء الصامتة (miss silent errors). والمقاييس المعيارية العامة (Public benchmarks) (B) لا تقيس مهام منتجك (your product's tasks). (🟡 التعمق أكثر (Going deeper): أسئلة التقييم (evaluation questions).)

</details>

**3. يريد فيصل نشر دراسة حالة لملف الأعمال (portfolio case study) عن نجم أسيست. أي نهج هو الصحيح؟**

- A. تضمين لقطات شاشة للوحة المعلومات الداخلية (internal dashboard) لإثبات النتائج، مع سطر يشرح كيف قاس الفريق الأرقام للقرّاء الراغبين في التحقق منها
- B. وصف القرار والأدلة والنتيجة (decision and result) بمستوى تفصيل يقبله البنك، وذكر دوره بدقة، وحذف الأرقام التي لا يُسمح له بمشاركتها
- C. قول «أنا بنيت نجم أسيست» (I built it) للاختصار
- D. تضمين الأجزاء التي سارت على نحو جيد فقط (went well)، كي تبقى دراسة الحالة قصيرة وتبدو قصة نجاح واضحة

<details><summary>الإجابة</summary>

**B.** السرية أولًا (Confidentiality comes first)، والإسناد الدقيق (precise attribution) يبني المصداقية (builds credibility). لقطات شاشة لوحات المعلومات الداخلية (A) تُعرّض البيانات لخطر التسريب (risk leaking data)؛ وعبارة «أنا بنيته (I built it)» (C) تبالغ في نسب عمل الفريق (overclaims a team's work)؛ وقصص النجاح وحدها (success-only stories) (D) تُخفي الحكم الذي يريد المحاورون رؤيته (the judgement interviewers want to see). (🟡 التعمق أكثر (Going deeper): ملف الأعمال (the portfolio).)

</details>

**4. إعلان وظيفي (job advert) يطلب مدير منتج ليتملّك «الوصول إلى النماذج وأدوات التقييم والضوابط الوقائية التي تستخدمها جميع فرق المنتج (model access, eval tooling and guardrails used by all product teams)». ما شكل هذا الدور (role shape)؟**

- A. مدير منتج لمنصة الذكاء الاصطناعي (AI platform PM)، يبني أدوات مشتركة تستخدمها الفرق الأخرى
- B. مدير منتج أصيل في الذكاء الاصطناعي (AI-native product PM)، يملك منتجًا للعملاء قائمًا على الذكاء الاصطناعي
- C. مدير منتج لميزات الذكاء الاصطناعي (AI feature PM)، يضيف الذكاء الاصطناعي إلى رحلة قائمة لفريق واحد
- D. مدير منتج للبيانات والتعلّم الآلي (Data/ML PM)، يملك مجموعات البيانات وخطوط تدريب النماذج

<details><summary>الإجابة</summary>

**A.** المنصة الداخلية التي تبني عليها الفرق الأخرى (internal platform that other teams build on) هي دور منصة (platform role)، يُستقصى فيه عن تجربة المطوّرين (developer experience) وإعادة الاستخدام (reuse) والحوكمة المدمجة (built-in governance). أما مدير المنتج الأصيل في الذكاء الاصطناعي (AI-native product PM) (B) فيملك منتجًا موجّهًا للعملاء (customer-facing product) قيمته الأساسية هي الذكاء الاصطناعي. (🟢 الأساسيات (The essentials): أشكال الأدوار (role shapes).)

</details>

**5. صدر نموذج جديد أرخص (new, cheaper model). ماذا يجب أن يفعل مدير منتجات ذكاء اصطناعي يتبع إيقاع تعلّم مستدامًا (sustainable learning cadence)؟**

- A. تحويل بيئة الإنتاج إليه فورًا لتوفير التكلفة (save cost)، لأن نموذجًا أرخص من المزوّد نفسه يُرجَّح أن يتصرف بالشكل ذاته تقريبًا
- B. تجاهله حتى يتبنّاه المنافسون (competitors)، كي لا يدفع الفريق ثمن نموذج لم يثبت الآخرون جدواه بعد في عملهم
- C. تشغيل مجموعة التقييمات الخاصة بالمنتج عليه (eval suite)، ثم القرار بحسب الجودة والتكلفة والمخاطر
- D. الاعتماد على درجاته في المقاييس المعيارية العامة (public benchmarks)، لأنها تقارنه بنماذج أقدم على المهام نفسها

<details><summary>الإجابة</summary>

**C.** مجموعتك المرجعية الخاصة (Your own golden set) هي أفضل دليل على ما إذا كان النموذج يعمل في مهامك (works for your tasks). أما التحويل الأعمى (Switching blindly) (A) فيتخطّى بوابة الانحدار (skips the regression gate)؛ والمقاييس المعيارية العامة (public benchmarks) (D) لا تقيس منتجك. (🔴 نظرة الخبير (Expert view): مواكبة المستجدات (staying current).)

</details>

## 📚 المراجع (References)
- دورة «من التخرّج إلى التوظيف (From Graduate to Hired)»، دورة المكتبة المهنية (career course): مسارات الأدوار (role paths)، ومعرض الأعمال (portfolio)، والسيرة الذاتية (CV)، والمقابلات (interviews)، والأيام التسعون الأولى (first 90 days): [../career/index.ar.html](../career/index.ar.html)
- Marty Cagan, *Inspired* (2nd ed., 2017) and *Empowered* (2020) — https://www.svpg.com
- Gayle Laakmann McDowell and Jackie Bavaro, *Cracking the PM Interview* (2013)
- Lewis C. Lin, *Decode and Conquer* (CIRCLES method)
- Teresa Torres, *Continuous Discovery Habits* (2021) — https://www.producttalk.org
- Kohavi, Tang and Xu, *Trustworthy Online Controlled Experiments* (2020) — https://experimentguide.com
- Chip Huyen, *AI Engineering* (O'Reilly, 2025) — https://www.oreilly.com
- Google PAIR, People + AI Guidebook — https://pair.withgoogle.com/guidebook
- Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (2023) — https://arxiv.org/abs/2306.05685

---

# 10.3 — الامتحان التدريبي: 60 سؤالًا قائمًا على سيناريوهات (Practice exam: 60 scenario questions)
*المستوى (Level): 🔴 متقدم (Advanced)* · *المتطلبات (Prerequisites): الوحدات 0–9 (Modules 0–9)* · *المرحلة (Stage): Discover, Define, Design, Build, Evaluate, Launch, Grow, Lead*

> **قيد المراجعة (under revision)، نوفمبر 2026.** في كثير من أسئلة هذا الامتحان التدريبي (practice exam) يمكن تمييز الخيار الصحيح من طوله أو صياغته، لذا فالدرجة العالية هنا لا تدل على الجاهزية (readiness) لأي امتحان حقيقي. استخدمه للتدرّب على التفكير (reasoning): أجب عن كل سؤال بكلماتك قبل أن تقرأ الخيارات، ثم قارن.

## ⚡ الدرس في دقيقة (In 60 seconds)
- هذا **امتحان تدريبي من 60 سؤالًا (60-question practice exam)** يغطي الدورة كلها، مجمّعًا حسب مراحل دورة الحياة الثماني (eight lifecycle stages): الاكتشاف (Discover)، والتعريف (Define)، والتصميم (Design)، والبناء (Build)، والتقييم (Evaluate)، والإطلاق (Launch)، والنمو (Grow)، والقيادة (Lead) (7–8 أسئلة لكل مرحلة). ومعظم الأسئلة سيناريوهات قصيرة (short scenarios) في بنك نجم (Najm Bank) أو في شركة محايدة (neutral company).
- **امنح نفسك 90 دقيقة، في جلسة واحدة، دون ملاحظات (Give yourself 90 minutes, in one sitting, with no notes).** اكتب كل إجابة قبل أن تفتح كتلة الإجابة (answer block) الخاصة بها. ونتيجتك (score) هي عدد الإجابات الصحيحة.
- لكل سؤال إجابة واحدة هي الأفضل (one best answer). وستبدو عدة خيارات معقولة (reasonable). اختر الخيار الذي سيختاره مدير منتج ذكاء اصطناعي حريص (careful AI product manager) **أولًا (first)** أو **أكثر من غيره (most)**، بناءً على ما يقوله السيناريو بالضبط.
- تشرح كل إجابة لماذا الخيار الصحيح صحيح، ولماذا الخيار الخاطئ الأكثر إغراءً (most tempting wrong option) خاطئ. وتنتهي بالمرحلة والدرس الذي ينبغي مراجعته (the stage and the lesson to review)، مثل *(Evaluate · 6.1)*.
- **اقرأ نتيجتك (score) خريطةً للفجوات (map of gaps):** الأسئلة التي أخطأت فيها تدلّك على الدروس التي ينبغي أن تدرسها مجددًا. والنتيجة العالية ليست معيار شهادة (certification standard) ولا علامة على الجاهزية (readiness). وهذه الدورة غير تابعة لأي جهة شهادات (certification body).

## 🧭 لماذا يهم (Why it matters)
أنهى فيصل الدورة في ثلاثة أسابيع وشعر بأنه مستعد. ثم سألته رانيا أربعة أسئلة سريعة في الممر: ما الذي سيقيسه أولًا (measure first) في نجم أسيست (Najm Assist)، ومتى سيوقف اختبار A/B (A/B test)، ومن يملك قرار (owns the decision) السماح للتمويل الفوري للشركات الصغيرة (SME Instant Finance) برفض طلب من تلقاء نفسه، وماذا يحدث لمساعد مذكرات الائتمان (Credit Memo Copilot) عندما يطرح مزوّد النموذج (model vendor) إصدارًا جديدًا. كان يعرف المصطلحات (the words) لكنه لم يعرف الإجابات. فمعرفة إطار عمل (framework) ليست مثل اللجوء إلى الإطار الصحيح عندما يُوصَف موقف في ثلاث جمل.

هذا ما يختبره هذا الامتحان. فالأسئلة ليست عن التعريفات (definitions). إنها تصف موقفًا (situation)، وغالبًا ما يكون فوضويًا (messy)، وتسأل ماذا ستفعل. والهدف (the aim) أن يجد القارئ الذي تصفّح على عجل (skimmed) إجابتين جذابتين، وأن يرى القارئ الذي فهم (understood) لماذا إحداهما خاطئة. وكثير من الأسئلة لا يحقق هذا الهدف بعد (انظر التنبيه (notice) أعلاه).

## 📐 كيف يعمل (How it works)
### 🟢 الأساسيات (The essentials)
للامتحان ثمانية أقسام (eight sections)، قسم لكل مرحلة من مراحل دورة الحياة (lifecycle stage). ويختبر كل سؤال درسًا واحدًا. ويبيّن الجدول التوزيع (the spread).

| المرحلة (Stage) | الأسئلة (Questions) | الدروس الرئيسية المختبَرة (Main lessons tested) |
|---|---|---|
| الاكتشاف (Discover) | 1–8 | 0.2، 1.1، 2.1، 2.2، 2.3 |
| التعريف (Define) | 9–15 | 1.3، 3.1، 3.3، 5.1 |
| التصميم (Design) | 16–23 | 4.1، 4.2، 4.3 |
| البناء (Build) | 24–30 | 1.2، 3.2، 5.2، 5.3 |
| التقييم (Evaluate) | 31–38 | 6.1، 6.2، 6.3 |
| الإطلاق (Launch) | 39–45 | 7.1، 7.2، 7.3 |
| النمو (Grow) | 46–53 | 8.1، 8.2، 8.3 |
| القيادة (Lead) | 54–60 | 9.1، 9.2، 9.3، 9.4، 10.2 |

### 🟡 التعمق أكثر (Going deeper)
اقرأ الجملة الأخيرة من كل سؤال أولًا. فهي تخبرك بما هو مطلوب: الخطوة *الأولى (first)*، أو الخيار *الأفضل (best)*، أو السبب *الأرجح (most likely)*، أو ما هو *الخطأ (wrong)*. ثم اقرأ السيناريو وضع خطًا تحت الحقائق المهمة (facts that matter): من هو المستخدم (who the user is)، وما الذي على المحك إذا أخطأ المنتج (what is at stake if the product is wrong)، وما البيانات الموجودة (what data exists)، وما الذي جُرِّب بالفعل (what has already been tried).

### 🔴 نظرة الخبير (Expert view)
تتبع الخيارات المضلِّلة (distractors) أنماطًا (patterns) صادفتها طوال الدورة. انتبه إلى الإجابة التي تقفز إلى التقنية قبل أن تتضح المشكلة (jumps to technology before the problem is clear)، والإجابة التي تقيس التكلفة لا الجودة (measures cost but not quality)، والإجابة التي تثق بنتيجة غير متصلة (offline score) كدليل على قيمة في العالم الحقيقي (real-world value)، والإجابة التي تسلّم قرارًا عالي المخاطر (high-stakes decision) لنموذج دون مسار بشري (no human path)، والإجابة التي تبدو شاملة (sounds thorough) لكنها تأتي بترتيب خاطئ (wrong order).

## 🧰 الأدوات (The toolkit)
| الأداة أو الإطار (Tool or framework) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **Stage map** — خريطة المراحل | مراحل دورة الحياة الثماني (eight lifecycle stages) مستخدمةً عدسةً (lens) لكل سؤال | لتحديد موقع السيناريو (place a scenario) قبل اختيار الإجابة |
| **Error log** — سجل الأخطاء | قائمة بكل إجابة خاطئة أو مخمَّنة (wrong or guessed answer)، مع الدرس الذي ينبغي مراجعته والفخ الذي وقعت فيه (the trap you fell for) | فور تصحيح الامتحان (straight after marking the exam) |
| **Trap checklist** — قائمة تحقق الفخاخ | أنماط الخيارات المضلِّلة الخمسة (five distractor patterns) في «نظرة الخبير (Expert view)» أعلاه | عندما يبدو خياران صحيحين معًا (two options both look right) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
تُجري رانيا هذا الامتحان مع كل مدير منتج ذكاء اصطناعي جديد (new AI product manager) في شهره الأول. ولا تهتم كثيرًا بالنتيجة (score). بل تهتم بسجل الأخطاء (error log). ويستخدم الفريق قالبًا مشتركًا واحدًا (one shared template):

| # | إجابتي (My answer) | الصحيحة (Correct) | المرحلة · الدرس (Stage · lesson) | الفخ الذي وقعت فيه (Trap I fell for) | ما سأعيد قراءته (What I will re-read) |
|---|---|---|---|---|---|
| 12 | A | D | Define · 5.1 | القفز إلى التقنية (Jumped to technology) | 5.1 «التعمق أكثر (Going deeper)» |
| 37 | C | A | Evaluate · 6.3 | قراءة النتائج قبل التحقق من صلاحية الاختبار (Read results before checking the test was valid) | 6.3 عن عدم تطابق نسبة العينة (sample ratio mismatch) |

## 🛠️ التمارين (Exercises)
- 🟢 **أدِّ الامتحان (Sit the exam).** أجب عن الأسئلة الستين كلها في 90 دقيقة دون ملاحظات (without notes). *يكتمل عندما (Done when):* تكون لديك نتيجة (score) وإجابة مكتوبة لكل سؤال.
- 🟡 **ابنِ سجل أخطائك (Build your error log).** لكل إجابة خاطئة أو مخمَّنة (wrong or guessed answer)، املأ صفًا واحدًا من القالب أعلاه. *يكتمل عندما (Done when):* يسمّي كل صف فخًا (trap) وقسمًا لإعادة قراءته (section to re-read).
- 🔴 **اكتب أسئلتك الخاصة (Write your own).** لأضعف مرحلتين لديك (two weakest stages)، اكتب سؤالين جديدين قائمين على سيناريو (scenario questions) لكل منهما، في بنك نجم أو في مؤسستك، مع إجابة تشرح أفضل خيار مضلِّل (best distractor). *يكتمل عندما (Done when):* يجيب عنها زميل ويجد خيارًا مضلِّلًا مغريًا (distractor tempting) في واحد منها على الأقل.

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **فتح الإجابات أثناء الحل (Opening answers as you go).** يحوّل ذلك الامتحان إلى تمرين قراءة (reading practice). اكتب إجاباتك كلها أولًا.
- **احتساب التخمينات المحظوظة معرفةً (Counting lucky guesses as knowledge).** علّم أي إجابة لم تكن متأكدًا منها على أنها خاطئة في سجل أخطائك (error log)، حتى لو كانت صحيحة.
- **اختيار الخيار الذي يبدو الأكمل (Picking the most complete-sounding option).** كثير من الأسئلة يسأل عمّا تفعله *أولًا (first)*. والخطة الكاملة (complete plan) غالبًا ما تكون الإجابة الخاطئة.
- **الإجابة عن الشركة التي تعرفها بدلًا من الشركة الموصوفة (Answering for the company you know instead of the one described).** استخدم الحقائق الواردة في السيناريو فقط (only the facts in the scenario).

## ✍️ الامتحان التدريبي (Practice exam)

### الاكتشاف (Discover)

**1. يقول خالد، رئيس الإقراض للأفراد (Head of Retail Lending)، لفيصل: «لدى جميع منافسينا ذكاء اصطناعي في تطبيقاتهم. ضع الذكاء الاصطناعي في رحلة الإقراض (lending journey) هذا الربع». ما الذي يجب أن يفعله فيصل أولًا؟**

- A. إعداد قائمة مختصرة بثلاثة مزوّدي نماذج وطلب عرض توضيحي (vendor demo) من كل منهم على عيّنة من بيانات الإقراض لمقارنة الجودة قبل الاختيار
- B. رسم خريطة رحلة الإقراض مع العملاء والموظفين للعثور على المهام ونقاط الألم (pain points) التي يمكن أن يغيّر فيها الذكاء الاصطناعي نتيجةً
- C. بناء روبوت محادثة (chatbot) لصفحة الإقراض، لأنه أسرع طريقة لإظهار استخدام البنك للذكاء الاصطناعي أمام عملائه
- D. كتابة وثيقة متطلبات المنتج (product requirements document) لمساعد قروض ذكي كي تبدأ الهندسة تقدير العمل وتخطيط الربع

<details><summary>الإجابة</summary>

**B.** يبدأ الاكتشاف (Discovery) من المهمة التي يحاول المستخدم إنجازها (the job the user is trying to get done) ومن سير العمل (workflow) الذي تحدث فيه، لا من التقنية. ولا يمكنك الحكم على ما إذا كان الذكاء الاصطناعي مناسبًا (whether AI fits) إلا بعد أن تعرف أين يكمن الألم. والخيار A مغرٍ (tempting) لأنه يبدو تقدمًا (feels like progress)، لكن اختيار المزوّدين قبل معرفة المشكلة يعني أنك ستقيّمهم على المهام الخاطئة (wrong tasks). وكل من C وD يلتزم بحل لم يتحقق منه أحد (a solution nobody has validated). *(Discover · 2.1)*

</details>

**2. يقيّم فيصل ثلاث حالات استخدام مرشّحة (candidate use cases) على مقياس من 1 إلى 5 للقيمة التجارية فقط (business value only)، ويضع «الرفض بالذكاء الاصطناعي لتمويل فواتير الشركات الصغيرة (AI declines for SME invoice finance)» في المرتبة الأولى. تعيد رانيا بطاقة التقييم (scorecard). ما أفضل إصلاح؟**

- A. استبدال مقياس 1–5 بمقياس 1–10 (scale) كي تتضح الفروق بين حالات الاستخدام الثلاث بصورة أكبر
- B. الطلب من خالد تأكيد الترتيب (ranking)، لأنه يملك النتيجة التجارية ويعرف أي حالة استخدام هي الأهم للبنك من بين الحالات الثلاث كلها وأعلاها قيمة
- C. الإبقاء على الترتيب مع إضافة ملاحظة (note) بأن الفكرة الأولى تحتاج إلى اختبار إضافي قبل أن يلتزم الفريق بها
- D. تقييم كل حالة استخدام على القيمة والجدوى التقنية والمخاطر، ومعاملة المخاطر المرتفعة جدًا بوصفها بوابة (gate) تُحلّ قبل الترتيب

<details><summary>الإجابة</summary>

**D.** تحتاج بطاقة تقييم حالات الاستخدام (use-case scorecard) إلى ثلاث عدسات على الأقل: القيمة (value) (هل تستحق العناء)، والجدوى التقنية (feasibility) (هل لدينا البيانات والمهارات والتقنية)، والمخاطر (risk) (ما الضرر إذا أخطأت). ورفض الائتمان الآلي (automated credit declines) عالي القيمة لكنه عالي المخاطر أيضًا، لذا يجب تقييم المخاطر، ويمكنها وحدها أن توقف الفكرة (block the idea on its own). والخيار B مغرٍ لأن خالدًا يملك القيمة، لكن موافقته (sign-off) لا تضيف بُعدَي الجدوى التقنية والمخاطر المفقودين (missing feasibility and risk dimensions). أما A فيغيّر المقياس فقط. *(Discover · 2.2)*

</details>

**3. تُحدَّد رسوم التسوية المبكرة للقرض (early loan settlement) في بنك نجم بتعرفة منشورة (published tariff): معادلة ثابتة (fixed formula) تعتمد على الرصيد والمدة المتبقية (balance and remaining term). يقترح فريق ميزة قائمة على نموذج لغوي كبير (LLM feature) «تحسب الرسوم» عندما يسأل العملاء. ما أفضل توصية؟**

- A. حساب الرسوم بشيفرة عادية (ordinary code) من التعرفة، واستخدام الذكاء الاصطناعي في أقصى الأحوال لشرح النتيجة
- B. استخدام النموذج اللغوي الكبير (LLM) مع خفض درجة الحرارة كي يحسب الرسوم بثبات في كل مرة يسأل فيها العميل عنها
- C. الضبط الدقيق (fine-tuning) لنموذج على حسابات الرسوم السابقة كي يتعلم معادلة التعرفة من أمثلة محلولة كثيرة للتسويات
- D. استخدام النموذج اللغوي الكبير وإضافة إخلاء مسؤولية (disclaimer) بأن الرسوم المعروضة تقديرية وقد يختلف الرقم النهائي عند التسوية

<details><summary>الإجابة</summary>

**A.** عندما تكون الإجابة محدَّدة بالكامل بقاعدة معروفة (fully determined by a known rule)، يكون البرنامج الحتمي (deterministic software) أرخص وأسرع ودقيقًا وقابلًا للتدقيق (auditable). أما النموذج الاحتمالي (probabilistic model) فيضيف خطأً بلا مكسب. والخيار B مغرٍ، لكن خفض درجة الحرارة يقلّل العشوائية (reduces randomness)؛ ولا يجعل النموذج اللغوي آلة حاسبة موثوقة (reliable calculator). أما D فيدفع أخطاء النموذج إلى العميل في أمر يكون فيه رقم البنك ملزِمًا (binding). *(Discover · 2.3)*

</details>

**4. في شجرة الفرص والحلول (Opportunity Solution Tree) لتيريزا توريس (Teresa Torres)، كتبت حصة النتيجة (outcome) «زيادة حصة طلبات تمويل فواتير الشركات الصغيرة المكتملة في التطبيق (Increase the share of SME invoice-finance requests completed in the app)». ما الذي يجب أن يأتي تحتها مباشرة؟**

- A. قائمة بميزات الذكاء الاصطناعي (AI features) التي يمكن للفريق بناؤها لتحريك النتيجة، مرتبةً حسب سهولة إطلاق كل ميزة هذا العام
- B. التجارب (experiments) التي سيُجريها الفريق في هذه الدورة القصيرة، لكل منها فرضية وموعد لقراءة النتيجة
- C. الفرص: احتياجات العملاء وآلامهم ورغباتهم المكتشفة في البحث (research)، مثل «لا أعرف أي الفواتير مؤهلة»
- D. خيارات النماذج (model options) التي يمكن للفريق استخدامها، مرتبةً حسب الدقة على المقاييس العامة للمهام المعنية

<details><summary>الإجابة</summary>

**C.** تمتد الشجرة من النتيجة (outcome)، إلى الفرص (opportunities) (احتياجات وآلام وُجدت عبر البحث)، إلى الحلول (solutions)، إلى التجارب (experiments) التي تختبر تلك الحلول. وتقع الفرص بين النتيجة وأي حل كي لا يقفز الفريق من هدف مباشرةً إلى ميزة (from a goal straight to a feature). والخيار A هو الأكثر إغراءً لأن الميزات تبدو ملموسة (concrete)، لكن سردها مباشرةً تحت النتيجة يتخطى الخطوة التي تخبرك بالمشكلة التي تحلها كل ميزة (which problem each feature solves). *(Discover · 2.1)*

</details>

**5. يوشك فيصل على إجراء تجربة تجريبية (pilot) مدتها أربعة أسابيع لأداة ذكاء اصطناعي تقترح الخطوات التالية (suggests next steps) على مديري علاقات الشركات الصغيرة (SME relationship managers). تطلب منه رانيا إضافة شيء واحد إلى خطة التجربة (pilot plan) قبل بدئها. ما الأرجح أن يكون؟**

- A. قائمة بميزات إضافية (extra features) تُضاف إذا نجحت التجربة، كي ينتقل الفريق بسرعة إلى المرحلة التالية
- B. مسودة بيان صحفي تعلن النتائج، كي يكون التسويق (marketing) جاهزًا للنشر فور انتهاء التجربة وظهور أرقام جيدة
- C. معايير الإيقاف (kill criteria) المتفق عليها مسبقًا: النتيجة التي تتوقف الفكرة إن نزلت عنها، مثل استخدام أقل من نسبة محددة
- D. فترة تجربة أطول (longer pilot)، لأن أربعة أسابيع نادرًا ما تكفي لرؤية كيف يستخدم مديرو العلاقات أداة ذكاء اصطناعي في عملهم اليومي

<details><summary>الإجابة</summary>

**C.** الاتفاق على شرط الإيقاف (stop condition) قبل وصول البيانات يحمي الفريق من تحريك المرمى (moving the goalposts) بعد أن يتعلّق بالفكرة. وإيقاف الأفكار الضعيفة مبكرًا (killing weak ideas early) هو ما يُبقي محفظة الذكاء الاصطناعي (AI portfolio) في حدود المقدور عليه (affordable). والخيار D مغرٍ، وأحيانًا تحتاج التجربة إلى وقت أطول، لكن تجربة أطول دون قاعدة قرار (decision rule) لا تفعل إلا تأجيل الجدال نفسه. *(Discover · 2.3)*

</details>

**6. يقارن خالد مساعد مذكرات الائتمان (Credit Memo Copilot) بنظام إنشاء القروض (loan origination system) في البنك: «دفعنا ثمن النظام مرة واحدة. فلماذا تكبر فاتورة المساعد كل شهر؟» ما أفضل تفسير؟**

- A. كل طلب ذكاء اصطناعي يستهلك حوسبة أو رموزًا (tokens) مدفوعة، فتزيد التكلفة مع الاستخدام، بينما الاستخدام الإضافي شبه مجاني في البرمجيات التقليدية
- B. المزوّد يبالغ في السعر (overcharging) على المساعد، وعلى المشتريات أن تعيد التفاوض على العقد وتطلب سعرًا أقل
- C. النموذج لا يزال يتدرب (training) على بيانات نجم، وهو جهد مقدّم سيتوقف بعد نحو سنة ثم تنخفض الفاتورة
- D. برمجيات الذكاء الاصطناعي تكلّف دائمًا أكثر من البرمجيات التقليدية طوال عمرها، لذا فمن المتوقع ببساطة أن تكون الفاتورة أعلى من فاتورة النظام القديم (total cost)

<details><summary>الإجابة</summary>

**A.** من السمات المميِّزة لمنتجات الذكاء الاصطناعي (defining feature of AI products)، وخاصة التوليدية منها، وجود تكلفة حدّية حقيقية لكل استخدام (real marginal cost per use): فكل استدعاء للنموذج (call to the model) يكلّف مالًا. ولهذا تحتاج منتجات الذكاء الاصطناعي إلى نموذج تكلفة لكل مهمة (cost-per-task model) وإلى تسعير يتتبّع الاستخدام (pricing that tracks usage). وقد يكون B صحيحًا أحيانًا، لكنه لا يفسّر النمط (pattern). والخيار C خاطئ: فاستدعاء النموذج لا يدرّبه عادةً. أما D فتعميم غير مدعوم (unsupported generalisation). *(Discover · 0.2)*

</details>

**7. يُظهر بحث حصة عن «مدرب ادخار (savings coach)» جديد في نجم أسيست (Najm Assist) أن العملاء يقولون إنهم يريدونه، لكن أيًا من العملاء الثمانية الذين قابلتهم لم يستخدم قط ميزة أهداف الادخار (savings goals feature) الحالية في البنك. أي من المخاطر الأربع الكبرى (four big risks) لمارتي كاغان (Marty Cagan) يثيره هذا الدليل أساسًا؟**

- A. مخاطر الجدوى التقنية (feasibility risk): هل يستطيع الفريق بناء مدرّب الادخار بما لديه من بيانات ومهارات وتقنية اليوم داخل المؤسسة
- B. مخاطر قابلية الاستخدام (usability risk): هل يستطيع العملاء معرفة كيفية استخدام مدرّب الادخار بعد أن يصبح داخل التطبيق فعلًا
- C. مخاطر الجدوى التجارية (business viability risk): هل يتوافق مدرّب الادخار مع القيود القانونية والمالية والتجارية للبنك كلها
- D. مخاطر القيمة (value risk): هل سيختار العملاء استخدامه فعلًا مهما قالوا في المقابلات

<details><summary>الإجابة</summary>

**D.** مخاطر كاغان الأربع هي القيمة (value) (هل سيستخدمونه أو يشترونه)، وسهولة الاستخدام (usability) (هل يستطيعون معرفة كيف)، والجدوى التقنية (feasibility) (هل نستطيع بناءه)، والجدوى التجارية (business viability) (هل ينجح للعمل، بما في ذلك القيود القانونية والمالية (legal and financial constraints)). وما يقول الناس إنهم يريدونه يختلف عمّا يفعلونه (what people say they want and what they do differ)، وهنا يوحي السلوك (behaviour) بأنهم قد لا يقدّرون الميزة. والخيار B مغرٍ لأن الميزة القديمة ربما كانت صعبة الاستخدام، لكن الدليل يتعلق بالطلب (demand)، لا بالصعوبة (difficulty). *(Discover · 2.1)*

</details>

**8. يريد فريق الاحتيال (fraud team) تحسين التنبيهات الذكية (Smart Alerts)، التي تُعلِّم معاملات البطاقات المشبوهة (suspicious card transactions) من بيانات منظَّمة (structured data): المبلغ، والتاجر، والموقع، والوقت. أي نهج هو الأنسب للبداية (best starting fit)؟**

- A. نموذج لغوي كبير يقرأ كل معاملة ويكتب حكمًا قصيرًا على ما إذا كانت تبدو احتيالية، مع أسبابه، ثم يرسله إلى المحللين (LLM)
- B. مصنِّف تعلّم آلي كلاسيكي (classic classifier) مدرَّب على حالات احتيال سابقة موسومة، يقيّم كل معاملة لحظة وصولها
- C. وكيل مستقل (autonomous agent) يحقق في كل معاملة باستخدام أدوات، ويجلب بيانات إضافية قبل أن يقرر ويكتب تقريرًا
- D. نموذج صور توليدي يحوّل أنماط الإنفاق إلى رسوم بيانية (charts) كي يلاحظ المحللون النشاط غير المعتاد في الحسابات

<details><summary>الإجابة</summary>

**B.** تصنيف السجلات المنظَّمة (scoring structured records) إلى «احتيال» أو «ليس احتيالًا»، بحجم كبير وزمن استجابة منخفض (high volume and low latency)، هو ما يُجيده التعلّم الآلي الخاضع للإشراف التقليدي (classic supervised machine learning). وهو أرخص وأسرع لكل معاملة من النموذج اللغوي الكبير (LLM)، وقابل للقياس بالدقة (precision) والاستدعاء (recall). والخيار A مغرٍ لأن النماذج اللغوية الكبيرة جديدة ومرنة (flexible)، لكن توليد نص عن كل معاملة يضيف تكلفة وزمن استجابة (cost and latency) ولا يناسب مهمة تقييم كبيرة الحجم (high-volume scoring task). *(Discover · 1.1)*

</details>

### التعريف (Define)

**9. تقول المواصفات الأولى (first spec) التي كتبها فيصل لمساعد مذكرات الائتمان (Credit Memo Copilot): «يجب أن تكون مسودة المذكرة دقيقة ومفيدة (accurate and helpful)». تقول دانة إنها لا تستطيع البناء أو الاختبار وفقها. ما الذي يجب أن يحل محلها؟**

- A. معايير جودة قابلة للقياس مرتبطة بتقييم (evaluation)، مثل «على المجموعة الذهبية من 200 حالة سابقة، حدٌّ أقصى لنسبة المسودات التي تحوي رقمًا خاطئًا»
- B. وصف مكتوب أطول لما تعنيه «الدقة» و«الفائدة» لمديري العلاقات، مع أمثلة محلولة (worked examples) لكل منهما، لتوضيح المعنى
- C. اشتراط استخدام النموذج الأعلى درجة على المقاييس العامة (public benchmarks) لمهام التلخيص والكتابة من هذا النوع بالذات
- D. عبارة بأن مديري العلاقات سيراجعون كل مسودة بأنفسهم، فالدقة مسؤوليتهم لا مسؤولية المنتج (responsibility)

<details><summary>الإجابة</summary>

**A.** في مواصفات الذكاء الاصطناعي (AI spec)، التقييمات هي المتطلبات (evals are the requirements): فكل توقّع للجودة (quality expectation) يحتاج إلى مقياس (metric)، ومجموعة بيانات يُقاس عليها (dataset)، وعتبة (threshold). وهذا يعطي دانة شيئًا تبني نحوه، ويعطي الفريق معيار إطلاق واضحًا (clear launch bar). والخيار C مغرٍ لأنه يبدو صارمًا (rigorous)، لكن المقاييس المعيارية العامة لا تقيس مهمتك على بياناتك (your task on your data). أما D فيخلط بين الضمانة (safeguard) والمتطلب (requirement). *(Define · 5.1)*

</details>

**10. تخطط دانة لتدريب التمويل الفوري للشركات الصغيرة (SME Instant Finance) على خمس سنوات من قرارات تمويل الفواتير السابقة (past invoice-finance decisions) ونتائج سدادها (repayment outcomes). ما أهم مشكلة في جاهزية البيانات (data-readiness problem) يجب طرحها؟**

- A. خمس سنوات بيانات قليلة جدًا (too little) على أي نموذج كي يتعلم منها، فعلى الفريق الانتظار حتى تتوافر سنوات أكثر
- B. يجب أولًا نقل البيانات إلى منصة سحابية (cloud platform) جديدة قبل تدريب أي نموذج عليها أصلًا
- C. نتائج السداد موجودة فقط للطلبات الموافَق عليها، فلا يرى النموذج أبدًا كيف كان سيتصرف المتقدمون المرفوضون (rejected applicants)
- D. بيانات الفواتير منظَّمة (structured)، والبيانات المنظَّمة لا يمكن أن يستخدمها الذكاء الاصطناعي، لذا يحتاج الفريق إلى مستندات بدلًا منها

<details><summary>الإجابة</summary>

**C.** هذه مشكلة وسوم (label problem) كلاسيكية في الإقراض: فالنتائج لا تُرصد إلا للمتقدمين المقبولين (approved applicants)، لذا فبيانات التدريب (training data) منحازة بعملية القرار القديمة (biased by the old decision process). ويجب أن يعرف الفريق ذلك ويخطط له قبل أن يعد بأداء معيّن (promising performance). والخيار A مغرٍ لأن المزيد من البيانات يساعد غالبًا، لكن لا توجد قاعدة تقول إن خمس سنوات قليلة؛ فكون البيانات مناسبة للغرض (fit for purpose) أهم من عمرها. أما D فخاطئ. *(Define · 3.1)*

</details>

**11. يجب أن يجيب مساعد مذكرات الائتمان عن أسئلة حول دليل سياسة الائتمان (credit policy manual) في نجم، الذي يُحدَّث عدة مرات في السنة، ويجب أن يبيّن القسم الذي جاءت منه كل إجابة. أي نهج من طيف البناء (build spectrum) هو الأنسب؟**

- A. تدريب نموذج جديد من الصفر (from scratch) على دليل السياسة، كي يحمل كل قاعدة في أوزانه الخاصة
- B. التوليد المعزَّز بالاسترجاع (RAG): جلب أقسام السياسة ذات الصلة وقت السؤال والإجابة منها، مع الاستشهادات
- C. الضبط الدقيق لنموذج على الدليل الحالي، وإعادة الضبط بعد كل تحديث كي يبقى النموذج متوافقًا مع السياسة (fine-tuning)
- D. وضع ملخص للدليل في موجِّه النظام (system prompt) كي تبدأ كل إجابة من السياسة

<details><summary>الإجابة</summary>

**B.** يناسب التوليد المعزّز بالاسترجاع (RAG) المعرفةَ التي تتغير والإجاباتِ التي يجب أن تستشهد بالمصادر (cite sources): حدِّث المستندات فتتحدّث الإجابات، والمقاطع المسترجَعة (retrieved passages) تعطي الاستشهادات. والخيار C هو الخيار المضلِّل المغري (tempting distractor). فالضبط الدقيق (Fine-tuning) يشكّل أساسًا السلوك والأسلوب والتنسيق (behaviour, style and format)؛ وهو طريقة ضعيفة لإبقاء الحقائق محدَّثة (keep facts current)، ويجب تكراره مع كل تغيير، ولا يعطيك استشهادات. أما D فيُضيّع التفاصيل. *(Define · 1.3)*

</details>

**12. تسرد مواصفات فيصل لنجم أسيست (Najm Assist) كل ما يجب أن يفعله المساعد. في المراجعة، تسأل ليلى عمّا هو ناقص. ما أهم فجوة (gap)؟**

- A. قائمة بكل سؤال قد يطرحه العملاء (customer questions)، كي يُختبر المساعد على كل واحد منها قبل الإطلاق
- B. اسم النموذج ونسخته (model version) كي يعرف فريقا الهندسة والمخاطر ما الذي يجري نشره بالضبط
- C. العدد المستهدف للمحادثات اليومية (daily conversations) كي يحدد الفريق حجم البنية التحتية والميزانية
- D. ما يجب ألا يفعله المساعد وكيف يتصرف حينها (out-of-scope): مواضيع يرفضها مثل النصيحة الاستثمارية الشخصية، ومتى يحوّل إلى موظف بشري

<details><summary>الإجابة</summary>

**D.** يجب أن تعرّف مواصفات سلوك الذكاء الاصطناعي (AI behaviour spec) السلوكَ خارج النطاق (out-of-scope behaviour) والرفضَ (refusals) والتصعيدَ (escalation) بالعناية نفسها التي تعرّف بها المسار السعيد (happy path)، لأن النظام الاحتمالي (probabilistic system) سيتلقى طلبات لم تخطط لها. والخيار B مغرٍ لأن المهندسين يحتاجون إليه، لكن النموذج خيار تنفيذي (implementation choice) قد يتغير؛ أما السلوك الذي يجب أن يضمنه المنتج فهو المتطلب (requirement). والخيار A مستحيل الإكمال. *(Define · 5.1)*

</details>

**13. يقترح طارق استخدام سجلات محادثات (chat transcripts) نجم أسيست لعامين لتحسين إجابات المساعد. ما الذي يجب أن يفعله فيصل قبل استخدام أي سجل؟**

- A. إخفاء هوية النصوص (anonymise) بحذف أسماء العملاء منها، ثم المتابعة في أعمال التحسين على النصوص كما هي
- B. سؤال سارة، مسؤولة حماية البيانات (DPO)، هل يتوافق هذا الاستخدام مع الغرض الأصلي، وهل له أساس قانوني، وما التقليل المطلوب
- C. المتابعة (proceed)، لأن البنك يحتفظ بالبيانات أصلًا وقد جُمعت في سياق خدمة العملاء المعتاد، فلا قيد على استخدامها ولا حاجة لسؤال أحد
- D. سؤال مزوّد النموذج (model vendor) هل يسمح باستخدام النصوص، لأن المزوّد سيعالجها وهو من يحدد شروط الاستخدام

<details><summary>الإجابة</summary>

**B.** الاحتفاظ بالبيانات لا يعني أنك تستطيع استخدامها لأي غرض. فإعادة استخدام محادثات العملاء لتحسين المنتج (product improvement) تثير أسئلة تقييد الغرض (purpose limitation) والأساس القانوني (lawful basis) وتقليل البيانات (minimisation) بموجب قوانين مثل GDPR وقانون حماية خصوصية البيانات الشخصية في قطر (Qatar's PDPPL)، ومدير المنتج (PM) مسؤول عن الحصول على هذه الإجابة قبل البناء. والخيار A مغرٍ، لكن حذف الأسماء نادرًا ما يكفي لإخفاء هوية المحادثات النصية الحرة (free-text chats)، التي كثيرًا ما تحتوي أرقام حسابات ومعرّفات أخرى (identifiers)؛ وهذا جزء مما يجب أن تقيّمه سارة. *(Define · 3.3)*

</details>

**14. في التنبيهات الذكية (Smart Alerts)، يكلّف الاحتيال الفائت (missed fraud) العميلَ مالًا وثقة، بينما يكلّف الإنذار الكاذب (false alarm) لحظة انزعاج، وإذا تكرر، إرهاق التنبيهات (alert fatigue). كيف يجب أن يتعامل فريق المنتج مع ذلك عند تعريف المنتج؟**

- A. معاملة تكلفة كل نوع من الخطأ بوصفها قرارًا منتجيًا (product decision)، وكتابتها في المواصفات، واستخدامها لتحديد العتبة
- B. ترك العتبة (threshold) لفريق علم البيانات، لأنها معامل تقني يضبطه كل يوم ضمن صيانة النموذج، وهو الأعرف بالنموذج وببيانات التدريب
- C. تعظيم الدقة الإجمالية (overall accuracy)، فهي توازن نوعي الخطأ تلقائيًا ولا تحتاج إلى قرارات إضافية من الفريق
- D. تقليل الإنذارات الكاذبة أولًا، لأن العملاء يشتكون منها أكثر وإرهاق التنبيهات (alert fatigue) هو الخطر الأكبر

<details><summary>الإجابة</summary>

**A.** أي الخطأين أسوأ، وبكم، هو حكم تجاري وحكم يتعلق بالمستخدم (business and user judgement). ويجب أن يجعله مدير المنتج صريحًا (explicit) كي تعكسه العتبة (threshold). والخيار C هو المغري، لكن الدقة الإجمالية مضلِّلة عندما يكون الاحتيال نادرًا: فالنموذج الذي لا يطلق تنبيهًا أبدًا قد يكون «دقيقًا» جدًا وعديم الفائدة (highly "accurate" and useless). أما B فيسلّم مفاضلة منتج (product trade-off) إلى الفريق الأقل قدرة على أن يوازن وحده بين ضرر العميل والانزعاج. *(Define · 5.1)*

</details>

**15. يريد بنك نجم مساعدًا داخليًا (internal assistant)، هو مساعد الموظفين التوليدي (Staff GenAI)، لمساعدة الموظفين على صياغة الرسائل الإلكترونية وتلخيص المستندات والبحث في السياسات الداخلية. لا شيء فيه خاص بالعمل المصرفي. ما الخيار الافتراضي الأكثر حكمة (most sensible default)؟**

- A. تدريب نموذج خاص من الصفر (proprietary model) كي يملك البنك التقنية ولا يعتمد على مورّد خارجي في عمله اليومي
- B. الضبط الدقيق لنموذج مفتوح الأوزان (open-weight) قبل تقييم أي منتج قائم، كي تناسب النتيجة لغة البنك واحتياجاته وبياناته الخاصة
- C. شراء أو ترخيص منتج مؤسسي (enterprise product) يلبي احتياجات البنك الأمنية والبيانية، وصرف الجهد على التبنّي والتكامل
- D. البناء من الصفر كي يُباع المساعد لاحقًا لبنوك أخرى بوصفه خط أعمال جديدًا (product line) يدرّ دخلًا

<details><summary>الإجابة</summary>

**C.** عندما تكون القدرة عامة (generic) وليست مصدرًا للميزة التنافسية (source of advantage)، يكون الشراء عادةً أسرع وأرخص، وينتقل عمل المنتج إلى الملاءمة والأمن والتبنّي والتكامل (fit, security, adoption and integration). ابنِ حيث تتميّز (Build where you differentiate). والخيار B مغرٍ لأنه يبدو طريقًا وسطًا (middle path)، لكنه يلتزم بجهد هندسي (engineering effort) قبل أن يتحقق أحد مما إذا كان منتج موجود يلبي الحاجة بالفعل. *(Define · 1.3)*

</details>

### التصميم (Design)

**16. أي مستوى من الأتمتة (level of automation) يناسب مساعد مذكرات الائتمان (Credit Memo Copilot) أكثر عند الإطلاق؟**

- A. التنفيذ (Act): يقدّم المساعد المذكرات النهائية إلى لجنة الائتمان تلقائيًا، مع سجل كامل بكل ما أُرسل منها
- B. القرار (Decide): يوصي المساعد بالموافقة أو الرفض، ويبقى القرار قائمًا ما لم يعترض شخص خلال مهلة محددة
- C. الاقتراح (Suggest): يكتفي المساعد بسرد الحقائق والأرقام من ملف الائتمان، ويكتب مدير العلاقات كل كلمة بنفسه
- D. المسودة (Draft): يعدّ المساعد مذكرة يراجعها مدير العلاقات ويعدّلها ويوقّعها بوصفها مذكرته

<details><summary>الإجابة</summary>

**D.** توفّر الصياغة (Drafting) على مدير العلاقات وقت الكتابة الثقيلة (heavy writing) مع إبقاء شخص مسمّى ومُساءَل (named, accountable person) مسؤولًا عن مستند ائتماني عالي المخاطر (high-stakes credit document). والخياران A وB يزيلان الحكم البشري (human judgement) الذي تتطلبه قرارات الائتمان. والخيار C هو الخيار الحذر المغري (tempting cautious choice)، لكنه يتخلى عن معظم القيمة في حين أن تدفق صياغة ومراجعة (draft-and-review flow) جيد التصميم يستطيع إدارة المخاطر. *(Design · 4.1)*

</details>

**17. في الاختبارات المبكرة، يتوقع مديرو العلاقات أن يعرف مساعد مذكرات الائتمان عن اجتماعات مع العملاء لم تُدوَّن قط. ويفقدون الثقة عندما لا يعرف. أي تغيير في التصميم يعالج السبب؟**

- A. إضافة رسوم متحركة (animations) أكثر أثناء توليد المسودة، كي يبدو الانتظار أقصر ويبدو المنتج أكثر كفاءة
- B. ضبط التوقعات من البداية (set expectations): إظهار ما يستطيع المساعد رؤيته وما لا يستطيعه، مثل «مسودات من الملف الائتماني والقوائم المالية فقط»
- C. إخفاء حدود المساعد (limitations) كي لا ينفر المستخدمون قبل أن يجرّبوه بأنفسهم
- D. جعل نبرة المساعد أكثر ثقة (confident tone) كي يشعر المديرون بأنهم يستطيعون الاعتماد على ما يكتبه

<details><summary>الإجابة</summary>

**B.** تبدأ إرشادات مايكروسوفت للتفاعل بين الإنسان والذكاء الاصطناعي (Microsoft's Guidelines for Human-AI Interaction) بتوضيح ما يستطيع النظام فعله ومدى جودة فعله له. والتوقعات غير المتطابقة (Mismatched expectations) مشكلة تصميم، والحل هو ضبطها قبل أن يكوّن المستخدمون توقعاتهم الخاصة. والخيار D مغرٍ لأن النص الواثق يبدو جديرًا بالثقة (trustworthy)، لكن الثقة غير المستحَقة (confidence that is not earned) تجعل الإخفاق الحتمي أسوأ. *(Design · 4.2)*

</details>

**18. يسيء نجم أسيست (Najm Assist) أحيانًا فهم المعاملة التي يسأل عنها العميل. ما أهم نمط تعافٍ (recovery pattern) يجب تصميمه؟**

- A. أن يُطلب من العميل تقييم الإجابة من 1 إلى 5 (rating)، كي يجد الفريق نقاط الضعف لاحقًا ويعالجها
- B. الاعتذار وإنهاء المحادثة (end the chat)، كي يبدأ العميل من جديد بطلب أوضح وأكثر دقة في المرة القادمة
- C. تسهيل التصحيح: إظهار المعاملة التي فهمها المساعد (correction)، وتمكين العميل من اختيار الصحيحة بنقرة
- D. إعادة المحاولة بنفس الإجابة بصياغة مختلفة (retry)، تحسبًا لأن العميل لم يفهمها ببساطة من المرة الأولى

<details><summary>الإجابة</summary>

**C.** سيخطئ الذكاء الاصطناعي أحيانًا، لذا يجعل التصميم الجيد الأخطاء مرئية ورخيصة الإصلاح (visible and cheap to fix). وبيان تفسير المساعد (assistant's interpretation) ودعم التصحيح الفعّال (efficient correction) من الإرشادات الأساسية للتفاعل بين الإنسان والذكاء الاصطناعي (human-AI interaction guidelines). والخيار A مغرٍ لأنه يجمع التغذية الراجعة (feedback)، لكن التقييم لا يساعد العميل العالق الآن. *(Design · 4.2)*

</details>

**19. يتطوّر نجم أسيست ليصبح وكيلًا (agent). سيتمكن العملاء من قول «جمِّد بطاقتي (freeze my card)» أو «اعترض على هذه المعاملة (dispute this transaction)». ما أهم قاعدة تصميم لهذه الإجراءات؟**

- A. قبل أي إجراء مؤثر، عرض ما سيحدث وطلب تأكيد صريح (explicit confirmation)، وتسهيل التراجع عن الإجراءات القابلة للعكس
- B. تنفيذ الإجراء فورًا (immediately)، لأن السرعة هي جوهر الوكيل والعملاء يتوقعون منه أن يتصرف دون تأخير أو أسئلة، حتى لو كان أثر الإجراء كبيرًا
- C. السماح بالأسئلة فقط ومنع الإجراءات تمامًا (no actions)، كي تبقى مخاطر الوكيل صفرًا طوال مدة التشغيل كلها
- D. أن يؤكد العميل كل رسالة (every message) حتى الأسئلة البسيطة، كي لا يحدث شيء على الحساب دون أن يُرى

<details><summary>الإجابة</summary>

**A.** عندما يتصرف وكيل (agent) في حساب عميل، يجب أن يبقى العميل متحكمًا (stay in control): معاينة واضحة (clear preview)، وتأكيد للإجراءات ذات العواقب، وتراجع (undo) حيثما أمكن. وتجميد البطاقة أمر حرج زمنيًا (time-critical) أيضًا، لذا يجب أن يكون التأكيد سريعًا، لا عائقًا. والخيار C مغرٍ لكنه يتخلى عن قيمة الوكيل كليًا. أما D فيضيف احتكاكًا (friction) كبيرًا لدرجة أن الناس سيتوقفون عن قراءة الرسائل. *(Design · 4.3)*

</details>

**20. يسأل مديرو العلاقات كيف يمكنهم الوثوق برقم في مذكرة ائتمان مصاغة (drafted credit memo). ما أنفع تفسير (explanation) يُصمَّم لهذا المنتج؟**

- A. وصف تقني (technical description) لكيفية عمل النموذج، مع رسم توضيحي، موجّه للمديرين الذين يعتمدون على المذكرات
- B. نسبة ثقة مئوية (confidence percentage) تظهر بجانب المذكرة كلها، ليعرف المراجعون إلى أي حد يمكنهم الاعتماد عليها
- C. عبارة على الشاشة بأن النموذج عالي الدقة (highly accurate)، مدعومة بنتائجه على المقاييس
- D. استشهاد (citation) بجانب كل رقم وادعاء رئيسي، يرتبط بالموضع الدقيق في المستند المصدر الذي جاء منه

<details><summary>الإجابة</summary>

**D.** التفسيرات الجيدة تساعد المستخدم على أن يقرر هل يعتمد على المخرَج (rely on an output). وفي مستند مبني من مصادر، يكون أنفع تفسير رابطًا قابلًا للتتبّع (traceable link) من كل ادعاء إلى مصدره، كي يتحقق منه المراجع في ثوانٍ. والخيار B مغرٍ لأنه يبدو دقيقًا، لكن نتيجة واحدة للمذكرة كلها لا تخبر المراجع بالجزء الذي يجب التحقق منه، ودرجات ثقة النموذج (model confidence scores) كثيرًا ما تكون سيئة المعايرة (poorly calibrated). *(Design · 4.2)*

</details>

**21. بعد ثلاثة أشهر من الإطلاق، تلاحظ دانة أن مديري العلاقات يوافقون الآن على 98% من مسودات المساعد (Copilot drafts) دون أي تعديل، بما فيها مسودات تعرف أنها تحتوي أخطاء. ما أفضل استجابة تصميمية؟**

- A. لا شيء: القبول العالي دليل على أن المسودات جيدة وأن المديرين يثقون بالمنتج وأنه يعمل كما قُصد (acceptance)
- B. إزالة المساعد من مديري العلاقات، لأن المستخدمين لا يُؤتمنون على مراجعة مسوداته بعناية (remove)
- C. مواجهة تحيّز الأتمتة (automation bias): تمييز الأقسام غير الموثَّقة، وإلزام المراجع بتأكيد الأرقام الرئيسية، وتتبع التعديلات
- D. إضافة إخلاء مسؤولية (disclaimer) في أسفل كل مذكرة بأن المسودة أُنتجت بالذكاء الاصطناعي ويجب فحصها قبل توقيعها من أي مراجع

<details><summary>الإجابة</summary>

**C.** عندما يختم الناس على مخرجات الذكاء الاصطناعي دون تمحيص (rubber-stamp AI output)، تتوقف المراجعة البشرية (human review) التي يعتمد عليها المنتج عن العمل. هذا هو انحياز الأتمتة (automation bias). والإجابة التصميمية هي احتكاك موضوع في مكانه الصحيح (well-placed friction) على الأجزاء المهمة، لا احتكاك في كل مكان. والخيار A هو الخيار المضلِّل المغري: فمعدل القبول (acceptance rate) وحده لا يميّز المسودات الجيدة من غير المراجَعة، وهنا يوجد دليل على أن الأخطاء تمر. أما D فإخلاء مسؤولية، يتوقف الناس عن قراءته. *(Design · 4.1)*

</details>

**22. سأل عميل نجم أسيست السؤال نفسه عن تحويل محجوب (blocked transfer) ثلاث مرات وبدأ يشعر بالإحباط. ما الذي يجب أن يفعله التصميم؟**

- A. الاستمرار في تجربة صياغات جديدة للإجابة حتى يرضى العميل أو يتوقف عن السؤال، مع استخدام المصادر نفسها (wordings)
- B. عرض التحويل إلى موظف بشري (hand-over) ينقل المحادثة وما جُرّب فيها، كي لا يكرر أحد كلامه
- C. عرض رابط لصفحة الأسئلة الشائعة (FAQ) يقرأ فيها العميل السياسة الكاملة للتحويلات المحجوزة ومدفوعات البطاقات
- D. إنهاء المحادثة بلباقة وطلب أن يتصل العميل بمركز الاتصال (contact centre) خلال ساعات عمله المعتادة مع الرقم

<details><summary>الإجابة</summary>

**B.** يحتاج المنتج الحواري (conversational product) إلى مسار واضح إلى شخص (clear path to a person)، يُطلَق بإشارات (signals) مثل التكرار أو الإحباط، ويجب أن يحمل التسليم السياق (hand-over must carry context). والخيار C مغرٍ لأنه رخيص، لكن العميل أظهر بالفعل أن إجابات الخدمة الذاتية (self-service answers) لا تحل مشكلته. أما D فيتخلى عن السياق ويجعل العميل يبدأ من جديد. *(Design · 4.3)*

</details>

**23. في قضية *Moffatt v. Air Canada* (2024)، حمّلت هيئة قضائية (tribunal) شركة الطيران المسؤولية عمّا قاله روبوت المحادثة (chatbot) في موقعها لعميل عن سياسة الأسعار (fare policy). ما الدرس التصميمي الرئيسي (main design lesson) لنجم أسيست؟**

- A. يجب أن تأتي الإجابات عن السياسات والرسوم والالتزامات من مصادر البنك المعتمدة (approved sources)، وألا يخترع المساعد شروطًا
- B. يجب تجنّب روبوتات المحادثة الموجّهة للعملاء في القطاعات الخاضعة للتنظيم، فقد تؤدي إجابة خاطئة إلى حكم أو غرامة (regulated industries)
- C. إخلاء المسؤولية بأن روبوت المحادثة قد يخطئ يزيل مسؤولية الشركة عمّا يقوله لعملائها (disclaimer)
- D. أن يحيل روبوت المحادثة كل سؤال إلى الموقع الإلكتروني (website) بدل الإجابة عنه، كي لا يُستخدم إلا النص المنشور

<details><summary>الإجابة</summary>

**A.** تُظهر القضية أن العملاء قد يعاملون ما يقوله المساعد على أنه كلام الشركة (the company speaking). وفي إجابات السياسات والرسوم، يجب أن يربط التصميم الردود بالمحتوى المعتمد (approved content) وأن يعتذر أو يصعّد (decline or escalate) حيث لا يستطيع ذلك. والخيار C مغرٍ، لكن القضية تُقرأ على نطاق واسع بوصفها تحذيرًا من أن الشركة لا تستطيع ببساطة التبرؤ مما يقوله روبوت المحادثة الخاص بها (disown what its own chatbot says). والخيار B رد فعل مبالغ فيه (overreacts)؛ أما D فيتخلى عن قيمة المنتج. *(Design · 4.3)*

</details>

### البناء (Build)

**24. قبل بناء نموذج ذكاء اصطناعي، يريد فيصل أن يختبر هل سيستخدم أصحاب الشركات الصغيرة (SME owners) «عرض سعر فوري (instant quote)» لتمويل الفواتير. ما أرخص اختبار موثوق (cheapest credible test)؟**

- A. بناء النموذج وإطلاقه لـ 5% من العملاء (release)، ثم مراقبة عدد من يطلبون عرض سعر خلال أسبوع
- B. إجراء استبيان (survey) لأصحاب الشركات الصغيرة يسألهم إن كانوا يرغبون في عروض أسعار فورية لتمويل الفواتير
- C. اختبار ساحر أوز (Wizard of Oz): يستخدم العملاء شاشة عرض سعر بينما ينتج موظفون مدرَّبون العروض خلفها
- D. سؤال دانا عن مدى الدقة الممكنة للنموذج (accuracy)، ثم القرار بالمتابعة بناءً على تقديرها لهذه الدقة

<details><summary>الإجابة</summary>

**C.** يتيح لك النموذج الأولي بأسلوب ساحر أوز (Wizard of Oz prototype) مراقبة السلوك الحقيقي (real behaviour) عبر تجربة تبدو حقيقية (real-feeling experience) قبل أن تنفق على النموذج، فتتعلم عن القيمة أولًا (learn about value first). والخيار B مغرٍ لأنه رخيص أيضًا، لكنه يقيس النية المعلنة (stated intent)، التي كثيرًا ما تختلف عمّا يفعله الناس. أما A فينفق أكثر من غيره قبل تعلّم أي شيء عن الطلب (demand). *(Build · 5.2)*

</details>

**25. يغيّر مهندس جملة واحدة في موجّه النظام (system prompt) لمساعد مذكرات الائتمان (Credit Memo Copilot) لإصلاح مشكلة تنسيق (formatting issue) وينشرها (deploys) يوم جمعة. ويوم الاثنين، تخلو المسودات من قسم المخاطر (risk section). أي ممارسة كانت ستمنع ذلك؟**

- A. معاملة الموجِّهات كشيفرة منتج (product code): ترقيمها بإصدارات، ومراجعة التغييرات، وتشغيل التقييمات قبل أي إطلاق
- B. السماح لمدير المنتج وحده بتعديل الموجِّهات (prompts)، كي يجري كل تغيير شخص يعرف المنتج ومستخدميه جيدًا
- C. عدم تغيير الموجّه إطلاقًا بعد الإطلاق (never change)، كي يبقى السلوك كما كان حين اختُبر قبل الإصدار الأول
- D. كتابة موجِّهات أطول (longer prompts) كي يقل أثر تغيير جملة واحدة في سلوك النظام وإجاباته كلها مع الوقت ومع تعدد المراجعين

<details><summary>الإجابة</summary>

**A.** الموجّهات والسياق وأوصاف الأدوات (Prompts, context and tool descriptions) جزء من سطح المنتج (product surface). فتغييرات الصياغة الصغيرة قد تحرّك السلوك، لذا تحتاج إلى التحكم في الإصدارات (version control) والمراجعة واختبار الانحدار (regression testing) نفسها التي تحتاجها الشيفرة. والخيار B مغرٍ لأنه يضيف مالكًا (owner)، لكن شخصًا واحدًا يراجع بالعين لا يستطيع رؤية انحدار (regression) عبر مئات الحالات؛ أما حزمة التقييمات فتستطيع. والخيار C يجمّد المنتج. *(Build · 5.3)*

</details>

**26. في أول جلسة تخطيط لدورة العمل (sprint planning session) للتمويل الفوري للشركات الصغيرة (SME Instant Finance)، ما أثمن ما يمكن أن يقدمه فيصل لفريق علم البيانات (data science team) الذي تقوده دانة؟**

- A. قرار بشأن الخوارزمية (algorithm) التي تُستخدم، كي يبدأ علماء البيانات بناء النموذج مباشرة دون انتظار أي نقاش مع الإدارة أو المنتج
- B. مطالبة بأن تبلغ دقة النموذج 99% في كل الحالات (99% accurate)، كي يكون للفريق هدف جودة واضح وطموح كل أسبوع
- C. موعد تسليم ثابت (fixed date) للنموذج النهائي، كي يخطَّط للإطلاق والتسويق على أساسه منذ الآن
- D. سياق العمل (business context): القرار الذي يدعمه النموذج، وكلفة كل نوع من الخطأ، وحالات حقيقية، وقيود كزمن الاستجابة

<details><summary>الإجابة</summary>

**D.** مدير المنتج الذي يعمل مع مهندسي التعلّم الآلي والذكاء الاصطناعي (ML and AI engineers) يضيف أكثر ما يضيف بتعريف المشكلة والرهانات والقيود (the problem, the stakes and the constraints)، ثم ترك الخبراء يختارون الطريقة (method). والخيار B مغرٍ لأنه يبدو معيار جودة واضحًا (clear quality bar)، لكن رقم دقة واحدًا (single accuracy number) لا صلة له بتكاليف الأخطاء أو بخط أساس (baseline) ليس ذا معنى ولا قابلًا للتحقيق عند الطلب. أما A فقرار علماء البيانات (the data scientists' call). *(Build · 5.2)*

</details>

**27. سيحصل وكيل (agent) نجم أسيست على أدوات (tools) لقراءة الأرصدة وتجميد البطاقات وتقديم الاعتراضات. يقترح طارق ربطه عبر حساب تكامل واحد (one integration account) بصلاحية كاملة على واجهة برمجة النظام المصرفي الأساسي (core banking API) «لإبقاء الأمور بسيطة». ما الذي يجب أن يدفع فيصل نحوه؟**

- A. وصول كامل مع تسجيل إضافي (extra logging) كي يراجع فريقا الأمن والتدقيق كل استدعاء يجريه الوكيل لاحقًا بدقة وبشكل منتظم
- B. أقل الصلاحيات (least privilege): أدوات منفصلة ضيقة لكل إجراء، تعمل على حسابات العميل المسجَّل فقط، مع حدود على كل منها
- C. إزالة كل الأدوات إلى أن يصبح النموذج مثاليًا، وأن يجيب الوكيل عن الأسئلة فقط ولا يتصرف في الحسابات (tools)
- D. ترك النموذج يختار استدعاءات الواجهة (API calls) وقت التشغيل بناءً على طلب العميل وحكمه الخاص دون قيود

<details><summary>الإجابة</summary>

**B.** تحدد الأدوات (Tools) ما يستطيع الوكيل فعله في العالم، لذا فهي سطح منتج (product surface) وحدّ أمني (security boundary). والأدوات الضيقة والموصوفة جيدًا تحدّ من الضرر الناتج عن خطأ النموذج أو عن حقن الموجّه (prompt injection). ومعايير مثل بروتوكول سياق النموذج (Model Context Protocol) تسهّل ربط الأدوات، لكنها لا تقرر ما هي الصلاحية المناسبة (what access is appropriate). والخيار A مغرٍ، لكن التسجيل (logging) يسجّل الضرر بدلًا من منعه. *(Build · 5.3)*

</details>

**28. لجعل مساعد مذكرات الائتمان «يعرف كل شيء»، يقترح مهندس وضع دليل سياسة الائتمان (credit policy manual) كاملًا، بصفحاته الستمئة، في كل طلب. ما المشكلة الرئيسية؟**

- A. يصبح كل طلب أبطأ وأغلى، وقد تفوّت النماذج تفاصيل مدفونة في سياق طويل جدًا (long context)؛ والأفضل عادةً استرجاع الأقسام المناسبة
- B. هذا مستحيل، لأن أي نموذج لا يقبل أكثر من بضع صفحات من النص في طلب واحد (impossible)
- C. يجعل النموذج ينسى جزءًا من تدريبه (training)، فتسوء معرفته العامة
- D. لا مشكلة، ما دامت نافذة السياق (context window) في النموذج كبيرة بما يكفي لاستيعاب الدليل

<details><summary>الإجابة</summary>

**A.** السياق ليس مجانيًا (Context is not free). فالتكلفة وزمن الاستجابة (Cost and latency) يزدادان مع الرموز (tokens) التي ترسلها في كل طلب، وقد تنخفض جودة الإجابة (answer quality) عندما تكون التفصيلة المهمة جزءًا صغيرًا من مُدخل طويل جدًا. والخيار D هو الخيار المضلِّل المغري: فالاتساع في النافذة لا يعني أنه تصميم جيد. أما B فخاطئ؛ فنوافذ السياق تتفاوت بحسب النموذج وقد كبرت، وهذا بالضبط سبب أن السؤال هو المفاضلة (trade-off)، لا حدًّا صارمًا (hard limit). *(Build · 1.2)*

</details>

**29. يضبط طارق درجة حرارة (temperature) مساعد مذكرات الائتمان على قيمة منخفضة جدًا عندما يستخرج الأرقام من القوائم المالية (financial statements). ما الذي يحققه ذلك؟**

- A. يمنع النموذج من الهلوسة (hallucination)، لأنه لم يعد لديه مجال لاختلاق الأشياء عند الإجابة عن أي سؤال
- B. يخفض تكلفة كل طلب (cost per request)، لأن العشوائية الأقل تحتاج حسابًا أقل لكل رمز ينتجه النموذج
- C. يجعل النموذج أكثر إبداعًا في ملخصاته (creative)، مما يجعل المذكرات تُقرأ بصورة أطبع للمديرين
- D. يجعل المخرجات أكثر اتساقًا من تشغيل لآخر (consistent)، وهذا يناسب الاستخراج، لكنه لا يضمن صحتها

<details><summary>الإجابة</summary>

**D.** تتحكم درجة الحرارة (Temperature) في مقدار العشوائية الداخلة في اختيار كل رمز تالٍ (next token). ودرجة الحرارة المنخفضة تجعل المخرجات أكثر قابلية للتكرار (repeatable)، وهذا يناسب مهام الاستخراج، لكن النموذج قد يكون مخطئًا باتساق (consistently wrong). والخيار A هو الخيار المضلِّل المغري: فهو اعتقاد شائع (common belief)، لكن التحقق من المصدر (checking against the source) يظل مطلوبًا. أما B فخاطئ؛ فدرجة الحرارة لا تغيّر سعر الطلب. *(Build · 1.2)*

</details>

**30. يريد فيصل أن يتحسّن مساعد مذكرات الائتمان مع الوقت. أي إشارة (signal) يجب أن يصمم المنتج لالتقاطها أولًا؟**

- A. عدد مرات فتح المساعد يوميًا بواسطة مديري العلاقات (daily opens)، بوصفه مؤشرًا على مدى اعتماد الفريق عليه
- B. استبيان منبثق بعد كل مذكرة (pop-up survey) يسأل المدير عن مدى فائدة المسودة وما الذي ينبغي تغييره فيها
- C. التعديلات التي يجريها مديرو العلاقات على كل مسودة قبل توقيعها (edits)، مرتبطة بالقسم وبيانات المصدر
- D. طول كل مسودة (draft length)، بوصفه مؤشرًا على حجم عمل الكتابة الذي يوفره المساعد لكل مدير

<details><summary>الإجابة</summary>

**C.** المنتج المتعلّم (learning product) يلتقط التغذية الراجعة (feedback) في المسار الطبيعي للعمل (normal course of work). والتعديلات التي يجريها الخبراء غنية ومحددة ومجانية الجمع (rich, specific and free to collect). فهي تُظهر ما كان خاطئًا وكيف يبدو الصواب، وتغذي تحليل الأخطاء (error analysis) والتقييمات المستقبلية (future evals). والخيار B مغرٍ لأنه يسأل مباشرة، لكن الاستبيانات بعد كل مهمة تُتجاهَل أو يُجاب عنها بلا اكتراث. أما A فيقيس الاستخدام (usage)، لا الجودة. *(Build · 3.2)*

</details>

### التقييم (Evaluate)

**31. تبني دانة مجموعة مرجعية (golden set) لتقييم مساعد مذكرات الائتمان (Credit Memo Copilot). أي نهج هو الأفضل؟**

- A. استخدام أحدث 200 مذكرة أيًا كان محتواها (recent memos)، لأنها تعكس طريقة عمل البنك اليوم وسلوك عملائه الحاليين ومنتجاتهم
- B. اختيار مجموعة ثابتة من الحالات الحقيقية (real cases): التوزيع المعتاد مع الحالات الصعبة، وإجابات يفحصها كبار موظفي الائتمان
- C. أن يولّد النموذج حالات الاختبار والإجابات المتوقعة، وهذا سريع ويتسع لآلاف الحالات الجديدة (generated tests)
- D. استخدام أصعب الحالات فقط، كي تكون الدرجة متحفظة ويعني النجاح شيئًا حقيقيًا للفريق كله (hardest cases)

<details><summary>الإجابة</summary>

**B.** يجب أن تمثّل المجموعة المرجعية التوزيع الحقيقي (real distribution)، وتتضمن الحالات الطرفية (edge cases) المهمة، وتحتوي إجابات مرجعية موثوقة (trusted reference answers)، وتبقى ثابتة كي تكون النتائج قابلة للمقارنة عبر الزمن (comparable over time). والخيار A مغرٍ لأنه سهل وحديث، لكنه قد يفوّت حالات نادرة عالية المخاطر (rare, high-stakes cases) وليست فيه إجابات مرجعية متحقَّق منها. أما C فيخاطر بأن يقيّم النموذج نقاطه العمياء (blind spots) بنفسه. وD يعطي نتيجة لا تعكس الاستخدام الطبيعي (normal use). *(Evaluate · 6.1)*

</details>

**32. لدى نموذج التنبيهات الذكية (Smart Alerts) الجديد دقة (precision) قدرها 0.9 واستدعاء (recall) قدره 0.4 في الاحتيال. ماذا يعني ذلك؟**

- A. يلتقط 90% من الاحتيال، لكن 40% من تنبيهاته إنذارات كاذبة تُرسل إلى عملاء حقيقيين لم يفعلوا شيئًا (false alarms)
- B. دقته الإجمالية 90%، ويصنّف 40% من حالات الاحتيال الأندر تصنيفًا صحيحًا في كل دفعة (overall accuracy)
- C. سيتلقى 40% من العملاء تنبيهًا، وتسعة من كل عشرة تنبيهات منها مبرَّرة تمامًا (alerts)
- D. حين يطلق تنبيهًا فهو غالبًا محق، لكنه يفوّت نحو 60% من الاحتيال (recall)

<details><summary>الإجابة</summary>

**D.** الدقة (Precision) هي حصة التنبيهات التي تكون احتيالًا حقيقيًا (0.9). والاستدعاء (Recall) هو حصة الاحتيال الحقيقي التي تحصل على تنبيه (0.4)، لذا يمر نحو 60% من الاحتيال دون تعليم (unflagged). والخيار A هو الخلط الكلاسيكي بين الاثنين (classic mix-up). أما B فيخلط بين الدقة (precision) والدقة الإجمالية (accuracy). وقبول هذه المفاضلة (trade-off) من عدمه يعتمد على تكاليف الأخطاء (error costs) المعرَّفة للمنتج. *(Evaluate · 6.1)*

</details>

**33. يحصل المساعد (Copilot) على 81% في المجموعة المرجعية، دون معيار الإطلاق (launch bar) البالغ 90%. يقترح فيصل الانتقال إلى نموذج أكبر (bigger model). ما الذي يجب أن يفعله الفريق أولًا؟**

- A. تحليل الأخطاء (error analysis): قراءة الحالات الفاشلة وتجميعها حسب السبب وإصلاح أكبر مجموعة قبل تغيير النموذج
- B. التحويل إلى النموذج الأكبر وإعادة تشغيل التقييمات، لأن النموذج الأقوى يحقق درجة أعلى عادةً في كل مهمة (bigger model)
- C. خفض حد الإطلاق إلى 80% كي يُطلق المساعد الآن ويتحسن بينما يستخدمه مديرو العلاقات الحقيقيون (launch bar)
- D. إضافة حالات أكثر إلى المجموعة الذهبية (golden set) حتى ترتفع الدرجة فوق حد الإطلاق البالغ 90% الذي وضعه الفريق

<details><summary>الإجابة</summary>

**A.** النتيجة الواحدة (single score) لا تقول ما الخطأ. وقراءة الإخفاقات وتصنيفها (categorising failures) كثيرًا ما تكشف أسبابًا لن يصلحها نموذج أكبر، مثل استرجاع (retrieval) يفوّت مستندًا، أو تعليمة في الموجّه (prompt instruction) يجري تجاهلها، أو مشكلة في تنسيق البيانات (data format problem). والخيار B مغرٍ وأحيانًا يكون صحيحًا، لكنك دون معرفة الأسباب تنفق المال على تخمين (a guess). أما C وD فيحرّكان الهدف (move the target) بدلًا من تحسين المنتج. *(Evaluate · 6.1)*

</details>

**34. تستخدم دانة نموذجًا لغويًا كبيرًا حَكَمًا (LLM as a judge) للمقارنة بين نسختين من مسودة مذكرة. وهو يفضّل المسودة المعروضة أولًا أكثر مما تفسّره الصدفة (chance). ماذا يجب أن تفعل؟**

- A. عرض النسخة الجديدة أولًا دائمًا (new version first)، كي تجري كل مقارنة في الظروف والترتيب نفسيهما
- B. استبدال الحَكَم بنموذج أكبر والتوقف عن الفحص (larger model)، لأن النماذج الأكبر تحكم بإنصاف أكثر وبتحيز أقل
- C. إجراء كل مقارنة مرتين مع تبديل الترتيب (swap the order)، واحتساب الأحكام المتسقة فقط أو معاملة التعارض كتعادل
- D. التوقف عن استخدام النموذج اللغوي حَكَمًا (LLM-as-judge) كليًا والاعتماد على مراجعين بشريين في كل مقارنة من الآن

<details><summary>الإجابة</summary>

**C.** انحياز الموضع (Position bias) أحد الانحيازات المعروفة للحكّام من النماذج اللغوية (known biases of LLM judges)، إلى جانب انحياز الإسهاب (verbosity bias) والتفضيل الذاتي (self-preference)، كما وُصف في أعمال مثل Zheng et al. (2023). وتبديل الترتيب يضبط هذا الانحياز (controls for it). والخيار D مغرٍ بوصفه خيارًا آمنًا، لكنه يرمي أداة قابلة للتوسّع (scalable tool) في حين أن للانحياز إصلاحًا معياريًا (standard fix). أما B فيفترض دون تحقق أن النموذج الأكبر خالٍ من الانحياز. *(Evaluate · 6.2)*

</details>

**35. قبل الوثوق بحَكَم من نموذج لغوي (LLM judge) لتقييم آلاف إجابات نجم أسيست (Najm Assist) كل أسبوع، ما أهم خطوة؟**

- A. كتابة موجّه حَكَم مفصَّل جدًا يوضح كل معيار ويقدم أمثلة محلولة عن الإجابات الجيدة والسيئة يتبعها النموذج (judge prompt)
- B. مقارنة درجات الحَكَم بتقييمات خبراء بشريين على عيّنة، وقياس الاتفاق، والتحسين حتى يصبح مقبولًا (human ratings)
- C. استخدام النموذج نفسه الذي يولّد الإجابات حَكَمًا، كي يفهم الحَكَم كيف أُنتجت (same model)
- D. تشغيل الحَكَم على عيّنة صغيرة والتأكد من أن الدرجات تبدو معقولة للفريق وللمراجعين (small sample)

<details><summary>الإجابة</summary>

**B.** الحَكَم من النماذج اللغوية (LLM judge) هو نفسه نموذج يجب تقييمه. ومعايرته مقابل الحكم البشري (calibrating it against human judgement)، باستخدام معايير تقييم واضحة (clear rubrics) وقياس الاتفاق (measuring agreement)، تخبرك هل لدرجاته أي معنى. والخيار A يساعد لكنه لا يثبت شيئًا وحده. والخيار D هو الخيار المضلِّل المغري: فعبارة «تبدو معقولة (looks reasonable)» ليست مقياسًا. أما C فيخاطر بانحياز التفضيل الذاتي (self-preference bias). *(Evaluate · 6.2)*

</details>

**36. قبل أن يتمكن نجم أسيست من اتخاذ إجراءات نيابةً عن العملاء، تطلب ليلى اختبار الفريق الأحمر (red-teaming). أي تمرين هو الأنسب؟**

- A. استبيان لرضا العملاء عن النسخة التجريبية (beta)، يجمع التقييمات والتعليقات من مستخدمي التجربة
- B. تشغيل المجموعة الذهبية مرة ثانية (golden set) للتأكد من ثبات الدرجات من تشغيل لآخر
- C. اختبار حِمل (load test) للتأكد من أن النظام يتحمل ذروة الحركة دون بطء أو تعطل
- D. محاولة منظَّمة من مختبِرين مكلَّفين لجعل المساعد يخرق قواعده (red-teaming): حقن التعليمات، وإساءة الاستخدام خارج الموضوع، وتنفيذ إجراءات على حساب خاطئ

<details><summary>الإجابة</summary>

**D.** اختبار الفريق الأحمر (Red-teaming) اختبار عدائي متعمَّد (deliberate adversarial testing) للعثور على إخفاقات لن يُظهرها التقييم العادي. وروبوت المحادثة لدى وكيل شيفروليه (Chevrolet dealer chatbot) الذي أُقنع بـ«الموافقة» على بيع سيارة بدولار واحد ($1) (Dec 2023) يُظهر كيف يبدو التلاعب غير المختبَر (untested manipulation) على الملأ. والخيار B مغرٍ لأنه تقييم، لكن المجموعة المرجعية تتحقق من السلوك المتوقع (expected behaviour) في الحالات العادية، لا مما يستطيع الخصم (adversary) أن يجعل النظام يفعله. *(Evaluate · 6.2)*

</details>

**37. في اختبار A/B (A/B test) لتصميم جديد لنجم أسيست، كانت الخطة تقسيمًا 50/50 (50/50 split)، لكن مجموعة المعالجة (treatment group) فيها عدد مستخدمين أقل بشكل ملحوظ من مجموعة الضبط (control). والمعالجة تتفوق على المقياس الرئيسي (main metric). ماذا يجب أن يفعل الفريق؟**

- A. التوقف والتحقيق في الاختلال قبل قراءة النتائج: عدم تطابق نسبة العيّنات (sample ratio mismatch) يعني غالبًا خللًا في التوزيع أو التسجيل
- B. شحن المعالجة (ship the treatment) لأنها تتفوق في المقياس الرئيسي والعيّنة ما زالت كبيرة
- C. إعادة وزن المجموعات إحصائيًا والإبلاغ عن النتيجة، مع ذكر الاختلال في التقرير (re-weight)
- D. تمديد الاختبار حتى تتساوى المجموعتان في الحجم ثم قراءة النتائج كما خُطط (extend the test)

<details><summary>الإجابة</summary>

**A.** يعامل كوهافي وتانغ وشو (Kohavi, Tang and Xu) (*Trustworthy Online Controlled Experiments*, 2020) عدم تطابق نسبة العينة بوصفه تحذيرًا من أن التجربة نفسها غير جديرة بالثقة (not trustworthy)، مثلًا لأن بعض مستخدمي المعالجة تعطّل لديهم التطبيق فخرجوا (crashed out) أو لم يُسجَّلوا. والخيار B هو الخيار المضلِّل المغري، لكن الفوز في اختبار معطّل (broken test) ليس دليلًا. أما C وD فلا يعالجان السبب الأساسي (underlying cause). *(Evaluate · 6.3)*

</details>

**38. يُحسّن اختبارٌ لنموذج جديد للتنبيهات الذكية (Smart Alerts) المقياسَ الرئيسي (main metric)، وهو الاحتيال المكتشف لكل ألف عميل (fraud caught per thousand customers). لكن المقياس الوقائي (guardrail metric) المتفق عليه مسبقًا، وهو شكاوى العملاء من البطاقات المحجوبة (complaints about blocked cards)، ارتفع متجاوزًا حدّه. ما القرار الصحيح؟**

- A. الشحن، لأن المقياس الرئيسي تحسن وتحقق هدف الاختبار المتفق عليه مسبقًا بفضل النموذج الجديد وحده (ship)
- B. الشحن لنصف العملاء كحل وسط (compromise)، ومراقبة ما إذا كانت الشكاوى تواصل الارتفاع قبل المضي أبعد في الإطلاق
- C. عدم الشحن كما هو: تجاوز حاجز الحماية (guardrail) يعني ضررًا اتفق الفريق على ألا يقبله؛ يجب التحقيق
- D. استبدال مقياس الحماية بمقياس لم يتحرك، لأن الشكاوى من البطاقات المحجوبة متقلبة بطبيعتها وغير موثوقة (noisy)

<details><summary>الإجابة</summary>

**C.** توجد المقاييس الوقائية (Guardrail metrics) كي تمنع فوزًا في المقياس الرئيسي من إخفاء ضرر غير مقبول (unacceptable harm) في مكان آخر. والاتفاق عليها مسبقًا (in advance) هو ما يجعلها ملزِمة (binding). والخيار A مغرٍ لأن الهدف الرئيسي تحسّن، لكنه يتجاهل القاعدة التي وضعها الفريق. أما D فهو تحريك المرمى (moving the goalposts) بعد ظهور النتيجة. *(Evaluate · 6.3)*

</details>

### الإطلاق (Launch)

**39. يخطط فيصل لإطلاق التمويل الفوري للشركات الصغيرة (SME Instant Finance) للتجار الأفراد (sole traders) في الاتحاد الأوروبي (EU) الشهر المقبل. وقد اجتاز النموذج تقييماته (passed its evals). أي خطوة هي الأوضح غيابًا (most clearly missing)؟**

- A. حملة تسويقية (marketing campaign) للإعلان عن تمويل الفواتير الفوري للشركات الصغيرة بين أصحاب الأعمال الفردية في الاتحاد الأوروبي
- B. جولة ثانية من التقييم دون اتصال (offline evaluation) للتأكد من أن النموذج يصمد قبل الإطلاق
- C. خطة لقياس التبنّي (adoption) كي يرى الفريق كم من أصحاب الأعمال الفردية يستخدمون المنتج
- D. بوابة الحوكمة (governance gate): يؤكد فريق ليلى فئة المخاطر والضوابط، لأن قرارات الائتمان المتعلقة بالأفراد قد تكون عالية المخاطر بموجب قانون الاتحاد الأوروبي للذكاء الاصطناعي

<details><summary>الإجابة</summary>

**D.** تشمل جاهزية الإطلاق (Launch readiness) الحوكمة (governance)، لا جودة النموذج فقط. فتقييم الجدارة الائتمانية للأشخاص الطبيعيين (Creditworthiness assessment of natural persons) مُدرج بوصفه عالي المخاطر بموجب قانون الذكاء الاصطناعي الأوروبي، والتاجر الفرد شخص طبيعي (natural person)، لذا يجب حسم التصنيف (classification) والتزاماته قبل الإطلاق. والخيار B مغرٍ لأن مزيدًا من الاختبار يبدو آمنًا، لكن التقييمات اجتيزت؛ والقطعة الناقصة هي الموافقة والضوابط (approval and controls). والتفاصيل مكانها دورة *AI Governance: Zero to Hero*. *(Launch · 7.1)*

</details>

**40. في يوم إطلاق نجم أسيست (Najm Assist)، أي استعداد تنساه فرق المنتج في أغلب الأحيان؟**

- A. البيان الصحفي (press release)، الذي ينبغي الاتفاق عليه مع فريقي الاتصال والشؤون القانونية قبل يوم الإطلاق بوقت كافٍ
- B. جاهزية مركز الاتصال (contact-centre readiness): نصوص للأخطاء الشائعة، وعرض لما قاله المساعد للعميل، ومسار تصعيد
- C. حفل إطلاق للفريق (launch party) للاحتفاء بالإنجاز وشكر كل من عملوا على المساعد طوال العام
- D. شعار جديد (new logo) للمساعد، كي يميزه العملاء عن خدمة الدردشة القديمة والتطبيق

<details><summary>الإجابة</summary>

**B.** عندما يخطئ منتج ذكاء اصطناعي في شيء، يتصل العملاء. ويحتاج الموظفون (Agents) إلى رؤية المحادثة، ومعرفة كيف يصححونها، ومعرفة إلى أين يصعّدون. ودون ذلك، يتحول كل خطأ للذكاء الاصطناعي إلى شكوى بطيئة ومحبطة (slow, frustrating complaint). والخيار A مهم للتوعية (awareness)، لكنه لا يفعل شيئًا للتعامل مع المشكلات التي ستصل. *(Launch · 7.1)*

</details>

**41. بعد تحديث (update)، شتم روبوت المحادثة (customer chatbot) لدى شركة طرود عميلًا وانتقد الشركة، وانتشرت لقطات الشاشة على نطاق واسع (قضية DPD، Jan 2024). أي ضابط إطلاق (launch control) كان سيحدّ من الضرر بشكل أكثر مباشرة؟**

- A. وسيلة مجرَّبة لإيقاف الميزة أو الرجوع إلى وضع آمن (kill switch)، مع اختبارات انحدار قبل كل تحديث
- B. سياسة خصوصية أطول (privacy policy) تشرح كيف يخزّن البنك ومورّدوه محادثات العملاء ويستخدمونها ويحمونها
- C. نموذج أغلى (more expensive model) يُفترض أن يكون أقل ميلًا إلى ردود فظة أو بعيدة عن هوية العلامة عند تحديثه
- D. ميزانية تسويق أكبر (marketing budget) لإصلاح صورة العلامة بعد أن انتشرت لقطات الشاشة على نطاق واسع جدًا

<details><summary>الإجابة</summary>

**A.** يحتاج كل إطلاق للذكاء الاصطناعي إلى مفتاح إيقاف (kill switch) أو بديل احتياطي (fallback) اختبره الفريق فعلًا، وتحتاج التحديثات إلى تقييم انحدار (regression evaluation) قبل الإصدار. ومعًا يقلّص هذان احتمال الإخفاق المحرج (embarrassing failure) ومدة بقائه كليهما. والخيار C مغرٍ لأن نموذجًا أقوى قد يتصرف بشكل أفضل، لكنه لا يُلغي الحاجة إلى اختبار التغييرات أو إلى الإيقاف السريع عندما يسوء شيء ما. *(Launch · 7.1)*

</details>

**42. يريد التسويق إطلاق مساعد مذكرات الائتمان (Credit Memo Copilot) داخليًا بعبارة «مذكرات ائتمان مثالية بنقرة واحدة (Perfect credit memos in one click)». ماذا يجب أن يفعل فيصل؟**

- A. الموافقة عليه، لأن الإطلاقات الداخلية لا تحتاج إلى صياغة دقيقة والمديرون يعرفون المنتج وحدوده جيدًا (approve)
- B. حذف أي ذكر للذكاء الاصطناعي (remove AI)، كي لا يتوقع أحد أن يتصرف المنتج كإنسان أو أن يصيب دائمًا
- C. إعادة كتابته ليعد بما يفعله المنتج بثبات (reliably): «مسودة أولى في دقائق، مع المصادر، لتراجعها وتوقّعها»
- D. إضافة «تجريبي» (beta) إلى الجملة وإبقاء الباقي، كي يعرف المستخدمون أن المنتج قد يتغير قبل الإصدار النهائي

<details><summary>الإجابة</summary>

**C.** يضبط التموضع (Positioning) التوقعات، والتوقعات تقود الثقة. والمبالغة في الادعاء (Overclaiming) تدعو المستخدمين إلى التوقف عن التحقق، وقد يطغى خطأ علني في عرض توضيحي على القصة كلها، كما حدث مع الخطأ الواقعي (factual error) في العرض التوضيحي لإطلاق Bard من Google (Google's Bard launch demo) (Feb 2023). والخيار D مغرٍ، لكن وسم «تجريبي (beta)» لا يصلح وعدًا بالكمال (promise of perfection) ولا الرسالة الناقصة بأن على المستخدم المراجعة. *(Launch · 7.2)*

</details>

**43. تبيع شركة برمجيات محايدة (neutral software company) وكيل دعم بالذكاء الاصطناعي (AI support agent) لشركات أخرى. تكاليفها تزداد مع كل محادثة، وعملاؤها يهتمون بالمشكلات المحلولة (problems solved)، لا بالمقاعد (seats). أي إشارة تسعير (pricing signal) هي الأنسب؟**

- A. رسم ترخيص لمرة واحدة (one-time licence) يُدفع عند الشراء ويغطي كل استخدام لاحق للوكيل، مع التحديثات والدعم
- B. سعر ثابت لكل مقعد موظف (per-seat price)، وهو ما يفهمه العملاء من برمجيات أخرى يشترونها ويستخدمونها كل يوم
- C. مجاني للأبد (free forever) بتمويل من إعلانات تُعرض على المستخدمين النهائيين للعملاء الذين ينشرون الوكيل في قنوات دعمهم
- D. تسعير قائم على النتائج (outcome-based)، مثل سعر لكل محادثة محلولة، بقواعد واضحة لما يُعدّ محلولًا

<details><summary>الإجابة</summary>

**D.** يربط التسعير القائم على النتائج الإيرادَ (revenue) بالقيمة التي يراها العميل وبالتكلفة التي تنمو مع الاستخدام. وقد سعّرت Intercom وكيلها Fin لكل حل (per resolution) منذ عام 2023، وتبعها آخرون بنماذج لكل محادثة (per-conversation models)؛ والأسعار الدقيقة تتغير. والخيار B مغرٍ لأن التسعير بالمقعد (seat pricing) مألوف في البرمجيات، لكنه ينهار عندما يؤدي الذكاء الاصطناعي العمل الذي كانت المقاعد تمثّله، ولا يتتبع التكلفة لكل استخدام (per-use cost). *(Launch · 7.2)*

</details>

**44. بعد ثلاثة أشهر من إطلاق مساعد الموظفين التوليدي (Staff GenAI)، لا تستخدمه أسبوعيًا إلا نسبة صغيرة من الموظفين، ومعظمهم في تقنية المعلومات (IT). ما أفضل خطوة تالية؟**

- A. إرسال بريد لكل الموظفين (all-staff email) يذكّرهم بوجود الأداة وكيفية فتحها وأين يطلبون المساعدة إن احتاجوا
- B. إيجاد سفراء (champions) في كل إدارة، وجمع حالات استخدام ملموسة لمهامهم الفعلية، وتدريب الناس داخل سير عملهم
- C. جعل استخدامها إلزاميًا (mandatory) لكل الموظفين، ورفع استخدام كل إدارة إلى الإدارة العليا شهريًا كجدول ترتيب
- D. التحويل إلى نموذج أفضل (better model)، لأن قلة الاستخدام تدل على أن الإجابات ليست جيدة بما يكفي لمعظم الموظفين

<details><summary>الإجابة</summary>

**B.** تبنّي الذكاء الاصطناعي في المؤسسات (Enterprise AI adoption) مشكلة إدارة تغيير (change-management problem). فالناس يتبنّون أداة عندما يرون كيف تساعد في عملهم هم، كما يعرضه زملاء يثقون بهم. والخيار A مغرٍ لأنه سريع، لكن الوعي (awareness) نادرًا ما يكون العائق. أما C فيخلق امتثالًا دون قيمة (compliance without value). وD يفترض أن النموذج هو المشكلة دون دليل. *(Launch · 7.3)*

</details>

**45. قبل طرح مساعد مذكرات الائتمان لجميع مديري العلاقات (relationship managers)، أي خطوة تمكين (enablement step) هي الأهم؟**

- A. تدريبهم على مواضع قوة المساعد وإخفاقه، وتوضيح أنهم يبقون مسؤولين عن المذكرة التي يوقّعونها (accountable)
- B. منحهم فيديو طويلًا عن بنية النموذج (architecture) كي يفهموا كيف تُنتج مسوداته ويُتحقق منها
- C. إرسال كتيّب المزوّد التسويقي (brochure) الذي يصف بالتفصيل ما يستطيع المنتج فعله في عملهم اليومي
- D. الانتظار حتى يطلب مديرو العلاقات التدريب (training)، كي تجيب الجلسات عن أسئلة يطرحها الناس فعلًا في عملهم

<details><summary>الإجابة</summary>

**A.** يحتاج مستخدمو منتج الصياغة والمراجعة (draft-and-review product) إلى معرفة أين يدققون بشدة (where to look hard) ومن المُساءَل (who is accountable). وهذه المعرفة هي ما يُبقي المراجعة البشرية ذات معنى (meaningful). والخيار B مغرٍ لأنه يبدو شاملًا، لكن فهم البنية (architecture) لا يخبر مدير العلاقات بالأقسام التي يجب أن يتحقق منها. *(Launch · 7.3)*

</details>

### النمو (Grow)

**46. تفيد شركة محايدة (neutral company) بأن مساعدها الذكي (AI assistant) يتولى الآن معظم محادثات العملاء وقد خفّض تكاليف الخدمة (service costs). ما الذي يجب أن يسأله مدير منتج حريص (careful PM) قبل أن يعدّ ذلك نجاحًا؟**

- A. كم رمزًا (tokens) يستخدم المساعد يوميًا، لأن استهلاك الرموز هو ما يحرك معظم تكلفة التشغيل للخدمة كلها
- B. هل يعلن المنافسون أرقامًا مماثلة (competitors)، كي توضع النتيجة في سياق السوق الأوسع الذي يعمل فيه البنك
- C. ماذا حدث للجودة: معدلات الحل، والاتصالات المتكررة، والشكاوى، والرضا (quality) مقارنةً بالموظفين
- D. ما سرعة رد المساعد (reply speed)، لأن الردود السريعة هي أول ما يلاحظه العملاء حين يحادثونه

<details><summary>الإجابة</summary>

**C.** وفورات التكلفة (Cost savings) نصف الصورة فقط. فقد أعلنت Klarna في عام 2024 أن مساعدها يتولى حصة كبيرة من المحادثات، ثم قالت في عام 2025 إنها ستعيد مزيدًا من الخدمة البشرية (human service)، وهذا تذكير بقياس الجودة إلى جانب التكلفة (measure quality alongside cost). والخيار D مغرٍ لأن السرعة مهمة، لكن الإجابة السريعة التي لا تحل المشكلة لا تفعل سوى نقل الاتصال إلى مكان آخر. *(Grow · 8.1)*

</details>

**47. باستخدام إطار HEART من Google (Google's HEART framework)، أي مقياس هو مثال على فئة «نجاح المهمة (Task success)» لمساعد مذكرات الائتمان (Credit Memo Copilot)؟**

- A. حصة المسودات التي تصل إلى لجنة الائتمان دون إعادة كتابة أي قسم (task success)
- B. عدد مديري العلاقات الذين فتحوا المساعد للمرة الأولى هذا الشهر من بين جميعهم الذين يعملون في البنك (opened)
- C. حصة المستخدمين الذين ما زالوا يستخدمونه بعد ثلاثة أشهر مقارنةً بشهرهم الأول في الاستخدام (retention)
- D. درجات استبيان الرضا من مديري العلاقات، تُجمع بعد كل مذكرة ينهونها ويوقّعونها بأنفسهم (satisfaction)

<details><summary>الإجابة</summary>

**A.** يغطي HEART (Rodden, Hutchinson and Fu, 2010) السعادة (Happiness)، والتفاعل (Engagement)، والتبنّي (Adoption)، والاحتفاظ (Retention)، ونجاح المهمة (Task success). ونجاح المهمة يتعلق بما إذا كان المستخدمون ينجزون ما جاؤوا لفعله، بكفاءة وبشكل صحيح (efficiently and correctly). والخيار B تبنٍّ (adoption)، وC احتفاظ (retention)، وD سعادة (happiness). والخيار B هو الأكثر إغراءً لأنه أسهل رقم يمكن الحصول عليه، لكنه لا يقول شيئًا عمّا إذا كان العمل قد أُنجز جيدًا. *(Grow · 8.1)*

</details>

**48. تطلب رانيا من فيصل اقتراح مقياس نجم الشمال (North Star metric) لمساعد مذكرات الائتمان. أيها الأفضل؟**

- A. عدد المسودات المولَّدة (drafts) كل شهر، وهو يزيد مع استخدام مزيد من المديرين للمساعد ومسوداته
- B. الرموز المعالَجة (tokens) شهريًا، وهي تبيّن مدى كثافة استخدام المساعد عبر البنك كل شهر
- C. متوسط تقييم المستخدمين للمسودات (user rating)، وهو يبيّن مدى رضا المديرين عن جودة مخرجاته
- D. الساعات الموفَّرة لكل طلب ائتمان (hours saved)، مع جودة مذكرة عند الحد المتفق عليه أو فوقه

<details><summary>الإجابة</summary>

**D.** يجب أن يلتقط مقياس نجم الشمال القيمة المقدَّمة (value delivered) للمستخدمين وللعمل، وأن يقاوم التلاعب (resist gaming). وقرن الوقت الموفَّر (time saved) بشرط جودة (quality condition) يمنع السرعة على حساب مذكرات الائتمان الجيدة. والخيار A مغرٍ لأنه ينمو مع الاستخدام، لكن عدد المسودات المولَّدة قد يرتفع بينما تنخفض القيمة، مثلًا إذا أعاد الناس توليد المسودات السيئة مرارًا (regenerate bad drafts repeatedly). *(Grow · 8.1)*

</details>

**49. يقدّر طارق أن كل مذكرة من مساعد مذكرات الائتمان تحتاج إلى 5 استدعاءات للنموذج (model calls)، بمتوسط 8,000 رمز إدخال (input tokens) و1,000 رمز إخراج (output tokens) لكل منها. باستخدام أسعار توضيحية (illustrative prices) قدرها $3 لكل مليون رمز إدخال و$15 لكل مليون رمز إخراج، ما تكلفة النموذج لكل مذكرة (model cost per memo)؟**

- A. نحو 0.04 دولار، وهي تكلفة رموز الإدخال والإخراج لاستدعاء واحد فقط (single call)
- B. نحو 0.20 دولار، وهي تكلفة رموز الإدخال والإخراج للاستدعاءات الخمسة (all five calls)
- C. نحو 0.12 دولار، وهي تكلفة رموز الإدخال وحدها للاستدعاءات الخمسة كلها (input only)
- D. نحو 1.95 دولار، وهي التكلفة لو قُرئت الأسعار لكل مئة ألف رمز (per hundred thousand)

<details><summary>الإجابة</summary>

**B.** الإدخال (Input): 5 × 8,000 = 40,000 رمز × $3 لكل مليون = $0.12. الإخراج (Output): 5 × 1,000 = 5,000 رمز × $15 لكل مليون = $0.075. المجموع ≈ $0.195. والخيار C هو الخيار المضلِّل المغري لأنه يحسب رموز الإدخال فقط (only input tokens). ونموذج التكلفة لكل مهمة (cost-per-task model) الحقيقي سيضيف أيضًا إعادات المحاولة (retries)، والاسترجاع (retrieval)، واستدعاءات الضوابط الوقائية (guardrail calls)، والبنية التحتية (infrastructure). والأسعار هنا توضيحية، لا أسعار السوق الحالية (current market rates). *(Grow · 8.2)*

</details>

**50. أضافت شركة برمجيات محايدة ميزة «ذكاء اصطناعي غير محدود (unlimited AI)» إلى اشتراكها الشهري الثابت (flat monthly subscription). والآن تكلّف مجموعة صغيرة من المستخدمين الكثيفين (heavy users) في خدمتها أكثر مما يدفعون. ما أفضل استجابة؟**

- A. إزالة ميزة الذكاء الاصطناعي عن الجميع (remove the feature)، كي لا يكلّف أي عميل أكثر مما يدفع ويصبح العرض بسيطًا
- B. رفع السعر على جميع العملاء بالمقدار نفسه (raise the price)، كي يغطي الاشتراك الثابت تكلفة المستخدمين الكثيفين
- C. إعادة تصميم التسعير ليعكس الاستخدام (usage): حدود استخدام عادل في الباقة الأساسية، وطبقة مميزة للاستخدام الكثيف
- D. تجاهل الأمر، لأن المستخدمين الكثيفين مجموعة صغيرة وهامش الربح المتوسط لكل العملاء ما زال إيجابيًا اليوم (ignore)

<details><summary>الإجابة</summary>

**C.** عندما تكون لكل استخدام تكلفة حقيقية، قد يحوّل التسعير الثابت غير المحدود (flat unlimited pricing) أفضل مستخدميك إلى أقلهم ربحية (least profitable). والفئات أو الحدود أو التسعير القائم على الاستخدام (Tiers, limits or usage-based pricing) تحافظ على هوامش سليمة (healthy margins) مع ترك مجال للقيمة؛ فقد وضعت Duolingo مثلًا ميزاتها للذكاء الاصطناعي التوليدي (GenAI features) في فئة مميزة (Duolingo Max, 2023). والخيار B مغرٍ لأنه بسيط، لكنه يحمّل المستخدمين الخفيفين (light users) تكاليف المستخدمين الكثيفين وقد يدفعهم إلى الرحيل. *(Grow · 8.2)*

</details>

**51. بعد ستة أشهر من الإطلاق، انجرف معدل الموافقة (approval rate) في التمويل الفوري للشركات الصغيرة صعودًا بينما ضعف أداء السداد المبكر (early repayment performance). ولم يتغير شيء في النموذج. ما التفسير الأرجح، والاستجابة الصحيحة؟**

- A. تغيّر المتقدمون أو الاقتصاد، فلم تعد البيانات تطابق التدريب: التحقيق في انحراف المدخلات والنتائج (drift) ثم المراجعة أو إعادة التدريب
- B. في النموذج خطأ برمجي (bug) ظهر منذ الإطلاق؛ يجب الرجوع إلى نسخة أقدم منه
- C. مديرو العلاقات يتجاوزون قرارات النموذج (overriding)؛ يجب تقييد وصولهم إلى وظيفة التجاوز
- D. هذا ضجيج عشوائي (random noise) في عيّنة صغيرة؛ يجب الانتظار ستة أشهر أخرى قبل الخروج بأي استنتاج

<details><summary>الإجابة</summary>

**A.** قد يتدهور النموذج (degrade) دون أي تغيير في الشيفرة عندما يتغير العالم الذي يقيّمه. ومراقبة توزيعات المدخلات (input distributions) والنتائج، ووجود مسار محدد للمراجعة وإعادة التدريب (defined review and retraining path)، جزء من تشغيل منتج ذكاء اصطناعي بعد الإطلاق. والخيار D مغرٍ لأن التشويش ممكن، لكن الانتظار ستة أشهر في الائتمان قد يكون مكلفًا. *(Grow · 8.3)*

</details>

**52. يعلن مزوّد النموذج (model vendor) الذي يقف خلف نجم أسيست أنه سيوقف (retire) إصدار النموذج الذي يستخدمه البنك وينقل العملاء إلى إصدار أحدث. ماذا يجب أن يفعل فيصل؟**

- A. افتراض أن النسخة الأحدث أفضل والتحويل في تاريخ الإيقاف كما يوصي المزوّد (retirement date)
- B. مطالبة المزوّد بإبقاء النسخة القديمة متاحة للأبد (old version)، كي لا يتغير شيء في المنتج
- C. إعادة بناء المساعد من الصفر على نموذج مزوّد آخر، لتفادي الاعتماد على هذا المزوّد (rebuild)
- D. تشغيل حزمة التقييمات الكاملة على النسخة الجديدة أولًا، ومقارنة حالات المجموعة الذهبية والمخاطر الرئيسية، وإصلاح أي تراجع (regressions) في الموجِّهات أو حواجز الحماية

<details><summary>الإجابة</summary>

**D.** قد يغيّر إصدار نموذج جديد السلوك بطرق لن يُظهرها مقياس معياري عام (general benchmark) على مهمتك. وتقييم الانحدار على بياناتك (regression evaluation on your own data) هو الطريقة الوحيدة لتعرف. والخيار A هو الخيار المضلِّل المغري لأن النماذج الأحدث كثيرًا ما تكون أفضل في المتوسط (better on average)، لكن «الأفضل في المتوسط» قد يظل يكسر سلوكًا يعتمد عليه منتجك. *(Grow · 8.3)*

</details>

**53. في أسبوعيها الأولين، سجّلت ميزة رؤى الإنفاق (spending-insights feature) الجديدة في نجم أسيست استخدامًا أسبوعيًا مرتفعًا جدًا، ثم تراجع بثبات منذ ذلك الحين. إلى ماذا يجب أن ينظر فيصل لفهم الصورة الحقيقية؟**

- A. إجمالي الاستخدام منذ الإطلاق (total usage)، وهو ما زال مرتفعًا ويدل على أن العملاء يقدّرون الميزة ويواصلون استخدامها كل أسبوع
- B. الاحتفاظ حسب دفعة الإطلاق (cohort retention): هل يعود من جرّبوا الميزة، وفيمَ يستخدمها العائدون
- C. عدد تنزيلات التطبيق (app downloads) في الفترة نفسها، كمؤشر على الاهتمام العام بتطبيق البنك
- D. متوسط زمن استجابة الميزة (response time)، لأن بطء الاستجابة قد يفسر انخفاض الاستخدام

<details><summary>الإجابة</summary>

**B.** كثيرًا ما تعكس القفزات المبكرة (Early spikes) الفضول (curiosity) لا القيمة الدائمة (lasting value). هذا هو أثر الجِدّة (novelty effect). ويُظهر الاحتفاظ حسب الفوج (Cohort retention) هل أصبحت الميزة عادة (habit) لدى أي أحد، ولدى من. والخيار A مغرٍ لأنه يبدو جيدًا في التقرير، لكن الإجمالي التراكمي (cumulative total) يُخفي التراجع الذي تحتاج إلى فهمه. *(Grow · 8.1)*

</details>

### القيادة (Lead)

**54. يسأل مجلس إدارة نجم (Najm's board) عمّا سيحمي مساعد مذكرات الائتمان (Credit Memo Copilot) من النسخ، في حين يستطيع المنافسون شراء النماذج نفسها. ما أفضل إجابة؟**

- A. موجِّهاتنا سرية (secret prompts)، فلا يستطيع المنافسون إعادة إنتاج طريقة توجيه المساعد
- B. نستخدم أكبر نموذج متاح (largest model)، وهو يعطي أفضل جودة يمكن للمنافسين شراؤها
- C. أطلقنا أولًا (launched first)، لذا سيبقى العملاء والموظفون مع منتجنا بدافع العادة
- D. ما لا يسهل على الآخرين نسخه (moat): بياناتنا الائتمانية، وتغذية راجعة من تعديلات خبرائنا، وتكاملنا العميق في سير عمل الإقراض، وثقة المديرين

<details><summary>الإجابة</summary>

**D.** عندما تكون النماذج متاحة على نطاق واسع، تأتي القابلية للدفاع (defensibility) من البيانات المملوكة (proprietary data)، وحلقات التغذية الراجعة (feedback loops) التي تحسّن المنتج مع الاستخدام، والتكامل في سير العمل (workflow integration)، والتوزيع (distribution). والخيار C مغرٍ لأن الأسبقية قد تساعد، لكنها وحدها نادرًا ما تدوم إذا كان المنتج سهل النسخ. أما A وB فيسهل على المنافسين مجاراتهما. *(Lead · 9.1)*

</details>

**55. تظهر نماذج جديدة كل بضعة أشهر، ويقلق طارق من أن خيارات الفريق ستتقادم سريعًا. أي مبدأ في خارطة الطريق (roadmap principle) يساعد أكثر؟**

- A. انتظار استقرار النماذج قبل بناء أي شيء ذي قيمة (wait)، كي لا يضيع أي عمل لاحقًا بسبب تغيّر النماذج
- B. الالتزام بمزوّد واحد خمس سنوات لتفادي التغيّر (one vendor)، والتفاوض على خصم مقابل الالتزام الطويل
- C. التصميم لنموذج قابل للتبديل (swappable model): طبقة رقيقة بين المنتج والنموذج، وتقييمات خاصة بك، ونموذج بديل
- D. إعادة بناء المنتج كلما صدر نموذج جديد (rebuild)، كي يستخدم دائمًا أحدث نموذج وأقدره من بين ما أصدره المزوّدون

<details><summary>الإجابة</summary>

**C.** في ظل التغير السريع للنماذج (fast model change)، تكون الأصول الدائمة (durable assets) هي تقييماتك وبياناتك وتكاملك في سير العمل ومنطق منتجك (product logic). وإبقاء النموذج قابلًا للتبديل (swappable)، وتقييماتك الخاصة اختبارًا لأي تبديل، يتيح لك الاستفادة من التحسينات دون إعادة بناء. والخيار A مغرٍ بوصفه خيارًا حذرًا، لكن الانتظار يعني أنك لا تتعلم ولا تسلّم أبدًا. أما B فيحبسك لدى مزوّد (locks you in). *(Lead · 9.2)*

</details>

**56. تطلب رانيا من فيصل إعادة صياغة خارطة طريقه (roadmap) لاثني عشر شهرًا، التي تسرد عشر ميزات ذكاء اصطناعي بتواريخ تسليم ثابتة (fixed delivery dates). ما الذي تطلبه على الأرجح؟**

- A. ميزات أكثر (more features) لإظهار الطموح ولإعطاء المجلس صورة أوسع عما يستطيع الفريق تسليمه خلال الاثني عشر شهرًا القادمة
- B. خارطة طريق مصاغة كرهانات (bets): النتيجة المستهدفة، وعدم اليقين الرئيسي، وكيفية اختباره، ومتى نستمر أو نغيّر أو نتوقف
- C. تواريخ أبعد لإضافة هامش (buffer)، كي يقل احتمال إخلاف التزام بالتسليم قُدّم للمجلس
- D. ميزة واحدة فقط (single feature)، لتقليل المخاطر ولكي يركز الفريق كله على شيء واحد وينجزه جيدًا

<details><summary>الإجابة</summary>

**B.** يحمل عمل الذكاء الاصطناعي عدم يقين حقيقيًا (real uncertainty) حول إمكانية بلوغ الجودة. وصياغة خارطة الطريق بوصفها رهانات مع نقاط أدلة (evidence points) وقواعد قرار (decision rules) أكثر صدقًا وتساعد الفريق على القرار أسرع. والخيار C مغرٍ لأنه يقلل خطر تفويت التواريخ، لكنه يُبقي على اليقين الزائف (false certainty) لقائمة الميزات والتواريخ (feature-and-date list). *(Lead · 9.2)*

</details>

**57. لدى بنك نجم الآن خمسة منتجات ذكاء اصطناعي. بنى كل فريق أدوات التقييم (evaluation tools) والضوابط الوقائية (guardrails) والوصول إلى النماذج (model access) الخاصة به، وتتفاوت التكاليف والجودة تفاوتًا كبيرًا. أي تغيير في نموذج التشغيل (operating model) هو الأنسب؟**

- A. فريق منصة ذكاء اصطناعي مشتركة (shared platform) للوصول إلى النماذج وأدوات التقييم وحواجز الحماية وتتبع التكلفة، وتملك فرق المنتج نتائجها
- B. دمج فرق المنتج الخمسة في فريق مركزي واحد (central team)، كي تُتخذ كل القرارات المتعلقة بمنتجات الذكاء الاصطناعي في مكان واحد
- C. ترك كل فريق على حاله (autonomy)، لأن الاستقلالية تدفع السرعة وكل فريق يعرف مستخدميه أفضل من غيره
- D. إسناد كل منتجات الذكاء الاصطناعي إلى مزوّد واحد (outsource)، كي يتحمل مورّد واحد مسؤولية جودتها وتكلفتها

<details><summary>الإجابة</summary>

**A.** مع تكاثر منتجات الذكاء الاصطناعي، تستحق الأجزاء التي يحتاجها كل فريق، مثل التقييمات والضوابط الوقائية والوصول إلى النماذج ورؤية التكاليف (cost visibility)، أن تُبنى مرة واحدة (worth building once). وتحتفظ فرق المنتج بالمسؤولية عن مستخدميها ونتائجها. والخيار B مغرٍ لأنه يعطي الاتساق (consistency)، لكن مركزة قرارات المنتج (centralising product decisions) تبطئ الفرق وتُبعد القرارات عن المستخدمين. أما C فيُبقي على الازدواجية (duplication) والجودة المتفاوتة. *(Lead · 9.3)*

</details>

**58. صُمّم التمويل الفوري للشركات الصغيرة (SME Instant Finance) ليرفض تلقائيًا بعض الطلبات من التجار الأفراد (sole traders) في الاتحاد الأوروبي، دون أي تدخل بشري (no human involvement). أي متطلب يجب أن يصمم له فيصل، بالعمل مع ليلى وسارة؟**

- A. إشعار في الشروط والأحكام (terms and conditions) يكفي، ما دام المتقدم قد وافق عليها
- B. الرفض مسموح فقط إذا ثبت أن النموذج أدق من المراجعين البشر (accuracy)
- C. لا شيء، لأن تمويل الفواتير منتج للأعمال ولا تنطبق عليه قواعد القرارات الآلية (business product)
- D. بموجب المادة 22 من اللائحة العامة لحماية البيانات (GDPR Article 22)، للأفراد حقوق في القرارات الآلية بالكامل ذات الأثر الكبير، تشمل غالبًا التدخل البشري وسبيلًا للطعن، لذا يحتاج المنتج إلى مسار مراجعة بشرية حقيقي

<details><summary>الإجابة</summary>

**D.** التاجر الفرد شخص طبيعي (natural person)، وقد يكون لرفض الائتمان أثر كبير عليه (significant effect). والمادة 22 من GDPR تقيّد القرارات المؤتمتة بالكامل من هذا النوع، وحيث يُسمح بها، تشترط ضمانات (safeguards) مثل التدخل البشري والحق في الاعتراض (right to contest). ودور مدير المنتج (PM's part) هو تصميم هذا المسار داخل المنتج. والخيار C هو الخيار المضلِّل المغري لأن المنتج موجّه للأعمال، لكن التجار الأفراد أفراد (individuals). والتفاصيل القانونية مكانها *AI Governance: Zero to Hero*. *(Lead · 9.4)*

</details>

**59. يريد خالد رفع حد الموافقة التلقائية (automatic approval limit) للتمويل الفوري للشركات الصغيرة بشكل حاد بعد ربع أول قوي. ما أفضل استجابة قيادية (leadership response)؟**

- A. الموافقة، لأن النتائج قوية ونمو الموافقات سيساعد الأعمال على بلوغ أهداف الإقراض للسنة كلها وللسنة التالية (agree)
- B. رفض أي زيادة حتى يعمل النموذج خمس سنوات ويجتاز دورة ائتمانية كاملة دون تغييرات (refuse)
- C. الزيادة على مراحل مع سقوف تعرّض (exposure caps)، ومواصلة مراقبة النتائج والانحراف، والاتفاق مسبقًا على ما يستدعي التراجع
- D. ترك القرار لفريق علم البيانات (data science team)، لأنه يفهم النموذج وحدوده أفضل من أي أحد في البنك

<details><summary>الإجابة</summary>

**C.** ربع جيد واحد لا يقول الكثير عن سلوك النموذج في ظروف مختلفة. والتوسع المرحلي مع حدود (Staged expansion with limits) يضع سقفًا للضرر إذا تغيّر العالم. فقد أُغلقت Zillow Offers تدريجيًا عام 2021 بعد أن أخطأت خوارزمية التسعير (pricing algorithm) لديها في تسعير المنازل على نطاق واسع (mispriced homes at scale)، مع شطب كبير للقيم (large write-downs). والخيار A مغرٍ لأن النتائج جيدة، لكنه يتحمّل كامل الجانب السلبي (full downside) لنموذج لم يُختبر في اقتصاد مختلف. *(Lead · 9.2)*

</details>

**60. في مقابلة لوظيفة مدير منتج ذكاء اصطناعي (AI product manager role)، يُطلب من فيصل التحدث عن مشروع في ملف أعماله (portfolio). أي إجابة ستُبهر أكثر؟**

- A. وصف تفصيلي لبنية النموذج (architecture) والموجِّهات التي كتبها، مع أسباب كل خيار اتخذه فيها
- B. المشكلة والمستخدم، وأين قرر أن الذكاء الاصطناعي يناسب، وكيف عرّف الجودة وقاسها، ومفاضلة وسببها، والنتائج بما فيها ما لم ينجح (trade-off)
- C. عرض حي (live demo) للمنتج يعمل جيدًا على مثال منتقى يُظهر أفضل ميزاته أمام لجنة المقابلة
- D. قائمة بكل أداة ذكاء اصطناعي استخدمها (AI tool)، مع تواريخها، لإظهار اتساع خبرته العملية في المجال

<details><summary>الإجابة</summary>

**B.** يبحث مديرو التوظيف (Hiring managers) لوظائف مدير منتج الذكاء الاصطناعي عن حسّ المنتج (product judgement): تأطير المشكلة (problem framing)، والتقييم، والمفاضلات (trade-offs)، والتعلّم من النتائج. وعرض ما لم ينجح يُظهر الصدق والصرامة (honesty and rigour). والخيار C مغرٍ لأن العروض التوضيحية حيّة ومؤثرة (vivid)، لكن عرضًا مصقولًا (polished demo) على مثال مختار يُخفي بالضبط ما يُدفع لمدير منتج الذكاء الاصطناعي أجرٌ لفهمه. والفجوة بين العرض التوضيحي وسير العمل الحقيقي (gap between demo and real workflow) درس كثيرًا ما يُستخلص من IBM Watson Health، التي بيعت وحداتها عام 2022 بعد استثمار كبير. *(Lead · 10.2)*

</details>

## 🧾 الخلاصة (Recap)
- **54–60 إجابة صحيحة (correct):** أخطاء قليلة (few misses). استخدم سجل الأخطاء (error log) لتحديد الدروس التي تقف خلفها، وأعد قراءتها.
- **48–53 إجابة صحيحة (correct):** بعض الفجوات (some gaps). أعد قراءة الدروس التي تقف خلف كل إجابة خاطئة.
- **36–47 إجابة صحيحة (correct):** فجوات في عدة مراحل (gaps in several stages). حدّد أضعف مرحلتين لديك (two weakest stages) في الجدول تحت «كيف يعمل (How it works)»، وأعد العمل على تلك الوحدات وأسئلة «اختبر نفسك (check-yourself)» فيها، ثم أعد الامتحان بعد أسبوع.
- **أقل من 36 (Below 36):** ارجع إلى الوحدات 2–9 (Modules 2–9) بالترتيب، وأنجز التمارين هذه المرة، وأدِّ المشروع الختامي (capstone) في 10.1 قبل المحاولة مجددًا.
- أيًا كانت نتيجتك، راجع كل سؤال خمّنت إجابته. فالتخمين المحظوظ (lucky guess) فجوة لم تكتشفها بعد.

## 📚 المراجع (References)
- Teresa Torres, *Continuous Discovery Habits* (2021) — https://www.producttalk.org/
- Marty Cagan, *Inspired* (2nd ed., 2017) — https://www.svpg.com/
- Ron Kohavi, Diane Tang and Ya Xu, *Trustworthy Online Controlled Experiments* (2020) — https://experimentguide.com/
- Saleema Amershi et al., "Guidelines for Human-AI Interaction", CHI 2019 — https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/
- Google PAIR, People + AI Guidebook — https://pair.withgoogle.com/guidebook/
- Lianmin Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (2023) — https://arxiv.org/abs/2306.05685
- Kerry Rodden, Hilary Hutchinson and Xin Fu, "Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications", CHI 2010 — https://research.google/
- EU AI Act, Regulation (EU) 2024/1689 — https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- GDPR, Regulation (EU) 2016/679 — https://eur-lex.europa.eu/eli/reg/2016/679/oj
