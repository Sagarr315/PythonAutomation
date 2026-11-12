import csv

from openpyxl import Workbook

from .config import (
    EMPLOYEE_CSV,
    EMPLOYEE_EXCEL,
    INPUT_DIR,
    SALES_EXCEL,
)


def create_employee_excel():

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Employees"

    sheet.append(["Employee_ID", "Name", "Department", "Salary"])

    sheet.append(["E001", "Employee_001", "IT", 45000])
    sheet.append(["E002", "Employee_002", "HR", 35000])
    sheet.append(["E003", "Employee_003", "IT", 50000])
    sheet.append(["E004", "Employee_004", "Finance", 40000])
    sheet.append(["E005", "Employee_005", "HR", 38000])

    workbook.save(EMPLOYEE_EXCEL)

    print("Created:", EMPLOYEE_EXCEL.name)


def create_sales_excel():

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Sales"

    sheet.append(["Order_ID", "Product", "Quantity", "Amount"])

    sheet.append(["O001", "Laptop", 2, 100000])
    sheet.append(["O002", "Mouse", 5, 2500])
    sheet.append(["O003", "Keyboard", 3, 4500])
    sheet.append(["O004", "Monitor", 2, 30000])

    workbook.save(SALES_EXCEL)

    print("Created:", SALES_EXCEL.name)


def create_employee_csv():

    records = [
        ["Employee_ID", "Name", "Department", "Salary"],
        ["E001", "Employee_001", "IT", 45000],
        ["E002", "Employee_002", "HR", 35000],
        ["E003", "Employee_003", "IT", 50000],
    ]

    with open(
        EMPLOYEE_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)
        writer.writerows(records)

    print("Created:", EMPLOYEE_CSV.name)


def main():

    create_employee_excel()
    create_sales_excel()
    create_employee_csv()

    print("\nSample data creation completed!")


if __name__ == "__main__":
    main()
