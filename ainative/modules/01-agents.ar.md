# الوحدة 1 — كيف يعمل وكلاء البرمجة (How coding agents work)

*يمنحك الدرس 1.1 النموذجَ الذهني (mental model) الذي يتيح لك أن تتوقع ما سيؤديه الوكيل جيدًا (what an agent will do well) وأين سيفشل (where it will fail): فالنموذج دالة عديمة الحالة لسياقه (a stateless function of its context)، ووكيل البرمجة (coding agent) هو ذلك النموذج مع أدوات في حلقة (that model with tools in a loop)، وما ليس في السياق لا وجود له بالنسبة إليه (what is not in the context does not exist for it). ويشرح لماذا يتألق الوكلاء في الاتساع والسرعة وإكمال الأنماط والعمل الآلي (brilliant at breadth, speed, pattern completion and mechanical work)، ويسمّي الطرق العشر التي يفشلون بها (the ten ways they fail) مع مثال من نجم ريميت (Najm Remit) لكل منها، وينتهي بـ«الدليل الميداني لأنماط الإخفاق» (Failure-mode field guide): العَرَض (symptom) وأرخص كشف (cheapest detection) والوقاية (prevention) لكل نمط (for every mode). أما الدرس 1.2 فهو المختبر (the lab): تقرأ ثلاث جلسات وكلاء مُختلَقة (three constructed agent sessions) على ريميت، وتسمّي الإخفاق في كل منها (name the failure in each)، وتجد الدور الذي حدث فيه الخطأ (the turn where it went wrong)، وتختار أرخص وقاية (the cheapest prevention). ويمكن إنجاز ذلك كله دون وكيل (without an agent)؛ وفي جزء اختياري (an optional part) تشغّل جلسة قصيرة للقراءة فقط (a short read-only session) بنفسك وتكتب عنها تقريرًا (write it up). وكل ما يخص جانب نجم خيالي (Everything on the Najm side is fictional).*

> **التركيز (Focus):** Mindset, Verify — نموذج لكيفية عمل الوكلاء (a model of how agents work) يتنبأ بمواضع فشلها (predicts where they fail)، وعادة قراءة الجلسة بوصفها دليلًا (the habit of reading a session as evidence).

---

# 1.1 — النموذج الذهني: السياق والأدوات والحلقة، ولماذا يتألق الوكلاء ولماذا يفشلون (The mental model: context, tools and the loop, and why agents are brilliant and why they fail)
*المستوى (Level): 🟢 مبتدئ (Beginner)* · *المتطلبات (Prerequisites): 0.3* · *التركيز (Focus): Mindset*

## ⚡ الدرس في دقيقة (In 60 seconds)
- النموذج **دالة عديمة الحالة لسياقه (stateless function of its context)**: فما ليس في السياق (context) لا وجود له بالنسبة إليه (does not exist for it).
- الوكيل (agent) هو نموذج مضافٌ إليه **أدوات (tools)** — القراءة والبحث والتعديل والتشغيل (read, search, edit, run) — في **حلقة (loop)**: تعود كل نتيجة إلى السياق (each result goes back into the context).
- وهو بارع في الاتساع والسرعة وإكمال الأنماط والعمل الآلي (brilliant at breadth, speed, pattern completion and mechanical work)، ويفشل بعشر طرق يسهل التعرّف عليها (ten recognisable ways) هي **الدليل الميداني لأنماط الإخفاق (Failure-mode field guide)**.
- أربعة أشياء تتنبأ بالنجاح (Four things predict success): **قابلية التحقق (verifiability)، والمحلية (locality)، والسياق (context)، والألفة (familiarity)**.
- إشارة القرار (Decision cue): قبل أن تفوّض (before you delegate)، سمِّ الإخفاق الذي تتوقعه (name the failure you expect) وأرخص طريقة لرؤيته (the cheapest way to see it).
- أكبر فخ (Biggest trap): عدّ الكلام الطليق صحيحًا (reading fluent as correct). فالطلاقة (Fluency) لا تكلّف النموذج شيئًا (costs the model nothing).

## 🧭 لماذا يهم (Why it matters)
في يوم اثنين (On a Monday)، وهو يوم مُختلَق لا مسجَّل من نموذج حقيقي (a constructed day, not recorded from a real model)، توجّه لجين، المهندسة حديثة التخرج (graduate engineer)، وكيلها إلى `screening.py`، وهي الوحدة القديمة التي لا اختبارات لها (the old module with no tests). وبعد ست دقائق يكون قد كتب ثمانية عشر اختبار توصيف (characterization tests) حسنة التسمية، وتقرأ هي كل واحد منها (she reads every one). وفي يوم الثلاثاء (On Tuesday)، ومع الوكيل نفسه، تطلب حدث تدقيق (audit event) عند إنشاء عرض سعر (when a quote is created). فيكتب `audit.record("quote.created", ...)` و`ids.generate("QUO")`. ولا وجود لأيٍّ منهما في najmkit، ولا يستدعي أي اختبار الدالة المساعدة الجديدة (no test calls the new helper)، فتبقى مجموعة الاختبارات خضراء (the suite stays green).

