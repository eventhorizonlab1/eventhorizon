"""
This script contains tests to verify the integrity of internal links in the Event Horizon website.
"""

import os
import re

HTML_FILES = [f for f in os.listdir('.') if f.endswith('.html')]
ALL_FILES = [f for f in os.listdir('.')]

def read_file_content(filepath):
    """Reads and returns the content of a given file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def test_internal_links():
    """
    Tests that all internal links in HTML files point to existing files.
    """
    for filepath in HTML_FILES:
        content = read_file_content(filepath)
        # Find all internal links (hrefs not starting with http)
        links = re.findall(r'href="([^"]+)"', content)
        internal_links = [l for l in links if not l.startswith('http') and not l.startswith('#')]

        for link in internal_links:
            # a-propos.html contains a link to "a-propos.html" which is valid
            if link == "a-propos.html":
                assert "a-propos.html" in HTML_FILES, f"Broken link in {filepath}: {link}"
            else:
                assert link in ALL_FILES, f"Broken link in {filepath}: {link}"

if __name__ == "__main__":
    test_internal_links()
    print("Test passed: All internal links are valid.")
