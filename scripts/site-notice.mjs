// One notice for every generated page in the library: what the material is, what it is not,
// and where to read how it was made or report a problem. Every builder imports this module and
// lists it among its sources, so a change here marks every course output stale until rebuilt.
//
// Keep both languages in step. Arabic text follows the library rule: English beside each term.

const REPO = 'https://github.com/Tamoura/system-design-for-vibe-coders';

/** Link to open the "Report a problem" issue form (.github/ISSUE_TEMPLATE/report-a-problem.yml), pre-titled with the course id. */
export function reportUrl(course) {
  const title = encodeURIComponent(`[${course}] `);
  return `${REPO}/issues/new?template=report-a-problem.yml&amp;title=${title}`;
}

/** Path from a page to the "How these courses are made" page. `root` is the path to the site root ('../' from a course folder, '' from the landing page). */
export function aboutUrl(lang, root = '../') {
  return lang === 'ar' ? `${root}about/index.ar.html` : `${root}about/`;
}

const TEXT = {
  en: {
    status: 'Status: drafted with AI; not yet reviewed by a subject expert.',
    advice: 'Educational material, not legal, financial, security or employment advice.',
    independent: 'Independent: not affiliated with or endorsed by any certification body or vendor named here; trademarks belong to their owners.',
    about: 'How these courses are made',
    report: 'Report a problem',
  },
  ar: {
    status: 'الحالة (status): مسودّة أُعدّت بالذكاء الاصطناعي (drafted with AI)، ولم يراجعها بعدُ خبير في الموضوع (subject expert).',
    advice: 'مادة تعليمية (educational material)، وليست استشارة قانونية أو مالية أو أمنية أو مهنية (legal, financial, security or employment advice).',
    independent: 'مستقلة (independent): غير تابعة لأي جهة شهادات (certification body) أو مورّد (vendor) مذكور هنا ولا معتمدة منها، والعلامات التجارية (trademarks) ملك أصحابها.',
    about: 'كيف تُصنع هذه الدورات (How these courses are made)',
    report: 'أبلغ عن مشكلة (Report a problem)',
  },
};

/**
 * The notice as one HTML paragraph body (no wrapping <p>), for a page footer.
 * @param {'en'|'ar'} lang
 * @param {string} course  short course id used in the issue title, e.g. 'aigp'
 * @param {string} root    path to the site root from the page ('../' or '')
 */
export function siteNotice(lang, course, root = '../') {
  const t = TEXT[lang] || TEXT.en;
  return `${t.status} ${t.advice} ${t.independent} <a href="${aboutUrl(lang, root)}">${t.about}</a> · <a href="${reportUrl(course)}" rel="noopener">${t.report}</a>`;
}

export const SITE_NOTICE_TEXT = TEXT;
