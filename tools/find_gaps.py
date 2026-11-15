"""List the prose blocks of a translated part that are still in English.

Used to drive the final gap-filling pass; the index returned is the position
of the block in the file's block sequence (text blocks only).
"""
import json
import os
import re
import sys

CODE_RE = re.compile(r"^```(\w*)\s*$")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
EN_WORD = re.compile(
    r"\b(the|and|of|to|is|are|that|this|with|for|from|which|can|will|when|"
    r"there|their|its|not|but|has|been|was|were|we|our|it|as|be|by|on|"
    r"in|an|a|or|than|then|also|so|because|where|while|after|before)\b", re.I)


def blocks(path):
    text = HTML_COMMENT.sub("", open(path, encoding="utf-8").read())
    lines = text.split("\n")
    out = []
    i = 0
    n = len(lines)
    while i < n:
        m = CODE_RE.match(lines[i])
        if m:
            lang = m.group(1)
            i += 1
            body = []
            while i < n and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            out.append(("code", (lang, body)))
            continue
        if lines[i].startswith("|") or lines[i].startswith("!["):
            out.append(("raw", lines[i]))
            i += 1
            continue
        if not lines[i].strip():
            out.append(("blank", None))
            i += 1
            continue
        para = [lines[i]]
        i += 1
        while i < n and lines[i].strip() and not lines[i].startswith(
                ("#", "|", "![", "```", "- ", "*Figure")):
            para.append(lines[i])
            i += 1
        out.append(("para", "\n".join(para)))
    return out


def is_english(text, threshold=0.10):
    words = text.split()
    if len(words) < 8:
        return False
    hits = len(EN_WORD.findall(text))
    return hits / len(words) > threshold


def main():
    path = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.10
    bl = blocks(path)
    idx = 0
    gaps = []
    for kind, val in bl:
        if kind != "para":
            continue
        if is_english(val, threshold):
            gaps.append({"index": idx, "text": val})
        idx += 1
    print(json.dumps(gaps, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
