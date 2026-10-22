"""Build the static site from data/ and tools/content.py.

    python3 tools/gather.py      # refresh data/ and the site icons and cards from their live sources
    python3 tools/build.py       # write index.html, sites/, library/, checks/, cv/index.html, 404.html, sitemap.xml,
                                 # robots.txt

The CSS is inlined into every page (one small stylesheet, so no extra request). The look is a component datasheet
(the "Datasheet" design, 2026-10; the previous design is the git tag design-classic): a mono header band, ruled
sections, square cards, IBM Plex Sans Condensed and IBM Plex Mono, self-hosted in assets/fonts/ (OFL). The scripts
are assets/hero.js (the home page's animation) and assets/twin.js (the Digital Twin side panel on the home, /sites/
and /cv/ pages). No external requests: local fonts and images; the panel loads /twin/, which is same-origin through
the rewrite.
"""
import datetime
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from optalysys import SECTIONS as O_SECTIONS, SOURCES as O_SOURCES  # noqa: E402
from content import DIGITAL_TWIN, HARDWARE, INDEXES, LIBRARY, QUOTES, SHOWCASES, GH  # noqa: E402
from cv import CV, DOMAIN_LABEL, PROFILE  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# the canonical address; GitHub Pages serves the same files from main, and its pages point here
BASE = "https://brendanlynskey.com"
PDF = "/cv/Brendan_Lynskey_CV.pdf"
NAME = "Brendan Lynskey"
DATA = json.load(open(os.path.join(ROOT, "data", "sites.json")))
COUNTS = json.load(open(os.path.join(ROOT, "data", "counts.json")))
BUILT = os.environ.get("BUILD_DATE") or datetime.date.today().isoformat()
# the owner's paragraph; its own comments (the draft note) stay out of the published page
HOW_BUILT = re.sub(r"<!--.*?-->\s*", "", open(os.path.join(ROOT, "src", "how-this-is-built.html")).read(),
                   flags=re.S).strip()

e = html.escape

# the datasheet's header band: a part number (the year the career starts), the revision (the build month) and where
PART = "BL-1994"
REV = BUILT[:7].replace("-", ".")
DATE_CODE = BUILT[2:4] + BUILT[5:7]                  # yymm, as printed on a package
WHERE = (lambda p: f"{p[0]}, {p[-1]}")([x.strip() for x in CV["location"].split(",")]).upper()   # "LEEDS, UK"
# the numbered pages of the datasheet, for the footer's "PAGE n OF m"
PAGES = ["/", "/sites/", "/library/", "/checks/", "/cv/"]
NAV = [("Portfolio", "/sites/"), ("Sites", "/sites/#sites"), ("Library", "/library/"), ("Checks", "/checks/"),
       ("CV", "/cv/"), ("GitHub", GH)]


def q(qid):
    """A quote from content.QUOTES, escaped, and its source link."""
    shown, _, text = QUOTES[qid]
    text = re.sub(r"<sup>&minus;12</sup>", "⁻¹²", text)
    return e(html.unescape(text)), shown


CSS = r"""
@font-face{font-family:"IBM Plex Sans Condensed";font-style:normal;font-weight:400;font-display:swap;src:url(/assets/fonts/ibm-plex-sans-condensed-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"IBM Plex Sans Condensed";font-style:normal;font-weight:600;font-display:swap;src:url(/assets/fonts/ibm-plex-sans-condensed-latin-600-normal.woff2) format("woff2")}
@font-face{font-family:"IBM Plex Sans Condensed";font-style:normal;font-weight:700;font-display:swap;src:url(/assets/fonts/ibm-plex-sans-condensed-latin-700-normal.woff2) format("woff2")}
@font-face{font-family:"IBM Plex Mono";font-style:normal;font-weight:400;font-display:swap;src:url(/assets/fonts/ibm-plex-mono-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"IBM Plex Mono";font-style:normal;font-weight:600;font-display:swap;src:url(/assets/fonts/ibm-plex-mono-latin-600-normal.woff2) format("woff2")}
:root{color-scheme:light dark;
 --bg:#f6f5f0;--surface:#ecebe4;--raised:#fbfaf7;--border:#c8c6bb;--rule:#111111;--text:#111111;--muted:#333333;--faint:#5c5a52;
 --accent:#f2a33a;--accent-fg:#111111;--accent-text:#9a3d06;--accent-line:#b3410a;--accent-soft:#fbe7c6;
 --chip:#1b1b1b;--chip-fg:#f6f5f0;--chip-muted:#c9c9c2;--lead:#111111;
 --hw:#0369a1;--hw2:#c2410c;--ok:#166534;
 --t-foundations:#0e7490;--t-hardware:#0369a1;--t-inference:#4f46e5;--t-agents:#b91c1c;
 --sans:"IBM Plex Sans Condensed","Arial Narrow","Roboto Condensed",ui-sans-serif,system-ui,sans-serif;
 --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
@media (prefers-color-scheme:dark){:root{
 --bg:#121211;--surface:#1c1c1a;--raised:#171716;--border:#3a3935;--rule:#eeece4;--text:#eeece4;--muted:#c9c7bd;--faint:#a3a199;
 --accent:#f2a33a;--accent-fg:#111111;--accent-text:#f2a33a;--accent-line:#f2a33a;--accent-soft:#3a2a12;
 --chip:#050505;--chip-fg:#eeece4;--chip-muted:#a3a199;--lead:#eeece4;
 --hw:#38bdf8;--hw2:#fb923c;--ok:#4ade80;
 --t-foundations:#22d3ee;--t-hardware:#38bdf8;--t-inference:#a5b4fc;--t-agents:#f87171}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased;scroll-padding-top:1rem}
body{margin:0;background:var(--bg);color:var(--text);font:17px/1.55 var(--sans)}
a{color:inherit;text-underline-offset:3px}
a:hover{color:var(--accent-text)}
img{max-width:100%;height:auto;display:block}
.wrap{max-width:77.5rem;margin:0 auto;padding:0 2rem}
@media (max-width:600px){.wrap{padding:0 1rem}}
.skip{position:absolute;left:-999px;top:0;background:var(--text);color:var(--bg);padding:.5rem 1rem;z-index:60}
.skip:focus{left:1rem;top:.5rem}
:focus-visible{outline:2px solid var(--accent-line);outline-offset:2px}
header.site .wrap{display:flex;flex-direction:column}
.band{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:.5rem 1rem;border-bottom:3px solid var(--rule);padding:1.1rem 0 .7rem;font:400 .85rem/1.3 var(--mono);letter-spacing:.06em;text-transform:uppercase}
.brand{display:inline-flex;align-items:center;min-height:44px;font-weight:600;text-decoration:none;white-space:nowrap}
.band .rev{color:var(--muted)}
.badge{display:inline-block;background:var(--accent);color:var(--accent-fg);padding:.25rem .65rem;font-weight:600;letter-spacing:.08em}
@media (max-width:600px){.band{font-size:.74rem;padding-top:.6rem}.band .rev{order:3;flex-basis:100%;margin-top:-.4rem}}
nav.top{display:flex;flex-wrap:wrap;gap:0 1.4rem;border-bottom:1px solid var(--rule);font:400 .82rem/1 var(--mono);letter-spacing:.08em;text-transform:uppercase}
nav.top a{display:inline-flex;align-items:center;min-height:44px;text-decoration:none;color:var(--muted)}
nav.top a:hover{color:var(--accent-text)}
nav.top a[aria-current]{color:var(--text);font-weight:600;box-shadow:inset 0 -3px 0 var(--accent)}
@media (max-width:600px){nav.top{gap:0 .95rem;font-size:.74rem}}
.eyebrow{font:600 .8rem/1.4 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--text);margin:0}
h1,h2,h3,h4{line-height:1.15;margin:0}
h1{font-size:clamp(2.6rem,7vw,4.6rem);font-weight:700;line-height:.92;letter-spacing:-.02em;text-transform:uppercase;margin-top:.6rem}
h2{font-size:clamp(1.55rem,3vw,2rem);font-weight:700;letter-spacing:-.01em}
h3{font-size:1.2rem;font-weight:600}
p{margin:0}
.lede{font-size:clamp(1.25rem,2.4vw,1.6rem);line-height:1.3;color:var(--text);max-width:42rem;margin-top:1.1rem}
.sub{color:var(--muted);max-width:42rem;margin-top:.9rem;font-size:1.06rem}
.hero{padding:3rem 0 1rem}
.hero-grid{display:grid;gap:1.75rem 2.5rem;grid-template-columns:minmax(0,1fr)}
.rest{display:flex;flex-direction:column}
@media (min-width:900px){.hero-grid{grid-template-columns:minmax(0,1fr) minmax(0,30rem);grid-template-areas:"intro fig" "rest fig";row-gap:0}
 .intro{grid-area:intro}.hero-fig{grid-area:fig;align-self:center}.rest{grid-area:rest}}
@media (max-width:899px){.rest .btns{order:-1;margin-top:0}.rest .sub{margin-top:1.25rem}}
.btns{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:1.6rem}
.btn{display:inline-flex;align-items:center;min-height:48px;padding:.5rem 1.3rem;font-size:1.06rem;font-weight:600;text-decoration:none;border:2px solid var(--rule);background:transparent;color:var(--text)}
.btn:hover{color:var(--text);box-shadow:4px 4px 0 var(--accent)}
.btn.primary{background:var(--text);border-color:var(--text);color:var(--bg)}
.btn.primary:hover{color:var(--bg)}
figure{margin:0}
.hero-fig{border:1px solid var(--rule);padding:.75rem;background:var(--raised);position:relative}
.hero-fig canvas{width:100%;aspect-ratio:560/300;display:block}
.hero-fig figcaption{font-size:.9rem;color:var(--faint);margin-top:.4rem;padding-right:5rem}
.hero-fig button{position:absolute;right:.75rem;bottom:.6rem;font:600 .78rem var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--text);background:var(--bg);border:1px solid var(--rule);padding:.3rem .7rem;min-height:44px;min-width:4.5rem;cursor:pointer}
.hero-fig button:hover{box-shadow:3px 3px 0 var(--accent)}
section.block{padding:3.25rem 0 0}
.block-head{margin-bottom:1.4rem;border-top:2px solid var(--rule);padding-top:.9rem}
.block-head h2{margin-top:.4rem}
.block-head>p{color:var(--muted);max-width:46rem;margin-top:.6rem}
main>.wrap>section.block>h2:first-child{border-top:2px solid var(--rule);padding-top:.9rem}
.grid{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,19rem),1fr))}
.card{position:relative;display:flex;flex-direction:column;border:1px solid var(--rule);background:var(--raised);overflow:hidden;transition:box-shadow .15s,transform .15s}
.card:hover{box-shadow:5px 5px 0 var(--accent);transform:translate(-2px,-2px)}
.card .thumb{aspect-ratio:1200/630;width:100%;object-fit:cover;background:var(--surface);border-bottom:1px solid var(--rule)}
.card .thumb.wide{aspect-ratio:16/9;object-position:top}
.hgrid .card .thumb.wide{aspect-ratio:2/1}
.card .body{padding:.9rem 1rem 1rem;display:flex;flex-direction:column;gap:.5rem;flex:1}
.card h3 a{text-decoration:none}
.card h3 a::after{content:"";position:absolute;inset:0;z-index:1}
.card .title{display:flex;align-items:center;gap:.55rem}
.card .title img{width:22px;height:22px;flex:none}
.card .place{font:400 .74rem/1.3 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--faint)}
.card .blurb{color:var(--muted);font-size:1rem}
.card .fact{font-size:.95rem;color:var(--text)}
.card .checked{font-size:.92rem;line-height:1.45;color:var(--muted);border-left:3px solid var(--accent);padding-left:.6rem}
.card .checked b{font:600 .7rem var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--faint);display:block}
.card .more{margin-top:auto;padding-top:.4rem;display:flex;flex-wrap:wrap;gap:.25rem .9rem;font-size:.95rem;position:relative;z-index:2}
.card .more a{color:var(--accent-text);text-decoration:underline;text-decoration-color:color-mix(in srgb,var(--accent-text) 40%,transparent)}
.card .more a:hover{text-decoration-color:currentColor}
.track{margin-top:2.25rem}
@media (min-width:860px){.grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}}
.card.mini .body{padding:1rem 1.1rem 1.1rem}
.card h2.h3{font-size:1.2rem;font-weight:600}
.card h2 a{text-decoration:none}
.card h2 a::after{content:"";position:absolute;inset:0;z-index:1}
.pill{display:inline-block;margin-left:.4rem;padding:.05rem .45rem;border:1px solid var(--rule);background:var(--accent);color:var(--accent-fg);letter-spacing:.06em}
.card .more a.btn{color:var(--bg);text-decoration:none;min-height:44px;padding:.45rem 1rem;margin-top:.15rem}
@media (min-width:760px){.grid.two{grid-template-columns:repeat(2,minmax(0,1fr))}}
.hgrid{display:grid;gap:1rem;grid-template-columns:minmax(0,1fr)}
@media (min-width:980px){.hgrid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:560px){.card.h{display:grid;grid-template-columns:minmax(0,38%) minmax(0,1fr)}
 .card.h .thumb{height:100%;aspect-ratio:auto;min-height:11rem;border-bottom:0;border-right:1px solid var(--rule)}}
.textlink{display:inline-flex;align-items:center;min-height:44px;color:var(--accent-text);font-weight:600}
.track-head{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem .65rem;margin-bottom:.9rem;padding-bottom:.5rem;border-bottom:1px solid var(--border)}
.track-head svg{width:22px;height:22px;flex:none}
.track-head h3{font-size:1.35rem;font-weight:700;text-transform:uppercase;letter-spacing:.01em}
.track-head p{color:var(--muted);font-size:1rem}
.checks4{display:grid;gap:0;grid-template-columns:repeat(auto-fill,minmax(min(100%,15rem),1fr));border-top:2px solid var(--rule);border-left:1px solid var(--rule)}
.stat{border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:1rem;background:var(--raised);display:flex;flex-direction:column;gap:.35rem}
.stat .n{font:600 1.65rem var(--mono);letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.stat .k{font:600 .72rem var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.stat p{font-size:.97rem;color:var(--muted)}
.stat a{font-size:.95rem;color:var(--accent-text);margin-top:auto;display:inline-flex;align-items:center;min-height:32px}
.list{border-top:2px solid var(--rule)}
.row{display:grid;grid-template-columns:minmax(0,12rem) minmax(0,1fr) auto;gap:.4rem 1.25rem;padding:.9rem 0;border-bottom:1px solid var(--border);align-items:baseline}
.row h3 a{text-decoration:none}
.row h3 a:hover{text-decoration:underline}
.row p{color:var(--muted);font-size:1rem}
.row .count{font:400 .88rem var(--mono);color:var(--text);white-space:nowrap;text-align:right}
@media (max-width:700px){.row{grid-template-columns:minmax(0,1fr) auto}.row p{grid-column:1/-1;grid-row:2}}
.note{font-size:.9rem;color:var(--faint);margin-top:.75rem}
.built{border:1px solid var(--rule);border-left:4px solid var(--accent);padding:1.25rem;background:var(--raised);max-width:50rem}
.built p+p{margin-top:.75rem}
.built p{color:var(--muted)}
code{font:.86em var(--mono);background:var(--surface);border:1px solid var(--border);padding:.05rem .3rem;overflow-wrap:anywhere}
footer.site{margin-top:4.5rem}
footer.site .fbar{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:.5rem 1.5rem;border-top:3px solid var(--rule);padding:.9rem 0 2.5rem;font:400 .8rem/1.6 var(--mono);color:var(--muted)}
footer.site .fbar>span:first-child{text-transform:uppercase;letter-spacing:.06em}
footer.site a{color:var(--text)}
.prose{max-width:48rem}
.prose p{color:var(--muted);margin-top:.9rem}
.big4{display:grid;gap:1.25rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,30rem),1fr));margin-top:1.25rem}
.check{border:1px solid var(--rule);background:var(--raised);padding:1.1rem 1.15rem;display:flex;flex-direction:column;gap:.6rem}
.check svg{width:100%;height:auto}
.check svg.dv{display:none;max-width:19rem;margin:0 auto}
@media (max-width:600px){.check svg.dh{display:none}.check svg.dv{display:block}}
.check blockquote{margin:0;border-left:3px solid var(--accent);padding-left:.75rem;color:var(--text);font-size:1rem}
.check .src{font-size:.9rem;color:var(--faint)}
.check .src a{color:var(--accent-text)}
.check .k{font:600 .72rem var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.tbl{width:100%;border-collapse:collapse;font-size:1rem}
.tbl th,.tbl td{text-align:left;vertical-align:top;padding:.7rem .6rem;border-bottom:1px solid var(--border)}
.tbl thead tr{border-top:2px solid var(--rule)}
.tbl thead th{border-bottom:2px solid var(--rule)}
.tbl tbody tr:last-child td{border-bottom:2px solid var(--rule)}
.tbl th{font:600 .74rem var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--text)}
.tbl td:first-child{white-space:nowrap}
.tbl td a{color:var(--accent-text)}
.tbl .site{display:flex;align-items:center;gap:.5rem;font-weight:600}
.tbl .site img{width:18px;height:18px}
@media (max-width:700px){.tbl thead{display:none}.tbl tr{display:block;padding:.7rem 0;border-bottom:1px solid var(--border)}
 .tbl td{display:block;border:0;padding:.15rem 0}.tbl td:first-child{white-space:normal}.tbl tbody tr:last-child td{border-bottom:0}}
.qt{border-collapse:collapse;font-size:.9rem;margin:.4rem 0;width:100%}
.qt th,.qt td{border:1px solid var(--border);padding:.3rem .45rem;text-align:left;vertical-align:top}
.qt th{font:600 .68rem var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--text);background:var(--surface);border-bottom:2px solid var(--rule)}
.miss{border:1px solid var(--rule);padding:1rem 1.15rem;background:var(--raised)}
.miss ul{margin:.5rem 0 0;padding-left:1.1rem;color:var(--muted)}
.miss li{margin:.45rem 0}
.miss li a{color:var(--accent-text)}
svg text{font-family:var(--mono)}
.o-link{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;margin-left:.6rem;vertical-align:middle;border:1px solid var(--border);border-radius:50%;font:600 .78rem var(--sans);color:var(--faint)!important;text-decoration:none;transition:color .2s,border-color .2s}
.o-link:hover,.o-link:focus-visible{color:var(--hw2)!important;border-color:var(--hw2)}
.hero.page{padding-bottom:0}
.hero.page h1{font-size:clamp(2.4rem,6.5vw,4.4rem)}
.hero.page .sub{max-width:46rem}
.jump{display:flex;flex-wrap:wrap;gap:.25rem 1.3rem;margin-top:1.1rem;font:400 .85rem var(--mono);letter-spacing:.06em;text-transform:uppercase}
.jump a{display:inline-flex;align-items:center;min-height:44px;color:var(--accent-text)}
@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}.card:hover{transform:none}}
"""

