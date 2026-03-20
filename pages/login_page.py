from playwright.sync_api import Page, expect


class LoginPage:
    """
    Page Object for automationexercise.com/login
    Contains all selectors and actions for the login page
    """

    URL = "https://www.automationexercise.com/login"

    # ── Selectors ────────────────────────────────────────
    EMAIL_INPUT    = "input[data-qa='login-email']"
    PASSWORD_INPUT = "input[data-qa='login-password']"
    LOGIN_BUTTON   = "button[data-qa='login-button']"
    ERROR_MESSAGE  = 'p[style*="color: red"]'
    SIGNUP_NAME    = "input[data-qa='signup-name']"
    SIGNUP_EMAIL   = "input[data-qa='signup-email']"

    def __init__(self, page: Page):
        self.page = page

    # ── Actions ───────────────────────────────────────────
    def navigate(self):
        self.page.set_default_timeout(60000)
        self.page.goto(self.URL, wait_until="domcontentloaded")
        return self

    def remove_ads(self):
        self.page.evaluate(
            "document.querySelectorAll('iframe').forEach(el => el.remove())"
        )
        return self

    def enter_email(self, email: str):
        self.page.fill(self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password: str):
        self.page.fill(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.page.locator(self.LOGIN_BUTTON).click()
        self.page.wait_for_timeout(2000)
        return self

    def login(self, email: str, password: str):
        """Full login flow in one method"""
        self.remove_ads()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return self

    # ── Assertions ────────────────────────────────────────
    def is_on_login_page(self) -> bool:
        return "/login" in self.page.url

    def get_error_message(self) -> str:
        try:
            error = self.page.locator(self.ERROR_MESSAGE)
            expect(error).to_be_visible(timeout=5000)
            return error.text_content().strip()
        except:
            return ""

    def has_login_form(self) -> bool:
        return self.page.locator(self.EMAIL_INPUT).is_visible()

    def has_signup_form(self) -> bool:
        return self.page.locator(self.SIGNUP_NAME).is_visible()