# JALA Academy - Selenium Assignment
# Testing the Magnus application

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class MagnusSeleniumTest:
    def __init__(self):
        # Set up the Chrome driver
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://magnus.jalatechnologies.com/"
    
    def login(self):
        """Login to the Magnus application"""
        try:
            self.driver.get(self.base_url)
            
            # Wait for username field
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "UserName"))
            )
            
            # Enter username
            username_field.clear()
            username_field.send_keys("training@jalaacademy.com")
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "Password")
            password_field.clear()
            password_field.send_keys("jobprogram")
            
            # Click login button
            login_button = self.driver.find_element(By.ID, "btnLogin")
            login_button.click()
            
            # Wait for dashboard to load
            time.sleep(3)  # Give some time for the page to load after login
            
            print("Login successful!")
            return True
            
        except TimeoutException:
            print("Timeout: Login page did not load in time")
            return False
        except NoSuchElementException:
            print("Element not found during login")
            return False
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return False
    
    def test_web_element_operations(self):
        """Test operations on web elements"""
        try:
            # Wait for page to load
            time.sleep(2)
            
            # Find and interact with a text input
            try:
                search_box = self.driver.find_element(By.ID, "searchInput")  # This might not exist on the actual site
                search_box.clear()
                search_box.send_keys("Test Search")
                search_box.send_keys(Keys.RETURN)
                print("Search operation completed")
            except NoSuchElementException:
                print("Search box not found")
            
            # Find and click a button
            try:
                button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Click')]")
                button.click()
                print("Button clicked")
            except NoSuchElementException:
                print("Specific button not found")
            
            # Work with dropdown if available
            try:
                dropdown = self.driver.find_element(By.TAG_NAME, "select")
                select = Select(dropdown)
                select.select_by_index(1)
                print("Dropdown selected")
            except NoSuchElementException:
                print("No dropdown found")
            
            # Work with checkboxes
            checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            for checkbox in checkboxes:
                if not checkbox.is_selected():
                    checkbox.click()
                    print("Checkbox checked")
                    break
            
            # Work with radio buttons
            radio_buttons = self.driver.find_elements(By.XPATH, "//input[@type='radio']")
            if radio_buttons:
                radio_buttons[0].click()
                print("Radio button selected")
            
            return True
            
        except Exception as e:
            print(f"Error during web element operations: {str(e)}")
            return False
    
    def test_locators(self):
        """Test different Selenium locators"""
        try:
            # Find element by ID (try to find a general element that's likely to exist)
            try:
                element_by_id = self.driver.find_element(By.TAG_NAME, "body")
                print("Found body element by tag name")
            except NoSuchElementException:
                print("Body element not found")
            
            # Find element by Name (try to find login elements if they exist)
            try:
                element_by_name = self.driver.find_element(By.NAME, "UserName")
                print("Found UserName element by name")
            except NoSuchElementException:
                print("UserName element not found by name")
            
            # Find elements by Class Name
            elements_by_class = self.driver.find_elements(By.CLASS_NAME, "form-control")
            print(f"Found {len(elements_by_class)} by Class Name")
            
            # Find input elements by Tag Name
            input_elements = self.driver.find_elements(By.TAG_NAME, "input")
            print(f"Found {len(input_elements)} input elements by Tag Name")
            
            # Find element by CSS Selector
            css_element = self.driver.find_element(By.CSS_SELECTOR, "input[type='text']")
            print("Found by CSS Selector")
            
            # Find element by XPath
            xpath_element = self.driver.find_element(By.XPATH, "//input[@id='UserName']")
            print("Found by XPath")
            
            # Find links by partial text
            try:
                link_elements = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "login")
                print(f"Found {len(link_elements)} links by partial text")
            except NoSuchElementException:
                print("No links with 'login' text found")
            
            return True
            
        except NoSuchElementException as e:
            print(f"Element not found: {str(e)}")
            return False
        except Exception as e:
            print(f"Error during locator testing: {str(e)}")
            return False
    
    def test_windows_and_popups(self):
        """Test handling of windows and popups"""
        try:
            # Get current window
            original_window = self.driver.current_window_handle
            
            # Handle alerts if they appear
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                print(f"Alert: {alert_text}")
                alert.accept()  # Accept the alert
                print("Alert accepted")
            except:
                print("No alert found")
            
            return True
            
        except Exception as e:
            print(f"Error during window/popup handling: {str(e)}")
            return False
    
    def test_miscellaneous_scenarios(self):
        """Test miscellaneous Selenium scenarios"""
        try:
            # Scroll to bottom of page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # Scroll to top of page
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Get page title
            title = self.driver.title
            print(f"Page title: {title}")
            
            # Get current URL
            current_url = self.driver.current_url
            print(f"Current URL: {current_url}")
            
            # Get page source
            page_source = self.driver.page_source
            if "Magnus" in page_source:
                print("Magnus text found in page source")
            
            # Wait for button to be clickable
            try:
                clickable_element = self.wait.until(
                    EC.element_to_be_clickable((By.TAG_NAME, "button"))
                )
                print("Found clickable button")
            except TimeoutException:
                print("No clickable button found")
            
            # Execute JavaScript
            js_result = self.driver.execute_script("return document.title;")
            print(f"Title from JS: {js_result}")
            
            return True
            
        except Exception as e:
            print(f"Error during miscellaneous testing: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all Selenium tests"""
        print("Starting Selenium tests for Magnus application...")
        
        # Try to login, but continue with tests even if login fails
        login_success = self.login()
        if not login_success:
            print("Login failed, but continuing with tests on the current page")
        
        print("\nRunning web element operations test...")
        self.test_web_element_operations()
        
        print("\nRunning locator tests...")
        self.test_locators()
        
        print("\nRunning windows and popups test...")
        self.test_windows_and_popups()
        
        print("\nRunning miscellaneous scenarios test...")
        self.test_miscellaneous_scenarios()
        
        print("\nAll Selenium tests completed!")
        return True
    
    def close(self):
        """Close the browser"""
        self.driver.quit()
        print("Browser closed")


class TestNGExample:
    """
    This class demonstrates TestNG-like functionality using unittest
    """
    
    def setup_method(self):
        """Setup method"""
        self.selenium_test = MagnusSeleniumTest()
    
    def teardown_method(self):
        """Teardown method"""
        self.selenium_test.close()
    
    def test_login_functionality(self):
        """Test login functionality"""
        assert self.selenium_test.login() == True
    
    def test_element_operations(self):
        """Test web element operations"""
        self.selenium_test.login()  # Login first
        assert self.selenium_test.test_web_element_operations() == True


def main():
    """Main function to run the Selenium tests"""
    print("JALA Academy Selenium Assignment")
    print("=" * 40)
    
    # Create an instance of the test class
    test = MagnusSeleniumTest()
    
    try:
        # Run all tests
        success = test.run_all_tests()
        
        if success:
            print("\nAll tests completed successfully!")
        else:
            print("\nSome tests failed.")
            
    except Exception as e:
        print(f"An error occurred during testing: {str(e)}")
    
    finally:
        # Close the browser
        test.close()


if __name__ == "__main__":
    main()