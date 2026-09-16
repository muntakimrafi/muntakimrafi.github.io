# Personal site — v2 (draft, not published)

A rewrite of [muntakimrafi.github.io](https://muntakimrafi.github.io/) as a
multi-tab site, using the same design language as
[bsri-bd.github.io](https://bsri-bd.github.io/): bottle green as the ink,
vermilion spent only on actions, Newsreader / Public Sans / IBM Plex Mono, and a
light and a dark theme driven off one set of tokens.

**This is not live.** It exists only on the `claude/personal-website-tabs-da2ufn`
branch, in this subdirectory. GitHub Pages serves the repository root of the
publishing branch, so nothing here is reachable from the web and the current site
at `muntakimrafi.github.io` is untouched.

## Tabs

| Page                | What is on it                                                       |
| ------------------- | ------------------------------------------------------------------- |
| `index.html`        | Hero, current work, topic index, three selected papers, links onward |
| `research.html`     | Research themes in depth, research positions, funded projects        |
| `publications.html` | Preprints and in preparation, journal articles, conference papers    |
| `talks.html`        | Invited talks, selected posters, workshops run                       |
| `teaching.html`     | Teaching assistantships with course lists, mentorship                |
| `service.html`      | Peer review, committees, community organising, memberships           |
| `cv.html`           | Education, positions held, awards, and the PDFs                      |

## Previewing it

```sh
cd v2
python3 -m http.server 8000
# then open http://localhost:8000/
```

### preview.html — the whole site as one file

`preview.html` is a generated, self-contained copy of all seven pages: the
stylesheet and script inlined, the portrait as a data URI, and the tabs
switched client-side through the URL hash (`#research`, `#cv`, …).

It exists because a Claude artifact injects the published page into the
viewer's own document — the page's `<head>`, `<html>` and `<body>` are
discarded by the parser, and a link to a sibling `.html` file leaves the
preview frame. Flattening the site into one document sidesteps both.

```sh
cd v2
python3 tools/build_preview.py      # rebuild after tools/build.py
```

It is a preview artefact only. The real site is the seven separate pages;
`preview.html` does not need to ship to GitHub Pages, and nothing links to it.

## Editing content

Every page shares a masthead, a footer and a `<head>`. Keeping seven hand-written
copies of those in sync is how navigation drifts, so the pages are generated:

```sh
cd v2
python3 tools/build.py
```

Content lives in `tools/build.py` as plain Python lists — `PREPRINTS`,
`JOURNALS`, `CONFERENCES`, `TALKS`, `POSTERS`, `WORKSHOPS`, `PROJECTS`,
`AWARDS`, and so on. Add an entry there, re-run the script, and commit both the
script and the regenerated HTML. The generated files are committed, so GitHub
Pages needs no build step.

Styling is hand-written in `assets/css/styles.css`; the build script never
touches it.

## Publishing it, when you decide

This replaces the current site only when you move it to the repository root of
the publishing branch. Everything the new site needs is inside `v2/`, so nothing
outside it has to move with it:

```sh
# from the repo root, on a branch off main
git rm index.html stylesheet.css sitemap.xml
git rm -r images data
git mv v2/index.html v2/research.html v2/publications.html v2/talks.html \
       v2/teaching.html v2/service.html v2/cv.html v2/favicon.ico \
       v2/README.md v2/assets v2/data v2/tools .
```

Then merge to the publishing branch. Until you do, both sites coexist and the
live one keeps serving.

## Still to fill in

**Three project descriptions are inferred and need replacing.** In the `WORK`
list in `tools/build.py`, these three had no paper or preprint to draw on, so
their summaries are written from the grant title alone and are guesses:

- *Continual improvement of gene regulatory models*
- *Lossless preprocessing of the sequence and expression space*
- *Selection on human gene expression*

The other five projects are summarised from the papers and preprints behind
them. If there is synthesis or automation work not represented here, it belongs
in this list — the homepage now leads on scaling data generation, and the
projects should carry that claim.

Also outstanding:

- The de Boer Lab and Talaria Summer Institute entries have no outbound links —
  I did not have URLs I could verify.
- No `og:image`, so link previews fall back to plain text.
