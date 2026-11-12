
import csv

import pandas as pd

from .config import EMPLOYEE_CSV, EMPLOYEE_EXCEL, OUTPUT_DIR


# 1. Read CSV using Python csv module
def read_csv_file(file_path):

    with open(
        file_path,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.reader(file)

        for row in reader:
            print(row)


# 2. Write CSV data
def write_csv_file(file_path, headers, records):

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(headers)
        writer.writerows(records)

    print("CSV file created:", file_path.name)


# 3. Append CSV data
def append_csv_record(file_path, record):

    with open(
        file_path,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)
        writer.writerow(record)

    print("CSV record appended.")


# 4. Filter CSV records using pandas
def filter_csv_records(file_path, department):

    dataframe = pd.read_csv(file_path)

    filtered_data = dataframe[
        dataframe["Department"] == department
    ]

    print(filtered_data)

    return filtered_data


# 5. Convert CSV to Excel
def csv_to_excel(csv_path, excel_path):

    dataframe = pd.read_csv(csv_path)

    dataframe.to_excel(
        excel_path,
        index=False
    )

    print("CSV converted to Excel:", excel_path.name)


# 6. Convert Excel to CSV
def excel_to_csv(excel_path, csv_path, sheet_name=0):

    dataframe = pd.read_excel(
        excel_path,
        sheet_name=sheet_name
    )

    dataframe.to_csv(
        csv_path,
        index=False
    )

    print("Excel converted to CSV:", csv_path.name)


# 7. Merge multiple CSV files
def merge_csv_files(file_paths, output_file):

    dataframes = [
        pd.read_csv(file_path)
        for file_path in file_paths
    ]

    combined_data = pd.concat(
        dataframes,
        ignore_index=True
    )

    combined_data.to_csv(
        output_file,
        index=False
    )

    print("CSV files merged:", output_file.name)


# 8. Main execution
if __name__ == "__main__":

    print("\n--- Read CSV ---")
    read_csv_file(EMPLOYEE_CSV)

    print("\n--- Create CSV ---")
    write_csv_file(
        OUTPUT_DIR / "New_Employees.csv",
        ["Employee_ID", "Name", "Department"],
        [
            ["E101", "Employee_101", "IT"],
            ["E102", "Employee_102", "HR"]
        ]
    )

    print("\n--- Append CSV ---")
    append_csv_record(
        EMPLOYEE_CSV,
        ["E004", "Employee_004", "Finance", 42000]
    )

    print("\n--- Filter CSV ---")
    filter_csv_records(EMPLOYEE_CSV, "IT")

    print("\n--- CSV to Excel ---")
    csv_to_excel(
        EMPLOYEE_CSV,
        OUTPUT_DIR / "CSV_Converted.xlsx"
    )

    print("\n--- Excel to CSV ---")
    excel_to_csv(
        EMPLOYEE_EXCEL,
        OUTPUT_DIR / "Excel_Converted.csv"
    )

    print("\nCSV automation completed!")
