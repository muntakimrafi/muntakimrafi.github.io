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

Exit status is 1 only when something is actually wrong. Having nothing to
report yet is normal on a new site and leaves the file untouched.
"""

import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "visitors.json")

DAYS = 90            # the window the page describes
PAGE = 100           # API maximum per request
STAMP = "%Y-%m-%dT%H:%M:%SZ"

# Codes worth a second try. A 404 is in here because GoatCounter has returned
# one mid-deploy for a route that exists the rest of the time, and a daily job
# that gives up on a two-second blip leaves the map a day stale.
RETRY_ON = {404, 408, 425, 429, 500, 502, 503, 504}
ATTEMPTS = 4


def window():
    """The reporting window, as timestamps rounded to the hour.

    `end` is the next whole hour rather than today's date: GoatCounter reads a
    bare date as midnight at the *start* of that day, which quietly excludes
    everything counted so far today — on a site that has just gone live, that
    is everything it has.
    """
    end = (dt.datetime.now(dt.timezone.utc).replace(minute=0, second=0, microsecond=0)
           + dt.timedelta(hours=1))
    start = (end - dt.timedelta(days=DAYS)).replace(hour=0)
    return start.strftime(STAMP), end.strftime(STAMP)


def api(code, token, path, params):
    """One API call, retried through the transient failures.

    A wrong site code or a rejected token is raised at once: those do not get
    better by asking again.
    """
    url = "https://%s.goatcounter.com/api/v0/%s?%s" % (
        code, path, urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer %s" % token,
        "Content-Type": "application/json",
    })
    for attempt in range(1, ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:            # a subclass of URLError
            if e.code not in RETRY_ON or attempt == ATTEMPTS:
                raise
            why = "%s %s" % (e.code, e.read().decode()[:120])
        except urllib.error.URLError as e:
            if attempt == ATTEMPTS:
                raise
            why = str(e.reason)
        wait = 5 * attempt
        print("  %s on attempt %d of %d; retrying in %ds"
              % (why, attempt, ATTEMPTS, wait), flush=True)
        time.sleep(wait)


def locations(code, token, start, end):
    """Every country row, following the API's pagination to the end."""
    counts, names, offset = {}, {}, 0
    while True:
        body = api(code, token, "stats/locations",
                   {"start": start, "end": end, "limit": PAGE, "offset": offset})
        rows = body.get("stats") or []
        for row in rows:
            # "BD", or "CA-BC" when region tracking is on: the country leads
            cc = (row.get("id") or "").split("-")[0].upper()
            if len(cc) != 2:
                continue
            counts[cc] = counts.get(cc, 0) + int(row.get("count") or 0)
            names.setdefault(cc, (row.get("name") or cc).split(",")[0].strip())
        if not body.get("more") or not rows:
            return counts, names
        offset += PAGE


def main():
    code = os.environ.get("GOATCOUNTER_CODE", "").strip()
    token = os.environ.get("GOATCOUNTER_TOKEN", "").strip()
    if not code or not token:
        sys.exit("GOATCOUNTER_CODE and GOATCOUNTER_TOKEN must both be set")

    start, end = window()
    print("asking %s.goatcounter.com for %s to %s" % (code, start, end), flush=True)

    try:
        counts, names = locations(code, token, start, end)
    except urllib.error.HTTPError as e:
        sys.exit("GoatCounter returned %s: %s" % (e.code, e.read().decode()[:400]))
    except urllib.error.URLError as e:
        sys.exit("could not reach GoatCounter: %s" % e.reason)

    if not counts:
        # Nothing to write. Say which kind of nothing, so the next step is clear.
        try:
            visits = api(code, token, "stats/total",
                         {"start": start, "end": end}).get("total", 0)
        except urllib.error.URLError:
            visits = None
        if visits:
            print("%d visits in this window, but GoatCounter reports no country for "
                  "any of them. Check that Country is ticked under Settings -> Data "
                  "collection; it cannot be filled in for visits already recorded."
                  % visits)
        else:
            print("no visits counted in this window yet")
        print("leaving %s as it is" % os.path.relpath(OUT, ROOT))
        return

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