# the home page's datasheet parts: the pin diagram, the tables, the timing diagram and the application tiles
HOME_CSS = r"""
.ds-k{font:600 .85rem/1.4 var(--mono);letter-spacing:.1em;text-transform:uppercase;margin:0}
.ds-sec{padding:2.5rem 0;border-bottom:1px solid var(--rule)}
.ds-sec>.ds-k,.ds-sec h2.ds-k{margin-bottom:1rem}
.ds-gd{display:flex;flex-wrap:wrap;gap:3rem;padding:3.5rem 0 2.5rem}
.gd-text{flex:999 1 32rem;min-width:0}
.gd-text .ds-k{margin-bottom:.6rem}
.ds-name{font-size:clamp(3.5rem,9vw,7rem);line-height:.9;font-weight:700;letter-spacing:-.02em;text-transform:uppercase;margin:0}
.gd-text .lede{font-size:clamp(1.3rem,2.6vw,1.65rem);margin-top:1.5rem;max-width:40rem}
.gd-text .sub{font-size:1.12rem;max-width:40rem}
.gd-text .btns{margin-top:1.75rem}
.pins{flex:1 1 22rem;min-width:0}
.pins .ds-k{margin-bottom:.9rem}
.pkg{display:grid;grid-template-columns:minmax(0,1fr) 9.5rem minmax(0,1fr);font:400 .95rem/1 var(--mono)}
.pkg ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;justify-content:space-around}
.pkg li{display:flex}
.pin{display:flex;align-items:center;gap:.5rem;min-height:44px;width:100%;text-decoration:none;letter-spacing:.04em}
.pkg .l .pin{justify-content:flex-end;text-align:right}
.pin .lead{flex:none;width:2.1rem;height:3px;background:var(--lead);transition:width .15s,background .15s}
.pin .no{flex:none;width:1.2rem;color:var(--faint);font-size:.8rem}
.pkg .l .pin .no{text-align:left;padding-left:.15rem}
.pkg .r .pin .no{text-align:right;padding-right:.15rem}
a.pin:hover,a.pin:focus-visible{color:var(--accent-text)}
a.pin:hover .lead,a.pin:focus-visible .lead{background:var(--accent);width:2.6rem}
.pin.gnd{color:var(--faint)}
.pin.gnd .lead{background:var(--faint);opacity:.7}
.chip{position:relative;border:3px solid var(--rule);background:var(--chip);color:var(--chip-fg);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.5rem;padding:1.25rem .5rem;min-height:15rem;text-align:center}
.chip::before{content:"";position:absolute;top:.6rem;left:.6rem;width:.75rem;height:.75rem;border-radius:50%;border:2px solid var(--chip-fg)}
.chip b{font:600 1.55rem/1 var(--mono);letter-spacing:.04em}
.chip span{font-size:.75rem;color:var(--chip-muted);letter-spacing:.06em}
@media (max-width:520px){.pkg{grid-template-columns:minmax(0,1fr) 5.6rem minmax(0,1fr);font-size:.82rem}
 .pin{gap:.3rem}.pin .lead{width:1rem}a.pin:hover .lead,a.pin:focus-visible .lead{width:1.2rem}.pin .no{width:.9rem;font-size:.7rem}
 .chip{min-height:13rem;padding:1rem .2rem}.chip b{font-size:.95rem}.chip span{font-size:.56rem;white-space:nowrap;letter-spacing:0}}
.ds-two{display:flex;flex-wrap:wrap;gap:2rem 3rem}
.ds-two>.feat{flex:1 1 20rem;min-width:0}
.ds-two>.elec{flex:2 1 34rem;min-width:0}
.feat ul{margin:0;padding-left:1.25rem;font-size:1.15rem;line-height:1.6}
.feat li::marker{color:var(--accent-text)}
.box{overflow-x:auto;max-width:100%}
.box:focus-visible{outline-offset:4px}
.ec{width:100%;min-width:34rem;border-collapse:collapse;font-size:1.05rem;font-variant-numeric:tabular-nums}
.ec thead tr{border-top:2px solid var(--rule);border-bottom:2px solid var(--rule)}
.ec th{font:600 .78rem var(--mono);letter-spacing:.06em;text-align:left;padding:.5rem .4rem}
.ec td{padding:.55rem .4rem;border-bottom:1px solid var(--border)}
.ec tbody tr:last-child td{border-bottom:2px solid var(--rule)}
.ec td.sym{font-family:var(--mono);font-size:.95rem}
.ec td.n{font-family:var(--mono)}
.ec .dash{color:var(--faint)}
@media (max-width:600px){.ec{min-width:0;font-size:.92rem}.ec th,.ec td{padding-left:.25rem;padding-right:.25rem}.ec th{font-size:.66rem;letter-spacing:0}.ec td.sym{font-size:.82rem}}
.ds-note{font-size:.95rem;color:var(--muted);margin-top:.7rem}
.ds-note a{color:var(--accent-text)}
.td-svg{display:block;width:100%;min-width:47.5rem}
.td-svg .lbl{font:400 14px var(--mono);fill:var(--text)}
.td-svg .yr{font:400 13px var(--mono);fill:var(--muted)}
.td-svg .grid{stroke:var(--faint);stroke-dasharray:3 5;stroke-width:1}
.td-svg .tr{fill:none;stroke:var(--text);stroke-width:2.5;stroke-linejoin:round}
.td-svg .tr.ai{stroke:var(--accent);stroke-width:3.5}
.td-svg .ann{font:400 12px var(--mono);fill:var(--muted)}
.fig2{display:flex;flex-wrap:wrap;gap:2rem 3rem;align-items:flex-start}
.fig2 .hero-fig{flex:1 1 30rem;min-width:0;max-width:40rem}
.fig2 .fd{flex:1 1 20rem;min-width:0}
.fig2 .fd p{color:var(--muted);font-size:1.08rem}
.fig2 .fd p+p{margin-top:.8rem}
.fig2 .fd b{color:var(--text)}
.apps{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,13rem),1fr))}
@media (min-width:1100px){.apps{grid-template-columns:repeat(5,minmax(0,1fr))}}
.app{display:flex;flex-direction:column;gap:.5rem;border:2px solid var(--rule);padding:1.2rem;text-decoration:none;color:var(--text);transition:box-shadow .15s,transform .15s}
.app:hover,.app:focus-visible{color:var(--text);box-shadow:5px 5px 0 var(--rule);transform:translate(-2px,-2px)}
.app .k{font:400 .8rem/1.3 var(--mono);letter-spacing:.04em;text-transform:uppercase}
.app .t{font-size:1.6rem;font-weight:700;line-height:1.05}
.app .b{font-size:1rem;color:var(--muted)}
.app .i{display:flex;flex-wrap:wrap;gap:.35rem;margin-top:auto;padding-top:.4rem}
.app .i img{width:20px;height:20px}
.app.hot{background:var(--accent);border-color:var(--accent);color:var(--accent-fg)}
.app.hot .b{color:var(--accent-fg)}
.app.hot:hover,.app.hot:focus-visible{color:var(--accent-fg);border-color:var(--rule)}
.ord{width:100%;border-collapse:collapse;font-size:1.05rem}
.ord thead tr{border-top:2px solid var(--rule);border-bottom:2px solid var(--rule)}
.ord th{font:600 .78rem var(--mono);letter-spacing:.06em;text-align:left;padding:.5rem .4rem;white-space:nowrap}
.ord td{padding:.6rem .4rem;border-bottom:1px solid var(--border);vertical-align:baseline}
.ord tbody tr:last-child td{border-bottom:2px solid var(--rule)}
.ord td:first-child{font:600 .9rem var(--mono);white-space:nowrap;letter-spacing:.04em}
.ord td.part{font-family:var(--mono);font-size:.9rem;white-space:nowrap}
.ord td a{display:inline-flex;align-items:center;min-height:44px;color:var(--accent-text);font-weight:600}
.ord td.d{color:var(--muted)}
@media (max-width:700px){.ord thead{display:none}.ord tr{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:0 1rem;padding:.6rem 0;border-bottom:1px solid var(--border)}
 .ord td{border:0;padding:.1rem 0}.ord td.d{grid-column:1/-1;grid-row:2}.ord tbody tr:last-child td{border-bottom:0}.ord tbody tr:last-child{border-bottom:2px solid var(--rule)}}
@media (prefers-reduced-motion:reduce){.app:hover,.app:focus-visible{transform:none}}
"""

# the home page used to hold the whole portfolio; old links to its sections now land on /sites/
OLD_ANCHORS = """<script>if(/^#(hardware|sites|track-[a-z]+|showcases|checks|decks|built)$/.test(location.hash))location.replace("/sites/"+location.hash)</script>
"""

TRACK_SHAPE = {
    # the companion sites' favicon shapes, one per track
    "foundations": '<circle cx="16" cy="16" r="15" fill="currentColor"/>',
    "hardware": '<rect x="3.5" y="3.5" width="25" height="25" rx="2.5" fill="currentColor"/><path d="M9 0h3v4h-3zM20 0h3v4h-3zM9 28h3v4h-3zM20 28h3v4h-3zM0 9h4v3h-4zM0 20h4v3h-4zM28 9h4v3h-4zM28 20h4v3h-4z" fill="currentColor"/>',
    "inference": '<path d="M16 0.5 29.5 8.25v15.5L16 31.5 2.5 23.75V8.25z" fill="currentColor"/>',
    "agents": '<rect x="0.5" y="1" width="31" height="24" rx="6" fill="currentColor"/><path d="M6 23v8.5l8.5-8.5z" fill="currentColor"/>',
}


