# parquet-2-csv.py — Parquet → CSV/XLSX Converter

A tiny, no-frills command-line utility to convert `.parquet` files into **CSV** (Excel-friendly) or **XLSX**.

This README covers installation, Python dependencies, usage, and common troubleshooting tips.

---

## Features

- Convert Parquet to:
  - **CSV** (UTF-8 by default, optional Excel-friendly BOM)
  - **XLSX** (Excel workbook)
- Keep or drop the DataFrame index
- Choose a custom output filename
- Set a worksheet name for `.xlsx` output

---

## Requirements

- **Python:** 3.10+  
  (The script uses modern type hints like `str | None`.)
- **Core dependency:** `pandas`
- **Parquet back-end (choose one):**
  - `pyarrow` (recommended), or
  - `fastparquet`
- **XLSX writer (choose one, only needed for `-f xlsx`):**
  - `openpyxl` (recommended), or
  - `xlsxwriter`

### Quick install

```bash
# CSV only
pip install pandas pyarrow

# If you also want XLSX output
pip install pandas pyarrow openpyxl
```

> On Windows you can use: `py -m pip install ...`

---

## Getting the script

Download the script and place it anywhere on your PATH (or run it with Python directly).

- **Script:** `parquet-2-csv.py`

Make it executable on macOS/Linux:

```bash
chmod +x parquet-2-csv.py
```

---

## Usage

```text
usage: parquet-2-csv.py [-h] [-o OUT] [-f {csv,xlsx}] [--excel] [--index] [--sheet-name SHEET_NAME] input

Convert Parquet to CSV or XLSX.

positional arguments:
  input                 Path to the .parquet file

options:
  -h, --help            Show this help message and exit
  -o, --out OUT         Output file path (optional)
  -f, --format {csv,xlsx}
                        Output format (default: csv)
  --excel               CSV only: add a UTF-8 BOM so Excel opens Unicode cleanly
  --index               Include the DataFrame index in the output
  --sheet-name SHEET_NAME
                        XLSX only: worksheet name (default: Sheet1)
```

---

## Examples

- **CSV (default):**
  ```bash
  python parquet-2-csv.py data.parquet
  # -> data.csv (UTF-8)
  ```

- **Excel `.xlsx`:**
  ```bash
  python parquet-2-csv.py data.parquet -f xlsx
  # -> data.xlsx
  ```

- **Excel-friendly CSV (adds UTF‑8 BOM so Excel handles Unicode cleanly on Windows):**
  ```bash
  python parquet-2-csv.py data.parquet --excel
  # -> data.csv (UTF-8 with BOM)
  ```

- **Choose output name:**
  ```bash
  python parquet-2-csv.py data.parquet -o out.csv
  ```

- **Include DataFrame index:**
  ```bash
  python parquet-2-csv.py data.parquet --index
  ```

- **Custom worksheet name for XLSX:**
  ```bash
  python parquet-2-csv.py data.parquet -f xlsx --sheet-name MySheet
  ```

---

## Troubleshooting

- **“This script requires pandas”**  
  Install pandas (and a Parquet engine):
  ```bash
  pip install pandas pyarrow
  ```

- **“Failed to read parquet… Ensure you have pyarrow or fastparquet installed”**  
  Install a Parquet back-end:
  ```bash
  pip install pyarrow
  # or
  pip install fastparquet
  ```

- **“Writing .xlsx requires an engine like 'openpyxl' or 'xlsxwriter'”**  
  Install one of the XLSX engines:
  ```bash
  pip install openpyxl
  # or
  pip install xlsxwriter
  ```

- **Encoding looks wrong in Excel (weird characters):**  
  Use the `--excel` switch for CSV to include a UTF‑8 BOM which helps Excel on Windows:
  ```bash
  python parquet-2-csv.py data.parquet --excel
  ```

- **Very large files:**  
  The script loads the whole file into memory via pandas. For huge datasets, consider chunked CSV export strategies or a dedicated ETL tool.

---

## How it works (briefly)

- Uses `pandas.read_parquet(...)` to load the dataset (via `pyarrow` or `fastparquet`).
- Writes:
  - CSV with `DataFrame.to_csv(...)` (`utf-8` by default, `utf-8-sig` with `--excel`), or
  - XLSX with `DataFrame.to_excel(...)` (engine auto-detected if installed).

---

## 📄 License

The code is distributed under terms and conditions of the [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

See [`LICENSE.md`](LICENSE.md).

---

## 🤝 Contributing

Issues and PRs are welcome. When filing an issue, please include:

- a minimal CSV sample (or a snippet),
- the exact command you ran,
- the observed vs. expected output (and a PNG if possible).

 Contact information:

* [Michael Taylor](michael.taylor@cefas.gov.uk)



