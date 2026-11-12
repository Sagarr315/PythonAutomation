from pypdf import PdfReader, PdfWriter

from .config import SAMPLE_FORM, OUTPUT_DIR


def read_form_fields(file_path):
    reader = PdfReader(str(file_path))
    fields = reader.get_fields()

    if not fields:
        print("No fillable form fields found.")
        return

    print("PDF form fields:")

    for field_name, field in fields.items():
        print(field_name, "=", field.get("/V"))


def fill_pdf_form(input_file, output_file, field_values):
    reader = PdfReader(str(input_file))
    writer = PdfWriter()

    writer.clone_document_from_reader(reader)

    for page in writer.pages:
        writer.update_page_form_field_values(
            page,
            field_values,
            auto_regenerate=False,
        )

    with open(output_file, "wb") as file:
        writer.write(file)

    writer.close()
    print("Filled PDF form:", output_file.name)


if __name__ == "__main__":
    read_form_fields(SAMPLE_FORM)

    fill_pdf_form(
        SAMPLE_FORM,
        OUTPUT_DIR / "Filled_Form.pdf",
        {
            "employee_name": "Employee_101",
            "department": "IT",
            "employee_id": "E101",
        },
    )