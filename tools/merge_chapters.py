"""Merge the translated chapter parts into the final ru/chapters/*.md files."""
import json
import os
import re
import sys

ROOT = r"C:\Users\Admin\Documents\RustBook-RU"
WORK = os.path.join(ROOT, "ru", "work")
OUT = os.path.join(ROOT, "ru", "chapters")

FILES = {
    "00-front-matter": "00-front-matter.md",
    "01-rust-basics": "01-rust-basics.md",
    "02-computer-science": "02-computer-science.md",
    "03-algorithm-analysis": "03-algorithm-analysis.md",
    "04-data-structures": "04-data-structures.md",
    "05-recursion": "05-recursion.md",
    "06-search": "06-search.md",
    "07-sorting": "07-sorting.md",
    "08-trees": "08-trees.md",
    "09-graphs": "09-graphs.md",
    "10-practice": "10-practice.md",
}

jobs = json.load(open(os.path.join(WORK, "_jobs.json"), encoding="utf-8"))
os.makedirs(OUT, exist_ok=True)

manifest = []
for j in jobs:
    base = j["chapter"]
    parts = []
    for p in j["parts"]:
        ru = p[:-3] + ".ru.md"
        if not os.path.exists(ru):
            print(f"MISSING: {ru}")
            continue
        with open(ru, encoding="utf-8") as f:
            parts.append(f.read().strip("\n"))
    text = "\n\n".join(parts) + "\n"

    # normalise: collapse 3+ blank lines, ensure a single trailing newline
    text = re.sub(r"\n{3,}", "\n\n", text)
    out = os.path.join(OUT, FILES[base])
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    heads = re.findall(r"^#{1,3} .*$", text, re.M)
    codes = text.count("```") // 2
    figs = len(re.findall(r"!\[", text))
    tabs = len(re.findall(r"^\*\*Таблица", text, re.M))
    manifest.append({
        "file": FILES[base], "parts": len(parts), "headings": len(heads),
        "code_blocks": codes, "figures": figs, "tables": tabs,
        "chars": len(text),
    })
    print(f"{FILES[base]:<28} parts={len(parts):<3} head={len(heads):<4} "
          f"code={codes:<4} fig={figs:<4} tab={tabs:<3} {len(text):>7} chars")

with open(os.path.join(OUT, "_manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)