# ---------------------------------------------------------------- the Digital Twin side panel
# A floating "Ask my twin" launcher (bottom right) on the home, /sites/ and /cv/ pages. assets/twin.js turns it,
# the Digital Twin card and the hero button into openers for a side panel holding the twin in an iframe of
# /twin/?embed=1 (same-origin through vercel.json's rewrite), loaded on first open and kept while on the page.
# Without the script, or on GitHub Pages (which has no /twin/), the launcher is a plain link to the twin.
TWIN_CSS = r"""
.tw-launch{position:fixed;right:1.25rem;bottom:1.25rem;z-index:40;display:inline-flex;align-items:center;gap:.6rem;min-height:48px;padding:.4rem 1.1rem .4rem .4rem;border:2px solid var(--rule);background:color-mix(in srgb,var(--raised) 90%,transparent);backdrop-filter:saturate(1.4) blur(10px);-webkit-backdrop-filter:saturate(1.4) blur(10px);color:var(--text);font:600 .9rem/1 var(--sans);text-decoration:none;box-shadow:4px 4px 0 var(--accent);transition:border-color .15s,box-shadow .2s,opacity .2s,transform .2s,visibility 0s}
.tw-launch:hover{color:var(--text);box-shadow:6px 6px 0 var(--accent)}
.tw-launch .tw-mark{position:relative;flex:none;width:36px;height:36px}
.tw-launch .tw-mark img{width:36px;height:36px}
.tw-launch .tw-mark::after{content:"";position:absolute;right:-2px;bottom:-2px;width:10px;height:10px;border-radius:50%;background:var(--ok);border:2px solid var(--raised)}
.tw-launch .tw-sub{display:block;font:500 .62rem/1.2 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--accent-text);margin-bottom:.2rem}
html.tw-open .tw-launch{opacity:0;visibility:hidden;transform:translateY(6px);transition:opacity .15s,transform .15s,visibility 0s linear .15s}
body.tw-has footer.site{padding-bottom:6.5rem}
.tw-scrim{display:none}
.tw-panel{position:fixed;z-index:50;top:4.5rem;right:.75rem;bottom:.75rem;width:min(26.5rem,calc(100vw - 1.5rem));display:flex;flex-direction:column;background:var(--bg);border:2px solid var(--rule);overflow:hidden;box-shadow:6px 6px 0 var(--accent);visibility:hidden;transform:translateX(calc(100% + 1.5rem));transition:transform .28s cubic-bezier(.2,.8,.2,1),visibility 0s linear .28s}
html.tw-open .tw-panel{visibility:visible;transform:none;transition:transform .32s cubic-bezier(.2,.8,.2,1),visibility 0s}
.tw-panel:focus{outline:none}
.tw-head{flex:none;display:flex;align-items:center;gap:.5rem;min-height:2.75rem;padding:0 .4rem 0 1rem;border-bottom:2px solid var(--rule);background:var(--surface)}
.tw-head-k{flex:1;font:500 .66rem/1.2 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--faint)}
.tw-full{display:inline-flex;align-items:center;gap:.35rem;min-height:36px;padding:0 .55rem;border-radius:.4rem;color:var(--muted);font-size:.8rem;text-decoration:none}
.tw-full:hover{color:var(--text);background:var(--bg)}
.tw-close{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:.4rem;border:1px solid transparent;background:none;color:var(--muted);cursor:pointer}
.tw-close:hover{color:var(--text);background:var(--bg);border-color:var(--border)}
.tw-body{position:relative;flex:1;min-height:0}
.tw-body iframe{position:absolute;inset:0;width:100%;height:100%;border:0;background:var(--bg);opacity:0;transition:opacity .25s}
.tw-body.ready iframe{opacity:1}
.tw-wait{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.75rem;color:var(--faint);font-size:.85rem}
.tw-wait span{display:inline-flex;gap:5px}
.tw-wait i{width:7px;height:7px;border-radius:50%;animation:tw-blink 1.2s ease-in-out infinite}
.tw-wait i:nth-child(1){background:var(--t-foundations)}.tw-wait i:nth-child(2){background:var(--t-inference);animation-delay:.15s}.tw-wait i:nth-child(3){background:var(--t-agents);animation-delay:.3s}
@keyframes tw-blink{0%,80%,100%{opacity:.25}40%{opacity:1}}
.tw-body.ready .tw-wait{display:none}
@media (max-width:640px){
 .tw-launch{right:1rem;bottom:1rem}

 .tw-scrim{display:block;position:fixed;inset:0;z-index:49;background:rgba(10,10,10,.45);opacity:0;visibility:hidden;transition:opacity .25s,visibility 0s linear .25s}
 html.tw-open .tw-scrim{opacity:1;visibility:visible;transition:opacity .25s,visibility 0s}
 html.tw-lock,html.tw-lock body{overflow:hidden}
 .tw-panel{top:var(--tw-y,.75rem);left:0;right:0;bottom:auto;width:auto;height:var(--tw-h,calc(100dvh - .75rem));border-radius:1rem 1rem 0 0;border-bottom:0;transform:translateY(100%)}
 .tw-head{padding-left:1rem}
 .tw-head::before{content:"";position:absolute;left:50%;top:5px;width:36px;height:4px;margin-left:-18px;border-radius:2px;background:var(--border)}
}
@media (prefers-reduced-motion:reduce){.tw-launch,.tw-panel,.tw-scrim,.tw-body iframe{transition:none!important}.tw-wait i{animation:none;opacity:.7}}
@media print{.tw-launch,.tw-panel,.tw-scrim{display:none!important}}
"""

TWIN_ICON_OUT = ('<svg viewBox="0 0 16 16" width="13" height="13" aria-hidden="true"><path d="M9.5 2.5h4v4M13.5 2.5 8 8M6.5 3.5h-3v9h9v-3" '
                 'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
TWIN_ICON_X = ('<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8" fill="none" '
               'stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>')


def twin_panel():
    """The launcher and the (empty, hidden) panel, at the end of <body>."""
    url = e(DIGITAL_TWIN["url"])
    return f"""<a class="tw-launch" id="tw-launch" href="{url}" data-twin><span class="tw-mark"><img src="/favicon.svg" alt="" width="36" height="36"></span><span><span class="tw-sub">Digital Twin</span>Ask my twin</span></a>
<div class="tw-scrim" id="tw-scrim" hidden></div>
<div class="tw-panel" id="tw-panel" role="dialog" aria-labelledby="tw-title" tabindex="-1" hidden>
<div class="tw-head"><h2 id="tw-title" class="sr">Brendan Lynskey's Digital Twin</h2><span class="tw-head-k" aria-hidden="true">Chat</span><a class="tw-full" href="{url}" target="_blank" rel="noopener">Open full page<span class="sr"> (opens in a new tab)</span>{TWIN_ICON_OUT}</a><button type="button" class="tw-close" id="tw-close" aria-label="Close the Digital Twin">{TWIN_ICON_X}</button></div>
<div class="tw-body" id="tw-body"><p class="tw-wait" role="status"><span aria-hidden="true"><i></i><i></i><i></i></span>Opening the Digital Twin…</p></div>
</div>
<script src="/assets/twin.js" defer></script>
"""


def nav_html(path):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{e(u)}"{cur if u == path else ""}>{e(t)}</a>' for t, u in NAV)
    return f'<nav class="top" aria-label="Main">{links}</nav>\n'


def head(title, description, path, extra="", noindex=False, twin=False, nav=True):
    url = BASE + path
    canonical = (f'<link rel="canonical" href="{url}">' if path != "/404.html"
                 else '<meta name="robots" content="noindex">')
    if noindex and path != "/404.html":
        canonical += '\n<meta name="robots" content="noindex">'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
{canonical}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#f6f5f0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121211" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url if path != "/404.html" else BASE + "/"}">
<meta property="og:image" content="{BASE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME}: hardware, software and agentic AI. Sixteen interactive sites, each checked against a reference.">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{BASE}/og.png">
<link rel="preload" href="/assets/fonts/ibm-plex-sans-condensed-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/ibm-plex-mono-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS.strip()}</style>
{f"<style>{TWIN_CSS.strip()}</style>" + chr(10) if twin else ""}{extra}</head>
<body{' class="tw-has"' if twin else ""}>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
<div class="band">
<a class="brand" href="/"><span class="sr">{NAME}, home page: </span>{PART} · Staff engineer</a>
<span class="rev">Datasheet · Rev {REV} · {WHERE}</span>
<span class="badge">Active</span>
</div>
{nav_html(path) if nav else ""}</div></header>
"""


def foot(extra="", twin=False, path=None):
    page = (f" · Page {PAGES.index(path) + 1} of {len(PAGES)}" if path in PAGES
            else " · Page not found" if path == "/404.html" else "")
    return f"""<footer class="site"><div class="wrap"><div class="fbar">
<span>{PART} datasheet{page} · {NAME} · <a href="{GH}">GitHub</a>{extra}</span>
<span>Information furnished is believed to be accurate: see <a href="/checks/">How I check the numbers</a>. A static page, built {BUILT} from its <a href="{GH}/BrendanJamesLynskey.github.io">source</a>.</span>
</div></div></footer>
{twin_panel() if twin else ""}</body>
</html>
"""


def sites_in(group):
    return [s for s in DATA["sites"] if s.get("group") == group]


def site_card(s, group_label):
    key = s["key"]
    return f"""<article class="card">
<img class="thumb" src="/assets/cards/{key}.webp" alt="" width="600" height="315" loading="lazy" decoding="async">
<div class="body">
<p class="place">{e(group_label)} › {e(s["label"])}</p>
<div class="title"><img src="/assets/icons/{key}.svg" alt="" width="22" height="22"><h3><a href="{e(s["landing"])}">{e(s["name"])}</a></h3></div>
<p class="blurb">{e(s["blurb"])}</p>
<p class="checked"><b>How this is checked</b>{e(s["claim"])}</p>
<p class="more"><a href="{e(s["evidence"])}">How it is tested<span class="sr"> ({e(s["name"])})</span></a></p>
</div>
</article>"""


def si_fact():
    c = COUNTS["Signal_Integrity"]
    return (f"{c['decks']} decks, {c['slides']} slides; {c['published_checks']} cross-checks against "
            f"published results, the largest difference {c['worst_pct']:.2f} %.")


def dsp_fact():
    c = COUNTS["DSP_and_Music"]
    return f"Twelve parts; the DSP & Music index lists {c['projects']} projects in {c['areas']} areas."


def hw_fact():
    return f"The Hardware index lists {COUNTS['Hardware']['series']} series."


def hw_card(h):
    fact = {"si": si_fact, "dsp": dsp_fact, "hw": hw_fact}[h["fact"]]() if h.get("fact") else h["fact_text"]
    links = "".join(f'<a href="{e(u)}">{e(t)}</a>' for t, u in h["links"])
    return f"""<article class="card">
<img class="thumb wide" src="/assets/shots/{h["key"]}.webp" alt="" width="640" height="360" loading="lazy" decoding="async">
<div class="body">
<h3><a href="{e(h["href"])}">{e(h["title"])}</a></h3>
<p class="blurb">{e(h["text"])}</p>
<p class="fact">{e(fact)}</p>
<p class="more">{links}</p>
</div>
</article>"""


def showcase_card(c):
    wide = "" if c["img"].startswith("cards/") else " wide"
    w, hgt = ("600", "315") if not wide else ("640", "360")
    links = "".join(f'<a href="{e(u)}">{e(t)}</a>' for t, u in c["links"])
    return f"""<article class="card">
<img class="thumb{wide}" src="/assets/{c["img"]}" alt="" width="{w}" height="{hgt}" loading="lazy" decoding="async">
<div class="body">
<h3><a href="{e(c["href"])}">{e(c["title"])}</a></h3>
<p class="blurb">{e(c["text"])}</p>
<p class="more">{links}</p>
</div>
</article>"""


def index_count(key):
    c = COUNTS[key]
    if key == "LLMs":
        return f"{c['series']} series · {c['decks']} decks"
    if key == "Signal_Integrity":
        return f"{c['decks']} decks · {c['slides']} slides"
    if key == "DSP_and_Music":
        return f"{c['projects']} projects · {c['areas']} areas"
    return f"{c['series']} series"


def index_row(x):
    return f"""<div class="row">
<h3><a href="{e(x["href"])}">{e(x["title"])}</a></h3>
<p>{e(x["text"])}</p>
<span class="count">{e(index_count(x["key"]))}</span>
</div>"""


# ---------------------------------------------------------------- the home page: a datasheet

# the CV source's date; its profile's "for the last two years ... agentic AI systems" is counted back from it
CV_DATE = re.search(r"Compiled (\d{4})-(\d{2})-(\d{2})", open(os.path.join(ROOT, "src", "cv_source.md")).read())
AI_FROM = int(CV_DATE.group(1)) - 2 + (int(CV_DATE.group(2)) - 1) / 12
# short trace names for the timing diagram (a layout choice); others are the company's name, upper-cased
TRACE_NAME = {"Imagination Technologies / MIPS": "IMG / MIPS", "Red Embedded": "RED EMB.",
              "Blaize (formerly Thinci)": "BLAIZE"}


def pins():
    """The pin configuration: the home page's navigation, drawn as an 8-pin package (pins 1-4 down the left,
    5-8 up the right). Pin 5 is GND, a decoration and not a link."""
    twin = DIGITAL_TWIN["url"] or DIGITAL_TWIN["interim_url"]
    left = [(1, "CV", "/cv/", ""), (2, "Twin", twin, " data-twin" if DIGITAL_TWIN["url"] else ""),
            (3, "Sites", "/sites/", ""), (4, "Library", "/library/", "")]
    right = [(8, "Checks", "/checks/", ""), (7, "GitHub", GH, ""), (6, "LinkedIn", CV["linkedin"], "")]
    lis = lambda side, items: "".join(
        f'<li><a class="pin" href="{e(u)}"{x}>'
        + (f'{e(t.upper())}<span class="lead" aria-hidden="true"></span><span class="no" aria-hidden="true">{n}</span>'
           if side == "l" else
           f'<span class="no" aria-hidden="true">{n}</span><span class="lead" aria-hidden="true"></span>{e(t.upper())}')
        + "</a></li>" for n, t, u, x in items)
    gnd = ('<li aria-hidden="true"><span class="pin gnd"><span class="no">5</span><span class="lead"></span>GND</span></li>')
    return f"""<nav class="pkg" aria-label="Pin configuration: the site's pages">
