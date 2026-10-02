# هندسة البيانات والتحليلات (Data Engineering & Analytics): من الصفر إلى الاحتراف (Zero to Hero)

**ابنِ أنظمة البيانات (data systems) التي يثق بها الناس. دورة مجانية ثنائية اللغة (bilingual course) تنقلك من الصفر إلى مهندس بيانات (data engineer) واثق، أو مهندس تحليلات (analytics engineer)، أو عالم بيانات (data scientist) يفكّر بعقلية الإنتاج (production-minded).**

## ما هذه الدورة (What this is)

كل لوحة معلومات (dashboard) ونموذج (model) ومساعد ذكاء اصطناعي (AI assistant) يعمل على بيانات قام أحدهم بنمذجتها (modelled) ونقلها (moved) وتنظيفها (cleaned) واختبارها (tested) وتأمينها (secured). وحين يُنجَز هذا العمل بشكل سيّئ، تتعارض الأرقام، وينجرف النموذج (model drifts) دون أن يلاحظ أحد، ويجيب مساعد الذكاء الاصطناعي من المستند الخاطئ (wrong document). وحين يُنجَز بإتقان، لا يلاحظه أحد. وهذا هو الهدف.

تعلّمك هذه الدورة العمل من بدايته إلى نهايته (end to end):
- لغة SQL التي تجيب عن أسئلة الأعمال الحقيقية (real business questions)، ونماذج البيانات (data models) التي تصمد أمام التغيير.
- مستودعات البيانات (warehouses) وبحيرات البيانات (lakes) والمستودعات البحيرية (lakehouses).
- خطوط البيانات (pipelines) الدفعية (batch) والمتدفقة (streaming) التي يمكن إعادة تشغيلها بأمان (safely re-run).
- التحويلات (transformations) بوصفها شيفرة مُختبَرة (tested code)، وجودة البيانات (data quality) والعقود (contracts).
- مقاييس (metrics) ولوحات معلومات (dashboards) يثق بها الناس، وتجارب (experiments) لا تخدعك.
- نقل تعلّم الآلة (machine learning) من دفتر الملاحظات (notebook) إلى الإنتاج (production).
- إعداد البيانات لتطبيقات النماذج اللغوية الكبيرة (LLM applications).
- الحوكمة (governance) والخصوصية (privacy) والأمن (security) لمنصة البيانات (data platform).

يعمل كل شيء على حاسوب محمول (laptop) بأدوات مجانية (free tools): PostgreSQL وDuckDB وPython وdbt وAirflow أو Dagster، وKafka.

كُتبت هذه الدورة لخرّيجي علوم البيانات (data science) وعلوم الحاسوب (computer science) والهندسة (engineering)، ولمهندسي البرمجيات (software engineers) المنتقلين إلى مجال البيانات، وللمحلّلين (analysts) الراغبين في العمل الهندسي، ولكل من يملك مسؤولية البيانات (owns data) في بنك أو جهة حكومية (government body) أو مؤسسة (enterprise).

## كيف يعمل كل درس (How every lesson works)

يتكوّن كل درس من الأجزاء العشرة نفسها (ten parts)، لتعرف دائمًا أين أنت:

| الجزء (Part) | ما تحصل عليه (What you get) |
|---|---|
| ⚡ **الدرس في دقيقة (In 60 seconds)** | الدرس في خمس نقاط (five bullets): ما هو، والقاعدة الأهم (the rule that matters most)، وإشارة القرار (decision cue)، والفخ الأكبر (biggest trap). |
| 🧭 **لماذا يهم (Why it matters)** | موقف في فريق البيانات (data team) لدى بنك نجم (Najm Bank) يجعل الموضوع أمرًا لا مفرّ منه. |
| 📐 **كيف يعمل (How it works)** | الأفكار صعودًا على سلّم (climbing a ladder): 🟢 *الأساسيات (The essentials)* ← 🟡 *التعمق أكثر (Going deeper)* ← 🔴 *نظرة الخبير (Expert view)*، مع شيفرة SQL والشيفرة (code) الخاطئة والصحيحة جنبًا إلى جنب (side by side). |
| 🧰 **الأدوات (The toolkit)** | الأدوات والأنماط (patterns) والمعايير (standards) المنطبقة: ما يفعله كلٌّ منها ومتى تلجأ إليه (when to reach for it). |
| 🏛️ **عمليًا في بنك نجم (In practice at Najm Bank)** | المُخرَج (artefact) الذي ينتجه هذا الدرس: نموذج بيانات (data model)، أو تصميم خط بيانات (pipeline design)، أو نموذج dbt مُختبَر (tested dbt model)، أو عقد بيانات (data contract)، أو بطاقة مقياس (metric card)، أو جدول خصوصية (privacy table). |
| 🛠️ **التمارين (Exercises)** | ثلاثة تمارين متدرّجة (graded exercises) (🟢 🟡 🔴)، لكلٍّ منها معايير «يكتمل عندما (done when)». |
| ⚠️ **أخطاء وفخاخ (Mistakes and traps)** | ما الذي يسوء في الممارسة الفعلية (in practice)، وما الذي تفعله بدلًا منه. |
| 🧾 **الخلاصة (Recap)** | الدروس المستفادة (takeaways) الجديرة بالتذكّر. |
| ✍️ **اختبر نفسك (Check yourself)** | خمسة أسئلة، معظمها سيناريوهات (scenarios)، مع إجابات مخفية (hidden answers) وشروح (explanations). |
| 📚 **المراجع (References)** | التوثيق الرسمي (official documentation) والأوراق البحثية (papers) والكتب الكلاسيكية (classic books). |

