"""
Structure-aware extractor for the RustBook PDF -> book.json

Layout model of the original LaTeX book
---------------------------------------
  * body text lines start at x = 56.5 (continuation) or x = 71.4 (first line
    of an indented paragraph)
  * code listings are set in SourceCodePro, with optional line numbers in the
    gutter, framed by light-blue ticks
  * tables and figures consist of "loose" text (cells / labels) placed at other
    x positions, plus vector graphics and rules
  * captions ("Figure 4.1: ...", "Table 4.1: ...") close the region above them

Output block types: chapter_label, h1..h4, p, ul, code, table, figure
"""
import json
import os
import re
import sys
import pymupdf

HEADER_Y = 45.0
FOOTER_Y = 688.0
CODE_BASE_X = 84.8
CHAR_W = 5.98
BODY_LEFT = 56.5
BODY_INDENT = 71.4
BODY_X_TOL = 1.6

MONO = "SourceCodePro"
SERIF = "TimesNewRomanPSMT"
SERIF_B = "TimesNewRomanPS-BoldMT"
SERIF_I = "TimesNewRomanPS-ItalicMT"
MATH_FONTS = ("CMR", "CMMI", "CMEX", "CMSY")

CAPTION_RE = re.compile(r"^(Figure|Table)\s+([\d.]+)\s*[:：]\s*(.*)$")
CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
BULLET_GLYPHS = ("•", "\uf0b7", "\x7f")


def clean(t):
    t = CTRL_RE.sub("", t).replace("\uf0b7", "•")
    t = t.replace("̸=", "≠")   # CM slash-overlay on '=' -> 'not equal'
    return t


def is_code_font(f):
    return MONO in f


def is_math_font(f):
    return f.startswith(MATH_FONTS)


def collect_lines(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] == 1:
            continue
        for l in b["lines"]:
            txt = clean("".join(s["text"] for s in l["spans"]))
            if not txt.strip():
                continue
            y0, y1 = l["bbox"][1], l["bbox"][3]
            if y1 < HEADER_Y or y0 > FOOTER_Y:
                continue
            out.append({
                "text": txt,
                "x0": round(l["bbox"][0], 2), "x1": round(l["bbox"][2], 2),
                "y0": round(y0, 2), "y1": round(y1, 2),
                "font": l["spans"][0]["font"],
                "size": round(max(s["size"] for s in l["spans"]), 2),
                "bold": "Bold" in l["spans"][0]["font"],
                "italic": "Italic" in l["spans"][0]["font"],
                "spans": [{"t": s["text"], "f": s["font"], "sz": round(s["size"], 2),
                           "x0": round(s["bbox"][0], 2), "x1": round(s["bbox"][2], 2)}
                          for s in l["spans"]],
            })
    out.sort(key=lambda l: (round(l["y0"], 1), l["x0"]))
    return out


def code_tick_bands(page):
    bands = []
    for dr in page.get_drawings():
        c = dr.get("color")
        if not (c and abs(c[0] - 0.808) < 0.03 and abs(c[1] - 0.832) < 0.03):
            continue
        r = dr["rect"]
        if r.x1 - r.x0 < 1.5 and (r.y1 - r.y0) > 4 and r.x0 < 70:
            bands.append((r.y0, r.y1))
    bands.sort()
    merged = []
    for b in bands:
        if merged and b[0] <= merged[-1][1] + 0.6:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b[1]))
        else:
            merged.append((b[0], b[1]))
    return merged


