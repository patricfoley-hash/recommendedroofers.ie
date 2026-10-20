# -*- coding: utf-8 -*-
"""Add the 'at a Glance' box + Gerard's Person schema to the six HAND-WRITTEN service pages.

Those pages are not generated (gen.py/blog.py own the area, hub and blog pages), so this edits them in place.
Idempotent: a page that already has the box is skipped.   Usage: python3 apply_service_boxes.py
"""
import json, os, re, sys
import glance as G

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "dublingutter")

for fname, sentences in G.SERVICE_BOXES.items():
    path = os.path.join(SITE, fname)
    h = open(path, encoding="utf8").read()
    if 'class="glance"' in h:
        print(f"skip {fname} (already has the box)"); continue
    title = re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S).group(1)).strip().replace("&amp;", "&")
    # the box goes straight after the credentials strip, which follows the trust bar on these pages
    m = re.search(r'<div class="creds"[^>]*>.*?</div></div>\s*\n', h, re.S)
    if not m:
        sys.exit(f"{fname}: credentials strip not found, nothing changed")
    h = h[:m.end()] + G.box(f"{title} at a Glance", sentences) + h[m.end():]
    # schema: add Gerard to the page's own graph
    def add_person(mm):
        j = json.loads(mm.group(1))
        g = j["@graph"]
        if not any(n.get("@id") == G.GERARD_NODE["@id"] for n in g):
            g.append(G.GERARD_NODE)
        return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + "</script>"
    h, n = re.subn(r'<script type="application/ld\+json">(.*?)</script>', add_person, h, count=1, flags=re.S)
    assert n == 1, f"{fname}: no JSON-LD"
    open(path, "w", encoding="utf8").write(h)
    print(f"✓ {fname}")
