"""Verifies that the website's JavaScript functions are working correctly.

This module contains a suite of browser-based tests for the Event Horizon
website, using Playwright to ensure that the JavaScript functions in
`documentation.js` are behaving as expected.
"""

import asyncio
import unittest
import os
from playwright.async_api import async_playwright

class TestBrowserDocumentation(unittest.TestCase):
    """Test suite for JavaScript functionality in the browser.

    This class sets up a Playwright browser instance and runs tests to verify
    the correct behavior of JavaScript functions, such as animations and
    event listeners. It ensures that the core JavaScript logic is functioning
    as expected in a real browser environment.
    """
    @classmethod
    def setUpClass(cls):
        """Sets up the browser and event loop for the test class.

        This method is called once before any tests in this class are run.
        It sets up a Playwright browser instance and an asyncio event loop.
        """
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        cls.playwright = cls.loop.run_until_complete(async_playwright().start())
        cls.browser = cls.loop.run_until_complete(cls.playwright.chromium.launch(headless=True))

    @classmethod
    def tearDownClass(cls):
        """Tears down the browser and event loop after the tests.

        This method is called once after all tests in this class have been run.
        It closes the Playwright browser instance and the asyncio event loop.
        """
        cls.loop.run_until_complete(cls.browser.close())
        cls.loop.run_until_complete(cls.playwright.stop())
        cls.loop.close()

    def setUp(self):
        """Sets up a new page for each test.

        This method is called before each test in this class is run.
        It creates a new Playwright page for each test to ensure that
        tests are isolated from each other.
        """
        self.page = self.loop.run_until_complete(self.browser.new_page())

    def tearDown(self):
        """Tears down the page after each test.

        This method is called after each test in this class is run.
        It closes the Playwright page to ensure that resources are
        cleaned up correctly.
        """
        self.loop.run_until_complete(self.page.close())

    def test_anime_is_defined(self):
        """Verifies that the anime.js library is defined on the page.

        This test ensures that the `anime` function is available in the global
        scope, which is crucial for all animations to work. Without anime.js,
        the site's animations would fail to run.
        """
        async def run_test():
            """Runs the anime.js definition test steps.

            Navigates to the index page and checks if the anime.js library
            has been successfully loaded and is available in the global scope.
            """
            await self.page.goto('http://localhost:8000/index.html')
            anime_defined = await self.page.evaluate('typeof anime')
            self.assertEqual(anime_defined, 'function')

        self.loop.run_until_complete(run_test())

    def test_theme_switcher(self):
        """Verifies that the theme switcher toggles the 'dark' class.

        This test simulates a user clicking the theme toggle button and
        asserts that the 'dark' class is correctly applied to the HTML element,
        switching the page to dark mode.
        """
        async def run_test():
            """Runs the theme switcher test steps."""
            await self.page.goto('http://localhost:8000/index.html')
            # Check initial state (should not be dark)
            html_class = await self.page.evaluate('document.documentElement.className')
            self.assertNotIn('dark', html_class)

            # Click the theme toggle button
            await self.page.click('#theme-toggle')

            # Verify that the 'dark' class is now present
            html_class = await self.page.evaluate('document.documentElement.className')
            self.assertIn('dark', html_class)

            # Click again to toggle back
            await self.page.click('#theme-toggle')
            html_class = await self.page.evaluate('document.documentElement.className')
            self.assertNotIn('dark', html_class)

        self.loop.run_until_complete(run_test())

    def test_language_switcher(self):
        """Verifies that the language switcher updates the text content.

        This test simulates a user clicking the language switcher and asserts
        that the text content of a key element is updated with the correct
        translation.
        """
        async def run_test():
            """Runs the language switcher test steps."""
            await self.page.goto('http://localhost:8000/index.html')

            # Check initial language (French)
            h1_text = await self.page.inner_text('h1.main-title')
            self.assertIn("l'industrie spatiale européenne", h1_text)

            # Click the 'EN' language link
            await self.page.click('a[data-lang="en"]')

            # Wait for the text to update
            await self.page.wait_for_function('''() => {
                const el = document.querySelector('h1.main-title');
                return el && el.innerText.includes('European space industry');
            }''')

            # Verify that the text has been translated to English
            h1_text = await self.page.inner_text('h1.main-title')
            self.assertIn("European space industry", h1_text)

        self.loop.run_until_complete(run_test())

    def test_particle_network_initialization(self):
        """Verifies that the particle network canvas is created."""
        async def run_test():
            """Runs the particle network initialization test steps."""
            await self.page.goto('http://localhost:8000/index.html')

            # Wait for the canvas to be created
            await self.page.wait_for_selector('#particle-network')

            # Verify that the canvas is inside the container
            canvas_handle = await self.page.query_selector('#particle-container > #particle-network')
            self.assertIsNotNone(canvas_handle)

        self.loop.run_until_complete(run_test())


if __name__ == '__main__':
    unittest.main()
