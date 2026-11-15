"""Structural verification of a translated chapter against its English source.

Checks
  * same number of headings (and same heading numbers)
  * same number of paragraphs / list items
  * byte-identical code blocks
  * same table shape (rows x columns)
  * all figure references present and pointing to existing files
  * heuristic: no long untranslated English paragraphs
"""
import os
import re
import sys


HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)


def parse(path):
    """Split a Markdown file into (kind, payload) blocks."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = HTML_COMMENT.sub("", text)
    lines = text.split("\n")
    blocks = []
    images = []
    captions = []
    i = 0
    n = len(lines)
    in_code = False
    code = []
    para = []
    ul = []
    table = []

    def flush_para():
        nonlocal para
        if para:
            blocks.append(("p", " ".join(para).strip()))
            para = []

    def flush_ul():
        nonlocal ul
        if ul:
            blocks.append(("ul", list(ul)))
            ul = []

    def flush_table():
        nonlocal table
        if table:
            blocks.append(("table", list(table)))
            table = []

    for ln in lines:
        if ln.startswith("```"):
            if in_code:
                blocks.append(("code", "\n".join(code)))
                code = []
                in_code = False
            else:
                flush_para()
                flush_ul()
                flush_table()
                in_code = True
            continue
        if in_code:
            code.append(ln)
            continue
        if ln.startswith("#"):
            flush_para()
            flush_ul()
            flush_table()
            m = re.match(r"(#+)\s*(.*)$", ln)
            blocks.append((f"h{len(m.group(1))}", m.group(2).strip()))
        elif ln.startswith("| "):
            flush_para()
            flush_ul()
            table.append(ln)
        elif ln.startswith("- "):
            flush_para()
            flush_table()
            ul.append(ln[2:].strip())
        elif ln.startswith("!["):
            flush_para()
            flush_ul()
            flush_table()
            m = re.match(r"!\[(.*?)\]\((.*?)\)", ln)
            images.append((m.group(1), m.group(2)) if m else ("", ""))
        elif ln.startswith("*") and ln.endswith("*") and not ln.startswith("**"):
            flush_para()
            flush_ul()
            flush_table()
            captions.append(ln.strip("* "))
        elif not ln.strip():
            flush_para()
            flush_ul()
            flush_table()
        else:
            flush_ul()
            flush_table()
            para.append(ln.strip())
    flush_para()
    flush_ul()
    flush_table()
    return blocks, images, captions


EN_WORD = re.compile(r"\b(the|and|of|to|is|are|that|this|with|for|from|which|"
                      r"can|will|when|there|their|its|not|but|has|been|was|were)\b",
                      re.IGNORECASE)


def check(en_path, ru_path, imgdir=None):
    """Return (errors, warnings) for the given pair of files."""
    errors = []
    warnings = []

    en_blocks, en_imgs, en_caps = parse(en_path)
    ru_blocks, ru_imgs, ru_caps = parse(ru_path)

    def count(blocks, kind):
        return sum(1 for b in blocks if b[0] == kind)

    for kind, label in (("h1", "H1"), ("h2", "H2"), ("h3", "H3"), ("h4", "H4"),
                         ("p", "paragraphs"), ("code", "code blocks"),
                         ("table", "tables")):
        a, b = count(en_blocks, kind), count(ru_blocks, kind)
        if kind == "ul":
            a = sum(len(x[1]) for x in en_blocks if x[0] == "ul")
            b = sum(len(x[1]) for x in ru_blocks if x[0] == "ul")
        if a != b:
            errors.append(f"{label}: source={a} translation={b}")

    def numbers(blocks):
        out = []
        for kind, val in blocks:
            if kind.startswith("h") and kind != "h0":
                m = re.match(r"^(\d+(?:\.\d+)*)\s", val)
                out.append(m.group(1) if m else None)
        return out

    en_nums, ru_nums = numbers(en_blocks), numbers(ru_blocks)
    if len(en_nums) != len(ru_nums):
        errors.append(f"heading count mismatch: {len(en_nums)} vs {len(ru_nums)}")
    else:
        for i, (a, b) in enumerate(zip(en_nums, ru_nums)):
            if a != b:
                errors.append(f"heading #{i}: number '{a}' -> '{b}'")

    en_code = [v for k, v in en_blocks if k == "code"]
    ru_code = [v for k, v in ru_blocks if k == "code"]
    if len(en_code) != len(ru_code):
        errors.append(f"code block count {len(en_code)} vs {len(ru_code)}")
    else:
        for i, (a, b) in enumerate(zip(en_code, ru_code)):
            if a != b:
                al, bl = a.split("\n"), b.split("\n")
                errors.append(f"code block #{i + 1} differs ({len(al)} vs {len(bl)} lines)")
                for j, (x, y) in enumerate(zip(al, bl)):
                    if x != y:
                        errors.append(f"    line {j + 1}: {x!r} != {y!r}")
                        break

    en_tab = [v for k, v in en_blocks if k == "table"]
    ru_tab = [v for k, v in ru_blocks if k == "table"]
    if len(en_tab) != len(ru_tab):
        errors.append(f"table count {len(en_tab)} vs {len(ru_tab)}")
    else:
        for i, (a, b) in enumerate(zip(en_tab, ru_tab)):
            ac = [len(r.split("|")[1:-1]) for r in a]
            bc = [len(r.split("|")[1:-1]) for r in b]
            if ac != bc:
                errors.append(f"table #{i + 1} shape differs: {ac} vs {bc}")

    if len(en_imgs) != len(ru_imgs):
        errors.append(f"image count {len(en_imgs)} vs {len(ru_imgs)}")
    else:
        for i, ((ea, ep), (ra, rp)) in enumerate(zip(en_imgs, ru_imgs)):
            if ep != rp:
                errors.append(f"image #{i + 1} path '{ep}' -> '{rp}'")
            if imgdir:
                p = os.path.join(imgdir, os.path.basename(rp))
                if not os.path.exists(p):
                    errors.append(f"image #{i + 1} missing on disk: {rp}")

    if len(en_caps) != len(ru_caps):
        errors.append(f"caption count {len(en_caps)} vs {len(ru_caps)}")

    for kind, val in ru_blocks:
        if kind != "p":
            continue
        words = val.split()
        if len(words) < 12:
            continue
        hits = len(EN_WORD.findall(val))
        if hits / max(1, len(words)) > 0.12:
            warnings.append(f"possible untranslated paragraph ({hits}/{len(words)}): {val[:110]!r}")

    return errors, warnings


def main():
    if len(sys.argv) < 3:
        print("usage: check_translation.py <en.md> <ru.md> [images-dir]")
        return 2
    en, ru = sys.argv[1], sys.argv[2]
    imgdir = sys.argv[3] if len(sys.argv) > 3 else None
    errors, warnings = check(en, ru, imgdir)
    name = os.path.basename(ru)
    if errors:
        print(f"FAIL {name}: {len(errors)} error(s)")
        for e in errors[:40]:
            print("   ERROR  ", e)
        if len(errors) > 40:
            print(f"   ... and {len(errors) - 40} more")
    else:
        print(f"OK   {name}: structure matches")
    if warnings:
        print(f"     {len(warnings)} warning(s):")
        for w in warnings[:10]:
            print("   WARN  ", w)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
