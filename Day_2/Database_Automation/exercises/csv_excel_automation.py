
import csv
from pathlib import Path
from decimal import Decimal
from datetime import datetime

from openpyxl import Workbook, load_workbook

from mysql.connector import Error

from Database_Automation.database.connection import (
    get_database_connection
)


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "output"

CSV_INPUT = OUTPUT_DIR / "employees_input.csv"

EXCEL_INPUT = OUTPUT_DIR / "employees_input.xlsx"

CSV_OUTPUT = OUTPUT_DIR / "employees_export.csv"

EXCEL_OUTPUT = OUTPUT_DIR / "employees_report.xlsx"

HEADERS = [
    "name",
    "email",
    "department",
    "salary"
]


# --------------------------------------------------
# 2. CREATE SAMPLE CSV AND EXCEL FILES
# --------------------------------------------------

def create_sample_files():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sample_records = [
        {
            "name": "CSV User 1",
            "email": "csv1@example.com",
            "department": "IT",
            "salary": 50000
        },
        {
            "name": "CSV User 2",
            "email": "csv2@example.com",
            "department": "HR",
            "salary": 45000
        },
        {
            "name": "CSV User 3",
            "email": "csv3@example.com",
            "department": "Finance",
            "salary": 55000
        }
    ]

    # Create CSV
    with open(CSV_INPUT, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=HEADERS
        )

        writer.writeheader()
        writer.writerows(sample_records)

    # Create Excel
    workbook = Workbook()

    worksheet = workbook.active
    worksheet.title = "Employees"

    worksheet.append(HEADERS)

    for record in sample_records:
        worksheet.append([
            record["name"],
            record["email"],
            record["department"],
            record["salary"]
        ])

    workbook.save(EXCEL_INPUT)

    print("Sample CSV and Excel files created!")


# --------------------------------------------------
# 3. CREATE DATABASE TABLE
# --------------------------------------------------

