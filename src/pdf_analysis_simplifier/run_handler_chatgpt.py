from time import sleep
import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dynamically add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.pdf_analysis_simplifier.web_gpt_handler import WebAIChatInteraction

if __name__ == "__main__":

    # Initialize the interaction
    web_interaction = WebAIChatInteraction()
    web_interaction.launch_web_page(url="https://www.chatgpt.com/")

    sleep(3)

    # If required, call for human intervention
    try:
        web_interaction.call_for_human()
        sleep(1)
    except Exception as e:
        logger.warning(f"Call for human interaction failed: {e}")

    # Main loop for chat interaction
    while True:
        # Activate the textarea
        textarea = web_interaction.activate_text_area(
            by_method=By.CSS_SELECTOR,
            text_identifier="div#prompt-textarea"
        )

        if not textarea:
            logger.error("Could not activate textarea. Exiting.")
            break

        # Input prompt and send message
        try:
            web_interaction.send_message(chat_input=textarea, message=input("Prompt: "), submit_method=By.CSS_SELECTOR, submit_identifier="button[data-testid='send-button']")
        except TimeoutException:
            logger.error("Send button not found. Exiting.")
            break

        # Wait for response to finish and retrieve it
        try:
            web_interaction.check_response_ended(By.CSS_SELECTOR, "button[data-testid='copy-turn-action-button']")
            response = web_interaction.read_last_message(By.CSS_SELECTOR, "div[data-message-author-role='assistant'] div.markdown.prose")
            logger.info(f"Response: {response}")
        except NoSuchElementException:
            logger.error("Failed to read the response. Please check the webpage layout.")
            break
