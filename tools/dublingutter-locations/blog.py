# -*- coding: utf-8 -*-
"""Blog index + first posts. Each post answers a question a Dublin homeowner
actually types, and links back into the service and area pages."""
import sys, os, html, re
sys.path.insert(0,'.')
from gen import (OUT, HEAD_CSS, topbar_header, FOOTER, QUOTE_FORM, PHONE, PHONE_HREF,
                 esc, jsonstr, ALL, HUBS)

HAND_WRITTEN = [
 dict(slug="how-often-should-you-clean-gutters-ireland",
  title="How Often Should You Clean Your Gutters in Ireland?",
  desc="Most Dublin homes need gutters cleared twice a year — but it depends on the trees around you. Here's how to tell what your house needs.",
  cat="Maintenance", read=6, date="2026-08-30",
  lede="The honest answer is twice a year for most Dublin houses. But that's an average, and averages are no use if you live under a line of lime trees.",
  body=[
   ("The short answer","<p>For a typical Dublin semi with no large trees overhanging the roof, <strong>once a year in late autumn</strong> is usually enough. Add a second clean in late spring if any of the following apply:</p>"
    "<ul class=\"post-list\"><li>Mature trees within about fifteen metres of the house</li><li>A north-facing roof that holds moss</li><li>Any gutter run that has overflowed in the last two years</li><li>A flat or shallow-pitched section that drains slowly</li></ul>"
    "<p>Houses on heavily planted roads — Rathgar, Clontarf, Mount Merrion, Castleknock — routinely need two cleans. Newer estates on open ground often manage on one.</p>"),
   ("Why autumn matters more than spring","<p>Leaf fall is the obvious reason, but it's not the main one. The real damage happens when a gutter full of wet leaf sits through a Dublin winter. The debris holds water against the fascia board, the timber softens, and by spring you have a rot problem rather than a blockage problem.</p>"
    "<p>Clearing in November, once the trees are bare, empties the gutter before the wet months do the harm. Clearing in March cleans up what the winter blew in.</p>"),
   ("The signs you've left it too long","<p>You don't need to get on a ladder to know. Watch for:</p>"
    "<ul class=\"post-list\"><li><strong>Water spilling over the front edge</strong> during rain — the classic sign of a blockage or a lost fall</li><li><strong>Staining down the wall</strong> beneath a joint or a gutter end</li><li><strong>Plants growing in the gutter</strong> — if something has rooted, there is soil up there</li><li><strong>Water running behind the gutter</strong> rather than out of the downpipe</li><li><strong>Damp patches inside</strong> on an upstairs wall or ceiling near the eaves</li></ul>"
    "<p>The last one means it has already stopped being a gutter problem.</p>"),
   ("What it costs to leave it","<p>A gutter clean is a modest job. The things a blocked gutter causes are not. Rotten fascia and soffit, damp penetrating a wall, and in the worst cases water tracking into a ceiling — all of them cost multiples of what the clean would have.</p>"
    "<p>That is the whole argument for doing it on a schedule rather than waiting for a symptom.</p>"),
   ("Doing it yourself","<p>If your house is a bungalow and you are comfortable and steady on a ladder, clearing your own gutters is reasonable. Wear gloves, work from a properly footed ladder, never lean sideways, and flush the downpipe with a hose when you have finished so you know it runs.</p>"
    "<p>On a two-storey house — or anything with a steep roof, an awkward return, or no flat ground for a ladder — it is not worth the risk. That is most of what we get called to.</p>"),
  ],
  faq=[("How much does gutter cleaning cost in Dublin?","It depends on the size of the house and the access. We quote per job after a look, with no call-out fee, so you know the figure before anything starts."),
       ("Do you clean the downpipes too?","Yes. Clearing the gutter and leaving a blocked downpipe achieves nothing — we flush the whole system and check it runs."),
       ("What time of year is best?","Late autumn, once the leaves are down. If you only do one clean a year, that is the one to do.")],
  links=[("/gutter-cleaning","Gutter cleaning"),("/gutter-repairs","Gutter repairs"),("/near-me","Areas we cover")]),

 dict(slug="signs-you-need-new-gutters",
  title="7 Signs You Need New Gutters (Not Just a Repair)",
  desc="Most gutter faults are a repair. These seven are the ones where replacement is genuinely the cheaper answer.",
  cat="Repairs", read=7, date="2026-08-30",
  lede="We repair before we replace, and we say so on every page of this site. But there is a point where repairing stops being the economical choice — here is how to recognise it.",
  body=[
   ("1. The gutter is cracked along its length","<p>A single cracked joint is a repair. A crack running the length of a section means the material itself has gone brittle — usually old PVC that has spent thirty years in UV. Patch it and the next section fails a month later.</p>"),
   ("2. It sags between every bracket","<p>Sagging at one point is a failed bracket. Sagging in a regular wave along the whole run means the gutter has lost its rigidity. New brackets will hold it up briefly and then pull through.</p>"),
   ("3. The profile is too small for the roof","<p>A great many Dublin houses built before the 1970s have gutters sized for the rainfall of that era. If yours overflows in heavy rain even when it is perfectly clean, no repair will fix it — the gutter is simply too small. Upsizing the profile is the fix.</p>"),
   ("4. There are more patches than gutter","<p>Sealant and repair tape have their place. When a run has four or five of them, each one is a future leak, and you are paying a call-out charge every year to add another.</p>"),
   ("5. Rust has gone through cast iron","<p>Cast iron is worth saving and often can be. But once rust has eaten right through the base rather than just pitting the surface, the section is finished. On a period house we usually replace the failed sections in matching cast iron rather than replacing the lot.</p>"),
   ("6. The fascia behind it has rotted","<p>If the board the gutter is screwed to has gone soft, there is nothing to fix a new bracket into. At that point gutter, fascia and soffit get done together — which is more work, but doing it in one visit is considerably cheaper than doing it twice.</p>"),
   ("7. The joints leak at every seam","<p>Old PVC gutters rely on rubber seals that harden and shrink. When one goes, the rest are the same age. Replacing every seal on a run costs close to what a new run costs, and the new run comes with a guarantee.</p>"),
  ],
  faq=[("Will you always try to repair first?","Yes. If a repair will genuinely hold, that is what we recommend and what we quote. We will tell you plainly when it will not."),
       ("How long should new gutters last?","Well-fitted PVC should give you thirty years or more. Aluminium and cast iron considerably longer."),
       ("Can you match my existing colour?","In almost every case, yes — including black, brown, grey and white in the common profiles.")],
  links=[("/new-gutters","New gutters"),("/gutter-repairs","Gutter repairs"),("/fascia-soffit","Fascia &amp; soffit")]),

 dict(slug="gutter-problems-dublin-houses",
  title="The Gutter Problems We See Most in Dublin — by Type of House",
  desc="Georgian, 1930s corporation, 1970s estate or a new build — the age of your house predicts the gutter problem you'll get.",
  cat="Local Knowledge", read=8, date="2026-08-30",
  lede="After thirty years on Dublin roofs, you can usually guess the fault from the address. The housing stock in this city falls into a handful of eras, and each one fails in its own way.",
  body=[
   ("Georgian and Victorian: parapet and valley gutters","<p>In the city centre, Dublin 4, Rathmines, Ranelagh and along the coast, the gutter is often not on the front of the house at all. It sits behind a parapet wall or in a valley between two roof slopes, draining into a hopper head and down a cast iron pipe.</p>"
    "<p>These leak inward. By the time you see a stain on a bedroom ceiling, water has been tracking through the structure for months. They need inspecting on a schedule, not waiting for a symptom.</p>"),
   ("1930s to 1950s: undersized and cast iron","<p>Crumlin, Cabra, Kimmage, Marino, Whitehall, Drimnagh — mile after mile of well-built houses with gutters sized for a different climate. Original cast iron is heavy, rusts from the inside, and the profiles are narrow.</p>"
    "<p>The common call here is overflow in heavy rain on a gutter that is perfectly clean. The gutter is simply too small, and upsizing it is the honest answer.</p>"),
   ("1960s to 1980s estates: everything ages at once","<p>Tallaght, Coolock, Finglas, Donaghmede, Knocklyon, Ballinteer. These estates went up quickly and to a common pattern, which means the gutters reach the end of their life across a whole road within a few years of each other.</p>"
    "<p>It is why we often do three or four houses on the same terrace in a week — and why neighbours going in together usually get a better rate.</p>"),
   ("Modern estates: fitting, not failure","<p>Adamstown, Citywest, Ongar, Leopardstown, Clongriffin. The gutters are new, so the material is fine. The problems are how they went on: falls that run the wrong way, joints that were never properly seated, and — most commonly — one downpipe serving a three-storey roof that needs two.</p>"
    "<p>These are refit jobs rather than replacements, and they are usually straightforward once someone actually measures the fall.</p>"),
   ("Coastal, at any age","<p>From Howth round through Clontarf and Sandymount, down to Dún Laoghaire, Dalkey and Shankill, salt is the deciding factor. It attacks fixings far faster than anything inland. Brackets fail while the gutter itself is still sound, which looks baffling until you know why.</p>"
    "<p>We fit stainless or marine-grade fixings as standard on coastal work. It costs a little more and lasts many times longer.</p>"),
  ],
  faq=[("Does the age of my house really change the price?","It changes the work. A parapet gutter on a protected Georgian building is a different job to a PVC run on a 1970s semi, and the quote reflects that."),
       ("Do you work on protected structures?","Yes. We work regularly on period and protected buildings and can match original profiles in cast iron."),
       ("I'm in a new estate and my gutters already overflow — is that normal?","It is common, and it is usually a fitting or sizing fault rather than a defect. It can normally be corrected without replacing anything.")],
  links=[("/gutter-services-north-dublin","North Dublin areas"),("/gutter-services-south-dublin","South Dublin areas"),("/commercial-guttering","Commercial guttering")]),
]

