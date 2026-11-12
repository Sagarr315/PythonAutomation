from openpyxl import load_workbook

from .config import EMPLOYEE_EXCEL, INPUT_DIR


# 1. Read complete worksheet
def read_complete_worksheet(file_path, sheet_name):

    workbook = load_workbook(file_path, data_only=False)

    if sheet_name not in workbook.sheetnames:
        print("Worksheet not found:", sheet_name)
        workbook.close()
        return

    sheet = workbook[sheet_name]

    for row in sheet.iter_rows(values_only=True):
        print(row)

    workbook.close()


# 2. Read a specific cell
def read_specific_cell(file_path, sheet_name, cell_address):

    workbook = load_workbook(file_path)
    sheet = workbook[sheet_name]

    value = sheet[cell_address].value

    print("Cell:", cell_address)
    print("Value:", value)

    workbook.close()


# 3. Read a specific row
def read_specific_row(file_path, sheet_name, row_number):

    workbook = load_workbook(file_path)
    sheet = workbook[sheet_name]

    values = [
        cell.value
        for cell in sheet[row_number]
    ]

    print("Row data:", values)

    workbook.close()


# 4. Read a specific column
def read_specific_column(file_path, sheet_name, column_number):

    workbook = load_workbook(file_path)
    sheet = workbook[sheet_name]

    values = [
        sheet.cell(row=row_number, column=column_number).value
        for row_number in range(1, sheet.max_row + 1)
    ]

    print("Column data:", values)

    workbook.close()


# 5. List worksheets
def list_worksheets(file_path):

    workbook = load_workbook(file_path)

    print("Worksheets:")

    for sheet_name in workbook.sheetnames:
        print(sheet_name)

    workbook.close()


# 6. Read all Excel files in a folder
def read_multiple_excel_files(folder_path):

    for file_path in folder_path.glob("*.xlsx"):

        if file_path.name.startswith("~$"):
            continue

        print("\nFile:", file_path.name)

        workbook = load_workbook(file_path, read_only=True)

        for sheet in workbook.worksheets:

            print("Worksheet:", sheet.title)

            for row in sheet.iter_rows(values_only=True):
                print(row)

        workbook.close()


# Individual execution
if __name__ == "__main__":

    print("\n--- Complete Worksheet ---")
    read_complete_worksheet(EMPLOYEE_EXCEL, "Employees")

    print("\n--- Specific Cell ---")
    read_specific_cell(EMPLOYEE_EXCEL, "Employees", "B2")

    print("\n--- Specific Row ---")
    read_specific_row(EMPLOYEE_EXCEL, "Employees", 2)

    print("\n--- Specific Column ---")
    read_specific_column(EMPLOYEE_EXCEL, "Employees", 2)

    print("\n--- Worksheets ---")
    list_worksheets(EMPLOYEE_EXCEL)

    print("\nExcel reading completed!")
