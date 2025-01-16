import os
import time
import pandas as pd
import logging
import shutil
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from src.pdf_analysis_simplifier.excel_data_parser import ExcelDataParser
from src.pdf_analysis_simplifier.response_handler import ResponseHandler
from src.pdf_analysis_simplifier.chatgpt_interaction_manager import ChatGPTInteractionManager
from src.pdf_analysis_simplifier.review_data_parser import ReviewDataParser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFToExcelProcessor:
    def __init__(self, pdf_folder_path, analysed_folder_path, excel_file_path, review_config, qa_sheet_name, de_sheet_name):
        self.pdf_folder_path = pdf_folder_path
        self.analysed_folder_path = analysed_folder_path
        self.excel_file_path = excel_file_path
        self.qa_sheet_name = qa_sheet_name
        self.de_sheet_name = de_sheet_name
        self.chatgpt_manager = ChatGPTInteractionManager()
        self.response_handler = ResponseHandler()
        self.excel_parser = ExcelDataParser(excel_file_path)
        self.review_parser = ReviewDataParser(review_config)

        # Load quality assessment and data extraction fields
        self.qa_fields = self.review_parser.get_all_quality_assessment_fields()
        self.data_extraction_fields = self.review_parser.get_all_data_extraction_fields()
        self.cutoff_score = self.review_parser.get_cutoff_score()

    def initiate_chatgpt_manager(self):
        self.chatgpt_manager.launch_chatpgt_page()
        self.chatgpt_manager.login()
        return True

    def get_pdf_paths(self):
        if not os.path.exists(self.pdf_folder_path):
            raise FileNotFoundError(f"The folder '{self.pdf_folder_path}' does not exist.")
        return [os.path.join(self.pdf_folder_path, f) for f in os.listdir(self.pdf_folder_path) if f.lower().endswith(".pdf")]

    def send_pdf_to_analysis(self, pdf_file):
        try:
            return self.chatgpt_manager.send_and_receive(pdf_file)
        except Exception as e:
            logger.error(f"Error sending PDF for analysis: {e}")
            return None

    def move_analysed_file(self, file_path):
        if not os.path.exists(self.analysed_folder_path):
            os.makedirs(self.analysed_folder_path, exist_ok=True)
        try:
            shutil.move(file_path, self.analysed_folder_path)
            logger.info(f"Moved '{file_path}' to '{self.analysed_folder_path}'.")
        except Exception as e:
            logger.error(f"Error moving file '{file_path}': {e}")

    def run(self):
        # Initialize the Excel sheets
        self.excel_parser.create_excel_file()
        qa_identifiers = [qa["id"] for qa in self.qa_fields]
        self.excel_parser.apply_excel_template(self.qa_sheet_name, qa_identifiers + ["Average Score"])
        de_identifiers = [de["key"] for de in self.data_extraction_fields]
        self.excel_parser.apply_excel_template(self.de_sheet_name, de_identifiers)

        # Initialize ChatGPT manager
        self.initiate_chatgpt_manager()

        for pdf_path in self.get_pdf_paths():
            try:
                logger.info(f"Processing file: {pdf_path}")
                self.chatgpt_manager.input_external_file(pdf_path)
                time.sleep(2)

                # Send analysis prompt and get response
                prompt = self.review_parser.get_analysis_prompt()
                response = self.send_pdf_to_analysis(prompt)

                if not response:
                    logger.warning(f"No response for file: {pdf_path}")
                    continue

                # Extract QA data and calculate average score
                qa_data = self.review_parser.get_quality_assessment_text(response)
                paper_score = qa_data.pop("Total Score", 0)  # Extract average score for logging
                if qa_data:
                    self.excel_parser.fill_excel_with_data(self.qa_sheet_name, {**qa_data, "Total Score": paper_score})
                    logger.info(f"Total QA Score: {paper_score}")
                else:
                    logger.warning(f"No QA data found for file: {pdf_path}")

                # Extract and write DE data only if the score meets the cutoff
                if paper_score and paper_score >= self.cutoff_score:
                    logger.info(f"Paper score ({paper_score}) meets the cutoff ({self.cutoff_score}). Extracting DE data...")
                    de_data = self.review_parser.get_data_extraction_text(response)
                    if de_data:
                        self.excel_parser.fill_excel_with_data(self.de_sheet_name, de_data)
                    else:
                        logger.warning(f"No DE data found for file: {pdf_path}")
                else:
                    logger.info(f"Paper score ({paper_score}) does not meet the cutoff ({self.cutoff_score}). Skipping DE data extraction.")

                # Move the file to the analysed folder
                self.move_analysed_file(pdf_path)

            except Exception as e:
                logger.error(f"Error processing file '{pdf_path}': {e}")


