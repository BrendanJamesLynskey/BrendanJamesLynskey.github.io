"""The CV, parsed from src/cv_source.md (the only source of facts for /cv/).

    python3 tools/cv.py          # print the parsed structure, to eyeball it

tools/build.py renders /cv/ from CV; tools/check_cv.py checks the page against the same parse. The only
hand-written text is PROFILE (the source's eight profile bullets cut to four sentences; the PR lists it for the
owner to check) and DOMAINS (which colour each role takes on the timeline, a layout choice, not a fact).
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "src", "cv_source.md")

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]

# the source's Profile section, shortened; every clause is from it
PROFILE = [
    "Engineer with over 25 years' experience across hardware, FPGA, SoC, DSP and software.",
    "Much of it designing and verifying FPGA and SoC systems (packet switching, high-speed serial links, cable "
    "modem PHY/MAC, CPU debug, broadcast video, cryptography), then board-level hardware for AI accelerators at "
    "Blaize: power delivery, signal integrity and DDR.",
    "For the last two years almost entirely software, mainly Python, building agentic AI systems with LangGraph "
    "and MCP; Claude Code and OpenCode every day.",
    "Keen to work where a hardware background counts, such as new compute architectures.",
]

# timeline colour per role (by company and start year); a role that spanned two domains carries two
DOMAINS = {
    ("Thales", 1994): ["hardware", "fpga"],
    ("Pace", 1998): ["hardware", "fpga"],
    ("Comodo", 2002): ["fpga", "crypto"],
    ("Pace", 2005): ["fpga", "dsp"],
    ("Red Embedded", 2011): ["fpga", "hardware", "dsp"],
    ("Imagination Technologies / MIPS", 2014): ["fpga", "hardware", "dsp"],
    ("Blaize (formerly Thinci)", 2018): ["hardware", "ai"],
}
DOMAIN_LABEL = {"hardware": "Hardware", "fpga": "FPGA and SoC", "dsp": "DSP", "crypto": "Cryptography",
                "ai": "Software and AI"}


def sections(text):
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^## (.+)$", line)
        if m:
            cur = m.group(1).strip()
            out[cur] = []
        elif cur:
            out[cur].append(line)
    return out


def bullets(lines):
    """Markdown bullets, with their wrapped continuation lines joined."""
    items = []
    for line in lines:
        if line.startswith("- "):
            items.append(line[2:].strip())
        elif line.startswith("  ") and items:
            items[-1] += " " + line.strip()
    return items


def paragraphs(lines):
    paras, cur = [], []
    for line in lines:
        if not line.strip() or line.startswith("- "):
            if cur:
                paras.append(" ".join(cur))
            cur = []
        elif not line.startswith("  "):
            cur.append(line.strip())
    if cur:
        paras.append(" ".join(cur))
    return paras


def month_year(s):
    s = s.strip()
    if s == "present":
        return None
    m, y = s.split()
    return int(y) + (MONTHS.index(m)) / 12


def roles(lines):
    out, cur = [], None
    for line in lines + ["### end"]:
        m = re.match(r"^### (.+?), (.+), (\w[\w ]*) — (\w+ \d{4}) to (present|\w+ \d{4})$", line)
        if line.startswith("### "):
            if cur:
                body = cur.pop("lines")
                cur["intro"] = " ".join(paragraphs(body))
                cur["bullets"] = bullets(body)
                out.append(cur)
            cur = None
            if line == "### end":
                break
            assert m, line
            title, company, place, start, end = m.groups()
            cur = dict(title=title, company=company, place=place, start=start, end=end,
                       t0=month_year(start), t1=month_year(end), lines=[])
            cur["domains"] = DOMAINS[(company, int(start.split()[1]))]
            cur["id"] = re.sub(r"[^a-z0-9]+", "-", f"{company.split(' (')[0]} {start.split()[1]}".lower()).strip("-")
        elif cur is not None:
            cur["lines"].append(line)
    return out


def split_top(s, seps):
    """Split on any of seps outside parentheses."""
    parts, depth, cur = [], 0, ""
    for ch in s:
        depth += (ch == "(") - (ch == ")")
        if ch in seps and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    return [p for p in parts + [cur.strip()] if p]


def skill_chips(s):
    chips = []
    for part in split_top(s, ";"):
        # "Synopsys, Cadence and Mentor simulation and synthesis tools" is one item, not three
        chips += [part] if part.endswith(" tools") and "," in part else split_top(part, ",")
    return chips


def education(item):
    m = re.match(r"^(.+?), (.+) \((.+)\)$", item)
    degree, school, when = m.groups()
    part_time = when.startswith("part-time, ")
    return dict(degree=degree, school=school, years=when.replace("part-time, ", ""), part_time=part_time, raw=item)


def parse(path=SOURCE):
    sec = sections(open(path).read())
    ident = {}
    for b in bullets(sec["Identity and links"]):
        k, _, v = b.partition(": ")
        ident[k] = v
    skills = []
    for b in bullets(sec["Skills"]):
        k, _, v = b.partition(": ")
        skills.append((k, skill_chips(v)))
    certs_head = next(k for k in sec if k.startswith("Certifications"))
    return dict(
        name=ident["Name"], location=ident["Location"], linkedin=ident["LinkedIn"], github=ident["GitHub"],
        portfolio=ident["Portfolio"], twin=ident["Career Conversation (earlier Digital Twin)"],
        headline=" ".join(paragraphs(sec["Headline"])),
        profile_source=bullets(sec["Profile"]),
        roles=roles(sec["Experience"]),
        education=[education(x) for x in bullets(sec["Education"])],
        certs=bullets(sec[certs_head]),
        certs_note=re.search(r"\((.+)\)", certs_head).group(1),
        skills=skills,
    )


CV = parse()

if __name__ == "__main__":
    import pprint
    pprint.pprint(CV, width=120)
