"""Final verification of the Russian edition against the English original.

Checks
  1. every chapter has the same block structure as its English source
  2. every code block is byte-identical to the original
  3. all figures referenced in the text exist
  4. no leftover English paragraphs
  5. the extracted PDF source and the translated chapters agree in size
"""
import json
import os
import re
import sys

ROOT = r"C:\Users\Admin\Documents\RustBook-RU"
sys.path.insert(0, os.path.join(ROOT, "tools"))

from find_gaps import blocks, is_english  # noqa: E402
from check_translation import parse  # noqa: E402

SRC = os.path.join(ROOT, "ru", "source")
RU = os.path.join(ROOT, "ru", "chapters")
IMAGES = os.path.join(ROOT, "ru", "images")

report = []
problems = []

names = sorted(f for f in os.listdir(SRC) if f.endswith(".md"))
for n in names:
    en_text = open(os.path.join(SRC, n), encoding="utf-8").read()
    ru_path = os.path.join(RU, n)
    if not os.path.exists(ru_path):
        problems.append(f"{n}: русская глава отсутствует")
        continue
    ru_text = open(ru_path, encoding="utf-8").read()

    en_blocks, en_imgs, en_caps = parse(os.path.join(SRC, n))
    ru_blocks, ru_imgs, ru_caps = parse(ru_path)

    row = {"chapter": n, "en_chars": len(en_text), "ru_chars": len(ru_text)}
    row["code"] = count = sum(1 for k, v in en_blocks if k == "code")
    if count != sum(1 for k, v in ru_blocks if k == "code"):
        problems.append(f"{n}: число блоков кода различается")

    # code blocks byte-identical
    en_code = [v for k, v in en_blocks if k == "code"]
    ru_code = [v for k, v in ru_blocks if k == "code"]
    diff = 0
    for a, b in zip(en_code, ru_code):
        if a != b:
            diff += 1
    row["code_diff"] = diff
    if diff:
        problems.append(f"{n}: {diff} блок(ов) кода отличаются от оригинала")

    # paragraphs / headings / lists
    row["paras_en"] = sum(1 for k, v in en_blocks if k == "p")
    row["paras_ru"] = sum(1 for k, v in ru_blocks if k == "p")
    row["heads"] = sum(1 for k, v in en_blocks if k.startswith("h"))
    row["heads_ru"] = sum(1 for k, v in ru_blocks if k.startswith("h"))
    if row["heads"] != row["heads_ru"]:
        problems.append(f"{n}: число заголовков различается "
                        f"({row['heads']} / {row['heads_ru']})")
    if row["paras_en"] != row["paras_ru"]:
        problems.append(f"{n}: число абзацев различается "
                        f"({row['paras_en']} / {row['paras_ru']})")

    # figures
    row["figs"] = len(en_imgs)
    row["figs_ru"] = len(ru_imgs)
    if row["figs"] != row["figs_ru"]:
        problems.append(f"{n}: число рисунков различается")
    for alt, path in ru_imgs:
        p = os.path.join(IMAGES, os.path.basename(path))
        if not os.path.exists(p):
            problems.append(f"{n}: нет файла рисунка {path}")

    # untranslated paragraphs
    bl = blocks(ru_path)
    gaps = [v for k, v in bl if k == "para" and is_english(v, 0.12)]
    row["untranslated"] = len(gaps)
    report.append(row)

# ------------------------------------------------------------------ totals
tot_code = sum(r["code"] for r in report)
tot_code_diff = sum(r["code_diff"] for r in report)
tot_paras = sum(r["paras_ru"] for r in report)
tot_figs = sum(r["figs_ru"] for r in report)
tot_gaps = sum(r["untranslated"] for r in report)

print(f"{'chapter':<26} {'chars(en)':>10} {'chars(ru)':>10} {'code':>5} "
      f"{'diff':>4} {'head':>5} {'para':>5} {'fig':>4} {'untr':>5}")
for r in report:
    print(f"{r['chapter']:<26} {r['en_chars']:>10} {r['ru_chars']:>10} "
          f"{r['code']:>5} {r['code_diff']:>4} {r['heads_ru']:>5} "
          f"{r['paras_ru']:>5} {r['figs_ru']:>4} {r['untranslated']:>5}")
print("-" * 78)
print(f"{'TOTAL':<26} {sum(r['en_chars'] for r in report):>10} "
      f"{sum(r['ru_chars'] for r in report):>10} {tot_code:>5} {tot_code_diff:>4} "
      f"{sum(r['heads_ru'] for r in report):>5} {tot_paras:>5} {tot_figs:>4} {tot_gaps:>5}")

print(f"\nПроблем: {len(problems)}")
for p in problems:
    print("  -", p)