<ul class="l">{lis("l", left)}</ul>
<div class="chip" aria-hidden="true"><b>{PART}</b><span>HW · SW · AI</span><span>{e(WHERE.split(",")[0])} {DATE_CODE}</span></div>
<ul class="r">{lis("r", right)}{gnd}</ul>
</nav>"""


def features(n_sites):
    edu = next(x for x in CV["education"] if "Low Power" in x["degree"])
    items = ["RTL and FPGA design, SoC and ASIC work",
             "DSP, signal and power integrity, power delivery",
             "Agentic AI in Python: LangGraph, MCP, open-weights LLMs",
             f"{n_sites} interactive sites, each model checked against a reference",
             f"Low-power operation: {edu['degree']}"]
    return "".join(f"<li>{e(x)}</li>" for x in items)


def characteristics(n_sites):
    """(parameter, symbol, subscript, min, typ, max, unit), every number from data/ or the CV source."""
    llms, si, lib = COUNTS["LLMs"], COUNTS["Signal_Integrity"], COUNTS["library"]
    rows = [("Hardware experience", "t", "HW", 25, None, None, "years"),
            ("Interactive sites", "N", "SITE", None, n_sites, None, "sites"),
            ("Deck series in the library", "N", "LIB", None, lib["series"], None, "series"),
            ("LLM deck series", "N", "SER", None, llms["series"], None, "series"),
            ("Decks in those series", "N", "DECK", None, llms["decks"], None, "decks"),
            ("Signal-integrity decks", "N", "SI", None, si["decks"], None, "decks"),
            (f"SI results against {si['published_checks']} published values", "δ", "SI", None, None,
             f"{si['worst_pct']:.2f}", "%")]
    cell = lambda v: f'<td class="n">{v}</td>' if v is not None else '<td class="dash" aria-label="none">—</td>'
    body = "".join(f"<tr><td>{e(p)}</td><td class=\"sym\">{s}<sub>{sub}</sub></td>{cell(a)}{cell(t)}{cell(m)}<td>{u}</td></tr>"
                   for p, s, sub, a, t, m, u in rows)
    return f"""<div class="box" tabindex="0" role="region" aria-label="Electrical characteristics (scrolls sideways)">
<table class="ec">
<thead><tr><th scope="col">PARAMETER</th><th scope="col">SYMBOL</th><th scope="col">MIN</th><th scope="col">TYP</th><th scope="col">MAX</th><th scope="col">UNIT</th></tr></thead>
<tbody>{body}</tbody>
</table>
</div>"""


def timing_diagram():
    """Figure 1: the career as a timing diagram, one trace per employer (newest at the top) plus agentic AI; a
    trace is high while a role is held. Dates are the CV source's."""
    t0, t1 = 1994.0, now_year()
    X0, X1, PITCH = 180.0, 1196.0, 40
    x = lambda t: X0 + (max(t, t0) - t0) / (t1 - t0) * (X1 - X0)
    rows, said = [("AGENTIC AI", [(AI_FROM, None)], True)], []
    for r in CV["roles"]:                                   # the source lists the newest role first
        key = r["company"]
        for k, iv, ai in rows:
            if k == key:
                iv.append((r["t0"], r["t1"]))
                break
        else:
            rows.append((key, [(r["t0"], r["t1"])], False))
    paths, labels = [], []
    for i, (k, iv, ai) in enumerate(rows):
        lo = 44 + PITCH * i
        hi = lo - 20
        d = f"M{X0:.0f},{lo}"
        for a, b in sorted(iv):
            xa = x(a)
            d += f" H{max(X0, xa - 3):.1f} L{xa + 3:.1f},{hi}" if xa > X0 else f" M{X0:.0f},{hi}"
            if b is None:
                d += f" H{X1:.0f}"
            else:
                xb = x(b)
                d += f" H{xb - 3:.1f} L{xb + 3:.1f},{lo}"
        if not d.endswith(f"H{X1:.0f}"):
            d += f" H{X1:.0f}"
        paths.append(f'<path class="tr{" ai" if ai else ""}" d="{d}"/>')
        name = k if ai else TRACE_NAME.get(k, k.upper())
        labels.append(f'<text class="lbl" x="0" y="{lo - 4}">{e(name)}</text>')
    H = 44 + PITCH * (len(rows) - 1) + 52
    years = list(range(1994, int(t1) + 1, 6))
    grid = "".join(f'<line class="grid" x1="{x(y):.1f}" y1="10" x2="{x(y):.1f}" y2="{H - 34}"/>' for y in years)
    yrs = "".join(f'<text class="yr" x="{x(y):.1f}" y="{H - 10}" text-anchor="middle">{y}</text>' for y in years)
    # the accessible description: every role, in the source's words
    for r in CV["roles"]:
        said.append(f"{r['company']}, {r['start']} to {r['end']}")
    ai_year = int(AI_FROM)
    label = (f"Career timing diagram, 1994 to now, newest at the top. Agentic AI from {ai_year} to now; "
             + "; ".join(said) + ".")
    return f"""<div class="box" tabindex="0" role="region" aria-label="Figure 1 (scrolls sideways)">
<svg class="td-svg" viewBox="0 0 1210 {H}" role="img" aria-label="{e(label)}">
{grid}{"".join(labels)}{"".join(paths)}{yrs}
</svg>
</div>""", ai_year


def apps():
    """Typical applications: the home-ground deck series, then one tile per track."""
    tiles = [("/sites/#hardware", f"App 1 · {len(HARDWARE)} deck series", "Home ground",
              "Hardware, DSP and signal integrity", [], False)]
    for n, g in enumerate(DATA["groups"], 2):
        ss = sites_in(g["key"])
        tiles.append((f"/sites/#track-{g['key']}", f"App {n} · {len(ss)} sites", g["label"], g["blurb"], ss,
                      n == len(DATA["groups"]) + 1))
    out = []
    for href, k, t, b, ss, hot in tiles:
        icons = "".join(f'<img src="/assets/icons/{s["key"]}.svg" alt="" width="20" height="20">' for s in ss)
        out.append(f"""<a class="app{" hot" if hot else ""}" href="{href}">
<span class="k">{e(k)}</span>
<span class="t">{e(t)}</span>
<span class="b">{e(b)}</span>
{f'<span class="i">{icons}</span>' if icons else ""}
</a>""")
    return "\n".join(out)


def ordering():
    """Ordering information: the CV, the Digital Twin and how to get in touch (what the home page's CV and contact
    cards used to say)."""
    t = DIGITAL_TWIN
    twin = (f'<a href="{e(t["url"])}" data-twin>Ask my twin →</a>' if t["url"]
            else f'<a href="{e(t["interim_url"])}">Try the earlier version →</a>')
    rows = [("BL-CV", "Experience and education. " + CV["headline"], '<a href="/cv/">Read the CV →</a>'),
            ("BL-CV-PDF", "The same CV as an A4 PDF.", f'<a href="{PDF}">Download the PDF</a>'),
            ("BL-TWIN", t["text"], twin),
            ("BL-MSG", "The best way to reach me is a message on LinkedIn.",
             f'<a href="{e(CV["linkedin"])}">Message me on LinkedIn →</a>')]
    body = "".join(f'<tr><td class="part">{c}</td><td class="d">{e(d)}</td><td>{a}</td></tr>' for c, d, a in rows)
    return f"""<table class="ord">
<thead><tr><th scope="col">ORDERING CODE</th><th scope="col">DESCRIPTION</th><th scope="col">ORDER</th></tr></thead>
<tbody>{body}</tbody>
</table>"""


def home():
    twin_btn = (f'<a class="btn primary" href="{e(DIGITAL_TWIN["url"])}" data-twin>Ask my Digital Twin</a>\n'
                if DIGITAL_TWIN["url"] else "")
    n_sites = sum(len(sites_in(g["key"])) for g in DATA["groups"])
    assert n_sites == 16, n_sites
    td, ai_year = timing_diagram()
    desc = ("Brendan Lynskey: a staff-level engineer across hardware (RTL and FPGA, DSP, signal integrity), "
            "software and agentic AI. His CV, a chat agent about his career, and a portfolio of explainer sites and deck "
            "series built for his own learning.")
    return head(f"{NAME}: hardware, software and agentic AI", desc, "/",
                OLD_ANCHORS + f"<style>{HOME_CSS.strip()}</style>\n", twin=True, nav=False) + f"""<main id="main"><div class="wrap">
<section class="ds-gd ds-sec" aria-labelledby="name-h">
<div class="gd-text">
<p class="ds-k">General description</p>
<h1 class="ds-name" id="name-h">Brendan<br>Lynskey</h1>
<p class="lede">A staff-level engineer across hardware (RTL and FPGA, DSP, signal integrity), software and agentic AI.</p>
<p class="sub">More than 25 years in hardware; for the last two years, almost entirely software (agentic AI in Python). Read my CV, ask a chat agent about my career, or look through the portfolio: explainer sites, deck series and simulators I built for my own learning.</p>
<div class="btns">
{twin_btn}<a class="btn{"" if twin_btn else " primary"}" href="/cv/">Read the CV</a>
</div>
</div>
<div class="pins">
<p class="ds-k" aria-hidden="true">Pin configuration · Top view</p>
{pins()}
</div>
</section>

<section class="ds-sec ds-two" aria-label="Features and electrical characteristics">
<div class="feat">
<h2 class="ds-k">Features</h2>
<ul>{features(n_sites)}</ul>
</div>
<div class="elec">
<h2 class="ds-k">Electrical characteristics · T = {BUILT[:4]}</h2>
{characteristics(n_sites)}
<p class="ds-note">The counts are taken from each index's README when this page is built; the SI deviation is the largest difference from {COUNTS["Signal_Integrity"]["published_checks"]} independently published results.</p>
</div>
</section>

<section class="ds-sec" aria-labelledby="fig1-h">
<h2 class="ds-k" id="fig1-h">Figure 1 · Timing diagram, 1994–{BUILT[:4]}</h2>
<p class="ds-note" style="margin:0 0 1rem">Each trace is high while the role is held. Newest at the top. The roles, with their dates, are in the <a href="/cv/#experience">CV</a>.</p>
{td}
</section>

<section class="ds-sec" aria-labelledby="fig2-h">
<h2 class="ds-k" id="fig2-h">Figure 2 · Functional block diagram</h2>
<div class="fig2">
<figure class="hero-fig">
<canvas id="hero-canvas" width="560" height="300" role="img" aria-label="Animation: an agent loop sends operands into a four-by-four systolic array; the operands move one cell per cycle and each cell fills as it accumulates; the results drain back to the loop, which checks them against a reference before planning the next step."></canvas>
<figcaption>Illustration: an agent loop drives a 4×4 output-stationary systolic array and checks every result against a reference.</figcaption>
<button type="button" id="hero-pause">Pause</button>
</figure>
<div class="fd">
<p><b>I built these sites and decks for my own learning, and I am still working my way through them.</b></p>
<p>They are where my interests are heading: the hardware I know, and the AI systems that run on it. Every number in them comes from tested code or a cited source.</p>
</div>
</div>
</section>

<section class="ds-sec" id="portfolio" aria-labelledby="apps-h">
<h2 class="ds-k" id="apps-h">Typical applications · Home ground and four tracks</h2>
<div class="apps">
{apps()}
</div>
<div class="btns"><a class="btn primary" href="/sites/">Open the portfolio →</a><a class="btn" href="/checks/">How I check the numbers →</a></div>
</section>

<section class="ds-sec" id="cv-twin" aria-labelledby="ord-h" style="border-bottom:0">
<h2 class="ds-k" id="ord-h">Ordering information · CV and contact</h2>
{ordering()}
</section>
</div></main>
<script src="/assets/hero.js" defer></script>
""" + foot(' <a class="o-link" href="/optalysys/" title="Optalysys-related work"><span class="sr">Optalysys-related work</span><span aria-hidden="true">O</span></a>', twin=True, path="/")


def sites_page():
    groups = DATA["groups"]
    tracks = []
    for g in groups:
        cards = "\n".join(site_card(s, g["label"]) for s in sites_in(g["key"]))
        tracks.append(f"""<div class="track" id="track-{g["key"]}">
<div class="track-head" style="color:var(--t-{g["key"]})"><svg viewBox="0 0 32 32" aria-hidden="true">{TRACK_SHAPE[g["key"]]}</svg>
<h3 style="color:var(--text)">{e(g["label"])}</h3><p>{e(g["blurb"])}</p></div>
<div class="grid{" two" if len(sites_in(g["key"])) % 3 else ""}">
{cards}
</div>
</div>""")
    rtl, rtl_src = q("rtl_array")
    lg, lg_src = q("lg_check")
    mcp, mcp_src = q("mcp")
    pt, pt_src = q("pt_decoder")
    desc = ("Brendan Lynskey's portfolio: hardware, DSP and signal-integrity deck series, sixteen interactive "
            "explainer sites in four tracks, showcases and how every number is checked. Built for his own learning.")
    return head(f"Portfolio · {NAME}", desc, "/sites/", twin=True) + f"""<main id="main">
<section class="hero page"><div class="wrap">
<p class="eyebrow">Portfolio</p>
<h1>Sites, decks and simulators</h1>
<p class="lede">I built all of this for my own learning, and I am still working my way through it.</p>
<p class="sub">Hardware, DSP and signal integrity first, where most of my career has been; then sixteen interactive explainer sites in four tracks, the showcases, how the numbers are checked, and the deck library.</p>
<p class="jump"><a href="#hardware">Hardware</a><a href="#sites">Sites</a><a href="#showcases">Showcases</a><a href="#checks">Checks</a><a href="#decks">Decks</a><a href="#built">Method</a></p>
</div></section>

<section class="block" id="hardware" aria-labelledby="hardware-h"><div class="wrap">
<div class="block-head"><div><p class="eyebrow">Home ground</p><h2 id="hardware-h">Hardware, DSP and signal integrity</h2></div>
<p>Where most of my career has been: channels and equalisers, RTL and its verification, accelerator simulators and the DSP behind audio. Each card links a series hub; the hubs link the decks.</p></div>
<div class="hgrid">
{"".join(hw_card(h) for h in HARDWARE)}
</div>
</div></section>

<section class="block" id="sites" aria-labelledby="sites-h"><div class="wrap">
<div class="block-head"><div><p class="eyebrow">Interactive sites</p><h2 id="sites-h">Sixteen sites, four tracks</h2></div>
<p><b>I built these sites for my own learning, and I am still working my way through them.</b> Each one is a computed, animated reading experience: the animations are drawn from a tested model, not hand-made. Every site's header has a menu to all the others, and every repository ships its models, fixtures and CI.</p></div>
{"".join(tracks)}
</div></section>

<section class="block" id="showcases" aria-labelledby="showcases-h"><div class="wrap">
<div class="block-head"><div><p class="eyebrow">Showcases</p><h2 id="showcases-h">Hardware agents and compute experiments</h2></div></div>
<div class="grid">
{"".join(showcase_card(c) for c in SHOWCASES)}
</div>
</div></section>

<section class="block" id="checks" aria-labelledby="checks-h"><div class="wrap">
<div class="block-head"><div><p class="eyebrow">Verification</p><h2 id="checks-h">How I check the numbers</h2></div>
<p>A model that agrees only with itself proves little, so every site is checked against something independent of it. Four examples, quoted from the sites:</p></div>
<div class="checks4">
<div class="stat"><span class="k">Against RTL</span><span class="n">613 / 0</span><p>Systolic: “{rtl}”, in Verilator.</p><a href="{rtl_src}">The check →</a></div>
<div class="stat"><span class="k">Against LangGraph</span><span class="n">39 sessions</span><p>Orchestration: real LangGraph 1.2.14. “{lg}”, the whole checkpoint history is compared.</p><a href="{lg_src}">The check →</a></div>
<div class="stat"><span class="k">Against the official SDKs</span><span class="n">160 messages</span><p>Protocols: “{mcp}”.</p><a href="{mcp_src}">The check →</a></div>
<div class="stat"><span class="k">Against PyTorch</span><span class="n">1e-5</span><p>Decoder: the TypeScript transformer is “{pt}”.</p><a href="{pt_src}">The check →</a></div>
</div>
<div class="btns"><a class="btn primary" href="/checks/">Every site's check, and where the models miss →</a></div>
</div></section>

<section class="block" id="decks" aria-labelledby="decks-h"><div class="wrap">
<div class="block-head"><div><p class="eyebrow">Deck library</p><h2 id="decks-h">The index hubs</h2></div>
<p>Lecture-style slide decks go deeper than the sites. These indexes list them; the counts are taken from each index's README when this page is built.</p></div>
<div class="list">
{"".join(index_row(x) for x in INDEXES)}
</div>
<div class="btns"><a class="btn primary" href="/library/">Browse the library: every index and its series →</a></div>
</div></section>

<section class="block" id="built" aria-labelledby="built-h"><div class="wrap">
<div class="block-head"><div><p class="eyebrow">Method</p><h2 id="built-h">How this is built</h2></div></div>
<div class="built">
<!-- how-this-is-built: start (src/how-this-is-built.html) -->
{HOW_BUILT}
<!-- how-this-is-built: end -->
</div>
</div></section>
</main>
""" + foot(twin=True, path="/sites/")


