import sys
import os
import time

# Dynamically add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.pdf_analysis_simplifier.pdf_to_excel import PDFToExcelProcessor

if __name__ == "__main__":

    pdf_to_excel_processor = PDFToExcelProcessor(pdf_folder_path="./pdf-files/",
                                                 excel_file_path="/home/pedrodias/Documents/git-repos/syst_review_tools/src/pdf_analysis_simplifier/excel-files/analysis_excel_file.xlsx",
                                                 qa_sheet_name="qa_sheet",
                                                 de_sheet_name="de_sheet",
                                                 review_config="./review_data.yaml")

    pdf_to_excel_processor.run()