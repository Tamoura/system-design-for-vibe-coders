/**
 * The course trailer player, shared by every course page builder.
 *
 * Trailers are rendered by scripts/build-videos.mjs into videos/renders/<slug>.mp4 (+ .jpg poster).
 * `base` is the path from the page to videos/renders/: '../videos/renders/' for a course in its
 * own folder, 'videos/renders/' for a page at the repo root.
 */
const CAPTION = {
  en: 'Course trailer · 22 seconds',
  ar: 'عرض تعريفي بالدورة (بالإنجليزية) · 22 ثانية',
};
const LABEL = {
  en: 'Course trailer',
  ar: 'عرض تعريفي بالدورة',
};

/** lang: 'en', 'ar', or 'both' (bilingual page that toggles .en-only / .ar-only). */
export function trailerHtml(slug, lang, base = '../videos/renders/') {
  const caption = lang === 'both'
    ? `<span class="en-only">${CAPTION.en}</span><span class="ar-only" lang="ar" dir="rtl">${CAPTION.ar}</span>`
    : CAPTION[lang];
  const label = lang === 'ar' ? LABEL.ar : LABEL.en;
  return `<figure class="trailer">
  <video controls preload="none" playsinline poster="${base}${slug}.jpg" aria-label="${label}"><source src="${base}${slug}.mp4" type="video/mp4"></video>
  <figcaption>${caption}</figcaption>
</figure>`;
}

export const TRAILER_CSS = `
/* Course trailer (scripts/trailer.mjs) */
.trailer{margin:1.8rem 0;max-width:720px}
.trailer video{display:block;width:100%;height:auto;aspect-ratio:16/9;border-radius:14px;background:#131519;
  border:1px solid var(--line,#e4e0d8);box-shadow:0 10px 30px rgba(20,20,30,.12)}
.trailer figcaption{margin-top:.5rem;font-size:.8rem;color:var(--muted,#5c6470)}
@media print{.trailer{display:none}}
`;
