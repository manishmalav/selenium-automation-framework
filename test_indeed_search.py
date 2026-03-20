from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

print("=" * 55)
print("  Automation Exercise — Search Test (Fixed)")
print("=" * 55)

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

print("\nStep 1: Opening Chrome browser...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
driver.maximize_window()
wait = WebDriverWait(driver, 15)

passed = 0
failed = 0

try:
    # ── TC-001: Page loads correctly ──────────────────────────
    print("\n--- TC-001: Verify products page loads ---")
    driver.get("https://www.automationexercise.com/products")
    time.sleep(3)

    if "All Products" in driver.title:
        print("PASS: Page title is correct:", driver.title)
        passed += 1
    else:
        print("FAIL: Unexpected page title:", driver.title)
        failed += 1

    # ── TC-002: Search box is visible ─────────────────────────
    print("\n--- TC-002: Verify search box is visible ---")
    search_box = wait.until(
        EC.presence_of_element_located((By.ID, "search_product"))
    )
    if search_box.is_displayed():
        print("PASS: Search box is visible")
        passed += 1
    else:
        print("FAIL: Search box not visible")
        failed += 1

    # ── TC-003: Search returns results ────────────────────────
    print("\n--- TC-003: Verify search returns results ---")
    search_box.clear()
    search_box.send_keys("dress")
    time.sleep(1)

    search_btn = driver.find_element(By.ID, "submit_search")
    search_btn.click()
    time.sleep(3)

    results = driver.find_elements(
        By.CSS_SELECTOR, ".productinfo p"
    )

    if results:
        print("PASS:", len(results), "products found!")
        print("First 3 product names:")
        for i, item in enumerate(results[:3]):
            name = item.text.strip()
            if name:
                print("  ", i+1, ".", name)
        passed += 1
    else:
        print("FAIL: No search results found")
        failed += 1

    # ── TC-004: Search heading is correct ─────────────────────
    print("\n--- TC-004: Verify search results heading ---")
    heading = driver.find_element(
        By.CSS_SELECTOR, ".title.text-center"
    )
    heading_text = heading.text.strip().upper()

    if "SEARCHED PRODUCTS" in heading_text:
        print("PASS: Correct heading displayed:", heading.text.strip())
        passed += 1
    else:
        print("FAIL: Wrong heading:", heading.text.strip())
        failed += 1

    # ── TC-005: Empty search behaviour ────────────────────────
    print("\n--- TC-005: Verify empty search behaviour ---")
    driver.get("https://www.automationexercise.com/products")
    time.sleep(2)

    empty_box = wait.until(
        EC.presence_of_element_located((By.ID, "search_product"))
    )
    empty_box.clear()
    driver.find_element(By.ID, "submit_search").click()
    time.sleep(2)

    all_products = driver.find_elements(
        By.CSS_SELECTOR, ".productinfo p"
    )

    if len(all_products) > 0:
        print("PASS: Empty search shows all products:", len(all_products), "found")
        passed += 1
    else:
        print("FAIL: Empty search shows no products")
        failed += 1

except Exception as e:
    print("\nERROR:", e)

finally:
    # ── Summary ───────────────────────────────────────────────
    total = passed + failed
    print("\n" + "=" * 55)
    print("  TEST EXECUTION SUMMARY")
    print("=" * 55)
    print("  Total Tests :", total)
    print("  Passed      :", passed)
    print("  Failed      :", failed)
    if total > 0:
        rate = round((passed / total) * 100)
        print("  Pass Rate   :", str(rate) + "%")
    print("=" * 55)

    time.sleep(2)
    driver.quit()
    print("\nBrowser closed. Done!")