يُوسَم كل درس بـ**مرحلته في دورة حياة البيانات (data life cycle stage)**: Ingest أو Store أو Model أو Transform أو Serve أو Analyse أو Operate أو Govern. ويجمع [فهرس الأدوات (toolkit catalogue)](./TOOLKIT.ar.md) كل أداة ونمط (pattern) في مكان واحد.

## الحالة المستمرة (The running case): فريق منصة البيانات في بنك نجم (Najm Bank's data platform team)

تتابع الدورة فريق **منصة البيانات والتحليلات (Data Platform & Analytics)** في **بنك نجم (Najm Bank)**، وهو البنك الخليجي الخيالي (fictional Gulf bank) المستخدم في جميع دورات هذه المكتبة. يعمل الفريق مع:
- قاعدة بيانات الأنظمة المصرفية الأساسية (core banking database)؛
- تدفق معاملات البطاقات (card transactions stream)؛
- أحداث التطبيق (app events) من تطبيق نجم للهاتف (Najm Mobile)؛
- مستودع البيانات (warehouse) ومتاجر بياناته (marts) الخاصة بالرؤية الشاملة للعميل (customer 360) ومخاطر الائتمان (credit-risk)؛
- نموذج كشف الاحتيال (fraud model) **التنبيهات الذكية (Smart Alerts)**؛
- **مساعد مذكرات الائتمان (Credit Memo Copilot)**، الذي يجيب استنادًا إلى مستندات البنك (bank documents).

**فيصل**، رئيس منصة البيانات (Head of Data Platform)، هو مرشدك (mentor). و**هدى**، مهندسة بيانات (data engineer) حديثة التخرّج (new graduate)، تتعلّم إلى جانبك.

## المسار من الصفر إلى الاحتراف (The path from zero to hero)

| المرحلة (Stage) | الوحدات (Modules) | ستكون قادرًا على… (You will be able to…) |
|---|---|---|
| 🟢 **الأسس (Foundations)** | 0–1 | شرح منظومة البيانات الحديثة (modern data stack)، وكتابة SQL تجيب عن أسئلة الأعمال (business questions)، ونمذجة البيانات بالحُبَيبية (grain) الصحيحة. |
| 🟡 **الممارس (Practitioner)** | 2–5 | بناء خطوط بيانات (pipelines) آمنة لإعادة التشغيل (safe to re-run)، واختبار تحويلاتك (transformations)، وتعريف مقاييس موثوقة (trusted metrics)، وإجراء تجارب سليمة (sound experiments)، ونقل النماذج وبيانات النماذج اللغوية الكبيرة (LLM data) إلى الإنتاج (production). |
| 🔴 **المحترف (Hero)** | 6–7 | حوكمة (govern) منصة بيانات وتأمينها (secure)، وبناء متجر بيانات مخاطر الائتمان (credit-risk mart) من البداية إلى النهاية (end to end)، واجتياز امتحان تدريبي (practice exam) من 60 سؤالًا. |

## الدورات المرافقة (Companion courses)

حين يتطرّق درس إلى قواعد البيانات في بيئة الإنتاج (databases in production)، أو أحداث التحليلات (analytics events)، أو قانون الخصوصية (privacy law)، أو تقييم الذكاء الاصطناعي (AI evaluation)، أو الأمن (security)، أو البنية التحتية (infrastructure)، فإنه يحيل إلى الدورة المرافقة (companion course) بدلًا من تكرارها: *System Design for Vibe Coders* و*SaaS Building Blocks* و*AI Governance* و*AI Product Management* و*Secure AI & Application Security* و*Cloud & DevOps* و*From Graduate to Hired*.

## لغتان (Two languages)

كل درس متاح بالإنجليزية والعربية. وفي النسخة العربية (Arabic edition)، تحمل المصطلحات التقنية (technical terms) اسمها الإنجليزي بين قوسين، مثل «نافذة الدالة (window function)»، لأن الأدوات والتوثيق (documentation) وإعلانات الوظائف (job ads) التي ستتعامل معها مكتوبة بالإنجليزية.

## إلى أين بعد ذلك (Where to go next)

افتح خريطة الدورة (course map)، أو ابدأ بالدرس 0.1.
