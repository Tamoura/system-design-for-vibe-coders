# Arabic edition — translation guide (Software Testing: Zero to Hero in the AI Era)

Not published. Every translator follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, like a well-written university or professional training manual. Faithful: same meaning, structure, emphasis, lists, tables. Never summarise, add or drop content.
- **English beside every technical term everywhere.** In every paragraph, list item, table cell, heading, quiz question, option and answer, each technical term and key phrase carries its English in parentheses on its first appearance in that unit (a unit = one paragraph, one list item, one table cell, one heading): `اختبار الوحدة (unit testing)`, `تحليل القيم الحدّية (boundary value analysis)`, `اختبار الطفرات (mutation testing)`, `الاختبار القائم على الخصائص (property-based testing)`, `اختبار الأداء (performance testing)`. Aim for roughly one gloss every 4–6 Arabic words in technical text. Gloss whole phrases, never split a construct. A space always separates the Arabic word from `(`. Use the English exactly as the English lesson words it.
- Key phrases, rules of thumb, labels and framework step names also get their English, e.g. `يكتمل عندما (Done when)`.
- If a gloss ends in punctuation (`?`, `.`, `!`), wrap it in a left-to-right isolate (the characters U+2066 before `(` and U+2069 after `)`), so it displays correctly in right-to-left text.
- Names of tools, products, standards, companies, platforms, programming languages and commands stay in their English form (pytest, Hypothesis, Playwright, Selenium, Cypress, Appium, Vitest, Jest, JUnit, k6, JMeter, Pact, Testcontainers, OWASP ZAP, Semgrep, promptfoo, Ragas, garak, PyRIT, GitHub Actions, Docker, Python, TypeScript, JavaScript). On first use in a unit you may add a short Arabic rendering before it.
- People: Rashid راشد, Nada ندى, Bilal بلال, Amal أمل, Tariq طارق, Maha مها, Noura نورة, Mariam مريم, Dana دانة, Rania رانيا, Hessa حصة, Layla ليلى, Sara سارة, Hamad حمد. Najm Bank → بنك نجم (Najm Bank). Najm Mobile → تطبيق نجم للهاتف (Najm Mobile); Najm Mobile API → واجهة برمجة تطبيق نجم للهاتف (Najm Mobile API); Najm Assist → نجم أسيست (Najm Assist); Quality Engineering team → فريق هندسة الجودة (Quality Engineering).

## Fixed terms
| English | Arabic |
|---|---|
| software testing / quality assurance (QA) | اختبار البرمجيات (software testing) / ضمان الجودة (quality assurance, QA) |
| quality engineering | هندسة الجودة (quality engineering) |
| error / defect (bug) / failure | الخطأ البشري (error) / العيب (defect, bug) / الفشل (failure) |
| verification / validation | التحقق (verification) / المصادقة على الملاءمة (validation) |
| test case / test suite / test plan / test strategy | حالة اختبار (test case) / مجموعة الاختبارات (test suite) / خطة الاختبار (test plan) / استراتيجية الاختبار (test strategy) |
| test oracle | مرجع النتيجة المتوقعة (test oracle) |
| regression testing | اختبار الانحدار (regression testing) |
| equivalence partitioning / boundary value analysis | تقسيم فئات التكافؤ (equivalence partitioning) / تحليل القيم الحدّية (boundary value analysis) |
| decision table / state transition / pairwise | جدول القرارات (decision table) / انتقال الحالات (state transition) / الاختبار الزوجي (pairwise testing) |
| unit test / integration test / end-to-end test | اختبار وحدة (unit test) / اختبار تكامل (integration test) / اختبار شامل من البداية إلى النهاية (end-to-end test) |
| test pyramid | هرم الاختبار (test pyramid) |
| test double / mock / stub / fake / spy | بديل اختباري (test double) / كائن محاكاة (mock) / بديل ثابت الاستجابة (stub) / بديل مزيّف (fake) / مراقب (spy) |
| test-driven development (TDD) | التطوير الموجَّه بالاختبار (test-driven development, TDD) |
| code coverage / mutation testing / property-based testing | تغطية الشيفرة (code coverage) / اختبار الطفرات (mutation testing) / الاختبار القائم على الخصائص (property-based testing) |
| flaky test | اختبار غير مستقر (flaky test) |
| contract test | اختبار العقد (contract test) |
| fixture / test data | تجهيزات الاختبار (fixture) / بيانات الاختبار (test data) |
| exploratory testing / charter | الاختبار الاستكشافي (exploratory testing) / ميثاق الجلسة (charter) |
| acceptance criteria / user acceptance testing (UAT) | معايير القبول (acceptance criteria) / اختبار قبول المستخدم (user acceptance testing, UAT) |
| behaviour-driven development (BDD) | التطوير الموجَّه بالسلوك (behaviour-driven development, BDD) |
| API testing | اختبار واجهات البرمجة (API testing) |
| load / stress / soak / spike test | اختبار الحِمل (load test) / اختبار الضغط (stress test) / اختبار التحمّل الطويل (soak test) / اختبار الذروة المفاجئة (spike test) |
| latency / throughput / percentile | زمن الاستجابة (latency) / الإنتاجية (throughput) / النسبة المئوية (percentile) |
| accessibility / localisation / internationalisation | إمكانية الوصول (accessibility) / التوطين (localisation) / التدويل (internationalisation) |
| right-to-left (RTL) | من اليمين إلى اليسار (right-to-left, RTL) |
| security testing / penetration test / fuzzing | اختبار الأمان (security testing) / اختبار الاختراق (penetration test) / الاختبار العشوائي الموجَّه (fuzzing) |
| SAST / DAST / SCA | الفحص الساكن للشيفرة (SAST) / الفحص الديناميكي للتطبيق (DAST) / تحليل مكوّنات الطرف الثالث (SCA) |
| chaos engineering | هندسة الفوضى (chaos engineering) |
| data quality | جودة البيانات (data quality) |
| risk-based testing | الاختبار القائم على المخاطر (risk-based testing) |
| shift-left / shift-right | الإزاحة نحو اليسار (shift-left) / الإزاحة نحو اليمين (shift-right) |
| CI/CD pipeline | خط التكامل والتسليم المستمرين (CI/CD pipeline) |
| feature flag / canary release | مفتاح الميزة (feature flag) / الإطلاق الكناري (canary release) |
| synthetic monitoring | المراقبة الاصطناعية (synthetic monitoring) |
| LLM / prompt / hallucination | النموذج اللغوي الكبير (LLM) / التوجيه (prompt) / الهلوسة (hallucination) |
| eval / golden set / grader | التقييم الآلي (eval) / المجموعة المرجعية (golden set) / المقيِّم (grader) |
| LLM-as-judge | النموذج اللغوي حَكَمًا (LLM-as-judge) |
| retrieval-augmented generation (RAG) | التوليد المعزَّز بالاسترجاع (retrieval-augmented generation, RAG) |
| groundedness / faithfulness | الاستناد إلى المصادر (groundedness) / الأمانة للمصدر (faithfulness) |
| agent / tool call / trajectory | الوكيل (agent) / استدعاء أداة (tool call) / مسار التنفيذ (trajectory) |
| non-determinism | عدم الحتمية (non-determinism) |
| red teaming / prompt injection | الفريق الأحمر (red teaming) / حقن التوجيه (prompt injection) |
| metamorphic testing | الاختبار التحويلي (metamorphic testing) |
| fairness / bias | العدالة (fairness) / التحيّز (bias) |
| drift | الانجراف (drift) |
| coding agent / AI-generated code | وكيل البرمجة (coding agent) / الشيفرة المولَّدة بالذكاء الاصطناعي (AI-generated code) |

