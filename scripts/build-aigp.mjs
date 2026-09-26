#!/usr/bin/env node
/**
 * Build the "AI Governance: Zero to Hero" course (aligned to the IAPP AIGP Body of Knowledge v2.1).
 *
 *   node scripts/build-aigp.mjs           → for each language (en, ar):
 *                                           aigp/index[.ar].html        (interactive reader)
 *                                           aigp/course[.ar].html       (the whole course, one flat page)
 *                                           aigp/COURSE[.ar].md         (the whole course, one markdown file)
 *                                           aigp/INSTRUMENTS[.ar].md    (laws, standards and frameworks catalogue)
 *   node scripts/build-aigp.mjs --check   → fail if the committed outputs are stale
 *   node scripts/build-aigp.mjs --lang=en → build one language only (drafting)
 *
 * Adapted from build-saas.mjs: same module/lesson format and reader, plus a BoK competency tag on
 * every lesson ("*Level: …* · *Prerequisites: …* · *BoK: II.C*"), and the "⚖️ The instruments"
 * tables in place of the repo tables. The first cell of each instruments row starts with the
 * instrument's name in bold; those names build the catalogue and must match across languages.
 *
 * Sources: aigp/README.md, aigp/modules/NN-*.md and their .ar.md mirrors. The markdown is the source
 * of truth; everything else in aigp/ is generated — never edit it by hand.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import puppeteer from 'puppeteer';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const COURSE_DIR = path.join(ROOT, 'aigp');
const MODULE_DIR = path.join(COURSE_DIR, 'modules');
const CHECK = process.argv.includes('--check');
const ONLY = (process.argv.find((a) => a.startsWith('--lang=')) || '').slice(7) || null;
const LANGS = ONLY ? [ONLY] : ['en', 'ar'];

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const slug = (num) => 'l' + num.replace('.', '-');
const sfx = (lang, ext) => (lang === 'en' ? '' : `.${lang}`) + ext;
const OUT = (lang) => ({
  html: path.join(COURSE_DIR, `index${sfx(lang, '.html')}`),
  course: path.join(COURSE_DIR, `course${sfx(lang, '.html')}`),
  courseMd: path.join(COURSE_DIR, `COURSE${sfx(lang, '.md')}`),
  repos: path.join(COURSE_DIR, `INSTRUMENTS${sfx(lang, '.md')}`),
});

/* ------------------------------------------------------------------ strings */

