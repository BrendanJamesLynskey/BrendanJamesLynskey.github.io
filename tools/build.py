"""Build the static site from data/ and tools/content.py.

    python3 tools/gather.py      # refresh data/ and the site icons and cards from their live sources
    python3 tools/build.py       # write index.html, checks/index.html, cv/index.html, 404.html, sitemap.xml,
                                 # robots.txt

The CSS is inlined into every page (one small stylesheet, so no extra request). The only script is
assets/hero.js. No external requests: system fonts, local images.
"""
import datetime
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import DIGITAL_TWIN, HARDWARE, INDEXES, QUOTES, SHOWCASES, GH  # noqa: E402
from cv import CV, DOMAIN_LABEL, PROFILE  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# the canonical address; GitHub Pages serves the same files from main, and its pages point here
BASE = "https://brendan-lynskey.vercel.app"
PDF = "/cv/Brendan_Lynskey_CV.pdf"
NAME = "Brendan Lynskey"
DATA = json.load(open(os.path.join(ROOT, "data", "sites.json")))
COUNTS = json.load(open(os.path.join(ROOT, "data", "counts.json")))
BUILT = os.environ.get("BUILD_DATE") or datetime.date.today().isoformat()
# the owner's paragraph; its own comments (the draft note) stay out of the published page
HOW_BUILT = re.sub(r"<!--.*?-->\s*", "", open(os.path.join(ROOT, "src", "how-this-is-built.html")).read(),
                   flags=re.S).strip()

e = html.escape


def q(qid):
    """A quote from content.QUOTES, escaped, and its source link."""
    shown, _, text = QUOTES[qid]
    text = re.sub(r"<sup>&minus;12</sup>", "⁻¹²", text)
    return e(html.unescape(text)), shown


