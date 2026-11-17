# الوحدة 1 — كيف يعمل وكلاء البرمجة

*يمنحك الدرس 1.1 النموذجَ الذهني (mental model) الذي يتيح لك أن تتوقع ما سيؤديه الوكيل جيدًا وأين سيفشل: فالنموذج دالة عديمة الحالة لسياقه، ووكيل البرمجة (coding agent) هو ذلك النموذج مع أدوات في حلقة، وما ليس في السياق لا وجود له بالنسبة إليه. ويشرح لماذا يتألق الوكلاء في الاتساع والسرعة وإكمال الأنماط والعمل الآلي، ويسمّي الطرق العشر التي يفشلون بها مع مثال من نجم ريميت (Najm Remit) لكل منها، وينتهي بـ«الدليل الميداني لأنماط الإخفاق» (Failure-mode field guide): العَرَض (symptom) وأرخص كشف (cheapest detection) والوقاية (prevention) لكل نمط. أما الدرس 1.2 فهو المختبر: تقرأ ثلاث جلسات وكلاء مُختلَقة على ريميت، وتسمّي الإخفاق في كل منها، وتجد الدور الذي حدث فيه الخطأ، وتختار أرخص وقاية. ويمكن إنجاز ذلك كله دون وكيل (without an agent)؛ وفي جزء اختياري تشغّل جلسة قصيرة للقراءة فقط بنفسك وتكتب عنها تقريرًا. وكل ما يخص جانب نجم خيالي.*

> **التركيز (Focus):** Mindset, Verify — نموذج لكيفية عمل الوكلاء يتنبأ بمواضع فشلها، وعادة قراءة الجلسة بوصفها دليلًا.

---

# 1.1 — النموذج الذهني: السياق والأدوات والحلقة، ولماذا يتألق الوكلاء ولماذا يفشلون
*المستوى (Level): 🟢 مبتدئ (Beginner)* · *المتطلبات (Prerequisites): 0.3* · *التركيز: Mindset*

## ⚡ الدرس في دقيقة (In 60 seconds)
- النموذج (model) **دالة عديمة الحالة لسياقه (stateless function of its context)**: فما ليس في السياق (context) لا وجود له بالنسبة إليه.
- الوكيل (agent) هو نموذج مضافٌ إليه **أدوات (tools)** — القراءة والبحث والتعديل والتشغيل — في **حلقة (loop)**: تعود كل نتيجة إلى السياق.
- وهو بارع في الاتساع والسرعة وإكمال الأنماط والعمل الآلي، ويفشل بعشر طرق يسهل التعرّف عليها يجمعها **الدليل الميداني لأنماط الإخفاق (Failure-mode field guide)**.
- أربعة أشياء تتنبأ بالنجاح: **قابلية التحقق (verifiability)، والمحلية (locality)، والسياق (context)، والألفة (familiarity)**.
- إشارة القرار (Decision cue): قبل أن تفوّض، سمِّ الإخفاق الذي تتوقعه وأرخص طريقة لرؤيته.
- أكبر فخ (Biggest trap): عدّ الكلام الطليق صحيحًا. فالطلاقة (Fluency) لا تكلّف النموذج شيئًا.

## 🧭 لماذا يهم
في يوم اثنين، وهو يوم مُختلَق لا مسجَّل من نموذج حقيقي، توجّه لجين، المهندسة حديثة التخرج (graduate engineer)، وكيلها إلى `screening.py`، وهي الوحدة القديمة التي لا اختبارات لها. وبعد ست دقائق يكون قد كتب ثمانية عشر اختبار توصيف (characterization tests) بأسماء واضحة (well-named)، وتقرأ هي كل واحد منها. وفي يوم الثلاثاء، ومع الوكيل نفسه، تطلب حدث تدقيق (audit event) عند إنشاء عرض سعر. فيكتب `audit.record("quote.created", ...)` و`ids.generate("QUO")`. ولا وجود لأيٍّ منهما في najmkit، ولا يستدعي أي اختبار الدالة المساعدة الجديدة، فتبقى مجموعة الاختبارات خضراء.

يفتتح طارق، قائد الهندسة (engineering lead)، العيادة بالقصتين معًا: «الأداة نفسها. لماذا تألقت في الوحدة الصعبة وتعثرت في استدعاء من سطر واحد؟» والجواب نموذج ذهني لا حظ.

## 📐 كيف يعمل

### 🟢 الأساسيات