def table_bands(page, lines=()):
    """Vertical bands occupied by tables, derived from their horizontal rules.

    A band is split wherever ordinary body text occurs, so that a table on one
    part of a page does not swallow the text below it.
    """
    rules = []
    for dr in page.get_drawings():
        r = dr["rect"]
        c = dr.get("color")
        if c and abs(c[0] - 0.808) < 0.03 and abs(c[1] - 0.832) < 0.03:
            continue
        if dr["type"] == "s" and abs(r.y1 - r.y0) < 0.7 and (r.x1 - r.x0) > 40:
            if abs(r.y0 - 38.9) < 0.8 and (r.x1 - r.x0) > 380:
                continue  # running-header rule
            rules.append((round(r.y0, 2), round(r.x0, 2), round(r.x1, 2)))
    rules.sort()
    groups = []
    for r in rules:
        placed = False
        for g in groups:
            if abs(r[1] - g["x0"]) < 30 and abs(r[2] - g["x1"]) < 30:
                g["rules"].append(r)
                placed = True
                break
        if not placed:
            groups.append({"x0": r[1], "x1": r[2], "rules": [r]})

    body_ys = sorted(l["y0"] for l in lines
                     if abs(l["x0"] - BODY_LEFT) <= BODY_X_TOL
                     or abs(l["x0"] - BODY_INDENT) <= BODY_X_TOL)
    bands = []
    for g in groups:
        rs = sorted(g["rules"])
        start = rs[0][0]
        for k in range(1, len(rs)):
            prev_y, cur_y = rs[k - 1][0], rs[k][0]
            if any(prev_y < by < cur_y for by in body_ys):
                bands.append((start - 2, prev_y + 2))
                start = cur_y
        bands.append((start - 2, rs[-1][0] + 2))
    return bands


def make_lineno_checker(page):
    bands = code_tick_bands(page)

    def is_lineno(ln):
        if not (ln["font"] == SERIF and 8.5 <= ln["size"] <= 9.4
                and ln["x0"] < 82 and ln["text"].strip().isdigit()):
            return False
        yc = (ln["y0"] + ln["y1"]) / 2
        return any(b[0] - 1.5 <= yc <= b[1] + 1.5 for b in bands)

    return is_lineno


def collect_graphics(page):
    """Raster images and vector drawing clusters (figures / table rules)."""
    items = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] == 1:
            items.append({"kind": "raster", "bbox": [round(v, 2) for v in b["bbox"]]})

    boxes = []
    for dr in page.get_drawings():
        r = dr["rect"]
        c = dr.get("color")
        if c and abs(c[0] - 0.808) < 0.03 and abs(c[1] - 0.832) < 0.03:
            continue
        if abs(r.y0 - 38.9) < 0.8 and (r.x1 - r.x0) > 380:
            continue
        boxes.append(r)

    boxes.sort(key=lambda r: (r.y0, r.x0))
    groups = []
    for r in boxes:
        hit = None
        for g in groups:
            if not (r.y0 > g["bbox"][3] + 14 or r.y1 < g["bbox"][1] - 14):
                hit = g
                break
        if hit is None:
            groups.append({"kind": "vector", "bbox": [r.x0, r.y0, r.x1, r.y1]})
        else:
            hit["bbox"] = [min(hit["bbox"][0], r.x0), min(hit["bbox"][1], r.y0),
                           max(hit["bbox"][2], r.x1), max(hit["bbox"][3], r.y1)]

    merged = True
    while merged:
        merged = False
        groups.sort(key=lambda g: g["bbox"][1])
        for i in range(len(groups) - 1):
            a, b = groups[i], groups[i + 1]
            if b["bbox"][1] - a["bbox"][3] <= 18 and b["bbox"][3] > a["bbox"][1]:
                a["bbox"] = [min(a["bbox"][0], b["bbox"][0]), min(a["bbox"][1], b["bbox"][1]),
                             max(a["bbox"][2], b["bbox"][2]), max(a["bbox"][3], b["bbox"][3])]
                groups.pop(i + 1)
                merged = True
                break
    items.extend(groups)
    items.sort(key=lambda g: g["bbox"][1])
    return items


def join_wrapped(parts):
    out = ""
    for t in parts:
        if not out:
            out = t
        elif out.endswith("-"):
            out = out[:-1] + t
        else:
            out = out + " " + t
    return out


