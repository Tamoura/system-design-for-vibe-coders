# أمن الذكاء الاصطناعي والتطبيقات: من الصفر إلى الاحتراف

**أمّن التطبيق والذكاء الاصطناعي الذي بداخله (Secure the app and the AI inside it). دورة مجانية ثنائية اللغة (free, bilingual course) تنقلك من الصفر إلى مدافع واثق (confident defender) عن تطبيقات الويب (web apps)، وواجهات برمجة التطبيقات (APIs)، والأنظمة السحابية (cloud systems)، وتطبيقات النماذج اللغوية الكبيرة (LLM applications)، ووكلاء الذكاء الاصطناعي (AI agents).**

> **دفاعية وتعليمية (Defensive and educational).** كل هجوم (attack) في هذه الدورة مشروح لكي تتعرّف عليه (recognise it)، وتختبر وجوده (test for it)، وتمنعه (prevent it). لا تختبر إلا الأنظمة التي تملكها (systems you own) أو التي لديك إذن مكتوب (written permission) باختبارها. وتدرّب على المختبرات المحلية (local labs) وعلى تطبيقات تدريبية معرّضة للثغرات عن عمد (deliberately vulnerable training apps).

## ما هذه الدورة (What this is)

لا تزال معظم الاختراقات (breaches) تدخل من قائمة قصيرة من الأبواب (short list of doors): فحص وصول مفقود (missing access check)، أو استعلام قابل للحقن (injectable query)، أو مفتاح مسرَّب (leaked key)، أو اعتمادية غير مرقَّعة (unpatched dependency)، أو حاوية تخزين سحابية سيئة الإعداد (misconfigured cloud bucket). وقد أضاف الذكاء الاصطناعي (AI) أبوابًا جديدة (new doors)، وهي الآن مفتوحة أيضًا. فيمكن استدراج روبوت محادثة (chatbot) بالكلام حتى يكشف تعليماته (revealing its instructions). ويمكن توجيه مساعدٍ يقرأ المستندات (assistant that reads documents) بنص مخفي داخلها (text hidden inside them). ويمكن خداع وكيل يملك أدوات (agent with tools) ليعمل لصالح المهاجم (acting for an attacker). ويمكن لوكيل برمجة (coding agent) أن يكتب بثقة شيفرة معرّضة للثغرات (vulnerable code)، أو أن يثبّت حزمة غير موجودة أصلًا (package that does not exist).

تعلّمك هذه الدورة كيف تُغلق تلك الأبواب (close those doors). فهي تغطي كيف يفكر المهاجمون (how attackers think) وكيف تقع الاختراقات فعلًا (how breaches really happen)، ونمذجة التهديدات (threat modelling)، ونقاط الضعف الكلاسيكية (classic weaknesses) في الويب وواجهات برمجة التطبيقات والهوية والهاتف المحمول والسحابة (web, API, identity, mobile and cloud) وطرق إصلاحها (their fixes)، والتشفير والأسرار للبُناة (cryptography and secrets for builders)، ودورة حياة التطوير الآمن (secure development life cycle) وسلسلة توريد البرمجيات (software supply chain)، وسطح الهجوم (attack surface) في تطبيقات النماذج اللغوية الكبيرة (LLM apps) والوكلاء (agents). وتُختتم بالرصد (detection)، والاستجابة للحوادث (incident response)، وقيادة برنامج أمني (leading a security programme). وهي مكتوبة للمطورين (developers) (ومنهم من يبنون باستخدام وكلاء البرمجة بالذكاء الاصطناعي (AI coding agents))، والمعماريين (architects)، ومديري الهندسة والمنتجات (engineering and product managers)، والمحللين المنتقلين إلى أمن التطبيقات (AppSec) أو أمن الذكاء الاصطناعي (AI security)، وكل من يملك نظامًا (owns a system) في بنك أو جهة حكومية أو مؤسسة (a bank, a government body or an enterprise). ولا تفترض أي خلفية أمنية (security background).

## كيف يعمل كل درس (How every lesson works)

لكل درس الأجزاء العشرة نفسها (same ten parts)، لتعرف دائمًا أين أنت:

| الجزء (Part) | ما تحصل عليه (What you get) |
|---|---|
| ⚡ **الدرس في دقيقة (In 60 seconds)** | الدرس في خمس نقاط (five bullets): ما هو، والقاعدة الأهم (the rule that matters most)، وإشارة القرار (decision cue)، والفخ الأكبر (biggest trap). |
| 🧭 **لماذا يهم (Why it matters)** | موقف في بنك نجم (Najm Bank)، أو حادثة عامة حقيقية (real public incident)، تجعل الموضوع أمرًا لا مفرّ منه (unavoidable). |
| 📐 **كيف يعمل (How it works)** | الأفكار على سلّم متدرّج (climbing a ladder): 🟢 *الأساسيات (The essentials)* ← 🟡 *التعمق أكثر (Going deeper)* ← 🔴 *نظرة الخبير (Expert view)*، مع الشيفرة المعرّضة للثغرات والشيفرة المُصلَحة جنبًا إلى جنب (vulnerable and fixed code side by side). |
| 🧰 **الأدوات (The toolkit)** | الضوابط والمعايير والأدوات (controls, standards and tools) المنطبقة (that apply): ما يفعله كلٌّ منها، ومتى تلجأ إليه (when to reach for it). |
| 🏛️ **عمليًا في بنك نجم (In practice at Najm Bank)** | المُخرَج (artefact) الذي ينتجه هذا الدرس: نموذج تهديدات (threat model)، أو قاعدة برمجة آمنة (secure-coding rule)، أو مصفوفة تحكم في الوصول (access-control matrix)، أو قاعدة رصد (detection rule)، أو دليل تشغيل (runbook). |
| 🛠️ **التمارين (Exercises)** | ثلاثة تمارين متدرّجة (three graded exercises) (🟢 🟡 🔴)، لكلٍّ منها معايير «يكتمل عندما (done when)». |
| ⚠️ **أخطاء وفخاخ (Mistakes and traps)** | ما يسوء في الممارسة (what goes wrong in practice)، وما تفعله بدلًا منه (what to do instead). |
| 🧾 **الخلاصة (Recap)** | الدروس المستفادة (takeaways) الجديرة بالتذكّر. |
| ✍️ **اختبر نفسك (Check yourself)** | خمسة أسئلة، معظمها سيناريوهات (scenarios)، مع إجابات مخفية وشروح (hidden answers and explanations). |
| 📚 **المراجع (References)** | OWASP وMITRE وNIST ووثائق RFC (RFCs) والأوراق البحثية (papers) وغيرها من المصادر الأولية (primary sources). |