# Posts written by the Core content pipeline live in their own file, so
# publish-dublingutter-blog.mjs can rewrite that file wholesale without ever
# risking the hand-written posts above. Newest date first, so the index leads
# with the newest work and every post's "Keep Reading" block follows suit.
try:
    from posts_generated import POSTS as _PIPELINE
except ImportError:
    _PIPELINE = []

# A hand-written post always wins a slug clash — the pipeline must never
# silently overwrite something a person wrote.
_HAND = {p["slug"] for p in HAND_WRITTEN}
_merged = HAND_WRITTEN + [p for p in _PIPELINE if p["slug"] not in _HAND]
POSTS = sorted(_merged, key=lambda x: x["date"], reverse=True)

BLOG_CSS = """  <style>
    .post-body { max-width: 72ch; margin: 0 auto; }
    .post-body h2 { font-size: 1.45rem; margin: 44px 0 14px; color: var(--grey-dark); }
    .post-body p { color: var(--text); line-height: 1.85; margin-bottom: 16px; }
    .post-lede { font-size: 1.12rem; color: var(--grey-dark); line-height: 1.8; padding-bottom: 26px; margin-bottom: 10px; border-bottom: 2px solid var(--blue-light); }
    .post-list { display: flex; flex-direction: column; gap: 9px; margin: 0 0 18px; }
    .post-list li { display: flex; align-items: flex-start; gap: 10px; color: var(--text); line-height: 1.7; }
    .post-list li::before { content: '\\2713'; color: var(--yellow-dark); font-weight: 700; flex-shrink: 0; }
    .post-meta { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; color: rgba(255,255,255,0.8); font-size: 0.88rem; }
    .post-cat { background: var(--yellow); color: var(--grey-dark); padding: 4px 12px; border-radius: 50px; font-weight: 700; font-size: 0.78rem; font-family: 'Poppins', sans-serif; }
    .post-links { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 26px; }
    .post-link-chip { display: inline-flex; align-items: center; gap: 7px; background: var(--white); border: 1.5px solid var(--border); border-radius: 100px; padding: 9px 16px; font-size: 0.88rem; font-weight: 600; color: var(--grey-dark); text-decoration: none; transition: all var(--transition); }
    .post-link-chip:hover { border-color: var(--blue); color: var(--blue); }
    .blog-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 24px; }
    .blog-card { background: var(--white); border: 1.5px solid var(--border); border-radius: var(--radius-lg); padding: 26px; text-decoration: none; color: inherit; display: flex; flex-direction: column; transition: all var(--transition); }
    .blog-card:hover { border-color: var(--blue); box-shadow: var(--shadow); transform: translateY(-3px); }
    .blog-card .post-cat { align-self: flex-start; margin-bottom: 14px; }
    .blog-card h2 { font-size: 1.15rem; margin-bottom: 10px; color: var(--grey-dark); }
    .blog-card p { font-size: 0.9rem; color: var(--grey); line-height: 1.65; flex: 1; }
    .blog-card .read { margin-top: 16px; font-size: 0.85rem; font-weight: 600; color: var(--yellow-dark); font-family: 'Poppins', sans-serif; display: flex; align-items: center; gap: 6px; }
  </style>"""