CSS = r"""
:root{color-scheme:light dark;
 --bg:#ffffff;--surface:#fafafa;--raised:#ffffff;--border:#e5e5e5;--text:#171717;--muted:#525252;--faint:#6b6b6b;
 --accent:#4f46e5;--accent-fg:#ffffff;--accent-text:#4338ca;--accent-line:#4f46e5;--accent-soft:#eef2ff;
 --hw:#0284c7;--hw2:#ea580c;--ok:#15803d;
 --t-foundations:#0891b2;--t-hardware:#0284c7;--t-inference:#4f46e5;--t-agents:#dc2626;
 --sans:Inter,"Noto Sans",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
 --mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
@media (prefers-color-scheme:dark){:root{
 --bg:#0a0a0a;--surface:#171717;--raised:#121212;--border:#2a2a2a;--text:#f5f5f5;--muted:#d4d4d4;--faint:#a3a3a3;
 --accent:#4f46e5;--accent-fg:#ffffff;--accent-text:#a5b4fc;--accent-line:#818cf8;--accent-soft:#1e1b4b;
 --hw:#38bdf8;--hw2:#fb923c;--ok:#4ade80;
 --t-foundations:#22d3ee;--t-hardware:#38bdf8;--t-inference:#a5b4fc;--t-agents:#f87171}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased;scroll-padding-top:4.5rem}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 var(--sans)}
a{color:inherit}
img{max-width:100%;height:auto;display:block}
.wrap{max-width:68rem;margin:0 auto;padding:0 1.5rem}
@media (max-width:480px){.wrap{padding:0 1rem}}
.skip{position:absolute;left:-999px;top:0;background:var(--accent);color:var(--accent-fg);padding:.5rem 1rem;z-index:10}
.skip:focus{left:1rem;top:.5rem}
:focus-visible{outline:2px solid var(--accent-line);outline-offset:2px;border-radius:4px}
header.site{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 88%,transparent);
 backdrop-filter:saturate(1.4) blur(8px);-webkit-backdrop-filter:saturate(1.4) blur(8px);border-bottom:1px solid var(--border)}
header.site .wrap{display:flex;align-items:center;justify-content:space-between;gap:1rem;min-height:3.75rem}
.brand{display:flex;align-items:center;gap:.6rem;text-decoration:none;font-weight:600;font-size:.95rem;white-space:nowrap}
.brand img{width:24px;height:24px}
nav.top{display:flex;gap:1.25rem;font-size:.9rem}
nav.top a{text-decoration:none;color:var(--muted);padding:.4rem 0}
nav.top a:hover{color:var(--text)}
@media (max-width:520px){nav.top{gap:.9rem}nav.top .wide{display:none}}
@media (max-width:420px){nav.top .mid{display:none}}
.eyebrow{font:500 .75rem/1.4 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--accent-text);margin:0}
h1,h2,h3,h4{line-height:1.2;letter-spacing:-.015em;margin:0}
h1{font-size:clamp(2.4rem,6vw,3.5rem);font-weight:650;margin-top:.75rem}
h2{font-size:clamp(1.5rem,3vw,1.9rem);font-weight:650}
h3{font-size:1.1rem;font-weight:600}
p{margin:0}
.lede{font-size:clamp(1.15rem,2.2vw,1.35rem);line-height:1.5;color:var(--text);max-width:40rem;margin-top:1rem}
.sub{color:var(--muted);max-width:40rem;margin-top:.9rem}
.hero{padding:3.5rem 0 1rem}
.hero-grid{display:grid;gap:1.75rem 2.5rem;grid-template-columns:minmax(0,1fr)}
.rest{display:flex;flex-direction:column}
@media (min-width:900px){.hero-grid{grid-template-columns:minmax(0,1fr) minmax(0,30rem);grid-template-areas:"intro fig" "rest fig";row-gap:0}
 .intro{grid-area:intro}.hero-fig{grid-area:fig;align-self:center}.rest{grid-area:rest}}
@media (max-width:899px){.rest .btns{order:-1;margin-top:0}.rest .sub{margin-top:1.25rem}}
.btns{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:1.5rem}
.btn{display:inline-flex;align-items:center;min-height:44px;padding:.55rem 1.15rem;border-radius:.4rem;font-size:.92rem;font-weight:550;text-decoration:none;border:1px solid var(--border);background:var(--raised);color:var(--text)}
.btn:hover{border-color:var(--faint)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:var(--accent-fg)}
.btn.primary:hover{opacity:.92}
figure{margin:0}
.hero-fig{border:1px solid var(--border);border-radius:.6rem;padding:.75rem;background:var(--raised);position:relative}
.hero-fig canvas{width:100%;aspect-ratio:560/300;display:block}
.hero-fig figcaption{font-size:.8rem;color:var(--faint);margin-top:.4rem;padding-right:4.5rem}
.hero-fig button{position:absolute;right:.75rem;bottom:.6rem;font:500 .75rem var(--mono);color:var(--muted);background:var(--surface);border:1px solid var(--border);border-radius:.3rem;padding:.3rem .6rem;min-height:32px;cursor:pointer}
.facts{display:flex;flex-wrap:wrap;gap:.5rem 1.5rem;margin-top:2rem;padding:1rem 0 0;border-top:1px solid var(--border);font-size:.88rem;color:var(--muted)}
.facts b{color:var(--text);font-weight:650}
section.block{padding:3.5rem 0 0}
.block-head{margin-bottom:1.25rem}
.block-head h2{margin-top:.35rem}
.block-head>p{color:var(--muted);max-width:44rem;margin-top:.6rem}
.grid{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,19rem),1fr))}
.card{position:relative;display:flex;flex-direction:column;border:1px solid var(--border);border-radius:.6rem;background:var(--raised);overflow:hidden;transition:border-color .15s,transform .15s}
.card:hover{border-color:var(--faint)}
.card .thumb{aspect-ratio:1200/630;width:100%;object-fit:cover;background:var(--surface);border-bottom:1px solid var(--border)}
.card .thumb.wide{aspect-ratio:16/9;object-position:top}
.hgrid .card .thumb.wide{aspect-ratio:2/1}
.card .body{padding:.9rem 1rem 1rem;display:flex;flex-direction:column;gap:.5rem;flex:1}
.card h3 a{text-decoration:none}
.card h3 a::after{content:"";position:absolute;inset:0;z-index:1}
.card .title{display:flex;align-items:center;gap:.55rem}
.card .title img{width:22px;height:22px;flex:none}
.card .place{font:500 .7rem/1.3 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.card .blurb{color:var(--muted);font-size:.93rem}
.card .fact{font-size:.86rem;color:var(--text)}
.card .checked{font-size:.82rem;line-height:1.5;color:var(--muted);border-left:2px solid var(--border);padding-left:.6rem}
.card .checked b{font:500 .68rem var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--faint);display:block}
.card .more{margin-top:auto;padding-top:.4rem;display:flex;flex-wrap:wrap;gap:.25rem .9rem;font-size:.85rem;position:relative;z-index:2}
.card .more a{color:var(--accent-text);text-decoration:underline;text-decoration-color:color-mix(in srgb,var(--accent-text) 35%,transparent);text-underline-offset:3px}
.card .more a:hover{text-decoration-color:currentColor}
.track{margin-top:2.25rem}
section.strip{padding-top:2rem}
@media (min-width:860px){.grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}}
.card.mini .body{padding:1rem 1.1rem 1.1rem}
.card h2.h3{font-size:1.1rem;font-weight:600;letter-spacing:-.015em}
.card h2 a{text-decoration:none}
.card h2 a::after{content:"";position:absolute;inset:0;z-index:1}
.pill{display:inline-block;margin-left:.4rem;padding:.05rem .45rem;border-radius:999px;border:1px solid var(--border);background:var(--accent-soft);color:var(--accent-text);letter-spacing:.06em}
@media (min-width:760px){.grid.two{grid-template-columns:repeat(2,minmax(0,1fr))}}
.hgrid{display:grid;gap:1rem;grid-template-columns:minmax(0,1fr)}
@media (min-width:980px){.hgrid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:560px){.card.h{display:grid;grid-template-columns:minmax(0,38%) minmax(0,1fr)}
 .card.h .thumb{height:100%;aspect-ratio:auto;min-height:11rem;border-bottom:0;border-right:1px solid var(--border)}}
.textlink{display:inline-flex;align-items:center;min-height:44px;color:var(--accent-text);font-size:.92rem;font-weight:550}
.track-head{display:flex;align-items:center;gap:.65rem;margin-bottom:.9rem}
.track-head svg{width:22px;height:22px;flex:none}
.track-head p{color:var(--muted);font-size:.95rem}
.checks4{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,15rem),1fr))}
.stat{border:1px solid var(--border);border-radius:.6rem;padding:1rem;background:var(--raised);display:flex;flex-direction:column;gap:.35rem}
.stat .n{font-size:1.65rem;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.stat .k{font:500 .7rem var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.stat p{font-size:.88rem;color:var(--muted)}
.stat a{font-size:.85rem;color:var(--accent-text);margin-top:auto}
.list{border-top:1px solid var(--border)}
.row{display:grid;grid-template-columns:minmax(0,12rem) minmax(0,1fr) auto;gap:.4rem 1.25rem;padding:.9rem 0;border-bottom:1px solid var(--border);align-items:baseline}
.row h3 a{text-decoration:none}
.row h3 a:hover{text-decoration:underline}
.row p{color:var(--muted);font-size:.93rem}
.row .count{font:500 .85rem var(--mono);color:var(--text);white-space:nowrap;text-align:right}
@media (max-width:700px){.row{grid-template-columns:minmax(0,1fr) auto}.row p{grid-column:1/-1;grid-row:2}}
.note{font-size:.82rem;color:var(--faint);margin-top:.75rem}
.built{border:1px solid var(--border);border-radius:.6rem;padding:1.25rem 1.25rem;background:var(--surface);max-width:48rem}
.built p+p{margin-top:.75rem}
.built p{color:var(--muted)}
code{font:.88em var(--mono);background:var(--surface);border:1px solid var(--border);border-radius:.25rem;padding:.05rem .3rem;overflow-wrap:anywhere}
footer.site{margin-top:4.5rem;border-top:1px solid var(--border);padding:1.5rem 0 2.5rem;font-size:.85rem;color:var(--faint)}
footer.site .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:.5rem 1.5rem}
footer.site a{color:var(--muted)}
.prose{max-width:46rem}
.prose p{color:var(--muted);margin-top:.9rem}
.big4{display:grid;gap:1.25rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,30rem),1fr));margin-top:1.25rem}
.check{border:1px solid var(--border);border-radius:.6rem;background:var(--raised);padding:1.1rem 1.15rem;display:flex;flex-direction:column;gap:.6rem}
.check svg{width:100%;height:auto}
.check svg.dv{display:none;max-width:19rem;margin:0 auto}
@media (max-width:600px){.check svg.dh{display:none}.check svg.dv{display:block}}
.check blockquote{margin:0;border-left:2px solid var(--accent-line);padding-left:.75rem;color:var(--text);font-size:.93rem}
.check .src{font-size:.82rem;color:var(--faint)}
.check .src a{color:var(--accent-text)}
.check .k{font:500 .7rem var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.tbl{width:100%;border-collapse:collapse;font-size:.9rem}
.tbl th,.tbl td{text-align:left;vertical-align:top;padding:.7rem .6rem;border-bottom:1px solid var(--border)}
.tbl th{font:500 .72rem var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--faint)}
.tbl td:first-child{white-space:nowrap}
.tbl td a{color:var(--accent-text)}
.tbl .site{display:flex;align-items:center;gap:.5rem;font-weight:550}
.tbl .site img{width:18px;height:18px}
@media (max-width:700px){.tbl thead{display:none}.tbl tr{display:block;padding:.7rem 0;border-bottom:1px solid var(--border)}
 .tbl td{display:block;border:0;padding:.15rem 0}.tbl td:first-child{white-space:normal}}
.qt{border-collapse:collapse;font-size:.82rem;margin:.4rem 0;width:100%}
.qt th,.qt td{border:1px solid var(--border);padding:.3rem .45rem;text-align:left;vertical-align:top}
.qt th{font:500 .68rem var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--faint);background:var(--surface)}
.miss{border:1px solid var(--border);border-radius:.6rem;padding:1rem 1.15rem;background:var(--raised)}
.miss ul{margin:.5rem 0 0;padding-left:1.1rem;color:var(--muted)}
.miss li{margin:.45rem 0}
.miss li a{color:var(--accent-text)}
svg text{font-family:var(--mono)}
@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""

TRACK_SHAPE = {
    # the companion sites' favicon shapes, one per track
    "foundations": '<circle cx="16" cy="16" r="15" fill="currentColor"/>',
    "hardware": '<rect x="3.5" y="3.5" width="25" height="25" rx="2.5" fill="currentColor"/><path d="M9 0h3v4h-3zM20 0h3v4h-3zM9 28h3v4h-3zM20 28h3v4h-3zM0 9h4v3h-4zM0 20h4v3h-4zM28 9h4v3h-4zM28 20h4v3h-4z" fill="currentColor"/>',
    "inference": '<path d="M16 0.5 29.5 8.25v15.5L16 31.5 2.5 23.75V8.25z" fill="currentColor"/>',
    "agents": '<rect x="0.5" y="1" width="31" height="24" rx="6" fill="currentColor"/><path d="M6 23v8.5l8.5-8.5z" fill="currentColor"/>',
}


def head(title, description, path, extra=""):
    url = BASE + path
    canonical = (f'<link rel="canonical" href="{url}">' if path != "/404.html"
                 else '<meta name="robots" content="noindex">')
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
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0a0a0a" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url if path != "/404.html" else BASE + "/"}">
<meta property="og:image" content="{BASE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME}: hardware and agentic AI. Sixteen interactive sites, each checked against a reference.">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{BASE}/og.png">
<style>{CSS.strip()}</style>
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
<a class="brand" href="/"><img src="/favicon.svg" alt="" width="24" height="24">{NAME}</a>
<nav class="top" aria-label="Main">
<a href="/#hardware" class="wide">Hardware</a>
<a href="/#sites">Sites</a>
<a href="/checks/" class="mid">Checks</a>
<a href="/cv/">CV</a>
<a href="{GH}">GitHub</a>
</nav>
</div></header>
"""


