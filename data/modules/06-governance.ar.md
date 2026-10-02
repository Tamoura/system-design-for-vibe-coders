# الوحدة 6 — الحوكمة والخصوصية والأمن (Governance, privacy and security)

*منصة البيانات التي تعمل (a data platform that works) ليست بعدُ منصة بيانات يثق بها الناس (a data platform people can trust). فالثقة تحتاج إلى ثلاثة أمور أخرى: أن يعرف الجميع من يملك كل مجموعة بيانات (who owns each dataset) وماذا تعني، وأن تُعامَل البيانات الشخصية (personal data) بالطريقة التي يتوقعها القانون والعميل (the law and the customer)، وألّا يصل إلى البيانات الصحيحة إلا الأشخاص الصحيحون (only the right people can reach the right data)، مع سجلّ بمن فعل ذلك (a record of who did). تحوّل هذه الوحدة تلك الاحتياجات الثلاثة إلى عمل هندسي (engineering work) يمكنك بناؤه واختباره وعرضه على المدقق (show to an auditor). تبدأ بالحوكمة التي تعمل (governance that works): المالكون (owners)، والفهرس (catalogue)، والنسب (lineage)، وعقود البيانات (data contracts)، وكلها تُدار بوصفها شيفرة (managed as code) لا بوصفها محاضر لجان (committee minutes). ثم تتناول البيانات الشخصية (personal data): كيف تصنّفها (classify)، وتخفيها (mask)، وتقلّلها (minimise)، وتحتفظ بها فقط ما دامت مطلوبة (keep it only as long as needed)، وتمحوها عند الطلب (erase it when asked)، مع القوانين التي تنطبق على بنك نجم (Najm Bank) في قطر والإمارات والاتحاد الأوروبي (Qatar, the UAE and the EU). وتنتهي بأمن المنصة نفسها (security for the platform itself): التحكم في الوصول (access control) حتى مستوى الصف والعمود (down to the row and column)، والأسرار (secrets)، وسجلات التدقيق (audit logs)، والطرق الآمنة لمشاركة البيانات (safe ways to share data). ستتابع فريق منصة البيانات والتحليلات (Data Platform & Analytics team) في بنك نجم بينما يتغيّر رقم "العملاء النشطين" ("active customers") بين ليلة وضحاها ولا يستطيع أحد أن يقول لماذا، وتنسخ هدى بيانات العملاء (customer data) إلى بيئة تجريبية (sandbox) ما كان ينبغي لها، ويُحيل فيصل إلى التقاعد حساب المستخدم الخارق المشترك (shared superuser account) الذي استخدمه كل خط بيانات (pipeline) وكل لوحة معلومات (dashboard) لسنوات.*

> **المراحل (Stages):** Govern, Operate — جعل البيانات مملوكة (owned)، ومفهومة (understood)، ومشروعة (lawful)، وآمنة (safe)، بضوابط تعيش في الشيفرة (controls that live in code) وتترك أدلة (leave evidence).

---

# 6.1 — حوكمة بيانات تعمل فعلًا: الملكية والفهرس والنسب وعقود البيانات (Data governance that works: ownership, catalogue, lineage and data contracts)
*المستوى (Level): 🔴 متقدم (Advanced)* · *المتطلبات (Prerequisites): 1.2، 3.1، 3.2* · *المرحلة (Stage): Govern*

## ⚡ الدرس في دقيقة (In 60 seconds)
- **حوكمة البيانات (data governance)** هي مجموعة حقوق اتخاذ القرار والمساءلة (decision rights and accountabilities) على البيانات: من يقرّر ما تعنيه مجموعة البيانات (who decides what a dataset means)، ومن يحق له تغييرها، ومن يحق له استخدامها، ومن يصلحها عندما تتعطّل (who fixes it when it breaks).
- يجب أن تجيب عن أربعة أسئلة في دقائق: *من يملك هذا (Who owns this)؟ ماذا يعني (What does it mean)؟ من أين يأتي وإلى أين يذهب (Where does it come from and go)؟ ماذا لو تغيّر (What if it changes)؟*
- لبناتها الأساسية (building blocks) هي **المالكون والقيّمون (owners and stewards)**، و**مسرد الأعمال (business glossary)**، و**فهرس البيانات (data catalogue)**، و**النسب (lineage)** (ويُفضَّل حتى مستوى العمود (down to the column))، و**عقود البيانات (data contracts)** بين المنتجين والمستهلكين (producers and consumers).
- أبقِ الحوكمة شيفرةً بجانب البيانات (governance as code next to the data): المالكون والعقود في ملفات YAML الخاصة بـ dbt (dbt YAML)، والنسب يُجمَع تلقائيًا (lineage harvested automatically)، والتغييرات تُراجَع في طلبات السحب (changes reviewed in pull requests).
- إشارة القرار (decision cue): ابدأ بـ **عناصر البيانات الحرجة (critical data elements)** التي تغذّي التقارير التنظيمية (regulatory reports) وحزم مجلس الإدارة (board packs) والنماذج (models)، لا بكل جدول في مستودع البيانات (warehouse).
- أكبر فخ (biggest trap): برنامج حوكمة (governance programme) من اللجان والسياسات وفهرس لا يحدّثه أحد (a catalogue nobody updates)، بينما تتغيّر خطوط البيانات (pipelines) كل يوم من تحته.

## 🧭 لماذا يهم (Why it matters)
في صباح يوم إثنين، تُظهر لوحة معلومات التجزئة (retail dashboard) ‏412,000 عميل نشط (active customers). وفي يوم الجمعة كانت تُظهر 391,000. لا شيء في النشاط التجاري يفسّر قفزة بخمسة في المئة (five per cent jump) خلال ثلاثة أيام. يثير كريم (محلّل بيانات التجزئة (retail data analyst)) المسألة؛ ولا تجد لينا (مهندسة التحليلات (analytics engineer)) أي نموذج dbt (dbt model) تغيّر. وبعد يومين تتتبّع هدى المشكلة إلى **قاعدة بيانات الأنظمة المصرفية الأساسية (core banking database)**: فقد أضاف فريق الحسابات (accounts team) حالة `D` ‏(خامل (dormant)) إلى `acct_status`، وكان نموذج التهيئة (staging model) يعامل كل حالة باستثناء `C` ‏(مغلق (closed)) على أنها نشطة (active).

يستغرق الإصلاح عشر دقائق (the fix takes ten minutes). أما العثور على كل ما يمسّه فيستغرق ثلاثة أسابيع (finding everything it touches takes three weeks). فالعمود يغذّي متجر **رؤية العميل الشاملة (customer 360)**، و**متجر مخاطر الائتمان (credit-risk mart)**، ومستخلصًا للتقارير التنظيمية (regulatory reporting extract)، وخاصيتين (two features) في **التنبيهات الذكية (Smart Alerts)**، وحزمة مالية لمجلس الإدارة (finance board pack). لا أحد يستطيع أن يقول من يملك `acct_status`، ولا إن كان على فريق الحسابات أن يُبلغ أحدًا قبل تغييره، ولا أي التقارير خرجت بالفعل بالرقم الخاطئ (the wrong number). وتضيف سارة، مسؤولة حماية البيانات (Data Protection Officer)، سؤالًا لا يستطيع أحد الإجابة عنه: أيّ تلك الجداول يحمل بيانات شخصية (personal data)؟

ويلخّص فيصل، رئيس منصة البيانات (Head of Data Platform)، الأمر: "كان الخلل صغيرًا (the bug was small). ما آلمنا هو أننا لم نستطع الإجابة عن *من يملكه (who owns it)*، و*من يستخدمه (who uses it)*، و*من كان ينبغي إبلاغه (who should have been told)*." يبني هذا الدرس الحد الأدنى من الحوكمة (the minimum governance) الذي يحوّل ثلاثة أسابيع إلى عصر يوم واحد (one afternoon).

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**الحوكمة مقابل الإدارة (Governance versus management).** **إدارة البيانات (data management)** هي عمل تشغيل البيانات (the work of running data): بناء خطوط البيانات (building pipelines)، والتخزين، والتأمين، والإصلاح. أما **حوكمة البيانات (data governance)** فهي الطبقة التي فوق ذلك (the layer above)، وتقرّر من يملك السلطة والمساءلة (authority and accountability) على ذلك العمل. والمرجع المعرفي (reference body of knowledge) هو **DAMA-DMBOK** (*دليل المعرفة في إدارة البيانات (Data Management Body of Knowledge)* الصادر عن DAMA International؛ ونُشرت الطبعة الثانية (second edition) عام 2017). وهو يضع الحوكمة في مركز عجلة (at the centre of a wheel) من مجالات المعرفة (knowledge areas) مثل جودة البيانات (data quality)، والبيانات الوصفية (metadata)، والأمن (security)، ومعمارية البيانات (data architecture).

**الأدوار (Roles).** تبدأ الحوكمة بأشخاص مسمَّين (named people). تختلف المسمّيات الوظيفية (titles) بين المؤسسات؛ أما المسؤوليات (responsibilities) فلا تختلف.

| الدور (Role) | مسؤول عن (Responsible for) | في نجم، لمتجر رؤية العميل الشاملة (At Najm, for the customer 360 mart) |
|---|---|---|
| **مالك البيانات (Data owner)** | خاضع للمساءلة (accountable): يعتمد التعريف والاستخدام والوصول (approves definition, use and access)؛ ويقبل المخاطر (accepts risks). وعادةً ما يكون قائدًا في الأعمال (business leader). | رئيس الخدمات المصرفية للأفراد (Head of Retail Banking) |
| **قيّم البيانات (Data steward)** | المعنى والجودة يومًا بيوم (day-to-day meaning and quality): التعريفات (definitions)، والأسئلة، والمشكلات (issues). | كريم |
| **المالك التقني (Technical owner)** (أو "الحارس (custodian)") | يشغّل خط البيانات والتخزين (runs pipeline and storage): الاختبارات (tests)، والإتاحة (availability)، والتغييرات (changes). | لينا |
| **المنتِج (Producer)** | ينشئ البيانات في المنبع (creates the data upstream). | فريق الأنظمة المصرفية الأساسية (core banking team) |
| **المستهلك (Consumer)** | يستخدمها (uses it): لوحات المعلومات (dashboards)، والنماذج (models)، والتقارير (reports). | المخاطر (risk)، والمالية (finance)، والتنبيهات الذكية (Smart Alerts) |

قاعدتان (two rules): **مالك واحد خاضع للمساءلة لكل مجموعة بيانات (one accountable owner per dataset)**، لا لجنة (not a committee)؛ والملكية على المستوى الذي يفكّر فيه الناس (at the level people reason about)، أي مجموعة بيانات أو منتج بيانات (dataset or data product) مثل "رؤية العميل الشاملة (customer 360)"، لا كل عمود على حدة (not each column).

**اللبنات الأساسية (The building blocks).**
- يعرّف **مسرد الأعمال (business glossary)** مصطلحات الأعمال (business terms) بلغة بسيطة (in plain language) ‏("عميل نشط (active customer)"، "حساب خامل (dormant account)")، ولكل مصطلح مالك (owner) وروابط إلى الأعمدة والمقاييس (columns and metrics) ‏(4.1) التي تنفّذه.
- **فهرس البيانات (data catalogue)** هو جرد قابل للبحث (searchable inventory) لمجموعات البيانات. يحمل *البيانات الوصفية التقنية (technical metadata)* التي تُجمَع تلقائيًا (harvested automatically) ‏(المخططات (schemas)، والأنواع (types)، وأعداد الصفوف (row counts)، والحداثة (freshness))، و*البيانات الوصفية للأعمال (business metadata)* التي يكتبها الناس (الأوصاف (descriptions)، والمالكون (owners)، ومصطلحات المسرد (glossary terms)، والتصنيفات (classifications))، و*البيانات الوصفية التشغيلية (operational metadata)* ‏(آخر تشغيل (last run)، ونتائج الاختبارات (test results)، والاستخدام (usage)). ومن الأمثلة مفتوحة المصدر (open-source examples) **OpenMetadata**، و**DataHub** (بدأ في LinkedIn)، و**Amundsen** (بدأ في Lyft)؛ وتقدّم المنصات السحابية (cloud platforms) فهارسها الخاصة.
- يسجّل **النسب (lineage)** كيف تتدفق البيانات (how data flows): أيّ المصادر تغذّي أيّ الجداول، وأيّ الجداول تغذّي أيّ لوحات المعلومات. يقول *النسب على مستوى الجدول (table-level lineage)* إن "customer 360 مبنيّ من stg_accounts". ويقول *النسب على مستوى العمود (column-level lineage)* إن "`customer_360.active_flag` مشتقّ من `core.accounts.acct_status`"، وهذا ما تحتاجه لتحليل الأثر (impact analysis) ولتتبّع البيانات الشخصية (tracing personal data).
- **عقد البيانات (data contract)** هو اتفاق بين المنتِج والمستهلك (producer–consumer agreement) على المخطط (schema) والمعنى (meaning) ومستويات الخدمة (service levels) ‏(بنى الدرس 3.2 عقدًا من أجل الجودة (built one for quality)). وتضيف الحوكمة قواعد التغيير (change rules): من يُبلَّغ (who is told)، وكم مدة الإشعار المسبق (how much notice)، ومن يعتمد (who approves).

هذه حادثة `acct_status` مرسومةً بوصفها نسبًا على مستوى العمود (column-level lineage). ومع وجود هذا الرسم البياني (graph) في الفهرس (catalogue)، تصبح قائمة الأثر (impact list) على بُعد نقرة واحدة (one click away):

```mermaid
flowchart RL
    A["حالة الحساب في جدول حسابات النظام الأساسي<br/>(core.accounts.acct_status)"] --> B["حالة الحساب في نموذج التهيئة<br/>(stg_accounts.account_status)"]
    B --> C["مؤشر النشاط في النموذج الوسيط لحسابات العملاء<br/>(int_customer_accounts.is_active)"]
    C --> D["علامة النشاط في رؤية العميل الشاملة<br/>(customer_360.active_flag)"]
    C --> E["التعرّض القائم في متجر مخاطر الائتمان<br/>(credit_risk_mart.open_exposure)"]
    C --> F["الحسابات النشطة في المستخلص التنظيمي<br/>(reg_extract.active_accounts)"]
    D --> G["لوحة معلومات التجزئة<br/>(Retail dashboard)"]
    D --> H["خصائص التنبيهات الذكية<br/>(Smart Alerts features)"]
    E --> I["الحزمة المالية لمجلس الإدارة<br/>(Finance board pack)"]
```

**كيف يبدو "النجاح" (What "working" looks like).** اختر عمودًا من الفئة الأولى (tier-1 column) عشوائيًا وقِس كم يستغرق الإجابة عن الأسئلة الأربعة (the four questions). في الحادثة استغرق الأمر ثلاثة أسابيع؛ والهدف أقل من ساعة (under an hour).

### 🟡 التعمق أكثر (Going deeper)

**الحوكمة بوصفها شيفرة مع dbt (Governance as code with dbt).** معظم البيانات الوصفية للفهرس (catalogue metadata) موجودة أصلًا في مشروع التحويل (transformation project) الخاص بك (3.1). ضع الباقي بجانبه، ليُراجَع في طلب السحب نفسه (the same pull request) مع شيفرة SQL التي يصفها.

```yaml
# models/marts/customer/_customer_360.yml
groups:
  - name: customer_data
    owner:
      name: Lina
      email: lina@najm.example

models:
  - name: customer_360
    description: "One row per customer who holds at least one non-closed product. Grain: customer_key."
    access: public            # other dbt projects and teams may ref() it
    config:
      group: customer_data
      contract:
        enforced: true        # the build fails if columns or types drift
      meta:
        data_owner: "Head of Retail Banking"
        steward: "kareem@najm.example"
        tier: 1
        classification: confidential
        contains_personal_data: true
    columns:
      - name: customer_key
        data_type: varchar
        constraints:
          - type: not_null
        data_tests: [unique]
      - name: active_flag
        data_type: boolean
        description: "Glossary: Active customer. True if any account status is in ('A','O'). Dormant ('D') is NOT active."
        data_tests:
          - not_null
```

يجعل **عقد النموذج (model contract)** ‏(المتاح منذ dbt Core 1.5) أداة dbt تتحقق وقت البناء (at build time) من أن النموذج يُرجع بالضبط الأعمدة وأنواع البيانات المعلنة (exactly the declared columns and data types)؛ ويجب أن يسرد العقد المُنفَّذ (enforced contract) كل عمود (عُرض عمودان فقط توفيرًا للمساحة (to save space)). وتحدّد **المجموعات (groups)** و**الوصول (access)** ‏(`private` أو `protected` أو `public`) أيّ النماذج يجوز للفرق الأخرى البناء عليها (other teams may build on). تستخدم إصدارات dbt الأقدم `tests:` بدلًا من `data_tests:`. لا تتصرّف dbt بناءً على كتلة `meta` الحرّة الشكل (free-form meta block)، لكن الفهارس مثل OpenMetadata وDataHub تستوعبها (ingest it)، فيُكتب المالكون والتصنيفات (owners and classifications) مرة واحدة فقط (typed once).

يعلن **التعريض (exposure)** في dbt عن مستهلك (declares a consumer) ‏(لوحة معلومات (dashboard) أو تقرير (report) أو نموذج تعلّم آلة (ML model))، فيمتد النسب إلى ما وراء مستودع البيانات (lineage reaches beyond the warehouse):

```yaml
exposures:
  - name: retail_active_customers_dashboard
    type: dashboard
    owner:
      name: Kareem
      email: kareem@najm.example
    depends_on:
      - ref('customer_360')
```

