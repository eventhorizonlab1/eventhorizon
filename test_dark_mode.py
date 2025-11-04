"""Tests for the dark mode functionality of the Event Horizon website."""

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

def test_quick_link_dark_mode_color_reset():
    """Verifies that '.quick-link' hover animation is theme-aware.

    This test checks the `mouseleave` event handler in `documentation.js`
    to ensure that the text color is not hardcoded to a light theme value,
    which would be incorrect when dark mode is active.

    Raises:
        AssertionError: If a hardcoded light-theme color is found.
    """
    content = read_file_content('documentation.js')

    # Find the mouseleave event listener for quickLinks within setupQuickLinkHovers
    mouseleave_match = re.search(r"link\.addEventListener\('mouseleave', \(\) => {([^}]+)}\);", content, re.DOTALL)
    assert mouseleave_match is not None, "Could not find the mouseleave event listener for '.quick-link'."

    animation_block = mouseleave_match.group(1)

    # Check that the color is not hardcoded to the light theme value.
    # This test will fail before the fix.
    hardcoded_color = "color: 'rgba(0, 0, 0, 0.6)'"
    assert hardcoded_color not in animation_block, (
        f"Found hardcoded light-theme color '{hardcoded_color}' in the mouseleave animation for '.quick-link'. "
        "This is incorrect for dark mode."
    )

if __name__ == "__main__":
    try:
        test_quick_link_dark_mode_color_reset()
        print("Test passed: The '.quick-link' mouseleave animation does not use a hardcoded light-theme color.")
    except AssertionError as e:
        print(f"Test failed: {e}")
        # Exit with a non-zero status code to indicate failure
        exit(1)
