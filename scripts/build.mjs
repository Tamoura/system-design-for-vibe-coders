#!/usr/bin/env node
/**
 * Builds every distributable form of the course from the module markdown.
 *
 *   npm run build   index.html (bilingual) + index.en.html + index.ar.html
 *   npm run dist    the above, plus PDF and EPUB per language into dist/
 *   npm run check   rebuild in memory; fail if the committed HTML is stale
 *
 * The markdown under modules/ is the source of truth. Everything here is
 * generated output — never hand-edit it, edit the lesson and rebuild.
 *
 * Mermaid diagrams are pre-rendered to inline SVG in a headless browser, so
 * every output is self-contained and needs no network at read time.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import puppeteer from 'puppeteer';
import archiver from 'archiver';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIST = path.join(ROOT, 'dist');
const argv = process.argv.slice(2);
const CHECK = argv.includes('--check');
const WANT_PDF = argv.includes('--pdf') || argv.includes('--all');
const WANT_EPUB = argv.includes('--epub') || argv.includes('--all');

/* Course order. Lessons are gathered from every file listed and then sorted by
   lesson number, so a module split across files (3.2 lives on its own) still
   comes out in reading order. */
const MODULES = [
  { key: 'F',  dir: '00-foundations',           files: ['foundations.md'] },
  { key: '0',  dir: '0-the-gap',                files: ['the-gap.md'] },
  { key: '1',  dir: '01-anatomy-of-a-real-app', files: ['lesson-1-draw-the-boxes.md', 'lesson-2-the-requests-journey.md', 'lesson-3-day-one-eyes.md'] },
  { key: '2',  dir: '02-data-storage-backups',  files: ['module.md'] },
  { key: '3',  dir: '03-caching',               files: ['module.md', 'lesson-2-cache-poisoning.md'] },
  { key: '4',  dir: '04-deploys',               files: ['module.md'] },
  { key: '5',  dir: '05-users-abuse',           files: ['module.md'] },
  { key: '6',  dir: '06-many-clients',          files: ['module.md'] },
  { key: '7',  dir: '07-observability',         files: ['module.md'] },
  { key: '8',  dir: '08-safety-nets',           files: ['module.md'] },
  { key: '9',  dir: '09-directing-ai-team',     files: ['module.md'] },
  { key: '10', dir: '10-scaling',               files: ['module.md'] },
  { key: '11', dir: '11-reaching-the-world',    files: ['module.md'] },
  { key: '12', dir: '12-capstone',              files: ['module.md'] },
];

/* The four pillars every lesson is built from, plus the three closing blocks.
   Detected by the emoji the markdown already uses as its section marker. */
const PILLARS = [
  { emoji: '🔥', cls: 'pc-story',     label: { en: 'War Story', ar: 'قصة من الميدان' } },
  { emoji: '📐', cls: 'pc-principle', label: { en: 'Principle', ar: 'المبدأ' } },
  { emoji: '🎛', cls: 'pc-build',     label: { en: 'Direct Your Agent', ar: 'وجّه وكيلك' } },
  { emoji: '✅', box: 'verify',       label: { en: 'Verify It', ar: 'تحقّق منه' } },
  { emoji: '🧾', box: 'recap',        label: { en: 'Recap card', ar: 'بطاقة الخلاصة' } },
  { emoji: '📚', box: 'refs',         label: { en: 'References', ar: 'المراجع' } },
];

const T = {
  en: {
    title: 'System Design for Vibe Coders', dir: 'ltr',
    eyebrow: 'The complete course · English', appendix: 'Appendix', map: 'Map', mapTitle: 'Course map',
    modWord: (k) => (k === 'F' ? 'Part 0' : `Module ${k}`),
    blurb: `Production engineering for AI-assisted builders. Every lesson is anchored in a real
  incident — from a real product's war-story bank or a famous industry outage — then turned
  into a principle, literal prompts to give your agent, and an evidence checklist so you can
  verify the work without reading code.`,
    mapBlurb: 'Fourteen modules, in the order a real product forces them on you. Click a module to see its lessons; click a lesson to jump to it.',
    stats: ['modules', 'lessons', 'languages', 'diagrams'],
    contents: 'Contents',
  },
  ar: {
    title: 'تصميم الأنظمة لمبرمجي الفايب', dir: 'rtl',
    eyebrow: 'الدورة كاملة · العربية', appendix: 'ملحق', map: 'الخريطة', mapTitle: 'خريطة الدورة',
    modWord: (k) => (k === 'F' ? 'الجزء 0' : `الوحدة ${k}`),
    blurb: 'هندسة الإنتاج لمن يبني بمساعدة الذكاء الاصطناعي. كل درس يبدأ من حادثة حقيقية — من بنك حوادث منتج حقيقي أو عطل صناعي شهير — ثم يتحول إلى مبدأ، وتعليمات حرفية توجّه بها وكيلك، وقائمة أدلة تتحقق بها من العمل دون قراءة كود.',
    mapBlurb: 'أربع عشرة وحدة، بالترتيب الذي يفرضه المنتج الحقيقي. اضغط على الوحدة لترى دروسها، وعلى الدرس للانتقال إليه.',
    stats: ['وحدة', 'درسًا', 'لغتان', 'مخططًا'],
    contents: 'المحتويات',
  },
};