def foot():
    return f"""<footer class="site"><div class="wrap">
<span>{NAME} · <a href="{GH}">GitHub</a> · <a href="/checks/">How I check the numbers</a></span>
<span>A static page, built {BUILT} from its <a href="{GH}/BrendanJamesLynskey.github.io">source</a>.</span>
</div></footer>
</body>
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
    return f"The Hardware index lists {COUNTS['Hardware']['projects']} projects."


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
        return f"{c['subhubs']} sub-hubs · {c['decks']} decks"
    if key == "Signal_Integrity":
        return f"{c['decks']} decks · {c['slides']} slides"
    if key == "DSP_and_Music":
        return f"{c['projects']} projects · {c['areas']} areas"
    return f"{c['projects']} projects"


def index_row(x):
    return f"""<div class="row">
<h3><a href="{e(x["href"])}">{e(x["title"])}</a></h3>
<p>{e(x["text"])}</p>
<span class="count">{e(index_count(x["key"]))}</span>
</div>"""


def strip():
    """CV · Digital Twin · Contact: three cards near the top of the home page."""
    t = DIGITAL_TWIN
    if t["url"]:
        twin_href, status, more = t["url"], "", f'<a href="{e(t["url"])}">Talk to it →</a>'
    else:
        twin_href = t["interim_url"]
        status = '<span class="pill">New version coming soon</span>'
        more = f'<a href="{e(t["interim_url"])}">Try the earlier version →</a>'
    return f"""<section class="block strip" id="cv-twin" aria-label="CV, Digital Twin and contact"><div class="wrap">
