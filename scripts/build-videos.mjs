// Builds one HyperFrames motion-graphics trailer per course.
//
//   node scripts/build-videos.mjs                 # generate projects into videos/build/<slug>/
//   node scripts/build-videos.mjs --check         # generate + `hyperframes check` each project
//   node scripts/build-videos.mjs --render        # generate + render videos/renders/<slug>.mp4
//   node scripts/build-videos.mjs --only=vibe,saas --render --quality=high   (default: standard)
//
// Course copy lives in videos/courses.json; this file owns the shared design and
// motion. Every project is a standalone HyperFrames composition (HTML + GSAP)
// with fonts and GSAP vendored locally so renders are deterministic and offline.
import { readFileSync, writeFileSync, mkdirSync, cpSync, rmSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const VIDEOS = join(ROOT, "videos");
const BUILD = join(VIDEOS, "build");
const RENDERS = join(VIDEOS, "renders");
const HYPERFRAMES = "hyperframes@0.8.124";
const SITE = "tamoura.github.io/system-design-for-vibe-coders";

const args = process.argv.slice(2);
const only = (args.find((a) => a.startsWith("--only=")) || "").slice(7).split(",").filter(Boolean);
const doCheck = args.includes("--check");
const doRender = args.includes("--render");
const quality = (args.find((a) => a.startsWith("--quality=")) || "--quality=standard").slice(10);

const DURATION = 22;
// Scene windows (seconds). Each scene enters at its start and exits just before the next.
const T = { title: 0, hook: 4.4, topics: 8.6, stats: 13.6, end: 17.8 };

const esc = (s) =>
  String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

// "*word*" marks an emphasis word in the hook line.
function hookWords(hook) {
  return hook
    .split(/\s+/)
    .map((w, i) => {
      const em = /^\*.*\*[.,!?]?$/.test(w);
      const text = em ? w.replace(/\*/g, "") : w;
      return `<span class="hw${em ? " em" : ""}" id="hw${i}">${esc(text)}</span>`;
    })
    .join(" ");
}

function hexToRgb(hex) {
  const n = parseInt(hex.slice(1), 16);
  return `${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255}`;
}

function composition(c) {
  const titleWords = c.title.split(" ").map((w, i) => `<span class="tw-mask"><span class="tw" id="tw${i}">${esc(w)}</span></span>`).join(" ");
  const topics = c.topics
    .map((t, i) => `<div class="chip" id="chip${i}"><span class="chip-n">${String(i + 1).padStart(2, "0")}</span><span class="chip-t">${esc(t)}</span></div>`)
    .join("\n          ");
  const stats = c.stats
    .map((s, i) => {
      const shown = s.text ?? `0${s.suffix ?? ""}`;
      return `<div class="stat" id="stat${i}"><div class="stat-v" id="statv${i}">${esc(shown)}</div><div class="stat-l">${esc(s.label)}</div></div>`;
    })
    .join("\n          ");
  const tags = c.tags.map((t) => `<span class="tag">${esc(t)}</span>`).join("");
  const url = `${SITE}/${c.slug}/`;
  const counters = JSON.stringify(c.stats.map((s, i) => (s.text ? null : { id: `statv${i}`, value: s.value, suffix: s.suffix ?? "" })).filter(Boolean));

  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>${esc(c.title)} — trailer</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Inter"; font-weight: 400; src: url("assets/fonts/inter-latin-400-normal.woff2") format("woff2"); }
      @font-face { font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2") format("woff2"); }
      @font-face { font-family: "Inter"; font-weight: 800; src: url("assets/fonts/inter-latin-800-normal.woff2") format("woff2"); }
      @font-face { font-family: "Plex Arabic"; font-weight: 400; src: url("assets/fonts/ibm-plex-sans-arabic-arabic-400-normal.woff2") format("woff2"); }
      @font-face { font-family: "Plex Arabic"; font-weight: 600; src: url("assets/fonts/ibm-plex-sans-arabic-arabic-600-normal.woff2") format("woff2"); }
      @font-face { font-family: "JetBrains Mono"; font-weight: 500; src: url("assets/fonts/jetbrains-mono-latin-500-normal.woff2") format("woff2"); }

      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #131519; }
      #root {
        --c: ${c.color}; --c-rgb: ${hexToRgb(c.color)};
        --ink: #ece9e3; --muted: #9aa0aa; --line: #2b2f37; --panel: #1b1e24;
        width: 100%; height: 100%; position: relative; overflow: hidden;
        font-family: "Inter", sans-serif; color: var(--ink);
      }
      #stage { position: absolute; inset: 0; }

      /* Backdrop: dot grid, drifting accent glow, frame corners, progress rail */
      .bg-grid {
        position: absolute; inset: -60px;
        background-image: radial-gradient(rgba(255,255,255,0.07) 1.5px, transparent 1.5px);
        background-size: 48px 48px;
      }
      .bg-glow {
        position: absolute; width: 1400px; height: 1400px; left: 900px; top: -500px; border-radius: 50%;
        background: radial-gradient(circle, rgba(var(--c-rgb), 0.22) 0%, rgba(var(--c-rgb), 0) 62%);
      }
      .bg-glow2 {
        position: absolute; width: 1100px; height: 1100px; left: -500px; top: 420px; border-radius: 50%;
        background: radial-gradient(circle, rgba(var(--c-rgb), 0.12) 0%, rgba(var(--c-rgb), 0) 60%);
      }
      .brand {
        position: absolute; left: 120px; top: 84px; display: flex; align-items: center; gap: 18px;
        font-family: "JetBrains Mono", monospace; font-size: 22px; letter-spacing: 0.14em; color: var(--muted);
      }
      .brand-dot { width: 14px; height: 14px; border-radius: 4px; background: var(--c); display: block; }
      .lang {
        position: absolute; right: 120px; top: 80px; display: flex; gap: 12px; align-items: center;
        font-size: 22px; color: var(--muted);
      }
      .lang .ar { font-family: "Plex Arabic", "Inter", sans-serif; font-size: 24px; }
      .rail { position: absolute; left: 120px; right: 120px; bottom: 72px; height: 4px; background: var(--line); border-radius: 2px; }
      .rail-fill { position: absolute; left: 0; top: 0; bottom: 0; width: 100%; background: var(--c); border-radius: 2px; transform-origin: 0 50%; display: block; }

      .scene { position: absolute; left: 120px; right: 120px; top: 180px; bottom: 140px; display: flex; flex-direction: column; justify-content: center; opacity: 0; }

      /* 1 — Title */
      .verb {
        align-self: flex-start; display: block; padding: 12px 26px; border-radius: 999px;
        border: 2px solid rgba(var(--c-rgb), 0.55); background: rgba(var(--c-rgb), 0.12);
        color: var(--c); font-size: 30px; font-weight: 600; letter-spacing: 0.02em; opacity: 0;
      }
      .title { margin-top: 40px; font-size: 128px; line-height: 1.04; font-weight: 800; letter-spacing: -0.035em; max-width: 1640px; text-wrap: balance; }
      .tw-mask { display: inline-block; overflow: hidden; vertical-align: top; padding-bottom: 0.08em; }
      .tw { display: inline-block; }
      .subtitle { margin-top: 18px; font-size: 56px; font-weight: 600; color: var(--c); letter-spacing: -0.02em; opacity: 0; }
      .underline { margin-top: 44px; width: 520px; height: 10px; border-radius: 5px; background: var(--c); transform-origin: 0 50%; display: block; }

      /* 2 — Hook */
      .hook { font-size: 92px; line-height: 1.14; font-weight: 800; letter-spacing: -0.03em; max-width: 1600px; text-wrap: balance; }
      .hw { display: inline-block; opacity: 0; }
      .hw.em { color: var(--c); }

      /* 3 — Topics */
      .kicker { font-family: "JetBrains Mono", monospace; font-size: 26px; letter-spacing: 0.08em; color: var(--c); text-transform: uppercase; opacity: 0; }
      .chips { margin-top: 48px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px; }
      .chip {
        display: flex; align-items: center; gap: 22px; padding: 30px 34px; border-radius: 22px;
        background: var(--panel); border: 2px solid var(--line); opacity: 0;
      }
      .chip-n { font-family: "JetBrains Mono", monospace; font-size: 24px; color: var(--c); }
      .chip-t { font-size: 38px; font-weight: 600; letter-spacing: -0.01em; line-height: 1.15; }

      /* 4 — Stats */
      .stats { display: flex; gap: 40px; }
      .stat { flex: 1; padding: 40px 40px 36px; border-left: 6px solid var(--c); background: rgba(var(--c-rgb), 0.07); border-radius: 0 20px 20px 0; opacity: 0; }
      .stat-v { font-size: 120px; font-weight: 800; letter-spacing: -0.04em; line-height: 1; font-variant-numeric: tabular-nums; }
      .stat-l { margin-top: 18px; font-size: 32px; color: var(--muted); font-weight: 600; }
      .tags { margin-top: 56px; display: flex; gap: 18px; flex-wrap: wrap; opacity: 0; }
      .tag { padding: 12px 24px; border-radius: 999px; border: 2px solid var(--line); font-size: 28px; color: var(--ink); }

      /* 5 — End card */
      .end { align-items: center; text-align: center; }
      .end .verb { align-self: center; }
      .end-title { margin-top: 36px; font-size: 104px; line-height: 1.06; font-weight: 800; letter-spacing: -0.035em; max-width: 1600px; text-wrap: balance; opacity: 0; }
      .end-ar { margin-top: 26px; font-family: "Plex Arabic", "Inter", sans-serif; font-size: 52px; font-weight: 600; color: var(--c); opacity: 0; }
      .end-meta { margin-top: 54px; font-size: 32px; color: var(--muted); opacity: 0; }
      .end-url {
        margin-top: 22px; display: inline-block; font-family: "JetBrains Mono", monospace; font-size: 34px;
        padding: 18px 34px; border-radius: 16px; background: var(--panel); border: 2px solid rgba(var(--c-rgb), 0.5); color: var(--ink); opacity: 0;
      }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${DURATION}" data-width="1920" data-height="1080">
      <div id="stage" class="clip" data-start="0" data-duration="${DURATION}" data-track-index="0">
        <div class="bg-grid" id="bgGrid"></div>
        <div class="bg-glow" id="bgGlow"></div>
        <div class="bg-glow2" id="bgGlow2"></div>
        <div class="brand" id="brand"><span class="brand-dot"></span><span>TAMOURA · COURSE LIBRARY</span></div>
        <div class="lang" id="lang"><span>EN</span><span>·</span><span class="ar" dir="rtl">العربية</span></div>

        <section class="scene" id="s1">
          <span class="verb" id="s1verb">${esc(c.verb)}</span>
          <h1 class="title">${titleWords}</h1>
          ${c.subtitle ? `<div class="subtitle" id="s1sub">${esc(c.subtitle)}</div>` : ""}
          <span class="underline" id="s1line"></span>
        </section>

        <section class="scene" id="s2">
          <p class="hook">${hookWords(c.hook)}</p>
        </section>

        <section class="scene" id="s3">
          <div class="kicker" id="s3kicker">${esc(c.topicsLabel)}</div>
          <div class="chips">
          ${topics}
          </div>
        </section>

        <section class="scene" id="s4">
          <div class="stats">
          ${stats}
          </div>
          <div class="tags" id="s4tags">${tags}<span class="tag">Self-assessment</span><span class="tag">Free to read</span></div>
        </section>

        <section class="scene end" id="s5">
          <span class="verb" id="s5verb">${esc(c.verb)}</span>
          <div class="end-title" id="s5title">${esc(c.title)}${c.subtitle ? `: ${esc(c.subtitle)}` : ""}</div>
          <div class="end-ar" id="s5ar" dir="rtl" lang="ar">${esc(c.titleAr)}</div>
          <div class="end-meta" id="s5meta">Free to read · English &amp; Arabic</div>
          <div><span class="end-url" id="s5url">${esc(url)}</span></div>
        </section>

        <div class="rail"><span class="rail-fill" id="railFill"></span></div>
      </div>
    </div>
    <script>
      const T = ${JSON.stringify(T)};
      const D = ${DURATION};
      const tl = gsap.timeline({ paused: true });
      const out = "power2.in", inn = "power3.out";

      // Backdrop + chrome (whole film)
      tl.fromTo("#bgGlow", { x: 0, y: 0 }, { x: -520, y: 260, duration: D, ease: "sine.inOut" }, 0);
      tl.fromTo("#bgGlow2", { x: 0, y: 0 }, { x: 380, y: -180, duration: D, ease: "sine.inOut" }, 0);
      tl.fromTo("#bgGrid", { y: 0 }, { y: 48, duration: D, ease: "none" }, 0);
      tl.fromTo("#railFill", { scaleX: 0 }, { scaleX: 1, duration: D, ease: "none" }, 0);
      tl.fromTo("#brand", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.7, ease: inn }, 0.1);
      tl.fromTo("#lang", { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.7, ease: inn }, 0.2);

      // Scene groups: on at start, off just before the next scene
      const scenes = [["#s1", T.title, T.hook], ["#s2", T.hook, T.topics], ["#s3", T.topics, T.stats], ["#s4", T.stats, T.end], ["#s5", T.end, null]];
      for (const [id, a, b] of scenes) {
        tl.to(id, { opacity: 1, duration: 0.01 }, a);
        if (b !== null) tl.to(id, { opacity: 0, y: -40, duration: 0.4, ease: out }, b - 0.45);
      }

      // 1 — Title: chip, masked word rise, subtitle, underline draw
      tl.fromTo("#s1verb", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: inn }, 0.35);
      tl.fromTo(".tw", { yPercent: 110 }, { yPercent: 0, duration: 0.85, ease: "expo.out", stagger: 0.09 }, 0.55);
      if (document.querySelector("#s1sub")) tl.fromTo("#s1sub", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.6, ease: inn }, 1.5);
      tl.fromTo("#s1line", { scaleX: 0 }, { scaleX: 1, duration: 0.9, ease: "expo.inOut" }, 1.6);

      // 2 — Hook: word-by-word, emphasis words pop
      tl.fromTo(".hw", { opacity: 0, y: 36 }, { opacity: 1, y: 0, duration: 0.5, ease: inn, stagger: 0.11 }, T.hook + 0.2);
      tl.fromTo(".hw.em", { textShadow: "0 0 0px rgba(${hexToRgb(c.color)}, 0)" }, { textShadow: "0 0 28px rgba(${hexToRgb(c.color)}, 0.85)", duration: 0.35, ease: "power2.out", yoyo: true, repeat: 1, stagger: 0.08, immediateRender: false }, T.hook + 2.3);

      // 3 — Topics: kicker, then chips cascade in
      tl.fromTo("#s3kicker", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: inn }, T.topics + 0.15);
      tl.fromTo(".chip", { opacity: 0, y: 40, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "back.out(1.6)", stagger: 0.16 }, T.topics + 0.45);
      tl.fromTo(".chip", { borderColor: "#2b2f37" }, { borderColor: "${c.color}", duration: 0.3, stagger: 0.16, immediateRender: false }, T.topics + 2.1);

      // 4 — Stats: cards rise, numbers count up, tags follow
      tl.fromTo(".stat", { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.6, ease: inn, stagger: 0.14 }, T.stats + 0.15);
      ${counters}.forEach((s, i) => {
        const el = document.getElementById(s.id);
        const p = { v: 0 };
        tl.fromTo(p, { v: 0 }, {
          v: s.value, duration: 1.6, ease: "power2.out", immediateRender: false,
          onUpdate: () => { el.textContent = Math.round(p.v) + s.suffix; },
        }, T.stats + 0.3 + i * 0.14);
      });
      tl.fromTo("#s4tags", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: inn }, T.stats + 1.9);

      // 5 — End card
      tl.fromTo("#s5verb", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: inn }, T.end + 0.15);
      tl.fromTo("#s5title", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.8, ease: "expo.out" }, T.end + 0.35);
      tl.fromTo("#s5ar", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.7, ease: inn }, T.end + 0.8);
      tl.fromTo("#s5meta", { opacity: 0 }, { opacity: 1, duration: 0.6 }, T.end + 1.3);
      tl.fromTo("#s5url", { opacity: 0, scale: 0.94 }, { opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.8)" }, T.end + 1.55);

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
`;
}

const courses = JSON.parse(readFileSync(join(VIDEOS, "courses.json"), "utf8")).filter((c) => !only.length || only.includes(c.slug));
if (!courses.length) throw new Error(`No courses match --only=${only.join(",")}`);

mkdirSync(BUILD, { recursive: true });
for (const c of courses) {
  const dir = join(BUILD, c.slug);
  if (existsSync(dir)) rmSync(dir, { recursive: true });
  mkdirSync(dir, { recursive: true });
  cpSync(join(VIDEOS, "assets"), join(dir, "assets"), { recursive: true });
  writeFileSync(join(dir, "index.html"), composition(c));
  writeFileSync(join(dir, "meta.json"), JSON.stringify({ id: `${c.slug}-trailer`, name: `${c.title} — trailer` }, null, 2) + "\n");
  writeFileSync(join(dir, "hyperframes.json"), JSON.stringify({ $schema: "https://hyperframes.heygen.com/schema/hyperframes.json", paths: { assets: "assets" } }, null, 2) + "\n");
  console.log(`generated  videos/build/${c.slug}/index.html`);

  const run = (...a) => execFileSync("npx", ["--yes", HYPERFRAMES, ...a], { cwd: dir, stdio: "inherit", env: { ...process.env, HYPERFRAMES_SKIP_SKILLS: "1" } });
  if (doCheck) run("check", ".");
  if (doRender) {
    mkdirSync(RENDERS, { recursive: true });
    run("render", ".", "-q", quality, "-o", join(RENDERS, `${c.slug}.mp4`));
  }
}
