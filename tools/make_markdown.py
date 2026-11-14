"""Convert the extracted book structure into per-chapter Markdown (English source).

Also matches every code listing against the repository sources in
`publication/code/` so that the listings can be validated with cargo.
"""
import json
import os
import re
import sys

JSON = sys.argv[1]
OUTDIR = sys.argv[2]
CODEDIR = sys.argv[3] if len(sys.argv) > 3 else None

os.makedirs(OUTDIR, exist_ok=True)

CHAPTER_FILES = {
    1: "01-rust-basics.md",
    2: "02-computer-science.md",
    3: "03-algorithm-analysis.md",
    4: "04-data-structures.md",
    5: "05-recursion.md",
    6: "06-search.md",
    7: "07-sorting.md",
    8: "08-trees.md",
    9: "09-graphs.md",
    10: "10-practice.md",
}

RUST_HINTS = [
    "fn ", "let ", "struct ", "impl ", "enum ", "use ", "pub ", "match ",
    "trait ", "vec!", "println!", "->", "::", "mut ", "mod ", "unsafe ",
]
SHELL_HINTS = ["$ ", "curl ", "export ", "rustup", "cargo ", "sudo ", "apt ", "chmod "]


def detect_lang(lines):
    text = "\n".join(lines)
    if any(l.startswith("$ ") or l.startswith("#!") for l in lines):
        return "bash"
    if "rustup" in text or "export RUSTPATH" in text:
        return "bash"
    if "apt-get" in text or "sudo" in text:
        return "bash"
    score = sum(text.count(h) for h in RUST_HINTS)
    if score >= 2:
        return "rust"
    if score == 1:
        return "rust"
    return "text"


def md_escape(s):
    return s.replace("|", "\\|")


def load_repo_files(codedir):
    files = {}
    if not codedir or not os.path.isdir(codedir):
        return files
    for root, _dirs, names in os.walk(codedir):
        for nm in names:
            p = os.path.join(root, nm)
            try:
                with open(p, encoding="utf-8") as f:
                    files[os.path.relpath(p, codedir).replace("\\", "/")] = f.read()
            except (UnicodeDecodeError, OSError):
                continue
    return files


def norm_code(s):
    """Normalise a code listing for comparison.

    Comments are stripped because the repository copies of the listings use
    Chinese comments while the English book uses English ones.
    """
    out = []
    in_block = False
    for raw in s.strip().splitlines():
        l = raw.strip()
        if in_block:
            if "*/" in l:
                in_block = False
            continue
        if l.startswith("/*"):
            if "*/" not in l:
                in_block = True
            continue
        if l.startswith("//"):
            continue
        if l:
            out.append(l)
    return out


def match_repo(code_lines, repo):
    """Find the repository file whose content best matches the listing."""
    listing = norm_code("\n".join(code_lines))
    if len(listing) < 3:
        return None
    best, best_score = None, 0.0
    for name, text in repo.items():
        if not name.endswith(".rs"):
            continue
        cand = norm_code(text)
        if not cand:
            continue
        # longest common prefix ratio plus overlap score
        common = 0
        for a, b in zip(listing, cand):
            if a == b:
                common += 1
            else:
                break
        setl, setc = set(listing), set(cand)
        overlap = len(setl & setc) / max(1, len(setl))
        score = 0.5 * (common / max(len(listing), 1)) + 0.5 * overlap
        if score > best_score:
            best, best_score = name, score
    if best_score >= 0.55:
        return best, round(best_score, 3)
    return None


def main():
    data = json.load(open(JSON, encoding="utf-8"))
    blocks = data["blocks"]
    repo = load_repo_files(CODEDIR)

    # split into chapters
    chapters = []
    cur = None
    for b in blocks:
        if b.get("type") == "chapter_label":
            m = re.match(r"Chapter\s+(\d+)", b["number"])
            num = int(m.group(1)) if m else len(chapters) + 1
            cur = {"num": num, "blocks": []}
            chapters.append(cur)
            continue
        if cur is None:
            cur = {"num": 0, "blocks": []}
            chapters.append(cur)
        cur["blocks"].append(b)

    # front matter (preface, bibliography) -> chapter 0
    front = chapters[0]
    front["num"] = 0

    manifest = []
    for ch in chapters:
        if ch["num"] == 0:
            fname = "00-front-matter.md"
        else:
            fname = CHAPTER_FILES[ch["num"]]
        out = []
        title = ""
        for b in ch["blocks"]:
            t = b.get("type")
            if t == "h1":
                if not title:
                    title = b["title"]
                out.append(f"# {b['title']}")
                out.append("")
            elif t == "h2":
                num = b.get("number", "")
                head = f"## {num} {b['title']}".strip()
                out.append(head)
                out.append("")
            elif t == "h3":
                num = b.get("number", "")
                head = f"### {num} {b['title']}".strip()
                out.append(head)
                out.append("")
            elif t == "p":
                out.append(b["text"])
                out.append("")
            elif t == "ul":
                for it in b["items"]:
                    out.append(f"- {it}")
                out.append("")
            elif t == "code":
                lang = detect_lang(b["lines"])
                out.append(f"```{lang}")
                out.extend(b["lines"])
                out.append("```")
                out.append("")
            elif t == "table":
                cap = f"Table {b['number']}: {b['caption']}" if b.get("caption") else ""
                if cap:
                    out.append(f"**{cap}**")
                    out.append("")
                hdr = b.get("header") or []
                rows = b.get("rows") or []
                if hdr or rows:
                    ncols = max([len(hdr)] + [len(r) for r in rows] or [1])
                    hdr = list(hdr) + [""] * (ncols - len(hdr))
                    out.append("| " + " | ".join(md_escape(h) for h in hdr) + " |")
                    out.append("| " + " | ".join("---" for _ in range(ncols)) + " |")
                    for r in rows:
                        r = list(r) + [""] * (ncols - len(r))
                        out.append("| " + " | ".join(md_escape(c) for c in r) + " |")
                    out.append("")
            elif t == "figure":
                out.append(f"![Figure {b['number']}: {b['caption']}](images/fig-{b['number']}.png)")
                out.append("")
                out.append(f"*Figure {b['number']}: {b['caption']}*")
                out.append("")
        path = os.path.join(OUTDIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out).rstrip() + "\n")
        manifest.append({"file": fname, "chapter": ch["num"], "title": title,
                         "blocks": len(ch["blocks"])})
        print(f"{fname:28s} ch{ch['num']:<3} {title!r} blocks={len(ch['blocks'])}")

    # code -> repository mapping
    mapping = []
    idx = 0
    for ch in chapters:
        for b in ch["blocks"]:
            if b.get("type") != "code":
                continue
            idx += 1
            m = match_repo(b["lines"], repo)
            mapping.append({"i": idx, "chapter": ch["num"], "page": b.get("page"),
                            "file": m[0] if m else None, "score": m[1] if m else None})
    with open(os.path.join(OUTDIR, "_code_map.json"), "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=1)
    matched = sum(1 for m in mapping if m["file"])
    print(f"\ncode listings: {len(mapping)}, matched to repo files: {matched}")


if __name__ == "__main__":
    main()
