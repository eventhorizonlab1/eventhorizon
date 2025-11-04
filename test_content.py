"""
This script contains tests to validate the content of the Event Horizon website.
"""

import os
import re

HTML_FILES = [f for f in os.listdir('.') if f.endswith('.html')]

def read_file_content(filepath):
    """Reads and returns the content of a given file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def test_animation_targets_present():
    """
    Tests that animation target classes are present in the relevant HTML files.
    """
    # Check for .animate-card in articles.html and videos.html
    for filepath in ['articles.html', 'videos.html']:
        content = read_file_content(filepath)
        assert re.search(r'class="[^"]*animate-card[^"]*"', content), f"Missing .animate-card in {filepath}"

def test_contact_form_present():
    """
    Tests that the contact form in contact.html has the required fields.
    """
    content = read_file_content('contact.html')
    # Check for form and required inputs
    assert '<form' in content, "Missing form in contact.html"
    assert 'type="email"' in content, "Missing email input in contact.html"

if __name__ == "__main__":
    test_animation_targets_present()
    print("Test passed: Animation targets are present.")
    test_contact_form_present()
    print("Test passed: Contact form is correctly structured.")