<div class="grid three">
<article class="card mini">
<div class="body">
<p class="place">CV</p>
<h2 class="h3"><a href="/cv/">Experience and education</a></h2>
<p class="blurb">{e(CV["headline"])}</p>
<p class="more"><a href="/cv/">Read the CV →</a><a href="{PDF}">Download the PDF</a></p>
</div>
</article>
<article class="card mini">
<div class="body">
<p class="place">{e(t["label"])} {status}</p>
<h2 class="h3"><a href="{e(twin_href)}">Ask about my career</a></h2>
<p class="blurb">{e(t["text"])}</p>
<p class="more">{more}</p>
</div>
</article>
<article class="card mini">
<div class="body">
<p class="place">Contact</p>
<h2 class="h3"><a href="{e(CV["linkedin"])}">LinkedIn</a></h2>
<p class="blurb">The best way to reach me is a message on LinkedIn.</p>
<p class="more"><a href="{e(CV["linkedin"])}">Message me on LinkedIn →</a></p>
</div>
</article>
</div>
</div></section>"""


def home():
    groups = DATA["groups"]
    n_sites = sum(len(sites_in(g["key"])) for g in groups)
    assert n_sites == 16, n_sites
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
    llms = COUNTS["LLMs"]
    desc = ("Brendan Lynskey: a staff-level engineer across hardware (RTL and FPGA, DSP, signal integrity) "
            "and agentic AI. Sixteen interactive explainer sites, deck series from signal integrity to agents, "
            "and how every number is checked.")
    return head(f"{NAME}: hardware and agentic AI", desc, "/") + f"""<main id="main">
