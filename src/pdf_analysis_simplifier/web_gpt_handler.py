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

    def find_element(self, by_method, identifier):
        try:
            element = self._driver.find_element(by_method, identifier)
            logger.info(f"Element found using {by_method} with identifier '{identifier}'.")
            return element
        except Exception as e:
            logger.error(f"Failed to find element using {by_method} with identifier '{identifier}': {e}")
            return None

    def find_elements(self, by_method, identifier):
        try:
            elements = self._driver.find_elements(by_method, identifier)
            logger.info(f"Elements found using {by_method} with identifier '{identifier}'.")
            return elements
        except Exception as e:
            logger.error(f"Failed to find elements using {by_method} with identifier '{identifier}': {e}")
            return []

    def send_message(self, message, chat_input, submit_method, submit_identifier):
        try:

            self.send_content_to_element(chat_input, message)
            logger.info(f"Message sent: {message}")

            # Find and click the submit button
            submit_button = WebDriverWait(self._driver, 5).until(
                EC.element_to_be_clickable((submit_method, submit_identifier))
            )

            if submit_button:
                # Click the button
                print("Send button found, clicking...")
                self.click_into_element(submit_button)
            else:
                # Alternatively, use ENTER key if no button is found
                chat_input.send_keys(Keys.ENTER)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")

    def read_last_message(self, by_method, identifier):
        try:
            # Get all responses
            all_responses = self._driver.find_elements(by_method, identifier)

            if all_responses:
                #last_message = all_responses[-1].text
                for response in all_responses:
                    logger.info(f"Last message: {response.text}")
                return last_message

        except Exception as e:
            logger.error(f"Failed to read last message: {e}")
        return None

    def check_response_ended(self, by_method, identifier, timeout=60):
        start_time = time.time()
        while True:
            try:
                response_elements = self.find_elements(by_method, identifier)
                if response_elements:
                    logger.info("Response has ended.")
                    break
            except Exception as e:
                logger.error(f"Error checking response: {e}")
            if time.time() - start_time > timeout:
                logger.warning("Timeout reached. Exiting response check.")
                break
            time.sleep(0.5)
        time.sleep(1)

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

