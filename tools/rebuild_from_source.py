"""Rebuild a translated part so that its structure matches the English source.

The English file defines the skeleton: headings, paragraphs, list items,
tables, images and code blocks all keep their original shape and position.
Only the *text* of prose blocks is taken from the translation; code listings
are copied verbatim from the original edition.

Alignment is done on a structural key (fence / code / text) so that the two
files line up even when the prose was translated.
"""
import difflib
import os
import re
import sys

CODE_RE = re.compile(r"^```(\w*)\s*$")


def skeleton(path):
    """Return (items, keys) where items carry the literal file content."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    items = []
    keys = []
    i = 0
    n = len(lines)
    while i < n:
        m = CODE_RE.match(lines[i])
        if m:
            lang = m.group(1)
            body = []
            i += 1
            while i < n and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            items.append(("code", lang, body))
            keys.append(("fence", lang))
            for b in body:
                keys.append(("code",))
            keys.append(("fence", lang))
        else:
            items.append(("text", None, lines[i]))
            keys.append(("text",))
            i += 1
    return items, keys


def main():
    en_path, ru_path = sys.argv[1], sys.argv[2]
    en_items, en_keys = skeleton(en_path)
    ru_items, ru_keys = skeleton(ru_path)

    sm = difflib.SequenceMatcher(None, en_keys, ru_keys, autojunk=False)
    ru_of_en = {}
    for a, b, size in sm.get_matching_blocks():
        for k in range(size):
            ru_of_en[a + k] = b + k

    out = []
    text_seen = 0
    for idx, (kind, lang, val) in enumerate(en_items):
        if kind == "code":
            out.append(("code", lang, val))
            continue
        j = ru_of_en.get(idx)
        if j is None:
            out.append(("text", None, val))
        else:
            rk, rlang, rval = ru_items[j]
            out.append(("text", None, rval))
            text_seen += 1

    with open(ru_path, "w", encoding="utf-8") as f:
        for kind, lang, val in out:
            if kind == "code":
                f.write(f"```{lang}\n" + "\n".join(val) + "\n```\n")
            else:
                f.write(val + "\n")
    print(f"en blocks={len(en_items)} ru blocks={len(ru_items)} "
          f"aligned text lines={text_seen}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
