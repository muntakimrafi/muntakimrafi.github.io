/* The places map: a dot at every city where a talk, poster or workshop was
   given in the room. Both files it reads are committed to this repository —
   the outlines from tools/build_world.py and the points from
   tools/build_talks_map.py — so the page fetches nothing from anyone else.

   The four kinds of appearance are separated by the filter rather than by
   colour, which keeps the map to one hue and leaves vermilion for actions.
   Every appearance is printed in the list underneath, so nothing on this page
   can only be reached by hovering. */
(function () {
  "use strict";

  var mount = document.getElementById("places");
  if (!mount) { return; }

  var SVG_NS = "http://www.w3.org/2000/svg";

  var KINDS = [
    { id: "all", label: "All" },
    { id: "invited", label: "Invited" },
    { id: "talk", label: "Talks" },
    { id: "poster", label: "Posters" },
    { id: "workshop", label: "Workshops" }
  ];

  var world = null, data = null, filter = "all";
  var byCity = {}, marks = {}, gDots, gHits;

  var el = {
    plate: document.getElementById("p-plate"),
    map: document.getElementById("p-map"),
    tip: document.getElementById("p-tip"),
    key: document.getElementById("p-key"),
    cap: document.getElementById("p-cap"),
    list: document.getElementById("p-list"),
    count: document.getElementById("p-count"),
    filters: document.getElementById("p-filters"),
    note: document.getElementById("p-note"),
    body: document.getElementById("p-body"),
    events: document.getElementById("p-events"),
    places: document.getElementById("p-places"),
    countries: document.getElementById("p-countries")
  };

  function make(name, attrs) {
    var node = document.createElementNS(SVG_NS, name);
    for (var k in attrs) { node.setAttribute(k, attrs[k]); }
    return node;
  }

  /* Area in proportion to the count, matching tools/build_talks_map.py so the
     dots are spaced for the size they are actually drawn at. */
  function radius(n) { return 5.2 * Math.sqrt(n); }

  function selected() {
    if (filter === "all") { return data.events; }
    return data.events.filter(function (e) { return e.kind === filter; });
  }

  function byYear(a, b) { return b.year - a.year; }

  /* ---- drawing --------------------------------------------------------- */

  function draw() {
    el.map.setAttribute("viewBox", "0 0 " + world.w + " " + world.h);

    var land = make("g", { "class": "vmap__land" });
    for (var code in world.shapes) {
      land.appendChild(make("path", { d: world.shapes[code].d }));
    }

    gDots = make("g", {});
    gHits = make("g", {});
    data.places.forEach(function (p) {
      var dot = make("circle", { "class": "vmap__dot", cx: p.x, cy: p.y, r: 0 });
      var hit = make("circle", { "class": "vmap__hit", cx: p.x, cy: p.y, r: 0 });
      hit.dataset.city = p.n;
      marks[p.n] = { dot: dot, hit: hit };
      gDots.appendChild(dot);
      gHits.appendChild(hit);
    });

    el.map.appendChild(land);
    el.map.appendChild(gDots);
    el.map.appendChild(gHits);
  }

  function paint() {
    var rows = selected();
    var per = {};
    rows.forEach(function (e) { per[e.place] = (per[e.place] || 0) + 1; });

    data.places.forEach(function (p) {
      var n = per[p.n] || 0;
      marks[p.n].dot.setAttribute("r", n ? radius(n) : 0);
      // a dot this small needs a hit area a finger can land on
      marks[p.n].hit.setAttribute("r", n ? Math.max(13, radius(n)) : 0);
    });

    var places = Object.keys(per).length;
    var countries = {};
    rows.forEach(function (e) { countries[byCity[e.place].k] = 1; });

    el.events.textContent = rows.length;
    el.places.textContent = places;
    el.countries.textContent = Object.keys(countries).length;
    el.count.textContent = places + (places === 1 ? " place" : " places");

    drawKey(per);
    drawList(per, rows);

    el.cap.textContent = (filter === "all"
      ? "All " + rows.length + " appearances given in person."
      : rows.length + " of " + data.events.length + " appearances given in person.")
      + " Talks given online are left off. Where two cities are too close to"
      + " separate at this scale, the dots are eased apart by up to about 300 km.";
  }

  function drawKey(per) {
    var counts = Object.keys(per).map(function (k) { return per[k]; });
    var steps = [1, 2, Math.max.apply(null, counts)].filter(function (v, i, a) {
      return v >= 1 && a.indexOf(v) === i;
    });
    el.key.innerHTML = steps.map(function (v) {
      var d = Math.round(radius(v) * 2.2);
      return "<div><i style=\"width:" + d + "px;height:" + d + "px\"></i>"
           + "<small>" + v + "</small></div>";
    }).join("");
  }

  /* ---- the list, which carries every appearance without a hover --------- */

  function drawList(per, rows) {
    var order = Object.keys(per).sort(function (a, b) {
      return per[b] - per[a] || a.localeCompare(b);
    });

    el.list.innerHTML = order.map(function (city) {
      var here = rows.filter(function (e) { return e.place === city; }).sort(byYear);
      return '<li tabindex="0" data-city="' + city + '">'
        + '<div class="plist__head"><span class="plist__name">' + city + "</span>"
        + '<span class="plist__country">' + byCity[city].k + "</span>"
        + '<span class="plist__n">' + per[city] + "</span></div>"
        + '<ul class="plist__events">' + here.map(function (e) {
            return "<li><span>" + e.year + "</span><b>" + e.label
                 + " &middot; " + e.venue + "</b></li>";
          }).join("") + "</ul></li>";
    }).join("");

    Array.prototype.forEach.call(el.list.children, function (li) {
      var city = li.dataset.city;
      li.addEventListener("mouseenter", function () { lift(city, true); });
      li.addEventListener("focus", function () { lift(city, true); });
      li.addEventListener("mouseleave", function () { lift(city, false); });
      li.addEventListener("blur", function () { lift(city, false); });
    });
  }

  /* ---- pointing at a place --------------------------------------------- */

  function lift(city, on) {
    if (marks[city]) {
      marks[city].dot.classList.toggle("is-on", on);
    }
  }

  function clear() {
    el.tip.hidden = true;
    data.places.forEach(function (p) { lift(p.n, false); });
  }

  function show(city, clientX, clientY) {
    var here = selected().filter(function (e) { return e.place === city; }).sort(byYear);
    if (!here.length) { return clear(); }

    var box = el.plate.getBoundingClientRect();
    el.tip.innerHTML = "<b>" + city + "</b><em>" + byCity[city].k + "</em>"
      + here.map(function (e) {
          return "<u><i>" + e.year + "</i>" + e.label + " &middot; " + e.venue + "</u>";
        }).join("");
    el.tip.hidden = false;
    el.tip.style.left = Math.min(Math.max(clientX - box.left, 100), box.width - 100) + "px";
    el.tip.style.top = (clientY - box.top) + "px";
    lift(city, true);
  }

  /* ---- go -------------------------------------------------------------- */

  function grab(url) {
    return fetch(url, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) { throw new Error(url + " returned " + r.status); }
      return r.json();
    });
  }

  Promise.all([
    grab("assets/data/world-110m.json"),
    grab("assets/data/talks-map.json")
  ]).then(function (loaded) {
    world = loaded[0];
    data = loaded[1];
    data.places.forEach(function (p) { byCity[p.n] = p; });

    el.note.hidden = true;
    el.body.hidden = false;

    el.filters.innerHTML = KINDS.map(function (k, i) {
      return '<input type="radio" name="kind" id="kind-' + k.id + '" value="' + k.id + '"'
           + (i ? "" : " checked") + '>'
           + '<label for="kind-' + k.id + '">' + k.label + "</label>";
    }).join("");

    draw();
    paint();

    el.map.addEventListener("pointermove", function (e) {
      var city = e.target.dataset && e.target.dataset.city;
      if (city) { show(city, e.clientX, e.clientY); } else { clear(); }
    });
    el.map.addEventListener("pointerleave", clear);

    Array.prototype.forEach.call(
      document.querySelectorAll('input[name="kind"]'), function (input) {
        input.addEventListener("change", function () {
          filter = input.value;
          clear();
          paint();
        });
      });
  }).catch(function (err) {
    el.note.textContent = "The map could not be loaded.";
    el.note.hidden = false;
    el.body.hidden = true;
    if (window.console) { console.error(err); }
  });
})();
