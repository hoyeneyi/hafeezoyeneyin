(function () {
  // ===== Edit these =====
  var FORM_ENDPOINT = "https://formspree.io/f/xvkkdgel";       // Formspree: "Portfolio – Start a project"
  var ROTATING = [                                              // home headline; keep each under ~12 characters
    { text: "from scratch", color: "var(--flare)" },
    { text: "to load fast", color: "var(--ion)" },
    { text: "to stand out", color: "var(--solar)" },
    { text: "to sell", color: "var(--volt)" }
  ];
  // ======================

  var doc = document.documentElement;
  doc.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var PREVIEW = !!window.SITE_PREVIEW;     // set only in the claude.ai preview build, where live iframes are blocked
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }

  var yr = $("#year"); if (yr) yr.textContent = new Date().getFullYear();

  // Visitor's local time (home HUD)
  var clock = $("#clock");
  if (clock) {
    var tick = function () {
      try { clock.textContent = new Intl.DateTimeFormat(undefined, { hour: "numeric", minute: "2-digit" }).format(new Date()); }
      catch (e) { clock.parentElement.hidden = true; }
    };
    tick(); setInterval(tick, 15000);
  }

  // Header
  var header = $("#header");
  function onScrollHeader() { header.classList.toggle("scrolled", window.scrollY > 40); }
  onScrollHeader(); window.addEventListener("scroll", onScrollHeader, { passive: true });

  // Mobile menu
  var menuBtn = $("#menu-btn"), menu = $("#mobile-menu");
  function setMenu(open) {
    menu.hidden = !open;
    header.classList.toggle("nav-open", open);
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }
  menuBtn.addEventListener("click", function () { setMenu(menu.hidden); });
  $$("a", menu).forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
  window.addEventListener("resize", function () { if (window.innerWidth > 820) setMenu(false); });

  // Headline rotator
  var rot = $("#rotator");
  if (rot) {
    var glyphs = "abcdefghijklmnopqrstuvwxyz0123456789/<>{}#", wi = 0;
    var decodeTo = function (item) {
      rot.style.setProperty("--c", item.color);
      var word = item.text;
      if (reduce) { rot.textContent = word; return; }
      var frame = 0, total = 20, len = Math.max(rot.textContent.length, word.length);
      (function step() {
        var out = "";
        for (var i = 0; i < len; i++) {
          var settle = (i / len) * total * 0.7 + total * 0.3;
          if (frame >= settle) out += word[i] || "";
          else if (word[i] === " ") out += " ";
          else if (i < word.length || frame < total * 0.5) out += '<span class="scr">' + glyphs[(Math.random() * glyphs.length) | 0] + "</span>";
        }
        rot.innerHTML = out;
        if (frame++ < total) requestAnimationFrame(step); else rot.textContent = word;
      })();
    };
    setInterval(function () { wi = (wi + 1) % ROTATING.length; decodeTo(ROTATING[wi]); }, 3000);
  }

  // Interactive point field (home hero)
  var cv = $("#field");
  if (cv) (function () {
    var ctx = cv.getContext("2d"), hero = cv.parentElement;
    var W = 0, H = 0, visible = true;
    var GX = 0.3, GZ = 0.42, Z0 = 2.6, ROWS = 50, COLS = 120, FOV = 900;
    var mx = 0.7, my = 0.62, tmx = 0.7, tmy = 0.62, energy = 0;
    var STOPS = [[124, 247, 255], [255, 91, 214], [255, 181, 71]];
    function colorAt(u) {
      var seg = u < 0.55 ? 0 : 1, k = seg === 0 ? u / 0.55 : (u - 0.55) / 0.45, a = STOPS[seg], b = STOPS[seg + 1];
      return [(a[0] + (b[0] - a[0]) * k) | 0, (a[1] + (b[1] - a[1]) * k) | 0, (a[2] + (b[2] - a[2]) * k) | 0];
    }
    function resize() {
      var dpr = Math.min(2, window.devicePixelRatio || 1);
      W = cv.clientWidth; H = cv.clientHeight;
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      FOV = Math.max(H * 0.9, 520); ROWS = W < 700 ? 36 : 50;
      COLS = Math.min(200, Math.ceil(W / (GX * FOV / (Z0 + ROWS * GZ))) + 6);
    }
    hero.addEventListener("pointermove", function (e) {
      var r = cv.getBoundingClientRect();
      tmx = (e.clientX - r.left) / r.width; tmy = (e.clientY - r.top) / r.height; energy = 1;
    });
    function draw(ms) {
      var t = ms * 0.001;
      mx += (tmx - mx) * 0.07; my += (tmy - my) * 0.07; energy *= 0.985;
      ctx.clearRect(0, 0, W, H);
      var camH = 1.25, horizon = H * 0.36, cx = W * 0.62;
      var syN = Math.max(0.02, (my * H - horizon) / FOV);
      var mwz = Math.min(Z0 + ROWS * GZ, Math.max(Z0, camH / syN));
      var mwx = (mx * W - cx) / (FOV / mwz);
      var xs = new Float32Array(COLS), ys = new Float32Array(COLS), bs = new Float32Array(COLS);
      for (var z = ROWS - 1; z >= 0; z--) {
        var wz = Z0 + z * GZ, scale = FOV / wz, depth = z / (ROWS - 1);
        var a = Math.pow(1 - depth, 1.3) * 0.9 + 0.08, x;
        for (x = 0; x < COLS; x++) {
          var wx = (x - COLS / 2) * GX;
          var y = Math.sin(wx * 0.55 + t * 0.9) * 0.16 + Math.cos(wz * 0.6 - t * 0.7) * 0.2 + Math.sin((wx * 0.7 + wz) * 0.35 + t * 0.5) * 0.12;
          var dx = wx - mwx, dz = wz - mwz, d2 = dx * dx + dz * dz;
          var bump = Math.exp(-d2 / 3.2) * (0.75 + energy * 0.5);
          y += bump * 0.75 + Math.sin(Math.sqrt(d2) * 2.6 - t * 4.5) * Math.exp(-d2 / 14) * 0.08;
          xs[x] = cx + wx * scale; ys[x] = horizon + (camH - y) * scale; bs[x] = bump;
        }
        var grad = ctx.createLinearGradient(0, 0, W, 0);
        grad.addColorStop(0, "rgba(124,247,255," + (a * 0.28).toFixed(3) + ")");
        grad.addColorStop(0.55, "rgba(255,91,214," + (a * 0.28).toFixed(3) + ")");
        grad.addColorStop(1, "rgba(255,181,71," + (a * 0.26).toFixed(3) + ")");
        ctx.strokeStyle = grad; ctx.lineWidth = 1; ctx.beginPath();
        for (x = 0; x < COLS; x++) { if (x) ctx.lineTo(xs[x], ys[x]); else ctx.moveTo(xs[x], ys[x]); }
        ctx.stroke();
        var s0 = Math.max(1, scale * 0.0045);
        for (x = 0; x < COLS; x++) {
          var px = xs[x], py = ys[x];
          if (px < -4 || px > W + 4 || py < -4 || py > H + 4) continue;
          var b = bs[x], c = colorAt(Math.min(1, Math.max(0, px / W)));
          var alpha = b > 0.08 ? Math.min(1, a + b) : a * 0.7, s = b > 0.08 ? s0 * (1 + b * 1.4) : s0;
          ctx.fillStyle = "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + alpha.toFixed(3) + ")";
          ctx.fillRect(px - s / 2, py - s / 2, s, s);
        }
      }
    }
    function loop(ms) { if (visible && !document.hidden) draw(ms); requestAnimationFrame(loop); }
    resize(); window.addEventListener("resize", resize);
    if (reduce) draw(0); else requestAnimationFrame(loop);
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(hero);
  })();

  // Poster details: Courtside shot clock, festival countdown
  $$("[data-shotclock]").forEach(function (el) {
    var v = 24;
    if (reduce) return;
    setInterval(function () { v = v <= 0.05 ? 24 : v - 0.1; el.textContent = v.toFixed(1); }, 100);
  });
  $$("[data-countdown]").forEach(function (el) {
    var target = new Date(el.getAttribute("data-countdown")).getTime();
    var days = Math.max(0, Math.ceil((target - Date.now()) / 86400000));
    el.textContent = days;
  });

  // Live previews: load the real site into each frame when it scrolls into view
  function fitFrame(f) {
    var view = $(".frame-view", f), ifr = $("iframe", view);
    if (!ifr) return;
    var phone = f.classList.contains("is-phone");
    var w = phone ? 390 : 1440, h = phone ? 760 : 900;
    var scale = view.clientWidth / w;
    ifr.style.width = w + "px";
    ifr.style.height = Math.ceil(view.clientHeight / scale) + "px";
    ifr.style.transform = "scale(" + scale + ")";
  }
  function loadFrame(f) {
    if (f.dataset.loaded || PREVIEW || f.dataset.live !== "1") return;
    if (f.dataset.lazyDesktop === "1" && window.innerWidth < 900) return;
    f.dataset.loaded = "1";
    var view = $(".frame-view", f);
    var ifr = document.createElement("iframe");
    ifr.src = f.dataset.url;
    ifr.title = "Live preview of " + f.dataset.name;
    ifr.loading = "lazy";
    ifr.tabIndex = f.classList.contains("interactive") ? 0 : -1;
    ifr.setAttribute("sandbox", "allow-scripts allow-same-origin allow-forms allow-popups");
    ifr.setAttribute("referrerpolicy", "no-referrer");
    var note = document.createElement("span"); note.className = "loading"; note.textContent = "loading live site…";
    f.classList.add("loading");
    ifr.addEventListener("load", function () { f.classList.remove("loading"); f.classList.add("loaded"); });
    view.appendChild(ifr); view.appendChild(note);
    fitFrame(f);
  }
  var frames = $$(".frame[data-url]");
  if ("IntersectionObserver" in window) {
    var fio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { loadFrame(e.target); fio.unobserve(e.target); } });
    }, { rootMargin: "200px 0px" });
    frames.forEach(function (f) { fio.observe(f); });
  } else frames.forEach(loadFrame);
  window.addEventListener("resize", function () { frames.forEach(fitFrame); });

  // Device toggle on case studies
  $$("[data-device]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var f = document.getElementById(btn.getAttribute("data-target"));
      var phone = btn.getAttribute("data-device") === "phone";
      f.classList.toggle("is-phone", phone);
      $$('[data-target="' + f.id + '"]').forEach(function (b) { b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
      fitFrame(f);
    });
  });

  // Work filters
  var filterBar = $(".filters");
  if (filterBar) {
    var cards = $$(".card[data-tags]");
    $$("button", filterBar).forEach(function (b) {
      b.addEventListener("click", function () {
        var tag = b.getAttribute("data-filter");
        $$("button", filterBar).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        cards.forEach(function (c) { c.hidden = !(tag === "all" || c.getAttribute("data-tags").split(" ").indexOf(tag) !== -1); });
        frames.forEach(fitFrame);
      });
    });
  }

  // Scroll reveal
  var reveals = $$(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    var rio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); rio.unobserve(e.target); } });
    }, { threshold: 0.08, rootMargin: "0px 0px -40px 0px" });
    reveals.forEach(function (el) { rio.observe(el); });
  } else reveals.forEach(function (el) { el.classList.add("in"); });

  // Process progress line
  var steps = $("#steps");
  if (steps) {
    var items = $$("li", steps);
    var onScrollSteps = function () {
      var r = steps.getBoundingClientRect(), vh = window.innerHeight;
      var p = reduce ? 1 : Math.min(1, Math.max(0, (vh * 0.8 - r.top) / (r.height + vh * 0.35)));
      steps.style.setProperty("--progress", p.toFixed(3));
      items.forEach(function (li, i) { li.classList.toggle("lit", p >= (i / items.length) + 0.02 || p >= 0.99); });
    };
    onScrollSteps(); window.addEventListener("scroll", onScrollSteps, { passive: true }); window.addEventListener("resize", onScrollSteps);
  }

  // Footer name
  var giant = $("#giant");
  if (giant) {
    var fitGiant = function () {
      giant.style.fontSize = "100px";
      var cs = getComputedStyle(giant.parentElement);
      var avail = giant.parentElement.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight) - 2;
      giant.style.fontSize = Math.max(24, Math.floor(100 * avail / giant.scrollWidth)) + "px";
    };
    fitGiant(); window.addEventListener("resize", fitGiant);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitGiant);
    giant.parentElement.addEventListener("pointermove", function (e) {
      giant.style.setProperty("--gx", (e.clientX - giant.getBoundingClientRect().left) + "px");
    });
  }

  // Copy buttons
  $$(".copy").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var el = document.getElementById(btn.getAttribute("data-copy"));
      var reset = function () { setTimeout(function () { btn.textContent = "copy"; }, 1600); };
      var fallback = function () {
        var range = document.createRange(); range.selectNodeContents(el);
        var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(range);
        btn.textContent = "selected"; reset();
      };
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(el.textContent.trim()).then(function () { btn.textContent = "copied"; reset(); }, fallback);
        else fallback();
      } catch (e) { fallback(); }
    });
  });

  // Intake form
  var form = $("#intake");
  if (form) {
    var status = $("#form-status"), submit = $("#f-submit");
    var email = form.getAttribute("data-email");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      status.className = "form-status";
      var name = form.elements.name.value.trim(), addr = form.elements.email.value.trim();
      if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(addr)) {
        status.classList.add("err");
        status.textContent = "Add your name and a valid email so I can reply.";
        (name ? form.elements.email : form.elements.name).focus();
        return;
      }
      if (FORM_ENDPOINT.indexOf("YOUR_FORM_ID") !== -1) {
        status.classList.add("err");
        status.textContent = "This form isn't connected yet. Email " + email + " and I'll reply directly.";
        return;
      }
      submit.disabled = true; status.textContent = "Sending…";
      fetch(FORM_ENDPOINT, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (res) {
          if (!res.ok) throw new Error("bad status");
          form.reset(); status.classList.add("ok");
          status.textContent = "Sent. I'll be in touch within two business days.";
        })
        .catch(function () {
          status.classList.add("err");
          status.textContent = "That didn't go through. Email " + email + " and I'll reply directly.";
        })
        .finally(function () { submit.disabled = false; });
    });
  }
})();
