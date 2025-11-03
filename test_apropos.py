"""This script contains tests specifically for the 'À propos' page of the Event Horizon website.

It verifies that all navigation links pointing to the 'À propos' page are correctly formatted.
"""

import re
import os

HTML_FILES = [f for f in os.listdir('.') if f.endswith('.html')]

def read_file_content(filepath):
    """Reads and returns the content of a given file.

    Args:
        filepath (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def test_apropos_links():
    """Tests that all 'À propos' links on the 'À propos' page point to the correct URL.

    This test specifically checks 'a-propos.html' to ensure that all internal links
    to the 'À propos' page itself are not broken.

    Raises:
        AssertionError: If fewer than two 'À propos' links are found, or if any of
                        them have an incorrect href attribute.
    """
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
