#!/usr/bin/env python3
"""
update_data.py
==============
Converts the ICO Excel export into registrars.json for the search page.

Usage:
    python update_data.py
    python update_data.py --input path/to/export.xlsx
    python update_data.py --input export.xlsx --out registrars.json
"""

import pandas as pd
import json
import math
import argparse
import glob
from pathlib import Path

SHEET = 'Active Registration Overviews'

COL_MAP = {
    'raw_id':          '(Do Not Modify) Registration Overview',
    'registration_no': 'Name',
    'name':            'Controller/Processor Name (Last Entry Submitted) (Registration)',
    'organisation_type': 'Organisation Type (Last Entry Submitted) (Registration)',
    'last_entry':      'Last Entry Submitted',
    'status':          'Registration Status',
    'fee_exempt':      'Fee Exempt (Last Entry Submitted) (Registration)',
    'expiry_date':     'Registration Expiry',
    'created_on':      'Created On',
    'modified_on':     '(Do Not Modify) Modified On',
}

def clean(val):
    if val is None: return None
    if isinstance(val, float) and math.isnan(val): return None
    try:
        import pandas as pd
        if pd.isna(val): return None
    except: pass
    if hasattr(val, 'strftime'):
        try: return val.strftime('%Y-%m-%d')
        except: return None
    s = str(val).strip()
    return s if s else None

def convert(xlsx_path, out_path):
    print(f"Reading {xlsx_path}…")
    df = pd.read_excel(xlsx_path, sheet_name=SHEET)
    print(f"  {len(df)} rows found.")

    records = []
    for i, row in df.iterrows():
        rec = {'id': i + 1}
        for key, col in COL_MAP.items():
            rec[key] = clean(row.get(col))
        records.append(rec)

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"  Saved {len(records)} records → {out_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=None, help='Path to Excel file (supports glob)')
    parser.add_argument('--out', default='registrars.json', help='Output JSON path')
    args = parser.parse_args()

    if args.input:
        paths = sorted(glob.glob(args.input))
        xlsx = paths[-1] if paths else args.input
    else:
        # Auto-detect most recent xlsx in current dir
        paths = sorted(glob.glob('*.xlsx'))
        if not paths:
            print('No .xlsx file found. Use --input to specify one.')
            exit(1)
        xlsx = paths[-1]
        print(f"Auto-detected: {xlsx}")

    convert(xlsx, args.out)