const LEVEL_KEYS = { Beginner: 'b', Intermediate: 'i', Advanced: 'a' };
const T = {
  en: {
    dir: 'ltr', other: 'ar', otherLabel: 'عربي', otherTitle: 'اقرأ بالعربية',
    readme: 'README.md',
    module: 'Module', levels: { Beginner: '🟢 Beginner', Intermediate: '🟡 Intermediate', Advanced: '🔴 Advanced' },
    levelWord: 'Level', prereqWord: 'Prerequisites', bokWord: 'BoK', before: 'Before this', comma: ', ',
    prev: '← Previous', next: 'Next →', appendixNext: 'Appendix →', catalog: 'The instruments catalogue',
    nav: { map: 'Map', about: 'Start here', repos: 'Instruments', one: 'One page', oneTitle: 'The whole course on one printable page', contents: 'Contents', reader: 'Reader' },
    eyebrow: 'AI governance · zero to hero · aligned to the IAPP AIGP Body of Knowledge v2.1',
    h1: 'Govern AI <em>before</em> it governs you.',
    lede: 'What AI is and why it needs governance; the laws, standards and frameworks that apply — GDPR, the EU AI Act, NIST AI RMF, ISO/IEC 42001 and more; and how to govern AI from the first idea to retirement. Built around one bank, with an exam-style quiz in every lesson and a 100-question mock exam.',
    stats: ['modules', 'lessons', 'laws & frameworks', 'practice questions'],
    start: 'Start with lesson 0.1 →', how: 'How the course works',
    tracks: {
      b: ['🟢 Foundations', 'Zero: what AI is, the risks it brings, and what an AI governance professional does.'],
      i: ['🟡 Practitioner', 'Build the programme and apply the law: policies, privacy, non-discrimination, the EU AI Act, NIST and ISO.'],
      a: ['🔴 Hero', 'Govern real systems end to end: design, data, testing, release, deployment, assessments — and pass the AIGP.'],
    },
    lessonsN: (n) => `${n} lesson${n === 1 ? '' : 's'}`,
    mapTitle: 'Course map',
    mapLede: 'Every lesson climbs the same ladder — 🟢 essentials → 🟡 going deeper → 🔴 expert view. The dot shows where each lesson <em>starts</em>; the tag shows its AIGP competency.',
    all: 'All', filterLabel: 'Filter by level',
    startHere: 'Start here',
    catLede: 'Every law, standard and framework the course teaches, with what it requires and the cue the exam tends to test. Instruments change — check the official source before relying on any of them.',
    catCols: ['Instrument', 'What it requires or recommends', 'Exam cue'],
    filterPh: (n) => `Filter ${n} instruments — try &quot;GDPR&quot;, &quot;deployer&quot;, &quot;ISO&quot;…`,
    footer: 'Part of the <a href="../">Course Library</a>. An independent course, not affiliated with or endorsed by the IAPP. Not legal advice. Generated from the markdown in <code>aigp/</code> by <code>npm run aigp:build</code>. Source: <a href="https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/aigp">github.com/Tamoura/system-design-for-vibe-coders</a>',
    flatEyebrow: 'The complete course · one page · print-friendly',
    flatH1: 'AI Governance: Zero to Hero — govern AI <em>before</em> it governs you.',
    backContents: '↑ Contents', appendixCatalog: 'Appendix — The instruments catalogue',
    flatFooter: 'Generated from the markdown in <code>aigp/</code> by <code>npm run aigp:build</code>. An independent course, not affiliated with or endorsed by the IAPP. Prefer one lesson at a time? Open the <a href="index.html">interactive reader</a>.',
    title: 'AI Governance: Zero to Hero', courseTitle: 'AI Governance: Zero to Hero — Complete Course',
    description: 'AI Governance: Zero to Hero — a free, bilingual course aligned to the IAPP AIGP Body of Knowledge v2.1: foundations, law, standards, and governing AI development and deployment, with exam-style questions and a 100-question mock exam.',
    md: {
      title: 'AI Governance: Zero to Hero — the complete course',
      sub: (m, l, r) => `*${m} modules · ${l} lessons · ${r} laws, standards and frameworks · aligned to the AIGP Body of Knowledge v2.1 · zero → hero*`,
      contents: 'Contents', appendix: 'Appendix — The instruments catalogue',
      catTitle: 'The Instruments Catalogue',
      catIntro: (n) => [`Every law, standard and framework taught in **AI Governance: Zero to Hero** — ${n} of them — grouped by`,
        'the lesson that teaches it, with what it requires and the exam cue. Instruments change: check the official source',
        'before relying on any of them. This is not legal advice.'],
      az: 'A–Z index',
    },
  },
  ar: {
    dir: 'rtl', other: 'en', otherLabel: 'English', otherTitle: 'Read in English',
    readme: 'README.ar.md',
    module: 'الوحدة', levels: { Beginner: '🟢 مبتدئ', Intermediate: '🟡 متوسط', Advanced: '🔴 متقدم' },
    levelWord: 'المستوى', prereqWord: 'المتطلبات', bokWord: 'مجال المعرفة (BoK)', before: 'اقرأ قبله', comma: '، ',
    prev: '→ السابق', next: 'التالي ←', appendixNext: 'الملحق ←', catalog: 'دليل الأدوات التنظيمية',
    nav: { map: 'الخريطة', about: 'ابدأ هنا', repos: 'الأدوات التنظيمية', one: 'صفحة واحدة', oneTitle: 'الدورة كاملة في صفحة واحدة قابلة للطباعة', contents: 'المحتويات', reader: 'القارئ' },
    eyebrow: 'حوكمة الذكاء الاصطناعي · من الصفر إلى الاحتراف · متوافقة مع مجال المعرفة لشهادة AIGP من IAPP (الإصدار 2.1)',
    h1: 'احكم الذكاء الاصطناعي <em>قبل</em> أن يحكمك.',
    lede: 'ما الذكاء الاصطناعي ولماذا يحتاج إلى حوكمة؛ والقوانين والمعايير والأطر التي تنطبق عليه، مثل GDPR وقانون الذكاء الاصطناعي الأوروبي (EU AI Act) وإطار NIST AI RMF ومعيار ISO/IEC 42001؛ وكيف تحكم الذكاء الاصطناعي من الفكرة الأولى حتى الإيقاف. مبنية حول بنك واحد، مع اختبار بأسلوب الامتحان في كل درس، وامتحان تجريبي من 100 سؤال.',
    stats: ['وحدات', 'درسًا', 'قانونًا ومعيارًا وإطارًا', 'سؤالًا تدريبيًا'],
    start: 'ابدأ بالدرس 0.1 ←', how: 'كيف تعمل الدورة',
    tracks: {
      b: ['🟢 الأساسيات', 'البداية: ما الذكاء الاصطناعي، وما المخاطر التي يجلبها، وماذا يفعل مختص حوكمة الذكاء الاصطناعي.'],
      i: ['🟡 الممارس', 'ابنِ البرنامج وطبّق القانون: السياسات، والخصوصية، وعدم التمييز، وقانون الذكاء الاصطناعي الأوروبي، وNIST وISO.'],
      a: ['🔴 المحترف', 'احكم أنظمة حقيقية من البداية إلى النهاية: التصميم، والبيانات، والاختبار، والإطلاق، والنشر، والتقييمات، واجتز امتحان AIGP.'],
    },
    lessonsN: (n) => `${n} ${n === 1 ? 'درس' : n <= 10 ? 'دروس' : 'درسًا'}`,
    mapTitle: 'خريطة الدورة',
    mapLede: 'كل درس يصعد السلّم نفسه: 🟢 الأساسيات ← 🟡 التعمق أكثر ← 🔴 نظرة الخبير. تشير النقطة إلى المستوى الذي <em>يبدأ</em> منه الدرس، ويشير الوسم إلى كفاءة AIGP التي يغطيها.',
    all: 'الكل', filterLabel: 'التصفية حسب المستوى',
    startHere: 'ابدأ هنا',
    catLede: 'كل قانون ومعيار وإطار تدرّسه الدورة، مع ما يشترطه والإشارة التي يختبرها الامتحان عادة. هذه الأدوات تتغير، فراجع المصدر الرسمي قبل الاعتماد على أيٍّ منها.',
    catCols: ['الأداة', 'ما تشترطه أو توصي به', 'إشارة الامتحان'],
    filterPh: (n) => `صفِّ ${n} أداة — جرّب &quot;GDPR&quot; أو &quot;deployer&quot; أو &quot;ISO&quot;…`,
    footer: 'جزء من <a href="../">مكتبة الدورات</a>. دورة مستقلة غير تابعة لـ IAPP ولا معتمدة منها، وليست استشارة قانونية. مولَّدة من ملفات الماركداون في <code>aigp/</code> عبر <code>npm run aigp:build</code>. المصدر: <a href="https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/aigp">github.com/Tamoura/system-design-for-vibe-coders</a>',
    flatEyebrow: 'الدورة كاملة · صفحة واحدة · مناسبة للطباعة',
    flatH1: 'حوكمة الذكاء الاصطناعي من الصفر إلى الاحتراف: احكم الذكاء الاصطناعي <em>قبل</em> أن يحكمك.',
    backContents: '↑ المحتويات', appendixCatalog: 'الملحق — دليل الأدوات التنظيمية',
    flatFooter: 'مولَّدة من ملفات الماركداون في <code>aigp/</code> عبر <code>npm run aigp:build</code>. دورة مستقلة غير تابعة لـ IAPP. تفضّل درسًا واحدًا في كل مرة؟ افتح <a href="index.ar.html">القارئ التفاعلي</a>.',
    title: 'حوكمة الذكاء الاصطناعي — من الصفر إلى الاحتراف', courseTitle: 'حوكمة الذكاء الاصطناعي من الصفر إلى الاحتراف — الدورة كاملة',
    description: 'حوكمة الذكاء الاصطناعي من الصفر إلى الاحتراف: دورة مجانية ثنائية اللغة متوافقة مع مجال المعرفة لشهادة AIGP (الإصدار 2.1)، مع أسئلة بأسلوب الامتحان وامتحان تجريبي من 100 سؤال.',
    md: {
      title: 'حوكمة الذكاء الاصطناعي من الصفر إلى الاحتراف — الدورة كاملة',
      sub: (m, l, r) => `*${m} وحدة · ${l} درسًا · ${r} قانونًا ومعيارًا وإطارًا · متوافقة مع مجال المعرفة لشهادة AIGP (الإصدار 2.1) · من الصفر إلى الاحتراف*`,
      contents: 'المحتويات', appendix: 'الملحق — دليل الأدوات التنظيمية',
      catTitle: 'دليل الأدوات التنظيمية',
      catIntro: (n) => [`كل قانون ومعيار وإطار تدرّسه دورة **حوكمة الذكاء الاصطناعي من الصفر إلى الاحتراف**، وعددها ${n}، مجمّعة حسب الدرس الذي يدرّسها،`,
        'مع ما تشترطه وإشارة الامتحان. هذه الأدوات تتغير، فراجع المصدر الرسمي قبل الاعتماد عليها. هذه ليست استشارة قانونية.'],
      az: 'فهرس أبجدي',
    },
  },
};

