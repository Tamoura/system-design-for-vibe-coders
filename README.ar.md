# تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)

**تستطيع اليوم أن تبني وتُطلق برمجيات أسرع من أي جيل من المبرمجين قبلك. هذه الدورة تعلّمك ما لن ينبّهك إليه الذكاء الاصطناعي (AI) — حتى يتعطل الإنتاج (production).**

## ما هذه الدورة (What this is)؟

دورة مكتوبة في تصميم الأنظمة العملي (practical system design)، موجّهة إلى **من يبنون بالذكاء الاصطناعي أولًا (AI-first builders)**: أولئك الذين يطلقون منتجات حقيقية عبر Claude Code وCursor وأمثالهما، دون دراسة نظامية للأنظمة الموزعة (distributed systems)، ثم يصطدمون بالجدار يوم يلتقي نموذجهم الأولي (their prototype) بمستخدمين حقيقيين (real users).

هذه ليست دورة تحضير لمقابلات التوظيف (interview prep course)؛ لا سبورة بيضاء (whiteboard) ولا «صمّم تويتر (designing Twitter)». كل درس فيها مبني على **حادثة حقيقية من بيئة الإنتاج (real production incident)** في منصة فعلية متعددة الواجهات (ويب (web) وiOS وأندرويد وتلفاز (TV)، تخدم جمهورًا عالميًا (global audience))، بُنيت وتُدار إلى حدّ بعيد *بواسطة* وكلاء ذكاء اصطناعي (AI agents) بإشراف بشري (under human direction). وتغطي الحوادث (incidents) كامل ما ينمو إليه المنتج الحقيقي: الكاش (cache) وشبكات توزيع المحتوى (CDNs)، البيانات والنسخ الاحتياطي (backups)، النشر (deploy)، المصادقة (auth) وOAuth، البريد (email) والنشرات البريدية (newsletters)، مفاتيح الميزات (feature flags)، إصدارات الموبايل (mobile releases)، الأمن (security) وإساءة الاستخدام (abuse)، والمراقبة (observability). الندوب حقيقية (The scars are real)، والإصلاحات وصلت إلى الإنتاج فعلًا (the fixes shipped).

## كيف تسير الدورة (How the course works)؟

**لا يُشترط أن تعرف البرمجة (You do not need to know how to code).** أنت في هذه الدورة المهندسُ المعماري (the architect) ومفتشُ السلامة (the safety inspector)، ووكيلك الذكي (your AI agent) هو البنّاء (the builder). كل خطوة عملية (hands-on step) مكتوبة تعليماتٍ *تعطيها للوكيل (agent)* ودليلًا (evidence) *تطالبه به* — لا كودًا (code) تكتبه بنفسك. ومن يعرف البرمجة يجد مربعات (boxes) **🔧 تحت الغطاء (Under the Hood)** الاختيارية بالأوامر والتفاصيل.

لكل درس الأركان الأربعة (four pillars) نفسها:

1. **🔥 قصة من الميدان (The War Story)** — حادثة (incident) حقيقية: الأعراض (symptoms) كما ظهرت، والفرضيات الخاطئة (wrong theories)، والسبب الجذري (root cause) الفعلي، والإصلاح (fix) الذي وصل إلى الإنتاج (production).
2. **📐 المبدأ (The Principle)** — مفهوم تصميم الأنظمة (system-design concept) الذي تعلّمنا إياه الحادثة (incident)، بلغة بسيطة ومخططات (diagrams)، وكل مصطلح يُعرَّف قبل استخدامه (يسنده (backed by) [المسرد (Glossary)](./GLOSSARY.ar.md)).
3. **🎛️ وجّه وكيلك (Direct Your Agent)** — تطبّق المبدأ (The Principle) على **Relay**، منتج عام عن قصد (حسابات (accounts)، محتوى صنّاع (creator content)، وسائط (media)، خلاصات (feeds)، بريد (email)، تطبيق موبايل (mobile client)) يُبنى عبر الدورة من نموذج إلى إنتاج (from prototype to production) دون انقطاع (zero-downtime) — بأن تقول للوكيل (agent) *ماذا* يبني: الموجّهات الحرفية (the exact prompts)، والسياق (context) الذي يجعله يبني الصواب، وحاجز الأمان (guardrail) الذي يجعل القاعدة تعيش بعد المحادثة. وطبّق كل خطوة على تطبيقك أنت إن كان لك تطبيق.
4. **✅ تحقق منه (Verify It)** — الركن (pillar) الذي يجعل برمجة الفايب (vibe coding) آمنة: قائمة أدلة (evidence checklist) تثبت أن الخطوة نجحت فعلًا، مصوغة بحيث لا يتطلب فحصُها **قراءة أي كود (zero code reading)** — أشياء تراها وتنقرها أو تجعل الوكيل (agent) يعرضها من الطبقة التي يلمسها المستخدمون (the layer users touch).

