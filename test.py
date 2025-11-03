import re
import os

# List of all HTML files to be tested
HTML_FILES = [f for f in os.listdir('.') if f.endswith('.html')]

def read_file_content(filepath):
    """Reads and returns the content of a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def test_alpine_version():
    """Tests that the Alpine.js CDN link is the correct version in all HTML files."""
    for filepath in HTML_FILES:
        content = read_file_content(filepath)
        match = re.search(r'<script defer src="https://cdn.jsdelivr.net/gh/alpinejs/alpine@v2.8.2/dist/alpine.min.js"></script>', content)
        assert match is not None, f"Alpine.js v2.8.2 CDN link not found in {filepath}!"

def test_tailwind_cdn_present():
    """Tests that the Tailwind CSS CDN link is present in all HTML files."""
    for filepath in HTML_FILES:
        content = read_file_content(filepath)
        match = re.search(r'<script src="https://cdn.tailwindcss.com"></script>', content)
        assert match is not None, f"Tailwind CSS CDN link not found in {filepath}!"

def test_header_present():
    """Tests that the main header is present in all HTML files."""
    for filepath in HTML_FILES:
        content = read_file_content(filepath)
        match = re.search(r'<header.*>.*<h2.*>Event Horizon</h2>.*</header>', content, re.DOTALL)
        assert match is not None, f"Header with logo not found in {filepath}!"

def test_footer_present():
    """Tests that the main footer is present in all HTML files."""
    for filepath in HTML_FILES:
        content = read_file_content(filepath)
        match = re.search(r'<footer.*>.*© 2024 Event Horizon. Tous droits réservés..*</footer>', content, re.DOTALL)
        assert match is not None, f"Footer with copyright notice not found in {filepath}!"

def test_navigation_links_present():
    """Tests that the main navigation links are present in all HTML files."""
    nav_links = [
        'href="index.html"',
        'href="videos.html"',
        'href="articles.html"',
        'href="ecosysteme.html"',
        'href="a-propos.html"',
        'href="contact.html"'
    ]
    for filepath in HTML_FILES:
        content = read_file_content(filepath)
        for link in nav_links:
            assert link in content, f"Navigation link {link} not found in {filepath}!"

def test_language_switcher_present():
    """Tests that the language switcher is present in all HTML files."""
    for filepath in HTML_FILES:
        content = read_file_content(filepath)
        match = re.search(r'<a class="text-white px-2 py-1 rounded-md" href="#">FR</a>\s*<span class="text-white/30">/</span>\s*<a class="text-white/60 hover:text-white px-2 py-1 rounded-md transition-colors" href="#">EN</a>', content)
        assert match is not None, f"Language switcher not found in {filepath}!"

if __name__ == "__main__":
    # Run all tests
    test_alpine_version()
    print("Test passed: Alpine.js CDN link is correct in all files.")
    test_tailwind_cdn_present()
    print("Test passed: Tailwind CSS CDN link is present in all files.")
    test_header_present()
    print("Test passed: Header is present in all files.")
    test_footer_present()
    print("Test passed: Footer is present in all files.")
    test_navigation_links_present()
    print("Test passed: Navigation links are present in all files.")
    test_language_switcher_present()
    print("Test passed: Language switcher is present in all files.")

    print("\nAll tests passed successfully!")
