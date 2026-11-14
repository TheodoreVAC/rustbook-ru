"""Compare the merged Russian chapters against the English source chapters."""
import os
import re
import sys

ROOT = r"C:\Users\Admin\Documents\RustBook-RU"
SRC = os.path.join(ROOT, "ru", "source")
RU = os.path.join(ROOT, "ru", "chapters")


def stats(text):
    code = text.count("```") // 2
    figs = len(re.findall(r"^!\[", text, re.M))
    tabs = len(re.findall(r"^\*\*Табл", text, re.M))
    heads = len(re.findall(r"^#{1,4} ", text, re.M))
    caps = len(re.findall(r"^\*Рисунок ", text, re.M))
    paras = len([p for p in re.split(r"\n\s*\n", text)
                 if p.strip() and not p.startswith(("#", "|", "![", "```", "- ", "*", ">"))
                 and not re.match(r"^[-*] ", p.strip())])
    items = len(re.findall(r"^- ", text, re.M))
    return dict(head=heads, code=code, figs=figs, tabs=tabs, paras=paras, items=items)


names = sorted(f for f in os.listdir(SRC) if f.endswith(".md"))
bad = 0
for n in names:
    ru_name = n
    en = open(os.path.join(SRC, n), encoding="utf-8").read()
    rp = os.path.join(RU, ru_name)
    if not os.path.exists(rp):
        print(f"{n}: MISSING Russian chapter")
        bad += 1
        continue
    ru = open(rp, encoding="utf-8").read()
    a, b = stats(en), stats(ru)
    diffs = {k: (a[k], b[k]) for k in a if a[k] != b[k]}
    flag = "OK  " if not diffs else "DIFF"
    if diffs:
        bad += 1
    print(f"{flag} {n:<28} {a} ")
    if diffs:
        print(f"       -> {b}")
        print(f"       differences: {diffs}")
print(f"\n{bad} chapter(s) with differences out of {len(names)}")
