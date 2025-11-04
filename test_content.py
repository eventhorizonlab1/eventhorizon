"""Tests to validate the content of the Event Horizon website."""

import os
import re

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

def test_animation_targets_present():
    """Verifies that animation target classes exist in the HTML.

    This test checks `articles.html` and `videos.html` to ensure that
    elements with the `.animate-card` class are present, which are
    required for animations to trigger.

    Raises:
        AssertionError: If `.animate-card` is not found in the relevant files.
    """
    # Check for .animate-card in articles.html and videos.html
    for filepath in ['articles.html', 'videos.html']:
        content = read_file_content(filepath)
        assert re.search(r'class="[^"]*animate-card[^"]*"', content), f"Missing .animate-card in {filepath}"

def test_contact_form_present():
    """Ensures the contact form is correctly structured.

    This test checks `contact.html` to confirm that it contains a `<form>`
    element and an email input field (`type="email"`), which are essential
    for the contact page to function.

    Raises:
        AssertionError: If the form or email input is missing.
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
