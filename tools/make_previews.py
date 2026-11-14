"""Render preview screenshots of the HTML book for the README / combined Markdown."""
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = r"C:\Users\Admin\Documents\RustBook-RU"
HTML = os.path.join(ROOT, "ru", "build", "index.html")
OUT = os.path.join(ROOT, "ru", "assets")
os.makedirs(OUT, exist_ok=True)

SHOTS = [
    # (name, anchor to scroll to, viewport width, height)
    ("preview-sidebar.png", None, 1600, 900),
    ("preview-toc.png", "toc", 1600, 900),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, anchor, w, h in SHOTS:
        page = browser.new_page(viewport={"width": w, "height": h},
                                device_scale_factor=2)
        page.goto("file:///" + HTML.replace("\\", "/"))
        page.wait_for_load_state("networkidle")
        if anchor:
            page.evaluate(f"document.querySelector('#{anchor}').scrollIntoView()")
        else:
            page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(400)
        path = os.path.join(OUT, name)
        page.screenshot(path=path)
        print(path, os.path.getsize(path) // 1024, "KB")
        page.close()
    browser.close()