# ---------------------------------------------------------------- the checks page

def diagram(left, right, rel, caption):
    """Two boxes and the relation between them, as an inline SVG."""
    return f"""<svg viewBox="0 0 540 110" role="img" aria-label="{e(caption)}">
<rect x="4" y="25" width="164" height="60" rx="8" fill="none" stroke="var(--hw)" stroke-width="2"/>
<text x="86" y="50" text-anchor="middle" font-size="12" fill="var(--text)">{e(left[0])}</text>
<text x="86" y="69" text-anchor="middle" font-size="10.5" fill="var(--faint)">{e(left[1])}</text>
<rect x="372" y="25" width="164" height="60" rx="8" fill="none" stroke="var(--accent-line)" stroke-width="2"/>
<text x="454" y="50" text-anchor="middle" font-size="12" fill="var(--text)">{e(right[0])}</text>
<text x="454" y="69" text-anchor="middle" font-size="10.5" fill="var(--faint)">{e(right[1])}</text>
<path d="M178 55h184" stroke="var(--ok)" stroke-width="2" marker-end="url(#ah)" marker-start="url(#ah2)"/>
<text x="270" y="44" text-anchor="middle" font-size="12" fill="var(--ok)">{e(rel[0])}</text>
<text x="270" y="74" text-anchor="middle" font-size="10.5" fill="var(--faint)">{e(rel[1])}</text>
</svg>""".replace("<svg ", '<svg class="dh" ', 1) + f"""<svg class="dv" viewBox="0 0 300 236" role="img" aria-label="{e(caption)}">
<rect x="50" y="4" width="200" height="56" rx="8" fill="none" stroke="var(--hw)" stroke-width="2"/>
<text x="150" y="28" text-anchor="middle" font-size="14" fill="var(--text)">{e(left[0])}</text>
<text x="150" y="47" text-anchor="middle" font-size="12" fill="var(--faint)">{e(left[1])}</text>
<path d="M64 70v96" stroke="var(--ok)" stroke-width="2" marker-end="url(#ah)" marker-start="url(#ah2)"/>
<text x="80" y="112" font-size="14" fill="var(--ok)">{e(rel[0])}</text>
<text x="80" y="131" font-size="12" fill="var(--faint)">{e(rel[1])}</text>
<rect x="50" y="176" width="200" height="56" rx="8" fill="none" stroke="var(--accent-line)" stroke-width="2"/>
<text x="150" y="200" text-anchor="middle" font-size="14" fill="var(--text)">{e(right[0])}</text>
<text x="150" y="219" text-anchor="middle" font-size="12" fill="var(--faint)">{e(right[1])}</text>
</svg>"""


SVG_DEFS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="var(--ok)"/></marker>
<marker id="ah2" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10 0 0 5 10 10z" fill="var(--ok)"/></marker>
</defs></svg>"""


TABLE_HEADS = {"pt_training": ["Check", "Measured", "Tolerance"], "pt_adamw": ["Check", "Measured", "Tolerance"],
               "si_droop": ["Quantity", "This series", "Reference value", "Difference"]}


def qtable(qids):
    """Quotes that are rows of a markdown table, shown as a table (the cells are verbatim)."""
    head = TABLE_HEADS[qids[0]]
    rows = []
    for x in qids:
        cells = [c.strip() for c in html.unescape(QUOTES[x][2]).strip().strip("|").split("|")][:len(head)]
        rows.append("<tr>" + "".join(f"<td>{e(c.replace('`', ''))}</td>" for c in cells) + "</tr>")
    th = "".join(f'<th scope="col">{e(h)}</th>' for h in head)
    return f'<table class="qt"><thead><tr>{th}</tr></thead><tbody>{"".join(rows)}</tbody></table>'


def check_card(kicker, title, svg, quotes, note=""):
    plain = [x for x in quotes if x not in TABLE_HEADS]
    tab = [x for x in quotes if x in TABLE_HEADS]
    qs = "".join(f'<blockquote>“{q(x)[0]}”</blockquote>' for x in plain) + (qtable(tab) if tab else "")
    src = q(quotes[0])[1]
    return f"""<article class="check">
<span class="k">{e(kicker)}</span>
<h3>{e(title)}</h3>
{svg}
{qs}
{note}
<p class="src">Source: <a href="{e(src)}">{e(src.replace("https://", ""))}</a></p>
</article>"""


def by_key(k):
    for s in DATA["sites"]:
        if s["key"] == k:
            return s
    raise KeyError(k)


def checks_page():
    four = [
        check_card("Against RTL", "Systolic Arrays Explained: the model against SystemVerilog",
                   diagram(("cycle-accurate model", "Python, TS port"), ("SV systolic array", "Verilator 5.020"),
                           ("= every edge", "613 values, 0 mismatches"),
                           "The model compared with the SystemVerilog array after every clock edge"),
                   ["rtl_array", "rtl_mac"]),
        check_card("Against LangGraph", "Agent Orchestration Explained: the engine against real LangGraph",
                   diagram(("engine graph runtime", "Agent_Loop_Sim"), ("LangGraph 1.2.14", "StateGraph"),
                           ("= checkpoints", "39 sessions, 71 ops"),
                           "The engine's checkpoint history compared with LangGraph's after every operation"),
                   ["lg_sessions", "lg_check", "lg_equal"],
                   f'<p class="src">Where it is not exact, the site says so: “{q("lg_nondet")[0]}”; that one field is left out on both sides.</p>'),
        check_card("Against the official SDKs", "Agent Protocols Explained: the engine against the MCP and A2A SDKs",
                   diagram(("engine protocol", "state machines"), ("official SDKs", "mcp 2.3.0, a2a-sdk 1.2.2"),
                           ("= messages", "160 MCP, 56 A2A"),
                           "The engine's messages compared with recordings of the official SDKs"),
                   ["mcp_sessions", "mcp", "a2a"]),
        check_card("Against PyTorch", "Transformer Decoder and Training: TypeScript against PyTorch",
                   diagram(("TS transformer", "in your browser"), ("PyTorch", "fixtures, float64 run"),
                           ("≤ 1e-5", "op by op"),
                           "The browser's transformer compared with PyTorch operation by operation"),
                   ["pt_decoder", "pt_training", "pt_adamw"],
                   f'<p class="src">Training: two rows of the correctness table in <a href="{e(QUOTES["pt_training"][0])}">results.md</a> (all its checks and tolerances are there).</p>'),
    ]
    ports = []
    for k, qid in [("kernels", "kernels_exact"), ("numerics", "numerics_ref"), ("tradeoffs", "tradeoffs_350"),
                   ("inference", "serving_bytes"), ("evals", "evals_scipy")]:
        s = by_key(k)
        text, src = q(qid)
        ports.append(f'<li><b>{e(s["name"])}</b>: “{text}”. <a href="{e(src)}">Source</a></li>')
    kst, ksrc = q("kernels_stale")
    misses = []
    for qid, who in [("acc_band", "AI Accelerators Explained"), ("acc_mlperf", "AI Accelerators Explained (MLPerf Offline throughput against the model's compute ceiling)"),
                     ("acc_miss", "AI Accelerators Explained"), ("racks_band", "AI Racks Explained (spec cross-checks against published figures)"),
                     ("arch_band", "LLM Architectures Explained"), ("arch_approx", "LLM Architectures Explained"),
                     ("si_droop", "Signal Integrity (an internal check: time domain against frequency domain)"),
                     ("cit_neg", "Compute in Transit (the experiment's result)")]:
        text, src = q(qid)
        body = qtable([qid]) if qid in TABLE_HEADS else f"“{text}”"
        misses.append(f'<li><b>{e(who)}</b>: {body} <a href="{e(src)}">Source</a></li>')
    rows = []
    for s in DATA["sites"]:
        rows.append(f"""<tr><td><span class="site"><img src="/assets/icons/{s["key"]}.svg" alt="" width="18" height="18"><a href="{e(s["landing"])}">{e(s["name"])}</a></span></td>
<td>{e(s["claim"])}</td><td><a href="{e(s["evidence"])}">Evidence<span class="sr"> for {e(s["name"])}</span></a></td></tr>""")
    si = COUNTS["Signal_Integrity"]
    sources = [x for x in si["sources"] if not any(y != x and y.startswith(x) for y in si["sources"])]
    sv19, sv19src = q("sv_19")
    svb, _ = q("sv_broken")
    desc = ("How the numbers on Brendan Lynskey's sixteen interactive sites are checked: RTL in Verilator, "
            "real LangGraph, the official MCP and A2A SDKs, PyTorch, exact ports with fixtures in CI, and "
            "validation bands that show where the models miss.")
    return head("How I check the numbers · " + NAME, desc, "/checks/") + SVG_DEFS + f"""<main id="main"><div class="wrap">
<section class="hero">
<p class="eyebrow">Verification</p>
<h1>How I check the numbers</h1>
<p class="lede">Every number on the sites comes from tested code or a cited, dated source, and every model is checked against something independent of it: RTL, a real framework, an official SDK, PyTorch or a published figure.</p>
<p class="sub">The quotes below are copied from each site's About page, its README or its <code>results.md</code>, and a script checks that every quote still appears, word for word, on the page it links to.</p>
</section>

<section class="block" aria-labelledby="four-h">
<h2 id="four-h">Four checks, in pictures</h2>
<div class="big4">
{"".join(four)}
</div>
</section>

<section class="block" aria-labelledby="ports-h">
<h2 id="ports-h">Exact ports, with fixtures in CI</h2>
<div class="prose">
<p>Each site's browser code is a TypeScript port of a Python reference. The reference writes JSON fixtures, and the site's unit tests require the port to reproduce them; for most sites exactly, with no tolerance. On GPU Kernels Explained, for example, “{kst}” (<a href="{e(ksrc)}">source</a>).</p>
</div>
<div class="miss" style="margin-top:1rem"><ul>
{"".join(ports)}
</ul></div>
</section>

<section class="block" aria-labelledby="bands-h">
<h2 id="bands-h">Sourced specs, validation bands, and where the models miss</h2>
<div class="prose"><p>The hardware sites take every specification from a dated source and never use vendor claims as inputs. Their models are then checked against published figures that they do not take as inputs, and the misses are reported, not hidden.</p></div>
<div class="miss" style="margin-top:1rem"><ul>
{"".join(misses)}
</ul></div>
</section>

<section class="block" aria-labelledby="hw-h">
<h2 id="hw-h">The hardware decks</h2>
<div class="prose">
<p><b>Signal Integrity.</b> {si["published_checks"]} of the series' results are cross-checked against independently published values ({e(", ".join(sources))}); the largest difference is {si["worst_pct"]:.2f} %. Its README lists every check, internal ones included (<a href="{e(QUOTES["si_verified"][0])}">the table</a>).</p>
<p><b>RTL challenges.</b> Parsing is not simulating: “{svb}”. Today: “{sv19}” (<a href="{e(sv19src)}">source</a>).</p>
</div>
</section>

