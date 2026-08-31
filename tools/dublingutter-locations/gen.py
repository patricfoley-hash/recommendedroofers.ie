# -*- coding: utf-8 -*-
import os, re, sys, html
sys.path.insert(0,'.')
from areas_north import NORTH
from areas_south import SOUTH
import variants as V

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "dublingutter")
PHONE, PHONE_HREF = "(01) 265 8463", "012658463"
HUBS = {"north": ("gutter-services-north-dublin", "North Dublin"),
        "south": ("gutter-services-south-dublin", "South Dublin")}

for a in NORTH: a["region"] = "north"
for a in SOUTH: a["region"] = "south"
ALL = NORTH + SOUTH
BY_SLUG = {a["slug"]: a for a in ALL}
# name -> slug, for turning neighbour names into internal links
NAME2SLUG = {a["name"].lower(): a["slug"] for a in ALL}
NAME2SLUG["dublin city centre"] = "city-centre"
NAME2SLUG["city centre"] = "city-centre"
NAME2SLUG["dun laoghaire"] = "dun-laoghaire"
NAME2SLUG["harold's cross"] = "harolds-cross"

PHOTOS = ["gutter-repairs-dublin.webp","gutter-cleaning-dublin.webp","downpipes-dublin.webp",
          "fascia-soffit-upvc-dublin.webp","fascia-soffit-repair-dublin.webp",
          "commercial-guttering-dublin.webp","new-gutters-dublin.webp"]
PHOTO_ALT = {
 "gutter-repairs-dublin.webp":"Gutter repair work on a Dublin home",
 "gutter-cleaning-dublin.webp":"Gutter cleaning and clearing on a Dublin house",
 "downpipes-dublin.webp":"New downpipe and gutter fitted to a Dublin home",
 "fascia-soffit-upvc-dublin.webp":"uPVC fascia, soffit and gutter on a Dublin roofline",
 "fascia-soffit-repair-dublin.webp":"Replacement fascia and soffit on a Dublin house",
 "commercial-guttering-dublin.webp":"Commercial guttering work in Dublin",
 "new-gutters-dublin.webp":"New gutters fitted to a Dublin home",
}

def esc(s): return html.escape(s, quote=False).replace("&amp;amp;","&amp;")

import json as _json
from urllib.parse import quote_plus
def jsonstr(x): return _json.dumps(x, ensure_ascii=False)

def siblings(a, n=8):
    """Nearby areas that have their own page — the sideways interlinks."""
    out, seen = [], {a["slug"]}
    for nb in a["nb"]:
        s = NAME2SLUG.get(nb.lower())
        if s and s not in seen:
            out.append(s); seen.add(s)
    if len(out) < n:   # top up from same sub-region, then same region
        for pool in (lambda x: x["sub"] == a["sub"], lambda x: x["region"] == a["region"]):
            for o in ALL:
                if len(out) >= n: break
                if pool(o) and o["slug"] not in seen:
                    out.append(o["slug"]); seen.add(o["slug"])
    return out[:n]

def local_area_cell(nb_name):
    """Neighbour chip — a link when that area has a page, plain text otherwise."""
    s = NAME2SLUG.get(nb_name.lower())
    if s:
        return f'<a href="/gutter-services-{s}" class="local-area"><i class="fas fa-map-marker-alt"></i> {esc(nb_name)}</a>'
    return f'<div class="local-area"><i class="fas fa-map-marker-alt"></i> {esc(nb_name)}</div>'

SERVICES = [
 ("/gutter-repairs","fa-wrench","Gutter Repairs","Leaking joints, sagging runs and loose brackets repaired fast across {A}. Same-day available."),
 ("/gutter-cleaning","fa-broom","Gutter Cleaning","Leaves and moss block gutters fast around {A}. We clear and flush the full system."),
 ("/new-gutters","fa-plus","New Gutters","Full PVC or aluminium gutter replacement in a range of colours to match your {A} home."),
 ("/fascia-soffit","fa-house-chimney","Fascia &amp; Soffit","New uPVC fascia and soffit to smarten your roofline and stop water getting behind the gutter."),
 ("/downpipes","fa-arrows-down-to-line","Downpipes","Blocked, detached or damaged downpipes cleared, resecured or replaced anywhere in {A}."),
 ("/commercial-guttering","fa-building","Commercial Guttering","Gutter services for shops, schools, offices and apartment blocks across {A}."),
]

