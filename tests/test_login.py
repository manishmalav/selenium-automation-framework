import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLoginModule:
    """
    Login Module Test Suite
    Maps to: TC-LGN-001, 007, 008, 010, 011
    Site: automationexercise.com
    """

    def test_valid_login_accepted(self, api, config):
        """TC-LGN-001: Valid credentials should return success"""
        response = api.post(
            config["api_url"],
            data={
                "email"   : config["valid_email"],
                "password": config["valid_password"]
            }
        )
        data = response.json()
        assert data["responseCode"] == 200, (
            "Expected 200 but got: " + str(data["responseCode"])
        )
        assert "exists" in data["message"].lower(), (
            "Unexpected message: " + data["message"]
        )

    def test_wrong_password_rejected(self, api, config):
        """TC-LGN-007: Wrong password should be rejected"""
        response = api.post(
            config["api_url"],
            data={
                "email"   : config["valid_email"],
                "password": config["wrong_password"]
            }
        )
        data = response.json()
        assert data["responseCode"] == 404, (
            "Expected 404 but got: " + str(data["responseCode"])
        )

    def test_unregistered_email_rejected(self, api, config):
        """TC-LGN-008: Unregistered email should be rejected"""
        response = api.post(
            config["api_url"],
            data={
                "email"   : config["fake_email"],
                "password": config["valid_password"]
            }
        )
        data = response.json()
        assert data["responseCode"] == 404, (
            "Expected 404 but got: " + str(data["responseCode"])
        )

    def test_empty_email_blocked(self, driver, config):
        """TC-LGN-010: Empty email should block form submission"""
        driver.get(config["base_url"] + "/login")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[data-qa='login-email']")
            )
        )
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")

        # Remove any ad iframes covering the page
        try:
            driver.execute_script(
                "document.querySelectorAll('iframe').forEach(el => el.remove());"
            )
            time.sleep(1)
        except:
            pass

        driver.find_element(
            By.CSS_SELECTOR, "input[data-qa='login-password']"
        ).send_keys(config["valid_password"])

        # Use JavaScript click to bypass any remaining overlay
        btn = driver.find_element(
            By.CSS_SELECTOR, "button[data-qa='login-button']"
        )
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(2)

        assert "login" in driver.current_url, (
            "Form submitted without email — should have been blocked"
        )

    def test_empty_password_blocked(self, driver, config):
        """TC-LGN-011: Empty password should block form submission"""
        driver.get(config["base_url"] + "/login")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[data-qa='login-email']")
            )
        )
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")

        # Remove any ad iframes covering the page
        try:
            driver.execute_script(
                "document.querySelectorAll('iframe').forEach(el => el.remove());"
            )
            time.sleep(1)
        except:
            pass

        driver.find_element(
            By.CSS_SELECTOR, "input[data-qa='login-email']"
        ).send_keys(config["valid_email"])

        # Use JavaScript click to bypass any remaining overlay
        btn = driver.find_element(
            By.CSS_SELECTOR, "button[data-qa='login-button']"
        )
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(2)

        assert "login" in driver.current_url, (
            "Form submitted without password — should have been blocked"
        )