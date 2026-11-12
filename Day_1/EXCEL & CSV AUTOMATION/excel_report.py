from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

from .config import EMPLOYEE_EXCEL, OUTPUT_DIR


def generate_excel_report(input_file, output_file):

    workbook = load_workbook(input_file)

    sheet = workbook.active

    # Format header row
    for cell in sheet[1]:

        cell.font = Font(
            bold=True,
            color="FFFFFF"
        )

        cell.fill = PatternFill(
            fill_type="solid",
            fgColor="1F4E78"
        )

        cell.alignment = Alignment(
            horizontal="center"
        )

    # Adjust column widths
    for column in sheet.columns:

        max_length = max(
            len(str(cell.value or ""))
            for cell in column
        )

        column_letter = get_column_letter(
            column[0].column
        )

        sheet.column_dimensions[
            column_letter
        ].width = max_length + 4

    # Freeze header row
    sheet.freeze_panes = "A2"

    # Add autofilter
    sheet.auto_filter.ref = sheet.dimensions

    workbook.save(output_file)
    workbook.close()

    print("Formatted Excel report generated:", output_file.name)


if __name__ == "__main__":

    generate_excel_report(
        EMPLOYEE_EXCEL,
        OUTPUT_DIR / "Employee_Report.xlsx"
    )

    print("\nReport generation completed!")
