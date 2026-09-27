# الوحدة 6 (Module 6) — المنتج والنمو (Product & Growth)

*بنت الوحدات 1–5 الآلية التي لا يراها العملاء (customers) أبدًا. تغطي هذه الوحدة الأجزاء التي يرونها، والأجزاء التي تخبرك بما يفعلونه: هيكل التطبيق (app shell) الذي يدخلون إليه كل يوم، والتحليلات (analytics) التي تبيّن هل يحصلون على قيمة، وأعلام الميزات (feature flags) التي تسمح لك بتغيير المنتج (product) من تحتهم دون أن تكسره. لا شيء من هذه صعب البداية، لكن الثلاثة تصبح فوضوية بسرعة إن لم تخطط لها.*

> **التطبيق العملي (Practice):** ابدأ من [نسخة البداية (starter) من Beacon](https://github.com/Tamoura/system-design-for-vibe-coders/tree/beacon/starter)، وحلّ التمارين قبل النظر إلى [الحل المرجعي (reference solution) لهذه الوحدة](https://github.com/Tamoura/system-design-for-vibe-coders/tree/beacon/module-6-solution) (الفرع (branch) `beacon/module-6-solution`).

---

# 6.1 — هيكل التطبيق (app shell): موقع التسويق (marketing site) والتهيئة (onboarding) ولوحة التحكم (dashboard) والإعدادات (settings)

*المستوى (Level): 🟢 مبتدئ (Beginner)* · *المتطلبات (Prerequisites): 1.1، 1.2*

## ⚡ الدرس في دقيقة (In 60 seconds)

- هيكل التطبيق (app shell) هو الإطار المحيط بمنتجك (your product): موقع التسويق (marketing site)، والتخطيط الخاص بالمستخدمين المسجلين (authenticated layout)، والتهيئة (onboarding)، والإعدادات (settings)، والنماذج (forms)، ونظام التصميم (design system)، والواجهات التي يراها المستأجرون (tenant-facing) مثل النطاقات المخصصة (custom domains).
- القاعدة الأهم (The rule that matters most): افصل موقع التسويق (ثابت أو مُصيَّر على الخادم (SSR)، مهيأ لمحركات البحث (SEO)، ويعدّله غير المهندسين (non-engineers)) عن التطبيق (يتطلب تسجيل الدخول (authenticated)، ومعرّف المؤسسة (org slug) في الرابط (URL)).
- الخيار الافتراضي للنسخة الأولى (The v1 default): مستودع أحادي (Monorepo) فيه موقع التسويق (marketing site) والتطبيق (app) منفصلان، وshadcn/ui مبنية على Radix وTailwind، ومخطط (schema) zod واحد يتشاركه النموذج (form) والخادم (server).
- صمّم لوحة التحكم الفارغة (empty dashboard) والتهيئة (onboarding) حول حدث تفعيل (activation event) واحد، واحفظ تقدم التهيئة (onboarding progress) على المؤسسة (organization) لا في `localStorage`.
- الفخ الأكبر (The biggest trap): أن تعدّ إخفاء زر (hidden button) أو التحقق في المتصفح (client-side validation) أمانًا (security). الخادم (server) يتحقق من المخطط (schema) والصلاحية (permission) وحدّ الخطة (plan limit) في كل مرة.

## 🧭 لماذا يحتاجه كل SaaS (Why every SaaS has this)

النسخة الأولى من Beacon تطبيق Next.js (Next.js app) واحد. الصفحة الرئيسية (landing page) وصفحة الأسعار (pricing page) ونموذج الدخول (login form) ولوحة المراقبات (monitor dashboard) وشاشات الإعدادات (settings screens) كلها في مجلد `app/` نفسه، وتتشارك تخطيطًا واحدًا (layout)، وتُنشر (deploy) معًا. ويعمل هذا جيدًا إلى أن تحدث ثلاثة أشياء في الشهر نفسه.

يريد فريق التسويق (marketing) إعادة كتابة الصفحة الرئيسية (landing page) ونشر مدونة (blog)، فيصبح كل تعديل على النص (copy change) يمر بخط CI (CI pipeline) نفسه وطابور المراجعة (review queue) نفسه الذي تمر به ترحيلات قاعدة البيانات (database migration). ويفهرس (indexes) Google مؤشر التحميل (loading spinner) في لوحة التحكم (dashboard) بدل صفحة الأسعار (pricing page)، لأن كل شيء يُصيَّر في المتصفح (renders client-side) خلف فحص المصادقة (auth check). ويسأل عميل (customer) على خطة (plan) Business لماذا تعيش صفحة حالته العامة (public status page) على `beacon.dev/s/acme` بينما يسمح له كل منافس باستخدام `status.acme.com`.

في الوقت نفسه، الأرقام سيئة بطريقة أهدأ. يسجل الناس (sign up)، فيصلون إلى لوحة فارغة (empty dashboard) مكتوب فيها "لا توجد مراقبات (monitors) بعد"، ثم يغادرون. لم يخبرهم أحد بما يفعلونه أولًا. وصفحة الإعدادات (settings page) نموذج (form) طويل واحد يقع فيه زر "حذف المؤسسة (delete org)" بجانب "تغيير صورتك".

لا شيء من هذا منطق منتج (product logic). إنه **هيكل التطبيق (App Shell)**: الإطار الذي يضعه كل SaaS حول منتجه الفعلي. ويشمل موقع التسويق (marketing site) العام، والتخطيط الخاص بالمستخدمين المسجلين (authenticated layout)، والتهيئة (Onboarding)، والإعدادات (settings)، والنماذج (forms)، ونظام التصميم (design system)، والواجهات التي يراها المستأجرون (Tenants) مثل النطاقات المخصصة (custom domains). **هيكل التطبيق هو الجزء من SaaS الذي يلمسه كل عميل (customer) في كل زيارة، لذلك يجعل الهيكلُ (shell) المهمَل منتجًا (product) جيدًا يبدو معطوبًا.**

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**افصل موقع التسويق (marketing site) عن التطبيق (app).** احتياجاتهما متعاكسة:

| | موقع التسويق (`beacon.dev`) | التطبيق (`app.beacon.dev`) |
|---|---|---|
| الجمهور (Audience) | زوار مجهولون (anonymous visitors) ومحركات البحث (search engines) | مستخدمون مسجلو الدخول (logged-in users) |
| التصيير (rendering) | ثابت أو على الخادم (SSG/SSR) من أجل محركات البحث (search engines) والسرعة | الاعتماد على المتصفح (browser) مقبول ولا حاجة لمحركات البحث (search engines) |
| التغييرات (Changes) | نصوص ومقالات وأسعار، وغالبًا يعدّلها غير المهندسين (non-engineers) | ميزات (features) يبنيها المهندسون (engineers) |
| المصادقة (Auth) | لا شيء | كل شيء خلف فحص الجلسة (session check) |
| كلفة الخطأ (failure cost) | خطأ إملائي (typo) | بيانات شخص ما |

التوليد الثابت (SSG — Static Site Generation) يعني أن الصفحات تُبنى إلى HTML وقت النشر (deploy time). والتصيير على الخادم (SSR — Server-Side Rendering) يعني أن HTML يُبنى مع كل طلب (per request). في الحالتين يحصل محرك البحث (search engine) على نص حقيقي بدل `<div id="root">` فارغ. التنظيم المعتاد هو **المستودع الأحادي (Monorepo)**، أي مستودع Git (Git repo) واحد يحوي عدة تطبيقات (apps) وحزمًا مشتركة (shared packages): `apps/web` للتسويق (marketing)، و`apps/app` للمنتج (product)، و`packages/ui` للمكونات المشتركة (shared components). يُنشر كل منها منفصلًا، لكنها تتشارك نظام تصميم (design system) واحدًا. وnext-forge مثال جيد على هذا الشكل. ويمكن أن يعيش موقع التسويق (marketing site) على نظام إدارة محتوى (CMS) أو أداة بناء مواقع (site builder) أيضًا. المهم ألا يحتاج مقال في المدونة (blog post) إلى مراجعة ترحيل قاعدة بيانات (database migration).

ملفات تعريف الارتباط (Cookies) تحدد كيف يتواصل الاثنان. إن أردت أن يعرض موقع التسويق (marketing site) "اذهب إلى لوحة التحكم (dashboard)" للزوار المسجلين (logged-in visitors)، فيجب أن يكون ملف الجلسة (session cookie) مقروءًا على النطاق الأب (parent domain)، أو أن يستدعي موقع التسويق نقطة نهاية (endpoint) صغيرة في التطبيق (app). قرّر هذا مبكرًا، لأنه يؤثر في خاصية (attribute) `Domain` لملف الارتباط (1.1).

**التخطيط الخاص بالمستخدمين المسجلين (authenticated layout)** هو الإطار المحيط بكل صفحة بعد الدخول (login). وفي SaaS الموجّه للشركات (B2B) استقر على شكل مألوف:

- **شريط جانبي (sidebar)** فيه الأقسام الرئيسية (المراقبات (monitors)، الحوادث (incidents)، صفحات الحالة (status pages)، الإعدادات (settings)).
- **مبدّل المؤسسات (org switcher)** في الأعلى، لأن المستخدمين (users) ينتمون إلى عدة مؤسسات (1.2). المؤسسة الحالية (current org) جزء من الرابط (`/acme/monitors`) وليست مخفية في حالة المتصفح (client state)، حتى يمكن مشاركة الروابط (links) ولا تنقل إعادةُ التحميل (reload) أحدًا إلى المستأجر الخطأ (wrong tenant).
- **قائمة المستخدم (user menu)** فيها الملف الشخصي (profile) والسمة (theme) وتسجيل الخروج (sign-out).
- **لوحة الأوامر (command palette)** (`⌘K`)، وهي مربع بحث (search box) ينقلك إلى أي صفحة أو إجراء (action). مكوّن (component) Command في shadcn/ui مبني على مكتبة (library) `cmdk`، لذلك تحصل عليها تقريبًا بلا جهد.

**التهيئة (onboarding) والحالات الفارغة (empty states).** مستخدم (user) Beacon الجديد ليس لديه مراقبات (monitors) ولا حوادث (incidents) ولا صفحة حالة (status page). هذه اللوحة (dashboard) الفارغة أهم شاشة ستطلقها، لأن كل مستخدم يراها، ومعظمهم يقرر خلال دقائق هل سيبقى. الحالة الفارغة الجيدة (empty state) تشرح ما الذي يوضع هنا وتقدم إجراءً (action) واحدًا واضحًا: "أضف أول مراقبة (monitor) لك: الصق رابطًا وسنفحصه كل 5 دقائق." والأفضل أن يطلب مسار التسجيل (signup flow) هذا الرابط (URL)، فلا تكون اللوحة فارغة أبدًا.

لتلك اللحظة القيّمة الأولى اسم. **التفعيل (Activation)** هو الحدث (event) الذي يعني أن المستخدم (user) جرّب فعلًا قيمة المنتج (product). في Beacon قد يكون "أنشأ مراقبة (monitor) وتلقى أول نتيجة فحص (check result) خلال 24 ساعة". اختر حدث تفعيل (activation event) واحدًا، وتتبّعه (6.2)، وصمم التهيئة (onboarding) لإيصال الناس إليه. قوائم المهام (checklists) والتلميحات (tooltips) والجولات التعريفية (product tours) كلها أساليب لخدمة هذا الرقم الواحد.

**النماذج (forms) والتحقق (validation).** معظم أي SaaS نماذج. الفكرة الأساسية أن **تعرّف مخطط التحقق (validation schema) لكل نموذج (form) مرة واحدة وتستخدمه في المتصفح (browser) والخادم (server) معًا.** نسخة المتصفح تعطي ملاحظات فورية (instant feedback). ونسخة الخادم هي التي تثق بها فعلًا، لأن أي شخص يستطيع تجاوز واجهتك (frontend) باستخدام `curl`. تفعل Zod هذا في TypeScript:

```ts
// packages/validation/monitor.ts, imported by the form AND the server
import { z } from "zod";

export const createMonitorSchema = z.object({
  name: z.string().trim().min(1, "Give it a name").max(80),
  url: z.string().url("Use a full URL, e.g. https://api.acme.com/health"),
  intervalSeconds: z.coerce.number().int().min(30).max(300),
});
export type CreateMonitorInput = z.infer<typeof createMonitorSchema>;

// Server side (route handler or server action)
export async function createMonitor(orgId: string, raw: unknown) {
  const parsed = createMonitorSchema.safeParse(raw);
  if (!parsed.success) return { ok: false, issues: parsed.error.issues };
  await assertCan(orgId, "monitor:create");   // lesson 1.3
  await assertWithinLimit(orgId, "monitors"); // lesson 3.2
  return { ok: true, monitor: await db.monitor.create({ data: { orgId, ...parsed.data } }) };
}
```

في المتصفح (browser)، تربط React Hook Form مع `@hookform/resolvers` المخطط (schema) نفسه بالنموذج (form). وللتقنيات الأخرى (other stacks) النمط نفسه: نماذج (forms) Django أو مُسلسِلات (serializers) DRF، وتحققات نماذج (model validations) Rails مع المعاملات القوية (Strong Parameters)، وForm Requests في Laravel، ووسوم الهياكل (struct tags) في Go مع `go-playground/validator`.

**نظام التصميم (design system).** لا تبنِ القوائم المنسدلة (dropdowns) بيدك. الخيار الافتراضي الحديث في React طبقات:

- **Tailwind CSS** يتولى التنسيق (styling) عبر أصناف مساعدة (Utility Classes).
- **Radix UI primitives** مكونات (components) بلا تنسيق (unstyled) وسهلة الوصول (accessible) (نافذة حوار (dialog)، قائمة منسدلة (dropdown)، نافذة منبثقة (popover)) تتعامل عنك مع حصر التركيز (focus traps) والتنقل بلوحة المفاتيح (keyboard navigation) وخصائص (properties) ARIA.
- **shadcn/ui** مجموعة مكونات (components) تُنسخ إلى مشروعك، مبنية على Radix وTailwind. تشغّل أداة سطر أوامر (CLI) فيصل الكود المصدري (source) *إلى مستودعك (your repo)*، فتملكه وتعدّله. ليست تبعية (dependency) تحدّثها.
- **TanStack Table** محرك جداول بلا واجهة (headless table engine) للفرز (sorting) والتصفية (filtering) والترقيم (pagination). في كل SaaS جدول (table) كبير في مكان ما.
- **Tremor** يقدم رسومًا بيانية (charts) للوحات التحكم (dashboards) وبطاقات المؤشرات الرئيسية (KPI).

### 🟡 التعمق أكثر (Going deeper)

**بنية الإعدادات (settings architecture).** "الإعدادات (settings)" في الحقيقة أربعة أشياء مختلفة لها مالكون (owners) وصلاحيات (permissions) مختلفة. إن خلطتها حصلت على أخطاء أمنية (security bugs) (عضو يغيّر الفوترة (billing)) وأخطاء تجربة استخدام (UX bugs) (مستخدم (user) لا يجد حقل كلمة مروره (password)).

| منطقة الإعدادات (settings area) | النطاق (Scope) | من يستطيع تغييرها (Who can change it) | أمثلة من Beacon (Beacon examples) |
|---|---|---|---|
| الحساب (account) / الملف الشخصي (profile) | المستخدم (user) في كل المؤسسات (orgs) | المستخدم (user) | الاسم، الصورة، كلمة المرور، التحقق بخطوتين (2FA)، تفضيلات الإشعارات (notification prefs) الشخصية، السمة (theme) |
| المؤسسة (organization) | مؤسسة (org) واحدة | Admin/Owner | اسم المؤسسة (organization)، المعرّف المختصر (slug)، الأعضاء والأدوار (members and roles)، SSO، قنوات التنبيه (alert channels) الافتراضية |
| الفوترة (billing) | مؤسسة (org) واحدة | Owner أو دور (role) Billing | الخطة (plan)، وسيلة الدفع (payment method)، الفواتير (invoices)، استهلاك رصيد الرسائل القصيرة (3.1–3.3) |
| المطوّر (developer) | مؤسسة (org) واحدة (أحيانًا لكل مستخدم (user)) | Admin | مفاتيح API (API keys)، الويب هوك (webhooks)، التكاملات (integrations) (5.2، 5.3) |
| منطقة الخطر (danger zone) | مؤسسة (org) واحدة | Owner فقط | نقل الملكية (transfer ownership)، حذف المؤسسة (delete org)، تصدير كل البيانات (export all data) |

ضع إعدادات المستخدم (user settings) على `/settings/account` وإعدادات المؤسسة (org settings) على `/[org]/settings/...`. كل مسار (route) لإعدادات المؤسسة (for org settings) يتحقق من الصلاحيات (permissions) على الخادم (1.3). إخفاء عنصر في القائمة (menu item) ليس تفويضًا (Authorization). والإجراءات المدمّرة (destructive actions) تحتاج تأكيدًا (confirmation) يجبر المستخدم (user) على كتابة اسم المؤسسة (organization).

**التهيئة (onboarding) بوصفها آلة حالات (state machine).** احفظ تقدم التهيئة (onboarding progress) على المؤسسة (organization)، مثل `onboarding_step` أو مجموعة من المراحل المكتملة (completed milestones)، لا في `localStorage`. لا ينبغي أن يُدفع المسؤول الثاني (second admin) في المؤسسة إلى "أنشئ أول مراقبة (monitor) لك" مرة أخرى. سجّل المراحل (milestones) عند حدوثها ("أُنشئت أول مراقبة"، "رُبطت أول قناة تنبيه (alert channel)"، "نُشرت صفحة الحالة (status page)")، واجعل واجهة قائمة المهام (checklist) وتحليلات التفعيل (activation analytics) تعتمدان على المصدر نفسه (source).

**التدويل (i18n) والتنسيق (formatting).** حتى لو أطلقت بالإنجليزية فقط، توقف عن كتابة النصوص مباشرة (hardcoding strings) في المكونات (components) بمجرد أن يصبح لديك عملاء يدفعون (paying customers) في الخارج، و**دائمًا** نسّق التواريخ (dates) والأرقام والعملات (currencies) بواجهات `Intl` حسب لغة المستخدم (locale) ومنطقته الزمنية (time zone). حادثة (incident) "بدأت الساعة 03:14" لا فائدة منها ما لم تقل 03:14 بتوقيت من. المكتبات (libraries): `next-intl`، و`i18next`/`react-i18next`، وFormatJS. وفي Rails نظام I18n مدمج، وفي Django يوجد `gettext`.

**سهولة الوصول (a11y)** تعني أن من يستخدمون لوحة المفاتيح (keyboard) أو قارئات الشاشة (screen readers) أو التكبير (zoom) يستطيعون استخدام تطبيقك (your app). وفي B2B أصبحت متطلبًا للمبيعات (sales requirement) بشكل متزايد. أقسام المشتريات (procurement) في المؤسسات (orgs) تطلب VPAT (وثيقة تصف مدى توافقك (conformance) مع WCAG)، وقانون إتاحة الوصول الأوروبي (European Accessibility Act) يسري على كثير من الخدمات الرقمية (digital services) المبيعة في الاتحاد الأوروبي منذ يونيو 2025. استخدام مكونات (components) مبنية على Radix يعطيك معظم الأجزاء الصعبة. والباقي عليك: تسميات للحقول (labels on inputs)، وحلقات تركيز ظاهرة (visible focus rings)، وتباين ألوان (colour contrast) كافٍ، وأخطاء تُعلَن لقارئات الشاشة، وعدم الاعتماد على اللون وحده لإظهار الحالة. نقاط "متوقف/يعمل" الحمراء والخضراء تحتاج أيقونة (icon) أو نصًا أيضًا. وهذه النقطة مهمة لمنتج مراقبة (monitoring product) بالذات.

### 🔴 على نطاق واسع وللمؤسسات (At scale / enterprise)

**النطاقات المخصصة (custom domains) للصفحات التي يراها المستأجرون.** صفحة الحالة العامة (public status page) في Beacon هي الواجهة الوحيدة (the one surface) التي يراها *عملاء عملائك (your customer's customers)*، لذلك تريدها الشركات على نطاقها الخاص (their own domain): `status.acme.com`. الآلية كالتالي:

1. يُدخل العميل (customer) `status.acme.com` في إعدادات (settings) Beacon.
2. يطلب منه Beacon إنشاء سجل (record) DNS من نوع **CNAME** يوجّه `status.acme.com` إلى شيء مثل `cname.beacon.dev`. وسجل CNAME اسم مستعار (alias) من اسم مضيف (hostname) إلى آخر.
3. يتحقق Beacon منه، إما بفحص (check) DNS أو بطلب سجل TXT إضافي لإثبات الملكية (ownership).
4. تصل الطلبات إلى حافة (edge) Beacon مع `Host: status.acme.com`. يبحث Beacon عن المؤسسة (organization) التي تملك هذا المضيف (host) ويعرض صفحة حالتها (its status page).
5. يحتاج Beacon إلى **شهادة (certificate) TLS** لـ `status.acme.com` تصدر تلقائيًا من Let's Encrypt أو ZeroSSL، لأنك لا تستطيع أن تطلب من كل عميل (customer) رفع شهادات (certificates).

```mermaid
flowchart RL
  V["الزائر<br/>(Visitor)"] --> D["DNS: status.acme.com CNAME cname.beacon.dev"]
  D --> E["وسيط الحافة (Caddy on-demand TLS)<br/>(Edge proxy (Caddy on-demand TLS))"]
  E -->|"أول مصافحة TLS (first TLS handshake)"| A["نقطة ask: هل هذا النطاق موثّق؟<br/>(Ask endpoint: is this domain verified?)"]
  A --> DB[("Postgres custom_domains")]
  E -->|"إصدار الشهادة إن سُمح (issue cert if allowed)"| LE["Let's Encrypt / ZeroSSL"]
  E --> S["تطبيق صفحة الحالة (SSR ومخزّن مؤقتًا)<br/>(Status page app (SSR, cached))"]
  S --> DB
  M["موقع التسويق beacon.dev (ثابت)<br/>(beacon.dev marketing (static))"] --- X["لوحة التحكم app.beacon.dev<br/>(app.beacon.dev dashboard)"]
  X --> DB
```

ثلاث طرق لتحقيق الخطوة 5:

- **Caddy on-demand TLS.** يستطيع Caddy، وهو خادم ويب (web server) مكتوب بلغة Go يدعم HTTPS تلقائيًا، أن يحصل على شهادة (certificate) أثناء *أول مصافحة (handshake) TLS* لاسم مضيف (hostname) لم يره من قبل. **يجب** أن تضبط نقطة نهاية (endpoint) `ask` حتى يسأل Caddy تطبيقك (your app) أولًا. من دونها يستطيع أي شخص توجيه أي نطاق (domain) إلى خادمك (your server) ويجعلك تطلب شهادات (certificates) حتى تصل إلى حدود المعدل (rate limits) لدى جهة إصدار الشهادات (CA).

  ```
  {
    on_demand_tls {
      ask http://localhost:3000/api/domains/allowed
    }
  }
  https:// {
    tls {
      on_demand
    }
    reverse_proxy localhost:3001
  }
  ```

- **واجهة النطاقات (domains API) في منصتك.** تسمح Vercel بإضافة نطاقات (domains) إلى مشروع عبر واجهتها البرمجية (its API). ويستخدم Dub هذا مثلًا لنطاقات الروابط المختصرة (short links) التي تحمل علامة العملاء (branded).
- **Cloudflare for SaaS** (Custom Hostnames) تدير الشهادات (certificates) والحافة (edge) عنك على نطاق Cloudflare (at Cloudflare's scale).

الأجزاء الصعبة على نطاق واسع (at scale) هي التالية. يجب إعادة التحقق دوريًا (re-verify)، لأن العملاء (customers) يحذفون سجلات DNS، وعندها يجب أن تتوقف عن خدمة النطاق (domain). والنطاقات الجذرية (apex domains) (`acme.com` بلا نطاق فرعي (subdomain)) لا تقبل CNAME، لذلك تحتاج سجلات A أو دعم ALIAS/ANAME. وكل طلب يحتاج بحثًا من اسم المضيف (hostname) إلى المؤسسة (organization)، لذلك خزّنه مؤقتًا (cache). ويجب أن تبقى صفحات الحالة (status pages) متاحة *بينما البنية التحتية (infrastructure) للعميل (customer) نفسه متوقفة*. استضفها بعيدًا عن لوحة التحكم (dashboard)، وخزّنها مؤقتًا بقوة على الحافة (edge)، ولا تسمح لنشر لوحة التحكم (dashboard deploy) أن يوقفها.

**العلامة البيضاء (White-labelling)** تذهب أبعد: شعار مخصص (custom logo)، وألوان، ونطاق مُرسِل للبريد (4.1)، وإزالة "Powered by Beacon" في الخطط الأعلى (higher tiers). عامل كل واحدة منها بوصفها استحقاقًا (entitlement) في الخطة (3.2)، لا شرطًا مكتوبًا في الكود (hardcoded) مثل `if (org.plan === "business")`.

## 🏆 أفضل المستودعات (The best repos)

| المستودع (Repo) | ما هو (What it is) | التقنيات (Stack) | الترخيص (License) | اختره عندما (Pick it when) |
|---|---|---|---|---|
| [shadcn-ui/ui](https://github.com/shadcn-ui/ui) | مكونات (components) تُنسخ إلى مستودعك (your repo) مبنية على Radix وTailwind | React, TypeScript | MIT | تريد من اليوم الأول مجموعة مكونات (components) جميلة تملكها |
| [radix-ui/primitives](https://github.com/radix-ui/primitives) | مكونات واجهة أساسية (UI primitives) بلا تنسيق (unstyled) وسهلة الوصول (accessible) | React, TypeScript | MIT | تبني نظام تصميمك (your own design system) الخاص وتريد أن تُحَل سهولة الوصول (accessibility) |
| [tailwindlabs/tailwindcss](https://github.com/tailwindlabs/tailwindcss) | إطار CSS قائم على الأصناف المساعدة (utility classes) | CSS, JS tooling | MIT | التنسيق الافتراضي (default styling) لمعظم واجهات SaaS الجديدة |
| [TanStack/table](https://github.com/TanStack/table) | منطق جداول (tables) وشبكات بيانات (data grids) بلا واجهة | TS (React, Vue, Solid, Svelte…) | MIT | أي قائمة فيها فرز أو تصفية أو ترقيم أو تحديد (selection) |
| [tremorlabs/tremor](https://github.com/tremorlabs/tremor) | رسوم بيانية (charts) ومكونات (components) مؤشرات للوحات التحكم (dashboards) | React, Tailwind | Apache-2.0 | لوحات تحكم يراها العملاء (نسبة التوفر (uptime)، أزمنة الاستجابة (response times)) |
| [react-hook-form/react-hook-form](https://github.com/react-hook-form/react-hook-form) | إدارة حالة نماذج (form state management) عالية الأداء (performant) في React | React, TypeScript | MIT | أي نموذج (form) غير بسيط، مع محلّل مخطط (schema resolver) |
| [colinhacks/zod](https://github.com/colinhacks/zod) | تحقق من المخططات (schema validation) مصمم أولًا لـ TypeScript | TypeScript | MIT | مخطط (schema) واحد يتشاركه المتصفح (browser) والخادم (server) |
| [vercel/next-forge](https://github.com/vercel/next-forge) | قالب (starter) SaaS جاهز للإنتاج (production-ready) مبني على Turborepo | Next.js monorepo | MIT | تريد أن ترى التسويق (marketing) والتطبيق (app) والـ API مقسمة إلى تطبيقات (apps) منفصلة |
| [caddyserver/caddy](https://github.com/caddyserver/caddy) | خادم ويب (web server) مع HTTPS تلقائي وon-demand TLS | Go | Apache-2.0 | نطاقات مخصصة (custom domains) مستضافة ذاتيًا (self-hosted) لصفحات المستأجرين (tenants) |

**إن درست مستودعًا واحدًا فقط (If you only study one):** ادرس **next-forge**. ليس مكتبة مكونات (component library)، لكنه يعرض الهيكل (shell) كاملًا في مستودع (repo) واحد: تطبيقات (apps) منفصلة للتسويق (marketing) والمنتج (product) والـ API، ومجلد `packages/` مشترك للواجهة (UI) والمصادقة (auth)، والربط بينها. اقرأ بنية مجلداته قبل أن تنشئ مستودعك الأحادي (your own monorepo).

**اشترِ أم ابنِ أم استضف بنفسك (Buy, build, or self-host)؟**

- **اشترِ (Buy)** شهادات TLS (TLS certificates) للنطاقات المخصصة (custom domains) عندما تكون أصلًا على منصة تبيعها: نطاقات (domains) Vercel، وCloudflare for SaaS. ولمواقع التسويق (marketing sites)، يكفي نظام إدارة محتوى (CMS) أو أداة بناء مواقع (Webflow أو Framer أو CMS بلا واجهة)، وهذا يُخرج المهندسين (engineers) من تعديلات النصوص (copy changes).
- **استضف بنفسك (Self-host)** Caddy مع on-demand TLS عندما تدير بنيتك التحتية (your own infrastructure) الخاصة أو تتوقع آلاف نطاقات (domains) العملاء (customers) وتريد التحكم في الكلفة (cost).
- **ابنِ (Build)** الهيكل (shell) نفسه (التخطيط (layout)، التهيئة (onboarding)، الإعدادات (settings)) فوق shadcn/ui وRadix وTailwind. هذا وجه منتجك (your product)، فامتلك الكود (code). لكن لا تبنِ مكتبة نماذج (form library) أو محرك جداول (table engine) أو قائمة منسدلة (dropdown) سهلة الوصول (accessible) من الصفر.

## 🔍 ادرسه في مشاريع حقيقية (Study it in the wild)

**dubinc/dub.** هيكل جيد للتعلم منه: مبدّل مساحات العمل (workspace switcher)، ولوحة تحكم مصقولة (polished)، و**نطاقات مخصصة (custom domains) للعملاء (customers)** للروابط المختصرة (short links). افتح المستودع (repo) واستخدم البحث في الكود (code search) عن `domains` مع `vercel` لتجد أين يضيف Dub النطاقات (domains) ويتحقق منها عبر واجهة Vercel. وقت كتابة هذا الدرس يعيش المنتج (product) في `apps/web`. لاحظ كيف يقرر التطبيق (app) بين سلوك التسويق (marketing) ولوحة التحكم (dashboard) وإعادة توجيه الروابط (link redirects) حسب اسم المضيف (hostname) الوارد.

**openstatusHQ/openstatus.** نسخة حقيقية من Beacon: مراقب توفر (uptime monitor) مفتوح المصدر (open-source) مع صفحات حالة (status pages) عامة. ابحث عن `custom domain` و`status page` لترى كيف تُحدَّد الصفحة من اسم المضيف (hostname) أو المعرّف المختصر (slug). وقارن طريقة تصيير صفحة الحالة (status page) بطريقة تصيير لوحة التحكم (dashboard) الخاصة بالمستخدمين المسجلين (logged-in users).

**calcom/cal.diy.** مسار التهيئة (onboarding flow) وتقسيم الإعدادات (settings) في Cal.com يستحقان القراءة. ابحث عن `getting-started` أو `onboarding` لتجد مسار الاستخدام الأول (first-run flow) خطوة بخطوة، وتصفح صفحات الإعدادات (settings pages) لترى كيف تبقى إعدادات الحساب (account-level settings) منفصلة عن إعدادات الفريق والمؤسسة (organization).

**vercel/next-forge.** هنا الهيكل (shell) *هو* المنتج (product). انظر إلى مجلد `apps/` في المستوى الأعلى (top-level): التسويق (marketing) وتطبيق (app) المنتج تطبيقا Next.js منفصلان يتشاركان `packages/`. لاحظ ما يُعدّ "مشتركًا" (نظام التصميم (design system)، المصادقة (auth)، التحليلات (analytics)) وما لا يُعدّ كذلك.

**ما الذي تلاحظه (What to notice):**

- معرّف المؤسسة أو مساحة العمل (workspace) موجود في الرابط (URL)، وكل صفحة وكل استدعاء API يستنتج المستأجر (tenant) منه ومن الجلسة (session)، لا من حالة المتصفح (client state) وحدها.
- صفحات التسويق (marketing pages) مُصيَّرة ثابتًا أو مخزّنة مؤقتًا (cached). ولوحة التحكم (dashboard) لا تفهرسها (noindex) محركات البحث (search engines).
- طلبات النطاقات المخصصة (custom domains) تُوجَّه حسب ترويسة (header) `Host` مبكرًا، غالبًا في البرمجية الوسيطة (Middleware)، قبل تشغيل أي منطق للصفحة.
- الحالات الفارغة (empty states) شاشات مصممة فيها دعوة واحدة واضحة لاتخاذ إجراء (call to action)، لا جدول (table) فارغ.
- مخططات التحقق (validation schemas) يستوردها مكوّن النموذج (form component) ومعالج الخادم (server handler) معًا.

## 🛠️ ابنِه في Beacon (Build it into Beacon)

### 🟢 تمرين المبتدئ (Beginner exercise)

ابنِ (Build) التخطيط الخاص بالمستخدمين المسجلين (authenticated layout) في Beacon باستخدام shadcn/ui: شريط جانبي (المراقبات (monitors)، الحوادث (incidents)، صفحات الحالة (status pages)، الإعدادات (settings))، ومبدّل مؤسسات (org switcher) يغيّر جزء `/[org]/...` في الرابط (URL)، وحالة فارغة (empty state) في صفحة المراقبات فيها زر واحد "أضف أول مراقبة (monitor) لك" يفتح نموذجًا (form) يُتحقق منه بمخطط (schema) zod مشترك.

**يكتمل عندما (Done when):**
- يغيّر تبديل المؤسسة (organization) الرابط (URL)، وتبقيك إعادة تحميل الصفحة في المؤسسة نفسها.
- يعرض إرسال رابط غير صالح (invalid URL) خطأً بجانب الحقل دون أي طلب شبكة (network request)، *و*يرفض الخادم (server) الحمولة (payload) الخاطئة نفسها عند إرسالها بـ `curl` بالرسالة نفسها.
- يعمل المسار كله بلوحة المفاتيح (keyboard) فقط (Tab وEnter، وEscape يغلق نافذة الحوار (dialog)).

### 🟡 تمرين المستوى المتوسط (Intermediate exercise)

قسّم الإعدادات (settings) إلى الحساب (`/settings/account`)، والمؤسسة (`/[org]/settings/general`، `/members`)، والفوترة (billing)، والمطوّر (مفاتيح API (API keys)). أضف قائمة مهام للتهيئة (onboarding checklist) تعتمد على مراحل محفوظة على المؤسسة: أول مراقبة (monitor)، أول قناة تنبيه (alert channel)، نشر صفحة الحالة (status page published). تختفي القائمة تلقائيًا عندما تكتمل المراحل (milestones) الثلاث.

**يكتمل عندما (Done when):**
- يحصل دور (role) Member على 403 من الخادم (server) عند استدعاء نقطة إعادة تسمية المؤسسة (org-rename endpoint) مباشرة، لا مجرد زر مخفي.
- لا يرى المسؤول الثاني (second admin) الذي ينضم بعد اكتمال التهيئة (onboarding) قائمة المهام (checklist) أبدًا.
- تُحفظ أوقات المراحل (milestone timestamps)، حتى تحسب لاحقًا "الوقت حتى التفعيل (time-to-activation)" (6.2).

### 🔴 تمرين المستوى المتقدم (Advanced exercise)

أطلق النطاقات المخصصة (custom domains) لصفحات الحالة (status pages). أضف جدول (table) `custom_domains` (`org_id`، `hostname`، `verified_at`، `last_checked_at`)، وصفحة إعدادات (settings page) تعرض سجل CNAME المطلوب إنشاؤه، ومهمة تحقق (5.1) تعيد فحص (check) DNS يوميًا، وإعداد Caddy فيه `on_demand_tls` بحيث لا تعيد نقطة `ask` القيمة 200 إلا لأسماء المضيفين (hostnames) الموثقة (verified).

**يكتمل عندما (Done when):**
- يخدم `status.yourtestdomain.com` صفحة حالة (status page) المؤسسة (organization) الصحيحة عبر HTTPS صالح دون أي خطوة يدوية للشهادة (certificate).
- توجيه نطاق غير مسجل (unregistered domain) إلى الخادم (server) **لا** يطلق طلب شهادة (certificate request) (راجع سجلات Caddy (Caddy's logs)).
- حذف سجل DNS يجعل النطاق (domain) غير موثق خلال يوم، فيتوقف تقديمه.

## ⚠️ أخطاء يقع فيها المبتدئون (Mistakes juniors make)

- **تقديم موقع التسويق (marketing site) من تطبيق الصفحة الواحدة (SPA) الخاص بالمستخدمين المسجلين (logged-in users).** ترى محركات البحث (search engines) مؤشر تحميل (spinner)، وكل تعديل على النص (copy change) يمر بنشر التطبيق (app's deploy). افصلهما: تسويق ثابت أو مُصيَّر على الخادم (server-rendered)، والتطبيق (app) على نطاق فرعي (subdomain) خاص به.
- **حفظ المؤسسة الحالية (current org) في حالة React أو `localStorage` فقط.** إعادة التحميل والروابط (links) المشتركة والتبويبات الجديدة (tabs) كلها تبدّل المستأجر (tenant) بصمت، وهذا على بعد خطوة من خطأ تسرب بين المستأجرين (cross-tenant leak). ضع معرّف المؤسسة في الرابط (org slug in the URL) وتحقق من العضوية (membership) على الخادم (server) في كل طلب.
- **التحقق في المتصفح (client-side validation) فقط.** المتصفح (browser) ليس حدًا أمنيًا (security boundary). شارك مخططًا (schema) واحدًا وشغّله دائمًا على الخادم (server)، ثم تحقق من الصلاحيات (1.3) وحدود الخطة (3.2) بعد ذلك.
- **اعتبار "إخفاء الزر" صلاحيات (permissions).** زر الحذف (deletion) المخفي ما زالت نقطة نهايته (its endpoint) تعمل. فحوص الخادم (server-side checks) تأتي أولًا، والواجهة (UI) تعكسها فقط.
- **تفعيل on-demand TLS دون فحص (check) `ask`.** يستطيع أي شخص توجيه DNS إليك ويجعلك تطلب شهادات (certificates) لأسماء عشوائية، فتستهلك حدود المعدل (rate limits) لدى جهة الإصدار (CA). اربطه دائمًا ببحث عن نطاق موثّق (verified domain).
- **تنسيق التواريخ (dates) بتوقيت الخادم (server time).** حادثة (incident) في "14:00" لا تعني شيئًا لعميل (customer) يبعد ثماني مناطق زمنية (time zones). احفظ بتوقيت UTC ونسّق بـ `Intl` حسب المنطقة الزمنية (time zone) للمشاهد.
- **بناء القوائم المنسدلة (dropdowns) والنوافذ المنبثقة (modals) بنفسك.** ستخطئ في إدارة التركيز (focus management) وسلوك قارئات الشاشة (screen readers). استخدم Radix أو shadcn/ui واصرف الوقت على حالاتك الفارغة (your empty states) بدلًا من ذلك.

## 🧾 الخلاصة (Recap)

- هيكل التطبيق (موقع التسويق (marketing site)، التخطيط (layout)، التهيئة (onboarding)، الإعدادات (settings)، نظام التصميم (design system)) هو نفسه في كل SaaS، والعملاء (customers) يحكمون عليك من خلاله.
- افصل التسويق (ثابت أو على الخادم (server)، محركات البحث (search engines)، غير المهندسين (non-engineers)) عن التطبيق (يتطلب الدخول (login)، والمستأجر (tenant) في الرابط (URL))، وعادة يكونان تطبيقين (apps) منفصلين في مستودع أحادي (monorepo) واحد.
- صمّم الحالة الفارغة (empty state) والتهيئة (onboarding) حول حدث **تفعيل** واحد، واحفظ التقدم على المؤسسة (organization).
- الإعدادات (settings) أربعة أنواع بصلاحيات (permissions) مختلفة: الحساب (account)، والمؤسسة (organization)، والفوترة (billing)، والمطوّر (developer). إضافة إلى منطقة الخطر (danger zone).
- مخطط تحقق (validation schema) واحد يتشاركه المتصفح (browser) والخادم (server). ونسخة الخادم هي التي تُحتسب.
- النطاقات المخصصة (custom domains) تعني: CNAME، وتحققًا (verification)، وTLS تلقائيًا (Caddy on-demand مع `ask`، أو Vercel، أو Cloudflare for SaaS)، وتوجيهًا حسب اسم المضيف (hostname).

## ✍️ اختبر نفسك (Check yourself)

**1. لماذا يجب أن يكون موقع التسويق (marketing site) والتطبيق (app) منفصلين، وما الذي يحتاجه كل منهما؟**

<details><summary>الإجابة (Answer)</summary>

احتياجاتهما متعاكسة. موقع التسويق (marketing site) يخدم زوارًا مجهولين (anonymous visitors) ومحركات البحث (search engines)، لذلك يكون ثابتًا أو مُصيَّرًا على الخادم (server-rendered)، وغالبًا يعدّله غير المهندسين (non-engineers). أما التطبيق (app) فيخدم مستخدمين مسجلين (logged-in users)، ويمكن أن يعتمد على المتصفح (browser)، ويضع كل شيء خلف فحص الجلسة (session check). راجع جدول (table) المقارنة في 🟢 الأساسيات (The essentials).

</details>

**2. ما التفعيل (activation)، ولماذا يهم في التهيئة (onboarding)؟**

<details><summary>الإجابة (Answer)</summary>

التفعيل (activation) هو الحدث (event) الذي يعني أن المستخدم (user) جرّب فعلًا قيمة المنتج (product)، وفي Beacon هو شيء مثل "أنشأ مراقبة (monitor) وتلقى أول نتيجة فحص (check result) خلال 24 ساعة". تختار حدثًا واحدًا، وتتتبعه، وتصمم التهيئة (onboarding) والحالات الفارغة (empty states) لإيصال الناس إليه. راجع "التهيئة والحالات الفارغة" في 🟢 الأساسيات (The essentials).

</details>

**3. عضو في Beacon يريد تغيير وسيلة الدفع (payment method) للمؤسسة (organization). في أي منطقة إعدادات (settings area) يقع هذا، وكيف يفرض Beacon من يستطيع فعله؟**

<details><summary>الإجابة (Answer)</summary>

إنها منطقة الفوترة (billing)، ونطاقها مؤسسة (org) واحدة، ولا يغيّرها إلا Owner أو دور (role) Billing. يجب أن يتحقق مسار إعدادات المؤسسة (org settings) من الصلاحية (permission) على الخادم (1.3)، لأن إخفاء عنصر القائمة (menu item) ليس تفويضًا (authorization). راجع جدول (table) الإعدادات (settings) في 🟡 التعمق أكثر (Going deeper).

</details>

**4. تريد Acme أن تكون صفحة حالتها (its status page) في Beacon على `status.acme.com`. ما الخطوات؟**

<details><summary>الإجابة (Answer)</summary>

تنشئ Acme سجل CNAME من `status.acme.com` إلى شيء مثل `cname.beacon.dev`، ويتحقق Beacon منه عبر DNS أو سجل TXT. بعد ذلك يوجّه Beacon الطلبات حسب ترويسة (header) `Host` إلى صفحة حالة (status page) Acme، ويصدر شهادة (certificate) TLS تلقائيًا، مثلًا باستخدام Caddy on-demand TLS أو واجهة النطاقات (domains API) في Vercel أو Cloudflare for SaaS. راجع 🔴 على نطاق واسع وللمؤسسات (At scale / enterprise).

</details>

**5. يفعّل مطوّر (developer) خيار `on_demand` في Caddy لكنه يترك نقطة `ask` ليوفر الوقت. ما الذي ينكسر؟**

<details><summary>الإجابة (Answer)</summary>

يستطيع أي شخص توجيه أي نطاق (domain) إلى خادم (server) Beacon، فيطلب Caddy شهادة (certificate) له أثناء أول مصافحة (handshake) TLS. ويستطيع المهاجم أن يجعلك تطلب شهادات (certificates) لأسماء عشوائية حتى تصل إلى حدود المعدل (rate limits) لدى جهة الإصدار (CA)، وهذا يمنع العملاء (customers) الحقيقيين أيضًا. يجب ألا تعيد نقطة `ask` القيمة 200 إلا لأسماء المضيفين (hostnames) الموثقة. راجع بند Caddy في 🔴 على نطاق واسع وللمؤسسات (At scale / enterprise) وقسم ⚠️ أخطاء يقع فيها المبتدئون (Mistakes juniors make).

</details>

## 📚 المراجع (References)

- shadcn/ui documentation — توثيق shadcn/ui: https://ui.shadcn.com
- Radix Primitives documentation, including accessibility notes per component — توثيق Radix مع ملاحظات سهولة الوصول (accessibility) لكل مكوّن (component): https://www.radix-ui.com/primitives
- Zod documentation — توثيق Zod: https://zod.dev
- React Hook Form documentation — توثيق React Hook Form: https://react-hook-form.com
- Caddy documentation on automatic HTTPS and on-demand TLS — توثيق Caddy عن HTTPS التلقائي وon-demand TLS: https://caddyserver.com/docs/automatic-https
- Cloudflare for SaaS documentation — توثيق Cloudflare for SaaS: https://developers.cloudflare.com/cloudflare-for-platforms/cloudflare-for-saas/
- W3C Web Content Accessibility Guidelines (WCAG) overview — نظرة عامة على إرشادات WCAG: https://www.w3.org/WAI/standards-guidelines/wcag/
- next-forge documentation — توثيق next-forge: https://www.next-forge.com

---

# 6.2 — التحليلات (analytics): تحليلات المنتج (product analytics) والويب وخط الأحداث (event pipeline)

*المستوى (Level): 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 1.2، 6.1*

## ⚡ الدرس في دقيقة (In 60 seconds)

- التحليلات (analytics) ثلاث وظائف: تحليلات الويب (web analytics) (من يزور موقع التسويق (marketing site))، وتحليلات المنتج (product analytics) (ماذا يفعل المستخدمون (users) داخل التطبيق (app))، وذكاء الأعمال (business intelligence) BI (كل أنظمتك مجموعة في مستودع بيانات (data warehouse)).
- القاعدة الأهم (The rule that matters most): اكتب خطة تتبع (tracking plan) بأسماء أحداث (event names) على شكل object_action قبل أن ترسل أي حدث، وأرسل استدعاءات (calls) `group` حتى تستطيع التحليل حسب المؤسسة (organization).
- الخيار الافتراضي للنسخة الأولى (The v1 default): تحليلات ويب (web analytics) بلا ملفات ارتباط (cookieless) (Plausible أو Umami) على موقع التسويق (marketing site)، وPostHog (أو ما يشبهه) داخل التطبيق (app)، مع إرسال أحداث الأعمال (business events) من الخادم (server).
- أبقِ البيانات الشخصية (PII) خارج خصائص الأحداث (event properties). أرسل المعرّفات (ids)، واحترم الموافقة (consent)، واعرف كيف تحذف أداتك أحداث (events) مستخدم (user) ما.
- الفخ الأكبر (The biggest trap): تتبّع كل شيء بلا خطة (plan)، أو تشغيل استعلامات التحليلات (analytics queries) على Postgres الإنتاجي (production). الأحداث كبيرة الحجم (high-volume events) مكانها مخزن (store) مثل ClickHouse، مع تقييد كل استعلام (query) بالمستأجر (tenant).

## 🧭 لماذا يحتاجه كل SaaS (Why every SaaS has this)

يبدأ مؤسسو Beacon اجتماعهم الأسبوعي (weekly meeting) بسؤال بسيط: "هل تعمل التهيئة الجديدة (onboarding)؟" لا أحد يستطيع الإجابة (Answer). لوحة (dashboard) Stripe تعرض الإيرادات (revenue). وجدول (table) `monitors` في Postgres يعرض عدد المراقبات (monitors) الموجودة. وGoogle Analytics يعرض أن 4,000 شخص زاروا صفحة الأسعار (pricing page). لكن لا أحد يستطيع أن يقول كم من المسجلين (signups) في الأسبوع الماضي أنشأ مراقبة (monitor)، وكم استغرق ذلك، وهل تبقى الفرق التي تربط Slack مدة أطول من الفرق التي لا تربطه.

فيضيف مهندس `track("clicked button")` في أربعين مكانًا. وبعد شهر تحتوي قائمة الأحداث (event list) على `Monitor Created` و`monitor_created` و`createMonitor` و`new-monitor`، وكلها تعني الشيء نفسه تقريبًا، ولا يسجل أيٌّ منها المؤسسة (organization) التي ينتمي إليها المستخدم (user). وفي منتج (product) B2B هذا هو الرقم الذي يهمك فعلًا، لأن *المؤسسة* هي التي تدفع لك، لا المستخدم.

**التحليلات (Analytics) هي المكوّن الذي يحوّل "نظن" إلى "قسنا"، ولا تعمل إلا إذا قررت ماذا تقيس وكيف تسميه قبل أن تبدأ بإرسال الأحداث (events).**

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

كلمة "التحليلات (analytics)" تغطي ثلاث وظائف مختلفة يخلط الناس بينها:

| النوع (Type) | السؤال الذي يجيب عنه (Question it answers) | الوحدة (Unit) | مثال من Beacon (Beacon example) | الأدوات (Tools) |
|---|---|---|---|---|
| **تحليلات الويب (web analytics)** | من يزور موقع التسويق (marketing site)، ومن أين؟ | مشاهدات الصفحات (pageviews) والجلسات (sessions) | أي مقال في المدونة (blog post) يجلب التسجيلات (signups)؟ | Plausible, Umami, Matomo |
| **تحليلات المنتج (product analytics)** | ماذا *يفعل* المستخدمون المسجلون (logged-in) داخل التطبيق (app)؟ | أحداث (events) حسب المستخدمين (users) والمؤسسات (orgs) | نسبة المؤسسات (orgs) الجديدة التي تنشئ مراقبة (monitor) خلال 24 ساعة | PostHog, OpenPanel, Amplitude, Mixpanel |
| **ذكاء الأعمال (business intelligence) / مستودع البيانات (data warehouse)** | كيف يبدو العمل عبر كل الأنظمة؟ | جداول مدموجة (joined tables) | الإيراد (revenue) لكل مؤسسة (org) مقابل المراقبات (monitors) مقابل تذاكر الدعم (support tickets) | مستودع بيانات (data warehouse) + dbt + أداة (tool) BI (Metabase, Superset) |

تحليلات الويب (web analytics) رخيصة وشبه تلقائية: ضع وسم سكربت (script tag) على موقع التسويق (marketing site). أما تحليلات المنتج (product analytics) فتحتاج **أحداثًا (events)** مقصودة. الحدث (Event) سجل بأن شيئًا ما حدث: من (معرّف المستخدم (user id))، وأي مؤسسة (org)، وماذا (اسم الحدث (event name))، ومتى (الطابع الزمني (timestamp))، إضافة إلى **خصائص** (Properties)، وهي تفاصيل على شكل مفتاح وقيمة (key-value) مثل `check_interval: 60`.

نموذج البيانات (data model) الذي تتشاركه معظم الأدوات (tools) مأخوذ من مواصفة (spec) Segment، وهي معيار فعلي (de facto standard):

- **`identify(userId, traits)`** تقول "هذا المتصفح (browser) أو الجهاز هو المستخدم (user) `u_123`، وبريده ...". وهي تربط النشاط المجهول (anonymous activity) قبل التسجيل بالمستخدم الحقيقي.
- **`track(event, properties)`** تقول "فعل المستخدم (user) كذا".
- **`page()` / `screen()`** تسجل مشاهدة صفحة (page view).
- **`group(groupId, traits)`** تقول "هذا المستخدم (user) ينتمي إلى المؤسسة (organization) `org_42` على خطة (plan) Pro". **هذا هو الاستدعاء الذي ينساه SaaS الموجّه للشركات (B2B)**، وهو ما يسمح لك بطرح الأسئلة لكل حساب بدل كل شخص. ويسميه PostHog تحليلات المجموعات (Group Analytics).

**خطة التتبع (Tracking Plan)** وثيقة قصيرة، غالبًا جدول (table) بيانات، تسرد كل حدث (every event) وخصائصه (its properties) وسبب وجوده. استخدم **تسمية object–action (object–action naming)**: الاسم ثم فعل بصيغة الماضي (past-tense)، بنمط كتابة (casing) واحد ثابت. `monitor_created`، `alert_channel_connected`، `status_page_published`، `subscription_upgraded`. عندها تستطيع قراءة القائمة أبجديًا حسب الكائن، ولا يخترع أحد `createMonitor`.

| الحدث (Event) | الخصائص الأساسية (Key properties) | لماذا نتتبعه (Why we track it) |
|---|---|---|
| `org_created` | `signup_source` | رأس كل قُمع (funnel) |
| `monitor_created` | `check_interval`، `type`، `is_first` | خطوة التفعيل (activation step) 1 |
| `monitor_check_completed` | `status` (فقط *أول* فحص (check) لكل مراقبة (monitor)) | خطوة التفعيل (activation step) 2: وصلت القيمة |
| `alert_channel_connected` | `channel` (email/slack/sms) | مؤشر قوي على الاحتفاظ (retention) يستحق الاختبار (test) |
| `subscription_upgraded` | `from_plan`، `to_plan` | الإيراد (revenue) |

بهذه الأحداث (events) تستطيع بناء الرسوم الثلاثة التي يعيش عليها كل SaaS:

- **القُمع (Funnel)**: من المؤسسات (orgs) التي أُنشئت هذا الأسبوع، ما النسبة التي أنشأت مراقبة (monitor)، ثم حصلت على نتيجة فحص (check result)، ثم ربطت قناة تنبيه (alert channel)؟
- **معدل التفعيل (activation rate)**: نسبة المؤسسات (orgs) الجديدة التي تصل إلى حدث التفعيل (activation event) (6.1) خلال N يومًا.
- **الاحتفاظ (Retention)**: من المؤسسات (orgs) التي سجلت في الأسبوع W، ما النسبة التي بقيت نشطة (active) في الأسابيع W+1 وW+2...؟ يُرسم هذا عادة بوصفه جدول أفواج (Cohort Table). ويجب أن يكون "النشاط" حدث قيمة (value event) حقيقيًا، مثل "شاهد لوحة التحكم (dashboard) أو تلقى تنبيهًا (alert)"، لا "سجّل الدخول (login)".

### 🟡 التعمق أكثر (Going deeper)

**التتبع في المتصفح (client-side tracking) مقابل التتبع على الخادم (server-side tracking).** التتبع في المتصفح يعني أن حزمة SDK (SDK) في المتصفح (browser) ترسل الأحداث (events). هي ترى النقرات (clicks) ومشاهدات الصفحات (page views)، لكن مانعات الإعلانات (ad blockers) وإضافات الخصوصية (privacy extensions) تحجب جزءًا حقيقيًا منها، ويستطيع المستخدمون (users) تزويرها (forge). والتتبع على الخادم يعني أن الخادم (server) يرسل الأحداث بعد أن يحدث الشيء فعلًا في قاعدة البيانات (database). هو موثوق وكامل، لكنه لا يرى تفاعلات الواجهة (UI interactions) البحتة. القاعدة: **أحداث الأعمال (business events) تُتتبع على الخادم** (`monitor_created` يُطلق بعد تثبيت الإدراج (insert commits)، و`subscription_upgraded` يُطلق من معالج ويب هوك (webhook handler) Stripe في 3.1)، و**سلوك الواجهة (UI behaviour) يُتتبع في المتصفح** (فتح لوحة الأوامر (command palette)، إغلاق قائمة المهام (checklist)). وكثير من الفرق تمرّر SDK المتصفح (browser SDK) عبر نطاقها الخاص (own domain) حتى تكون المانعات أقل صرامة. كن صادقًا مع نفسك في سبب فعل ذلك، وراجع النقطة التالية.

```mermaid
flowchart RL
  B["SDK المتصفح (أحداث الواجهة)<br/>(Browser SDK (UI events))"] --> C["المُجمِّع أو CDP<br/>(Collector or CDP)"]
  S["الخادم (أحداث الأعمال)<br/>(Backend (business events))"] --> C
  W["ويب هوك Stripe<br/>(Stripe webhooks)"] --> S
  C --> P["تحليلات المنتج (PostHog)<br/>(Product analytics (PostHog))"]
  C --> WH[("مستودع البيانات أو ClickHouse<br/>(Warehouse or ClickHouse)")]
  DB[("قاعدة بيانات التطبيق Postgres<br/>(Postgres app DB)")] -->|"مزامنة ELT (ELT sync)"| WH
  WH --> BI["لوحات BI<br/>(BI dashboards)"]
  WH -->|"ETL عكسي (reverse ETL)"| CRM["أدوات CRM والبريد<br/>(CRM and email tools)"]
```

**الخصوصية والموافقة (privacy and consent).** في الاتحاد الأوروبي والمملكة المتحدة، تشترط قواعد (rules) ePrivacy الحصول على موافقة (consent) قبل تخزين أو قراءة بيانات غير ضرورية على جهاز المستخدم (ملفات الارتباط (cookies)، ومعرّفات `localStorage`)، ويحكم GDPR البيانات الشخصية (personal data) نفسها (8.1). عمليًا:

- تحليلات الويب (web analytics) بلا ملفات ارتباط (cookieless) مثل Plausible، التي تستخدم تجزئة (Hash) لعنوان IP مع وكيل المستخدم (user agent) وملحًا (Salt) يتغير يوميًا ولا تخزن أي ملف ارتباط (cookie)، مصممة عمومًا بحيث لا تحتاج شريط موافقة (consent banner). تحقق من ذلك مع مستشارك القانوني (lawyer).
- تحليلات المنتج (product analytics) التي تعرّف المستخدمين (users) *داخل* تطبيقك (your app) معالجة لبيانات شخصية (personal data processing). غطّها في سياسة الخصوصية (privacy policy) واتفاقية معالجة البيانات (DPA)، وأدرج المزوّد (vendor) بوصفه معالجًا فرعيًا (subprocessor) (8.1)، ولا ترسل بيانات لا تحتاجها. **لا تضع أبدًا البريد الإلكتروني أو الأسماء أو روابط المراقبات (monitor URLs) في خصائص الأحداث (event properties) إلا إذا احتجتها فعلًا.** استخدم المعرّفات (IDs).
- أدوات (tools) إعادة تشغيل الجلسات (session replay) تسجّل الشاشات. أخفِ كل الحقول (mask) افتراضيًا.
- ادعم الحذف (deletion). عندما يمارس المستخدم (user) حق المحو (right to erasure) في GDPR، يجب أن تكون أحداثه (their events) قابلة للحذف أيضًا. اعرف كيف تفعل أداة التحليلات (analytics tool) هذا قبل أن تختارها.

**خط الأحداث (event pipeline) ومنصات CDP.** **منصة بيانات العملاء (CDP — Customer Data Platform)** مثل RudderStack أو Jitsu أو Segment تجمع الأحداث (events) مرة واحدة وتوزعها على وجهات (destinations) كثيرة: تحليلات المنتج (product analytics)، ومستودع البيانات، وCRM، وأداة البريد (email tool). وهي تمنعك من تثبيت خمس حزم SDK (SDKs). و**مستودع البيانات (Data Warehouse)** (BigQuery أو Snowflake أو Postgres أو ClickHouse) هو المكان الذي تلتقي فيه الأحداث ببيانات تطبيقك (your app). تزامن جداول (tables) Postgres إليه بطريقة ELT (استخراج ثم تحميل ثم تحويل (extract, load, transform) بـ SQL، غالبًا باستخدام dbt)، فتستطيع دمج "الأحداث" مع "المؤسسات (orgs)" و"فواتير Stripe". و**ETL العكسي (Reverse ETL)** يدفع الخصائص المحسوبة (computed traits) إلى الخارج، مثل "هذه المؤسسة (organization) وصلت إلى 90% من حد المراقبات (monitors)" إلى CRM حتى يتصل بها فريق المبيعات (sales).

### 🔴 على نطاق واسع وللمؤسسات (At scale / enterprise)

**لماذا يظهر ClickHouse دائمًا.** استعلامات التحليلات (analytics queries) تشبه "عدّ الأحداث (events) مجمّعة حسب اليوم (grouped by day)، مصفّاة (filtered) حسب المؤسسة (organization)، خلال 90 يومًا، عبر مليارات الصفوف (rows)". مخزن صفوف (row store) مثل Postgres يقرأ الصفوف كاملة ويبطئ كثيرًا هنا. أما **ClickHouse** فقاعدة بيانات عمودية (Column-oriented): تخزن كل عمود (column) على حدة ومضغوطًا (compressed)، فالاستعلام (query) الذي يلمس ثلاثة أعمدة (columns) يقرأ تلك الثلاثة فقط، ويجمّع (aggregates) بسرعة كبيرة. وPostHog وPlausible وOpenPanel كلها تخزن أحداثها (their events) في ClickHouse. المقايضات (trade-offs): يفضّل ClickHouse عمليات الإدراج الكبيرة على دفعات (large batched inserts) بدل كتابة صف واحد (single row)، والتحديثات والحذف (updates and deletes) مكلفة وتتم عمليات في الخلفية (وهذا مهم لحذف GDPR (GDPR deletion))، وهو ليس قاعدة بيانات معاملات (transactional database) لتطبيقك (your app). أبقِ Postgres للتطبيق (app) وClickHouse للأحداث.

**التحليلات التي يراها العملاء (customer-facing analytics).** سيأتي يوم *يبيع* فيه Beacon التحليلات (analytics): نسبة التوفر (uptime)، ورسوم زمن الاستجابة (latency)، وعدد مشاهدات صفحة الحالة (status-page view counts) لكل عميل (customer). عندها تصبح التحليلات ميزة (feature) في المنتج (product) لها حد مستأجر (tenant boundary) ومتطلبات زمن استجابة وحدود خطط (plan limits) (Free تحتفظ بتاريخ 7 أيام، وBusiness بسنة). وDub مثال جيد، فهو يعرض تحليلات النقرات (click analytics) لعملائه ويستخدم **Tinybird**، وهي خدمة مُدارة (managed service) مبنية على ClickHouse تعرض استعلامات (queries) SQL بوصفها نقاط نهاية (endpoints) API (API endpoints). مهما اخترت، يجب أن يُصفّى كل استعلام (query) بـ `org_id` على الخادم (server). عزل المستأجرين (tenant isolation) (2.4) ينطبق على مخزن التحليلات (analytics store) تمامًا كما ينطبق على Postgres. وصفوف `monitor_check_completed` في Beacon، صف لكل فحص (check) كل 30 ثانية لكل مراقبة (monitor)، مثال نموذجي على جدول (table) ClickHouse: إضافة فقط (append-only)، سلسلة زمنية (time-series)، ومجمّعة حسب فترات زمنية.

**جودة البيانات (data quality) على نطاق واسع (at scale).** خطط التتبع (tracking plans) تتقادم (rot). افرضها بدوال تتبع مُنمَّطة (typed tracking functions) تُولَّد من الخطة (`track.monitorCreated({ checkInterval })`)، أو بفحوص في CI (CI checks)، أو بتحقق من المخطط (schema validation) داخل خط الأحداث (event pipeline) يرفض الأحداث (events) المجهولة. أعطِ الأحداث إصدارات (versions) عندما يتغير معناها (`monitor_created` v2) بدل إعادة تعريفها بصمت. وراقب الكلفة (cost) أيضًا: تسعير (pricing) تحليلات المنتج (product analytics) عادة لكل حدث (every event)، وحزمة SDK (SDK) ثرثارة (chatty) مع الالتقاط التلقائي (Autocapture) قد تضاعف فاتورتك (bill) دون أن يطرح أحد سؤالًا جديدًا.

**حل الهوية (identity resolution) في B2B.** ينتمي المستخدمون (users) إلى عدة مؤسسات (orgs)، ويغيّرون بريدهم، ويُجهَّزون (provisioned) عبر SCIM (1.4). أرسل المؤسسة (organization) دائمًا بوصفها مجموعة مع كل حدث (every event)، لا وقت `identify` فقط. واحتفظ بمعرّف مستخدم داخلي ثابت (stable internal user ID)، لا البريد أبدًا، بوصفه المعرّف المميز (distinct id). وقرّر لأي مؤسسة (org) ينتمي الحدث (event) عندما يعمل مستخدم (user) في مساحتي عمل (workspaces) في جلسة (session) واحدة.

## 🏆 أفضل المستودعات (The best repos)

| المستودع (Repo) | ما هو (What it is) | التقنيات (Stack) | الترخيص (License) | اختره عندما (Pick it when) |
|---|---|---|---|---|
| [PostHog/posthog](https://github.com/PostHog/posthog) | تحليلات منتج شاملة (all-in-one product analytics) مع إعادة تشغيل الجلسات (session replay) والأعلام (flags) والتجارب (experiments) | Python/Django, TypeScript, ClickHouse | MIT (core; `ee/` separately licensed) | تريد أداة (tool) واحدة لتحليلات المنتج (product analytics) والأعلام (flags)، سحابية (cloud) أو مستضافة ذاتيًا (cloud or self-hosted) |
| [plausible/analytics](https://github.com/plausible/analytics) | تحليلات ويب (web analytics) خفيفة بلا ملفات ارتباط (cookieless) | Elixir, ClickHouse, Postgres | AGPL-3.0 | تحليلات (analytics) تحترم الخصوصية (privacy-friendly) لموقع التسويق (marketing site) |
| [umami-software/umami](https://github.com/umami-software/umami) | تحليلات ويب (web analytics) بسيطة مستضافة ذاتيًا (self-hosted) | Next.js, Postgres/MySQL | MIT | أسهل تحليلات ويب (web analytics) مستضافة ذاتيًا (self-hosted) في التشغيل |
| [Openpanel-dev/openpanel](https://github.com/Openpanel-dev/openpanel) | تحليلات ويب (web analytics) ومنتج (product) مفتوحة المصدر (open-source) | TypeScript, ClickHouse | AGPL-3.0 | بديل أخف لـ PostHog على طريقة Mixpanel |
| [jitsucom/jitsu](https://github.com/jitsucom/jitsu) | جمع الأحداث (event collection) / CDP إلى مستودع بياناتك (your warehouse) | TypeScript, Go | MIT | تريد جمعًا على طريقة Segment إلى مستودع بياناتك (your warehouse) الخاص |
| [rudderlabs/rudder-server](https://github.com/rudderlabs/rudder-server) | موجّه أحداث (event router) CDP (بديل Segment) | Go | Elastic License 2.0 | وجهات (destinations) كثيرة وخط أحداث (pipeline) يبدأ من مستودع البيانات (data warehouse) |
| [matomo-org/matomo](https://github.com/matomo-org/matomo) | بديل قديم وراسخ لـ Google Analytics | PHP, MySQL | GPL-3.0 | بديل كامل الميزات (features) ومستضاف ذاتيًا (self-hosted) لـ GA، وقوي في الاتحاد الأوروبي |
| [ClickHouse/ClickHouse](https://github.com/ClickHouse/ClickHouse) | قاعدة بيانات تحليلية عمودية (columnar analytical database) | C++ | Apache-2.0 | تخزين مليارات الأحداث (events) والاستعلام (query) عنها، أو تحليلات (analytics) يراها العملاء (customers) |

**إن درست مستودعًا واحدًا فقط (If you only study one):** ادرس **PostHog**. هو SaaS إنتاجي (production SaaS) *و*نظام تحليلات (analytics) في الوقت نفسه، فتستطيع أن تقرأ كيف تُستقبل الأحداث (ingested)، وكيف تُنمذج `identify`/`group`، وكيف تُنظَّم جداول (tables) ClickHouse، وكيف يقيّد تسلسل المؤسسة (organization)/المشروع (org/project hierarchy) كل ذلك. وهو يغطي الدرس 6.3 أيضًا.

**اشترِ أم ابنِ أم استضف بنفسك (Buy, build, or self-host)؟**

- **اشترِ (Buy)** تحليلات المنتج (product analytics) مبكرًا: PostHog Cloud أو Amplitude أو Mixpanel. وللتسويق (marketing)، Plausible Cloud أو Fathom. الإعداد يستغرق يومًا، ووقتك يُصرف بشكل أفضل على خطة التتبع (tracking plan) لا على تشغيل ClickHouse.
- **استضف بنفسك (Self-host)** عندما تتطلب ذلك إقامة البيانات (data residency) أو وعود الخصوصية (privacy promises)، أو عندما يجعل حجم الأحداث (event volume) التسعير (pricing) لكل حدث (every event) مؤلمًا. Umami وPlausible سهلان في الاستضافة الذاتية (self-hosting). أما PostHog المستضاف ذاتيًا (self-hosted) فالتزام تشغيلي (operational commitment) جاد.
- **ابنِ (Build)** فقط التحليلات (analytics) *التي يراها العملاء (customers)* (رسوم التوفر (uptime charts) في Beacon)، لأنها منتجك (your product)، فوق ClickHouse أو Tinybird أو TimescaleDB. لا تبنِ أبدًا أداة (tool) تحليلات منتج (product analytics) داخلية خاصة بك.

## 🔍 ادرسه في مشاريع حقيقية (Study it in the wild)

**PostHog/posthog.** ابحث عن `group_type` و`groups` لترى كيف تُنمذج تحليلات المجموعات (group analytics) في B2B، وابحث عن تعريفات مخطط (schema) ClickHouse (ابحث عن `CREATE TABLE` مع `MergeTree`) لترى كيف تُرتب الأحداث (events) على القرص (disk). وكود (code) plugin-server والاستقبال (ingestion) يعرض ما يحدث بين SDK وقاعدة البيانات (database): التجميع على دفعات (batching)، ودمج الأشخاص (person merging)، ومعالجة الخصائص (properties).

**dubinc/dub.** مثال نظيف على **التحليلات التي يراها العملاء (customer-facing analytics)**. استخدم البحث في الكود (code search) عن `tinybird` لتجد أين تُرسل أحداث النقر (click events) وأين تُستعلم التحليلات (analytics) لكل مساحة عمل (workspace) ورابط (URL). لاحظ أن Postgres الخاص بـ Dub يخزن الروابط (links) ومساحات العمل (workspaces)، بينما يذهب تيار النقرات (click stream) الكبير إلى مخزن تحليلات (analytics store) منفصل.

**plausible/analytics.** يستحق القراءة بوصفه حجة تصميمية (design argument). انظر كيف يُحسب الزائر (visitor) بلا ملفات ارتباط (ابحث عن `salt`)، وكيف يبقى جانب Postgres (المواقع، المستخدمون (users)) منفصلًا عن جانب ClickHouse (الأحداث (events)).

**umami-software/umami.** أصغر قاعدة كود (codebase) هنا. اقرأ كيف يبني سكربت التتبع (tracking script) الحمولة (payload) وكيف تتحقق نقطة الجمع (collection endpoint) منها وتخزنها. وهو نموذج جيد (good model) لعدّاد مشاهدات صفحة الحالة (status-page view counts) في Beacon.

**ما الذي تلاحظه (What to notice):**

- بيانات التطبيق (app) التعاملية (Postgres) والأحداث كبيرة الحجم (ClickHouse أو Tinybird) تعيش في مخازن (stores) منفصلة بأنماط وصول (access patterns) منفصلة.
- كل حدث (every event) يحمل معرّف (ID) مشروع أو موقع أو مساحة عمل (workspace)، وكل استعلام (query) مقيّد به.
- الاستقبال (ingestion) يتم على دفعات (batched) وبشكل غير متزامن (asynchronously). الطلب الذي يسجل نقرة لا ينتظر قاعدة بيانات التحليلات (analytics database) أبدًا.
- الخصوصية (privacy) قرار تصميمي في الكود (الملح (salting)، والإخفاء (masking)، واقتطاع IP (IP truncation))، لا مجرد سطر في السياسة.

## 🛠️ ابنِه في Beacon (Build it into Beacon)

### 🟢 تمرين المبتدئ (Beginner exercise)

اكتب خطة التتبع (tracking plan) الخاصة بـ Beacon: من 8 إلى 12 حدثًا (event) بصيغة object_action، لكل منها خصائصه (its properties) وسطر واحد يشرح "لماذا". ثم أضف تحليلات ويب (web analytics) بلا ملفات ارتباط (Plausible أو Umami) إلى موقع التسويق (marketing site) فقط.

**يكتمل عندما (Done when):**
- يرتبط كل حدث (every event) في الخطة (plan) بسؤال ستطرحه فعلًا (التفعيل (activation)، الاحتفاظ (retention)، الترقية (upgrade)).
- لا تحتوي أي خاصية حدث (event property) على بريد أو اسم أو رابط مراقَب (monitored URL).
- تظهر زيارات موقع التسويق (marketing site) في اللوحة (dashboard) دون ضبط أي ملف ارتباط (تحقق من DevTools → Application).

### 🟡 تمرين المستوى المتوسط (Intermediate exercise)

ادمج PostHog (سحابيًا (cloud) أو مستضافًا ذاتيًا (self-hosted)). استدعِ `identify` عند الدخول (login) و`group("organization", orgId, { plan })` عند تحميل كل صفحة (page load) في التطبيق (app). أرسل `monitor_created` و`subscription_upgraded` **من الخادم (server)** بعد نجاح الكتابة في قاعدة البيانات (database) أو ويب هوك (webhook) Stripe. ابنِ (Build) قُمع تفعيل (activation funnel): `org_created` ← `monitor_created` ← أول `monitor_check_completed` خلال 24 ساعة.

**يكتمل عندما (Done when):**
- يمكن تقسيم القُمع (funnel) حسب خطة (plan) المؤسسة (organization)، لا حسب المستخدم (user) فقط.
- حجب (blocking) نطاق (domain) PostHog في المتصفح (browser) لا يمنع تسجيل `monitor_created`.
- دالة (function) `track` مُنمَّطة ترفض وقت الترجمة (compile time) أسماء الأحداث (event names) غير الموجودة في خطتك.

### 🔴 تمرين المستوى المتقدم (Advanced exercise)

ابنِ (Build) تحليلات توفر يراها العملاء (customer-facing uptime analytics). اكتب كل نتيجة فحص (check result) إلى جدول (table) ClickHouse (`org_id`، `monitor_id`، `ts`، `status`، `latency_ms`) بعمليات إدراج على دفعات (batched inserts) من عامل الفحص (check worker) (5.1). اعرض نقطة نهاية (endpoint) على الخادم (server) تعيد نسبة التوفر (uptime) اليومية لـ 90 يومًا وزمن الاستجابة (latency) p95 لمراقبة (monitor) واحدة، واعرضها بـ Tremor في صفحة الحالة (status page).

**يكتمل عندما (Done when):**
- تأخذ نقطة النهاية (endpoint) `org_id` من الجلسة (session) أو من البحث عن صفحة الحالة (status page)، لا من معامل الاستعلام (query parameter) أبدًا، ويثبت اختبار (test) أن المؤسسة (organization) A لا تستطيع قراءة بيانات المؤسسة B.
- تتم عمليات الإدراج (inserts) على دفعات (مثلًا كل ثانية أو كل 1,000 صف)، لا صفًا لكل فحص (one row per check).
- تحذف سياسة احتفاظ (retention policy) (TTL في ClickHouse) البيانات (data) التي تتجاوز حد التاريخ في الخطة (plan).

## ⚠️ أخطاء يقع فيها المبتدئون (Mistakes juniors make)

- **تتبّع كل شيء بلا خطة (plan).** الالتقاط التلقائي (autocapture) واستدعاءات `track()` العشوائية تعطيك آلاف الأحداث (events) وصفر إجابات. اكتب خطة التتبع (tracking plan) أولًا، ثم أضف أحداثًا لأسئلة ستطرحها فعلًا.
- **نسيان المؤسسة (organization).** في B2B يخفي القُمع (funnel) على مستوى المستخدم (user) الحقيقة: مستخدم متحمس واحد في حساب ميت (dead account) يبدو بصحة جيدة. أرسل استدعاءات `group` وحلّل حسب المؤسسة.
- **تتبّع أحداث الأعمال (business events) من المتصفح (browser).** مانعات الإعلانات (ad blockers) تسقطها والمستخدمون (users) يستطيعون تزويرها. أرسل `monitor_created` والترقيات (upgrades) من الخادم (server) بعد تثبيت الكتابة.
- **وضع بيانات شخصية (PII) في خصائص الأحداث (event properties).** البريد والروابط (links) في التحليلات (analytics) تجعل طلبات الحذف (deletion requests) في GDPR كابوسًا وتسرّب البيانات (data) إلى مزوّد آخر (another vendor). أرسل المعرّفات (IDs) وادمج لاحقًا في مستودع البيانات (data warehouse) إن احتجت.
- **تشغيل استعلامات التحليلات (analytics queries) على Postgres الإنتاجي (production).** استعلام (query) GROUP BY "سريع" لـ 90 يومًا على جدول (table) الفحوص (checks) يبطئ التطبيق (app) لكل العملاء (customers). استخدم نسخة قراءة (read replica) أو مستودع بيانات (data warehouse) أو ClickHouse.
- **قياس الاحتفاظ (retention) بـ "تسجيلات الدخول (logins)".** تسجيل الدخول (logging in) ليس قيمة. عرّف الاستخدام النشط (active usage) بحدث القيمة (تلقى تنبيهًا (alert)، شاهد الحوادث (incidents)، نشر صفحة حالة (status page)).

## 🧾 الخلاصة (Recap)

- تحليلات الويب (موقع التسويق (marketing site))، وتحليلات المنتج (السلوك داخل التطبيق (app))، وذكاء الأعمال (كل شيء مدموجًا) ثلاث وظائف مختلفة.
- خطة التتبع (tracking plan) بأسماء object_action تأتي قبل أي كود (code)، واستدعاءات `group` هي ما يجعل تحليلات (analytics) B2B تعمل.
- تتبّع أحداث الأعمال (business events) على الخادم (server) وأحداث الواجهة (UI events) في المتصفح (browser). أبقِ البيانات الشخصية (personal data) خارج الخصائص (properties) واحترم الموافقة (consent).
- منصة CDP تجمع الأحداث (events) مرة واحدة وتوجّهها. ومستودع البيانات (data warehouse) يدمجها مع بيانات التطبيق (app). وETL العكسي يرسل الاستنتاجات (insights) إلى الخارج.
- ClickHouse (العمودي (columnar)) هو المخزن (store) المعتاد للأحداث (events) وللتحليلات التي يراها العملاء (customer-facing analytics) كما في Dub. قيّد كل استعلام (query) بالمستأجر (tenant).

## ✍️ اختبر نفسك (Check yourself)

**1. ما الأنواع الثلاثة للتحليلات (analytics)، وأي سؤال يجيب عنه كل منها؟**

<details><summary>الإجابة (Answer)</summary>

تحليلات الويب (web analytics) تجيب عن من يزور موقع التسويق (marketing site) ومن أين. وتحليلات المنتج (product analytics) تجيب عن ماذا يفعل المستخدمون المسجلون (logged-in users) داخل التطبيق (app). وذكاء الأعمال (business intelligence) ومستودع البيانات (data warehouse) يجيبان عن كيف يبدو العمل عبر كل الأنظمة مدموجة معًا. راجع الجدول (table) في بداية 🟢 الأساسيات (The essentials).

</details>

**2. ماذا يفعل استدعاء `group`، ولماذا يحتاجه SaaS الموجّه للشركات (B2B)؟**

<details><summary>الإجابة (Answer)</summary>

`group(groupId, traits)` يحدد المؤسسة (organization) التي ينتمي إليها المستخدم (user)، مثل `org_42` على خطة (plan) Pro. في B2B تدفع لك المؤسسة لا المستخدم، لذلك تحتاج إلى تحليل القُمع (funnel) والاحتفاظ (retention) لكل حساب بدل كل شخص. راجع بنود مواصفة (spec) Segment في 🟢 الأساسيات (The essentials).

</details>

**3. هل يجب أن يرسل Beacon الحدث (event) `monitor_created` من المتصفح (browser) أم من الخادم (server)؟ ولماذا؟**

<details><summary>الإجابة (Answer)</summary>

من الخادم (server)، بعد تثبيت الإدراج (insert) في قاعدة البيانات (database). إنه حدث أعمال (business event)، والتتبع في المتصفح (client-side tracking) تحجب مانعات الإعلانات (ad blockers) جزءًا منه ويستطيع المستخدمون (users) تزويره. التتبع في المتصفح مخصص لسلوك الواجهة (UI behaviour) البحت مثل فتح لوحة الأوامر (command palette). راجع "التتبع في المتصفح مقابل التتبع على الخادم (server-side tracking)" في 🟡 التعمق أكثر (Going deeper).

</details>

**4. يريد Beacon أن يعرض لكل عميل (customer) رسوم التوفر (uptime charts) لـ 90 يومًا. أين يجب أن تعيش نتائج الفحوص (check results)، وما القاعدة التي يجب أن يتبعها كل استعلام (query)؟**

<details><summary>الإجابة (Answer)</summary>

في مخزن عمودي (column-oriented store) مثل ClickHouse (أو Tinybird)، تُكتب إليه بعمليات إدراج على دفعات (batched inserts)، بينما يحتفظ Postgres ببيانات التطبيق (app). ويجب أن يُصفّى كل استعلام (query) بـ `org_id` على الخادم (server)، مأخوذًا من الجلسة (session) أو من البحث عن صفحة الحالة (status page)، لا من معامل استعلام (query parameter) أبدًا. عزل المستأجرين (tenant isolation) ينطبق على مخزن التحليلات (analytics store) كما ينطبق على Postgres. راجع "التحليلات التي يراها العملاء (customer-facing analytics)" في 🔴 على نطاق واسع وللمؤسسات (At scale / enterprise).

</details>

**5. لوحة (dashboard) تعرض الاحتفاظ (retention) بوصفه "المستخدمين (users) الذين سجلوا الدخول (login) كل أسبوع"، وكل حدث (every event) يحتوي على بريد المستخدم (user) والرابط المراقَب (monitored URL). ما الخطأ؟**

<details><summary>الإجابة (Answer)</summary>

تسجيل الدخول (logging in) ليس قيمة، لذلك يجب قياس الاحتفاظ (retention) بحدث قيمة (value event) مثل تلقي تنبيه أو مشاهدة الحوادث (incidents). والبريد والروابط (links) بيانات شخصية (PII) تُرسل إلى مزوّد آخر (another vendor)، وتجعل طلبات الحذف (deletion requests) في GDPR أصعب بكثير. أرسل المعرّفات (IDs) وادمج في مستودع البيانات (data warehouse) إن احتجت. راجع ⚠️ أخطاء يقع فيها المبتدئون (Mistakes juniors make) و"الخصوصية والموافقة (privacy and consent)" في 🟡 التعمق أكثر (Going deeper).

</details>

## 📚 المراجع (References)

- PostHog documentation, including group analytics — توثيق PostHog بما فيه تحليلات المجموعات (group analytics): https://posthog.com/docs
- Segment Spec (identify, track, page, group) — مواصفة (spec) Segment: https://segment.com/docs/connections/spec/
- Plausible data policy (how cookieless counting works) — سياسة البيانات (data) في Plausible وكيف يعمل (How it works) العد بلا ملفات ارتباط (cookieless): https://plausible.io/data-policy
- ClickHouse documentation — توثيق ClickHouse: https://clickhouse.com/docs
- Tinybird documentation — توثيق Tinybird: https://www.tinybird.co/docs
- RudderStack documentation — توثيق RudderStack: https://www.rudderstack.com/docs/
- Umami documentation — توثيق Umami: https://umami.is/docs

---

# 6.3 — أعلام الميزات (feature flags) والتجارب (experiments)

*المستوى (Level): 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 3.2، 6.2*

## ⚡ الدرس في دقيقة (In 60 seconds)

- علم الميزة (Feature Flag) جملة `if` وقت التشغيل (runtime) تتحكم في شرطها من خارج الكود (code). وهو يفصل نشر الكود (deploy) عن إطلاقه (release).
- القاعدة الأهم (The rule that matters most): الأعلام (flags) مؤقتة. أعطِ كل علم مالكًا (owner) وتاريخ انتهاء (expiry date)، ولا تُعِد استخدام اسم أبدًا، واحذف العلم (flag) مع الكود الميت (dead code) المرتبط به.
- الخيار الافتراضي للنسخة الأولى (The v1 default): التقييم على الخادم (server-side evaluation) مع قواعد مخزّنة مؤقتًا (cached rules) وقيمة افتراضية آمنة (safe default)، والطرح حسب المؤسسة (per-org rollout) بتجزئة ثابتة (deterministic hash) لمفتاح العلم (flag key) مع معرّف المؤسسة (org ID)، والاستدعاء عبر OpenFeature.
- الاستحقاقات (entitlements) ليست أعلامًا. الخطط (plans) والأسعار (pricing) تعيش في نظام الاستحقاقات (3.2)، لا في أداة (tool) الأعلام (flags).
- الفخ الأكبر (The biggest trap): الطرح (rollout) بـ `Math.random()`، والطرح حسب المستخدم (per-user rollout) في B2B، والنظر إلى نتائج التجارب (experiments) حتى تصبح p < 0.05. معظم منتجات (products) B2B لا تملك الحركة الكافية (traffic) لاختبارات A/B (A/B tests)، ولا بأس بذلك.

## 🧭 لماذا يحتاجه كل SaaS (Why every SaaS has this)

في 1 أغسطس 2012 نشرت Knight Capital كود تداول (trading code) جديدًا على خوادمها (servers). أعاد الكود (code) الجديد استخدام علم إعدادات (configuration flag) قديم كان يشغّل يومًا ميزة ميتة (dead feature) منذ زمن اسمها "Power Peg". خادم واحد من ثمانية لم يحصل على الكود الجديد. وعندما شُغّل العلم (flag)، نفّذ ذلك الخادم (server) منطق Power Peg القديم على السوق الحية (live market). في نحو 45 دقيقة خسرت Knight قرابة 440 مليون دولار، ولم تنجُ الشركة بوصفها شركة مستقلة. ويصف أمر هيئة الأوراق المالية الأمريكية (SEC) اللاحق ما حدث بالتفصيل. وما زالت هذه أغلى درس مسجَّل في نظافة الأعلام (flag hygiene): **لا تُعِد توظيف علم قديم (old flag) أبدًا، واحذف الأعلام (flags) الميتة مع كودها.**

المخاطر في Beacon أصغر، لكن الشكل نفسه. يعيد الفريق كتابة مُجدوِل الفحوص (check scheduler). يستطيعون دمجه (merge) يوم جمعة ويأملون، أو يدمجونه *مطفأً (off)*، ثم يشغّلونه لمؤسستهم (their own org) الخاصة، ثم لـ 5% من مؤسسات (orgs) Free، ويراقبون معدل الأخطاء (error rate)، ويطفئونه بنقرة واحدة إن بدأت الفحوص (checks) تتأخر. وبشكل منفصل، يريد فريق المنتج (product team) أن يعرف هل ترفع قائمة مهام التهيئة (onboarding checklist) الجديدة معدل التفعيل (activation rate)، و"تبدو أفضل" ليست إجابة.

أعلام الميزات (feature flags) تفصل **نشر** الكود (وضعه على الخوادم (servers)) عن **إطلاقه (releasing it)** (السماح للمستخدمين (users) بتشغيله). والتجارب (experiments) تعيد استخدام الآلية نفسها لقياس هل ساعد التغيير. **علم الميزة (feature flag) جملة `if` وقت التشغيل (runtime) تتحكم في شرطها من خارج الكود. قوته تأتي بالضبط من كونه فرعًا مخفيًا (hidden branch) في الإنتاج (production)، وخطره للسبب نفسه.**

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

في أبسط صوره، العلم (flag) هو:

```ts
if (await flags.isEnabled("new-scheduler", { orgId: org.id, plan: org.plan })) {
  return scheduleWithNewEngine(monitor);
}
return scheduleWithOldEngine(monitor);
```

قواعد (rules) العلم ("مفعّل للمؤسسة (organization) `beacon-internal`، ولـ 5% من الباقين") تعيش في خدمة أعلام (flag service) أو ملف إعدادات (config file)، لا في الكود (code). غيّر القاعدة فيتغير السلوك دون نشر (without a deploy).

هناك عدة أنواع من الأعلام (flags)، وتختلف في مدة بقائها ومن يملكها. ومقال Pete Hodgson على martinfowler.com هو التصنيف (taxonomy) الكلاسيكي:

| النوع (Type) | الغرض (Purpose) | مدة البقاء (lifespan) | من يقلبه (Who flips it) | مثال من Beacon (Beacon example) |
|---|---|---|---|---|
| **علم الإطلاق (Release Flag)** | شحن كود (ship code) غير مكتمل أو خطر وهو مخفي، وطرحه تدريجيًا (roll out gradually) | من أيام إلى أسابيع، ثم **يُحذف** | المهندسون (engineers) | `new-scheduler` |
| **علم التشغيل (ops flag) / مفتاح الإيقاف (Kill Switch)** | إيقاف نظام فرعي (subsystem) مكلف أو متعطل بسرعة | طويل البقاء (long-lived) بطبيعته | المناوب (on-call) | `disable-sms-sending` أثناء انقطاع المزوّد (provider outage) |
| **علم الإذن (Permission Flag)** | وصول مبكر (early access) أو برامج تجريبية (betas) لعملاء (customers) مختارين | من أسابيع إلى أشهر | المنتج (product)/نجاح العملاء (customer success) | `ai-incident-summary-beta` لـ 10 مؤسسات (orgs) |
| **التجربة (Experiment)** | تقسيم المستخدمين (users) عشوائيًا لقياس الأثر على مقياس (metric) | حتى تصبح النتيجة ذات دلالة (significant)، ثم يُحذف | المنتج (product)/النمو (growth) | `onboarding-checklist-v2` مقابل المجموعة الضابطة (control) |

**الاستحقاقات (Entitlements) ليست أعلام ميزات (not feature flags).** "خطة (plan) Business تحصل على SSO وفحوص (checks) كل 30 ثانية" قاعدة *تسعير (pricing)* تعيش في نظام الخطط (plans) والاستحقاقات (3.2) وتتغير عندما يدفع العميل (customer). أما أعلام الميزات (feature flags) فأدوات تحكم هندسية (engineering controls) ومنتجية مؤقتة. إن نمذجت الخطط بوصفها أعلامًا (flags) في LaunchDarkly، تنجرف (drift) الفوترة والوصول (billing and access) بعيدًا عن بعضهما ولا يعرف أحد أيهما الحقيقة. علم تجريبي (beta flag) *يمكنه* أن يفحص استحقاقًا ("تجريبي، لكن لمؤسسات (orgs) Business فقط")، لكنهما نظامان مختلفان.

لماذا لا تستخدم متغير بيئة (environment variable) فقط؟ متغيرات البيئة (env vars) تحتاج إعادة نشر (redeploy) لتتغير، ولا تستطيع استهداف عميل (customer) واحد، ولا تدعم النسب (percentages). هذا مقبول لمفتاح إيقاف (kill switch) في تطبيق (app) صغير جدًا، لكنه غير مقبول لأي شيء آخر.

### 🟡 التعمق أكثر (Going deeper)

**أين يُقيَّم العلم (flag).** هناك نموذجان (two models):

- **التقييم البعيد (Remote Evaluation).** يسأل التطبيق (app) خدمة الأعلام (flag service) مع كل طلب: "هل `new-scheduler` مفعّل للمؤسسة (organization) 42؟". هذا بسيط، والقواعد (rules) لا تغادر الخادم (server) أبدًا. الكلفة (cost) قفزة شبكة (network hop) مع كل فحص (check)، ويجب أن تقرر ماذا يحدث عندما تتوقف الخدمة.
- **التقييم المحلي (Local Evaluation).** تنزّل حزمة SDK (SDK) *مجموعة القواعد (ruleset) كاملة* عند بدء التشغيل (startup)، وتبقيها محدّثة بالاستطلاع أو البث (polling or streaming)، وتقيّم في الذاكرة (memory) خلال ميكروثوانٍ. هذا ما تريده في عمّال الفحص (check workers) في Beacon، الذين يتخذون ملايين القرارات يوميًا. حزم SDK (SDKs) للخادم (server) في Unleash وFlagsmith وGrowthBook وPostHog كلها تدعمه. أما حزم SDK للمتصفح (browser) فتحصل عادة على نتائج مقيّمة مسبقًا (pre-evaluated) من الخادم، حتى لا تنكشف قواعد الاستهداف (targeting rules) (وقوائم العملاء (customers)) لكل من يفتح DevTools.

```mermaid
sequenceDiagram
    participant B as المتصفح (Browser)
    participant W as SDK عامل Beacon (Beacon worker SDK)
    participant FS as خدمة الأعلام (Flag service)
    participant UI as لوحة الأعلام (Flag dashboard)
  UI->>FS: اضبط new-scheduler على 5 بالمئة من المؤسسات (Set new-scheduler to 5 percent of orgs)
  FS-->>W: دفع أو استطلاع مجموعة القواعد المحدثة (Push or poll updated rule set)
  W->>W: تجزئة مفتاح العلم مع orgId إلى دلو من 0 إلى 99 (hash of flag key and orgId, bucket 0 to 99)
  W->>W: الدلو أقل من 5 يعني المحرك الجديد (bucket under 5 means new engine)
  B->>FS: اطلب الأعلام المقيّمة لهذه الجلسة (Get evaluated flags for this session)
  FS-->>B: new-scheduler قيمته false (new-scheduler is false)
```

عرّف دائمًا **قيمة افتراضية (default value)** لحالة عدم الوصول إلى خدمة الأعلام (flag service)، واجعلها القيمة الآمنة (عادة "مطفأ"، أي مسار الكود (code) القديم).

**الطرح بالنسب (percentage rollout) يحتاج تجزئة ثابتة (consistent hash).** "5% من المؤسسات (orgs)" لا يمكن أن تعني `Math.random() < 0.05`، لأن المؤسسة (organization) نفسها ستتنقل عندها بين الكود (code) القديم والجديد مع كل طلب. بدلًا من ذلك، جزّئ مفتاحًا ثابتًا مثل `hash(flagKey + ":" + orgId)` إلى رقم من 0 إلى 99، وفعّل العلم (flag) إن كان أقل من 5. المؤسسة نفسها تقع دائمًا في الدلو (bucket) نفسه، والانتقال من 5% إلى 20% يبقي الـ 5% الأصلية داخل الطرح (rollout). وإدخال مفتاح العلم (flag key) في التجزئة (hashing) يعني أن الأعلام (flags) المختلفة تختار شرائح (slices) 5% مختلفة، فلا يحصل العملاء (customers) غير المحظوظين أنفسهم على كل نسخة تجريبية (beta). وتستخدم الأدوات (tools) دوال تجزئة (hash functions) ثابتة مثل MurmurHash3 أو SHA-1 لهذا.

**استهدف حسب المؤسسة (organization) في B2B.** إن طرحت حسب *المستخدم (user)*، يرى زميلان في Acme لوحتي تحكم مختلفتين ويفتحان تذاكر دعم (support tickets) محيّرة. استخدم معرّف المؤسسة (org ID) بوصفه مفتاح الطرح (rollout key)، ومرّر خصائص (properties) المؤسسة (الخطة (plan)، المنطقة، تاريخ الإنشاء) بوصفها سياق استهداف (targeting context). في PostHog أعلام مبنية على المجموعات (group-based flags) لهذا الغرض، وUnleash وFlagsmith وGrowthBook كلها تسمح لك باختيار خاصية الالتصاق (Stickiness) أو التجزئة (hashing).

**OpenFeature** مشروع تابع لـ CNCF يعرّف واجهة أعلام (flag API) محايدة تجاه المزوّدين (vendor-neutral). يستدعي كودك `client.getBooleanValue("new-scheduler", false, { targetingKey: orgId })`، و**مزوّد** (Provider) يربط Unleash أو Flagsmith أو LaunchDarkly أو flagd أو مزوّدك الخاص. تستطيع تغيير المزوّد (vendor) دون لمس مواضع الاستدعاء (call sites)، و**الخطافات** (Hooks) تعطيك مكانًا واحدًا لتسجيل كل تقييم (evaluation). وفي قاعدة كود (codebase) جديدة هي طريقة رخيصة لتجنب الارتهان لمزوّد واحد (vendor lock-in).

**دَين الأعلام (Flag Debt).** كل علم إطلاق (release flag) يضاعف عدد المسارات (code paths) في ذلك الكود (code). عشرة أعلام قديمة (stale flags) تعني ما يصل إلى 1,024 تركيبة (combinations) لم يختبرها أحد. وقصة Knight Capital هي دين الأعلام في أسوأ صوره. والحل عملية منظمة (process):

- أعطِ كل علم (flag) مالكًا (owner) وتاريخ انتهاء عند إنشائه. يعلّم Unleash الأعلام (flags) بوصفها قديمة محتملة (potentially stale) حسب نوعها، وعدة أدوات (tools) تبلّغ عن الأعلام التي لم تُقيَّم مؤخرًا.
- حذف العلم (flag) جزء من "الاكتمال": تذكرة متابعة (follow-up ticket) تُنشأ مع العلم، وتُنجز عندما يصل الطرح (rollout) إلى 100%.
- لا تُعِد استخدام اسم علم أبدًا. أنشئ علمًا (flag) جديدًا.
- ابحث في قاعدة الكود (codebase) عن الأعلام (flags) المفعّلة 100% في كل مكان، واحذف العلم (flag) *و*الفرع الميت (dead branch).

### 🔴 على نطاق واسع وللمؤسسات (At scale / enterprise)

**أساسيات اختبار A/B (A/B testing).** التجربة (experiment) تُسند الوحدات (units) (في Beacon: **المؤسسات (orgs)**) عشوائيًا إلى المجموعة الضابطة (control) أو إلى النسخة الجديدة (variant) بالتجزئة الثابتة (consistent hashing) نفسها، وتعرّضها للتغيير، وتقارن مقياسًا (metric) واحدًا مختارًا مسبقًا. الفخاخ:

- **اختر مقياسًا أساسيًا (primary metric) واحدًا قبل أن تبدأ**، مثل "نسبة المؤسسات (orgs) المفعّلة خلال 24 ساعة". افحص عشرين مقياسًا (metric) وسيبدو أحدها ذا دلالة (significant) بالصدفة.
- **احسب حجم العينة (sample size) مسبقًا.** اكتشاف تحسن بنقطتين (two-point lift) على معدل تفعيل (activation rate) 30% يحتاج آلاف المؤسسات (orgs) في كل ذراع (arm). وكثير من منتجات (products) SaaS الموجّهة للشركات لا *تملك* هذه الحركة. إن كان لديك 200 تسجيل أسبوعيًا، فمعظم التجارب (experiments) لن تصل إلى الدلالة (significance) أبدًا. اشحن التغيير خلف علم إطلاق (release flag) وراقب الأرقام بدلًا من ذلك.
- **مشكلة التلصص (Peeking).** فحص (check) اختبار كلاسيكي (classical test) (ذي أفق ثابت (fixed-horizon)) كل يوم والتوقف لحظة تصبح p < 0.05 يضخّم النتائج الإيجابية الكاذبة (false positives) كثيرًا. إما أن تنتظر حجم العينة المخطط (planned sample size)، أو تستخدم طريقة مصممة للمراقبة المستمرة (continuous monitoring) (الاختبار التسلسلي (sequential testing)، أو المقاربات البايزية (Bayesian) التي تقدمها أدوات (tools) مثل GrowthBook).
- **سجّل التعرّض (exposure) لا الإسناد (assignment).** احسب المؤسسة (organization) ضمن التجربة (experiment) فقط عندما تصل فعلًا إلى الشاشة المتغيرة. وإلا فستخفف الأثر بأشخاص لم يروه قط.
- **عدم تطابق نسبة العينة (Sample Ratio Mismatch).** إن خرج تقسيم 50/50 بنسبة 55/45، فشيء ما معطوب (روبوتات (bots)، أو إعادة توجيه (redirect) تُسقط مستخدمين (users)، أو تخزين مؤقت (caching)). لا تثق بالنتيجة.

**الأعلام (flags) في المسار الحرج (critical path).** على نطاق واسع (at scale) يصبح نظام الأعلام بنية تحتية (infrastructure). يجب أن تخزّن حزم SDK (SDKs) آخر قواعد معروفة (last known rules) وتستمر في العمل إن اختفت الخدمة. وتحتاج تغييرات الأعلام إلى **سجل تدقيق** (Audit Log) (7.3)، ويُفضَّل وجود موافقات (approvals) على مفاتيح الإيقاف (kill switches) في الإنتاج (production)، لأن "من أوقف إرسال الرسائل القصيرة (SMS) الساعة 02:00؟" سؤال حقيقي. ويجب أن تظهر التغييرات (Changes) أيضًا في أدوات المراقبة (observability) (7.2) بوصفها تعليقات على اللوحات (annotations)، لأن أول سؤال أثناء أي حادثة (incident) هو "ما الذي تغيّر؟"، وقلب علم (flag flip) يُعدّ تغييرًا كما يُعدّ النشر (deploy) تغييرًا.

**الاتساق بين الخدمات (consistency across services).** إن كانت الـ API وعامل الفحص (check worker) يقيّمان `new-scheduler` كلاهما، فيجب أن يتفقا للمؤسسة (organization) نفسها. وهذا يعني المفتاح نفسه، والتجزئة (hashing) نفسها، وإصدار مجموعة قواعد (rules) ينتشر (propagates) خلال ثوانٍ. ووسطاء الترحيل أو الحافة (relay or edge proxies) (Unleash Edge وflagd وFlagsmith Edge Proxy) يبقون التقييم (evaluation) قريبًا من خدماتك ويخففون الحمل عن خادم الأعلام المركزي (central flag server).

## 🏆 أفضل المستودعات (The best repos)

| المستودع (Repo) | ما هو (What it is) | التقنيات (Stack) | الترخيص (License) | اختره عندما (Pick it when) |
|---|---|---|---|---|
| [Unleash/unleash](https://github.com/Unleash/unleash) | منصة أعلام ميزات (feature flag platform) مفتوحة المصدر (open-source) وناضجة | Node.js/TypeScript, Postgres | AGPL-3.0 | أعلام (flags) مستضافة ذاتيًا (self-hosted) مع استراتيجيات طرح (rollout strategies) قوية وحزم SDK (SDKs) كثيرة |
| [Flagsmith/flagsmith](https://github.com/Flagsmith/flagsmith) | أعلام (flags) وإعدادات عن بُعد (remote config)، سحابية (cloud) أو مستضافة ذاتيًا (self-hosted) | Python/Django, React | BSD-3-Clause | تريد أعلامًا (flags) مع قيم إعدادات عن بُعد (remote config) لكل هوية (identity) |
| [growthbook/growthbook](https://github.com/growthbook/growthbook) | أعلام (flags) مع منصة تجارب (experimentation platform) تعمل مباشرة على مستودع البيانات (data warehouse) | TypeScript, MongoDB | MIT (core) | تجارب (experiments) بإحصاء حقيقي (real statistics) على بيانات في مستودعك الخاص (your own warehouse) |
| [flipt-io/flipt](https://github.com/flipt-io/flipt) | خادم (server) أعلام (flags) خفيف يناسب GitOps | Go | Fair Core License (FCL-1.0-MIT) | ملف تنفيذي (binary) واحد، والأعلام (flags) مخزنة بجانب إعداداتك |
| [open-feature/spec](https://github.com/open-feature/spec) | مواصفة (spec) واجهة أعلام الميزات (feature flags) المحايدة تجاه المزوّدين | Spec (Markdown) | Apache-2.0 | فهم المعيار (standard) الذي يجب أن تتبعه استدعاءات SDK لديك |
| [open-feature/js-sdk](https://github.com/open-feature/js-sdk) | حزمة OpenFeature SDK لـ JavaScript/TypeScript | TypeScript | Apache-2.0 | كتابة استدعاءات أعلام (flags) محايدة تجاه المزوّدين (vendor-neutral) في تطبيق (app) Node أو ويب |
| [PostHog/posthog](https://github.com/PostHog/posthog) | أعلام (flags) وتجارب (experiments) مدمجة مع تحليلات المنتج (product analytics) | Python/Django, ClickHouse | MIT (core; `ee/` separately licensed) | تستخدم PostHog أصلًا وتريد أعلامًا (flags) مرتبطة بالأحداث (events) والمجموعات |

**إن درست مستودعًا واحدًا فقط (If you only study one):** ادرس **Unleash**. توثيقه وكوده يعرضان بوضوح أنواع الأعلام (flag types)، واستراتيجيات التفعيل (activation strategies)، والالتصاق (مفتاح التجزئة الثابتة (consistent hashing))، واكتشاف الأعلام القديمة (stale flags). وهو أوضح نموذج (clearest model) لنظام أعلام (flags) مبني للمهندسين (engineers).

**اشترِ أم ابنِ أم استضف بنفسك (Buy, build, or self-host)؟**

- **اشترِ (Buy)** عندما تكون الأعلام (flags) حرجة وتفضّل ألا تشغّل الخدمة بنفسك: LaunchDarkly هو المعيار (standard) في المؤسسات (orgs)، وStatsig قوي في التجارب (experiments)، وPostHog Cloud أو GrowthBook Cloud حلول شاملة (all-in-one) أرخص.
- **استضف بنفسك (Self-host)** Unleash أو Flagsmith أو GrowthBook أو Flipt عندما تحتاج الأعلام (flags) داخل شبكتك الخاصة (private network)، أو عندما يكون منتجك (your product) نفسه قابلًا للاستضافة الذاتية (7.4). كلها سهلة التشغيل مع Postgres.
- **ابنِ (Build)** نسخة صغيرة جدًا فقط: جدول (table) `feature_flags` مع تجاوزات (overrides) لكل مؤسسة (org) ونسبة مجزّأة، مخزّن مؤقتًا (cached) في الذاكرة (memory). هذا يكفي لأعلامك (your flags) القليلة الأولى. وعندما تريد سجلات تدقيق (audit logs)، أو تجارب (experiments)، أو حزم SDK (SDKs) بعدة لغات، أو أن يقلب غير المهندسين (non-engineers) الأعلام (flags)، فاعتمد أداة (tool)، ويُفضَّل أن تكون خلف OpenFeature حتى يكون التبديل رخيصًا.

## 🔍 ادرسه في مشاريع حقيقية (Study it in the wild)

**PostHog/posthog.** يشغّل PostHog أعلامه (its flags) على نفسه. استخدم البحث في الكود (code search) عن `feature_flag` و`hash` لتجد كيف تُحسب نسبة الطرح (rollout percentage) من مفتاح العلم (flag key) والمعرّف المميز (distinct id) (أو مفتاح المجموعة (group key) في الأعلام المبنية على المجموعات (group-based flags)). وابحث عن طريقة تقييم (evaluation) الأعلام (flags) لكل نوع مجموعة (group type) لترى الاستهداف (targeting) على مستوى المؤسسة (organization) في B2B.

**Unleash/unleash.** اقرأ كود (code) استراتيجيات التفعيل (ابحث عن `strategy` و`stickiness`)، وانظر كيف تُحدَّد الأعلام القديمة (stale flags) حسب نوع العلم (flag) وعمره. وحزم SDK (SDKs)، الموجودة في مستودعات (repos) منفصلة تحت منظمة Unleash، تعرض التقييم المحلي (local evaluation): تنزيل القواعد (rules)، وتحديثها في الخلفية، والتقييم (evaluation) في الذاكرة (memory).

**growthbook/growthbook.** ابحث عن `hash` في كود (code) SDK لترى كيف يُسند المستخدمون (users) إلى نسخ التجربة (experiment variations) بشكل حتمي (deterministically)، وتصفح محرك الإحصاء (Python) لترى الاختبار التسلسلي (sequential testing) والتحليل البايزي (Bayesian analysis) منفذين فعلًا لا موصوفين فقط.

**calcom/cal.diy.** قاعدة كود (codebase) منتج (product) تستخدم الأعلام (flags)، لا مزوّد أعلام (flag vendor). استخدم البحث في الكود (code search) عن `feature flag` أو `features` لتجد كيف يقيّد (gates) Cal.com الميزات (features) في قاعدة بياناته (its database) الخاصة ويفحصها لكل فريق. وهو مثال واقعي على "نظام أعلام داخلي صغير" تقارنه بالأدوات (tools) المخصصة.

**ما الذي تلاحظه (What to notice):**

- مدخل التجزئة (hashing) يجمع مفتاح العلم (flag key) ومعرّفًا (ID) ثابتًا، فيبقى الطرح (rollout) ملتصقًا (sticky) ولا يتداخل بين الأعلام (flags).
- حزم SDK (SDKs) لها قيم افتراضية (defaults) صريحة ومجموعات قواعد مخزّنة مؤقتًا (cached rules) لحالة عدم الوصول إلى الخادم (server is unreachable).
- *أنواع* الأعلام (flags) مفهوم أساسي، وهي تغيّر المدة المتوقعة لبقاء العلم (flag).
- سياق الاستهداف (targeting context) يشمل خصائص (properties) المجموعة أو المؤسسة (organization)، لا خصائص المستخدم (user) فقط.

## 🛠️ ابنِه في Beacon (Build it into Beacon)

### 🟢 تمرين المبتدئ (Beginner exercise)

نفّذ علمًا (flag) داخليًا بسيطًا: جدول (table) `feature_flags` (`key`، `enabled`، `rollout_percent`) وجدول `feature_flag_overrides` (`key`، `org_id`، `enabled`). اكتب `isEnabled(key, orgId)` التي تفحص التجاوزات (overrides) أولًا، ثم تجزّئ `key:orgId` إلى رقم من 0 إلى 99 وتقارنه بـ `rollout_percent`.

**يكتمل عندما (Done when):**
- تحصل المؤسسة (organization) نفسها دائمًا على الإجابة نفسها (same answer) للعلم (flag) نفسه (اكتب اختبارًا (test) على 1,000 استدعاء).
- رفع الطرح (rollout) من 10% إلى 30% يبقي كل مؤسسة (org) كانت مفعّلة أصلًا.
- تجاوز لمؤسستك (override) الداخلية يفعّل العلم (flag) بغض النظر عن النسبة.

### 🟡 تمرين المستوى المتوسط (Intermediate exercise)

استبدل الدالة (function) الداخلية بـ OpenFeature مع مزوّد (provider) Unleash (أو Flagsmith) مستضاف ذاتيًا (self-hosted). ضع المُجدوِل الجديد (new scheduler) خلف `new-scheduler`، بمفتاح هو معرّف المؤسسة (org ID)، مع تقييم (evaluation) محلي في العامل (worker). أضف `disable-sms-sending` بوصفه مفتاح إيقاف تشغيلي (ops kill switch) يستطيع المناوب (on-call) قلبه من اللوحة (dashboard).

**يكتمل عندما (Done when):**
- إيقاف خدمة الأعلام (flag service) لا يُسقط العمّال (workers)، بل يستمرون في استخدام آخر قواعد معروفة (last known rules) أو القيمة الافتراضية الآمنة (safe default).
- قلب مفتاح الإيقاف (kill switch) يوقف إرسال الرسائل القصيرة (SMS) خلال فترة التحديث (refresh interval) لديك، دون نشر (without a deploy).
- لكل علم (flag) مالك وتاريخ انتهاء مسجّلان، وهناك تذكرة (ticket) لحذف (deletion) `new-scheduler`.

### 🔴 تمرين المستوى المتقدم (Advanced exercise)

شغّل تجربة حقيقية (real experiment) على التهيئة (onboarding) باستخدام GrowthBook أو PostHog: `onboarding-checklist-v2`، مقسّمة عشوائيًا حسب المؤسسة (organization)، والمقياس الأساسي (primary metric) "مفعّلة خلال 24 ساعة" (من 6.2). سجّل حدث تعرّض (exposure event) فقط عندما ترى المؤسسة قائمة المهام (checklist). وقبل الإطلاق (release)، اكتب أدنى أثر قابل للاكتشاف (minimum detectable effect) وحجم العينة (sample size) المطلوب.

**يكتمل عندما (Done when):**
- تذكر وثيقة التجربة (experiment doc) المقياس (metric) وحجم العينة (sample size) وقاعدة التوقف (stopping rule) *قبل* الإطلاق (release).
- يعمل فحص (check) لعدم تطابق نسبة العينة (sample ratio mismatch) وينجح.
- تُسجَّل النتيجة (فوز أو خسارة أو غير حاسمة (inconclusive))، ويُحذف الفرع الخاسر (losing branch) والعلم (flag)، ويُظهر سجل التدقيق (audit log) من غيّر التجربة (experiment) ومتى.

## ⚠️ أخطاء يقع فيها المبتدئون (Mistakes juniors make)

- **استخدام الأعلام (flags) للخطط (plans) والأسعار (pricing).** "Pro تحصل على فحوص (checks) كل دقيقة" مكانها الاستحقاقات (3.2) المرتبطة بالفوترة (billing). الأعلام أدوات تحكم (controls) مؤقتة، وخلط الاثنين يعطيك عملاء يدفعون (paying customers) مقابل ميزات (features) لا يستطيعون استخدامها.
- **التوزيع العشوائي (randomising) مع كل طلب.** الطرح (rollout) بـ `Math.random()` ينقل المستخدمين (users) بين النسخ مع كل تحميل صفحة (page load). جزّئ معرّفًا (ID) ثابتًا مع مفتاح العلم (flag key).
- **الطرح حسب المستخدم (per-user rollout) في منتج (product) B2B.** يرى الزملاء منتجات (products) مختلفة ويرتبك الدعم. استخدم المؤسسة (organization) بوصفها مفتاح الطرح (rollout key).
- **عدم حذف الأعلام (flags) أبدًا.** كل علم قديم (old flag) فرع مخفي (hidden branch) وKnight Capital محتملة. أعطِ الأعلام مالكين (owners) وتواريخ انتهاء، واعتبر الحذف (deletion) جزءًا من الميزة (feature).
- **إرسال قواعد الاستهداف (targeting rules) إلى المتصفح (browser).** التقييم المحلي (local evaluation) في المتصفح قد يكشف قوائم العملاء (customers) وأسماء الميزات غير المعلنة (unreleased features). قيّم على الخادم (server) وأرسل إلى المتصفح النتائج فقط.
- **التلصص (peeking) على التجارب (experiments) والتوقف مبكرًا.** التوقف عند أول p < 0.05 يجد الضوضاء (noise) في الغالب. ثبّت حجم العينة (sample size) والمقياس (metric) مسبقًا، أو استخدم طرقًا تسلسلية (sequential methods).
- **عدم وجود قيمة افتراضية (default value) عند توقف خدمة الأعلام (flag service).** البحث عن علم (flag) الذي يرمي استثناءً (throws) يُسقط الطلب كله معه. مرّر دائمًا قيمة افتراضية آمنة (safe default) وخزّن القواعد (rules) مؤقتًا.

## 🧾 الخلاصة (Recap)

- الأعلام (flags) تفصل النشر (deploy) عن الإطلاق (release): أعلام الإطلاق (release flags)، ومفاتيح الإيقاف التشغيلية (ops kill switches)، وأعلام الإذن (permission flags)، والتجارب (experiments)، ولكل منها مدة بقاء ومالك مختلفان.
- الاستحقاقات (entitlements) ليست أعلامًا. التسعير (pricing) يعيش في 3.2، والأعلام (flags) يمكنها الرجوع إليه لكن لا ينبغي أن تحل محله.
- قيّم محليًا على الخوادم (servers) مع قواعد مخزّنة مؤقتًا (cached rules) وقيم افتراضية آمنة (safe defaults). وأرسل إلى المتصفحات (browsers) نتائج مقيّمة مسبقًا (pre-evaluated).
- الطرح بالنسب (percentage rollout) يستخدم تجزئة ثابتة (consistent hash) لمفتاح العلم (flag key) مع معرّف (ID) ثابت، وفي B2B هذا المعرّف هو المؤسسة (organization).
- OpenFeature يبقي مواضع الاستدعاء (call sites) محايدة تجاه المزوّدين (vendor-neutral). ودين الأعلام (flag debt) حقيقي، فاحذف الأعلام (flags) مع كودها الميت (its dead code).
- التجارب (experiments) تحتاج مقياسًا (metric) واحدًا، وحجم عينة محددًا مسبقًا، وعدم تلصص. كثير من منتجات (products) B2B لا تملك الحركة الكافية (traffic)، ولا بأس بذلك.

## ✍️ اختبر نفسك (Check yourself)

**1. ما الفرق بين النشر (deploy) والإطلاق (release)، وكيف تربط أعلام الميزات (feature flags) بينهما؟**

<details><summary>الإجابة (Answer)</summary>

النشر (deploy) يضع الكود (code) على الخوادم (servers)، والإطلاق (release) يسمح للمستخدمين (users) بتشغيله. يسمح لك العلم (flag) بنشر الكود وهو مطفأ، ثم إطلاقه (releasing it) تدريجيًا أو لمؤسسات (orgs) مختارة دون نشر آخر (without another deploy). راجع 🧭 لماذا يحتاجه كل SaaS (Why every SaaS has this).

</details>

**2. اذكر أنواع الأعلام الأربعة (four flag types) ومدة بقاء كل منها.**

<details><summary>الإجابة (Answer)</summary>

أعلام الإطلاق (release flags) تبقى من أيام إلى أسابيع ثم تُحذف. وأعلام التشغيل (ops flags) أو مفاتيح الإيقاف (kill switches) طويلة البقاء (long-lived) بطبيعتها. وأعلام الإذن (permission flags) للبرامج التجريبية (betas) تبقى من أسابيع إلى أشهر. والتجارب (experiments) تبقى حتى تصبح النتيجة ذات دلالة (significant) ثم تُحذف. راجع جدول (table) أنواع الأعلام (flag types) في 🟢 الأساسيات (The essentials).

</details>

**3. تتضمن خطة (plan) Business في Beacon خدمة SSO وفحوصًا (checks) كل 30 ثانية. هل يجب أن تكون هذه أعلام ميزات (feature flags)؟**

<details><summary>الإجابة (Answer)</summary>

لا. إنها قواعد (rules) تسعير (pricing)، لذلك مكانها نظام الخطط (plans) والاستحقاقات (3.2)، الذي يتغير عندما يدفع العميل (customer). إن نمذجت الخطط بوصفها أعلامًا (flags)، تنجرف الفوترة والوصول (billing and access) بعيدًا عن بعضهما. يمكن لعلم تجريبي (beta flag) أن يفحص استحقاقًا (entitlement)، لكنهما نظامان منفصلان. راجع "الاستحقاقات ليست أعلام ميزات (not feature flags)" في 🟢 الأساسيات (The essentials).

</details>

**4. يريد Beacon طرح `new-scheduler` لـ 5% من المؤسسات (orgs). كيف يجب أن تقرر عمّال الفحص (check workers) أي المؤسسات تحصل عليه؟**

<details><summary>الإجابة (Answer)</summary>

جزّئ مفتاحًا ثابتًا مثل `flagKey + ":" + orgId` إلى دلو من 0 إلى 99، وفعّل العلم (flag) إن كان الدلو (bucket) أقل من 5. المؤسسة (organization) نفسها تحصل دائمًا على الإجابة نفسها (same answer)، ورفع الطرح (rollout) إلى 20% يبقي المؤسسات (orgs) الأصلية داخله. ويجب أن يستخدم العمّال (workers) التقييم المحلي (local evaluation) مع قواعد مخزّنة مؤقتًا (cached rules) وقيمة افتراضية آمنة (safe default). راجع "الطرح بالنسب (percentage rollout) يحتاج تجزئة ثابتة (consistent hash)" في 🟡 التعمق أكثر (Going deeper).

</details>

**5. يطرح مطوّر (developer) لوحة تحكم (dashboard) جديدة بـ `if (Math.random() < 0.1)` لكل مستخدم (user). ما الذي ينكسر؟**

<details><summary>الإجابة (Answer)</summary>

ينتقل المستخدم (user) نفسه بين النسخة القديمة والجديدة مع كل طلب، لأنه لا شيء ملتصق (sticky). ولأن الطرح حسب المستخدم (per-user rollout)، يرى زميلان في المؤسسة (organization) نفسها منتجين مختلفين ويفتحان تذاكر دعم (support tickets) محيّرة. جزّئ معرّف المؤسسة (org ID) مع مفتاح العلم (flag key) بدلًا من ذلك. راجع ⚠️ أخطاء يقع فيها المبتدئون (Mistakes juniors make).

</details>

## 📚 المراجع (References)

- Pete Hodgson, "Feature Toggles (aka Feature Flags)", martinfowler.com — المقال الكلاسيكي عن أنواع الأعلام (flag types): https://martinfowler.com/articles/feature-toggles.html
- OpenFeature documentation — توثيق OpenFeature: https://openfeature.dev
- Unleash documentation — توثيق Unleash: https://docs.getunleash.io
- GrowthBook documentation (experimentation and statistics) — توثيق GrowthBook عن التجارب (experiments) والإحصاء: https://docs.growthbook.io
- Evan Miller, "How Not To Run an A/B Test" — كيف لا تُجري اختبار A/B (A/B test): https://www.evanmiller.org/how-not-to-run-an-ab-test.html
- SEC order on Knight Capital Americas LLC (2013), available from https://www.sec.gov — أمر هيئة الأوراق المالية الأمريكية (SEC) بشأن Knight Capital
- PostHog feature flags documentation — توثيق أعلام الميزات (feature flags) في PostHog: https://posthog.com/docs/feature-flags

التالي: **الوحدة 7 (Module 7) — تشغيل SaaS (Operating the SaaS)**، حيث تُبقي لوحة الإدارة (admin panel) والمراقبة وسجلات التدقيق (audit logs) والنشر (deploy) كل هذا يعمل.
