# CSVInsight
A dependency-free CSV data-quality and exploratory-analysis CLI.

## Features
- Count rows, columns, exact repeated rows (excluding first occurrence), and blank/whitespace-only cells.
- Infer numeric, text or empty columns and report distinct values, frequent values, min/max/mean/median.
- Export structured JSON for further analysis.

## Run (Python 3.10+)
```sh
python csvinsight.py sample.csv --json report.json
python -m unittest -v
```
The sample has six data rows, one repeated row and one missing score.

## Limitations
Designed for small-to-medium comma-separated UTF-8 files; the profiler stores values and unique rows in memory. Only blanks are missing; strings such as `NA` are not automatically treated as missing. Numeric inference uses finite floating-point values, not semantic date or ID detection. Reports may include sensitive source values; do not publish private data.
