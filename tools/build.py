"""Build the static site from data/ and tools/content.py.

    python3 tools/gather.py      # refresh data/ and the site icons and cards from their live sources
    python3 tools/build.py       # write index.html, sites/, library/, checks/, cv/index.html, 404.html, sitemap.xml,
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
from optalysys import SECTIONS as O_SECTIONS, SOURCES as O_SOURCES  # noqa: E402
from content import DIGITAL_TWIN, HARDWARE, INDEXES, LIBRARY, QUOTES, SHOWCASES, GH  # noqa: E402
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
.o-link{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;margin-left:.6rem;vertical-align:middle;border:1px solid var(--border);border-radius:50%;font:600 .78rem var(--sans);color:var(--faint)!important;text-decoration:none;transition:color .2s,border-color .2s}
.o-link:hover,.o-link:focus-visible{color:var(--hw2)!important;border-color:var(--hw2)}
.hero.page{padding-bottom:0}
.hero.page h1{font-size:clamp(2rem,5vw,3rem)}
.hero.page .sub{max-width:44rem}
.jump{display:flex;flex-wrap:wrap;gap:.25rem 1.1rem;margin-top:1.1rem;font:500 .85rem var(--mono)}
.jump a{display:inline-flex;align-items:center;min-height:44px;color:var(--accent-text)}
.doors{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,13.5rem),1fr))}
.door{position:relative;display:flex;flex-direction:column;gap:.4rem;padding:1.1rem 1.1rem 1rem;border:1px solid var(--border);border-radius:.6rem;background:var(--raised);text-decoration:none;color:var(--text);overflow:hidden;transition:border-color .2s,transform .2s,box-shadow .2s}
.door::before{content:"";position:absolute;inset:0 auto 0 0;width:3px;background:var(--c)}
.door::after{content:"";position:absolute;right:-2.5rem;top:-2.5rem;width:7rem;height:7rem;border-radius:50%;background:var(--c);opacity:.08;transition:opacity .2s,transform .3s}
.door:hover,.door:focus-visible{border-color:var(--c);transform:translateY(-2px);box-shadow:0 8px 24px -12px var(--c)}
.door:hover::after,.door:focus-visible::after{opacity:.16;transform:scale(1.25)}
.door svg{width:28px;height:28px;color:var(--c)}
.door .k{font:500 .68rem var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--faint);margin-top:.35rem}
.door .t{font-size:1.1rem;font-weight:600;letter-spacing:-.015em;line-height:1.3}
.door .b{font-size:.9rem;color:var(--muted)}
.door .i{display:flex;flex-wrap:wrap;align-items:center;gap:.35rem;margin-top:auto;padding-top:.5rem}
.door .i img{width:20px;height:20px}
.door .n{font:500 .78rem var(--mono);color:var(--muted);margin-left:.25rem}
#portfolio .btns{margin-top:1.25rem}
@media (min-width:1100px){.doors{grid-template-columns:repeat(5,minmax(0,1fr))}}
@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""

# the home page used to hold the whole portfolio; old links to its sections now land on /sites/
OLD_ANCHORS = """<script>if(/^#(hardware|sites|track-[a-z]+|showcases|checks|decks|built)$/.test(location.hash))location.replace("/sites/"+location.hash)</script>
"""

HOME_SHAPE = '<path d="M1 16c3-9 6-9 9 0s6 9 9 0 6-9 9 0" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/><path d="M1 27h30" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" opacity=".5"/>'

TRACK_SHAPE = {
    # the companion sites' favicon shapes, one per track
    "foundations": '<circle cx="16" cy="16" r="15" fill="currentColor"/>',
    "hardware": '<rect x="3.5" y="3.5" width="25" height="25" rx="2.5" fill="currentColor"/><path d="M9 0h3v4h-3zM20 0h3v4h-3zM9 28h3v4h-3zM20 28h3v4h-3zM0 9h4v3h-4zM0 20h4v3h-4zM28 9h4v3h-4zM28 20h4v3h-4z" fill="currentColor"/>',
    "inference": '<path d="M16 0.5 29.5 8.25v15.5L16 31.5 2.5 23.75V8.25z" fill="currentColor"/>',
    "agents": '<rect x="0.5" y="1" width="31" height="24" rx="6" fill="currentColor"/><path d="M6 23v8.5l8.5-8.5z" fill="currentColor"/>',
}


def head(title, description, path, extra="", noindex=False):
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
<a href="/sites/">Portfolio</a>
<a href="/sites/#sites" class="wide">Sites</a>
<a href="/library/" class="wide">Library</a>
<a href="/checks/" class="mid">Checks</a>
<a href="/cv/">CV</a>
<a href="{GH}">GitHub</a>
</nav>
</div></header>
"""


def foot(extra=""):
    return f"""<footer class="site"><div class="wrap">
<span>{NAME} · <a href="{GH}">GitHub</a> · <a href="/checks/">How I check the numbers</a>{extra}</span>
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
    n_sites = sum(len(sites_in(g["key"])) for g in DATA["groups"])
    assert n_sites == 16, n_sites
    llms = COUNTS["LLMs"]
    desc = ("Brendan Lynskey: a staff-level engineer across hardware (RTL and FPGA, DSP, signal integrity) "
            "and agentic AI. His CV, a chat agent about his career, and a portfolio of explainer sites and deck "
            "series built for his own learning.")
    return head(f"{NAME}: hardware and agentic AI", desc, "/", OLD_ANCHORS) + f"""<main id="main">
<section class="hero"><div class="wrap">
<div class="hero-grid">
<div class="intro">
<p class="eyebrow">Hardware and agentic AI</p>
<h1>{NAME}</h1>
<p class="lede">A staff-level engineer across hardware (RTL and FPGA, DSP, signal integrity) and agentic AI.</p>
</div>
<figure class="hero-fig">
<canvas id="hero-canvas" width="560" height="300" role="img" aria-label="Animation: an agent loop sends operands into a four-by-four systolic array; the operands move one cell per cycle and each cell fills as it accumulates; the results drain back to the loop, which checks them against a reference before planning the next step."></canvas>
<figcaption>Illustration: an agent loop drives a 4×4 output-stationary systolic array and checks every result against a reference.</figcaption>
<button type="button" id="hero-pause">Pause</button>
</figure>
<div class="rest">
<p class="sub">More than 25 years in hardware, and I write the software too. Read my CV, ask a chat agent about my career, or look through the portfolio: explainer sites, deck series and simulators I built for my own learning.</p>
<div class="btns">
<a class="btn primary" href="/cv/">Read the CV →</a>
<a class="btn" href="/sites/">Open the portfolio →</a>
</div>
</div>
</div>
<p class="facts"><span><b>25+</b> years in hardware</span><span><b>16</b> interactive sites</span><span><b>{llms['series']}</b> LLM deck series, <b>{llms['decks']}</b> decks</span><span><b>{COUNTS['Signal_Integrity']['decks']}</b> signal-integrity decks</span></p>
</div></section>

{strip()}

<section class="block" id="portfolio" aria-labelledby="portfolio-h"><div class="wrap">
<div class="block-head"><div><p class="eyebrow">Portfolio</p><h2 id="portfolio-h">Built to learn, shared as I go</h2></div>
<p><b>I built these sites and decks for my own learning, and I am still working my way through them.</b> They are where my interests are heading: the hardware I know, and the AI systems that run on it. Every number in them comes from tested code or a cited source.</p></div>
<div class="doors">
{doors()}
</div>
<div class="btns"><a class="btn primary" href="/sites/">Open the portfolio →</a><a class="btn" href="/checks/">How I check the numbers →</a></div>
</div></section>
</main>
<script src="/assets/hero.js" defer></script>
""" + foot(' <a class="o-link" href="/optalysys/" title="Optalysys-related work"><span class="sr">Optalysys-related work</span><span aria-hidden="true">O</span></a>')


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
    return head(f"Portfolio · {NAME}", desc, "/sites/") + f"""<main id="main">
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
""" + foot()


def doors():
    """The landing page's way into the portfolio: the home-ground hubs, then one tile per track."""
    tiles = [("hardware", "/sites/#hardware", "Home ground", "Hardware, DSP and signal integrity",
              f"{len(HARDWARE)} deck series", "var(--hw)", HOME_SHAPE, [])]
    for g in DATA["groups"]:
        ss = sites_in(g["key"])
        tiles.append((g["key"], f"/sites/#track-{g['key']}", "Interactive sites", g["label"], g["blurb"],
                      f"var(--t-{g['key']})", TRACK_SHAPE[g["key"]], ss))
    out = []
    for key, href, kicker, title, blurb, colour, shape, ss in tiles:
        icons = "".join(f'<img src="/assets/icons/{s["key"]}.svg" alt="" width="20" height="20">' for s in ss)
        count = f'<span class="n">{len(ss)} sites</span>' if ss else ""
        out.append(f"""<a class="door" href="{href}" style="--c:{colour}">
<svg viewBox="0 0 32 32" aria-hidden="true">{shape}</svg>
<span class="k">{e(kicker)}</span>
<span class="t">{e(title)}</span>
<span class="b">{e(blurb)}</span>
<span class="i">{icons}{count}</span>
</a>""")
    return "\n".join(out)


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
""" + foot()


# ---------------------------------------------------------------- the CV page

CV_CSS = r"""
:root{--d-hardware:#0369a1;--d-fpga:#6d28d9;--d-dsp:#c2410c;--d-crypto:#be185d;--d-sw:#a16207;--d-ai:#4d7c0f;--d-fg:#ffffff;--d-edu:#8a8a8a}
@media (prefers-color-scheme:dark){:root{--d-hardware:#38bdf8;--d-fpga:#a78bfa;--d-dsp:#fb923c;--d-crypto:#f472b6;--d-sw:#facc15;--d-ai:#4ade80;--d-fg:#0a0a0a;--d-edu:#737373}}
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
 :root{color-scheme:light;--bg:#fff;--surface:#f5f5f5;--raised:#fff;--border:#d4d4d4;--text:#111;--muted:#333;--faint:#555;
  --accent:#4338ca;--accent-text:#3730a3;--accent-line:#4f46e5;--accent-soft:#eef2ff;
  --d-hardware:#0369a1;--d-fpga:#6d28d9;--d-dsp:#c2410c;--d-crypto:#be185d;--d-sw:#a16207;--d-ai:#4d7c0f;--d-fg:#fff;--d-edu:#8a8a8a}
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
""" + foot()


# ---------------------------------------------------------------- the library page (brief 45)

LIB_CSS = (".lib{border-top:1px solid var(--border)}"
           ".lib-row{display:grid;grid-template-columns:minmax(0,13rem) minmax(0,1fr);gap:.5rem 1.5rem;padding:1.1rem 0;"
           "border-bottom:1px solid var(--border)}"
           ".lib-row h2{font-size:1.2rem;margin:0}.lib-row h2 a{text-decoration:none}.lib-row h2 a:hover{text-decoration:underline}"
           ".lib-row p{color:var(--muted);font-size:.93rem;margin-top:.3rem}"
           ".lib-row ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;align-content:flex-start;gap:.35rem .5rem}"
           ".lib-row li a{display:inline-flex;align-items:center;min-height:36px;padding:.2rem .7rem;border:1px solid var(--border);"
           "border-radius:999px;font-size:.88rem;color:var(--text);text-decoration:none;background:var(--surface,transparent)}"
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
""" + foot()


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
