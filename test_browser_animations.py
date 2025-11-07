"""Tests for browser-based animations on the Event Horizon website.

This module uses Playwright to simulate user interactions and verify
that the JavaScript-based animations behave as expected in a live browser
environment. This file is fully documented with Google Style Python Docstrings.
"""

import unittest
from playwright.sync_api import sync_playwright
import os

class TestBrowserAnimations(unittest.TestCase):
    """Test suite for browser-based animations.

    This class contains tests that use Playwright to interact with the website
    and verify that the animations are triggered correctly.
    """
    @classmethod
    def setUpClass(cls):
        """Initializes the Playwright browser instance."""
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        """Closes the Playwright browser instance."""
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        """Creates a new page for each test."""
        self.page = self.browser.new_page()

    def tearDown(self):
        """Closes the page after each test."""
        self.page.close()

    def test_page_title(self):
        """Verifies that the page title is correct."""
        self.page.goto("file://" + os.path.abspath("index.html"))
        self.assertEqual(self.page.title(), "Event Horizon - Votre source sur l'industrie spatiale européenne")



    def test_menu_item_hover_animation(self):
        """Verifies that the menu item hover animation restores the original color."""
        self.page.goto("file://" + os.path.abspath("index.html"))
        # Wait for dark mode styles to be applied
        self.page.wait_for_timeout(500)
        menu_item = self.page.query_selector('nav a')
        self.assertIsNotNone(menu_item, "Menu item not found.")

        # Get the initial color of the menu item
        initial_color = self.page.evaluate('(element) => getComputedStyle(element).color', menu_item)

        # Hover over the menu item
        menu_item.hover()

        # Wait for the animation to complete
        self.page.wait_for_timeout(500)

        # Get the hover color of the menu item
        hover_color = self.page.evaluate('(element) => getComputedStyle(element).color', menu_item)

        # Assert that the color has changed
        self.assertNotEqual(initial_color, hover_color, "Menu item hover animation did not change the color.")

        # Move the mouse away from the menu item
        self.page.mouse.move(0, 0)

        # Wait for the animation to complete
        self.page.wait_for_timeout(500)

        # Get the final color of the menu item
        final_color = self.page.evaluate('(element) => getComputedStyle(element).color', menu_item)

        # Assert that the color has been restored
        self.assertEqual(initial_color, final_color, "Menu item hover animation did not restore the original color.")


