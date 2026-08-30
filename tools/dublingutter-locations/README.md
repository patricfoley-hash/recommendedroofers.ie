# dublingutter.ie — location & blog page generator

Generates the 78 area pages, the two regional hubs, `/near-me` and the blog for
**dublingutter.ie**. The generated HTML is committed in `../../dublingutter/`;
this directory is the source it comes from.

> This folder sits **outside** `dublingutter/`, so Cloudflare Pages
> (`root_dir: dublingutter`) never publishes it.

## Regenerate

```bash
cd tools/dublingutter-locations
python3 gen.py      # 78 area pages + 2 hubs + near-me
python3 blog.py     # blog index + posts
python3 check.py    # quality gates — run this before committing
```

`gen.py` also builds `sitemap.xml`. Nothing else in the site is touched, so it is
safe to re-run; output is deterministic and will overwrite cleanly.

Then commit and push to `main` — that triggers the Cloudflare `github:push` build.

## Files

| File | What it holds |
|------|---------------|
| `areas_north.py` | 30 North Dublin areas |
| `areas_south.py` | 48 South Dublin areas |
| `variants.py` | rotating phrasings for the shared scaffolding |
| `gen.py` | area page, hub page, `/near-me` and sitemap templates |
| `blog.py` | blog index, post template and post content |
| `check.py` | quality gates (`--live` also fetches every URL) |

## Adding an area

Append a dict to `NORTH` or `SOUTH`:

```python
dict(slug="ballybrack", name="Ballybrack", label="Co. Dublin", sub="South Dublin",
     char="What the housing stock is actually like.",
     cond="What that means for gutters — the local fault.",
     nb=["Killiney","Shankill","Cabinteely", ...],       # 9-12 nearby places
     revs=[("quote","Name S.","nearby area"), ...])      # exactly 3
```

Then `python3 gen.py && python3 check.py`.

`nb` entries that match another area's `name` become internal links automatically
— that is what builds the sideways interlinking, so use real neighbouring place
names.

## Things that will bite you

- **Slugs are flat** (`gutter-services-<area>`), not nested under the hub. Thirteen
  of these URLs were indexed before this build. **Do not restructure them.**
- **`check.py` enforces a similarity ceiling.** The first pass, before `variants.py`
  existed, scored a median 6-gram Jaccard of **0.363** between area pages and read
  as doorway pages. It is **0.128** now, and the gate fails above 0.22. If you add
  areas and it climbs, add more variants rather than raising the ceiling.
- **Write real local detail in `char` / `cond`.** They are the bulk of what makes
  each page distinct. Generic filler there defeats the whole exercise.
- **Cloudflare 403s non-browser user-agents.** A `urllib` sweep returns 403 on
  every URL including the homepage, which looks exactly like an outage. `check.py
  --live` sends a browser UA for this reason.
- `set(...)` ordering is not used anywhere that affects output — regeneration is
  byte-identical, so a rebuild with no data change produces no diff.
