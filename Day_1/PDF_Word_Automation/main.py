from .sample_data import main as create_sample_data

from .pdf_reading import read_pdf_text, read_specific_page, count_pdf_pages
from .pdf_creation import create_pdf_report
from .pdf_merging import merge_pdfs
from .pdf_splitting import split_pdf
from .pdf_metadata import read_pdf_metadata
from .pdf_table_extraction import extract_pdf_tables, export_to_csv, export_to_excel
from .pdf_images import convert_pdf_pages_to_images, extract_embedded_images
from .pdf_forms import read_form_fields, fill_pdf_form

from .word_creation import create_word_document
from .word_reading import read_word_document
from .word_editing import edit_word_document

from .config import (
    SAMPLE_PDF,
    SAMPLE_FORM,
    SAMPLE_WORD,
    OUTPUT_DIR,
)


def display_menu():
    print("\n========================================")
    print("       PDF & WORD AUTOMATION")
    print("========================================")
    print("1. Create Sample PDF, Form and Word Files")
    print("2. Read PDF Text")
    print("3. Read Specific PDF Page")
    print("4. Count PDF Pages")
    print("5. Create PDF Report")
    print("6. Merge PDFs")
    print("7. Split PDF into Individual Pages")
    print("8. Read PDF Metadata")
    print("9. Extract PDF Tables to CSV and Excel")
    print("10. Convert PDF Pages to Images")
    print("11. Extract Embedded PDF Images")
    print("12. Read PDF Form Fields")
    print("13. Fill PDF Form")
    print("14. Create Word Document")
    print("15. Read Word Document")
    print("16. Edit Word Document")
    print("0. Exit")
    print("========================================")


def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                create_sample_data()

            elif choice == "2":
                read_pdf_text(SAMPLE_PDF)

            elif choice == "3":
                page = int(input("Enter page number: "))
                read_specific_page(SAMPLE_PDF, page)

            elif choice == "4":
                count_pdf_pages(SAMPLE_PDF)

            elif choice == "5":
                create_pdf_report(
                    OUTPUT_DIR / "Generated_Report.pdf"
                )

            elif choice == "6":
                merge_pdfs(
                    [SAMPLE_PDF, SAMPLE_FORM],
                    OUTPUT_DIR / "Merged_Report.pdf",
                )

            elif choice == "7":
                split_pdf(SAMPLE_PDF, OUTPUT_DIR)

            elif choice == "8":
                read_pdf_metadata(SAMPLE_PDF)

            elif choice == "9":
                rows = extract_pdf_tables(SAMPLE_PDF)

                if rows:
                    export_to_csv(
                        rows,
                        OUTPUT_DIR / "PDF_Table.csv",
                    )
                    export_to_excel(
                        rows,
                        OUTPUT_DIR / "PDF_Table.xlsx",
                    )
                else:
                    print("No tables found.")

            elif choice == "10":
                convert_pdf_pages_to_images(SAMPLE_PDF)

            elif choice == "11":
                extract_embedded_images(SAMPLE_PDF)

            elif choice == "12":
                read_form_fields(SAMPLE_FORM)

            elif choice == "13":
                fill_pdf_form(
                    SAMPLE_FORM,
                    OUTPUT_DIR / "Filled_Form.pdf",
                    {
                        "employee_name": "Employee_101",
                        "department": "IT",
                        "employee_id": "E101",
                    },
                )

            elif choice == "14":
                create_word_document(
                    OUTPUT_DIR / "Generated_Report.docx"
                )

            elif choice == "15":
                read_word_document(SAMPLE_WORD)

            elif choice == "16":
                edit_word_document(
                    SAMPLE_WORD,
                    OUTPUT_DIR / "Updated_Report.docx",
                )

            elif choice == "0":
                print("PDF & Word automation application closed.")
                break

            else:
                print("Invalid choice. Please try again.")

        except (OSError, ValueError, KeyError, IndexError) as error:
            print("Operation failed:", error)

        except Exception as error:
            print("Unexpected error:", error)

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()