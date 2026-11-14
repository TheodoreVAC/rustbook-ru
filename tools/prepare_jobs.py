"""Prepare translation jobs: split large chapters into parts, emit job manifests."""
import json
import os
import sys

SRC = r"C:\Users\Admin\Documents\RustBook-RU\ru\source"
WORK = r"C:\Users\Admin\Documents\RustBook-RU\ru\work"
MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30000

os.makedirs(WORK, exist_ok=True)
jobs = []
for fn in sorted(os.listdir(SRC)):
    if not fn.endswith(".md"):
        continue
    base = fn[:-3]
    src = os.path.join(SRC, fn)
    size = os.path.getsize(src)
    outdir = os.path.join(WORK, base)
    if size <= MAX:
        outdir = os.path.join(WORK, base)
        os.makedirs(outdir, exist_ok=True)
        p = os.path.join(outdir, "part-001.md")
        if not os.path.exists(p):
            with open(src, encoding="utf-8") as fi, open(p, "w", encoding="utf-8") as fo:
                fo.write(fi.read())
        jobs.append({"chapter": base, "parts": [p], "size": size})
        continue
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "split_chapter.py"),
                        "split", src, outdir, str(MAX)],
                       capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    # fold the preamble (chapter H1) into the first part
    pre = os.path.join(outdir, "_preamble.md")
    p1 = os.path.join(outdir, "part-001.md")
    if os.path.exists(pre) and os.path.exists(p1):
        with open(pre, encoding="utf-8") as f:
            head = f.read().strip("\n")
        with open(p1, encoding="utf-8") as f:
            body = f.read().strip("\n")
        with open(p1, "w", encoding="utf-8") as f:
            f.write((head + "\n\n" + body if head else body) + "\n")
        os.remove(pre)
    parts = sorted(os.path.join(outdir, p) for p in os.listdir(outdir)
                   if p.startswith("part-") and p.endswith(".md"))
    jobs.append({"chapter": base, "parts": parts, "size": size})

with open(os.path.join(WORK, "_jobs.json"), "w", encoding="utf-8") as f:
    json.dump(jobs, f, ensure_ascii=False, indent=1)
print(f"\n{len(jobs)} chapters, {sum(len(j['parts']) for j in jobs)} translation jobs")
for j in jobs:
    print(f"  {j['chapter']:28s} {j['size']:>7} bytes  {len(j['parts'])} part(s)")
