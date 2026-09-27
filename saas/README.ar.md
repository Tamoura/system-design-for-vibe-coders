# SaaS Building Blocks — مكوّنات بناء SaaS (SaaS Building Blocks)

**كل SaaS هو التطبيق نفسه بمنتج مختلف (Every SaaS is the same app wearing a different product). تعلّم المكوّنات (components) الـ 25 تقريبًا التي تشترك فيها
جميعًا، مرة واحدة، من أفضل كود مفتوح المصدر (the best open-source code) متاح.**

## ما هذه الدورة (What this is)

دورة مكتوبة (A written course) **للمطورين المبتدئين (junior developers)** الذين يستطيعون بناء تطبيق CRUD (CRUD app) لكنهم لم يطلقوا SaaS
حقيقيًا أو يشغّلوه من قبل. افتح عشرة منتجات SaaS ناجحة، مثل أداة جدولة (scheduling tool)، ونظام لإدارة
علاقات العملاء (CRM)، ومختصر روابط (link shortener)، ومتتبّع أخطاء (error tracker)، وستجد الآليات (machinery) نفسها في كل واحد منها:
التسجيل وتسجيل الدخول (sign-up and login)، والمؤسسات والدعوات (organizations and invitations)، والأدوار (roles)، وصفحة الفوترة (billing page)، والبريد الإلكتروني
التشغيلي (Transactional Email)، والمهام الخلفية (Background Jobs)، وواجهة برمجية (API)
بمفاتيح (keys)، والويب هوك (Webhook) الصادرة، وسجل التدقيق (Audit Log)، ولوحة الإدارة (admin panel)، والدخول
الموحد (SSO) للعملاء الكبار (big customers). أما الجزء الذي يدفع العميل مقابله (the part the customer actually pays for) فعلًا فكثيرًا ما يكون
نسبة صغيرة من الكود (code).

وهذا خبر جيد، لأنه يعني أن أسرع طريق لتصبح مفيدًا في أي فريق SaaS (SaaS team) هو أن تتعلّم هذه
المكوّنات المشتركة (shared components) جيدًا، وأن تعرف أين توجد أفضل تطبيقاتها (best implementations). وهذه الدورة (course) تفعل الأمرين:

- **مكوّن واحد في كل درس (One component per lesson)**، يُشرح من المبادئ الأولى (first principles) ويصعد من الأساسيات (The essentials) إلى ما يقلق
  المهندسين الخبراء (senior engineers) على نطاق واسع (at scale).
- **أفضل المستودعات لكل مكوّن (The best repos for each component)**: المكتبات (libraries) والخدمات التي يمكنك استضافتها بنفسك (self-hostable services) وتبنّيها،
  *و*قواعد كود SaaS (SaaS codebases) مفتوحة المصدر (open-source) تعمل في الإنتاج (Cal.com، وDocumenso، وDub، وTwenty،
  وPlane، وPostHog، وSentry، وGitLab، وChatwoot، وInfisical…) حيث يمكنك قراءة المكوّن (component) وهو
  يعمل فعلًا.
- **منتج واحد يُبنى على امتداد الدورة كلها (One product built across the whole course)**: **Beacon**، مراقبة الجاهزية (uptime monitoring) وصفحات الحالة (status pages)
  العامة للفرق، وقد اختير لأنه يحتاج كل المكوّنات (components).

## كيف يعمل كل درس (How every lesson works)

لكل درس (lesson) الأجزاء العشرة نفسها، حتى تعرف دائمًا أين أنت:

