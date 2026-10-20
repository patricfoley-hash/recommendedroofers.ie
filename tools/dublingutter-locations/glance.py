# -*- coding: utf-8 -*-
"""'At a Glance' answer box + named people for dublingutter.ie (Cited Page Swipe File, Patrick 2026-10-20).

Every figure and claim here is lifted from this site's OWN knowledge base
(Core repo: projects/dublin-gutter/knowledge-base/03-pricing.md, 07-faqs.md, 05-credentials-and-trust.md) — never
from recommendedroofing.ie or recommendedguttering.ie, whose gutter prices and call-out policy differ
(this site: NO call-out fee; the Guttering site charges a credited EUR150). Nothing is invented: a page with no
published price says it is quoted after a survey.

People (title only, never invented credentials): articles are authored by Patrick Foley, Business Owner;
Gerard O'Gorman is General Manager of Recommended Roofing and is named on town and service pages.
"""
import html as _html
import json as _json

OWNER = {"name": "Patrick Foley", "jobTitle": "Business Owner"}
MANAGER = {"name": "Gerard O'Gorman", "jobTitle": "General Manager"}
ORIGIN = "https://dublingutter.ie"


def _person(slug, p, works_for):
    return {"@type": "Person", "@id": f"{ORIGIN}/#{slug}", "name": p["name"], "jobTitle": p["jobTitle"],
            "worksFor": {"@type": "Organization", "name": works_for}}


PATRICK_NODE = _person("patrick-foley", OWNER, "Recommended Roofing & Guttering")
GERARD_NODE = _person("gerard-ogorman", MANAGER, "Recommended Roofing")
PATRICK_ID = PATRICK_NODE["@id"]
PATRICK_LD = _json.dumps(PATRICK_NODE, ensure_ascii=False)
GERARD_LD = _json.dumps(GERARD_NODE, ensure_ascii=False)

GUARANTEE_ALL = "Every job carries a 10-year written guarantee."
GUARANTEE_REPLACE = "Every job carries a 10-year written guarantee, and a full gutter replacement also carries our Lifetime Leak Guarantee."
FREE_LINE = "Quotes and inspections are free, with no call-out fee and a written breakdown before anything starts."


def _esc(s):
    return _html.escape(s, quote=False)


def box(heading, sentences):
    paras = "\n".join(f'        <p style="font-size:1.02rem;line-height:1.7;color:#334155;margin-bottom:8px">{_esc(t)}</p>' for t in sentences)
    return f'''  <section class="section" style="padding-top:28px;padding-bottom:8px">
    <div class="container">
      <div class="glance" style="background:#fff;border:1px solid #e2e8f0;border-left:4px solid #E11B22;padding:22px 26px;max-width:880px">
        <h2 style="font-size:clamp(1.3rem,2.2vw,1.8rem);margin-bottom:12px">{_esc(heading)}</h2>
{paras}
        <p style="font-size:.95rem;line-height:1.6;color:#64748b">Recommended Roofing is managed day to day by Gerard O&rsquo;Gorman, General Manager.</p>
      </div>
    </div>
  </section>
'''


def area_box(place):
    s1 = (f"In {place}, replacing the gutters on a typical semi (about 20 metres) costs €1,000–€1,400 in uPVC, "
          f"€1,300–€1,800 in aluminium and €2,100–€2,800 in cast iron, and a gutter repair starts at €500, with most between €1,000 and €1,900.")
    s2 = ("These are indicative prices: the length of run, the material, the height and access, and whether the fascia behind is sound all move them, "
          "and the figure is confirmed free after a survey. " + FREE_LINE)
    return box(f"Gutters {place} at a Glance", [s1, s2, GUARANTEE_REPLACE])


# Hand-written service pages: sentences from the same knowledge base, one set per page.
SERVICE_BOXES = {
    "gutter-repairs.html": [
        "Gutter repair starts at €500, and most repairs land between €1,000 and €1,900: a couple of leaking joints on one run is €500–€800, a typical repair (a sagging run re-aligned, brackets renewed, joints re-sealed, a downpipe) is €1,000–€1,900, and extensive or cast iron work is €1,900–€3,000.",
        FREE_LINE, GUARANTEE_ALL],
    "new-gutters.html": [
        "Replacing the gutters on a typical semi (about 20 metres) costs €1,000–€1,400 in uPVC, €1,300–€1,800 in aluminium and €2,100–€2,800 in cast iron; a larger or detached house (about 50 metres) costs €2,900–€3,600, €3,600–€4,500 and €5,500–€6,500.",
        "Prices include removing and disposing of the old system, new brackets, downpipes and outlets, and are confirmed free after a survey. " + FREE_LINE, GUARANTEE_REPLACE],
    "gutter-cleaning.html": [
        "Gutter cleaning is priced per job after a look at the house, because the size of the house, the height, the access and how much is up there all change the work; the downpipes are included.",
        FREE_LINE, GUARANTEE_ALL],
    "fascia-soffit.html": [
        "Fascia and soffit are priced with the guttering when the two are done together, which is the usual case because the gutter has to come off to reach the board, and doing both in one visit is considerably cheaper than doing them in two.",
        FREE_LINE, GUARANTEE_ALL],
    "downpipes.html": [
        "Downpipe repair and replacement is priced after we look at the job, because the number of pipes, the height and the access change the work.",
        FREE_LINE, GUARANTEE_ALL],
    "commercial-guttering.html": [
        "Commercial guttering is quoted per site after a survey, because box and valley gutters, large-diameter downpipes and access arrangements make per-metre rates meaningless on commercial work.",
        FREE_LINE, GUARANTEE_ALL],
}
