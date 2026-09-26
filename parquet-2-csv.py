#!/usr/bin/env python3
#
# parquet-2-csv.py
# michael.taylor@cefas.gov.uk 
# 31 Oct 2025
"""
parquet-2-csv.py — Convert a .parquet file to CSV (Excel-friendly) or XLSX.

Usage examples:
  python parquet-2-csv.py data.parquet                     # -> data.csv (UTF‑8)
  python parquet-2-csv.py data.parquet -f xlsx             # -> data.xlsx
  python parquet-2-csv.py data.parquet -o out.csv --excel  # -> out.csv with BOM for Excel
"""

import argparse
import os
import sys

try:
    import pandas as pd
except Exception as e:
    raise SystemExit(
        "This script requires pandas. Install it with: pip install pandas pyarrow"
    ) from e


def convert_parquet(input_path: str,
                    out_path: str | None = None,
                    fmt: str = "csv",
                    excel_bom: bool = False,
                    index: bool = False,
                    sheet_name: str = "Sheet1") -> str:
    """Convert a Parquet file to CSV or XLSX and return the output path."""
    if not os.path.exists(input_path):
        raise SystemExit(f"Input file not found: {input_path}")

    if out_path is None:
        base, _ = os.path.splitext(input_path)
        out_path = base + (".csv" if fmt.lower() == "csv" else ".xlsx")

    # Read Parquet (requires pyarrow or fastparquet)
    try:
        df = pd.read_parquet(input_path)
    except Exception as e:
        raise SystemExit(
            "Failed to read parquet. Ensure you have pyarrow or fastparquet installed "
            "(e.g., pip install pyarrow). Original error: " + str(e)
        ) from e

    fmt = fmt.lower()
    if fmt == "csv":
        # Excel often prefers a UTF-8 BOM for clean Unicode handling on Windows.
        encoding = "utf-8-sig" if excel_bom else "utf-8"
        try:
            df.to_csv(out_path, index=index, encoding=encoding)
        except Exception as e:
            raise SystemExit(f"Failed to write CSV: {e}") from e
    elif fmt == "xlsx":
        try:
            # pandas will use openpyxl by default if available; xlsxwriter is also fine.
            df.to_excel(out_path, index=index, sheet_name=sheet_name)
        except ModuleNotFoundError as e:
            raise SystemExit(
                "Writing .xlsx requires an engine like 'openpyxl' or 'xlsxwriter'. "
                "Install one, e.g.: pip install openpyxl"
            ) from e
        except Exception as e:
            raise SystemExit(f"Failed to write XLSX: {e}") from e
    else:
        raise SystemExit("Unknown format. Use 'csv' or 'xlsx'.")

    return out_path


def main():
    parser = argparse.ArgumentParser(description="Convert Parquet to CSV or XLSX.")
    parser.add_argument("input", help="Path to the .parquet file")
    parser.add_argument("-o", "--out", help="Output file path (optional)")
    parser.add_argument("-f", "--format", choices=["csv", "xlsx"], default="csv",
                        help="Output format (default: csv)")
    parser.add_argument("--excel", action="store_true",
                        help="CSV only: add a UTF-8 BOM so Excel opens Unicode cleanly")
    parser.add_argument("--index", action="store_true",
                        help="Include the DataFrame index in the output")
    parser.add_argument("--sheet-name", default="Sheet1",
                        help="XLSX only: worksheet name (default: Sheet1)")
    args = parser.parse_args()

    out = convert_parquet(args.input, args.out, args.format, args.excel, args.index, args.sheet_name)
    print(f"Wrote: {out}")


if __name__ == "__main__":
    main()
