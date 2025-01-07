from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException

class AutoWebInteraction:

    # Initialize the WebDriver
    def __init__(self):
        self.driver = webdriver.Chrome()

    # Enter a webpage
    def enter_in_webpage(self, url):
        self.driver.get(url)

    # Select an element in webpage by name
    def select_element_by_name(self, _element_name):
        return self.driver.find_element(By.NAME, _element_name)

    # Select an element in webpage by id
    def select_element_by_id(self, _element_id):
        return self.driver.find_element(By.ID, _element_id)

    # Select an element in webpage by xpath (by an XML expression)
    def select_element_by_xpath(self, _element_path):
        return self.driver.find_element(By.XPATH, _element_path)

    # Select an element in a webpage that is a link (e.g., links referenced by href)
    def select_element_by_link_text(self, _element_link_text):
        return self.driver.find_element(By.LINK_TEXT, _element_link_text)

    # Select an element in a webpage by its tag name (e.g., <input>)
    def select_element_by_tag_name(self, _element_tag_name):
        return self.driver.find_element(By.TAG_NAME, _element_tag_name)

    # Send text to the selected element
    def send_text_to_element(self, _element, _text):
        try:
            _element.send_keys(_text)
            return True
        except WebDriverException as e:
            print(f"Failed to send text to element: {e}")
            return False

    # Read text from a selected element
    def read_text_from_element(self, _element):
        return _element.get_attribute("value")

    # Click on a selected element
    def click_into_element(self, _element):
        try:
            _element.click()
            return True
        except WebDriverException as e:
            print(f"Failed to click on element: {e}")
            return False

    # Close the browser
    def close(self):
        self.driver.quit()
