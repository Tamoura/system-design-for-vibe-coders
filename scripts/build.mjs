#!/usr/bin/env node
/**
 * Builds index.html — the whole bilingual course as one self-contained page —
 * from the module markdown.
 *
 * The markdown under modules/ is the source of truth. This script only renders
 * it, so nothing can drift: run `npm run build` after editing any lesson.
 * `npm run check` rebuilds in memory and fails if index.html is out of date.
 *
 * Mermaid diagrams are pre-rendered to inline SVG in a headless browser, so the
 * output page needs no network at runtime.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import puppeteer from 'puppeteer';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(ROOT, 'index.html');
const CHECK = process.argv.includes('--check');

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

const LESSON_RE = /^((?:F|\d+)\.\d+|12)\s+—\s+(.+)$/;
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/** Anchor for a lesson: "F.1" -> lF-1, "10.3" -> l10-3, "12" -> l12. */
const anchor = (num) => 'l' + num.replace('.', '-');

/* ---------------------------------------------------------------- markdown */

const diagrams = [];   // mermaid source, in document order; index === placeholder id

/** Links in the markdown are written for GitHub; retarget them for one page. */
function retargetLinks(md) {
  return md
    .replace(/\]\((?:\.\.\/)*\.?\/?GLOSSARY(?:\.ar)?\.md\)/g, '](#glossary)')
    .replace(/\]\((?:\.\.\/)+([^)]+)\)/g, ']($1)');
}

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
  const withPlaceholders = md.replace(/```mermaid\n([\s\S]*?)```/g, (_, code) => {
    const i = diagrams.push(code.trim()) - 1;
    return `\n<div data-diagram="${i}"></div>\n`;
  });
  let html = marked.parse(retargetLinks(withPlaceholders), { async: false, gfm: true, breaks: false });
  html = html.replace(/<(\/?)h([1-5])(\s[^>]*)?>/g, (_, slash, n, rest) => `<${slash}h${+n + 1}${rest || ''}>`);
  html = html.replace(/<table>/g, '<div class="table-scroll"><table>').replace(/<\/table>/g, '</table></div>');
  return html;
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
  const subtitle = m ? m[1].trim() : '';
  return `<h3 class="${pillar.cls}"><span class="tag">${esc(pillar.label[lang])}</span>${esc(subtitle)}</h3>\n${inner}`;
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
        // A leading *italic line* is the module kicker, not prose.
        let kicker = '';
        const k = body.match(/^\*([^*\n][^\n]*)\*\s*(?:\n|$)/);
        if (k) { kicker = k[1].trim(); body = trim(body.slice(k[0].length)); }
        lessons.push({ num: m[1], title: m[2].trim(), kicker, body });
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

/* -------------------------------------------------------------------- page */

const pair = (en, ar) =>
  `<div class="en-only">${en}</div>\n<div class="ar-only" lang="ar" dir="rtl">${ar}</div>`;

function lessonArticle(lesson, mod, walls, lang) {
  const kicker = lesson.kicker ? `<p class="kicker">${esc(lesson.kicker)}</p>` : '';
  const sections = splitSections(lesson.body).map((s) => renderSection(s, lang)).join('\n');
  const cls = lang === 'ar' ? 'lesson-full ar-only" lang="ar" dir="rtl' : 'lesson-full en-only';
  return `<article class="${cls}">
${kicker}
<h2>${esc(lesson.num)} — ${esc(lesson.title)}</h2>
${sections}
</article>`;
}

