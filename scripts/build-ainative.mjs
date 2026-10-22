/**
 * Build the "A Practical Guide to Becoming an AI-Native Engineer" course.
 *
 *   node scripts/build-ainative.mjs           → for each language (en, ar):
 *                                            ainative/index[.ar].html        (interactive reader)
 *                                            ainative/course[.ar].html       (the whole course, one flat page)
 *                                            ainative/COURSE[.ar].md         (the whole course, one markdown file)
 *                                            ainative/TOOLKIT[.ar].md        (controls, standards and tools catalogue)
 *   node scripts/build-ainative.mjs --check   → fail if the committed outputs are stale
 *   node scripts/build-ainative.mjs --lang=en → build one language only (drafting)
 *
 * Adapted from build-aiapps.mjs: same module/lesson format and reader, with a
 * focus tag on every lesson ("*Level: …* · *Prerequisites: …* · *Focus: Verify*") and the
 * "🧰 The toolkit" tables feeding the catalogue. The first cell of each toolkit row starts with the
 * item's name in bold; those names build the catalogue and must match across languages.
 *
 * Sources: ainative/README.md, ainative/modules/NN-*.md and their .ar.md mirrors. The markdown is the source
 * of truth; everything else in ainative/ is generated — never edit it by hand.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import { trailerHtml, TRAILER_CSS } from './trailer.mjs';
import puppeteer from 'puppeteer';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const COURSE_DIR = path.join(ROOT, 'ainative');
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
  repos: path.join(COURSE_DIR, `TOOLKIT${sfx(lang, '.md')}`),
});

/* ------------------------------------------------------------------ strings */

