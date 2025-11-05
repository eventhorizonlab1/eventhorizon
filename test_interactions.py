"""Tests for the UI interactions of the Event Horizon website.

This file is fully documented with Google Style Python Docstrings.
"""

import asyncio
import unittest
from playwright.async_api import async_playwright
import os

class TestInteractions(unittest.TestCase):
    """Test suite for UI interactions.

    This class contains tests to ensure that the JavaScript-based UI
    interactions run correctly in a browser environment.
    """

    @classmethod
    def setUpClass(cls):
        """Set up the browser and page objects for the test class."""
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        cls.playwright = cls.loop.run_until_complete(async_playwright().start())
        cls.browser = cls.loop.run_until_complete(cls.playwright.chromium.launch())

    @classmethod
    def tearDownClass(cls):
        """Tear down the browser and page objects for the test class."""
        cls.loop.run_until_complete(cls.browser.close())
        cls.loop.run_until_complete(cls.playwright.stop())
        cls.loop.close()

    def setUp(self):
        """Set up a new page for each test."""
        self.page = self.loop.run_until_complete(self.browser.new_page())

    def tearDown(self):
        """Close the page after each test."""
        self.loop.run_until_complete(self.page.close())

    def test_main_title_animation(self):
        """Verifies that the main title animation runs correctly.

        This test loads the index.html page and checks the opacity of the
        .main-title element to verify that the animation has run.
        """
        async def run_test(page):
            # Get the absolute path to the HTML file
            file_path = os.path.abspath('index.html')
            await page.goto(f'file://{file_path}')

            # Get the main title element
            main_title = await page.query_selector('.main-title')
            self.assertIsNotNone(main_title, "The .main-title element was not found.")

            # Wait for the animation to complete (duration is 1000ms)
            await page.wait_for_timeout(1500)

            # Check the final opacity (it should be 1)
            final_opacity = await main_title.evaluate('(element) => getComputedStyle(element).opacity')
            self.assertEqual(final_opacity, '1',
                f"Expected final opacity to be 1, but it was {final_opacity}.")

        # Run the async test
        self.loop.run_until_complete(run_test(self.page))

    def test_back_to_top_button(self):
        """Verifies that the 'Back to Top' button works correctly.

        This test loads the index.html page, scrolls down to reveal the
        button, clicks it, and verifies that the page scrolls back to the top.
        """
        async def run_test(page):
            # Get the absolute path to the HTML file
            file_path = os.path.abspath('index.html')
            await page.goto(f'file://{file_path}')

            # Add placeholder content to make the page scrollable
            await page.evaluate('() => { document.body.style.height = "2000px"; }')

            # Get the back to top button
            back_to_top_button = await page.query_selector('#back-to-top')
            self.assertIsNotNone(back_to_top_button, "The 'Back to Top' button was not found.")

            # Check that the button is initially transparent
            initial_opacity = await back_to_top_button.evaluate('(element) => getComputedStyle(element).opacity')
            self.assertEqual(initial_opacity, '0',
                f"Expected initial opacity to be 0, but it was {initial_opacity}.")

            # Scroll down and check that the button becomes visible
            await page.evaluate('() => { window.scrollTo(0, 500); }')
            await page.wait_for_timeout(500)  # Wait for the scroll event to be processed
            final_opacity = await back_to_top_button.evaluate('(element) => getComputedStyle(element).opacity')
            self.assertEqual(final_opacity, '1',
                f"Expected final opacity to be 1 after scrolling, but it was {final_opacity}.")

            # Click the button and check that the page scrolls to the top
            await back_to_top_button.click()
            await page.wait_for_timeout(500)  # Wait for the scroll to complete
            scroll_y = await page.evaluate('() => window.scrollY')
            self.assertEqual(scroll_y, 0,
                f"The page did not scroll to the top after clicking the 'Back to Top' button. Current scrollY: {scroll_y}")

        # Run the async test
        self.loop.run_until_complete(run_test(self.page))

    def test_header_scroll_animation(self):
        """Verifies that the header scroll animation works correctly.

        This test loads the index.html page, scrolls down, and verifies
        that the `scrolled` class is added to the header.
        """
        async def run_test(page):
            # Get the absolute path to the HTML file
            file_path = os.path.abspath('index.html')
            await page.goto(f'file://{file_path}')

            # Get the header element
            header = await page.query_selector('header')
            self.assertIsNotNone(header, "The header element was not found.")

            # Check that the header does not have the `scrolled` class initially
            self.assertFalse('scrolled' in await header.get_attribute('class'),
                "The `scrolled` class was present on the header on initial load.")

            # Scroll down and check that the `scrolled` class is added
            await page.evaluate('() => { window.scrollTo(0, 100); }')
            await page.wait_for_timeout(500)  # Wait for the scroll event to be processed
            self.assertTrue('scrolled' in await header.get_attribute('class'),
                "The `scrolled` class was not added to the header after scrolling down.")

        # Run the async test
        self.loop.run_until_complete(run_test(self.page))

    def test_lazy_loading(self):
        """Verifies that the lazy loading functionality works correctly.

        This test loads the index.html page, scrolls down to a lazy-loaded
        element, and verifies that its `data-src` is loaded into the `src`
        or `background-image` attribute.
        """
        async def run_test(page):
            # Get the absolute path to the HTML file
            file_path = os.path.abspath('index.html')
            await page.goto(f'file://{file_path}')

            # Get a lazy-loaded image
            lazy_image = await page.query_selector('.lazy')
            self.assertIsNotNone(lazy_image, "No lazy-loaded elements were found.")

            # Check that the `src` or `background-image` is initially empty
            tag_name = await lazy_image.evaluate('(element) => element.tagName')
            if tag_name == 'IMG':
                self.assertEqual(await lazy_image.get_attribute('src'), '',
                    "The `src` attribute of the lazy-loaded image was not initially empty.")
            else:
                style = await lazy_image.get_attribute('style')
                self.assertNotIn('background-image', style or '',
                    "The `background-image` style of the lazy-loaded element was not initially empty.")

            # Scroll the element into view
            await lazy_image.scroll_into_view_if_needed()
            await page.wait_for_timeout(500)  # Wait for the IntersectionObserver to trigger

            # Check that the `src` or `background-image` is now loaded
            data_src = await lazy_image.get_attribute('data-src')
            if tag_name == 'IMG':
                self.assertEqual(await lazy_image.get_attribute('src'), data_src,
                    "The `src` attribute of the lazy-loaded image was not updated correctly.")
            else:
                style = await lazy_image.get_attribute('style')
                self.assertIn(data_src, style,
                    "The `background-image` style of the lazy-loaded element was not updated correctly.")

        # Run the async test
        self.loop.run_until_complete(run_test(self.page))

if __name__ == "__main__":
    unittest.main()
