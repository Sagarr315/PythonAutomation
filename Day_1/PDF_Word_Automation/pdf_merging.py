
from pypdf import PdfWriter

from .config import SAMPLE_PDF, SAMPLE_FORM, OUTPUT_DIR


def merge_pdfs(file_paths, output_file):
    writer = PdfWriter()

    try:
        for file_path in file_paths:
            writer.append(str(file_path))

        with open(output_file, "wb") as file:
            writer.write(file)

        print("Merged PDF:", output_file.name)

    finally:
        writer.close()


if __name__ == "__main__":
    merge_pdfs(
        [SAMPLE_PDF, SAMPLE_FORM],
        OUTPUT_DIR / "Merged_Report.pdf",
    )
