// Print /cv/ to cv/Brendan_Lynskey_CV.pdf (A4, two pages at most), with the page's print stylesheet.
//
//   python3 -m http.server 8740 &      # from the repo root
//   NODE_PATH=<node_modules with puppeteer> node tools/cv_pdf.js [base]
//
// The print stylesheet (in tools/build.py) drops the header, the footer, the theme and the timeline's
// hover labels; the links stay clickable in the PDF. Exits non-zero if the PDF runs past two pages.
const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");

const base = process.argv[2] || "http://127.0.0.1:8740";
const out = path.join(__dirname, "..", "cv", "Brendan_Lynskey_CV.pdf");

(async () => {
  const browser = await puppeteer.launch({ headless: "shell", args: ["--no-sandbox"] });
  const page = await browser.newPage();
  await page.emulateMediaFeatures([{ name: "prefers-color-scheme", value: "light" }]);
  await page.goto(base + "/cv/", { waitUntil: "networkidle0" });
  await page.emulateMediaType("print");
  const pdf = await page.pdf({ format: "A4", printBackground: true, preferCSSPageSize: true, tagged: true, outline: false });
  await browser.close();
  fs.writeFileSync(out, pdf);
  const pages = (Buffer.from(pdf).toString("latin1").match(/\/Type\s*\/Page(?!s)/g) || []).length;
  console.log(`wrote ${path.relative(process.cwd(), out)}: ${pages} page(s), ${pdf.length} bytes`);
  process.exit(pages >= 1 && pages <= 2 ? 0 : 1);
})();
