from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfgen import canvas
from docx import Document

from .config import SAMPLE_PDF, SAMPLE_FORM, SAMPLE_WORD


def create_sample_pdf():
    document = SimpleDocTemplate(str(SAMPLE_PDF), pagesize=A4)
    styles = getSampleStyleSheet()

    content = [
        Paragraph("Employee Sales Report", styles["Title"]),
        Spacer(1, 20),
        Paragraph("Sample employee sales data", styles["Normal"]),
        Spacer(1, 15),
    ]

    data = [
        ["Employee ID", "Name", "Department", "Sales"],
        ["E001", "Employee_001", "IT", "50000"],
        ["E002", "Employee_002", "HR", "35000"],
        ["E003", "Employee_003", "Finance", "45000"],
        ["E004", "Employee_004", "IT", "60000"],
    ]

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    content.append(table)
    document.build(content)
    print("Created:", SAMPLE_PDF.name)


def create_sample_form():
    pdf = canvas.Canvas(str(SAMPLE_FORM), pagesize=A4)
    form = pdf.acroForm

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(100, 780, "Employee Registration Form")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(100, 720, "Employee Name:")
    form.textfield(
        name="employee_name",
        x=220, y=705, width=200, height=25,
        borderStyle="solid",
    )

    pdf.drawString(100, 660, "Department:")
    form.textfield(
        name="department",
        x=220, y=645, width=200, height=25,
        borderStyle="solid",
    )

    pdf.drawString(100, 600, "Employee ID:")
    form.textfield(
        name="employee_id",
        x=220, y=585, width=200, height=25,
        borderStyle="solid",
    )

    pdf.save()
    print("Created:", SAMPLE_FORM.name)


def create_sample_word():
    document = Document()
    document.add_heading("Employee Report", level=1)
    document.add_paragraph(
        "This is a sample Word document created using Python."
    )
    document.add_heading("Employee Details", level=2)

    table = document.add_table(rows=1, cols=3)
    table.style = "Table Grid"

    headers = ["Employee ID", "Name", "Department"]
    for index, header in enumerate(headers):
        table.rows[0].cells[index].text = header

    records = [
        ["E001", "Employee_001", "IT"],
        ["E002", "Employee_002", "HR"],
        ["E003", "Employee_003", "Finance"],
    ]

    for record in records:
        cells = table.add_row().cells
        for index, value in enumerate(record):
            cells[index].text = value

    document.save(SAMPLE_WORD)
    print("Created:", SAMPLE_WORD.name)


def main():
    create_sample_pdf()
    create_sample_form()
    create_sample_word()
    print("\nSample data creation completed!")


if __name__ == "__main__":
    main()