function build(en, ar, wallsEn, wallsAr, glossEn, glossAr) {
  const chips = [...MODULES.map((m) => `<a class="chip" href="#m${m.key}">${m.key}</a>`),
    '<a class="chip" href="#glossary" title="Glossary">📖</a>'].join('');

  const toc = MODULES.map((mod) => {
    const e = wallsEn[mod.key], a = wallsAr[mod.key];
    const items = en[mod.key].lessons.map((l, i) => {
      const arL = ar[mod.key].lessons[i];
      return `<li><a href="#${anchor(l.num)}"><span class="lno">${esc(l.num)}</span>` +
        `<span class="en-only">${esc(l.title)}</span>` +
        `<span class="ar-only" lang="ar" dir="rtl">${esc(arL ? arL.title : l.title)}</span></a></li>`;
    }).join('');
    return `<details class="toc-mod" id="t${mod.key}">
<summary><span class="tnum">${mod.key}</span><span class="ttl">
<span class="en-only">${esc(e.title)}<span class="twall">${esc(e.wall)}</span></span>
<span class="ar-only" lang="ar" dir="rtl">${esc(a.title)}<span class="twall">${esc(a.wall)}</span></span>
</span></summary><ol class="toc-lessons">${items}</ol></details>`;
  }).join('\n');

  const templates = MODULES.map((mod) => {
    const e = wallsEn[mod.key], a = wallsAr[mod.key];
    const divider = `<section class="mod-div" id="m${mod.key}"><div class="wrap">
${pair(
    `<p class="eyebrow">${mod.key === 'F' ? 'Part 0' : 'Module ' + mod.key}</p><h2>${esc(e.title)}</h2>` +
      (en[mod.key].intro ? `<div class="mod-intro">${en[mod.key].intro.html}</div>` : ''),
    `<p class="eyebrow">${mod.key === 'F' ? 'الجزء 0' : 'الوحدة ' + mod.key}</p><h2>${esc(a.title)}</h2>` +
      (ar[mod.key].intro ? `<div class="mod-intro">${ar[mod.key].intro.html}</div>` : ''))}
</div></section>`;

    const lessons = en[mod.key].lessons.map((l, i) => {
      const arL = ar[mod.key].lessons[i] || l;
      return `<section class="lpair" id="${anchor(l.num)}">
${lessonArticle(l, mod, wallsEn, 'en')}
${lessonArticle(arL, mod, wallsAr, 'ar')}
</section>`;
    }).join('\n');

    return `<template id="tpl-${mod.key}">${divider}<div class="wrap">
${lessons}
</div></template>`;
  }).join('\n');

  const l2m = {};
  MODULES.forEach((mod) => en[mod.key].lessons.forEach((l) => { l2m[anchor(l.num)] = mod.key; }));

  const lessonCount = MODULES.reduce((n, m) => n + en[m.key].lessons.length, 0);
  const diagramCount = diagrams.length / 2;   // every diagram exists in both languages

  return `<title>System Design for Vibe Coders — The Complete Course</title>
<style>
${fs.readFileSync(path.join(ROOT, 'scripts/style.css'), 'utf8')}
</style>
<header class="masthead"><div class="wrap">
  <a class="brand" href="#top">SD4VC</a>
  <div class="chips">${chips}</div>
  <nav><a href="#map"><span class="en-only">Map</span><span class="ar-only" lang="ar">الخريطة</span></a>
  <button class="lang-btn" id="langBtn" type="button">عربي</button></nav>
</div></header>
<section class="hero" id="top"><div class="wrap">
${pair(
    `<p class="eyebrow">The complete course · Bilingual · English / العربية</p>
  <h1>System Design for Vibe Coders</h1>
  <p>Production engineering for AI-assisted builders. Every lesson is anchored in a real
  incident — from a real product's war-story bank or a famous industry outage — then turned
  into a principle, literal prompts to give your agent, and an evidence checklist so you can
  verify the work without reading code.</p>
  <div class="stats"><div><b>${MODULES.length}</b><span>modules</span></div><div><b>${lessonCount}</b><span>lessons</span></div><div><b>2</b><span>languages</span></div><div><b>${diagramCount}</b><span>diagrams</span></div></div>`,
    `<p class="eyebrow">الدورة كاملة · بلغتين · English / العربية</p>
  <h1>تصميم الأنظمة لمبرمجي الفايب</h1>
  <p>هندسة الإنتاج لمن يبني بمساعدة الذكاء الاصطناعي. كل درس يبدأ من حادثة حقيقية — من بنك حوادث منتج حقيقي أو عطل صناعي شهير — ثم يتحول إلى مبدأ، وتعليمات حرفية توجّه بها وكيلك، وقائمة أدلة تتحقق بها من العمل دون قراءة كود.</p>
  <div class="stats"><div><b>${MODULES.length}</b><span>وحدة</span></div><div><b>${lessonCount}</b><span>درسًا</span></div><div><b>2</b><span>لغتان</span></div><div><b>${diagramCount}</b><span>مخططًا</span></div></div>`)}
</div></section>
<section class="map" id="map"><div class="wrap">
<h2 class="en-only">Course map</h2><h2 class="ar-only" lang="ar" dir="rtl">خريطة الدورة</h2>
<p class="en-only" style="color:var(--muted)">Fourteen modules, in the order a real product forces them on you. Click a module to see its lessons; click a lesson to jump to it.</p>
<p class="ar-only" lang="ar" dir="rtl" style="color:var(--muted)">أربع عشرة وحدة، بالترتيب الذي يفرضه المنتج الحقيقي. اضغط على الوحدة لترى دروسها، وعلى الدرس للانتقال إليه.</p>
${toc}
</div></section>
<main id="view"></main>
${templates}
<template id="tpl-glossary"><section class="appendix" id="glossary"><div class="wrap">
${pair(`<p class="eyebrow">Appendix</p><h2>${esc(glossEn.title)}</h2>${glossEn.html}`,
    `<p class="eyebrow">ملحق</p><h2>${esc(glossAr.title)}</h2>${glossAr.html}`)}
</div></section></template>
<footer><div class="wrap">
${pair(
    `<p>Generated from the module markdown by <code>npm run build</code> — the markdown is the source of truth.
     Source: <a href="https://github.com/Tamoura/system-design-for-vibe-coders">github.com/Tamoura/system-design-for-vibe-coders</a></p>`,
    `<p>مولَّدة من ملفات الماركداون عبر <code>npm run build</code> — والماركداون هو مصدر الحقيقة.
     المصدر: <a href="https://github.com/Tamoura/system-design-for-vibe-coders">github.com/Tamoura/system-design-for-vibe-coders</a></p>`)}
</div></footer>
<script>
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
<script>
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
</script>
`;
}

