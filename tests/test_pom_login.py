import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage

VALID_EMAIL    = "testuser_manish@gmail.com"
VALID_PASSWORD = "Test@1234"
WRONG_PASSWORD = "WrongPass999"
FAKE_EMAIL     = "notexist@random.com"


class TestLoginPOM:
    """
    Login tests using Page Object Model
    Notice how clean and readable these tests are
    """

    def test_login_page_has_both_forms(self):
        """Verify login page loads with login and signup forms"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            login = LoginPage(page)

            login.navigate()

            assert login.has_login_form(), "Login form not found"
            assert login.has_signup_form(), "Signup form not found"
            print("\nPASS: Both forms visible on login page")

            browser.close()

    def test_valid_login_redirects(self):
        """TC-LGN-001: Valid login should redirect away from login page"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            login = LoginPage(page)

            login.navigate()
            login.login(VALID_EMAIL, VALID_PASSWORD)

            assert not login.is_on_login_page(), (
                "Should have left login page after valid login"
            )
            print("\nPASS: Redirected to:", page.url)

            browser.close()

    def test_wrong_password_shows_error(self):
        """TC-LGN-007: Wrong password should show error message"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            login = LoginPage(page)

            login.navigate()
            login.login(VALID_EMAIL, WRONG_PASSWORD)

            error = login.get_error_message()
            assert error != "", "No error message shown for wrong password"
            assert login.is_on_login_page(), "Should stay on login page"
            print("\nPASS: Error shown:", error)

            browser.close()

    def test_unregistered_email_shows_error(self):
        """TC-LGN-008: Unregistered email should show error"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            login = LoginPage(page)

            login.navigate()
            login.login(FAKE_EMAIL, VALID_PASSWORD)

            error = login.get_error_message()
            assert error != "", "No error message for unregistered email"
            print("\nPASS: Error shown:", error)

            browser.close()

    def test_empty_email_stays_on_login(self):
        """TC-LGN-010: Empty email should block submission"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            login = LoginPage(page)

            login.navigate()
            login.remove_ads()
            login.enter_password(VALID_PASSWORD)
            login.click_login()

            assert login.is_on_login_page(), (
                "Form should not submit with empty email"
            )
            print("\nPASS: Stayed on login page with empty email")

            browser.close()