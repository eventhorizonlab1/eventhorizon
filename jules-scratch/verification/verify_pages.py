import os
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    pages = [
        "index.html",
        "videos.html",
        "articles.html",
        "podcasts.html",
        "contact.html",
        "industrie-spatiale-europeenne.html",
        "ingenierie-spatiale.html",
        "ecosysteme-toulousain.html",
        "a-propos.html",
        "mentions-legales.html",
        "politique-de-confidentialite.html",
    ]

    for i, page_name in enumerate(pages):
        abs_path = os.path.abspath(page_name)
        page.goto(f"file://{abs_path}")
        page.screenshot(path=f"jules-scratch/verification/screenshot-{i}.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