def heading_level(size):
    if size > 22:
        return 1
    if size > 19:
        return 0
    if size > 13:
        return 2
    if size > 11:
        return 3
    return None


def is_body_line(ln, in_table=False):
    if in_table:
        return False
    if abs(ln["x0"] - BODY_LEFT) <= BODY_X_TOL or abs(ln["x0"] - BODY_INDENT) <= BODY_X_TOL:
        return True
    # a centred, wide display equation is body content too
    if is_math_font(ln["font"]) and ln["size"] >= 9.5:
        width = ln["x1"] - ln["x0"]
        centre = (ln["x0"] + ln["x1"]) / 2
        if width >= 50 and abs(centre - 262.25) <= 45:
            return True
    return False


def is_bullet_line(ln):
    s0 = ln["spans"][0]
    return s0["f"].startswith("CMSY") and s0["t"].strip() in BULLET_GLYPHS


def build_elements(lines, is_lineno, bands=(), eq_idx=frozenset()):
    """Split the page's lines into ordered elements."""
    def in_table(ln):
        return any(y0 - 2 <= ln["y0"] <= y1 + 2 for y0, y1 in bands)

    els = []
    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]
        if i in eq_idx:
            j = i
            eq = []
            while j < n and j in eq_idx:
                eq.append(lines[j])
                j += 1
            els.append({"kind": "equation", "lines": eq,
                        "y0": eq[0]["y0"], "y1": eq[-1]["y1"]})
            i = j
            continue
        if is_code_font(ln["font"]) or is_lineno(ln):
            code, j = [], i
            while j < n:
                l2 = lines[j]
                if is_lineno(l2):
                    k = j + 1
                    parts = []
                    while k < n and is_code_font(lines[k]["font"]) and not is_lineno(lines[k]):
                        parts.append((lines[k]["x0"], lines[k]["text"].rstrip()))
                        k += 1
                    if parts:
                        ind = max(0, round((parts[0][0] - CODE_BASE_X) / CHAR_W))
                        body = parts[0][1]
                        for _, extra in parts[1:]:
                            body = (body[:-1] if body.endswith("-") else body) + " " + extra
                        code.append(" " * ind + body)
                    else:
                        code.append("")
                    j = k
                    continue
                if is_code_font(l2["font"]):
                    ind = max(0, round((l2["x0"] - CODE_BASE_X) / CHAR_W))
                    code.append(" " * ind + l2["text"].rstrip())
                    j += 1
                    continue
                break
            merged = []
            for c in code:
                if c == "" and merged and merged[-1] == "":
                    continue
                merged.append(c)
            while merged and merged[-1] == "":
                merged.pop()
            els.append({"kind": "code", "lines": merged,
                        "y0": lines[i]["y0"], "y1": lines[j - 1]["y1"] if j > i else lines[i]["y1"]})
            i = j
            continue

        if ln["bold"] and heading_level(ln["size"]) is not None:
            hlv = heading_level(ln["size"])
            hlines = [ln]
            j = i + 1
            if re.match(r"^Chapter\s+\d+$", ln["text"].strip()):
                # "Chapter N" is followed by the chapter title (level 1)
                while j < n and lines[j]["bold"] and heading_level(lines[j]["size"]) == 1:
                    hlines.append(lines[j])
                    j += 1
            else:
                # a numbered heading is followed by its title at the same level
                while j < n and lines[j]["bold"] and heading_level(lines[j]["size"]) == hlv:
                    hlines.append(lines[j])
                    j += 1
            els.append({"kind": "heading", "lines": hlines,
                        "y0": ln["y0"], "y1": hlines[-1]["y1"]})
            i = j
            continue

        if CAPTION_RE.match(ln["text"].strip()) and ln["size"] < 13:
            m = CAPTION_RE.match(ln["text"].strip())
            ckind = m.group(1)
            el = {"kind": "caption", "line": ln, "ckind": ckind,
                  "y0": ln["y0"], "y1": ln["y1"], "region": []}
            if ckind == "Table":
                # a table caption sits *above* its cells
                j = i + 1
                reg = []
                while j < n and not is_code_font(lines[j]["font"]) and not is_lineno(lines[j]) \
                        and not is_body_line(lines[j], in_table(lines[j])) and not is_bullet_line(lines[j]) \
                        and not CAPTION_RE.match(lines[j]["text"].strip()):
                    reg.append(lines[j])
                    j += 1
                if reg:
                    el["region"] = [{"lines": reg}]
                    i = j - 1
            els.append(el)
            i += 1
            continue

        if is_bullet_line(ln):
            items, cur = [], None
            j = i
            while j < n:
                l2 = lines[j]
                if is_bullet_line(l2):
                    if cur:
                        items.append(join_wrapped(cur))
                    cur = [l2["text"][len(l2["spans"][0]["t"]):].strip()]
                elif (abs(l2["x0"] - BODY_LEFT) <= BODY_X_TOL and not l2["bold"]
                      and l2["size"] < 12 and not is_code_font(l2["font"])
                      and not CAPTION_RE.match(l2["text"].strip())):
                    if cur is None:
                        break
                    cur.append(l2["text"].strip())
                else:
                    break
                j += 1
            if cur:
                items.append(join_wrapped(cur))
            if items:
                els.append({"kind": "ul", "items": items,
                            "y0": lines[i]["y0"], "y1": lines[j - 1]["y1"]})
                i = j
                continue
            i += 1
            continue

        if is_body_line(ln, in_table(ln)):
            j, cur = i, [ln]
            while j + 1 < n:
                nxt = lines[j + 1]
                if is_code_font(nxt["font"]) or is_lineno(nxt) or nxt["bold"] or nxt["size"] > 11:
                    break
                if is_bullet_line(nxt) or CAPTION_RE.match(nxt["text"].strip()):
                    break
                if not is_body_line(nxt, in_table(nxt)):
                    break
                cur.append(nxt)
                j += 1
            els.append({"kind": "body", "lines": cur,
                        "y0": lines[i]["y0"], "y1": lines[j]["y1"]})
            i = j + 1
            continue

        # loose text: table cell, figure label, display equation, ...
        j = i
        loose = []
        while j < n and not is_code_font(lines[j]["font"]) and not is_lineno(lines[j]) \
                and not is_body_line(lines[j], in_table(lines[j])) and not is_bullet_line(lines[j]) \
                and not CAPTION_RE.match(lines[j]["text"].strip()):
            loose.append(lines[j])
            j += 1
        if loose:
            els.append({"kind": "loose", "lines": loose,
                        "y0": loose[0]["y0"], "y1": loose[-1]["y1"]})
            i = j
            continue
        i += 1
    return els


