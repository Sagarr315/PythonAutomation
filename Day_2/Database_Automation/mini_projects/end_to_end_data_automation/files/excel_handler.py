
import logging

from decimal import Decimal, InvalidOperation
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

from Database_Automation.mini_projects.end_to_end_data_automation.config import (
    OUTPUT_DIR
)


logger = logging.getLogger(__name__)

INPUT_DIR = OUTPUT_DIR / "excel_input"
EXPORT_DIR = OUTPUT_DIR / "excel_output"

INPUT_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILE = INPUT_DIR / "employees.xlsx"
OUTPUT_FILE = EXPORT_DIR / "employees_report.xlsx"

HEADERS = [
    "Name",
    "Email",
    "Department",
    "Salary"
]


# --------------------------------------------------
# 1. APPLY WORKSHEET FORMATTING
# --------------------------------------------------

def format_worksheet(worksheet):

    header_fill = PatternFill(
        fill_type="solid",
        fgColor="1F4E78"
    )

    header_font = Font(
        bold=True,
        color="FFFFFF"
    )

    for cell in worksheet[1]:

        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(
            horizontal="center"
        )

    worksheet.freeze_panes = "A2"

    worksheet.auto_filter.ref = worksheet.dimensions

    for column_cells in worksheet.columns:

        max_length = 0

        column_letter = get_column_letter(
            column_cells[0].column
        )

        for cell in column_cells:

            value = cell.value

            if value is not None:
                max_length = max(
                    max_length,
                    len(str(value))
                )

        worksheet.column_dimensions[
            column_letter
        ].width = min(max_length + 4, 45)


# --------------------------------------------------
# 2. CREATE SAMPLE EXCEL INPUT
# --------------------------------------------------

def create_sample_excel():

    records = [
        [
            "John Smith",
            "john@example.com",
            "IT",
            55000
        ],
        [
            "Alice Johnson",
            "alice@example.com",
            "HR",
            45000
        ],
        [
            "Robert Brown",
            "robert@example.com",
            "Finance",
            60000
        ],
        [
            "David Wilson",
            "david@example.com",
            "IT",
            65000
        ],
        [
            "John Duplicate",
            "john@example.com",
            "IT",
            55000
        ],
        [
            "Invalid Employee",
            "invalid-email",
            "IT",
            50000
        ]
    ]

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Employee Data"

    worksheet.append(HEADERS)

    for record in records:
        worksheet.append(record)

    format_worksheet(worksheet)

    workbook.save(INPUT_FILE)

    print("Sample Excel created:", INPUT_FILE)

    logger.info("Sample Excel input created")


# --------------------------------------------------
# 3. VALIDATE ONE EXCEL RECORD
# --------------------------------------------------

def validate_excel_record(record):

    name = str(record.get("Name") or "").strip()

    email = str(record.get("Email") or "").strip()

    department = str(
        record.get("Department") or ""
    ).strip()

    salary_value = record.get("Salary")

    if not name or not email or not department:
        return None

    if "@" not in email:
        return None

    try:

        salary = Decimal(str(salary_value))

        if not salary.is_finite() or salary < 0:
            return None

    except (InvalidOperation, ValueError, TypeError):
        return None

    return {
        "name": name,
        "email": email.lower(),
        "department": department,
        "salary": salary
    }


# --------------------------------------------------
# 4. READ AND VALIDATE EXCEL DATA
# --------------------------------------------------

def read_excel_records():

    workbook = load_workbook(
        INPUT_FILE,
        read_only=True,
        data_only=True
    )

    try:

        if "Employee Data" not in workbook.sheetnames:
            raise ValueError("Employee Data worksheet not found.")

        worksheet = workbook["Employee Data"]

        rows = worksheet.iter_rows(
            values_only=True
        )

        headers = next(rows, None)

        if headers is None:
            raise ValueError("Excel worksheet is empty.")

        if not set(HEADERS).issubset(set(headers)):
            raise ValueError("Required Excel columns are missing.")

        header_indexes = {
            header: index
            for index, header in enumerate(headers)
        }

        valid_records = []

        seen_emails = set()

        for row in rows:

            record = {
                header: row[header_indexes[header]]
                if header_indexes[header] < len(row)
                else None
                for header in HEADERS
            }

            cleaned = validate_excel_record(record)

            if cleaned is None:

                logger.warning("Invalid Excel row skipped.")

                continue

            email = cleaned["email"]

            if email in seen_emails:

                logger.warning(
                    "Duplicate Excel email skipped: %s",
                    email
                )

                continue

            seen_emails.add(email)

            valid_records.append(cleaned)

        print("\nExcel reading completed!")

        print("Valid unique records:", len(valid_records))

        return valid_records

    finally:

        workbook.close()


