
import csv
import logging

from decimal import Decimal, InvalidOperation

from Database_Automation.mini_projects.end_to_end_data_automation.config import (
    OUTPUT_DIR
)


logger = logging.getLogger(__name__)

INPUT_DIR = OUTPUT_DIR / "csv_input"
EXPORT_DIR = OUTPUT_DIR / "csv_output"

INPUT_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILE = INPUT_DIR / "employees.csv"
OUTPUT_FILE = EXPORT_DIR / "employees_cleaned.csv"

CSV_FIELDS = [
    "name",
    "email",
    "department",
    "salary"
]


# --------------------------------------------------
# 1. CREATE SAMPLE CSV FILE
# --------------------------------------------------

def create_sample_csv():

    sample_records = [
        {
            "name": "John Smith",
            "email": "john@example.com",
            "department": "IT",
            "salary": "55000"
        },
        {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "department": "HR",
            "salary": "45000"
        },
        {
            "name": "Robert Brown",
            "email": "robert@example.com",
            "department": "Finance",
            "salary": "60000"
        },
        {
            "name": "John Smith Duplicate",
            "email": "john@example.com",
            "department": "IT",
            "salary": "55000"
        },
        {
            "name": "Invalid Employee",
            "email": "invalid-email",
            "department": "IT",
            "salary": "50000"
        }
    ]

    with open(
        INPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=CSV_FIELDS
        )

        writer.writeheader()

        writer.writerows(sample_records)

    print("Sample CSV file created:", INPUT_FILE)

    logger.info("Sample CSV created")


# --------------------------------------------------
# 2. VALIDATE ONE CSV RECORD
# --------------------------------------------------

def validate_csv_record(record):

    name = (record.get("name") or "").strip()

    email = (record.get("email") or "").strip()

    department = (record.get("department") or "").strip()

    salary_text = (record.get("salary") or "").strip()

    if not name or not email or not department:
        return None

    if "@" not in email:
        return None

    try:

        salary = Decimal(salary_text)

        if not salary.is_finite() or salary < 0:
            return None

    except (InvalidOperation, ValueError):
        return None

    return {
        "name": name,
        "email": email.lower(),
        "department": department,
        "salary": salary
    }


# --------------------------------------------------
# 3. READ AND VALIDATE CSV
# --------------------------------------------------

def read_csv_records():

    valid_records = []

    seen_emails = set()

    with open(
        INPUT_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames or not set(CSV_FIELDS).issubset(
            set(reader.fieldnames)
        ):
            raise ValueError("CSV file is missing required columns.")

        for row in reader:

            cleaned_record = validate_csv_record(row)

            if cleaned_record is None:

                logger.warning("Invalid CSV record skipped.")

                continue

            email = cleaned_record["email"]

            if email in seen_emails:

                logger.warning(
                    "Duplicate email skipped: %s",
                    email
                )

                continue

            seen_emails.add(email)

            valid_records.append(cleaned_record)

    print("\nCSV reading completed!")

    print("Valid unique records:", len(valid_records))

    return valid_records


# --------------------------------------------------
# 4. EXPORT CLEANED DATA TO CSV
# --------------------------------------------------

def export_csv_records(records):

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=CSV_FIELDS
        )

        writer.writeheader()

        for record in records:

            export_record = {
                "name": record["name"],
                "email": record["email"],
                "department": record["department"],
                "salary": str(record["salary"])
            }

            writer.writerow(export_record)

    print("\nCleaned CSV exported successfully!")

    print("Export location:", OUTPUT_FILE)

    logger.info(
        "Exported %s CSV records",
        len(records)
    )


# --------------------------------------------------
# 5. DISPLAY RECORDS
# --------------------------------------------------

def display_records(records):

    print("\n--- CLEANED CSV RECORDS ---")

    for record in records:

        print(
            f"Name: {record['name']} | "
            f"Email: {record['email']} | "
            f"Department: {record['department']} | "
            f"Salary: {record['salary']}"
        )


# --------------------------------------------------
# 6. MAIN EXECUTION
# --------------------------------------------------

def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s"
    )

    print("Starting CSV automation...")

    try:

        create_sample_csv()

        records = read_csv_records()

        display_records(records)

        export_csv_records(records)

        print("\nCSV automation completed successfully!")

    except (OSError, ValueError) as error:

        print("CSV automation error:", error)

        logger.exception("CSV automation failed")


if __name__ == "__main__":
    main()