/* -------------------------------------------------------------------- main */

const en = {}, ar = {};
for (const mod of MODULES) {
  en[mod.key] = parseModule(mod, 'en');
  ar[mod.key] = parseModule(mod, 'ar');
  const [e, a] = [en[mod.key].lessons.length, ar[mod.key].lessons.length];
  if (e !== a) throw new Error(`module ${mod.key}: ${e} English lessons but ${a} Arabic`);
}

const glossEn = readGlossary('en');
const glossAr = readGlossary('ar');
let html = build(en, ar, readWalls('README.md'), readWalls('README.ar.md'), glossEn, glossAr);

const svgs = await renderDiagrams(diagrams);
const failed = [];
svgs.forEach((svg, i) => {
  const figure = typeof svg === 'string'
    ? `<figure class="diagram">${svg}</figure>`
    : `<figure class="diagram"><pre>${esc(diagrams[i])}</pre></figure>`;
  if (typeof svg !== 'string') failed.push({ i, error: svg.error });
  html = html.replace(`<div data-diagram="${i}"></div>`, () => figure);
});

const lessons = MODULES.reduce((n, m) => n + en[m.key].lessons.length, 0);
if (failed.length) {
  console.error(`\n${failed.length} diagram(s) failed to render:`);
  for (const f of failed.slice(0, 5)) console.error(`  #${f.i}: ${f.error}`);
}

if (CHECK) {
  const current = fs.existsSync(OUT) ? fs.readFileSync(OUT, 'utf8') : '';
  if (current !== html) {
    console.error('index.html is out of date — run `npm run build`.');
    process.exit(1);
  }
  console.log('index.html is up to date.');
} else {
  fs.writeFileSync(OUT, html);
  console.log(`index.html — ${lessons} lessons ×2 languages, ${diagrams.length} diagrams, ${(html.length / 1e6).toFixed(1)} MB`);
}
if (failed.length) process.exit(1);
