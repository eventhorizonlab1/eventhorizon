import unittest
from playwright.sync_api import sync_playwright
import os

class TestBrowserAnimations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.page = self.browser.new_page()

    def tearDown(self):
        self.page.close()

    def test_page_title(self):
        """Verify that the page title is correct."""
        self.page.goto("file://" + os.path.abspath("index.html"))
        self.assertEqual(self.page.title(), "Event Horizon - Votre source sur l'industrie spatiale européenne")

    def test_logo_hover_animation(self):
        """Verify that the logo hover animation is triggered."""
        self.page.goto("file://" + os.path.abspath("index.html"))
        logo = self.page.query_selector('.logo-container')
        self.assertIsNotNone(logo, "Logo container not found.")

        # Get the initial state of the logo's transform property
        initial_transform = self.page.evaluate('(element) => getComputedStyle(element).transform', logo)

        # Hover over the logo
        logo.hover()

        # Wait for the animation to complete
        self.page.wait_for_timeout(500)

        # Get the final state of the logo's transform property
        final_transform = self.page.evaluate('(element) => getComputedStyle(element).transform', logo)

        # Assert that the transform property has changed
        self.assertNotEqual(initial_transform, final_transform, "Logo hover animation did not change the transform property.")

    def test_back_to_top_button(self):
        """Verify that the 'Back to Top' button appears and functions correctly."""
        self.page.goto("file://" + os.path.abspath("index.html"))

        # Scroll down to make the button appear
        self.page.evaluate('window.scrollTo(0, 500)')

        # Wait for the button to appear
        self.page.wait_for_selector('#back-to-top', state='visible')

        button = self.page.query_selector('#back-to-top')
        self.assertIsNotNone(button, "'Back to Top' button not found.")

        # Click the button
        button.click()

        # Wait for the scroll to complete
        self.page.wait_for_function('() => window.scrollY === 0')

        # Assert that the page has scrolled to the top
        self.assertEqual(self.page.evaluate('() => window.scrollY'), 0,
                         "'Back to Top' button did not scroll to the top of the page.")
