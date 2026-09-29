#!/usr/bin/env python3
"""Build assets/data/talks-map.json — the points on the places map.

Reads INVITED, TALKS, POSTERS and WORKSHOPS straight out of build.py and keeps
every entry that was given in the room, which is every entry whose note is not
"Online". Each one is placed by the CITIES table below, projected with the same
Equal Earth fit as assets/data/world-110m.json so the dots land on the outlines.

Adding a talk is a change to build.py alone, unless it is in a city that has
not been visited before: then add its place string here too. A place string
with no entry stops the build rather than quietly dropping the talk.

    python3 tools/build_talks_map.py      # needs network, for the same reason
                                          # tools/build_world.py does

"""

import importlib.util
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "data", "talks-map.json")


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


build = load("build")
bw = load("build_world")

# The place strings as they are written in build.py -> (city, country, lon, lat).
# The city is what the map labels; the venue keeps the institution's name.
CITIES = {
    "Broad Institute of MIT and Harvard, Cambridge, United States":
        ("Cambridge", "United States", -71.0843, 42.3626),
    "IBM Thomas J. Watson Research Center, New York, United States":
        ("Yorktown Heights", "United States", -73.8007, 41.2098),
    "Imperial College London, London, United Kingdom":
        ("London", "United Kingdom", -0.1749, 51.4988),
    "University of Windsor, Windsor, Canada":
        ("Windsor", "Canada", -83.0664, 42.3049),
    "Vancouver, Canada":
        ("Vancouver", "Canada", -123.1207, 49.2827),
    "Michael Smith Laboratories, UBC":
        ("Vancouver", "Canada", -123.1207, 49.2827),
    "Liverpool, United Kingdom":
        ("Liverpool", "United Kingdom", -2.9916, 53.4084),
    "Cold Spring Harbor Laboratory, New York, United States":
        ("Cold Spring Harbor", "United States", -73.4685, 40.8593),
    "New York, United States":            # the 90th Cold Spring Harbor Symposium
        ("Cold Spring Harbor", "United States", -73.4685, 40.8593),
    "Santa Fe, United States":
        ("Santa Fe", "United States", -105.9378, 35.6870),
    "Stanford University, Stanford, United States":
        ("Stanford", "United States", -122.1697, 37.4275),
    "Calico Life Sciences, South San Francisco, United States":
        ("South San Francisco", "United States", -122.4087, 37.6516),
    "Fred Hutchinson Cancer Center, Seattle, United States":
        ("Seattle", "United States", -122.3321, 47.6062),
    "Seattle, United States":
        ("Seattle", "United States", -122.3321, 47.6062),
    "Las Vegas, United States":
        ("Las Vegas", "United States", -115.1398, 36.1699),
    "Athens, Greece":
        ("Athens", "Greece", 23.7275, 37.9838),
    "Turku, Finland":
        ("Turku", "Finland", 22.2666, 60.4518),
    "Zugspitze, Germany":
        ("Zugspitze", "Germany", 10.9853, 47.4211),
    "Long Beach, United States":
        ("Long Beach", "United States", -118.1937, 33.7701),
    "Guadalajara, Mexico":
        ("Guadalajara", "Mexico", -103.3496, 20.6597),
}

SOURCES = [
    ("invited", "Invited talk", build.INVITED),
    ("talk", "Talk", build.TALKS),
    ("poster", "Poster", build.POSTERS),
    ("workshop", "Workshop", build.WORKSHOPS),
]


def fit():
    """Re-derive the transform build_world.py fitted, so the points agree."""
    topo = bw.fetch(bw.SHAPES)
    arcs = bw.decode_arcs(topo)

    def ring(indexes):
        pts = []
        for i in indexes:
            seg = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts.extend(seg[1:] if pts else seg)
        return pts

    pts = []
    for geom in topo["objects"]["countries"]["geometries"]:
        if geom.get("id") in bw.SKIP:
            continue
        polys = (geom["arcs"] if geom["type"] == "MultiPolygon"
                 else [geom["arcs"]] if geom["type"] == "Polygon" else [])
        for poly in polys:
            for r in poly:
                for piece in bw.cut_antimeridian(ring(r)):
                    pts.extend(bw.equal_earth(*p) for p in piece)

    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    k = 1000.0 / (x1 - x0)
    return x0, y0, k, (y1 - y0) * k


def relax(places, rounds=400, pad=1.2, home=0.10):
    """Push overlapping dots apart, easing each back toward its true position.

    Stanford and South San Francisco are 40 km apart, which is one unit on a
    1000-unit-wide world map. Without this they are one blob.
    """
    keys = list(places)
    for _ in range(rounds):
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                p, q = places[a], places[b]
                dx, dy = q["x"] - p["x"], q["y"] - p["y"]
                d = math.hypot(dx, dy) or 0.01
                want = p["r"] + q["r"] + pad
                if d < want:
                    push, ux, uy = (want - d) / 2, dx / d, dy / d
                    p["x"] -= ux * push
                    p["y"] -= uy * push
                    q["x"] += ux * push
                    q["y"] += uy * push
        for key in keys:
            p = places[key]
            p["x"] += (p["ax"] - p["x"]) * home
            p["y"] += (p["ay"] - p["y"]) * home


def main():
    events, unknown = [], set()
    for kind, label, rows in SOURCES:
        for _mark, venue, where, when, _what, note in rows:
            if note == "Online":
                continue
            if where not in CITIES:
                unknown.add(where)
                continue
            year = re.findall(r"\b(\d{4})\b", when)[-1]
            events.append({"kind": kind, "label": label, "year": year,
                           "venue": venue, "place": CITIES[where][0]})

    if unknown:
        raise SystemExit("No city for these place strings; add them to CITIES:\n  "
                         + "\n  ".join(sorted(unknown)))

    x0, y0, k, height = fit()
    world = json.load(open(os.path.join(ROOT, "assets", "data", "world-110m.json")))
    if round(height, 1) != world["h"]:
        raise SystemExit("the fit no longer matches world-110m.json; rerun build_world.py")

    counts = {}
    for e in events:
        counts[e["place"]] = counts.get(e["place"], 0) + 1

    places = {}
    for city, country, lon, lat in CITIES.values():
        if city not in counts or city in places:
            continue
        px, py = bw.equal_earth(lon, lat)
        px, py = (px - x0) * k, (py - y0) * k
        places[city] = {"n": city, "k": country, "x": px, "y": py,
                        "ax": px, "ay": py, "r": 5.2 * math.sqrt(counts[city])}

    relax(places)
    for p in places.values():
        for key in ("x", "y", "ax", "ay"):
            p[key] = round(p[key], 1)
        del p["r"]

    blob = json.dumps({"places": list(places.values()), "events": events},
                      separators=(",", ":"))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(blob)

    print("wrote %s — %d appearances, %d places, %d countries"
          % (os.path.relpath(OUT, ROOT), len(events), len(places),
             len(set(p["k"] for p in places.values()))))


if __name__ == "__main__":
    main()
