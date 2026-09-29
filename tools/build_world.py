#!/usr/bin/env python3
"""Build assets/data/world-110m.json — the outlines the visitors map draws.

Natural Earth's 110m country outlines, projected once here so the browser only
has to draw them, and keyed by ISO 3166-1 alpha-2 so a GoatCounter row ("BD",
468) maps straight onto a shape with no name matching.

The projection is Equal Earth. It is equal-area, so a country's share of the
ink is its share of the world's land; Web Mercator would print Greenland the
size of Africa, which on a traffic map reads as readers who are not there.

    python3 tools/build_world.py      # needs network; rerun only to change the map

"""

import json
import math
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "data", "world-110m.json")

SHAPES = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json"
CODES = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
         "master/geojson/ne_110m_admin_0_countries.geojson")

SKIP = {"010"}                       # Antarctica: no readers, half the height

A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
SQ3 = math.sqrt(3)


def fetch(url):
    print("fetching %s" % url)
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.load(r)


def equal_earth(lon, lat):
    lam, phi = math.radians(lon), math.radians(lat)
    th = math.asin(SQ3 / 2 * math.sin(phi))
    t2 = th * th
    dy = A1 + 3 * A2 * t2 + t2 * t2 * t2 * (7 * A3 + 9 * A4 * t2)
    return (2 * SQ3 * lam * math.cos(th) / (3 * dy),
            -th * (A1 + A2 * t2 + t2 * t2 * t2 * (A3 + A4 * t2)))   # SVG y grows down


def decode_arcs(topo):
    """TopoJSON stores arcs as quantised deltas; walk them back to lon/lat."""
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    out = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        out.append(pts)
    return out


def cut_antimeridian(pts):
    """Split a lon/lat ring where it jumps the 180th meridian.

    Russia and Fiji are stored as single rings that run off one edge of the
    world and continue on the other. Projected as they stand, the return jump
    is drawn as a line straight across the map, so each crossing is cut and the
    two ends pinned to the meridian at the latitude it was crossed.
    """
    parts, cur = [], [pts[0]]
    for a, b in zip(pts, pts[1:]):
        if abs(b[0] - a[0]) > 180:
            east = 180 if a[0] > 0 else -180
            span = (b[0] - a[0]) - math.copysign(360, b[0] - a[0])
            lat = a[1] + (b[1] - a[1]) * ((east - a[0]) / span if span else 0)
            cur.append((east, lat))
            parts.append(cur)
            cur = [(-east, lat)]
        else:
            cur.append(b)
    parts.append(cur)
    if len(parts) > 1:                      # a ring is a loop: last piece joins first
        parts[0] = parts.pop()[:-1] + parts[0]
    return [p for p in parts if len(p) > 2]


def main():
    topo = fetch(SHAPES)
    arcs = decode_arcs(topo)

    # numeric ISO code -> (alpha-2, display name), from Natural Earth's own table
    code = {}
    for f in fetch(CODES)["features"]:
        p = f["properties"]
        a2 = p.get("ISO_A2_EH") or p.get("ISO_A2")
        n3 = p.get("ISO_N3_EH") or p.get("ISO_N3")
        if a2 and a2 != "-99" and n3 and n3 != "-99":
            code[str(int(n3)).zfill(3)] = (a2, p["NAME"])

    def ring(indexes):
        pts = []
        for i in indexes:
            seg = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts.extend(seg[1:] if pts else seg)
        return pts

    shapes = []
    for geom in topo["objects"]["countries"]["geometries"]:
        cid = geom.get("id")
        if cid in SKIP or cid not in code:
            continue
        polys = (geom["arcs"] if geom["type"] == "MultiPolygon"
                 else [geom["arcs"]] if geom["type"] == "Polygon" else [])
        rings = [[[equal_earth(*p) for p in piece]]
                 for poly in polys for r in poly for piece in cut_antimeridian(ring(r))]
        if rings:
            shapes.append((code[cid][0], code[cid][1], rings))

    pts = [p for _, _, rs in shapes for poly in rs for r in poly for p in r]
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    W = 1000.0
    K = W / (x1 - x0)

    def place(p):
        return ((p[0] - x0) * K, (p[1] - y0) * K)

    def centroid(rings):
        """Area-weighted centroid of the largest ring, so a dot sits on the
        mainland rather than between a country and its islands."""
        best, best_a = None, 0.0
        for poly in rings:
            r = [place(p) for p in poly[0]]
            a = cx = cy = 0.0
            for i in range(len(r) - 1):
                cross = r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1]
                a += cross
                cx += (r[i][0] + r[i + 1][0]) * cross
                cy += (r[i][1] + r[i + 1][1]) * cross
            if abs(a) > abs(best_a):
                best_a, best = a, ((cx / (3 * a), cy / (3 * a)) if a else r[0])
        return best

    def path(rings):
        d, prev = [], None
        for poly in rings:
            for r in poly:
                for i, q in enumerate(place(p) for p in r):
                    if i == 0:
                        d.append("M%.1f %.1f" % q)
                    elif round(q[0], 1) != round(prev[0], 1) or round(q[1], 1) != round(prev[1], 1):
                        d.append("L%.1f %.1f" % q)
                    prev = q
                d.append("Z")
        return "".join(d)

    out = {}
    for a2, name, rings in shapes:
        c = centroid(rings)
        out[a2] = {"n": name, "d": path(rings), "c": [round(c[0], 1), round(c[1], 1)]}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    blob = json.dumps({"w": round(W), "h": round((y1 - y0) * K, 1), "shapes": out},
                      separators=(",", ":"))
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(blob)
    print("wrote %s — %d countries, %d KB"
          % (os.path.relpath(OUT, ROOT), len(out), len(blob) // 1024))


if __name__ == "__main__":
    main()