يُوسَم كل درس بـ**مرحلته في دورة حياة الأمن (security life cycle phase)**: Plan أو Design أو Build أو Test أو Deploy أو Operate أو Respond أو Govern. ويجمع [فهرس الأدوات (toolkit catalogue)](./TOOLKIT.ar.md) كل ضابط ومعيار وأداة (every control, standard and tool) في مكان واحد.

## الحالة المستمرة: فريق الأمن في بنك نجم (The running case: Najm Bank's security team)

تتابع الدورة فريق **أمن التطبيقات والذكاء الاصطناعي (Application & AI Security)** في **بنك نجم (Najm Bank)**، وهو البنك الخليجي الخيالي (fictional Gulf bank) المستخدم في جميع دورات هذه المكتبة (across this library). يحمي الفريق **تطبيق نجم للهاتف (Najm Mobile)** وواجهته البرمجية العامة (public API)، و**بوابة الشركات الصغيرة (SME Portal)** لعملاء الأعمال (business customers)، و**نجم أسيست (Najm Assist)** (مساعد قائم على نموذج لغوي كبير (LLM assistant) يتطور ليصبح وكيلًا يملك أدوات (agent with tools))، و**مساعد مذكرات الائتمان (Credit Memo Copilot)** (ذكاء اصطناعي توليدي داخلي (internal GenAI) مع استرجاع من مستندات البنك (retrieval over bank documents))، ونموذج كشف الاحتيال (fraud model) **التنبيهات الذكية (Smart Alerts)**، والمنصة السحابية للبنك (bank's cloud platform) ووكلاء البرمجة بالذكاء الاصطناعي (AI coding agents) لديه. و**نورة**، رئيسة أمن التطبيقات والذكاء الاصطناعي (Head of Application & AI Security)، هي مرشدتك (your mentor). وبحلول المشروع الختامي (capstone) ستكون قد أمّنت نجم أسيست (Najm Assist) من نموذج التهديدات (threat model) حتى تمرين محاكاة الحوادث (incident drill).

## الطريق من الصفر إلى الاحتراف (The path from zero to hero)

| المرحلة (Stage) | الوحدات (Modules) | ستكون قادرًا على… (You will be able to…) |
|---|---|---|
| 🟢 **الأسس (Foundations)** | 0–1 | شرح الأصول والمهاجمين والمخاطر (assets, attackers and risk)، وكيف تقع الاختراقات (how breaches happen)، ونمذجة التهديدات باستخدام STRIDE (model threats with STRIDE). |
| 🟡 **الممارس (Practitioner)** | 2–7 | إيجاد نقاط الضعف وإصلاحها (find and fix weaknesses) في الويب (web)، والهوية (identity)، وواجهات برمجة التطبيقات (API)، والهاتف المحمول (mobile)، والتشفير (crypto)، والأسرار (secrets)، وخطوط البناء والنشر (pipeline)، والسحابة (cloud). |
| 🔴 **المحترف (Hero)** | 8–12 | تأمين تطبيقات النماذج اللغوية الكبيرة والوكلاء (secure LLM apps and agents)، واختبار الذكاء الاصطناعي بأسلوب الفريق الأحمر (red-team AI)، ورصد الحوادث والاستجابة لها (detect and respond to incidents)، وقيادة برنامج أمني (lead a security programme)، واجتياز امتحان تدريبي من 60 سؤالًا (pass a 60-question practice exam). |

## الدورات المرافقة (Companion courses)

هذه الدورة هي طبقة الأمن (security layer) في المكتبة. وحين يمسّ درسٌ تصميمَ الأنظمة (system design)، أو مكوّنات بناء SaaS (SaaS building blocks)، أو الوكلاء (agents)، أو قانون الحوكمة (governance law)، أو قرارات المنتج (product decisions)، فإنه يحيلك إلى الدورة المرافقة (companion course) بدلًا من تكرارها: *System Design for Vibe Coders* و*SaaS Building Blocks* و*Production AI Agents* و*AI Governance: Zero to Hero* و*AI Product Management: Zero to Hero*.

## لغتان (Two languages)

كل درس متاح بالإنجليزية والعربية (English and Arabic). وفي النسخة العربية (Arabic edition) تحمل المصطلحات التقنية (technical terms) اسمها الإنجليزي بين قوسين، مثل «حقن الموجّهات (prompt injection)»، لأن المعايير والأدوات والنشرات الأمنية (standards, tools and advisories) التي ستعمل معها كلها بالإنجليزية.

## إلى أين بعد ذلك (Where to go next)

افتح خريطة الدورة (course map)، أو ابدأ بالدرس 0.1.
