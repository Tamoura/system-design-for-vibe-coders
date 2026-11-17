# الوحدة 3 — البنية التحتية بوصفها شيفرة (Infrastructure as code)

*الحساب السحابي (cloud account) الذي يغيّره الناس بالنقر نظامٌ لا يستطيع أحد أن يصفه وصفًا كاملًا أو يراجعه أو يعيد بناءه. وهذه الوحدة تحوّل البنية التحتية (infrastructure) لبنك نجم (Najm Bank) إلى شيفرة (code): ملفات في Git تقول ما الذي ينبغي أن يوجد، وأداة تستنتج كيف تصل إليه، ومراجعة (review) قبل أن يتغيّر أي شيء. تبدأ الوحدة بـ Terraform وOpenTofu، وهما أوسع الأدوات من هذا النوع استخدامًا: كيف تعمل الحالة (state) والخطط (plans) والوحدات البرمجية (modules)، ولماذا يكون ملف الحالة (state file) أكثر ملف حساسيةً يملكه فريق المنصة (platform team). ثم تنتقل من بيئة واحدة (one environment) إلى بيئات كثيرة (many)، مستخدمةً GitOps لترقية (promote) التغيير نفسه من بيئة التطوير (dev) إلى بيئة ما قبل الإنتاج (staging) إلى الإنتاج (production) عبر طلب سحب (pull request)، بينما يسحب Argo CD أو Flux النتيجة إلى العناقيد (clusters). وتنتهي بالضوابط (controls) التي تُبقي كل ذلك آمنًا على نطاق واسع: السياسة بوصفها شيفرة (policy as code) التي تفحص كل تغيير آليًا، واكتشاف الانحراف (drift detection) الذي يلاحظ متى لم يعد الواقع مطابقًا للشيفرة، والحواجز الواقية (guardrails) التي تجعل المسار الآمن (safe path) هو المسار السهل. ستتابع يوسف بينما تكاد إعادة تسمية (rename) من كلمة واحدة في طلب سحب أن تستبدل قاعدة بيانات إنتاجية (production database)، وسالم وهو يصمّم مسار الترقية (promotion path) لـ واجهة برمجة تطبيق نجم للهاتف (Najm Mobile API)، ومها وهي تكتشف لماذا كفّت بيئة ما قبل الإنتاج والإنتاج عن التصرّف بالطريقة نفسها.*

> **المراحل (Phases):** Code, Release, Deploy, Operate — وصف البنية التحتية (describing infrastructure) في ملفات قابلة للمراجعة (reviewable files)، وترقية التغييرات عبر البيئات بطلبات السحب، وإبقاء ما يعمل متّسقًا مع ما اعتُمد.

---

# 3.1 — البنية التحتية بوصفها شيفرة باستخدام Terraform/OpenTofu: الحالة والوحدات والخطط
*المستوى (Level): 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 1.2، 1.3* · *المرحلة (Phase): Code, Deploy*

## ⚡ الدرس في دقيقة (In 60 seconds)
- تعني **البنية التحتية بوصفها شيفرة (infrastructure as code, IaC)** وصفَ الخوادم (servers) والشبكات (networks) وقواعد البيانات (databases) والصلاحيات (permissions) في ملفات نصية (text files) تطبّقها أداةٌ نيابةً عنك. تُراجَع الملفات (reviewed)، وتُدار إصداراتها (versioned)، ويمكن تكرارها (repeatable)؛ وتصبح وحدة التحكم (console) للقراءة فقط (read-only) في العمل اليومي (day-to-day work).
- إن **Terraform** وفرعه مفتوح المصدر (open-source fork) **OpenTofu** أداتان *تصريحيتان (declarative)*: تكتب الحالة النهائية (end state) التي تريدها، فتستنتج الأداة أيّ استدعاءات إنشاء وتحديث وحذف عليها أن تنفّذ.
- تتذكّر الأداة ما تديره في **ملف الحالة (state file)**. احفظ الحالة عن بُعد (remote)، ومقفلة (locked)، ومشفّرة (encrypted)، ومضبوطة الوصول بإحكام (tightly access-controlled)، لأنها قد تحتوي على أسرار (secrets)، وفقدانها يعني أن تفقد تتبّع ما تملكه.
- **اقرأ الخطة دائمًا (Always read the plan).** عبارتا "must be replaced" أو "destroy" بجوار قاعدة بيانات (database) هما أهم سطرين ستراهما طوال الأسبوع.
- غلّف الأنماط المتكررة (repeated patterns) في **وحدات برمجية (modules)** ذات واجهات صغيرة مُتحقَّق منها؛ وثبّت إصدارات (pin versions) الوحدات والمزوّدات.
- الفخ الأكبر (Biggest trap): تنفيذ `apply` من حاسوب محمول (laptop) ببيانات اعتماد واسعة (broad credentials). عمليات التطبيق في الإنتاج (production applies) تجري في خط تسليم (pipeline)، انطلاقًا من خطة محفوظة سبقت مراجعتها.

## 🧭 لماذا يهم
تبدو أول تذكرة (ticket) يتسلّمها يوسف صغيرة: إعادة تسمية قاعدة بيانات المدفوعات (Payments database) من `payments-db` إلى `najm-payments-prod` لتوافق معيار التسمية (naming standard). يعدّل سطرًا واحدًا ويطلب موافقة سريعة (quick approval). تفتح مها الخطة (plan) التي أرفقها خط التسليم بطلب السحب:

```text
  # module.payments_db.aws_db_instance.this must be replaced
-/+ resource "aws_db_instance" "this" {
      ~ identifier = "payments-db" -> "najm-payments-prod" # forces replacement
      ...
Plan: 1 to add, 0 to change, 1 to destroy.
```

مع إصدار مزوّد AWS الذي يثبّته الفريق، لا يمكن تغيير المعرّف (identifier) في مكانه (إصدارات المزوّد الأحدث تستطيع إعادة تسميته في مكانه؛ والخطة وحدها تخبرك بأيّهما لديك)، لذا كانت الأداة ستحذف قاعدة بيانات المدفوعات الإنتاجية وتنشئ قاعدة فارغة (empty one). كانت الشيفرة صحيحة (valid)، وقالت الخطة بالضبط ما سيحدث؛ والسؤال الوحيد كان هل سيقرؤها أحد. تمنع مها الدمج. وفي عصر ذلك اليوم يضيف سالم قاعدتين: كل قاعدة بيانات إنتاجية تحمل `prevent_destroy`، ولا يُدمج أي طلب سحب للإنتاج حتى يؤكد مراجعٌ (reviewer) سطرَ ملخّص الخطة.

