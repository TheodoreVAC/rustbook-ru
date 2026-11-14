"""Render every figure of the book to a high-resolution PNG.

Raster figures are extracted at their native resolution; vector figures are
rendered from the PDF page at 300 dpi so that the original artwork is
reproduced exactly.
"""
import json
import os
import sys
import pymupdf

PDF = sys.argv[1]
JSON = sys.argv[2]
OUT = sys.argv[3]
DPI = int(sys.argv[4]) if len(sys.argv) > 4 else 300

os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)
blocks = json.load(open(JSON, encoding="utf-8"))["blocks"]

index = []
for b in blocks:
    if b.get("type") != "figure":
        continue
    page_no = b["page"]
    bbox = b.get("bbox")
    if not bbox:
        continue
    page = doc[page_no - 1]
    rect = pymupdf.Rect(*bbox)

    # a raster image inside the region -> use it at native resolution
    native = None
    native_xref = None
    for xref, *_ in page.get_images(full=True):
        for r in page.get_image_rects(xref):
            rr = pymupdf.Rect(r)
            if rr.get_area() > 0.5 * rect.get_area() and rr.intersects(rect):
                native_xref = xref
                native = rr
                break
        if native_xref:
            break

    name = f"fig-{b['number']}.png"
    path = os.path.join(OUT, name)
    if native_xref is not None:
        try:
            info = doc.extract_image(native_xref)
            raw = os.path.join(OUT, f"_raw_{name}")
            with open(raw, "wb") as f:
                f.write(info["image"])
            os.replace(raw, path)
            src = f"raster xref={native_xref} {info['width']}x{info['height']} {info['ext']}"
        except Exception as exc:
            clip = pymupdf.Rect(*bbox) + (-3, -3, 3, 3)
            pix = page.get_pixmap(clip=clip, dpi=DPI, alpha=False)
            pix.save(path)
            src = f"raster-fallback {exc}"
    else:
        clip = rect + (-3, -3, 3, 3)
        pix = page.get_pixmap(clip=clip, dpi=DPI, alpha=False)
        pix.save(path)
        src = f"vector {pix.width}x{pix.height} @{DPI}dpi"

    index.append({
        "file": name,
        "number": b["number"],
        "caption": b["caption"],
        "page": page_no,
        "bbox": bbox,
        "source": src,
        "labels": b.get("labels", []),
    })
    print(f"{name:22s} p{page_no:<4} {src}")

with open(os.path.join(OUT, "_figures.json"), "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=1)
print(f"\n{len(index)} figures written to {OUT}")