**كيف يُبنى النسب (How lineage gets built).** هناك ثلاث طرق شائعة (three common ways)، والمنصات الناضجة (mature platforms) تجمع بينها:
1. **تحليل SQL (Parsing SQL).** تقرأ أداةٌ شيفرة SQL لكل نموذج وتستنتج أيّ الأعمدة تغذّي أيّها (which columns feed which). يحمل ملف `manifest.json` في dbt أصلًا الآباء والأبناء على مستوى الجدول (table-level parents and children)؛ وتضيف الفهارس التحليل على مستوى العمود (column-level parsing).
2. **أحداث وقت التشغيل (Runtime events).** **OpenLineage** ‏(مشروع تابع لـ LF AI & Data (an LF AI & Data project)) معيار مفتوح لأحداث النسب (open standard for lineage events): كل تشغيل لمهمة (each job run) يُصدر "المهمة X قرأت A وB وكتبت C" ("job X read A and B and wrote C"). توجد تكاملات (integrations) مع Airflow وSpark وdbt؛ و**Marquez** هو الواجهة الخلفية المرجعية (reference back end) له.
3. **الإعلانات (Declarations).** تملأ التعريضات التي يكتبها الناس (exposures written by people) الفجوات التي لا تراها الأدوات (gaps tools cannot see)، مثل مستخلص يُرسَل بالبريد الإلكتروني إلى المالية (an extract emailed to finance).

النسب رسم بياني (lineage is a graph)، لذا فتحليل الأثر (impact analysis) هو تجوال في الرسم البياني (graph walk). يمكنك بناء نموذج أولي (prototype) له في DuckDB أو PostgreSQL باستعلام تعاوُدي (recursive query):

```sql
CREATE TABLE lineage_edges (upstream TEXT, downstream TEXT);
INSERT INTO lineage_edges VALUES
  ('core.accounts.acct_status',        'stg_accounts.account_status'),
  ('stg_accounts.account_status',      'int_customer_accounts.is_active'),
  ('int_customer_accounts.is_active',  'customer_360.active_flag'),
  ('int_customer_accounts.is_active',  'credit_risk_mart.open_exposure'),
  ('int_customer_accounts.is_active',  'reg_extract.active_accounts'),
  ('customer_360.active_flag',         'exposure.retail_active_customers_dashboard');

-- Everything downstream of one source column, with distance
WITH RECURSIVE impact(node, depth) AS (
  SELECT CAST('core.accounts.acct_status' AS TEXT), 0
  UNION ALL
  SELECT e.downstream, i.depth + 1
  FROM lineage_edges e
  JOIN impact i ON e.upstream = i.node
)
SELECT node, MIN(depth) AS depth
FROM impact
GROUP BY node
ORDER BY depth, node;
```

اربط النتيجة بسجلّ الملكية (join the result to the ownership register) فتحصل على الأشخاص الذين يجب إبلاغهم قبل التغيير (the people to tell before the change).

**قواعد التغيير في العقد (Change rules in the contract).** ليست كل التغييرات متساوية (not every change is equal). صنّفها (classify them)، واتفق على القواعد مع المنتجين مسبقًا (agree the rules with producers in advance):

