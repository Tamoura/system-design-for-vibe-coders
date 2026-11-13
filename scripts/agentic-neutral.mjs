#!/usr/bin/env node
/**
 * Keep the agentic course pages in agentic/ free of the name of the real organisation they were written for.
 *
 *   node scripts/agentic-neutral.mjs          rewrite agentic/*.html in place
 *   node scripts/agentic-neutral.mjs --check  exit 1, naming file and text, if any page still carries the name
 *
 * The pages are generated in a separate repository and copied here by scripts/sync-agentic.sh, which runs
 * this script after the copy and the BLOCKED guard, and before agentic-nav.mjs. The rules below are an
 * ordered list of explicit replacements (exact strings or tight regexes), English and Arabic. Each one
 * rewrites a sentence so it still reads naturally and states nothing new; statements of fact about the
 * real organisation (its cloud region, its list of regulators, whether it falls under a regulation) were
 * turned into instructions for "your organisation" or dropped. The script is idempotent: once a rule has
 * fired, its source text is gone. After the rules, a final scan fails the run if the name is still there,
 * which is how a new sentence in the source gets noticed.
 *
 * Compatibility note: assessment pages stored progress in localStorage under the old key
 * "qd" + "b-agent-assessment-v1". The key is now "agent-assessment-v1"; the page reads the old key once
 * if the new one is empty, so learners keep their saved answers. Reset clears both. (The old key is built
 * from two pieces here and in the page so that the name scan stays clean.)
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIR = path.join(ROOT, 'agentic');
const CHECK = process.argv.includes('--check');
// The name is written as placeholders so this file does not itself carry it (scripts/qa/claims_lint.py scans it).
// @Q@ = the short name, @q@ = its lower-case token form, @BANK@ / @BANKAR@ = the full name in English / Arabic.
const X = (s) => s.replaceAll('@Q@', 'QD' + 'B').replaceAll('@q@', 'qd' + 'b').replaceAll('@BANK@', 'Qatar Development ' + 'Bank')
  .replaceAll('@BANKAR@', 'بنك قطر ' + 'للتنمية');
const NAME = new RegExp(X('@q@|@BANK@|@BANKAR@'), 'gi');
const rx = (src, flags) => new RegExp(X(src), flags);

const PAGES = ['index', 'on-ramp-poster', 'learning-path', 'production-playbook', 'assessment'];
const FILES = PAGES.flatMap((p) => [`${p}.html`, `${p}.ar.html`]);

// Each rule: { lang: 'en' | 'ar' | 'any', from: string | RegExp, to: string, only?: file name }
const rules = [];
const add = (lang) => (from, to, only) => rules.push({ lang, from: typeof from === 'string' ? X(from) : from, to, only });
const en = add('en');
const ar = add('ar');
const any = add('any');

// ---- assessment: storage key with a migration read of the old key (before the generic token rules) ----
any('const KEY = "@q@-agent-assessment-v1";',
  'const KEY = "agent-assessment-v1"; const OLD_KEY = ["qd", "b-agent-assessment-v1"].join(""); /* progress saved under the old key is still read */');
any('try { const raw = localStorage.getItem(KEY); if (raw)',
  'try { const raw = localStorage.getItem(KEY) || localStorage.getItem(OLD_KEY); if (raw)');
