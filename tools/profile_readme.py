"""Write the GitHub profile README (the BrendanJamesLynskey/BrendanJamesLynskey repo) from the same data
as the home page, so the two never disagree.

    python3 tools/profile_readme.py ../BrendanJamesLynskey/README.md

No stats widgets and no images from third-party servers: plain Markdown.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = "https://brendan-lynskey.vercel.app"  # the portfolio home, CV and Digital Twin card
PG = "https://brendanjameslynskey.github.io"  # GitHub Pages: the deck hubs live here, one repo each
GH = "https://github.com/BrendanJamesLynskey"
DATA = json.load(open(os.path.join(ROOT, "data", "sites.json")))
COUNTS = json.load(open(os.path.join(ROOT, "data", "counts.json")))
SITES = {s["key"]: s for s in DATA["sites"]}


def main(out):
    si, llms = COUNTS["Signal_Integrity"], COUNTS["LLMs"]
    tracks = []
    for g in DATA["groups"]:
        links = " · ".join(f'[{s["label"]}]({s["landing"]})' for s in DATA["sites"] if s.get("group") == g["key"])
        tracks.append(f'| **{g["label"]}**: {g["blurb"].lower()} | {links} |')
    featured = [
        (f'[Systolic Arrays Explained]({SITES["silicon"]["landing"]})', "Inside a matrix engine, cycle by cycle",
         "A SystemVerilog array in Verilator: 613 values, 0 mismatches"),
        (f'[HW Design-Space Agent]({SITES["dse"]["landing"]})',
         "A LangGraph agent that explores hardware trade-offs down a fidelity ladder to synthesis",
         "Every number from a recorded run of the agent"),
        (f"[Signal Integrity]({PG}/Signal_Integrity/)",
         f'{si["decks"]} decks, {si["slides"]} slides, from transmission lines to channel operating margin',
         f'{si["published_checks"]} cross-checks against published results, largest difference {si["worst_pct"]:.2f} %'),
        (f'[Agent Orchestration Explained]({SITES["orchestration"]["landing"]})',
         "Graphs, multi-agent patterns and durability",
         "Real LangGraph 1.2.14: 39 sessions, checkpoint history equal after every one of 71 operations"),
        (f'[Transformer Decoder Explained]({SITES["decoder"]["landing"]})', "How one forward pass works, live in the browser",
         "PyTorch, operation by operation, to within 1e-5"),
        (f"[LLMs index]({PG}/LLMs/)", f'{llms["subhubs"]} sub-hubs listing {llms["decks"]} decks',
         "The deck library behind the sites"),
    ]
    rows = "\n".join(f"| {a} | {b} | {c} |" for a, b, c in featured)
    md = f"""# Brendan Lynskey

A staff-level engineer across hardware (RTL and FPGA, DSP, signal integrity) and agentic AI. More than 25 years in
hardware, and I write the software too.

**[Portfolio home →]({HOME}/)** · [CV]({HOME}/cv/) · [How I check the numbers]({HOME}/checks/) · [Hardware, DSP and signal integrity]({HOME}/#hardware)

## Sixteen interactive sites, in four tracks

Each site is computed and animated by a tested model, and each is checked against something independent of it.

| Track | Sites |
|---|---|
{chr(10).join(tracks)}

## Featured

| | What | Checked against |
|---|---|---|
{rows}

<sub>Built with Claude Code as an agentic engineering workflow: I specify the work, set the verification rules and
check the numbers; commits made this way carry a Co-Authored-By line. More on the [portfolio home]({HOME}/#built).</sub>
"""
    open(out, "w").write(md)
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "..", "BrendanJamesLynskey", "README.md"))
