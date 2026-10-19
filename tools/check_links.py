"""Check every link and image on the built pages (and the profile README, if given) returns 200.

    python3 tools/check_links.py [--live] [../BrendanJamesLynskey/README.md]

Root-relative links are checked against the files in this repo. Absolute links are fetched (GET, redirects
followed, a browser user agent). Links to this site and to its own repositories cannot exist before the
first publish; they are listed as "after publish", and checked too with --live (the owner script runs that
once the site is up).
"""
import concurrent.futures
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "sites/index.html", "checks/index.html", "cv/index.html", "optalysys/index.html", "404.html"]
# the site's own pages (at the canonical Vercel address and on GitHub Pages) and repositories: exist only once
# published
PENDING = re.compile(r"^https://(brendan-lynskey\.vercel\.app|brendanjameslynskey\.github\.io)"
                     r"/(checks/|cv/|sites/|optalysys/|cv/Brendan_Lynskey_CV\.pdf|og\.png|sitemap\.xml|#[\w-]+)?$"
                     r"|^https://github\.com/BrendanJamesLynskey/BrendanJamesLynskey(\.github\.io)?$")
# LinkedIn (999) and optalysys.com (403) answer automated requests with an error whatever the page; reported, not counted as a failure
BLOCKS_BOTS = re.compile(r"^https://(www\.linkedin\.com|optalysys\.com)/")


def links_in(path):
    s = open(path).read()
    if path.endswith(".md"):
        return set(re.findall(r"\]\((https?://[^)\s]+)\)", s))
    return set(re.findall(r'(?:href|src|content)="((?:https?://|/)[^"]*)"', s))


def fetch(url):
    req = urllib.request.Request(url.split("#")[0], headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return url, r.status
    except urllib.error.HTTPError as e:
        return url, e.code
    except Exception as e:  # noqa: BLE001
        return url, str(e)


def main():
    urls, local = set(), set()
    live = "--live" in sys.argv
    files = [os.path.join(ROOT, p) for p in PAGES] + [a for a in sys.argv[1:] if a != "--live"]
    for f in files:
        for u in links_in(f):
            (local if u.startswith("/") else urls).add(u)
    bad = 0
    for u in sorted(local):
        p = u.split("#")[0].split("?")[0]
        p = os.path.join(ROOT, p.lstrip("/"), "index.html" if p.endswith("/") else "")
        ok = os.path.isfile(p.rstrip("/"))
        bad += not ok
        print(("ok    " if ok else "MISS  ") + u)
    pending = [] if live else sorted(u for u in urls if PENDING.match(u))
    ext = sorted(urls - set(pending))
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        for u, code in ex.map(fetch, ext):
            if code in (999, 403) and BLOCKS_BOTS.match(u):
                print(f"bot?  {code} {u} (refuses automated requests; check it by hand)")
                continue
            ok = code == 200
            bad += not ok
            print(f"{'ok  ' if ok else 'FAIL'}  {code} {u}")
    for u in pending:
        print("after publish  " + u)
    print(f"{len(local)} local, {len(ext)} external checked, {len(pending)} after publish; {bad} failures")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
