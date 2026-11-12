import pdfplumber

from .config import SAMPLE_PDF


def read_pdf_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            print(f"\n--- Page {page_number} ---")
            print(page.extract_text() or "No extractable text found.")


def read_specific_page(file_path, page_number):
    with pdfplumber.open(file_path) as pdf:
        if page_number < 1 or page_number > len(pdf.pages):
            raise ValueError("Invalid page number.")

        page = pdf.pages[page_number - 1]
        print(page.extract_text() or "No text found.")


def count_pdf_pages(file_path):
    with pdfplumber.open(file_path) as pdf:
        print("Total pages:", len(pdf.pages))


if __name__ == "__main__":
    read_pdf_text(SAMPLE_PDF)
    count_pdf_pages(SAMPLE_PDF)