"""
This script contains tests for the lazy loading functionality of the Event Horizon website.
"""

import re

def read_file_content(filepath):
    """Reads and returns the content of a given file.

    Args:
        filepath (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def test_lazy_loading_on_index_page():
    """
    Tests that the images on the index.html page are using the 'lazy' class.
    """
    content = read_file_content('index.html')

    # Find all divs that should be lazy-loaded
    image_divs = re.findall(r'<div[^>]+data-alt="[^"]+"[^>]*>', content)

    # Check that each of these divs has the 'lazy' class and a 'data-src' attribute
    for div in image_divs:
        assert 'lazy' in div, f"Image div does not have the 'lazy' class: {div}"
        assert 'data-src' in div, f"Image div does not have the 'data-src' attribute: {div}"

if __name__ == "__main__":
    try:
        test_lazy_loading_on_index_page()
        print("Test passed: All images on the index page are using lazy loading.")
    except AssertionError as e:
        print(f"Test failed: {e}")
        # Exit with a non-zero status code to indicate failure
        exit(1)
