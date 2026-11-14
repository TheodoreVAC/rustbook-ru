"""Diff the PDF text of a page against the extracted blocks for that page."""
import json
import re
import sys
import difflib
import collections
import pymupdf

pdf_path, json_path = sys.argv[1], sys.argv[2]
pages = [int(x) for x in sys.argv[3].split(",")]
doc = pymupdf.open(pdf_path)
blocks = json.load(open(json_path, encoding="utf-8"))["blocks"]
by_page = collections.defaultdict(list)
for b in blocks:
    by_page[b.get("page", 0)].append(b)

NONWORD = re.compile(r"[^a-z0-9]+")
CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

for pno in pages:
    page = doc[pno - 1]
    raw = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] == 1:
            continue
        for l in b["lines"]:
            if l["bbox"][3] < 45 or l["bbox"][1] > 688:
                continue
            t = CTRL.sub("", "".join(s["text"] for s in l["spans"]))
            if t.strip():
                raw.append(t)
    raw_s = NONWORD.sub("", " ".join(raw).lower())

    got = []
    for b in by_page.get(pno, []):
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
    got_s = NONWORD.sub("", " ".join(str(x) for x in got).lower())

    print(f"=== page {pno}: raw={len(raw_s)} got={len(got_s)}")
    sm = difflib.SequenceMatcher(None, raw_s, got_s, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            print(f"   {tag}: raw[{i1}:{i2}]={raw_s[i1:i2]!r}  got[{j1}:{j2}]={got_s[j1:j2]!r}")