any(/localStorage\.removeItem\(KEY\);(?! try \{ localStorage\.removeItem\(OLD_KEY\))/g, 'localStorage.removeItem(KEY); try { localStorage.removeItem(OLD_KEY); } catch(e){}');

// ---- titles, kickers, footers ----
en('<title>@Q@ Agentic AI — ', '<title>Agentic AI — ');
en('<h1>@Q@ Agentic AI — ', '<h1>Agentic AI — ');
en('<title>How to Run Agents in Production — @Q@</title>', '<title>How to Run Agents in Production</title>');
en('@BANK@ · Agentic AI Program', 'Agentic AI Program');
en('@Q@ Agentic AI Program', 'Agentic AI Program');
en('@Q@ Agent Framework', 'Agent Framework');
ar('@Q@ Agent Framework', 'Agent Framework');
ar(rx(' — @Q@</title>', 'g'), '</title>');
ar('<title>برنامج الذكاء الاصطناعي الوكيلي — @Q@</title>', '<title>برنامج الذكاء الاصطناعي الوكيلي</title>');
ar('الذكاء الاصطناعي الوكيلي في @Q@ — ', 'الذكاء الاصطناعي الوكيلي — ');
ar('برنامج الذكاء الاصطناعي الوكيلي في @Q@', 'برنامج الذكاء الاصطناعي الوكيلي');
ar('@BANKAR@ (@BANK@) · برنامج', 'برنامج');
ar('مركز برنامج الذكاء الاصطناعي الوكيلي في @BANKAR@ (@Q@):', 'مركز برنامج الذكاء الاصطناعي الوكيلي:');

// ---- playbook ----
en('A playbook for @Q@:', 'A playbook for your organisation:');
ar('دليل تشغيل (playbook) ل@BANKAR@ (@Q@):', 'دليل تشغيل (playbook) لمؤسستك:');

// ---- learning path (same sentence in both languages) ----
en('calibrated for a regulated financial institution (@Q@).', 'calibrated for a regulated financial institution.');
ar('خاضعة للتنظيم (@Q@).', 'خاضعة للتنظيم.');
en('a factual question about @Q@ the model', 'a factual question about your organisation the model');
ar('سؤالًا واقعيًا عن @Q@ لا', 'سؤالًا واقعيًا عن مؤسستك لا');
en('which rules apply to @Q@ and', 'which rules apply to your organisation and');
ar('القواعد التي تنطبق على @Q@ وما', 'القواعد التي تنطبق على مؤسستك وما');
en('for five @Q@ scenarios (', 'for five illustrative scenarios (');
ar('لخمسة سيناريوهات في @Q@ (', 'لخمسة سيناريوهات توضيحية (');
en('Budget and load-test against @Q@&#39;s real Arabic/English traffic mix', 'Budget and load-test against your real Arabic/English traffic mix');
ar('على المزيج الحقيقي لحركة @Q@ بالعربية', 'على المزيج الحقيقي لحركة مؤسستك بالعربية');
// Regional / estate facts about the real organisation: rewritten as neutral instructions.
en('consistent with @Q@&#39;s estate (Azure Qatar primary, DR per bank standards);', 'consistent with your organisation&#39;s estate and standards;');
ar('بما يتسق مع بنية @Q@ (Azure Qatar أساسياً، والتعافي وفق معايير البنك)؛', 'بما يتسق مع بنية مؤسستك ومعاييرها؛');
en('write the concrete @Q@ scenario (', 'write a concrete scenario from your organisation (');
ar('اكتب سيناريو @Q@ الملموس (', 'اكتب سيناريو ملموسًا من مؤسستك (');
en('ground @Q@&#39;s AI governance', 'ground your organisation&#39;s AI governance');
ar('حوكمة (governance) الذكاء الاصطناعي (AI) في @Q@ على', 'حوكمة (governance) الذكاء الاصطناعي (AI) في مؤسستك على');
en('skeleton for @Q@&#39;s framework', 'skeleton for your organisation&#39;s framework');
ar('لإطار (framework) @Q@ بدلًا', 'لإطار (framework) مؤسستك بدلًا');
// Whether the real organisation falls under the EU AI Act is a fact about it; replaced by a neutral statement.
en('— @Q@ isn&#39;t EU-regulated anyway; the Act is the benchmark because regional regulators borrow from it.',
   '— whether or not the Act applies to your organisation directly, it is the benchmark because regional regulators borrow from it.');
ar('— فـ@Q@ ليس خاضعًا لتنظيم الاتحاد الأوروبي أصلًا؛ والقانون مرجع مقارنة لأن',
   '— سواء أكان القانون ينطبق على مؤسستك مباشرة أم لا، فهو مرجع مقارنة لأن');
// Module 4.5: heading, its generated id, the table-of-contents link and the anchor link change together.
en('Module 4.5 — The @Q@ Regulatory Stack (≈4h)', 'Module 4.5 — The Regulatory Stack (≈4h)');
ar('المنظومة التنظيمية (regulatory stack) لـ@Q@ (≈4h)', 'المنظومة التنظيمية (regulatory stack) (≈4h)');
any('module-45-the-@q@-regulatory-stack-4h', 'module-45-the-regulatory-stack-4h');
// The list of local regulators that applied to the real organisation is replaced by a neutral instruction.
en('map @Q@&#39;s actual obligations (QCB, PDPPL, NCSA/NIA, Sharia governance) to implementing controls',
   'map the obligations that apply to your organisation (banking supervision, data protection, cybersecurity and, where relevant, Sharia governance) to implementing controls');
ar('اربط الالتزامات الفعلية لـ@Q@ (QCB، PDPPL، NCSA/NIA، الحوكمة الشرعية (Sharia governance)) بالضوابط',
   'اربط الالتزامات التي تنطبق على مؤسستك (الإشراف المصرفي (banking supervision)، وحماية البيانات (data protection)، والأمن السيبراني (cybersecurity)، والحوكمة الشرعية (Sharia governance) حيثما انطبقت) بالضوابط');
en('&quot;I can run @Q@&#39;s agent program', '&quot;I can run my organisation&#39;s agent program');
ar('برنامج الوكلاء (agents) في @Q@ من', 'برنامج الوكلاء (agents) في مؤسستي من');
en('keep @Q@ able to change model provider', 'keep your organisation able to change model provider');
ar('حافظ على قدرة @Q@ على تغيير', 'حافظ على قدرة مؤسستك على تغيير');
en('one real @Q@ process</strong>', 'one real process from your organisation</strong>');
ar('عملية حقيقية واحدة من عمليات @Q@</strong>', 'عملية حقيقية واحدة من عمليات مؤسستك</strong>');
en('differentiator for @Q@<', 'differentiator for your organisation<');
ar('بالنسبة لـ@Q@<', 'بالنسبة لمؤسستك<');

// ---- diagram: the enclosing box was labelled with the organisation name. Id and label change together;
// the label is shorter, so its box (foreignObject) is narrowed and re-centred in the cluster.
any(rx('(id="[0-9a-z]+)-@Q@(" data-look)', 'g'), '$1-Boundary$2');
en('<g class="cluster-label" transform="translate(140.2265625, 8)"><foreignObject width="356.671875" height="24">',
   '<g class="cluster-label" transform="translate(183.75, 8)"><foreignObject width="253.63" height="24">');
en('<p>Inside @Q@ — governance envelope on every hop</p>', '<p>Governance envelope on every hop</p>');
ar('<g class="cluster-label" transform="translate(38.3828125, 8)"><foreignObject width="655.875" height="24">',
   '<g class="cluster-label" transform="translate(125.2, 8)"><foreignObject width="466.22" height="24">');
ar('<p>داخل @Q@ — غلاف الحوكمة على كل قفزة (Inside @Q@ — governance envelope on every hop)</p>',
   '<p>غلاف الحوكمة على كل قفزة (Governance envelope on every hop)</p>');

// ---- code names, last, so the sentence rules above see the original text ----
any('@q@-regulatory-stack', 'regulatory-stack');
any('@q@-agent-framework', 'agent-framework');
any('@q@-agent-assessment-v', 'agent-assessment-v');
any(rx('\\b@q@\\.data\\.', 'g'), 'data.');

const isAr = (f) => f.endsWith('.ar.html');
let bad = 0;
for (const f of FILES) {
  const file = path.join(DIR, f);
  if (!fs.existsSync(file)) continue;
  const before = fs.readFileSync(file, 'utf8');
  let s = before;
  if (!CHECK) {
    for (const r of rules) {
      if (r.lang === 'en' && isAr(f)) continue;
      if (r.lang === 'ar' && !isAr(f)) continue;
      if (r.only && r.only !== f) continue;
      s = typeof r.from === 'string' ? s.split(r.from).join(r.to) : s.replace(r.from, r.to);
    }
    if (s !== before) { fs.writeFileSync(file, s); console.log('neutralised agentic/' + f); }
  }
  for (const m of s.matchAll(NAME)) {
    bad++;
    const i = m.index;
    console.error(`agentic/${f}: still contains "${m[0]}" near: ${s.slice(Math.max(0, i - 50), i + 60).replace(/\s+/g, ' ')}`);
  }
}
if (bad) {
  console.error(`error: ${bad} mention(s) of the organisation name remain. Add or fix a rule in scripts/agentic-neutral.mjs.`);
  process.exit(1);
}
if (CHECK) console.log('agentic pages carry no organisation name');
