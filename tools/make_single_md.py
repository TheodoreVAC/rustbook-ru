"""Assemble the whole book into a single, convenient Markdown file.

    python make_single_md.py

The result (`ru/RustBook-RU.md`) contains the title page, the preview
screenshots, a clickable table of contents and all eleven chapters.
Figure references point at the Russian versions of the illustrations
(`images/ru/…`); the untouched originals stay in `images/`.
"""
import os
import re
import unicodedata

ROOT = r"C:\Users\Admin\Documents\RustBook-RU"
RU = os.path.join(ROOT, "ru")
CH = os.path.join(RU, "chapters")
OUT = os.path.join(RU, "RustBook-RU.md")

ORDER = [
    ("00-front-matter.md", "preface", "Предисловие"),
    ("01-rust-basics.md", "ch01", "Глава 1. Основы Rust"),
    ("02-computer-science.md", "ch02", "Глава 2. Информатика"),
    ("03-algorithm-analysis.md", "ch03", "Глава 3. Анализ алгоритмов"),
    ("04-data-structures.md", "ch04", "Глава 4. Базовые структуры данных"),
    ("05-recursion.md", "ch05", "Глава 5. Рекурсия"),
    ("06-search.md", "ch06", "Глава 6. Поиск"),
    ("07-sorting.md", "ch07", "Глава 7. Сортировка"),
    ("08-trees.md", "ch08", "Глава 8. Деревья"),
    ("09-graphs.md", "ch09", "Глава 9. Графы"),
    ("10-practice.md", "ch10", "Глава 10. Практика"),
]

HEAD = """<!--
  Файл изменён по сравнению с оригиналом проекта QMHTMY/RustBook:
  текст переведён на русский язык. Лицензия: Apache License 2.0.
  Оригинал: https://github.com/QMHTMY/RustBook
-->

# Решение задач алгоритмами и структурами данных на Rust

### Русское издание

**Полный перевод** книги *Problem Solving with Algorithms and Data Structures
Using Rust* ([QMHTMY/RustBook](https://github.com/QMHTMY/RustBook)).

| | |
|---|---|
| Автор оригинала | **Шибер (Shieber)** |
| Оригинал | <https://github.com/QMHTMY/RustBook> |
| Лицензия | [Apache License 2.0](../LICENSE) |
| Перевод | RustBook RU — русскоязычное сообщество Rust |
| Объём | 10 глав, 181 раздел, 69 иллюстраций, 467 листингов кода |

> **Это перевод, а не самостоятельная книга.** Авторство, название, состав и
> оформление оригинала принадлежат его правообладателю. Русское издание
> распространяется на тех же условиях — Apache License 2.0; подробности в
> [`NOTICE.md`](../NOTICE.md). Все 467 блоков кода воспроизведены побайтово
> идентично оригиналу, иллюстрации — извлечены из оригинального PDF
> (оригиналы в [`images/`](images), русские версии с переведёнными надписями —
> в [`images/ru/`](images/ru)).

![Обложка русского издания](assets/cover-ru.png)

![Страница книги с боковым оглавлением и текстом](assets/preview-sidebar.png)

![Страница оглавления](assets/preview-toc.png)

---

## Содержание

<!--TOC-->

---

"""


def slug(text):
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = text.replace("ё", "е")
    out = []
    for ch in text:
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


def main():
    chapters = []
    toc = []
    for fname, anchor, label in ORDER:
        path = os.path.join(CH, fname)
        with open(path, encoding="utf-8") as f:
            text = f.read().rstrip()
        # point figures at the Russian versions
        text = text.replace("(images/fig-", "(images/ru/fig-")
        # demote nothing: chapter titles are already "#"
        chapters.append((anchor, label, text))
        toc.append(f"- [{label}](#{anchor})")
        for m in re.finditer(r"^#{2,3} (.+)$", text, re.M):
            title = m.group(1).strip()
            tid = slug(title)
            toc.append(f"  - [{title}](#{anchor}-{tid})")

    parts = [HEAD.replace("<!--TOC-->", "\n".join(toc))]
    for anchor, label, text in chapters:
        # explicit anchors so that the table of contents works on GitHub
        out_lines = []
        for line in text.split("\n"):
            m = re.match(r"^(#{2,3}) (.+)$", line)
            if m:
                title = m.group(2).strip()
                out_lines.append(f'<a id="{anchor}-{slug(title)}"></a>')
                out_lines.append("")
            out_lines.append(line)
        text = "\n".join(out_lines)
        parts.append(f'<a id="{anchor}"></a>\n\n{text}\n\n---\n\n')

    out = "\n".join(parts)
    out = re.sub(r"\n{4,}", "\n\n\n", out)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print(f"{OUT}: {len(out)/1024:.0f} KB, {len(chapters)} chapters, "
          f"{len(toc)} toc entries")


if __name__ == "__main__":
    main()