const LESSON_RE = /^((?:F|\d+)\.\d+|12)\s+—\s+(.+)$/;
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/** Anchor for a lesson: "F.1" -> lF-1, "10.3" -> l10-3, "12" -> l12. */
const anchor = (num) => 'l' + num.replace('.', '-');

/* ---------------------------------------------------------------- diagrams */

/* Every distinct Mermaid source gets one id, so rendering the same lesson into
   several outputs reuses one SVG instead of re-registering it. */
const diagramIds = new Map();
const diagramId = (src) => {
  if (!diagramIds.has(src)) diagramIds.set(src, diagramIds.size);
  return diagramIds.get(src);
};
let SVGS = [];

const inlineDiagrams = (html) =>
  html.replace(/<div data-diagram="(\d+)"><\/div>/g, (_, i) => {
    const svg = SVGS[+i];
    return typeof svg === 'string'
      ? `<figure class="diagram">${svg}</figure>`
      : `<figure class="diagram"><pre>${esc([...diagramIds.keys()][+i])}</pre></figure>`;
  });

/* ---------------------------------------------------------------- markdown */

/** Links in the markdown are written for GitHub; retarget them for one page. */
const retargetLinks = (md) => md
  .replace(/\]\((?:\.\.\/)*\.?\/?GLOSSARY(?:\.ar)?\.md\)/g, '](#glossary)')
  .replace(/\]\((?:\.\.\/)+([^)]+)\)/g, ']($1)');