const LEVEL_KEYS = { Beginner: 'b', Intermediate: 'i', Advanced: 'a' };
const T = {
  en: {
    dir: 'ltr', other: 'ar', otherLabel: 'عربي', otherTitle: 'اقرأ بالعربية',
    readme: 'README.md',
    module: 'Module', levels: { Beginner: '🟢 Beginner', Intermediate: '🟡 Intermediate', Advanced: '🔴 Advanced' },
    levelWord: 'Level', prereqWord: 'Prerequisites', bokWord: 'Focus', before: 'Before this', comma: ', ',
    prev: '← Previous', next: 'Next →', appendixNext: 'Appendix →', catalog: 'The toolkit catalogue',
    nav: { map: 'Map', about: 'Start here', repos: 'Toolkit', one: 'One page', oneTitle: 'The whole course on one printable page', contents: 'Contents', reader: 'Reader' },
    start: 'Start with lesson 0.1 →', how: 'How the course works',
    lessonsN: (n) => `${n} lesson${n === 1 ? '' : 's'}`,
    mapTitle: 'Course map',
    all: 'All', filterLabel: 'Filter by level',
    startHere: 'Start here',
    flatEyebrow: 'The complete course · one page · print-friendly',
    backContents: '↑ Contents', appendixCatalog: 'Appendix — The toolkit catalogue',
    eyebrow: 'AI-native engineering · a practical guide · for engineers who code',
    h1: 'Work <em>with</em> the agent. Stay <em>accountable</em> for the result.',
    lede: 'What strong engineers do differently when an AI agent is in the loop: give context first, specify before delegating, work in small verified steps, trust evidence rather than fluency, and automate what repeats while keeping the skill. Practical labs on one shared Python codebase with offline graders, with Claude Code as the worked example: context engineering, spec-driven development, the daily loop, verifying and reviewing AI-written code, debugging, legacy code and migration, security, hooks, skills and subagents, parallel agents, team playbooks and staying sharp — with a quiz in every lesson and a 60-question practice exam.',
    stats: ['modules', 'lessons', 'tools, practices & patterns', 'practice questions'],
    tracks: {
      b: ['🟢 Foundations', 'What an AI-native engineer is, how coding agents really work, context engineering and writing specs an agent can build from.'],
      i: ['🟡 Practitioner', 'The daily loop, verification and code review, debugging, legacy code and migration, security, and automating your agent with hooks, skills and subagents.'],
      a: ['🔴 Hero', 'Parallel and multi-agent work, AI across the lifecycle, team playbooks and metrics, staying sharp — then take a change through the whole cycle.'],
    },
    mapLede: 'Every lesson climbs the same ladder — 🟢 essentials → 🟡 going deeper → 🔴 expert view. The dot shows where each lesson <em>starts</em>; the tag shows its focus.',
    catLede: 'Every tool, practice and pattern the course teaches, with what it does and when to reach for it. Agent tools change fast — check the current documentation.',
    catCols: ['Tool, practice or pattern', 'What it is and does', 'When to reach for it'],
    filterPh: (n) => `Filter ${n} entries — try &quot;hook&quot;, &quot;worktree&quot;, &quot;ADR&quot;…`,
    footer: 'Part of the <a href="../">Course Library</a>. Generated from the markdown in <code>ainative/</code> by <code>npm run ainative:build</code>. Source: <a href="https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/ainative">github.com/Tamoura/system-design-for-vibe-coders</a>',
    flatH1: 'A Practical Guide to Becoming an AI-Native Engineer — work <em>with</em> the agent, stay <em>accountable</em> for the result.',
    flatFooter: 'Generated from the markdown in <code>ainative/</code> by <code>npm run ainative:build</code>. Prefer one lesson at a time? Open the <a href="index.html">interactive reader</a>.',
    brand: 'AI-Native Engineer <b>a practical guide</b>',
    title: 'A Practical Guide to Becoming an AI-Native Engineer', courseTitle: 'A Practical Guide to Becoming an AI-Native Engineer — Complete Course',
    description: 'A Practical Guide to Becoming an AI-Native Engineer — a free, bilingual course for engineers who code: how coding agents work, context engineering, spec-driven development, the daily loop, verifying AI-written code, debugging, legacy code, security, hooks, skills and subagents, parallel agents, team playbooks and staying sharp, with graded offline labs, a quiz in every lesson and a 60-question practice exam.',
    md: {
      title: 'A Practical Guide to Becoming an AI-Native Engineer — the complete course',
      sub: (m, l, r) => `*${m} modules · ${l} lessons · ${r} tools, practices and patterns · practical, graded labs*`,
      contents: 'Contents', appendix: 'Appendix — The toolkit catalogue',
      catTitle: 'The Toolkit Catalogue',
      catIntro: (n) => [`Every tool, practice and pattern taught in **A Practical Guide to Becoming an AI-Native Engineer** — ${n} of them — grouped by`,
        'the lesson that teaches it, with what it does and when to reach for it.'],
      az: 'A–Z index',
    },
  },
  ar: {
    dir: 'rtl', other: 'en', otherLabel: 'English', otherTitle: 'Read in English',
    readme: 'README.ar.md',
    module: 'الوحدة', levels: { Beginner: '🟢 مبتدئ', Intermediate: '🟡 متوسط', Advanced: '🔴 متقدم' },
    levelWord: 'المستوى', prereqWord: 'المتطلبات', bokWord: 'التركيز (Focus)', before: 'اقرأ قبله', comma: '، ',
    prev: '→ السابق', next: 'التالي ←', appendixNext: 'الملحق ←', catalog: 'دليل الأدوات (Toolkit)',
    nav: { map: 'الخريطة', about: 'ابدأ هنا', repos: 'الأدوات (Toolkit)', one: 'صفحة واحدة', oneTitle: 'الدورة كاملة في صفحة واحدة قابلة للطباعة', contents: 'المحتويات', reader: 'القارئ' },
    start: 'ابدأ بالدرس 0.1 ←', how: 'كيف تعمل الدورة',
    lessonsN: (n) => `${n} ${n === 1 ? 'درس' : n <= 10 ? 'دروس' : 'درسًا'}`,
    mapTitle: 'خريطة الدورة',
    all: 'الكل', filterLabel: 'التصفية حسب المستوى',
    startHere: 'ابدأ هنا',
    flatEyebrow: 'الدورة كاملة · صفحة واحدة · مناسبة للطباعة',
    backContents: '↑ المحتويات', appendixCatalog: 'الملحق — دليل الأدوات (Toolkit)',
    eyebrow: 'الهندسة الأصيلة في الذكاء الاصطناعي (AI-native engineering) · دليل عملي · للمهندسين الذين يبرمجون',
    h1: 'اعمل <em>مع</em> الوكيل. وابقَ <em>مسؤولًا</em> عن النتيجة.',
    lede: 'ما الذي يفعله المهندسون الأقوياء بصورة مختلفة حين يكون وكيل الذكاء الاصطناعي (AI agent) في الحلقة: يعطون السياق (context) أولًا، ويكتبون المواصفة (spec) قبل التفويض (delegating)، ويعملون بخطوات صغيرة مُتحقَّق منها (small verified steps)، ويثقون بالدليل (evidence) لا بالطلاقة (fluency)، ويؤتمتون ما يتكرر مع الحفاظ على المهارة. مختبرات عملية على مستودع Python واحد مشترك بمُقيِّمات (graders) تعمل دون اتصال، مع Claude Code مثالًا تطبيقيًا: هندسة السياق (context engineering)، والتطوير الموجَّه بالمواصفات (spec-driven development)، والحلقة اليومية (daily loop)، والتحقق من الشيفرة التي كتبها الذكاء الاصطناعي ومراجعتها، وتصحيح الأخطاء (debugging)، والشيفرة الموروثة (legacy code) والترحيل (migration)، والأمان (security)، والخطافات (hooks) والمهارات (skills) والوكلاء الفرعيين (subagents)، والعمل المتوازي مع عدة وكلاء، وأدلة الفرق (team playbooks)، والبقاء حادّ المهارة — مع اختبار في كل درس وامتحان تدريبي من 60 سؤالًا.',
    stats: ['وحدات', 'درسًا', 'أداة وممارسة ونمط', 'سؤالًا تدريبيًا'],
    tracks: {
      b: ['🟢 الأساسيات (Foundations)', 'ما المهندس الأصيل في الذكاء الاصطناعي (AI-native engineer)، وكيف يعمل وكلاء البرمجة (coding agents) فعلًا، وهندسة السياق (context engineering)، وكتابة مواصفات يستطيع الوكيل البناء منها.'],
      i: ['🟡 الممارس (Practitioner)', 'الحلقة اليومية (daily loop)، والتحقق ومراجعة الشيفرة (code review)، وتصحيح الأخطاء، والشيفرة الموروثة والترحيل، والأمان، وأتمتة وكيلك بالخطافات (hooks) والمهارات (skills) والوكلاء الفرعيين (subagents).'],
      a: ['🔴 المحترف (Hero)', 'العمل المتوازي ومتعدد الوكلاء (multi-agent)، والذكاء الاصطناعي عبر دورة الحياة، وأدلة الفرق (team playbooks) والمقاييس، والبقاء حادّ المهارة — ثم الوصول بتغيير كامل عبر الدورة كلها.'],
    },
    mapLede: 'كل درس يصعد السلّم نفسه: 🟢 الأساسيات ← 🟡 التعمق أكثر ← 🔴 نظرة الخبير. تشير النقطة إلى المستوى الذي <em>يبدأ</em> منه الدرس، ويشير الوسم إلى تركيزه (focus).',
    catLede: 'كل أداة (tool) وممارسة (practice) ونمط (pattern) تدرّسها الدورة، مع ما تفعله ومتى تلجأ إليها. أدوات الوكلاء تتغير بسرعة، فراجع التوثيق الحالي (current documentation).',
    catCols: ['الأداة أو الممارسة أو النمط', 'ما هي وماذا تفعل', 'متى تلجأ إليها'],
    filterPh: (n) => `صفِّ ${n} عنصرًا — جرّب &quot;hook&quot; أو &quot;worktree&quot; أو &quot;ADR&quot;…`,
    footer: 'جزء من <a href="../">مكتبة الدورات</a>. مولَّدة من ملفات الماركداون في <code>ainative/</code> عبر <code>npm run ainative:build</code>. المصدر: <a href="https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/ainative">github.com/Tamoura/system-design-for-vibe-coders</a>',
    flatH1: 'دليل عملي لتصبح مهندسًا أصيلًا في الذكاء الاصطناعي (AI-Native Engineer): اعمل <em>مع</em> الوكيل وابقَ <em>مسؤولًا</em> عن النتيجة.',
    flatFooter: 'مولَّدة من ملفات الماركداون في <code>ainative/</code> عبر <code>npm run ainative:build</code>. تفضّل درسًا واحدًا في كل مرة؟ افتح <a href="index.ar.html">القارئ التفاعلي</a>.',
    brand: 'المهندس الأصيل في الذكاء الاصطناعي <b>دليل عملي</b>',
    title: 'دليل عملي لتصبح مهندسًا أصيلًا في الذكاء الاصطناعي (AI-Native Engineer)', courseTitle: 'دليل عملي لتصبح مهندسًا أصيلًا في الذكاء الاصطناعي (AI-Native Engineer) — الدورة كاملة',
    description: 'دليل عملي لتصبح مهندسًا أصيلًا في الذكاء الاصطناعي: دورة مجانية ثنائية اللغة للمهندسين الذين يبرمجون عن كيف يعمل وكلاء البرمجة، وهندسة السياق، والتطوير الموجَّه بالمواصفات، والحلقة اليومية، والتحقق من الشيفرة التي يكتبها الذكاء الاصطناعي، وتصحيح الأخطاء، والشيفرة الموروثة، والأمان، والخطافات والمهارات والوكلاء الفرعيين، والوكلاء المتوازيين، وأدلة الفرق، والبقاء حادّ المهارة، مع مختبرات مُقيَّمة تعمل دون اتصال واختبار في كل درس وامتحان تدريبي من 60 سؤالًا.',
    md: {
      title: 'دليل عملي لتصبح مهندسًا أصيلًا في الذكاء الاصطناعي (AI-Native Engineer) — الدورة كاملة',
      sub: (m, l, r) => `*${m} وحدات · ${l} درسًا · ${r} أداة وممارسة ونمط · مختبرات عملية مُقيَّمة*`,
      contents: 'المحتويات', appendix: 'الملحق — دليل الأدوات (Toolkit)',
      catTitle: 'دليل الأدوات (Toolkit)',
      catIntro: (n) => [`كل أداة وممارسة ونمط تدرّسها دورة **دليل عملي لتصبح مهندسًا أصيلًا في الذكاء الاصطناعي (AI-Native Engineer)**، وعددها ${n}، مجمّعة حسب الدرس الذي يدرّسها،`,
        'مع ما تفعله ومتى تلجأ إليها.'],
      az: 'فهرس أبجدي',
    },
  },
};

