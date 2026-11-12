from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import TableStyle

from .config import OUTPUT_DIR


def create_pdf_report(output_file):
    document = SimpleDocTemplate(str(output_file), pagesize=A4)
    styles = getSampleStyleSheet()

    content = [
        Paragraph("Monthly Business Report", styles["Title"]),
        Spacer(1, 20),
        Paragraph("Generated using Python automation.", styles["Normal"]),
        Spacer(1, 20),
    ]

    data = [
        ["Product", "Quantity", "Amount"],
        ["Laptop", "2", "100000"],
        ["Mouse", "5", "2500"],
        ["Monitor", "2", "30000"],
    ]

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.navy),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    content.append(table)
    document.build(content)
    print("PDF created:", output_file.name)


if __name__ == "__main__":
    create_pdf_report(OUTPUT_DIR / "Generated_Report.pdf")