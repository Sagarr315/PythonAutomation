from openpyxl import Workbook, load_workbook

from .config import OUTPUT_DIR


# 1. Create a new Excel workbook
def create_excel_file(file_path, sheet_name="Sheet1"):

    workbook = Workbook()
    workbook.active.title = sheet_name

    workbook.save(file_path)
    workbook.close()

    print("Excel file created:", file_path.name)


# 2. Write data into a worksheet
def write_excel_data(file_path, sheet_name, data):

    workbook = load_workbook(file_path)

    if sheet_name not in workbook.sheetnames:
        workbook.close()
        raise ValueError(f"Worksheet not found: {sheet_name}")

    sheet = workbook[sheet_name]

    for row in data:
        sheet.append(row)

    workbook.save(file_path)
    workbook.close()

    print("Excel data written successfully.")


# 3. Update a specific cell
def update_excel_cell(file_path, sheet_name, cell, value):

    workbook = load_workbook(file_path)
    sheet = workbook[sheet_name]

    sheet[cell] = value

    workbook.save(file_path)
    workbook.close()

    print("Cell updated:", cell)


# 4. Append a new row
def append_excel_row(file_path, sheet_name, row_data):

    workbook = load_workbook(file_path)
    sheet = workbook[sheet_name]

    sheet.append(row_data)

    workbook.save(file_path)
    workbook.close()

    print("New row appended.")


# 5. Main execution
if __name__ == "__main__":

    output_file = OUTPUT_DIR / "New_Employees.xlsx"

    create_excel_file(output_file, "Employees")

    write_excel_data(
        output_file,
        "Employees",
        [
            ["Employee_ID", "Name", "Department", "Salary"],
            ["E101", "Employee_101", "IT", 55000],
            ["E102", "Employee_102", "Finance", 48000],
        ]
    )

    update_excel_cell(
        output_file,
        "Employees",
        "D2",
        60000
    )

    append_excel_row(
        output_file,
        "Employees",
        ["E103", "Employee_103", "HR", 42000]
    )

    print("\nExcel writing completed!")
