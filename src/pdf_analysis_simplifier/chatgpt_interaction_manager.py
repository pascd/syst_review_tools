from time import sleep
import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

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
        # Activate the textarea
        textarea = self.driver.activate_text_area(
            by_method=By.CSS_SELECTOR,
            text_identifier="div#prompt-textarea"
        )

        if not textarea:
            logger.error("Could not activate textarea. Exiting.")
            return False

        # Input prompt and send message
        try:
            self.driver.send_message(chat_input=textarea,
                                     message=message,
                                     submit_method=By.CSS_SELECTOR,
                                     submit_identifier="button[data-testid='send-button']")
        except TimeoutException:
            logger.error("Send button not found. Exiting.")
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