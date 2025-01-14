import time
import logging
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.pdf_analysis_simplifier.auto_web_interaction import AutoWebInteraction
from selenium.webdriver.common.action_chains import ActionChains

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebAIChatInteraction(AutoWebInteraction):
    def __init__(self, platform="DEEPSEEK"):
        super().__init__()

    def launch_web_page(self, url):
        self.enter_in_webpage(url)
        logger.info(f"{url} webpage initiated.")

    def send_message(self, message, chat_input, submit_method, submit_identifier):
        try:

            self.send_content_to_element(chat_input, message)
            logger.info(f"Message sent: {message}")

            if self.wait_and_click_element(chat_input, submit_method, submit_identifier):
                logger.info(f"Submit button clicked: {message}")
            else:
                # Alternatively, use ENTER key if no button is found
                chat_input.send_keys(Keys.ENTER)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")

    # Find the "stop" button to check if response has ended
    def read_last_message(self, by_method, identifier):
        try:
            # Get all responses
            all_responses = self.find_elements(by_method, identifier)

            if all_responses:
                last_message = all_responses[-1].text
                return last_message

        except Exception as e:
            logger.error(f"Failed to read last message: {e}")
        return None

    def check_response_ended(self, by_method, identifier, timeout):
        start_time = time.time()
        try:
            while time.time() - start_time < timeout:
                if not self.find_elements(by_method, identifier):
                    return True
                sleep(0.1)
            return False
        except Exception as e:
            logger.error(f"Error waiting for element: {e}")
            return False

    def init_new_chat(self, by_method, identifier):
        try:
            new_chat_button = self.find_element(by_method, identifier)
            if new_chat_button:
                self.click_into_element(new_chat_button)
                logger.info("New chat initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize new chat: {e}")

    # Call for human interaction, whenever its needed
    def call_for_human(self):
        while input("Human interaction needed. Press [y] to continue.").upper() != "Y":
            print("Invalid input. Press [y/n]")
        return True

    # Activate and interact with the contenteditable div
    def activate_text_area(self, by_method, text_identifier):
        try:
            # Find the editable div
            print(f"Finding div with {by_method} = {text_identifier}")
            editable_div = self._driver.find_element(by_method, text_identifier)

            # Click the div to focus
            print("Div found, clicking...")
            ActionChains(self._driver).move_to_element(editable_div).click().perform()

            return editable_div

        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

