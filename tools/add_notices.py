"""Add the Apache-2.0 §4(b) change notice to every translated Markdown file.

The notice is an HTML comment, so it does not alter the Markdown structure and
the structural verification continues to pass unchanged.
"""
import glob
import os

ROOT = r"C:\Users\Admin\Documents\RustBook-RU\ru"

NOTICE = ("<!--\n"
          "  Файл изменён по сравнению с оригиналом проекта QMHTMY/RustBook:\n"
          "  текст переведён на русский язык. Лицензия: Apache License 2.0.\n"
          "  Оригинал: https://github.com/QMHTMY/RustBook\n"
          "-->\n")

targets = sorted(glob.glob(os.path.join(ROOT, "chapters", "*.md")))
targets.append(os.path.join(ROOT, "RustBook-RU.md"))

for path in targets:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if text.lstrip().startswith("<!--\n  Файл изменён"):
        continue
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(NOTICE + text)
    print("notified:", os.path.basename(path))
