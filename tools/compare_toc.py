"""Compare extracted headings with the PDF's embedded table of contents."""
import json
import sys
import pymupdf

pdf_path, json_path = sys.argv[1], sys.argv[2]
doc = pymupdf.open(pdf_path)
toc = doc.get_toc()
blocks = json.load(open(json_path, encoding="utf-8"))["blocks"]

mine = []
for b in blocks:
    t = b.get("type")
    if t == "chapter_label":
        mine.append((1, b["number"]))
    elif t == "h1":
        mine.append((1, b["title"]))
    elif t == "h2":
        mine.append((2, b["number"], b["title"]))
    elif t == "h3":
        mine.append((3, b["number"], b["title"]))

theirs = [(lvl, title) for lvl, title, pg in toc if title != "Contents"]

print(f"PDF TOC entries: {len(theirs)}   extracted headings: {len(mine)}")
only_mine = []
for m in mine:
    key = m[-1]
    if not any(key.lower() == t[-1].lower() for t in theirs):
        only_mine.append(m)
only_theirs = []
for t in theirs:
    if not any(t[-1].lower() == m[-1].lower() for m in mine):
        only_theirs.append(t)

print(f"\nOnly in extraction ({len(only_mine)}):")
for m in only_mine:
    print("   ", m)
print(f"\nOnly in PDF TOC ({len(only_theirs)}):")
for t in only_theirs:
    print("   ", t)
