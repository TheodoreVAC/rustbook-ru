# Сборка русского издания RustBook

Русское издание собирается из Markdown-файлов в `ru/chapters/` в
самодостаточный HTML-файл и PDF.

---

## 1. Требования

* **Python 3.10+**
* пакеты: `markdown`, `pymupdf`, `playwright`
* **Chromium** для рендеринга PDF (устанавливается отдельно)

```bash
pip install markdown pymupdf playwright
python -m playwright install chromium
```

Шрифты: Cambria (основной текст) и Consolas (код) — входят в состав
Windows. При их отсутствии используются Georgia / Times New Roman и
Cascadia Mono / Courier New.

---

## 2. Сборка

```bash
cd C:\Users\Admin\Documents\RustBook-RU

# только HTML
python tools\build_book.py

# HTML + PDF
python tools\build_book.py --pdf

# очистка обложки PDF от колонтитулов и статистика
python tools\pdf_post.py ru\build\rust-book-ru.pdf --clean
```

Результат:

| Файл | Описание |
|---|---|
| `ru/build/index.html` | HTML-книга с боковым оглавлением, переходами по главам и навигацией «предыдущая / следующая глава» |
| `ru/build/images/` | иллюстрации (русские версии приоритетнее оригиналов) |
| `ru/build/rust-book-ru.pdf` | PDF-книга, формат A5 (420 × 596 pt) |

Параметры печати заданы в `tools/build_book.py` (`build_pdf`):
формат A5, поля 13–14 мм, колонтитул с названием книги, номер страницы
внизу по центру.

---

## 3. Структура проекта

```
RustBook-RU/
├── README.md                  ← описание проекта (этот уровень)
├── LICENSE                    ← Apache License 2.0 (копия оригинала)
├── NOTICE.md                  ← уведомление о переводе
├── TRANSLATION_PROGRESS.md    ← прогресс и статус работ
├── original/                  ← оригинальный репозиторий, не изменялся
├── ru/                        ← русское издание
│   ├── README.md
│   ├── glossary.md            ← глоссарий
│   ├── STYLE_GUIDE.md         ← правила перевода
│   ├── TRANSLATION_NOTES.md   ← изменения при переводе
│   ├── BUILD.md               ← этот файл
│   ├── QA_REPORT.md           ← отчёт о качестве
│   ├── chapters/              ← главы в Markdown (11 файлов)
│   ├── images/                ← 69 иллюстраций (оригиналы)
│   │   └── ru/                ← русские версии иллюстраций
│   ├── code/                  ← исходники примеров (как в оригинале)
│   ├── source/                ← английский текст, извлечённый из PDF
│   └── build/                 ← собранная книга
└── tools/                     ← конвейер сборки и проверок
```

---

## 4. Проверки

```bash
# 4.1. Итоговая сверка издания с оригиналом
python tools\final_check.py

# 4.2. Пофрагментная проверка перевода
python tools\check_translation.py ru\source\04-data-structures.md \
       ru\chapters\04-data-structures.md ru\images

# 4.3. Полнота извлечения оригинала из PDF
python tools\verify_chars.py original\books\rust-book-en-us-shieber.pdf \
       tools\extract\en\book.json 6,7,8,9

# 4.4. Сверка заголовков с оглавлением оригинального PDF
python tools\compare_toc.py original\books\rust-book-en-us-shieber.pdf \
       tools\extract\en\book.json

# 4.5. Поиск непереведённых абзацев
python tools\find_gaps.py ru\chapters\04-data-structures.md
```

`tools\final_check.py` — основная проверка: сравнивает число заголовков,
абзацев, таблиц и рисунков с английским источником и сверяет **побайтово**
все блоки кода.

---

## 5. Пересборка исходника из PDF

Если оригинальный PDF обновится, английский источник и иллюстрации
пересобираются так:

```bash
python tools\extract_book.py original\books\rust-book-en-us-shieber.pdf \
       tools\extract\en\book.json
python tools\verify_chars.py original\books\rust-book-en-us-shieber.pdf \
       tools\extract\en\book.json 6,7,8,9
python tools\extract_figures.py original\books\rust-book-en-us-shieber.pdf \
       tools\extract\en\book.json ru\images 300
python tools\make_markdown.py tools\extract\en\book.json ru\source \
       original\publication\code
python tools\prepare_jobs.py 45000
python tools\make_ru_figures.py original\books\rust-book-en-us-shieber.pdf \
       ru\images\_figures.json ru\images\ru
```

---

## 6. Перевод нового фрагмента

```bash
python tools\apply_gaps.py list ru\work\<глава>\part-XXX.ru.md \
       ru\work\<глава>\gaps.json
# … перевести найденные абзацы …
python tools\apply_gaps.py apply ru\work\<глава>\part-XXX.ru.md \
       ru\work\<глава>\gaps.json ru\work\<глава>\gaps.ru.json
python tools\merge_chapters.py
python tools\final_check.py
```
