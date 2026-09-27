# الوحدة 9 (Module 9) — البيانات للتدريب والاختبار (Data for training and testing)

*لا يمكن أن يكون النموذج (model) أفضل من البيانات التي يتعلّم منها والاختبارات (tests) التي يخضع لها. ومعظم الأضرار (harms) التي ظهرت في إخفاقات الذكاء الاصطناعي (AI) الحقيقية (التوظيف المتحيّز (biased hiring)، والائتمان غير العادل (unfair credit)، والمستفيدون من الإعانات (benefit claimants) الذين وُصموا خطأً) ترجع إلى بيانات أُخذت دون الحق في استخدامها، أو جُمعت بشكل غير متوازن، أو وُسمت بإهمال، أو لم تُختبر قط على الأشخاص الذين ستؤثر فيهم. تتتبّع هذه الوحدة بيانات بنك نجم (Najm Bank) عبر ثلاث بوابات (three gates): هل يجوز لنا استخدامها (المصادر (sourcing) وتسلسل البيانات (lineage) والحقوق (rights))، وهل هي جيدة بما يكفي وعادلة بما يكفي (الجودة (quality) والتمثيلية (representativeness) والتحيّز (bias))، وهل يعمل النظام فعلًا (الاختبار والتقييم والتحقق والمصادقة (test, evaluation, verification and validation)، واختبار الفريق الأحمر (red-teaming)). هذه الدورة لأغراض التعليم والتحضير للامتحان، وليست استشارة قانونية (not legal advice).*

> **تغطية مجال المعرفة (BoK coverage):** III.B — حوكمة (governance) جمع بيانات التدريب (training data) والاختبار (testing) والحقوق (rights) فيها وجودتها واستخدامها، واختبار أنظمة الذكاء الاصطناعي (AI systems) وتقييمها والمصادقة (validation) عليها قبل الإطلاق (launch).

---

# 9.1 — المصادر وتسلسل البيانات وحقوق استخدامها (Sourcing, lineage and rights to use data)
*المستوى: 🔴 متقدم (Level: Advanced)* · *المتطلبات: 3.2، 4.1، 5.2 (Prerequisites)* · *مجال المعرفة (BoK): III.B*

## ⚡ الدرس في دقيقة (In 60 seconds)
- تأتي بيانات التدريب (training data) من خمسة مصادر (sources) رئيسية: **بيانات الطرف الأول** (first-party) (سجلاتك الخاصة)، و**المشتراة أو المرخّصة** (purchased or licensed)، و**المجمّعة آليًا** (scraped) من الويب، و**الاصطناعية** (synthetic) (المولَّدة)، و**مجموعات البيانات العامة** (public datasets). ولكلٍّ منها ملف مختلف من الحقوق (rights) والمخاطر.
- **تسلسل البيانات** (lineage) يسجّل من أين جاءت البيانات وكل تحويل (every transformation) مرّت به. و**مصدر البيانات** (provenance) هو الدليل (evidence) على منشئها وأصالتها. ومن دونهما لا تستطيع إثبات حقوقك (prove your rights)، ولا إعادة إنتاج نموذجك، ولا تنفيذ طلب حذف (deletion request).
- **حق استخدام** البيانات (right to use) للذكاء الاصطناعي (AI) هو عدة أذونات منفصلة: أساس قانوني (lawful basis) في **الخصوصية** (privacy) وتوافق مع الغرض (purpose)، وشروط **العقد/الترخيص** (contract/licence)، و**حقوق النشر** (copyright) (بما فيها الانسحاب من استثناء التنقيب في النصوص والبيانات (text-and-data-mining opt-outs))، وواجبات **السرية** (confidentiality). وتحتاج إليها كلها، لا إلى واحد منها فقط.
- إعادة استخدام بيانات عملاء جُمعت لغرض (purpose) ما من أجل تدريب نموذج (model) هي **غرض جديد** (new purpose). ويجب أن يكون متوافقًا (GDPR المادة 6(4) (Art. 6(4))) أو أن يكون له أساسه القانوني الخاص.
- إشارة الامتحان (Exam cue): "متاح للعموم" لا يعني "مجاني الاستخدام". فالبيانات الشخصية (personal data) العامة تبقى بيانات شخصية، ومحتوى الويب العام يبقى محميًا بحقوق النشر (copyright).
- الفخ الأكبر (Biggest trap): اعتبار البيانات الاصطناعية (synthetic data) أو "المجهّلة" (anonymised) خارج قانون الخصوصية (privacy law) تلقائيًا.

## 🧭 لماذا يهم (Why it matters)
يريد فريق دانة إجراء الضبط الدقيق (fine-tune) للمساعد الذكي لمذكرات الائتمان (credit memo copilot) على مذكرات الائتمان التاريخية (historical credit memos) لبنك نجم (Najm Bank) خلال عشر سنوات. ويريدون أيضًا تحسين نموذج ائتمان الأفراد (retail credit model) بثلاثة مصادر (sources) إضافية: مجموعة بيانات مشتراة (purchased dataset) لسجلات سداد فواتير الاتصالات (telecom payment histories)، وإشارات من وسائل التواصل الاجتماعي (social-media signals) مجمّعة آليًا (scraped) من الملفات العامة للمتقدمين (applicants)، ومجموعة بيانات اصطناعية (synthetic data) ولّدها مورّد (vendor) "لسد الفجوات" الخاصة بالمتقدمين الشباب (young applicants). كل فكرة ممكنة تقنيًا. وعمر (رئيس البيانات، CDO) متحمس. أما سارة (مسؤولة حماية البيانات (Data Protection Officer, DPO)) فلديها أسئلة عن كل واحدة منها.

تحتوي المذكرات التاريخية (historical memos) على بيانات مالية للعملاء (client financials) قُدّمت في إطار السرية المصرفية (banking confidentiality)، وعلى بيانات شخصية عن الكفلاء (personal data about guarantors) جُمعت لتقييم (evaluation) القروض لا لتدريب الذكاء الاصطناعي (to train AI). وبيانات الاتصالات باعها وسيط (broker) لم يقرأ أحد صيغة الموافقة (consent language) لديه. وتجميع الملفات الاجتماعية آليًا (Scraping social profiles) يثير المسائل التي تناولها المجلس الأوروبي لحماية البيانات (EDPB) في رأيه 28/2024 (Opinion 28/2024) بشأن نماذج (models) الذكاء الاصطناعي (AI)، وقد فرضت عدة سلطات أوروبية لحماية البيانات (EU data protection authorities) غرامات (fines) على Clearview AI لتجميعها صور الوجوه من الويب (for scraping facial images from the web) دون أساس قانوني (lawful basis). والبيانات الاصطناعية (synthetic data) وُلّدت من بيانات حقيقية تعود إلى *شخص ما*. فمن هو؟ الحوكمة (governance) في هذه المرحلة تحدد هل تُبنى نماذج بنك نجم على أرض يملكها، أم على أرض قد يُضطر إلى إعادتها.

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**مصادر البيانات ومشكلاتها المعتادة (Data sources and their typical issues):**

| المصدر (source) | مثال في بنك نجم (Example at Najm) | مسائل الحوكمة المعتادة (Typical governance issues) |
|---|---|---|
| **الطرف الأول (first-party)** | طلبات القروض (loan applications) وسجلات السداد (repayment histories) | التوافق (compatibility) مع غرض الجمع الأصلي (original collection)؛ إشعارات الشفافية (transparency notices)؛ الاحتفاظ (retention)؛ السرية (confidentiality) |
| **مشتراة / مرخّصة (Purchased / licensed)** | بيانات سداد فواتير الاتصالات (telecom payment data) من وسيط (broker) | هل كان لدى الوسيط (broker) أساس قانوني (lawful basis) لبيعها، ولهذا الاستخدام؟ نطاق الترخيص (مجال الاستخدام (field of use)، الإقليم (territory)، تدريب الذكاء الاصطناعي (AI training)، الأعمال المشتقة (derivatives))؛ الضمانات والتعويضات (warranties and indemnities)؛ الجودة (quality) |
| **مجمّعة آليًا (scraped)** | ملفات عامة على وسائل التواصل الاجتماعي (social media)؛ مواقع ويب | الأساس القانوني (lawful basis) للبيانات الشخصية (personal data)؛ شروط المواقع (website terms)؛ حقوق النشر (copyright) والانسحاب من التنقيب في النصوص والبيانات (TDM opt-outs)؛ التوقعات المعقولة (reasonable expectations) لأصحاب البيانات (data subjects)؛ الدقة (accuracy) |
| **اصطناعية (synthetic)** | سجلات "متقدمين شباب (young applicants)" ولّدها مورّد (vendor) | الحقوق (rights) في بيانات المصدر (source data) المستخدمة لتوليدها؛ خطر إعادة التعرّف (re-identification risk)؛ الأمانة (هل تعكس الواقع؟)؛ قد تضخّم تحيّزات المصدر (source biases) |
| **مجموعات بيانات عامة (public datasets)** | مجموعات بيانات مرجعية مفتوحة (open benchmark datasets) | شروط الترخيص (بعضها يمنع الاستخدام التجاري (commercial use))؛ مصدر موثّق (documented provenance)؛ تحيّزات معروفة (known biases)؛ تلوّث مجموعات الاختبار (contamination of test sets) |

**تسلسل البيانات ومصدرها (Lineage and provenance).**
- **تسلسل البيانات** (data lineage) هو المسار القابل للتتبّع للبيانات من المصدر (source) عبر كل استخراج ودمج وتصفية وتحويل ووسم (extraction, join, filter, transformation and label) وصولًا إلى مجموعة التدريب (training set) ونسخة النموذج (model version). ويجيب عن السؤال "أي بيانات صنعت هذا النموذج (model)؟"
- **مصدر البيانات** (provenance) هو المنشأ الموثّق (documented origin) وسلسلة الحيازة (chain of custody): من جمعها، ومتى، وكيف، وبأي شروط. ويجيب عن "هل نستطيع إثبات أنه كان مسموحًا لنا باستخدامها؟"

وكلاهما لازم من أجل: إعادة إنتاج نموذج (model) للمصادقة (validation) عليه؛ وإثبات الحقوق (proving rights) أمام جهة تنظيمية؛ والعثور على النماذج (models) المتأثرة عندما يتبيّن أن البيانات خاطئة أو غير مشروعة (unlawful)؛ وتنفيذ طلبات المحو والاعتراض (erasure and objection)؛ واستيفاء متطلبات (requirements) حوكمة البيانات في قانون الذكاء الاصطناعي الأوروبي (EU AI Act) للأنظمة عالية المخاطر (high-risk systems)، ومنها توثيق (documentation) عمليات جمع البيانات ومنشأ البيانات (origin of data). ويتوقع الملف الفني وفق الملحق IV (8.3) أن يُوصف مصدر البيانات (provenance) وإعدادها.

