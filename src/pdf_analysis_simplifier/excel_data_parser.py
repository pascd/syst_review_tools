import os
import sys
import pandas as pd

class ExcelDataParser:

    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path
        # Load Excel file
        self.excel_file = pd.read_excel(self.excel_file_path)

    # Retrieve the column values in a list
    ## _column can be a name or an index
    def get_column_values(self, _column):
        return self.excel_file[_column].values.tolist()

    # Retrieve the column names in a list
    def get_column_names(self):
        return self.excel_file.columns.tolist()

    # Write in a specific cell with
    def write_in_cell(self, _sheet_name, _column, _row, _cell_value):

        # Write the value into the specified cell
        self.excel_file.iat[_row, _column] = _cell_value

        # Save the DataFrame back to the Excel file
        with pd.ExcelWriter(self.excel_file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            self.excel_file.to_excel(writer, sheet_name=_sheet_name, index=False)

    # Rename a column
    def rename_column(self, _old_column_name, _new_column_name):
        self.excel_file[_old_column_name].values = [_new_column_name]

    # Add a new column
    def add_new_column(self, _old_column_name, _new_column_name):
        self.excel_file[_old_column_name].values = [_new_column_name]