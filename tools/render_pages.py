"""Render selected PDF pages to PNG for visual inspection."""
import os
import sys

import pymupdf

pdf = sys.argv[1]
outdir = sys.argv[2]
pages = [int(x) for x in sys.argv[3].split(",")]
os.makedirs(outdir, exist_ok=True)
doc = pymupdf.open(pdf)
for pno in pages:
    page = doc[pno - 1]
    pix = page.get_pixmap(dpi=110, alpha=False)
    path = os.path.join(outdir, f"page-{pno:04d}.png")
    pix.save(path)
    print(path, pix.width, "x", pix.height)
