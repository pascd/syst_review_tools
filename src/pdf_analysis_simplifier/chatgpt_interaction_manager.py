from time import sleep
import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import logging
import time

# Dynamically add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.pdf_analysis_simplifier.web_gpt_handler import WebAIChatInteraction

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatGPTInteractionManager:
    def __init__(self):
        self.driver = WebAIChatInteraction()

    # Launch ChatGPT page
    def launch_chatpgt_page(self):
        self.driver.launch_web_page(url="https://www.chatgpt.com/")
        return True

    def login(self):
        # Since automated login is not funtional, it is necessary to call for human interaction to do it
        self.driver.call_for_human()
        return True

    def send_and_receive(self, message):

        # Locate the chat input
        chat_input = self.driver.activate_text_area(
            by_method=By.CSS_SELECTOR,
            text_identifier="div#prompt-textarea"
        )

        if not chat_input:
            logger.error("Could not activate chat input. Exiting.")
            return False

        # Input the message in the chat input
        try:
            chat_input.send_keys(message)
            logger.info(f"Message entered: {message}")
        except Exception as e:
            logger.error(f"Failed to enter message: {e}")
            return False

        # Wait and click the submit button
        try:
            if not self.driver.wait_and_click_element(
                    by=By.CSS_SELECTOR,
                    value="button[data-testid='send-button']",
                    timeout=60
            ):
                logger.warning("Failed to click the submit button. Using ENTER key as fallback.")
                chat_input.send_keys(Keys.ENTER)
        except Exception as e:
            logger.error(f"Error while trying to click submit button: {e}")
            return False

        # Wait for response to finish and retrieve it
        try:
            if self.driver.check_response_ended(By.CSS_SELECTOR, "button[data-testid='stop-button']", 60):
                response = self.driver.read_last_message(By.CSS_SELECTOR, "div[data-message-author-role='assistant'] div.markdown.prose")
                logger.info(f"Response: {response}")
                return response
        except NoSuchElementException:
            logger.error("Failed to read the response. Please check the webpage layout.")
            return False


    # Input a file into the chat
    def input_external_file(self, file_path):
        time.sleep(2)
        self.driver.drag_and_drop_file_into_element(file_path=file_path,
                                                    by_method=By.CSS_SELECTOR,
                                                    identifier="div#prompt-textarea")
        time.sleep(1)