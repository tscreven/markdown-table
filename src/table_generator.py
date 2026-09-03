import pandas as pd
import sys
import os
from typing import Literal
import numpy as np

def error(message:str):
    print(message)
    sys.exit(1)

class MarkdownTable:

    def __init__(self, 
                 data_file, md_file, 
                 table_alignment: Literal["left", "center", "right"], 
                 line_num:int, append:bool, col_headers:list, excel_sheets:list
                ) -> None:

        if not os.path.exists(data_file):
            error(f"{data_file} does not exist.")

        if md_file[-3:] != ".md":
            error(f"Target {md_file} is not a Markdown file.")

        if not os.path.exists(md_file):
            error(f"{md_file} does not exist.")

        if not append and line_num <= 0:
            append = True

        self.data_file = data_file
        self.md_file = md_file
        self.align = table_alignment
        self.line_num = line_num 
        self.append = append
        self.col_headers = col_headers
        self.num_cols = len(col_headers)

        if self.data_file[-4:] == ".csv":
            self.process_csv()
        elif self.data_file[-4:] == ".npy":
            if self.num_cols == 0:
                error("Column headers must be given for NumPy file.")
            self.process_npy()
        elif self.data_file[-5:] == ".xlsx":
            self.process_excel(excel_sheets)
        else:
            error("Invalid file type. Data file must be either a CSV (.csv), NumPy (.npy), or Excel (.xlsx) file.")


    def col_header_update(self, headers):
        '''Update instance for tracking new column headers.'''
        if len(headers) == 0:
            error(f"No column headers given and column headers could not be located in {self.data_file}.")
        self.col_headers = headers
        self.num_cols = len(headers)


    def process_dataframe(self, df:pd.DataFrame):
        '''Helper function for file processing functions using Dataframes.'''

        def check_header(header):
            if header not in df:
                error(f'Category "{header}" is not a column header in {self.data_file}. Note that column headers are case sensitive.')

        check_header(self.col_headers[0])

        num_rows = len(df[self.col_headers[0]])
        rows = [[] for _ in range(num_rows)]

        for header in self.col_headers:

            check_header(header)

            if len(df[header]) != num_rows:
                error(f"Unequal column length between columns {self.col_headers[0]} and {header}.")

            col_values = df[header]
            for i in range(num_rows):
                rows[i].append(col_values[i])

        self.gen_table(rows)


    def process_csv(self):
        '''Process given CSV file: find column headers if none given and store
        values for all tracked column headers in row order.'''
        # If no columns given, assume the entire first row is column headers.
        if self.num_cols == 0:
            with open(self.data_file, 'r') as f:
                line = next(f)
            headers = line.strip().split(',')
            self.col_header_update(headers)

        df = pd.read_csv(self.data_file)
        self.process_dataframe(df)


    def process_excel(self, sheet_names:list):
        '''Process given Excel file: find column headers in sheet_names if none
        are given and store values for all tracked column headers in row order.
        If there are multiple sheets, generate a table for each sheet.'''

        dfs = pd.read_excel(self.data_file, sheet_name=None)
        all_file_sheets = dfs.keys()
        if sheet_names == []:
            # Load all sheets in Excel file if sheet_names is unspecified.
            sheet_names = list(all_file_sheets)
        else:
            for sheet in sheet_names:
                if sheet not in all_file_sheets:
                    error(f"Sheet name {sheet} is not in {self.data_file}.")
        
        # If no columns given, assume the entire first row is column headers.
        no_headers = self.num_cols == 0

        for i, sheet in enumerate(sheet_names):
            if no_headers:
                headers = dfs[sheet_names[i]].columns
                self.col_header_update(headers)

            df = dfs[sheet]
            self.process_dataframe(df)


    def process_npy(self):
        '''Process given NumPy file: Column headers must be given. Table values
        are stored in 2D NumPy matrix in row order; transpose the matrix if it
        is required to match the number of expected columns.'''

        data = np.load(self.data_file)
        assert type(data) == np.ndarray

        if data.ndim != 2:
            error(f"Invalid number of dimensions in {self.data_file} with {data.ndim} dimension(s). NumPy files must be a 2D matrix.")

        data_cols = data.shape[1]
        if data_cols != self.num_cols:
            print(f"Mismatch in number of columns in NumPy matrix and given column headers.") 

            if data.shape[0] == self.num_cols:
                print("The number of rows match the number of listed column headers. Generated table from transposed matrix.")
                data = data.T
            else:
                error(f"{self.data_file} contains {data_cols} columns, given {self.num_cols} column headers.")

        self.gen_table(data.tolist())


    def gen_table(self, rows:list):
        '''Write Markdown formatted table in md_file at line_num or at end of file.'''

        next_line = "\n|"
        table_str = next_line

        # Column headers
        for h in self.col_headers:
            table_str += f" {h} |"
        table_str += next_line

        if self.align == "left":
            sep = ":-"
        elif self.align == "center":
            sep = ":-:" 
        else: # right alignment
            sep = "-:" 

        # Horizontal line separator
        for _ in range(self.num_cols):
            table_str += f" {sep} |"

        # Add each row
        for row in rows:
            table_str += next_line
            for item in row:
                table_str += f" {item} |"

        new_lines = len(rows) + 4

        # Need extra new line for formatting. 
        table_str += "\n"*2

        with open(self.md_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if self.append or self.line_num + 1 > len(lines):
            with open(self.md_file, "a", encoding="utf-8") as f:
                f.write('\n')
                f.write(table_str[:-1])
                new_lines += 1
        else:
            lines.insert(self.line_num - 1, table_str)
            with open(self.md_file, "w", encoding="utf-8") as f:
                f.writelines(lines)