def _faq_ld(faq):
    return ",\n      ".join(
        '{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
        % (jsonstr(q), jsonstr(a)) for q, a in faq)

def post_page(p):
    secs = "\n".join(f"        <h2>{esc(h)}</h2>\n        {b}" for h, b in p["body"])
    faqs = "\n        ".join(
        f'<div class="faq-item"><button class="faq-q" onclick="toggleFaq(this)">{esc(q)} <i class="fas fa-plus"></i></button>'
        f'<div class="faq-a"><p>{esc(a)}</p></div></div>' for q, a in p["faq"])
    chips = "\n        ".join(
        f'<a href="{h}" class="post-link-chip"><i class="fas fa-arrow-right"></i> {t}</a>' for h, t in p["links"])
    # Capped at 3. With two hand-written posts "every other post" was a
    # sensible Keep Reading block; once the pipeline is feeding this blog it
    # would be a wall of twenty cards under every article.
    others = [o for o in POSTS if o["slug"] != p["slug"]][:3]
    more = "\n        ".join(
        f'<a href="/blog/{o["slug"]}" class="blog-card"><span class="post-cat">{esc(o["cat"])}</span>'
        f'<h2>{esc(o["title"])}</h2><p>{esc(o["desc"])}</p>'
        f'<span class="read">Read more <i class="fas fa-arrow-right"></i></span></a>' for o in others)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="canonical" href="https://dublingutter.ie/blog/{p['slug']}" />
  <title>{esc(p['title'])} | Recommended Roofing &amp; Guttering</title>
  <meta name="description" content="{esc(p['desc'])}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Open+Sans:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  <link rel="stylesheet" href="/style.css" />
{HEAD_CSS}
{BLOG_CSS}
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
    {{
      "@type": "BlogPosting",
      "headline": {jsonstr(p['title'])},
      "description": {jsonstr(p['desc'])},
      "datePublished": "{p['date']}",
      "dateModified": "{p['date']}",
      "author": {{ "@type": "Organization", "name": "Recommended Roofing & Guttering" }},
      "publisher": {{ "@type": "Organization", "name": "Recommended Roofing & Guttering",
        "logo": {{ "@type": "ImageObject", "url": "https://dublingutter.ie/images/logo-recommended-roofing.svg" }} }},
      "mainEntityOfPage": "https://dublingutter.ie/blog/{p['slug']}"
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://dublingutter.ie/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Gutter Advice", "item": "https://dublingutter.ie/blog" }},
        {{ "@type": "ListItem", "position": 3, "name": {jsonstr(p['title'])}, "item": "https://dublingutter.ie/blog/{p['slug']}" }}
      ]
    }},
    {{ "@type": "FAQPage", "mainEntity": [
      {_faq_ld(p['faq'])}
    ] }}
    ]
  }}
  </script>