<section class="hero"><div class="wrap">
<div class="hero-grid">
<div class="intro">
<p class="eyebrow">Portfolio</p>
<h1>{NAME}</h1>
<p class="lede">A staff-level engineer across hardware (RTL and FPGA, DSP, signal integrity) and agentic AI.</p>
</div>
<figure class="hero-fig">
<canvas id="hero-canvas" width="560" height="300" role="img" aria-label="Animation: an agent loop sends operands into a four-by-four systolic array; the operands move one cell per cycle and each cell fills as it accumulates; the results drain back to the loop, which checks them against a reference before planning the next step."></canvas>
<figcaption>Illustration: an agent loop drives a 4×4 output-stationary systolic array and checks every result against a reference.</figcaption>
<button type="button" id="hero-pause">Pause</button>
</figure>
<div class="rest">
<p class="sub">More than 25 years in hardware, and I write the software too. Here are sixteen interactive explainer sites in four tracks, deck series from signal integrity to agents, and the simulators and RTL behind them. Every number comes from tested code or a cited, dated source, and every model is checked against something independent of it.</p>
<div class="btns">
<a class="btn primary" href="#sites">Explore the sites ↓</a>
<a class="btn" href="/checks/">How I check the numbers →</a>
<a class="textlink" href="#hardware">Hardware, DSP and SI ↓</a>
</div>
</div>
</div>
<p class="facts"><span><b>16</b> interactive sites</span><span><b>4</b> tracks</span><span><b>{llms['subhubs']}</b> LLM sub-hubs, <b>{llms['decks']}</b> decks</span><span><b>{COUNTS['Signal_Integrity']['decks']}</b> signal-integrity decks</span><span>Every number tested or sourced</span></p>
</div></section>

