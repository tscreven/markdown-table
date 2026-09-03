# markdown-table

`markdown-table` programatically generates Markdown formatted table(s) from a given data file and writes it to a Markdown file. Supported data file formats: CSV (.csv), NumPy (.npy), and Excel (.xlsx) files. 

## Overview

Program processes text from data files and processes them into row-ordered table(s) with column headers. The table is written to a Markdown file either at a specific line number or appendeded to the end of the file.

**CSV and Excel:** Users have the option to specify which column headers from the file to process. If left unspecified, the package will process all columns. The package assumes the first row in the file is column headers. 

**Excel**: For Excel files, a new table is generated for every sheet. There is an additional option to specify what sheet names to generate tables for. If left unspecified, every sheet will be processed.

**NumPy**: Unlike the other two file types, it is required to specify column headers. The first row in the matrix should not be the intended column headers. The number of column headers must match the number of columns in the matrix. 


## Usage
```bash
markdown-table f md -cols -sheets -align -line -append
```

| Argument |                       Description                      |               Required?              |   Default   |        Example        |
| :------: | :----------------------------------------------------: | :----------------------------------: | :---------: | :-------------------: |
|     f    |                        Data file                       |                 Yes                  |             |       data.xlsx       |
|    md    |                      Markdown file                     |                 Yes                  |             |       report.md       |
|   -cols  |    List of column headers to include from data file    | No, unless data file is a NumPy file |             | -cols Time Population |
|  -sheets |   List of sheets from Excel file to write tables for   |                  No                  |             | -sheets Sheet1 Sheet2 |
|  -align  | Table column alignment options: left, center, or right |                  No                  |    center   |      -align right     |
|   -line  |     Line number in Markdown file to write table to     |                  No                  | end of file |        -line 50       |
|  -append |       Flag to write table at end of Markdown file      |                  No                  |    False    |        -append        |


### Examples

```bash
markdown-table data.xlsx report.md -cols Time Population -sheets Sheet1 Sheet2 -align right -line 50
```
Generates two tables for Sheet1 and Sheet2 with columns Time and Population from data.xlsx. The table's columns are right aligned. The table is written on line 50 in report.md.

```bash
markdown-table data.csv report.md -align left -append
```
Generates one table with columns Time and Population from data.csv. The table's columns are left aligned. The table is written to the end of report.md.

```bash
markdown-table data.npy report.md -cols Time Population -line 50
```
Generates one table from the 2D matrix in data.npy with column headers Time and Population. The table's columns are center aligned. The table is written onen line 50 in report.md.