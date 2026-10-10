# Course trailers

One 22-second motion-graphics trailer per course, built with
[HyperFrames](https://github.com/heygen-com/hyperframes) (HTML + GSAP → MP4).
No narration; 1920×1080, 30 fps, H.264.

| Course | Video |
|---|---|
| System Design for Vibe Coders | [renders/vibe.mp4](renders/vibe.mp4) |
| Running AI Agents in Production | [renders/agentic.mp4](renders/agentic.mp4) |
| SaaS Building Blocks | [renders/saas.mp4](renders/saas.mp4) |
| AI Governance: Zero to Hero | [renders/aigp.mp4](renders/aigp.mp4) |
| AI Product Management: Zero to Hero | [renders/aipm.mp4](renders/aipm.mp4) |
| Secure AI & Application Security: Zero to Hero | [renders/secai.mp4](renders/secai.mp4) |
| Data Engineering & Analytics: Zero to Hero | [renders/data.mp4](renders/data.mp4) |
| Cloud & DevOps: Zero to Hero | [renders/cloud.mp4](renders/cloud.mp4) |
| From Graduate to Hired | [renders/career.mp4](renders/career.mp4) |
| Software Testing: Zero to Hero in the AI Era | [renders/testing.mp4](renders/testing.mp4) |

## Structure of each trailer

| Time | Scene |
|---|---|
| 0–4.4s | Course verb chip, title rises word by word, accent underline draws |
| 4.4–8.6s | The hook line, word by word; emphasis words glow in the course colour |
| 8.6–13.6s | Six or seven topic chips cascade in |
| 13.6–17.8s | Course numbers count up (modules, lessons, …) and audience tags |
| 17.8–22s | End card: English + Arabic title, "free to read", course URL |

Each course uses its colour from the landing page (`landing.html`, dark theme).

## Editing

- **Copy** (titles, hook, topics, numbers, tags, colour): `videos/courses.json`.
  Wrap a hook word in `*asterisks*` to make it an emphasis word.
- **Design and motion** (shared by all trailers): `scripts/build-videos.mjs`.

```bash
npm run videos:build                            # generate videos/build/<slug>/ (HyperFrames projects)
npm run videos:check                            # + lint / layout / contrast checks
npm run videos:render                           # + render videos/renders/<slug>.mp4
node scripts/build-videos.mjs --only=saas --render --quality=high
```

To tweak one interactively: `cd videos/build/<slug> && npx hyperframes preview`.

Requires Node ≥ 22 and FFmpeg. `videos/build/` is generated and git-ignored.
GSAP and the fonts (Inter, IBM Plex Sans Arabic, JetBrains Mono — all SIL Open
Font License) are vendored in `videos/assets/` so renders work offline and come out the same every time.