| الجزء (Part) | ما تحصل عليه (What you get) |
|---|---|
| ⚡ **الدرس في دقيقة (In 60 seconds)** | من أربع إلى ست نقاط: ما المكوّن (component)، والقاعدة الأهم (the rule that matters most)، والخيار الافتراضي للنسخة الأولى (the v1 default)، وأكبر فخ (the biggest trap). |
| 🧭 **لماذا يحتاجه كل SaaS (Why every SaaS has this)** | السيناريو في Beacon (أو حالة عامة حقيقية (real public case)) الذي يجعل المكوّن (component) ضروريًا. |
| 📐 **كيف يعمل (How it works)** | المفاهيم على شكل سلّم (ladder): 🟢 *الأساسيات (The essentials)* ← 🟡 *التعمق أكثر (Going deeper)* ← 🔴 *على نطاق واسع وللمؤسسات (At scale / enterprise)*. |
| 🏆 **أفضل المستودعات (The best repos)** | جدول مقارنة (comparison table) لأفضل الخيارات مفتوحة المصدر (open-source options)، والمستودع الذي تدرسه أولًا (the one to study first)، وحكم بالشراء أو الاستضافة الذاتية أو البناء (buy / self-host / build verdict). |
| 🔍 **ادرسه في مشاريع حقيقية (Study it in the wild)** | أين تطبّقه قواعد كود SaaS (SaaS codebases) حقيقية في الإنتاج (production)، وكيف تجد الكود (code)، وما الذي تلاحظه (what to notice). |
| 🛠️ **ابنِه في Beacon (Build it into Beacon)** | ثلاثة تمارين متدرجة (graded exercises)، 🟢 للمبتدئ (beginner) و🟡 للمتوسط (intermediate) و🔴 للمتقدم (advanced)، ولكل منها معايير (criteria) "يكتمل عندما (done when)". |
| ⚠️ **أخطاء يقع فيها المبتدئون (Mistakes juniors make)** | الفخاخ (traps)، وما يجب فعله بدلًا منها. |
| 🧾 **الخلاصة (Recap)** | النقاط التي تستحق أن تتذكرها. |
| ✍️ **اختبر نفسك (Check yourself)** | خمسة أسئلة بإجابات مخفية (hidden answers): أسئلة تذكّر (recall)، وأسئلة تطبيقية على Beacon (applied to Beacon)، وسيناريو واحد من نوع "ما الذي ينكسر (what breaks)". |
| 📚 **المراجع (References)** | المواصفات (specs)، والتوثيق الرسمي (official docs)، وتوثيق المستودعات نفسها (the repos' own documentation). |

## مسارات التعلّم (Learning paths)

يحمل كل درس (lesson) شارة مستوى (level badge) تبيّن من أين *يبدأ*: 🟢 مبتدئ (Beginner)، أو 🟡 متوسط (Intermediate)، أو 🔴 متقدم (Advanced).
اختر المسار (track) الذي يناسبك.

### 🟢 مسار المبتدئ (Beginner track): "أطلق النسخة الأولى من SaaS (ship a SaaS v1)" (نحو 4 أسابيع)

اقرأ (Read) الوحدة 0 (Module 0)، ثم الدروس (lessons) 1.1 و1.2 و2.1 و2.2 و3.1 و4.1 و6.1. نفّذ (Do) تمرين (exercise) 🟢 في كل منها.
في النهاية سيكون لديك Beacon يستطيع الناس التسجيل (sign-up) فيه، وإنشاء مساحة عمل (workspace)، ودعوة زملائهم (invite teammates)،
والدفع مقابله، وتلقّي البريد (receive email) منه.

### 🟡 المسار المتوسط (Intermediate track): "انجُ مع عملاء حقيقيين (survive real customers)" (نحو 5 أسابيع)

الدروس (lessons) 1.3 و2.3 و3.2 و4.2 و5.1 و5.2 و5.3 و6.2 و6.3 و7.1 و7.2 و7.3، إضافة إلى تمارين (exercises) 🟡
في دروس المبتدئ (Beginner lessons) التي قرأتها. هذه هي الطبقة (layer) التي تفصل العرض التجريبي (demo) عن المنتج:
الصلاحيات (permissions)، والمهام الخلفية (background jobs)، والواجهة البرمجية العامة (public API)، والويب هوك (webhooks)، والتحليلات (analytics)، وأعلام
الميزات (Feature Flags)، ولوحة الإدارة (admin panel)، والمراقبة (Observability)، وسجل التدقيق (audit log).

### 🔴 المسار المتقدم (Advanced track): "اربح صفقات المؤسسات وتوسّع (win enterprise deals and scale)" (نحو 4 أسابيع)

الدروس (lessons) 1.4 و2.4 و3.3 و4.3 و5.4 و7.4 و8.1 و8.2، وتمارين (exercises) 🔴 في كل مكان، والمشروع الختامي (capstone)
(9.1). الدخول الموحد (SSO) وSCIM، وعزل المستأجرين (tenant isolation)، والفوترة حسب الاستخدام (usage-based billing)، والتعاون اللحظي (realtime collaboration)،
وسير العمل المتين (durable workflows)، والاستضافة الذاتية (self-hosting)، والامتثال (compliance)، وميزات الذكاء الاصطناعي (AI features).

### خطة من 12 أسبوعًا لدفعة من المبتدئين (A 12-week plan for a junior cohort)

| الأسبوع (Week) | اقرأ (Read) | نفّذ (Do) |
|---|---|---|
| 1 | 0.1، 0.2، 0.3 | شغّل SaaS مرجعيًا (reference SaaS) واحدًا محليًا (locally)، وارسم خريطة مكوّناته (map its components). |
| 2 | 1.1، 1.2 | التسجيل وتسجيل الدخول (sign-up and login) والمؤسسات والدعوات (organizations and invitations) في Beacon. |
| 3 | 2.1، 2.2 | المخطط (schema)، والترحيلات (migrations)، وبيانات البذر (seeds)، ورفع شعار صفحة الحالة (status-page logo upload). |
| 4 | 3.1، 4.1 | الدفع عبر Stripe (Stripe checkout) والويب هوك (webhooks)، ورسائل التحقق والدعوة (verification and invite emails). |
| 5 | 6.1، 1.3 | هيكل التطبيق (app shell)، والإعداد الأولي (onboarding)، والإعدادات (settings)، والأدوار (roles) وفحص الصلاحيات (permission checks). |
| 6 | 5.1 | مجدول فحص المراقِبات (monitor-check scheduler) والعمّال (workers). |
| 7 | 3.2، 4.2 | حدود الخطط (plan limits)، وإشعارات الحوادث (incident notifications) مع التفضيلات (preferences). |
| 8 | 5.2، 5.3 | واجهة برمجية عامة (public API) بمفاتيح (keys) وتحديد معدل (rate limits)، وويب هوك صادرة (outbound webhooks) وSlack. |
| 9 | 6.2، 6.3، 2.3 | أحداث التحليلات (analytics events)، وطرح ميزة (feature rollout) عبر علم ميزة (feature flag)، والبحث (search). |
| 10 | 7.1، 7.2، 7.3 | لوحة الإدارة (admin panel)، والمراقبة (observability)، وسجل التدقيق (audit log). |
| 11 | اختر 3 من الوحدة (module) 1.4 إلى 8.2 | تمرين (exercise) 🔴 واحد لكل منها. |
| 12 | 9.1 | مراجعة المشروع الختامي (Capstone review): اعرض معمارية Beacon (Beacon's architecture) وقرارات البناء أو الشراء (build-vs-buy choices). |

للمرشدين (Mentors): اجعلوا المبتدئين (juniors) يعرضون نتائج "🔍 ادرسه في مشاريع حقيقية (Study it in the wild)" على بعضهم. قراءة
كود حقيقي (real code) وشرحه بصوت عالٍ هي المهارة (skill) التي تعلّمها هذه الدورة (course) فعلًا.

## مستودع التدريب (The practice repo): Beacon

لكل تمرين (exercise) من تمارين (exercises) "🛠️ ابنِه في Beacon (Build it into Beacon)" شيفرة حقيقية (real codebase) تعمل عليها. **نسخة البداية من Beacon (Beacon starter)** تطبيق يعمل مبني
بـ Next.js وPostgreSQL: المراقِبات (monitors)، وفحوص التوفر (uptime checks)، والحوادث (incidents)، ولوحة التحكم (dashboard)، وصفحة الحالة العامة (public status page). أما المكوّنات (components)
العامة التي يحتاجها كل تطبيق SaaS (SaaS app) فغير موجودة، وكل واحد منها معلَّم بتعليق `TODO(رقم الدرس)`. انسخها كمستودع مستقل (standalone repo):

```bash
git clone -b beacon/starter --single-branch https://github.com/Tamoura/system-design-for-vibe-coders.git beacon
```

لكل وحدة (module) **فرع حلٍّ مرجعي (reference solution branch)** باسم `beacon/module-N-solution`، ينفّذ تمارين (exercises) 🟢 و🟡 فوق حل الوحدة السابقة (previous module).
أما تمارين (exercises) 🔴 فتُركت تحديًا إضافيًا (stretch goals). حاول حل كل تمرين (exercise) أولًا، ثم قارن:

```bash
git fetch origin beacon/module-3-solution:module-3-solution
git diff main module-3-solution
```

تُنشر فروع الحلول (solution branches) تباعًا مع اكتمال كل وحدة (module). يمكنك أيضًا تصفّح نسخة البداية (starter) في مجلد
[`beacon/`](https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/beacon)، وستجد كل التمارين مع
معايير اكتمالها (done when criteria) في ملف (file) `docs/EXERCISES.md` داخله.

## ما تحتاجه (What you need)

- الارتياح في العمل مع تقنية ويب واحدة (الأمثلة تستخدم TypeScript وNext.js وPostgreSQL،
  وكل درس (lesson) يذكر ما يقابلها في Django وRails وLaravel وGo).
- Git وDocker وحساب على GitHub (GitHub account) لقراءة المستودعات المرجعية (reference repos) وتشغيلها.
- لا تحتاج خبرة سابقة في SaaS (prior SaaS experience). كل مصطلح (term) يُعرَّف عند ظهوره أول مرة.

## ملاحظة عن المستودعات (A note on the repos)

توصي الدورة (course) بأكثر من 220 مستودعًا (repositories). اختيرت لأنها مستخدمة على نطاق واسع (widely used)، أو تُصان بنشاط (actively maintained)،
أو سهلة القراءة (readable) على نحو غير معتاد، لا لأن أحدًا دفع مقابل ذكرها. وهناك تنبيهان (Two cautions):

- **التراخيص تتغيّر (Licenses change).** انتقلت عدة مشاريع معروفة بين MIT/Apache وAGPL وتراخيص الكود (source-available licenses)
  المتاح (FSL، وBSL، وELv2، و"fair-code") في السنوات الأخيرة. يشرح الدرس (lesson) 0.3 ما يعنيه كل
  منها لك. اقرأ (Read) دائمًا ملف (file) `LICENSE` في المستودع قبل أن تنسخ الكود (code) أو تستضيفه تجاريًا (self-host commercially).
- **المشاريع تتغيّر (Projects move).** تُعاد تسمية المستودعات (repos) أو تُؤرشف (archived) أو يُستحوذ عليها (acquired). القائمة الكاملة (full list)
  موجودة في [فهرس المستودعات (repo catalog)](./REPOS.ar.md)، وشغّل `npm run saas:repos` للتحقق من كل رابط.

## ما الجديد في الإصدار 2 (What's new in version 2)

- **نسخة عربية من كل درس وكل صفحة (An Arabic edition of every lesson and page).** لكل وحدة (module) نسخة عربية مطابقة (`NN-slug.ar.md`)،
  وكذلك هذا الملف و[خريطة الدورة (course map)](./OUTLINE.ar.md).
- **ملخصات في 60 ثانية (60-second summaries).** يبدأ كل درس (lesson) الآن بقسم ⚡ *الدرس في دقيقة (In 60 seconds)*، لقراءة سريعة (quick read) قبل
  التعمق أو لمراجعة لاحقة (refresher).
- **اختبارات ذاتية (Self-checks).** ينتهي كل درس (lesson) الآن بقسم ✍️ *اختبر نفسك (Check yourself)*: خمسة أسئلة بإجابات يمكنك
  إظهارها، وكل إجابة تشير إلى القسم الذي يشرحها.

## إلى أين بعد ذلك (Where to go next)

افتح [خريطة الدورة (course map)](./OUTLINE.ar.md) أو ابدأ بالدرس (lesson) 0.1.
