# muntakimrafi.github.io

The source for [muntakimrafi.github.io](https://muntakimrafi.github.io/).

A multi-tab personal site using the same design language as
[bsri-bd.github.io](https://bsri-bd.github.io/): bottle green as the ink,
vermilion spent only on actions, Newsreader / Public Sans / IBM Plex Mono, and
a light and a dark theme driven off one set of tokens.

## Tabs

| Page                | What is on it                                                       |
| ------------------- | ------------------------------------------------------------------- |
| `index.html`        | Hero, the five questions, topic index, counts, links onward          |
| `research.html`     | Research themes, projects, funding                                   |
| `publications.html` | Preprints, journal articles, conference papers                       |
| `talks.html`        | Invited talks, conference talks, posters, workshops                  |
| `teaching.html`     | Teaching assistantships with course lists, mentorship                |
| `service.html`      | Peer review, committee service, events and organisations             |
| `cv.html`           | The CV and CV of failures, as PDFs                                   |
| `visitors.html`     | A map of the countries the site is read from                         |

## Previewing it

```sh
python3 -m http.server 8000
# then open http://localhost:8000/
```

### preview.html — the whole site as one file

`preview.html` is a generated, self-contained copy of all eight pages: the
stylesheet and script inlined, the portrait as a data URI, and the tabs
switched client-side through the URL hash (`#research`, `#cv`, …).

It exists because a Claude artifact injects the published page into the
viewer's own document — the page's `<head>`, `<html>` and `<body>` are
discarded by the parser, and a link to a sibling `.html` file leaves the
preview frame. Flattening the site into one document sidesteps both.

```sh
python3 tools/build_preview.py
```

It is a preview artefact only and is gitignored: the real site is the eight
separate pages. Regenerate it whenever you need one. The visitors map is left
out of it, because that page draws itself from files it fetches at runtime.

## Editing content

Every page shares a masthead, a footer and a `<head>`. Keeping seven hand-written
copies of those in sync is how navigation drifts, so the pages are generated:

```sh
python3 tools/build.py
```

Content lives in `tools/build.py` as plain Python lists — `PREPRINTS`,
`JOURNALS`, `CONFERENCES`, `INVITED`, `TALKS`, `POSTERS`, `WORKSHOPS`,
`WORK`, `PROJECTS`, `TOPICS`, and so on. Add an entry there, re-run the script, and commit both the
script and the regenerated HTML. The generated files are committed, so GitHub
Pages needs no build step.

Styling is hand-written in `assets/css/styles.css`; the build script never
touches it.

## Venue logos on the talk cards

Each talk and poster shows a small tile. It renders the venue's initials by
default, and an image as soon as one exists:

```
assets/img/venues/<mark>.svg     # .png, .webp, .jpg also work
```

`<mark>` is the lowercased code in the first field of each entry in `INVITED`,
`TALKS` and `POSTERS` — `bi`, `ismb`, `cshl`, `cvpr` and so on. Add the file,
re-run `tools/build.py`, and that card switches over. Square or near-square
artwork renders best; the tile is 3.4rem with `object-fit: contain`.

## The visitors map

`visitors.html` shades a world map by the countries the site has been read
from. Three pieces feed it:

1. **GoatCounter counts the visits.** Every page carries its one-line snippet,
   added by `build.py` from the `GOATCOUNTER` constant at the top of that file.
   It sets no cookie, stores no IP address and needs no consent banner.
2. **A nightly job fetches the totals.** `.github/workflows/visitors.yml` runs
   `tools/fetch_visitors.py`, which asks the GoatCounter API for visits by
   country over the last 90 days and commits `data/visitors.json`.
3. **The page draws them.** `assets/js/visitors.js` reads that file and
   `assets/data/world-110m.json`, both served from this site, so nothing is
   fetched from anyone else while the page is open.

### Setting it up

1. Create a site at [goatcounter.com](https://www.goatcounter.com/). The code
   you pick becomes `<code>.goatcounter.com`; set `GOATCOUNTER` in
   `tools/build.py` to match it and re-run the build.
2. In GoatCounter, under **Settings → API tokens**, create a token with
   *Read statistics* permission.
3. In this repository, under **Settings → Secrets and variables → Actions**,
   add two secrets:

   | Secret              | Value                                |
   | ------------------- | ------------------------------------ |
   | `GOATCOUNTER_CODE`  | the site code from step 1            |
   | `GOATCOUNTER_TOKEN` | the API token from step 2            |

4. Run the workflow once by hand from the **Actions** tab. Until it does, the
   page says no visits have been counted yet.

Until both secrets exist the workflow fails and `data/visitors.json` keeps its
last good contents, so a bad night never blanks the map.

### The country outlines

`assets/data/world-110m.json` holds Natural Earth's 110m country outlines,
already projected and keyed by ISO 3166-1 alpha-2 so a GoatCounter row maps
straight onto a shape. Regenerate it only to change the map itself:

```sh
python3 tools/build_world.py
```

The projection is Equal Earth, which is equal-area: a country's share of the
ink is its share of the world's land. A handful of small countries and
city-states have no outline at this resolution; their visits are counted and
listed, but no shape lights up for them.
