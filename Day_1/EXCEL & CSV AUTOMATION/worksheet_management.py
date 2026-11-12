from openpyxl import load_workbook

from .config import EMPLOYEE_EXCEL, OUTPUT_DIR


# 1. Add a worksheet
def add_worksheet(file_path, sheet_name):

    workbook = load_workbook(file_path)

    if sheet_name in workbook.sheetnames:
        print("Worksheet already exists.")
        workbook.close()
        return

    workbook.create_sheet(sheet_name)

    workbook.save(file_path)
    workbook.close()

    print("Worksheet added:", sheet_name)


# 2. Rename a worksheet
def rename_worksheet(file_path, old_name, new_name):

    workbook = load_workbook(file_path)

    if old_name not in workbook.sheetnames:
        print("Original worksheet not found.")
        workbook.close()
        return

    if new_name in workbook.sheetnames:
        print("New worksheet name already exists.")
        workbook.close()
        return

    workbook[old_name].title = new_name

    workbook.save(file_path)
    workbook.close()

    print("Worksheet renamed:", new_name)


# 3. Copy a worksheet
def copy_worksheet(file_path, source_name, new_name):

    workbook = load_workbook(file_path)

    if source_name not in workbook.sheetnames:
        print("Source worksheet not found.")
        workbook.close()
        return

    if new_name in workbook.sheetnames:
        print("Destination worksheet already exists.")
        workbook.close()
        return

    copied_sheet = workbook.copy_worksheet(
        workbook[source_name]
    )

    copied_sheet.title = new_name

    workbook.save(file_path)
    workbook.close()

    print("Worksheet copied:", new_name)


# 4. Delete a worksheet
def delete_worksheet(file_path, sheet_name):

    workbook = load_workbook(file_path)

    if sheet_name not in workbook.sheetnames:
        print("Worksheet not found.")
        workbook.close()
        return

    if len(workbook.sheetnames) == 1:
        print("Cannot delete the only worksheet.")
        workbook.close()
        return

    del workbook[sheet_name]

    workbook.save(file_path)
    workbook.close()

    print("Worksheet deleted:", sheet_name)


# 5. Main execution
if __name__ == "__main__":

    test_file = OUTPUT_DIR / "Worksheet_Test.xlsx"

    if not test_file.exists():
        from openpyxl import Workbook

        workbook = Workbook()
        workbook.active.title = "Employees"
        workbook.save(test_file)
        workbook.close()

    add_worksheet(test_file, "Sales")

    rename_worksheet(test_file, "Sales", "Sales_Report")

    copy_worksheet(test_file, "Employees", "Employees_Copy")

    # Uncomment to test deletion:
    # delete_worksheet(test_file, "Employees_Copy")

    print("\nWorksheet operations completed!")