HEAD_CSS = """  <style>
    .service-hero { padding: 60px 0; }   /* background lives in style.css */
    .service-hero-inner { display: grid; grid-template-columns: 1fr 380px; gap: 50px; align-items: center; }
    .service-hero-content .breadcrumb { justify-content: flex-start; margin-bottom: 16px; }
    .service-hero-content h1 { color: var(--white); font-size: clamp(1.8rem, 3.5vw, 2.6rem); margin-bottom: 14px; }
    .service-hero-content p { color: rgba(255,255,255,0.85); font-size: 1.05rem; margin-bottom: 24px; line-height: 1.7; }
    .service-hero-bullets { display: flex; flex-direction: column; gap: 10px; margin-bottom: 28px; }
    .service-hero-bullets li { display: flex; align-items: center; gap: 10px; color: var(--white); font-size: 0.95rem; }
    .service-hero-bullets i { color: var(--yellow); }
    .service-hero-ctas { display: flex; gap: 12px; flex-wrap: wrap; }
    .service-hero-form { background: var(--white); border-radius: var(--radius-lg); padding: 14px; }
    .content-split { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; }
    .content-split-img { background: var(--blue-xlight); border-radius: var(--radius-lg); aspect-ratio: 16/9; display: flex; align-items: center; justify-content: center; overflow: hidden; }
    .content-split-img img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .content-split-text h2 { font-size: 1.7rem; margin-bottom: 14px; }
    .content-split-text p { color: var(--grey); margin-bottom: 14px; line-height: 1.75; }
    .content-split-text ul { display: flex; flex-direction: column; gap: 9px; margin-bottom: 24px; }
    .content-split-text li { display: flex; align-items: flex-start; gap: 10px; font-size: 0.92rem; color: var(--text); }
    .content-split-text li i { color: var(--yellow-dark); margin-top: 3px; flex-shrink: 0; }
    .local-areas { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; }
    .local-area { display: flex; align-items: center; gap: 10px; background: var(--white); border: 1.5px solid var(--border); border-radius: var(--radius); padding: 14px 16px; font-size: 0.9rem; font-weight: 600; color: var(--grey-dark); text-decoration: none; transition: all var(--transition); }
    a.local-area:hover { border-color: var(--blue); color: var(--blue); transform: translateY(-2px); box-shadow: var(--shadow); }
    .local-area i { color: var(--blue); }
    .nearby-links { display: flex; flex-wrap: wrap; gap: 10px; }
    .nearby-link { display: inline-flex; align-items: center; gap: 7px; background: var(--white); border: 1.5px solid var(--border); border-radius: 100px; padding: 9px 16px; font-size: 0.88rem; font-weight: 600; color: var(--grey-dark); text-decoration: none; transition: all var(--transition); }
    .nearby-link:hover { border-color: var(--blue); color: var(--blue); }
    .nearby-link i { color: var(--yellow-dark); font-size: 0.8rem; }
    @media (max-width: 1024px) {
      .service-hero-inner { grid-template-columns: 1fr; }
      .content-split { grid-template-columns: 1fr; }
    }
  </style>"""

def topbar_header(active):
    nav = ""
    for href, label in [("/","Home"),("/services","Services"),("/near-me","Near Me"),
                        ("/blog","Blog"),("/about","About"),("/contact","Contact")]:
        cls = "nav-link active" if label == active else "nav-link"
        nav += f'\n        <a href="{href}" class="{cls}">{label}</a>'
    return f"""
  <div class="topbar">
    <div class="container topbar-inner">
      <div class="topbar-left">
        <span><i class="fas fa-phone"></i> {PHONE}</span>
        <span><i class="fas fa-envelope"></i> info@recommendedroofing.ie</span>
      </div>
      <div class="topbar-right">
        <span><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i><i class="fas fa-star"></i> 4.9 Google Reviews</span>
        <span><i class="fas fa-shield-halved"></i> Fully Insured</span>
      </div>
    </div>
  </div>

  <header class="header" id="header">
    <div class="container header-inner">
      <a href="/" class="logo"><img src="images/logo-recommended-roofing.svg" alt="Recommended Roofing &amp; Guttering" height="80" /></a>
      <nav class="nav" id="nav">{nav}
      </nav>
      <a href="/quote" class="btn btn-primary header-cta">Get Free Quote</a>
      <button class="hamburger" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </header>
"""

