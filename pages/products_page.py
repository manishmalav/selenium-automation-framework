from playwright.sync_api import Page, expect


class ProductsPage:
    """
    Page Object for automationexercise.com/products
    Contains all selectors and actions for the products page
    """

    URL = "https://www.automationexercise.com/products"

    # ── Selectors ─────────────────────────────────────────
    SEARCH_INPUT   = "#search_product"
    SEARCH_BUTTON  = "#submit_search"
    PRODUCT_NAMES  = ".productinfo p"
    PAGE_HEADING   = ".title.text-center"

    def __init__(self, page: Page):
        self.page = page

    # ── Actions ───────────────────────────────────────────
    def navigate(self):
        self.page.set_default_timeout(60000)
        self.page.goto(self.URL, wait_until="domcontentloaded")
        self.page.wait_for_selector(self.SEARCH_INPUT)
        return self

    def search(self, keyword: str):
        self.page.fill(self.SEARCH_INPUT, keyword)
        self.page.click(self.SEARCH_BUTTON)
        self.page.wait_for_timeout(2000)
        return self

    # ── Assertions ────────────────────────────────────────
    def get_page_title(self) -> str:
        return self.page.title()

    def get_heading(self) -> str:
        return self.page.locator(self.PAGE_HEADING).text_content().strip()

    def get_product_names(self) -> list:
        items = self.page.locator(self.PRODUCT_NAMES).all()
        return [i.text_content().strip() for i in items if i.text_content().strip()]

    def get_product_count(self) -> int:
        return len(self.get_product_names())