import pytest
from playwright.sync_api import sync_playwright
from pages.products_page import ProductsPage


class TestSearchPOM:
    """
    Search tests using Page Object Model
    """

    def test_products_page_loads(self):
        """Verify products page loads correctly"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            products = ProductsPage(page)

            products.navigate()

            assert "All Products" in products.get_page_title(), (
                "Wrong page title: " + products.get_page_title()
            )
            print("\nPASS: Products page loaded:", products.get_page_title())

            browser.close()

    def test_search_returns_results(self):
        """Verify search returns results"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            products = ProductsPage(page)

            products.navigate()
            products.search("dress")

            count = products.get_product_count()
            assert count > 0, "Search returned no results"
            print("\nPASS:", count, "products found")
            print("First 3:", products.get_product_names()[:3])

            browser.close()

    def test_search_heading_shown(self):
        """Verify searched products heading appears"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            products = ProductsPage(page)

            products.navigate()
            products.search("top")

            heading = products.get_heading()
            assert "searched products" in heading.lower(), (
                "Wrong heading: " + heading
            )
            print("\nPASS: Heading correct:", heading)

            browser.close()

    def test_empty_search_shows_all(self):
        """Verify empty search shows all products"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            products = ProductsPage(page)

            products.navigate()
            products.search("")

            count = products.get_product_count()
            assert count > 10, "Expected many products, got: " + str(count)
            print("\nPASS:", count, "products shown for empty search")

            browser.close()