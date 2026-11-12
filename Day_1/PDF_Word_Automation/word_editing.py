from docx import Document
from docx.shared import Pt, RGBColor

from .config import SAMPLE_WORD, OUTPUT_DIR


def edit_word_document(input_file, output_file):
    document = Document(input_file)

    document.add_heading("Automation Results", level=2)

    paragraph = document.add_paragraph(
        "This section was added automatically using Python."
    )

    for run in paragraph.runs:
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 128)

    document.add_paragraph(
        "Document processing completed successfully."
    )

    document.save(output_file)
    print("Word document updated:", output_file.name)


if __name__ == "__main__":
    edit_word_document(
        SAMPLE_WORD,
        OUTPUT_DIR / "Updated_Report.docx",
    )