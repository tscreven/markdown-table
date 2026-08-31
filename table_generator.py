import pandas as pd
import sys
import os
from typing import Literal
import numpy as np

def error(message:str):
    print(message)
    sys.exit(1)

class MarkdownTable:

    def __init__(self, data_file, md_file, align: Literal["left", "center", "right"]="center", line_num=1, append=False, 
                 col_headers=[]) -> None:

        if not os.path.exists(data_file):
            error(f"{data_file} does not exist.")

        if md_file[-3:] != ".md":
            error(f"Target {md_file} is not a Markdown file.")

        if not os.path.exists(md_file):
            error(f"{md_file} does not exist.")

        self.data_file = data_file
        self.md_file = md_file
        self.align = align
        self.line_num = line_num 
        self.append = append
        self.col_headers = col_headers
        self.num_cols = len(col_headers)

        self.delegate()


    def delegate(self):
        if self.data_file[-4:] == ".csv":
            self.process_csv()
        elif self.data_file[-4:] == ".npy":
            if self.num_cols == 0:
                error("Column headers must be given for NumPy file.")
            self.process_npy()
        elif self.data_file[-5:] == ".xlsx":
            self.process_excel()
        else:
            error("Invalid file type. Data file must be either a CSV, NumPy, or Excel file.")


    def process_dataframe(self, df):
        num_rows = len(df[self.col_headers[0]])
        rows = [[] for _ in range(num_rows)]

        for category in self.col_headers:

            if category not in df:
                error(f"Category '{category}' is not a column header in {self.data_file}.")

            if len(df[category]) != num_rows:
                error(f"Unequal column length between columns {self.col_headers[0]} and {category}.")

            col_values = df[category]
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
            self.col_headers = headers
            self.num_cols = len(headers)

        df = pd.read_csv(self.data_file)
        self.process_dataframe(df)


    def process_excel(self):

        dfs = pd.read_excel(self.data_file, sheet_name=None)
        sheet_names = list(dfs.keys())
        
        # If no columns given, assume the entire first row is column headers.
        no_headers = self.num_cols == 0

        for i, sheet in enumerate(sheet_names):
            if no_headers:
                headers = dfs[sheet_names[i]].columns
                self.col_headers = headers
                self.num_cols = len(headers)

            df = dfs[sheet]
            self.process_dataframe(df)


    def process_npy(self):

        data = np.load(self.data_file)
        assert type(data) == np.ndarray

        if data.ndim != 2:
            error(f"Invalid number of dimensions in {self.data_file} with {data.ndim} dimension(s). NumPy files must be a 2D matrix.")

        data_cols = data.shape[1]
        if data_cols != self.num_cols:
            print(f"Mismatch in number of columns in NumPy matrix and given column headers.") 

            if data.shape[0] == self.num_cols:
                print("The number of rows match the number of given column headers. Generated table from transposed matrix.")
                data = data.T
            else:
                error(f"{self.data_file} contains {data_cols} columns, given {self.num_cols} column headers.")

        self.gen_table(data.tolist())


    def gen_table(self, rows:list):
        '''Write Markdown formatted table in md_file at line_num or at end of file.'''

        num_lines = 1

        line_prefix = "\n|"
        table_str = line_prefix

        # Column headers
        for h in self.col_headers:
            table_str += f" {h} |"
        table_str += line_prefix

        def aligner() -> str:
            '''Ensures left, center, or right alignment in table.'''
            match self.align:
                case "left":
                    return ":-"
                case "center":
                    return ":-:"      
                case _:
                    return "-:"  

        # Horizontal line separator
        for _ in range(len(self.col_headers)):
            table_str += f" {aligner()} |"

        # Add each row
        for row in rows:
            table_str += line_prefix
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

        self.line_num += num_lines