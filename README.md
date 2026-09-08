# md_table_writer

`md_table_writer` generates Markdown formatted table(s) from one or more data files and writes them to a Markdown file. Supported data file formats: CSV (.csv), NumPy (.npy), and Excel (.xlsx). 

## Download

```bash
pip install md_table_writer
```

## Overview

`md_table_writer` converts data files into Markdown-formatted tables with column headers. 

Multiple data files can be provided, and they are processed in order. If more than one data file is provided, all file specific options must be valid across all files. A new set of tables is generated for each provided data file. Generated tables are inserted into a Markdown file either at a specific line number or appended to the end of the file. 

### Number of Tables Generated per File
CSV and NumPy data files generate one table per file. Excel data files generate one table per sheet.

### File Specific Arguments

**CSV:** Users can specify which column headers from the file to include through the `-cols` option. If `-cols` is not provided, all columns are included. The first row in the data file must be exclusively for column headers. 

**Excel:** Option `-sheets` processes only select sheets. If `-sheets` is not provided, every sheet will be processed.

**NumPy:** Unlike the other two file types, column headers must be provided via `-cols`. The NumPy matrix should be data only: the first row should not contain column headers. The number of provided column headers must match the number of columns in the matrix. 


## Usage
```bash
md_table_writer f md -cols -sheets -align -line -append
```

| Argument | Description | Required? | Default | Example |
| :------: | :---------- | :-------- | :------ | :------ |
| `f` | Paths to the input data files; files are processed in their provided order | Yes, must input at least one file path | - | `data.xlsx` |
| `md` | Path to the target Markdown file | Yes | - | `report.md` |
| `-cols` | Column headers to process from data files | No, unless at least one data file is a NumPy file | All columns for CSV/Excel | `-cols Time Population` |
| `-sheets` | List of sheets from Excel file to generate tables for | No | All sheets | `-sheets Sheet1 Sheet2` |
| `-align` | Table column alignment options: left, center, or right | No | center | `-align right` |
| `-line` | Line number in Markdown file to insert | No | end of file | `-line 50` |
| `-append` | Append generated table to the end of the Markdown file | No | False | `-append` |

### Argument Positioning
The only two positional arguments are `f` (paths to data files) and `md` (path to Markdown file). All data file paths must be specified before the Markdown file path. Both positional arguments must be provided before other options.

### Examples

```bash
md_table_writer data.xlsx report.md -cols Time Population -sheets Sheet1 Sheet2 -align right -line 50
```
Generates two tables for Sheet1 and Sheet2 with columns Time and Population from data.xlsx. The table's columns are right aligned. The table is written on line 50 in report.md.

```bash
md_table_writer data.csv report.md -align left -append
```
Generates one table with all column headers in data.csv. The table's columns are left aligned. The table is written to the end of report.md.

```bash
md_table_writer data.npy report.md -cols Time Population -line 50
```
Generates one table from the 2D matrix in data.npy with column headers Time and Population. The table's columns are center aligned. The table is written on line 50 in report.md.

```bash
md_table_writer data.csv data.npy report.md -cols Time Population -line 50
```
Generates two tables, one from data.csv and the other from data.npy. Both tables have column headers Time and Population. The table's columns are center aligned. Both tables are written on line 50 in report.md.