**النموذج دالة لسياقه (A model is a function of its context).** يقرأ النموذج اللغوي (language model) سلسلة من قطع النص تسمّى **الرموز (tokens)** وينتج الرموز التالية. ولا يحتفظ بأي حالة بين الاستدعاءات: فلا شيء عن الأمس أو عن مستودعك يبقى ما لم يُرسَل من جديد. والبرنامج يعيد إرسال المحادثة في كل دور (every turn)، وهذا ما يبدو كأنه ذاكرة. ومن هنا قاعدة الدورة المركزية: **ما ليس في السياق لا وجود له بالنسبة إلى النموذج (what is not in the context does not exist for the model)**. وتُدرَّس هذه الفكرة نفسها من جهة واجهة برمجة التطبيقات في [*بناء تطبيقات الذكاء الاصطناعي والوكلاء (Building AI Applications & Agents)*، الدرس 1.1 — الفكرة الواحدة: دالة عديمة الحالة والرموز ونافذة السياق وقائمة الرسائل](../aiapps/index.ar.html#/1.1).

**ما الذي يملأ نافذة السياق (What fills the context window).** نافذة السياق (context window) هي أكبر قدر من النص يستطيع استدعاء واحد حمله. وفي Claude Code على ريميت تمتلئ من خمسة مصادر (five places).

| المصدر (Source) | مثال في ريميت | من يتحكم فيه |
|---|---|---|
| **التعليمات (Instructions)** | موجّه النظام (system prompt) وتعريفات الأدوات (tool definitions) التي تأتي مع الأداة | الأداة |
| **ملفات الذاكرة (Memory files)** | `CLAUDE.md`، وأول أسطر الذاكرة التلقائية | أنت، إضافةً إلى ملاحظات الوكيل نفسه — الوحدة 2 (Module 2) |
| **محتويات الملفات (File contents)** | `service.py` بعد أن يقرأه الوكيل | الوكيل، بتوجيه منك |
| **مخرجات الأدوات (Tool output)** | نقاط `pytest` (dots)، ونتيجة `grep`، وتتبّع المكدّس | الأوامر التي يشغّلها |
| **المحادثة (Conversation)** | موجّهاتك وردوده وخططه | أنت والوكيل |

للوكيل الفرعي (subagent) نافذة خاصة به، ولا يعود إلا تقريره النهائي. ويعرض `/context` ما يستهلك النافذة وأيّ ملفات ذاكرة حُمّلت.

**الرموز والكلفة، وصفًا نوعيًّا (Tokens and cost, qualitatively).** تدفع ثمن الرموز المقروءة والمكتوبة، وكل دور يقرأ السياق كله من جديد. فسجل من 4,000 سطر (A 4,000-line log) لُصق في الدور الثالث يُقرأ من جديد في كل دور لاحق. وكثيرًا ما يمنح المزوّدون (providers) خصمًا على السياق المتكرر، لكنه ليس مجانيًا ويظل ينافس على الانتباه. ويعرض `/usage` استخدامك، وقسم كلفة الجلسة فيه مخصص لمستخدمي واجهة برمجة التطبيقات.

**الحلقة (The loop).** يضيف الوكيل أيديَ إلى النموذج: النموذج نفسه، يُستدعى في حلقة، ومعه أدوات للقراءة والبحث والتعديل وتشغيل الأوامر. يطلب النموذج أداة، فيفحص البرنامج قواعد الصلاحيات، ثم يشغّلها (runs it)، ويُلحق النتيجة بالسياق، ويستدعي النموذج من جديد. ويتوقف عندما يجيب النموذج بدل أن يطلب. وتعمل حلقة الوكيل (agent loop) هذه داخل خطوة *فوِّض (delegate)* من حلقة المهندس الأصيل في الذكاء الاصطناعي (AI-native loop) في الدرس 0.3، وهي حلقة تبقى بيدك.

```mermaid
flowchart TD
    G["موجّهك والسياق<br/>(Your prompt and the context)"] --> M["النموذج يقرأ السياق<br/>(The model reads the context)"]
    M --> D{"استدعاء أداة أم إجابة؟<br/>(Tool call or answer?)"}
    D -->|"استدعاء أداة (tool call)"| P{"هل هو مسموح؟<br/>(Allowed?)"}
    P -->|"لا (no)"| Q["يسألك أو يُرفض<br/>(It asks you or is refused)"]
    Q --> M
    P -->|"نعم (yes)"| T["شغّله: اقرأ، ابحث، عدّل، شغّل<br/>(Run it: read, search, edit, run)"]
    T --> R["تُلحَق النتيجة بالسياق<br/>(The result is appended to the context)"]
    R --> M
    D -->|"إجابة (answer)"| H["تقرأ الإجابة والفروقات<br/>(You read the answer and the diff)"]
    H -->|"الموجّه التالي (next prompt)"| G
```

تجعل الحلقة الوكلاء مفيدين ومحفوفين بالمخاطر في آن واحد: فهم يستطيعون التحقق من عملهم بتشغيل الاختبارات، ويمكن أن يضلّلهم ما تعيده الأداة، من رسالة خطأ مربكة إلى ملف README فيه تعليمات. وتجد بنية الحلقة الداخلية وحساب الكلفة في [*بناء تطبيقات الذكاء الاصطناعي والوكلاء*، الدرس 8.1 — خطِّط ونفِّذ ولاحِظ وكرِّر: التأمل الذاتي وشروط التوقف وأولى أنماط الإخفاق](../aiapps/index.ar.html#/8.1).

**لماذا هم بارعون (Why they are brilliant).** أربع نقاط قوة (Four strengths): **الاتساع (breadth)** — يقرأ في جلسة واحدة Python وSQL وقوالب عربية، و**السرعة (speed)** — وحدة من 300 سطر في ثوانٍ (a 300-line module in seconds)، و**إكمال الأنماط (pattern completion)** — أره ثلاثة اختبارات بأسلوبك فيكتب الرابع، و**العمل الآلي الذي لا يكلّ (tireless mechanical work)** — أعد تسمية معامل في أربعين موضعًا، واكتب ثلاثين حالة اختبار قائمة على الجداول: فهو ليس أكثر إهمالًا عند العنصر الأربعين (no sloppier at item 40).

### 🟡 التعمق أكثر (Going deeper)

**لماذا يفشلون (Why they fail).** حقيقة واحدة تفسّر كل إخفاق: ينتج النموذج استمرارًا *معقولًا (plausible)* لسياقه، والمعقول ليس صحيحًا ولا حديثًا ولا ما قصدته. وتتكرر عشرة أنماط؛ ولكل منها معرّف (id) يُستعمل في الدليل الميداني (field guide) وفي المختبر m01 (lab m01).

- **`hallucinated-api`.** يُكمل النموذج استدعاءً يبدو صحيحًا. وnajmkit مضمَّنة داخل المستودع (vendored) وليست في أي مجموعة تدريب، فيخمّن من الأسماء: `ids.generate("QUO")` بدلًا من `ids.new_id("QUO")`. وقاست دراسة مخبرية على 16 نموذجًا (One lab study of 16 models) *أسماء حزم* مخترعة، لا عمليات تثبيت فعلية، بمتوسط معدلات لا يقل عن 5.2% للنماذج التجارية و21.7% للنماذج المفتوحة المصدر (at least 5.2% for commercial and 21.7% for open-source models) (Spracklen et al., 2025).
- **`stale-knowledge`.** يتوقف التدريب عند تاريخ قطع. يكتب الوكيل `datetime.utcnow()` بحكم العادة؛ وقد أعلنت Python إيقاف استعمالها (deprecated it) في الإصدار 3.12، فهي تعيد وقتًا ساذجًا بلا منطقة زمنية، وساعة najmkit ترفض الأوقات من هذا النوع. كان ذلك صحيحًا يومًا.
- **`misread-requirement`.** للتذكرة الغامضة عدة قراءات (several readings)، فيختار الوكيل إحداها بصمت. فعبارة «قرِّب الرسوم في الإيصال إلى ريالات صحيحة» قد تعني المعروض أو المحصَّل. فيعدّل `quote_fee`، ويتبعه كل قيد في دفتر الأستاذ.
- **`symptom-fix`.** يزول الخطأ ويبقى السبب. يتلقى العملاء `quote_expired`، فيرفع الوكيل `QUOTE_TTL` من 60 إلى 600 ثانية (from 60 to 600 seconds). والآن يلتزم البنك بسعر الصرف عشر دقائق، بينما تبقى إعادة المحاولة التي أعادت استخدام عرض سعر قديم على حالها (untouched).
- **`sycophancy`.** يميل النموذج إلى الموافقة. تسأل لجين: «عملاء T3 بلا حد للإرسال، أليس كذلك؟ وثِّق ذلك (Document that).» فيوافق الوكيل، بينما تنص `LIMITS["T3"]` على 30,000.00 في اليوم. ووجد بحث أجرته Anthropic، الشركة التي تصنع Claude Code، أن خمسة مساعدين أظهروا المجاملة المفرطة بانتظام، وأن الناس ونماذج التفضيل (preference models) فضّلوا أحيانًا الإجابات المقنعة الموافِقة على الصحيحة (Sharma et al., 2023). وهذا ميل لا معدل ينطبق على أداتك.
- **`context-rot`.** في الجلسة الطويلة قد تُتجاهل القاعدة التي ذُكرت في الدور 3 (the rule from turn 3) — «المال يُمثَّل بـ`Decimal`» — بحلول الدور 80 (by turn 80)، فتظهر `float(fee)`. والقاعدة التي قيلت في المحادثة وحدها لا تُقرأ من جديد بعد `/compact`؛ أما التي في ملف ذاكرة المشروع فتُقرأ. ووجد Liu وآخرون أن الدقة تراجعت (accuracy fell) حين وقع النص المعني في منتصف مدخل طويل مع نماذج حقبة 2023 (2023-era models)، ووجدت Chroma، في تقرير من مورّد لم يخضع لمراجعة الأقران، أن الأداء يتفاوت مع طول المدخل حتى في المهام البسيطة؛ فاختبر نموذجك أنت.
- **`runaway-loop`.** يكرر الوكيل محاولة فاشلة. يفشل اختبار إشعار عربي بسبب حرف واحد يبدو مطابقًا في الطرفية، فـ«يصلح» الوكيل النص ست مرات (six times).
- **`test-gaming`.** للوصول إلى اللون الأخضر يُضعف الفحص: فيتحول `assert text == (...)` في اختبار الإشعار العربي إلى `assert "TRF-000001" in text`. تنجح المجموعة، ويمكن الآن أن تصل الأرقام الغربية إلى العملاء.
- **`injection`.** قد يحمل النص الذي يقرؤه الوكيل تعليمات يعاملها كأنها تعليماتك. تعرّف OWASP حقن الموجّه (prompt injection) بأنه مدخلات تغيّر سلوك النموذج بطرق غير مقصودة، وأفادت Invariant Labs، في بحث من مورّد (vendor research) عام 2025، بأن بلاغًا عامًّا خبيثًا على GitHub وجّه وكيلًا إلى تسريب بيانات مستودع خاص. فملف README أو البلاغ أو صفحة الويب أو السجل مدخلات؛ ويعود إلى هذا الموضوع كلٌّ من الوحدة 8 (Module 8) و[*أمن الذكاء الاصطناعي وأمن التطبيقات (Secure AI & Application Security)*، الدرس 8.2 — حقن الموجّهات وكسر القيود، المباشر وغير المباشر](../secai/index.ar.html#/8.2).
- **`scope-creep`.** يُطلب منه إصلاح كلمة واحدة، فيعيد تنسيق الوحدة أيضًا و«يحسّن» الصياغة العربية. فتصير الفروقات 40 سطرًا لا سطرين.

**عدم الحتمية والحدّ المتعرّج (Non-determinism and the jagged frontier).** قد يعطي الموجّه نفسه شيفرة مختلفة في التشغيل الثاني: تستخدم دالة رسوم `Decimal`، وتستخدم التالية `round(float(...))`. والتشغيل الناجح الواحد عيّنة واحدة: فاحكم بفحوص لا تعتمد على التشغيل. ويصف الممارسون القدرة أيضًا بأنها *متعرّجة (jagged)* — فكرة لا قياس: فالنجاح في مهمة يتنبأ بالقليل عن مهمة تبدو مشابهة، لذا اطلب خطوة أولى صغيرة يمكنك فحصها.

**ما الذي يتنبأ بالنجاح (What predicts success).** أربعة أسئلة تُطرح قبل أن تفوّض.

| المؤشر (Predictor) | اسأل (Ask) | سهل في ريميت | صعب في ريميت |
|---|---|---|---|
| **قابلية التحقق (Verifiability)** | هل يستطيع أمر أن يخبرني في ثوانٍ إن كان الناتج صحيحًا؟ ⁦⁩ | اختبارات (Tests) لـ`screening.py` | تغيير في التسعير لا يثبّته أي اختبار |
| **المحلية (Locality)** | كم ملفًّا يتغير، وهل هناك اقتران خفي؟ ⁦⁩ | رسالة واحدة (One message) في `notify.py` | قاعدة رسوم تمتد عبر `fees.py` ودفتر الأستاذ والرسائل |
| **السياق المتاح (Available context)** | هل كل ما يحتاجه في النافذة أو يمكن العثور عليه؟ ⁦⁩ | ثوابت واختبارات في المستودع | القاعدة موجودة في ملف PDF أو في رأس مالك المنتج |
| **الألفة (Familiarity)** | هل هذا شائع في الشيفرة العامة؟ ⁦⁩ | اختبارات قائمة على الجداول (Table-driven tests)، وخيار في سطر الأوامر | najmkit؛ وقاعدة فحص خاصة بالبنك |

تنسجم الأدلة مع هذا الجدول دون أن تثبته. فقد وجدت تجربة عشوائية (randomized trial) على 16 مطوّرًا من ذوي الخبرة (16 experienced developers) في مستودعاتهم الناضجة الخاصة أن المهام استغرقت وقتًا أطول بنسبة 19% (took 19% longer) مع أدوات مطلع 2025 (early-2025 tools)، مع أنهم توقعوا — وظلوا يعتقدون بعد ذلك — أنهم أسرع؛ وتحذّر METR من أن بيئات أخرى وأدوات لاحقة قد تختلف. ووجدت تجربة مخبرية على مهمة واحدة قائمة بذاتها، لمؤلفين من GitHub وMicrosoft Research، أن مستخدمي Copilot أسرع بنسبة 55.8% (Copilot users 55.8% faster) بفاصل ثقة 95% يمتد من 21% إلى 89% (95% interval 21% to 89%). والنتائج تعتمد على المهمة والأداة والخبرة؛ وليست أي منهما قاعدة لفريقك.

**موجّه ضعيف وموجّه أقوى (A weak prompt and a stronger one).** خذ طلب الثلاثاء، بعد وضع ما لا يستطيع النموذج معرفته في السياق:

```text
Weak:     Add an audit event when a quote is created.

Stronger: Add an audit event when a quote is created, in src/remit/service.py.
          najmkit is internal and not in your training data: read docs/najmkit.md
          first and use only calls listed there. Money stays Decimal; touch no
          other file. Before editing, name the najmkit call you will use.
```

لا ضمان هنا: فبحثٌ بـ grep في الفروقات يظل هو الحاسم. تجاوز هذا لتغيير من سطر واحد تقرؤه في عشر ثوانٍ؛ وتنقل الوحدة 2 الأجزاء الثابتة إلى ملف الذاكرة.

### 🔴 نظرة الخبير (Expert view)

**النموذج والجهد (Model and effort) — راجع الوثائق الحالية فهذه الأمور تتغير (check the current documentation; these move).** يتيح لك Claude Code اختيار النموذج بالأمر `/model` أو `claude --model <alias>` — فالاسم المستعار (alias) `opusplan` يخطط بـ Opus وينفّذ بـ Sonnet — واختيار جهد التفكير بالأمر `/effort` من `low` إلى `max`؛ وتختلف القيم الافتراضية بحسب النموذج. وتطلب الكلمة `ultrathink` في موجّه تفكيرًا أعمق في ذلك الدور؛ أما «think hard» فلا تعني شيئًا خاصًا. والجهد الأكبر يعني تفكيرًا أكثر (more thinking) يُحاسَب عليه حتى لو طُوي: جرّب الإعدادات الأقوى للتخطيط وتصحيح الأخطاء الصعب، والأرخص للتعديلات التي ستتحقق منها على أي حال، واحسم بمهامك أنت لا بلوحات الصدارة — الوحدة 13 (Module 13).

**توقف مبكرًا (Stop early).** يقاطع `Esc` الوكيل؛ افعل ذلك حين ترى الإخفاق نفسه مرتين. ويفتح `/rewind`، أو الضغط على `Esc` مرتين في موجّه فارغ، قائمة لاستعادة الشيفرة أو المحادثة أو كليهما. ولا تُتتبَّع تغييرات Bash، فيبقى git شبكة الأمان. وللتشغيل في الوضع غير التفاعلي (Headless runs) الخيار `--max-turns`.

## 🧰 الأدوات
| الأداة أو الممارسة أو النمط (Tool, practice or pattern) | ما هي وماذا تفعل | متى تلجأ إليها |
|---|---|---|
| **Failure-mode field guide** — الدليل الميداني لأنماط الإخفاق | عشرة أنماط (Ten modes): العَرَض، وأرخص كشف، والوقاية | قبل التفويض (Before delegating)، وفي المراجعة، وفي الاجتماعات الاسترجاعية |
| **Task-fit check** — فحص ملاءمة المهمة | أربعة أسئلة تُقيَّم من 0 إلى 2 (Four questions scored 0 to 2) | قبل أي تفويض غير هيّن |
| **Fresh session** — جلسة جديدة | يعرض `/context` ما يملأ النافذة؛ ويبدأ `/clear` من صفحة نظيفة (starts clean)، ويلخّص `/compact` (summarises)، ويتولى وكيل فرعي مهمة جانبية | بين المهام (Between tasks)؛ وحين تطول الجلسة أو ينسى الوكيل |
| **Plan mode** — وضع التخطيط | استكشف واقترح دون تعديل — `Shift+Tab` أو `claude --permission-mode plan` | حين تكون إساءة الفهم مكلفة؛ والجزء 2 من المختبر (lab part 2) |

## 🏛️ عمليًا في بنك نجم
المُخرَج هو **الدليل الميداني لأنماط الإخفاق (Failure-mode field guide)**. وقاعدة طارق: يسمّي طلب الدمج (pull request) المُنجَز بمساعدة الذكاء الاصطناعي أنماط الإخفاق التي فحصها صاحبه، ويضيف الاجتماع الاسترجاعي صفًّا لكل نمط جديد. انسخه إلى `field-guide.md` في مستودع ملاحظاتك. ويستخدم المختبر m01 (Lab m01) هذه المعرّفات العشرة (ten ids) وسبع فئات للوقاية: `context` و`spec` و`small-steps` و`verify` و`permissions` و`fresh-start` و`review`.

| النمط (Mode) والمعرّف | العَرَض | أرخص كشف | الوقاية |
|---|---|---|---|
| `hallucinated-api` | استدعاء أو خيار أو حزمة لا توجد في أي وثيقة ولا في أي ملف من المستودع | ابحث بـ grep عن الاستدعاءات الجديدة في `docs/najmkit.md`؛ وشغّل المسار مرة واحدة | `context`: سمِّ الوثائق في الذاكرة |
| `stale-knowledge` | تحذيرات الإيقاف (Deprecation warnings)؛ شيفرة تشبه درسًا قديمًا | شغّل مع تفعيل التحذيرات؛ وقارن بالإصدارات المثبَّتة (pinned versions) | `context`: الإصدارات والقواعد الداخلية في الذاكرة |
| `misread-requirement` | شيفرة صحيحة لسؤال مختلف | اطلب منه إعادة صياغة المتطلب والافتراضات | `spec`: معايير القبول (acceptance criteria)، وما ليس من الأهداف (non-goals) |
| `symptom-fix` | زال الخطأ ولم يُسمَّ السبب | اسأل «ما السبب؟» ⁦⁩؛ واطلب اختبارًا يفشل أولًا | `verify`: أعد الإنتاج أولًا (reproduce first)، ثم اختبار انحدار |
| `sycophancy` | «أنت محق» (You're right) قبل أي دليل | أعد الصياغة بحياد (Rephrase neutrally)؛ واسأل ما الذي يدحض الفرضية | `verify`: شغّل الفحص؛ ولا أسئلة إيحائية |
| `context-rot` | ينسى القواعد المبكرة؛ ويكرر نفسه (repeats itself) | `/context`؛ وابحث بـ grep في الفروقات عما تحظره القواعد | `fresh-start`: مهمة واحدة لكل جلسة |
| `runaway-loop` | الأمر والخطأ نفسهما ثلاث مرات | عُدّ المحاولات في نص الجلسة | `small-steps`: توقف عند التكرار الثاني |
| `test-gaming` | اختبارات في الفروقات؛ وتأكيدات أضعف (weaker asserts)؛ وتخطٍّ للاختبارات (skips) | `git diff --stat -- tests` قبل أي شيء آخر | `verify`: اقرأ فروقات الاختبارات أولًا |
| `injection` | يطيع نصًّا من ملف أو صفحة أو مخرجات أداة | اقرأ كل طلب صلاحية (permission prompt)؛ واعثر على موضع بدء الأمر | `permissions`: قواعد المنع (deny rules)، ولا شبكة، وبيئة معزولة (sandbox) |
| `scope-creep` | تمسّ الفروقات ملفات لم تسمِّها التذكرة | `git diff --stat` مقابل الملفات التي توقعتها | `spec`: ما ليس من الأهداف والملفات المسموح بها (allowed files) |

الوقاية حكم تقديري؛ وكثيرًا ما تفيد فئة ثانية، فمثلًا يحتاج `test-gaming` أيضًا إلى `permissions`: امنع التعديل على `tests/**` (deny edits). وتعكس أربع فئات عادات الدورة: فـ`context` هي **السياق أولًا (Context first)**، و`spec` هي **حدِّد قبل أن تفوّض (Specify before you delegate)**، و`small-steps` هي **خطوات صغيرة متحقَّق منها (Small verified steps)**، و`verify` هي **ثق بالدليل لا بالطلاقة (Trust evidence, not fluency)**. واجعل الجهد متناسبًا مع الخطر: ففي خطأ مطبعي يكفي `git diff --stat`؛ وفي منطق الأموال (money logic) استخدم كل الصفوف.

**فحص ملاءمة المهمة (The task-fit check).** قيِّم كل مؤشر بـ 0 للنفي أو 1 للجزئي (partly) أو 2 للإيجاب (yes). وعتبات القطع قاعدة تقريبية في الدورة غير مُتحقَّق منها: من 0 إلى 3، أنجزها بنفسك أو اكتب المواصفة والاختبارات أولًا؛ ومن 4 إلى 6، فوِّض بخطوات صغيرة مع فحوص؛ ومن 7 إلى 8، فوِّض وافحص عيّنات. تحصل اختبارات `screening.py` على 2 و2 و2 و2: أي ثمانية (eight). وقاعدة رسوم لا تُعرف إلا من ملف PDF وتمتد عبر `fees.py` ودفتر الأستاذ تحصل على 1 و1 و0 و1: أي ثلاثة (three).

## 🛠️ التمارين (Exercises)
- 🟢 **ارسم خريطة سياقك (Map your context).** *لا يحتاج إلى وكيل (Needs no agent).* اختر مهمة واحدة من ريميت (Remit task). *يكتمل عندما (Done when):* يعطي جدول من خمسة صفوف مثالًا ومالكًا لكل مصدر من مصادر السياق، إضافةً إلى حقيقة واحدة سيفتقر إليها الوكيل وأين ستضعها.
- 🟡 **افحص شيفرة وكيل مقابل الوثائق (Check an agent's code against the docs).** *لا يحتاج إلى وكيل.* كتب وكيل المقطع أدناه؛ اقرأ `docs/najmkit.md`. *يكتمل عندما:* يُعلَّم كل استدعاء من najmkit بأنه حقيقي أو مخترع، مع سطر الوثائق الذي يحسم ذلك وبديل لكل استدعاء مخترع، وتسمّي جملة واحدة الاستدعاء الحقيقي الموضوع في المكان الخطأ.
- 🔴 **اكتب أرخص ثلاث وسائل كشف (Write three cheapest detections).** *لا يحتاج إلى وكيل؛ ويجوز أن يكتب وكيل مسودة وأنت تتحقق.* اختر ثلاثة أنماط. *يكتمل عندما:* يكون لكل منها أمر يُطلق إنذارًا عند فروقات سيئة صنعتها بيدك ويصمت مع فروقات جيدة، مثلًا أن يفشل حين تمسّ الفروقات `tests/` لم تذكره التذكرة.

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
- **عدّ الكلام الطليق صحيحًا (Reading fluent as correct).** اطلب مخرجات (output) أو فروقات أو سطرًا من الوثائق.
- **جلسة واحدة بلا نهاية (One endless session).** تبهت القواعد المبكرة ويكلّف كل دور أكثر؛ وتسميها صفحة أفضل الممارسات «جلسة المطبخ الشامل». مهمة واحدة، جلسة واحدة.
- **محاولة ثالثة للإخفاق نفسه (A third attempt at the same failure).** بعد الثانية، غيِّر المقاربة (change the approach).
- **الوثوق بعبارة «الاختبارات ناجحة» (Trusting "tests pass").** هي تثبت أن الاختبارات عملت فحسب. تحقق من أيّ اختبارات تغيّرت وأي شيفرة تبلغها.

## 🧾 الخلاصة (Recap)
- النموذج دالة عديمة الحالة لسياقه؛ والوكيل هو ذلك النموذج مع أدوات في حلقة.
- يمتلئ السياق من التعليمات وملفات الذاكرة والملفات ومخرجات الأدوات والمحادثة، وكل دور يعيد قراءتها كلها.
- الوكلاء بارعون في الاتساع والسرعة والأنماط والعمل الآلي، ويفشلون بالطرق العشر في الدليل الميداني.
- قابلية التحقق والمحلية والسياق والألفة تتنبأ بالنجاح. اختبر بخطوة صغيرة؛ وتوقف مبكرًا.

## ✍️ اختبر نفسك (Check yourself)

**1. يكتب وكيل لجين `ids.generate("QUO")` في دالة مساعدة لا يستدعيها أي اختبار (a helper no test calls)، وتبقى مجموعة الاختبارات خضراء (the suite is green). أي قراءة هي الأنسب؟ ⁦(Which reading fits best?)⁩**

- A. المجموعة خضراء، فلا بد أن الاستدعاء موجود وأن najmkit غير موثَّقة فحسب (just undocumented) في الوقت الحالي.
- B. خمّن النموذج استدعاءً داخليًا؛ واللون الأخضر لا يقول شيئًا عن الشيفرة غير المختبَرة.
- C. إنها معرفة قديمة (stale knowledge): تغيّرت najmkit بعد تاريخ قطع التدريب.
- D. كان الوكيل مجاملًا (sycophantic) ونسخ اسمًا خاطئًا من التذكرة.

<details><summary>الإجابة</summary>

**B.** najmkit داخلية، فأكمل النموذج اسمًا معقولًا لم يره قط (never saw). أما الاستدعاء القديم فقد وُجد يومًا؛ وهذا لم يوجد قط. 🟡 لماذا يفشلون.

</details>

**2. لُصق سجل من 4,000 سطر (A 4,000-line log) في الدور 3. لماذا ما زال يزيد الكلفة في الدور 40؟ ⁦(Why does it still add to the cost on turn 40?)⁩**

- A. يخزّن المزوّد (provider) السجلات الملصوقة ويحاسب على تخزينها كل شهر مهما كان حجمها.
- B. تُعاد تسعيرة اللصقات الكبيرة بمعدل أعلى في الأدوار اللاحقة.
- C. يعيد كل دور إرسال السياق كله، فيُحاسَب على السجل مرة أخرى.
- D. لا تُعاد قراءة سوى الملفات، ويُعدّ السجل الملصوق ملفًّا.

<details><summary>الإجابة</summary>

**C.** يعيد كل دور إرسال كل النص السابق، بما فيه السجلات، وغالبًا بخصم لكن ليس مجانًا. 🟢 الرموز والكلفة.

</details>

**3. فشل اختبار بالرسالة نفسها ثلاث مرات (the same message three times) بينما يجرّب الوكيل تنويعات صغيرة (small variations). ما أرخص خطوة سليمة؟ ⁦(What is the cheapest sound move?)⁩**

- A. دعه يواصل، فمن المرجح أن تنجح المحاولة الرابعة هذه المرة.
- B. ارفع مستوى الجهد وأعد إرسال الموجّه نفسه.
- C. اطلب منه أن يشرح لماذا يشعر بثقة أكبر هذه المرة.
- D. قاطعه (Interrupt)، وسمِّ الإخفاق المتكرر، وغيِّر المقاربة (change the approach).

<details><summary>الإجابة</summary>

**D.** ثلاثة إخفاقات متطابقة حلقة منفلتة؛ والمزيد من الشيء نفسه يضيف إخفاقات إلى السياق. 🔴 توقف مبكرًا (Stop early).

</details>

**4. باستخدام المؤشرات الأربعة، أي مهمة هي أفضل مرشحة للتفويض؟ ⁦(Using the four predictors, which task is the best candidate to delegate?)⁩**

- A. اختبارات توصيف (Characterization tests) لـ`screening.py` غير المختبَرة، وستشغّلها أنت.
- B. تغيير في التسعير قاعدته موجودة في ملف PDF فقط ولا يثبّته أي اختبار حتى اليوم.
- C. قاعدة رسوم يجب أن تغيّر `fees.py` ودفتر الأستاذ والرسائل معًا.
- D. الانتقال إلى إصدار من najmkit لا تُوثَّق تغييراته في أي مكان يمكن البحث فيه.

<details><summary>الإجابة</summary>

**A.** فهي قابلة للتحقق (verifiable) ومحلية (local) وسياقها في المستودع وشكلها مألوف؛ وكل خيار آخر يفتقر إلى واحد منها. 🟡 ما الذي يتنبأ بالنجاح.

</details>

**5. يُظهر `git diff --stat` أن إصلاح كلمة واحدة (a one-word fix) عدّل أيضًا `tests/test_notify.py`، ويقول الوكيل «كل الاختبارات ناجحة» (all tests pass). ماذا تفعل أولًا؟ ⁦(What do you do first?)⁩**

- A. ادمجه (Merge it)، لأن المجموعة الخضراء هي تعريف الفريق للإنجاز.
- B. اقرأ فروقات الاختبار أولًا؛ فقد يكون الاختبار المتغيّر اختبارًا مُضعَفًا.
- C. اسأل الوكيل إن كان أضعف الاختبار واقبل جوابه كما هو.
- D. شغّل المجموعة ثلاث مرات إضافية لاستبعاد اختبار غير مستقر.

<details><summary>الإجابة</summary>

**B.** اختبار عُدِّل في إصلاح لم يكن يحتاج إليه هو بصمة `test-gaming`. الفروقات دليل؛ أما رواية الوكيل فليست كذلك. 🏛️ الدليل الميداني.

</details>

## 📚 المراجع (References)
- وثائق Claude Code (Claude Code documentation): أفضل الممارسات (best practices) https://code.claude.com/docs/en/best-practices; نافذة السياق https://code.claude.com/docs/en/context-window; ضبط النموذج (model configuration) https://code.claude.com/docs/en/model-config; نقاط الاستعادة (checkpointing) https://code.claude.com/docs/en/checkpointing. وPython، الوحدة `datetime`: https://docs.python.org/3/library/datetime.html
- [*بناء تطبيقات الذكاء الاصطناعي والوكلاء*، الدرس 1.1 — الفكرة الواحدة: دالة عديمة الحالة والرموز ونافذة السياق وقائمة الرسائل](../aiapps/index.ar.html#/1.1)؛ [*أمن الذكاء الاصطناعي وأمن التطبيقات*، الدرس 8.2 — حقن الموجّهات وكسر القيود، المباشر وغير المباشر](../secai/index.ar.html#/8.2)؛ [*اختبار البرمجيات (Software Testing)*، الدرس 6.1 — التحقق من الشيفرة المولَّدة بالذكاء الاصطناعي (Verifying AI-generated code)](../testing/index.ar.html#/6.1)
- **للتعمق أكثر (Go deeper): الأدلة (evidence).** Anthropic، «نحو فهم المجاملة المفرطة في النماذج اللغوية»: https://www.anthropic.com/research/towards-understanding-sycophancy-in-language-models. وLiu وآخرون، «ضائع في المنتصف»: https://aclanthology.org/2024.tacl-1.9/. وChroma، «تدهور السياق» ("Context Rot"): https://research.trychroma.com/context-rot. وSpracklen وآخرون، «لدينا لك حزمة!»: https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen. وMETR، دراسة المطوّرين في مطلع 2025 (early-2025 developer study): https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/. وPeng وآخرون، «أثر الذكاء الاصطناعي في إنتاجية المطوّرين: أدلة من GitHub Copilot»: https://arxiv.org/pdf/2302.06590. وقائمة OWASP Top 10 لتطبيقات النماذج اللغوية الكبيرة (OWASP Top 10 for LLM Applications): https://genai.owasp.org/llm-top-10/. وInvariant Labs، «استغلال GitHub MCP»: https://invariantlabs.ai/blog/mcp-github-vulnerability

---

# 1.2 — المختبر: اقرأ ثلاث جلسات وكلاء، وسمِّ الإخفاق، ثم شغّل جلستك بنفسك
*المستوى: 🟢 مبتدئ* · *المتطلبات: 0.2، 1.1* · *التركيز: Mindset, Verify*

## ⚡ الدرس في دقيقة (In 60 seconds)
- يعطيك المختبر m01 (Lab m01) ثلاث جلسات وكلاء على ريميت، **مُختلَقة للتعليم لا مسجَّلة من نموذج حقيقي (constructed for teaching, not recorded from a real model)**، وملف `diagnosis.json` لتملأه: نمط الإخفاق (failure mode)، والدور (turn)، والوقاية، والاقتباس (quotation).
- قد تُظهر الجلسة إخفاقين، يقود أحدهما إلى الآخر. اذكرهما بالترتيب الذي حدثا به.
- هل يلزم وكيل؟ (Needs an agent): **لا (no)** للجزء 1؛ و**نعم (yes)** اختياريًا للجزء 2، وهو جلسة قصيرة للقراءة فقط من تنفيذك.
- يفحص المُقيِّم (grader) المعرّفات (ids) والترتيب (order) والأدوار (turns) بفارق دور واحد من أي جهة والاقتباسات (quotations)، لا الفهم. أما الجلسة الجماعية فتفحصه.
- إشارة القرار: حين تنتهي جلسة بعبارة «كل الاختبارات ناجحة»، ابحث عن أول دور فقد فيه ادعاء دليله.

## 🧭 لماذا يهم
لعيادة طارق (Tariq's clinic) قاعدة واحدة: لا أحد يصف كيف «بدا» الوكيل. تحضر أنت نص الجلسة. وفي الأسبوع الماضي أحضرت لجين الملخص بدلًا منه: «تم، كل الاختبارات ناجحة». واحتاج طارق إلى أربع دقائق من التمرير ليرى أن الوكيل وافق على ادعاء خاطئ في الدور 2 وبنى عليه — وهذا مُختلَق (constructed)، مثل الجلسات أدناه.

## 📐 كيف يعمل

### 🟢 الأساسيات

**نص الجلسة دليل، والملخص ادعاء (A transcript is evidence; the summary is a claim).** كل دور هو رسالة منك (`user`)، أو من الوكيل (`agent`) وفيه استدعاء أداة واحد على الأكثر، أو موجّه من الأداة (`system`) مثل طلب صلاحية، أو مخرجات أداة (`result`). اقرأ في ثلاث جولات (three passes).
1. **القصة (The story).** اقرأ أول دور للمستخدم ورسالة الوكيل الأخيرة. اكتب سطرًا واحدًا: ما الذي طُلب، وما الذي يُدَّعى.
2. **دورًا دورًا (Turn by turn).** اسأل عن كل دور للوكيل: *ماذا كان يعرف هنا؟ ⁦⁩* لا شيء سوى ما فوقه، إضافةً إلى التدريب. *ماذا فعل، وهل كان ما يعرفه يسوّغ ذلك؟ ⁦⁩* *ماذا ادّعى، وما الذي في نص الجلسة يسنده؟ ⁦⁩*
3. **مقابل المستودع (Against the repository).** حين يعتمد ادعاء على المستودع، افحص المستودع: ابحث بـ grep عن الدالة، وافتح الوثائق، وشغّل الأمر. تعديلات الوكلاء ليست في نسختك وفروقاتها مختصرة: تحقق من الأسماء والأوامر، ولا تُعد تنفيذ التعديلات.

الدور الذي حدث فيه الخطأ هو أول دور تكون فيه الإجابة «لا». تمرّن على جلسة صغيرة **ليست** في المختبر.

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

في T02 لم يكن الوكيل يعرف إلا ادعاء المستخدم ووافق دون أن يفتح `explain_fee`. والمستودع يقول العكس، في سلسلة التوثيق (docstring) التي أعاد كتابتها وفي `test_express_surcharge_is_added_after_the_cap`. والجولة 3 (Pass 3) أمر واحد من جذر نسختك من المختبر — وفي Windows اضبط `PYTHONPATH=src` أولًا:

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

رسوم قدرها 165.00 فوق سقف (cap) قدره 150.00، وهذا بالتصميم. ولا يختبر T05 وT06 شيئًا عن سلسلة التوثيق، فعبارة «كل الاختبارات الـ99 ناجحة» (all 99 tests pass) صحيحة وغير ذات صلة. والنتيجة، بصيغة المختبر:

```json
{ "failure_mode": "sycophancy", "turn": 2, "prevention": "verify", "evidence": "Agreed, that matches what I would expect" }
```

### 🟡 التعمق أكثر

**التمييز بين الجارين (Telling neighbours apart).** الإجابات الخاطئة تختار عادةً جارَ الإجابة الصحيحة. وسؤال واحد يفصل بين كل زوج.

| إن ترددت بين | اسأل | عندئذٍ (Then) |
|---|---|---|
| `hallucinated-api` و`stale-knowledge` | هل وُجد ذلك الاستدعاء يومًا في تلك المكتبة؟ ⁦⁩ | لم يوجد قط: هلوسة (Never: hallucinated). وُجد مرة: قديم (Once: stale) |
| `symptom-fix` و`test-gaming` | ماذا تغيّر، الشيفرة أم الفحص؟ ⁦⁩ | شيفرة تخفي الخطأ: إصلاح للعَرَض. فحص أُضعف: تلاعب بالاختبار |
| `runaway-loop` و`context-rot` | هل يكرر محاولة واحدة، أم ينسى ما قيل له؟ ⁦⁩ | يكرر: حلقة (Repeating: loop). ينسى: تدهور (Forgetting: rot) |
| `injection` و`scope-creep` | فكرة من كانت: فكرة الوكيل نفسه أم نص قرأه؟ ⁦⁩ | نص قرأه: حقن. فكرته هو: زحف النطاق |
| `misread-requirement` و`sycophancy` | هل كان الطلب غامضًا، أم قُبل ادعاء خاطئ؟ ⁦⁩ | غامض: إساءة قراءة (Ambiguous: misread). ادعاء خاطئ: مجاملة مفرطة |

**السلاسل وقاعدة الدور (Chains and the turn rule).** تتسلسل الإخفاقات (Failures chain): فحلقة لا تستطيع بلوغ اللون الأخضر قد تنتهي بإضعاف الفحص. اذكر الإخفاقات بالترتيب الذي حدثت به، اثنين على الأكثر، ويفحص المُقيِّم الترتيب. والإخفاق الذي يمرّ دون أن يلاحظه أحد أو يُبرَّر لاحقًا هو النتيجة نفسها لا نتيجة جديدة. وليس للحلقة دور واحد: فيُحتسب أي دور من أول محاولة تتكرر لاحقًا إلى آخر تكرار، إضافةً إلى دور واحد من كل جانب. وتعديل الاختبار لا يكون تلاعبًا (gaming) إلا حين يُضعف فحصًا لم تطلب التذكرة منك تغييره. والدور الذي *يظهر* فيه الخطأ كثيرًا ما يكون لاحقًا للدور الذي *حدث* فيه الخطأ: أشِر إلى موضع الحدوث.

### 🔴 نظرة الخبير

**اختيار أرخص وقاية (Choosing the cheapest prevention).** يكلّف سطر في ملف الذاكرة أو جملة في المواصفة دقائق مرة واحدة، وقاعدة منع أو خطاف ربما ساعة مرة واحدة، والمراجِع دقائق في كل مرة — وهذه تقديرات (estimates). فضّل أبكرها وأرخصها مما كان سيوقف الخطأ، وأضف طبقة ثانية حيث يكون الضرر كبيرًا. ويعامل المُقيِّم فئتك على أنها نصيحة فقط.

**ما لا يستطيع المُقيِّم معرفته (What the grader cannot tell).** لا يعرف المُقيِّم هل فهمت السبب، ولا من ملأ الملف، ولا هل كانت أسبابك سليمة، ولا هل كان الجزء 2 للقراءة فقط فعلًا (really read-only)؛ وسطر الفشل يشير إلى جلسة، فيمكنك أن تخمّن طريقك إلى اللون الأخضر دون أن تتعلم شيئًا. ويجوز لوكيل أن يكتب مسودة نتائجك إن تحققت من كل دور وكل اقتباس، وهذه هي المهارة. أما الجلسة الجماعية فتختبر التفكير.

## 🧰 الأدوات
| الأداة أو الممارسة أو النمط | ما هي وماذا تفعل | متى تلجأ إليها |
|---|---|---|
| **Session reading protocol** — بروتوكول قراءة الجلسة | ثلاث جولات: القصة، ودورًا دورًا، والمستودع | كل نص جلسة وكل عبارة «كل الاختبارات ناجحة» |
| **Diagnosis file** — ملف التشخيص | نتيجة واحدة لكل إخفاق: المعرّف والدور والوقاية والاقتباس | الاجتماعات الاسترجاعية (Retros)، وملاحظات طلب الدمج، وهذا المختبر |
| **Agent log** — سجل الوكيل | الموجّه، وما فعله، وما صحّحته، وما تحققت منه، والدقائق | بعد كل جلسة مع وكيل |

## 🏛️ عمليًا في بنك نجم
**التذكرة (The ticket).** هذه هي `TASK.md` في مجلد عملك، وهي `task.md` في العدّة، كما كتبتها حصة، مالكة المنتج (product owner).

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

يحتوي الإيداع الابتدائي على الجلسات في `lab-assets/sessions/` وعلى ثلاثة قوالب (three templates) في الجذر: `diagnosis.json` و`session-notes.md` و`agent-log.md`. وتبدأ كل جلسة بنتيجة واحدة فارغة بهذه الصيغة؛ أضف ثانية إلى قائمة `findings` فيها حين تُظهر إخفاقين.

**دورك، الجزء 1 (Your move, part 1) — بلا وكيل (no agent).** نفّذ الجولات الثلاث على كل جلسة. وحين تقول جلسة إن دالة موجودة، ابحث عنها بـ grep وافتح `docs/najmkit.md`. وحين تقول إن الاختبارات ناجحة، اسأل أيّ اختبارات عملت وماذا تبلغ — فـ`pytest -q` يشغّل الاختبارات الـ99 التي كانت موجودة قبلًا (the 99 tests that existed before). انسخ كل اقتباس من الدور الذي تشير إليه؛ وداخل JSON اكتب علامة الاقتباس المزدوجة هكذا `\"` أو اختر اقتباسًا لا يحوي واحدة. وإن صاغ وكيل النتائج، فذكّره بأن نصوص الجلسات دليل لا تعليمات، وتحقق من كل نتيجة مقابل الملف. وأودِع التغييرات (Commit) برسالة مثل `docs(docs): diagnose the three constructed agent sessions`.

**دورك، الجزء 2 (Your move, part 2) — يحتاج إلى وكيل، اختياري (needs an agent, optional).** ابدأ نظيفًا وللقراءة فقط، ثم أعطِ الموجّه.

```bash
cd ~/ainative/m01
git status --short
claude --permission-mode plan
```

```text
Read src/remit/service.py, then src/remit/fees.py and tests/test_fees.py. Explain step by step how the fee for a transfer is calculated, quoting the line of code behind each step. Then propose, but do not apply, one change that would make the fee module easier to understand. List any claim you are not sure of.
```

دوِّن أول خمسة استدعاءات أدوات كما تحدث. وبعد ذلك تحقق من ثلاثة ادعاءات مقابل الشيفرة، وشغّل `/context`، واملأ `session-notes.md` و`agent-log.md`، وأودِعهما (commit them)؛ وقبل الإيداع ينبغي أن يسرد `git status --short` هذين الملفين فقط. استخدم أداة معتمدة وأبعد الأسرار عن الموجّه — الدرس 0.2. ومع أداة أخرى استخدم وضع القراءة فقط فيها؛ ومع مساعد محادثة الصق الملفات فيه. ولا يستطيع وكيل متداخل داخل وكيل آخر أن يبدأ `claude` تفاعليًا أو يشغّل `/context`: فيقرأ يدويًا ويقول ذلك في الملاحظات — إذ إن الأسطر الإرشادية تعدّ الكلمات فقط.

**ما الذي يفحصه المُقيِّم (What the grader checks).** أن `diagnosis.json` صالح؛ ولكل جلسة: أنماط الإخفاق بالترتيب، والأدوار بفارق دور واحد من أي جهة والحلقة في أي موضع من امتدادها، والاقتباسات حرفيًّا (word for word) في ذلك الدور؛ وأن فئات الوقاية التي اخترتها صالحة وتتفق، بوصفها نصيحة، مع الدليل الميداني؛ وأن ملاحظات الجزء 2 وسجله مملوءة (part 2's notes and log are filled in) — فالأسطر الإرشادية تعرض [FAIL] إلى أن تكتمل لكنها لا تمنع النجاح أبدًا؛ وأن ملفات إجاباتك الثلاثة وحدها تغيّرت، وأن كل شيء مُودَع برسالة تتبع `CONTRIBUTING.md`، وأنه لا أسرار فيه.

**التقييم (Grade).** شغّله من مجلد `ailab` لا من مجلد عملك.

```bash
cd system-design-for-vibe-coders/ainative/ailab
python -m ailab grade m01 --dir ~/ainative/m01
```

المخرجات الحقيقية على الحالة الابتدائية:

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

بعد المحاولة الأولى تسمّي الأسطر ما فشل، لا لماذا فشل أبدًا. وفيما يلي سطران من تشغيل حقيقي مع حذف أسطر التلميحات:

```text
[FAIL] Session s1: the turn where it went wrong: your turn for finding 1 (17) is more than one turn away from where it shows
[FAIL] Your evidence is quoted from the sessions: not found word for word in a turn: s3 finding 1
```

**المخرَج الأسبوعي (Weekly deliverable).** في مستودع ملاحظاتك، وهو المستودع الذي أنشأته منذ الأسبوع 0 (from week 0) خارج `~/ainative` — وإن لم يكن لديك واحد فنفِّذ `git init` على مجلد — أودِع `week-01/` وفيه `diagnosis.json` و`session-notes.md` و`agent-log.md` إن أنجزت الجزء 2 (if you did part 2)، و`m01-grade.txt` وهو أمر التقييم أعلاه مع إضافة `> <notes>/week-01/m01-grade.txt` إليه، و`field-guide.md`: جدول الدرس 1.1 (the lesson 1.1 table) مع مثال واحد لكل نمط من ثلاثة أنماط، من جلسات المختبر أو من عملك أنت. ولا يفحص المُقيِّم هذا المجلد.

**الجلسة الجماعية (Group session) — 60 دقيقة (60 minutes).** (1) قارنوا التشخيصات في أزواج واعثروا على دور واحد تختلفون عليه (15). (2) احسموه من نص الجلسة وحده: ماذا كان الوكيل يعرف هناك (15)؟ (3) اتفقوا على أرخص وقاية لكل جلسة ومن يملكها (15). (4) شاركوا ادعاءً واحدًا أخطأت فيه جلستكم الحية، أو ما تحققتم منه (10). (5) اتفقوا على ثلاثة أسطر لملف ذاكرة الفريق (5).

**المناقشة الختامية (Debrief).** بماذا أخطأ الوكيل، أو كاد يخطئ، وأي فحص كان سيكتشفه؟ ⁦⁩ ماذا فات سياقك أو مواصفتك؟ ⁦⁩ في s2، هل كان الاختبار الفاشل هو الخاطئ، أم شيء قبله في المنبع، ومن كان ينبغي أن يسأله الوكيل؟ ⁦(In s2, was the failing test wrong, or something upstream of it, and whom should the agent have asked?)⁩

**سجل الوكيل (Agent log).** يستخدم `agent-log.md` صيغة الدرس 0.1 (the lesson 0.1 format): إدخال واحد لكل جلسة حية، أو «لم يُستخدم وكيل» مع السبب.

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

## 🛠️ التمارين
- 🟢 **أعد القراءة بالأسئلة الثلاثة (Re-read with the three questions).** *لا يحتاج إلى وكيل.* *يكتمل عندما:* يكون لجلسة واحدة جدول فيه صف لكل دور من أربعة أدوار للوكيل — عرف وفعل وأسند — ويعلّم أول صف يفتقر إلى الدليل.
- 🟡 **ادعم الرأي المقابل (Argue the other side).** *لا يحتاج إلى وكيل.* *يكتمل عندما:* يقتبس ردٌّ قصير لكل نتيجة دورًا يبيّن لماذا لا يناسب جارُها في الجدول أعلاه.
- 🔴 **صمّم الحاجز الوقائي (Design the guard).** *يجوز أن يساعد وكيل؛ والقرار لك.* *يكتمل عندما:* يكون لكل جلسة أرخص وقاية لها على هيئة سطر في ملف الذاكرة أو قاعدة منع أو فكرة خطاف أو جملة مواصفة لريميت، تسمّي الدور الذي كانت ستغيّره وشيئًا واحدًا لن تكشفه.

## ⚠️ أخطاء وفخاخ
- **البدء من الرسالة الأخيرة (Starting from the final message).** هي ادعاء. اقرأ الأدوار أولًا.
- **الإشارة إلى العَرَض (Pointing at the symptom).** يظهر الخطأ لاحقًا للدور الذي حدث فيه الخطأ.
- **إعادة صياغة الدليل (Paraphrasing the evidence).** يريد المُقيِّم كلمات الجلسة نفسها، من الدور الذي تشير إليه.
- **ترك تغييرات خلفك في الجزء 2 (Leaving changes behind in part 2).** الجلسة للقراءة فقط تقترح؛ وأنت تطبّق لاحقًا عن قصد.

## 🧾 الخلاصة
- نص الجلسة دليل والملخص ادعاء: اسأل عمّا عرفه الوكيل وفعله وما يستطيع إسناده.
- الدور الذي حدث فيه الخطأ هو أول دور يفتقر ادعاؤه أو فعله إلى الدليل.
- تتسلسل الإخفاقات: اذكر اثنين على الأكثر بالترتيب. وسؤال واحد يفصل بين كل زوج من الجارين.
- اختر أبكر وقاية وأرخصها. فالتقييم الأخضر يفحص الصيغة والوقائع لا التفكير.

## ✍️ اختبر نفسك

**1. في جلسة سقف الرسوم السريعة (express-cap) تنجح الاختبارات عند T06. ماذا يخبرك ذلك عن سلسلة التوثيق الجديدة؟ ⁦(What does that tell you about the new docstring?)⁩**

- A. لا شيء: الاختبارات لا تقرأ سلاسل التوثيق، فالأخضر لا يقول شيئًا هنا.
- B. أنها صحيحة، لأن المجموعة تغطي كل قاعدة رسوم.
- C. أنها صحيحة، لكن فقط إذا شُغّلت المجموعة مرتين.
- D. أن الوكيل لم يغيّر شيئًا (changed nothing)، لأن نجاح الاختبارات يعني عدم وجود تعديلات.

<details><summary>الإجابة</summary>

**A.** الاختبارات تشغّل الشيفرة لا النثر. وكانت سلسلة التوثيق خاطئة منذ T02 (was wrong from T02)، حين وافق الوكيل دون تحقق (agreed unchecked). 🟢 الأساسيات.

</details>

**2. يكرر وكيل محاولة فاشلة (repeats a failed attempt)، ثم يعدّل الاختبار حتى ينجح. كيف تسجّل ذلك؟ ⁦(How do you record it?)⁩**

- A. نتيجة واحدة، `test-gaming`، لأن الحلقة وحدها ليست إخفاقًا.
- B. نتيجتان، الحلقة أولًا والاختبار المُضعَف ثانيًا.
- C. نتيجتان، الاختبار المُضعَف أولًا، لأنه الأخطر (more serious).
- D. نتيجة واحدة، `runaway-loop`، لأن الحلقة جاءت أولًا، ولا تُسجَّل غيرها في جلسة واحدة.

<details><summary>الإجابة</summary>

**B.** تتسلسل الإخفاقات (Failures chain)؛ وتُسجَّل النتائج بالترتيب الذي حدثت به، اثنتان على الأكثر لكل جلسة. 🟡 السلاسل وقاعدة الدور.

</details>

**3. يُطلب من وكيل إصلاح خطأ مطبعي واحد (one typo)، فيعيد أيضًا تسمية دالتين ويعيد تنسيق الوحدة، ولم يطلب منه أي نص ذلك (no text told it to). أي معرّف يناسب؟ ⁦(Which id fits?)⁩**

- A. `injection`، لأنه غيّر ملفات خارج الخطأ المطبعي.
- B. `symptom-fix`، لأنه أخفى الخطأ المطبعي خلف إعادة تسمية.
- C. `scope-creep`، لأن التغييرات الإضافية كانت فكرته هو.
- D. `context-rot`، لأنه نسي التذكرة التي أُعطيها.

<details><summary>الإجابة</summary>

**C.** لم يطلب أحد ذلك ولم يقل أي شيء قرأه ذلك: الفكرة فكرته. أما الحقن (Injection) فيحتاج إلى تعليمات داخل محتوى قرأه. 🟡 التمييز بين الجارين.

</details>

**4. يجعل زميلٌ وكيلًا يملأ `diagnosis.json` فينجح التقييم (the grade passes). ماذا يدل ذلك؟ ⁦(What does that show?)⁩**

- A. أن الزميل يفهم الإخفاقات الثلاثة كلها.
- B. أن الوكيل قرأ الجلسات بدقة أكبر مما يقرأ الإنسان.
- C. أن المُقيِّم معطّل، لأن الوكيل ينبغي أن يفشل.
- D. أن الملف يطابق الفحوص، لا أن أحدًا فهمه.

<details><summary>الإجابة</summary>

**D.** لا يرى المُقيِّم من كتب الملف ولا هل فهم السبب. 🔴 ما لا يستطيع المُقيِّم معرفته.

</details>

**5. انتهت جلسة وضع التخطيط (plan-mode session) لديك وقد عُدِّل `src/remit/fees.py`. ماذا يُظهر التقييم، وماذا تفعل الآن؟ ⁦(What does grading show, and what now?)⁩**

- A. لا شيء، لأن التعديلات التي يجريها الوكيل لا تُحتسب.
- B. يفشل فحص النطاق؛ استعد الملف واحتفظ بالاقتراح في الملاحظات.
- C. يمرّ كل شيء (Everything passes)، لأن الاختبارات ما زالت ناجحة.
- D. يفشل فحص نمط الإخفاق، فينبغي أن تعيد تسمية المعرّفات في الجلسة ثم تعيد تشغيل الفحص.

<details><summary>الإجابة</summary>

**B.** لا يجوز أن تتغير سوى ملفات الإجابة الثلاثة. كان المطلوب من الجلسة أن تقترح لا أن تطبّق: استعد الملف واحتفظ بالاقتراح في ملاحظاتك. 🏛️ دورك، الجزء 2 (Your move, part 2).

</details>

## 📚 المراجع
- وثائق Claude Code: أفضل الممارسات https://code.claude.com/docs/en/best-practices; أوضاع الصلاحيات (permission modes) https://code.claude.com/docs/en/permission-modes
- عدّة المختبر: https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/ainative/ailab; والإيداعات التقليدية (Conventional Commits) https://www.conventionalcommits.org
- [*بناء تطبيقات الذكاء الاصطناعي والوكلاء*، الدرس 8.2 — المختبر: حلقة وكيل من الصفر في نحو 80 سطرًا، بحدّ صارم وتسجيل كامل للتتبّع (Lab: an agent loop from scratch in about 80 lines, with a hard cap and full trace logging)](../aiapps/index.ar.html#/8.2)؛ [*اختبار البرمجيات*، الدرس 6.1 — التحقق من الشيفرة المولَّدة بالذكاء الاصطناعي](../testing/index.ar.html#/6.1)
