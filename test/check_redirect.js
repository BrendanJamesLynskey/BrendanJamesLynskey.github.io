// Browser test of the redirect stub: serves this folder the way GitHub Pages does (a file if it exists, else
// 404.html with status 404), opens old addresses in Chrome and checks where each one lands.
//
//   NODE_PATH=<node_modules with puppeteer or puppeteer-core> node test/check_redirect.js
//
// With JavaScript, every path, query and anchor must land on the same place on https://brendanlynskey.com; without
// it, the meta refresh must land on https://brendanlynskey.com/. Requests to brendanlynskey.com are answered
// locally (nothing is fetched from the internet), and any other outside request fails the test. Each page must
// also carry the canonical link, robots noindex and the one visible line. Exits non-zero on any failure.
const http = require("http");
const fs = require("fs");
const path = require("path");
let puppeteer;
try { puppeteer = require("puppeteer"); } catch { puppeteer = require("puppeteer-core"); }

const ROOT = path.resolve(__dirname, "..");
const TARGET = "https://brendanlynskey.com";
// old addresses (path + query + hash) that other pages link to, and the 200/404 GitHub Pages gives each
const CASES = ["/", "/#sites", "/#track-agents", "/?utm=x#hardware", "/sites/", "/sites/#showcases", "/cv/",
  "/cv/#experience", "/cv/Brendan_Lynskey_CV.pdf", "/checks/", "/library/", "/library/?q=dsp", "/index.html", "/404.html",
  "/no/such/page/", "/twin/"];

function serve() {
  const server = http.createServer((req, res) => {
    const p = decodeURIComponent(new URL(req.url, "http://x").pathname);
    let f = path.join(ROOT, p.endsWith("/") ? p + "index.html" : p);
    let status = 200;
    if (!f.startsWith(ROOT) || !fs.existsSync(f) || !fs.statSync(f).isFile() || f.includes(`${path.sep}test${path.sep}`)) {
      f = path.join(ROOT, "404.html"); status = 404;
    }
    res.writeHead(status, { "content-type": f.endsWith(".html") ? "text/html; charset=utf-8" : "application/octet-stream" });
    fs.createReadStream(f).pipe(res);
  });
  return new Promise((ok) => server.listen(0, "127.0.0.1", () => ok(server)));
}

(async () => {
  const server = await serve();
  const base = `http://127.0.0.1:${server.address().port}`;
  const browser = await puppeteer.launch({ headless: "new", executablePath: "/usr/bin/google-chrome",
    args: ["--no-sandbox", "--mute-audio"] });
  let fails = 0;
  const report = (ok, msg) => { fails += !ok; console.log(`${ok ? "ok  " : "FAIL"}  ${msg}`); };
  try {
    for (const js of [true, false]) {
      for (const c of js ? CASES : ["/", "/cv/", "/sites/#showcases"]) {
        const page = await browser.newPage();
        await page.setJavaScriptEnabled(js);
        const errors = [], outside = [], statuses = {};
        page.on("pageerror", (e) => errors.push(e.message));
        await page.setRequestInterception(true);
        page.on("request", (r) => {
          const u = r.url();
          if (u.startsWith(base)) return r.continue();
          if (u.startsWith(TARGET + "/")) return r.respond({ status: 200, contentType: "text/html", body: "<title>arrived</title>" });
          outside.push(u); r.abort();
        });
        page.on("response", (r) => { if (r.url().startsWith(base)) statuses[r.url().split("#")[0]] = r.status(); });
        // the stub's own page first, without following the redirect, to read what it carries
        const want = js ? TARGET + c : TARGET + "/";
        const arrived = page.waitForFunction((t) => location.href.startsWith(t), { timeout: 10000 }, TARGET);
        await page.goto(base + c, { waitUntil: "domcontentloaded" }).catch(() => {});
        await arrived.catch(() => {});
        await new Promise((r) => setTimeout(r, 300)); // a second, later navigation (the fallback) would show here
        const got = page.url();
        const status = statuses[base + c.split("#")[0]];
        const wantStatus = ["/", "/index.html", "/404.html"].includes(c.split(/[?#]/)[0]) ? 200 : 404;
        report(got === want && status === wantStatus && !errors.length && !outside.length,
          `${js ? "js   " : "no-js"} ${c} (${status}) -> ${got}${got === want ? "" : `, want ${want}`}`
          + (errors.length ? ` errors: ${errors}` : "") + (outside.length ? ` outside: ${outside}` : ""));
        await page.close();
      }
    }
    // what the pages carry, read from the files GitHub Pages serves
    for (const f of ["index.html", "404.html"]) {
      const s = fs.readFileSync(path.join(ROOT, f), "utf8");
      const page = await browser.newPage();
      await page.setJavaScriptEnabled(false);
      await page.setViewport({ width: 390, height: 844 });
      await page.setContent(s);
      const t = await page.evaluate(() => ({
        canonical: document.querySelector('link[rel="canonical"]')?.href,
        robots: document.querySelector('meta[name="robots"]')?.content,
        text: document.body.innerText.trim(),
        link: document.querySelector("body a")?.href,
        bg: getComputedStyle(document.body).backgroundColor,
        overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      }));
      report(t.canonical === TARGET + "/" && t.robots === "noindex" && t.text === "This page has moved to brendanlynskey.com."
        && t.link === TARGET + "/" && t.bg === "rgb(246, 245, 240)" && !t.overflow && !/optalysys/i.test(s) && !/<link[^>]+stylesheet|src=/i.test(s),
        `${f}: canonical ${t.canonical}, robots ${t.robots}, text "${t.text}", link ${t.link}, background ${t.bg}`);
      await page.close();
    }
  } finally {
    await browser.close();
    server.close();
  }
  console.log(fails ? `${fails} failure(s)` : "all redirects ok");
  process.exit(fails ? 1 : 0);
})();
