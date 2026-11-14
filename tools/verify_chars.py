"""Completeness check: compare normalized character counts per page.

For every page the PDF text (minus code line numbers) is normalised to a
character stream, and the same is done for the extracted blocks.  Pages whose
sizes differ by more than a tolerance indicate lost or duplicated content.
"""
import json
import re
import sys
import collections
import pymupdf

pdf_path, json_path = sys.argv[1], sys.argv[2]
toc_pages = set(int(x) for x in sys.argv[3].split(",")) if len(sys.argv) > 3 else set()
doc = pymupdf.open(pdf_path)
blocks = json.load(open(json_path, encoding="utf-8"))["blocks"]
by_page = collections.defaultdict(list)
for b in blocks:
    by_page[b.get("page", 0)].append(b)

CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
NONWORD_RE = re.compile(r"[^a-z0-9]+")


def norm(s):
    return NONWORD_RE.sub("", s.lower())


def code_tick_bands(page):
    bands = []
    for dr in page.get_drawings():
        c = dr.get("color")
        if not (c and abs(c[0] - 0.808) < 0.03 and abs(c[1] - 0.832) < 0.03):
            continue
        r = dr["rect"]
        if r.x1 - r.x0 < 1.5 and (r.y1 - r.y0) > 4 and r.x0 < 70:
            bands.append((r.y0, r.y1))
    return bands


bad = []
for pno in range(doc.page_count):
    page = doc[pno]
    pg = pno + 1
    if pg in toc_pages:
        continue
    bands = code_tick_bands(page)

    def is_lineno(l, bands=bands):
        s0 = l["spans"][0]
        if not (s0["font"] == "TimesNewRomanPSMT" and 8.5 <= round(s0["size"], 2) <= 9.4
                and l["bbox"][0] < 82
                and "".join(s["text"] for s in l["spans"]).strip().isdigit()):
            return False
        yc = (l["bbox"][1] + l["bbox"][3]) / 2
        return any(b[0] - 1.5 <= yc <= b[1] + 1.5 for b in bands)

    raw = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] == 1:
            continue
        for l in b["lines"]:
            if l["bbox"][3] < 45 or l["bbox"][1] > 688:
                continue
            txt = CTRL_RE.sub("", "".join(s["text"] for s in l["spans"]))
            if not txt.strip() or is_lineno(l):
                continue
            raw.append(txt)
    raw_s = norm(" ".join(raw))

    got = []
    for b in by_page.get(pg, []):
        ty = b.get("type")
        if ty == "p":
            got.append(b.get("text", ""))
        elif ty == "ul":
            got.extend(b.get("items", []))
        elif ty == "code":
            got.extend(b.get("lines", []))
        elif ty in ("h1", "h2", "h3", "h4"):
            got.extend([b.get("number", ""), b.get("title", "")])
        elif ty == "chapter_label":
            got.append(b.get("number", ""))
        elif ty == "table":
            got.extend(["Table", b.get("number", ""), b.get("caption", "")])
            got.extend(b.get("header", []))
            for r in b.get("rows", []):
                got.extend(r)
        elif ty == "figure":
            got.extend(["Figure", b.get("number", ""), b.get("caption", "")])
            got.extend(b.get("labels", []))
    got_s = norm(" ".join(str(x) for x in got))

    # the caption prefix appears in got but not in raw -> neutralise it
    got_s = got_s.replace("table" + norm(b"number") if False else "table", "", 1)
    if not raw_s:
        continue
    ratio = len(got_s) / len(raw_s)
    if ratio < 0.985 or ratio > 1.02:
        bad.append((pg, len(raw_s), len(got_s), ratio))

print(f"pages with size mismatch: {len(bad)}")
tot_r = tot_g = 0
for pg, r, g, ratio in bad:
    print(f"  p{pg}: raw={r} got={g} ratio={ratio:.3f}")
for pno in range(doc.page_count):
    pass
print(f"total pages compared: {doc.page_count - len(toc_pages)}")
