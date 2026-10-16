"""The home page's favicon and link-preview card, in the companion sites' family style.

    python3 tools/brand.py                    # writes favicon.svg and tools/out/{og,apple}.html
    node tools/render_brand.js                # renders og.png (1200x630) and apple-touch-icon.png (180)

The sites' favicons are one shape per track with a letter; the home page's is a rounded square (the
shape no track uses) with a "B" and a stripe in the four track colours. The letter is a Noto Sans Bold
outline, so the icon needs no font. The card uses the same fonts as the sites' cards (Noto Sans).
"""
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


def grid_svg():
    """A still of the hero: the array mid-wavefront, the loop with its check."""
    cells = []
    for i in range(5):
        for j in range(5):
            k = 5 - i - j  # filled fraction along the anti-diagonal wavefront
            fill = "#38bdf8" if k > 1 else ("#1d4e6b" if k == 1 else "#16213a")
            ring = ' stroke="#fb923c" stroke-width="3"' if k == 1 else ' stroke="#2b3a55" stroke-width="1.5"'
            cells.append(f'<rect x="{j * 62}" y="{60 + i * 62}" width="52" height="52" rx="8" fill="{fill}"{ring}/>')
    a_in = "".join(f'<rect x="-34" y="{80 + i * 62}" width="22" height="12" rx="4" fill="#0284c7"/>' for i in range(5))
    b_in = "".join(f'<rect x="{18 + j * 62}" y="18" width="16" height="22" rx="4" fill="#ea580c"/>' for j in range(5))
    loop = ('<circle cx="430" cy="215" r="88" fill="none" stroke="#334155" stroke-width="3"/>'
            '<circle cx="342" cy="215" r="11" fill="#0b1220" stroke="#818cf8" stroke-width="3"/>'
            '<circle cx="430" cy="127" r="11" fill="#0b1220" stroke="#334155" stroke-width="3"/>'
            '<circle cx="430" cy="303" r="11" fill="#0b1220" stroke="#334155" stroke-width="3"/>'
            '<circle cx="518" cy="215" r="13" fill="#4ade80"/>'
            '<path d="M511 215l5 5 9-11" stroke="#0b1220" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
            '<text x="430" y="221" text-anchor="middle" font-size="20" fill="#94a3b8" font-family="Noto Sans Mono">agent loop</text>'
            '<text x="518" y="252" text-anchor="middle" font-size="17" fill="#4ade80" font-family="Noto Sans Mono">check</text>'
            '<text x="342" y="252" text-anchor="middle" font-size="17" fill="#94a3b8" font-family="Noto Sans Mono">act</text>'
            '<text x="430" y="104" text-anchor="middle" font-size="17" fill="#94a3b8" font-family="Noto Sans Mono">plan</text>'
            '<text x="430" y="342" text-anchor="middle" font-size="17" fill="#94a3b8" font-family="Noto Sans Mono">observe</text>')
    return f'<svg viewBox="-40 0 600 380" width="470" height="298">{a_in}{b_in}{"".join(cells)}{loop}</svg>'


def og_html():
    font = lambda name, w: (f"@font-face{{font-family:'NS';src:url('file://{FONT_DIR}/NotoSans-{name}.ttf');font-weight:{w}}}")
    stripe = "".join(f'<i style="background:{c}"></i>' for c in TRACKS)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{font("Regular", 400)}{font("Bold", 700)}
@font-face{{font-family:'NSM';src:url('file://{FONT_DIR}/NotoSansMono-Bold.ttf');font-weight:700}}
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
body{{background:radial-gradient(ellipse at 78% 40%,#13284a 0%,#0b1220 55%,#070b14 100%);color:#f1f5f9;font-family:'NS';position:relative}}
.k{{position:absolute;left:72px;top:70px;font:700 26px 'NSM';letter-spacing:.12em;color:#c7d2fe;display:flex;align-items:center;gap:18px}}
.k img{{width:44px;height:44px}}
h1{{position:absolute;left:72px;top:140px;margin:0;font-size:80px;line-height:1.02;font-weight:700;letter-spacing:-1px;width:600px}}
.l{{position:absolute;left:72px;top:330px;width:560px;font-size:31px;line-height:1.35;color:#cbd5e1}}
.c{{position:absolute;left:72px;top:474px;width:540px;border-left:5px solid #4f46e5;padding-left:22px}}
.c b{{display:block;font:700 20px 'NSM';letter-spacing:.14em;color:#94a3b8;margin-bottom:6px}}
.c span{{font-size:25px;line-height:1.35;color:#e2e8f0}}
.g{{position:absolute;right:60px;top:110px}}
.u{{position:absolute;right:72px;bottom:44px;font-size:25px;color:#cbd5e1}}
.s{{position:absolute;left:0;right:0;bottom:0;height:10px;display:flex}}.s i{{flex:1}}
</style></head><body>
<div class="k"><img src="file://{ROOT}/favicon.svg">PORTFOLIO</div>
<h1>Brendan Lynskey</h1>
<p class="l">Hardware (RTL and FPGA, DSP, signal integrity) and agentic AI</p>
<div class="c"><b>HOW THIS IS CHECKED</b><span>Sixteen interactive sites, every model checked against a reference</span></div>
<div class="g">{grid_svg()}</div>
<div class="u">brendanjameslynskey.github.io</div>
<div class="s">{stripe}</div>
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
