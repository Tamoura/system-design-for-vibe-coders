#!/usr/bin/env node
/**
 * Build the self-assessment page of every course in the library.
 *
 *   node scripts/build-assessment.mjs                 → every course with an assessment: <dir>/assessment[.ar].html
 *   node scripts/build-assessment.mjs --course=aigp   → one course only
 *   node scripts/build-assessment.mjs --check         → fail if a committed page is stale or the items are malformed
 *
 * Sources per course: <course>/assessment/areas.json (the course's areas or modules and their lessons) and
 * <course>/assessment/data/<area>.json (4 questions + 2 evidence items per area, each in English and Arabic).
 * The vibe course keeps its sources in assessment/ at the repo root. Pages are self-contained: answers stay in
 * the reader's browser (localStorage) and can be exported as JSON for a teacher's group view. Lesson links point
 * at the course reader next to the page.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CHECK = process.argv.includes('--check');
const ONLY = (process.argv.find((a) => a.startsWith('--course=')) || '').slice(9) || null;

/* ---------------------------------------------------------------- courses */

const COURSES = [
  { id: 'vibe', src: 'assessment', out: '', reader: { en: 'index.en.html', ar: 'index.ar.html' }, mode: 'l', store: 'sdvc', theme: 'sdvc-theme',
    name: { en: 'System Design for Vibe Coders', ar: 'تصميم الأنظمة لمبرمجي الفايب (System Design for Vibe Coders)' }, brand: 'SD4VC',
    unit: { en: 'area', ens: 'areas', ar: 'مجال (area)', ars: 'مجالات (areas)' },
    evidenceHint: { en: 'on your phone, in the data, in the logs — not what your agent told you', ar: 'على هاتفك أو في البيانات (data) أو في السجلات (logs)، لا ما قاله لك وكيلك (agent)' },
    levels: {
      en: [['🟢 Vibe coder', 'You can get things working with an agent. The next step is knowing why systems break — start with the areas marked Not yet.'],
        ['🟡 Builder', 'You know the core ideas in most areas. Turn knowledge into habit: do the "verify it" steps in the lessons and tick the evidence.'],
        ['🟠 Operator', 'You can run a real product: you know the failure modes and have practised most of the safety nets. Close the remaining gaps.'],
        ['🔴 Architect', 'You know every area and have practised nearly all of them. You can direct an AI team on a production system — and teach others.']],
      ar: [['🟢 مبرمج فايب (Vibe coder)', 'تستطيع أن تجعل الأشياء تعمل مع وكيل (agent). الخطوة التالية أن تعرف لماذا تنكسر الأنظمة؛ ابدأ بالمجالات الموسومة «ليس بعد (Not yet)».'],
        ['🟡 بنّاء (Builder)', 'تعرف الأفكار الأساسية في معظم المجالات. حوّل المعرفة إلى عادة: نفّذ خطوات «تحقق منه (verify it)» في الدروس وضع علامات على الأدلة.'],
        ['🟠 مشغّل (Operator)', 'تستطيع تشغيل منتج حقيقي: تعرف أنماط الفشل (failure modes) ومارست معظم شبكات الأمان (safety nets). أغلق الفجوات المتبقية.'],
        ['🔴 مهندس أنظمة (Architect)', 'تعرف كل المجالات ومارست معظمها تقريبًا. تستطيع قيادة فريق ذكاء اصطناعي (AI team) على نظام في الإنتاج (production)، وتعليم غيرك.']] } },
  { id: 'saas', src: 'saas/assessment', out: 'saas', reader: { en: 'index.html', ar: 'index.ar.html' }, mode: 'hash', store: 'saas', theme: 'saas-theme',
    name: { en: 'SaaS Building Blocks', ar: 'مكوّنات بناء SaaS (SaaS Building Blocks)' }, brand: 'SaaS Building Blocks',
    unit: { en: 'module', ens: 'modules', ar: 'وحدة (module)', ars: 'وحدات (modules)' },
    evidenceHint: { en: 'in your app, in the data, in the logs — not what your agent told you', ar: 'في تطبيقك أو في البيانات (data) أو في السجلات (logs)، لا ما قاله لك وكيلك (agent)' },
    levels: {
      en: [['🟢 Explorer', 'You know what a SaaS is made of. Next: learn how each building block works and fails — start with the modules marked Not yet.'],
        ['🟡 Builder', 'You know the core building blocks in most modules. Turn knowledge into habit: build the exercises and tick the evidence.'],
        ['🟠 Operator', 'You can run a real SaaS: identity, data, money, background work and operations. Close the remaining gaps.'],
        ['🔴 SaaS architect', 'You know every building block and have practised nearly all of them. You can design and direct a production SaaS — and teach others.']],
      ar: [['🟢 مستكشف (Explorer)', 'تعرف مما يتكوّن منتج SaaS. الخطوة التالية أن تتعلم كيف يعمل كل مكوّن (building block) وكيف يفشل؛ ابدأ بالوحدات الموسومة «ليس بعد (Not yet)».'],
        ['🟡 بنّاء (Builder)', 'تعرف المكوّنات الأساسية في معظم الوحدات. حوّل المعرفة إلى عادة: نفّذ التمارين (exercises) وضع علامات على الأدلة.'],
        ['🟠 مشغّل (Operator)', 'تستطيع تشغيل منتج SaaS حقيقي: الهوية (identity)، والبيانات (data)، والمال (money)، والعمل في الخلفية (background work)، والعمليات (operations). أغلق الفجوات المتبقية.'],
        ['🔴 مهندس SaaS (SaaS architect)', 'تعرف كل المكوّنات ومارست معظمها تقريبًا. تستطيع تصميم منتج SaaS في الإنتاج (production) وقيادة بنائه، وتعليم غيرك.']] } },
  { id: 'aigp', src: 'aigp/assessment', out: 'aigp', reader: { en: 'index.html', ar: 'index.ar.html' }, mode: 'hash', store: 'aigp', theme: 'aigp-theme',
    name: { en: 'AI Governance: Zero to Hero', ar: 'حوكمة الذكاء الاصطناعي: من الصفر إلى الاحتراف (AI Governance: Zero to Hero)' }, brand: 'AI Governance',
    unit: { en: 'module', ens: 'modules', ar: 'وحدة (module)', ars: 'وحدات (modules)' },
    evidenceHint: { en: 'a real policy, assessment, register or decision you produced — not something you only read about', ar: 'سياسة (policy) أو تقييم (assessment) أو سجل (register) أو قرار (decision) حقيقي أعددته أنت، لا شيء قرأت عنه فقط' },
    levels: {
      en: [['🟢 Newcomer', 'You know what AI governance is for. Next: the laws, standards and processes — start with the modules marked Not yet.'],
        ['🟡 Practitioner', 'You know the core of most domains. Practise: produce the artefacts in the lessons and tick the evidence.'],
        ['🟠 Professional', 'You can run real governance work across the AI life cycle. Close the remaining gaps, then sit the 100-question mock exam in lesson 12.3.'],
        ['🔴 Governance lead', 'You know every domain and have practised nearly all of it. You are ready for the AIGP exam and to lead an AI governance programme.']],
      ar: [['🟢 مبتدئ (Newcomer)', 'تعرف الغرض من حوكمة الذكاء الاصطناعي (AI governance). الخطوة التالية: القوانين (laws) والمعايير (standards) والعمليات (processes)؛ ابدأ بالوحدات الموسومة «ليس بعد (Not yet)».'],
        ['🟡 ممارس (Practitioner)', 'تعرف جوهر معظم المجالات (domains). مارِس: أعدّ الوثائق (artefacts) الواردة في الدروس وضع علامات على الأدلة.'],
        ['🟠 محترف (Professional)', 'تستطيع أداء عمل حوكمة حقيقي عبر دورة حياة الذكاء الاصطناعي (AI life cycle). أغلق الفجوات المتبقية، ثم خض الامتحان التجريبي (mock exam) من 100 سؤال في الدرس 12.3.'],
        ['🔴 قائد حوكمة (Governance lead)', 'تعرف كل المجالات ومارست معظمها تقريبًا. أنت جاهز لامتحان AIGP ولقيادة برنامج لحوكمة الذكاء الاصطناعي (AI governance programme).']] } },
  { id: 'aipm', src: 'aipm/assessment', out: 'aipm', reader: { en: 'index.html', ar: 'index.ar.html' }, mode: 'hash', store: 'aipm', theme: 'aipm-theme',
    name: { en: 'AI Product Management: Zero to Hero', ar: 'إدارة منتجات الذكاء الاصطناعي: من الصفر إلى الاحتراف (AI Product Management: Zero to Hero)' }, brand: 'AI Product Management',
    unit: { en: 'module', ens: 'modules', ar: 'وحدة (module)', ars: 'وحدات (modules)' },
    evidenceHint: { en: 'a real brief, scorecard, spec, eval plan or launch decision you produced — not something you only read about', ar: 'موجز (brief) أو بطاقة تقييم (scorecard) أو مواصفات (spec) أو خطة تقييم (eval plan) أو قرار إطلاق (launch decision) حقيقي أعددته أنت، لا شيء قرأت عنه فقط' },
    levels: {
      en: [['🟢 Curious', 'You know how AI products differ. Next: discovery, design and evaluation — start with the modules marked Not yet.'],
        ['🟡 Practitioner', 'You can discover, specify and evaluate AI features in most areas. Practise: build the artefacts and tick the evidence.'],
        ['🟠 AI product manager', 'You can take an AI product from idea to launch and measure it. Close the remaining gaps.'],
        ['🔴 AI product leader', 'You know every module and have practised nearly all of it. You can lead AI product strategy and teams — and teach others.']],
      ar: [['🟢 فضولي (Curious)', 'تعرف كيف تختلف منتجات الذكاء الاصطناعي (AI products). الخطوة التالية: الاكتشاف (discovery) والتصميم (design) والتقييم (evaluation)؛ ابدأ بالوحدات الموسومة «ليس بعد (Not yet)».'],
        ['🟡 ممارس (Practitioner)', 'تستطيع اكتشاف ميزات الذكاء الاصطناعي (AI features) وكتابة مواصفاتها (specs) وتقييمها في معظم المجالات. مارِس: أعدّ الوثائق (artefacts) وضع علامات على الأدلة.'],
        ['🟠 مدير منتج ذكاء اصطناعي (AI product manager)', 'تستطيع أخذ منتج ذكاء اصطناعي من الفكرة إلى الإطلاق (launch) وقياسه. أغلق الفجوات المتبقية.'],
        ['🔴 قائد منتجات ذكاء اصطناعي (AI product leader)', 'تعرف كل الوحدات ومارست معظمها تقريبًا. تستطيع قيادة استراتيجية المنتج (product strategy) والفرق، وتعليم غيرك.']] } },
  { id: 'secai', src: 'secai/assessment', out: 'secai', reader: { en: 'index.html', ar: 'index.ar.html' }, mode: 'hash', store: 'secai', theme: 'secai-theme',
    name: { en: 'Secure AI & Application Security: Zero to Hero', ar: 'أمن الذكاء الاصطناعي والتطبيقات: من الصفر إلى الاحتراف (Secure AI & Application Security: Zero to Hero)' }, brand: 'Secure AI & AppSec',
    unit: { en: 'module', ens: 'modules', ar: 'وحدة (module)', ars: 'وحدات (modules)' },
    evidenceHint: { en: 'on your own code, a local lab or a training app, with the result checked — never on systems you are not authorised to test', ar: 'على كودك (code) أو مختبر محلي (local lab) أو تطبيق تدريبي (training app)، مع التحقق من النتيجة، وليس أبدًا على أنظمة غير مصرَّح لك باختبارها' },
    levels: {
      en: [['🟢 Aware', 'You know how attackers get in. Next: the classic weaknesses and their fixes — start with the modules marked Not yet.'],
        ['🟡 Practitioner', 'You can find and fix the common web, identity, API and cloud weaknesses. Practise in a lab and tick the evidence.'],
        ['🟠 Defender', 'You can secure applications and AI systems and respond to incidents. Close the remaining gaps.'],
        ['🔴 Security lead', 'You know every module and have practised nearly all of it. You can lead application and AI security — and teach others.']],
      ar: [['🟢 مُدرِك (Aware)', 'تعرف كيف يدخل المهاجمون (attackers). الخطوة التالية: نقاط الضعف الكلاسيكية (classic weaknesses) وطرق إصلاحها؛ ابدأ بالوحدات الموسومة «ليس بعد (Not yet)».'],
        ['🟡 ممارس (Practitioner)', 'تستطيع اكتشاف نقاط الضعف الشائعة في الويب (web) والهوية (identity) وواجهات API والسحابة (cloud) وإصلاحها. مارِس في مختبر (lab) وضع علامات على الأدلة.'],
        ['🟠 مدافع (Defender)', 'تستطيع تأمين التطبيقات وأنظمة الذكاء الاصطناعي والاستجابة للحوادث (incidents). أغلق الفجوات المتبقية.'],
        ['🔴 قائد أمن (Security lead)', 'تعرف كل الوحدات ومارست معظمها تقريبًا. تستطيع قيادة أمن التطبيقات والذكاء الاصطناعي (application and AI security)، وتعليم غيرك.']] } },
];

