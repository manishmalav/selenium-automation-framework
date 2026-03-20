import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL    = "https://www.automationexercise.com"
VALID_EMAIL    = "testuser_manish@gmail.com"
VALID_PASSWORD = "Test@1234"
WRONG_PASSWORD = "WrongPass999"
FAKE_EMAIL     = "notexist@random.com"
API_URL        = BASE_URL + "/api/verifyLogin"

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    d = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    d.maximize_window()
    yield d
    d.quit()

@pytest.fixture
def api():
    return requests.Session()

@pytest.fixture
def config():
    return {
        "base_url"      : BASE_URL,
        "valid_email"   : VALID_EMAIL,
        "valid_password": VALID_PASSWORD,
        "wrong_password": WRONG_PASSWORD,
        "fake_email"    : FAKE_EMAIL,
        "api_url"       : API_URL,
    }