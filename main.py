import argparse
from table_generator import MarkdownTable

def main():
    parser = argparse.ArgumentParser("fill in")
    parser.add_argument("f", help="Path to file.")
    parser.add_argument("md", help="Markdown file.")
    parser.add_argument("-cols", nargs='+', 
                        help="Column headers to display from data file.")
    parser.add_argument("-sheets", nargs='+', 
                        help="Sheet names to generate table for if data file is an Excel file.")
    parser.add_argument("-align", choices=["left", "center", "right"], 
                        default="center", help="Markdown file.")
    parser.add_argument("-line", type=int, default=0,
                        help="Line number where table(s) are written to in Markdown file.")
    parser.add_argument("-append", action='store_true', help="Append table to end of Markdown file.")

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
