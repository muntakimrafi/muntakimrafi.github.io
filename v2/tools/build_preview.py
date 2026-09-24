#!/usr/bin/env python3
"""Build preview.html — the whole site as one self-contained file.

The artifact viewer injects a published page into its own document body, so a
multi-page site loses its <head>, its <body> and any navigation that leaves the
frame. This flattens all seven pages into one document: stylesheet and script
inlined, the portrait as a data URI, and the tabs switched client-side through
the URL hash. Nothing is fetched relative to the page except the CV PDFs.

    python3 tools/build_preview.py      # run from the site root
"""

import base64
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import build  # noqa: E402

# slug -> hash fragment used in place of the page file
HASH = {slug: "#" + ("home" if slug == "index.html" else slug[:-5])
        for slug, _, _, _ in build.PAGES}


def read(path, mode="r"):
    with open(os.path.join(ROOT, path), mode, **({} if "b" in mode else {"encoding": "utf-8"})) as fh:
        return fh.read()


def link_rewrite(html):
    """Point every in-site link at its panel instead of its file."""
    for slug, frag in HASH.items():
        html = html.replace('href="%s"' % slug, 'href="%s"' % frag)
    return html


def nav(cls):
    return "\n".join(
        '      <a href="%s">%s</a>' % (HASH[slug], label) for slug, label in build.NAV)


def main():
    css = read("assets/css/styles.css")
    js = read("assets/js/main.js")
    portrait = base64.b64encode(read("assets/img/portrait.jpg", "rb")).decode("ascii")

    panels = []
    for slug, title, _desc, builder in build.PAGES:
        frag = HASH[slug][1:]
        body = link_rewrite(builder().strip())
        panels.append('<div class="page" id="%s" data-page data-title="%s"%s>\n%s\n</div>'
                      % (frag, title, "" if slug == "index.html" else " hidden", body))

    masthead = link_rewrite(build.masthead("index.html"))
    # The brand and the current-page marker are handled by the router instead.
    masthead = masthead.replace(' aria-current="page" class="is-current"', "")
    footer = link_rewrite(build.footer())
    footer = footer.replace('<script src="assets/js/main.js"></script>\n</body>\n</html>\n', "")

    # Only the chrome survives from masthead()/footer(); strip their page wrapper.
    body_open = masthead[masthead.index("<header"):]
    panels_html = "\n\n".join(panels).replace(
        'src="assets/img/portrait.jpg"', 'src="data:image/jpeg;base64,%s"' % portrait)

    # Venue logos, if any have been added, get inlined too.
    MEDIA = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
             "svg": "image/svg+xml", "webp": "image/webp"}
    for rel in sorted(set(re.findall(r'src="(assets/img/venues/[^"]+)"', panels_html))):
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        mime = MEDIA.get(rel.rsplit(".", 1)[-1].lower(), "application/octet-stream")
        blob = base64.b64encode(read(rel, "rb")).decode("ascii")
        panels_html = panels_html.replace(
            'src="%s"' % rel, 'src="data:%s;base64,%s"' % (mime, blob))

    router = """
/* Tab router. The published page is injected into the viewer's own document,
   so navigating to a sibling file would leave the preview; each page is a
   panel here and the hash selects one. */
(function () {
  "use strict";
  var panels = Array.prototype.slice.call(document.querySelectorAll("[data-page]"));
  var links = Array.prototype.slice.call(
    document.querySelectorAll('.nav a[href^="#"], .footer__links a[href^="#"], .cardlink[href^="#"], .btn[href^="#"]'));
  var ids = panels.map(function (p) { return "#" + p.id; });

  function show(hash, scroll) {
    if (ids.indexOf(hash) === -1) { return false; }
    panels.forEach(function (p) { p.hidden = ("#" + p.id) !== hash; });
    links.forEach(function (a) {
      var on = a.getAttribute("href") === hash;
      if (a.classList.contains("nav-link") || a.closest(".nav") || a.closest(".footer__links")) {
        a.classList.toggle("is-current", on);
      }
      if (on) { a.setAttribute("aria-current", "page"); } else { a.removeAttribute("aria-current"); }
    });
    var panel = document.getElementById(hash.slice(1));
    if (panel && panel.dataset.title) { document.title = panel.dataset.title; }
    if (scroll) { window.scrollTo(0, 0); }
    return true;
  }

  window.addEventListener("hashchange", function () { show(window.location.hash, true); });
  if (!show(window.location.hash, false)) { show("#home", false); }
})();
"""

    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&family=Public+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
{css}
/* The viewer supplies the outer document, so guarantee the page fills it. */
body {{ min-height: 100vh; }}
.page[hidden] {{ display: none !important; }}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

{masthead}
<main id="main">
{panels}
</main>

{footer}
<script>
{js}
{router}
</script>
</body>
</html>
""".format(name=build.NAME, desc=build.PAGES[0][2], css=css, masthead=body_open,
           panels=panels_html, footer=footer.strip(), js=js, router=router)

    out = os.path.join(ROOT, "preview.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote preview.html (%.0f KB, %d panels)" % (len(html.encode()) / 1024, len(panels)))


if __name__ == "__main__":
    main()