أما لماذا تحتاج عمليات النشر (deploys) إلى بوابات (gates) أصلًا فيتناوله [*تصميم الأنظمة لمبرمجي الحدس (System Design for Vibe Coders)*، الدرس 4.4 — التراجع وبيئة ما قبل الإنتاج وبوابات الإطلاق (Rollback, staging, and release gates)](../vibe/index.ar.html#l4-4)؛ وهنا تتعلّم كيف تُبنى البنية التحتية التي تحتها وكيف تُغيَّر.

## 📐 كيف يعمل
### 🟢 الأساسيات
**لماذا الشيفرة بدل النقرات (Why code instead of clicks).** قاعدة البيانات التي تُنشأ في وحدة تحكم ويب (web console) لا تترك سجلًا قابلًا للمراجعة (reviewable record). لا يستطيع أحد مراجعة التغيير مسبقًا (beforehand)، ولا تكراره بدقة في بيئة أخرى (another environment)، ولا إعادة بنائه بعد كارثة (disaster). والبنية التحتية بوصفها شيفرة (IaC) تعالج الثلاثة كلها: لكل تغيير في Git مؤلِّف (author) ومراجِع وتاريخ (history)؛ والملفات نفسها تبني بيئة التطوير وبيئة ما قبل الإنتاج والإنتاج؛ وبعد عطل إقليمي (regional failure) يكون وصف كل ما تحتاجه موجودًا في مستودع (repository).

**التصريحي مقابل الأمري (Declarative versus imperative).** السكربت *الأمري (imperative)* يسرد خطوات ("أنشئ شبكة، ثم قاعدة بيانات")؛ شغّله مرتين وقد تحصل على قاعدتي بيانات. أما الأداة *التصريحية* فتقارن وصف الحالة النهائية بما هو موجود؛ شغّلها مرتين فلا يفعل التشغيل الثاني شيئًا. هذه الخاصية هي **عدم التأثر بالتكرار (idempotence)**، وهي ما يجعل إعادة تشغيل البنية التحتية بوصفها شيفرة آمنة.

**Terraform وOpenTofu.** تستخدم أداة **Terraform**، من إنتاج HashiCorp، لغة تهيئة (configuration language) تُسمّى **HCL**. وفي أغسطس 2023 نقلت HashiCorp أداة Terraform من رخصة مفتوحة المصدر (open-source licence) إلى رخصة المصدر التجاري. فاشتقّ المجتمع (community) آخر إصدار مفتوح المصدر باسم **OpenTofu**، وهو مشروع تابع لـ Linux Foundation (قُبل في بيئة الاحتضان CNCF sandbox عام 2025). وتبقى الأداتان متقاربتين: لغة HCL نفسها، والمزوّدات (providers) نفسها، ومعظم الأوامر (commands) نفسها (`terraform` مقابل `tofu`)، وإن كانت بعض الميزات (features) تختلف الآن، فراجع التوثيق (docs) الخاص بأداتك وإصدارها. ينطبق هذا الدرس على كلتيهما؛ وتستخدم التمارين (exercises) OpenTofu لأنه مفتوح المصدر.

اللبنات الأساسية:

| المفهوم (Concept) | ما هو | مثال (Example) |
|---|---|---|
| **المزوّد (Provider)** | إضافة (plugin) تتخاطب مع واجهة برمجة تطبيقات (API) واحدة: سحابة (cloud)، أو Kubernetes، أو Docker، أو GitHub | `hashicorp/aws`، `hashicorp/azurerm`، `hashicorp/google`، `kreuzwerker/docker` |
| **المورد (Resource)** | شيء واحد تنشئه الأداة وتديره | شبكة (network)، قاعدة بيانات، حاوية تخزين (bucket)، حاوية (container) |
| **مصدر البيانات (Data source)** | شيء يُقرأ ولكن لا يُدار | معرّف شبكة فريق آخر |
| **المتغيّر (Variable)** | مُدخل (input) إلى التهيئة (configuration) | `environment = "prod"` |
| **المُخرج (Output)** | قيمة تكشفها التهيئة | اسم مضيف الاتصال (connection hostname) لقاعدة البيانات |
| **الوحدة البرمجية (Module)** | مجلد قابل لإعادة الاستخدام (reusable folder) من الموارد له مُدخلات ومُخرجات | `modules/postgres` |
| **الحالة (State)** | سجلّ الأداة لأيّ الكائنات الحقيقية (real objects) تديرها | `terraform.tfstate` |

تهيئة مصغّرة (minimal configuration) يمكنك تشغيلها محليًا (locally) باستخدام مزوّد Docker (Docker provider)، دون حاجة إلى حساب سحابي:

```hcl
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0" # allow any 3.x release, never a surprise 4.0
    }
  }
}

provider "docker" {}

resource "docker_image" "web" {
  name         = "nginx:1.27-alpine"
  keep_locally = true
}

resource "docker_container" "web" {
  name  = "najm-hello"
  image = docker_image.web.image_id
  ports {
    internal = 80
    external = 8080
  }
}
```

**سير العمل (The workflow).** أربعة أوامر تحمل كل شيء تقريبًا:

```shell
tofu init                 # download providers and modules, connect to the state backend
tofu plan -out=tfplan     # compare code, state and reality; save the proposed changes
tofu show tfplan          # read the plan (a human does this)
tofu apply tfplan         # apply exactly the saved plan, nothing else
```

يكتب `init` أيضًا **ملف قفل الاعتماديات (dependency lock file)**، وهو `.terraform.lock.hcl`، بإصدارات المزوّدات الدقيقة ومجاميعها الاختبارية (checksums). أودِعه في المستودع (Commit it).

**قراءة الخطة (Reading a plan).** يبدأ سطر كل مورد برمز (symbol): `+` إنشاء (create)، و`-` حذف (destroy)، و`~` تحديث في المكان، و`-/+` حذف ثم إنشاء بديل. اقرأ سطر الملخّص (summary line) أولًا ("Plan: 2 to add, 1 to change, 0 to destroy.")، ثم كل `-` و`-/+`. والتغييرات التي لا يمكن إجراؤها في المكان تُعلَّم بـ `# forces replacement`.

### 🟡 التعمق أكثر (Going deeper)
**الحالة: ذاكرة الأداة (State: the tool's memory).** يربط ملف **الحالة (state)** الشيفرة بالواقع: فهو يقابل `module.payments_db.aws_db_instance.this` بمعرّف قاعدة بيانات حقيقي ويخزّن آخر سماتها المعروفة. ومن دونه لا تستطيع الأداة التمييز بين "قاعدة بياناتي، وتحتاج إلى تغيير" و"قاعدة بيانات شخص آخر".

ثلاث حقائق تحدّد كيف تتعامل معه:
- **قد يحتوي على أسرار بنص صريح (secrets in plain text).** إذا كانت لمورد سمة كلمة مرور (password attribute)، فإن قيمتها تنتهي في الحالة، حتى لو كان المتغيّر مُعلَّمًا بـ `sensitive` (فهذه العلامة تخفيها فقط من مُخرجات الشاشة). عامِل ملف الحالة كما تعامل مخزن بيانات الاعتماد (credential store). وقد أضاف OpenTofu تشفيرًا اختياريًا للحالة من جهة العميل؛ وأيًّا كانت الأداة التي تستخدمها، شفّر أيضًا وسيط التخزين (storage) الذي توجد فيه. والأفضل من ذلك أن تتجنّب تمرير الأسرار عبر البنية التحتية بوصفها شيفرة أصلًا: دع قاعدة البيانات تولّد كلمة مرور المسؤول (admin password) داخل مدير أسرار (secrets manager) ([*أمن الذكاء الاصطناعي والتطبيقات (Secure AI & Application Security)*، الدرس 5.2 — إدارة الأسرار: المفاتيح والرموز وأين تتسرّب](../secai/index.ar.html#/5.2)).
- **قد يُفسده شخصان يطبّقان في الوقت نفسه (Two people applying at once can corrupt it).** يمنع **القفل (lock)** تشغيلًا ثانيًا ما دام تشغيلٌ آخر قيد التنفيذ.
- **الملف المحلي على حاسوب محمول نقطة إخفاق وحيدة (single point of failure).** إن فقدته نسيت الأداة كل ما تديره.

لذلك تعيش حالة الإنتاج (production state) في **واجهة تخزين خلفية بعيدة (remote backend)** مزوّدة بالقفل (locking) والتشفير (encryption) وإدارة الإصدارات (versioning) ووصول ضيّق (narrow access):

```hcl
terraform {
  backend "s3" {
    bucket       = "najm-tfstate-prod"           # versioning and encryption enabled on the bucket
    key          = "mobile-api/database.tfstate" # one state per component
    region       = "<your-region>"
    encrypt      = true
    use_lockfile = true # S3-native locking in recent versions; older setups use a DynamoDB table
  }
}
```

تستخدم Azure الواجهة الخلفية `azurerm`، وتستخدم Google Cloud الواجهة الخلفية `gcs`؛ وتخزّن الخدمات المستضافة (hosted services) مثل HCP Terraform الحالةَ نيابةً عنك. راجع توثيق أداتك (tool's documentation) لمعرفة الخيارات الحالية (current options).

**الوحدات البرمجية: منتج فريق المنصة (Modules: the platform team's product).** **الوحدة البرمجية (module)** مجلد من الموارد تكون المتغيّرات (variables) مُدخلاته والمُخرجات (outputs) نتائجه. لا يريد بنك نجم أربعين إعدادًا مختلفًا قليلًا لـ PostgreSQL؛ بل يريد إعدادًا واحدًا يكون افتراضيًا مدعومًا بنسخ احتياطية (backed up)، ومشفّرًا، وخاصًا (private)، ومراقَبًا (monitored)، تستهلكه الفرق (teams) كما تستهلك مكتبة (library):

```hcl
module "orders_db" {
  source = "git::https://git.najm.example/platform/tf-modules.git//postgres?ref=v1.4.0" # pinned tag

  name           = "orders"
  environment    = "prod"
  size           = "medium"
  data_class     = "confidential"
  backup_days    = 35
  owner          = "team-orders"
}
```

الوحدات البرمجية الجيدة (Good modules) لها واجهة صغيرة (small interface)، وقيم افتراضية ذات رأي واضح (opinionated defaults)، وكتل `validation` على المتغيّرات تُفشل مبكرًا (fail early) برسالة واضحة (clear message) (مثلًا، يجب أن تكون `environment` إما `dev` أو `staging` أو `prod`). والوحدة البرمجية التي تكشف كل وسيطات المزوّد ليست سوى المزوّد نفسه مع خطوات إضافية.

**حماية ما يجب ألّا يموت (Protecting what must not die).** في الموارد ذات الحالة (stateful resources)، اطلب من الأداة أن ترفض الحذف (refuse destruction):

```hcl
resource "aws_db_instance" "this" {
  # ...
  deletion_protection = true # the cloud API refuses deletes too
  lifecycle {
    prevent_destroy = true   # the IaC tool refuses any plan that would destroy this
  }
}
```

يوقف `prevent_destroy` الخطة السيئة (bad plan)؛ أما حماية الحذف (deletion protection) لدى المزوّد فتوقف أيضًا من يعمل في وحدة التحكم أو في أداة أخرى (another tool).

**من يشغّل `apply` (Who runs apply).** في بنك نجم لا أحد يطبّق على الإنتاج (applies production) من حاسوب محمول. ينشر خط التسليم الخطة على كل طلب سحب؛ وبعد الموافقة (approval) والدمج (merge) يطبّق *تلك الخطة المحفوظة* بدور قصير العمر (short-lived role) يُحصل عليه عبر اتحاد الهوية OIDC (OIDC federation)، لا بمفاتيح مخزّنة (stored keys) (1.3). أما `apply` جديد بعد ساعة فسيحسب خطة جديدة (new plan) لم يراجعها أحد.

```mermaid
flowchart RL
    A["طلب سحب<br/>(Pull request)"] --> B["التكامل المستمر يشغّل الخطة<br/>(CI runs plan)"]
    B --> C["نشر الخطة للمراجعة<br/>(Plan posted for review)"]
    C --> D["المراجع يوافق<br/>(Reviewer approves)"]
    D --> E["الدمج في الفرع الرئيسي<br/>(Merge to main)"]
    E --> F["التكامل المستمر يطبّق الخطة المحفوظة<br/>(CI applies saved plan)"]
    F --> G["حفظ الحالة وتحرير القفل<br/>(State saved and lock released)"]
```

### 🔴 نظرة الخبير (Expert view)
**نطاق الضرر وحدود الحالة (Blast radius and state boundaries).** حالة واحدة عملاقة للبنك كله تجعل كل خطة بطيئة، وكل تطبيق (apply) يُقفل الباب على الجميع، وكل خطأ قادرًا على المساس بكل شيء. قسّم الحالة حسب المكوّن والمالك: أسس الشبكة (network foundations)، وعنقود Kubernetes (Kubernetes cluster)، ومخازن بيانات كل تطبيق، وDNS. ومرّر القيم بين الحالات (between states) عبر مُخرجات تقرؤها مصادر البيانات (data sources)، أو عبر مخزن معاملات (parameter store).

**إعادة الهيكلة دون حذف (Refactoring without destroying).** نقل مورد إلى وحدة برمجية يغيّر عنوانه (address)، وعادةً سترى الأداة "حُذف العنوان القديم، وأُنشئ العنوان الجديد". أما كتلة `moved` فتخبرها بأن الكائن (object) صار له ببساطة اسم جديد:

```hcl
moved {
  from = aws_db_instance.payments
  to   = module.payments_db.aws_db_instance.this
}
```

وبالمثل، تُدخل كتل `import` الموارد الموجودة المبنية يدويًا تحت الإدارة (under management)، وتوقف كتل `removed` إدارة مورد ما دون حذفه. وتُراجَع هذه في الخطة مثل كل شيء آخر، بخلاف أمرَي سطر الأوامر (command-line) `state mv` و`state rm` اللذين يغيّران الحالة دون أي مراجعة. تحقّق من أن إصدارك يدعم كل كتلة.

**انضباط الإصدارات (Versioning discipline).** ثبّت إصدار الأداة (`required_version` وفي التكامل المستمر (CI))، والمزوّدات (القيود (constraints) مع ملف القفل)، والوحدات البرمجية (وسم (tag)، لا فرعًا متحرّكًا (moving branch) أبدًا). رقِّ (Upgrade) واحدًا في كل مرة، في بيئة التطوير أولًا: فترقية مزوّد (provider upgrade) تغيّر قيمة افتراضية (default) قد تُنتج خطة مليئة بتحديثات لم يطلبها أحد.

**البدائل (Alternatives).** تستخدم **Pulumi** لغات عامة الأغراض (general-purpose languages) مثل TypeScript أو Python أو Go، مع نموذج الحالة والخطة (state-and-plan model) نفسه. أما **AWS CloudFormation** و**Azure Bicep** فأصيلتان في سحابتيهما (وقد تغيّر العرض الأصيل (native offering) لدى Google Cloud مع الوقت؛ راجع توثيقه)؛ وكثيرًا ما تدعمان الخدمات الجديدة أولًا. يغطي Terraform وOpenTofu مزوّدات كثيرة (many providers) بسير عمل واحد (one workflow)، وهذا يناسب بنكًا يشغّل Kubernetes وDNS وشبكة توصيل محتوى (CDN) وGitHub وسحابة معًا. والمفاهيم (concepts) هنا تنتقل إليها جميعًا.

**وكلاء البرمجة بالذكاء الاصطناعي والبنية التحتية بوصفها شيفرة (AI coding agents and IaC).** يكتب الوكلاء (Agents) شيفرة HCL بسرعة، وقد "يصلحون" خطأً بتوسيع مجموعة أمان أو بإضافة صلاحية شاملة (wildcard permission). الخطة والماسحات (scanners) والسياسات (policies) (3.3) هي التي تقرّر، لا ثقة الوكيل (agent's confidence). ويغطي [*أمن الذكاء الاصطناعي والتطبيقات*، الدرس 7.2 — الحاويات وKubernetes والبنية التحتية بوصفها شيفرة](../secai/index.ar.html#/7.2) الفحوص الأمنية (security checks) بتعمّق.

## 🧰 الأدوات
| الأداة أو الممارسة أو الخدمة (Tool, practice or service) | ما هي وماذا تفعل | متى تلجأ إليها |
|---|---|---|
| **OpenTofu** (Linux Foundation) | أداة بنية تحتية بوصفها شيفرة تصريحية مفتوحة المصدر مشتقّة من Terraform؛ HCL والمزوّدات والحالة والخطط | الخيار الافتراضي (default choice) لأعمال IaC الجديدة مفتوحة المصدر ولتمارين هذه الدورة |
| **Terraform** (HashiCorp) | الأداة الأصلية (original) للبنية التحتية بوصفها شيفرة القائمة على HCL، تخضع لرخصة BSL منذ أغسطس 2023، ولها خدمة مستضافة (hosted service) هي HCP Terraform | حيث تكون مؤسستك قد اعتمدتها معيارًا أو تستخدم ميزاتها المستضافة (hosted features) |
| **Remote state with locking** — الحالة البعيدة مع القفل | تخزين حالة مشترك ومشفّر ومُدار الإصدارات يمنع عمليات التطبيق المتزامنة (concurrent applies) | أي تهيئة يلمسها أكثر من شخص واحد أو خط تسليم واحد |
| **IaC module** — وحدة البنية التحتية البرمجية | مجلد قابل لإعادة الاستخدام من الموارد بواجهة صغيرة مُتحقَّق منها وقيم افتراضية آمنة (safe defaults) | أي نمط يُبنى أكثر من مرتين: قواعد البيانات، وحاويات التخزين (buckets)، والعناقيد، والشبكات |
| **Pulumi** | البنية التحتية بوصفها شيفرة بلغات عامة الأغراض مع نموذج الخطة والحالة (plan-and-state model) نفسه | الفرق التي تفضّل لغات حقيقية (real languages) للبنية التحتية |

## 🏛️ عمليًا في بنك نجم
يطلب سالم من يوسف أن يكتب الواجهة (interface) لأول وحدة برمجية من نوع المسار الذهبي (golden-path module) في المنصة، كي تستطيع فرق التطبيقات (app teams) طلب قاعدة بيانات بملء ستة أسطر. هذا هو **معيار نجم للوحدات البرمجية للبنية التحتية (Najm IaC module standard): `postgres` v1**.

**الجزء أ: الواجهة (Part A: interface)**

| المُدخل | النوع والقيم المسموحة | القيمة الافتراضية | لماذا هو مُدخل |
|---|---|---|---|
| `name` | سلسلة نصية (string)، أحرف صغيرة وشَرطات، من 3 إلى 30 حرفًا | لا يوجد (مطلوب) | يبني المعرّف `najm-<name>-<environment>` |
| `environment` | `dev` أو `staging` أو `prod` | لا يوجد (مطلوب) | يحدّد حدود الحجم (size limits) والنسخ الاحتياطية (backups) والحماية (protection) |
| `size` | `small` أو `medium` أو `large` | `small` | يقابل فئة مثيل (instance class) لكل سحابة؛ لا تختار الفرق أنواع المثيلات الخام أبدًا |
| `data_class` | `internal` أو `confidential` أو `restricted` | `confidential` | التصنيف المقيَّد (Restricted) يفرض مفاتيح يديرها العميل (customer-managed keys) وتسجيلًا إضافيًا (extra logging) |
| `backup_days` | رقم (number)، من 7 إلى 35 | 7 في بيئة التطوير، و35 في الإنتاج (prod) | هدف التعافي (recovery target)؛ محدود بالحد الأقصى لدى المزوّد (provider's maximum) |
| `owner` | المعرّف المختصر للفريق (team slug) | لا يوجد (مطلوب) | يصبح الوسم `owner` للتنبيهات (alerts) وتقارير التكلفة (cost reports) (6.2) |

| المُخرج | الاستخدام (Use) |
|---|---|
| `endpoint` | اسم مضيف خاص (private hostname) لتهيئة التطبيق (application's configuration) |
| `secret_ref` | اسم مدخل مدير الأسرار (secrets-manager entry) الذي يحفظ بيانات الاعتماد المولّدة (generated credentials)؛ وليس كلمة المرور نفسها أبدًا |
| `dashboard_url` | رابط إلى لوحة المتابعة القياسية (standard dashboard) لقاعدة البيانات |

**الجزء ب: ما تثبّته الوحدة البرمجية ولا يمكن تهيئته (Part B: fixed by the module, not configurable)**
- شبكات خاصة فقط؛ لا نقطة نهاية عامة (public endpoint) أبدًا.
- التشفير أثناء التخزين (encryption at rest) وTLS أثناء النقل مُفعَّلان.
- حماية الحذف و`prevent_destroy` في `staging` و`prod`.
- بيانات اعتماد المسؤول (Admin credentials) تولّدها السحابة وتُخزَّن في مدير الأسرار؛ ولا يمرّ أيٌّ منها عبر المتغيّرات.
- الوسوم القياسية (Standard tags): `owner`، و`environment`، و`data-class`، و`cost-centre`، و`managed-by = opentofu`.

**الجزء ج: قواعد الحالة والتطبيق (Part C: state and apply rules)**
- حالة واحدة لكل مكوّن (`<team>/<service>/<component>.tfstate`)، وحاوية تخزين خلفية (backend bucket) واحدة لكل بيئة (per environment)؛ إدارة الإصدارات والتشفير مُفعَّلان؛ والوصول (access) مقصور على دور خط التسليم (pipeline role) ومهندسَين اثنين مسمَّيين لكسر الزجاج.
- عمليات التطبيق في الإنتاج تجري فقط من خط التسليم، ومن خطة محفوظة (saved plan)، بموافقة فريق المنصة والفريق المالك (owning team).
- أي `destroy` أو `must be replaced` على مورد ذي حالة (stateful resource) يحتاج إلى موافقة مها أو سالم.

## 🛠️ التمارين
تعمل الثلاثة كلها على جهازك باستخدام Docker وOpenTofu. وإن اخترت بدلًا من ذلك الفئة المجانية (free tier) لدى سحابة ما، فاضبط تنبيه ميزانية (budget alert) قبل إنشاء أي شيء.

- 🟢 استخدم تهيئة Docker (Docker configuration) من 🟢 الأساسيات. شغّل `init` و`plan -out=tfplan` و`apply tfplan`، وتحقّق من الصفحة على المنفذ (port) 8080، ثم غيّر المنفذ الخارجي (external port) واقرأ الخطة الجديدة. وأخيرًا شغّل `plan` مرة أخرى دون تغيير أي شيء. *يكتمل عندما (Done when):* تستطيع الإشارة إلى السطر الذي يقول هل ستُحدَّث الحاوية في مكانها أم ستُستبدل (replaced)، وتُبلغ الخطة الأخيرة بعدم وجود تغييرات.
- 🟡 حوّل التهيئة إلى وحدة برمجية `modules/web` بمُدخلات مُتحقَّق منها (validated inputs) هي `name` و`port` و`image_tag`، واستدعِها مرتين لتشغيل حاويتين (two containers). استخدم كتلة `moved` للحاوية الأصلية (original container). *يكتمل عندما:* يفشل منفذ غير صالح (invalid port) عند `plan` برسالة الخطأ التي كتبتها، وتُظهر خطة إعادة الهيكلة (refactor plan) نقلًا (move) دون أي حذف (zero destroys).
- 🔴 شغّل مخزن كائنات متوافقًا مع S3 (S3-compatible object store) محليًا في Docker (MinIO أو بديلًا عنه؛ تحقّق من رخصته الحالية (current licence) وصوره)، واستخدمه واجهة تخزين خلفية بعيدة مقفلة. ابدأ عمليتي تطبيق (two applies) في الوقت نفسه من طرفيتين (two terminals). ثم أضف `prevent_destroy` إلى إحدى الحاويتين وغيّر اسمها، وهو ما يفرض الاستبدال (forces replacement). *يكتمل عندما:* يُرفض التطبيق الثاني بسبب القفل، وتُرفض خطة الاستبدال المفروض (forced-replacement plan) بخطأ `prevent_destroy`، ولا يوجد ملف حالة في مجلد العمل (working directory).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **تصفّح الخطة على عجل (Skimming the plan).** اقرأ سطر الملخّص وكل `-` و`-/+` قبل الموافقة. اجعل خط التسليم ينشر الخطة داخل طلب السحب كي لا يستطيع المراجعون (reviewers) تجاوزها.
- **الحالة في Git أو على حاسوب محمول (State in Git or on a laptop).** قد تحمل الحالة أسرارًا، وهي الخريطة الوحيدة لما تملكه. استخدم واجهة تخزين خلفية (backend) بعيدة ومقفلة ومشفّرة ومُدارة الإصدارات بوصول ضيّق.
- **تشغيل `apply` جديد بدل الخطة التي رُوجعت (Running a fresh apply instead of the reviewed plan).** ربما تغيّر الواقع (reality) في الأثناء. طبّق ملف الخطة المحفوظ، أو أعد التخطيط وأعد المراجعة.
- **وحدات برمجية ومزوّدات غير مثبّتة الإصدار (Unpinned modules and providers).** إنها تغيّر بنيتك التحتية دون تغيير في الشيفرة (code change). ثبّت الإصدارات وأودِع ملف القفل (lock file).
- **جراحة الحالة في الثانية فجرًا ⁦(State surgery at 2 a.m.)⁩.** أمر `state rm` غير المراجَع (unreviewed) يُفقدك تتبّع موارد حقيقية (real resources). استخدم كتل `moved` و`import` و`removed` في طلب سحب.

## 🧾 الخلاصة (Recap)
- تحوّل البنية التحتية بوصفها شيفرة البنية التحتية إلى شيفرة مُراجَعة ومُدارة الإصدارات وقابلة للتكرار؛ والأدوات التصريحية (declarative tools) مثل Terraform وOpenTofu تحسب التغييرات نيابةً عنك.
- تربط الحالة الشيفرة بالموارد الحقيقية. احفظها بعيدة ومقفلة ومشفّرة ومضبوطة الوصول، وقسّمها حسب المكوّن للحدّ من نطاق الضرر (blast radius).
- الخطة هي شبكة الأمان (safety net): احفظها، وراجعها في طلب السحب، وطبّق تلك الخطة بعينها من خط تسليم ببيانات اعتماد قصيرة العمر (short-lived credentials).
- الوحدات البرمجية هي منتج فريق المنصة: واجهات صغيرة مُتحقَّق منها، وقيم افتراضية آمنة، وإصدارات مثبّتة (pinned versions).
- احمِ الموارد ذات الحالة بـ `prevent_destroy` وبحماية الحذف لدى المزوّد، وأعد الهيكلة (refactor) بكتل `moved` و`import` و`removed`.

## ✍️ اختبر نفسك (Check yourself)

**1. يعيد يوسف تسمية معرّف (identifier) قاعدة بيانات المدفوعات الإنتاجية (production payments database) في شيفرة Terraform. تُظهر الخطة (plan) `-/+` و`# forces replacement` لقاعدة البيانات. ماذا سيحدث إذا طُبّقت هذه الخطة؟**

- A. تُعاد تسمية قاعدة البيانات في مكانها دون أي توقف
- B. تُحذف قاعدة البيانات وتُستبدل بقاعدة جديدة فارغة
- C. لا شيء، لأن Terraform لا يحذف قواعد البيانات أبدًا
- D. يُحدَّث ملف الحالة (state file) فقط، وتبقى قاعدة البيانات الحقيقية (real database) دون مساس

<details><summary>الإجابة</summary>

**B.** تعني `-/+` الحذف ثم إنشاء بديل، ويقول التعليق (comment) أيّ سمة (attribute) تفرض ذلك. الخيار A هو ما افترضه يوسف؛ والخيار C خاطئ ما لم تُضبط `prevent_destroy` أو حماية الحذف (deletion protection). (🟢 الأساسيات، و🧭 لماذا يهم.)

</details>

**2. لماذا يجب تخزين ملف الحالة (state file) لـ Terraform أو OpenTofu في واجهة تخزين خلفية (backend) مقفلة ومشفّرة ومضبوطة الوصول (locked, encrypted, access-controlled) بدل إيداعه في Git؟**

- A. لا يستطيع Git تخزين ملفات أكبر من ميغابايت واحد، وملفات الحالة (state files) كثيرًا ما تتجاوز ذلك
- B. لا تُحتاج ملفات الحالة (state files) إلا أثناء التطبيق الأول (first apply)
- C. ترفض المزوّدات (providers) العمل إذا كانت الحالة في مستودع (repository)
- D. قد تحمل الحالة أسرارًا بنص صريح (plain-text secrets)، وقد تُفسدها عمليات الكتابة المتزامنة غير المقفلة

<details><summary>الإجابة</summary>

**D.** تنتهي السمات الحساسة (sensitive attributes) في الحالة (state) بصرف النظر عن العلامة `sensitive`، والقفل (locking) يمنع تشغيلين من الكتابة في آن واحد. الخيار B خاطئ: فالحالة مطلوبة في كل تشغيل (every run). (🟡 التعمق أكثر (Going deeper).)

</details>

**3. يشغّل خط تسليم (pipeline) الأمر `plan` عند فتح طلب سحب (pull request). يُوافَق على طلب السحب ويُدمج بعد ثلاث ساعات، ثم يشغّل خط التسليم `apply` جديدًا (fresh) دون خطة محفوظة (saved plan). ما الخطر؟**

- A. إنه يعيد التخطيط (re-plans) مقابل الشيفرة والواقع الحاليين، لذا قد يطبّق تغييرات لم تُراجَع
- B. لا يوجد خطر، لأن `apply` يكرّر دائمًا أحدث خطة شغّلها خط التسليم (pipeline)
- C. سيفشل التطبيق، لأن كل خطة تنتهي صلاحيتها بعد ساعة من تشغيل `plan`
- D. سيُحذف ملف الحالة (state file) بالكامل من الواجهة الخلفية البعيدة (remote backend)

<details><summary>الإجابة</summary>

**A.** التطبيق الجديد (fresh apply) يحسب خطة جديدة. وحفظ الخطة باستخدام `-out` ثم تطبيق ذلك الملف يعني أن التغييرات المُراجَعة هي التغييرات المطبَّقة. الخيار B هو سوء الفهم الشائع (common misunderstanding). (🟡 التعمق أكثر (Going deeper).)

</details>

**4. يريد سالم أن تنشئ فرق التطبيقات (app teams) قواعد بيانات PostgreSQL تكون دائمًا خاصة ومشفّرة ومدعومة بنسخ احتياطية (private, encrypted and backed up). أيّ تصميم يحقّق ذلك على أفضل وجه؟**

- A. صفحة ويكي (wiki page) تسرد الإعدادات الموصى بها (recommended settings)، مرتبطة من دليل الإعداد (onboarding guide) لكل فريق
- B. وحدة برمجية (module) تكشف كل وسيطات المزوّد متغيّراتٍ كي تحظى الفرق بمرونة كاملة (full flexibility)
- C. وحدة برمجية بواجهة صغيرة مُتحقَّق منها وإعدادات الأمان مثبّتة داخلها
- D. منح كل فريق صلاحية المسؤول (administrator access) على وحدة التحكم السحابية (cloud console)

<details><summary>الإجابة</summary>

**C.** تثبيت القيم الافتراضية الآمنة (safe defaults) داخل الوحدة البرمجية يجعل التهيئة الصحيحة (right configuration) هي الوحيدة المتاحة. الخيار B يعيد إنتاج عدم الاتساق (inconsistency) الذي ينبغي للوحدة أن تزيله؛ والخيار A يعتمد على أن يقرأه الجميع ويتّبعوه. (🟡 التعمق أكثر (Going deeper)، و🏛️ عمليًا.)

</details>

**5. ينقل فريق المنصة (platform team) مورد قاعدة بيانات موجودًا (existing database resource) إلى وحدة برمجية جديدة (new module). تُظهر الخطة حذف العنوان القديم (old address) وإنشاء عنوان جديد. ما الإصلاح الأكثر أمانًا (safest fix)؟**

- A. طبّقها في ساعة هادئة (quiet hour) واستعد من النسخة الاحتياطية بعد ذلك
- B. أضف كتلة `moved` من العنوان القديم (old address) إلى العنوان الجديد (new address)
- C. احذف ملف الحالة (state file) وشغّل `import` من سطر الأوامر (command line) لكل مورد
- D. انسخ شيفرة الوحدة البرمجية (module code) عائدًا إلى التهيئة الجذرية (root configuration) بصورة دائمة

<details><summary>الإجابة</summary>

**B.** تسجّل كتلة `moved` إعادة التسمية تصريحيًا وتُراجَع في الخطة. الخيار A يسبّب انقطاعًا (outage) وفقدانًا للبيانات (data loss)؛ والخيار C جراحة حالة (state surgery) خطرة غير مُراجَعة. (🔴 نظرة الخبير (Expert view).)

</details>

## 📚 المراجع (References)
- توثيق OpenTofu (OpenTofu documentation) — https://opentofu.org/docs/
- توثيق Terraform (Terraform documentation) — https://developer.hashicorp.com/terraform/docs
- لغة Terraform: الحالة — https://developer.hashicorp.com/terraform/language/state
- لغة Terraform: الوحدات البرمجية — https://developer.hashicorp.com/terraform/language/modules
- HashiCorp، الأسئلة الشائعة حول الترخيص (licensing FAQ) (رخصة المصدر التجاري) — https://www.hashicorp.com/
- Linux Foundation، مشروع OpenTofu (OpenTofu project) — https://opentofu.org/
- توثيق Pulumi (Pulumi documentation) — https://www.pulumi.com/docs/

---

# 3.2 — البيئات وGitOps: ترقية التغييرات من بيئة التطوير إلى الإنتاج
*المستوى: 🟡 متوسط* · *المتطلبات: 2.2، 2.3، 3.1* · *المرحلة: Release, Deploy*

## ⚡ الدرس في دقيقة (In 60 seconds)
- **البيئة (environment)** (التطوير، وما قبل الإنتاج، والإنتاج) نسخة كاملة من النظام لغرض محدّد. ينبغي ألّا تختلف البيئات إلا في التهيئة والحجم، ولا تختلف أبدًا في الشيفرة أو البنية.
- **ابنِ مرة واحدة، ورقِّ الأثر البرمجي نفسه (Build once, promote the same artefact).** بصمة الصورة (image digest) نفسها التي اختُبرت في بيئة ما قبل الإنتاج هي التي تصل إلى الإنتاج؛ ولا يُعاد بناء شيء على طول الطريق.
- تعني **GitOps** أن الحالة المرغوبة (desired state) لكل بيئة تعيش في Git، وأن وكيلًا (agent) داخل المنصة يسحبها ويجعل الواقع مطابقًا لها باستمرار. مبادئه الأربعة (four principles): تصريحي، ومُدار الإصدارات وغير قابل للتغيير (versioned and immutable)، ويُسحب آليًا (pulled automatically)، ويُوفَّق باستمرار (continuously reconciled).
- **الترقية (promotion)** طلب سحب يغيّر قيمة واحدة (عادةً بصمة صورة) في مجلد البيئة التالية. راجِع، وادمج، ويتولّى **Argo CD** أو **Flux** الباقي؛ أما **التراجع (rollback)** فهو `git revert`.
- إشارة القرار (Decision cue): إن لم تستطع الإجابة عن سؤال "ما الذي يعمل في الإنتاج بالضبط، ومن وافق عليه؟" من Git وحده، فأنت لا تمارس GitOps بعد.
- الفخ الأكبر: فروع طويلة العمر لكل بيئة، وتعديلات يدوية (hand edits) بـ `kubectl` تكتب فوقها المزامنة التالية (next sync) بصمت، أو لا يلاحظها أحد أبدًا.

## 🧭 لماذا يهم
في 1 أغسطس 2012 نشرت Knight Capital، وهي شركة أمريكية كبيرة لصناعة السوق (market-making firm)، شيفرة تداول جديدة على خوادمها. ووفقًا لأمر هيئة الأوراق المالية والبورصات الأمريكية في القضية، نسخ فنّيٌّ (technician) الشيفرة الجديدة إلى سبعة من الخوادم الثمانية ولم ينسخها إلى الثامن، ولم يلاحظ أحد. وأعاد الإصدار الجديد (new release) استخدام علامة (flag) شغّلت على الخادم الثامن شيفرةً قديمة متروكة منذ زمن طويل. فأرسل ذلك الخادم ملايين الأوامر غير المقصودة (unintended orders) خلال نحو 45 دقيقة، وخسرت الشركة قرابة 460 مليون دولار، وفقًا للهيئة (SEC). كان النشر يدويًا (manual deployment)، ولم يكن هناك فحص آلي (automated check) يتحقّق من أن كل خادم يشغّل الإصدار نفسه (same version)، ولم يراجع شخص ثانٍ (second person) النتيجة.

لدى بنك نجم نسخة أصغر من المشكلة نفسها. تحقّق مها في سبب استمرار خلل مهلة (timeout bug) أُصلح في بيئة ما قبل الإنتاج في الظهور في الإنتاج. فالإنتاج يشغّل صورة (image) من الالتزام (commit) نفسه لكنها أُعيد بناؤها بعد يومين بصورة أساس (base image) أحدث، كما أن أحدهم رفع حجم مجمّع الاتصالات (connection-pool size) باستخدام `kubectl edit` أثناء حادثة (incident) الشهر الماضي. ولا شيء في Git يسجّل أيًّا من الاختلافين، فلم تعد بيئة ما قبل الإنتاج تتنبّأ بسلوك الإنتاج.

يمنح هذا الدرس الفريق قاعدة واحدة (one rule) وآلية واحدة (one mechanism). القاعدة: الأثر البرمجي (artefact) نفسه ينتقل عبر كل بيئة، ولا تختلف إلا التهيئة. والآلية: GitOps، حيث يكون Git السجلّ الوحيد (single record) لما ينبغي أن يعمل وأين، ويجعل متحكّمٌ (controller) ذلك واقعًا ويُبلغ عن أي اختلاف (difference).

## 📐 كيف يعمل
### 🟢 الأساسيات
**لماذا البيئات (Why environments).** تحتاج إلى مكان تجرّب فيه التغييرات ليس هو الإنتاج. يستخدم بنك نجم ثلاث بيئات:

| البيئة | الغرض (Purpose) | البيانات (Data) | من ينشر |
|---|---|---|---|
| **dev** — التطوير | دمج التغييرات وتجربتها بسرعة | بيانات اختبار اصطناعية | آليًا عند كل دمج |
| **staging** — ما قبل الإنتاج | بروفة نهائية (Final rehearsal) بتهيئة وحجم شبيهين بالإنتاج | بيانات مُقنَّعة أو اصطناعية، ولا بيانات عملاء حقيقية (real customer data) أبدًا دون موافقة | طلب سحب للترقية (Promotion pull request)، بموافقة الفريق (team approval) |
| **prod** — الإنتاج | العملاء (Customers) | بيانات حقيقية (Real data) | طلب سحب للترقية، بموافقة الفريق والمنصة |

**تكافؤ البيئات (Environment parity).** يسمّي منهج التطبيق ذي العوامل الاثني عشر (Twelve-Factor App) ذلك "تكافؤ التطوير والإنتاج (dev/prod parity)": أبقِ البيئات متشابهة قدر الإمكان. ولا يُسمح بالاختلافات إلا حيث تكون مقصودة ومكتوبة: أعداد النسخ المتماثلة (replica counts)، وأحجام المثيلات (instance sizes)، وأسماء النطاقات (domain names)، وبيانات الاعتماد (credentials)، وإعدادات أعلام الميزات (feature-flag settings). أما اختلاف الشيفرة، أو الصور (images)، أو إصدارات Kubernetes، أو تخطيطات الشبكة (network layouts)، فيجعل نتائج بيئة ما قبل الإنتاج (staging results) بلا معنى.

**ابنِ مرة واحدة، ورقِّ الأثر البرمجي (Build once, promote the artefact).** يبني التكامل المستمر صورة الحاوية (container image) مرة واحدة، من التزام واحد، ويدفعها (pushes) إلى السجل (registry). وتُعرَّف الصورة ببصمتها (**digest**)، وهي تجزئة SHA-256 (SHA-256 hash) لمحتواها مثل `sha256:4f1c…`، لا بوسم مثل `v2.3` أو `latest`، لأن الوسم يمكن نقله إلى صورة مختلفة أما البصمة فلا (2.1). ثم تشغّل كل بيئة تلك البصمة. أما إعادة البناء للإنتاج، كما في حالة مها، فتُنتج أثرًا برمجيًا مختلفًا (different artefact) لم يختبره أحد.

**ما هو GitOps (What GitOps is).** يحدّد مشروع OpenGitOps، التابع لـ CNCF، أربعة مبادئ:
- **تصريحي (Declarative)**: تُوصَف الحالة المرغوبة للنظام، ولا تُكتب في سكربت.
- **مُدار الإصدارات وغير قابل للتغيير (Versioned and immutable)**: يُخزَّن ذلك الوصف بطريقة تحفظ التاريخ الكامل (full history) ولا يمكن تغييرها بصمت، وهذا يعني عمليًا Git.
- **يُسحب آليًا (Pulled automatically)**: تجلب وكلاء برمجية (software agents) الحالة المرغوبة من المصدر (source)؛ ولا يدفع أحد التغييرات إلى العنقود (cluster) يدويًا.
- **يُوفَّق باستمرار (Continuously reconciled)**: تواصل الوكلاء مقارنة الحالة الفعلية (actual state) بالحالة المرغوبة وتعمل على سدّ أي فجوة.

أشهر متحكّمَي GitOps (GitOps controllers) لـ Kubernetes هما **Argo CD** و**Flux**، وكلاهما مشروع متخرّج (graduated) في CNCF. يعمل كلٌّ منهما داخل العنقود، ويراقب مستودع Git (Git repository)، ويطبّق ما يجده.

**الدفع مقابل السحب (Push versus pull).** في خط تسليم *الدفع (push)* التقليدي، يحمل التكامل المستمر بيانات اعتماد العنقود (cluster credentials) ويشغّل `kubectl apply` أو `helm upgrade` في النهاية. أما في GitOps القائم على *السحب (pull)*، فلا يلمس التكامل المستمر العنقود أبدًا: إنه يحدّث Git فقط. والمتحكّم داخل العنقود هو الذي يسحب. وهذا يعني بيانات اعتماد قوية (powerful credentials) أقل خارج العنقود، ومسار تدقيق كاملًا في Git، وتصحيحًا آليًا (automatic correction) حين يغيّر أحدهم العنقود يدويًا.

```mermaid
flowchart RL
    A["التزام في مستودع التطبيق<br/>(Commit to app repo)"] --> B["التكامل المستمر يبني الصورة ويختبرها<br/>(CI builds and tests image)"]
    B --> C["السجل يخزّن الصورة ببصمتها<br/>(Registry stores image by digest)"]
    C --> D["طلب سحب يرفع البصمة في مجلد التطوير<br/>(PR bumps digest in dev folder)"]
    D --> E["أرغو سي دي يزامن بيئة التطوير<br/>(Argo CD syncs dev)"]
    E --> F["طلب سحب يرقّي البصمة إلى ما قبل الإنتاج<br/>(PR promotes digest to staging)"]
    F --> G["أرغو سي دي يزامن بيئة ما قبل الإنتاج<br/>(Argo CD syncs staging)"]
    G --> H["طلب سحب معتمد يرقّي إلى الإنتاج<br/>(Approved PR promotes to prod)"]
    H --> I["أرغو سي دي يزامن بيئة الإنتاج<br/>(Argo CD syncs prod)"]
```

### 🟡 التعمق أكثر
**مستودعان (Two repositories).** يفصل بنك نجم شيفرة مصدر التطبيق عن تهيئة البيئات (environment configuration):
- يحفظ **مستودع التطبيق (app repo)** شيفرة واجهة الهاتف (Mobile API) وملف Dockerfile والاختبارات (tests)؛ ويبني التكامل المستمر الصور منه؛
- ويحفظ **مستودع GitOps (GitOps repo)** ما يعمل وأين: بيانات Kubernetes الوصفية (Kubernetes manifests) أو قيم Helm (Helm values) لكل بيئة.

وعندئذ لا تُطلق تغييرات التهيئة (configuration changes) أي عمليات بناء (builds)، ويمكن أن تختلف صلاحيات الوصول، ويكون تاريخ GitOps (GitOps history) سجلًا نظيفًا لعمليات النشر.

**مجلدات لا فروع لكل بيئة (Folders, not branches, per environment).** يحتفظ تصميم مبكر شائع بفرع `dev` وفرع `staging` وفرع `prod` ويدمج بينها. ويوصي كثير من الممارسين (practitioners) بعدم ذلك: فعمليات الدمج (merges) تحمل معها تغييرات لا علاقة لها، والفروع تتباعد (drift apart)، والاختلافات بين البيئات تختبئ في تاريخ Git (Git history) بدل أن تكون ظاهرة في الملفات. يستخدم بنك نجم فرعًا واحدًا `main` ومجلدًا واحدًا لكل بيئة (one folder per environment)، مبنيًّا بأداة **Kustomize**، وهي أداة مدمجة في `kubectl` تضع رقعًا صغيرة (small patches) طبقاتٍ فوق قاعدة مشتركة (shared base):

```text
gitops/
  apps/mobile-api/
    base/                 # Deployment, Service, probes: shared by all environments
      deployment.yaml
      service.yaml
      kustomization.yaml
    overlays/
      dev/kustomization.yaml
      staging/kustomization.yaml
      prod/kustomization.yaml
      prod/replicas.yaml
```

ولا تذكر طبقة الإنتاج (production overlay) إلا ما يختلف:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
images:
  - name: registry.najm.example/mobile-api
    digest: sha256:4f1c0e…   # the promoted artefact; set by the promotion PR
patches:
  - path: replicas.yaml       # 6 replicas in prod, 2 in staging
```

وإن كانت خدماتك تستخدم Helm بدلًا من ذلك (2.3)، فالنمط نفسه (same pattern) يبقى قائمًا: مخطّط (chart) واحد، وملف قيم (values file) واحد لكل بيئة، وبصمة الصورة في ملف القيم.

**الترقية طلب سحب (Promotion is a pull request).** ترقية واجهة الهاتف من بيئة ما قبل الإنتاج إلى الإنتاج تعني نسخ بصمة واحدة (one digest) من `overlays/staging` إلى `overlays/prod`. ويفتح سكربت صغير أو روبوت طلب السحب ذلك آليًا بعد اجتياز فحوص بيئة ما قبل الإنتاج (staging checks). يُظهر طلب السحب بالضبط ما يتغيّر، وتفرض قواعد CODEOWNERS (CODEOWNERS rules) الموافقين المناسبين (right approvers)، ويكون الدمج (merging) هو قرار الإطلاق (release decision). ويمكن لأدوات مثل Argo CD Image Updater وأتمتة الصور في Flux أن تكتب رفع البصمة في بيئة التطوير (dev bump) نيابةً عنك؛ أما ترقيات الإنتاج (production promotions) فأبقِها طلبات سحب صريحة مُراجَعة.

**إخبار Argo CD بما يراقبه (Telling Argo CD what to watch).** يشير كائن `Application` في Argo CD إلى مجلد (folder) وعنقود:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: mobile-api-prod
  namespace: argocd
spec:
  project: retail
  source:
    repoURL: https://git.najm.example/platform/gitops.git
    targetRevision: main
    path: apps/mobile-api/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: mobile-api
  syncPolicy:
    automated:
      prune: true     # delete objects removed from Git
      selfHeal: true  # undo manual changes made in the cluster
```

يزيل `prune` الكائنات (objects) التي حُذفت من Git؛ ويعيد `selfHeal` التعديلات اليدوية إلى ما كانت عليه. ومع تفعيل الاثنين، كان `kubectl edit` الذي وجدته مها سيُلغى خلال دقائق، وسيظهر في الأثناء بحالة "OutOfSync". ويعبّر Flux عن الفكرة نفسها بكائنَي `GitRepository` و`Kustomization`.

**التراجع (Rollback).** لأن كل عملية نشر (deployment) التزامٌ، فإن التراجع (rolling back) هو `git revert` لطلب سحب الترقية: تعود البصمة القديمة (old digest)، ويُزامِن المتحكّم (controller syncs)، ويسجّل التاريخ من تراجع ولماذا. التراجع عن *الشيفرة* سهل؛ أما التراجع عن *مخطّط قاعدة البيانات (database schema)* فليس كذلك، ولذا تتبع تغييرات المخطّط (schema changes) نمط التوسيع ثم التقليص (expand-and-contract pattern) الذي يُغطّى مع استراتيجيات الإطلاق (release strategies) (4.2).

**الأسرار في GitOps (Secrets in GitOps).** يجب ألّا يحتوي مستودع GitOps على أسرار صريحة (plain secrets)، وكائنات Secrets في Kubernetes مُرمَّزة بـ base64 فقط (only base64-encoded)، وليست مشفّرة (2.3). الأنماط الشائعة (Common patterns): **External Secrets Operator**، الذي يزامن القيم من مدير أسرار سحابي (cloud secrets manager) إلى العنقود، مع وجود مرجع (reference) فقط في Git؛ و**Sealed Secrets** أو **SOPS**، اللذان يخزّنان قيمًا مشفّرة (encrypted values) في Git لا يستطيع فكّ تشفيرها إلا العنقود. يستخدم بنك نجم مراجع إلى مدير الأسرار الخاص به؛ انظر [*أمن الذكاء الاصطناعي والتطبيقات*، الدرس 5.2 — إدارة الأسرار: المفاتيح والرموز وأين تتسرّب](../secai/index.ar.html#/5.2).

### 🔴 نظرة الخبير
**بيئات للبنية التحتية أيضًا (Environments for infrastructure, too).** تتولّى متحكّمات GitOps ما يعمل *داخل (inside)* Kubernetes. أما العناقيد وقواعد البيانات والشبكات التي تحتها فتُدار بـ OpenTofu (3.1)، وتنطبق القواعد نفسها: مجلد واحد لكل بيئة يستدعي إصدارات الوحدات البرمجية نفسها، فيكون الفرق بين بيئة ما قبل الإنتاج والإنتاج قائمةً قصيرة مقروءة من المُدخلات. تتيح **مساحات العمل (workspaces)** في Terraform لتهيئة واحدة (one configuration) أن تحتفظ بعدة حالات (several states)، لكنها تخفي البيئة التي أنت فيها خلف إعداد في سطر الأوامر (command-line setting) وتجعل التطبيق على البيئة الخاطئة سهلًا؛ أما المجلدات والواجهات الخلفية (backends) وبيانات الاعتماد المنفصلة لكل بيئة فأوضح. وتستخدم بعض الفرق أغلفة (wrappers) مثل Terragrunt، أو متحكّمات تشغّل البنية التحتية بوصفها شيفرة عبر GitOps (متحكّم Tofu المجتمعي لـ Flux، وCrossplane)؛ قيّمها بعناية مقابل خط التسليم الأبسط (simpler pipeline) في 3.1.

**حسابات منفصلة، لا مجرد فضاءات أسماء (Separate accounts, not just namespaces).** ضع الإنتاج في حسابه السحابي الخاص (AWS)، أو اشتراكه (subscription) (Azure)، أو مشروعه (project) (Google Cloud)، بحدود هوية خاصة به. خط تسليم بيئة التطوير (dev pipeline) الذي لا تستطيع بيانات اعتماده حتى رؤية الإنتاج لا يمكنه أن يكسره.

**الترتيب والاعتماديات (Ordering and dependencies).** نادرًا ما تقتصر الترقيات الحقيقية (real promotions) على خدمة واحدة. تتيح موجات المزامنة (sync waves) في Argo CD و`dependsOn` في Flux ترتيب الموارد (order resources)، مثل تغيير تهيئة (configuration change) قبل كائن Deployment الذي يحتاجه. ويولّد **ApplicationSet** في Argo CD كائن `Application` واحدًا لكل بيئة أو عنقود من قالب (template)، وهذا يُبقي خمسين عنقودًا متّسقة (consistent). أبقِ التغييرات العابرة للخدمات (cross-service changes) متوافقة مع الإصدارات السابقة (backward compatible) كي يمكن ترقية كل خدمة وحدها؛ فالترقيات المترابطة (coupled promotions) علامة على عيب في التصميم (design smell).

**البيانات الوصفية المُصيَّرة (Rendered manifests).** حين يُصيِّر Helm أو Kustomize النتيجة على نحو مختلف عمّا توقّعت، لا يُظهر الفرق (diff) في طلب السحب إلا تغيير المُدخل (input change). وتُصيِّر بعض الفرق ملف YAML النهائي (final YAML) في التكامل المستمر وتودِعه (أو تنشر الفرق المُصيَّر (rendered diff) في طلب السحب) كي يرى المراجعون بالضبط ما سيتلقّاه العنقود. يكلّف ذلك بعض الضجيج في المستودع (repository noise) ويشتري الوضوح (clarity).

**التنظيم (Regulation).** بالنسبة إلى بنك، يكون تاريخ GitOps دليلًا (evidence): من وافق على أيّ تغيير في الإنتاج، ومتى، وما الذي نُشر بالضبط. ويتوقّع قانون المرونة التشغيلية الرقمية الأوروبي (EU DORA)، الذي يسري على الكيانات المالية (financial entities) في الاتحاد الأوروبي منذ يناير 2025، إدارةً موثّقة لتغييرات تقنية المعلومات والاتصالات؛ كما تضع الجهات التنظيمية في دول الخليج (GCC regulators) مثل مصرف قطر المركزي (Qatar Central Bank) توقّعات بشأن ضبط التغيير (change control) واستخدام السحابة (cloud use). راجع النصوص الحالية (current texts) مع فريق الامتثال (compliance team) بدل الاعتماد على الملخّصات (summaries).

## 🧰 الأدوات
| الأداة أو الممارسة أو الخدمة | ما هي وماذا تفعل | متى تلجأ إليها |
|---|---|---|
| **Argo CD** (متخرّج في CNCF) | متحكّم GitOps (GitOps controller) لـ Kubernetes بواجهة ويب (web UI)، وحالة مزامنة (sync status)، وعرض للفروق (diff view)، وموجات مزامنة، وApplicationSets | الفرق التي تريد حالة مزامنة مرئية وواجهة مستخدم (UI)؛ وعناقيد كثيرة من قوالب |
| **Flux** (متخرّج في CNCF) | مجموعة أدوات من متحكّمات GitOps لـ Kubernetes (مصادر Git (Git sources)، وKustomize، وHelm، وأتمتة الصور) | الفرق التي تفضّل نهجًا قابلًا للتركيب (composable approach) يقوده سطر الأوامر والموارد المخصّصة |
| **Kustomize** | يضع رقعًا خاصة بكل بيئة (environment-specific patches) طبقاتٍ فوق بيانات Kubernetes الوصفية المشتركة؛ مدمج في `kubectl` | مجلد واحد لكل بيئة باختلافات قليلة مقروءة |
| **Helm** | يحزم بيانات Kubernetes الوصفية في مخطّطات (charts) مع ملفات قيم (values files) | الخدمات المحزومة أصلًا في مخطّطات؛ ملف قيم واحد لكل بيئة |
| **Promotion pull request** — طلب سحب الترقية | تغيير مُراجَع (reviewed change) ينسخ بصمة صورة من مجلد بيئة إلى التالية | كل خطوة نحو الإنتاج؛ قرار الإطلاق |
| **External Secrets Operator** | يزامن الأسرار (syncs secrets) من مدير أسرار سحابي إلى Kubernetes، ولا يُبقي في Git إلا المراجع | أي إعداد GitOps (GitOps setup) يحتاج إلى أسرار |

## 🏛️ عمليًا في بنك نجم
يكتب سالم **سياسة نجم للبيئات والترقية، الإصدار 1 (Najm Environment and Promotion Policy v1)**، بدءًا بـ واجهة برمجة تطبيق نجم للهاتف.

**الجزء أ: البيئات (Part A: environments)**

| | التطوير | ما قبل الإنتاج | الإنتاج |
|---|---|---|---|
| الحدّ السحابي (Cloud boundary) | حساب مشترك لغير الإنتاج | حساب خاص (Own account) | حساب خاص بهوية منفصلة |
| العنقود | عنقود تطوير مشترك | عنقود ما قبل الإنتاج (Staging cluster)، بإصدار Kubernetes الفرعي نفسه للإنتاج | عنقود الإنتاج (Prod cluster)، متعدّد المناطق (multi-zone) |
| البيانات | اصطناعية (Synthetic) | اصطناعية أو مُقنَّعة (Synthetic or masked) | حقيقية (Real) |
| الاختلافات المسموحة عن الإنتاج | النسخ المتماثلة (Replicas)، والأحجام (sizes)، والنطاق (domain)، وبيانات الاعتماد، والأعلام (flags) | النسخ المتماثلة، والنطاق، وبيانات الاعتماد | — |
| مزامنة Argo CD | آلية، مع الحذف والإصلاح الذاتي (Automated, prune and self-heal) | آلية، مع الحذف والإصلاح الذاتي | آلية، مع الحذف والإصلاح الذاتي؛ والتغييرات فقط عبر طلب سحب معتمد (approved PR) |
| من يستطيع الدمج | أي عضو في الفريق | قائد الفريق (Team lead) | قائد الفريق ومهندس المنصة؛ وتحتاج المدفوعات (Payments) أيضًا إلى مها |

**الجزء ب: قواعد الترقية (Part B: promotion rules)**
1. يبني التكامل المستمر صورة واحدة لكل التزام، ويوقّعها (signs it) (4.3)، ويسجّل بصمتها (digest). ولا تعيد أي بيئة البناء.
2. الدمج في `main` بمستودع التطبيق يفتح طلب سحب آليًا من روبوت يضبط البصمة في `overlays/dev`؛ ويُدمج آليًا إذا اجتازت الفحوص (checks pass).
3. الترقية إلى بيئة ما قبل الإنتاج والإنتاج تنسخ البصمة *نفسها (same)*، عبر طلب سحب، بعد اجتياز فحوص البيئة السابقة (اختبارات الدخان (smoke tests)، واستهلاك هدف مستوى الخدمة (SLO burn) ضمن الحدود لمدة 30 دقيقة).
4. تجري ترقيات الإنتاج في نافذة الإطلاق المتّفق عليها؛ وخارجها يستطيع قائد الحادثة (incident commander) الموافقة على ترقية طارئة (emergency promotion)، تُسجَّل في طلب السحب.
5. التراجع هو إلغاء (revert) طلب سحب الترقية. ولا أحد يشغّل `kubectl edit` أو `kubectl apply` أو `helm upgrade` على بيئة ما قبل الإنتاج أو الإنتاج.
6. كسر الزجاج (Break-glass): أثناء حادثة من الدرجة الأولى (Sev-1)، يجوز لمهندس مسمّى (named engineer) أن يغيّر الإنتاج يدويًا بموافقة قائد الحادثة؛ ويُكتب التغيير عائدًا إلى Git خلال يوم عمل واحد، وإلا ألغته المزامنة التالية.

**الجزء ج: فحص التكافؤ الأسبوعي (Part C: the weekly parity check).** يشغّل جدول المناوبة (on-call rota) الخاص بمها سكربتًا قصيرًا كل يوم اثنين يقارن (diffs) بين `overlays/staging` و`overlays/prod` ويسرد أي اختلاف غير موجود في جدول الاختلافات المسموحة (allowed table) أعلاه. وتتحوّل الاختلافات غير المفسَّرة (Unexplained differences) إلى تذاكر (tickets).

## 🛠️ التمارين
شغّل هذه التمارين على عنقود محلي (local cluster) (kind أو k3d) مع مستودع Git تملكه، مثل مستودع GitHub مجاني.

- 🟢 أنشئ `base/` و`overlays/dev` و`overlays/prod` لكائن Deployment ويب صغير، بحيث يستخدم الإنتاج ثلاث نسخ متماثلة (three replicas) والتطوير نسخة واحدة. صيِّر الاثنين (Render both) باستخدام `kubectl kustomize`. *يكتمل عندما:* تكون الاختلافات الوحيدة بين المُخرجَين المُصيَّرين هي التي قصدتها، وتستطيع سردها.
- 🟡 ثبّت Argo CD على عنقود kind، وأنشئ كائنَي `Application` (فضاءا أسماء (namespaces) للتطوير والإنتاج) يشيران إلى طبقاتك (overlays)، مع مزامنة آلية (automated sync) وحذف (prune) وإصلاح ذاتي (self-heal). غيّر بصمة صورة في بيئة التطوير عبر طلب سحب، ثم رقِّها إلى الإنتاج بطلب سحب ثانٍ. وأخيرًا شغّل `kubectl scale` يدويًا على كائن Deployment في الإنتاج. *يكتمل عندما:* تكون الترقيتان (both promotions) ظاهرتين بوصفهما التزامات (commits)، ويُلغى التحجيم اليدوي (manual scale) آليًا، وتستطيع إظهار حالة "OutOfSync" التي رأيتها قبل أن يُصلَح.
- 🔴 أضف سير عمل للتكامل المستمر (CI workflow) (لا بأس بـ GitHub Actions) إلى مستودع تطبيق يبني صورة، ويدفعها إلى سجل تتحكّم فيه، ويفتح طلب سحب في مستودع GitOps يضبط البصمة الجديدة (new digest) في `overlays/dev`. ثم تراجَع عن ترقية سيئة (bad promotion) باستخدام `git revert`. *يكتمل عندما:* يؤدي التزام شيفرة (code commit) إلى نشر في بيئة التطوير (dev deployment) دون أن يلمس أي إنسان العنقود، ويُشار إلى الصورة ببصمتها لا بوسمها، ويكون التراجع التزام إلغاء واحدًا.

## ⚠️ أخطاء وفخاخ
- **إعادة البناء لكل بيئة (Rebuilding per environment).** الصورة المُعاد بناؤها (rebuilt image) أثر برمجي مختلف غير مُختبَر. ابنِ مرة واحدة، وأشِر بالبصمة، ورقِّ البصمة.
- **فرع لكل بيئة (A branch per environment).** الفروع تتباعد (Branches drift) وتخفي الاختلافات في التاريخ. استخدم فرعًا واحدًا مع مجلد لكل بيئة.
- **التعديلات اليدوية في العنقود (Hand edits in the cluster).** أمر `kubectl edit` أثناء حادثة يُحدث انحرافًا (drift) لا يتذكّره أحد. فعّل الإصلاح الذاتي واكتب تغييرات كسر الزجاج (break-glass changes) عائدًا إلى Git.
- **أسرار صريحة في مستودع GitOps (Plain secrets in the GitOps repo).** ترميز Base64 ليس تشفيرًا. خزّن مراجع (External Secrets) أو قيمًا مشفّرة.
- **بيئة ما قبل إنتاج "شبه" إنتاجية (Staging that is "almost" production).** اختلاف إصدارات Kubernetes أو تخطيطات الشبكة أو الصور يجعل اختبارات بيئة ما قبل الإنتاج مضلِّلة (misleading). احتفظ بقائمة مكتوبة بالاختلافات المسموحة وافحصها.
- **تكامل مستمر ببيانات اعتماد مسؤول العنقود (CI with cluster-admin credentials).** في GitOps القائم على السحب (pull-based GitOps)، يكتب التكامل المستمر إلى Git فقط؛ والمتحكّم داخل العنقود هو الذي ينشر.

## 🧾 الخلاصة
- لا تختلف البيئات (Environments) إلا في تهيئة مقصودة موثّقة؛ أما الشيفرة والصورة فهما نفسهما.
- ابنِ مرة واحدة ورقِّ بصمة الصورة نفسها من التطوير إلى ما قبل الإنتاج إلى الإنتاج.
- GitOps: حالة مرغوبة مُصرَّح بها ومُدارة الإصدارات في Git، تُسحب آليًا ويوفّقها باستمرار متحكّمٌ مثل Argo CD أو Flux.
- الترقية والتراجع طلبات سحب وعمليات إلغاء، فيكون Git هو سجلّ ما يعمل وأين ومن وافق عليه.
- أبقِ الأسرار خارج Git، والإنتاج في حسابه الخاص، والتعديلات اليدوية نادرة ومعتمدة ومكتوبة عائدًا.

## ✍️ اختبر نفسك

**1. تكتشف مها أن الإنتاج (production) يشغّل صورة (image) مبنية من الالتزام (commit) نفسه الذي بُنيت منه صورة بيئة ما قبل الإنتاج (staging)، لكنها أُعيد بناؤها بعد يومين. لماذا تُعدّ هذه مشكلة؟**

- A. ليست مشكلة، لأن الالتزام نفسه (same commit) يُنتج دائمًا صورة مطابقة (identical image)
- B. يجب ألّا يُعاد بناء صور الإنتاج إلا في نافذة الإطلاق المعتمدة في عطلة نهاية الأسبوع
- C. قد تسحب إعادة البناء (rebuild) صور أساس أو اعتماديات مختلفة: أثر برمجي غير مُختبَر (untested artefact)
- D. لا يمكن تخزين الصور المُعاد بناؤها (Rebuilt images) في السجل (registry) نفسه الذي فيه البناء الأصلي

<details><summary>الإجابة</summary>

**C.** المصدر نفسه (same source) قد يُنتج صورًا مختلفة مع مرور الوقت. ابنِ مرة واحدة ورقِّ البصمة نفسها (same digest). الخيار A هو الافتراض المغري (tempting assumption) الذي يصحّحه الدرس. (🟢 الأساسيات، و🧭 لماذا يهم.)

</details>

**2. أيٌّ مما يلي أحد مبادئ OpenGitOps الأربعة (four OpenGitOps principles)؟**

- A. تسحب الوكلاء (agents) الحالة المرغوبة (desired state) آليًا وتوفّقها باستمرار
- B. يجب أن تحمل خطوط التكامل المستمر (CI pipelines) بيانات اعتماد مسؤول العنقود (cluster-admin credentials)
- C. يجب أن يكون لكل بيئة فرع Git خاص طويل العمر، يُدمج بالترتيب
- D. يجب أن يوافق مجلس استشاري للتغيير أولًا على كل نشر في الإنتاج (production deployment)

<details><summary>الإجابة</summary>

**A.** المبادئ هي: تصريحي (declarative)، ومُدار الإصدارات وغير قابل للتغيير (versioned and immutable)، ويُسحب آليًا (pulled automatically)، ويُوفَّق باستمرار (continuously reconciled). الخيار B نقيض GitOps القائم على السحب (pull-based GitOps)؛ والخيار C نمط يوصي كثيرون بعدم اتّباعه؛ والخيار D خيار تنظيمي (organisational choice)، لا مبدأ من مبادئ GitOps. (🟢 الأساسيات.)

</details>

**3. أثناء حادثة (incident)، يرفع مهندس عدد النسخ المتماثلة في الإنتاج (production replica count) باستخدام `kubectl scale`. لدى Argo CD مزامنة آلية (automated sync) مع `selfHeal: true`. ماذا يحدث بعد ذلك، وماذا ينبغي للفريق أن يفعل؟**

- A. يسجّل Argo CD القيمة الجديدة (new value) في Git آليًا (automatically)، فلا حاجة إلى أي شيء آخر
- B. يحذف Argo CD كائن Deployment بالكامل
- C. يبقى التغيير إلى الأبد (stays forever) لأن Argo CD لا يراقب إلا Git
- D. يعيده Argo CD ليطابق Git؛ والتغيير المطلوب (needed change) يمرّ عبر طلب سحب (pull request)

<details><summary>الإجابة</summary>

**D.** الإصلاح الذاتي (Self-heal) يجعل العنقود (cluster) مطابقًا لـ Git، فتُلغى التغييرات اليدوية (manual changes). والإصلاح هو تغيير الحالة المرغوبة (desired state) في Git. الخيار A خاطئ: المتحكّمات (controllers) لا تكتب عائدةً إلى Git. (🟡 التعمق أكثر (Going deeper).)

</details>

**4. تسبّب ترقية واجهة برمجة تطبيق نجم للهاتف (Najm Mobile API) إلى الإنتاج أخطاءً. ما طريقة GitOps للتراجع (GitOps way to roll back)؟**

- A. شغّل `helm rollback` مباشرة على عنقود الإنتاج (production cluster)، ثم أخبر الفريق في المحادثة (chat)
- B. ألغِ طلب سحب الترقية كي تعود البصمة السابقة وتُزامَن
- C. أعد بناء الإصدار السابق من المصدر وادفعه مجددًا تحت الوسم نفسه (same tag)
- D. احذف فضاء الأسماء (namespace) وأعد نشر الإصدار القديم من حاسوب محمول (laptop)

<details><summary>الإجابة</summary>

**B.** الإلغاء (revert) يستعيد الحالة المرغوبة السابقة ويسجّل من تراجع ولماذا. الخيار A ينجح لفترة وجيزة لكن المتحكّم (controller) سيزامن Git مجددًا والتغيير غير مسجّل (unrecorded)؛ والخيار C يعيد بناء أثر برمجي غير مُختبَر (untested artefact). (🟡 التعمق أكثر (Going deeper).)

</details>

**5. يقترح يوسف تهيئة Terraform واحدة (one Terraform configuration) بمساحات عمل (workspaces) تُسمّى dev وstaging وprod، تُختار من سطر الأوامر (command line). ما مصدر القلق الرئيسي (main concern)؟**

- A. لا تدعم أيّ واجهة تخزين خلفية بعيدة (remote backend) مساحات العمل، لذا يجب أن تبقى الحالة محلية (local)
- B. تُجبر مساحات العمل كل البيئات على مشاركة ملف حالة واحد، فيُقفلها كل تطبيق (apply) جميعًا
- C. البيئة المستهدفة (target environment) مخفية في إعداد سطر أوامر، ما يسهّل التطبيق الخاطئ (wrong applies)
- D. لا تعمل مساحات العمل إلا مع مزوّدات Kubernetes (Kubernetes providers)، لا مع قواعد البيانات أو الشبكات السحابية

<details><summary>الإجابة</summary>

**C.** تحتفظ مساحات العمل (Workspaces) بحالات منفصلة (separate states) لكنها تجعل البيئة المستهدفة ضمنية (implicit). أما المجلدات لكل بيئة بواجهتها الخلفية (backend) وبيانات اعتمادها (credentials) الخاصة فتجعل الهدف مرئيًا (visible) وتحدّ مما يمكن أن يطاله الخطأ. الخيار B خاطئ: لكل مساحة عمل حالتها الخاصة (own state). (🔴 نظرة الخبير (Expert view).)

</details>

## 📚 المراجع
- مبادئ OpenGitOps (OpenGitOps principles) — https://opengitops.dev/
- توثيق Argo CD (Argo CD documentation) — https://argo-cd.readthedocs.io/
- توثيق Flux (Flux documentation) — https://fluxcd.io/flux/
- توثيق Kustomize (Kustomize documentation) (Kubernetes) — https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
- التطبيق ذو العوامل الاثني عشر، العامل العاشر: تكافؤ التطوير والإنتاج (X. Dev/prod parity) — https://12factor.net/dev-prod-parity
- هيئة الأوراق المالية والبورصات الأمريكية (US SEC)، الأمر في قضية Knight Capital Americas LLC (2013) — https://www.sec.gov/
- External Secrets Operator — https://external-secrets.io/
- مشاريع CNCF (CNCF projects) — https://www.cncf.io/projects/

---

# 3.3 — السياسة بوصفها شيفرة والانحراف والحواجز الواقية
*المستوى: 🟡 متوسط* · *المتطلبات: 3.1، 3.2* · *المرحلة: Test, Operate*

## ⚡ الدرس في دقيقة (In 60 seconds)
- تكتب **السياسة بوصفها شيفرة (policy as code)** قواعد مثل "لا قاعدة بيانات مفتوحة على الإنترنت" أو "لكل مورد وسم مالك" في صورة شيفرة تفحصها أداة آليًا، عند كل تغيير، وبالطريقة نفسها في كل مرة.
- افحص على طبقات: في **طلب السحب (pull request)** (ماسحات البنية التحتية بوصفها شيفرة)، وفي **وقت التخطيط (plan time)** (سياسات على الخطة)، وعند **القبول (admission)** في Kubernetes، وعلى مستوى **المؤسسة (organisation)** في السحابة، و**أثناء التشغيل (at runtime)** (رصد الانحراف والتهيئة).
- **الانحراف (Drift)** هو أي اختلاف بين الشيفرة وما يعمل فعلًا. اكتشفه وفق جدول زمني، ثم إما أن تعيد الواقع إلى الشيفرة أو تحدّث الشيفرة لتطابقه، ولا تتركه أبدًا دون تفسير (unexplained).
- فضّل **الحواجز الواقية (guardrails)** التي لا تمنع إلا ما هو خطر حقًّا (truly dangerous) وتشرح كيف تصلحه، على البوابات التي تمنع كل شيء وتعلّم الناس الالتفاف عليها (bypass them).
- اطرح السياسات الجديدة (new policies) في وضع التحذير (warn mode)، وقِس، ثم افرضها (enforce). ولكل استثناء (exception) مالك (owner) وسبب (reason) وتاريخ انتهاء (expiry date).
- الفخ الأكبر: سياسة لا يستطيع أحد اختبارها أو فهمها أو الحصول على استثناء منها. فينتهي بها الأمر إلى التعطيل (disabled).

## 🧭 لماذا يهم
في 28 فبراير 2017 تعطّلت خدمة Amazon S3 في منطقة شرق الولايات المتحدة (فرجينيا الشمالية) (US East (Northern Virginia) region) لعدة ساعات. ويشرح الملخّص العلني (public summary) من AWS أن مهندسًا، باتّباعه دليل تشغيل معتمدًا (established playbook)، شغّل أمرًا يُقصد به إزالة عدد صغير من الخوادم من نظام فرعي للفوترة (billing subsystem)، وأُدخل أحد المُدخلات خطأً (entered incorrectly). فأُزيلت مجموعة أكبر بكثير من الخوادم، بينها خوادم تدعم أنظمة فرعية حرجة أخرى (other critical S3 subsystems) في S3، احتاجت بعدها إلى إعادة تشغيل كاملة (full restart). وفشلت معها خدمات كثيرة تعتمد على S3. ولم تكن استجابة AWS أن تطلب من المهندسين الكتابة بعناية أكبر. بل غيّروا الأداة لتزيل السعة (capacity) ببطء أكبر وترفض إنزال أي نظام فرعي إلى ما دون الحد الأدنى من السعة المطلوبة.

سيخطئ الناس والوكلاء؛ وينبغي للنظام أن يجعل الأخطاء الخطرة (dangerous ones) مستحيلة أو صاخبة. لقد اكتُشفت إعادة تسمية يوسف لقاعدة البيانات في الدرس 3.1 لأن مها قرأت الخطة؛ ويسأل سالم عمّا يحدث في اليوم الذي يكون فيه المراجع متعبًا. وقد وجد فريق نورة للتو قاعدة بيانات اختبار (test database) تسمح قاعدة الشبكة (network rule) فيها بحركة المرور من أي مكان، أُنشئت قبل أشهر في وحدة التحكم، ولم تكن في الشيفرة قط. ولم يلاحظ شيءٌ ذلك، لأن لا شيء كان يقارن الواقع بالشيفرة.

## 📐 كيف يعمل
### 🟢 الأساسيات
**من قوائم التحقق إلى الشيفرة (From checklists to code).** المعيار المكتوب في ملف PDF ("يجب ألّا تكون قواعد البيانات قابلة للوصول العام (publicly reachable)") يعتمد على تذكّر الناس له. أما **السياسة بوصفها شيفرة (policy as code)** فتحوّل القاعدة إلى برنامج يأخذ تغييرًا مقترحًا (proposed change) ويُعيد "سماح (allow)" أو "رفض، لأن… ⁦(deny, because…)⁩"، عند كل تغيير، في ثوانٍ، وبالطريقة نفسها للجميع. والقاعدة نفسها تُراجَع وتُدار إصداراتها مثل أي شيفرة أخرى.

**أين تعمل السياسات (Where policies run).** لا يرى فحص واحد (single check) كل شيء، ولذلك يفحص بنك نجم عند عدة نقاط:

| الطبقة (Layer) | ما تراه | أدوات على سبيل المثال (Example tools) | قاعدة على سبيل المثال (Example rule) |
|---|---|---|---|
| **طلب السحب (Pull request)** | ملفات البنية التحتية بوصفها شيفرة والبيانات الوصفية | Checkov، Trivy، KICS | لا حاوية تخزين (storage bucket) ذات وصول عام (public access) |
| **وقت التخطيط (Plan time)** | الخطة المحسوبة (computed plan): ما الذي سيتغيّر فعلًا | Conftest مع OPA، وميزات السياسات في HCP Terraform | لا خطة تحذف قاعدة بيانات إنتاجية؛ ولا منفذ قاعدة بيانات (database port) مفتوح على 0.0.0.0/0 |
| **القبول في Kubernetes (Kubernetes admission)** | كل كائن يُرسَل إلى خادم واجهة برمجة التطبيقات (API server) في العنقود | Kyverno، OPA Gatekeeper، ValidatingAdmissionPolicy | الصور من سجل البنك (bank's registry) فقط، مثبّتة بالبصمة (pinned by digest) |
| **المؤسسة السحابية (Cloud organisation)** | كل استدعاء لواجهة برمجة التطبيقات (API call) في حساب ما، أيًّا كانت الأداة التي أجرته | سياسات التحكم بالخدمات في AWS، وAzure Policy، وسياسة المؤسسة في Google Cloud | لا موارد خارج المناطق المعتمدة (approved regions) |
| **وقت التشغيل (Runtime)** | ما هو موجود فعلًا الآن | اكتشاف الانحراف المجدوَل، وحالة مزامنة Argo CD، وخدمات رصد التهيئة السحابية | التنبيه (Alert) عندما يختلف الواقع عن الشيفرة |

كلما جرى الفحص أبكر، كان الإصلاح أرخص. وكلما جرى متأخرًا، التقط أكثر، بما في ذلك التغييرات التي لم تمرّ قط عبر خط التسليم.

```mermaid
flowchart RL
    A["تغيير في طلب سحب<br/>(Change in a PR)"] --> B["فحص البنية التحتية بوصفها شيفرة<br/>(IaC scan)"]
    B --> C["سياسة وقت التخطيط<br/>(Plan-time policy)"]
    C --> D["التطبيق أو المزامنة<br/>(Apply or sync)"]
    D --> E["سياسات القبول والمؤسسة<br/>(Admission and org policies)"]
    E --> F["الموارد العاملة<br/>(Running resources)"]
    F --> G["فحص الانحراف المجدول<br/>(Scheduled drift check)"]
    G -->|"وُجد اختلاف (difference found)"| H["الإرجاع أو تحديث الشيفرة<br/>(Revert or update code)"]
```

**ما هو الانحراف (What drift is).** **الانحراف (Drift)** هو أي اختلاف بين الحالة المُصرَّح بها في الشيفرة والحالة الحقيقية (real state). وهو ينشأ من تغييرات وحدة التحكم (console changes) ("ClickOps")، والتعديلات اليدوية أثناء الحوادث، والأدوات الأخرى التي تلمس الموارد نفسها، والموارد التي تُنشأ خارج البنية التحتية بوصفها شيفرة كليًا. وهو خطر لأن إعادة البناء من الشيفرة لم تعد تمنحك النظام نفسه، ولأن التطبيق التالي (next apply) قد يلغي بصمت إصلاحًا مقصودًا (deliberate fix)، ولأن الإعداد المنحرف (drifted setting) قد يكون الثغرة التي يستغلّها مهاجم (attacker).

**الحواجز الواقية مقابل البوابات (Guardrails versus gates).** **البوابة (gate)** توقف كل شيء حتى يوافق أحدهم. أما **الحاجز الواقي (guardrail)** فيدع الناس يتحرّكون بسرعة ولا يوقف إلا الحالات الخطرة (dangerous cases)، مع رسالة تقول كيف تصلحها. وتفضّل هندسة المنصات (platform engineering) الحواجز الواقية: فالمسار الآمن (الوحدة البرمجية `postgres` من 3.1، وطلب سحب الترقية من 3.2) ينبغي أن يكون أيضًا المسار الأسهل (easiest path)، والسياسات تلتقط ما يسقط عنه.

### 🟡 التعمق أكثر
**سياسة وقت التخطيط باستخدام OPA وConftest (Plan-time policy with OPA and Conftest).** **Open Policy Agent (OPA)** محرّك سياسات عام الأغراض، وهو مشروع متخرّج في CNCF، بلغة سياسات (policy language) تُسمّى **Rego**. ويشغّل **Conftest** سياسات Rego على ملفات منظّمة (structured files) مثل JSON أو YAML. ويستطيع Terraform وOpenTofu تصدير خطة محفوظة بصيغة JSON، فتستطيع كتابة قواعد حول ما سيتغيّر، لا حول ما تقوله الملفات فحسب:

```shell
tofu plan -out=tfplan
tofu show -json tfplan > tfplan.json
conftest test tfplan.json --policy policy/
```

قاعدة تمنع فتح PostgreSQL على الإنترنت كله (مثال من AWS؛ والفكرة نفسها تنطبق على مجموعات أمان الشبكة في Azure أو قواعد جدار الحماية في Google Cloud):

```rego
package main

import rego.v1

deny contains msg if {
  some rc in input.resource_changes
  rc.type == "aws_security_group_rule"
  rc.change.after.type == "ingress"
  "0.0.0.0/0" in rc.change.after.cidr_blocks
  rc.change.after.from_port <= 5432
  rc.change.after.to_port >= 5432
  msg := sprintf("%s opens PostgreSQL to the internet; use the private endpoint from the postgres module", [rc.address])
}

deny contains msg if {
  some rc in input.resource_changes
  "delete" in rc.change.actions
  rc.type in {"aws_db_instance", "aws_rds_cluster"}
  msg := sprintf("%s would be deleted; deleting a database needs a platform-lead approved exception", [rc.address])
}
```

كل رسالة تقول ما الخطأ *وكذلك* ما العمل. تغيّرت صياغة Rego (Rego syntax) بين إصدارات OPA؛ و`import rego.v1` يجعل هذا صالحًا على إصدارات 0.x بدءًا من 0.59 وعلى OPA 1.x. وقد تستخدم شيفرة AWS الأحدث `aws_vpc_security_group_ingress_rule`، الذي يحتاج إلى قاعدة خاصة به.

**السياسات شيفرة، فاختبرها (Policies are code, so test them).** لدى OPA مشغّل اختبارات مدمج (`opa test`)، ويستطيع Conftest أيضًا تشغيل حالات اختبار (test cases). احتفظ لكل قاعدة بمثال واحد على الأقل يجب أن يُرفض ومثال يجب أن يُسمح به. فالسياسة غير المختبرة ستمنع يومًا ما كل عمليات النشر (every deployment)، أو لن تمنع أيًّا منها.

**سياسات القبول في Kubernetes (Admission policies in Kubernetes).** حتى مع خطوط تسليم مثالية (perfect pipelines)، يظل بوسع أحدهم تشغيل `kubectl apply`. يفحص **متحكّم القبول (admission controller)** كل كائن يتلقّاه خادم واجهة برمجة التطبيقات ويستطيع رفضه. يكتب **Kyverno** السياسات بلغة YAML الخاصة بـ Kubernetes (Kubernetes YAML)؛ ويستخدم **OPA Gatekeeper** لغة Rego؛ ويوفّر Kubernetes نفسه الآن **ValidatingAdmissionPolicy**، باستخدام لغة التعبيرات CEL، التي أصبحت متاحة للعموم (generally available) في Kubernetes 1.30. قاعدة Kyverno تشترط تثبيت الصور بالبصمة (images pinned by digest):

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-image-digest
spec:
  validationFailureAction: Audit   # start in Audit, move to Enforce after review
  rules:
    - name: images-pinned-by-digest
      match:
        any:
          - resources:
              kinds: ["Pod"]
      validate:
        message: "Pin images by digest (image@sha256:...), as the promotion pipeline does."
        pattern:
          spec:
            containers:
              - image: "*@sha256:*"
```

تتّجه إصدارات Kyverno الحديثة إلى نقل إجراء الإخفاق (failure action) إلى كل قاعدة على حدة؛ تحقّق من أسماء الحقول (field names) في إصدارك.

**اكتشاف الانحراف (Detecting drift).** في البنية التحتية بوصفها شيفرة، أبسط كاشف (simplest detector) هو خطة مجدوَلة (scheduled plan) ينبغي ألّا تُظهر شيئًا:

```shell
tofu plan -detailed-exitcode -input=false
# exit code 0: no changes, code and reality match
# exit code 2: changes pending: drift, or merged code that was never applied
# exit code 1: error
```

يشغّل بنك نجم هذا كل ليلة (nightly) لكل حالة (every state) ببيانات اعتماد للقراءة فقط (read-only credentials) ويفتح تذكرة عند رمز الخروج (exit code) 2. ويُظهر `plan -refresh-only` ما تغيّر في الواقع فقط، وهذا يساعدك على فهم الانحراف (understand drift) قبل التصرّف. وفي Kubernetes، يُبلغ Argo CD وFlux عن الانحراف بحالة "OutOfSync"، ويستطيع الإصلاح الذاتي إلغاءه. كما تلتقط خدمات رصد التهيئة السحابية (مثل AWS Config، وامتثال Azure Policy، وGoogle Cloud Security Command Center) الموارد التي لم تعرف عنها البنية التحتية بوصفها شيفرة قط.

**الاستجابة للانحراف (Responding to drift).** كل بند انحراف (drift item) يحصل على إحدى إجابتين:
- **الإرجاع (Revert)**: كانت الشيفرة محقّة؛ طبّقها مجددًا واكتشف من غيّر الواقع ولماذا.
- **التبنّي (Adopt)**: كان التغيير محقًّا (غالبًا إصلاح حادثة)؛ حدّث الشيفرة عبر طلب سحب كي تتطابق الشيفرة والواقع، ثم أغلق التذكرة.

لا تترك الانحراف أبدًا بوصفه "معروفًا (known)". وإن كانت سمة (attribute) ما تتغيّر خارج البنية التحتية بوصفها شيفرة على نحو مشروع (legitimately)، مثل عدد النسخ المتماثلة (replica count) الذي يديره موسِّع تلقائي (autoscaler)، فصرّح بذلك صراحةً باستخدام `lifecycle { ignore_changes = [...] }` لتلك السمة وحدها، مع تعليق (comment) يشرح السبب.

### 🔴 نظرة الخبير
**طرح سياسة دون تمرّد (Rolling out a policy without a revolt).** ابدأ في وضع التحذير أو التدقيق، وقِس ما سيفشل، وأصلحه أو استثنِه، وأعلن تاريخًا، ثم افرض. انشر كل سياسة بمعرّف (ID)، وسبب، ومثال ممتثل (compliant example)، ومالك. وتتبّع عدد مرات انطلاق كل سياسة، وعدد مرات انطلاقها خطأً: فالإيجابيات الكاذبة (false positives) تعلّم الناس تجاهل كل سياسة.

**الاستثناءات جزء من التصميم (Exceptions are part of the design).** تحتاج الأنظمة الحقيقية إلى استثناءات (exceptions): جهاز مورّد (vendor appliance) يجب أن يستخدم منفذًا بعينه، أو عملية ترحيل (migration) تحذف قاعدة بيانات على نحو مشروع. اجعل مسار الاستثناء (exception path) صريحًا: ملف استثناءات (exception file) في مستودع السياسات (policy repo)، يوافق عليه مالك السياسة (policy owner)، مع سبب وتاريخ انتهاء، وتقرؤه السياسة. والاستثناءات المنتهية (Expired exceptions) تُفشل البناء (fail the build). وهذا أفضل من الفحوص المعطّلة (disabled checks) أو صلاحية المسؤول (admin access).

**الحواجز الواقية على مستوى المؤسسة (Organisation-level guardrails).** تنطبق سياسات التحكم بالخدمات في AWS، وAzure Policy على مستوى مجموعة الإدارة (management-group level)، وسياسات المؤسسة في Google Cloud على كل حساب أو مشروع تحتها، أيًّا كان من يُجري الاستدعاء. استخدمها لقائمة قصيرة من الأمور غير القابلة للتفاوض (non-negotiables) (المناطق المعتمدة لإقامة البيانات، وتسجيل التدقيق مُفعَّل دائمًا، ولا تخزين عام افتراضيًا)؛ فهي صعبة التصحيح وتؤثّر في الجميع.

**كسر الزجاج على الوجه الصحيح (Break-glass, done properly).** سيأتي يوم يتعطّل فيه خط التسليم ويتعيّن على أحدهم تغيير الإنتاج يدويًا. خطّط لذلك: أدوار كسر زجاج مسمّاة، وبيانات اعتماد مخزّنة على حدة، واستخدام يستدعي (pages) قائد هندسة موثوقية المواقع (SRE lead) والأمن (security)، وتذكرة إلزامية (mandatory ticket)، واكتشاف انحراف يُعلِّم التغيير حتى يصبح في الشيفرة. خطّط لمسار الطوارئ (emergency path) قبل الطوارئ.

**السياسة والتنظيم (Policy and regulation).** تترك السياسة بوصفها شيفرة أدلّة يقدّرها المدقّقون (auditors): القاعدة، وتاريخها، وكل تقييم (evaluation) واستثناء. وهذا يدعم توقّعات إدارة التغيير (change-management expectations) مثل توقّعات قانون EU DORA ومتطلبات الجهات التنظيمية الخليجية للسحابة؛ راجع النصوص الحالية مع فريق الامتثال (compliance). أما أيّ أخطاء التهيئة (misconfigurations) أهم فيتناوله [*أمن الذكاء الاصطناعي والتطبيقات*، الدرس 7.1 — أمن السحابة: المسؤولية المشتركة وإدارة الهوية والوصول وأخطاء التهيئة](../secai/index.ar.html#/7.1) و[*أمن الذكاء الاصطناعي والتطبيقات*، الدرس 7.2 — الحاويات وKubernetes والبنية التحتية بوصفها شيفرة](../secai/index.ar.html#/7.2).

## 🧰 الأدوات
| الأداة أو الممارسة أو الخدمة | ما هي وماذا تفعل | متى تلجأ إليها |
|---|---|---|
| **Open Policy Agent** (OPA، متخرّج في CNCF) | محرّك سياسات عام الأغراض بلغة Rego؛ يستطيع تقييم أي مُدخل JSON | سياسات البنية التحتية بوصفها شيفرة في وقت التخطيط، وتفويض واجهات برمجة التطبيقات (API authorisation)، ولغة سياسات واحدة عبر أنظمة كثيرة |
| **Conftest** | يشغّل سياسات Rego على ملفات التهيئة (configuration files) وملف JSON للخطة (plan JSON) في التكامل المستمر | فحص خطط OpenTofu أو Terraform وبيانات Kubernetes الوصفية في خط تسليم |
| **Kyverno** (CNCF) | محرّك قبول وسياسات أصيل في Kubernetes؛ تُكتب السياسات بلغة YAML | فرض قواعد العنقود (cluster rules) مثل السجل وتثبيت البصمة (digest pinning) وحدود الموارد (resource limits) |
| **ValidatingAdmissionPolicy** | فحوص قبول مدمجة مكتوبة بلغة CEL، دون حاجة إلى متحكّم إضافي (extra controller) | قواعد تحقّق بسيطة حين لا تريد مكوّنات إضافية (extra components) |
| **IaC scanner** — ماسح البنية التحتية بوصفها شيفرة | فحوص ثابتة (static checks) على ملفات البنية التحتية بوصفها شيفرة والبيانات الوصفية (manifests) بحثًا عن أخطاء تهيئة معروفة (known misconfigurations) | كل طلب سحب يلمس البنية التحتية |
| **Scheduled drift detection** — اكتشاف الانحراف المجدوَل | تشغيل ليلي لـ `plan -detailed-exitcode` لكل حالة (per state)، إضافةً إلى حالة مزامنة GitOps | كل بيئة مُدارة (managed environment)؛ تذاكر لأي اختلاف غير مفسَّر (unexplained difference) |
| **Organisation guardrails** — الحواجز الواقية للمؤسسة | قواعد تُفرض على كل استدعاء لواجهة برمجة التطبيقات (every API call) داخل تسلسل هرمي للحسابات (account hierarchy) | قائمة قصيرة من القواعد غير القابلة للتفاوض (non-negotiable rules) مثل المناطق المعتمدة وتسجيل التدقيق (audit logging) |

## 🏛️ عمليًا في بنك نجم
ينشر سالم ونورة **دليل نجم للحواجز الواقية للمنصة، الإصدار 1 (Najm Platform Guardrail Catalogue v1)**. لكل حاجز واقٍ معرّف، ومكان تشغيله (where it runs)، ووضعه (mode)، ومسار الاستثناء (exception route) الخاص به.

**الجزء أ: الحواجز الواقية (Part A: guardrails)**

| المعرّف | القاعدة (Rule) | أين تعمل | الوضع | مسار الاستثناء |
|---|---|---|---|---|
| G-01 | الموارد في المناطق المعتمدة فقط | سياسة المؤسسة (Organisation policy) | فرض | حمد (كبير مسؤولي أمن المعلومات (CISO)) والامتثال، كتابيًا (written) |
| G-02 | لا منفذ قاعدة بيانات مفتوح على 0.0.0.0/0 | Conftest في وقت التخطيط (Plan-time Conftest)؛ فحص البنية التحتية بوصفها شيفرة (IaC scan) | فرض | لا يوجد (None) |
| G-03 | لا حذف أو استبدال لمورد ذي حالة في الإنتاج دون موافقة | Conftest في وقت التخطيط | فرض | سالم أو مها، لكل تغيير (per change)، وينتهي بعد تطبيق واحد |
| G-04 | الوسوم المطلوبة (Required tags): `owner`، `environment`، `data-class`، `cost-centre` | Conftest في وقت التخطيط | تحذير حتى نهاية الربع، ثم فرض | فريق المنصة، 30 يومًا |
| G-05 | الصور من سجل البنك (bank registry)، مثبّتة بالبصمة | قبول Kyverno (Kyverno admission) | فرض في الإنتاج، وتدقيق في التطوير | فريق المنصة، 14 يومًا |
| G-06 | طلبات المعالج والذاكرة مضبوطة على كل حاوية | قبول Kyverno | فرض | لا يوجد |
| G-07 | لا يمكن تعطيل تسجيل التدقيق | سياسة المؤسسة | فرض | لا يوجد |
| G-08 | لا انحراف غير مفسَّر | خطة ليلية لكل حالة؛ حالة مزامنة Argo CD | تذكرة خلال يوم عمل واحد | الحلّ بالإرجاع أو التبنّي |

**الجزء ب: دليل تشغيل الانحراف (Part B: the drift runbook)**
1. تجد المهمة الليلية (nightly job) رمز الخروج 2 وتفتح تذكرة مرفقًا بها مُخرج الخطة (plan output).
2. يفحص الفريق المالك سجلّ التدقيق السحابي لمعرفة من غيّر ماذا، ومتى.
3. قرِّر: **الإرجاع (revert)** (طبّق الشيفرة) أو **التبنّي (adopt)** (طلب سحب لتغيير الشيفرة). وسجّل القرار في التذكرة.
4. إن أُجري التغيير خارج كسر الزجاج (outside break-glass)، فأضف ملاحظة قصيرة إلى مراجعة المنصة الأسبوعية؛ فالانحراف المتكرّر على المورد نفسه يعني أن حاجزًا واقيًا أو وحدة برمجية مفقودة.

**الجزء ج: قواعد مستودع السياسات (Part C: policy repository rules).** لكل سياسة اختبارات لحالة مسموحة (allowed) واحدة على الأقل وحالة مرفوضة (denied) واحدة؛ وتمرّ التغييرات على السياسات عبر طلبات سحب (pull requests) يراجعها فريق المنصة، ويراجعها فريق نورة أيضًا في القواعد الأمنية (security rules)؛ وتعيش الاستثناءات في `exceptions.yaml` مع المالك والسبب وتاريخ الانتهاء (expiry)، والمدخلات المنتهية (expired entries) تُفشل البناء.

## 🛠️ التمارين
شغّل هذه التمارين محليًا باستخدام OpenTofu وConftest وعنقود kind أو k3d.

- 🟢 باستخدام تهيئة مزوّد Docker (Docker-provider configuration) من الدرس 3.1، شغّل `plan -detailed-exitcode` ولاحظ رمز الخروج. ثم أوقف الحاوية أو أعد تسميتها يدويًا باستخدام واجهة سطر أوامر Docker (Docker CLI) وشغّله مجددًا. *يكتمل عندما:* ترى رمز الخروج 0 قبل ذلك و2 بعده، وتستطيع أن تشرح من مُخرج الخطة ما الذي تقترح الأداة إعادته.
- 🟡 اكتب سياسة Conftest (Conftest policy) على ملف JSON للخطة تمنع أي `docker_container` يكشف منفذًا خارجيًا أقل من 1024، وأخرى تمنع أي وسم صورة (image tag) `latest`. واكتب اختبارات للاثنتين. *يكتمل عندما:* يفشل `conftest test` على خطة تخالف كل قاعدة برسالة تقول كيف تصلحها، وينجح على خطة ممتثلة (compliant plan)، وتنجح اختبارات سياستك (policy tests).
- 🔴 ثبّت Kyverno على عنقود محلي وطبّق سياسة تشترط تثبيت الصور بالبصمة، أولًا في وضع التدقيق (Audit)، ثم في وضع الفرض. انشر حجيرة (pod) بالوسم وأخرى بالبصمة في كل وضع، واقرأ تقارير السياسة (policy reports). ثم أضف استثناءً لفضاء أسماء (namespace) واحد مع ملاحظة انتهاء (expiry note) في مستودعك. *يكتمل عندما:* يُبلَّغ عن الحجيرة الموسومة (tagged pod) في وضع التدقيق، وتُرفض في وضع الفرض برسالتك، وتعمل الحجيرة المثبّتة بالبصمة (digest-pinned pod)، ويكون استثناؤك محصورًا في فضاء أسماء واحد وموثّقًا (documented).

## ⚠️ أخطاء وفخاخ
- **فحص واحد عند نقطة واحدة (One check, at one point).** فحص طلب السحب (pull-request scan) يفوته تغييرات وحدة التحكم؛ وسياسة المؤسسة يفوتها Kubernetes. اجعل الفحوص طبقات.
- **الفرض من اليوم الأول (Enforcing on day one).** السياسة الجديدة التي تكسر كل خط تسليم تُعطَّل. دقّق أولًا (Audit first)، وأصلح أو استثنِ، ثم افرض في تاريخ معلَن (announced date).
- **رسائل لا تقول إلا "مرفوض" (Messages that only say "denied").** يحتاج الناس إلى معرفة كيف يصلحون الأمر. كل رسالة سياسة (policy message) تسمّي المشكلة والبديل الممتثل (compliant alternative).
- **استثناءات بلا تاريخ انتهاء (Exceptions with no expiry).** تصبح ثغرات دائمة (permanent holes). امنح كلًّا منها مالكًا وسببًا وتاريخ نهاية (end date) يفرضه البناء (build).
- **تجاهل الانحراف أو "إصلاحه" بتطبيق أعمى (Ignoring drift or "fixing" it with a blind apply).** قد يلغي التطبيق إصلاحًا مقصودًا لحادثة. تحقّق أولًا، ثم أرجِع أو تبنَّ (revert or adopt)، وسجّل أيّهما.
- **سياسات غير مختبرة (Untested policies).** خطأ مطبعي (typo) قد يسمح بكل شيء أو يمنع كل شيء. احتفظ بحالات اختبار مسموحة ومرفوضة لكل قاعدة.

## 🧾 الخلاصة
- تحوّل السياسة بوصفها شيفرة المعايير المكتوبة (written standards) إلى فحوص آلية ومُدارة الإصدارات وقابلة للاختبار عند كل تغيير.
- اجعل الفحوص طبقات: طلب السحب، ووقت التخطيط، والقبول في Kubernetes، والمؤسسة السحابية، ووقت التشغيل.
- الانحراف هو أي فجوة بين الشيفرة والواقع؛ اكتشفه وفق جدول زمني وعالج كل بند بالإرجاع أو التبنّي.
- الحواجز الواقية لا تمنع إلا الخطر الحقيقي (real danger)، وتشرح الإصلاح، وتُطرح في وضع التدقيق أولًا، ولها مسار استثناء صريح ينتهي.
- خطّط لوصول كسر الزجاج (break-glass access) قبل أن تحتاج إليه، ودع اكتشاف الانحراف يعيد تغييرات الطوارئ (emergency changes) إلى الشيفرة.

## ✍️ اختبر نفسك

**1. كانت استجابة AWS لانقطاع S3 في فبراير 2017 (February 2017 S3 outage)، الذي سبّبه أمر كُتب خطأً (mistyped command)، في الأساس:**

- A. اشتراط أن يفحص مهندس ثانٍ (second engineer) كل أمر ويؤكّده قبل تشغيله
- B. التوقّف عن استخدام أدلّة التشغيل المكتوبة (written playbooks) وترك المهندسين يقرّرون الخطوات أثناء العمليات (during operations)
- C. نقل S3 نهائيًا إلى منطقة أخرى (another region) فيها خدمات معتمدة أقل
- D. تغيير الأداة لتزيل السعة (capacity) ببطء، ولا تنزل أبدًا دون الحد الأدنى لنظام فرعي

<details><summary>الإجابة</summary>

**D.** الدرس هو بناء الحواجز الواقية داخل الأدوات، كي لا يتحوّل الخطأ إلى كارثة (disaster). الخيار A يعتمد على أن يكون الناس مثاليين، وهي المشكلة التي تحلّها الحواجز الواقية. (🧭 لماذا يهم.)

</details>

**2. يجد فريق نورة قاعدة بيانات اختبار (test database) تسمح قاعدة الشبكة (network rule) فيها بحركة المرور من أي مكان. أُنشئت في وحدة التحكم (console) ولم تظهر في أي طلب سحب (pull request). أيّ طبقة فحص (layer of checking) كان يمكن أن تلتقطها؟**

- A. ماسح بنية تحتية بوصفها شيفرة (IaC scanner) يعمل آليًا على كل طلب سحب للبنية التحتية في التكامل المستمر (CI)
- B. سياسات المؤسسة (Organisation policies) ورصد التهيئة في وقت التشغيل، اللذان يريان كل تغيير
- C. سياسة قبول Kyverno في عنقود Kubernetes الإنتاجي
- D. مراجعة شيفرة دقيقة لمستودع التطبيق (application repository)

<details><summary>الإجابة</summary>

**B.** التغييرات التي تُجرى خارج خط التسليم لا تراها إلا الضوابط (controls) المفروضة على واجهة برمجة التطبيقات السحابية نفسها أو على الموارد العاملة (running resources). الخياران A وD لا يريان إلا الشيفرة؛ والخيار C لا يرى إلا كائنات Kubernetes (Kubernetes objects). (🟢 الأساسيات.)

</details>

**3. تشغّل مهمة الانحراف الليلية (nightly drift job) الأمر `tofu plan -detailed-exitcode` لحالة قاعدة بيانات المدفوعات (Payments database state) وتحصل على رمز الخروج (exit code) 2. ماذا يعني هذا، وما أول ما ينبغي للفريق فعله؟**

- A. انحراف (Drift) أو شيفرة مدموجة غير مُطبَّقة؛ تحقّق، ثم أرجِع أو تبنَّ (revert or adopt)
- B. فشلت الخطة بخطأ (error)، فأعد تشغيلها مع تفعيل تسجيل أكثر تفصيلًا
- C. كل شيء متطابق (everything matches)، فلا حاجة إلى أي إجراء حتى تشغيل الغد (tomorrow's run)
- D. شغّل `apply` فورًا (immediately) لتكتب فوق (overwrite) كل ما تغيّر في الواقع منذ التشغيل الأخير (last run)

<details><summary>الإجابة</summary>

**A.** رمز الخروج 2 يعني أن هناك تغييرات معلّقة. والخيار D قد يلغي إصلاحًا مقصودًا لحادثة؛ تحقّق أولًا، ثم أرجِع أو تبنَّ. الخيار B هو رمز الخروج 1، والخيار C هو رمز الخروج 0. (🟡 التعمق أكثر (Going deeper).)

</details>

**4. يريد سالم اشتراط تثبيت الصور بالبصمة (images pinned by digest) في كل عنقود (cluster). كثير من أعباء العمل القائمة (existing workloads) تستخدم الوسوم (tags). ما أفضل طريقة للطرح (best rollout)؟**

- A. الفرض فورًا (Enforce immediately) في كل عنقود كي تتعلّم كل الفرق القاعدة بسرعة
- B. إعلان القاعدة بالبريد الإلكتروني لكل الفرق وعدم فرضها
- C. التدقيق أولًا (Audit first)، وإصلاح أعباء العمل القائمة أو استثناؤها، وإعلان تاريخ، ثم الفرض
- D. تعطيل التحكم بالقبول (admission control) والاعتماد على مراجعة شيفرة دقيقة بدلًا منه

<details><summary>الإجابة</summary>

**C.** التدقيق أولًا (Audit first) يتيح لك إيجاد المخالفات القائمة (existing violations) وإصلاحها دون كسر عمليات النشر (deployments). الخيار A يكسر خطوط تسليم كثيرة ويستدعي الالتفاف (invites bypassing)؛ والخيار B لا أثر له. (🔴 نظرة الخبير (Expert view).)

</details>

**5. يحتاج جهاز مورّد (vendor appliance) في بنك نجم (Najm Bank) على نحو مشروع إلى قاعدة يرفضها دليل الحواجز الواقية (guardrail catalogue) عادةً. ما الطريقة الصحيحة للسماح بها؟**

- A. تعطيل السياسة للجميع حتى ينتهي مشروع المورّد (vendor project) العام المقبل أو بعده
- B. منح فريق المورّد صلاحية المسؤول (administrator access) كي يتجاوزوا خط التسليم (pipeline)
- C. إجراء التغيير يدويًا في وحدة التحكم (console) وتجاهل تنبيهات الانحراف (drift alerts) التي يسبّبها
- D. إضافة استثناء محصور (scoped exception) بمالك وسبب وتاريخ انتهاء، يفرضه البناء (build)

<details><summary>الإجابة</summary>

**D.** الاستثناءات الصريحة المحصورة المنتهية تُبقي الحاجز الواقي (guardrail) قائمًا للجميع غيرهم وتحفظ دليلًا على القرار. أما الخيارات A وB وC فكلها تزيل الحماية على نطاق أوسع بكثير مما يلزم ولا تترك سجلًا نظيفًا (clean record). (🔴 نظرة الخبير (Expert view)، و🏛️ عمليًا.)

</details>

## 📚 المراجع
- توثيق Open Policy Agent — https://www.openpolicyagent.org/docs/
- Conftest — https://www.conftest.dev/
- توثيق Kyverno (Kyverno documentation) — https://kyverno.io/docs/
- Kubernetes، سياسة القبول التحقّقية — https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/
- OpenTofu، أمر plan (plan command) — https://opentofu.org/docs/cli/commands/plan/
- Terraform، اكتشاف الانحراف ووضع التحديث فقط — https://developer.hashicorp.com/terraform/docs
- AWS، ملخّص تعطّل خدمة Amazon S3 في منطقة فرجينيا الشمالية (summary of the Amazon S3 service disruption in the Northern Virginia (US-EAST-1) region) — https://aws.amazon.com/message/41926/
- AWS Organizations، سياسات التحكم بالخدمات — https://docs.aws.amazon.com/organizations/
- توثيق Azure Policy — https://learn.microsoft.com/azure/governance/policy/
- Google Cloud، خدمة سياسات المؤسسة — https://cloud.google.com/resource-manager/docs