FOOTER = """
  <footer class="footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <a href="/" class="logo logo-light"><img src="images/logo-recommended-roofing.svg" alt="Recommended Roofing &amp; Guttering" height="80" /></a>
        <p>Dublin's trusted gutter repair and replacement experts. Serving homeowners and businesses across Dublin for over 30 years.</p>
        <div class="footer-social"><a href="#"><i class="fab fa-facebook-f"></i></a><a href="#"><i class="fab fa-google"></i></a></div>
      </div>
      <div class="footer-col"><h4>Services</h4><ul><li><a href="/gutter-repairs">Gutter Repairs</a></li><li><a href="/gutter-cleaning">Gutter Cleaning</a></li><li><a href="/new-gutters">New Gutters</a></li><li><a href="/fascia-soffit">Fascia &amp; Soffit</a></li><li><a href="/downpipes">Downpipes Repair</a></li><li><a href="/commercial-guttering">Commercial Guttering</a></li></ul></div>
      <div class="footer-col"><h4>Areas We Cover</h4><ul><li><a href="/gutter-services-north-dublin">North Dublin</a></li><li><a href="/gutter-services-south-dublin">South Dublin</a></li><li><a href="/near-me">All Areas</a></li><li><a href="/blog">Gutter Advice</a></li><li><a href="/about">About Us</a></li><li><a href="/contact">Contact</a></li></ul></div>
      <div class="footer-col"><h4>Contact Us</h4><ul class="footer-contact"><li><i class="fas fa-phone"></i> <a href="tel:012658463">(01) 265 8463</a></li><li><i class="fas fa-envelope"></i> <a href="mailto:info@recommendedroofing.ie">info@recommendedroofing.ie</a></li><li><i class="fas fa-map-marker-alt"></i> 24A Baggot Street Upper, Dublin 4, D04 N528</li><li><i class="fas fa-clock"></i> Mon&ndash;Sun: 7am&ndash;9pm</li></ul></div>
    </div>
    <div class="footer-bottom"><div class="container"><p>&copy; 2026 Recommended Roofing &amp; Guttering — All rights reserved.</p><p><a href="#">Privacy Policy</a> | <a href="#">Terms</a></p></div></div>
  </footer>

  <div class="float-ctas">
    <a href="tel:012658463" class="float-btn float-phone"><i class="fas fa-phone"></i></a>
    <a href="https://wa.me/35312658463" class="float-btn float-whatsapp"><i class="fab fa-whatsapp"></i></a>
  </div>

  <script>
    window.addEventListener('scroll', () => { document.getElementById('header').classList.toggle('scrolled', window.scrollY > 50); });
    document.getElementById('hamburger').addEventListener('click', () => { document.getElementById('nav').classList.toggle('open'); document.getElementById('hamburger').classList.toggle('active'); });
    function toggleFaq(btn) { const item = btn.parentElement; const isOpen = item.classList.contains('open'); document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open')); if (!isOpen) item.classList.add('open'); }
  </script>
</body>
</html>
"""

QUOTE_FORM = """<iframe
            src="https://api.twolabsleadgen.com/widget/form/b3qFYv3eyajJCp7nJblw"
            style="width:100%;height:493px;border:none;border-radius:var(--radius-lg)"
            id="inline-b3qFYv3eyajJCp7nJblw"
            data-layout="{'id':'INLINE'}"
            data-trigger-type="alwaysShow" data-trigger-value=""
            data-activation-type="alwaysActivated" data-activation-value=""
            data-deactivation-type="neverDeactivate" data-deactivation-value=""
            data-form-name="Quotation Form" data-height="493"
            data-layout-iframe-id="inline-b3qFYv3eyajJCp7nJblw"
            data-form-id="b3qFYv3eyajJCp7nJblw" title="Quotation Form">
          </iframe>
          <script src="https://api.twolabsleadgen.com/js/form_embed.js"></script>"""

STARS = '<i class="fas fa-star"></i>' * 5

