# -*- coding: utf-8 -*-
"""Rotating phrasings so 78 area pages don't read as one template with the name swapped.
Selection is deterministic per slug, so a page's wording is stable across rebuilds."""
import zlib
def pick(pool, slug, salt=0):
    return pool[(zlib.crc32((slug + "|" + str(salt)).encode()) % len(pool))]

HERO = [
 "Local gutter repair, cleaning and replacement for homes and businesses across {A} and the wider {S} area. Our teams know the local roads well and can often be with you the same day, with an upfront price agreed before any work starts.",
 "We've been repairing, clearing and replacing gutters across {A} for three decades. Whatever's going on with yours, we'll tell you straight what it needs, what it costs, and get it done without the runaround.",
 "Blocked, leaking or sagging gutters in {A}? We cover the whole of {S} with same-day call-outs where we can, a fixed price agreed before we start, and no call-out fee either way.",
 "From a single leaking joint to a full replacement, we handle gutter work of every size across {A}. Thirty years on {S} roofs means we've usually seen your problem before — and know the quickest honest fix.",
 "Gutter problems don't wait for a convenient moment. We run mobile teams throughout {S}, so if something's overflowing or hanging off in {A} we can usually be there today.",
 "Straightforward gutter work in {A} — repairs, cleaning, downpipes, fascia and soffit, and full replacements. Free quotes, a price agreed up front, and a guarantee on everything we do.",
]

BULLETS = [
 ["Same-day call-outs across {A} &amp; {S}", "Upfront price agreed before work starts",
  "30 years of gutter experience in {S}", "Fully insured &amp; guaranteed work"],
 ["No call-out fee anywhere in {A}", "Fixed quote before a tool comes out of the van",
  "Repairs first — we only replace when it's genuinely needed", "Fully insured, with all work guaranteed"],
 ["Covering every road in {A} and around it", "Emergency and storm damage handled same day",
  "Clear pricing with nothing added at the end", "Tidy work and a full clean-up afterwards"],
 ["Local teams working across {S} daily", "Free inspection and honest advice before you commit",
  "Three decades of Dublin gutter work behind us", "Insured, guaranteed and fully tax compliant"],
 ["Fast response throughout {A}", "You'll know the price before we begin",
  "We fix the cause, not just the symptom", "Guaranteed work — if it fails, we come back"],
]

SERVICE_COPY = {
 "Gutter Repairs": [
  "Leaking joints, sagging runs and loose brackets repaired fast across {A}. Same-day available.",
  "Cracked seals, dropped sections and gutters pulling off the fascia — all repaired properly in {A}.",
  "We fix the cause rather than patching the symptom, so {A} gutters keep working through the next storm.",
  "Most gutter faults in {A} are a repair, not a replacement. We'll tell you honestly which yours is.",
 ],
 "Gutter Cleaning": [
  "Leaves and moss block gutters fast around {A}. We clear and flush the full system.",
  "Full clear-out and flush of gutters, hoppers and downpipes anywhere in {A}.",
  "A blocked gutter is how water gets behind a fascia. We clear {A} gutters before that happens.",
  "Clearing, flushing and a check-over of the whole system — the {A} houses we do yearly never have trouble.",
 ],
 "New Gutters": [
  "Full PVC or aluminium gutter replacement in a range of colours to match your {A} home.",
  "When a system is past repair we replace it properly — measured, made to fit and colour matched in {A}.",
  "Complete replacement in PVC, aluminium or cast iron, sized correctly for your {A} roof.",
  "New gutters fitted to the right fall with enough downpipes to actually cope. Common sense, done right in {A}.",
 ],
 "Fascia &amp; Soffit": [
  "New uPVC fascia and soffit to smarten your roofline and stop water getting behind the gutter.",
  "Rotten boards replaced and the whole roofline made weatherproof again — a common job in {A}.",
  "Fascia and soffit renewal, usually done alongside the gutters so it's one visit and one price.",
  "Maintenance-free uPVC roofline that transforms how a house looks and keeps water out for good.",
 ],
 "Downpipes": [
  "Blocked, detached or damaged downpipes cleared, resecured or replaced anywhere in {A}.",
  "Undersized downpipes are behind a lot of {A} overflow problems. We size and fit them properly.",
  "Cracked, loose or blocked downpipes sorted — including rerouting discharge away from walls and drives.",
  "Downpipe repairs, replacements and additional pipes where one simply can't handle the roof.",
 ],
 "Commercial Guttering": [
  "Gutter services for shops, schools, offices and apartment blocks across {A}.",
  "Box gutters, valley gutters and internal outlets on commercial buildings in and around {A}.",
  "Scheduled maintenance and reactive repairs for {A} commercial property, fully insured and documented.",
  "Industrial and commercial roofs need a different approach to a house. We do both across {A}.",
 ],
}

WHY_BULLETS = [
 ["We cover {A} and all the surrounding areas", "Honest advice — we repair before we replace",
  "No call-out fee and no obligation to proceed", "Tidy work and full clean-up when we're done"],
 ["Local to {A}, so we're not charging you travel", "You get told what's actually wrong, not what sells",
  "A written price before anything starts", "Everything cleared away before we leave"],
 ["Working {A} roofs for three decades", "Repair recommended wherever repair will do",
  "Free inspection and quote, no strings", "Guaranteed work, in writing"],
 ["Familiar with the housing stock right across {A}", "Straight answers about what needs doing and what doesn't",
  "Fixed pricing agreed in advance", "Fully insured for your peace of mind"],
]

FAQ_COST = [
 "Every job is different, so we quote on-site after a quick inspection. There's no call-out fee and the price is agreed upfront before any work begins — no surprises on the bill.",
 "We price each job on what it actually needs rather than a flat rate. The inspection and quote are free, and whatever we quote is what you pay.",
 "It depends on the height, the length of the run and what's wrong. We'll look at it for free, give you a fixed price, and you decide from there.",
 "There's no standard price because no two roofs are the same. What we can promise is a free look, a firm figure before we start, and no extras added afterwards.",
]

FAQ_GUARANTEE = [
 "Yes — we're fully insured and all our work is guaranteed. If a repaired section fails, we'll come back and put it right at no charge.",
 "Fully insured, and everything we do is guaranteed. If something we've fixed gives trouble, we return and sort it for nothing.",
 "We carry full public liability insurance and guarantee our work. Paperwork is available on request before we start.",
 "Yes to both. Insurance details can be sent over before we come out, and the guarantee covers everything we install or repair.",
]

FAQ_SAMEDAY = [
 "In most cases, yes. We run mobile teams across {S}, so for urgent leaks or storm damage we can usually get to you the same day at no extra charge.",
 "Usually. We keep teams working across {S} every day, so an emergency in {A} can normally be seen the same day.",
 "Often, yes — especially for leaks and storm damage. Ring us and we'll tell you honestly whether we can reach you today or tomorrow.",
 "For anything urgent we'll do our best to get there the same day. There's no premium for an emergency call-out in {S}.",
]

CTA_SUB = [
 "Get a free, no-obligation quote today. Same-day service available across {A} and {S}.",
 "Free quote, fixed price, no call-out fee. We're working across {S} every day of the week.",
 "Tell us what's happening and we'll tell you what it needs. Free inspection anywhere in {A}.",
 "No obligation, no pressure, no call-out charge. Just a straight price for the work in {A}.",
]
