from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "Input"
OUTPUT_DIR = BASE_DIR / "Output"
ARCHIVE_DIR = BASE_DIR / "Archive"

for folder in (INPUT_DIR, OUTPUT_DIR, ARCHIVE_DIR):
    folder.mkdir(parents=True, exist_ok=True)

EMPLOYEE_EXCEL = INPUT_DIR / "Employees.xlsx"
SALES_EXCEL = INPUT_DIR / "Sales.xlsx"
EMPLOYEE_CSV = INPUT_DIR / "Employees.csv"