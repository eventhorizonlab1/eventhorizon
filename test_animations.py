"""This script contains tests for the animation logic of the Event Horizon website."""

import re

def read_file_content(filepath):
    """Reads and returns the content of a given file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def test_quick_link_hover_animation():
    """Tests that the hover animation for '.quick-link' correctly resets the color.

    This test verifies that the mouseleave event listener for '.quick-link'
    in animations.js includes a color reset animation.

    Raises:
        AssertionError: If the color reset is not found in the mouseleave event listener.
    """
    content = read_file_content('animations.js')

    # Find the mouseleave event listener for quickLinks
    mouseleave_match = re.search(r"link\.addEventListener\('mouseleave', \(\) => {([^}]+)}\);", content, re.DOTALL)
    assert mouseleave_match is not None, "Could not find the mouseleave event listener for '.quick-link'."

    # Check that the color is reset in the mouseleave animation
    animation_block = mouseleave_match.group(1)
    color_reset_match = re.search(r"color:", animation_block)
    assert color_reset_match is not None, "The color is not reset in the mouseleave animation for '.quick-link'."

if __name__ == "__main__":
    test_quick_link_hover_animation()
    print("Test passed: The hover animation for '.quick-link' correctly resets the color.")
