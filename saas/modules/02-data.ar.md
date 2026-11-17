# الوحدة 2 (Module 2) — البيانات

*كل SaaS هو في جوهره، تحت واجهة المستخدم (UI)، آلة دقيقة تخزّن بيانات الآخرين ولا تعيدها إلا للأشخاص المخوّلين. تغطي هذه الوحدة (module) أربعة مكوّنات للبيانات (data components) ستبنيها في كل مشروع: قاعدة البيانات العلائقية (relational database) نفسها، والملفات التي لا مكان لها فيها، والبحث (search) في الاثنين، وحدود المستأجر (tenant boundary) التي تبقي بيانات عميل بعيدة عن عميل آخر. إن أتقنت هذه المكوّنات (components) مبكرًا صارت أغلب الوحدات اللاحقة (later modules) أسهل، وإن أخطأت فيها ورثت كل وحدة لاحقة (later module) تلك الفوضى.*

> **التطبيق العملي (Practice):** ابدأ من [نسخة البداية (starter) من Beacon](https://github.com/Tamoura/system-design-for-vibe-coders/tree/beacon/starter)، وحلّ التمارين قبل النظر إلى [الحل المرجعي (reference solution) لهذه الوحدة](https://github.com/Tamoura/system-design-for-vibe-coders/tree/beacon/module-2-solution) (الفرع (branch) `beacon/module-2-solution`).

---

# 2.1 — طبقة البيانات (data layer): Postgres وأدوات ORM (ORMs) والترحيلات (migrations) وبيانات البذر (seed data)
*المستوى (Level): 🟢 مبتدئ (Beginner)* · *المتطلبات (Prerequisites): 1.2*

## ⚡ الدرس في دقيقة (In 60 seconds)

- طبقة البيانات هي قاعدة البيانات العلائقية مع الأدوات المحيطة بها: أداة ORM (ORM) أو باني استعلامات (query builder)، وترحيلات لها إصدارات (versioned migrations)، وسكربتات بذر (seed scripts).
- الخيار الافتراضي للإصدار الأول (v1 default): Postgres مُدار (managed)، وكل جدول يملكه مستأجر (tenant-owned table) فيه `organization_id` و`created_at` و`updated_at` وقيود حقيقية (constraints)، ومعرّفات (ids) مرتبة زمنيًا (time-ordered) ويصعب تخمينها (UUIDv7، مع بادئة (prefix) مثل `mon_` إن شئت).
- القاعدة الأهم: لا تغيّر مخطط الإنتاج (production schema) يدويًا أبدًا. كل تغيير يمر عبر ترحيل (migration)، والتغييرات الخطرة تستخدم أسلوب التوسيع ثم التقليص (expand/contract) كي يعمل الكود القديم والجديد جنبًا إلى جنب.
- اعرف ما يرسله ORM من SQL: استعلامات N+1 (N+1 queries) والفهارس الناقصة (indexes) هي أكثر أسباب بطء لوحات التحكم (dashboard) شيوعًا.
- الفخ الأكبر: أن تفترض أن النسخ الاحتياطية (backups) تعمل. فعّل الاستعادة إلى نقطة زمنية (point-in-time recovery) وتدرّب على الاستعادة (restore)، لأن النسخة التي لم تستعدها يومًا مجرد أمل.

## 🧭 لماذا يحتاجه كل SaaS

يخزّن الإصدار الأول (v1) من Beacon كل شيء في قاعدة بيانات (database) Postgres واحدة. بعد ثلاثة أشهر يشتكي عميل لديه 400 مراقِب (monitors) من أن لوحة التحكم تستغرق تسع ثوانٍ لتظهر. تبحث فتجد أن الصفحة تنفّذ 401 استعلام (query): واحد لقائمة المراقِبات، ثم واحد لكل مراقِب لجلب آخر فحص (check) له. بعد أسبوع تعيد تسمية عمود (column) وتنشر (deploy)، فتفشل كل الطلبات (request) لمدة أربع دقائق لأن الكود القديم ما زال يعمل على المخطط الجديد (new schema). ثم يشغّل أحدهم سكربت تنظيف (cleanup script) على الإنتاج (production) بدلًا من بيئة الاختبار (Staging).

هذه هي الطرق الثلاث الكلاسيكية التي يؤذي بها SaaS ناشئ نفسه: استعلامات بطيئة (slow queries)، وتغييرات غير آمنة (unsafe changes) في المخطط (schema)، وأخطاء لا يمكن التراجع (rollback) عنها. أشهر مثال على الأخيرة: في يناير 2017 فقدت GitLab عدة ساعات من بيانات الإنتاج (production data) بعد أن حذف (delete) مهندس مجلد قاعدة البيانات الخطأ أثناء حادثة (incident)، ثم اكتشفوا أن عدة آليات للنسخ الاحتياطي (backup mechanisms) لديهم لم تكن تعمل. تقرير ما بعد الحادثة (postmortem) الذي نشروه علنًا ما زال يستحق القراءة.

قاعدة البيانات هي المكوّن (component) الوحيد الذي لا تستطيع إعادة كتابته في عطلة نهاية أسبوع. يمكن إعادة نشر (redeploy) الكود، لكن البيانات التي فُقدت أو تلفت أو صُمّمت بشكل سيئ تبقى مفقودة أو تالفة أو سيئة التصميم.

**عامل قاعدة البيانات (database) على أنها ذاكرة المنتج (the product's memory): اختر محركًا (engine) مملًا ومجرّبًا، ولا تغيّره إلا عبر ترحيلات لها إصدارات (versioned migrations)، وتأكد أنك تستطيع استعادته إلى أي دقيقة من الأمس.**

## 📐 كيف يعمل

### 🟢 الأساسيات

**لماذا Postgres هو الخيار الافتراضي (default).** PostgreSQL قاعدة بيانات علائقية: تعيش البيانات في جداول (tables) ذات أعمدة (columns) محددة الأنواع (types)، وتستعلم عنها بلغة SQL (SQL). هو الخيار الافتراضي لأي SaaS جديد لأسباب مملة وجيدة: مفتوح المصدر (open source)، وتقدّمه كل منصة سحابية (cloud platform) بشكل مُدار، ويدعم المعاملات (transactions) الحقيقية، والقيود القوية، وأعمدة JSON (`jsonb`) للأجزاء شبه المنظمة (semi-structured)، والبحث النصي الكامل (full-text search) (الدرس 2.3)، وأمان مستوى الصف (row-level security) (الدرس 2.4)، ومنظومة إضافات (extension ecosystem) (`pgvector` للتضمينات (embeddings)، و`pg_trgm` للمطابقة التقريبية). MySQL وSQLite خياران جيدان أيضًا، لكن إن لم يكن لديك سبب قوي فاختر Postgres وتوقّف عن التردد.

**تصميم المخطط (Schema) في SaaS.** بعض الأعراف (conventions) تؤتي ثمارها من اليوم الأول:

- **كل جدول يملكه مستأجر (tenant-owned table) فيه عمود (column) `organization_id`** (من الدرس 1.2)، حتى لو استطعت استنتاجه عبر ربط (Join). هذا يجعل التصفية (filtering) والفهرسة (indexing) والعزل (isolation) لاحقًا (الدرس 2.4) أبسط بكثير.
- **كل جدول (table) فيه `created_at` و`updated_at`**، مخزّنين بنوع `timestamptz` (طابع زمني (timestamp) مع المنطقة الزمنية) بتوقيت UTC. ستحتاجهما لتذاكر الدعم (support tickets) وتصحيح الأخطاء (debugging) والتدقيق (audits).
- **استخدم القيود (Constraints).** `NOT NULL`، و`UNIQUE (organization_id, slug)`، والمفاتيح الأجنبية (foreign keys)، و`CHECK (interval_seconds >= 30)`. قاعدةٌ تفرضها قاعدة البيانات تساوي عشر مراجعات كود (code reviews).

هذا هو المخطط الأساسي (base schema) لـ Beacon:

```mermaid
erDiagram
    ORGANIZATION ||--o{ MEMBERSHIP : "تملك (has)"
    USER ||--o{ MEMBERSHIP : "يملك (has)"
    ORGANIZATION ||--o{ MONITOR : "تمتلك (owns)"
    MONITOR ||--o{ CHECK_RESULT : "يسجّل (records)"
    MONITOR ||--o{ INCIDENT : "يفتح (opens)"
    ORGANIZATION {
        string id
        string name
        string plan
        timestamp created_at
    }
    MONITOR {
        string id
        string organization_id
        string url
        int interval_seconds
        timestamp created_at
    }
    CHECK_RESULT {
        string id
        string monitor_id
        int status_code
        int latency_ms
        timestamp checked_at
    }
    INCIDENT {
        string id
        string monitor_id
        string status
        timestamp opened_at
    }
```

**اختيار المعرّفات (IDs).** الأعداد الصحيحة ذات الزيادة التلقائية (auto-increment integers) (`1, 2, 3`) صغيرة وسريعة، لكنها تسرّب معلومات (يستطيع منافس أن يعدّ عملاءك بالتسجيل (signup) مرتين) وتجعل التخمين سهلًا. أغلب منتجات SaaS اليوم تستخدم أحد هذه الأنماط:

| نمط المعرّف (Id style) | مثال | المزايا (Pros) | العيوب (Cons) |
|---|---|---|---|
| عدد صحيح بزيادة تلقائية (Auto-increment integer) | `4211` | صغير جدًا وسريع ومقروء | يمكن تخمينه، ويكشف الحجم، ويصعب دمجه بين قواعد بيانات (databases) |
| UUID v4 (عشوائي) | `9f1c…` | لا يمكن تخمينه، ويُولَّد في أي مكان | ترتيبه العشوائي يجزّئ فهارس B-tree (B-tree indexes) |
| UUID v7 / ULID (مرتب زمنيًا) | `0190…` | صعب التخمين بما يكفي، ويُرتَّب حسب وقت الإنشاء (creation time)، وملائم للفهارس | يكشف وقت الإنشاء |
| معرّف ببادئة (prefixed id) | `mon_01J8…` | يصف نفسه في السجلات (logs) وتذاكر الدعم والروابط (URLs) | يُخزَّن نصًا أو يحتاج ترميزًا وفك ترميز (encode/decode) |

نشرت Stripe فكرة المعرّفات ذات البادئة (prefixed ids): العميل `cus_…` والاشتراك (subscription) `sub_…`. عندما يلصق عميل معرّفًا في محادثة الدعم (support chat) تعرف فورًا ما هو. الخيار الافتراضي الجيد لـ Beacon هو UUIDv7 في قاعدة البيانات مع إضافة البادئات (`org_`، `mon_`، `inc_`) عند حدود الواجهة البرمجية (API boundary)، أو تخزينه نصًا مباشرة إن فضّلت البساطة. يحدّد RFC 9562 معيار UUIDv7، والإصدارات (versions) الحديثة من Postgres (18 فما فوق) تأتي بدالة مدمجة (built-in function) `uuidv7()`، وإلا فهناك مكتبات (libraries) لكل لغة.

**كيف يتحدث كودك مع قاعدة البيانات (database).** هناك ثلاثة أساليب:

| الأسلوب (Approach) | أمثلة (Examples) | ما تكتبه | يتقن (Good at) | انتبه إلى (Watch out for) |
|---|---|---|---|---|
| ORM (أداة ربط الكائنات بالجداول) | Prisma، ActiveRecord، Django ORM، TypeORM | نماذج واستدعاءات دوال | عمليات CRUD السريعة والعلاقات (relations) والترحيلات المدمجة (built-in migrations) | الاستعلامات المخفية (hidden queries)، وN+1، وصعوبة SQL المعقد |
| باني الاستعلامات | Drizzle، Kysely، Knex | TypeScript بشكل يشبه SQL | أمان الأنواع (type safety) مع التحكم في SQL (SQL control) | يجب أن تعرف SQL |
| SQL خام (raw SQL) مع توليد الكود (codegen) | sqlc (Go)، `pg` العادي | ملفات SQL | تحكم كامل وأنواع مولَّدة (generated types) | كود متكرر (boilerplate) أكثر لعمليات CRUD |

لا يوجد خيار خاطئ بين هذه. الخطأ هو ألا تعرف ما ترسله أداتك من SQL. فعّل تسجيل الاستعلامات (query logging) في بيئة التطوير (development) من اليوم الأول.

**الترحيلات (Migrations).** الترحيل ملف له إصدار (version) ومحفوظ في المستودع (Repo)، ويغيّر المخطط: `0007_add_monitor_timeout.sql`. تسجّل الأداة الترحيلات التي نُفّذت في جدول داخل قاعدة البيانات نفسها، لذلك تصل كل بيئة (environment) (جهازك، وCI، وبيئة الاختبار، والإنتاج) إلى المخطط نفسه. تفعل ذلك كلٌّ من Prisma Migrate وDrizzle Kit وترحيلات Rails وDjango وLaravel وgolang-migrate وgoose وFlyway وAtlas. القاعدة: **لا تغيّر مخطط الإنتاج (production schema) يدويًا أبدًا.** إن لم يكن التغيير في ترحيل فهو لم يحدث.

**بيانات البذر والتجهيزات (Seeds and Fixtures).** سكربت البذر (seed script) يملأ قاعدة بيانات جديدة ببيانات واقعية: منظمة تجريبية (demo org)، وثلاثة مستخدمين بأدوار (roles) مختلفة، وعشرون مراقِبًا (monitor)، وأسبوع من نتائج الفحص (check results)، وحادثة واحدة مفتوحة. بفضله يصبح تجهيز مطوّر جديد (onboarding) أمرًا واحدًا. التجهيزات (fixtures) هي النسخة الخاصة بالاختبارات (tests): مجموعات بيانات صغيرة ومعروفة تُحمَّل قبل الاختبارات. اجعل سكربت البذر متساوي القوة (Idempotent)، أي آمنًا عند تشغيله مرتين، ولا تسمح له بالعمل على الإنتاج أبدًا.

### 🟡 التعمق أكثر (Going deeper)

**الفهارس (indexes) ومشكلة N+1 (N+1 problem).** الفهرس (Index) بنية جانبية مرتبة تسمح لـ Postgres بإيجاد الصفوف (rows) دون مسح الجدول (scanning) كله. أكثر استعلامات (queries) Beacon شيوعًا هو "آخر الفحوص (checks) لهذا المراقِب"، لذلك يحتاج إلى:

```sql
CREATE INDEX check_result_monitor_time_idx
  ON check_result (monitor_id, checked_at DESC);
```

ترتيب الأعمدة مهم: هذا الفهرس يخدم الاستعلامات التي تصفّي حسب `monitor_id` وترتّب حسب `checked_at`، وليس العكس. تعلّم قراءة مخرجات `EXPLAIN ANALYZE`؛ فوجود `Seq Scan` على جدول كبير في مسار ساخن (hot path) هو بلاغ خطأ (bug report) ينتظر أن يُكتب. وتذكّر أن Postgres *لا* يفهرس أعمدة المفاتيح الأجنبية تلقائيًا.

مشكلة N+1 (N+1 problem) التي رأيناها في البداية هي الفخ الكلاسيكي لأدوات ORM: استعلام واحد للقائمة، ثم N استعلامًا لعلاقة (relation) كل عنصر. الحل أن تجلب العلاقات دفعة واحدة: `include` في Prisma، و`with` في الاستعلامات العلائقية في Drizzle، و`includes`/`preload` في Rails، و`select_related`/`prefetch_related` في Django، أو استعلام SQL واحد مع ربط أو `DISTINCT ON`. سجلات الاستعلامات (query logs) وتتبّعات (traces) APM (الدرس 7.2) تجعلها مرئية.

**المعاملات (Transactions).** المعاملة (transaction) تجمع عدة تعليمات بحيث تنجح كلها أو تفشل كلها. عندما يفتح Beacon حادثة، يجب أن يُدرج الحادثة، ويعلّم المراقِب بأنه متوقف، ويضع الإشعارات (notifications) في الطابور (queue). إن فشلت الخطوة الثانية بعد نجاح الأولى فستكون لديك حادثة لمراقِب يبدو سليمًا. ضعها في معاملة واحدة. اجعل المعاملات قصيرة، ولا تستدعِ واجهات خارجية (external APIs) (Stripe، البريد) داخلها أبدًا. النمط المناسب لـ "اكتب في قاعدة البيانات وأطلق أثرًا جانبيًا (side effect) بشكل موثوق" هو **صندوق الصادر المعاملاتي (Transactional Outbox)**: أدرج صفًا (row) في جدول `outbox` ضمن المعاملة نفسها، ودع عاملًا في الخلفية (background worker) (الدرس 5.1) يوصله.

**ترحيلات بلا توقف (zero-downtime migrations): التوسيع ثم التقليص (Expand and Contract).** أثناء النشر يعمل الإصدار القديم والجديد من كودك في الوقت نفسه على قاعدة بيانات واحدة. لذلك يجب أن يكون الترحيل متوافقًا مع الاثنين. إعادة تسمية `monitor.url` إلى `monitor.target` بأمان تحتاج عدة عمليات نشر (deploys):

```mermaid
flowchart RL
    A["1. التوسيع<br/>إضافة العمود target<br/>(1. Expand<br/>add column target)"] --> B["2. الكتابة المزدوجة<br/>الكود يكتب في url وtarget<br/>(2. Dual-write<br/>code writes url and target)"]
    B --> C["3. الملء الرجعي<br/>نسخ الصفوف القديمة على دفعات<br/>(3. Backfill<br/>copy old rows in batches)"]
    C --> D["4. تحويل القراءة<br/>الكود يقرأ target<br/>(4. Switch reads<br/>code reads target)"]
    D --> E["5. التقليص<br/>حذف العمود url<br/>(5. Contract<br/>drop column url)"]
```

عمليات خطرة أخرى في Postgres: إضافة عمود بقيمة افتراضية متقلبة (volatile default) مثل `clock_timestamp()` (تعيد كتابة الجدول كله)، وإنشاء فهرس دون `CONCURRENTLY` (يمنع الكتابة (blocks writes) على الجدول)، وإضافة قيد (constraint) `NOT NULL` على جدول كبير في خطوة واحدة، وتغيير نوع عمود. هناك أدوات تساعد: جوهرة (gem) `strong_migrations` في Rails ترفض الترحيلات غير الآمنة (unsafe migrations)، وAtlas يستطيع فحص الترحيلات (lint) بحثًا عن التغييرات المدمّرة (destructive changes). واضبط أيضًا `lock_timeout` في الترحيلات، كي يفشل الترحيل الذي ينتظر قفلًا (lock) بسرعة بدلًا من أن يصطف كل استعلام آخر خلفه.

**تجميع الاتصالات (Connection Pooling).** كل اتصال بـ Postgres هو عملية (process) على الخادم (server) تستهلك ذاكرة حقيقية، والنسخة المُدارة (managed instance) المعتادة تسمح ببضع مئات من الاتصالات (connections) على الأكثر. الدوال عديمة الخادم (Serverless) تكسر الإعدادات الساذجة: 500 استدعاء متزامن (concurrent invocations) قد يفتح كلٌّ منها اتصالًا (connection) فتُستنزف قاعدة البيانات. الحل هو **مجمّع اتصالات (Connection Pooler)** بين التطبيق وقاعدة البيانات (DB): PgBouncer هو الكلاسيكي، وSupabase يشغّل Supavisor، وNeon وأغلب المزوّدين (providers) المُدارين يعطونك سلسلة اتصال مجمّعة. في وضع *المعاملة* في PgBouncer يكون اتصال الخادم (server connection) لك فقط طوال المعاملة، ما يعني أن ميزات الجلسة (session features) (أوامر `SET` على مستوى الجلسة (session level)، والأقفال الاستشارية (advisory locks) الممتدة عبر المعاملات، وبعض إعدادات التعليمات المُعدّة مسبقًا) تتصرف بشكل مختلف.

### 🔴 على نطاق واسع وللمؤسسات

**النسخ الاحتياطي (backups) والاستعادة إلى نقطة زمنية (PITR).** أمر `pg_dump` ليلي بداية، وليس استراتيجية (strategy). يكتب Postgres كل تغيير في سجل الكتابة المسبقة (WAL)؛ فإن أرشفت نسخة أساسية (base backup) مع تدفق WAL تستطيع استعادة قاعدة البيانات إلى *أي لحظة*، مثل 14:31:59، قبل ثانية من تشغيل أحدهم أمر `DELETE` الخاطئ. الخدمات المُدارة (managed services) تقدّم PITR كإعداد، ومن يستضيف بنفسه (self-hosters) يستخدم أدوات مثل pgBackRest أو WAL-G. درس GitLab ينطبق هنا: **النسخة الاحتياطية (backup) التي لم تستعدها يومًا أمل، وليست نسخة احتياطية.** حدّد موعدًا لتمرين استعادة (restore drill)، وقِس المدة التي يستغرقها (هذا هو زمن التعافي (recovery time) الحقيقي لديك)، وضع الرقم في دليل التشغيل (runbook). استبيانات المؤسسات (enterprise questionnaires) ستسأل عن هذه الأرقام تحديدًا (RPO وRTO).

**النسخ المتماثلة للقراءة (Read Replicas).** النسخة المتماثلة (replica) نسخة من قاعدة البيانات تتبع الأساسية (primary) عبر بثّ WAL الخاص بها. تستطيع إرسال استعلامات القراءة فقط (read-only queries) (التقارير (reports)، والتحليلات (analytics)، وصفحة الحالة العامة) إليها. المشكلة (Problem) هي **تأخر التماثل (Replication Lag)**: يحفظ المستخدم مراقِبًا، ويُعاد توجيهه (redirected)، ولم ترَ النسخة المتماثلة الكتابة بعد، فـ"يختفي" المراقِب. الحل الشائع: اقرأ ما كتبته من القاعدة الأساسية لبضع ثوانٍ بعد الكتابة، أو وجّه الطلبات (requests) حسب نقطة النهاية (endpoint).

**السلاسل الزمنية (time-series) والجداول الساخنة (hot tables).** جدول `check_result` في Beacon يزداد ملايين الصفوف يوميًا. **التقسيم (Partitioning)** التصريحي حسب الوقت (قسم لكل (partition) يوم أو شهر) يسمح لك بحذف البيانات القديمة بـ `DROP TABLE` بدلًا من `DELETE` بطيء، ويبقي الفهارس صغيرة. إضافات (extensions) مثل TimescaleDB تؤتمت ذلك.

**مقايضات الحذف الناعم (Soft Delete).** الحذف الناعم (soft-delete) يعني ضبط `deleted_at` بدلًا من إزالة الصف. هذا يتيح "التراجع" والاستعادة، لكن كل استعلام يجب الآن أن يصفّي `WHERE deleted_at IS NULL`، وقيود التفرّد (unique constraints) يجب أن تصبح فهارس جزئية (partial indexes)، وطلبات المحو (erasure requests) وفق GDPR (الدرس 8.1) تتطلب حذفًا حقيقيًا (real delete) في النهاية. النمط الأنظف لكثير من الجداول هو الحذف الفعلي (hard delete) مع سجل تدقيق (audit log) أو جدول أرشيف (archive table) (الدرس 7.3). استخدم الحذف الناعم عن قصد للكائنات (objects) القليلة التي يتوقع المستخدمون استعادتها (منظمة (org)، صفحة حالة)، وليس في كل مكان بحكم العادة.

**الخيارات المُدارة (Managed options).** Neon (Postgres عديم الخادم مع التفريع (branching): قاعدة بيانات بنسخ عند الكتابة (copy-on-write) لكل طلب دمج)، وSupabase (Postgres مع المصادقة (auth) والتخزين (storage) والوقت الحقيقي (realtime) وواجهة برمجية مولَّدة تلقائيًا)، وAmazon RDS/Aurora، وGoogle Cloud SQL/AlloyDB، وPlanetScale (المعروف بـ MySQL المبني على Vitess مع تغييرات مخطط (schema changes) لا تحجب العمل (non-blocking)، ويقدّم الآن Postgres أيضًا).

## 🏆 أفضل المستودعات

| المستودع | ما هو | التقنيات (Stack) | الترخيص (License) | اختره عندما (Pick it when) |
|---|---|---|---|---|
| [postgres/postgres](https://github.com/postgres/postgres) | قاعدة البيانات نفسها (نسخة مطابقة (mirror) على GitHub) | C | PostgreSQL | تريد قراءة كود أو توثيق (documentation) الشيء الذي تعتمد عليه |
| [prisma/orm](https://github.com/prisma/orm) | أداة ORM تبدأ من المخطط، مع ترحيلات وأداة Studio | TypeScript | Apache-2.0 | تريد أسهل مدخل وملف مخطط مقروء |
| [drizzle-team/drizzle-orm](https://github.com/drizzle-team/drizzle-orm) | أداة ORM لـ TypeScript تشبه SQL، مع ترحيلات Drizzle Kit | TypeScript | Apache-2.0 | تعرف SQL، وتريد الأنواع، وتنشر على بيئة عديمة الخادم أو على الحافة (edge) |
| [kysely-org/kysely](https://github.com/kysely-org/kysely) | باني استعلامات SQL آمن الأنواع (type-safe) | TypeScript | MIT | تريد التحكم في SQL مع الأنواع ودون طبقة ORM |
| [sqlc-dev/sqlc](https://github.com/sqlc-dev/sqlc) | يولّد كودًا آمن الأنواع من استعلامات SQL | Go | MIT | تكتب بلغة Go وتفضّل ملفات SQL على ORM |
| [ariga/atlas](https://github.com/ariga/atlas) | إدارة تصريحية للمخطط وفحص الترحيلات (migration linting) | Go | Apache-2.0 | تريد مقارنة الترحيلات (migration diffing) وفحوص الأمان (safety checks) في CI |
| [golang-migrate/migrate](https://github.com/golang-migrate/migrate) | أداة بسيطة لتشغيل (operations) ترحيلات SQL صعودًا ونزولًا | Go | MIT | تريد أداة ترحيل (migration tool) سطر أوامر (CLI) لا ترتبط بلغة |
| [supabase/supabase](https://github.com/supabase/supabase) | منصة (platform) Postgres: مصادقة وتخزين ووقت حقيقي وواجهات برمجية (APIs) | TypeScript, Elixir, Go | Apache-2.0 | تريد Postgres مُدارًا أو مستضافًا ذاتيًا (self-hosted) مع كل الملحقات |
| [neondatabase/neon](https://github.com/neondatabase/neon) | Postgres عديم الخادم مع فصل التخزين عن الحوسبة (storage/compute separation) | Rust | Apache-2.0 | تريد فهم التفريع والتقليص إلى الصفر (scale-to-zero) |

**إن درست مستودعًا واحدًا فقط (If you study one repo):** اقرأ توثيق Drizzle وكوده المصدري إلى جانب مخطط Drizzle حقيقي. هو قريب من SQL بما يكفي لتتعلم SQL أثناء استخدامه، ومولّد الترحيلات (migration generator) فيه يعرض بالضبط أوامر DDL (DDL statements) التي سينفّذها. إن كنت تعمل بـ Rails أو Django فأداة ORM والترحيلات المدمجة هي الجواب المكافئ؛ لا تستبدلها.

**اشترِ أم ابنِ أم استضف بنفسك (self-host)؟**

- **اشترِ (خدمة مُدارة (managed service)):** في كل الحالات تقريبًا بالنسبة لقاعدة البيانات نفسها. Neon أو Supabase أو RDS أو Cloud SQL أو PlanetScale تعطيك النسخ الاحتياطي وPITR والتحويل عند الفشل (failover) ومجمّع الاتصالات بأقل من كلفة ساعة عمل مهندس شهريًا. اختر الأقرب إلى مكان تشغيل تطبيقك.
- **استضف بنفسك (Self-host):** عندما تشغّل خوادمك أصلًا ولديك شخص سيتولى النسخ الاحتياطي والاستعادة والترقيات (upgrades)، أو عندما يتطلب عقد عميل ذلك. خصّص ميزانية لـ pgBackRest أو WAL-G ولتمرين استعادة مراقَب.
- **ابنِ (Build):** لا تبنِ قاعدة البيانات أو أداة الترحيل أبدًا. لكن ابنِ سكربت البذر الخاص بك، ودالة (function) المعرّفات (`newId("mon")`)، وطبقة وصول رفيعة للبيانات (data-access layer) كي تعيش تصفية المستأجر (tenant filtering) في مكان واحد.

## 🔍 ادرسه في مشاريع حقيقية (Study it in the wild)

**Cal.com (`calcom/cal.diy`).** مستودع أحادي (monorepo) كبير بـ Next.js يستخدم Prisma. وقت كتابة هذا الدرس يوجد المخطط تحت `packages/prisma`؛ افتح `schema.prisma` واقرأ نماذج `User` و`Team` و`Membership`، ثم تصفّح مجلد `migrations` المجاور لترى سنوات من تطوّر مخطط حقيقي، بما في ذلك عمليات الملء الرجعي (backfills) والأعمدة المعاد تسميتها.

**Documenso (`documenso/documenso`).** يستخدم Prisma أيضًا في `packages/prisma`، وهو أصغر من Cal.com، لذلك يسهل استيعابه. ابحث في المخطط عن `@default(` و`@@index`، وابحث عن سكربت البذر.

**OpenStatus (`openstatusHQ/openstatus`).** هو حرفيًا Beacon حقيقي. يستخدم Drizzle؛ استخدم بحث الكود (code search) عن `drizzle` و`sqliteTable` أو `pgTable` لتجد تعريفات جداول المراقِبات والحوادث (incidents) وصفحات الحالة (status pages). قارن جدول المراقِبات (monitors table) عندهم بمخطط الكيانات والعلاقات (ER diagram) أعلاه.

**Discourse (`discourse/discourse`).** تطبيق Rails فيه أكثر من عقد من الترحيلات. افتح `db/migrate` و`db/post_migrate`: يفصل Discourse الترحيلات التي يجب أن تعمل قبل الكود الجديد عن تلك التي تعمل بعده، وهذه فكرة التوسيع ثم التقليص مكتوبة في أسماء المجلدات.

**ما الذي تلاحظه (What to notice):**

- ما استراتيجية المعرّفات التي يستخدمها كل مشروع (cuid أو UUID أو عدد صحيح (integer) أو ببادئة)، وهل تظهر في الروابط.
- كم من الترحيلات إضافي فقط (additive) مقابل المدمّر (destructive)، وكيف تُقسَّم الترحيلات المدمّرة (destructive migrations) على مراحل.
- قيود التفرّد المركّبة التي تتضمن معرّف الفريق (team id) أو المنظمة.
- أين تُعرَّف الفهارس، وأي استعلامات تخدمها بوضوح.
- كيف ينشئ سكربت البذر مستخدمين بأدوار وخطط (plans) مختلفة.

## 🛠️ ابنِه في Beacon (Build it into Beacon)

### 🟢 تمرين المبتدئ (Beginner exercise)

أنشئ مخطط Beacon للجداول `organization` و`user` و`membership` و`monitor` و`check_result` بأداة ORM أو باني الاستعلامات الذي تختاره، وولّد الترحيل الأول، واكتب سكربت بذر متساوي القوة ينشئ منظمة واحدة، ومستخدمَين (مالك وعضو)، وخمسة مراقِبات مع يوم من نتائج الفحص المزيفة.

**يكتمل عندما (Done when):**

- ينتج عن نسخة جديدة من المستودع (fresh clone) مع أمر واحد (`npm run db:reset` أو ما يكافئه) قاعدة بيانات تعمل وفيها بيانات البذر.
- يحتوي كل جدول يملكه مستأجر على `organization_id` و`created_at` و`updated_at`، مع مفاتيح أجنبية.
- لا يُنشئ تشغيل البذر (seed) مرتين أي تكرارات (duplicates).

### 🟡 تمرين المستوى المتوسط (Intermediate exercise)

ابنِ استعلام لوحة التحكم "كل المراقِبات في منظمتي مع آخر فحص لكل منها" واجعله سريعًا. ازرع 500 مراقِب مع 1,000 فحص لكل منها، وسجّل الاستعلامات، وأصلح أي N+1، وأضف الفهرس الذي يجعل `EXPLAIN ANALYZE` يُظهر مسحًا عبر الفهرس (index scan).

```sql
SELECT DISTINCT ON (m.id) m.id, m.url, c.status_code, c.checked_at
FROM monitor m
LEFT JOIN check_result c ON c.monitor_id = m.id
WHERE m.organization_id = $1
ORDER BY m.id, c.checked_at DESC;
```

**يكتمل عندما (Done when):**

- تنفّذ الصفحة عددًا ثابتًا من الاستعلامات مهما كان عدد المراقِبات.
- لا يُظهر `EXPLAIN ANALYZE` أي مسح تسلسلي (sequential scan) على `check_result`.
- تُحمَّل الصفحة في أقل من 200 مللي ثانية (ms) محليًا مع بيانات البذر الكبيرة.

### 🔴 تمرين المستوى المتقدم (Advanced exercise)

أعد تسمية `monitor.url` إلى `monitor.target` دون توقف (zero downtime)، باستخدام التوسيع ثم التقليص عبر ثلاثة ترحيلات وعمليات نشر منفصلة على الأقل. ثم فعّل PITR لدى مزوّدك المُدار (أو pgBackRest محليًا)، واحذف كل المراقِبات عمدًا، واستعد قاعدة البيانات إلى الدقيقة السابقة.

**يكتمل عندما (Done when):**

- لا يرى سكربت حمل (load script) يضرب الواجهة البرمجية (API) طوال كل خطوة أي أخطاء.
- يعمل الملء الرجعي (backfill) على دفعات مع ضبط `lock_timeout`.
- يكون لديك دليل استعادة (restore runbook) مكتوب يتضمن زمن التعافي المقيس.

## ⚠️ أخطاء يقع فيها المبتدئون (Mistakes juniors make)

- **تعديل مخطط الإنتاج (production schema) يدويًا "هذه المرة فقط".** يصبح الإنتاج مختلفًا عن كل ملفات الترحيل (migration files)، ويفشل النشر التالي بطرق مربكة. كل تغيير يمر عبر ترحيل، بما في ذلك تغييرات الطوارئ (emergency changes).
- **إعادة تسمية عمود (column) أو حذفه في نفس عملية نشر (deploy) تغيير الكود.** النسخ القديمة التي ما زالت تعمل أثناء النشر تنهار. استخدم التوسيع ثم التقليص، والخطوات المدمّرة (destructive steps) تأتي أخيرًا في عملية نشر خاصة بها.
- **فتح عميل قاعدة بيانات (database client) جديد لكل طلب (request) في كود عديم الخادم (serverless).** تستنزف الاتصالات مع أول ارتفاع في الزيارات (traffic spike). أنشئ العميل مرة واحدة لكل عملية (per process)، واتصل عبر مجمّع اتصالات.
- **عدم النظر أبدًا إلى SQL الذي يولّده ORM.** تبقى استعلامات N+1 (N+1 queries) والفهارس الناقصة (missing indexes) غير مرئية حتى يأتي عميل كبير. فعّل تسجيل الاستعلامات في التطوير واقرأ `EXPLAIN` لأكثر خمسة استعلامات استخدامًا.
- **استدعاء Stripe أو إرسال بريد داخل معاملة قاعدة بيانات (database transaction).** تبقى الأقفال (locks) محتجزة أثناء انتظارك للشبكة (network)، والتراجع لا يستطيع إلغاء إرسال بريد. نفّذ الالتزام (commit) أولًا، ثم نفّذ الآثار الجانبية (side effects) عبر صندوق صادر (outbox) أو مهمة خلفية (job).
- **افتراض أن النسخ الاحتياطية (backups) لدى المزوّد (provider) تعمل.** استعد واحدة. قِس الوقت. اكتبه.

## 🧾 الخلاصة (Recap)

- Postgres هو الخيار الافتراضي لأنه ممل، ومُدار في كل مكان، وينمو معك (JSON، والبحث، وRLS، والمتجهات).
- ضع `organization_id` والطوابع الزمنية (timestamps) والقيود الحقيقية (real constraints) في كل جدول يملكه مستأجر، واختر معرّفات مرتبة زمنيًا ويصعب تخمينها.
- أداة ORM أو باني الاستعلامات أو SQL الخام كلها تعمل؛ ما لا يعمل هو ألا تعرف ما ينفَّذ من SQL.
- كل تغيير في المخطط ترحيل، والتغييرات الخطرة تستخدم التوسيع ثم التقليص كي يتعايش الكود القديم والجديد.
- جمّع الاتصالات، وفهرس لاستعلاماتك الحقيقية، واجعل المعاملات قصيرة والآثار الجانبية خارجها.
- PITR مع استعادة مجرّبة هو المعنى الحقيقي لعبارة "لدينا نسخ احتياطية".

## ✍️ اختبر نفسك (Check yourself)

**1. ما الترحيل (migration)، وكيف تصل كل بيئة (environment) إلى المخطط (schema) نفسه؟**

<details><summary>الإجابة (Answer)</summary>

الترحيل ملف له إصدار ومحفوظ في المستودع، ويغيّر المخطط، مثل `0007_add_monitor_timeout.sql`. تسجّل أداة الترحيل الترحيلات التي نُفّذت في جدول داخل قاعدة البيانات نفسها، لذلك يصل جهازك وCI وبيئة الاختبار والإنتاج إلى المخطط نفسه. راجع فقرة "الترحيلات" في 🟢 الأساسيات.

</details>

**2. ما مشكلة N+1 (N+1 problem)، وكيف تصلحها؟**

<details><summary>الإجابة</summary>

هي استعلام واحد لقائمة، ثم استعلام إضافي لكل عنصر لتحميل علاقته، فيصبح 400 مراقِب 401 استعلام. تصلحها بجلب العلاقات دفعة واحدة: `include` في Prisma، و`with` في Drizzle، و`includes`/`preload` في Rails، و`select_related`/`prefetch_related` في Django، أو ربط SQL واحد أو `DISTINCT ON`. راجع فقرة "الفهارس ومشكلة N+1 (N+1 problem)" في 🟡 التعمق أكثر.

</details>

**3. يريد Beacon إعادة تسمية `monitor.url` إلى `monitor.target` دون أي توقف (any downtime). ما الخطوات؟**

<details><summary>الإجابة</summary>

استخدم التوسيع ثم التقليص عبر عدة عمليات نشر: أضف العمود `target`، واجعل الكود يكتب في العمودين (both columns)، واملأ الصفوف القديمة رجعيًا على دفعات، وحوّل القراءة إلى `target`، ثم احذف `url` في عملية نشر خاصة به. كل خطوة تبقي قاعدة البيانات متوافقة مع الكود القديم والجديد اللذين يعملان جنبًا إلى جنب أثناء النشر. راجع فقرة "ترحيلات بلا توقف" في 🟡 التعمق أكثر.

</details>

**4. عندما يفتح Beacon حادثة يجب أن يُدرج الحادثة (incident)، ويعلّم المراقِب (monitor) بأنه متوقف، ويُشعر الفريق بالبريد. كيف تنظّم ذلك؟**

<details><summary>الإجابة</summary>

ضع عمليتي الكتابة في قاعدة البيانات في معاملة قصيرة واحدة كي تنجحا أو تفشلا معًا، وأضف صفًا في `outbox` ضمن المعاملة نفسها. ثم يقرأ عامل في الخلفية صندوق الصادر ويرسل البريد. لا تستدعِ البريد أو Stripe داخل المعاملة أبدًا: فهي تحتجز الأقفال أثناء انتظار الشبكة، والتراجع لا يستطيع إلغاء إرسال بريد. راجع فقرة "المعاملات" في 🟡 التعمق أكثر.

</details>

**5. ينتقل Beacon إلى منصة عديمة الخادم (serverless platform). مع أول ارتفاع في الزيارات (traffic spike) تبدأ قاعدة البيانات (database) برفض الاتصالات (connections)، مع أن الاستعلامات (queries) سريعة. ما الذي تعطّل، وما الحل؟**

<details><summary>الإجابة</summary>

كل استدعاء متزامن (concurrent invocation) للدالة فتح اتصاله الخاص بـ Postgres، والنسخة المُدارة المعتادة تسمح ببضع مئات فقط. أنشئ العميل مرة واحدة لكل عملية، واتصل عبر مجمّع اتصالات مثل PgBouncer أو Supavisor أو سلسلة الاتصال المجمّعة لدى مزوّدك. وتذكّر أن ميزات الجلسة تتصرف بشكل مختلف في وضع المعاملة (transaction mode). راجع فقرة "تجميع الاتصالات" في 🟡 التعمق أكثر.

</details>

## 📚 المراجع (References)

- PostgreSQL documentation, especially "Continuous Archiving and Point-in-Time Recovery": https://www.postgresql.org/docs/current/continuous-archiving.html — الأرشفة المستمرة (continuous archiving) والاستعادة إلى نقطة زمنية
- RFC 9562, Universally Unique IDentifiers (UUIDv7): https://www.rfc-editor.org/rfc/rfc9562 — معيار المعرّفات الفريدة
- Use The Index, Luke — a free guide to SQL indexing: https://use-the-index-luke.com — دليل مجاني لفهرسة SQL
- Stripe engineering, "Online migrations at scale": https://stripe.com/blog/online-migrations — الترحيلات أثناء التشغيل (online migrations) على نطاق واسع
- PgBouncer documentation: https://www.pgbouncer.org — أوضاع التجميع (pool modes) وحدودها
- Drizzle ORM docs: https://orm.drizzle.team · Prisma docs: https://www.prisma.io/docs
- Rails `strong_migrations` gem, a catalogue of unsafe migrations: https://github.com/ankane/strong_migrations — فهرس بالترحيلات غير الآمنة

---

# 2.2 — رفع الملفات (file uploads) وتخزين الكائنات (object storage)
*المستوى: 🟢 مبتدئ* · *المتطلبات: 2.1*

## ⚡ الدرس في دقيقة (In 60 seconds)

- الملفات (الشعارات (logos)، ولقطات الشاشة (screenshots)، وتقارير PDF، والتصديرات) مكانها تخزين كائنات متوافق مع S3 (S3-compatible object storage)، وليس أقراص خوادم التطبيق ولا قاعدة البيانات.
- القاعدة الأهم: المتصفح يرفع الملفات وينزّلها مباشرة عبر روابط موقّعة مسبقًا قصيرة العمر، لا يوقّعها خادمك إلا بعد التحقق من الصلاحيات (permissions).
- الخيار الافتراضي للإصدار الأول (v1 default): حاوية خاصة (private bucket)، وجدول بيانات وصفية (metadata) `file` في Postgres، ومفاتيح (keys) تولّدها بنفسك تحت `orgs/{orgId}/…`، وتحقق على الخادم (server-side validation) قبل التوقيع (signing) ومرة أخرى بعد الرفع (upload).
- قدّم ملفات المستخدمين (user files) من نطاق منفصل (domain)، وافحص (scan) كل ما يشاركه المستخدمون مع بعضهم.
- الفخ الأكبر: حاوية عامة (public bucket) أو رابط طويل العمر (long-lived URL)، فيصبح كل ملف خاص على بعد رابط (URL) واحد مُخمَّن أو مُعاد توجيهه (forwarded) من الإنترنت.

## 🧭 لماذا يحتاجه كل SaaS

يحتاج Beacon إلى الملفات أبكر مما تظن. كل منظمة ترفع شعارًا (logo) وأيقونة موقع (Favicon) لصفحة الحالة (status page) الخاصة بها. تحديثات الحوادث (incident updates) قد تحمل لقطات شاشة. عملاء خطة (plan) Business يريدون تقريرًا شهريًا عن مدة التشغيل (uptime) بصيغة PDF، وزر "صدّر بياناتي" ينتج ملف zip. لا شيء من هذا هو المنتج، ويجب أن يعمل كله.

نسخة المبتدئ هي نموذج (form) يرسل الملف إلى خادم Next.js أو Express، فيكتبه في `./uploads` على القرص (disk). يعمل ذلك على جهازك. أما في الإنتاج فلا يجد الخادم الثاني الملف الذي حفظه الأول، وتُعاد تشغيل الحاوية (container restarts) فيُمسح القرص، ويرفع عميل تسجيل شاشة (screen recording) بحجم 400 ميغابايت فيشغل عاملًا من عمال الويب (web worker) لدقيقتين، ويرفع أحدهم ملف HTML اسمه `logo.png` يشغّل JavaScript على نطاقك. ولأن المجلد يُقدَّم للعموم، فإن رابطًا مُخمَّنًا يعرض لقطات شاشة حوادث عميل على عميل آخر.

كانت حاويات التخزين العامة سيئة الإعداد إحدى أكثر قصص تسريب البيانات (data-leak) تكرارًا في العقد الماضي، ولهذا السبب بالضبط: الملفات سهلة التخزين وسهلة النسيان.

**الملفات لا مكان لها في قاعدة بياناتك ولا على خوادم تطبيقك (your app servers): مكانها تخزين الكائنات (object storage)، يرفعها المتصفح مباشرة بروابط موقّعة (signed URLs) قصيرة العمر (short-lived)، ولا تُقرأ إلا عبر فحوص (checks) تتحكم أنت فيها.**

## 📐 كيف يعمل

### 🟢 الأساسيات

**تخزين الكائنات (Object Storage)** خدمة تخزّن كتلًا من البيانات (blobs) (بايتات مع قليل من البيانات الوصفية) تحت مفاتيح في فضاء أسماء مسطّح (flat namespace) يسمى الحاوية (Bucket). هو ليس نظام ملفات (filesystem): لا توجد مجلدات حقيقية، ولا إلحاق (appending)، ولا كتابة جزئية (partial overwrites)؛ أنت تضع كائنًا (object) كاملًا، أو تجلبه، أو تحذفه. في المقابل هو رخيص، وغير محدود عمليًا، ومتين جدًا (durable). عرّفت Amazon S3 الواجهة البرمجية، وأصبح "المتوافق مع S3 (S3-compatible)" هو المعيار اليوم: Cloudflare R2، وGoogle Cloud Storage (عبر وضع التوافق)، وBackblaze B2، وDigitalOcean Spaces، وSupabase Storage، والخوادم المستضافة ذاتيًا (self-hosted servers) مثل SeaweedFS وGarage وMinIO كلها تتحدث بها. اكتب كودك على واجهة S3 وستستطيع تغيير المزوّد بتغيير نقطة النهاية وبيانات الاعتماد (credentials).

**لماذا لا نستخدم خادم التطبيق (app server) أو قاعدة البيانات (database)؟**

| المكان | المشكلة |
|---|---|
| قرص خادم التطبيق | يضيع عند إعادة النشر، ولا يُشارَك بين النسخ (instances)، ويشغل عمال الويب (web workers) أثناء الرفع البطيء (slow uploads) |
| عمود `bytea` في قاعدة البيانات | يضخّم النسخ الاحتياطية والنسخ المتماثلة (replicas)، ومكلف لكل غيغابايت، وبطيء في البث (stream) |
| تخزين الكائنات | مصمَّم لهذا الغرض: رخيص ومتين ويبث مباشرة من العملاء وإليهم |

قاعدة البيانات ما زالت مهمة: فهي تخزّن صف **البيانات الوصفية (metadata)** (جدول `file`: المعرّف (id)، وorganization_id، والمفتاح (key)، ونوع المحتوى (content type)، والحجم، وuploaded_by، والحالة). والحاوية تخزّن البايتات. الصف هو ما تستخدمه فحوص التفويض (authorization checks) وواجهة المستخدم؛ والمفتاح مجرد مؤشر (pointer).

**الروابط الموقّعة مسبقًا (Presigned URLs).** الرابط الموقّع مسبقًا (presigned URL) رابط S3 عادي يحمل توقيعًا (signature) في سلسلة الاستعلام (query string)، ويمنح عملية واحدة محددة (PUT لهذا المفتاح، أو GET لهذا المفتاح) حتى وقت انتهاء (expiry time)، دون أن تسلّم بيانات اعتمادك. يوقّعه خادمك بعد التحقق من الصلاحيات (checking permissions)، ثم يتحدث المتصفح مع التخزين مباشرة، فلا تمر الملفات الكبيرة (large files) عبر تطبيقك أبدًا.

```mermaid
sequenceDiagram
    participant S as تخزين الكائنات (Object storage)
    participant D as Postgres
    participant A as واجهة Beacon البرمجية (Beacon API)
    participant B as المتصفح (Browser)
    B->>A: POST /uploads مع الاسم والنوع والحجم (POST /uploads with name, type, size)
    A->>A: التحقق من الجلسة والدور وحدود الخطة (Check session, role and plan limits)
    A->>D: إدراج صف الملف بحالة pending (Insert file row with status pending)
    A->>S: توقيع رابط PUT لمفتاح المنظمة بصلاحية 5 دقائق (Sign PUT URL for org key, 5 min expiry)
    A-->>B: الرابط الموقّع ومعرّف الملف (Presigned URL and file id)
    B->>S: PUT لبايتات الملف مباشرة (PUT file bytes directly)
    S-->>B: 200 OK
    B->>A: POST /uploads/id/complete
    A->>S: HEAD للكائن للتحقق من الحجم والنوع (HEAD object to verify size and type)
    A->>D: تعليم صف الملف بأنه جاهز (Mark file row as ready)
```

التنزيل (download) يعكس هذا المسار: يطلب المتصفح ملفًا من واجهتك البرمجية، فتتحقق الواجهة من أن المستخدم يستطيع رؤيته، وتعيد رابط GET موقّعًا صالحًا لبضع دقائق. مع AWS SDK لـ JavaScript v3 يكفي بضعة أسطر:

```ts
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const s3 = new S3Client({ region: "auto", endpoint: process.env.S3_ENDPOINT });

export async function signLogoUpload(orgId: string, fileId: string, type: string) {
  const key = `orgs/${orgId}/logos/${fileId}`;
  const cmd = new PutObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: key,
    ContentType: type, // must match what the browser sends
  });
  return { key, url: await getSignedUrl(s3, cmd, { expiresIn: 300 }) };
}
```

ميزة "direct uploads" في Rails Active Storage، وDjango مع `django-storages`، و`Storage::temporaryUrl` في Laravel تطبّق النمط نفسه.

**مفاتيح تولّدها أنت (Keys you generate)، لا أسماء ملفات المستخدمين (user filenames).** ولّد مفتاح الكائن (object key) بنفسك (`orgs/org_123/logos/file_456`) وخزّن اسم الملف الأصلي (original filename) في قاعدة البيانات. الأسماء التي يرسلها المستخدمون تحتوي مسافات ويونيكود (unicode) و`../` وتتصادم (collisions) مع بعضها.

**خاص افتراضيًا (Private by default).** يجب أن تحجب الحاويات (buckets) الوصول العام (public access) (حاويات S3 الجديدة تفعل ذلك افتراضيًا). قدّم الملفات الخاصة (private files) عبر روابط GET موقّعة قصيرة العمر. الأشياء العامة فعلًا، مثل شعار صفحة الحالة (status page logo)، يمكن أن تذهب إلى حاوية عامة منفصلة أو خلف CDN، لكن اختر ذلك لكل حاوية على حدة وعن قصد.

### 🟡 التعمق أكثر

**التحقق (validation) يحدث على الخادم (server)، مرتين.** قبل التوقيع، افحص الحجم ونوع المحتوى المعلنين مقابل قائمة مسموحات (allowlist) (الشعارات: PNG وJPEG، وSVG فقط بعد تنقيته (sanitised)، وحد أقصى 2 ميغابايت). لكن المتصفح قد يكذب، لذلك تحقق مرة أخرى بعد الرفع: نفّذ `HEAD` على الكائن لمعرفة حجمه الحقيقي، واقرأ البايتات الأولى لاكتشاف نوعه الفعلي من رقمه السحري (Magic Number) (حزمة (package) `file-type` في npm، و`python-magic` في Python، و`http.DetectContentType` في Go). رابط PUT الموقّع لا يفرض حدًا أقصى للحجم بمفرده؛ أما رابط **POST** الموقّع (presigned POST) مع سياسة (policy) فيستطيع ذلك (`content-length-range`)، ولهذا تستخدم مكتبات رفع (upload libraries) كثيرة POST. قدّم ملفات المستخدمين مع `Content-Disposition: attachment` ما لم تحتج عرضها داخل الصفحة، ولا تقدّمها أبدًا من نطاق تطبيقك الرئيسي: ملف HTML أو SVG مرفوع على `app.beacon.dev` يستطيع تشغيل سكربت (script) يصل إلى ملفات تعريف الارتباط (Cookies) لديك. استخدم نطاقًا منفصلًا (separate domain) مثل `beaconusercontent.com`.

**فحص البرمجيات الخبيثة (malware scanning).** إن كان المستخدمون يشاركون الملفات مع مستخدمين آخرين (مرفقات حوادث (incident attachments) يراها الفريق كله، أو مشتركو صفحة الحالة)، فافحصها. الإعداد الشائع: يصل الملف المرفوع إلى بادئة حجر صحي (quarantine prefix)، ويطلق حدث إنشاء الكائن (object-created event) مهمة خلفية (الدرس 5.1) تشغّل ClamAV أو خدمة فحص سحابية، وبعد ذلك فقط يُنقل الملف أو يُعلَّم بأنه `ready`. حتى ذلك الحين تعرض الواجهة "قيد المعالجة (processing)".

**الرفع المجزّأ والقابل للاستئناف (multipart and resumable uploads).** الملفات الكبيرة تفشل على الاتصالات المتقطعة (flaky connections). **الرفع المجزّأ (Multipart Upload)** في S3 يقسم الملف إلى أجزاء (5 ميغابايت على الأقل لكل جزء، باستثناء الأخير) تُرفع بالتوازي ويمكن إعادة محاولة (retried) كل منها منفردًا، ثم يجمعها استدعاء "complete". **tus** بروتوكول مفتوح (open protocol) للرفع القابل للاستئناف (resumable upload) عبر HTTP: يستطيع العميل الاستئناف من آخر بايت بعد انقطاع الاتصال (dropped connection) أو حتى بعد إعادة تشغيل المتصفح. `tusd` هو الخادم المرجعي (reference server) ويستطيع الكتابة إلى S3، وUppy أداة رفع (uploader) للمتصفح بواجهة لوحة تحكم وسحب وإفلات (drag-and-drop) وإضافات (plugins) لـ tus والرفع المجزّأ في S3 (S3 multipart uploads) والرفع الموقّع مسبقًا. أما UploadThing فتغلّف المسار كله (التوقيع، والاستدعاءات الراجعة (callbacks)، ومكوّنات React) كخدمة مستضافة (hosted service) مع SDK مفتوح المصدر.

| الأسلوب | الأنسب لـ (Best for) | ما تشغّله |
|---|---|---|
| رابط PUT أو POST موقّع واحد | ملفات أقل من ~100 ميغابايت، والشعارات، ولقطات الشاشة | واجهتك البرمجية مع الحاوية |
| رفع S3 مجزّأ (S3 multipart) مع أجزاء (parts) موقّعة | الملفات الكبيرة والسرعة بالتوازي | واجهتك البرمجية توقّع كل جزء |
| tus القابل للاستئناف (resumable) | الشبكات غير الموثوقة (unreliable networks)، والملفات الكبيرة جدًا، والجوال (mobile) | خادم tus مثل tusd |
| أداة رفع مستضافة (UploadThing) | الإطلاق السريع (shipping fast) في Next.js | خدمتهم مع استدعاءاتك الراجعة |

**الصور وشبكات CDN (CDNs).** لا تقدّم صورة هاتف بحجم 6 ميغابايت كصورة رمزية (avatar) بعرض 32 بكسل. غيّر الحجم عند الرفع بمهمة خلفية (background job) تستخدم `sharp` (Node) أو Pillow (Python)، أو غيّره عند الطلب بوسيط صور (image proxy) مثل imgproxy، أو بخدمة صور (image service) لدى مزوّد (Cloudflare Images، وimgix، وتحسين الصور (image optimisation) في Vercel). ضع شبكة CDN (شبكة توصيل المحتوى، وهي كاش عالمي) أمام الأصول العامة (public assets) كي تُحمَّل شعارات صفحات الحالة بسرعة في كل العالم. استخدم مفاتيح ثابتة لا تتغير (immutable keys) (مفتاح جديد لكل إصدار جديد) كي تستطيع التخزين المؤقت (cache) إلى الأبد دون صراع مع كاش قديم (stale caches).

### 🔴 على نطاق واسع وللمؤسسات

**بادئات مفاتيح لكل مستأجر (per-tenant key prefixes).** ضع كل كائن تحت `orgs/{orgId}/…`. هذا يجعل سياسات IAM (IAM policies)، وقواعد دورة الحياة (lifecycle rules)، وتقارير الاستخدام (usage reports) لكل مستأجر ("أنت تستخدم 3.2 غيغابايت")، وحذف المستأجر (tenant deletion) أمورًا مباشرة: لإنهاء خدمة عميل (offboard) احذف بادئة. ويجعل أيضًا أخطاء تجاوز حدود المستأجر (cross-tenant bugs) أسهل اكتشافًا: دالة توقيع (signing function) تتأكد من أن المفتاح يبدأ ببادئة منظمة المستدعي (caller) حارس رخيص (guard) ضد خطأ تبديل المعرّفات (id-swapping bug).

```mermaid
flowchart TD
    B["الحاوية beacon-private<br/>(Bucket beacon-private)"] --> O1["orgs/org_1/"]
    B --> O2["orgs/org_2/"]
    O1 --> L1["logos/"]
    O1 --> A1["attachments/"]
    O1 --> E1["exports/ تنتهي بعد 7 أيام<br/>(exports/ expires after 7 days)"]
    O2 --> L2["logos/"]
    O2 --> A2["attachments/"]
    B --> Q["quarantine/ بانتظار الفحص<br/>(quarantine/ pending scan)"]
```

**قواعد دورة الحياة (Lifecycle Rules).** يستطيع مزوّدو التخزين (storage providers) إنهاء الكائنات أو نقلها تلقائيًا حسب البادئة والعمر. يجب على Beacon أن يحذف `exports/` بعد سبعة أيام، وأن ينقل المرفقات (attachments) القديمة إلى طبقة الوصول غير المتكرر (infrequent-access tier)، وأن **يلغي عمليات الرفع المجزّأ غير المكتملة (incomplete multipart uploads)** بعد يوم (وإلا بقيت الأجزاء المهجورة (abandoned parts) هناك تكلّفك دون أن تراها). وافحص بشكل دوري (reconcile) أيضًا: ابحث عن صفوف `pending` أقدم من يوم واحذف الصف وأي كائن مرتبط به.

**الحذف (deletion) وGDPR.** عندما يحذف مستخدم حادثة، احذف مرفقاتها أيضًا، عبر مهمة خلفية لا داخل الطلب. عندما تغلق منظمة حسابها، يحدد عقدك وسياسة الخصوصية (privacy policy) مدى سرعة زوال بياناتها؛ وتخزين الكائنات هو المكان الذي تبقى فيه البيانات بصمت. إن كانت إدارة إصدارات الحاوية (bucket versioning) مفعّلة (وهي حماية جيدة من الحذف الخاطئ)، فإن "الحذف" يضيف علامة حذف (delete marker) فقط؛ وتبقى الإصدارات القديمة حتى تزيلها قاعدة دورة حياة (lifecycle rule) تحذف الإصدارات غير الحالية (noncurrent versions). اعرف نافذة الاحتفاظ (retention window) لديك ووثّقها (الدرس 8.1).

**التكلفة وحركة الخروج (Egress).** التخزين رخيص؛ أما نقل البيانات إلى الخارج فغالبًا ليس كذلك. تفرض S3 رسومًا على حركة الخروج، بينما لا تفرض Cloudflare R2 أي رسوم عليها، ولهذا تحتفظ منتجات SaaS كثيرة بالأصول (assets) التي يراها المستخدمون على R2. ضع CDN في الأمام في الحالتين.

**إقامة البيانات (residency) وحاوية العميل الخاصة (bring-your-own-bucket).** قد يحتاج عملاء الاتحاد الأوروبي (EU) إلى تخزين ملفاتهم في منطقة أوروبية (EU region) (الدرس 2.4)، فتصبح المنطقة (region) جزءًا من إعدادات المستأجر (tenant's config)، ويختار كود التوقيع (signing code) الحاوية الصحيحة. يطلب بعض عملاء المؤسسات (enterprise customers) تخزين الملفات في حاويتهم *الخاصة*؛ واجهة S3 تجعل ذلك ممكنًا (نقطة نهاية وحاوية وبيانات اعتماد لكل مستأجر (tenant)، أو دور عبر الحسابات)، لكنها تضاعف مساحة الدعم (support surface) لديك. قدّم ذلك فقط في الخطة التي تدفع مقابله.

**الاستضافة الذاتية (self-hosting).** إن كنت تقدّم نسخة قابلة للاستضافة الذاتية (الدرس 7.4) أو تحتاج تخزينًا داخل مقر العميل (on-prem)، فأنت تحتاج خادمًا متوافقًا مع S3 (S3-compatible). كان MinIO الخيار الافتراضي لسنوات، لكن في 2025 انتقلت نسخته المجتمعية (community edition) إلى التوزيع (distribution) كمصدر فقط (source-only) ووضع الصيانة (maintenance mode)، ثم أُرشف (archived) مستودع `minio/minio`. البدائل المعتادة هي SeaweedFS، وRustFS (خادم مرخّص بـ Apache-2.0 صُمّم للانتقال من MinIO والعمل بجانبه)، وGarage (خادم S3 خفيف وموزّع جغرافيًا (geo-distributed) من Deuxfleurs).

## 🏆 أفضل المستودعات

| المستودع | ما هو | التقنيات | الترخيص | اختره عندما |
|---|---|---|---|---|
| [transloadit/uppy](https://github.com/transloadit/uppy) | واجهة رفع معيارية للمتصفح مع إضافات S3 والرفع المجزّأ وtus | JavaScript | MIT | تريد أداة رفع مصقولة (polished) دون أن تكتبها |
| [tus/tusd](https://github.com/tus/tusd) | خادم tus المرجعي للرفع القابل للاستئناف، مع دعم S3 | Go | MIT | يرفع المستخدمون ملفات كبيرة عبر شبكات غير موثوقة |
| [pingdotgg/uploadthing](https://github.com/pingdotgg/uploadthing) | SDK لخدمة الرفع المستضافة UploadThing | TypeScript | MIT | تعمل بـ Next.js وتريد الرفع جاهزًا بعد ظهر اليوم |
| [aws/aws-sdk-js-v3](https://github.com/aws/aws-sdk-js-v3) | SDK الرسمي من AWS: عميل S3 (S3 client)، والتوقيع المسبق (presigner)، وأدوات الرفع المجزّأ | TypeScript | Apache-2.0 | توقّع الروابط بنفسك مع أي تخزين متوافق مع S3 (S3-compatible) |
| [lovell/sharp](https://github.com/lovell/sharp) | تغيير حجم الصور وتحويلها بسرعة في Node | C++, JavaScript | Apache-2.0 | تنشئ صورًا مصغرة (thumbnails) وصورًا رمزية (avatars) في مهمة خلفية |
| [imgproxy/imgproxy](https://github.com/imgproxy/imgproxy) | خادم لتغيير حجم الصور عند الطلب | Go | Apache-2.0 | تريد تحويلات عبر الرابط (URL-based transforms) خلف CDN |
| [supabase/storage](https://github.com/supabase/storage) | واجهة التخزين في Supabase: خلفية S3 (S3 backend)، وبيانات وصفية في Postgres، وسياسات (policies) | TypeScript | Apache-2.0 | تريد قراءة كود خدمة تخزين (storage service) تعمل في الإنتاج |
| [seaweedfs/seaweedfs](https://github.com/seaweedfs/seaweedfs) | مخزن كتل موزّع مع بوابة S3 (S3 gateway) | Go | Apache-2.0 | تستضيف التخزين بنفسك على نطاق حقيقي (real scale) |
| [rustfs/rustfs](https://github.com/rustfs/rustfs) | مخزن كائنات متوافق مع S3 (S3-compatible) صُمّم للانتقال من MinIO والعمل بجانبه | Rust | Apache-2.0 | تستبدل MinIO (المؤرشف) أو تريد ترخيصًا متساهلًا (permissive licence) |

يُطوَّر Garage على منصة Deuxfleurs الخاصة ([garagehq.deuxfleurs.fr](https://garagehq.deuxfleurs.fr))، وله نسخة مرآة للقراءة فقط (read-only mirror) على GitHub في [deuxfleurs-org/garage](https://github.com/deuxfleurs-org/garage). وهو مناسب لعمليات النشر الصغيرة (deployments) المستضافة ذاتيًا أو الموزعة على عدة مواقع.

**إن درست مستودعًا واحدًا فقط (If you study one repo):** `supabase/storage`. إنه خدمة تخزين حقيقية متعددة المستأجرين (multi-tenant) تفعل بالضبط ما يصفه هذا الدرس: البايتات في خلفية S3 (S3 backend)، وصفوف البيانات الوصفية في Postgres، والوصول تحدده سياسات قاعدة البيانات، والروابط الموقّعة، والرفع القابل للاستئناف. قراءة الطريقة التي يربط بها الطلب بحاوية ومفتاح وفحص صلاحية (permission check) تعلّمك أكثر من أي درس تعليمي.

**اشترِ أم ابنِ أم استضف بنفسك ⁦(Buy, build, or self-host?)⁩؟**

- **اشترِ (Buy):** S3 أو Cloudflare R2 أو Google Cloud Storage للبايتات، دائمًا، ما لم يكن لديك سبب لغير ذلك. وUploadThing أو Transloadit أو Cloudinary إن كنت تفضّل ألا تمتلك مسار الرفع (upload path) ومعالجة الصور (image processing).
- **استضف بنفسك (Self-host):** SeaweedFS أو Garage لنسخة من المنتج قابلة للاستضافة الذاتية (self-hostable)، أو لعملاء معزولين عن الشبكة (air-gapped)، أو لبيئة تطوير محلية (local development environment) تحاكي الإنتاج؛ وtusd إن احتجت الرفع القابل للاستئناف على بنيتك التحتية (infrastructure).
- **ابنِ (Build):** الطبقة الرفيعة (thin layer) المهمة: جدول `file`، ونقطة نهاية التوقيع (signing endpoint) مع فحوص المصادقة (auth checks) والخطة، وتسمية المفاتيح (key naming)، والتحقق، ومهام التنظيف (cleanup jobs). هذا الجزء هو حدّك الأمني (security boundary)، لذلك امتلكه.

## 🔍 ادرسه في مشاريع حقيقية

**Documenso (`documenso/documenso`).** منتج SaaS للتوقيع الإلكتروني (e-signature)، ومنتجه كله ملفات PDF مرفوعة. استخدم بحث الكود عن `presign` و`upload` في المستودع الأحادي. يدعم أكثر من وسيلة نقل (transport) للرفع (التخزين في تخزين متوافق مع S3 (S3-compatible)، أو في قاعدة البيانات لإعدادات الاستضافة الذاتية البسيطة)، وهذا يوضح كيف تخفي التخزين خلف واجهة صغيرة.

**Papermark (`mfts/papermark`).** مشاركة مستندات مع تحليلات لكل مشاهد، لذلك يهتم كثيرًا بمن يحق له تنزيل ماذا. ابحث عن `upload` و`presigned` و`getFile` لترى كيف تُقدَّم المستندات الخاصة عبر روابط قصيرة العمر بدلًا من روابط عامة.

**Chatwoot (`chatwoot/chatwoot`).** تطبيق Rails يستخدم Active Storage لمرفقات المحادثات والصور الرمزية. افتح `config/storage.yml` لترى الخلفيات القابلة للتبديل (swappable backends) (محلي، وS3، وGCS، وAzure)، ثم ابحث عن `direct_upload` لترى مسار الرفع من المتصفح إلى الحاوية بمصطلحات (terms) Rails.

**ما الذي تلاحظه (What to notice):**

- أين يحدث فحص التفويض (authorization check) قبل توقيع (sign) الرابط، وكم يعيش الرابط.
- كيف تُبنى مفاتيح الكائنات (object keys)، وهل تتضمن معرّف الفريق أو المنظمة.
- ما البيانات الوصفية المخزّنة في قاعدة البيانات مقابل تلك المخزّنة على الكائن.
- كيف تعمل بيئة التطوير المحلية دون حاوية S3 حقيقية.
- ماذا يحدث للملفات عندما يُحذف السجل الأب (parent record).

## 🛠️ ابنِه في Beacon

### 🟢 تمرين المبتدئ

اسمح لمسؤولي المنظمة (org admins) برفع شعار صفحة الحالة. أنشئ جدول `file`، ونقطة نهاية تعيد رابط PUT موقّعًا لـ `orgs/{orgId}/logos/{fileId}`، ونقطة نهاية "complete" تعلّم الصف بأنه جاهز. شغّل SeaweedFS أو Garage أو حاوية R2 في الطبقة المجانية (free tier) كتخزين.

**يكتمل عندما (Done when):**

- لا تمر بايتات الملف عبر خادم تطبيقك أبدًا.
- لا يستطيع طلب رابط موقّع (signed URL) لمنظمة إلا مسؤولو تلك المنظمة.
- يُرفض رفع ملف بحجم 10 ميغابايت أو ملف `.exe` قبل إصدار أي رابط.

### 🟡 تمرين المستوى المتوسط

أضف لقطات شاشة للحوادث تكون خاصة بأعضاء المنظمة. يمر التنزيل عبر نقطة نهاية تتحقق من العضوية (membership) وتعيد التوجيه (redirect) إلى رابط GET موقّع لمدة 5 دقائق. بعد الرفع، اكتشف نوع المحتوى الحقيقي من البايتات وارفض عدم التطابق، وولّد صورة مصغرة (thumbnail) بعرض 400 بكسل في مهمة خلفية باستخدام `sharp`.

**يكتمل عندما (Done when):**

- يحصل مستخدم مسجّل الدخول (signed-in) من منظمة أخرى على 404 من نقطة نهاية التنزيل (download endpoint)، حتى مع معرّف ملف (file id) صالح.
- يُرفض ملف نصي أُعيدت تسميته إلى `.png` بعد الرفع ويُحذف كائنه.
- تُولَّد الصور المصغرة بشكل غير متزامن (asynchronously) وتعرض الواجهة حالة "قيد المعالجة".

### 🔴 تمرين المستوى المتقدم

طبّق إنهاء خدمة المنظمة (org offboarding) بالنسبة للملفات وأضف قواعد نظافة (hygiene rules). اكتب مهمة خلفية تحذف كل كائن تحت بادئة المنظمة (org prefix) على دفعات، إضافة إلى قواعد دورة حياة لـ `exports/` (7 أيام) وللرفع المجزّأ غير المكتمل (يوم واحد). أضف مهمة مطابقة (reconciliation job) ليلية تجد صفوف `pending` اليتيمة (orphaned) والكائنات التي لا صف لها.

**يكتمل عندما (Done when):**

- يزيل حذف منظمة اختبارية كل كائناتها، ويُتحقق من ذلك بسرد البادئة.
- تُعرَّف قواعد دورة الحياة في الكود (Terraform أو OpenTofu أو سكربت)، لا بالنقر في لوحة التحكم.
- تبلّغ مهمة المطابقة عن العناصر اليتيمة في الاتجاهين وتنظّفها.

## ⚠️ أخطاء يقع فيها المبتدئون

- **تمرير الملفات المرفوعة عبر خادم التطبيق (app server).** يُحجب العمال (workers) لدقائق، وترتفع الذاكرة، وتصطدم المنصات عديمة الخادم (serverless platforms) بحدود حجم الطلب. وقّع رابطًا ودع المتصفح يرفع مباشرة.
- **الثقة بـ `Content-Type` واسم الملف القادمين من المتصفح.** كلاهما تحت سيطرة المهاجم (attacker-controlled). استخدم قائمة مسموحات للأنواع، واكتشف النوع من البايتات بعد الرفع، وولّد المفاتيح بنفسك.
- **جعل الحاوية (bucket) كلها عامة كي "تعمل" الصور.** يصبح كل مرفق (attachment) خاص على بعد رابط مُخمَّن واحد من الإنترنت. أبقِ الحاويات خاصة واجعل الاستثناءات العامة صريحة.
- **تقديم ملفات SVG أو HTML يرفعها المستخدمون من نطاق تطبيقك (your app domain).** هذا XSS مخزَّن (stored XSS) يصل إلى ملفات تعريف الارتباط الخاصة بالجلسات (session cookies). استخدم نطاقًا منفصلًا لمحتوى المستخدمين (user content) و`Content-Disposition: attachment`.
- **روابط موقّعة (signed URLs) تعيش أسبوعًا.** تُلصق في Slack ويُعاد توجيهها. اجعلها دقائق، ووقّع رابطًا جديدًا لكل عرض.
- **نسيان الملفات عند حذف (delete) البيانات.** يختفي الصف ويبقى الكائن إلى الأبد، ويصبح جوابك عن GDPR خاطئًا. احذف الكائنات في مهمة خلفية وطابق بشكل منتظم.
- **ربط الكود بـ AWS بشكل ثابت (hard-code).** استخدم واجهة S3 مع نقطة نهاية قابلة للإعداد (configurable endpoint) كي تعمل بيئة التطوير المحلية وR2 وعملاء الاستضافة الذاتية.

## 🧾 الخلاصة

- البايتات تذهب إلى تخزين الكائنات، والبيانات الوصفية إلى Postgres، ويبقى خادم التطبيق خارج مسار البيانات (data path).
- الروابط الموقّعة مسبقًا تسمح للمتصفح بالرفع والتنزيل مباشرة، بعد أن يتحقق خادمك من الصلاحيات.
- تحقّق على الخادم قبل التوقيع ومرة أخرى بعد الرفع، وافحص كل ما يشاركه المستخدمون مع غيرهم.
- استخدم الرفع المجزّأ أو tus للملفات الكبيرة أو الاتصالات المتقطعة، وغيّر حجم الصور في مهام خلفية (background jobs) أو بوسيط صور خلف CDN.
- ضع بادئة المستأجر (tenant prefix) في المفاتيح، وأبقِ الحاويات خاصة، وأتمت الانتهاء (expiry) والحذف بقواعد دورة الحياة.

## ✍️ اختبر نفسك

**1. ما الرابط الموقّع مسبقًا (presigned URL)، ولماذا يبقي الملفات الكبيرة (large files) بعيدة عن خوادم تطبيقك (your app servers)؟**

<details><summary>الإجابة</summary>

هو رابط S3 عادي يحمل توقيعًا في سلسلة الاستعلام، ويسمح بعملية واحدة محددة (PUT أو GET على مفتاح واحد) حتى وقت انتهاء، دون أن تسلّم بيانات اعتمادك. يوقّعه خادمك بعد التحقق من الصلاحيات، ثم يتحدث المتصفح مع التخزين مباشرة، فلا تمر البايتات عبر تطبيقك أبدًا. راجع فقرة "الروابط الموقّعة مسبقًا" في 🟢 الأساسيات.

</details>

**2. ما الذي يُخزَّن في Postgres وما الذي يُخزَّن في الحاوية (bucket)؟**

<details><summary>الإجابة</summary>

الحاوية تخزّن البايتات. وPostgres يخزّن صف البيانات الوصفية في جدول `file`: المعرّف، وorganization_id، والمفتاح، ونوع المحتوى، والحجم، وuploaded_by، والحالة. تستخدم فحوص التفويض والواجهة هذا الصف؛ والمفتاح مجرد مؤشر. راجع 🟢 الأساسيات.

</details>

**3. يريد Beacon السماح لمسؤولي المنظمة (org admins) برفع شعار صفحة الحالة (status page logo). اذكر الفحوص (checks) قبل الرفع (upload) وبعده.**

<details><summary>الإجابة</summary>

قبل التوقيع، تحقّق من الجلسة (session) ودور المسؤول (admin role) وحدود الخطة (plan limits)، وافحص الحجم ونوع المحتوى المعلنين مقابل قائمة مسموحات (PNG أو JPEG، وحد أقصى 2 ميغابايت). بعد الرفع، نفّذ `HEAD` على الكائن لمعرفة حجمه الحقيقي، واقرأ البايتات الأولى لتأكيد نوعه الفعلي، ثم علّم الصف بأنه جاهز. والمفتاح تولّده أنت، مثل `orgs/{orgId}/logos/{fileId}`. راجع مخطط الرفع وفقرة "التحقق يحدث على الخادم، مرتين" في 🟡 التعمق أكثر.

</details>

**4. يغلق عميل لدى Beacon حسابه. كيف تتأكد من أن ملفاته زالت فعلًا؟**

<details><summary>الإجابة</summary>

لأن كل كائن يعيش تحت `orgs/{orgId}/`، تستطيع مهمة خلفية حذف البادئة كلها على دفعات. إن كانت إدارة إصدارات الحاوية مفعّلة، فيجب أن تزيل قاعدة دورة حياة الإصدارات غير الحالية أيضًا، ويجب أن تنظّف مهمة مطابقة الصفوف والكائنات اليتيمة. راجع فقرتي "بادئات مفاتيح لكل مستأجر" و"الحذف وGDPR" في 🔴 على نطاق واسع وللمؤسسات.

</details>

**5. يرفع مستخدم ملفًا اسمه `logo.svg` يحتوي سكربتًا (script)، ويقدّمه Beacon من `app.beacon.dev/uploads/logo.svg`. ما الذي يتعطل؟**

<details><summary>الإجابة</summary>

هذا XSS مخزَّن: يشغّل ملف SVG سكربتًا على نطاق تطبيقك ويصل إلى ملفات تعريف الارتباط الخاصة بجلسات مستخدميك. قدّم ملفات المستخدمين من نطاق منفصل مثل `beaconusercontent.com`، واستخدم `Content-Disposition: attachment` ما لم تحتج عرضها داخل الصفحة، ولا تسمح بـ SVG إلا بعد تنقيته (sanitising it). راجع فقرة "التحقق يحدث على الخادم، مرتين" في 🟡 التعمق أكثر.

</details>

## 📚 المراجع

- Amazon S3 documentation: https://docs.aws.amazon.com/s3/ — توثيق S3: الروابط الموقّعة والرفع المجزّأ ودورة الحياة (lifecycle) وحجب الوصول العام
- OWASP File Upload Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html — ورقة مرجعية (cheat sheet) لأمان رفع الملفات
- The tus resumable upload protocol: https://tus.io — بروتوكول الرفع القابل للاستئناف
- Uppy documentation: https://uppy.io/docs/
- Cloudflare R2 documentation: https://developers.cloudflare.com/r2/
- Garage documentation: https://garagehq.deuxfleurs.fr
- Rails Active Storage guide: https://guides.rubyonrails.org/active_storage_overview.html — دليل Active Storage في Rails

---

# 2.3 — البحث: من `LIKE '%x%'` إلى محرك بحث (search engine)
*المستوى: 🟡 متوسط (Intermediate)* · *المتطلبات: 2.1*

## ⚡ الدرس في دقيقة (In 60 seconds)

- البحث سُلَّم (ladder): `ILIKE`، ثم `pg_trgm`، ثم البحث النصي الكامل في Postgres، ثم محرك بحث، ثم البحث الهجين بالكلمات والمتجهات.
- الخيار الافتراضي للإصدار الأول (v1): ابقَ داخل Postgres. `pg_trgm` يتعامل مع الأسماء والأخطاء الإملائية (typos)، وعمود `tsvector` مع فهرس GIN يتعامل مع النصوص الطويلة (prose).
- القاعدة الأهم: فهرس البحث (search index) نسخة من بيانات المستأجرين، لذلك يجب تصفيته (filtered) حسب المستأجر بصرامة قاعدة البيانات نفسها، وبمرشّح (filter) لا يستطيع المتصفح إزالته.
- عندما تضيف محركًا مثل Meilisearch أو Typesense، غذّه عبر صندوق صادر وعامل خلفي (worker)، واحتفظ بإعادة فهرسة كاملة (full reindex) من Postgres، الذي يبقى مصدر الحقيقة (source of truth).
- الفخ الأكبر: أن تترك العميل (client) يرسل مرشّح المستأجر (tenant filter)، أو أن تنسى أن عمليات الحذف (deletes) يجب أن تصل إلى الفهرس أيضًا.

## 🧭 لماذا يحتاجه كل SaaS

أول مربع بحث (search box) في Beacon سطر كود (code) واحد: `WHERE name ILIKE '%' || $1 || '%'`. هذا مناسب لمستخدم لديه اثنا عشر مراقِبًا. ثم تشترك وكالة (agency) لديها 1,800 مراقِب بأسماء مثل `api-eu-west-checkout-prod`. يكتبون `checkout eu` فلا يحصلون على شيء، لأن الكلمتين غير متجاورتين. يكتبون `chekout` فلا يحصلون على شيء، لأن أحدًا لم يعلّم قاعدة البيانات عن الأخطاء الإملائية. ويريد قائد فريق الدعم (support lead) لديهم البحث في تحديثات الحوادث عن "certificate" عبر سنتين من التاريخ، فيستغرق الاستعلام ثماني ثوانٍ لأنه يمسح (scans) كل صف (every row).

ثم يطلب فريق المنتج (product team) لوحة أوامر (palette) cmd-K تبحث في المراقِبات والحوادث وصفحات الحالة وأعضاء الفريق (team members) وصفحات الإعدادات (settings pages) معًا، أثناء الكتابة، في أقل من 100 مللي ثانية.

وهناك فشل أهدأ. في اليوم الذي تضيف فيه محرك بحث مخصصًا، تكون قد أنشأت نسخة ثانية من بيانات عملائك خارج Postgres، بقواعد وصول (access rules) خاصة بها. إن لم يصفِّ فهرس البحث حسب المستأجر بصرامة قاعدة البيانات نفسها، يصبح مربع البحث أسهل طريق لتسريب البيانات بين المستأجرين (cross-tenant leak) في تطبيقك.

**البحث (search) سُلَّم (ladder): اصعده درجة (rung) درجة، وابدأ داخل Postgres، وعامل كل فهرس بحث (search index) على أنه نسخة من بيانات المستأجرين (tenant data) يجب تصفيتها ومزامنتها (kept in sync) بعناية قاعدة البيانات (database) نفسها.**

## 📐 كيف يعمل

### 🟢 الأساسيات

بعض المصطلحات أولًا. **الاستدعاء (Recall)** يعني هل تظهر النتائج الصحيحة أصلًا؛ و**الملاءمة (Relevance)** أو الترتيب (ranking) تعني هل تظهر بالترتيب الصحيح. **المُقطِّع (Tokenizer)** يقسم النص إلى مصطلحات ("api-eu-west" تصبح `api` و`eu` و`west`). **التجذيع (Stemming)** يردّ الكلمات إلى جذرها، فتطابق "failing" الكلمة "failed". **الفهرس المقلوب (Inverted Index)** يربط كل مصطلح بقائمة الصفوف التي تحتويه، وهذا ما يجعل البحث سريعًا: بدلًا من قراءة كل صف، تبحث عن المصطلح (term).

هذا هو السلّم الذي تصعده أغلب منتجات SaaS:

```mermaid
flowchart RL
    A["ILIKE<br/>مسح للنصوص الجزئية<br/>(ILIKE<br/>substring scan)"] --> B["pg_trgm<br/>تقريبي ومفهرس<br/>(pg_trgm<br/>fuzzy and indexed)"]
    B --> C["البحث النصي الكامل في Postgres<br/>tsvector والترتيب<br/>(Postgres full-text<br/>tsvector and ranking)"]
    C --> D["محرك بحث<br/>Meilisearch وTypesense وOpenSearch<br/>(Search engine<br/>Meilisearch, Typesense, OpenSearch)"]
    D --> E["هجين<br/>كلمات مع متجهات<br/>(Hybrid<br/>keywords plus vectors)"]
```

**الدرجة 1 (Rung 1): `ILIKE`.** مطابقة لنص جزئي دون تمييز حالة الأحرف. لا يستطيع أي فهرس B-tree (B-tree index) عادي مساعدة نمط يبدأ بحرف بدل (Wildcard)، لذلك يحدث مسح. هذا مقبول للجداول الصغيرة إذا صُفّيت حسب `organization_id` أولًا (يضيّق Postgres النطاق إلى 50 مراقِبًا لمنظمة واحدة، ثم يمسحها). احتفظ دائمًا بمرشّح المستأجر هذا.

**الدرجة 2 (Rung 2): `pg_trgm`.** إضافة مرفقة (bundled extension) مع Postgres تقسم النص إلى ثلاثيات حروف (Trigrams)، أي قطع من ثلاثة أحرف: "check" تحتوي `che` و`hec` و`eck`، إضافة إلى ثلاثيات مبطّنة (padded) لأطراف الكلمة. مع فهرس GIN (GIN index) أو GiST على هذه الثلاثيات، يصبح `ILIKE '%checkout%'` مدعومًا بالفهرس (index-assisted)، ويجد عامل التشابه (similarity operator) `%` الأخطاء القريبة (near-misses) مثل "chekout". هذه أفضل درجة في السلّم من حيث القيمة مقابل الجهد للأسماء والمعرّفات النصية (Slugs) وعناوين البريد (emails) والروابط.

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX monitor_name_trgm_idx
  ON monitor USING gin (name gin_trgm_ops);

SELECT id, name, similarity(name, $2) AS score
FROM monitor
WHERE organization_id = $1 AND name % $2
ORDER BY score DESC
LIMIT 10;
```

**الدرجة 3 (Rung 3): البحث النصي الكامل (full-text search) في Postgres.** للنصوص الطويلة (تحديثات الحوادث، وتقارير ما بعد الحوادث (postmortems)، والملاحظات)، يحوّل Postgres النص إلى `tsvector`: قائمة مرتبة من المصطلحات المجذّعة (stemmed terms) مع مواضعها (positions). وتصبح الاستعلامات `tsquery`. تقبل `websearch_to_tsquery('english', 'certificate -staging')` صيغة (syntax) شبيهة بـ Google، وترتّب `ts_rank` النتائج، وتبرز (highlights) `ts_headline` المطابقات (matches). خزّن المتجه في عمود مولَّد (generated column) مع فهرس GIN:

```sql
ALTER TABLE incident_update ADD COLUMN search tsvector
  GENERATED ALWAYS AS (to_tsvector('english', coalesce(body, ''))) STORED;
CREATE INDEX incident_update_search_idx ON incident_update USING gin (search);
```

في Rails توجد `pg_search`، وفي Django توجد `django.contrib.postgres.search`، وكل باني استعلامات في TypeScript يستطيع استدعاء هذه الدوال (functions) مباشرة.

### 🟡 التعمق أكثر

**ما لا يستطيع بحث (search) Postgres فعله بسهولة.** لا يتسامح مع الأخطاء الإملائية (typo tolerance) في استعلامات النص الكامل (الثلاثيات تساعد في الحقول القصيرة (short fields) فقط)، والبحث ببادئة (prefix search) كل كلمة أثناء الكتابة مرهق، وضبط الملاءمة (relevance tuning) يدوي، والتصنيف بالأوجه (Faceting)، أي العدّ لكل فئة: "12 متوقف، 40 يعمل، 3 موقوف مؤقتًا"، بطيء نسبيًا على مجموعات النتائج (result sets) الكبيرة. عند نقطة ما ستريد **محرك بحث (search engine)**: خدمة منفصلة (separate service) مبنية حول الفهارس المقلوبة (inverted indexes)، مع التسامح مع الأخطاء الإملائية، ومطابقة البادئات (prefix matching)، والأوجه (facets)، والمرادفات (synonyms)، والإبراز (highlighting) جاهزة.

| الخيار | نقاط القوة (Strengths) | المقايضات (Trade-offs) | الاستخدام المعتاد (Typical fit) |
|---|---|---|---|
| `pg_trgm` + النص الكامل (full-text) في Postgres | لا بنية تحتية جديدة (infra)، ومعاملاتي (transactional)، والصلاحيات نفسها | تسامح ضعيف مع الأخطاء الإملائية، وملاءمة يدوية | أغلب منتجات SaaS في أول سنة أو سنتين |
| Meilisearch | فوري، ومتسامح مع الأخطاء (typo-tolerant)، وواجهة بسيطة، ورموز المستأجرين (tenant tokens) | تركيز على العقدة الواحدة (single-node)، وليس لبيانات بحجم السجلات (log-scale) | البحث داخل التطبيق (in-app search) وcmd-K |
| Typesense | سريع، ومتسامح مع الأخطاء، ومفاتيح API محددة النطاق (scoped API keys)، وعنقدة مدمجة (built-in clustering) | يجب أن تتسع البيانات في الذاكرة (RAM) | البحث داخل التطبيق مع حاجة للتوافر العالي (HA) |
| OpenSearch / Elasticsearch | نطاق ضخم (scale)، وتجميعات (aggregations)، وسجلات، ومرونة كبيرة | ثقيل تشغيليًا (operationally heavy)، وضبط JVM | مجموعات بيانات كبيرة (large datasets)، وبحث بطابع تحليلي (analytics-style) |
| ParadeDB (`pg_search`) | ترتيب BM25 داخل Postgres، دون مسار مزامنة (sync pipeline) | أحدث عهدًا، وإضافة يجب أن يُسمح لك بتثبيتها | تريد جودة محرك بحث دون مغادرة Postgres |
| Algolia / Elastic Cloud | مُدار بالكامل (fully managed)، وأدوات ملاءمة ممتازة | تسعير (pricing) لكل سجل ولكل عملية بحث (per search) | فرق تريد شراء البحث |

**مسارات الفهرسة (Indexing Pipelines).** مع محرك خارجي (external engine)، يجب أن يصل كل تغيير في Postgres إلى الفهرس. هناك ثلاث طرق، من الأبسط إلى الأمتن:

1. **المزامنة عند الكتابة (sync on write).** بعد حفظ مراقِب، استدعِ `index.addDocuments(...)` داخل الطلب. هذا بسيط، لكن إن فشل استدعاء البحث ينحرف (drifts) الفهرس بصمت، ويبطئ كل عملية كتابة.
2. **صندوق الصادر مع عامل خلفي (outbox plus worker).** في المعاملة نفسها التي تكتب فيها، أدرج صفًا في جدول `outbox` (الدرس 2.1). يقرأه عامل خلفي ويحدّث الفهرس، ويعيد المحاولة (retrying) عند الفشل. هذا هو الخيار الافتراضي الصحيح.
3. **التقاط تغييرات البيانات (CDC).** أداة مثل Debezium تقرأ تدفق النسخ المنطقي في Postgres وتصدر كل تغيير في الصفوف إلى طابور، يستهلكه مُفهرِس (indexer). لا يستطيع أي كود في التطبيق أن ينسى إصدار حدث (event)، لكنك الآن تشغّل بنية تحتية أكثر.

```mermaid
flowchart RL
    APP["واجهة Beacon البرمجية<br/>(Beacon API)"] -->|"معاملة واحدة (one transaction)"| PG[("Postgres<br/>monitor + outbox")]
    PG --> W["عامل الفهرسة<br/>(Indexer worker)"]
    W --> SE[("محرك البحث<br/>(Search engine)")]
    W -.->|"إعادة المحاولة عند الفشل (retry on failure)"| W
    J["مهمة إعادة الفهرسة الليلية<br/>(Nightly reindex job)"] --> SE
    UI["لوحة أوامر cmd-K<br/>(cmd-K palette)"] -->|"مفتاح محدد بالمستأجر (tenant-scoped key)"| SE
```

أيًّا كان اختيارك، أضف مهمة **إعادة فهرسة كاملة (full reindex)** تعيد بناء الفهرس من Postgres (ويُفضَّل في فهرس جديد، ثم تبديل اسم مستعار). ستحتاجها بعد كل تغيير في التعيينات (mapping) وبعد كل خطأ سبّب انحرافًا. يبقى Postgres مصدر الحقيقة؛ والفهرس قابل للرمي (disposable).

**تصفية المستأجر (tenant filtering) ضابط أمني (security control)، وليست ميزة.** في Postgres تضيف طبقة الوصول إلى البيانات `organization_id = $1`. وفي محرك البحث يجب أن تفعل الشيء نفسه، ويجب ألا تسمح للمتصفح باختيار المرشّح. لكل محرك آلية لذلك: **رموز المستأجرين (Tenant Tokens)** في Meilisearch، و**مفاتيح API محددة النطاق (Scoped API Keys)** في Typesense، و**مفاتيح API المؤمَّنة (Secured API Keys)** في Algolia، وكلها تضمّن مرشّحًا إلزاميًا (mandatory filter) مثل `organization_id = org_123` داخل مفتاح موقّع (signed key) يولّده خادمك لكل مستخدم. يستطيع المتصفح الاستعلام من المحرك مباشرة للسرعة، لكنه لا يستطيع إزالة المرشّح. وإن مرّرت (proxy) البحث عبر واجهتك البرمجية بدلًا من ذلك، فأضف المرشّح على الخادم، دائمًا. وافهرس فقط ما يُسمح للمستخدم برؤيته: إن كان حقل ما خاصًا بالمسؤولين (admins)، فإما أن تتركه خارج الفهرس المشترك (shared index) أو أن تصفّي على سمة الدور (role attribute) أيضًا.

**تجربة المستخدم في البحث (search UX).** أخّر معالجة ضغطات المفاتيح (Debounce) بنحو 150 مللي ثانية، وابحث بالبادئات، وأبرز النص المطابق، واعرض نوع الكائن (object type) والمنظمة في كل نتيجة، وضع عناصر "الأخيرة" و"التنقل" (الإعدادات، والفوترة) أولًا عندما يكون المربع فارغًا. حزمة React الشائعة `cmdk` تتولى سلوك لوحة المفاتيح (keyboard) في اللوحة؛ والنتائج تأتي من واجهتك البرمجية أو من المحرك.

### 🔴 على نطاق واسع وللمؤسسات

**ضبط الملاءمة (relevance tuning).** يحكم المستخدمون الحقيقيون على البحث من أول ثلاث نتائج. احتفظ بقائمة صغيرة من الاستعلامات الحقيقية مع النتائج الأولى المتوقعة لكل منها ("مجموعة ذهبية (golden set)") وافحصها بعد كل تغيير في الترتيب. ارفع وزن المطابقات الدقيقة (exact matches) للاسم فوق مطابقات الوصف، والحوادث الحديثة فوق القديمة. سجّل الاستعلامات التي لا تعيد نتائج (zero-result queries): فهي تخبرك بالمرادفات التي يجب إضافتها.

**البحث الدلالي والهجين (semantic and hybrid search).** يفشل البحث بالكلمات المفتاحية (keyword search) عندما يصف المستخدمون المعنى بدل الكلمات: "why was checkout slow last Tuesday" لا تشترك في مصطلحات كثيرة مع حادثة عنوانها "Elevated p95 latency on payments API". **التضمينات (Embeddings)** متجهات ينتجها نموذج (model) بحيث تقع المعاني المتشابهة قرب بعضها؛ و**البحث المتجهي (Vector Search)** يجد أقرب الجيران (nearest neighbours). يضيف `pgvector` نوع عمود متجهي وفهارس لأقرب الجيران التقريبية (HNSW وIVFFlat) إلى Postgres؛ وتوجد قواعد بيانات متجهية (vector databases) مخصصة مثل Qdrant للمجموعات الكبيرة جدًا، كما يدعم Meilisearch وTypesense وOpenSearch وElasticsearch المتجهات (vectors) أيضًا. الفائز العملي هو **البحث الهجين (Hybrid Search)**: شغّل البحث بالكلمات والبحث المتجهي، ثم ادمج القائمتين المرتبتين (ranked lists)، مثلًا بدمج الرتب المتبادلة (Reciprocal Rank Fusion)، أي جمع `1 / (k + rank)` لكل مستند عبر القوائم. وهذا يشغّل أيضًا ملخصات الحوادث بالذكاء الاصطناعي في Beacon (الدرس 8.2)، حيث جودة الاسترجاع (retrieval quality) هي كل شيء.

**فهارس لكل مستأجر (per-tenant indexes) مقابل فهرس مشترك (versus shared index).** الفهرس المشترك مع مرشّح المستأجر هو الأبسط والأكفأ. الفهرس لكل مستأجر (per-tenant index) يعطي عزلًا أقوى، وإعدادات ملاءمة لكل مستأجر، وحذفًا سهلًا، لكن آلاف الفهارس الصغيرة ترهق أغلب المحركات (engines). الحل الوسط الشائع: فهرس مشترك للذيل الطويل (long tail)، وفهارس مخصصة لعملاء المؤسسات القلائل الذين يدفعون مقابلها (وهو الاختيار نفسه بين المجمّع والصومعة الذي يغطيه الدرس 2.4).

**الحذف وإقامة البيانات (deletion and residency).** عندما يُحذف سجل، أو يستخدم مستخدم حقه في المحو (erasure) وفق GDPR، يجب تحديث فهرس البحث أيضًا؛ واختبر ذلك. عناقيد البحث (search clusters) مخازن بيانات (data stores) في منطقة معينة، لذلك مكان بيانات مستأجري (tenants) الاتحاد الأوروبي عنقود (cluster) أوروبي، ويجب أن تتضمن إجاباتك عن استبيانات الأمان (security questionnaires) مزوّد البحث (search provider) بوصفه معالجًا فرعيًا (Subprocessor).

**السعة (capacity).** المحركات التي تحتفظ بالفهارس في الذاكرة (Typesense، وMeilisearch إلى حد كبير) تحتاج ذاكرة تتناسب مع حجم البيانات. لا تفهرس البيانات عالية الحجم مثل نتائج الفحص الخام في Beacon؛ فهرس المراقِبات والحوادث والتحديثات والأشخاص. السجلات والأحداث مكانها مخزن للمراقبة التشغيلية (observability) (الدرس 7.2).

## 🏆 أفضل المستودعات

| المستودع | ما هو | التقنيات | الترخيص | اختره عندما |
|---|---|---|---|---|
| [meilisearch/meilisearch](https://github.com/meilisearch/meilisearch) | محرك بحث فوري متسامح مع الأخطاء الإملائية مع رموز المستأجرين | Rust | MIT; Enterprise Edition parts BUSL-1.1 | تريد أفضل تجربة بحث داخل التطبيق بأقل ضبط |
| [typesense/typesense](https://github.com/typesense/typesense) | بحث في الذاكرة متسامح مع الأخطاء مع مفاتيح API محددة النطاق وعنقدة (clustering) | C++ | GPL-3.0 | تريد بحثًا شبيهًا بـ Algolia تستضيفه بنفسك مع توافر عالٍ (high availability) |
| [opensearch-project/OpenSearch](https://github.com/opensearch-project/OpenSearch) | تفرّع مجتمعي (community fork) من Elasticsearch، مشروع تابع لـ Linux Foundation | Java | Apache-2.0 | مجموعات بيانات كبيرة، أو تجميعات، أو تعمل على AWS |
| [elastic/elasticsearch](https://github.com/elastic/elasticsearch) | محرك البحث والتحليل الموزّع الأصلي | Java | AGPL-3.0 / SSPL / ELv2 (choice) | تحتاج منظومته (ecosystem) أو تستخدم Elastic Cloud |
| [paradedb/paradedb](https://github.com/paradedb/paradedb) | بحث نصي كامل بترتيب BM25 كإضافة لـ Postgres (Postgres extension) | Rust | AGPL-3.0 | تريد ترتيبًا بجودة محرك بحث دون مسار مزامنة |
| [pgvector/pgvector](https://github.com/pgvector/pgvector) | نوع متجهي (vector type) وفهارس ANN لـ Postgres | C | PostgreSQL | تضيف بحثًا دلاليًا (semantic search) أو هجينًا وتريد البقاء في Postgres |
| [quickwit-oss/tantivy](https://github.com/quickwit-oss/tantivy) | مكتبة بحث نصي كامل، المقابل في Rust لـ Lucene | Rust | MIT | تريد فهم طريقة عمل محرك قائم على الفهرس المقلوب |
| [debezium/debezium](https://github.com/debezium/debezium) | التقاط تغييرات البيانات (change data capture) من Postgres وMySQL وغيرهما | Java | Apache-2.0 | يتجاوز مسار الفهرسة (indexing pipeline) لديك نمط صندوق الصادر |

**إن درست مستودعًا واحدًا فقط (If you study one repo):** Meilisearch. اقرأ توثيقه عن رموز المستأجرين والسمات القابلة للتصفية (filterable attributes) والتسامح مع الأخطاء الإملائية، ثم شغّله محليًا وافهرس مراقِبات Beacon في فترة بعد الظهر. سيريك كيف يبدو البحث "الجيد" داخل التطبيق، وهو المعيار الذي تقيس Postgres عليه.

**اشترِ أم ابنِ أم استضف بنفسك ⁦(Buy, build, or self-host?)⁩؟**

- **اشترِ (Buy):** Algolia أو Elastic Cloud أو Meilisearch Cloud أو Typesense Cloud عندما يكون البحث محوريًا في المنتج ولا أحد يريد امتلاك عنقود. خطّط للميزانية بعناية؛ فالتسعير يتصاعد مع عدد السجلات والاستعلامات.
- **استضف بنفسك (Self-host):** Meilisearch أو Typesense لأغلب منتجات SaaS، وOpenSearch عندما تكون البيانات كبيرة أو تحتاج التجميعات؛ وParadeDB إن أردته داخل Postgres.
- **ابنِ (Build):** المسار (صندوق الصادر، والعامل، وإعادة الفهرسة)، وإصدار المفاتيح المحددة بالمستأجر، وواجهة cmd-K. لا تبنِ المحرك أبدًا. ولا تضف محركًا على الإطلاق حتى يستنفد `pg_trgm` والبحث النصي الكامل قدرتهما بشكل واضح.

## 🔍 ادرسه في مشاريع حقيقية

**Discourse (`discourse/discourse`).** مثال ناضج على البحث النصي الكامل في Postgres في الإنتاج وعلى نطاق واسع. استخدم بحث الكود عن `ts_rank` و`to_tsvector` و`search_data` لتجد كيف تُفهرس المنشورات (posts) في جداول بحث مخصصة، وكيف يعطي الترتيب العناوين وزنًا أعلى من المتن (body)، وكيف تُعالَج اللغات المتعددة.

**Mastodon (`mastodon/mastodon`).** بحث نصي كامل اختياري عبر Elasticsearch أو OpenSearch باستخدام جوهرة Chewy. انظر في `app/chewy` (وقت كتابة هذا الدرس) لتعريفات الفهارس، ثم ابحث عن `update_index` لترى كيف تتدفق تغييرات النماذج (model changes) إلى الفهرس، واقرأ مهام (jobs) إعادة الفهرسة (reindex) في توثيق سطر أوامر الإدارة (admin CLI).

**Twenty (`twentyhq/twenty`).** نظام CRM يمتد بحثه عبر الأشخاص والشركات والكائنات المخصصة (custom objects). استخدم بحث الكود عن `tsvector` و`searchVector` لترى كيف تبقي قاعدة كود (codebase) حديثة بـ TypeScript البحث داخل Postgres، حتى مع حقول يعرّفها المستخدم (user-defined fields).

**ما الذي تلاحظه (What to notice):**

- هل يعيش البحث في Postgres أم في محرك خارجي، وما الذي دفعهم إلى ذلك.
- كيف تصل المستندات إلى الفهرس: داخل الطلب، أو عبر مهام خلفية، أو بعملية مزامنة (sync).
- كيف تُصفّى النتائج حسب الصلاحيات، لا حسب المستأجر فقط.
- كيف تُطلق إعادة الفهرسة الكاملة وكم يتوقعون أن تستغرق.
- ما الحقول التي تحصل على وزن أعلى في الترتيب.

## 🛠️ ابنِه في Beacon

### 🟢 تمرين المبتدئ

أضف بحث المراقِبات إلى لوحة تحكم Beacon باستخدام `pg_trgm`. فهرس `name` و`url`، ورتّب حسب التشابه (similarity)، وصفِّ دائمًا حسب المنظمة الحالية.

**يكتمل عندما (Done when):**

- تجد "chekout" مراقِبًا اسمه "checkout-api".
- يُظهر `EXPLAIN ANALYZE` استخدام فهرس الثلاثيات (trigram index) على بيانات بذر من 50,000 مراقِب.
- يثبت اختبار (test) أن المستخدم لا يتلقى أبدًا مراقِبات منظمة أخرى، حتى مع أسماء متطابقة.

### 🟡 تمرين المستوى المتوسط

أضف بحثًا نصيًا كاملًا في تحديثات الحوادث باستخدام عمود `tsvector` مولَّد، و`websearch_to_tsquery`، والترتيب، ومقتطفات (snippets) مع إبراز، ثم ابنِ لوحة أوامر (command palette) cmd-K تستعلم عن المراقِبات والحوادث وصفحات الإعدادات في استدعاء واحد.

**يكتمل عندما (Done when):**

- يتصرف `"certificate expired" -staging` مثل استعلام بحث على الويب.
- تعرض النتائج مقتطفًا (snippet) مع إبراز ونوع الكائن.
- يمكن استخدام اللوحة بلوحة المفاتيح وحدها، وتستجيب في أقل من 150 مللي ثانية محليًا.

### 🔴 تمرين المستوى المتقدم

انقل البحث إلى Meilisearch أو Typesense مع مُفهرِس يعمل عبر صندوق الصادر، وإعادة فهرسة ليلية في فهرس جديد يُبدَّل ذريًا (atomic swap). يستعلم المتصفح من المحرك مباشرة باستخدام رمز مستأجر (tenant token) أو مفتاح محدد النطاق (scoped key) تصدره واجهتك البرمجية مع مرشّح `organization_id` إلزامي.

**يكتمل عندما (Done when):**

- لا يضيع أي تحديث عند إيقاف محرك البحث لمدة خمس دقائق؛ ويلحق (catches up) العامل بما فاته.
- يعيد العبث بالمرشّح (tampering) في المتصفح نتائج منظمة المستخدم فقط.
- يؤدي حذف حادثة إلى إزالتها من البحث خلال دقيقة.

## ⚠️ أخطاء يقع فيها المبتدئون

- **القفز إلى Elasticsearch من اليوم الأول.** أنت الآن تشغّل عنقودًا ومسار مزامنة للبحث في 300 صف. اصعد السلّم: `pg_trgm` والبحث النصي الكامل يغطيان أغلب منتجات SaaS لوقت طويل.
- **ترك العميل (letting the client) يرسل مرشّح المستأجر (tenant filter).** يستطيع أي شخص تعديل الطلب. استخدم رموز المستأجرين أو المفاتيح محددة النطاق (scoped keys)، أو أضف المرشّح على الخادم.
- **الفهرسة (indexing) داخل مسار الطلب (request path) دون إعادة محاولة.** استدعاء واحد فاشل وينحرف الفهرس إلى الأبد. استخدم صندوق صادر وعاملًا خلفيًا، إضافة إلى مهمة إعادة فهرسة.
- **معاملة (transaction) الفهرس (index) على أنه مصدر الحقيقة (source of truth).** الفهارس تتلف، والتعيينات (mappings) تتغير، والمحركات تُستبدل. كن قادرًا دائمًا على إعادة البناء من Postgres.
- **نسيان عمليات الحذف (deletion).** تستمر السجلات المحذوفة والممحوة وفق GDPR في الظهور في البحث. اختبر أن الحذف يصل إلى الفهرس.
- **فهرسة (indexing) كل شيء.** نتائج الفحص الخام أو السجلات تضخّم الذاكرة والتكلفة (cost). فهرس ما يبحث عنه الناس فعلًا.

## 🧾 الخلاصة

- البحث سُلَّم: `ILIKE`، ثم `pg_trgm`، ثم النص الكامل في Postgres، ثم محرك بحث، ثم الهجين (hybrid) مع المتجهات.
- يأخذك Postgres بعيدًا، دون مشكلة مزامنة ومع الصلاحيات نفسها التي تحكم بقية بياناتك.
- الفهرس الخارجي نسخة من بيانات المستأجرين: صفِّه بمفاتيح موقّعة محددة بالمستأجر، وأبقه متزامنًا عبر صندوق الصادر أو CDC.
- احتفظ دائمًا بمسار لإعادة الفهرسة الكاملة؛ فـ Postgres هو مصدر الحقيقة.
- البحث الهجين بالكلمات والمتجهات هو الخيار الافتراضي الحديث للاستعلامات باللغة الطبيعية (natural-language) وميزات الذكاء الاصطناعي (AI features).

## ✍️ اختبر نفسك

**1. ما الفهرس المقلوب (inverted index)، ولماذا يجعل البحث (search) سريعًا؟**

<details><summary>الإجابة</summary>

يربط كل مصطلح بقائمة الصفوف التي تحتويه. بدلًا من قراءة كل صف، يبحث المحرك عن المصطلح ويحصل على الصفوف المطابقة مباشرة. راجع 🟢 الأساسيات.

</details>

**2. ماذا تضيف إضافة `pg_trgm`، وما أنسب استخداماتها؟**

<details><summary>الإجابة</summary>

تقسم النص إلى ثلاثيات حروف (قطع من ثلاثة أحرف). مع فهرس GIN أو GiST يصبح `ILIKE '%checkout%'` مدعومًا بالفهرس، ويجد عامل التشابه `%` الأخطاء القريبة مثل "chekout". أنسب استخداماتها الحقول القصيرة: الأسماء، والمعرّفات النصية، وعناوين البريد، والروابط. راجع فقرة "الدرجة 2 (Rung 2)" في 🟢 الأساسيات.

</details>

**3. يريد قائد فريق الدعم (support lead) في Beacon البحث (search) في سنتين من تحديثات الحوادث (incident updates) عن "certificate". أي درجة (rung) في السلّم (ladder) تناسب ذلك، وكيف تجهّزها؟**

<details><summary>الإجابة</summary>

البحث النصي الكامل في Postgres، لأن هذا نص طويل. أضف عمود `tsvector` مولَّدًا على `incident_update` مع فهرس GIN، واستعلم عنه بـ `websearch_to_tsquery`، ورتّب بـ `ts_rank`، وأبرز المطابقات بـ `ts_headline`. راجع فقرة "الدرجة 3 (Rung 3)" في 🟢 الأساسيات.

</details>

**4. ينقل Beacon بحث (search) المراقِبات (monitors) إلى Meilisearch. كيف تبقي الفهرس (index) متزامنًا (in sync) مع Postgres؟**

<details><summary>الإجابة</summary>

في المعاملة نفسها التي تكتب فيها، أدرج صفًا في جدول `outbox`، ودع عاملًا خلفيًا يحدّث الفهرس ويعيد المحاولة عند الفشل. أضف مهمة إعادة فهرسة كاملة تبني فهرسًا جديدًا وتبدّل اسمًا مستعارًا (alias)، لتغييرات التعيينات وحالات الانحراف (drift). يبقى Postgres مصدر الحقيقة. راجع فقرة "مسارات الفهرسة" في 🟡 التعمق أكثر.

</details>

**5. تستعلم لوحة أوامر (command palette) cmd-K في Beacon من محرك البحث (search engine) مباشرة من المتصفح، ويتضمن الطلب (request) `filter: "organization_id = org_123"`. ما الذي يتعطل؟**

<details><summary>الإجابة</summary>

يستطيع أي شخص تعديل الطلب، فيغيّر المرشّح أو يزيله، ويقرأ مراقِبات منظمة أخرى وحوادثها: تسريب بين المستأجرين عبر مربع البحث. يجب أن يصدر خادمك لكل مستخدم رمز مستأجر أو مفتاح API محدد النطاق يتضمن مرشّح `organization_id` الإلزامي موقّعًا بداخله، أو أن يضيف المرشّح على الخادم إن كان البحث يمر عبر واجهتك البرمجية. راجع فقرة "تصفية المستأجر ضابط أمني، وليست ميزة" في 🟡 التعمق أكثر.

</details>

## 📚 المراجع

- PostgreSQL full-text search chapter: https://www.postgresql.org/docs/current/textsearch.html — فصل البحث النصي الكامل
- PostgreSQL `pg_trgm` module: https://www.postgresql.org/docs/current/pgtrgm.html — وحدة الثلاثيات
- Meilisearch documentation: https://www.meilisearch.com/docs — تعدد المستأجرين (multi-tenancy) ورموز المستأجرين
- Typesense documentation: https://typesense.org/docs/ — مفاتيح API محددة النطاق
- ParadeDB documentation: https://docs.paradedb.com
- pgvector README: https://github.com/pgvector/pgvector
- Debezium documentation: https://debezium.io/documentation/

---

# 2.4 — تعمّق في تعدد المستأجرين: العزل والجيران المزعجون (noisy neighbours) وإقامة البيانات (data residency)
*المستوى: 🔴 متقدم (Advanced)* · *المتطلبات: 1.2، 1.3، 2.1*

## ⚡ الدرس في دقيقة (In 60 seconds)

- تعدد المستأجرين طيف من العزل: المجمّع (Pool) أي جداول مشتركة (shared tables)، والجسر (Bridge) أي مخطط لكل مستأجر (schema per tenant)، والصومعة (Silo) أي قاعدة بيانات أو بنية كاملة لكل مستأجر.
- الخيار الافتراضي للإصدار الأول (v1 default): المجمّع، مع `organization_id` في كل جدول يملكه مستأجر (tenant table)، وطبقة وصول إلى البيانات محددة بالمستأجر كي تكون التصفية جزءًا من البنية (structural) لا شيئًا يتذكره المطوّر.
- القاعدة الأهم: النظام هو من يفرض حدود المستأجر (دوال مساعدة محددة النطاق (scoped helpers)، والتحميل عبر الأب (load-through-parent)، وإعادة 404، واختبارات لكل مسار (per-route tests)، وأمان مستوى الصف (RLS) في Postgres كدفاع إضافي).
- يجب أن يتدفق سياق المستأجر (tenant context) عبر المهام الخلفية والكاش (caches) والسجلات والبحث، لا عبر معالجات HTTP (HTTP handlers) وحدها.
- الفخ الأكبر: جلب كائن بمعرّفه وحده، وهذا هو التسريب بين المستأجرين الذي ينتظر أن يحدث.

## 🧭 لماذا يحتاجه كل SaaS

يتلقى مهندس دعم (support engineer) في Beacon رسالة من عميل: "لماذا أرى حادثة اسمها 'Payments DB failover' في لوحة التحكم عندي؟ ليس لدينا قاعدة بيانات للمدفوعات." الحادثة تخص شركة أخرى. السبب شرط واحد ناقص (missing clause): نقطة نهاية جديدة، `GET /api/incidents/:id`، حمّلت الحادثة بمعرّفها ونسيت `AND organization_id = $2`. جاء المعرّف من رابط مشترك (shared link). لم يخترق (hacked) أحد شيئًا؛ كل ما في الأمر أن مطوّرًا كتب استعلامًا يبدو عاديًا.

هذا هو **التسريب بين المستأجرين (Cross-Tenant Leak)**، فئة الأخطاء (bug class) التي تحدد البرمجيات متعددة المستأجرين (multi-tenant software). إنه مرجع مباشر غير آمن للكائن (IDOR) بأسوأ نطاق ضرر (blast radius) ممكن: ليست بيانات مستخدم واحد، بل بيانات *عميل* آخر. ويحدث أيضًا في طبقة البنية التحتية (infrastructure layer): في 2021 كشف باحثون في Wiz عن "ChaosDB"، وهي ثغرة (flaw) في ميزة الدفاتر (Notebooks) في Azure Cosmos DB كان يمكن أن تسمح لعميل بالحصول على مفاتيح قواعد بيانات عملاء آخرين. أخطاء تعدد المستأجرين تعيش في كل طبقة.

بعد أسبوعين، يرسل عميل محتمل (prospect) لخطة Business استبيانًا أمنيًا (security questionnaire): "صِف كيف تُعزل بياناتنا منطقيًا وفيزيائيًا عن العملاء الآخرين (other customers). هل يمكن تخزين بياناتنا حصريًا في الاتحاد الأوروبي؟ هل يمكن أن نحصل على نسخة مخصصة (dedicated instance)؟" وفي الوقت نفسه ينشئ مستخدم في الخطة المجانية (Free-plan) 3,000 مراقِب بسكربت، فيتأخر مجدول الفحوص (check scheduler) على الجميع.

أعطى الدرس 1.2 منظماتٍ (orgs) لـ Beacon. وهذا الدرس عن جعل الحدود بينها صامدة أمام الأخطاء البرمجية والحمل (load) والجهات التنظيمية (regulators) وعقود المؤسسات (enterprise contracts).

**تعدد المستأجرين (multi-tenancy) طيف من العزل (spectrum of isolation) تختاره لكل فئة (tier) من المستأجرين (tenants)، وأيًّا كان اختيارك يجب أن يفرض النظامُ حدود المستأجر (tenant boundary)، لا أن يتذكرها كل مطوّر.**

## 📐 كيف يعمل

### 🟢 الأساسيات

**المستأجر (Tenant)** هو وحدة العميل (customer unit) التي تملك البيانات: في Beacon هو المنظمة. و**متعدد المستأجرين (Multi-tenant)** يعني أن مستأجرين كثيرين يتشاركون نظامًا واحدًا قيد التشغيل (running system). تسمّي إرشادات AWS لـ SaaS ثلاثة نماذج للمشاركة، وأصبحت هذه المفردات معيارًا:

| النموذج | يسمى أيضًا (Also called) | كيف تُفصل البيانات | العزل | التكلفة لكل مستأجر | العبء التشغيلي (operational load) |
|---|---|---|---|---|---|
| **المجمّع (Pool)** | جداول مشتركة | مخطط واحد، وكل صف فيه `tenant_id` | منطقي (logical)، يفرضه الكود أو RLS | الأدنى (lowest) | الأدنى: قاعدة بيانات واحدة للترحيل (migrate) |
| **الجسر (Bridge)** | مخطط لكل مستأجر | قاعدة بيانات واحدة، ومخطط Postgres (Postgres schema) لكل مستأجر | فصل منطقي أقوى | متوسطة (medium) | الترحيلات تعمل N مرة |
| **الصومعة (Silo)** | قاعدة بيانات أو بنية لكل مستأجر | قاعدة بيانات منفصلة، وأحيانًا كل شيء منفصل | فيزيائي (physical) | الأعلى (highest) | N قاعدة بيانات للترقيع (patch) والنسخ الاحتياطي والمراقبة |

```mermaid
flowchart TD
    subgraph POOL["المجمّع Pool (Pool)"]
        P1[("قاعدة بيانات واحدة<br/>الصفوف موسومة بـ org_id<br/>(One database<br/>rows tagged org_id)")]
    end
    subgraph BRIDGE["الجسر Bridge (Bridge)"]
        B1[("قاعدة بيانات واحدة<br/>(One database)")] --> BS1["المخطط org_a<br/>(schema org_a)"]
        B1 --> BS2["المخطط org_b<br/>(schema org_b)"]
    end
    subgraph SILO["الصومعة Silo (Silo)"]
        S1[("قاعدة بيانات لـ org_a<br/>(DB for org_a)")]
        S2[("قاعدة بيانات لـ org_b<br/>(DB for org_b)")]
    end
```

**ابدأ بالمجمّع (Start with pool).** تقريبًا كل SaaS ستدرسه يعمل بنموذج المجمّع: جداول مشتركة مع `team_id` أو `organization_id`. هو الأرخص، والأبسط في الترحيل والاستعلام عبر المستأجرين (ولوحة الإدارة (admin panel) والتحليلات تحتاج ذلك)، ويتوسع (scales) إلى ملايين المستأجرين. نقطة ضعفه هي بالضبط الخطأ الذي بدأنا به: العزل يعتمد على أن يتضمن كل استعلام المرشّح. لذلك فإن بقية هذا الدرس تدور في معظمها حول جعل نسيان هذا المرشّح مستحيلًا، وحول متى تنقل بعض المستأجرين إلى الجسر أو الصومعة.

**اجعل المرشّح جزءًا من البنية (Make the filter structural).** الحد الأدنى (minimum) من الدفاعات (defences) في الإصدار الأول (v1) بنموذج المجمّع:

- **طبقة وصول إلى البيانات محددة بالمستأجر (tenant-scoped data-access layer)**: دوال المستودع (repository functions) تأخذ `orgId` كوسيط أول إلزامي، أو عميل محدد النطاق (scoped client) (`db.forOrg(orgId).monitors.find(id)`) يضيف المرشّح تلقائيًا. جوهرة `acts_as_tenant` في Rails، ومديرو النماذج (Managers) في Django، وامتدادات عميل Prisma كلها تطبّق هذه الفكرة.
- **حمّل الأبناء عبر الأب (load children through the parent)**: `org.monitors.find(id)`، ولا تكتب `Monitor.find(id)` أبدًا.
- **أعد 404 لا 403** لكائنات المستأجرين الآخرين، كي لا يمكن تحسّس المعرّفات (probed).
- **اختبار لكل نقطة نهاية (A test per endpoint)** يسجّل الدخول (logs in) كمنظمة B ويطلب كائنًا من المنظمة A.

### 🟡 التعمق أكثر

**أمان مستوى الصف (row-level security) في Postgres (RLS).** يسمح RLS لقاعدة البيانات نفسها بفرض مرشّح المستأجر. تفعّله على جدول وتكتب **سياسة (Policy)**: تعبيرًا منطقيًا (boolean expression) يضيفه Postgres بصمت إلى كل استعلام. إن نسي كود التطبيق (application code) شرط `WHERE`، تظل قاعدة البيانات تعيد صفوف المستأجر الحالي (current tenant) فقط.

```sql
ALTER TABLE monitor ENABLE ROW LEVEL SECURITY;
ALTER TABLE monitor FORCE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON monitor
  USING (organization_id = current_setting('app.current_org')::uuid)
  WITH CHECK (organization_id = current_setting('app.current_org')::uuid);
```

يضبط التطبيق المستأجر في بداية كل معاملة:

```sql
BEGIN;
SELECT set_config('app.current_org', $1, true); -- true = local to this transaction
SELECT * FROM monitor WHERE id = $2;            -- RLS adds the org filter
COMMIT;
```

التفاصيل مهمة. `USING` يصفّي ما تستطيع قراءته، و`WITH CHECK` يمنعك من كتابة صفوف في مستأجر آخر. مالكو الجداول (table owners) يتجاوزون RLS ما لم تستخدم `FORCE`، والمستخدمون الخارقون (Superusers) والأدوار التي تملك `BYPASSRLS` يتجاوزونه دائمًا، لذلك يجب أن يتصل التطبيق بدور مخصص ليس مالكًا للجداول. استخدم إعدادات محلية للمعاملة (transaction-local settings) (قيمة `true` أعلاه)، لأنه مع مجمّع اتصالات (pooler) في وضع المعاملة يتسرّب أمر `SET` على مستوى الجلسة (session-level) إلى الطلب التالي الذي يعيد استخدام الاتصال. ضع فهرسًا على `organization_id` كي تبقى السياسات سريعة.

نشرت Supabase هذا الأسلوب: يتحدث المتصفح مع Postgres عبر واجهة برمجية مولَّدة تلقائيًا (auto-generated API)، وسياسات RLS التي تستخدم `auth.uid()` أو المطالبات (Claims) من JWT الخاص بالمستخدم هي الشيء *الوحيد* الذي يحمي البيانات. هذا قوي ولا يغفر الأخطاء: الجدول الذي بلا سياسة يكون عامًا. في تطبيق يُعرض على الخادم (server-rendered)، يكون RLS عادة **دفاعًا إضافيًا (Defence in Depth)** خلف طبقة الوصول إلى البيانات، لا بديلًا عنها.

**تمرير سياق المستأجر (tenant context propagation).** يجب أن يتدفق "المستأجر الحالي" عبر كل ما يلمسه الطلب:

```mermaid
sequenceDiagram
    participant Q as طابور المهام (Job queue)
    participant D as Postgres
    participant H as المعالج (Handler)
    participant M as الوسيط البرمجي (Middleware)
    participant U as المستخدم (User)
    U->>M: طلب مع ملف تعريف ارتباط الجلسة (Request with session cookie)
    M->>M: تحديد المستخدم والمنظمة النشطة والتحقق من العضوية (Resolve user and active org, verify membership)
    M->>H: تشغيل المعالج داخل سياق المستأجر (Run handler inside tenant context)
    H->>D: BEGIN ثم set_config app.current_org (BEGIN then set_config app.current_org)
    D-->>H: صفوف مصفّاة بسياسة RLS (Rows filtered by RLS policy)
    H->>Q: وضع مهمة في الطابور مع org_id في الحمولة (Enqueue job with org_id in payload)
    Q->>D: العامل يضبط سياق المستأجر قبل الاستعلام (Worker sets tenant context before querying)
```

تستخدم Node الأداة `AsyncLocalStorage`، وPython `contextvars`، وRails `ActiveSupport::CurrentAttributes`، وGo قيمة في `context.Context`. الأماكن التي يضيع فيها السياق: المهام الخلفية (يجب أن تحمل الحمولة (payload) `org_id` ويجب أن يعيد العامل إنشاء السياق)، والمهام المجدولة (cron tasks) التي تمر على كل المستأجرين، والويب هوك (Webhook) القادم من Stripe (اربط عميل Stripe (Stripe customer) بالمنظمة)، والكاش (يجب أن يتضمن كل مفتاح كاش (cache key) المستأجر: `org:123:monitors`)، والسجلات (ضع `org_id` على كل سطر سجل (log line)، وهذا يسهّل الدعم كثيرًا أيضًا). سواء جاءت المنظمة من نطاق فرعي (subdomain) أو مسار (`/org/acme/...`) أو ترويسة (header)، **تحقق دائمًا من العضوية (membership)** على الخادم؛ ولا تثق أبدًا بمعرّف المنظمة (org id) في الرابط وحده.

**الجيران المزعجون (Noisy Neighbours).** في نظام مشترك (shared system)، حمل مستأجر واحد يضعف أداء الجميع. نسخة Beacon: منظمة واحدة لديها 3,000 مراقِب يعمل كل 30 ثانية تُغرق طابور الفحوص (check queue). الدفاعات، من الأرخص:

- **حدود الخطة (plan limits)** تُفرض وقت الإنشاء (الدرس 3.2): الخطة المجانية (Free plan) تحصل على 5 مراقِبات، نقطة.
- **تحديد معدل لكل مستأجر (per-tenant rate limits)** على الواجهة البرمجية ونقاط النهاية المكلفة (expensive endpoints) (الدرس 5.2).
- **الاصطفاف العادل (Fair Queuing)**: ضع حدًا للمهام المتزامنة (concurrent jobs) لكل مستأجر، أو استخدم طوابير أو أولويات لكل مستأجر، كي لا يستطيع مستأجر واحد إشغال كل العمال. عدة أنظمة مهام (job systems) في الدرس 5.1 تدعم حدود التزامن لكل مفتاح.
- **حراسات قاعدة البيانات (database guards)**: `statement_timeout` على دور التطبيق (app role)، وحدود للتصفح بالصفحات (pagination)، ولوحات استعلامات (query dashboards) لكل مستأجر (`pg_stat_statements` مع استعلامات موسومة) لاكتشاف المستأجر المسؤول عن استعلام بطيء (slow query).

### 🔴 على نطاق واسع وللمؤسسات

**التجزئة حسب المستأجر (Sharding).** عندما لا تتسع قاعدة Postgres أساسية واحدة للجميع، توزّع المستأجرين على عدة قواعد بيانات. ولأن كل استعلام تقريبًا في SaaS محصور بمستأجر واحد، يكون معرّف المستأجر (tenant id) هو **مفتاح التجزئة (Shard Key)** الطبيعي: تعيش كل صفوف المستأجر الواحد معًا، فلا تعبر الاستعلامات بين الأجزاء (shards). تفعل Citus، وهي إضافة لـ Postgres، ذلك بشفافية (transparently): تعلّم الجداول بأنها موزّعة (distributed) حسب `organization_id`، وتضع الجداول المرتبطة معًا (co-locate) على المفتاح نفسه، وتبقي الجداول المشتركة الصغيرة (الخطط، وأعلام الميزات) كجداول مرجعية (reference tables) منسوخة إلى كل عقدة، وتستطيع نقل مستأجر كبير إلى عقدة خاصة به. القاعدة التي تجعل التجزئة ممكنة الاحتمال يمكنك اعتمادها اليوم: **ضع `organization_id` في كل جدول يملكه مستأجر (tenant-owned table) وفي مفاتيحه الأساسية أو الفريدة (primary or unique keys)**، كي تكون البيانات مهيأة للتوزيع مسبقًا.

**قاعدة بيانات لكل مستأجر (database-per-tenant)، بتكلفة منخفضة.** كانت الصومعة تعني "مكلف". هناك نهجان أحدث يجعلانها عملية لعدد كبير من المستأجرين. **Turso/libSQL** (تفرّع من SQLite مع النسخ المتماثل (replication) ووضع الخادم) مصمَّم لأعداد ضخمة من قواعد البيانات الصغيرة، واحدة لكل مستأجر أو حتى لكل مستخدم. و**Neon** يفصل التخزين عن الحوسبة ويقلّص قواعد البيانات الخاملة (idle) إلى الصفر، فيكلّف مشروع أو فرع لكل مستأجر القليل عند عدم الاستخدام. ينتقل الجزء الصعب إلى التشغيل: تعمل الترحيلات الآن عبر آلاف قواعد البيانات، لذلك تحتاج أداة تشغيل موزِّعة (fan-out runner) تتتبع إصدار كل قاعدة بيانات، وتتحمل الفشل الجزئي (partial failure)، وتبقي الكود متوافقًا مع إصداري المخطط (schema versions) أثناء النشر (rollout) (التوسيع ثم التقليص مجددًا، من الدرس 2.1). الاستعلامات عبر المستأجرين (cross-tenant queries) للوحة الإدارة والتحليلات تحتاج مسارًا منفصلًا (separate pipeline). الجسر (مخطط لكل مستأجر) لديه مشكلة توزيع الترحيلات (migration fan-out) نفسها؛ تطبّقه `django-tenants` في Django وجواهر (gems) على نمط Apartment في Rails، ويستخدم Twenty مخططًا لكل مساحة عمل (workspace).

**إقامة البيانات (Data Residency).** بعض العملاء، غالبًا في الاتحاد الأوروبي بموجب GDPR أو في الصناعات المنظَّمة (regulated industries)، يشترطون تخزين بياناتهم ومعالجتها في منطقة محددة. وهذا يعني *كل* البيانات: قاعدة البيانات، وتخزين الكائنات (الدرس 2.2)، وفهرس البحث (الدرس 2.3)، والنسخ الاحتياطية، والسجلات، والمعالجين الفرعيين (subprocessors) مثل مزوّد البريد (email provider). البنية الشائعة (architecture) هي **الخلايا الإقليمية (Regional Cells)**: نسخة كاملة من البنية لكل منطقة، مع مستوى تحكم عالمي صغير لا يخزّن إلا دليل المستأجرين (tenant directory) (أي منظمة تعيش في أي منطقة) ويوجّه (routes) المستخدمين إليها.

```mermaid
flowchart RL
    U["المستخدم<br/>(User)"] --> G["الموجّه العالمي<br/>دليل المستأجرين<br/>(Global router<br/>tenant directory)"]
    G -->|"المنظمة في الاتحاد الأوروبي (org in EU)"| EU["خلية الاتحاد الأوروبي<br/>التطبيق وPostgres والحاوية والبحث<br/>(EU cell<br/>app, Postgres, bucket, search)"]
    G -->|"المنظمة في الولايات المتحدة (org in US)"| US["خلية الولايات المتحدة<br/>التطبيق وPostgres والحاوية والبحث<br/>(US cell<br/>app, Postgres, bucket, search)"]
    EU --> EUB[("نسخ احتياطية أوروبية<br/>(EU backups)")]
    US --> USB[("نسخ احتياطية أمريكية<br/>(US backups)")]
```

قرّر مكان الإقامة عند التسجيل (نقل مستأجر بين المناطق (regions) لاحقًا مشروع ترحيل (migration project) كامل)، وأبقِ البيانات الشخصية (personal data) خارج الدليل العالمي (global directory)، وتأكد من أن أدوات المراقبة التشغيلية والدعم لا تنسخ بيانات الاتحاد الأوروبي بصمت إلى الولايات المتحدة (US).

**عمليات النشر المخصصة (Dedicated Deployments).** هذا هو الطرف الأقصى للصومعة: يحصل عميل Business على بنيته الخاصة (قاعدة بياناته، وعماله، وأحيانًا حسابه السحابي (cloud account) الخاص). بِعها كفئة مميزة (premium tier)، وابنِها بوصفها **الكود نفسه والصور نفسها (images) بإعدادات مختلفة (configuration)**، تنشرها مسارات البنية التحتية ككود (infrastructure-as-code pipeline) نفسها (الدرس 7.4). في اللحظة التي يعمل فيها عميل مخصص على فرع منفصل (forked branch) من الكود، تصبح تصون منتجين. النمط المتكرر هو الهجين: المجمّع للخطتين Free وPro، وقواعد بيانات صومعة لمستأجري المؤسسات، مع جدول توجيه (routing table) من المستأجر إلى قاعدة البيانات.

**التصدير وإنهاء الخدمة (export and offboarding).** تنص عقود المؤسسات على أنك عند انتهاء العقد (termination) تصدّر بيانات المستأجر ثم تحذفها خلال مدة محددة. ابنِ تصديرًا (export) لكل مستأجر (JSON أو CSV لكل جدول إضافة إلى الملفات، تنتجه مهمة خلفية) وحذفًا لكل مستأجر يغطي كل مخزن (store): صفوف Postgres، والكائنات تحت بادئة المستأجر، ومستندات البحث (search documents)، والكاش، والتحليلات، والنسخ الاحتياطية (عادة بترك النسخ الاحتياطية تنتهي بمرور الوقت، والتصريح بذلك في سياستك). في نموذج المجمّع هذا استعلام لكل جدول مُصفّى بـ `organization_id`؛ وفي نموذج الصومعة هو حذف قاعدة بيانات، وهذا أحد أسباب تفضيل مشتري المؤسسات (enterprise buyers) للصوامع (silos).

## 🏆 أفضل المستودعات

| المستودع | ما هو | التقنيات | الترخيص | اختره عندما |
|---|---|---|---|---|
| [postgres/postgres](https://github.com/postgres/postgres) | أمان مستوى الصف، والسياسات، والأدوار، والمخططات (schemas) | C | PostgreSQL | تريد عزلًا تفرضه قاعدة البيانات في نموذج المجمّع |
| [supabase/supabase](https://github.com/supabase/supabase) | منصة Postgres مبنية حول سياسات RLS ومطالبات JWT (JWT claims) | TypeScript, Elixir, Go | Apache-2.0 | تريد تعلّم RLS من منصة تعتمد عليه |
| [citusdata/citus](https://github.com/citusdata/citus) | Postgres موزّع، مع التجزئة حسب معرّف المستأجر | C | AGPL-3.0 | لم تعد قاعدة Postgres أساسية واحدة كافية |
| [citusdata/activerecord-multi-tenant](https://github.com/citusdata/activerecord-multi-tenant) | جوهرة Rails تحصر الاستعلامات بالمستأجر تلقائيًا | Ruby | MIT | تشغّل Rails بنموذج المجمّع، مع Citus أو بدونها |
| [tursodatabase/libsql](https://github.com/tursodatabase/libsql) | تفرّع من SQLite مع وضع الخادم (server mode) والنسخ المتماثل | C, Rust | MIT | تريد آلاف قواعد البيانات الرخيصة لكل مستأجر |
| [neondatabase/neon](https://github.com/neondatabase/neon) | Postgres عديم الخادم مع التفريع والتقليص إلى الصفر | Rust | Apache-2.0 | تريد Postgres بقاعدة بيانات لكل مستأجر دون تكلفة الخمول (idle cost) |
| [ariga/atlas](https://github.com/ariga/atlas) | ترحيلات المخطط (schema migrations) ككود (schema-as-code migrations)، يمكن توجيهها إلى قواعد بيانات كثيرة | Go | Apache-2.0 | تشغّل الجسر أو الصومعة ويجب أن ترحّل N مخططًا بأمان |
| [boxyhq/saas-starter-kit](https://github.com/boxyhq/saas-starter-kit) | قالب بدء (starter kit) بـ Next.js مع الفرق والدخول الموحد (SSO) وSCIM وسجلات التدقيق (audit logs) | TypeScript | Apache-2.0 | تريد رؤية نموذج مجمّع جاهز للمؤسسات من البداية إلى النهاية |

**إن درست مستودعًا واحدًا فقط (If you study one repo):** توثيق Supabase وأمثلتها عن أمان مستوى الصف، تقرؤها إلى جانب فصل RLS في توثيق Postgres. كتابة سياسات لجداول `monitor` و`incident` و`membership` في Beacon، ثم محاولة كسرها، ستعلّمك عن عزل المستأجرين (tenant isolation) أكثر من أي مخطط.

**اشترِ أم ابنِ أم استضف بنفسك ⁦(Buy, build, or self-host?)⁩؟**

- **اشترِ (Buy):** Postgres مُدار مع RLS، وCitus مُدار للتجزئة، وTurso لقواعد SQLite لكل مستأجر. لإقامة البيانات، اختر مزوّدين لديهم المناطق التي تحتاجها ووقّع اتفاقيات معالجة البيانات (DPA) معهم.
- **استضف بنفسك (Self-host):** Citus أو مجموعة من نسخ Postgres عندما يشترط عقد أن تعمل على بنيتك التحتية أو يتطلب عمليات نشر مخصصة؛ وخصّص ميزانية لتوزيع الترحيلات والمراقبة.
- **ابنِ (Build):** تمرير سياق المستأجر، وطبقة الوصول إلى البيانات محددة النطاق (scoped)، وسياسات RLS، ودليل المستأجر إلى المنطقة أو إلى قاعدة البيانات، ومهام التصدير والحذف. هذه جوهرية لموثوقية منتجك ولا يستطيع أي مزوّد كتابتها نيابة عنك.

## 🔍 ادرسه في مشاريع حقيقية

**PostHog (`PostHog/posthog`).** نموذج مجمّع في Django: المنظمات تملك المشاريع (projects) (كانت تسمى تاريخيًا فرقًا)، وكل نموذج وجدول ClickHouse تقريبًا يحمل `team_id`. استخدم بحث الكود عن `team_id` و`TeamAndOrgViewSetMixin` (أو mixins مشابهة في طبقة الواجهة البرمجية) لترى كيف تحصر الـ viewsets مجموعات الاستعلامات (querysets) بالفريق الحالي. ويشغّل PostHog أيضًا منطقتين سحابيتين (cloud regions) منفصلتين في الولايات المتحدة والاتحاد الأوروبي، وهذا مثال حقيقي على الخلايا الإقليمية.

**Twenty (`twentyhq/twenty`).** نموذج جسر: البيانات الوصفية الأساسية (core metadata) تعيش في جداول مشتركة، بينما تعيش بيانات CRM لكل مساحة عمل في مخطط Postgres خاص بها. استخدم بحث الكود عن `workspaceDataSource` و`schema` في حزمة الخادم (server package) لترى كيف يختار الطلب المخطط الصحيح، وكيف تُطبَّق الترحيلات لكل مساحة عمل.

**Supabase (`supabase/supabase`).** ابحث في مجلد `examples` في المستودع عن `create policy` لتجد سياسات RLS حقيقية تستخدم `auth.uid()`، بما في ذلك سياسات عضوية الفرق (team membership) التي تربط عبر جدول الأعضاء.

**Cal.com (`calcom/cal.diy`).** ابحث في مخطط Prisma عن `teamId` و`organizationId` لترى نموذج مجمّع نمت فوق فرقه طبقة "organizations"، وكيف تُحصر قيود التفرّد.

**ما الذي تلاحظه (What to notice):**

- أين يدخل معرّف المستأجر إلى الطلب، والمكان الوحيد الذي يُتحقق فيه منه مقابل العضوية.
- هل الحصر تلقائي (scoping) (mixins، أو عملاء محددو النطاق (scoped clients)، أو RLS) أم يدوي في كل استعلام.
- كيف تحمل المهام الخلفية والكاش معرّف المستأجر وتستخدمه.
- أي الجداول *ليست* محصورة بالمستأجر عمدًا (الخطط، والإعدادات العامة) وكيف تُعلَّم.
- كيف تعمل الترحيلات عندما يوجد أكثر من مخطط أو قاعدة بيانات.

## 🛠️ ابنِه في Beacon

### 🟢 تمرين المبتدئ

دقّق (audit) كل نقاط النهاية (endpoints) في Beacon من حيث حصرها بالمستأجر. أضف دالة مساعدة محددة النطاق (scoped helper) للوصول إلى البيانات (data access) كي لا تستطيع المعالجات (handlers) تحميل بيانات المستأجر إلا عبر `forOrg(orgId)`، واكتب اختبارًا للتسريب بين المستأجرين يعمل على كل مسار.

**يكتمل عندما (Done when):**

- لا يستعلم أي معالج (handler) من جدول مستأجر دون المرور بالدالة المساعدة محددة النطاق (تفرضه قاعدة فحص كود (lint rule) أو قائمة تحقق (checklist) لمراجعة الكود).
- يسجّل اختبار آلي (automated test) الدخول كمنظمة B ويحصل على 404 لكل مورد (resource) من موارد المنظمة A.
- تتضمن مفاتيح الكاش (cache keys) وحمولات المهام (job payloads) `org_id`.

### 🟡 تمرين المستوى المتوسط

فعّل RLS في Postgres على `monitor` و`incident` و`incident_update` كدفاع إضافي. يتصل التطبيق بدور ليس مالكًا للجداول (non-owner role) ويضبط `app.current_org` لكل معاملة؛ والمهام الخلفية تضبطه أيضًا.

```ts
export async function withOrg<T>(orgId: string, fn: (tx: Tx) => Promise<T>) {
  return db.transaction(async (tx) => {
    await tx.execute(sql`select set_config('app.current_org', ${orgId}, true)`);
    return fn(tx);
  });
}
```

**يكتمل عندما (Done when):**

- يظل حذف `WHERE organization_id` من استعلام في اختبار يعيد صفوف المنظمة الحالية فقط.
- يفشل إدراج مراقِب بمعرّف منظمة أخرى بخطأ انتهاك RLS (RLS violation).
- يعمل ذلك عبر PgBouncer أو مجمّع الاتصالات لدى مزوّدك في وضع المعاملة.

### 🔴 تمرين المستوى المتقدم

أضف إقامة البيانات في الاتحاد الأوروبي والجدولة العادلة (fair scheduling). أنشئ جدول دليل المستأجرين (المنظمة ← المنطقة)، وشغّل "خليتين (two cells)" محليتين بقواعد بيانات وحاويات منفصلة، ووجّه الطلبات حسب منطقة المنظمة. ثم ضع حدًا لمهام الفحص (check jobs) المتزامنة لكل منظمة كي لا تستطيع منظمة لديها 3,000 مراقِب تأخير غيرها.

**يكتمل عندما (Done when):**

- توجد صفوف منظمة أوروبية وملفاتها ومستندات بحثها في الخلية الأوروبية (EU cell) فقط.
- لا يخزّن الدليل العالمي أي بيانات شخصية سوى المعرّفات والمنطقة.
- يبقي اختبار حمل (load test) مع منظمة ضخمة واحدة فحوص المنظمات الأخرى ضمن فتراتها المجدولة (scheduled intervals).

## ⚠️ أخطاء يقع فيها المبتدئون

- **الجلب بالمعرّف (id) وحده.** `findUnique({ where: { id } })` هو التسريب بين المستأجرين الذي ينتظر أن يحدث. احصر الاستعلام دائمًا بالمنظمة، أو حمّل عبر الأب.
- **الثقة بمعرّف المنظمة (org id) القادم من الرابط (URL) أو جسم الطلب (request body).** تحقق من عضوية المستخدم في تلك المنظمة في كل طلب، على الخادم.
- **استخدام `SET` على مستوى الجلسة (session level) مع مجمّع اتصالات (connection pooler) في وضع المعاملة (transaction mode).** يرث الطلب التالي على ذلك الاتصال المستأجر السابق (previous tenant). استخدم `set_config(..., true)` داخل معاملة.
- **الاتصال (connection) بصفة مالك الجدول (table owner) أو مستخدم خارق (superuser) مع تفعيل RLS.** تُتجاوز (bypassed) السياسات بصمت. استخدم دورًا مخصصًا (dedicated role) و`FORCE ROW LEVEL SECURITY`.
- **نسيان المستأجر (tenant) في المهام الخلفية (background jobs) والكاش (cache) والبحث (search).** قاعدة البيانات محصورة، لكن مفتاح كاش Redis `monitors:list` ليس كذلك. كل مخزن يحتاج المستأجر في مفتاحه أو مرشّحه.
- **اختيار الصومعة (silo) من اليوم الأول "من أجل الأمان".** تضاعف عمل الترحيل والنسخ الاحتياطي والمراقبة قبل أن يكون لديك عملاء يدفعون مقابله. ابدأ بالمجمّع، واجعل العزل جزءًا من البنية، وقدّم الصوامع كفئة مدفوعة (paid tier).
- **الوعد بإقامة البيانات (data residency) في الاتحاد الأوروبي (EU) دون فحص (check) السجلات (logs) والنسخ الاحتياطية (backups) ومزوّدي البريد (email providers).** إقامة البيانات تشمل كل نسخة من البيانات، بما في ذلك المعالجين الفرعيين لديك.

## 🧾 الخلاصة

- المجمّع والجسر والصومعة نقاط على طيف العزل (isolation spectrum)؛ أغلب منتجات SaaS تبدأ بالمجمّع وتضع أكبر عملائها في صوامع.
- التسريب بين المستأجرين هو فئة الأخطاء التي تصمّم ضدها (design against): وصول محدد النطاق إلى البيانات، والتحميل عبر الأب، وإعادة 404، واختبارات لكل مسار.
- يفرض RLS في Postgres مرشّح المستأجر داخل قاعدة البيانات؛ استخدمه كدفاع إضافي مع دور ليس مالكًا للجداول وإعدادات محلية للمعاملة.
- مرّر سياق المستأجر عبر المهام الخلفية والكاش والسجلات والبحث، لا عبر معالجات HTTP وحدها.
- يُتعامل مع الجيران المزعجين بحدود الخطط وتحديد المعدل (rate limiting) والاصطفاف العادل؛ والتجزئة حسب معرّف المستأجر (Citus) هي طريق التوسع (scaling path).
- إقامة البيانات وعمليات النشر المخصصة وإنهاء الخدمة (offboarding) متطلبات للمؤسسات تصبح أسهل بكثير إن كان `organization_id` في كل مكان من اليوم الأول.

## ✍️ اختبر نفسك

**1. ما نماذج المجمّع (pool) والجسر (bridge) والصومعة (silo)؟**

<details><summary>الإجابة</summary>

المجمّع جداول مشتركة يحمل فيها كل صف معرّف المستأجر. والجسر قاعدة بيانات واحدة مع مخطط Postgres لكل مستأجر. والصومعة قاعدة بيانات منفصلة لكل مستأجر، وأحيانًا بنية منفصلة بالكامل. وهي تقايض التكلفة والعبء التشغيلي مقابل قوة العزل. راجع الجدول في 🟢 الأساسيات.

</details>

**2. في سياسة (policy) RLS، ما الفرق بين `USING` و`WITH CHECK`؟**

<details><summary>الإجابة</summary>

`USING` يصفّي الصفوف التي تستطيع قراءتها. و`WITH CHECK` يمنعك من كتابة صفوف تخص مستأجرًا آخر. تحتاج عادة الاثنين على جدول المستأجر. راجع فقرة "أمان مستوى الصف في Postgres" في 🟡 التعمق أكثر.

</details>

**3. تنشئ منظمة (org) في الخطة المجانية (Free plan) 3,000 مراقِب (monitor) بسكربت (script)، فيتأخر مجدول الفحوص (check scheduler) في Beacon على الجميع. ما الدفاعات (defences) المناسبة، من الأرخص؟**

<details><summary>الإجابة</summary>

حدود الخطة وقت الإنشاء (الخطة المجانية تحصل على 5 مراقِبات)، وتحديد المعدل لكل مستأجر على الواجهة البرمجية، والاصطفاف العادل الذي يضع حدًا للمهام المتزامنة لكل مستأجر، وحراسات قاعدة البيانات مثل `statement_timeout` ولوحات الاستعلامات لكل مستأجر. راجع فقرة "الجيران المزعجون" في 🟡 التعمق أكثر.

</details>

**4. يطلب عميل محتمل (prospect) لخطة (plan) Business أن تبقى بياناته في الاتحاد الأوروبي (EU). ما الذي يحتاجه Beacon، وماذا تشمل عبارة "بياناته"؟**

<details><summary>الإجابة</summary>

تشمل كل شيء: قاعدة البيانات، وتخزين الكائنات، وفهرس البحث، والنسخ الاحتياطية، والسجلات، والمعالجين الفرعيين مثل مزوّد البريد. التصميم الشائع هو الخلايا الإقليمية، أي بنية كاملة لكل منطقة، مع دليل عالمي صغير لا يخزّن إلا أي منظمة تعيش في أي منطقة ويوجّه المستخدمين إليها. قرّر المنطقة عند التسجيل. راجع فقرة "إقامة البيانات" في 🔴 على نطاق واسع وللمؤسسات.

</details>

**5. يستخدم Beacon الـ RLS مع `SET app.current_org = ...` في بداية كل طلب (request)، ويتصل عبر PgBouncer في وضع المعاملة (transaction mode). أحيانًا يرى مستخدم مراقِبات (monitors) منظمة (org) أخرى. ما الذي تعطّل؟**

<details><summary>الإجابة</summary>

أمر `SET` على مستوى الجلسة يبقى على اتصال الخادم، وفي وضع المعاملة يرث الطلب التالي الذي يعيد استخدام ذلك الاتصال المستأجر السابق. استخدم `set_config('app.current_org', $1, true)` داخل معاملة كي يكون الإعداد محليًا لها. واتصل أيضًا بدور ليس مالكًا للجداول، لأن المالكين والمستخدمين الخارقين يتجاوزون RLS ما لم يُفرض. راجع فقرة "أمان مستوى الصف في Postgres" في 🟡 التعمق أكثر.

</details>

## 📚 المراجع

- PostgreSQL documentation, "Row Security Policies": https://www.postgresql.org/docs/current/ddl-rowsecurity.html — سياسات أمان الصفوف
- AWS Well-Architected SaaS Lens and the AWS whitepapers "SaaS Architecture Fundamentals" and "SaaS Tenant Isolation Strategies": https://docs.aws.amazon.com/wellarchitected/ and https://docs.aws.amazon.com/whitepapers/ — أساسيات بنية SaaS واستراتيجيات عزل المستأجرين
- Supabase documentation on Row Level Security: https://supabase.com/docs
- Citus documentation (multi-tenant applications): https://docs.citusdata.com — التطبيقات متعددة المستأجرين
- Turso documentation: https://docs.turso.tech — قاعدة بيانات لكل مستأجر
- Neon documentation: https://neon.com/docs
- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html — ورقة مرجعية للتفويض (authorization)

التالي: **الوحدة 3 (Module 3) — المال**، حيث يبدأ Beacon بتحصيل المال مقابل كل هذا.