def area_page(a, i):
    A, slug = a["name"], a["slug"]
    hub_slug, hub_name = HUBS[a["region"]]
    label = a.get("label","")
    title_loc = f"{A} ({label})" if label and label.startswith("Dublin") else A
    h1 = f"Gutter Services in {A}" + (f", {label}" if label else "")
    photo = PHOTOS[i % len(PHOTOS)]
    sibs = siblings(a)
    nb_disp = a["nb"][:12]

    fmt = dict(A=esc(A), S=esc(a["sub"]))
    hero_p = V.pick(V.HERO, slug).format(**fmt)
    hero_bullets = "\n".join(
        f'          <li><i class="fas fa-check-circle"></i> {b.format(**fmt)}</li>'
        for b in V.pick(V.BULLETS, slug))
    why_bullets = "\n".join(
        f'          <li><i class="fas fa-check"></i> {b.format(**fmt)}</li>'
        for b in V.pick(V.WHY_BULLETS, slug, 1))
    cta_sub = V.pick(V.CTA_SUB, slug, 2).format(**fmt)

    svc_cards = "\n        ".join(
        f'<a href="{h}" class="service-card"><div class="service-icon"><i class="fas {ic}"></i></div>'
        f'<h3>{nm}</h3><p>{V.pick(V.SERVICE_COPY[nm], slug, nm).format(**fmt)}</p>'
        f'<span class="service-link">Learn more <i class="fas fa-arrow-right"></i></span></a>'
        for h, ic, nm, tx in SERVICES)

    area_cells = "\n        ".join(local_area_cell(x) for x in nb_disp)
    sib_links = "\n        ".join(
        f'<a href="/gutter-services-{s}" class="nearby-link"><i class="fas fa-location-dot"></i> {esc(BY_SLUG[s]["name"])}</a>'
        for s in sibs)

    revs = "\n        ".join(
        f'<div class="review-card"><div class="review-stars">{STARS}</div>'
        f'<p>&ldquo;{esc(q)}&rdquo;</p><div class="review-author"><div class="review-avatar">{esc(nm[0])}</div>'
        f'<div><strong>{esc(nm)}</strong><span>{esc(ar)}</span></div></div></div>'
        for q, nm, ar in a["revs"])

    area_served = ",\n      ".join(
        '{ "@type": "Place", "name": "%s" }' % esc(x) for x in ([title_loc] + nb_disp[:6]))

    faqs = [
      (f"Do you cover all of {A}?",
       f"Yes — we cover {A} and the surrounding areas including {', '.join(nb_disp[:4])}. If you're nearby and unsure, just give us a call."),
      (f"Can you come out same-day in {A}?",
       V.pick(V.FAQ_SAMEDAY, slug, 3).format(**fmt)),
      ("How much does a gutter repair cost?",
       V.pick(V.FAQ_COST, slug, 4)),
      (f"What causes most gutter problems in {A}?",
       esc(a["cond"])),
      ("Are you insured and is the work guaranteed?",
       V.pick(V.FAQ_GUARANTEE, slug, 5)),
    ]
    faq_html = "\n        ".join(
        f'<div class="faq-item"><button class="faq-q" onclick="toggleFaq(this)">{esc(q)} <i class="fas fa-plus"></i></button>'
        f'<div class="faq-a"><p>{aa}</p></div></div>' for q, aa in faqs)
    faq_ld = ",\n      ".join(
        '{ "@type": "Question", "name": %s, "acceptedAnswer": { "@type": "Answer", "text": %s } }'
        % (jsonstr(q), jsonstr(re.sub(r"<[^>]+>", "", aa))) for q, aa in faqs)

    meta_desc = (f"Gutter repairs, cleaning and replacement in {A}{', ' + label if label else ''}. "
                 f"Same-day call-outs across {', '.join(nb_disp[:4])}. Free quotes, upfront pricing.")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="canonical" href="https://dublingutter.ie/gutter-services-{slug}" />
  <title>Gutter Services {title_loc} | Repairs, Cleaning &amp; New Gutters | Recommended Roofing &amp; Guttering</title>
  <meta name="description" content="{esc(meta_desc)}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Open+Sans:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  <link rel="stylesheet" href="style.css" />
{HEAD_CSS}
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
    {{
      "@type": "LocalBusiness",
      "name": "Recommended Roofing & Guttering — {esc(A)}",
      "image": "https://dublingutter.ie/images/logo-recommended-roofing.svg",
      "url": "https://dublingutter.ie/gutter-services-{slug}",
      "telephone": "+35312658463",
      "email": "info@recommendedroofing.ie",
      "priceRange": "€€",
      "address": {{ "@type": "PostalAddress", "streetAddress": "24A Baggot Street Upper", "addressLocality": "Dublin", "postalCode": "D04 N528", "addressCountry": "IE" }},
      "areaServed": [
      {area_served}
      ],
      "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "5", "reviewCount": "20" }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://dublingutter.ie/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Areas We Cover", "item": "https://dublingutter.ie/near-me" }},
        {{ "@type": "ListItem", "position": 3, "name": "{hub_name}", "item": "https://dublingutter.ie/{hub_slug}" }},
        {{ "@type": "ListItem", "position": 4, "name": "{esc(A)}", "item": "https://dublingutter.ie/gutter-services-{slug}" }}
      ]
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
      {faq_ld}
      ]
    }}
    ]
  }}
  </script>
