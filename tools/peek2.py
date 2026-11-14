import io, re
t = io.open(r"ru\RustBook-RU.md", encoding="utf-8").read()
ids = set(re.findall(r'<a id="([^"]+)"></a>', t))
links = re.findall(r"\]\(#([^)]+)\)", t)
missing = [l for l in links if l not in ids]
print("anchors:", len(ids), " toc links:", len(links), " broken:", len(missing))
if missing: print("  ", missing[:10])
imgs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", t)
import os
bad = [i for i in imgs if not os.path.exists(os.path.join(r"ru", i))]
print("images:", len(imgs), " missing:", len(bad), bad[:5])
