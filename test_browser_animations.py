"""Verifies that browser animations and interactions work as expected.

This script contains a suite of browser-based tests for the Event Horizon
website, using Playwright to ensure that animations and interactive elements
are functioning correctly.
This file is fully documented with Google Style Python Docstrings.
"""

import asyncio
import unittest
import os
from playwright.async_api import async_playwright
import http.server
import socketserver
import threading

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

class TestBrowserAnimations(unittest.TestCase):
    """Test suite for browser-based animations and interactions.

    This class sets up a Playwright browser instance and runs tests to verify
    the correct behavior of animations and interactive elements on the website.
    """

    @classmethod
    def setUpClass(cls):
        """Sets up the browser and event loop for the test class."""
        cls.server = socketserver.TCPServer(("", PORT), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        cls.playwright = cls.loop.run_until_complete(async_playwright().start())
        cls.browser = cls.loop.run_until_complete(cls.playwright.chromium.launch(headless=True))

    @classmethod
    def tearDownClass(cls):
        """Tears down the browser and event loop after the tests."""
        cls.loop.run_until_complete(cls.browser.close())
        cls.loop.run_until_complete(cls.playwright.stop())
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        cls.loop.close()

    def setUp(self):
        """Sets up a new page for each test."""
        self.page = self.loop.run_until_complete(self.browser.new_page())

    def tearDown(self):
        """Tears down the page after each test."""
        self.loop.run_until_complete(self.page.close())

    def test_page_title(self):
        """Verifies that the page title is correct."""
        async def run_test():
            """Runs the page title test steps."""
            await self.page.goto(f'http://localhost:{PORT}/index.html')
            self.assertEqual(await self.page.title(), "Event Horizon - Dans les coulisses de l'industrie spatiale européenne")
        self.loop.run_until_complete(run_test())

    def test_navigation_scroll(self):
        """Verifies that clicking the navigation links scrolls to the correct section."""
        async def run_test():
            """Runs the navigation scroll test steps."""
            await self.page.goto(f'http://localhost:{PORT}/index.html')
            await self.page.click('a[href="#videos"]')
            await self.page.wait_for_timeout(1000)  # Wait for scroll animation
            videos_section = await self.page.query_selector('#videos')
            self.assertTrue(await videos_section.is_visible())

            await self.page.click('a[href="#articles"]')
            await self.page.wait_for_timeout(1000)  # Wait for scroll animation
            articles_section = await self.page.query_selector('#articles')
            self.assertTrue(await articles_section.is_visible())

            await self.page.click('a[href="#ecosysteme"]')
            await self.page.wait_for_timeout(1000)  # Wait for scroll animation
            ecosysteme_section = await self.page.query_selector('#ecosysteme')
            self.assertTrue(await ecosysteme_section.is_visible())
        self.loop.run_until_complete(run_test())

    def test_language_switcher(self):
        async def test_logic():
            await self.page.goto(f"http://localhost:{PORT}/index.html")

            # Check default (French)
            await self.page.wait_for_selector('[data-i18n-key="main_title"]')
            main_title_fr = await self.page.inner_text('[data-i18n-key="main_title"]')
            self.assertIn("Event Horizon : Dans les coulisses de l'industrie spatiale européenne", main_title_fr)

            nav_videos_fr = await self.page.inner_text('[data-i18n-key="nav.videos"]')
            self.assertEqual("Vidéos", nav_videos_fr)

            # Switch to English
            await self.page.click('[data-lang="en"]')

            # Check English
            await self.page.wait_for_selector('[data-i18n-key="main_title"]')
            main_title_en = await self.page.inner_text('[data-i18n-key="main_title"]')
            self.assertIn("Event Horizon: Behind the scenes of the European space industry", main_title_en)

            nav_videos_en = await self.page.inner_text('[data-i18n-key="nav.videos"]')
            self.assertEqual("Videos", nav_videos_en)

        self.loop.run_until_complete(test_logic())

    def test_particle_animation(self):
        async def test_logic():
            await self.page.goto(f"http://localhost:{PORT}/index.html")

            # Check for the particle container
            particle_container = await self.page.query_selector('#particle-container')
            self.assertIsNotNone(particle_container)

            # Check for particles
            await self.page.wait_for_selector('.particle')
            particles = await self.page.query_selector_all('.particle')
            self.assertGreater(len(particles), 0)

            # Check if particles are visible (opacity > 0)
            await self.page.wait_for_function('document.querySelector(".particle").style.opacity > 0')
            opacity = await self.page.evaluate('document.querySelector(".particle").style.opacity')
            self.assertGreater(float(opacity), 0)

        self.loop.run_until_complete(test_logic())

    def test_anime_is_defined(self):
        """Verifies that the anime.js library is defined on the page.

        This test ensures that the `anime` function is available in the global
        scope, which is crucial for all animations to work.
        """
        async def run_test():
            """Runs the anime.js definition test steps."""
            await self.page.goto(f'http://localhost:{PORT}/index.html')
            anime_defined = await self.page.evaluate('typeof anime')
            self.assertEqual(anime_defined, 'function')

        self.loop.run_until_complete(run_test())