<section class="block" aria-labelledby="all-h">
<h2 id="all-h">Every site's check</h2>
<p class="sub">Each site's “How this is checked” line, as it appears on its landing page, with the link to the evidence.</p>
<table class="tbl" style="margin-top:1rem">
<thead><tr><th scope="col">Site</th><th scope="col">How it is checked</th><th scope="col">Evidence</th></tr></thead>
<tbody>
{"".join(rows)}
</tbody></table>
</section>
</div></main>
""" + foot(path="/checks/")


# ---------------------------------------------------------------- the /optalysys/ page

O_CSS = """
.o-hero .lede{max-width:36rem}
.o-fig svg{width:100%;height:auto;display:block}
.o-fig .flow{fill:none;stroke:var(--hw2);stroke-width:2.4;stroke-linecap:round;stroke-dasharray:5 15;animation:o-flow 1.1s linear infinite}
.o-fig .rail{fill:none;stroke:var(--hw2);stroke-width:1.4;opacity:.28}
.o-fig .el{fill:none;stroke:var(--ok);stroke-width:2;stroke-dasharray:3 9;animation:o-flow 1.1s linear infinite}
.o-fig.paused .flow,.o-fig.paused .el{animation-play-state:paused}
.o-fig .box{fill:var(--surface);stroke:var(--border)}
.o-fig .lo{fill:none;stroke:#a855f7;stroke-width:1.4;stroke-dasharray:2 4;opacity:.8}
.o-fig .drv{stroke:var(--ok);stroke-width:2}
.o-fig .rx{fill:var(--surface);stroke:var(--text);stroke-width:1.4}
.o-fig .ps{fill:var(--surface);stroke:var(--hw2)}
.o-fig text{font-size:10.5px;fill:var(--faint)}
.o-fig .lbl{fill:var(--text);font-size:11px}
@keyframes o-flow{to{stroke-dashoffset:-20}}
.o-map{display:grid;gap:.75rem;grid-template-columns:minmax(0,1fr);margin-top:2rem}
@media (min-width:760px){.o-map{grid-template-columns:repeat(3,minmax(0,1fr))}}
.o-map a{display:flex;gap:.8rem;align-items:center;padding:.8rem 1rem;border:1px solid var(--border);border-radius:.6rem;background:var(--raised);text-decoration:none;transition:border-color .2s,transform .2s}
.o-map a:hover,.o-map a:focus-visible{border-color:var(--c);transform:translateY(-2px)}
.o-num{flex:none;display:inline-flex;align-items:center;justify-content:center;width:2.1rem;height:2.1rem;border-radius:50%;border:2px solid var(--c);color:var(--c);font:700 .95rem var(--mono)}
.o-map b{display:block;font-weight:600}
.o-map small{display:block;color:var(--muted);font-size:.8rem}
.o-sec{padding-top:3.75rem}
.o-sec-head{display:flex;gap:1rem;align-items:flex-start;margin-bottom:1.4rem}
.o-sec-head .o-num{width:2.75rem;height:2.75rem;font-size:1.15rem;margin-top:.2rem}
.o-sec-head p{color:var(--muted);max-width:42rem;margin-top:.35rem}
.o-grid{display:grid;gap:1.1rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,22rem),1fr))}
.o-card{position:relative;display:flex;flex-direction:column;border:1px solid var(--border);border-radius:.7rem;background:var(--raised);overflow:hidden;transition:border-color .2s,box-shadow .2s}
.o-card:hover{border-color:var(--c);box-shadow:0 10px 30px -18px var(--c)}
.o-card .thumb{aspect-ratio:16/9;width:100%;object-fit:cover;object-position:top;border-bottom:1px solid var(--border);background:var(--surface)}
.o-card .body{padding:1rem 1.15rem 1.15rem;display:flex;flex-direction:column;gap:.65rem;flex:1}
.o-card .k{font:500 .68rem/1.4 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.o-card .k span{color:var(--text)}
.o-card .k span::before{content:"";display:inline-block;width:.5rem;height:.5rem;border-radius:50%;background:var(--c);margin-right:.45rem;vertical-align:.05rem}
.o-card h3{font-size:1.2rem;letter-spacing:-.015em}
.o-card h3 a{text-decoration:none}
.o-card h3 a::after{content:"";position:absolute;inset:0;z-index:1}
.o-card .what{color:var(--muted);font-size:.93rem}
.o-card .why{font-size:.9rem;border-left:3px solid var(--c);background:color-mix(in srgb,var(--c) 7%,transparent);padding:.55rem .75rem;border-radius:0 .35rem .35rem 0}
.o-card .why b,.o-card .what b{display:block;font:500 .66rem var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--faint);margin-bottom:.15rem}
.o-card .more{margin-top:auto;display:flex;flex-wrap:wrap;gap:.25rem 1rem;font-size:.86rem;position:relative;z-index:2}
.o-card .more a{display:inline-flex;align-items:center;min-height:32px;color:var(--accent-text);text-underline-offset:3px}
@media (min-width:900px){.o-card.wide{grid-column:1/-1;display:grid;grid-template-columns:minmax(0,46%) minmax(0,1fr)}
 .o-card.wide .thumb{height:100%;aspect-ratio:auto;object-position:left top;border-bottom:0;border-right:1px solid var(--border)}}
.o-src{padding-top:3.75rem}
.o-src-lede{color:var(--muted);max-width:44rem;margin:.4rem 0 1.25rem}
.o-src-grid{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,24rem),1fr))}
.o-src-grid>div{border:1px solid var(--border);border-radius:.7rem;background:var(--raised);padding:1rem 1.15rem}
.o-src h3{font:600 .72rem var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--faint);margin-bottom:.5rem}
.o-src ul{list-style:none;margin:0;padding:0}
.o-src li{padding:.5rem 0;border-top:1px solid var(--border);font-size:.9rem}
.o-src li:first-child{border-top:0;padding-top:0}
.o-src li a{color:var(--accent-text);text-underline-offset:3px}
.o-src li span{display:block;color:var(--muted);font-size:.8rem;margin-top:.15rem}
.o-end{margin-top:3.5rem;padding:1.4rem 1.25rem;border:1px solid var(--border);border-radius:.7rem;background:var(--surface)}
.o-end p{color:var(--muted);max-width:44rem}
"""

O_COLOUR = {"hardware": "var(--hw2)", "workloads": "var(--accent-line)", "engineering": "var(--hw)"}

def o_fig():
    """The 4-point optical DFT as the simulator models it: a 2-stage radix-2 mesh of 2x2 couplers, a -j phase
    shifter and one waveguide crossing, read by coherent receivers fed from the same laser (the real layout is not
    published)."""
    R = [80, 130, 180, 230]                     # rows: x0, x2, x1, x3 (bit-reversed in, so couplers are adjacent)
    out = []
    W = lambda d: f'<path class="rail" d="{d}"/><path class="flow" d="{d}"/>'

    def coupler(x0, ya, yb):
        m, g = (ya + yb) / 2, 5
        top = f"M{x0} {ya}C{x0 + 14} {ya} {x0 + 10} {m - g} {x0 + 24} {m - g}H{x0 + 36}C{x0 + 50} {m - g} {x0 + 46} {ya} {x0 + 60} {ya}"
        bot = f"M{x0} {yb}C{x0 + 14} {yb} {x0 + 10} {m + g} {x0 + 24} {m + g}H{x0 + 36}C{x0 + 50} {m + g} {x0 + 46} {yb} {x0 + 60} {yb}"
        return W(top) + W(bot)

    # laser, a 1x4 splitter bus and the local-oscillator tap
    out.append('<rect class="box" x="6" y="140" width="40" height="30" rx="5"/><text class="lbl" x="26" y="159" text-anchor="middle">laser</text>')
    out.append(W("M46 155H58") + W("M58 155V80") + W("M58 155V230"))
    out.append('<path class="lo" d="M58 80V44H380V214"/><text x="150" y="38">local oscillator, from the same laser</text>'
               '<text x="88" y="38" text-anchor="middle">bits ↓</text>')
    for k, y in enumerate(R):
        lab = ["x0", "x2", "x1", "x3"][k]
        out.append(W(f"M58 {y}H70") + f'<rect class="box" x="70" y="{y - 11}" width="36" height="22" rx="4"/>'
                   f'<path class="drv" d="M88 {y - 25}V{y - 11}"/>'
                   + W(f"M106 {y}H140") + f'<text x="120" y="{y - 6}" text-anchor="middle">{lab}</text>')
    # stage 1: couplers on (x0,x2) and (x1,x3)
    out.append(coupler(140, R[0], R[1]) + coupler(140, R[2], R[3]))
    # -j on row 4, straight through on rows 1-3
    for y in R[:3]:
        out.append(W(f"M200 {y}H246"))
    out.append(W(f"M200 {R[3]}H210") + f'<rect class="ps" x="210" y="{R[3] - 10}" width="26" height="20" rx="3"/>'
               f'<text class="lbl" x="223" y="{R[3] + 4}" text-anchor="middle">−j</text>' + W(f"M236 {R[3]}H246"))
    # one waveguide crossing between rows 2 and 3
    out.append(W(f"M246 {R[0]}H276") + W(f"M246 {R[3]}H276") + W(f"M246 {R[1]}L276 {R[2]}") + W(f"M246 {R[2]}L276 {R[1]}"))
    # stage 2: couplers on the new adjacent pairs
    out.append(coupler(276, R[0], R[1]) + coupler(276, R[2], R[3]))
    for k, y in enumerate(R):
        out.append(W(f"M336 {y}H392") + f'<text x="356" y="{y - 6}" text-anchor="middle">{["X0", "X2", "X1", "X3"][k]}</text>')
        # coherent receiver: the LO mixes in, then a right-pointing amplifier (balanced detector + TIA)
        out.append(f'<path class="lo" d="M380 {y - 16}H398V{y - 9}"/><path class="rx" d="M392 {y - 12}L414 {y}L392 {y + 12}Z"/>'
                   f'<path class="el" d="M414 {y}H446"/>')
    out.append('<text x="170" y="262" text-anchor="middle">stage 1</text><text x="306" y="262" text-anchor="middle">stage 2</text>'
               '<text x="261" y="276" text-anchor="middle">crossing</text>')
    # read-out: two modes
    out.append('<rect class="box" x="446" y="62" width="148" height="88" rx="7"/>'
               '<text class="lbl" x="458" y="84">exact mode</text><text x="458" y="102">PAM4 slicers + table</text>'
               '<text x="458" y="118">→ exact integers</text><text x="458" y="136">NTT, FHE</text>'
               '<rect class="box" x="446" y="160" width="148" height="88" rx="7"/>'
               '<text class="lbl" x="458" y="182">approximate mode</text><text x="458" y="200">ADCs</text>'
               '<text x="458" y="216">→ a few bits</text><text x="458" y="234">FFT- and AI-style</text>')
    hdr = ('<text x="26" y="20" text-anchor="middle">source</text><text x="88" y="20" text-anchor="middle">modulators</text>'
           '<text x="238" y="20" text-anchor="middle">4-point optical DFT</text><text x="403" y="20" text-anchor="middle">receivers</text>'
           '<text x="520" y="20" text-anchor="middle">read-out</text>')
    return f'<svg viewBox="0 0 600 280" role="img" aria-labelledby="o-fig-cap">{hdr}{"".join(out)}</svg>'


def o_card(it, colour):
    links = "".join(f'<a href="{e(u)}">{e(t)}<span class="sr"> ({e(it["title"])})</span></a>' for t, u in it["links"])
    return f"""<article class="o-card{" wide" if it.get("wide") else ""}" style="--c:{colour}">
<img class="thumb" src="/assets/shots/{it["key"]}.webp" alt="" width="640" height="360" loading="lazy" decoding="async">
<div class="body">
<p class="k"><span>{e(it["kind"])}</span> · {e(it["size"])}</p>
<h3><a href="{e(it["href"])}">{e(it["title"])}</a></h3>
<p class="what"><b>What it does</b>{e(it["what"])}</p>
<p class="why"><b>Why I built it</b>{e(it["why"])}</p>
<p class="more">{links}</p>
</div>
</article>"""


def o_sources():
    out = []
    for group, items in O_SOURCES:
        lis = "".join(f'<li><a href="{e(u)}">{e(t)}</a><span>Used in: {e(used)}</span></li>' for t, u, used in items)
        out.append(f'<div><h3>{e(group)}</h3><ul>{lis}</ul></div>')
    return "\n".join(out)


def optalysys_page():
    secs, chips = [], []
    for sec in O_SECTIONS:
        c = O_COLOUR[sec["key"]]
        chips.append(f'<a href="#{sec["key"]}" style="--c:{c}"><span class="o-num">{sec["n"]}</span>'
                     f'<span><b>{e(sec["title"])}</b><small>{len(sec["items"])} '
                     f'{"resource" if len(sec["items"]) == 1 else "resources"}</small></span></a>')
        cards = "\n".join(o_card(it, c) for it in sec["items"])
        secs.append(f"""<section class="o-sec" id="{sec["key"]}" aria-labelledby="{sec["key"]}-h" style="--c:{c}">
<div class="o-sec-head"><span class="o-num" aria-hidden="true">{sec["n"]}</span>
<div><h2 id="{sec["key"]}-h">{e(sec["title"])}</h2><p>{e(sec["lede"])}</p></div></div>
<div class="o-grid">
{cards}
</div>
</section>""")
    desc = ("Explainer sites, deck series and simulators Brendan Lynskey built to learn the areas Optalysys works "
            "in: optical computing, fully homomorphic encryption, AI workloads and simulation engineering.")
    script = """<script>(()=>{const f=document.getElementById("o-fig"),b=document.getElementById("o-pause");
const set=p=>{f.classList.toggle("paused",p);b.textContent=p?"Play":"Pause";b.setAttribute("aria-pressed",String(p))};
set(matchMedia("(prefers-reduced-motion: reduce)").matches);b.addEventListener("click",()=>set(!f.classList.contains("paused")))})()</script>"""
    return head(f"Optalysys · {NAME}", desc, "/optalysys/", f"<style>{O_CSS.strip()}</style>\n", noindex=True) + f"""<main id="main">
<section class="hero o-hero"><div class="wrap">
<div class="hero-grid">
<div class="intro">
<p class="eyebrow">For Optalysys</p>
<h1>Computing with light: encryption and AI</h1>
<p class="lede">Optalysys works on optical computing, including for fully homomorphic encryption. These are the sites, decks and simulators I built to learn the areas that work touches: the optics, encrypted computing, AI workloads, and how to simulate all three.</p>
</div>
<figure class="hero-fig o-fig" id="o-fig">
{o_fig()}
<figcaption id="o-fig-cap">Illustration, as the simulator models it: one laser feeds four modulators driven by bits, and a local oscillator. A two-stage mesh of 2×2 couplers, a −j phase shifter and one crossing computes a 4-point DFT in one pass; coherent receivers read it. In exact mode the levels decode to exact integers (NTT, FHE); in approximate mode ADCs keep a few bits (FFT- and AI-style work). The real layout is not published.</figcaption>
<button type="button" id="o-pause" aria-pressed="false">Pause</button>
</figure>
<div class="rest">
<p class="sub">I built all of this for my own learning, and I am still working my way through it. Each page below says what it does and why I made it. They follow one path: the hardware, the workloads it might run, and the engineering that makes a simulator's answers trustworthy.</p>
</div>
</div>
<nav class="o-map" aria-label="Sections">
{"".join(chips)}
</nav>
</div></section>
<div class="wrap">
{"".join(secs)}
<section class="o-src" id="sources" aria-labelledby="sources-h">
<h2 id="sources-h">Sources</h2>
<p class="o-src-lede">The material rests on these: the module's paper and patents, its developer's public talks, and the encryption and AI work it builds on. Each line says where it is used.</p>
<div class="o-src-grid">
{o_sources()}
</div>
</section>
<div class="o-end">
<p>The rest of my work, from signal integrity to agentic AI, is in the <a href="/sites/">portfolio</a>, and my experience is in the <a href="/cv/">CV</a>.</p>
</div>
</div>
</main>
{script}
""" + foot()


def not_found():
    return head("Page not found · " + NAME, "This page does not exist. The portfolio home lists everything.", "/404.html") + """<main id="main"><div class="wrap">
