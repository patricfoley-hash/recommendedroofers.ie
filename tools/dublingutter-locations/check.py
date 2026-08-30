# -*- coding: utf-8 -*-
"""Quality gates for the generated dublingutter.ie pages.

    python3 check.py            # check the built site
    python3 check.py --live     # also fetch every URL from dublingutter.ie

Fails loudly on: broken internal links, duplicate titles/descriptions/H1s,
malformed HTML, and area pages that read too much alike (the doorway-page risk).
"""
import os, re, sys, glob, html.parser, itertools, statistics, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import ALL, HUBS, OUT
from blog import POSTS

# A first pass without the variant pools scored 0.363 and read as templated.
SIMILARITY_CEILING = 0.22   # median 6-gram Jaccard between area pages
VOID = {"br","img","input","meta","link","hr","source","area","base","col",
        "embed","param","track","wbr"}
fails = []

def note(ok, label, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}{(' — ' + detail) if detail else ''}")
    if not ok: fails.append(label)

def pages():
    return glob.glob(os.path.join(OUT, "*.html")) + glob.glob(os.path.join(OUT, "blog", "*.html"))

def body(p):
    s = open(p).read()
    s = re.sub(r'(?s)<(script|style).*?</\1>', ' ', s)
    s = re.sub(r'(?s)<footer.*?</footer>', ' ', s)
    s = re.sub(r'(?s)<header.*?</header>', ' ', s)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip().lower()

class Parser(html.parser.HTMLParser):
    def __init__(self): super().__init__(); self.stack = []; self.bad = []
    def handle_startendtag(self, t, a): pass
    def handle_starttag(self, t, a):
        if t not in VOID: self.stack.append(t)
    def handle_endtag(self, t):
        if t in VOID: return
        if self.stack and self.stack[-1] == t: self.stack.pop()
        elif t in self.stack:
            while self.stack and self.stack.pop() != t: pass
        else: self.bad.append(t)

def main():
    ps = pages()
    print(f"\n{len(ps)} pages in {os.path.relpath(OUT)}\n")

    # 1. internal links all resolve
    have = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(OUT, "*.html"))}
    have |= {"blog/" + os.path.basename(f)[:-5] for f in glob.glob(os.path.join(OUT, "blog", "*.html"))}
    have.add("")
    broken = collections.Counter()
    for f in ps:
        for href in set(re.findall(r'href="/([a-z0-9\-/]*)"', open(f).read())):
            if href.rstrip("/") not in have: broken[href] += 1
    note(not broken, "internal links resolve", f"{len(broken)} broken: {list(broken)[:5]}" if broken else "")

    # 2. no duplicate titles / descriptions / H1s
    for label, rx in (("titles", r'<title>(.*?)</title>'),
                      ("meta descriptions", r'name="description" content="(.*?)"'),
                      ("H1s", r'<h1[^>]*>(.*?)</h1>')):
        c = collections.Counter()
        for f in ps:
            m = re.search(rx, open(f).read(), re.S)
            if m: c[m.group(1).strip()] += 1
        dupes = [k[:45] for k, v in c.items() if v > 1]
        note(not dupes, f"unique {label}", f"{len(dupes)} duplicated: {dupes[:3]}" if dupes else "")

    # 3. well-formed HTML
    bad = []
    for f in ps:
        p = Parser(); p.feed(open(f).read())
        if p.bad or p.stack: bad.append(os.path.basename(f))
    note(not bad, "HTML well-formed", f"{len(bad)} malformed: {bad[:3]}" if bad else "")

    # 4. area pages don't read as one template with the name swapped
    T = {a["slug"]: body(os.path.join(OUT, f"gutter-services-{a['slug']}.html")) for a in ALL}
    def shingles(t, n=6):
        w = t.split(); return {tuple(w[i:i+n]) for i in range(len(w)-n+1)}
    S = {k: shingles(v) for k, v in T.items()}
    sims = [(len(S[a] & S[b]) / len(S[a] | S[b]), a, b) for a, b in itertools.combinations(S, 2)]
    med = statistics.median(s for s, _, _ in sims)
    worst = max(sims)
    note(med <= SIMILARITY_CEILING, "area pages read distinctly",
         f"median 6-gram Jaccard {med:.3f} (ceiling {SIMILARITY_CEILING}), worst pair "
         f"{worst[1]}/{worst[2]} at {worst[0]:.3f}")

    wc = [len(v.split()) for v in T.values()]
    note(min(wc) >= 500, "area pages have real substance", f"{min(wc)}-{max(wc)} words")

    # 5. every page carries its schema
    missing = [os.path.basename(f) for f in ps if "application/ld+json" not in open(f).read()]
    note(not missing, "structured data present", f"{len(missing)} missing" if missing else "")

    if "--live" in sys.argv:
        import subprocess, concurrent.futures as cf
        # Cloudflare 403s non-browser user-agents on this site — always send a real UA.
        UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
        urls = ["", "near-me", "blog", "services", "about", "contact", "quote", "sitemap.xml"]
        urls += [HUBS[r][0] for r in ("north", "south")]
        urls += [f"gutter-services-{a['slug']}" for a in ALL]
        urls += [f"blog/{p['slug']}" for p in POSTS]
        def fetch(u):
            r = subprocess.run(["curl", "-sS", "-A", UA, "-o", "/dev/null",
                                "-w", "%{http_code} %{size_download}",
                                "https://dublingutter.ie/" + u],
                               capture_output=True, text=True).stdout.split()
            return u, r[0], int(r[1])
        with cf.ThreadPoolExecutor(10) as ex:
            live_bad = [(u, c, n) for u, c, n in ex.map(fetch, urls) if c != "200" or n < 3000]
        note(not live_bad, f"all {len(urls)} URLs live", str(live_bad[:3]) if live_bad else "")

    print()
    if fails:
        print(f"{len(fails)} CHECK(S) FAILED: {', '.join(fails)}\n"); sys.exit(1)
    print("all checks passed\n")

if __name__ == "__main__":
    main()
