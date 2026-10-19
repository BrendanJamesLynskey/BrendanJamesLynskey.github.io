// Browser check of the built pages, served locally (python3 -m http.server 8740 from the repo root).
//
//   NODE_PATH=<node_modules with puppeteer and axe-core> node tools/check_pages.js [base] [outdir]
//
// For each page at 1280 and 390 px, light and dark: zero page errors, no horizontal overflow
// (scrollWidth <= clientWidth), axe-core with the WCAG 2.x A/AA tags, and a full-page screenshot.
// External requests are blocked (the pages make none; this proves it). Exits non-zero on any failure.
const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");
const axeSource = fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");

const base = process.argv[2] || "http://127.0.0.1:8740";
const out = process.argv[3] || path.join(__dirname, "out", "shots");
fs.mkdirSync(out, { recursive: true });
const pages = [["home", "/"], ["sites", "/sites/"], ["checks", "/checks/"], ["cv", "/cv/"], ["optalysys", "/optalysys/"], ["404", "/404.html"]];
const modes = [[1280, "light"], [1280, "dark"], [390, "light"], [390, "dark"]];

(async () => {
  const browser = await puppeteer.launch({ headless: "shell", args: ["--no-sandbox"] });
  let failures = 0;
  for (const [name, p] of pages) for (const [w, scheme] of modes) {
    const page = await browser.newPage();
    const errors = [], external = [];
    page.on("pageerror", (e) => errors.push(e.message));
    page.on("console", (m) => { if (m.type() === "error") errors.push("console: " + m.text()); });
    await page.setRequestInterception(true);
    page.on("request", (r) => {
      if (r.url().startsWith(base) || r.url().startsWith("data:")) r.continue();
      else { external.push(r.url()); r.abort(); }
    });
    await page.setViewport({ width: w, height: w > 500 ? 800 : 844, deviceScaleFactor: 1 });
    await page.emulateMediaFeatures([{ name: "prefers-color-scheme", value: scheme }]);
    await page.goto(base + p, { waitUntil: "load" });
    // load the lazy images before the full-page screenshot
    await page.evaluate(async () => {
      document.querySelectorAll("img[loading=lazy]").forEach((i) => (i.loading = "eager"));
      await Promise.all([...document.images].map((i) => i.complete ? 0 : new Promise((r) => (i.onload = i.onerror = r))));
    });
    await new Promise((r) => setTimeout(r, 2500));
    const overflow = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
    await page.addScriptTag({ content: axeSource });
    const axe = await page.evaluate(async () => {
      const r = await window.axe.run(document, { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"] } });
      return r.violations.map((v) => `${v.id} (${v.impact}): ${v.nodes.length} nodes, e.g. ${v.nodes[0].target.join(" ")}`);
    });
    const file = path.join(out, `${name}_${w}_${scheme}.png`);
    await page.screenshot({ path: file, fullPage: true, captureBeyondViewport: true });
    const ok = errors.length === 0 && overflow.sw <= overflow.cw && axe.length === 0 && external.length === 0;
    failures += !ok;
    console.log(`${ok ? "ok  " : "FAIL"} ${name} ${w} ${scheme}: errors ${errors.length}, scrollWidth ${overflow.sw}/${overflow.cw}, axe ${axe.length}, external ${external.length}`);
    for (const x of [...errors, ...axe, ...external]) console.log("     " + x);
    await page.close();
  }
  // the hero animates normally, holds a still frame under prefers-reduced-motion, and its button pauses it
  for (const reduce of ["no-preference", "reduce"]) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    await page.emulateMediaFeatures([{ name: "prefers-reduced-motion", value: reduce }]);
    await page.goto(base + "/", { waitUntil: "load" });
    const grab = () => page.evaluate(() => document.getElementById("hero-canvas").toDataURL());
    await new Promise((r) => setTimeout(r, 500));
    const a = await grab(); await new Promise((r) => setTimeout(r, 1200)); const b = await grab();
    const label = await page.$eval("#hero-pause", (x) => x.textContent);
    let pausedStill = true;
    if (reduce === "no-preference") {
      await page.click("#hero-pause"); await new Promise((r) => setTimeout(r, 300));
      const c = await grab(); await new Promise((r) => setTimeout(r, 1200)); pausedStill = c === (await grab());
    }
    const ok = reduce === "reduce" ? a === b && label === "Play" : a !== b && label === "Pause" && pausedStill;
    failures += !ok;
    console.log(`${ok ? "ok  " : "FAIL"} hero, prefers-reduced-motion: ${reduce}: frames ${a === b ? "still" : "moving"}, button "${label}"${reduce === "no-preference" ? `, still after Pause: ${pausedStill}` : ""}`);
    await page.close();
  }
  // the CV timeline: tabbing to a band shows its role, the hint hides, and the band links to the role's entry
  {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    await page.goto(base + "/cv/", { waitUntil: "load" });
    const bands = await page.$$eval(".tl-svg a", (as) => as.map((a) => [a.dataset.r, a.getAttribute("href")]));
    let shown = 0;
    // tab from the top of the page to the first band, then through the bands in order
    for (let i = 0; i < 60 && !(await page.evaluate(() => !!document.activeElement.closest(".tl-svg"))); i++)
      await page.keyboard.press("Tab");
    for (const [r, href] of bands) {
      if (r !== (await page.evaluate(() => document.activeElement.dataset && document.activeElement.dataset.r))) break;
      const st = await page.evaluate((r, href) => ({
        out: getComputedStyle(document.querySelector(`[data-o="${r}"]`)).display,
        hint: getComputedStyle(document.querySelector(".tl-hint")).display,
        target: !!document.querySelector(href),
      }), r, href);
      shown += st.out === "block" && st.hint === "none" && st.target;
      await page.keyboard.press("Tab");
    }
    const ok = bands.length > 0 && shown === bands.length;
    failures += !ok;
    console.log(`${ok ? "ok  " : "FAIL"} cv timeline: ${shown}/${bands.length} bands show their label on focus and link to an entry`);
    await page.close();
  }
  await browser.close();
  process.exit(failures ? 1 : 0);
})();
