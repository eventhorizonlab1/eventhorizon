
import asyncio
from playwright.async_api import async_playwright
import http.server
import socketserver
import threading
import os

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

def run_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

async def main():
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"http://localhost:{PORT}/index.html")
        await page.screenshot(path="fixed_layout.png")
        await browser.close()

    # The server is a daemon thread, so it will exit when the main thread exits.
    # We need to find a way to stop it gracefully. For now, we'll just exit.
    # This is a temporary script, so this is acceptable.
    os._exit(0)

if __name__ == "__main__":
    asyncio.run(main())
