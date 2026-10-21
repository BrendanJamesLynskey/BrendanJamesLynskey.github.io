"""Collect the facts the home page shows, from their live sources, into data/.

    python3 tools/gather.py

Nothing on the page is typed in by hand where a source exists:
- each companion site's name, track and one-line blurb come from the shared site switch
  (SiteSwitch.tsx, byte-identical on every site), read from GitHub;
- each site's "How this is checked" line, the link to its evidence, its favicon and its
  link-preview card come from the live landing page;
- the deck counts come from the index READMEs on GitHub (see count_readme below); a series is one hub page that
  lists its decks (count_llms, count_series).

Writes data/sites.json and data/counts.json, assets/icons/<key>.svg and assets/cards/<key>.webp.
Needs network access and Pillow (with WebP).
"""
import html
import io
import json
import os
import re
import sys
import urllib.request

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNER = "BrendanJamesLynskey"
RAW = f"https://raw.githubusercontent.com/{OWNER}"
UA = {"User-Agent": "Mozilla/5.0 (portfolio-home gather)"}

# key in the switch -> (repo, live landing path); the order is the switch's order
EXTRA = {
    # not in the switch's four tracks, but shown as showcases
    "dse": dict(label="HW Design-Space Agent", repo="hw-design-space-agent",
                href="https://hw-design-space-agent.vercel.app"),
}
REPOS = {
    "decoder": "transformer-explainer", "training": "transformer-explainer",
    "kernels": "gpu-kernels-explained", "silicon": "systolic-arrays-explained",
    "accelerators": "ai-accelerators-explained", "racks": "ai-racks-explained",
    "inference": "llm-inference-explained", "architectures": "llm-architectures-explained",
    "numerics": "numerics-explained", "tradeoffs": "inference-tradeoffs-explained",
    "harnesses": "agent-harnesses-explained", "protocols": "agent-protocols-explained",
    "context": "agent-context-explained", "orchestration": "agent-orchestration-explained",
    "evals": "agent-evals-explained", "security": "agent-security-explained",
    "transit": "compute-in-transit-results", "dse": "hw-design-space-agent",
}


def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")


def text_of(fragment):
    t = re.sub(r"<!--.*?-->", "", fragment, flags=re.S)
    t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def parse_switch(src):
    """The SITES and GROUPS arrays of SiteSwitch.tsx, as dicts (string fields only)."""
    def objects(block):
        out = []
        for body in re.findall(r"\{(.*?)\}", block, flags=re.S):
            o = {}
            for k, v in re.findall(r'(\w+):\s*"((?:[^"\\]|\\.)*)"', body):
                o[k] = v
            for k, v in re.findall(r"(\w+):\s*(true|false)", body):
                o[k] = v == "true"
            if o:
                out.append(o)
        return out
    sites = objects(src[src.index("const SITES = ["):src.index("] as const;")])
    g0 = src.index("const GROUPS = [")
    groups = objects(src[g0:src.index("] as const;", g0)])
    return sites, groups


def landing(key, href):
    url = href + ("/training" if key == "training" else "/")
    page = get(url)
    m = re.search(r"<p[^>]*data-checked-strip[^>]*>(.*?)</p>", page, flags=re.S)
    assert m, f"no checked strip on {url}"
    inner = m.group(1)
    tag = re.search(r"<a[^>]*data-checked-link[^>]*>", inner)
    assert tag, f"no evidence link on {url}"
    link = re.search(r'href="([^"]+)"', tag.group(0))
    claim = text_of(inner)
    claim = re.sub(r"^How this is checked\s*", "", claim)
    claim = re.sub(r"\s*How it is tested →$", "", claim)
    evidence = link.group(1)
    if evidence.startswith("/"):
        evidence = href + evidence
    og = re.search(r'property="og:image" content="([^"]+)"', page)
    icon = re.search(r'<link rel="icon" href="([^"]+)"', page)
    return dict(landing=url, claim=claim, evidence=evidence,
                og=html.unescape(og.group(1)) if og else None,
                icon=href + icon.group(1).split("?")[0] if icon else None)


def save_assets(key, info):
    if info["icon"]:
        svg = get(info["icon"])
        assert svg.lstrip().startswith("<svg"), info["icon"]
        open(os.path.join(ROOT, "assets", "icons", f"{key}.svg"), "w").write(svg)
    if info["og"]:
        im = Image.open(io.BytesIO(get(info["og"], binary=True))).convert("RGB")
        im = im.resize((600, 315), Image.LANCZOS)
        im.save(os.path.join(ROOT, "assets", "cards", f"{key}.webp"), "WEBP", quality=78, method=6)


def count_readme(repo):
    """Projects listed in an index README: table rows whose first cell starts with a link."""
    md = get(f"{RAW}/{repo}/main/README.md")
    rows = [ln for ln in md.splitlines() if re.match(r"^\|\s*\**\[", ln)]
    return md, len(rows)