def build_table(loose_lines):
    """Group loose lines into table rows / cells."""
    rows = []
    for l in loose_lines:
        placed = False
        for r in rows:
            if abs(l["y0"] - r[0]["y0"]) <= 4.0:
                r.append(l)
                placed = True
                break
        if not placed:
            rows.append([l])
    table = []
    for r in rows:
        cells = sorted(r, key=lambda l: l["x0"])
        table.append([clean(c["text"]).strip() for c in cells])
    return table


BRACE_CHARS = "\uf8f1\uf8f2\uf8f3\uf8f4"


def is_brace_line(ln):
    t = ln["text"].strip()
    return bool(t) and all(ch in BRACE_CHARS for ch in t)


def equation_lines(lines):
    """Indices of the lines that belong to a display equation.

    A display equation is marked by the extensible brace pieces of the
    Computer Modern maths font; the whole vertical band they span belongs
    to the equation.
    """
    groups = {}
    for i, l in enumerate(lines):
        if is_brace_line(l):
            key = round(l["x0"] / 3)
            groups.setdefault(key, []).append(i)
    marked = set()
    for idxs in groups.values():
        y0 = min(lines[i]["y0"] for i in idxs)
        y1 = max(lines[i]["y1"] for i in idxs)
        for i, l in enumerate(lines):
            if y0 - 6 <= l["y0"] <= y1 + 6 and l["x0"] >= 100:
                marked.add(i)
    return marked


