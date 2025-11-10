"""Tests for the internationalization (i18n) and language switching functionality.

This module contains a suite of browser-based tests for the Event Horizon
website, using Playwright to ensure that the language switcher is functioning
correctly. It verifies that the content of the page is correctly translated
when the user switches between French and English.
"""

import asyncio
import unittest
import os
from playwright.async_api import async_playwright

class TestInternationalization(unittest.TestCase):
    """Test suite for internationalization and language switching.

    This class uses Playwright to conduct browser-based tests on the language
    switching functionality. It verifies that when a user clicks the language
    switcher, the content of the page is correctly translated. This is a critical
    test for a bilingual website.
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

    def test_language_switcher(self):
        """Verifies that the language switcher correctly changes the page content.

        This test simulates a user switching between French and English and
        verifies that the content is updated accordingly. This is a crucial
        feature for a bilingual website.
        """
        async def run_test():
            """Runs the language switcher test steps.

            This async function navigates to the page, checks the initial
            language, switches to English and verifies the change, then switches
            back to French and verifies the change again.
            """
            await self.page.goto('http://localhost:8000/index.html')

            # Check the initial language (French)
            french_title = "Event Horizon : Dans les coulisses de l'industrie spatiale européenne"
            main_title_element = await self.page.query_selector('[data-i18n-key="main_title"]')
            initial_title = await main_title_element.inner_text()
            self.assertEqual(initial_title.strip(), french_title)

            # Switch to English
            await self.page.click('a[data-lang="en"]')

            english_title = "Event Horizon: Behind the scenes of the European space industry"
            await self.page.wait_for_function(f'''
                () => document.querySelector('[data-i18n-key="main_title"]').innerText.trim() === "{english_title}"
            ''')

            # Check for the English title
            translated_title = await main_title_element.inner_text()
            self.assertEqual(translated_title.strip(), english_title)

            # Switch back to French
            await self.page.click('a[data-lang="fr"]')
            await self.page.wait_for_function(f'''
                () => document.querySelector('[data-i18n-key="main_title"]').innerText.trim() === "{french_title}"
            ''')

            # Check for the French title again
            reverted_title = await main_title_element.inner_text()
            self.assertEqual(reverted_title.strip(), french_title)

        self.loop.run_until_complete(run_test())

if __name__ == '__main__':
    unittest.main()
