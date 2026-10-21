# brendanjameslynskey.github.io

The portfolio home page, CV and Digital Twin card: **[brendan-lynskey.vercel.app](https://brendan-lynskey.vercel.app/)**
(the canonical address). GitHub Pages serves the same files from `main` at
[brendanjameslynskey.github.io](https://brendanjameslynskey.github.io/), so old links still work; their canonical
tags point to Vercel.

- [`index.html`](index.html): the landing page: who I am, the CV, Digital Twin and contact cards, and one tile per
  part of the portfolio. Old links to its former sections (`/#sites`, `/#hardware`, …) are sent on to `/sites/`.
- [`sites/index.html`](sites/index.html): the **portfolio**, built for my own learning: hardware, DSP and signal
  integrity first, then the sixteen interactive sites in their four tracks, the showcases, the verification summary,
  the deck library and how the work is built.
- [`library/index.html`](library/index.html): the **library**, one row per subject index (LLMs, Hardware, Software,
  Mathematics, DSP & Music, Miscellaneous) with links to its series hubs, from `LIBRARY` in
  [`tools/content.py`](tools/content.py); the GitHub profile README's "Browse the library" table uses the same rows.
- [`optalysys/index.html`](optalysys/index.html): a landing page for the work built while learning the areas
  Optalysys works in (the photonic link module site, silicon photonics, FHE, compute in transit, Fourier optics and
  simulation engineering), with what each does and why it was built. The entries are in
  [`tools/optalysys.py`](tools/optalysys.py); the page is `noindex`, left out of the sitemap, and linked from the
  landing page only by a small "O" in the footer.
- [`checks/index.html`](checks/index.html): **How I check the numbers**, every site's check, quoted from its source.
- [`cv/index.html`](cv/index.html): the **CV**, generated from [`src/cv_source.md`](src/cv_source.md) by
  [`tools/cv.py`](tools/cv.py), with a career timeline and the PDF,
  [`cv/Brendan_Lynskey_CV.pdf`](cv/Brendan_Lynskey_CV.pdf).
- [`src/cv_source.md`](src/cv_source.md): the facts behind the CV page (the only source for `/cv/`), and
  [`docs/landing_brief.md`](docs/landing_brief.md): the brief for the CV page, the Digital Twin card and the move to
  brendan-lynskey.vercel.app.
- [`404.html`](404.html), [`sitemap.xml`](sitemap.xml), [`robots.txt`](robots.txt), [`og.png`](og.png) (the
  link-preview card), [`favicon.svg`](favicon.svg) and [`apple-touch-icon.png`](apple-touch-icon.png).

It is a static site: plain HTML and CSS, one small script ([`assets/hero.js`](assets/hero.js), the hero animation,
which honours `prefers-reduced-motion`), system fonts and local images. It makes no external requests.

## How it is built

Nothing on the page that has a source is typed in by hand.

| Step | Command | What it does |
|---|---|---|
| Gather | `python3 tools/gather.py` | Reads each site's name, track and blurb from the shared site switch, its "How this is checked" line, evidence link, favicon and card from the live landing page, and the deck counts from the index READMEs; writes [`data/`](data/), [`assets/icons/`](assets/icons/) and [`assets/cards/`](assets/cards/) |
| Build | `python3 tools/build.py` | Writes the pages from `data/`, [`tools/content.py`](tools/content.py) (the hubs, showcases, quotes and the Digital Twin card), [`src/how-this-is-built.html`](src/how-this-is-built.html) and, for `/cv/`, [`src/cv_source.md`](src/cv_source.md) |
| CV PDF | `node tools/cv_pdf.js` (with `python3 -m http.server 8740` running) | Prints `/cv/` with its print stylesheet to `cv/Brendan_Lynskey_CV.pdf` (A4, two pages at most) |
| Brand | `python3 tools/brand.py && node tools/render_brand.js` | The favicon, the card and the touch icon |
| Profile | `python3 tools/profile_readme.py <path>` | The GitHub profile README, from the same data |

Checks (run before publishing):

| Check | Command |
|---|---|
| Every quote still appears, word for word, on its source page | `python3 tools/check_quotes.py` |
| Every link returns 200 | `python3 tools/check_links.py` |
| Every experience entry, date range, education item, award, certification and skill in `src/cv_source.md` is on `/cv/`, and nothing else in those categories | `python3 tools/check_cv.py` |
| Each page at 1280 and 390 px, light and dark: no page errors, no horizontal overflow, axe clean, no external requests | `node tools/check_pages.js` (with `python3 -m http.server 8740` running) |

## The Digital Twin card

The Digital Twin is a chat agent that answers questions about my career in my voice. It lives in its own private
repository (BrendanJamesLynskey/Digital_Twin, a Next.js app on the Vercel project `brendan-lynskey-twin`) and is
served at [brendan-lynskey.vercel.app/twin/](https://brendan-lynskey.vercel.app/twin/) through the rewrites in
[`vercel.json`](vercel.json). The home page's Digital Twin card, the hero's "Ask my Digital Twin" button and the
CV page's link all come from `DIGITAL_TWIN` in [`tools/content.py`](tools/content.py). With `"url"` set to `None`
the card falls back to "new version coming soon" and links the earlier version (`"interim_url"`, the
CareerConversation Space); change it and run `python3 tools/build.py`.

## Deploying

The owner deploys: [`tools/deploy_vercel.sh`](tools/deploy_vercel.sh) takes a `git archive` of `origin/main` and
deploys it to the Vercel project `brendan-lynskey` ([`vercel.json`](vercel.json): static, no build step, clean URLs,
trailing slashes; [`.vercelignore`](.vercelignore) keeps `tools/`, `docs/`, `src/` and `data/` out), then checks the
live pages answer, including the Digital Twin at `/twin/`. To deploy both projects, the twin first:
[`tools/deploy_both.sh`](tools/deploy_both.sh) runs the twin's own `tools/deploy_twin.sh` (from a clone of the
twin repository next to this one, or `TWIN_REPO=...`) and then `tools/deploy_vercel.sh`.

The thumbnails in [`assets/shots/`](assets/shots/) are screenshots of each page's first screen
([`tools/thumbs.js`](tools/thumbs.js)), resized to 640×360 WebP.

The work is built with Claude Code as an agentic engineering workflow; commits made this way carry a
`Co-Authored-By` line. See "How this is built" on the portfolio page.
