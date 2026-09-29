/* The visitors map. Two files arrive: the country outlines, projected once by
   tools/build_world.py and keyed by ISO code, and the counts that
   .github/workflows/visitors.yml writes from GoatCounter each night. Both are
   plain files in the repository, so the page fetches nothing from anyone else.

   Every count is also printed in the list underneath, so no value on this page
   can only be reached by hovering. */
(function () {
  "use strict";

  var mount = document.getElementById("visitors");
  if (!mount) { return; }

  var SVG_NS = "http://www.w3.org/2000/svg";
  var TOP = 12;                       // countries listed by name; the rest are summed

  /* Bins for the shaded map. Every label names a count the scale reaches. */
  var BINS = [700, 200, 50, 10, 1];

  var nf = new Intl.NumberFormat("en-US");
  var world = null, rows = [], total = 0, max = 1, mode = "shade";
  var shapes = {}, gLand, gDots, halo;

  var el = {
    plate: document.getElementById("v-plate"),
    map: document.getElementById("v-map"),
    tip: document.getElementById("v-tip"),
    ranks: document.getElementById("v-ranks"),
    rest: document.getElementById("v-rest"),
    count: document.getElementById("v-count"),
    note: document.getElementById("v-note"),
    figures: document.getElementById("v-figures"),
    body: document.getElementById("v-body"),
    visits: document.getElementById("v-visits"),
    countries: document.getElementById("v-countries"),
    share: document.getElementById("v-share")
  };

  function say(message) {
    el.note.textContent = message;
    el.note.hidden = false;
    el.body.hidden = true;
  }

  function make(name, attrs) {
    var node = document.createElementNS(SVG_NS, name);
    for (var k in attrs) { node.setAttribute(k, attrs[k]); }
    return node;
  }

  function binOf(v) {
    for (var i = 0; i < BINS.length; i++) { if (v >= BINS[i]) { return i; } }
    return BINS.length - 1;
  }

  function radius(v) { return 4 + 26 * Math.sqrt(v / max); }

  /* ---- drawing --------------------------------------------------------- */

  function draw() {
    el.map.setAttribute("viewBox", "0 0 " + world.w + " " + world.h);
    gLand = make("g", { "class": "vmap__land" });
    gDots = make("g", { "class": "vmap__dots" });
    halo = make("path", { "class": "vmap__halo" });

    var code;
    for (code in world.shapes) {
      var path = make("path", { d: world.shapes[code].d });
      path.dataset.code = code;
      shapes[code] = path;
      gLand.appendChild(path);
    }

    /* Biggest circles first, so the small ones stay on top and stay hoverable. */
    rows.forEach(function (row) {
      var shape = world.shapes[row.c];
      if (!shape) { return; }
      var dot = make("circle", {
        "class": "vmap__dot",
        cx: shape.c[0], cy: shape.c[1], r: radius(row.v)
      });
      dot.dataset.code = row.c;
      gDots.appendChild(dot);
    });

    el.map.appendChild(gLand);
    el.map.appendChild(gDots);
    el.map.appendChild(halo);
  }

  function paint() {
    var shaded = mode === "shade";
    var byCode = {};
    rows.forEach(function (row) { byCode[row.c] = row.v; });

    for (var code in shapes) {
      var v = byCode[code];
      shapes[code].style.fill = (shaded && v) ? "var(--vmap-" + (5 - binOf(v)) + ")" : "";
    }
    gDots.style.display = shaded ? "none" : "";
    gLand.style.pointerEvents = shaded ? "" : "none";
  }

  /* ---- pointing at a country ------------------------------------------- */

  function highlight(code) {
    var shape = world.shapes[code];
    if (shape) { halo.setAttribute("d", shape.d); }
  }

  function clear() {
    el.tip.hidden = true;
    halo.removeAttribute("d");
  }

  function show(code, clientX, clientY) {
    var row = null;
    rows.some(function (r) { if (r.c === code) { row = r; return true; } return false; });
    if (!row) { return clear(); }

    var box = el.plate.getBoundingClientRect();
    el.tip.innerHTML = "<b>" + row.n + "</b><span>" + nf.format(row.v) + " visits &middot; "
                     + (row.v / total * 100).toFixed(1) + "%</span>";
    el.tip.hidden = false;
    el.tip.style.left = Math.min(Math.max(clientX - box.left, 70), box.width - 70) + "px";
    el.tip.style.top = (clientY - box.top) + "px";
    highlight(code);
  }

  /* ---- the same counts as text ----------------------------------------- */

  function fill() {
    total = rows.reduce(function (s, r) { return s + r.v; }, 0);
    max = rows[0].v;

    el.visits.textContent = nf.format(total);
    el.countries.textContent = rows.length;
    el.share.textContent = Math.round(
      rows.slice(0, 5).reduce(function (s, r) { return s + r.v; }, 0) / total * 100) + "%";
    el.count.textContent = rows.length + (rows.length === 1 ? " country" : " countries");

    el.ranks.innerHTML = rows.slice(0, TOP).map(function (row) {
      return '<li tabindex="0" data-code="' + row.c + '">'
           + '<span class="vranks__name">' + row.n + "</span>"
           + '<span class="vranks__bar" aria-hidden="true"><i style="width:'
           + (row.v / max * 100).toFixed(1) + '%"></i></span>'
           + '<span class="vranks__value">' + nf.format(row.v) + "</span></li>";
    }).join("");

    var tail = rows.slice(TOP);
    el.rest.textContent = tail.length
      ? "and " + tail.length + " more countries, "
        + nf.format(tail.reduce(function (s, r) { return s + r.v; }, 0)) + " visits between them."
      : "";

    Array.prototype.forEach.call(el.ranks.children, function (li) {
      var code = li.dataset.code;
      li.addEventListener("mouseenter", function () { highlight(code); });
      li.addEventListener("focus", function () { highlight(code); });
      li.addEventListener("mouseleave", clear);
      li.addEventListener("blur", clear);
    });
  }

  /* ---- go -------------------------------------------------------------- */

  function grab(url) {
    return fetch(url, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) { throw new Error(url + " returned " + r.status); }
      return r.json();
    });
  }

  say("Drawing the map\u2026");

  Promise.all([
    grab("assets/data/world-110m.json"),
    grab("data/visitors.json")
  ]).then(function (loaded) {
    world = loaded[0];
    var data = loaded[1];
    rows = (data.countries || []).filter(function (r) { return r.v > 0; });

    if (!rows.length) {
      // Nothing counted yet: show the heading alone rather than an apology.
      el.note.hidden = true;
      return;
    }

    el.note.hidden = true;
    el.body.hidden = false;
    fill();
    draw();
    paint();

    el.map.addEventListener("pointermove", function (e) {
      var code = e.target.dataset && e.target.dataset.code;
      if (code) { show(code, e.clientX, e.clientY); } else { clear(); }
    });
    el.map.addEventListener("pointerleave", clear);

    Array.prototype.forEach.call(
      document.querySelectorAll('input[name="vmode"]'), function (input) {
        input.addEventListener("change", function () { mode = input.value; paint(); });
      });
  }).catch(function (err) {
    say("The visitor counts could not be loaded.");
    if (window.console) { console.error(err); }
  });
})();