{strip()}

<section class="block" id="hardware" aria-labelledby="hardware-h"><div class="wrap">
<div class="block-head"><div><p class="eyebrow">Home ground</p><h2 id="hardware-h">Hardware, DSP and signal integrity</h2></div>
<p>Where most of my career has been: channels and equalisers, RTL and its verification, accelerator simulators and the DSP behind audio. Each card links a series hub; the hubs link the decks.</p></div>
<div class="hgrid">
{"".join(hw_card(h) for h in HARDWARE)}
</div>
</div></section>

<section class="block" id="sites" aria-labelledby="sites-h"><div class="wrap">
<div class="block-head"><div><p class="eyebrow">Interactive sites</p><h2 id="sites-h">Sixteen sites, four tracks</h2></div>
<p>Each site is a computed, animated reading experience: the animations are drawn from a tested model, not hand-made. Every site's header has a menu to all the others, and every repository ships its models, fixtures and CI.</p></div>
{"".join(tracks)}
</div></section>

<section class="block" id="showcases" aria-labelledby="showcases-h"><div class="wrap">
<div class="block-head"><div><p class="eyebrow">Showcases</p><h2 id="showcases-h">Agents for hardware, and things that make sound or move</h2></div></div>
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
<script src="/assets/hero.js" defer></script>
""" + foot()


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
""" + foot()


def not_found():
    return head("Page not found · " + NAME, "This page does not exist. The portfolio home lists everything.", "/404.html") + """<main id="main"><div class="wrap">
<section class="hero">
<p class="eyebrow">404</p>
<h1>Page not found</h1>
<p class="lede">There is nothing at this address.</p>
<div class="btns"><a class="btn primary" href="/">Portfolio home</a><a class="btn" href="/#sites">The interactive sites</a><a class="btn" href="/checks/">How I check the numbers</a></div>
</section>
</div></main>
""" + foot()


# ---------------------------------------------------------------- the CV page

