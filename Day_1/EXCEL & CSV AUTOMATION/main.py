from .sample_data import main as create_sample_data

from .excel_reading import (
    read_complete_worksheet,
    read_specific_cell,
    list_worksheets,
)

from .excel_writing import (
    create_excel_file,
    write_excel_data,
    append_excel_row,
)

from .worksheet_management import (
    add_worksheet,
    rename_worksheet,
)

from .excel_processing import (
    read_excel_data,
    filter_records,
    sort_records,
)

from .csv_automation import (
    read_csv_file,
    csv_to_excel,
    excel_to_csv,
)

from .excel_report import generate_excel_report

from .config import (
    EMPLOYEE_EXCEL,
    EMPLOYEE_CSV,
    OUTPUT_DIR,
)


def display_menu():

    print("\n====================================")
    print("      EXCEL & CSV AUTOMATION")
    print("====================================")

    print("1. Create Sample Excel and CSV Files")
    print("2. Read Complete Excel Worksheet")
    print("3. Read Specific Excel Cell")
    print("4. List Excel Worksheets")
    print("5. Create New Excel File")
    print("6. Write Excel Data")
    print("7. Append Excel Row")
    print("8. Add Excel Worksheet")
    print("9. Rename Excel Worksheet")
    print("10. Filter Excel Records")
    print("11. Sort Excel Records")
    print("12. Read CSV File")
    print("13. Convert CSV to Excel")
    print("14. Convert Excel to CSV")
    print("15. Generate Formatted Excel Report")
    print("0. Exit")

    print("====================================")


def main():

    while True:

        display_menu()

        choice = input("Enter your choice: ").strip()

        try:

            if choice == "1":

                create_sample_data()

            elif choice == "2":

                read_complete_worksheet(
                    EMPLOYEE_EXCEL,
                    "Employees"
                )

            elif choice == "3":

                read_specific_cell(
                    EMPLOYEE_EXCEL,
                    "Employees",
                    "B2"
                )

            elif choice == "4":

                list_worksheets(EMPLOYEE_EXCEL)

            elif choice == "5":

                create_excel_file(
                    OUTPUT_DIR / "New_Workbook.xlsx"
                )

            elif choice == "6":

                write_excel_data(
                    OUTPUT_DIR / "New_Workbook.xlsx",
                    "Sheet1",
                    [["E101", "Employee_101", "IT"]]
                )

            elif choice == "7":

                append_excel_row(
                    EMPLOYEE_EXCEL,
                    "Employees",
                    ["E006", "Employee_006", "IT", 47000]
                )

            elif choice == "8":

                add_worksheet(
                    EMPLOYEE_EXCEL,
                    "New_Sheet"
                )

            elif choice == "9":

                rename_worksheet(
                    EMPLOYEE_EXCEL,
                    "New_Sheet",
                    "Updated_Sheet"
                )

            elif choice == "10":

                filter_records(
                    EMPLOYEE_EXCEL,
                    "IT"
                )

            elif choice == "11":

                sort_records(
                    EMPLOYEE_EXCEL,
                    "Salary"
                )

            elif choice == "12":

                read_csv_file(EMPLOYEE_CSV)

            elif choice == "13":

                csv_to_excel(
                    EMPLOYEE_CSV,
                    OUTPUT_DIR / "Converted_From_CSV.xlsx"
                )

            elif choice == "14":

                excel_to_csv(
                    EMPLOYEE_EXCEL,
                    OUTPUT_DIR / "Converted_From_Excel.csv"
                )

            elif choice == "15":

                generate_excel_report(
                    EMPLOYEE_EXCEL,
                    OUTPUT_DIR / "Formatted_Report.xlsx"
                )

            elif choice == "0":

                print("Automation application closed.")
                break

            else:

                print("Invalid choice. Please try again.")

        except (OSError, ValueError, KeyError) as error:

            print("Operation failed:", error)

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