</head>
<body>
{topbar_header("Near Me")}
  <section class="service-hero">
    <div class="container service-hero-inner">
      <div class="service-hero-content">
        <div class="breadcrumb"><a href="/">Home</a><span>/</span><a href="/near-me">Areas</a><span>/</span><a href="/{hub_slug}">{hub_name}</a><span>/</span><span>{esc(A)}</span></div>
        <h1>{esc(h1)}</h1>
        <p>{hero_p}</p>
        <ul class="service-hero-bullets">
{hero_bullets}
        </ul>
        <div class="service-hero-ctas">
          <a href="/quote" class="btn btn-primary"><i class="fas fa-paper-plane"></i> Get Free Quote</a>
          <a href="tel:{PHONE_HREF}" class="btn btn-outline-white"><i class="fas fa-phone"></i> {PHONE}</a>
        </div>
      </div>
      <div class="service-hero-form">
          {QUOTE_FORM}
      </div>
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
    <div class="container content-split">
      <div class="content-split-text">
        <span class="section-tag">Your Local Gutter Team</span>
        <h2>Trusted Gutter Specialists in {esc(A)}</h2>
        <p>{esc(a['char'])}</p>
        <p>{esc(a['cond'])}</p>
        <ul>
{why_bullets}
        </ul>
        <a href="/quote" class="btn btn-primary">Get a Free Quote</a>
      </div>
      <div class="content-split-img"><img src="/images/services/{photo}" alt="{esc(PHOTO_ALT[photo])} in {esc(A)}" width="1200" height="675" loading="lazy" decoding="async" /></div>
    </div>
  </section>

  <section class="section section-light">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Our Services</span>
        <h2>Gutter Services We Offer in {esc(A)}</h2>
        <p>Our full range of gutter services is available right across {esc(A)} and nearby</p>
      </div>
      <div class="services-grid">
        {svc_cards}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Local Coverage</span>
        <h2>Areas We Cover Around {esc(A)}</h2>
        <p>If you're in or near any of these areas, we can help</p>
      </div>
      <div class="local-areas">
        {area_cells}
      </div>
      <p class="areas-note" style="margin-top: 28px;">Not sure if we reach you? <a href="/contact">Contact us</a> — we cover {esc(A)} and all of {hub_name}.</p>
    </div>
  </section>

  <section class="section section-light">
    <div class="container">
      <div class="section-header"><span class="section-tag">Reviews</span><h2>What {esc(A)} Customers Say</h2></div>
      <div class="reviews-grid">
        {revs}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-header"><span class="section-tag">FAQ</span><h2>{esc(A)} Gutter Questions</h2></div>
      <div class="faq-grid">
        {faq_html}
      </div>
    </div>
  </section>

  <section class="section section-light">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Nearby</span>
        <h2>Gutter Services Near {esc(A)}</h2>
        <p>We work right across {hub_name} — here are the areas closest to {esc(A)}</p>
      </div>
      <div class="nearby-links">
        {sib_links}
      </div>
      <p class="areas-note" style="margin-top: 28px;">See every area we cover in <a href="/{hub_slug}">{hub_name}</a>, or browse <a href="/near-me">all Dublin areas</a>.</p>
    </div>
  </section>

  <section class="cta-banner">
    <div class="container cta-inner">
      <div class="cta-text"><h2>Need a Gutter Expert in {esc(A)}?</h2><p>{cta_sub}</p></div>
      <div class="cta-actions">
        <a href="tel:{PHONE_HREF}" class="btn btn-white"><i class="fas fa-phone"></i> {PHONE}</a>
        <a href="/quote" class="btn btn-outline-white">Get Free Quote</a>
      </div>
    </div>
  </section>

  <section class="map-section">
    <iframe src="https://www.google.com/maps?q={quote_plus(A + ', Dublin, Ireland')}&amp;output=embed" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="{esc(A)}"></iframe>
  </section>
{FOOTER}"""


HUB_COPY = {
 "north": dict(
  intro="North Dublin runs from the Georgian terraces of the north inner city out through the big post-war suburbs and on to the coastal towns of Fingal. We cover all of it — the red-brick roads of Clontarf and Drumcondra, the estate housing of Coolock, Finglas and Donaghmede, the Dublin 15 sprawl around Blanchardstown, and the seaside towns from Howth up to Balbriggan.",
  cond="Two things shape gutter work on the northside. The coast — from Clontarf round to Malahide and Portmarnock — brings salt air that corrodes brackets and fixings far faster than inland, so we use marine-grade fixings as standard on those jobs. Inland, the great 1930s to 1970s housing schemes were built at the same time and are now reaching the end of their gutter life together, which is why we do so many full replacements across Cabra, Crumlin's northside equivalents, Artane and Coolock.",
  q="North Dublin"),
 "south": dict(
  intro="South Dublin covers an enormous range — the Victorian red-brick of Rathmines, Rathgar and Donnybrook, the coastal towns from Sandymount down to Dalkey and Shankill, the mid-century suburbs of Stillorgan, Mount Merrion and Goatstown, and the big western estates through Tallaght, Clondalkin and Lucan. We work across all of it.",
  cond="The southside splits into three kinds of gutter work. Period property in Dublin 4, 6 and along the coast means cast iron, parapet gutters and hidden valleys — work that needs proper access and judgement rather than a ladder and sealant. The mid-century suburbs are on their second gutter system, usually with heavy leaf load from mature planting. And the western estates at Tallaght, Clondalkin and Knocklyon were built to a common pattern and are all reaching replacement age at once.",
  q="South Dublin"),
}

def hub_page(region):
    slug, name = HUBS[region]
    areas = sorted([a for a in ALL if a["region"] == region], key=lambda x: x["name"])
    copy = HUB_COPY[region]
    other = HUBS["south" if region == "north" else "north"]

    by_sub = {}
    for a in areas: by_sub.setdefault(a["sub"], []).append(a)
    groups = ""
    for sub in sorted(by_sub):
        cards = "\n        ".join(
            f'<a href="/gutter-services-{a["slug"]}" class="area-card">'
            f'<div class="area-icon"><i class="fas fa-map-marker-alt"></i></div>'
            f'<h3>{esc(a["name"])}</h3><p>{esc(a["label"] or name)}</p>'
            f'<span class="area-link">Gutter services <i class="fas fa-arrow-right"></i></span></a>'
            for a in by_sub[sub])
        groups += f"""
      <h3 class="area-group-title">{esc(sub)}</h3>
      <div class="areas-grid">
        {cards}
      </div>
