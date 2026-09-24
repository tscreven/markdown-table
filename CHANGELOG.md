# Changelog

Changelog introduced in version 0.1.4.

## [1.1.0] - 2026-09-24

### Changed
- Standardized line spacing around generated tables no matter where it is written: one empty line above and below the table.
    - Except if appending to the end of the file, no empty line after the last generated table.
- Implemented custom error messaging when incorrectly formatted arguments are provided.
- When line number is not provided, append to end of file, instead of inserting table(s) on the first line.
- Return error when provided line number is non-positive, instead of inserting table(s) on the first line.

## [1.0.0] - 2026-09-08

### Changed
- Multiple data files can now be provided.

### Fixed
- Fixed displaying "nan" when there is an empty value in a CSV or Excel file.

## [0.1.4] - 2026-09-07

### Changed
- Formatting of error messages.
- Started Changelog documentation.

### Fixed
- Fixed handling of CSV files with unequal number of commas between lines.