/* ---------------------------------------------------------------- load + validate */

function load(C) {
  const dir = path.join(ROOT, C.src);
  const AREAS = JSON.parse(fs.readFileSync(path.join(dir, 'areas.json'), 'utf8'));
  const problems = [];
  const items = AREAS.map((a) => {
    const f = path.join(dir, 'data', `${a.id}.json`);
    if (!fs.existsSync(f)) { problems.push(`missing ${path.relative(ROOT, f)}`); return { area: a.id, questions: [], evidence: [] }; }
    const d = JSON.parse(fs.readFileSync(f, 'utf8'));
    if (d.area !== a.id) problems.push(`${C.id}/${a.id}: "area" is ${d.area}`);
    if (d.questions?.length !== 4) problems.push(`${C.id}/${a.id}: ${d.questions?.length} questions, expected 4`);
    if (d.evidence?.length !== 2) problems.push(`${C.id}/${a.id}: ${d.evidence?.length} evidence items, expected 2`);
    for (const q of d.questions || []) {
      for (const l of ['en', 'ar']) {
        if (!q.q?.[l] || !q.why?.[l]) problems.push(`${C.id}/${q.id}: missing ${l} text`);
        if (q.o?.[l]?.length !== 4) problems.push(`${C.id}/${q.id}: ${l} needs 4 options`);
      }
      if (!(q.a >= 0 && q.a <= 3)) problems.push(`${C.id}/${q.id}: answer index ${q.a}`);
      if (![1, 2, 3].includes(q.level)) problems.push(`${C.id}/${q.id}: level ${q.level}`);
      if (!a.lessons.includes(q.lesson) && C.id !== 'vibe') problems.push(`${C.id}/${q.id}: lesson ${q.lesson} is not in module ${a.key}`);
    }
    for (const e of d.evidence || []) if (!e.text?.en || !e.text?.ar) problems.push(`${C.id}/${e.id}: missing text`);
    return d;
  });
  const SRC = crypto.createHash('sha256')
    .update(fs.readFileSync(path.join(dir, 'areas.json')))
    .update(JSON.stringify(items))
    .update(JSON.stringify(C))
    .update(fs.readFileSync(fileURLToPath(import.meta.url)))
    .digest('hex').slice(0, 16);
  const nq = items.reduce((n, d) => n + d.questions.length, 0), ne = items.reduce((n, d) => n + d.evidence.length, 0);
  return { AREAS, items, SRC, problems, nq, ne, na: AREAS.length };
}

