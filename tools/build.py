"""Build the static site from data/ and tools/content.py.

    python3 tools/gather.py      # refresh data/ and the site icons and cards from their live sources
    python3 tools/build.py       # write index.html, checks/index.html, 404.html, sitemap.xml, robots.txt

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
from content import HARDWARE, INDEXES, QUOTES, SHOWCASES, GH  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://brendanjameslynskey.github.io"
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
<a href="/checks/">Checks</a>
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
<p class="sub">More than 25 years in hardware, and I write the software too. Here are sixteen interactive explainer sites in four tracks, deck series from signal integrity to agents, and the simulators and RTL behind them. Every number comes from tested code that is checked against a reference.</p>
<div class="btns">
<a class="btn primary" href="#sites">Explore the sites ↓</a>
<a class="btn" href="/checks/">How I check the numbers →</a>
<a class="textlink" href="#hardware">Hardware, DSP and SI ↓</a>
</div>
</div>
</div>
<p class="facts"><span><b>16</b> interactive sites</span><span><b>4</b> tracks</span><span><b>{llms['subhubs']}</b> LLM sub-hubs, <b>{llms['decks']}</b> decks</span><span><b>{COUNTS['Signal_Integrity']['decks']}</b> signal-integrity decks</span><span>Every number from a recorded run</span></p>
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
    for qid, who in [("acc_band", "AI Accelerators Explained"), ("acc_mlperf", "AI Accelerators Explained"),
                     ("acc_miss", "AI Accelerators Explained"), ("racks_band", "AI Racks Explained"),
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
<p class="lede">Every number on the sites comes from tested code, and every model is checked against something independent of it: RTL, a real framework, an official SDK, PyTorch or a published figure.</p>
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


SR_CSS = ".sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}"


def main():
    global CSS
    CSS = CSS + SR_CSS
    pages = {"index.html": home(), "checks/index.html": checks_page(), "404.html": not_found()}
    for p, s in pages.items():
        os.makedirs(os.path.dirname(os.path.join(ROOT, p)) or ROOT, exist_ok=True)
        open(os.path.join(ROOT, p), "w").write(s)
        print("wrote", p, len(s))
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    urls = "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{BUILT}</lastmod></url>\n" for u in ["/", "/checks/"])
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + urls + "</urlset>\n")


if __name__ == "__main__":
    main()