CV_CSS = r"""
:root{--d-hardware:#0369a1;--d-fpga:#6d28d9;--d-dsp:#c2410c;--d-ai:#047857;--d-fg:#ffffff;--d-edu:#8a8a8a}
@media (prefers-color-scheme:dark){:root{--d-hardware:#38bdf8;--d-fpga:#a78bfa;--d-dsp:#fb923c;--d-ai:#34d399;--d-fg:#0a0a0a;--d-edu:#737373}}
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
 :root{color-scheme:light;--bg:#fff;--surface:#f5f5f5;--raised:#fff;--border:#d4d4d4;--text:#111;--muted:#333;--faint:#555;
  --accent:#4338ca;--accent-text:#3730a3;--accent-line:#4f46e5;--accent-soft:#eef2ff;
  --d-hardware:#0369a1;--d-fpga:#6d28d9;--d-dsp:#c2410c;--d-ai:#047857;--d-fg:#fff;--d-edu:#8a8a8a}
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


def now_year():
    y, m, d = (int(x) for x in BUILT.split("-"))
    return y + (m - 1 + d / 31) / 12


def dates(r):
    return f"{r['start']} – {r['end']}"


def short(company):
    c = company.split(" (")[0].split(" /")[0]
    return c.split()[0] if len(c) > 14 else c


def role_label(r):
    doms = " and ".join(DOMAIN_LABEL[d] for d in r["domains"])
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
        rects = "".join(f'<rect x="{a:.1f}" y="{i * 40 / n:.1f}" width="{b - a:.1f}" height="{40 / n:.1f}" fill="{DOMAIN_VAR[d]}"{sep}/>'
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
        if g:
            names.append(f'<span style="left:{a / 10 + .15:.2f}%;width:{(b - a) / 10 - .3:.2f}%">{e(ed["school"].split()[-1])}</span>')
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
    legend = "".join(f'<li><span class="sw" style="background:{DOMAIN_VAR[d]}"></span>{e(lbl)}</li>'
                     for d, lbl in DOMAIN_LABEL.items())
    legend += '<li><span class="sw edu" style="background:var(--d-edu)"></span>Study</li>'
    return css, f"""<figure class="tl" aria-labelledby="tl-cap">
<p id="tl-cap" class="sr">Career timeline from 1994 to now: one band per role, coloured by domain, with study below. The same information is in the list under “The timeline as text” and in Experience.</p>
<div class="tl-strip">
<svg class="tl-svg" viewBox="0 0 1000 60" preserveAspectRatio="none" role="group" aria-label="Career timeline, 1994 to now">
{"".join(bands)}
</svg>
<div class="tl-names" aria-hidden="true">{"".join(names)}</div>
</div>
<div class="tl-axis" aria-hidden="true">{"".join(axis)}</div>
<div class="tl-out" aria-hidden="true"><p class="tl-hint">Hover over a band, or tab to it, to see the role. Each band links to its entry below.</p>{"".join(outs)}</div>
<ul class="legend" aria-label="Key">{legend}</ul>
<details class="tl-text"><summary>The timeline as text</summary><ol>{"".join(alt)}</ol></details>
</figure>"""


def role_html(r):
    doms = "".join(f'<span class="dom"><span class="sw" style="background:{DOMAIN_VAR[d]}"></span>{e(DOMAIN_LABEL[d])}</span>'
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
            + link("Portfolio", BASE + "/") + f'<li class="no-print"><a href="{e(twin)}">{e(twin_label)}</a></li>')
    edu = "".join(f'<li><span class="yrs">{e(x["years"])}</span><span><b>{e(x["degree"])}</b>, '
                  f'<span class="sch">{e(x["school"])}{" (part-time)" if x["part_time"] else ""}</span></span></li>'
                  for x in CV["education"])
    certs = "".join(f"<li>{e(c)}</li>" for c in CV["certs"])
    desc = f"{CV['name']}: CV. {CV['headline']}"
    return head(f"{NAME}: CV", desc, "/cv/", f"<style>{CV_CSS.strip()}\n{css}</style>\n") + f"""<main id="main"><div class="wrap">
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
<div class="work">
{selected_work()}
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
""" + foot()


SR_CSS = ".sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}"


def main():
    global CSS
    CSS = CSS + SR_CSS
    pages = {"index.html": home(), "checks/index.html": checks_page(), "cv/index.html": cv_page(),
             "404.html": not_found()}
    for p, s in pages.items():
        os.makedirs(os.path.dirname(os.path.join(ROOT, p)) or ROOT, exist_ok=True)
        open(os.path.join(ROOT, p), "w").write(s)
        print("wrote", p, len(s))
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    urls = "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{BUILT}</lastmod></url>\n" for u in ["/", "/cv/", "/checks/"])
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + urls + "</urlset>\n")


if __name__ == "__main__":
    main()