"""
    svc_cards = "\n        ".join(
        f'<a href="{h}" class="service-card"><div class="service-icon"><i class="fas {ic}"></i></div>'
        f'<h3>{nm}</h3><p>{tx.format(A=name)}</p>'
        f'<span class="service-link">Learn more <i class="fas fa-arrow-right"></i></span></a>'
        for h, ic, nm, tx in SERVICES)
    listed = ",\n      ".join('{ "@type": "Place", "name": %s }' % jsonstr(a["name"]) for a in areas)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="canonical" href="https://dublingutter.ie/{slug}" />
  <title>Gutter Services {name} | Repairs, Cleaning &amp; Replacement | Recommended Roofing &amp; Guttering</title>
  <meta name="description" content="Gutter repairs, cleaning and replacement across {name}. Covering {len(areas)} areas with same-day call-outs, upfront pricing and 30 years' experience. Free quotes." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Open+Sans:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  <link rel="stylesheet" href="style.css" />
{HEAD_CSS}
  <style>
    .areas-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 18px; margin-bottom: 40px; }}
    .area-card {{ background: var(--white); border: 1.5px solid var(--border); border-radius: var(--radius-lg); padding: 22px; text-decoration: none; color: inherit; transition: all var(--transition); display: flex; flex-direction: column; }}
    .area-card:hover {{ border-color: var(--blue); box-shadow: var(--shadow); transform: translateY(-3px); }}
    .area-icon {{ width: 42px; height: 42px; background: var(--blue-xlight); border-radius: 10px; display: grid; place-items: center; margin-bottom: 12px; }}
    .area-icon i {{ color: var(--blue); }}
    .area-card h3 {{ font-size: 1rem; color: var(--grey-dark); margin-bottom: 4px; }}
    .area-card p {{ font-size: 0.82rem; color: var(--grey); flex: 1; }}
    .area-link {{ margin-top: 12px; font-size: 0.82rem; font-weight: 600; color: var(--yellow-dark); font-family: 'Poppins', sans-serif; display: flex; align-items: center; gap: 6px; }}
    .area-group-title {{ font-size: 1.15rem; color: var(--grey-dark); margin: 8px 0 18px; padding-bottom: 10px; border-bottom: 2px solid var(--blue-light); }}
  </style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
    {{
      "@type": "LocalBusiness",
      "name": "Recommended Roofing & Guttering — {name}",
      "image": "https://dublingutter.ie/images/logo-recommended-roofing.svg",
      "url": "https://dublingutter.ie/{slug}",
      "telephone": "+35312658463",
      "email": "info@recommendedroofing.ie",
      "priceRange": "€€",
      "address": {{ "@type": "PostalAddress", "streetAddress": "24A Baggot Street Upper", "addressLocality": "Dublin", "postalCode": "D04 N528", "addressCountry": "IE" }},
      "areaServed": [
      {listed}
      ],
      "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "5", "reviewCount": "20" }}
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://dublingutter.ie/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Areas We Cover", "item": "https://dublingutter.ie/near-me" }},
        {{ "@type": "ListItem", "position": 3, "name": "{name}", "item": "https://dublingutter.ie/{slug}" }}
      ]
    }}
    ]
  }}
  </script>
</head>
<body>
{topbar_header("Near Me")}
  <section class="service-hero">
    <div class="container service-hero-inner">
      <div class="service-hero-content">
        <div class="breadcrumb"><a href="/">Home</a><span>/</span><a href="/near-me">Areas</a><span>/</span><span>{name}</span></div>
        <h1>Gutter Services in {name}</h1>
        <p>{esc(copy['intro'])}</p>
        <ul class="service-hero-bullets">
          <li><i class="fas fa-check-circle"></i> {len(areas)} areas covered across {name}</li>
          <li><i class="fas fa-check-circle"></i> Same-day call-outs, 7 days a week</li>
          <li><i class="fas fa-check-circle"></i> Upfront price agreed before work starts</li>
          <li><i class="fas fa-check-circle"></i> Fully insured &amp; guaranteed work</li>
        </ul>
        <div class="service-hero-ctas">
          <a href="/quote" class="btn btn-primary"><i class="fas fa-paper-plane"></i> Get Free Quote</a>
          <a href="tel:{PHONE_HREF}" class="btn btn-outline-white"><i class="fas fa-phone"></i> {PHONE}</a>
        </div>
      </div>
      <div class="service-hero-form">
          {QUOTE_FORM}
      </div>
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
      <div class="section-header">
        <span class="section-tag">Local Knowledge</span>
        <h2>What Gutters Are Like in {name}</h2>
      </div>
      <div style="max-width: 78ch; margin: 0 auto; text-align: center;">
        <p style="color: var(--grey); line-height: 1.8;">{esc(copy['cond'])}</p>
      </div>
    </div>
  </section>

  <section class="section section-light">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Areas We Cover</span>
        <h2>Gutter Services Across {name}</h2>
        <p>Pick your area for local details, or call us and we'll tell you straight away</p>
      </div>
{groups}
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Our Services</span>
        <h2>What We Do Across {name}</h2>
      </div>
      <div class="services-grid">
        {svc_cards}
      </div>
    </div>
  </section>

  <section class="cta-banner">
    <div class="container cta-inner">
      <div class="cta-text"><h2>Need a Gutter Expert in {name}?</h2><p>Free, no-obligation quotes. Same-day service available across all {len(areas)} areas.</p></div>
      <div class="cta-actions">
        <a href="tel:{PHONE_HREF}" class="btn btn-white"><i class="fas fa-phone"></i> {PHONE}</a>
        <a href="/quote" class="btn btn-outline-white">Get Free Quote</a>
      </div>
    </div>
  </section>

  <section class="section section-light">
    <div class="container">
      <div class="section-header"><h2>Also Covering {other[1]}</h2>
      <p>We work on both sides of the Liffey — see our <a href="/{other[0]}">{other[1]}</a> areas, or <a href="/near-me">every area we cover</a>.</p></div>
    </div>
  </section>
{FOOTER}"""