<section class="hero">
<p class="eyebrow">404</p>
<h1>Page not found</h1>
<p class="lede">There is nothing at this address.</p>
<div class="btns"><a class="btn primary" href="/">Portfolio home</a><a class="btn" href="/sites/">The portfolio</a><a class="btn" href="/checks/">How I check the numbers</a></div>
</section>
</div></main>
""" + foot(path="/404.html")


# ---------------------------------------------------------------- the CV page

CV_CSS = r"""
:root{--d-hardware:#9c4a26;--d-fpga:#1f3b5c;--d-dsp:#24756a;--d-crypto:#5f3a78;--d-sw:#4f6b1f;--d-ai:#8a6510;--d-hatch:rgba(255,255,255,.3);--d-fg:#ffffff;--d-edu:#8a8a8a}
@media (prefers-color-scheme:dark){:root{--d-hardware:#e39a5b;--d-fpga:#a3bde0;--d-dsp:#7cc7b6;--d-crypto:#bfa3d8;--d-sw:#a9c46e;--d-ai:#e0bf5c;--d-hatch:rgba(0,0,0,.22);--d-fg:#0a0a0a;--d-edu:#737373}}
.cv-head{padding:3rem 0 0}
.cv-head h1{margin-top:.5rem}
.cv-head .lede{max-width:44rem}
.meta{display:flex;flex-wrap:wrap;gap:.35rem 1.25rem;margin-top:1.1rem;font-size:.93rem;color:var(--muted);list-style:none;padding:0}
.meta a{color:var(--accent-text);text-underline-offset:3px;display:inline-flex;align-items:center;min-height:32px}
.meta li{display:flex;align-items:center}
.cv-head .btns{margin-top:1.25rem}
.cv-sec{padding:2.75rem 0 0;display:grid;gap:.75rem 2rem;grid-template-columns:minmax(0,1fr)}
@media (min-width:900px){.cv-sec{grid-template-columns:10rem minmax(0,1fr)}.cv-sec>h2{padding-top:.2rem}}
.cv-sec>h2{font:600 .78rem/1.4 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--accent-text)}
.profile{font-size:1.06rem;line-height:1.65;max-width:46rem}
.tl{margin:0}
.tl-strip{position:relative}
.tl-svg{display:block;width:100%;height:5rem;overflow:visible}
.tl-svg a rect{transition:opacity .15s}
.tl-svg:hover a rect{opacity:.55}
.tl-svg a:hover rect,.tl-svg a:focus rect{opacity:1}
.tl-svg a:focus{outline:none}
.tl-svg a:focus-visible rect{stroke:var(--text);stroke-width:2.5px;vector-effect:non-scaling-stroke;opacity:1}
.tl-names{position:absolute;left:0;right:0;top:0;height:3.125rem;pointer-events:none;display:none}
.tl-names span{position:absolute;top:0;height:100%;display:flex;align-items:center;justify-content:safe center;font:600 .72rem/1 var(--sans);color:var(--d-fg);white-space:nowrap;overflow:hidden;letter-spacing:-.01em}
@media (min-width:760px){.tl-names{display:block}}
.tl-axis{position:relative;height:1.3rem;margin-top:.35rem;border-top:1px solid var(--border);font:500 .72rem/1 var(--mono);color:var(--faint)}
.tl-axis span{position:absolute;top:.35rem;transform:translateX(-50%)}
.tl-axis span::before{content:"";position:absolute;left:50%;top:-.4rem;height:.3rem;border-left:1px solid var(--border)}
@media (max-width:600px){.tl-axis span.near{display:none}}
.tl-axis span.first{transform:none}.tl-axis span.first::before{left:0}
.tl-axis span.last{transform:translateX(-100%)}.tl-axis span.last::before{left:100%}
.tl-out{min-height:3rem;margin-top:.6rem;font-size:.92rem}
.tl-out p{display:none}
.tl-out p.tl-hint{display:block;color:var(--faint)}
.tl-out b{font-weight:600}
.tl-out .d{color:var(--muted)}
.legend{display:flex;flex-wrap:wrap;gap:.35rem 1.1rem;font-size:.84rem;color:var(--muted);list-style:none;padding:0;margin:.25rem 0 0}
.legend li{display:flex;align-items:center;gap:.4rem}
.sw{display:inline-block;width:.8rem;height:.8rem;border-radius:2px;flex:none}
.sw.edu{height:.35rem}
.tl-text{margin-top:.75rem;font-size:.88rem;color:var(--muted)}
.tl-text summary{cursor:pointer;color:var(--accent-text);min-height:32px;display:inline-flex;align-items:center}
.tl-text ol{margin:.4rem 0 0;padding-left:1.2rem}
.roles{display:flex;flex-direction:column}
.role{display:grid;gap:.25rem 1.5rem;grid-template-columns:minmax(0,1fr);padding:1.25rem 0;border-top:1px solid var(--border)}
.role:first-child{border-top:0;padding-top:0}
@media (min-width:640px){.role{grid-template-columns:9.5rem minmax(0,1fr)}}
.when{font:500 .8rem/1.5 var(--mono);color:var(--faint);padding-top:.2rem}
.when span{white-space:nowrap}
.role h3{font-size:1.08rem}
.role h3 .at{font-weight:500;color:var(--muted)}
.where{display:flex;flex-wrap:wrap;align-items:center;gap:.3rem .9rem;font-size:.85rem;color:var(--faint);margin-top:.2rem}
.where .dom{display:inline-flex;align-items:center;gap:.35rem}
.where .sw{width:.6rem;height:.6rem;border-radius:50%}
.role .intro{margin-top:.55rem;color:var(--text)}
.role ul{margin:.5rem 0 0;padding-left:1.1rem;color:var(--muted)}
.role li{margin:.3rem 0}
.role li::marker{color:var(--faint)}
.work{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,17rem),1fr))}
.work .thumb{aspect-ratio:1200/630;object-fit:cover;object-position:top}
.work .url{display:none}
.work-note{color:var(--muted);font-size:.95rem;margin-bottom:1rem;max-width:42rem}
.work-note a{color:var(--accent-text)}
.skills{display:grid;gap:.9rem;margin:0}
.skills>div{display:grid;gap:.35rem 1rem;grid-template-columns:minmax(0,1fr)}
@media (min-width:640px){.skills>div{grid-template-columns:9.5rem minmax(0,1fr)}}
.skills dt{font-size:.86rem;font-weight:600;padding-top:.25rem}
.skills dd{margin:0}
.chips{display:flex;flex-wrap:wrap;gap:.35rem;list-style:none;margin:0;padding:0}
.chips li{font-size:.84rem;line-height:1.35;padding:.22rem .6rem;border:1px solid var(--border);border-radius:999px;background:var(--surface);color:var(--text)}
.edu,.certs{list-style:none;margin:0;padding:0;display:grid;gap:.75rem}
.edu li{display:grid;gap:.1rem 1.5rem;grid-template-columns:minmax(0,1fr)}
@media (min-width:640px){.edu li{grid-template-columns:9.5rem minmax(0,1fr)}}
.edu .yrs{font:500 .8rem/1.6 var(--mono);color:var(--faint)}
.edu b{font-weight:600}
.edu .sch{color:var(--muted)}
.certs{gap:.4rem}
.certs li{padding-left:1.1rem;position:relative}
.certs li::before{content:"";position:absolute;left:0;top:.62em;width:.45rem;height:.45rem;border-radius:50%;background:var(--accent-line)}
.certs-note{font-size:.85rem;color:var(--faint);margin-top:.6rem}
.purl{display:none}
@page{size:A4;margin:11mm 12mm}
@media print{
 :root{color-scheme:light;--bg:#fff;--surface:#f5f5f5;--raised:#fff;--border:#d4d4d4;--rule:#111;--text:#111;--muted:#333;--faint:#555;
  --accent:#f2a33a;--accent-text:#9a3d06;--accent-line:#b3410a;--accent-soft:#fbe7c6;
  --d-hardware:#9c4a26;--d-fpga:#1f3b5c;--d-dsp:#24756a;--d-crypto:#5f3a78;--d-sw:#4f6b1f;--d-ai:#8a6510;--d-hatch:rgba(255,255,255,.3);--d-fg:#fff;--d-edu:#8a8a8a}
 html{font-size:12px}
 body{font-size:8.6pt;line-height:1.36;-webkit-print-color-adjust:exact;print-color-adjust:exact}
 .wrap{max-width:none;padding:0}
 header.site,footer.site,.skip,.cv-head .btns,.tl-out,.tl-text,.work img,.work .more,.no-print{display:none!important}
 a{text-decoration:none}
 .cv-head{padding:0}
 .cv-head .eyebrow{display:none}
 .cv-head h1{font-size:20pt;margin:0}
 .cv-head .lede{font-size:10pt;margin-top:.15rem;max-width:none}
 .meta{margin-top:.35rem;font-size:8.4pt;gap:0 1rem}
 .meta a{min-height:0;color:var(--accent-text)}
 .meta .lbl{display:none}.purl{display:inline}
 .cv-sec{padding:.85rem 0 0;grid-template-columns:7rem minmax(0,1fr);gap:.2rem .8rem}
 .cv-sec>h2{font-size:6.8pt;letter-spacing:.06em;padding-top:.15rem}
 .profile{font-size:8.9pt;line-height:1.42;max-width:none}
 .tl-svg{height:2.9rem}
 .tl-svg:hover a rect{opacity:1}
 .tl-names{display:block;height:1.85rem}
 .tl-names span{font-size:6.2pt;letter-spacing:-.02em}
 .tl-axis{font-size:6.6pt;height:1rem;margin-top:.2rem}
 .legend{font-size:7pt;margin-top:0}
 .role{padding:.45rem 0;grid-template-columns:7.6rem minmax(0,1fr);gap:0 .9rem}
 .role li,.role .intro,.role h3{break-inside:avoid}
 .role h3{break-after:avoid}
 .role:first-child{padding-top:0}
 .when{font-size:7.2pt;padding-top:.1rem}
 .role h3{font-size:9.4pt}
 .where{font-size:7.4pt;margin-top:0}
 .role .intro{margin-top:.15rem}
 .role ul{margin-top:.15rem}
 .role li{margin:.05rem 0}
 .work{grid-template-columns:repeat(2,minmax(0,1fr));gap:.55rem 1rem}
 .work .card{border:0;border-radius:0;break-inside:avoid}
 .work .card .body{padding:0;gap:0}
 .work .card h3{font-size:8.6pt}
 .work .card .place,.work .card .checked{display:none}
 .work .card .blurb{font-size:7.6pt;color:var(--muted)}
 .work .url{display:block;font-size:7.2pt;color:var(--accent-text)}
 .work-note{font-size:7.6pt;margin-bottom:.35rem}
 .skills{gap:.2rem}
 .skills>div{grid-template-columns:7.6rem minmax(0,1fr);gap:0 .9rem}
 .skills dt{font-size:7.8pt;padding-top:0}
 .chips{gap:.15rem .25rem}
 .chips li{font-size:7.4pt;padding:.02rem .4rem;background:none}
 .edu{gap:.1rem}
 .edu li{grid-template-columns:7.6rem minmax(0,1fr);gap:0 .9rem}
 .edu .yrs{font-size:7.2pt}
 .certs{grid-template-columns:repeat(2,minmax(0,1fr));gap:.05rem 1rem}
 .certs-note{font-size:7.2pt;margin-top:.15rem}
 .cv-print-break{break-before:page}
}
"""

DOMAIN_VAR = {d: f"var(--d-{d})" for d in DOMAIN_LABEL}
# the software-side domains are hatched as well as coloured (AI at +45°, Software at -45°), so neighbouring bands
# differ in texture too; the hardware-side domains stay solid
HATCH = {"ai": 45, "sw": -45}
DOMAIN_BG = {d: (f"repeating-linear-gradient({HATCH[d]}deg,var(--d-hatch) 0 2px,transparent 2px 6px),var(--d-{d})"
                 if d in HATCH else f"var(--d-{d})") for d in DOMAIN_LABEL}
DOMAIN_FILL = {d: (f"url(#tl-h-{d})" if d in HATCH else f"var(--d-{d})") for d in DOMAIN_LABEL}
TL_DEFS = "<defs>" + "".join(
    f'<pattern id="tl-h-{d}" patternUnits="userSpaceOnUse" width="7" height="7" patternTransform="rotate({-a})">'
    f'<rect width="7" height="7" fill="var(--d-{d})"/><rect width="2.4" height="7" fill="var(--d-hatch)"/></pattern>'
    for d, a in HATCH.items()) + "</defs>"


def now_year():
    y, m, d = (int(x) for x in BUILT.split("-"))
    return y + (m - 1 + d / 31) / 12


def dates(r):
    return f"{r['start']} – {r['end']}"


def short(company):
    c = company.split(" (")[0].split(" /")[0]
    return c.split()[0] if len(c) > 14 else c


def role_label(r):
    names = [DOMAIN_LABEL[d] for d in r["domains"]]
    doms = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]
    return f"{r['title']}, {r['company']}, {r['place']}, {dates(r)} ({doms})"


def timeline():
    t0, t1 = 1994.0, now_year()
    W, span = 1000.0, now_year() - 1994.0

    def x(t):
        return (t - t0) / span * W

    bands, names, outs, rules, alt = [], [], [], [], []
    # Blocks abut: each role runs from its start to the next block's start (the strip is a coarse picture; exact
    # dates are in Experience). A gap between roles is full-time study, drawn as a grey block on the same row.
    # A uniform vertical hairline (in the page background colour) separates neighbouring blocks.
    roles = sorted(CV["roles"], key=lambda r: r["t0"])
    full_time = [ed for ed in CV["education"] if not ed["part_time"]]
    gaps = []  # (t0, t1, education item) for full-time study between roles
    for prev, nxt in zip(roles, roles[1:]):
        if prev["t1"] and nxt["t0"] - prev["t1"] > 0.25:
            ed = next((ed for ed in full_time
                       if int(ed["years"].split("–")[0]) <= nxt["t0"] and int(ed["years"].split("–")[1]) >= prev["t1"]), None)
            if ed:
                gaps.append((prev["t1"], nxt["t0"], ed))
    starts = sorted([r["t0"] for r in roles] + [g[0] for g in gaps])
    sep = ""  # dividers are drawn once, as vertical lines at block starts (below), so split blocks keep their labels clear

    def end_of(t):
        later = [u for u in starts if u > t]
        return later[0] if later else t1

    for r in roles:
        a, b = x(r["t0"]), x(end_of(r["t0"]))
        n = len(r["domains"])
        rects = "".join(f'<rect x="{a:.1f}" y="{i * 40 / n:.1f}" width="{b - a:.1f}" height="{40 / n:.1f}" fill="{DOMAIN_FILL[d]}"{sep}/>'
                        for i, d in enumerate(r["domains"]))
        label = role_label(r)
        bands.append(f'<a href="#r-{r["id"]}" data-r="{r["id"]}" aria-label="{e(label)}"><title>{e(label)}</title>{rects}</a>')
        names.append(f'<span style="left:{a / 10 + .15:.2f}%;width:{(b - a) / 10 - .3:.2f}%">{e(short(r["company"]))}</span>')
        doms = " + ".join(DOMAIN_LABEL[d] for d in r["domains"])
        outs.append(f'<p data-o="{r["id"]}"><b>{e(r["title"])}</b>, {e(r["company"])}, {e(r["place"])} · {e(dates(r))} '
                    f'<span class="d">· {e(doms)}</span></p>')
        rules.append(f'.tl:has([data-r="{r["id"]}"]:is(:hover,:focus-visible)) [data-o="{r["id"]}"]')
        alt.append(f"<li>{e(dates(r))}: {e(r['title'])}, {e(r['company'])} ({e(doms)})</li>")
    gap_of = {id(g[2]): g for g in gaps}
    for i, ed in enumerate(CV["education"]):
        y0, y1 = (int(v) for v in ed["years"].split("–"))
        if y1 <= t0:
            continue  # before the strip starts; it is in the Education section
        g = gap_of.get(id(ed))
        a, b = (x(g[0]), x(g[1])) if g else (x(max(y0, t0)), x(y1))
        label = f"{ed['degree']}, {ed['school']}, {ed['years']}{' (part-time)' if ed['part_time'] else ''}"
        top = (f'<rect x="{a:.1f}" y="0" width="{b - a:.1f}" height="40" fill="var(--d-edu)"{sep}/>' if g else "")
        bands.append(f'<a href="#education" data-r="e{i}" aria-label="{e(label)}"><title>{e(label)}</title>{top}'
                     f'<rect x="{a:.1f}" y="50" width="{b - a:.1f}" height="10" fill="var(--d-edu)"{sep}/></a>')
        outs.append(f'<p data-o="e{i}"><b>{e(ed["degree"])}</b>, {e(ed["school"])} · {e(ed["years"])}'
                    f'{" <span class=d>· part-time</span>" if ed["part_time"] else ""}</p>')
        rules.append(f'.tl:has([data-r="e{i}"]:is(:hover,:focus-visible)) [data-o="e{i}"]')
        alt.append(f"<li>{e(ed['years'])}: {e(ed['degree'])}, {e(ed['school'])}</li>")
    bands.append("".join(f'<line x1="{x(u):.1f}" x2="{x(u):.1f}" y1="0" y2="40" stroke="var(--bg)" stroke-width="2" '
                         f'vector-effect="non-scaling-stroke" aria-hidden="true"/>' for u in starts[1:]))
    years = list(range(2000, int(t1) + 1, 5))
    axis = [f'<span class="first" style="left:0">1994</span>']
    axis += [f'<span{" class=near" if x(y) > W - 90 else ""} style="left:{x(y) / 10:.2f}%">{y}</span>' for y in years if x(y) < W - 45]
    axis.append(f'<span class="last" style="left:100%">now</span>')
    css = (",\n".join(rules) + "{display:block}\n"
           ".tl:has(.tl-svg a:is(:hover,:focus-visible)) .tl-hint{display:none}")
    legend = "".join(f'<li><span class="sw" style="background:{DOMAIN_BG[d]}"></span>{e(lbl)}</li>'
                     for d, lbl in DOMAIN_LABEL.items())
    legend += '<li><span class="sw edu" style="background:var(--d-edu)"></span>Study</li>'
    return css, f"""<figure class="tl" aria-labelledby="tl-cap">
<p id="tl-cap" class="sr">Career timeline from 1994 to now: one band per role, coloured by domain, with study below. The same information is in the list under “The timeline as text” and in Experience.</p>
<div class="tl-strip">
<svg class="tl-svg" viewBox="0 0 1000 60" preserveAspectRatio="none" role="group" aria-label="Career timeline, 1994 to now">
{TL_DEFS}{"".join(bands)}
</svg>
<div class="tl-names" aria-hidden="true">{"".join(names)}</div>
</div>
<div class="tl-axis" aria-hidden="true">{"".join(axis)}</div>
<div class="tl-out" aria-hidden="true"><p class="tl-hint">Hover over a band, or tab to it, to see the role. Each band links to its entry below.</p>{"".join(outs)}</div>
<ul class="legend" aria-label="Key">{legend}</ul>
<details class="tl-text"><summary>The timeline as text</summary><ol>{"".join(alt)}</ol></details>
</figure>"""


def role_html(r):
    doms = "".join(f'<span class="dom"><span class="sw" style="background:{DOMAIN_BG[d]}"></span>{e(DOMAIN_LABEL[d])}</span>'
                   for d in r["domains"])
    lis = "".join(f"<li>{e(b)}</li>" for b in r["bullets"])
    return f"""<article class="role" id="r-{r["id"]}" data-title="{e(r["title"])}" data-company="{e(r["company"])}">
<p class="when"><span>{e(r["start"])}</span> – <span>{e(r["end"])}</span></p>
<div>
<h3>{e(r["title"])} <span class="at">· {e(r["company"])}</span></h3>
<p class="where"><span>{e(r["place"])}</span>{doms}</p>
<p class="intro">{e(r["intro"])}</p>
{f"<ul>{lis}</ul>" if lis else ""}
</div>
</article>"""


def selected_work():
    """Six cards; the titles, links and blurbs come from data/sites.json and tools/content.py."""
    sites = {s["key"]: s for s in DATA["sites"]}
    hubs = {h["key"]: h for h in HARDWARE}
    shows = {c["key"]: c for c in SHOWCASES}
    picks = [("show", "dse"), ("site", "decoder"), ("hub", "si"), ("site", "silicon"), ("site", "orchestration"),
             ("hub", "fhe")]
    cards = []
    for kind, k in picks:
        if kind == "site":
            s = sites[k]
            title, href, img, place, text = s["name"], s["landing"], f"cards/{k}.webp", s["blurb"], s["claim"]
        elif kind == "hub":
            h = hubs[k]
            title, href, img, place, text = h["title"], h["href"], f"shots/{k}.webp", "Hardware deck series", h["text"]
        else:
            c = shows[k]
            title, href, img, place, text = c["title"], c["href"], c["img"], "Showcase", c["text"]
        cards.append(f"""<article class="card">
<img class="thumb" src="/assets/{img}" alt="" width="600" height="315" loading="lazy" decoding="async">
<div class="body">
<p class="place">{e(place)}</p>
<h3><a href="{e(href)}">{e(title)}</a></h3>
<p class="blurb">{e(text)}</p>
<p class="url">{e(href.replace("https://", "").rstrip("/"))}</p>
</div>
</article>""")
    return "\n".join(cards)


def cv_page():
    css, tl = timeline()
    location = CV["location"].replace(", England", "")
    twin = DIGITAL_TWIN["url"] or DIGITAL_TWIN["interim_url"]
    twin_label = "Digital Twin" if DIGITAL_TWIN["url"] else "Digital Twin (earlier version)"

    def link(label, href):
        return (f'<li><a href="{e(href)}"><span class="lbl">{e(label)}</span>'
                f'<span class="purl">{e(href.replace("https://", "").replace("www.", ""))}</span></a></li>')
    meta = (f"<li>{e(location)}</li>" + link("LinkedIn", CV["linkedin"]) + link("GitHub", CV["github"])
            + link("Portfolio", BASE + "/") + f'<li class="no-print"><a href="{e(twin)}"{" data-twin" if DIGITAL_TWIN["url"] else ""}>{e(twin_label)}</a></li>')
    edu = "".join(f'<li><span class="yrs">{e(x["years"])}</span><span><b>{e(x["degree"])}</b>, '
                  f'<span class="sch">{e(x["school"])}{" (part-time)" if x["part_time"] else ""}</span></span></li>'
                  for x in CV["education"])
    certs = "".join(f"<li>{e(c)}</li>" for c in CV["certs"])
    desc = f"{CV['name']}: CV. {CV['headline']}"
    return head(f"{NAME}: CV", desc, "/cv/", f"<style>{CV_CSS.strip()}\n{css}</style>\n", twin=True) + f"""<main id="main"><div class="wrap">
<header class="cv-head">
<p class="eyebrow">Curriculum vitae</p>
<h1>{e(CV["name"])}</h1>
<p class="lede">{e(CV["headline"])}</p>
<ul class="meta">{meta}</ul>
<div class="btns"><a class="btn primary" href="{PDF}" download>Download PDF</a><a class="btn" href="/">Portfolio home</a></div>
</header>

<section class="cv-sec" aria-labelledby="profile-h">
<h2 id="profile-h">Profile</h2>
<p class="profile">{e(" ".join(PROFILE))}</p>
</section>

<section class="cv-sec" aria-labelledby="timeline-h">
<h2 id="timeline-h">Timeline</h2>
{tl}
</section>

<section class="cv-sec" id="experience" aria-labelledby="experience-h">
<h2 id="experience-h">Experience</h2>
<div class="roles">
{"".join(role_html(r) for r in CV["roles"])}
</div>
</section>

<section class="cv-sec" aria-labelledby="work-h">
<h2 id="work-h">Selected public work</h2>
<div>
<p class="work-note">I built these for my own learning, and I am still working my way through them. The full set is in the <a href="{BASE}/sites/">portfolio</a>.</p>
<div class="work">
{selected_work()}
</div>
</div>
</section>


<section class="cv-sec" id="education" aria-labelledby="education-h">
<h2 id="education-h">Education</h2>
<ul class="edu">{edu}</ul>
</section>

<section class="cv-sec" aria-labelledby="certs-h">
<h2 id="certs-h">Certifications</h2>
<div><ul class="certs">{certs}</ul>
<p class="certs-note">{e(CV["certs_note"][0].upper() + CV["certs_note"][1:])}.</p></div>
</section>
</div></main>
""" + foot(twin=True, path="/cv/")


# ---------------------------------------------------------------- the library page (brief 45)

LIB_CSS = (".lib{border-top:1px solid var(--border)}"
           ".lib-row{display:grid;grid-template-columns:minmax(0,13rem) minmax(0,1fr);gap:.5rem 1.5rem;padding:1.1rem 0;"
           "border-bottom:1px solid var(--border)}"
           ".lib-row h2{font-size:1.2rem;margin:0}.lib-row h2 a{text-decoration:none}.lib-row h2 a:hover{text-decoration:underline}"
           ".lib-row p{color:var(--muted);font-size:.93rem;margin-top:.3rem}"
           ".lib-row ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;align-content:flex-start;gap:.35rem .5rem}"
           ".lib-row li a{display:inline-flex;align-items:center;min-height:36px;padding:.2rem .7rem;border:1px solid var(--border);"
           "font-size:.95rem;color:var(--text);text-decoration:none;background:var(--raised)}"
           ".lib-row li a:hover,.lib-row li a:focus-visible{border-color:var(--accent-text);color:var(--accent-text)}"
           ".lib-row li.all a{border-style:dashed;color:var(--accent-text)}"
           "@media (max-width:700px){.lib-row{grid-template-columns:minmax(0,1fr)}}")


def library_row(x):
    chips = "".join(f'<li><a href="{e(u)}">{e(t)}</a></li>' for t, u, _ in x["series"])
    if x.get("total") and x["total"] > len(x["series"]):
        chips += f'<li class="all"><a href="{e(x["series_href"])}">All {x["total"]} series →</a></li>'
    return f"""<div class="lib-row">
<div><h2><a href="{e(x["href"])}">{e(x["title"])}</a></h2><p>{e(x["text"])}</p></div>
<ul aria-label="{e(x["title"])} series">{chips}</ul>
</div>"""


def library_page():
    shown = len({u for x in LIBRARY for _, u, _ in x["series"]})  # a hub listed by two indexes counts once
    lib = COUNTS["library"]["series"]
    desc = ("Brendan Lynskey's deck library: six subject indexes and the series hubs in each, from LLMs and "
            "hardware to software, mathematics, DSP and interview preparation.")
    return head(f"Library · {NAME}", desc, "/library/") + f"""<main id="main">
<section class="hero page"><div class="wrap">
<p class="eyebrow">Library</p>
<h1>The deck library</h1>
<p class="lede">Six subject indexes, and the series hubs in each.</p>
<p class="sub">The lecture-style slide decks behind the sites. Each index lists everything in it; each series hub lists its decks in reading order. The six indexes hold {lib} series between them (a series is one hub page that lists its decks); {shown} are linked below, and the LLMs index lists the other {lib - shown}.</p>
</div></section>
<section class="block" aria-label="Indexes and their series"><div class="wrap">
<div class="lib">
{"".join(library_row(x) for x in LIBRARY)}
</div>
<div class="btns"><a class="btn" href="/sites/">The interactive sites →</a><a class="btn" href="/checks/">How I check the numbers →</a></div>
</div></section>
</main>
""" + foot(path="/library/")


SR_CSS = ".sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}"


def main():
    global CSS
    CSS = CSS + SR_CSS + LIB_CSS
    pages = {"index.html": home(), "sites/index.html": sites_page(), "library/index.html": library_page(), "checks/index.html": checks_page(), "cv/index.html": cv_page(),
             "optalysys/index.html": optalysys_page(),
             "404.html": not_found()}
    for p, s in pages.items():
        os.makedirs(os.path.dirname(os.path.join(ROOT, p)) or ROOT, exist_ok=True)
        open(os.path.join(ROOT, p), "w").write(s)
        print("wrote", p, len(s))
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    urls = "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{BUILT}</lastmod></url>\n" for u in ["/", "/sites/", "/library/", "/cv/", "/checks/"])
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + urls + "</urlset>\n")


if __name__ == "__main__":
    main()
