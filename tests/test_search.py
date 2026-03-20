import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSearchModule:
    """
    Search Module Test Suite
    Site: automationexercise.com
    """

    def test_products_page_loads(self, driver, config):
        """Verify products page loads with correct title"""
        driver.get(config["base_url"] + "/products")
        time.sleep(2)
        assert "All Products" in driver.title, (
            "Expected 'All Products' in title but got: " + driver.title
        )

    def test_search_box_visible(self, driver, config):
        """Verify search box is visible on products page"""
        driver.get(config["base_url"] + "/products")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search_product"))
        )
        search_box = driver.find_element(By.ID, "search_product")
        assert search_box.is_displayed(), "Search box is not visible"

    def test_search_returns_results(self, driver, config):
        """Verify search returns relevant results"""
        driver.get(config["base_url"] + "/products")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search_product"))
        )
        driver.find_element(By.ID, "search_product").send_keys("dress")
        driver.find_element(By.ID, "submit_search").click()
        time.sleep(3)
        results = driver.find_elements(By.CSS_SELECTOR, ".productinfo p")
        assert len(results) > 0, "Search returned no results for 'dress'"

    def test_search_heading_correct(self, driver, config):
        """Verify search results page shows correct heading"""
        driver.get(config["base_url"] + "/products")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search_product"))
        )
        driver.find_element(By.ID, "search_product").send_keys("top")
        driver.find_element(By.ID, "submit_search").click()
        time.sleep(3)
        heading = driver.find_element(By.CSS_SELECTOR, ".title.text-center")
        assert "SEARCHED PRODUCTS" in heading.text.upper(), (
            "Wrong heading: " + heading.text
        )

    def test_empty_search_shows_all(self, driver, config):
        """Verify empty search shows all products"""
        driver.get(config["base_url"] + "/products")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search_product"))
        )
        driver.find_element(By.ID, "submit_search").click()
        time.sleep(3)
        results = driver.find_elements(By.CSS_SELECTOR, ".productinfo p")
        assert len(results) > 10, (
            "Expected many products but got: " + str(len(results))
        )