/* ---------------------------------------------------------------- strings */

function makeT(C, lang, L) {
  const { na, nq } = L, per = Math.round(nq / na), mins = Math.max(10, Math.round(nq * 0.35 / 5) * 5);
  const U = C.unit, rd = C.reader[lang];
  if (lang === 'en') return {
    dir: 'ltr', title: `${C.name.en} — Self-Assessment`, reader: rd,
    other: { href: 'assessment.ar.html', label: 'العربية' },
    brand: `${C.brand} · Self-assessment`, back: '← Course', home: 'Library',
    h1: 'Where do you stand?',
    lede: `A self-assessment for <a href="${rd}">${C.name.en}</a>: ${nq} questions across the course's ${na} ${U.ens}, plus a checklist of what you have actually done. You get a level, a map of strong and weak ${U.ens}, and the exact lessons to study next.`,
    tabs: { start: 'Start', knowledge: 'Knowledge check', evidence: 'Evidence', results: 'Results', group: 'Group view' },
    startH: 'How it works',
    startSteps: [
      `<b>Knowledge check</b> — ${nq} multiple-choice questions, ${per} per ${U.en}, about ${mins} minutes. Answer without looking things up; unanswered counts as wrong.`,
      '<b>Evidence</b> — tick only what you have <em>actually done and verified yourself</em>. "I could do it" is not "I did it".',
      `<b>Results</b> — each ${U.en} is <i>Not yet</i>, <i>Aware</i> (3 of 4 questions right) or <i>Practised</i> (aware + both evidence items). Your level and the lessons to study next follow from that.`,
    ],
    nameL: 'Your name (optional — only used in the exported result)', nameP: 'e.g. Sara',
    privacy: 'Everything stays in this browser. Nothing is sent anywhere unless you export your result yourself.',
    begin: 'Begin the knowledge check →',
    kH: 'Knowledge check', kSub: 'Pick the best answer. You can change answers until you open your results.',
    toEvidence: 'Continue to evidence →',
    lvl: { 1: '🟢 core idea', 2: '🟡 apply it', 3: '🔴 judgement' },
    eH: 'Evidence of practice', eSub: `Tick only what you have done for real and checked with your own eyes — ${C.evidenceHint.en}.`,
    toResults: 'See my results →',
    rEmpty: 'Answer the knowledge check first — your results appear here.',
    rH: 'Your results', score: 'Knowledge score', areasAware: `${U.ens} aware`, areasPract: `${U.ens} practised`,
    status: ['Not yet', 'Aware', 'Practised'],
    levels: C.levels.en,
    colArea: U.en[0].toUpperCase() + U.en.slice(1), colK: 'Knowledge', colE: 'Evidence', colS: 'Status',
    nextH: 'Study next', nextSub: `The lessons behind the questions you missed, weakest ${U.ens} first.`, nextNone: 'Nothing to review — every answer was right.',
    reviewH: 'Review your answers', yours: 'Your answer', right: 'Correct answer', noAns: 'not answered', lessonW: 'Lesson',
    saveH: 'Save & share', saveSub: 'Download your result to keep it or send it to your teacher, who can combine everyone\'s results in the Group view.',
    exportB: 'Download my result (JSON)', printB: 'Print', resetB: 'Start over', resetQ: 'Erase all answers and start over?',
    gH: 'Group view — for teachers and team leads', gSub: `Load the JSON results your learners exported to see who is where and which ${U.ens} the group is weakest in. Files are read in this browser only.`,
    gPaste: '…or paste one or more exported results:', gAdd: 'Add pasted results', gName: 'Name', gLevel: 'Level', gScore: 'Score',
    gCover: 'aware or practised', gBad: 'Could not read that — paste the exported JSON.',
    footer: 'Part of the <a href="../">Course Library</a> · self-contained, no data leaves this browser · generated by <code>npm run assess:build</code>',
    theme: 'Theme',
  };
  return {
    dir: 'rtl', title: `${C.name.ar} — التقييم الذاتي (Self-Assessment)`, reader: rd,
    other: { href: 'assessment.html', label: 'English' },
    brand: `${C.brand} · التقييم الذاتي (Self-assessment)`, back: 'الدورة →', home: 'المكتبة',
    h1: 'أين تقف الآن؟',
    lede: `تقييم ذاتي (self-assessment) لدورة <a href="${rd}">${C.name.ar.replace(/\(([^()]+)\)$/, '<bdi>($1)</bdi>')}</a>: ‏${nq} سؤالًا موزعة على ${U.ars} الدورة البالغ عددها ${na}، مع قائمة تحقق (checklist) بما فعلته فعلًا. تحصل على مستوى (level)، وخريطة لنقاط قوتك وضعفك، والدروس المحددة التي تدرسها بعد ذلك.`,
    tabs: { start: 'البداية', knowledge: 'اختبار المعرفة (Knowledge check)', evidence: 'الأدلة (Evidence)', results: 'النتائج (Results)', group: 'عرض المجموعة (Group view)' },
    startH: 'كيف يعمل',
    startSteps: [
      `<b>اختبار المعرفة (Knowledge check)</b> — ‏${nq} سؤال اختيار من متعدد (multiple-choice)، ${per} لكل ${U.ar}، نحو ${mins} دقيقة. أجب دون أن تبحث؛ السؤال الذي لا تجيب عنه يُحسب خطأً.`,
      '<b>الأدلة (Evidence)</b> — ضع علامة فقط على ما <em>فعلته فعلًا وتحققت منه بنفسك (actually done and verified)</em>. «أستطيع فعله» ليس «فعلته».',
      `<b>النتائج (Results)</b> — كل ${U.ar} إما <i>ليس بعد (Not yet)</i>، أو <i>مُلِمّ (Aware)</i> (ثلاث إجابات صحيحة من أربع)، أو <i>ممارِس (Practised)</i> (مُلِمّ مع دليلَي الممارسة كليهما). ومن ذلك يُحدَّد مستواك والدروس التي تدرسها بعد ذلك.`,
    ],
    nameL: 'اسمك (اختياري، يُستخدم فقط في النتيجة المُصدَّرة (exported result))', nameP: 'مثلًا: سارة',
    privacy: 'كل شيء يبقى في هذا المتصفح (browser). لا يُرسَل شيء إلى أي مكان إلا إذا صدّرت نتيجتك بنفسك.',
    begin: 'ابدأ اختبار المعرفة ←',
    kH: 'اختبار المعرفة (Knowledge check)', kSub: 'اختر أفضل إجابة. يمكنك تغيير إجاباتك حتى تفتح نتائجك.',
    toEvidence: 'تابع إلى الأدلة ←',
    lvl: { 1: '🟢 فكرة أساسية (core idea)', 2: '🟡 طبّقها (apply it)', 3: '🔴 حكم وتقدير (judgement)' },
    eH: 'أدلة الممارسة (Evidence of practice)', eSub: `ضع علامة فقط على ما فعلته حقًا وتحققت منه بعينيك: ${C.evidenceHint.ar}.`,
    toResults: 'اعرض نتائجي ←',
    rEmpty: 'أجب عن اختبار المعرفة أولًا، وستظهر نتائجك هنا.',
    rH: 'نتائجك', score: 'درجة المعرفة (Knowledge score)', areasAware: `${U.ars} مُلِمّ بها (aware)`, areasPract: `${U.ars} تمارسها (practised)`,
    status: ['ليس بعد (Not yet)', 'مُلِمّ (Aware)', 'ممارِس (Practised)'],
    levels: C.levels.ar,
    colArea: U.ar, colK: 'المعرفة (Knowledge)', colE: 'الأدلة (Evidence)', colS: 'الحالة (Status)',
    nextH: 'ادرس بعد ذلك (Study next)', nextSub: 'الدروس التي تقف خلف الأسئلة التي أخطأت فيها، بدءًا بالأضعف.', nextNone: 'لا شيء للمراجعة، فكل إجاباتك صحيحة.',
    reviewH: 'راجع إجاباتك', yours: 'إجابتك', right: 'الإجابة الصحيحة', noAns: 'لم تُجب', lessonW: 'الدرس',
    saveH: 'احفظ وشارك', saveSub: 'نزّل نتيجتك لتحتفظ بها أو ترسلها إلى معلّمك، الذي يستطيع جمع نتائج الجميع في عرض المجموعة (Group view).',
    exportB: 'نزّل نتيجتي (JSON)', printB: 'اطبع', resetB: 'ابدأ من جديد', resetQ: 'هل تريد مسح كل الإجابات والبدء من جديد؟',
    gH: 'عرض المجموعة (Group view) — للمعلّمين وقادة الفرق', gSub: 'حمّل نتائج JSON التي صدّرها المتعلمون لترى أين يقف كل واحد، وما الأجزاء الأضعف لدى المجموعة. تُقرأ الملفات في هذا المتصفح فقط.',
    gPaste: '…أو الصق نتيجة مُصدَّرة أو أكثر:', gAdd: 'أضف النتائج الملصقة', gName: 'الاسم', gLevel: 'المستوى (Level)', gScore: 'الدرجة (Score)',
    gCover: 'مُلِمّ أو ممارِس', gBad: 'تعذّرت قراءتها، الصق ملف JSON المُصدَّر.',
    footer: 'جزء من <a href="../">مكتبة الدورات</a> · صفحة مستقلة، لا تغادر بياناتك هذا المتصفح · مولَّدة عبر <code>npm run assess:build</code>',
    theme: 'المظهر',
  };
}