## لمن هذه الدورة (Who it's for)؟

- تبني (أو تريد أن تبني) منتجات حقيقية بتوجيه وكيل ذكاء اصطناعي (AI agent) — بخلفية برمجية أو بدونها (with or without a programming background).
- اكتويتَ (أو توشك أن تكتوي) بشيء «كان يعمل» حتى وصل المستخدمون الحقيقيون (real users).
- تريد أن تكفّ عن الثقة وتبدأ التحقق (stop trusting and start verifying) — دون حاجة إلى قراءة الكود (reading the code).

**جديد كليًا على هذا العالم (Completely new to this world)؟** ابدأ من **الجزء 0 — الأسس (Foundations)**: خمسة دروس بلغة بسيطة بلا أي شروط مسبقة (ما الخادم (server)، وماذا يحدث حين تفتح موقعًا، وما الكود (code) والمستودع (repo) والنشر (deploy)، وكيف تعمل مع وكيلك (your agent)، ووضع صفحتك الأولى على الهواء — بدليل (with proof)).

## وليست لِـ (Who it's not for)

- المتأهبين للمقابلات (Interview preppers) — لذلك دوراتها.
- من يريد نظرية بلا تشغيل حقيقي (theory without operating anything).

## المنهج (Curriculum)

انظر [OUTLINE.ar.md](./OUTLINE.ar.md) للمنهج الكامل وحدةً وحدة (full module-by-module curriculum)، و[war-stories/incident-bank.md](./war-stories/incident-bank.md) لبنك الحوادث الخام (raw incident material) الذي بُنيت منه الدروس.

