from docx import Document

from .config import OUTPUT_DIR


def create_word_document(output_file):
    document = Document()

    document.add_heading("Business Automation Report", level=1)

    document.add_paragraph(
        "This document was generated using Python."
    )

    document.add_heading("Employee Details", level=2)

    table = document.add_table(rows=1, cols=3)
    table.style = "Table Grid"

    headers = ["Employee ID", "Name", "Department"]

    for index, value in enumerate(headers):
        table.rows[0].cells[index].text = value

    records = [
        ["E001", "Employee_001", "IT"],
        ["E002", "Employee_002", "HR"],
    ]

    for record in records:
        cells = table.add_row().cells

        for index, value in enumerate(record):
            cells[index].text = value

    document.save(output_file)
    print("Word document created:", output_file.name)


if __name__ == "__main__":
    create_word_document(
        OUTPUT_DIR / "Generated_Report.docx"
    )