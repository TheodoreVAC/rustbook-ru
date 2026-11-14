"""Post-process the rendered PDF: clean the cover page and report statistics."""
import os
import sys

import pymupdf


def clean_cover(pdf_path, strip_top=26, strip_bottom=26):
    doc = pymupdf.open(pdf_path)
    page = doc[0]
    r = page.rect
    # remove the running header and the page number from the cover
    for band in (pymupdf.Rect(r.x0, r.y0, r.x1, r.y0 + strip_top),
                 pymupdf.Rect(r.x0, r.y1 - strip_bottom, r.x1, r.y1)):
        page.add_redact_annot(band, fill=(1, 1, 1))
    page.apply_redactions()
    doc.saveIncr()
    doc.close()


def report(pdf_path):
    doc = pymupdf.open(pdf_path)
    n_img = 0
    n_code = 0
    for i in range(doc.page_count):
        n_img += len(doc[i].get_images(full=True))
        txt = doc[i].get_text()
        n_code += txt.count("```")
    print(f"pages          : {doc.page_count}")
    print(f"page size      : {doc[0].rect.width:.0f} x {doc[0].rect.height:.0f} pt")
    print(f"embedded images: {n_img}")
    # check for missing glyphs / tofu
    tofu = 0
    for i in range(doc.page_count):
        tofu += doc[i].get_text().count("\ufffd")
    print(f"replacement chr: {tofu}")
    doc.close()


if __name__ == "__main__":
    pdf = sys.argv[1]
    if "--clean" in sys.argv:
        clean_cover(pdf)
        print("cover cleaned")
    report(pdf)
