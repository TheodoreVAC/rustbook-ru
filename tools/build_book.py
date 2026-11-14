"""Build the Russian edition of RustBook: a single-page HTML book and a PDF.

    python build_book.py [--pdf]

The HTML book is one self-contained page with a table of contents, chapter
anchors and navigation; the PDF is rendered from the same HTML with
Chromium so that both formats share identical typography.
"""
import argparse
import html
import os
import re
import shutil
import sys
import time

import markdown

ROOT = r"C:\Users\Admin\Documents\RustBook-RU"
RU = os.path.join(ROOT, "ru")
CHAPTERS = os.path.join(RU, "chapters")
BUILD = os.path.join(RU, "build")
IMAGES = os.path.join(RU, "images")

TITLE = "Решение задач алгоритмами и структурами данных на Rust"
SUBTITLE = "Русское издание"
AUTHOR = "Шибер (Shieber)"
TRANSLATOR = "Проект русского перевода RustBook"
VERSION = "1.0"

ORDER = [
    ("00-front-matter.md", "Предисловие", "preface"),
    ("01-rust-basics.md", "Глава 1. Основы Rust", "ch01"),
    ("02-computer-science.md", "Глава 2. Информатика", "ch02"),
    ("03-algorithm-analysis.md", "Глава 3. Анализ алгоритмов", "ch03"),
    ("04-data-structures.md", "Глава 4. Базовые структуры данных", "ch04"),
    ("05-recursion.md", "Глава 5. Рекурсия", "ch05"),
    ("06-search.md", "Глава 6. Поиск", "ch06"),
    ("07-sorting.md", "Глава 7. Сортировка", "ch07"),
    ("08-trees.md", "Глава 8. Деревья", "ch08"),
    ("09-graphs.md", "Глава 9. Графы", "ch09"),
    ("10-practice.md", "Глава 10. Практика", "ch10"),
]

MD_EXTENSIONS = ["extra", "tables", "fenced_code", "toc", "sane_lists", "attr_list"]


def render_markdown(text):
    md = markdown.Markdown(extensions=MD_EXTENSIONS, output_format="html")
    body = md.convert(text)
    toc = md.toc
    return body, toc


def slugify(text):
    s = re.sub(r"<[^>]+>", "", text).strip().lower()
    s = re.sub(r"[^0-9a-zа-яё]+", "-", s, flags=re.UNICODE)
    return s.strip("-") or "sec"


def build_html():
    os.makedirs(BUILD, exist_ok=True)
    chapters = []
    toc_entries = []

    for fname, label, anchor in ORDER:
        path = os.path.join(CHAPTERS, fname)
        if not os.path.exists(path):
            print(f"  !! missing chapter file: {fname}")
            continue
        with open(path, encoding="utf-8") as f:
            md_text = f.read()
        body, _ = render_markdown(md_text)

        # rewrite internal heading anchors so that they are unique per chapter
        seen = {}
        def fix_ids(m):
            raw = m.group(1)
            sid = slugify(raw)
            if sid in seen:
                seen[sid] += 1
                sid = f"{sid}-{seen[sid]}"
            else:
                seen[sid] = 0
            return f'id="{sid}"'

        body = re.sub(r'id="([^"]+)"', fix_ids, body)
        chapters.append((anchor, label, body, fname))

    # ---------------------------------------------------------------- TOC
    toc_html = []
    for anchor, label, body, fname in chapters:
        toc_html.append(f'<li class="toc-chapter"><a href="#{anchor}">{html.escape(label)}</a></li>')
        for m in re.finditer(r'<h([23]) id="([^"]+)">(.*?)</h\1>', body, re.S):
            lvl, sid, inner = m.group(1), m.group(2), m.group(3)
            text = re.sub(r"<[^>]+>", "", inner).strip()
            toc_html.append(f'<li class="toc-sec toc-l{lvl}"><a href="#{anchor}-{sid}">{html.escape(text)}</a></li>')

    # ---------------------------------------------------------------- body
    toc_page = ['<section class="chapter toc-page" id="toc"><h1>Содержание</h1><ol class="toc-print">']
    for anchor, label, body, fname in chapters:
        toc_page.append(f'<li><a href="#{anchor}">{html.escape(label)}</a></li>')
        subs = []
        for m in re.finditer(r'<h([23]) id="([^"]+)">(.*?)</h\1>', body, re.S):
            lvl, sid, inner = m.group(1), m.group(2), m.group(3)
            text = re.sub(r"<[^>]+>", "", inner).strip()
            subs.append((lvl, sid, text))
        if subs:
            toc_page.append('<ol class="toc-sub">')
            for lvl, sid, text in subs:
                toc_page.append(f'<li class="toc-l{lvl}"><a href="#{anchor}-{sid}">{html.escape(text)}</a></li>')
            toc_page.append('</ol>')
    toc_page.append('</ol></section>')
    toc_page_html = "".join(toc_page)

    parts = []
    parts.append(f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITLE)} — {html.escape(SUBTITLE)}</title>
