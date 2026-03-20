import pytest
from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://www.automationexercise.com"


class TestPlaywrightSearch:

    def test_login_page_loads(self):
        """Verify login page loads with both forms"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.set_default_timeout(60000)
            page.goto(BASE_URL + "/login", wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            expect(
                page.locator("input[data-qa='login-email']")
            ).to_be_visible(timeout=15000)
            expect(
                page.locator("input[data-qa='signup-name']")
            ).to_be_visible(timeout=15000)
            print("\nPASS: Login page has both Login and Signup forms")
            browser.close()

    def test_search_returns_results(self):
        """Verify search returns results for keyword"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.set_default_timeout(60000)
            page.goto(BASE_URL + "/products", wait_until="domcontentloaded")
            page.fill("#search_product", "dress")
            page.click("#submit_search")
            page.wait_for_timeout(2000)
            expect(
                page.locator(".title.text-center")
            ).to_be_visible()
            results = page.locator(".productinfo p").all()
            assert len(results) > 0, "No search results found"
            print("\nPASS:", len(results), "results found")
            browser.close()

    def test_search_heading_correct(self):
        """Verify searched products heading appears"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.set_default_timeout(60000)
            page.goto(BASE_URL + "/products", wait_until="domcontentloaded")
            page.fill("#search_product", "top")
            page.click("#submit_search")
            page.wait_for_timeout(2000)
            heading = page.locator(".title.text-center")
            assert "searched products" in heading.text_content().lower(), (
                "Wrong heading: " + heading.text_content()
            )
            print("\nPASS: Heading correct:", heading.text_content())
            browser.close()

    def test_invalid_login_shows_error(self):
        """Verify wrong credentials show error message"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.set_default_timeout(60000)
            page.goto(BASE_URL + "/login", wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            page.evaluate(
                "document.querySelectorAll('iframe').forEach(el => el.remove())"
            )
            page.wait_for_timeout(1000)
            page.fill("input[data-qa='login-email']", "wrong@test.com")
            page.fill("input[data-qa='login-password']", "wrongpass")
            btn = page.locator("button[data-qa='login-button']")
            btn.evaluate("el => el.click()")
            page.wait_for_timeout(4000)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(1000)
            error = page.locator('p[style*="color: red"]')
            expect(error).to_be_visible(timeout=8000)
            print("\nPASS: Error message shown:", error.text_content())
            browser.close()