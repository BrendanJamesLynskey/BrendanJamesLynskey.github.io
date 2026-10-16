// Render tools/out/og.html -> og.png (1200x630) and tools/out/apple.html -> apple-touch-icon.png (180x180).
// Needs puppeteer (NODE_PATH pointing at a node_modules that has it). Run tools/brand.py first.
const path = require("path");
const puppeteer = require("puppeteer");
const ROOT = path.resolve(__dirname, "..");

(async () => {
  for (const [src, out, w, h] of [["og.html", "og.png", 1200, 630], ["apple.html", "apple-touch-icon.png", 180, 180]]) {
    // one browser per image, sized to it: a resized default window tiled the capture
    const browser = await puppeteer.launch({
      headless: "shell", defaultViewport: { width: w, height: h, deviceScaleFactor: 1 },
      args: ["--no-sandbox", "--allow-file-access-from-files", `--window-size=${w},${h}`],
    });
    const page = await browser.newPage();
    await page.goto("file://" + path.join(ROOT, "tools", "out", src), { waitUntil: "load" });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(ROOT, out), captureBeyondViewport: false });
    await browser.close();
    console.log("wrote", out);
  }
})();