<style>{CSS}</style>
</head>
<body>
<div class="layout">
<nav class="sidebar">
  <div class="sidebar-head">
    <div class="sidebar-title">{html.escape(TITLE)}</div>
    <div class="sidebar-sub">{html.escape(SUBTITLE)}</div>
  </div>
  <ul class="toc">
    {''.join(toc_html)}
  </ul>
</nav>
<main class="content">
<section class="cover">
  <div class="cover-rule"></div>
  <h1 class="cover-title">{html.escape(TITLE)}</h1>
  <div class="cover-sub">{html.escape(SUBTITLE)}</div>
  <div class="cover-rule"></div>
  <p class="cover-author">Автор оригинала: <b>{html.escape(AUTHOR)}</b></p>
  <p class="cover-meta">Русский перевод · {html.escape(VERSION)}</p>
  <p class="cover-note">Полный перевод книги <i>Problem Solving with Algorithms and Data Structures Using Rust</i>.
  Оригинал: <a href="https://github.com/QMHTMY/RustBook">github.com/QMHTMY/RustBook</a>.</p>
</section>
{toc_page_html}
""")

    nav = []
    for i, (anchor, label, body, fname) in enumerate(chapters):
        prev = chapters[i - 1][1] if i > 0 else None
        nxt = chapters[i + 1][1] if i + 1 < len(chapters) else None
        p = f'<a class="nav-prev" href="#{chapters[i-1][0]}">← {html.escape(prev)}</a>' if prev else '<span></span>'
        n = f'<a class="nav-next" href="#{chapters[i+1][0]}">{html.escape(nxt)} →</a>' if nxt else '<span></span>'
        nav.append(f'<div class="ch-nav">{p}<span class="nav-home"><a href="#top">↑ Оглавление</a></span>{n}</div>')
        parts.append(f"""
<section class="chapter" id="{anchor}">
  {nav[-1]}
  {body}
</section>
""")

    parts.append("""
</main>
</div>
<script>
(function () {
  var links = [].slice.call(document.querySelectorAll('.toc a'));
  var targets = links.map(function (a) { return document.querySelector(a.getAttribute('href')); });
  function onScroll() {
    var best = 0;
    for (var i = 0; i < targets.length; i++) {
      if (targets[i] && targets[i].getBoundingClientRect().top < 120) best = i;
    }
    links.forEach(function (a, i) { a.classList.toggle('active', i === best); });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === 'PageDown') { window.scrollBy(0, innerHeight * 0.9); }
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') { window.scrollBy(0, -innerHeight * 0.9); }
    if (e.key === 'Home') { location.hash = 'top'; }
  });
})();
</script>
</body>
</html>
""")

    out = os.path.join(BUILD, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write("".join(parts))
    return out, chapters


CSS = r"""
:root {
  --ink: #1c1c1e;
  --ink-soft: #3a3a3c;
  --muted: #6b6b70;
  --accent: #8a3324;
  --accent-soft: #b5563f;
  --rule: #d8d3cb;
  --code-bg: #f6f4ef;
  --code-border: #e2ded4;
  --page-bg: #f2efe9;
  --serif: "Cambria", "Constantia", "Georgia", "Times New Roman", serif;
  --mono: "Consolas", "Cascadia Mono", "Courier New", monospace;
}

* { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  margin: 0;
  background: var(--page-bg);
  color: var(--ink);
  font-family: var(--serif);
  font-size: 17px;
  line-height: 1.62;
}

.layout { display: flex; align-items: flex-start; }