| # | الوحدة (Module) | الجدار الذي ستصطدم به (The wall you hit) |
|---|--------|------------------------|
| F | الجزء 0: الأسس (Foundations) | لا تعرف البرمجة (You don't code) — ولا تحتاجها (and you don't need to). بلا شروط مسبقة (no prerequisites). |
| 0 | فجوة مبرمج الفايب (The Vibe Coder's Gap) | «يعمل» شيء، و«نظام» شيء آخر (It works and it's a system are different claims) |
| 1 | تشريح تطبيق حقيقي (Anatomy of a Real App) | لا تستطيع أن تفكّر فيما لا تستطيع رسمه (You can't reason about what you can't draw) |
| 2 | البيانات والتخزين والنسخ الاحتياطي (Data, Storage & Backups) | قاعدة البيانات ليست الشيء الوحيد الذي يفقد البيانات (The database is not the only thing that can lose data) |
| 3 | الكاش (cache): أمضى سكين في الدرج (the Sharpest Knife in the Drawer) | كل كاش خطأٌ لم تلتقِ به بعد (Every cache is a bug you haven't met yet) |
| 4 | النشر دون انقطاع (Deploys Without Downtime) | الإطلاق نظام متكامل، لا أمر يُنفَّذ (Shipping is a system, not a command) |
| 5 | مستخدمون حقيقيون وإساءة حقيقية (Real Users, Real Abuse) | حدود المعدل (rate limits)، والمصادقة (auth)، وأول مهاجم (the first attacker) |
| 6 | خادم واحد وعملاء كثر (One Backend, Many Clients) | ويب (web) وموبايل (mobile) وتلفاز (TV) — ومعضلة التحديث (the update problem) |
| 7 | المراقبة (observability) | لا تصلح ما لا تراه (You can't fix what you can't see) |
| 8 | شبكات أمان للكود المولَّد بالذكاء الاصطناعي (Safety Nets for AI-Generated Code) | اختبارات (tests) وحواجز (guardrails) ونظافة git (git hygiene) بسرعة الوكلاء (at agent speed) |
| 9 | قيادة فريق من وكلاء الذكاء الاصطناعي (Directing an AI Team) | المواصفات (specs) وهندسة السياق (context engineering) ومن المراجعة إلى الحاجز (review-to-guardrail) |
| 10 | التوسّع بعد خادم واحد (Scaling Beyond One Server) | قانون التوسّع الكلاسيكي (the classic scaling canon) بعدسة منتج كبر (through the lens of a product that grew) |
| 11 | الوصول إلى العالم (Reaching the World) | DNS وTLS، والتعريب (internationalization)، وSEO، والتكلفة (cost) |
| 12 | المشروع الختامي (Capstone): وصلك الإنذار (You Get Paged) | الأعراض فقط (Symptoms only). شخّصها (Diagnose it). |

المنهج (Curriculum) مجموعة **مكتملة** (complete set) في تصميم الأنظمة العملي (practical system design): مسنودة بالحوادث حيث لدينا ندوب (incident-backed where we have scars)، ومكتملة المفاهيم (concept-complete) فيما سواها. (الدروس التي بلا قصة ميدانية (war story) معلَّمة بوصفها دروس مفاهيم (concept lessons)، وتكتسب قصتها كلما تراكمت الحوادث (incidents).)

## اللغات (Languages)

الدورة **ثنائية اللغة (bilingual)**: كل وثيقة تصدر بالإنجليزية والعربية (بتخطيط RTL). الملفات الإنجليزية هي مصدر الحقيقة (source of truth) أثناء الصياغة، والعربية مرآتها (mirrors) إلى جوارها (`README.ar.md`، `OUTLINE.ar.md`، `lesson-N.ar.md`).

## كيف تقرؤها (Reading it)

تُبنى الدورة كاملةً في عدة صيغ مكتفية بذاتها (self-contained editions). اقرأها على الإنترنت من
**[tamoura.github.io/system-design-for-vibe-coders](https://tamoura.github.io/system-design-for-vibe-coders/)**،
أو خذها معك:

| الصيغة (Edition) | الملف (File) | لماذا (What it's for) |
|---|---|---|
| صفحة بلغتين (Bilingual page) | [`index.html`](./index.html) | كل شيء، مع مبدّل لغة (language toggle) |
| صفحة إنجليزية (English page) | [`index.en.html`](./index.en.html) | لغة واحدة (single language)، بنصف الحجم (half the weight) |
| صفحة عربية (Arabic page) | [`index.ar.html`](./index.ar.html) | لغة واحدة (single language)، RTL بالكامل (RTL throughout) |
| PDF | `course-ar.pdf` · `course-en.pdf` | الطباعة والقراءة دون اتصال (نحو 350 صفحة) |
| EPUB | `course-ar.epub` · `course-en.epub` | القرّاء الإلكترونيون (e-readers) وKindle |

كل صيغة تحمل الدروس الثمانية والستين بمخططاتها (its diagrams) مرسومةً مسبقًا (pre-rendered) — بلا خادم ولا اتصال ولا CDN (no server, no network, no CDN).
وصفحات HTML تضيف خريطة دورة قابلة للنقر (clickable course map)، وملحق المسرد (glossary appendix)، ووضعًا داكنًا (dark mode). أما PDF وEPUB فتُنشر (published) مع
كل إصدار (release) بدل أن تُودَع في المستودع (committed)؛ ولبنائها محليًا استخدم `npm run dist`.

```
npm install     # مرة واحدة — marked وmermaid وpuppeteer وarchiver (للبناء فقط)
npm run build   # إعادة توليد صفحات HTML من الماركداون
npm run dist    # ما سبق، إضافةً إلى PDF وEPUB لكل لغة في dist/
npm run check   # يفشل إن كانت الصفحات المودعة قديمة (يستخدمه التكامل المستمر)
```

يقارن `check` بصمةً للمصادر (a fingerprint of the sources) — الدروس وجداول README (README tables) والمسارد (glossaries) وقوالب البناء (build templates) نفسها — بالبصمة (fingerprint)
المضمّنة في كل صفحة مودعة (committed page). وهو لا يقارن البايتات المولَّدة (rendered bytes) عن قصد: إذ يقيس Mermaid النصّ ليحدّد
أحجام الصناديق (boxes)، فيخرج المدخل نفسه بهندسة SVG (SVG geometry) مختلفة على جهاز بخطوط مختلفة. أما البصمة (fingerprint) فتجيب عن
السؤال الذي يهم فعلًا («هل بُنيت هذه الصفحة من هذا الماركداون (markdown)؟») في نصف ثانية، وبلا متصفح (browser).

**ملفات الماركداون (markdown files) في `modules/` هي مصدر الحقيقة (source of truth).** وكل ما سبق ناتجٌ مولَّد (generated output) — لا تحرّره يدويًا
أبدًا، بل حرّر الدرس ثم أعد البناء (edit the lesson and rebuild). ويفشل البناء صراحةً (the build fails loudly) إن اختلف عدد الدروس الإنجليزية عن
العربية في أي وحدة (module)، أو تعذّر رسم أي مخطط (diagram)، أو لم يكن أحد مستندات EPUB (EPUB documents) صحيح البنية (well-formed).

## الحالة (Status)

مكتملة: الدروس الـ 69 كلها (الجزء 0، والوحدات (modules) 0–11، والمشروع الختامي (Capstone)) مكتوبة بالعربية والإنجليزية. تُضاف الحوادث الجديدة (New incidents are added) إلى الدروس عند وقوعها.
