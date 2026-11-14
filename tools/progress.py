"""Track translation progress: which chapter parts are translated and verified."""
import json
import os
import re
import subprocess
import sys

ROOT = r"C:\Users\Admin\Documents\RustBook-RU"
WORK = os.path.join(ROOT, "ru", "work")
SRC = os.path.join(ROOT, "ru", "source")
CHAPTERS = os.path.join(ROOT, "ru", "chapters")
IMAGES = os.path.join(ROOT, "ru", "images")

jobs = json.load(open(os.path.join(WORK, "_jobs.json"), encoding="utf-8"))

# map source chapter -> (english source file, list of part files, ru outputs)
rows = []
for j in jobs:
    base = j["chapter"]
    parts = j["parts"]
    outs = []
    for p in parts:
        d, n = os.path.split(p)
        outs.append(os.path.join(d, n[:-3] + ".ru.md"))
    rows.append((base, parts, outs))

print(f"{'chapter':<26} {'parts':>5} {'done':>5} {'ok':>4} {'bytes(en)':>10} {'status'}")
total = done = ok = 0
for base, parts, outs in rows:
    n_ok = n_done = 0
    for en, ru in zip(parts, outs):
        total += 1
        if os.path.exists(ru):
            done += 1
            n_done += 1
            r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "check_translation.py"),
                                en, ru, IMAGES], capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            if "OK " in r.stdout:
                n_ok += 1
                ok += 1
    en_size = sum(os.path.getsize(p) for p in parts)
    status = "DONE" if n_ok == len(parts) else ("PARTIAL" if n_done else "TODO")
    print(f"{base:<26} {len(parts):>5} {n_done:>5} {n_ok:>4} {en_size:>10} {status}")

print(f"\nTOTAL parts: {total}   translated: {done}   verified: {ok}")

# per-chapter page counts from the PDF extraction
book = json.load(open(os.path.join(ROOT, "tools", "extract", "en", "book.json"), encoding="utf-8"))
ranges, ch = {}, None
for b in book["blocks"]:
    if b.get("type") == "chapter_label":
        ch = b["number"]
        ranges[ch] = [b["page"], b["page"]]
    elif ch:
        ranges[ch][1] = max(ranges[ch][1], b.get("page", 0))
print("\nchapter page spans:", {k: v[1] - v[0] + 1 for k, v in ranges.items()})