def rebuild_equation(lines):
    """Reconstruct a display equation whose big braces are CMEX pieces."""
    if not any(is_brace_line(l) for l in lines):
        return None
    brace_x = None
    rest = []
    for l in lines:
        t = l["text"].strip()
        if not t:
            continue
        if is_brace_line(l):
            brace_x = l["x0"] if brace_x is None else brace_x
            continue
        rest.append(l)
    cols = []
    for l in sorted(rest, key=lambda l: (l["x0"], l["y0"])):
        if cols and abs(cols[-1][0]["x0"] - l["x0"]) < 3:
            cols[-1].append(l)
        else:
            cols.append([l])
    parts = []
    brace_done = brace_x is None
    for c in cols:
        if not brace_done and c[0]["x0"] > brace_x:
            parts.append("{")
            brace_done = True
        txt = " ".join(x["text"].strip() for x in sorted(c, key=lambda l: l["y0"]))
        parts.append(txt)
    if not brace_done:
        parts.insert(0, "{")
    return " ".join(parts) + "}"


def main():
    src, out_path = sys.argv[1], sys.argv[2]
    doc = pymupdf.open(src)
    blocks = []

    # ------------------------------------------------------------------
    # headings need bold/size information, so the walk below re-inspects the
    # first line of every "body" element
    for pno in range(doc.page_count):
        page = doc[pno]
        lines = collect_lines(page)
        graphics = collect_graphics(page)
        is_lineno = make_lineno_checker(page)
        els = build_elements(lines, is_lineno, table_bands(page, lines),
                             equation_lines(lines))
        gidx = 0
        g_floor = HEADER_Y
        pending = []          # loose elements waiting to be claimed by a caption
        i = 0

        def flush_pending():
            """Emit loose elements that no caption claimed."""
            for pe in pending:
                eq = rebuild_equation(pe["lines"])
                if eq is not None:
                    blocks.append({"type": "p", "text": eq, "page": pno + 1,
                                   "kind": "equation"})
                    continue
                txt = join_wrapped([l["text"] for l in pe["lines"]]).strip()
                if txt:
                    blocks.append({"type": "p", "text": txt, "page": pno + 1})
            pending.clear()

        while i < len(els):
            el = els[i]
            kind = el["kind"]
            if kind == "loose":
                pending.append(el)
                i += 1
                continue
            if kind == "heading":
                flush_pending()
                hlines = el["lines"]
                hlv = heading_level(hlines[0]["size"])
                num, title = "", hlines[0]["text"].strip()
                if re.match(r"^\d+(\.\d+)*$", title):
                    num = title
                    if len(hlines) > 1:
                        title = hlines[1]["text"].strip()
                elif re.match(r"^Chapter\s+\d+$", title):
                    num = title
                    if len(hlines) > 1:
                        title = hlines[1]["text"].strip()
                if hlv == 0:
                    blocks.append({"type": "chapter_label", "number": num, "page": pno + 1})
                    if title:
                        blocks.append({"type": "h1", "number": "", "title": title, "page": pno + 1})
                else:
                    blocks.append({"type": f"h{hlv}", "number": num, "title": title, "page": pno + 1})
                g_floor = el["y1"]
                i += 1
                continue
            if kind == "equation":
                flush_pending()
                eq = rebuild_equation(el["lines"])
                if eq:
                    blocks.append({"type": "p", "text": eq, "page": pno + 1,
                                   "kind": "equation"})
                g_floor = el["y1"]
                i += 1
                continue
            if kind == "body":
                flush_pending()
                eq = rebuild_equation(el["lines"])
                if eq is not None:
                    blocks.append({"type": "p", "text": eq, "page": pno + 1,
                                   "kind": "equation"})
                    g_floor = el["y1"]
                    i += 1
                    continue
                txt = join_wrapped([l["text"] for l in el["lines"]]).strip()
                if txt:
                    blocks.append({"type": "p", "text": txt, "page": pno + 1})
                g_floor = el["y1"]
                i += 1
                continue
            if kind == "code":
                flush_pending()
                if any(x.strip() for x in el["lines"]):
                    blocks.append({"type": "code", "lines": el["lines"], "page": pno + 1})
                g_floor = el["y1"]
                i += 1
                continue
            if kind == "ul":
                flush_pending()
                blocks.append({"type": "ul", "items": el["items"], "page": pno + 1})
                g_floor = el["y1"]
                i += 1
                continue
            if kind == "caption":
                ln = el["line"]
                m = CAPTION_RE.match(ln["text"].strip())
                ckind, cnum, ctext = m.group(1), m.group(2), m.group(3).strip()
                region = pending
                pending = []
                if ckind == "Table" and el.get("region"):
                    # table cells live below the caption
                    region = el["region"]
                elif ckind == "Table" and not region:
                    region = []
                gstart = gidx
                while gidx < len(graphics) and graphics[gidx]["bbox"][1] < ln["y0"]:
                    gidx += 1
                gregion = [g for g in graphics[gstart:gidx]
                           if g["bbox"][1] >= g_floor - 4 and g["bbox"][3] <= ln["y0"] + 2]
                blk = {"type": "figure" if ckind == "Figure" else "table",
                       "number": cnum, "caption": ctext, "page": pno + 1}
                loose_lines = [l for r in region for l in r["lines"]]
                if ckind == "Table":
                    tbl = build_table(loose_lines)
                    if tbl:
                        blk["header"] = tbl[0]
                        blk["rows"] = tbl[1:]
                    else:
                        blk["header"], blk["rows"] = [], []
                    blk["ncols"] = max([len(blk["header"])] + [len(r) for r in blk["rows"]] or [0])
                else:
                    blk["labels"] = [clean(l["text"]).strip() for l in loose_lines
                                     if clean(l["text"]).strip()]
                bb = None
                for r in region:
                    for l in r["lines"]:
                        b = [l["x0"], l["y0"], l["x1"], l["y1"]]
                        bb = b if bb is None else [min(bb[0], b[0]), min(bb[1], b[1]),
                                                  max(bb[2], b[2]), max(bb[3], b[3])]
                for g in gregion:
                    b = g["bbox"]
                    bb = b if bb is None else [min(bb[0], b[0]), min(bb[1], b[1]),
                                              max(bb[2], b[2]), max(bb[3], b[3])]
                if bb is not None:
                    blk["bbox"] = [round(v, 2) for v in bb]
                    blk["yrange"] = [round(bb[1], 2), round(bb[3], 2)]
                blocks.append(blk)
                g_floor = ln["y1"]
                i += 1
                continue
            i += 1
        flush_pending()

    # drop the auto-generated table of contents (recreated from headings)
    start = end = None
    for idx, b in enumerate(blocks):
        if b.get("type") == "h1" and b.get("title", "").strip().lower() == "contents":
            start = idx
        if start is not None and b.get("type") == "chapter_label":
            end = idx
            break
    if start is not None and end is not None:
        blocks = blocks[:start] + blocks[end:]

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"source": src, "blocks": blocks}, f, ensure_ascii=False, indent=1)

    from collections import Counter
    c = Counter(b.get("type", "?") for b in blocks)
    print("blocks:", len(blocks))
    for k, v in sorted(c.items()):
        print(f"   {k}: {v}")
    print("chars in p:", sum(len(b.get("text", "")) for b in blocks if b.get("type") == "p"))
    print("chars in ul:", sum(len(" ".join(b.get("items", []))) for b in blocks if b.get("type") == "ul"))
    print("code chars:", sum(len("".join(b.get("lines", []))) for b in blocks if b.get("type") == "code"))


if __name__ == "__main__":
    main()
