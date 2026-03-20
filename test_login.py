from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

BASE_URL       = "https://www.automationexercise.com"
VALID_EMAIL    = "testuser_manish@gmail.com"
VALID_PASSWORD = "Test@1234"
WRONG_PASSWORD = "WrongPass999"
FAKE_EMAIL     = "notexist@random.com"

# ═══════════════════════════════════════════════
# BROWSER SETUP
# ═══════════════════════════════════════════════
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.maximize_window()
    return driver

def print_result(tc_id, title, status, note=""):
    symbol = "PASS" if status else "FAIL"
    print("  [" + symbol + "] " + tc_id + ": " + title)
    if note:
        print("         Note: " + note)
    return 1 if status else 0

# ═══════════════════════════════════════════════
# TC-LGN-001: Valid login via API
# ═══════════════════════════════════════════════
def test_valid_login():
    try:
        response = requests.post(
            BASE_URL + "/api/verifyLogin",
            data={
                "email": VALID_EMAIL,
                "password": VALID_PASSWORD
            }
        )
        data = response.json()
        if data.get("responseCode") == 200:
            return print_result(
                "TC-LGN-001", "Valid login accepted",
                True, "API response: " + data.get("message", "")
            )
        else:
            return print_result(
                "TC-LGN-001", "Valid login accepted",
                False, "Code: " + str(data.get("responseCode")) + " | " + data.get("message", "")
            )
    except Exception as e:
        print("  [ERROR] TC-LGN-001: " + str(e))
    return 0

# ═══════════════════════════════════════════════
# TC-LGN-007: Wrong password via API
# ═══════════════════════════════════════════════
def test_wrong_password():
    try:
        response = requests.post(
            BASE_URL + "/api/verifyLogin",
            data={
                "email": VALID_EMAIL,
                "password": WRONG_PASSWORD
            }
        )
        data = response.json()
        if data.get("responseCode") == 404:
            return print_result(
                "TC-LGN-007", "Wrong password rejected",
                True, "API response: " + data.get("message", "")
            )
        else:
            return print_result(
                "TC-LGN-007", "Wrong password rejected",
                False, "Unexpected code: " + str(data.get("responseCode"))
            )
    except Exception as e:
        print("  [ERROR] TC-LGN-007: " + str(e))
    return 0

# ═══════════════════════════════════════════════
# TC-LGN-008: Unregistered email via API
# ═══════════════════════════════════════════════
def test_unregistered_email():
    try:
        response = requests.post(
            BASE_URL + "/api/verifyLogin",
            data={
                "email": FAKE_EMAIL,
                "password": VALID_PASSWORD
            }
        )
        data = response.json()
        if data.get("responseCode") == 404:
            return print_result(
                "TC-LGN-008", "Unregistered email rejected",
                True, "API response: " + data.get("message", "")
            )
        else:
            return print_result(
                "TC-LGN-008", "Unregistered email rejected",
                False, "Unexpected code: " + str(data.get("responseCode"))
            )
    except Exception as e:
        print("  [ERROR] TC-LGN-008: " + str(e))
    return 0

# ═══════════════════════════════════════════════
# TC-LGN-010: Empty email — UI test
# ═══════════════════════════════════════════════
def test_empty_email():
    driver = get_driver()
    passed = 0
    try:
        driver.get(BASE_URL + "/login")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[data-qa='login-email']")
            )
        )
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        driver.find_element(
            By.CSS_SELECTOR, "input[data-qa='login-password']"
        ).send_keys(VALID_PASSWORD)
        driver.find_element(
            By.CSS_SELECTOR, "button[data-qa='login-button']"
        ).click()
        time.sleep(2)
        still_on_login = "login" in driver.current_url
        if still_on_login:
            passed = print_result(
                "TC-LGN-010", "Empty email blocked",
                True, "Browser validation prevented submission"
            )
        else:
            passed = print_result(
                "TC-LGN-010", "Empty email blocked",
                False, "Form submitted without email"
            )
    except Exception as e:
        print("  [ERROR] TC-LGN-010: " + str(e))
    finally:
        driver.quit()
    return passed

# ═══════════════════════════════════════════════
# TC-LGN-011: Empty password — UI test
# ═══════════════════════════════════════════════
def test_empty_password():
    driver = get_driver()
    passed = 0
    try:
        driver.get(BASE_URL + "/login")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[data-qa='login-email']")
            )
        )
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        driver.find_element(
            By.CSS_SELECTOR, "input[data-qa='login-email']"
        ).send_keys(VALID_EMAIL)
        driver.find_element(
            By.CSS_SELECTOR, "button[data-qa='login-button']"
        ).click()
        time.sleep(2)
        still_on_login = "login" in driver.current_url
        if still_on_login:
            passed = print_result(
                "TC-LGN-011", "Empty password blocked",
                True, "Browser validation prevented submission"
            )
        else:
            passed = print_result(
                "TC-LGN-011", "Empty password blocked",
                False, "Form submitted without password"
            )
    except Exception as e:
        print("  [ERROR] TC-LGN-011: " + str(e))
    finally:
        driver.quit()
    return passed


# ═══════════════════════════════════════════════
# MAIN RUNNER
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    print("")
    print("=" * 55)
    print("  LOGIN MODULE - Automated Test Suite")
    print("  Site: automationexercise.com")
    print("  Method: API + Selenium hybrid")
    print("=" * 55)
    print("")
    print("--- Running 5 Login Test Cases ---")
    print("")

    results = []
    results.append(test_valid_login())
    results.append(test_wrong_password())
    results.append(test_empty_email())
    results.append(test_empty_password())
    results.append(test_unregistered_email())

    passed = sum(results)
    failed = len(results) - passed
    total  = len(results)
    rate   = round((passed / total) * 100)

    print("")
    print("=" * 55)
    print("  TEST EXECUTION SUMMARY")
    print("=" * 55)
    print("  Total Tests  : " + str(total))
    print("  Passed       : " + str(passed))
    print("  Failed       : " + str(failed))
    print("  Pass Rate    : " + str(rate) + "%")
    print("=" * 55)
    print("")