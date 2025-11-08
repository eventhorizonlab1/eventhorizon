"""Verifies that the website's JavaScript functions are working correctly.

This script contains a suite of browser-based tests for the Event Horizon
website, using Playwright to ensure that the JavaScript functions in
`documentation.js` are behaving as expected.
This file is fully documented with Google Style Python Docstrings.
"""

import asyncio
import unittest
import os
from playwright.async_api import async_playwright

class TestBrowserDocumentation(unittest.TestCase):
    """Test suite for JavaScript functionality in the browser.

    This class sets up a Playwright browser instance and runs tests to verify
    the correct behavior of JavaScript functions, such as animations and
    event listeners.
    """
    @classmethod
    def setUpClass(cls):
        """Sets up the browser and event loop for the test class."""
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        cls.playwright = cls.loop.run_until_complete(async_playwright().start())
        cls.browser = cls.loop.run_until_complete(cls.playwright.chromium.launch(headless=True))

    @classmethod
    def tearDownClass(cls):
        """Tears down the browser and event loop after the tests."""
        cls.loop.run_until_complete(cls.browser.close())
        cls.loop.run_until_complete(cls.playwright.stop())
        cls.loop.close()

    def setUp(self):
        """Sets up a new page for each test."""
        self.page = self.loop.run_until_complete(self.browser.new_page())

    def tearDown(self):
        """Tears down the page after each test."""
        self.loop.run_until_complete(self.page.close())

    def test_anime_is_defined(self):
        """Verifies that the anime.js library is defined on the page.

        This test ensures that the `anime` function is available in the global
        scope, which is crucial for all animations to work.
        """
        async def run_test():
            await self.page.goto('file://' + os.path.abspath('index.html'))
            anime_defined = await self.page.evaluate('typeof anime')
            self.assertEqual(anime_defined, 'function')

        self.loop.run_until_complete(run_test())

    def test_header_scroll_animation(self):
        """Verifies the header scroll animation.

        This test checks that the 'scrolled' class is correctly added to the
        header when the user scrolls down, and removed when they scroll back
        to the top.
        """
        async def run_test():
            await self.page.goto('file://' + os.path.abspath('index.html'))

            # Get header element
            header = await self.page.query_selector('header')
            self.assertIsNotNone(header, "Header element not found")

            # 1. Check initial state
            initial_class = await header.get_attribute('class')
            self.assertNotIn('scrolled', initial_class or '', "Header should not have 'scrolled' class initially")

            # 2. Scroll down and check for 'scrolled' class
            await self.page.evaluate('window.scrollTo(0, 100)')
            await self.page.wait_for_timeout(500)

            scrolled_class = await header.get_attribute('class')
            self.assertIn('scrolled', scrolled_class or '', "Header should have 'scrolled' class after scrolling down")

            # 3. Scroll back to top and check for 'scrolled' class removal
            await self.page.evaluate('window.scrollTo(0, 0)')
            await self.page.wait_for_timeout(500)

            final_class = await header.get_attribute('class')
            self.assertNotIn('scrolled', final_class or '', "Header should not have 'scrolled' class after scrolling to top")

        self.loop.run_until_complete(run_test())

    def test_quick_link_hover_effect(self):
        """Verifies the hover effect on the footer's quick links.

        This test ensures that the 'text-primary' class is added to a quick
        link on hover and removed when the mouse moves away.
        """
        async def run_test():
            await self.page.goto('file://' + os.path.abspath('index.html'))

            # Find the "À Propos" link in the footer
            quick_link = await self.page.query_selector('footer a[href="a-propos.html"]')
            self.assertIsNotNone(quick_link, "Quick link not found")

            # 1. Check initial color
            initial_color = await quick_link.evaluate('(element) => window.getComputedStyle(element).color')

            # 2. Hover over the link and check for color change
            await quick_link.hover()
            await self.page.wait_for_timeout(500) # Wait for animation

            hover_color = await quick_link.evaluate('(element) => window.getComputedStyle(element).color')
            self.assertNotEqual(initial_color, hover_color, "Quick link color should change on hover")

            # 3. Move the mouse away and check for color to revert
            await self.page.mouse.move(0, 0)
            await self.page.wait_for_timeout(500) # Wait for animation

            final_color = await quick_link.evaluate('(element) => window.getComputedStyle(element).color')
            self.assertEqual(initial_color, final_color, "Quick link color should revert after hover")

        self.loop.run_until_complete(run_test())

if __name__ == '__main__':
    unittest.main()
