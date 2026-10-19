"""Check /cv/ against src/cv_source.md.

    python3 tools/check_cv.py

Every experience entry (title, company, place, intro and bullets), date range, education item, award string,
certification in the source must appear on cv/index.html, and nothing else in those categories may:
the page must hold exactly the source's roles, education items and certifications, every date range on it must be
one of the source's, and every sentence on it that mentions an award must come from the source. Exits non-zero on
any failure.
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cv import CV, MONTHS, ROOT  # noqa: E402

PAGE = os.path.join(ROOT, "cv", "index.html")
MONTH = "(?:" + "|".join(MONTHS) + ")"


def norm(s):
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def text_of(fragment):
    return norm(re.sub(r"<[^>]+>", " ", fragment)).replace(" ,", ",")


def main():
    raw = open(PAGE).read()
    body = re.sub(r"<(style|script)\b.*?</\1>", " ", raw, flags=re.S)
    page = text_of(body)
    bad = []

    def need(what, s):
        if norm(s) not in page:
            bad.append(f"missing {what}: {s}")

    # experience: exactly the source's roles, each with all its text
    articles = re.findall(r'<article class="role"[^>]*data-title="([^"]*)" data-company="([^"]*)">(.*?)</article>',
                          raw, re.S)
    src_roles = [(r["title"], r["company"]) for r in CV["roles"]]
    page_roles = [(html.unescape(t), html.unescape(c)) for t, c, _ in articles]
    if page_roles != src_roles:
        bad.append(f"roles on the page {page_roles} differ from the source {src_roles}")
    for r, (_, _, inner) in zip(CV["roles"], articles):
        txt = text_of(inner)
        for what, s in [("title", r["title"]), ("company", r["company"]), ("place", r["place"]),
                        ("date range", f"{r['start']} – {r['end']}"), ("intro", r["intro"])]:
            if norm(s) not in txt:
                bad.append(f"{r['id']}: missing {what}: {s}")
        for b in r["bullets"]:
            if norm(b) not in txt:
                bad.append(f"{r['id']}: missing bullet: {b}")
        if len(re.findall(r"<li>", inner)) != len(r["bullets"]):
            bad.append(f"{r['id']}: {len(re.findall('<li>', inner))} bullets on the page, {len(r['bullets'])} in the source")

    # date ranges: every one on the page is a role's or an education item's
    ranges = {f"{r['start']} – {r['end']}" for r in CV["roles"]}
    for m in re.findall(rf"{MONTH} \d{{4}} – (?:present|{MONTH} \d{{4}})", page):
        if m not in ranges:
            bad.append(f"date range not in the source: {m}")
    years = {x["years"] for x in CV["education"]}
    for m in re.findall(r"\b\d{4}–\d{4}\b", page):
        if m not in years:
            bad.append(f"year range not in the source: {m}")
    for r in ranges:
        need("date range", r)

    # education: exactly the source's items
    edu = re.search(r'<ul class="edu">(.*?)</ul>', raw, re.S).group(1)
    items = [text_of(x) for x in re.findall(r"<li>(.*?)</li>", edu, re.S)]
    if len(items) != len(CV["education"]):
        bad.append(f"{len(items)} education items on the page, {len(CV['education'])} in the source")
    for x, shown in zip(CV["education"], items):
        for part in [x["degree"], x["school"], x["years"]] + (["part-time"] if x["part_time"] else []):
            if part not in shown:
                bad.append(f"education item {x['raw']!r}: missing {part!r} in {shown!r}")

    # certifications: exactly the source's
    certs = re.search(r'<ul class="certs">(.*?)</ul>', raw, re.S).group(1)
    shown = [text_of(x) for x in re.findall(r"<li>(.*?)</li>", certs, re.S)]
    if shown != [norm(c) for c in CV["certs"]]:
        bad.append(f"certifications on the page {shown} differ from the source {CV['certs']}")

    # awards: each source award string is on the page, and every sentence mentioning an award is from the source
    awards = []
    for r in CV["roles"]:
        for s in [r["intro"]] + r["bullets"]:
            awards += [a for a in re.findall(r"[^.;]*\b[Aa]wards?\b[^.;]*", s)]
    for a in awards:
        need("award", a.strip())
    sources = " ".join(norm(s) for r in CV["roles"] for s in [r["intro"]] + r["bullets"])
    nodes = [norm(t) for t in re.split(r"<[^>]+>", body) if t.strip()]
    for m in [m for t in nodes for m in re.findall(r"[^.;]*\b(?:[Aa]wards?|[Pp]rize|Product of the Year)\b[^.;]*", t)]:
        if norm(m) not in sources:
            bad.append(f"award text not in the source: {m.strip()}")

    # skills are deliberately not shown on the page (owner decision, 2026-10-19)
    if 'class="chips"' in raw:
        bad.append("a skills section is on the page; it was removed by the owner")

    n = len(CV["roles"])
    print(f"roles {len(articles)}/{n}, date ranges {len(ranges)}, education {len(items)}/{len(CV['education'])}, "
          f"certifications {len(shown)}/{len(CV['certs'])}, award strings {len(awards)}")
    for b in bad:
        print("FAIL", b)
    print("ok: /cv/ matches src/cv_source.md" if not bad else f"{len(bad)} failures")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
