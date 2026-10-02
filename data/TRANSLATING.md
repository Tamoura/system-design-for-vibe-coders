# Arabic edition — translation guide (Data Engineering & Analytics: Zero to Hero)

Not published. Every translator follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, like a well-written university or professional training manual. Faithful: same meaning, structure, emphasis, lists, tables. Never summarise, add or drop content.
- **English beside every technical term everywhere.** In every paragraph, list item, table cell, heading, quiz question, option and answer, each technical term and key phrase carries its English in parentheses on its first appearance in that unit (a unit = one paragraph, one list item, one table cell, one heading): `نافذة الدالة (window function)`, `مخطط النجمة (star schema)`, `الحُبَيبية (grain)`, `التقاط تغيّر البيانات (change data capture, CDC)`, `عقد البيانات (data contract)`. Aim for roughly one gloss every 4–6 Arabic words in technical text. Gloss whole phrases, never split a construct. A space always separates the Arabic word from `(`. Use the English exactly as the English lesson words it.
- Key phrases, rules of thumb, labels and framework step names also get their English, e.g. `يكتمل عندما (Done when)`.
- If a gloss ends in punctuation (`?`, `.`, `!`), wrap it in a left-to-right isolate (the characters U+2066 before `(` and U+2069 after `)`), so it displays correctly in right-to-left text.
- Names of tools, products, standards, companies, platforms, programming languages and commands stay in their English form (SQL, PostgreSQL, DuckDB, Python, pandas, Polars, dbt, Airflow, Dagster, Kafka, Redpanda, Parquet, Apache Iceberg, Delta Lake, Snowflake, BigQuery, Databricks, MLflow, Feast, pgvector, Metabase, Superset). On first use in a unit you may add a short Arabic rendering before it.
- People: Faisal فيصل, Huda هدى, Lina لينا, Dana دانة, Kareem كريم, Sara سارة, Layla ليلى, Tariq طارق, Salem سالم. Najm Bank → بنك نجم (Najm Bank). Smart Alerts → التنبيهات الذكية (Smart Alerts); Credit Memo Copilot → مساعد مذكرات الائتمان (Credit Memo Copilot); Najm Mobile → تطبيق نجم للهاتف (Najm Mobile); Najm Assist → نجم أسيست (Najm Assist).

## Fixed terms
| English | Arabic |
|---|---|
| data engineering | هندسة البيانات (data engineering) |
| analytics engineer / data analyst / data scientist | مهندس التحليلات (analytics engineer) / محلّل البيانات (data analyst) / عالم البيانات (data scientist) |
| pipeline | خط البيانات (pipeline) |
| warehouse / lake / lakehouse | مستودع البيانات (warehouse) / بحيرة البيانات (lake) / المستودع البحيري (lakehouse) |
| data model / grain | نموذج البيانات (data model) / الحُبَيبية (grain) |
| fact / dimension | جدول الحقائق (fact) / جدول الأبعاد (dimension) |
| slowly changing dimension | البُعد المتغيّر ببطء (slowly changing dimension, SCD) |
| ingestion / batch / streaming | الاستيعاب (ingestion) / الدفعي (batch) / المتدفق (streaming) |
| orchestration / DAG | التنسيق (orchestration) / الرسم البياني الموجّه غير الدوري (DAG) |
| idempotent / backfill | متساوي الأثر (idempotent) / إعادة التعبئة (backfill) |
| transformation | التحويل (transformation) |
| data quality / data contract | جودة البيانات (data quality) / عقد البيانات (data contract) |
| metric / semantic layer | المقياس (metric) / الطبقة الدلالية (semantic layer) |
| dashboard | لوحة المعلومات (dashboard) |
| A/B test | اختبار A/B (A/B test) |
| feature / feature store | الخاصية (feature) / مخزن الخصائص (feature store) |
| drift | الانجراف (drift) |
| embedding / vector search / chunking | التضمين (embedding) / البحث المتّجهي (vector search) / التقطيع (chunking) |
| lineage / catalogue | النسب (lineage) / الفهرس (catalogue) |
| personal data / masking | البيانات الشخصية (personal data) / الإخفاء (masking) |

## Structure the build depends on (do not break)
- Module heading: `# الوحدة N — العنوان` (N unchanged). Lesson heading: `# N.M — العنوان` (numbers unchanged).
- The line right after each lesson heading, translated exactly like this pattern:
  `*المستوى (Level): 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 1.1، 1.2* · *المرحلة (Stage): Model, Analyse*`
  (🟢 مبتدئ (Beginner) / 🟡 متوسط (Intermediate) / 🔴 متقدم (Advanced); keep the same emoji; keep lesson numbers; **stage names stay in English** exactly as in the English line; separate lesson lists with «، »). If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated: `## ⚡ الدرس في دقيقة (In 60 seconds)`, `## 🧭 لماذا يهم (Why it matters)`, `## 📐 كيف يعمل (How it works)`, `### 🟢 الأساسيات (The essentials)`, `### 🟡 التعمق أكثر (Going deeper)`, `### 🔴 نظرة الخبير (Expert view)`, `## 🧰 الأدوات (The toolkit)`, `## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)`, `## 🛠️ التمارين (Exercises)`, `## ⚠️ أخطاء وفخاخ (Mistakes and traps)`, `## 🧾 الخلاصة (Recap)`, `## ✍️ اختبر نفسك (Check yourself)`, `## 📚 المراجع (References)` (7.3: `## ✍️ الامتحان التدريبي (Practice exam)`). Same number of `#`/`##`/`###` headings in the same order as the English.
- **🧰 tables:** the first cell of every row must START with the same bold English name as the English row, exactly (e.g. `**dbt** — …`, `**Star schema** — …`). Translate everything after the bold name and the other cells. Header row: `| الأداة أو النمط أو المعيار (Tool, pattern or standard) | ما هو وماذا يفعل (What it is and does) | متى تلجأ إليه (When to reach for it) |`.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 7.3 keep the stage/lesson tag in English, e.g. `*(Model · 1.2)*`.
- **Code blocks stay byte-identical** (code, SQL, YAML, shell, config). Comments inside code stay in English.
- **Mermaid diagrams:** keep the syntax, the direction line and node IDs exactly; translate only the label text into Arabic (no English in the labels, no parentheses inside labels). The build adds the English and flips the direction for Arabic afterwards.
- **Links:** keep external URLs unchanged. Relative links to other courses in the library point to their Arabic pages: `index.html` → `index.ar.html`, `index.en.html` → `index.ar.html`, `learning-path.html` → `learning-path.ar.html`, `assessment.html` → `assessment.ar.html` (keep the `#…` part). Translate the link text.
- Keep unchanged: inline `code`, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما (Done when):*`.

## Verify
Run: `python3 data/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/stage lines, section emoji order, 🧰 bold names, quiz letters, details blocks, code and mermaid blocks, links and that the text is really Arabic.
