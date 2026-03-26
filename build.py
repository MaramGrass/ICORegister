#!/usr/bin/env python3
"""
build.py — Regenerate index.html from a fresh Excel export.

Usage:
    python build.py                          # auto-detects newest .xlsx in folder
    python build.py --input new_export.xlsx  # specify file
"""
import pandas as pd, json, math, argparse, glob, shutil
from pathlib import Path

SHEET = 'Active Registration Overviews'

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

def build(xlsx_path):
    print(f"Reading {xlsx_path}...")
    df = pd.read_excel(xlsx_path, sheet_name=SHEET)
    records = []
    for i, row in df.iterrows():
        name   = clean(row['Controller/Processor Name (Last Entry Submitted) (Registration)'])
        status = clean(row['Registration Status'])
        if not name or not status:
            continue
        records.append({
            'id':      len(records),
            'regNo':   clean(row['Name']),
            'name':    name,
            'orgType': clean(row['Organisation Type (Last Entry Submitted) (Registration)']),
            'entry':   clean(row['Last Entry Submitted']),
            'status':  status,
            'exempt':  clean(row['Fee Exempt (Last Entry Submitted) (Registration)']),
            'expiry':  clean(row['Registration Expiry']),
            'created': clean(row['Created On']),
            'modified':clean(row['(Do Not Modify) Modified On']),
        })
    print(f"  {len(records)} valid records found.")
    data_json = json.dumps(records, separators=(',', ':'))

    template = Path('index_template.html').read_text(encoding='utf-8')
    html = template.replace('%%DATA%%', data_json)
    Path('index.html').write_text(html, encoding='utf-8')
    print(f"  index.html written ({len(html)//1024} KB)")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=None)
    args = parser.parse_args()
    if args.input:
        xlsx = args.input
    else:
        files = sorted(glob.glob('*.xlsx'))
        if not files:
            print("No .xlsx file found. Use --input to specify one.")
            exit(1)
        xlsx = files[-1]
        print(f"Auto-detected: {xlsx}")
    build(xlsx)