def near_me_page():
    blocks = ""
    for region in ("north","south"):
        slug, name = HUBS[region]
        areas = sorted([a for a in ALL if a["region"]==region], key=lambda x: x["name"])
        cards = "\n        ".join(
            f'<a href="/gutter-services-{a["slug"]}" class="area-card">'
            f'<div class="area-icon"><i class="fas fa-map-marker-alt"></i></div>'
            f'<h3>{esc(a["name"])}</h3><p>{esc(a["label"] or name)}</p>'
            f'<span class="area-link">Gutter services <i class="fas fa-arrow-right"></i></span></a>'
            for a in areas)
        blocks += f"""
      <div class="region-block">
        <div class="region-head">
          <h2>{name}</h2>
          <a href="/{slug}" class="btn btn-outline-blue">All {name} <i class="fas fa-arrow-right"></i></a>
        </div>
        <p class="region-sub">{len(areas)} areas covered across {name}</p>
        <div class="areas-grid">
        {cards}
        </div>
      </div>
"""
    svc_cards = "\n        ".join(
        f'<a href="{h}" class="service-card"><div class="service-icon"><i class="fas {ic}"></i></div>'
        f'<h3>{nm}</h3><p>{tx.format(A="Dublin")}</p>'
        f'<span class="service-link">Learn more <i class="fas fa-arrow-right"></i></span></a>'
        for h, ic, nm, tx in SERVICES)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="canonical" href="https://dublingutter.ie/near-me" />
  <title>Gutter Services Near Me — All Dublin Areas | Recommended Roofing &amp; Guttering</title>
  <meta name="description" content="Gutter repairs, cleaning and replacement across {len(ALL)} areas of North and South Dublin. Find your area for local details. Same-day call-outs, free quotes." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Open+Sans:wght@400;500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  <link rel="stylesheet" href="style.css" />
{HEAD_CSS}
  <style>
    .areas-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 18px; }}
    .area-card {{ background: var(--white); border: 1.5px solid var(--border); border-radius: var(--radius-lg); padding: 22px; text-decoration: none; color: inherit; transition: all var(--transition); display: flex; flex-direction: column; }}
    .area-card:hover {{ border-color: var(--blue); box-shadow: var(--shadow); transform: translateY(-3px); }}
    .area-icon {{ width: 42px; height: 42px; background: var(--blue-xlight); border-radius: 10px; display: grid; place-items: center; margin-bottom: 12px; }}
    .area-icon i {{ color: var(--blue); }}
    .area-card h3 {{ font-size: 1rem; color: var(--grey-dark); margin-bottom: 4px; }}
    .area-card p {{ font-size: 0.82rem; color: var(--grey); flex: 1; }}
    .area-link {{ margin-top: 12px; font-size: 0.82rem; font-weight: 600; color: var(--yellow-dark); font-family: 'Poppins', sans-serif; display: flex; align-items: center; gap: 6px; }}
    .region-block {{ margin-bottom: 60px; }}
    .region-head {{ display: flex; align-items: center; justify-content: space-between; gap: 20px; flex-wrap: wrap; padding-bottom: 12px; border-bottom: 2px solid var(--blue-light); margin-bottom: 8px; }}
    .region-head h2 {{ font-size: 1.6rem; margin: 0; }}
    .region-sub {{ color: var(--grey); font-size: 0.9rem; margin-bottom: 22px; }}
  </style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://dublingutter.ie/" }},
      {{ "@type": "ListItem", "position": 2, "name": "Areas We Cover", "item": "https://dublingutter.ie/near-me" }}
    ]
  }}
  </script>
