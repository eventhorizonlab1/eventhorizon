import re

def test_alpine_version():
    """Tests that the Alpine.js CDN link is the correct version.

    This test reads the index.html file and searches for a specific CDN link to
    Alpine.js v2.8.2. It asserts that the link is present.
    """
    with open("index.html", "r") as f:
        content = f.read()

    # Search for the script tag loading Alpine.js
    match = re.search(r'<script defer src="(https://cdn.jsdelivr.net/gh/alpinejs/alpine@v2.8.2/dist/alpine.min.js)"></script>', content)

    # Assert that a match is found
    assert match is not None, "Alpine.js v2.8.2 CDN link not found!"

if __name__ == "__main__":
    test_alpine_version()
    print("Test passed: Alpine.js CDN link is correct.")
