"""Extract untranslated paragraphs for gap filling and apply the translations.

    python apply_gaps.py list <part.ru.md> <gaps.json>
    python apply_gaps.py apply <part.ru.md> <gaps.json> <translations.json>

The translations file is a JSON array of strings, one per gap, in the same
order as the gap list.  Only the text of the listed paragraphs is replaced;
the surrounding structure is never touched.
"""
import json
import os
import sys

from find_gaps import blocks, is_english


def gap_indices(path, threshold=0.10):
    bl = blocks(path)
    out = []
    for bi, (kind, val) in enumerate(bl):
        if kind != "para":
            continue
        if is_english(val, threshold):
            out.append(bi)
    return out, bl


def cmd_list(path, out):
    idxs, bl = gap_indices(path)
    gaps = [bl[i][1] for i in idxs]
    with open(out, "w", encoding="utf-8") as f:
        json.dump(gaps, f, ensure_ascii=False, indent=1)
    print(f"{len(gaps)} gap(s) -> {out}")


def cmd_apply(path, gaps_json, tr_json):
    idxs, bl = gap_indices(path)
    gaps = json.load(open(gaps_json, encoding="utf-8"))
    tr = json.load(open(tr_json, encoding="utf-8"))
    if len(tr) != len(gaps):
        print(f"ERROR: {len(tr)} translations for {len(gaps)} gaps")
        return 1
    mapping = dict(zip(idxs, tr))
    out = []
    for bi, (kind, val) in enumerate(bl):
        if kind == "para" and bi in mapping:
            out.append(("para", mapping[bi]))
        else:
            out.append((kind, val))
    with open(path, "w", encoding="utf-8") as f:
        for kind, val in out:
            if kind == "code":
                lang, body = val
                f.write(f"```{lang}\n" + "\n".join(body) + "\n```\n")
            else:
                f.write((val if val is not None else "") + "\n")
    print(f"applied {len(tr)} translation(s) to {path}")
    return 0


if __name__ == "__main__":
    if sys.argv[1] == "list":
        cmd_list(sys.argv[2], sys.argv[3])
    else:
        sys.exit(cmd_apply(sys.argv[2], sys.argv[3], sys.argv[4]))