</head>
<body>
{topbar_header("Near Me")}
  <section class="service-hero">
    <div class="container service-hero-inner">
      <div class="service-hero-content">
        <div class="breadcrumb"><a href="/">Home</a><span>/</span><span>Areas We Cover</span></div>
        <h1>Gutter Services Near Me — All Dublin Areas</h1>
        <p>We cover {len(ALL)} areas across Dublin, north and south of the Liffey, plus the nearest commuter towns. Find your area below for local detail, or just call us — if you're in Dublin, we cover you.</p>
        <div class="service-hero-ctas">
          <a href="/gutter-services-north-dublin" class="btn btn-primary"><i class="fas fa-location-dot"></i> North Dublin</a>
          <a href="/gutter-services-south-dublin" class="btn btn-outline-white"><i class="fas fa-location-dot"></i> South Dublin</a>
        </div>
      </div>
      <div class="service-hero-form">
          {QUOTE_FORM}
      </div>
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
{blocks}
    </div>
  </section>

  <section class="section section-light">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Our Services</span>
        <h2>Services Available in Your Area</h2>
        <p>Whatever part of Dublin you're in, this is what we do</p>
      </div>
      <div class="services-grid">
        {svc_cards}
      </div>
    </div>
  </section>

  <section class="cta-banner">
    <div class="container cta-inner">
      <div class="cta-text"><h2>Find a Gutter Expert Near You</h2><p>Free quotes across every Dublin area. Same-day call-outs available.</p></div>
      <div class="cta-actions">
        <a href="tel:{PHONE_HREF}" class="btn btn-white"><i class="fas fa-phone"></i> {PHONE}</a>
        <a href="/quote" class="btn btn-outline-white">Get Free Quote</a>
      </div>
    </div>
  </section>
{FOOTER}"""


STATIC = ["", "services", "near-me", "about", "contact", "quote", "blog",
          "gutter-repairs", "gutter-cleaning", "new-gutters", "fascia-soffit",
          "downpipes", "commercial-guttering"]

def sitemap(extra_blog=()):
    from datetime import date
    d = date.today().isoformat()
    urls = []
    def add(loc, pri, freq="monthly"):
        urls.append(f"  <url>\n    <loc>https://dublingutter.ie/{loc}</loc>\n"
                    f"    <lastmod>{d}</lastmod>\n    <changefreq>{freq}</changefreq>\n"
                    f"    <priority>{pri}</priority>\n  </url>")
    add("", "1.0", "weekly")
    for p in STATIC[1:]:
        add(p, "0.9" if p in ("services", "near-me", "blog") else "0.8")
    for r in ("north", "south"):
        add(HUBS[r][0], "0.9")
    for a in sorted(ALL, key=lambda x: x["slug"]):
        add(f"gutter-services-{a['slug']}", "0.7")
    for b in extra_blog:
        add(f"blog/{b}", "0.6", "weekly")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def main():
    written = []
    for i, a in enumerate(ALL):
        p = os.path.join(OUT, f"gutter-services-{a['slug']}.html")
        open(p, "w").write(area_page(a, i)); written.append(p)
    for r in ("north", "south"):
        p = os.path.join(OUT, HUBS[r][0] + ".html")
        open(p, "w").write(hub_page(r)); written.append(p)
    p = os.path.join(OUT, "near-me.html")
    open(p, "w").write(near_me_page()); written.append(p)
    print(f"{len(written)} pages written ({len(ALL)} areas + 2 hubs + near-me)")
    return written


if __name__ == "__main__":
    main()
