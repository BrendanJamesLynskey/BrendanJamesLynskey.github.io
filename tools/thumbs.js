// The thumbnails of the hardware hubs and the showcase apps (assets/shots/*.webp): a 1280x720 screenshot of
// each live page's first screen, converted to 640x360 WebP with Pillow afterwards (see the README).
//
//   NODE_PATH=<node_modules with puppeteer> node tools/thumbs.js [outdir]
//
// Phatty is shot after its power-on overlay is clicked; the WebGL apps need ANGLE's SwiftShader.
const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");
const PG = "https://brendanjameslynskey.github.io";
const out = process.argv[2] || path.join(__dirname, "out", "thumbs");
fs.mkdirSync(out, { recursive: true });
const PAGES = [
  ["si", `${PG}/Signal_Integrity/`], ["serdes", `${PG}/SerDes_Equalisation/`],
  ["svsim", `${PG}/SystemVerilog_Simulators/`], ["fhe", `${PG}/FHE_Hub_Accelerator_Simulators/`],
  ["simeng", `${PG}/SimEng_Hub_Toolkit/`], ["nss", `${PG}/Neural_Sound_Synthesis/`],
  ["cithub", `${PG}/LLM_Hub_Compute_in_Transit/`], ["hardware", `${PG}/Hardware/`],
  ["phatty", `${PG}/Phatty/app.html`], ["rc", `${PG}/RC-Flight-Line/`], ["class47", `${PG}/Class-47-Cab-Sim/`],
];

(async () => {
  const browser = await puppeteer.launch({
    headless: "new",
    args: ["--no-sandbox", "--mute-audio", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"],
  });
  for (const [key, url] of PAGES) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720 });
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 120000 }).catch((e) => console.log(key, e.message));
    await new Promise((r) => setTimeout(r, 8000));
    if (key === "phatty") { await page.mouse.click(640, 280); await new Promise((r) => setTimeout(r, 4000)); }
    await page.addStyleTag({ content: ".slide{opacity:1!important}" }).catch(() => {});
    await page.screenshot({ path: path.join(out, `${key}.png`) });
    console.log("shot", key);
    await page.close();
  }
  await browser.close();
})();
