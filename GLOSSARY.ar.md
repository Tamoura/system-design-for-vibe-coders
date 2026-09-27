# المسرد (Glossary) — بلغة بسيطة (plain language)، بلا شروط مسبقة (no prerequisites)

كل مصطلح تستخدمه الدورة، معرَّفًا لقارئ لم يكتب كودًا (code) قط. المصطلح الإنجليزي (English term) مُبقى لأنك ستراه في أدواتك. المرآة الإنجليزية (English mirror): [GLOSSARY.md](./GLOSSARY.md).

## الأجهزة (The machines)

| المصطلح (Term) | English | المعنى ببساطة (Plain meaning) |
|---|---|---|
| الخادم | Server | حاسوب (computer) يشغّل منتجك طوال اليوم ولا ينام. مستأجَر (rented) غالبًا، يقبع في مركز بيانات (data center). |
| العميل | Client | ما يمسكه المستخدم (the user): متصفح (browser) أو تطبيق هاتف (phone app) أو تطبيق تلفاز (TV app). هو يسأل والخادم (server) يجيب. |
| الخادم الافتراضي | VPS | شريحة مستأجرة من حاسوب كبير (a rented slice of a big computer) تتصرف كأنها خادمك (your server) الخاص. |
| السحابة | The cloud | خوادم (servers) غيرك، تُستأجر بالساعة (rented by the hour). |
| مركز البيانات | Data center | المستودع المليء بالخوادم (the warehouse full of servers) حيث تعيش «السحابة (the cloud)» فعليًا. |

## رحلة الطلب (The journey of a request)

