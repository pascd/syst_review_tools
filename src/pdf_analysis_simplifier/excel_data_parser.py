import os
from openpyxl import load_workbook, Workbook
import pandas as pd

class ExcelDataParser:

    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path
        if not os.path.exists(self.excel_file_path):
            raise FileNotFoundError(f"The file '{self.excel_file_path}' does not exist.")
        # Load the Excel file with openpyxl
        self.workbook = load_workbook(self.excel_file_path)

    # Create an Excel file
    def create_excel_file(self, sheet_name="Sheet1"):
        # If file exists
        try:

            self.workbook = load_workbook(self.excel_file_path)
        except FileNotFoundError:
            self.workbook = Workbook()
            self.workbook.remove(self.workbook.active)

    # Create a new sheet in an existing Excel file
    def create_excel_sheet(self, sheet_name):
        sheet = self.workbook.active
        sheet.title = sheet_name
        self.save_workbook()

    def save_workbook(self):
        self.workbook.save(self.excel_file_path)

    # Create the Excel file based on the identifiers given
    def apply_excel_template(self, sheet_name, identifiers):

        # Ensure the sheet exists
        if sheet_name not in self.workbook.sheetnames:
            print(f"Sheet '{sheet_name}' does not exist. Creating it...")
            self.workbook.create_sheet(sheet_name)
        else:
            print(f"Sheet '{sheet_name}' already exists.")

        # Get existing column names
        existing_headers = self.get_column_names(sheet_name)

        # Find the starting column index for new identifiers
        start_col_index = len(existing_headers) + 1

        # Add new identifiers as column names
        for i, identifier in enumerate(identifiers):
            column_index = start_col_index + i
            # Write identifier in the first row of the column
            self.write_in_cell(sheet_name=sheet_name, row=1, column=column_index, cell_value=identifier)

        # Save changes to the file
        self.save_workbook()

    # Retrieve column values in a list
    def get_column_values(self, sheet_name, column):
        sheet = self.workbook[sheet_name]
        # Convert column index (e.g., "A") to rows of values
        return [sheet[f"{column}{row}"].value for row in range(1, sheet.max_row + 1)]

    # Retrieve column names in a list
    def get_column_names(self, sheet_name):
        sheet = self.workbook[sheet_name]
        # Assuming first row contains headers
        return [cell.value for cell in sheet[1]]

    # Write to a specific cell
    def write_in_cell(self, sheet_name, column, row, cell_value):
        sheet = self.workbook[sheet_name]
        # Write the value to the specified cell
        sheet.cell(row=row, column=column, value=cell_value)
        #self.workbook.save(self.excel_file_path)

    # Rename a column
    def rename_column(self, sheet_name, old_column_name, new_column_name):
        sheet = self.workbook[sheet_name]
        headers = self.get_column_names(sheet_name)
        if old_column_name not in headers:
            raise ValueError(f"Column '{old_column_name}' does not exist.")
        # Update the header row
        column_index = headers.index(old_column_name) + 1
        sheet.cell(row=1, column=column_index, value=new_column_name)

        # Save changes to the file
        self.save_workbook()

    # Add a new column
    def add_new_column(self, sheet_name, column_name, default_value=None):
        sheet = self.workbook[sheet_name]
        headers = self.get_column_names(sheet_name)
        new_col_index = len(headers) + 1
        # Add header
        sheet.cell(row=1, column=new_col_index, value=column_name)
        # Fill the new column with the default value
        for row in range(2, sheet.max_row + 1):
            sheet.cell(row=row, column=new_col_index, value=default_value)

        # Save changes to the file
        self.save_workbook()