## Structure the build depends on (do not break)
- Module heading: `# الوحدة N — العنوان` (N unchanged). Lesson heading: `# N.M — العنوان` (numbers unchanged).
- The line right after each lesson heading, translated exactly like this pattern:
  `*المستوى (Level): 🟡 متوسط (Intermediate)* · *المتطلبات (Prerequisites): 1.1، 1.2* · *التركيز (Focus): Unit, Integration*`
  (🟢 مبتدئ (Beginner) / 🟡 متوسط (Intermediate) / 🔴 متقدم (Advanced); keep the same emoji; keep lesson numbers; **focus names stay in English** exactly as in the English line; separate lesson lists with «، »). If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated: `## ⚡ الدرس في دقيقة (In 60 seconds)`, `## 🧭 لماذا يهم (Why it matters)`, `## 📐 كيف يعمل (How it works)`, `### 🟢 الأساسيات (The essentials)`, `### 🟡 التعمق أكثر (Going deeper)`, `### 🔴 نظرة الخبير (Expert view)`, `## 🧰 الأدوات (The toolkit)`, `## 🏛️ عمليًا في بنك نجم (In practice at Najm Bank)`, `## 🛠️ التمارين (Exercises)`, `## ⚠️ أخطاء وفخاخ (Mistakes and traps)`, `## 🧾 الخلاصة (Recap)`, `## ✍️ اختبر نفسك (Check yourself)`, `## 📚 المراجع (References)` (8.3: `## ✍️ الامتحان التدريبي (Practice exam)`). Same number of `#`/`##`/`###` headings in the same order as the English.
- **🧰 tables:** the first cell of every row must START with the same bold English name as the English row, exactly (e.g. `**pytest** — …`, `**Mutation testing** — …`). Translate everything after the bold name and the other cells. Header row: `| الأداة أو الممارسة أو التقنية (Tool, practice or technique) | ما هي وماذا تفعل (What it is and does) | متى تلجأ إليها (When to reach for it) |`.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 8.3 keep the focus/lesson tag in English, e.g. `*(Unit · 2.1)*`.
- **Code blocks stay byte-identical** (code, YAML, shell, config, Gherkin). Comments and string literals inside code stay in English.
- **Mermaid diagrams:** keep the syntax, the direction line and node IDs exactly; translate only the label text into Arabic (no English in the labels, no parentheses inside labels). The build adds the English and flips the direction for Arabic afterwards.
- **Links:** keep external URLs unchanged. Relative links to other courses in the library point to their Arabic pages: `index.html` → `index.ar.html`, `index.en.html` → `index.ar.html`, `learning-path.html` → `learning-path.ar.html`, `assessment.html` → `assessment.ar.html` (keep the `#…` part). Translate the link text.
- Keep unchanged: inline `code`, numbers, `---` separators, tables' column counts.
- `*Done when:*` → `*يكتمل عندما (Done when):*`.

## Verify
Run: `python3 testing/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/phase lines, section emoji order, 🧰 bold names, quiz letters, details blocks, code and mermaid blocks, links and that the text is really Arabic.
