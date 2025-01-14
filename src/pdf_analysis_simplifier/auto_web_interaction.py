from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import base64
import os

class AutoWebInteraction:
    # Initialize the WebDriver
    def __init__(self):
        try:
            # Set up Chrome options
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")  # Undetectable driver
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

            # Initialize the WebDriver with undetected-chromedriver
            self._driver = uc.Chrome(options=options)
            self._driver.implicitly_wait(10)  # Set implicit wait
            self._driver.maximize_window()  # Maximize the browser window

        except WebDriverException as e:
            print(f"Failed to initialize WebDriver: {e}")
            raise


    # Enter a webpage
    def enter_in_webpage(self, url):
        self._driver.get(url)

    # Send text to the selected element
    def send_content_to_element(self, element, content):
        try:
            element.send_keys(content)
            return True
        except WebDriverException as e:
            print(f"Failed to send text to element: {e}")
            return False

    # Read text from a selected element
    def read_text_from_element(self, element):
        try:
            return element.get_attribute("value") or element.text
        except Exception as e:
            print(f"Failed to read text from element: {e}")
            return None

    # Click on a selected element
    def click_into_element(self, element):
        try:
            element.click()
            return True
        except WebDriverException as e:
            print(f"Failed to click on element: {e}")
            return False

    # Wait for an element to be clickable and click it
    def wait_and_click_element(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self._driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True
        except Exception as e:
            print(f"Failed to wait and click element: {e}")
            return False

    # Click an element at a specific position using JavaScript
    def click_element_with_javascript(self, elements, position):
        try:
            if position < len(elements):
                self._driver.execute_script("arguments[0].click();", elements[position])
                return True
            else:
                print(f"Position {position} is out of range.")
                return False
        except Exception as e:
            print(f"Failed to click element with JavaScript: {e}")
            return False

    # Drag-and-Drop file into a webpage
    def drag_and_drop_file_into_element(self, file_path, by_method, identifier):
        try:

            with open(file_path, "rb") as file:
                file_content = file.read()

            # Read and encode the file content
            file_content = base64.b64encode(file_content).decode("utf-8")
            if file_content is None:
                print("Failed to read file content.")
                return False

            # Get the file name (without the full path)
            file_name = os.path.basename(file_path)

            # Locate the drop area element
            element = self.find_element(by_method, identifier)

            # JavaScript to simulate file drop with actual file content
            js_script = """
        // Decode the base64 content
        const fileContent = atob(arguments[0]);

        // Convert the decoded content to a Uint8Array
        const uint8Array = new Uint8Array(fileContent.length);
        for (let i = 0; i < fileContent.length; i++) {
            uint8Array[i] = fileContent.charCodeAt(i);
        }

        // Create a Blob from the Uint8Array
        const fileBlob = new Blob([uint8Array], { type: 'application/pdf' });

        // Create a File object
        const file = new File([fileBlob], arguments[1], { type: 'application/pdf' });

        // Create a DataTransfer object and add the file
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);

        // Dispatch the drop event
        const dropEvent = new DragEvent('drop', {
            bubbles: true,
            dataTransfer: dataTransfer
        });
        arguments[2].dispatchEvent(dropEvent);
        """

            # Execute the JavaScript
            self._driver.execute_script(js_script, file_content, file_name, element)
            return True
        except Exception as e:
            print(f"Failed to drag and drop file: {e}")
            return False

    # Find an element in the webpage
    def find_element(self, by_method, identifier):
        try:
            element = self._driver.find_element(by_method, identifier)
            print(f"Element found using {by_method} with identifier '{identifier}'.")
            return element
        except Exception as e:
            print(f"Failed to find element using {by_method} with identifier '{identifier}': {e}")
            return None

# Close the browser
    def close(self):
        self._driver.quit()