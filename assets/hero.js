/*
 * The home page's hero figure: an agent loop drives a 4x4 output-stationary systolic array.
 *
 *   act      the loop sends the operands into the array (A from the left, B from the top, skewed);
 *   compute  each operand moves one PE per cycle; PE(i, j) does its k-th multiply-accumulate at
 *            cycle i + j + k, so the wavefront runs corner to corner and fills each PE in turn;
 *   observe  the results drain out to the loop;
 *   check    the loop compares them with a reference and only then plans the next step.
 *
 * An illustration, not a simulation: the timing is the textbook output-stationary schedule.
 * Plain canvas, no libraries. Honours prefers-reduced-motion (one still frame), pauses when the
 * figure is off screen or the tab is hidden, and has a pause button.
 */
(function () {
  "use strict";
  var canvas = document.getElementById("hero-canvas");
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext("2d");
  var btn = document.getElementById("hero-pause");
  var W = 560, H = 300;           // logical size; the canvas is scaled to its box
  var N = 4, K = 4;               // array size, inner dimension
  var CELL = 34, GAP = 9, PITCH = CELL + GAP;
  var GX = 58, GY = 78;           // top-left of the array
  var LC = { x: 432, y: 150 }, LR = 84;   // the agent loop
  var NODES = [                   // the loop runs act -> observe -> check -> plan -> act
    { k: "plan", a: -90 }, { k: "act", a: 180 }, { k: "observe", a: 90 }, { k: "check", a: 0 }
  ];
  // phase boundaries in seconds; one period is one turn of the loop
  var T_ACT = 1.4, T_COMP = 7.0, T_DRAIN = 8.6, T_LOOP = 12.6;
  var CYCLES_PER_S = (2 * (N - 1) + K + 1) / (T_COMP - T_ACT);

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");
  var running = !(reduce && reduce.matches);
  var visible = true, t0 = null, tPaused = 0, colours = null;

  function css(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }
  function readColours() {
    colours = {
      text: css("--text"), muted: css("--faint"), border: css("--border"), surface: css("--surface"),
      bg: css("--bg"), a: css("--hw"), b: css("--hw2"), acc: css("--accent-line"), ok: css("--ok")
    };
  }
  function node(k) {
    for (var i = 0; i < NODES.length; i++) if (NODES[i].k === k) {
      var r = NODES[i].a * Math.PI / 180;
      return { x: LC.x + LR * Math.cos(r), y: LC.y + LR * Math.sin(r), a: NODES[i].a };
    }
  }
  function cellXY(i, j) { return { x: GX + j * PITCH, y: GY + i * PITCH }; }
  function lerp(a, b, u) { return a + (b - a) * u; }
  function clamp(x, a, b) { return Math.max(a, Math.min(b, x)); }
  function ease(u) { return u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2; }

  // quadratic Bezier paths between the loop and the array
  var ACT_PATH, OBS_PATH;
  function paths() {
    var act = node("act"), obs = node("observe");
    ACT_PATH = [act, { x: 300, y: 28 }, { x: GX + 1.5 * PITCH + CELL / 2, y: GY - 34 }];
    OBS_PATH = [{ x: GX + N * PITCH - GAP + 4, y: GY + 3 * PITCH + CELL / 2 },
                { x: 330, y: 272 }, obs];
  }
  function bez(p, u) {
    var a = 1 - u;
    return { x: a * a * p[0].x + 2 * a * u * p[1].x + u * u * p[2].x,
             y: a * a * p[0].y + 2 * a * u * p[1].y + u * u * p[2].y };
  }
  function strokePath(p, colour, dash) {
    ctx.save();
    ctx.strokeStyle = colour; ctx.lineWidth = 1.5; ctx.setLineDash(dash || []);
    ctx.beginPath(); ctx.moveTo(p[0].x, p[0].y); ctx.quadraticCurveTo(p[1].x, p[1].y, p[2].x, p[2].y);
    ctx.stroke(); ctx.restore();
  }
  function dot(x, y, r, colour) {
    ctx.fillStyle = colour; ctx.beginPath(); ctx.arc(x, y, r, 0, 2 * Math.PI); ctx.fill();
  }
  var textScale = 1;   // labels stay about 9.5 px on screen when the canvas is narrow
  function label(text, x, y, align, colour, size) {
    ctx.fillStyle = colour || colours.muted;
    ctx.font = ((size || 11) * textScale).toFixed(1) + "px ui-monospace, SFMono-Regular, Menlo, monospace";
    ctx.textAlign = align || "center"; ctx.textBaseline = "middle";
    ctx.fillText(text, x, y);
  }

  function draw(t) {
    var p = t % T_LOOP;
    ctx.clearRect(0, 0, W, H);
    // --- connectors
    strokePath(ACT_PATH, colours.border, [4, 4]);
    strokePath(OBS_PATH, colours.border, [4, 4]);
    // --- the array
    var c = p < T_ACT ? -1 : (p - T_ACT) * CYCLES_PER_S - 1;   // cycle, continuous
    var fade = p > T_DRAIN ? clamp(1 - (p - T_DRAIN) / 1.2, 0, 1) : 1;
    for (var i = 0; i < N; i++) for (var j = 0; j < N; j++) {
      var q = cellXY(i, j);
      var done = clamp(c - i - j + 1, 0, K) / K;                  // MACs done, as a fraction
      if (p > T_COMP) done = 1;
      var fill = done * fade;
      ctx.fillStyle = colours.surface; ctx.strokeStyle = colours.border; ctx.lineWidth = 1;
      roundRect(q.x, q.y, CELL, CELL, 5); ctx.fill(); ctx.stroke();
      if (fill > 0) {
        ctx.globalAlpha = 0.18 + 0.62 * fill;
        ctx.fillStyle = colours.a;
        var h = CELL * fill;
        roundRect(q.x, q.y + CELL - h, CELL, h, 5); ctx.fill();
        ctx.globalAlpha = 1;
      }
      // a MAC happening right now: a ring on the PE
      var k = Math.floor(c) - i - j;
      if (p >= T_ACT && p < T_COMP && k >= 0 && k < K) {
        var f = c - Math.floor(c);
        ctx.strokeStyle = colours.b; ctx.lineWidth = 2; ctx.globalAlpha = 1 - f;
        roundRect(q.x - 2, q.y - 2, CELL + 4, CELL + 4, 7); ctx.stroke(); ctx.globalAlpha = 1;
      }
    }
    // operands in flight: a[i][k] reaches column j at cycle i + j + k; b[k][j] reaches row i then too
    if (p >= T_ACT && p < T_COMP + 0.4) {
      for (var r = 0; r < N; r++) for (var kk = 0; kk < K; kk++) {
        var col = c - r - kk;                     // continuous column position of a[r][kk]
        if (col > -1.6 && col < N - 0.5) {
          var x = GX + col * PITCH + CELL / 2, y = GY + r * PITCH + CELL / 2;
          dot(x - CELL / 2 - GAP / 2 + 2, y, 3.2, colours.a);
        }
        var row = c - r - kk;                     // b[kk][r] travelling down column r
        if (row > -1.6 && row < N - 0.5) {
          var bx = GX + r * PITCH + CELL / 2, by = GY + row * PITCH + CELL / 2;
          dot(bx, by - CELL / 2 - GAP / 2 + 2, 3.2, colours.b);
        }
      }
    }
    label("systolic array", GX + (N * PITCH - GAP) / 2, GY + N * PITCH + 12);
    label("A →", GX - 30, GY + CELL / 2, "center", colours.a);
    label("B ↓", GX - 30, GY - 22, "center", colours.b);
    // --- act: the operands leave the loop for the array
    if (p < T_ACT) {
      var u = ease(p / T_ACT);
      for (var d = 0; d < 3; d++) {
        var uu = clamp(u - d * 0.08, 0, 1);
        if (uu > 0 && uu < 1) { var pt = bez(ACT_PATH, uu); dot(pt.x, pt.y, 3.5 - d * 0.7, colours.acc); }
      }
    }
    // --- observe: the results drain to the loop
    if (p > T_COMP && p < T_DRAIN + 0.2) {
      var v = clamp((p - T_COMP) / (T_DRAIN - T_COMP), 0, 1);
      for (var e = 0; e < 4; e++) {
        var ve = clamp(v * 1.3 - e * 0.1, 0, 1);
        if (ve > 0 && ve < 1) { var po = bez(OBS_PATH, ease(ve)); dot(po.x, po.y, 3.5, colours.a); }
      }
    }
    // --- the agent loop
    ctx.strokeStyle = colours.border; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.arc(LC.x, LC.y, LR, 0, 2 * Math.PI); ctx.stroke();
    label("agent loop", LC.x, LC.y, "center", colours.muted, 12);
    // the loop's token: at act during compute, then observe -> check -> plan -> act
    var ang;
    if (p < T_DRAIN) ang = 180;                                   // waiting at act / observe
    else ang = 90 - 270 * ease(clamp((p - T_DRAIN) / (T_LOOP - T_DRAIN - 0.3), 0, 1));
    if (p >= T_COMP && p < T_DRAIN) ang = 90 + 90 * (1 - ease(clamp((p - T_COMP) / (T_DRAIN - T_COMP), 0, 1)));
    var active = null;
    for (var n = 0; n < NODES.length; n++) {
      var nd = node(NODES[n].k);
      var da = Math.abs(((ang - NODES[n].a) % 360 + 540) % 360 - 180);
      var on = da < 14;
      if (on) active = NODES[n].k;
      var isCheck = NODES[n].k === "check";
      var colour = on ? (isCheck ? colours.ok : colours.acc) : colours.border;
      ctx.fillStyle = colours.bg; ctx.strokeStyle = colour; ctx.lineWidth = on ? 2.5 : 1.5;
      ctx.beginPath(); ctx.arc(nd.x, nd.y, 9, 0, 2 * Math.PI); ctx.fill(); ctx.stroke();
      if (on) dot(nd.x, nd.y, 4, colour);
      var lx = nd.x;
      var ly = nd.y + (NODES[n].a === -90 ? -20 : NODES[n].a === 90 ? 21 : 22);
      label(NODES[n].k, lx, ly, "center", on ? colours.text : colours.muted);
    }
    var tok = { x: LC.x + LR * Math.cos(ang * Math.PI / 180), y: LC.y + LR * Math.sin(ang * Math.PI / 180) };
    dot(tok.x, tok.y, 5, active === "check" ? colours.ok : colours.acc);
    // the check passes: a tick and its reason
    var pc = node("check");
    var tc = T_DRAIN + (T_LOOP - T_DRAIN - 0.3) * Math.sqrt(1 / 6);   // ease(u) = 1/3
    var since = p - tc;
    if (since > -0.25 && since < 2.2) {
      ctx.globalAlpha = clamp(1 - Math.max(0, since - 1.4) / 0.8, 0, 1);
      ctx.strokeStyle = colours.ok; ctx.lineWidth = 2.5; ctx.lineCap = "round";
      ctx.beginPath(); ctx.moveTo(pc.x - 6, pc.y - 30); ctx.lineTo(pc.x, pc.y - 24);
      ctx.lineTo(pc.x + 10, pc.y - 38); ctx.stroke(); ctx.lineCap = "butt";
      label("= reference", pc.x - 4, pc.y - 52, "center", colours.ok);
      ctx.globalAlpha = 1;
    }
  }

  function roundRect(x, y, w, h, r) {
    r = Math.min(r, h / 2, w / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }

  function resize() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = canvas.clientWidth || W;
    textScale = clamp((9.5 / 11) * (W / w), 1, 1.5);
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(w * H / W * dpr);
    ctx.setTransform(canvas.width / W, 0, 0, canvas.height / H, 0, 0);
  }

  var STILL = T_ACT + 4.6 / CYCLES_PER_S;   // mid-wavefront, for reduced motion and while paused
  function frame(now) {
    if (!running || !visible) { t0 = null; return; }
    if (t0 === null) t0 = now / 1000 - tPaused;
    tPaused = now / 1000 - t0;
    draw(tPaused);
    requestAnimationFrame(frame);
  }
  function start() { if (running && visible) requestAnimationFrame(frame); }
  function still() { draw(tPaused || STILL); }

  function setButton() {
    if (!btn) return;
    btn.textContent = running ? "Pause" : "Play";
    btn.setAttribute("aria-pressed", running ? "false" : "true");
    btn.setAttribute("aria-label", running ? "Pause the animation" : "Play the animation");
  }
  if (btn) btn.addEventListener("click", function () {
    running = !running; setButton();
    if (running) start(); else still();
  });

  readColours(); paths(); resize(); setButton();
  if (running) start(); else draw(STILL);

  window.addEventListener("resize", function () { resize(); if (!running) still(); });
  var dark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)");
  function rescheme() { readColours(); if (!running) still(); }
  if (dark && dark.addEventListener) dark.addEventListener("change", rescheme);
  if (reduce && reduce.addEventListener) reduce.addEventListener("change", function () {
    running = !reduce.matches; setButton(); if (running) start(); else still();
  });
  document.addEventListener("visibilitychange", function () {
    visible = !document.hidden; if (visible) start();
  });
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) {
      visible = es[0].isIntersecting && !document.hidden; if (visible) start();
    }).observe(canvas);
  }
})();