</head>
<body>
{topbar_header("Blog").replace('src="images/', 'src="/images/')}
  <section class="service-hero">
    <div class="container">
      <div class="breadcrumb"><a href="/">Home</a><span>/</span><a href="/blog">Gutter Advice</a><span>/</span><span>{esc(p['title'][:40])}&hellip;</span></div>
      <h1 style="color:var(--white);max-width:20ch;font-size:clamp(1.8rem,3.5vw,2.6rem);margin:14px 0 18px;">{esc(p['title'])}</h1>
      <div class="post-meta">
        <span class="post-cat">{esc(p['cat'])}</span>
        <span><i class="fas fa-clock"></i> {p['read']} min read</span>
        <span><i class="fas fa-calendar"></i> {p['date']}</span>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="post-body">
        <p class="post-lede">{esc(p['lede'])}</p>
{secs}
        <div class="post-links">
        {chips}
        </div>
      </div>
    </div>
  </section>

  <section class="section section-light">
    <div class="container">
      <div class="section-header"><span class="section-tag">FAQ</span><h2>Common Questions</h2></div>
      <div class="faq-grid">
        {faqs}
      </div>
    </div>
  </section>

  <section class="cta-banner">
    <div class="container cta-inner">
      <div class="cta-text"><h2>Need a Hand With Your Gutters?</h2><p>Free quote, fixed price, no call-out fee — anywhere in Dublin.</p></div>
      <div class="cta-actions">
        <a href="tel:{PHONE_HREF}" class="btn btn-white"><i class="fas fa-phone"></i> {PHONE}</a>
        <a href="/quote" class="btn btn-outline-white">Get Free Quote</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-header"><span class="section-tag">More Advice</span><h2>Keep Reading</h2></div>
      <div class="blog-grid">
        {more}
      </div>
    </div>
  </section>
{FOOTER.replace('src="images/', 'src="/images/')}"""


def blog_index():
    cards = "\n        ".join(
        f'<a href="/blog/{p["slug"]}" class="blog-card"><span class="post-cat">{esc(p["cat"])}</span>'
        f'<h2>{esc(p["title"])}</h2><p>{esc(p["desc"])}</p>'
        f'<span class="read">{p["read"]} min read <i class="fas fa-arrow-right"></i></span></a>' for p in POSTS)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="canonical" href="https://dublingutter.ie/blog" />
  <title>Gutter Advice for Dublin Homeowners | Recommended Roofing &amp; Guttering</title>
  <meta name="description" content="Practical gutter advice from 30 years working on Dublin roofs — when to clean, when to repair, when to replace, and what goes wrong on each type of Dublin house." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Open+Sans:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  <link rel="stylesheet" href="style.css" />
{HEAD_CSS}
{BLOG_CSS}
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Blog",
    "name": "Gutter Advice",
    "url": "https://dublingutter.ie/blog",
    "publisher": {{ "@type": "Organization", "name": "Recommended Roofing & Guttering" }},
    "blogPost": [
      {",".join(jsonstr({"@type":"BlogPosting","headline":p["title"],"url":f"https://dublingutter.ie/blog/{p['slug']}","datePublished":p["date"]}) for p in POSTS)}
    ]
  }}
  </script>
</head>
<body>
{topbar_header("Blog")}
  <section class="service-hero">
    <div class="container">
      <div class="breadcrumb"><a href="/">Home</a><span>/</span><span>Gutter Advice</span></div>
      <h1 style="color:var(--white);font-size:clamp(1.8rem,3.5vw,2.6rem);margin:14px 0 14px;">Gutter Advice for Dublin Homes</h1>
      <p style="color:rgba(255,255,255,0.85);max-width:62ch;font-size:1.05rem;">Thirty years on Dublin roofs, written down. No filler — just what actually goes wrong, why it goes wrong here, and what it takes to put right.</p>
    </div>
  </section>

  <section class="trust-bar">
    <div class="container trust-bar-inner">
      <div class="trust-item"><i class="fas fa-bolt"></i><div><strong>Same-Day Available</strong><span>7 days a week</span></div></div>
      <div class="trust-item"><i class="fas fa-hard-hat"></i><div><strong>30 Years Experience</strong><span>Trusted since 1994</span></div></div>
      <div class="trust-item"><i class="fas fa-tag"></i><div><strong>Upfront Pricing</strong><span>No hidden charges</span></div></div>
      <div class="trust-item"><i class="fab fa-google"></i><div><strong>20+ Google Reviews</strong><span>Rated 4.9 / 5 stars</span></div></div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="blog-grid">
        {cards}
      </div>
    </div>
  </section>

  <section class="cta-banner">
    <div class="container cta-inner">
      <div class="cta-text"><h2>Rather Just Ask Someone?</h2><p>Free quote and honest advice on your gutters, anywhere in Dublin.</p></div>
      <div class="cta-actions">
        <a href="tel:{PHONE_HREF}" class="btn btn-white"><i class="fas fa-phone"></i> {PHONE}</a>
        <a href="/quote" class="btn btn-outline-white">Get Free Quote</a>
      </div>
    </div>
  </section>
{FOOTER}"""


def main():
    os.makedirs(os.path.join(OUT, "blog"), exist_ok=True)
    open(os.path.join(OUT, "blog.html"), "w").write(blog_index())
    for p in POSTS:
        open(os.path.join(OUT, "blog", p["slug"] + ".html"), "w").write(post_page(p))
    print(f"blog index + {len(POSTS)} posts written")
    return [p["slug"] for p in POSTS]

if __name__ == "__main__":
    main()
