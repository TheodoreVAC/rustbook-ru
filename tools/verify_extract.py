"""Verify extraction completeness against the PDF text.

Accounts for the intentional differences:
  * code-block line numbers are dropped
  * words hyphenated across a line break are rejoined
  * the auto-generated TOC pages are replaced by a generated TOC
  * labels drawn inside a figure graphic belong to the figure image
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

TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")
CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

total_miss = 0
total_extra = 0
issues = []


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


for pno in range(doc.page_count):
    page = doc[pno]
    pg = pno + 1
    if pg in toc_pages:
        continue
    bands = code_tick_bands(page)

    def is_lineno(l, bands=bands):
        if not (l["spans"][0]["font"] == "TimesNewRomanPSMT"
                and 8.5 <= round(l["spans"][0]["size"], 2) <= 9.4
                and l["bbox"][0] < 82
                and "".join(s["text"] for s in l["spans"]).strip().isdigit()):
            return False
        yc = (l["bbox"][1] + l["bbox"][3]) / 2
        return any(b[0] - 1.5 <= yc <= b[1] + 1.5 for b in bands)

    raw_lines = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] == 1:
            continue
        for l in b["lines"]:
            if l["bbox"][3] < 45 or l["bbox"][1] > 688:
                continue
            txt = CTRL_RE.sub("", "".join(s["text"] for s in l["spans"]))
            if not txt.strip():
                continue
            if is_lineno(l):
                continue
            raw_lines.append(txt)

    joined = ""
    for t in raw_lines:
        if not joined:
            joined = t
        elif joined.endswith("-"):
            joined = joined[:-1] + t
        else:
            joined = joined + " " + t
    raw_tokens = collections.Counter(TOKEN_RE.findall(joined))

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
    got_tokens = collections.Counter()
    for t in got:
        if isinstance(t, list):
            t = " ".join(str(x) for x in t)
        got_tokens.update(TOKEN_RE.findall(str(t)))

    miss = raw_tokens - got_tokens
    extra = got_tokens - raw_tokens
    if miss or extra:
        total_miss += sum(miss.values())
        total_extra += sum(extra.values())
        issues.append((pg, dict(miss), dict(extra)))

print(f"pages with differences: {len(issues)}")
print(f"missing tokens: {total_miss}   extra tokens: {total_extra}")
for pg, m, e in issues:
    print(f"  p{pg}: MISSING={m} EXTRA={e}")
