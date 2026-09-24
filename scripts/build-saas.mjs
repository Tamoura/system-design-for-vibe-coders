#!/usr/bin/env node
/**
 * Build the "SaaS Building Blocks" course.
 *
 *   node scripts/build-saas.mjs           → saas/index.html (interactive reader),
 *                                           saas/course.html (the whole course, one flat page),
 *                                           saas/COURSE.md (the whole course, one markdown file),
 *                                           saas/REPOS.md (the repo catalog)
 *   node scripts/build-saas.mjs --check   → fail if the committed outputs are stale
 *
 * Sources: saas/README.md, saas/modules/NN-*.md. The markdown is the source of
 * truth; index.html and REPOS.md are generated — never edit them by hand.
 *
 * Module files look like:
 *   # Module 3 — Money
 *   *intro paragraph*
 *   ---
 *   # 3.1 — Lesson title
 *   *Level: 🟢 Beginner* · *Prerequisites: 1.2*
 *   ## 🧭 Why every SaaS has this
 *   …
 *
 * Mermaid blocks are pre-rendered to inline SVG with a headless browser, so the
 * page needs no network and no CDN. Set PUPPETEER_EXECUTABLE_PATH to use a
 * system Chromium instead of puppeteer's bundled one.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import puppeteer from 'puppeteer';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SAAS = path.join(ROOT, 'saas');
const MODULE_DIR = path.join(SAAS, 'modules');
const OUT_HTML = path.join(SAAS, 'index.html');
const OUT_REPOS = path.join(SAAS, 'REPOS.md');
const OUT_COURSE_MD = path.join(SAAS, 'COURSE.md');
const OUT_COURSE_HTML = path.join(SAAS, 'course.html');
const CHECK = process.argv.includes('--check');

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const slug = (num) => 'l' + num.replace('.', '-');

/* ------------------------------------------------------------------ sources */

const moduleFiles = fs.readdirSync(MODULE_DIR).filter((f) => /^\d\d-.+\.md$/.test(f) && !f.endsWith('.ar.md')).sort();
const SOURCE_FILES = [
  'saas/README.md',
  ...moduleFiles.map((f) => `saas/modules/${f}`),
  'scripts/build-saas.mjs',
  'scripts/saas.css',
];
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
  for (const f of [OUT_HTML, OUT_REPOS, OUT_COURSE_MD, OUT_COURSE_HTML]) {
    const txt = fs.existsSync(f) ? fs.readFileSync(f, 'utf8') : '';
    if (!txt.includes(`saas-source: ${SOURCE_DIGEST}`) && !txt.includes(`saas-source" content="${SOURCE_DIGEST}"`)) {
      stale.push(path.relative(ROOT, f));
    }
  }
  if (stale.length) {
    console.error(`✗ Stale SaaS course output: ${stale.join(', ')}\n  Run \`npm run saas:build\` and commit the result.`);
    process.exit(1);
  }
  console.log(`✓ SaaS course output matches its sources (${SOURCE_DIGEST}).`);
  process.exit(0);
}

/* ------------------------------------------------------------------- parse */

const MODULE_RE = /^# Module (\d+) — (.+)$/m;
const LESSON_RE = /^# (\d+\.\d+) — (.+)$/;
const LEVEL_RE = /^\*Level:\s*(🟢|🟡|🔴)\s*(Beginner|Intermediate|Advanced)\*(.*)$/;
const LEVELS = { Beginner: 'b', Intermediate: 'i', Advanced: 'a' };