/* ------------------------------------------------------------------ sources */

const enFiles = fs.readdirSync(MODULE_DIR).filter((f) => /^\d\d-.+\.md$/.test(f) && !f.endsWith('.ar.md')).sort();
const filesFor = (lang) => (lang === 'en' ? enFiles : enFiles.map((f) => f.replace(/\.md$/, `.${lang}.md`)));
const SOURCE_FILES = [
  ...LANGS.flatMap((lang) => [`aigp/${T[lang].readme}`, ...filesFor(lang).map((f) => `aigp/modules/${f}`)]),
  'scripts/build-aigp.mjs',
  'scripts/saas.css',
];
for (const f of SOURCE_FILES) {
  if (!fs.existsSync(path.join(ROOT, f))) {
    console.error(`✗ Missing source: ${f}\n  Every module and README needs its Arabic mirror (NN-slug.ar.md, README.ar.md). Use --lang=en while drafting.`);
    process.exit(1);
  }
}
const SOURCE_DIGEST = (() => {
  const h = crypto.createHash('sha256');
  for (const f of SOURCE_FILES) {
    h.update(f + '\0');
    h.update(fs.readFileSync(path.join(ROOT, f)));
  }
  return h.digest('hex').slice(0, 16);
})();

if (CHECK) {
  const stale = [];
  for (const lang of LANGS) {
    for (const f of Object.values(OUT(lang))) {
      const txt = fs.existsSync(f) ? fs.readFileSync(f, 'utf8') : '';
      if (!txt.includes(`aigp-source: ${SOURCE_DIGEST}`) && !txt.includes(`aigp-source" content="${SOURCE_DIGEST}"`)) {
        stale.push(path.relative(ROOT, f));
      }
    }
  }
  if (stale.length) {
    console.error(`✗ Stale AIGP course output: ${stale.join(', ')}\n  Run \`npm run aigp:build\` and commit the result.`);
    process.exit(1);
  }
  console.log(`✓ AIGP course output matches its sources (${SOURCE_DIGEST}).`);
  process.exit(0);
}

/* ------------------------------------------------------------------- parse */

const MODULE_RE = /^# (?:Module|الوحدة) (\d+) — (.+)$/m;
const LESSON_RE = /^# (\d+\.\d+) — (.+)$/;
const LEVEL_RE = /^\*(?:Level|المستوى):\s*(🟢|🟡|🔴)\s*(Beginner|Intermediate|Advanced|مبتدئ|متوسط|متقدم)\*(.*)$/;
const LEVEL_NORM = { 'مبتدئ': 'Beginner', 'متوسط': 'Intermediate', 'متقدم': 'Advanced' };

function parseModule(file) {
  const md = fs.readFileSync(path.join(MODULE_DIR, file), 'utf8').replace(/\r\n/g, '\n');
  const m = md.match(MODULE_RE);
  if (!m) throw new Error(`${file}: first heading must be "# Module N — Title" / "# الوحدة N — العنوان"`);
  const lessons = [];
  let intro = [];
  let cur = null;
  let seenModule = false;
  for (const line of md.split('\n')) {
    const lm = line.match(LESSON_RE);
    if (lm) {
      cur = { num: lm[1], title: lm[2].trim(), body: [], level: null, prereq: '', bok: '' };
      lessons.push(cur);
      continue;
    }
    if (!seenModule && MODULE_RE.test(line)) { seenModule = true; continue; }
    if (cur) {
      if (!cur.level && !cur.body.some((l) => l.trim())) {
        const lv = line.trim().match(LEVEL_RE);
        if (lv) {
          cur.level = LEVEL_NORM[lv[2]] || lv[2];
          const pre = lv[3].match(/(?:Prerequisites?|المتطلبات):\s*([^*]+)\*/);
          cur.prereq = pre ? pre[1].trim() : '';
          const bok = lv[3].match(/(?:BoK|مجال المعرفة)[^:]*:\s*([^*]+)\*/);
          cur.bok = bok ? bok[1].trim() : '';
          continue;
        }
      }
      cur.body.push(line);
    } else {
      intro.push(line);
    }
  }
  if (!lessons.length) throw new Error(`${file}: no lessons found ("# N.M — Title")`);
  for (const l of lessons) {
    if (!l.level) throw new Error(`${file}: lesson ${l.num} is missing its level line`);
    l.body = l.body.join('\n').replace(/\n\s*---\s*$/g, '').trim();
  }
  intro = intro.join('\n').replace(/^\s*---\s*$/gm, '').trim();
  return { key: m[1], title: m[2].trim(), intro, lessons, file };
}

