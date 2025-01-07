import os
import sys
import pandas as pd

# Load an excel file
def load_excel_file(_excel_file_path):
    return pd.read_excel(_excel_file_path)

# Retrieve the column values in a list
## _column can be a name or an index
def get_column_values(_excel_file, _column):
    return _excel_file[_column].values.tolist()

# Retrieve the column names in a list
def get_column_names(_excel_file):
    return _excel_file.columns.tolist()

# Write in a specific cell with
def write_in_cell(_excel_file, _excel_file_path, _sheet_name, _column, _row, _cell_value):

    # Write the value into the specified cell
    _excel_file.iat[_row, _column] = _cell_value

    # Save the DataFrame back to the Excel file
    with pd.ExcelWriter(_excel_file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        _excel_file.to_excel(writer, sheet_name=_sheet_name, index=False)

# Rename a column
def rename_column(_excel_file, _old_column_name, _new_column_name):
    _excel_file[_old_column_name].values = [_new_column_name]

# Add a new column
def add_new_column(_excel_file, _old_column_name, _new_column_name):
    _excel_file[_old_column_name].values = [_new_column_name]