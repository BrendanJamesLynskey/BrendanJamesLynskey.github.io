# brendanjameslynskey.github.io

The portfolio home page: **[brendanjameslynskey.github.io](https://brendanjameslynskey.github.io/)**.

- [`index.html`](index.html): the home page: hardware, DSP and signal integrity first, then the sixteen interactive
  sites in their four tracks, the showcases, the verification summary, the deck library and how the work is built.
- [`checks/index.html`](checks/index.html): **How I check the numbers**, every site's check, quoted from its source.
- [`404.html`](404.html), [`sitemap.xml`](sitemap.xml), [`robots.txt`](robots.txt), [`og.png`](og.png) (the
  link-preview card), [`favicon.svg`](favicon.svg) and [`apple-touch-icon.png`](apple-touch-icon.png).

It is a static site: plain HTML and CSS, one small script ([`assets/hero.js`](assets/hero.js), the hero animation,
which honours `prefers-reduced-motion`), system fonts and local images. It makes no external requests.

## How it is built

Nothing on the page that has a source is typed in by hand.

| Step | Command | What it does |
|---|---|---|
| Gather | `python3 tools/gather.py` | Reads each site's name, track and blurb from the shared site switch, its "How this is checked" line, evidence link, favicon and card from the live landing page, and the deck counts from the index READMEs; writes [`data/`](data/), [`assets/icons/`](assets/icons/) and [`assets/cards/`](assets/cards/) |
| Build | `python3 tools/build.py` | Writes the pages from `data/`, [`tools/content.py`](tools/content.py) (the hubs, showcases and quotes) and [`src/how-this-is-built.html`](src/how-this-is-built.html) |
| Brand | `python3 tools/brand.py && node tools/render_brand.js` | The favicon, the card and the touch icon |
| Profile | `python3 tools/profile_readme.py <path>` | The GitHub profile README, from the same data |

Checks (run before publishing):

| Check | Command |
|---|---|
| Every quote still appears, word for word, on its source page | `python3 tools/check_quotes.py` |
| Every link returns 200 | `python3 tools/check_links.py` |
| Each page at 1280 and 390 px, light and dark: no page errors, no horizontal overflow, axe clean, no external requests | `node tools/check_pages.js` (with `python3 -m http.server 8740` running) |

The thumbnails in [`assets/shots/`](assets/shots/) are screenshots of each page's first screen
([`tools/thumbs.js`](tools/thumbs.js)), resized to 640×360 WebP.

The work is built with Claude Code as an agentic engineering workflow; commits made this way carry a
`Co-Authored-By` line. See "How this is built" on the home page.