/* ------------------------------------------------------------------ sources */

const enFiles = fs.readdirSync(MODULE_DIR).filter((f) => /^\d\d-.+\.md$/.test(f) && !f.endsWith('.ar.md')).sort();
const filesFor = (lang) => (lang === 'en' ? enFiles : enFiles.map((f) => f.replace(/\.md$/, `.${lang}.md`)));
const SOURCE_FILES = [
  ...LANGS.flatMap((lang) => [`ainative/${T[lang].readme}`, ...filesFor(lang).map((f) => `ainative/modules/${f}`)]),
  'scripts/build-ainative.mjs',
  'scripts/saas.css', 'scripts/trailer.mjs',
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
      if (!txt.includes(`ainative-source: ${SOURCE_DIGEST}`) && !txt.includes(`ainative-source" content="${SOURCE_DIGEST}"`)) {
        stale.push(path.relative(ROOT, f));
      }
    }
  }
  if (stale.length) {
    console.error(`✗ Stale ainative course output: ${stale.join(', ')}\n  Run \`npm run ainative:build\` and commit the result.`);
    process.exit(1);
  }
  console.log(`✓ Ainative course output matches its sources (${SOURCE_DIGEST}).`);
  process.exit(0);
}

/* ------------------------------------------------------------------- parse */