/** Split a file on top-level `# ` headings, ignoring anything inside a fence. */
function splitBlocks(md) {
  const lines = md.split('\n');
  const marks = [];
  let fence = false;
  lines.forEach((l, i) => {
    if (/^\s*```/.test(l)) fence = !fence;
    if (!fence && /^# \S/.test(l)) marks.push(i);
  });
  return marks.map((start, i) => ({
    heading: lines[start].replace(/^# /, '').trim(),
    body: lines.slice(start + 1, i + 1 < marks.length ? marks[i + 1] : lines.length).join('\n'),
  }));
}

/** Split a lesson body on `## ` section headings, ignoring fences. */
function splitSections(body) {
  const lines = body.split('\n');
  const out = [{ head: null, lines: [] }];
  let fence = false;
  for (const l of lines) {
    if (/^\s*```/.test(l)) fence = !fence;
    if (!fence && /^## \S/.test(l)) out.push({ head: l.replace(/^## /, '').trim(), lines: [] });
    else out[out.length - 1].lines.push(l);
  }
  return out.filter((s) => s.head !== null || s.lines.join('').trim());
}

const trim = (s) => s.replace(/^\s*(?:---\s*)?\n?/, '').replace(/\n\s*---\s*$/, '').trim();

/** Markdown -> HTML for one chunk: diagrams pulled out, headings pushed down. */
function render(md) {
  const withPlaceholders = md.replace(/```mermaid\n([\s\S]*?)```/g,
    (_, code) => `\n<div data-diagram="${diagramId(code.trim())}"></div>\n`);
  let html = marked.parse(retargetLinks(withPlaceholders), { async: false, gfm: true, breaks: false });
  html = html.replace(/<(\/?)h([1-5])(\s[^>]*)?>/g, (_, slash, n, rest) => `<${slash}h${+n + 1}${rest || ''}>`);
  return html.replace(/<table>/g, '<div class="table-scroll"><table>').replace(/<\/table>/g, '</table></div>');
}

/** One `## ` section -> its pillar heading or coloured box. */
function renderSection(section, lang) {
  const inner = render(section.lines.join('\n'));
  if (section.head === null) return inner;

  const pillar = PILLARS.find((p) => section.head.startsWith(p.emoji));
  if (!pillar) return `<h3>${esc(section.head)}</h3>\n${inner}`;

  const rest = section.head.slice(pillar.emoji.length).replace(/^️?\s*/, '');
  if (pillar.box) return `<div class="${pillar.box}"><h4>${esc(pillar.label[lang])}</h4>\n${inner}</div>`;

  // "The Story: the day Facebook forgot where it lived" -> keep the subtitle only;
  // the tag chip already says which pillar this is.
  const m = rest.match(/^[^:—]*[:：]\s*(.+)$/) || rest.match(/^[^—]*—\s*(.+)$/);
  return `<h3 class="${pillar.cls}"><span class="tag">${esc(pillar.label[lang])}</span>${esc(m ? m[1].trim() : '')}</h3>\n${inner}`;
}

/** Parse one module's markdown for a language into {intro, lessons}. */
function parseModule(mod, lang) {
  const suffix = lang === 'ar' ? '.ar.md' : '.md';
  let intro = null;
  const lessons = [];

  for (const file of mod.files) {
    const full = path.join(ROOT, 'modules', mod.dir, file.replace(/\.md$/, suffix));
    if (!fs.existsSync(full)) throw new Error(`missing ${path.relative(ROOT, full)}`);

    for (const block of splitBlocks(fs.readFileSync(full, 'utf8'))) {
      const m = block.heading.match(LESSON_RE);
      if (m) {
        let body = trim(block.body);
        let kicker = '';
        const k = body.match(/^\*([^*\n][^\n]*)\*\s*(?:\n|$)/);   // leading *italic* is the module kicker
        if (k) { kicker = k[1].trim(); body = trim(body.slice(k[0].length)); }
        lessons.push({ num: m[1], title: m[2].trim(), kicker, body, lang });
      } else if (!intro) {
        intro = { title: block.heading, html: render(trim(block.body)) };
      }
    }
  }

  const order = (n) => (n === '12' ? 0 : Number(n.split('.')[1]));
  lessons.sort((a, b) => order(a.num) - order(b.num));
  return { intro, lessons };
}

/* ------------------------------------------------------------------ inputs */

/** Module titles + "the wall you hit" come from the README table. */
function readWalls(file) {
  const out = {};
  for (const line of fs.readFileSync(path.join(ROOT, file), 'utf8').split('\n')) {
    const m = line.match(/^\|\s*([F0-9]+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$/);
    if (m) out[m[1]] = { title: m[2].replace(/^(?:Part 0:|الجزء 0:)\s*/, ''), wall: m[3] };
  }
  return out;
}

function readGlossary(lang) {
  const md = fs.readFileSync(path.join(ROOT, lang === 'ar' ? 'GLOSSARY.ar.md' : 'GLOSSARY.md'), 'utf8');
  const [, title, rest] = md.match(/^#\s+(.+?)\n([\s\S]*)$/);
  return { title: title.trim(), html: render(rest.trim()) };
}

/* ----------------------------------------------------------------- mermaid */

async function renderDiagrams(sources) {
  if (!sources.length) return [];
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
  try {
    const page = await browser.newPage();
    await page.setContent('<!doctype html><html><body></body></html>');
    await page.addScriptTag({ path: path.join(ROOT, 'node_modules/mermaid/dist/mermaid.min.js') });
    return await page.evaluate(async (codes) => {
      /* Mermaid invents random ids (gitGraph commit hashes) and draws some
         shapes with rough.js, so an unseeded render differs byte-for-byte
         every run. Seed it so `npm run check` can compare builds. */
      let seed = 20260727;
      Math.random = () => {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        return seed / 2147483648;
      };
      window.mermaid.initialize({
        startOnLoad: false, theme: 'neutral', securityLevel: 'loose', look: 'classic',
        deterministicIds: true, deterministicIDSeed: 'sd4vc',
        fontFamily: 'ui-sans-serif, system-ui, -apple-system, sans-serif',
      });
      const out = [];
      for (let i = 0; i < codes.length; i++) {
        try {
          const { svg } = await window.mermaid.render('d' + i, codes[i]);
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

/* ------------------------------------------------------------- html pieces */

const CSS = () => fs.readFileSync(path.join(ROOT, 'scripts/style.css'), 'utf8');
const PRINT_CSS = () => fs.readFileSync(path.join(ROOT, 'scripts/print.css'), 'utf8');

/** Wrap a per-language pair for a page that carries one language or both. */
function block(parts, langs) {
  if (langs.length === 1) {
    return langs[0] === 'ar' ? `<div lang="ar" dir="rtl">${parts.ar}</div>` : parts.en;
  }
  return `<div class="en-only">${parts.en}</div>\n<div class="ar-only" lang="ar" dir="rtl">${parts.ar}</div>`;
}

function lessonArticle(lesson, langs) {
  const cls = langs.length === 1
    ? (lesson.lang === 'ar' ? 'lesson-full" lang="ar" dir="rtl' : 'lesson-full')
    : (lesson.lang === 'ar' ? 'lesson-full ar-only" lang="ar" dir="rtl' : 'lesson-full en-only');
  const kicker = lesson.kicker ? `<p class="kicker">${esc(lesson.kicker)}</p>` : '';
  const sections = splitSections(lesson.body).map((s) => renderSection(s, lesson.lang)).join('\n');
  return `<article class="${cls}">
${kicker}
<h2>${esc(lesson.num)} — ${esc(lesson.title)}</h2>
${sections}
</article>`;
}

function moduleDivider(mod, C, langs) {
  const parts = {};
  for (const lang of ['en', 'ar']) {
    const w = C.walls[lang][mod.key];
    const intro = C[lang][mod.key].intro;
    parts[lang] = `<p class="eyebrow">${T[lang].modWord(mod.key)}</p><h2>${esc(w.title)}</h2>` +
      (intro ? `<div class="mod-intro">${intro.html}</div>` : '');
  }
  return `<section class="mod-div" id="m${mod.key}"><div class="wrap">
${block(parts, langs)}
</div></section>`;
}

function tocFor(C, langs) {
  return MODULES.map((mod) => {
    const items = C.en[mod.key].lessons.map((l, i) => {
      const arL = C.ar[mod.key].lessons[i] || l;
      const titles = langs.length === 1
        ? esc(langs[0] === 'ar' ? arL.title : l.title)
        : `<span class="en-only">${esc(l.title)}</span><span class="ar-only" lang="ar" dir="rtl">${esc(arL.title)}</span>`;
      return `<li><a href="#${anchor(l.num)}"><span class="lno">${esc(l.num)}</span>${titles}</a></li>`;
    }).join('');
    const heads = {};
    for (const lang of ['en', 'ar']) {
      const w = C.walls[lang][mod.key];
      heads[lang] = `${esc(w.title)}<span class="twall">${esc(w.wall)}</span>`;
    }
    const summary = langs.length === 1
      ? (langs[0] === 'ar' ? `<span lang="ar" dir="rtl">${heads.ar}</span>` : heads.en)
      : `<span class="en-only">${heads.en}</span>\n<span class="ar-only" lang="ar" dir="rtl">${heads.ar}</span>`;
    return `<details class="toc-mod" id="t${mod.key}">
<summary><span class="tnum">${mod.key}</span><span class="ttl">
${summary}
</span></summary><ol class="toc-lessons">${items}</ol></details>`;
  }).join('\n');
}

function heroFor(C, langs) {
  const parts = {};
  for (const lang of ['en', 'ar']) {
    const t = T[lang];
    const stats = [MODULES.length, C.lessonCount, 2, C.diagramCount]
      .map((v, i) => `<div><b>${v}</b><span>${t.stats[i]}</span></div>`).join('');
    const eyebrow = langs.length > 1
      ? (lang === 'en' ? 'The complete course · Bilingual · English / العربية' : 'الدورة كاملة · بلغتين · English / العربية')
      : t.eyebrow;
    parts[lang] = `<p class="eyebrow">${eyebrow}</p>
  <h1>${esc(t.title)}</h1>
  <p>${t.blurb}</p>
  <div class="stats">${stats}</div>`;
  }
  return block(parts, langs);
}

const docShell = ({ lang, dir, title, css, body, scripts = '' }) => `<!doctype html>
<html lang="${lang}"${dir ? ` dir="${dir}"` : ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title>
<style>
${css}
</style>
</head>
<body>
${body}
${scripts}
</body>
</html>
`;

/* --------------------------------------------------------- the reading app */

function appPage(C, langs) {
  const bilingual = langs.length > 1;
  const primary = bilingual ? 'en' : langs[0];

  const chips = [...MODULES.map((m) => `<a class="chip" href="#m${m.key}">${m.key}</a>`),
    '<a class="chip" href="#glossary" title="Glossary">📖</a>'].join('');

  const templates = MODULES.map((mod) => {
    const lessons = C.en[mod.key].lessons.map((l, i) => {
      const arL = C.ar[mod.key].lessons[i] || l;
      const articles = bilingual
        ? `${lessonArticle(l, langs)}\n${lessonArticle(arL, langs)}`
        : lessonArticle(primary === 'ar' ? arL : l, langs);
      return `<section class="lpair" id="${anchor(l.num)}">\n${articles}\n</section>`;
    }).join('\n');
    return `<template id="tpl-${mod.key}">${moduleDivider(mod, C, langs)}<div class="wrap">\n${lessons}\n</div></template>`;
  }).join('\n');

  const l2m = {};
  MODULES.forEach((mod) => C.en[mod.key].lessons.forEach((l) => { l2m[anchor(l.num)] = mod.key; }));

  const gloss = block({
    en: `<p class="eyebrow">${T.en.appendix}</p><h2>${esc(C.gloss.en.title)}</h2>${C.gloss.en.html}`,
    ar: `<p class="eyebrow">${T.ar.appendix}</p><h2>${esc(C.gloss.ar.title)}</h2>${C.gloss.ar.html}`,
  }, langs);

  const mapLabel = bilingual
    ? '<span class="en-only">Map</span><span class="ar-only" lang="ar">الخريطة</span>'
    : esc(T[primary].map);
  const langBtn = bilingual ? '\n  <button class="lang-btn" id="langBtn" type="button">عربي</button>' : '';

  const mapHead = bilingual
    ? `<h2 class="en-only">Course map</h2><h2 class="ar-only" lang="ar" dir="rtl">خريطة الدورة</h2>
<p class="en-only" style="color:var(--muted)">${T.en.mapBlurb}</p>
<p class="ar-only" lang="ar" dir="rtl" style="color:var(--muted)">${T.ar.mapBlurb}</p>`
    : `<h2>${esc(T[primary].mapTitle)}</h2>\n<p style="color:var(--muted)">${T[primary].mapBlurb}</p>`;

  const otherEditions = bilingual ? '' :
    `<p class="build-note">${primary === 'en'
      ? '<a href="index.ar.html">العربية</a> · <a href="index.html">Bilingual</a>'
      : '<a href="index.en.html">English</a> · <a href="index.html">نسخة بلغتين</a>'}</p>`;

  const body = `<header class="masthead"><div class="wrap">
  <a class="brand" href="#top">SD4VC</a>
  <div class="chips">${chips}</div>
  <nav><a href="#map">${mapLabel}</a>${langBtn}</nav>
</div></header>
<section class="hero" id="top"><div class="wrap">
${heroFor(C, langs)}
${otherEditions}
</div></section>
<section class="map" id="map"><div class="wrap">
${mapHead}
${tocFor(C, langs)}
</div></section>
<main id="view"></main>
${templates}
<template id="tpl-glossary"><section class="appendix" id="glossary"><div class="wrap">
${gloss}
</div></section></template>
<footer><div class="wrap">
${block({
    en: `<p>Generated from the module markdown by <code>npm run build</code> — the markdown is the source of truth.
     Source: <a href="https://github.com/Tamoura/system-design-for-vibe-coders">github.com/Tamoura/system-design-for-vibe-coders</a></p>`,
    ar: `<p>مولَّدة من ملفات الماركداون عبر <code>npm run build</code> — والماركداون هو مصدر الحقيقة.
     المصدر: <a href="https://github.com/Tamoura/system-design-for-vibe-coders">github.com/Tamoura/system-design-for-vibe-coders</a></p>`,
  }, langs)}
</div></footer>`;

  const langScript = bilingual ? `<script>
(function(){
  var btn=document.getElementById('langBtn');
  function setLang(l){
    var ar=l==='ar';
    document.body.classList.toggle('lang-ar',ar);
    btn.textContent=ar?'English':'عربي';
    try{localStorage.setItem('sd4vc-lang',l);}catch(e){}
  }
  btn.addEventListener('click',function(){
    setLang(document.body.classList.contains('lang-ar')?'en':'ar');
  });
  var saved='en';
  try{saved=localStorage.getItem('sd4vc-lang')||'en';}catch(e){}
  setLang(saved);
})();
</script>
` : '';

  const navScript = `<script>
(function(){
  var view=document.getElementById('view');
  var L2M=${JSON.stringify(l2m)};
  function stamp(key){
    var t=document.getElementById('tpl-'+key);
    if(!t) return false;
    view.innerHTML='';
    view.appendChild(t.content.cloneNode(true));
    return true;
  }
  function go(el){
    if(!el) return;
    requestAnimationFrame(function(){
      requestAnimationFrame(function(){ el.scrollIntoView({behavior:'instant',block:'start'}); });
    });
  }
  function apply(h){
    if(!h||h==='top'||h==='map'){
      view.innerHTML='';
      if(h==='map') go(document.getElementById('map')); else window.scrollTo(0,0);
      return;
    }
    if(h==='glossary'){ if(stamp('glossary')) go(view); return; }
    if(h.charAt(0)==='m'&&document.getElementById('tpl-'+h.slice(1))){ stamp(h.slice(1)); go(view); return; }
    if(L2M[h]){ stamp(L2M[h]); go(document.getElementById(h)); }
  }
  document.addEventListener('click',function(e){
    var a=e.target&&e.target.closest&&e.target.closest('a[href^="#"]');
    if(!a) return;
    e.preventDefault();
    var h=decodeURIComponent(a.getAttribute('href').slice(1));
    apply(h);
    try{history.replaceState(null,'','#'+h);}catch(err){}
  });
  window.addEventListener('hashchange',function(){ apply(decodeURIComponent(location.hash.slice(1))); });
  apply(decodeURIComponent(location.hash.slice(1)));
})();
</script>`;

  // Diagrams are inlined later, once every page has registered its placeholders.
  return docShell({
    lang: primary,
    dir: !bilingual && T[primary].dir === 'rtl' ? 'rtl' : '',
    title: bilingual ? `${T.en.title} — The Complete Course` : T[primary].title,
    css: CSS(),
    body,
    scripts: langScript + navScript,
  });
}

/* -------------------------------------------------------- the printed book */

/** Everything inline, in reading order — the source document for the PDF. */
function flatPage(C, lang) {
  const t = T[lang];
  const langs = [lang];

  const contents = MODULES.map((mod) => {
    const w = C.walls[lang][mod.key];
    const items = C[lang][mod.key].lessons
      .map((l) => `<li><span class="lno">${esc(l.num)}</span> ${esc(l.title)}</li>`).join('');
    return `<li class="toc-m"><b>${mod.key} · ${esc(w.title)}</b><ol>${items}</ol></li>`;
  }).join('');

  const chapters = MODULES.map((mod) => {
    const lessons = C[lang][mod.key].lessons
      .map((l) => `<section class="lpair" id="${anchor(l.num)}">${lessonArticle(l, langs)}</section>`).join('\n');
    return `${moduleDivider(mod, C, langs)}<div class="wrap">\n${lessons}\n</div>`;
  }).join('\n');

  const body = `<section class="hero titlepage"><div class="wrap">
${heroFor(C, langs)}
</div></section>
<section class="print-toc"><div class="wrap"><h2>${esc(t.contents)}</h2><ol class="toc-book">${contents}</ol></div></section>
${chapters}
<section class="appendix" id="glossary"><div class="wrap">
<p class="eyebrow">${esc(t.appendix)}</p><h2>${esc(C.gloss[lang].title)}</h2>
${C.gloss[lang].html}
</div></section>`;

  return docShell({
    lang, dir: t.dir === 'rtl' ? 'rtl' : '',
    title: t.title, css: CSS() + '\n' + PRINT_CSS(), body,
  });
}

async function writePdf(C, lang) {
  const html = inlineDiagrams(flatPage(C, lang));
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
  try {
    const page = await browser.newPage();
    await page.setContent(html, { waitUntil: 'load', timeout: 180000 });
    await page.emulateMediaType('print');
    const file = path.join(DIST, `course-${lang}.pdf`);
    await page.pdf({
      path: file, format: 'A4', printBackground: true, timeout: 600000,
      margin: { top: '16mm', bottom: '16mm', left: '15mm', right: '15mm' },
      displayHeaderFooter: true,
      headerTemplate: '<div></div>',
      footerTemplate: '<div style="width:100%;font-size:8px;color:#888;text-align:center;font-family:sans-serif"><span class="pageNumber"></span></div>',
    });
    return file;
  } finally {
    await browser.close();
  }
}

/* -------------------------------------------------------------------- epub */

const VOID = 'area|base|br|col|embed|hr|img|input|link|meta|param|source|track|wbr';

/** HTML -> well-formed XHTML (every EPUB document must parse as XML). */
function toXhtml(html) {
  return html
    .replace(new RegExp(`<(${VOID})((?:\\s[^>]*?)?)\\s*/?>`, 'gi'), (_, tag, attrs) => `<${tag}${attrs}/>`)
    .replace(/&nbsp;/g, '&#160;')
    .replace(/&mdash;/g, '&#8212;')
    .replace(/&ndash;/g, '&#8211;')
    .replace(/&hellip;/g, '&#8230;');
}

const xhtmlDoc = (lang, dir, title, body) => `<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="${lang}" xml:lang="${lang}"${dir ? ` dir="${dir}"` : ''}>
<head><meta charset="utf-8"/><title>${esc(title)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
${body}
</body>
</html>
`;

function epubDocs(C, lang) {
  const t = T[lang];
  const dir = t.dir === 'rtl' ? 'rtl' : '';
  const docs = [];

  docs.push({
    id: 'titlepage', file: 'titlepage.xhtml', title: t.title,
    xhtml: xhtmlDoc(lang, dir, t.title, toXhtml(
      `<section class="titlepage"><h1>${esc(t.title)}</h1><p>${t.blurb}</p></section>`)),
  });

  for (const mod of MODULES) {
    const w = C.walls[lang][mod.key];
    const intro = C[lang][mod.key].intro;
    docs.push({
      id: `m${mod.key.replace('.', '')}`, file: `m${mod.key}.xhtml`, title: `${t.modWord(mod.key)} — ${w.title}`,
      xhtml: xhtmlDoc(lang, dir, w.title, toXhtml(inlineDiagrams(
        `<section class="mod-div"><p class="eyebrow">${t.modWord(mod.key)}</p><h1>${esc(w.title)}</h1>` +
        `<p><i>${esc(w.wall)}</i></p>${intro ? `<div class="mod-intro">${intro.html}</div>` : ''}</section>`))),
    });
    for (const l of C[lang][mod.key].lessons) {
      docs.push({
        id: anchor(l.num), file: `${anchor(l.num)}.xhtml`, title: `${l.num} — ${l.title}`,
        xhtml: xhtmlDoc(lang, dir, `${l.num} — ${l.title}`,
          toXhtml(inlineDiagrams(lessonArticle(l, [lang])))),
      });
    }
  }

  docs.push({
    id: 'glossary', file: 'glossary.xhtml', title: C.gloss[lang].title,
    xhtml: xhtmlDoc(lang, dir, C.gloss[lang].title, toXhtml(inlineDiagrams(
      `<section class="appendix"><h1>${esc(C.gloss[lang].title)}</h1>${C.gloss[lang].html}</section>`))),
  });

  const navItems = docs.filter((d) => d.id !== 'titlepage')
    .map((d) => `<li><a href="${d.file}">${esc(d.title)}</a></li>`).join('\n');
  docs.push({
    id: 'nav', file: 'nav.xhtml', title: t.contents, nav: true,
    xhtml: xhtmlDoc(lang, dir, t.contents,
      `<nav epub:type="toc" id="toc"><h1>${esc(t.contents)}</h1><ol>\n${navItems}\n</ol></nav>`),
  });

  return docs;
}

async function writeEpub(C, lang) {
  const t = T[lang];
  const docs = epubDocs(C, lang);
  const file = path.join(DIST, `course-${lang}.epub`);
  const spine = docs.filter((d) => !d.nav);

  const opf = `<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="${lang}"${t.dir === 'rtl' ? ' dir="rtl"' : ''}>
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="uid">urn:uuid:5d4bc5a0-0000-4000-8000-00000000${lang === 'en' ? '0001' : '0002'}</dc:identifier>
    <dc:title>${esc(t.title)}</dc:title>
    <dc:language>${lang}</dc:language>
    <dc:creator>Tamoura</dc:creator>
    <meta property="dcterms:modified">2026-07-28T00:00:00Z</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="css" href="style.css" media-type="text/css"/>
${spine.map((d) => `    <item id="${d.id}" href="${d.file}" media-type="application/xhtml+xml"/>`).join('\n')}
  </manifest>
  <spine${t.dir === 'rtl' ? ' page-progression-direction="rtl"' : ''}>
${spine.map((d) => `    <itemref idref="${d.id}"/>`).join('\n')}
  </spine>
</package>
`;

  const container = `<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
`;

  await new Promise((resolve, reject) => {
    const out = fs.createWriteStream(file);
    const zip = archiver('zip', { zlib: { level: 9 } });
    out.on('close', resolve);
    zip.on('error', reject);
    zip.pipe(out);
    const date = new Date('2026-07-28T00:00:00Z');   // fixed, so repeated builds match
    zip.append('application/epub+zip', { name: 'mimetype', store: true, date });
    zip.append(container, { name: 'META-INF/container.xml', date });
    zip.append(opf, { name: 'OEBPS/content.opf', date });
    zip.append(CSS() + '\n' + PRINT_CSS(), { name: 'OEBPS/style.css', date });
    for (const d of docs) zip.append(d.xhtml, { name: `OEBPS/${d.file}`, date });
    zip.finalize();
  });

  return { file, docs };
}

/** EPUB documents must be valid XML; parse them all before shipping. */
async function validateXhtml(docs, lang) {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
  try {
    const page = await browser.newPage();
    await page.setContent('<!doctype html><html><body></body></html>');
    return await page.evaluate((files) => {
      const bad = [];
      for (const f of files) {
        const doc = new DOMParser().parseFromString(f.xhtml, 'application/xml');
        const err = doc.querySelector('parsererror');
        if (err) bad.push({ file: f.file, error: err.textContent.replace(/\s+/g, ' ').slice(0, 180) });
      }
      return bad;
    }, docs.map((d) => ({ file: `${lang}/${d.file}`, xhtml: d.xhtml })));
  } finally {
    await browser.close();
  }
}

/* -------------------------------------------------------------------- main */

const C = { en: {}, ar: {}, walls: { en: readWalls('README.md'), ar: readWalls('README.ar.md') } };
for (const mod of MODULES) {
  C.en[mod.key] = parseModule(mod, 'en');
  C.ar[mod.key] = parseModule(mod, 'ar');
  const [e, a] = [C.en[mod.key].lessons.length, C.ar[mod.key].lessons.length];
  if (e !== a) throw new Error(`module ${mod.key}: ${e} English lessons but ${a} Arabic`);
}
C.gloss = { en: readGlossary('en'), ar: readGlossary('ar') };
C.lessonCount = MODULES.reduce((n, m) => n + C.en[m.key].lessons.length, 0);

/* Counted from the markdown rather than from diagramIds, because the hero is
   emitted before the lesson bodies have registered their own diagrams. */
C.diagramCount = MODULES.reduce((n, mod) => n + mod.files.reduce((m, f) => {
  const md = fs.readFileSync(path.join(ROOT, 'modules', mod.dir, f), 'utf8');
  return m + (md.match(/```mermaid/g) || []).length;
}, 0), 0);

/* Emit every page first so all placeholders exist, then render each distinct
   diagram once and inline the SVG into whichever outputs reference it. */
const pages = {
  'index.html': appPage(C, ['en', 'ar']),
  'index.en.html': appPage(C, ['en']),
  'index.ar.html': appPage(C, ['ar']),
};

SVGS = await renderDiagrams([...diagramIds.keys()]);
const failed = SVGS.map((s, i) => (typeof s === 'string' ? null : i)).filter((i) => i !== null);
if (failed.length) {
  console.error(`\n${failed.length} diagram(s) failed to render:`);
  for (const i of failed.slice(0, 5)) console.error(`  #${i}: ${SVGS[i].error}`);
}
for (const f of Object.keys(pages)) pages[f] = inlineDiagrams(pages[f]);

if (CHECK) {
  const stale = Object.keys(pages).filter((f) => {
    const p = path.join(ROOT, f);
    return !fs.existsSync(p) || fs.readFileSync(p, 'utf8') !== pages[f];
  });
  if (stale.length) {
    console.error(`out of date — run \`npm run build\`: ${stale.join(', ')}`);
    process.exit(1);
  }
  console.log('generated pages are up to date.');
} else {
  for (const [file, html] of Object.entries(pages)) {
    fs.writeFileSync(path.join(ROOT, file), html);
    console.log(`${file.padEnd(24)} ${(html.length / 1e6).toFixed(1)} MB`);
  }
  console.log(`${C.lessonCount} lessons × 2 languages · ${diagramIds.size} diagrams`);
}

if (WANT_PDF || WANT_EPUB) fs.mkdirSync(DIST, { recursive: true });

if (WANT_EPUB) {
  for (const lang of ['en', 'ar']) {
    const { file, docs } = await writeEpub(C, lang);
    const bad = await validateXhtml(docs, lang);
    if (bad.length) {
      console.error(`\n${bad.length} invalid XHTML document(s) in the ${lang} EPUB:`);
      for (const b of bad.slice(0, 5)) console.error(`  ${b.file}: ${b.error}`);
      process.exitCode = 1;
    }
    console.log(`${path.relative(ROOT, file).padEnd(24)} ${(fs.statSync(file).size / 1e6).toFixed(1)} MB · ${docs.length} documents${bad.length ? ' · INVALID XHTML' : ''}`);
  }
}

if (WANT_PDF) {
  for (const lang of ['en', 'ar']) {
    const file = await writePdf(C, lang);
    console.log(`${path.relative(ROOT, file).padEnd(24)} ${(fs.statSync(file).size / 1e6).toFixed(1)} MB`);
  }
}

if (failed.length) process.exit(1);