/* ---------------------------------------------------------------- page */

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function page(C, L, lang) {
  const t = makeT(C, lang, L);
  const { AREAS, items, SRC } = L;
  const data = {
    lang, reader: t.reader, cfg: { key: `${C.store}-assessment-v1`, tool: `${C.store}-assessment`, theme: C.theme, mode: C.mode },
    areas: AREAS.map((a) => ({ id: a.id, key: a.key, name: a[lang] })),
    qs: items.flatMap((d) => d.questions.map((q) => ({ id: q.id, area: d.area, level: q.level, lesson: q.lesson, q: q.q[lang], o: q.o[lang], a: q.a, why: q.why[lang] }))),
    ev: items.flatMap((d) => d.evidence.map((e) => ({ id: e.id, area: d.area, lesson: e.lesson, text: e.text[lang] }))),
    t,
  };
  const json = JSON.stringify(data).replace(/</g, '\\u003c');
  return `<!doctype html>
<html lang="${lang}" dir="${t.dir}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="assess-source" content="${SRC}">
<title>${esc(t.title)}</title>
<style>
:root{--bg:#F4F6F7;--surface:#FCFDFD;--ink:#1C2630;--muted:#5B6B79;--line:#DBE2E7;--ember:#B33F1C;--ember-soft:#F6E7E1;--blue:#33619E;
--good:#3E7A52;--good-soft:#E3F0E7;--mid:#8A6D1F;--mid-soft:#F5EEDB;--bad:#9C3838;--bad-soft:#F6E4E4;--code-bg:#EDF1F3;
--sans:"Avenir Next","Segoe UI",system-ui,-apple-system,sans-serif;--serif:Charter,"Iowan Old Style","Palatino Linotype",Georgia,serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121920;--surface:#1A232C;--ink:#E4EAEF;--muted:#94A3B1;--line:#2B3743;--ember:#E0673C;--ember-soft:#33221B;--blue:#729FD9;
--good:#6FAF85;--good-soft:#1C2B22;--mid:#D8B45A;--mid-soft:#33290F;--bad:#E08A8A;--bad-soft:#3A2020;--code-bg:#141B22}}
:root[data-theme="dark"]{--bg:#121920;--surface:#1A232C;--ink:#E4EAEF;--muted:#94A3B1;--line:#2B3743;--ember:#E0673C;--ember-soft:#33221B;--blue:#729FD9;
--good:#6FAF85;--good-soft:#1C2B22;--mid:#D8B45A;--mid-soft:#33290F;--bad:#E08A8A;--bad-soft:#3A2020;--code-bg:#141B22}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:1rem/1.65 var(--serif);overflow-x:hidden}
html[lang="ar"] body{font-family:"Noto Naskh Arabic","Geeza Pro","Segoe UI",Tahoma,sans-serif;line-height:1.85}
a{color:var(--blue)}
.wrap{max-width:52rem;margin:0 auto;padding:0 16px}
.top{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 90%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;gap:.9rem;padding:.55rem 16px;flex-wrap:wrap;font-family:var(--sans);font-size:.85rem}
.top .brand{font-family:var(--mono);font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;font-weight:600;color:var(--ink);text-decoration:none}
.top nav{margin-inline-start:auto;display:flex;gap:.8rem;align-items:center}
.top button{font:inherit;background:none;border:1px solid var(--line);border-radius:999px;padding:.1rem .6rem;color:var(--muted);cursor:pointer}
header.hero{padding:2.2rem 0 1rem}
.eyebrow{font-family:var(--mono);font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;color:var(--ember)}
h1,h2,h3{font-family:var(--sans);line-height:1.25;letter-spacing:-.01em}
h1{font-size:clamp(1.7rem,4.5vw,2.4rem);margin:.3rem 0 .6rem}
html[lang="ar"] h1,html[lang="ar"] h2,html[lang="ar"] h3{font-family:inherit;letter-spacing:0}
.lede{color:var(--muted);font-size:1.05rem;margin:0}
.tabs{display:flex;gap:.4rem;flex-wrap:wrap;margin:1.2rem 0;font-family:var(--sans)}
html[lang="ar"] .tabs{font-family:inherit}
.tabs button{font:inherit;font-weight:600;font-size:.9rem;padding:.45rem .95rem;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--muted);cursor:pointer}
.tabs button.on{background:var(--ember);border-color:var(--ember);color:#fff}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:1.2rem 1.3rem;margin:0 0 1rem;overflow-wrap:anywhere}
.q label>span{min-width:0}
.card h2{margin:.1rem 0 .4rem;font-size:1.3rem}
.sub{color:var(--muted);margin:.2rem 0 1rem}
.hide{display:none}
ol.steps{padding-inline-start:1.2rem}ol.steps li{margin:.4rem 0}
label.field{display:block;font-family:var(--sans);font-size:.9rem;color:var(--muted);margin:.8rem 0 .3rem}
html[lang="ar"] label.field{font-family:inherit}
input[type=text],textarea{width:100%;font:inherit;padding:.5rem .7rem;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink)}
textarea{min-height:5rem;font-family:var(--mono);font-size:.8rem}
button.primary,button.ghost{font:inherit;font-family:var(--sans);font-weight:600;border-radius:8px;padding:.6rem 1.1rem;cursor:pointer;margin:.6rem .4rem 0 0}
html[lang="ar"] button.primary,html[lang="ar"] button.ghost{font-family:inherit;margin:.6rem 0 0 .4rem}
button.primary{background:var(--ember);color:#fff;border:1px solid var(--ember)}
button.ghost{background:none;color:var(--ink);border:1px solid var(--line)}
.privacy{font-size:.88rem;color:var(--muted);border-inline-start:3px solid var(--good);padding-inline-start:.7rem}
.progress{position:sticky;top:2.6rem;z-index:4;font-family:var(--mono);font-size:.78rem;color:var(--muted);background:var(--surface);padding:.3rem 0;border-bottom:1px solid var(--line);margin-bottom:.6rem}
.area-h{font-family:var(--sans);font-size:1.02rem;margin:1.6rem 0 .5rem;padding-bottom:.25rem;border-bottom:2px solid var(--ember-soft)}
html[lang="ar"] .area-h{font-family:inherit}
.area-h .k{font-family:var(--mono);font-size:.75rem;color:var(--ember);margin-inline-end:.5rem}
.q{margin:.9rem 0 1.2rem}
.q .stem{font-weight:600;margin:0 0 .45rem}
.q .lv{font-family:var(--mono);font-size:.7rem;color:var(--muted);display:block;margin-bottom:.15rem}
.q label{display:flex;gap:.6rem;align-items:flex-start;padding:.45rem .7rem;border:1px solid var(--line);border-radius:8px;margin:.3rem 0;cursor:pointer;background:var(--bg)}
.q label:hover{border-color:var(--ember)}
.q input{margin-top:.35rem;accent-color:var(--ember)}
.q label.sel{border-color:var(--ember);background:var(--ember-soft)}
.ev label{display:flex;gap:.6rem;align-items:flex-start;margin:.35rem 0;cursor:pointer}
.ev input{margin-top:.4rem;accent-color:var(--good)}
.ev .ln{font-family:var(--mono);font-size:.72rem;color:var(--muted)}
.level{border-radius:12px;padding:1rem 1.2rem;background:var(--ember-soft);margin:.4rem 0 1rem}
.level b{font-family:var(--sans);font-size:1.35rem;display:block}
html[lang="ar"] .level b{font-family:inherit}
.kpis{display:flex;gap:1rem;flex-wrap:wrap;margin:.2rem 0 1rem;font-family:var(--sans)}
.kpis div{background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:.55rem .9rem;min-width:8rem}
.kpis b{display:block;font-size:1.4rem}
.kpis span{font-size:.8rem;color:var(--muted)}
.tbl{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.93rem}
th,td{text-align:start;padding:.45rem .5rem;border-bottom:1px solid var(--line);vertical-align:top}
th{font-family:var(--sans);font-size:.8rem;color:var(--muted);font-weight:600}
html[lang="ar"] th{font-family:inherit}
.bar{display:inline-block;width:4.5rem;height:.5rem;border-radius:999px;background:var(--line);vertical-align:middle;margin-inline-end:.4rem;overflow:hidden}
.bar i{display:block;height:100%;background:var(--ember)}
.st{display:inline-block;font-size:.78rem;font-weight:600;border-radius:999px;padding:.05rem .55rem;white-space:nowrap}
.st0{background:var(--bad-soft);color:var(--bad)}.st1{background:var(--mid-soft);color:var(--mid)}.st2{background:var(--good-soft);color:var(--good)}
ul.next{padding-inline-start:1.1rem}ul.next li{margin:.35rem 0}
details.rev{border:1px solid var(--line);border-radius:8px;padding:.5rem .8rem;margin:.4rem 0;background:var(--bg)}
details.rev summary{cursor:pointer;font-weight:600}
.ok{color:var(--good)}.no{color:var(--bad)}
footer{color:var(--muted);font-size:.82rem;padding:2rem 0 3rem;text-align:center}
@media print{.top,.tabs,.noprint,footer{display:none}.card{border:0;padding:0}body{background:#fff}}
</style>
</head>
<body>
<div class="top"><div class="wrap">
  <a class="brand" href="${t.reader}">${esc(t.brand)}</a>
  <nav><a href="${t.reader}">${esc(t.back)}</a><a href="../">${esc(t.home)}</a><a href="${t.other.href}" hreflang="${lang === 'en' ? 'ar' : 'en'}">${t.other.label}</a>
  <button type="button" id="theme" aria-label="${esc(t.theme)}">◐</button></nav>
</div></div>
<div class="wrap">
<header class="hero">
  <div class="eyebrow">${esc(C.name.en)}</div>
  <h1>${esc(t.h1)}</h1>
  <p class="lede">${t.lede}</p>
</header>
<div class="tabs" role="tablist">
  ${['start', 'knowledge', 'evidence', 'results', 'group'].map((k) => `<button type="button" data-tab="${k}">${esc(t.tabs[k])}</button>`).join('')}
</div>
<section id="tab-start" class="card">
  <h2>${esc(t.startH)}</h2>
  <ol class="steps">${t.startSteps.map((s) => `<li>${s}</li>`).join('')}</ol>
  <label class="field" for="name">${esc(t.nameL)}</label>
  <input type="text" id="name" placeholder="${esc(t.nameP)}" autocomplete="name">
  <p class="privacy">${esc(t.privacy)}</p>
  <button type="button" class="primary" data-go="knowledge">${esc(t.begin)}</button>
</section>
<section id="tab-knowledge" class="card hide">
  <h2>${esc(t.kH)}</h2><p class="sub">${esc(t.kSub)}</p>
  <div class="progress" id="kprog"></div>
  <div id="klist"></div>
  <button type="button" class="primary" data-go="evidence">${esc(t.toEvidence)}</button>
</section>
<section id="tab-evidence" class="card hide">
  <h2>${esc(t.eH)}</h2><p class="sub">${esc(t.eSub)}</p>
  <div id="elist" class="ev"></div>
  <button type="button" class="primary" data-go="results">${esc(t.toResults)}</button>
</section>
<section id="tab-results" class="hide"><div id="rout"></div></section>
<section id="tab-group" class="card hide">
  <h2>${esc(t.gH)}</h2><p class="sub">${esc(t.gSub)}</p>
  <input type="file" id="gfiles" multiple accept=".json,application/json">
  <label class="field" for="gpaste">${esc(t.gPaste)}</label>
  <textarea id="gpaste"></textarea>
  <button type="button" class="ghost" id="gadd">${esc(t.gAdd)}</button>
  <div id="gout"></div>
</section>
<footer>${t.footer}</footer>
</div>
<script>
"use strict";
const D = ${json};
const T = D.t, KEY = D.cfg.key, TOOL = D.cfg.tool, N = D.areas.length;
const ANSWERED = ${lang === 'en' ? '(n,t)=>n+" / "+t+" answered"' : '(n,t)=>"أُجيب عن "+n+" من "+t'};
let S = { name:"", answers:{}, evidence:{}, seed:0 };
try { const r = localStorage.getItem(KEY); if (r) S = Object.assign(S, JSON.parse(r)); } catch(e) {}
if (!S.seed) S.seed = (Math.floor(Math.random()*2147483647) || 1);
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch(e) {} };
save();
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
const gl = (s) => D.lang === "ar" ? esc(s).replace(/(\u2066?)[(]([A-Za-z0-9][^()\u0600-\u06FF]*)[)](\u2069?)/g, "<bdi>$1($2)$3</bdi>") : esc(s);
const link = (n) => '<a href="' + D.reader + (D.cfg.mode === 'l' ? '#l' + n.replace('.', '-') : '#/' + n) + '">' + T.lessonW + ' ' + n + '</a>';
function rng(a){ return function(){ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function order(i){ const r = rng(S.seed + i*7919), o = [0,1,2,3]; for (let k=3;k>0;k--){ const j = Math.floor(r()*(k+1)); [o[k],o[j]]=[o[j],o[k]]; } return o; }

/* theme */
(function(){ let th = null; try { th = localStorage.getItem(D.cfg.theme); } catch(e) {}
  if (th) document.documentElement.setAttribute("data-theme", th);
  $("#theme").addEventListener("click", () => { const cur = document.documentElement.getAttribute("data-theme") || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    const nx = cur === "dark" ? "light" : "dark"; document.documentElement.setAttribute("data-theme", nx); try { localStorage.setItem(D.cfg.theme, nx); } catch(e) {} }); })();

/* knowledge */
function renderK(){
  let h = "", i = 0;
  for (const a of D.areas) {
    h += '<h3 class="area-h"><span class="k">' + esc(a.key) + '</span>' + gl(a.name) + '</h3>';
    for (const q of D.qs.filter((x) => x.area === a.id)) {
      const qi = D.qs.indexOf(q); i++;
      h += '<div class="q" id="q-' + q.id + '"><span class="lv">' + i + ' · ' + esc(T.lvl[q.level]) + '</span><p class="stem">' + gl(q.q) + '</p>';
      for (const oi of order(qi)) {
        const on = S.answers[q.id] === oi;
        h += '<label class="' + (on ? 'sel' : '') + '"><input type="radio" name="' + q.id + '" value="' + oi + '"' + (on ? ' checked' : '') + '><span>' + gl(q.o[oi]) + '</span></label>';
      }
      h += '</div>';
    }
  }
  $("#klist").innerHTML = h;
  $("#klist").querySelectorAll("input").forEach((el) => el.addEventListener("change", () => {
    S.answers[el.name] = +el.value; save();
    el.closest(".q").querySelectorAll("label").forEach((l) => l.classList.toggle("sel", l.contains(el)));
    prog();
  }));
  prog();
}
function prog(){ $("#kprog").textContent = ANSWERED(Object.keys(S.answers).filter((k) => D.qs.some((q) => q.id === k)).length, D.qs.length); }

/* evidence */
function renderE(){
  let h = "";
  for (const a of D.areas) {
    h += '<h3 class="area-h"><span class="k">' + esc(a.key) + '</span>' + gl(a.name) + '</h3>';
    for (const e of D.ev.filter((x) => x.area === a.id))
      h += '<label><input type="checkbox" data-e="' + e.id + '"' + (S.evidence[e.id] ? ' checked' : '') + '><span>' + gl(e.text) + ' <span class="ln">(' + link(e.lesson) + ')</span></span></label>';
  }
  $("#elist").innerHTML = h;
  $("#elist").querySelectorAll("input").forEach((el) => el.addEventListener("change", () => { S.evidence[el.dataset.e] = el.checked; save(); }));
}

/* results */
function compute(){
  const areas = {}; let right = 0;
  for (const a of D.areas) {
    const qs = D.qs.filter((q) => q.area === a.id), ev = D.ev.filter((e) => e.area === a.id);
    const k = qs.filter((q) => S.answers[q.id] === q.a).length, e = ev.filter((x) => S.evidence[x.id]).length;
    right += k;
    areas[a.id] = { k, kt: qs.length, e, et: ev.length, status: k >= 3 ? (e === ev.length ? 2 : 1) : 0 };
  }
  const st = Object.values(areas), aware = st.filter((x) => x.status >= 1).length, pract = st.filter((x) => x.status === 2).length;
  const level = (aware === N && pract >= 10) ? 3 : (aware >= 10 && pract >= 5) ? 2 : aware >= 5 ? 1 : 0;
  return { areas, right, total: D.qs.length, aware, pract, level };
}
function renderR(){
  const any = Object.keys(S.answers).length;
  if (!any) { $("#rout").innerHTML = '<div class="card"><p class="sub">' + esc(T.rEmpty) + '</p></div>'; return; }
  const R = compute(), L = T.levels[R.level];
  let h = '<div class="card"><h2>' + esc(T.rH) + (S.name ? ' — ' + esc(S.name) : '') + '</h2>';
  h += '<div class="level"><b>' + gl(L[0]) + '</b>' + gl(L[1]) + '</div>';
  h += '<div class="kpis"><div><b>' + Math.round(100*R.right/R.total) + '%</b><span>' + esc(T.score) + ' (' + R.right + '/' + R.total + ')</span></div>'
     + '<div><b>' + R.aware + '/' + N + '</b><span>' + esc(T.areasAware) + '</span></div>'
     + '<div><b>' + R.pract + '/' + N + '</b><span>' + esc(T.areasPract) + '</span></div></div>';
  h += '<div class="tbl"><table><thead><tr><th>' + esc(T.colArea) + '</th><th>' + esc(T.colK) + '</th><th>' + esc(T.colE) + '</th><th>' + esc(T.colS) + '</th></tr></thead><tbody>';
  for (const a of D.areas) { const x = R.areas[a.id];
    h += '<tr><td><span class="k" style="font-family:var(--mono);color:var(--ember);font-size:.75rem">' + esc(a.key) + '</span> ' + gl(a.name) + '</td><td><span class="bar"><i style="width:' + (100*x.k/x.kt) + '%"></i></span>' + x.k + '/' + x.kt + '</td><td>' + x.e + '/' + x.et + '</td><td><span class="st st' + x.status + '">' + esc(T.status[x.status]) + '</span></td></tr>'; }
  h += '</tbody></table></div></div>';
  /* study next: missed questions' lessons, weakest areas first */
  const missed = D.qs.filter((q) => S.answers[q.id] !== q.a);
  const byArea = D.areas.map((a) => ({ a, x: R.areas[a.id], ls: [...new Set(missed.filter((q) => q.area === a.id).map((q) => q.lesson))] })).filter((z) => z.ls.length)
    .sort((p, q) => (p.x.status - q.x.status) || (p.x.k - q.x.k));
  h += '<div class="card"><h2>' + esc(T.nextH) + '</h2><p class="sub">' + esc(T.nextSub) + '</p>';
  h += byArea.length ? '<ul class="next">' + byArea.map((z) => '<li><b>' + gl(z.a.name) + '</b> — ' + z.ls.map(link).join(' · ') + '</li>').join('') + '</ul>' : '<p>' + esc(T.nextNone) + '</p>';
  h += '</div><div class="card"><h2>' + esc(T.reviewH) + '</h2>';
  D.qs.forEach((q, i) => { const ua = S.answers[q.id], ok = ua === q.a;
    h += '<details class="rev"><summary><span class="' + (ok ? 'ok' : 'no') + '">' + (ok ? '✓' : '✗') + '</span> ' + (i+1) + '. ' + gl(q.q) + '</summary>'
      + '<p>' + esc(T.yours) + ': ' + (ua === undefined ? '<i>' + esc(T.noAns) + '</i>' : gl(q.o[ua])) + '<br>' + esc(T.right) + ': <b>' + gl(q.o[q.a]) + '</b></p><p>' + gl(q.why) + ' (' + link(q.lesson) + ')</p></details>'; });
  h += '</div><div class="card noprint"><h2>' + esc(T.saveH) + '</h2><p class="sub">' + esc(T.saveSub) + '</p>'
     + '<button type="button" class="ghost" id="exp">' + esc(T.exportB) + '</button><button type="button" class="ghost" onclick="print()">' + esc(T.printB) + '</button><button type="button" class="ghost" id="rst">' + esc(T.resetB) + '</button></div>';
  $("#rout").innerHTML = h;
  $("#exp").addEventListener("click", exportJSON);
  $("#rst").addEventListener("click", () => { if (confirm(T.resetQ)) { S = { name:"", answers:{}, evidence:{}, seed:(Math.floor(Math.random()*2147483647)||1) }; save(); $("#name").value=""; renderK(); renderE(); show("start"); } });
}
function exportJSON(){
  const R = compute();
  const out = { tool:TOOL, version:1, name:S.name || "", date:new Date().toISOString().slice(0,10), lang:D.lang,
    level:R.level, score:R.right, total:R.total, areas:Object.fromEntries(Object.entries(R.areas).map(([k,v]) => [k,{k:v.k,e:v.e,status:v.status}])) };
  const b = new Blob([JSON.stringify(out, null, 2)], { type:"application/json" }), u = URL.createObjectURL(b), a = document.createElement("a");
  a.href = u; a.download = TOOL + "-" + (S.name || "result").replace(/[^\\w\\u0600-\\u06FF-]+/g, "_") + ".json"; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(u), 1000);
}

/* group view */
const G = [];
function addG(o){ if (o && o.tool === TOOL && o.areas) { G.push(o); return true; } return false; }
function parseMany(txt){ txt = txt.trim(); if (!txt) return false; let ok = false;
  try { const v = JSON.parse(txt); (Array.isArray(v) ? v : [v]).forEach((o) => { ok = addG(o) || ok; }); return ok; } catch(e) {}
  for (const part of txt.split(/}\\s*(?={)/)) { try { ok = addG(JSON.parse(part.endsWith("}") ? part : part + "}")) || ok; } catch(e) {} } return ok; }
function renderG(){
  if (!G.length) { $("#gout").innerHTML = ""; return; }
  let h = '<div class="tbl" style="margin-top:1rem"><table><thead><tr><th>' + esc(T.gName) + '</th><th>' + esc(T.gLevel) + '</th><th>' + esc(T.gScore) + '</th>' + D.areas.map((a) => '<th title="' + esc(a.name) + '">' + esc(a.key) + '</th>').join('') + '</tr></thead><tbody>';
  for (const o of G) h += '<tr><td>' + esc(o.name || '—') + '</td><td>' + esc((T.levels[o.level] || ['?'])[0]) + '</td><td>' + o.score + '/' + o.total + '</td>' + D.areas.map((a) => { const s = (o.areas[a.id] || {}).status ?? 0; return '<td><span class="st st' + s + '">' + ['·','A','P'][s] + '</span></td>'; }).join('') + '</tr>';
  h += '<tr><th colspan="3">' + esc(T.gCover) + '</th>' + D.areas.map((a) => '<th>' + G.filter((o) => ((o.areas[a.id] || {}).status || 0) >= 1).length + '/' + G.length + '</th>').join('') + '</tr></tbody></table></div>';
  $("#gout").innerHTML = h;
}
$("#gfiles").addEventListener("change", async (ev) => { for (const f of ev.target.files) parseMany(await f.text()); renderG(); });
$("#gadd").addEventListener("click", () => { if (!parseMany($("#gpaste").value)) alert(T.gBad); else { $("#gpaste").value = ""; renderG(); } });

/* tabs */
function show(tab){
  document.querySelectorAll("section[id^=tab-]").forEach((s) => s.classList.toggle("hide", s.id !== "tab-" + tab));
  document.querySelectorAll(".tabs button").forEach((b) => b.classList.toggle("on", b.dataset.tab === tab));
  if (tab === "results") renderR();
  try { sessionStorage.setItem(TOOL + "-tab", tab); } catch(e) {}
  window.scrollTo(0, 0);
}
document.querySelectorAll("[data-tab]").forEach((b) => b.addEventListener("click", () => show(b.dataset.tab)));
document.querySelectorAll("[data-go]").forEach((b) => b.addEventListener("click", () => show(b.dataset.go)));
$("#name").value = S.name; $("#name").addEventListener("input", (e) => { S.name = e.target.value; save(); });
renderK(); renderE();
let start = "start"; try { start = sessionStorage.getItem(TOOL + "-tab") || (Object.keys(S.answers).length ? "knowledge" : "start"); } catch(e) {}
show(start);
</script>
</body>
</html>
`;
}