/* ------------------------------------------------------------- sidebar */
.sidebar {
  position: sticky;
  top: 0;
  width: 320px;
  flex: 0 0 320px;
  height: 100vh;
  overflow-y: auto;
  padding: 26px 18px 60px 26px;
  background: #fbfaf7;
  border-right: 1px solid var(--rule);
}
.sidebar-head { margin-bottom: 18px; }
.sidebar-title { font-size: 15px; font-weight: 700; line-height: 1.35; }
.sidebar-sub { font-size: 13px; color: var(--muted); margin-top: 3px; }
.toc { list-style: none; margin: 0; padding: 0; font-size: 13.5px; line-height: 1.42; }
.toc li { margin: 0; }
.toc a {
  display: block;
  padding: 3px 6px 3px 8px;
  color: var(--ink-soft);
  text-decoration: none;
  border-left: 2px solid transparent;
}
.toc a:hover { color: var(--accent); background: #f1ece3; }
.toc a.active { color: var(--accent); border-left-color: var(--accent); background: #f1ece3; }
.toc-chapter { margin-top: 12px; }
.toc-chapter a { font-weight: 700; color: var(--ink); }
.toc-l2 { padding-left: 16px !important; font-size: 13px; }
.toc-l3 { padding-left: 28px !important; font-size: 12.5px; color: var(--muted); }

/* ------------------------------------------------------------- content */
.content {
  flex: 1 1 auto;
  max-width: 940px;
  margin: 0 auto;
  padding: 30px 40px 120px;
}

.chapter {
  background: #fff;
  padding: 46px 56px 54px;
  margin-bottom: 34px;
  border: 1px solid var(--rule);
  box-shadow: 0 1px 3px rgba(0,0,0,.05);
}

.cover { text-align: center; padding: 70px 20px 80px; }
.cover-rule { width: 120px; height: 2px; background: var(--accent); margin: 0 auto 26px; }
.cover-rule + .cover-rule { margin: 26px auto 30px; }
.cover-title { font-size: 40px; line-height: 1.2; margin: 0 0 12px; letter-spacing: .2px; }
.cover-sub { font-size: 21px; color: var(--accent); margin-bottom: 8px; }
.cover-author { font-size: 17px; margin: 18px 0 4px; }
.cover-meta { color: var(--muted); font-size: 15px; margin: 0 0 26px; }
.cover-note { color: var(--muted); font-size: 14px; max-width: 620px; margin: 0 auto; line-height: 1.55; }

h1, h2, h3, h4 {
  font-weight: 700;
  color: var(--ink);
  line-height: 1.25;
  page-break-after: avoid;
  break-after: avoid;
}
h1 { font-size: 30px; margin: 6px 0 26px; padding-bottom: 12px; border-bottom: 3px solid var(--accent); }
h2 { font-size: 23px; margin: 42px 0 14px; padding-bottom: 7px; border-bottom: 1px solid var(--rule); }
h3 { font-size: 19px; margin: 30px 0 10px; color: var(--accent); }

p { margin: 0 0 13px; text-align: justify; hyphens: auto; }
.content li p, .content li { text-align: justify; }

ul, ol { margin: 0 0 15px; padding-left: 26px; }
li { margin: 4px 0; }

a { color: var(--accent-soft); }
strong { color: #000; }

code {
  font-family: var(--mono);
  font-size: .88em;
  background: var(--code-bg);
  border: 1px solid var(--code-border);
  border-radius: 3px;
  padding: 1px 4px;
}

pre {
  font-family: var(--mono);
  background: var(--code-bg);
  border: 1px solid var(--code-border);
  border-left: 3px solid var(--accent-soft);
  border-radius: 4px;
  padding: 12px 14px;
  margin: 0 0 18px;
  overflow-x: auto;
  font-size: 13.2px;
  line-height: 1.48;
  white-space: pre-wrap;
  word-break: break-word;
  page-break-inside: avoid;
  break-inside: avoid;
}
pre code { background: none; border: none; padding: 0; font-size: 1em; }

table {
  border-collapse: collapse;
  width: 100%;
  margin: 6px 0 20px;
  font-size: 14.5px;
  page-break-inside: avoid;
  break-inside: avoid;
}
th, td { border: 1px solid var(--rule); padding: 6px 9px; text-align: left; vertical-align: top; }
th { background: #f0ece4; font-weight: 700; }
tr:nth-child(even) td { background: #faf8f4; }

img {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 14px auto 6px;
  page-break-inside: avoid;
  break-inside: avoid;
}

blockquote {
  margin: 16px 0;
  padding: 8px 18px;
  border-left: 3px solid var(--rule);
  color: var(--ink-soft);
}

hr { border: none; border-top: 1px solid var(--rule); margin: 30px 0; }

.toc-page ol { list-style: none; padding-left: 0; margin: 0; }
.toc-page > ol > li { font-weight: 700; font-size: 15px; margin: 9px 0 3px; }
.toc-page .toc-sub { margin: 0 0 6px 14px; font-size: 13.4px; font-weight: 400; }
.toc-page .toc-sub li { margin: 1px 0; }
.toc-page .toc-l3 { margin-left: 16px !important; color: var(--muted); font-size: 12.6px; }
.toc-page a { color: var(--ink-soft); text-decoration: none; }
.toc-page a:hover { color: var(--accent); }

.ch-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  font-size: 13.5px;
  font-family: var(--mono);
  color: var(--muted);
  margin-bottom: 26px;
  padding-bottom: 10px;
  border-bottom: 1px dashed var(--rule);
}
.ch-nav a { text-decoration: none; color: var(--muted); }
.ch-nav a:hover { color: var(--accent); }
.nav-home { flex: 0 0 auto; }

/* ---------------------------------------------------------- print / pdf */
@page {
  size: 170mm 245mm;
  margin: 16mm 15mm 16mm 15mm;
}

@media print {
  html, body { background: #fff; }
  body { font-size: 10.4pt; line-height: 1.52; }
  .layout { display: block; }
  .sidebar { display: none; }
  .content { max-width: none; margin: 0; padding: 0; }
  .chapter {
    background: none; border: none; box-shadow: none;
    padding: 0; margin: 0;
    page-break-before: always;
    break-before: page;
  }
  .cover { page-break-after: always; break-after: page; padding-top: 30mm; }
  .cover-title { font-size: 30pt; }
  .ch-nav { display: none; }
  h1 { font-size: 20pt; }
  h2 { font-size: 15pt; margin-top: 22pt; }
  h3 { font-size: 12.6pt; }
  pre { font-size: 8.6pt; padding: 8px 10px; }
  table { font-size: 9.4pt; }
  p, li { orphans: 3; widows: 3; }
  a { color: inherit; text-decoration: none; }
  img { max-height: 78mm; }
}
"""


def build_pdf(html_path, out_pdf):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("file:///" + html_path.replace("\\", "/"))
        page.wait_for_load_state("networkidle")
        page.emulate_media(media="print")
        page.pdf(
            path=out_pdf,
            format="A5",
            print_background=True,
            display_header_footer=True,
            header_template=(
                '<div style="font-size:7px;color:#8a8a8a;width:100%;'
                'padding:0 12mm;font-family:Georgia,serif;">'
                '<span style="float:left">Решение задач алгоритмами и структурами данных на Rust</span>'
                '</div>'
            ),
            footer_template=(
                '<div style="font-size:8px;color:#8a8a8a;width:100%;'
                'padding:0 12mm;font-family:Georgia,serif;text-align:center;">'
                '<span class="pageNumber"></span>'
                '</div>'
            ),
            margin={"top": "14mm", "bottom": "14mm", "left": "13mm", "right": "13mm"},
        )
        browser.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", action="store_true")
    args = ap.parse_args()

    out, chapters = build_html()
    size = os.path.getsize(out)
    print(f"HTML: {out}  ({size/1024:.1f} KB, {len(chapters)} sections)")

    # copy images next to the HTML so that relative links work; the Russian
    # versions (translated labels) take precedence over the originals
    img_out = os.path.join(BUILD, "images")
    if os.path.isdir(img_out):
        shutil.rmtree(img_out)
    shutil.copytree(IMAGES, img_out)
    ru_imgs = os.path.join(IMAGES, "ru")
    if os.path.isdir(ru_imgs):
        for n in os.listdir(ru_imgs):
            if n.endswith(".png"):
                shutil.copyfile(os.path.join(ru_imgs, n), os.path.join(img_out, n))
        print(f"Russian figure labels applied: "
              f"{len([n for n in os.listdir(ru_imgs) if n.endswith('.png')])}")

    if args.pdf:
        pdf = os.path.join(BUILD, "rust-book-ru.pdf")
        t0 = time.time()
        build_pdf(out, pdf)
        print(f"PDF : {pdf}  ({os.path.getsize(pdf)/1024/1024:.2f} MB, "
              f"{time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
