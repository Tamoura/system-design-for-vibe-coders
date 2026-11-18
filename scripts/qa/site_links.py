#!/usr/bin/env python3
"""Internal links: every link inside the assembled site points at a file (and anchor) that exists.

Run after the publish workflow's "Assemble the site" step, on the `_site/` folder it builds, so paths
are checked in the layout readers actually get (for example `/vibe/index.en.html`, which does not exist
in the source tree). External links (http, https, mailto and similar) are not checked here; the lychee
step reports those without blocking the deploy.

What is checked, in every .html page under the site folder:
- `href` and `src` values that are relative or root-relative paths: the target file must exist
  (a folder resolves to its index.html);
- a `#fragment` on such a link, or a bare `#fragment`: the target page must contain an element with that
  `id` or `name`. Fragments that start with `/` (`#/6.3`) are routes read by the page's script; they are
  checked against the lesson ids the page carries (`data-lesson`, `id`) when the page has any, else skipped.

usage: python3 scripts/qa/site_links.py [SITE_DIR]      (default: _site)
exit status: 0 when every internal link resolves, 1 when any is broken, 2 when the folder is missing.
"""
from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

EXTERNAL = ("http:", "https:", "mailto:", "tel:", "data:", "javascript:", "blob:", "about:")


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, int]] = []
        self.ids: set[str] = set()
        self.routes: set[str] = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value is None:
                continue
            if name in ("id", "name"):
                self.ids.add(value)
            elif name == "data-lesson":
                self.routes.add(value)
            elif name in ("href", "src"):
                self.links.append((value.strip(), self.getpos()[0]))


def parse(path: Path, cache: dict[Path, Page]) -> Page:
    if path not in cache:
        p = Page()
        p.feed(path.read_text(encoding="utf-8", errors="replace"))
        cache[path] = p
    return cache[path]


def resolve(site: Path, page: Path, target: str) -> Path:
    if target.startswith("/"):
        parts = target.lstrip("/").split("/", 1)
        # GitHub Pages serves the site under /<repo>/; accept both forms.
        candidate = site / target.lstrip("/")
        if not candidate.exists() and len(parts) == 2:
            candidate = site / parts[1]
        return candidate
    return (page.parent / target).resolve()


def main() -> int:
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "_site").resolve()
    if not site.is_dir():
        print(f"site folder not found: {site}", file=sys.stderr)
        return 2
    cache: dict[Path, Page] = {}
    pages = sorted(site.rglob("*.html"))
    broken: list[str] = []
    checked = 0
    for page in pages:
        doc = parse(page, cache)
        for raw, line in doc.links:
            if not raw or raw.lower().startswith(EXTERNAL) or raw.startswith("//") or "${" in raw or "{{" in raw:
                continue
            parts = urlsplit(raw)
            path, frag = unquote(parts.path), unquote(parts.fragment)
            checked += 1
            target = page if not path else resolve(site, page, path)
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                broken.append(f"{page.relative_to(site)}:{line}: {raw} → missing file")
                continue
            if not frag or target.suffix != ".html":
                continue
            tdoc = parse(target, cache)
            if frag.startswith("/"):
                route = frag[1:]
                if tdoc.routes and route and route not in tdoc.routes and route not in tdoc.ids:
                    broken.append(f"{page.relative_to(site)}:{line}: {raw} → no lesson '{route}' in {target.relative_to(site)}")
                continue
            if frag not in tdoc.ids:
                broken.append(f"{page.relative_to(site)}:{line}: {raw} → no #{frag} in {target.relative_to(site)}")
    print(f"Internal links (scripts/qa/site_links.py): {len(pages)} pages, {checked} internal links checked")
    if broken:
        print(f"✗ {len(broken)} broken internal link(s)")
        for b in broken[:200]:
            print(f"  - {b}")
        if len(broken) > 200:
            print(f"  … and {len(broken) - 200} more")
        return 1
    print("✓ every internal link resolves")
    return 0


if __name__ == "__main__":
    sys.exit(main())