function parseModule(file) {
  const md = fs.readFileSync(path.join(MODULE_DIR, file), 'utf8').replace(/\r\n/g, '\n');
  const m = md.match(MODULE_RE);
  if (!m) throw new Error(`${file}: first heading must be "# Module N — Title"`);
  const lines = md.split('\n');
  const lessons = [];
  let intro = [];
  let cur = null;
  let seenModule = false;
  for (const line of lines) {
    const lm = line.match(LESSON_RE);
    if (lm) {
      cur = { num: lm[1], title: lm[2].trim(), body: [], level: null, prereq: '' };
      lessons.push(cur);
      continue;
    }
    if (!seenModule && MODULE_RE.test(line)) { seenModule = true; continue; }
    if (cur) {
      if (!cur.level && !cur.body.some((l) => l.trim())) {
        const lv = line.trim().match(LEVEL_RE);
        if (lv) {
          cur.level = lv[2];
          const pre = lv[3].match(/Prerequisites?:\s*([^*]+)\*/);
          cur.prereq = pre ? pre[1].trim() : '';
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
    if (!l.level) throw new Error(`${file}: lesson ${l.num} is missing its "*Level: …*" line`);
    // Drop the trailing separator between lessons.
    l.body = l.body.join('\n').replace(/\n\s*---\s*$/g, '').trim();
  }
  intro = intro.join('\n').replace(/^\s*---\s*$/gm, '').trim();
  return { key: m[1], title: m[2].trim(), intro, lessons, file };
}

const MODULES = moduleFiles.map(parseModule);
const ALL_LESSONS = MODULES.flatMap((mod) => mod.lessons.map((l) => ({ ...l, mod })));

/* ------------------------------------------------------------ repo catalog */

const GH_RE = /\[([^\]]+)\]\(https:\/\/github\.com\/([\w.-]+\/[\w.-]+?)\/?\)/;

function repoRows(lesson) {
  const sec = lesson.body.split(/\n(?=## )/).find((s) => s.startsWith('## 🏆'));
  if (!sec) return [];
  const rows = [];
  for (const line of sec.split('\n')) {
    if (!line.startsWith('|')) continue;
    const cells = line.split('|').slice(1, -1).map((c) => c.trim());
    const gh = cells[0] && cells[0].match(GH_RE);
    if (!gh) continue;
    rows.push({ repo: gh[2], cells });
  }
  return rows;
}

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
  out.push('<!-- Generated by scripts/build-saas.mjs from the lessons\' "🏆 The best repos" tables. Do not edit by hand. -->');
  out.push(`<!-- saas-source: ${SOURCE_DIGEST} -->`);
  out.push('');
  out.push('# The Repo Catalog');
  out.push('');
  out.push(`Every repository recommended in **SaaS Building Blocks** — ${REPO_INDEX.size} of them — grouped by the`);
  out.push('component (lesson) that recommends it. Licenses change: check the repo\'s LICENSE file before');
  out.push('adopting anything. Run `npm run saas:repos` to check that every link still resolves.');
  out.push('');
  for (const mod of MODULES) {
    const entries = CATALOG.filter((c) => c.lesson.mod === mod);
    if (!entries.length) continue;
    out.push(`## Module ${mod.key} — ${mod.title}`);
    out.push('');
    for (const { lesson, rows } of entries) {
      out.push(`### ${lesson.num} — ${lesson.title}`);
      out.push('');
      out.push('| Repo | What it is | Stack | License | Pick it when |');
      out.push('|---|---|---|---|---|');
      for (const r of rows) out.push(`| ${r.cells.join(' | ')} |`);
      out.push('');
    }
  }
  out.push('## A–Z index');
  out.push('');
  const sorted = [...REPO_INDEX.values()].sort((a, b) => a.repo.toLowerCase().localeCompare(b.repo.toLowerCase()));
  for (const e of sorted) out.push(`- [${e.repo}](https://github.com/${e.repo}) — ${e.lessons.join(', ')}`);
  out.push('');
  return out.join('\n');
}


/* ------------------------------------------------------- whole-course .md */

/** Shift markdown headings down by `by` levels, leaving code blocks alone. */
function shiftHeadings(md, by) {
  let fence = false;
  return md.split('\n').map((line) => {
    if (/^```/.test(line)) fence = !fence;
    if (fence || !/^#{1,5} /.test(line)) return line;
    return '#'.repeat(by) + line;
  }).join('\n');
}

const MD_LINKS = (md) => md
  .replace(/\]\(\.\.?\/REPOS\.md\)/g, '](#appendix-the-repo-catalog)')
  .replace(/\]\(\.\.?\/(?:OUTLINE|README)\.md(?:#[\w-]+)?\)/g, '](#contents)');

function courseMarkdown() {
  const out = [];
  const readme = fs.readFileSync(path.join(SAAS, 'README.md'), 'utf8').replace(/^# .+\n/, '');
  out.push('<!-- Generated by scripts/build-saas.mjs from saas/README.md and saas/modules/*.md. Do not edit by hand. -->');
  out.push(`<!-- saas-source: ${SOURCE_DIGEST} -->`);
  out.push('');
  out.push('# SaaS Building Blocks — the complete course');
  out.push('');
  out.push(`*${MODULES.length} modules · ${ALL_LESSONS.length} lessons · ${REPO_INDEX.size} recommended repositories · beginner → advanced*`);
  out.push('');
  out.push(MD_LINKS(shiftHeadings(readme.trim(), 0)));
  out.push('');
  out.push('<a id="contents"></a>');
  out.push('');
  out.push('## Contents');
  out.push('');
  for (const mod of MODULES) {
    out.push(`- **[Module ${mod.key} — ${mod.title}](#m${mod.key})**`);
    for (const l of mod.lessons) out.push(`  - [${l.num} — ${l.title}](#${slug(l.num)}) · ${LEVEL_LABEL[l.level]}`);
  }
  out.push('- **[Appendix — The repo catalog](#appendix-the-repo-catalog)**');
  out.push('');
  for (const mod of MODULES) {
    out.push('---');
    out.push('');
    out.push(`<a id="m${mod.key}"></a>`);
    out.push('');
    out.push(`# Module ${mod.key} — ${mod.title}`);
    out.push('');
    if (mod.intro) { out.push(MD_LINKS(mod.intro)); out.push(''); }
    for (const l of mod.lessons) {
      out.push(`<a id="${slug(l.num)}"></a>`);
      out.push('');
      out.push(`## ${l.num} — ${l.title}`);
      out.push('');
      out.push(`*Level: ${LEVEL_LABEL[l.level]}*${l.prereq ? ` · *Prerequisites: ${l.prereq}*` : ''}`);
      out.push('');
      out.push(MD_LINKS(shiftHeadings(l.body, 1)));
      out.push('');
    }
  }
  out.push('---');
  out.push('');
  out.push('<a id="appendix-the-repo-catalog"></a>');
  out.push('');
  out.push('# Appendix — The repo catalog');
  out.push('');
  const catalog = reposMarkdown().split('\n').filter((l) => !l.startsWith('<!--')).join('\n')
    .replace(/^# The Repo Catalog\n/m, '');
  out.push(shiftHeadings(catalog.trim(), 0));
  out.push('');
  return out.join('\n');
}

/* ----------------------------------------------------------------- render */

const diagrams = [];
marked.use({
  gfm: true,
  renderer: {
    code({ text, lang }) {
      if ((lang || '').trim() === 'mermaid') {
        diagrams.push(text);
        return `<div class="diagram"><!--DIAGRAM:${diagrams.length - 1}--></div>`;
      }
      return false;
    },
  },
});

const SECTION_CLASS = {
  '🧭': 'why', '📐': 'how', '🏆': 'repos', '🔍': 'wild', '🛠️': 'build', '🛠': 'build',
  '⚠️': 'mistakes', '⚠': 'mistakes', '🧾': 'recap', '📚': 'refs',
};

/** Link "(3.2)" and "lesson 3.2" style references to the lesson, in text only. */
const LESSON_NUMS = new Set(ALL_LESSONS.map((l) => l.num));
const XREF_RE = /(\(|\b[Ll]essons? |\b[Ss]ee )(\d+\.\d+)(?![\d.]*\d)/g;
function linkLessons(html) {
  let skip = 0; // depth inside <a>, <code>, <pre>, <svg>, headings
  return html.split(/(<[^>]+>)/).map((part) => {
    const tag = part.match(/^<(\/?)(a|code|pre|svg|h[1-6])\b/i);
    if (tag) { skip += tag[1] ? -1 : 1; return part; }
    if (part.startsWith('<') || skip > 0) return part;
    return part.replace(XREF_RE, (m, pre, n) => (LESSON_NUMS.has(n) ? `${pre}<a class="xref" href="#/${n}">${n}</a>` : m));
  }).join('');
}

const tableWrap = (html) => html.replace(/<table>/g, '<div class="table-scroll"><table>').replace(/<\/table>/g, '</table></div>');

function renderLesson(l) {
  const parts = l.body.split(/\n(?=## )/);
  const html = parts.map((p) => {
    const h = p.match(/^## (\S+)/);
    const cls = h ? (SECTION_CLASS[h[1]] || SECTION_CLASS[h[1].replace(/️/g, '')] || 'plain') : 'lead';
    const md = p.replace(/\]\(\.\.\/REPOS\.md\)/g, '](#/repos)').replace(/\]\(\.\.\/(?:OUTLINE|README)\.md\)/g, '](#/map)');
    const inner = linkLessons(tableWrap(marked.parse(md)));
    return `<section class="sec sec-${cls}">${inner}</section>`;
  }).join('\n');
  return html;
}

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
        deterministicIds: true, deterministicIDSeed: 'saas',
        fontFamily: 'ui-sans-serif, system-ui, -apple-system, sans-serif',
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

/* ------------------------------------------------------------------- page */

const LEVEL_LABEL = { Beginner: '🟢 Beginner', Intermediate: '🟡 Intermediate', Advanced: '🔴 Advanced' };

function lessonInner(l) {
  const prereq = l.prereq
    ? ` · <span class="prereq">Before this: ${l.prereq.split(/,\s*/).map((n) => LESSON_NUMS.has(n) ? `<a href="#/${n}">${n}</a>` : esc(n)).join(', ')}</span>`
    : '';
  return `<p class="crumb"><a href="#/map">Module ${esc(l.mod.key)} — ${esc(l.mod.title)}</a></p>
<h1><span class="num">${esc(l.num)}</span> ${esc(l.title)}</h1>
<p class="meta"><span class="lvl lvl-${LEVELS[l.level]}">${LEVEL_LABEL[l.level]}</span>${prereq}</p>
${l.html}`;
}

function lessonTemplate(l, i) {
  const prev = ALL_LESSONS[i - 1];
  const next = ALL_LESSONS[i + 1];
  const nav = `<nav class="pager">
  ${prev ? `<a href="#/${prev.num}" class="prev"><span>← Previous</span>${esc(prev.num)} ${esc(prev.title)}</a>` : '<span></span>'}
  ${next ? `<a href="#/${next.num}" class="next"><span>Next →</span>${esc(next.num)} ${esc(next.title)}</a>` : '<a href="#/repos" class="next"><span>Appendix →</span>The repo catalog</a>'}
</nav>`;
  return `<template id="t-${slug(l.num)}"><article class="lesson" data-level="${LEVELS[l.level]}">
${lessonInner(l)}
${nav}
</article></template>`;
}

function mapHtml() {
  return MODULES.map((mod) => `<section class="mod" id="m${esc(mod.key)}">
  <div class="mod-head"><span class="mod-num">${esc(mod.key)}</span><h3>${esc(mod.title)}</h3></div>
  ${mod.intro ? `<div class="mod-intro">${marked.parse(mod.intro)}</div>` : ''}
  <ol class="lessons">
    ${mod.lessons.map((l) => `<li data-level="${LEVELS[l.level]}"><a href="#/${l.num}"><span class="num">${esc(l.num)}</span><span class="t">${esc(l.title)}</span><span class="dot lvl-${LEVELS[l.level]}" title="${l.level}"></span></a></li>`).join('\n    ')}
  </ol>
</section>`).join('\n');
}

function catalogHtml() {
  const blocks = CATALOG.map(({ lesson, rows }) => `<section class="cat" data-level="${LEVELS[lesson.level]}">
<h3><a href="#/${lesson.num}">${esc(lesson.num)} — ${esc(lesson.title)}</a></h3>
<div class="table-scroll"><table><thead><tr><th>Repo</th><th>What it is</th><th>Stack</th><th>License</th><th>Pick it when</th></tr></thead><tbody>
${rows.map((r) => `<tr data-q="${esc(r.cells.join(' ').toLowerCase())}">${r.cells.map((c) => `<td>${marked.parseInline(c)}</td>`).join('')}</tr>`).join('\n')}
</tbody></table></div></section>`).join('\n');
  return `<div class="cat-tools"><input id="repoFilter" type="search" placeholder="Filter ${REPO_INDEX.size} repos — try &quot;postgres&quot;, &quot;MIT&quot;, &quot;go&quot;…" aria-label="Filter repositories"></div>\n${blocks}`;
}

function readmeHtml() {
  const md = fs.readFileSync(path.join(SAAS, 'README.md'), 'utf8')
    .replace(/^# .+\n/, '') // the page has its own hero
    .replace(/\]\(\.\/OUTLINE\.md\)/g, '](#/map)')
    .replace(/\]\(\.\/REPOS\.md\)/g, '](#/repos)');
  return linkLessons(tableWrap(marked.parse(md)));
}

function page(svgs) {
  const fill = (html) => html.replace(/<!--DIAGRAM:(\d+)-->/g, (_, i) => svgs[+i]);
  const lessonCount = ALL_LESSONS.length;
  const css = fs.readFileSync(path.join(ROOT, 'scripts/saas.css'), 'utf8');
  const count = (lv) => ALL_LESSONS.filter((l) => l.level === lv).length;
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="saas-source" content="${SOURCE_DIGEST}">
<meta name="description" content="SaaS Building Blocks — the ~25 components every SaaS shares, taught beginner to advanced, with the best open-source repos to learn each one from.">
<title>SaaS Building Blocks</title>
<style>
${css}
</style>
</head>
<body>
<header class="top"><div class="bar">
  <a class="brand" href="#/">SaaS <b>Building Blocks</b></a>
  <nav>
    <a href="#/map">Map</a>
    <a href="#/about">Start here</a>
    <a href="#/repos">Repos</a>
    <a href="course.html" title="The whole course on one printable page">One page</a>
    <button id="themeBtn" type="button" aria-label="Toggle dark mode">◐</button>
  </nav>
</div></header>

<main id="view" tabindex="-1"></main>

<template id="t-home">
<section class="hero">
  <p class="eyebrow">A course for junior developers · beginner → advanced</p>
  <h1>Every SaaS is the <em>same app</em> wearing a different product.</h1>
  <p class="lede">Auth, organizations, billing, email, jobs, permissions, webhooks, audit logs, SSO… Learn the ~25 components every SaaS shares, once — and learn them from the best open-source code on the planet.</p>
  <div class="stats">
    <div><b>${MODULES.length}</b>modules</div>
    <div><b>${lessonCount}</b>lessons</div>
    <div><b>${REPO_INDEX.size}</b>repos</div>
    <div><b>1</b>product built: Beacon</div>
  </div>
  <div class="cta"><a class="btn" href="#/0.1">Start with lesson 0.1 →</a><a class="btn ghost" href="#/about">How the course works</a></div>
</section>
<section class="tracks">
  <a href="#/map" data-track="b" class="track t-b"><span class="lvl lvl-b">🟢 Beginner track</span><b>${count('Beginner')} lesson${count('Beginner') === 1 ? '' : 's'}</b><span>Ship a SaaS v1: auth, orgs, data, files, payments, email, the app shell.</span></a>
  <a href="#/map" data-track="i" class="track t-i"><span class="lvl lvl-i">🟡 Intermediate track</span><b>${count('Intermediate')} lesson${count('Intermediate') === 1 ? '' : 's'}</b><span>Survive real customers: permissions, jobs, APIs, webhooks, flags, analytics, ops.</span></a>
  <a href="#/map" data-track="a" class="track t-a"><span class="lvl lvl-a">🔴 Advanced track</span><b>${count('Advanced')} lesson${count('Advanced') === 1 ? '' : 's'}</b><span>Win enterprise deals and scale: SSO/SCIM, tenancy, metering, realtime, compliance, AI.</span></a>
</section>
<section class="home-map"><h2>Course map</h2>${mapHtml()}</section>
</template>

<template id="t-map">
<section class="page">
  <h1>Course map</h1>
  <p class="lede">Every lesson climbs the same ladder — 🟢 essentials → 🟡 going deeper → 🔴 at scale. The dot shows where each lesson <em>starts</em>.</p>
  <div class="filters" role="group" aria-label="Filter by level">
    <button data-f="all" class="on">All</button><button data-f="b">🟢 Beginner</button><button data-f="i">🟡 Intermediate</button><button data-f="a">🔴 Advanced</button>
  </div>
  ${mapHtml()}
</section>
</template>

<template id="t-about"><section class="page prose">
<h1>Start here</h1>
${readmeHtml()}
</section></template>

<template id="t-repos"><section class="page">
<h1>The repo catalog</h1>
<p class="lede">Every repository the course recommends, grouped by component. Licenses change — read the LICENSE file before adopting anything.</p>
${catalogHtml()}
</section></template>

${fill(ALL_LESSONS.map(lessonTemplate).join('\n'))}

<footer><p>Part of the <a href="../">Course Library</a>. Generated from the markdown in <code>saas/</code> by <code>npm run saas:build</code>. Source: <a href="https://github.com/Tamoura/system-design-for-vibe-coders/tree/main/saas">github.com/Tamoura/system-design-for-vibe-coders</a></p></footer>

<script>
(function(){
  var root=document.documentElement, view=document.getElementById('view');
  try{var t=localStorage.getItem('saas-theme'); if(t) root.setAttribute('data-theme',t);}catch(e){}
  document.getElementById('themeBtn').addEventListener('click',function(){
    var dark=root.getAttribute('data-theme')==='dark'||(!root.getAttribute('data-theme')&&matchMedia('(prefers-color-scheme: dark)').matches);
    var next=dark?'light':'dark'; root.setAttribute('data-theme',next);
    try{localStorage.setItem('saas-theme',next);}catch(e){}
  });
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
    document.title = (tpl.id.indexOf('t-l')===0 ? view.querySelector('h1').textContent.trim()+' · ' : '') + 'SaaS Building Blocks';
    view.querySelectorAll('.filters button').forEach(function(b){b.addEventListener('click',function(){filter=b.dataset.f;applyFilter();try{sessionStorage.setItem('saas-filter',filter);}catch(e){}});});
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
  try{filter=sessionStorage.getItem('saas-filter')||'all';}catch(e){}
  window.addEventListener('hashchange',route); route();
})();
</script>
</body>
</html>
`;
}


/* ------------------------------------------------ whole-course flat page */

/** Point the reader's "#/x" routes at in-page anchors. */
const flatLinks = (html) => html
  .replace(/href="#\/(\d+)\.(\d+)"/g, 'href="#l$1-$2"')
  .replace(/href="#\/repos"/g, 'href="#repos"')
  .replace(/href="#\/map"/g, 'href="#contents"')
  .replace(/href="#\/about"/g, 'href="#start"')
  .replace(/href="#\/"/g, 'href="#top"');

function flatPage(svgs) {
  const fill = (html) => html.replace(/<!--DIAGRAM:(\d+)-->/g, (_, i) => svgs[+i]);
  const css = fs.readFileSync(path.join(ROOT, 'scripts/saas.css'), 'utf8');
  const modules = MODULES.map((mod) => `<section class="flat-mod" id="module-${esc(mod.key)}">
  <p class="eyebrow">Module ${esc(mod.key)}</p>
  <h1>${esc(mod.title)}</h1>
  ${mod.intro ? `<div class="mod-intro">${marked.parse(mod.intro)}</div>` : ''}
</section>
${ALL_LESSONS.filter((l) => l.mod === mod).map((l) => `<article class="lesson flat-lesson" id="${slug(l.num)}" data-level="${LEVELS[l.level]}">
${lessonInner(l)}
<p class="back"><a href="#contents">↑ Contents</a></p>
</article>`).join('\n')}`).join('\n');
  const body = `<header class="top"><div class="bar">
  <a class="brand" href="#top">SaaS <b>Building Blocks</b></a>
  <nav>
    <a href="#contents">Contents</a>
    <a href="#repos">Repos</a>
    <a href="index.html">Reader</a>
    <button id="themeBtn" type="button" aria-label="Toggle dark mode">◐</button>
  </nav>
</div></header>
<main id="top">
<section class="hero">
  <p class="eyebrow">The complete course · one page · print-friendly</p>
  <h1>SaaS Building Blocks: every SaaS is the <em>same app</em> wearing a different product.</h1>
  <div class="stats">
    <div><b>${MODULES.length}</b>modules</div>
    <div><b>${ALL_LESSONS.length}</b>lessons</div>
    <div><b>${REPO_INDEX.size}</b>repos</div>
  </div>
</section>
<section class="page prose" id="start">
<h1>Start here</h1>
${readmeHtml()}
</section>
<section class="page" id="contents">
  <h1>Contents</h1>
  <div class="filters" role="group" aria-label="Filter by level">
    <button data-f="all" class="on">All</button><button data-f="b">🟢 Beginner</button><button data-f="i">🟡 Intermediate</button><button data-f="a">🔴 Advanced</button>
  </div>
  ${mapHtml()}
</section>
${modules}
<section class="page" id="repos">
<h1>Appendix — The repo catalog</h1>
<p class="lede">Every repository the course recommends, grouped by component. Licenses change — read the LICENSE file before adopting anything.</p>
${catalogHtml()}
</section>
</main>
<footer><p>Generated from the markdown in <code>saas/</code> by <code>npm run saas:build</code>. Prefer one lesson at a time? Open the <a href="index.html">interactive reader</a>.</p></footer>`;
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="saas-source" content="${SOURCE_DIGEST}">
<meta name="description" content="SaaS Building Blocks — the complete course on one page.">
<title>SaaS Building Blocks — Complete Course</title>
<style>
${css}
.flat-mod{padding:3.5rem 0 1rem;border-top:2px solid var(--line);margin-top:2rem}
.flat-mod h1{font-family:var(--serif);font-size:clamp(1.9rem,5vw,2.8rem);margin:.2rem 0 .6rem}
.flat-lesson{border-top:1px dashed var(--line);margin-top:1.5rem}
.back{font:600 .82rem var(--sans);text-align:right}
.back a{text-decoration:none}
@media print{.back,.filters,.cat-tools{display:none}.flat-mod,.flat-lesson{break-before:page;border:0}}
</style>
</head>
<body>
${fill(flatLinks(body))}
<script>
(function(){
  var root=document.documentElement;
  try{var t=localStorage.getItem('saas-theme'); if(t) root.setAttribute('data-theme',t);}catch(e){}
  document.getElementById('themeBtn').addEventListener('click',function(){
    var dark=root.getAttribute('data-theme')==='dark'||(!root.getAttribute('data-theme')&&matchMedia('(prefers-color-scheme: dark)').matches);
    var next=dark?'light':'dark'; root.setAttribute('data-theme',next);
    try{localStorage.setItem('saas-theme',next);}catch(e){}
  });
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

/* -------------------------------------------------------------------- main */

for (const l of ALL_LESSONS) l.html = renderLesson(l);
// Module intros and the README may also carry diagrams; render lessons first so
// diagram indices are stable, then everything else reuses the same list.
const svgs = await renderDiagrams(diagrams);
const failed = svgs.map((s, i) => (typeof s === 'string' ? null : i)).filter((i) => i !== null);
if (failed.length) {
  for (const i of failed) console.error(`✗ Mermaid diagram ${i} failed: ${svgs[i].error}\n---\n${diagrams[i]}\n---`);
  process.exit(1);
}
for (const l of ALL_LESSONS) {
  if (!/## 🏆/.test(l.body)) console.warn(`! ${l.num} has no "🏆 The best repos" section`);
}
fs.writeFileSync(OUT_HTML, page(svgs));
fs.writeFileSync(OUT_REPOS, reposMarkdown());
fs.writeFileSync(OUT_COURSE_HTML, flatPage(svgs));
fs.writeFileSync(OUT_COURSE_MD, courseMarkdown());
console.log(`✓ saas/index.html — ${MODULES.length} modules, ${ALL_LESSONS.length} lessons, ${diagrams.length} diagrams, ${REPO_INDEX.size} repos (${SOURCE_DIGEST})`);
console.log('✓ saas/course.html — the whole course on one page');
console.log('✓ saas/COURSE.md — the whole course in one markdown file');
console.log('✓ saas/REPOS.md');