const MODULE_RE = /^# (?:Module|الوحدة)(?: \([^)]*\))? (\d+)(?: \([^)]*\))? — (.+)$/m;
const LESSON_RE = /^# (\d+\.\d+) — (.+)$/;
const LEVEL_RE = /^\*(?:Level|المستوى)(?: \([^)]*\))?:\s*(🟢|🟡|🔴)\s*(Beginner|Intermediate|Advanced|مبتدئ|متوسط|متقدم)(?: \([^)]*\))?\*(.*)$/;
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
          const pre = lv[3].match(/(?:Prerequisites?|المتطلبات)(?: \([^)]*\))?:\s*([^*]+)\*/);
          cur.prereq = pre ? pre[1].trim() : '';
          const bok = lv[3].match(/(?:Focus|التركيز)[^:]*:\s*([^*]+)\*/);
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
  '⚡': 'tldr', '🧭': 'why', '📐': 'how', '🧰': 'repos', '🏛': 'wild', '🛠': 'build',
  '⚠': 'mistakes', '🧾': 'recap', '✍': 'quiz', '📚': 'refs',
};

const AINATIVE_CSS = `
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
    const sec = lesson.body.split(/\n(?=## )/).find((s) => s.startsWith('## 🧰'));
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
    out.push('<!-- Generated by scripts/build-ainative.mjs from the lessons\' "🧰" tables. Do not edit by hand. -->');
    out.push(`<!-- ainative-source: ${SOURCE_DIGEST} -->`);
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
    .replace(/\]\(\.\.?\/(?:REPOS|INSTRUMENTS|TOOLKIT)(?:\.ar)?\.md\)/g, '](#appendix-the-repo-catalog)')
    .replace(/\]\(\.\.?\/(?:OUTLINE|README)(?:\.ar)?\.md(?:#[\w-]+)?\)/g, '](#contents)');

  function courseMarkdown() {
    const out = [];
    const readme = fs.readFileSync(path.join(COURSE_DIR, t.readme), 'utf8').replace(/^# .+\n/, '');
    out.push(`<!-- Generated by scripts/build-ainative.mjs from ainative/${t.readme} and ainative/modules/*${sfx(lang, '.md')}. Do not edit by hand. -->`);
    out.push(`<!-- ainative-source: ${SOURCE_DIGEST} -->`);
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
      const md = p.replace(/\]\(\.\.\/(?:REPOS|INSTRUMENTS|TOOLKIT)(?:\.ar)?\.md\)/g, '](#/repos)').replace(/\]\(\.\.\/(?:OUTLINE|README)(?:\.ar)?\.md\)/g, '](#/map)');
      return `<section class="sec sec-${cls}">${linkLessons(tableWrap(marked.parse(md)))}</section>`;
    }).join('\n');
  }

  const prereqLinks = (l) => l.prereq.split(/\s*[,،]\s*/).map((n) => (LESSON_NUMS.has(n) ? `<a href="#/${n}">${n}</a>` : esc(n))).join(t.comma);
  function lessonInner(l) {
    const prereq = l.prereq ? ` · <span class="prereq">${t.before}: ${prereqLinks(l)}</span>` : '';
    return `<p class="crumb"><a href="#/map">${t.module} ${esc(l.mod.key)} — ${esc(l.mod.title)}</a></p>
<h1><span class="num">${esc(l.num)}</span> ${esc(l.title)}</h1>
<p class="meta"><span class="lvl lvl-${LEVEL_KEYS[l.level]}">${lvlLabel(l.level)}</span>${l.bok ? ` · <span class="bok">${t.bokWord} <bdi dir="${/[\u0600-\u06FF]/.test(l.bok) ? 'rtl' : 'ltr'}">${esc(l.bok)}</bdi></span>` : ''}${prereq}</p>
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
      .replace(/\]\(\.\/(?:REPOS|INSTRUMENTS|TOOLKIT)(?:\.ar)?\.md\)/g, '](#/repos)');
    return linkLessons(tableWrap(marked.parse(md)));
  }

  const langLink = (target) => `<a class="lang" href="${target}" hreflang="${t.other}" lang="${t.other}" title="${t.otherTitle}" data-keep-hash>${t.otherLabel}</a>`;
  const themeScript = `var root=document.documentElement;
  try{var t=localStorage.getItem('ainative-theme'); if(t) root.setAttribute('data-theme',t);}catch(e){}
  document.getElementById('themeBtn').addEventListener('click',function(){
    var dark=root.getAttribute('data-theme')==='dark'||(!root.getAttribute('data-theme')&&matchMedia('(prefers-color-scheme: dark)').matches);
    var next=dark?'light':'dark'; root.setAttribute('data-theme',next);
    try{localStorage.setItem('ainative-theme',next);}catch(e){}
  });
  document.querySelectorAll('[data-keep-hash]').forEach(function(a){a.addEventListener('click',function(){a.href=a.getAttribute('href').split('#')[0]+location.hash;});});
  try{localStorage.setItem('ainative-lang','${lang}');}catch(e){}`;
  const css = fs.readFileSync(path.join(ROOT, 'scripts/saas.css'), 'utf8') + TRAILER_CSS;
  const head = (title, desc, extraCss = '') => `<!doctype html>
<html lang="${lang}" dir="${t.dir}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="ainative-source" content="${SOURCE_DIGEST}">
<meta name="description" content="${esc(desc)}">
<title>${esc(title)}</title>
<style>
${css}${extraCss}
</style>
</head>`;
  const n = (k) => ALL_LESSONS.filter((l) => l.level === k).length;

  function page(fill) {
    return `${head(t.title, t.description, AINATIVE_CSS)}
<body>
<header class="top"><div class="bar">
  <a class="brand" href="#/">${t.brand}</a>
  <nav>
    <a href="#/map">${t.nav.map}</a>
    <a href="#/about">${t.nav.about}</a>
    <a href="#/repos">${t.nav.repos}</a>
    <a href="course${sfx(lang, '.html')}" title="${t.nav.oneTitle}">${t.nav.one}</a>
    <a href="assessment${sfx(lang, '.html')}">${lang === 'ar' ? 'التقييم الذاتي' : 'Self-assessment'}</a>
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
  ${trailerHtml('ainative', lang)}
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
    view.innerHTML=''; view.appendChild(document.importNode(tpl.content,true));
    document.title = (tpl.id.indexOf('t-l')===0 ? view.querySelector('h1').textContent.trim()+' · ' : '') + ${JSON.stringify(t.title)};
    view.querySelectorAll('.filters button').forEach(function(b){b.addEventListener('click',function(){filter=b.dataset.f;applyFilter();try{sessionStorage.setItem('ainative-filter',filter);}catch(e){}});});
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
  try{filter=sessionStorage.getItem('ainative-filter')||'all';}catch(e){}
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
  <a class="brand" href="#top">${t.brand}</a>
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
    return `${head(t.courseTitle, t.description, AINATIVE_CSS + `
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
      problems.push(`${o.lang} toolkit tables differ (bold names must match the English) — missing: ${miss.join(', ') || '—'}; extra: ${extra.join(', ') || '—'}`);
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

// Arabic pages: isolate every parenthesised English gloss so the bidi algorithm keeps its words,
// digits and hyphens in order inside right-to-left text — «(60-question exam)» would otherwise
// show as «(question exam-60)», and «(Non-repudiation)» broken across lines as «(-Non».
// Runs before diagrams are filled in, and never inside script, style, code, pre or title.
const GLOSS = /⁦?\((?=[^\s()؀-ۿ<>])[^()؀-ۿ<>\n]*\)⁩?/g;
const isolateGlosses = (html) => html.replace(
  /<(script|style|pre|code|title|textarea)\b[\s\S]*?<\/\1>|<[^>]*>|[^<]+/gi,
  (m, protectedTag) => (protectedTag || m[0] === '<' ? m : m.replace(GLOSS, '<bdi>$&</bdi>')));

for (const b of built) {
  const o = OUT(b.lang);
  for (const l of b.ALL_LESSONS) {
    for (const [emoji, name] of [['🧰', 'toolkit'], ['⚡', 'summary'], ['✍', 'quiz']]) {
      if (!b.ALL_LESSONS.length || !new RegExp(`^## ${emoji}`, 'm').test(l.body)) console.warn(`! [${b.lang}] ${l.num} has no ${name} section`);
    }
  }
  const bidi = (html) => fill(b.lang === 'ar' ? isolateGlosses(html) : html);
  fs.writeFileSync(o.html, bidi(b.page((h) => h)));
  fs.writeFileSync(o.course, bidi(b.flatPage((h) => h)));
  fs.writeFileSync(o.courseMd, b.courseMarkdown());
  fs.writeFileSync(o.repos, b.reposMarkdown());
  console.log(`✓ [${b.lang}] ${b.MODULES.length} modules, ${b.ALL_LESSONS.length} lessons, ${b.REPO_INDEX.size} tools → ${Object.values(o).map((f) => path.relative(ROOT, f)).join(', ')}`);
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
        deterministicIds: true, deterministicIDSeed: 'ainative',
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
