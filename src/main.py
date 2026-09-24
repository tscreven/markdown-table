import argparse
from table_generator import MarkdownTable
import sys
from termcolor import colored


class Parser(argparse.ArgumentParser):
    def error(self, message):
        if "required" in message:
            print()
            print(colored("INVALID ARGUMENT ERROR:", "red"), 
                  "At least two file paths must be passed with the final one being to a Markdown file. See help message below.", 
                  end='\n'*2)
            self.print_help()
        else:
            print(message)

        sys.exit(2)

            
def main():
    parser = Parser(
        description="Generate Markdown tables from CSV, Excel, or NumPy files."
    )
    parser.add_argument("f", nargs='+', help="Path to data file(s).")
    parser.add_argument("md", help="Path to target Markdown file.")
    parser.add_argument("-cols", nargs='+', 
                        help="Column headers to include from the data file.")
    parser.add_argument("-sheets", nargs='+', 
                        help="Excel sheet names to generate tables from.")
    parser.add_argument("-align", choices=["left", "center", "right"], 
                        default="center", help="Table column alignment.")
    parser.add_argument("-line", type=int, default=None,
                        help="Line number where table(s) are inserted in the Markdown file.")
    parser.add_argument("-append", action='store_true', 
                        help="Append table(s) to the end of the Markdown file.")

    args = parser.parse_args()

    col_headers = [] if args.cols is None else args.cols
    excel_sheets = [] if args.sheets is None else args.sheets

    MarkdownTable(args.f, 
                  args.md, 
                  args.align, 
                  args.line, 
                  args.append,
                  col_headers, 
                  excel_sheets
                )

if __name__ == "__main__":
    main()
