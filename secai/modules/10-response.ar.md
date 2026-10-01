# الوحدة 10 — الرصد والاستجابة (Detection and response)

*يخفق المنع أحيانًا (Prevention sometimes fails)، حتى في مصرفٍ حسن الإدارة (even in a well-run bank). وتتناول هذه الوحدة ما يحدث بعد ذلك (what happens next): ملاحظة الهجوم وهو لا يزال صغيرًا (noticing an attack while it is still small)، والتعامل معه بهدوء حين يقع (handling it calmly when it lands)، وسدّ مواطن الضعف التي يكتشفها الآخرون (closing the weaknesses that others find) قبل أن يستغلّها المهاجمون (before attackers use them). وهي تبدأ بالتسجيل والمراقبة وهندسة الرصد (logging, monitoring and detection engineering): ما الذي يُسجَّل (what to record)، وكيف تبقى السجلات جديرةً بالثقة وخاصة (how to keep logs trustworthy and private)، وكيف تتحوّل المعرفة بسلوك المهاجمين (knowledge of attacker behaviour) إلى تنبيهاتٍ مُختبَرة (tested alerts)، بما في ذلك تنبيهات تطبيقات النماذج اللغوية الكبيرة والوكلاء (alerts for LLM apps and agents). ثم تستعرض دورة حياة الاستجابة للحوادث (the incident response life cycle)، من الاستعداد (from preparation) إلى مراجعة ما بعد الحادثة (to the post-incident review)، مع الخطوات الإضافية التي تحتاجها حادثة الذكاء الاصطناعي (the extra steps an AI incident needs). وتنتهي بإدارة الثغرات والإفصاح عنها (vulnerability management and disclosure): ترتيب أولويات الإصلاحات (prioritising fixes) باستخدام CVSS وEPSS وكتالوج CISA KEV (the CISA KEV catalogue)، ونشر سياسة إفصاح (publishing a disclosure policy)، وتقرير متى يستحق برنامج مكافآت الثغرات العناء (deciding when a bug bounty is worth it). ستتابع فريق أمن التطبيقات والذكاء الاصطناعي في بنك نجم (Najm Bank's Application & AI Security team) بينما يكتشف علي أين تذهب سجلات نجم أسيست فعلًا (where Najm Assist's logs really go)، ويدير جاسم حادثةً في ليلة خميس (runs a Thursday-night incident) سببها مقالٌ مسموم في قاعدة المعرفة (a poisoned knowledge-base article)، ويسأل حمد لماذا بقيت رسالة باحثةٍ بلا ردّ ثلاثة أسابيع (why a researcher's email sat unanswered for three weeks).*

> **المراحل (Phases):** Operate, Respond — رؤية الهجمات أثناء حدوثها (seeing attacks while they happen)، والاستجابة بطريقةٍ متمرَّسٍ عليها حين تقع (responding in a practised way when they land)، وإصلاح مواطن الضعف المعروفة (fixing known weaknesses) بحسب ترتيب مخاطرها الحقيقية (in order of real risk).

---

# 10.1 — التسجيل والمراقبة وهندسة الرصد (Logging, monitoring and detection engineering)
*المستوى (Level): 🔴 متقدم (Advanced)* · *المتطلبات (Prerequisites): 1.1، 5.3، 9.1* · *المرحلة (Phase): Operate*

## ⚡ الدرس في دقيقة (In 60 seconds)
- **التسجيل (Logging)** يدوّن الأحداث ذات الصلة بالأمن (records security-relevant events)، و**المراقبة (monitoring)** تتابعها (watches them)، و**هندسة الرصد (detection engineering)** تحوّل المعرفة بسلوك المهاجمين (turns knowledge of attacker behaviour) إلى قواعد مُختبَرة (tested rules) تُطلق تنبيهاتٍ يتصرّف بناءً عليها شخصٌ ما (raise alerts a person acts on).
- سجّل الأحداث المهمة (Log the events that matter)، أي تسجيلات الدخول (sign-ins)، ورفض الوصول (access denials)، والإجراءات عالية القيمة (high-value actions)، والتغييرات الإدارية (admin changes)، وفي أنظمة الذكاء الاصطناعي (for AI): استدعاءات الأدوات (tool calls)، وأحكام الضوابط الوقائية (guardrail verdicts)، والمستندات المسترجَعة (retrieved documents)؛ وسجّلها بصيغةٍ **مُهيكَلة (structured)**، مع طوابع زمنية بتوقيت **UTC** (UTC timestamps) و**معرّف طلب (request ID)** يربط بين الخدمات (that links services).
- السجلات مخزن بيانات (Logs are a data store) له مخاطر اختراقٍ خاصة به (with their own breach risk). لا تسجّل أبدًا كلمات المرور أو الرموز المميزة أو المفاتيح أو أرقام البطاقات الكاملة (Never log passwords, tokens, keys or full card numbers).
- انقل السجلات بسرعة خارج الجهاز (Ship logs off the machine quickly) إلى مخزنٍ مركزي مقاوم للعبث (a tamper-resistant central store)، وأطلِق تنبيهًا حين **يصمت مصدرٌ (a source goes silent)**.
- عامِل كل قاعدة رصدٍ معاملة الشيفرة (Treat each detection as code): مالك (owner)، واختبار (test)، ومعدّل إيجابياتٍ كاذبة معروف (known false-positive rate)، ودليل استجابة (playbook). ارصد **السلوك (behaviour)**، أي تقنيات MITRE ATT&CK وATLAS (MITRE ATT&CK and ATLAS techniques)، لا عناوين IP وحدها (not only IP addresses)، فالمهاجمون يغيّرونها في دقائق (which attackers change in minutes).
- أكبر فخ (Biggest trap): تسجيل كل شيء (logging everything)، والتنبيه على كل شيء (alerting on everything)، ثم عدم رؤية أي شيء (and seeing nothing).

## 🧭 لماذا يهم (Why it matters)
بعد ستة أسابيع من بدء التجربة الأولية لنجم أسيست (Six weeks into Najm Assist's pilot)، يطلب جاسم، قائد مركز العمليات الأمنية والاستجابة للحوادث (SOC and incident response lead)، من علي سجلاتِ المساعد (asks Ali for its logs). فيجدها علي في حاوية التصحيح التابعة لفريق التطبيق (the app team's debug bucket). وهي تحوي نصّ المحادثات كاملًا (full conversation text)، بما في ذلك أرقام البطاقات التي كتبها العملاء (card numbers customers typed)، لكنها لا تبيّن أيّ أداةٍ استُدعيت (which tool was called)، ولا لصالح من (for whom)، ولا ما إذا كان ذلك مسموحًا (whether it was allowed). والساعات غير متطابقة (Clocks disagree)، وكل شيءٍ يُحذف بعد سبعة أيام (everything is deleted after seven days). فلو جمّد نجم أسيست البطاقة الخطأ (If Najm Assist froze the wrong card)، لما استطاع أحدٌ إثبات ما حدث (nobody could prove what happened)، وقد أصبحت هذه الحاوية الآن أكثر مخازن البيانات حساسيةً في المشروع (the project's most sensitive data store).

إن «إخفاقات التسجيل والمراقبة الأمنية» ("Security Logging and Monitoring Failures") فئةٌ في قائمة OWASP Top 10 (a category in the OWASP Top 10)، وهي A09 في إصدار 2021 (A09 in the 2021 edition)، ويعيد تحديث 2025 تسميتها (the 2025 update renames it) «إخفاقات التسجيل والتنبيه الأمني» ("Security Logging and Alerting Failures")، فتحقّق من القائمة الحالية (so check the current list)؛ وسبب ذلك أن الاختراقات كثيرًا ما تُكتشف متأخرة (because breaches are so often found late)، وعلى يد جهاتٍ خارجية (and by outsiders). ففي اختراق Equifax عام 2017 (In the Equifax breach of 2017)، أفادت مراجعاتٌ حكومية أمريكية نُشرت عام 2018 (US government reviews published in 2018) بأن جهازًا لفحص حركة المرور المشفّرة (a device for inspecting encrypted traffic) كانت شهادته منتهية الصلاحية (had an expired certificate)، فلم يكن يفحص تلك الحركة (so it was not inspecting that traffic)؛ وما إن جُدّدت الشهادة (once the certificate was renewed) حتى لاحظ الموظفون النشاط المريب (staff noticed the suspicious activity). إن ضابط المراقبة الذي يتوقف عن العمل بصمت (A monitoring control that silently stops working) أسوأ من عدم وجوده أصلًا (is worse than none)، لأن الجميع يعتقدون أنهم محميّون (because everyone believes they are covered).

وتلخّص نورة، رئيسة أمن التطبيقات والذكاء الاصطناعي (Head of Application & AI Security)، الأمر قائلةً: «إن لم يُسجَّل، فهو لم يحدث (If it isn't logged, it didn't happen). وإن لم ينظر إليه أحد، فهو أيضًا لم يحدث (If nobody looks, it still didn't happen). وإن سُجّل ومعه رقم بطاقة، فقد صنعنا حادثةً ثانية (If it's logged with a card number, we've created a second incident).»

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**المفردات (Vocabulary).** **الحدث (event)** يدوّن أن شيئًا ما قد حدث (records that something happened)؛ و**السجلّ (log)** تدفّقٌ من الأحداث (a stream of them). و**SIEM**، أي منصة إدارة المعلومات والأحداث الأمنية (security information and event management platform)، تجمع السجلات من مصادر كثيرة (collects logs from many sources)، وتوحّدها في حقولٍ مشتركة (normalises them into common fields)، وتجعلها قابلةً للبحث (makes them searchable)، وتشغّل قواعد الرصد (runs detection rules). و**قاعدة الرصد (detection)** منطقٌ يشير إلى حدثٍ أو نمطٍ مريب (logic that flags a suspicious event or pattern)؛ وحين تنطلق (when it fires) تُنشئ **تنبيهًا (alert)**. ويتولّى **مركز العمليات الأمنية (SOC, security operations centre)**، وهو فريق جاسم، **فرز (triages)** التنبيهات، أي تقرير ما إذا كان كلٌّ منها حقيقيًا (deciding whether each is real) ومدى إلحاحه (and how urgent)، ثم يبدأ الاستجابة للحوادث (starts incident response) (10.2).

**ما الذي يُسجَّل (What to log).** تقدّم ورقة OWASP المختصرة للتسجيل (OWASP Logging Cheat Sheet) وورقة OWASP المختصرة لمفردات التسجيل (Logging Vocabulary Cheat Sheet) قائمة بدايةٍ جيدة (a good starting list). وفي بنك نجم (At Najm Bank):

| عائلة الأحداث (Event family) | أمثلة (Examples) | ما الذي تتيح لك اكتشافه (What it lets you catch) |
|---|---|---|
| المصادقة (Authentication) | نجاح تسجيل الدخول وفشله (Sign-in success and failure)، وتحدّي المصادقة متعددة العوامل (MFA challenge)، وإعادة تعيين كلمة المرور (password reset)، وجهازٌ جديد (new device) | حشو بيانات الاعتماد (Credential stuffing)، والاستيلاء على الحساب (account takeover) (3.1) |
| التفويض (Authorisation) | رفض الوصول (Access denied)، وفشل فحص ملكية الكائن (object-ownership check failed) | استكشاف ثغرات IDOR وBOLA (IDOR and BOLA probing) (3.3، 4.1) |
| التحقق من المدخلات (Input validation) | الحمولات المرفوضة (Rejected payloads)، وأنواع الملفات المحجوبة (blocked file types) | استكشاف ثغرات الحقن والرفع (Injection and upload probing) (2.1، 2.3) |
| الإجراءات عالية القيمة (High-value actions) | التحويل (Transfer)، والمستفيد الجديد (new beneficiary)، وتغيير الحدود (limit change)، وتجميد البطاقة (card freeze) | الاحتيال وإساءة استخدام مسارات العمل (Fraud and business-flow abuse) (4.2) |
| الإدارة والإعدادات (Admin and configuration) | منح دور (Role granted)، وتغيير علامة ميزة (feature flag changed)، وقراءة سرّ (secret read)، وتغيير إعدادات التسجيل (logging changed) | إساءة الاستخدام من الداخل (Insider misuse)، وثبات المهاجم (attacker persistence) |
| أنظمة الذكاء الاصطناعي (AI systems) | استدعاء الأداة والقرار بشأنه (Tool call and decision)، وحكم الضابط الوقائي (guardrail verdict)، ومعرّفات المستندات المسترجَعة (retrieved document IDs)، وإصدار الموجّه والنموذج (prompt and model version) | حقن الموجّهات (Prompt injection)، والصلاحيات المفرطة (excessive agency)، والاستهلاك غير المحدود (unbounded consumption) (8.2، 9.2) |

**ما يحتاجه كل حدث (What every event needs).** *مَن (Who)*: هوية المستخدم أو الخدمة (user or service identity)، مستعارةً حيثما أمكن (pseudonymised where possible)؛ و*ماذا (what)*: اسم حدثٍ من مفرداتٍ ثابتة (an event name from a fixed vocabulary)، مثل `authn_login_fail`؛ و*متى (when)*: بتوقيت UTC، وبصيغة ISO 8601، وبساعاتٍ متزامنة (synchronised clocks)؛ و*أين (where)*: الخدمة والمضيف وعنوان IP المصدر (service, host, source IP)؛ و*النتيجة (outcome)*: نجاحٌ أو فشلٌ أو رفض، مع السبب (success, failure or denied, with a reason)؛ و**معرّف ربط (correlation ID)** يربط طلب الهاتف المحمول واستدعاء واجهة البرمجة والكتابة في قاعدة البيانات معًا (tying the mobile request, API call and database write together).

**ما لا يدخل السجل أبدًا (What never goes in a log).** كلمات المرور (Passwords)، ورموز الاستخدام لمرةٍ واحدة (one-time codes)، والرموز المميزة والمفاتيح (tokens and keys) (5.2)؛ وأرقام البطاقات الكاملة (full card numbers)؛ ورموز أمان البطاقات (card security codes)، التي يحظر معيار PCI DSS الاحتفاظ بها بعد التفويض في أي مكان (which PCI DSS forbids keeping after authorisation anywhere)، بما في ذلك السجلات (logs included)؛ والبيانات الشخصية التي لا تحتاجها (personal data you do not need) (5.3). ويسمّي CWE-532 هذا الضعف (names this weakness).

```python
# Vulnerable: secret in the log, free text, user input written raw
log.info(f"Login failed for {username} with password {password}")
```

```python
# Fixed: event name, structured fields, no secret, pseudonymous user
log.warning("authn_login_fail", extra={
    "event": "authn_login_fail",
    "user_ref": pseudonymise(username),   # keyed hash, not the raw value
    "src_ip": client_ip,
    "request_id": request_id,
    "reason": "bad_credentials",
})
# A JSON formatter writes one line per record and escapes control characters.
```

يُسرّب الإصدار الأول كلمة المرور (The first version leaks the password). كما أنه يسمح بـ**حقن السجلات (log injection)** (CWE-117): فـ«اسم مستخدم» ("username") يحتوي على فاصل سطر (containing a line break) يستطيع تزوير سطر سجلٍّ إضافي (can forge an extra log line)، مثل تسجيل دخولٍ ناجح مزيّف (such as a fake successful sign-in). والمخرجات المُهيكَلة والمُهرَّبة (Structured, escaped output) توقف ذلك (stops that)، واسم الحدث الثابت (a fixed event name) يسهل عدّه (is easy to count).

**المراقبة ليست رصدًا (Monitoring is not detection).** لا تفيد لوحة المعلومات (A dashboard helps) إلا إذا كان أحدٌ يتابعها في اللحظة المناسبة (only if someone is watching at the right moment). أما قاعدة الرصد فتنطلق من تلقاء نفسها (A detection fires on its own) وتسلّم شخصًا مسمّى تنبيهًا (hands a named person an alert) مع سياقٍ يكفي للتصرّف (with enough context to act).

### 🟡 التعمق أكثر (Going deeper)

```mermaid
flowchart RL
    A["التطبيقات وواجهات البرمجة ونجم أسيست<br/>(Apps, APIs, Najm Assist)"] --> B["ناقل السجلات<br/>(Log shipper)"]
    K["سجلات التدقيق السحابية<br/>(Cloud audit logs)"] --> B
    B --> C["المخزن المركزي: إلحاق فقط<br/>(Central store: append-only)"]
    C --> D["منصة إدارة الأحداث الأمنية: توحيد وربط<br/>(SIEM: normalise and correlate)"]
    D --> E["قواعد رصد من مستودع الشيفرة<br/>(Detection rules from git)"]
    E --> F["تنبيه مع سياق<br/>(Alert with context)"]
    F --> G["فرز مركز العمليات الأمنية<br/>(SOC triage)"]
    G -->|"حقيقي (Real)"| H["الاستجابة للحوادث<br/>(Incident response)"]
    G -->|"إيجابية كاذبة (False positive)"| I["ضبط القاعدة<br/>(Tune the rule)"]
    I --> E
    C --> J["فحص سلامة المصادر<br/>(Source health check)"]
    J -->|"مصدر صامت (Source silent)"| F
```

**احمِ خط النقل (Protect the pipeline).**
- **أخرِج السجلات من الجهاز بسرعة (Get logs off the box fast).** يستطيع مهاجمٌ على خادمٍ ما (An attacker on a server) حذف سجلاته المحلية (can delete its local logs)، وهي تقنية *إزالة المؤشرات (Indicator Removal)* في ATT&CK. انقل الأحداث خلال ثوانٍ (Ship events within seconds) إلى حسابٍ منفصل لا يستطيع فريق التطبيق تغييره (to a separate account the application team cannot change)، مع تخزينٍ بنمط الكتابة مرةً واحدة للأرشيف (with write-once storage for the archive).
- **زامِن الوقت (Synchronise time).** استخدم بروتوكول NTP وتوقيت UTC في كل مكان (Use NTP and UTC everywhere)؛ فالخط الزمني المبني على ساعاتٍ يفصل بينها أربع دقائق (a timeline from clocks four minutes apart) يعطي إجاباتٍ خاطئة (gives wrong answers).
- **راقب الصمت (Watch for silence).** لكل مصدرٍ حجمٌ متوقَّع (Each source has an expected volume)؛ والهبوط إلى الصفر (a drop to zero) يُطلق تنبيهًا (raises an alert). وهذا هو درس Equifax (That is the Equifax lesson).
- **خط النقل نفسه سطح هجوم (The pipeline is attack surface).** كانت Log4Shell (CVE-2021-44228، ديسمبر 2021) خللًا في مكتبة تسجيل (a flaw in a logging library): فتسجيل سلسلةٍ نصية يتحكم فيها المهاجم (logging an attacker-controlled string) قد يجعل الخادم يجلب شيفرةً بعيدة ويشغّلها (could make the server fetch and run remote code). حدِّث مكوّنات التسجيل كأي اعتمادية (Patch logging components like any dependency) (6.2)، وهرِّب المخرجات في عارضات السجلات (escape output in log viewers) لتجنّب البرمجة النصية المخزَّنة عبر المواقع (to avoid stored XSS) (2.2).
- **مدة الاحتفاظ متطلَّبٌ إلزامي (Retention is a requirement).** يشترط معيار PCI DSS v4.0.1 الاحتفاظ بسجلات التدقيق للأنظمة الداخلة في النطاق (requires audit logs for in-scope systems to be kept) مدةً لا تقل عن 12 شهرًا (at least 12 months)، على أن تكون الأشهر الثلاثة الأخيرة متاحةً فورًا (the latest three immediately available). وتحدّد سارة، مسؤولة حماية البيانات (DPO)، مع فريق الامتثال (and compliance) الباقي (set the rest).

**هندسة الرصد بوصفها دورة حياة (Detection engineering as a life cycle).**
1. **الفرضية (Hypothesis)**: «من يختبر كلمات مرورٍ مسروقة (Someone testing stolen passwords) يجرّب حساباتٍ كثيرة من شبكاتٍ قليلة (tries many accounts from few networks)، مع نجاحاتٍ قليلة (with few successes).» وتأتي الأفكار من معلومات التهديدات (Ideas come from threat intelligence)، ونتائج الفريق الأحمر (red-team findings) (9.4)، والحوادث (incidents)، وATT&CK.
2. **فحص البيانات (Data check)**: هل نسجّل الحقول التي تحتاجها القاعدة؟ ⁦(do we log the fields the rule needs?)⁩ وكثيرًا ما يكون الناتج الأول إصلاحًا في التسجيل (The first output is often a logging fix).
3. **اكتب القاعدة (Write the rule)** في نظام التحكم في الإصدارات (in version control)، وراجِعها كما تُراجَع الشيفرة (reviewed like code).
4. **اختبرها (Test it)**: أعِد تشغيل عيّنةٍ مختبرية (replay a lab sample) لتثبت أنها تنطلق (to prove it fires)؛ وشغّلها على بيانات الأسابيع الماضية (run it over past weeks) لقياس الإيجابيات الكاذبة (to measure false positives).
5. **انشرها مع السياق (Deploy with context)**: الخطورة (severity)، والمالك (owner)، والربط بـATT&CK أو ATLAS (ATT&CK or ATLAS mapping)، ورابط دليل الاستجابة (playbook link).
6. **قِس واضبط (Measure and tune)**، أو أوقِف القاعدة (or retire).

ويُسمّى هذا غالبًا **الرصد بوصفه شيفرة (detection as code)**. و**Sigma** صيغة YAML مفتوحة ومحايدة تجاه المورّدين (an open, vendor-neutral YAML format) لكتابة القواعد (for rules)؛ وتحوّل أدوات مشروع Sigma (the Sigma project's tools) القاعدةَ الواحدة إلى لغات الاستعلام لدى كثيرٍ من منصات SIEM (convert a rule into many SIEMs' query languages). وهذه قاعدةٌ لبوابة أدوات نجم أسيست (A rule for Najm Assist's tool gateway):

```yaml
title: Najm Assist tool call denied by ownership check
status: experimental
description: The assistant tried to act on a card the signed-in customer does not own. Possible prompt injection or a tool-argument bug.
logsource:
  product: najm_assist
  service: tool_gateway
detection:
  selection:
    event: tool_call
    decision: deny
    deny_reason: resource_not_owned
  condition: selection
falsepositives:
  - Supplementary cardholder flows, until the ownership model covers them
level: high
```

وتعتمد قواعد أخرى على العدّ عبر الزمن (Other rules count over time). فقاعدة نجم لحشو بيانات الاعتماد (Najm's credential-stuffing rule) (ATT&CK T1110.004) تجمّع تسجيلات الدخول حسب الشبكة أو بصمة الجهاز (groups sign-ins by network or device fingerprint)، لا حسب عنوان IP منفرد (not single IP address)، لأن أدوات الحشو تبدّل العناوين (because stuffing tools rotate addresses). وهي تنطلق حين تُجرَّب مئات الحسابات في عشر دقائق (when hundreds of accounts are tried in ten minutes) بمعدّل نجاحٍ منخفضٍ جدًا (with a very low success rate)؛ فاضبط مثل هذه العتبات على بياناتك أنت (tune such thresholds on your own data).

**السلوك يتفوّق على المؤشرات (Behaviour beats indicators).** يرتّب **هرم الألم (Pyramid of Pain)** الذي وضعه ديفيد بيانكو (David Bianco) عام 2013 ما يرصده المدافعون (ranks what defenders detect) بحسب كلفة تغييره على المهاجم (by how much it costs the attacker to change). فتقع قيم التجزئة (hashes) وعناوين IP في القاعدة (sit at the bottom)، وتغييرها تافه (trivial to change)؛ وتقع **الأساليب والتقنيات والإجراءات (TTPs, tactics, techniques and procedures)** في القمة (sit at the top). وقواعد الرصد التي تدوم (The detections that last) هي التي تصف السلوك (describe behaviour).

**جودة التنبيهات (Alert quality).** تتبّع لكل قاعدة (Per rule, track) عدد التنبيهات أسبوعيًا (alerts per week)، ونسبة ما كان حقيقيًا منها (the share that were real)، ووقت الفرز (time to triage)، و**متوسط وقت الرصد (mean time to detect, MTTD)**. فالقاعدة التي تنطلق 300 مرة أسبوعيًا (A rule that fires 300 times a week) وتصدق مرةً واحدة (and is real once) تعوّد المحللين على تجاهلها (trains analysts to ignore it): وهذا هو **إرهاق التنبيهات (alert fatigue)**.

### 🔴 نظرة الخبير (Expert view)

**القياس عن بُعد لتطبيقات النماذج اللغوية الكبيرة والوكلاء (Telemetry for LLM apps and agents).** يعني التحقيق في نجم أسيست (Investigating Najm Assist means) الإجابة عن هذه الأسئلة (answering): ماذا سأل العميل (what did the customer ask)، وماذا رأى النموذج (what did the model see)، أي إصدار الموجّه والمستندات المسترجَعة ونتائج الأدوات (prompt version, retrieved documents, tool results)، وماذا قرّر (what did it decide)، وماذا سمحت به طبقة السياسات (what did the policy layer allow)؟ وهذا حدث استدعاء أداة (A tool-call event):

```json
{
  "ts": "2026-09-14T10:42:07.311Z",
  "event": "tool_call",
  "request_id": "r-77ac0e",
  "customer_ref": "c-5be1a9",
  "model_id": "vendor-model-2026-06",
  "system_prompt_version": "assist-sp-v14",
  "retrieved_doc_ids": ["kb-fees-2026-03"],
  "tool": "freeze_card",
  "decision": "deny",
  "deny_reason": "resource_not_owned",
  "guardrail": {"injection_score": 0.91, "verdict": "flag"}
}
```

**التوتّر مع الخصوصية (The privacy tension).** النصوص الكاملة للموجّهات والاستجابات (Full prompts and responses) هي أفضل دليل (are the best evidence)، وهي تحتوي على بياناتٍ شخصية (and contain personal data). وجواب نجم، المتفق عليه مع سارة (Najm's answer, agreed with Sara): تذهب البيانات الوصفية إلى منصة SIEM (metadata goes to the SIEM)؛ ويذهب النص الكامل إلى مخزنٍ مقيَّد (full text goes to a restricted store)، محجوبًا وقت الكتابة (masked at write time)، بمدة احتفاظٍ قصيرة (with short retention)، ولا يُوصَل إليه إلا عبر طلب كسر زجاجٍ مسجَّل (access only through a logged break-glass request) مرتبطٍ بحادثة (tied to an incident). ولدى **OpenTelemetry** اصطلاحاتٌ دلالية للذكاء الاصطناعي التوليدي (semantic conventions for generative AI)، وهي لا تزال قيد التطوير وقت كتابة هذا النص، 2026 (still in development at the time of writing, 2026)، تُبقي مثل هذه الحقول متّسقةً عبر المورّدين (keep such fields consistent across vendors).

**قواعد رصدٍ خاصة بالذكاء الاصطناعي (AI-specific detections)**، مربوطةٌ بقائمة OWASP Top 10 لتطبيقات النماذج اللغوية الكبيرة (OWASP Top 10 for LLM Applications) (2025):
- **كناري موجّه النظام (System-prompt canary)**: سلسلةٌ عشوائية فريدة في موجّه النظام (a unique random string in the system prompt) يجب ألّا تظهر أبدًا في المخرجات (that must never appear in output). وظهورها يعني تسرّب موجّه النظام (Seeing it means system prompt leakage) (LLM07).
- **رابطٌ غير معتمد في المخرجات (Unapproved link in output)**: أي نطاقٍ ليس على قائمة السماح لدى البنك (any domain not on the bank's allow-list) يُحجب ويُسجَّل (is blocked and logged). وتدلّ الموجة المفاجئة منها (A burst suggests) على حقن موجّهاتٍ غير مباشر عبر المحتوى المسترجَع (indirect prompt injection through retrieved content) (LLM01).
- **قفزات رفض الأدوات (Tool-denial spikes)**: قاعدة Sigma أعلاه (the Sigma rule above) مع قاعدة معدّل (plus a rate rule) (LLM06).
- **القيم الشاذة في الرموز (Token outliers)**: الجلسات التي تتجاوز خط الأساس للرموز بكثير (sessions far above the token baseline) تدلّ على إساءة استخدامٍ أو محاولات استخراج (suggest abuse or extraction attempts) (LLM10).
- **تحوّل الضوابط الوقائية بعد تغيير المحتوى (Guardrail shift after a content change)**: يقفز معدّل الإشارات لدى مصنِّف الحقن (the injection classifier's flag rate jumps) بعد تحديثٍ لقاعدة المعرفة (after a knowledge-base update) (LLM04، LLM08).
- **مراقبة النماذج (Model monitoring)**: في التنبيهات الذكية (for Smart Alerts)، قد يشير الانخفاض المفاجئ في التنبيهات لفئة تجّارٍ واحدة (a sudden drop in alerts for one merchant category) إلى التهرّب أو التسميم (can signal evasion or poisoning) (8.3). ومراقبة دانة (Dana's monitoring) تغذّي مركز العمليات الأمنية (feeds the SOC)، لا لوحة معلوماتٍ لعلم البيانات فحسب (not only a data-science dashboard).

**رموز الطُّعم (Honeytokens).** **رمز الطُّعم (honeytoken)** بيانات اعتمادٍ أو سجلٌّ أو مستندٌ مزيّف (a fake credential, record or document) لا تلمسه أي عمليةٍ مشروعة (that no legitimate process touches)، مثل مفتاحٍ سحابي مزيّف في مستودعٍ خاص (a fake cloud key in a private repository) أو مذكرةٍ مزيّفة في فهرس مساعد مذكرات الائتمان (a fake memo in the copilot's index). وأي استخدامٍ له (Any use) تنبيهٌ عالي الثقة (is a high-confidence alert).

**اختبر قواعد الرصد، ولا تكتفِ بكتابتها (Test detections, not just write them).** في **عمل الفريق البنفسجي (purple teaming)**، ينفّذ فريق مريم الأحمر (Mariam's red team) تقنيةً متفقًا عليها (runs an agreed technique)، بينما يتحقق فريق جاسم (while Jassim's team checks) مما إذا كانت قد سُجّلت ورُصدت وفُرزت (whether it was logged, detected and triaged). والناتج قائمةٌ بالفجوات (The output is a gap list). والخلية الخضراء في خريطة تغطية ATT&CK (A green cell on an ATT&CK coverage map) تعني فقط أن قاعدةً موجودة (only means a rule exists)، لا أنها تعمل (not that it works). وإذا كان نموذجٌ لغوي كبير يلخّص التنبيهات لمركز العمليات الأمنية (if an LLM summarises alerts for the SOC)، فتذكّر أن محتوى السجلات يتحكم فيه المهاجم (remember that log content is attacker-controlled): أبقِه للقراءة فقط (keep it read-only)، مع إنسانٍ في كل قرار احتواء (with a person on every containment decision).

## 🧰 الأدوات (The toolkit)
| الضابط أو المعيار أو الأداة (Control, standard or tool) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **OWASP Logging Cheat Sheet** — ورقة OWASP المختصرة للتسجيل | ما يُسجَّل، وما لا يُسجَّل أبدًا، وكيف تُحمى السجلات (What to log, what never to log and how to protect logs)؛ وورقةٌ مختصرة مرافقة تسمّي الأحداث (a companion cheat sheet names events) | كتابة معيار تسجيلٍ أو مراجعته (Writing or reviewing a logging standard) |
| **SIEM** — إدارة المعلومات والأحداث الأمنية (security information and event management) | منصةٌ مركزية تجمع السجلات وتوحّدها وتبحث فيها (Central platform that collects, normalises and searches logs) وتشغّل قواعد الرصد (and runs detection rules) | حين تصبح لديك مصادر سجلاتٍ كثيرة (Once you have many log sources) وفريقٌ يفرز التنبيهات (and a team that triages alerts) |
| **Sigma** (SigmaHQ) — صيغة قواعد رصد | صيغة YAML مفتوحة ومحايدة تجاه المورّدين لقواعد الرصد (Open, vendor-neutral YAML format for detection rules)، تُحوَّل إلى استعلاماتٍ لمنصات SIEM (converted into SIEM queries) | قواعد رصدٍ بوصفها شيفرة (Detections as code) يمكن مراجعتها واختبارها ونقلها بين منصات SIEM (that can be reviewed, tested and moved between SIEMs) |
| **MITRE ATT&CK** — قاعدة معرفة | قاعدة معرفةٍ بأساليب الخصوم وتقنياتهم (Knowledge base of adversary tactics and techniques) مستمدّةٌ من الملاحظة الواقعية (from real-world observation) | فرضيات الرصد (Detection hypotheses)، ووسم القواعد (tagging rules)، وإيجاد فجوات الرؤية (finding visibility gaps) |
| **MITRE ATLAS** — قاعدة معرفة للذكاء الاصطناعي | قاعدة معرفةٍ بأساليب الخصوم وتقنياتهم ضد أنظمة الذكاء الاصطناعي (Knowledge base of adversary tactics and techniques against AI systems) | ربط قواعد رصد الذكاء الاصطناعي (Mapping AI detections) لنجم أسيست ومساعد مذكرات الائتمان والتنبيهات الذكية (for Najm Assist, the copilot and Smart Alerts) |
| **Honeytokens** — رموز الطُّعم | بيانات اعتمادٍ أو سجلاتٌ أو مستنداتٌ مزيّفة (Fake credentials, records or documents) تُطلق تنبيهًا عند استخدامها (that alert when used) | رصدٌ رخيص قليل الضجيج للمتسلّلين والمطّلعين من الداخل (Cheap, low-noise detection of intruders and insiders) |
| **OpenTelemetry** — معيار القياس عن بُعد | معيارٌ مفتوح للتتبّعات والمقاييس والسجلات (Open standard for traces, metrics and logs)، مع اصطلاحاتٍ للذكاء الاصطناعي التوليدي (with generative-AI conventions) | قياسٌ عن بُعد متّسق (Consistent telemetry) عبر الخدمات وتطبيقات النماذج اللغوية الكبيرة (across services and LLM apps) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
تنشر نورة وجاسم (Noura and Jassim publish) **معيار التسجيل الأمني لبنك نجم، الإصدار 1 (Najm Bank Security Logging Standard v1)**، الذي وقّعه حمد، كبير مسؤولي أمن المعلومات (signed by Hamad, the CISO)، وأول **كتالوج لقواعد الرصد (Detection Catalogue)**. والأرقام خياراتٌ توضيحية من نجم (The numbers are Najm's illustrative choices).

**قواعد التسجيل (Logging rules)، مقتطف (excerpt)**

| القاعدة (Rule) | المتطلَّب (Requirement) |
|---|---|
| L1 الصيغة (Format) | أسطر JSON (JSON lines)، ومفردات أحداث نجم (Najm event vocabulary)، وطوابع زمنية بتوقيت UTC وبصيغة ISO 8601 (UTC ISO 8601 timestamps)، ومعرّف طلبٍ من الحافة إلى قاعدة البيانات (request ID from edge to database) |
| L2 لا يُسجَّل أبدًا (Never log) | كلمات المرور (Passwords)، ورموز الاستخدام لمرةٍ واحدة (one-time codes)، والرموز المميزة (tokens)، والمفاتيح (keys)، وأرقام البطاقات الكاملة (full card numbers)، ورموز أمان البطاقات (card security codes)، وأرقام الهوية الوطنية الكاملة (full national ID numbers) |
| L3 النقل (Shipping) | خارج المضيف خلال 60 ثانية (Off-host within 60 seconds) إلى حساب السجلات الأمنية (to the security log account)؛ ولا تستطيع فرق التطبيقات الحذف (application teams cannot delete) |
| L4 السلامة (Health) | 15 دقيقة من الصمت من أي مصدر (15 minutes of silence from any source) تُطلق تنبيهًا متوسط الخطورة (raises a medium alert) |
| L5 القياس عن بُعد للذكاء الاصطناعي (AI telemetry) | النموذج (Model)، وإصدار الموجّه (prompt version)، ومعرّفات المستندات المسترجَعة (retrieved document IDs)، واستدعاءات الأدوات (tool calls)، والقرارات (decisions)، وأحكام الضوابط الوقائية (guardrail verdicts) تذهب إلى منصة SIEM (to the SIEM)؛ والنص الكامل في المخزن المقيَّد فقط (full text only in the restricted store)، محجوبًا (masked)، وبوصول كسر الزجاج (break-glass access) |

**كتالوج قواعد الرصد، الإصدار 1 (Detection Catalogue v1)، مقتطف (excerpt)**

| المعرّف (ID) | ما ترصده (Detects) | الربط (Mapping) | الخطورة (Severity) | دليل الاستجابة (Playbook) | الاختبار (Test) |
|---|---|---|---|---|---|
| NM-01 | حشو بيانات الاعتماد على تطبيق نجم للهاتف (Credential stuffing on Najm Mobile) | ATT&CK T1110.004 | عالية (High) | PB-02 الاستيلاء على الحساب (Account takeover) | إعادة تشغيلٍ مختبرية على 300 حساب اختبار (Lab replay over 300 test accounts) |
| SP-01 | أكثر من 20 رفضًا لفحص الملكية (Over 20 ownership denials) في جلسةٍ واحدة على بوابة الشركات الصغيرة (in one SME Portal session) | OWASP API1 BOLA | متوسطة (Medium) | PB-04 استكشاف الوصول (Access probing) | إعادة تشغيلٍ مُبرمَجة في بيئة التجهيز (Scripted replay in staging) |
| NA-01 | كناري موجّه النظام في مخرجات أسيست (System-prompt canary in Assist output) | LLM07 | عالية (High) | PB-07 حادثة أسيست (Assist incident) | موجّه كناري في التكامل المستمر (Canary prompt in CI) |
| NA-02 | رفض استدعاء أداةٍ في أسيست: المورد غير مملوك (Assist tool call denied: resource not owned) | LLM06، LLM01 | عالية (High) | PB-07 حادثة أسيست (Assist incident) | حالات الفريق الأحمر من 9.4 (Red-team cases from 9.4) |
| NA-04 | أكثر من 5 نطاقاتٍ غير معتمدة (Over 5 unapproved domains) في مخرجات أسيست خلال 10 دقائق (in Assist output in 10 minutes) | LLM01 | عالية (High) | PB-07 حادثة أسيست (Assist incident) | مستند اختبارٍ غير ضار في فهرس بيئة التجهيز (Benign test document in staging index) |
| CL-01 | استخدام مفتاحٍ سحابي طُعم (Honeytoken cloud key used) | ATT&CK T1078 Valid Accounts | حرجة (Critical) | PB-09 اختراق بيانات الاعتماد السحابية (Cloud credential compromise) | استخدامٌ مضبوط فصليًا (Quarterly controlled use) |

**قواعد الكتالوج (Catalogue rules).** لا تدخل أي قاعدة رصدٍ الخدمةَ (No detection goes live) دون مالكٍ واختبارٍ آلي ودليل استجابة (without an owner, an automated test and a playbook). والقاعدة التي تصدق أقل من 10% من الوقت على مدى 30 يومًا (A rule real less than 10% of the time over 30 days) تُضبط أو تُوقَف (is tuned or retired). وتسأل كل مراجعة حادثة (Every incident review) (10.2) عن قاعدة الرصد التي كان ينبغي أن تنطلق أبكر (which detection should have fired earlier).

## 🛠️ التمارين (Exercises)
- 🟢 لخدمةٍ تملكها (For a service you own)، أو لنسخةٍ محلية من OWASP Juice Shop (a local copy of OWASP Juice Shop)، وهو تطبيق تدريبٍ معرَّضٌ للثغرات عمدًا (a deliberately vulnerable training app)، اكتب قائمةً بالأحداث الأمنية التي ينبغي أن يسجّلها (list the security events it should log) وتحقّق مما إذا كان يسجّلها (check whether it does). *يكتمل عندما (Done when):* يكون لديك ثمانية أحداثٍ على الأقل مع حقولها (you have at least eight events with their fields)، كلٌّ منها موسومٌ بـ«مُسجَّل» ("logged") أو «جزئيًا» ("partly") أو «مفقود» ("missing")، إضافةً إلى قائمةٍ بالحقول التي يجب ألّا تُسجَّل أبدًا (a list of fields that must never be logged).
- 🟡 شغّل Juice Shop أو تطبيقك محليًا (Run Juice Shop or your own app locally) مع كتابة السجلات بصيغة أسطر JSON (with logs written as JSON lines). اكتب نصًّا برمجيًا يُطلق دفعةً من محاولات تسجيل الدخول الفاشلة (Script a burst of failed sign-ins) على نسختك المحلية فقط (against your own local instance)، ثم اكتب قاعدة رصدٍ واحدة (write one detection)، قاعدة Sigma أو استعلامًا (Sigma rule or query)، تلتقطها (that catches it). *يكتمل عندما (Done when):* تكون القاعدة في git (the rule is in git) مع اختبارٍ إيجابي (with a positive test)، أي أن الدفعة تُطلقها (the burst fires it)، واختبارٍ سلبي (and a negative test)، أي أن ساعةً من الاستخدام العادي لا تُطلقها (an hour of normal use does not).
- 🔴 أضِف القياس عن بُعد للذكاء الاصطناعي (Add AI telemetry) إلى تطبيق نموذجٍ لغوي كبير تملكه (to an LLM app you own)، أو إلى عرضٍ محلي بنموذجٍ مفتوح الأوزان (or a local demo with an open-weight model): حدث استدعاء الأداة أعلاه (the tool-call event above)، وكناري موجّه النظام (a system-prompt canary)، ومرشّح الروابط غير المعتمدة (an unapproved-link filter)، ومخزن نصوصٍ كاملة مقيَّد (a restricted full-text store). *يكتمل عندما (Done when):* في مختبرك الخاص (in your own lab)، يُطلق سؤال التطبيق عن تعليماته (asking the app for its instructions) تنبيهَ الكناري (trips the canary alert)، ويُطلق مستند اختبارٍ يحوي رابطًا خارج القائمة (a test document with an off-list link) تنبيهَ الروابط (trips the link alert)، ولا تصل أي أسرارٍ إلى السجل الرئيسي (no secrets reach the main log).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **تسجيل كل شيء «احتياطًا» (Logging everything "just in case").** كلفةٌ وضجيج (Cost, noise) واختراقٌ للخصوصية ينتظر وقوعه (and a privacy breach in waiting). سجّل ما يُدرجه المعيار (Log what the standard lists).
- **تسجيل التصحيح في الإنتاج (Debug logging in production).** تسريبٌ كلاسيكي (A classic leak). احجب البيانات وقت الكتابة (Mask at write time) وافحص السجلات بحثًا عن الأسرار (scan logs for secrets).
- **أسطر السجل النصية الحرة (Free-text log lines).** لا يمكن عدّها (They cannot be counted)، وهي تسمح بحقن السجلات (they allow log injection). استخدم أسماء الأحداث والحقول المُهيكَلة (Use event names and structured fields).
- **قواعد بلا مالكٍ أو اختبارٍ أو دليل استجابة (Rules with no owner, test or playbook).** إنها تتعفّن (They rot)، ثم تنطلق في الثالثة فجرًا ولا أحد يعرف ما يجب فعله (then fire at 3 a.m. with nobody knowing what to do).
- **الرصد القائم على المؤشرات وحدها (Indicator-only detection).** قوائم حجب عناوين IP وقيم التجزئة (IP and hash blocklists) تنتهي صلاحيتها بسرعة (expire fast). أضِف قواعد سلوكية مربوطة بـATT&CK أو ATLAS (Add behaviour rules mapped to ATT&CK or ATLAS).
- **افتراض أن الصمت يعني الأمان (Assuming silence means safety).** أطلِق التنبيهات على المصادر المفقودة (Alert on missing sources) واختبر قواعد الرصد عبر عمل الفريق البنفسجي (purple-team your detections).

## 🧾 الخلاصة (Recap)
- سجّل الأحداث المهمة (Log the events that matter)، مُهيكَلةً (structured)، بتوقيت UTC (in UTC)، مع معرّفات الربط (with correlation IDs)؛ ولا تسجّل أبدًا الأسرار أو البيانات الشخصية غير اللازمة (never log secrets or unneeded personal data).
- انقل السجلات بسرعة إلى مخزنٍ مركزي مقاوم للعبث (Ship logs quickly to a tamper-resistant central store) وأطلِق تنبيهًا حين يصمت مصدر (and alert when a source goes silent).
- هندسة الرصد دورة حياة (Detection engineering is a life cycle): الفرضية (hypothesis)، وفحص البيانات (data check)، والقاعدة (rule)، والاختبار (test)، والنشر مع دليل استجابة (deploy with a playbook)، والقياس (measure)، والضبط (tune).
- اكتب القواعد بوصفها شيفرة (Write rules as code)، واربطها بـATT&CK وATLAS (map them to ATT&CK and ATLAS)، وفضّل السلوك على المؤشرات (favour behaviour over indicators).
- في تطبيقات النماذج اللغوية الكبيرة (For LLM apps)، سجّل النموذج وإصدار الموجّه والمستندات المسترجَعة واستدعاءات الأدوات وأحكام الضوابط الوقائية (log model, prompt version, retrieved documents, tool calls and guardrail verdicts)؛ وأبقِ النص الكامل مقيَّدًا (keep full text restricted)؛ وابدأ بالكناري ومرشّحات الروابط وقواعد رفض الأدوات (start with canaries, link filters and tool-denial rules).

## ✍️ اختبر نفسك (Check yourself)

**1. يقترح علي إرسال كل محادثةٍ في نجم أسيست كاملةً إلى منصة SIEM (Ali proposes sending every Najm Assist conversation, in full, to the SIEM) «كي لا يفوتنا شيء» ("so nothing is missed"). أيّ ردٍّ يتّبع هذا الدرس على أفضل وجه (Which response best follows this lesson)؟**

- A. الموافقة (Agree)، لأن النص الكامل هو أفضل دليل (because full text is the best evidence)
- B. رفض تسجيل المحادثات كليًا (Refuse to log conversations at all)، حمايةً للخصوصية (to protect privacy)
- C. إرسال البيانات الوصفية المُهيكَلة (Send structured metadata)، أي النموذج وإصدار الموجّه والمستندات المسترجَعة واستدعاءات الأدوات والقرارات (model, prompt version, retrieved documents, tool calls, decisions)، إلى منصة SIEM (to the SIEM)، والاحتفاظ بالنص الكامل محجوبًا في مخزنٍ مقيَّد (keep masked full text in a restricted store) مع وصول كسر زجاجٍ مسجَّل (with logged break-glass access)
- D. تسجيل النص الكامل (Log full text)، ولكن في حاوية التصحيح لدى فريق التطبيق فقط (but only in the app team's debug bucket)

<details><summary>الإجابة</summary>

**C.** فهو يحفظ الدليل (It keeps the evidence) مع تقييد من يرى البيانات الشخصية (while limiting who sees personal data). أما A فيحوّل منصة SIEM إلى مخزن بياناتٍ شخصية (turns the SIEM into a personal-data store)؛ وB يجعل إعادة بناء الحوادث مستحيلة (makes incidents impossible to reconstruct)؛ وD هو المشكلة التي وجدها علي (is the problem Ali found). انظر: 🔴 نظرة الخبير (Expert view).

</details>

**2. تكتب خدمة واجهة برمجةٍ في تطبيق نجم للهاتف (A Najm Mobile API service writes) `log.info(f"Login failed for {username}")`. بصرف النظر عن صعوبة البحث فيه (Apart from being hard to search)، ما المشكلة الأمنية الرئيسية (what is the main security problem)؟**

- A. اسم مستخدمٍ يحتوي على فاصل سطر (A username containing a line break) يستطيع تزوير أسطر سجلٍّ مزيّفة (can forge fake log lines)، ولذا فمكان القيمة حقلٌ مُهيكَل ومُهرَّب (so the value belongs in a structured, escaped field)
- B. يحظر معيار PCI DSS تسجيل محاولات الدخول الفاشلة (PCI DSS forbids logging failed sign-ins)
- C. سلاسل f-strings أبطأ من طرق التنسيق الأخرى (f-strings are slower than other formatting)
- D. يجب ألّا تُسجَّل محاولات الدخول الفاشلة أبدًا (Failed sign-ins should never be logged)

<details><summary>الإجابة</summary>

**A.** إدخال المستخدم الخام في سطرٍ نصي حر (Raw user input in a free-text line) يسمح بحقن السجلات (allows log injection) (CWE-117). أما B وD فخاطئان (are wrong): فمحاولات الدخول الفاشلة من أهم الأحداث التي ينبغي تسجيلها (failed sign-ins are among the most important events to log). وC ليست مشكلةً أمنية (is not a security issue). انظر: 🟢 الأساسيات (The essentials).

</details>

**3. لم تتلقَّ منصة SIEM أي أحداثٍ من بوابة الشركات الصغيرة منذ ست ساعات (The SIEM has received no events from the SME Portal for six hours)، ولم ينطلق أي تنبيه (and no alerts have fired). ما الذي ينبغي أن يستنتجه فريق جاسم (What should Jassim's team conclude)؟**

- A. البوابة هادئة، إذن فهي آمنة (The portal is quiet, so it is safe)
- B. الصمت بحدّ ذاته إشارة (Silence is itself a signal): ينبغي أن يُطلق فحص سلامة المصادر تنبيهًا (a source-health check should alert)، وأن يكتشف الفريق سبب توقّف المصدر (and the team should find out why the source stopped)
- C. قواعد الرصد مضبوطةٌ جيدًا (The detections are well tuned)
- D. لا شيء؛ ففترات الهدوء طبيعية (Nothing; quiet periods are normal)

<details><summary>الإجابة</summary>

**B.** إذا توقّف مصدرٌ عن الإرسال (If a source stops sending)، فإن كل قاعدة رصدٍ تعتمد عليه تصبح عمياء (every detection relying on it is blind)، كما بيّن جهاز الفحص في Equifax (as the Equifax inspection device showed). أما A وC فيخلطان بين «لا تنبيهات» ("no alerts") و«لا هجوم» ("no attack"). انظر: 🟡 التعمق أكثر (Going deeper).

</details>

**4. أيّ قاعدة رصدٍ ستبقى مفيدةً أطول مدة (Which detection will stay useful longest) في مواجهة مجموعةٍ تنفّذ حشو بيانات الاعتماد على تطبيق نجم للهاتف (against a group running credential stuffing against Najm Mobile)؟**

- A. قائمة حجبٍ لعناوين IP الخمسين التي شوهدت أمس (A blocklist of the 50 IP addresses seen yesterday)
- B. قائمةٌ بقيم تجزئة ملفات أدواتهم (A list of file hashes of their tools)
- C. قاعدةٌ سلوكية (A behaviour rule): حساباتٌ متمايزة كثيرة ومعدّل نجاحٍ منخفضٌ جدًا (many distinct accounts and a very low success rate) من شبكةٍ واحدة أو بصمة جهازٍ واحدة (from one network or device fingerprint) في نافذةٍ زمنية قصيرة (in a short window)
- D. قاعدةٌ تطابق سلسلة وكيل المستخدم التي استخدموها بالضبط (A rule matching the exact user-agent string they used)

<details><summary>الإجابة</summary>

**C.** فهي تصف التقنية (It describes the technique)، قرب قمة هرم الألم (near the top of the Pyramid of Pain)، ويكلّف تغييرها كثيرًا (and costly to change). أما عناوين IP وقيم التجزئة وسلاسل وكيل المستخدم (IP addresses, hashes and user-agent strings) فتغييرها رخيص (are cheap to change). انظر: 🟡 التعمق أكثر (Going deeper).

</details>

**5. ينفّذ فريق مريم تقنيةً متفقًا عليها ضد بيئة التجهيز (Mariam's team runs an agreed technique against staging)، بينما يتحقق فريق جاسم من الخطوات التي سُجّلت ورُصدت وفُرزت (while Jassim's team checks which steps were logged, detected and triaged). ما هذا، وما ناتجه الرئيسي (What is this, and what is its main output)؟**

- A. اختبار اختراق (A penetration test)؛ وناتجه درجة CVSS (its output is a CVSS score)
- B. عمل الفريق البنفسجي (Purple teaming)؛ وناتجه قائمةٌ بفجوات التسجيل والرصد الواجب إصلاحها (its output is a list of logging and detection gaps to fix)
- C. تمرين محاكاةٍ نظرية (A tabletop exercise)؛ وناتجه خطة اتصالات (its output is a communications plan)
- D. برنامج مكافآت ثغرات (A bug bounty)؛ وناتجه دفعةٌ مالية (its output is a payout)

<details><summary>الإجابة</summary>

**B.** يختبر عمل الفريق البنفسجي قواعد الرصد (Purple teaming tests detections) مقابل تنفيذٍ حقيقي للتقنيات (against real technique execution)، وينتج قائمةً بالفجوات (and produces a gap list). أما تمرين المحاكاة النظرية فهو نقاشٌ فقط (A tabletop is discussion only) (10.2)؛ وبرنامج مكافآت الثغرات يستعين بباحثين من الخارج (a bug bounty uses outside researchers) (10.3). انظر: 🔴 نظرة الخبير (Expert view).

</details>

## 📚 المراجع (References)
- قائمة OWASP Top 10، إصدار 2021 (2021 edition)، البند A09، إخفاقات التسجيل والمراقبة الأمنية (Security Logging and Monitoring Failures)؛ وتحقّق من الإصدار الحالي (check the current edition) — https://owasp.org/Top10/
- ورقة OWASP المختصرة للتسجيل (OWASP Logging Cheat Sheet) — https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- ورقة OWASP المختصرة لمفردات التسجيل (OWASP Logging Vocabulary Cheat Sheet) — https://cheatsheetseries.owasp.org/cheatsheets/Logging_Vocabulary_Cheat_Sheet.html
- NIST SP 800-92، دليل إدارة سجلات أمن الحاسوب (Guide to Computer Security Log Management)، 2006؛ ونُشرت مسودةٌ للمراجعة الأولى عام 2023 (a Rev. 1 draft was published in 2023)، فتحقّق من وجود مراجعةٍ نهائية (so check for a final revision) — https://csrc.nist.gov/pubs/sp/800/92/final
- MITRE ATT&CK — https://attack.mitre.org/
- MITRE ATLAS — https://atlas.mitre.org/
- CWE-117، التحييد غير السليم للمخرجات في السجلات (Improper Output Neutralization for Logs) — https://cwe.mitre.org/data/definitions/117.html
- CWE-532، إدراج معلوماتٍ حساسة في ملف السجل (Insertion of Sensitive Information into Log File) — https://cwe.mitre.org/data/definitions/532.html
- Sigma (SigmaHQ) — https://github.com/SigmaHQ/sigma
- الاصطلاحات الدلالية في OpenTelemetry (OpenTelemetry semantic conventions) — https://opentelemetry.io/docs/specs/semconv/
- قائمة OWASP Top 10 لتطبيقات النماذج اللغوية الكبيرة 2025 (OWASP Top 10 for LLM Applications 2025) — https://genai.owasp.org/
- مجلس معايير أمن صناعة بطاقات الدفع (PCI Security Standards Council)، معيار PCI DSS v4.0.1 — https://www.pcisecuritystandards.org/

---

# 10.2 — الاستجابة للحوادث: الاستعداد والرصد والاحتواء والتعافي والتعلّم (Incident response: prepare, detect, contain, recover, learn)
*المستوى (Level): 🔴 متقدم (Advanced)* · *المتطلبات (Prerequisites): 1.3، 10.1* · *المرحلة (Phase): Respond*

## ⚡ الدرس في دقيقة (In 60 seconds)
- **الحادثة الأمنية (security incident)** تُلحق ضررًا فعليًا أو محتملًا (actually or potentially harms) بسرية الأنظمة أو البيانات أو سلامتها أو توافرها (the confidentiality, integrity or availability of systems or data). و**الاستجابة للحوادث (incident response, IR)** هي العملية المتمرَّس عليها للتعامل معها (the practised process for handling one).
- دورة الحياة (The life cycle): **الاستعداد (prepare)**، و**الرصد والتحليل (detect and analyse)**، و**الاحتواء (contain)**، و**الاستئصال والتعافي (eradicate and recover)**، و**التعلّم (learn)**. ويؤطّرها الإصدار NIST SP 800-61 Rev. 3 (2025) حول وظائف إطار CSF 2.0 (frames it around the CSF 2.0 functions).
- الاستعداد يحسم النتيجة (Preparation decides the outcome): الأدوار (roles)، وأدلة التشغيل (runbooks)، وجهات الاتصال (contacts)، وقناةٌ خارج النطاق (an out-of-band channel)، وسجلاتٌ تجيب عن الأسئلة (logs that answer questions)، و**مفاتيح الإيقاف الطارئ (kill switches)** للميزات الخطرة (for risky features)، وكلها مُتمرَّنٌ عليها (all rehearsed).
- في لحظة الحادثة (In the moment): أعلِن مبكرًا (declare early)، وعيّن **قائدًا للحادثة (incident commander)**، واحتفظ بسجل قراراتٍ مؤرَّخٍ زمنيًا (keep a timestamped decision log)، واحفظ الأدلة قبل تغيير الأشياء (preserve evidence before changing things)، واحتوِ قبل أن تنظّف (contain before you clean up).
- تبدأ المهل القانونية من لحظة العلم (Legal clocks run from awareness): تتوقع اللائحة العامة لحماية البيانات (GDPR) إخطار السلطة خلال 72 ساعة حيثما أمكن (expects the authority to be notified within 72 hours where feasible)، كما تخضع المصارف أيضًا لقانون DORA وللجهات الرقابية الوطنية (banks also answer to DORA and national regulators). أشرِك مسؤول حماية البيانات والفريق القانوني في الساعة الأولى (Bring in the DPO and legal in the first hour).
- تحتاج حوادث الذكاء الاصطناعي إلى استعدادٍ إضافي (AI incidents need extra preparation): مفاتيح للأدوات ومصادر الاسترجاع (switches for tools and retrieval sources)، وموجّهاتٌ وسياقٌ محفوظان (preserved prompts and context)، وطريقةٌ لحصر كل عميلٍ رأى مخرجاتٍ سيئة (a way to list every customer who saw a bad output).

## 🧭 لماذا يهم (Why it matters)
الخميس، الساعة 21:40 (Thursday, 21:40). تنطلق قاعدة الرصد NA-04 من الدرس 10.1 (Detection NA-04 from 10.1)، أي النطاقات غير المعتمدة في مخرجات نجم أسيست (unapproved domains in Najm Assist output)، 37 مرة في 20 دقيقة (37 times in 20 minutes). فالعملاء الذين يسألون عن رسوم البطاقات (Customers asking about card fees) يُطلب منهم «إعادة التحقق» ("re-verify") من بطاقاتهم على عنوانٍ لا يملكه البنك (at an address the bank does not own). ويحذف مرشّح المخرجات معظم هذه الروابط (The output filter strips most of these links)، لكن بعضها، المكتوب بصيغةٍ لا يتعرّف عليها بوصفها رابطًا (written in a form it does not recognise as a link)، يتسلّل (get through). ويُستدعى جاسم (Jassim is paged).

في الساعة 19:55 (At 19:55)، عُدّل مقالٌ عن الرسوم في قاعدة المعرفة (a fees article in the knowledge base was edited) من حسابٍ لإدارة المحتوى (from a content-management account)، وهو يخفي الآن تعليماتٍ موجّهة إلى المساعد (now hides instructions aimed at the assistant): حقن موجّهاتٍ غير مباشر (indirect prompt injection) (8.2). ويسأل الجميع في آنٍ واحد (Everyone asks at once): كم عميلًا رأى الرابط (how many customers saw the link)، وهل أدخل أيٌّ منهم بيانات بطاقته (and did any enter card details)؟ هل اختُرق حساب المحتوى (Was the content account compromised)، وما الذي لمسه أيضًا (and what else did it touch)؟ هل يمكننا إيقاف هذا دون إطفاء نجم أسيست للجميع (Can we stop this without switching off Najm Assist for everyone)؟ هل يجب أن نُخطر مصرف قطر المركزي (QCB) والسلطات الأوروبية (EU authorities) والعملاء (and customers)، ومتى (and by when)؟ ومن يقرّر (Who decides)؟

بعض الإجابات يستغرق دقائق (Some answers take minutes)، لأن معيار التسجيل يدوّن المستندات التي استرجعتها كل إجابة (because the logging standard records which documents each answer retrieved). وبعضها الآخر يستغرق ساعات (Others take hours)، لأن أحدًا لم يكتب من يجوز له إطفاء مصدر استرجاعٍ ليلًا (because nobody wrote down who may switch off a retrieval source at night). وهذا الدرس يُفرغ تلك القائمة الثانية مسبقًا (This lesson empties that second list in advance). والسيناريو خيالي (The scenario is fictional)؛ أما نمط التعليمات المخفية في المحتوى المسترجَع (the pattern of instructions hidden in retrieved content) فموثّقٌ في الأبحاث المنشورة (is documented in public research) (Greshake et al., 2023).

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**الحدث والحادثة والخرق (Event, incident, breach).** **الحدث (event)** هو أي شيءٍ قابل للملاحظة (anything observable)، مثل التنبيه (such as an alert). و**الحادثة (incident)** حدثٌ أو سلسلة أحداث (an event or series) تُلحق ضررًا فعليًا أو محتملًا بالسرية أو السلامة أو التوافر (actually or potentially harms confidentiality, integrity or availability)، أو تخرق السياسة الأمنية (or breaks security policy). و**خرق البيانات الشخصية (personal data breach)** (GDPR Art. 4(12)) هو خرقٌ أمني يؤدي إلى (a breach of security leading to) الإتلاف العرضي أو غير المشروع للبيانات الشخصية أو فقدانها أو تعديلها أو الإفصاح غير المصرّح به عنها أو الوصول إليها (the accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to, personal data): وهو فئةٌ قانونية (a legal category) تترتب عليها واجبات إخطار (with notification duties). ويتحمّل البنك هذه الواجبات بصفته المتحكّم في البيانات (The bank, as controller, carries those duties)؛ وفي نجم، تتخذ سارة، مسؤولة حماية البيانات (the DPO)، القرار مع الفريق القانوني (makes the call with legal).

**دورة الحياة (The life cycle).** وصف الإصدار NIST SP 800-61 Rev. 2 (2012) أربع مراحل (described four phases)؛ وتغطي الخطوات الست التي يدرّسها معهد SANS على نطاقٍ واسع (the SANS Institute's widely taught six steps) المساحةَ نفسها (cover the same ground). ويعيد الإصدار NIST SP 800-61 Rev. 3 (2025) تأطير الاستجابة للحوادث (re-frames IR) حول وظائف إطار CSF 2.0 الست (around the six CSF 2.0 functions)، وهي الحوكمة والتحديد والحماية والرصد والاستجابة والتعافي (Govern, Identify, Protect, Detect, Respond, Recover)، فيجعلها جزءًا من إدارة المخاطر الشاملة (making it part of overall risk management). وتستخدم هذه الدورة التدريبية خمسة أفعالٍ بسيطة (This course uses five plain verbs):

| المرحلة (Phase) | الهدف (Goal) | المخرجات الرئيسية (Key outputs) |
|---|---|---|
| الاستعداد (Prepare) | أن تكون قادرًا على الاستجابة قبل أن تحتاج إليها (Be able to respond before you need to) | خطة الاستجابة للحوادث (IR plan)، والأدوار وجدول المناوبات (roles and rota)، وأدلة التشغيل (runbooks)، وجهات الاتصال (contacts)، والتسجيل (logging) (10.1)، والمفاتيح (switches)، والتمارين (drills) |
| الرصد والتحليل (Detect and analyse) | معرفة ما يحدث وحجمه وما إذا كان مستمرًا (Know what is happening, how big it is, whether it continues) | حادثةٌ مُعلنة (Declared incident)، والخطورة (severity)، والنطاق (scope)، والخط الزمني (timeline)، والفرضيات (hypotheses) |
| الاحتواء (Contain) | إيقاف انتشار الضرر (Stop the harm spreading) | ميزاتٌ معطَّلة (Disabled features)، وبيانات اعتمادٍ ملغاة (revoked credentials)، وأنظمةٌ معزولة (isolated systems)، وأدلةٌ محفوظة (preserved evidence) |
| الاستئصال والتعافي (Eradicate and recover) | إزالة السبب والعودة إلى خدمةٍ آمنة (Remove the cause and return to safe service) | إزالة السبب (Cause removed)، وتدوير الأسرار (secrets rotated)، وإعادة بناءٍ نظيفة (clean rebuilds)، واستعادةٌ مراقَبة (monitored restore) |
| التعلّم (Learn) | جعل تكرارها أقل احتمالًا وأقل ضررًا في المرة القادمة (Make it less likely and less harmful next time) | مراجعة ما بعد الحادثة (Post-incident review)، وإجراءاتٌ متتبَّعة (tracked actions)، وقواعد رصدٍ واختباراتٌ جديدة (new detections and tests) |

```mermaid
flowchart RL
    P["الاستعداد<br/>(Prepare)"] --> D["الرصد والتحليل<br/>(Detect and analyse)"]
    D --> C["الاحتواء<br/>(Contain)"]
    C --> E["الاستئصال والتعافي<br/>(Eradicate and recover)"]
    E --> L["التعلم<br/>(Learn)"]
    L -->|"أدلة التشغيل وقواعد الرصد والاختبارات (Runbooks, detections, tests)"| P
    C -->|"نتائج جديدة توسع النطاق (New findings widen scope)"| D
    E -->|"عودة المهاجم (Attacker returns)"| D
```

**الخطورة (Severity).** اتفقوا على المستويات مسبقًا (Agree levels in advance)، ومستويات نجم في قسم 🏛️ (Najm's are in the 🏛️ section)، كي لا يتجادل فيها أحدٌ في الساعة 22:00 (so nobody debates them at 22:00). أعلِن بمستوى عالٍ ثم خفّضه لاحقًا (Declare high and downgrade later): فالبداية البطيئة تكلّف أكثر من مكالمةٍ ضائعة (a slow start costs more than a wasted call).

**الأدوار (Roles)**، مستعارةٌ من نظام قيادة الحوادث لدى خدمات الطوارئ (borrowed from emergency services' incident command):
- **قائد الحادثة (Incident commander, IC)**: يدير الاستجابة (runs the response)، ويحدّد الأولويات (sets priorities)، ويتخذ القرارات أو يصعّدها (makes or escalates decisions)؛ ولا يقوم بأي تحليلٍ عملي بنفسه (does no hands-on analysis).
- **القائد التقني (Technical lead)**: يوجّه التحقيق والاحتواء (directs investigation and containment).
- **المدوِّن (Scribe)**: يحتفظ بالسجل المؤرَّخ زمنيًا للحقائق والإجراءات والقرارات (keeps the timestamped log of facts, actions and decisions).
- **قائد الاتصالات (Communications lead)**: الرسائل الداخلية والموجّهة إلى العملاء ووسائل الإعلام (internal, customer and media messages)، بالتنسيق مع الفريق القانوني (with legal).
- **الفريق القانوني ومسؤولة حماية البيانات (Legal and DPO)**، أي سارة: المهل التنظيمية والإخطارات (regulatory clocks and notifications).
- **مالك العمل (Business owner)**، وهي رانيا في حالة نجم أسيست (Rania for Najm Assist): الموازنات التجارية (business trade-offs)، مثل إطفاء ميزةٍ ما (such as switching a feature off).
- **المسؤول التنفيذي (Executive)**، أي حمد، كبير مسؤولي أمن المعلومات (the CISO): القرارات الكبرى (big decisions)، ومجلس الإدارة (the board)، والجهات الرقابية (and regulators).

**قائمة التحقق للاستعداد (Preparation checklist).** خطة استجابةٍ للحوادث معتمدة (An approved IR plan)؛ وجدول مناوبةٍ مع بدلاء (an on-call rota with backups)؛ وأدلة تشغيل (runbooks)؛ وقائمة جهات اتصال (a contact sheet) تشمل المورّدين ومزوّدي السحابة والنماذج (covering vendors, cloud and model providers) والمستشارين القانونيين الخارجيين (outside counsel) والجهات الرقابية (regulators) وجهات إنفاذ القانون (and law enforcement)؛ و**قناةٌ خارج النطاق (out-of-band channel)**، أي وسيلة اتصالٍ لا تعتمد على أنظمةٍ ربما تكون مخترقة (communication that does not depend on possibly compromised systems)، مثل مساحة عملٍ منفصلة أو خطٍّ هاتفي جماعي (such as a separate workspace or phone bridge)؛ وسجلاتٌ مفيدة (useful logs)؛ و**مفاتيح الإيقاف الطارئ (kill switches)**؛ وتمارين (and drills).

### 🟡 التعمق أكثر (Going deeper)

**الرصد والتحليل (Detect and analyse).** هل هي حقيقية (Is it real)، وما المتأثر (what is affected)، وهل لا تزال جارية (is it still happening)، وما أسوأ حالةٍ معقولة (what is the worst plausible case)؟ ابنِ **خطًا زمنيًا (timeline)** من السجلات (from logs) واحتفظ بالفرضيات مع الأدلة المؤيدة والمعارضة (keep hypotheses with evidence for and against). ودوِّن كل قرارٍ مع وقته ومالكه (Record each decision with time and owner): «22:05 عطّل قائد الحادثة الاسترجاع من مجموعة الرسوم؛ بموافقة رانيا.» ⁦("22:05 IC disabled retrieval from the fees collection; approved by Rania.")⁩ ويخدم هذا السجل لاحقًا الجهات الرقابية والمدققين والمراجعة (That log later serves regulators, auditors and the review).

**الاحتواء (Contain).** الاحتواء قصير المدى (Short-term containment) يوقف الضرر الآن (stops the harm now)؛ والاحتواء طويل المدى (long-term containment) يُبقيه متوقفًا (keeps it stopped) بينما تُصلح السبب (while you fix the cause).

| الخيار (Option) | ما يوقفه (Stops) | الكلفة (Costs) | انتبه إلى (Watch out for) |
|---|---|---|---|
| تعطيل ميزةٍ أو أداةٍ واحدة بمفتاح (Disable one feature or tool with a switch) | مسار الضرر ذاك (That path of harm) | فقدانٌ جزئي للخدمة (Partial loss of service) | يجب أن يكون المفتاح موجودًا ومُختبَرًا (The switch must exist and be tested) |
| إلغاء الجلسات وتدوير بيانات الاعتماد (Revoke sessions, rotate credentials) | إعادة استخدام الوصول المسروق (Reuse of stolen access) | تسجيل خروج المستخدمين وتعطّل التكاملات (Users signed out, integrations break) | دوِّر كل ما كان بوسع المهاجم رؤيته (Rotate everything the attacker could have seen) |
| عزل مضيفٍ أو حاوية (Isolate a host or container) | الانتشار من تلك الآلة (Spread from that machine) | السعة (Capacity) | التقط الحالة أولًا (Capture state first)؛ فإطفاء الجهاز يُضيّع محتوى الذاكرة (powering off loses memory) |
| حجب عنوان IP أو نطاقٍ أو حساب (Block an IP, domain or account) | ذلك المؤشر الواحد (That one indicator) | قليلة (Little) | يغيّر المهاجمون المؤشرات بسرعة (Attackers change indicators fast) (10.1) |

هل سيُنبّه الاحتواء المبكر المهاجمَ (Will early containment tip off the attacker)؟ في الهجوم سريع الحركة على العملاء (For a fast-moving attack on customers)، احتوِ (contain). أما في التسلّل الهادئ طويل الأمد (For a quiet, long-running intrusion)، فقد يكون من الصواب المراقبة لفترةٍ وجيزة لمعرفة النطاق (observing briefly to learn scope can be right)، ولكن بقرارٍ صريح فقط من قائد الحادثة وكبير مسؤولي أمن المعلومات (but only by explicit IC and CISO decision).

لا ينجح الاحتواء إلا إذا كان المفتاح موجودًا (Containment works only if the switch exists). ففي البداية لم يكن ممكنًا إيقاف أدوات نجم (Najm's tools could at first be stopped) إلا بإعادة النشر (only by a redeploy). أما الآن (Now):

```python
# Every tool and retrieval collection has an operational switch
def run_tool(name, args, session):
    if name not in TOOLS:                       # tool names come from the model: allow-list them
        return ToolResult.unavailable("Unknown action.")
    if flags.off("assist.tools.all") or flags.off(f"assist.tool.{name}"):
        audit.log("tool_blocked_by_switch", tool=name, session_id=session.id)
        return ToolResult.unavailable("This action is paused. Please use the app menu or call us.")
    return TOOLS[name](args, session)           # ownership and confirmation checks still apply inside

def retrieve(query, session):
    live = [c for c in COLLECTIONS if not flags.off(f"assist.kb.{c}")]
    if not live:                                # an empty filter must never mean "search everything"
        return []
    return index.search(query, collections=live, user=session.user)
```

تُقرأ العلامات وقت الطلب (Flags are read at request time)، ويستطيع قائد الحادثة المناوب قلبها في ثوانٍ (the on-call IC can flip them in seconds)، وكل قلبٍ يُسجَّل ويُتمرَّن عليه (every flip is logged and drilled).

**احفظ الأدلة (Preserve evidence).** تُظهر الأدلة النطاق (Evidence shows the scope)، وتُثبت ما *لم* يحدث (proves what did *not* happen)، وتدعم الإجراءات القانونية (and supports legal action). ويحدّد RFC 3227، أي إرشادات جمع الأدلة وأرشفتها (Guidelines for Evidence Collection and Archiving)، الصادر عام 2002، **ترتيب التطاير (order of volatility)**: اجمع البيانات الأقصر عمرًا أولًا (collect the most short-lived data first)، مثل الذاكرة والعمليات الجارية (such as memory and running processes)، ثم الأقراص (then disks)، ثم النسخ الاحتياطية والأرشيفات (then backups and archives). وفي السحابة (In the cloud)، التقط لقطاتٍ للأقراص وصدّر السجلات (snapshot disks and export logs) قبل إنهاء أي شيء (before terminating anything)، وأوقِف مؤقتًا الاستبدال الآلي (pause automatic replacement) الذي قد يُتلف مثيلًا مخترقًا (that would destroy a compromised instance). ودوِّن قيم تجزئة الملفات (Record file hashes) و**سلسلة العهدة (chain of custody)**: من حاز الدليل (who held the evidence)، ومتى (when)، وماذا فعل به (and what they did with it).

**الاستئصال والتعافي (Eradicate and recover).** أزِل السبب الجذري (Remove the root cause) وأي وسيلة ثباتٍ للمهاجم (and any attacker persistence)، ودوِّر كل سرٍّ كان بوسع المهاجم بلوغه (rotate every secret the attacker could have reached)، وأعِد البناء من صورٍ معروفٍ أنها سليمة (rebuild from known-good images) بدلًا من «تنظيف» خادم (rather than "cleaning" a server)، واستعِد الخدمة على مراحل (restore in stages) وفق معايير محدّدة مسبقًا (against criteria set in advance).

**تواصَل (Communicate).** صوتٌ واحد (One voice)، وتحديثاتٌ وفق جدولٍ ثابت (updates on a fixed schedule)، مثل «التحديث التالي 23:00» ("next update 23:00")، وحقائق لا تكهّنات (facts not speculation). وتقول رسائل العملاء (Customer messages say) ما الذي حدث (what happened)، وما يعنيه لهم (what it means for them)، وما يفعله البنك (what the bank is doing)، وما ينبغي أن يفعلوه (and what they should do)، بالعربية والإنجليزية (in Arabic and English).

**المهل التنظيمية (Regulatory clocks)**، وهذا ملخصٌ فقط (a summary only)، مع التحفّظ بحسب الوضع وقت كتابة هذا النص، 2026 (hedged at the time of writing, 2026)؛ والتفاصيل من شأن الفريق القانوني (details belong to legal) ودورة *AI Governance: Zero to Hero*:
- **GDPR**، المادة 33 (Art. 33): أخطِر السلطة الرقابية دون تأخيرٍ لا مبرّر له (notify the supervisory authority without undue delay)، وخلال 72 ساعة من العلم بخرق البيانات الشخصية حيثما أمكن (where feasible, within 72 hours of becoming aware of a personal data breach)، ما لم يكن من غير المرجّح أن ينتج عنه خطر (unless it is unlikely to result in risk)؛ ويجوز تقديم المعلومات على مراحل (information may come in phases). والمادة 34 (Art. 34): أبلِغ الأشخاص المتأثرين دون تأخيرٍ لا مبرّر له (tell affected people without undue delay) حين يكون الخطر عليهم مرتفعًا (when the risk to them is high).
- **قانون حماية خصوصية البيانات الشخصية في قطر (Qatar PDPPL)**، القانون رقم 13 لسنة 2016 (Law No. 13 of 2016)، يتضمن واجبات إخطارٍ بالخروقات (includes breach notification duties)؛ فاتّبع الإرشادات الحالية للسلطة المختصة (follow the competent authority's current guidance).
- **قانون DORA الأوروبي (EU DORA)**، الساري منذ يناير 2025 (applying from January 2025)، يُلزم الكيانات المالية (requires financial entities) بتصنيف الحوادث المتعلقة بتقنية المعلومات والاتصالات (to classify ICT-related incidents) والإبلاغ عن الكبرى منها في تقارير مرحلية (and report major ones in staged reports)، وفق جداول زمنية تحدّدها معاييره التقنية (on timelines set in its technical standards).
- **مصرف قطر المركزي (QCB)** والجهات الرقابية الأخرى على نجم (and Najm's other supervisors) يتوقعون الإبلاغ عن الحوادث السيبرانية الجسيمة (expect significant cyber incidents to be reported) وفق تعليماتهم الحالية (under their current instructions).
- **PCI DSS** v4.0.1 يشترط أن تغطي خطة الاستجابة للحوادث (requires the IR plan to cover) إخطار العلامات التجارية لشبكات الدفع والجهات المُحصِّلة (notifying the payment brands and acquirers) حين يُحتمل أن تكون بيانات البطاقات معنيّة (when card data may be involved).

### 🔴 نظرة الخبير (Expert view)

**ما الذي يختلف في حوادث الذكاء الاصطناعي (What is different about AI incidents).**
- **لا يمكنك ببساطة إعادة تشغيلها (You cannot simply replay it).** تتباين المخرجات بين مرات التشغيل (Output varies between runs)، ويتغيّر السياق (and the context changes)، أي المستندات المسترجَعة ونتائج الأدوات وسجل المحادثة (retrieved documents, tool results, history). وتحتاج إعادة البناء (Reconstruction needs) إلى معرّف النموذج المسجَّل (the logged model ID)، وإصدار الموجّه (prompt version)، ومعرّفات المستندات المسترجَعة (retrieved document IDs)، واستدعاءات الأدوات (and tool calls) (10.1).
- **الحمولة نصٌّ داخل البيانات (The payload is text in data).** يعني الاستئصال (Eradication means) إزالة كل نسخةٍ من المقال المسموم (removing every copy of the poisoned article)، بما في ذلك أجزاؤه وتضميناته في فهرس المتجهات (including its chunks and embeddings in the vector index) (9.3)، وذاكرات التخزين المؤقت (caches)، والملخصات المولَّدة (and generated summaries)، ومراجعة كل ما لمسه الحساب أيضًا (and reviewing everything else the account touched).
- **نطاق الضرر يساوي الصلاحيات (Blast radius equals permissions).** كان ما تستطيع التعليمات المحقونة تحقيقه (What the injected instructions could achieve) محدودًا بما تسمح به أدوات نجم أسيست دون تأكيد (was bounded by what Najm Assist's tools allowed without confirmation) (9.2). فأقل الصلاحيات (Least privilege) ضابطٌ للاستجابة للحوادث (is an incident-response control) يُختار قبل الحادثة بزمنٍ طويل (chosen long before the incident).
- **إيجاد المتأثرين يحتاج إلى سجلات المخرجات (Finding affected people needs output logs).** فسؤال «من رأى الرابط؟» ⁦("Who saw the link?")⁩ يعني ربط الجلسات (means joining sessions) التي استرجعت `kb-fees-2026-03` بعد الساعة 19:55 (after 19:55) باستجاباتها (with their responses).
- **التراجع (Rollback).** أخضِع الموجّهات واختيارات النماذج ولقطات قاعدة المعرفة وبيانات التدريب لإدارة الإصدارات (Version prompts, model choices, knowledge-base snapshots and training data)، كي يكون التعافي تغييرًا في الإعدادات (so recovery is a configuration change) أو إعادة تدريبٍ من لقطةٍ معروفٍ أنها سليمة (or a retrain from a known-good snapshot)، كما في التنبيهات الذكية (Smart Alerts) (8.3)، لا إعادة بناءٍ طارئة (not an emergency rebuild).
- **ليست كل حادثة ذكاءٍ اصطناعي هجومًا (Not every AI incident is an attack).** فتحديثٌ للنموذج يقتبس رسومًا خاطئة (A model update that quotes wrong fees) يضرّ العملاء أيضًا (also harms customers). مرِّر أضرار الذكاء الاصطناعي عبر العملية نفسها (Route AI harm through the same process)، بالتعاون مع فريق حوكمة الذكاء الاصطناعي بقيادة ليلى (with Layla's AI governance team). ويقع على مزوّدي أنظمة الذكاء الاصطناعي عالية المخاطر (Providers of high-risk AI systems) أيضًا واجبات إبلاغٍ عن الحوادث الجسيمة (also have serious-incident reporting duties) بموجب قانون الذكاء الاصطناعي الأوروبي (under the EU AI Act) (Art. 73) بمجرد سريان قواعد الأنظمة عالية المخاطر (once the high-risk rules apply)؛ وقد أُرجئت مواعيدها وقت كتابة هذا النص (their dates were pushed back at the time of writing)، فتحقّق من النص الحالي (so check the current text) وراجِع دورة *AI Governance: Zero to Hero*.

**حوادث الأطراف الثالثة (Third-party incidents).** تبدأ حوادث كثيرة لدى مورّد (Many incidents start at a supplier): فثغرة حقن SQL في MOVEit Transfer (the MOVEit Transfer SQL injection)، التي استُغلّت على نطاقٍ واسع عام 2023 (exploited at scale in 2023)، بلغت مؤسساتٍ كثيرة (reached many organisations) عبر برمجياتٍ شغّلتها هي أو مورّدوها (through software they or their suppliers ran). احتفظ بدليل تشغيلٍ لحالة «أبلغنا المورّد» (Keep a "supplier told us" runbook): ما البيانات والوصول اللذان يحوزهما كل مورّد (what data and access each supplier holds)، وجهات الاتصال (contacts)، وكيف تقطع وصوله بسرعة (and how to cut its access fast). ويشدّد قانون DORA على مخاطر الأطراف الثالثة في تقنية المعلومات والاتصالات (DORA stresses ICT third-party risk)، ومزوّدو النماذج وقواعد بيانات المتجهات لديك (and your model and vector database providers) مورّدون أيضًا (are suppliers too).

**مراجعة ما بعد الحادثة (The post-incident review).** خلال أسبوعين تقريبًا (Within about two weeks)، أجرِ مراجعةً **بلا لوم (blameless)**: اسأل كيف جعل النظامُ الإخفاقَ ممكنًا (ask how the system made the failure possible)، لا من يجب معاقبته (not whom to punish)، لأن الناس الذين يخشون اللوم يُخفون الحقائق (because people who fear blame hide facts). والمخرجات (Outputs): خطٌّ زمني متفقٌ عليه (an agreed timeline)؛ وما سار على ما يرام (what went well)؛ والعوامل المساهمة (contributing factors)، وهي عادةً عدة عوامل (usually several)؛ وإجراءاتٌ لها مالكون وتواريخ (owned, dated actions) تُتابَع حتى الإغلاق (tracked to closure)؛ وقواعد رصدٍ جديدة وخطواتٌ جديدة في أدلة التشغيل وحالاتٌ جديدة للفريق الأحمر (and new detections, runbook steps and red-team cases) (9.4).

**تمرَّن (Practise).** **تمرين المحاكاة النظرية (tabletop exercise)** تمرينٌ قائم على النقاش (is a discussion-based drill): يناقش الفريق سيناريو (the team talks through a scenario) بينما يضيف الميسّر وقائع جديدة (while a facilitator adds new facts)، دون لمس الأنظمة (without touching systems). أما **أيام التمرين العملي (Game days)** فتُشغّل المفاتيح وعمليات الاستعادة الحقيقية (exercise real switches and restores) في بيئة اختبار (in a test environment). وكلاهما يكشف رقم الهاتف المفقود (Both find the missing phone number) ما دام إصلاح ذلك رخيصًا (while it is cheap).

## 🧰 الأدوات (The toolkit)
| الضابط أو المعيار أو الأداة (Control, standard or tool) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **NIST SP 800-61 Rev. 3** — توصيات NIST للاستجابة للحوادث | توصيات NIST للاستجابة للحوادث (NIST's incident response recommendations) (2025)، منظَّمةً حول وظائف إطار CSF 2.0 (organised around the CSF 2.0 functions) | كتابة خطة استجابةٍ للحوادث أو تحديثها (Writing or refreshing an IR plan) وربطها بإدارة المخاطر (and tying it to risk management) |
| **ISO/IEC 27035** — سلسلة معايير دولية | سلسلة معايير دولية لإدارة الحوادث الأمنية (International standard series for security incident management) | مواءمة الاستجابة للحوادث مع نظام إدارةٍ وفق ISO/IEC 27001 (Aligning IR with an ISO/IEC 27001 management system) |
| **RFC 3227** — إرشادات جمع الأدلة | إرشادات IETF لجمع الأدلة (IETF guidelines for evidence collection)، بما فيها ترتيب التطاير (including the order of volatility) | كتابة خطوات التعامل مع الأدلة في أدلة التشغيل (Writing evidence-handling steps into runbooks) |
| **Incident runbooks** — أدلة تشغيل الحوادث | أدلة استجابةٍ خطوةً بخطوة لكل نوع حادثة (Step-by-step playbooks per incident type)، مع المالكين والقرارات (with owners and decisions) | كل حادثةٍ مرجّحة (Each likely incident): الاستيلاء على الحساب (account takeover)، والمفتاح المسرَّب (leaked key)، وسوء سلوك الذكاء الاصطناعي (AI misbehaviour) |
| **Kill switches** — مفاتيح الإيقاف الطارئ | علاماتٌ وقت التشغيل (Runtime flags) تعطّل ميزةً أو أداةً أو مصدر بيانات (that disable a feature, tool or data source) دون إعادة نشر (without a redeploy) | أي قدرةٍ خطرة (Any risky capability)، ولا سيما أدوات الوكلاء ومصادر الاسترجاع (especially agent tools and retrieval sources) |
| **Tabletop exercise** — تمرين المحاكاة النظرية | تمرينٌ قائم على النقاش يأخذ الفريق عبر سيناريو (Discussion-based drill that walks a team through a scenario) | مرةً في السنة على الأقل لكل نظامٍ حرج (At least yearly per critical system)، وبعد التغييرات الكبرى (and after major changes) |
| **Blameless post-incident review** — مراجعة ما بعد الحادثة بلا لوم | مراجعةٌ للعوامل المساهمة (Review of contributing factors)، تنتهي بإجراءاتٍ متتبَّعة (ending in tracked actions) | بعد كل حادثةٍ جسيمة (After every serious incident) وكل حادثةٍ وشيكة مفيدة للتعلّم (and instructive near miss) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
بعد ليلة الخميس (After Thursday night)، يعيد جاسم كتابة دليل التشغيل (Jassim rewrites the runbook)؛ ويعتمده حمد (Hamad approves it)؛ ويُتمرَّن عليه فصليًا (it is rehearsed quarterly).

**PB-07 — نجم أسيست: مخرجاتٌ ضارة أو إجراءٌ غير مصرّح به (Najm Assist: harmful output or unauthorised action)، الإصدار 2 (v2)**

*المحفّزات (Triggers):* قواعد الرصد NA-01 أو NA-02 أو NA-04 (detections NA-01, NA-02 or NA-04) (10.1)؛ وشكوى عميلٍ بشأن إجابةٍ أو إجراءٍ من المساعد (a customer complaint about an assistant answer or action)؛ وتقريرٌ من الفريق الأحمر أو من باحث (a red-team or researcher report) يُظهر أثرًا فعليًا (showing live impact).

*الخطورة (Severity)*

| المستوى (Level) | المعايير لنجم أسيست (Criteria for Najm Assist) |
|---|---|
| SEV1 | تلقّى عملاء تعليماتٍ أو روابط ضارة (Customers received harmful instructions or links)، أو نُفّذ إجراءٌ غير مصرّح به (an unauthorised action executed)، أو كُشفت بيانات عميلٍ آخر (or another customer's data was disclosed) |
| SEV2 | جرت محاولة مخرجاتٍ أو إجراءٍ ضار لكنها حُجبت (Harmful output or action attempted but blocked)؛ أو اشتباهٌ في محتوى مسموم في فهرسٍ حي (suspected poisoned content in a live index) |
| SEV3 | جلسةٌ شاذة واحدة (One anomalous session)؛ ولم يُعثر على أثرٍ على العملاء بعد (no customer impact found yet) |

*أول 60 دقيقة (First 60 minutes)*

| بحلول (By) | الإجراء (Action) | المالك (Owner) |
|---|---|---|
| 10 دقائق (10 min) | الإقرار (Acknowledge)؛ وفتح غرفة الحادثة في مساحة العمل خارج النطاق (open the incident room in the out-of-band workspace)؛ وتعيين قائد الحادثة والمدوِّن (appoint IC and scribe)؛ وبدء سجل القرارات (start the decision log) | مناوب مركز العمليات الأمنية (SOC on-call) |
| 20 دقيقة (20 min) | الاحتواء (Contain): إطفاء المجموعة أو الأداة المتأثرة (switch off the affected collection or tool) (`assist.kb.*`، `assist.tool.*`)؛ وإن لم يتضح الأمر (if unclear)، وضع أسيست في وضع الأسئلة الشائعة فقط (put Assist in FAQ-only mode) | قائد الحادثة، مع رانيا أو نائبها (IC, with Rania or her deputy) |
| 30 دقيقة (30 min) | الحفظ (Preserve): تصدير السجلات (export logs)؛ والتقاط لقطةٍ للفهرس والمستندات المشتبه بها مع سجل تعديلاتها (snapshot the index and suspect documents with edit history)؛ وتدوين قيم التجزئة (record hashes) | القائد التقني (Technical lead) |
| 40 دقيقة (40 min) | تحديد النطاق (Scope): الجلسات التي استرجعت المحتوى المشتبه به أو استدعت الأداة (sessions that retrieved the suspect content or hit the tool)؛ والعملاء الذين رأوا مخرجاتٍ غير مرشَّحة (customers who saw unfiltered output) | القائد التقني ودانة (Technical lead, Dana) |
| 60 دقيقة (60 min) | تقييم الإخطار (Assess notification): البيانات الشخصية (personal data)، والضرر على العملاء (customer harm)، والعملاء في الاتحاد الأوروبي (EU customers)، وبيانات البطاقات (card data) | سارة والفريق القانوني (Sara, legal) |
| 60 دقيقة (60 min) | أول تحديثٍ لحمد ولقطاع الأعمال (First update to Hamad and the business)، مع موعد التحديث التالي (with the next update time) | قائد الحادثة (IC) |

*الاستئصال والتعافي (Eradicate and recover).* أزِل المحتوى المسموم وأجزاءه وتضميناته (Remove the poisoned content, chunks and embeddings)؛ وراجِع تعديلات الحساب في آخر 90 يومًا (review the account's edits for the last 90 days)؛ وأعِد تعيينه وافرض عليه المصادقة متعددة العوامل (reset it and enforce MFA)؛ وأعِد تفعيل المجموعة (re-enable the collection) بعد مراجعة المحتوى (after content review) وفحصٍ نظيف بمصنِّف الحقن (and a clean injection-classifier scan)؛ وراقب NA-04 عن كثب مدة 72 ساعة (watch NA-04 closely for 72 hours).

*العملاء (Customers).* قوالب معتمدة مسبقًا بالعربية والإنجليزية (Pre-approved Arabic and English templates)؛ ويعيد فريق مكافحة الاحتيال إصدار البطاقات (the fraud team reissues cards) لكل من أدخل بياناته في الموقع الخارجي (for anyone who entered details on the external site).

*التعلّم (Learn).* مراجعةٌ بلا لوم خلال 10 أيام عمل (Blameless review within 10 working days)؛ والإجراءات في سجل المخاطر (actions in the risk register)؛ وإضافة الهجوم إلى مجموعة اختبارات الفريق الأحمر للذكاء الاصطناعي (the attack added to the AI red-team suite) (9.4).

## 🛠️ التمارين (Exercises)
- 🟢 اكتب مصفوفة خطورةٍ وقائمة جهات اتصال في صفحةٍ واحدة (Write a one-page severity matrix and contact sheet) لنظامٍ تملكه أو تعرفه (for a system you own or know). *يكتمل عندما (Done when):* تحتوي على ثلاثة مستويات على الأقل بمعايير ملموسة (it has at least three levels with concrete criteria)، ويكون لكل دورٍ من الأدوار الرئيسية (every top-level role) شخصٌ أساسي وبديلٌ مسمَّيان (has a named primary and backup)، وتكون القناة خارج النطاق مكتوبة (and the out-of-band channel is written down).
- 🟡 أدِر تمرين محاكاةٍ نظرية مدته 60 دقيقة (Run a 60-minute tabletop) مع ثلاثة إلى خمسة زملاء (with three to five colleagues) على سيناريو ليلة الخميس أو على نظامك الخاص (on the Thursday-night scenario or your own system)، مع خمسة مُدخلاتٍ موقوتة (with five timed injects)، مثل «عميلٌ ينشر لقطة شاشة على وسائل التواصل الاجتماعي» ("a customer posts a screenshot on social media"). *يكتمل عندما (Done when):* يكون لديك سجل قراراتٍ مؤرَّخ زمنيًا (you have a timestamped decision log) وثلاث فجواتٍ على الأقل (and at least three gaps)، مثل مفتاحٍ أو جهة اتصالٍ أو حقل سجلٍّ مفقود (a missing switch, contact or log field)، لكلٍّ منها مالكٌ وتاريخ (each with an owner and a date).
- 🔴 في مختبرٍ محلي (In a local lab) مع تطبيق نموذجٍ لغوي كبير بنيته بنفسك (with an LLM app you built)، أي نموذجٍ صغير وأداةٍ واحدة غير ضارة ومجلد مستنداتٍ للاسترجاع (a small model, one harmless tool, a folder of documents for retrieval)، ازرع تعليمةً غير ضارة في مستندٍ واحد (plant a benign instruction in one document)، مثل «اختم كل إجابةٍ بكلمة BANANA» ("end every answer with the word BANANA"). استجب كما تستجيب لحادثة (Respond as to an incident): ارصدها من السجلات (detect it from logs)، وأطفئ الاسترجاع من ذلك المجلد (switch off retrieval from that folder)، واحصر الجلسات المتأثرة (list affected sessions)، وأزِل المستند وتضميناته (remove the document and its embeddings)، وتحقّق (and verify). *يكتمل عندما (Done when):* تُنتج قائمة الجلسات المتأثرة من السجلات وحدها (you produce the affected-session list from logs alone)، ولا يعود الفهرس يُرجع المستند (the index no longer returns the document)، وتكون كل مرحلةٍ موقوتة (and each phase is timed).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **انتظار اليقين قبل الإعلان (Waiting for certainty before declaring).** أعلِن مبكرًا بخطورةٍ مؤقتة (Declare early with a provisional severity)؛ فالتخفيض رخيص (downgrading is cheap).
- **قائد الحادثة يجري التحليل الجنائي بنفسه (The IC doing the forensics).** عندئذٍ لا أحد يدير الاستجابة (Then nobody is running the response). افصل بين الأدوار (Separate the roles)، حتى في الفريق الصغير (even in a small team).
- **إتلاف الأدلة أثناء الاحتواء (Destroying evidence while containing).** التقط اللقطات وصدّر ودوِّن (Snapshot, export and record) قبل أن تُنهي أو تنظّف أي شيء (before you terminate or clean anything)، ونسّق خارج النطاق (and coordinate out of band) إذا احتُمل أن تكون الأنظمة الداخلية مخترقة (if internal systems may be compromised).
- **تدوير بيانات الاعتماد الواضحة فقط (Rotating only the obvious credential).** دوِّر كل ما يمكن بلوغه (Rotate everything reachable)، وابحث عن حساباتٍ أو مفاتيح أنشأها المهاجم (and look for accounts or keys the attacker created).
- **مراجعةٌ تنتهي باللوم، أو بإجراءاتٍ لا يتابعها أحد (A review that ends in blame, or in actions nobody tracks).** سمِّ العوامل المساهمة (Name contributing factors)، وعيّن المالكين والتواريخ (assign owners and dates)، وتحقّق من الإغلاق (and check closure).

## 🧾 الخلاصة (Recap)
- الاستجابة للحوادث دورةٌ متمرَّسٌ عليها (Incident response is a practised cycle): الاستعداد (prepare)، والرصد والتحليل (detect and analyse)، والاحتواء (contain)، والاستئصال والتعافي (eradicate and recover)، والتعلّم (learn)؛ ويربطها الإصدار NIST SP 800-61 Rev. 3 بإطار CSF 2.0 (ties it to CSF 2.0).
- الاستعداد (Preparation)، أي الأدوار وأدلة التشغيل وجهات الاتصال والقناة خارج النطاق والسجلات ومفاتيح الإيقاف الطارئ والتمارين (roles, runbooks, contacts, out-of-band channel, logs, kill switches, drills)، هو ما يحدّد كيف تمضي الليلة العصيبة (decides how a bad night goes).
- أثناء الحادثة (During an incident): قائدٌ للحادثة (an incident commander)، وسجل قرارات (a decision log)، والأدلة قبل التغيير (evidence before change)، والاحتواء قبل التنظيف (containment before cleanup).
- تبدأ المهل القانونية من لحظة العلم (Legal clocks start at awareness)؛ أشرِك مسؤول حماية البيانات والفريق القانوني مبكرًا (involve the DPO and legal early).
- تحتاج حوادث الذكاء الاصطناعي إلى سياقٍ مسجَّل (AI incidents need logged context)، واستئصالٍ يشمل الفهارس وذاكرات التخزين المؤقت (eradication across indexes and caches)، وموجّهاتٍ ونماذج وبياناتٍ ذات إصداراتٍ تتيح التراجع (versioned prompts, models and data for rollback)، وسجلات مخرجاتٍ لإيجاد العملاء المتأثرين (and output logs to find affected customers).

## ✍️ اختبر نفسك (Check yourself)

**1. في الساعة 21:55 (At 21:55)، يؤكد جاسم أن مقالًا مسمومًا في مجموعة الرسوم (a poisoned article in the fees collection) يجعل نجم أسيست يعرض رابطًا خارجيًا (is making Najm Assist show an external link). ما أفضل خطوة احتواءٍ أولى (What is the best first containment step)؟**

- A. إيقاف تطبيق الهاتف بالكامل حتى يُعرف السبب الجذري (Shut down the whole mobile app until the root cause is known)
- B. إطفاء الاسترجاع من مجموعة الرسوم (Switch off retrieval from the fees collection)، ثم حفظ المقال وسجل تعديلاته والسجلات (then preserve the article, its edit history and the logs) قبل حذف أي شيء (before deleting anything)
- C. حذف المقال فورًا وإغلاق الحادثة (Delete the article immediately and close the incident)
- D. إعادة تدريب النموذج كي يتجاهل مثل هذه التعليمات (Retrain the model so it ignores such instructions)

<details><summary>الإجابة</summary>

**B.** فهو يوقف الضرر بأقل خسارةٍ في الخدمة (It stops the harm with the least service loss) ويحفظ الأدلة (and keeps the evidence). أما A فغير متناسب (is out of proportion) ما دام هناك مفتاحٌ موجَّه (when a targeted switch exists)؛ وC يُتلف الأدلة ويتجاهل النطاق (destroys evidence and ignores scope)؛ وD بطيء (is slow)، ولا يوجد إصلاحٌ تقني كامل لحقن الموجّهات (and no complete technical fix for prompt injection exists). انظر: 🟡 التعمق أكثر (Going deeper).

</details>

**2. في الساعة 09:00 يوم الاثنين (At 09:00 on Monday)، تؤكد سارة أن بياناتٍ شخصية لعملاء نجم، بمن فيهم مقيمون في الاتحاد الأوروبي (personal data of Najm customers, including EU residents)، قد كُشفت (was exposed). ولم تُعرف كل الوقائع بعد (Not all facts are known yet). ما الذي ينطبق بموجب اللائحة العامة لحماية البيانات (Under GDPR, what applies)؟**

- A. الإخطار فقط بعد اكتمال التحقيق، مهما طال (Notify only once the investigation is complete, however long it takes)
- B. إخطار السلطة الرقابية دون تأخيرٍ لا مبرّر له (Notify the supervisory authority without undue delay)، وخلال 72 ساعة من العلم حيثما أمكن (and, where feasible, within 72 hours of becoming aware)؛ ويجوز تقديم المعلومات على مراحل (information may be provided in phases)
- C. لا شيء (Nothing)، لأن المقر الرئيسي لنجم ليس في الاتحاد الأوروبي (because Najm is not headquartered in the EU)
- D. الإخطار فقط إذا كُشفت أرقام البطاقات (Notify only if card numbers were exposed)

<details><summary>الإجابة</summary>

**B.** تسري المادة 33 من لحظة العلم (Article 33 runs from awareness) وتسمح بتقديم المعلومات على مراحل (and allows phased information). أما A فيتجاهل المهلة (ignores the clock). وC افتراض (is an assumption): فنجم تخدم عملاء في الاتحاد الأوروبي (Najm serves EU customers)، وتحديد النطاق حكمٌ قانوني لا افتراضٌ مسبق (and scope is a legal judgement, not a default). وD يخترع شرطًا (invents a condition). انظر: 🟡 التعمق أكثر (Going deeper).

</details>

**3. حاويةٌ مخترقة في عنقود Kubernetes لدى نجم (A compromised container in Najm's Kubernetes cluster) على وشك أن تُستبدل آليًا (is about to be replaced automatically). ماذا ينبغي أن يفعل القائد التقني أولًا (What should the technical lead do first)؟**

- A. يتركها تُستبدل، لأن الحاوية الجديدة نظيفة (Let it be replaced, because a fresh container is clean)
- B. يعزلها (Isolate it)، ويوقف الاستبدال مؤقتًا حيثما أمكن (pause the replacement where possible)، ويلتقط حالتها وسجلاتها قبل إتلافها (and capture its state and logs before it is destroyed)
- C. يحذف العقدة فورًا (Delete the node immediately)
- D. يشغّل فحصًا بمضاد الفيروسات داخل الحاوية (Run an antivirus scan inside the container)

<details><summary>الإجابة</summary>

**B.** الأدلة المتطايرة أولًا (Volatile evidence goes first) (RFC 3227)؛ فالاستبدال سيُتلف سجلّ ما حدث (replacement would destroy the record of what happened). أما A وC فيُضيّعان الأدلة (lose the evidence)؛ وD يغيّر النظام (changes the system). انظر: 🟡 التعمق أكثر (Going deeper).

</details>

**4. أثناء حادثةٍ من المستوى SEV1 (During a SEV1)، يبدأ علي، الذي يعمل قائدًا للحادثة (acting as incident commander)، بقراءة التقاطات الحزم بنفسه (starts reading packet captures himself) لأنه أفضل محلّلٍ في المناوبة (because he is the best analyst on shift). ما المشكلة (What is the problem)؟**

- A. لا مشكلة؛ فينبغي أن يقوم قائد الحادثة بأهم تحليل (None; the IC should do the most important analysis)
- B. لم يعد أحدٌ يدير الاستجابة الآن (Nobody is now running the response)، فتتعطّل الأولويات والقرارات والتحديثات (so priorities, decisions and updates stall)؛ والتحليل من شأن القائد التقني (analysis belongs with the technical lead)
- C. التقاطات الحزم غير مفيدة في الحوادث (Packet captures are not useful in incidents)
- D. لا يجوز إلا لكبير مسؤولي أمن المعلومات (Only the CISO) قراءة التقاطات الحزم (may read packet captures)

<details><summary>الإجابة</summary>

**B.** مهمة قائد الحادثة هي الصورة الكاملة (The IC's job is the whole picture). أما A فيخلط بين الأدوار (confuses the roles)؛ وC وD خاطئان (are false). انظر: 🟢 الأساسيات (The essentials).

</details>

**5. أيّ نتيجةٍ من نتائج مراجعة ما بعد الحادثة (Which post-incident review finding) هي الأكثر فائدة (is most useful)؟**

- A. «كان على علي أن يكون أكثر حرصًا مع حساب المحتوى.» ⁦("Ali should have been more careful with the content account.")⁩
- B. «كان مهاجمٌ متطوّر هو المسؤول؛ ولا حاجة إلى أي إجراء.» ⁦("A sophisticated attacker was responsible; no action needed.")⁩
- C. «العوامل المساهمة (Contributing factors): لا مصادقة متعددة العوامل على حساب المحتوى (no MFA on the content account)، ولا مراجعة للمحتوى القابل للاسترجاع (no review of retrievable content)، ومفتاحٌ غير موثّق (an undocumented switch). الإجراءات (Actions): المصادقة متعددة العوامل (MFA) بحلول 15 أكتوبر (طارق)؛ وسير عمل المراجعة (review workflow) بحلول 30 أكتوبر (رانيا)؛ والتمرّن على المفتاح ضمن PB-07 (switch drilled in PB-07) (جاسم).»
- D. «ينبغي إطفاء نجم أسيست نهائيًا.» ⁦("Najm Assist should be switched off permanently.")⁩

<details><summary>الإجابة</summary>

**C.** فهي بلا لوم (It is blameless)، وتسمّي عدة عوامل مساهمة (names several contributing factors)، وتنتهي بإجراءاتٍ لها مالكون وتواريخ (and ends in owned, dated actions). أما A فيلوم شخصًا (blames a person)، وB لا يتعلّم شيئًا (learns nothing)، وD يبالغ في ردّ الفعل (overreacts) بدلًا من إصلاح الأسباب (instead of fixing causes). انظر: 🔴 نظرة الخبير (Expert view).

</details>

## 📚 المراجع (References)
- NIST SP 800-61 Rev. 3، توصيات واعتبارات الاستجابة للحوادث لإدارة مخاطر الأمن السيبراني (Incident Response Recommendations and Considerations for Cybersecurity Risk Management)، 2025 — https://csrc.nist.gov/pubs/sp/800/61/r3/final
- إطار NIST للأمن السيبراني 2.0 (NIST Cybersecurity Framework 2.0) — https://www.nist.gov/cyberframework
- RFC 3227، إرشادات جمع الأدلة وأرشفتها (Guidelines for Evidence Collection and Archiving) — https://www.rfc-editor.org/rfc/rfc3227
- سلسلة ISO/IEC 27035، إدارة حوادث أمن المعلومات (Information security incident management)؛ وتحقّق من الإصدارات الحالية (check the current editions) — https://www.iso.org/
- اللائحة العامة لحماية البيانات (GDPR)، اللائحة Regulation (EU) 2016/679، المواد 4 و33 و34 (Arts. 4, 33 and 34) — https://eur-lex.europa.eu/eli/reg/2016/679/oj
- قانون DORA، اللائحة Regulation (EU) 2022/2554 — https://eur-lex.europa.eu/eli/reg/2022/2554/oj
- قانون الذكاء الاصطناعي الأوروبي (EU AI Act)، اللائحة Regulation (EU) 2024/1689 — https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- Greshake, K. et al. (2023)، «ليس ما اشتركت فيه: اختراق تطبيقاتٍ واقعية مدمجة بالنماذج اللغوية الكبيرة عبر حقن الموجّهات غير المباشر» ("Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection") — https://arxiv.org/abs/2302.12173

---

# 10.3 — إدارة الثغرات والإفصاح عنها وبرامج مكافآت الثغرات (Vulnerability management, disclosure and bug bounties)
*المستوى (Level): 🔴 متقدم (Advanced)* · *المتطلبات (Prerequisites): 1.3، 6.2، 10.2* · *المرحلة (Phase): Operate, Respond*

## ⚡ الدرس في دقيقة (In 60 seconds)
- **إدارة الثغرات (Vulnerability management)** هي الدورة المستمرة (the continuous cycle) لإيجاد مواطن الضعف فيما تشغّله (of finding weaknesses in what you run)، وترتيبها (ranking them)، وإصلاحها أو تخفيفها (fixing or mitigating them)، وإثبات الإصلاح (and proving the fix)، فوق **جرد أصولٍ (asset inventory)** دقيق (on top of an accurate asset inventory).
- رتّب الأولويات بحسب المخاطر لا الخطورة وحدها (Prioritise by risk, not severity alone). يصف **CVSS v4.0** مدى سوء الثغرة (describes how bad a flaw is)؛ ويقدّر **EPSS** مدى احتمال استغلالها (estimates how likely exploitation is)؛ ويُدرج **كتالوج CISA KEV (CISA KEV catalogue)** الثغرات المعروف استغلالها (lists flaws known to be exploited)؛ وسياقك (your context)، أي هل النظام مكشوفٌ للإنترنت وهل يحوي بيانات العملاء (internet-facing, customer data)، هو ما يحدّد الترتيب (sets the order).
- حدّد مواعيد نهائية للمعالجة بحسب الأولوية (Set remediation deadlines by priority)، وتتبّع الاستثناءات بمالكٍ وتاريخ انتهاء (track exceptions with an owner and an expiry date)، وقِس وقت المعالجة (and measure time to remediate).
- اجعل الإبلاغ سهلًا (Make reporting easy): **سياسة إفصاحٍ عن الثغرات (vulnerability disclosure policy, VDP)** مع ملاذٍ آمن (with safe harbour)، وقناةٌ مراقَبة (a monitored channel)، وملف `security.txt` (a security.txt file) (RFC 9116).
- **برنامج مكافآت الثغرات (bug bounty)** يدفع مقابل النتائج الصحيحة (pays for valid findings). لا تبدأه إلا بعد أن تعمل سياسة الإفصاح والفرز والإصلاح (Start one only after the VDP, triage and fixing work)، وابدأه خاصًا (and start private).
- أكبر فخ (Biggest trap): آلاف النتائج مرتّبةٌ حسب درجة CVSS الأساسية (thousands of findings sorted by CVSS base score)، والثغرة الوحيدة المستغَلّة على البوابة المكشوفة للإنترنت (with the one exploited flaw on the internet-facing gateway) ضائعةٌ في المنتصف (lost in the middle).

## 🧭 لماذا يهم (Why it matters)
يعثر علي على رسالة بريدٍ عمرها ثلاثة أسابيع (Ali finds a three-week-old email) في صندوق البريد العام للبنك (in the bank's general inbox). تكتب فيها باحثةٌ (A researcher writes) أنها حين غيّرت معرّف شركةٍ في طلبٍ إلى بوابة الشركات الصغيرة (by changing a company ID in an SME Portal request) من حساب شركتها الخاص (from her own business account)، رأت قائمة فواتير شركةٍ أخرى (she saw another company's invoice list). ولم يردّ أحد (Nobody replied). وبالأمس نشرت أن «بنك نجم يتجاهل البلاغات الأمنية» ("Najm Bank ignores security reports"). ويريد حمد، كبير مسؤولي أمن المعلومات (CISO)، جوابين بحلول يوم الأحد (wants two answers by Sunday): كيف كان ينبغي التعامل مع هذا البلاغ (how this report should have been handled)، ولماذا لا يملك البنك طريقةً منشورة للإبلاغ (and why the bank has no published way to report one). وفي الأثناء (Meanwhile)، لدى فرق طارق 2,300 نتيجة فحصٍ مفتوحة (Tariq's teams have 2,300 open scanner findings) مرتّبةً حسب CVSS (sorted by CVSS)، دون مواعيد نهائية متفقٍ عليها (with no agreed deadlines).

تُظهر الحالات العامة حجم الرهان (Public cases show the stakes). ففي اختراق Equifax (In the Equifax breach) عام 2017، استغلّ المهاجمون ثغرةً في Apache Struts (attackers exploited an Apache Struts vulnerability) (CVE-2017-5638) كان إصلاحها قد نُشر قبل نحو شهرين من دخولهم (whose fix had been published about two months before they got in). وحين ظهرت Log4Shell (CVE-2021-44228) في ديسمبر 2021 (in December 2021)، سارعت المؤسسات للإجابة عن سؤال «أين نشغّل Log4j؟» ⁦("where do we run Log4j?")⁩، وكانت المؤسسات التي تملك جردًا دقيقًا وقوائم مكونات البرمجيات (those with accurate inventories and SBOMs) (6.2) الأسرعَ إجابة (answered fastest). وعلمت Capital One باختراقها عام 2019 (Capital One learned of its 2019 breach) من بلاغٍ خارجي (from an outside tip) أُرسل إلى عنوان الإفصاح المسؤول لديها (sent to its responsible-disclosure address): فقناة الإبلاغ مصدرٌ للرصد أيضًا (the reporting channel is a detection source too).

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**المصطلحات (Terms).** **الثغرة (vulnerability)** ضعفٌ يمكن استغلاله لإحداث ضرر (a weakness that can be exploited to cause harm). ومعرّف **CVE** (Common Vulnerabilities and Exposures) يسمّي ثغرةً معروفة علنًا في منتجٍ ما (names a publicly known vulnerability in a product)، وتخصّصه **هيئة ترقيم CVE (CNA, CVE Numbering Authority)**، مثل مورّدٍ أو جهة تنسيق (such as a vendor or coordinator). و**CWE** يسمّي نوع الضعف (names the weakness type): فخلل بوابة الشركات الصغيرة (the SME Portal bug) هو CWE-639، أي تجاوز التفويض عبر مفتاحٍ يتحكم فيه المستخدم (authorisation bypass through a user-controlled key)، وهو من نوع IDOR (3.3). وكثيرٌ من أهم ثغرات البنك (Many of a bank's most important vulnerabilities) موجودٌ في شيفرته الخاصة (are in its own code)، ولن يكون لها معرّف CVE أبدًا (and will never have a CVE).

**الدورة (The cycle).**

```mermaid
flowchart RL
    I["الجرد وقوائم مكونات البرمجيات<br/>(Inventory and SBOMs)"] --> F["الإيجاد: الماسحات والاختبارات والبلاغات<br/>(Find: scanners, tests, reports)"]
    F --> T["الفرز: حقيقية ومنشورة وقابلة للبلوغ<br/>(Triage: real, deployed, reachable)"]
    T --> P["ترتيب الأولويات: الاستغلال المعروف واحتمال الاستغلال والتعرض والخطورة<br/>(Prioritise: KEV, EPSS, exposure, CVSS)"]
    P --> R["الإصلاح أو التخفيف<br/>(Fix or mitigate)"]
    P --> X["القبول بمالك وتاريخ انتهاء<br/>(Accept with owner and expiry)"]
    R --> V["التحقق والإغلاق<br/>(Verify and close)"]
    X -->|"بلوغ تاريخ الانتهاء (Expiry reached)"| P
    V --> M["المقاييس والدروس<br/>(Metrics and lessons)"]
    M --> I
```

1. **الجرد (Inventory).** لا يمكنك تحديث ما لا تعرف أنك تشغّله (You cannot patch what you do not know you run): المضيفات (hosts)، والحاويات (containers)، وواجهات البرمجة (APIs) (API9، 4.1)، والمكتبات عبر قوائم مكونات البرمجيات (libraries via SBOMs) (6.2)، ونماذج الذكاء الاصطناعي ومجموعات البيانات والموجّهات وموصلات الأدوات (and AI models, datasets, prompts and tool connectors).
2. **الإيجاد (Find).** ماسحات البنية التحتية والحاويات والاعتماديات (Infrastructure, container and dependency scanners)، أي SCA، وSAST وDAST (6.1)، وفحوص الوضع الأمني السحابي (cloud posture checks) (7.1)، واختبارات الاختراق (penetration tests)، واختبارات الفريق الأحمر للذكاء الاصطناعي (AI red-teaming) (9.4)، وتنبيهات المورّدين (vendor advisories)، والبلاغات الخارجية (and outside reports).
3. **الفرز (Triage).** هل هي حقيقية؟ ⁦(Is it real?)⁩ هل الإصدار المتأثر منشور؟ ⁦(Is the affected version deployed?)⁩ هل يمكن بلوغ الشيفرة المعرَّضة؟ ⁦(Is the vulnerable code reachable?)⁩
4. **ترتيب الأولويات (Prioritise)**، انظر أدناه (below).
5. **الإصلاح (Fix)**، أو **التخفيف (mitigate)** أولًا إذا كان الإصلاح سيستغرق وقتًا (first if the fix will take time)، مثل قاعدةٍ في جدار حماية تطبيقات الويب (a WAF rule)، أو ميزةٍ معطَّلة (a disabled feature)، أو وصولٍ مقيَّد (restricted access)، مع تدوين ذلك (and record it).
6. **التحقق (Verify)** بإعادة الفحص أو الاختبار (by rescanning or retesting)، ثم الإغلاق (then close).
7. **القبول (Accept)** صراحةً فقط (only explicitly): مالك مخاطر مسمّى (a named risk owner)، وضوابط تعويضية (compensating controls)، وتاريخ انتهاء (and an expiry date).

**الخطورة ليست الأولوية (Severity is not priority).** يمنح **CVSS** (Common Vulnerability Scoring System)، أي نظام تقييم الثغرات الشائع الصادر عن FIRST (from FIRST)، خصائصَ الثغرة درجةً من 0 إلى 10 (scores a vulnerability's characteristics from 0 to 10). وللإصدار 4.0 (Version 4.0)، الصادر في نوفمبر 2023 (November 2023)، أربع مجموعات مقاييس (four metric groups): **الأساسية (Base)**، أي الجوهرية: كيف تُهاجَم وما الذي تؤثر فيه (intrinsic: how it is attacked and what it affects)؛ و**التهديد (Threat)**، أي مدى نضج الاستغلالات (how mature exploits are)؛ و**البيئية (Environmental)**، أي سياقك ومتطلباتك الأمنية (your context and security requirements)؛ و**التكميلية (Supplemental)**، أي معلوماتٌ إضافية (extra information)، مثل ما إذا كان يمكن أتمتة الاستغلال (such as whether exploitation can be automated). وتُوسَم الدرجات بحسب المجموعات المستخدمة (Scores are labelled by the groups used): CVSS-B للأساسية فقط (for base only)، ثم CVSS-BT أو CVSS-BE أو CVSS-BTE. والدرجة الأساسية المأخوذة من قاعدة بيانات (A base score from a database) نقطة انطلاق (is a starting point)، لا أولويتك (not your priority). وتوقّع أن تجد درجات الإصدار v3.1 في المصادر أيضًا (Expect v3.1 scores in feeds too).

إشارتان أخريان (Two more signals):
- **EPSS** (Exploit Prediction Scoring System)، أي نظام تقييم التنبؤ بالاستغلال، الصادر أيضًا عن FIRST (also from FIRST)، يقدّر يوميًا (estimates, daily) احتمالَ (the probability)، من 0 إلى 1، أن تشهد ثغرة CVE منشورة نشاطَ استغلال (that a published CVE will see exploitation activity) خلال الثلاثين يومًا التالية (in the next 30 days). وتحصل معظم ثغرات CVE على درجاتٍ منخفضة جدًا (Most CVEs score very low)؛ والدرجة المرتفعة تستحق الاهتمام (a high score deserves attention) حتى حين تكون درجة CVSS متواضعة (even when CVSS is modest).
- **كتالوج CISA KEV (CISA KEV catalogue)**، أي الثغرات المعروف استغلالها (Known Exploited Vulnerabilities)، يُدرج ثغرات CVE التي توجد أدلةٌ موثوقة على استغلالها فعليًا (lists CVEs with reliable evidence of exploitation in the wild). ويجب على الوكالات المدنية الفيدرالية الأمريكية (US federal civilian agencies) إصلاحها في مواعيد محدّدة (must fix them by set deadlines) بموجب التوجيه التشغيلي الملزم 22-01 (under Binding Operational Directive 22-01)؛ أما للجميع غيرها (for everyone else) فهو قائمةٌ مجانية بعنوان «أصلِح هذا أولًا» (it is a free "fix this first" list).

```python
# Naive: sort the backlog by CVSS base score
backlog.sort(key=lambda v: v.cvss_base, reverse=True)
```

```python
# Better: exploitation and exposure first, then likelihood, then severity in context
def priority(v, asset):
    exploited = v.in_kev or v.seen_exploited    # KEV, or evidence from Najm's own SOC
    epss = v.epss or 0.0                        # findings in your own code have no CVE, so no EPSS
    if exploited and (asset.internet_facing or asset.holds_customer_data):
        return "P0"
    if exploited or v.cross_customer_access or (epss >= 0.10 and asset.internet_facing):
        return "P1"
    if v.cvss_bte >= 9.0 or (v.cvss_bte >= 7.0 and asset.holds_customer_data):
        return "P2"
    if v.cvss_bte >= 4.0:
        return "P3"
    return "P4"
```

العتبات توضيحية (Thresholds are illustrative)؛ ومواعيد نجم النهائية في قسم 🏛️ (Najm's deadlines are in the 🏛️ section). وليس للثغرات في شيفرتك الخاصة (Flaws in your own code)، مثل ثغرة IDOR في بوابة الشركات الصغيرة (the SME Portal IDOR)، أي إدخالٍ في EPSS أو KEV (have no EPSS or KEV entry)، فقيّمها بدرجة CVSS-BTE مع التقدير المهني (so score them with CVSS-BTE plus judgement)، مع التحقق المتقاطع بمنهجية OWASP لتقييم المخاطر (cross-checked with the OWASP Risk Rating Methodology) (1.3)؛ والوصول المؤكَّد بين العملاء (confirmed cross-customer access) يذهب مباشرةً إلى P1 (goes straight to P1).

### 🟡 التعمق أكثر (Going deeper)

**نتائج أقل وأفضل (Fewer, better findings).**
- **أزِل التكرار (Deduplicate).** ثغرة CVE نفسها في 400 صورة حاوية (The same CVE in 400 container images) إصلاحٌ واحد (is one fix): حدِّث الصورة الأساسية (update the base image).
- **قابلية البلوغ (Reachability).** تُبلغ كثيرٌ من أدوات SCA (Many SCA tools report) عمّا إذا كانت شيفرتك تستدعي الدالة المعرَّضة (whether your code calls the vulnerable function). استخدمها للترتيب لا للتجاهل (Use it to sort, not to ignore)؛ فالتحليل قد يكون خاطئًا (the analysis can be wrong).
- **VEX** (Vulnerability Exploitability eXchange) بيانٌ مقروءٌ آليًا (is a machine-readable statement) بأن منتجًا ما غير متأثر أو متأثر أو تم إصلاحه أو قيد التحقيق (that a product is not affected, affected, fixed or under investigation)، مع مبرّر (with a justification) مثل «الشيفرة المعرَّضة ليست في مسار التنفيذ» ("vulnerable code not in execute path"). وينشره المورّدون إلى جانب قوائم مكونات البرمجيات (Suppliers publish it alongside SBOMs)، وتدعمه CycloneDX وOASIS CSAF (CycloneDX and OASIS CSAF support it)، فتُغلق النتائج بالأدلة لا بالجدال (so you close findings with evidence, not argument).
- **SSVC** (Stakeholder-Specific Vulnerability Categorization)، أي تصنيف الثغرات الخاص بأصحاب المصلحة، الصادر عن CERT/CC في جامعة كارنيغي ميلون (from Carnegie Mellon's CERT/CC) والذي كيّفته CISA (and adapted by CISA)، يستبدل بالدرجة شجرةَ قرار (replaces a score with a decision tree) تقوم على حالة الاستغلال (over exploitation status)، وقابلية الأتمتة (automatability)، والأثر التقني (technical impact)، والأثر على المهمة والرفاه (and mission and well-being impact). والناتج إجراءٌ (The outcome is an action) من بين Track وTrack* وAttend وAct، وهذا يلائم العملية أكثر من الرقم (which fits a process better than a number).

**المواعيد النهائية والاستثناءات (Deadlines and exceptions).** الموعد النهائي للمعالجة (A remediation deadline)، ويُسمّى غالبًا اتفاقية مستوى الخدمة (often called an SLA)، هو أقصى وقتٍ لإصلاح نتيجةٍ من كل أولوية (is the maximum time to fix a finding of each priority). ولا يكون موثوقًا إلا مع **عملية استثناءات (exception process)**: يوقّع مالك مخاطر مسمّى (a named risk owner signs) قبولًا محدّد المدة (a time-limited acceptance) مع ضوابط تعويضية (with compensating controls)، ويُدوَّن في سجل المخاطر (recorded in the risk register). وأبلِغ عن التعرّض لثغرات KEV (Report KEV exposure)، أي ثغرات KEV المفتوحة على الأنظمة المكشوفة للإنترنت (KEV-listed flaws open on internet-facing systems)، والهدف صفر (target zero)، وعن تغطية الفحص للجرد (and scan coverage of the inventory)، إلى جانب الالتزام بالمواعيد النهائية (alongside deadline compliance).

**الإفصاح المنسَّق عن الثغرات (Coordinated vulnerability disclosure, CVD).** يُبلغ المكتشف بشكلٍ خاص (The finder reports privately)، ويُصلح المالك (the owner fixes)، وتُنشر التفاصيل، إن نُشرت أصلًا (and details are published, if at all)، بعد أن يصبح المستخدمون محميين (once users are protected). ويصف معياران من ISO جانب المالك (Two ISO standards describe the owner's side): **ISO/IEC 29147**، أي تلقّي البلاغات ونشر التنبيهات الأمنية (receiving reports and publishing advisories)، و**ISO/IEC 30111**، أي عملية المعالجة الداخلية من البلاغ إلى الإصلاح (the internal handling process from report to fix). ويعمل كثيرٌ من الباحثين وفق مهلةٍ افتراضية (Many researchers work to a default deadline)، مثل مهلة الـ90 يومًا التي روّج لها Google Project Zero (such as the 90 days popularised by Google Project Zero)؛ واتفق على التمديدات (agree extensions) حين يكون هناك تقدّمٌ حقيقي (when there is real progress).

**سياسة الإفصاح عن الثغرات (vulnerability disclosure policy, VDP)** هي الوعد العلني (is the public promise) الذي يجعل الإفصاح المنسَّق يعمل (that makes CVD work). وهي تحدّد (It sets out):
- **النطاق (Scope)**: أيّ الأنظمة داخله (which systems are in)، وما الخارج عنه (and what is out).
- **كيفية الإبلاغ (How to report)**: عنوانٌ أو نموذجٌ مراقَب (a monitored address or form)، ويفضَّل مع خيارٍ للتشفير (ideally with an encryption option).
- **القواعد (Rules)**: حساباتك الخاصة فقط (own accounts only)؛ وإذا بلغتَ بيانات أشخاصٍ آخرين (if you reach other people's data)، فتوقّف (stop)، ولا تحتفظ بشيء (keep nothing)، وأبلِغ عن ذلك (and report it)؛ ولا حجب للخدمة ولا هندسة اجتماعية ولا هجمات مادية (no denial of service, social engineering or physical attacks).
- **الملاذ الآمن (Safe harbour)**: لا إجراءات قانونية ضد البحث بحسن نية ضمن السياسة (no legal action against good-faith research within the policy)، بصياغة الفريق القانوني (worded by legal).
- **ما يمكن أن يتوقعه المُبلِّغون (What reporters can expect)**: أوقات الاستجابة (response times)، والتحديثات (updates)، ونسبة الفضل إليهم (and credit).

ألزم التوجيه التشغيلي الملزم 20-01 من CISA (CISA's Binding Operational Directive 20-01) الوكالاتِ الفيدرالية الأمريكية بنشر سياسات إفصاح (required US federal agencies to publish VDPs)، وهو نموذجٌ عام مفيد (and is a useful public model)؛ وتغطي ورقة OWASP المختصرة للإفصاح عن الثغرات (the OWASP Vulnerability Disclosure Cheat Sheet) كلا الجانبين (covers both sides).

**security.txt.** يعرّف RFC 9116 (2022) ملفًا نصيًا عاديًا (defines a plain-text file) في المسار `/.well-known/security.txt` (at /.well-known/security.txt) يخبر الباحثين كيف يصلون إليك (telling researchers how to reach you). والحقلان `Contact` و`Expires` إلزاميان (Contact and Expires are required)؛ ويوصي الـRFC بتاريخ انتهاءٍ في غضون أقل من عام (the RFC recommends an expiry under a year ahead)، كي يُراجَع الملف (so the file gets reviewed):

```text
Contact: mailto:security@najmbank.example
Contact: https://najmbank.example/security/report
Expires: 2027-09-30T20:59:00.000Z
Encryption: https://najmbank.example/.well-known/security-key.asc
Policy: https://najmbank.example/security/disclosure-policy
Acknowledgments: https://najmbank.example/security/thanks
Preferred-Languages: en, ar
Canonical: https://najmbank.example/.well-known/security.txt
```

(النطاق `.example` محجوزٌ للتوثيق (.example is reserved for documentation)؛ وبنك نجم خيالي (Najm Bank is fictional).)

**التعامل الجيد مع البلاغ (Handling a report well).** أقِرّ بالاستلام خلال بضعة أيام عمل (Acknowledge within a few working days) من شخصٍ مسمّى (from a named person)؛ وأعِد إنتاج الثغرة وقيّمها (reproduce and rate it)؛ وأبقِ المُبلِّغ على اطلاع (keep the reporter updated)؛ وأصلِح وتحقّق (fix and verify)؛ وانسب الفضل إليه بموافقته (credit with consent)؛ وانشر تنبيهًا أمنيًا (publish an advisory) إذا كان على آخرين أن يتصرفوا (if others must act). ولا تهدّد أبدًا مُبلِّغًا حسن النية (Never threaten a good-faith reporter): فهذا يوقف البلاغات لا الثغرات (it stops the reports, not the bugs).

### 🔴 نظرة الخبير (Expert view)

**برامج مكافآت الثغرات (Bug bounties).** **برنامج مكافآت الثغرات (bug bounty programme)** يدفع مكافآتٍ عن النتائج الصحيحة الواقعة ضمن النطاق (pays rewards for valid, in-scope findings)، عادةً عبر منصةٍ (usually through a platform) تتولى هوية الباحثين والدفع والفرز الأولي (that handles researcher identity, payment and first-line triage). ويضاعف برنامج المكافآت البلاغات الواردة (A bounty multiplies inbound reports)، لذا اجعل الأساسيات تعمل أولًا (so first get the basics working): الجرد (inventory)، وسياسة إفصاحٍ تعاملت مع بلاغاتٍ حقيقية (a VDP that has handled real reports)، وموظفو فرز (triage staff)، ومواعيد نهائية مُلتزَمٌ بها (and met deadlines). ابدأ **خاصًا (private)**، أي بباحثين مدعوّين ونطاقٍ ضيق (invited researchers, narrow scope)، ثم وسّع (then widen). ونقاط التصميم (Design points):
- **حدّد النطاق (Scope)** بدقة (precisely)، مع بيئة اختبار وحسابات اختبار (with a test environment and test accounts)، كي لا يمسّ أحدٌ أموال العملاء الحقيقيين أو بياناتهم (so nobody touches real customers' money or data).
- **المكافآت (Rewards)** بحسب الخطورة (by severity)، منشورةٌ مسبقًا (published in advance)، مع قاعدةٍ للتكرارات (with a rule for duplicates)، إذ يفوز عادةً أول بلاغٍ صحيح (usually the first valid report wins).
- **قواعد الاشتباك (Rules of engagement)** كما في سياسة الإفصاح (as in the VDP)، إضافةً إلى حدود المعدّل (plus rate limits) وترويسةٍ تعريفية (and an identifying header) كي يتعرّف مركز العمليات الأمنية على حركة البحث (so the SOC recognises research traffic).
- **قدرة الفرز (Triage capacity)**: الاستجابات البطيئة تُفقدك الباحثين الجيدين (slow responses lose good researchers).

**نتائج الذكاء الاصطناعي (AI findings).** قرّر مسبقًا (Decide in advance) ما الذي يُعدّ ثغرةً أمنية (what counts as a security vulnerability) في نجم أسيست ومساعد مذكرات الائتمان (in Najm Assist and the copilot):

| البلاغ (Report) | يُعامَل بوصفه (Treat as) |
|---|---|
| يتصرّف في حساب عميلٍ آخر (Acts on another customer's account)، أو يتخطّى تأكيدًا مطلوبًا (or skips a required confirmation) | ثغرةٌ أمنية، عالية أو حرجة (Security vulnerability, high or critical) (LLM06؛ 3.3) |
| يكشف بيانات عميلٍ آخر (Reveals another customer's data)، أو أسرارًا من سياقه (or secrets from its context) | ثغرةٌ أمنية (Security vulnerability) (LLM02، LLM07) |
| محتوى يستطيع طرفٌ خارجي زرعه (Outsider-plantable content) يُطلق حقنًا غير مباشر بأثرٍ حقيقي (triggers indirect injection with real impact) | ثغرةٌ أمنية (Security vulnerability) (LLM01) |
| كسر قيودٍ ينتج نصًا وقحًا (Jailbreak producing rude text)، دون أثرٍ على البيانات أو الإجراءات (with no data or action impact) | ليس خللًا أمنيًا (Not a security bug): يُحال إلى قناة سلامة الذكاء الاصطناعي (route to the AI safety channel)، أي فريق ليلى (Layla's team) |
| اقتباس رسومٍ خاطئة (Wrong fee quoted) | مشكلة جودة لفريق رانيا (Quality issue for Rania's team)؛ وحادثة (an incident) (10.2) إذا تضرّر العملاء (if customers were harmed) |

لا يوجد لحقن الموجّهات إصلاحٌ تقني كامل وقت كتابة هذا النص (Prompt injection has no complete technical fix at the time of writing) (8.2)، ولذا لا يمكن «ترقيع» بعض نتائج الذكاء الاصطناعي (so some AI findings cannot be "patched"). تتبّعها بوصفها مخاطر (Track them as risks) مع ضوابط تعويضية (with compensating controls)، أي أدواتٍ أضيق وتأكيداتٍ ومعالجةٍ للمخرجات (narrower tools, confirmations, output handling) (9.1، 9.2)، وأضِف الهجوم إلى مجموعة اختبارات الانحدار للفريق الأحمر للذكاء الاصطناعي (add the attack to the AI red-team regression suite) (9.4)، وأعِد الاختبار مع كل تغييرٍ في النموذج أو الموجّه (and re-test on every model or prompt change). أما «لن يُصلَح» ("Won't fix") فيرمي تلك المعرفة جانبًا (throws that knowledge away).

**مكوّنات الذكاء الاصطناعي أصولٌ أيضًا (AI components are assets too).** أدرِج في الجرد النماذج ومجموعات البيانات والموجّهات وموصلات الأدوات (Inventory models, datasets, prompts and tool connectors)، إذ تستطيع CycloneDX وصف مكونات تعلّم الآلة (CycloneDX can describe ML components). وتتبّع ثغرات أطر تعلّم الآلة كأي اعتمادية (Track ML framework vulnerabilities like any dependency)، وعامِل ملفات النماذج معاملة الشيفرة (treat model files as code): فبعض الصيغ (some formats)، مثل pickle في Python (such as Python pickle)، قد تنفّذ شيفرةً عند تحميلها (can execute code when loaded) (2.3)، لذا فضّل صيغًا مثل safetensors (so prefer formats such as safetensors). وقد يعيد تغييرُ النموذج فتحَ نتيجةٍ مغلقة (A model change can reopen a closed finding)، فأعِد تشغيل التقييم الأمني (so re-run the security evaluation).

**حين تكون نجم هي المُبلِّغة (When Najm is the reporter).** في الثغرات الموجودة في منتجات المورّدين (For flaws in vendors' products)، استخدم جهة الاتصال الأمنية لدى المورّد (use the vendor's security contact) أو ملف `security.txt` الخاص به (or security.txt)؛ وإذا لم يستجب (if it does not respond)، فبوسع جهة تنسيقٍ (a coordinator) مثل CERT/CC أو فريق CERT وطني (such as CERT/CC or a national CERT) أن تساعد (can help).

**المقاييس (Metrics).** لا يكفي «عدد الثغرات المكتشفة» وحده (Not "vulnerabilities found" alone): بل وقت المعالجة بحسب الأولوية (time to remediate by priority)، والالتزام بالمواعيد النهائية (deadline compliance)، ونافذة التعرّض لثغرات KEV (KEV exposure window)، والنتائج المتكررة بحسب CWE (repeat findings by CWE)، التي تشير إلى احتياجات التدريب (pointing to training needs) (6.1)، ونسبة ما يُكتشف داخليًا (and the share found internally)؛ فإذا كان الخارجيون يجدون معظم الثغرات (if outsiders find most bugs)، فالاختبار الداخلي ضعيف (internal testing is weak).

## 🧰 الأدوات (The toolkit)
| الضابط أو المعيار أو الأداة (Control, standard or tool) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **CVSS** (FIRST; v4.0) — نظام تقييم الثغرات الشائع | تقييم الخطورة بمقاييس أساسية وتهديد وبيئية وتكميلية (Severity scoring with Base, Threat, Environmental and Supplemental metrics) | خطورةٌ متّسقة (Consistent severity)؛ وسياقك عبر CVSS-BTE (your context via CVSS-BTE) |
| **EPSS** (FIRST) — نظام تقييم التنبؤ بالاستغلال | تقديرٌ يومي لاحتمال استغلال ثغرة CVE خلال الثلاثين يومًا التالية (Daily estimate of the probability that a CVE is exploited in the next 30 days) | ترتيب قائمةٍ كبيرة من ثغرات CVE المتراكمة بحسب الاحتمال (Ranking a large CVE backlog by likelihood) |
| **CISA KEV catalogue** — كتالوج الثغرات المعروف استغلالها | قائمةٌ بثغرات CVE التي توجد أدلةٌ على استغلالها فعليًا (List of CVEs with evidence of exploitation in the wild) | قائمة «أصلِح أولًا» (Fix-first list)؛ وأولويةٌ قصوى على الأنظمة المكشوفة للإنترنت (top priority on internet-facing systems) |
| **SSVC** (CERT/CC, CISA) — تصنيف الثغرات الخاص بأصحاب المصلحة | شجرة قرارٍ تحوّل الاستغلال وقابلية الأتمتة والأثر إلى إجراء (Decision tree that turns exploitation, automatability and impact into an action) | قرارات ترتيب أولوياتٍ قابلة للتفسير (Explainable prioritisation decisions) |
| **VEX** — تبادل قابلية استغلال الثغرات | بيانٌ مقروءٌ آليًا (Machine-readable statement) بما إذا كان منتجٌ ما متأثرًا بثغرة (of whether a product is affected by a vulnerability) | إغلاق النتائج المستندة إلى قوائم مكونات البرمجيات بأدلة المورّد (Closing SBOM-driven findings with supplier evidence) |
| **security.txt** (RFC 9116) — ملف جهة الاتصال الأمنية | ملفٌ قياسي يخبر الباحثين كيف يُبلغون عن الثغرات (Standard file telling researchers how to report vulnerabilities) | كل نطاقٍ عام تملكه (Every public domain you own) |
| **ISO/IEC 29147 and ISO/IEC 30111** — معيارا الإفصاح والمعالجة | معايير للإفصاح عن الثغرات والمعالجة الداخلية (Standards for vulnerability disclosure and internal handling) | تصميم سياسة إفصاحٍ وعملية معالجة أو تدقيقهما (Designing or auditing a VDP and handling process) |
| **Bug bounty programme** — برنامج مكافآت الثغرات | مكافآتٌ للنتائج الصحيحة الواقعة ضمن النطاق (Rewards for valid, in-scope findings)، عادةً عبر منصة (usually via a platform) | بعد أن تعمل سياسة الإفصاح والإصلاح (After the VDP and fixing work)؛ وابدأ خاصًا (start private) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
تكتب نورة **معيار إدارة الثغرات في بنك نجم، الإصدار 1 (Najm Bank Vulnerability Management Standard v1)**، الذي يحلّ محلّ معيار ترتيب الأولويات من الدرس 1.3 (which replaces the prioritisation standard from 1.3)، وأولَ سياسة إفصاحٍ للبنك (and the bank's first VDP)؛ ويوقّع حمد كليهما (Hamad signs both)، ويصوغ الفريق القانوني الملاذ الآمن (and legal words the safe harbour). والمواعيد النهائية توضيحية (Deadlines are illustrative).

**الجزء أ: الأولويات والمواعيد النهائية (Part A: priorities and deadlines)**

| الأولوية (Priority) | القاعدة (Rule) | التخفيف بحلول (Mitigate by) | الإصلاح بحلول (Fix by) | من يجوز له قبول المخاطر (Who may accept the risk) |
|---|---|---|---|---|
| P0 | مُدرجة في KEV أو شوهد استغلالها (KEV-listed or seen exploited)، على نظامٍ مكشوف للإنترنت أو يحوي بيانات العملاء (on an internet-facing or customer-data system) | 72 ساعة (72 hours) | 7 أيام (7 days) | كبير مسؤولي أمن المعلومات فقط (CISO only)، لمدة 14 يومًا كحدٍّ أقصى (at most 14 days) |
| P1 | مُدرجة في KEV في مكانٍ آخر (KEV-listed elsewhere)؛ أو EPSS ≥ 0.10 على نظامٍ مكشوف للإنترنت (EPSS ≥ 0.10 on internet-facing)؛ أو وصولٌ مؤكَّد بين العملاء في شيفرتنا الخاصة (confirmed cross-customer access in own code) | 7 أيام (7 days) | 14 يومًا (14 days) | كبير مسؤولي أمن المعلومات (CISO) |
| P2 | CVSS-BTE ≥ 9.0، أو ≥ 7.0 على نظامٍ يحوي بيانات العملاء (or ≥ 7.0 on a customer-data system) | — | 30 يومًا (30 days) | رئيسة أمن التطبيقات مع مالك النظام (Head of AppSec with system owner) |
| P3 | النتائج الأخرى ذات CVSS-BTE ≥ 4.0 (Other findings with CVSS-BTE ≥ 4.0) | — | 90 يومًا (90 days) | مالك النظام (System owner) |
| P4 | منخفضة (Low) | — | الترقية المخطّطة التالية (Next planned upgrade) | مالك النظام (System owner) |

تحتاج الاستثناءات إلى مالك (Exceptions need an owner)، وضوابط تعويضية (compensating controls)، وتاريخ انتهاءٍ لا يتجاوز 90 يومًا (and an expiry of at most 90 days). ونتائج الذكاء الاصطناعي التي لا إصلاح كاملًا لها (AI findings without a complete fix) تصبح مخاطر مع ضوابط تعويضية واختبار انحدار (become risks with compensating controls and a regression test). ويتلقى حمد تقريرًا شهريًا (Hamad gets a monthly report): الالتزام بالمواعيد النهائية (deadline compliance)، والتعرّض لثغرات KEV (KEV exposure)، وأقدم نتائج P0 وP1 المفتوحة (oldest open P0 and P1)، وأنواع CWE المتكررة (repeat CWEs).

**الجزء ب: سياسة الإفصاح عن الثغرات (Part B: VDP)، مقتطف (excerpt)**

> **النطاق (Scope).** تطبيق نجم للهاتف وواجهة برمجته العامة (Najm Mobile and its public API)، وبوابة الشركات الصغيرة (the SME Portal)، ونجم أسيست (Najm Assist)، ومواقع najmbank.example (najmbank.example websites). وخارج النطاق (Out of scope): حجب الخدمة (denial of service)، والهندسة الاجتماعية (social engineering)، والهجمات المادية (physical attacks)، وخدمات الأطراف الثالثة التي لا نشغّلها (and third-party services we do not operate).
>
> **الاختبار (Testing).** استخدم حساباتك أو حسابات الاختبار لدينا فقط (Use only your own or our test accounts). وإذا بلغتَ بيانات شخصٍ آخر (If you reach another person's data)، فتوقّف (stop)، ولا تحتفظ بشيء (keep nothing)، وأخبرنا بما رأيت (and tell us what you saw). وابقَ دون 5 طلباتٍ آلية في الثانية (Stay under 5 automated requests per second) وأرسل الترويسة التي ننشرها (and send the header we publish).
>
> **وعدنا (Our promise).** نُقرّ باستلام البلاغات خلال يومَي عمل (We acknowledge reports within 2 working days)، ونقدّم تقييمًا أوليًا خلال 10 أيام (give a first assessment within 10)، ونُبقيك على اطلاع حتى الإصلاح (and update you until the fix). وإذا تصرّفت بحسن نية بموجب هذه السياسة (If you act in good faith under this policy)، فلن نتخذ إجراءً قانونيًا ضدك (we will not take legal action against you). وننسب الفضل للباحثين الذين يرغبون في ذلك (We credit researchers who wish it). ونرحّب بالبلاغات بالعربية أو الإنجليزية (Reports are welcome in Arabic or English).

**الجزء ج: بلاغ بوابة الشركات الصغيرة، مُعادًا تمثيله (Part C: the SME Portal report, replayed).** اليوم 0 (Day 0): الإقرار بالاستلام مع الشكر (acknowledged with thanks). اليوم 1 (Day 1): أُعيد إنتاجه في بيئة التجهيز (reproduced in staging)، وصُنّف P1 (rated P1). اليوم 5 (Day 5): نُشر فحص الملكية واختبار الانحدار (ownership check and regression test deployed)؛ وبُحث في السجلات عن إساءة استخدامٍ أخرى (logs searched for other abuse)؛ وأُبلغت الشركات المتأثرة بناءً على تقييم سارة (affected companies informed on Sara's assessment)؛ ونُسب الفضل للباحثة بموافقتها (researcher credited with consent).

## 🛠️ التمارين (Exercises)
- 🟢 اكتب ملف `security.txt` وسياسة إفصاحٍ في صفحةٍ واحدة (Write a security.txt and a one-page VDP) لموقعٍ تملكه (for a site you own)، أو لموقعٍ خيالي على نطاق `.example` (or a fictional one on a .example domain). *يكتمل عندما (Done when):* يكون الحقلان `Contact` و`Expires` موجودين (Contact and Expires are present) بتاريخ انتهاءٍ في غضون أقل من عام (with an expiry under a year ahead)، وتغطي السياسة (and the VDP covers) النطاق (scope)، وكيفية الإبلاغ (how to report)، وقواعد الاختبار (testing rules)، والملاذ الآمن (safe harbour)، موسومًا بعبارة «للمراجعة القانونية» (marked "for legal review")، وأوقات الاستجابة (and response times).
- 🟡 شغّل ماسح SCA أو ماسح حاويات (Run an SCA or container scanner) على مشروعٍ تملكه (on a project you own). أضِف درجة EPSS وحالة KEV لكل ثغرة CVE (Add each CVE's EPSS score and KEV status)، وكلاهما متاحٌ للتنزيل مجانًا (both free downloads)، ثم طبّق دالة الأولوية في هذا الدرس (then apply this lesson's priority function). *يكتمل عندما (Done when):* تُجمَّع التكرارات في إصلاحات (duplicates are grouped into fixes)، وتُرتَّب القائمة (the list is ranked)، وتستطيع أن تشرح في جملةٍ واحدة (and you can explain in one sentence) لماذا تتقدّم البنود الثلاثة الأولى على أعلى درجة CVSS أساسية (why the top three outrank the highest CVSS base score).
- 🔴 صمّم تجربةً أولية لبرنامج مكافآت ثغراتٍ خاص (Design a private bug-bounty pilot) لنظامٍ تملكه أو لنجم أسيست (for a system you own or for Najm Assist): النطاق (scope)، وبيئة الاختبار (test environment)، وقواعد الاشتباك (rules of engagement)، والمكافآت (rewards)، وتصنيف نتائج الذكاء الاصطناعي (AI finding classification)، وتوفير موظفي الفرز (and triage staffing). *يكتمل عندما (Done when):* يستطيع زميلٌ يؤدي دور باحث (a colleague playing a researcher) أن يعرف من وثيقتك (can tell from your document) ما إذا كانت ثلاثة بلاغاتٍ نموذجية (whether three sample reports)، وهي ثغرة IDOR (an IDOR)، وكسر قيودٍ وقح (a rude jailbreak)، وحقنٌ غير مباشر يُطلق أداة (an indirect injection that triggers a tool)، ضمن النطاق (are in scope)، وكم يستحق كلٌّ منها تقريبًا (and roughly what each would earn).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **الترتيب حسب درجة CVSS الأساسية وحدها (Sorting by CVSS base score alone).** أضِف أدلة الاستغلال (Add exploitation evidence) (KEV)، والاحتمال (likelihood) (EPSS)، وسياقك (and your context).
- **غياب الجرد (No inventory).** الأصول غير المعروفة لا تُفحص أبدًا (Unknown assets are never scanned). أبلِغ عن تغطية الفحص مقابل الجرد (Report scan coverage against the inventory).
- **قبول المخاطر دون تاريخ انتهاء (Risk acceptance without expiry).** يصبح «المقبول» «منسيًا» ("Accepted" becomes "forgotten"). اشترط مالكًا وضوابط تعويضية وتاريخ انتهاء (Require an owner, compensating controls and an end date).
- **صندوق بريدٍ عام قناةً للإفصاح (A general inbox as the disclosure channel).** انشر ملف `security.txt` وسياسة إفصاح (Publish security.txt and a VDP) مع استقبالٍ مراقَب ومُدارٍ بالتذاكر (with a monitored, ticketed intake) وأهدافٍ لأوقات الاستجابة (and response targets).
- **تهديد الباحثين حسني النية (Threatening good-faith researchers).** قدّم ملاذًا آمنًا (Offer safe harbour) وأبقِهم على اطلاع (and keep them updated).
- **برنامج مكافآتٍ عام قبل أن تكون قادرًا على الإصلاح (A public bounty before you can fix).** ابدأ بسياسة إفصاح (Start with a VDP)، ثم ببرنامج مكافآتٍ خاص (then a private bounty)، ثم توسّع مع نمو القدرة (and grow with capacity).

## 🧾 الخلاصة (Recap)
- إدارة الثغرات دورةٌ قائمة على جرد الأصول (Vulnerability management is a cycle on an asset inventory): الإيجاد (find)، والفرز (triage)، وترتيب الأولويات (prioritise)، والإصلاح أو التخفيف (fix or mitigate)، والتحقق (verify)، والقبول فقط مع مالكٍ وتاريخ انتهاء (and accept only with an owner and expiry).
- تجمع الأولوية بين أدلة الاستغلال (Priority combines exploitation evidence) (KEV)، والاحتمال (likelihood) (EPSS)، والخطورة في السياق (severity in context) (CVSS-BTE)، والتعرّض (and exposure)؛ ويجعل SSVC وVEX القرارات قابلةً للتفسير (SSVC and VEX make decisions explainable).
- يحتاج الإفصاح المنسَّق (Coordinated disclosure needs) إلى سياسة إفصاحٍ تتضمن النطاق والقواعد والملاذ الآمن (a VDP with scope, rules and safe harbour)، وقناةٍ مراقَبة (a monitored channel)، وملف `security.txt` (RFC 9116).
- تأتي برامج مكافآت الثغرات بعد الأساسيات (Bug bounties come after the basics)، وتبدأ خاصة (start private)، وتحتاج إلى بيئة اختبار وموظفي فرز (and need a test environment and triage staff).
- حدّد أيّ نتائج الذكاء الاصطناعي تُعدّ خللًا أمنيًا (Define which AI findings are security bugs)؛ وتتبّع حقن الموجّهات بوصفه خطرًا (track prompt injection as a risk) مع ضوابط تعويضية واختبارات انحدار (with compensating controls and regression tests).

## ✍️ اختبر نفسك (Check yourself)

**1. تُبلغ ماسحات نجم عن نتيجتين (Najm's scanners report two findings). X: درجة CVSS الأساسية 9.8 (CVSS 9.8 base)، في أداةٍ داخلية لا يمكن بلوغها إلا من شبكةٍ إدارية (in an internal tool reachable only from an admin network)، ودرجة EPSS منخفضة جدًا (very low EPSS)، وليست في KEV (not in KEV). Y: درجة CVSS الأساسية 7.5 (CVSS 7.5 base)، في بوابة واجهات البرمجة المكشوفة للإنترنت (in the internet-facing API gateway)، ومُدرجة في كتالوج CISA KEV (in the CISA KEV catalogue). أيّهما يأتي أولًا (Which comes first)؟**

- A. X، لأن درجة CVSS الخاصة بها أعلى (X, because its CVSS score is higher)
- B. Y، لأنها معروفٌ استغلالها ومكشوفةٌ للإنترنت (Y, because it is known to be exploited and is exposed to the internet)
- C. كلتاهما معًا، بالترتيب الأبجدي (Both together, in alphabetical order)
- D. لا هذه ولا تلك، حتى يؤكدهما اختبار اختراق (Neither, until a penetration test confirms them)

<details><summary>الإجابة</summary>

**B.** الاستغلال المعروف على نظامٍ مكشوف (Known exploitation on an exposed system) هو مستوى P0 لدى نجم (is Najm's P0). أما A فيعامل الخطورة على أنها أولوية (treats severity as priority)؛ وD يؤخّر ثغرةً معروفًا استغلالها (delays a known-exploited flaw). ولا تزال X تُصلَح ضمن موعدها النهائي الخاص (X is still fixed within its own deadline). انظر: 🟢 الأساسيات (The essentials).

</details>

**2. تكتب باحثةٌ في رسالة بريد (A researcher emails) أنها استطاعت رؤية فواتير شركةٍ أخرى في بوابة الشركات الصغيرة (she could see another company's invoices in the SME Portal) بتغيير معرّفٍ في طلبٍ من حسابها الخاص (by changing an ID in her own account's request). ما أفضل ردٍّ أول (What is the best first response)؟**

- A. تجاهلها، لأنها لم تكن مخوّلةً بالاختبار (Ignore it, because she was not authorised to test)
- B. حذّرها من أن البنك قد يتخذ إجراءً قانونيًا (Warn her that the bank may take legal action)
- C. أقِرّ بالاستلام سريعًا (Acknowledge quickly)، واشكرها (thank her)، واطلب التفاصيل وتأكيدًا بأنها لم تحتفظ بأي بيانات (ask for details and confirmation that she has not kept any data)، وافرزها بوصفها خللًا مرجّحًا عالي الأولوية في التحكم في الوصول (triage it as a likely high-priority access-control flaw)، وأبقِها على اطلاع (and keep her updated)
- D. لا تردّ إلا بعد نشر الإصلاح (Reply only once the fix is deployed)

<details><summary>الإجابة</summary>

**C.** هذا إفصاحٌ منسَّق جيد (That is good coordinated disclosure). أما A وD فيتركان الثغرة مفتوحة (leave the flaw open) ويدفعانها إلى النشر العلني (and push her to go public)؛ وB يوقف البلاغات لا الثغرة (stops reports, not the bug). انظر: 🟡 التعمق أكثر (Going deeper).

</details>

**3. أيّ عبارةٍ عن `security.txt` صحيحة (Which statement about security.txt is correct)؟**

- A. يقع في المسار `/.well-known/security.txt` (It sits at /.well-known/security.txt) ويجب أن يتضمن الحقلين `Contact` و`Expires` (and must include Contact and Expires fields)
- B. يُدرج الثغرات المعروفة لدى المؤسسة (It lists the organisation's known vulnerabilities)
- C. يحلّ محلّ سياسة الإفصاح (It replaces a disclosure policy)
- D. ينبغي إخفاؤه عن العامة (It should be hidden from the public)

<details><summary>الإجابة</summary>

**A.** يحدّد RFC 9116 الموقع والحقلين الإلزاميين (defines the location and the two required fields). وهو يشير إلى سياسة (It points to a policy)، فـC خاطئ (C is wrong)، ومقصودٌ أن يكون علنيًا (and is meant to be public)، فـD خاطئ (D is wrong). انظر: 🟡 التعمق أكثر (Going deeper).

</details>

**4. يسأل طارق عمّا إذا كان ينبغي لنجم إطلاق برنامج مكافآت ثغراتٍ عام الشهر المقبل (Tariq asks whether Najm should launch a public bug bounty next month). ليس لدى البنك سياسة إفصاح (The bank has no VDP)، وتغطي الفحوص 60% من الأصول (scans cover 60% of assets)، و400 نتيجة تجاوزت موعدها النهائي (and 400 findings are past their deadline). بمَ ينبغي أن توصي نورة (What should Noura recommend)؟**

- A. الإطلاق العلني للحصول على أكبر عددٍ من النتائج (Launch publicly to get the most findings)
- B. عدم تشغيل برنامج مكافآت ثغراتٍ في مصرفٍ أبدًا (Never run a bug bounty in a bank)
- C. إصلاح الأساسيات أولًا (Fix the basics first)، أي سياسة الإفصاح والجرد وتغطية الفحص والالتزام بالمواعيد النهائية (a VDP, inventory and scan coverage, meeting deadlines)، ثم تشغيل برنامج مكافآتٍ خاص بنطاقٍ ضيق وبيئة اختبار (then run a private bounty with narrow scope and a test environment)
- D. تشغيل البرنامج دون دفع مكافآت (Run the bounty without paying rewards)

<details><summary>الإجابة</summary>

**C.** يضاعف برنامج المكافآت البلاغات الواردة (A bounty multiplies inbound reports)؛ ومن دون قدرةٍ على الفرز والإصلاح (without triage and fixing capacity) فإنه يضيف كلفةً وإحباطًا (it adds cost and frustration). أما B فمطلقٌ أكثر مما ينبغي (is too absolute)؛ وD ليس برنامج مكافآت (is not a bounty). انظر: 🔴 نظرة الخبير (Expert view).

</details>

**5. يجعل أحد الباحثين نجم أسيست يكتب قصيدةً وقحة عن البنك (One researcher makes Najm Assist write a rude poem about the bank). ويُظهر آخر (Another shows) أن نصًا في نموذج اعتراض (that text in a dispute form) يمكن أن يجعله يستدعي أداةً على بطاقة عميلٍ آخر (can make it call a tool on another customer's card). كيف ينبغي أن تعاملهما سياسة الإفصاح (How should the VDP treat them)؟**

- A. كلاهما ثغرتان أمنيتان حرجتان (Both as critical security vulnerabilities)
- B. كلاهما خارج النطاق (Both as out of scope)، لأن سلوك الذكاء الاصطناعي ليس من الأمن (because AI behaviour is not security)
- C. الثاني ثغرةٌ أمنية بأثرٍ يمتد بين العملاء (The second as a security vulnerability with cross-customer impact)؛ والأول بلاغ جودةٍ غير أمني لقناة سلامة الذكاء الاصطناعي (the first as a non-security quality report for the AI safety channel)
- D. الأول حرج، لأنه يضرّ بالعلامة التجارية (The first as critical, because it harms the brand)

<details><summary>الإجابة</summary>

**C.** الأثر الأمني (Security impact)، أي إجراءٌ غير مصرّح به على حساب عميلٍ آخر (an unauthorised action on another customer's account)، يجعل الثاني ثغرةً (makes the second a vulnerability)؛ أما الأول فلا أثر له على البيانات أو الإجراءات (the first has no data or action impact). ويضخّم A وD الخطورة (A and D inflate severity)؛ ويُغفل B ثغرات الذكاء الاصطناعي الحقيقية (B misses real AI vulnerabilities). انظر: 🔴 نظرة الخبير (Expert view).

</details>

## 📚 المراجع (References)
- FIRST، نظام تقييم الثغرات الشائع، الإصدار 4.0 (Common Vulnerability Scoring System v4.0) — https://www.first.org/cvss/
- FIRST، نظام تقييم التنبؤ بالاستغلال (Exploit Prediction Scoring System, EPSS) — https://www.first.org/epss/
- CISA، كتالوج الثغرات المعروف استغلالها (Known Exploited Vulnerabilities Catalog) — https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- CISA، تصنيف الثغرات الخاص بأصحاب المصلحة (Stakeholder-Specific Vulnerability Categorization, SSVC) — https://www.cisa.gov/stakeholder-specific-vulnerability-categorization-ssvc
- برنامج CVE (CVE Program) — https://www.cve.org/
- CWE-639، تجاوز التفويض عبر مفتاحٍ يتحكم فيه المستخدم (Authorization Bypass Through User-Controlled Key) — https://cwe.mitre.org/data/definitions/639.html
- RFC 9116، صيغة ملفٍ للمساعدة في الإفصاح عن الثغرات الأمنية (A File Format to Aid in Security Vulnerability Disclosure) — https://www.rfc-editor.org/rfc/rfc9116
- ورقة OWASP المختصرة للإفصاح عن الثغرات (OWASP Vulnerability Disclosure Cheat Sheet) — https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html
- ISO/IEC 29147 وISO/IEC 30111، وتحقّق من الإصدارات الحالية (check the current editions) — https://www.iso.org/
- CycloneDX — https://cyclonedx.org/
