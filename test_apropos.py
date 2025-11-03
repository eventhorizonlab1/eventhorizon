
import re
import os

HTML_FILES = [f for f in os.listdir('.') if f.endswith('.html')]

def read_file_content(filepath):
    """Reads and returns the content of a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def test_apropos_links():
    """Tests that all 'À propos' links on the 'À propos' page are correct."""
    content = read_file_content('a-propos.html')

    # Find all 'À propos' links
    matches = re.findall(r'<a[^>]*>À Propos</a>', content)

    # Check that there are at least two such links (header and footer)
    assert len(matches) >= 2, "Expected at least two 'À propos' links in a-propos.html"

    # Check that all 'À propos' links have the correct href
    for match in matches:
        assert 'href="a-propos.html"' in match, f"Incorrect 'À propos' link found: {match}"

if __name__ == "__main__":
    test_apropos_links()
    print("Test passed: All 'À propos' links on the 'À propos' page are correct.")