**الاحتفاظ (Retention).** لا تُحفظ بيانات التدريب (training data) إلى الأبد "تحسّبًا". فتقييد التخزين (storage limitation) (GDPR المادة 5(1)(e) (Art. 5(1)(e))) يوجب ألا تُحفظ البيانات القابلة للتعرّف (identifiable data) مدة أطول مما يلزم للغرض (purpose). ويجب أن يوازن الاحتفاظ لأغراض الذكاء الاصطناعي (AI) بين حاجتين: قابلية إعادة الإنتاج والتدقيق (reproducibility and audit) من جهة (فقد يحتاج المصادِقون (validators) والجهات التنظيمية (regulators) إلى رؤية ما دُرّب عليه النموذج (model))، وتقليل البيانات (minimisation) من جهة أخرى. ومن الأنماط الشائعة الاحتفاظ بلقطة (snapshot) من مجموعة التدريب (training set) ذات إصدار محدد وخاضعة لضوابط الوصول (access controls) طوال العمر المدعوم للنموذج (model's supported life) مضافًا إليه فترة تدقيق (audit period)، مع الترميز المستعار (pseudonymised) حيثما أمكن، ثم حذفها وفق جدول زمني محدد (defined schedule).

### 🟡 التعمق أكثر (Going deeper)

**حقوق الاستخدام: أربعة أقفال منفصلة (Rights to use: four separate locks).** تخيّل كل مجموعة بيانات (dataset) خلف أربعة أقفال. وتحتاج إلى مفتاح لكل واحد منها.

1. **قانون الخصوصية (privacy law).** هل تتضمن البيانات بيانات شخصية (personal data)؟ إن كان الأمر كذلك فأنت تحتاج إلى **أساس قانوني** (lawful basis) بموجب GDPR المادة 6 (للتدريب، عادةً المصلحة المشروعة (legitimate interests)، أو الموافقة (consent) بدرجة أقل). وللفئات الخاصة (special categories) تحتاج أيضًا إلى شرط من المادة 9 (Art. 9). ولبيانات قطر أو الإمارات تنطبق متطلبات (requirements) PDPPL أو UAE PDPL. فقانون PDPPL القطري مثلًا يمنح بعض "البيانات الشخصية ذات الطبيعة الخاصة (personal data of a special nature)" حماية إضافية، لذا تحقّق من القواعد الحالية وإرشادات الجهة التنظيمية (regulator guidance) مع مستشار قانوني محلي (local counsel).
2. **العقد (contract) أو الترخيص (licence).** تأتي مجموعات البيانات (datasets) المشتراة والعامة مع شروط: الاستخدامات المسموح بها (permitted uses)، وهل يُسمح بتدريب الذكاء الاصطناعي (AI training) والاستخدام التجاري (commercial use)، والإسناد، وإعادة التوزيع (attribution, redistribution)، والأعمال المشتقة (derivatives)، والإقليم (territory). وقد تقيّد عقود العملاء (Customer contracts) الاستخدام أيضًا، وكذلك شروط الموردين (مثل شروط مزوّد API (API provider) بشأن استخدام المخرجات (outputs) لتدريب نماذج منافسة (competing models)).
3. **حقوق النشر والحقوق المجاورة (Copyright and related rights).** قد تكون النصوص والصور والشيفرات وقواعد البيانات محمية. ففي الاتحاد الأوروبي، تنص توجيهة حقوق النشر في السوق الرقمية الموحدة (Copyright in the Digital Single Market Directive) (EU) 2019/790 على استثناءات للتنقيب في النصوص والبيانات (text-and-data-mining, TDM). المادة 3 تغطي مؤسسات البحث (research organisations) ومؤسسات التراث الثقافي (cultural heritage institutions). والمادة 4 تغطي أي جهة أخرى، لكن فقط إذا *لم يحتفظ* صاحب الحقوق (rightsholder) بحقوقه "بطريقة مناسبة"، وهذا يعني بالنسبة إلى المحتوى المتاح للعموم على الإنترنت وسائل قابلة للقراءة آليًا (مثل إشارات على نمط robots.txt أو إشارات في البيانات الوصفية (metadata)). ويشترط قانون الذكاء الاصطناعي الأوروبي (EU AI Act) على مقدّمي نماذج الذكاء الاصطناعي للأغراض العامة (GPAI) أن تكون لديهم سياسة للامتثال لقانون حقوق النشر الأوروبي (policy to comply with EU copyright law)، بما في ذلك تحديد هذه التحفظات (these reservations) واحترامها، وأن ينشروا ملخصًا مفصّلًا بما يكفي عن محتوى التدريب (sufficiently detailed summary of training content). وخارج الاتحاد الأوروبي يختلف الوضع (مثل "الاستخدام العادل" (fair use) في الولايات المتحدة الذي يُحسم في المحاكم قضية بقضية). انظر 5.2.
4. **السرية (confidentiality).** قد تمنع السرية المصرفية (banking confidentiality) واتفاقيات عدم الإفصاح (NDAs) والأسرار التجارية (trade secrets) والسرية المهنية أو التنظيمية (professional or regulatory confidentiality) استخداماتٍ يسمح بها قانون الخصوصية (privacy law). فالبيانات المالية للعملاء (client financials) في مذكرات الائتمان (credit memos) لدى بنك نجم سرية بصرف النظر عن كونها بيانات شخصية (personal data) أم لا.

**الموافقة والتوافق مع الغرض (Consent and purpose compatibility).** بموجب GDPR، يجب أن تُجمع البيانات الشخصية (personal data) لأغراض محددة وصريحة ومشروعة (specified, explicit and legitimate purposes)، وألا تُعالج لاحقًا بطريقة لا تتوافق معها (المادة 5(1)(b)، تحديد الغرض (purpose limitation)). وعندما تريد إعادة استخدام البيانات لتدريب نموذج (model)، تحدد المادة 6(4) اختبارًا للتوافق (compatibility). وهو ينظر في الصلة بين الغرض الأصلي (original purpose) والغرض الجديد (new purpose)، وسياق الجمع (وخاصة العلاقة مع أصحاب البيانات (data subjects) وتوقعاتهم المعقولة (their reasonable expectations))، وطبيعة البيانات (فئات خاصة (special categories)؟ بيانات جنائية (criminal data)؟)، والعواقب المحتملة (possible consequences) على أصحاب البيانات، والضمانات (التشفير (encryption)، والترميز المستعار (pseudonymisation)). فإذا كان الغرض الجديد متوافقًا (the new purpose is compatible)، فقد ينتقل الأساس الأصلي إليه. وإذا لم يكن كذلك، فأنت تحتاج إلى أساس جديد، وغالبًا ما يكون الموافقة (consent). وتنطبق أيضًا التزامات الشفافية (transparency): يجب إبلاغ الناس بالأغراض الجديدة (new purposes) قبل بدء المعالجة (the processing starts).

*الموافقة (consent)* لا تناسب معظم عمليات التدريب. فيجب أن تُعطى بحرية، وأن تكون محددة ومستنيرة ولا لبس فيها، ويمكن سحبها، وهذا يثير سؤال ما الذي تفعله بنموذج (model) دُرّب بالفعل. وحيث يوجد اختلال واضح في القوة (صاحب العمل والموظف (employer–employee)) أو حيث تُشترط الموافقة للحصول على خدمة، يُستبعد أن تكون الموافقة قد أُعطيت بحرية. أما المصلحة المشروعة (legitimate interests) فتتطلب اختبارًا موثّقًا من ثلاثة أجزاء (مصلحة مشروعة (a legitimate interest)؛ الضرورة (necessity)؛ الموازنة (balancing) مع حقوق الأفراد وتوقعاتهم المعقولة (their reasonable expectations)). ويصف رأي EDPB رقم 28/2024 (EDPB Opinion 28/2024) كيف يمكن للسلطات الرقابية (supervisory authorities) تقييمها في تطوير الذكاء الاصطناعي (AI)، بما في ذلك تدابير التخفيف (mitigations) مثل استبعاد مصادر (sources) معينة، واحترام طلبات الانسحاب (opt-outs)، والشفافية الإضافية (extra transparency).

**التجميع الآلي من الويب (Web scraping).** تجميع البيانات الشخصية آليًا (Scraping personal data) ليس غير مشروع (unlawful) في حد ذاته في الاتحاد الأوروبي، لكنه يحتاج إلى أساس قانوني (lawful basis)، واحترام التوقعات المعقولة (reasonable expectations) لأصحاب البيانات (data subjects)، وتدابير تخفيف (mitigations). أمثلة: استبعاد المصادر الحساسة (sensitive sources)، وتصفية بيانات الفئات الخاصة (filter out special-category data)، واحترام robots.txt وغيره من آليات الانسحاب (opt-outs)، وتقليل البيانات (minimisation). ويتناول رأي EDPB رقم 28/2024 (EDPB Opinion 28/2024) أيضًا ما يحدث لاحقًا عندما يكون النموذج (model) قد *طُوّر ببيانات شخصية (personal data) عولجت بشكل غير مشروع (unlawfully processed)*. فقد تتأثر مشروعية النشر اللاحق (lawfulness of later deployment) بحسب الحالة، بما في ذلك هل جرى تجهيل النموذج فعليًا (the model has been effectively anonymised). وتُظهر إجراءات الإنفاذ (enforcement actions) ضد Clearview AI النهاية التي يؤول إليها التجميع الآلي (scraping) دون أساس قانوني: غرامات (fines)، وأوامر حذف (deletion orders)، وحظر. (and bans)

### 🔴 نظرة الخبير (Expert view)

**البيانات الاصطناعية ليست تصريح مرور مجانيًا (Synthetic data is not a free pass).** تُولَّد البيانات الاصطناعية (synthetic data) بواسطة نموذج (model) دُرّب على بيانات حقيقية، أو بالمحاكاة (simulation). وأسئلة حوكمتها هي:
- *الحقوق تُورَّث (Rights inherit).* توليدها معالجةٌ لبيانات المصدر (source data)، وهذه تحتاج إلى أساس قانوني (lawful basis).
- *يجب إثبات إخفاء الهوية لا افتراضه (Anonymity must be shown, not assumed).* قد تحفظ المولِّدات (generators) سجلات حقيقية وتعيد إنتاجها، وخاصة الحالات الشاذة (outliers). اختبر خطر إعادة التعرّف (re-identification) وخطر استنتاج العضوية (membership inference) قبل معاملة البيانات الاصطناعية (synthetic data) على أنها غير شخصية.
- *الأمانة والتحيّز (Fidelity and bias).* تعيد البيانات الاصطناعية (synthetic data) إنتاج الأنماط الموجودة في مصدرها، وقد تضخّمها. فتوليد "متقدمين شباب" من مجموعة بيانات (dataset) كان المتقدمون الشباب (young applicants) فيها يُرفضون تاريخيًا قد يرسّخ ذلك التاريخ.
- *تلوّث التقييم (Evaluation contamination).* لا تصادق أبدًا على نموذج (model) باستخدام بيانات اصطناعية (synthetic data) وحدها وُلّدت من المصدر (source) نفسه الذي جاءت منه بيانات تدريبه.

**إخفاء هوية النماذج نفسها (Anonymisation of models themselves).** يرى رأي EDPB رقم 28/2024 (EDPB Opinion 28/2024) أن نموذج الذكاء الاصطناعي (AI) المدرَّب على بيانات شخصية (personal data) لا يمكن افتراض أنه مجهول الهوية (anonymous). وتحديد ما إذا كان مجهول الهوية تقييم يُجرى حالة بحالة (case-by-case assessment): يجب أن يكون احتمال استخراج بيانات شخصية (likelihood of extracting personal data) من النموذج (model)، مباشرة أو عبر الاستعلامات، ضئيلًا. وهذا مهم عندما يشتري بنك نجم نماذج (models) أو يبنيها. فقد يكون النموذج "بيانات شخصية" بمعنى الحوكمة (governance)، وقد تمتد إليه حقوق الحذف (deletion rights) وواجبات الأمن (security).

**تسلسل البيانات عمليًا (Lineage in practice).** تستخدم الفرق الناضجة فهارس البيانات (data catalogues) وأدوات تسلسل البيانات (lineage tools) التي تسجّل إصدارات مجموعات البيانات (dataset versions)، والمخططات (schemas)، والمالكين، وعقود المصادر (source contracts)، ووسوم الأساس القانوني (legal basis tags)، والتحويلات (transformations)، وتربط كل نسخة من النموذج (model version) بإصدارات مجموعات البيانات (datasets) التي استخدمها بالضبط. وينبغي للحوكمة (governance) أن تشترط: **ورقة بيانات مجموعة البيانات** (datasheet) لكل مجموعة بيانات (dataset) تدريب واختبار (8.3)؛ و**سجل حقوق** (rights register) يربط كل مصدر بأساسه القانوني وترخيصه (its licence) وقيوده؛ و**وسومًا** (tags) ترافق البيانات أينما ذهبت (مثل "لا لتدريب الذكاء الاصطناعي (to train AI)"، "الاتحاد الأوروبي فقط"، "تُحذف بحلول 2029-12").

**الاحتفاظ والمحو بعد التدريب (Retention and erasure after training).** عندما يمارس صاحب البيانات (data subject) حقه في المحو أو الاعتراض (erasure or objection)، يكون حذف السجل من المصدر (source) أمرًا مباشرًا. لكن ماذا عن النموذج (model) المدرَّب؟ تتراوح الخيارات بين الإزالة عند إعادة التدريب المجدولة (scheduled retrain) التالية، وتقنيات "إلغاء التعلّم الآلي" (machine unlearning) (وهي مجال بحث نشط، لا ضمانة ناضجة)، وتقييم (evaluation) ما إذا كان النموذج يحتفظ أصلًا ببيانات شخصية (personal data) قابلة للاستخراج (extraction). وينبغي للحوكمة (governance) أن تقرر النهج مسبقًا، وأن توثّقه في تقييم الأثر على حماية البيانات (DPIA)، وأن تذكره في إشعارات الخصوصية (privacy notices).

**الاستخدام المتناسب لمصادر البيانات الجديدة (Proportionate use of new data sources).** إضافة إشارات وسائل التواصل الاجتماعي (social-media signals) إلى تقييم الجدارة الائتمانية (creditworthiness evaluation) ليست مسألة حقوق (rights issue) فقط. هل هي ضرورية؟ هل هي دقيقة؟ هل يتوقعها المتقدمون (applicants)؟ هل تُحدث تمييزًا بالوكالة (proxy discrimination)؟ هل ستراها الجهة التنظيمية (regulator) عادلة؟ ينبغي للجنة (committee) بنك نجم أن تطبّق عدسة التناسب (proportionality lens) نفسها المستخدمة عند الاستقبال (8.1).

## ⚖️ الأدوات التنظيمية (The instruments)
| الأداة | ما تشترطه أو توصي به (What it requires or recommends) | إشارة الامتحان (Exam cue) |
|---|---|---|
| **GDPR** — المواد 5(1)(b) و5(1)(e) و6(4) | تحديد الغرض (purpose limitation)؛ تقييد التخزين (storage limitation)؛ اختبار التوافق للمعالجة اللاحقة (compatibility test for further processing) | إعادة استخدام بيانات العملاء (client data) للتدريب = غرض جديد (new purpose) |
| **GDPR** — المواد 6 و9 و13–14 | الأساس القانوني (lawful basis)؛ شروط الفئات الخاصة (special-category conditions)؛ الشفافية (transparency)، بما فيها للبيانات التي لم تُجمع من الشخص نفسه | البيانات المجمّعة آليًا (scraped data) تحتاج أيضًا إلى أساس وشفافية (transparency) |
| **EDPB Opinion 28/2024** | متى تكون نماذج (models) الذكاء الاصطناعي (AI) مجهولة الهوية (anonymous)؛ المصلحة المشروعة (legitimate interests) في التطوير (development) والنشر (deployment)؛ عواقب بيانات التدريب (training data) المعالَجة بشكل غير مشروع (unlawfully processed) | النماذج (models) ليست مجهولة الهوية (anonymous) تلقائيًا |
| **EU DSM Copyright Directive** — المادتان 3 و4 | استثناءات التنقيب في النصوص والبيانات (TDM exceptions)؛ المادة 4 خاضعة لتحفظات الحقوق القابلة للقراءة آليًا (machine-readable rights reservations) على الإنترنت | احترم الانسحاب من التنقيب في النصوص والبيانات (TDM opt-outs) |
| **EU AI Act** — المادة 53 (Art. 53) | مقدّمو نماذج GPAI (GPAI model providers): سياسة امتثال لحقوق النشر (copyright-compliance policy) تشمل احترام تحفظات التنقيب (TDM reservations)؛ ملخص علني لمحتوى التدريب (public summary of training content) | واجبات حقوق النشر على GPAI (GPAI copyright duties) |
| **EU AI Act** — المادة 10 | حوكمة البيانات (data governance) للأنظمة عالية المخاطر (high-risk systems)، بما فيها عمليات جمع البيانات ومنشؤها وعمليات إعدادها | مصدر البيانات (provenance) متطلب قانوني للأنظمة عالية المخاطر (high-risk systems) |
| **Qatar PDPPL** | القانون رقم 13 لسنة 2016: المعالجة المشروعة (lawful processing)، والشفافية (transparency)، وحماية إضافية للبيانات الشخصية ذات الطبيعة الخاصة (personal data of a special nature) | بيانات الخليج تحتاج إلى تحليل محلي |
| **ISO/IEC 42001** | ضوابط (controls) نظام إدارة الذكاء الاصطناعي (AI management system) التي تغطي بيانات أنظمة الذكاء الاصطناعي (AI systems): الاقتناء، والجودة (quality)، والمصدر (source)، والإعداد | ضوابط (controls) بيانات قابلة للاعتماد |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
**سجل حقوق بيانات التدريب (Training Data Rights Register)**، تراجعه سارة (مسؤولة حماية البيانات (Data Protection Officer, DPO)) والإدارة القانونية (Legal) وعمر (رئيس البيانات):

| مجموعة البيانات (dataset) | نوع المصدر (source type) | الأساس القانوني / الشرط (Lawful basis / condition) | الترخيص / العقد (Licence / contract) | حقوق النشر / السرية (Copyright / confidentiality) | القرار |
|---|---|---|---|---|---|
| طلبات الأفراد وسجلات السداد (Retail applications and repayments) 2017–2024 | الطرف الأول (first-party) | المصلحة المشروعة (تقييم التوافق (compatibility assessment) CA-07؛ مرجع DPIA)؛ حُدّثت الإشعارات في 2026 | لا ينطبق (n/a) | السرية المصرفية (banking confidentiality): للاستخدام الداخلي (internal use) فقط | ✅ مُعتمد؛ بترميز مستعار؛ الاحتفاظ (retention) = عمر النموذج (model life) + 7 سنوات، مع المراجعة |
| سجلات سداد فواتير الاتصالات (telecom payment histories) | مشتراة (purchased) | يدّعي الوسيط (broker) وجود موافقة (consent)؛ نص الموافقة (consent text) لا يذكر تقييم الجدارة الائتمانية من أطراف ثالثة (credit scoring by third parties) | الترخيص (licence) لا يذكر تدريب الذكاء الاصطناعي (AI training) | لا ينطبق (n/a) | ⛔ مرفوض إلى حين الحصول على ترخيص جديد (new licence) ودليل (evidence) على الأساس |
| إشارات عامة من وسائل التواصل الاجتماعي (social media) | مجمّعة آليًا (scraped) | لم يوجد أساس متناسب (proportionate)؛ عدم تطابق كبير مع التوقعات (high expectation mismatch) | شروط المنصة (Platform terms) تمنع التجميع الآلي (scraping) | حقوق النشر (copyright) في المنشورات | ⛔ مرفوض: لا يجتاز اختبار التناسب (proportionality) |
| بيانات اصطناعية (synthetic data) للمتقدمين الشباب (young applicants) | اصطناعية (مورّد (vendor)) | ولّدها المورّد (vendor) من بيانات عملائه: الأساس غير مُتحقَّق منه | العقد (contract) قيد المراجعة | لا ينطبق (n/a) | ⏸ معلّق: يلزم إثبات حقوق المصدر (source rights) واختبار إعادة التعرّف (re-identification test) |
| مذكرات الائتمان التاريخية (historical credit memos) 2015–2025 (الضبط الدقيق (fine-tuning) للمساعد (copilot)) | الطرف الأول (first-party) | البيانات الشخصية للكفلاء (Guarantor personal data): التوافق (compatibility) مشكوك فيه؛ التقليل عبر الحجب (minimise via redaction) | اتفاقيات العملاء (Client agreements): بنود سرية (confidentiality clauses) | معلومات سرية للعملاء (Client confidential information) | ⏸ تُستخدم للتوليد المعزّز بالاسترجاع (RAG) مع صلاحيات الوصول فقط؛ الضبط الدقيق (fine-tuning) مؤجّل |

قاعدة دائمة اعتمدتها اللجنة (Standing rule adopted by the committee): *"لا يجوز استخدام أي مجموعة بيانات (dataset) لتدريب نظام ذكاء اصطناعي (AI system) أو ضبطه ضبطًا دقيقًا (fine-tuning it) أو تقييمه ما لم تكن مدرجة في السجل بحالة مُعتمدة ومعها ورقة بيانات (datasheet)."*

## 🛠️ التمارين (Exercises)
- 🟢 صنّف خمس مجموعات بيانات (datasets) تعرفها (في العمل أو عامة) حسب نوع المصدر (source type)، واذكر مسألة حقوق (rights issue) واحدة لكل منها. *يكتمل عندما (Done when):* يكون لكل منها نوع مصدر وقفل محدد (الخصوصية (privacy)، أو الترخيص (licence)، أو حقوق النشر (copyright)، أو السرية (confidentiality)).
- 🟡 أجرِ تقييم توافق (compatibility assessment) وفق GDPR المادة 6(4) لاستخدام تسجيلات مركز الاتصال (call-centre recordings) في بنك نجم لتدريب روبوت محادثة خدمة العملاء (customer-service chatbot). *يكتمل عندما (Done when):* تتناول العوامل الخمسة كلها وتصل إلى استنتاج مُعلَّل مع ضمانات (safeguards).
- 🔴 تطلب عميلة محو بياناتها (erasure) بعد أن دُرّب نموذج الائتمان (credit model) في بنك نجم على بياناتها. صُغ موقف بنك نجم بشأن حذف المصدر (source deletion)، ووتيرة إعادة تدريب النموذج (model retraining cadence)، وإلغاء التعلّم (unlearning)، وما يُقال للعميلة. *يكتمل عندما (Done when):* تكون السياسة متسقة مع تقييم الأثر على حماية البيانات (DPIA) وإشعار الخصوصية (privacy notice)، ولا تبالغ في الوعد بالحذف التقني (technical deletion).

## ⚠️ أخطاء وفخاخ الامتحان (Mistakes and exam traps)
- **"إنها عامة، إذن يمكننا استخدامها."** البيانات الشخصية (personal data) العامة تحتاج مع ذلك إلى أساس قانوني (lawful basis). والمحتوى العام يبقى خاضعًا لحقوق النشر (copyright) والشروط.
- **"لدينا أساس قانوني (lawful basis)، إذن انتهينا."** الترخيص (licence) وحقوق النشر (copyright) والسرية (confidentiality) أقفال منفصلة (separate locks).
- **"اصطناعية/مجهّلة (Synthetic/anonymised) = ليست بيانات شخصية (personal data)."** فقط إذا ثبت أن خطر إعادة التعرّف (re-identification risk) ضئيل. ويقول EDPB إن النماذج (models) ليست مجهولة الهوية (anonymous) تلقائيًا.
- **الاعتماد على الموافقة (consent) في كل شيء.** كثيرًا ما لا تُعطى بحرية، ويصعب احترام سحبها في نموذج (model) مدرَّب. فكّر في الأساس الأنسب.
- **غياب تسلسل البيانات (lineage).** من دونه لا تستطيع إثبات الحقوق (proving rights)، ولا إعادة إنتاج النتائج، ولا العثور على النماذج (models) المتأثرة.
- **الاحتفاظ (retention) ببيانات التدريب (training data) إلى أجل غير مسمى "للتدقيق".** حدّد مدة احتفاظ (retention period) وبرّرها.

## 🧾 الخلاصة (Recap)
- خمسة أنواع من المصادر (sources)، لكلٍّ منها ملفه الخاص من الحقوق (rights) والمخاطر.
- تسلسل البيانات (lineage) يتتبّعها عبر التحويلات (transformations) وصولًا إلى نسخ النموذج (model versions). ومصدر البيانات (provenance) يثبت المنشأ (origin) والشروط.
- حقوق الاستخدام (rights to use) = أساس الخصوصية (privacy) + الترخيص (licence) + حقوق النشر (copyright)/التنقيب في النصوص والبيانات (text-and-data mining) + السرية (confidentiality).
- إعادة الاستخدام للتدريب غرض جديد (new purpose). طبّق اختبار التوافق (compatibility test) وحدّث الشفافية (transparency).
- البيانات الاصطناعية (synthetic data) والنماذج (models) المدرَّبة قد تظل تنطوي على بيانات شخصية (personal data). والاحتفاظ (retention) يحتاج إلى مدة محددة ومبرَّرة.

## ✍️ اختبر نفسك (Check yourself)

**1. يريد بنك نجم استخدام بيانات طلبات القروض (loan applications) لعشر سنوات، التي جُمعت للبت في تلك القروض، لتدريب نموذج ائتمان (credit model) جديد. ما التحليل الأساسي بموجب GDPR؟**

- A. لا شيء؛ فبنك نجم يحتفظ بالبيانات أصلًا
- B. هل الغرض الجديد (new purpose) متوافق مع الغرض الأصلي (original purpose)، بالنظر إلى الصلة والسياق (context) وطبيعة البيانات (nature of the data) والعواقب والضمانات (safeguards)، وإلا فالحاجة إلى أساس قانوني (lawful basis) جديد
- C. هل البيانات مشفّرة (encrypted) فقط
- D. هل وقّع المتقدمون (applicants) نموذجًا (model) ورقيًا

<details><summary>الإجابة (Answer)</summary>

**B.** يجب أن تكون المعالجة اللاحقة (further processing) متوافقة (المادة 6(4)) أو أن تستند إلى أساس جديد، مع الشفافية (transparency). والتشفير (C) ضمانة ضمن ذلك الاختبار (testing)، وليس التحليل كله. (🟡 التعمق أكثر (Going deeper).)

</details>

**2. مقدّم نموذج ذكاء اصطناعي للأغراض العامة (provider of a general-purpose AI model) يجمع آليًا مواقع ويب أوروبية متاحة للعموم لأغراض التدريب. أي عبارة هي الأدق؟**

- A. ينطبق استثناء التنقيب في النصوص والبيانات (TDM exception) في المادة 4 من توجيهة DSM (DSM Directive) ما لم يحتفظ أصحاب الحقوق (rightsholders) بحقوقهم بطريقة مناسبة (وبالنسبة إلى المحتوى على الإنترنت، قابلة للقراءة آليًا (machine-readable))، ويشترط قانون الذكاء الاصطناعي (AI) على مقدّمي GPAI أن تكون لديهم سياسة لاحترام هذه التحفظات (policy to respect such reservations)
- B. محتوى الويب العام خالٍ من حقوق النشر (copyright)
- C. يعفي قانون الذكاء الاصطناعي (AI) كل تدريب للذكاء الاصطناعي من حقوق النشر (copyright)
- D. مؤسسات البحث (research organisations) وحدها يجوز لها التدريب على بيانات الويب

<details><summary>الإجابة (Answer)</summary>

**A.** تسمح المادة 4 بالتنقيب في النصوص والبيانات (text-and-data mining) مع مراعاة الانسحاب (opt-out)، ويجب أن تكون لدى مقدّمي GPAI سياسة امتثال لحقوق النشر (copyright-compliance policy). أما D فيصف المادة 3، وهي واحد فقط من الاستثناءين. (🟡 التعمق أكثر (Going deeper).)

</details>

**3. يعرض مورّد (vendor) على بنك نجم بيانات متقدمين اصطناعية (synthetic) "مجهولة الهوية تمامًا (fully anonymous)". ما الذي ينبغي أن تشترطه الحوكمة (governance) أولًا؟**

- A. لا شيء؛ البيانات الاصطناعية (synthetic data) خارج نطاق GDPR
- B. سعرًا أقل
- C. دليلًا على حقوق المورّد (vendor) في بيانات المصدر (source data) وتقييمًا لخطر إعادة التعرّف (re-identification risk)، إضافة إلى مراجعة للأمانة والتحيّز (fidelity and bias review)
- D. أن ينشر بنك نجم البيانات

<details><summary>الإجابة (Answer)</summary>

**C.** البيانات الاصطناعية (synthetic data) ترث أسئلة الحقوق (rights questions)، وقد تسرّب (leakage) مصدرها أو تضخّمه. وA هو الفخ. (🔴 نظرة الخبير (Expert view).)

</details>

**4. ما الذي يتيحه تسلسل البيانات (lineage) في المقام الأول؟**

- A. تدريبًا أسرع للنموذج (model)
- B. اختيار مقياس للعدالة (fairness)
- C. تشفير البيانات المخزّنة
- D. تتبّع أي بيانات، وعبر أي تحويلات، أنتجت نسخة معينة من النموذج (model)، بما يدعم قابلية إعادة الإنتاج (reproducibility) وإثبات الحقوق (proving rights) والاستجابة لأخطاء البيانات أو طلبات المحو (erasure requests)

<details><summary>الإجابة (Answer)</summary>

**D.** يربط تسلسل البيانات (lineage) بين المصادر (sources) والتحويلات (transformations) ونسخ النموذج (model versions). وهذا الربط هو ما تعتمد عليه الحوكمة (governance) في قابلية إعادة الإنتاج (reproducibility) والحقوق والمعالجة (rights and remediation). (🟢 الأساسيات (The essentials).)

</details>

**5. وفقًا لرأي EDPB رقم 28/2024 (EDPB Opinion 28/2024)، فإن نموذج (model) الذكاء الاصطناعي (AI) المدرَّب على بيانات شخصية (personal data):**

- A. مجهول الهوية (anonymous) دائمًا لأنه يخزّن المعاملات (parameters) فقط
- B. ليس مجهول الهوية (anonymous) أبدًا
- C. لا يمكن افتراض أنه مجهول الهوية (anonymous)؛ يجب تقييم (evaluation) إخفاء الهوية (anonymity) حالة بحالة (case by case)، بما في ذلك احتمال استخراج بيانات شخصية (likelihood of extracting personal data) منه
- D. مجهول الهوية (anonymous) إذا قال المقدّم ذلك في شروطه

<details><summary>الإجابة (Answer)</summary>

**C.** يشترط EDPB تقييمًا حالة بحالة (case-by-case assessment). وA وB كلاهما عبارتان مطلقتان، وهذه هي العلامة المعتادة على الخيار المضلِّل في الامتحان. (🔴 نظرة الخبير (Expert view).)

</details>

## 📚 المراجع (References)
- GDPR، اللائحة (EU) 2016/679 — https://eur-lex.europa.eu/eli/reg/2016/679/oj
- EDPB، الرأي 28/2024 بشأن بعض جوانب حماية البيانات (data protection) المتعلقة بمعالجة البيانات الشخصية (personal data) في سياق نماذج الذكاء الاصطناعي (Opinion 28/2024) — https://www.edpb.europa.eu
- التوجيهة (EU) 2019/790 بشأن حقوق النشر في السوق الرقمية الموحدة (copyright in the Digital Single Market) — https://eur-lex.europa.eu/eli/dir/2019/790/oj
- EU AI Act، اللائحة (EU) 2024/1689 — https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- المفوضية الأوروبية (European Commission)، مكتب الذكاء الاصطناعي (AI Office) (مدونة الممارسات لنماذج GPAI (GPAI Code of Practice) ونموذج ملخص محتوى التدريب (training-content summary template)) — https://digital-strategy.ec.europa.eu/en/policies/ai-office
- البوابة القانونية القطرية (الميزان، Al Meezan)، القانون رقم 13 لسنة 2016 — https://www.almeezan.qa
- ISO/IEC 42001:2023 — https://www.iso.org/standard/81230.html
- IAPP، مجال المعرفة (BoK) لشهادة AIGP — https://iapp.org/certify/aigp/

---

# 9.2 — الجودة والتمثيلية والتحيّز (Quality, representativeness and bias)
*المستوى: 🔴 متقدم (Level: Advanced)* · *المتطلبات: 9.1، 5.1 (Prerequisites)* · *مجال المعرفة (BoK): III.B*

## ⚡ الدرس في دقيقة (In 60 seconds)
- **جودة البيانات** (data quality) لها عدة أبعاد: الدقة (accuracy)، والاكتمال (completeness)، والاتساق (consistency)، والحداثة (timeliness)، والصلاحية (validity)، والتفرّد (uniqueness). ولها أيضًا **الملاءمة للغرض** (fitness for purpose)، وهو البعد (Dimension) الأهم.
- **التمثيلية** (representativeness) تسأل هل تعكس البيانات الأشخاص والظروف التي سيواجهها النظام فعلًا. وقد تكون مجموعة بيانات (dataset) كبيرة غير تمثيلية (unrepresentative) مع ذلك.
- **الوسوم** (labels) بيانات أيضًا. وتعتمد جودة الوسوم (label quality) على إرشادات واضحة للمُوسِّمين (annotators)، ومُوسِّمين مدرَّبين (trained annotators)، وفحوص للاتفاق (agreement checks)، والوعي بأن الوسوم التاريخية (مثل "تعثّر في السداد"، "عُيّن") تُرمّز قرارات سابقة.
- يدخل التحيّز (bias) في كل مرحلة: **التاريخي (historical)، والتمثيلي (representation)، والقياسي (measurement)، والتجميعي (aggregation)، والتقييمي (evaluation)** (والنشر (deployment)). وتدابير التخفيف (mitigations) هي **المعالجة المسبقة** (pre-processing) (إصلاح البيانات)، أو **المعالجة أثناء التدريب** (in-processing) (تقييد التعلّم)، أو **المعالجة اللاحقة** (post-processing) (تعديل المخرجات (outputs))، ولكلٍّ منها حدود قانونية وعملية.
- **معضلة الفئات الخاصة** (special-categories dilemma): لكي تختبر وجود التمييز (discrimination)، كثيرًا ما تحتاج إلى البيانات الحساسة (sensitive data) ذاتها التي يُطلب منك تجنّبها. ويمنح قانون الذكاء الاصطناعي الأوروبي (EU AI Act) مقدّمي الأنظمة عالية المخاطر (high-risk providers) إذنًا **ضيقًا ومشروطًا (narrow, conditional)** بمعالجة الفئات الخاصة (special-category processing) لاكتشاف التحيّز وتصحيحه (for bias detection and correction).
- الفخ الأكبر (Biggest trap): "نحن لا نجمع العرق (ethnicity) أو الجنس (sex)، إذن لا يمكن لنموذجنا أن يميّز." المتغيرات البديلة (proxies) يمكن أن تميّز مع ذلك، ومن دون البيانات لا تستطيع رؤية ذلك.

## 🧭 لماذا يهم (Why it matters)
تشير التقارير إلى أن Amazon تخلّت نحو عام 2018 عن نموذج توظيف تجريبي (experimental recruiting model) بعد أن تبيّن أنه يعاقب السير الذاتية (CVs) التي تشير إلى أن المتقدم (applicant) امرأة. لقد تعلّم من سير ذاتية لعقد (contract) كامل من مجموعة متقدمين يهيمن عليها الذكور. لم يكتب أحد في الشيفرة "فضّل الرجال". البيانات حملت التاريخ، والنموذج (model) تعلّمه. وفي فضيحة إعانات رعاية الأطفال الهولندية (*toeslagenaffaire*)، أسهم نهج لتصنيف المخاطر (risk-classification approach) يأخذ الجنسية (nationality) في الحسبان في معاملة آلاف الأسر خطأً على أنها محتالة، مع عواقب مدمّرة، واستقالة حكومة.

يُدرَّب نموذج الائتمان (credit model) في بنك نجم (Najm Bank) على طلبات بتّ فيها مكتتبو (underwriters) بنك نجم أنفسهم بين 2017 و2024. ولا تضم البيانات سوى 11% من المتقدمات الإناث (female applicants)، وقليلًا من المتقدمين (applicants) دون 25 عامًا، ونتائج (سُدّد أو تعثّر) فقط للأشخاص الذين *وُوفق* عليهم، لأن المتقدمين المرفوضين (declined applicants) لم يحصلوا على قرض أصلًا، فلا أحد يعرف هل كانوا سيسددون. والجنسية (nationality) مسجّلة. والجنس (sex) مسجّل لأغراض اعرف عميلك (KYC). والعرق (ethnicity) غير مسجّل إطلاقًا. تسأل دانة ليلى هل ينبغي لها حذف حقل الجنس "احتياطًا". فتفاجئها إجابة ليلى: "احذفيه كمُدخل للنموذج (model)، نعم، على الأرجح. لكننا قد نحتاج إليه *لاختبار (testing)* ما إذا كان النموذج عادلًا (fair)."

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**أبعاد جودة البيانات (Data quality dimensions).** هذه أبعاد شائعة. وتضفي عليها معايير ISO/IEC (ومنها سلسلة ISO/IEC 5259 بشأن جودة البيانات (data quality) للتحليلات (analytics) وتعلّم الآلة (machine learning)) وأطر إدارة البيانات (data-management frameworks) طابعًا رسميًا.

| البعد (Dimension) | السؤال | مثال من بنك نجم (Najm example) |
|---|---|---|
| **الدقة (accuracy)** | هل تعكس القيمة الواقع؟ | حقل الدخل يصرّح به المتقدم (applicant) ولا يُتحقق منه أبدًا |
| **الاكتمال (completeness)** | هل القيم المطلوبة موجودة؟ | 18% من قيم مدة العمل (employment length) مفقودة، ومعظمها للعاملين لحسابهم الخاص (self-employed) |
| **الاتساق (consistency)** | هل تتفق القيم عبر الأنظمة وعبر الزمن؟ | نظاما الإمارات وقطر يرمّزان "عدد الأشهر في العنوان" بشكل مختلف |
| **الحداثة (timeliness)** | هل البيانات حديثة بما يكفي؟ | بيانات مكتب الائتمان (Bureau) تُحدَّث كل ربع سنة، والقرارات يومية |
| **الصلاحية (validity)** | هل تتبع الصيغ والقواعد؟ | تواريخ ميلاد في المستقبل |
| **التفرّد (uniqueness)** | هل توجد تكرارات؟ | المتقدم (applicant) نفسه الذي يعيد التقديم يظهر كأشخاص منفصلين |
| **الصلة / الملاءمة للغرض (Relevance / fitness for purpose)** | هل هي البيانات المناسبة *لهذا* الاستخدام؟ | بيانات ما قبل 2020 السابقة لتغيير كبير في المنتج |

لا يُحكم على الجودة (quality) في المطلق أبدًا. فالسؤال دائمًا: "هل هي جيدة بما يكفي لهذا الغرض (purpose)، ولهؤلاء الأشخاص، وفي فئة المخاطر (risk tier) هذه؟" ويطلب قانون الذكاء الاصطناعي الأوروبي (EU AI Act) أن تكون بيانات التدريب والتحقق والاختبار (training, validation and testing data) للأنظمة عالية المخاطر (high-risk systems) ذات صلة (relevant)، وتمثيلية (representative) بما يكفي، وخالية من الأخطاء (free of errors) ومكتملة إلى أقصى حد ممكن في ضوء الغرض المقصود (intended purpose). ويطلب أيضًا أن تكون لها الخصائص الإحصائية (statistical properties) المناسبة للأشخاص أو المجموعات (groups) التي يُقصد استخدام النظام عليها.

**التمثيلية وأخذ العينات (Representativeness and sampling).** تكون مجموعة البيانات (dataset) *تمثيلية (representative)* عندما يعكس تكوينها المجتمع وظروف الاستخدام. ومن المشكلات *نقص التمثيل* (under-representation) (أمثلة قليلة لمجموعة ما، فيتعلّم النموذج (model) أنماطها بشكل ضعيف)، و*فجوات التغطية* (coverage gaps) (غياب البيانات تمامًا لبعض الظروف، مثل الركود)، و*تحيّز الاختيار* (selection bias) (من ينتهي به الأمر في البيانات ليس عشوائيًا). وفي الائتمان مشكلة اختيار كلاسيكية (classic selection problem) تُسمى **استدلال المرفوضين** (reject inference): النتائج موجودة فقط للمتقدمين الموافق عليهم (approved applicants)، فيتعلّم النموذج من مجتمع اختارته السياسة القديمة (old policy). ومن استراتيجيات أخذ العينات (sampling) أخذ العينات الطبقية (stratified sampling) (ضمان ظهور كل مجموعة بنسبتها أو فوق حد أدنى)، والإفراط في تمثيل المجموعات الصغيرة (oversampling) عند التدريب، والعينات خارج الفترة الزمنية (out-of-time samples) للاختبار (testing).

**جودة الوسم (Labelling quality).** تتعلّم النماذج الخاضعة للإشراف (Supervised models) من الوسوم (labels): "تعثّر"، "احتيال"، "تعيين جيد"، "مسيء". وقد تكون الوسوم خاطئة أو غير متسقة أو متحيّزة. والممارسة الجيدة هي:
- **إرشادات المُوسِّمين (Annotator guidance):** تعريفات مكتوبة، وأمثلة محلولة (worked examples)، وحالات حدّية (edge cases)، وما يُفعل عند عدم اليقين.
- **مُوسِّمون مؤهَّلون (Qualified annotators):** خبراء في المجال (domain experts) حيث يلزم (محللو ائتمان (credit analysts)، لا جمهور عام (generic crowd)، لتقييم (evaluation) جودة المذكرات)، مع كفاءة لغوية وثقافية. ويشمل ذلك في بنك نجم اللغة العربية.
- **ضبط الجودة (Quality control):** عدة مُوسِّمين (annotators) على عينة، ومقاييس **الاتفاق بين المُوسِّمين** (inter-annotator agreement) (مثل معامل كابا لكوهين (Cohen's kappa)، الذي يصحّح الاتفاق من أثر الصدفة)، والفصل في حالات الخلاف (adjudication of disagreements)، وعناصر فحص مرجعية (gold-standard).
- **الوعي بمصدر الوسم (Label-source awareness):** عندما يكون الوسم (label) *قرارًا بشريًا سابقًا (past human decision)* ("عُيّن"، "وُوفق عليه"، "أُشير إليه")، فإنه يُرمّز تحيّزات (biases) صاحب القرار. وعندما يكون *نتيجة* ("تعثّر")، فقد يعكس مع ذلك معاملة غير متساوية (unequal treatment)، مثل إجراءات تحصيل (collections) أشد قسوة مع بعض المجموعات (groups).
- **رفاه المُوسِّمين (Annotator welfare)** في الإشراف على المحتوى (content moderation) ووسم اختبارات الفريق الأحمر (red-team labelling)، إذ قد يعرّض ذلك العاملين لمواد ضارة.

### 🟡 التعمق أكثر (Going deeper)

**من أين يأتي التحيّز (Where bias comes from).** يسمّي إطار واسع الاستخدام (Suresh وGuttag) مصادر (sources) التحيّز (bias) على طول خط المعالجة (pipeline). ويصنّف NIST SP 1270 تحيّز الذكاء الاصطناعي (AI bias) في فئات *نظامية* (systemic) و*إحصائية/حسابية* (statistical/computational) و*إدراكية بشرية* (human-cognitive). وكلا المنظورين مفيد.

| نوع التحيّز (Bias type) | ما يحدث | مثال من بنك نجم (Najm example) |
|---|---|---|
| **التاريخي (Historical)** | العالم الذي تعكسه البيانات كان غير متكافئ أصلًا؛ وحتى القياس المثالي (perfect measurement) يعيد إنتاجه | عُرضت على النساء تاريخيًا حدود ائتمان أصغر، فصار سجلهن الائتماني أقل |
| **التمثيلي (Representation)** | بعض المجموعات (groups) ممثَّلة بعينات أقل أو غائبة | 11% متقدمات إناث (female applicants)؛ عدد قليل جدًا دون 25 عامًا |
| **القياسي (Measurement)** | الخصائص (features) أو الوسوم (labels) بدائل ضعيفة أو غير متكافئة لما يهمك | "التعثّر (default)" يُسجَّل بشكل مختلف حسب الفرع؛ الدخل يُتحقق منه للموظفين بأجر لا للعاملين لحسابهم الخاص (self-employed) |
| **التجميعي (Aggregation)** | نموذج (model) واحد لمجموعات (groups) تتصرف بشكل مختلف | نموذج (model) واحد للمتقدمين (applicants) المغتربين (expatriate) والمواطنين (national)، مع أن سجلاتهم الائتمانية تختلف بنيويًا |
| **التقييمي (Evaluation)** | بيانات الاختبار (test data) أو المقاييس المرجعية لا تمثّل مجتمع الاستخدام؛ ولا يُبلَّغ إلا عن المقاييس الإجمالية (aggregate metrics) | قيمة AUC إجمالية مرتفعة (High overall AUC) تخفي أداءً ضعيفًا مع المتقدمين الشباب (young applicants) |
| **النشر (deployment)** | يُستخدم النظام في سياق أو بطريقة لم يُصمَّم لها | إعادة استخدام نموذج (model) الأفراد لأصحاب المنشآت الصغيرة والمتوسطة (SMEs) |

**المتغيرات البديلة (Proxies).** نادرًا ما تؤدي إزالة سمة محمية إلى إزالة تأثيرها. فالرمز البريدي (postcode)، وجهة العمل (employer)، والاسم الأول (first name)، وأنماط التسوّق (shopping patterns)، وإعدادات اللغة (language settings)، وحتى نوع الجهاز (device type) قد ترتبط بالجنسية (nationality) أو العرق (ethnicity) أو الجنس (sex). ويستطيع النموذج (model) إعادة بناء السمة (attribute) منها. اختبر وجود المتغيرات البديلة: تحقّق من مدى قدرة الخصائص (features) المتبقية على التنبؤ بالسمة المحمية (protected attribute)، واختبر النتائج حسب المجموعة (by group).

**التخفيف: ثلاث عائلات (Mitigation: three families).**

| المرحلة | التقنيات (مفاهيميًا) (Techniques, conceptual) | نقاط القوة (Strengths) | الحدود والمخاطر (Limits and risks) |
|---|---|---|---|
| **المعالجة المسبقة (pre-processing)** (البيانات) | جمع بيانات أفضل؛ إعادة الترجيح (reweighting) أو إعادة أخذ العينات (resampling) للمجموعات (groups) ناقصة التمثيل (under-represented)؛ إصلاح الوسوم (labels) المتحيّزة أو إعادة وسمها (relabel)؛ إزالة الخصائص البديلة (proxy features) أو تحويلها | تعالج الأسباب الجذرية (root causes)؛ لا تعتمد على نوع النموذج (model) | قد لا تزيل المتغيرات البديلة (proxies) المتعلَّمة؛ إعادة الوسم (relabelling) تحتاج إلى تبرير |
| **المعالجة أثناء التدريب (in-processing)** (التدريب) | إضافة قيود أو عقوبات للعدالة (fairness constraints or penalties) إلى هدف التعلّم (learning objective)؛ إزالة التحيّز بالخصومة (adversarial debiasing) (معاقبة النموذج (model) إذا استطاع نموذج ثانٍ تخمين السمة المحمية (protected attribute) من مخرجاته) | تحسّن المفاضلة (trade-off) مباشرة | تحتاج إلى بيانات السمة المحمية (protected attribute) أثناء التدريب؛ قد تقلل الدقة (accuracy)؛ أعقد في المصادقة (validation) |
| **المعالجة اللاحقة (post-processing)** (المخرجات (outputs)) | تعديل العتبات (thresholds) أو الدرجات لكل مجموعة لمساواة مقياس مختار؛ التصنيف بخيار الرفض (reject-option classification) قرب الحد الفاصل (boundary) | بسيطة؛ تعمل مع النماذج (models) المشتراة | استخدام السمات المحمية (protected attributes) وقت القرار قد يكون **معاملة متفاوتة غير مشروعة** (unlawful disparate treatment) في بعض الولايات القضائية (مثل قانون الائتمان الأمريكي (US credit law))؛ وقد تنقل الضرر (harm) فقط |

كثيرًا ما يكون أفضل تخفيف **ليس** تقنية. فقد يعني تغيير الهدف (التنبؤ بالقدرة على السداد، لا "التشابه مع العملاء الموافق عليهم (approved) سابقًا")، أو جمع بيانات من المجموعات (groups) ناقصة التمثيل (under-represented)، أو تضييق الغرض المقصود (intended purpose)، أو إضافة مراجعة بشرية (human review) للمجموعات التي يضعف فيها النموذج (model).

### 🔴 نظرة الخبير (Expert view)

**معضلة الفئات الخاصة (special-categories dilemma).** لقياس ما إذا كان النموذج (model) يعامل المجموعات العرقية (ethnic groups) بشكل مختلف، تحتاج عمومًا إلى معرفة عرق المتقدمين (applicants). لكن GDPR المادة 9 (Art. 9) تحظر معالجة الفئات الخاصة (الأصل العرقي أو الإثني (racial or ethnic origin)، والآراء السياسية (political opinions)، والمعتقدات الدينية (religious beliefs)، وعضوية النقابات (trade-union membership)، والبيانات الجينية (genetic)، والبيومترية لأغراض التعرّف (biometric for identification)، والصحة، والحياة الجنسية أو التوجه الجنسي (sex life or sexual orientation)) ما لم ينطبق شرط محدد، والشروط لا تشمل بشكل واضح "اختبار العدالة (fairness testing)". والمؤسسات التي "لا تجمع" هذه البيانات تكون في الغالب *عمياء* عن التمييز (discrimination) لا خالية منه. ولاحظ أن الجنس (sex) والجنسية (nationality) ليسا من الفئات الخاصة (special categories) في المادة 9، وإن كانا أساسين محميين (protected grounds) في قانون مكافحة التمييز (non-discrimination law). ولهذا يستطيع بنك نجم استخدامهما في الاختبار (testing) بأساس قانوني (lawful basis) عادي مع ضمانات (safeguards).

**الإذن الضيق في قانون الذكاء الاصطناعي الأوروبي (The EU AI Act's narrow permission).** بالنسبة إلى أنظمة الذكاء الاصطناعي (AI systems) **عالية المخاطر (high-risk)**، تسمح مادة حوكمة البيانات (data governance) في قانون الذكاء الاصطناعي (AI) لمقدّمي الأنظمة (providers)، *استثناءً*، بمعالجة الفئات الخاصة من البيانات الشخصية (special categories of personal data) **بالقدر الضروري حصرًا (to the extent strictly necessary)** لـ **اكتشاف التحيّز وتصحيحه (bias detection and correction)**. ويقوم هذا الإذن إلى جانب GDPR أساسًا لتلك المعالجة (that processing)، مع مراعاة الضمانات المناسبة (appropriate safeguards). والشروط صارمة. وباختصار:
- لا يمكن اكتشاف التحيّز وتصحيحه (bias detection and correction) بفعالية باستخدام بيانات أخرى، بما فيها البيانات الاصطناعية (synthetic data) أو المجهّلة (anonymised)؛
- تخضع بيانات الفئات الخاصة (special-category data) لقيود تقنية على إعادة الاستخدام، ولأحدث تدابير الأمن والحفاظ على الخصوصية (state-of-the-art security and privacy-preserving measures)، بما فيها الترميز المستعار (pseudonymisation)؛
- ضوابط وصول وتوثيق صارمة (strict access controls and documentation)، مع قصر الوصول على أشخاص مخوَّلين (authorised persons) ملزَمين بواجبات السرية (confidentiality duties)؛
- لا تُنقل البيانات إلى أطراف أخرى ولا تصل إليها أطراف أخرى؛
- تُحذف بمجرد تصحيح التحيّز (bias) أو انتهاء فترة الاحتفاظ (retention period)، أيهما أسبق؛
- توضّح سجلات أنشطة المعالجة (records of processing activities) لماذا كانت المعالجة (processing) ضرورية حصرًا (strictly necessary) ولماذا لم يكن ممكنًا تحقيق الهدف ببيانات أخرى.

صِفه بعناية: إنه **ليس** ترخيصًا عامًا (general licence) لجمع البيانات الحساسة (sensitive data). فهو ينطبق على الأنظمة عالية المخاطر (high-risk systems)، ولاكتشاف التحيّز وتصحيحه (for bias detection and correction) فقط، حيث يكون ضروريًا حصرًا، ومع تلك الضمانات (safeguards). وخارج نطاق قانون الذكاء الاصطناعي (AI)، تظل المؤسسات بحاجة إلى شرط من المادة 9 (Art. 9). وكثيرًا ما تستخدم أيضًا بدائل تحافظ على الخصوصية (privacy-preserving alternatives): استبيانات تعريف ذاتي طوعية (voluntary self-identification surveys) تُجمع بشكل منفصل بموافقة صريحة (with explicit consent)، أو الاستدلال الإحصائي على الانتماء إلى المجموعة (statistical inference of group membership) لأغراض الاختبار *الإجمالي* (aggregate testing) فقط (وهو نفسه نشاط معالجة حساس (sensitive processing activity) يحتاج إلى تبريره الخاص)، أو أطراف ثالثة موثوقة (trusted third parties) تحتفظ بالبيانات الحساسة ولا تعيد إلا إحصاءات عدالة إجمالية (aggregate fairness statistics).

**زاوية دول الخليج (GCC angle).** يحمي PDPPL القطري وغيره من قوانين دول الخليج (GCC laws) الفئات الحساسة (sensitive categories) أيضًا، وقد تختلف شروطها. وتشترط سياسة بنك نجم الحصول على موافقة قانونية محلية (local legal sign-off) قبل استخدام أي بيانات حساسة (sensitive data) للاختبار (testing) في قطر أو الإمارات.

**الوسم والحقيقة المرجعية قرارات حوكمة (Labelling and ground truth are governance decisions).** اختيار "التعثّر (default) خلال 12 شهرًا" بدلًا من "التأخر 90 يومًا عن السداد (90 days past due) في أي وقت" يغيّر من يُحسب مقترضًا سيئًا (bad borrower)، وقد يغيّر نتائج المجموعات (groups). وهذا الاختيار مكانه سجل القرارات (decision log) (8.3)، مع فحص للعدالة (fairness)، لا أن يُدفن في دفتر ملاحظات (notebook).

**توثيق الجودة والتحيّز (Documenting quality and bias).** ينبغي أن تسجّل ورقة بيانات مجموعة البيانات (datasheet) (8.3) التكوين (composition) حسب المجموعات (groups) ذات الصلة، والفجوات المعروفة، وعملية الوسم (label) وإحصاءات الاتفاق (agreement statistics)، والتحيّزات المعروفة (known biases) وتدابير التخفيف المطبّقة (mitigations applied). ويتوقع ملف الملحق IV (Annex IV) للأنظمة عالية المخاطر (high-risk systems) أن يُوثَّق فحص التحيّزات المحتملة (possible biases)، والتدابير المتخذة لاكتشافها ومنعها والتخفيف (mitigation) منها.

## ⚖️ الأدوات التنظيمية (The instruments)
| الأداة | ما تشترطه أو توصي به (What it requires or recommends) | إشارة الامتحان (Exam cue) |
|---|---|---|
| **EU AI Act** — المادة 10(2)–(4) | بيانات التدريب والتحقق والاختبار (training, validation and testing data) للأنظمة عالية المخاطر (high-risk systems): ممارسات الحوكمة (governance)، وفحص التحيّزات المحتملة (possible biases)، والصلة، والتمثيلية (representativeness)، والخلو من الأخطاء (error-freeness) والاكتمال (completeness) إلى أقصى حد ممكن، والخصائص (features) الخاصة بالسياق (context) | جودة البيانات (data quality) متطلب قانوني للأنظمة عالية المخاطر (high-risk systems) |
| **EU AI Act** — المادة 10(5) | معالجة استثنائية للفئات الخاصة (special categories) بالقدر الضروري حصرًا (to the extent strictly necessary) لاكتشاف التحيّز وتصحيحه (for bias detection and correction)، مع ضمانات صارمة (strict safeguards) وحذف | إذن ضيق ومشروط (Narrow, conditional permission)، لا ترخيص عام (general licence) |
| **GDPR** — المادة 9 (Art. 9) | حظر معالجة الفئات الخاصة (special-category processing) ما لم ينطبق شرط مدرج | المعضلة وراء اختبار العدالة (fairness testing) |
| **NIST SP 1270** | تحديد التحيّز (bias) وإدارته: النظامي (systemic)، والإحصائي/الحسابي (statistical/computational)، والإدراكي البشري (human-cognitive) | التحيّز (bias) أكثر من مشكلة إحصائية |
| **ISO/IEC TR 24027** | تقرير تقني (Technical report) عن التحيّز (bias) في أنظمة الذكاء الاصطناعي (AI systems) واتخاذ القرار بمساعدة الذكاء الاصطناعي (AI-aided decision-making) | مفردات التحيّز القائمة على المعايير (Standards-based bias vocabulary) |
| **ISO/IEC 5259 series** | جودة البيانات (data quality) للتحليلات (analytics) وتعلّم الآلة (machine learning): نموذج الجودة (quality model)، والمقاييس، والإدارة | عائلة معايير جودة البيانات (Data quality standard family) |
| **ECOA / Regulation B** | يحظر التمييز الائتماني (credit discrimination) على أسس محمية (protected bases)؛ ويقيّد جمع الخصائص المحمية (protected characteristics) واستخدامها في قرارات الائتمان | عتبات المجموعات (Group thresholds) قد تكون معاملة متفاوتة (disparate treatment) |
| **NYC Local Law 144** | تدقيق مستقل للتحيّز (معدلات الاختيار (selection rates) ونسب الأثر (impact ratios) حسب فئات الجنس (sex) والعرق/الإثنية (race/ethnicity)) لأدوات قرارات التوظيف الآلية (automated employment decision tools) المستخدمة في مدينة نيويورك، مع إشعارات | مثال على اختبار التحيّز الإلزامي (mandated bias testing) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
**مراجعة جودة البيانات والتحيّز (Data Quality and Bias Review): مجموعة تدريب (training set) نموذج ائتمان الأفراد (retail credit model)** (يوقّع عليها (sign-off) دانة وعمر وليلى، مع سارة في قسم البيانات الحساسة (sensitive data)):

| الفحص | النتيجة | الإجراء | المسؤول |
|---|---|---|---|
| الاكتمال (completeness) | مدة العمل (employment length) مفقودة في 18%، وتتركز في العاملين لحسابهم الخاص (self-employed) | إضافة مؤشر "يعمل لحسابه الخاص (self-employed)"؛ عدم تعويض القيم المفقودة بقيمة افتراضية؛ اختبار (testing) الأداء (performance) لهذه الشريحة (segment) | دانة |
| التمثيلية (representativeness) | 11% إناث؛ دون 25 عامًا 4% | إعادة الترجيح (reweighting) في التدريب؛ تحديد حد أدنى لحجم عينة الاختبار (testing) لكل مجموعة؛ الإشارة إلى القيد في بطاقة النموذج (model card) | دانة |
| الاختيار / استدلال المرفوضين (Selection / reject inference) | النتائج متاحة فقط للمتقدمين الموافق عليهم (approved applicants) | التوثيق (documentation)؛ استخدام طريقة محافظة لاستدلال المرفوضين (reject inference)؛ رصد حالات تجاوز القرار في مجتمع المرفوضين (declined-population) | دانة / خالد |
| تعريف الوسم (Label definition) | "التعثّر (default)" مرمَّز بشكل مختلف في الإمارات وقطر | التوحيد على التأخر 90 يومًا عن السداد (90 days past due) خلال 12 شهرًا؛ إعادة اشتقاق الوسوم (re-derive labels) | عمر |
| اختبار المتغيرات البديلة (Proxy test) | يمكن التنبؤ بالجنسية (nationality) من جهة العمل (employer) + الرمز البريدي (postcode) | إزالة اسم جهة العمل (employer name)؛ اختبار (testing) النتائج حسب مجموعة الجنسية (nationality group) | دانة |
| البيانات الحساسة (sensitive data) للاختبار (testing) | الجنس (sex) والجنسية (nationality) محفوظان لأغراض اعرف عميلك (KYC)؛ لا يوجد عرق | استخدام الجنس (sex) والجنسية (nationality) لاختبار العدالة الإجمالي (aggregate fairness testing) فقط، بأساس موثّق وضوابط (controls) وصول؛ لا يُقترح حاليًا أي معالجة وفق المادة 10(5) | سارة / ليلى |
| اختيار التخفيف (Mitigation choice) | نسبة معدل الموافقة (approval-rate ratio) للنساء 0.72 في خط الأساس (baseline) | قيد أثناء التدريب (انظر DL-014)؛ لا عتبات خاصة بالمجموعات (مخاطر قانونية (legal risk)) | اللجنة (committee) |

## 🛠️ التمارين (Exercises)
- 🟢 اربط كل نوع من أنواع التحيّز (bias types) الستة بمثال واحد في نظام تعرفه (أو في أداة فرز السير الذاتية (CV-screening tool) لدى بنك نجم). *يكتمل عندما (Done when):* يذكر كل مثال في أي موضع من خط المعالجة (pipeline) يدخل التحيّز (bias).
- 🟡 اكتب دليلًا للمُوسِّمين (صفحة واحدة) لوسم (label) "جودة مذكرة الائتمان" لمجموعة تقييم المساعد (copilot evaluation set). *يكتمل عندما (Done when):* يتضمن تعريفات، وثلاثة أمثلة محلولة (worked examples)، وقاعدة لحالة "غير متأكد"، وفحصًا للاتفاق (agreement check).
- 🔴 يريد فريق بنك نجم في الاتحاد الأوروبي استنتاج عرق المتقدمين (applicants) من أسمائهم لاختبار (testing) نموذج الائتمان (credit model) بحثًا عن تحيّز عرقي (ethnic bias). قدّم المشورة بشأن مسار المادة 10(5) في قانون الذكاء الاصطناعي (AI) وGDPR، واقترح بديلًا أكثر أمانًا. *يكتمل عندما (Done when):* تطبّق كل شرط من شروط المادة 10(5) وتصل إلى توصية مع ضمانات (safeguards).

## ⚠️ أخطاء وفخاخ الامتحان (Mistakes and exam traps)
- **"العدالة عبر عدم المعرفة" (Fairness through unawareness).** حذف السمات المحمية (protected attributes) لا يوقف التمييز بالوكالة (proxy discrimination)، ويمنعك من قياسه.
- **معاملة المادة 10(5) كإذن عام (as a general permission).** إنها مقصورة على الأنظمة عالية المخاطر (high-risk systems)، واكتشاف التحيّز وتصحيحه (bias detection and correction)، والضرورة الحصرية (strict necessity)، والضمانات الصارمة (strict safeguards)، مع الحذف (deletion).
- **افتراض أن البيانات الضخمة (big data) تعني بيانات تمثيلية (representative data).** الحجم لا يصلح فجوات التغطية (coverage gaps) ولا تحيّز الاختيار (selection bias).
- **الثقة بالوسوم (labels).** القرارات التاريخية المستخدمة كوسوم تحمل التحيّز التاريخي (historical bias).
- **القفز مباشرة إلى المعالجة اللاحقة (post-processing).** العتبات الخاصة بالمجموعات (Group-specific thresholds) قد تكون غير مشروعة (unlawful). فكّر أولًا في إصلاح الأسباب الجذرية (root-cause fixes).
- **الإبلاغ عن الجودة الإجمالية (aggregate quality) فقط.** افحص الجودة (quality) والأداء (performance) حسب المجموعة (by group) والشريحة (segment).

## 🧾 الخلاصة (Recap)
- احكم على الجودة (quality) بالملاءمة للغرض (by fitness for purpose) عبر الدقة (accuracy) والاكتمال (completeness) والاتساق (consistency) والحداثة (timeliness) والصلاحية (validity) والتفرّد (uniqueness).
- التمثيلية وأخذ العينات (Representativeness and sampling) واستدلال المرفوضين (reject inference) تحدد من يتعلّم النموذج (model) عنهم.
- جودة الوسوم (label quality) تحتاج إلى إرشادات، ومُوسِّمين مؤهَّلين (qualified annotators)، وفحوص للاتفاق (agreement checks)، ووعي بالتحيّز التاريخي (historical bias).
- يدخل التحيّز (bias) في كل مرحلة (التاريخي (Historical)، والتمثيلي (Representation)، والقياسي (Measurement)، والتجميعي (Aggregation)، والتقييمي (Evaluation)، والنشر (deployment)). خفّفه بالمعالجة المسبقة (pre-processing) أو أثناء التدريب أو اللاحقة ضمن الحدود القانونية.
- المادة 10(5) من قانون الذكاء الاصطناعي (AI) استثناء ضيق ومحاط بالضمانات (safeguards) لاكتشاف التحيّز (to detect bias) في الأنظمة عالية المخاطر (high-risk systems).

## ✍️ اختبر نفسك (Check yourself)

**1. دُرّب نموذج الائتمان (credit model) في بنك نجم فقط على المتقدمين (applicants) الذين وافقت عليهم السياسة القديمة (old policy). أي مشكلة يصفها هذا بالشكل الأكثر مباشرة؟**

- A. التحيّز التجميعي (Aggregation bias)
- B. تحيّز الاختيار (مشكلة استدلال المرفوضين (reject inference)): النتائج مفقودة للمتقدمين (applicants) الذين رفضتهم السياسة القديمة (old policy)
- C. استخراج النموذج (model extraction)
- D. ضوضاء الوسوم (label noise) من المُوسِّمين (annotators)

<details><summary>الإجابة (Answer)</summary>

**B.** مجتمع البيانات اختارته سياسة القرار السابقة (previous decision policy). أما التحيّز التجميعي (A) فيتعلق بنموذج (model) واحد لمجموعات (groups) مختلفة. (🟢 الأساسيات (The essentials).)

</details>

**2. يريد مقدّم (provider) نظام ذكاء اصطناعي (AI system) عالي المخاطر (high-risk) معالجة بيانات العرق (ethnicity) لاكتشاف التحيّز (to detect bias). بموجب قانون الذكاء الاصطناعي الأوروبي (EU AI Act)، أي عبارة صحيحة؟**

- A. يجوز له ذلك استثناءً بالقدر الضروري حصرًا (to the extent strictly necessary) لاكتشاف التحيّز وتصحيحه (for bias detection and correction)، مع مراعاة ضمانات صارمة (strict safeguards)، منها ألا تكون البيانات الأخرى، كالبيانات الاصطناعية (synthetic data) أو المجهّلة (anonymised)، كافية، والحذف (deletion) بعد ذلك
- B. يجوز له ذلك بحرية لأن قانون الذكاء الاصطناعي (AI) يعلو على GDPR
- C. هذا محظور (prohibited) دائمًا
- D. يجوز له ذلك لأي نظام ذكاء اصطناعي (AI system)، عالي المخاطر (high-risk) أو لا

<details><summary>الإجابة (Answer)</summary>

**A.** المادة 10(5) ضيقة ومشروطة. وB وD يبالغان فيها، وC يتجاهلها. (🔴 نظرة الخبير (Expert view).)

</details>

**3. تزيل دانة "الجنس (sex)" من مدخلات نموذج الائتمان (credit model)، لكن معدلات الموافقة (approval rates) للنساء تظل أقل بكثير. ما التفسير (explanation) الأرجح؟**

- A. النموذج (model) عادل (fair) تمامًا والنساء أكثر خطورة
- B. قيم SHAP خاطئة
- C. إزالة خاصية (feature) تزيد التحيّز (bias) دائمًا
- D. خصائص أخرى تعمل كمتغيرات بديلة (as proxies) للجنس (sex)، وقد يكون التحيّز التاريخي (historical bias) موجودًا في الوسوم (labels)

<details><summary>الإجابة (Answer)</summary>

**D.** المتغيرات البديلة (proxies) والوسوم التاريخية (historical labels) تُبقي الأثر (impact) حيًا بعد إزالة السمة (attribute). أما A فيقفز إلى استنتاج دون اختبار (testing) معدلات الخطأ (error rates) والوسوم (labels). (🟡 التعمق أكثر (Going deeper).)

</details>

**4. أيٌّ مما يلي مثال على تخفيف التحيّز (bias mitigation) أثناء التدريب؟**

- A. إعادة ترجيح (reweighting) أمثلة التدريب من المجموعات (groups) ناقصة التمثيل (under-represented)
- B. إضافة قيد أو عقوبة للعدالة (fairness constraint or penalty) إلى هدف تدريب النموذج (model's training objective)
- C. تحديد عتبات درجات مختلفة لكل مجموعة (different score thresholds per group) بعد التدريب
- D. جمع مزيد من البيانات عن المتقدمين الشباب (young applicants)

<details><summary>الإجابة (Answer)</summary>

**B.** المعالجة أثناء التدريب (in-processing) تغيّر التعلّم نفسه. أما A وD فمعالجة مسبقة (pre-processing). وC معالجة لاحقة (post-processing). (🟡 التعمق أكثر (Going deeper).)

</details>

**5. في مشروع وسم (labelling project) لبناء (build) مجموعة تقييم المساعد (copilot evaluation set)، أي ضابط (control) يحسّن جودة الوسوم (label quality) أكثر من غيره؟**

- A. إرشادات مكتوبة مع أمثلة محلولة (worked examples) وحالات حدّية (edge cases)، ومُوسِّمون مؤهَّلون (Qualified annotators)، وقياس الاتفاق بين المُوسِّمين (inter-annotator agreement) مع الفصل في الخلافات (adjudication)
- B. استخدام أرخص منصة جمهور (crowd platform) متاحة
- C. ترك كل مُوسِّم (annotator) يعرّف "المذكرة الجيدة" بنفسه
- D. وسم الحالات السهلة فقط (Labelling only the easy cases)

<details><summary>الإجابة (Answer)</summary>

**A.** الإرشادات والكفاءة (competence) وقياس الاتفاق (agreement measurement) والفصل في الخلافات (adjudication) هي الضوابط (controls) الأساسية لجودة الوسوم (label quality). ووسم الحالات السهلة فقط (D) يحيّز مجموعة التقييم (evaluation set). (🟢 الأساسيات (The essentials).)

</details>

## 📚 المراجع (References)
- EU AI Act، اللائحة (EU) 2024/1689 (المادة 10) — https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- GDPR، اللائحة (EU) 2016/679 (المادة 9 (Art. 9)) — https://eur-lex.europa.eu/eli/reg/2016/679/oj
- NIST SP 1270، نحو معيار لتحديد التحيّز في الذكاء الاصطناعي وإدارته (Towards a Standard for Identifying and Managing Bias in Artificial Intelligence) — https://doi.org/10.6028/NIST.SP.1270
- ISO/IEC JTC 1/SC 42 (ISO/IEC TR 24027، سلسلة ISO/IEC 5259) — https://www.iso.org/committee/6794475.html
- مكتب الحماية المالية للمستهلك الأمريكي (ECOA/Regulation B) — https://www.consumerfinance.gov
- إدارة حماية المستهلك والعامل في مدينة نيويورك (قانون أدوات قرارات التوظيف الآلية (AEDT law)، AEDT) — https://www.nyc.gov/site/dca/index.page
- IAPP، مجال المعرفة (BoK) لشهادة AIGP — https://iapp.org/certify/aigp/

---

# 9.3 — الاختبار والتقييم والمصادقة واختبار الفريق الأحمر (Testing, evaluation, validation and red-teaming)
*المستوى: 🔴 متقدم (Level: Advanced)* · *المتطلبات: 9.2، 8.2 (Prerequisites)* · *مجال المعرفة (BoK): III.B*

## ⚡ الدرس في دقيقة (In 60 seconds)
- **الاختبار والتقييم والتحقق والمصادقة (TEVV)** هو الطريقة التي تحصل بها على دليل (evidence) أن النظام يعمل كما هو مقصود، للأشخاص الذين يؤثر فيهم، وتحت الظروف التي سيواجهها. *التحقق* (verification): هل بنيناه بشكل صحيح (وفق المواصفات (to spec))؟ *المصادقة* (validation): هل بنينا الشيء الصحيح (الملائم للاستخدام الحقيقي)؟
- قسّم البيانات إلى **مجموعات تدريب وتحقق واختبار** (training, validation and test sets)، واحترس من **التسرّب** (leakage)، أي عندما تتسلل إلى التدريب أو الاختبار (testing) معلومات لن تكون لدى النموذج (model) وقت اتخاذ القرار، فتبدو النتائج أفضل من حقيقتها.
- اختر **مقاييس الأداء** (performance metrics) المناسبة للاستخدام: الدقة (accuracy) كثيرًا ما تكون مضلِّلة. استخدم الضبط (precision) والاستدعاء (recall) وAUC والمعايرة (calibration) بحسب ما يتطلبه الاستخدام. وأبلغ عنها **حسب المجموعة (by group)**.
- **مقاييس العدالة** (fairness metrics) (التكافؤ الديموغرافي (demographic parity)، وتكافؤ الاحتمالات (equalised odds)، والتكافؤ التنبؤي (predictive parity)) تقيس أشياء مختلفة و**لا يمكن استيفاؤها كلها** عندما تختلف المعدلات الأساسية (base rates). والاختيار بينها قرار حوكمة (governance).
- **اختبار الفريق الأحمر** (red-teaming)، واختبارات الإجهاد (stress tests)، والتقييم البشري (human evaluation)، و**المصادقة المستقلة** (independent validation) ("التحدي الفعّال" (effective challenge) في إدارة مخاطر النماذج (model risk management)) تكمل الصورة. **تُحدَّد معايير القبول (acceptance criteria) قبل الاختبار**، ويتبع الاعتماد النهائي (sign-off) الفئة (tier).
- الفخ الأكبر (Biggest trap): تحديد درجة النجاح (pass mark) بعد رؤية النتائج.

## 🧭 لماذا يهم (Why it matters)
في عام 2016 حلّلت ProPublica أداة تقدير خطر العودة إلى الإجرام COMPAS، وأفادت بأن المتهمين السود الذين لم يعودوا إلى الإجرام كانوا أكثر عرضة للتصنيف (classification) بأنهم عالو الخطورة (high-risk) من المتهمين البيض الذين لم يعودوا إلى الإجرام. وهذه فجوة في *معدلات الإيجابيات الكاذبة* (false positive rates). وردّ المطوّر بأن الدرجات كانت *تنبؤية* بالقدر نفسه للمجموعتين: فالدرجة (score) الواحدة تعني تقريبًا الاحتمال نفسه للعودة إلى الإجرام. وكان كلا الطرفين يقيس شيئًا حقيقيًا. ثم أثبت الباحثون أنه عندما تختلف المعدلات الأساسية (base rates) بين المجموعات (groups)، لا يمكن لدرجةٍ عمومًا أن تستوفي الخاصيتين معًا. وعلّم هذا الجدل مجالًا كاملًا أن سؤال "هل هو عادل (fair)؟" لا جواب له حتى تحدد *أي عدالة*، و*لمن*، و*من قرّر*.

نموذج الائتمان (credit model) في بنك نجم (Najm Bank) جاهز للاختبار (testing). تُبلغ دانة عن دقة إجمالية (overall accuracy) قدرها 94% وتريد الإطلاق (launch). تطرح ليلى أربعة أسئلة. كم ستكون الدقة (accuracy) لو تنبأ النموذج (model) بـ "لا تعثّر" للجميع؟ كيف يؤدي مع النساء والمتقدمين الشباب (young applicants) والعاملين لحسابهم الخاص (self-employed)؟ من، غير فريق دانة، راجع العمل؟ وما معايير النجاح (pass criteria) التي وُضعت *قبل* إجراء الاختبارات (tests)؟ الإجابات تحدد هل يصل النموذج إلى مكتتبي (underwriters) خالد.

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**مفردات TEVV (TEVV vocabulary).** يستخدم NIST مصطلح "TEVV" في أنحاء وظيفة (function) **القياس** (Measure) في إطار AI RMF.
- **الاختبار (Testing):** تشغيل النظام على مدخلات محددة لملاحظة سلوكه.
- **التقييم (Evaluation):** الحكم على النتائج مقابل المقاييس والمعايير.
- **التحقق (Verification):** تأكيد أن النظام يستوفي متطلباته المحددة (قائمة المتطلبات (requirement list) في 8.2).
- **المصادقة (Validation):** تأكيد أنه ملائم لغرضه المقصود (fit for its intended purpose) في سياقه الحقيقي، وغالبًا ما يقوم بها شخص مستقل عن البنّائين (builders).

**تقسيم البيانات والتسرّب (Data splits and leakage).**
- **مجموعة التدريب (training set):** البيانات التي يتعلّم منها النموذج (model).
- **مجموعة التحقق (validation set):** تُستخدم أثناء التطوير (development) لضبط الإعدادات والاختيار بين النماذج (models).
- **مجموعة الاختبار (المحجوزة، hold-out):** تُستخدم *مرة واحدة*، في النهاية، لتقدير الأداء (performance) في العالم الحقيقي. وإعادة استخدامها مرارًا تحوّلها إلى مجموعة تحقق (validation set) ثانية وتضخّم النتائج.
- في المشكلات المعتمدة على الزمن مثل الائتمان والاحتيال (fraud)، استخدم مجموعة اختبار (test set) **خارج الفترة الزمنية** (out-of-time) (مثل التدريب على 2017–2022 والاختبار (testing) على 2023–2024) حتى يحاكي الاختبار النشر (deployment) على متقدمين مستقبليين.

يحدث **التسرّب (leakage)** عندما يرى النموذج (model) أثناء التدريب أو الاختبار (testing) معلومات لن تكون لديه وقت القرار، أو عندما تتداخل بيانات الاختبار (test data) مع بيانات التدريب (training data). أمثلة في بنك نجم: خاصية (feature) "مؤشر التحصيل (collections flag)" التي لا تُضبط إلا *بعد* التعثّر (default)؛ والعميل نفسه يظهر في مجموعتي التدريب والاختبار (training and test sets) معًا؛ ونموذج ذكاء اصطناعي توليدي (GenAI) يُقيَّم على أسئلة ظهرت في بيانات تدريبه (**تلوّث المقاييس المرجعية**، benchmark contamination). والتسرّب ينتج درجات اختبار رائعة وأداءً فعليًا ضعيفًا.

**مقاييس الأداء، مفاهيميًا (Performance metrics, conceptually).** في التنبؤ بنعم/لا (تعثّر أم لا)، تقع كل حالة في واحد من أربعة مربعات: إيجابي صحيح (true positive)، وإيجابي كاذب (false positive)، وسلبي صحيح (true negative)، وسلبي كاذب (false negative).

| المقياس (Metric) | المعنى البسيط (Plain meaning) | متى يهم (When it matters) |
|---|---|---|
| **الدقة (Accuracy)** | نسبة التنبؤات الصحيحة من مجموع التنبؤات | مضلِّلة عندما تكون الفئات غير متوازنة |
| **الضبط (Precision)** | من بين الحالات المصنّفة إيجابية، كم منها إيجابي فعلًا | كلفة الإنذارات الكاذبة (تنبيهات احتيال (fraud alerts) تزعج العملاء) |
| **الاستدعاء (Recall) (الحساسية (sensitivity)، معدل الإيجابيات الصحيحة (true positive rate))** | من بين كل الإيجابيات الحقيقية، كم منها التُقط | كلفة الإخفاقات (احتيال فائت (missed fraud)؛ متقدمون جديرون ائتمانيًا فائتون) |
| **معدل الإيجابيات الكاذبة (False positive rate)** | من بين السلبيات الحقيقية، كم منها صُنّف خطأً | الضرر (harm) على الأشخاص المتهمين أو المرفوضين خطأً |
| **AUC (ROC)** | احتمال أن يرتّب النموذج (model) حالة إيجابية عشوائية فوق حالة سلبية عشوائية؛ 0.5 = رمي عملة (coin flip)، 1.0 = مثالي | جودة الترتيب (Ranking quality) بصرف النظر عن نقطة القطع (cut-off)؛ فرق الائتمان كثيرًا ما تُبلغ عن Gini = 2 × AUC − 1 |
| **المعايرة (Calibration)** | هل تطابق الاحتمالات المتنبأ بها (predicted probabilities) المعدلات الملاحظة (observed rates)؟ (من المتقدمين (applicants) الذين قُدّر احتمال تعثّرهم (PD) بـ 10%، يتعثّر نحو 10%) | التسعير (pricing)، والمخصصات (provisioning)، وأي استخدام يعتمد على الرقم نفسه |

**لماذا قد لا تعني دقة 94% شيئًا (Why 94% accuracy may mean nothing):** إذا تعثّر 6% من المتقدمين (applicants)، فإن نموذجًا (model) يتنبأ بـ "لا تعثّر" للجميع تكون دقته 94% وهو عديم الفائدة. أما الضبط والاستدعاء (precision and recall) وAUC والمعايرة (calibration) فتروي القصة الحقيقية.

### 🟡 التعمق أكثر (Going deeper)

**مقاييس العدالة (fairness metrics).** قارن بين المجموعات (لنقل A وB) من حيث:
- **التكافؤ الديموغرافي (الإحصائي) (Demographic (statistical) parity):** تساوي *معدلات الاختيار (selection rates)*، أي النسبة نفسها من الموافقات (Approvals) في كل مجموعة. وغالبًا ما يُعبَّر عنه بنسبة. وتعدّ "قاعدة الأربعة أخماس" (four-fifths rule) الأمريكية (من الإرشادات الموحدة لإجراءات اختيار الموظفين (Uniform Guidelines on Employee Selection Procedures) لعام 1978) نسبة معدلات اختيار (selection-rate ratio) أقل من 0.8 دليلًا على أثر سلبي (adverse impact). وهي قاعدة تقريبية (rule of thumb)، لا ملاذ آمن (safe harbour).
- **تكافؤ الفرص (Equal opportunity):** تساوي *معدلات الإيجابيات الصحيحة (true positive rates)*. أي يُوافَق على المؤهَّلين (qualified) أو الجديرين ائتمانيًا بالمعدل نفسه في كل مجموعة.
- **تكافؤ الاحتمالات (Equalised odds):** تساوي معدلات الإيجابيات الصحيحة (true positive rates) *و*تساوي معدلات الإيجابيات الكاذبة (false positive rates).
- **التكافؤ التنبؤي (Predictive parity):** تساوي *الضبط* (precision). أي من بين الموافق عليهم (approved)، تكون النسبة نفسها جديرة ائتمانيًا فعلًا في كل مجموعة. ويرتبط ارتباطًا وثيقًا بـ **المعايرة حسب المجموعة** (calibration by group).

**مثال محلول (worked example).** تضم مجموعة الاختبار (test set) في بنك نجم 1,000 متقدم من كل مجموعة من مجموعتين. و"جيد" يعني أن المتقدم (applicant) كان سيسدد.

| | المجموعة A (Group A) | المجموعة B (Group B) |
|---|---|---|
| جيد فعلًا (Truly good) | 600 | 400 |
| سيئ فعلًا (Truly bad) | 400 | 600 |
| وافق عليهم النموذج (Approved by model) | 540 (500 جيد، 40 سيئ) | 360 (330 جيد، 30 سيئ) |
| **معدل الموافقة (approval rate)** | 54% | 36% |
| **معدل الإيجابيات الصحيحة (true positive rate)** (الجيدون الذين وُوفق عليهم) | 500/600 = 83% | 330/400 = 83% (82.5%) |
| **معدل الإيجابيات الكاذبة (false positive rate)** (السيئون الذين وُوفق عليهم) | 40/400 = 10% | 30/600 = 5% |
| **الضبط** (الموافق عليهم (approved) الجيدون) | 500/540 = 93% | 330/360 = 92% |

اقرأه كمختص في الحوكمة (Read it as a governance professional):
- **التكافؤ الديموغرافي (demographic parity) لا يتحقق:** 36% ÷ 54% = 0.67، أي أقل من 0.8.
- **تكافؤ الفرص (equal opportunity) يتحقق:** يُوافَق على المتقدمين (applicants) الجيدين بالمعدل نفسه تقريبًا (83%) في المجموعتين.
- **التكافؤ التنبؤي (predictive parity) يتحقق تقريبًا:** 93% مقابل 92%.
- **تكافؤ الاحتمالات (equalised odds) لا يتحقق** من حيث معدلات الإيجابيات الكاذبة (10% مقابل 5%).

افترض الآن أن اللجنة (committee) طالبت بالتكافؤ الديموغرافي (demographic parity) بالموافقة (consent) على 540 شخصًا في المجموعة B (Group B). لا يتبقى إلا 70 متقدمًا جيدًا من المجموعة B دون موافقة (400 − 330)، لذا يجب أن يكون 110 على الأقل من الموافقات (Approvals) الإضافية البالغة 180 سيئين. وفي أفضل الأحوال ينخفض ضبط المجموعة B (Group B's precision) إلى 400/540 = 74% ويرتفع معدل الإيجابيات الكاذبة (false positive rate) فيها إلى 140/600 = 23%. وهذا يعني منح مزيد من عملاء المجموعة B قروضًا لا يستطيعون سدادها. وهذا أيضًا ضرر، ومسألة مخاطر سلوكية (conduct risk) للبنك. **هذه هي نتيجة الاستحالة (impossibility result) في صورة مصغّرة.** فعندما تختلف المعدلات الأساسية (60% مقابل 40% جيدون)، لا يمكنك عمومًا مساواة معدلات الاختيار (selection rates) ومعدلات الخطأ والضبط (error rates and precision) في الوقت نفسه، إلا مع متنبئ مثالي (perfect predictor). وقد أثبت Kleinberg وMullainathan وRaghavan (2016) وChouldechova (2017) صيغًا من ذلك إثباتًا رسميًا.

نقطتان إضافيتان في الحوكمة (governance). أولًا، قد تحمل وسوم (labels) "جيد فعلًا (Truly good)" نفسها تحيّزًا تاريخيًا (9.2). فإذا كانت المجموعة B (Group B) قد مُنحت تاريخيًا شروطًا أسوأ، فقد يعكس معدلها الأساسي (its base rate) جزئيًا المعاملة السابقة. ثانيًا، يعتمد المقياس (Metric) الذي تُعطى له الأولوية على الضرر (8.2) وعلى القانون. فبعض الولايات القضائية (jurisdictions) تختبر الأثر المتفاوت (disparate impact) على معدلات الاختيار (selection rates)، واستخدام السمات المحمية (protected attributes) لمساواة النتائج قد يكون هو نفسه غير مشروع (unlawful). **يجب أن تُوثَّق المفاضلة (trade-off) ويقبلها المالك (owner) المسؤول، لا أن يحسمها عالم بيانات بصمت.**

**اختبارات المتانة والإجهاد (Robustness and stress tests).** اختبر ما يتجاوز الحالة المتوسطة:
- **الحالات خارج التوزيع (Out-of-distribution) والحالات الحدّية (edge cases):** متقدمون بملفات ائتمانية شحيحة (thin-file)، وأنماط دخل غير معتادة، ومستندات بالعربية فقط، وحقول مفقودة.
- **اختبارات الاضطراب (Perturbation tests):** التغييرات الصغيرة في المدخلات (تقريب الدخل، إعادة ترتيب النص) لا ينبغي أن تقلب القرارات بشكل غير معقول.
- **اختبارات السيناريوهات والإجهاد (Scenario and stress tests):** ركود اقتصادي (economic downturn)، أو صدمة في أسعار الفائدة (interest-rate shock)، أو منتج جديد (new product). تفعل فرق الائتمان هذا بالفعل لنماذج رأس المال (capital models)، وينبغي اختبار (testing) نماذج (models) الذكاء الاصطناعي (AI) بالطريقة نفسها.
- **الاختبارات العدائية (Adversarial tests):** هل يستطيع محتال ضبط معاملاته للإفلات من الكشف؟ هل يستطيع مستند مصمَّم بعناية تضليل المساعد (copilot)؟
- **اختبارات التفسير (Explanation tests):** هل رموز الأسباب (reason codes) مستقرة وأمينة (8.2)؟

### 🔴 نظرة الخبير (Expert view)

**اختبار الفريق الأحمر (Red-teaming).** اختبار الفريق الأحمر اختبار عدائي منظَّم (structured adversarial testing): يحاول أشخاص (بمساعدة أدوات آلية أحيانًا) جعل النظام يفشل أو يسيء التصرف أو يسبب ضررًا، على نحو ما قد يفعل مهاجم أو مستخدم مهمل. وفي الذكاء الاصطناعي التوليدي (GenAI) يستكشف:
- حقن الأوامر (prompt injection) وكسر القيود (jailbreaks) (تجاوز تعليمات السلامة (safety instructions))؛
- تسرّب أوامر النظام (system prompts) أو البيانات السرية (confidential data) أو البيانات الشخصية (personal data)؛
- الحقائق والأرقام والاستشهادات (citations) الناتجة عن الهلوسة (hallucinated)؛
- المحتوى الضار أو المتحيّز أو المسيء، بما في ذلك بالعربية واللهجات؛
- الصلاحية المفرطة (excessive agency) (أدوات تفعل ما لا ينبغي لها)؛
- إساءة الاستخدام (misuse) خارج الغرض المقصود (intended purpose).

الفرق الحمراء (red-teams) الجيدة **متنوعة** (منظورات الأمن (security)، والمجال، واللغة، والمجتمعات المتأثرة)، و**محددة النطاق** (نموذج تهديد (threat model) وقواعد اشتباك (rules of engagement))، و**موثَّقة** (النتائج، والخطورة (severity)، والإصلاحات، وإعادة الاختبار (testing))، و**متكررة** بعد التغييرات الجوهرية. ويشترط قانون الذكاء الاصطناعي الأوروبي (EU AI Act) على مقدّمي نماذج GPAI ذات المخاطر النظامية (systemic risk) إجراء اختبارات عدائية (adversarial testing) وتوثيقها. ويعدّ NIST AI 600-1 اختبار الفريق الأحمر (red-teaming) ممارسة أساسية في الذكاء الاصطناعي التوليدي (GenAI). واختبار الفريق الأحمر (red team) يكتشف الإخفاقات. لكنه لا يثبت غيابها، ولذلك فهو يكمّل التقييم المنهجي (systematic evaluation) ولا يحل محله.

**تقييم الذكاء الاصطناعي التوليدي والتقييم البشري (GenAI evaluation and human evaluation).** مقاييس الدقة (accuracy) التقليدية لا تناسب النصوص المفتوحة. يقيّم بنك نجم المساعد (copilot) على مجموعة اختبار منتقاة (curated test set) من حالات حقيقية (محجوبة البيانات)، تُقدَّر درجاتها حسب الاستناد إلى المصدر (groundedness) (هل كل ادعاء مدعوم بالمصدر (source)؟)، والدقة الواقعية للأرقام (factual accuracy of figures)، والاكتمال (completeness)، والأسلوب (tone). ويجمع بين:
- **المقاييس الآلية (automated metrics)** (مثل معدلات مطابقة الأرقام (figure-match rates) مع المستندات المصدرية (source documents))؛
- تقدير الدرجات بأسلوب **النموذج اللغوي حَكَمًا** (LLM-as-judge) لتحقيق النطاق الواسع. وهذا مفيد، لكن النموذج الحكم (judge model) له تحيّزاته وأخطاؤه، لذا عايره مقابل البشر ولا تعتمد عليه وحده أبدًا في الفحوص عالية الأهمية؛
- **التقييم البشري (human evaluation)** من خبراء ائتمان (credit experts) وفق معيار تقدير مكتوب (rubric)، دون أن يعرفوا أي نظام أنتج المسودة (draft) حيثما أمكن، مع فحص الاتفاق بين المقيّمين (9.2).

**المصادقة المستقلة وإدارة مخاطر النماذج (MRM).** للبنوك سبق هنا. فالإرشادات الرقابية الأمريكية (US supervisory guidance) **SR 11-7** (الاحتياطي الفيدرالي (Federal Reserve)، 2011، واعتمدها OCC) تعرّف مخاطر النماذج (model risk) وتشترط تطويرًا سليمًا (sound development) و**مصادقة مستقلة** وحوكمة (governance). وفكرتها الأساسية هي **التحدي الفعّال** (effective challenge): تحليل نقدي من أطراف موضوعية ومطّلعة تملك الكفاءة (competence) والنفوذ والحوافز لتحديد القيود وفرض التغييرات. وتضع **SS1/23** الصادرة عن هيئة التنظيم الاحترازي البريطانية (PRA) مبادئ إدارة مخاطر النماذج (model risk management principles) للبنوك، وتُدخل صراحةً نماذج (models) الذكاء الاصطناعي (AI) وتعلّم الآلة (machine learning) في نطاقها. ويطبّق كثير من بنوك دول الخليج (GCC) مبادئ مماثلة. وينبغي لبنك نجم أيضًا مراجعة إرشادات الذكاء الاصطناعي الصادرة عن QCB لمعرفة التوقعات الحالية. وعادةً ما تراجع المصادقة المستقلة (independent validation) لنظام ذكاء اصطناعي (AI system): السلامة المفاهيمية (هل النهج مناسب؟ هل البيانات والخصائص (features) مبرَّرة؟)؛ وجودة البيانات (data quality) وتسلسلها؛ وتكرار النتائج الرئيسية (replication of key results)؛ وتحليل النتائج (outcomes analysis) والمقارنة المرجعية مع البدائل (benchmarking against alternatives)؛ واختبارات العدالة (fairness tests) وقابلية التفسير (explainability)؛ والمتانة (robustness)؛ واختبار التنفيذ (هل يطابق الإنتاج (production) ما جرت المصادقة (validation) عليه؟)؛ وخطة الرصد (monitoring plan). ويرفع المصادِق (validator) تقاريره إلى خط الدفاع الثاني (المخاطر)، لا إلى بنّائي النموذج (model). وفي أبريل 2026 حلّت محلّها إرشادات **SR 26-2** (*Revised Guidance on Model Risk Management*) التي أصدرها الاحتياطي الفيدرالي وOCC وFDIC. وهي أكثر اعتمادًا على المبادئ (principles-based)، وتربط شدة التحقق (validation intensity) بأهمية النموذج (materiality) بدلًا من دورات ثابتة، وتضيّق تعريف النموذج، وتُخضع نماذج المورّدين (vendor models) للمعيار نفسه؛ راجع نصّها الحالي لمعرفة كيف تتعامل مع الذكاء الاصطناعي التوليدي والوكيلي (generative and agentic AI).

**معايير القبول والاعتماد النهائي (Acceptance criteria and sign-off).** قبل بدء الاختبار (testing)، يتفق المالك (owner) والمطوّرون والمصادِق (validator) والحوكمة (governance) على **معايير القبول** (acceptance criteria): المقاييس، والعتبات (thresholds)، والمجموعات (groups)، ومجموعات الاختبار، وعاقبة الإخفاق. مثال: "AUC على بيانات خارج الفترة الزمنية (out-of-time) ≥ الحد الأدنى المتفق عليه (agreed floor)؛ المعايرة (calibration) ضمن الهامش المسموح (tolerance) في كل بلد؛ نسبة معدل الموافقة (approval-rate ratio) ≥ 0.8 أو تبرير موثّق توافق عليه اللجنة (committee)؛ فجوة معدل الإيجابيات الصحيحة (TPR gap) ≤ 3 نقاط؛ لا توجد نتائج حرجة مفتوحة من الفريق الأحمر (critical red-team findings open)؛ اجتياز فحص أمانة رموز الأسباب (reason-code faithfulness check)." ثم تُقارن النتائج بمعايير ثُبّتت مسبقًا، وهذا يمنع تحريك المرمى (moving the goalposts). ويتبع الاعتماد النهائي (sign-off) الفئة (tier) المحددة في 8.1. وبالنسبة إلى نظام من الفئة 1 (Tier 1) في بنك نجم، يعني ذلك مالك الأعمال (business owner)، والمصادِق المستقل (independent validator)، ومسؤول حماية البيانات (للمخاطر المتبقية في تقييم الأثر على حماية البيانات (DPIA residual risk))، ولجنة حوكمة الذكاء الاصطناعي (AI Governance Committee). وتُسجَّل الشروط والمخاطر المتبقية المقبولة (accepted residual risks) في سجل القرارات (decision log). وبالنسبة إلى الأنظمة عالية المخاطر (high-risk systems) بموجب قانون الذكاء الاصطناعي الأوروبي (EU AI Act)، فإن الاختبار مقابل مقاييس محددة مسبقًا (prior defined metrics) وعتبات احتمالية (probabilistic thresholds) جزء من نظام إدارة المخاطر (risk management system) لدى مقدّم النظام (provider). وتغذّي نتائجه ملف الملحق IV (Annex IV) وتقييم المطابقة (conformity assessment) (الوحدة 10 (Module 10)).

## ⚖️ الأدوات التنظيمية (The instruments)
| الأداة | ما تشترطه أو توصي به (What it requires or recommends) | إشارة الامتحان (Exam cue) |
|---|---|---|
| **EU AI Act** — المادتان 9 و15 | الأنظمة عالية المخاطر (high-risk systems): الاختبار (testing) مقابل مقاييس محددة مسبقًا (prior defined metrics) وعتبات احتمالية (probabilistic thresholds) كجزء من إدارة المخاطر (risk management)؛ مستويات مناسبة من الدقة والمتانة والأمن السيبراني (appropriate levels of accuracy, robustness and cybersecurity) مُعلنة في التعليمات (instructions) | المعايير تُحدَّد قبل الاختبار (testing) |
| **EU AI Act** — المادة 55 | نماذج GPAI (GPAI models) ذات المخاطر النظامية (systemic risk): تقييم النموذج (model evaluation)، بما فيه الاختبار العدائي (adversarial testing)، مع التوثيق (documentation) | واجب اختبار الفريق الأحمر (red-teaming) لنماذج GPAI (GPAI models) ذات المخاطر النظامية (systemic risk) |
| **NIST AI RMF** — وظيفة القياس (Measure function) | أساليب TEVV، والمقاييس، والتقييم (evaluation) المستقل، وتتبّع خصائص الجدارة بالثقة (trustworthiness) | "القياس" (Measure) = TEVV |
| **NIST AI 600-1** | مخاطر الذكاء الاصطناعي التوليدي (GenAI) والإجراءات (actions)، بما فيها اختبار الفريق الأحمر (red-teaming)، ومصدر المحتوى (content provenance)، وتقييم التلفيق (confabulation evaluation) | اختبار الفريق الأحمر (red-teaming) في الذكاء الاصطناعي التوليدي (GenAI) |
| **SR 11-7** | (حلّت محلّها **SR 26-2** في أبريل 2026.) إرشادات رقابية أمريكية (US supervisory guidance) بشأن إدارة مخاطر النماذج (model risk management): التطوير السليم (sound development)، والمصادقة المستقلة (independent validation)، والتحدي الفعّال (effective challenge)، والحوكمة (governance) | "التحدي الفعّال (effective challenge)" |
| **PRA SS1/23** | مبادئ بريطانية لإدارة مخاطر النماذج (model risk management) في البنوك، بما فيها نماذج (models) الذكاء الاصطناعي (AI) وتعلّم الآلة (machine learning) | إدارة مخاطر النماذج (model risk management) تمتد إلى الذكاء الاصطناعي (AI) |
| **NYC Local Law 144** | تدقيق مستقل سنوي للتحيّز (Annual independent bias audit) في أدوات قرارات التوظيف الآلية (automated employment decision tools)، مع نشر ملخص | اختبار العدالة الإلزامي (Mandated fairness testing) |
| **ISO/IEC 42001** | نظام إدارة الذكاء الاصطناعي (AI management system): التحقق والمصادقة (verification and validation) وتقييم الأداء (performance evaluation) كجزء من ضوابط (controls) دورة الحياة (life cycle) | أدلة TEVV (TEVV evidence) قابلة للاعتماد |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
**ورقة معايير القبول والاعتماد النهائي (Acceptance Criteria and Sign-off Sheet): نموذج ائتمان الأفراد (retail credit model) الإصدار 1.0 (الفئة 1 (Tier 1))**، المتفق عليها *قبل* جولة الاختبار النهائية (final test run):

| # | المعيار (Criterion) | العتبة (Threshold) | النتيجة | الحالة |
|---|---|---|---|---|
| 1 | AUC خارج الفترة الزمنية (2023–24) | ≥ الحد الأدنى المتفق عليه (agreed floor) و≥ بطاقة التقييم الحالية (current scorecard) | مستوفى؛ أعلى من بطاقة التقييم (scorecard) | ✅ |
| 2 | المعايرة حسب البلد (QA، AE، DE) | المتنبأ به مقابل الملاحظ (Predicted vs observed) ضمن الهامش المسموح (tolerance) | DE يبالغ قليلًا في التنبؤ | ⚠️ إعادة المعايرة (Recalibrate)؛ إعادة الاختبار (testing) |
| 3 | نسبة معدل الموافقة (النساء/الرجال؛ دون 25/25 فأكثر) | ≥ 0.8 أو تبرير توافق عليه اللجنة (committee) | 0.84 / 0.77 | ⚠️ يلزم تبرير لفئة دون 25 (under-25) |
| 4 | فجوة تكافؤ الفرص (معدل الإيجابيات الصحيحة (true positive rate)) | ≤ 3 نقاط | 1.2 / 2.6 | ✅ |
| 5 | مراجعة التسرّب (Leakage review) | لا خصائص لاحقة للقرار؛ لا تداخل في العملاء | أُزيلت خاصية (feature) واحدة؛ أُعيد التشغيل | ✅ |
| 6 | اختبار الإجهاد (سيناريو الركود (recession scenario)) | التدهور (Degradation) ضمن الهامش المسموح (tolerance)؛ موثَّق | موثَّق | ✅ |
| 7 | رموز الأسباب (reason codes) | اجتياز فحوص الأمانة (faithfulness checks) والاستقرار؛ صياغة اعتمدتها إدارة الامتثال (Compliance) | مُجتاز | ✅ |
| 8 | المصادقة المستقلة (independent validation) | لا نتائج عالية الخطورة (high-severity) مفتوحة | نتيجتان متوسطتا الخطورة (medium) مع خطة معالجة (remediation plan) | ✅ بشروط (with conditions) |
| 9 | المخاطر المتبقية في DPIA / FRIA (DPIA / FRIA residual risk) | يقبلها مسؤول حماية البيانات (Data Protection Officer, DPO) ومالك الأعمال (business owner) | مقبولة | ✅ |

**الاعتماد النهائي (sign-off):** خالد (مالك الأعمال (business owner)) · المصادقة المستقلة على النماذج (خط الدفاع الثاني (second line)) · سارة (مسؤولة حماية البيانات (Data Protection Officer, DPO)) · ليلى (حوكمة الذكاء الاصطناعي (AI governance)) ← **لجنة حوكمة الذكاء الاصطناعي (AI Governance Committee): موافقة بشروط (approved with conditions)** (إعادة معايرة (recalibrate) DE؛ تبرير أو تخفيف لفئة دون 25 (under-25) خلال 60 يومًا؛ مراجعة يدوية (manual review) بنسبة 100% للمتقدمين (applicants) دون 25 حتى ذلك الحين).

## 🛠️ التمارين (Exercises)
- 🟢 نموذج (model) احتيال يصنّف 1% من المعاملات؛ والاحتيال (fraud) يمثل 0.2% من المعاملات. اشرح بكلمات بسيطة لماذا الدقة (accuracy) مقياس ضعيف هنا، وأي مقياسين ستبلغ عنهما بدلًا منها. *يكتمل عندما (Done when):* تستطيع شرح الضبط والاستدعاء (precision and recall) لخالد في جملتين لكل منهما.
- 🟡 باستخدام المثال المحلول (worked example)، احسب نسبة معدل الموافقة (approval-rate ratio) وفجوة معدل الإيجابيات الكاذبة (FPR gap) إذا ارتفعت موافقات المجموعة B (Group B) إلى 450 (400 جيد، 50 سيئ). *يكتمل عندما (Done when):* تذكر أي مقاييس العدالة (fairness metrics) تتحسن، وأيها يسوء، وما الذي يجب أن يقبله مالك الأعمال (business owner).
- 🔴 صمّم خطة اختبار فريق أحمر (red-team plan) للمساعد الذكي لمذكرات الائتمان (credit memo copilot): النطاق، وتكوين الفريق، وعشرة سيناريوهات اختبار (ثلاثة منها على الأقل بالعربية)، ومقياس الخطورة (severity scale)، ومعايير الخروج (exit criteria). *يكتمل عندما (Done when):* يرتبط كل سيناريو بخطر من مخاطر OWASP للنماذج اللغوية الكبيرة (LLM) أو بمتطلب جدارة بالثقة من 8.2، وترتبط معايير الخروج بالاعتماد النهائي (sign-off).

## ⚠️ أخطاء وفخاخ الامتحان (Mistakes and exam traps)
- **الدقة الإجمالية (overall accuracy) على بيانات غير متوازنة (imbalanced data).** استخدم الضبط والاستدعاء (precision and recall) وAUC والمعايرة (calibration)، وأبلغ عنها حسب المجموعة (by group).
- **"النموذج (model) يستوفي كل مقاييس العدالة (fairness metrics)."** مع اختلاف المعدلات الأساسية (base rates) يكون هذا مستحيلًا في العادة. توقّع المفاضلة (trade-off) ووثّق الاختيار.
- **الضبط على مجموعة الاختبار (Tuning on the test set).** إنه يضخّم النتائج. استخدم مجموعة تحقق منفصلة (separate validation set) واختبارًا خارج الفترة الزمنية (out-of-time test).
- **المصادقة على يد البنّائين (Validation by the builders).** تشترط إدارة مخاطر النماذج (model risk management) تحديًا مستقلًا وفعّالًا (independent, effective challenge).
- **تحديد العتبات (thresholds) بعد رؤية النتائج.** معايير القبول (acceptance criteria) تُثبَّت مسبقًا.
- **معاملة اختبار الفريق الأحمر (red-teaming) كإثبات للسلامة (proof of safety).** إنه يكتشف الإخفاقات. ويكمّل التقييم المنهجي (systematic evaluation) والرصد (monitoring).

## 🧾 الخلاصة (Recap)
- يوفّر TEVV الأدلة (evidence). فالتحقق (verification) يفحص البناء (build) مقابل المواصفات (spec)، والمصادقة (validation) تفحص الملاءمة للاستخدام الحقيقي.
- التقسيم السليم، والاختبار خارج الفترة الزمنية (out-of-time testing)، وفحوص التسرّب (leakage checks) تجعل النتائج جديرة بالثقة.
- اختر المقاييس بحسب الضرر (harm) والقرار. فالدقة (accuracy) وحدها مضلِّلة.
- تتعارض مقاييس العدالة (fairness metrics) عندما تختلف المعدلات الأساسية (base rates). والاختيار بينها قرار حوكمة (governance) موثَّق.
- اختبارات الإجهاد (stress tests)، واختبار الفريق الأحمر (red-teaming)، والتقييم البشري (human evaluation)، والمصادقة المستقلة (independent validation) تكمل الأدلة (evidence). ومعايير القبول (acceptance criteria) المتفق عليها مسبقًا تقود اعتمادًا نهائيًا مناسبًا للفئة (tier-appropriate).

## ✍️ اختبر نفسك (Check yourself)

**1. يُبلغ نموذج الائتمان (credit model) في بنك نجم عن دقة 94% على مجموعة اختبار (test set) تعثّر فيها 6% من المتقدمين (applicants). ما أفضل استجابة؟**

- A. اعتمده؛ 94% ممتازة
- B. اطلب من الفريق رفع الدقة (accuracy) إلى 99%
- C. اطلب الضبط والاستدعاء (precision and recall) وAUC والمعايرة (calibration)، إجمالًا وحسب المجموعة (by group)، لأن نموذجًا (model) يتنبأ بـ "لا تعثّر" للجميع سيحقق 94% أيضًا
- D. استبدل مجموعة الاختبار (test set) بمجموعة التدريب (training set)

<details><summary>الإجابة (Answer)</summary>

**C.** مع الفئات غير المتوازنة (imbalanced classes)، تخفي الدقة (accuracy) الإخفاق. أما D فسيُدخل تسرّبًا (leakage) ويضخّم النتائج. (🟢 الأساسيات (The essentials).)

</details>

**2. في المثال المحلول (worked example)، معدل موافقة (approval rate) المجموعة A (Group A) هو 54% ومعدل المجموعة B (Group B) هو 36%، بينما معدلات الإيجابيات الصحيحة (true positive rates) متساوية تقريبًا. أي عبارة صحيحة؟**

- A. التكافؤ الديموغرافي (demographic parity) وتكافؤ الفرص (equal opportunity) كلاهما متحقق
- B. لا يمكن حساب أي مقياس عدالة (fairness metric) دون قيم SHAP
- C. تكافؤ الفرص (equal opportunity) لا يتحقق لكن التكافؤ الديموغرافي (demographic parity) يتحقق
- D. التكافؤ الديموغرافي (demographic parity) لا يتحقق (النسبة ≈ 0.67) لكن تكافؤ الفرص (equal opportunity) متحقق تقريبًا

<details><summary>الإجابة (Answer)</summary>

**D.** 36/54 ≈ 0.67 أقل من 0.8، ومعدلات الإيجابيات الصحيحة (true positive rates) نحو 83% في المجموعتين. فالمقاييس تقيس أشياء مختلفة. (🟡 التعمق أكثر (Going deeper).)

</details>

**3. تتضمن بيانات تدريب نموذج ائتمان (credit model) مؤشر "أُحيل إلى التحصيل (sent to collections)" لا يُضبط إلا بعد تعثّر العميل. يحقق النموذج (model) درجات ممتازة في الاختبار (testing) وأداءً ضعيفًا في الإنتاج (production). ما السبب الأرجح؟**

- A. تسرّب البيانات (Data leakage)
- B. التحيّز التجميعي (Aggregation bias)
- C. استخراج النموذج (model extraction)
- D. قلة سيناريوهات الفريق الأحمر (red-team scenarios)

<details><summary>الإجابة (Answer)</summary>

**A.** خاصية (feature) غير متاحة وقت القرار سرّبت معلومات النتيجة إلى التدريب. (🟢 الأساسيات (The essentials).)

</details>

**4. بموجب إرشادات إدارة مخاطر النماذج (model risk management guidance) مثل SR 11-7، ما الذي يتطلبه "التحدي الفعّال (effective challenge)"؟**

- A. أن يعيد فريق التطوير (development) تشغيل اختباراته الخاصة
- B. مراجعة نقدية من أطراف موضوعية وكفؤة تملك نفوذًا كافيًا لفرض معالجة القيود
- C. أن يعتمد المورّد (vendor) نموذجه بنفسه
- D. اجتماعًا سنويًا واحدًا لمجلس الإدارة (board)

<details><summary>الإجابة (Answer)</summary>

**B.** يعتمد التحدي الفعّال (effective challenge) على الاستقلالية والكفاءة والنفوذ (independence, competence and influence). والمراجعة الذاتية (A، C) لا تُعدّ كذلك. (🔴 نظرة الخبير (Expert view).)

</details>

**5. يقترح فريق المساعد (copilot) تحديد عتبات النجاح (pass thresholds) للاستناد إلى المصدر (groundedness) *بعد* رؤية نتائج التقييم (evaluation results) "لنكون واقعيين". بماذا ينبغي أن ينصح مسؤول حوكمة الذكاء الاصطناعي (AI governance)؟**

- A. الموافقة (consent)، لأن العتبات (thresholds) ينبغي أن تعكس ما يستطيع النموذج (model) فعله
- B. تجاوز العتبات (thresholds) في أنظمة الذكاء الاصطناعي التوليدي (GenAI)
- C. الرفض: يجب تحديد معايير القبول (acceptance criteria) مسبقًا والاتفاق عليها مع المالك (owner) والمصادِق (validator) والحوكمة (governance)، مع توثيق (documentation) أي تغيير لاحق واعتماده
- D. ترك المورّد (vendor) يحدد العتبات (thresholds)

<details><summary>الإجابة (Answer)</summary>

**C.** المعايير المتفق عليها مسبقًا تمنع تحريك المرمى (moving the goalposts) وتجعل الاعتماد النهائي (sign-off) ذا معنى. وقانون الذكاء الاصطناعي (AI) يتوقع كذلك أن تُختبر الأنظمة عالية المخاطر (high-risk systems) مقابل مقاييس محددة مسبقًا (prior defined metrics). (🔴 نظرة الخبير (Expert view).)

</details>

## 📚 المراجع (References)
- EU AI Act، اللائحة (EU) 2024/1689 (المواد 9 و15 و55) — https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- إطار NIST لإدارة مخاطر الذكاء الاصطناعي 1.0 ودليله التطبيقي (NIST AI Risk Management Framework 1.0 and Playbook) — https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI 600-1، ملف الذكاء الاصطناعي التوليدي (Generative AI Profile) — https://doi.org/10.6028/NIST.AI.600-1
- مجلس محافظي نظام الاحتياطي الفيدرالي (Board of Governors of the Federal Reserve System)، SR 11-7 إرشادات إدارة مخاطر النماذج (Guidance on Model Risk Management) — https://www.federalreserve.gov/boarddocs/srletters/2011/sr1107.htm
- الاحتياطي الفيدرالي (Federal Reserve) وOCC وFDIC، SR 26-2 الإرشادات المنقّحة بشأن إدارة مخاطر النماذج (Revised Guidance on Model Risk Management)، أبريل 2026: https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm
- بنك إنجلترا، هيئة التنظيم الاحترازي (SS1/23 مبادئ إدارة مخاطر النماذج (model risk management principles) للبنوك) — https://www.bankofengland.co.uk/prudential-regulation
- إدارة حماية المستهلك والعامل في مدينة نيويورك (قانون أدوات قرارات التوظيف الآلية (AEDT law)، AEDT) — https://www.nyc.gov/site/dca/index.page
- ISO/IEC 42001:2023 — https://www.iso.org/standard/81230.html
- IAPP، مجال المعرفة (BoK) لشهادة AIGP — https://iapp.org/certify/aigp/
