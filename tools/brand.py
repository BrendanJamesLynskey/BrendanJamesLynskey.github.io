"""The home page's favicon and link-preview card, in the companion sites' family style.

    python3 tools/brand.py                    # writes favicon.svg and tools/out/{og,apple}.html
    node tools/render_brand.js                # renders og.png (1200x630) and apple-touch-icon.png (180)

The sites' favicons are one shape per track with a letter; the home page's is a rounded square (the
shape no track uses) with a "B" and a stripe in the four track colours. The letter is a Noto Sans Bold
outline, so the icon needs no font. The card is a datasheet front page, like the site: IBM Plex Sans Condensed and
IBM Plex Mono from assets/fonts/.
"""
import datetime
import os

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "tools", "out")
FONT_DIR = "/usr/share/fonts/truetype/noto"
TRACKS = ["#0891b2", "#0284c7", "#4f46e5", "#dc2626"]  # Foundations, Hardware, Inference, Agents


def letter(ch, cx, cy, cap_px):
    f = TTFont(os.path.join(FONT_DIR, "NotoSans-Bold.ttf"))
    gs = f.getGlyphSet()
    g = gs[f.getBestCmap()[ord(ch)]]
    s = cap_px / f["OS/2"].sCapHeight
    bp = BoundsPen(gs)
    g.draw(bp)
    x0, y0, x1, y1 = bp.bounds
    pen = SVGPathPen(gs, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
    g.draw(TransformPen(pen, (s, 0, 0, -s, cx - (x0 + x1) / 2 * s, cy + (y0 + y1) / 2 * s)))
    return pen.getCommands()


def favicon():
    stripe = "".join(f'<rect x="{4 + i * 6}" y="25" width="6" height="3" fill="{c}"/>' for i, c in enumerate(TRACKS))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
            '<rect x="0.5" y="0.5" width="31" height="31" rx="7" fill="#18181b" stroke="#3f3f46"/>'
            f'<path d="{letter("B", 16, 13.5, 15)}" fill="#fff"/>{stripe}</svg>\n')


def og_html():
    """The link-preview card in the site's datasheet style: the header band, the name, the pin package."""
    rev = datetime.date.today().strftime("%Y.%m")
    face = lambda fam, file, w: (f"@font-face{{font-family:'{fam}';src:url('file://{ROOT}/assets/fonts/{file}.woff2');"
                                 f"font-weight:{w}}}")
    fonts = (face("PSC", "ibm-plex-sans-condensed-latin-400-normal", 400)
             + face("PSC", "ibm-plex-sans-condensed-latin-700-normal", 700)
             + face("PM", "ibm-plex-mono-latin-400-normal", 400) + face("PM", "ibm-plex-mono-latin-600-normal", 600))
    left = ["CV", "TWIN", "SITES", "LIBRARY"]
    right = ["CHECKS", "GITHUB", "LINKEDIN", "GND"]
    pin = lambda n, t, side: (f'<div class="p s{side}{" g" if t == "GND" else ""}">'
                              + (f"{t}<i></i><em>{n}</em>" if side == "l" else f"<em>{n}</em><i></i>{t}") + "</div>")
    lp = "".join(pin(n, t, "l") for n, t in enumerate(left, 1))
    rp = "".join(pin(n, t, "r") for n, t in zip([8, 7, 6, 5], right))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{fonts}
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
body{{background:#f6f5f0;color:#111;font-family:'PSC';position:relative}}
.band{{position:absolute;left:64px;right:64px;top:40px;display:flex;justify-content:space-between;align-items:center;
 border-bottom:4px solid #111;padding-bottom:16px;font:400 22px 'PM';letter-spacing:.06em}}
.band b{{font-weight:600}}.badge{{background:#f2a33a;padding:5px 14px;font-weight:600}}
.k{{position:absolute;left:64px;top:126px;font:600 21px 'PM';letter-spacing:.1em}}
h1{{position:absolute;left:60px;top:160px;margin:0;font-size:132px;line-height:.88;font-weight:700;letter-spacing:-3px;text-transform:uppercase}}
.hl{{position:absolute;left:64px;top:410px;width:600px;margin:0;font-size:31px;line-height:1.22}}
.pkg{{position:absolute;right:64px;top:146px;height:290px;display:grid;grid-template-columns:150px 140px 150px;font:400 21px 'PM'}}
.col{{display:flex;flex-direction:column;justify-content:space-around}}
.p{{display:flex;align-items:center;gap:8px;height:56px}}.p.sl{{justify-content:flex-end}}
.p i{{width:26px;height:4px;background:#111}}.p em{{font-style:normal;font-size:16px;color:#5c5a52;width:16px;text-align:center}}
.p.g{{color:#5c5a52}}.p.g i{{background:#8a887f}}
.chip{{position:relative;background:#1b1b1b;border:4px solid #111;color:#f6f5f0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px}}
.chip:before{{content:"";position:absolute;left:14px;top:14px;width:16px;height:16px;border:3px solid #f6f5f0;border-radius:50%}}
.chip b{{font:600 26px 'PM';white-space:nowrap}}.chip span{{font-size:17px;color:#c9c9c2;font-family:'PM'}}
.foot{{position:absolute;left:64px;right:64px;bottom:36px;display:flex;justify-content:space-between;border-top:4px solid #111;
 padding-top:14px;font:400 19px 'PM';letter-spacing:.03em}}
</style></head><body>
<div class="band"><b>BL-1994 · STAFF ENGINEER</b><span>DATASHEET · REV {rev} · LEEDS, UK</span><span class="badge">ACTIVE</span></div>
<div class="k">GENERAL DESCRIPTION</div>
<h1>Brendan<br>Lynskey</h1>
<p class="hl">Hardware (RTL and FPGA, DSP, signal integrity), software and agentic AI</p>
<div class="pkg"><div class="col">{lp}</div><div class="chip"><b>BL-1994</b><span>HW · SW · AI</span></div><div class="col">{rp}</div></div>
<div class="foot"><span>16 INTERACTIVE SITES · EACH CHECKED AGAINST A REFERENCE</span><span>brendanjameslynskey.github.io</span></div>
</body></html>"""


def apple_html():
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;width:180px;height:180px;background:#18181b}}
img{{width:180px;height:180px;display:block}}</style></head><body><img src="file://{ROOT}/favicon.svg"></body></html>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(ROOT, "favicon.svg"), "w").write(favicon())
    open(os.path.join(OUT, "og.html"), "w").write(og_html())
    open(os.path.join(OUT, "apple.html"), "w").write(apple_html())
    print("wrote favicon.svg, tools/out/og.html, tools/out/apple.html")


if __name__ == "__main__":
    main()
