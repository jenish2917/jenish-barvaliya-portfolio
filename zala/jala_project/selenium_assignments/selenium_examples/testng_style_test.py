"""
JALA Academy - TestNG Style Selenium Test
Demonstrating TestNG concepts using Python's unittest framework
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class TestMagnusApplication(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Class setup method - equivalent to @BeforeClass in TestNG"""
        print("Setting up class - initializing driver")
        cls.driver = webdriver.Chrome()
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.base_url = "http://magnus.jalatechnologies.com/"
    
    @classmethod
    def tearDownClass(cls):
        """Class teardown method - equivalent to @AfterClass in TestNG"""
        print("Tearing down class - closing driver")
        cls.driver.quit()
    
    def setUp(self):
        """Method setup - equivalent to @BeforeMethod in TestNG"""
        print(f"Setting up test: {self._testMethodName}")
        self.driver.get(self.base_url)
        time.sleep(1)
    
    def tearDown(self):
        """Method teardown - equivalent to @AfterMethod in TestNG"""
        print(f"Tearing down test: {self._testMethodName}")
        # Optionally clear the page or reset state here
    
    def login_to_application(self):
        """Helper method to login to the application"""
        try:
            # Wait for the username field to be present
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "UserName"))
            )
            
            # Fill in the username
            username_field.clear()
            username_field.send_keys("training@jalaacademy.com")
            
            # Fill in the password
            password_field = self.driver.find_element(By.ID, "Password")
            password_field.clear()
            password_field.send_keys("jobprogram")
            
            # Click the login button
            login_button = self.driver.find_element(By.ID, "btnLogin")
            login_button.click()
            
            # Wait for the dashboard to load
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
            )
            
            return True
            
        except TimeoutException:
            print("Timeout: Login page did not load in time")
            return False
    
    def test_login_functionality(self):
        """Test login functionality"""
        print("Testing login functionality")
        
        # Perform login
        success = self.login_to_application()
        self.assertTrue(success, "Login should be successful")
        
        # Verify we're on the dashboard
        page_title = self.driver.title
        self.assertIn("Dashboard", page_title, "Page title should contain 'Dashboard'")
        
        print("Login functionality test passed")
    
    def test_element_interactions(self):
        """Test interactions with web elements"""
        print("Testing element interactions")
        
        # First login
        success = self.login_to_application()
        self.assertTrue(success, "Login should be successful")
        
        # Wait a bit for the page to load
        time.sleep(2)
        
        # Test finding and interacting with elements
        try:
            # Find a text input field (example - actual elements depend on the page)
            input_fields = self.driver.find_elements(By.TAG_NAME, "input")
            self.assertGreater(len(input_fields), 0, "There should be at least one input field")
            
            # Find a button (example)
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            self.assertGreater(len(buttons), 0, "There should be at least one button")
            
            print(f"Found {len(input_fields)} input fields and {len(buttons)} buttons")
            
        except Exception as e:
            self.fail(f"Error during element interaction test: {str(e)}")
        
        print("Element interactions test passed")
    
    def test_page_navigation(self):
        """Test page navigation"""
        print("Testing page navigation")
        
        # Get initial URL
        initial_url = self.driver.current_url
        print(f"Initial URL: {initial_url}")
        
        # Get page title
        title = self.driver.title
        self.assertIsNotNone(title, "Page should have a title")
        print(f"Page title: {title}")
        
        # Test that the page loaded correctly
        page_source = self.driver.page_source
        self.assertIn("Magnus", page_source, "Page source should contain 'Magnus'")
        
        print("Page navigation test passed")
    
    def test_element_locators(self):
        """Test different element locators"""
        print("Testing element locators")
        
        # Test various locators
        locators_to_test = [
            (By.ID, "UserName", "Username field"),
            (By.NAME, "UserName", "Username field by name"),
            (By.CLASS_NAME, "form-control", "Form control elements"),
            (By.TAG_NAME, "input", "Input elements"),
            (By.CSS_SELECTOR, "input[type='text']", "Text input fields"),
        ]
        
        for locator_type, locator_value, description in locators_to_test:
            try:
                if locator_type == By.CLASS_NAME or locator_type == By.TAG_NAME:
                    elements = self.driver.find_elements(locator_type, locator_value)
                    self.assertGreater(len(elements), 0, f"Should find elements for {description}")
                    print(f"Found {len(elements)} elements for {description}")
                else:
                    element = self.driver.find_element(locator_type, locator_value)
                    self.assertIsNotNone(element, f"Should find element for {description}")
                    print(f"Found element for {description}")
            except Exception as e:
                print(f"Could not find {description}: {str(e)}")
        
        print("Element locators test completed")


def suite():
    """Create a test suite - equivalent to TestNG suite"""
    test_suite = unittest.TestSuite()
    
    # Add tests to the suite
    test_suite.addTest(TestMagnusApplication('test_login_functionality'))
    test_suite.addTest(TestMagnusApplication('test_element_interactions'))
    test_suite.addTest(TestMagnusApplication('test_page_navigation'))
    test_suite.addTest(TestMagnusApplication('test_element_locators'))
    
    return test_suite


def run_tests():
    """Run the tests"""
    print("JALA Academy - TestNG Style Selenium Tests")
    print("=" * 50)
    
    # Option 1: Run all tests in the class
    runner = unittest.TextTestRunner(verbosity=2)
    suite_instance = suite()
    result = runner.run(suite_instance)
    
    # Print summary
    print(f"\nTests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")


if __name__ == "__main__":
    run_tests()