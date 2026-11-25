"""Profile a UTF-8 CSV file with the Python standard library."""
import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from statistics import mean, median


def number(value):
    try:
        n = float(value)
        return n if math.isfinite(n) else None
    except ValueError:
        return None


def profile(source):
    reader = csv.reader(source, strict=True)
    headers = next(reader, None)
    if not headers or any(not h.strip() for h in headers) or len(set(headers)) != len(headers):
        raise ValueError('CSV requires nonempty, unique column names')
    columns = [[] for _ in headers]
    seen = set()
    duplicates = count = 0
    for row in reader:
        if not row:
            continue
        if len(row) != len(headers):
            raise ValueError(f'Line {reader.line_num}: expected {len(headers)} fields, got {len(row)}')
        count += 1
        key = tuple(row)
        if key in seen:
            duplicates += 1
        seen.add(key)
        for col, value in zip(columns, row):
            col.append(value.strip())
    report = []
    for name, col in zip(headers, columns):
        present = [v for v in col if v]
        nums = [number(v) for v in present]
        numeric = bool(present) and all(n is not None for n in nums)
        item = {'name': name, 'type': 'empty' if not present else 'numeric' if numeric else 'text',
                'missing': count - len(present), 'unique_nonempty': len(set(present)),
                'top_values': [{'value': v, 'count': n} for v, n in Counter(present).most_common(3)]}
        if numeric:
            item['statistics'] = {'min': min(nums), 'max': max(nums), 'mean': mean(nums), 'median': median(nums)}
        report.append(item)
    return {'rows': count, 'columns': len(headers), 'duplicate_rows': duplicates, 'column_profiles': report}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file', type=Path)
    parser.add_argument('--json', type=Path, help='Write a machine-readable report')
    args = parser.parse_args()
    try:
        if args.json and args.json.resolve() == args.csv_file.resolve():
            raise ValueError('Output must differ from input')
        with args.csv_file.open(encoding='utf-8-sig', newline='') as handle:
            result = profile(handle)
        print(f"Rows: {result['rows']} | Columns: {result['columns']} | Duplicate rows: {result['duplicate_rows']}")
        for c in result['column_profiles']:
            print(f"{c['name']}: {c['type']}; missing={c['missing']}; unique={c['unique_nonempty']}")
            if 'statistics' in c:
                print('  ' + ' | '.join(f'{k}: {v:.6g}' for k, v in c['statistics'].items()))
        if args.json:
            args.json.write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)+'\n', encoding='utf-8')
            print(f'Report written to {args.json}')
    except (OSError, ValueError, csv.Error, OverflowError) as exc:
        parser.exit(2, f'CSVInsight: {exc}\n')


if __name__ == '__main__':
    main()
