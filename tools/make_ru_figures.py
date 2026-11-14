"""Create Russian versions of the figures.

The original artwork is taken from the English edition.  For figures that
carry instructional labels, the English text is redacted from the PDF page
and replaced with the Russian wording; the surrounding vector artwork is left
untouched.  The result is rendered to PNG at the same resolution as the
original figure.

    python make_ru_figures.py <pdf> <figures.json> <outdir>
"""
import json
import os
import re
import sys

import pymupdf

PDF = sys.argv[1]
FIGJSON = sys.argv[2]
OUT = sys.argv[3]
DPI = 300
FONT = "C:/Windows/Fonts/times.ttf"

# English label -> Russian label.  API names, personal names, company names
# and numeric data are deliberately left as they are.
LABELS = {
    # --- stack of hardware layers (fig. 4.1) -------------------------
    "Computer": "Компьютер",
    "Integrated Circuit": "Интегральная схема",
    "Transistor": "Транзистор",
    "Semicondutor": "Полупроводник",
    "Energy band theory": "Теория энергетических зон",
    "Quantum mechanics": "Квантовая механика",
    "top": "верх",
    "bottom": "низ",
    # --- operating-system layers (fig. 2.2) ---------------------------
    "User": "Пользователь",
    "Interface": "Интерфейс",
    "Shell": "Оболочка",
    "Kernnel": "Ядро",
    "Operations": "Операции",
    # --- data structures ----------------------------------------------
    "deque": "дек",
    "stack": "стек",
    "List": "Список",
    "head": "голова",
    "Head": "Голова",
    # --- parenthesis matching (fig. 4.3) ------------------------------
    "first matched parenthesis": "первая сопоставленная скобка",
    "last matched parenthesis": "последняя сопоставленная скобка",
    # --- AVL rotations (fig. 8.8) -------------------------------------
    "left rotation": "левый поворот",
    "right rotation": "правый поворот",
    "relocate": "перемещение",
    # --- BST insertion (fig. 8.6) --------------------------------------
    "insert 19": "вставить 19",
    "insert 24": "вставить 24",
    "insert 31": "вставить 31",
    "insert 44": "вставить 44",
    "insert 56": "вставить 56",
    "insert 66": "вставить 66",
    "insert 72": "вставить 72",
    # --- course prerequisites (fig. 9.6 / 9.7) -------------------------
    "algebra": "алгебра",
    "calculus": "математический анализ",
    "derivatives": "производные",
    "equations": "уравнения",
    "functions": "функции",
    "probability theory": "теория вероятностей",
    "calculus probability": "математический анализ, теория вероятностей",
    "function derivation equation": "уравнение производной функции",
    # --- cooking a pancake (fig. 9.8) ---------------------------------
    "1 egg": "1 яйцо",
    "1 tablespoon olive oil": "1 столовая ложка оливкового масла",
    "3/4 cup milk": "3/4 стакана молока",
    "3/4 cup of milk": "3/4 стакана молока",
    "Heat the pan": "Нагреть сковороду",
    "Mix": "Смешать",
    "Pour in 1/4 cup": "Влить 1/4 стакана",
    "Flip the bottom until golden": "Перевернуть до румяной корочки",
    "Heat the sauce": "Подогреть соус",
    "Enjoy": "Приятного аппетита",
}


def spans_in(page, bbox):
    """Text spans fully inside bbox."""
    x0, y0, x1, y1 = bbox
    out = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] == 1:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                sx0, sy0, sx1, sy1 = s["bbox"]
                if sx0 >= x0 - 2 and sx1 <= x1 + 2 and sy0 >= y0 - 2 and sy1 <= y1 + 2:
                    out.append(s)
    return out


FONT_OBJ = pymupdf.Font(fontfile=FONT)


def make_ru_figure(doc, fig, outdir):
    page = doc[fig["page"] - 1]
    bbox = fig.get("bbox")
    if not bbox:
        return None
    spans = spans_in(page, bbox)
    jobs = []
    for s in spans:
        key = s["text"].strip()
        ru = LABELS.get(key)
        if not ru:
            continue
        size = s["size"]
        rect = pymupdf.Rect(s["bbox"])
        # Russian words are longer; allow some extra room but shrink to fit
        limit = rect.width * 2.4
        width = FONT_OBJ.text_length(ru, fontsize=size)
        if width > limit:
            size = max(4.5, size * limit / width)
            width = FONT_OBJ.text_length(ru, fontsize=size)
        x = rect.x0 + (rect.width - width) / 2
        y = rect.y1 - (rect.height - size) * 0.35
        jobs.append((rect, ru, x, y, size))
        page.add_redact_annot(rect, fill=None)

    if jobs:
        # redactions first: they would otherwise remove the new text as well
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                              graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
        page.insert_font(fontname="cyr", fontfile=FONT)
        for rect, ru, x, y, size in jobs:
            page.insert_text((x, y), ru, fontname="cyr", fontsize=size, color=(0, 0, 0))
    changed = len(jobs)
    if changed:
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                              graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    clip = pymupdf.Rect(*bbox) + (-3, -3, 3, 3)
    pix = page.get_pixmap(clip=clip, dpi=DPI, alpha=False)
    path = os.path.join(outdir, f"fig-{fig['number']}.png")
    pix.save(path)
    return changed, path


def main():
    os.makedirs(OUT, exist_ok=True)
    doc = pymupdf.open(PDF)
    figs = json.load(open(FIGJSON, encoding="utf-8"))
    total = 0
    touched = []
    for fig in figs:
        res = make_ru_figure(doc, fig, OUT)
        if res and res[0]:
            total += res[0]
            touched.append((fig["number"], res[0]))
    doc.save(os.path.join(OUT, "_ru_figures.pdf"))
    print(f"translated labels: {total}")
    for n, c in touched:
        print(f"  fig-{n}.png: {c} label(s)")
    print(f"output: {OUT}")


if __name__ == "__main__":
    main()
