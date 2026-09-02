import argparse
from table_generator import MarkdownTable

def main():
    parser = argparse.ArgumentParser(
        description="Generate Markdown tables from CSV, Excel, or NumPy files."
    )
    parser.add_argument("f", help="Path to data file.")
    parser.add_argument("md", help="Path to target Markdown file.")
    parser.add_argument("-cols", nargs='+', 
                        help="Column headers to include from the data file.")
    parser.add_argument("-sheets", nargs='+', 
                        help="Excel sheet names to generate tables from.")
    parser.add_argument("-align", choices=["left", "center", "right"], 
                        default="center", help="Table column alignment.")
    parser.add_argument("-line", type=int, default=0,
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
