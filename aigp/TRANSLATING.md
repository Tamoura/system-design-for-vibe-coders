# Arabic edition — translation guide (AI Governance: Zero to Hero)

Not published. Every translator follows this.

## Language and English terms
- Modern Standard Arabic, clear and professional, like a well-written regulator or bank training manual. Faithful: same meaning, structure, emphasis, lists, tables. Never summarise, add or drop content.
- **English beside every technical term on first use in each lesson** (and in the module intro): `الحوكمة (governance)`, `مقدّم النظام (provider)`, `المُشغِّل (deployer)`, `تقييم الأثر على حماية البيانات (DPIA)`. Later uses in the same lesson: Arabic only. Use the English exactly as the English lesson words it.
- Names of laws, standards, frameworks, bodies and cases stay in their English form (EU AI Act, GDPR, NIST AI RMF, ISO/IEC 42001, OECD, EDPB, CJEU, QCB, SDAIA, SCHUFA, Moffatt v. Air Canada). On first use in a lesson you may add a short Arabic rendering before it: «قانون الذكاء الاصطناعي الأوروبي (EU AI Act)».
- Article references stay as written: Art. 22 → «المادة 22 (Art. 22)» on first use, then «المادة 22». Annex III → «الملحق III».
- People: Layla ليلى, Omar عمر, Sara سارة, Khalid خالد, Dana دانة, Yusuf يوسف; Najm Bank → بنك نجم (Najm Bank) on first use per lesson.

## Fixed terms
| English | Arabic |
|---|---|
| AI governance | حوكمة الذكاء الاصطناعي |
| AI system / AI model | نظام الذكاء الاصطناعي / نموذج الذكاء الاصطناعي |
| provider / deployer / importer / distributor | مقدّم النظام / المُشغِّل / المستورد / الموزّع |
| authorised representative | الممثل المفوَّض |
| high-risk | عالي المخاطر |
| prohibited practices | الممارسات المحظورة |
| general-purpose AI (GPAI) model | نموذج ذكاء اصطناعي للأغراض العامة (GPAI) |
| systemic risk | المخاطر النظامية |
| conformity assessment | تقييم المطابقة |
| post-market monitoring | الرصد بعد الطرح في السوق |
| serious incident | الحادث الجسيم |
| fundamental rights impact assessment (FRIA) | تقييم الأثر على الحقوق الأساسية (FRIA) |
| data protection impact assessment (DPIA) | تقييم الأثر على حماية البيانات (DPIA) |
| impact assessment | تقييم الأثر |
| data subject | صاحب البيانات |
| controller / processor | المتحكّم / المعالِج |
| lawful basis | الأساس القانوني |
| legitimate interest | المصلحة المشروعة |
| purpose limitation / data minimisation | تحديد الغرض / تقليل البيانات |
| automated decision-making | اتخاذ القرار الآلي |
| profiling | التنميط |
| human oversight | الإشراف البشري |
| human in/on/over the loop | الإنسان في الحلقة / على الحلقة / فوق الحلقة |
| explainability / interpretability | قابلية التفسير / قابلية الفهم |
| transparency | الشفافية |
| accountability | المساءلة |
| fairness / bias | العدالة / التحيّز |
| disparate impact | الأثر المتفاوت |
| risk appetite / risk tolerance | شهية المخاطر / تحمّل المخاطر |
| AI inventory | سجل أنظمة الذكاء الاصطناعي |
| use case | حالة الاستخدام |
| life cycle | دورة الحياة |
| third-party / supply chain | الطرف الثالث / سلسلة التوريد |
| due diligence | العناية الواجبة |
| training / validation / test data | بيانات التدريب / التحقق / الاختبار |
| data provenance / lineage | مصدر البيانات / تسلسل البيانات |
| drift | الانجراف |
| red-teaming | اختبار الفريق الأحمر |
| TEVV (test, evaluation, verification and validation) | الاختبار والتقييم والتحقق والمصادقة (TEVV) |
| model card / datasheet | بطاقة النموذج / ورقة بيانات مجموعة البيانات |
| hallucination | الهلوسة |
| retrieval-augmented generation (RAG) | التوليد المعزّز بالاسترجاع (RAG) |
| foundation model | النموذج الأساسي |
| fine-tuning | الضبط الدقيق |
| AI literacy | الإلمام بالذكاء الاصطناعي |
| three lines model | نموذج الخطوط الثلاثة |
| AI governance committee | لجنة حوكمة الذكاء الاصطناعي |
| AI management system (AIMS) | نظام إدارة الذكاء الاصطناعي (AIMS) |
| harmonised standard | المعيار المنسَّق |
| regulatory sandbox | البيئة التنظيمية التجريبية |
| incident response | الاستجابة للحوادث |
| decommissioning | الإيقاف والتقاعد |
| Body of Knowledge (BoK) | مجال المعرفة (BoK) |

## Structure the build depends on (do not break)
- Module heading: `# الوحدة N — العنوان` (N unchanged). Lesson heading: `# N.M — العنوان` (numbers unchanged).
- The line right after each lesson heading, translated like this and nothing else:
  `*المستوى: 🟢 مبتدئ* · *المتطلبات: 1.1، 4.1* · *مجال المعرفة (BoK): II.C*`
  (🟢 مبتدئ / 🟡 متوسط / 🔴 متقدم; keep the same emoji; keep lesson numbers and BoK codes; separate lists with «، »). If the English has no prerequisites, omit that part as the English does.
- Section headings keep their emoji first, translated: `## ⚡ الدرس في دقيقة`, `## 🧭 لماذا يهم`, `## 📐 كيف يعمل`, `### 🟢 الأساسيات`, `### 🟡 التعمق أكثر`, `### 🔴 نظرة الخبير`, `## ⚖️ الأدوات التنظيمية`, `## 🏛️ عمليًا في بنك نجم`, `## 🛠️ التمارين`, `## ⚠️ أخطاء وفخاخ الامتحان`, `## 🧾 الخلاصة`, `## ✍️ اختبر نفسك`, `## 📚 المراجع` (12.3: `## ✍️ الامتحان التجريبي`). Same number of `#`/`##`/`###` headings in the same order as the English.
- **⚖️ tables:** the first cell of every row must START with the same bold English instrument name as the English row, exactly (e.g. `**EU AI Act** — المادة 6 والملحق III`, `**GDPR** — المادة 22`). Translate everything after the bold name and the other cells. Header row: `| الأداة | ما تشترطه أو توصي به | إشارة الامتحان |`.
- **Quizzes:** keep the question numbers; options stay labelled `- A.` `- B.` `- C.` `- D.` in Latin letters and in the same order; `<details><summary>الإجابة</summary>` then a blank line, then `**X.**` with the SAME correct letter as the English; letters cited in explanations stay the same Latin letters. Same number of questions and `<details>` blocks. In 12.3 keep the competency tag as `*الكفاءة: II.C*`.
- Keep unchanged: fenced code, inline `code`, URLs and link targets, mermaid syntax and node IDs (translate only label text, keep it short, no parentheses inside labels), numbers, dates (write dates as in English but you may use Arabic month names: 2 أغسطس 2026), `---` separators, tables' column counts.
- `**Done when:**`/`*Done when:*` → `*يكتمل عندما:*`.

## Verify
Run: `python3 aigp/check_ar.py <english file> <arabic file>` until it prints ✓. It checks headings, the level/BoK lines, section emoji order, ⚖️ bold names, quiz letters, details blocks, mermaid blocks, code, links and that the text is really Arabic.