/* ----------------------------------------------------------------- markdown */

const diagrams = [];
marked.use({
  gfm: true,
  renderer: {
    code({ text, lang }) {
      if ((lang || '').trim() === 'mermaid') {
        diagrams.push(text);
        return `<div class="diagram" dir="ltr"><!--DIAGRAM:${diagrams.length - 1}--></div>`;
      }
      return false;
    },
  },
});

const SECTION_CLASS = {
  '⚡': 'tldr', '🧭': 'why', '📐': 'how', '⚖': 'repos', '🏛': 'wild', '🛠': 'build',
  '⚠': 'mistakes', '🧾': 'recap', '✍': 'quiz', '📚': 'refs',
};

const AIGP_CSS = `
.bok{font:600 .78rem/1 ui-monospace,SFMono-Regular,Menlo,monospace;padding:.2rem .45rem;border-radius:6px;border:1px solid currentColor;opacity:.8;unicode-bidi:isolate}
`;
const tableWrap = (html) => html.replace(/<table>/g, '<div class="table-scroll"><table>').replace(/<\/table>/g, '</table></div>');
const count = (s, re) => (s.match(re) || []).length;

/* ------------------------------------------------------------- per language */

function buildLang(lang) {
  const t = T[lang];
  const MODULES = filesFor(lang).map(parseModule);
  const ALL_LESSONS = MODULES.flatMap((mod) => mod.lessons.map((l) => ({ ...l, mod })));
  const LESSON_NUMS = new Set(ALL_LESSONS.map((l) => l.num));
  const lvlLabel = (l) => t.levels[l];

  /* repo catalog */
  const NAME_RE = /^\*\*([^*]+)\*\*/; // first cell of an instruments row: **Name** — Art. X
  const repoRows = (lesson) => {
    const sec = lesson.body.split(/\n(?=## )/).find((s) => s.startsWith('## ⚖'));
    if (!sec) return [];
    const rows = [];
    for (const line of sec.split('\n')) {
      if (!line.startsWith('|')) continue;
      const cells = line.split('|').slice(1, -1).map((c) => c.trim());
      const nm = cells[0] && cells[0].match(NAME_RE);
      if (nm) rows.push({ repo: nm[1].trim(), cells });
    }
    return rows;
  };
  const CATALOG = ALL_LESSONS.map((l) => ({ lesson: l, rows: repoRows(l) })).filter((c) => c.rows.length);
  const REPO_INDEX = new Map();
  for (const { lesson, rows } of CATALOG) {
    for (const r of rows) {
      const k = r.repo.toLowerCase();
      if (!REPO_INDEX.has(k)) REPO_INDEX.set(k, { repo: r.repo, lessons: [] });
      const e = REPO_INDEX.get(k);
      if (!e.lessons.includes(lesson.num)) e.lessons.push(lesson.num);
    }
  }

  function reposMarkdown() {
    const out = [];
    out.push('<!-- Generated by scripts/build-aigp.mjs from the lessons\' "⚖️" tables. Do not edit by hand. -->');
    out.push(`<!-- aigp-source: ${SOURCE_DIGEST} -->`);
    out.push('');
    out.push(`# ${t.md.catTitle}`);
    out.push('');
    out.push(...t.md.catIntro(REPO_INDEX.size));
    out.push('');
    for (const mod of MODULES) {
      const entries = CATALOG.filter((c) => c.lesson.mod === mod);
      if (!entries.length) continue;
      out.push(`## ${t.module} ${mod.key} — ${mod.title}`);
      out.push('');
      for (const { lesson, rows } of entries) {
        out.push(`### ${lesson.num} — ${lesson.title}`);
        out.push('');
        out.push(`| ${t.catCols.join(' | ')} |`);
        out.push('|---|---|---|');
        for (const r of rows) out.push(`| ${r.cells.join(' | ')} |`);
        out.push('');
      }
    }
    out.push(`## ${t.md.az}`);
    out.push('');
    const sorted = [...REPO_INDEX.values()].sort((a, b) => a.repo.toLowerCase().localeCompare(b.repo.toLowerCase()));
    for (const e of sorted) out.push(`- **${e.repo}** — ${e.lessons.join(', ')}`);
    out.push('');
    return out.join('\n');
  }

  /* whole-course markdown */
  const shiftHeadings = (md, by) => {
    let fence = false;
    return md.split('\n').map((line) => {
      if (/^```/.test(line)) fence = !fence;
      if (fence || !/^#{1,5} /.test(line)) return line;
      return '#'.repeat(by) + line;
    }).join('\n');
  };
  const MD_LINKS = (md) => md
    .replace(/\]\(\.\.?\/(?:REPOS|INSTRUMENTS)(?:\.ar)?\.md\)/g, '](#appendix-the-repo-catalog)')
    .replace(/\]\(\.\.?\/(?:OUTLINE|README)(?:\.ar)?\.md(?:#[\w-]+)?\)/g, '](#contents)');

  function courseMarkdown() {
    const out = [];
    const readme = fs.readFileSync(path.join(COURSE_DIR, t.readme), 'utf8').replace(/^# .+\n/, '');
    out.push(`<!-- Generated by scripts/build-aigp.mjs from aigp/${t.readme} and aigp/modules/*${sfx(lang, '.md')}. Do not edit by hand. -->`);
    out.push(`<!-- aigp-source: ${SOURCE_DIGEST} -->`);
    out.push('');
    if (lang !== 'en') { out.push('<div dir="rtl">'); out.push(''); }
    out.push(`# ${t.md.title}`);
    out.push('');
    out.push(t.md.sub(MODULES.length, ALL_LESSONS.length, REPO_INDEX.size));
    out.push('');
    out.push(MD_LINKS(readme.trim()));
    out.push('');
    out.push('<a id="contents"></a>');
    out.push('');
    out.push(`## ${t.md.contents}`);
    out.push('');
    for (const mod of MODULES) {
      out.push(`- **[${t.module} ${mod.key} — ${mod.title}](#m${mod.key})**`);
      for (const l of mod.lessons) out.push(`  - [${l.num} — ${l.title}](#${slug(l.num)}) · ${lvlLabel(l.level)}`);
    }
    out.push(`- **[${t.md.appendix}](#appendix-the-repo-catalog)**`);
    out.push('');
    for (const mod of MODULES) {
      out.push('---');
      out.push('');
      out.push(`<a id="m${mod.key}"></a>`);
      out.push('');
      out.push(`# ${t.module} ${mod.key} — ${mod.title}`);
      out.push('');
      if (mod.intro) { out.push(MD_LINKS(mod.intro)); out.push(''); }
      for (const l of mod.lessons) {
        out.push(`<a id="${slug(l.num)}"></a>`);
        out.push('');
        out.push(`## ${l.num} — ${l.title}`);
        out.push('');
        out.push(`*${t.levelWord}: ${lvlLabel(l.level)}*${l.prereq ? ` · *${t.prereqWord}: ${l.prereq}*` : ''}${l.bok ? ` · *${t.bokWord}: ${l.bok}*` : ''}`);
        out.push('');
        out.push(MD_LINKS(shiftHeadings(l.body, 1)));
        out.push('');
      }
    }
    out.push('---');
    out.push('');
    out.push('<a id="appendix-the-repo-catalog"></a>');
    out.push('');
    out.push(`# ${t.md.appendix}`);
    out.push('');
    const catalog = reposMarkdown().split('\n').filter((l) => !l.startsWith('<!--')).join('\n')
      .replace(new RegExp(`^# ${t.md.catTitle}\\n`, 'm'), '');
    out.push(catalog.trim());
    out.push('');
    if (lang !== 'en') { out.push('</div>'); out.push(''); }
    return out.join('\n');
  }

  /* html pieces */
  const XREF_RE = /(\(|\b[Ll]essons? |\b[Ss]ee |الدرس |الدرسين |الدروس |انظر |راجع )(\d+\.\d+)(?![\d.]*\d)/g;
  function linkLessons(html) {
    let skip = 0; // depth inside <a>, <code>, <pre>, <svg>, headings
    return html.split(/(<[^>]+>)/).map((part) => {
      const tag = part.match(/^<(\/?)(a|code|pre|svg|h[1-6])\b/i);
      if (tag) { skip += tag[1] ? -1 : 1; return part; }
      if (part.startsWith('<') || skip > 0) return part;
      return part.replace(XREF_RE, (m, pre, n) => (LESSON_NUMS.has(n) ? `${pre}<a class="xref" href="#/${n}">${n}</a>` : m));
    }).join('');
  }

  function renderLesson(l) {
    return l.body.split(/\n(?=## )/).map((p) => {
      const h = p.match(/^## (\S+)/);
      const key = h ? h[1].replace(/️/g, '') : '';
      const cls = h ? (SECTION_CLASS[key] || 'plain') : 'lead';
      const md = p.replace(/\]\(\.\.\/(?:REPOS|INSTRUMENTS)(?:\.ar)?\.md\)/g, '](#/repos)').replace(/\]\(\.\.\/(?:OUTLINE|README)(?:\.ar)?\.md\)/g, '](#/map)');
      return `<section class="sec sec-${cls}">${linkLessons(tableWrap(marked.parse(md)))}</section>`;
    }).join('\n');
  }

  const prereqLinks = (l) => l.prereq.split(/\s*[,،]\s*/).map((n) => (LESSON_NUMS.has(n) ? `<a href="#/${n}">${n}</a>` : esc(n))).join(t.comma);
  function lessonInner(l) {
    const prereq = l.prereq ? ` · <span class="prereq">${t.before}: ${prereqLinks(l)}</span>` : '';
    return `<p class="crumb"><a href="#/map">${t.module} ${esc(l.mod.key)} — ${esc(l.mod.title)}</a></p>
<h1><span class="num">${esc(l.num)}</span> ${esc(l.title)}</h1>
<p class="meta"><span class="lvl lvl-${LEVEL_KEYS[l.level]}">${lvlLabel(l.level)}</span>${l.bok ? ` · <span class="bok" dir="ltr">${t.bokWord} ${esc(l.bok)}</span>` : ''}${prereq}</p>
${l.html}`;
  }

  function lessonTemplate(l, i) {
    const prev = ALL_LESSONS[i - 1];
    const next = ALL_LESSONS[i + 1];
    const nav = `<nav class="pager">
  ${prev ? `<a href="#/${prev.num}" class="prev"><span>${t.prev}</span>${esc(prev.num)} ${esc(prev.title)}</a>` : '<span></span>'}
  ${next ? `<a href="#/${next.num}" class="next"><span>${t.next}</span>${esc(next.num)} ${esc(next.title)}</a>` : `<a href="#/repos" class="next"><span>${t.appendixNext}</span>${t.catalog}</a>`}
</nav>`;
    return `<template id="t-${slug(l.num)}"><article class="lesson" data-level="${LEVEL_KEYS[l.level]}">
${lessonInner(l)}
${nav}
</article></template>`;
  }

  const mapHtml = () => MODULES.map((mod) => `<section class="mod" id="m${esc(mod.key)}">
  <div class="mod-head"><span class="mod-num">${esc(mod.key)}</span><h3>${esc(mod.title)}</h3></div>
  ${mod.intro ? `<div class="mod-intro">${marked.parse(mod.intro)}</div>` : ''}
  <ol class="lessons">
    ${mod.lessons.map((l) => `<li data-level="${LEVEL_KEYS[l.level]}"><a href="#/${l.num}"><span class="num">${esc(l.num)}</span><span class="t">${esc(l.title)}</span><span class="dot lvl-${LEVEL_KEYS[l.level]}" title="${esc(lvlLabel(l.level))}"></span></a></li>`).join('\n    ')}
  </ol>
</section>`).join('\n');

  function catalogHtml() {
    const blocks = CATALOG.map(({ lesson, rows }) => `<section class="cat" data-level="${LEVEL_KEYS[lesson.level]}">
<h3><a href="#/${lesson.num}">${esc(lesson.num)} — ${esc(lesson.title)}</a></h3>
<div class="table-scroll"><table><thead><tr>${t.catCols.map((c) => `<th>${c}</th>`).join('')}</tr></thead><tbody>
${rows.map((r) => `<tr data-q="${esc(r.cells.join(' ').toLowerCase())}">${r.cells.map((c) => `<td>${marked.parseInline(c)}</td>`).join('')}</tr>`).join('\n')}
</tbody></table></div></section>`).join('\n');
    return `<div class="cat-tools"><input id="repoFilter" type="search" placeholder="${t.filterPh(REPO_INDEX.size)}" aria-label="${t.nav.repos}"></div>\n${blocks}`;
  }

  function readmeHtml() {
    const md = fs.readFileSync(path.join(COURSE_DIR, t.readme), 'utf8')
      .replace(/^# .+\n/, '')
      .replace(/\]\(\.\/OUTLINE(?:\.ar)?\.md\)/g, '](#/map)')
      .replace(/\]\(\.\/(?:REPOS|INSTRUMENTS)(?:\.ar)?\.md\)/g, '](#/repos)');
    return linkLessons(tableWrap(marked.parse(md)));
  }

  const langLink = (target) => `<a class="lang" href="${target}" hreflang="${t.other}" lang="${t.other}" title="${t.otherTitle}" data-keep-hash>${t.otherLabel}</a>`;
  const themeScript = `var root=document.documentElement;
  try{var t=localStorage.getItem('aigp-theme'); if(t) root.setAttribute('data-theme',t);}catch(e){}
  document.getElementById('themeBtn').addEventListener('click',function(){
    var dark=root.getAttribute('data-theme')==='dark'||(!root.getAttribute('data-theme')&&matchMedia('(prefers-color-scheme: dark)').matches);
    var next=dark?'light':'dark'; root.setAttribute('data-theme',next);
    try{localStorage.setItem('aigp-theme',next);}catch(e){}
  });
  document.querySelectorAll('[data-keep-hash]').forEach(function(a){a.addEventListener('click',function(){a.href=a.getAttribute('href').split('#')[0]+location.hash;});});
  try{localStorage.setItem('aigp-lang','${lang}');}catch(e){}`;
  const css = fs.readFileSync(path.join(ROOT, 'scripts/saas.css'), 'utf8');
  const head = (title, desc, extraCss = '') => `<!doctype html>
<html lang="${lang}" dir="${t.dir}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="aigp-source" content="${SOURCE_DIGEST}">
<meta name="description" content="${esc(desc)}">
<title>${esc(title)}</title>
<style>
${css}${extraCss}
</style>
</head>`;
  const n = (k) => ALL_LESSONS.filter((l) => l.level === k).length;

  function page(fill) {
    return `${head(t.title, t.description, AIGP_CSS)}
<body>
<header class="top"><div class="bar">
  <a class="brand" href="#/">AI Governance <b>Zero to Hero</b></a>
  <nav>
    <a href="#/map">${t.nav.map}</a>
    <a href="#/about">${t.nav.about}</a>
    <a href="#/repos">${t.nav.repos}</a>
    <a href="course${sfx(lang, '.html')}" title="${t.nav.oneTitle}">${t.nav.one}</a>
    ${langLink(`index${sfx(t.other, '.html')}`)}
    <button id="themeBtn" type="button" aria-label="Toggle dark mode">◐</button>
  </nav>
</div></header>

<main id="view" tabindex="-1"></main>

<template id="t-home">
<section class="hero">
  <p class="eyebrow">${t.eyebrow}</p>
  <h1>${t.h1}</h1>
  <p class="lede">${t.lede}</p>
  <div class="stats">
    <div><b>${MODULES.length}</b>${t.stats[0]}</div>
    <div><b>${ALL_LESSONS.length}</b>${t.stats[1]}</div>
    <div><b>${REPO_INDEX.size}</b>${t.stats[2]}</div>
    <div><b>${ALL_LESSONS.reduce((s, l) => s + count(l.body, /<details>/g), 0)}</b>${t.stats[3]}</div>
  </div>
  <div class="cta"><a class="btn" href="#/0.1">${t.start}</a><a class="btn ghost" href="#/about">${t.how}</a></div>
</section>
<section class="tracks">
${['b', 'i', 'a'].map((k) => `  <a href="#/map" data-track="${k}" class="track t-${k}"><span class="lvl lvl-${k}">${t.tracks[k][0]}</span><b>${t.lessonsN(n({ b: 'Beginner', i: 'Intermediate', a: 'Advanced' }[k]))}</b><span>${t.tracks[k][1]}</span></a>`).join('\n')}
</section>
<section class="home-map"><h2>${t.mapTitle}</h2>${mapHtml()}</section>
</template>

<template id="t-map">
<section class="page">
  <h1>${t.mapTitle}</h1>
  <p class="lede">${t.mapLede}</p>
  <div class="filters" role="group" aria-label="${t.filterLabel}">
    <button data-f="all" class="on">${t.all}</button><button data-f="b">${t.levels.Beginner}</button><button data-f="i">${t.levels.Intermediate}</button><button data-f="a">${t.levels.Advanced}</button>
  </div>
  ${mapHtml()}
</section>
</template>

<template id="t-about"><section class="page prose">
<h1>${t.startHere}</h1>
${readmeHtml()}
</section></template>

<template id="t-repos"><section class="page">
<h1>${t.catalog}</h1>
<p class="lede">${t.catLede}</p>
${catalogHtml()}
</section></template>

${fill(ALL_LESSONS.map(lessonTemplate).join('\n'))}

<footer><p>${t.footer}</p></footer>

<script>
(function(){
  ${themeScript}
  var view=document.getElementById('view');
  var filter='all';
  function applyFilter(){
    view.querySelectorAll('.filters button').forEach(function(b){b.classList.toggle('on',b.dataset.f===filter);});
    view.querySelectorAll('.lessons li').forEach(function(li){li.classList.toggle('dim',filter!=='all'&&li.dataset.level!==filter);});
  }
  function route(){
    var h=location.hash.replace(/^#\\/?/,'');
    var id = !h ? 't-home' : /^\\d+\\.\\d+$/.test(h) ? 't-l'+h.replace('.','-') : 't-'+h;
    var tpl=document.getElementById(id) || document.getElementById('t-home');
    view.innerHTML=''; view.appendChild(tpl.content.cloneNode(true));
    document.title = (tpl.id.indexOf('t-l')===0 ? view.querySelector('h1').textContent.trim()+' · ' : '') + ${JSON.stringify(t.title)};
    view.querySelectorAll('.filters button').forEach(function(b){b.addEventListener('click',function(){filter=b.dataset.f;applyFilter();try{sessionStorage.setItem('aigp-filter',filter);}catch(e){}});});
    applyFilter();
    var rf=document.getElementById('repoFilter');
    if(rf) rf.addEventListener('input',function(){
      var q=rf.value.trim().toLowerCase();
      view.querySelectorAll('.cat').forEach(function(sec){
        var any=false; sec.querySelectorAll('tbody tr').forEach(function(tr){var m=!q||tr.dataset.q.indexOf(q)>-1; tr.hidden=!m; any=any||m;});
        sec.hidden=!any;
      });
    });
    window.scrollTo(0,0); view.focus({preventScroll:true});
  }
  view.addEventListener('click',function(e){var a=e.target.closest('[data-track]'); if(a){filter=a.dataset.track;}});
  try{filter=sessionStorage.getItem('aigp-filter')||'all';}catch(e){}
  window.addEventListener('hashchange',route); route();
})();
</script>
</body>
</html>
`;
  }

  const flatLinks = (html) => html
    .replace(/href="#\/(\d+)\.(\d+)"/g, 'href="#l$1-$2"')
    .replace(/href="#\/repos"/g, 'href="#repos"')
    .replace(/href="#\/map"/g, 'href="#contents"')
    .replace(/href="#\/about"/g, 'href="#start"')
    .replace(/href="#\/"/g, 'href="#top"');

  function flatPage(fill) {
    const modules = MODULES.map((mod) => `<section class="flat-mod" id="module-${esc(mod.key)}">
  <p class="eyebrow">${t.module} ${esc(mod.key)}</p>
  <h1>${esc(mod.title)}</h1>
  ${mod.intro ? `<div class="mod-intro">${marked.parse(mod.intro)}</div>` : ''}
</section>
${ALL_LESSONS.filter((l) => l.mod === mod).map((l) => `<article class="lesson flat-lesson" id="${slug(l.num)}" data-level="${LEVEL_KEYS[l.level]}">
${lessonInner(l)}
<p class="back"><a href="#contents">${t.backContents}</a></p>
</article>`).join('\n')}`).join('\n');
    const body = `<header class="top"><div class="bar">
  <a class="brand" href="#top">AI Governance <b>Zero to Hero</b></a>
  <nav>
    <a href="#contents">${t.nav.contents}</a>
    <a href="#repos">${t.nav.repos}</a>
    <a href="index${sfx(lang, '.html')}">${t.nav.reader}</a>
    ${langLink(`course${sfx(t.other, '.html')}`)}
    <button id="themeBtn" type="button" aria-label="Toggle dark mode">◐</button>
  </nav>
</div></header>
<main id="top">
<section class="hero">
  <p class="eyebrow">${t.flatEyebrow}</p>
  <h1>${t.flatH1}</h1>
  <div class="stats">
    <div><b>${MODULES.length}</b>${t.stats[0]}</div>
    <div><b>${ALL_LESSONS.length}</b>${t.stats[1]}</div>
    <div><b>${REPO_INDEX.size}</b>${t.stats[2]}</div>
  </div>
</section>
<section class="page prose" id="start">
<h1>${t.startHere}</h1>
${readmeHtml()}
</section>
<section class="page" id="contents">
  <h1>${t.nav.contents}</h1>
  <div class="filters" role="group" aria-label="${t.filterLabel}">
    <button data-f="all" class="on">${t.all}</button><button data-f="b">${t.levels.Beginner}</button><button data-f="i">${t.levels.Intermediate}</button><button data-f="a">${t.levels.Advanced}</button>
  </div>
  ${mapHtml()}
</section>
${modules}
<section class="page" id="repos">
<h1>${t.appendixCatalog}</h1>
<p class="lede">${t.catLede}</p>
${catalogHtml()}
</section>
</main>
<footer><p>${t.flatFooter}</p></footer>`;
    return `${head(t.courseTitle, t.description, AIGP_CSS + `
.flat-mod{padding:3.5rem 0 1rem;border-top:2px solid var(--line);margin-top:2rem}
.flat-mod h1{font-family:var(--serif);font-size:clamp(1.9rem,5vw,2.8rem);margin:.2rem 0 .6rem}
.flat-lesson{border-top:1px dashed var(--line);margin-top:1.5rem}
.back{font:600 .82rem var(--sans);text-align:end}
.back a{text-decoration:none}
@media print{.back,.filters,.cat-tools{display:none}.flat-mod,.flat-lesson{break-before:page;border:0}.sec-quiz details{display:block}}`)}
<body>
${fill(flatLinks(body))}
<script>
(function(){
  ${themeScript}
  document.querySelectorAll('.filters button').forEach(function(b){b.addEventListener('click',function(){
    var f=b.dataset.f;
    document.querySelectorAll('.filters button').forEach(function(x){x.classList.toggle('on',x===b);});
    document.querySelectorAll('.lessons li').forEach(function(li){li.classList.toggle('dim',f!=='all'&&li.dataset.level!==f);});
  });});
  var rf=document.getElementById('repoFilter');
  if(rf) rf.addEventListener('input',function(){
    var q=rf.value.trim().toLowerCase();
    document.querySelectorAll('.cat').forEach(function(sec){
      var any=false; sec.querySelectorAll('tbody tr').forEach(function(tr){var m=!q||tr.dataset.q.indexOf(q)>-1; tr.hidden=!m; any=any||m;});
      sec.hidden=!any;
    });
  });
})();
</script>
</body>
</html>
`;
  }

  for (const l of ALL_LESSONS) l.html = renderLesson(l);
  return { lang, MODULES, ALL_LESSONS, REPO_INDEX, CATALOG, page, flatPage, courseMarkdown, reposMarkdown };
}

/* -------------------------------------------------------------------- main */

const built = LANGS.map(buildLang);

// Parity: the Arabic mirror must carry the same lessons as the English source.
if (built.length > 1) {
  const [en, ...others] = built;
  const problems = [];
  for (const o of others) {
    en.MODULES.forEach((m, i) => {
      const om = o.MODULES[i];
      const a = m.lessons.map((l) => l.num).join(','), b = om ? om.lessons.map((l) => l.num).join(',') : '';
      if (a !== b) problems.push(`${o.MODULES[i]?.file || m.file}: lessons [${b}] ≠ English [${a}]`);
    });
    en.ALL_LESSONS.forEach((l, i) => {
      const ol = o.ALL_LESSONS[i];
      if (!ol) return;
      if (l.level !== ol.level) problems.push(`${l.num}: level ${ol.level} ≠ English ${l.level}`);
      const d = count(l.body, /```mermaid/g), od = count(ol.body, /```mermaid/g);
      if (d !== od) problems.push(`${l.num}: ${od} diagrams ≠ English ${d}`);
      const q = count(l.body, /<details>/g), oq = count(ol.body, /<details>/g);
      if (q !== oq) problems.push(`${l.num}: ${oq} quiz answers ≠ English ${q}`);
    });
    const en_r = [...en.REPO_INDEX.keys()].sort().join(), o_r = [...o.REPO_INDEX.keys()].sort().join();
    if (en_r !== o_r) {
      const miss = [...en.REPO_INDEX.keys()].filter((k) => !o.REPO_INDEX.has(k));
      const extra = [...o.REPO_INDEX.keys()].filter((k) => !en.REPO_INDEX.has(k));
      problems.push(`${o.lang} instrument tables differ (bold names must match the English) — missing: ${miss.join(', ') || '—'}; extra: ${extra.join(', ') || '—'}`);
    }
  }
  if (problems.length) {
    console.error(`✗ Arabic mirror is out of step with the English source:\n  ${problems.join('\n  ')}`);
    process.exit(1);
  }
}

const svgs = await renderDiagrams(diagrams);
const failed = svgs.map((s, i) => (typeof s === 'string' ? null : i)).filter((i) => i !== null);
if (failed.length) {
  for (const i of failed) console.error(`✗ Mermaid diagram ${i} failed: ${svgs[i].error}\n---\n${diagrams[i]}\n---`);
  process.exit(1);
}
const fill = (html) => html.replace(/<!--DIAGRAM:(\d+)-->/g, (_, i) => svgs[+i]);

for (const b of built) {
  const o = OUT(b.lang);
  for (const l of b.ALL_LESSONS) {
    for (const [emoji, name] of [['⚖', 'instruments'], ['⚡', 'summary'], ['✍', 'quiz']]) {
      if (!b.ALL_LESSONS.length || !new RegExp(`^## ${emoji}`, 'm').test(l.body)) console.warn(`! [${b.lang}] ${l.num} has no ${name} section`);
    }
  }
  fs.writeFileSync(o.html, b.page(fill));
  fs.writeFileSync(o.course, b.flatPage(fill));
  fs.writeFileSync(o.courseMd, b.courseMarkdown());
  fs.writeFileSync(o.repos, b.reposMarkdown());
  console.log(`✓ [${b.lang}] ${b.MODULES.length} modules, ${b.ALL_LESSONS.length} lessons, ${b.REPO_INDEX.size} instruments → ${Object.values(o).map((f) => path.relative(ROOT, f)).join(', ')}`);
}
console.log(`✓ ${diagrams.length} diagrams rendered (${SOURCE_DIGEST})`);

async function renderDiagrams(sources) {
  if (!sources.length) return [];
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox'],
    executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || undefined,
  });
  try {
    const page = await browser.newPage();
    await page.setContent('<!doctype html><html><body></body></html>');
    await page.addScriptTag({ path: path.join(ROOT, 'node_modules/mermaid/dist/mermaid.min.js') });
    return await page.evaluate(async (codes) => {
      let seed = 20260924;
      Math.random = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
      window.mermaid.initialize({
        startOnLoad: false, theme: 'neutral', securityLevel: 'loose', look: 'classic',
        deterministicIds: true, deterministicIDSeed: 'aigp',
        fontFamily: 'ui-sans-serif, system-ui, -apple-system, "Segoe UI", Tahoma, sans-serif',
      });
      const out = [];
      for (let i = 0; i < codes.length; i++) {
        try {
          const { svg } = await window.mermaid.render('sd' + i, codes[i]);
          out.push(svg);
        } catch (e) {
          out.push({ error: String((e && e.message) || e) });
        }
      }
      return out;
    }, sources);
  } finally {
    await browser.close();
  }
}