/* ---------------------------------------------------------------- write / check */

let bad = 0;
for (const C of COURSES) {
  if (ONLY && C.id !== ONLY) continue;
  if (!fs.existsSync(path.join(ROOT, C.src, 'areas.json'))) { console.log(`· ${C.id}: no assessment yet (${C.src}/areas.json missing) — skipped`); continue; }
  const L = load(C);
  if (L.problems.length) { console.error(`✗ ${C.id} assessment items:\n  ${L.problems.join('\n  ')}`); bad++; continue; }
  const OUT = { en: path.join(ROOT, C.out, 'assessment.html'), ar: path.join(ROOT, C.out, 'assessment.ar.html') };
  if (CHECK) {
    const stale = Object.values(OUT).filter((f) => !fs.existsSync(f) || !fs.readFileSync(f, 'utf8').includes(`content="${L.SRC}"`)).map((f) => path.relative(ROOT, f));
    if (stale.length) { console.error(`✗ Stale assessment pages: ${stale.join(', ')}\n  Run \`npm run assess:build\` and commit the result.`); bad++; }
    else console.log(`✓ ${C.id} assessment matches its sources (${L.SRC}).`);
  } else {
    for (const [lang, f] of Object.entries(OUT)) fs.writeFileSync(f, page(C, L, lang));
    console.log(`✓ ${C.id}: ${L.na} ${C.unit.ens}, ${L.nq} questions, ${L.ne} evidence items → ${Object.values(OUT).map((f) => path.relative(ROOT, f)).join(', ')} (${L.SRC})`);
  }
}
if (bad) process.exit(1);
