#!/usr/bin/env python3
"""Build research.graybearstudio.com (Hidden Structure Research Group) into dist/.

A standalone site, separate from the GrayBear Studio app pages. Page content, figures
and maths come from research/research.py (maintained by the Observer Limit Program chat).
That module was written for paths under /research/; this build maps them to the root:
"research" -> "/", "research/idea" -> "/idea/", and so on.

    pip install latex2mathml
    python3 build.py
"""
import hashlib
import html
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "research"))
import research  # noqa: E402

DIST = os.path.join(ROOT, "dist")
DOMAIN = "research.graybearstudio.com"
FONTS = ("https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;"
         "1,6..72,400&family=Public+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap")
E = html.escape

# mark: a visible core inside a hidden ring
MARK = ('<svg viewBox="0 0 32 32" aria-hidden="true" fill="none">'
        '<circle cx="16" cy="16" r="12.5" stroke="var(--app2)" stroke-width="1.6" stroke-dasharray="2.2 3.2" stroke-linecap="round"/>'
        '<circle cx="16" cy="16" r="5.5" fill="var(--app)"/></svg>')


def local(p):
    """Map the module's /research/... paths to this site's root."""
    p = p.strip("/")
    if p == "research":
        return ""
    if p.startswith("research/"):
        return p[len("research/"):]
    return p


def href(frm, to):
    up = [x for x in local(frm).split("/") if x]
    target = [x for x in local(to).split("/") if x]
    i = 0
    while i < min(len(up), len(target)) and up[i] == target[i]:
        i += 1
    rel = "../" * (len(up) - i) + "/".join(target[i:])
    if not rel:
        return "./"
    return rel if rel.endswith("/") else rel + "/"


def accent_css(sec):
    l1, d1 = sec["accent"]
    l2, d2 = sec["accent2"]
    return (f"<style>:root{{--app:{l1};--app2:{l2}}}"
            f"@media (prefers-color-scheme: dark){{:root:not([data-theme=\"light\"]){{--app:{d1};--app2:{d2}}}}}"
            f":root[data-theme=\"dark\"]{{--app:{d1};--app2:{d2}}}</style>")


def asset_url(here, name):
    with open(os.path.join(ROOT, "assets", name) if name == "site.css" else os.path.join(ROOT, "research", name), "rb") as f:
        v = hashlib.sha1(f.read()).hexdigest()[:10]
    return href(here, "assets") + f"{name}?v={v}"


def page(here, title, body, sec=None, description=""):
    sec = sec or research.SECTION
    home = href(here, "")
    full_title = title if local(here) == "" else f"{title} · Hidden Structure Research Group"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(full_title)}</title>
<meta name="description" content="{E(description)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{asset_url(here, 'site.css')}">
{accent_css(sec)}
<style>.mark svg{{color:inherit}}</style>
</head>
<body>
<header class="top"><div class="wrap">
<a class="mark" href="{home}">{MARK}<b>Hidden Structure</b><span>Research Group</span></a>
</div></header>
<main>
{body}
</main>
<footer class="bottom"><div class="wrap">
<span>Hidden Structure Research Group · <a href="mailto:hello@graybearstudio.com">hello@graybearstudio.com</a></span>
<nav aria-label="Footer"><a href="{home}">Overview</a><a href="https://graybearstudio.com/privacy/">Privacy</a></nav>
<p class="notes">Research notes from the Hidden Structure Research Group, a project of GrayBear Studio. Mathematics, not medical, financial or professional advice. This site uses no cookies and no analytics.</p>
</div></footer>
</body>
</html>
"""


def write(rel_dir, content):
    d = os.path.join(DIST, local(rel_dir))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(content)


def main():
    shutil.rmtree(DIST, ignore_errors=True)
    os.makedirs(os.path.join(DIST, "assets"))
    shutil.copy(os.path.join(ROOT, "assets", "site.css"), os.path.join(DIST, "assets", "site.css"))
    shutil.copy(os.path.join(ROOT, "research", "research.css"), os.path.join(DIST, "assets", "research.css"))
    for here, (fn, title, desc) in research.BUILDERS.items():
        doc = page(here, title, fn(href), research.SECTION, desc)
        doc = doc.replace("</head>", f'<link rel="stylesheet" href="{asset_url(here, "research.css")}">\n</head>', 1)
        write(here, doc)
    nf = page("404", "Page not found", """<section class="wrap intro"><p class="eyebrow">404</p>
<h1>That page isn't here.</h1><p>It may have moved. <a href="/">Go to the overview</a>.</p></section>""",
              research.SECTION, "")
    with open(os.path.join(DIST, "404.html"), "w", encoding="utf-8") as f:
        f.write(nf.replace('href="../"', 'href="/"').replace('href="../assets/', 'href="/assets/'))
    urls = [f"https://{DOMAIN}/" + (local(h) + "/" if local(h) else "") for h in research.BUILDERS]
    with open(os.path.join(DIST, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    with open(os.path.join(DIST, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: https://{DOMAIN}/sitemap.xml\n")
    with open(os.path.join(DIST, "CNAME"), "w") as f:
        f.write(DOMAIN + "\n")
    open(os.path.join(DIST, ".nojekyll"), "w").close()
    n = sum(len(fs) for _, _, fs in os.walk(DIST))
    print(f"built {n} files into dist")


if __name__ == "__main__":
    main()
