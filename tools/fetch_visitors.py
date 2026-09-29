#!/usr/bin/env python3
"""Write data/visitors.json from GoatCounter's location stats.

Run by .github/workflows/visitors.yml once a day. Reads two variables from the
environment and nothing else, so it needs no dependencies beyond the standard
library:

    GOATCOUNTER_CODE    the site code, i.e. <code>.goatcounter.com
    GOATCOUNTER_TOKEN   an API token with "read statistics" permission

    python3 tools/fetch_visitors.py

Only country totals are stored: a two-letter code and a count. GoatCounter
itself keeps no cookie and no IP address, and nothing per-visitor reaches the
repository.
"""

import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "visitors.json")

DAYS = 90            # the window the page describes
PAGE = 100           # API maximum per request


def get(code, token, offset):
    end = dt.date.today()
    start = end - dt.timedelta(days=DAYS)
    url = ("https://%s.goatcounter.com/api/v0/stats/locations"
           "?start=%s&end=%s&limit=%d&offset=%d" % (code, start, end, PAGE, offset))
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer %s" % token,
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main():
    code = os.environ.get("GOATCOUNTER_CODE", "").strip()
    token = os.environ.get("GOATCOUNTER_TOKEN", "").strip()
    if not code or not token:
        sys.exit("GOATCOUNTER_CODE and GOATCOUNTER_TOKEN must both be set")

    counts, names, offset = {}, {}, 0
    while True:
        try:
            body = get(code, token, offset)
        except urllib.error.HTTPError as e:
            sys.exit("GoatCounter returned %s: %s" % (e.code, e.read().decode()[:400]))

        rows = body.get("stats") or []
        for row in rows:
            # "BD", or "CA-BC" when region tracking is on: the country leads
            cc = (row.get("id") or "").split("-")[0].upper()
            if len(cc) != 2:
                continue
            counts[cc] = counts.get(cc, 0) + int(row.get("count") or 0)
            names.setdefault(cc, (row.get("name") or cc).split(",")[0].strip())

        if not body.get("more") or not rows:
            break
        offset += PAGE

    if not counts:
        # A transient failure must not blank a map that is already correct.
        sys.exit("no country rows returned; leaving %s as it is"
                 % os.path.relpath(OUT, ROOT))

    rows = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    out = {
        "updated": dt.date.today().isoformat(),
        "days": DAYS,
        "total": sum(counts.values()),
        "countries": [{"c": c, "n": names[c], "v": v} for c, v in rows],
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=False)
        fh.write("\n")
    print("wrote %s — %d visits from %d countries"
          % (os.path.relpath(OUT, ROOT), out["total"], len(rows)))


if __name__ == "__main__":
    main()
