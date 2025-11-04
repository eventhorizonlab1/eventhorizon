"""
This script contains a test to verify the correct implementation of the animation logic
in the `animations.js` file.
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

def test_animation_logic():
    """
    Tests that `animations.js` uses the correct `anime({...})` and `anime.stagger()` calls.

    This test is designed to fail if the incorrect `animate({...})` or `stagger()` calls are present,
    which are bugs caused by an incorrect destructuring of the `anime` object.

    Raises:
        AssertionError: If the incorrect destructuring or function calls are found.
    """
    content = read_file_content('animations.js')

    # 1. Check for the incorrect destructuring
    incorrect_destructuring = re.search(r'const\s*{\s*animate,\s*stagger\s*}\s*=\s*anime;', content)
    assert incorrect_destructuring is None, "Found incorrect destructuring of anime object in animations.js: `const { animate, stagger } = anime;`"

    # 2. Check for incorrect `animate` calls
    incorrect_animate_calls = re.findall(r'\banimate\({', content)
    assert len(incorrect_animate_calls) == 0, f"Found {len(incorrect_animate_calls)} incorrect calls to `animate` in animations.js. Use `anime` instead."

    # 3. Check for incorrect `stagger` calls (should be `anime.stagger`)
    incorrect_stagger_calls = re.findall(r'delay:\s*stagger\(', content)
    assert len(incorrect_stagger_calls) == 0, f"Found incorrect calls to `stagger` in animations.js. Use `anime.stagger` instead."

if __name__ == "__main__":
    test_animation_logic()
    print("Test passed: animations.js uses the correct `anime` and `anime.stagger` functions.")
