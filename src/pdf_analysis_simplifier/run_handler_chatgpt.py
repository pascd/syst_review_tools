import sys
import os

# Dynamically add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.pdf_analysis_simplifier.chatgpt_interaction_manager import ChatGPTInteractionManager

if __name__ == "__main__":

    chatgpt_handler = ChatGPTInteractionManager()

    chatgpt_handler.launch_chatpgt_page()

    chatgpt_handler.login()

    while True:
        chatgpt_handler.send_and_receive(message=input("Prompt: "))