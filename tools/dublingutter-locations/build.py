# -*- coding: utf-8 -*-
"""Build the whole site in one command — areas, hubs, near-me, blog, sitemap.

Why this exists: `gen.main()` does NOT write the sitemap, and `gen.sitemap()`
needs the blog slugs, which only `blog.py` knows. So the sitemap was written by
hand, and the live sitemap had drifted from the repo more than once. Anything
that rebuilds this site must go through here, so the sitemap can never be one
build behind the pages.

    python3 build.py          # rebuild everything, then run the quality gates
    python3 build.py --skip-check
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gen
import blog

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    gen.main()
    slugs = blog.main()
    sitemap_path = os.path.join(gen.OUT, "sitemap.xml")
    with open(sitemap_path, "w") as fh:
        fh.write(gen.sitemap(extra_blog=slugs))
    print(f"sitemap written with {len(slugs)} blog url(s)")

    if "--skip-check" in sys.argv:
        return 0
    return subprocess.call([sys.executable, os.path.join(HERE, "check.py")], cwd=HERE)


if __name__ == "__main__":
    sys.exit(main())
