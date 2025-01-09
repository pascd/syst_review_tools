import os
from time import sleep

from src.pdf_analysis_simplifier.web_gpt_handler import WebAIChatInteraction

if __name__ == "__main__":
    # Choose the platform (DEEPSEEK or CHATGPT)
    platform = ""
    while platform != "DEEPSEEK" and platform != "CHATGPT":
        platform = input("Choose the platform (DEEPSEEK or CHATGPT): ").upper()

    # Initialize the interaction
    web_interaction = WebAIChatInteraction(platform=platform)
    web_interaction.launch_web_page()

    sleep(3)

    web_interaction.automated_login(password=os.getenv("DEEPSEEK_PASSWORD"), username=os.getenv("DEEPSEEK_USERNAME"))

    web_interaction.call_for_human()

    # Start a new chat and interact
    web_interaction.init_new_chat()
    sleep(2)
    while True:
        web_interaction.send_message(input("Prompt: "))
        web_interaction.check_response_ended()
        last_message = web_interaction.read_last_message()
        logger.info(f"Last message received: {last_message}")