def setup_table(cursor, connection):

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS imported_employees (

            id INT AUTO_INCREMENT PRIMARY KEY,

            name VARCHAR(100) NOT NULL,

            email VARCHAR(150) UNIQUE NOT NULL,

            department VARCHAR(100),

            salary DECIMAL(10, 2),

            source_file VARCHAR(100),

            imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    print("Import table ready!")


# --------------------------------------------------
# 4. VALIDATE RECORDS
# --------------------------------------------------

def validate_records(records):

    valid_records = []
    seen_emails = set()

    for record in records:

        name = str(record.get("name") or "").strip()

        email = str(record.get("email") or "").strip()

        department = str(
            record.get("department") or ""
        ).strip()

        salary_value = record.get("salary")

        if not name or not email or not salary_value:
            continue

        try:

            salary = Decimal(str(salary_value))

        except Exception:
            continue

        if not salary.is_finite() or salary < 0:
            continue

        if "@" not in email:
            continue

        normalized_email = email.lower()

        if normalized_email in seen_emails:
            continue

        seen_emails.add(normalized_email)

        valid_records.append((
            name,
            email,
            department,
            salary
        ))

    return valid_records


# --------------------------------------------------
# 5. READ CSV FILE
# --------------------------------------------------

def read_csv_file():

    records = []

    with open(
        CSV_INPUT,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            records.append(row)

    print("\nCSV records read:", len(records))

    return records


# --------------------------------------------------
# 6. READ EXCEL FILE
# --------------------------------------------------

def read_excel_file():

    workbook = load_workbook(
        EXCEL_INPUT,
        read_only=True,
        data_only=True
    )

    worksheet = workbook["Employees"]

    rows = worksheet.iter_rows(values_only=True)

    headers = next(rows)

    records = []

    for row in rows:

        record = dict(zip(headers, row))

        records.append(record)

    workbook.close()

    print("\nExcel records read:", len(records))

    return records


# --------------------------------------------------
# 7. IMPORT RECORDS INTO MYSQL
# --------------------------------------------------

def import_records(cursor, connection, records, source_name):

    valid_records = validate_records(records)

    if not valid_records:

        print("No valid records to import:", source_name)

        return

    query = """
        INSERT INTO imported_employees
        (name, email, department, salary, source_file)

        VALUES (%s, %s, %s, %s, %s)

        ON DUPLICATE KEY UPDATE

        name = VALUES(name),
        department = VALUES(department),
        salary = VALUES(salary),
        source_file = VALUES(source_file)
    """

    data = [
        (*record, source_name)
        for record in valid_records
    ]

    try:

        cursor.executemany(query, data)

        connection.commit()

        print(f"\n{source_name} import completed!")

        print("Valid records:", len(valid_records))

        print("Affected rows:", cursor.rowcount)

    except Error as error:

        connection.rollback()

        print("Import error:", error)


# --------------------------------------------------
# 8. FETCH MYSQL RECORDS
# --------------------------------------------------

def fetch_database_data(cursor):

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            department,
            salary,
            source_file,
            imported_at

        FROM imported_employees

        ORDER BY id
    """)

    records = cursor.fetchall()

    print("\nDatabase records fetched:", len(records))

    return records


# --------------------------------------------------
# 9. EXPORT MYSQL DATA TO CSV
# --------------------------------------------------

def export_csv(records):

    columns = [
        "id",
        "name",
        "email",
        "department",
        "salary",
        "source_file",
        "imported_at"
    ]

    with open(
        CSV_OUTPUT,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=columns
        )

        writer.writeheader()

        for record in records:

            output_record = record.copy()

            output_record["salary"] = str(
                output_record["salary"]
            )

            output_record["imported_at"] = str(
                output_record["imported_at"]
            )

            writer.writerow(output_record)

    print("\nCSV export completed!")
    print("File:", CSV_OUTPUT)


# --------------------------------------------------
# 10. EXPORT MYSQL DATA TO MULTIPLE EXCEL SHEETS
# --------------------------------------------------

def export_excel(records):

    workbook = Workbook()

    # Sheet 1: All Employees
    all_sheet = workbook.active

    all_sheet.title = "All Employees"

    headers = [
        "ID",
        "Name",
        "Email",
        "Department",
        "Salary",
        "Source File",
        "Imported At"
    ]

    all_sheet.append(headers)

    for record in records:

        all_sheet.append([
            record["id"],
            record["name"],
            record["email"],
            record["department"],
            float(record["salary"]),
            record["source_file"],
            record["imported_at"]
        ])

    # Sheet 2: Department Summary
    summary_sheet = workbook.create_sheet(
        "Department Summary"
    )

    summary_sheet.append([
        "Department",
        "Total Employees",
        "Average Salary",
        "Total Salary"
    ])

    summary = {}

    for record in records:

        department = record["department"] or "Unassigned"

        salary = float(record["salary"])

        if department not in summary:

            summary[department] = {
                "count": 0,
                "total": 0
            }

        summary[department]["count"] += 1

        summary[department]["total"] += salary

    for department, values in summary.items():

        count = values["count"]

        total = values["total"]

        average = total / count

        summary_sheet.append([
            department,
            count,
            average,
            total
        ])

    # Sheet 3: CSV Imports
    csv_sheet = workbook.create_sheet("CSV Imports")

    csv_sheet.append(headers)

    for record in records:

        if record["source_file"] == "CSV":

            csv_sheet.append([
                record["id"],
                record["name"],
                record["email"],
                record["department"],
                float(record["salary"]),
                record["source_file"],
                record["imported_at"]
            ])

    # Sheet 4: Excel Imports
    excel_sheet = workbook.create_sheet("Excel Imports")

    excel_sheet.append(headers)

    for record in records:

        if record["source_file"] == "Excel":

            excel_sheet.append([
                record["id"],
                record["name"],
                record["email"],
                record["department"],
                float(record["salary"]),
                record["source_file"],
                record["imported_at"]
            ])

    workbook.save(EXCEL_OUTPUT)

    print("\nExcel report generated!")

    print("Worksheets:")
    print(workbook.sheetnames)

    print("File:", EXCEL_OUTPUT)


# --------------------------------------------------
# 11. MAIN EXECUTION
# --------------------------------------------------

def run_automation():

    connection = None
    cursor = None

    try:

        create_sample_files()

        connection = get_database_connection()

        if connection is None:
            return

        cursor = connection.cursor(dictionary=True)

        print("\nMySQL connected!")

        setup_table(cursor, connection)

        # CSV to MySQL
        csv_records = read_csv_file()

        import_records(
            cursor,
            connection,
            csv_records,
            "CSV"
        )

        # Excel to MySQL
        excel_records = read_excel_file()

        import_records(
            cursor,
            connection,
            excel_records,
            "Excel"
        )

        # MySQL to CSV and Excel
        database_records = fetch_database_data(cursor)

        export_csv(database_records)

        export_excel(database_records)

        print("\nCSV and Excel automation completed!")

    except Error as error:

        if connection is not None and connection.is_connected():
            connection.rollback()

        print("MySQL Error:", error)

    except Exception as error:

        print("Automation Error:", error)

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

        print("Database connection closed!")


if __name__ == "__main__":
    run_automation()