# --------------------------------------------------
# 5. CREATE EMPLOYEE WORKSHEET
# --------------------------------------------------

def create_employee_sheet(workbook, records):

    worksheet = workbook.active

    worksheet.title = "Employees"

    worksheet.append(HEADERS)

    for record in records:

        worksheet.append([
            record["name"],
            record["email"],
            record["department"],
            float(record["salary"])
        ])

    for row in worksheet.iter_rows(
        min_row=2,
        min_col=4,
        max_col=4
    ):

        row[0].number_format = '#,##0.00'

    format_worksheet(worksheet)

    return worksheet


# --------------------------------------------------
# 6. CREATE DEPARTMENT SUMMARY WORKSHEET
# --------------------------------------------------

def create_department_summary(workbook, records):

    worksheet = workbook.create_sheet(
        "Department Summary"
    )

    worksheet.append([
        "Department",
        "Employee Count",
        "Total Salary",
        "Average Salary"
    ])

    departments = {}

    for record in records:

        department = record["department"]

        salary = record["salary"]

        if department not in departments:

            departments[department] = {
                "count": 0,
                "total": Decimal("0")
            }

        departments[department]["count"] += 1

        departments[department]["total"] += salary

    for department, details in sorted(departments.items()):

        count = details["count"]

        total = details["total"]

        average = total / count

        worksheet.append([
            department,
            count,
            float(total),
            float(average)
        ])

    for row in worksheet.iter_rows(
        min_row=2,
        min_col=3,
        max_col=4
    ):

        for cell in row:
            cell.number_format = '#,##0.00'

    format_worksheet(worksheet)

    return worksheet


# --------------------------------------------------
# 7. CREATE IMPORT SUMMARY WORKSHEET
# --------------------------------------------------

def create_import_summary(workbook, records):

    worksheet = workbook.create_sheet(
        "Import Summary"
    )

    worksheet.append([
        "Metric",
        "Value"
    ])

    total_employees = len(records)

    total_salary = sum(
        (record["salary"] for record in records),
        Decimal("0")
    )

    worksheet.append([
        "Total Valid Employees",
        total_employees
    ])

    worksheet.append([
        "Total Salary",
        float(total_salary)
    ])

    worksheet.append([
        "Average Salary",
        float(total_salary / total_employees)
        if total_employees else 0
    ])

    worksheet.append([
        "Unique Departments",
        len({
            record["department"]
            for record in records
        })
    ])

    worksheet["B3"].number_format = '#,##0.00'

    worksheet["B4"].number_format = '#,##0.00'

    format_worksheet(worksheet)

    return worksheet


# --------------------------------------------------
# 8. EXPORT PROFESSIONAL EXCEL REPORT
# --------------------------------------------------

def export_excel_report(records):

    workbook = Workbook()

    create_employee_sheet(
        workbook,
        records
    )

    create_department_summary(
        workbook,
        records
    )

    create_import_summary(
        workbook,
        records
    )

    workbook.save(OUTPUT_FILE)

    print("\nExcel report generated successfully!")

    print("Worksheets:", workbook.sheetnames)

    print("Export location:", OUTPUT_FILE)

    logger.info(
        "Excel report generated with %s records",
        len(records)
    )


# --------------------------------------------------
# 9. DISPLAY EXCEL RECORDS
# --------------------------------------------------

def display_records(records):

    print("\n--- CLEANED EXCEL RECORDS ---")

    for record in records:

        print(
            f"Name: {record['name']} | "
            f"Email: {record['email']} | "
            f"Department: {record['department']} | "
            f"Salary: {record['salary']}"
        )


# --------------------------------------------------
# 10. MAIN EXECUTION
# --------------------------------------------------

def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s"
    )

    print("Starting Excel automation...")

    try:

        create_sample_excel()

        records = read_excel_records()

        display_records(records)

        export_excel_report(records)

        print("\nExcel automation completed successfully!")

    except (OSError, ValueError) as error:

        print("Excel automation error:", error)

        logger.exception("Excel automation failed")


if __name__ == "__main__":
    main()