| المصطلح (Term) | English | المعنى ببساطة (Plain meaning) |
|---|---|---|
| الطلب / الاستجابة | Request / Response | العميل (client) يسأل (طلب (request)) والخادم (server) يجيب (استجابة (response)). الويب (web) كله هذا، مليارات المرات (billions of times). |
| نظام أسماء النطاقات | DNS | دليل هاتف الإنترنت (the internet's phone book): يحوّل الاسم (`relay.app`) إلى عنوان خادم (address of a server). |
| النطاق | Domain | اسم منتجك العلني (your product's public name) على الإنترنت. |
| HTTP / HTTPS | — | اللغة التي تُنطق بها الطلبات والاستجابات (the language requests and responses are spoken in)؛ حرف S يعني أنها مشفّرة (encrypted). |
| التشفير والشهادة | TLS / Certificate | القفل (the lock) الذي يجعل HTTPS خاصًا، والوثيقة التي تثبت أن الموقع موقعك حقًا (the paper that proves the site is really you). |
| شبكة توزيع المحتوى | CDN | سلسلة حواسيب مساعدة (helper computers) حول العالم تحفظ نسخًا من صفحاتك قريبًا من المستخدمين (users) لتسرع التحميل (load fast) — وتحمي خادمك (your server). |
| الحافة | Edge | حواسيب الـCDN (the CDN's computers) القريبة من المستخدم (مقابل «الأصل» (origin)). |
| الخادم الأصل | Origin | خادمك (your server) الفعلي خلف الـCDN. |
| الوسيط العكسي | Reverse proxy | برنامج البوّاب (doorman program) على خادمك (غالبًا nginx): يستقبل كل طلب (request) ويوجهه إلى البرنامج الداخلي الصحيح (the right internal program). |
| الترويسة | Header | ورقة ملاحظات ملصقة (a sticky note) على الطلب أو الاستجابة (a request or response): ممن هو، وكم يُحفظ، وما شكله. تقرؤها الآلات (Machines read these). |
| الكمون | Latency | زمن الذهاب والإياب (round trip). يُقاس بأجزاء الثانية (in milliseconds) ويُحَس بالصبر. |

## الكود والإطلاق (Code and shipping)

| المصطلح (Term) | English | المعنى ببساطة (Plain meaning) |
|---|---|---|
| الكود | Code | تعليمات منتجك (your product's instructions) مكتوبةً بدقة تكفي لتتبعها آلة. |
| المستودع | Repo | مجلد المنتج (the product's home folder) مع تاريخه الكامل من النسخ المحفوظة (تحفظه أداة اسمها git). |
| الإيداع | Commit | نسخة محفوظة واحدة (one saved version) في ذلك التاريخ، مع ملاحظة عمّا تغيّر. |
| الفرع | Branch | مسودة موازية (a parallel draft) للمنتج تُجرى فيها التغييرات بأمان قبل ضمّها إلى النسخة الرئيسة (the main version). |
| طلب الدمج | PR | اقتراح: «هذه تغييراتي — راجعوها قبل أن تنضم إلى النسخة الرئيسة (the main version).» |
| النشر | Deploy | نسخ إصدار (release) مختار من الكود (code) إلى الخادم الدائم (the always-on server) ليستلمه العالم. |
| التراجع | Rollback | نشر (deploy) نسخة أمسِ السليمة (yesterday's known-good version) لأن نسخة اليوم أخطأت. |
| البناء | Build | الخطوة التي تحوّل الكود (code) المكتوب إلى الملفات المحسَّنة (the optimized files) التي يشغّلها الخادم (server) فعلًا. |
| البيئة | Environment | نسخة كاملة من نظامك (one complete copy of your system): جهازك (محلية (local))، ونسخة بروفة (تجهيز (staging))، والحقيقية (إنتاج (production)). |
| متغير البيئة | Env var | إعداد مسمّى (a named setting) يقرؤه الكود (code) وقت التشغيل (runtime) — كأي قاعدة بيانات (database) يستخدم — يختلف بين البيئات. |
| التكامل المستمر | CI | روبوت (robot) يشغّل فحوصك (اختبارات (tests) وقواعد (rules)) تلقائيًا على كل تغيير مقترح (proposed change). |
| النشر الأزرق-الأخضر | Blue-green | إبقاء نسختين من التطبيق وتحويل الحركة (switch traffic) إلى الجديدة فقط بعد أن تثبت صحتها — فلا ينقطع المستخدمون (users). |

## البيانات (Data)

| المصطلح (Term) | English | المعنى ببساطة (Plain meaning) |
|---|---|---|
| قاعدة البيانات | Database | الدفتر الذي لا يضيّعه منتجك أبدًا (The notebook your product never loses): المستخدمون والمحتوى والطلبات (users, content, orders) — مصدر الحقيقة (source of truth). |
| مخطط البيانات | Schema | الشكل المتفق عليه للمخزون (the agreed shape of what's stored): ممَّ يتكون سجل «المستخدم» (a user record) وما الذي يميّزه. |
| الاستعلام | Query | سؤال يُطرح على قاعدة البيانات (a question asked of the database). |
| الفهرس | Index | فهرس محتويات القاعدة (the database's table of contents) — الفرق بين إيجاد سجل فورًا (finding a record instantly) وقراءة الدفتر كله. |
| الهجرة | Migration | تغيير منضبط (a controlled change) في شكل البيانات (data) أو مسكنها. |
| تخزين الكائنات | Object storage | مستودع الملفات الكبيرة (صوت وصور وفيديو (audio, images, video)) — منفصل عن قاعدة البيانات (database). |
| النسخة الاحتياطية | Backup | نسخة من البيانات (data) تستطيع إعادة بناء (rebuild) المنتج منها. لا تصير حقيقية إلا بعد أن تتدرب على استعادتها (restoring it). |
| الاحتفاظ / أجل البقاء | Retention / TTL | كم تُحفظ البيانات (data) قبل حذفها تلقائيًا (automatic deletion). |
| الكاش | Cache | ذاكرة قصيرة سريعة (a fast short-term memory) تحفظ نسخًا من الإجابات الأخيرة (copies of recent answers) كي يُسأل المصدرُ البطيء الصادق (the slow, true source) أقل. قد يختفي في أي لحظة — عن قصد. |
| إبطال الكاش | Invalidation | حذف إجابة مخزنة (a cached answer) لأن الحقيقة تغيّرت. إحدى المسألتين الصعبتين الشهيرتين (one of the two famously hard things). |

## الحسابات والأمان (Accounts and safety)

| المصطلح (Term) | English | المعنى ببساطة (Plain meaning) |
|---|---|---|
| المصادقة | Auth | إثبات من أنت (تسجيل الدخول (login)). أما التخويل (authorization) فما يُسمح لك بفعله. |
| الرمز | Token | تصريح مؤقت (a temporary pass) يحمله العميل (client) ليثبت أنه سجّل الدخول من قبل. |
| — | OAuth | «الدخول بجوجل/آبل» (Sign in with Google/Apple): استعارة تسجيل دخول من مزوّد (provider) بدل كلمة مرور جديدة (a new password). |
| تحديد المعدل | Rate limiting | «حدٌّ أقصى N طلبًا (requests) في الدقيقة» — الحارس (the bouncer) الذي يمنع السكربتات (scripts) من إغراقك. |
| اختبار البشرية | CAPTCHA / Turnstile | بوابة «أثبت أنك إنسان» (the prove-you're-human gate) على النماذج (forms). |
| — | SSRF | خداع الخادم (Tricking a server) ليطلب أماكن لا ينبغي له (كدواخله هو). من الهجمات الكلاسيكية (classic attacks). |
| — | OWASP Top 10 | قائمة مجتمع الأمن (the security community's list) بأشيع عشر طرق تُخترق بها تطبيقات الويب (web). |
| السر | Secret | كلمة مرور (password) أو مفتاح (key) أو رمز (token) يحمله نظامك. لا يسكن الكود (code) أبدًا، ولا المحادثة (chat)، ويُبدَّل إذا انكشف (rotated when exposed). |

## التشغيل (Operating)

| المصطلح (Term) | English | المعنى ببساطة (Plain meaning) |
|---|---|---|
| المراقبة | Observability | قدرتك على رؤية ما يفعله نظامك: سجلات وأخطاء ومقاييس (logs, errors, metrics) — كي توقظ مشكلةُ الثالثة فجرًا لوحةً (a dashboard) لا مستخدمًا (a user). |
| السجل | Log | يوميات النظام (the system's diary): سطر لكل حدث (one line per thing that happened). |
| المقياس | Metric | رقم يُتتبع عبر الزمن (طلبات/دقيقة، أخطاء/ساعة (requests/minute, errors/hour)). |
| التشغيل / الانقطاع | Uptime / Downtime | زمن عمل منتجك (the time your product is working) / وزمن تعطله (not working). |
| الحادثة | Incident | النافذة بين «شيء ما خطأ» (something is wrong) و«أُصلح وفُهم» (it's fixed and understood). |
| تشريح الحادثة | Postmortem | الكتابة الصادقة بعدها (the honest write-up afterward): الأعراض والسبب والإصلاح والدرس (symptoms, cause, fix, lesson). من هذه بُنيت الدورة (This course is built from these). |
| مفتاح الميزة | Feature flag | مفتاح تشغيل/إيقاف (an on/off switch) لميزة، يُتحكم به دون إعادة نشر (redeploying). |
| الوظيفة الخلفية | Background job | عمل يؤديه النظام على جدوله الخاص (إرسال نشرة (send newsletter)، تنظيف (clean up)) — لا أحد يراقب (nobody is watching)، فيلزمه قفل وسجل وإيصال (locks, records, and receipts). |
| آمن التكرار | Idempotent | يجوز تشغيله مرتين (Safe to run twice): إعادته لا تغيّر شيئًا زائدًا. الخاصية التي تجعل المحاولات المتكررة (retries) بلا ضرر. |
| الطابور | Queue | صف انتظار للعمل (a waiting line for work): تُلقى فيه المهام (tasks) ويسحبها العمال (workers) بوتيرة محتملة (at a sustainable pace). |
| — | Webhook | نظامٌ يقرع جرس نظامٍ آخر (ringing another's doorbell) حين يقع حدث (when something happens). |

## توجيه الوكلاء (Directing agents)

| المصطلح (Term) | English | المعنى ببساطة (Plain meaning) |
|---|---|---|
| الوكيل | Agent | ذكاء اصطناعي (AI) يستطيع الفعل (كتابة كود (write code)، تنفيذ أوامر (run commands)) لا المحادثة (chat) فقط. بنّاؤك (your builder). |
| — | CLAUDE.md | ملف الذاكرة الدائم (standing memory file) للوكيل (agent) في مستودعك (your repo): ما المنتج، والقواعد (the rules)، والمعمارية (architecture). وصفُ وظيفته (Its job description). |
| السياق | Context | كل ما يراه الوكيل (agent) الآن. ينسى بين الجلسات (sessions) — ولهذا وُجدت ملفات الذاكرة (memory files). |
| الموجّه | Prompt | التعليمة (the instruction) التي تعطيها. الجيدة تحمل هدفًا وقيودًا ودليلًا (a goal, constraints, and the evidence) تطالب به. |
| الخطّاف | Hook | قاعدة تلقائية (An automatic rule) تعمل في لحظات محددة (قبل كل إيداع (every commit) مثلًا) — تفرض ما لا تفرضه الذاكرة وحدها (memory alone). |
| المهارة | Skill | إجراء محفوظ قابل للتكرار (a saved, repeatable procedure) يشغّله الوكيل (مهارة نشر (a deploy skill)، مهارة تدقيق (an audit skill)). |
| حاجز الأمان | Guardrail | كل حماية آلية (mechanical protection) — خطّاف (hook) أو اختبار (test) أو تأكيد (assertion) — توقف خطأً معروفًا (a known mistake) دون أن يتذكره إنسان. |
| كاشف الانجراف | Drift guard | اختبار يفشل (a test that fails) حين يكفّ شيئان يجب تطابقهما عن التطابق (قائمة مقابل الواقع (a list vs reality)). |
| التحقق | Verification | مطالبةٌ بالدليل (Demanding evidence) من الطبقة التي يلمسها المستخدم (the layer the user touches) بدل الثقة بكلمة «تم» (done). روحُ هذه الدورة (The soul of this course). |
