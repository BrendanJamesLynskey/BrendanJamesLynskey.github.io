"""Check that every quote in tools/content.py appears, word for word, on its source page.

    python3 tools/check_quotes.py

The page is fetched (the raw file for a GitHub README), its tags are stripped for an HTML page, and
whitespace and entities are normalised on both sides. Exits non-zero if any quote is missing.
"""
import html
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import QUOTES  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (portfolio-home quote check)"}


def norm(s):
    s = html.unescape(s).replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", s).strip()


def page_text(url):
    req = urllib.request.Request(url, headers=UA)
    raw = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
    if "raw.githubusercontent.com" in url:
        return norm(raw), norm(raw)
    body = re.sub(r"<!--.*?-->", "", re.sub(r"<script.*?</script>", " ", raw, flags=re.S), flags=re.S)
    text = re.sub(r"<[^>]+>", " ", body)
    # Next.js pages also carry their text in the RSC payload; keep the raw page as a fallback
    return norm(text), norm(raw.replace('\\"', '"'))


def main():
    cache, bad = {}, 0
    for qid, (shown, fetch, quote) in QUOTES.items():
        url = (fetch or shown).split("#")[0]
        if url not in cache:
            cache[url] = page_text(url)
        text, raw = cache[url]
        q = norm(quote)
        ok = q in text or q in raw or q in re.sub(r" ([,.;:])", r"\1", text)
        print(("ok   " if ok else "MISS ") + qid, url)
        bad += not ok
    print(f"{len(QUOTES) - bad}/{len(QUOTES)} quotes found")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
