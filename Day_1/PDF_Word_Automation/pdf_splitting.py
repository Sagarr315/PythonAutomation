from pypdf import PdfReader, PdfWriter

from .config import SAMPLE_PDF, OUTPUT_DIR


def split_pdf(file_path, output_folder):
    reader = PdfReader(str(file_path))

    for page_number, page in enumerate(reader.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)

        output_file = output_folder / f"Page_{page_number}.pdf"

        with open(output_file, "wb") as file:
            writer.write(file)

        writer.close()
        print("Created:", output_file.name)


if __name__ == "__main__":
    split_pdf(SAMPLE_PDF, OUTPUT_DIR)