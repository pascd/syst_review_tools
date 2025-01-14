import os
import sys
import pandas as pd
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Assuming the classes are in the same directory or properly referenced
from src.pdf_analysis_simplifier.excel_data_parser import ExcelDataParser
from src.pdf_analysis_simplifier.response_handler import ResponseHandler
from src.pdf_analysis_simplifier.chatgpt_interaction_manager import ChatGPTInteractionManager
from src.pdf_analysis_simplifier.review_data_parser import ReviewDataParser

class PDFToExcelProcessor:
    def __init__(self, pdf_folder_path, analysed_folder_path, excel_file_path, review_config, qa_sheet_name, de_sheet_name):
        self.pdf_folder_path = pdf_folder_path
        self.excel_file_path = excel_file_path
        self.qa_sheet_name = qa_sheet_name
        self.de_sheet_name = de_sheet_name
        self.analysed_folder_path = analysed_folder_path
        self.chatgpt_manager = ChatGPTInteractionManager()
        self.response_handler = ResponseHandler()
        self.excel_parser = ExcelDataParser(excel_file_path)
        self.review_parser = ReviewDataParser(review_config)

        # Retrieve all identifiers
        self.qa_fields = self.review_parser.get_all_quality_assessment_fields()
        self.data_extraction_fields = self.review_parser.get_all_data_extraction_fields()
        self.cutoff_score = self.review_parser.get_cutoff_score()

    # Initiate the chatgpt manager
    def initiate_chatgpt_manager(self):
        self.chatgpt_manager.launch_chatpgt_page()
        self.chatgpt_manager.login()
        return True

    # Iterate over all pdfs in folder, and return list with all pdf paths
    def get_pdf_paths(self):
        # Ensure the folder path exists
        if not os.path.exists(self.pdf_folder_path):
            raise FileNotFoundError(f"The folder '{self.pdf_folder_path}' does not exist.")

        # Get the absolute path of the folder
        pdf_folder_path = os.path.abspath(self.pdf_folder_path)

        # List all files in the folder and filter for PDFs
        pdf_files = [os.path.join(pdf_folder_path, f) for f in os.listdir(pdf_folder_path) if f.lower().endswith(".pdf")]

        return pdf_files

    # Send pdf and wait for response
    def send_pfd_to_analysis(self, pdf_file):
        return self.chatgpt_manager.send_and_receive(pdf_file)

    # Extract the text associated with a specific identifier
    def extract_data_from_response(self, response, identifiers):
        extracted_data = {}
        try:
            for identifier in identifiers:
                extracted_text = self.response_handler.extract_by_identifier(response=response, identifier=identifier)

                if extracted_text:
                    extracted_data[identifier] = extracted_text
                else:
                    logger.warning(f"No text found for identifier: {identifier}")
                    return None
            return extracted_data
        except:
            logger.warning(f"Error retrieving data from identifiers)")

    # Write the retrieved data for all identifiers in Excel file
    def write_data_to_excel(self, extracted_data, sheet_name):

        # Create a new DataFrame with the extracted data
        data = {identifier: [extracted_data.get(identifier, "")] for identifier in self.identifiers}
        df = pd.DataFrame(data)

        # Save the DataFrame to the Excel file
        with pd.ExcelWriter(self.excel_file_path, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        return True

    # Move analysed files from source folder to other folder
    def move_analysed_files(self):
        if not os.path.isdir(self.analysed_folder_path):
            return True



    # Run the sequence for PDF analysis
    def run(self):

        # Initialize the Excel file for analysis
        self.excel_parser.create_excel_file()
        qa_identifiers = [question["id"] for question in self.review_parser.get_all_quality_assessment_fields()]
        self.excel_parser.apply_excel_template(sheet_name=self.qa_sheet_name, identifiers=qa_identifiers)

        de_fields = [field["key"] for field in self.review_parser.get_all_data_extraction_fields()]
        self.excel_parser.apply_excel_template(sheet_name=self.de_sheet_name, identifiers=de_fields)

        # Initiate chatgpt manager
        self.initiate_chatgpt_manager()

        # Retrieve all existing PDFs
        all_pdf_paths = self.get_pdf_paths()

        for pdf_path in all_pdf_paths:

            # Input the file
            self.chatgpt_manager.input_external_file(file_path=pdf_path)

            time.sleep(2)

            # Send pdf to analysis and retrieve answer
            response = self.send_pfd_to_analysis(self.review_parser.get_analysis_prompt())

            time.sleep(2)

            # Extract the desired content from response
            extracted_qa_data = self.extract_data_from_response(response, qa_identifiers)

            if extracted_qa_data:
                # Write the extracted data into the Excel file
                self.write_data_to_excel(extracted_data=extracted_qa_data, sheet_name=self.qa_sheet_name)
            else:
                print(f"No data found for Quality Assessment analysis.")

            # If the article passed the cutoff score, retrieve data extraction information
            paper_score = self.extract_data_from_response(response, "#score")

            if paper_score:

                if paper_score >= self.cutoff_score:
                    # Extract the desired content from response
                    extracted_de_data = self.extract_data_from_response(response, de_fields)

                    if extracted_de_data:
                        self.write_data_to_excel(extracted_data=extracted_de_data, sheet_name=self.de_sheet_name)
                    else:
                        print(f"No data found for Data Extraction analysis.")
                else:
                    print("Paper has a score lower than the cutoff score.")
                    time.sleep(2)
                    continue
            else:
                print("No score found for specific paper")
                break