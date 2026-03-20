# Selenium Automation Framework

A professional test automation framework built with Selenium, pytest, and Python.
Covers UI and API testing using a hybrid approach.

## Project Structure

```
indeed-automation/
├── conftest.py          # Shared fixtures (browser setup, config)
├── pytest.ini           # pytest configuration
├── tests/
│   ├── test_login.py    # Login module — 5 test cases
│   └── test_search.py   # Search module — 5 test cases
└── reports/             # HTML test reports (auto-generated)
```

## Tech Stack

- Python 3.13
- Selenium 4.x — UI browser automation
- pytest — test framework and runner
- pytest-html — HTML report generation
- requests — API testing

## Test Coverage

### Login Module (5 tests)

| Test Case                   | Type     | Method   |
| --------------------------- | -------- | -------- |
| Valid login accepted        | Positive | API      |
| Wrong password rejected     | Negative | API      |
| Unregistered email rejected | Negative | API      |
| Empty email blocked         | Negative | Selenium |
| Empty password blocked      | Negative | Selenium |

### Search Module (5 tests)

| Test Case              | Type      | Method   |
| ---------------------- | --------- | -------- |
| Products page loads    | Positive  | Selenium |
| Search box visible     | Positive  | Selenium |
| Search returns results | Positive  | Selenium |
| Search heading correct | Positive  | Selenium |
| Empty search shows all | Edge Case | Selenium |

## How to Run

### Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install selenium pytest pytest-html requests webdriver-manager
playwright install
```

### Run all tests

```bash
pytest
```

### Run with HTML report

```bash
pytest --html=reports/report.html
```

### Run specific module

```bash
pytest tests/test_login.py
pytest tests/test_search.py
```

## Test Results

- Total: 10 tests
- Passed: 10
- Failed: 0
- Pass Rate: 100%
- Execution time: ~92 seconds

## Key Technical Decisions

**Hybrid API + UI approach:** Login credential tests use direct API calls
to bypass bot detection, while UI validation tests use Selenium.
This mirrors real-world QA practice where staging APIs are tested
separately from browser interactions.

**Fixtures in conftest.py:** Browser setup and teardown is handled
by pytest fixtures — no repetition across test files.

**Ad overlay handling:** JavaScript iframe removal handles ad overlays
that intercept button clicks on free test sites.
