"""Split a chapter Markdown file into parts at heading boundaries, and merge them back.

Splits at `##` first; if a section is still too large it is split further at
`###` boundaries.  The preamble (everything before the first `##`) is kept
separate so that merging restores the original order exactly.

Usage:
    python split_chapter.py split <file> <outdir> <max_bytes>
    python split_chapter.py merge <outdir> <outfile>
"""
import glob
import os
import sys


def split(path, outdir, max_bytes):
    os.makedirs(outdir, exist_ok=True)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.split("\n")

    def sections_at(level):
        marks = [i for i, l in enumerate(lines) if l.startswith("#" * level + " ")
                 and not l.startswith("#" * (level + 1) + " ")]
        out = []
        for k, start in enumerate(marks):
            end = marks[k + 1] if k + 1 < len(marks) else len(lines)
            out.append((start, end))
        return out

    top = sections_at(2)
    preamble_end = top[0][0] if top else len(lines)
    preamble = "\n".join(lines[:preamble_end])

    def size_of(a, b):
        return len("\n".join(lines[a:b]).encode("utf-8"))

    parts = []
    for a, b in top:
        if size_of(a, b) <= max_bytes:
            parts.append((a, b))
            continue
        # split a big section further at its subsections, grouping them
        subs = [(sa, sb) for sa, sb in sections_at(3) if a <= sa and sb <= b]
        cur = a
        chunk_start = a
        chunk_size = 0
        for sa, sb in subs:
            s = size_of(sa, sb)
            if chunk_size and chunk_size + s > max_bytes:
                parts.append((chunk_start, sa))
                chunk_start = sa
                chunk_size = 0
            chunk_size += s
        if chunk_start < b:
            parts.append((chunk_start, b))

    names = []
    for n, (a, b) in enumerate(parts, 1):
        name = f"part-{n:03d}.md"
        body = "\n".join(lines[a:b]).strip("\n")
        with open(os.path.join(outdir, name), "w", encoding="utf-8") as f:
            f.write(body + "\n")
        names.append(name)
        print(f"  {name}: {len(body.encode('utf-8'))} bytes")
    with open(os.path.join(outdir, "_preamble.md"), "w", encoding="utf-8") as f:
        f.write(preamble.strip("\n"))
    return len(parts)


def merge(outdir, outfile):
    names = sorted(glob.glob(os.path.join(outdir, "part-*.md")))
    pre = os.path.join(outdir, "_preamble.md")
    chunks = []
    if os.path.exists(pre):
        with open(pre, encoding="utf-8") as f:
            t = f.read().strip("\n")
            if t:
                chunks.append(t)
    for n in names:
        with open(n, encoding="utf-8") as f:
            t = f.read().strip("\n")
            if t:
                chunks.append(t)
    os.makedirs(os.path.dirname(outfile) or ".", exist_ok=True)
    with open(outfile, "w", encoding="utf-8") as f:
        f.write("\n\n".join(chunks) + "\n")
    print(f"merged {len(names)} parts -> {outfile}")


if __name__ == "__main__":
    if sys.argv[1] == "split":
        split(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    else:
        merge(sys.argv[2], sys.argv[3])