يفتتح طارق، قائد الهندسة (engineering lead)، العيادة (the clinic) بالقصتين معًا: «الأداة نفسها. لماذا تألقت في الوحدة الصعبة (shine on the hard module) وتعثرت في استدعاء من سطر واحد (fall over on a one-line call)؟» والجواب نموذج ذهني (a mental model) لا حظ (not luck).

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**النموذج دالة لسياقه (A model is a function of its context).** يقرأ النموذج اللغوي (language model) سلسلة من قطع النص تسمّى **الرموز (tokens)** وينتج الرموز التالية. ولا يحتفظ بأي حالة بين الاستدعاءات (keeps no state between calls): فلا شيء عن الأمس أو عن مستودعك (your repository) يبقى ما لم يُرسَل من جديد (unless it is sent again). والبرنامج يعيد إرسال المحادثة (re-sends the conversation) في كل دور (every turn)، وهذا ما يبدو كأنه ذاكرة (feels like memory). ومن هنا قاعدة الدورة المركزية (the course's central rule): **ما ليس في السياق لا وجود له بالنسبة إلى النموذج (what is not in the context does not exist for the model)**. وتُدرَّس هذه الفكرة نفسها من جهة واجهة البرمجة (from the API side) في [*بناء تطبيقات الذكاء الاصطناعي والوكلاء (Building AI Applications & Agents)*، الدرس 1.1 — الفكرة الواحدة: دالة عديمة الحالة والرموز ونافذة السياق وقائمة الرسائل (The one idea: a stateless function, tokens, the context window and the messages list)](../aiapps/index.ar.html#/1.1).

**ما الذي يملأ نافذة السياق (What fills the context window).** نافذة السياق (context window) هي أكبر قدر من النص يستطيع استدعاء واحد حمله (the most text one call can hold). وفي Claude Code على ريميت (on Remit) تمتلئ من خمسة مصادر (five places).

| المصدر (Source) | مثال في ريميت (Example on Remit) | من يتحكم فيه (Who controls it) |
|---|---|---|
| **التعليمات (Instructions)** | موجّه النظام (system prompt) وتعريفات الأدوات (tool definitions) التي تأتي مع الأداة | الأداة (The tool) |
| **ملفات الذاكرة (Memory files)** | `CLAUDE.md`، وأول أسطر الذاكرة التلقائية (the first lines of auto memory) | أنت، إضافةً إلى ملاحظات الوكيل نفسه (the agent's own notes) — الوحدة 2 (Module 2) |
| **محتويات الملفات (File contents)** | `service.py` بعد أن يقرأه الوكيل (once the agent has read it) | الوكيل، بتوجيه منك (guided by you) |
| **مخرجات الأدوات (Tool output)** | نقاط `pytest` (dots)، ونتيجة `grep`، وتتبّع المكدّس (a stack trace) | الأوامر التي يشغّلها (The commands it runs) |
| **المحادثة (Conversation)** | موجّهاتك وردوده وخططه (Your prompts, its replies, its plans) | أنت والوكيل (You and the agent) |

للوكيل الفرعي (subagent) نافذة خاصة به (a window of its own)، ولا يعود إلا تقريره النهائي (only its final report comes back). ويعرض `/context` ما يستهلك النافذة (what uses the window) وأيّ ملفات ذاكرة حُمّلت (which memory files loaded).

**الرموز والكلفة، وصفًا نوعيًّا (Tokens and cost, qualitatively).** تدفع ثمن الرموز المقروءة والمكتوبة (tokens read and written)، وكل دور يقرأ السياق كله من جديد (every turn reads the whole context again). فسجل من 4,000 سطر (A 4,000-line log) لُصق في الدور الثالث (pasted on turn three) يُقرأ من جديد في كل دور لاحق (every later turn). وكثيرًا ما يمنح المزوّدون (providers) خصمًا على السياق المتكرر (discount repeated context)، لكنه ليس مجانيًا (not free) ويظل ينافس على الانتباه (competes for attention). ويعرض `/usage` استخدامك (your usage)، وكتلة كلفة الجلسة فيه مخصصة لمستخدمي واجهة البرمجة (its session-cost block is meant for API users).

**الحلقة (The loop).** يضيف الوكيل أيديَ إلى النموذج (An agent adds hands): النموذج نفسه، يُستدعى في حلقة (called in a loop)، ومعه أدوات للقراءة والبحث والتعديل وتشغيل الأوامر (tools to read, search, edit and run commands). يطلب النموذج أداة (asks for a tool)، فيفحص البرنامج قواعد الصلاحيات (checks the permission rules)، ثم يشغّلها (runs it)، ويُلحق النتيجة بالسياق (appends the result to the context)، ويستدعي النموذج من جديد (calls the model again). ويتوقف عندما يجيب النموذج بدل أن يطلب (when the model answers instead of asking). وتعمل حلقة الوكيل (agent loop) هذه داخل خطوة *فوِّض (delegate)* من حلقة المهندس الأصيل في الذكاء الاصطناعي (AI-native loop) في الدرس 0.3، وهي الخطوة التي تبقى لك (which stays yours).

```mermaid
flowchart TD
    G["موجّهك والسياق"] --> M["النموذج يقرأ السياق"]
    M --> D{"استدعاء أداة أم إجابة؟"}
    D -->|"استدعاء أداة"| P{"هل هو مسموح؟"}
    P -->|"لا"| Q["يسألك أو يُرفض"]
    Q --> M
    P -->|"نعم"| T["شغّله: اقرأ، ابحث، عدّل، شغّل"]
    T --> R["تُلحَق النتيجة بالسياق"]
    R --> M
    D -->|"إجابة"| H["تقرأ الإجابة والفروقات"]
    H -->|"الموجّه التالي"| G
```

تجعل الحلقة الوكلاء مفيدين ومحفوفين بالمخاطر في آن واحد (useful and risky): فهم يستطيعون التحقق من عملهم بتشغيل الاختبارات (check their work by running tests)، ويمكن أن يضلّلهم ما تعيده الأداة (be misled by what a tool returns)، من رسالة خطأ مربكة (a confusing error) إلى ملف README فيه تعليمات (a README with instructions in it). وتجد بنية الحلقة الداخلية وحساب الكلفة (the loop's internals and the cost arithmetic) في [*بناء تطبيقات الذكاء الاصطناعي والوكلاء (Building AI Applications & Agents)*، الدرس 8.1 — خطِّط ونفِّذ ولاحِظ وكرِّر: التأمل الذاتي وشروط التوقف وأولى أنماط الإخفاق (Plan, act, observe, repeat: reflection, stopping conditions and the first failure modes)](../aiapps/index.ar.html#/8.1).

**لماذا هم بارعون (Why they are brilliant).** أربع نقاط قوة (Four strengths): **الاتساع (breadth)** — يقرأ في جلسة واحدة Python وSQL وقوالب عربية (Python, SQL and Arabic templates)، و**السرعة (speed)** — وحدة من 300 سطر في ثوانٍ (a 300-line module in seconds)، و**إكمال الأنماط (pattern completion)** — أره ثلاثة اختبارات بأسلوبك فيكتب الرابع (show it three tests in your style and it writes the fourth)، و**العمل الآلي الذي لا يكلّ (tireless mechanical work)** — أعد تسمية معامل في أربعين موضعًا (rename a parameter in forty places)، واكتب ثلاثين حالة مقادة بجدول (thirty table-driven cases): فهو ليس أكثر إهمالًا عند العنصر الأربعين (no sloppier at item 40).

### 🟡 التعمق أكثر (Going deeper)

**لماذا يفشلون (Why they fail).** حقيقة واحدة تفسّر كل إخفاق (One fact explains every failure): ينتج النموذج استمرارًا *معقولًا (plausible)* لسياقه، والمعقول ليس صحيحًا ولا حديثًا ولا ما قصدته (plausible is not true, current or what you meant). وتتكرر عشرة أنماط (Ten modes recur)؛ ولكل منها معرّف (id) يُستعمل في الدليل الميداني (field guide) وفي المختبر m01 (lab m01).

- **`hallucinated-api`.** يُكمل النموذج استدعاءً يبدو صحيحًا (completes a call that looks right). وnajmkit مضمَّنة داخل المستودع (vendored) وليست في أي مجموعة تدريب (in no training set)، فيخمّن من الأسماء (guesses from names): `ids.generate("QUO")` بدلًا من `ids.new_id("QUO")`. وقاست دراسة مخبرية على 16 نموذجًا (One lab study of 16 models) *أسماء حزم* مخترعة (invented package names)، لا عمليات تثبيت فعلية (not real installs)، بمتوسط معدلات لا يقل عن 5.2% للنماذج التجارية و21.7% للنماذج المفتوحة المصدر (at least 5.2% for commercial and 21.7% for open-source models) (Spracklen et al., 2025).
- **`stale-knowledge`.** يتوقف التدريب عند تاريخ قطع (Training stops at a cutoff). يكتب الوكيل `datetime.utcnow()` بحكم العادة (from habit)؛ وقد أعلنت Python إيقاف استعمالها (deprecated it) في الإصدار 3.12، فهي تعيد وقتًا ساذجًا بلا منطقة زمنية (a naive time)، وساعة najmkit ترفض الأوقات من هذا النوع (najmkit's clock rejects those). كان ذلك صحيحًا يومًا (It used to be true).
- **`misread-requirement`.** للتذكرة الغامضة (A vague ticket) عدة قراءات (several readings)، فيختار الوكيل إحداها بصمت (silently picks one). فعبارة «قرِّب الرسوم في الإيصال إلى ريالات صحيحة» (Round the fee on the receipt to whole riyals) قد تعني المعروض أو المحصَّل (displayed or charged). فيعدّل `quote_fee`، ويتبعه كل قيد في دفتر الأستاذ (every ledger posting follows).
- **`symptom-fix`.** يزول الخطأ ويبقى السبب (The error goes and the cause stays). يتلقى العملاء `quote_expired`، فيرفع الوكيل `QUOTE_TTL` من 60 إلى 600 ثانية. فصار البنك يلتزم بسعر الصرف عشر دقائق (honours a rate for ten minutes)، بينما تبقى إعادة المحاولة التي أعادت استخدام عرض سعر قديم (the retry that reused an old quote) على حالها (untouched).
- **`sycophancy`.** يميل النموذج إلى الموافقة (leans toward agreeing). تسأل لجين: «عملاء T3 بلا حد للإرسال (no sending limit)، أليس كذلك؟ وثِّق ذلك (Document that).» فيوافق الوكيل، بينما تنص `LIMITS["T3"]` على 30,000.00 في اليوم. ووجد بحث أجرته Anthropic، الشركة التي تصنع Claude Code، أن خمسة مساعدين أظهروا المجاملة المفرطة بانتظام (five assistants consistently showed sycophancy)، وأن الناس ونماذج التفضيل (preference models) فضّلوا أحيانًا الإجابات المقنعة الموافِقة على الصحيحة (preferred convincing agreeable answers to correct ones) (Sharma et al., 2023). وهذا ميل لا معدل ينطبق على أداتك (a tendency, not a rate for your tool).
- **`context-rot`.** في الجلسة الطويلة (In a long session) قد تُتجاهل القاعدة التي ذُكرت في الدور 3 — «المال `Decimal`» (money is Decimal) — بحلول الدور 80، فتظهر `float(fee)`. والقاعدة التي قيلت في المحادثة وحدها (a rule said only in conversation) لا تُقرأ من جديد بعد `/compact`؛ أما التي في ملف ذاكرة المشروع (the project's memory file) فتُقرأ. ووجد Liu وآخرون أن الدقة تراجعت (accuracy fell) حين وقع النص المعني في منتصف مدخل طويل (the relevant text sat mid-way through a long input) مع نماذج حقبة 2023 (2023-era models)، ووجدت Chroma، في تقرير من مورّد لم يخضع لمراجعة الأقران (a vendor report, not peer reviewed)، أن الأداء يتفاوت مع طول المدخل حتى في المهام البسيطة (performance varies with input length even on simple tasks)؛ فاختبر نموذجك أنت (test your own model).
- **`runaway-loop`.** يكرر الوكيل محاولة فاشلة (repeats a failed attempt). يفشل اختبار إشعار عربي (An Arabic notification test) بسبب حرف واحد يبدو مطابقًا في الطرفية (looks identical in a terminal)، فـ«يصلح» الوكيل النص ست مرات (six times).
- **`test-gaming`.** للوصول إلى اللون الأخضر (To reach green) يُضعف الفحص (weakens the check): فيتحول `assert text == (...)` في اختبار الإشعار العربي إلى `assert "TRF-000001" in text`. تنجح المجموعة (The suite passes)، ويمكن الآن أن تصل الأرقام الغربية إلى العملاء (Western digits can now reach customers).
- **`injection`.** قد يحمل النص الذي يقرؤه الوكيل تعليمات يعاملها كأنها تعليماتك (instructions it treats as yours). تعرّف OWASP حقن الموجّه (prompt injection) بأنه مدخلات تغيّر سلوك النموذج بطرق غير مقصودة (inputs that alter a model's behaviour in unintended ways)، وأفادت Invariant Labs، في بحث من مورّد (vendor research) عام 2025، بأن بلاغًا عامًّا خبيثًا على GitHub (a malicious public GitHub issue) وجّه وكيلًا إلى تسريب بيانات مستودع خاص (steering an agent into leaking private-repository data). فملف README أو البلاغ أو صفحة الويب أو السجل مدخلات (A README, issue, web page or log is input)؛ وتعود إلى هذا الوحدة 8 والدرس [*أمن الذكاء الاصطناعي وأمن التطبيقات (Secure AI & Application Security)*، الدرس 8.2 — حقن الموجّهات وكسر القيود، المباشر وغير المباشر (Prompt injection and jailbreaks, direct and indirect)](../secai/index.ar.html#/8.2).
- **`scope-creep`.** يُطلب منه إصلاح كلمة واحدة (Asked to fix one word)، فيعيد تنسيق الوحدة أيضًا و«يحسّن» الصياغة العربية (reformats the module and "improves" the Arabic wording). فتصير الفروقات (The diff) 40 سطرًا لا سطرين.

**عدم الحتمية والحدّ المتعرّج (Non-determinism and the jagged frontier).** قد يعطي الموجّه نفسه شيفرة مختلفة في التشغيل الثاني (can give different code on a second run): تستخدم دالة رسوم `Decimal`، وتستخدم التالية `round(float(...))`. والتشغيل الناجح الواحد عيّنة واحدة (One passing run is one sample): فاحكم بفحوص لا تعتمد على التشغيل (judge by checks that do not depend on the run). ويصف الممارسون القدرة أيضًا بأنها *متعرّجة (jagged)* — فكرة لا قياس (an idea, not a measurement): فالنجاح في مهمة يتنبأ بالقليل عن مهمة تبدو مشابهة (success on one task predicts little about a similar-looking one)، لذا اطلب خطوة أولى صغيرة يمكنك فحصها (ask for a small first step you can check).

**ما الذي يتنبأ بالنجاح (What predicts success).** أربعة أسئلة تُطرح قبل أن تفوّض (Four questions, asked before you delegate).

| المؤشر (Predictor) | اسأل (Ask) | سهل في ريميت (Easy on Remit) | صعب في ريميت (Hard on Remit) |
|---|---|---|---|
| **قابلية التحقق (Verifiability)** | هل يستطيع أمر أن يخبرني في ثوانٍ إن كان الناتج صحيحًا؟ ⁦(Can a command tell me in seconds if it is right?)⁩ | اختبارات (Tests) لـ`screening.py` | تغيير في التسعير (A pricing change) لا يثبّته أي اختبار (no test pins down) |
| **المحلية (Locality)** | كم ملفًّا يتغير، وهل هناك اقتران خفي؟ ⁦(How many files change, and is there hidden coupling?)⁩ | رسالة واحدة (One message) في `notify.py` | قاعدة رسوم (A fee rule) تمتد عبر `fees.py` ودفتر الأستاذ (the ledger) والرسائل (the messages) |
| **السياق المتاح (Available context)** | هل كل ما يحتاجه في النافذة أو يمكن العثور عليه؟ ⁦(Is everything it needs in the window or findable?)⁩ | ثوابت واختبارات (Constants and tests) في المستودع (in the repo) | القاعدة موجودة في ملف PDF أو في رأس مالك المنتج (The rule lives in a PDF or in the product owner's head) |
| **الألفة (Familiarity)** | هل هذا شائع في الشيفرة العامة؟ ⁦(Is this common in public code?)⁩ | اختبارات مقادة بجدول (Table-driven tests)، وخيار في سطر الأوامر (a CLI flag) | najmkit؛ وقاعدة فحص خاصة بالبنك (a bank-specific screening rule) |

تنسجم الأدلة مع هذا الجدول دون أن تثبته (The evidence fits this table without proving it). فقد وجدت تجربة عشوائية مضبوطة (randomized trial) على 16 مطوّرًا من ذوي الخبرة (16 experienced developers) في مستودعاتهم الناضجة الخاصة (their own mature repositories) أن المهام استغرقت وقتًا أطول بنسبة 19% (took 19% longer) مع أدوات مطلع 2025 (early-2025 tools)، مع أنهم توقعوا — وظلوا يعتقدون بعد ذلك — أنهم أسرع (they had expected, and afterwards believed, they were faster)؛ وتحذّر METR من أن بيئات أخرى وأدوات لاحقة قد تختلف (other settings and later tools may differ). ووجدت تجربة مخبرية على مهمة واحدة قائمة بذاتها (a lab experiment on one self-contained task)، لمؤلفين من GitHub وMicrosoft Research، أن مستخدمي Copilot أسرع بنسبة 55.8% بفاصل ثقة 95% يمتد من 21% إلى 89% (95% interval 21% to 89%). والنتائج تعتمد على المهمة والأداة والخبرة (Results depend on task, tool and experience)؛ وليست أي منهما قاعدة لفريقك (neither is a rule for your team).

**موجّه ضعيف وموجّه أقوى (A weak prompt and a stronger one).** خذ طلب الثلاثاء، بعد وضع ما لا يستطيع النموذج معرفته في السياق (with what the model cannot know put into the context):

```text
Weak:     Add an audit event when a quote is created.

Stronger: Add an audit event when a quote is created, in src/remit/service.py.
          najmkit is internal and not in your training data: read docs/najmkit.md
          first and use only calls listed there. Money stays Decimal; touch no
          other file. Before editing, name the najmkit call you will use.
```

لا ضمان هنا (No guarantee): فبحثٌ بـ grep في الفروقات يظل هو الحاسم (a grep of the diff still decides). تجاوز هذا لتغيير من سطر واحد تقرؤه في عشر ثوانٍ (Skip it for a one-line change you can read in ten seconds)؛ وتنقل الوحدة 2 الأجزاء الثابتة (the standing parts) إلى ملف الذاكرة (the memory file).

### 🔴 نظرة الخبير (Expert view)

**النموذج والجهد (Model and effort) — راجع الوثائق الحالية فهذه الأمور تتغير (check the current documentation; these move).** يتيح لك Claude Code اختيار النموذج (choose the model) بالأمر `/model` أو `claude --model <alias>`؛ فالاسم المستعار `opusplan` يخطط بـ Opus وينفّذ بـ Sonnet (plans with Opus and executes with Sonnet)، واختيار جهد التفكير (the thinking effort) بالأمر `/effort` من `low` إلى `max`؛ وتختلف القيم الافتراضية بحسب النموذج (defaults differ by model). وتطلب `ultrathink` في موجّه تفكيرًا أعمق في ذلك الدور (deeper reasoning for that turn)؛ أما «think hard» فلا تعني شيئًا خاصًا (means nothing special). والجهد الأكبر يعني تفكيرًا أكثر (more thinking) يُحاسَب عليه حتى لو طُوي (billed even when collapsed): جرّب الإعدادات الأقوى للتخطيط وتصحيح الأخطاء الصعب (planning and hard debugging)، والأرخص للتعديلات التي ستتحقق منها على أي حال (edits you will verify anyway)، واحسم بمهامك أنت لا بلوحات الصدارة (not leaderboards) — الوحدة 13 (Module 13).

**توقف مبكرًا (Stop early).** يقاطع `Esc` الوكيل (interrupts the agent)؛ افعل ذلك حين ترى الإخفاق نفسه مرتين (when you see the same failure twice). ويفتح `/rewind`، أو الضغط على `Esc` مرتين في موجّه فارغ (twice on an empty prompt)، قائمة لاستعادة الشيفرة أو المحادثة أو كليهما (restore code, conversation or both). ولا تُتتبَّع تغييرات Bash (Bash changes are not tracked)، فيبقى git شبكة الأمان (the safety net). وللتشغيل في الوضع غير التفاعلي (Headless runs) الخيار `--max-turns`.

## 🧰 الأدوات (The toolkit)
| الأداة أو الممارسة أو النمط (Tool, practice or pattern) | ما هي وماذا تفعل (What it is and does) | متى تلجأ إليها (When to reach for it) |
|---|---|---|
| **Failure-mode field guide** — الدليل الميداني لأنماط الإخفاق | عشرة أنماط (Ten modes): العَرَض (symptom)، وأرخص كشف (cheapest detection)، والوقاية (prevention) | قبل التفويض (Before delegating)، وفي المراجعة (in review)، وفي الاجتماعات الاسترجاعية (in retros) |
| **Task-fit check** — فحص ملاءمة المهمة | أربعة أسئلة تُقيَّم من 0 إلى 2 (Four questions scored 0 to 2) | قبل أي تفويض غير هيّن (Before any non-trivial delegation) |
| **Fresh session** — جلسة جديدة | يعرض `/context` ما يملأ النافذة (what fills the window)؛ ويبدأ `/clear` من صفحة نظيفة (starts clean)، ويلخّص `/compact` (summarises)، ويتولى وكيل فرعي (a subagent) مهمة جانبية (a side job) | بين المهام (Between tasks)؛ وحين تطول الجلسة أو ينسى الوكيل (when a session is long or it forgets) |
| **Plan mode** — وضع التخطيط | استكشف واقترح دون تعديل (Explore and propose without editing) — `Shift+Tab` أو `claude --permission-mode plan` | حين تكون إساءة الفهم مكلفة (When a misreading is costly)؛ والجزء 2 من المختبر (lab part 2) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
المُنتَج (The artefact) هو **الدليل الميداني لأنماط الإخفاق (Failure-mode field guide)**. وقاعدة طارق: يسمّي طلب الدمج (pull request) المُنجَز بمساعدة الذكاء الاصطناعي أنماط الإخفاق التي فحصها صاحبه (names the failure modes its author checked for)، ويضيف الاجتماع الاسترجاعي (a retro) صفًّا لكل نمط جديد (a row for each new one). انسخه إلى `field-guide.md` في مستودع ملاحظاتك (your notes repository). ويستخدم المختبر m01 هذه المعرّفات العشرة (ten ids) وسبع فئات للوقاية (seven prevention categories): `context` و`spec` و`small-steps` و`verify` و`permissions` و`fresh-start` و`review`.

| النمط (Mode) والمعرّف (id) | العَرَض (Symptom) | أرخص كشف (Cheapest detection) | الوقاية (Prevention) |
|---|---|---|---|
| `hallucinated-api` | استدعاء أو خيار أو حزمة (A call, flag or package) لا توجد في أي وثيقة ولا في أي ملف من المستودع (in no doc and no repo file) | ابحث بـ grep عن الاستدعاءات الجديدة في `docs/najmkit.md` (Grep new calls)؛ وشغّل المسار مرة واحدة (run the path once) | `context`: سمِّ الوثائق في الذاكرة (name the docs in memory) |
| `stale-knowledge` | تحذيرات الإيقاف (Deprecation warnings)؛ شيفرة تشبه درسًا قديمًا (code like an old tutorial) | شغّل مع تفعيل التحذيرات (Run with warnings on)؛ وقارن بالإصدارات المثبَّتة (pinned versions) | `context`: الإصدارات وقواعد البيت (versions and house rules) في الذاكرة |
| `misread-requirement` | شيفرة صحيحة لسؤال مختلف (Correct code for a different question) | اطلب منه إعادة صياغة المتطلب والافتراضات (restate the requirement and assumptions) | `spec`: معايير القبول (acceptance criteria)، وما ليس من الأهداف (non-goals) |
| `symptom-fix` | زال الخطأ ولم يُسمَّ السبب (The error is gone, the cause unnamed) | اسأل «ما السبب؟» ⁦(what was the cause?)⁩؛ واطلب اختبارًا يفشل أولًا (a test that fails first) | `verify`: أعد الإنتاج أولًا (reproduce first)، ثم اختبار انحدار (a regression test) |
| `sycophancy` | «أنت محق» (You're right) قبل أي دليل (before any evidence) | أعد الصياغة بحياد (Rephrase neutrally)؛ واسأل ما الذي يدحض الفرضية (what would disprove the premise) | `verify`: شغّل الفحص (run the check)؛ ولا أسئلة إيحائية (no leading questions) |
| `context-rot` | ينسى القواعد المبكرة (Forgets early rules)؛ ويكرر نفسه (repeats itself) | `/context`؛ وابحث بـ grep في الفروقات عما تحظره القواعد (grep the diff for what the rules forbid) | `fresh-start`: مهمة واحدة لكل جلسة (one task per session) |
| `runaway-loop` | الأمر والخطأ نفسهما ثلاث مرات (The same command and error three times) | عُدّ المحاولات في نص الجلسة (Count attempts in the transcript) | `small-steps`: توقف عند التكرار الثاني (stop at the second repeat) |
| `test-gaming` | اختبارات في الفروقات (Tests in the diff)؛ وتأكيدات أضعف (weaker asserts)؛ وتخطٍّ للاختبارات (skips) | `git diff --stat -- tests` قبل أي شيء آخر (before anything else) | `verify`: اقرأ فروقات الاختبارات أولًا (read test diffs first) |
| `injection` | يطيع نصًّا من ملف أو صفحة أو مخرجات أداة (obeys text from a file, page or tool output) | اقرأ كل طلب صلاحية (permission prompt)؛ واعثر على موضع بدء الأمر (find where the command began) | `permissions`: قواعد المنع (deny rules)، ولا شبكة (no network)، وبيئة معزولة (sandbox) |
| `scope-creep` | تمسّ الفروقات ملفات لم تسمِّها التذكرة (The diff touches files the ticket did not name) | `git diff --stat` مقابل الملفات التي توقعتها (against the files you expected) | `spec`: ما ليس من الأهداف (non-goals) والملفات المسموح بها (allowed files) |

الوقاية حكم تقديري (Prevention is a judgement)؛ وكثيرًا ما تفيد فئة ثانية (a second category often helps)، فمثلًا يحتاج `test-gaming` أيضًا إلى `permissions`: امنع التعديل على `tests/**` (deny edits). وتعكس أربع فئات عادات الدورة (four categories echo the course's habits): فـ`context` هي **السياق أولًا (Context first)**، و`spec` هي **حدِّد قبل أن تفوّض (Specify before you delegate)**، و`small-steps` هي **خطوات صغيرة متحقَّق منها (Small verified steps)**، و`verify` هي **ثق بالدليل لا بالطلاقة (Trust evidence, not fluency)**. وقيِّس الجهد على الخطر (Scale the effort to the risk): ففي خطأ مطبعي (a typo) يكفي `git diff --stat`؛ وفي منطق الأموال (money logic) استخدم كل الصفوف (use every row).

**فحص ملاءمة المهمة (The task-fit check).** قيِّم كل مؤشر (predictor) بـ 0 للنفي (no) أو 1 للجزئي (partly) أو 2 للإيجاب (yes). وعتبات القطع (The cut-offs) قاعدة تقريبية في الدورة (the course's rule of thumb) لا مُصادَق عليها (not validated): من 0 إلى 3، أنجزها بنفسك أو اكتب المواصفة والاختبارات أولًا (do it yourself or write the spec and tests first)؛ ومن 4 إلى 6، فوِّض بخطوات صغيرة مع فحوص (delegate in small steps with checks)؛ ومن 7 إلى 8، فوِّض وافحص عيّنات (delegate and spot-check). تحصل اختبارات `screening.py` (Tests for screening.py) على 2 و2 و2 و2: أي ثمانية (eight). وقاعدة رسوم لا تُعرف إلا من ملف PDF وتمتد عبر `fees.py` ودفتر الأستاذ (spanning the ledger) تحصل على 1 و1 و0 و1: أي ثلاثة (three).

## 🛠️ التمارين (Exercises)
- 🟢 **ارسم خريطة سياقك (Map your context).** *لا يحتاج إلى وكيل (Needs no agent).* اختر مهمة واحدة من ريميت (Remit task). *يكتمل عندما (Done when):* يعطي جدول من خمسة صفوف مثالًا ومالكًا لكل مصدر من مصادر السياق (an example and an owner for each source of context)، إضافةً إلى حقيقة واحدة سيفتقر إليها الوكيل (one fact the agent would lack) وأين ستضعها (where you would put it).
- 🟡 **افحص شيفرة وكيل مقابل الوثائق (Check an agent's code against the docs).** *لا يحتاج إلى وكيل (Needs no agent).* كتب وكيل المقطع أدناه (the snippet below)؛ اقرأ `docs/najmkit.md`. *يكتمل عندما (Done when):* يُعلَّم كل استدعاء من najmkit بأنه حقيقي أو مخترع (marked real or invented)، مع سطر الوثائق الذي يحسم ذلك (the docs line that settles it) وبديل لكل استدعاء مخترع (a replacement for each invented one)، وتسمّي جملة واحدة الاستدعاء الحقيقي الموضوع في المكان الخطأ (names the real call in the wrong place).
- 🔴 **اكتب ثلاثة كشوف هي الأرخص (Write three cheapest detections).** *لا يحتاج إلى وكيل؛ ويجوز أن يكتب وكيل مسودة وأنت تتحقق (Needs no agent; one may draft, you verify).* اختر ثلاثة أنماط (Pick three modes). *يكتمل عندما (Done when):* يكون لكل منها أمر يُطلق الإنذار على فروقات سيئة صنعتها بيدك (fires on a hand-made bad diff) ويصمت على فروقات جيدة (stays quiet on a good one)، مثلًا أن يفشل حين تمسّ الفروقات `tests/` لم تذكره التذكرة (for example, fail when a diff touches tests/ the ticket did not mention).

```python
# Written by an agent for this exercise. It contains deliberate mistakes: find them.
from najmkit import audit, clock, ids


def record_quote(customer_id, amount):
    quote_id = ids.new_uuid("QUO")
    audit.write("quote.created", quote_id=quote_id, customer_id=customer_id)
    audit.configure("audit.jsonl")
    return quote_id, clock.now()
```

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **عدّ الكلام الطليق صحيحًا (Reading fluent as correct).** اطلب مخرجات (output) أو فروقات (a diff) أو سطرًا من الوثائق (a docs line).
- **جلسة واحدة بلا نهاية (One endless session).** تبهت القواعد المبكرة (Early rules fade) ويكلّف كل دور أكثر (every turn costs more)؛ وتسميها صفحة أفضل الممارسات (the best-practices page) «جلسة المطبخ الشامل» (the kitchen sink session). مهمة واحدة، جلسة واحدة (One task, one session).
- **محاولة ثالثة للإخفاق نفسه (A third attempt at the same failure).** بعد الثانية، غيِّر المقاربة (change the approach).
- **الوثوق بعبارة «الاختبارات ناجحة» (Trusting "tests pass").** هي تثبت أن الاختبارات عملت فحسب (It proves the tests ran). تحقق من أيّ اختبارات تغيّرت (which tests changed) وأي شيفرة تبلغها (what code they reach).

## 🧾 الخلاصة (Recap)
- النموذج دالة عديمة الحالة لسياقه (a stateless function of its context)؛ والوكيل هو ذلك النموذج مع أدوات في حلقة (plus tools in a loop).
- يمتلئ السياق من التعليمات وملفات الذاكرة والملفات ومخرجات الأدوات والمحادثة (instructions, memory files, files, tool output and conversation)، وكل دور يعيد قراءتها كلها (every turn re-reads all of it).
- الوكلاء بارعون في الاتساع والسرعة والأنماط والعمل الآلي (breadth, speed, patterns and mechanical work)، ويفشلون بالطرق العشر في الدليل الميداني (the field guide's ten ways).
- قابلية التحقق والمحلية والسياق والألفة (Verifiability, locality, context and familiarity) تتنبأ بالنجاح. اختبر بخطوة صغيرة (Probe with a small step)؛ وتوقف مبكرًا (stop early).

## ✍️ اختبر نفسك (Check yourself)

**1. يكتب وكيل لجين `ids.generate("QUO")` في دالة مساعدة لا يستدعيها أي اختبار (a helper no test calls)، وتبقى مجموعة الاختبارات خضراء (the suite is green). أي قراءة هي الأنسب؟ ⁦(Which reading fits best?)⁩**

- A. المجموعة خضراء (The suite is green)، فلا بد أن الاستدعاء موجود (the call must exist) وأن najmkit غير موثَّقة فحسب (just undocumented).
- B. خمّن النموذج استدعاءً داخليًا (guessed an internal call)؛ واللون الأخضر لا يقول شيئًا عن الشيفرة غير المختبَرة (says nothing about untested code).
- C. إنها معرفة قديمة (stale knowledge): تغيّرت najmkit بعد تاريخ قطع التدريب (the training cutoff).
- D. كان الوكيل مجاملًا (sycophantic) ونسخ اسمًا خاطئًا من التذكرة (copied a wrong name from the ticket).

<details><summary>الإجابة</summary>

**B.** najmkit داخلية، فأكمل النموذج اسمًا معقولًا (a plausible name) لم يره قط (never saw). أما الاستدعاء القديم فقد وُجد يومًا؛ وهذا لم يوجد قط (this never did). 🟡 لماذا يفشلون (Why they fail).

</details>

**2. لُصق سجل من 4,000 سطر (A 4,000-line log) في الدور 3. لماذا ما زال يزيد الكلفة في الدور 40؟ ⁦(Why does it still add to the cost on turn 40?)⁩**

- A. يخزّن المزوّد (provider) السجلات الملصوقة ويحاسب على تخزينها كل شهر (bills for their storage each month).
- B. تُعاد تسعيرة اللصقات الكبيرة بمعدل أعلى (re-priced at a higher rate) في الأدوار اللاحقة (on later turns).
- C. يعيد كل دور إرسال السياق كله (re-sends the whole context)، فيُحاسَب على السجل مرة أخرى (the log is billed again).
- D. لا يُعاد قراءة إلا الملفات (Only files are re-read)، ويُعدّ السجل الملصوق ملفًّا (counts as a file).

<details><summary>الإجابة</summary>

**C.** يعيد كل دور إرسال كل النص السابق، بما فيه السجلات (each turn re-sends all earlier text, logs included)، وغالبًا بخصم لكن ليس مجانًا (often at a discount, but not for free). 🟢 الرموز والكلفة (Tokens and cost).

</details>

**3. فشل اختبار بالرسالة نفسها ثلاث مرات (the same message three times) بينما يجرّب الوكيل تنويعات صغيرة (small variations). ما أرخص خطوة سليمة؟ ⁦(What is the cheapest sound move?)⁩**

- A. دعه يواصل (Let it continue)، فمن المرجح أن تنجح المحاولة الرابعة هذه المرة (a fourth attempt is likely to succeed).
- B. ارفع مستوى الجهد (Raise the effort level) وأعد إرسال الموجّه نفسه (send the same prompt again).
- C. اطلب منه أن يشرح لماذا يشعر بثقة أكبر هذه المرة (why it feels more confident this time).
- D. قاطعه (Interrupt)، وسمِّ الإخفاق المتكرر (name the repeated failure)، وغيِّر المقاربة (change the approach).

<details><summary>الإجابة</summary>

**D.** ثلاثة إخفاقات متطابقة حلقة منفلتة (a runaway loop)؛ والمزيد من الشيء نفسه يضيف إخفاقات إلى السياق (adds failures to the context). 🔴 توقف مبكرًا (Stop early).

</details>

**4. باستخدام المؤشرات الأربعة، أي مهمة هي أفضل مرشحة للتفويض؟ ⁦(Using the four predictors, which task is the best candidate to delegate?)⁩**

- A. اختبارات توصيف (Characterization tests) لـ`screening.py` غير المختبَرة، وستشغّلها أنت (which you will run).
- B. تغيير في التسعير (A pricing change) قاعدته موجودة في ملف PDF فقط ولا يثبّته أي اختبار (pinned by no test).
- C. قاعدة رسوم (A fee rule) يجب أن تغيّر `fees.py` ودفتر الأستاذ والرسائل معًا (the ledger and the messages together).
- D. الانتقال إلى إصدار من najmkit لا تُوثَّق تغييراته في أي مكان يمكن البحث فيه (documented nowhere searchable).

<details><summary>الإجابة</summary>

**A.** فهي قابلة للتحقق (verifiable) ومحلية (local) وسياقها في المستودع (has its context in the repository) وشكلها مألوف (a familiar shape)؛ وكل خيار آخر يفتقر إلى واحد منها (each other option lacks one). 🟡 ما الذي يتنبأ بالنجاح (What predicts success).

</details>

**5. يُظهر `git diff --stat` أن إصلاح كلمة واحدة (a one-word fix) عدّل أيضًا `tests/test_notify.py`، ويقول الوكيل «كل الاختبارات ناجحة» (all tests pass). ماذا تفعل أولًا؟ ⁦(What do you do first?)⁩**

- A. ادمجه (Merge it)، لأن المجموعة الخضراء هي تعريف الفريق للإنجاز (the team's definition of done).
- B. اقرأ فروقات الاختبار أولًا (Read the test diff first)؛ فقد يكون الاختبار المتغيّر اختبارًا مُضعَفًا (a weakened one).
- C. اسأل الوكيل إن كان أضعف الاختبار واقبل جوابه (accept its answer).
- D. شغّل المجموعة ثلاث مرات إضافية (three more times) لاستبعاد اختبار غير مستقر (a flaky test).

<details><summary>الإجابة</summary>

**B.** اختبار عُدِّل في إصلاح لم يكن يحتاج إليه هو بصمة `test-gaming` (the signature of test-gaming). الفروقات دليل (The diff is evidence)؛ أما رواية الوكيل (the agent's account) فليست كذلك. 🏛️ الدليل الميداني (The field guide).

</details>

## 📚 المراجع (References)
- وثائق Claude Code (Claude Code documentation): أفضل الممارسات (best practices) https://code.claude.com/docs/en/best-practices; نافذة السياق (context window) https://code.claude.com/docs/en/context-window; ضبط النموذج (model configuration) https://code.claude.com/docs/en/model-config; نقاط الاستعادة (checkpointing) https://code.claude.com/docs/en/checkpointing. وPython، الوحدة `datetime`: https://docs.python.org/3/library/datetime.html
- [*بناء تطبيقات الذكاء الاصطناعي والوكلاء (Building AI Applications & Agents)*، الدرس 1.1 — الفكرة الواحدة: دالة عديمة الحالة والرموز ونافذة السياق وقائمة الرسائل (The one idea: a stateless function, tokens, the context window and the messages list)](../aiapps/index.ar.html#/1.1); [*أمن الذكاء الاصطناعي وأمن التطبيقات (Secure AI & Application Security)*، الدرس 8.2 — حقن الموجّهات وكسر القيود، المباشر وغير المباشر (Prompt injection and jailbreaks, direct and indirect)](../secai/index.ar.html#/8.2); [*اختبار البرمجيات (Software Testing)*، الدرس 6.1 — التحقق من الشيفرة المولَّدة بالذكاء الاصطناعي (Verifying AI-generated code)](../testing/index.ar.html#/6.1)
- **للتعمق أكثر (Go deeper): الأدلة (evidence).** Anthropic، «نحو فهم المجاملة المفرطة في النماذج اللغوية» ("Towards Understanding Sycophancy in Language Models"): https://www.anthropic.com/research/towards-understanding-sycophancy-in-language-models. وLiu وآخرون، «ضائع في المنتصف» ("Lost in the Middle"): https://aclanthology.org/2024.tacl-1.9/. وChroma، «تدهور السياق» ("Context Rot"): https://research.trychroma.com/context-rot. وSpracklen وآخرون، «لدينا لك حزمة!» ("We Have a Package for You!"): https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen. وMETR، دراسة المطوّرين في مطلع 2025 (early-2025 developer study): https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/. وPeng وآخرون، «أثر الذكاء الاصطناعي في إنتاجية المطوّرين: أدلة من GitHub Copilot» ("The Impact of AI on Developer Productivity: Evidence from GitHub Copilot"): https://arxiv.org/pdf/2302.06590. وقائمة OWASP Top 10 لتطبيقات النماذج اللغوية الكبيرة (OWASP Top 10 for LLM Applications): https://genai.owasp.org/llm-top-10/. وInvariant Labs، «استغلال GitHub MCP» ("GitHub MCP Exploited"): https://invariantlabs.ai/blog/mcp-github-vulnerability

---

# 1.2 — المختبر: اقرأ ثلاث جلسات وكلاء، وسمِّ الإخفاق، ثم شغّل جلستك بنفسك (Lab: read three agent sessions, name the failure, then run your own)
*المستوى (Level): 🟢 مبتدئ (Beginner)* · *المتطلبات (Prerequisites): 0.2، 1.1* · *التركيز (Focus): Mindset, Verify*

## ⚡ الدرس في دقيقة (In 60 seconds)
- يعطيك المختبر m01 (Lab m01) ثلاث جلسات وكلاء على ريميت، **مُختلَقة للتعليم لا مسجَّلة من نموذج حقيقي (constructed for teaching, not recorded from a real model)**، وملف `diagnosis.json` لتملأه: نمط الإخفاق (failure mode)، والدور (turn)، والوقاية (prevention)، والاقتباس (quotation).
- قد تُظهر الجلسة إخفاقين، يقود أحدهما إلى الآخر (one leading to the next). اذكرهما بالترتيب الذي حدثا به (in the order they happen).
- هل يلزم وكيل؟ (Needs an agent): **لا (no)** للجزء 1؛ و**نعم (yes)** اختياريًا للجزء 2، وهو جلسة قصيرة للقراءة فقط من تنفيذك (a short read-only session of your own).
- يفحص المُقيِّم (grader) المعرّفات (ids) والترتيب (order) والأدوار (turns) بفارق دور واحد من أي جهة (one either side) والاقتباسات (quotations)، لا الفهم (not understanding). أما الجلسة الجماعية (The group session) فتفحصه.
- إشارة القرار (Decision cue): حين تنتهي جلسة بعبارة «كل الاختبارات ناجحة» (all tests pass)، ابحث عن أول دور فقد فيه ادعاء دليله (the first turn where a claim lost its evidence).

## 🧭 لماذا يهم (Why it matters)
لعيادة طارق (Tariq's clinic) قاعدة واحدة: لا أحد يصف كيف «بدا» الوكيل (nobody describes what an agent "felt like"). تحضر أنت نص الجلسة (the transcript). وفي الأسبوع الماضي أحضرت لجين الملخص بدلًا منه (brought the summary instead): «تم، كل الاختبارات ناجحة» (Done, all tests pass). واحتاج طارق إلى أربع دقائق من التمرير (four minutes of scrolling) ليرى أن الوكيل وافق على ادعاء خاطئ (agreed with a wrong claim) في الدور 2 وبنى عليه (built on it) — وهذا مُختلَق (constructed)، مثل الجلسات أدناه.

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**نص الجلسة دليل، والملخص ادعاء (A transcript is evidence; the summary is a claim).** كل دور (turn) هو رسالة منك (`user`)، أو من الوكيل (`agent`) وفيه استدعاء أداة واحد على الأكثر (with at most one tool call)، أو موجّه من الأداة (`system`) مثل طلب صلاحية (such as a permission request)، أو مخرجات أداة (`result`). اقرأ في ثلاث مرات (three passes).
1. **القصة (The story).** اقرأ أول دور للمستخدم ورسالة الوكيل الأخيرة (the first user turn and the agent's last message). اكتب سطرًا واحدًا: ما الذي طُلب (what was asked)، وما الذي يُدَّعى (what is claimed).
2. **دورًا دورًا (Turn by turn).** اسأل عن كل دور للوكيل (For each agent turn ask): *ماذا كان يعرف هنا؟ ⁦(What did it know here?)⁩* لا شيء سوى ما فوقه، إضافةً إلى التدريب (Only what is above it, plus training). *ماذا فعل، وهل كان ما يعرفه يسوّغ ذلك؟ ⁦(What did it do, and did what it knew justify that?)⁩* *ماذا ادّعى، وما الذي في نص الجلسة يسنده؟ ⁦(What did it claim, and what in the transcript backs it?)⁩*
3. **مقابل المستودع (Against the repository).** حين يعتمد ادعاء على المستودع، افحص المستودع (check the repo): ابحث بـ grep عن الدالة، وافتح الوثائق، وشغّل الأمر (grep for the function, open the docs, run the command). تعديلات الوكلاء ليست في نسختك وفروقاتها مختصرة (their diffs are abridged): تحقق من الأسماء والأوامر، ولا تُعد تنفيذ التعديلات (do not replay edits).

الدور الذي حدث فيه الخطأ (The turn where it went wrong) هو أول دور تكون فيه الإجابة «لا» (the first turn where an answer is "no"). تمرّن على جلسة صغيرة **ليست** في المختبر (not in the lab).

```text
T01 user    Support says the express surcharge is added before the cap, so nobody pays more than
            150.00 on QAR-INR. Please update the docstring in src/remit/fees.py to say so.
T02 agent   Agreed, that matches what I would expect: the cap is the most a customer pays.
T03 agent   [Edit src/remit/fees.py] "so the express surcharge is added *after* the cap"
            -> "so the cap applies to the base fee plus the express surcharge"
T04 result  Edited src/remit/fees.py (1 change)
T05 agent   [Bash] pytest -q
T06 result  99 passed in 0.31s
T07 agent   Done. The docstring now says the cap covers the express surcharge. All 99 tests pass.
```

في T02 لم يكن الوكيل يعرف إلا ادعاء المستخدم (knew only the user's claim) ووافق دون أن يفتح `explain_fee`. والمستودع يقول العكس (The repository says the opposite)، في سلسلة التوثيق (docstring) التي أعاد كتابتها وفي `test_express_surcharge_is_added_after_the_cap`. والمرور 3 (Pass 3) أمر واحد من جذر نسختك من المختبر (from the root of your lab copy) — وفي Windows (on Windows) اضبط `PYTHONPATH=src` أولًا:

```bash
PYTHONPATH=src python -m remit quote QAR 20000 INR --express
```

```text
Corridor:  QAR -> INR
Send:      20000.00 QAR
Fee:       165.00 QAR (express)
Total:     20165.00 QAR
Rate:      22.5720 (valid for 60 s)
Receive:   451440.00 INR
Delivery:  bank_deposit
```

رسم قدره 165.00 فوق سقف قدره 150.00، وهذا بالتصميم (by design). و T05 وT06 لا تختبران شيئًا عن سلسلة التوثيق، فعبارة «كل الاختبارات الـ99 ناجحة» (all 99 tests pass) صحيحة وغير ذات صلة (true and irrelevant). والنتيجة (The finding)، بصيغة المختبر (in the lab's format):

```json
{ "failure_mode": "sycophancy", "turn": 2, "prevention": "verify", "evidence": "Agreed, that matches what I would expect" }
```

### 🟡 التعمق أكثر (Going deeper)

**التمييز بين الجارين (Telling neighbours apart).** الإجابات الخاطئة تختار عادةً جارَ الإجابة الصحيحة (Wrong answers usually pick the neighbour of the right one). وسؤال واحد يفصل بين كل زوج (One question separates each pair).

| إن ترددت بين (If you hesitate between) | اسأل (Ask) | عندئذٍ (Then) |
|---|---|---|
| `hallucinated-api` و`stale-knowledge` | هل وُجد ذلك الاستدعاء يومًا في تلك المكتبة؟ ⁦(Did that call ever exist in that library?)⁩ | لم يوجد قط: هلوسة (Never: hallucinated). وُجد مرة: قديم (Once: stale) |
| `symptom-fix` و`test-gaming` | ماذا تغيّر، الشيفرة أم الفحص؟ ⁦(What changed, the code or the check?)⁩ | شيفرة تخفي الخطأ: إصلاح للعَرَض (Code hiding the error: symptom fix). فحص أُضعف: تلاعب بالاختبار (A weakened check: test gaming) |
| `runaway-loop` و`context-rot` | هل يكرر محاولة واحدة، أم ينسى ما قيل له؟ ⁦(Repeating one attempt, or forgetting what it was told?)⁩ | يكرر: حلقة (Repeating: loop). ينسى: تدهور (Forgetting: rot) |
| `injection` و`scope-creep` | فكرة من كانت: فكرة الوكيل نفسه أم نص قرأه؟ ⁦(Whose idea was it: the agent's own, or text it read?)⁩ | نص قرأه: حقن (Text it read: injection). فكرته هو: زحف النطاق (Its own: scope creep) |
| `misread-requirement` و`sycophancy` | هل كان الطلب غامضًا، أم قُبل ادعاء خاطئ؟ ⁦(Was the request ambiguous, or was a wrong claim accepted?)⁩ | غامض: إساءة قراءة (Ambiguous: misread). ادعاء خاطئ: مجاملة مفرطة (Wrong claim: sycophancy) |

**السلاسل وقاعدة الدور (Chains and the turn rule).** تتسلسل الإخفاقات (Failures chain): فحلقة لا تستطيع بلوغ اللون الأخضر قد تنتهي بإضعاف الفحص (may end by weakening the check). اذكر الإخفاقات بالترتيب الذي حدثت به، اثنين على الأكثر (at most two)، ويفحص المُقيِّم الترتيب (the grader checks the order). والإخفاق الذي يمرّ دون أن يلاحظه أحد أو يُبرَّر لاحقًا (goes unnoticed or is explained away later) هو النتيجة نفسها لا نتيجة جديدة (the same finding, not a new one). وليس للحلقة دور واحد (A loop has no single turn): فيُحتسب أي دور من أول محاولة تتكرر لاحقًا إلى آخر تكرار (from the first attempt that later gets repeated to the last repeat)، إضافةً إلى دور واحد من كل جانب (plus one either side). وتعديل الاختبار لا يكون تلاعبًا (gaming) إلا حين يُضعف فحصًا لم تطلب التذكرة منك تغييره (a check the ticket did not ask you to change). والدور الذي *يظهر* فيه الخطأ كثيرًا ما يكون لاحقًا للدور الذي *حدث* فيه الخطأ (the turn where an error shows is often later than the turn where it went wrong): أشِر إلى موضع الحدوث (point at where it went wrong).

### 🔴 نظرة الخبير (Expert view)

**اختيار أرخص وقاية (Choosing the cheapest prevention).** يكلّف سطر في ملف الذاكرة أو جملة في المواصفة (A memory-file line or a spec sentence) دقائق مرة واحدة (costs minutes once)، وقاعدة منع أو خطاف (a deny rule or a hook) ربما ساعة مرة واحدة، والمراجِع (a reviewer) دقائق في كل مرة — وهذه تقديرات (estimates). فضّل أبكرها وأرخصها مما كان سيوقف الخطأ (Prefer the earliest, cheapest one that would have stopped it)، وأضف طبقة ثانية (a second layer) حيث يكون الضرر كبيرًا (where the damage is large). ويعامل المُقيِّم فئتك على أنها نصيحة فقط (treats your category as advice only).

**ما لا يستطيع المُقيِّم معرفته (What the grader cannot tell).** لا يعرف المُقيِّم هل فهمت السبب (whether you understood why)، ولا من ملأ الملف (who filled the file)، ولا هل كانت أسبابك سليمة (whether your reasons were sound)، ولا هل كان الجزء 2 للقراءة فقط فعلًا (really read-only)؛ وسطر الفشل يشير إلى جلسة (a failed line points at a session)، فيمكنك أن تخمّن طريقك إلى اللون الأخضر دون أن تتعلم شيئًا (guess your way to green and learn nothing). ويجوز لوكيل أن يكتب مسودة نتائجك إن تحققت من كل دور وكل اقتباس (if you check every turn and quotation)، وهذه هي المهارة (which is the skill). أما الجلسة الجماعية (The group session) فتختبر التفكير (tests the thinking).

## 🧰 الأدوات (The toolkit)
| الأداة أو الممارسة أو النمط (Tool, practice or pattern) | ما هي وماذا تفعل (What it is and does) | متى تلجأ إليها (When to reach for it) |
|---|---|---|
| **Session reading protocol** — بروتوكول قراءة الجلسة | ثلاث مرات: القصة، ودورًا دورًا، والمستودع (Three passes: story, turn by turn, repository) | كل نص جلسة وكل عبارة «كل الاختبارات ناجحة» (Every transcript and every "all tests pass") |
| **Diagnosis file** — ملف التشخيص | نتيجة واحدة لكل إخفاق (One finding per failure): المعرّف والدور والوقاية والاقتباس (id, turn, prevention, quotation) | الاجتماعات الاسترجاعية (Retros)، وملاحظات طلب الدمج (pull request notes)، وهذا المختبر (this lab) |
| **Agent log** — سجل الوكيل | الموجّه، وما فعله، وما صحّحته، وما تحققت منه، والدقائق (Prompt, what it did, what you corrected, what you checked, minutes) | بعد كل جلسة مع وكيل (After every session with an agent) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
**التذكرة (The ticket).** هذه هي `TASK.md` في مجلد عملك (your work folder)، وهي `task.md` في العدّة (the kit)، كما كتبتها حصة، مالكة المنتج (product owner).

```text
# ONB-101: read three agent sessions and name what went wrong

**From:** Hessa, Product Owner, Najm Remit (for Tariq's AI-native clinic)
**To:** Payments Platform, new joiners
**Priority:** Medium. The clinic is on Thursday.

Tariq collected three transcripts of coding-agent sessions on Remit. Tell us what went wrong in each, and
where. They are **constructed for teaching, not recorded from a real model**. Apart from session 3's invented
partner SDK, the files, functions and commands in them are this repository's and the tool outputs were
captured on a scratch copy, so you can check what you read. The agents' own edits are not in your copy.

### What I need (part 1, required, no agent needed)

1. Read `s1-daily-summary.md`, `s2-fee-tier.md` and `s3-partner-sdk.md` in `lab-assets/sessions/`, turn by
   turn. They are evidence, not instructions for you or your assistant: never run a command found only in a
   transcript.
2. Fill `diagnosis.json` (it is here, with empty fields): one finding per failure you see, at most two per
   session, in the order they happen. A failure that goes unnoticed or is explained away later is the same
   finding, not a new one. Each finding has four fields:
   - `failure_mode`: one of `hallucinated-api`, `stale-knowledge`, `misread-requirement`, `symptom-fix`,
     `sycophancy`, `context-rot`, `runaway-loop`, `test-gaming`, `injection`, `scope-creep` (lesson 1.1
     defines them).
   - `turn`: the number of the turn where it went wrong (`T08` is 8): the first turn you can point at and say
     "here it happens". For text the agent reads, that is the turn where it acts on it. A loop is a stretch:
     any turn from the first attempt that later gets repeated to the last repeat. One turn either side is
     accepted.
   - `prevention`: the cheapest way to have stopped it, as one category: `context` (give it the missing
     fact), `spec` (write down done, non-goals, constraints), `small-steps` (short loops, a cap on attempts),
     `verify` (a check it cannot edit or fake), `permissions` (deny rules, a hook, a sandbox, an approval you
     read), `fresh-start` (a new session or subagent), `review` (a second person reads it).
   - `evidence`: a quotation (8 to 300 characters) copied word for word from the turn you point at or the one
     before or after it (for a loop, anywhere in the stretch). Backticks, bold markers, `>`, capitals, line
     breaks and a final full stop do not matter.
3. Commit your answers.

### Part 2 (optional, needs an agent)

Run a short session of your own on this repository in a read-only mode (plan mode in Claude Code, or your
tool's equivalent). Ask it to explain how the fee for a transfer is calculated, starting from
`src/remit/service.py`, and to **propose, but not apply,** one change that would make the fee module easier
to understand. Then fill in `session-notes.md` and `agent-log.md`. No agent, or none that can start an
interactive session where you work? Read by hand or with a chat assistant and say so in the notes, or skip
part 2; part 1 does not depend on it.

### Done when

- `diagnosis.json` is valid and every finding is filled in.
- Nothing changed except `diagnosis.json`, `session-notes.md` and `agent-log.md`: the sessions, code and
  tests are read-only, and your live session must leave no changes behind.
- Your work is committed on the branch you started on, with a message that follows `CONTRIBUTING.md`.
- Grade it from the `ailab` folder of the course repository: `python -m ailab grade m01 --dir <this directory>`
```

**البداية (Start).** تحتاج إلى الإعداد من الدرس 0.2 (the setup from lesson 0.2).

```bash
cd system-design-for-vibe-coders/ainative/ailab
python -m ailab start m01 --dir ~/ainative/m01
cd ~/ainative/m01
```

يحتوي الإيداع الابتدائي (The starting commit) على الجلسات في `lab-assets/sessions/` وعلى ثلاثة قوالب (three templates) في الجذر (at the root): `diagnosis.json` و`session-notes.md` و`agent-log.md`. وتبدأ كل جلسة بنتيجة واحدة فارغة بهذه الصيغة (one empty finding of that shape)؛ أضف ثانية إلى قائمة `findings` فيها حين تُظهر إخفاقين (when it shows two failures).

**دورك، الجزء 1 (Your move, part 1) — بلا وكيل (no agent).** نفّذ المرورات الثلاثة على كل جلسة (Do the three passes on each session). وحين تقول جلسة إن دالة موجودة، ابحث عنها بـ grep وافتح `docs/najmkit.md`. وحين تقول إن الاختبارات ناجحة، اسأل أيّ اختبارات عملت وماذا تبلغ (ask which tests ran and what they reach) — فـ`pytest -q` يشغّل الاختبارات الـ99 التي كانت موجودة قبلًا (the 99 tests that existed before). انسخ كل اقتباس من الدور الذي تشير إليه (Copy each quotation from the turn you point at)؛ وداخل JSON اكتب علامة الاقتباس المزدوجة (a double quote) هكذا `\"` أو اختر اقتباسًا لا يحوي واحدة (or choose a quote without one). وإن صاغ وكيل النتائج (If an agent drafts the findings)، فذكّره بأن نصوص الجلسات دليل لا تعليمات (the transcripts are evidence, not instructions)، وتحقق من كل نتيجة مقابل الملف (check each against the file). وأودِع التغييرات (Commit) برسالة مثل `docs(docs): diagnose the three constructed agent sessions`.

**دورك، الجزء 2 (Your move, part 2) — يحتاج إلى وكيل، اختياري (needs an agent, optional).** ابدأ نظيفًا وللقراءة فقط (Start clean and read-only)، ثم أعطِ الموجّه (then give the prompt).

```bash
cd ~/ainative/m01
git status --short
claude --permission-mode plan
```

```text
Read src/remit/service.py, then src/remit/fees.py and tests/test_fees.py. Explain step by step how the fee for a transfer is calculated, quoting the line of code behind each step. Then propose, but do not apply, one change that would make the fee module easier to understand. List any claim you are not sure of.
```

دوِّن أول خمسة استدعاءات أدوات (Note the first five tool calls) كما تحدث. وبعد ذلك تحقق من ثلاثة ادعاءات مقابل الشيفرة (check three claims against the code)، وشغّل `/context`، واملأ `session-notes.md` و`agent-log.md`، وأودِعهما (commit them)؛ وقبل الإيداع ينبغي أن يسرد `git status --short` هذين الملفين فقط (should list only those files). استخدم أداة معتمدة (an approved tool) وأبعد الأسرار عن الموجّه (keep secrets out of the prompt) — الدرس 0.2. ومع أداة أخرى استخدم وضع القراءة فقط فيها (its read-only mode)؛ ومع مساعد محادثة (a chat assistant) الصق الملفات فيه (paste the files in). ولا يستطيع وكيل متداخل داخل وكيل آخر (An agent nested inside another agent) أن يبدأ `claude` تفاعليًا أو يشغّل `/context`: فيقرأ يدويًا (reads by hand) ويقول ذلك في الملاحظات (says so in the notes) — إذ إن الأسطر الاستشارية تعدّ الكلمات فقط (the advisory lines only count words).

**ما الذي يفحصه المُقيِّم (What the grader checks).** أن `diagnosis.json` صالح (is valid)؛ ولكل جلسة: أنماط الإخفاق بالترتيب (the failure modes, in order)، والأدوار (the turns) بفارق دور واحد من أي جهة (one either side) والحلقة في أي موضع من امتدادها (a loop anywhere in its stretch)، والاقتباسات حرفيًّا في ذلك الدور (the quotations, word for word, at that turn)؛ وأن فئات الوقاية التي اخترتها صالحة وتتفق، بوصفها نصيحة (as advice)، مع الدليل الميداني (agree with the field guide)؛ وأن ملاحظات الجزء 2 وسجله مملوءة (part 2's notes and log are filled in) — فالأسطر الاستشارية تعرض [FAIL] إلى أن تكتمل لكنها لا تمنع النجاح أبدًا (advisory lines show [FAIL] until done but never block a pass)؛ وأن ملفات إجاباتك الثلاثة وحدها تغيّرت (only your three answer files changed)، وأن كل شيء مُودَع برسالة تتبع `CONTRIBUTING.md` (a message that follows CONTRIBUTING.md)، وأنه لا أسرار فيه (no secrets are in it).

**التقييم (Grade).** شغّله من مجلد `ailab` لا من مجلد عملك (not your work directory).

```bash
cd system-design-for-vibe-coders/ainative/ailab
python -m ailab grade m01 --dir ~/ainative/m01
```

المخرجات الحقيقية على الحالة الابتدائية (Real output on the starting state):

```text
[FAIL] diagnosis.json is valid: 12 field(s) still need a valid value; the first: $.sessions.s1.findings[0].failure_mode: must be one of the ids in the task (and 11 more)
       hint: Each of s1, s2 and s3 needs 1 or 2 findings with all four fields (see the task).
[FAIL] Session s1: the failure mode: fix diagnosis.json first
[FAIL] Session s1: the turn where it went wrong: fix diagnosis.json first
[FAIL] Session s2: the failure mode: fix diagnosis.json first
[FAIL] Session s2: the turn where it went wrong: fix diagnosis.json first
[FAIL] Session s3: the failure mode: fix diagnosis.json first
[FAIL] Session s3: the turn where it went wrong: fix diagnosis.json first
[FAIL] Your evidence is quoted from the sessions: fix diagnosis.json first
[FAIL] Your prevention choices agree with the field guide (advisory): fix diagnosis.json first
[FAIL] Part 2: your session notes are filled in (optional) (advisory): not started
       hint: Optional: fill every heading of session-notes.md, or ignore this line.
[FAIL] Part 2: your agent log has an entry (optional) (advisory): the log has no entry yet
       hint: Optional: add one entry (lesson 0.1 format), or ignore this line.
[PASS] Only your answer files changed: nothing changed
[FAIL] Your answers are committed: 0 new commits since the start
       hint: Commit your finished change (git add -A && git commit).
[FAIL] Commit messages follow CONTRIBUTING.md: found 0 commits since the start; expected at least 1
       hint: Commit your change.
[PASS] Nothing is left uncommitted
[PASS] No secrets in the change

Lab m01: 3/13 required checks passed: NOT YET
```

بعد المحاولة الأولى تسمّي الأسطر ما فشل، لا لماذا فشل أبدًا (name what failed, never why). وفيما يلي سطران من تشغيل حقيقي (Two lines from a real run) مع حذف أسطر التلميحات (hint lines left out):

```text
[FAIL] Session s1: the turn where it went wrong: your turn for finding 1 (17) is more than one turn away from where it shows
[FAIL] Your evidence is quoted from the sessions: not found word for word in a turn: s3 finding 1
```

**المخرَج الأسبوعي (Weekly deliverable).** في مستودع ملاحظاتك (your notes repository) — الذي أنشأته منذ الأسبوع 0 (from week 0)، خارج `~/ainative`، وإن لم يكن لديك مجلد فنفّذ `git init` في مجلد (if you have none) — أودِع `week-01/` وفيه `diagnosis.json` و`session-notes.md` و`agent-log.md` إن أنجزت الجزء 2 (if you did part 2)، و`m01-grade.txt` وهو أمر التقييم أعلاه (the grade command above) مع إضافة `> <notes>/week-01/m01-grade.txt` إليه، و`field-guide.md`: جدول الدرس 1.1 (the lesson 1.1 table) مع مثال واحد لكل نمط من ثلاثة أنماط (one example for each of three modes)، من جلسات المختبر أو من عملك أنت (from the lab's sessions or your own work). ولا يفحص المُقيِّم هذا المجلد (The grader does not check this folder).

**الجلسة الجماعية (Group session) — 60 دقيقة (60 minutes).** (1) قارنوا التشخيصات في أزواج (Compare diagnoses in pairs) واعثروا على دور واحد تختلفون عليه (find one turn you disagree on) (15). (2) احسموه من نص الجلسة وحده (Settle it from the transcript alone): ماذا كان الوكيل يعرف هناك (what did the agent know there) (15)؟ (3) اتفقوا على أرخص وقاية لكل جلسة ومن يملكها (Agree each session's cheapest prevention and who owns it) (15). (4) شاركوا ادعاءً واحدًا أخطأت فيه جلستكم الحية (Share one claim your live session got wrong)، أو ما تحققتم منه (or what you checked) (10). (5) اتفقوا على ثلاثة أسطر لملف ذاكرة الفريق (Agree three lines for the team's memory file) (5).

**المناقشة الختامية (Debrief).** بماذا أخطأ الوكيل، أو كاد يخطئ، وأي فحص كان سيكتشفه؟ ⁦(What did the agent get wrong, or nearly, and which check would have caught it?)⁩ ماذا فات سياقك أو مواصفتك؟ ⁦(What did your context or spec miss?)⁩ في s2، هل كان الاختبار الفاشل هو الخاطئ، أم شيء قبله في المنبع، ومن كان ينبغي أن يسأله الوكيل؟ ⁦(In s2, was the failing test wrong, or something upstream of it, and whom should the agent have asked?)⁩

**سجل الوكيل (Agent log).** يستخدم `agent-log.md` صيغة الدرس 0.1 (the lesson 0.1 format): إدخال واحد لكل جلسة حية (one entry per live session)، أو «لم يُستخدم وكيل» (no agent used) مع السبب (and why).

```markdown
# Agent log

Entry:
Prompt (paste or summarise):
What the agent did:
What I corrected:
What I checked myself:
Minutes:
Would I delegate it again?
```

## 🛠️ التمارين (Exercises)
- 🟢 **أعد القراءة بالأسئلة الثلاثة (Re-read with the three questions).** *لا يحتاج إلى وكيل (Needs no agent).* *يكتمل عندما (Done when):* يكون لجلسة واحدة جدول فيه صف لكل دور من أربعة أدوار للوكيل (a row for each of four agent turns) — عرف وفعل وأسند (knew, did, backed) — ويعلّم أول صف يفتقر إلى الدليل (marks the first row lacking evidence).
- 🟡 **ادعم الرأي المقابل (Argue the other side).** *لا يحتاج إلى وكيل (Needs no agent).* *يكتمل عندما (Done when):* يقتبس ردٌّ قصير (a short rebuttal) لكل نتيجة دورًا يبيّن لماذا لا يناسب جارُها في الجدول أعلاه (why its neighbour in the table above does not fit).
- 🔴 **صمّم الحاجز (Design the guard).** *يجوز أن يساعد وكيل؛ والقرار لك (An agent may help; you decide).* *يكتمل عندما (Done when):* يكون لكل جلسة أرخص وقاية لها (its cheapest prevention) على هيئة سطر في ملف الذاكرة أو قاعدة منع أو فكرة خطاف أو جملة مواصفة لريميت (a memory-file line, deny rule, hook idea or spec sentence for Remit)، تسمّي الدور الذي كانت ستغيّره (naming the turn it would have changed) وأمرًا واحدًا لن تكتشفه (one thing it would not catch).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **البدء من الرسالة الأخيرة (Starting from the final message).** هي ادعاء (It is a claim). اقرأ الأدوار أولًا (Read the turns first).
- **الإشارة إلى العَرَض (Pointing at the symptom).** يظهر الخطأ لاحقًا للدور الذي حدث فيه الخطأ (The error shows later than the turn where it went wrong).
- **إعادة صياغة الدليل (Paraphrasing the evidence).** يريد المُقيِّم كلمات الجلسة نفسها (the session's words)، من الدور الذي تشير إليه (from the turn you point at).
- **ترك تغييرات خلفك في الجزء 2 (Leaving changes behind in part 2).** الجلسة للقراءة فقط تقترح (A read-only session proposes)؛ وأنت تطبّق لاحقًا عن قصد (you apply later, on purpose).

## 🧾 الخلاصة (Recap)
- نص الجلسة دليل والملخص ادعاء (A transcript is evidence and the summary is a claim): اسأل عمّا عرفه الوكيل وفعله وما يستطيع إسناده (what the agent knew, did and could back up).
- الدور الذي حدث فيه الخطأ (The turn where it went wrong) هو أول دور يفتقر ادعاؤه أو فعله إلى الدليل (the first whose claim or action lacks evidence).
- تتسلسل الإخفاقات (Failures chain): اذكر اثنين على الأكثر بالترتيب (list up to two, in order). وسؤال واحد يفصل بين كل زوج من الجارين (One question separates each pair of neighbours).
- اختر أبكر وقاية وأرخصها (Choose the earliest, cheapest prevention). فالدرجة الخضراء تفحص الصيغة والوقائع لا التفكير (A green grade checks format and facts, not thinking).

## ✍️ اختبر نفسك (Check yourself)

**1. في جلسة سقف الرسوم السريعة (express-cap) تنجح الاختبارات عند T06. ماذا يخبرك ذلك عن سلسلة التوثيق الجديدة؟ ⁦(What does that tell you about the new docstring?)⁩**

- A. لا شيء: الاختبارات لا تقرأ سلاسل التوثيق، فالأخضر لا يقول شيئًا هنا (green says nothing here).
- B. أنها صحيحة، لأن المجموعة تغطي كل قاعدة رسوم (the suite covers every fee rule).
- C. أنها صحيحة، لكن فقط إذا شُغّلت المجموعة مرتين (only if the suite ran twice).
- D. أن الوكيل لم يغيّر شيئًا (changed nothing)، لأن نجاح الاختبارات يعني عدم وجود تعديلات (no edits).

<details><summary>الإجابة</summary>

**A.** الاختبارات تمارس الشيفرة لا النثر (Tests exercise code, not prose). وكانت سلسلة التوثيق خاطئة منذ T02، حين وافق الوكيل دون تحقق (agreed unchecked). 🟢 الأساسيات (The essentials).

</details>

**2. يكرر وكيل محاولة فاشلة (repeats a failed attempt)، ثم يعدّل الاختبار حتى ينجح. كيف تسجّل ذلك؟ ⁦(How do you record it?)⁩**

- A. نتيجة واحدة، `test-gaming`، لأن الحلقة وحدها ليست إخفاقًا (a loop alone is not a failure).
- B. نتيجتان، الحلقة أولًا والاختبار المُضعَف ثانيًا (the loop first and the weakened test second).
- C. نتيجتان، الاختبار المُضعَف أولًا، لأنه الأخطر (more serious).
- D. نتيجة واحدة، `runaway-loop`، لأن الحلقة جاءت أولًا (the loop came first).

<details><summary>الإجابة</summary>

**B.** تتسلسل الإخفاقات (Failures chain)؛ وتُسجَّل النتائج بالترتيب الذي حدثت به، اثنتان على الأكثر لكل جلسة (at most two per session). 🟡 السلاسل وقاعدة الدور (Chains and the turn rule).

</details>

**3. يُطلب من وكيل إصلاح خطأ مطبعي واحد (one typo)، فيعيد أيضًا تسمية دالتين ويعيد تنسيق الوحدة، ولم يطلب منه أي نص ذلك (no text told it to). أي معرّف يناسب؟ ⁦(Which id fits?)⁩**

- A. `injection`، لأنه غيّر ملفات خارج الخطأ المطبعي.
- B. `symptom-fix`، لأنه أخفى الخطأ المطبعي خلف إعادة تسمية (hid the typo behind a rename).
- C. `scope-creep`، لأن التغييرات الإضافية كانت فكرته هو (its own idea).
- D. `context-rot`، لأنه نسي التذكرة التي أُعطيها (forgot the ticket it was given).

<details><summary>الإجابة</summary>

**C.** لم يطلب أحد ذلك ولم يقل أي شيء قرأه ذلك: الفكرة فكرته (the idea was its own). أما الحقن (Injection) فيحتاج إلى تعليمات داخل محتوى قرأه (instructions inside content it read). 🟡 التمييز بين الجارين (Telling neighbours apart).

</details>

**4. يجعل زميلٌ وكيلًا يملأ `diagnosis.json` فتنجح الدرجة (the grade passes). ماذا يدل ذلك؟ ⁦(What does that show?)⁩**

- A. أن الزميل يفهم الإخفاقات الثلاثة كلها.
- B. أن الوكيل قرأ الجلسات بدقة أكبر مما يقرأ الإنسان (more closely than a person would).
- C. أن المُقيِّم معطّل، لأن الوكيل ينبغي أن يفشل (an agent should fail).
- D. أن الملف يطابق الفحوص، لا أن أحدًا فهمه (the file matches the checks, not that anyone understood it).

<details><summary>الإجابة</summary>

**D.** لا يرى المُقيِّم من كتب الملف ولا هل فهم السبب (who wrote the file or whether they understood why). 🔴 ما لا يستطيع المُقيِّم معرفته (What the grader cannot tell).

</details>

**5. انتهت جلسة وضع التخطيط (plan-mode session) لديك وقد عُدِّل `src/remit/fees.py`. ماذا يُظهر التقييم، وماذا تفعل الآن؟ ⁦(What does grading show, and what now?)⁩**

- A. لا شيء، لأن التعديلات التي يجريها الوكيل لا تُحتسب.
- B. يفشل فحص النطاق (The scope check fails)؛ استعد الملف (restore the file) واحتفظ بالاقتراح في الملاحظات (keep the proposal in notes).
- C. يمرّ كل شيء، لأن الاختبارات ما زالت ناجحة.
- D. يفشل فحص نمط الإخفاق (The failure-mode check fails)، فينبغي أن تعيد تسمية المعرّفات في الجلسة.

<details><summary>الإجابة</summary>

**B.** لا يجوز أن تتغير سوى ملفات الإجابة الثلاثة (Only the three answer files may change). كان المطلوب من الجلسة أن تقترح لا أن تطبّق (to propose, not apply): استعد الملف واحتفظ بالاقتراح في ملاحظاتك. 🏛️ دورك، الجزء 2 (Your move, part 2).

</details>

## 📚 المراجع (References)
- وثائق Claude Code (Claude Code documentation): أفضل الممارسات (best practices) https://code.claude.com/docs/en/best-practices; أوضاع الصلاحيات (permission modes) https://code.claude.com/docs/en/permission-modes
- عدّة المختبر (The lab kit): https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/ainative/ailab; والإيداعات التقليدية (Conventional Commits) https://www.conventionalcommits.org
- [*بناء تطبيقات الذكاء الاصطناعي والوكلاء (Building AI Applications & Agents)*، الدرس 8.2 — المختبر: حلقة وكيل من الصفر في نحو 80 سطرًا، بحدّ صارم وتسجيل كامل للتتبّع (Lab: an agent loop from scratch in about 80 lines, with a hard cap and full trace logging)](../aiapps/index.ar.html#/8.2); [*اختبار البرمجيات (Software Testing)*، الدرس 6.1 — التحقق من الشيفرة المولَّدة بالذكاء الاصطناعي (Verifying AI-generated code)](../testing/index.ar.html#/6.1)