def count_llms(md):
    """The LLMs index: its series and their decks, from the Sub-hub index table. A series is one hub page that
    lists its decks; a row counts when its Status cell states "N decks" (the interactive sites, and the single
    Cloud *aaS deck linked here, have no such count and are not series)."""
    sub = md[md.index("## Sub-hub index"):md.index("## Articles")]
    series, decks = 0, 0
    for ln in sub.splitlines():
        if not re.match(r"^\|\s*\[", ln):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        m = re.search(r"(\d+) decks?", cells[1])
        if m:
            series += 1
            decks += int(m.group(1))
    return series, decks


SERIES_LINK = re.compile(r"\]\((?:https://brendanjameslynskey\.github\.io/([A-Za-z0-9_.-]+)/[^)]*|"
                         r"https://github\.com/BrendanJamesLynskey/([A-Za-z0-9_.-]+)[^)]*|([^)]+))\)")


def count_series(md, repo):
    """The series an index's "Series in this index" block lists (one per table row, or each link of a bulleted
    list; an "Also linked" bullet is not a series of that index). Returns the set of series keys, so the
    library total counts a series listed by two indexes once."""
    lines = md.splitlines()
    i = next(k for k, l in enumerate(lines) if re.match(r"#+ *Series in this index", l))
    found, started = [], False
    for l in lines[i + 1:]:
        if l.startswith("#") or l.startswith("---"):
            break
        if l.startswith("|") or l.startswith("- "):
            started = True
            if l.startswith("- **Also linked:**") or re.match(r"^\|[\s:|-]+\|?$", l):
                continue
            for a, b, c in SERIES_LINK.findall(l):
                found.append(a or b or f"{repo}:{c}")
                if l.startswith("|"):
                    break
        elif started and l.strip():
            break
    return set(found)


def count_si(md):
    """The Signal Integrity README: its deck rows (| NN | [title](url) | slides | ...), and its
    "Verified" table: the cross-checks against published results (internal checks left out)."""
    decks = [ln for ln in md.splitlines() if re.match(r"^\|\s*\d\d\s*\|\s*\[", ln)]
    slides = sum(int(ln.strip("|").split("|")[2]) for ln in decks)
    ver = md[md.index("## Verified"):]
    ext, worst = 0, 0.0
    sources = []
    for ln in ver.splitlines()[1:]:
        if ln.startswith("## "):
            break
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) != 5 or not re.match(r"^[+-]?\d", cells[3]) or cells[4].startswith("internal"):
            continue
        ext += 1
        worst = max(worst, abs(float(cells[3].replace("%", "").strip())))
        name = cells[4].split(",")[0].split(" sec")[0].strip()
        if name not in sources:
            sources.append(name)
    return dict(decks=len(decks), slides=slides, published_checks=ext, worst_pct=worst, sources=sources)


def main():
    src = get(f"{RAW}/agent-security-explained/main/src/components/ui/SiteSwitch.tsx")
    switch_sites, groups = parse_switch(src)
    sites = []
    for s in switch_sites:
        key = s["key"]
        s = dict(s, repo=REPOS[key])
        s["name"] = s["title"].split(":")[0]
        s.update(landing(key, s["href"]))
        save_assets(key, s)
        sites.append(s)
        print("site", key, "|", s["claim"][:70])
    for key, s in EXTRA.items():
        s = dict(s, key=key, group="none", unlisted=True, name=s["label"])
        s.update(landing(key, s["href"]))
        save_assets(key, s)
        sites.append(s)
        print("site", key, "|", s["claim"][:70])
    json.dump(dict(groups=groups, sites=sites), open(os.path.join(ROOT, "data", "sites.json"), "w"),
              indent=1, ensure_ascii=False)

    counts = {}
    llms_md, _ = count_readme("LLMs")
    n_series, decks = count_llms(llms_md)
    counts["LLMs"] = dict(series=n_series, decks=decks)
    library = set(count_series(llms_md, "LLMs"))
    assert len(library) == n_series, (len(library), n_series)  # the Series block and the Sub-hub index agree
    for repo in ["Hardware", "Software", "Mathematics", "Miscellaneous"]:
        ser = count_series(count_readme(repo)[0], repo)
        library |= ser
        counts[repo] = dict(series=len(ser))
    counts["Signal_Integrity"] = count_si(count_readme("Signal_Integrity")[0])
    # DSP_and_Music lists its projects in one page per area
    dsp_md, _ = count_readme("DSP_and_Music")
    dsp_series = count_series(dsp_md, "DSP_and_Music")
    library |= dsp_series
    areas = re.findall(r"\]\((\w+\.md)\)", dsp_md)
    n = 0
    for a in dict.fromkeys(areas):
        page = get(f"{RAW}/DSP_and_Music/main/{a}")
        n += len([ln for ln in page.splitlines() if re.match(r"^\|\s*\**\[", ln)])
    counts["DSP_and_Music"] = dict(areas=len(dict.fromkeys(areas)), projects=n, series=len(dsp_series))
    counts["library"] = dict(series=len(library))  # a series is one hub page that lists its decks
    json.dump(counts, open(os.path.join(ROOT, "data", "counts.json"), "w"), indent=1)
    print(json.dumps(counts))


if __name__ == "__main__":
    sys.exit(main())
