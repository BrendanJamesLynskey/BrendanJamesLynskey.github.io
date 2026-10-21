/*
 * The Digital Twin side panel (home, /sites/ and /cv/).
 *
 * The launcher, the Digital Twin card and the hero button are plain links to the twin. This script turns them
 * into openers for a side panel holding the twin in an iframe of /twin/?embed=1, which is same-origin here
 * through vercel.json's rewrite. Desktop: a tall card on the right, the page stays usable beside it. Phone
 * (640 px and narrower): a modal sheet over the page.
 *
 *   - the iframe is created on first open (or when the pointer reaches the launcher), never on page load,
 *     and is kept when the panel closes, so the conversation lasts while you stay on the page;
 *   - closes with its button, Escape (the twin posts a message, as key presses inside an iframe never reach
 *     this page) and, on a phone, a tap on the backdrop; focus moves into the panel and back to the opener;
 *   - a one-time nudge after a few seconds, remembered in localStorage (wrapped: storage can be blocked).
 *
 * On GitHub Pages there is no /twin/, so the links are left alone.
 */
(function () {
  "use strict";
  var launcher = document.getElementById("tw-launch");
  var panel = document.getElementById("tw-panel");
  if (!launcher || !panel || /(^|\.)github\.io$/.test(location.hostname)) return;

  var SRC = "/twin/?embed=1";
  var MSG_READY = "bl-twin:ready", MSG_CLOSE = "bl-twin:close", MSG_FOCUS = "bl-twin:focus";
  var NUDGE_KEY = "bl-twin-nudge", NUDGE_DELAY = 6000;
  var body = document.getElementById("tw-body");
  var scrim = document.getElementById("tw-scrim");
  var nudge = document.getElementById("tw-nudge");
  var closeBtn = document.getElementById("tw-close");
  var root = document.documentElement;
  var phoneQ = window.matchMedia("(max-width: 640px)");
  var frame = null, ready = false, open = false, opener = null, modal = false, nudgeTimer = 0;

  panel.hidden = false;
  scrim.hidden = false;
  launcher.setAttribute("role", "button");
  launcher.setAttribute("aria-haspopup", "dialog");
  launcher.setAttribute("aria-controls", "tw-panel");
  launcher.setAttribute("aria-expanded", "false");

  function store(get, val) {
    try {
      if (get) return localStorage.getItem(NUDGE_KEY);
      localStorage.setItem(NUDGE_KEY, val);
    } catch (e) { /* storage blocked: the nudge may show again */ }
    return null;
  }

  function ensureFrame() {
    if (frame) return;
    frame = document.createElement("iframe");
    frame.title = "Brendan Lynskey's Digital Twin";
    frame.src = SRC;
    frame.addEventListener("load", function () { body.classList.add("ready"); });
    body.appendChild(frame);
  }

  function focusTwin() {
    frame.focus();
    frame.contentWindow.postMessage({ type: MSG_FOCUS }, location.origin);
  }

  // the page behind a phone sheet is inert, so focus and the screen reader stay in the dialog
  function pageInert(on) {
    var kids = document.body.children;
    for (var i = 0; i < kids.length; i++) {
      var el = kids[i];
      if (el === panel || el === scrim || el.tagName === "SCRIPT") continue;
      if (on) el.setAttribute("inert", ""); else el.removeAttribute("inert");
    }
  }

  // on a phone the keyboard shrinks the visual viewport but not a fixed element; keep the sheet inside it
  function fitSheet() {
    var vv = window.visualViewport;
    if (!modal || !vv) return;
    var gap = 12;
    panel.style.setProperty("--tw-y", (vv.offsetTop + gap) + "px");
    panel.style.setProperty("--tw-h", (vv.height - gap) + "px");
  }

  function show(from) {
    if (open) return;
    hideNudge(true);
    ensureFrame();
    open = true;
    opener = from || launcher;
    modal = phoneQ.matches;
    panel.setAttribute("aria-modal", modal ? "true" : "false");
    root.classList.add("tw-open");
    launcher.setAttribute("aria-expanded", "true");
    if (modal) {
      root.classList.add("tw-lock");
      pageInert(true);
      fitSheet();
      if (window.visualViewport) {
        window.visualViewport.addEventListener("resize", fitSheet);
        window.visualViewport.addEventListener("scroll", fitSheet);
      }
    }
    // desktop: straight to the message box; phone: the dialog itself, so the keyboard does not cover the page
    if (!modal && ready) focusTwin();
    else panel.focus({ preventScroll: true });
  }

  function hide() {
    if (!open) return;
    var inside = panel.contains(document.activeElement);
    open = false;
    root.classList.remove("tw-open", "tw-lock");
    launcher.setAttribute("aria-expanded", "false");
    if (modal) {
      pageInert(false);
      if (window.visualViewport) {
        window.visualViewport.removeEventListener("resize", fitSheet);
        window.visualViewport.removeEventListener("scroll", fitSheet);
      }
    }
    var back = opener && document.contains(opener) ? opener : launcher;
    opener = null;
    if (inside || document.activeElement === document.body) back.focus({ preventScroll: true });
  }

  function onOpener(ev) {
    // let new-tab and new-window clicks through to the plain link
    if (ev.defaultPrevented || ev.button !== 0 || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
    ev.preventDefault();
    show(ev.currentTarget);
  }

  var links = document.querySelectorAll("a[data-twin]");
  for (var i = 0; i < links.length; i++) {
    links[i].setAttribute("aria-haspopup", "dialog");
    links[i].addEventListener("click", onOpener);
  }
  // the launcher is a button now: Space presses it too
  launcher.addEventListener("keydown", function (ev) {
    if (ev.key === " ") { ev.preventDefault(); show(launcher); }
  });
  // warm the twin when the pointer reaches the launcher, so it is usually ready by the click
  launcher.addEventListener("pointerenter", ensureFrame);

  closeBtn.addEventListener("click", hide);
  scrim.addEventListener("click", hide);
  document.addEventListener("keydown", function (ev) {
    if (open && ev.key === "Escape") { ev.preventDefault(); hide(); }
  });
  window.addEventListener("message", function (ev) {
    if (!frame || ev.source !== frame.contentWindow || ev.origin !== location.origin || !ev.data) return;
    if (ev.data.type === MSG_READY) {
      ready = true;
      body.classList.add("ready");
      // focus was parked on the panel while the twin loaded; hand it to the message box
      if (open && !modal && document.activeElement === panel) focusTwin();
    } else if (ev.data.type === MSG_CLOSE && open) hide();
  });

  // the nudge: once, a few seconds in, never while the panel is or has been open
  function hideNudge(remember) {
    clearTimeout(nudgeTimer);
    if (remember) store(false, "1");
    if (nudge.hidden) return;
    nudge.classList.remove("on");
    nudge.hidden = true;
  }
  if (!store(true)) {
    nudgeTimer = setTimeout(function () {
      if (open || frame) return;
      store(false, "1");
      nudge.hidden = false;
      requestAnimationFrame(function () { requestAnimationFrame(function () { nudge.classList.add("on"); }); });
    }, NUDGE_DELAY);
  }
  nudge.querySelector(".tw-nudge-open").addEventListener("click", function () { show(launcher); });
  nudge.querySelector(".tw-nudge-x").addEventListener("click", function () {
    hideNudge(true);
    launcher.focus({ preventScroll: true });
  });
})();
