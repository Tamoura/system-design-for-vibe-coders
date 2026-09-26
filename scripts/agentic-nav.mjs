#!/usr/bin/env node
/**
 * Add site navigation to the agentic course pages in agentic/.
 *
 *   node scripts/agentic-nav.mjs          patch agentic/*.html in place
 *   node scripts/agentic-nav.mjs --check  exit 1 if any page is missing the current navigation
 *
 * The pages are generated in the AI-agents repo and copied here by scripts/sync-agentic.sh,
 * which runs this script after every sync, so the navigation survives a re-sync. It is
 * idempotent: everything it adds sits between AGX markers and is replaced on each run.
 *
 * What it adds:
 *   - a top bar on every page: back to the course library, and links between the program,
 *     curriculum, playbook, assessment and poster (the current page highlighted);
 *   - in the long pages' sidebar, every h3 (the curriculum's 33 modules) under its section;
 *   - the section you are reading highlighted in the sidebar, which keeps it in view;
 *   - on narrow screens, the contents as a slide-out drawer opened from the top bar instead
 *     of a 30-item list above the content, no sideways scrolling, and a back-to-top button.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR = path.join(ROOT, 'agentic');
const CHECK = process.argv.includes('--check');
const VERSION = 'agx-nav v4';

// [English page, English label, Arabic label]. Each page has an Arabic twin named *.ar.html.
const PAGES = [
  ['index.html', 'Program', 'البرنامج'],
  ['learning-path.html', 'Curriculum', 'المنهج'],
  ['production-playbook.html', 'Playbook', 'دليل التشغيل'],
  ['assessment.html', 'Assessment', 'التقييم'],
  ['on-ramp-poster.html', 'Poster', 'الملصق'],
];
const arOf = (f) => f.replace(/\.html$/, '.ar.html');
const FILES = PAGES.flatMap(([f]) => [f, arOf(f)]);
const isAr = (f) => f.endsWith('.ar.html');
const twin = (f) => (isAr(f) ? f.replace(/\.ar\.html$/, '.html') : arOf(f));

const text = (html) => html.replace(/<a class="anchor"[\s\S]*?<\/a>/g, '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
const strip = (s, a, b) => s.replace(new RegExp(`${a}[\\s\\S]*?${b}\\n?`, 'g'), '');

const CSS = `
/* ${VERSION}: navigation added by scripts/agentic-nav.mjs */
.agx-bar{position:sticky;top:0;z-index:50;display:flex;align-items:center;gap:.4rem;flex-wrap:wrap;
  padding:.5rem 1rem;background:color-mix(in srgb,var(--bg,#f7f6f2) 92%,transparent);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--line,#e4e0d8);font:600 .82rem/1.2 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.agx-bar a{color:var(--muted,#5b6470);text-decoration:none;padding:.35rem .6rem;border-radius:999px;white-space:nowrap}
.agx-bar a:hover{color:var(--ink,#1e232c);background:var(--accent-soft,#f4e4e6)}
.agx-bar a[aria-current=page]{color:#fff;background:var(--accent,#7a1f2b)}
.agx-bar .agx-home{color:var(--ink,#1e232c);margin-inline-end:.4rem}
.agx-bar .agx-lang{border:1px solid var(--line,#e4e0d8)}
[dir=rtl] .agx-bar{font-family:"Noto Sans Arabic","Segoe UI",Tahoma,sans-serif}
.agx-bar .agx-spacer{flex:1}
.agx-toc-btn{display:none;font:inherit;color:var(--ink,#1e232c);background:var(--panel,#fff);border:1px solid var(--line,#e4e0d8);
  border-radius:999px;padding:.35rem .75rem;cursor:pointer}
nav[aria-label="Table of contents"]{top:var(--agx-bar-h,44px) !important;height:calc(100vh - var(--agx-bar-h,44px)) !important}
.toc-d3>a{padding-block:.18rem !important;padding-inline:1.9rem .5rem !important;font-size:.84em;border-inline-start:2px solid var(--line,#e4e0d8);border-radius:0;margin-inline-start:.5rem}
nav[aria-label="Table of contents"] a.agx-active{color:var(--ink,#1e232c);background:var(--accent-soft,#f4e4e6);border-inline-start-color:var(--accent,#7a1f2b)}
main [id]{scroll-margin-top:calc(var(--agx-bar-h,44px) + 12px)}
.agx-top{position:fixed;inset-inline-end:1rem;bottom:1rem;z-index:40;display:none;width:2.6rem;height:2.6rem;border-radius:50%;
  border:1px solid var(--line,#e4e0d8);background:var(--panel,#fff);color:var(--ink,#1e232c);font-size:1.1rem;cursor:pointer;
  box-shadow:0 2px 8px rgba(0,0,0,.12)}
.agx-top.agx-show{display:block}
.agx-scrim{display:none}
@media (max-width:900px){
  .agx-toc-btn{display:inline-block}
  .agx-bar .agx-pages{order:3;width:100%;overflow-x:auto;display:flex;gap:.2rem;padding-top:.2rem;scrollbar-width:none}
  nav[aria-label="Table of contents"]{position:fixed !important;left:0;top:0 !important;bottom:0;height:100vh !important;
    width:min(86vw,340px);z-index:60;background:var(--bg,#f7f6f2);border-inline-end:1px solid var(--line,#e4e0d8) !important;
    border-bottom:none !important;transform:translateX(-105%);transition:transform .2s ease;overflow-y:auto}
  [dir=rtl] nav[aria-label="Table of contents"]{left:auto;right:0;transform:translateX(105%)}
  body.agx-open nav[aria-label="Table of contents"]{transform:none}
  body.agx-open .agx-scrim{display:block;position:fixed;inset:0;z-index:55;background:rgba(0,0,0,.35)}
  .layout{display:block !important}
  main{max-width:100% !important}
  body{overflow-wrap:anywhere}
  h1,h2,h3{white-space:normal !important}
  pre,table{display:block;max-width:100%;overflow-x:auto}
  img,svg{max-width:100%;height:auto}
}
@media print{.agx-bar,.agx-top,.agx-scrim{display:none !important}}
`;

const JS = `
(function(){
  var bar=document.querySelector('.agx-bar'); if(!bar) return;
  function barH(){document.documentElement.style.setProperty('--agx-bar-h',bar.offsetHeight+'px');}
  barH(); window.addEventListener('resize',barH);
  var nav=document.querySelector('nav[aria-label="Table of contents"]');
  var btn=document.querySelector('.agx-toc-btn'), scrim=document.querySelector('.agx-scrim');
  function close(){document.body.classList.remove('agx-open'); if(btn) btn.setAttribute('aria-expanded','false');}
  if(btn&&nav){btn.addEventListener('click',function(){var o=document.body.classList.toggle('agx-open');btn.setAttribute('aria-expanded',o?'true':'false');});
    nav.addEventListener('click',function(e){if(e.target.closest('a')) close();});
    if(scrim) scrim.addEventListener('click',close);
    document.addEventListener('keydown',function(e){if(e.key==='Escape') close();});}
  var top=document.querySelector('.agx-top');
  if(top) top.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});
  var links=nav?Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]')):[];
  var byId={}; links.forEach(function(a){byId[decodeURIComponent(a.getAttribute('href').slice(1))]=a;});
  var targets=links.map(function(a){return document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));}).filter(Boolean);
  var current=null, ticking=false;
  function update(){
    ticking=false;
    if(top) top.classList.toggle('agx-show',window.scrollY>900);
    if(!targets.length) return;
    var line=(bar.offsetHeight||44)+110, hit=null; // a heading within ~110px of the bar counts as "here"
    for(var i=0;i<targets.length;i++){ if(targets[i].getBoundingClientRect().top<=line) hit=targets[i]; else break; }
    var a=hit?byId[hit.id]:null;
    if(a!==current){ if(current) current.classList.remove('agx-active'); current=a;
      if(a){ a.classList.add('agx-active');
        var nr=nav.getBoundingClientRect(), ar=a.getBoundingClientRect();
        if(ar.top<nr.top+40||ar.bottom>nr.bottom-40) nav.scrollTop+=ar.top-nr.top-nr.height/3; } }
  }
  window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(update);}},{passive:true});
  update();
})();
`;

function topBar(file) {
  const hasToc = PAGES_WITH_TOC.has(file);
  const ar = isAr(file);
  const links = PAGES.map(([f, en, arLabel]) => {
    const target = ar ? arOf(f) : f;
    return `<a href="${target}"${target === file ? ' aria-current="page"' : ''}>${ar ? arLabel : en}</a>`;
  }).join('');
  const lang = fs.existsSync(path.join(DIR, twin(file)))
    ? `<a class="agx-lang" href="${twin(file)}" hreflang="${ar ? 'en' : 'ar'}" lang="${ar ? 'en' : 'ar'}">${ar ? 'English' : 'العربية'}</a>`
    : '';
  return `<!--AGX:bar-->
<header class="agx-bar" role="navigation" aria-label="${ar ? 'الدورة' : 'Course'}">
  <a class="agx-home" href="../">${ar ? '→ مكتبة الدورات' : '← Course library'}</a>
  ${hasToc ? `<button class="agx-toc-btn" type="button" aria-expanded="false">☰ ${ar ? 'المحتويات' : 'Contents'}</button>` : ''}
  <span class="agx-spacer"></span>
  <span class="agx-pages">${links}</span>
  ${lang}
</header>
${hasToc ? '<div class="agx-scrim"></div>' : ''}
<!--/AGX:bar-->
`;
}

let PAGES_WITH_TOC = new Set();

/** Put every h3 in the sidebar, under the h2 it belongs to. */
function addH3s(html) {
  const navStart = html.indexOf('<nav aria-label="Table of contents">');
  if (navStart === -1) return html;
  const navEnd = html.indexOf('</nav>', navStart);
  let nav = html.slice(navStart, navEnd).replace(/<li class="toc-d3">[\s\S]*?<\/li>\n?/g, '');
  const body = html.slice(navEnd);
  // Children of each h2, in document order.
  const kids = {};
  let parent = null;
  for (const m of body.matchAll(/<h([23]) id="([^"]+)"[^>]*>([\s\S]*?)<\/h\1>/g)) {
    if (m[1] === '2') { parent = m[2]; kids[parent] = []; }
    else if (parent) kids[parent].push(`<li class="toc-d3"><a href="#${m[2]}">${text(m[3])}</a></li>`); // already HTML: entities stay as they are
  }
  nav = nav.replace(/(<li class="toc-d\d"><a href="#([^"]+)">[\s\S]*?<\/a><\/li>)\n?/g, (li, whole, id) =>
    `${whole}\n${(kids[id] || []).join('\n')}${kids[id]?.length ? '\n' : ''}`);
  return html.slice(0, navStart) + nav + body;
}

function patch(file, html) {
  let s = strip(html, '<!--AGX:bar-->', '<!--/AGX:bar-->');
  s = strip(s, '<style id="agx-nav">', '</style>');
  s = strip(s, '<script id="agx-nav">', '</script>');
  s = s.replace(/<button class="agx-top"[^>]*>[^<]*<\/button>\n?/g, '');
  if (PAGES_WITH_TOC.has(file)) s = addH3s(s);
  s = s.replace('</head>', `<style id="agx-nav">${CSS}</style>\n</head>`);
  s = s.replace(/<body([^>]*)>\n?/, (m) => `${m.trimEnd()}\n${topBar(file)}`);
  s = s.replace('</body>', `<button class="agx-top" type="button" aria-label="${isAr(file) ? 'العودة إلى الأعلى' : 'Back to top'}">↑</button>\n<script id="agx-nav">${JS}</script>\n</body>`);
  return s;
}

let stale = 0;
for (const file of FILES) {
  const p = path.join(DIR, file);
  if (!fs.existsSync(p)) { if (!isAr(file)) console.warn(`! missing agentic/${file}`); continue; }
  const html = fs.readFileSync(p, 'utf8');
  if (html.includes('<nav aria-label="Table of contents">')) PAGES_WITH_TOC.add(file);
}
for (const file of FILES) {
  const p = path.join(DIR, file);
  if (!fs.existsSync(p)) continue;
  const html = fs.readFileSync(p, 'utf8');
  const out = patch(file, html);
  if (CHECK) {
    if (out !== html) { stale++; console.error(`✗ agentic/${file} needs navigation (run node scripts/agentic-nav.mjs)`); }
  } else {
    fs.writeFileSync(p, out);
    const d3 = (out.match(/class="toc-d3"/g) || []).length;
    console.log(`✓ agentic/${file}${d3 ? ` (${d3} sub-sections in the sidebar)` : ''}`);
  }
}
if (CHECK) {
  if (stale) process.exit(1);
  console.log('✓ agentic pages have navigation');
}
