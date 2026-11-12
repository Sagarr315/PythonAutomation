import csv
import pdfplumber

from openpyxl import Workbook

from .config import SAMPLE_PDF, OUTPUT_DIR


def extract_pdf_tables(file_path):
    all_tables = []

    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()

            for table in tables:
                print(f"\nTable found on page {page_number}")
                for row in table:
                    print(row)
                all_tables.extend(table)

    return all_tables


def export_to_csv(rows, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print("CSV exported:", output_file.name)


def export_to_excel(rows, output_file):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Extracted_Table"

    for row in rows:
        sheet.append(row)

    workbook.save(output_file)
    workbook.close()

    print("Excel exported:", output_file.name)


if __name__ == "__main__":
    extracted_rows = extract_pdf_tables(SAMPLE_PDF)

    if extracted_rows:
        export_to_csv(
            extracted_rows,
            OUTPUT_DIR / "PDF_Table.csv",
        )
        export_to_excel(
            extracted_rows,
            OUTPUT_DIR / "PDF_Table.xlsx",
        )
    else:
        print("No tables found.")