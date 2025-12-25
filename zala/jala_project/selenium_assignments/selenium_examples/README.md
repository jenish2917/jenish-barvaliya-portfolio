# JALA Academy Selenium Assignment

This project contains Selenium test examples for the Magnus application as part of the JALA Academy assignments.

## Features

### Selenium WebDriver Examples
- Web element operations (click, type, select, etc.)
- Different locator strategies (ID, Name, Class, XPath, CSS Selector)
- Handling windows and popups
- Miscellaneous Selenium scenarios
- Page navigation and interactions

### TestNG Framework Simulation
- TestNG-style annotations using Python's unittest
- @BeforeClass/@AfterClass equivalent (setUpClass/tearDownClass)
- @BeforeMethod/@AfterMethod equivalent (setUp/tearDown)
- Test suite creation
- Assertion methods

## Files

- `magnus_test.py` - Main Selenium test for Magnus application
- `testng_style_test.py` - TestNG-style tests using Python unittest
- `README.md` - This file

## Requirements

To run these tests, you need:

1. Python 3.x
2. Selenium: `pip install selenium`
3. ChromeDriver for Chrome browser automation
4. WebDriver Manager (optional, for automatic driver management): `pip install webdriver-manager`

## How to Run

1. Install required packages:
   ```
   pip install selenium
   ```

2. Download ChromeDriver from https://chromedriver.chromium.org/ or use webdriver-manager:
   ```
   pip install webdriver-manager
   ```

3. Run the tests:
   ```
   python magnus_test.py
   ```
   or
   ```
   python testng_style_test.py
   ```

## Assignment Coverage

This implementation covers:
- Selenium locators
- Operations on web elements
- WebDriver methods
- Handling popups and windows
- Selenium miscellaneous scenarios
- TestNG framework concepts
- Page Object Model (POM) concepts

## Test Credentials

- Username: `training@jalaacademy.com`
- Password: `jobprogram`
- Application URL: `http://magnus.jalatechnologies.com/`

## Notes

- The tests are designed to work with the Magnus application
- Make sure the Chrome browser is installed on your system
- Internet connection is required to access the web application
- Some elements may change if the application UI is updated