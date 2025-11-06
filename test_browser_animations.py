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

    def test_menu_item_hover_animation(self):
        """Verify that the menu item hover animation restores the original color."""
        self.page.goto("file://" + os.path.abspath("index.html"))
        # Wait for dark mode styles to be applied
        self.page.wait_for_timeout(500)
        menu_item = self.page.query_selector('.menu-item')
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

    def test_main_title_animation(self):
        """Verify that the main title animation runs on page load."""
        self.page.goto("file://" + os.path.abspath("index.html"))
        main_title = self.page.wait_for_selector('.main-title')

        # Wait for the animation to complete by checking for opacity to be 1
        main_title.wait_for_element_state('visible')

        opacity = main_title.evaluate('(element) => getComputedStyle(element).opacity')
        transform = main_title.evaluate('(element) => getComputedStyle(element).transform')

        self.assertEqual(float(opacity), 1)
        self.assertNotEqual(transform, 'none')

    def test_header_animation(self):
        """Verify that the header animation runs on page load."""
        self.page.goto("file://" + os.path.abspath("index.html"))

        header_logo = self.page.wait_for_selector('header h2')
        nav_links = self.page.query_selector_all('header nav a')
        theme_toggle = self.page.wait_for_selector('#theme-toggle')

        # The nav links animate with a stagger. Wait for the last one to be fully visible.
        if nav_links:
            last_nav_link = nav_links[-1]
            self.page.wait_for_function(
                "(element) => parseFloat(getComputedStyle(element).opacity) > 0.95",
                arg=last_nav_link
            )

        logo_opacity = header_logo.evaluate('(element) => getComputedStyle(element).opacity')
        self.assertGreater(float(logo_opacity), 0.9)

        for link in nav_links:
            link_opacity = link.evaluate('(element) => getComputedStyle(element).opacity')
            self.assertGreater(float(link_opacity), 0.9)

        theme_toggle_opacity = theme_toggle.evaluate('(element) => getComputedStyle(element).opacity')
        self.assertGreater(float(theme_toggle_opacity), 0.9)