| التغيير (Change) | مثال (Example) | الفئة (Class) | القاعدة في نجم (Rule at Najm) |
|---|---|---|---|
| إضافة عمود يقبل القيم الفارغة (Add a nullable column) | عمود `branch_code` جديد (New column) | غير كاسر (Non-breaking) | الإعلان في ملاحظات الإصدار (Announce in the release notes) |
| إضافة قيمة إلى قائمة رموز (Add a value to a code list) | حالة جديدة `D` ‏(New status) | **كاسر في المعنى (Breaking in meaning)** | إشعار مسبق لمدة 30 يومًا لكل المستهلكين في النسب (30 days' notice to all consumers in lineage)؛ ويعتمده القيّم (steward signs off) |
| إعادة تسمية عمود أو حذفه (Rename or drop a column) | من `acct_status` إلى `status` | كاسر (Breaking) | إصدار جديد من العقد (new contract version)؛ ويُحتفظ بالقديم 60 يومًا |
| تغيير الحُبَيبية (Change the grain) | صف واحد لكل حساب بدلًا من كل عميل (One row per account instead of per customer) | كاسر (Breaking) | مجموعة بيانات جديدة (New dataset) |

بدت الحالة `D` غير مؤذية (looked harmless): لم تُعَد تسمية أي عمود، ولم يتغيّر أي نوع. لقد كانت تغييرًا كاسرًا **دلاليًا (semantic)**، ولا شيء سوى عقدٍ يسرد القيم المسموح بها (a contract listing allowed values)، مُنفَّذٍ باختبار `accepted_values` في طبقة التهيئة (staging)، يحوّلها إلى بناء فاشل (failed build) بدلًا من حزمة مجلس إدارة خاطئة (wrong board pack). وتتيح لك **إصدارات النماذج (model versions)** في dbt نشر `v2` بجانب `v1` مع تاريخ إيقاف (deprecation date).

### 🔴 نظرة الخبير (Expert view)

**ابدأ بعناصر البيانات الحرجة (Start with critical data elements).** تبدأ البنوك عادةً بـ **عناصر البيانات الحرجة (critical data elements, CDEs)**: الحقول التي تغذّي البيانات التنظيمية المرفوعة (regulatory returns)، وأرقام المخاطر (risk numbers)، وتقارير مجلس الإدارة (board reporting)، والنماذج (models). والمرجع المصرفي الكلاسيكي (classic banking reference) هو **BCBS 239**، أي *مبادئ التجميع الفعّال لبيانات المخاطر والإبلاغ عنها (Principles for effective risk data aggregation and risk reporting)* الصادرة عن لجنة بازل (Basel Committee) ‏(يناير 2013). وقد كُتبت لأكبر البنوك ذات الأهمية النظامية العالمية (the largest, globally systemic banks)، لكن محاورها (its themes) ‏(الحوكمة (governance)، ودقة بيانات المخاطر واكتمالها وحسن توقيتها وقابليتها للتكيّف (accuracy, completeness, timeliness and adaptability of risk data)) تُستخدم على نطاق واسع بوصفها ممارسة جيدة (good practice) في أماكن أخرى؛ فتحقّق مما يتوقعه الجهاز الرقابي الخاص بك (what your own regulator expects). وتغطي قائمة عناصر البيانات الحرجة الأولى في نجم (Najm's first CDE list) المستخلصات التنظيمية (regulatory extracts) ومتجر مخاطر الائتمان (credit-risk mart)؛ ويحصل كل عنصر على مالك (owner)، وتعريف (definition)، ونسب حتى المصدر (lineage to source)، وعقد (contract)، واختبارات (tests).

**نماذج التشغيل (Operating models).** من يقوم بعمل الحوكمة (who does the governance work)؟
- **المركزي (Centralised):** فريق بيانات واحد يحوكم كل شيء (one data team governs everything). متّسق (consistent)، لكنه عنق زجاجة (bottleneck) تنقصه معرفة الأعمال (business knowledge).
- **الاتحادي (Federated):** مكتب مركزي صغير (small central office) يضع المعايير والأدوات (standards and tooling)؛ وتملك النطاقات (domains) ‏(التجزئة (retail)، والمخاطر (risk)، والمالية (finance)) بياناتها وتعيّن القيّمين (appoint stewards). ومعظم البنوك تنتهي إلى هذا النموذج.
- **شبكة البيانات (Data mesh):** نهج Zhamak Dehghani ‏(الذي وُصف أول مرة عام 2019): ملكية النطاق (domain ownership)، والبيانات بوصفها منتجًا (data as a product)، ومنصة خدمة ذاتية (self-serve platform)، و*الحوكمة الحسابية الاتحادية (federated computational governance)*، أي قواعد تفرضها المنصة تلقائيًا (rules enforced by the platform automatically)، لا الاجتماعات.

**افرض القواعد بالبوابات لا بالمذكرات (Enforce with gates, not memos).** نصٌّ برمجي قصير (short script) يعمل على `manifest.json` في التكامل المستمر (CI) لدى نجم (راجع [*السحابة وDevOps: من الصفر إلى الاحتراف (Cloud & DevOps: Zero to Hero)*، الدرس 4.1 — التكامل المستمر: خطوط التنفيذ والاختبارات والمُخرَجات والتغذية الراجعة السريعة (Continuous integration: pipelines, tests, artefacts and fast feedback)](../cloud/index.ar.html#/4.1)) يُفشل طلب السحب (fails a pull request) عندما يفتقر نموذج من الفئة الأولى (tier-1 model) إلى `meta.data_owner` أو يفتقر نموذج `public` إلى عقد مُنفَّذ (enforced contract). وبذلك تسري القواعد على كل تغيير (hold for every change)، لا على ما يلاحظه المراجع فقط (not only those a reviewer notices).

**قِسها (Measure it).** قِس التغطية والسرعة (coverage and speed)، لا النشاط (not activity): نسبة نماذج الفئة الأولى التي لها مالك ووصف وعقد واختبارات (owner, description, contract and tests)؛ ونسبة عناصر البيانات الحرجة التي لها نسب على مستوى العمود (column-level lineage)؛ والوقت اللازم للإجابة عن سؤال أثر (time to answer an impact question)؛ والحوادث الناجمة عن تغييرات غير معلنة في المنبع (incidents caused by unannounced upstream changes).

**حوكمة الذكاء الاصطناعي تعيد استخدام الأجزاء نفسها (Governance for AI reuses the same parts).** عندما تدرّب دانة التنبيهات الذكية (Smart Alerts) أو عندما يفهرس مساعد مذكرات الائتمان (Credit Memo Copilot) سياسات الائتمان (credit policies)، تكون الأسئلة نفسها: من أين جاءت البيانات (where did the data come from)، ومن يملكها، وهل يحق لنا استخدامها لهذا الغرض (for this purpose)؟ جانب السياسات (the policy side) موجود في [*حوكمة الذكاء الاصطناعي: من الصفر إلى الاحتراف (AI Governance: Zero to Hero)*، الدرس 3.2 — سياسات حوكمة البيانات والملكية الفكرية للذكاء الاصطناعي (Data governance and intellectual-property policies for AI)](../aigp/index.ar.html#/3.2) وفي [*حوكمة الذكاء الاصطناعي: من الصفر إلى الاحتراف (AI Governance: Zero to Hero)*، الدرس 9.1 — مصادر البيانات ونسبها وحقوق استخدامها (Sourcing, lineage and rights to use data)](../aigp/index.ar.html#/9.1). والنسب والملكية (lineage and ownership) لديك هما الدليل الذي تحتاجه (their evidence).

## 🧰 الأدوات (The toolkit)
| الأداة أو النمط أو المعيار (Tool, pattern or standard) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **DAMA-DMBOK** (DAMA International) — دليل المعرفة في إدارة البيانات | مرجع معرفي (reference body of knowledge) لإدارة البيانات وحوكمتها (data management and governance): الأدوار (roles)، ومجالات المعرفة (knowledge areas)، والمفردات (vocabulary) | عند تصميم برنامج حوكمة (designing a governance programme)؛ وللتحدث بلغة مكاتب الحوكمة والمدققين (governance offices and auditors) |
| **OpenMetadata** | فهرس بيانات مفتوح المصدر (open-source data catalogue) فيه موصِّلات استيعاب (ingestion connectors)، ومسرد (glossary)، وملكية (ownership)، ونسب (lineage)، وعروض لجودة البيانات (data quality views) | فهرس مُستضاف ذاتيًا (self-hosted catalogue) يستوعب البيانات الوصفية من dbt ومستودع البيانات وأدوات ذكاء الأعمال (dbt, warehouse and BI metadata) |
| **OpenLineage** | معيار مفتوح (open standard) لأحداث النسب التي تُصدرها المهام وقت التشغيل (lineage events emitted by jobs at run time)، وMarquez هو الواجهة الخلفية المرجعية (reference back end) | لالتقاط النسب من تشغيلات Airflow وSpark وdbt دون مخططات مرسومة يدويًا (without hand-written diagrams) |
| **dbt model contracts** — عقود نماذج dbt | تحقق وقت البناء (build-time check) من أن النموذج يُرجع بالضبط الأعمدة والأنواع المعلنة (exactly the declared columns and types)، إضافة إلى المجموعات (groups) والوصول (access) والإصدارات (versions) | كل نموذج تعتمد عليه فرق أخرى (other teams depend on)؛ وأي نموذج من الفئة الأولى أو عام (tier-1 or public model) |
| **Data contract** — عقد البيانات | اتفاق بين المنتِج والمستهلك (producer–consumer agreement) على المخطط والمعنى ومستويات الخدمة وقواعد التغيير (schema, meaning, service levels and change rules) | كل نظام مصدر يغذّي بيانات حرجة (every source system feeding critical data)؛ وأي مجموعة بيانات عابرة للفرق (cross-team dataset) |
| **BCBS 239** (Basel Committee, 2013) — مبادئ لجنة بازل | مبادئ لتجميع بيانات المخاطر والإبلاغ عنها في البنوك (risk data aggregation and risk reporting in banks) | لترتيب أولويات عناصر البيانات الحرجة (prioritising critical data elements) وشرح الحوكمة للمشرفين المصرفيين (bank supervisors) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
بعد الحادثة، تكتب لينا وهدى **سجلّ ملكية البيانات وسياسة التغيير في نجم، الإصدار 1 (Najm Data Ownership Register and Change Policy v1)** لمجموعات بيانات الفئة الأولى (tier-1 datasets). وهو يعيش في هيئة ملفات YAML ‏(lives as YAML) في مستودع dbt (dbt repository) ويُنشر في الفهرس (published to the catalogue).

**الجزء أ: سجلّ الملكية (الفئة الأولى، المُدخلات الأولى) (Part A: ownership register (tier 1, first entries))**

| مجموعة البيانات (Dataset) | مالك البيانات (Data owner) | القيّم (Steward) | المالك التقني (Technical owner) | التصنيف (Classification) | أبرز المستهلكين (Top consumers) |
|---|---|---|---|---|---|
| `core.accounts` ‏(مصدر (source)) | رئيس عمليات الأنظمة المصرفية الأساسية (Head of Core Banking Operations) | محلّل منتجات الحسابات (Accounts product analyst) | فريق الأنظمة المصرفية الأساسية (Core banking team) | سرّي، شخصي (Confidential, personal) | كل المتاجر (All marts) |
| `customer_360` | رئيس الخدمات المصرفية للأفراد (Head of Retail Banking) | كريم | لينا | سرّي، شخصي (Confidential, personal) | لوحة معلومات التجزئة (Retail dashboard)، والتنبيهات الذكية (Smart Alerts) |
| `credit_risk_mart` | رئيس المخاطر (Chief Risk Officer) | قيّم بيانات المخاطر (Risk data steward) | هدى | سرّي (Confidential) | حزمة مجلس الإدارة (Board pack)، والمستخلص التنظيمي (regulatory extract) |
| `card_authorisations` ‏(تدفق (stream)) | رئيس البطاقات (Head of Cards) | محلّل البطاقات (Cards analyst) | فريق التدفق (Streaming team) | مقيّد (بيانات البطاقات) (Restricted (card data)) | التنبيهات الذكية (Smart Alerts) |

**الجزء ب: سياسة التغيير (Part B: change policy)**
1. لكل مجموعة بيانات من الفئة الأولى (tier-1 dataset) مالك بيانات واحد بالضبط، وقيّم واحد، ومالك تقني واحد (exactly one data owner, one steward and one technical owner)، مسجّلون في `meta`. ويفشل في التكامل المستمر (fails CI) أي طلب سحب ينشر نموذجًا من الفئة الأولى أو نموذج `public` من دونهم.
2. يصنّف المنتجون (producers) كل تغيير باستخدام جدول التغييرات (change table) في هذا الدرس. وتحتاج التغييرات الكاسرة والدلالية (breaking and semantic changes) إلى إشعار مسبق لمدة 30 يومًا لكل من هم في المصبّ ضمن النسب (everyone downstream in lineage)، يُولَّد من الفهرس (generated from the catalogue)، وإلى اعتماد قيّم كل مجموعة بيانات متأثرة من الفئة الأولى (sign-off by the steward of each affected tier-1 dataset).
3. لكل قائمة رموز (code list) ‏(الحالات (statuses)، وأنواع المنتجات (product types)، والشرائح (segments)) في مصدر من الفئة الأولى اختبار `accepted_values` في طبقة التهيئة (staging)، بحيث تُفشل أي قيمة جديدة البناء (a new value fails the build) بدلًا من أن تغيّر رقمًا بصمت (changing a number silently).
4. تُشحن التغييرات الكاسرة (breaking changes) بوصفها إصدارًا جديدًا من العقد (new contract version)؛ ويبقى الإصدار القديم متاحًا 60 يومًا.
5. يُبلغ مكتب الحوكمة (governance office) كل ربع سنة عن تغطية الفئة الأولى (tier-1 coverage) والوقت المستغرق للإجابة عن ثلاثة أسئلة أثر عشوائية (three random impact questions).

**الجزء ج: قاعدة الحوادث (Part C: incident rule).** كل حادثة ناجمة عن تغيير في المنبع (caused by an upstream change) تضيف بند العقد أو الاختبار الناقص (the missing contract clause or test) خلال دورة عمل واحدة (one sprint)؛ فقد أصبحت الحالة `D` اختبار `accepted_values` ومُدخلًا في المسرد (glossary entry) لمصطلح "حساب خامل (dormant account)".

## 🛠️ التمارين (Exercises)
استخدم بيانات اصطناعية (synthetic) أو بيانات عامة مفتوحة (public open data) فقط.

- 🟢 باستخدام مشروع المثال "jaffle shop" من dbt ‏(dbt "jaffle shop" example project) أو مجموعة بيانات عامة مفتوحة فيها عدة جداول، اكتب سجلّ ملكية (ownership register) لخمس مجموعات بيانات (المالك (owner)، والقيّم (steward)، والمالك التقني (technical owner)، والتصنيف (classification)، والمستهلكون (consumers)) وتعريفات مسرد (glossary definitions) لثلاثة مصطلحات أعمال (business terms). *يكتمل عندما (Done when):* يستطيع زميل أن يجيب عن "من أسأل عن هذا العمود، وماذا يعني هذا المصطلح؟" ⁦("who do I ask about this column, and what does this term mean?")⁩ لأي من مجموعات البيانات الخمس باستخدام سجلّك فقط.
- 🟡 في مشروع dbt Core على DuckDB أو PostgreSQL، أضف مالكين في `meta` ‏(meta owners)، ومجموعة (group)، و`access: public`، وعقدًا مُنفَّذًا (enforced contract) إلى نموذجَي متجر (two mart models)، وأضف تعريضًا واحدًا (one exposure). ثم غيّر نوع عمود (column's type) في شيفرة SQL. *يكتمل عندما (Done when):* يفشل `dbt build` على العقد برسالة واضحة (clear message)، وينجح بعد أن تصلحه، ويُظهر `dbt docs generate` التعريض في رسم النسب البياني (lineage graph).
- 🔴 اكتب نصًا برمجيًا بلغة Python ‏(Python script) يحمّل خريطة الآباء والأبناء (parent–child map) من ملف `target/manifest.json` في dbt إلى DuckDB، ويسرد لعقدة معيّنة (for a given node) كل نموذج وتعريض في المصبّ (every downstream model and exposure) مع مالكه في `meta` ‏(meta owner). أضف فحصًا (check) ينتهي بخطأ (exits with an error) إذا افتقر أي نموذج `public` إلى مالك أو عقد مُنفَّذ. *يكتمل عندما (Done when):* يطبع النص قائمة أثر صحيحة (correct impact list) لنموذج تهيئة (staging model)، ويفشل الفحص عندما تزيل مالكًا وينجح عندما تعيده.

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **الحوكمة بوصفها أوراقًا (Governance as paperwork).** السياسات غير المرتبطة بخطوط البيانات (policies unlinked to pipelines) تتقادم خلال أسابيع (go stale in weeks). ضع المالكين والعقود في الشيفرة (in code)؛ وافرضها في التكامل المستمر (enforce them in CI).
- **مملوكة لـ"فريق البيانات" (Owned by "the data team").** الفريق ليس مالكًا (a team is not an owner). سمِّ شخصًا واحدًا خاضعًا للمساءلة لكل مجموعة بيانات (one accountable person per dataset)، واجعل مالك الأعمال (business owner) خاضعًا للمساءلة عن المعنى والاستخدام (meaning and use).
- **فهرسة كل شيء أولًا (Cataloguing everything first).** عشرة آلاف جدول غير موثّق (undocumented tables) لا تساعد أحدًا. ابدأ بعناصر البيانات الحرجة (critical data elements) ووثّقها جيدًا.
- **النسب على مستوى الجدول فقط (Table-level lineage only).** يحتاج تحليل الأثر وتتبّع البيانات الشخصية (impact analysis and personal-data tracing) إلى نسب على مستوى العمود (column-level lineage) للأعمدة الحرجة (critical columns).
- **اعتبار تغييرات المخطط وحدها كاسرة (Treating only schema changes as breaking).** قيمة رمز جديدة (new code value)، أو تغيير في الوحدة (unit change)، أو حُبَيبية جديدة (new grain) تكسر المستهلكين دون تغيير نوع واحد. يجب أن تغطي العقود المعنى (contracts must cover meaning)، ويجب أن تتحقق الاختبارات من القيم المسموح بها (allowed values).

## 🧾 الخلاصة (Recap)
- تحدّد حوكمة البيانات (data governance) حقوق اتخاذ القرار والمساءلة (decision rights and accountability): من يملك كل مجموعة بيانات ويعرّفها ويغيّرها ويحق له استخدامها.
- اللبنات الأساسية (building blocks) هي مالكون وقيّمون مسمَّون (named owners and stewards)، ومسرد أعمال (business glossary)، وفهرس (catalogue)، ونسب على مستوى العمود (column-level lineage)، وعقود بيانات بقواعد تغيير (data contracts with change rules).
- أبقِ الحوكمة في الشيفرة بجانب البيانات (in code next to the data) ‏(`meta` في dbt، والمجموعات (groups)، والوصول (access)، والعقود (contracts)، والتعريضات (exposures)) وافرضها بفحوص التكامل المستمر (CI checks).
- ابدأ بعناصر البيانات الحرجة (critical data elements)، واختر نموذجًا اتحاديًا (federated model)، وقِس التغطية وسرعة الإجابات (coverage and speed of answers)، لا النشاط.

## ✍️ اختبر نفسك (Check yourself)

**1. يضيف فريق الأنظمة المصرفية الأساسية (core banking team) قيمة جديدة `D` ‏(خامل (dormant)) إلى `acct_status`. لم تُعَد تسمية أي عمود ولم يتغيّر أي نوع. كيف ينبغي أن تصنّف سياسة التغيير (change policy) في نجم هذا التغيير؟**

- A. غير كاسر (non-breaking)، لأنه لم تُعَد تسمية أي عمود ولم يتغيّر أي نوع بيانات (data type)
- B. تغيير كاسر دلالي (semantic breaking change) يحتاج إلى إشعار للمستهلكين في النسب (notice to consumers in lineage)
- C. تغيير في الحُبَيبية (grain change)، لذا يجب أن يُشحن بوصفه مجموعة بيانات جديدة (new dataset)
- D. ليس مسألة حوكمة (not a governance matter)، لأن تطبيق المنتِج وحده (only the producer's application) يكتب في العمود

<details><summary>الإجابة</summary>

**B.** تغيّر قيمة الرمز الجديدة (new code value) ما تعنيه البيانات، وقد كسرت عدّ العملاء النشطين (active-customer count)، مع أن المخطط (schema) بقي كما هو. A هي الإجابة المغرية (tempting answer)، لأن النظر إلى العقود من زاوية المخطط وحده (schema-only view of contracts) يُغفل المعنى؛ وD تتجاهل المستهلكين في المصبّ (downstream consumers) الذين يُظهرهم النسب. (🟡 التعمق أكثر (Going deeper).)

</details>

**2. أيّ عبارة تصف على أفضل وجه الفرق بين حوكمة البيانات (data governance) وإدارة البيانات (data management)؟**

- A. الحوكمة يقوم بها قسم تقنية المعلومات (IT department)؛ والإدارة تقوم بها فرق الأعمال (business teams)
- B. الحوكمة هي أداة الفهرس (catalogue tool)؛ والإدارة هي كل شيء آخر يفعله فريق البيانات
- C. هما اسمان للنشاط نفسه (two names for the same activity)، يستخدمهما مورّدون مختلفون (different vendors)
- D. الحوكمة تحدّد حقوق اتخاذ القرار والمساءلة (decision rights and accountability)؛ والإدارة تؤدي العمل (does the work)

<details><summary>الإجابة</summary>

**D.** تقرّر الحوكمة السلطة والمساءلة (authority and accountability)؛ وتؤدي الإدارة العمل. A خاطئة لأن مالكي الأعمال (business owners) هم الخاضعون للمساءلة، والفهرس (catalogue) ‏(B) ليس إلا أداة واحدة. (🟢 الأساسيات (The essentials).)

</details>

**3. يجب على هدى أن تجد كل تقرير يتأثر بتغيير في `core.accounts.acct_status` قبل شحن التغيير. ما الذي يعطيها الإجابة الأكثر موثوقية (most reliable answer)؟**

- A. النسب الحالي على مستوى العمود (current column-level lineage)، مع التجوال فيه نحو المصبّ (walked downstream) وربطه بسجلّ الملكية (ownership register)
- B. السؤال في قناة الدردشة الخاصة بفريق التحليلات (analytics team's chat channel) عمّن يستخدم جدول الحسابات
- C. النسب على مستوى الجدول (table-level lineage) الذي يُظهر كل متجر وتقرير يقرأ `core.accounts`
- D. مخطط النسب المفصّل (detailed lineage diagram) الذي رُسم خلال مراجعة المعمارية (architecture review) في العام الماضي

<details><summary>الإجابة</summary>

**A.** النسب على مستوى العمود المجموع من الشيفرة وأحداث التشغيل (harvested from code and run events) حديث (current)، والسجلّ (register) يحوّله إلى أشخاص يجب إبلاغهم. C مغرية لكنها خشنة أكثر مما ينبغي (too coarse): فكثير من الجداول تقرأ `core.accounts` دون هذا العمود؛ وD متقادمة (stale). (🟡 التعمق أكثر (Going deeper).)

</details>

**4. تريد نجم أن تبدأ الحوكمة بعدد محدود من الأشخاص (limited people). أيّ نطاق بداية (starting scope) هو الأكثر منطقية؟**

- A. فهرسة كل جدول في مستودع البيانات أولًا (catalogue every table)، ثم تعيين المالكين بعد اكتمال الجرد (once the inventory is complete)
- B. شراء أداة فهرس تجارية (commercial catalogue tool) وترك الاعتماد عليها ينمو من تلقاء نفسه (let adoption grow on its own)
- C. البدء بعناصر البيانات الحرجة (critical data elements) وإعطاء كل منها مالكًا وتعريفًا ونسبًا وعقدًا واختبارات (owner, definition, lineage, contract and tests)
- D. كتابة سياسة حوكمة كاملة (full governance policy)، واعتمادها في لجنة، وانتظار أن تتبناها الفرق

<details><summary>الإجابة</summary>

**C.** البدء بعناصر البيانات الحرجة، وهو النهج الذي تتبعه البنوك غالبًا مع BCBS 239 مرجعًا (as a reference)، يضع الجهد حيث تؤلم الأخطاء أكثر (where errors hurt most). A تشتّت الجهد أكثر مما ينبغي (spreads effort too thin)؛ وB وD تُنشئان أدوات وأوراقًا بلا ملكية (tools and paper without ownership). (🔴 نظرة الخبير (Expert view).)

</details>

**5. ما الذي يتحقق منه عقد نموذج dbt المُنفَّذ (enforced dbt model contract)؟**

- A. أن عدد صفوف النموذج (row count) يطابق جدول المصدر (source table) بعد كل تشغيل
- B. أن النموذج يُرجع بالضبط الأعمدة وأنواع البيانات المعلنة (exactly the declared columns and data types)
- C. أن مالك البيانات (data owner) المسمّى في `meta` قد اعتمد آخر تغيير
- D. ألّا يكون في النموذج أي عمود موسوم بأنه بيانات شخصية (tagged as personal data)

<details><summary>الإجابة</summary>

**B.** يتحقق العقد من شكل النموذج (model's shape) وقت البناء (at build time): أسماء الأعمدة (column names)، والأنواع (types)، والقيود المعلنة (declared constraints). أما أعداد الصفوف (A)، والاعتمادات (approvals) ‏(C)، والتصنيف (classification) ‏(D) فتحتاج إلى اختبارات (tests)، وقواعد مراجعة (review rules)، وعمل الدرس 6.2. (🟡 التعمق أكثر (Going deeper).)

</details>

## 📚 المراجع (References)
- DAMA International، *DAMA-DMBOK: Data Management Body of Knowledge* (دليل المعرفة في إدارة البيانات)، الطبعة الثانية (2nd edition) ‏(2017) — https://www.dama.org/
- توثيق dbt: عقود النماذج (dbt documentation: model contracts) — https://docs.getdbt.com/reference/resource-configs/contract
- توثيق dbt: التعريضات (dbt documentation: exposures) — https://docs.getdbt.com/docs/build/exposures
- OpenLineage — https://openlineage.io/
- OpenMetadata — https://open-metadata.org/
- DataHub — https://datahubproject.io/
- لجنة بازل للرقابة المصرفية (Basel Committee on Banking Supervision)، *مبادئ التجميع الفعّال لبيانات المخاطر والإبلاغ عنها (Principles for effective risk data aggregation and risk reporting)* ‏(BCBS 239، 2013) — https://www.bis.org/publ/bcbs239.htm
- Zhamak Dehghani، *Data Mesh: Delivering Data-Driven Value at Scale* (شبكة البيانات: تحقيق قيمة قائمة على البيانات على نطاق واسع) ‏(O'Reilly، 2022)

---

# 6.2 — البيانات الشخصية: التصنيف والإخفاء والتقليل والاحتفاظ والقانون (Personal data: classification, masking, minimisation, retention and the law)
*المستوى (Level): 🔴 متقدم (Advanced)* · *المتطلبات (Prerequisites): 1.3، 6.1* · *المرحلة (Stage): Govern, Store*

## ⚡ الدرس في دقيقة (In 60 seconds)
- **البيانات الشخصية (personal data)** هي أي معلومات عن شخص قابل للتعرّف عليه (identifiable person): لا الأسماء والهويات فحسب (not just names and IDs)، بل أيضًا أرقام الحسابات (account numbers)، ومعرّفات الأجهزة (device IDs)، أو مزيج نادر (rare mix) من تاريخ الميلاد والجنسية والفرع (birth date, nationality and branch).
- **صنّف (classify)** كل عمود (عام (public)، داخلي (internal)، سرّي (confidential)، مقيّد (restricted)، إضافة إلى وسم البيانات الشخصية (personal-data tag))، ودع التصنيف يقود الإخفاء والوصول والاحتفاظ تلقائيًا (drive masking, access and retention automatically).
- **قلّل (minimise)** أولًا: أكثر البيانات الشخصية أمانًا هي البيانات التي لم تنسخها قط (the data you never copied). ثم **استخدم الأسماء المستعارة (pseudonymise)** بتجزئة مُفتاحية (keyed hash) أو رموز مميّزة (tokens)، و**أخفِ (mask)** ما يراه الناس، و**احذف (delete)** وفق جدول زمني (on a schedule).
- **البيانات ذات الأسماء المستعارة تبقى بيانات شخصية (pseudonymised data is still personal data)** بموجب اللائحة العامة لحماية البيانات (GDPR). وحدها البيانات المجهّلة تجهيلًا صحيحًا (properly anonymised data) تقع خارجها، والتجهيل (anonymisation) أصعب بكثير مما يبدو.
- إشارة القرار (decision cue): قبل أي نسخة، اسأل: "أيّ الأعمدة يحتاجها هذا الغرض فعلًا، ومتى ستُحذف؟" ⁦("which columns does this purpose actually need, and when will they be deleted?")⁩
- أكبر فخ (biggest trap): تجزئة غير مملّحة (unsalted hash) لرقم الهوية الوطنية (national ID)، تُسمّى "مجهّلة (anonymised)"، في بيئة تجريبية (sandbox) لا ينظّفها أحد أبدًا.

## 🧭 لماذا يهم (Why it matters)
تريد هدى أن تعرف لماذا تنتهي محادثات نجم أسيست (Najm Assist) حول نزاعات البطاقات (card disputes) بشكاوى (complaints). يمنحها زميل صلاحية القراءة (read access) على `core.customers`، فتنسخ الأعمدة الثمانية والثلاثين كلها (الأسماء، والهواتف، وأرقام الهوية الوطنية (national IDs)، وتواريخ الميلاد، والرواتب، والعناوين) إلى مخطط تجريبي شخصي (personal sandbox schema). ثم يصدّر دفتر ملاحظاتها (notebook) عيّنة (sample) إلى ملف CSV على محرّك أقراص مشترك (shared drive) "ليطّلع عليها كريم".

بعد ثلاثة أسابيع، تجد سارة، مسؤولة حماية البيانات (Data Protection Officer)، المخطط في فحص روتيني (routine scan). تشرح هدى أنها جزّأت أرقام الهوية الوطنية (hashed the national IDs)، فالبيانات إذن "مجهّلة (anonymised)". وتُريها سارة لماذا ليست كذلك: الهويات أرقام قصيرة ذات بنية معروفة (short numbers with a known structure)، لذا يستطيع أي شخص أن يجزّئ كل قيمة ممكنة (hash every possible value) ويطابقها عكسيًا (match them back). ثم تطرح الأسئلة التي يطرحها القانون (the questions the law asks): لأي غرض نُسخت (for what purpose)، وهل كان كل عمود مطلوبًا، ومن غيرها وصل إليها، ومتى ستُحذف؟

لم يتسرّب شيء خارج البنك (nothing leaked outside the bank)، ولم يحتج تحليل هدى إلا إلى خمسة أعمدة، ليس أيّ منها معرِّفًا (none of them identifying). يبني هذا الدرس منصة يكون فيها المسار الآمن (the safe path) ‏(بيانات مصنّفة (classified data)، وعروض مُخفاة (masked views)، ونسخ محدودة بغرض تنتهي صلاحيتها (purpose-limited copies that expire)) هو المسار السهل أيضًا (also the easy one).

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**ما الذي يُعدّ بيانات شخصية (What counts as personal data).** تعرّف اللائحة العامة لحماية البيانات (GDPR) البيانات الشخصية بأنها أي معلومات تتعلق بشخص طبيعي محدَّد أو قابل للتحديد (any information relating to an identified or identifiable natural person) ‏(المادة 4(1) (Article 4(1))). ويواجه مهندسو البيانات (data engineers) عادةً ثلاثة أنواع:
- **المعرِّفات المباشرة (direct identifiers)** تحدّد هوية الشخص بمفردها (on their own): الاسم، ورقم الهوية الوطنية (national ID)، والهاتف، والبريد الإلكتروني، ورقم الحساب (account number)، ورقم البطاقة (card number).
- **أشباه المعرِّفات (quasi-identifiers)** ‏(المعرِّفات غير المباشرة (indirect identifiers)) تحدّد هوية الأشخاص عند اجتماعها (in combination): تاريخ الميلاد، والجنسية، والرمز البريدي أو الفرع (postcode or branch)، والمسمّى الوظيفي (job title)، ومبلغ معاملة نادر في وقت معروف (a rare transaction amount at a known time).
- **الفئات الخاصة (special categories)** تحتاج إلى حماية إضافية (extra protection) بموجب المادة 9 من اللائحة (GDPR Article 9): الصحة (health)، والدين (religion)، والأصل العرقي (ethnic origin)، والبيانات الحيوية (biometrics)، وغيرها. وهي تختبئ في النص الحر (free text) مثل ملاحظات الشكاوى (complaint notes) وسجلات نجم أسيست (Najm Assist logs).

**صنّف كل عمود (Classify every column).** يعطي **مخطط تصنيف البيانات (data classification scheme)** كل عمود مستوى حساسية (sensitivity level) ووسومًا (tags)، وتستخدمها المنصة لتقرّر من يرى ماذا (who sees what). مخطط نجم (Najm's scheme):

| المستوى (Level) | المعنى (Meaning) | أمثلة في نجم (Examples at Najm) |
|---|---|---|
| **عام (Public)** | معتمد للنشر (approved for publication) | عناوين الفروع (branch addresses)، والأسعار المنشورة (published rates) |
| **داخلي (Internal)** | للموظفين فقط، وضرر منخفض إن تسرّب (staff only, low harm if leaked) | رموز المنتجات (product codes)، والأحجام اليومية المجمّعة (aggregated daily volumes) |
| **سرّي (Confidential)** | ضرر للعملاء أو للبنك إن تسرّب (harm to customers or the bank if leaked) | أرصدة الحسابات (account balances)، والشريحة (segment)، ودرجات الائتمان (credit scores)، ومفتاح العميل (customer key) |
| **مقيّد (Restricted)** | ضرر جسيم؛ ويخضع لرقابة مشددة (serious harm; tightly controlled) | رقم الهوية الوطنية (national ID)، وأرقام البطاقات (card numbers)، والراتب (salary)، وبيانات الفئات الخاصة (special-category data)، وبيانات المصادقة (authentication data) |

فوق المستوى، تحمل الأعمدة **وسومًا (tags)**: `pii:direct`، و`pii:quasi`، و`pii:special`، و`pci` ‏(بيانات البطاقات بموجب معيار أمن بيانات صناعة بطاقات الدفع (card data under the Payment Card Industry Data Security Standard))، و**فئة الاحتفاظ (retention class)**. تعيش الوسوم في كتلة `meta` الخاصة بـ dbt من الدرس 6.1، فتتدفق إلى الفهرس (catalogue) وسياسات الوصول (access policies).

**المبادئ وقد تحوّلت إلى قرارات هندسية (The principles turned into engineering decisions).** تسرد المادة 5 من اللائحة (GDPR Article 5) المبادئ؛ ومعظم قوانين الخصوصية الحديثة (modern privacy laws)، بما فيها قوانين دول مجلس التعاون الخليجي (GCC)، تشاركها روحها (share their spirit). ويصبح كل مبدأ قرارًا في المنصة (platform decision):

| المبدأ (Principle (GDPR Art. 5)) | ما يعنيه لمنصة البيانات (What it means for the data platform) |
|---|---|
| المشروعية والإنصاف والشفافية (Lawfulness, fairness and transparency) | يسجّل كل خط بيانات (pipeline) غرضه وأساسه القانوني (purpose and legal basis)، بالاتفاق مع مسؤول حماية البيانات (DPO) |
| تحديد الغرض (Purpose limitation) | لا يُعاد استخدام بيانات الاحتيال (fraud data) للتسويق (marketing) دون تقييم جديد (new assessment) |
| تقليل البيانات (Data minimisation) | حمّل واكشف فقط الأعمدة التي يحتاجها الغرض (only the columns a purpose needs) |
| الدقة (Accuracy) | اختبارات الجودة (quality tests) ‏(3.2)؛ والتصحيحات تتدفق إلى المصبّ (corrections flow downstream) |
| تحديد مدة التخزين (Storage limitation) | لكل جدول فئة احتفاظ (retention class) ومهمة حذف (deletion job) |
| السلامة والسرّية (Integrity and confidentiality) | التحكم في الوصول (access control)، والتشفير (encryption)، والتدقيق (audit) ‏(6.3) |
| المساءلة (Accountability) | أدلة يمكنك عرضها (evidence you can show): التصنيف (classification)، والنسب (lineage)، وتشغيلات الاحتفاظ (retention runs)، وسجلات الوصول (access logs) |

**القوانين، في سطر واحد لكل منها (The laws, in one line each)** (هذا توجيه عام لا استشارة قانونية (orientation, not legal advice)؛ فسارة والمستشار القانوني (legal counsel) هم من يقرّرون):
- **اللائحة العامة لحماية البيانات (GDPR)** ‏(اللائحة (الاتحاد الأوروبي) 2016/679 (Regulation (EU) 2016/679)) تغطي بيانات عملاء نجم في الاتحاد الأوروبي (EU customers' data) وتمنح الأشخاص حقوقًا منها الوصول (access) ‏(المادة 15)، والمحو (erasure) ‏(المادة 17)، وقابلية النقل (portability) ‏(المادة 20)، إضافة إلى حماية البيانات بالتصميم وبصورة افتراضية (data protection by design and by default) ‏(المادة 25).
- **قانون حماية خصوصية البيانات الشخصية في قطر (Qatar's PDPPL)**، القانون رقم 13 لسنة 2016 بشأن حماية خصوصية البيانات الشخصية (Law No. 13 of 2016 on the protection of personal data privacy)، يغطي المعالجة في قطر (processing in Qatar)؛ ولمركز قطر للمال (Qatar Financial Centre) لوائحه الخاصة.
- **الإمارات (The UAE)** لديها المرسوم بقانون اتحادي رقم 45 لسنة 2021 بشأن حماية البيانات الشخصية (Federal Decree-Law No. 45 of 2021 on personal data protection)؛ وللمنطقتين الحرتين مركز دبي المالي العالمي (DIFC) وسوق أبوظبي العالمي (ADGM) أنظمتهما الخاصة (their own regimes).
- **القواعد المصرفية (Banking rules)** تضيف واجبات سرّية (confidentiality duties)، وغالبًا ما يضع المشرفون الإقليميون (regional supervisors) توقعات بشأن أين يجوز تخزين بيانات العملاء ومعالجتها (**توطين البيانات (data residency)**). وهذه تختلف وتتغيّر؛ فتحقّق من القواعد الحالية قبل أن تقرّر أين تعيش النسخة (where a copy lives).

وللتفاصيل القانونية (legal detail)، راجع [*حوكمة الذكاء الاصطناعي: من الصفر إلى الاحتراف (AI Governance: Zero to Hero)*، الدرس 4.1 — مبادئ حماية البيانات تلتقي بالذكاء الاصطناعي (Data protection principles meet AI)](../aigp/index.ar.html#/4.1) و[*حوكمة الذكاء الاصطناعي: من الصفر إلى الاحتراف (AI Governance: Zero to Hero)*، الدرس 4.3 — تقييمات أثر حماية البيانات وخريطة الخصوصية العالمية، من الاتحاد الأوروبي إلى الخليج (DPIAs and the global privacy map, from the EU to the GCC)](../aigp/index.ar.html#/4.3).

### 🟡 التعمق أكثر (Going deeper)

**صندوق أدوات الحماية (The toolbox of protections).** من الأقوى إلى الأضعف من حيث الخصوصية (from strongest to weakest for privacy):

| التقنية (Technique) | ماذا تفعل (What it does) | هل تبقى بيانات شخصية؟ ⁦(Still personal data?)⁩ | الاستخدام في نجم (Use at Najm) |
|---|---|---|---|
| **عدم الجمع أو النسخ (Don't collect or copy)** | إسقاط العمود وقت التحميل (drop the column at load time) | لا بيانات على الإطلاق (no data at all) | الافتراضي لكل نسخة تجريبية (default for every sandbox copy) |
| **التجميع مع العتبات (Aggregation with thresholds)** | الإبلاغ عن الأعداد والمجاميع (counts and sums)، وحجب المجموعات الصغيرة (suppress small groups) | عادةً لا، إن كانت المجموعات كبيرة بما يكفي (if groups are large enough) | لوحات المعلومات خارج فريق البيانات (dashboards outside the data team) |
| **التعميم (Generalisation)** | تاريخ الميلاد إلى فئة عمرية (birth date to age band)، والعنوان إلى مدينة (address to city) | غالبًا نعم (often yes) | متاجر التحليلات (analytics marts) |
| **الأسماء المستعارة (Pseudonymisation)** | استبدال المعرِّفات بتجزئات مُفتاحية أو رموز مميّزة (keyed hashes or tokens) | **نعم (Yes)** ‏(المادة 4(5) من اللائحة (GDPR Art. 4(5))) | الربط بين مجموعات البيانات دون كشف الهوية (joins across datasets without revealing identity) |
| **الإخفاء (Masking)** | إظهار قيم جزئية (show partial values) ‏(`+974 55** **12`) | نعم (Yes) | الشاشات التشغيلية (operational screens)، والدعم (support) |

**الأسماء المستعارة بالطريقة الخاطئة، وبالطريقة الصحيحة (Pseudonymisation done wrong, and right).** خطأ هدى هو الأكثر شيوعًا في هندسة البيانات (the most common one in data engineering):

```python
import hashlib, hmac

# WRONG: unsalted hash. National IDs have a small, structured value space,
# so an attacker hashes every possible ID and looks the result up.
pseudo_id = hashlib.md5(national_id.encode()).hexdigest()

# RIGHT: keyed hash (HMAC-SHA-256). Without the secret key, which lives in
# the secrets manager and never in code, the values cannot be recomputed.
def pseudonymise(value: str, key: bytes) -> str:
    normalised = value.strip().upper()
    return hmac.new(key, normalised.encode(), hashlib.sha256).hexdigest()
```

التجزئة المُفتاحية حتمية (the keyed hash is deterministic)، فيحصل العميل نفسه على الاسم المستعار نفسه في كل مكان (the same pseudonym everywhere) وتظل عمليات الربط (joins) تعمل. ومن دون المفتاح لا يمكن إعادة حسابها (cannot be recomputed)؛ ومعه يستطيع أي شخص إعادة الربط (re-link)، لذا تبقى النتيجة بيانات شخصية (still personal data). وعندما يتعيّن على بعض الأشخاص استرجاع القيمة الحقيقية (recover the real value) ‏(محقّق احتيال (fraud investigator))، استخدم **الترميز (tokenisation)**: خزنة (vault) تحفظ الربط بين الرمز والقيمة (token-to-value mapping) ولا يجوز البحث فيها إلا للخدمات المخوّلة (authorised services). وتوفّر إضافة `pgcrypto` في PostgreSQL ‏(PostgreSQL's extension) الدالة `hmac()` لإجراء التجزئة المُفتاحية نفسها في SQL.

**عروض مُخفاة للمحلّلين (Masked views for analysts).** نادرًا ما يحتاج المحلّلون (analysts) إلى المعرِّفات المباشرة (direct identifiers). أعطهم عرضًا (view) يعمّم البيانات (generalises) ولا يُظهر المعرِّفات إلا لدور معتمد (approved role):

```sql
-- Analysts get SELECT on this view only, never on marts.customer_360
CREATE VIEW marts.customer_360_analyst AS
SELECT
    customer_key,                           -- surrogate key, no meaning outside Najm
    segment,
    country_code,
    date_part('year', age(date_of_birth))::int / 10 * 10 AS age_band,
    CASE WHEN pg_has_role(current_user, 'pii_reader', 'MEMBER')
         THEN phone
         ELSE left(phone, 4) || '******' || right(phone, 2)
    END AS phone
FROM marts.customer_360;
```

هذا هو **الإخفاء الديناميكي للبيانات (dynamic data masking)**: الاستعلام نفسه يُرجع قيمًا مختلفة بحسب من يشغّله (depending on who runs it). تبنيه مستودعات البيانات المُدارة (managed warehouses) في داخلها (سياسات الإخفاء (masking policies) أو وسوم السياسات (policy tags))، وفي PostgreSQL تضيف الإضافة مفتوحة المصدر **PostgreSQL Anonymizer** قواعد تصريحية (declarative rules). ويتناول الدرس 6.3 من يحصل على `pii_reader`.

**الاحتفاظ والحذف (Retention and deletion).** يعطي **جدول الاحتفاظ (retention schedule)**، الذي يُقرَّر مع مسؤول حماية البيانات (DPO) والشؤون القانونية (legal)، كل فئة مدةً ومُطلِقًا (a period and a trigger)، مثل "سجلات الحسابات المغلقة: المدة التي تقتضيها القواعد المصرفية وقواعد مكافحة غسل الأموال، من تاريخ الإغلاق" ("closed account records: the period required by banking and anti-money-laundering rules, from closure"). والهندسة هي التي تجعل الحذف حقيقيًا (engineering makes deletion real):
- **قسّم حسب ساعة الاحتفاظ (Partition by the retention clock)** ‏(تاريخ الحدث (event date)، تاريخ الإغلاق (closure date))، بحيث يكون الحذف `DROP` للأقسام القديمة (old partitions)، لا `DELETE` بطيئًا.
- **جداول المستودع البحيري تحتفظ بالتاريخ (Lakehouse tables keep history).** في Delta Lake وApache Iceberg، تظل اللقطات القديمة (old snapshots) تحمل الصفوف المحذوفة لأغراض السفر عبر الزمن (time travel) حتى تشغّل `VACUUM` ‏(Delta) أو تُنهي صلاحية اللقطات (expire snapshots) ‏(Iceberg)، وهو ما يحذف ملفات البيانات التي لم يعد يُشار إليها (data files no longer referenced).
- **النسخ تُحسب (Copies count).** النسخ الاحتياطية (backups)، والبيئات التجريبية (sandboxes)، وتصديرات CSV ‏(CSV exports)، ومخازن الخصائص (feature stores) كلها تحمل بيانات شخصية أيضًا.

**طلبات المحو (Erasure requests).** المحو ليس دائمًا "احذف كل شيء" ("delete everything"): فالبنوك ملزمة قانونًا بالاحتفاظ ببعض السجلات (must keep some records by law)، والمادة 17 تسمح بذلك. وتحتاج المنصة إلى إجراء قابل للتكرار (repeatable procedure): اعثر على كل موقع من النسب (find every location from lineage) ‏(6.1)، واحذف أو استخدم الأسماء المستعارة (delete or pseudonymise) حيث لا ينطبق واجب احتفاظ (no duty to keep applies)، وسجّل الأدلة (record evidence).

```mermaid
flowchart RL
    A["عمود المصدر<br/>(Source column)"] --> B["التصنيف والوسم في البيانات الوصفية<br/>(Classify and tag in meta)"]
    B --> C["التحميل: إسقاط الأعمدة غير المطلوبة<br/>(Load: drop unneeded columns)"]
    C --> D["استبدال المعرِّفات بأسماء مستعارة<br/>(Pseudonymise identifiers)"]
    D --> E["عروض مُخفاة حسب الدور<br/>(Masked views by role)"]
    D --> F["فئة الاحتفاظ ومهمة الحذف<br/>(Retention class and deletion job)"]
    F --> G["أدلة لمسؤول حماية البيانات<br/>(Evidence for the DPO)"]
```

### 🔴 نظرة الخبير (Expert view)

**التجهيل ادّعاء يجب أن تدافع عنه (Anonymisation is a claim you must defend).** تستثني الحيثية 26 من اللائحة (GDPR Recital 26) البيانات المجهولة (anonymous data): البيانات التي لم يعد ممكنًا فيها التعرّف على الأشخاص بوسائل يُرجَّح استخدامها على نحو معقول (by means reasonably likely to be used). والسقف مرتفع (the bar is high). فقد أظهرت Latanya Sweeney في أواخر التسعينيات أن الرمز البريدي (ZIP code) وتاريخ الميلاد والجنس معًا تحدّد بشكل فريد (uniquely identify) نسبة كبيرة من الأمريكيين، وفي عام 2008 أعاد Narayanan وShmatikov التعرّف على مستخدمين (re-identified users) في مجموعة بيانات جائزة Netflix "المجهّلة" ("anonymised" Netflix Prize dataset) بربطها بمراجعات عامة (public reviews). وتساعد المقاربات الرسمية (formal approaches):
- **إخفاء الهوية من الدرجة k ‏(k-anonymity)**: يشترك كل سجل في قيم أشباه المعرِّفات (quasi-identifier values) مع ما لا يقل عن *k − 1* سجلات أخرى؛ تحقّق من ذلك بـ `GROUP BY` و`HAVING COUNT(*) < k`. ومع ذلك قد يسرّب سمةً يشترك فيها كل من في المجموعة (an attribute everyone in a group shares)، وهو ما يعالجه **التنوّع من الدرجة l ‏(l-diversity)**.
- **الخصوصية التفاضلية (Differential privacy)**: ضوضاء معايَرة (calibrated noise) في نتائج الاستعلام بحيث لا يكاد أي شخص بمفرده يغيّر المُخرَج (any one person barely changes the output)؛ وتناسب الإحصاءات المنشورة (published statistics).
- **البيانات الاصطناعية (Synthetic data)**: سجلات مولَّدة تحاكي الإحصاءات الحقيقية (generated records mimicking real statistics)؛ جيدة للاختبارات (good for tests)، لكن المولّدات (generators) قد تحفظ سجلات حقيقية نادرة (memorise rare real records).

لذا فالافتراض الافتراضي في نجم (the default assumption) هو "أسماء مستعارة، ولا تزال شخصية" ("pseudonymised, still personal")، وأي مجموعة بيانات "مجهولة" تحتاج إلى اعتماد سارة (Sara's sign-off).

**النص الحر وبيانات النماذج اللغوية الكبيرة (Free text and LLM data).** تحمل سجلات نجم أسيست (Najm Assist logs) ومستندات مساعد مذكرات الائتمان (Credit Memo Copilot documents) ‏(5.3) بيانات شخصية في صورة غير مهيكلة (unstructured form). اكتشفها قبل أن تصل إلى مستودع البيانات (warehouse) أو الفهرس المتّجهي (vector index): أنماط (patterns) لأرقام الهوية والهواتف وأرقام الحسابات المصرفية الدولية (IDs, phones and IBANs)، والتعرّف على الكيانات المسمّاة (named-entity recognition) للأسماء (و**Microsoft Presidio** مثال مفتوح المصدر (open-source example)). والاكتشاف غير مثالي (detection is imperfect)، لذا أضف التحكم في الوصول (access control) ومدة احتفاظ قصيرة (short retention) للسجلات الخام (raw logs). راجع [*أمن الذكاء الاصطناعي وأمن التطبيقات: من الصفر إلى الاحتراف (Secure AI & Application Security: Zero to Hero)*، الدرس 5.3 — حماية البيانات الشخصية: التقليل والتسجيل وهندسة الخصوصية (Protecting personal data: minimisation, logging and privacy engineering)](../secai/index.ar.html#/5.3).

**التمزيق التشفيري (Crypto-shredding).** للمخازن التي يصعب فيها الحذف (where deletion is hard) ‏(السجلات التي تقبل الإلحاق فقط (append-only logs)، والاحتفاظ الطويل في Kafka ‏(long Kafka retention)، والنسخ الاحتياطية (backups))، شفّر الحقول الحساسة لكل عميل بمفتاح خاص به (per-customer key) واحذف المفتاح عند المحو (delete the key on erasure). أما هل يُعدّ ذلك محوًا (counts as erasure) في حالة بعينها فأمر يقرّره مسؤول حماية البيانات (DPO).

**مُنتَجات المساءلة (Accountability artefacts).** تشترط المادة 30 من اللائحة (GDPR Article 30) سجلات أنشطة المعالجة (records of processing)، وتشترط المادة 35 تقييم أثر حماية البيانات (data protection impact assessment, DPIA) للمعالجة عالية المخاطر (high-risk processing). ولّد أدلتها (generate their evidence) ‏(الوسوم (tags)، والنسب (lineage)، وسجلات الاحتفاظ والوصول (retention and access logs)) من المنصة، لا يدويًا (not by hand).

## 🧰 الأدوات (The toolkit)
| الأداة أو النمط أو المعيار (Tool, pattern or standard) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **Data classification scheme** — مخطط تصنيف البيانات | مستويات حساسية (sensitivity levels) إضافة إلى وسوم (tags) ‏(PII، وPCI، وفئة الاحتفاظ (retention class)) على كل عمود | قبل نشر أي مجموعة بيانات (before any dataset is published)؛ ويقود الإخفاء والوصول والاحتفاظ (drives masking, access and retention) |
| **Pseudonymisation** (keyed hashing, tokenisation) — الأسماء المستعارة (التجزئة المُفتاحية، الترميز) | يستبدل المعرِّفات (identifiers) بقيم لا يمكن عكسها دون مفتاح أو خزنة (cannot be reversed without a key or vault) | ربط مجموعات بيانات عن العميل نفسه دون كشف الهوية (without exposing identity) |
| **Dynamic data masking** — الإخفاء الديناميكي للبيانات | يُرجع قيمًا مُخفاة أو واضحة (masked or clear values) بحسب دور المستدعي (caller's role) | المتاجر المشتركة (shared marts) التي يستخدمها أشخاص باحتياجات مختلفة (different needs) |
| **PostgreSQL Anonymizer** | إضافة PostgreSQL مفتوحة المصدر (open-source PostgreSQL extension) للإخفاء التصريحي (declarative masking) والتفريغات المجهّلة (anonymised dumps) | العروض المُخفاة (masked views) ونسخ الاختبار الآمنة (safe test copies) من PostgreSQL |
| **Microsoft Presidio** | إطار عمل مفتوح المصدر (open-source framework) لاكتشاف المعلومات الشخصية المعرِّفة وتنقيحها في النصوص (detecting and redacting PII in text) | سجلات الدردشة (chat logs)، والملاحظات (notes)، والمستندات (documents) قبل أن تصل إلى التحليلات (analytics) أو إلى فهرس متّجهي (vector index) |
| **Retention schedule** — جدول الاحتفاظ | مدد ومُطلِقات لكل فئة احتفاظ (periods and triggers per retention class)، تُنفَّذ بوصفها مهام حذف (deletion jobs) | كل جدول يحمل بيانات شخصية، بما في ذلك البيئات التجريبية والنسخ الاحتياطية (sandboxes and backups) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
تنشر سارة ولينا **معيار نجم للتعامل مع البيانات الشخصية، الإصدار 1 (Najm Personal Data Handling Standard v1)** لمنصة البيانات (data platform). ولبّه جدول تصنيف (classification table) لـ `core.customers` ومصفوفة تعامل (handling matrix).

**الجزء أ: تصنيف `core.customers` ‏(مقتطف) (Part A: classification (excerpt))**

| العمود (Column) | المستوى (Level) | الوسوم (Tags) | في رؤية العميل الشاملة؟ ⁦(In customer 360?)⁩ | عرض المحلّل (Analyst view) | فئة الاحتفاظ (Retention class) |
|---|---|---|---|---|---|
| `customer_id` | سرّي (Confidential) | `pii:direct` | يُحوَّل إلى اسم مستعار هو `customer_key` ‏(Pseudonymised) | `customer_key` | R-ACCOUNT |
| `national_id` | مقيّد (Restricted) | `pii:direct` | تجزئة مُفتاحية فقط (Keyed hash only) | غير معروض (Not shown) | R-ACCOUNT |
| `phone` | مقيّد (Restricted) | `pii:direct` | نعم (Yes) | مُخفى ما لم يكن المستخدم `pii_reader` ‏(Masked unless) | R-ACCOUNT |
| `date_of_birth` | سرّي (Confidential) | `pii:quasi` | نعم (Yes) | فئة عمرية (Age band) | R-ACCOUNT |
| `nationality` | سرّي (Confidential) | `pii:quasi` | نعم (Yes) | معروض، مع حجب المجموعات الصغيرة في لوحات المعلومات (Shown, small groups suppressed in dashboards) | R-ACCOUNT |
| `monthly_salary` | مقيّد (Restricted) | `pii:quasi` | مُصنَّف في شرائح (Banded) | شريحة الراتب (Salary band) | R-ACCOUNT |

**الجزء ب: مصفوفة التعامل (Part B: handling matrix)**

| المستوى (Level) | نسخة تجريبية (Sandbox copy) | لوحات المعلومات (Dashboards) | التصدير خارج المنصة (Export outside platform) | بيئات الاختبار (Test environments) |
|---|---|---|---|---|
| داخلي (Internal) | مسموح (Allowed) | مسموح (Allowed) | بموافقة المالك (With owner approval) | مسموح (Allowed) |
| سرّي (Confidential) | مسجّلة الغرض، تنتهي بعد 30 يومًا (Purpose-registered, 30-day expiry) | مجاميع؛ وتُحجب المجموعات الأقل من 10 (Aggregates; groups below 10 suppressed) | موافقة مسؤول حماية البيانات (DPO approval) | بيانات اصطناعية أو ذات أسماء مستعارة فقط (Synthetic or pseudonymised only) |
| مقيّد (Restricted) | لا يُسمح بها أبدًا بنص واضح؛ تجزئة مُفتاحية فقط (Never in clear; keyed hash only) | لا يُسمح بها أبدًا على مستوى الصف (Never at row level) | لا يُسمح به أبدًا دون موافقة مسؤول حماية البيانات ومالك البيانات (Never without DPO and data owner approval) | لا يُسمح بها أبدًا؛ بيانات اصطناعية فقط (Never; synthetic only) |

**الجزء ج: القواعد (Part C: rules).** تُنشأ المخططات التجريبية (sandbox schemas) بنص برمجي (script) يسجّل المالك والغرض وتاريخ انتهاء الصلاحية (owner, purpose and expiry)؛ وتُسقط مهمة ليلية (nightly job) المنتهي منها. والأعمدة الجديدة غير المصنّفة (unclassified new columns) تُفشل التكامل المستمر (fail CI). وجداول المستودع البحيري (lakehouse tables) التي تحمل بيانات شخصية تُنهي صلاحية لقطاتها أسبوعيًا (expire snapshots weekly). ولا يُدوَّر سرّ التجزئة المُفتاحية (keyed-hash secret rotates) إلا مع خطة إعادة ترميز بالمفتاح (re-keying plan)، لأن التدوير يغيّر كل اسم مستعار (rotation changes every pseudonym).

## 🛠️ التمارين (Exercises)
استخدم بيانات اصطناعية فقط (synthetic data only) ‏(مولَّدة مثلًا بمكتبة Faker في Python ‏(Python Faker library)). لا تستخدم أبدًا بيانات شخصية حقيقية (real personal data) في هذه التمارين.

- 🟢 ولّد بمكتبة Faker جدول عملاء اصطناعيًا (synthetic customer table) من 20 عمودًا. صنّف كل عمود بمستوى ووسوم وفئة احتفاظ (a level, tags and a retention class)، وحدّد لغرض "تحليل دوافع الشكاوى" ("analyse complaint drivers") أيّ الأعمدة مطلوبة. *يكتمل عندما (Done when):* يكون كل عمود مصنّفًا ولا يحتاج غرضك إلى أكثر من ثلثها (no more than a third of them).
- 🟡 في PostgreSQL أو DuckDB، حمّل جدولك الاصطناعي وابنِ عرضًا للمحلّل (analyst view) فيه مفتاح عميل بتجزئة مُفتاحية (keyed-hash customer key)، وفئة عمرية (age band)، وهاتف مُخفى (masked phone). ثم بيّن ضعف التجزئة البسيطة (weakness of plain hashing): جزّئ بـ MD5 ‏(MD5-hash) رقم هوية وهميًا من ست خانات (fake six-digit ID) واسترجعه بتجزئة كل المرشحين المليون (all one million candidates). *يكتمل عندما (Done when):* تعمل عمليات الربط على التجزئة المُفتاحية (joins on the keyed hash) عبر جدولين، ويسترجع نصّك البرمجي الهوية المجزّأة بـ MD5 لكنه لا يسترجع الهوية المجزّأة بالتجزئة المُفتاحية (but not the keyed one).
- 🔴 ابنِ مهمة احتفاظ ومحو (retention and erasure job) لجدول PostgreSQL مقسَّم حسب الشهر (partitioned by month): أسقط الأقسام الأقدم من مدة الاحتفاظ (drop partitions older than the retention period)، ونفّذ إجراء محو (erasure procedure) لعميل واحد يحوّله إلى اسم مستعار في ثلاثة جداول ويكتب سجلّ أدلة (evidence record) ‏(من، ومتى، وأيّ الجداول، والصفوف المتأثرة (who, when, which tables, rows affected)). *يكتمل عندما (Done when):* يعطي تشغيل المهمة مرتين النتيجة نفسها (the same result)، ويُظهر جدول الأدلة (evidence table) كل تشغيل، ولا يُرجع فحص إخفاء الهوية من الدرجة k ‏(k-anonymity check) ‏(`GROUP BY` على أشباه المعرِّفات (quasi-identifiers) `HAVING COUNT(*) < 5`) على مجموعة بياناتك المنشورة (released dataset) أي صفوف.

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **"جزّأناها، إذن هي مجهولة" ⁦("We hashed it, so it is anonymous.")⁩** التجزئات البسيطة (plain hashes) للقيم الصغيرة المهيكلة (small, structured values) قابلة للعكس بالقوة الغاشمة (reversible by brute force)، وحتى التجزئات المُفتاحية (keyed hashes) هي أسماء مستعارة لا بيانات مجهولة (pseudonymous, not anonymous). استخدم التجزئات المُفتاحية أو الرموز المميّزة (tokens) وعامل المُخرَج بوصفه بيانات شخصية (personal data).
- **نسخ جداول كاملة "احتياطًا" (Copying whole tables "just in case").** كل عمود إضافي مخاطرة بلا فائدة (risk with no benefit). اختر الأعمدة حسب الغرض وقت التحميل (select columns by purpose at load time).
- **نسيان النسخ (Forgetting the copies).** البيئات التجريبية (sandboxes)، والتصديرات (exports)، والنسخ الاحتياطية (backups)، والفهارس المتّجهية (vector indexes) تحمل بيانات شخصية أيضًا. تتبّعها في النسب (track them in lineage) وأعطها تواريخ انتهاء صلاحية (expiry dates).
- **الاعتقاد بأن `DELETE` يحذف (Believing it deletes).** في صيغ المستودع البحيري (lakehouse formats)، تحتفظ اللقطات القديمة (old snapshots) بالصفوف حتى تنظّفها أو تُنهي صلاحيتها (vacuum or expire them). جدوِل ذلك وتحقّق منه (schedule that and verify it).
- **مهندسون يقرّرون القانون (Engineers deciding the law).** الأساس القانوني (legal basis)، ومدد الاحتفاظ (retention periods)، واستثناءات المحو (erasure exceptions) أمور يقرّرها مسؤول حماية البيانات (DPO) والمستشار القانوني (legal counsel)؛ وأنت تنفّذها وتُنتج الأدلة (produce evidence).

## 🧾 الخلاصة (Recap)
- تشمل البيانات الشخصية (personal data) المعرِّفات المباشرة (direct identifiers)، وأشباه المعرِّفات (quasi-identifiers)، والفئات الخاصة (special categories)، وغالبًا ما تختبئ في النص الحر (free text).
- صنّف كل عمود بمستوى ووسوم في الشيفرة (a level and tags in code)، ودع التصنيف يقود الإخفاء والوصول والاحتفاظ وفحوص التكامل المستمر (masking, access, retention and CI checks).
- قلّل أولًا (minimise first)، ثم استخدم الأسماء المستعارة بتجزئات مُفتاحية أو رموز مميّزة (pseudonymise with keyed hashes or tokens)، وأخفِ حسب الدور (mask by role)، وجمّع مع العتبات (aggregate with thresholds).
- يحتاج الاحتفاظ (retention) إلى التقسيم حسب ساعة الاحتفاظ (partitioning by the retention clock)، وإنهاء صلاحية اللقطات (snapshot expiry) في المستودعات البحيرية، وتغطية كل نسخة (coverage of every copy).
- تضع اللائحة العامة لحماية البيانات (GDPR)، وقانون حماية خصوصية البيانات الشخصية في قطر (Qatar's PDPPL)، وقوانين الإمارات (the UAE's laws) القواعد؛ والتجهيل (anonymisation) سقف مرتفع (a high bar)، ومسؤول حماية البيانات (DPO) هو من يقرّر.

## ✍️ اختبر نفسك (Check yourself)

**1. تستبدل هدى كل رقم هوية وطنية (national ID) بتجزئة MD5 غير مملّحة (unsalted MD5 hash) له وتصف الجدول بأنه "مجهّل (anonymised)". ما المشكلة الرئيسية؟**

- A. مُخرَج MD5 ‏(MD5 output) أطول من أن يُخزَّن بكفاءة في عمود يُستخدم للربط (used for joins)
- B. التجزئة تُلغي القدرة على ربط الجداول على العميل (join tables on the customer)
- C. يمكن عكس التجزئات بتجزئة كل رقم هوية ممكن (hashing every possible ID)، لذا ليست البيانات مجهولة (not anonymous)
- D. تجزئة البيانات الشخصية محظورة تمامًا (prohibited outright) بموجب اللائحة العامة لحماية البيانات (GDPR)

<details><summary>الإجابة</summary>

**C.** يستطيع المهاجم (attacker) أن يجزّئ كل الهويات الممكنة ويطابقها عكسيًا (match them back). B خاطئة: فالتجزئة الحتمية (deterministic hash) تظل تدعم الربط (supports joins). وD خاطئة: التجزئة مسموحة، لكنها ببساطة ليست تجهيلًا (not anonymisation). (🟡 التعمق أكثر (Going deeper).)

</details>

**2. بموجب اللائحة العامة لحماية البيانات (GDPR)، كيف ينبغي لنجم أن تعامل مجموعة بيانات استُبدلت فيها معرّفات العملاء (customer IDs) بقيم HMAC-SHA-256 ‏(HMAC-SHA-256 values) بمفتاح سرّي (secret key) يحتفظ به فريق المنصة (platform team)؟**

- A. بوصفها بيانات شخصية (personal data)، لأن حامل المفتاح (key holder) يستطيع إعادة ربطها (re-link it)
- B. بوصفها بيانات مجهولة خارج نطاق اللائحة (anonymous data outside the GDPR's scope)، لأنه لا يظهر أي رقم هوية
- C. بوصفها بيانات فئة خاصة (special-category data) تحتاج إلى حماية المادة 9 (Article 9 protection)
- D. بوصفها بيانات عامة (public data) بعد تدوير المفتاح (once the key is rotated)، لأن الأسماء المستعارة القديمة لم تعد تتطابق

<details><summary>الإجابة</summary>

**A.** البيانات ذات الأسماء المستعارة تبقى بيانات شخصية (pseudonymised data remains personal data) ‏(المادة 4(5) والحيثية 26 (Article 4(5) and Recital 26)). B هي الخطأ المغري (tempting mistake)؛ فالتجهيل (anonymisation) يحتاج إلى أكثر من ذلك بكثير. (🟢 الأساسيات (The essentials)، 🔴 نظرة الخبير (Expert view).)

</details>

**3. يحتاج كريم إلى لوحة معلومات (dashboard) للشكاوى حسب الجنسية والفرع (by nationality and branch) لفريق الإدارة التنفيذية للتجزئة (retail executive team). أيّ نهج يتوافق على أفضل وجه مع تقليل البيانات (data minimisation)؟**

- A. تصدير على مستوى الصف (row-level export) للشكاوى مع أسماء العملاء كي يتمكن الفريق من المتابعة (follow up)
- B. لوحة معلومات على جدول العملاء الكامل (full customer table)، مع تصفية وقت العرض (filtered at view time)
- C. لوحة معلومات تُخفي عمود الجنسية (hides the nationality column)
- D. لوحة معلومات مجمّعة (aggregated dashboard) تحجب المجموعات الأصغر من عتبة متفق عليها (agreed threshold)

<details><summary>الإجابة</summary>

**D.** التجميع مع حجب المجموعات الصغيرة (aggregation with small-group suppression) يجيب عن السؤال دون كشف الأفراد (without exposing individuals)؛ وإلا فقد تحدّد أزواج الجنسية والفرع النادرة (rare nationality-branch pairs) هوية أشخاص. A وB تكشفان أكثر بكثير من اللازم؛ وC تزيل البُعد نفسه (the very dimension) الذي يسأل عنه السؤال. (🟡 التعمق أكثر (Going deeper)؛ 🏛️ الجزء ب (Part B).)

</details>

**4. تشغّل لينا `DELETE` على جدول Apache Iceberg ‏(Apache Iceberg table) للعملاء الذين انتهت مدة احتفاظهم (retention period has ended). ما الذي يجب أن يحدث أيضًا قبل أن تزول البيانات فعليًا (physically gone)؟**

- A. لا شيء؛ ففي Iceberg يزيل `DELETE` ملفات البيانات الأساسية (underlying data files) فورًا
- B. إنهاء صلاحية اللقطات القديمة (expire old snapshots) لتُحذف ملفات البيانات غير المُشار إليها (unreferenced data files)، وتنظيف النسخ (clean up copies)
- C. إعادة تسمية الجدول (rename the table) كي لا تعود استعلامات السفر عبر الزمن (time-travel queries) قادرة على العثور على الصفوف القديمة
- D. إعادة تشغيل نماذج dbt التي تقرأ الجدول (re-run the dbt models) كي تُعاد بناء المتاجر في المصبّ (downstream marts)

<details><summary>الإجابة</summary>

**B.** اللقطات الأقدم المحفوظة للسفر عبر الزمن (older snapshots kept for time travel) تظل تحمل الصفوف المحذوفة حتى تنتهي صلاحيتها وتُزال الملفات (VACUUM في Delta Lake ‏(VACUUM in Delta Lake)). والنسخ تحتاج إلى حذف خاص بها (their own deletion). (🟡 التعمق أكثر (Going deeper).)

</details>

**5. يطلب عميل لنجم في الاتحاد الأوروبي (EU customer) المحو (erasure). يجب الاحتفاظ ببعض سجلات معاملاته بموجب قواعد حفظ السجلات المصرفية (banking record-keeping rules). ماذا ينبغي أن تفعل منصة البيانات؟**

- A. حذف كل سجل فورًا، بما في ذلك السجلات التي يُلزم القانون البنك بالاحتفاظ بها
- B. رفض الطلب كله (refuse the whole request)، لأن بعض السجلات يجب الاحتفاظ بها قانونًا
- C. العثور على كل نسخة عبر النسب (find every copy via lineage)، والمحو حيث لا ينطبق واجب احتفاظ (no duty to keep)، وتقييد الباقي (restrict the rest)، وتسجيل الأدلة (record evidence)
- D. حذف صف العميل في `core.customers` فقط، لأن كل متجر يُعاد بناؤه منه (every mart rebuilds from it)

<details><summary>الإجابة</summary>

**C.** للحق في المحو (right to erasure) استثناءات، منها الالتزامات القانونية بالاحتفاظ (legal obligations to retain)، لذا فالإجابة إجراء دقيق متفق عليه مع مسؤول حماية البيانات (a precise procedure agreed with the DPO)، لا كل شيء أو لا شيء (not all or nothing). D مغرية لكنها تُغفل كل نسخة في المصبّ (every downstream copy). (🟡 التعمق أكثر (Going deeper).)

</details>

## 📚 المراجع (References)
- اللائحة (الاتحاد الأوروبي) 2016/679 (اللائحة العامة لحماية البيانات) (Regulation (EU) 2016/679 (General Data Protection Regulation)) — https://eur-lex.europa.eu/eli/reg/2016/679/oj
- قطر، القانون رقم 13 لسنة 2016 بشأن حماية خصوصية البيانات الشخصية (Qatar, Law No. 13 of 2016 on the protection of personal data privacy) — الميزان، البوابة القانونية القطرية (Al Meezan, Qatar Legal Portal): https://www.almeezan.qa/
- المرسوم بقانون اتحادي الإماراتي رقم 45 لسنة 2021 بشأن حماية البيانات الشخصية (UAE Federal Decree-Law No. 45 of 2021 on the protection of personal data) — https://u.ae/
- توثيق PostgreSQL: ‏pgcrypto ‏(PostgreSQL documentation: pgcrypto) — https://www.postgresql.org/docs/current/pgcrypto.html
- PostgreSQL Anonymizer — https://postgresql-anonymizer.readthedocs.io/
- Microsoft Presidio — https://microsoft.github.io/presidio/
- توثيق Delta Lake: ‏VACUUM ‏(Delta Lake documentation: VACUUM) — https://docs.delta.io/
- توثيق Apache Iceberg: الصيانة (إنهاء صلاحية اللقطات) (Apache Iceberg documentation: maintenance (expire snapshots)) — https://iceberg.apache.org/docs/latest/maintenance/
- Arvind Narayanan وVitaly Shmatikov، "Robust De-anonymization of Large Sparse Datasets" (إزالة التجهيل المتينة لمجموعات البيانات الكبيرة المتناثرة) ‏(IEEE Symposium on Security and Privacy، 2008)
- Latanya Sweeney، "k-anonymity: a model for protecting privacy" (إخفاء الهوية من الدرجة k: نموذج لحماية الخصوصية) ‏(International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems، 2002)

---

# 6.3 — تأمين منصة البيانات: التحكم في الوصول والأسرار والتدقيق والمشاركة الآمنة (Securing the data platform: access control, secrets, audit and sharing safely)
*المستوى (Level): 🔴 متقدم (Advanced)* · *المتطلبات (Prerequisites): 6.1، 6.2* · *المرحلة (Stage): Govern, Operate*

## ⚡ الدرس في دقيقة (In 60 seconds)
- تركّز منصة البيانات (data platform) أثمن بيانات البنك (the bank's most valuable data) في مكان واحد، لذا تحتاج إلى **أقل الصلاحيات (least privilege)**: يحصل كل شخص وكل خط بيانات (every person and every pipeline) على الحد الأدنى من الوصول الذي يحتاجه غرضه (the minimum access its purpose needs)، ولا شيء أكثر.
- امنح الوصول إلى **هويات مسمّاة عبر الأدوار (named identities through roles)**، لا عبر حسابات مشتركة (shared accounts) أبدًا. ورتّب الضوابط في طبقات (layer the controls): صلاحيات المخطط والجدول (schema and table grants)، و**أمن مستوى الصف (row-level security)**، وصلاحيات الأعمدة (column grants)، و**الإخفاء (masking)**.
- **الأسرار (secrets)** ‏(كلمات المرور (passwords)، والمفاتيح (keys)، والرموز المميّزة (tokens)) تعيش في مدير أسرار (secrets manager) وتصل إلى خطوط البيانات وقت التشغيل (at run time)؛ وفضّل بيانات الاعتماد قصيرة العمر (short-lived credentials) على كلمات المرور طويلة العمر (long-lived passwords).
- **سجلات التدقيق (audit logs)** تسجّل من قرأ ماذا ومن غيّر ماذا (who read and changed what)، وتُخزَّن حيث لا يستطيع أصحابها تعديلها (where their subjects cannot alter them)، وتغذّي التنبيهات للوصول غير المعتاد (alerts for unusual access).
- إشارة القرار (decision cue): لكل مسار وصول (access path) ‏(لوحة معلومات (dashboard)، ودفتر ملاحظات (notebook)، وتصدير (export)، وواجهة برمجة تطبيقات (API)، واسترجاع النماذج اللغوية الكبيرة (LLM retrieval))، اسأل: "هوية من التي يراها مستودع البيانات، وأيّ السياسات تنطبق عليها؟" ⁦("whose identity does the warehouse see, and which policies apply to it?")⁩
- أكبر فخ (biggest trap): حساب مستخدم خارق مشترك واحد (one shared superuser account) خلف كل خط بيانات ولوحة معلومات، ما يجعل التحكم في الوصول بلا معنى (access control meaningless) وسجلات التدقيق بلا فائدة (audit logs useless).

## 🧭 لماذا يهم (Why it matters)
يرسل التدقيق الداخلي (internal audit) إلى فيصل سؤالًا بسيطًا: "من اطّلع على راتب العميل 10-447-221 ورصيده الشهر الماضي؟" ⁦("Who viewed the salary and balance of customer 10-447-221 last month?")⁩ فقد اشتكى العميل، وهو رجل أعمال معروف (well-known business owner)، من أن قريبًا لأحد موظفي البنك كان يعرف تفاصيل عن أوضاعه المالية.

لا يستطيع فيصل الإجابة. تُظهر سجلات مستودع البيانات (warehouse logs) أن كل استعلام ذي صلة (every relevant query) شُغّل باسم `etl_admin`، وهو مستخدم خارق (superuser) أُنشئ قبل سنوات لتشغيل خطوط البيانات الأولى. وكلمة مروره موجودة في متغيّر Airflow ‏(Airflow variable)، وفي دفترَي ملاحظات أُودعا في git ‏(committed to git)، وفي إعدادات الاتصال (connection settings) لأداة ذكاء الأعمال (BI tool)، لذا تستعلم كل لوحة معلومات من مستودع البيانات باسم `etl_admin` أيضًا. يستخدمه ثلاثة وعشرون شخصًا وأربع عشرة مهمة (fourteen jobs). أمن مستوى الصف (row-level security) موجود على متجر مخاطر الائتمان (credit-risk mart)، لكن المستخدمين الخارقين يتجاوزونه (superusers bypass it). ولإحدى لوحات معلومات رؤية العميل الشاملة (customer 360 dashboard) أيضًا رابط مشاركة عام (public sharing link) يستطيع أي شخص لديه عنوان URL فتحه.

لا يوجد دليل على إساءة استخدام (no evidence of misuse)، ولا دليل على أي شيء آخر أيضًا. وهذه هي المشكلة: لا يستطيع البنك أن يُثبت من وصل إلى ماذا (who accessed what). يتفق سالم، رئيس هندسة المنصات (Head of Platform Engineering)، وفيصل على برنامج للربع (programme for the quarter): إحالة `etl_admin` إلى التقاعد (retire)، ومنح كل شخص وكل خط بيانات هويته الخاصة (its own identity)، ونقل الأسرار خارج الشيفرة (move secrets out of code)، وتفعيل تسجيل التدقيق (turn on audit logging)، وإغلاق الروابط العامة (close the public links). وهذا الدرس هو ذلك البرنامج.

## 📐 كيف يعمل (How it works)

### 🟢 الأساسيات (The essentials)

**ما الذي يمكن أن يسوء (What can go wrong).** الطرق الشائعة التي تتسرّب بها منصات البيانات (the common ways data platforms leak) عادية: وصول واسع أكثر من اللازم (access that is too broad)، وبيانات اعتماد مشتركة (shared credentials)، وأسرار مُودَعة في الشيفرة (secrets committed to code)، وتصديرات وروابط عامة (exports and public links)، وأشخاص لديهم وصول مشروع ينظرون إلى ما لا ينبغي لهم (people with legitimate access looking at what they should not) ‏(المطّلعون من الداخل (insiders))، وتخزين سيئ الإعداد (misconfigured storage) مثل حاوية تخزين كائنات عامة (public object-storage bucket). الهجمات المتقدمة (advanced attacks) مهمة، لكن هذه تأتي أولًا.

**المبادئ (The principles).**
- **أقل الصلاحيات (Least privilege):** امنح فقط ما يحتاجه الغرض (only what the purpose needs)، وطوال المدة التي يحتاجه فيها فقط.
- **الهويات المسمّاة (Named identities):** لكل إنسان وكل عبء عمل (every human and every workload) هويته الخاصة، بحيث يمكن تتبّع كل إجراء (every action can be traced). ويسجّل الأشخاص الدخول عبر مزوّد هوية الدخول الموحّد (single sign-on (SSO) identity provider) في البنك، لا بكلمات مرور محلية (local passwords).
- **الفصل بين المهام (Separation of duties):** الأشخاص الذين يبنون خطوط البيانات ليسوا تلقائيًا الأشخاص الذين يحق لهم قراءة البيانات المقيّدة (restricted data)؛ والأشخاص الذين يمنحون الوصول لا يعتمدون طلباتهم الخاصة (do not approve their own requests).
- **الدفاع في العمق (Defence in depth):** عدة طبقات مستقلة (several independent layers)، بحيث لا يكشف خطأ واحد كل شيء (one mistake does not expose everything).

**نماذج الوصول (Access models).**
- **التحكم في الوصول القائم على الأدوار (Role-based access control, RBAC):** تُمنح الصلاحيات للأدوار (permissions go to roles) ‏(`marts_reader`، `pii_reader`)، ويحصل الأشخاص على الأدوار. بسيط وقابل للتدقيق (simple and auditable).
- **التحكم في الوصول القائم على السمات (Attribute-based access control, ABAC):** تستخدم القرارات سمات الشخص (attributes of the person) ‏(البلد (country)، والفريق (team))، والبيانات (وسوم التصنيف (classification tags) من الدرس 6.2)، والسياق (context). فعبارة "يجوز للمحلّلين قراءة الأعمدة السرّية لعملاء بلدهم" ("Analysts may read confidential columns of their own country's customers") قاعدة واحدة بدلًا من عشرات الأدوار (dozens of roles).
- **أمن مستوى الصف (Row-level security, RLS):** يصفّي الصفوف التي يراها المستخدم (filters the rows a user sees)، مثلًا حسب البلد أو الفرع (by country or branch).
- **أمن مستوى العمود والإخفاء (Column-level security and masking):** يُخفي الأعمدة أو يحجبها جزئيًا (hides or masks columns) ‏(6.2) بناءً على الدور (based on the role).

**الوصول في PostgreSQL، طبقةً بعد طبقة (Access in PostgreSQL, layer by layer).** تحمل أدوار المجموعات (group roles) الصلاحيات؛ ويرثها الأشخاص وخطوط البيانات (people and pipelines inherit them).

```sql
-- Group roles: no login, they only hold permissions
CREATE ROLE marts_reader NOLOGIN;
CREATE ROLE pii_reader   NOLOGIN;

-- Named people (authenticated via SSO or certificates in production), never shared
CREATE ROLE kareem LOGIN;
GRANT marts_reader TO kareem;

-- Each pipeline gets its own identity, writing only to its own schema
CREATE ROLE svc_dbt_marts LOGIN;
GRANT USAGE, CREATE ON SCHEMA marts TO svc_dbt_marts;

-- Readers see curated views, not raw or base tables
GRANT USAGE ON SCHEMA marts TO marts_reader;
GRANT SELECT ON marts.customer_360_analyst, marts.loan_book TO marts_reader;
REVOKE ALL ON SCHEMA raw FROM PUBLIC;

-- Row-level security: analysts see only loans in countries they are scoped to
ALTER TABLE marts.loan_book ENABLE ROW LEVEL SECURITY;
ALTER TABLE marts.loan_book FORCE ROW LEVEL SECURITY;   -- applies to the table owner too
CREATE POLICY loan_book_by_country ON marts.loan_book
    FOR SELECT TO marts_reader
    USING (country_code IN (
        SELECT country_code FROM security.analyst_scope
        WHERE username = current_user));
```

لاحظ تفصيلين (note two details). يحتاج القرّاء (readers) إلى `USAGE` على المخطط `security` وإلى `SELECT` على `security.analyst_scope` كي يعمل البحث في السياسة (the policy's lookup) ‏(أو غلّف البحث في دالة صغيرة يملكها دور أمني (a small function owned by a security role)). والمستخدمون الخارقون (superusers) والأدوار التي لها السمة `BYPASSRLS` يتخطّون كل سياسة (skip every policy)، وهذا بالضبط سبب أن `etl_admin` جعل أمن مستوى الصف في نجم بلا معنى. وتقدّم مستودعات البيانات المُدارة (managed warehouses) الأفكار نفسها بأسمائها الخاصة (سياسات الوصول إلى الصفوف (row access policies)، ومرشّحات الصفوف (row filters)، وأقنعة الأعمدة (column masks)، ووسوم السياسات (policy tags))؛ والتصميم واحد (the design is the same).

**مسار الوصول (The access path).** يجب أن يحمل كل طريق إلى البيانات (every route to the data) هوية الشخص إلى مستودع البيانات (carry the person's identity to the warehouse) وأن يترك سجلًّا (leave a record):

```mermaid
flowchart RL
    U["المحلّل<br/>(Analyst)"] --> S["مزوّد هوية الدخول الموحّد<br/>(SSO identity provider)"]
    S --> G["المجموعة: محلّلو التجزئة في قطر<br/>(Group: retail-analysts-qa)"]
    G --> R["دور المستودع: قارئ المتاجر<br/>(Warehouse role: marts_reader)"]
    R --> P["السياسات: الصلاحيات وأمن الصفوف والإخفاء<br/>(Policies: grants, RLS, masking)"]
    P --> D["البيانات<br/>(Data)"]
    P --> A["سجل التدقيق<br/>(Audit log)"]
    A --> M["المراقبة والتنبيهات<br/>(Monitoring and alerts)"]
```

### 🟡 التعمق أكثر (Going deeper)

**الصلاحيات بوصفها شيفرة (Grants as code).** الصلاحيات التي تُمنح بالنقر في وحدة التحكم (grants clicked into a console) تنجرف (drift) ولا يمكن مراجعتها. أبقِها في نظام التحكم في الإصدارات (version control) وطبّقها في كل نشر (every deployment). تستطيع dbt فعل ذلك للكائنات التي تبنيها (the objects it builds) عبر إعداد `grants` ‏(grants config):

```yaml
models:
  - name: customer_360_analyst
    config:
      grants:
        select: ['marts_reader']
  - name: customer_360
    config:
      grants:
        select: ['svc_smart_alerts_features']   # one named workload, no humans
```

الأدوار (roles)، وتعيينات المجموعات (group mappings)، والإعدادات على مستوى قاعدة البيانات (database-level settings) مكانها البنية التحتية بوصفها شيفرة (infrastructure as code) ‏(راجع [*السحابة وDevOps: من الصفر إلى الاحتراف (Cloud & DevOps: Zero to Hero)*، الدرس 3.1 — البنية التحتية بوصفها شيفرة مع Terraform/OpenTofu: الحالة والوحدات والخطط (Infrastructure as code with Terraform/OpenTofu: state, modules and plans)](../cloud/index.ar.html#/3.1)). وعندئذ يصبح طلب السحب (pull request) هو طلب الوصول والمراجعة والسجلّ معًا (the access request, the review and the record).

**الأسرار (Secrets).** **السرّ (secret)** هو أي شيء يمنح الوصول (anything that grants access): كلمات المرور (passwords)، ومفاتيح واجهات برمجة التطبيقات (API keys)، والرموز المميّزة (tokens)، والمفاتيح الخاصة (private keys)، ومفتاح HMAC من الدرس 6.2 ‏(the HMAC key from 6.2).

```python
import os, psycopg

# WRONG: a password in code ends up in git history, notebooks and screenshots
conn = psycopg.connect("postgresql://etl_admin:Najm2019!@dwh.internal/dwh")

# BETTER: injected at run time by the orchestrator from the secrets manager
conn = psycopg.connect(os.environ["DWH_DSN"])
```

قواعد تسري عبر الأدوات (rules that hold across tools):
- خزّن الأسرار في **مدير أسرار (secrets manager)** ‏(HashiCorp Vault، أو الخدمة المقابلة لدى مزوّدك السحابي (your cloud provider's service)). يستطيع Airflow وDagster قراءة الاتصالات والمتغيّرات (connections and variables) من مثل هذه الواجهات الخلفية (back ends) بدلًا من قاعدة بيانات البيانات الوصفية الخاصة بهما (their own metadata database).
- فضّل **بيانات الاعتماد قصيرة العمر (short-lived credentials)**. فمحرّك أسرار قواعد البيانات (database secrets engine) في Vault، مثلًا، ينشئ مستخدم قاعدة بيانات لكل مهمة (a database user per job) مع تاريخ انتهاء صلاحية (expiry)، بحيث يتوقف بيان الاعتماد المسرَّب (leaked credential) عن العمل قريبًا. وتقدّم المنصات السحابية هوية أعباء العمل (workload identity) بحيث لا تحتاج المهام إلى أي كلمة مرور مخزّنة (no stored password at all).
- **افحص (scan)** المستودعات ودفاتر الملاحظات (repositories and notebooks) بحثًا عن الأسرار قبل دفعها (before they are pushed) ‏(وgitleaks ماسح مفتوح المصدر شائع (common open-source scanner))، و**دوّر (rotate)** أي سرّ أُودع يومًا (ever been committed)؛ فحذف السطر لا يزيله من التاريخ (does not remove it from history).

وللتعمق (for depth)، راجع [*أمن الذكاء الاصطناعي وأمن التطبيقات: من الصفر إلى الاحتراف (Secure AI & Application Security: Zero to Hero)*، الدرس 5.2 — إدارة الأسرار: المفاتيح والرموز المميّزة وأين تتسرّب (Secrets management: keys, tokens and where they leak)](../secai/index.ar.html#/5.2).

**سجلات التدقيق (Audit logs).** يجيب سجلّ التدقيق (audit log) عن "من فعل ماذا، وبأي بيانات، ومتى، ومن أين" ("who did what, to which data, when and from where"). ولمنصة البيانات يعني ذلك: عمليات تسجيل الدخول (logins)، والصلاحيات وتغييرات الأدوار (grants and role changes)، وتغييرات المخطط (schema changes)، وعمليات الكتابة (writes)، وقراءات البيانات المقيّدة (reads of restricted data). وفي PostgreSQL تضيف الإضافة **pgaudit** تسجيل تدقيق مفصّلًا (detailed audit logging):

```ini
# postgresql.conf
shared_preload_libraries = 'pgaudit'
pgaudit.log = 'ddl, role, write'     # session audit: schema changes, grants, writes
pgaudit.role = 'auditor'             # object audit: log access to objects 'auditor' holds rights on
```

```sql
-- Log every read of the restricted customer table
CREATE ROLE auditor NOLOGIN;
GRANT SELECT ON core.customers TO auditor;
```

تحتفظ مستودعات البيانات المُدارة (managed warehouses) بتاريخ الاستعلامات والوصول (query and access history) في عروض النظام (system views). وفي كلتا الحالتين، انقل السجلات إلى مخزن لا يستطيع مسؤولو المنصة تعديله (a store that platform administrators cannot alter) ‏(حساب منفصل (separate account) أو تخزين يُكتب مرة واحدة (write-once storage))، واحتفظ بها للمدة التي تحدّدها سياستك (the period your policy sets)، ونبّه على الأنماط (alert on patterns): القراءات الجماعية للجداول المقيّدة (bulk reads of restricted tables)، والوصول خارج ساعات العمل (access outside working hours)، واستخدام حساب خدمة من حاسوب محمول (a service account used from a laptop)، والصلاحيات الممنوحة خارج عملية طلبات السحب (grants made outside the pull-request process). وتُغطّى هندسة الاكتشاف (detection engineering) في [*أمن الذكاء الاصطناعي وأمن التطبيقات: من الصفر إلى الاحتراف (Secure AI & Application Security: Zero to Hero)*، الدرس 10.1 — التسجيل والمراقبة وهندسة الاكتشاف (Logging, monitoring and detection engineering)](../secai/index.ar.html#/10.1).

**التشفير (Encryption)** يحمي البيانات أثناء النقل (in transit) ‏(TLS على كل اتصال بمستودع البيانات (TLS on every connection to the warehouse)) وأثناء التخزين (at rest) ‏(تشفير التخزين بمفاتيح في خدمة إدارة المفاتيح (storage encryption with keys in a key management service)). وهو ضروري لكنه غير كافٍ (necessary but not sufficient): فأي شخص لديه تسجيل دخول صالح (valid login) يرى البيانات مفكوكة التشفير (decrypted data)، ولهذا فالتحكم في الوصول والتدقيق (access control and audit) أهم في العمل اليومي (day to day).

### 🔴 نظرة الخبير (Expert view)

**يجب أن يحمل كل مسار للمستهلك الهوية (Every consumer path must carry identity).** فشلت ضوابط نجم عند الأطراف (at the edges)، لا في مستودع البيانات:
- **أدوات ذكاء الأعمال (BI tools).** لوحة المعلومات التي تتصل بحساب خدمة واحد (one service account) تُري كل مشاهد ما يراه ذلك الحساب، فلا يستطيع أمن مستوى الصف في المستودع (warehouse RLS) أن يساعد. فإما أن تمرّر هوية المشاهد إلى مستودع البيانات (pass the viewer's identity to the warehouse) حيث تدعم الأداة ذلك، أو تطبّق صلاحيات صفوف مكافئة داخل الأداة (equivalent row permissions inside the tool)، أو تبني متاجر منفصلة لكل جمهور (separate marts per audience). وعطّل الروابط العامة (disable public links) لكل ما هو أعلى من "داخلي" ("internal").
- **دفاتر الملاحظات والتصديرات (Notebooks and exports).** البيانات التي تغادر مستودع البيانات تغادر ضوابطه (leaves its controls). قيّد صلاحيات التصدير (limit export rights) للبيانات المقيّدة، وسجّل التصديرات (log exports)، وفضّل مشاركة عرض محكوم (governed view) على مشاركة ملف (sharing a file).
- **تطبيقات النماذج اللغوية الكبيرة (LLM applications).** يجب أن يسترجع مساعد مذكرات الائتمان (Credit Memo Copilot) ‏(5.3) فقط المستندات التي يحق للمستخدم السائل قراءتها (the asking user may read)؛ فالفهرس المبني بنظرة مستخدم خارق إلى كل المذكرات (a superuser's view of all memos) يسرّبها عبر الإجابات (leaks them through answers). ويُغطّى الاسترجاع المدرك للصلاحيات (permission-aware retrieval) في [*أمن الذكاء الاصطناعي وأمن التطبيقات: من الصفر إلى الاحتراف (Secure AI & Application Security: Zero to Hero)*، الدرس 9.3 — تأمين الاسترجاع (RAG): حدود البيانات والتحكم في الوصول (Securing retrieval (RAG): data boundaries and access control)](../secai/index.ar.html#/9.3).

**المشاركة خارج البنك (Sharing outside the bank).** شارك الحد الأدنى (share the minimum)، وبأكثر الصيغ خضوعًا للرقابة (in the most controlled form): المجاميع قبل الصفوف (aggregates before rows)، والعروض المحكومة قبل النسخ (governed views before copies)، والأسماء المستعارة قبل البيانات المعرَّفة (pseudonymised before identified) ‏(6.2). وتتيح البروتوكولات المفتوحة (open protocols) مثل **Delta Sharing** والمشاركة الأصلية في مستودعات البيانات (warehouse-native sharing) للشريك أن يستعلم عرضًا حيًا للقراءة فقط (live, read-only view) تتحكم فيه ويمكنك إلغاؤه (revoke)، بدلًا من تلقّي ملف لا يمكنك استرداده أبدًا (a file you can never recall). وتتيح **غرف البيانات النظيفة (data clean rooms)** لطرفين حساب مجاميع مشتركة (joint aggregates) دون أن يرى أيّهما صفوف الآخر. وأي مشاركة خارجية للبيانات الشخصية تحتاج أيضًا إلى أساس قانوني (legal basis) واتفاقية مشاركة بيانات (data sharing agreement) تعتمدها سارة.

**وصول تنتهي صلاحيته (Access that expires).** الوصول الدائم يتراكم (permanent access accumulates). وتضيف المنصات الناضجة (mature platforms):
- **مراجعات الوصول (Access reviews):** كل ربع سنة، يعيد مالكو البيانات (data owners) المصادقة على من يحمل أدوارًا على بياناتهم (recertify who holds roles)؛ ويُزال الوصول غير المؤكَّد (unconfirmed access).
- **الوصول في الوقت المناسب (Just-in-time access):** يُمنح `pii_reader` لمهمة موثّقة بتذكرة (ticketed task) وتنتهي صلاحيته تلقائيًا بعد ساعات أو أيام.
- **حسابات كسر الزجاج (Break-glass accounts):** حساب عالي الصلاحيات للطوارئ (highly privileged account for emergencies)، مختوم (sealed)، يُطلق تنبيهًا عند كل استخدام (alerting on every use) ويُراجَع بعد ذلك.

**سياسات يقودها التصنيف (Policies driven by classification).** عندما تكون وسوم التصنيف (classification tags) من الدرس 6.2 في الفهرس، يمكن للسياسات أن تتبعها تلقائيًا: أي عمود موسوم بـ `pii:direct` يُخفى ما لم يحمل المستدعي `pii_reader`، أيًا كان الجدول الذي يوجد فيه. هذا هو التحكم في الوصول القائم على السمات (ABAC) عمليًا، وهو يتوسّع أفضل من الصلاحيات لكل جدول (scales better than per-table grants). وتطبّق محركات السياسات العامة (general policy engines) مثل **Open Policy Agent** الفكرة نفسها عبر الخدمات (across services). وأقل الصلاحيات ومبادئ انعدام الثقة (least privilege and zero-trust principles) بالتفصيل موجودة في [*أمن الذكاء الاصطناعي وأمن التطبيقات: من الصفر إلى الاحتراف (Secure AI & Application Security: Zero to Hero)*، الدرس 1.2 — مبادئ الأمن: أقل الصلاحيات، والدفاع في العمق، والإعدادات الافتراضية الآمنة، وانعدام الثقة (Security principles: least privilege, defence in depth, secure defaults, zero trust)](../secai/index.ar.html#/1.2).

## 🧰 الأدوات (The toolkit)
| الأداة أو النمط أو المعيار (Tool, pattern or standard) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |
|---|---|---|
| **Role-based access control (RBAC)** — التحكم في الوصول القائم على الأدوار | صلاحيات تُمنح للأدوار (permissions granted to roles)؛ ويُمنح الأشخاص وأعباء العمل الأدوار (people and workloads granted roles) | خط الأساس (the baseline) لكل مستودع بيانات وبحيرة بيانات (every warehouse and lake) |
| **Attribute-based access control (ABAC)** — التحكم في الوصول القائم على السمات | قرارات قائمة على سمات المستخدم والبيانات والسياق (attributes of user, data and context)، مثل وسوم التصنيف (classification tags) | كثرة المستخدمين ومجموعات البيانات حيث ستنفجر أعداد الأدوار لكل جدول (per-table roles would explode) |
| **Row-level security** (PostgreSQL) — أمن مستوى الصف | سياسات تصفّي الصفوف التي يستطيع كل دور رؤيتها (filter the rows each role can see) | بيانات محدودة النطاق حسب البلد أو الفرع أو المحفظة أو العميل (scoped by country, branch, portfolio or customer) |
| **dbt grants** — صلاحيات dbt | يعلن الصلاحيات على الكائنات التي تبنيها dbt (dbt-built objects) في نظام التحكم في الإصدارات ويطبّقها عند البناء (applies them at build) | كل نموذج يقرؤه أشخاص أو أعباء عمل (every model that people or workloads read) |
| **HashiCorp Vault** | مدير أسرار (secrets manager) ببيانات اعتماد ديناميكية قصيرة العمر لقواعد البيانات (short-lived, dynamic database credentials) | خطوط البيانات والخدمات التي تحتاج إلى الوصول إلى مستودع البيانات (warehouse access) |
| **pgaudit** | إضافة PostgreSQL ‏(PostgreSQL extension) لتسجيل تدقيق مفصّل على مستوى الجلسة والكائن (detailed session and object audit logging) | لإثبات من قرأ البيانات المقيّدة ومن غيّر الصلاحيات (who read restricted data and who changed grants) |
| **Delta Sharing** | بروتوكول مفتوح (open protocol) لمشاركة جداول حيّة للقراءة فقط (live, read-only tables) مع متلقّين خارجيين (external recipients) | مشاركة البيانات مع الشركاء دون إرسال نسخ (without sending copies) |

## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)
ينشر فيصل وسالم **سياسة الوصول إلى منصة بيانات نجم، الإصدار 1 (Najm Data Platform Access Policy v1)**. الجزء أ هو مصفوفة الأدوار (role matrix)؛ والجزء ب هو القواعد (rules).

**الجزء أ: من يحق له قراءة أيّ طبقة (Part A: who may read which layer)**

| الدور (Role) | الخام (Raw) | التهيئة (Staging) | المتاجر (العروض المنسّقة) (Marts (curated views)) | المتاجر (الجداول الأساسية ذات الأعمدة المقيّدة) (Marts (base tables with restricted columns)) | يمنحه (Granted by) |
|---|---|---|---|---|---|
| مهندسو البيانات (مسمَّون) (Data engineers (named)) | التطوير والاختبار فقط (Dev and test only) | التطوير والاختبار فقط (Dev and test only) | قراءة (Read) | في الوقت المناسب، بتذكرة (Just-in-time, ticketed) | فيصل |
| حسابات خدمة خطوط البيانات (Pipeline service accounts) | مصادرها الخاصة فقط (Own sources only) | نماذجها الخاصة فقط (Own models only) | كتابة نماذجها الخاصة (Write own models) | نماذجها الخاصة فقط (Own models only) | طلب سحب (Pull request) |
| محلّلو `marts_reader` ‏(analysts) | — | — | قراءة، مع أمن مستوى الصف حسب البلد (Read, RLS by country) | — | مالك البيانات (Data owner) |
| `pii_reader` | — | — | قراءة دون إخفاء (Read unmasked) | قراءة، لمدة محدودة (Read, time-limited) | مالك البيانات وسارة (Data owner and Sara) |
| حسابات خدمة ذكاء الأعمال (BI service accounts) | — | — | حساب لكل جمهور، مع تطبيق أمن مستوى الصف (One per audience, RLS applied) | — | لينا |
| كسر الزجاج (Break-glass) | الكل (All) | الكل (All) | الكل (All) | الكل (All) | مختوم؛ سالم وفيصل معًا (Sealed; Salem and Faisal together) |

**الجزء ب: القواعد (Part B: rules)**
1. لا حسابات بشرية مشتركة (no shared human accounts). أُحيل `etl_admin` إلى التقاعد؛ ويقتصر استخدام المستخدم الخارق (superuser use) على كسر الزجاج (break-glass) ويخضع للتدقيق (audited).
2. كل صلاحية شيفرة (every grant is code) ‏(`grants` في dbt أو البنية التحتية بوصفها شيفرة (infrastructure as code))، تُراجَع في طلب سحب (pull request)؛ وتُلغى الصلاحيات الممنوحة من وحدة التحكم (console grants) في النشر التالي (next deployment).
3. لا تعيش الأسرار إلا في مدير الأسرار (secrets manager)؛ وتستخدم خطوط البيانات بيانات اعتماد قصيرة العمر (short-lived credentials). ويعمل فحص الأسرار (secret scanning) على كل مستودع ودفتر ملاحظات؛ ويُدوَّر أي سرّ مُودَع (committed secret) خلال 24 ساعة.
4. يسجّل pgaudit ‏(أو تاريخ الوصول في مستودع البيانات (warehouse's access history)) الصلاحيات، وتغييرات المخطط (schema changes)، وعمليات الكتابة (writes)، وكل قراءات الجداول المقيّدة (all reads of restricted tables)، وتُنقل إلى مخزن سجلات فريق الأمن (security team's log store). التنبيهات (alerts): القراءات المقيّدة الجماعية (bulk restricted reads)، والوصول المقيّد خارج ساعات العمل (off-hours restricted access)، وحسابات الخدمة المستخدمة تفاعليًا (service accounts used interactively).
5. الروابط العامة (public links) معطّلة في أداة ذكاء الأعمال (BI tool). وتستخدم المشاركة الخارجية (external sharing) العروض المحكومة أو بروتوكولات المشاركة (governed views or sharing protocols)، لا الملفات أبدًا، وتحتاج إلى اتفاقية مشاركة بيانات (data sharing agreement) تعتمدها سارة.
6. يعيد مالكو البيانات (data owners) المصادقة على الوصول (recertify access) إلى مجموعات بيانات الفئة الأولى (tier-1 datasets) الخاصة بهم كل ربع سنة.

مع وجود هذه الضوابط، يستغرق سؤال التدقيق دقائق: اسرد كل مستخدم مسمّى (every named user) قرأت استعلاماته المسجّلة (logged queries) ‏`core.customers` أو `customer_360` الشهر الماضي، ثم ضيّق النطاق إلى العبارات التي مسّت ذلك العميل (statements that touched that customer). يسجّل pgaudit العبارات لا الصفوف المُرجَعة (statements, not returned rows)، لذا فالاستعلام الواسع (broad query) خيط يجب تتبّعه (a lead to follow up)، لا دليل (not proof).

## 🛠️ التمارين (Exercises)
استخدم بيانات اصطناعية (synthetic data) في PostgreSQL محلي (local PostgreSQL) ‏(مثل الصورة الرسمية (official image) في Docker). لا تختبر أبدًا على أنظمة لا تملكها (systems you do not own).

- 🟢 أنشئ أدوار المجموعات (group roles)، ومستخدمَين مسمَّيين (two named users)، ومخططين (two schemas) من هذا الدرس. امنح أحد المستخدمين `marts_reader` وتحقّق باستعلامات حقيقية (real queries) من أنه يستطيع قراءة العرض المنسّق (curated view) لا الجدول الأساسي (base table) ولا المخطط الخام (raw schema). *يكتمل عندما (Done when):* يكون لديك نص برمجي ينشئ كل شيء من الصفر (from scratch) ونص اختبار (test script) تظهر فيه كل أخطاء "رُفض الإذن" ("permission denied") المتوقعة.
- 🟡 أضف أمن مستوى الصف حسب البلد (row-level security by country) إلى جدول قروض اصطناعي (synthetic loan table)، مع جدول نطاق (scope table) يربط المستخدمين بالبلدان. ثم بيّن التجاوز (show the bypass): شغّل الاستعلام نفسه بوصفك مستخدمًا خارقًا (superuser) وبوصفك مالك الجدول (table owner) دون `FORCE ROW LEVEL SECURITY`. *يكتمل عندما (Done when):* يرى كل مستخدم صفوف بلده فقط، وتستطيع أن تشرح في جملتين لماذا يحدث كلا التجاوزين وكيف يصلحهما `FORCE` وإزالة صفة المستخدم الخارق (removing superuser).
- 🔴 شغّل PostgreSQL مع pgaudit ‏(صورة تتضمنه، أو ابنِ واحدة)، واضبط التدقيق على مستوى الجلسة والكائن (session and object auditing)، وشغّل خط بيانات صغيرًا (small pipeline) تأتي بيانات اعتماده (credentials) من خادم تطوير Vault محلي (local Vault dev server) أو من متغيّرات البيئة (environment variables)، لا من الشيفرة أبدًا. افحص مستودعك بـ gitleaks. *يكتمل عندما (Done when):* يُظهر سجل التدقيق (audit log) قراءة مستخدم مسمّى للجدول المقيّد (restricted table)، ويبلغ gitleaks عن صفر نتائج (zero findings)، ويسري تغيير السرّ المخزَّن (stored secret) دون تغيير في الشيفرة (without a code change).

## ⚠️ أخطاء وفخاخ (Mistakes and traps)
- **حسابات المستخدم الخارق المشتركة (Shared superuser accounts).** تتجاوز أمن مستوى الصف (bypass RLS)، وتُفشل التدقيق (defeat audit)، ولا يمكن سحبها من شخص واحد (cannot be revoked from one person). أعطِ كل إنسان وعبء عمل هويته الخاصة ودورًا بأدنى صلاحيات (minimal role).
- **ضوابط في مستودع البيانات فقط (Controls only in the warehouse).** أدوات ذكاء الأعمال ذات حسابات الخدمة (BI tools with service accounts)، والتصديرات (exports)، وفهارس النماذج اللغوية الكبيرة (LLM indexes) تتجاوز سياسات المستودع. مرّر هوية المشاهد (carry the viewer's identity through) أو افرض ضوابط مكافئة (equivalent controls) على كل مسار.
- **عروض تتخطى أمن مستوى الصف بصمت (Views that silently skip RLS).** يعمل العرض (view) في PostgreSQL بصلاحيات مالكه افتراضيًا (with its owner's rights by default)، لذا يُتحقَّق من أمن مستوى الصف على الجدول الأساسي (base-table RLS) مقابل المالك لا المستدعي (the owner, not the caller). استخدم `security_invoker = true` ‏(PostgreSQL 15 وما بعده) عندما يجب أن تنطبق سياسات المستدعي (the caller's policies)، أو صفِّ داخل العرض (filter inside the view).
- **حذف سرّ مُودَع بدلًا من تدويره (Deleting a committed secret instead of rotating it).** يحتفظ به تاريخ git ‏(git history) والتفرّعات (forks) والنسخ المستنسخة (clones). دوّر أولًا (rotate first)، ثم نظّف (clean up).
- **سجلات يستطيع المسؤولون تعديلها (Logs the administrators can edit).** مسار التدقيق (audit trail) الذي يستطيع أصحابه تغييره لا يُثبت شيئًا. انقل السجلات إلى مخزن منفصل يقبل الإلحاق فقط (separate, append-only store).
- **وصول لا تنتهي صلاحيته أبدًا (Access that never expires).** تتراكم الأدوار (roles pile up) مع تغيّر وظائف الناس. استخدم إعادة المصادقة الفصلية (quarterly recertification) والصلاحيات محدودة المدة (time-limited grants) للأدوار الحساسة (sensitive roles).

## 🧾 الخلاصة (Recap)
- أقل الصلاحيات (least privilege)، والهويات المسمّاة (named identities)، والفصل بين المهام (separation of duties)، والدفاع في العمق (defence in depth) هي مبادئ التصميم (design principles).
- اجمع بين التحكم في الوصول القائم على الأدوار (RBAC) والسمات المستمدة من التصنيف (attributes from classification)، وأمن مستوى الصف (row-level security)، وإخفاء الأعمدة (column masking)؛ وأدِر الصلاحيات بوصفها شيفرة (manage grants as code).
- احفظ الأسرار في مدير أسرار (secrets manager)، وفضّل بيانات الاعتماد قصيرة العمر (short-lived credentials)، وافحص بحثًا عن التسريبات (scan for leaks)، ودوّر أي شيء مكشوف (rotate anything exposed).
- يجب أن تسجّل سجلات التدقيق (audit logs) قراءات البيانات المقيّدة، وأن تعيش بعيدًا عن متناول المسؤولين (outside administrators' reach)، وأن تقود التنبيهات (drive alerts).
- أمّن كل مسار للمستهلك (every consumer path) ‏(ذكاء الأعمال (BI)، والتصديرات (exports)، والمشاركة (sharing)، واسترجاع النماذج اللغوية الكبيرة (LLM retrieval)) بحيث يرى مستودع البيانات هوية المستخدم الحقيقي (the real user's identity).

## ✍️ اختبر نفسك (Check yourself)

**1. لدى متجر مخاطر الائتمان (credit-risk mart) في نجم سياسات لأمن مستوى الصف (row-level security policies)، لكن المحلّلين الذين يستخدمون لوحة معلومات المخاطر (risk dashboard) يرون قروض كل البلدان. ما السبب الأرجح (most likely cause)؟**

- A. أمن مستوى الصف لا يعمل على جداول المتاجر التي تبنيها dbt ‏(mart tables built by dbt)
- B. كُتبت السياسات بلغة SQL في مستودع البيانات بدلًا من أداة ذكاء الأعمال (BI tool)
- C. سياسات أمن مستوى الصف لا تنطبق إلا على عبارات INSERT وUPDATE ‏(INSERT and UPDATE statements)
- D. تتصل لوحة المعلومات بوصفها مستخدمًا خارقًا مشتركًا (shared superuser)، وهو ما يتجاوز السياسات (bypasses the policies)

<details><summary>الإجابة</summary>

**D.** المستخدمون الخارقون (superusers) والأدوار التي لها `BYPASSRLS` يتخطّون كل السياسات، وحساب الخدمة المشترك (shared service account) يُخفي هوية المشاهد على أي حال. A وB وC خاطئة: أمن مستوى الصف (RLS) يعمل على أي جدول، ومكانه مستودع البيانات، والسياسة هنا `FOR SELECT`. (🟢 الأساسيات (The essentials)؛ 🔴 نظرة الخبير (Expert view).)

</details>

**2. تجد هدى كلمة مرور لمستودع البيانات (warehouse password) في دفتر ملاحظات أُودع في git ‏(committed to git) قبل ستة أشهر. ما الذي يجب أن يحدث أولًا؟**

- A. حذف السطر من دفتر الملاحظات، وإيداع التغيير ودفعه (commit the change and push it)
- B. تدوير بيان الاعتماد (rotate the credential)، ثم نقل خط البيانات إلى مدير الأسرار (secrets manager)
- C. جعل المستودع خاصًا (make the repository private) كي لا يرى أحد آخر كلمة المرور
- D. لا شيء، لأن المستودع داخلي في البنك (internal to the bank)

<details><summary>الإجابة</summary>

**B.** يبقى السرّ المُودَع (committed secret) في التاريخ وفي كل نسخة مستنسخة (every clone)، لذا يجب معاملته بوصفه مكشوفًا (treated as exposed) وتدويره. A هي الإجابة المغرية (tempting answer) لكنها تترك كلمة المرور القديمة صالحة (leaves the old password valid). (🟡 التعمق أكثر (Going deeper).)

</details>

**3. تريد نجم أن يرى المحلّلون الأعمدة السرّية (confidential columns) فقط لعملاء بلدهم، مع إخفاء تقوده وسوم التصنيف (classification tags) من الدرس 6.2. أيّ نموذج وصول (access model) هو الأنسب؟**

- A. دور واحد لكل جدول لكل بلد (one role per table per country)، يمنحه كل مالك بيانات
- B. حساب محلّل مشترك واحد (single shared analyst account) مع عرض مُخفى (masked view) للجميع
- C. التحكم في الوصول القائم على السمات (ABAC) على سمات المستخدم ووسوم الأعمدة (user attributes and column tags)، مع أمن مستوى الصف (row-level security)
- D. منح كل المحلّلين `pii_reader` والاعتماد على التدريب (relying on training)

<details><summary>الإجابة</summary>

**C.** يعبّر التحكم في الوصول القائم على السمات (ABAC) عن "البلد نفسه، ومُخفى ما لم يكن مخوَّلًا" ("own country, masked unless authorised") بقواعد قليلة تقودها السمات والوسوم (attributes and tags). A تعمل لكن أعداد الأدوار تنفجر (explodes in number of roles)؛ وB وD تكسران مبدأ أقل الصلاحيات (break least privilege). (🔴 نظرة الخبير (Expert view).)

</details>

**4. أيّ إعداد لسجلات التدقيق (audit-log setup) يعطي أدلة يستطيع التدقيق الداخلي (internal audit) الاعتماد عليها؟**

- A. سجلات بأسماء المستخدمين (named-user logs) للصلاحيات وعمليات الكتابة والقراءات المقيّدة (grants, writes and restricted reads)، في مخزن لا يستطيع المسؤولون تعديله
- B. سجلات مفصّلة محفوظة على خادم مستودع البيانات (warehouse server)، يستطيع مسؤولو المنصة تعديلها
- C. سجلات محاولات تسجيل الدخول الفاشلة فقط (failed logins only)، محفوظة لسبع سنوات
- D. لقطات شاشة لإعدادات التحكم في الوصول (screenshots of the access-control settings)، تُلتقط مرة في السنة للمدققين

<details><summary>الإجابة</summary>

**A.** تحتاج الأدلة (evidence) إلى هويات مسمّاة (named identities)، وتغطية للإجراءات المهمة (coverage of the actions that matter)، ومخزن لا يستطيع أصحابه تعديله (a store its subjects cannot alter). B مغرية لأنها سهلة، لكن المسؤولين قد يغيّرونها. (🟡 التعمق أكثر (Going deeper).)

</details>

**5. يريد شريك في التقنية المالية (fintech partner) بيانات الإنفاق اليومي ببطاقات الشركات الصغيرة والمتوسطة حسب القطاع (daily SME card-spend data by sector) من نجم لبناء منتج مشترك (joint product). أيّ نهج هو الأكثر أمانًا (safest)؟**

- A. إرسال ملف CSV مشفّر يوميًا (daily encrypted CSV) بالبريد الإلكتروني إلى الشريك بكل معاملات بطاقات الشركات الصغيرة والمتوسطة
- B. إعطاء الشريك تسجيل دخول مسمّى (named login) إلى مستودع البيانات مع `marts_reader`
- C. نسخ تدفق البطاقات الخام (raw card stream) إلى الحساب السحابي للشريك (partner's cloud account) كل ليلة
- D. عرض مجمّع للقراءة فقط قابل للإلغاء (revocable, read-only aggregated view)، يُشارَك بموجب اتفاقية يعتمدها مسؤول حماية البيانات (DPO-approved agreement)

<details><summary>الإجابة</summary>

**D.** المجاميع قبل الصفوف (aggregates before rows)، والعروض الحيّة قبل النسخ (live views before copies)، ووصول قابل للإلغاء (revocable access)، واتفاقية قانونية (legal agreement). A وC ترسلان نسخًا لا تستطيع نجم استردادها أبدًا (can never recall)؛ وB تكشف أكثر بكثير مما يحتاجه الغرض. (🔴 نظرة الخبير (Expert view).)

</details>

## 📚 المراجع (References)
- توثيق PostgreSQL: سياسات أمن الصفوف (PostgreSQL documentation: row security policies) — https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- توثيق PostgreSQL: الصلاحيات (PostgreSQL documentation: privileges) — https://www.postgresql.org/docs/current/ddl-priv.html
- توثيق PostgreSQL: ‏CREATE VIEW ‏(security_invoker) ‏(PostgreSQL documentation: CREATE VIEW (security_invoker)) — https://www.postgresql.org/docs/current/sql-createview.html
- pgaudit — https://github.com/pgaudit/pgaudit
- توثيق dbt: الصلاحيات (dbt documentation: grants) — https://docs.getdbt.com/reference/resource-configs/grants
- توثيق HashiCorp Vault ‏(HashiCorp Vault documentation) — https://developer.hashicorp.com/vault/docs
- توثيق Apache Airflow: الواجهات الخلفية للأسرار (Apache Airflow documentation: secrets backends) — https://airflow.apache.org/docs/
- Delta Sharing — https://delta.io/sharing/
- gitleaks — https://github.com/gitleaks/gitleaks
- Open Policy Agent — https://www.openpolicyagent.org/
